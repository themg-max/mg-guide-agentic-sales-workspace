import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from mg_guide.firestore_audit.project import project_workflow_run_audit
from mg_guide.firestore_audit.models import ProjectionContext
from orchestration.models import base_packet
from orchestration.manifest_gate import RuntimeManifestGate

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def execute_d1_run(manifest_path: Path, operation: str = "create-contact") -> Dict[str, Any]:
    run_id = "at-09-run"
    gate = RuntimeManifestGate(manifest_path)
    
    packet = base_packet(
        run_id=run_id,
        status="received",
        meeting={"transcript_hash": "0000000000000000000000000000000000000000000000000000000000000000", "call_id": "test"},
        participants=[],
        created_at=_utc_now(),
        started_at=_utc_now(),
    )
    
    if gate.is_blocked(operation):
        cap_class = gate.classify_operation(operation)
        packet["audit"]["warnings"].append(f"TOOL_MANIFEST_REFUSED:{cap_class}")
        packet["run"]["status"] = "failed"
        packet["audit"]["final_disposition"] = "failed"
        packet["audit"]["completed_at"] = _utc_now()
        # Ensure counters are zero
        packet["external_effects"] = 0
        return packet

    # If it was allowed, it would reach adapter (mocked here as complete for testing)
    packet["run"]["status"] = "completed"
    packet["audit"]["final_disposition"] = "completed"
    packet["audit"]["completed_at"] = _utc_now()
    return packet

def write_proof(packet: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ctx = ProjectionContext(
        recorded_at=_utc_now(),
        fixture_id="at-09-d1-proof",
        source_refs=[],
        writer_component="nw008_tranche_d",
        writer_component_version="v1",
        writer_mode="local_fixture",
    )
    
    audit = project_workflow_run_audit(packet, ctx)
    
    with open(output_dir / "at-09-run.json", "w") as f:
        json.dump(packet, f, indent=2)
        
    with open(output_dir / "at-09-workflow-run-audit.json", "w") as f:
        json.dump(audit, f, indent=2)

if __name__ == "__main__":
    manifest_path = Path("contracts/ghl_tool_manifest.yaml")
    output_dir = Path("proof/nw008/tranche-d")
    packet = execute_d1_run(manifest_path)
    write_proof(packet, output_dir)
