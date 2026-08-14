"""NW-008 Tranche B synthetic longitudinal replay acceptance tests."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError

from orchestration.nw008_tranche_b import (
    ENTRYPOINTS,
    Nw008TrancheBHarness,
    validate_tranche_b_context_delta,
    validate_tranche_b_proof_return,
)


@pytest.fixture
def harness(repo_root: Path, tmp_path: Path) -> Nw008TrancheBHarness:
    return Nw008TrancheBHarness(
        repo_root=repo_root,
        proof_root=tmp_path / "proof" / "nw008" / "tranche-b",
        commit_sha="TEST_NW008_TRANCHE_B_SHA",
    )


def test_tranche_b_longitudinal_replay_executes_real_agent_chain(harness: Nw008TrancheBHarness):
    result = harness.run()
    meeting_1 = result.meeting_1_run
    meeting_2 = result.meeting_2_run

    assert result.actual_agent_chain_executed is True
    assert result.prior_context_retrieved is True
    assert result.deterministic_replay == "PASS"
    assert result.effect_counters == {
        "GHL_LIVE_CALLS": 0,
        "GHL_READS": 0,
        "GHL_WRITES": 0,
        "FIRESTORE_WRITES": 0,
        "EXTERNAL_EFFECTS": 0,
        "REAL_CUSTOMER_DATA": 0,
        "NW013_EXECUTED": "NO",
        "DEPLOYMENT_PERFORMED": "NO",
    }
    assert result.historical_at_claims["FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP"] == "CLOSED"

    for run in (meeting_1, meeting_2):
        assert run["ok"] is True
        assert run["session"]["backend"] == "google_adk_package"
        assert [entry["agent_id"] for entry in run["session"]["agent_trace"]] == [
            "meeting_context_agent",
            "relationship_context_agent",
            "follow_up_planning_agent",
        ]
        assert all(entry["status"] == "ok" for entry in run["session"]["agent_trace"])
        assert run["follow_up_packet"]["external_effects"] == 0
        assert run["follow_up_proposal"]["external_effects"] == 0

    assert "approved_prior_context" in meeting_2["session"]["state_keys"]
    assert result.proof_obligations["TB-02"].STATUS == "PASS"
    assert result.proof_obligations["TB-03"].STATUS == "PASS"
    assert result.decision_card["policy_state"] == "ALLOWED"
    assert result.decision_card["policy_reason_code"] == "NONE"


def test_tranche_b_context_delta_classifies_changes_and_preserves_provenance(
    harness: Nw008TrancheBHarness,
):
    result = harness.run()
    delta = result.context_delta
    validate_tranche_b_context_delta(delta)

    unchanged = {item["fact_id"] for item in delta["unchanged_facts"]}
    corrected = {item["fact_id"]: item for item in delta["corrected_facts"]}
    new_facts = {item["fact_id"] for item in delta["new_facts"]}
    completed = {item["commitment_id"]: item for item in delta["commitments_completed"]}
    open_commitments = {
        item["commitment_id"]: item for item in delta["commitments_open"]
    }
    refined = {item["fact_id"] for item in delta["goals_refined"]}
    unresolved = {item["question_id"] for item in delta["unresolved_questions"]}

    assert "goal.primary" in unchanged
    assert "fact.planning.launch_window_months" in unchanged

    correction = corrected["fact.preference.flexible_monthly_savings_capacity"]
    assert correction["prior_value"] == 450
    assert correction["new_value"] == 325
    assert correction["prior_meeting_id"] == "nw008_tb_meeting_1"
    assert correction["current_meeting_id"] == "nw008_tb_meeting_2"
    assert correction["prior_evidence_refs"] == ["m1_capacity_01"]
    assert correction["current_evidence_refs"] == ["m2_capacity_correction_01"]
    assert correction["superseded"] is True

    assert "fact.income.grant_end_month" in new_facts
    assert "goal.priority" in refined

    completed_commitment = completed[
        "commitment.prospect.provide_current_monthly_budget_worksheet"
    ]
    assert completed_commitment["prior_meeting_id"] == "nw008_tb_meeting_1"
    assert completed_commitment["current_meeting_id"] == "nw008_tb_meeting_2"
    assert completed_commitment["current_evidence_refs"] == ["m2_commitment_complete_01"]

    open_commitment = open_commitments[
        "commitment.agent.send_a_draft_two_bucket_savings_scenario"
    ]
    assert open_commitment["source_meeting_id"] == "nw008_tb_meeting_1"
    assert open_commitment["current_meeting_id"] == "nw008_tb_meeting_2"
    assert open_commitment["current_evidence_refs"] == ["m2_commitment_open_01"]

    assert unresolved == {
        "question.reserve_account_mix",
        "question.equipment_timing",
    }
    assert delta["proposed_next_step"]["action"] == (
        "Review the revised liquidity-first scenario next Tuesday"
    )
    assert delta["proposed_next_step"]["evidence_refs"] == ["m2_next_step_01"]
    assert delta["unsupported_inferences"] == [
        {
            "claim_id": "fact.unsupported.inferred_risk_score",
            "reason": "missing_evidence_reference",
        }
    ]


def test_tranche_b_follow_up_planning_uses_confirmed_context_only(
    harness: Nw008TrancheBHarness,
):
    result = harness.run()
    proposal = result.meeting_2_run["follow_up_proposal"]
    packet = result.meeting_2_run["follow_up_packet"]
    context_used = proposal["confirmed_context_used"]

    assert context_used["source"] == "relationship_context.longitudinal_context"
    assert "fact.preference.flexible_monthly_savings_capacity" in context_used[
        "confirmed_fact_ids"
    ]
    assert "question.equipment_timing" in context_used["unresolved_question_ids"]
    assert "fact.unsupported.inferred_risk_score" not in context_used[
        "confirmed_fact_ids"
    ]
    assert proposal["note_proposal"]["body_ref"] == (
        "relationship_context.longitudinal_context"
    )
    assert proposal["policy_evaluation"]["invoked"] is True
    assert proposal["policy_evaluation"]["context_supplied"] is True
    assert proposal["policy_evaluation"]["context_source"] == (
        "relationship_context.longitudinal_context"
    )
    assert proposal["summary"].startswith("Primary goal:")
    assert proposal["proposed_next_steps"][0] == result.context_delta["proposed_next_step"][
        "action"
    ]
    assert packet["run"]["status"] == "completed"
    assert packet["policy"]["note_write"] == "allowed"
    assert packet["policy"]["stage_write"] == "allowed"


def test_tranche_b_proof_obligations_strict(
    harness: Nw008TrancheBHarness,
):
    result = harness.run()
    obligations = result.proof_obligations

    # TB-06 derives from context_delta.new_facts, not merely current_confirmed_facts.
    assert obligations["TB-06"].STATUS == "PASS"
    new_fact_ids = {item["fact_id"] for item in result.context_delta["new_facts"]}
    assert "fact.income.grant_end_month" in new_fact_ids

    # TB-10 evidence coverage across all relevant confirmed-context claim classes.
    for tb_id in (
        "TB-06",
        "TB-10",
        "TB-12",
        "TB-13",
        "TB-17",
    ):
        assert obligations[tb_id].STATUS == "PASS", f"{tb_id} failed"

    # TB-12 exact checks.
    policy_eval = result.meeting_2_run["follow_up_proposal"]["policy_evaluation"]
    assert policy_eval["invoked"] is True
    assert policy_eval["context_supplied"] is True
    assert policy_eval["context_source"] == "relationship_context.longitudinal_context"
    assert policy_eval["deterministic_policy_bypass"] is False

    # TB-13 exact checks.
    assert result.decision_card
    assert result.decision_card_text
    assert result.decision_card_html
    assert result.decision_card["external_effects"] == 0
    assert result.decision_card["next_action"] in (
        "REVIEW_FOLLOW_UP",
        "KEEP_CURRENT_STAGE_AND_REVIEW",
        "RESOLVE_CONTACT",
        "REVIEW_REQUIRED_UNKNOWN_STATE",
    )
    assert result.decision_card["policy_state"] in {
        "ALLOWED",
        "BLOCKED",
        "REVIEW_REQUIRED",
    }


def test_tranche_b_tb10_negative_uncited_commitment_fails(
    harness: Nw008TrancheBHarness,
):
    """An uncited commitment must prevent TB-10 PASS."""
    result = harness.run()
    delta = deepcopy(result.context_delta)
    if delta["commitments_completed"]:
        delta["commitments_completed"][0]["current_evidence_refs"] = []
        delta["commitments_completed"][0]["evidence_refs"] = []

    from orchestration.nw008_tranche_b import (
        Nw008TrancheBHarness as _Harness,
        TrancheBResult,
    )

    patched = TrancheBResult(
        implementation_subject_sha=result.implementation_subject_sha,
        meeting_1_fixture=result.meeting_1_fixture,
        meeting_2_fixture=result.meeting_2_fixture,
        meeting_1_hash=result.meeting_1_hash,
        meeting_2_hash=result.meeting_2_hash,
        meeting_1_run=result.meeting_1_run,
        meeting_2_run=result.meeting_2_run,
        approved_prior_context=result.approved_prior_context,
        context_delta=delta,
        proof_obligations=result.proof_obligations,
        decision_card=result.decision_card,
        decision_card_text=result.decision_card_text,
        decision_card_html=result.decision_card_html,
        actual_agent_chain_executed=result.actual_agent_chain_executed,
        prior_context_retrieved=result.prior_context_retrieved,
        deterministic_replay=result.deterministic_replay,
        historical_at_claims=result.historical_at_claims,
        remaining_gaps=result.remaining_gaps,
        effect_counters=result.effect_counters,
    )
    recomputed = _Harness(
        repo_root=harness.repo_root,
        fixtures_dir=harness.fixtures_dir,
        proof_root=harness.proof_root,
        crm_fixture_path=harness.crm_fixture_path,
        commit_sha=harness.implementation_subject_sha,
    )._proof_obligations(
        execution={
            "meeting_1_run": patched.meeting_1_run,
            "meeting_2_run": patched.meeting_2_run,
            "context_delta": patched.context_delta,
            "decision_card": patched.decision_card,
            "decision_card_text": patched.decision_card_text,
            "decision_card_html": patched.decision_card_html,
            "actual_agent_chain_executed": patched.actual_agent_chain_executed,
            "prior_context_retrieved": patched.prior_context_retrieved,
        },
        deterministic_replay=patched.deterministic_replay,
        fixture_errors=[],
    )
    assert recomputed["TB-10"].STATUS == "FAIL"


def test_tranche_b_tb17_negative_non_synthetic_source_fails(
    harness: Nw008TrancheBHarness,
):
    """A non-synthetic fixture source must prevent TB-17 PASS."""
    result = harness.run()
    run = deepcopy(result.meeting_1_run)
    run["meeting_context"]["meeting"]["source"] = "real_customer_export"
    run["meeting_context"]["participants"][0]["email"] = "taylor@customer.example"

    from orchestration.nw008_tranche_b import _validate_synthetic_fixtures

    errors = _validate_synthetic_fixtures(
        [
            {
                "fixture_id": run["meeting_context"]["meeting"]["meeting_id"],
                "meeting": run["meeting_context"]["meeting"],
                "participants": run["meeting_context"]["participants"],
            }
        ],
        [
            result.meeting_1_run["relationship_context"]["crm_source"],
        ],
    )
    assert errors
    assert any("source" in err for err in errors)
    assert any("customer.example" in err for err in errors)


def test_tranche_b_proof_bundle_and_fail_closed_validation(
    harness: Nw008TrancheBHarness,
):
    result = harness.run()
    paths = harness.write_proof_artifacts(result)

    assert paths["proof_manifest"].is_file()
    assert paths["proof_return"].is_file()
    assert paths["context_delta"].is_file()
    assert paths["meeting_1_run"].is_file()
    assert paths["meeting_2_run"].is_file()
    assert paths["decision_card"].is_file()

    manifest = paths["proof_manifest"].read_text(encoding="utf-8")
    for key, value in ENTRYPOINTS.items():
        assert key in manifest
        assert value in manifest

    proof_return = yaml.safe_load(paths["proof_return"].read_text(encoding="utf-8"))
    validate_tranche_b_proof_return(proof_return)
    assert proof_return["proof_obligations"]["TB-18"]["STATUS"] == "PASS"
    assert proof_return["historical_at_claims"]["AT-2"]["status"] == "NO"
    assert proof_return["historical_at_claims"]["AT-4"]["status"] == "NO"
    assert proof_return["historical_at_claims"]["AT-5"]["status"] == "NO"

    delta = json.loads(paths["context_delta"].read_text(encoding="utf-8"))
    validate_tranche_b_context_delta(delta)

    malformed_delta = deepcopy(delta)
    malformed_delta["corrected_facts"][0]["superseded"] = False
    with pytest.raises(ValidationError):
        validate_tranche_b_context_delta(malformed_delta)

    malformed_return = deepcopy(proof_return)
    malformed_return["effect_counters"]["GHL_WRITES"] = 1
    with pytest.raises(ValidationError):
        validate_tranche_b_proof_return(malformed_return)
