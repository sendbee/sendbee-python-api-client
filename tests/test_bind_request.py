"""Tests for the bind_request factory.

The factory in `sendbee_api/bind.py` is the core that every endpoint method
funnels through. These tests cover: request construction, query/path/body
serialization, header generation including the HMAC auth token, single vs.
multi-model response shaping, error mapping to exceptions, pagination
boundary behavior, warning surfacing, and the print_params escape hatch.

All tests mock at the `requests` HTTP layer via the `responses` library, so
they exercise the real `_do_request` -> `_process_response` path.
"""

import base64
from urllib.parse import urlparse, parse_qs

import pytest
import responses
import ujson

from sendbee_api import constants
from sendbee_api.auth import SendbeeAuth
from sendbee_api.bind import bind_request
from sendbee_api.exceptions import (
    SendbeeRequestApiException,
    PaginationException,
)
from sendbee_api.fields import TextField, NumberField, ModelField
from sendbee_api.models import Model
from sendbee_api.query_params import QueryParams


class _Item(Model):
    """Test-only response model with two text fields."""
    _id = TextField(index="id")
    _name = TextField(index="name")


class _DemoQueryParams(QueryParams):
    """Test-only query params covering python<->wire name aliasing."""
    name = "name", "Contact name"
    search_query = "search_query", "Free text filter"
    tags = "tags", "Tag list"
    active = "active", "Active flag"
    page = "page", "Page number"


def _client():
    """Build a fresh client. Imported here to avoid module-load coupling."""
    from sendbee_api import SendbeeApi
    return SendbeeApi("test-key", "test-secret")


def _make_get(api_path="/demo", **kw):
    return bind_request(
        api_path=api_path,
        model=_Item,
        query_parameters=_DemoQueryParams,
        **kw,
    )


def _make_post(api_path="/demo", **kw):
    return bind_request(
        api_path=api_path,
        model=_Item,
        method=constants.RequestConst.POST,
        query_parameters=_DemoQueryParams,
        **kw,
    )


def _query_dict(call):
    """Parse a responses.calls[i].request.url into a {param: [vals]} dict."""
    return parse_qs(urlparse(call.request.url).query)


# ---------------------------------------------------------------------------
# Request construction: timeout and defaults
# ---------------------------------------------------------------------------

@responses.activate
def test_timeout_kwarg_is_consumed_and_not_sent_as_query_param(json_body, register):
    """timeout=5 controls the HTTP timeout and is stripped from the query."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), timeout=5, name="Alice")

    qs = _query_dict(responses.calls[0])
    assert "timeout" not in qs
    assert qs["name"] == ["Alice"]


@responses.activate
def test_non_integer_timeout_falls_back_without_raising(json_body, register):
    """timeout='abc' does not raise; request still succeeds."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    response = call(_client(), timeout="abc", name="Alice")

    assert response.models == []


@responses.activate
def test_default_parameters_are_merged_into_outgoing_query(json_body, register):
    """Bind-site default_parameters appear in the request query."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get(default_parameters={"name": "default-name"})

    call(_client())

    qs = _query_dict(responses.calls[0])
    assert qs["name"] == ["default-name"]


@responses.activate
def test_call_site_kwarg_overrides_default_parameter_for_same_key(json_body, register):
    """Call-site kwargs win over bind-site defaults."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get(default_parameters={"name": "default-name"})

    call(_client(), name="Bob")

    qs = _query_dict(responses.calls[0])
    assert qs["name"] == ["Bob"]


# ---------------------------------------------------------------------------
# Query param name aliasing
# ---------------------------------------------------------------------------

@responses.activate
def test_python_name_kwarg_is_translated_to_wire_name_in_url(json_body, register):
    """msg_type kwarg becomes msgtype=... in the outgoing URL."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), msg_type="simple")

    qs = _query_dict(responses.calls[0])
    assert qs["msgtype"] == ["simple"]
    assert "msg_type" not in qs


@responses.activate
def test_wire_name_kwarg_is_preserved_as_is(json_body, register):
    """Passing the wire-name directly is preserved in the URL."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), msgtype="extended")

    qs = _query_dict(responses.calls[0])
    assert qs["msgtype"] == ["extended"]


@responses.activate
def test_unknown_kwarg_is_silently_dropped(json_body, register):
    """A kwarg with no matching wire/python name is omitted, no error raised."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), nonsense_param="x", name="Alice")

    qs = _query_dict(responses.calls[0])
    assert "nonsense_param" not in qs
    assert qs["name"] == ["Alice"]


@responses.activate
def test_none_valued_kwarg_is_omitted_from_query(json_body, register):
    """None values are skipped, so the param key does not appear in the URL."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), name=None, search_query="hi")

    qs = _query_dict(responses.calls[0])
    assert "name" not in qs
    assert qs["search_query"] == ["hi"]


# ---------------------------------------------------------------------------
# GET serialization: bool, list, path params
# ---------------------------------------------------------------------------

@responses.activate
def test_boolean_true_is_serialized_as_one_in_query(json_body, register):
    """True becomes '1' in the GET querystring."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), active=True)

    qs = _query_dict(responses.calls[0])
    assert qs["active"] == ["1"]


@responses.activate
def test_boolean_false_is_serialized_as_zero_in_query(json_body, register):
    """False becomes '0' in the GET querystring."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), active=False)

    qs = _query_dict(responses.calls[0])
    assert qs["active"] == ["0"]


@responses.activate
def test_list_value_is_serialized_as_comma_joined_string(json_body, register):
    """tags=['a','b'] is sent as tags=a,b."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), tags=["a", "b"])

    qs = _query_dict(responses.calls[0])
    assert qs["tags"] == ["a,b"]


@responses.activate
def test_positional_path_params_are_appended_to_url(json_body, register):
    """Positional args build base/path/{a}/{b} URL."""
    register("GET", "/demo/abc/def", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client(), "abc", "def")

    actual = responses.calls[0].request.url
    assert "/demo/abc/def" in actual


# ---------------------------------------------------------------------------
# POST/PUT/DELETE: body shape and single-model response
# ---------------------------------------------------------------------------

@responses.activate
def test_post_sends_payload_in_json_body_not_querystring(json_body, register):
    """POST puts parameters in the JSON body and leaves the URL path-only."""
    register("POST", "/demo", body=json_body(data=[{"id": "1", "name": "Alice"}], meta={"current_page": 1, "last_page": 1}))
    call = _make_post()

    call(_client(), name="Alice", search_query="hi")

    request = responses.calls[0].request
    assert urlparse(request.url).query == ""
    body = ujson.loads(request.body)
    assert body == {"name": "Alice", "search_query": "hi"}


@responses.activate
def test_post_returns_single_model_not_response_wrapper(json_body, register):
    """POST auto-triggers single_model_response; result is a Model instance."""
    register("POST", "/demo", body=json_body(data=[{"id": "1", "name": "Alice"}], meta={"current_page": 1, "last_page": 1}))
    call = _make_post()

    result = call(_client(), name="Alice")

    assert isinstance(result, _Item)
    assert result.name == "Alice"


@responses.activate
def test_post_returns_none_when_server_returns_empty_data(json_body, register):
    """Empty data list with POST yields None, not an empty Response."""
    register("POST", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_post()

    result = call(_client(), name="Alice")

    assert result is None


@responses.activate
def test_force_single_model_response_makes_get_return_one_model(json_body, register):
    """force_single_model_response=True on a GET returns one model, not a Response."""
    register("GET", "/demo", body=json_body(data=[{"id": "1", "name": "Alice"}], meta={"current_page": 1, "last_page": 1}))
    call = _make_get(force_single_model_response=True)

    result = call(_client())

    assert isinstance(result, _Item)
    assert result.id == "1"


@responses.activate
def test_put_method_sends_request_with_json_body_and_returns_single_model(json_body, register):
    """PUT path is exercised end-to-end: body in JSON, single-model response."""
    register("PUT", "/demo", body=json_body(data=[{"id": "1", "name": "x"}], meta={"current_page": 1, "last_page": 1}))
    call = bind_request(
        api_path="/demo",
        model=_Item,
        method=constants.RequestConst.PUT,
        query_parameters=_DemoQueryParams,
    )

    result = call(_client(), name="x")

    assert isinstance(result, _Item)
    body = ujson.loads(responses.calls[0].request.body)
    assert body == {"name": "x"}


@responses.activate
def test_delete_method_sends_delete_request_and_returns_single_model(json_body, register):
    """DELETE path returns a single model (typically ServerMessage)."""
    from sendbee_api.models import ServerMessage
    register("DELETE", "/demo", body=json_body(data=[{"message": "deleted"}], meta={"current_page": 1, "last_page": 1}))
    call = bind_request(
        api_path="/demo",
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=_DemoQueryParams,
    )

    result = call(_client(), name="to-delete")

    assert isinstance(result, ServerMessage)
    assert result.message == "deleted"
    assert responses.calls[0].request.method == "DELETE"


# ---------------------------------------------------------------------------
# Headers and auth
# ---------------------------------------------------------------------------

@responses.activate
def test_request_carries_api_key_and_auth_token_headers(json_body, register):
    """X-Api-Key matches client.api_key; X-Auth-Token is a valid HMAC."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()
    client = _client()

    call(client)

    sent_headers = responses.calls[0].request.headers
    assert sent_headers["X-Api-Key"] == client.api_key
    token = sent_headers["X-Auth-Token"]
    assert SendbeeAuth(client.api_secret).check_auth_token(token) is True


@responses.activate
def test_request_carries_static_accept_content_type_and_user_agent(json_body, register):
    """Static SDK headers are present on every outgoing request."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    call(_client())

    headers = responses.calls[0].request.headers
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert headers["User-Agent"] == "Sendbee Python API Client"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@responses.activate
def test_http_400_with_error_detail_raises_with_message_extracted(json_body, register):
    """HTTP 400 + {error:{detail:...}} raises and surfaces the detail string."""
    register(
        "GET", "/demo",
        body=ujson.dumps({"error": {"detail": "Phone is invalid", "type": "validation_error"}}),
        status=400,
    )
    call = _make_get()

    with pytest.raises(SendbeeRequestApiException) as exc_info:
        call(_client())

    assert "Phone is invalid" in str(exc_info.value.args[0])
    assert exc_info.value.response is not None
    assert exc_info.value.response.status_code == 400


@responses.activate
def test_http_400_without_error_key_falls_back_to_default_error_message(json_body, register):
    """A 400 body that doesn't match the {error:{detail}} shape uses default."""
    register("GET", "/demo", body=ujson.dumps({"something_else": "x"}), status=400)
    call = _make_get()

    with pytest.raises(SendbeeRequestApiException) as exc_info:
        call(_client())

    assert exc_info.value.args[0] == constants.ResponseConst.DEFAULT_ERROR_MESSAGE


@responses.activate
def test_http_404_raises_with_not_found_message_regardless_of_body(json_body, register):
    """404 uses the canonical NOT_FOUND error string."""
    register("GET", "/demo", body=ujson.dumps({"data": []}), status=404)
    call = _make_get()

    with pytest.raises(SendbeeRequestApiException) as exc_info:
        call(_client())

    assert exc_info.value.args[0] == constants.ErrorConst.NOT_FOUND


@responses.activate
def test_ignore_error_true_swallows_4xx_and_returns_response(json_body, register):
    """ignore_error=True on the bind site lets a 400 pass through."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}), status=400)
    call = _make_get(ignore_error=True)

    response = call(_client())

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Pagination edge case
# ---------------------------------------------------------------------------

@responses.activate
def test_pagination_exception_when_page_greater_than_one_returns_empty_data(json_body, register):
    """current_page > 1 with empty data list raises PaginationException."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 2, "last_page": 1}))
    call = _make_get()

    with pytest.raises(PaginationException):
        call(_client(), page=2)


@responses.activate
def test_no_pagination_exception_on_page_one_even_when_data_empty(json_body, register):
    """An empty first page is a valid 'no results', not an exception."""
    register("GET", "/demo", body=json_body(data=[], meta={"current_page": 1, "last_page": 1}))
    call = _make_get()

    response = call(_client())

    assert response.models == []


# ---------------------------------------------------------------------------
# Warnings
# ---------------------------------------------------------------------------

@responses.activate
def test_warning_in_response_is_printed_to_stdout_but_does_not_raise(
    json_body, register, capsys
):
    """A server warning is printed via click.secho and exposed via .warning."""
    register("GET", "/demo", body=json_body(
        data=[],
        meta={"current_page": 1, "last_page": 1},
        warning="deprecated-endpoint",
    ))
    call = _make_get()

    response = call(_client())

    captured = capsys.readouterr()
    assert "deprecated-endpoint" in captured.out
    assert response.warning == "deprecated-endpoint"


# ---------------------------------------------------------------------------
# print_params escape hatch
# ---------------------------------------------------------------------------

@responses.activate
def test_print_params_true_short_circuits_before_any_http_call(capsys):
    """print_params=True returns without making a request."""
    call = _make_get()

    result = call(_client(), print_params=True)

    assert result is None
    assert len(responses.calls) == 0
