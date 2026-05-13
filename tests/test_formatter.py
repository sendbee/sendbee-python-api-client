"""Tests for the Json formatter and FormatterFactory lookup."""

import ujson

from sendbee_api.formatter import Json, FormatterFactory
from sendbee_api import constants


class _StubResponse:
    """Minimal Response stand-in; the formatter only uses it for context."""


def _formatter():
    return Json(_StubResponse())


def test_format_data_unwraps_data_key_from_envelope():
    """{"data": [...]} returns [...] from format_data."""
    body = ujson.dumps({"data": [{"id": "c1"}], "meta": {}})

    result = _formatter().format_data(body)

    assert result == [{"id": "c1"}]


def test_format_data_returns_dict_unchanged_when_no_data_key():
    """Envelope without `data` key passes through as the parsed dict."""
    body = ujson.dumps({"error": {"detail": "bad"}})

    result = _formatter().format_data(body)

    assert result == {"error": {"detail": "bad"}}


def test_format_data_returns_default_error_when_body_is_not_valid_json():
    """Garbage input is replaced by the canonical DEFAULT_ERROR_MESSAGE."""
    result = _formatter().format_data("not-json-at-all")

    assert result == constants.ResponseConst.DEFAULT_ERROR_MESSAGE


def test_format_meta_returns_meta_key_when_present():
    """Envelope's meta block is returned verbatim."""
    body = ujson.dumps({
        "data": [],
        "meta": {"current_page": 2, "last_page": 5, "total": 100},
    })

    result = _formatter().format_meta(body)

    assert result == {"current_page": 2, "last_page": 5, "total": 100}


def test_format_meta_returns_empty_dict_when_meta_key_absent():
    """Dict body without `meta` yields {}."""
    body = ujson.dumps({"data": []})

    assert _formatter().format_meta(body) == {}


def test_format_warning_returns_warning_string_when_present():
    """Warning text is returned as-is."""
    body = ujson.dumps({"data": [], "warning": "rate-limit-soon"})

    assert _formatter().format_warning(body) == "rate-limit-soon"


def test_format_warning_returns_none_when_warning_absent():
    """Missing warning yields None."""
    body = ujson.dumps({"data": []})

    assert _formatter().format_warning(body) is None


def test_formatter_factory_returns_json_class_for_json_key():
    """FormatterFactory exposes the Json class for the 'json' lookup."""
    formatter_cls = FormatterFactory(constants.FormatterConst.JSON).get_formatter()

    assert formatter_cls is Json
