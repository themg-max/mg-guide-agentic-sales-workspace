"""Offline test-side stand-in for the private control plane's owner origin.

This module is TEST-ONLY and deliberately lives outside ``src/`` so that
production public code performs no authority origin whatsoever -- not at
import time and not at call time.

It models the shape of the real private control plane: a provisioned-resolver
artifact that cannot be constructed by any public caller, because construction
requires a token that never leaves this module. Public ``note_path`` verifies
that property behaviourally; it never creates or vouches for an anchor.
"""

from __future__ import annotations

from types import MappingProxyType
from types import ModuleType

from integrations.ghl.highlevel_rest.note_path import _DESIGNATED_PRIVATE_OWNER_ID


_CONSTRUCTION_TOKEN = object()

# Registry of artifacts this module genuinely provisioned. Mirrors the real
# private plane, which recognises its own artifacts by identity so that a
# ``__new__``-bypassed or otherwise reconstructed instance is not accepted.
_PROVISIONED_ARTIFACTS: "dict[int, object]" = {}


# The contract note_path reads to recognise a private-origin defining module.
PRIVATE_ORIGIN_ANCHOR_CONTRACT = MappingProxyType(
    {
        "DESIGNATION_ID": _DESIGNATED_PRIVATE_OWNER_ID,
        "PRIVATE_CONTROL_PLANE_IS_AUTHORITY_SOURCE": True,
        "ANCHOR_PUBLICLY_CONSTRUCTIBLE": False,
    }
)


class ProvisionedPrivateOwnerResolver:
    """Artifact proving the private control plane provisioned a resolver.

    Construction requires the private token, so no public caller can create
    one, and no public module can vouch for one it did not receive.
    """

    __slots__ = (
        "designation_id",
        "provisioned_resolver",
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
        "__weakref__",
    )

    def __init__(
        self,
        *,
        _token: object = None,
        resolver: ModuleType = None,
        authorization_identity: str = "",
        workflow_run_id: str = "",
    ) -> None:
        if _token is not _CONSTRUCTION_TOKEN:
            raise RuntimeError(
                "provisioned resolver bindings cannot be constructed or "
                "reconstructed"
            )
        object.__setattr__(self, "designation_id", _DESIGNATED_PRIVATE_OWNER_ID)
        object.__setattr__(self, "provisioned_resolver", resolver)
        object.__setattr__(
            self, "consumer_authorization_identity", authorization_identity
        )
        object.__setattr__(self, "consumer_workflow_run_id", workflow_run_id)

    def __repr__(self) -> str:
        return "<ProvisionedPrivateOwnerResolver>"


def is_genuinely_provisioned(artifact: object) -> bool:
    """Recognise only artifacts this module actually provisioned."""
    return _PROVISIONED_ARTIFACTS.get(id(artifact)) is artifact


def provision_simulated_private_owner(
    *,
    authorization_identity: str,
    workflow_run_id: str,
    module_name: str = "simulated_private_owner",
) -> tuple[ModuleType, ProvisionedPrivateOwnerResolver]:
    """Model an owner/anchor pair the private control plane already provisioned."""
    resolver = ModuleType(module_name)
    resolver.DESIGNATION_ID = _DESIGNATED_PRIVATE_OWNER_ID
    anchor = ProvisionedPrivateOwnerResolver(
        _token=_CONSTRUCTION_TOKEN,
        resolver=resolver,
        authorization_identity=authorization_identity,
        workflow_run_id=workflow_run_id,
    )
    _PROVISIONED_ARTIFACTS[id(anchor)] = anchor
    return resolver, anchor


def install_as_root_designated_private_origin(monkeypatch) -> None:
    """Drive the REAL root composition seam to bind this module as the origin.

    Only the process root may select an authority origin. Tests therefore go
    through the production composition boundary rather than reaching into
    note_path, so the seam under test is the one production uses.

    The binding in note_path is one-shot per trust-issuer instance, so the
    module-level issuer is rebuilt first to give each test a pristine,
    unbound composition. That models process startup, not a rebinding
    capability offered to callers.
    """
    import sys

    import integrations.ghl.highlevel_rest.live_note_runtime as runtime
    from integrations.ghl.highlevel_rest import note_path

    monkeypatch.setitem(sys.modules, __name__, sys.modules[__name__])
    monkeypatch.setenv(
        runtime._ROOT_OWNED_PRIVATE_ORIGIN_MODULE_KEY, __name__
    )
    _rebuild_unbound_trust_issuer(monkeypatch, note_path)
    runtime.compose_root_owned_private_origin()


def _rebuild_unbound_trust_issuer(monkeypatch, note_path) -> None:
    """Give the test a fresh, not-yet-composed trust issuer (process startup)."""
    rebuilt = note_path._build_internal_trust_issuer()
    names = _TRUST_ISSUER_EXPORT_NAMES
    assert len(rebuilt) == len(names), (len(rebuilt), len(names))
    for name, value in zip(names, rebuilt):
        monkeypatch.setattr(note_path, name, value)


_TRUST_ISSUER_EXPORT_NAMES = (
    "_issue_bound_contact_capability",
    "_issue_synthetic_test_capability",
    "_issue_private_at8_handoff_source_for_synthetic_tests",
    "_handoff_private_at8_capability_from_registered_source",
    "_issue_private_at8_binding_reference_for_synthetic_tests",
    "_consume_private_at8_binding_lease",
    "_bind_root_composed_private_origin",
    "_consume_designated_private_owner_binding_reference",
    "_private_at8_binding_lease_state",
    "_build_bound_contact_get",
    "_require_issued_verified_capability",
)
