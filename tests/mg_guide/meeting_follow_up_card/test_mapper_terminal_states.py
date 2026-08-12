from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"


def _load_packet(name: str):
    return json.loads((PACKET_DIR / name).read_text(encoding="utf-8"))


def _card_validator() -> Draft202012Validator:
    schema = json.loads(
        (REPO_ROOT / "contracts" / "mg_guide_meeting_follow_up_card.schema.json").read_text(
            encoding="utf-8"
        )
    )
    return Draft202012Validator(schema)


@pytest.mark.parametrize(
    ("fixture_name", "expected_state", "expected_tone"),
    [
        ("packet-success.completed.json", "completed", "success"),
        (
            "packet-stage-change-denied.completed_with_review.json",
            "completed_with_review",
            "review",
        ),
        ("packet-ambiguous-contact.blocked.json", "blocked", "blocked"),
        ("packet-ambiguous-opportunity.blocked.json", "blocked", "blocked"),
        ("packet-no-opportunity.blocked.json", "blocked", "blocked"),
        ("packet-insufficient-context.blocked.json", "blocked", "blocked"),
        ("packet-tool-failure.failed.json", "failed", "failed"),
    ],
)
def test_terminal_status_mapping(fixture_name: str, expected_state: str, expected_tone: str):
    packet = _load_packet(fixture_name)
    card = map_packet_to_card(packet)
    _card_validator().validate(card)
    assert card["card_state"] == expected_state
    assert card["framing"]["tone"] == expected_tone
    assert card["ui_integrity"]["errors"] == []
    assert card["integrity"]["external_effects"] == 0


def test_stage_change_denied_reason_code_passthrough():
    packet = _load_packet("packet-stage-change-denied.completed_with_review.json")
    card = map_packet_to_card(packet)
    assert card["policy_display"]["reason_codes"] == ["STAGE_TRANSITION_NOT_ALLOWED"]

