"""Gemini / Google ADK provider for Meeting Context Agent.

Live model calls are optional and disabled by default. CI uses fixture or
`gemini_adk_stub` mode so tests pass without API keys or network.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..models import MeetingContextResult
from .base import ProviderRequest

# Durable marker that the Gemini/ADK implementation surface has been started.
GEMINI_ADK_STARTED = True

DEFAULT_MODEL = "gemini-2.0-flash"


@dataclass(frozen=True)
class GeminiAdkConfig:
    mode: str  # "live" | "stub"
    model: str = DEFAULT_MODEL
    api_key_env: str = "GEMINI_API_KEY"

    @staticmethod
    def from_env() -> "GeminiAdkConfig":
        raw = (os.environ.get("MEETING_CONTEXT_GEMINI_MODE") or "stub").strip().lower()
        if raw not in {"live", "stub"}:
            raise ValueError(
                "MEETING_CONTEXT_GEMINI_MODE must be 'live' or 'stub' "
                f"(got {raw!r})"
            )
        model = os.environ.get("MEETING_CONTEXT_GEMINI_MODEL") or DEFAULT_MODEL
        return GeminiAdkConfig(mode=raw, model=model)


class GeminiAdkContextProvider:
    """Bounded Gemini/ADK extraction provider.

    - mode=stub: no network; builds structured context from request sidecar fields
      while exercising the ADK provider surface (CI-safe).
    - mode=live: attempts Google GenAI / ADK call when credentials are present.
      Live mode never performs CRM/GHL/Firestore side effects.
    """

    name = "gemini_adk"

    def __init__(self, config: Optional[GeminiAdkConfig] = None) -> None:
        self.config = config or GeminiAdkConfig.from_env()
        self.name = (
            "gemini_adk_stub" if self.config.mode == "stub" else "gemini_adk"
        )

    def extract(self, request: ProviderRequest) -> MeetingContextResult:
        if not request.transcript_text or not request.transcript_text.strip():
            raise ValueError("transcript_text must be non-empty synthetic input")

        if self.config.mode == "stub":
            return self._extract_stub(request)
        return self._extract_live(request)

    def _extract_stub(self, request: ProviderRequest) -> MeetingContextResult:
        # Prefer explicit sidecar extraction when present (fixture harness).
        if request.extraction_result is not None and request.extraction_confidence is not None:
            return MeetingContextResult.from_parts(
                provider=self.name,
                meeting=request.meeting,
                participants=request.participants,
                extraction_result=request.extraction_result,
                extraction_confidence=float(request.extraction_confidence),
                evidence_references=list(request.evidence_references or []),
            )
        # Minimal heuristic fallback for stub without sidecar (still offline).
        summary = _first_nonempty_line_after_marker(request.transcript_text)
        extraction = {
            "summary": summary or "Synthetic meeting context (stub provider).",
            "needs": [],
            "objections": [],
            "commitments": [],
            "next_step": None,
            "opportunity_signal": {
                "recommended_stage": None,
                "rationale": "Stub provider did not infer a stage change.",
            },
        }
        return MeetingContextResult.from_parts(
            provider=self.name,
            meeting=request.meeting,
            participants=request.participants,
            extraction_result=extraction,
            extraction_confidence=0.5,
            evidence_references=[],
        )

    def _extract_live(self, request: ProviderRequest) -> MeetingContextResult:
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Live Gemini mode requires {self.config.api_key_env} to be set"
            )

        prompt = _build_extraction_prompt(request)
        raw_text = _call_gemini_generate(
            model=self.config.model,
            api_key=api_key,
            prompt=prompt,
        )
        payload = _parse_json_object(raw_text)
        extraction = {
            "summary": payload.get("summary"),
            "needs": list(payload.get("needs") or []),
            "objections": list(payload.get("objections") or []),
            "commitments": list(payload.get("commitments") or []),
            "next_step": payload.get("next_step"),
            "opportunity_signal": payload.get("opportunity_signal"),
        }
        confidence = float(payload.get("extraction_confidence") or 0.0)
        evidence = list(payload.get("evidence_references") or [])
        meeting = dict(request.meeting)
        participants = list(request.participants)
        # Prefer model-supplied meeting/participants only when fully shaped.
        if isinstance(payload.get("meeting"), dict) and payload["meeting"].get(
            "meeting_id"
        ):
            meeting = dict(payload["meeting"])
        if isinstance(payload.get("participants"), list) and payload["participants"]:
            participants = [dict(p) for p in payload["participants"]]

        return MeetingContextResult.from_parts(
            provider=self.name,
            meeting=meeting,
            participants=participants,
            extraction_result=extraction,
            extraction_confidence=confidence,
            evidence_references=evidence,
        )


def _build_extraction_prompt(request: ProviderRequest) -> str:
    return (
        "You are the Meeting Context Agent for workflow meeting_follow_up_v1.\n"
        "Extract structured meeting context from the synthetic transcript.\n"
        "Return ONLY a JSON object with keys: meeting, participants, summary, needs,\n"
        "objections, commitments, next_step, opportunity_signal, extraction_confidence,\n"
        "evidence_references.\n"
        "Do not call CRM tools. Do not propose executing CRM mutations.\n"
        "Deterministic policy remains authoritative for any later write decisions.\n\n"
        f"Known meeting metadata (JSON):\n{json.dumps(request.meeting, indent=2)}\n\n"
        f"Known participants (JSON):\n{json.dumps(request.participants, indent=2)}\n\n"
        f"TRANSCRIPT:\n{request.transcript_text}\n"
    )


def _call_gemini_generate(*, model: str, api_key: str, prompt: str) -> str:
    """Call Gemini via google-genai if installed; else raise a clear error.

    This function performs model egress only. No CRM/GHL/Firestore calls.
    """
    try:
        from google import genai  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError(
            "Live Gemini mode requires the optional 'google-genai' package. "
            "Install with: pip install google-genai"
        ) from exc

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        # Fallback for response shapes without .text
        text = str(response)
    return text


def _parse_json_object(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("Gemini response did not contain a JSON object")
    data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("Gemini JSON payload must be an object")
    return data


def _first_nonempty_line_after_marker(transcript: str) -> Optional[str]:
    lines = transcript.splitlines()
    seen_marker = False
    for line in lines:
        if "--- TRANSCRIPT ---" in line:
            seen_marker = True
            continue
        if not seen_marker:
            continue
        stripped = line.strip()
        if stripped and not stripped.startswith("---"):
            return stripped[:240]
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:240]
    return None


def adk_agent_declaration() -> Dict[str, Any]:
    """Sanitized ADK agent declaration for proof/telemetry (no secrets)."""
    return {
        "agent_id": "meeting_context_agent",
        "framework": "google_adk_compatible",
        "model_default": DEFAULT_MODEL,
        "tools": [],
        "side_effects": [],
        "gemini_adk_started": GEMINI_ADK_STARTED,
        "deterministic_policy_bypass": False,
        "crm_access": "none",
    }
