from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import pytest

import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl import At1ExecutionStore
from integrations.ghl.at1_commitment_key_provider import SyntheticCommitmentKeyProvider
from integrations.ghl.highlevel_rest import (
    BindingError,
    DeterministicFakeTransport,
    FakeResponse,
    NoteContractError,
    NotePathAdapter,
    TransportError,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
FIXTURE_PATH = REPO_ROOT / "fixtures" / "ghl" / "highlevel_rest" / "note-path-fixtures.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY = (
    "NW008_AT8G_GHL_REST_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001"
)
_VERSION_RESOURCE = "projects/synthetic-project/secrets/at1-commitment-key/versions/1"


@pytest.fixture(autouse=True)
def _reset_shared_ledger() -> None:
    note_path_module._reset_shared_test_ledger()


@pytest.fixture
def store(tmp_path: Path) -> At1ExecutionStore:
    return At1ExecutionStore(
        db_path=tmp_path / "note-path-at1.sqlite3",
        commitment_material=_material("synthetic-commitment-key"),
    )


def _material(payload: str):
    return SyntheticCommitmentKeyProvider(
        payload=payload,
        version_resource=_VERSION_RESOURCE,
    ).resolve()


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


def _adapter(
    case_id: str,
    store: At1ExecutionStore,
    *,
    consumer_workflow_run_id: str = "synthetic-workflow-run-at8g-001",
    consumer_authorization_identity: str = DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
    location_id: str = "synthetic-location-001",
    contact_id: str = "synthetic-contact-001",
) -> tuple[NotePathAdapter, DeterministicFakeTransport]:
    transport = DeterministicFakeTransport(deepcopy(FIXTURE), case_id)
    return (
        NotePathAdapter(
            location_id=location_id,
            contact_id=contact_id,
            transport=transport,
            consumer_authorization_identity=consumer_authorization_identity,
            consumer_workflow_run_id=consumer_workflow_run_id,
            execution_store=store,
        ),
        transport,
    )


def _grant_run_id(
    consumer_authorization_identity: str, consumer_workflow_run_id: str
) -> str:
    canonical = note_path_module.NotePathAdapter._canonical_json(
        {
            "consumer_authorization_identity": consumer_authorization_identity,
            "consumer_workflow_run_id": consumer_workflow_run_id,
            "mapping_version": note_path_module._MAPPING_VERSION,
            "namespace": note_path_module._GRANT_RUN_ID_NAMESPACE,
            "operation": note_path_module._NOTE_CREATE_OPERATION,
        },
    )
    digest = sha256(canonical.encode("utf-8")).hexdigest()
    return f"npgr1:{digest}"


def _create(adapter: NotePathAdapter) -> None:
    if adapter.CONTACT_PREFLIGHT_VERIFIED == "NO":
        adapter.get_bound_contact()
    adapter.create_meeting_note(_note())


def test_capability_check_occurs_before_store_calls(store: At1ExecutionStore) -> None:
    adapter, _ = _adapter("note_create_success", store)

    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())

    assert store.list_private_attempts(_grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    )) == []


def test_note_contract_validation_occurs_before_store_calls(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    adapter.get_bound_contact()
    bad_note = _note()
    del bad_note["meeting_id"]

    with pytest.raises(NoteContractError):
        adapter.create_meeting_note(bad_note)

    assert store.list_private_attempts(_grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    )) == []


def test_mark_dispatched_occurs_before_transport_dispatch(store: At1ExecutionStore) -> None:
    class _InspectingTransport(DeterministicFakeTransport):
        def __init__(self, fixture: dict[str, Any], case_id: str, store: At1ExecutionStore) -> None:
            super().__init__(fixture, case_id)
            self.store = store
            self.grant_run_id = _grant_run_id(
                DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
                "synthetic-workflow-run-at8g-001",
            )

        def dispatch(
            self, method: str, path: str, body: dict[str, object] | None = None
        ) -> FakeResponse:
            if method == "POST":
                attempts = self.store.list_private_attempts(self.grant_run_id)
                assert len(attempts) == 1
                assert attempts[0]["state"] == "DISPATCHED"
            return super().dispatch(method, path, body)

    transport = _InspectingTransport(deepcopy(FIXTURE), "note_create_success", store)
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-at8g-001",
        execution_store=store,
    )
    adapter.get_bound_contact()
    adapter.create_meeting_note(_note())


def test_successful_note_create_creates_exactly_ordinal_one(store: At1ExecutionStore) -> None:
    adapter, transport = _adapter("note_create_success", store)
    _create(adapter)

    grant_run_id = _grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    )
    attempts = store.list_private_attempts(grant_run_id)
    assert len(attempts) == 1
    assert attempts[0]["operation_ordinal"] == note_path_module.NOTE_CREATE_OPERATION_ORDINAL
    assert attempts[0]["operation_id"] == note_path_module._NOTE_CREATE_OPERATION
    assert attempts[0]["state"] == "RESPONSE_CAPTURED"
    assert attempts[0]["parse_success"] is True
    assert attempts[0]["semantic_success"] is True
    assert attempts[0]["business_effect_truth"] is None
    transport.assert_exhausted()


def test_second_note_create_same_grant_run_blocked(store: At1ExecutionStore) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-duplicate-001"
    adapter, transport = _adapter(
        "note_create_success", store, consumer_workflow_run_id=workflow_run_id
    )
    _create(adapter)

    with pytest.raises(TransportError, match="store reservation refused") as exc_info:
        _create(adapter)

    assert isinstance(exc_info.value.__cause__, note_path_module.DuplicateBusinessOrdinalError)
    assert [method for method, _, _ in transport.calls].count("POST") == 1


def test_grant_run_id_matches_authorized_npgr1_formula(store: At1ExecutionStore) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-formula-001"
    other_workflow_run_id = "synthetic-workflow-run-at8g-formula-002"
    other_authz = "NW008_AT8G_FORMULA_AUTHORIZATION_002"
    adapter, _ = _adapter(
        "note_create_success",
        store,
        consumer_workflow_run_id=workflow_run_id,
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    same_binding_adapter, _ = _adapter(
        "note_create_success",
        store,
        consumer_workflow_run_id=workflow_run_id,
        location_id="synthetic-location-002",
        contact_id="synthetic-contact-002",
    )
    other_authz_adapter, _ = _adapter(
        "note_create_success",
        store,
        consumer_authorization_identity=other_authz,
        consumer_workflow_run_id=workflow_run_id,
    )
    other_run_adapter, _ = _adapter(
        "note_create_success",
        store,
        consumer_workflow_run_id=other_workflow_run_id,
    )

    grant_run_id = adapter._deterministic_grant_run_id()
    prefix = grant_run_id[:6]
    digest = grant_run_id[6:]
    assert prefix == "npgr1:"
    canonical = note_path_module.NotePathAdapter._canonical_json(
        {
            "consumer_authorization_identity": DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            "consumer_workflow_run_id": workflow_run_id,
            "mapping_version": note_path_module._MAPPING_VERSION,
            "namespace": note_path_module._GRANT_RUN_ID_NAMESPACE,
            "operation": note_path_module._NOTE_CREATE_OPERATION,
        },
    )
    expected_digest = sha256(canonical.encode("utf-8")).hexdigest()
    assert digest == expected_digest
    assert len(digest) == 64
    assert digest == digest.lower()
    assert set(digest) <= set("0123456789abcdef")
    assert grant_run_id == f"npgr1:{expected_digest}"
    assert same_binding_adapter._deterministic_grant_run_id() == grant_run_id
    assert other_authz_adapter._deterministic_grant_run_id() != grant_run_id
    assert other_run_adapter._deterministic_grant_run_id() != grant_run_id
    assert other_authz_adapter._deterministic_grant_run_id()[:6] == "npgr1:"
    assert other_run_adapter._deterministic_grant_run_id()[:6] == "npgr1:"


def test_different_workflow_run_distinct_grant_run_id(store: At1ExecutionStore) -> None:
    first_run = "synthetic-workflow-run-at8g-first-001"
    second_run = "synthetic-workflow-run-at8g-second-001"
    first_adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=first_run
    )
    second_adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=second_run
    )
    first_adapter.get_bound_contact()
    second_adapter.get_bound_contact()

    first_adapter.create_meeting_note(_note())
    second_adapter.create_meeting_note(_note())

    first_grant = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, first_run)
    second_grant = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, second_run)
    assert first_grant != second_grant
    assert len(store.list_private_attempts(first_grant)) == 1
    assert len(store.list_private_attempts(second_grant)) == 1


def test_different_authorization_distinct_grant_run_id(store: At1ExecutionStore) -> None:
    first_authz = "NW008_AT8G_FIRST_AUTHORIZATION_001"
    second_authz = "NW008_AT8G_SECOND_AUTHORIZATION_001"
    run_id = "synthetic-workflow-run-at8g-authz-001"
    first_adapter, _ = _adapter(
        "note_create_success", store, consumer_authorization_identity=first_authz
    )
    second_adapter, _ = _adapter(
        "note_create_success", store, consumer_authorization_identity=second_authz
    )
    first_adapter.get_bound_contact()
    second_adapter.get_bound_contact()

    first_adapter.create_meeting_note(_note())
    second_adapter.create_meeting_note(_note())

    first_grant = _grant_run_id(first_authz, "synthetic-workflow-run-at8g-001")
    second_grant = _grant_run_id(second_authz, "synthetic-workflow-run-at8g-001")
    assert first_grant != second_grant


def test_contact_and_location_excluded_from_mapping(store: At1ExecutionStore) -> None:
    base_run = "synthetic-workflow-run-at8g-mapping-001"
    first_adapter, first_transport = _adapter(
        "note_create_success",
        store,
        consumer_workflow_run_id=base_run,
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    second_adapter, _ = _adapter(
        "note_create_success",
        store,
        consumer_workflow_run_id=base_run,
        location_id="synthetic-location-002",
        contact_id="synthetic-contact-002",
    )

    first_grant = first_adapter._deterministic_grant_run_id()
    second_grant = second_adapter._deterministic_grant_run_id()
    assert first_grant[:6] == "npgr1:"
    assert first_grant == second_grant
    assert first_grant == _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, base_run)

    _create(first_adapter)
    assert [method for method, _, _ in first_transport.calls].count("POST") == 1
    assert len(store.list_private_attempts(first_grant)) == 1
    assert store.list_private_attempts(second_grant) == store.list_private_attempts(
        first_grant
    )


def test_redacted_request_envelope_contains_no_private_data(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    _create(adapter)

    attempts = store.list_private_attempts(_grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    ))
    envelope = attempts[0]["request_envelope"]
    raw_envelope = json.dumps(envelope)

    assert "synthetic-location" not in raw_envelope
    assert "synthetic-contact" not in raw_envelope
    assert "Synthetic discovery meeting" not in raw_envelope
    assert "Automated reminders" not in raw_envelope
    assert "Share proposal" not in raw_envelope
    assert "body" not in envelope
    assert "meeting_summary" not in envelope
    assert "needs" not in envelope
    assert "objections" not in envelope
    assert "commitments" not in envelope
    assert "note_content_digest" in envelope
    assert "provider_body_digest" in envelope
    assert set(envelope) <= {
        "namespace",
        "operation",
        "operation_ordinal",
        "mapping_version",
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
        "workflow_id",
        "request_id",
        "note_content_digest",
        "provider_body_digest",
    }


def test_redacted_response_envelope_contains_no_private_data(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    _create(adapter)

    attempts = store.list_private_attempts(_grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    ))
    envelope = attempts[0]["response_envelope"]
    raw_envelope = json.dumps(envelope)

    assert "synthetic-note-001" not in raw_envelope
    assert "synthetic-contact" not in raw_envelope
    assert "status" not in envelope
    assert "provider_note_id_digest" not in envelope
    assert envelope.get("response_status_class") == "ok"
    assert set(envelope) <= {
        "namespace",
        "operation",
        "operation_ordinal",
        "mapping_version",
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
        "workflow_id",
        "request_id",
        "note_content_digest",
        "provider_body_digest",
        "response_status_class",
    }


def test_duplicate_ordinal_translates_to_transport_error_with_chained_cause(
    store: At1ExecutionStore,
) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-dup-ord-001"
    grant_run_id = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id)
    store.acquire_claim(grant_run_id, DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY)
    store.record_attempt(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
        operation_id=note_path_module._NOTE_CREATE_OPERATION,
        request_id="pre-existing-request-id",
        request_envelope={},
    )
    store.mark_dispatched(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
    )
    store.capture_response(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
        response_envelope={"status": "ok"},
    )
    store.record_parse_outcome(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
        success=True,
    )
    store.record_semantic_outcome(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
        success=True,
    )

    adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=workflow_run_id
    )
    adapter.get_bound_contact()

    with pytest.raises(TransportError, match="store reservation refused") as exc_info:
        adapter.create_meeting_note(_note())

    assert isinstance(exc_info.value.__cause__, note_path_module.DuplicateBusinessOrdinalError)


def test_run_continuable_refusal_translates_to_transport_error_with_chained_cause(
    store: At1ExecutionStore,
) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-continuable-001"
    grant_run_id = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id)
    store.acquire_claim(grant_run_id, DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY)
    store.record_attempt(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
        operation_id=note_path_module._NOTE_CREATE_OPERATION,
        request_id="pre-existing-request-id",
        request_envelope={},
    )
    store.mark_dispatched(
        grant_run_id=grant_run_id,
        operation_ordinal=note_path_module.NOTE_CREATE_OPERATION_ORDINAL,
    )

    adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=workflow_run_id
    )
    adapter.get_bound_contact()

    with pytest.raises(TransportError, match="store reservation refused") as exc_info:
        adapter.create_meeting_note(_note())

    assert isinstance(exc_info.value.__cause__, note_path_module.RunContinuationRefusedError)


def test_claim_owner_is_consumer_authorization_identity(store: At1ExecutionStore) -> None:
    adapter, _ = _adapter("note_create_success", store)
    _create(adapter)

    grant_run_id = _grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    )
    row = store._connection.execute(
        "SELECT owner_id FROM execution_claims WHERE grant_run_id = ?",
        (grant_run_id,),
    ).fetchone()
    assert row is not None
    assert row["owner_id"] == DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY


def test_same_owner_reclaim(store: At1ExecutionStore) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-reclaim-001"
    grant_run_id = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id)

    store.acquire_claim(grant_run_id, DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY)
    store.acquire_claim(grant_run_id, DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY)

    adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=workflow_run_id
    )
    adapter.get_bound_contact()
    adapter.create_meeting_note(_note())

    assert len(store.list_private_attempts(grant_run_id)) == 1


def test_direct_store_boundary_different_owner_contention(
    store: At1ExecutionStore,
) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-contention-001"
    grant_run_id = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id)
    store.acquire_claim(grant_run_id, "OTHER_CONSUMER_IDENTITY_001")

    adapter, _ = _adapter(
        "note_create_success", store, consumer_workflow_run_id=workflow_run_id
    )
    adapter.get_bound_contact()

    with pytest.raises(TransportError, match="store reservation refused") as exc_info:
        adapter.create_meeting_note(_note())

    assert isinstance(exc_info.value.__cause__, note_path_module.ExecutionClaimError)


def test_restart_preserves_reservation(tmp_path: Path) -> None:
    db_path = tmp_path / "note-path-at1-restart.sqlite3"
    commitment_key = "synthetic-commitment-key"
    workflow_run_id = "synthetic-workflow-run-at8g-restart-001"

    store_a = At1ExecutionStore(
        db_path=db_path,
        commitment_material=_material(commitment_key),
    )
    first_adapter, first_transport = _adapter(
        "note_create_success", store_a, consumer_workflow_run_id=workflow_run_id
    )
    _create(first_adapter)
    assert [method for method, _, _ in first_transport.calls].count("POST") == 1

    store_a._connection.close()
    del store_a

    store_b = At1ExecutionStore(
        db_path=db_path,
        commitment_material=_material(commitment_key),
    )
    second_adapter, second_transport = _adapter(
        "note_create_success", store_b, consumer_workflow_run_id=workflow_run_id
    )
    second_adapter.get_bound_contact()
    with pytest.raises(TransportError, match="store reservation refused") as exc_info:
        second_adapter.create_meeting_note(_note())

    assert isinstance(
        exc_info.value.__cause__,
        (
            note_path_module.DuplicateBusinessOrdinalError,
            note_path_module.RunContinuationRefusedError,
        ),
    )
    assert [method for method, _, _ in second_transport.calls] == ["GET"]
    grant_run_id = _grant_run_id(DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id)
    assert len(store_b.list_private_attempts(grant_run_id)) == 1


def _assert_attempt_state_error_translated(exc: BaseException) -> None:
    assert type(exc) is TransportError
    assert not isinstance(exc, note_path_module.AttemptStateError)
    assert isinstance(exc.__cause__, note_path_module.AttemptStateError)


def test_parse_outcome_attempt_state_error_translates_to_transport_error(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    adapter.get_bound_contact()

    def _boom(**kwargs: Any) -> None:
        raise note_path_module.AttemptStateError("injected parse outcome fault")

    store.record_parse_outcome = _boom  # type: ignore[method-assign]

    try:
        adapter.create_meeting_note(_note())
    except note_path_module.AttemptStateError:
        pytest.fail("raw AttemptStateError leaked from parse lifecycle")
    except TransportError as exc:
        _assert_attempt_state_error_translated(exc)
    else:
        pytest.fail("expected TransportError from parse lifecycle")


def test_semantic_outcome_attempt_state_error_translates_to_transport_error(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    adapter.get_bound_contact()

    def _boom(**kwargs: Any) -> None:
        raise note_path_module.AttemptStateError("injected semantic outcome fault")

    store.record_semantic_outcome = _boom  # type: ignore[method-assign]

    try:
        adapter.create_meeting_note(_note())
    except note_path_module.AttemptStateError:
        pytest.fail("raw AttemptStateError leaked from semantic lifecycle")
    except TransportError as exc:
        _assert_attempt_state_error_translated(exc)
    else:
        pytest.fail("expected TransportError from semantic lifecycle")


def test_capture_response_attempt_state_error_translates_to_transport_error(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    adapter.get_bound_contact()

    def _boom(**kwargs: Any) -> str:
        raise note_path_module.AttemptStateError("injected capture response fault")

    store.capture_response = _boom  # type: ignore[method-assign]

    try:
        adapter.create_meeting_note(_note())
    except note_path_module.AttemptStateError:
        pytest.fail("raw AttemptStateError leaked from capture_response")
    except TransportError as exc:
        _assert_attempt_state_error_translated(exc)
    else:
        pytest.fail("expected TransportError from capture_response")


def test_mark_terminal_attempt_state_error_translates_to_transport_error(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_ambiguous_result", store)
    adapter.get_bound_contact()

    def _boom(**kwargs: Any) -> None:
        raise note_path_module.AttemptStateError("injected mark_terminal fault")

    store.mark_terminal = _boom  # type: ignore[method-assign]

    try:
        adapter.create_meeting_note(_note())
    except note_path_module.AttemptStateError:
        pytest.fail("raw AttemptStateError leaked from mark_terminal")
    except TransportError as exc:
        _assert_attempt_state_error_translated(exc)
    else:
        pytest.fail("expected TransportError from mark_terminal")


def test_ambiguity_terminalizes_unknown(store: At1ExecutionStore) -> None:
    workflow_run_id = "synthetic-workflow-run-at8g-ambiguous-001"
    adapter, _ = _adapter(
        "note_create_ambiguous_result", store, consumer_workflow_run_id=workflow_run_id
    )
    adapter.get_bound_contact()

    with pytest.raises(TransportError, match="not retried"):
        adapter.create_meeting_note(_note())

    attempts = store.list_private_attempts(_grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY, workflow_run_id
    ))
    assert len(attempts) == 1
    assert attempts[0]["state"] == "TERMINAL"
    assert attempts[0]["business_effect_truth"] == "UNKNOWN"
    assert attempts[0]["terminal_failure_code"] == "AMBIGUOUS_POST"


def test_pr107_verified_capability_remains_mandatory(store: At1ExecutionStore) -> None:
    adapter, _ = _adapter("note_create_success", store)
    capability = note_path_module.NotePathAdapter._build_at8_shaped_test_capability(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-at8g-001",
    )
    object.__setattr__(
        capability, "source_proof_merge_sha", "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    )
    adapter._verified_contact_binding_capability = capability
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"

    with pytest.raises(BindingError, match="source proof is invalid"):
        adapter.create_meeting_note(_note())


def test_compute_public_projection_not_used_as_note_path_truth(
    store: At1ExecutionStore,
) -> None:
    adapter, _ = _adapter("note_create_success", store)
    _create(adapter)

    grant_run_id = _grant_run_id(
        DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        "synthetic-workflow-run-at8g-001",
    )
    attempts = store.list_private_attempts(grant_run_id)
    assert attempts[0]["business_effect_truth"] is None

    projection = store.compute_public_projection(grant_run_id)
    assert projection["business_effect_truth"] in {"UNKNOWN", "NO"}


def test_zero_network_calls(store: At1ExecutionStore) -> None:
    adapter, transport = _adapter("note_create_success", store)
    _create(adapter)

    assert note_path_module.NETWORK_CALLS == 0
    assert note_path_module.HIGHLEVEL_NETWORK_CALLS == 0
    assert note_path_module.EXTERNAL_EFFECTS == 0
    assert FIXTURE["network_calls"] == 0
    assert FIXTURE["external_effects"] == 0
    assert [method for method, _, _ in transport.calls] == ["GET", "POST"]
