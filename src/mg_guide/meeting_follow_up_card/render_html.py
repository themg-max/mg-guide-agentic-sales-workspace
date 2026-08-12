"""Static HTML renderer for the card."""

from __future__ import annotations

from html import escape
from typing import Any, Dict, Iterable


def _li(values: Iterable[str]) -> str:
    items = [f"<li>{escape(str(v), quote=True)}</li>" for v in values if str(v)]
    if not items:
        return "<li>(none)</li>"
    return "".join(items)


def render_card_html(card: Dict[str, Any]) -> str:
    framing = card["framing"]
    policy = card["policy_display"]
    ui_integrity = card["ui_integrity"]
    crm = card["crm_display"]
    learning = card["learning"]
    brief = card["brief_display"]
    controls = card["controls"]
    intents = card["intents_display"]

    return (
        "<section class='mg-guide-card'>"
        f"<h1>{escape(framing['headline'], quote=True)}</h1>"
        f"<p><strong>State:</strong> {escape(card['card_state'], quote=True)}</p>"
        f"<p>{escape(framing['body'], quote=True)}</p>"
        f"<p><strong>Run:</strong> {escape(str(card['run']['run_id']), quote=True)}"
        f" ({escape(str(card['run']['packet_status']), quote=True)})</p>"
        f"<p><strong>Meeting:</strong> {escape(str(card['meeting']['title']), quote=True)}</p>"
        f"<p><strong>CRM:</strong> {escape(str(crm['resolution_status']), quote=True)}"
        f" | basis={escape(str(crm['match_basis']), quote=True)}"
        f" | candidates={escape(str(crm['candidate_count']), quote=True)}</p>"
        f"<p><strong>Current stage:</strong> {escape(str(crm['current_stage']), quote=True)}</p>"
        f"<p><strong>Summary:</strong> {escape(str(learning['summary']), quote=True)}</p>"
        f"<p><strong>Next step:</strong> {escape(str(learning['next_step_action']), quote=True)}"
        f" (owner: {escape(str(learning['next_step_owner']), quote=True)})</p>"
        "<h2>Needs</h2>"
        f"<ul>{_li(learning['needs'])}</ul>"
        "<h2>Objections</h2>"
        f"<ul>{_li(learning['objections'])}</ul>"
        "<h2>Policy reason codes</h2>"
        f"<ul>{_li(policy['reason_codes'])}</ul>"
        "<h2>UI integrity errors</h2>"
        f"<ul>{_li(ui_integrity['errors'])}</ul>"
        "<h2>Intents</h2>"
        f"<ul>{_li([intent['summary'] for intent in intents['note']] + [intent['summary'] for intent in intents['stage']])}</ul>"
        f"<p><strong>Brief:</strong> {escape(str(brief['headline']), quote=True)}</p>"
        f"<p><strong>Next action:</strong> {escape(str(brief['next_action']), quote=True)}</p>"
        "<h2>Allowed actions</h2>"
        f"<ul>{_li(controls['allowed_human_actions'])}</ul>"
        f"<p><strong>Card CRM changes made:</strong> {escape(str(not framing['no_crm_changes_made']), quote=True)}</p>"
        f"<p><strong>External effects:</strong> {escape(str(card['integrity']['external_effects']), quote=True)}</p>"
        "</section>"
    )

