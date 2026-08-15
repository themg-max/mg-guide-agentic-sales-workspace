"""Offline-only AT-10 acceptance-demo validation and proof generation.

This module models the authorized implementation-only lane: no network calls,
no Firestore reads or writes, and no external effects. It validates the exact
four-run synthetic allowlist and the exact AT-10 field paths described in the
NW-008 AT-10 acceptance-demo packet.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from .canonicalize import fingerprint_hex
from .models import default_stage_a_context
from .project import _content_fingerprint_body, project_workflow_run_audit
from .validate import validate_workflow_run_audit

AT10_ACCEPTANCE_SET = (
    "run_nw006_success_001",
    "run_nw006_stage_denied_001",
    "run_nw006_ambiguous_contact_001",
    "run_nw006_failed_001",
)
AT10_ACCEPTANCE_SET_SIZE = len(AT10_ACCEPTANCE_SET)
AT10_FIELD_PATHS = {
    "agents": "agent_steps.agents_used",
    "tool_counts": "tool_call_counts",
    "reason_codes": "reason_codes",
    "final_disposition": "final_disposition",
}
AT10_REQUIRED_FIELD_PATHS = tuple(AT10_FIELD_PATHS.values())
AT10_DISPOSITION_BY_RUN_ID = {
    "run_nw006_success_001": "completed",
    "run_nw006_stage_denied_001": "completed_with_review",
    "run_nw006_ambiguous_contact_001": "blocked",
    "run_nw006_failed_001": "failed",
}
AT10_ACCEPTANCE_SET_COMPLETE = True

MAX_LOCAL_CREATES = 4
MAX_LOCAL_READS = 12
MAX_LOCAL_DELETES = 4

LOCAL_CAP_EXCEEDED = "LOCAL_CAP_EXCEEDED"
FINGERPRINT_MISMATCH = "FINGERPRINT_MISMATCH"
FIRESTORE_CREATE_CONFLICT = "FIRESTORE_CREATE_CONFLICT"

PROOF_NAMESPACE = Path("proof/nw008/at-10/acceptance-demo")


class AcceptanceDemoValidationError(ValueError):
    """Fail-closed validation error for the AT-10 acceptance-demo lane."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


_MISSING = object()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _nested_get(mapping: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = mapping
    for part in dotted_path.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
            continue
        return _MISSING
    return current


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_exact_audit_field_paths(
    audit: Mapping[str, Any], *, run_id: Optional[str] = None
) -> Dict[str, Any]:
    """Require the exact durable paths bound by the AT-10 acceptance packet."""
    if not isinstance(audit, Mapping):
        raise AcceptanceDemoValidationError("audit must be a mapping")

    try:
        validate_workflow_run_audit(audit)
    except Exception as exc:  # pragma: no cover - converted to fail-closed gateway error
        raise AcceptanceDemoValidationError(f"schema validation failed: {exc}") from exc

    resolved_run_id = run_id or audit.get("run_id")
    if not isinstance(resolved_run_id, str):
        raise AcceptanceDemoValidationError("audit.run_id must be a string")

    if resolved_run_id not in AT10_ACCEPTANCE_SET:
        raise AcceptanceDemoValidationError(
            f"run_id={resolved_run_id!r} is outside the AT-10 acceptance allowlist"
        )

    expected_disposition = AT10_DISPOSITION_BY_RUN_ID.get(resolved_run_id)
    if expected_disposition is not None:
        actual_disposition = audit.get("final_disposition")
        if actual_disposition != expected_disposition:
            raise AcceptanceDemoValidationError(
                f"run_id={resolved_run_id!r} expected final_disposition={expected_disposition!r}, "
                f"got {actual_disposition!r}"
            )

    presence: Dict[str, Any] = {}
    for key, path in AT10_FIELD_PATHS.items():
        value = _nested_get(audit, path)
        if value is _MISSING:
            raise AcceptanceDemoValidationError(f"required path {path!r} missing on run_id={resolved_run_id!r}")
        if key == "agents" and not isinstance(value, list):
            raise AcceptanceDemoValidationError(f"{path!r} must be an array of strings")
        if key == "tool_counts" and not isinstance(value, dict):
            raise AcceptanceDemoValidationError(f"{path!r} must be an object")
        if key == "reason_codes" and not isinstance(value, list):
            raise AcceptanceDemoValidationError(f"{path!r} must be an array of strings")
        if key == "final_disposition" and not isinstance(value, str):
            raise AcceptanceDemoValidationError(f"{path!r} must be a string")
        presence[key] = value

    return {
        "run_id": resolved_run_id,
        "required_paths_present": True,
        "field_paths": dict(AT10_FIELD_PATHS),
        "presence": presence,
    }


def validate_acceptance_demo_set(
    records: Iterable[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Validate the complete four-run AT-10 acceptance set."""
    if isinstance(records, Mapping):
        valid_records = list(records.values())
    else:
        valid_records = list(records)
    if len(valid_records) != AT10_ACCEPTANCE_SET_SIZE:
        raise AcceptanceDemoValidationError(
            f"expected {AT10_ACCEPTANCE_SET_SIZE} records, got {len(valid_records)}"
        )

    run_ids = []
    dispositions = set()
    for record in valid_records:
        audit = dict(record)
        run_id = str(audit.get("run_id"))
        validate_exact_audit_field_paths(audit, run_id=run_id)
        run_ids.append(run_id)
        dispositions.add(audit.get("final_disposition"))

    if set(run_ids) != set(AT10_ACCEPTANCE_SET):
        raise AcceptanceDemoValidationError(
            f"run_ids mismatch: expected {sorted(AT10_ACCEPTANCE_SET)}, got {sorted(run_ids)}"
        )

    required_dispositions = {"completed", "completed_with_review", "blocked", "failed"}
    if not required_dispositions.issubset(dispositions):
        raise AcceptanceDemoValidationError(
            "AT-10 acceptance set must cover completed, completed_with_review, blocked, and failed"
        )

    return {
        "status": "PASS",
        "allowlist_count": AT10_ACCEPTANCE_SET_SIZE,
        "allowed_run_ids": list(AT10_ACCEPTANCE_SET),
        "present_run_ids": sorted(run_ids),
        "dispositions": sorted(dispositions),
        "acceptance_set_complete": True,
        "exact_field_paths_verified": True,
    }


def verify_fingerprint_gate(
    readback: Mapping[str, Any],
    projected: Mapping[str, Any],
) -> Dict[str, Any]:
    """Fail-closed triple-equality fingerprint gate.

    Requires:
      RECOMPUTED_READBACK_CONTENT_FINGERPRINT
      == STORED_CONTENT_FINGERPRINT
      == EXPECTED_PROJECTED_CONTENT_FINGERPRINT
    """
    if not isinstance(readback, Mapping):
        raise AcceptanceDemoValidationError("readback must be a mapping")
    if not isinstance(projected, Mapping):
        raise AcceptanceDemoValidationError("projected must be a mapping")

    stored = readback.get("integrity", {}).get("content_fingerprint")
    if not isinstance(stored, str) or not stored:
        raise AcceptanceDemoValidationError("readback integrity.content_fingerprint missing")

    recomputed = fingerprint_hex(_content_fingerprint_body(readback))
    expected = fingerprint_hex(_content_fingerprint_body(projected))

    if recomputed != stored:
        raise AcceptanceDemoValidationError(
            f"{FINGERPRINT_MISMATCH}: recomputed readback content fingerprint {recomputed!r} "
            f"does not match stored fingerprint {stored!r}"
        )
    if stored != expected:
        raise AcceptanceDemoValidationError(
            f"{FINGERPRINT_MISMATCH}: stored content fingerprint {stored!r} "
            f"does not match expected projected fingerprint {expected!r}"
        )

    return {
        "recomputed_content_fingerprint": recomputed,
        "stored_content_fingerprint": stored,
        "expected_projected_content_fingerprint": expected,
        "fingerprint_gate": "PASS",
    }


@dataclass
class OfflineAcceptanceDemoStore:
    """In-memory local-only model of the acceptance-demo Firestore lane.

    The store deliberately tracks local-only lifecycle counts, never increments a
    network or Firestore-side counter, and rejects any run_id outside the exact
    four-run allowance. Local CAPS fail closed before any operation that would
    exceed the authorized offline lifecycle counters.
    """

    _docs: MutableMapping[str, Dict[str, Any]] = field(default_factory=dict)
    network_calls: int = 0
    firestore_network_operations: int = 0
    firestore_reads: int = 0
    firestore_writes: int = 0
    firestore_deletes: int = 0
    local_creates: int = 0
    local_reads: int = 0
    local_deletes: int = 0
    max_local_creates: int = MAX_LOCAL_CREATES
    max_local_reads: int = MAX_LOCAL_READS
    max_local_deletes: int = MAX_LOCAL_DELETES

    def _check_read_cap(self) -> None:
        if self.local_reads >= self.max_local_reads:
            raise AcceptanceDemoValidationError(
                f"{LOCAL_CAP_EXCEEDED}: local read cap {self.max_local_reads} would be exceeded"
            )

    def _check_create_cap(self) -> None:
        if self.local_creates >= self.max_local_creates:
            raise AcceptanceDemoValidationError(
                f"{LOCAL_CAP_EXCEEDED}: local create cap {self.max_local_creates} would be exceeded"
            )

    def _check_delete_cap(self) -> None:
        if self.local_deletes >= self.max_local_deletes:
            raise AcceptanceDemoValidationError(
                f"{LOCAL_CAP_EXCEEDED}: local delete cap {self.max_local_deletes} would be exceeded"
            )

    def get(self, run_id: str) -> Optional[Dict[str, Any]]:
        self._check_read_cap()
        self.local_reads += 1
        doc = self._docs.get(run_id)
        if doc is None:
            return None
        return copy.deepcopy(doc)

    def require_not_found(self, run_id: str) -> None:
        """Exact get that fails closed if the document exists."""
        found = self.get(run_id)
        if found is not None:
            raise AcceptanceDemoValidationError(
                f"document workflow_runs/{run_id} exists but was required to be absent"
            )

    def create_exact(self, run_id: str, audit: Mapping[str, Any]) -> Dict[str, Any]:
        if run_id not in AT10_ACCEPTANCE_SET:
            raise AcceptanceDemoValidationError(
                f"run_id={run_id!r} is outside the AT-10 acceptance allowlist"
            )
        if run_id in self._docs:
            raise AcceptanceDemoValidationError(
                f"{FIRESTORE_CREATE_CONFLICT}: document workflow_runs/{run_id} already exists"
            )
        self._check_create_cap()

        projected = dict(audit)
        validate_exact_audit_field_paths(projected, run_id=run_id)
        self._docs[run_id] = copy.deepcopy(projected)
        self.local_creates += 1
        return {"run_id": run_id, "status": "created", "network_calls": 0}

    def delete_exact(self, run_id: str) -> Dict[str, Any]:
        if run_id not in self._docs:
            raise AcceptanceDemoValidationError(
                f"document workflow_runs/{run_id} does not exist"
            )
        self._check_delete_cap()
        del self._docs[run_id]
        self.local_deletes += 1
        return {"run_id": run_id, "status": "deleted", "network_calls": 0}

    def __len__(self) -> int:
        return len(self._docs)


def _acceptance_demo_packet_map() -> Dict[str, str]:
    return {
        "run_nw006_success_001": "packet-success.completed.json",
        "run_nw006_stage_denied_001": "packet-stage-change-denied.completed_with_review.json",
        "run_nw006_ambiguous_contact_001": "packet-ambiguous-contact.blocked.json",
        "run_nw006_failed_001": "packet-tool-failure.failed.json",
    }


def _project_packet_from_fixture(packet_name: str) -> Dict[str, Any]:
    packet_path = _repo_root() / "fixtures" / "nw005" / "packets" / packet_name
    packet = _load_json(packet_path)
    context = default_stage_a_context(
        fixture_id=packet_name,
        source_refs=[f"fixtures/nw005/packets/{packet_name}"],
        recorded_at="2026-08-12T20:00:00Z",
        writer_component_version="0.1.0-stage-a",
    )
    return project_workflow_run_audit(packet, context)


def emit_acceptance_demo_proof(summary: Mapping[str, Any]) -> Dict[str, Any]:
    """Emit local proof artifacts under the frozen future-proof namespace.

    Proof emission occurs only after cleanup has been performed and verified,
    so cleanup success is never asserted before the documents are actually
    removed.
    """
    proof_dir = _repo_root() / PROOF_NAMESPACE
    proof_dir.mkdir(parents=True, exist_ok=True)

    cleanup_performed = bool(summary.get("cleanup_performed", False))
    cleanup_verified = bool(summary.get("cleanup_verified_not_found", False))

    proof_manifest = {
        "AUTHORIZATION_ID": "MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1",
        "AUTHORIZATION_DECISION": "AUTHORIZED_FOR_IMPLEMENTATION_ONLY",
        "AT10_ACCEPTANCE_SET": list(AT10_ACCEPTANCE_SET),
        "AT10_ACCEPTANCE_SET_SIZE": AT10_ACCEPTANCE_SET_SIZE,
        "EXTERNAL_EFFECTS": 0,
        "NETWORK_CALLS": 0,
        "FIRESTORE_NETWORK_OPERATIONS": 0,
        "RECORDS": summary.get("present_run_ids", []),
        "STATUS": summary.get("status", "PASS"),
    }
    (proof_dir / "at-10-run-manifest.json").write_text(
        json.dumps(proof_manifest, indent=2, sort_keys=True), encoding="utf-8"
    )

    evidence = {
        "run_ids": list(AT10_ACCEPTANCE_SET),
        "acceptance_set_complete": bool(summary.get("acceptance_set_complete", False)),
        "field_paths": dict(AT10_FIELD_PATHS),
        "dispositions": summary.get("dispositions", []),
    }
    (proof_dir / "at-10-record-evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
    )

    cleanup_evidence = {
        "cleanup_required": True,
        "cleanup_performed": cleanup_performed,
        "cleanup_verified_not_found": cleanup_verified,
        "documents_deleted": summary.get("present_run_ids", []) if cleanup_performed else [],
        "network_calls": 0,
    }
    (proof_dir / "at-10-cleanup-evidence.json").write_text(
        json.dumps(cleanup_evidence, indent=2, sort_keys=True), encoding="utf-8"
    )

    readme = """# NW-008 AT-10 offline acceptance-demo proof

This directory is the frozen future-proof namespace for the offline acceptance-demo lane.
It is intentionally local-only and does not invoke any external service.
"""
    (proof_dir / "proof-manifest.md").write_text(readme, encoding="utf-8")

    proof_return = {
        "PROOF_CLASS": "OFFLINE_IMPLEMENTATION_VALIDATION",
        "OFFLINE_VALIDATION_RESULT": "PASS",
        "AT10_EXECUTION_OCCURRED": "NO",
        "FIRESTORE_ACCEPTANCE_DEMO_EXECUTED": "NO",
        "AT10_COMPLETE": "NO",
        "AT10_EXECUTION_AUTHORIZED": "NO",
        "AT10_COMPLETION_CLAIM_AUTHORIZED": "NO",
        "NETWORK_CALLS": 0,
        "FIRESTORE_NETWORK_OPERATIONS": 0,
        "FIRESTORE_READS": 0,
        "FIRESTORE_WRITES": 0,
        "FIRESTORE_DELETES": 0,
        "EXTERNAL_EFFECTS": 0,
        "LOCAL_DOCUMENT_CREATES": summary.get("local_creates", 0),
        "LOCAL_DOCUMENT_READS": summary.get("local_reads", 0),
        "LOCAL_DOCUMENT_DELETES": summary.get("local_deletes", 0),
        "PROOF_NAMESPACE": str(PROOF_NAMESPACE),
        "CLEANUP_PERFORMED": cleanup_performed,
        "CLEANUP_VERIFIED_NOT_FOUND": cleanup_verified,
    }
    (proof_dir / "proof-return.yaml").write_text(
        _dict_to_yaml(proof_return), encoding="utf-8"
    )

    return {
        "proof_dir": str(proof_dir),
        "files": [
            "at-10-run-manifest.json",
            "at-10-record-evidence.json",
            "at-10-cleanup-evidence.json",
            "proof-manifest.md",
            "proof-return.yaml",
        ],
    }


def _dict_to_yaml(data: Mapping[str, Any]) -> str:
    """Minimal deterministic YAML serializer for proof-return artifacts.

    Only handles the flat scalar values used by the offline proof; it does not
    claim full YAML conformance.
    """
    lines: List[str] = []
    for key, value in sorted(data.items()):
        if isinstance(value, str):
            # Quote strings so that "NO" remains the literal string "NO".
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        elif isinstance(value, (list, tuple)):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def simulate_acceptance_demo() -> Dict[str, Any]:
    """Execute the offline four-run acceptance lifecycle without network access.

    Mirror the future exact lifecycle locally:
      1. pre-create exact get x4 -> require None
      2. create x4
      3. readback exact get x4
      4. schema/path/fingerprint validation x4
      5. aggregate validation
      6. delete exact x4
      7. post-delete exact get x4 -> require None
      8. emit final cleanup proof

    Required final counters:
      LOCAL_DOCUMENT_CREATES=4
      LOCAL_DOCUMENT_READS=12
      LOCAL_DOCUMENT_DELETES=4
    """
    store = OfflineAcceptanceDemoStore()
    packet_map = _acceptance_demo_packet_map()
    synthesized: List[Dict[str, Any]] = []

    # 1. Pre-create exact get x4 -> require NOT_FOUND.
    for run_id in AT10_ACCEPTANCE_SET:
        store.require_not_found(run_id)

    # 2. Create x4, 3. readback exact get x4, 4. validation x4.
    for run_id, packet_name in packet_map.items():
        projected = _project_packet_from_fixture(packet_name)
        validate_exact_audit_field_paths(projected, run_id=run_id)
        store.create_exact(run_id, projected)
        readback = store.get(run_id)
        if readback is None:
            raise AcceptanceDemoValidationError(f"readback missing for run_id={run_id!r}")
        validate_exact_audit_field_paths(readback, run_id=run_id)
        verify_fingerprint_gate(readback, projected)
        synthesized.append(readback)

    # 5. Aggregate validation.
    summary = validate_acceptance_demo_set(synthesized)

    # 6. Delete exact x4.
    for run_id in AT10_ACCEPTANCE_SET:
        store.delete_exact(run_id)

    # 7. Post-delete exact get x4 -> require NOT_FOUND.
    for run_id in AT10_ACCEPTANCE_SET:
        store.require_not_found(run_id)

    if len(store) != 0:
        raise AcceptanceDemoValidationError("cleanup failed; synthetic acceptance records remain")

    summary["network_calls"] = store.network_calls
    summary["firestore_network_operations"] = store.firestore_network_operations
    summary["firestore_reads"] = store.firestore_reads
    summary["firestore_writes"] = store.firestore_writes
    summary["firestore_deletes"] = store.firestore_deletes
    summary["local_creates"] = store.local_creates
    summary["local_reads"] = store.local_reads
    summary["local_deletes"] = store.local_deletes
    summary["cleanup_performed"] = True
    summary["cleanup_verified_not_found"] = True
    summary["external_effects"] = 0

    # 8. Emit final cleanup proof only after cleanup is verified.
    summary["proof_artifacts"] = emit_acceptance_demo_proof(summary)
    return summary
