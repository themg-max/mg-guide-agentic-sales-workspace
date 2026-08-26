from __future__ import annotations

import ast
from dataclasses import dataclass
import json
import logging
from pathlib import Path
import socket
from typing import Any, Mapping

import pytest

import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl import At1ExecutionStore
from integrations.ghl.at1_commitment_key_provider import SyntheticCommitmentKeyProvider
from integrations.ghl.highlevel_rest import NotePathAdapter, TransportError
from integrations.ghl.highlevel_rest.live_note_transport import (
    AMBIGUITY_TRUTH,
    AUTOMATIC_RETRY,
    BASE_URL,
    BoundedLiveNoteTransport,
    CONTACT_GET_ATTEMPTS_MAX,
    GENERIC_EXECUTE,
    InjectedLiveNoteCredential,
    LIVE_EXECUTION_AUTHORIZED,
    LIST,
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
    LiveNoteResponse,
    LiveNoteTransportError,
    PAGINATION,
    POST_ATTEMPTS_MAX,
    RAW_REST_FALLBACK,
    READBACK_GET_ATTEMPTS_MAX,
    REQUEST_TIMEOUT_SECONDS,
    SEARCH,
    SECOND_POST,
    TOTAL_MUTATION_CALLS_MAX,
    TOTAL_NETWORK_CALLS_MAX,
    VERSION_HEADER,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"
TRANSPORT_PATH = SOURCE_ROOT / "live_note_transport.py"
NOTE_PATH_PATH = SOURCE_ROOT / "note_path.py"

SYNTHETIC_CONTACT_ID = "synthetic-contact-001"
SYNTHETIC_NOTE_ID = "synthetic-note-001"
SYNTHETIC_TOKEN = "synthetic-placeholder-token-at8h"
DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY = (
    "NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001"
)
POST_PATH = f"/contacts/{SYNTHETIC_CONTACT_ID}/notes"
CONTACT_GET_PATH = f"/contacts/{SYNTHETIC_CONTACT_ID}"
GET_PATH = f"/contacts/{SYNTHETIC_CONTACT_ID}/notes/{SYNTHETIC_NOTE_ID}"
POST_URL = f"{BASE_URL}{POST_PATH}"
CONTACT_GET_URL = f"{BASE_URL}{CONTACT_GET_PATH}"
GET_URL = f"{BASE_URL}{GET_PATH}"


@pytest.fixture(autouse=True)
def _reset_shared_ledger() -> None:
    note_path_module._reset_shared_test_ledger()


@dataclass
class RecordedHttpCall:
    method: str
    url: str
    headers: dict[str, str]
    body: bytes | None
    timeout_seconds: float
    allow_redirects: bool


class ScriptedHttpClient:
    def __init__(self, outcomes: list[LiveNoteHttpResult | BaseException]) -> None:
        self._outcomes = list(outcomes)
        self.calls: list[RecordedHttpCall] = []

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
            RecordedHttpCall(
                method=method,
                url=url,
                headers=dict(headers),
                body=body,
                timeout_seconds=timeout_seconds,
                allow_redirects=allow_redirects,
            )
        )
        if not self._outcomes:
            raise AssertionError("scripted HTTP client has no remaining outcomes")
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class EchoNoteHttpClient:
    def __init__(self, note_id: str = SYNTHETIC_NOTE_ID) -> None:
        self.note_id = note_id
        self.calls: list[RecordedHttpCall] = []

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
            RecordedHttpCall(
                method=method,
                url=url,
                headers=dict(headers),
                body=body,
                timeout_seconds=timeout_seconds,
                allow_redirects=allow_redirects,
            )
        )
        if url == CONTACT_GET_URL:
            return _contact_ok()
        if method == "POST":
            sent = json.loads((body or b"{}").decode("utf-8"))
            return _http_ok(
                note_id=self.note_id,
                body=sent["body"],
                extra={"dateAdded": "not-published", "locationId": "hidden"},
            )
        post_call = next(
            call for call in reversed(self.calls[:-1]) if call.method == "POST"
        )
        sent_body = json.loads((post_call.body or b"{}").decode("utf-8"))["body"]
        return _http_ok(note_id=self.note_id, body=sent_body)


def _http_ok(
    *,
    note_id: str = SYNTHETIC_NOTE_ID,
    body: str = "created",
    contact_id: str = SYNTHETIC_CONTACT_ID,
    extra: Mapping[str, Any] | None = None,
    status_code: int = 201,
) -> LiveNoteHttpResult:
    note = {"id": note_id, "body": body, "contactId": contact_id}
    if extra:
        note.update(dict(extra))
    return LiveNoteHttpResult(
        status_code, json.dumps({"note": note}).encode("utf-8")
    )


def _contact_ok(
    *,
    contact_id: str = SYNTHETIC_CONTACT_ID,
    location_id: str = "synthetic-location-001",
    extra: Mapping[str, Any] | None = None,
    status_code: int = 200,
) -> LiveNoteHttpResult:
    contact = {"id": contact_id, "locationId": location_id}
    if extra:
        contact.update(dict(extra))
    return LiveNoteHttpResult(
        status_code, json.dumps({"contact": contact}).encode("utf-8")
    )


def _credential() -> InjectedLiveNoteCredential:
    return InjectedLiveNoteCredential(SYNTHETIC_TOKEN)


def _transport(
    client: ScriptedHttpClient | EchoNoteHttpClient,
    *,
    bound_contact_id: str = SYNTHETIC_CONTACT_ID,
    optional_author_user_id: str | None = None,
    optional_title: str | None = None,
) -> BoundedLiveNoteTransport:
    return BoundedLiveNoteTransport(
        bound_contact_id=bound_contact_id,
        credential=_credential(),
        http_client=client,
        optional_author_user_id=optional_author_user_id,
        optional_title=optional_title,
    )


def _post(
    transport: BoundedLiveNoteTransport, body: str = "created"
) -> LiveNoteResponse:
    return transport.dispatch("POST", POST_PATH, {"body": body})


def _note() -> dict[str, object]:
    return {
        "SYNTHETIC_MARKER": "implementation_reviewed_synthetic_marker",
        "meeting_id": "synthetic-meeting-001",
        "meeting_summary": "Synthetic discovery meeting.",
        "needs": ["Automated reminders"],
        "objections": [],
        "commitments": [{"owner": "Avery", "action": "Share proposal"}],
        "next_step": {"owner": "Avery", "action": "Review proposal"},
        "opportunity_signal": None,
        "workflow_id": "meeting_follow_up_v1",
        "transcript_hash": "a" * 64,
    }


def test_exact_post_route() -> None:
    client = ScriptedHttpClient([_http_ok()])
    transport = _transport(client)

    response = _post(transport)

    assert response.status == "ok"
    assert client.calls[0].method == "POST"
    assert client.calls[0].url == POST_URL
    assert client.calls[0].allow_redirects is False
    assert client.calls[0].timeout_seconds == REQUEST_TIMEOUT_SECONDS
    assert json.loads(client.calls[0].body or b"") == {"body": "created"}


def test_exact_get_route() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200)])
    transport = _transport(client)
    _post(transport)

    response = transport.dispatch("GET", GET_PATH)

    assert response.status == "ok"
    assert client.calls[1].method == "GET"
    assert client.calls[1].url == GET_URL
    assert client.calls[1].body is None
    assert client.calls[1].allow_redirects is False


def test_exact_bound_contact_get_route() -> None:
    client = ScriptedHttpClient([_contact_ok()])
    transport = _transport(client)

    response = transport.dispatch("GET", CONTACT_GET_PATH)

    assert response.status == "ok"
    assert response.payload == {
        "contact": {
            "id": SYNTHETIC_CONTACT_ID,
            "locationId": "synthetic-location-001",
        }
    }
    assert client.calls[0].method == "GET"
    assert client.calls[0].url == CONTACT_GET_URL
    assert client.calls[0].body is None
    assert client.calls[0].allow_redirects is False
    assert transport.contact_get_attempts == 1
    assert transport.total_network_calls == 0
    assert transport.total_mutation_calls == 0


def test_bound_contact_get_minimizes_provider_response() -> None:
    client = ScriptedHttpClient(
        [
            _contact_ok(
                extra={
                    "email": "not-published@example.test",
                    "phone": "not-published",
                    "customFields": [{"id": "not-published"}],
                }
            )
        ]
    )

    response = _transport(client).dispatch("GET", CONTACT_GET_PATH)

    assert response.status == "ok"
    assert response.payload == {
        "contact": {
            "id": SYNTHETIC_CONTACT_ID,
            "locationId": "synthetic-location-001",
        }
    }
    assert "email" not in response.payload["contact"]
    assert "phone" not in response.payload["contact"]
    assert "customFields" not in response.payload["contact"]


def test_bound_contact_get_rejects_body_alternate_query_and_fragment() -> None:
    client = ScriptedHttpClient([])
    transport = _transport(client)

    with pytest.raises(LiveNoteTransportError, match="does not accept a body"):
        transport.dispatch("GET", CONTACT_GET_PATH, {"body": "forbidden"})
    for path in (
        "/contacts/synthetic-contact-other",
        f"{CONTACT_GET_PATH}?limit=1",
        f"{CONTACT_GET_PATH}#fragment",
    ):
        with pytest.raises(LiveNoteTransportError):
            transport.dispatch("GET", path)

    assert client.calls == []
    assert transport.contact_get_attempts == 0
    assert transport.total_mutation_calls == 0


def test_bound_contact_get_max_one_and_second_attempt_is_rejected() -> None:
    client = ScriptedHttpClient([_contact_ok(), _contact_ok()])
    transport = _transport(client)
    transport.dispatch("GET", CONTACT_GET_PATH)

    with pytest.raises(
        LiveNoteTransportError, match="bound-contact GET attempts max is 1"
    ):
        transport.dispatch("GET", CONTACT_GET_PATH)

    assert transport.contact_get_attempts == CONTACT_GET_ATTEMPTS_MAX
    assert len(client.calls) == 1
    assert transport.total_mutation_calls == 0


@pytest.mark.parametrize(
    "result",
    [
        LiveNoteHttpResult(503, b"unavailable"),
        LiveNoteHttpResult(200, b"not-json"),
        LiveNoteHttpResult(200, b'{"contact":{"id":"synthetic-contact-001"}}'),
        LiveNoteHttpResult(200, b'{"contact":{"locationId":"synthetic-location-001"}}'),
    ],
)
def test_bound_contact_get_malformed_or_unsuccessful_response_fails_closed(
    result: LiveNoteHttpResult,
) -> None:
    response = _transport(ScriptedHttpClient([result])).dispatch(
        "GET", CONTACT_GET_PATH
    )

    assert response.status == "error"
    assert response.payload == {}


def test_bound_contact_get_network_uncertainty_fails_closed() -> None:
    transport = _transport(
        ScriptedHttpClient([LiveNoteHttpUncertainty("synthetic timeout")])
    )

    response = transport.dispatch("GET", CONTACT_GET_PATH)

    assert response.status == "error"
    assert response.payload == {}
    assert transport.contact_get_attempts == 1
    assert transport.total_network_calls == 0
    assert transport.total_mutation_calls == 0


def test_contact_preflight_preserves_frozen_note_route_budget() -> None:
    client = EchoNoteHttpClient()
    transport = _transport(client)

    transport.dispatch("GET", CONTACT_GET_PATH)
    _post(transport)
    response = transport.dispatch("GET", GET_PATH)

    assert response.status == "ok"
    assert transport.contact_get_attempts == CONTACT_GET_ATTEMPTS_MAX
    assert transport.total_network_calls == TOTAL_NETWORK_CALLS_MAX
    assert transport.total_mutation_calls == TOTAL_MUTATION_CALLS_MAX
    assert [call.url for call in client.calls] == [CONTACT_GET_URL, POST_URL, GET_URL]


def test_bound_contact_only() -> None:
    client = ScriptedHttpClient([_http_ok()])
    transport = _transport(client)

    with pytest.raises(LiveNoteTransportError, match="bound-contact"):
        transport.dispatch(
            "POST", "/contacts/synthetic-contact-other/notes", {"body": "created"}
        )
    assert client.calls == []
    assert transport.post_attempts == 0


def test_same_run_note_id_only() -> None:
    client = ScriptedHttpClient([_http_ok()])
    transport = _transport(client)
    _post(transport)

    with pytest.raises(LiveNoteTransportError, match="same-run"):
        transport.dispatch(
            "GET", f"/contacts/{SYNTHETIC_CONTACT_ID}/notes/synthetic-note-other"
        )
    assert len(client.calls) == 1
    assert transport.get_attempts == 0


def test_get_before_post_is_rejected() -> None:
    client = ScriptedHttpClient([])
    transport = _transport(client)

    with pytest.raises(LiveNoteTransportError, match="same-run"):
        transport.dispatch("GET", GET_PATH)
    assert client.calls == []


def test_post_max_one() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok()])
    transport = _transport(client)
    _post(transport)

    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)
    assert transport.post_attempts == POST_ATTEMPTS_MAX
    assert len(client.calls) == 1


def test_get_max_one() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200), _http_ok()])
    transport = _transport(client)
    _post(transport)
    transport.dispatch("GET", GET_PATH)

    with pytest.raises(LiveNoteTransportError, match="GET attempts max is 1"):
        transport.dispatch("GET", GET_PATH)
    assert transport.get_attempts == READBACK_GET_ATTEMPTS_MAX
    assert len(client.calls) == 2


def test_total_calls_max_two() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200)])
    transport = _transport(client)
    _post(transport)
    transport.dispatch("GET", GET_PATH)

    assert transport.total_network_calls == TOTAL_NETWORK_CALLS_MAX
    assert transport.total_mutation_calls == TOTAL_MUTATION_CALLS_MAX
    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)


def test_no_retry() -> None:
    assert AUTOMATIC_RETRY is False
    assert SECOND_POST is False
    client = ScriptedHttpClient([LiveNoteHttpUncertainty("timeout")])
    transport = _transport(client)
    response = _post(transport)

    assert response.status == "ambiguous"
    assert transport.post_attempts == 1
    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)
    assert len(client.calls) == 1


def test_no_search_list_pagination() -> None:
    assert SEARCH is False
    assert LIST is False
    assert PAGINATION is False
    client = ScriptedHttpClient([])
    transport = _transport(client)
    forbidden = [
        f"/contacts/{SYNTHETIC_CONTACT_ID}/notes?limit=10",
        f"/contacts/{SYNTHETIC_CONTACT_ID}/notes/",
        "/contacts/search",
        f"/contacts/{SYNTHETIC_CONTACT_ID}/notes?page=2",
    ]
    for path in forbidden:
        with pytest.raises(LiveNoteTransportError):
            transport.dispatch("GET", path)
        with pytest.raises(LiveNoteTransportError):
            transport.dispatch("POST", path, {"body": "created"})
    assert client.calls == []


def test_no_alternate_target() -> None:
    client = ScriptedHttpClient([_http_ok()])
    transport = _transport(client)
    _post(transport)

    with pytest.raises(LiveNoteTransportError, match="bound-contact|same-run"):
        transport.dispatch(
            "GET", f"/contacts/synthetic-contact-other/notes/{SYNTHETIC_NOTE_ID}"
        )
    with pytest.raises(LiveNoteTransportError, match="bound-contact"):
        transport.dispatch(
            "POST",
            "/contacts/synthetic-contact-other/notes",
            {"body": "created"},
        )
    assert len(client.calls) == 1


def test_no_generic_execute() -> None:
    assert GENERIC_EXECUTE is False
    assert RAW_REST_FALLBACK is False
    public = {
        name for name in vars(BoundedLiveNoteTransport) if not name.startswith("_")
    }
    assert "dispatch" in public
    assert not public & {
        "search",
        "list",
        "paginate",
        "execute",
        "request",
        "delete",
        "update",
        "put",
        "patch",
    }
    source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "GENERIC_EXECUTE = False" in source
    assert "RAW_REST_FALLBACK = False" in source


def test_auth_header_not_logged(caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]) -> None:
    caplog.set_level(logging.DEBUG)
    client = ScriptedHttpClient([_http_ok()])
    transport = _transport(client)
    response = _post(transport)

    captured = capsys.readouterr()
    haystacks = [
        repr(transport),
        str(transport),
        repr(response),
        str(response),
        repr(_credential()),
        captured.out,
        captured.err,
        caplog.text,
    ]
    for haystack in haystacks:
        assert "Authorization" not in haystack
        assert SYNTHETIC_TOKEN not in haystack
        assert "Bearer " not in haystack
    assert "Authorization" in client.calls[0].headers
    assert client.calls[0].headers["Authorization"] == f"Bearer {SYNTHETIC_TOKEN}"
    assert client.calls[0].headers["Version"] == VERSION_HEADER


def test_token_not_logged() -> None:
    credential = _credential()
    transport = _transport(ScriptedHttpClient([_http_ok()]))
    _post(transport)
    assert SYNTHETIC_TOKEN not in repr(credential)
    assert SYNTHETIC_TOKEN not in str(credential)
    assert SYNTHETIC_TOKEN not in repr(transport)
    assert "bearer_token" not in repr(transport)


def test_raw_provider_response_not_published() -> None:
    client = ScriptedHttpClient(
        [
            _http_ok(
                extra={
                    "dateAdded": "2026-01-01T00:00:00.000Z",
                    "userId": "hidden-user",
                    "locationId": "hidden-location",
                }
            )
        ]
    )
    response = _post(_transport(client))
    assert set(response.payload) == {"note"}
    assert set(response.payload["note"]) == {"id", "body", "contactId"}
    assert "dateAdded" not in response.payload["note"]
    assert "userId" not in response.payload["note"]
    assert "locationId" not in response.payload["note"]


def test_post_timeout_classified_ambiguous() -> None:
    client = ScriptedHttpClient([LiveNoteHttpUncertainty("deadline exceeded")])
    response = _post(_transport(client))
    assert response.status == "ambiguous"
    assert response.payload == {}
    assert AMBIGUITY_TRUTH == "UNKNOWN"


def test_post_5xx_classified_ambiguous() -> None:
    client = ScriptedHttpClient([LiveNoteHttpResult(503, b"unavailable")])
    response = _post(_transport(client))
    assert response.status == "ambiguous"


def test_post_unparseable_success_classified_ambiguous() -> None:
    client = ScriptedHttpClient([LiveNoteHttpResult(201, b"not-json")])
    response = _post(_transport(client))
    assert response.status == "ambiguous"
    assert response.payload == {}


def test_post_success_without_note_id_classified_ambiguous() -> None:
    result = LiveNoteHttpResult(
        201,
        json.dumps(
            {"note": {"body": "created", "contactId": SYNTHETIC_CONTACT_ID}}
        ).encode("utf-8"),
    )
    client = ScriptedHttpClient([result, _http_ok()])
    transport = _transport(client)

    response = _post(transport)

    assert response.status == "ambiguous"
    assert response.payload == {}
    assert transport.post_attempts == 1
    assert transport.post_successes == 0
    assert AMBIGUITY_TRUTH == "UNKNOWN"
    with pytest.raises(LiveNoteTransportError, match="same-run"):
        transport.dispatch("GET", GET_PATH)
    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)
    assert SECOND_POST is False
    assert len(client.calls) == 1


def test_no_second_post_after_ambiguity() -> None:
    client = ScriptedHttpClient(
        [LiveNoteHttpUncertainty("timeout"), _http_ok()]
    )
    transport = _transport(client)
    first = _post(transport)
    assert first.status == "ambiguous"
    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)
    assert len(client.calls) == 1
    assert transport.total_mutation_calls == 1


def test_ambiguous_post_does_not_unlock_get() -> None:
    client = ScriptedHttpClient([LiveNoteHttpUncertainty("timeout")])
    transport = _transport(client)
    _post(transport)
    with pytest.raises(LiveNoteTransportError, match="same-run"):
        transport.dispatch("GET", GET_PATH)
    assert len(client.calls) == 1


def test_provider_response_normalization() -> None:
    client = ScriptedHttpClient(
        [_http_ok(body="created", extra={"dateAdded": "hidden"})]
    )
    response = _post(_transport(client))
    assert isinstance(response, LiveNoteResponse)
    assert response.status == "ok"
    assert response.payload == {
        "note": {
            "id": SYNTHETIC_NOTE_ID,
            "body": "created",
            "contactId": SYNTHETIC_CONTACT_ID,
        }
    }


def test_provider_note_id_only_in_memory_for_same_run_readback() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200)])
    transport = _transport(client)
    _post(transport)
    assert "synthetic-note-001" not in repr(transport)
    transport.dispatch("GET", GET_PATH)
    assert client.calls[1].url.endswith(f"/notes/{SYNTHETIC_NOTE_ID}")
    public = {
        name for name in vars(BoundedLiveNoteTransport) if not name.startswith("_")
    }
    assert "same_run_note_id" not in public


def test_diagnostic_call_history_is_private_and_redacted() -> None:
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200)])
    transport = _transport(client)
    _post(transport)
    transport.dispatch("GET", GET_PATH)

    public = {
        name for name in vars(BoundedLiveNoteTransport) if not name.startswith("_")
    }
    history = json.dumps(transport._call_history)
    assert "calls" not in public
    assert not hasattr(transport, "calls")
    assert SYNTHETIC_CONTACT_ID not in history
    assert SYNTHETIC_NOTE_ID not in history
    assert history == json.dumps(
        [
            ["POST", "/contacts/<redacted>/notes"],
            ["GET", "/contacts/<redacted>/notes/<redacted>"],
        ]
    )


def test_post_4xx_is_definite_error_and_consumes_budget() -> None:
    client = ScriptedHttpClient([LiveNoteHttpResult(400, b'{"error":"rejected"}')])
    transport = _transport(client)
    response = _post(transport)
    assert response.status == "error"
    with pytest.raises(LiveNoteTransportError, match="POST attempts max is 1"):
        _post(transport)
    assert len(client.calls) == 1


def test_optional_injected_author_metadata_only_when_supplied() -> None:
    default_client = ScriptedHttpClient([_http_ok()])
    _post(_transport(default_client))
    assert json.loads(default_client.calls[0].body or b"") == {"body": "created"}

    authored_client = ScriptedHttpClient([_http_ok()])
    authored = _transport(
        authored_client, optional_author_user_id="synthetic-user-001"
    )
    _post(authored)
    assert json.loads(authored_client.calls[0].body or b"") == {
        "body": "created",
        "userId": "synthetic-user-001",
    }


def test_live_execution_remains_unauthorized() -> None:
    assert LIVE_EXECUTION_AUTHORIZED is False


def test_zero_real_network_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("real network is forbidden during AT8H tests")

    monkeypatch.setattr(socket, "socket", _forbid)
    monkeypatch.setattr(socket, "create_connection", _forbid)
    client = ScriptedHttpClient([_http_ok(), _http_ok(status_code=200)])
    transport = _transport(client)
    _post(transport)
    transport.dispatch("GET", GET_PATH)
    assert len(client.calls) == 2


def test_transport_module_has_no_live_imports() -> None:
    forbidden_import_roots = {
        "requests",
        "httpx",
        "urllib",
        "socket",
        "os",
        "asyncio",
        "http",
        "ssl",
    }
    tree = ast.parse(TRANSPORT_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {name.name.split(".", 1)[0] for name in node.names}
            assert not imported & forbidden_import_roots
        if isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots


def test_at8g_durable_reservation_contract_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "NOTE_CREATE_OPERATION_ORDINAL = 1" in source
    assert "_GRANT_RUN_ID_PREFIX = \"npgr1:\"" in source
    assert "mark_dispatched" in source
    assert "business_effect_truth=\"UNKNOWN\"" in source


def test_pr107_trust_boundary_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "_trust_marker" in source
    assert "private_at8_verified_binding_handoff" in source
    assert "at8_shaped_test_capability" in source
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "_trust_marker" not in transport_source
    assert "VerifiedContactBindingCapability" not in transport_source
    assert "_issue_capability" not in transport_source


def test_injectable_bound_contact_preflight_uses_minimized_contact_response() -> None:
    client = EchoNoteHttpClient()
    transport = _transport(client)
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id=SYNTHETIC_CONTACT_ID,
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-at8w30-contact-001",
    )

    contact = adapter.get_bound_contact()

    assert contact == {
        "id": SYNTHETIC_CONTACT_ID,
        "locationId": "synthetic-location-001",
    }
    assert adapter.CONTACT_PREFLIGHT_VERIFIED == "YES"
    assert transport.contact_get_attempts == CONTACT_GET_ATTEMPTS_MAX
    assert transport.total_network_calls == 0
    assert transport.total_mutation_calls == 0
    assert [call.url for call in client.calls] == [CONTACT_GET_URL]


def test_bound_contact_preflight_rejects_identifier_mismatch() -> None:
    client = ScriptedHttpClient([_contact_ok(contact_id="synthetic-contact-other")])
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id=SYNTHETIC_CONTACT_ID,
        transport=_transport(client),
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-at8w30-contact-mismatch-001",
    )

    with pytest.raises(note_path_module.BindingError, match="does not match"):
        adapter.get_bound_contact()

    assert len(client.calls) == 1


def test_injectable_into_note_path_adapter() -> None:
    client = EchoNoteHttpClient()
    transport = _transport(client)
    workflow_run_id = "synthetic-workflow-run-at8h-001"
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id=SYNTHETIC_CONTACT_ID,
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = (
        NotePathAdapter._build_at8_shaped_test_capability(
            location_id="synthetic-location-001",
            contact_id=SYNTHETIC_CONTACT_ID,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )
    )

    created = adapter.create_meeting_note(_note())
    verified = adapter.verify_meeting_note()

    assert created.note_id == SYNTHETIC_NOTE_ID
    assert verified.note_id == SYNTHETIC_NOTE_ID
    assert [call.method for call in client.calls] == ["POST", "GET"]
    assert [call.url for call in client.calls] == [POST_URL, GET_URL]


def test_injectable_transport_preserves_at8g_store_ordinal(tmp_path: Path) -> None:
    store = At1ExecutionStore(
        db_path=tmp_path / "at8h-note-path.sqlite3",
        commitment_material=SyntheticCommitmentKeyProvider(
            payload="synthetic-commitment-key",
            version_resource="projects/synthetic-project/secrets/at1-commitment-key/versions/1",
        ).resolve(),
    )
    client = EchoNoteHttpClient()
    transport = _transport(client)
    workflow_run_id = "synthetic-workflow-run-at8h-store-001"
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id=SYNTHETIC_CONTACT_ID,
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
        execution_store=store,
    )
    adapter._verified_contact_binding_capability = (
        NotePathAdapter._build_at8_shaped_test_capability(
            location_id="synthetic-location-001",
            contact_id=SYNTHETIC_CONTACT_ID,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )
    )

    adapter.create_meeting_note(_note())
    grant_run_id = adapter._deterministic_grant_run_id()
    attempts = store.list_private_attempts(grant_run_id)
    assert len(attempts) == 1
    assert attempts[0]["operation_ordinal"] == 1
    assert attempts[0]["operation_id"] == "NOTE_CREATE"


def test_adapter_ambiguous_post_is_terminal_unknown(tmp_path: Path) -> None:
    store = At1ExecutionStore(
        db_path=tmp_path / "at8h-ambiguous.sqlite3",
        commitment_material=SyntheticCommitmentKeyProvider(
            payload="synthetic-commitment-key",
            version_resource="projects/synthetic-project/secrets/at1-commitment-key/versions/1",
        ).resolve(),
    )
    client = ScriptedHttpClient([LiveNoteHttpUncertainty("timeout")])
    transport = _transport(client)
    workflow_run_id = "synthetic-workflow-run-at8h-ambiguous-001"
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id=SYNTHETIC_CONTACT_ID,
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
        execution_store=store,
    )
    adapter._verified_contact_binding_capability = (
        NotePathAdapter._build_at8_shaped_test_capability(
            location_id="synthetic-location-001",
            contact_id=SYNTHETIC_CONTACT_ID,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )
    )

    with pytest.raises(TransportError, match="not retried"):
        adapter.create_meeting_note(_note())
    grant_run_id = adapter._deterministic_grant_run_id()
    attempts = store.list_private_attempts(grant_run_id)
    assert attempts[0]["business_effect_truth"] == "UNKNOWN"
    assert len(client.calls) == 1


def test_dispatch_rejects_put_delete_and_patch() -> None:
    client = ScriptedHttpClient([])
    transport = _transport(client)
    for method in ("PUT", "PATCH", "DELETE", "HEAD"):
        with pytest.raises(LiveNoteTransportError, match="only POST and GET"):
            transport.dispatch(method, POST_PATH, {"body": "created"})
    assert client.calls == []
