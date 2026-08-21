"""Offline-only commitment-key material for :class:`At1ExecutionStore`."""

from __future__ import annotations

import re


_MATERIAL_FACTORY_TOKEN = object()
_VERSION_RESOURCE_PATTERN = re.compile(
    r"^projects/[^/\s?#]+/secrets/[^/\s?#]+/versions/[1-9][0-9]*$"
)


def validate_version_resource(version_resource: str) -> str:
    """Validate the immutable exact-version identifier accepted by the store."""

    if not isinstance(version_resource, str) or not _VERSION_RESOURCE_PATTERN.fullmatch(
        version_resource
    ):
        raise ValueError("version_resource must be an exact positive numeric version resource")
    return version_resource


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


def _payload_bytes_from_material(material: CommitmentKeyMaterial) -> bytes:
    if type(material) is not CommitmentKeyMaterial:
        raise TypeError("commitment_material must be provider-resolved CommitmentKeyMaterial")
    return material._payload_bytes()
