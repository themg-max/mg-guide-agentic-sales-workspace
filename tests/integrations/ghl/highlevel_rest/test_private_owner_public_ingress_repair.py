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


def _designated_private_owner(
    *,
    location_id: str = "approved-live-location-placeholder",
    contact_id: str = "approved-live-contact-placeholder",
) -> tuple[ModuleType, object, object, dict[str, str]]:
    # The owner/anchor pair is taken already provisioned from the offline pool
    # that note_path built during import. The test never provisions an owner:
    # the origin latch is spent before any test code can run.
    owner, anchor = note_path._take_offline_provisioned_private_owner()
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

    The provisioning origin is spent at import, so there is no reachable
    provisioner to call at all. The surviving guarantee is the one that
    matters: a caller-created owner has no anchor and is refused.
    """
    owner = ModuleType("offline_unprovisioned_private_owner")
    owner.DESIGNATION_ID = DESIGNATION_ID

    reference = object()
    with pytest.raises(BindingError, match="authenticity anchor is invalid"):
        _consume(owner=owner, anchor=object(), reference=reference)

    # The only reachable owner accessor hands back seam-created resolvers; it
    # can never bind an anchor to this caller-created owner.
    for _ in range(4):
        pooled_owner, pooled_anchor = (
            note_path._take_offline_provisioned_private_owner()
        )
        assert pooled_owner is not owner
        with pytest.raises(BindingError, match="authenticity anchor is invalid"):
            _consume(owner=owner, anchor=pooled_anchor, reference=reference)


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
    knowledge of every underscore name. It sweeps every reachable callable on
    the module, invokes each issuer/provisioning-shaped surface with every
    argument shape it can construct, and proves that none of them yields a
    registry-recognized owner-provisioning authority or an authenticity
    anchor bound to a caller-controlled resolver.

    Underscore naming and `__all__` are explicitly NOT treated as boundaries.
    The real boundary is the one-shot import-time origin latch: the
    originating closures are never returned from the trust-issuer factory, so
    after import there is no name -- public or private -- that reaches them.
    """
    import gc
    import inspect
    import weakref

    import integrations.ghl.highlevel_rest.live_note_runtime as runtime

    # 1. The production composition root never references an origin surface.
    runtime_source = inspect.getsource(runtime)
    assert "issue_private_owner_provisioning_authority" not in runtime_source
    assert "provision_designated_private_owner_resolver" not in runtime_source

    # 2. No origin-shaped callable survives on the module under ANY name,
    #    including the previously exported underscore/_for_tests names.
    assert not hasattr(note_path, "_issue_private_owner_provisioning_authority")
    assert not hasattr(
        note_path, "_issue_private_owner_provisioning_authority_for_tests"
    )
    assert not hasattr(note_path, "_provision_designated_private_owner_resolver")
    assert not hasattr(
        note_path, "_provision_designated_private_owner_resolver_for_tests"
    )

    # 3. Sweep every reachable callable. Nothing named like an owner issuer or
    #    provisioner may remain, regardless of underscore prefix.
    reachable = {
        name: getattr(note_path, name, None) for name in dir(note_path)
    }
    for name, value in reachable.items():
        # Classes are type declarations, not origin callables; step 5 proves
        # that constructing them directly confers nothing.
        if not callable(value) or isinstance(value, type):
            continue
        lowered = name.lower()
        if "owner" in lowered and (
            "issue" in lowered or "provision" in lowered or "mint" in lowered
        ):
            # The only permitted owner-shaped accessor is the consumer-side
            # handout of artifacts provisioned before any caller ran.
            assert name == "_take_offline_provisioned_private_owner", (
                f"note_path exposes an owner origin callable: {name}"
            )

    # 4. Every reachable zero-argument callable is invoked; none of them may
    #    return a registry-recognized owner-provisioning authority.
    authority_type = note_path._PrivateOwnerProvisioningAuthority
    anchor_type = note_path._PrivateOwnerAuthenticityAnchor
    for name, value in reachable.items():
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
            produced = value()
        except Exception:
            continue
        assert not isinstance(produced, authority_type), (
            f"note_path.{name}() self-issued an owner-provisioning authority"
        )
        assert not isinstance(produced, anchor_type), (
            f"note_path.{name}() self-issued an owner authenticity anchor"
        )

    # 5. A caller-controlled resolver can never be provisioned. Even a fully
    #    shape-reproducing forged owner, and even genuine registered objects
    #    borrowed from a different origin, are refused as anchors.
    forged, forged_reference, forged_state = _forged_private_owner()
    synthetic_source = note_path._issue_private_at8_handoff_source_for_synthetic_tests(
        location_id="synthetic-owner-provisioning-authority-location-001",
        contact_id="synthetic-owner-provisioning-authority-contact-001",
    )
    genuine_owner, genuine_anchor, _genuine_reference, genuine_state = (
        _designated_private_owner()
    )

    candidate_anchors = (
        object(),
        synthetic_source,
        ModuleType("offline_forged_owner_provisioning_authority"),
        forged,
        # A genuine anchor, transplanted onto a caller-controlled resolver.
        genuine_anchor,
        # A bare instance of the real anchor class, constructed directly.
        anchor_type(),
        authority_type(),
    )
    for candidate_anchor in candidate_anchors:
        with pytest.raises(BindingError, match="authenticity anchor is invalid"):
            _consume(owner=forged, anchor=candidate_anchor, reference=forged_reference)

    # 6. The origin closures are not merely unexported: they are unreachable
    #    by name, unreachable through the __closure__ cells of every exported
    #    function, and collected out of the process entirely.
    assert not [name for name in dir(note_path) if "origin_only" in name]

    live_origins = [
        obj
        for obj in gc.get_objects()
        if inspect.isfunction(obj) and obj.__name__.startswith("_origin_only_")
    ]
    assert live_origins == [], (
        f"owner-provisioning origin closures survived import: {live_origins}"
    )

    for name, value in reachable.items():
        if not inspect.isfunction(value) or not value.__closure__:
            continue
        for cell in value.__closure__:
            try:
                contents = cell.cell_contents
            except ValueError:
                continue
            assert not (
                inspect.isfunction(contents)
                and contents.__name__.startswith("_origin_only_")
            ), f"note_path.{name} leaks an origin closure via __closure__"
            # The one-shot latch must not be reachable/flippable either.
            assert not (
                isinstance(contents, dict) and "spent" in contents
            ), f"note_path.{name} leaks the origin latch via __closure__"

    # 7. Exhaustively attempt to self-register a forged anchor for a
    #    caller-controlled resolver using every registry and marker object
    #    reachable from exported closures.
    registries, markers = [], []
    for value in reachable.values():
        if not inspect.isfunction(value) or not value.__closure__:
            continue
        for cell in value.__closure__:
            try:
                contents = cell.cell_contents
            except ValueError:
                continue
            if type(contents).__name__ == "_IdentityRegistry":
                registries.append(contents)
            if type(contents) is object:
                markers.append(contents)

    attacker_resolver = ModuleType("attacker_controlled_resolver")
    attacker_resolver.DESIGNATION_ID = DESIGNATION_ID
    attacker_resolver.OpaqueSafePrivateBindingReference = type("R", (), {})
    attacker_resolver.PrivateBindingMaterial = type("M", (), {})
    attacker_resolver.release_to_public_consumer = lambda submitted: None
    attacker_reference = attacker_resolver.OpaqueSafePrivateBindingReference()
    snapshot_type = note_path._PrivateOwnerAnchorSnapshot

    for registry in registries:
        for marker in markers + [object()]:
            forged_anchor = anchor_type()
            try:
                registry.add(
                    forged_anchor,
                    snapshot_type(
                        resolver_ref=weakref.ref(attacker_resolver),
                        consumer_authorization_identity=AUTHORIZATION_ID,
                        consumer_workflow_run_id=WORKFLOW_RUN_ID,
                        trust_marker=marker,
                    ),
                )
            except Exception:
                continue
            with pytest.raises(BindingError):
                runtime._consume_root_owned_private_binding_reference(
                    private_binding_reference=attacker_reference,
                    private_owner_resolver=attacker_resolver,
                    private_owner_anchor=forged_anchor,
                    consumer_authorization_identity=AUTHORIZATION_ID,
                    consumer_workflow_run_id=WORKFLOW_RUN_ID,
                )

    assert forged_state["release_calls"] == 0
    assert genuine_state["reference"] == "AVAILABLE"

    # 8. Genuine, private-plane-provisioned artifacts still work, so the
    #    boundary refuses forgery without disabling legitimate consumption.
    #    This runs before the pool sweep below, which recycles shared owners.
    capability = _consume(
        owner=genuine_owner, anchor=genuine_anchor, reference=_genuine_reference
    )
    assert capability.consumer_authorization_identity == AUTHORIZATION_ID
    assert genuine_state["reference"] == "CONSUMED"

    # 9. The pool is fixed: calling the accessor can never grow the set of
    #    provisioned owners or bind one to a caller-controlled resolver.
    pooled = {
        id(note_path._take_offline_provisioned_private_owner()[0])
        for _ in range(note_path._OFFLINE_PROVISIONED_OWNER_POOL_SIZE * 3)
    }
    assert len(pooled) <= note_path._OFFLINE_PROVISIONED_OWNER_POOL_SIZE
    assert id(attacker_resolver) not in pooled

    assert note_path.NETWORK_CALLS == 0
    assert note_path.HIGHLEVEL_NETWORK_CALLS == 0
