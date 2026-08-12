"""Unit 2 fixture harness: ADK runtime + Relationship Context Agent."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from agents.adk_runtime import (
    ADK_STATUS_RUNTIME_INTEGRATED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    GoogleAdkRuntime,
    adk_runtime_declaration,
)
from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context.schema import validate_relationship_context

from .agent import RelationshipContextAgent
from .crm_store import SyntheticCrmStore


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


# Scenario id -> (transcript fixture id, expected resolution status)
DEFAULT_SCENARIOS: Dict[str, Dict[str, str]] = {
    "RELATIONSHIP_MATCH": {
        "transcript_fixture": "transcript-success",
        "expected_status": "matched",
    },
    "AMBIGUOUS_CONTACT": {
        "transcript_fixture": "transcript-ambiguous-contact",
        "expected_status": "ambiguous",
    },
    "NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT": {
        "transcript_fixture": "transcript-no-stage-change",
        "expected_status": "opportunity_missing",
    },
    "AMBIGUOUS_OPPORTUNITY": {
        "transcript_fixture": "transcript-ambiguous-opportunity",
        "expected_status": "opportunity_ambiguous",
    },
}


@dataclass
class Unit2CaseResult:
    scenario_id: str
    transcript_fixture: str
    ok: bool
    expected_status: str
    actual_status: Optional[str]
    errors: List[str]
    meeting_context: Optional[Dict[str, Any]]
    relationship_context: Optional[Dict[str, Any]]
    external_effects: int
    deterministic_policy_bypass: bool
    offline_ghl_adapter_used: bool
    runtime_backend: Optional[str]
    google_adk_package_bound: bool
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool


@dataclass
class Unit2HarnessReport:
    cases: List[Unit2CaseResult]
    google_adk_package_bound: bool
    google_adk_runtime_started: bool
    adk_integration_status: str
    adk_runtime_backend: str
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool
    meeting_context_agent_reused: bool
    relationship_context_agent_implemented: bool
    offline_ghl_adapter_used: bool
    synthetic_crm_context_only: bool
    relationship_context_output_valid: bool
    deterministic_policy_bypass: bool
    external_effects: int
    scenario_results: Dict[str, str]
    runtime_telemetry: Dict[str, Any]

    @property
    def ok(self) -> bool:
        return (
            all(c.ok for c in self.cases)
            and self.google_adk_package_bound
            and self.google_adk_runtime_started
            and self.adk_integration_status == ADK_STATUS_RUNTIME_INTEGRATED
            and self.adk_runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK
            and self.adk_runtime_primitive_used
            and not self.local_adk_fallback_used
            and self.relationship_context_output_valid
            and self.external_effects == 0
            and not self.deterministic_policy_bypass
            and all(v == "PASS" for v in self.scenario_results.values())
        )

    def proof_markers(self) -> Dict[str, Any]:
        """Proof-surface markers (YES/NO) derived from actual runtime state."""
        return {
            "GOOGLE_ADK_PACKAGE_BOUND": (
                "YES" if self.google_adk_package_bound else "NO"
            ),
            "GOOGLE_ADK_RUNTIME_STARTED": (
                "YES" if self.google_adk_runtime_started else "NO"
            ),
            "ADK_INTEGRATION_STATUS": self.adk_integration_status,
            "ADK_RUNTIME_BACKEND": self.adk_runtime_backend,
            "ADK_RUNTIME_PRIMITIVE_USED": (
                "YES" if self.adk_runtime_primitive_used else "NO"
            ),
            "LOCAL_ADK_FALLBACK_USED": (
                "YES" if self.local_adk_fallback_used else "NO"
            ),
            "DETERMINISTIC_POLICY_BYPASS": (
                "YES" if self.deterministic_policy_bypass else "NO"
            ),
            "EXTERNAL_EFFECTS": self.external_effects,
            "GHL_LIVE_CALLS": self.runtime_telemetry.get("ghl_live_calls", 0),
            "GHL_WRITES": self.runtime_telemetry.get("ghl_writes", 0),
            "REAL_CUSTOMER_DATA": self.runtime_telemetry.get(
                "real_customer_data", 0
            ),
            **self.scenario_results,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "proof_markers": self.proof_markers(),
            "google_adk_package_bound": self.google_adk_package_bound,
            "google_adk_runtime_started": self.google_adk_runtime_started,
            "adk_integration_status": self.adk_integration_status,
            "adk_runtime_backend": self.adk_runtime_backend,
            "adk_runtime_primitive_used": self.adk_runtime_primitive_used,
            "local_adk_fallback_used": self.local_adk_fallback_used,
            "meeting_context_agent_reused": self.meeting_context_agent_reused,
            "relationship_context_agent_implemented": (
                self.relationship_context_agent_implemented
            ),
            "offline_ghl_adapter_used": self.offline_ghl_adapter_used,
            "synthetic_crm_context_only": self.synthetic_crm_context_only,
            "relationship_context_output_valid": self.relationship_context_output_valid,
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
            "scenario_results": dict(self.scenario_results),
            "runtime_telemetry": self.runtime_telemetry,
            "cases": [
                {
                    "scenario_id": c.scenario_id,
                    "transcript_fixture": c.transcript_fixture,
                    "ok": c.ok,
                    "expected_status": c.expected_status,
                    "actual_status": c.actual_status,
                    "errors": list(c.errors),
                    "external_effects": c.external_effects,
                    "deterministic_policy_bypass": c.deterministic_policy_bypass,
                    "offline_ghl_adapter_used": c.offline_ghl_adapter_used,
                    "runtime_backend": c.runtime_backend,
                    "google_adk_package_bound": c.google_adk_package_bound,
                    "adk_runtime_primitive_used": c.adk_runtime_primitive_used,
                    "local_adk_fallback_used": c.local_adk_fallback_used,
                    "relationship_context": c.relationship_context,
                }
                for c in self.cases
            ],
        }


class Unit2RelationshipHarness:
    """Runs Unit 2 ADK runtime + relationship scenarios against synthetic data."""

    def __init__(
        self,
        *,
        fixtures_dir: Optional[Path] = None,
        crm_fixture_path: Optional[Path] = None,
        meeting_provider_mode: str = "fixture",
    ) -> None:
        self.fixtures_dir = fixtures_dir or (_repo_root() / "fixtures")
        self.crm_fixture_path = crm_fixture_path or (
            _repo_root() / "fixtures" / "ghl" / "relationship-context-crm.json"
        )
        self.meeting_provider_mode = meeting_provider_mode

    def _meeting_agent(self) -> MeetingContextAgent:
        if self.meeting_provider_mode == "fixture":
            return MeetingContextAgent.for_fixture_mode()
        if self.meeting_provider_mode in {"gemini_adk_stub", "stub"}:
            return MeetingContextAgent.for_gemini_adk(mode="stub")
        raise ValueError(f"unsupported meeting_provider_mode: {self.meeting_provider_mode}")

    def _load_meeting_request(self, transcript_fixture: str) -> ProviderRequest:
        transcript_path = self.fixtures_dir / f"{transcript_fixture}.txt"
        sidecar_path = self.fixtures_dir / f"{transcript_fixture}.expected.json"
        if not transcript_path.is_file():
            raise FileNotFoundError(f"missing transcript fixture: {transcript_path}")
        if not sidecar_path.is_file():
            raise FileNotFoundError(f"missing sidecar fixture: {sidecar_path}")
        transcript_text = transcript_path.read_text(encoding="utf-8")
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
        meeting = dict(sidecar["meeting"])
        digest = hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        if not meeting.get("transcript_hash"):
            meeting["transcript_hash"] = digest
        return ProviderRequest(
            fixture_id=transcript_fixture,
            transcript_text=transcript_text,
            transcript_path=str(transcript_path),
            meeting=meeting,
            participants=list(sidecar["participants"]),
            extraction_result=sidecar.get("extraction_result"),
            extraction_confidence=sidecar.get("extraction_confidence"),
            evidence_references=list(sidecar.get("evidence_references") or []),
        )

    def run_scenario(self, scenario_id: str) -> Unit2CaseResult:
        if scenario_id not in DEFAULT_SCENARIOS:
            raise KeyError(f"unknown scenario_id: {scenario_id}")
        meta = DEFAULT_SCENARIOS[scenario_id]
        transcript_fixture = meta["transcript_fixture"]
        expected_status = meta["expected_status"]
        errors: List[str] = []

        store = SyntheticCrmStore.from_fixture_path(self.crm_fixture_path)
        runtime = GoogleAdkRuntime(
            meeting_agent=self._meeting_agent(),
            relationship_agent=RelationshipContextAgent(store=store),
        )
        runtime.start()
        meeting_request = self._load_meeting_request(transcript_fixture)
        run = runtime.run_unit2(
            meeting_request=meeting_request,
            run_id=f"unit2_{scenario_id.lower()}",
            scenario_id=scenario_id,
        )

        if not run.google_adk_package_bound:
            errors.append("GOOGLE_ADK_PACKAGE_BOUND expected YES")
        if not run.google_adk_runtime_started:
            errors.append("GOOGLE_ADK_RUNTIME_STARTED expected YES")
        if run.adk_integration_status != ADK_STATUS_RUNTIME_INTEGRATED:
            errors.append(
                f"ADK_INTEGRATION_STATUS expected RUNTIME_INTEGRATED, got "
                f"{run.adk_integration_status}"
            )
        if run.session.backend != RUNTIME_BACKEND_GOOGLE_ADK:
            errors.append(
                f"ADK_RUNTIME_BACKEND expected google_adk_package, got "
                f"{run.session.backend}"
            )
        if not run.adk_runtime_primitive_used:
            errors.append("ADK_RUNTIME_PRIMITIVE_USED expected YES")
        if run.local_adk_fallback_used:
            errors.append("LOCAL_ADK_FALLBACK_USED expected NO")
        if not run.meeting_context_agent_reused:
            errors.append("Meeting Context Agent must be reused")
        if not run.relationship_context_agent_implemented:
            errors.append("Relationship Context Agent must be implemented")
        if run.errors:
            errors.extend(run.errors)

        actual_status: Optional[str] = None
        rel = run.relationship_context
        if rel is None:
            errors.append("relationship_context missing")
        else:
            ok_schema, schema_errors = validate_relationship_context(rel)
            if not ok_schema:
                errors.extend(schema_errors)
            actual_status = (rel.get("resolution") or {}).get("status")
            if actual_status != expected_status:
                errors.append(
                    f"expected resolution.status={expected_status}, got {actual_status}"
                )
            if rel.get("external_effects") != 0:
                errors.append("relationship external_effects must be 0")
            if rel.get("policy_authority", {}).get("deterministic_policy_bypass"):
                errors.append("deterministic_policy_bypass must be false")
            if (rel.get("crm_source") or {}).get("live_calls", 0) != 0:
                errors.append("GHL live_calls must be 0")
            if (rel.get("crm_source") or {}).get("writes", 0) != 0:
                errors.append("GHL writes must be 0")

        bypass = run.deterministic_policy_bypass or any(
            "bypass" in e.lower() for e in errors
        )
        return Unit2CaseResult(
            scenario_id=scenario_id,
            transcript_fixture=transcript_fixture,
            ok=not errors,
            expected_status=expected_status,
            actual_status=actual_status,
            errors=errors,
            meeting_context=run.meeting_context,
            relationship_context=rel,
            external_effects=run.external_effects,
            deterministic_policy_bypass=bypass,
            offline_ghl_adapter_used=run.offline_ghl_adapter_used,
            runtime_backend=run.session.backend,
            google_adk_package_bound=run.google_adk_package_bound,
            adk_runtime_primitive_used=run.adk_runtime_primitive_used,
            local_adk_fallback_used=run.local_adk_fallback_used,
        )

    def run(
        self, scenario_ids: Optional[Sequence[str]] = None
    ) -> Unit2HarnessReport:
        ids: Iterable[str] = scenario_ids or tuple(DEFAULT_SCENARIOS.keys())
        cases = [self.run_scenario(sid) for sid in ids]
        scenario_results = {
            c.scenario_id: ("PASS" if c.ok else "FAIL") for c in cases
        }
        external_effects = max((c.external_effects for c in cases), default=0)
        bypass = any(c.deterministic_policy_bypass for c in cases)
        offline_used = all(c.offline_ghl_adapter_used for c in cases) and bool(cases)
        rel_valid = all(
            c.ok and c.relationship_context is not None for c in cases
        ) and bool(cases)

        # Fresh runtime telemetry sample (started + primitive use measured).
        sample_runtime = GoogleAdkRuntime(
            meeting_agent=self._meeting_agent(),
            relationship_agent=RelationshipContextAgent(
                store=SyntheticCrmStore.from_fixture_path(self.crm_fixture_path)
            ),
        )
        sample_runtime.start()
        telemetry = sample_runtime.telemetry()

        # Primitive use is measured per case run; aggregate from case results.
        primitive_used = all(c.adk_runtime_primitive_used for c in cases) and bool(
            cases
        )
        package_bound = all(c.google_adk_package_bound for c in cases) and bool(
            cases
        )
        fallback_used = any(c.local_adk_fallback_used for c in cases)
        backends = {c.runtime_backend for c in cases}
        runtime_started = (
            package_bound
            and primitive_used
            and telemetry.get("runtime_started") is True
        )
        backend = (
            RUNTIME_BACKEND_GOOGLE_ADK
            if backends == {RUNTIME_BACKEND_GOOGLE_ADK}
            else (sorted(backends)[0] if backends else telemetry["runtime_backend"])
        )
        integration_status = (
            ADK_STATUS_RUNTIME_INTEGRATED
            if runtime_started
            and backend == RUNTIME_BACKEND_GOOGLE_ADK
            and not fallback_used
            else telemetry["adk_integration_status"]
        )

        return Unit2HarnessReport(
            cases=cases,
            google_adk_package_bound=package_bound,
            google_adk_runtime_started=bool(runtime_started),
            adk_integration_status=integration_status,
            adk_runtime_backend=backend,
            adk_runtime_primitive_used=primitive_used,
            local_adk_fallback_used=fallback_used,
            meeting_context_agent_reused=True,
            relationship_context_agent_implemented=True,
            offline_ghl_adapter_used=offline_used,
            synthetic_crm_context_only=True,
            relationship_context_output_valid=rel_valid,
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
            scenario_results=scenario_results,
            runtime_telemetry=telemetry,
        )


def run_unit2_harness(
    *,
    scenario_ids: Optional[Sequence[str]] = None,
    meeting_provider_mode: str = "fixture",
) -> Unit2HarnessReport:
    harness = Unit2RelationshipHarness(meeting_provider_mode=meeting_provider_mode)
    return harness.run(scenario_ids=scenario_ids)


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Phase 3 Unit 2 ADK runtime + Relationship Context harness"
    )
    parser.add_argument(
        "--scenario",
        action="append",
        dest="scenarios",
        help="Scenario id (repeatable). Defaults to all Unit 2 scenarios.",
    )
    parser.add_argument(
        "--meeting-provider",
        default="fixture",
        choices=["fixture", "gemini_adk_stub"],
        help="Meeting Context provider mode (default: fixture)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = run_unit2_harness(
        scenario_ids=args.scenarios,
        meeting_provider_mode=args.meeting_provider,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
