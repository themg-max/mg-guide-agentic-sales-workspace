"""Deterministic decision-card view model for NW-007."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class DecisionCard:
    workflow_status: str
    agent_contributions: List[str]
    policy_state: str
    policy_reason_code: str
    policy_explanation: str
    human_review_required: bool
    external_effects: Any
    next_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
