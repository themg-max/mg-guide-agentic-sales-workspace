from __future__ import annotations

import ast
import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

import pytest
import yaml

from scripts.nw008.run_at10_bounded_execution import (
    ACTIVE_GRANT_BEGIN,
    ACTIVE_GRANT_END,
    BOUND_EXCEEDED,
    COLLECTION,
    DATABASE,
    GOVERNANCE_REJECTED,
    LOCATION,
    MAX_CREATES,
    MAX_DELETES,
    MAX_READS,
    MAX_TOTAL_OPERATIONS,
    PROJECT,
    RUN_ALLOWLIST,
    At10BoundedExecutor,
    BoundedExecutionError,
    BoundedFirestoreGateway,
    OperationCounter,
    main,
    parse_and_validate_active_grant,
    _load_projected_records,
)

TEST_SHA = "a" * 40
CANONICAL_APPROVED_AT = "2026-08-15T12:33:00-04:00"


def _active_grant_lines(
    *,
    decision: str = "AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION",
    status: str = "HUMAN_APPROVED",
    human_signature: str = "APPROVED",
    approved_at: str = CANONICAL_APPROVED_AT,
    execution_authorized: str = "YES",
    subject_sha: str = TEST_SHA,
    execution_code_sha: str = TEST_SHA,
    extra_lines: tuple[str, ...] = (),
    omit: frozenset[str] | set[str] | None = None,
) -> list[str]:
    omitted = set(omit or ())
    fields = [
        ("STATUS", status),
        ("DECISION", decision),
        ("HUMAN_SIGNATURE", human_signature),
        ("HUMAN_APPROVER_EMAIL", "themg@themiliare-group.com"),
        ("HUMAN_APPROVER_NAME", "AARON PRESTON CHANDLER"),
        ("APPROVED_AT", approved_at),
        ("AT10_EXECUTION_AUTHORIZED", execution_authorized),
        ("AT10_COMPLETION_CLAIM_AUTHORIZED", "NO"),
        ("AT10_COMPLETE", "NO"),
        ("IMPLEMENTATION_SUBJECT_SHA", subject_sha),
        ("EXECUTION_CODE_SHA", execution_code_sha),
        ("PROJECT", "mg-devpost"),
        ("DATABASE", "devpost-google-contest"),
        ("LOCATION", "us-east4"),
        ("COLLECTION", "workflow_runs"),
        ("RUN_ALLOWLIST", ",".join(RUN_ALLOWLIST)),
        ("MAX_DISTINCT_RUN_IDS", "4"),
        ("MAX_DOCUMENT_CREATES", "4"),
        ("MAX_DOCUMENT_READS", "12"),
        ("MAX_DOCUMENT_DELETES", "4"),
        ("MAX_NETWORK_CALLS", "20"),
        ("MAX_EXECUTION_MINUTES", "10"),
        ("FIRESTORE_LIST_AUTHORIZED", "NO"),
        ("FIRESTORE_QUERY_AUTHORIZED", "NO"),
        ("COLLECTION_SWEEP_AUTHORIZED", "NO"),
        ("OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED", "NO"),
        ("PR53_AUTHORITY_REUSABLE", "NO"),
    ]
    body = [f"{key}={value}" for key, value in fields if key not in omitted]
    body.extend(extra_lines)
    return [ACTIVE_GRANT_BEGIN, *body, ACTIVE_GRANT_END]


def _canonical_approved_grant_text(**kwargs: Any) -> str:
    prose = [
        "# Example explanatory prose (not authoritative)",
        "DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION",
        "STATUS=HUMAN_APPROVED",
        "HUMAN_SIGNATURE=APPROVED",
        "AT10_EXECUTION_AUTHORIZED=YES",
        "",
    ]
    return "\n".join([*prose, *_active_grant_lines(**kwargs), ""])


class FakeSnapshot:
    def __init__(self, value: Optional[Dict[str, Any]]) -> None:
        self.exists = value is not None
        self._value = value

    def to_dict(self) -> Optional[Dict[str, Any]]:
        return dict(self._value) if self._value is not None else None


class FakeDocument:
    def __init__(self, client: "FakeFirestoreClient", run_id: str) -> None:
        self.client = client
        self.run_id = run_id

    def create(self, payload: Dict[str, Any]) -> None:
        self.client.calls.append(("create", self.run_id))
        self.client.documents[self.run_id] = dict(payload)

    def get(self) -> FakeSnapshot:
        self.client.calls.append(("read", self.run_id))
        return FakeSnapshot(self.client.documents.get(self.run_id))

    def delete(self) -> None:
        self.client.calls.append(("delete", self.run_id))
        self.client.documents.pop(self.run_id, None)


class FakeCollection:
    def __init__(self, client: "FakeFirestoreClient") -> None:
        self.client = client

    def document(self, run_id: str) -> FakeDocument:
        return FakeDocument(self.client, run_id)


class FakeFirestoreClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.documents: Dict[str, Dict[str, Any]] = {}

    def collection(self, collection: str) -> FakeCollection:
        assert collection == "workflow_runs"
        return FakeCollection(self)


def _gateway(
    *,
    max_creates: int = MAX_CREATES,
    max_reads: int = MAX_READS,
    max_deletes: int = MAX_DELETES,
    max_total: int = MAX_TOTAL_OPERATIONS,
) -> tuple[BoundedFirestoreGateway, FakeFirestoreClient]:
    client = FakeFirestoreClient()
    counter = OperationCounter(
        max_creates=max_creates,
        max_reads=max_reads,
        max_deletes=max_deletes,
        max_total=max_total,
    )
    return BoundedFirestoreGateway(client, counter), client


def test_fifth_run_id_fails_closed_before_network() -> None:
    gateway, client = _gateway()
    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.get_exact("run_nw006_fifth_001")
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert client.calls == []
    assert gateway.counter.total == 0


def test_target_is_exact_and_not_runtime_configurable() -> None:
    assert (PROJECT, DATABASE, LOCATION, COLLECTION) == (
        "mg-devpost",
        "devpost-google-contest",
        "us-east4",
        "workflow_runs",
    )


def test_approved_but_unmerged_authorization_rejected_before_client(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import scripts.nw008.run_at10_bounded_execution as runner

    authorization = tmp_path / "approved-grant.md"
    authorization.write_text(_canonical_approved_grant_text(), encoding="utf-8")
    network_calls = 0
    client_creations = 0

    def fake_run_git(arguments: list[str]) -> subprocess.CompletedProcess[str]:
        if arguments[:2] == ["merge-base", "--is-ancestor"]:
            return subprocess.CompletedProcess(arguments, 1, "", "")
        return subprocess.CompletedProcess(arguments, 0, "", "")

    def fail_if_client_created() -> Any:
        nonlocal client_creations, network_calls
        client_creations += 1
        network_calls += 1
        raise AssertionError("Firestore client must not be created")

    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(runner, "_run_git", fake_run_git)
    monkeypatch.setattr(runner, "verify_source_binding", lambda *_: None)
    monkeypatch.setattr(runner, "_create_firestore_client", fail_if_client_created)
    monkeypatch.setattr(
        runner,
        "_parse_args",
        lambda: argparse.Namespace(
            implementation_subject_sha=TEST_SHA,
            execution_code_sha=TEST_SHA,
            authorization_decision_sha="b" * 40,
            authorization_artifact=authorization,
            proof_dir=tmp_path / "proof",
        ),
    )

    with pytest.raises(BoundedExecutionError) as excinfo:
        main()
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert "not an ancestor of origin/main" in excinfo.value.message
    assert client_creations == 0
    assert network_calls == 0


def test_pending_active_block_with_approved_prose_is_rejected() -> None:
    text = "\n".join(
        [
            "# Outside prose must never authorize execution",
            "DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION",
            "STATUS=HUMAN_APPROVED",
            "HUMAN_SIGNATURE=APPROVED",
            "AT10_EXECUTION_AUTHORIZED=YES",
            "APPROVED_AT=2026-08-15T12:33:00-04:00",
            "",
            *_active_grant_lines(
                decision="PENDING_HUMAN_EXECUTION_AUTHORIZATION",
                status="PENDING_HUMAN_DECISION",
                human_signature="PENDING",
                execution_authorized="NO",
            ),
            "",
        ]
    )
    with pytest.raises(BoundedExecutionError) as excinfo:
        parse_and_validate_active_grant(text, TEST_SHA, TEST_SHA)
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert "pending" in excinfo.value.message.lower()


def test_conflicting_duplicate_decision_keys_are_rejected() -> None:
    text = _canonical_approved_grant_text(
        extra_lines=("DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION",)
    )
    with pytest.raises(BoundedExecutionError) as excinfo:
        parse_and_validate_active_grant(text, TEST_SHA, TEST_SHA)
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert "duplicate key" in excinfo.value.message


def test_two_active_blocks_are_rejected() -> None:
    block = "\n".join(_active_grant_lines())
    text = f"{block}\n\n{block}\n"
    with pytest.raises(BoundedExecutionError) as excinfo:
        parse_and_validate_active_grant(text, TEST_SHA, TEST_SHA)
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert "exactly one ACTIVE GRANT block" in excinfo.value.message


def test_malformed_approval_timestamp_is_rejected() -> None:
    text = _canonical_approved_grant_text(approved_at="2026-08-15 12:33:00")
    with pytest.raises(BoundedExecutionError) as excinfo:
        parse_and_validate_active_grant(text, TEST_SHA, TEST_SHA)
    assert excinfo.value.code == GOVERNANCE_REJECTED
    assert "APPROVED_AT is malformed" in excinfo.value.message


def test_canonical_approved_active_block_passes() -> None:
    text = _canonical_approved_grant_text()
    fields = parse_and_validate_active_grant(text, TEST_SHA, TEST_SHA)
    assert fields["DECISION"] == "AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION"
    assert fields["STATUS"] == "HUMAN_APPROVED"
    assert fields["AT10_EXECUTION_AUTHORIZED"] == "YES"
    assert fields["AT10_COMPLETION_CLAIM_AUTHORIZED"] == "NO"
    assert fields["AT10_COMPLETE"] == "NO"
    assert fields["APPROVED_AT"] == CANONICAL_APPROVED_AT
    assert fields["RUN_ALLOWLIST"] == ",".join(RUN_ALLOWLIST)
    assert fields["OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED"] == "NO"
    assert fields["PR53_AUTHORITY_REUSABLE"] == "NO"


def test_operation_after_ten_minutes_fails_closed_before_network() -> None:
    times = iter((0.0, 601.0))
    client = FakeFirestoreClient()
    counter = OperationCounter(clock=lambda: next(times))
    gateway = BoundedFirestoreGateway(client, counter)

    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.get_exact(RUN_ALLOWLIST[0])
    assert excinfo.value.code == BOUND_EXCEEDED
    assert client.calls == []
    assert counter.total == 0


def test_fifth_create_fails_closed_before_network() -> None:
    gateway, client = _gateway()
    audit = _load_projected_records("2026-08-15T16:00:00+00:00")[RUN_ALLOWLIST[0]]
    for index in range(4):
        gateway.create_exact(RUN_ALLOWLIST[index], audit)
    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.create_exact(RUN_ALLOWLIST[0], audit)
    assert excinfo.value.code == BOUND_EXCEEDED
    assert len(client.calls) == 4


def test_thirteenth_read_fails_closed_before_network() -> None:
    gateway, client = _gateway()
    for index in range(12):
        gateway.get_exact(RUN_ALLOWLIST[index % 4])
    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.get_exact(RUN_ALLOWLIST[0])
    assert excinfo.value.code == BOUND_EXCEEDED
    assert len(client.calls) == 12


def test_fifth_delete_fails_closed_before_network() -> None:
    gateway, client = _gateway()
    for index in range(4):
        gateway.delete_exact(RUN_ALLOWLIST[index])
    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.delete_exact(RUN_ALLOWLIST[0])
    assert excinfo.value.code == BOUND_EXCEEDED
    assert len(client.calls) == 4


def test_twenty_first_total_operation_fails_closed() -> None:
    gateway, client = _gateway(
        max_creates=25,
        max_reads=25,
        max_deletes=25,
        max_total=20,
    )
    for index in range(20):
        gateway.get_exact(RUN_ALLOWLIST[index % 4])
    with pytest.raises(BoundedExecutionError) as excinfo:
        gateway.get_exact(RUN_ALLOWLIST[0])
    assert excinfo.value.code == BOUND_EXCEEDED
    assert len(client.calls) == 20
    assert gateway.counter.total == 20


def test_list_query_and_sweep_are_not_exposed() -> None:
    gateway, _ = _gateway()
    assert not hasattr(gateway, "list")
    assert not hasattr(gateway, "list_documents")
    assert not hasattr(gateway, "query")
    assert not hasattr(gateway, "stream")
    assert not hasattr(gateway, "sweep")


def test_precreate_and_postdelete_checks_count_as_reads(tmp_path: Path) -> None:
    gateway, client = _gateway()
    executor = At10BoundedExecutor(
        gateway,
        tmp_path,
        TEST_SHA,
        TEST_SHA,
        TEST_SHA,
    )
    result = executor.run(
        _load_projected_records("2026-08-15T16:00:00+00:00")
    )

    reads = [call for call in client.calls if call[0] == "read"]
    assert reads[:4] == [("read", run_id) for run_id in RUN_ALLOWLIST]
    assert reads[-4:] == [("read", run_id) for run_id in RUN_ALLOWLIST]
    assert result["COUNTERS"]["reads"] == 12
    assert result["COUNTERS"]["total"] == 20


def test_no_firestore_helper_bypasses_the_bounded_counter() -> None:
    runner_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "nw008"
        / "run_at10_bounded_execution.py"
    )
    tree = ast.parse(runner_path.read_text(encoding="utf-8"))
    network_calls: list[tuple[str, str]] = []
    counter_calls: list[tuple[str, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Call) or not isinstance(child.func, ast.Attribute):
                continue
            if (
                child.func.attr in {"create", "get", "delete"}
                and isinstance(child.func.value, ast.Name)
                and child.func.value.id == "document"
            ):
                network_calls.append((node.name, child.func.attr))
            if child.func.attr == "record":
                counter_calls.append((node.name, child.func.attr))

    assert network_calls == [
        ("_execute", "create"),
        ("_execute", "get"),
        ("_execute", "delete"),
    ]
    assert counter_calls == [("_execute", "record")]


def test_proof_counters_equal_executor_counters(tmp_path: Path) -> None:
    gateway, client = _gateway()
    executor = At10BoundedExecutor(
        gateway,
        tmp_path,
        TEST_SHA,
        TEST_SHA,
        TEST_SHA,
    )
    result = executor.run(
        _load_projected_records("2026-08-15T16:00:00+00:00")
    )
    expected = {
        "creates": 4,
        "reads": 12,
        "deletes": 4,
        "total": 20,
    }
    assert result["COUNTERS"] == expected
    assert len(client.calls) == expected["total"]

    manifest = json.loads((tmp_path / "at-10-run-manifest.json").read_text())
    records = json.loads((tmp_path / "at-10-record-evidence.json").read_text())
    cleanup = json.loads((tmp_path / "at-10-cleanup-evidence.json").read_text())
    proof_return = yaml.safe_load((tmp_path / "proof-return.yaml").read_text())

    assert manifest["COUNTERS"] == expected
    assert records["COUNTERS"] == expected
    assert cleanup["COUNTERS"] == expected
    assert proof_return["DOCUMENT_CREATES"] == expected["creates"]
    assert proof_return["DOCUMENT_READS"] == expected["reads"]
    assert proof_return["DOCUMENT_DELETES"] == expected["deletes"]
    assert proof_return["FIRESTORE_NETWORK_OPERATIONS"] == expected["total"]
    assert manifest["AT10_COMPLETE"] == "NO"
    assert records["AT10_COMPLETE"] == "NO"
    assert cleanup["AT10_COMPLETE"] == "NO"
    assert proof_return["AT10_COMPLETE"] == "NO"
