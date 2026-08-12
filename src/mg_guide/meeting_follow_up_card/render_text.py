"""Plain-text card chrome renderer."""

from __future__ import annotations

from typing import Any, Dict, Iterable


def _render_list(values: Iterable[str]) -> str:
    entries = [str(v) for v in values if str(v)]
    if not entries:
        return "(none)"
    return "; ".join(entries)


def render_card_text(card: Dict[str, Any]) -> str:
    framing = card["framing"]
    policy = card["policy_display"]
    ui_integrity = card["ui_integrity"]
    crm = card["crm_display"]
    learning = card["learning"]
    intents = card["intents_display"]
    brief = card["brief_display"]
    controls = card["controls"]

    lines = [
        "MG Guide Meeting Follow-Up Card",
        f"State: {card['card_state']}",
        f"Headline: {framing['headline']}",
        f"Body: {framing['body']}",
        f"Run: {card['run']['run_id']} ({card['run']['packet_status']})",
        f"Meeting: {card['meeting']['title']}",
        f"CRM resolution: {crm['resolution_status']} | basis={crm['match_basis']} | candidates={crm['candidate_count']}",
        f"Current stage: {crm['current_stage']}",
        f"Learning summary: {learning['summary']}",
        f"Needs: {_render_list(learning['needs'])}",
        f"Objections: {_render_list(learning['objections'])}",
        f"Next step: {learning['next_step_action']} (owner: {learning['next_step_owner']})",
        f"Policy note_write={policy['note_write']} stage_write={policy['stage_write']}",
        f"Policy reason codes: {_render_list(policy['reason_codes'])}",
        f"UI errors: {_render_list(ui_integrity['errors'])}",
        f"Brief headline: {brief['headline']}",
        f"Brief next action: {brief['next_action']}",
        f"Brief CRM actions: {_render_list(brief['crm_actions'])}",
        f"Attention required: {brief['salesperson_attention_required']}",
        f"Allowed actions: {_render_list(controls['allowed_human_actions'])}",
        f"No CRM changes made: {framing['no_crm_changes_made']}",
        f"External effects: {card['integrity']['external_effects']}",
    ]

    for intent in intents["note"]:
        lines.append(f"Note intent: {intent['summary']}")
    for intent in intents["stage"]:
        lines.append(f"Stage intent: {intent['summary']}")

    return "\n".join(lines)

