"""Plain-text rendering for the NW-007 decision card."""

from __future__ import annotations

from typing import Any, Iterable

NEXT_ACTION_LABELS = {
    "REVIEW_FOLLOW_UP": "Review follow-up",
    "KEEP_CURRENT_STAGE_AND_REVIEW": "Keep current stage and review",
    "RESOLVE_CONTACT": "Resolve contact",
    "REVIEW_REQUIRED_UNKNOWN_STATE": "Review required (unrecognized state)",
}
SUPPORTED_WORKFLOW_STATUSES = {
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


def _render_list(values: Iterable[str]) -> str:
    entries = [str(item) for item in values if str(item)]
    if not entries:
        return "(none)"
    return "; ".join(entries)


def _safe_workflow_status(value: Any) -> str:
    if isinstance(value, str) and value in SUPPORTED_WORKFLOW_STATUSES:
        return value
    return "unknown"


def _next_action_display(value: Any) -> str:
    if value in NEXT_ACTION_LABELS:
        return NEXT_ACTION_LABELS[value]
    return NEXT_ACTION_LABELS["REVIEW_REQUIRED_UNKNOWN_STATE"]


def _external_effects_display(value: Any) -> str:
    if type(value) is int and value == 0:
        return "0"
    return "unknown"


def render_decision_card_text(card: Any) -> str:
    if hasattr(card, "to_dict"):
        rendered = card.to_dict()
    else:
        rendered = dict(card)

    lines = [
        "MG Guide Decision Card",
        f"Workflow status: {_safe_workflow_status(rendered.get('workflow_status'))}",
        f"Agent contributions: {_render_list(rendered.get('agent_contributions', []))}",
        f"Policy state: {rendered.get('policy_state', 'unknown')}",
        f"Policy reason code: {rendered.get('policy_reason_code', 'unknown')}",
        f"Policy explanation: {rendered.get('policy_explanation', 'unknown')}",
        f"Human review required: {str(bool(rendered.get('human_review_required'))).lower()}",
        f"External effects: {_external_effects_display(rendered.get('external_effects'))}",
        f"Next action: {_next_action_display(rendered.get('next_action'))}",
    ]
    return "\n".join(lines)
