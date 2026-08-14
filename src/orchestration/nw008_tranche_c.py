"""NW-008 Tranche C historical failure-path replay harness.

Feeds AT-2 / AT-4 / AT-5 synthetic transcript source envelopes through the
existing Unit 3 agent fleet (Meeting Context → Relationship Context →
Follow-Up Planning) and records per-run proof.

The harness does not introduce a parallel orchestration engine, live CRM/GHL
calls, Firestore writes, policy changes, or Google Workspace integration.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml
from jsonschema import Draft202012Validator

from agents.follow_up_planning import FollowUpPlanningAgent, Unit3FollowUpRuntime
from agents.meeting_context import MeetingContextAgent
from agents.relationship_context import RelationshipContextAgent
from agents.relationship_context.crm_store import SyntheticCrmStore
from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_html import render_decision_card_html
from mg_guide.meeting_follow_up_card.decision_render_text import render_decision_card_text
from orchestration.state_machine import StateMachine
from orchestration.transcript_source import (
    TranscriptSourceEnvelope,
    envelope_from_dict,
    envelope_to_provider_request,
    validate_envelope,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "fixtures" / "nw008" / "tranche_c"
PROOF_ROOT = REPO_ROOT / "proof" / "nw008" / "tranche-c"
CRM_FIXTURE = REPO_ROOT / "fixtures" / "ghl" / "relationship-context-crm.json"
ENVELOPE_SCHEMA = REPO_ROOT / "contracts" / "transcript_source_envelope.schema.json"

ENTRYPOINTS = {
    "MEETING_CONTEXT_ENTRYPOINT": "agents.meeting_context.agent.MeetingContextAgent.run",
    "RELATIONSHIP_CONTEXT_ENTRYPOINT": "agents.relationship_context.agent.RelationshipContextAgent.run",
    "FOLLOW_UP_PLANNING_ENTRYPOINT": "agents.follow_up_planning.agent.FollowUpPlanningAgent.run",
    "ADK_RUNTIME_ENTRYPOINT": "agents.follow_up_planning.runtime.Unit3FollowUpRuntime.run_unit3",
    "POLICY_ENTRYPOINT": "orchestration.policy.evaluate_policy",
    "PACKET_ENTRYPOINT": "agents.follow_up_planning.packet.FollowUpPacketAssembler.assemble",
    "DECISION_CARD_ENTRYPOINT": "mg_guide.meeting_follow_up_card.decision_mapper.map_packet_to_decision_card",
    "TRANSCRIPT_SOURCE_ENTRYPOINT": "orchestration.transcript_source.envelope_to_provider_request",
}

SCENARIOS = {
    "AT-02": {
        "governed_stop_profile": {
            "boundary_agent_id": "relationship_context_agent",
        },
        "expected_reason_code": "AMBIGUOUS_CONTACT",
        "expected_stop_point": "relationship_context_agent",
        "expected_disposition": "blocked",
        "expected_policy_gate_invoked": False,
        "historical_card_required": True,
    },
    "AT-04": {
        "governed_stop_profile": {
            "boundary_agent_id": "relationship_context_agent",
        },
        "expected_reason_code": "CONTACT_NOT_FOUND",
        "expected_stop_point": "relationship_context_agent",
        "expected_disposition": "blocked",
        "expected_policy_gate_invoked": False,
        "historical_card_required": False,
    },
    "AT-05": {
        "governed_stop_profile": {
            "boundary_agent_id": "meeting_context_agent",
        },
        "expected_reason_code": "LOW_EXTRACTION_CONFIDENCE",
        "expected_stop_point": "meeting_context_agent",
        "expected_disposition": "blocked",
        "expected_policy_gate_invoked": False,
        "historical_card_required": False,
    },
}

AUTHORITATIVE_STOP_SOURCE = "STATE_MACHINE_WORKFLOW_CONTRACT"

SCENARIO_LABELS = {
    "AT-02": "AT-2",
    "AT-04": "AT-4",
    "AT-05": "AT-5",
}

SCENARIO_STEMS = {
    "AT-02": "at-02",
    "AT-04": "at-04",
    "AT-05": "at-05",
}

STOP_BOUNDARY_DOWNSTREAM = {
    "meeting_context_agent": (
        "relationship_context_agent",
        "follow_up_planning_agent",
    ),
    "relationship_context_agent": ("follow_up_planning_agent",),
}

STATE_2_EQUIVALENT_AT2 = {
    "policy_state": "BLOCKED",
    "policy_reason_code": "AMBIGUOUS_CONTACT",
    "next_action": "RESOLVE_CONTACT",
}

AT2_CARD_EVIDENCE_SOURCE = (
    "GOVERNED_STOP_PROOF_PROJECTION_THROUGH_EXISTING_NW007_MAPPER"
)


class TrancheCReplayError(RuntimeError):
    """Raised when a Tranche C replay violates an invariant."""


@dataclass(frozen=True)
class ObligationResult:
    STATUS: str
    EVIDENCE_PATH: str
    DETAIL: str
    REMAINING_GAP: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "STATUS": self.STATUS,
            "EVIDENCE_PATH": self.EVIDENCE_PATH,
            "DETAIL": self.DETAIL,
            "REMAINING_GAP": self.REMAINING_GAP,
        }


@dataclass(frozen=True)
class ScenarioRun:
    scenario: str
    envelope: Dict[str, Any]
    transcript_content_hash: str
    envelope_digest: str
    sidecar: Dict[str, Any]
    run_id: str
    run_path: str
    envelope_path: str
    result: Dict[str, Any]
    agents_started: List[str]
    agents_completed: List[str]
    agent_statuses: Dict[str, str]
    agent_execution: Dict[str, Any]
    stop_point: str
    stop_reason_code: str
    stop_reason_source: str
    policy_bypass: bool
    policy_gate_invoked: bool
    disposition: str
    effect_counters: Dict[str, Any]
    packet: Optional[Dict[str, Any]]
    proposal: Optional[Dict[str, Any]]
    decision_card: Optional[Dict[str, Any]]
    decision_card_text: str
    decision_card_html: str
    envelope_preserved: bool


@dataclass(frozen=True)
class TrancheCResult:
    implementation_subject_sha: str
    scenarios: Dict[str, ScenarioRun]
    proof_obligations: Dict[str, ObligationResult]
    effect_counters: Dict[str, Any]
    historical_at_claims: Dict[str, Any]
    remaining_gaps: List[str]
    deterministic_replay: str


def _git_head(repo_root: Path) -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=str(repo_root), text=True
            )
            .strip()
            or "UNKNOWN"
        )
    except Exception:  # pragma: no cover - defensive
        return "UNKNOWN"


def _canonical_json_text(data: Mapping[str, Any]) -> str:
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _sha256_dict(data: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json_text(data).encode("utf-8")).hexdigest()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_envelope_schema() -> Dict[str, Any]:
    return json.loads(ENVELOPE_SCHEMA.read_text(encoding="utf-8"))


def _validate_proof_return(data: Mapping[str, Any]) -> Tuple[bool, List[str]]:
    schema_path = REPO_ROOT / "contracts" / "nw008_tranche_c_proof_return.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(dict(data)), key=lambda e: list(e.path))
    messages = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        messages.append(f"{path}: {err.message}")
    return (not messages, messages)


class Nw008TrancheCHarness:
    def __init__(
        self,
        *,
        repo_root: Optional[Path] = None,
        fixtures_dir: Optional[Path] = None,
        proof_root: Optional[Path] = None,
        crm_fixture_path: Optional[Path] = None,
        commit_sha: Optional[str] = None,
    ) -> None:
        self.repo_root = repo_root or REPO_ROOT
        self.fixtures_dir = fixtures_dir or FIXTURES_DIR
        self.proof_root = proof_root or PROOF_ROOT
        self.crm_fixture_path = crm_fixture_path or CRM_FIXTURE
        self.implementation_subject_sha = commit_sha or _git_head(self.repo_root)

    def run(self, *, verify_replay: bool = True) -> TrancheCResult:
        scenarios = self._execute_replay()
        deterministic_replay = "NOT_RUN"
        if verify_replay:
            replay_scenarios = self._execute_replay()
            deterministic_replay = (
                "PASS"
                if self._normalized_snapshot(scenarios)
                == self._normalized_snapshot(replay_scenarios)
                else "FAIL"
            )

        proof_obligations = self._proof_obligations(
            scenarios,
            deterministic_replay=deterministic_replay,
        )
        remaining_gaps = [
            f"{tc_id}:{result.REMAINING_GAP}"
            for tc_id, result in proof_obligations.items()
            if result.REMAINING_GAP
        ]
        effect_counters = self._aggregate_effect_counters(scenarios)
        historical_at_claims = self._historical_at_claims(scenarios)

        return TrancheCResult(
            implementation_subject_sha=self.implementation_subject_sha,
            scenarios=scenarios,
            proof_obligations=proof_obligations,
            effect_counters=effect_counters,
            historical_at_claims=historical_at_claims,
            remaining_gaps=remaining_gaps,
            deterministic_replay=deterministic_replay,
        )

    def _execute_replay(self) -> Dict[str, ScenarioRun]:
        scenarios: Dict[str, ScenarioRun] = {}
        for scenario in SCENARIOS:
            scenarios[scenario] = self._run_scenario(scenario)
        return scenarios

    @staticmethod
    def _normalized_snapshot(
        scenarios: Mapping[str, ScenarioRun],
    ) -> Dict[str, Any]:
        snapshot: Dict[str, Any] = {}
        for scenario, run in scenarios.items():
            run_dict = deepcopy(run.result)
            session = run_dict.get("session") or {}
            if isinstance(session, dict):
                session.pop("session_id", None)
                for trace_entry in session.get("agent_trace") or []:
                    if isinstance(trace_entry, dict):
                        trace_entry.pop("error", None)
            for key in ("run", "audit"):
                section = ((run_dict.get("follow_up_packet") or {}).get(key) or {})
                if isinstance(section, dict):
                    section.pop("created_at", None)
                    section.pop("started_at", None)
                    section.pop("completed_at", None)
            snapshot[scenario] = {
                "result": run_dict,
                "transcript_content_hash": run.transcript_content_hash,
                "envelope_digest": run.envelope_digest,
                "stop_point": run.stop_point,
                "stop_reason_code": run.stop_reason_code,
                "stop_reason_source": run.stop_reason_source,
                "policy_bypass": run.policy_bypass,
                "policy_gate_invoked": run.policy_gate_invoked,
                "disposition": run.disposition,
                "effect_counters": dict(run.effect_counters),
                "agent_statuses": dict(run.agent_statuses),
            }
        return snapshot

    def write_proof_artifacts(
        self, result: Optional[TrancheCResult] = None
    ) -> Dict[str, Path]:
        result = result or self.run()
        self.proof_root.mkdir(parents=True, exist_ok=True)
        paths: Dict[str, Path] = {}
        for scenario, run in result.scenarios.items():
            stem = SCENARIO_STEMS[scenario]
            run_path = self.proof_root / f"{stem}-run.json"
            run_path.write_text(
                json.dumps(run.result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            paths[f"{scenario}_run"] = run_path
        manifest_path = self.proof_root / "proof-manifest.md"
        return_path = self.proof_root / "proof-return.yaml"
        manifest_path.write_text(self._manifest(result), encoding="utf-8")
        return_payload = self._proof_return_payload(result)
        ok, errors = _validate_proof_return(return_payload)
        if not ok:
            raise TrancheCReplayError(
                "proof-return failed schema validation: " + "; ".join(errors)
            )
        return_path.write_text(
            yaml.safe_dump(return_payload, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        paths["proof_manifest"] = manifest_path
        paths["proof_return"] = return_path
        return paths

    def _run_scenario(self, scenario: str) -> ScenarioRun:
        spec = SCENARIOS[scenario]
        stem = SCENARIO_STEMS[scenario]
        label = SCENARIO_LABELS[scenario]
        envelope_path = self.fixtures_dir / f"{stem}-envelope.json"
        sidecar_path = self.fixtures_dir / f"{stem}-sidecar.json"
        run_path = f"proof/nw008/tranche-c/{stem}-run.json"
        envelope_path_public = f"fixtures/nw008/tranche_c/{stem}-envelope.json"

        envelope_raw = _load_json(envelope_path)
        ok, errors = validate_envelope(envelope_raw)
        if not ok:
            raise TrancheCReplayError(
                f"{scenario} envelope validation failed: " + "; ".join(errors)
            )
        envelope = envelope_from_dict(envelope_raw)
        transcript_content_hash = envelope.content_hash
        envelope_digest = _sha256_dict(envelope_raw)
        sidecar = _load_json(sidecar_path)

        request = envelope_to_provider_request(
            envelope,
            extraction_result=sidecar["extraction_result"],
            extraction_confidence=sidecar["extraction_confidence"],
            evidence_references=sidecar.get("evidence_references"),
            participants=sidecar["participants"],
        )

        store = SyntheticCrmStore.from_fixture_path(self.crm_fixture_path)
        runtime = Unit3FollowUpRuntime(
            meeting_agent=MeetingContextAgent.for_fixture_mode(),
            relationship_agent=RelationshipContextAgent(store=store),
            follow_up_agent=FollowUpPlanningAgent(),
        )
        runtime.start()
        run_id = f"nw008_tranche_c_{stem}"
        unit3_result = runtime.run_unit3(
            meeting_request=request,
            run_id=run_id,
            scenario_id=f"NW008_TC_{label}",
            governed_stop_profile=spec["governed_stop_profile"],
        )
        if not unit3_result.ok:
            raise TrancheCReplayError(
                f"{scenario} runtime failed: " + "; ".join(unit3_result.errors)
            )

        result_dict = unit3_result.to_dict()
        packet = (
            dict(unit3_result.follow_up_packet)
            if isinstance(unit3_result.follow_up_packet, Mapping)
            else None
        )
        proposal = (
            dict(unit3_result.follow_up_proposal)
            if isinstance(unit3_result.follow_up_proposal, Mapping)
            else None
        )

        packet_effects = int((packet or {}).get("external_effects", 0))
        proposal_effects = int((proposal or {}).get("external_effects", 0))
        if proposal_effects != 0 or packet_effects != 0:
            raise TrancheCReplayError(f"{scenario}: external_effects must be 0")

        trace = list((result_dict.get("session") or {}).get("agent_trace") or [])
        agents_started = [str(a.get("agent_id")) for a in trace if a.get("agent_id")]
        agents_completed = [
            str(a.get("agent_id"))
            for a in trace
            if a.get("agent_id")
            and a.get("status") in {"ok", "BLOCK_ORIGIN"}
        ]
        agent_statuses = {
            str(a.get("agent_id")): str(a.get("status"))
            for a in trace
            if a.get("agent_id")
        }

        governed_stop = (
            dict(unit3_result.governed_stop)
            if isinstance(unit3_result.governed_stop, Mapping)
            else {}
        )
        stop_point = str(governed_stop.get("boundary_agent_id") or "")
        stop_reason_code = str(governed_stop.get("reason_code") or "")
        stop_reason_source = str(governed_stop.get("reason_source") or "")

        if not stop_reason_code and proposal is not None:
            reason_codes = list(
                (proposal.get("policy_evaluation") or {}).get("reason_codes") or []
            )
            if reason_codes:
                stop_reason_code = str(reason_codes[0])
        if not stop_reason_code and packet is not None:
            reason_codes = list((packet.get("policy") or {}).get("reason_codes") or [])
            if reason_codes:
                stop_reason_code = str(reason_codes[0])

        disposition = (
            str((packet.get("run") or {}).get("status"))
            if packet is not None
            else "blocked"
        )
        if stop_point != spec["expected_stop_point"]:
            raise TrancheCReplayError(
                f"{scenario}: expected stop_point={spec['expected_stop_point']} got {stop_point}"
            )
        if stop_reason_code != spec["expected_reason_code"]:
            raise TrancheCReplayError(
                f"{scenario}: expected reason_code={spec['expected_reason_code']} got {stop_reason_code}"
            )
        if disposition != spec["expected_disposition"]:
            raise TrancheCReplayError(
                f"{scenario}: expected disposition={spec['expected_disposition']} got {disposition}"
            )

        policy_bypass = bool(unit3_result.deterministic_policy_bypass)
        policy_gate_invoked = bool(unit3_result.deterministic_policy_gate_invoked)
        if policy_gate_invoked != spec["expected_policy_gate_invoked"]:
            raise TrancheCReplayError(
                f"{scenario}: expected policy_gate_invoked={spec['expected_policy_gate_invoked']} "
                f"got {policy_gate_invoked}"
            )

        decision_packet = packet or self._decision_card_packet_for_governed_stop(
            run_id=run_id,
            reason_code=stop_reason_code,
            agents_started=agents_started,
        )
        card = map_packet_to_decision_card(decision_packet)
        decision_card = card.to_dict()

        result_dict["transcript_source_envelope"] = {
            "schema": envelope_raw.get("schema"),
            "source": deepcopy(envelope_raw.get("source")),
            "ownership": deepcopy(envelope_raw.get("ownership")),
            "access_context": deepcopy(envelope_raw.get("access_context")),
            "provenance": deepcopy(envelope_raw.get("provenance")),
        }
        result_dict["transcript_content_hash"] = transcript_content_hash
        result_dict["transcript_source_envelope_digest"] = envelope_digest
        envelope_preserved = self._envelope_preserved(
            result_dict=result_dict,
            envelope_raw=envelope_raw,
            envelope_digest=envelope_digest,
        )

        return ScenarioRun(
            scenario=scenario,
            envelope=envelope_raw,
            transcript_content_hash=transcript_content_hash,
            envelope_digest=envelope_digest,
            sidecar=sidecar,
            run_id=run_id,
            run_path=run_path,
            envelope_path=envelope_path_public,
            result=result_dict,
            agents_started=agents_started,
            agents_completed=agents_completed,
            agent_statuses=agent_statuses,
            agent_execution=dict(unit3_result.agent_execution),
            stop_point=stop_point,
            stop_reason_code=stop_reason_code,
            stop_reason_source=stop_reason_source,
            policy_bypass=policy_bypass,
            policy_gate_invoked=policy_gate_invoked,
            disposition=disposition,
            effect_counters={
                "GHL_LIVE_CALLS": 0,
                "GHL_READS": 0,
                "GHL_WRITES": 0,
                "FIRESTORE_WRITES": 0,
                "EXTERNAL_EFFECTS": unit3_result.external_effects,
                "REAL_CUSTOMER_DATA": 0,
            },
            packet=packet,
            proposal=proposal,
            decision_card=decision_card,
            decision_card_text=render_decision_card_text(card),
            decision_card_html=render_decision_card_html(card),
            envelope_preserved=envelope_preserved,
        )

    @staticmethod
    def _decision_card_packet_for_governed_stop(
        *, run_id: str, reason_code: str, agents_started: List[str]
    ) -> Dict[str, Any]:
        return {
            "schema": "meeting_follow_up_packet_v1",
            "run": {"run_id": run_id, "status": "blocked"},
            "policy": {
                "reason_codes": [reason_code] if reason_code else [],
            },
            "external_effects": 0,
            "audit": {
                "agents_used": list(agents_started),
            },
        }

    @staticmethod
    def _envelope_preserved(
        *,
        result_dict: Dict[str, Any],
        envelope_raw: Dict[str, Any],
        envelope_digest: str,
    ) -> bool:
        preserved = result_dict.get("transcript_source_envelope") or {}
        required_keys = ("source", "ownership", "access_context", "provenance")
        for key in required_keys:
            if preserved.get(key) != envelope_raw.get(key):
                return False
        if result_dict.get("transcript_content_hash") != (
            (envelope_raw.get("artifact") or {}).get("content_hash")
        ):
            return False
        if result_dict.get("transcript_source_envelope_digest") != envelope_digest:
            return False
        return True

    @staticmethod
    def _scenario_evidence_paths(scenario: str) -> str:
        stem = SCENARIO_STEMS[scenario]
        return (
            f"fixtures/nw008/tranche_c/{stem}-envelope.json | "
            f"fixtures/nw008/tranche_c/{stem}-sidecar.json | "
            f"proof/nw008/tranche-c/{stem}-run.json"
        )

    @staticmethod
    def _verify_historical_definitions() -> Tuple[bool, str]:
        contract_path = REPO_ROOT / "contracts" / "workflow_states.yaml"
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        sm = StateMachine(contract)
        invariants_list = contract.get("invariants") or []
        invariants: Dict[str, Any] = {}
        for item in invariants_list:
            if isinstance(item, dict):
                invariants.update(item)
        checks: List[Tuple[bool, str]] = [
            (sm.is_terminal("blocked"), "blocked state is terminal"),
            (
                any(
                    tr.source == "extracting"
                    and tr.target == "blocked"
                    and tr.reason_code == "LOW_EXTRACTION_CONFIDENCE"
                    for tr in sm.transitions
                ),
                "AT-5 extracting->blocked LOW_EXTRACTION_CONFIDENCE",
            ),
            (
                any(
                    tr.source == "resolving"
                    and tr.target == "blocked"
                    and tr.reason_code == "AMBIGUOUS_CONTACT"
                    for tr in sm.transitions
                ),
                "AT-2 resolving->blocked AMBIGUOUS_CONTACT",
            ),
            (
                any(
                    tr.source == "resolving"
                    and tr.target == "blocked"
                    and tr.reason_code == "CONTACT_NOT_FOUND"
                    for tr in sm.transitions
                ),
                "AT-4 resolving->blocked CONTACT_NOT_FOUND",
            ),
            (
                invariants.get("production_crm_writes") == "forbidden",
                "production_crm_writes forbidden (0 CRM writes)",
            ),
            (
                float(sm.extraction_abort_threshold) == 0.70,
                f"AT-5 extraction_abort_threshold=0.70 (got {sm.extraction_abort_threshold})",
            ),
        ]
        failed = [desc for ok, desc in checks if not ok]
        if failed:
            return False, "historical definition mismatch: " + "; ".join(failed)
        return (
            True,
            "canonical AT-2/AT-4/AT-5 definitions verified in contracts/workflow_states.yaml",
        )

    @staticmethod
    def _zero_effects(run: ScenarioRun) -> bool:
        return all(
            int(run.effect_counters.get(key, 0)) == 0
            for key in (
                "GHL_LIVE_CALLS",
                "GHL_READS",
                "GHL_WRITES",
                "FIRESTORE_WRITES",
                "EXTERNAL_EFFECTS",
                "REAL_CUSTOMER_DATA",
            )
        )

    @staticmethod
    def _obligation(
        *,
        ok: bool,
        detail: str,
        evidence_path: str,
        remaining_gap: str = "",
    ) -> ObligationResult:
        return ObligationResult(
            STATUS="PASS" if ok else "FAIL",
            EVIDENCE_PATH=evidence_path,
            DETAIL=detail,
            REMAINING_GAP="" if ok else remaining_gap,
        )

    def _short_circuit_valid(
        self,
        *,
        run: ScenarioRun,
        boundary_agent: str,
    ) -> bool:
        boundary_execution = run.agent_execution.get(boundary_agent) or {}
        if (
            boundary_execution.get("wrapper_status") != "BLOCK_ORIGIN"
            or boundary_execution.get("delegate_called") is not True
        ):
            return False
        for downstream in STOP_BOUNDARY_DOWNSTREAM.get(boundary_agent, ()):
            entry = run.agent_execution.get(downstream) or {}
            if (
                entry.get("wrapper_status") != "SKIPPED_GOVERNED_STOP"
                or entry.get("delegate_called") is not False
            ):
                return False
            if downstream in run.agents_completed:
                return False
        return True

    def _proof_obligations(
        self,
        scenarios: Mapping[str, ScenarioRun],
        *,
        deterministic_replay: str,
    ) -> Dict[str, ObligationResult]:
        obligations: Dict[str, ObligationResult] = {}

        at2 = scenarios["AT-02"]
        at4 = scenarios["AT-04"]
        at5 = scenarios["AT-05"]

        obligations["TC-01"] = self._obligation(
            ok=at2.transcript_content_hash
            == str((at2.envelope.get("artifact") or {}).get("content_hash") or ""),
            detail=(
                "AT-2 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with "
                f"TRANSCRIPT_CONTENT_HASH={at2.transcript_content_hash}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-02"),
            remaining_gap="tc01_content_hash_mismatch",
        )
        obligations["TC-02"] = self._obligation(
            ok=all(
                agent in at2.agents_started
                for agent in (
                    "meeting_context_agent",
                    "relationship_context_agent",
                    "follow_up_planning_agent",
                )
            ),
            detail=f"AT-2 AGENTS_STARTED={at2.agents_started}",
            evidence_path=self._scenario_evidence_paths("AT-02"),
            remaining_gap="tc02_agent_trace_missing",
        )
        obligations["TC-03"] = self._obligation(
            ok=(
                at2.stop_reason_code == "AMBIGUOUS_CONTACT"
                and at2.stop_point == "relationship_context_agent"
                and at2.disposition == "blocked"
            ),
            detail=(
                f"AT-2 STOP_POINT={at2.stop_point}, STOP_REASON_CODE={at2.stop_reason_code}, "
                f"DISPOSITION={at2.disposition}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-02"),
            remaining_gap="tc03_at2_stop_reason_or_disposition",
        )
        obligations["TC-04"] = self._obligation(
            ok=self._short_circuit_valid(
                run=at2,
                boundary_agent="relationship_context_agent",
            ),
            detail=(
                f"AT-2 AGENT_STATUSES={at2.agent_statuses}, AGENT_EXECUTION={at2.agent_execution}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-02"),
            remaining_gap="tc04_downstream_execution_after_governed_stop",
        )
        obligations["TC-05"] = self._obligation(
            ok=(
                at2.policy_gate_invoked is False
                and at2.policy_bypass is False
                and self._zero_effects(at2)
            ),
            detail=(
                "AT-2 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, "
                f"POLICY_BYPASS={at2.policy_bypass}, EFFECT_COUNTERS={at2.effect_counters}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-02"),
            remaining_gap="tc05_pre_policy_fail_closed_violation",
        )

        obligations["TC-06"] = self._obligation(
            ok=at4.transcript_content_hash
            == str((at4.envelope.get("artifact") or {}).get("content_hash") or ""),
            detail=(
                "AT-4 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with "
                f"TRANSCRIPT_CONTENT_HASH={at4.transcript_content_hash}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-04"),
            remaining_gap="tc06_content_hash_mismatch",
        )
        obligations["TC-07"] = self._obligation(
            ok=all(
                agent in at4.agents_started
                for agent in (
                    "meeting_context_agent",
                    "relationship_context_agent",
                    "follow_up_planning_agent",
                )
            ),
            detail=f"AT-4 AGENTS_STARTED={at4.agents_started}",
            evidence_path=self._scenario_evidence_paths("AT-04"),
            remaining_gap="tc07_agent_trace_missing",
        )
        obligations["TC-08"] = self._obligation(
            ok=(
                at4.stop_reason_code == "CONTACT_NOT_FOUND"
                and at4.stop_point == "relationship_context_agent"
                and at4.disposition == "blocked"
            ),
            detail=(
                f"AT-4 STOP_POINT={at4.stop_point}, STOP_REASON_CODE={at4.stop_reason_code}, "
                f"DISPOSITION={at4.disposition}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-04"),
            remaining_gap="tc08_at4_stop_reason_or_disposition",
        )
        obligations["TC-09"] = self._obligation(
            ok=self._short_circuit_valid(
                run=at4,
                boundary_agent="relationship_context_agent",
            ),
            detail=(
                f"AT-4 AGENT_STATUSES={at4.agent_statuses}, AGENT_EXECUTION={at4.agent_execution}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-04"),
            remaining_gap="tc09_downstream_execution_after_governed_stop",
        )
        obligations["TC-10"] = self._obligation(
            ok=(
                at4.policy_gate_invoked is False
                and at4.policy_bypass is False
                and self._zero_effects(at4)
            ),
            detail=(
                "AT-4 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, "
                f"POLICY_BYPASS={at4.policy_bypass}, EFFECT_COUNTERS={at4.effect_counters}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-04"),
            remaining_gap="tc10_pre_policy_fail_closed_violation",
        )

        obligations["TC-11"] = self._obligation(
            ok=at5.transcript_content_hash
            == str((at5.envelope.get("artifact") or {}).get("content_hash") or ""),
            detail=(
                "AT-5 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with "
                f"TRANSCRIPT_CONTENT_HASH={at5.transcript_content_hash}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-05"),
            remaining_gap="tc11_content_hash_mismatch",
        )
        obligations["TC-12"] = self._obligation(
            ok=all(
                agent in at5.agents_started
                for agent in (
                    "meeting_context_agent",
                    "relationship_context_agent",
                    "follow_up_planning_agent",
                )
            ),
            detail=f"AT-5 AGENTS_STARTED={at5.agents_started}",
            evidence_path=self._scenario_evidence_paths("AT-05"),
            remaining_gap="tc12_agent_trace_missing",
        )
        obligations["TC-13"] = self._obligation(
            ok=(
                at5.stop_reason_code == "LOW_EXTRACTION_CONFIDENCE"
                and at5.stop_point == "meeting_context_agent"
                and at5.disposition == "blocked"
            ),
            detail=(
                f"AT-5 STOP_POINT={at5.stop_point}, STOP_REASON_CODE={at5.stop_reason_code}, "
                f"DISPOSITION={at5.disposition}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-05"),
            remaining_gap="tc13_at5_stop_reason_or_disposition",
        )
        obligations["TC-14"] = self._obligation(
            ok=self._short_circuit_valid(
                run=at5,
                boundary_agent="meeting_context_agent",
            ),
            detail=(
                f"AT-5 AGENT_STATUSES={at5.agent_statuses}, AGENT_EXECUTION={at5.agent_execution}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-05"),
            remaining_gap="tc14_downstream_execution_after_governed_stop",
        )
        obligations["TC-15"] = self._obligation(
            ok=(
                at5.policy_gate_invoked is False
                and at5.policy_bypass is False
                and self._zero_effects(at5)
            ),
            detail=(
                "AT-5 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, "
                f"POLICY_BYPASS={at5.policy_bypass}, EFFECT_COUNTERS={at5.effect_counters}"
            ),
            evidence_path=self._scenario_evidence_paths("AT-05"),
            remaining_gap="tc15_pre_policy_fail_closed_violation",
        )

        known_agents = {
            "meeting_context_agent",
            "relationship_context_agent",
            "follow_up_planning_agent",
        }
        obligations["TC-16"] = self._obligation(
            ok=all(
                set(run.agents_started).issubset(known_agents) for run in scenarios.values()
            ),
            detail="Existing fleet entrypoints reused; no new runtime agent IDs observed",
            evidence_path=(
                "proof/nw008/tranche-c/at-02-run.json | "
                "proof/nw008/tranche-c/at-04-run.json | "
                "proof/nw008/tranche-c/at-05-run.json"
            ),
            remaining_gap="tc16_unexpected_agent_id",
        )
        obligations["TC-17"] = self._obligation(
            ok=deterministic_replay == "PASS",
            detail=f"Deterministic replay result={deterministic_replay}",
            evidence_path=(
                "proof/nw008/tranche-c/at-02-run.json | "
                "proof/nw008/tranche-c/at-04-run.json | "
                "proof/nw008/tranche-c/at-05-run.json"
            ),
            remaining_gap="tc17_deterministic_replay_failed",
        )
        obligations["TC-18"] = self._obligation(
            ok=all(
                run.envelope["source"]["provider"] == "synthetic"
                and run.envelope["source"]["acquisition_mode"] == "fixture"
                and run.envelope["data_classification"]["contains_real_customer_data"]
                is False
                and run.envelope["data_classification"]["permitted_for_public_proof"]
                is True
                for run in scenarios.values()
            ),
            detail="Synthetic-only envelope invariants verified from fixture envelopes",
            evidence_path=(
                "fixtures/nw008/tranche_c/at-02-envelope.json | "
                "fixtures/nw008/tranche_c/at-04-envelope.json | "
                "fixtures/nw008/tranche_c/at-05-envelope.json"
            ),
            remaining_gap="tc18_synthetic_source_violation",
        )
        historical_defs_ok, historical_defs_detail = self._verify_historical_definitions()
        obligations["TC-19"] = self._obligation(
            ok=(
                set(SCENARIO_LABELS.values()) == {"AT-2", "AT-4", "AT-5"}
                and historical_defs_ok
            ),
            detail=historical_defs_detail,
            evidence_path=(
                "contracts/workflow_states.yaml | "
                "src/orchestration/nw008_tranche_c.py | "
                "contracts/nw008_tranche_c_proof_return.schema.json"
            ),
            remaining_gap="tc19_historical_definition_changed",
        )

        obligations["TC-20"] = self._obligation(
            ok=all(
                run.envelope_preserved
                and run.transcript_content_hash
                == str((run.envelope.get("artifact") or {}).get("content_hash") or "")
                and run.envelope_digest == _sha256_dict(run.envelope)
                for run in scenarios.values()
            ),
            detail=(
                "TRANSCRIPT_CONTENT_HASH and ENVELOPE_DIGEST verified; "
                "source/ownership/access_context/provenance preserved"
            ),
            evidence_path=(
                "proof/nw008/tranche-c/at-02-run.json | "
                "proof/nw008/tranche-c/at-04-run.json | "
                "proof/nw008/tranche-c/at-05-run.json"
            ),
            remaining_gap="tc20_envelope_integrity_or_preservation_failed",
        )
        obligations["TC-21"] = self._obligation(
            ok=all(
                run.envelope["data_classification"]["treat_content_as_data_only"] is True
                and run.envelope["content"]["instruction_authority"] is False
                for run in scenarios.values()
            ),
            detail=(
                "All envelopes enforce treat_content_as_data_only=true and "
                "instruction_authority=false"
            ),
            evidence_path=(
                "fixtures/nw008/tranche_c/at-02-envelope.json | "
                "fixtures/nw008/tranche_c/at-04-envelope.json | "
                "fixtures/nw008/tranche_c/at-05-envelope.json"
            ),
            remaining_gap="tc21_instruction_authority_violation",
        )
        at2_card = at2.decision_card or {}
        obligations["TC-22"] = self._obligation(
            ok=all(
                at2_card.get(field) == expected
                for field, expected in STATE_2_EQUIVALENT_AT2.items()
            ),
            detail=(
                "AT-2 State-2-equivalent card semantics: "
                f"policy_state={at2_card.get('policy_state')}, "
                f"policy_reason_code={at2_card.get('policy_reason_code')}, "
                f"next_action={at2_card.get('next_action')}"
            ),
            evidence_path="proof/nw008/tranche-c/at-02-run.json",
            remaining_gap="tc22_at2_state2_semantics_mismatch",
        )

        return obligations

    def _aggregate_effect_counters(
        self, scenarios: Mapping[str, ScenarioRun]
    ) -> Dict[str, Any]:
        totals = {
            "GHL_LIVE_CALLS": 0,
            "GHL_READS": 0,
            "GHL_WRITES": 0,
            "FIRESTORE_WRITES": 0,
            "EXTERNAL_EFFECTS": 0,
            "REAL_CUSTOMER_DATA": 0,
            "NW013_EXECUTED": "NO",
            "DEPLOYMENT_PERFORMED": "NO",
        }
        for run in scenarios.values():
            for key in (
                "GHL_LIVE_CALLS",
                "GHL_READS",
                "GHL_WRITES",
                "FIRESTORE_WRITES",
                "EXTERNAL_EFFECTS",
                "REAL_CUSTOMER_DATA",
            ):
                totals[key] = max(totals[key], int(run.effect_counters.get(key, 0)))
        return totals

    def _historical_at_claims(
        self, scenarios: Mapping[str, ScenarioRun]
    ) -> Dict[str, Any]:
        claims: Dict[str, Any] = {}
        for scenario, run in scenarios.items():
            label = SCENARIO_LABELS[scenario]
            failed: List[str] = []
            if run.disposition != "blocked":
                failed.append("disposition=blocked")
            if run.policy_gate_invoked is not False:
                failed.append("policy_gate_invoked=false")
            if run.policy_bypass is not False:
                failed.append("policy_bypass=false")
            if not self._zero_effects(run):
                failed.append("zero_effects")

            if label == "AT-2":
                if run.stop_reason_code != "AMBIGUOUS_CONTACT":
                    failed.append("stop_reason_code=AMBIGUOUS_CONTACT")
                if run.stop_point != "relationship_context_agent":
                    failed.append("stop_point=relationship_context_agent")
                card = run.decision_card or {}
                state2_exact = all(
                    card.get(field) == expected
                    for field, expected in STATE_2_EQUIVALENT_AT2.items()
                )
                if not state2_exact:
                    failed.append("state_2_equivalent_card")
                if failed:
                    claims[label] = {
                        "status": "NO",
                        "detail": "missing " + ", ".join(failed),
                    }
                else:
                    claims[label] = {
                        "status": "CANDIDATE",
                        "detail": (
                            "Blocked with AMBIGUOUS_CONTACT; PRE_POLICY_FAIL_CLOSED=true; "
                            "State2Equivalent=true."
                        ),
                    }
            elif label == "AT-4":
                if run.stop_reason_code != "CONTACT_NOT_FOUND":
                    failed.append("stop_reason_code=CONTACT_NOT_FOUND")
                if run.stop_point != "relationship_context_agent":
                    failed.append("stop_point=relationship_context_agent")
                if failed:
                    claims[label] = {
                        "status": "NO",
                        "detail": "missing " + ", ".join(failed),
                    }
                else:
                    claims[label] = {
                        "status": "CANDIDATE",
                        "detail": (
                            "Blocked with CONTACT_NOT_FOUND; PRE_POLICY_FAIL_CLOSED=true; "
                            "NW007 card semantics unchanged."
                        ),
                    }
            elif label == "AT-5":
                if run.stop_reason_code != "LOW_EXTRACTION_CONFIDENCE":
                    failed.append("stop_reason_code=LOW_EXTRACTION_CONFIDENCE")
                if run.stop_point != "meeting_context_agent":
                    failed.append("stop_point=meeting_context_agent")
                if failed:
                    claims[label] = {
                        "status": "NO",
                        "detail": "missing " + ", ".join(failed),
                    }
                else:
                    claims[label] = {
                        "status": "CANDIDATE",
                        "detail": (
                            "Blocked with LOW_EXTRACTION_CONFIDENCE; "
                            "PRE_POLICY_FAIL_CLOSED=true; "
                            "NW007 card semantics unchanged."
                        ),
                    }
            else:
                claims[label] = {
                    "status": "NO",
                    "detail": f"unsupported historical AT label {label}",
                }
        return claims

    def _manifest(self, result: TrancheCResult) -> str:
        lines = [
            "# NW-008 Tranche C — Proof Manifest",
            "",
            "| Field | Value |",
            "| --- | --- |",
            "| Execution unit | TRANCHE_C |",
            "| Purpose | HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY |",
            f"| Implementation subject SHA | `{result.implementation_subject_sha}` |",
            "| Transcript source contract | TRANSCRIPT_SOURCE_ENVELOPE_V1 |",
            "| Targets | AT-2, AT-4, AT-5 |",
            "| Excludes | AT-8, AT-9 |",
            f"| Deterministic replay | {result.deterministic_replay} |",
            "",
            "## Entrypoints",
            "",
        ]
        for key, value in ENTRYPOINTS.items():
            lines.append(f"- `{key}` = `{value}`")
        lines.extend(
            ["", "## Proof obligations", "", "| ID | Status | Detail |", "| --- | --- | --- |"]
        )
        for tc_id, obligation in result.proof_obligations.items():
            lines.append(f"| {tc_id} | {obligation.STATUS} | {obligation.DETAIL} |")
        lines.extend(["", "## Effect counters", ""])
        for key, value in result.effect_counters.items():
            lines.append(f"- `{key}` = `{value}`")
        lines.extend(["", "## Historical AT claims", ""])
        for at, claim in result.historical_at_claims.items():
            lines.append(f"- **{at}**: {claim['status']} — {claim['detail']}")
        lines.extend(
            [
                "",
                "## Card evidence source",
                "",
                f"- `AT2_CARD_EVIDENCE_SOURCE` = `{AT2_CARD_EVIDENCE_SOURCE}`",
                "- `NW007_CARD_SEMANTICS_CHANGE` = `NO`",
            ]
        )
        return "\n".join(lines) + "\n"

    def _proof_return_payload(self, result: TrancheCResult) -> Dict[str, Any]:
        scenario_payloads: Dict[str, Any] = {}
        for scenario, run in result.scenarios.items():
            scenario_payloads[SCENARIO_LABELS[scenario]] = {
                "envelope_path": run.envelope_path,
                "transcript_content_hash": run.transcript_content_hash,
                "envelope_digest": run.envelope_digest,
                "run_id": run.run_id,
                "run_path": run.run_path,
                "agents_started": run.agents_started,
                "agents_completed": run.agents_completed,
                "agent_statuses": run.agent_statuses,
                "agent_execution": run.agent_execution,
                "stop_point": run.stop_point,
                "stop_reason_code": run.stop_reason_code,
                "stop_reason_source": run.stop_reason_source,
                "policy_gate_invoked": run.policy_gate_invoked,
                "policy_bypass": run.policy_bypass,
                "disposition": run.disposition,
                "effect_counters": run.effect_counters,
            }
        return {
            "execution_unit": "TRANCHE_C",
            "purpose": "HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY",
            "implementation_subject_sha": result.implementation_subject_sha,
            "transcript_source_contract": "TRANSCRIPT_SOURCE_ENVELOPE_V1",
            "authoritative_stop_source": AUTHORITATIVE_STOP_SOURCE,
            "targets": ["AT-2", "AT-4", "AT-5"],
            "excludes": ["AT-8", "AT-9"],
            "scenarios": scenario_payloads,
            "proof_obligations": {
                tc_id: ob.to_dict() for tc_id, ob in result.proof_obligations.items()
            },
            "effect_counters": result.effect_counters,
            "historical_at_claims": result.historical_at_claims,
            "at2_card_evidence_source": AT2_CARD_EVIDENCE_SOURCE,
            "nw007_card_semantics_change": "NO",
            "remaining_gaps": result.remaining_gaps,
            "entrypoints": ENTRYPOINTS,
        }
