"""Plain-text rendering for the NW-007 decision card."""

from __future__ import annotations

from typing import Any, Iterable


def _render_list(values: Iterable[str]) -> str:
    entries = [str(item) for item in values if str(item)]
    if not entries:
        return "(none)"
    return "; ".join(entries)


def render_decision_card_text(card: Any) -> str:
    if hasattr(card, "to_dict"):
        rendered = card.to_dict()
    else:
        rendered = dict(card)

    lines = [
        "MG Guide Decision Card",
        f"Workflow status: {rendered.get('workflow_status', 'unknown')}",
        f"Agent contributions: {_render_list(rendered.get('agent_contributions', []))}",
        f"Policy state: {rendered.get('policy_state', 'unknown')}",
        f"Policy reason code: {rendered.get('policy_reason_code', 'unknown')}",
        f"Policy explanation: {rendered.get('policy_explanation', 'unknown')}",
        f"Human review required: {str(bool(rendered.get('human_review_required'))).lower()}",
        f"External effects: {rendered.get('external_effects', 'unknown') if rendered.get('external_effects') is not None else 'unknown'}",
        f"Next action: {rendered.get('next_action', 'unknown')}",
    ]
    return "\n".join(lines)
