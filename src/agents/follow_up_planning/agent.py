"""Follow-Up Planning Agent entrypoint (Phase 3 Unit 3).

Consumes ``meeting_context_v1`` (Unit 1) and ``relationship_context_v1``
(Unit 2), proposes a structured follow-up plan, invokes the deterministic
policy gate as the sole mutation-authorization surface, and emits a reviewable
``meeting_follow_up_packet_v1``. The agent proposes only — it never
self-authorizes CRM mutation, never calls live GHL, and never writes CRM.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

from .models import FollowUpPlanningRequest, FollowUpPlanningResult
from .packet import FollowUpPacketAssembler, utc_now, validate_follow_up_packet
from .schema import validate_follow_up_proposal


class FollowUpPlanningAgent:
    """Proposes structured follow-up plans under deterministic policy authority.

    Zero external effects: no live GHL reads, no CRM writes, no policy bypass.
    """

    agent_id = "follow_up_planning_agent"

    def __init__(
        self, assembler: Optional[FollowUpPacketAssembler] = None
    ) -> None:
        self.assembler = assembler or FollowUpPacketAssembler()

    def run(self, request: FollowUpPlanningRequest) -> FollowUpPlanningResult:
        meeting_context = dict(request.meeting_context)
        relationship_context = dict(request.relationship_context)

        meeting = dict(meeting_context.get("meeting") or {})
        if not meeting.get("meeting_id"):
            raise ValueError("meeting_context.meeting.meeting_id is required")
        if not list(meeting_context.get("participants") or []):
            raise ValueError("meeting_context.participants must be non-empty")
        resolution = dict(relationship_context.get("resolution") or {})
        resolution_status = str(resolution.get("status") or "not_found")

        extraction = dict(meeting_context.get("extraction") or {})
        longitudinal_context = relationship_context.get("longitudinal_context")
        confirmed_context_used = self._confirmed_context_used(longitudinal_context)
        summary = self._summary_for_proposal(
            extraction=extraction,
            longitudinal_context=longitudinal_context,
        )
        next_step = self._next_step_for_proposal(
            extraction=extraction,
            longitudinal_context=longitudinal_context,
        )
        recommended_stage = self._recommended_stage_for_proposal(
            extraction=extraction,
            longitudinal_context=longitudinal_context,
        )
        matched = resolution_status == "matched"

        # Proposal only: the agent requests intents; it never authorizes them.
        note_requested = bool(summary) and matched
        stage_requested = bool(recommended_stage) and matched

        run_id = request.run_id or f"unit3_run_{meeting['meeting_id']}"
        assembly = self.assembler.assemble(
            meeting_context=meeting_context,
            relationship_context=relationship_context,
            run_id=run_id,
            note_requested=note_requested,
            stage_requested=stage_requested,
            recommended_stage=recommended_stage,
            policy_context=confirmed_context_used,
        )
        packet = assembly.packet
        decision = assembly.decision

        proposal = self._build_proposal(
            request=request,
            run_id=run_id,
            summary=summary,
            next_step=next_step,
            resolution_status=resolution_status,
            resolution=resolution,
            recommended_stage=recommended_stage,
            note_requested=note_requested,
            stage_requested=stage_requested,
            confirmed_context_used=confirmed_context_used,
            assembly=assembly,
        )

        ok, errors = validate_follow_up_proposal(proposal)
        if not ok:
            raise ValueError(
                "Follow-up proposal failed schema validation: " + "; ".join(errors)
            )
        packet_errors = validate_follow_up_packet(packet)
        if packet_errors:
            raise ValueError(
                "Follow-up packet failed schema validation: "
                + "; ".join(packet_errors)
            )
        if proposal["external_effects"] != 0 or packet["external_effects"] != 0:
            raise ValueError("Follow-Up Planning Agent must set external_effects=0")
        if proposal["policy_authority"]["deterministic_policy_bypass"] is not False:
            raise ValueError("Deterministic policy bypass is forbidden")
        # Authority invariant: authorized intents exist only when the
        # deterministic policy gate was invoked and allowed them.
        intents = proposal["authorized_mutation_intents"]
        if (intents["note"] or intents["stage"]) and not assembly.policy_gate_invoked:
            raise ValueError(
                "Mutation intents require deterministic policy gate invocation"
            )

        return FollowUpPlanningResult(
            proposal=proposal,
            packet=packet,
            policy_gate_invoked=assembly.policy_gate_invoked,
            external_effects=0,
        )

    def _build_proposal(
        self,
        *,
        request: FollowUpPlanningRequest,
        run_id: str,
        summary: Optional[str],
        next_step: Dict[str, Any],
        resolution_status: str,
        resolution: Dict[str, Any],
        recommended_stage: Optional[str],
        note_requested: bool,
        stage_requested: bool,
        confirmed_context_used: Optional[Dict[str, Any]],
        assembly: Any,
    ) -> Dict[str, Any]:
        packet = assembly.packet
        decision = assembly.decision
        gate_invoked = assembly.policy_gate_invoked
        final_state = assembly.final_state

        if final_state == "completed":
            disposition = "proposed"
        elif final_state == "completed_with_review":
            disposition = "proposed_with_review"
        elif "LOW_EXTRACTION_CONFIDENCE" in assembly.reason_codes:
            disposition = "no_op"
        elif final_state == "blocked":
            disposition = "needs_review"
        else:
            disposition = "blocked"

        proposed_next_steps: List[str] = []
        if next_step.get("action"):
            proposed_next_steps.append(str(next_step["action"]))
        if disposition in {"needs_review", "blocked", "no_op"}:
            proposed_next_steps.append(
                "Human review required before any CRM mutation"
            )

        policy_evaluation = {
            "invoked": gate_invoked,
            "evaluator": "orchestration.policy.evaluate_policy",
            "note_write": decision.note_write if gate_invoked else "not_attempted",
            "stage_write": decision.stage_write if gate_invoked else "not_attempted",
            "reason_codes": list(assembly.reason_codes),
            "deterministic_policy_bypass": False,
            "context_supplied": bool(
                gate_invoked and assembly.policy_inputs_used.get("proposal_context")
            ),
            "context_source": (
                str(
                    (
                        assembly.policy_inputs_used.get("proposal_context") or {}
                    ).get("source")
                )
                if gate_invoked and assembly.policy_inputs_used.get("proposal_context")
                else None
            ),
        }

        proposal = {
            "schema": "follow_up_proposal_v1",
            "agent": self.agent_id,
            "run_id": run_id,
            "scenario_id": request.scenario_id,
            "disposition": disposition,
            "summary": summary,
            "proposed_next_steps": proposed_next_steps,
            "note_proposal": {
                "requested": bool(note_requested),
                "body_ref": (
                    "relationship_context.longitudinal_context"
                    if note_requested and confirmed_context_used is not None
                    else "extraction.summary"
                    if note_requested
                    else None
                ),
            },
            "stage_proposal": {
                "requested": bool(stage_requested),
                "from_stage": resolution.get("current_stage"),
                "to_stage": recommended_stage if stage_requested else None,
            },
            "crm_targets": {
                "contact_id": resolution.get("contact_id"),
                "opportunity_id": resolution.get("opportunity_id"),
            },
            "resolution_status": resolution_status,
            "policy_evaluation": policy_evaluation,
            "authorized_mutation_intents": {
                "note": [dict(i) for i in assembly.intents.get("note", [])],
                "stage": [dict(i) for i in assembly.intents.get("stage", [])],
            },
            "external_effects": 0,
            "policy_authority": {
                "deterministic_policy_bypass": False,
                "notes": (
                    "Follow-Up Planning Agent proposes facts, next steps, and "
                    "optional stage-change intent only; the deterministic policy "
                    "gate evaluates and authorizes any mutation intent. No live "
                    "GHL, no CRM writes, no policy bypass."
                ),
            },
        }
        if confirmed_context_used is not None:
            proposal["confirmed_context_used"] = confirmed_context_used
        return proposal

    @staticmethod
    def _confirmed_context_used(longitudinal_context: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(longitudinal_context, dict):
            return None
        confirmed_fact_ids = [
            str(item.get("fact_id"))
            for item in (longitudinal_context.get("current_confirmed_facts") or [])
            if isinstance(item, dict) and item.get("fact_id")
        ]
        unresolved_question_ids = [
            str(item.get("question_id"))
            for item in (longitudinal_context.get("unresolved_questions") or [])
            if isinstance(item, dict) and item.get("question_id")
        ]
        evidence_ids = sorted(
            {
                str(excerpt_id)
                for ref in (longitudinal_context.get("evidence_references") or [])
                if isinstance(ref, dict)
                for excerpt_id in (ref.get("excerpt_ids") or [])
                if excerpt_id
            }
        )
        return {
            "source": "relationship_context.longitudinal_context",
            "confirmed_fact_ids": confirmed_fact_ids,
            "unresolved_question_ids": unresolved_question_ids,
            "proposed_next_step": deepcopy(longitudinal_context.get("proposed_next_step")),
            "evidence_excerpt_ids": evidence_ids,
        }

    @staticmethod
    def _summary_for_proposal(
        *,
        extraction: Dict[str, Any],
        longitudinal_context: Any,
    ) -> Optional[str]:
        if not isinstance(longitudinal_context, dict):
            return extraction.get("summary")
        facts = {
            str(item.get("fact_id")): item
            for item in (longitudinal_context.get("current_confirmed_facts") or [])
            if isinstance(item, dict) and item.get("fact_id")
        }
        parts: List[str] = []
        primary_goal = (facts.get("goal.primary") or {}).get("value")
        if primary_goal:
            parts.append(f"Primary goal: {primary_goal}.")
        capacity = (
            facts.get("fact.preference.flexible_monthly_savings_capacity") or {}
        ).get("value")
        if capacity is not None:
            parts.append(f"Flexible monthly savings capacity: {capacity}.")
        for item in (longitudinal_context.get("new_facts") or [])[:1]:
            if isinstance(item, dict):
                parts.append(
                    f"New confirmed fact {item.get('fact_id')}: {item.get('value')}."
                )
        for item in (longitudinal_context.get("commitments_completed") or [])[:1]:
            if isinstance(item, dict):
                parts.append(f"Completed commitment: {item.get('action')}.")
        for item in (longitudinal_context.get("commitments_open") or [])[:1]:
            if isinstance(item, dict):
                parts.append(f"Open commitment: {item.get('action')}.")
        return " ".join(parts) if parts else extraction.get("summary")

    @staticmethod
    def _next_step_for_proposal(
        *,
        extraction: Dict[str, Any],
        longitudinal_context: Any,
    ) -> Dict[str, Any]:
        if isinstance(longitudinal_context, dict):
            next_step = longitudinal_context.get("proposed_next_step")
            if isinstance(next_step, dict) and next_step.get("action"):
                return dict(next_step)
        return dict(extraction.get("next_step") or {})

    @staticmethod
    def _recommended_stage_for_proposal(
        *,
        extraction: Dict[str, Any],
        longitudinal_context: Any,
    ) -> Optional[str]:
        if isinstance(longitudinal_context, dict):
            for item in longitudinal_context.get("current_confirmed_facts") or []:
                if (
                    isinstance(item, dict)
                    and item.get("fact_id") == "opportunity.recommended_stage"
                ):
                    return item.get("value")
        signal = extraction.get("opportunity_signal") or {}
        return signal.get("recommended_stage")

    def telemetry(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "authority": "propose_only",
            "policy_gate": "orchestration.policy.evaluate_policy",
            "external_effects": 0,
            "deterministic_policy_bypass": False,
            "ghl_live_calls": 0,
            "ghl_writes": 0,
            "real_customer_data": 0,
            "generated_at": utc_now(),
        }
