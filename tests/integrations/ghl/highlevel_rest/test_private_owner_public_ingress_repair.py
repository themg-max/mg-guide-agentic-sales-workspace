from __future__ import annotations

import copy
import pickle
from types import ModuleType

import pytest

import integrations.ghl.highlevel_rest.live_note_runtime as runtime
import integrations.ghl.highlevel_rest.note_path as note_path
from integrations.ghl.highlevel_rest.note_path import BindingError, NotePathAdapter

from _simulated_private_control_plane import (
    install_as_root_designated_private_origin,
    provision_simulated_private_owner,
)


# The exact consumer authorization/run binding is installed at owner
# provisioning time by the private control plane. These offline values model
# the governed post-repair binding; no pre-repair (PR223) identity is required.
AUTHORIZATION_ID = "nw008-at8w30-r3-ingress-repair-test-consumer-authorization-001"
WORKFLOW_RUN_ID = "nw008-at8w30-r3-ingress-repair-test-consumer-run-001"
DESIGNATION_ID = note_path._DESIGNATED_PRIVATE_OWNER_ID


@pytest.fixture(autouse=True)
def _root_designates_private_origin(monkeypatch):
    """The PROCESS ROOT designates the private-origin module, never a caller.

    Without this root-owned designation note_path trusts no origin at all, so
    every anchor is refused. Tests make the designation explicit rather than
    letting production code fall back to a caller-supplied origin.
    """
    install_as_root_designated_private_origin(monkeypatch)


def _designated_private_owner(
    *,
    location_id: str = "approved-live-location-placeholder",
    contact_id: str = "approved-live-contact-placeholder",
) -> tuple[ModuleType, object, object, dict[str, str]]:
    # The owner/anchor pair is modelled test-side as an artifact the private
    # control plane already provisioned. note_path originates nothing: it only
    # verifies an artifact from the root-designated private-origin module.
    owner, anchor = provision_simulated_private_owner(
        authorization_identity=AUTHORIZATION_ID,
        workflow_run_id=WORKFLOW_RUN_ID,
    )
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

    owner.OpaqueSafePrivateBindingReference = OpaqueSafePrivateBindingReference
    owner.PrivateBindingMaterial = PrivateBindingMaterial
    owner.release_to_public_consumer = release_to_public_consumer
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
    other_owner, other_anchor, _, _ = _designated_private_owner()

    # The transplant must be between genuinely distinct provisioned owners,
    # otherwise this test would be vacuous.
    assert other_owner is not owner
    assert other_anchor is not anchor

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=other_owner, anchor=anchor, reference=reference)

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=owner, anchor=object(), reference=reference)

    assert state["reference"] == "AVAILABLE"


def test_owner_anchor_provisioning_requires_private_authority() -> None:
    """T08: an owner the private plane never provisioned can never be used.

    note_path contains no provisioner at all, so there is nothing to call. The
    surviving guarantee is the one that matters: a caller-created owner has no
    private-origin anchor and is refused.
    """
    owner = ModuleType("offline_unprovisioned_private_owner")
    owner.DESIGNATION_ID = DESIGNATION_ID

    reference = object()
    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=owner, anchor=object(), reference=reference)

    # An anchor provisioned for a different resolver cannot be transplanted
    # onto this caller-created owner.
    for index in range(4):
        other_owner, other_anchor = provision_simulated_private_owner(
            authorization_identity=AUTHORIZATION_ID,
            workflow_run_id=WORKFLOW_RUN_ID,
            module_name=f"offline_other_private_owner_{index:03d}",
        )
        assert other_owner is not owner
        with pytest.raises(BindingError, match="authenticity anchor is invalid"):
            _consume(owner=owner, anchor=other_anchor, reference=reference)


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


def test_public_synthetic_handoff_source_cannot_provision_designated_owner() -> None:
    """T13: public synthetic AT8 handoff cannot provision a designated owner.

    A synthetic AT8 handoff source is a genuine, registry-recognized object,
    but it is a different origin than owner provisioning. It cannot be turned
    into an owner anchor, and there is no longer any reachable provisioner it
    could even be presented to.
    """
    _genuine_owner, _genuine_anchor, _genuine_reference, genuine_state = (
        _designated_private_owner()
    )
    forged, forged_reference, forged_state = _forged_private_owner()
    synthetic_source = note_path._issue_private_at8_handoff_source_for_synthetic_tests(
        location_id="synthetic-owner-provisioning-location-001",
        contact_id="synthetic-owner-provisioning-contact-001",
    )

    # The synthetic source is a real registered object, yet it grants nothing
    # on the owner-provisioning origin: it cannot be used as an anchor.
    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=forged, anchor=synthetic_source, reference=forged_reference)

    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=forged, anchor=object(), reference=forged_reference)

    assert forged_state["release_calls"] == 0
    assert genuine_state["reference"] == "AVAILABLE"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0


def test_ordinary_importer_cannot_self_issue_or_provision_owner() -> None:
    """T14: an ordinary importer cannot self-issue authority or self-provision.

    This test acts as a hostile ordinary consumer of note_path with full
    knowledge of every underscore name. It sweeps every reachable callable,
    invokes every zero-argument surface, walks closures, and proves that
    nothing yields an anchor the production consumer will accept for a
    caller-controlled resolver.

    Underscore naming and ``__all__`` are explicitly NOT treated as
    boundaries. The boundary is structural: note_path holds no anchor
    registry and no provisioning callable, so there is nothing to reach.
    """
    import inspect
    import sys

    import integrations.ghl.highlevel_rest.live_note_runtime as runtime
    import _simulated_private_control_plane as simulated_plane

    # 1. The production composition root never references an origin surface.
    runtime_source = inspect.getsource(runtime)
    assert "issue_private_owner_provisioning_authority" not in runtime_source
    assert "provision_designated_private_owner_resolver" not in runtime_source

    # 2. No origin-shaped callable or type survives on the module under ANY
    #    name, including every previously exported name.
    for removed in (
        "_issue_private_owner_provisioning_authority",
        "_issue_private_owner_provisioning_authority_for_tests",
        "_provision_designated_private_owner_resolver",
        "_provision_designated_private_owner_resolver_for_tests",
        "_take_offline_provisioned_private_owner",
        "_PrivateOwnerProvisioningAuthority",
        "_PrivateOwnerAuthenticityAnchor",
    ):
        assert not hasattr(note_path, removed), removed

    # 3. Sweep every reachable name. Nothing owner-issuing/provisioning-shaped
    #    may remain, regardless of underscore prefix or callable/type kind.
    for name in dir(note_path):
        lowered = name.lower()
        if "owner" in lowered and (
            "issue" in lowered or "provision" in lowered or "mint" in lowered
        ):
            raise AssertionError(
                f"note_path exposes an owner origin surface: {name}"
            )

    # 4. Invoke every reachable zero-argument callable. None may return
    #    anything the production consumer will accept as an anchor.
    caller_owner = ModuleType("t14_caller_controlled_resolver")
    caller_owner.DESIGNATION_ID = DESIGNATION_ID
    harvested: list[object] = []
    for name in dir(note_path):
        value = getattr(note_path, name, None)
        if not callable(value) or isinstance(value, type):
            continue
        try:
            signature = inspect.signature(value)
        except (TypeError, ValueError):
            continue
        if any(
            parameter.default is inspect.Parameter.empty
            and parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
            for parameter in signature.parameters.values()
        ):
            continue
        try:
            harvested.append(value())
        except Exception:
            continue

    # 5. Direct construction of any reachable class confers nothing either.
    for name in dir(note_path):
        value = getattr(note_path, name, None)
        if isinstance(value, type):
            try:
                harvested.append(value())
            except Exception:
                continue

    # 6. Walk the closure cells of every exported function, harvesting every
    #    reachable object as a candidate forged anchor.
    for name in dir(note_path):
        value = getattr(note_path, name, None)
        closure = getattr(value, "__closure__", None) or ()
        for cell in closure:
            try:
                harvested.append(cell.cell_contents)
            except ValueError:
                continue

    # 7. Nothing harvested may be accepted as an anchor for a resolver the
    #    caller controls.
    reference = object()
    for candidate in harvested:
        with pytest.raises(BindingError):
            _consume(owner=caller_owner, anchor=candidate, reference=reference)

    # 8. Self-certifying anchors are refused. A caller can always write an
    #    object -- or a whole module -- that *claims* private origin, so none
    #    of these may be accepted. Each of these was a real breach during
    #    development, so they are regression-guarded here.
    forged, forged_reference, forged_state = _forged_private_owner()

    class SelfAttestingAnchor:
        """Answers an attestation challenge for a caller-controlled resolver."""

        def attest_private_origin_provisioning(self, challenge: object):
            return (DESIGNATION_ID, forged, AUTHORIZATION_ID, WORKFLOW_RUN_ID)

    class DuckTypedAnchor:
        designation_id = DESIGNATION_ID
        provisioned_resolver = forged
        consumer_authorization_identity = AUTHORIZATION_ID
        consumer_workflow_run_id = WORKFLOW_RUN_ID

    # A caller-authored module asserting it is the private control plane,
    # including an unconstructable artifact type and a self-recognising
    # membership check.
    caller_plane = ModuleType("t14_caller_authored_private_plane")
    caller_token = object()

    class CallerPlaneAnchor:
        designation_id = DESIGNATION_ID
        provisioned_resolver = forged
        consumer_authorization_identity = AUTHORIZATION_ID
        consumer_workflow_run_id = WORKFLOW_RUN_ID

        def __init__(self, token: object = None) -> None:
            if token is not caller_token:
                raise RuntimeError("unconstructable")

    CallerPlaneAnchor.__module__ = caller_plane.__name__
    caller_plane.ProvisionedPrivateOwnerResolver = CallerPlaneAnchor
    caller_plane.is_genuinely_provisioned = lambda artifact: True
    sys.modules[caller_plane.__name__] = caller_plane
    try:
        # An instance of the GENUINE artifact type, reconstructed through
        # __new__ to bypass the private construction token.
        token_bypassed = simulated_plane.ProvisionedPrivateOwnerResolver.__new__(
            simulated_plane.ProvisionedPrivateOwnerResolver
        )
        for attribute, value in (
            ("designation_id", DESIGNATION_ID),
            ("provisioned_resolver", forged),
            ("consumer_authorization_identity", AUTHORIZATION_ID),
            ("consumer_workflow_run_id", WORKFLOW_RUN_ID),
        ):
            object.__setattr__(token_bypassed, attribute, value)

        for label, candidate in (
            ("self-attesting", SelfAttestingAnchor()),
            ("duck-typed", DuckTypedAnchor()),
            ("caller-authored private plane", CallerPlaneAnchor(caller_token)),
            ("__new__ token bypass", token_bypassed),
        ):
            with pytest.raises(BindingError):
                _consume(
                    owner=forged,
                    anchor=candidate,
                    reference=forged_reference,
                )
            assert forged_state["release_calls"] == 0, label
    finally:
        sys.modules.pop(caller_plane.__name__, None)

    # 9. The legitimate private-origin consumer handoff still works.
    owner, anchor, genuine_reference, state = _designated_private_owner()
    capability = _consume(owner=owner, anchor=anchor, reference=genuine_reference)
    assert capability.contact_id == "approved-live-contact-placeholder"
    assert state["reference"] == "CONSUMED"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0


def test_public_module_performs_no_authority_origin_at_import() -> None:
    """T15: importing note_path performs no authority origin at all.

    Proves the public module is a verifier/consumer only: importing it creates
    no owner-provisioning authority and no private-owner authenticity anchor,
    and production ``src/`` contains no bootstrap that could register either.
    """
    import gc
    import importlib
    import inspect
    import pathlib
    import sys

    import integrations.ghl.highlevel_rest.live_note_runtime as runtime

    # 1/2. A fresh import of note_path creates no authority and no anchor.
    #      Re-import the module from source and diff the live object graph for
    #      anything origin-shaped, rather than trusting names.
    def _origin_shaped_live_objects() -> list[str]:
        found = []
        for obj in gc.get_objects():
            try:
                type_name = type(obj).__name__
            except Exception:
                continue
            if type_name in (
                "_PrivateOwnerProvisioningAuthority",
                "_PrivateOwnerAuthenticityAnchor",
            ):
                found.append(type_name)
        return found

    module_name = "integrations.ghl.highlevel_rest.note_path"
    saved = sys.modules.pop(module_name)
    try:
        reimported = importlib.import_module(module_name)
        assert _origin_shaped_live_objects() == []
        # The reimported module exposes no owner origin surface either.
        for name in dir(reimported):
            lowered = name.lower()
            assert not (
                "owner" in lowered
                and ("issue" in lowered or "provision" in lowered or "mint" in lowered)
            ), name
    finally:
        sys.modules[module_name] = saved

    # 3. Production src/ contains no bootstrap that registers either artifact.
    src_root = pathlib.Path(inspect.getsourcefile(note_path)).resolve().parents[3]
    assert src_root.name == "src", src_root
    banned = (
        "_PrivateOwnerProvisioningAuthority",
        "_PrivateOwnerAuthenticityAnchor",
        "owner_provisioning_authorities",
        "designated_owner_anchors",
        "_bootstrap_offline_provisioned_owner_pool",
        "origin_latch",
    )
    for source_file in src_root.rglob("*.py"):
        text = source_file.read_text()
        for token in banned:
            assert token not in text, f"{source_file}: {token}"

    # 4. No production callable can bind a caller-controlled resolver. The
    #    only anchor-accepting production entry point refuses one.
    caller_owner = ModuleType("t15_caller_controlled_resolver")
    caller_owner.DESIGNATION_ID = DESIGNATION_ID
    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=caller_owner, anchor=object(), reference=object())

    # 5. Legitimate root-owned/private-origin consumer handoff still passes.
    owner, anchor, reference, state = _designated_private_owner()
    capability = runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        private_owner_resolver=owner,
        private_owner_anchor=anchor,
        consumer_authorization_identity=AUTHORIZATION_ID,
        consumer_workflow_run_id=WORKFLOW_RUN_ID,
    )
    assert capability.contact_id == "approved-live-contact-placeholder"
    assert state["reference"] == "CONSUMED"
    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0
