from __future__ import annotations

import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_html import render_decision_card_html

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = REPO_ROOT / "fixtures" / "nw006" / "packets" / "packet-stage-change-denied.completed_with_review.json"


def test_render_decision_card_html_includes_required_fields_without_crm_ids():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    card = map_packet_to_decision_card(packet)
    rendered = render_decision_card_html(card)

    assert "Workflow status:" in rendered
    assert "Policy state:" in rendered
    assert "Policy reason code:" in rendered
    assert "Policy explanation:" in rendered
    assert "Human review required:" in rendered
    assert "External effects:" in rendered
    assert "Next action:" in rendered
    assert "contact_demo_casey_001" not in rendered
    assert "opp_demo_casey_001" not in rendered
    assert "KEEP_CURRENT_STAGE_AND_REVIEW" in rendered
    assert "external_effects" not in rendered.lower()
    assert "&lt;script&gt;" not in rendered.lower()
