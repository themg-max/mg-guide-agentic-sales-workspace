import pytest
import yaml
from pathlib import Path
from orchestration.manifest_gate import RuntimeManifestGate

@pytest.fixture
def base_manifest_path(tmp_path):
    manifest = {
        "blocked_capability_classes": ["contact_create", "email_send"]
    }
    p = tmp_path / "ghl_tool_manifest.yaml"
    p.write_text(yaml.dump(manifest))
    return p

def test_manifest_gate_blocks_create_contact(base_manifest_path):
    gate = RuntimeManifestGate(base_manifest_path)
    assert gate.is_blocked("create-contact")

def test_manifest_gate_allows_unblocked(base_manifest_path):
    gate = RuntimeManifestGate(base_manifest_path)
    # NC-D1-2
    assert not gate.is_blocked("get-contact")

def test_manifest_gate_test_manifest_unblocks(tmp_path):
    # NC-D1-4
    manifest = {
        "blocked_capability_classes": ["email_send"]
    }
    p = tmp_path / "unblocked_manifest.yaml"
    p.write_text(yaml.dump(manifest))
    gate = RuntimeManifestGate(p)
    assert not gate.is_blocked("create-contact")
