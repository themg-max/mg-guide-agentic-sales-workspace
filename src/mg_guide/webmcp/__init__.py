"""WebMCP Challenge competition adapter for MG Guide.

This package is additive: it does not modify meeting_follow_up_v1 workflow
logic, the judge_surface add-on auth contract, or any CRM/agent runtime code.
It exposes a narrow, public, synthetic-only HTTP boundary consumed by the
browser-native WebMCP frontend under ``webmcp/static``.
"""

from __future__ import annotations

__all__ = ["WebMCPSurfaceApp", "WEBMCP_SCENARIOS"]

from .app import WebMCPSurfaceApp
from .scenarios import WEBMCP_SCENARIOS
