"""Live-note credential acquisition with a root-owned production accessor.

Production composition constructs the Secret Manager adapter with one designated
version resource. Live invocation remains separately authorization-gated; tests
inject a fake client and never access a real Secret Manager payload.
"""

from __future__ import annotations

import importlib
from typing import Any, Protocol

from .live_note_transport import InjectedLiveNoteCredential, LiveNoteTransportError


class LiveNoteCredentialProviderError(ValueError):
    """Raised when credential acquisition is rejected before any secret access."""


class LiveNoteSecretAccessor(Protocol):
    """Injectable secret accessor interface."""

    def read_secret_payload(self, *, resource_name: str) -> str:
        """Return a secret payload string for the configured resource name."""


class SyntheticLiveNoteSecretAccessor:
    """In-memory synthetic accessor for offline deterministic tests only."""

    REAL_SECRET_READS = 0
    SECRET_PAYLOAD_READS_ARE_SYNTHETIC = True

    def __init__(self, *, payloads: dict[str, str] | None = None) -> None:
        self._payloads = {
            str(key): str(value) for key, value in dict(payloads or {}).items()
        }
        self._synthetic_reads = 0

    @property
    def synthetic_read_count(self) -> int:
        return self._synthetic_reads

    def read_secret_payload(self, *, resource_name: str) -> str:
        if not isinstance(resource_name, str) or not resource_name.strip():
            raise LiveNoteCredentialProviderError(
                "resource_name must be a non-empty string"
            )
        if resource_name not in self._payloads:
            raise LiveNoteCredentialProviderError(
                "synthetic accessor has no payload for resource_name"
            )
        self._synthetic_reads += 1
        return self._payloads[resource_name]

    def __repr__(self) -> str:
        return (
            "SyntheticLiveNoteSecretAccessor("
            f"resources={len(self._payloads)}, "
            f"synthetic_reads={self._synthetic_reads})"
        )

    def __str__(self) -> str:
        return self.__repr__()


DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE = (
    "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1"
)


def _new_secret_manager_client() -> Any:
    try:
        secretmanager_module = importlib.import_module("google.cloud.secretmanager")
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency is optional in offline mode
        raise RuntimeError(
            "google-cloud-secret-manager is required for production secret resolution"
        ) from exc
    return secretmanager_module.SecretManagerServiceClient()


class GoogleSecretManagerLiveNoteSecretAccessor:
    """Production Secret Manager-backed accessor bound to the exact GHL PIT version."""

    REAL_SECRET_READS = 0
    SECRET_PAYLOAD_READS_ARE_SYNTHETIC = False

    def __init__(
        self,
        *,
        client: Any | None = None,
    ) -> None:
        self._client = client
        self.REAL_SECRET_READS = 0
        self.SECRET_PAYLOAD_READS_ARE_SYNTHETIC = False

    @property
    def resource_name(self) -> str:
        return DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE

    @property
    def version_resource(self) -> str:
        return DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE

    def read_secret_payload(self, *, resource_name: str) -> str:
        if resource_name != DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE:
            raise LiveNoteCredentialProviderError(
                "resource_name does not match the root-owned Secret Manager resource"
            )
        client = self._client if self._client is not None else _new_secret_manager_client()
        response = client.access_secret_version(
            request={"name": DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE}
        )
        payload = getattr(response, "payload", None)
        if payload is None:
            raise LiveNoteCredentialProviderError(
                "Secret Manager response did not include a payload"
            )
        data = getattr(payload, "data", None)
        if data is None:
            raise LiveNoteCredentialProviderError(
                "Secret Manager payload did not include data bytes"
            )
        value = data.decode("utf-8") if isinstance(data, bytes) else str(data)
        if not value.strip():
            raise LiveNoteCredentialProviderError(
                "accessor returned an empty credential payload"
            )
        self.REAL_SECRET_READS += 1
        return value

    def __repr__(self) -> str:
        return (
            "GoogleSecretManagerLiveNoteSecretAccessor("
            f"resource_name={DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE!r}, "
            f"real_reads={self.REAL_SECRET_READS})"
        )

    __str__ = __repr__


class RootOwnedLiveNoteCredentialInjection:
    """Bind a root-owned accessor to one sealed credential resource."""

    def __init__(
        self,
        *,
        accessor: LiveNoteSecretAccessor,
        resource_name: str,
    ) -> None:
        if accessor is None or not hasattr(accessor, "read_secret_payload"):
            raise LiveNoteCredentialProviderError(
                "root-owned credential injection requires an accessor"
            )
        if not isinstance(resource_name, str) or not resource_name.strip():
            raise LiveNoteCredentialProviderError(
                "root-owned credential injection requires a resource_name"
            )
        self._accessor = accessor
        self._resource_name = resource_name

    def build_provider(self) -> "LiveNoteCredentialProvider":
        """Create the provider without exposing its accessor or resource identity."""
        return LiveNoteCredentialProvider(
            accessor=self._accessor,
            resource_name=self._resource_name,
        )

    def __repr__(self) -> str:
        return "RootOwnedLiveNoteCredentialInjection(<redacted>)"

    __str__ = __repr__


class LiveNoteCredentialProvider:
    """Credential provider that returns ``InjectedLiveNoteCredential``.

    Secret acquisition is delegated exclusively to an injected accessor. This
    class never imports Secret Manager clients, never shells out to gcloud, and
    never discovers tokens from the environment.
    """

    REAL_SECRET_READS_AUTHORIZED = False
    REAL_CREDENTIAL_USE_AUTHORIZED = False
    ENVIRONMENT_TOKEN_DISCOVERY = False
    GCLOUD_SUBPROCESS_SECRET_ACCESS = False
    SHELL_SECRET_ACCESS = False

    def __init__(
        self,
        *,
        accessor: LiveNoteSecretAccessor,
        resource_name: str,
    ) -> None:
        if accessor is None:
            raise LiveNoteCredentialProviderError("accessor is required")
        if not hasattr(accessor, "read_secret_payload"):
            raise LiveNoteCredentialProviderError(
                "accessor must implement read_secret_payload"
            )
        if not isinstance(resource_name, str) or not resource_name.strip():
            raise LiveNoteCredentialProviderError(
                "resource_name must be a non-empty string"
            )
        self._accessor = accessor
        self._resource_name = resource_name
        self._acquire_count = 0

    @property
    def resource_name(self) -> str:
        """Configured secret resource identity (not a secret payload)."""
        return self._resource_name

    @property
    def acquire_count(self) -> int:
        return self._acquire_count

    def get_credential(self) -> InjectedLiveNoteCredential:
        """Acquire a credential through the injected accessor only."""
        payload = self._accessor.read_secret_payload(resource_name=self._resource_name)
        if not isinstance(payload, str) or not payload.strip():
            raise LiveNoteCredentialProviderError(
                "accessor returned an empty credential payload"
            )
        try:
            credential = InjectedLiveNoteCredential(payload)
        except LiveNoteTransportError as exc:
            raise LiveNoteCredentialProviderError(str(exc)) from exc
        self._acquire_count += 1
        return credential

    def __repr__(self) -> str:
        return (
            "LiveNoteCredentialProvider("
            "resource_name=<redacted>, "
            "accessor=<injected>, "
            f"acquire_count={self._acquire_count}, "
            "real_secret_reads_authorized=False)"
        )

    def __str__(self) -> str:
        return self.__repr__()
