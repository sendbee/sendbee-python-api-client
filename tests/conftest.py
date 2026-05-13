"""Shared fixtures for the sendbee-api test suite.

Tests mock at the `requests` HTTP boundary using the `responses` library. The
SDK's documented `fake_response_path` test seam is not used because its branch
in `bind.py` returns a 2-tuple while `call()` unpacks 3 elements.
"""

import ujson
import pytest
import responses as _responses

from sendbee_api import SendbeeApi


API_KEY = "test-key"
API_SECRET = "test-secret"
BASE_URL = "https://api-v2.sendbee.io"


@pytest.fixture
def api_key():
    return API_KEY


@pytest.fixture
def api_secret():
    return API_SECRET


@pytest.fixture
def client():
    """Fresh SendbeeApi instance per test."""
    return SendbeeApi(API_KEY, API_SECRET)


@pytest.fixture
def json_body():
    """Build a Sendbee-shaped JSON envelope as a string.

    The server wraps responses as {"data": ..., "meta": ..., "warning": ...}.
    The Json formatter unwraps these keys; tests pass the inner shapes here.
    """
    def _build(data=None, meta=None, warning=None):
        body = {}
        if data is not None:
            body["data"] = data
        if meta is not None:
            body["meta"] = meta
        if warning is not None:
            body["warning"] = warning
        return ujson.dumps(body)
    return _build


@pytest.fixture
def register():
    """Register a mocked HTTP response on the Sendbee base URL.

    Thin wrapper around responses.add() that prepends BASE_URL so tests stay
    terse. Call as register("GET", "/contacts", body=..., status=...).
    """
    def _register(method, path, body="", status=200, content_type="application/json"):
        method_const = {
            "GET": _responses.GET,
            "POST": _responses.POST,
            "PUT": _responses.PUT,
            "DELETE": _responses.DELETE,
        }[method.upper()]
        _responses.add(
            method_const,
            BASE_URL + path,
            body=body,
            status=status,
            content_type=content_type,
        )
    return _register
