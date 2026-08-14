import inspect
import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from orchestration.manifest_gate import UnknownOperationError
from orchestration.nw008_tranche_d import (
    PROOF_TIMESTAMP,
    build_d1_evidence,
    execute_d1_run,
    validate_d1_proof,
    write_proof,
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


def test_blocked_operation_is_refused_before_downstream(
    base_manifest_path: Path,
) -> None:
    downstream_calls = []
    packet = execute_d1_run(base_manifest_path, downstream_executor=downstream_calls.append)

    assert packet["run"]["status"] == "failed"
    assert packet["audit"]["final_disposition"] == "failed"
    assert packet["audit"]["warnings"] == ["TOOL_MANIFEST_REFUSED:contact_create"]
    assert packet["d1_execution"]["DOWNSTREAM_EXECUTOR_CALLED"] is False
    assert packet["d1_execution"]["TRANSPORT_ATTEMPTED"] is False
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


def test_nc_d1_6_7_and_8_audit_and_validator(
    base_manifest_path: Path, tmp_path: Path
) -> None:
    packet = execute_d1_run(base_manifest_path)
    paths = write_proof(packet, tmp_path / "proof", "a" * 40)
    audit = json.loads(paths["audit"].read_text(encoding="utf-8"))
    proof_return = yaml.safe_load(paths["return"].read_text(encoding="utf-8"))
    evidence = proof_return["evidence"]

    assert audit["warnings"] == ["TOOL_MANIFEST_REFUSED:contact_create"]
    assert audit["external_effects"]["counters"] == {
        "EXTERNAL_EFFECTS": 0,
        "GHL_READS": 0,
        "GHL_WRITES": 0,
    }
    assert evidence["FIRESTORE_STAGE_B_INSTANTIATED"] is False
    assert evidence["FIRESTORE_STAGE_B_CALLED"] is False
    assert evidence["FIRESTORE_WRITES"] == 0
    assert validate_d1_proof(evidence) == "PASS"

    bad_ghl = deepcopy(evidence)
    bad_ghl["GHL_WRITES"] = 1
    bad_ghl["PROOF_STATUS"] = "PASS"
    assert validate_d1_proof(bad_ghl) == "FAIL"

    bad_effects = deepcopy(evidence)
    bad_effects["EXTERNAL_EFFECTS"] = 1
    assert validate_d1_proof(bad_effects) == "FAIL"


def test_proof_replay_is_byte_deterministic(
    base_manifest_path: Path, tmp_path: Path
) -> None:
    packet = execute_d1_run(base_manifest_path)
    first = write_proof(packet, tmp_path / "first", "b" * 40)
    second = write_proof(packet, tmp_path / "second", "b" * 40)

    assert PROOF_TIMESTAMP == "2026-08-14T17:30:00Z"
    for key in ("run", "audit", "manifest", "return"):
        assert first[key].read_bytes() == second[key].read_bytes()
