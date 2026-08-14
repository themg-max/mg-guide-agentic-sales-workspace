"""Fail-closed runtime authority for the GHL tool manifest."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import FrozenSet

import yaml

MANIFEST_NODE = "ghl_mcp.blocked_capability_classes"


class ManifestContractError(ValueError):
    """Raised when the manifest cannot supply the required authorization data."""

    def __init__(self, detail: str) -> None:
        super().__init__(f"INVALID_GHL_MANIFEST_CONTRACT: {detail}")


class UnknownOperationError(ValueError):
    """Raised before a downstream call for an operation with no runtime mapping."""

    def __init__(self, operation_id: str) -> None:
        super().__init__(f"UNKNOWN_OPERATION_FAILS_CLOSED:{operation_id}")


class RuntimeManifestGate:
    """Classify operations and enforce the repository's nested manifest contract."""

    _CLASSIFIER_MAP = {
        "create-contact": "contact_create",
        "search-contacts-advanced": "contact_search",
        "get-contact": "contact_fetch",
    }

    def __init__(self, manifest_path: Path):
        try:
            raw_manifest = manifest_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ManifestContractError("manifest cannot be read") from exc

        try:
            data = yaml.safe_load(raw_manifest)
        except yaml.YAMLError as exc:
            raise ManifestContractError("manifest is not valid YAML") from exc

        self.blocked_classes = self._blocked_classes_from(data)

    @staticmethod
    def _blocked_classes_from(data: object) -> FrozenSet[str]:
        if not isinstance(data, Mapping):
            raise ManifestContractError("root must be a mapping")

        ghl_mcp = data.get("ghl_mcp")
        if not isinstance(ghl_mcp, Mapping):
            raise ManifestContractError("ghl_mcp must be a mapping")

        blocked = ghl_mcp.get("blocked_capability_classes")
        if not isinstance(blocked, list):
            raise ManifestContractError(
                "ghl_mcp.blocked_capability_classes must be a list"
            )
        if any(not isinstance(item, str) or not item.strip() for item in blocked):
            raise ManifestContractError(
                "ghl_mcp.blocked_capability_classes entries must be non-empty strings"
            )
        return frozenset(blocked)

    def classify_operation(self, operation_id: str) -> str:
        try:
            return self._CLASSIFIER_MAP[operation_id]
        except KeyError as exc:
            raise UnknownOperationError(operation_id) from exc

    def is_blocked(self, operation_id: str) -> bool:
        return self.classify_operation(operation_id) in self.blocked_classes
