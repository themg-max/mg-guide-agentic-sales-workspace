"""Packet and fixture models for meeting_follow_up_v1 Phase 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


TERMINAL_STATES = frozenset(
    {"completed", "completed_with_review", "blocked", "failed"}
)

ACTIVE_STATES = frozenset(
    {"received", "extracting", "resolving", "evaluating", "writing"}
)

ALL_STATES = ACTIVE_STATES | TERMINAL_STATES


@dataclass(frozen=True)
class PolicyThresholds:
    extraction_abort_threshold: float
    stage_transition_confidence_min: float


@dataclass
class RunRegistry:
    """In-process replay/idempotency registry."""

    terminal_runs: Dict[str, str] = field(default_factory=dict)

    def is_terminal(self, run_id: str) -> bool:
        return run_id in self.terminal_runs

    def mark_terminal(self, run_id: str, state: str) -> None:
        if state not in TERMINAL_STATES:
            raise ValueError(f"not a terminal state: {state}")
        self.terminal_runs[run_id] = state


def empty_extraction() -> Dict[str, Any]:
    return {
        "lifecycle": "not_attempted",
        "summary": None,
        "needs": [],
        "objections": [],
        "commitments": [],
        "next_step": None,
        "opportunity_signal": None,
    }


def empty_crm() -> Dict[str, Any]:
    return {
        "lifecycle": "not_attempted",
        "status": "not_attempted",
        "contact_id": None,
        "opportunity_id": None,
        "match_basis": "not_attempted",
        "candidate_count": 0,
        "current_stage": None,
    }


def empty_policy() -> Dict[str, Any]:
    return {
        "lifecycle": "not_attempted",
        "note_write": "not_attempted",
        "stage_write": "not_attempted",
        "reason_codes": [],
    }


def empty_mutations() -> Dict[str, Any]:
    return {
        "lifecycle": "not_attempted",
        "note": {"attempted": False, "verified": False, "record_id": None},
        "opportunity_stage": {
            "attempted": False,
            "from_stage": None,
            "to_stage": None,
            "verified": False,
        },
    }


def empty_intents() -> Dict[str, Any]:
    return {"note": [], "stage": []}


def empty_brief() -> Dict[str, Any]:
    return {
        "lifecycle": "not_attempted",
        "headline": None,
        "meeting_summary": None,
        "crm_actions": [],
        "next_action": None,
        "salesperson_attention_required": None,
    }


def base_packet(
    *,
    run_id: str,
    status: str,
    meeting: Dict[str, Any],
    participants: List[Dict[str, Any]],
    created_at: str,
    started_at: str,
) -> Dict[str, Any]:
    return {
        "schema": "meeting_follow_up_packet_v1",
        "run": {
            "run_id": run_id,
            "workflow": "meeting_follow_up_v1",
            "created_at": created_at,
            "status": status,
        },
        "meeting": meeting,
        "participants": participants,
        "extraction": empty_extraction(),
        "evidence": {"transcript_spans": [], "extraction_confidence": None},
        "crm_resolution": empty_crm(),
        "policy": empty_policy(),
        "mutations": empty_mutations(),
        "mutation_intents": empty_intents(),
        "brief": empty_brief(),
        "audit": {
            "started_at": started_at,
            "completed_at": None,
            "agents_used": [],
            "tools_used": [],
            "warnings": [],
            "final_disposition": "pending" if status in ACTIVE_STATES else None,
        },
        "external_effects": 0,
    }


@dataclass
class FixtureSidecar:
    fixture_id: str
    run_id: str
    meeting: Dict[str, Any]
    participants: List[Dict[str, Any]]
    extraction_result: Optional[Dict[str, Any]]
    extraction_confidence: Optional[float]
    evidence_references: List[Dict[str, str]]
    crm_resolution_stub: Dict[str, Any]
    policy_inputs: Dict[str, Any]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FixtureSidecar":
        required = [
            "fixture_id",
            "run_id",
            "meeting",
            "participants",
            "extraction_confidence",
            "evidence_references",
            "crm_resolution_stub",
            "policy_inputs",
        ]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"sidecar missing keys: {missing}")
        return FixtureSidecar(
            fixture_id=data["fixture_id"],
            run_id=data["run_id"],
            meeting=data["meeting"],
            participants=data["participants"],
            extraction_result=data.get("extraction_result"),
            extraction_confidence=data.get("extraction_confidence"),
            evidence_references=list(data.get("evidence_references") or []),
            crm_resolution_stub=dict(data["crm_resolution_stub"]),
            policy_inputs=dict(data["policy_inputs"]),
        )
