"""Deterministic policy evaluation for meeting_follow_up_v1 Phase 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .state_machine import StateMachine


@dataclass
class PolicyDecision:
    note_write: str  # allowed | blocked
    stage_write: str  # allowed | blocked | approval_required
    reason_codes: List[str] = field(default_factory=list)
    note_intent: Optional[Dict[str, Any]] = None
    stage_intent: Optional[Dict[str, Any]] = None

    @property
    def any_permitted(self) -> bool:
        return self.note_write == "allowed" or self.stage_write == "allowed"


def evaluate_policy(
    sm: StateMachine,
    *,
    extraction_confidence: float,
    crm: Dict[str, Any],
    policy_inputs: Dict[str, Any],
    extraction_result: Optional[Dict[str, Any]],
) -> PolicyDecision:
    """Evaluate note/stage policy without external side effects."""
    reasons: List[str] = []

    force_note_denied = bool(policy_inputs.get("force_note_denied", False))
    force_stage_denied = bool(policy_inputs.get("force_stage_denied", False))
    note_requested = bool(policy_inputs.get("note_write_request", True))
    stage_requested = bool(policy_inputs.get("stage_write_request", False))

    recommended = None
    if extraction_result and extraction_result.get("opportunity_signal"):
        recommended = extraction_result["opportunity_signal"].get(
            "recommended_stage"
        )
    recommended = policy_inputs.get("recommended_stage", recommended)
    current_stage = crm.get("current_stage")

    # Note policy — explicit denial supported.
    if force_note_denied or not note_requested:
        note_write = "blocked"
        if force_note_denied:
            reasons.append("NOTE_WRITE_BLOCKED")
        note_intent = {
            "kind": "note",
            "status": "denied",
            "body_ref": None,
        }
    else:
        note_write = "allowed"
        note_intent = {
            "kind": "note",
            "status": "planned",
            "body_ref": "extraction.summary",
        }

    # Stage policy — distinct confidence threshold from extraction abort.
    stage_write = "blocked"
    stage_intent = None
    if stage_requested and not force_stage_denied:
        if extraction_confidence < sm.stage_transition_confidence_min:
            stage_write = "blocked"
            reasons.append("STAGE_TRANSITION_NOT_ALLOWED")
            stage_intent = {
                "kind": "stage",
                "status": "denied",
                "from_stage": current_stage,
                "to_stage": recommended,
            }
        elif (
            current_stage == "discovery_scheduled"
            and recommended == "discovery_complete"
            and crm.get("status") == "matched"
            and crm.get("match_basis") in {"email", "phone"}
        ):
            stage_write = "allowed"
            stage_intent = {
                "kind": "stage",
                "status": "planned",
                "from_stage": current_stage,
                "to_stage": recommended,
            }
        else:
            stage_write = "blocked"
            reasons.append("STAGE_TRANSITION_NOT_ALLOWED")
            stage_intent = {
                "kind": "stage",
                "status": "denied",
                "from_stage": current_stage,
                "to_stage": recommended,
            }
    elif stage_requested and force_stage_denied:
        stage_write = "blocked"
        reasons.append("STAGE_TRANSITION_NOT_ALLOWED")
        stage_intent = {
            "kind": "stage",
            "status": "denied",
            "from_stage": current_stage,
            "to_stage": recommended,
        }

    # Deduplicate reason codes while preserving order.
    seen = set()
    ordered: List[str] = []
    for code in reasons:
        if code not in seen:
            seen.add(code)
            ordered.append(code)

    return PolicyDecision(
        note_write=note_write,
        stage_write=stage_write,
        reason_codes=ordered,
        note_intent=note_intent if note_requested or force_note_denied else None,
        stage_intent=stage_intent,
    )


def bound_intents(
    decision: PolicyDecision, *, max_note: int = 1, max_stage: int = 1
) -> Dict[str, List[Dict[str, Any]]]:
    notes: List[Dict[str, Any]] = []
    stages: List[Dict[str, Any]] = []
    if decision.note_intent and decision.note_write == "allowed":
        notes.append(decision.note_intent)
    if decision.stage_intent and decision.stage_write == "allowed":
        stages.append(decision.stage_intent)
    if len(notes) > max_note:
        raise ValueError("note intent cardinality exceeded")
    if len(stages) > max_stage:
        raise ValueError("stage intent cardinality exceeded")
    return {"note": notes[:max_note], "stage": stages[:max_stage]}
