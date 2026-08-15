"""Deterministic state machine for meeting_follow_up_v1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .models import TERMINAL_STATES


class TransitionError(ValueError):
    """Illegal workflow transition."""


class WriteCapContractError(ValueError):
    """Raised when write-attempt caps cannot be loaded fail-closed from contract."""

    def __init__(self, detail: str) -> None:
        super().__init__(f"INVALID_WRITE_CAP_CONTRACT: {detail}")


@dataclass(frozen=True)
class Transition:
    source: str
    target: str
    when: str
    reason_code: Optional[str] = None


def _invariant_map(contract: Dict[str, Any]) -> Dict[str, Any]:
    raw = contract.get("invariants")
    if raw is None:
        return {}
    if not isinstance(raw, list):
        raise WriteCapContractError("invariants must be a list")
    merged: Dict[str, Any] = {}
    for item in raw:
        if not isinstance(item, dict):
            raise WriteCapContractError("each invariant entry must be a mapping")
        merged.update(item)
    return merged


def require_positive_int_cap(invariants: Dict[str, Any], field: str) -> int:
    """Normalize and validate a write/intent cap. Fail closed on any invalid value."""

    if field not in invariants:
        raise WriteCapContractError(f"missing {field}")
    value = invariants[field]
    # bool is a subclass of int; reject explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise WriteCapContractError(
            f"{field} must be a positive integer >= 1; got {value!r}"
        )
    return value


class StateMachine:
    def __init__(self, contract: Dict[str, Any]):
        self.workflow = contract["workflow"]
        self.states: Dict[str, Dict[str, Any]] = {
            s["id"]: s for s in contract["states"]
        }
        self.transitions: List[Transition] = [
            Transition(
                source=t["from"],
                target=t["to"],
                when=t["when"],
                reason_code=t.get("reason_code"),
            )
            for t in contract["transitions"]
        ]
        self._by_edge: Dict[Tuple[str, str], List[Transition]] = {}
        for tr in self.transitions:
            self._by_edge.setdefault((tr.source, tr.target), []).append(tr)

        thresholds = contract["policy_thresholds"]
        self.extraction_abort_threshold = float(
            thresholds["extraction_abort_threshold"]
        )
        self.stage_transition_confidence_min = float(
            thresholds["stage_transition_confidence_min"]
        )
        if self.extraction_abort_threshold >= self.stage_transition_confidence_min:
            # Allowed numerically but must remain distinct values for Phase 1 clarity.
            if self.extraction_abort_threshold == self.stage_transition_confidence_min:
                raise ValueError(
                    "extraction_abort_threshold and stage_transition_confidence_min must be distinct"
                )

        invariants = _invariant_map(contract)
        # CONTRACT_LOADING_REPAIR: write caps are authoritative from workflow_states.yaml.
        self.max_note_writes_per_run = require_positive_int_cap(
            invariants, "max_note_writes_per_run"
        )
        self.max_stage_writes_per_run = require_positive_int_cap(
            invariants, "max_stage_writes_per_run"
        )
        self.max_note_intents = require_positive_int_cap(
            invariants, "max_note_intents_per_run"
        )
        self.max_stage_intents = require_positive_int_cap(
            invariants, "max_stage_intents_per_run"
        )
        self.cap_source = "contracts/workflow_states.yaml"
        self.cap_node = "invariants"

    @classmethod
    def from_yaml(cls, path: Path) -> "StateMachine":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(data)

    def write_cap_for(self, write_kind: str) -> int:
        kind = str(write_kind or "").strip().lower()
        if kind == "note":
            return self.max_note_writes_per_run
        if kind == "stage":
            return self.max_stage_writes_per_run
        raise WriteCapContractError(
            f"unsupported write kind for cap lookup: {write_kind!r}"
        )

    def is_terminal(self, state: str) -> bool:
        meta = self.states.get(state)
        if meta is None:
            raise TransitionError(f"unknown state: {state}")
        return bool(meta.get("terminal"))

    def legal_targets(self, source: str) -> Set[str]:
        return {tr.target for tr in self.transitions if tr.source == source}

    def validate_transition(
        self, source: str, target: str, when: Optional[str] = None
    ) -> Transition:
        if source not in self.states:
            raise TransitionError(f"unknown source state: {source}")
        if target not in self.states:
            raise TransitionError(f"unknown target state: {target}")
        if self.is_terminal(source):
            raise TransitionError(
                f"terminal state is immutable: cannot transition from {source}"
            )
        candidates = self._by_edge.get((source, target), [])
        if not candidates:
            raise TransitionError(f"illegal transition: {source} -> {target}")
        if when is None:
            return candidates[0]
        for tr in candidates:
            if tr.when == when:
                return tr
        raise TransitionError(
            f"illegal transition: {source} -> {target} when={when}"
        )

    def all_legal_edges(self) -> List[Tuple[str, str, str]]:
        return [(tr.source, tr.target, tr.when) for tr in self.transitions]
