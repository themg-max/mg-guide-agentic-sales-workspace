"""Meeting Context Agent entrypoint."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .models import MeetingContextResult
from .providers.base import ContextProvider, ProviderRequest
from .providers.fixture_provider import FixtureContextProvider
from .providers.gemini_adk_provider import (
    GEMINI_ADK_STARTED,
    GeminiAdkConfig,
    GeminiAdkContextProvider,
    adk_agent_declaration,
)
from .schema import validate_meeting_context


class MeetingContextAgent:
    """Produces schema-valid structured meeting context from a transcript.

    Does not call GHL, does not write CRM, does not bypass deterministic policy.
    """

    agent_id = "meeting_context_agent"

    def __init__(self, provider: Optional[ContextProvider] = None) -> None:
        self.provider = provider or FixtureContextProvider()

    @staticmethod
    def for_fixture_mode() -> "MeetingContextAgent":
        return MeetingContextAgent(provider=FixtureContextProvider())

    @staticmethod
    def for_gemini_adk(mode: str = "stub") -> "MeetingContextAgent":
        return MeetingContextAgent(
            provider=GeminiAdkContextProvider(GeminiAdkConfig(mode=mode))
        )

    def run(self, request: ProviderRequest) -> MeetingContextResult:
        result = self.provider.extract(request)
        payload = result.to_dict()
        ok, errors = validate_meeting_context(payload)
        if not ok:
            raise ValueError(
                "Meeting context failed schema validation: " + "; ".join(errors)
            )
        if payload["external_effects"] != 0:
            raise ValueError("Meeting Context Agent must set external_effects=0")
        if payload["policy_authority"]["deterministic_policy_bypass"] is not False:
            raise ValueError("Deterministic policy bypass is forbidden")
        return result

    def telemetry(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "provider": getattr(self.provider, "name", type(self.provider).__name__),
            "gemini_adk_started": GEMINI_ADK_STARTED,
            "adk_declaration": adk_agent_declaration(),
            "external_effects": 0,
            "deterministic_policy_bypass": False,
        }
