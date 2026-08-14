"""NW-008 Tranche C acceptance tests."""

from __future__ import annotations

import copy
import inspect
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from agents.follow_up_planning.runtime import Unit3FollowUpRuntime
from orchestration.nw008_tranche_c import (
    Nw008TrancheCHarness,
    TrancheCReplayError,
    _sha256_dict,
    _validate_proof_return,
    verify_proof_subject_sha,
)


@pytest.fixture
def harness(repo_root: Path) -> Nw008TrancheCHarness:
    return Nw008TrancheCHarness(repo_root=repo_root)


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


def test_negative_control_harness_boundary_input_eliminated():
    """The harness cannot choose the authoritative enforcement boundary.

    The boundary input is eliminated entirely: no scenario supplies a
    governed_stop_profile and run_unit3 no longer accepts one. Runtime
    enforcement is derived only from the StateMachine/workflow contract.
    """
    from orchestration import nw008_tranche_c as tc_mod

    params = inspect.signature(Unit3FollowUpRuntime.run_unit3).parameters
    assert "governed_stop_profile" not in params
    for spec in tc_mod.SCENARIOS.values():
        assert "governed_stop_profile" not in spec


def test_negative_control_reason_derived_from_state_machine_transition(
    harness: Nw008TrancheCHarness, monkeypatch
):
    """Monkeypatch the authoritative StateMachine transition and prove the
    runtime reason_code derives from the transition, not a hard-coded string."""
    from agents.follow_up_planning import runtime as rt_mod
    from agents.follow_up_planning import FollowUpPlanningAgent
    from agents.meeting_context import MeetingContextAgent
    from agents.relationship_context import RelationshipContextAgent
    from agents.relationship_context.crm_store import SyntheticCrmStore
    from orchestration import nw008_tranche_c as tc_mod
    from orchestration.state_machine import StateMachine
    from orchestration.transcript_source import (
        envelope_from_dict,
        envelope_to_provider_request,
    )

    contract = yaml.safe_load(
        (tc_mod.REPO_ROOT / "contracts" / "workflow_states.yaml").read_text(
            encoding="utf-8"
        )
    )
    tampered_reason = "TAMPERED_CONTRACT_REASON"
    for transition in contract["transitions"]:
        if (
            transition["from"] == "resolving"
            and transition["to"] == "blocked"
            and transition["when"] == "contact_ambiguous"
        ):
            transition["reason_code"] = tampered_reason
    tampered_sm = StateMachine(contract)
    monkeypatch.setattr(rt_mod, "_unit3_state_machine", lambda: tampered_sm)

    envelope_raw = tc_mod._load_json(harness.fixtures_dir / "at-02-envelope.json")
    sidecar = tc_mod._load_json(harness.fixtures_dir / "at-02-sidecar.json")
    request = envelope_to_provider_request(
        envelope_from_dict(envelope_raw),
        extraction_result=sidecar["extraction_result"],
        extraction_confidence=sidecar["extraction_confidence"],
        evidence_references=sidecar.get("evidence_references"),
        participants=sidecar["participants"],
    )
    store = SyntheticCrmStore.from_fixture_path(harness.crm_fixture_path)
    runtime = Unit3FollowUpRuntime(
        meeting_agent=MeetingContextAgent.for_fixture_mode(),
        relationship_agent=RelationshipContextAgent(store=store),
        follow_up_agent=FollowUpPlanningAgent(),
    )
    runtime.start()
    run = runtime.run_unit3(
        meeting_request=request,
        run_id="neg_reason_derivation",
        scenario_id="NEG_REASON",
    )
    assert run.governed_stop is not None
    assert run.governed_stop["reason_code"] == tampered_reason
    assert tampered_reason in run.governed_stop["reason_source"]


def test_negative_control_nonexistent_subject_sha_fails(
    harness: Nw008TrancheCHarness, result
):
    nonexistent = "0" * 40
    ok, detail = verify_proof_subject_sha(nonexistent, harness.repo_root)
    assert not ok
    assert "PROOF_SUBJECT_SHA_EXISTS=false" in detail

    tampered = replace(result, implementation_subject_sha=nonexistent)
    with pytest.raises(
        TrancheCReplayError, match="proof subject SHA integrity"
    ):
        harness.write_proof_artifacts(tampered)


def test_proof_subject_sha_integrity(repo_root: Path):
    """The committed proof-return's implementation_subject_sha resolves to a
    commit that is an ancestor of the current HEAD."""
    payload = yaml.safe_load(
        (repo_root / "proof" / "nw008" / "tranche-c" / "proof-return.yaml").read_text(
            encoding="utf-8"
        )
    )
    ok, detail = verify_proof_subject_sha(
        payload["implementation_subject_sha"], repo_root
    )
    assert ok, detail


def test_negative_control_foundation_clause_mismatch_fails_tc19(
    result, harness: Nw008TrancheCHarness, monkeypatch
):
    # Direct: tampered §17 text is detected.
    ok, detail = Nw008TrancheCHarness._verify_foundation_definitions(
        foundation_text="## 17. Acceptance tests\n\n| AT-2 | tampered |\n"
    )
    assert not ok
    assert "FOUNDATION_DEFINITIONS_UNCHANGED=false" in detail

    # Bounded: a Foundation clause mismatch makes TC-19 FAIL.
    monkeypatch.setattr(
        Nw008TrancheCHarness,
        "_verify_foundation_definitions",
        classmethod(
            lambda cls, foundation_text=None: (
                False,
                "FOUNDATION_DEFINITIONS_UNCHANGED=false: tampered",
            )
        ),
    )
    obligations = harness._proof_obligations(
        result.scenarios, deterministic_replay="PASS"
    )
    assert obligations["TC-19"].STATUS == "FAIL"


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
