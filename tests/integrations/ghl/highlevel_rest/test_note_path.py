from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import ast
from hashlib import sha256
from itertools import count
import json
from pathlib import Path
import threading

import pytest

import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest import (
    BindingError,
    DeterministicFakeTransport,
    NoteContractError,
    NotePathAdapter,
    TransportError,
)


DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY = (
    "NW008_AT8B_GHL_REST_NOTE_PATH_MUTATION_GUARD_HARDENING_IMPLEMENTATION_001"
)
_RUN_COUNTER = count(1)

REPO_ROOT = Path(__file__).resolve().parents[4]
FIXTURE_PATH = REPO_ROOT / "fixtures" / "ghl" / "highlevel_rest" / "note-path-fixtures.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"


@pytest.fixture(autouse=True)
def _reset_shared_ledger() -> None:
    note_path_module._reset_shared_test_ledger()


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


def _next_workflow_run_id() -> str:
    return f"synthetic-workflow-run-{next(_RUN_COUNTER):04d}"


def _adapter(
    case_id: str,
    *,
    consumer_workflow_run_id: str | None = None,
    consumer_authorization_identity: str = DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
) -> tuple[NotePathAdapter, DeterministicFakeTransport]:
    transport = DeterministicFakeTransport(deepcopy(FIXTURE), case_id)
    return (
        NotePathAdapter(
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            transport=transport,
            consumer_authorization_identity=consumer_authorization_identity,
            consumer_workflow_run_id=consumer_workflow_run_id or _next_workflow_run_id(),
        ),
        transport,
    )


def _create(adapter: NotePathAdapter) -> None:
    if adapter.CONTACT_PREFLIGHT_VERIFIED == "NO":
        adapter.get_bound_contact()
    adapter.create_meeting_note(_note())


def _post_body(transport: DeterministicFakeTransport) -> str:
    return next(body["body"] for method, _, body in transport.calls if method == "POST")


def _replace_readback_body(
    transport: DeterministicFakeTransport, body: str
) -> DeterministicFakeTransport:
    transport._calls[-1]["response"]["payload"]["note"]["body"] = body
    return transport


def _trusted_test_capability(
    *,
    workflow_id: str = "meeting_follow_up_v1",
    source_execution_unit: str = (
        "NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002"
    ),
    source_proof_merge_sha: str = "6256f287bbd88effc2ef1cd13a801faec79a0af2",
    location_id: str = "synthetic-location-001",
    contact_id: str = "synthetic-contact-001",
    consumer_authorization_identity: str = DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
    consumer_workflow_run_id: str = "synthetic-workflow-run-override",
):
    capability = NotePathAdapter._build_at8_shaped_test_capability(
        location_id=location_id,
        contact_id=contact_id,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )
    if capability.workflow_id != workflow_id:
        object.__setattr__(capability, "workflow_id", workflow_id)
    if capability.source_execution_unit != source_execution_unit:
        object.__setattr__(capability, "source_execution_unit", source_execution_unit)
    if capability.source_proof_merge_sha != source_proof_merge_sha:
        object.__setattr__(capability, "source_proof_merge_sha", source_proof_merge_sha)
    return capability


def test_exact_contact_binding_pass() -> None:
    adapter, transport = _adapter("contact_success")

    assert adapter.get_bound_contact() == {
        "id": "synthetic-contact-001",
        "locationId": "synthetic-location-001",
    }
    assert adapter.CONTACT_PREFLIGHT_VERIFIED == "YES"
    transport.assert_exhausted()


@pytest.mark.parametrize(
    ("case_id", "message"),
    [
        ("contact_id_mismatch", "contact id"),
        ("location_id_mismatch", "location id"),
        ("contact_missing", "not successful"),
    ],
)
def test_contact_binding_mismatch_block(case_id: str, message: str) -> None:
    adapter, _ = _adapter(case_id)

    with pytest.raises((BindingError, TransportError), match=message):
        adapter.get_bound_contact()


def _adapter_with_missing_binding(field_name: str) -> None:
    kwargs = {
        "location_id": "synthetic-location-001",
        "contact_id": "synthetic-contact-001",
        "transport": DeterministicFakeTransport(deepcopy(FIXTURE), "contact_success"),
        "consumer_authorization_identity": DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "consumer_workflow_run_id": _next_workflow_run_id(),
    }
    kwargs[field_name] = ""
    NotePathAdapter(**kwargs)


def test_missing_contact_binding_block() -> None:
    with pytest.raises(BindingError, match="private binding"):
        _adapter_with_missing_binding("contact_id")


def test_missing_location_binding_block() -> None:
    with pytest.raises(BindingError, match="private binding"):
        _adapter_with_missing_binding("location_id")


@pytest.mark.parametrize("field_name", ["contact_id", "location_id"])
def test_caller_supplied_provider_id_block(field_name: str) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    note[field_name] = "caller-override"
    adapter.get_bound_contact()

    with pytest.raises(NoteContractError, match="extra"):
        adapter.create_meeting_note(note)
    assert [method for method, _, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda note: note.__setitem__("raw_transcript", "unbounded source"),
        lambda note: note.__setitem__("SYNTHETIC_MARKER", "live_source"),
    ],
)
def test_raw_transcript_and_non_synthetic_source_rejected(mutation) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    mutation(note)
    adapter.get_bound_contact()

    with pytest.raises(NoteContractError):
        adapter.create_meeting_note(note)
    assert [method for method, _, _ in transport.calls] == ["GET"]


def test_note_body_only_payload() -> None:
    adapter, transport = _adapter("note_create_success")

    _create(adapter)

    method, path, body = transport.calls[1]
    assert (method, path) == ("POST", "/contacts/synthetic-contact-001/notes")
    assert set(body or {}) == {"body"}
    assert "userId" not in (body or {})
    assert "title" not in (body or {})
    assert "color" not in (body or {})
    assert "pinned" not in (body or {})


def test_create_without_contact_preflight_block() -> None:
    adapter, transport = _adapter("note_create_success")

    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert adapter.CONTACT_PREFLIGHT_VERIFIED == "NO"
    assert adapter.POST_ATTEMPTS == 0
    assert transport.calls == []


@pytest.mark.parametrize(
    "case_id",
    ["contact_missing", "contact_id_mismatch", "location_id_mismatch"],
)
def test_failed_contact_preflight_blocks_post(case_id: str) -> None:
    adapter, transport = _adapter(case_id)

    with pytest.raises((BindingError, TransportError)):
        adapter.get_bound_contact()
    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert adapter.CONTACT_PREFLIGHT_VERIFIED == "NO"
    assert adapter.POST_ATTEMPTS == 0
    assert [method for method, _, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize("field_name", ["userId", "title", "color", "pinned"])
def test_denied_provider_fields_rejected(field_name: str) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    note[field_name] = "denied"
    adapter.get_bound_contact()

    with pytest.raises(NoteContractError, match="extra"):
        adapter.create_meeting_note(note)
    assert [method for method, _, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize(
    "case_id",
    [
        "note_create_definite_failure",
        "note_response_malformed",
        "note_response_contact_mismatch",
    ],
)
def test_same_run_note_id_and_contact_binding_required(case_id: str) -> None:
    adapter, _ = _adapter(case_id)

    with pytest.raises(TransportError):
        _create(adapter)


def test_same_run_note_id_required() -> None:
    adapter, transport = _adapter("note_create_success")
    transport._calls[1]["response"]["payload"]["note"].pop("id")

    with pytest.raises(TransportError, match="id is required"):
        _create(adapter)


def test_public_preflight_flag_cannot_bypass() -> None:
    adapter, transport = _adapter("note_create_success")
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"

    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_public_post_counter_cannot_reset_budget() -> None:
    adapter, transport = _adapter("note_create_success")
    _create(adapter)
    adapter.POST_ATTEMPTS = 0

    with pytest.raises(TransportError, match="exactly one"):
        _create(adapter)
    assert [method for method, _, _ in transport.calls] == ["GET", "POST"]


def test_one_note_write_budget() -> None:
    adapter, transport = _adapter("note_create_success")
    _create(adapter)

    with pytest.raises(TransportError, match="exactly one"):
        _create(adapter)
    assert [method for method, _, _ in transport.calls] == ["GET", "POST"]


def test_second_adapter_cannot_restore_budget() -> None:
    workflow_run_id = "synthetic-workflow-run-shared-budget-001"
    first_adapter, first_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    second_adapter, second_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    first_adapter.get_bound_contact()
    second_adapter.get_bound_contact()

    first_adapter.create_meeting_note(_note())
    with pytest.raises(TransportError, match="exactly one"):
        second_adapter.create_meeting_note(_note())
    assert [method for method, _, _ in first_transport.calls] == ["GET", "POST"]
    assert [method for method, _, _ in second_transport.calls] == ["GET"]


def test_ambiguous_post_no_retry() -> None:
    adapter, transport = _adapter("note_create_ambiguous_result")

    with pytest.raises(TransportError, match="not retried"):
        _create(adapter)
    with pytest.raises(TransportError, match="exactly one"):
        _create(adapter)
    assert [method for method, _, _ in transport.calls] == ["GET", "POST"]


def test_ambiguous_post_budget_remains_consumed() -> None:
    workflow_run_id = "synthetic-workflow-run-ambiguous-terminal-001"
    first_adapter, first_transport = _adapter(
        "note_create_ambiguous_result", consumer_workflow_run_id=workflow_run_id
    )
    second_adapter, second_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )

    with pytest.raises(TransportError, match="not retried"):
        _create(first_adapter)
    second_adapter.get_bound_contact()
    with pytest.raises(TransportError, match="exactly one"):
        second_adapter.create_meeting_note(_note())

    assert [method for method, _, _ in first_transport.calls] == ["GET", "POST"]
    assert [method for method, _, _ in second_transport.calls] == ["GET"]


def test_invalid_verified_binding_capability_blocks() -> None:
    adapter, transport = _adapter("note_create_success")
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"
    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []

    trusted_binding_source = note_path_module._TrustedPrivateBindingSource(
        workflow_id="meeting_follow_up_v1",
        source_execution_unit="NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002",
        source_proof_merge_sha="6256f287bbd88effc2ef1cd13a801faec79a0af2",
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        trusted_origin="private_at8_verified_binding_handoff",
        _trust_marker=object(),
    )
    forged = note_path_module._VerifiedContactBindingCapability(
        workflow_id="meeting_follow_up_v1",
        source_execution_unit="NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002",
        source_proof_merge_sha="6256f287bbd88effc2ef1cd13a801faec79a0af2",
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-forged-001",
        trusted_binding_source=trusted_binding_source,
        _trust_marker=object(),
    )
    adapter._verified_contact_binding_capability = forged
    with pytest.raises(BindingError, match="invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


@pytest.mark.parametrize(
    ("capability_kwargs", "message"),
    [
        (
            {"workflow_id": "wrong_workflow_v2"},
            "workflow binding is invalid",
        ),
        (
            {"consumer_workflow_run_id": "synthetic-workflow-run-other-9999"},
            "workflow run binding is invalid",
        ),
        (
            {"consumer_authorization_identity": "WRONG_AUTHZ_IDENTITY"},
            "authorization binding is invalid",
        ),
        (
            {"source_proof_merge_sha": "deadbeef"},
            "source proof is invalid",
        ),
        (
            {"source_execution_unit": "WRONG_EXECUTION_UNIT"},
            "source execution unit is invalid",
        ),
    ],
)
def test_wrong_workflow_or_authorization_binding_blocks(
    capability_kwargs: dict[str, str], message: str
) -> None:
    workflow_run_id = "synthetic-workflow-run-capability-binding-001"
    adapter, transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    capability_defaults = {
        "workflow_id": "meeting_follow_up_v1",
        "source_execution_unit": (
            "NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002"
        ),
        "source_proof_merge_sha": "6256f287bbd88effc2ef1cd13a801faec79a0af2",
        "location_id": "synthetic-location-001",
        "contact_id": "synthetic-contact-001",
        "consumer_authorization_identity": DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "consumer_workflow_run_id": workflow_run_id,
    }
    capability_defaults.update(capability_kwargs)
    adapter._verified_contact_binding_capability = _trusted_test_capability(
        **capability_defaults
    )
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"

    with pytest.raises(BindingError, match=message):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_pre_reservation_validation_failure_does_not_consume_budget() -> None:
    workflow_run_id = "synthetic-workflow-run-pre-validation-001"
    adapter, transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    adapter._verified_contact_binding_capability = _trusted_test_capability(
        consumer_workflow_run_id=workflow_run_id,
        workflow_id="wrong_workflow",
    )
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"

    with pytest.raises(BindingError):
        adapter.create_meeting_note(_note())
    assert transport.calls == []

    adapter.get_bound_contact()
    adapter.create_meeting_note(_note())
    assert [method for method, _, _ in transport.calls] == ["GET", "POST"]


def test_concurrent_reservation_exactly_one_winner() -> None:
    workflow_run_id = "synthetic-workflow-run-concurrent-001"
    first_adapter, first_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    second_adapter, second_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )
    first_adapter.get_bound_contact()
    second_adapter.get_bound_contact()

    barrier = threading.Barrier(3)
    successes: list[str] = []
    errors: list[TransportError] = []

    def _worker(adapter: NotePathAdapter) -> str:
        barrier.wait()
        adapter.create_meeting_note(_note())
        return "ok"

    with ThreadPoolExecutor(max_workers=2) as executor:
        first_future = executor.submit(_worker, first_adapter)
        second_future = executor.submit(_worker, second_adapter)
        barrier.wait()
        for future in (first_future, second_future):
            try:
                successes.append(future.result())
            except TransportError as error:
                errors.append(error)

    assert len(successes) == 1
    assert len(errors) == 1
    assert isinstance(errors[0], TransportError)
    assert "exactly one" in str(errors[0])
    calls = [*first_transport.calls, *second_transport.calls]
    assert sum(1 for method, _, _ in calls if method == "POST") == 1


class _PostReservationFailureTransport(DeterministicFakeTransport):
    def dispatch(
        self, method: str, path: str, body: dict[str, object] | None = None
    ) -> note_path_module.FakeResponse:
        response = super().dispatch(method, path, body)
        if method == "POST":
            raise RuntimeError("forced post-reservation exception")
        return response


def test_post_reservation_exception_remains_consumed() -> None:
    workflow_run_id = "synthetic-workflow-run-post-exception-001"
    exploding_transport = _PostReservationFailureTransport(
        deepcopy(FIXTURE), "note_create_success"
    )
    first_adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        transport=exploding_transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    second_adapter, second_transport = _adapter(
        "note_create_success", consumer_workflow_run_id=workflow_run_id
    )

    first_adapter.get_bound_contact()
    with pytest.raises(RuntimeError, match="post-reservation exception"):
        first_adapter.create_meeting_note(_note())

    second_adapter.get_bound_contact()
    with pytest.raises(TransportError, match="exactly one"):
        second_adapter.create_meeting_note(_note())
    assert [method for method, _, _ in exploding_transport.calls] == ["GET", "POST"]
    assert [method for method, _, _ in second_transport.calls] == ["GET"]


def test_strict_parser_pass_and_note_content_digest_pass() -> None:
    adapter, transport = _adapter("note_readback_success")
    _create(adapter)
    body = _post_body(transport)
    _replace_readback_body(transport, body)

    result = adapter.verify_meeting_note()

    assert result.note_id == "synthetic-note-001"
    assert len(result.note_content_digest) == 64
    assert len(result.provider_body_digest) == 64
    transport.assert_exhausted()


@pytest.mark.parametrize(
    ("case_id", "body"),
    [
        (
            "note_body_parser_failure",
            "MG Guide \u2014 Synthetic Meeting Follow-Up\nunknown: \"value\"\n",
        ),
        (
            "note_body_parser_failure",
            "MG Guide \u2014 Synthetic Meeting Follow-Up\n"
            "SYNTHETIC_MARKER: \"implementation_reviewed_synthetic_marker\"\n"
            "SYNTHETIC_MARKER: \"implementation_reviewed_synthetic_marker\"\n",
        ),
    ],
)
def test_strict_parser_unknown_and_duplicate_label_block(case_id: str, body: str) -> None:
    adapter, transport = _adapter(case_id)
    _create(adapter)
    _replace_readback_body(transport, body)

    with pytest.raises(TransportError):
        adapter.verify_meeting_note()


def test_note_content_digest_mismatch_block() -> None:
    adapter, transport = _adapter("digest_mismatch")
    _create(adapter)
    changed = _note()
    changed["meeting_summary"] = "Different synthetic summary."
    changed_body = adapter._serialize_note(changed)
    _replace_readback_body(transport, changed_body)

    with pytest.raises(TransportError, match="NOTE_CONTENT_DIGEST"):
        adapter.verify_meeting_note()


def test_provider_body_digest_is_stable_and_exact() -> None:
    first_adapter, first_transport = _adapter("note_create_success")
    second_adapter, second_transport = _adapter("note_create_success")
    _create(first_adapter)
    _create(second_adapter)

    first = first_adapter._created_note
    second = second_adapter._created_note
    assert first is not None and second is not None
    assert first.provider_body_digest == second.provider_body_digest
    exact_body = {"body": _post_body(first_transport)}
    expected = sha256(
        json.dumps(
            exact_body,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    assert first.provider_body_digest == expected


def test_changed_provider_body_has_different_digest() -> None:
    first_adapter, _ = _adapter("note_create_success")
    second_adapter, _ = _adapter("note_create_success")
    _create(first_adapter)
    second_adapter.get_bound_contact()
    changed_note = _note()
    changed_note["meeting_summary"] = "Changed synthetic summary."
    second_adapter.create_meeting_note(changed_note)

    assert first_adapter._created_note is not None
    assert second_adapter._created_note is not None
    assert (
        first_adapter._created_note.provider_body_digest
        != second_adapter._created_note.provider_body_digest
    )


def test_synthetic_excerpt_is_unavailable_until_its_limit_is_resolved() -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    note["synthetic_excerpt"] = "Unbounded values are not accepted."
    adapter.get_bound_contact()

    with pytest.raises(NoteContractError, match="extra"):
        adapter.create_meeting_note(note)
    assert adapter.POST_ATTEMPTS == 0
    assert [method for method, _, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize(
    "case_id",
    ["note_readback_id_mismatch", "note_readback_contact_mismatch"],
)
def test_readback_identity_mismatch_block(case_id: str) -> None:
    adapter, transport = _adapter(case_id)
    _create(adapter)
    body = _post_body(transport)
    _replace_readback_body(transport, body)

    with pytest.raises(TransportError):
        adapter.verify_meeting_note()


def test_search_list_generic_execute_and_stage_routes_absent() -> None:
    public_methods = {
        name for name in vars(NotePathAdapter) if not name.startswith("_")
    }

    assert public_methods == {
        "get_bound_contact",
        "create_meeting_note",
        "verify_meeting_note",
    }
    source = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_ROOT.glob("*.py"))
    assert "execute_operation" not in source
    assert "/opportunit" not in source.lower()
    assert "/contacts/" in source


def test_real_client_socket_dns_env_and_live_imports_absent() -> None:
    forbidden_import_roots = {
        "requests",
        "httpx",
        "urllib",
        "socket",
        "os",
        "asyncio",
    }
    forbidden_imports = {
        "integrations.ghl.at1_live_transport_adapter",
        "integrations.ghl.at1_live_transport_serializer",
        "integrations.ghl.bounded_at1_executor",
    }
    for path in SOURCE_ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {name.name.split(".", 1)[0] for name in node.names}
                assert not imported & forbidden_import_roots
            if isinstance(node, ast.ImportFrom):
                assert node.module not in forbidden_imports
                assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots


def test_network_calls_and_external_effects_zero() -> None:
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")

    assert "NETWORK_CALLS = 0" in source
    assert "HIGHLEVEL_NETWORK_CALLS = 0" in source
    assert "EXTERNAL_EFFECTS = 0" in source
    assert FIXTURE["network_calls"] == 0
    assert FIXTURE["external_effects"] == 0
