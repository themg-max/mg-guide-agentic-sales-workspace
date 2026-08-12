"""Unit 3 fixture harness: ADK runtime + Follow-Up Planning Agent."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from agents.adk_runtime import (
    ADK_STATUS_RUNTIME_INTEGRATED,
    RUNTIME_BACKEND_GOOGLE_ADK,
)
from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context import RelationshipContextAgent
from agents.relationship_context.crm_store import SyntheticCrmStore

from .agent import FollowUpPlanningAgent
from .packet import validate_follow_up_packet
from .runtime import Unit3FollowUpRuntime
from .schema import validate_follow_up_proposal


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


# Scenario id -> transcript fixture + expected fail-closed/policy outcomes.
DEFAULT_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "SUCCESS": {
        "transcript_fixture": "transcript-success",
        "expected_packet_status": "completed",
        "expected_reason_codes": [],
        "expected_note_intents": 1,
        "expected_stage_intents": 1,
        "expected_policy_gate_invoked": True,
    },
    "AMBIGUOUS_CONTACT": {
        "transcript_fixture": "transcript-ambiguous-contact",
        "expected_packet_status": "blocked",
        "expected_reason_codes": ["AMBIGUOUS_CONTACT"],
        "expected_note_intents": 0,
        "expected_stage_intents": 0,
        "expected_policy_gate_invoked": False,
    },
    "AMBIGUOUS_OPPORTUNITY": {
        "transcript_fixture": "transcript-ambiguous-opportunity",
        "expected_packet_status": "blocked",
        "expected_reason_codes": ["AMBIGUOUS_OPPORTUNITY"],
        "expected_note_intents": 0,
        "expected_stage_intents": 0,
        "expected_policy_gate_invoked": False,
    },
    "NO_OPPORTUNITY": {
        "transcript_fixture": "transcript-no-stage-change",
        "expected_packet_status": "blocked",
        "expected_reason_codes": ["OPPORTUNITY_NOT_FOUND"],
        "expected_note_intents": 0,
        "expected_stage_intents": 0,
        "expected_policy_gate_invoked": False,
    },
    "STAGE_CHANGE_DENIED": {
        "transcript_fixture": "transcript-stage-change-denied",
        "expected_packet_status": "completed_with_review",
        "expected_reason_codes": ["STAGE_TRANSITION_NOT_ALLOWED"],
        "expected_note_intents": 1,
        "expected_stage_intents": 0,
        "expected_policy_gate_invoked": True,
    },
    "INSUFFICIENT_CONTEXT": {
        "transcript_fixture": "transcript-insufficient-context",
        "expected_packet_status": "blocked",
        "expected_reason_codes": ["LOW_EXTRACTION_CONFIDENCE"],
        "expected_note_intents": 0,
        "expected_stage_intents": 0,
        "expected_policy_gate_invoked": False,
    },
}


@dataclass
class Unit3CaseResult:
    scenario_id: str
    transcript_fixture: str
    ok: bool
    expected_packet_status: str
    actual_packet_status: Optional[str]
    errors: List[str]
    follow_up_proposal: Optional[Dict[str, Any]]
    follow_up_packet: Optional[Dict[str, Any]]
    policy_gate_invoked: bool
    external_effects: int
    deterministic_policy_bypass: bool
    relationship_context_reused: bool
    runtime_backend: Optional[str]
    google_adk_package_bound: bool
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool


@dataclass
class Unit3HarnessReport:
    cases: List[Unit3CaseResult]
    google_adk_package_bound: bool
    google_adk_runtime_started: bool
    adk_integration_status: str
    adk_runtime_backend: str
    adk_runtime_primitive_used: bool
    local_adk_fallback_used: bool
    follow_up_planning_agent_implemented: bool
    meeting_context_reused: bool
    relationship_context_reused: bool
    google_adk_runtime_reused: bool
    follow_up_proposal_output_valid: bool
    deterministic_policy_gate_invoked: bool
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
            and self.follow_up_planning_agent_implemented
            and self.meeting_context_reused
            and self.relationship_context_reused
            and self.google_adk_runtime_reused
            and self.follow_up_proposal_output_valid
            and self.deterministic_policy_gate_invoked
            and not self.deterministic_policy_bypass
            and self.external_effects == 0
            and all(v == "PASS" for v in self.scenario_results.values())
        )

    def proof_markers(self) -> Dict[str, Any]:
        """Proof-surface markers (YES/NO) derived from actual runtime state."""
        return {
            "FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED": (
                "YES" if self.follow_up_planning_agent_implemented else "NO"
            ),
            "MEETING_CONTEXT_REUSED": (
                "YES" if self.meeting_context_reused else "NO"
            ),
            "RELATIONSHIP_CONTEXT_REUSED": (
                "YES" if self.relationship_context_reused else "NO"
            ),
            "GOOGLE_ADK_RUNTIME_REUSED": (
                "YES"
                if (
                    self.google_adk_runtime_reused
                    and self.google_adk_package_bound
                    and self.google_adk_runtime_started
                    and self.adk_runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK
                )
                else "NO"
            ),
            "FOLLOW_UP_PROPOSAL_OUTPUT": (
                "VALID" if self.follow_up_proposal_output_valid else "INVALID"
            ),
            "DETERMINISTIC_POLICY_GATE_INVOKED": (
                "YES" if self.deterministic_policy_gate_invoked else "NO"
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
            "L3A_RUNTIME_STATUS": "DEFERRED_RUNTIME_NOT_PROMOTED",
            "FIRESTORE_WRITES": self.runtime_telemetry.get("firestore_writes", 0),
            "DEPLOYMENT": (
                "NO" if not self.runtime_telemetry.get("deployment") else "YES"
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
            "follow_up_planning_agent_implemented": (
                self.follow_up_planning_agent_implemented
            ),
            "meeting_context_reused": self.meeting_context_reused,
            "relationship_context_reused": self.relationship_context_reused,
            "google_adk_runtime_reused": self.google_adk_runtime_reused,
            "follow_up_proposal_output_valid": self.follow_up_proposal_output_valid,
            "deterministic_policy_gate_invoked": (
                self.deterministic_policy_gate_invoked
            ),
            "deterministic_policy_bypass": self.deterministic_policy_bypass,
            "external_effects": self.external_effects,
            "scenario_results": dict(self.scenario_results),
            "runtime_telemetry": self.runtime_telemetry,
            "cases": [
                {
                    "scenario_id": c.scenario_id,
                    "transcript_fixture": c.transcript_fixture,
                    "ok": c.ok,
                    "expected_packet_status": c.expected_packet_status,
                    "actual_packet_status": c.actual_packet_status,
                    "errors": list(c.errors),
                    "policy_gate_invoked": c.policy_gate_invoked,
                    "external_effects": c.external_effects,
                    "deterministic_policy_bypass": c.deterministic_policy_bypass,
                    "relationship_context_reused": c.relationship_context_reused,
                    "runtime_backend": c.runtime_backend,
                    "google_adk_package_bound": c.google_adk_package_bound,
                    "adk_runtime_primitive_used": c.adk_runtime_primitive_used,
                    "local_adk_fallback_used": c.local_adk_fallback_used,
                    "follow_up_proposal": c.follow_up_proposal,
                    "follow_up_packet": c.follow_up_packet,
                }
                for c in self.cases
            ],
        }


class Unit3FollowUpHarness:
    """Runs Unit 3 ADK runtime + follow-up planning scenarios (synthetic only)."""

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
        raise ValueError(
            f"unsupported meeting_provider_mode: {self.meeting_provider_mode}"
        )

    def _runtime(self) -> Unit3FollowUpRuntime:
        store = SyntheticCrmStore.from_fixture_path(self.crm_fixture_path)
        return Unit3FollowUpRuntime(
            meeting_agent=self._meeting_agent(),
            relationship_agent=RelationshipContextAgent(store=store),
            follow_up_agent=FollowUpPlanningAgent(),
        )

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

    def run_scenario(self, scenario_id: str) -> Unit3CaseResult:
        if scenario_id not in DEFAULT_SCENARIOS:
            raise KeyError(f"unknown scenario_id: {scenario_id}")
        meta = DEFAULT_SCENARIOS[scenario_id]
        transcript_fixture = meta["transcript_fixture"]
        expected_status = meta["expected_packet_status"]
        expected_codes = list(meta["expected_reason_codes"])
        errors: List[str] = []

        runtime = self._runtime()
        runtime.start()
        meeting_request = self._load_meeting_request(transcript_fixture)
        run = runtime.run_unit3(
            meeting_request=meeting_request,
            run_id=f"unit3_{scenario_id.lower()}",
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
        if not run.meeting_context_reused:
            errors.append("Meeting Context Agent must be reused")
        if not run.relationship_context_reused:
            errors.append("Relationship Context Agent must be reused")
        if run.errors:
            errors.extend(run.errors)

        actual_status: Optional[str] = None
        proposal = run.follow_up_proposal
        packet = run.follow_up_packet

        if proposal is None or packet is None:
            errors.append("follow_up_proposal/follow_up_packet missing")
        else:
            ok_schema, schema_errors = validate_follow_up_proposal(proposal)
            if not ok_schema:
                errors.extend(schema_errors)
            packet_errors = validate_follow_up_packet(packet)
            if packet_errors:
                errors.extend(packet_errors)

            actual_status = (packet.get("run") or {}).get("status")
            if actual_status != expected_status:
                errors.append(
                    f"expected packet status={expected_status}, got {actual_status}"
                )
            for code in expected_codes:
                if code not in (packet.get("policy") or {}).get("reason_codes", []):
                    errors.append(f"expected reason code {code} in packet policy")
            intents = packet.get("mutation_intents") or {"note": [], "stage": []}
            if len(intents.get("note") or []) != meta["expected_note_intents"]:
                errors.append(
                    f"expected {meta['expected_note_intents']} note intents, got "
                    f"{len(intents.get('note') or [])}"
                )
            if len(intents.get("stage") or []) != meta["expected_stage_intents"]:
                errors.append(
                    f"expected {meta['expected_stage_intents']} stage intents, got "
                    f"{len(intents.get('stage') or [])}"
                )
            if run.deterministic_policy_gate_invoked != (
                meta["expected_policy_gate_invoked"]
            ):
                errors.append(
                    f"expected policy_gate_invoked="
                    f"{meta['expected_policy_gate_invoked']}, got "
                    f"{run.deterministic_policy_gate_invoked}"
                )
            # Authority invariant: intents only exist under gate invocation.
            if (
                intents.get("note") or intents.get("stage")
            ) and not run.deterministic_policy_gate_invoked:
                errors.append("mutation intents without policy gate invocation")
            if proposal.get("external_effects") != 0:
                errors.append("proposal external_effects must be 0")
            if packet.get("external_effects") != 0:
                errors.append("packet external_effects must be 0")
            if proposal.get("policy_authority", {}).get(
                "deterministic_policy_bypass"
            ):
                errors.append("deterministic_policy_bypass must be false")

        bypass = run.deterministic_policy_bypass or any(
            "bypass" in e.lower() for e in errors
        )
        return Unit3CaseResult(
            scenario_id=scenario_id,
            transcript_fixture=transcript_fixture,
            ok=not errors,
            expected_packet_status=expected_status,
            actual_packet_status=actual_status,
            errors=errors,
            follow_up_proposal=proposal,
            follow_up_packet=packet,
            policy_gate_invoked=run.deterministic_policy_gate_invoked,
            external_effects=run.external_effects,
            deterministic_policy_bypass=bypass,
            relationship_context_reused=run.relationship_context_reused,
            runtime_backend=run.session.backend,
            google_adk_package_bound=run.google_adk_package_bound,
            adk_runtime_primitive_used=run.adk_runtime_primitive_used,
            local_adk_fallback_used=run.local_adk_fallback_used,
        )

    def run(
        self, scenario_ids: Optional[Sequence[str]] = None
    ) -> Unit3HarnessReport:
        ids: Iterable[str] = scenario_ids or tuple(DEFAULT_SCENARIOS.keys())
        cases = [self.run_scenario(sid) for sid in ids]
        scenario_results = {
            c.scenario_id: ("PASS" if c.ok else "FAIL") for c in cases
        }
        external_effects = max((c.external_effects for c in cases), default=0)
        bypass = any(c.deterministic_policy_bypass for c in cases)
        primitive_used = all(c.adk_runtime_primitive_used for c in cases) and bool(
            cases
        )
        package_bound = all(c.google_adk_package_bound for c in cases) and bool(
            cases
        )
        fallback_used = any(c.local_adk_fallback_used for c in cases)
        backends = {c.runtime_backend for c in cases}
        proposals_valid = all(
            c.follow_up_proposal is not None
            and c.follow_up_proposal.get("schema") == "follow_up_proposal_v1"
            and not validate_follow_up_proposal(c.follow_up_proposal)[1]
            for c in cases
        ) and bool(cases)

        # Fresh runtime telemetry sample (started + primitive use measured).
        sample_runtime = self._runtime()
        sample_runtime.start()
        telemetry = sample_runtime.telemetry()

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

        # The deterministic policy gate is the sole authorization surface:
        # invoked wherever mutation intents exist, and at least once overall.
        gate_invoked = (
            all(
                c.policy_gate_invoked
                for c in cases
                if (c.follow_up_packet or {}).get("mutation_intents", {}).get("note")
                or (c.follow_up_packet or {}).get("mutation_intents", {}).get("stage")
            )
            and any(c.policy_gate_invoked for c in cases)
            and not bypass
        )

        return Unit3HarnessReport(
            cases=cases,
            google_adk_package_bound=package_bound,
            google_adk_runtime_started=bool(runtime_started),
            adk_integration_status=integration_status,
            adk_runtime_backend=backend,
            adk_runtime_primitive_used=primitive_used,
            local_adk_fallback_used=fallback_used,
            follow_up_planning_agent_implemented=all(
                c.follow_up_proposal is not None for c in cases
            )
            and bool(cases),
            meeting_context_reused=all(
                (c.follow_up_packet or {}).get("meeting") for c in cases
            )
            and bool(cases),
            relationship_context_reused=all(
                c.relationship_context_reused for c in cases
            )
            and bool(cases),
            google_adk_runtime_reused=bool(runtime_started),
            follow_up_proposal_output_valid=proposals_valid,
            deterministic_policy_gate_invoked=bool(gate_invoked),
            deterministic_policy_bypass=bypass,
            external_effects=external_effects,
            scenario_results=scenario_results,
            runtime_telemetry=telemetry,
        )


def run_unit3_harness(
    *,
    scenario_ids: Optional[Sequence[str]] = None,
    meeting_provider_mode: str = "fixture",
) -> Unit3HarnessReport:
    harness = Unit3FollowUpHarness(meeting_provider_mode=meeting_provider_mode)
    return harness.run(scenario_ids=scenario_ids)


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Phase 3 Unit 3 ADK runtime + Follow-Up Planning harness"
    )
    parser.add_argument(
        "--scenario",
        action="append",
        dest="scenarios",
        help="Scenario id (repeatable). Defaults to all Unit 3 scenarios.",
    )
    parser.add_argument(
        "--meeting-provider",
        default="fixture",
        choices=["fixture", "gemini_adk_stub"],
        help="Meeting Context provider mode (default: fixture)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = run_unit3_harness(
        scenario_ids=args.scenarios,
        meeting_provider_mode=args.meeting_provider,
    )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
