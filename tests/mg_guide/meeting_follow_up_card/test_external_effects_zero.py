from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from mg_guide.meeting_follow_up_card.cli import main
from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"


def _packet_validator() -> Draft202012Validator:
    schema = json.loads(
        (REPO_ROOT / "contracts" / "meeting_follow_up_packet.schema.json").read_text(
            encoding="utf-8"
        )
    )
    return Draft202012Validator(schema)


def _card_validator() -> Draft202012Validator:
    schema = json.loads(
        (REPO_ROOT / "contracts" / "mg_guide_meeting_follow_up_card.schema.json").read_text(
            encoding="utf-8"
        )
    )
    return Draft202012Validator(schema)


def test_all_nw006_packets_are_schema_valid_and_zero_effect():
    packet_validator = _packet_validator()
    card_validator = _card_validator()
    for packet_path in sorted(PACKET_DIR.glob("*.json")):
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        packet_validator.validate(packet)
        assert packet["external_effects"] == 0
        assert packet["mutations"]["note"]["attempted"] is False
        assert packet["mutations"]["note"]["verified"] is False
        assert packet["mutations"]["opportunity_stage"]["attempted"] is False
        assert packet["mutations"]["opportunity_stage"]["verified"] is False
        card = map_packet_to_card(packet)
        card_validator.validate(card)
        assert card["integrity"]["external_effects"] == 0


def test_cli_writes_to_stdout_only(capsys):
    packet_path = PACKET_DIR / "packet-success.completed.json"
    exit_code = main(["--packet", str(packet_path), "--format", "text"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "MG Guide Meeting Follow-Up Card" in captured.out
    assert captured.err == ""

