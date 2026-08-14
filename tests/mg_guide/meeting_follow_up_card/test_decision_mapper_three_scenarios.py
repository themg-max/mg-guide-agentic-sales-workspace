from __future__ import annotations

import json
from pathlib import Path

import pytest

from mg_guide.meeting_follow_up_card.decision_mapper import (
    POLICY_EXPLANATION_AMBIGUOUS_CONTACT,
    POLICY_EXPLANATION_STAGE_TRANSITION_NOT_ALLOWED,
    POLICY_EXPLANATION_SUCCESS_NO_BLOCKER,
    map_packet_to_decision_card,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKET_DIR = REPO_ROOT / "fixtures" / "nw006" / "packets"


def _load_packet(name: str):
    return json.loads((PACKET_DIR / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    (
        "fixture_name",
        "expected_policy_state",
        "expected_reason_code",
        "expected_next_action",
        "expected_explanation",
        "expected_review",
    ),
    [
        (
            "packet-success.completed.json",
            "ALLOWED",
            "NONE",
            "REVIEW_FOLLOW_UP",
            POLICY_EXPLANATION_SUCCESS_NO_BLOCKER,
            False,
        ),
        (
            "packet-stage-change-denied.completed_with_review.json",
            "BLOCKED",
            "STAGE_TRANSITION_NOT_ALLOWED",
            "KEEP_CURRENT_STAGE_AND_REVIEW",
            POLICY_EXPLANATION_STAGE_TRANSITION_NOT_ALLOWED,
            True,
        ),
        (
            "packet-ambiguous-contact.blocked.json",
            "BLOCKED",
            "AMBIGUOUS_CONTACT",
            "RESOLVE_CONTACT",
            POLICY_EXPLANATION_AMBIGUOUS_CONTACT,
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
    assert card.policy_state == expected_policy_state
    assert card.policy_reason_code == expected_reason_code
    assert card.policy_explanation == expected_explanation
    assert card.human_review_required is expected_review
    assert card.external_effects == 0
    assert card.next_action == expected_next_action


def test_agent_contributions_use_fixed_labels_only():
    packet = _load_packet("packet-success.completed.json")
    card = map_packet_to_decision_card(packet)

    assert "Meeting Context Agent" in card.agent_contributions
    assert "Relationship Context Agent" in card.agent_contributions
    assert "Follow-Up Planning Agent" in card.agent_contributions
    # Raw agent identifiers are not echoed into the human-facing labels.
    assert "meeting_context_agent" not in " ".join(card.agent_contributions)
    # Raw CRM identifiers never appear in contributions.
    assert packet["crm_resolution"]["contact_id"] not in " ".join(
        card.agent_contributions
    )
    assert packet["crm_resolution"]["opportunity_id"] not in " ".join(
        card.agent_contributions
    )


def test_unknown_agent_identifiers_are_not_printed():
    packet = _load_packet("packet-success.completed.json")
    packet["audit"]["agents_used"] = [
        "meeting_context_agent",
        "contact_demo_taylor_001",
        "unknown_custom_agent",
    ]
    card = map_packet_to_decision_card(packet)

    assert card.agent_contributions == ["Meeting Context Agent"]
    assert "unknown_custom_agent" not in " ".join(card.agent_contributions)
    assert "contact_demo_taylor_001" not in " ".join(card.agent_contributions)


def test_reason_codes_pass_through_unchanged_for_known_scenarios():
    packet = _load_packet("packet-stage-change-denied.completed_with_review.json")
    card = map_packet_to_decision_card(packet)
    assert card.policy_reason_code == "STAGE_TRANSITION_NOT_ALLOWED"
    assert packet["policy"]["reason_codes"] == ["STAGE_TRANSITION_NOT_ALLOWED"]
