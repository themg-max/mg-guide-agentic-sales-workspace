import pytest
import yaml
import json
from pathlib import Path
from orchestration.nw008_tranche_d import execute_d1_run, write_proof

@pytest.fixture
def base_manifest_path(tmp_path):
    manifest = {
        "blocked_capability_classes": ["contact_create", "email_send"]
    }
    p = tmp_path / "ghl_tool_manifest.yaml"
    p.write_text(yaml.dump(manifest))
    return p

def test_nc_d1_3_blocked_operation_refused_early(base_manifest_path):
    packet = execute_d1_run(base_manifest_path, "create-contact")
    assert packet["run"]["status"] == "failed"
    assert "TOOL_MANIFEST_REFUSED:contact_create" in packet["audit"]["warnings"]

def test_nc_d1_5_normal_run_no_warning(base_manifest_path):
    packet = execute_d1_run(base_manifest_path, "search-contacts")
    assert packet["run"]["status"] == "completed"
    assert not any("TOOL_MANIFEST_REFUSED" in w for w in packet["audit"]["warnings"])

def test_nc_d1_6_and_7_stage_a_projection_and_counters(base_manifest_path, tmp_path):
    packet = execute_d1_run(base_manifest_path, "create-contact")
    
    proof_dir = tmp_path / "proof"
    write_proof(packet, proof_dir)
    
    with open(proof_dir / "at-09-workflow-run-audit.json") as f:
        audit = json.load(f)
        
    assert "TOOL_MANIFEST_REFUSED:contact_create" in audit["warnings"]
    assert audit["external_effects"]["counters"]["GHL_READS"] == 0
    assert audit["external_effects"]["counters"]["GHL_WRITES"] == 0
    assert audit["external_effects"]["counters"]["EXTERNAL_EFFECTS"] == 0
    assert audit["tool_call_counts"]["ghl_mcp"]["reads"] == 0
    assert audit["tool_call_counts"]["ghl_mcp"]["writes"] == 0
