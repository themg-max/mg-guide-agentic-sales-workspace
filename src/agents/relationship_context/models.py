"""Models for Relationship Context Agent structured output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class RelationshipRequest:
    """Input to the Relationship Context Agent."""

    meeting_context: Mapping[str, Any]
    run_id: Optional[str] = None
    scenario_id: Optional[str] = None
    prior_context: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class RelationshipContextResult:
    """Structured relationship context suitable for packet crm_resolution overlay."""

    schema: str
    agent: str
    provider: str
    meeting_ref: Dict[str, Any]
    resolution: Dict[str, Any]
    crm_source: Dict[str, Any]
    evidence: Dict[str, Any]
    external_effects: int
    policy_authority: Dict[str, Any]
    longitudinal_context: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "schema": self.schema,
            "agent": self.agent,
            "provider": self.provider,
            "meeting_ref": dict(self.meeting_ref),
            "resolution": dict(self.resolution),
            "crm_source": dict(self.crm_source),
            "evidence": dict(self.evidence),
            "external_effects": self.external_effects,
            "policy_authority": dict(self.policy_authority),
        }
        if self.longitudinal_context is not None:
            payload["longitudinal_context"] = dict(self.longitudinal_context)
        return payload

    def to_crm_resolution_overlay(self) -> Dict[str, Any]:
        """Map into meeting_follow_up_packet_v1 crm_resolution shape."""
        res = self.resolution
        status = res["status"]
        # Packet enum uses opportunity_missing; insufficient_context maps to
        # not_found and opportunity_ambiguous maps to ambiguous.
        packet_status = status
        if status == "insufficient_context":
            packet_status = "not_found"
        elif status == "opportunity_ambiguous":
            packet_status = "ambiguous"
        return {
            "lifecycle": res["lifecycle"] if res["lifecycle"] == "complete" else "failed",
            "status": packet_status,
            "contact_id": res.get("contact_id"),
            "opportunity_id": res.get("opportunity_id"),
            "match_basis": res.get("match_basis") or "none",
            "candidate_count": int(res.get("candidate_count") or 0),
            "current_stage": res.get("current_stage"),
        }


def empty_resolution(*, status: str = "not_found", match_basis: str = "none") -> Dict[str, Any]:
    return {
        "lifecycle": "complete",
        "status": status,
        "contact_id": None,
        "opportunity_id": None,
        "match_basis": match_basis,
        "candidate_count": 0,
        "current_stage": None,
        "candidates": [],
        "contact": None,
        "opportunity": None,
    }
