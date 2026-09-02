"""Unit tests for six-stage demo projection and salesperson UX experience."""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest

from mg_guide.judge_surface.demo_stages import (
    UX_COMPLETED,
    UX_NEEDS_REVIEW,
    project_demo_payload,
    project_demo_stages,
    project_ux_experience,
)
from mg_guide.judge_surface.render_demo_stages import (
    render_demo_stages_html,
    render_demo_stages_text,
)
from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card
from orchestration.runner import WorkflowRunner

REPO_ROOT = Path(__file__).resolve().parents[2]
STAGE_TITLES = [
    "Meeting ready",
    "Meeting Context",
    "Relationship Resolution",
    "Follow-Up Planning",
    "Policy Evaluation",
    "Meeting Follow-Up result card",
]
def _run(name: str):
    sidecar = REPO_ROOT / "fixtures" / name
    result = WorkflowRunner().run_fixture(sidecar)
    assert result.validation_ok, result.error
    card = map_packet_to_card(result.packet)
    return result, card


def test_success_demo_stages_field_contract():
    result, card = _run("transcript-success.expected.json")
    stages = project_demo_stages(
        result.packet, card, workflow_status=result.final_state
    )
    assert [s["title"] for s in stages] == STAGE_TITLES
    assert len(stages) == 6

    meeting_ready = stages[0]["evidence"]
    participants = meeting_ready["participants"]
    prospect = next(p for p in participants if p["role"] == "prospect")
    assert prospect["name"] == "Taylor Morgan"
    assert prospect["email"] == "taylor.morgan@example-demo.test"
    assert meeting_ready["source"] == "synthetic_demo"

    context = stages[1]["evidence"]
    assert context["extraction_confidence"] == 0.95
    assert context["summary"]

    crm = stages[2]["evidence"]
    assert crm["match_basis"] == "email"
    assert crm["candidate_count"] == 1
    assert crm["current_stage"] == "discovery_scheduled"
    assert crm["resolution_status"] == "matched"

    planning = stages[3]["evidence"]
    stage_summaries = " ".join(i["summary"] or "" for i in planning["stage_intents"])
    assert "discovery_scheduled" in stage_summaries
    assert "discovery_complete" in stage_summaries
    assert planning["note_execution_attempted"] is False
    assert planning["stage_execution_attempted"] is False

    policy = stages[4]["evidence"]
    assert policy["note_write"] == "allowed"
    assert policy["stage_write"] == "allowed"
    assert policy["reason_codes"] == []

    result_card = stages[5]["evidence"]
    assert result_card["card_state"] == "completed"
    assert result_card["framing"]["no_crm_changes_made"] is True
    assert result_card["integrity"]["external_effects"] == 0
    assert result_card["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"


def test_ambiguous_demo_stages_field_contract():
    result, card = _run("transcript-ambiguous-contact.expected.json")
    stages = project_demo_stages(
        result.packet, card, workflow_status=result.final_state
    )
    assert [s["title"] for s in stages] == STAGE_TITLES

    prospect = next(
        p for p in stages[0]["evidence"]["participants"] if p["role"] == "prospect"
    )
    assert prospect["name"] == "Jordan Lee"

    crm = stages[2]["evidence"]
    assert crm["resolution_status"] == "ambiguous"
    assert crm["candidate_count"] == 2

    planning = stages[3]["evidence"]
    assert planning["note_intents"] == []
    assert planning["stage_intents"] == []
    assert planning["note_execution_attempted"] is False
    assert planning["stage_execution_attempted"] is False

    policy = stages[4]["evidence"]
    assert policy["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    # Live runner truth — not NW-006 snapshot blocked enums.
    assert policy["note_write"] == "not_attempted"
    assert policy["stage_write"] == "not_attempted"

    result_card = stages[5]["evidence"]
    assert result_card["card_state"] == "blocked"
    assert result_card["workflow_status"] == "blocked"
    assert result_card["final_disposition"] == "blocked"
    assert result_card["integrity"]["external_effects"] == 0
    assert "escalate_offline" in result_card["controls"]["allowed_human_actions"]


def test_success_ux_experience_completed_state():
    result, card = _run("transcript-success.expected.json")
    ux = project_ux_experience(result.packet, card, workflow_status=result.final_state)
    assert ux["ux_state"] == UX_COMPLETED
    assert ux["meeting_context"]["prospect"]["name"] == "Taylor Morgan"
    assert ux["meeting_context"]["prospect"]["email"] == "taylor.morgan@example-demo.test"
    assert ux["summary"]
    assert ux["relationship_context"]["contact_resolved"] is True
    assert ux["relationship_context"]["match_basis"] == "email"
    assert ux["proposed_follow_up"]["label"] == "proposed_intents_only"
    assert ux["proposed_follow_up"]["execution_attempted"]["note"] is False
    assert ux["policy_decision"]["note_write"] == "allowed"
    assert ux["policy_decision"]["stage_write"] == "allowed"
    assert ux["permitted_action_result"]["external_effects"] == 0
    assert ux["permitted_action_result"]["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
    assert ux["permitted_action_result"]["crm_changes_made"] is False
    assert ux["audit_status"]["recorded"] is True
    assert ux["audit_status"]["final_disposition"] == "completed"
    assert "audit" in ux["audit_status"]["display"].lower() or "agents" in ux["audit_status"]["display"]
    assert ux["salesperson_next_step"]
    assert "completed" in ux
    assert ux["completed"]["policy_pass"] is True
    assert ux["extraction_confidence"] == 0.95


def test_ambiguous_ux_experience_needs_review_state():
    result, card = _run("transcript-ambiguous-contact.expected.json")
    ux = project_ux_experience(result.packet, card, workflow_status=result.final_state)
    assert ux["ux_state"] == UX_NEEDS_REVIEW
    needs = ux["needs_review"]
    assert "candidate" in needs["reason"].lower() or "AMBIGUOUS" in needs["reason"]
    assert needs["zero_unauthorized_effects"] is True
    assert "No CRM changes were made" in needs["zero_unauthorized_effects_message"]
    assert needs["block_context"]["candidate_count"] == 2
    assert needs["block_context"]["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    assert needs["block_context"]["note_write"] == "not_attempted"
    assert needs["block_context"]["stage_write"] == "not_attempted"
    assert needs["block_context"]["workflow_status"] == "blocked"
    assert needs["explicit_next_action"]
    assert "Resolve contact" in needs["explicit_next_action"] or "offline" in needs["explicit_next_action"].lower()
    assert ux["policy_decision"]["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    assert ux["salesperson_next_step"]
    assert ux["audit_status"]["final_disposition"] == "blocked"
    assert ux["permitted_action_result"]["external_effects"] == 0


def test_stage_change_denied_ux_is_needs_review():
    result, card = _run("transcript-no-stage-change.expected.json")
    ux = project_ux_experience(result.packet, card, workflow_status=result.final_state)
    assert ux["ux_state"] == UX_NEEDS_REVIEW
    assert "STAGE_TRANSITION_NOT_ALLOWED" in ux["policy_decision"]["reason_codes"]
    assert ux["permitted_action_result"]["external_effects"] == 0
    assert ux["salesperson_next_step"]


def _collect_keys(value, found=None):
    if found is None:
        found = set()
    if isinstance(value, dict):
        for key, child in value.items():
            found.add(str(key).lower())
            _collect_keys(child, found)
    elif isinstance(value, list):
        for child in value:
            _collect_keys(child, found)
    return found


def test_demo_stages_have_no_reasoning_payload():
    result, card = _run("transcript-success.expected.json")
    payload = project_demo_payload(
        result.packet, card, workflow_status=result.final_state
    )
    keys = _collect_keys(payload)
    # Banner may mention PRIVATE_MODEL_REASONING_DISPLAYED=false; that is a
    # safety flag, not a reasoning payload. Forbid reasoning content keys.
    for token in ("chain_of_thought", "scratchpad", "private_thoughts"):
        assert token not in keys
    assert "reasoning" not in keys
    # Values must not embed free-form private reasoning blobs.
    serialized = json.dumps(payload, sort_keys=True).lower()
    assert "chain_of_thought" not in serialized
    assert "scratchpad" not in serialized
    assert "private_thoughts" not in serialized


def test_demo_stages_projection_is_pure():
    src = (
        REPO_ROOT / "src" / "mg_guide" / "judge_surface" / "demo_stages.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(src)
    imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    forbidden_prefixes = (
        "integrations",
        "google",
        "agents",
        "orchestration",
        "firebase",
        "firestore",
    )
    for name in imports:
        assert not any(name.startswith(p) for p in forbidden_prefixes), name

    result, card = _run("transcript-success.expected.json")
    payload = project_demo_payload(
        result.packet, card, workflow_status=result.final_state
    )
    assert payload["demo_truth"]["EXTERNAL_EFFECTS"] == 0
    assert payload["ux_experience"]["permitted_action_result"]["external_effects"] == 0


def test_render_stages_html_contains_required_tokens():
    result, card = _run("transcript-success.expected.json")
    payload = project_demo_payload(
        result.packet, card, workflow_status=result.final_state
    )
    html = render_demo_stages_html(
        payload["demo_stages"],
        payload["demo_truth"],
        ux_experience=payload["ux_experience"],
    )
    for title in STAGE_TITLES:
        assert title in html
    assert "LIVE_CRM_EXECUTION=NOT_PERFORMED" in html or "LIVE_CRM_EXECUTION</strong>=NOT_PERFORMED" in html
    assert "COMPLETED" in html
    assert "Salesperson next step" in html
    assert "Policy decision" in html
    assert "Audit status" in html
    assert "Taylor Morgan" in html
    assert "<script>" not in html.lower().replace("&lt;script&gt;", "")


def test_render_stages_html_ambiguous_fail_closed():
    result, card = _run("transcript-ambiguous-contact.expected.json")
    payload = project_demo_payload(
        result.packet, card, workflow_status=result.final_state
    )
    html = render_demo_stages_html(
        payload["demo_stages"],
        payload["demo_truth"],
        ux_experience=payload["ux_experience"],
    )
    assert "Jordan Lee" in html
    assert "AMBIGUOUS_CONTACT" in html
    assert "NEEDS_REVIEW" in html
    assert "No CRM changes were made" in html
    assert "blocked" in html
    text = render_demo_stages_text(
        payload["demo_stages"],
        payload["demo_truth"],
        ux_experience=payload["ux_experience"],
    )
    assert "NEEDS_REVIEW" in text
    assert "EXTERNAL_EFFECTS=0" in text


# --- T-DRAFT: deterministic follow-up draft projection (UX v2) ---


def _ux_for(fixture_name: str):
    result, card = _run(fixture_name)
    ux = project_ux_experience(
        result.packet, card, workflow_status=result.final_state
    )
    return ux, result, card


def test_t_draft_01_success_projects_safe_follow_up_draft():
    ux, _, _ = _ux_for("transcript-success.expected.json")
    draft = ux["follow_up_draft"]
    assert draft["status"] == "READY"
    assert draft["recipient_name"] == "Taylor Morgan"
    assert draft["recipient_email"] == "taylor.morgan@example-demo.test"
    assert draft["subject"] == "Following up on our conversation"
    assert draft["source"] == "meeting_follow_up_v1"
    assert draft["requires_human_send"] is True
    body = draft["body_text"]
    assert body.startswith("Hi Taylor,")
    assert "Thank you again for your time today." in body
    assert "retirement income planning" in body
    assert "maintaining liquidity" in body
    assert "sixty-day timeline" in body
    assert "prepare for our recommendation review" in body
    assert "(owner:" not in body
    assert "Next step:" not in body
    assert "Please let me know if I missed anything" not in body
    assert body.rstrip().endswith("Alex")


def test_t_draft_02_recipient_only_from_resolved_participant_context():
    ux, result, _ = _ux_for("transcript-success.expected.json")
    draft = ux["follow_up_draft"]
    prospect = next(
        p for p in result.packet["participants"] if p["role"] == "prospect"
    )
    assert draft["recipient_email"] == prospect["email"]
    assert draft["recipient_name"] == prospect["name"]
    # The agent participant is never the recipient.
    agent = next(p for p in result.packet["participants"] if p["role"] == "agent")
    assert draft["recipient_email"] != agent["email"]


def test_t_draft_03_missing_recipient_means_not_available():
    result, card = _run("transcript-success.expected.json")
    packet = copy.deepcopy(result.packet)
    for participant in packet["participants"]:
        if participant.get("role") == "prospect":
            participant["email"] = ""
    ux = project_ux_experience(
        packet, card, workflow_status=result.final_state
    )
    assert ux["ux_state"] == UX_COMPLETED
    draft = ux["follow_up_draft"]
    assert draft["status"] == "NOT_AVAILABLE"
    assert draft["recipient_email"] is None
    assert draft["subject"] is None
    assert draft["body_text"] is None
    assert draft["requires_human_send"] is True


def test_t_draft_04_ambiguous_contact_means_not_available():
    ux, result, _ = _ux_for("transcript-ambiguous-contact.expected.json")
    assert ux["ux_state"] == UX_NEEDS_REVIEW
    draft = ux["follow_up_draft"]
    assert draft["status"] == "NOT_AVAILABLE"
    assert draft["recipient_name"] is None
    assert draft["recipient_email"] is None
    assert draft["subject"] is None
    assert draft["body_text"] is None
    assert draft["requires_human_send"] is True
    assert ux["policy_decision"]["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    assert result.external_effects == 0


def test_t_draft_15_no_raw_crm_ids_in_draft():
    ux, result, _ = _ux_for("transcript-success.expected.json")
    serialized = json.dumps(ux["follow_up_draft"])
    crm = result.packet["crm_resolution"]
    for raw_id in (crm.get("contact_id"), crm.get("opportunity_id")):
        assert raw_id  # fixture carries synthetic raw IDs
        assert raw_id not in serialized
    assert "contact_demo" not in serialized
    assert "opp_demo" not in serialized


def test_t_draft_16_draft_body_is_deterministic_from_approved_fields():
    ux1, result, card = _ux_for("transcript-success.expected.json")
    ux2 = project_ux_experience(
        result.packet, card, workflow_status=result.final_state
    )
    assert ux1["follow_up_draft"] == ux2["follow_up_draft"]
    draft = ux1["follow_up_draft"]
    # Body is deterministic and uses approved meeting facts without leaking
    # internal ownership metadata into customer-facing correspondence.
    assert draft["body_text"] == (
        "Hi Taylor,\n\n"
        "Thank you again for your time today. I appreciated the opportunity to "
        "talk through your retirement income planning, particularly the "
        "importance of maintaining liquidity and working within your sixty-day "
        "timeline.\n\n"
        "My next step is to prepare for our recommendation review so we can "
        "continue the conversation and make sure the approach reflects what "
        "matters most to you.\n\n"
        "If anything from our conversation comes to mind before then, feel "
        "free to let me know.\n\n"
        "Best,\n"
        "Alex"
    )


def test_t_draft_17_crm_verified_wording_impossible_without_live_execution():
    for fixture in (
        "transcript-success.expected.json",
        "transcript-ambiguous-contact.expected.json",
        "transcript-no-stage-change.expected.json",
    ):
        ux, _, _ = _ux_for(fixture)
        status = ux["crm_note_status"]
        assert ux["permitted_action_result"]["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
        assert status["state"] != "VERIFIED"
        assert "CRM note verified" not in json.dumps(ux)

    ux, result, card = _ux_for("transcript-success.expected.json")
    assert ux["crm_note_status"] == {
        "state": "NOT_EXECUTED",
        "display": "CRM note not executed in competition mode",
    }
    # Even a forged verified-effect marker cannot produce VERIFIED while
    # LIVE_CRM_EXECUTION remains NOT_PERFORMED.
    forged_card = copy.deepcopy(card)
    forged_card["crm_effect"] = {"verified": True, "evidence": "provider_readback"}
    ux_forged = project_ux_experience(
        result.packet, forged_card, workflow_status=result.final_state
    )
    assert ux_forged["crm_note_status"]["state"] != "VERIFIED"
    assert "CRM note verified" not in json.dumps(ux_forged["crm_note_status"])

    ux_amb, _, _ = _ux_for("transcript-ambiguous-contact.expected.json")
    assert ux_amb["crm_note_status"]["state"] == "BLOCKED"
    assert "No change performed" in ux_amb["crm_note_status"]["display"]


def test_t_draft_18_existing_backend_behavior_unchanged():
    # SUCCESS core contract
    ux, result, _ = _ux_for("transcript-success.expected.json")
    assert result.final_state == "completed"
    assert ux["ux_state"] == UX_COMPLETED
    assert ux["policy_decision"]["note_write"] == "allowed"
    assert ux["policy_decision"]["stage_write"] == "allowed"
    assert ux["policy_decision"]["reason_codes"] == []
    assert ux["permitted_action_result"]["external_effects"] == 0
    assert ux["permitted_action_result"]["crm_changes_made"] is False
    assert ux["audit_status"]["final_disposition"] == "completed"
    # AMBIGUOUS_CONTACT core contract
    ux_amb, result_amb, _ = _ux_for("transcript-ambiguous-contact.expected.json")
    assert result_amb.final_state == "blocked"
    assert ux_amb["ux_state"] == UX_NEEDS_REVIEW
    assert ux_amb["policy_decision"]["note_write"] == "not_attempted"
    assert ux_amb["policy_decision"]["stage_write"] == "not_attempted"
    assert ux_amb["policy_decision"]["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    assert ux_amb["needs_review"]["zero_unauthorized_effects"] is True
    assert ux_amb["permitted_action_result"]["external_effects"] == 0
