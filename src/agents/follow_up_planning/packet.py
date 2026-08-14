"""Reviewable meeting_follow_up_packet_v1 assembly for Phase 3 Unit 3.

Assembles the canonical packet from Unit 1 ``meeting_context_v1`` and Unit 2
``relationship_context_v1`` artifacts, driving the deterministic workflow state
machine and invoking the deterministic policy evaluator (the sole mutation
authorization surface). Intent-only: external effects remain 0.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from jsonschema import Draft202012Validator

from orchestration.models import base_packet
from orchestration.policy import bound_intents, evaluate_policy
from orchestration.state_machine import StateMachine


def _repo_root() -> Path:
    # src/agents/follow_up_planning/packet.py -> repo root
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def _packet_schema() -> Dict[str, Any]:
    path = _repo_root() / "contracts" / "meeting_follow_up_packet.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_follow_up_packet(packet: Mapping[str, Any]) -> List[str]:
    """Validate packet against meeting_follow_up_packet.schema.json."""
    validator = Draft202012Validator(_packet_schema())
    errors = sorted(validator.iter_errors(dict(packet)), key=lambda e: list(e.path))
    messages = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        messages.append(f"{path}: {err.message}")
    return messages


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


@dataclass
class PacketAssembly:
    packet: Dict[str, Any]
    decision: Optional[Any] = None  # PolicyDecision when the gate was invoked
    intents: Dict[str, List[Dict[str, Any]]] = field(
        default_factory=lambda: {"note": [], "stage": []}
    )
    reason_codes: List[str] = field(default_factory=list)
    policy_gate_invoked: bool = False
    policy_inputs_used: Dict[str, Any] = field(default_factory=dict)
    final_state: str = "received"


class FollowUpPacketAssembler:
    """Assembles meeting_follow_up_packet_v1 from agent-produced contexts.

    Reuses the Phase 1 deterministic state machine and policy evaluator. The
    assembler never fabricates CRM facts: when context is insufficient, the
    packet fails closed (blocked / no fabricated crm_resolution values).
    """

    def __init__(self, state_machine: Optional[StateMachine] = None) -> None:
        self.sm = state_machine or StateMachine.from_yaml(
            _repo_root() / "contracts" / "workflow_states.yaml"
        )

    def assemble(
        self,
        *,
        meeting_context: Mapping[str, Any],
        relationship_context: Mapping[str, Any],
        run_id: str,
        note_requested: bool,
        stage_requested: bool,
        recommended_stage: Optional[str],
        policy_context: Optional[Mapping[str, Any]] = None,
        created_at: Optional[str] = None,
    ) -> PacketAssembly:
        meeting = deepcopy(dict(meeting_context.get("meeting") or {}))
        participants = deepcopy(list(meeting_context.get("participants") or []))
        extraction_ctx = deepcopy(dict(meeting_context.get("extraction") or {}))
        evidence_ctx = deepcopy(dict(meeting_context.get("evidence") or {}))
        confidence = evidence_ctx.get("extraction_confidence")

        ts = created_at or utc_now()
        packet = base_packet(
            run_id=run_id,
            status="received",
            meeting=meeting,
            participants=participants,
            created_at=ts,
            started_at=ts,
        )
        packet["audit"]["agents_used"] = [
            "meeting_context_agent",
            "relationship_context_agent",
            "follow_up_planning_agent",
        ]

        # received -> extracting
        self._advance(packet, "extracting", when="transcript_accepted")
        packet["evidence"] = {
            "transcript_spans": list(evidence_ctx.get("transcript_spans") or []),
            "extraction_confidence": confidence,
        }
        if confidence is None or float(confidence) < self.sm.extraction_abort_threshold:
            # Insufficient context: no fabricated CRM facts; extraction aborted.
            packet["extraction"] = {
                "lifecycle": "aborted",
                "summary": None,
                "needs": [],
                "objections": [],
                "commitments": [],
                "next_step": None,
                "opportunity_signal": None,
            }
            return self._finalize(
                packet,
                "blocked",
                when="extraction_confidence_lt_extraction_abort_threshold",
                reason_codes=["LOW_EXTRACTION_CONFIDENCE"],
            )
        packet["extraction"] = extraction_ctx

        # extracting -> resolving
        self._advance(
            packet,
            "resolving",
            when="extraction_confidence_gte_extraction_abort_threshold",
        )
        overlay = self._crm_overlay(relationship_context)
        packet["crm_resolution"] = overlay
        crm_status = overlay["status"]
        if crm_status == "tool_failure":
            return self._finalize(
                packet,
                "failed",
                when="required_crm_resolution_tool_read_failure",
                reason_codes=["GHL_TOOL_FAILURE"],
            )
        if crm_status == "ambiguous":
            rel_status = str(
                (relationship_context.get("resolution") or {}).get("status") or ""
            )
            if rel_status == "opportunity_ambiguous":
                return self._finalize(
                    packet,
                    "blocked",
                    when="contact_ambiguous",
                    reason_codes=["AMBIGUOUS_OPPORTUNITY"],
                )
            return self._finalize(
                packet,
                "blocked",
                when="contact_ambiguous",
                reason_codes=["AMBIGUOUS_CONTACT"],
            )
        if crm_status == "not_found":
            return self._finalize(
                packet,
                "blocked",
                when="contact_not_found",
                reason_codes=["CONTACT_NOT_FOUND"],
            )
        if crm_status == "opportunity_missing":
            return self._finalize(
                packet,
                "blocked",
                when="opportunity_missing",
                reason_codes=["OPPORTUNITY_NOT_FOUND"],
            )
        if crm_status != "matched":
            raise ValueError(f"unexpected crm resolution status: {crm_status}")

        # resolving -> evaluating: invoke the deterministic policy gate.
        self._advance(
            packet, "evaluating", when="contact_matched_and_opportunity_present"
        )
        policy_inputs = {
            "note_write_request": bool(note_requested),
            "stage_write_request": bool(stage_requested and recommended_stage),
            "recommended_stage": recommended_stage,
            "force_note_denied": False,
            "force_stage_denied": False,
        }
        if policy_context is not None:
            policy_inputs["proposal_context"] = deepcopy(dict(policy_context))
        decision = evaluate_policy(
            self.sm,
            extraction_confidence=float(confidence),
            crm=packet["crm_resolution"],
            policy_inputs=policy_inputs,
            extraction_result=extraction_ctx,
        )
        packet["policy"] = {
            "lifecycle": "complete",
            "note_write": decision.note_write,
            "stage_write": decision.stage_write,
            "reason_codes": list(decision.reason_codes),
        }

        if not decision.any_permitted:
            codes = list(decision.reason_codes)
            if "NOTE_WRITE_BLOCKED" not in codes and decision.note_write == "blocked":
                codes.append("NOTE_WRITE_BLOCKED")
            packet["policy"]["reason_codes"] = codes
            packet["mutation_intents"] = {"note": [], "stage": []}
            assembly = self._finalize(
                packet,
                "blocked",
                when="note_policy_blocked_and_no_permitted_action_remains",
                reason_codes=codes,
            )
            assembly.decision = decision
            assembly.policy_gate_invoked = True
            assembly.policy_inputs_used = deepcopy(policy_inputs)
            return assembly

        # evaluating -> writing: record policy-bounded intents only (no effects).
        self._advance(
            packet, "writing", when="at_least_one_mutation_intent_permitted"
        )
        intents = bound_intents(
            decision,
            max_note=self.sm.max_note_intents,
            max_stage=self.sm.max_stage_intents,
        )
        packet["mutation_intents"] = intents
        packet["mutations"] = {
            "lifecycle": "intent_only",
            "note": {"attempted": False, "verified": False, "record_id": None},
            "opportunity_stage": {
                "attempted": False,
                "from_stage": packet["crm_resolution"].get("current_stage"),
                "to_stage": intents["stage"][0]["to_stage"]
                if intents["stage"]
                else None,
                "verified": False,
            },
        }
        packet["external_effects"] = 0
        self._apply_brief(packet, decision)

        review = bool(decision.reason_codes) or (
            intents["note"]
            and not intents["stage"]
            and decision.stage_write != "allowed"
        )
        if review:
            assembly = self._finalize(
                packet,
                "completed_with_review",
                when="note_intent_recorded_and_stage_suppressed_or_review_required",
                reason_codes=list(decision.reason_codes),
            )
        else:
            assembly = self._finalize(
                packet,
                "completed",
                when="intents_recorded_and_no_review_flags",
                reason_codes=list(decision.reason_codes),
            )
        assembly.decision = decision
        assembly.intents = intents
        assembly.policy_gate_invoked = True
        assembly.policy_inputs_used = deepcopy(policy_inputs)
        return assembly

    @staticmethod
    def _crm_overlay(relationship_context: Mapping[str, Any]) -> Dict[str, Any]:
        """Map relationship_context_v1 resolution into packet crm_resolution."""
        resolution = dict(relationship_context.get("resolution") or {})
        status = str(resolution.get("status") or "not_found")
        # Packet enum lacks resolver-internal statuses; map fail-closed.
        if status == "insufficient_context":
            packet_status = "not_found"
        elif status == "opportunity_ambiguous":
            packet_status = "ambiguous"
        elif status in {"matched", "ambiguous", "not_found", "opportunity_missing",
                        "tool_failure", "not_attempted"}:
            packet_status = status
        else:
            packet_status = "not_found"
        match_basis = resolution.get("match_basis") or "none"
        if match_basis not in {"email", "phone", "name", "none", "not_attempted"}:
            match_basis = "none"
        return {
            "lifecycle": (
                "complete" if resolution.get("lifecycle") == "complete" else "failed"
            ),
            "status": packet_status,
            "contact_id": resolution.get("contact_id"),
            "opportunity_id": resolution.get("opportunity_id"),
            "match_basis": match_basis,
            "candidate_count": int(resolution.get("candidate_count") or 0),
            "current_stage": resolution.get("current_stage"),
        }

    def _apply_brief(self, packet: Dict[str, Any], decision: Any) -> None:
        extraction = packet["extraction"]
        actions = []
        if decision.note_write == "allowed":
            actions.append("plan_note_intent")
        if decision.stage_write == "allowed":
            actions.append("plan_stage_intent")
        next_step = extraction.get("next_step") or {}
        packet["brief"] = {
            "lifecycle": "complete",
            "headline": "Meeting follow-up proposal reviewed (Unit 3 intent-only)",
            "meeting_summary": extraction.get("summary"),
            "crm_actions": actions,
            "next_action": next_step.get("action") or "Review follow-up brief",
            "salesperson_attention_required": (
                bool(decision.reason_codes) or decision.stage_write != "allowed"
            ),
        }

    def _advance(self, packet: Dict[str, Any], target: str, *, when: str) -> None:
        source = packet["run"]["status"]
        self.sm.validate_transition(source, target, when=when)
        packet["run"]["status"] = target
        packet["audit"]["final_disposition"] = "pending"

    def _finalize(
        self,
        packet: Dict[str, Any],
        target: str,
        *,
        when: str,
        reason_codes: List[str],
    ) -> PacketAssembly:
        source = packet["run"]["status"]
        self.sm.validate_transition(source, target, when=when)
        packet["run"]["status"] = target
        packet["audit"]["completed_at"] = utc_now()
        packet["audit"]["final_disposition"] = target
        existing = list(packet.get("policy", {}).get("reason_codes") or [])
        merged = list(existing)
        for code in reason_codes:
            if code not in merged:
                merged.append(code)
        if packet.get("policy"):
            packet["policy"]["reason_codes"] = merged
        if target in {"blocked", "failed"}:
            packet["mutation_intents"] = {"note": [], "stage": []}
            packet["brief"] = {
                "lifecycle": "complete",
                "headline": f"Run {target}",
                "meeting_summary": packet["extraction"].get("summary"),
                "crm_actions": [],
                "next_action": (
                    "Human review required"
                    if target == "blocked"
                    else "Investigate failure"
                ),
                "salesperson_attention_required": True,
            }
        packet["external_effects"] = 0
        return PacketAssembly(
            packet=packet,
            reason_codes=merged,
            final_state=target,
        )
