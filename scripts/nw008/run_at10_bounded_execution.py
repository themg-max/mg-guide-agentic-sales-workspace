#!/usr/bin/env python3
"""Governed NW-008 AT-10 bounded Firestore execution runner.

This runner does not grant its own execution authority. It requires a separate
human-approved authorization artifact bound to the exact implementation subject
and execution code SHA before it creates a Firestore client.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mg_guide.firestore_audit.acceptance_demo import (  # noqa: E402
    validate_exact_audit_field_paths,
    verify_fingerprint_gate,
)
from mg_guide.firestore_audit.models import ProjectionContext  # noqa: E402
from mg_guide.firestore_audit.project import project_workflow_run_audit  # noqa: E402

PROJECT = "mg-devpost"
DATABASE = "devpost-google-contest"
LOCATION = "us-east4"
COLLECTION = "workflow_runs"

RUN_ALLOWLIST = (
    "run_nw006_success_001",
    "run_nw006_stage_denied_001",
    "run_nw006_ambiguous_contact_001",
    "run_nw006_failed_001",
)
PACKET_BY_RUN_ID = {
    "run_nw006_success_001": "packet-success.completed.json",
    "run_nw006_stage_denied_001": "packet-stage-change-denied.completed_with_review.json",
    "run_nw006_ambiguous_contact_001": "packet-ambiguous-contact.blocked.json",
    "run_nw006_failed_001": "packet-tool-failure.failed.json",
}

MAX_CREATES = 4
MAX_READS = 12
MAX_DELETES = 4
MAX_TOTAL_OPERATIONS = 20
MAX_EXECUTION_SECONDS = 10 * 60

DEFAULT_PROOF_DIR = REPO_ROOT / "proof" / "nw008" / "at-10" / "rerun-execution"
EXECUTION_SOURCE_PATHS = (
    "scripts/nw008/run_at10_bounded_execution.py",
    "src/mg_guide/firestore_audit",
    "contracts/workflow_run_audit.schema.json",
    "fixtures/nw005/packets",
)

BOUND_EXCEEDED = "BOUND_EXCEEDED"
GOVERNANCE_REJECTED = "GOVERNANCE_REJECTED"
OPERATION_PROHIBITED = "OPERATION_PROHIBITED"
LIFECYCLE_REJECTED = "LIFECYCLE_REJECTED"


class BoundedExecutionError(RuntimeError):
    """Fail-closed runner error with a stable governance code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass
class OperationCounter:
    """Single counter for every Firestore operation in one executor lifecycle."""

    max_creates: int = MAX_CREATES
    max_reads: int = MAX_READS
    max_deletes: int = MAX_DELETES
    max_total: int = MAX_TOTAL_OPERATIONS
    max_seconds: float = MAX_EXECUTION_SECONDS
    clock: Callable[[], float] = time.monotonic
    creates: int = field(default=0, init=False)
    reads: int = field(default=0, init=False)
    deletes: int = field(default=0, init=False)
    _started_at: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._started_at = self.clock()

    @property
    def total(self) -> int:
        return self.creates + self.reads + self.deletes

    def ensure_within_deadline(self) -> None:
        if self.clock() - self._started_at > self.max_seconds:
            raise BoundedExecutionError(
                BOUND_EXCEEDED,
                f"execution duration exceeded {self.max_seconds:g} seconds",
            )

    def record(self, operation: str) -> None:
        """Reserve one operation before the corresponding network call."""
        self.ensure_within_deadline()
        limits = {
            "create": ("creates", self.max_creates),
            "read": ("reads", self.max_reads),
            "delete": ("deletes", self.max_deletes),
        }
        if operation not in limits:
            raise BoundedExecutionError(
                OPERATION_PROHIBITED,
                f"Firestore operation {operation!r} is not create/get/delete",
            )
        attribute, limit = limits[operation]
        if getattr(self, attribute) >= limit:
            raise BoundedExecutionError(
                BOUND_EXCEEDED,
                f"{operation} cap {limit} would be exceeded",
            )
        if self.total >= self.max_total:
            raise BoundedExecutionError(
                BOUND_EXCEEDED,
                f"total Firestore operation cap {self.max_total} would be exceeded",
            )
        setattr(self, attribute, getattr(self, attribute) + 1)

    def snapshot(self) -> Dict[str, int]:
        return {
            "creates": self.creates,
            "reads": self.reads,
            "deletes": self.deletes,
            "total": self.total,
        }


class BoundedFirestoreGateway:
    """Exact-path create/get/delete gateway with no collection access surface."""

    def __init__(self, client: Any, counter: OperationCounter) -> None:
        self.__client = client
        self.counter = counter

    @staticmethod
    def _guard_run_id(run_id: str) -> None:
        if run_id not in RUN_ALLOWLIST:
            raise BoundedExecutionError(
                GOVERNANCE_REJECTED,
                f"run_id={run_id!r} is outside the exact AT-10 allowlist",
            )

    def _execute(
        self,
        operation: str,
        run_id: str,
        payload: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """The only Firestore operation call site in this module."""
        self._guard_run_id(run_id)
        self.counter.record(operation)
        document = self.__client.collection(COLLECTION).document(run_id)
        if operation == "create":
            if payload is None:
                raise BoundedExecutionError(
                    LIFECYCLE_REJECTED,
                    "create requires an audit payload",
                )
            document.create(dict(payload))
            return {"run_id": run_id, "created": True}
        if operation == "read":
            snapshot = document.get()
            return snapshot.to_dict() if snapshot.exists else None
        if operation == "delete":
            document.delete()
            return {"run_id": run_id, "deleted": True}
        raise BoundedExecutionError(
            OPERATION_PROHIBITED,
            f"Firestore operation {operation!r} is prohibited",
        )

    def create_exact(self, run_id: str, audit: Mapping[str, Any]) -> None:
        self._execute("create", run_id, audit)

    def get_exact(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self._execute("read", run_id)

    def delete_exact(self, run_id: str) -> None:
        self._execute("delete", run_id)


def _run_git(arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _require_git_success(arguments: Sequence[str], failure: str) -> str:
    result = _run_git(arguments)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise BoundedExecutionError(GOVERNANCE_REJECTED, f"{failure}: {detail}")
    return result.stdout.strip()


def _require_git_blob(arguments: Sequence[str], failure: str) -> str:
    result = _run_git(arguments)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise BoundedExecutionError(GOVERNANCE_REJECTED, f"{failure}: {detail}")
    return result.stdout


def verify_source_binding(subject_sha: str, execution_code_sha: str) -> None:
    """Require runtime sources to match the reviewed implementation subject."""
    if subject_sha != execution_code_sha:
        raise BoundedExecutionError(
            GOVERNANCE_REJECTED,
            "EXECUTION_CODE_SHA must equal IMPLEMENTATION_SUBJECT_SHA",
        )
    if re.fullmatch(r"[0-9a-f]{40}", subject_sha) is None:
        raise BoundedExecutionError(
            GOVERNANCE_REJECTED,
            "implementation subject must be a full lowercase 40-character Git SHA",
        )

    _require_git_success(
        ["cat-file", "-e", f"{subject_sha}^{{commit}}"],
        "implementation subject commit is unavailable",
    )
    _require_git_success(
        ["merge-base", "--is-ancestor", subject_sha, "HEAD"],
        "implementation subject is not an ancestor of HEAD",
    )
    _require_git_success(
        ["diff", "--quiet", subject_sha, "--", *EXECUTION_SOURCE_PATHS],
        "runtime sources differ from the reviewed implementation subject",
    )
    _require_git_success(
        ["diff", "--quiet", "--", *EXECUTION_SOURCE_PATHS],
        "runtime sources contain unstaged changes",
    )
    _require_git_success(
        ["diff", "--cached", "--quiet", "--", *EXECUTION_SOURCE_PATHS],
        "runtime sources contain staged changes",
    )


ACTIVE_GRANT_BEGIN = "BEGIN_AT10_ACTIVE_GRANT"
ACTIVE_GRANT_END = "END_AT10_ACTIVE_GRANT"
ACTIVE_GRANT_DECISION = "AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION"
ACTIVE_GRANT_APPROVER_EMAIL = "themg@themiliare-group.com"
ACTIVE_GRANT_APPROVER_NAME = "AARON PRESTON CHANDLER"
APPROVED_AT_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)$"
)
ACTIVE_GRANT_LINE_PATTERN = re.compile(
    r"^(?P<key>[A-Z][A-Z0-9_]*)=(?P<value>.*)$"
)

# Closed field set. Unknown keys are rejected fail-closed.
ACTIVE_GRANT_ALLOWED_KEYS = frozenset(
    {
        "STATUS",
        "DECISION",
        "HUMAN_SIGNATURE",
        "HUMAN_APPROVER_EMAIL",
        "HUMAN_APPROVER_NAME",
        "APPROVED_AT",
        "AT10_EXECUTION_AUTHORIZED",
        "AT10_COMPLETION_CLAIM_AUTHORIZED",
        "AT10_COMPLETE",
        "IMPLEMENTATION_SUBJECT_SHA",
        "EXECUTION_CODE_SHA",
        "PROJECT",
        "DATABASE",
        "LOCATION",
        "COLLECTION",
        "RUN_ALLOWLIST",
        "MAX_DISTINCT_RUN_IDS",
        "MAX_DOCUMENT_CREATES",
        "MAX_DOCUMENT_READS",
        "MAX_DOCUMENT_DELETES",
        "MAX_NETWORK_CALLS",
        "MAX_EXECUTION_MINUTES",
        "FIRESTORE_LIST_AUTHORIZED",
        "FIRESTORE_QUERY_AUTHORIZED",
        "COLLECTION_SWEEP_AUTHORIZED",
        "OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED",
        "PR53_AUTHORITY_REUSABLE",
    }
)


def _reject_grant(message: str) -> None:
    raise BoundedExecutionError(GOVERNANCE_REJECTED, message)


def extract_active_grant_block(text: str) -> str:
    """Return the body of the single canonical ACTIVE GRANT block."""
    begin_token = ACTIVE_GRANT_BEGIN
    end_token = ACTIVE_GRANT_END
    begins = [match.start() for match in re.finditer(re.escape(begin_token), text)]
    ends = [match.start() for match in re.finditer(re.escape(end_token), text)]
    if len(begins) == 0 or len(ends) == 0:
        _reject_grant("authorization artifact must contain exactly one ACTIVE GRANT block")
    if len(begins) != 1 or len(ends) != 1:
        _reject_grant("authorization artifact must contain exactly one ACTIVE GRANT block")

    begin_at = begins[0]
    end_at = ends[0]
    begin_line_end = text.find("\n", begin_at)
    if begin_line_end < 0:
        _reject_grant("ACTIVE GRANT begin marker is malformed")
    if end_at <= begin_line_end:
        _reject_grant("ACTIVE GRANT end marker must follow the begin marker")

    # Ensure markers occupy their own lines (allow surrounding whitespace only).
    begin_line_start = text.rfind("\n", 0, begin_at) + 1
    begin_line = text[begin_line_start:begin_line_end].strip()
    if begin_line != begin_token:
        _reject_grant("ACTIVE GRANT begin marker must occupy its own line")

    end_line_end = text.find("\n", end_at)
    if end_line_end < 0:
        end_line_end = len(text)
    end_line_start = text.rfind("\n", 0, end_at) + 1
    end_line = text[end_line_start:end_line_end].strip()
    if end_line != end_token:
        _reject_grant("ACTIVE GRANT end marker must occupy its own line")

    return text[begin_line_end + 1 : end_line_start]


def parse_active_grant_fields(block_body: str) -> Dict[str, str]:
    """Parse KEY=VALUE fields from one ACTIVE GRANT body fail-closed."""
    fields: Dict[str, str] = {}
    for raw_line in block_body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = ACTIVE_GRANT_LINE_PATTERN.fullmatch(line)
        if match is None:
            _reject_grant(f"ACTIVE GRANT contains malformed line {raw_line!r}")
        key = match.group("key")
        value = match.group("value")
        if key not in ACTIVE_GRANT_ALLOWED_KEYS:
            _reject_grant(f"ACTIVE GRANT contains unknown field {key!r}")
        if key in fields:
            _reject_grant(f"ACTIVE GRANT contains duplicate key {key!r}")
        if value != value.strip() or value == "":
            _reject_grant(f"ACTIVE GRANT field {key!r} has a malformed value")
        fields[key] = value
    return fields


def validate_active_grant_fields(
    fields: Mapping[str, str],
    subject_sha: str,
    execution_code_sha: str,
) -> Dict[str, str]:
    """Require the canonical approved ACTIVE GRANT field set."""
    required = {
        "STATUS": "HUMAN_APPROVED",
        "DECISION": ACTIVE_GRANT_DECISION,
        "HUMAN_SIGNATURE": "APPROVED",
        "HUMAN_APPROVER_EMAIL": ACTIVE_GRANT_APPROVER_EMAIL,
        "HUMAN_APPROVER_NAME": ACTIVE_GRANT_APPROVER_NAME,
        "AT10_EXECUTION_AUTHORIZED": "YES",
        "AT10_COMPLETION_CLAIM_AUTHORIZED": "NO",
        "AT10_COMPLETE": "NO",
        "IMPLEMENTATION_SUBJECT_SHA": subject_sha,
        "EXECUTION_CODE_SHA": execution_code_sha,
        "PROJECT": PROJECT,
        "DATABASE": DATABASE,
        "LOCATION": LOCATION,
        "COLLECTION": COLLECTION,
        "RUN_ALLOWLIST": ",".join(RUN_ALLOWLIST),
        "MAX_DISTINCT_RUN_IDS": str(len(RUN_ALLOWLIST)),
        "MAX_DOCUMENT_CREATES": str(MAX_CREATES),
        "MAX_DOCUMENT_READS": str(MAX_READS),
        "MAX_DOCUMENT_DELETES": str(MAX_DELETES),
        "MAX_NETWORK_CALLS": str(MAX_TOTAL_OPERATIONS),
        "MAX_EXECUTION_MINUTES": "10",
        "FIRESTORE_LIST_AUTHORIZED": "NO",
        "FIRESTORE_QUERY_AUTHORIZED": "NO",
        "COLLECTION_SWEEP_AUTHORIZED": "NO",
        "OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED": "NO",
        "PR53_AUTHORITY_REUSABLE": "NO",
    }

    expected_keys = set(required) | {"APPROVED_AT"}
    missing_keys = sorted(expected_keys - set(fields))
    if missing_keys:
        _reject_grant(f"ACTIVE GRANT is missing required field {missing_keys[0]!r}")

    extra_keys = sorted(set(fields) - expected_keys)
    if extra_keys:
        _reject_grant(f"ACTIVE GRANT contains unknown field {extra_keys[0]!r}")

    decision = fields.get("DECISION", "")
    if decision != ACTIVE_GRANT_DECISION:
        if "PENDING" in decision.upper():
            _reject_grant("ACTIVE GRANT decision is pending and not authorized")
        _reject_grant(
            f"ACTIVE GRANT decision token {decision!r} is noncanonical"
        )

    for key, expected in required.items():
        actual = fields[key]
        if actual != expected:
            _reject_grant(
                f"ACTIVE GRANT field {key!r} must equal {expected!r}, got {actual!r}"
            )

    approved_at = fields["APPROVED_AT"]
    if APPROVED_AT_PATTERN.fullmatch(approved_at) is None:
        _reject_grant(f"ACTIVE GRANT APPROVED_AT is malformed: {approved_at!r}")

    return dict(fields)


def parse_and_validate_active_grant(
    text: str,
    subject_sha: str,
    execution_code_sha: str,
) -> Dict[str, str]:
    """Extract and validate exactly one canonical ACTIVE GRANT from artifact text."""
    body = extract_active_grant_block(text)
    fields = parse_active_grant_fields(body)
    return validate_active_grant_fields(fields, subject_sha, execution_code_sha)


def verify_execution_authorization(
    authorization_artifact: Path,
    authorization_decision_sha: str,
    subject_sha: str,
    execution_code_sha: str,
) -> None:
    """Require an approved ACTIVE GRANT whose exact blob is merged on origin/main."""
    if re.fullmatch(r"[0-9a-f]{40}", authorization_decision_sha) is None:
        raise BoundedExecutionError(
            GOVERNANCE_REJECTED,
            "authorization decision must be a full lowercase 40-character Git SHA",
        )

    artifact = authorization_artifact.resolve()
    try:
        relative = artifact.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise BoundedExecutionError(
            GOVERNANCE_REJECTED,
            "authorization artifact must be inside the repository",
        ) from exc

    _require_git_success(
        ["ls-files", "--error-unmatch", str(relative)],
        "authorization artifact is not tracked",
    )
    _require_git_success(
        ["diff", "--quiet", "HEAD", "--", str(relative)],
        "authorization artifact differs from HEAD",
    )

    text = artifact.read_text(encoding="utf-8")
    # Only the canonical ACTIVE GRANT block confers authority. Explanatory or
    # pending prose outside the block cannot satisfy execution grant checks.
    parse_and_validate_active_grant(text, subject_sha, execution_code_sha)

    _require_git_success(
        [
            "merge-base",
            "--is-ancestor",
            authorization_decision_sha,
            "origin/main",
        ],
        "authorization decision is not an ancestor of origin/main",
    )
    decision_text = _require_git_blob(
        ["show", f"{authorization_decision_sha}:{relative}"],
        "approved grant is absent from the authorization decision",
    )
    origin_main_text = _require_git_blob(
        ["show", f"origin/main:{relative}"],
        "approved grant is absent from origin/main",
    )
    if decision_text != text or origin_main_text != text:
        raise BoundedExecutionError(
            GOVERNANCE_REJECTED,
            "local approved grant does not exactly match the authorization decision and origin/main",
        )


def _load_projected_records(recorded_at: str) -> Dict[str, Dict[str, Any]]:
    records: Dict[str, Dict[str, Any]] = {}
    for run_id in RUN_ALLOWLIST:
        packet_name = PACKET_BY_RUN_ID[run_id]
        packet_path = REPO_ROOT / "fixtures" / "nw005" / "packets" / packet_name
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        if packet.get("run", {}).get("run_id") != run_id:
            raise BoundedExecutionError(
                GOVERNANCE_REJECTED,
                f"fixture {packet_name!r} is not bound to run_id={run_id!r}",
            )
        context = ProjectionContext(
            recorded_at=recorded_at,
            fixture_id=packet_name,
            source_refs=(f"fixtures/nw005/packets/{packet_name}",),
            writer_component="scripts.nw008.run_at10_bounded_execution",
            writer_component_version="1.0.0",
            writer_mode="firestore_test_project",
        )
        records[run_id] = project_workflow_run_audit(packet, context)
    return records


class At10BoundedExecutor:
    """Runs and proves exactly one bounded four-document lifecycle."""

    def __init__(
        self,
        gateway: BoundedFirestoreGateway,
        proof_dir: Path,
        implementation_subject_sha: str,
        execution_code_sha: str,
        authorization_decision_sha: str,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        if implementation_subject_sha != execution_code_sha:
            raise BoundedExecutionError(
                GOVERNANCE_REJECTED,
                "EXECUTION_CODE_SHA must equal IMPLEMENTATION_SUBJECT_SHA",
            )
        if re.fullmatch(r"[0-9a-f]{40}", authorization_decision_sha) is None:
            raise BoundedExecutionError(
                GOVERNANCE_REJECTED,
                "authorization decision must be a full lowercase 40-character Git SHA",
            )
        self.gateway = gateway
        self.proof_dir = proof_dir
        self.implementation_subject_sha = implementation_subject_sha
        self.execution_code_sha = execution_code_sha
        self.authorization_decision_sha = authorization_decision_sha
        self.now = now

    def run(
        self,
        records: Optional[Mapping[str, Mapping[str, Any]]] = None,
    ) -> Dict[str, Any]:
        started_at = self.now().isoformat()
        projected = (
            {run_id: dict(record) for run_id, record in records.items()}
            if records is not None
            else _load_projected_records(started_at)
        )
        if tuple(projected) != RUN_ALLOWLIST:
            raise BoundedExecutionError(
                GOVERNANCE_REJECTED,
                "executor records must match the ordered four-run allowlist exactly",
            )

        created: list[str] = []
        record_evidence: Dict[str, Dict[str, Any]] = {}
        try:
            for run_id in RUN_ALLOWLIST:
                if self.gateway.get_exact(run_id) is not None:
                    raise BoundedExecutionError(
                        LIFECYCLE_REJECTED,
                        f"precreate check found workflow_runs/{run_id}",
                    )

            for run_id in RUN_ALLOWLIST:
                audit = projected[run_id]
                validate_exact_audit_field_paths(audit, run_id=run_id)
                self.gateway.create_exact(run_id, audit)
                created.append(run_id)

            for run_id in RUN_ALLOWLIST:
                readback = self.gateway.get_exact(run_id)
                if readback is None:
                    raise BoundedExecutionError(
                        LIFECYCLE_REJECTED,
                        f"workflow_runs/{run_id} was not found after create",
                    )
                field_result = validate_exact_audit_field_paths(
                    readback,
                    run_id=run_id,
                )
                fingerprint_result = verify_fingerprint_gate(
                    readback,
                    projected[run_id],
                )
                record_evidence[run_id] = {
                    "path": f"{COLLECTION}/{run_id}",
                    "required_paths_present": field_result["required_paths_present"],
                    **fingerprint_result,
                }

            for run_id in RUN_ALLOWLIST:
                self.gateway.delete_exact(run_id)
                created.remove(run_id)

            for run_id in RUN_ALLOWLIST:
                if self.gateway.get_exact(run_id) is not None:
                    raise BoundedExecutionError(
                        LIFECYCLE_REJECTED,
                        f"postdelete check found workflow_runs/{run_id}",
                    )
        finally:
            for run_id in tuple(created):
                self.gateway.delete_exact(run_id)
                created.remove(run_id)

        self.gateway.counter.ensure_within_deadline()
        counters = self.gateway.counter.snapshot()
        expected = {
            "creates": MAX_CREATES,
            "reads": MAX_READS,
            "deletes": MAX_DELETES,
            "total": MAX_TOTAL_OPERATIONS,
        }
        if counters != expected:
            raise BoundedExecutionError(
                LIFECYCLE_REJECTED,
                f"completed lifecycle counters {counters!r} do not equal {expected!r}",
            )

        result = {
            "STATUS": "PASS",
            "FUNCTIONAL_RESULT": "PASS",
            "CLEANUP_RESULT": "PASS",
            "AT10_EXECUTION_OCCURRED": "YES",
            "AT10_COMPLETION_CLAIM_AUTHORIZED": "NO",
            "AT10_COMPLETE": "NO",
            "PROJECT": PROJECT,
            "DATABASE": DATABASE,
            "LOCATION": LOCATION,
            "COLLECTION": COLLECTION,
            "RUN_IDS": list(RUN_ALLOWLIST),
            "IMPLEMENTATION_SUBJECT_SHA": self.implementation_subject_sha,
            "EXECUTION_CODE_SHA": self.execution_code_sha,
            "AUTHORIZATION_DECISION_SHA": self.authorization_decision_sha,
            "STARTED_AT": started_at,
            "COMPLETED_AT": self.now().isoformat(),
            "COUNTERS": counters,
            "RECORDS": record_evidence,
        }
        self._emit_proof(result)
        return result

    def _emit_proof(self, result: Mapping[str, Any]) -> None:
        """Emit all proof directly from this executor's result and counter."""
        self.proof_dir.mkdir(parents=True, exist_ok=True)
        counters = self.gateway.counter.snapshot()
        if counters != result["COUNTERS"]:
            raise BoundedExecutionError(
                LIFECYCLE_REJECTED,
                "proof counters diverged from executor counters",
            )

        manifest = dict(result)
        records = {
            "AT10_COMPLETE": "NO",
            "COUNTERS": counters,
            "RECORDS": result["RECORDS"],
        }
        cleanup = {
            "AT10_COMPLETE": "NO",
            "cleanup_performed": True,
            "cleanup_verified_not_found": True,
            "documents_deleted": list(RUN_ALLOWLIST),
            "COUNTERS": counters,
        }
        proof_return = {
            "PROOF_CLASS": "BOUNDED_FIRESTORE_RERUN_EXECUTION",
            "EXECUTION_RESULT": "PASS",
            "CLEANUP_RESULT": "PASS",
            "AT10_EXECUTION_OCCURRED": "YES",
            "AT10_COMPLETION_CLAIM_AUTHORIZED": "NO",
            "AT10_COMPLETE": "NO",
            "DOCUMENT_CREATES": counters["creates"],
            "DOCUMENT_READS": counters["reads"],
            "DOCUMENT_DELETES": counters["deletes"],
            "FIRESTORE_NETWORK_OPERATIONS": counters["total"],
            "IMPLEMENTATION_SUBJECT_SHA": self.implementation_subject_sha,
            "EXECUTION_CODE_SHA": self.execution_code_sha,
            "AUTHORIZATION_DECISION_SHA": self.authorization_decision_sha,
        }

        (self.proof_dir / "at-10-run-manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.proof_dir / "at-10-record-evidence.json").write_text(
            json.dumps(records, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.proof_dir / "at-10-cleanup-evidence.json").write_text(
            json.dumps(cleanup, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.proof_dir / "proof-return.yaml").write_text(
            yaml.safe_dump(proof_return, sort_keys=True),
            encoding="utf-8",
        )
        (self.proof_dir / "proof-manifest.md").write_text(
            "\n".join(
                (
                    "# NW-008 AT-10 bounded Firestore rerun proof",
                    "",
                    f"IMPLEMENTATION_SUBJECT_SHA={self.implementation_subject_sha}",
                    f"EXECUTION_CODE_SHA={self.execution_code_sha}",
                    f"AUTHORIZATION_DECISION_SHA={self.authorization_decision_sha}",
                    "AT10_COMPLETION_CLAIM_AUTHORIZED=NO",
                    "AT10_COMPLETE=NO",
                    "",
                )
            ),
            encoding="utf-8",
        )


def _create_firestore_client() -> Any:
    from google.cloud import firestore

    return firestore.Client(project=PROJECT, database=DATABASE)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-subject-sha", required=True)
    parser.add_argument("--execution-code-sha", required=True)
    parser.add_argument("--authorization-decision-sha", required=True)
    parser.add_argument("--authorization-artifact", type=Path, required=True)
    parser.add_argument("--proof-dir", type=Path, default=DEFAULT_PROOF_DIR)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    verify_source_binding(
        args.implementation_subject_sha,
        args.execution_code_sha,
    )
    verify_execution_authorization(
        args.authorization_artifact,
        args.authorization_decision_sha,
        args.implementation_subject_sha,
        args.execution_code_sha,
    )
    counter = OperationCounter()
    gateway = BoundedFirestoreGateway(_create_firestore_client(), counter)
    executor = At10BoundedExecutor(
        gateway=gateway,
        proof_dir=args.proof_dir,
        implementation_subject_sha=args.implementation_subject_sha,
        execution_code_sha=args.execution_code_sha,
        authorization_decision_sha=args.authorization_decision_sha,
    )
    result = executor.run()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BoundedExecutionError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
