import inspect
import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from orchestration.manifest_gate import UnknownOperationError
from orchestration.nw008_tranche_d import (
    PROOF_TIMESTAMP,
    StageBWriterSpy,
    execute_d1_run,
    generate_final_proof,
    validate_d1_proof,
)


@pytest.fixture
def base_manifest_path(tmp_path: Path) -> Path:
    path = tmp_path / "ghl_tool_manifest.yaml"
    path.write_text(
        yaml.safe_dump(
            {"ghl_mcp": {"blocked_capability_classes": ["contact_create"]}}
        ),
        encoding="utf-8",
    )
    return path


def test_nc_d1_1_harness_cannot_inject_classifier_mapping(
    base_manifest_path: Path,
) -> None:
    assert "classifier_map" not in inspect.signature(execute_d1_run).parameters

    with pytest.raises(TypeError):
        execute_d1_run(base_manifest_path, classifier_map={})  # type: ignore[call-arg]


def test_blocked_operation_is_refused_before_downstream_or_stage_b(
    base_manifest_path: Path,
) -> None:
    downstream_calls = []
    stage_b_spy = StageBWriterSpy()
    packet = execute_d1_run(
        base_manifest_path,
        downstream_executor=downstream_calls.append,
        stage_b_spy=stage_b_spy,
    )

    assert packet["run"]["status"] == "failed"
    assert packet["audit"]["final_disposition"] == "failed"
    assert packet["audit"]["warnings"] == ["TOOL_MANIFEST_REFUSED:contact_create"]
    assert packet["d1_execution"]["DOWNSTREAM_EXECUTOR_CALLED"] is False
    assert packet["d1_execution"]["TRANSPORT_ATTEMPTED"] is False
    assert packet["d1_execution"]["STAGE_B_SPY_INSTANTIATED"] is True
    assert packet["d1_execution"]["STAGE_B_SPY_CALLED"] is False
    assert packet["d1_execution"]["FIRESTORE_STAGE_B_INSTANTIATED"] is False
    assert packet["d1_execution"]["FIRESTORE_STAGE_B_CALLED"] is False
    assert stage_b_spy.client_instantiations == 0
    assert stage_b_spy.calls == []
    assert stage_b_spy.writes == 0
    assert downstream_calls == []


def test_nc_d1_2_and_5_known_allowed_operation_reaches_local_downstream(
    base_manifest_path: Path,
) -> None:
    downstream_calls = []
    packet = execute_d1_run(
        base_manifest_path,
        "search-contacts-advanced",
        downstream_calls.append,
    )

    assert packet["run"]["status"] == "completed"
    assert packet["d1_execution"]["CAPABILITY_CLASS"] == "contact_search"
    assert packet["d1_execution"]["MANIFEST_BLOCKED"] is False
    assert packet["d1_execution"]["DOWNSTREAM_EXECUTOR_CALLED"] is True
    assert packet["audit"]["warnings"] == []
    assert downstream_calls == ["contact_search"]


def test_unknown_operation_fails_closed_before_downstream(
    base_manifest_path: Path,
) -> None:
    downstream_calls = []

    with pytest.raises(UnknownOperationError):
        execute_d1_run(base_manifest_path, "unknown-operation", downstream_calls.append)

    assert downstream_calls == []


def test_nc_d1_4_manifest_data_owns_blocking(tmp_path: Path) -> None:
    path = tmp_path / "manifest.yaml"
    path.write_text(
        yaml.safe_dump({"ghl_mcp": {"blocked_capability_classes": ["email_send"]}}),
        encoding="utf-8",
    )
    downstream_calls = []

    packet = execute_d1_run(path, "create-contact", downstream_calls.append)

    assert packet["run"]["status"] == "completed"
    assert downstream_calls == ["contact_create"]


def test_nc_d1_statuses_are_computed_from_observations(
    base_manifest_path: Path, tmp_path: Path
) -> None:
    packet = execute_d1_run(base_manifest_path)
    audit_path = tmp_path / "proof"
    paths = generate_final_proof(base_manifest_path, audit_path, "a" * 40)
    audit = json.loads(paths["audit"].read_text(encoding="utf-8"))
    proof_return = yaml.safe_load(paths["return"].read_text(encoding="utf-8"))
    evidence = proof_return["evidence"]

    assert audit["warnings"] == ["TOOL_MANIFEST_REFUSED:contact_create"]
    assert evidence["PROOF_STATUS"] == "PASS"
    assert evidence["DETERMINISTIC_PROOF_REPLAY"] == "PASS"
    assert all(evidence[f"NC_D1_{number}"] == "PASS" for number in range(1, 9))
    assert validate_d1_proof(evidence) == "PASS"
    assert packet["d1_execution"]["FIRESTORE_WRITES"] == 0


def test_nc_d1_7_validator_rejects_nonzero_effect_observations(
    base_manifest_path: Path, tmp_path: Path
) -> None:
    evidence = yaml.safe_load(
        generate_final_proof(base_manifest_path, tmp_path / "proof", "b" * 40)[
            "return"
        ].read_text(encoding="utf-8")
    )["evidence"]

    bad_ghl = deepcopy(evidence)
    bad_ghl["GHL_WRITES"] = 1
    bad_ghl["PROOF_STATUS"] = "PASS"
    assert validate_d1_proof(bad_ghl) == "FAIL"

    bad_effects = deepcopy(evidence)
    bad_effects["EXTERNAL_EFFECTS"] = 1
    assert validate_d1_proof(bad_effects) == "FAIL"


def test_proof_replay_is_computed_and_byte_deterministic(
    base_manifest_path: Path, tmp_path: Path
) -> None:
    first = generate_final_proof(base_manifest_path, tmp_path / "first", "c" * 40)
    second = generate_final_proof(base_manifest_path, tmp_path / "second", "c" * 40)

    assert PROOF_TIMESTAMP == "2026-08-14T17:30:00Z"
    for key in ("run", "audit", "manifest", "return"):
        assert first[key].read_bytes() == second[key].read_bytes()


# ---------------------------------------------------------------------------
# D2 / AT-8 acceptance (A2 implementation subject — no durable proof files)
# ---------------------------------------------------------------------------

from copy import deepcopy as _deepcopy

import yaml as _yaml

from orchestration.nw008_tranche_d import (
    build_d2_evidence,
    compute_d2_negative_controls,
    run_d2_attempt_matrix,
    validate_d2_proof,
)
from orchestration.policy import ENFORCEMENT_DECISION_OWNER
from orchestration.runner import WorkflowRunner
from orchestration.state_machine import StateMachine


def _production_contract() -> dict:
    root = Path(__file__).resolve().parents[1]
    return _yaml.safe_load(
        (root / "contracts" / "workflow_states.yaml").read_text(encoding="utf-8")
    )


def test_d2_authority_model_and_offline_matrix() -> None:
    contract = _production_contract()
    sm = StateMachine(_deepcopy(contract))
    matrix = run_d2_attempt_matrix(sm, run_id="accept-d2")
    assert matrix["max_note_writes_per_run"] == 1
    assert matrix["max_stage_writes_per_run"] == 1
    assert matrix["enforcement_decision_owner"] == ENFORCEMENT_DECISION_OWNER
    assert matrix["runner_authority"] == WorkflowRunner.RUNNER_AUTHORITY
    assert matrix["agent_cap_authority"] is False
    assert matrix["harness_cap_authority"] is False
    assert matrix["note_decisions"][0]["decision"] == "PERMIT"
    assert matrix["note_decisions"][1]["decision"] == "REFUSE"
    assert matrix["stage_decisions"][0]["decision"] == "PERMIT"
    assert matrix["stage_decisions"][1]["decision"] == "REFUSE"
    assert matrix["effects"]["EXTERNAL_EFFECTS"] == 0
    assert matrix["effects"]["TRANSPORT_EXECUTOR_CALLS"] == []


def test_d2_negative_controls_all_pass() -> None:
    controls = compute_d2_negative_controls(_production_contract())
    assert all(controls[f"NC_D2_{n}"] == "PASS" for n in range(1, 11)), controls


def test_d2_validator_fail_closed_on_nonzero_effects() -> None:
    sm = StateMachine(_deepcopy(_production_contract()))
    matrix = run_d2_attempt_matrix(sm, run_id="accept-d2-val")
    evidence = build_d2_evidence(
        matrix,
        implementation_subject_sha="f" * 40,
        production_contract=_production_contract(),
    )
    assert validate_d2_proof(evidence) == "PASS"
    assert evidence["DETERMINISTIC_REPLAY_BYTES_EQUAL"] is True
    assert evidence["DETERMINISTIC_REPLAY_HASHES_EQUAL"] is True
    poisoned = dict(evidence)
    poisoned["FIRESTORE_WRITES"] = 1
    assert validate_d2_proof(poisoned) == "FAIL"


def test_d2_does_not_emit_durable_proof_namespace(tmp_path: Path) -> None:
    """A2 must not create durable d2-at8 proof artifacts under proof/."""
    durable = (
        Path(__file__).resolve().parents[1]
        / "proof"
        / "nw008"
        / "tranche-d"
        / "d2-at8"
    )
    assert not durable.exists()
    assert list(tmp_path.iterdir()) == []
