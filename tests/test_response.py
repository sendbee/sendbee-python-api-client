"""Tests for the Response wrapper: lazy unwrap and pagination helpers."""

import ujson

from sendbee_api.response import Response
from sendbee_api.formatter import Json
from sendbee_api.fields import TextField
from sendbee_api.models import Model


class _Item(Model):
    _id = TextField(index="id")
    _name = TextField(index="name")


class _ApiRequestStub:
    model = _Item


def _build_response(body, headers=None, status=200):
    return Response(body, headers or {}, status, Json, _ApiRequestStub())


def test_models_property_returns_parsed_model_instances_from_data_envelope():
    """Response.models maps each `data` entry to a model instance."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}],
        "meta": {"current_page": 1, "last_page": 1, "total": 2},
    })

    response = _build_response(body)

    assert [m.name for m in response.models] == ["a", "b"]


def test_iter_delegates_to_models():
    """`for m in response` iterates response.models."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}],
        "meta": {"current_page": 1, "last_page": 1, "total": 1},
    })

    response = _build_response(body)

    assert [m.name for m in response] == ["a"]


def test_raw_data_returns_input_string_unchanged():
    """`raw_data` is the unparsed body."""
    body = '{"data": []}'

    response = _build_response(body)

    assert response.raw_data == body


def test_meta_exposes_current_and_last_page_as_int():
    """Pagination meta is parsed via Meta model into ints."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}],
        "meta": {"current_page": 1, "last_page": 3, "total": 25},
    })

    response = _build_response(body)

    assert response.meta.current_page == 1
    assert response.meta.last_page == 3


def test_has_next_returns_true_when_more_pages_remain():
    """has_next() is True iff current_page < last_page."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}],
        "meta": {"current_page": 1, "last_page": 3},
    })

    response = _build_response(body)

    assert response.has_next() is True


def test_has_next_returns_false_on_final_page():
    """has_next() is False when current_page equals last_page."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}],
        "meta": {"current_page": 3, "last_page": 3},
    })

    response = _build_response(body)

    assert response.has_next() is False


def test_next_page_returns_current_page_plus_one():
    """next_page() advances by exactly one."""
    body = ujson.dumps({
        "data": [{"id": "1", "name": "a"}],
        "meta": {"current_page": 2, "last_page": 5},
    })

    response = _build_response(body)

    assert response.next_page() == 3


def test_warning_returns_server_warning_string_when_present():
    """Warning text from the envelope is exposed via .warning."""
    body = ujson.dumps({"data": [], "warning": "deprecated-endpoint"})

    response = _build_response(body)

    assert response.warning == "deprecated-endpoint"
