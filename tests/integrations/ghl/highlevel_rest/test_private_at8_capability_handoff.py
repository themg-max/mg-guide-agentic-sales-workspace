from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path

import pytest

import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest import (
    BindingError,
    DeterministicFakeTransport,
    NotePathAdapter,
)


DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY = (
    "NW008_AT8B_GHL_REST_NOTE_PATH_MUTATION_GUARD_HARDENING_IMPLEMENTATION_001"
)
AT8_SOURCE_EXECUTION_UNIT = (
    "NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002"
)
AT8_SOURCE_PROOF_MERGE_SHA = "6256f287bbd88effc2ef1cd13a801faec79a0af2"
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


def _adapter(*, consumer_authorization_identity: str, consumer_workflow_run_id: str):
    transport = DeterministicFakeTransport(deepcopy(FIXTURE), "note_create_success")
    adapter = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        transport=transport,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )
    return adapter, transport


def _synthetic_binding() -> note_path_module._PrivateContactBinding:
    return note_path_module._PrivateContactBinding(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )


class _InjectedSyntheticBindingSource:
    def __init__(self, binding: note_path_module._PrivateContactBinding) -> None:
        self._binding = binding

    def get_binding(self) -> note_path_module._PrivateContactBinding:
        return self._binding


def test_valid_private_binding_handoff_shape() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-valid-001"
    capability = note_path_module._handoff_private_at8_verified_binding_capability(
        private_binding=_synthetic_binding(),
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
        workflow_id="meeting_follow_up_v1",
    )

    assert note_path_module._PrivateContactBinding.__dataclass_params__.frozen is True
    assert note_path_module._VerifiedContactBindingCapability.__dataclass_params__.frozen is True
    assert capability.workflow_id == "meeting_follow_up_v1"
    assert capability.source_execution_unit == AT8_SOURCE_EXECUTION_UNIT
    assert capability.source_proof_merge_sha == AT8_SOURCE_PROOF_MERGE_SHA
    assert capability.location_id == "synthetic-location-001"
    assert capability.contact_id == "synthetic-contact-001"
    assert capability.consumer_authorization_identity == DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY
    assert capability.consumer_workflow_run_id == workflow_run_id
    assert capability.trusted_source == "private_at8_verified_binding_handoff"
    assert capability._trust_marker is note_path_module._CAPABILITY_TRUST_MARKER
    assert "trusted_source" not in inspect.signature(
        note_path_module._handoff_private_at8_verified_binding_capability
    ).parameters
    assert "_trust_marker" not in inspect.signature(
        note_path_module._handoff_private_at8_verified_binding_capability
    ).parameters

    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = capability
    assert adapter._require_trusted_verified_capability() is capability
    assert transport.calls == []


def test_handoff_accepts_injected_private_binding_source() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-source-001"
    capability = note_path_module._handoff_private_at8_verified_binding_capability(
        private_binding_source=_InjectedSyntheticBindingSource(_synthetic_binding()),
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
        workflow_id="meeting_follow_up_v1",
    )
    assert capability.contact_id == "synthetic-contact-001"
    assert capability._trust_marker is note_path_module._CAPABILITY_TRUST_MARKER


def test_at8_provenance_mismatch_blocks() -> None:
    with pytest.raises(BindingError, match="source proof is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            private_binding=_synthetic_binding(),
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha="0" * 40,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-proof-001",
            workflow_id="meeting_follow_up_v1",
        )
    with pytest.raises(BindingError, match="source execution unit is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            private_binding=_synthetic_binding(),
            source_execution_unit="NW008_WRONG_EXECUTION_UNIT",
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-unit-001",
            workflow_id="meeting_follow_up_v1",
        )


def test_wrong_consumer_authorization_blocks() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-authz-001"
    capability = note_path_module._handoff_private_at8_verified_binding_capability(
        private_binding=_synthetic_binding(),
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        consumer_authorization_identity="WRONG_AUTHZ_IDENTITY",
        consumer_workflow_run_id=workflow_run_id,
        workflow_id="meeting_follow_up_v1",
    )
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = capability
    with pytest.raises(BindingError, match="authorization binding is invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_wrong_workflow_run_blocks() -> None:
    capability = note_path_module._handoff_private_at8_verified_binding_capability(
        private_binding=_synthetic_binding(),
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-other-001",
        workflow_id="meeting_follow_up_v1",
    )
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-run-001",
    )
    adapter._verified_contact_binding_capability = capability
    with pytest.raises(BindingError, match="workflow run binding is invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_wrong_workflow_id_blocks() -> None:
    with pytest.raises(BindingError, match="workflow binding is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            private_binding=_synthetic_binding(),
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-workflow-001",
            workflow_id="wrong_workflow_v2",
        )


def test_caller_forged_capability_blocks() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-forged-001",
    )
    forged = note_path_module._VerifiedContactBindingCapability(
        workflow_id="meeting_follow_up_v1",
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-forged-001",
        trusted_source="private_at8_verified_binding_handoff",
        _trust_marker=object(),
    )
    adapter._verified_contact_binding_capability = forged
    with pytest.raises(BindingError, match="invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_public_trusted_source_injection_blocks() -> None:
    with pytest.raises(TypeError):
        note_path_module._handoff_private_at8_verified_binding_capability(
            private_binding=_synthetic_binding(),
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-source-inject-001",
            workflow_id="meeting_follow_up_v1",
            trusted_source="caller-supplied-trusted-source",
        )
    with pytest.raises(BindingError, match="trusted source is invalid"):
        note_path_module._mint_trusted_capability(
            workflow_id="meeting_follow_up_v1",
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-source-inject-002",
            trusted_source="caller-supplied-trusted-source",
        )


def test_public_boolean_promotion_blocks() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-boolean-001",
    )
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"
    adapter.trusted = True
    adapter.authorized = True
    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert adapter._verified_contact_binding_capability is None
    assert transport.calls == []


def test_synthetic_test_factory_real_id_use_blocks() -> None:
    with pytest.raises(BindingError, match="must be synthetic"):
        NotePathAdapter._build_at8_shaped_test_capability(
            location_id="live-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-factory-001",
        )
    with pytest.raises(BindingError, match="must be synthetic"):
        NotePathAdapter._build_at8_shaped_test_capability(
            location_id="synthetic-location-001",
            contact_id="live-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-factory-002",
        )


def test_private_binding_is_data_not_authority() -> None:
    binding = _synthetic_binding()
    assert not hasattr(binding, "_trust_marker")
    assert not hasattr(binding, "trusted_source")
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-data-001",
    )
    adapter.private_binding = binding
    adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"
    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert adapter._verified_contact_binding_capability is None
    assert transport.calls == []


def test_private_binding_publication_absent() -> None:
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")
    assert "print(" not in source
    assert "logging" not in source
    public_methods = {
        name for name in vars(NotePathAdapter) if not name.startswith("_")
    }
    assert public_methods == {
        "get_bound_contact",
        "create_meeting_note",
        "verify_meeting_note",
    }
    assert "handoff_private_at8_verified_binding_capability" not in public_methods
    assert "_handoff_private_at8_verified_binding_capability" not in dir(NotePathAdapter)


def test_no_provider_get_and_zero_network_effects() -> None:
    assert note_path_module.NETWORK_CALLS == 0
    assert note_path_module.HIGHLEVEL_NETWORK_CALLS == 0
    assert note_path_module.EXTERNAL_EFFECTS == 0
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")
    assert "At1ExecutionStore" not in source
    assert "secretmanager" not in source.lower()
    assert "Secret Manager" not in source
    assert "at1_execution_store" not in source
    assert "at1_live_transport_adapter" not in source
