"""Tests for SendbeeApi construction and mixin composition."""

import pytest

from sendbee_api import SendbeeApi
from sendbee_api.exceptions import SendbeeRequestApiException
from sendbee_api.contacts.client import Contacts
from sendbee_api.conversations.client import Messages
from sendbee_api.automation.client import Automation
from sendbee_api.teams.client import Teams
from sendbee_api.rate_limit.client import RateLimit


def test_constructor_raises_when_api_key_missing():
    """Empty api_key raises SendbeeRequestApiException."""
    with pytest.raises(SendbeeRequestApiException):
        SendbeeApi(api_key="", api_secret="s")


def test_constructor_raises_when_api_secret_missing():
    """Empty api_secret raises SendbeeRequestApiException."""
    with pytest.raises(SendbeeRequestApiException):
        SendbeeApi(api_key="k", api_secret="")


def test_constructor_stores_credentials_and_debug_flag():
    """Credentials and debug flag round-trip onto the instance."""
    client = SendbeeApi(api_key="k", api_secret="s", debug=True)

    assert client.api_key == "k"
    assert client.api_secret == "s"
    assert client.debug is True
    assert client.fake_response_path is None


def test_client_inherits_all_five_resource_mixins():
    """Client MRO includes every resource mixin."""
    for mixin in (Contacts, Messages, Automation, Teams, RateLimit):
        assert issubclass(SendbeeApi, mixin), f"{mixin.__name__} missing from MRO"


def test_client_exposes_endpoint_methods_from_each_mixin():
    """One representative method from each mixin is callable on the client."""
    client = SendbeeApi("k", "s")

    assert callable(client.contacts)
    assert callable(client.conversations)
    assert callable(client.chatbot_activity_status)
    assert callable(client.teams)
    assert callable(client.rate_limit_error_test)


def test_auth_property_returns_sendbee_auth_bound_to_api_secret():
    """client.auth is a SendbeeAuth that can verify its own tokens."""
    client = SendbeeApi("k", "secret-xyz")

    token = client.auth.get_auth_token()

    assert client.auth.check_auth_token(token) is True


def test_print_params_for_unknown_method_prints_red_warning(capsys):
    """Calling print_params_for with a bogus name prints a warning, not raises."""
    SendbeeApi.print_params_for("not_a_real_endpoint")

    captured = capsys.readouterr()
    assert "Unknown API method" in captured.out
