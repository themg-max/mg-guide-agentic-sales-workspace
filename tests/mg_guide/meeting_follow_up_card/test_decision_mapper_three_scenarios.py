from __future__ import annotations

import json
from pathlib import Path

import pytest

from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"


def _load_packet(name: str):
    return json.loads((PACKET_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("fixture_name", "expected_policy_state", "expected_reason_code", "expected_next_action", "expected_explanation", "expected_review"),
    [
        (
            "packet-success.completed.json",
            "allowed",
            "NONE",
            "REVIEW_FOLLOW_UP",
            "Policy evaluation completed with no blocking reason code.",
            False,
        ),
        (
            "packet-stage-change-denied.completed_with_review.json",
            "blocked",
            "STAGE_TRANSITION_NOT_ALLOWED",
            "KEEP_CURRENT_STAGE_AND_REVIEW",
            "The requested stage transition is not permitted by policy. The current stage must be preserved pending human review.",
            True,
        ),
        (
            "packet-ambiguous-contact.blocked.json",
            "blocked",
            "AMBIGUOUS_CONTACT",
            "RESOLVE_CONTACT",
            "The contact could not be matched unambiguously. Resolve the contact identity before proceeding.",
            True,
        ),
    ],
)
def test_decision_mapper_three_scenarios(
    fixture_name: str,
    expected_policy_state: str,
    expected_reason_code: str,
    expected_next_action: str,
    expected_explanation: str,
    expected_review: bool,
):
    packet = _load_packet(fixture_name)
    card = map_packet_to_decision_card(packet)

    assert card.workflow_status == packet["run"]["status"]
    assert "meeting_context_agent" in " ".join(card.agent_contributions)
    assert card.policy_state == expected_policy_state
    assert card.policy_reason_code == expected_reason_code
    assert card.policy_explanation == expected_explanation
    assert card.human_review_required is expected_review
    assert card.external_effects == 0
    assert card.next_action == expected_next_action
    assert "contact_demo" not in " ".join(card.agent_contributions)
    assert "opp_demo" not in " ".join(card.agent_contributions)
