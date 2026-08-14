"""HTML rendering for the NW-007 decision card."""

from __future__ import annotations

from html import escape
from typing import Any

NEXT_ACTION_LABELS = {
    "REVIEW_FOLLOW_UP": "Review follow-up",
    "KEEP_CURRENT_STAGE_AND_REVIEW": "Keep current stage and review",
    "RESOLVE_CONTACT": "Resolve contact",
    "REVIEW_REQUIRED_UNKNOWN_STATE": "Review required (unrecognized state)",
}


def _render_li(items: Any) -> str:
    values = [str(item) for item in list(items or []) if str(item)]
    if not values:
        return "<li>(none)</li>"
    return "".join(f"<li>{escape(item, quote=True)}</li>" for item in values)


def _next_action_display(value: Any) -> str:
    if value in NEXT_ACTION_LABELS:
        return NEXT_ACTION_LABELS[value]
    return NEXT_ACTION_LABELS["REVIEW_REQUIRED_UNKNOWN_STATE"]


def _external_effects_display(value: Any) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return "unknown"


def render_decision_card_html(card: Any) -> str:
    if hasattr(card, "to_dict"):
        rendered = card.to_dict()
    else:
        rendered = dict(card)

    external_effects_display = _external_effects_display(
        rendered.get("external_effects")
    )
    if isinstance(rendered.get("agent_contributions"), list):
        agent_contributions = rendered["agent_contributions"]
    else:
        agent_contributions = []

    return (
        "<section class='mg-guide-decision-card'>"
        f"<h1>MG Guide Decision Card</h1>"
        f"<p><strong>Workflow status:</strong> {escape(str(rendered.get('workflow_status', 'unknown')), quote=True)}</p>"
        f"<p><strong>Agent contributions:</strong></p><ul>{_render_li(agent_contributions)}</ul>"
        f"<p><strong>Policy state:</strong> {escape(str(rendered.get('policy_state', 'unknown')), quote=True)}</p>"
        f"<p><strong>Policy reason code:</strong> {escape(str(rendered.get('policy_reason_code', 'unknown')), quote=True)}</p>"
        f"<p><strong>Policy explanation:</strong> {escape(str(rendered.get('policy_explanation', 'unknown')), quote=True)}</p>"
        f"<p><strong>Human review required:</strong> {escape(str(bool(rendered.get('human_review_required'))).lower(), quote=True)}</p>"
        f"<p><strong>External effects:</strong> {escape(external_effects_display, quote=True)}</p>"
        f"<p><strong>Next action:</strong> {escape(_next_action_display(rendered.get('next_action')), quote=True)}</p>"
        "</section>"
    )
