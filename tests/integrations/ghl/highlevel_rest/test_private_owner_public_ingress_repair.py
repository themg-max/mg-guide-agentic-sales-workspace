from __future__ import annotations

import copy
import pickle
from types import ModuleType

import pytest

import integrations.ghl.highlevel_rest.live_note_runtime as runtime
import integrations.ghl.highlevel_rest.note_path as note_path
from integrations.ghl.highlevel_rest.note_path import BindingError, NotePathAdapter


# The exact consumer authorization/run binding is installed at owner
# provisioning time by the private control plane. These offline values model
# the governed post-repair binding; no pre-repair (PR223) identity is required.
AUTHORIZATION_ID = "nw008-at8w30-r3-ingress-repair-test-consumer-authorization-001"
WORKFLOW_RUN_ID = "nw008-at8w30-r3-ingress-repair-test-consumer-run-001"
DESIGNATION_ID = note_path._DESIGNATED_PRIVATE_OWNER_ID


def _provision_owner(
    owner: ModuleType,
    *,
    authorization_id: str = AUTHORIZATION_ID,
    workflow_run_id: str = WORKFLOW_RUN_ID,
) -> object:
    handoff_source = note_path._issue_private_at8_handoff_source_for_synthetic_tests(
        location_id="synthetic-owner-provisioning-location-001",
        contact_id="synthetic-owner-provisioning-contact-001",
    )
    return note_path._provision_designated_private_owner_resolver(
        trusted_binding_source=handoff_source,
        private_owner_resolver=owner,
        consumer_authorization_identity=authorization_id,
        consumer_workflow_run_id=workflow_run_id,
    )


def _designated_private_owner(
    *,
    location_id: str = "approved-live-location-placeholder",
    contact_id: str = "approved-live-contact-placeholder",
) -> tuple[ModuleType, object, object, dict[str, str]]:
    owner = ModuleType("offline_designated_private_owner")
    state = {"reference": "AVAILABLE"}
    registry: set[int] = set()

    class OpaqueSafePrivateBindingReference:
        __slots__ = ("__weakref__",)

        def __reduce__(self):
            raise BindingError("private binding reference is not serializable")

        def __copy__(self):
            raise BindingError("private binding reference is not copyable")

        def __deepcopy__(self, memo: object):
            raise BindingError("private binding reference is not copyable")

    class PrivateBindingMaterial:
        __slots__ = ("designation_id", "provider_ids")

        def __init__(self) -> None:
            self.designation_id = DESIGNATION_ID
            self.provider_ids = (location_id, contact_id)

    reference = OpaqueSafePrivateBindingReference()
    registry.add(id(reference))

    def release_to_public_consumer(submitted: object) -> object:
        if (
            not isinstance(submitted, OpaqueSafePrivateBindingReference)
            or id(submitted) not in registry
        ):
            raise BindingError("private binding reference is not recognized")
        if state["reference"] != "AVAILABLE":
            raise BindingError("private binding reference is already consumed")
        state["reference"] = "CONSUMED"
        return PrivateBindingMaterial()

    owner.DESIGNATION_ID = DESIGNATION_ID
    owner.OpaqueSafePrivateBindingReference = OpaqueSafePrivateBindingReference
    owner.PrivateBindingMaterial = PrivateBindingMaterial
    owner.release_to_public_consumer = release_to_public_consumer
    anchor = _provision_owner(owner)
    return owner, anchor, reference, state


def _forged_private_owner() -> tuple[ModuleType, object, dict[str, int]]:
    """A caller-created module reproducing the entire public resolver shape."""
    forged = ModuleType("offline_forged_private_owner")
    state = {"release_calls": 0}

    class OpaqueSafePrivateBindingReference:
        __slots__ = ("__weakref__",)

    class PrivateBindingMaterial:
        __slots__ = ("designation_id", "provider_ids")

        def __init__(self) -> None:
            self.designation_id = DESIGNATION_ID
            self.provider_ids = (
                "forged-live-location-placeholder",
                "forged-live-contact-placeholder",
            )

    def release_to_public_consumer(submitted: object) -> object:
        state["release_calls"] += 1
        return PrivateBindingMaterial()

    forged.DESIGNATION_ID = DESIGNATION_ID
    forged.OpaqueSafePrivateBindingReference = OpaqueSafePrivateBindingReference
    forged.PrivateBindingMaterial = PrivateBindingMaterial
    forged.release_to_public_consumer = release_to_public_consumer
    return forged, OpaqueSafePrivateBindingReference(), state


def _consume(
    *,
    owner: object,
    anchor: object,
    reference: object,
    authorization_id: str = AUTHORIZATION_ID,
    workflow_run_id: str = WORKFLOW_RUN_ID,
):
    return runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        private_owner_resolver=owner,
        private_owner_anchor=anchor,
        consumer_authorization_identity=authorization_id,
        consumer_workflow_run_id=workflow_run_id,
    )


def test_legacy_synthetic_lease_path_remains_available() -> None:
    reference = NotePathAdapter._build_private_at8_binding_lease_for_tests(
        location_id="synthetic-location-legacy-001",
        contact_id="synthetic-contact-legacy-001",
        consumer_authorization_identity="synthetic-legacy-consumer-001",
        consumer_workflow_run_id="synthetic-legacy-run-001",
    )

    capability = runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        consumer_authorization_identity="synthetic-legacy-consumer-001",
        consumer_workflow_run_id="synthetic-legacy-run-001",
    )

    assert capability.contact_id == "synthetic-contact-legacy-001"


def test_raw_live_ids_alone_reject() -> None:
    owner, anchor, _, _ = _designated_private_owner()

    for raw_input in (
        "approved-live-contact-placeholder",
        ("approved-live-location-placeholder", "approved-live-contact-placeholder"),
        {
            "location_id": "approved-live-location-placeholder",
            "contact_id": "approved-live-contact-placeholder",
        },
    ):
        with pytest.raises(BindingError, match="reference is invalid"):
            _consume(owner=owner, anchor=anchor, reference=raw_input)


def test_forged_opaque_reference_rejects() -> None:
    owner, anchor, _, state = _designated_private_owner()
    forged_reference = owner.OpaqueSafePrivateBindingReference()

    with pytest.raises(BindingError, match="not recognized"):
        _consume(owner=owner, anchor=anchor, reference=forged_reference)

    assert state["reference"] == "AVAILABLE"


def test_serialized_or_reconstructed_reference_rejects() -> None:
    owner, anchor, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="not serializable"):
        pickle.dumps(reference)
    with pytest.raises(BindingError, match="not copyable"):
        copy.copy(reference)
    reconstructed_reference = owner.OpaqueSafePrivateBindingReference()
    with pytest.raises(BindingError, match="not recognized"):
        _consume(owner=owner, anchor=anchor, reference=reconstructed_reference)

    assert state["reference"] == "AVAILABLE"


def test_wrong_owner_or_designation_rejects() -> None:
    owner, anchor, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="resolver is invalid"):
        _consume(
            owner=ModuleType("offline_unrelated_private_owner"),
            anchor=anchor,
            reference=reference,
        )

    assert state["reference"] == "AVAILABLE"

    owner.DESIGNATION_ID = "NW008_UNRELATED_PRIVATE_OWNER_001"

    with pytest.raises(BindingError, match="resolver is invalid"):
        _consume(owner=owner, anchor=anchor, reference=reference)

    assert state["reference"] == "AVAILABLE"


def test_anchor_transplant_to_foreign_resolver_rejects() -> None:
    owner, anchor, reference, state = _designated_private_owner()
    other_owner, _, _, _ = _designated_private_owner()

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=other_owner, anchor=anchor, reference=reference)

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=owner, anchor=object(), reference=reference)

    assert state["reference"] == "AVAILABLE"


def test_owner_anchor_provisioning_requires_private_authority() -> None:
    owner = ModuleType("offline_unprovisioned_private_owner")
    owner.DESIGNATION_ID = DESIGNATION_ID

    with pytest.raises(BindingError, match="trusted binding source is invalid"):
        note_path._provision_designated_private_owner_resolver(
            trusted_binding_source=object(),
            private_owner_resolver=owner,
            consumer_authorization_identity=AUTHORIZATION_ID,
            consumer_workflow_run_id=WORKFLOW_RUN_ID,
        )


def test_wrong_authorization_identity_rejects_before_private_consumption() -> None:
    owner, anchor, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="authorization binding is invalid"):
        _consume(
            owner=owner,
            anchor=anchor,
            reference=reference,
            authorization_id="NW008_UNRELATED_AUTHORIZATION_001",
        )

    assert state["reference"] == "AVAILABLE"


def test_wrong_workflow_run_identity_rejects_before_private_consumption() -> None:
    owner, anchor, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="workflow run binding is invalid"):
        _consume(
            owner=owner,
            anchor=anchor,
            reference=reference,
            workflow_run_id="nw008-unrelated-run-001",
        )

    assert state["reference"] == "AVAILABLE"


def test_valid_private_owner_one_shot_reference_passes() -> None:
    owner, anchor, reference, state = _designated_private_owner()

    capability = _consume(owner=owner, anchor=anchor, reference=reference)

    assert capability.consumer_authorization_identity == AUTHORIZATION_ID
    assert capability.consumer_workflow_run_id == WORKFLOW_RUN_ID
    assert state["reference"] == "CONSUMED"


def test_private_owner_reference_replay_rejects() -> None:
    owner, anchor, reference, state = _designated_private_owner()
    _consume(owner=owner, anchor=anchor, reference=reference)

    with pytest.raises(BindingError, match="already consumed"):
        _consume(owner=owner, anchor=anchor, reference=reference)

    assert state["reference"] == "CONSUMED"


def test_non_synthetic_verified_private_target_traverses_ingress_without_network() -> None:
    owner, anchor, reference, state = _designated_private_owner(
        location_id="approved-live-location-placeholder",
        contact_id="approved-live-contact-placeholder",
    )

    capability = _consume(owner=owner, anchor=anchor, reference=reference)

    assert capability.location_id == "approved-live-location-placeholder"
    assert capability.contact_id == "approved-live-contact-placeholder"
    assert not capability.location_id.startswith("synthetic-")
    assert not capability.contact_id.startswith("synthetic-")
    assert state["reference"] == "CONSUMED"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0


def test_forged_owner_with_correct_designation_rejects() -> None:
    """T11: full resolver-shape forgery fails closed before any issuance."""
    owner, anchor, reference, state = _designated_private_owner()
    forged, forged_reference, forged_state = _forged_private_owner()

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=forged, anchor=object(), reference=forged_reference)

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=forged, anchor=anchor, reference=forged_reference)

    assert forged_state["release_calls"] == 0
    assert state["reference"] == "AVAILABLE"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0


def test_valid_owner_remains_available_after_forged_owner_rejection() -> None:
    """T12: forged-owner probes never spend genuine private authority."""
    owner, anchor, reference, state = _designated_private_owner()
    forged, forged_reference, forged_state = _forged_private_owner()

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=forged, anchor=anchor, reference=forged_reference)

    assert forged_state["release_calls"] == 0
    assert state["reference"] == "AVAILABLE"

    capability = _consume(owner=owner, anchor=anchor, reference=reference)

    assert capability.consumer_authorization_identity == AUTHORIZATION_ID
    assert capability.consumer_workflow_run_id == WORKFLOW_RUN_ID
    assert state["reference"] == "CONSUMED"
