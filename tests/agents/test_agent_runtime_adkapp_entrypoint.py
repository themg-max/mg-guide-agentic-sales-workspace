"""Offline Agent Runtime AdkApp serving-object contract."""

from __future__ import annotations

import sys
from pathlib import Path

DEPLOYMENT_ROOT = (
    Path(__file__).resolve().parents[2] / "deployment" / "agent-runtime"
)


def test_agent_runtime_app_wraps_existing_sequential_graph() -> None:
    if str(DEPLOYMENT_ROOT) not in sys.path:
        sys.path.insert(0, str(DEPLOYMENT_ROOT))

    import app.agent as entrypoint

    obj = entrypoint.agent_runtime_app
    assert type(obj).__name__ == "AdkApp"
    assert obj.__class__.__module__.startswith("agentplatform.agent_engines")
    assert hasattr(obj, "register_operations")
    assert hasattr(obj, "async_stream_query")

    operations = obj.register_operations()
    assert operations
    flat = {name for names in operations.values() for name in names}
    assert "async_stream_query" in flat

    assert entrypoint.root_agent.name == "unit3_meeting_to_follow_up_packet"
    assert [agent.name for agent in entrypoint.root_agent.sub_agents] == [
        "meeting_context_agent",
        "relationship_context_agent",
        "follow_up_planning_agent",
    ]
    assert type(entrypoint.root_agent).__name__ == "SequentialAgent"
    assert getattr(obj, "_tmpl_attrs", {}).get("runner") is None
