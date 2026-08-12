"""Models for Meeting Context Agent structured output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class MeetingContextResult:
    """Structured meeting context suitable for packet construction."""

    schema: str
    agent: str
    provider: str
    meeting: Dict[str, Any]
    participants: List[Dict[str, Any]]
    extraction: Dict[str, Any]
    evidence: Dict[str, Any]
    external_effects: int
    policy_authority: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "agent": self.agent,
            "provider": self.provider,
            "meeting": dict(self.meeting),
            "participants": [dict(p) for p in self.participants],
            "extraction": dict(self.extraction),
            "evidence": dict(self.evidence),
            "external_effects": self.external_effects,
            "policy_authority": dict(self.policy_authority),
        }

    @staticmethod
    def from_parts(
        *,
        provider: str,
        meeting: Mapping[str, Any],
        participants: List[Mapping[str, Any]],
        extraction_result: Optional[Mapping[str, Any]],
        extraction_confidence: float,
        evidence_references: List[Mapping[str, str]],
    ) -> "MeetingContextResult":
        extraction = {
            "lifecycle": "complete",
            "summary": None,
            "needs": [],
            "objections": [],
            "commitments": [],
            "next_step": None,
            "opportunity_signal": None,
        }
        if extraction_result:
            extraction.update(
                {
                    "summary": extraction_result.get("summary"),
                    "needs": list(extraction_result.get("needs") or []),
                    "objections": list(extraction_result.get("objections") or []),
                    "commitments": [
                        dict(c) for c in (extraction_result.get("commitments") or [])
                    ],
                    "next_step": (
                        dict(extraction_result["next_step"])
                        if extraction_result.get("next_step") is not None
                        else None
                    ),
                    "opportunity_signal": (
                        dict(extraction_result["opportunity_signal"])
                        if extraction_result.get("opportunity_signal") is not None
                        else None
                    ),
                }
            )

        return MeetingContextResult(
            schema="meeting_context_v1",
            agent="meeting_context_agent",
            provider=provider,
            meeting=dict(meeting),
            participants=[dict(p) for p in participants],
            extraction=extraction,
            evidence={
                "transcript_spans": [dict(e) for e in evidence_references],
                "extraction_confidence": float(extraction_confidence),
            },
            external_effects=0,
            policy_authority={
                "deterministic_policy_bypass": False,
                "notes": (
                    "Meeting Context Agent proposes structured context only; "
                    "deterministic policy remains authoritative for any CRM mutation."
                ),
            },
        )


def packet_extraction_overlay(context: Mapping[str, Any]) -> Dict[str, Any]:
    """Map meeting context extraction into meeting_follow_up_packet_v1 extraction shape."""
    extraction = dict(context["extraction"])
    return extraction
