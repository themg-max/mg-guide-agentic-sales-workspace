"""Deterministic state machine for meeting_follow_up_v1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .models import TERMINAL_STATES


class TransitionError(ValueError):
    """Illegal workflow transition."""


@dataclass(frozen=True)
class Transition:
    source: str
    target: str
    when: str
    reason_code: Optional[str] = None


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

        self.max_note_intents = 1
        self.max_stage_intents = 1

    @classmethod
    def from_yaml(cls, path: Path) -> "StateMachine":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(data)

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
