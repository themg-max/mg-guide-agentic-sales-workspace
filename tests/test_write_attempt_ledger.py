"""TD2-01..12 and NC-D2-1..10 for NW-008 D2 / AT-8 write-attempt caps."""

from __future__ import annotations

import inspect
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from orchestration.attempt_ledger import LEDGER_STATE_OWNER, WriteAttemptLedger
from orchestration.nw008_tranche_d import (
    build_d2_evidence,
    compute_d2_negative_controls,
    run_d2_attempt_matrix,
    validate_d2_proof,
)
from orchestration.policy import (
    ENFORCEMENT_DECISION_OWNER,
    evaluate_write_attempt,
)
from orchestration.runner import WorkflowRunner
from orchestration.state_machine import StateMachine, WriteCapContractError


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_CONTRACT_PATH = REPO_ROOT / "contracts" / "workflow_states.yaml"


@pytest.fixture(scope="module")
def production_contract() -> dict:
    return yaml.safe_load(PRODUCTION_CONTRACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def sm(production_contract: dict) -> StateMachine:
    return StateMachine(deepcopy(production_contract))


def _with_note_cap(contract: dict, value: object) -> dict:
    temp = deepcopy(contract)
    invariants = []
    for item in temp.get("invariants") or []:
        if isinstance(item, dict) and "max_note_writes_per_run" in item:
            invariants.append({"max_note_writes_per_run": value})
        else:
            invariants.append(item)
    temp["invariants"] = invariants
    return temp


def test_td2_01_contract_derived_note_cap(sm: StateMachine) -> None:
    assert sm.cap_source == "contracts/workflow_states.yaml"
    assert sm.cap_node == "invariants"
    assert sm.max_note_writes_per_run == 1


def test_td2_02_contract_derived_stage_cap(sm: StateMachine) -> None:
    assert sm.max_stage_writes_per_run == 1
    assert sm.write_cap_for("stage") == 1


def test_td2_03_note_attempt_1_admitted(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    calls: list[str] = []
    decision = runner.request_write_attempt(
        "td2-03", "note", transport_executor=lambda: calls.append("x")
    )
    assert decision.decision == "PERMIT"
    assert decision.before == 0
    assert decision.after == 1
    assert decision.max == 1
    assert decision.transport_attempted is False
    assert calls == []


def test_td2_04_note_attempt_2_refused_by_ol3(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    runner.request_write_attempt("td2-04", "note")
    decision = runner.request_write_attempt("td2-04", "note")
    assert decision.decision == "REFUSE"
    assert decision.before == 1
    assert decision.after == 1
    assert decision.decision_owner == ENFORCEMENT_DECISION_OWNER
    assert decision.reason_code == "WRITE_ATTEMPT_CAP_EXCEEDED"


def test_td2_05_stage_attempt_1_admitted(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    decision = runner.request_write_attempt("td2-05", "stage")
    assert decision.decision == "PERMIT"
    assert decision.before == 0
    assert decision.after == 1
    assert decision.transport_attempted is False


def test_td2_06_stage_attempt_2_refused_by_ol3(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    runner.request_write_attempt("td2-06", "stage")
    decision = runner.request_write_attempt("td2-06", "stage")
    assert decision.decision == "REFUSE"
    assert decision.before == 1
    assert decision.after == 1
    assert decision.decision_owner == ENFORCEMENT_DECISION_OWNER


def test_td2_07_independent_counters(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    runner.request_write_attempt("td2-07", "note")
    refused_note = runner.request_write_attempt("td2-07", "note")
    stage = runner.request_write_attempt("td2-07", "stage")
    assert refused_note.decision == "REFUSE"
    assert stage.decision == "PERMIT"
    assert stage.before == 0
    assert stage.after == 1


def test_td2_08_new_run_resets_ledger(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    runner.request_write_attempt("run-1", "note")
    runner.request_write_attempt("run-1", "note")
    fresh = runner.request_write_attempt("run-2", "note")
    assert fresh.decision == "PERMIT"
    assert fresh.before == 0
    assert fresh.after == 1


def test_td2_09_refusal_before_transport(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    calls: list[str] = []
    runner.request_write_attempt(
        "td2-09", "note", transport_executor=lambda: calls.append("admit")
    )
    runner.request_write_attempt(
        "td2-09", "note", transport_executor=lambda: calls.append("refuse")
    )
    assert calls == []


def test_td2_10_deterministic_replay(sm: StateMachine) -> None:
    first = run_d2_attempt_matrix(sm, run_id="replay")
    second = run_d2_attempt_matrix(sm, run_id="replay")
    assert first["note_decisions"] == second["note_decisions"]
    assert first["stage_decisions"] == second["stage_decisions"]
    assert first["ledger_snapshot"] == second["ledger_snapshot"]


def test_td2_11_zero_external_effects(sm: StateMachine) -> None:
    matrix = run_d2_attempt_matrix(sm, run_id="effects")
    effects = matrix["effects"]
    assert effects["GHL_LIVE_CALLS"] == 0
    assert effects["GHL_WRITES"] == 0
    assert effects["FIRESTORE_WRITES"] == 0
    assert effects["EXTERNAL_EFFECTS"] == 0
    assert effects["TRANSPORT_ATTEMPTED"] is False
    assert effects["TRANSPORT_EXECUTOR_CALLS"] == []


def test_td2_12_proof_binds_implementation_subject_sha(sm: StateMachine) -> None:
    """A2 does not emit durable proof files; binding is verified in-memory."""
    sha = "1234567890abcdef1234567890abcdef12345678"
    matrix = run_d2_attempt_matrix(sm, run_id="td2-12")
    evidence = build_d2_evidence(matrix, implementation_subject_sha=sha)
    assert evidence["IMPLEMENTATION_SUBJECT_SHA"] == sha
    assert validate_d2_proof(evidence) == "PASS"
    missing = dict(evidence)
    missing["IMPLEMENTATION_SUBJECT_SHA"] = ""
    assert validate_d2_proof(missing) == "FAIL"


def test_nc_d2_1_through_10_computed(production_contract: dict) -> None:
    controls = compute_d2_negative_controls(production_contract)
    for number in range(1, 11):
        key = f"NC_D2_{number}"
        assert controls[key] == "PASS", controls


def test_nc_d2_1_harness_cannot_override_caps(sm: StateMachine) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    params = set(inspect.signature(runner.request_write_attempt).parameters)
    assert "force_permit" not in params
    assert "force_admit" not in params
    assert "max_writes" not in params
    assert "override_cap" not in params
    runner.request_write_attempt("nc1", "note")
    second = runner.request_write_attempt("nc1", "note")
    assert second.decision == "REFUSE"
    assert second.decision_owner == ENFORCEMENT_DECISION_OWNER


def test_nc_d2_9_temporary_contract_note_cap_2(
    production_contract: dict, sm: StateMachine
) -> None:
    production_bytes = PRODUCTION_CONTRACT_PATH.read_bytes()
    temp_contract = _with_note_cap(production_contract, 2)
    temp_sm = StateMachine(temp_contract)
    runner = WorkflowRunner(state_machine=temp_sm, allow_transport=False)
    d1 = runner.request_write_attempt("cap2", "note")
    d2 = runner.request_write_attempt("cap2", "note")
    d3 = runner.request_write_attempt("cap2", "note")
    assert temp_sm.max_note_writes_per_run == 2
    assert (d1.decision, d2.decision, d3.decision) == ("PERMIT", "PERMIT", "REFUSE")
    assert sm.max_note_writes_per_run == 1
    assert PRODUCTION_CONTRACT_PATH.read_bytes() == production_bytes


@pytest.mark.parametrize(
    "value",
    [None, 0, -1, True, False, "1", 1.5, [], {}],
)
def test_nc_d2_10_malformed_or_missing_cap_fails_closed(
    production_contract: dict, value: object
) -> None:
    if value is None:
        contract = deepcopy(production_contract)
        contract["invariants"] = [
            item
            for item in contract["invariants"]
            if not (isinstance(item, dict) and "max_note_writes_per_run" in item)
        ]
    else:
        contract = _with_note_cap(production_contract, value)
    with pytest.raises(WriteCapContractError):
        StateMachine(contract)

    ledger = WriteAttemptLedger(run_id="invalid-max")
    decision = evaluate_write_attempt(
        write_kind="note", ledger=ledger, max_writes=value if value is not None else 0
    )
    assert decision.decision == "REFUSE"
    assert decision.after == decision.before == 0
    assert decision.decision_owner == ENFORCEMENT_DECISION_OWNER


def test_ledger_is_accounting_only_and_run_local() -> None:
    ledger = WriteAttemptLedger(run_id="acct")
    assert ledger.state_owner == LEDGER_STATE_OWNER
    assert ledger.before("note") == 0
    assert ledger.record_admission("note") == 1
    # Ledger has no permit/refuse API.
    assert not hasattr(ledger, "permit")
    assert not hasattr(ledger, "refuse")
    assert not hasattr(ledger, "decide")


def test_runner_fixture_path_invokes_write_attempt_policy(
    sm: StateMachine, repo_root: Path
) -> None:
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)
    result = runner.run_fixture(
        repo_root / "fixtures" / "transcript-success.expected.json",
        run_id_override="fixture-d2",
        created_at="2026-08-15T12:00:00Z",
    )
    assert result.validation_ok
    assert result.external_effects == 0
    assert "write_attempt_trace" not in result.packet
    assert "write_attempt_policy" not in result.packet
    trace = list(runner.write_attempt_trace)
    assert trace
    assert all(item["decision_owner"] == ENFORCEMENT_DECISION_OWNER for item in trace)
    assert all(item["transport_attempted"] is False for item in trace)
