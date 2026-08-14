from pathlib import Path

import pytest
import yaml

from orchestration.manifest_gate import (
    MANIFEST_NODE,
    ManifestContractError,
    RuntimeManifestGate,
    UnknownOperationError,
)


@pytest.fixture
def base_manifest_path(tmp_path: Path) -> Path:
    manifest = {
        "ghl_mcp": {
            "blocked_capability_classes": ["contact_create", "email_send"],
        }
    }
    path = tmp_path / "ghl_tool_manifest.yaml"
    path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    return path


def test_manifest_gate_uses_nested_manifest_authority(base_manifest_path: Path) -> None:
    gate = RuntimeManifestGate(base_manifest_path)

    assert MANIFEST_NODE == "ghl_mcp.blocked_capability_classes"
    assert gate.classify_operation("create-contact") == "contact_create"
    assert gate.is_blocked("create-contact") is True


def test_manifest_gate_classifies_known_unblocked_operations(
    base_manifest_path: Path,
) -> None:
    gate = RuntimeManifestGate(base_manifest_path)

    assert gate.classify_operation("search-contacts-advanced") == "contact_search"
    assert gate.classify_operation("get-contact") == "contact_fetch"
    assert gate.is_blocked("search-contacts-advanced") is False


@pytest.mark.parametrize(
    "manifest",
    [
        [],
        {},
        {"ghl_mcp": []},
        {"ghl_mcp": {}},
        {"ghl_mcp": {"blocked_capability_classes": "contact_create"}},
        {"ghl_mcp": {"blocked_capability_classes": [""]}},
        {"ghl_mcp": {"blocked_capability_classes": [1]}},
    ],
)
def test_malformed_manifest_fails_closed(tmp_path: Path, manifest: object) -> None:
    path = tmp_path / "manifest.yaml"
    path.write_text(yaml.safe_dump(manifest), encoding="utf-8")

    with pytest.raises(ManifestContractError, match="INVALID_GHL_MANIFEST_CONTRACT"):
        RuntimeManifestGate(path)


def test_unknown_operation_fails_closed(base_manifest_path: Path) -> None:
    gate = RuntimeManifestGate(base_manifest_path)

    with pytest.raises(UnknownOperationError, match="UNKNOWN_OPERATION_FAILS_CLOSED"):
        gate.is_blocked("not-a-known-operation")


def test_manifest_data_can_allow_known_create_contact(tmp_path: Path) -> None:
    path = tmp_path / "manifest.yaml"
    path.write_text(
        yaml.safe_dump({"ghl_mcp": {"blocked_capability_classes": ["email_send"]}}),
        encoding="utf-8",
    )

    assert RuntimeManifestGate(path).is_blocked("create-contact") is False
