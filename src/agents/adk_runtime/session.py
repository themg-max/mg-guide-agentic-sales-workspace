"""ADK runtime session / invocation state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class AgentInvocationRecord:
    agent_id: str
    status: str
    output_schema: Optional[str] = None
    error: Optional[str] = None
    external_effects: int = 0


@dataclass
class RuntimeSession:
    """In-memory ADK-compatible session for a single orchestrated run."""

    session_id: str
    run_id: str
    workflow: str = "meeting_follow_up_v1"
    state: Dict[str, Any] = field(default_factory=dict)
    agent_trace: List[AgentInvocationRecord] = field(default_factory=list)
    started: bool = False
    completed: bool = False
    external_effects: int = 0
    backend: str = "local_adk_compatible_runtime"

    @staticmethod
    def create(
        *, run_id: Optional[str] = None, workflow: str = "meeting_follow_up_v1"
    ) -> "RuntimeSession":
        rid = run_id or f"adk_run_{uuid4().hex[:12]}"
        return RuntimeSession(
            session_id=f"adk_session_{uuid4().hex[:12]}",
            run_id=rid,
            workflow=workflow,
        )

    def put(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def record_invocation(self, record: AgentInvocationRecord) -> None:
        self.agent_trace.append(record)
        self.external_effects += int(record.external_effects or 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "run_id": self.run_id,
            "workflow": self.workflow,
            "started": self.started,
            "completed": self.completed,
            "external_effects": self.external_effects,
            "backend": self.backend,
            "agent_trace": [
                {
                    "agent_id": r.agent_id,
                    "status": r.status,
                    "output_schema": r.output_schema,
                    "error": r.error,
                    "external_effects": r.external_effects,
                }
                for r in self.agent_trace
            ],
            "state_keys": sorted(self.state.keys()),
        }
