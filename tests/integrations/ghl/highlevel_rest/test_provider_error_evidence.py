from __future__ import annotations

import hashlib
import json
import logging
import socket
from typing import Any, Mapping

import pytest

from integrations.ghl.highlevel_rest.live_note_http_client import (
    ConcreteLiveNoteHttpClient,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    ALTERNATE_ROUTE,
    AUTOMATIC_RETRY,
    BoundedLiveNoteTransport,
    GENERIC_EXECUTE,
    InjectedLiveNoteCredential,
    LiveNoteHttpResult,
    LiveNoteTransportError,
    POST_ATTEMPTS_MAX,
    RAW_REST_FALLBACK,
    READBACK_GET_ATTEMPTS_MAX,
    REQUEST_TIMEOUT_SECONDS,
    TOTAL_MUTATION_CALLS_MAX,
    TOTAL_NETWORK_CALLS_MAX,
    derive_private_provider_error_evidence,
    project_public_provider_error_evidence,
    public_provider_error_projection_from_result,
)


SYNTHETIC_TOKEN = "synthetic-provider-error-token-never-persist"
SYNTHETIC_CONTACT_ID = "synthetic-contact-error-001"
NOTE_PATH = f"/contacts/{SYNTHETIC_CONTACT_ID}/notes"


def _result(
    status_code: int,
    body: bytes,
    headers: Mapping[str, str] | None = None,
) -> LiveNoteHttpResult:
    return LiveNoteHttpResult(
        status_code=status_code,
        body=body,
        headers=dict(headers or {}),
    )


def _json_body(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def test_success_path_unchanged_with_optional_headers() -> None:
    body = _json_body(
        {
            "note": {
                "id": "synthetic-note-ok",
                "body": "created",
                "contactId": SYNTHETIC_CONTACT_ID,
            }
        }
    )
    result = _result(201, body, {"Content-Type": "application/json", "X-Request-Id": "ok-1"})
    assert result.status_code == 201
    assert result.body == body
    assert result.headers["X-Request-Id"] == "ok-1"
    with pytest.raises(LiveNoteTransportError, match="non-2xx"):
        derive_private_provider_error_evidence(result)


def test_403_json_with_correlation_header() -> None:
    body = _json_body(
        {
            "statusCode": 403,
            "message": "private synthetic forbidden detail",
            "error": "Forbidden",
            "errorCode": "forbidden_scope",
        }
    )
    result = _result(
        403,
        body,
        {
            "Content-Type": "application/json; charset=utf-8",
            "X-Correlation-Id": "corr-403-fixture",
            "X-Request-Id": "req-403-fixture",
            "Authorization": "Bearer must-not-enter-evidence",
            "X-Unknown-Header": "ignored-for-public",
        },
    )
    private = derive_private_provider_error_evidence(result)
    public = project_public_provider_error_evidence(private).as_public_dict()

    assert private.PROVIDER_HTTP_STATUS == 403
    assert private.CONTENT_TYPE_CLASS == "JSON"
    assert private.RESPONSE_BODY_LENGTH == len(body)
    assert private.RESPONSE_BODY_SHA256 == hashlib.sha256(body).hexdigest()
    assert private.PROVIDER_ERROR_ENVELOPE_PARSEABLE is True
    assert private.PROVIDER_ERROR_CODE == "forbidden_scope"
    assert private.PROVIDER_ERROR_MESSAGE == "private synthetic forbidden detail"
    assert private.PROVIDER_REQUEST_ID == "req-403-fixture"
    assert private.PROVIDER_CORRELATION_ID == "corr-403-fixture"
    assert private.PROVIDER_ERROR_CLASS == "AUTHORIZATION"
    assert private.PROVIDER_ERROR_CAUSE == "UNKNOWN"
    assert private.CONTENT_TYPE is not None
    # Authorization is stripped during private header normalization for evidence.
    assert "Bearer must-not-enter-evidence" not in repr(private)
    assert "Bearer must-not-enter-evidence" not in str(private)

    assert public == {
        "PROVIDER_HTTP_STATUS": 403,
        "PROVIDER_CONTENT_TYPE_CLASS": "JSON",
        "PROVIDER_ERROR_ENVELOPE_PRESENT": "YES",
        "PROVIDER_ERROR_CODE_PRESENT": "YES",
        "PROVIDER_ERROR_MESSAGE_PRESENT": "YES",
        "PROVIDER_REQUEST_ID_PRESENT": "YES",
        "PROVIDER_CORRELATION_ID_PRESENT": "YES",
        "PROVIDER_ERROR_CLASS": "AUTHORIZATION",
        "PROVIDER_ERROR_CAUSE": "UNKNOWN",
        "RAW_PROVIDER_RESPONSE_PUBLISHED": "NO",
        "PROVIDER_ERROR_MESSAGE_PUBLISHED": "NO",
        "PROVIDER_REQUEST_ID_PUBLISHED": "NO",
        "PROVIDER_CORRELATION_ID_PUBLISHED": "NO",
        "AUTHORIZATION_HEADER_PUBLISHED": "NO",
        "TOKEN_OR_PIT_PUBLISHED": "NO",
    }
    rendered_public = json.dumps(public)
    assert "private synthetic forbidden detail" not in rendered_public
    assert "corr-403-fixture" not in rendered_public
    assert "req-403-fixture" not in rendered_public
    assert "forbidden_scope" not in rendered_public
    assert SYNTHETIC_TOKEN not in rendered_public


def test_403_json_without_headers() -> None:
    body = _json_body({"message": "denied", "code": "E_DENIED"})
    private = derive_private_provider_error_evidence(
        _result(403, body, {"Content-Type": "application/json"})
    )
    public = project_public_provider_error_evidence(private)

    assert private.PROVIDER_REQUEST_ID is None
    assert private.PROVIDER_CORRELATION_ID is None
    assert public.PROVIDER_REQUEST_ID_PRESENT == "NO"
    assert public.PROVIDER_CORRELATION_ID_PRESENT == "NO"
    assert public.PROVIDER_ERROR_CLASS == "AUTHORIZATION"
    assert public.PROVIDER_ERROR_CAUSE == "UNKNOWN"


def test_403_non_json_body() -> None:
    body = b"<html>forbidden</html>"
    private = derive_private_provider_error_evidence(
        _result(403, body, {"Content-Type": "text/html; charset=utf-8"})
    )
    public = project_public_provider_error_evidence(private)

    assert private.CONTENT_TYPE_CLASS == "HTML"
    assert private.PROVIDER_ERROR_ENVELOPE_PARSEABLE is False
    assert private.PROVIDER_ERROR_CODE is None
    assert private.PROVIDER_ERROR_MESSAGE is None
    assert public.PROVIDER_CONTENT_TYPE_CLASS == "HTML"
    assert public.PROVIDER_ERROR_ENVELOPE_PRESENT == "UNKNOWN"
    assert public.PROVIDER_ERROR_CODE_PRESENT == "NO"
    assert public.PROVIDER_ERROR_MESSAGE_PRESENT == "NO"
    assert public.PROVIDER_ERROR_CLASS == "AUTHORIZATION"


def test_403_empty_body() -> None:
    private = derive_private_provider_error_evidence(_result(403, b"", {}))
    public = project_public_provider_error_evidence(private)

    assert private.CONTENT_TYPE_CLASS == "EMPTY"
    assert private.RESPONSE_BODY_LENGTH == 0
    assert private.RESPONSE_BODY_SHA256 == hashlib.sha256(b"").hexdigest()
    assert private.PROVIDER_ERROR_ENVELOPE_PARSEABLE is False
    assert public.PROVIDER_CONTENT_TYPE_CLASS == "EMPTY"
    assert public.PROVIDER_ERROR_ENVELOPE_PRESENT == "NO"
    assert public.PROVIDER_ERROR_CLASS == "AUTHORIZATION"


def test_401_json_authentication_class() -> None:
    body = _json_body({"message": "invalid token", "error": "Unauthorized"})
    public = public_provider_error_projection_from_result(
        _result(401, body, {"Content-Type": "application/json", "Request-Id": "r-401"})
    )
    assert public["PROVIDER_HTTP_STATUS"] == 401
    assert public["PROVIDER_ERROR_CLASS"] == "AUTHENTICATION"
    assert public["PROVIDER_ERROR_CAUSE"] == "UNKNOWN"
    assert public["PROVIDER_REQUEST_ID_PRESENT"] == "YES"
    assert public["PROVIDER_ERROR_MESSAGE_PRESENT"] == "YES"
    assert "invalid token" not in json.dumps(public)


def test_422_validation_envelope() -> None:
    body = _json_body(
        {
            "message": ["pipelineStageId must be a UUID"],
            "error": "Unprocessable Entity",
            "statusCode": 422,
        }
    )
    private = derive_private_provider_error_evidence(
        _result(422, body, {"Content-Type": "application/json"})
    )
    public = project_public_provider_error_evidence(private)

    assert private.PROVIDER_ERROR_CLASS == "REQUEST_VALIDATION"
    # Nested/array message shapes remain non-string; code can still be present.
    assert private.PROVIDER_ERROR_CODE == "422"
    assert private.PROVIDER_ERROR_MESSAGE == "Unprocessable Entity"
    assert public.PROVIDER_ERROR_CLASS == "REQUEST_VALIDATION"
    assert public.PROVIDER_ERROR_CODE_PRESENT == "YES"
    assert public.PROVIDER_ERROR_MESSAGE_PRESENT == "YES"
    assert "pipelineStageId must be a UUID" not in public.as_public_dict().values()


def test_429_rate_limit_class() -> None:
    public = public_provider_error_projection_from_result(
        _result(
            429,
            b"slow down",
            {"Content-Type": "text/plain", "X-Correlation-Id": "rate-1"},
        )
    )
    assert public["PROVIDER_ERROR_CLASS"] == "RATE_LIMIT"
    assert public["PROVIDER_CONTENT_TYPE_CLASS"] == "TEXT"
    assert public["PROVIDER_CORRELATION_ID_PRESENT"] == "YES"
    assert public["PROVIDER_ERROR_ENVELOPE_PRESENT"] == "UNKNOWN"


def test_500_text_html_provider_failure() -> None:
    public = public_provider_error_projection_from_result(
        _result(500, b"<html>error</html>", {"Content-Type": "text/html"})
    )
    assert public["PROVIDER_HTTP_STATUS"] == 500
    assert public["PROVIDER_ERROR_CLASS"] == "PROVIDER_FAILURE"
    assert public["PROVIDER_CONTENT_TYPE_CLASS"] == "HTML"
    assert public["PROVIDER_ERROR_ENVELOPE_PRESENT"] == "UNKNOWN"


def test_malformed_json_envelope() -> None:
    body = b'{"message":'
    private = derive_private_provider_error_evidence(
        _result(403, body, {"Content-Type": "application/json"})
    )
    public = project_public_provider_error_evidence(private)

    assert private.CONTENT_TYPE_CLASS == "JSON"
    assert private.PROVIDER_ERROR_ENVELOPE_PARSEABLE is False
    assert private.PROVIDER_ERROR_CODE is None
    assert private.PROVIDER_ERROR_MESSAGE is None
    assert public.PROVIDER_ERROR_ENVELOPE_PRESENT == "NO"
    assert public.PROVIDER_ERROR_CODE_PRESENT == "NO"
    assert public.PROVIDER_ERROR_MESSAGE_PRESENT == "NO"


def test_default_headers_backward_compatible_positional_constructor() -> None:
    result = LiveNoteHttpResult(403, b"{}")
    assert result.headers == {}
    assert result.status_code == 403


def test_authorization_header_never_persisted_in_public_or_private_repr(
    caplog: pytest.LogCaptureFixture,
) -> None:
    body = _json_body({"message": "no"})
    result = _result(
        403,
        body,
        {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SYNTHETIC_TOKEN}",
            "X-Request-Id": "private-request-id",
        },
    )
    private = derive_private_provider_error_evidence(result)
    public = project_public_provider_error_evidence(private)

    with caplog.at_level(logging.DEBUG):
        rendered = "\n".join(
            [
                repr(private),
                str(private),
                repr(public),
                str(public),
                json.dumps(public.as_public_dict()),
                caplog.text,
            ]
        )
    assert SYNTHETIC_TOKEN not in rendered
    assert "Bearer " not in rendered
    assert "Authorization" not in rendered
    assert "private-request-id" not in json.dumps(public.as_public_dict())
    assert public.AUTHORIZATION_HEADER_PUBLISHED == "NO"
    assert public.TOKEN_OR_PIT_PUBLISHED == "NO"
    assert public.RAW_PROVIDER_RESPONSE_PUBLISHED == "NO"


def test_transport_budgets_and_no_retry_flags_unchanged(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("real network is forbidden in provider error evidence tests")

    monkeypatch.setattr(socket, "socket", _forbid)
    monkeypatch.setattr(socket, "create_connection", _forbid)

    assert AUTOMATIC_RETRY is False
    assert ALTERNATE_ROUTE is False
    assert GENERIC_EXECUTE is False
    assert RAW_REST_FALLBACK is False
    assert POST_ATTEMPTS_MAX == 1
    assert READBACK_GET_ATTEMPTS_MAX == 1
    assert TOTAL_NETWORK_CALLS_MAX == 2
    assert TOTAL_MUTATION_CALLS_MAX == 1
    assert ConcreteLiveNoteHttpClient.AUTOMATIC_RETRY is False
    assert ConcreteLiveNoteHttpClient.ALTERNATE_ROUTE is False
    assert ConcreteLiveNoteHttpClient.GENERIC_REST_FALLBACK is False

    class _OneShot:
        def __init__(self) -> None:
            self.calls = 0

        def request(self, **_kwargs: object) -> LiveNoteHttpResult:
            self.calls += 1
            return _result(
                201,
                _json_body(
                    {
                        "note": {
                            "id": "n-ok",
                            "body": "created",
                            "contactId": SYNTHETIC_CONTACT_ID,
                        }
                    }
                ),
                {"Content-Type": "application/json"},
            )

    session = _OneShot()
    client = ConcreteLiveNoteHttpClient(session=session)  # type: ignore[arg-type]
    transport = BoundedLiveNoteTransport(
        bound_contact_id=SYNTHETIC_CONTACT_ID,
        credential=InjectedLiveNoteCredential(SYNTHETIC_TOKEN),
        http_client=client,
    )
    response = transport.dispatch("POST", NOTE_PATH, {"body": "created"})
    assert response.status == "ok"
    assert session.calls == 1
    assert transport.post_attempts == 1
    assert transport.total_network_calls == 1
    assert client.default_timeout_seconds == REQUEST_TIMEOUT_SECONDS


def test_required_verification_predicates() -> None:
    fixtures = [
        _result(
            403,
            _json_body({"message": "x", "code": "c"}),
            {"Content-Type": "application/json", "X-Correlation-Id": "c1"},
        ),
        _result(403, _json_body({"message": "x"}), {"Content-Type": "application/json"}),
        _result(403, b"plain", {"Content-Type": "text/plain"}),
        _result(403, b"", {}),
        _result(401, _json_body({"message": "auth"}), {"Content-Type": "application/json"}),
        _result(422, _json_body({"error": "bad"}), {"Content-Type": "application/json"}),
        _result(429, b"wait", {"Content-Type": "text/plain"}),
        _result(500, b"<html></html>", {"Content-Type": "text/html"}),
        _result(403, b"{", {"Content-Type": "application/json"}),
    ]
    for fixture in fixtures:
        private = derive_private_provider_error_evidence(fixture)
        public = project_public_provider_error_evidence(private)
        assert private.PROVIDER_HTTP_STATUS == fixture.status_code
        assert private.CONTENT_TYPE_CLASS in {
            "JSON",
            "TEXT",
            "HTML",
            "EMPTY",
            "OTHER",
            "UNKNOWN",
        }
        assert public.PROVIDER_ERROR_CLASS in {
            "AUTHENTICATION",
            "AUTHORIZATION",
            "REQUEST_VALIDATION",
            "NOT_FOUND",
            "CONFLICT",
            "RATE_LIMIT",
            "PROVIDER_FAILURE",
            "UNKNOWN",
        }
        assert public.PROVIDER_REQUEST_ID_PRESENT in {"YES", "NO"}
        assert public.PROVIDER_CORRELATION_ID_PRESENT in {"YES", "NO"}
        assert public.RAW_PROVIDER_RESPONSE_PUBLISHED == "NO"

    assert AUTOMATIC_RETRY is False
    assert ALTERNATE_ROUTE is False
    assert TOTAL_NETWORK_CALLS_MAX == 2
    assert TOTAL_MUTATION_CALLS_MAX == 1
