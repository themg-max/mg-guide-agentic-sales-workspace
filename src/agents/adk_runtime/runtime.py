"""Google ADK runtime orchestration for meeting_follow_up_v1 Phase 3 Unit 2.

This module orchestrates the Unit 2 sequence with *actual* Google ADK
runtime/agent primitives (``google.adk`` package):

    synthetic transcript
      -> Meeting Context Agent (reused from Unit 1, wrapped as ADK BaseAgent)
      -> Google ADK SequentialAgent + Runner + InMemorySessionService
      -> Relationship Context Agent (wrapped as ADK BaseAgent)
      -> Phase 2B offline GHL adapter (synthetic CRM only)
      -> relationship_context_v1
      -> STOP  (Follow-Up Planning Agent is not invoked)

The google-adk package is REQUIRED. There is no local/custom fallback
orchestration: when the package is unavailable the runtime fails closed
(``start()`` raises ``GoogleAdkPackageUnavailable`` and no runtime-started
marker can be derived). Live CRM/GHL/Firestore/deployment remain forbidden.

All runtime-truth markers are derived from measured runtime state (package
binding, backend, consumed ADK events, session state) — never hard-coded.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context.agent import RelationshipContextAgent
from agents.relationship_context.models import RelationshipRequest

from .markers import (
    ADK_STATUS_NOT_STARTED,
    ADK_STATUS_RUNTIME_INTEGRATED,
    GEMINI_ADK_STARTED,
    GEMINI_PROVIDER_STARTED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    derive_runtime_markers,
)
from .session import AgentInvocationRecord, RuntimeSession

APP_NAME = "mg_guide_meeting_follow_up_v1"
USER_ID = "synthetic_unit2"


class GoogleAdkPackageUnavailable(RuntimeError):
    """Raised when the google-adk package cannot be bound. Fail closed."""


def _import_google_adk_primitives() -> Dict[str, Any]:
    """Import supported Google ADK runtime/agent orchestration primitives."""
    try:
        import google.adk  # type: ignore
        from google.adk.agents import BaseAgent, SequentialAgent  # type: ignore
        from google.adk.events import Event, EventActions  # type: ignore
        from google.adk.runners import Runner  # type: ignore
        from google.adk.sessions import InMemorySessionService  # type: ignore
        from google.genai import types as genai_types  # type: ignore
    except Exception as exc:  # pragma: no cover - exercised via monkeypatch
        raise GoogleAdkPackageUnavailable(
            f"google-adk package unavailable ({type(exc).__name__}: {exc}); "
            "Unit 2 has no local fallback runtime and fails closed"
        ) from exc
    return {
        "google_adk": google.adk,
        "BaseAgent": BaseAgent,
        "SequentialAgent": SequentialAgent,
        "Event": Event,
        "EventActions": EventActions,
        "Runner": Runner,
        "InMemorySessionService": InMemorySessionService,
        "genai_types": genai_types,
    }


@dataclass(frozen=True)
class RuntimeAgentSpec:
    agent_id: str
    role: str
    description: str


UNIT2_AGENT_GRAPH: Sequence[RuntimeAgentSpec] = (
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
)


def _build_adk_agents(
    prim: Dict[str, Any],
    *,
    meeting_agent: MeetingContextAgent,
    relationship_agent: RelationshipContextAgent,
) -> Any:
    """Build the ADK SequentialAgent wrapping both deterministic delegates."""
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

    meeting_adk = MeetingContextAdkAgent(
        name="meeting_context_agent", delegate=meeting_agent
    )
    relationship_adk = RelationshipContextAdkAgent(
        name="relationship_context_agent", delegate=relationship_agent
    )
    return SequentialAgent(
        name="unit2_meeting_to_relationship_context",
        sub_agents=[meeting_adk, relationship_adk],
    )


@dataclass
class RuntimeRunResult:
    ok: bool
    session: RuntimeSession
    meeting_context: Optional[Dict[str, Any]]
    relationship_context: Optional[Dict[str, Any]]
    errors: List[str]
    google_adk_package_bound: bool
    google_adk_runtime_started: bool
    adk_integration_status: str
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool
    meeting_context_agent_reused: bool
    relationship_context_agent_implemented: bool
    offline_ghl_adapter_used: bool
    synthetic_crm_context_only: bool
    relationship_context_output_valid: bool
    deterministic_policy_bypass: bool
    external_effects: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "session": self.session.to_dict(),
            "meeting_context": self.meeting_context,
            "relationship_context": self.relationship_context,
            "errors": list(self.errors),
            "google_adk_package_bound": self.google_adk_package_bound,
            "google_adk_runtime_started": self.google_adk_runtime_started,
            "adk_integration_status": self.adk_integration_status,
            "adk_runtime_primitive_used": self.adk_runtime_primitive_used,
            "local_adk_fallback_used": self.local_adk_fallback_used,
            "meeting_context_agent_reused": self.meeting_context_agent_reused,
            "relationship_context_agent_implemented": (
                self.relationship_context_agent_implemented
            ),
            "offline_ghl_adapter_used": self.offline_ghl_adapter_used,
            "synthetic_crm_context_only": self.synthetic_crm_context_only,
            "relationship_context_output_valid": self.relationship_context_output_valid,
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
        }


class GoogleAdkRuntime:
    """Google ADK package-backed sequential runtime for Unit 2.

    Fail-closed: ``start()`` raises ``GoogleAdkPackageUnavailable`` when the
    google-adk package cannot be bound. No local orchestration fallback.
    """

    agent_graph = UNIT2_AGENT_GRAPH

    def __init__(
        self,
        *,
        meeting_agent: Optional[MeetingContextAgent] = None,
        relationship_agent: Optional[RelationshipContextAgent] = None,
    ) -> None:
        self.meeting_agent = meeting_agent or MeetingContextAgent.for_fixture_mode()
        self.relationship_agent = relationship_agent or RelationshipContextAgent()
        self._started = False
        self._backend = ADK_STATUS_NOT_STARTED
        self._google_adk_bound = False
        self._google_adk_bind_detail: Optional[str] = None
        self._primitive_used = False
        self._runner: Any = None
        self._session_service: Any = None
        self._prim: Optional[Dict[str, Any]] = None

    @property
    def started(self) -> bool:
        return self._started

    @property
    def backend(self) -> str:
        return self._backend

    @property
    def google_adk_package_bound(self) -> bool:
        return self._google_adk_bound

    def start(self) -> "GoogleAdkRuntime":
        """Bind the google-adk package and construct ADK runtime primitives."""
        prim = _import_google_adk_primitives()
        root_agent = _build_adk_agents(
            prim,
            meeting_agent=self.meeting_agent,
            relationship_agent=self.relationship_agent,
        )
        session_service = prim["InMemorySessionService"]()
        runner = prim["Runner"](
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        # Binding is only true once supported ADK primitives are constructed.
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

    def ensure_started(self) -> None:
        if not self._started:
            self.start()

    async def _execute(
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
            "stop_before": "follow_up_planning_agent",
            "follow_up_planning_agent_invoked": False,
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
                    text="run unit2 meeting_context -> relationship_context"
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

    def run_unit2(
        self,
        *,
        meeting_request: ProviderRequest,
        run_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
    ) -> RuntimeRunResult:
        """Execute the Unit 2 pipeline through the Google ADK Runner and stop."""
        self.ensure_started()
        session, events, runner_errors = asyncio.run(
            self._execute(
                meeting_request=meeting_request,
                run_id=run_id,
                scenario_id=scenario_id,
            )
        )

        state = dict(session.state) if session is not None else {}
        meeting_context = state.get("meeting_context")
        relationship_context = state.get("relationship_context")

        # ADK primitive use is only true when events authored by both ADK
        # sub-agents were actually consumed from the Runner event stream.
        authors = [getattr(e, "author", None) for e in events]
        expected_authors = [a.agent_id for a in UNIT2_AGENT_GRAPH]
        primitive_used = all(a in authors for a in expected_authors)
        self._primitive_used = self._primitive_used or primitive_used

        # Proof-level session record derived from actual ADK session/events.
        record = RuntimeSession(
            session_id=str(session.id) if session is not None else "unknown",
            run_id=str(state.get("run_id") or run_id or "unknown"),
            backend=self._backend,
            started=True,
            completed=True,
        )
        record.state = {
            k: v for k, v in state.items() if k != "meeting_request"
        }
        for spec in UNIT2_AGENT_GRAPH:
            if spec.agent_id in authors:
                output = state.get(f"{spec.role}")
                status = "ok" if output is not None else "error"
                record.record_invocation(
                    AgentInvocationRecord(
                        agent_id=spec.agent_id,
                        status=status,
                        output_schema=(
                            (output or {}).get("schema") if output else None
                        ),
                        error=(
                            None
                            if output is not None
                            else f"{spec.agent_id} produced no output"
                        ),
                        external_effects=int(
                            (output or {}).get("external_effects", 0)
                        ),
                    )
                )

        errors: List[str] = list(runner_errors)
        state_errors = [str(e) for e in (state.get("errors") or [])]
        errors.extend(state_errors)

        bypass = False
        offline_ghl_used = False
        synthetic_only = True
        relationship_valid = False

        if meeting_context is not None:
            if meeting_context.get("external_effects", 0) != 0:
                errors.append("meeting_context external_effects must be 0")
            if meeting_context.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                bypass = True
                errors.append("meeting_context attempted deterministic policy bypass")
        else:
            errors.append("meeting_context missing")

        if relationship_context is not None:
            offline_ghl_used = True
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
                synthetic_only = False
            if crm.get("mode") != "offline_synthetic":
                synthetic_only = False
                errors.append("crm_source.mode must be offline_synthetic")
            if crm.get("real_customer_data", 0) != 0:
                synthetic_only = False
                errors.append("real_customer_data must be 0")
            relationship_valid = (
                relationship_context.get("schema") == "relationship_context_v1"
            )
        else:
            errors.append("relationship_context missing")

        external_effects = int(record.external_effects)
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
            and relationship_valid
            and external_effects == 0
            and not bypass
        )

        return RuntimeRunResult(
            ok=ok,
            session=record,
            meeting_context=meeting_context,
            relationship_context=relationship_context,
            errors=errors,
            google_adk_package_bound=markers["google_adk_package_bound"],
            google_adk_runtime_started=markers["google_adk_runtime_started"],
            adk_integration_status=markers["adk_integration_status"],
            adk_runtime_primitive_used=markers["adk_runtime_primitive_used"],
            local_adk_fallback_used=markers["local_adk_fallback_used"],
            meeting_context_agent_reused=True,
            relationship_context_agent_implemented=True,
            offline_ghl_adapter_used=offline_ghl_used,
            synthetic_crm_context_only=synthetic_only,
            relationship_context_output_valid=relationship_valid and ok,
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
        )

    def telemetry(self) -> Dict[str, Any]:
        markers = derive_runtime_markers(
            google_adk_package_bound=self._google_adk_bound,
            runtime_backend=self._backend,
            runtime_started=self._started,
            adk_runtime_primitive_used=self._primitive_used,
        )
        return {
            **markers,
            "runtime_started": self._started,
            "google_adk_bind_detail": self._google_adk_bind_detail,
            "agent_graph": [
                {
                    "agent_id": a.agent_id,
                    "role": a.role,
                    "description": a.description,
                }
                for a in self.agent_graph
            ],
            "stop_before": "follow_up_planning_agent",
            "gemini_provider_started": GEMINI_PROVIDER_STARTED,
            "gemini_adk_started": GEMINI_ADK_STARTED,
        }


def adk_runtime_declaration(runtime: "GoogleAdkRuntime") -> Dict[str, Any]:
    """Sanitized runtime declaration derived from a started runtime."""
    markers = derive_runtime_markers(
        google_adk_package_bound=runtime.google_adk_package_bound,
        runtime_backend=runtime.backend,
        runtime_started=runtime.started,
        adk_runtime_primitive_used=runtime._primitive_used,
    )
    return {
        "framework": "google_adk_runtime",
        "integration_status": markers["adk_integration_status"],
        "google_adk_package_bound": markers["google_adk_package_bound"],
        "google_adk_runtime_started": markers["google_adk_runtime_started"],
        "runtime_backend": markers["runtime_backend"],
        "adk_runtime_primitive_used": markers["adk_runtime_primitive_used"],
        "local_adk_fallback_used": markers["local_adk_fallback_used"],
        "unit": "phase3_unit2_relationship_context",
        "agents": [a.agent_id for a in UNIT2_AGENT_GRAPH],
        "stop_before": "follow_up_planning_agent",
        "tools_crm": ["phase2b_offline_ghl_read_adapter"],
        "side_effects": [],
        "deterministic_policy_bypass": False,
        "external_effects": 0,
    }
