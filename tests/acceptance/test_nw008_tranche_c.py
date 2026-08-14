"""NW-008 Tranche C acceptance tests."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from orchestration.nw008_tranche_c import (
    Nw008TrancheCHarness,
    _sha256_dict,
    _validate_proof_return,
)


@pytest.fixture
def harness(repo_root: Path) -> Nw008TrancheCHarness:
    return Nw008TrancheCHarness(
        repo_root=repo_root,
        commit_sha="deadbeef",
    )


@pytest.fixture
def result(harness: Nw008TrancheCHarness):
    return harness.run()


def test_governed_short_circuit_boundaries(result):
    at2 = result.scenarios["AT-02"]
    at4 = result.scenarios["AT-04"]
    at5 = result.scenarios["AT-05"]

    assert at2.stop_point == "relationship_context_agent"
    assert at2.agent_statuses["relationship_context_agent"] == "BLOCK_ORIGIN"
    assert at2.agent_statuses["follow_up_planning_agent"] == "SKIPPED_GOVERNED_STOP"
    assert at2.agent_execution["follow_up_planning_agent"]["delegate_called"] is False
    assert "follow_up_planning_agent" not in at2.agents_completed

    assert at4.stop_point == "relationship_context_agent"
    assert at4.agent_statuses["relationship_context_agent"] == "BLOCK_ORIGIN"
    assert at4.agent_statuses["follow_up_planning_agent"] == "SKIPPED_GOVERNED_STOP"
    assert at4.agent_execution["follow_up_planning_agent"]["delegate_called"] is False
    assert "follow_up_planning_agent" not in at4.agents_completed

    assert at5.stop_point == "meeting_context_agent"
    assert at5.agent_statuses["meeting_context_agent"] == "BLOCK_ORIGIN"
    assert at5.agent_statuses["relationship_context_agent"] == "SKIPPED_GOVERNED_STOP"
    assert at5.agent_statuses["follow_up_planning_agent"] == "SKIPPED_GOVERNED_STOP"
    assert at5.agent_execution["relationship_context_agent"]["delegate_called"] is False
    assert at5.agent_execution["follow_up_planning_agent"]["delegate_called"] is False
    assert "relationship_context_agent" not in at5.agents_completed
    assert "follow_up_planning_agent" not in at5.agents_completed


def test_scenarios_blocked_policy_not_bypassed_zero_effects(result):
    for run in result.scenarios.values():
        assert run.disposition == "blocked"
        assert run.policy_gate_invoked is False
        assert run.policy_bypass is False
        assert run.effect_counters["GHL_LIVE_CALLS"] == 0
        assert run.effect_counters["GHL_READS"] == 0
        assert run.effect_counters["GHL_WRITES"] == 0
        assert run.effect_counters["FIRESTORE_WRITES"] == 0
        assert run.effect_counters["EXTERNAL_EFFECTS"] == 0
        assert run.effect_counters["REAL_CUSTOMER_DATA"] == 0


def test_at2_card_state2_equivalent_exact(result):
    at2 = result.scenarios["AT-02"]
    assert at2.decision_card is not None
    assert at2.decision_card["policy_state"] == "BLOCKED"
    assert at2.decision_card["policy_reason_code"] == "AMBIGUOUS_CONTACT"
    assert at2.decision_card["next_action"] == "RESOLVE_CONTACT"


def test_transcript_hash_and_envelope_digest_integrity(result):
    for run in result.scenarios.values():
        assert run.transcript_content_hash == run.envelope["artifact"]["content_hash"]
        assert run.envelope_digest == _sha256_dict(run.envelope)
        assert run.envelope_preserved is True


def test_proof_bundle_schema_and_obligations(harness: Nw008TrancheCHarness, result):
    paths = harness.write_proof_artifacts(result)
    assert paths["proof_manifest"].is_file()
    assert paths["proof_return"].is_file()

    payload = yaml.safe_load(paths["proof_return"].read_text(encoding="utf-8"))
    ok, errors = _validate_proof_return(payload)
    if not ok:
        pytest.fail("; ".join(errors))

    assert payload["targets"] == ["AT-2", "AT-4", "AT-5"]
    assert payload["excludes"] == ["AT-8", "AT-9"]
    assert set(payload["proof_obligations"].keys()) == {
        f"TC-{i:02d}" for i in range(1, 23)
    }
    for obligation in payload["proof_obligations"].values():
        assert obligation["EVIDENCE_PATH"]


def _tampered_obligations(base_result, harness: Nw008TrancheCHarness, scenario: str, **updates):
    run = copy.deepcopy(base_result.scenarios[scenario])
    tampered = replace(run, **updates)
    scenarios = dict(base_result.scenarios)
    scenarios[scenario] = tampered
    return harness._proof_obligations(scenarios, deterministic_replay="PASS")


def test_negative_control_downstream_execution_after_governed_stop_fails(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    execution = dict(run.agent_execution)
    execution["follow_up_planning_agent"] = {
        "wrapper_status": "EXECUTED",
        "delegate_called": True,
        "block_origin": False,
    }
    statuses = dict(run.agent_statuses)
    statuses["follow_up_planning_agent"] = "ok"
    obligations = _tampered_obligations(
        result,
        harness,
        "AT-02",
        agent_execution=execution,
        agent_statuses=statuses,
        agents_completed=list(run.agents_completed) + ["follow_up_planning_agent"],
    )
    assert obligations["TC-04"].STATUS == "FAIL"


def test_negative_control_nonzero_effect_counter_fails(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    counters = dict(run.effect_counters)
    counters["EXTERNAL_EFFECTS"] = 1
    obligations = _tampered_obligations(
        result,
        harness,
        "AT-02",
        effect_counters=counters,
    )
    assert obligations["TC-05"].STATUS == "FAIL"


def test_negative_control_tampered_envelope_provenance_fails(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    tampered_result = copy.deepcopy(run.result)
    tampered_result["transcript_source_envelope"]["ownership"]["tenant_ref"] = "tampered"
    obligations = _tampered_obligations(
        result,
        harness,
        "AT-02",
        result=tampered_result,
        envelope_preserved=False,
    )
    assert obligations["TC-20"].STATUS == "FAIL"


def test_negative_control_instruction_authority_true_fails(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    envelope = copy.deepcopy(run.envelope)
    envelope["content"]["instruction_authority"] = True
    obligations = _tampered_obligations(
        result,
        harness,
        "AT-02",
        envelope=envelope,
    )
    assert obligations["TC-21"].STATUS == "FAIL"


def test_negative_control_at2_card_semantics_mismatch_fails(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    card = dict(run.decision_card or {})
    card["policy_state"] = "REVIEW_REQUIRED"
    obligations = _tampered_obligations(
        result,
        harness,
        "AT-02",
        decision_card=card,
    )
    assert obligations["TC-22"].STATUS == "FAIL"


def test_negative_control_harness_threshold_reason_cannot_override_authority(
    harness: Nw008TrancheCHarness, monkeypatch
):
    from orchestration import nw008_tranche_c as tc_mod

    tampered = copy.deepcopy(tc_mod.SCENARIOS)
    tampered["AT-05"]["governed_stop_profile"]["extraction_abort_threshold"] = 0.99
    tampered["AT-05"]["governed_stop_profile"]["reason_code"] = "FORCED_REASON"
    tampered["AT-05"]["governed_stop_profile"][
        "reason_source"
    ] = "harness.override.authority"
    monkeypatch.setattr(tc_mod, "SCENARIOS", tampered)

    result = harness.run()
    at5 = result.scenarios["AT-05"]
    assert at5.stop_reason_code == "LOW_EXTRACTION_CONFIDENCE"
    assert "FORCED" not in at5.stop_reason_source
    assert "harness.override" not in at5.stop_reason_source
    assert "workflow_states.yaml" in at5.stop_reason_source


def test_negative_control_historical_claim_fails_closed(
    result, harness: Nw008TrancheCHarness
):
    run = copy.deepcopy(result.scenarios["AT-02"])
    card = dict(run.decision_card or {})
    card["policy_state"] = "REVIEW_REQUIRED"
    tampered = replace(run, decision_card=card)
    claims = harness._historical_at_claims({"AT-02": tampered})
    assert claims["AT-2"]["status"] == "NO"
    assert "state_2_equivalent_card" in claims["AT-2"]["detail"]


def test_deterministic_replay_passes(result):
    assert result.deterministic_replay == "PASS"
