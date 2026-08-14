"""Deterministic mapper for the NW-007 follow-up decision card."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from .decision_models import DecisionCard

REASON_EXPLANATIONS = {
    "STAGE_TRANSITION_NOT_ALLOWED": (
        "The requested stage transition is not permitted by policy. "
        "The current stage must be preserved pending human review."
    ),
    "AMBIGUOUS_CONTACT": (
        "The contact could not be matched unambiguously. "
        "Resolve the contact identity before proceeding."
    ),
    "SUCCESS_NO_BLOCKER": "Policy evaluation completed with no blocking reason code.",
}

NEXT_ACTIONS = {
    "SUCCESS": "REVIEW_FOLLOW_UP",
    "STAGE_TRANSITION_NOT_ALLOWED": "KEEP_CURRENT_STAGE_AND_REVIEW",
    "AMBIGUOUS_CONTACT": "RESOLVE_CONTACT",
}

UNKNOWN_EXPLANATION = "An unrecognized workflow or policy state requires human review."


def _normalize_reason_codes(raw: Any) -> List[str]:
    if not isinstance(raw, list):
        return []
    codes: List[str] = []
    for value in raw:
        if isinstance(value, str) and value:
            codes.append(value)
    return codes


def _agent_contributions(packet: Mapping[str, Any]) -> List[str]:
    audit = packet.get("audit") if isinstance(packet.get("audit"), Mapping) else {}
    agents = audit.get("agents_used") if isinstance(audit.get("agents_used"), list) else []
    seen = set()
    contributions: List[str] = []
    for agent in agents:
        if not isinstance(agent, str) or not agent or agent in seen:
            continue
        seen.add(agent)
        contributions.append(f"{agent}: packet-supported outcome: used")
    if not contributions:
        return ["no packet-supported agent contribution metadata"]
    return contributions


def _external_effects(packet: Mapping[str, Any]) -> Any:
    if "external_effects" in packet:
        return packet.get("external_effects")
    return None


def _policy_state_and_explanation(reason_codes: List[str]) -> Dict[str, str]:
    if not reason_codes:
        return {
            "policy_state": "allowed",
            "policy_reason_code": "NONE",
            "policy_explanation": REASON_EXPLANATIONS["SUCCESS_NO_BLOCKER"],
        }
    if "STAGE_TRANSITION_NOT_ALLOWED" in reason_codes:
        return {
            "policy_state": "blocked",
            "policy_reason_code": "STAGE_TRANSITION_NOT_ALLOWED",
            "policy_explanation": REASON_EXPLANATIONS["STAGE_TRANSITION_NOT_ALLOWED"],
        }
    if "AMBIGUOUS_CONTACT" in reason_codes:
        return {
            "policy_state": "blocked",
            "policy_reason_code": "AMBIGUOUS_CONTACT",
            "policy_explanation": REASON_EXPLANATIONS["AMBIGUOUS_CONTACT"],
        }
    first_reason = reason_codes[0]
    return {
        "policy_state": "REVIEW_REQUIRED",
        "policy_reason_code": first_reason,
        "policy_explanation": UNKNOWN_EXPLANATION,
    }


def _next_action(workflow_status: str, policy_state: str, reason_code: str) -> str:
    normalized_status = str(workflow_status or "unknown").strip().lower()
    if normalized_status == "completed" and policy_state == "allowed":
        return NEXT_ACTIONS["SUCCESS"]
    if reason_code == "STAGE_TRANSITION_NOT_ALLOWED":
        return NEXT_ACTIONS["STAGE_TRANSITION_NOT_ALLOWED"]
    if reason_code == "AMBIGUOUS_CONTACT":
        return NEXT_ACTIONS["AMBIGUOUS_CONTACT"]
    return "REVIEW_REQUIRED_UNKNOWN_STATE"


def map_packet_to_decision_card(packet: Mapping[str, Any]) -> DecisionCard:
    run = packet.get("run") if isinstance(packet.get("run"), Mapping) else {}
    policy = packet.get("policy") if isinstance(packet.get("policy"), Mapping) else {}
    workflow_status = str(run.get("status") or "unknown")
    reason_codes = _normalize_reason_codes(policy.get("reason_codes"))
    policy_details = _policy_state_and_explanation(reason_codes)
    policy_reason_code = policy_details["policy_reason_code"]
    policy_state = policy_details["policy_state"]
    explanation = policy_details["policy_explanation"]
    next_action = _next_action(workflow_status, policy_state, policy_reason_code)
    human_review_required = (
        policy_state in {"blocked", "REVIEW_REQUIRED"}
        or workflow_status in {"completed_with_review", "blocked", "failed", "unknown"}
    )

    return DecisionCard(
        workflow_status=workflow_status,
        agent_contributions=_agent_contributions(packet),
        policy_state=policy_state,
        policy_reason_code=policy_reason_code,
        policy_explanation=explanation,
        human_review_required=human_review_required,
        external_effects=_external_effects(packet),
        next_action=next_action,
    )
