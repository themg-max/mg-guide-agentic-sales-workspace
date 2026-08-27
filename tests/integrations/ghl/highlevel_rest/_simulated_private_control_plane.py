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
    """Model the process root designating this module as the private origin.

    Only the process root may do this in production; tests perform it
    explicitly so that the designation is never implicit or caller-driven.
    """
    import sys

    from integrations.ghl.highlevel_rest.note_path import (
        _ROOT_OWNED_PRIVATE_ORIGIN_MODULE_KEY,
    )

    monkeypatch.setitem(sys.modules, __name__, sys.modules[__name__])
    monkeypatch.setenv(_ROOT_OWNED_PRIVATE_ORIGIN_MODULE_KEY, __name__)
