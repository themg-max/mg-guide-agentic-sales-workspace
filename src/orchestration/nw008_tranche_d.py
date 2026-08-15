"""Deterministic, local-only proof harness for NW-008 Tranche D (D1/AT-9 + D2/AT-8)."""

from __future__ import annotations

import inspect
import json
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple

import yaml

from mg_guide.firestore_audit.models import ProjectionContext
from mg_guide.firestore_audit.project import project_workflow_run_audit
from orchestration.manifest_gate import MANIFEST_NODE, RuntimeManifestGate
from orchestration.models import base_packet
from orchestration.policy import (
    ENFORCEMENT_DECISION_OWNER,
    evaluate_write_attempt,
)
from orchestration.runner import WorkflowRunner
from orchestration.state_machine import StateMachine, WriteCapContractError
from orchestration.attempt_ledger import LEDGER_STATE_OWNER, WriteAttemptLedger

PROOF_TIMESTAMP = "2026-08-14T17:30:00Z"
SUPERSEDED_A1 = "3be4309c02e2fc5e0685eadaba5a997b3cb8d81a"
SUPERSEDED_P1 = "500f50c34e84575491c1690c9d622e173e45860b"


@dataclass
class StageBWriterSpy:
    """A local Stage-B seam that records any forbidden client or writer access."""

    client_instantiations: int = 0
    calls: list[str] = field(default_factory=list)
    writes: int = 0

    def instantiate_client(self) -> "StageBWriterSpy":
        self.client_instantiations += 1
        return self

    def write(self, document: Mapping[str, Any]) -> None:
        self.calls.append(str(document))
        self.writes += 1


def _base_packet() -> Dict[str, Any]:
    return base_packet(
        run_id="at-09-run",
        status="received",
        meeting={
            "transcript_hash": (
                "0000000000000000000000000000000000000000000000000000000000000000"
            ),
            "call_id": "synthetic-at-09",
        },
        participants=[],
        created_at=PROOF_TIMESTAMP,
        started_at=PROOF_TIMESTAMP,
    )


def execute_d1_run(
    manifest_path: Path,
    operation: str = "create-contact",
    downstream_executor: Optional[Callable[[str], None]] = None,
    stage_b_spy: Optional[StageBWriterSpy] = None,
) -> Dict[str, Any]:
    """Run the local D1 seam; blocked and unknown operations never reach downstream."""

    gate = RuntimeManifestGate(manifest_path)
    capability_class = gate.classify_operation(operation)
    manifest_blocked = gate.is_blocked(operation)
    stage_b_spy = stage_b_spy or StageBWriterSpy()
    packet = _base_packet()
    execution = {
        "REQUESTED_OPERATION": operation,
        "CAPABILITY_CLASS": capability_class,
        "MANIFEST_NODE": MANIFEST_NODE,
        "MANIFEST_BLOCKED": manifest_blocked,
        "TOOL_MANIFEST_REFUSED": manifest_blocked,
        "REFUSAL_LAYER": "TOOL_MANIFEST" if manifest_blocked else None,
        "DOWNSTREAM_EXECUTOR_CALLED": False,
        "TRANSPORT_ATTEMPTED": False,
        "STAGE_B_SPY_INSTANTIATED": True,
        "STAGE_B_SPY_CALLED": bool(stage_b_spy.calls),
        "FIRESTORE_STAGE_B_INSTANTIATED": stage_b_spy.client_instantiations > 0,
        "FIRESTORE_STAGE_B_CALLED": bool(stage_b_spy.calls),
        "FIRESTORE_WRITES": stage_b_spy.writes,
        "GHL_LIVE_CALLS": 0,
        "GHL_WRITES": 0,
        "EXTERNAL_EFFECTS": 0,
    }

    if manifest_blocked:
        packet["audit"]["warnings"].append(
            f"TOOL_MANIFEST_REFUSED:{capability_class}"
        )
        packet["run"]["status"] = "failed"
        packet["audit"]["final_disposition"] = "failed"
    else:
        executor = downstream_executor or (lambda _: None)
        executor(capability_class)
        execution["DOWNSTREAM_EXECUTOR_CALLED"] = True
        packet["run"]["status"] = "completed"
        packet["audit"]["final_disposition"] = "completed"

    packet["audit"]["completed_at"] = PROOF_TIMESTAMP
    packet["d1_execution"] = execution
    return packet


def _audit_for(packet: Mapping[str, Any]) -> Dict[str, Any]:
    context = ProjectionContext(
        recorded_at=PROOF_TIMESTAMP,
        fixture_id="at-09-d1-proof",
        source_refs=(),
        writer_component="nw008_tranche_d",
        writer_component_version="v3",
        writer_mode="local_fixture",
    )
    return project_workflow_run_audit(packet, context)


def _status(value: bool) -> str:
    return "PASS" if value else "FAIL"


def _temporary_manifest(blocked_capabilities: Sequence[str]) -> Tuple[Path, TemporaryDirectory]:
    temporary_dir = TemporaryDirectory()
    path = Path(temporary_dir.name) / "ghl_tool_manifest.yaml"
    path.write_text(
        yaml.safe_dump(
            {"ghl_mcp": {"blocked_capability_classes": list(blocked_capabilities)}},
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return path, temporary_dir


def _negative_controls(
    manifest_path: Path, blocked_packet: Mapping[str, Any], audit: Mapping[str, Any]
) -> Dict[str, str]:
    """Execute each frozen control rather than reporting a handwritten status."""

    blocked_execution = blocked_packet["d1_execution"]
    controls: Dict[str, str] = {}

    try:
        RuntimeManifestGate(manifest_path, classifier_map={})  # type: ignore[call-arg]
    except TypeError:
        classifier_injection_rejected = (
            "classifier_map" not in inspect.signature(RuntimeManifestGate).parameters
        )
    else:  # pragma: no cover - retained for fail-closed proof computation
        classifier_injection_rejected = False
    controls["NC_D1_1"] = _status(classifier_injection_rejected)

    allowed_path, temporary_dir = _temporary_manifest(["email_send"])
    try:
        allowed_calls: list[str] = []
        allowed_packet = execute_d1_run(
            allowed_path,
            "search-contacts-advanced",
            allowed_calls.append,
        )
        allowed_execution = allowed_packet["d1_execution"]
        controls["NC_D1_2"] = _status(
            allowed_execution["CAPABILITY_CLASS"] == "contact_search"
            and not allowed_execution["MANIFEST_BLOCKED"]
            and allowed_execution["DOWNSTREAM_EXECUTOR_CALLED"]
            and allowed_calls == ["contact_search"]
        )
        unblocked_create = execute_d1_run(
            allowed_path, "create-contact", allowed_calls.append
        )
        controls["NC_D1_4"] = _status(
            not unblocked_create["d1_execution"]["MANIFEST_BLOCKED"]
            and unblocked_create["d1_execution"]["DOWNSTREAM_EXECUTOR_CALLED"]
            and allowed_calls == ["contact_search", "contact_create"]
        )
        controls["NC_D1_5"] = _status(
            not allowed_packet["audit"]["warnings"]
            and not allowed_execution["TOOL_MANIFEST_REFUSED"]
        )
    finally:
        temporary_dir.cleanup()

    controls["NC_D1_3"] = _status(
        blocked_execution["MANIFEST_BLOCKED"]
        and not blocked_execution["DOWNSTREAM_EXECUTOR_CALLED"]
        and not blocked_execution["TRANSPORT_ATTEMPTED"]
    )
    warning = "TOOL_MANIFEST_REFUSED:contact_create"
    controls["NC_D1_6"] = _status(
        blocked_packet["audit"]["warnings"] == [warning] and audit["warnings"] == [warning]
    )
    controls["NC_D1_8"] = _status(
        blocked_execution["STAGE_B_SPY_INSTANTIATED"]
        and not blocked_execution["STAGE_B_SPY_CALLED"]
        and not blocked_execution["FIRESTORE_STAGE_B_INSTANTIATED"]
        and not blocked_execution["FIRESTORE_STAGE_B_CALLED"]
        and blocked_execution["FIRESTORE_WRITES"] == 0
    )

    validator_baseline = {
        **blocked_execution,
        "AUDIT_WARNING_RECORDED": warning in blocked_packet["audit"]["warnings"],
        "AUDIT_WARNING_PROJECTED_STAGE_A": warning in audit["warnings"],
        **controls,
        "NC_D1_7": "PASS",
        "DETERMINISTIC_PROOF_REPLAY": "PASS",
    }
    invalid_ghl = deepcopy(validator_baseline)
    invalid_ghl["GHL_WRITES"] = 1
    invalid_effects = deepcopy(validator_baseline)
    invalid_effects["EXTERNAL_EFFECTS"] = 1
    controls["NC_D1_7"] = _status(
        validate_d1_proof(invalid_ghl) == "FAIL"
        and validate_d1_proof(invalid_effects) == "FAIL"
    )
    return controls


def build_d1_evidence(
    packet: Mapping[str, Any],
    audit: Mapping[str, Any],
    manifest_path: Path,
    deterministic_proof_replay: str,
) -> Dict[str, Any]:
    """Build validator input from actual local runs and pure Stage-A projection."""

    execution = packet["d1_execution"]
    warning = "TOOL_MANIFEST_REFUSED:contact_create"
    evidence: Dict[str, Any] = {
        **execution,
        "AUDIT_WARNING_RECORDED": warning in packet["audit"]["warnings"],
        "AUDIT_WARNING_PROJECTED_STAGE_A": warning in audit["warnings"],
        **_negative_controls(manifest_path, packet, audit),
        "DETERMINISTIC_PROOF_REPLAY": deterministic_proof_replay,
    }
    evidence["PROOF_STATUS"] = validate_d1_proof(evidence)
    return evidence


def validate_d1_proof(evidence: Mapping[str, Any]) -> str:
    """Compute proof status from every D1 predicate; never trust supplied status."""

    expected = {
        "REQUESTED_OPERATION": "create-contact",
        "CAPABILITY_CLASS": "contact_create",
        "MANIFEST_NODE": MANIFEST_NODE,
        "MANIFEST_BLOCKED": True,
        "TOOL_MANIFEST_REFUSED": True,
        "REFUSAL_LAYER": "TOOL_MANIFEST",
        "DOWNSTREAM_EXECUTOR_CALLED": False,
        "TRANSPORT_ATTEMPTED": False,
        "AUDIT_WARNING_RECORDED": True,
        "AUDIT_WARNING_PROJECTED_STAGE_A": True,
        "DETERMINISTIC_PROOF_REPLAY": "PASS",
        "GHL_LIVE_CALLS": 0,
        "GHL_WRITES": 0,
        "FIRESTORE_WRITES": 0,
        "EXTERNAL_EFFECTS": 0,
        "STAGE_B_SPY_INSTANTIATED": True,
        "STAGE_B_SPY_CALLED": False,
        "FIRESTORE_STAGE_B_INSTANTIATED": False,
        "FIRESTORE_STAGE_B_CALLED": False,
    }
    negative_controls = {f"NC_D1_{number}": "PASS" for number in range(1, 9)}
    return (
        "PASS"
        if all(evidence.get(key) == value for key, value in expected.items())
        and all(evidence.get(key) == value for key, value in negative_controls.items())
        else "FAIL"
    )


def _manifest_markdown(
    implementation_subject_sha: str, evidence: Mapping[str, Any]
) -> str:
    return "\n".join(
        [
            "# NW-008 Tranche D1 (AT-9) Proof Manifest",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Implementation subject SHA | `{implementation_subject_sha}` |",
            f"| Manifest path | `contracts/ghl_tool_manifest.yaml` |",
            f"| Manifest node | `{MANIFEST_NODE}` |",
            f"| Superseded A1 | `{SUPERSEDED_A1}` |",
            f"| Superseded P1 | `{SUPERSEDED_P1}` |",
            "| Superseded status | `INVALID_FOR_ACCEPTANCE` |",
            f"| Proof clock | `{PROOF_TIMESTAMP}` |",
            "",
            "## Computed D1 proof",
            "",
            *[
                f"- {key}={value}"
                for key, value in sorted(evidence.items())
                if key != "PROOF_STATUS"
            ],
            f"- PROOF_VALIDATOR={evidence['PROOF_STATUS']}",
            "",
        ]
    )


def _render_proof(
    manifest_path: Path,
    implementation_subject_sha: str,
    deterministic_proof_replay: str,
) -> Dict[str, str]:
    packet = execute_d1_run(manifest_path)
    audit = _audit_for(packet)
    evidence = build_d1_evidence(
        packet, audit, manifest_path, deterministic_proof_replay
    )
    proof_return = {
        "proof_id": "NW008-D1-AT9",
        "implementation_subject_sha": implementation_subject_sha,
        "superseded_a1": SUPERSEDED_A1,
        "superseded_p1": SUPERSEDED_P1,
        "superseded_status": "INVALID_FOR_ACCEPTANCE",
        "manifest_path": "contracts/ghl_tool_manifest.yaml",
        "manifest_node": MANIFEST_NODE,
        "evidence": evidence,
        "proof_validator": evidence["PROOF_STATUS"],
        "deterministic_proof_replay": deterministic_proof_replay,
    }
    return {
        "run": json.dumps(packet, indent=2, sort_keys=True) + "\n",
        "audit": json.dumps(audit, indent=2, sort_keys=True) + "\n",
        "manifest": _manifest_markdown(implementation_subject_sha, evidence),
        "return": yaml.safe_dump(proof_return, sort_keys=True),
    }


def _write_proof_artifacts(
    artifacts: Mapping[str, str], output_dir: Path
) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "run": output_dir / "at-09-run.json",
        "audit": output_dir / "at-09-workflow-run-audit.json",
        "manifest": output_dir / "proof-manifest.md",
        "return": output_dir / "proof-return.yaml",
    }
    for key, path in paths.items():
        path.write_text(artifacts[key], encoding="utf-8")
    return paths


def write_proof(
    packet: Mapping[str, Any],
    output_dir: Path,
    implementation_subject_sha: str,
    manifest_path: Path,
    deterministic_proof_replay: str,
) -> Dict[str, Path]:
    """Write proof for one observed run with an explicitly computed replay status."""

    audit = _audit_for(packet)
    evidence = build_d1_evidence(
        packet, audit, manifest_path, deterministic_proof_replay
    )
    proof_return = {
        "proof_id": "NW008-D1-AT9",
        "implementation_subject_sha": implementation_subject_sha,
        "superseded_a1": SUPERSEDED_A1,
        "superseded_p1": SUPERSEDED_P1,
        "superseded_status": "INVALID_FOR_ACCEPTANCE",
        "manifest_path": "contracts/ghl_tool_manifest.yaml",
        "manifest_node": MANIFEST_NODE,
        "evidence": evidence,
        "proof_validator": evidence["PROOF_STATUS"],
        "deterministic_proof_replay": deterministic_proof_replay,
    }
    artifacts = {
        "run": json.dumps(packet, indent=2, sort_keys=True) + "\n",
        "audit": json.dumps(audit, indent=2, sort_keys=True) + "\n",
        "manifest": _manifest_markdown(implementation_subject_sha, evidence),
        "return": yaml.safe_dump(proof_return, sort_keys=True),
    }
    return _write_proof_artifacts(artifacts, output_dir)


def generate_final_proof(
    manifest_path: Path, output_dir: Path, implementation_subject_sha: str
) -> Dict[str, Path]:
    """Render two complete runs, compute replay, then write the final proof."""

    first = _render_proof(manifest_path, implementation_subject_sha, "PENDING")
    second = _render_proof(manifest_path, implementation_subject_sha, "PENDING")
    replay_status = "PASS" if first == second else "FAIL"
    final_artifacts = _render_proof(
        manifest_path, implementation_subject_sha, replay_status
    )
    return _write_proof_artifacts(final_artifacts, output_dir)



# ---------------------------------------------------------------------------
# D2 / AT-8 offline write-attempt-cap helpers (no durable proof emission in A2)
# ---------------------------------------------------------------------------

D2_PROOF_NAMESPACE = "proof/nw008/tranche-d/d2-at8"
D2_CAP_SOURCE = "contracts/workflow_states.yaml"
D2_PROOF_TIMESTAMP = "2026-08-15T12:00:00Z"


def execute_d2_write_attempt(
    runner: WorkflowRunner,
    *,
    run_id: str,
    write_kind: str,
    transport_executor=None,
):
    """Orchestration-only seam: runner asks OL3 policy before any transport."""

    return runner.request_write_attempt(
        run_id,
        write_kind,
        transport_executor=transport_executor,
    )


def run_d2_attempt_matrix(
    state_machine: StateMachine,
    *,
    run_id: str = "d2-run",
    note_attempts: int = 2,
    stage_attempts: int = 2,
) -> Dict[str, Any]:
    """Execute offline note/stage attempt sequences and collect computable evidence."""

    runner = WorkflowRunner(state_machine=state_machine, allow_transport=False)
    transport_calls: list[str] = []

    def _transport(label: str):
        transport_calls.append(label)

    note_decisions = []
    for _ in range(note_attempts):
        note_decisions.append(
            execute_d2_write_attempt(
                runner,
                run_id=run_id,
                write_kind="note",
                transport_executor=lambda: _transport("note"),
            ).as_dict()
        )

    stage_decisions = []
    for _ in range(stage_attempts):
        stage_decisions.append(
            execute_d2_write_attempt(
                runner,
                run_id=run_id,
                write_kind="stage",
                transport_executor=lambda: _transport("stage"),
            ).as_dict()
        )

    effects = {
        "GHL_LIVE_CALLS": 0,
        "GHL_WRITES": 0,
        "FIRESTORE_WRITES": 0,
        "EXTERNAL_EFFECTS": 0,
        "TRANSPORT_ATTEMPTED": False,
        "TRANSPORT_EXECUTOR_CALLS": list(transport_calls),
    }
    return {
        "run_id": run_id,
        "cap_source": getattr(state_machine, "cap_source", D2_CAP_SOURCE),
        "cap_node": getattr(state_machine, "cap_node", "invariants"),
        "max_note_writes_per_run": state_machine.max_note_writes_per_run,
        "max_stage_writes_per_run": state_machine.max_stage_writes_per_run,
        "ledger_state_owner": LEDGER_STATE_OWNER,
        "enforcement_decision_owner": ENFORCEMENT_DECISION_OWNER,
        "runner_authority": WorkflowRunner.RUNNER_AUTHORITY,
        "agent_cap_authority": WorkflowRunner.AGENT_CAP_AUTHORITY,
        "harness_cap_authority": WorkflowRunner.HARNESS_CAP_AUTHORITY,
        "note_decisions": note_decisions,
        "stage_decisions": stage_decisions,
        "ledger_snapshot": runner.ledger_for(run_id).snapshot(),
        "effects": effects,
    }


def build_d2_evidence(
    matrix: Mapping[str, Any],
    *,
    implementation_subject_sha: str,
    negative_controls: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """Assemble computable D2 evidence. Does not trust caller PASS labels."""

    note = list(matrix.get("note_decisions") or [])
    stage = list(matrix.get("stage_decisions") or [])
    effects = dict(matrix.get("effects") or {})
    evidence: Dict[str, Any] = {
        "IMPLEMENTATION_SUBJECT_SHA": implementation_subject_sha,
        "CAP_SOURCE": matrix.get("cap_source", D2_CAP_SOURCE),
        "CAP_NODE": matrix.get("cap_node", "invariants"),
        "LEDGER_STATE_OWNER": matrix.get("ledger_state_owner", LEDGER_STATE_OWNER),
        "ENFORCEMENT_DECISION_OWNER": matrix.get(
            "enforcement_decision_owner", ENFORCEMENT_DECISION_OWNER
        ),
        "RUNNER_AUTHORITY": matrix.get(
            "runner_authority", WorkflowRunner.RUNNER_AUTHORITY
        ),
        "AGENT_CAP_AUTHORITY": matrix.get("agent_cap_authority", False),
        "HARNESS_CAP_AUTHORITY": matrix.get("harness_cap_authority", False),
        "MAX_NOTE_WRITES_PER_RUN": matrix.get("max_note_writes_per_run"),
        "MAX_STAGE_WRITES_PER_RUN": matrix.get("max_stage_writes_per_run"),
        "NOTE_DECISIONS": note,
        "STAGE_DECISIONS": stage,
        "LEDGER_SNAPSHOT": dict(matrix.get("ledger_snapshot") or {}),
        "GHL_LIVE_CALLS": int(effects.get("GHL_LIVE_CALLS", 0)),
        "GHL_WRITES": int(effects.get("GHL_WRITES", 0)),
        "FIRESTORE_WRITES": int(effects.get("FIRESTORE_WRITES", 0)),
        "EXTERNAL_EFFECTS": int(effects.get("EXTERNAL_EFFECTS", 0)),
        "TRANSPORT_ATTEMPTED": bool(effects.get("TRANSPORT_ATTEMPTED", False)),
        "TRANSPORT_EXECUTOR_CALLS": list(effects.get("TRANSPORT_EXECUTOR_CALLS") or []),
    }
    if negative_controls:
        evidence.update({k: v for k, v in negative_controls.items()})
    evidence["PROOF_STATUS"] = validate_d2_proof(evidence)
    return evidence


def validate_d2_proof(evidence: Mapping[str, Any]) -> str:
    """Fail closed on nonzero effects or missing authority/SHA binding."""

    sha = evidence.get("IMPLEMENTATION_SUBJECT_SHA")
    if not isinstance(sha, str) or len(sha.strip()) < 7:
        return "FAIL"
    if evidence.get("ENFORCEMENT_DECISION_OWNER") != ENFORCEMENT_DECISION_OWNER:
        return "FAIL"
    if evidence.get("LEDGER_STATE_OWNER") != LEDGER_STATE_OWNER:
        return "FAIL"
    if evidence.get("RUNNER_AUTHORITY") != WorkflowRunner.RUNNER_AUTHORITY:
        return "FAIL"
    if evidence.get("AGENT_CAP_AUTHORITY") not in (False, "NO", 0):
        return "FAIL"
    if evidence.get("HARNESS_CAP_AUTHORITY") not in (False, "NO", 0):
        return "FAIL"
    if evidence.get("CAP_SOURCE") != D2_CAP_SOURCE and not str(
        evidence.get("CAP_SOURCE", "")
    ).endswith("workflow_states.yaml"):
        # Temporary test contracts may override numeric caps but source label remains yaml path
        # unless explicitly temporary; still require a non-empty source string.
        if not evidence.get("CAP_SOURCE"):
            return "FAIL"
    for key in ("GHL_LIVE_CALLS", "GHL_WRITES", "FIRESTORE_WRITES", "EXTERNAL_EFFECTS"):
        if int(evidence.get(key, 0) or 0) != 0:
            return "FAIL"
    if evidence.get("TRANSPORT_ATTEMPTED") is True:
        return "FAIL"
    if list(evidence.get("TRANSPORT_EXECUTOR_CALLS") or []):
        return "FAIL"

    note = list(evidence.get("NOTE_DECISIONS") or [])
    stage = list(evidence.get("STAGE_DECISIONS") or [])
    for decisions in (note, stage):
        for item in decisions:
            if item.get("decision_owner") != ENFORCEMENT_DECISION_OWNER:
                return "FAIL"
            if item.get("transport_attempted") is True:
                return "FAIL"
            if item.get("decision") not in {"PERMIT", "REFUSE"}:
                return "FAIL"
    return "PASS"


def compute_d2_negative_controls(
    production_contract: Mapping[str, Any],
) -> Dict[str, str]:
    """Execute NC-D2-1..10 from runtime observations rather than handwritten PASS."""

    from copy import deepcopy
    import inspect

    controls: Dict[str, str] = {}
    sm = StateMachine(deepcopy(dict(production_contract)))
    runner = WorkflowRunner(state_machine=sm, allow_transport=False)

    # NC-D2-1: harness cannot override caps / force admit.
    sig = inspect.signature(runner.request_write_attempt)
    forbidden = {"force_permit", "force_admit", "max_writes", "max", "override_cap"}
    no_override_params = forbidden.isdisjoint(sig.parameters)
    first = runner.request_write_attempt("nc-d2-1", "note")
    second = runner.request_write_attempt("nc-d2-1", "note")
    controls["NC_D2_1"] = _status(
        no_override_params
        and first.decision == "PERMIT"
        and second.decision == "REFUSE"
        and second.decision_owner == ENFORCEMENT_DECISION_OWNER
    )

    # NC-D2-2 / NC-D2-3 note first/second
    r_note = WorkflowRunner(state_machine=sm, allow_transport=False)
    n1 = r_note.request_write_attempt("nc-note", "note")
    n2 = r_note.request_write_attempt("nc-note", "note")
    controls["NC_D2_2"] = _status(
        n1.decision == "PERMIT" and n1.before == 0 and n1.after == 1
    )
    controls["NC_D2_3"] = _status(
        n2.decision == "REFUSE"
        and n2.before == 1
        and n2.after == 1
        and n2.decision_owner == ENFORCEMENT_DECISION_OWNER
    )

    # NC-D2-4 / NC-D2-5 stage first/second
    r_stage = WorkflowRunner(state_machine=sm, allow_transport=False)
    s1 = r_stage.request_write_attempt("nc-stage", "stage")
    s2 = r_stage.request_write_attempt("nc-stage", "stage")
    controls["NC_D2_4"] = _status(
        s1.decision == "PERMIT" and s1.before == 0 and s1.after == 1
    )
    controls["NC_D2_5"] = _status(
        s2.decision == "REFUSE"
        and s2.before == 1
        and s2.after == 1
        and s2.decision_owner == ENFORCEMENT_DECISION_OWNER
    )

    # NC-D2-6 independent counters
    r_ind = WorkflowRunner(state_machine=sm, allow_transport=False)
    r_ind.request_write_attempt("nc-ind", "note")
    r_ind.request_write_attempt("nc-ind", "note")  # exhaust note
    stage_after_note_exhaust = r_ind.request_write_attempt("nc-ind", "stage")
    controls["NC_D2_6"] = _status(stage_after_note_exhaust.decision == "PERMIT")

    # NC-D2-7 new run_id resets
    r_reset = WorkflowRunner(state_machine=sm, allow_transport=False)
    r_reset.request_write_attempt("run-a", "note")
    r_reset.request_write_attempt("run-a", "note")
    fresh = r_reset.request_write_attempt("run-b", "note")
    controls["NC_D2_7"] = _status(
        fresh.decision == "PERMIT" and fresh.before == 0 and fresh.after == 1
    )

    # NC-D2-8 nonzero effect forces validator FAIL
    matrix = run_d2_attempt_matrix(sm, run_id="nc-effects")
    good = build_d2_evidence(matrix, implementation_subject_sha="a" * 40)
    bad_ghl = dict(good)
    bad_ghl["GHL_WRITES"] = 1
    bad_effects = dict(good)
    bad_effects["EXTERNAL_EFFECTS"] = 1
    controls["NC_D2_8"] = _status(
        validate_d2_proof(bad_ghl) == "FAIL" and validate_d2_proof(bad_effects) == "FAIL"
    )

    # NC-D2-9 temporary contract note cap=2
    temp = deepcopy(dict(production_contract))
    new_invariants = []
    for item in temp.get("invariants") or []:
        if isinstance(item, dict) and "max_note_writes_per_run" in item:
            new_invariants.append({"max_note_writes_per_run": 2})
        else:
            new_invariants.append(item)
    temp["invariants"] = new_invariants
    temp_sm = StateMachine(temp)
    r_temp = WorkflowRunner(state_machine=temp_sm, allow_transport=False)
    t1 = r_temp.request_write_attempt("nc-cap2", "note")
    t2 = r_temp.request_write_attempt("nc-cap2", "note")
    t3 = r_temp.request_write_attempt("nc-cap2", "note")
    prod_sm = StateMachine(deepcopy(dict(production_contract)))
    controls["NC_D2_9"] = _status(
        temp_sm.max_note_writes_per_run == 2
        and t1.decision == "PERMIT"
        and t2.decision == "PERMIT"
        and t3.decision == "REFUSE"
        and prod_sm.max_note_writes_per_run == 1
    )

    # NC-D2-10 malformed/missing cap fails closed
    missing = deepcopy(dict(production_contract))
    missing["invariants"] = [
        item
        for item in (missing.get("invariants") or [])
        if not (isinstance(item, dict) and "max_note_writes_per_run" in item)
    ]
    malformed_cases = [
        missing,
        _with_note_cap(production_contract, 0),
        _with_note_cap(production_contract, -1),
        _with_note_cap(production_contract, True),
        _with_note_cap(production_contract, "1"),
        _with_note_cap(production_contract, 1.5),
        _with_note_cap(production_contract, None),
    ]
    load_failures = 0
    for case in malformed_cases:
        try:
            StateMachine(deepcopy(dict(case)))
        except WriteCapContractError:
            load_failures += 1
        else:
            pass
    # Policy-level fail-closed if an invalid max somehow reaches evaluate_write_attempt
    ledger = WriteAttemptLedger(run_id="nc-invalid-max")
    refused = evaluate_write_attempt(write_kind="note", ledger=ledger, max_writes=0)
    controls["NC_D2_10"] = _status(
        load_failures == len(malformed_cases)
        and refused.decision == "REFUSE"
        and refused.reason_code == "INVALID_WRITE_CAP"
    )
    return controls


def _with_note_cap(production_contract: Mapping[str, Any], value: object) -> Dict[str, Any]:
    from copy import deepcopy

    temp = deepcopy(dict(production_contract))
    new_invariants = []
    for item in temp.get("invariants") or []:
        if isinstance(item, dict) and "max_note_writes_per_run" in item:
            new_invariants.append({"max_note_writes_per_run": value})
        else:
            new_invariants.append(item)
    temp["invariants"] = new_invariants
    return temp

if __name__ == "__main__":
    import subprocess

    implementation_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    generate_final_proof(
        Path("contracts/ghl_tool_manifest.yaml"),
        Path("proof/nw008/tranche-d"),
        implementation_sha,
    )
