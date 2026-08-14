from __future__ import annotations

import copy
import json
from pathlib import Path

from mg_guide.meeting_follow_up_card.decision_mapper import (
    POLICY_EXPLANATION_UNKNOWN,
    map_packet_to_decision_card,
)
from mg_guide.meeting_follow_up_card.decision_render_html import render_decision_card_html
from mg_guide.meeting_follow_up_card.decision_render_text import render_decision_card_text

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"
SUCCESS_PACKET = PACKET_DIR / "packet-success.completed.json"
AMBIGUOUS_PACKET = PACKET_DIR / "packet-ambiguous-contact.blocked.json"


def _load_success_packet():
    return json.loads(SUCCESS_PACKET.read_text(encoding="utf-8"))


def _assert_fail_closed(card) -> None:
    assert card.policy_state == "REVIEW_REQUIRED"
    assert card.human_review_required is True
    assert card.next_action == "REVIEW_REQUIRED_UNKNOWN_STATE"
    assert card.policy_explanation == POLICY_EXPLANATION_UNKNOWN


def test_unknown_status_with_empty_reasons_fails_closed():
    packet = _load_success_packet()
    packet["run"]["status"] = "unknown"
    packet["policy"]["reason_codes"] = []
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)


def test_completed_with_malformed_reason_codes_fails_closed():
    packet = _load_success_packet()
    packet["run"]["status"] = "completed"
    packet["policy"]["reason_codes"] = "STAGE_TRANSITION_NOT_ALLOWED"
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)


def test_completed_with_missing_policy_fails_closed():
    packet = _load_success_packet()
    packet["run"]["status"] = "completed"
    del packet["policy"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)


def test_inconsistent_state_reason_combination_fails_closed():
    packet = _load_success_packet()
    packet["run"]["status"] = "completed"
    packet["policy"]["reason_codes"] = ["STAGE_TRANSITION_NOT_ALLOWED"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)


def test_known_reason_plus_unknown_reason_fails_closed_and_does_not_reflect():
    packet = json.loads(AMBIGUOUS_PACKET.read_text(encoding="utf-8"))
    assert packet["run"]["status"] == "blocked"
    packet["policy"]["reason_codes"] = ["AMBIGUOUS_CONTACT", "TOTALLY_UNKNOWN_REASON"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)
    # The unsupported reason must not be reflected into judge-visible output.
    assert card.policy_reason_code == "NONE"
    assert "TOTALLY_UNKNOWN_REASON" not in render_decision_card_text(card)
    assert "TOTALLY_UNKNOWN_REASON" not in render_decision_card_html(card)


def test_success_tuple_with_missing_external_effects_fails_closed():
    packet = _load_success_packet()
    del packet["external_effects"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)
    assert card.external_effects is None
    text = render_decision_card_text(card)
    html = render_decision_card_html(card)
    assert "External effects: unknown" in text
    assert "External effects:</strong> unknown" in html
    assert "External effects: 0" not in text


def test_success_tuple_with_malformed_external_effects_fails_closed_and_does_not_leak():
    packet = _load_success_packet()
    packet["external_effects"] = {"contact_demo_taylor_001": ["nested", "data"]}
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)
    assert card.external_effects is None
    text = render_decision_card_text(card)
    html = render_decision_card_html(card)
    # Raw nested contents must never leak into rendered output.
    assert "contact_demo_taylor_001" not in text
    assert "contact_demo_taylor_001" not in html
    assert "nested" not in text
    assert "nested" not in html
    assert "External effects: unknown" in text


def test_unknown_reason_containing_crm_style_identifier_is_not_reflected():
    packet = _load_success_packet()
    packet["policy"]["reason_codes"] = ["contact_demo_taylor_001"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)
    text = render_decision_card_text(card)
    html = render_decision_card_html(card)
    assert "contact_demo_taylor_001" not in text
    assert "contact_demo_taylor_001" not in html


def test_unknown_reason_containing_html_markup_is_sanitized():
    packet = _load_success_packet()
    packet["policy"]["reason_codes"] = ["<script>alert('x')</script>"]
    card = map_packet_to_decision_card(packet)
    _assert_fail_closed(card)
    text = render_decision_card_text(card)
    html = render_decision_card_html(card)
    assert "<script>" not in text
    assert "<script>" not in html
    assert "alert" not in text
    assert "alert" not in html


def test_unknown_state_fail_closed_end_to_end():
    packet = {
        "schema": "meeting_follow_up_packet_v1",
        "run": {"status": "unknown"},
        "policy": {"reason_codes": ["CUSTOM_REASON"]},
        "audit": {"agents_used": ["meeting_context_agent", "relationship_context_agent"]},
        "external_effects": None,
    }

    card = map_packet_to_decision_card(packet)

    assert card.workflow_status == "unknown"
    _assert_fail_closed(card)
    assert card.external_effects is None
    assert card.agent_contributions == [
        "Meeting Context Agent",
        "Relationship Context Agent",
    ]

    text = render_decision_card_text(card)
    html = render_decision_card_html(card)

    assert "REVIEW_REQUIRED" in text
    assert "Review required (unrecognized state)" in text
    assert POLICY_EXPLANATION_UNKNOWN in text
    assert "External effects: unknown" in text
    assert "REVIEW_REQUIRED" in html
    assert "Review required (unrecognized state)" in html
    assert "External effects:</strong> unknown" in html
    assert "External effects: 0" not in text
    assert "External effects:</strong> 0" not in html
    # Unknown agent/status details never echo raw identifiers.
    assert "CUSTOM_REASON" not in text
    assert "CUSTOM_REASON" not in html
