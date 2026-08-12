"""Google ADK runtime orchestration for meeting_follow_up_v1 Phase 3 Unit 2.

This module implements actual multi-agent runtime orchestration (not a
declaration-only surface). Default CI uses a local ADK-compatible backend that
sequences agents in-process with zero external effects.

When the optional ``google-adk`` package is installed, the runtime records a
package binding. Live CRM/GHL/Firestore/deployment remain forbidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context.agent import RelationshipContextAgent
from agents.relationship_context.models import RelationshipRequest

from .markers import (
    ADK_INTEGRATION_STATUS,
    GEMINI_ADK_STARTED,
    GEMINI_PROVIDER_STARTED,
    GOOGLE_ADK_RUNTIME_STARTED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    RUNTIME_BACKEND_LOCAL,
    runtime_markers,
)
from .session import AgentInvocationRecord, RuntimeSession


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


@dataclass
class RuntimeRunResult:
    ok: bool
    session: RuntimeSession
    meeting_context: Optional[Dict[str, Any]]
    relationship_context: Optional[Dict[str, Any]]
    errors: List[str]
    google_adk_runtime_started: bool
    adk_integration_status: str
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
            "google_adk_runtime_started": self.google_adk_runtime_started,
            "adk_integration_status": self.adk_integration_status,
            "meeting_context_agent_reused": self.meeting_context_agent_reused,
            "relationship_context_agent_implemented": (
                self.relationship_context_agent_implemented
            ),
            "offline_ghl_adapter_used": self.offline_ghl_adapter_used,
            "synthetic_crm_context_only": self.synthetic_crm_context_only,
            "relationship_context_output_valid": self.relationship_context_output_valid,
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
            "markers": runtime_markers(),
        }


class GoogleAdkRuntime:
    """Sequential multi-agent ADK runtime for Unit 2.

    Architecture (stop before Follow-Up Planning Agent):

        synthetic transcript
          -> Meeting Context Agent (reused from Unit 1)
          -> Google ADK runtime orchestration
          -> Relationship Context Agent
          -> Phase 2B offline GHL adapter (synthetic CRM only)
          -> relationship_context_v1
          -> STOP
    """

    agent_graph = UNIT2_AGENT_GRAPH

    def __init__(
        self,
        *,
        meeting_agent: Optional[MeetingContextAgent] = None,
        relationship_agent: Optional[RelationshipContextAgent] = None,
        prefer_google_adk_package: bool = True,
    ) -> None:
        self.meeting_agent = meeting_agent or MeetingContextAgent.for_fixture_mode()
        self.relationship_agent = relationship_agent or RelationshipContextAgent()
        self.prefer_google_adk_package = prefer_google_adk_package
        self._started = False
        self._backend = RUNTIME_BACKEND_LOCAL
        self._google_adk_bound = False
        self._google_adk_bind_detail: Optional[str] = None

    @property
    def started(self) -> bool:
        return self._started

    @property
    def backend(self) -> str:
        return self._backend

    def start(self) -> "GoogleAdkRuntime":
        """Start the runtime and resolve the ADK backend binding."""
        self._backend, self._google_adk_bound, self._google_adk_bind_detail = (
            self._resolve_backend()
        )
        self._started = True
        return self

    def ensure_started(self) -> None:
        if not self._started:
            self.start()

    def _resolve_backend(self) -> tuple[str, bool, Optional[str]]:
        if not self.prefer_google_adk_package:
            return RUNTIME_BACKEND_LOCAL, False, "prefer_google_adk_package=false"
        try:
            import google.adk  # type: ignore  # noqa: F401

            version = getattr(google.adk, "__version__", "unknown")
            return (
                RUNTIME_BACKEND_GOOGLE_ADK,
                True,
                f"google.adk import ok version={version}",
            )
        except Exception as exc:  # pragma: no cover - optional dependency path
            return (
                RUNTIME_BACKEND_LOCAL,
                False,
                f"google.adk unavailable ({type(exc).__name__}); using local runtime",
            )

    def run_unit2(
        self,
        *,
        meeting_request: ProviderRequest,
        run_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
    ) -> RuntimeRunResult:
        """Execute Unit 2 pipeline through the ADK runtime and stop."""
        self.ensure_started()
        session = RuntimeSession.create(run_id=run_id)
        session.backend = self._backend
        session.started = True
        if scenario_id:
            session.put("scenario_id", scenario_id)

        errors: List[str] = []
        meeting_context: Optional[Dict[str, Any]] = None
        relationship_context: Optional[Dict[str, Any]] = None
        offline_ghl_used = False
        synthetic_only = True
        relationship_valid = False
        bypass = False

        # --- Agent 1: Meeting Context (reused) ---
        try:
            meeting_result = self.meeting_agent.run(meeting_request)
            meeting_context = meeting_result.to_dict()
            session.put("meeting_context", meeting_context)
            session.record_invocation(
                AgentInvocationRecord(
                    agent_id="meeting_context_agent",
                    status="ok",
                    output_schema=meeting_context.get("schema"),
                    external_effects=int(meeting_context.get("external_effects", 0)),
                )
            )
            if meeting_context.get("external_effects", 0) != 0:
                errors.append("meeting_context external_effects must be 0")
            if meeting_context.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                bypass = True
                errors.append("meeting_context attempted deterministic policy bypass")
        except Exception as exc:
            errors.append(f"meeting_context_agent: {type(exc).__name__}: {exc}")
            session.record_invocation(
                AgentInvocationRecord(
                    agent_id="meeting_context_agent",
                    status="error",
                    error=f"{type(exc).__name__}: {exc}",
                    external_effects=0,
                )
            )

        # --- Agent 2: Relationship Context ---
        if meeting_context is not None and not errors:
            try:
                rel_request = RelationshipRequest(
                    meeting_context=meeting_context,
                    run_id=session.run_id,
                    scenario_id=scenario_id,
                )
                rel_result = self.relationship_agent.run(rel_request)
                relationship_context = rel_result.to_dict()
                session.put("relationship_context", relationship_context)
                offline_ghl_used = True
                session.record_invocation(
                    AgentInvocationRecord(
                        agent_id="relationship_context_agent",
                        status="ok",
                        output_schema=relationship_context.get("schema"),
                        external_effects=int(
                            relationship_context.get("external_effects", 0)
                        ),
                    )
                )
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
                relationship_valid = relationship_context.get("schema") == (
                    "relationship_context_v1"
                )
            except Exception as exc:
                errors.append(
                    f"relationship_context_agent: {type(exc).__name__}: {exc}"
                )
                session.record_invocation(
                    AgentInvocationRecord(
                        agent_id="relationship_context_agent",
                        status="error",
                        error=f"{type(exc).__name__}: {exc}",
                        external_effects=0,
                    )
                )

        # Explicit stop gate: Follow-Up Planning Agent is NOT invoked in Unit 2.
        session.put("stop_before", "follow_up_planning_agent")
        session.put("follow_up_planning_agent_invoked", False)
        session.completed = True

        external_effects = int(session.external_effects)
        ok = (
            not errors
            and meeting_context is not None
            and relationship_context is not None
            and relationship_valid
            and external_effects == 0
            and not bypass
        )

        return RuntimeRunResult(
            ok=ok,
            session=session,
            meeting_context=meeting_context,
            relationship_context=relationship_context,
            errors=errors,
            google_adk_runtime_started=GOOGLE_ADK_RUNTIME_STARTED and self._started,
            adk_integration_status=ADK_INTEGRATION_STATUS,
            meeting_context_agent_reused=True,
            relationship_context_agent_implemented=True,
            offline_ghl_adapter_used=offline_ghl_used,
            synthetic_crm_context_only=synthetic_only,
            relationship_context_output_valid=relationship_valid and ok,
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
        )

    def telemetry(self) -> Dict[str, Any]:
        self.ensure_started()
        markers = runtime_markers()
        return {
            **markers,
            "runtime_started": self._started,
            "runtime_backend": self._backend,
            "google_adk_package_bound": self._google_adk_bound,
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


def adk_runtime_declaration() -> Dict[str, Any]:
    """Sanitized runtime declaration for proof/telemetry."""
    return {
        "framework": "google_adk_runtime",
        "integration_status": ADK_INTEGRATION_STATUS,
        "google_adk_runtime_started": GOOGLE_ADK_RUNTIME_STARTED,
        "unit": "phase3_unit2_relationship_context",
        "agents": [a.agent_id for a in UNIT2_AGENT_GRAPH],
        "stop_before": "follow_up_planning_agent",
        "tools_crm": ["phase2b_offline_ghl_read_adapter"],
        "side_effects": [],
        "deterministic_policy_bypass": False,
        "external_effects": 0,
    }
