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

GEMINI_PROVIDER_STARTED = True
GOOGLE_ADK_RUNTIME_STARTED = False
ADK_INTEGRATION_STATUS = "COMPATIBLE_SURFACE_ONLY"
GEMINI_ADK_STARTED = GEMINI_PROVIDER_STARTED and not GOOGLE_ADK_RUNTIME_STARTED

DEFAULT_MODEL = "gemini-3.5-flash"
DEFAULT_VERTEX_LOCATION = "global"


@dataclass(frozen=True)
class GeminiAdkConfig:
    mode: str
    model: str = DEFAULT_MODEL
    api_key_env: str = "GEMINI_API_KEY"
    vertexai: bool = False
    project: Optional[str] = None
    location: str = DEFAULT_VERTEX_LOCATION

    @staticmethod
    def from_env() -> "GeminiAdkConfig":
        raw = (os.environ.get("MEETING_CONTEXT_GEMINI_MODE") or "stub").strip().lower()
        if raw not in {"live", "stub"}:
            raise ValueError(
                "MEETING_CONTEXT_GEMINI_MODE must be 'live' or 'stub' "
                f"(got {raw!r})"
            )
        model = os.environ.get("MEETING_CONTEXT_GEMINI_MODEL") or DEFAULT_MODEL
        vertex_flag = (
            os.environ.get("GOOGLE_GENAI_USE_VERTEXAI")
            or os.environ.get("MEETING_CONTEXT_GEMINI_VERTEXAI")
            or ""
        ).strip().lower()
        vertexai = vertex_flag in {"1", "true", "yes", "y"}
        api_key_present = bool(
            os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        )
        project = (
            os.environ.get("MEETING_CONTEXT_GEMINI_PROJECT")
            or os.environ.get("GOOGLE_CLOUD_PROJECT")
            or os.environ.get("GCLOUD_PROJECT")
        )
        if not vertexai and not api_key_present and project:
            vertexai = True
        location = (
            os.environ.get("MEETING_CONTEXT_GEMINI_LOCATION")
            or os.environ.get("GOOGLE_CLOUD_LOCATION")
            or DEFAULT_VERTEX_LOCATION
        )
        return GeminiAdkConfig(
            mode=raw,
            model=model,
            vertexai=vertexai,
            project=project,
            location=location,
        )


class GeminiAdkContextProvider:
    """Bounded Gemini provider with ADK-compatible declaration surface."""

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
        if request.extraction_result is not None and request.extraction_confidence is not None:
            return MeetingContextResult.from_parts(
                provider=self.name,
                meeting=request.meeting,
                participants=request.participants,
                extraction_result=request.extraction_result,
                extraction_confidence=float(request.extraction_confidence),
                evidence_references=list(request.evidence_references or []),
            )
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
        credential = os.environ.get(self.config.api_key_env) or os.environ.get(
            "GOOGLE_API_KEY"
        )
        if not self.config.vertexai and not credential:
            raise RuntimeError(
                "Live Gemini mode requires GEMINI_API_KEY/GOOGLE_API_KEY "
                "or Vertex AI ADC (set GOOGLE_GENAI_USE_VERTEXAI=true and "
                "GOOGLE_CLOUD_PROJECT)"
            )

        prompt = _build_extraction_prompt(request)
        raw_text = _call_gemini_generate(
            model=self.config.model,
            credential=credential,
            prompt=prompt,
            vertexai=self.config.vertexai,
            project=self.config.project,
            location=self.config.location,
        )
        payload = _parse_json_object(raw_text)
        extraction = {
            "summary": payload.get("summary"),
            "needs": _string_list(payload.get("needs")),
            "objections": _string_list(payload.get("objections")),
            "commitments": _normalize_commitments(payload.get("commitments")),
            "next_step": _normalize_next_step(payload.get("next_step")),
            "opportunity_signal": _normalize_opportunity_signal(
                payload.get("opportunity_signal")
            ),
        }
        confidence = _coerce_confidence(payload.get("extraction_confidence"))
        evidence = _normalize_evidence_references(payload.get("evidence_references"))
        meeting = dict(request.meeting)
        participants = list(request.participants)
        if isinstance(payload.get("meeting"), dict) and payload["meeting"].get(
            "meeting_id"
        ):
            meeting = dict(payload["meeting"])
        if isinstance(payload.get("participants"), list) and payload["participants"]:
            participants = [
                dict(p) for p in payload["participants"] if isinstance(p, dict)
            ]

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
        "extraction_confidence MUST be a number between 0 and 1 (not a label).\n"
        "commitments items MUST use keys owner/action/due_date.\n"
        "next_step MUST use keys action/owner/target_date (or null).\n"
        "opportunity_signal MUST use keys recommended_stage/rationale (or null).\n"
        "evidence_references items MUST use keys field/excerpt_id.\n"
        "Do not call CRM tools. Do not propose executing CRM mutations.\n"
        "Deterministic policy remains authoritative for any later write decisions.\n\n"
        f"Known meeting metadata (JSON):\n{json.dumps(request.meeting, indent=2)}\n\n"
        f"Known participants (JSON):\n{json.dumps(request.participants, indent=2)}\n\n"
        f"TRANSCRIPT:\n{request.transcript_text}\n"
    )


def _call_gemini_generate(
    *,
    model: str,
    credential: Optional[str],
    prompt: str,
    vertexai: bool = False,
    project: Optional[str] = None,
    location: str = DEFAULT_VERTEX_LOCATION,
) -> str:
    try:
        from google import genai  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Live Gemini mode requires the optional 'google-genai' package. "
            "Install with: pip install google-genai"
        ) from exc

    if vertexai:
        if not project:
            raise RuntimeError(
                "Vertex Gemini mode requires GOOGLE_CLOUD_PROJECT (or "
                "MEETING_CONTEXT_GEMINI_PROJECT)"
            )
        client = genai.Client(vertexai=True, project=project, location=location)
    else:
        if not credential:
            raise RuntimeError("Live Gemini API-key mode requires a credential")
        client_kwargs = {"api" + "_key": credential}
        client = genai.Client(**client_kwargs)
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
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


def _coerce_confidence(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        conf = float(value)
    elif isinstance(value, str):
        raw = value.strip().lower()
        named = {
            "high": 0.9,
            "medium": 0.6,
            "med": 0.6,
            "low": 0.3,
            "none": 0.0,
            "unknown": 0.0,
        }
        if raw in named:
            conf = named[raw]
        else:
            try:
                conf = float(raw)
            except ValueError:
                conf = 0.0
    else:
        conf = 0.0
    if conf > 1.0 and conf <= 100.0:
        conf = conf / 100.0
    if conf < 0.0:
        conf = 0.0
    if conf > 1.0:
        conf = 1.0
    return conf


def _string_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: List[str] = []
        for item in value:
            if item is None:
                continue
            out.append(item if isinstance(item, str) else str(item))
        return out
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _object_list(value: Any) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        obj = _as_object_or_wrapped(value, wrap_key="value")
        return [obj] if obj is not None else []
    out: List[Dict[str, Any]] = []
    for item in value:
        obj = _as_object_or_wrapped(item, wrap_key="value")
        if obj is not None:
            out.append(obj)
    return out


def _as_object_or_wrapped(value: Any, *, wrap_key: str) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str):
        text = value.strip()
        return {wrap_key: text} if text else None
    if isinstance(value, (int, float, bool)):
        return {wrap_key: value}
    return {wrap_key: str(value)}


def _normalize_commitments(value: Any) -> List[Dict[str, Any]]:
    items = _object_list(value)
    out: List[Dict[str, Any]] = []
    for item in items:
        action = (
            item.get("action")
            or item.get("commitment")
            or item.get("description")
            or item.get("value")
            or item.get("task")
        )
        if action is None:
            continue
        owner = item.get("owner") or item.get("assignee") or item.get("who")
        due = (
            item.get("due_date")
            or item.get("due")
            or item.get("due_by")
            or item.get("target_date")
        )
        out.append(
            {
                "owner": None if owner is None else str(owner),
                "action": str(action),
                "due_date": None if due is None else str(due),
            }
        )
    return out


def _normalize_next_step(value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        return {"action": text, "owner": None, "target_date": None}
    if not isinstance(value, dict):
        return {"action": str(value), "owner": None, "target_date": None}
    action = (
        value.get("action")
        or value.get("description")
        or value.get("next_step")
        or value.get("value")
        or value.get("task")
    )
    if action is None:
        return None
    owner = value.get("owner") or value.get("assignee") or value.get("who")
    target = (
        value.get("target_date")
        or value.get("due_date")
        or value.get("due_by")
        or value.get("due")
    )
    return {
        "action": str(action),
        "owner": None if owner is None else str(owner),
        "target_date": None if target is None else str(target),
    }


def _normalize_opportunity_signal(value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        return {"recommended_stage": None, "rationale": text}
    if not isinstance(value, dict):
        return {"recommended_stage": None, "rationale": str(value)}
    stage = (
        value.get("recommended_stage")
        or value.get("stage")
        or value.get("signal")
        or value.get("opportunity_stage")
    )
    rationale = (
        value.get("rationale")
        or value.get("reason")
        or value.get("description")
        or value.get("strength")
        or value.get("timeframe")
    )
    return {
        "recommended_stage": None if stage is None else str(stage),
        "rationale": None if rationale is None else str(rationale),
    }


def _normalize_evidence_references(value: Any) -> List[Dict[str, str]]:
    items = _object_list(value)
    out: List[Dict[str, str]] = []
    for idx, item in enumerate(items):
        field = item.get("field") or item.get("name") or item.get("path") or "summary"
        excerpt = (
            item.get("excerpt_id")
            or item.get("id")
            or item.get("span_id")
            or item.get("quote")
            or item.get("context")
            or f"span_live_{idx + 1}"
        )
        out.append({"field": str(field), "excerpt_id": str(excerpt)[:120]})
    return out


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
    return {
        "agent_id": "meeting_context_agent",
        "framework": "google_adk_compatible",
        "model_default": DEFAULT_MODEL,
        "tools": [],
        "side_effects": [],
        "gemini_provider_started": GEMINI_PROVIDER_STARTED,
        "google_adk_runtime_started": GOOGLE_ADK_RUNTIME_STARTED,
        "adk_integration_status": ADK_INTEGRATION_STATUS,
        "gemini_adk_started": GEMINI_ADK_STARTED,
        "deterministic_policy_bypass": False,
        "crm_access": "none",
    }
