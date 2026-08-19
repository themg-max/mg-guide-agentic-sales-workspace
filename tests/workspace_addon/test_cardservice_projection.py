"""CardService projection contract for SUCCESS and AMBIGUOUS_CONTACT."""

from __future__ import annotations

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


def test_home_branding_and_primary_scenarios():
    home = project_cardservice_home()
    assert home["header"]["title"] == PRODUCT_NAME
    assert home["header"]["subtitle"] == PRODUCT_ATTRIBUTION
    text = flatten_visible_text(home)
    assert "MG Guide" in text
    assert "Powered by AI Rolodex" in text
    assert "Meeting Follow-Up" in text
    assert "Run SUCCESS" in text
    assert "Run AMBIGUOUS_CONTACT" in text
    assert "AI Rolodex – Limitless" not in text
    assert "Endurance Assistant" not in text


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

    text = flatten_visible_text(card)
    assert "MG Guide" in text
    assert "Powered by AI Rolodex" in text
    assert "UX_STATE" in text and "COMPLETED" in text
    assert "policy.note_write" in text
    assert "allowed" in text
    assert "Salesperson next step" in text
    assert "Audit status" in text
    assert "external_effects" in text
    assert "NOT_PERFORMED" in text
    assert "Taylor Morgan" in text or "matched" in text


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

    text = flatten_visible_text(card)
    assert "NEEDS_REVIEW" in text
    assert "AMBIGUOUS_CONTACT" in text
    assert "not_attempted" in text
    assert "No CRM changes were made" in text
    assert "Resolve contact identity before any CRM write" in text
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
