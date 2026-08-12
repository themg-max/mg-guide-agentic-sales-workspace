from __future__ import annotations

import copy
import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card
from mg_guide.meeting_follow_up_card.render_html import render_card_html
from mg_guide.meeting_follow_up_card.render_text import render_card_text

REPO_ROOT = Path(__file__).resolve().parents[3]
SUCCESS_PACKET = (
    REPO_ROOT / "fixtures" / "nw006" / "packets" / "packet-success.completed.json"
)


def _load_success_packet():
    return json.loads(SUCCESS_PACKET.read_text(encoding="utf-8"))


def test_raw_crm_ids_not_rendered_in_text_or_html():
    packet = _load_success_packet()
    card = map_packet_to_card(packet)
    rendered_text = render_card_text(card)
    rendered_html = render_card_html(card)

    assert packet["crm_resolution"]["contact_id"] not in rendered_text
    assert packet["crm_resolution"]["contact_id"] not in rendered_html
    assert packet["crm_resolution"]["opportunity_id"] not in rendered_text
    assert packet["crm_resolution"]["opportunity_id"] not in rendered_html


def test_html_escaping_with_untrusted_content():
    packet = _load_success_packet()
    packet["participants"][0]["name"] = "<script>alert('x')</script>"
    packet["extraction"]["summary"] = "<img src=x onerror=alert(1)> & < > \" '"
    packet["brief"]["headline"] = "quote \" and ampersand & and <tag>"
    card = map_packet_to_card(packet)
    html = render_card_html(card)

    assert "<script>alert('x')</script>" not in html
    assert "<img src=x onerror=alert(1)>" not in html
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;" in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "&amp;" in html
    assert "&lt;" in html
    assert "&gt;" in html
    assert "&quot;" in html


def test_deterministic_repeatability_for_mapper_and_renderers():
    packet = _load_success_packet()
    card1 = map_packet_to_card(packet)
    card2 = map_packet_to_card(copy.deepcopy(packet))
    assert card1 == card2
    assert render_card_text(card1) == render_card_text(card2)
    assert render_card_html(card1) == render_card_html(card2)


def test_ui_errors_separate_from_policy_reason_codes():
    packet = _load_success_packet()
    packet["run"]["status"] = "unknown"
    packet["policy"]["reason_codes"] = ["STAGE_TRANSITION_NOT_ALLOWED"]
    card = map_packet_to_card(packet)
    assert "CARD_INPUT_INVALID" in card["ui_integrity"]["errors"]
    assert card["policy_display"]["reason_codes"] == ["STAGE_TRANSITION_NOT_ALLOWED"]
    assert "CARD_INPUT_INVALID" not in card["policy_display"]["reason_codes"]


def test_out_of_scope_mutation_packet_fails_closed():
    packet = _load_success_packet()
    packet["external_effects"] = 1
    packet["mutations"]["note"]["attempted"] = True
    card = map_packet_to_card(packet)
    assert card["card_state"] == "failed"
    assert "CARD_INPUT_OUT_OF_SCOPE" in card["ui_integrity"]["errors"]
    assert "CARD_INPUT_OUT_OF_SCOPE" not in card["policy_display"]["reason_codes"]

