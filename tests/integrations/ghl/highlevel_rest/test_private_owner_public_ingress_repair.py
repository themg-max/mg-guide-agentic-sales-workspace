from __future__ import annotations

import copy
import pickle
from types import ModuleType

import pytest

import integrations.ghl.highlevel_rest.live_note_runtime as runtime
import integrations.ghl.highlevel_rest.note_path as note_path
from integrations.ghl.highlevel_rest.note_path import BindingError, NotePathAdapter


AUTHORIZATION_ID = note_path._DESIGNATED_PRIVATE_OWNER_CONSUMER_AUTHORIZATION_ID
WORKFLOW_RUN_ID = note_path._DESIGNATED_PRIVATE_OWNER_CONSUMER_WORKFLOW_RUN_ID
DESIGNATION_ID = note_path._DESIGNATED_PRIVATE_OWNER_ID


def _designated_private_owner(
    *,
    location_id: str = "approved-live-location-placeholder",
    contact_id: str = "approved-live-contact-placeholder",
) -> tuple[ModuleType, object, dict[str, str]]:
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
    return owner, reference, state


def _consume(
    *,
    owner: object,
    reference: object,
    authorization_id: str = AUTHORIZATION_ID,
    workflow_run_id: str = WORKFLOW_RUN_ID,
):
    return runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        private_owner_resolver=owner,
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
    owner, _, _ = _designated_private_owner()

    for raw_input in (
        "approved-live-contact-placeholder",
        ("approved-live-location-placeholder", "approved-live-contact-placeholder"),
        {
            "location_id": "approved-live-location-placeholder",
            "contact_id": "approved-live-contact-placeholder",
        },
    ):
        with pytest.raises(BindingError, match="reference is invalid"):
            _consume(owner=owner, reference=raw_input)


def test_forged_opaque_reference_rejects() -> None:
    owner, _, state = _designated_private_owner()
    forged_reference = owner.OpaqueSafePrivateBindingReference()

    with pytest.raises(BindingError, match="not recognized"):
        _consume(owner=owner, reference=forged_reference)

    assert state["reference"] == "AVAILABLE"


def test_serialized_or_reconstructed_reference_rejects() -> None:
    owner, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="not serializable"):
        pickle.dumps(reference)
    with pytest.raises(BindingError, match="not copyable"):
        copy.copy(reference)
    reconstructed_reference = owner.OpaqueSafePrivateBindingReference()
    with pytest.raises(BindingError, match="not recognized"):
        _consume(owner=owner, reference=reconstructed_reference)

    assert state["reference"] == "AVAILABLE"


def test_wrong_owner_or_designation_rejects() -> None:
    owner, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="resolver is invalid"):
        _consume(owner=ModuleType("offline_unrelated_private_owner"), reference=reference)

    assert state["reference"] == "AVAILABLE"

    owner.DESIGNATION_ID = "NW008_UNRELATED_PRIVATE_OWNER_001"

    with pytest.raises(BindingError, match="resolver is invalid"):
        _consume(owner=owner, reference=reference)

    assert state["reference"] == "AVAILABLE"


def test_wrong_authorization_identity_rejects_before_private_consumption() -> None:
    owner, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="authorization binding is invalid"):
        _consume(
            owner=owner,
            reference=reference,
            authorization_id="NW008_UNRELATED_AUTHORIZATION_001",
        )

    assert state["reference"] == "AVAILABLE"


def test_wrong_workflow_run_identity_rejects_before_private_consumption() -> None:
    owner, reference, state = _designated_private_owner()

    with pytest.raises(BindingError, match="workflow run binding is invalid"):
        _consume(
            owner=owner,
            reference=reference,
            workflow_run_id="nw008-unrelated-run-001",
        )

    assert state["reference"] == "AVAILABLE"


def test_valid_private_owner_one_shot_reference_passes() -> None:
    owner, reference, state = _designated_private_owner()

    capability = _consume(owner=owner, reference=reference)

    assert capability.consumer_authorization_identity == AUTHORIZATION_ID
    assert capability.consumer_workflow_run_id == WORKFLOW_RUN_ID
    assert state["reference"] == "CONSUMED"


def test_private_owner_reference_replay_rejects() -> None:
    owner, reference, state = _designated_private_owner()
    _consume(owner=owner, reference=reference)

    with pytest.raises(BindingError, match="already consumed"):
        _consume(owner=owner, reference=reference)

    assert state["reference"] == "CONSUMED"


def test_non_synthetic_verified_private_target_traverses_ingress_without_network() -> None:
    owner, reference, state = _designated_private_owner(
        location_id="approved-live-location-placeholder",
        contact_id="approved-live-contact-placeholder",
    )

    capability = _consume(owner=owner, reference=reference)

    assert capability.location_id == "approved-live-location-placeholder"
    assert capability.contact_id == "approved-live-contact-placeholder"
    assert not capability.location_id.startswith("synthetic-")
    assert not capability.contact_id.startswith("synthetic-")
    assert state["reference"] == "CONSUMED"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0
