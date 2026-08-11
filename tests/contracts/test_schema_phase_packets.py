from __future__ import annotations

import copy
from datetime import datetime, timezone

import pytest

from orchestration.models import base_packet

TS = "2026-08-11T12:00:00Z"
HASH = "a" * 64
MEETING = {
    "meeting_id": "m1",
    "occurred_at": TS,
    "source": "synthetic_demo",
    "transcript_hash": HASH,
}
PARTICIPANTS = [{"name": "A", "email": "a@example-demo.test", "phone": None, "role": "prospect"}]


def _pkt(status: str):
    return base_packet(
        run_id=f"run_{status}",
        status=status,
        meeting=MEETING,
        participants=PARTICIPANTS,
        created_at=TS,
        started_at=TS,
    )


@pytest.mark.parametrize(
    "status",
    [
        "received",
        "extracting",
        "resolving",
        "evaluating",
        "writing",
        "completed",
        "completed_with_review",
        "blocked",
        "failed",
    ],
)
def test_phase_valid_packets(packet_schema, status):
    pkt = _pkt(status)
    if status in {"completed", "completed_with_review", "blocked", "failed"}:
        pkt["audit"]["final_disposition"] = status
        pkt["audit"]["completed_at"] = TS
        if status == "completed":
            pkt["extraction"]["lifecycle"] = "complete"
            pkt["extraction"]["summary"] = "done"
            pkt["extraction"]["next_step"] = {"action": "x", "owner": "y", "target_date": None}
            pkt["extraction"]["opportunity_signal"] = {
                "recommended_stage": "discovery_complete",
                "rationale": "ok",
            }
            pkt["evidence"]["extraction_confidence"] = 0.95
            pkt["crm_resolution"] = {
                "lifecycle": "complete",
                "status": "matched",
                "contact_id": "c1",
                "opportunity_id": "o1",
                "match_basis": "email",
                "candidate_count": 1,
                "current_stage": "discovery_scheduled",
            }
            pkt["policy"] = {
                "lifecycle": "complete",
                "note_write": "allowed",
                "stage_write": "allowed",
                "reason_codes": [],
            }
            pkt["mutations"]["lifecycle"] = "intent_only"
            pkt["mutation_intents"] = {
                "note": [{"kind": "note", "status": "planned", "body_ref": "extraction.summary"}],
                "stage": [
                    {
                        "kind": "stage",
                        "status": "planned",
                        "from_stage": "discovery_scheduled",
                        "to_stage": "discovery_complete",
                    }
                ],
            }
            pkt["brief"] = {
                "lifecycle": "complete",
                "headline": "ok",
                "meeting_summary": "done",
                "crm_actions": ["plan_note_intent"],
                "next_action": "x",
                "salesperson_attention_required": False,
            }
    packet_schema.validate(pkt)


def test_active_run_cannot_require_terminal_disposition(packet_schema):
    pkt = _pkt("evaluating")
    pkt["audit"]["final_disposition"] = "completed"
    with pytest.raises(Exception):
        packet_schema.validate(pkt)


def test_terminal_requires_terminal_disposition(packet_schema):
    pkt = _pkt("blocked")
    pkt["audit"]["final_disposition"] = "pending"
    with pytest.raises(Exception):
        packet_schema.validate(pkt)


def test_yaml_contracts_parse(workflow_contract, failure_codes):
    assert workflow_contract["workflow"] == "meeting_follow_up_v1"
    thr = workflow_contract["policy_thresholds"]
    assert thr["extraction_abort_threshold"] != thr["stage_transition_confidence_min"]
    required = {
        "AMBIGUOUS_CONTACT",
        "CONTACT_NOT_FOUND",
        "OPPORTUNITY_NOT_FOUND",
        "LOW_EXTRACTION_CONFIDENCE",
        "STAGE_TRANSITION_NOT_ALLOWED",
        "GHL_TOOL_FAILURE",
        "GHL_WRITE_NOT_VERIFIED",
        "NOTE_WRITE_BLOCKED",
    }
    assert required.issubset(set(failure_codes["codes"]))


def test_external_effects_const_zero(packet_schema):
    pkt = _pkt("received")
    pkt["external_effects"] = 1
    with pytest.raises(Exception):
        packet_schema.validate(pkt)
