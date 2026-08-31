"""CardService projection contract for SUCCESS and AMBIGUOUS_CONTACT (UX v2)."""

from __future__ import annotations

import json

from mg_guide.workspace_addon.cardservice_projection import (
    PRODUCT_ATTRIBUTION,
    PRODUCT_NAME,
    project_cardservice_home,
    project_cardservice_result,
    project_error_card,
)
from mg_guide.workspace_addon.local_adapter import (
    WorkspaceAddonLocalAdapter,
    flatten_visible_text,
)


def _compose_actions(card):
    actions = []
    for section in card.get("sections") or []:
        for widget in section.get("widgets") or []:
            if widget.get("action_type") == "compose":
                actions.append(widget)
    return actions


def test_home_branding_and_product_first_journey():
    home = project_cardservice_home()
    assert home["header"]["title"] == PRODUCT_NAME
    assert home["header"]["subtitle"] == PRODUCT_ATTRIBUTION
    text = flatten_visible_text(home)
    assert "MG Guide" in text
    assert "Powered by AI Rolodex" in text
    assert "Meeting Follow-Up" in text
    # Product value proposition first; harness wording is gone.
    assert (
        "Turn a completed meeting into relationship context, "
        "CRM-ready documentation, and a follow-up draft." in text
    )
    assert "Process Meeting Follow-Up" in text
    # Small competition truth marker, not the visual headline.
    assert "Competition mode" in text
    assert "Approved synthetic transcript" in text
    assert "governed CRM boundary" in text
    # Judge-only scenarios live in the secondary section.
    assert "Judge test scenarios" in text
    assert "Ambiguous contact" in text
    assert "Policy guardrail" in text
    # Forbidden / legacy labels.
    assert "Run Successful Follow-Up" not in text
    assert "Run SUCCESS" not in text
    assert "Run AMBIGUOUS_CONTACT" not in text
    assert "AI Rolodex – Limitless" not in text
    assert "Endurance Assistant" not in text

    primary, secondary = home["sections"]
    assert primary["header"] == "Meeting Follow-Up"
    primary_buttons = [w for w in primary["widgets"] if w["type"] == "button"]
    assert len(primary_buttons) == 1
    assert primary_buttons[0]["text"] == "Process Meeting Follow-Up"
    assert primary_buttons[0]["parameters"] == {"scenario": "SUCCESS"}
    assert primary_buttons[0]["style"] == "filled"
    assert secondary["header"] == "Judge test scenarios"
    secondary_scenarios = [
        w["parameters"]["scenario"]
        for w in secondary["widgets"]
        if w["type"] == "button"
    ]
    assert secondary_scenarios == ["AMBIGUOUS_CONTACT", "STAGE_CHANGE_DENIED"]


def test_success_scenario_completed_ux():
    card = WorkspaceAddonLocalAdapter().run_scenario("SUCCESS")
    assert card["card_id"] == "mg_guide_meeting_follow_up_result"
    assert card["ux_state"] == "COMPLETED"
    assert card["workflow_status"] == "completed"
    assert card["external_effects"] == 0
    assert card["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
    assert card["policy_decision"]["note_write"] == "allowed"
    assert card["policy_decision"]["stage_write"] == "allowed"
    assert card["policy_decision"]["reason_codes"] == []
    assert card["salesperson_next_step"]
    assert card["audit_status"]

    idx = card["visible_field_index"]
    assert idx["summary_present"] is True
    assert idx["relationship_status"] == "matched"
    assert idx["match_basis"] == "email"
    assert idx["candidate_count"] == 1
    assert idx["note_write"] == "allowed"
    assert idx["stage_write"] == "allowed"
    assert idx["salesperson_next_step_present"] is True
    assert idx["audit_status_present"] is True
    assert idx["stage_count"] == 6
    assert idx["stage_titles"][0] == "Meeting ready"
    assert idx["stage_titles"][5] in {
        "Meeting Follow-Up result",
        "Meeting Follow-Up",
    }
    assert idx["crm_note_status"] == "NOT_EXECUTED"
    assert idx["follow_up_draft_status"] == "READY"

    # Result-first ordering: outcome first, audit/integrity last.
    headers = [s["header"] for s in card["sections"]]
    assert headers == [
        "Follow-up ready",
        "Processing status",
        "What we heard",
        "Relationship",
        "CRM",
        "Follow-up draft",
        "Send follow-up",
        "Audit and integrity",
    ]

    text = flatten_visible_text(card)
    assert "MG Guide" in text
    assert "Powered by AI Rolodex" in text
    assert "FOLLOW-UP READY" in text
    assert "Processed" in text
    assert "Understood" in text
    assert "Matched" in text
    assert "UX_STATE" in text and "COMPLETED" in text
    assert "policy.note_write" in text
    assert "allowed" in text
    assert "Salesperson next step" in text
    assert "Audit status" in text
    assert "external_effects" in text
    assert "NOT_PERFORMED" in text
    assert "Taylor Morgan" in text or "matched" in text


def test_t_draft_05_needs_review_result_has_no_compose_action():
    for scenario in ("AMBIGUOUS_CONTACT", "STAGE_CHANGE_DENIED"):
        card = WorkspaceAddonLocalAdapter().run_scenario(scenario)
        assert card["ux_state"] == "NEEDS_REVIEW"
        assert _compose_actions(card) == []
        assert card["visible_field_index"]["compose_action_count"] == 0
        assert "Open Draft in Gmail" not in flatten_visible_text(card)


def test_t_draft_06_success_result_has_exactly_one_compose_action():
    card = WorkspaceAddonLocalAdapter().run_scenario("SUCCESS")
    actions = _compose_actions(card)
    assert len(actions) == 1
    action = actions[0]
    assert action["text"] == "Open Draft in Gmail"
    assert action["action"] == "createFollowUpDraft"
    assert action["composed_email_type"] == "STANDALONE_DRAFT"
    assert action["parameters"] == {"scenario": "SUCCESS"}
    assert card["visible_field_index"]["compose_action_count"] == 1


def test_t_draft_card_model_carries_safe_draft_projection():
    card = WorkspaceAddonLocalAdapter().run_scenario("SUCCESS")
    draft = card["follow_up_draft"]
    assert draft["status"] == "READY"
    assert draft["recipient_name"] == "Taylor Morgan"
    assert draft["recipient_email"] == "taylor.morgan@example-demo.test"
    assert draft["subject"] == "Follow-up: Taylor Morgan - Discovery Meeting"
    assert draft["source"] == "meeting_follow_up_v1"
    assert draft["requires_human_send"] is True
    assert "Hi Taylor," in draft["body_preview"]
    text = flatten_visible_text(card)
    assert "Follow-up draft" in text
    assert "Human review and send required" in text


def test_t_draft_15_no_raw_crm_ids_rendered_into_card_or_draft():
    card = WorkspaceAddonLocalAdapter().run_scenario("SUCCESS")
    serialized = json.dumps(card)
    assert "contact_demo_taylor_001" not in serialized
    assert "opp_demo_taylor_001" not in serialized
    assert "contact_demo" not in serialized
    assert "opp_demo" not in serialized


def test_t_draft_17_no_crm_verified_wording_in_competition_mode():
    for scenario in ("SUCCESS", "AMBIGUOUS_CONTACT", "STAGE_CHANGE_DENIED"):
        card = WorkspaceAddonLocalAdapter().run_scenario(scenario)
        assert card["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
        assert card["crm_note_status"]["state"] in {"NOT_EXECUTED", "BLOCKED"}
        text = flatten_visible_text(card)
        assert "CRM note verified" not in text

    success = WorkspaceAddonLocalAdapter().run_scenario("SUCCESS")
    assert (
        success["crm_note_status"]["display"]
        == "CRM note not executed in competition mode"
    )
    ambiguous = WorkspaceAddonLocalAdapter().run_scenario("AMBIGUOUS_CONTACT")
    assert ambiguous["crm_note_status"]["state"] == "BLOCKED"
    assert "No change performed" in ambiguous["crm_note_status"]["display"]


def test_t_draft_17b_forged_verified_claim_fails_closed():
    adapter = WorkspaceAddonLocalAdapter()
    code, body = adapter._post_demo("SUCCESS")
    assert code == 200
    body["ux_experience"]["crm_note_status"] = {
        "state": "VERIFIED",
        "display": "CRM note verified",
    }
    card = project_cardservice_result(body)
    # LIVE_CRM_EXECUTION stays NOT_PERFORMED, so VERIFIED fails closed.
    assert card["crm_note_status"]["state"] == "UNKNOWN"
    assert "CRM note verified" not in flatten_visible_text(card)


def test_ambiguous_contact_needs_review_ux():
    card = WorkspaceAddonLocalAdapter().run_scenario("AMBIGUOUS_CONTACT")
    assert card["ux_state"] == "NEEDS_REVIEW"
    assert card["workflow_status"] == "blocked"
    assert card["external_effects"] == 0
    assert card["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
    assert card["policy_decision"]["note_write"] == "not_attempted"
    assert card["policy_decision"]["stage_write"] == "not_attempted"
    assert card["policy_decision"]["reason_codes"] == ["AMBIGUOUS_CONTACT"]

    idx = card["visible_field_index"]
    assert idx["relationship_status"] == "ambiguous"
    assert idx["candidate_count"] == 2
    assert idx["note_write"] == "not_attempted"
    assert idx["stage_write"] == "not_attempted"
    assert "AMBIGUOUS_CONTACT" in idx["reason_codes"]
    assert idx["crm_note_status"] == "BLOCKED"
    assert idx["follow_up_draft_status"] == "NOT_AVAILABLE"
    assert idx["compose_action_count"] == 0

    headers = [s["header"] for s in card["sections"]]
    assert headers[0] == "Needs review"
    assert "Follow-up draft" not in headers
    assert "Send follow-up" not in headers
    assert headers[-1] == "Audit and integrity"

    text = flatten_visible_text(card)
    assert "NEEDS REVIEW" in text
    assert "NEEDS_REVIEW" in text
    assert "Ambiguous" in text
    assert "AMBIGUOUS_CONTACT" in text
    assert "not_attempted" in text
    assert "No change performed" in text
    assert "Not created" in text
    assert "Why:" in text
    assert "multiple candidates" in text
    assert "No CRM changes were made" in text
    assert "Resolve contact identity offline before any CRM write" in text
    assert "candidate_count" in text
    assert "2" in text
    # Must not rewrite not_attempted as blocked in policy fields.
    assert "policy.note_write" in text
    assert "blocked" in text  # workflow_status may be blocked
    # Ensure policy lines still say not_attempted
    assert "policy.note_write" in text and "not_attempted" in text


def test_invalid_scenario_error_card():
    card = WorkspaceAddonLocalAdapter().run_scenario("ATTACK")
    assert card["card_id"] == "mg_guide_error"
    assert card["error"]["code"] == "SCENARIO_BLOCKED"
    assert card["error"]["external_effects"] == 0
    assert card["error"]["crm_mutations_performed"] is False
    text = flatten_visible_text(card)
    assert "No CRM changes were made" in text


def test_error_card_codes():
    for code in (
        "AUTH_ERROR",
        "BACKEND_UNAVAILABLE",
        "INVALID_RESPONSE",
        "SCENARIO_BLOCKED",
    ):
        card = project_error_card(code, "x")
        assert card["error"]["code"] == code
        assert card["error"]["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
        assert "No CRM changes were made" in flatten_visible_text(card)


def test_project_result_requires_six_stages():
    card = project_cardservice_result(
        {
            "scenario": "SUCCESS",
            "workflow_status": "completed",
            "policy_decision": {},
            "demo_stages": [],
            "ux_experience": {"ux_state": "COMPLETED"},
            "external_effects": 0,
            "demo_truth": {"LIVE_CRM_EXECUTION": "NOT_PERFORMED"},
        }
    )
    assert card["error"]["code"] == "INVALID_RESPONSE"
