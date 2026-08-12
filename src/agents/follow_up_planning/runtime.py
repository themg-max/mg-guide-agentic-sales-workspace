"""Google ADK runtime orchestration for meeting_follow_up_v1 Phase 3 Unit 3.

Extends the Unit 2 Google ADK package runtime with the Follow-Up Planning
Agent as a third sequential agent:

    synthetic transcript
      -> Meeting Context Agent (reused from Unit 1, wrapped as ADK BaseAgent)
      -> Google ADK SequentialAgent + Runner + InMemorySessionService
      -> Relationship Context Agent (reused from Unit 2, ADK BaseAgent)
      -> Phase 2B offline GHL adapter (synthetic CRM only)
      -> relationship_context_v1
      -> Follow-Up Planning Agent (ADK BaseAgent; proposes only)
      -> deterministic policy gate (orchestration.policy.evaluate_policy)
      -> reviewable meeting_follow_up_packet_v1
      -> STOP  (no mutation execution; external effects remain 0)

The google-adk package is REQUIRED (inherited fail-closed posture from the
Unit 2 runtime; no local fallback). Live CRM/GHL/Firestore/deployment remain
forbidden. All runtime-truth markers are derived from measured runtime state.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from agents.adk_runtime.markers import (
    ADK_STATUS_RUNTIME_INTEGRATED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    derive_runtime_markers,
)
from agents.adk_runtime.runtime import (
    APP_NAME,
    USER_ID,
    GoogleAdkRuntime,
    RuntimeAgentSpec,
    _import_google_adk_primitives,
)
from agents.adk_runtime.session import AgentInvocationRecord, RuntimeSession
from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context.agent import RelationshipContextAgent
from agents.relationship_context.models import RelationshipRequest

from .agent import FollowUpPlanningAgent
from .models import FollowUpPlanningRequest

UNIT3_AGENT_GRAPH: Sequence[RuntimeAgentSpec] = (
    RuntimeAgentSpec(
        agent_id="meeting_context_agent",
        role="meeting_context",
        description="Extract structured meeting context from synthetic transcript",
    ),
    RuntimeAgentSpec(
        agent_id="relationship_context_agent",
        role="relationship_context",
        description="Resolve synthetic CRM relationship context offline",
    ),
    RuntimeAgentSpec(
        agent_id="follow_up_planning_agent",
        role="follow_up_planning",
        description=(
            "Propose structured follow-up plan and assemble reviewable "
            "meeting_follow_up_packet_v1 under the deterministic policy gate"
        ),
    ),
)

_STATE_KEYS = (
    "meeting_context",
    "relationship_context",
    "follow_up_proposal",
    "follow_up_packet",
)


def _build_unit3_adk_agents(
    prim: Dict[str, Any],
    *,
    meeting_agent: MeetingContextAgent,
    relationship_agent: RelationshipContextAgent,
    follow_up_agent: FollowUpPlanningAgent,
) -> Any:
    """Build the ADK SequentialAgent wrapping all three deterministic delegates."""
    BaseAgent = prim["BaseAgent"]
    SequentialAgent = prim["SequentialAgent"]
    Event = prim["Event"]
    EventActions = prim["EventActions"]
    genai_types = prim["genai_types"]

    def _event(ctx: Any, name: str, payload: Dict[str, Any]) -> Any:
        return Event(
            invocation_id=ctx.invocation_id,
            author=name,
            branch=ctx.branch,
            content=genai_types.Content(
                role="model",
                parts=[genai_types.Part(text=json.dumps(payload, sort_keys=True))],
            ),
            actions=EventActions(state_delta=payload),
        )

    class MeetingContextAdkAgent(BaseAgent):
        """ADK agent wrapper around the Unit 1 Meeting Context Agent."""

        delegate: Any = None

        async def _run_async_impl(self, ctx: Any) -> Any:
            try:
                request = ctx.session.state["meeting_request"]
                result = self.delegate.run(request)
                payload = {"meeting_context": result.to_dict()}
            except Exception as exc:
                payload = {
                    "meeting_context": None,
                    "errors": [f"meeting_context_agent: {type(exc).__name__}: {exc}"],
                }
            yield _event(ctx, self.name, payload)

    class RelationshipContextAdkAgent(BaseAgent):
        """ADK agent wrapper around the Unit 2 Relationship Context Agent."""

        delegate: Any = None

        async def _run_async_impl(self, ctx: Any) -> Any:
            meeting_context = ctx.session.state.get("meeting_context")
            if meeting_context is None:
                payload = {
                    "relationship_context": None,
                    "errors": [
                        "relationship_context_agent: meeting_context missing"
                    ],
                }
            else:
                try:
                    request = RelationshipRequest(
                        meeting_context=meeting_context,
                        run_id=ctx.session.state.get("run_id"),
                        scenario_id=ctx.session.state.get("scenario_id"),
                    )
                    result = self.delegate.run(request)
                    payload = {"relationship_context": result.to_dict()}
                except Exception as exc:
                    payload = {
                        "relationship_context": None,
                        "errors": [
                            f"relationship_context_agent: "
                            f"{type(exc).__name__}: {exc}"
                        ],
                    }
            yield _event(ctx, self.name, payload)

    class FollowUpPlanningAdkAgent(BaseAgent):
        """ADK agent wrapper around the Unit 3 Follow-Up Planning Agent."""

        delegate: Any = None

        async def _run_async_impl(self, ctx: Any) -> Any:
            meeting_context = ctx.session.state.get("meeting_context")
            relationship_context = ctx.session.state.get("relationship_context")
            if meeting_context is None or relationship_context is None:
                payload = {
                    "follow_up_proposal": None,
                    "follow_up_packet": None,
                    "follow_up_policy_gate_invoked": False,
                    "errors": [
                        "follow_up_planning_agent: meeting_context or "
                        "relationship_context missing"
                    ],
                }
            else:
                try:
                    request = FollowUpPlanningRequest(
                        meeting_context=meeting_context,
                        relationship_context=relationship_context,
                        run_id=ctx.session.state.get("run_id"),
                        scenario_id=ctx.session.state.get("scenario_id"),
                    )
                    result = self.delegate.run(request)
                    payload = {
                        "follow_up_proposal": result.proposal,
                        "follow_up_packet": result.packet,
                        "follow_up_policy_gate_invoked": (
                            result.policy_gate_invoked
                        ),
                    }
                except Exception as exc:
                    payload = {
                        "follow_up_proposal": None,
                        "follow_up_packet": None,
                        "follow_up_policy_gate_invoked": False,
                        "errors": [
                            f"follow_up_planning_agent: "
                            f"{type(exc).__name__}: {exc}"
                        ],
                    }
            yield _event(ctx, self.name, payload)

    meeting_adk = MeetingContextAdkAgent(
        name="meeting_context_agent", delegate=meeting_agent
    )
    relationship_adk = RelationshipContextAdkAgent(
        name="relationship_context_agent", delegate=relationship_agent
    )
    follow_up_adk = FollowUpPlanningAdkAgent(
        name="follow_up_planning_agent", delegate=follow_up_agent
    )
    return SequentialAgent(
        name="unit3_meeting_to_follow_up_packet",
        sub_agents=[meeting_adk, relationship_adk, follow_up_adk],
    )


@dataclass
class Unit3RunResult:
    ok: bool
    session: RuntimeSession
    meeting_context: Optional[Dict[str, Any]]
    relationship_context: Optional[Dict[str, Any]]
    follow_up_proposal: Optional[Dict[str, Any]]
    follow_up_packet: Optional[Dict[str, Any]]
    errors: List[str]
    google_adk_package_bound: bool
    google_adk_runtime_started: bool
    adk_integration_status: str
    adk_runtime_backend: str
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool
    meeting_context_reused: bool
    relationship_context_reused: bool
    follow_up_planning_agent_implemented: bool
    follow_up_proposal_valid: bool
    deterministic_policy_gate_invoked: bool
    deterministic_policy_bypass: bool
    external_effects: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "session": self.session.to_dict(),
            "meeting_context": self.meeting_context,
            "relationship_context": self.relationship_context,
            "follow_up_proposal": self.follow_up_proposal,
            "follow_up_packet": self.follow_up_packet,
            "errors": list(self.errors),
            "google_adk_package_bound": self.google_adk_package_bound,
            "google_adk_runtime_started": self.google_adk_runtime_started,
            "adk_integration_status": self.adk_integration_status,
            "adk_runtime_backend": self.adk_runtime_backend,
            "adk_runtime_primitive_used": self.adk_runtime_primitive_used,
            "local_adk_fallback_used": self.local_adk_fallback_used,
            "meeting_context_reused": self.meeting_context_reused,
            "relationship_context_reused": self.relationship_context_reused,
            "follow_up_planning_agent_implemented": (
                self.follow_up_planning_agent_implemented
            ),
            "follow_up_proposal_valid": self.follow_up_proposal_valid,
            "deterministic_policy_gate_invoked": (
                self.deterministic_policy_gate_invoked
            ),
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
        }


class Unit3FollowUpRuntime(GoogleAdkRuntime):
    """Google ADK package-backed sequential runtime for Unit 3.

    Reuses the Unit 2 runtime (package binding, Runner/SequentialAgent/session
    primitives, fail-closed start) and adds the Follow-Up Planning Agent to the
    sequential graph. No local orchestration fallback.
    """

    agent_graph = UNIT3_AGENT_GRAPH

    def __init__(
        self,
        *,
        meeting_agent: Optional[MeetingContextAgent] = None,
        relationship_agent: Optional[RelationshipContextAgent] = None,
        follow_up_agent: Optional[FollowUpPlanningAgent] = None,
    ) -> None:
        super().__init__(
            meeting_agent=meeting_agent,
            relationship_agent=relationship_agent,
        )
        self.follow_up_agent = follow_up_agent or FollowUpPlanningAgent()

    def start(self) -> "Unit3FollowUpRuntime":
        """Bind the google-adk package and construct the Unit 3 agent graph."""
        prim = _import_google_adk_primitives()
        root_agent = _build_unit3_adk_agents(
            prim,
            meeting_agent=self.meeting_agent,
            relationship_agent=self.relationship_agent,
            follow_up_agent=self.follow_up_agent,
        )
        session_service = prim["InMemorySessionService"]()
        runner = prim["Runner"](
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        version = getattr(prim["google_adk"], "__version__", "unknown")
        self._prim = prim
        self._runner = runner
        self._session_service = session_service
        self._backend = RUNTIME_BACKEND_GOOGLE_ADK
        self._google_adk_bound = True
        self._google_adk_bind_detail = (
            f"google.adk Runner/SequentialAgent/InMemorySessionService "
            f"constructed (version={version})"
        )
        self._started = True
        return self

    async def _execute_unit3(
        self,
        *,
        meeting_request: ProviderRequest,
        run_id: Optional[str],
        scenario_id: Optional[str],
    ) -> Tuple[Any, List[Any], List[str]]:
        """Execute the ADK Runner and return (final_session, events, errors)."""
        prim = self._prim
        assert prim is not None
        initial_state: Dict[str, Any] = {
            "meeting_request": meeting_request,
            "run_id": run_id,
            "scenario_id": scenario_id,
            "errors": [],
            "meeting_context": None,
            "relationship_context": None,
            "follow_up_proposal": None,
            "follow_up_packet": None,
            "follow_up_policy_gate_invoked": False,
            "stop_after": "follow_up_planning_agent",
            "mutation_execution": "not_authorized_intent_only",
        }
        session = await self._session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        new_message = prim["genai_types"].Content(
            role="user",
            parts=[
                prim["genai_types"].Part(
                    text=(
                        "run unit3 meeting_context -> relationship_context "
                        "-> follow_up_planning -> STOP"
                    )
                )
            ],
        )
        events: List[Any] = []
        runner_errors: List[str] = []
        try:
            async for event in self._runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=new_message,
            ):
                events.append(event)
        except Exception as exc:  # pragma: no cover - defensive
            runner_errors.append(f"adk_runner: {type(exc).__name__}: {exc}")
        final_session = await self._session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session.id
        )
        return final_session, events, runner_errors

    def run_unit3(
        self,
        *,
        meeting_request: ProviderRequest,
        run_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
    ) -> Unit3RunResult:
        """Execute the Unit 3 pipeline through the Google ADK Runner and stop."""
        self.ensure_started()
        session, events, runner_errors = asyncio.run(
            self._execute_unit3(
                meeting_request=meeting_request,
                run_id=run_id,
                scenario_id=scenario_id,
            )
        )

        state = dict(session.state) if session is not None else {}
        meeting_context = state.get("meeting_context")
        relationship_context = state.get("relationship_context")
        proposal = state.get("follow_up_proposal")
        packet = state.get("follow_up_packet")
        gate_invoked = bool(state.get("follow_up_policy_gate_invoked"))

        # ADK primitive use requires events authored by all three sub-agents.
        authors = [getattr(e, "author", None) for e in events]
        expected_authors = [a.agent_id for a in UNIT3_AGENT_GRAPH]
        primitive_used = all(a in authors for a in expected_authors)
        self._primitive_used = self._primitive_used or primitive_used

        record = RuntimeSession(
            session_id=str(session.id) if session is not None else "unknown",
            run_id=str(state.get("run_id") or run_id or "unknown"),
            backend=self._backend,
            started=True,
            completed=True,
        )
        record.state = {k: v for k, v in state.items() if k != "meeting_request"}
        for spec in UNIT3_AGENT_GRAPH:
            if spec.agent_id not in authors:
                continue
            if spec.role == "follow_up_planning":
                output = proposal
                output_schema = (proposal or {}).get("schema") if proposal else None
            else:
                output = state.get(spec.role)
                output_schema = (output or {}).get("schema") if output else None
            record.record_invocation(
                AgentInvocationRecord(
                    agent_id=spec.agent_id,
                    status="ok" if output is not None else "error",
                    output_schema=output_schema,
                    error=(
                        None
                        if output is not None
                        else f"{spec.agent_id} produced no output"
                    ),
                    external_effects=int((output or {}).get("external_effects", 0)),
                )
            )

        errors: List[str] = list(runner_errors)
        errors.extend(str(e) for e in (state.get("errors") or []))

        bypass = False
        proposal_valid = False

        if meeting_context is None:
            errors.append("meeting_context missing")
        else:
            if meeting_context.get("external_effects", 0) != 0:
                errors.append("meeting_context external_effects must be 0")
            if meeting_context.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                bypass = True
                errors.append("meeting_context attempted deterministic policy bypass")

        if relationship_context is None:
            errors.append("relationship_context missing")
        else:
            if relationship_context.get("external_effects", 0) != 0:
                errors.append("relationship_context external_effects must be 0")
            if relationship_context.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                bypass = True
                errors.append(
                    "relationship_context attempted deterministic policy bypass"
                )
            crm = relationship_context.get("crm_source") or {}
            if crm.get("live_calls", 0) != 0 or crm.get("writes", 0) != 0:
                errors.append("CRM live calls/writes must remain 0")
            if crm.get("mode") != "offline_synthetic":
                errors.append("crm_source.mode must be offline_synthetic")
            if crm.get("real_customer_data", 0) != 0:
                errors.append("real_customer_data must be 0")

        if proposal is None or packet is None:
            errors.append("follow_up_proposal/follow_up_packet missing")
        else:
            proposal_valid = proposal.get("schema") == "follow_up_proposal_v1"
            if not proposal_valid:
                errors.append("follow_up_proposal schema must be follow_up_proposal_v1")
            if packet.get("schema") != "meeting_follow_up_packet_v1":
                errors.append(
                    "follow_up_packet schema must be meeting_follow_up_packet_v1"
                )
            if proposal.get("external_effects", 0) != 0:
                errors.append("follow_up_proposal external_effects must be 0")
            if packet.get("external_effects", 0) != 0:
                errors.append("follow_up_packet external_effects must be 0")
            for container, label in ((proposal, "proposal"), (packet, "packet")):
                authority = container.get("policy_authority") or {}
                if authority.get("deterministic_policy_bypass"):
                    bypass = True
                    errors.append(
                        f"follow_up_{label} attempted deterministic policy bypass"
                    )
            evaluation = proposal.get("policy_evaluation") or {}
            if evaluation.get("deterministic_policy_bypass"):
                bypass = True
                errors.append("policy_evaluation claimed deterministic bypass")
            # Authority invariant: intents only exist under gate invocation.
            intents = proposal.get("authorized_mutation_intents") or {}
            if (intents.get("note") or intents.get("stage")) and not gate_invoked:
                bypass = True
                errors.append(
                    "mutation intents present without policy gate invocation"
                )
            mutations = packet.get("mutations") or {}
            if mutations.get("lifecycle") != "intent_only" and packet.get("run", {}).get(
                "status"
            ) in {"completed", "completed_with_review"}:
                errors.append("mutations must remain intent_only")
            for mut_key in ("note", "opportunity_stage"):
                mut = mutations.get(mut_key) or {}
                if mut.get("attempted") or mut.get("verified"):
                    errors.append(f"mutations.{mut_key} must not be attempted")

        external_effects = int(record.external_effects)
        if packet is not None:
            external_effects = max(external_effects, int(packet.get("external_effects", 0)))

        markers = derive_runtime_markers(
            google_adk_package_bound=self._google_adk_bound,
            runtime_backend=self._backend,
            runtime_started=self._started,
            adk_runtime_primitive_used=primitive_used,
        )

        ok = (
            not errors
            and markers["google_adk_runtime_started"]
            and markers["adk_integration_status"] == ADK_STATUS_RUNTIME_INTEGRATED
            and markers["runtime_backend"] == RUNTIME_BACKEND_GOOGLE_ADK
            and markers["adk_runtime_primitive_used"]
            and not markers["local_adk_fallback_used"]
            and meeting_context is not None
            and relationship_context is not None
            and proposal is not None
            and packet is not None
            and proposal_valid
            and external_effects == 0
            and not bypass
        )

        return Unit3RunResult(
            ok=ok,
            session=record,
            meeting_context=meeting_context,
            relationship_context=relationship_context,
            follow_up_proposal=proposal,
            follow_up_packet=packet,
            errors=errors,
            google_adk_package_bound=markers["google_adk_package_bound"],
            google_adk_runtime_started=markers["google_adk_runtime_started"],
            adk_integration_status=markers["adk_integration_status"],
            adk_runtime_backend=markers["runtime_backend"],
            adk_runtime_primitive_used=markers["adk_runtime_primitive_used"],
            local_adk_fallback_used=markers["local_adk_fallback_used"],
            meeting_context_reused=meeting_context is not None,
            relationship_context_reused=relationship_context is not None,
            follow_up_planning_agent_implemented=proposal is not None,
            follow_up_proposal_valid=proposal_valid,
            deterministic_policy_gate_invoked=gate_invoked,
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
        )
