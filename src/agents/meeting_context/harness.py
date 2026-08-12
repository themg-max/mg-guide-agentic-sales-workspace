"""Fixture harness for Meeting Context Agent (synthetic transcripts only)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from .agent import MeetingContextAgent
from .models import MeetingContextResult
from .providers.base import ProviderRequest
from .schema import validate_meeting_context


DEFAULT_FIXTURE_IDS = (
    "transcript-success",
    "transcript-ambiguous-contact",
    "transcript-no-stage-change",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class FixtureCase:
    fixture_id: str
    transcript_path: Path
    sidecar_path: Path
    transcript_text: str
    sidecar: Dict[str, Any]


@dataclass
class HarnessCaseResult:
    fixture_id: str
    ok: bool
    provider: str
    context: Optional[Dict[str, Any]]
    errors: List[str]
    external_effects: int
    deterministic_policy_bypass: bool


@dataclass
class HarnessReport:
    cases: List[HarnessCaseResult]
    gemini_provider_started: bool
    google_adk_runtime_started: bool
    adk_integration_status: str
    gemini_adk_started: bool
    meeting_context_agent_implemented: bool
    synthetic_transcript_input: bool
    structured_context_output_valid: bool
    deterministic_policy_bypass: bool
    external_effects: int

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.cases) and self.structured_context_output_valid

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "gemini_provider_started": self.gemini_provider_started,
            "google_adk_runtime_started": self.google_adk_runtime_started,
            "adk_integration_status": self.adk_integration_status,
            "gemini_adk_started": self.gemini_adk_started,
            "meeting_context_agent_implemented": self.meeting_context_agent_implemented,
            "synthetic_transcript_input": self.synthetic_transcript_input,
            "structured_context_output_valid": self.structured_context_output_valid,
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
            "cases": [
                {
                    "fixture_id": c.fixture_id,
                    "ok": c.ok,
                    "provider": c.provider,
                    "errors": list(c.errors),
                    "external_effects": c.external_effects,
                    "deterministic_policy_bypass": c.deterministic_policy_bypass,
                    "context": c.context,
                }
                for c in self.cases
            ],
        }


class MeetingContextFixtureHarness:
    """Runs Meeting Context Agent against synthetic transcript fixtures."""

    def __init__(
        self,
        *,
        fixtures_dir: Optional[Path] = None,
        agent: Optional[MeetingContextAgent] = None,
        provider_mode: str = "fixture",
    ) -> None:
        self.fixtures_dir = fixtures_dir or (_repo_root() / "fixtures")
        if agent is not None:
            self.agent = agent
        elif provider_mode == "fixture":
            self.agent = MeetingContextAgent.for_fixture_mode()
        elif provider_mode in {"gemini_adk", "gemini_adk_stub", "stub"}:
            mode = "stub" if provider_mode in {"gemini_adk_stub", "stub"} else "live"
            # harness default for gemini_adk is stub unless explicitly live
            if provider_mode == "gemini_adk":
                mode = "stub"
            self.agent = MeetingContextAgent.for_gemini_adk(mode=mode)
        else:
            raise ValueError(f"unknown provider_mode: {provider_mode}")

    def load_case(self, fixture_id: str) -> FixtureCase:
        transcript_path = self.fixtures_dir / f"{fixture_id}.txt"
        sidecar_path = self.fixtures_dir / f"{fixture_id}.expected.json"
        if not transcript_path.is_file():
            raise FileNotFoundError(f"missing transcript fixture: {transcript_path}")
        if not sidecar_path.is_file():
            raise FileNotFoundError(f"missing sidecar fixture: {sidecar_path}")
        transcript_text = transcript_path.read_text(encoding="utf-8")
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
        return FixtureCase(
            fixture_id=fixture_id,
            transcript_path=transcript_path,
            sidecar_path=sidecar_path,
            transcript_text=transcript_text,
            sidecar=sidecar,
        )

    def run_case(self, fixture_id: str) -> HarnessCaseResult:
        case = self.load_case(fixture_id)
        sidecar = case.sidecar
        meeting = dict(sidecar["meeting"])
        # Ensure hash matches transcript bytes when not pre-bound correctly.
        digest = hashlib.sha256(case.transcript_text.encode("utf-8")).hexdigest()
        if not meeting.get("transcript_hash"):
            meeting["transcript_hash"] = digest

        request = ProviderRequest(
            fixture_id=fixture_id,
            transcript_text=case.transcript_text,
            transcript_path=str(case.transcript_path),
            meeting=meeting,
            participants=list(sidecar["participants"]),
            extraction_result=sidecar.get("extraction_result"),
            extraction_confidence=sidecar.get("extraction_confidence"),
            evidence_references=list(sidecar.get("evidence_references") or []),
        )

        errors: List[str] = []
        context_dict: Optional[Dict[str, Any]] = None
        provider_name = getattr(self.agent.provider, "name", "unknown")
        try:
            result: MeetingContextResult = self.agent.run(request)
            context_dict = result.to_dict()
            ok, schema_errors = validate_meeting_context(context_dict)
            if not ok:
                errors.extend(schema_errors)
            if context_dict.get("external_effects") != 0:
                errors.append("external_effects must be 0")
            if context_dict.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                errors.append("deterministic_policy_bypass must be false")
            # Basic consistency: participants non-empty and meeting id present.
            if not context_dict.get("participants"):
                errors.append("participants must be non-empty")
            if not context_dict.get("meeting", {}).get("meeting_id"):
                errors.append("meeting.meeting_id required")
        except Exception as exc:  # keep harness resilient for multi-case runs
            errors.append(f"{type(exc).__name__}: {exc}")

        return HarnessCaseResult(
            fixture_id=fixture_id,
            ok=not errors,
            provider=provider_name,
            context=context_dict,
            errors=errors,
            external_effects=(
                int(context_dict.get("external_effects", 1))
                if context_dict is not None
                else 1
            ),
            deterministic_policy_bypass=bool(
                (context_dict or {})
                .get("policy_authority", {})
                .get("deterministic_policy_bypass", True)
            ),
        )

    def run(
        self, fixture_ids: Optional[Sequence[str]] = None
    ) -> HarnessReport:
        ids: Iterable[str] = fixture_ids or DEFAULT_FIXTURE_IDS
        cases = [self.run_case(fid) for fid in ids]
        structured_valid = all(c.ok for c in cases)
        external_effects = max((c.external_effects for c in cases), default=0)
        bypass = any(c.deterministic_policy_bypass for c in cases)
        telemetry = self.agent.telemetry()
        return HarnessReport(
            cases=cases,
            gemini_provider_started=bool(
                telemetry.get("gemini_provider_started")
            ),
            google_adk_runtime_started=bool(
                telemetry.get("google_adk_runtime_started")
            ),
            adk_integration_status=str(
                telemetry.get("adk_integration_status")
                or "COMPATIBLE_SURFACE_ONLY"
            ),
            gemini_adk_started=bool(telemetry.get("gemini_adk_started")),
            meeting_context_agent_implemented=True,
            synthetic_transcript_input=True,
            structured_context_output_valid=structured_valid,
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
        )


def run_fixture_harness(
    *,
    provider_mode: str = "fixture",
    fixture_ids: Optional[Sequence[str]] = None,
) -> HarnessReport:
    harness = MeetingContextFixtureHarness(provider_mode=provider_mode)
    return harness.run(fixture_ids=fixture_ids)


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Meeting Context Agent fixture harness")
    parser.add_argument(
        "--provider",
        default="fixture",
        choices=["fixture", "gemini_adk_stub", "gemini_adk"],
        help="Provider mode (default: fixture; gemini_adk uses stub unless live env set)",
    )
    parser.add_argument(
        "--fixture",
        action="append",
        dest="fixtures",
        help="Fixture id (repeatable). Defaults to the three synthetic transcripts.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    provider_mode = args.provider
    report = run_fixture_harness(provider_mode=provider_mode, fixture_ids=args.fixtures)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
