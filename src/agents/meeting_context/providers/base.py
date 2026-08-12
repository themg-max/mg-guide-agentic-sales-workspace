"""Provider protocol for Meeting Context Agent."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol

from ..models import MeetingContextResult


@dataclass(frozen=True)
class ProviderRequest:
    fixture_id: str
    transcript_text: str
    transcript_path: Optional[str]
    meeting: Dict[str, Any]
    participants: List[Dict[str, Any]]
    # Optional expected extraction used only by fixture/stub providers.
    extraction_result: Optional[Dict[str, Any]] = None
    extraction_confidence: Optional[float] = None
    evidence_references: Optional[List[Dict[str, str]]] = None


class ContextProvider(Protocol):
    name: str

    def extract(self, request: ProviderRequest) -> MeetingContextResult:
        """Produce structured meeting context with zero external CRM effects."""
