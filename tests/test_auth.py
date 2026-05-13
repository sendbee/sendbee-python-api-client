"""Tests for SendbeeAuth: HMAC token generation and verification."""

import base64
import hmac
import hashlib
from datetime import datetime, timezone

import pytest

from sendbee_api.auth import SendbeeAuth


def test_get_auth_token_returns_base64_encoded_timestamp_dot_hmac():
    """Token format is base64(<unix_ts>.<sha256_hmac_hex>)."""
    auth = SendbeeAuth("secret")

    token = auth.get_auth_token()

    decoded = base64.b64decode(token).decode("utf-8")
    timestamp, hex_digest = decoded.split(".")
    assert timestamp.isdigit()
    assert len(hex_digest) == 64
    int(hex_digest, 16)


def test_get_auth_token_uses_hmac_sha256_of_timestamp_under_private_key(monkeypatch):
    """HMAC payload is the timestamp string, key is the private key."""
    fixed_ts = 1700000000
    secret = "secret-bytes"

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(fixed_ts, tz=tz)

    monkeypatch.setattr("sendbee_api.auth.datetime", _FrozenDatetime)

    expected_hmac = hmac.new(
        secret.encode("utf-8"),
        str(fixed_ts).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    token = SendbeeAuth(secret).get_auth_token()

    decoded = base64.b64decode(token).decode("utf-8")
    timestamp, hex_digest = decoded.split(".")
    assert timestamp == str(fixed_ts)
    assert hex_digest == expected_hmac


def test_get_auth_token_changes_when_timestamp_changes(monkeypatch):
    """Two tokens generated at different timestamps differ."""
    secret = "secret"
    timestamps = iter([1700000000, 1700000001])

    class _CountingDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(next(timestamps), tz=tz)

    monkeypatch.setattr("sendbee_api.auth.datetime", _CountingDatetime)

    token_a = SendbeeAuth(secret).get_auth_token()
    token_b = SendbeeAuth(secret).get_auth_token()

    assert token_a != token_b


def test_check_auth_token_returns_true_for_self_generated_token():
    """A token produced by get_auth_token verifies under the same secret."""
    auth = SendbeeAuth("secret")

    token = auth.get_auth_token()

    assert auth.check_auth_token(token) is True


def test_check_auth_token_returns_false_when_hmac_tampered():
    """A token whose HMAC has been altered fails verification."""
    auth = SendbeeAuth("secret")
    token = auth.get_auth_token()
    decoded = base64.b64decode(token).decode("utf-8")
    timestamp, hex_digest = decoded.split(".")
    tampered_hex = ("0" if hex_digest[0] != "0" else "1") + hex_digest[1:]
    tampered = base64.b64encode(
        f"{timestamp}.{tampered_hex}".encode("utf-8")
    ).decode("utf-8")

    assert auth.check_auth_token(tampered) is False


def test_check_auth_token_returns_false_when_secret_differs():
    """A token signed with secret A cannot be verified with secret B."""
    token = SendbeeAuth("secret-a").get_auth_token()
    other = SendbeeAuth("secret-b")

    assert other.check_auth_token(token) is False


def test_constructor_accepts_str_and_bytes_keys():
    """Both str and bytes private keys produce identical tokens."""
    fixed_ts = b"1700000000"
    expected = hmac.new(b"secret", fixed_ts, hashlib.sha256).hexdigest()

    str_auth = SendbeeAuth("secret")
    bytes_auth = SendbeeAuth(b"secret")

    assert str_auth._get_encrypted_key(fixed_ts) == expected
    assert bytes_auth._get_encrypted_key(fixed_ts) == expected
