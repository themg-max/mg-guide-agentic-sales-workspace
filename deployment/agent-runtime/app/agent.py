"""Agent Runtime entrypoint for the MG Guide Unit 3 business graph."""

from __future__ import annotations

import sys
from pathlib import Path

from google.adk.apps import App


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from agents.follow_up_planning import build_unit3_root_agent  # noqa: E402


root_agent = build_unit3_root_agent()
app = App(root_agent=root_agent, name="app")
