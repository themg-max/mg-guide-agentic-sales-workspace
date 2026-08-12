"""Deterministic fixture provider for offline CI (no live model calls)."""

from __future__ import annotations

from ..models import MeetingContextResult
from .base import ProviderRequest


class FixtureContextProvider:
    """Replay structured context from synthetic fixture sidecars.

    This is the default CI path. It does not call Gemini and does not touch CRM.
    """

    name = "fixture"

    def extract(self, request: ProviderRequest) -> MeetingContextResult:
        if request.extraction_result is None:
            raise ValueError(
                "FixtureContextProvider requires extraction_result on the request"
            )
        if request.extraction_confidence is None:
            raise ValueError(
                "FixtureContextProvider requires extraction_confidence on the request"
            )
        if not request.transcript_text or not request.transcript_text.strip():
            raise ValueError("transcript_text must be non-empty synthetic input")

        return MeetingContextResult.from_parts(
            provider=self.name,
            meeting=request.meeting,
            participants=request.participants,
            extraction_result=request.extraction_result,
            extraction_confidence=float(request.extraction_confidence),
            evidence_references=list(request.evidence_references or []),
        )
