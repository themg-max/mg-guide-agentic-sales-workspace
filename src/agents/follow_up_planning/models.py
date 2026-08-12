"""Models for Follow-Up Planning Agent structured output (Phase 3 Unit 3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class FollowUpPlanningRequest:
    """Input to the Follow-Up Planning Agent.

    Consumes already-produced Unit 1 / Unit 2 artifacts only.
    """

    meeting_context: Mapping[str, Any]
    relationship_context: Mapping[str, Any]
    run_id: Optional[str] = None
    scenario_id: Optional[str] = None


@dataclass(frozen=True)
class FollowUpPlanningResult:
    """Structured follow-up proposal plus the reviewable packet."""

    proposal: Dict[str, Any]
    packet: Dict[str, Any]
    policy_gate_invoked: bool
    external_effects: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal": dict(self.proposal),
            "packet": dict(self.packet),
            "policy_gate_invoked": self.policy_gate_invoked,
            "external_effects": self.external_effects,
        }
