from __future__ import annotations

import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_non_terminal_maps_to_in_progress():
    packet = json.loads(
        (
            REPO_ROOT
            / "fixtures"
            / "nw006"
            / "packets"
            / "packet-non-terminal.evaluating.json"
        ).read_text(encoding="utf-8")
    )
    card = map_packet_to_card(packet)
    assert card["card_state"] == "in_progress"
    assert card["framing"]["tone"] == "in_progress"
    assert card["controls"]["allowed_human_actions"] == ["wait"]
    assert card["policy_display"]["reason_codes"] == []

