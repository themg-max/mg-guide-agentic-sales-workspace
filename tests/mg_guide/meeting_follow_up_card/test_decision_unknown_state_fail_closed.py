from __future__ import annotations

from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_html import render_decision_card_html
from mg_guide.meeting_follow_up_card.decision_render_text import render_decision_card_text


def test_unknown_state_fails_closed_without_defaulting_to_zero():
    packet = {
        "schema": "meeting_follow_up_packet_v1",
        "run": {"status": "unknown"},
        "policy": {"reason_codes": ["CUSTOM_REASON"]},
        "audit": {"agents_used": ["meeting_context_agent", "relationship_context_agent"]},
        "external_effects": None,
    }

    card = map_packet_to_decision_card(packet)

    assert card.workflow_status == "unknown"
    assert card.policy_state == "REVIEW_REQUIRED"
    assert card.policy_reason_code == "CUSTOM_REASON"
    assert card.policy_explanation == "An unrecognized workflow or policy state requires human review."
    assert card.next_action == "REVIEW_REQUIRED_UNKNOWN_STATE"
    assert card.human_review_required is True
    assert card.external_effects is None

    text = render_decision_card_text(card)
    html = render_decision_card_html(card)

    assert "REVIEW_REQUIRED" in text
    assert "REVIEW_REQUIRED_UNKNOWN_STATE" in text
    assert "An unrecognized workflow or policy state requires human review." in text
    assert "External effects: unknown" in text
    assert "REVIEW_REQUIRED" in html
    assert "REVIEW_REQUIRED_UNKNOWN_STATE" in html
    assert "External effects:" in html
    assert "unknown" in html
    assert "External effects: 0" not in text
    assert "External effects: 0" not in html
