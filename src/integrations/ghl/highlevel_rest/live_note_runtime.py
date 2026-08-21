"""Offline-only live-note runtime composition root.

Production assembly deliberately fails closed until a later authorization
establishes root-owned execution-store construction and a concrete secret
accessor. The private test seam is limited to deterministic synthetic inputs.
"""

from __future__ import annotations

from integrations.ghl.at1_execution_store import At1ExecutionStore

from . import note_path
from .live_note_credential_provider import (
    LiveNoteCredentialProvider,
    SyntheticLiveNoteSecretAccessor,
)
from .live_note_http_client import ConcreteLiveNoteHttpClient
from .live_note_transport import BoundedLiveNoteTransport
from .note_path import NotePathAdapter

_SEALED_LIVE_NOTE_REST_RESOURCE_NAME = (
    "projects/831270426395/secrets/MG_GUIDE_PIT_GHL"
)


class LiveNoteRuntimeAssemblyError(RuntimeError):
    """Raised when assembly would exceed the authorized offline boundary."""


def _validate_issued_capability(
    verified_capability: object,
) -> note_path._VerifiedContactBindingCapability:
    """Validate only the submitted capability before any adapter construction."""
    return note_path._require_issued_verified_capability(
        verified_capability,
        location_id=getattr(verified_capability, "location_id", None),
        contact_id=getattr(verified_capability, "contact_id", None),
        consumer_authorization_identity=getattr(
            verified_capability, "consumer_authorization_identity", None
        ),
        consumer_workflow_run_id=getattr(
            verified_capability, "consumer_workflow_run_id", None
        ),
    )


def assemble_bound_live_note_runtime(
    *,
    verified_capability: object,
) -> NotePathAdapter:
    """Validate the production capability, then fail closed without a root store."""
    _validate_issued_capability(verified_capability)
    raise LiveNoteRuntimeAssemblyError(
        "production live-note runtime assembly requires a root-owned execution store"
    )


def _assemble_bound_live_note_runtime_for_tests(
    *,
    verified_capability: object,
    synthetic_secret_accessor: SyntheticLiveNoteSecretAccessor,
    execution_store: At1ExecutionStore,
) -> NotePathAdapter:
    """Assemble the deterministic test runtime from validated capability identity."""
    validated_capability = _validate_issued_capability(verified_capability)

    if not isinstance(synthetic_secret_accessor, SyntheticLiveNoteSecretAccessor):
        raise LiveNoteRuntimeAssemblyError(
            "synthetic_secret_accessor must be a SyntheticLiveNoteSecretAccessor"
        )
    if not isinstance(execution_store, At1ExecutionStore):
        raise LiveNoteRuntimeAssemblyError(
            "execution_store must be an At1ExecutionStore in the private test seam"
        )

    credential_provider = LiveNoteCredentialProvider(
        accessor=synthetic_secret_accessor,
        resource_name=_SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
    )
    credential = credential_provider.get_credential()
    http_client = ConcreteLiveNoteHttpClient()
    transport = BoundedLiveNoteTransport(
        bound_contact_id=validated_capability.contact_id,
        credential=credential,
        http_client=http_client,
    )
    adapter = NotePathAdapter(
        location_id=validated_capability.location_id,
        contact_id=validated_capability.contact_id,
        transport=transport,
        consumer_authorization_identity=(
            validated_capability.consumer_authorization_identity
        ),
        consumer_workflow_run_id=validated_capability.consumer_workflow_run_id,
        execution_store=execution_store,
    )
    adapter._verified_contact_binding_capability = validated_capability
    return adapter
