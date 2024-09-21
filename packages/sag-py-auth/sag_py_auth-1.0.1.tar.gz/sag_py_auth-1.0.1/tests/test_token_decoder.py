from typing import Any

from mock import Mock
from pytest import MonkeyPatch
from requests import Response

from sag_py_auth import AuthConfig
from sag_py_auth.token_decoder import _get_token_jwk, verify_and_decode_token
from sag_py_auth.token_types import JwkDict


def get_mock(url: str, headers: dict[str, str], timeout: int) -> Response:
    if (url == "https://authserver.com/auth/realms/projectName/protocol/openid-connect/certs"
            and headers["content-type"] == "application/json"):
        return Mock(status_code=200,
                    json=lambda: {"keys": [{"kid": "123456", "kty": "RSA", "alg": "RS256", },
                                           {"kid": "654321", "kty": "RSA", "alg": "RS256", }, ]}, )

    return Response()


def get_unverified_header_mock(token_string: str) -> dict[str, Any]:
    return {"kid": "654321"} if token_string == "validTokenString" else {}


def test__get_token_jwk(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setattr("sag_py_auth.token_decoder.requests.get", get_mock)
    monkeypatch.setattr("sag_py_auth.token_decoder.jwt.get_unverified_header", get_unverified_header_mock)

    # Act
    actual: JwkDict = _get_token_jwk("https://authserver.com/auth/realms/projectName", "validTokenString")

    # Assert
    assert actual == {"kid": "654321", "kty": "RSA", "alg": "RS256"}


def token_jwk(_: Any, __: Any) -> str:
    return "test"


def test_verify_and_decode_token(monkeypatch: MonkeyPatch) -> None:
    # Arrange
    auth_config = AuthConfig(issuer="https://authserver.com/auth/realms/projectName", audience="audienceOne")
    token_string = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHR"
                    "wczovL2F1dGhzZXJ2ZXIuY29tL2F1dGgvcmVhbG1zL3Byb2plY3R"
                    "OYW1lIn0.4Ona6SRNZsy8RNdH46VLEB7fx1XugWjJyLKsZ4KgHyQ")

    monkeypatch.setattr("sag_py_auth.token_decoder._get_token_jwk", token_jwk)

    # Act
    token = verify_and_decode_token(auth_config, token_string)
    # Assert
    assert token is not None
    assert token.get("iss") == "https://authserver.com/auth/realms/projectName"
