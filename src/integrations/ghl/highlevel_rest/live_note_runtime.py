"""Live-note runtime composition root.

Production adapters and root-owned dependency composition are implemented.
Live runtime invocation remains separately authorization-gated; the private
test seam is limited to deterministic synthetic inputs.
"""

from __future__ import annotations

import importlib

from integrations.ghl.at1_commitment_key_provider import (
    GoogleSecretManagerCommitmentKeyProvider,
)
from integrations.ghl.at1_execution_store import At1ExecutionStore

from . import note_path
from .live_note_credential_provider import (
    GoogleSecretManagerLiveNoteSecretAccessor,
    LiveNoteCredentialProvider,
    RootOwnedLiveNoteCredentialInjection,
    SyntheticLiveNoteSecretAccessor,
)
from .live_note_http_client import ConcreteLiveNoteHttpClient
from .live_note_transport import BoundedLiveNoteTransport
from .note_path import NotePathAdapter

_SEALED_LIVE_NOTE_REST_RESOURCE_NAME = (
    "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1"
)
_ROOT_OWNED_DB_CONFIG_KEY = "MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH"


class LiveNoteRuntimeAssemblyError(RuntimeError):
    """Raised when assembly would exceed the authorized offline boundary."""


class _RootOwnedLiveNoteRuntimeDependencies:
    """Dependencies resolved exclusively by the composition root's environment."""

    def __init__(
        self,
        *,
        credential_injection: RootOwnedLiveNoteCredentialInjection,
        execution_store: At1ExecutionStore,
    ) -> None:
        if not isinstance(
            credential_injection, RootOwnedLiveNoteCredentialInjection
        ):
            raise LiveNoteRuntimeAssemblyError(
                "root-owned credential injection is required"
            )
        if not isinstance(execution_store, At1ExecutionStore):
            raise LiveNoteRuntimeAssemblyError(
                "root-owned execution store is required"
            )
        self.credential_injection = credential_injection
        self.execution_store = execution_store


def _resolve_root_owned_runtime_dependencies() -> _RootOwnedLiveNoteRuntimeDependencies:
    """Resolve the minimal production dependencies from the orchestrator-owned process environment."""
    db_path = importlib.import_module("os").environ.get(_ROOT_OWNED_DB_CONFIG_KEY)
    if not isinstance(db_path, str) or not db_path.strip():
        raise LiveNoteRuntimeAssemblyError(
            "production live-note runtime assembly requires root-owned dependencies"
        )

    secret_accessor = GoogleSecretManagerLiveNoteSecretAccessor()
    credential_injection = RootOwnedLiveNoteCredentialInjection(
        accessor=secret_accessor,
        resource_name=_SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
    )
    commitment_key_provider = GoogleSecretManagerCommitmentKeyProvider()
    try:
        commitment_material = commitment_key_provider.resolve()
        execution_store = At1ExecutionStore(
            db_path=db_path,
            commitment_material=commitment_material,
        )
    except (RuntimeError, ValueError, TypeError) as exc:
        raise LiveNoteRuntimeAssemblyError(
            "production live-note runtime assembly requires root-owned dependencies"
        ) from exc
    return _RootOwnedLiveNoteRuntimeDependencies(
        credential_injection=credential_injection,
        execution_store=execution_store,
    )


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
    """Assemble only from validated capability and root-owned dependencies."""
    validated_capability = _validate_issued_capability(verified_capability)
    dependencies = _resolve_root_owned_runtime_dependencies()
    credential = dependencies.credential_injection.build_provider().get_credential()
    transport = BoundedLiveNoteTransport(
        bound_contact_id=validated_capability.contact_id,
        credential=credential,
        http_client=ConcreteLiveNoteHttpClient(),
    )
    adapter = NotePathAdapter(
        location_id=validated_capability.location_id,
        contact_id=validated_capability.contact_id,
        transport=transport,
        consumer_authorization_identity=(
            validated_capability.consumer_authorization_identity
        ),
        consumer_workflow_run_id=validated_capability.consumer_workflow_run_id,
        execution_store=dependencies.execution_store,
    )
    adapter._verified_contact_binding_capability = validated_capability
    return adapter


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
