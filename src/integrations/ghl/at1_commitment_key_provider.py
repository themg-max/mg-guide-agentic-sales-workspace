"""Commitment-key material providers for :class:`At1ExecutionStore`.

Production resolution is pinned to the designated Secret Manager version.
Live invocation remains separately authorization-gated; tests inject fake
clients and never access a real secret payload.
"""

from __future__ import annotations

import importlib
import re
from typing import Any


_MATERIAL_FACTORY_TOKEN = object()
_VERSION_RESOURCE_PATTERN = re.compile(
    r"^projects/[^/\s?#]+/secrets/[^/\s?#]+/versions/[1-9][0-9]*$"
)
DESIGNATED_COMMITMENT_KEY_VERSION_RESOURCE = (
    "projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1"
)


def validate_version_resource(version_resource: str) -> str:
    """Validate the immutable exact-version identifier accepted by the store."""

    if not isinstance(version_resource, str) or not _VERSION_RESOURCE_PATTERN.fullmatch(
        version_resource
    ):
        raise ValueError("version_resource must be an exact positive numeric version resource")
    return version_resource


def _new_secret_manager_client() -> Any:
    """Create a Secret Manager client only when production resolution is invoked."""

    try:
        secretmanager_module = importlib.import_module("google.cloud.secretmanager")
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency is optional in offline mode
        raise RuntimeError(
            "google-cloud-secret-manager is required for production commitment-key resolution"
        ) from exc
    return secretmanager_module.SecretManagerServiceClient()


class CommitmentKeyProvider:
    """Base production provider contract for commitment-key material."""

    def resolve(self) -> "CommitmentKeyMaterial":
        raise NotImplementedError("CommitmentKeyProvider.resolve() must be implemented")


class CommitmentKeyMaterial:
    """Opaque payload/version pairing resolved by a commitment-key provider."""

    __slots__ = ("__payload", "__version_resource")

    def __init__(
        self,
        *,
        _payload: bytes,
        _version_resource: str,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _MATERIAL_FACTORY_TOKEN:
            raise TypeError("CommitmentKeyMaterial must be resolved by a provider")
        if not isinstance(_payload, bytes) or not _payload:
            raise ValueError("commitment-key material payload must be non-empty")
        self.__payload = _payload
        self.__version_resource = validate_version_resource(_version_resource)

    @property
    def version_resource(self) -> str:
        """Return the non-secret immutable version identifier."""

        return self.__version_resource

    def __repr__(self) -> str:
        return f"{type(self).__name__}(version_resource={self.__version_resource!r})"

    __str__ = __repr__

    def __reduce_ex__(self, protocol: int) -> object:
        raise TypeError("CommitmentKeyMaterial serialization is forbidden")

    def _payload_bytes(self) -> bytes:
        return self.__payload


class SyntheticCommitmentKeyProvider:
    """Deterministic offline provider; it never accesses Secret Manager."""

    __slots__ = ("__payload", "__version_resource")

    def __init__(self, *, payload: str, version_resource: str) -> None:
        if not isinstance(payload, str) or not payload:
            raise ValueError("synthetic commitment-key payload must be non-empty")
        self.__payload = payload.encode("utf-8")
        self.__version_resource = validate_version_resource(version_resource)

    def resolve(self) -> CommitmentKeyMaterial:
        """Bind deterministic payload and exact version identity into one result."""

        return CommitmentKeyMaterial(
            _payload=self.__payload,
            _version_resource=self.__version_resource,
            _factory_token=_MATERIAL_FACTORY_TOKEN,
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(version_resource={self.__version_resource!r})"

    __str__ = __repr__


class GoogleSecretManagerCommitmentKeyProvider(CommitmentKeyProvider):
    """Resolve exact-version commitment-key material from Secret Manager."""

    __slots__ = ("__client", "__secret_resource", "__version_resource")

    def __init__(
        self,
        *,
        client: Any | None = None,
    ) -> None:
        self.__secret_resource = DESIGNATED_COMMITMENT_KEY_VERSION_RESOURCE.rsplit(
            "/versions/", 1
        )[0]
        self.__version_resource = DESIGNATED_COMMITMENT_KEY_VERSION_RESOURCE
        self.__client = client

    @property
    def secret_resource(self) -> str:
        return self.__secret_resource

    @property
    def version_resource(self) -> str:
        return self.__version_resource

    def resolve(self) -> CommitmentKeyMaterial:
        """Fetch and bind the exact numeric Secret Manager version payload."""

        client = self.__client if self.__client is not None else _new_secret_manager_client()
        response = client.access_secret_version(request={"name": self.__version_resource})
        payload = getattr(response, "payload", None)
        if payload is None:
            raise ValueError("Secret Manager response did not include payload data")
        data = getattr(payload, "data", None)
        if data is None:
            raise ValueError("Secret Manager payload did not include data bytes")
        raw_bytes = bytes(data)
        if not raw_bytes:
            raise ValueError("commitment-key payload must be non-empty")
        return CommitmentKeyMaterial(
            _payload=raw_bytes,
            _version_resource=self.__version_resource,
            _factory_token=_MATERIAL_FACTORY_TOKEN,
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(secret_resource={self.__secret_resource!r}, "
            f"version_resource={self.__version_resource!r})"
        )

    __str__ = __repr__


def _payload_bytes_from_material(material: CommitmentKeyMaterial) -> bytes:
    if type(material) is not CommitmentKeyMaterial:
        raise TypeError("commitment_material must be provider-resolved CommitmentKeyMaterial")
    return material._payload_bytes()
