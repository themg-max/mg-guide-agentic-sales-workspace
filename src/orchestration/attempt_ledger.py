"""Run-scoped write-attempt ledger for meeting_follow_up_v1.

The ledger owns accounting state only. It never decides PERMIT/REFUSE.
OL3 orchestration policy is the sole enforcement decision owner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


WRITE_KINDS = frozenset({"note", "stage"})
LEDGER_STATE_OWNER = "WRITE_ATTEMPT_LEDGER"


class UnknownWriteKindError(ValueError):
    """Raised when a write kind is outside the supported note/stage set."""


@dataclass
class WriteAttemptLedger:
    """Non-persistent, run-local counters for admitted write attempts."""

    run_id: str
    _counts: Dict[str, int] = field(default_factory=lambda: {"note": 0, "stage": 0})

    def __post_init__(self) -> None:
        if not self.run_id or not str(self.run_id).strip():
            raise ValueError("run_id is required")
        # Ensure both independent counters exist even if constructed oddly.
        for kind in WRITE_KINDS:
            self._counts.setdefault(kind, 0)

    @property
    def state_owner(self) -> str:
        return LEDGER_STATE_OWNER

    def before(self, write_kind: str) -> int:
        return self._count(write_kind)

    def count(self, write_kind: str) -> int:
        return self._count(write_kind)

    def record_admission(self, write_kind: str) -> int:
        """Increment the admitted-attempt counter for *write_kind*.

        Called only by OL3 policy after it has already decided PERMIT.
        Refused attempts must never call this method.
        """
        kind = self._normalize_kind(write_kind)
        self._counts[kind] = self._counts[kind] + 1
        return self._counts[kind]

    def snapshot(self) -> Dict[str, int]:
        return {kind: int(self._counts[kind]) for kind in sorted(WRITE_KINDS)}

    def _count(self, write_kind: str) -> int:
        kind = self._normalize_kind(write_kind)
        return int(self._counts[kind])

    @staticmethod
    def _normalize_kind(write_kind: str) -> str:
        kind = str(write_kind or "").strip().lower()
        if kind not in WRITE_KINDS:
            raise UnknownWriteKindError(f"unsupported write kind: {write_kind!r}")
        return kind


@dataclass
class WriteAttemptLedgerRegistry:
    """Process-local registry mapping run_id -> independent ledger instance."""

    _ledgers: Dict[str, WriteAttemptLedger] = field(default_factory=dict)

    def for_run(self, run_id: str) -> WriteAttemptLedger:
        key = str(run_id)
        ledger = self._ledgers.get(key)
        if ledger is None:
            ledger = WriteAttemptLedger(run_id=key)
            self._ledgers[key] = ledger
        return ledger

    def known_run_ids(self) -> Iterable[str]:
        return tuple(self._ledgers.keys())
