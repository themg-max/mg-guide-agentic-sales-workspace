from __future__ import annotations

import ast
import io
import logging
import socket
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pytest

from integrations.ghl.highlevel_rest.live_note_http_client import (
    ConcreteLiveNoteHttpClient,
    LiveNoteHttpClientError,
    RedactedHttpCallRecord,
    StdlibLiveNoteHttpSession,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    AMBIGUITY_TRUTH,
    AUTOMATIC_RETRY,
    BoundedLiveNoteTransport,
    GENERIC_EXECUTE,
    InjectedLiveNoteCredential,
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
    POST_ATTEMPTS_MAX,
    RAW_REST_FALLBACK,
    READBACK_GET_ATTEMPTS_MAX,
    REQUEST_TIMEOUT_SECONDS,
    TOTAL_MUTATION_CALLS_MAX,
    TOTAL_NETWORK_CALLS_MAX,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"
HTTP_CLIENT_PATH = SOURCE_ROOT / "live_note_http_client.py"
TRANSPORT_PATH = SOURCE_ROOT / "live_note_transport.py"
NOTE_PATH_PATH = SOURCE_ROOT / "note_path.py"

SYNTHETIC_TOKEN = "synthetic-placeholder-token-at8i"
SYNTHETIC_URL = "https://services.leadconnectorhq.com/contacts/synthetic-contact-001/notes"
SYNTHETIC_HEADERS = {
    "Authorization": f"Bearer {SYNTHETIC_TOKEN}",
    "Version": "v3",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


@dataclass
class RecordedSessionCall:
    method: str
    url: str
    headers: dict[str, str]
    body: bytes | None
    timeout_seconds: float
    allow_redirects: bool


class ScriptedSession:
    def __init__(self, outcomes: list[LiveNoteHttpResult | BaseException]) -> None:
        self._outcomes = list(outcomes)
        self.calls: list[RecordedSessionCall] = []

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout_seconds: float,
        allow_redirects: bool,
    ) -> LiveNoteHttpResult:
        self.calls.append(
            RecordedSessionCall(
                method=method,
                url=url,
                headers=dict(headers),
                body=body,
                timeout_seconds=timeout_seconds,
                allow_redirects=allow_redirects,
            )
        )
        if not self._outcomes:
            raise AssertionError("scripted session has no remaining outcomes")
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class CountingRetrySession(ScriptedSession):
    """Session that would allow retries if the client looped incorrectly."""

    def __init__(self) -> None:
        super().__init__(
            [
                LiveNoteHttpUncertainty("first-failure"),
                LiveNoteHttpResult(201, b'{"note":{"id":"n1"}}'),
            ]
        )


def _client(session: ScriptedSession | None = None) -> ConcreteLiveNoteHttpClient:
    return ConcreteLiveNoteHttpClient(session=session)


def test_concrete_http_client_conforms_protocol() -> None:
    session = ScriptedSession([LiveNoteHttpResult(201, b'{"ok":true}')])
    client: ConcreteLiveNoteHttpClient = _client(session)

    result = client.request(
        method="POST",
        url=SYNTHETIC_URL,
        headers=SYNTHETIC_HEADERS,
        body=b'{"body":"created"}',
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    assert isinstance(result, LiveNoteHttpResult)
    assert result.status_code == 201
    assert result.body == b'{"ok":true}'
    assert callable(getattr(client, "request"))
    # Structural protocol surface.
    assert {
        "method",
        "url",
        "headers",
        "body",
        "timeout_seconds",
        "allow_redirects",
    }.issubset(client.request.__code__.co_varnames)


def test_http_client_explicit_timeout() -> None:
    session = ScriptedSession([LiveNoteHttpResult(200, b"{}")])
    client = _client(session)

    assert client.default_timeout_seconds == REQUEST_TIMEOUT_SECONDS
    assert ConcreteLiveNoteHttpClient.DEFAULT_TIMEOUT_SECONDS == REQUEST_TIMEOUT_SECONDS
    assert client.DEFAULT_TIMEOUT_SECONDS == 10.0

    client.request(
        method="GET",
        url=SYNTHETIC_URL,
        headers={"Accept": "application/json"},
        body=None,
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )
    assert session.calls[0].timeout_seconds == REQUEST_TIMEOUT_SECONDS

    with pytest.raises(LiveNoteHttpClientError, match="timeout_seconds"):
        client.request(
            method="GET",
            url=SYNTHETIC_URL,
            headers={},
            body=None,
            timeout_seconds=0,
            allow_redirects=False,
        )
    with pytest.raises(LiveNoteHttpClientError, match="REQUEST_TIMEOUT_SECONDS"):
        ConcreteLiveNoteHttpClient(session=session, default_timeout_seconds=30.0)


def test_http_client_no_automatic_retry() -> None:
    session = CountingRetrySession()
    client = _client(session)

    with pytest.raises(LiveNoteHttpUncertainty, match="first-failure"):
        client.request(
            method="POST",
            url=SYNTHETIC_URL,
            headers=SYNTHETIC_HEADERS,
            body=b"{}",
            timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=False,
        )

    assert len(session.calls) == 1
    assert client.AUTOMATIC_RETRY is False
    assert ConcreteLiveNoteHttpClient.AUTOMATIC_RETRY is False
    source = HTTP_CLIENT_PATH.read_text(encoding="utf-8")
    assert "for _ in range" not in source
    assert "while True" not in source
    assert "tenacity" not in source
    assert "retries" not in source.lower() or "no hidden retry" in source.lower()


def test_http_client_injectable_session() -> None:
    session = ScriptedSession([LiveNoteHttpResult(204, b"")])
    client = ConcreteLiveNoteHttpClient(session=session)

    result = client.request(
        method="GET",
        url=SYNTHETIC_URL + "/note-1",
        headers={"Accept": "application/json"},
        body=None,
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    assert result.status_code == 204
    assert len(session.calls) == 1
    assert session.calls[0].method == "GET"
    assert session.calls[0].allow_redirects is False
    assert isinstance(client.call_history[0], RedactedHttpCallRecord)


def test_http_client_zero_real_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("real network is forbidden during AT8I HTTP client tests")

    monkeypatch.setattr(socket, "socket", _forbid)
    monkeypatch.setattr(socket, "create_connection", _forbid)

    session = ScriptedSession([LiveNoteHttpResult(201, b'{"note":{"id":"n1"}}')])
    client = _client(session)
    result = client.request(
        method="POST",
        url=SYNTHETIC_URL,
        headers=SYNTHETIC_HEADERS,
        body=b'{"body":"x"}',
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )
    assert result.status_code == 201
    assert len(session.calls) == 1


def test_http_client_preserves_allow_redirects_false() -> None:
    session = ScriptedSession([LiveNoteHttpResult(200, b"{}")])
    client = _client(session)

    with pytest.raises(LiveNoteHttpClientError, match="allow_redirects"):
        client.request(
            method="GET",
            url=SYNTHETIC_URL,
            headers={},
            body=None,
            timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
    assert session.calls == []

    client.request(
        method="GET",
        url=SYNTHETIC_URL,
        headers={},
        body=None,
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )
    assert session.calls[0].allow_redirects is False


def test_token_not_logged_and_authorization_header_not_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    session = ScriptedSession([LiveNoteHttpResult(201, b"{}")])
    client = _client(session)

    with caplog.at_level(logging.DEBUG):
        client.request(
            method="POST",
            url=SYNTHETIC_URL,
            headers=SYNTHETIC_HEADERS,
            body=b'{"body":"created"}',
            timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=False,
        )

    rendered = "\n".join(
        [
            repr(client),
            str(client),
            repr(client.call_history),
            str(client.call_history),
            caplog.text,
        ]
    )
    assert SYNTHETIC_TOKEN not in rendered
    assert "Bearer " not in rendered
    assert "Authorization:" not in rendered
    assert "authorization=" not in rendered.lower()
    # History keeps header names only, never values.
    assert client.call_history[0].header_names == tuple(
        sorted(SYNTHETIC_HEADERS)
    )


def test_stdlib_session_maps_timeout_to_uncertainty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = StdlibLiveNoteHttpSession()
    urllib_error = __import__("urllib.error", fromlist=["URLError"])
    urllib_request = __import__("urllib.request", fromlist=["build_opener"])

    def _timeout_open(_request: object, timeout: float = 0) -> None:
        assert timeout == REQUEST_TIMEOUT_SECONDS
        raise urllib_error.URLError(TimeoutError("timed out"))

    class _Opener:
        def open(self, request: object, timeout: float = 0) -> None:
            return _timeout_open(request, timeout=timeout)

    monkeypatch.setattr(
        urllib_request,
        "build_opener",
        lambda *_args, **_kwargs: _Opener(),
    )

    with pytest.raises(LiveNoteHttpUncertainty, match="timeout"):
        session.request(
            method="POST",
            url=SYNTHETIC_URL,
            headers=SYNTHETIC_HEADERS,
            body=b"{}",
            timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=False,
        )


def test_stdlib_session_rejects_redirects() -> None:
    session = StdlibLiveNoteHttpSession()
    with pytest.raises(LiveNoteHttpClientError, match="allow_redirects"):
        session.request(
            method="GET",
            url=SYNTHETIC_URL,
            headers={},
            body=None,
            timeout_seconds=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )


def test_stdlib_redirect_not_followed(monkeypatch: pytest.MonkeyPatch) -> None:
    session = StdlibLiveNoteHttpSession()
    urllib_request = __import__("urllib.request", fromlist=["build_opener"])
    source_url = SYNTHETIC_URL
    alternate_url = (
        "https://services.leadconnectorhq.com/contacts/synthetic-contact-other/notes"
    )
    attempted_urls: list[str] = []

    class _RecordingOpener:
        def __init__(self, no_redirect_handler: object) -> None:
            self._no_redirect_handler = no_redirect_handler

        def open(self, request: object, timeout: float = 0) -> object:
            assert timeout == REQUEST_TIMEOUT_SECONDS
            attempted_urls.append(request.full_url)
            return self._no_redirect_handler.http_error_302(
                request,
                io.BytesIO(b"redirect body"),
                302,
                "Found",
                {"location": alternate_url},
            )

    def _build_opener(*handlers: object) -> _RecordingOpener:
        no_redirect_handler = next(
            handler
            for handler in handlers
            if handler.__class__.__name__ == "_NoRedirectHandler"
        )
        return _RecordingOpener(no_redirect_handler)

    monkeypatch.setattr(urllib_request, "build_opener", _build_opener)

    result = session.request(
        method="POST",
        url=source_url,
        headers=SYNTHETIC_HEADERS,
        body=b"{}",
        timeout_seconds=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
    )

    assert result.status_code == 302
    assert result.body == b"redirect body"
    assert result.headers.get("location") == alternate_url
    assert attempted_urls == [source_url]
    assert len(attempted_urls) - 1 == 0
    assert alternate_url not in attempted_urls


def test_client_usable_by_bounded_transport() -> None:
    session = ScriptedSession(
        [
            LiveNoteHttpResult(
                201,
                b'{"note":{"id":"synthetic-note-001","body":"created","contactId":"c1"}}',
            )
        ]
    )
    http_client = ConcreteLiveNoteHttpClient(session=session)
    transport = BoundedLiveNoteTransport(
        bound_contact_id="c1",
        credential=InjectedLiveNoteCredential(SYNTHETIC_TOKEN),
        http_client=http_client,
    )
    response = transport.dispatch("POST", "/contacts/c1/notes", {"body": "created"})
    assert response.status == "ok"
    assert len(session.calls) == 1
    assert session.calls[0].timeout_seconds == REQUEST_TIMEOUT_SECONDS
    assert session.calls[0].allow_redirects is False


def test_http_client_module_import_policy() -> None:
    forbidden_third_party = {"requests", "httpx", "aiohttp", "urllib3"}
    tree = ast.parse(HTTP_CLIENT_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots = {alias.name.split(".", 1)[0] for alias in node.names}
            assert not roots & forbidden_third_party
        if isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in forbidden_third_party


def test_private_target_boundary_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "_trust_marker" in source
    assert "private_at8_verified_binding_handoff" in source
    assert "at8_shaped_test_capability" in source
    http_source = HTTP_CLIENT_PATH.read_text(encoding="utf-8")
    assert "VerifiedContactBindingCapability" not in http_source
    assert "_trust_marker" not in http_source
    assert "bound_contact_id" not in http_source
    assert ConcreteLiveNoteHttpClient.TARGET_AUTHORITY is False


def test_caller_target_override_forbidden() -> None:
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "bound_contact_id" in transport_source
    assert "POST path is not the bound-contact notes route" in transport_source
    assert "same-run note id" in transport_source or "same_run_note_id" in transport_source
    http_source = HTTP_CLIENT_PATH.read_text(encoding="utf-8")
    assert "location_id" not in http_source
    assert "contact_id" not in http_source
    assert ConcreteLiveNoteHttpClient.ALTERNATE_ROUTE is False
    assert ConcreteLiveNoteHttpClient.GENERIC_REST_FALLBACK is False


def test_at8h_transport_caps_unchanged() -> None:
    assert POST_ATTEMPTS_MAX == 1
    assert READBACK_GET_ATTEMPTS_MAX == 1
    assert TOTAL_NETWORK_CALLS_MAX == 2
    assert TOTAL_MUTATION_CALLS_MAX == 1
    assert AUTOMATIC_RETRY is False
    assert GENERIC_EXECUTE is False
    assert RAW_REST_FALLBACK is False
    assert REQUEST_TIMEOUT_SECONDS == 10.0
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "POST_ATTEMPTS_MAX = 1" in transport_source
    assert "READBACK_GET_ATTEMPTS_MAX = 1" in transport_source
    assert "TOTAL_NETWORK_CALLS_MAX = 2" in transport_source
    assert "TOTAL_MUTATION_CALLS_MAX = 1" in transport_source
    assert "REQUEST_TIMEOUT_SECONDS = 10.0" in transport_source


def test_at8g_reservation_contract_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "NOTE_CREATE_OPERATION_ORDINAL = 1" in source
    assert '_GRANT_RUN_ID_PREFIX = "npgr1:"' in source
    assert "mark_dispatched" in source
    assert 'business_effect_truth="UNKNOWN"' in source


def test_ambiguity_no_retry_unchanged() -> None:
    assert AMBIGUITY_TRUTH == "UNKNOWN"
    assert AUTOMATIC_RETRY is False
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert 'AMBIGUITY_TRUTH = "UNKNOWN"' in transport_source
    assert "AUTOMATIC_RETRY = False" in transport_source
    assert "SECOND_POST = False" in transport_source
