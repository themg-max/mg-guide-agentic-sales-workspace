"""Terminal-only in-memory audit store (Stage A; zero external effects)."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

from .models import TERMINAL_STATES
from .validate import validate_workflow_run_audit

AUDIT_IDEMPOTENCY_CONFLICT = "AUDIT_IDEMPOTENCY_CONFLICT"
AUDIT_TERMINAL_STATE_CONFLICT = "AUDIT_TERMINAL_STATE_CONFLICT"
AUDIT_NON_TERMINAL_DURABLE_WRITE = "AUDIT_NON_TERMINAL_DURABLE_WRITE"


class AuditStoreError(ValueError):
    """Fail-closed store error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True)
class PersistResult:
    """Result of a store.persist attempt (static audit + dynamic observation)."""

    status: str  # created | idempotent_noop | rejected
    run_id: str
    terminal_state: Optional[str]
    projection_input_fingerprint: Optional[str]
    content_fingerprint: Optional[str]
    duplicate_write_rejected: bool
    prior_terminal_state: Optional[str]
    durable_write: bool
    code: Optional[str] = None
    message: Optional[str] = None


@dataclass
class MemoryAuditStore:
    """In-process create-once store mirroring NW-005 Decision 5 truth table.

    - Terminal audits may persist.
    - Non-terminal projections MUST NOT persist.
    - Same run_id + same projection_input_fingerprint + same terminal_state
      → idempotent no-op.
    - Same run_id + different projection_input_fingerprint
      → AUDIT_IDEMPOTENCY_CONFLICT.
    - Same run_id + different terminal_state
      → AUDIT_TERMINAL_STATE_CONFLICT.
    """

    _docs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    creates: int = 0
    noop_hits: int = 0
    rejects: int = 0

    def get(self, run_id: str) -> Optional[Dict[str, Any]]:
        doc = self._docs.get(run_id)
        return copy.deepcopy(doc) if doc is not None else None

    def __contains__(self, run_id: str) -> bool:
        return run_id in self._docs

    def __len__(self) -> int:
        return len(self._docs)

    def persist(self, audit: Mapping[str, Any], *, raise_on_conflict: bool = True) -> PersistResult:
        """Persist a validated terminal audit under Decision 5 rules."""
        validated = validate_workflow_run_audit(audit)
        run_id = validated["run_id"]
        terminal_state = validated["terminal_state"]
        integrity = validated["integrity"]
        pip = integrity["projection_input_fingerprint"]
        cfp = integrity["content_fingerprint"]

        if terminal_state not in TERMINAL_STATES:
            self.rejects += 1
            result = PersistResult(
                status="rejected",
                run_id=run_id,
                terminal_state=terminal_state,
                projection_input_fingerprint=pip,
                content_fingerprint=cfp,
                duplicate_write_rejected=False,
                prior_terminal_state=None,
                durable_write=False,
                code=AUDIT_NON_TERMINAL_DURABLE_WRITE,
                message="NW-005 v1 persists terminal states only; non-terminal must not be durable",
            )
            if raise_on_conflict:
                raise AuditStoreError(result.code or AUDIT_NON_TERMINAL_DURABLE_WRITE, result.message or "")
            return result

        existing = self._docs.get(run_id)
        if existing is None:
            self._docs[run_id] = copy.deepcopy(validated)
            self.creates += 1
            return PersistResult(
                status="created",
                run_id=run_id,
                terminal_state=terminal_state,
                projection_input_fingerprint=pip,
                content_fingerprint=cfp,
                duplicate_write_rejected=False,
                prior_terminal_state=None,
                durable_write=True,
            )

        prior_state = existing["terminal_state"]
        prior_pip = existing["integrity"]["projection_input_fingerprint"]

        if prior_state == terminal_state and prior_pip == pip:
            self.noop_hits += 1
            return PersistResult(
                status="idempotent_noop",
                run_id=run_id,
                terminal_state=terminal_state,
                projection_input_fingerprint=pip,
                content_fingerprint=cfp,
                duplicate_write_rejected=False,
                prior_terminal_state=prior_state,
                durable_write=False,
            )

        if prior_state != terminal_state:
            self.rejects += 1
            result = PersistResult(
                status="rejected",
                run_id=run_id,
                terminal_state=terminal_state,
                projection_input_fingerprint=pip,
                content_fingerprint=cfp,
                duplicate_write_rejected=True,
                prior_terminal_state=prior_state,
                durable_write=False,
                code=AUDIT_TERMINAL_STATE_CONFLICT,
                message=(
                    f"existing terminal_state={prior_state!r} conflicts with "
                    f"new terminal_state={terminal_state!r}"
                ),
            )
            if raise_on_conflict:
                raise AuditStoreError(AUDIT_TERMINAL_STATE_CONFLICT, result.message or "")
            return result

        # Same terminal_state, different projection_input_fingerprint
        self.rejects += 1
        result = PersistResult(
            status="rejected",
            run_id=run_id,
            terminal_state=terminal_state,
            projection_input_fingerprint=pip,
            content_fingerprint=cfp,
            duplicate_write_rejected=True,
            prior_terminal_state=prior_state,
            durable_write=False,
            code=AUDIT_IDEMPOTENCY_CONFLICT,
            message=(
                "existing projection_input_fingerprint differs from new projection "
                f"for run_id={run_id!r} terminal_state={terminal_state!r}"
            ),
        )
        if raise_on_conflict:
            raise AuditStoreError(AUDIT_IDEMPOTENCY_CONFLICT, result.message or "")
        return result
