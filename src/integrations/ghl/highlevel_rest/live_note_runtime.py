"""Live-note runtime composition root.

Production adapters and root-owned dependency composition are implemented.
Live runtime invocation remains separately authorization-gated; the private
test seam is limited to deterministic synthetic inputs.
"""

from __future__ import annotations

import importlib
import sqlite3
from typing import Any

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
_TARGET_RUNTIME_SERVICE_ACCOUNT = (
    "mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
)
_TARGET_RUNTIME_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)
_TARGET_RUNTIME_CREDENTIAL_LIFETIME_SECONDS = 3600


class LiveNoteRuntimeAssemblyError(RuntimeError):
    """Raised when assembly would exceed the authorized offline boundary."""


class _StoreOwnershipGuard:
    """Closes a root-owned store unless assembly transfers it to an adapter."""

    def __init__(self, execution_store: At1ExecutionStore) -> None:
        self._execution_store = execution_store
        self._ownership_transferred = False
        self._close_attempted = False

    def transfer_to_returned_adapter(self) -> None:
        self._ownership_transferred = True

    def close_after_failed_assembly(self) -> None:
        if self._ownership_transferred or self._close_attempted:
            return
        self._close_attempted = True
        try:
            self._execution_store._connection.close()
        except sqlite3.Error:
            # Cleanup must not replace the composition exception being unwound.
            pass


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


def _resolve_source_application_credentials() -> object:
    """Resolve source ADC only when the production composition root is invoked."""
    try:
        google_auth_module = importlib.import_module("google.auth")
    except ModuleNotFoundError as exc:  # pragma: no cover - optional offline dependency
        raise LiveNoteRuntimeAssemblyError(
            "google-auth is required for production runtime credential resolution"
        ) from exc
    credentials, _ = google_auth_module.default()
    return credentials


def _impersonate_target_runtime_credentials(source_credentials: object) -> object:
    """Create the one target-runtime credential used by Secret Manager."""
    try:
        impersonated_credentials_module = importlib.import_module(
            "google.auth.impersonated_credentials"
        )
    except ModuleNotFoundError as exc:  # pragma: no cover - optional offline dependency
        raise LiveNoteRuntimeAssemblyError(
            "google-auth impersonation support is required for production runtime assembly"
        ) from exc
    return impersonated_credentials_module.Credentials(
        source_credentials=source_credentials,
        target_principal=_TARGET_RUNTIME_SERVICE_ACCOUNT,
        target_scopes=list(_TARGET_RUNTIME_SCOPES),
        lifetime=_TARGET_RUNTIME_CREDENTIAL_LIFETIME_SECONDS,
    )


def _new_secret_manager_client(target_runtime_credentials: object) -> Any:
    """Create the sole Secret Manager client bound to the target runtime identity."""
    try:
        secretmanager_module = importlib.import_module("google.cloud.secretmanager")
    except ModuleNotFoundError as exc:  # pragma: no cover - optional offline dependency
        raise LiveNoteRuntimeAssemblyError(
            "google-cloud-secret-manager is required for production runtime assembly"
        ) from exc
    return secretmanager_module.SecretManagerServiceClient(
        credentials=target_runtime_credentials
    )


def _resolve_root_owned_runtime_dependencies() -> _RootOwnedLiveNoteRuntimeDependencies:
    """Resolve the minimal production dependencies from the orchestrator-owned process environment."""
    db_path = importlib.import_module("os").environ.get(_ROOT_OWNED_DB_CONFIG_KEY)
    if not isinstance(db_path, str) or not db_path.strip():
        raise LiveNoteRuntimeAssemblyError(
            "production live-note runtime assembly requires root-owned dependencies"
        )

    source_credentials = _resolve_source_application_credentials()
    target_runtime_credentials = _impersonate_target_runtime_credentials(
        source_credentials
    )
    secret_manager_client = _new_secret_manager_client(target_runtime_credentials)
    secret_accessor = GoogleSecretManagerLiveNoteSecretAccessor(
        client=secret_manager_client
    )
    credential_injection = RootOwnedLiveNoteCredentialInjection(
        accessor=secret_accessor,
        resource_name=_SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
    )
    commitment_key_provider = GoogleSecretManagerCommitmentKeyProvider(
        client=secret_manager_client
    )
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
    *,
    consumer_authorization_identity: str,
    consumer_workflow_run_id: str,
) -> note_path._VerifiedContactBindingCapability:
    """Validate the submitted capability against explicitly bound expectations.

    Expectations are never self-derived from the submitted capability, so a
    capability cannot vouch for its own authorization identity or workflow run.
    """
    return note_path._require_issued_verified_capability(
        verified_capability,
        location_id=getattr(verified_capability, "location_id", None),
        contact_id=getattr(verified_capability, "contact_id", None),
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )


def _consume_root_owned_private_binding_reference(
    *,
    private_binding_reference: object,
    consumer_authorization_identity: str,
    consumer_workflow_run_id: str,
    private_owner_resolver: object | None = None,
) -> note_path._VerifiedContactBindingCapability:
    """Consume a pre-existing opaque private binding reference.

    This composition root never mints private authority and never resolves an
    authority provider. It accepts only an opaque reference materialized earlier
    by the private control plane, and a finished capability is explicitly not an
    accepted boundary substitute.
    """
    if isinstance(private_binding_reference, note_path._VerifiedContactBindingCapability):
        raise LiveNoteRuntimeAssemblyError(
            "production live-note runtime assembly requires an opaque private binding reference"
        )
    expected_consumer_authorization_identity = note_path._require_identifier(
        "consumer_authorization_identity", consumer_authorization_identity
    )
    expected_consumer_workflow_run_id = note_path._require_identifier(
        "consumer_workflow_run_id", consumer_workflow_run_id
    )
    if private_owner_resolver is None:
        verified_capability = note_path._consume_private_at8_binding_lease(
            private_binding_reference,
            consumer_authorization_identity=expected_consumer_authorization_identity,
            consumer_workflow_run_id=expected_consumer_workflow_run_id,
        )
    else:
        verified_capability = (
            note_path._consume_designated_private_owner_binding_reference(
                private_owner_resolver=private_owner_resolver,
                private_binding_reference=private_binding_reference,
                consumer_authorization_identity=expected_consumer_authorization_identity,
                consumer_workflow_run_id=expected_consumer_workflow_run_id,
            )
        )
    return _validate_issued_capability(
        verified_capability,
        consumer_authorization_identity=expected_consumer_authorization_identity,
        consumer_workflow_run_id=expected_consumer_workflow_run_id,
    )


def assemble_bound_live_note_runtime(
    *,
    private_binding_reference: object,
    consumer_authorization_identity: str,
    consumer_workflow_run_id: str,
    private_owner_resolver: object | None = None,
) -> NotePathAdapter:
    """Assemble only from a consumed private reference and root-owned dependencies."""
    validated_capability = _consume_root_owned_private_binding_reference(
        private_binding_reference=private_binding_reference,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
        private_owner_resolver=private_owner_resolver,
    )
    dependencies = _resolve_root_owned_runtime_dependencies()
    store_ownership = _StoreOwnershipGuard(dependencies.execution_store)
    try:
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
    except Exception:
        store_ownership.close_after_failed_assembly()
        raise
    store_ownership.transfer_to_returned_adapter()
    return adapter


def _assemble_bound_live_note_runtime_for_tests(
    *,
    verified_capability: object,
    consumer_authorization_identity: str,
    consumer_workflow_run_id: str,
    synthetic_secret_accessor: SyntheticLiveNoteSecretAccessor,
    execution_store: At1ExecutionStore,
) -> NotePathAdapter:
    """Assemble the deterministic test runtime from validated capability identity."""
    validated_capability = _validate_issued_capability(
        verified_capability,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )

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
