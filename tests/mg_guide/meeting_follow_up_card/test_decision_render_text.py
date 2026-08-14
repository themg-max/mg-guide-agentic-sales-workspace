from __future__ import annotations

import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_text import render_decision_card_text

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = REPO_ROOT / "fixtures" / "nw006" / "packets" / "packet-success.completed.json"


def test_render_decision_card_text_includes_required_fields_without_crm_ids():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    card = map_packet_to_decision_card(packet)
    rendered = render_decision_card_text(card)

    assert "Workflow status:" in rendered
    assert "Agent contributions:" in rendered
    assert "Meeting Context Agent" in rendered
    assert "Policy state:" in rendered
    assert "Policy reason code:" in rendered
    assert "Policy explanation:" in rendered
    assert "Human review required:" in rendered
    assert "External effects:" in rendered
    assert "Next action:" in rendered
    assert packet["crm_resolution"]["contact_id"] not in rendered
    assert packet["crm_resolution"]["opportunity_id"] not in rendered
    # Friendly label is rendered while the enum stays internal.
    assert "Review follow-up" in rendered
    assert "External effects: 0" in rendered


def test_render_decision_card_text_is_deterministic():
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    first = render_decision_card_text(map_packet_to_decision_card(packet))
    second = render_decision_card_text(
        map_packet_to_decision_card(json.loads(PACKET_PATH.read_text(encoding="utf-8")))
    )
    assert first == second
