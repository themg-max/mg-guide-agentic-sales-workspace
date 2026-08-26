from __future__ import annotations

from copy import deepcopy
import inspect
import json
from pathlib import Path
import pickle

import pytest

import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest import (
    BindingError,
    DeterministicFakeTransport,
    NotePathAdapter,
    TransportError,
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


def _issue_synthetic_capability(
    *,
    consumer_workflow_run_id: str,
    consumer_authorization_identity: str = DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
    location_id: str = "synthetic-location-001",
    contact_id: str = "synthetic-contact-001",
    workflow_id: str = "meeting_follow_up_v1",
    source_execution_unit: str = AT8_SOURCE_EXECUTION_UNIT,
    source_proof_merge_sha: str = AT8_SOURCE_PROOF_MERGE_SHA,
) -> note_path_module._VerifiedContactBindingCapability:
    return note_path_module._issue_synthetic_test_capability(
        location_id=location_id,
        contact_id=contact_id,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
        workflow_id=workflow_id,
        source_execution_unit=source_execution_unit,
        source_proof_merge_sha=source_proof_merge_sha,
    )


def _root_owned_private_delivery_reference() -> object:
    trusted_binding_source = NotePathAdapter._build_private_at8_verified_binding_source(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    return note_path_module._register_root_owned_private_binding_delivery_reference(
        trusted_binding_source=trusted_binding_source
    )


def _root_owned_private_provenance_source(
    *,
    location_id: str = "opaque-fixture-location-001",
    contact_id: str = "opaque-fixture-contact-001",
    source_execution_unit: str = AT8_SOURCE_EXECUTION_UNIT,
    source_proof_merge_sha: str = AT8_SOURCE_PROOF_MERGE_SHA,
) -> note_path_module._TrustedPrivateBindingSource:
    return note_path_module._issue_private_at8_handoff_source_from_root_owned_private_provenance(
        location_id=location_id,
        contact_id=contact_id,
        source_execution_unit=source_execution_unit,
        source_proof_merge_sha=source_proof_merge_sha,
    )


class _UntrustedStructuralBindingSource:
    def get_trusted_binding_source(self) -> note_path_module._TrustedPrivateBindingSource:
        return note_path_module._TrustedPrivateBindingSource(
            workflow_id="meeting_follow_up_v1",
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
            trusted_origin="private_at8_verified_binding_handoff",
            _trust_marker=object(),
        )


def test_valid_internal_private_at8_handoff() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-valid-001"
    trusted_binding_source = NotePathAdapter._build_private_at8_verified_binding_source(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    capability = note_path_module._handoff_private_at8_verified_binding_capability(
        trusted_binding_source=trusted_binding_source,
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
        workflow_id="meeting_follow_up_v1",
    )

    assert note_path_module._PrivateContactBinding.__dataclass_params__.frozen is True
    assert note_path_module._VerifiedContactBindingCapability.__dataclass_params__.frozen is True
    assert trusted_binding_source.trusted_origin == "private_at8_verified_binding_handoff"
    assert capability.workflow_id == "meeting_follow_up_v1"
    assert capability.source_execution_unit == AT8_SOURCE_EXECUTION_UNIT
    assert capability.source_proof_merge_sha == AT8_SOURCE_PROOF_MERGE_SHA
    assert capability.location_id == "synthetic-location-001"
    assert capability.contact_id == "synthetic-contact-001"
    assert capability.consumer_authorization_identity == DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY
    assert capability.consumer_workflow_run_id == workflow_run_id
    assert capability.trusted_binding_source is trusted_binding_source
    assert capability.trusted_binding_source.trusted_origin == (
        "private_at8_verified_binding_handoff"
    )
    assert "trusted_source" not in inspect.signature(
        note_path_module._handoff_private_at8_verified_binding_capability
    ).parameters
    assert "trusted_binding_source" in inspect.signature(
        note_path_module._handoff_private_at8_verified_binding_capability
    ).parameters
    assert not hasattr(note_path_module, "_issue_private_at8_handoff_capability")

    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = capability
    assert adapter._require_trusted_verified_capability() is capability
    assert transport.calls == []

    bound_adapter, bound_transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-valid-bound-001",
    )
    bound_adapter.get_bound_contact()
    bound_capability = bound_adapter._require_trusted_verified_capability()
    assert bound_capability.trusted_binding_source.trusted_origin == (
        "fake_transport_bound_contact_verification"
    )
    assert [method for method, _, _ in bound_transport.calls] == ["GET"]


def test_root_owned_private_delivery_reference_issues_capability() -> None:
    workflow_run_id = "synthetic-workflow-run-root-owned-delivery-001"
    reference = _root_owned_private_delivery_reference()
    signature = inspect.signature(
        note_path_module._issue_root_owned_private_binding_delivery_capability
    )

    assert tuple(signature.parameters) == (
        "safe_private_delivery_reference",
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
    )
    assert "location_id" not in signature.parameters
    assert "contact_id" not in signature.parameters
    assert "private_binding" not in signature.parameters
    assert "source_locator" not in signature.parameters
    assert not hasattr(
        NotePathAdapter, "_issue_root_owned_private_binding_delivery_capability"
    )

    capability = note_path_module._issue_root_owned_private_binding_delivery_capability(
        safe_private_delivery_reference=reference,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )

    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = capability

    assert adapter._require_trusted_verified_capability() is capability
    assert capability.trusted_binding_source.trusted_origin == (
        "private_at8_verified_binding_handoff"
    )
    assert transport.calls == []


def test_opaque_ids_without_trusted_provenance_fail_closed() -> None:
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            trusted_binding_source=note_path_module._TrustedPrivateBindingSource(
                workflow_id="meeting_follow_up_v1",
                source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
                source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
                location_id="opaque-fixture-location-without-provenance-001",
                contact_id="opaque-fixture-contact-without-provenance-001",
                synthetic_contact_bound=True,
                private_allowlist_complete=True,
                relationship_verified=True,
                trusted_origin="private_at8_verified_binding_handoff",
                _trust_marker=object(),
            ),
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-opaque-untrusted-001",
            workflow_id="meeting_follow_up_v1",
        )


def test_opaque_ids_with_valid_root_owned_private_provenance_pass() -> None:
    workflow_run_id = "synthetic-workflow-run-opaque-root-owned-001"
    trusted_binding_source = _root_owned_private_provenance_source()
    reference = note_path_module._register_root_owned_private_binding_delivery_reference(
        trusted_binding_source=trusted_binding_source
    )
    capability = note_path_module._issue_root_owned_private_binding_delivery_capability(
        safe_private_delivery_reference=reference,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    transport = DeterministicFakeTransport(deepcopy(FIXTURE), "note_create_success")
    adapter = NotePathAdapter(
        location_id="opaque-fixture-location-001",
        contact_id="opaque-fixture-contact-001",
        transport=transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = capability

    assert capability.location_id == "opaque-fixture-location-001"
    assert capability.contact_id == "opaque-fixture-contact-001"
    assert capability.trusted_binding_source.synthetic_contact_bound is True
    assert capability.trusted_binding_source.private_allowlist_complete is True
    assert capability.trusted_binding_source.relationship_verified is True
    assert adapter._require_trusted_verified_capability() is capability
    assert transport.calls == []


def test_opaque_ids_with_synthetic_false_fail_closed() -> None:
    trusted_binding_source = _root_owned_private_provenance_source(
        location_id="opaque-fixture-location-synthetic-false-001",
        contact_id="opaque-fixture-contact-synthetic-false-001",
    )
    object.__setattr__(trusted_binding_source, "synthetic_contact_bound", False)

    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._register_root_owned_private_binding_delivery_reference(
            trusted_binding_source=trusted_binding_source
        )


def test_opaque_ids_with_allowlist_complete_false_fail_closed() -> None:
    trusted_binding_source = _root_owned_private_provenance_source(
        location_id="opaque-fixture-location-allowlist-false-001",
        contact_id="opaque-fixture-contact-allowlist-false-001",
    )
    object.__setattr__(trusted_binding_source, "private_allowlist_complete", False)

    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._register_root_owned_private_binding_delivery_reference(
            trusted_binding_source=trusted_binding_source
        )


def test_opaque_ids_with_relationship_verified_false_fail_closed() -> None:
    trusted_binding_source = _root_owned_private_provenance_source(
        location_id="opaque-fixture-location-relationship-false-001",
        contact_id="opaque-fixture-contact-relationship-false-001",
    )
    object.__setattr__(trusted_binding_source, "relationship_verified", False)

    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._register_root_owned_private_binding_delivery_reference(
            trusted_binding_source=trusted_binding_source
        )


def test_opaque_private_provenance_wrong_source_execution_unit_fails_closed() -> None:
    with pytest.raises(BindingError, match="source execution unit is invalid"):
        _root_owned_private_provenance_source(
            location_id="opaque-fixture-location-wrong-unit-001",
            contact_id="opaque-fixture-contact-wrong-unit-001",
            source_execution_unit="NW008_WRONG_EXECUTION_UNIT",
        )


def test_opaque_private_provenance_wrong_source_proof_fails_closed() -> None:
    with pytest.raises(BindingError, match="source proof is invalid"):
        _root_owned_private_provenance_source(
            location_id="opaque-fixture-location-wrong-proof-001",
            contact_id="opaque-fixture-contact-wrong-proof-001",
            source_proof_merge_sha="0" * 40,
        )


@pytest.mark.parametrize(
    "safe_private_delivery_reference",
    (None, object(), note_path_module._RootOwnedPrivateBindingDeliveryReference(object())),
)
def test_root_owned_private_delivery_reference_unavailable_fails_closed(
    safe_private_delivery_reference: object,
) -> None:
    with pytest.raises(BindingError, match="root-owned private binding delivery is unavailable"):
        note_path_module._issue_root_owned_private_binding_delivery_capability(
            safe_private_delivery_reference=safe_private_delivery_reference,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-root-owned-unavailable-001",
        )


def test_root_owned_private_delivery_capability_issuance_failure_fails_closed() -> None:
    trusted_binding_source = NotePathAdapter._build_private_at8_verified_binding_source(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    reference = note_path_module._register_root_owned_private_binding_delivery_reference(
        trusted_binding_source=trusted_binding_source
    )
    object.__setattr__(trusted_binding_source, "contact_id", "tampered-contact-001")

    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._issue_root_owned_private_binding_delivery_capability(
            safe_private_delivery_reference=reference,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-root-owned-tampered-001",
        )


def test_raw_private_binding_direct_handoff_blocks() -> None:
    binding = _synthetic_binding()
    with pytest.raises(TypeError):
        note_path_module._handoff_private_at8_verified_binding_capability(
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-raw-001",
            workflow_id="meeting_follow_up_v1",
            private_binding=binding,
        )
    assert not hasattr(note_path_module, "_issue_private_at8_handoff_capability")


def test_origin_specific_private_mint_not_available_to_ordinary_caller() -> None:
    assert not hasattr(note_path_module, "_mint_private_at8_verified_binding_handoff_source")
    assert not hasattr(note_path_module, "_mint_bound_contact_trusted_binding_source")
    assert not hasattr(note_path_module, "_mint_at8_shaped_test_trusted_binding_source")
    assert not hasattr(note_path_module, "_mint_trusted_capability")
    assert not hasattr(note_path_module, "_issue_private_at8_handoff_capability")
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")
    assert "_mint_private_at8_verified_binding_handoff_source" not in source
    assert "def _mint_trusted_capability" not in source
    assert "def _issue_private_at8_handoff_capability" not in source


def test_untrusted_structural_binding_source_cannot_handoff() -> None:
    untrusted = _UntrustedStructuralBindingSource().get_trusted_binding_source()
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            trusted_binding_source=untrusted,
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-untrusted-001",
            workflow_id="meeting_follow_up_v1",
        )
    assert not hasattr(note_path_module, "_issue_private_at8_handoff_capability")


def test_known_at8_strings_alone_cannot_mint() -> None:
    with pytest.raises(TypeError):
        note_path_module._handoff_private_at8_verified_binding_capability(
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-strings-001",
            workflow_id="meeting_follow_up_v1",
        )
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-strings-002",
    )
    forged = note_path_module._VerifiedContactBindingCapability(
        workflow_id="meeting_follow_up_v1",
        source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-strings-002",
        trusted_binding_source=note_path_module._TrustedPrivateBindingSource(
            workflow_id="meeting_follow_up_v1",
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
            trusted_origin="private_at8_verified_binding_handoff",
            _trust_marker=object(),
        ),
        _trust_marker=object(),
    )
    adapter._verified_contact_binding_capability = forged
    with pytest.raises(BindingError, match="invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_real_module_marker_not_caller_accessible() -> None:
    assert not hasattr(note_path_module, "_TRUSTED_BINDING_SOURCE_MARKER")
    assert not hasattr(note_path_module, "_VERIFIED_CAPABILITY_TRUST_MARKER")
    assert not hasattr(note_path_module, "_ALLOWED_TRUSTED_BINDING_SOURCES")


def test_caller_with_real_module_marker_cannot_forge() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-stolen-marker-001"
    issued = _issue_synthetic_capability(consumer_workflow_run_id=workflow_run_id)
    forged = note_path_module._VerifiedContactBindingCapability(
        workflow_id=issued.workflow_id,
        source_execution_unit=issued.source_execution_unit,
        source_proof_merge_sha=issued.source_proof_merge_sha,
        location_id=issued.location_id,
        contact_id=issued.contact_id,
        consumer_authorization_identity=issued.consumer_authorization_identity,
        consumer_workflow_run_id=workflow_run_id,
        trusted_binding_source=issued.trusted_binding_source,
        _trust_marker=issued._trust_marker,
    )
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = forged
    with pytest.raises(BindingError, match="invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_private_handoff_rejects_bound_contact_origin() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-reject-bound-001",
    )
    adapter.get_bound_contact()
    bound_source = adapter._verified_contact_binding_capability.trusted_binding_source
    assert bound_source.trusted_origin == "fake_transport_bound_contact_verification"
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            trusted_binding_source=bound_source,
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-reject-bound-001",
            workflow_id="meeting_follow_up_v1",
        )
    assert not hasattr(note_path_module, "_issue_private_at8_handoff_capability")
    assert [method for method, _, _ in transport.calls] == ["GET"]


def test_private_handoff_rejects_synthetic_test_origin() -> None:
    synthetic = NotePathAdapter._build_at8_shaped_test_capability(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-reject-synthetic-001",
    )
    assert synthetic.trusted_binding_source.trusted_origin == "at8_shaped_test_capability"
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._handoff_private_at8_verified_binding_capability(
            trusted_binding_source=synthetic.trusted_binding_source,
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-reject-synthetic-001",
            workflow_id="meeting_follow_up_v1",
        )


def test_direct_bound_contact_capability_mint_blocks() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-bound-get-001",
    )
    assert adapter._verified_contact_binding_capability is None
    assert not hasattr(NotePathAdapter, "_mint_bound_contact_verified_capability")
    assert not hasattr(adapter, "_bound_contact_preflight_marker")
    assert not hasattr(adapter, "_verified_bound_contact_preflight")
    with pytest.raises(BindingError, match="preflight"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []
    with pytest.raises(BindingError, match="successful bound contact preflight is required"):
        note_path_module._issue_bound_contact_capability(adapter=adapter)


def test_caller_copied_preflight_marker_cannot_mint() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-copied-marker-001",
    )
    forged_marker = object()
    adapter._bound_contact_preflight_marker = forged_marker
    adapter._verified_bound_contact_preflight = forged_marker

    with pytest.raises(BindingError, match="preflight"):
        note_path_module._issue_bound_contact_capability(adapter=adapter)

    assert adapter._verified_contact_binding_capability is None
    assert transport.calls == []


def test_get_bound_contact_mismatch_mints_nothing() -> None:
    mismatched_transport = DeterministicFakeTransport(deepcopy(FIXTURE), "contact_id_mismatch")
    mismatched = NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        transport=mismatched_transport,
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-bound-get-002",
    )
    with pytest.raises((BindingError, TransportError)):
        mismatched.get_bound_contact()
    assert mismatched._verified_contact_binding_capability is None
    assert [method for method, _, _ in mismatched_transport.calls] == ["GET"]
    with pytest.raises(BindingError, match="successful bound contact preflight is required"):
        note_path_module._issue_bound_contact_capability(adapter=mismatched)


def test_get_bound_contact_success_mints_bound_capability() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-bound-get-success-001",
    )
    adapter.get_bound_contact()
    capability = adapter._verified_contact_binding_capability
    assert capability is not None
    assert capability.trusted_binding_source.trusted_origin == (
        "fake_transport_bound_contact_verification"
    )
    assert [method for method, _, _ in transport.calls] == ["GET"]


def test_caller_matching_contact_mapping_cannot_mint_bound_trust() -> None:
    expected_contact = {"id": "synthetic-contact-001", "locationId": "synthetic-location-001"}
    with pytest.raises(AttributeError):
        getattr(note_path_module, "_issue_verified_bound_contact_get")(
            verified_contact=expected_contact,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
        )


def test_at8_provenance_mismatch_blocks() -> None:
    with pytest.raises(BindingError, match="source proof is invalid"):
        _issue_synthetic_capability(
            consumer_workflow_run_id="synthetic-workflow-run-handoff-proof-001",
            source_proof_merge_sha="0" * 40,
        )
    with pytest.raises(BindingError, match="source execution unit is invalid"):
        _issue_synthetic_capability(
            consumer_workflow_run_id="synthetic-workflow-run-handoff-unit-001",
            source_execution_unit="NW008_WRONG_EXECUTION_UNIT",
        )


def test_wrong_consumer_authorization_blocks() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-authz-001"
    capability = _issue_synthetic_capability(
        consumer_workflow_run_id=workflow_run_id,
        consumer_authorization_identity="WRONG_AUTHZ_IDENTITY",
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
    capability = _issue_synthetic_capability(
        consumer_workflow_run_id="synthetic-workflow-run-handoff-other-001",
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
        _issue_synthetic_capability(
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
        trusted_binding_source=note_path_module._TrustedPrivateBindingSource(
            workflow_id="meeting_follow_up_v1",
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
            trusted_origin="private_at8_verified_binding_handoff",
            _trust_marker=object(),
        ),
        _trust_marker=object(),
    )
    adapter._verified_contact_binding_capability = forged
    with pytest.raises(BindingError, match="invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_public_trusted_source_injection_blocks() -> None:
    with pytest.raises(TypeError):
        note_path_module._handoff_private_at8_verified_binding_capability(
            source_execution_unit=AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=AT8_SOURCE_PROOF_MERGE_SHA,
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-source-inject-001",
            workflow_id="meeting_follow_up_v1",
            trusted_source="caller-supplied-trusted-source",
        )
    assert not hasattr(note_path_module, "_mint_trusted_capability")


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


def test_private_handoff_source_factory_real_id_use_blocks() -> None:
    with pytest.raises(BindingError, match="must be synthetic"):
        NotePathAdapter._build_private_at8_verified_binding_source(
            location_id="live-location-001",
            contact_id="synthetic-contact-001",
        )
    with pytest.raises(BindingError, match="must be synthetic"):
        NotePathAdapter._build_private_at8_verified_binding_source(
            location_id="synthetic-location-001",
            contact_id="live-contact-001",
        )


def test_capability_trust_registry_is_process_local() -> None:
    capability = _issue_synthetic_capability(
        consumer_workflow_run_id="synthetic-workflow-run-handoff-process-local-001",
    )
    restart_registry = note_path_module._build_internal_trust_issuer()
    restart_require_issued_verified_capability = restart_registry[-1]
    with pytest.raises(BindingError, match="verified-contact binding capability is invalid"):
        restart_require_issued_verified_capability(
            capability,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-process-local-001",
        )


def test_capability_serialization_does_not_restore_authority() -> None:
    workflow_run_id = "synthetic-workflow-run-handoff-serialization-001"
    capability = _issue_synthetic_capability(consumer_workflow_run_id=workflow_run_id)
    restored = pickle.loads(pickle.dumps(capability))
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )
    adapter._verified_contact_binding_capability = restored
    with pytest.raises(BindingError, match="verified-contact binding capability is invalid"):
        adapter.create_meeting_note(_note())
    assert transport.calls == []


def test_process_restart_requires_fresh_trust_issuance() -> None:
    restart_registry = note_path_module._build_internal_trust_issuer()
    restart_issue_synthetic_test_capability = restart_registry[1]
    restart_require_issued_verified_capability = restart_registry[-1]
    fresh_capability = restart_issue_synthetic_test_capability(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-handoff-process-restart-001",
    )
    assert (
        restart_require_issued_verified_capability(
            fresh_capability,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-handoff-process-restart-001",
        )
        is fresh_capability
    )


def test_private_binding_is_data_not_authority() -> None:
    binding = _synthetic_binding()
    assert not hasattr(binding, "_trust_marker")
    assert not hasattr(binding, "trusted_binding_source")
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
    assert "_issue_private_at8_handoff_capability" not in dir(NotePathAdapter)


def test_caller_matching_mapping_cannot_self_issue_verified_get() -> None:
    """The former matching-mapping -> registered-GET -> capability path is absent."""
    matching_mapping = {"id": "synthetic-contact-001", "locationId": "synthetic-location-001"}
    with pytest.raises(AttributeError):
        getattr(note_path_module, "_issue_verified_bound_contact_get")(
            verified_contact=matching_mapping,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
        )


def test_issued_synthetic_capability_in_place_retarget_blocks() -> None:
    capability = _issue_synthetic_capability(
        consumer_workflow_run_id="synthetic-workflow-run-synthetic-retarget-001",
    )
    object.__setattr__(capability, "location_id", "synthetic-location-002")
    with pytest.raises(BindingError, match="capability is invalid"):
        note_path_module._require_issued_verified_capability(
            capability,
            location_id="synthetic-location-002",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-synthetic-retarget-001",
        )


def test_issued_synthetic_source_in_place_retarget_blocks() -> None:
    capability = _issue_synthetic_capability(
        consumer_workflow_run_id="synthetic-workflow-run-source-retarget-001",
    )
    object.__setattr__(
        capability.trusted_binding_source, "location_id", "synthetic-location-002"
    )
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._require_issued_verified_capability(
            capability,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-source-retarget-001",
        )


def test_issued_bound_contact_capability_in_place_retarget_blocks() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-bound-retarget-001",
    )
    adapter.get_bound_contact()
    capability = adapter._require_trusted_verified_capability()
    object.__setattr__(capability, "location_id", "synthetic-location-002")
    with pytest.raises(BindingError, match="capability is invalid"):
        note_path_module._require_issued_verified_capability(
            capability,
            location_id="synthetic-location-002",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-bound-retarget-001",
        )
    assert [method for method, _, _ in transport.calls] == ["GET"]


def test_issued_bound_contact_source_in_place_retarget_blocks() -> None:
    adapter, transport = _adapter(
        consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-bound-source-retarget-001",
    )
    adapter.get_bound_contact()
    capability = adapter._require_trusted_verified_capability()
    object.__setattr__(
        capability.trusted_binding_source, "contact_id", "synthetic-contact-002"
    )
    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path_module._require_issued_verified_capability(
            capability,
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            consumer_authorization_identity=DEFAULT_CONSUMER_AUTHORIZATION_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-bound-source-retarget-001",
        )
    assert [method for method, _, _ in transport.calls] == ["GET"]


def test_no_provider_get_and_zero_network_effects() -> None:
    assert note_path_module.NETWORK_CALLS == 0
    assert note_path_module.HIGHLEVEL_NETWORK_CALLS == 0
    assert note_path_module.EXTERNAL_EFFECTS == 0
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")
    assert "At1ExecutionStore" in source
    assert "secretmanager" not in source.lower()
    assert "Secret Manager" not in source
    assert "at1_live_transport_adapter" not in source
