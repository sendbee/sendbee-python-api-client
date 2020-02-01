import hmac
import base64
import hashlib
from datetime import datetime, timezone

import requests
from abc import ABCMeta
from typing import Union

from sendbee_api.debug import Debug
from sendbee_api.auth import SendbeeAuth
from sendbee_api.response import Response
from sendbee_api.formatter import FormatterFactory
from sendbee_api.exceptions import SendbeeRequestApiException
from sendbee_api.constants import RequestConst, ResponseConst, ClientConst, \
    TestConst, ResponseCode, BoolConst, MiscConst


class Api(metaclass=ABCMeta):
    """Abstract API class."""


def bind_request(**request_data) -> 'callable':
    """Binds request class to client property, dynamically."""

    class Request(Api):
        """Request class. Does the actual API request."""

        model = request_data.get(ClientConst.MODEL)
        api_path = request_data.get(RequestConst.API_PATH)
        formatter = request_data.get(ClientConst.FORMATTER)
        method = request_data.get(RequestConst.METHOD, RequestConst.GET)
        query_parameters = request_data.get(RequestConst.QUERY_PARAMETERS)
        fake_response_path = request_data.get(TestConst.FAKE_RESPONSE_PATH)
        default_parameters = request_data.get(RequestConst.DEFAULT_PARAMETERS, {})

        def __init__(self, client, debug: 'Debug',
                     *path_params, **query_params):
            client.request = self

            self.url = None
            self.debug = debug
            self.client = client
            self.parameters = {RequestConst.QUERY: {},
                               RequestConst.PATH: []}

            self._timeout = 5

            self._set_parameters(*path_params, **query_params)

        def _set_parameters(self, *path_params, **query_params) -> None:
            """
            Prepares the list of query parameters
            :path_params: list of path parameters
            :query_params: dict of query parameters
            :return: None
            """

            # take timeout
            try:
                self._timeout = int(query_params.get(RequestConst.TIMEOUT,
                                                     self._timeout))
            except ValueError:
                pass
            try:
                del query_params[RequestConst.TIMEOUT]
            except KeyError:
                pass

            # set default API call params
            for key, value in self.default_parameters.items():
                self.parameters[RequestConst.QUERY][key] = value

            _query_params = self.query_parameters.get_params()

            # set API call params defined during the "call" invocation
            for key, value in query_params.items():
                if value is None:
                    continue

                if key in _query_params.values():
                    self.parameters[RequestConst.QUERY][key] = value

                elif key in _query_params.keys():
                    self.parameters[RequestConst.QUERY][_query_params[key]] = value

            # transform all True and False param to 1 and 0
            for key, value in self.parameters[RequestConst.QUERY].items():
                if value is True:
                    self.parameters[RequestConst.QUERY][key] = BoolConst.TRUE
                if value is False:
                    self.parameters[RequestConst.QUERY][key] = BoolConst.FALSE

            # set optional url path params
            for value in path_params:
                self.parameters[RequestConst.PATH].append(value)

            # set business_id param if one is provided
            if self.client.business_id:
                self.parameters[RequestConst.QUERY]['business_id'] = \
                    self.client.business_id

        def _prepare_url(self) -> str:
            """
            Prepares url and query parameters for the request
            :return: URL
            """

            base_url = '{}://{}{}'.format(
                self.client.protocol, self.client.base_url, self.api_path
            )
            url_parts = '/'.join(
                [part for part in self.parameters[RequestConst.PATH]]
            )

            if url_parts:
                final_url = '{}/{}'.format(base_url, url_parts)
            else:
                final_url = base_url

            if self.method == RequestConst.GET:
                params = self.parameters[RequestConst.QUERY]
                for param, value in params.items():
                    if isinstance(value, list):
                        params[param] = ','.join(value)
                    elif isinstance(value, dict):
                        params[param] = ','.join([f'{k}:{v}' for k, v in value])

                url_query = '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
                final_url = '{}{}'.format(final_url, url_query)

            self.debug.ok('final url', final_url)

            return final_url

        def _headers(self) -> dict:
            """Construct headers data with authentication part"""

            auth_token = SendbeeAuth(self.client.secret).get_auth_token()
            headers = {
                'X-Authorization': auth_token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            self.debug.ok('headers', headers)

            return headers

        def _do_request(self, url: str) -> (int, dict):
            """
            Makes the request to Sendbee Api servers
            :url: Url for the request
            :return: Tuple with two elements, status code and content
            """

            self.debug.ok('method', self.method)

            if self.client.fake_response_path:
                with open(self.client.fake_response_path, 'r') as f:
                    return ResponseCode.OK, f.read()

            elif self.method == RequestConst.GET:
                response = requests.get(
                    url, headers=self._headers(), timeout=self._timeout
                )

                self.debug.ok(
                    RequestConst.QUERY_PARAMETERS,
                    self.parameters[RequestConst.QUERY]
                )
                self.debug.ok(ResponseConst.RESPONSE_OBJECT, response)

                return response.status_code, response.text

            elif self.method in [RequestConst.POST, RequestConst.PUT,
                                 RequestConst.DELETE]:

                if self.method == RequestConst.POST:
                    send_request = requests.post
                elif self.method == RequestConst.PUT:
                    send_request = requests.put
                elif self.method == RequestConst.DELETE:
                    send_request = requests.delete

                response = send_request(
                    url, json=self.parameters[RequestConst.QUERY],
                    headers=self._headers(), timeout=self._timeout
                )

                self.debug.ok('payload', self.parameters[RequestConst.QUERY])
                self.debug.ok(ResponseConst.RESPONSE_OBJECT, response)

                return response.status_code, response.text

            else:
                return ResponseCode.NOT_FOUND, {}

        def _process_response(self, status_code: int, response: str) -> 'Response':
            """
            Process response using models
            :status_code: Response status code
            :response: Content
            :return: Response object
            """

            formatter = self.formatter
            if not formatter:
                formatter = FormatterFactory(
                    self.parameters[RequestConst.QUERY][RequestConst.PROTOCOL])\
                    .get_formatter()

            response = Response(response, status_code, formatter, self)

            if status_code >= ResponseCode.BAD_REQUEST:

                error_message = response.formatted_data
                if 'error' not in error_message:
                    error_message = \
                        ResponseConst.DEFAULT_ERROR_MESSAGE

                self.debug.error(ResponseConst.STATUS_CODE, status_code)
                self.debug.error(
                    ResponseConst.RESPONSE, response.formatted_data
                )

                error_msg = error_message.get('error', {})\
                    .get('detail', 'Unrecognized error')
                raise SendbeeRequestApiException(error_msg)
            else:
                self.debug.ok(ResponseConst.STATUS_CODE, status_code)
                self.debug.ok(ResponseConst.RESPONSE, response.raw_data)

            if self.method in [RequestConst.POST, RequestConst.PUT,
                               RequestConst.DELETE]:
                return response.models[0]
            else:
                return response

        def call(self) -> 'Response':
            """
            Makes the API call
            :return: Return value from self._process_response()
            """

            self.url = self._prepare_url()
            status_code, response = self._do_request(self.url)
            return self._process_response(status_code, response)

    def call(client, *path_params, **query_params) -> Union['Response', None]:
        """
        Binded method for API calls
        :path_params: list of path parameters
        :query_params: dict of query parameters
        :return: Return value from Request.call()
        """

        if MiscConst.PRINT_PARAMS in query_params:
            Request.query_parameters.print_params()
            return

        with Debug(client=client) as debug:
            request = Request(client, debug, *path_params, **query_params)
            return request.call()

    call.__doc__ = request_data.get(ClientConst.DESCRIPTION)

    return call
