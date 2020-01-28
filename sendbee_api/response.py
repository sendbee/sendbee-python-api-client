from typing import Any, Type, List, Union

from sendbee_api.formatter import Formatter, Json
from sendbee_api.constants import ClientConst, FormatterConst


class Response:
    """Response object returned from API call."""

    def __init__(self, data: Any, status_code: int,
                 formatter: Type[Formatter],
                 api_request):
        self._data = data
        self._model = api_request.model

        self.api_reguest = api_request
        self.formatter = formatter(self)
        self.status_code = status_code

        self._response_data = {
            FormatterConst.FORMATTED: None,
            ClientConst.MODELS: [],
            ClientConst.META: None
        }

    def __iter__(self):
        return iter(self.models)

    @property
    def raw_data(self) -> Any:
        """Return data as is from the server."""

        return self._data

    @property
    def formatted_data(self) -> Union[Type[Json], None]:
        """Format data using selected formatter."""

        if self._response_data[FormatterConst.FORMATTED] is None:
            self._response_data[FormatterConst.FORMATTED] = \
                self.formatter.format(self._data)

        return self._response_data[FormatterConst.FORMATTED]

    @property
    def models(self) -> Union[List[object], None]:
        """Transform raw data into models."""

        if not self._response_data[ClientConst.MODELS]:
            formatted_data = self.formatter.format(self._data)
            if not isinstance(formatted_data, list):
                formatted_data = [formatted_data]
            self._response_data[ClientConst.MODELS] = \
                self._model.process(formatted_data)

        return self._response_data[ClientConst.MODELS]

    @property
    def meta(self) -> Union[List[object], None]:
        """Transform raw meta data into models."""

        if not self._response_data[ClientConst.META]:
            from sendbee_api.models import Meta
            formatted_data = self.formatter.format_meta(self._data)
            self._response_data[ClientConst.META] = \
                Meta.process([formatted_data])[0]

        return self._response_data[ClientConst.META]
