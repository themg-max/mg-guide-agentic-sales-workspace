"""Deterministic mapper for the NW-007 follow-up decision card.

Only exact packet-supported tuples are classified as named scenarios. Every
malformed, unsupported, or inconsistent combination fails closed.
"""

from __future__ import annotations

from typing import Any, List, Mapping

from .decision_models import DecisionCard

POLICY_EXPLANATION_STAGE_TRANSITION_NOT_ALLOWED = (
    "The requested stage transition is not permitted by policy. "
    "The current stage must be preserved pending human review."
)
POLICY_EXPLANATION_AMBIGUOUS_CONTACT = (
    "The contact could not be matched unambiguously. "
    "Resolve the contact identity before proceeding."
)
POLICY_EXPLANATION_SUCCESS_NO_BLOCKER = "Policy evaluation completed with no blocking reason code."
POLICY_EXPLANATION_UNKNOWN = "An unrecognized workflow or policy state requires human review."

NEXT_ACTION_ENUM = (
    "REVIEW_FOLLOW_UP",
    "KEEP_CURRENT_STAGE_AND_REVIEW",
    "RESOLVE_CONTACT",
    "REVIEW_REQUIRED_UNKNOWN_STATE",
)

KNOWN_REASON_CODES = ("STAGE_TRANSITION_NOT_ALLOWED", "AMBIGUOUS_CONTACT")
KNOWN_WORKFLOW_STATUSES = {
    "received",
    "extracting",
    "resolving",
    "evaluating",
    "writing",
    "completed",
    "completed_with_review",
    "blocked",
    "failed",
}
KNOWN_AGENT_LABELS = {
    "meeting_context_agent": "Meeting Context Agent",
    "relationship_context_agent": "Relationship Context Agent",
    "follow_up_planning_agent": "Follow-Up Planning Agent",
}

_SCENARIOS = {
    "SUCCESS": {
        "policy_state": "ALLOWED",
        "policy_reason_code": "NONE",
        "policy_explanation": POLICY_EXPLANATION_SUCCESS_NO_BLOCKER,
        "human_review_required": False,
        "next_action": "REVIEW_FOLLOW_UP",
    },
    "STAGE_CHANGE_DENIED": {
        "policy_state": "BLOCKED",
        "policy_reason_code": "STAGE_TRANSITION_NOT_ALLOWED",
        "policy_explanation": POLICY_EXPLANATION_STAGE_TRANSITION_NOT_ALLOWED,
        "human_review_required": True,
        "next_action": "KEEP_CURRENT_STAGE_AND_REVIEW",
    },
    "AMBIGUOUS_CONTACT": {
        "policy_state": "BLOCKED",
        "policy_reason_code": "AMBIGUOUS_CONTACT",
        "policy_explanation": POLICY_EXPLANATION_AMBIGUOUS_CONTACT,
        "human_review_required": True,
        "next_action": "RESOLVE_CONTACT",
    },
}

_UNKNOWN_OUTCOME = {
    "policy_state": "REVIEW_REQUIRED",
    "policy_reason_code": "NONE",
    "policy_explanation": POLICY_EXPLANATION_UNKNOWN,
    "human_review_required": True,
    "next_action": "REVIEW_REQUIRED_UNKNOWN_STATE",
}


def _normalize_workflow_status(status: Any) -> str:
    if isinstance(status, str) and status in KNOWN_WORKFLOW_STATUSES:
        return status
    return "unknown"


def _valid_reason_codes(policy: Any) -> Any:
    if not isinstance(policy, Mapping):
        return None
    if "reason_codes" not in policy:
        return None
    codes = policy.get("reason_codes")
    if not isinstance(codes, list):
        return None
    for code in codes:
        if not isinstance(code, str):
            return None
    return codes


def _valid_external_effects(packet: Mapping[str, Any]) -> bool:
    if not isinstance(packet, Mapping):
        return False
    if "external_effects" not in packet:
        return False
    value = packet.get("external_effects")
    return type(value) is int and value == 0


def _classify_scenario(workflow_status: Any, reason_codes: Any, external_effects_valid: bool) -> str:
    if _normalize_workflow_status(workflow_status) == "unknown":
        return "UNKNOWN"
    if reason_codes is None or not external_effects_valid:
        return "UNKNOWN"
    if any(code not in KNOWN_REASON_CODES for code in reason_codes):
        return "UNKNOWN"
    if workflow_status == "completed" and reason_codes == []:
        return "SUCCESS"
    if workflow_status == "completed_with_review" and reason_codes == ["STAGE_TRANSITION_NOT_ALLOWED"]:
        return "STAGE_CHANGE_DENIED"
    if workflow_status == "blocked" and reason_codes == ["AMBIGUOUS_CONTACT"]:
        return "AMBIGUOUS_CONTACT"
    return "UNKNOWN"


def _agent_contributions(packet: Mapping[str, Any]) -> List[str]:
    audit = packet.get("audit") if isinstance(packet.get("audit"), Mapping) else {}
    agents = audit.get("agents_used")
    if not isinstance(agents, list):
        return []
    contributions: List[str] = []
    seen = set()
    for agent in agents:
        if not isinstance(agent, str):
            continue
        if agent in KNOWN_AGENT_LABELS and agent not in seen:
            seen.add(agent)
            contributions.append(f"{KNOWN_AGENT_LABELS[agent]} — present in packet audit")
    return contributions


def map_packet_to_decision_card(packet: Mapping[str, Any]) -> DecisionCard:
    run = packet.get("run") if isinstance(packet.get("run"), Mapping) else {}
    policy = packet.get("policy")

    workflow_status = _normalize_workflow_status(run.get("status"))
    reason_codes = _valid_reason_codes(policy)
    external_effects_valid = _valid_external_effects(packet)
    scenario = _classify_scenario(run.get("status"), reason_codes, external_effects_valid)

    if scenario == "UNKNOWN":
        outcome = _UNKNOWN_OUTCOME
    else:
        outcome = _SCENARIOS[scenario]

    external_effects = packet.get("external_effects") if external_effects_valid else None

    return DecisionCard(
        workflow_status=workflow_status,
        agent_contributions=_agent_contributions(packet),
        policy_state=outcome["policy_state"],
        policy_reason_code=outcome["policy_reason_code"],
        policy_explanation=outcome["policy_explanation"],
        human_review_required=outcome["human_review_required"],
        external_effects=external_effects,
        next_action=outcome["next_action"],
    )
