from __future__ import annotations

import json

from mg_guide.firestore_audit.memory_store import MemoryAuditStore
from mg_guide.firestore_audit.project import project_workflow_run_audit

TERMINAL_CASES = [
    ("packet-success.completed.json", "audit-success.completed.json", "completed"),
    (
        "packet-stage-change-denied.completed_with_review.json",
        "audit-stage-change-denied.completed_with_review.json",
        "completed_with_review",
    ),
    (
        "packet-ambiguous-contact.blocked.json",
        "audit-ambiguous-contact.blocked.json",
        "blocked",
    ),
    (
        "packet-tool-failure.failed.json",
        "audit-tool-failure.failed.json",
        "failed",
    ),
]


def test_projection_external_effect_counters_zero(load_packet, stage_a_context_for):
    for packet_name, _, _ in TERMINAL_CASES:
        audit = project_workflow_run_audit(
            load_packet(packet_name), stage_a_context_for(packet_name)
        )
        assert audit["external_effects"]["packet_external_effects"] == 0
        assert audit["external_effects"]["counters"]["GHL_READS"] == 0
        assert audit["external_effects"]["counters"]["GHL_WRITES"] == 0
        assert audit["external_effects"]["counters"]["EXTERNAL_EFFECTS"] == 0
        assert audit["tool_call_counts"]["ghl_mcp"]["reads"] == 0
        assert audit["tool_call_counts"]["ghl_mcp"]["writes"] == 0


def test_memory_store_is_local_only(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    for packet_name, _, _ in TERMINAL_CASES:
        audit = project_workflow_run_audit(
            load_packet(packet_name), stage_a_context_for(packet_name)
        )
        store.persist(audit)
    assert store.creates == 4
    # No network markers in stored docs
    for run_id in list(store._docs):
        blob = json.dumps(store.get(run_id))
        assert "googleapis.com" not in blob
        assert "transcript_body" not in blob
