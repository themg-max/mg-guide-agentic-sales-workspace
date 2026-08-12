from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"
EXPECTED_DIR = REPO_ROOT / "fixtures" / "nw006" / "expected"

SCENARIOS = [
    ("packet-success.completed.json", "card-success.json"),
    (
        "packet-stage-change-denied.completed_with_review.json",
        "card-stage-change-denied.json",
    ),
    ("packet-ambiguous-contact.blocked.json", "card-ambiguous-contact.json"),
    ("packet-ambiguous-opportunity.blocked.json", "card-ambiguous-opportunity.json"),
    ("packet-no-opportunity.blocked.json", "card-no-opportunity.json"),
    ("packet-insufficient-context.blocked.json", "card-insufficient-context.json"),
    ("packet-tool-failure.failed.json", "card-tool-failure.json"),
    ("packet-non-terminal.evaluating.json", "card-non-terminal.json"),
]


def _card_validator() -> Draft202012Validator:
    schema = json.loads(
        (
            REPO_ROOT / "contracts" / "mg_guide_meeting_follow_up_card.schema.json"
        ).read_text(encoding="utf-8")
    )
    return Draft202012Validator(schema)


@pytest.mark.parametrize(("packet_name", "expected_name"), SCENARIOS)
def test_expected_card_viewmodel_snapshots(packet_name: str, expected_name: str):
    packet = json.loads((PACKET_DIR / packet_name).read_text(encoding="utf-8"))
    expected = json.loads((EXPECTED_DIR / expected_name).read_text(encoding="utf-8"))
    card = map_packet_to_card(packet)
    _card_validator().validate(card)
    assert card == expected
