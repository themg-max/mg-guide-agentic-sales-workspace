"""Offline Agent Runtime AdkApp serving-object contract."""

from __future__ import annotations

import sys
from pathlib import Path

from vertexai import init

DEPLOYMENT_ROOT = (
    Path(__file__).resolve().parents[2] / "deployment" / "agent-runtime"
)


def test_agent_runtime_app_wraps_existing_sequential_graph() -> None:
    # AdkApp reads Vertex global project configuration during construction.
    # This synthetic test setting performs no credential lookup or network call.
    init(project="mg-guide-agent-runtime-test", location="us-east1")

    if str(DEPLOYMENT_ROOT) not in sys.path:
        sys.path.insert(0, str(DEPLOYMENT_ROOT))

    import app.agent as entrypoint

    agent_runtime_app = entrypoint.agent_runtime_app
    assert type(agent_runtime_app).__name__ == "AdkApp"
    assert agent_runtime_app.__class__.__module__.startswith("vertexai.agent_engines")
    assert hasattr(agent_runtime_app, "register_operations")
    assert hasattr(agent_runtime_app, "async_stream_query")

    ops = agent_runtime_app.register_operations()
    assert ops
    flat = {name for names in ops.values() for name in names}
    assert "async_stream_query" in flat

    assert entrypoint.root_agent.name == "unit3_meeting_to_follow_up_packet"
    assert [agent.name for agent in entrypoint.root_agent.sub_agents] == [
        "meeting_context_agent",
        "relationship_context_agent",
        "follow_up_planning_agent",
    ]
    assert type(entrypoint.root_agent).__name__ == "SequentialAgent"
    assert getattr(agent_runtime_app, "_tmpl_attrs", {}).get("runner") is None
