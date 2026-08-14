from __future__ import annotations

import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_html import render_decision_card_html

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = (
    REPO_ROOT
    / "fixtures"
    / "nw006"
    / "packets"
    / "packet-stage-change-denied.completed_with_review.json"
)


def test_render_decision_card_html_includes_required_fields_without_crm_ids():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    card = map_packet_to_decision_card(packet)
    rendered = render_decision_card_html(card)

    assert "Workflow status:" in rendered
    assert "Agent contributions:" in rendered
    assert "Meeting Context Agent" in rendered
    assert "Policy state:" in rendered
    assert "Policy reason code:" in rendered
    assert "STAGE_TRANSITION_NOT_ALLOWED" in rendered
    assert "Policy explanation:" in rendered
    assert "Human review required:" in rendered
    assert "External effects:</strong> 0" in rendered
    assert "Next action:" in rendered
    assert packet["crm_resolution"]["contact_id"] not in rendered
    assert packet["crm_resolution"]["opportunity_id"] not in rendered
    # Friendly label is rendered while the enum stays internal.
    assert "Keep current stage and review" in rendered


def test_render_decision_card_html_escapes_untrusted_content():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    packet["run"]["status"] = "<script>alert('x')</script>"
    card = map_packet_to_decision_card(packet)
    rendered = render_decision_card_html(card)

    assert card.policy_state == "REVIEW_REQUIRED"
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
