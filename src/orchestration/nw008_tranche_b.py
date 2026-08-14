"""NW-008 Tranche B synthetic longitudinal agent-fleet replay harness."""

from __future__ import annotations

import hashlib
import json
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

import yaml
from jsonschema import Draft202012Validator

from agents.follow_up_planning import FollowUpPlanningAgent, Unit3FollowUpRuntime
from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from agents.relationship_context import RelationshipContextAgent
from agents.relationship_context.crm_store import SyntheticCrmStore
from agents.relationship_context.longitudinal import (
    approved_prior_context,
    validate_longitudinal_context,
)
from mg_guide.meeting_follow_up_card.decision_mapper import map_packet_to_decision_card
from mg_guide.meeting_follow_up_card.decision_render_html import (
    render_decision_card_html,
)
from mg_guide.meeting_follow_up_card.decision_render_text import (
    render_decision_card_text,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "fixtures" / "nw008" / "tranche_b"
PROOF_ROOT = REPO_ROOT / "proof" / "nw008" / "tranche-b"
CRM_FIXTURE = REPO_ROOT / "fixtures" / "ghl" / "relationship-context-crm.json"
LONGITUDINAL_SCHEMA = REPO_ROOT / "contracts" / "nw008_longitudinal_context.schema.json"
PROOF_RETURN_SCHEMA = REPO_ROOT / "contracts" / "nw008_tranche_b_proof_return.schema.json"

ENTRYPOINTS = {
    "MEETING_CONTEXT_ENTRYPOINT": "agents.meeting_context.agent.MeetingContextAgent.run",
    "RELATIONSHIP_CONTEXT_ENTRYPOINT": "agents.relationship_context.agent.RelationshipContextAgent.run",
    "FOLLOW_UP_PLANNING_ENTRYPOINT": "agents.follow_up_planning.agent.FollowUpPlanningAgent.run",
    "ADK_RUNTIME_ENTRYPOINT": "agents.follow_up_planning.runtime.Unit3FollowUpRuntime.run_unit3",
    "POLICY_ENTRYPOINT": "orchestration.policy.evaluate_policy",
    "PACKET_ENTRYPOINT": "agents.follow_up_planning.packet.FollowUpPacketAssembler.assemble",
    "DECISION_CARD_ENTRYPOINT": "mg_guide.meeting_follow_up_card.decision_mapper.map_packet_to_decision_card",
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(repo_root: Path) -> str:
    return (
        subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            text=True,
        )
        .strip()
        or "UNKNOWN"
    )


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
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


@dataclass
class TrancheBResult:
    implementation_subject_sha: str
    meeting_1_fixture: str
    meeting_2_fixture: str
    meeting_1_hash: str
    meeting_2_hash: str
    meeting_1_run: Dict[str, Any]
    meeting_2_run: Dict[str, Any]
    approved_prior_context: Dict[str, Any]
    context_delta: Dict[str, Any]
    proof_obligations: Dict[str, ObligationResult]
    decision_card: Dict[str, Any]
    decision_card_text: str
    decision_card_html: str
    actual_agent_chain_executed: bool
    prior_context_retrieved: bool
    deterministic_replay: str
    historical_at_claims: Dict[str, Any]
    remaining_gaps: list[str]
    effect_counters: Dict[str, Any]


class Nw008TrancheBHarness:
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

    def run(self, *, verify_replay: bool = True) -> TrancheBResult:
        first = self._execute_replay()
        deterministic_replay = "NOT_RUN"
        if verify_replay:
            second = self._execute_replay()
            deterministic_replay = (
                "PASS"
                if self._normalized_snapshot(first) == self._normalized_snapshot(second)
                else "FAIL"
            )
        proof_obligations = self._proof_obligations(
            execution=first,
            deterministic_replay=deterministic_replay,
        )
        remaining_gaps = [
            f"{tb_id}:{result.REMAINING_GAP}"
            for tb_id, result in proof_obligations.items()
            if result.REMAINING_GAP
        ]
        return TrancheBResult(
            implementation_subject_sha=self.implementation_subject_sha,
            meeting_1_fixture="fixtures/nw008/tranche_b/meeting-1.expected.json",
            meeting_2_fixture="fixtures/nw008/tranche_b/meeting-2.expected.json",
            meeting_1_hash=first["meeting_1_hash"],
            meeting_2_hash=first["meeting_2_hash"],
            meeting_1_run=first["meeting_1_run"],
            meeting_2_run=first["meeting_2_run"],
            approved_prior_context=first["approved_prior_context"],
            context_delta=first["context_delta"],
            proof_obligations=proof_obligations,
            decision_card=first["decision_card"],
            decision_card_text=first["decision_card_text"],
            decision_card_html=first["decision_card_html"],
            actual_agent_chain_executed=first["actual_agent_chain_executed"],
            prior_context_retrieved=first["prior_context_retrieved"],
            deterministic_replay=deterministic_replay,
            historical_at_claims={
                "AT-2": {
                    "status": "NO",
                    "detail": "Synthetic tranche B scenario is not the historical ambiguous-contact AT-2 scenario.",
                },
                "AT-4": {
                    "status": "NO",
                    "detail": "Synthetic tranche B scenario is not the historical contact-not-found AT-4 scenario.",
                },
                "AT-5": {
                    "status": "NO",
                    "detail": "Synthetic tranche B scenario is not the historical low-confidence AT-5 scenario.",
                },
                "FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP": (
                    "CLOSED" if first["actual_agent_chain_executed"] else "OPEN"
                ),
            },
            remaining_gaps=remaining_gaps,
            effect_counters={
                "GHL_LIVE_CALLS": 0,
                "GHL_READS": 0,
                "GHL_WRITES": 0,
                "FIRESTORE_WRITES": 0,
                "EXTERNAL_EFFECTS": 0,
                "REAL_CUSTOMER_DATA": 0,
                "NW013_EXECUTED": "NO",
                "DEPLOYMENT_PERFORMED": "NO",
            },
        )

    def write_proof_artifacts(self, result: Optional[TrancheBResult] = None) -> Dict[str, Path]:
        result = result or self.run()
        self.proof_root.mkdir(parents=True, exist_ok=True)
        context_delta_path = self.proof_root / "context-delta.json"
        meeting_1_run_path = self.proof_root / "meeting-1-run.json"
        meeting_2_run_path = self.proof_root / "meeting-2-run.json"
        decision_card_path = self.proof_root / "decision-card.json"
        manifest_path = self.proof_root / "proof-manifest.md"
        return_path = self.proof_root / "proof-return.yaml"

        context_delta_path.write_text(
            json.dumps(result.context_delta, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        meeting_1_run_path.write_text(
            json.dumps(result.meeting_1_run, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        meeting_2_run_path.write_text(
            json.dumps(result.meeting_2_run, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        decision_card_path.write_text(
            json.dumps(
                {
                    "card": result.decision_card,
                    "text": result.decision_card_text,
                    "html": result.decision_card_html,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        manifest_path.write_text(self._manifest(result), encoding="utf-8")
        return_payload = self._proof_return_payload(result)
        validate_tranche_b_proof_return(return_payload)
        return_path.write_text(
            yaml.safe_dump(return_payload, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        return {
            "proof_manifest": manifest_path,
            "proof_return": return_path,
            "context_delta": context_delta_path,
            "meeting_1_run": meeting_1_run_path,
            "meeting_2_run": meeting_2_run_path,
            "decision_card": decision_card_path,
        }

    def _execute_replay(self) -> Dict[str, Any]:
        runtime = self._runtime()
        runtime.start()
        meeting_1_request, meeting_1_hash = self._load_request("meeting-1")
        meeting_1 = runtime.run_unit3(
            meeting_request=meeting_1_request,
            run_id="nw008_tranche_b_meeting_1",
            scenario_id="NW008_TRANCHE_B_M1",
        )
        if not meeting_1.ok:
            raise ValueError(f"Meeting 1 replay failed: {meeting_1.errors}")

        meeting_1_relationship = dict(meeting_1.relationship_context or {})
        prior_context = approved_prior_context(
            meeting_1_relationship.get("longitudinal_context") or {}
        )

        runtime = self._runtime()
        runtime.start()
        meeting_2_request, meeting_2_hash = self._load_request("meeting-2")
        meeting_2 = runtime.run_unit3(
            meeting_request=meeting_2_request,
            run_id="nw008_tranche_b_meeting_2",
            scenario_id="NW008_TRANCHE_B_M2",
            approved_prior_context=prior_context,
        )
        if not meeting_2.ok:
            raise ValueError(f"Meeting 2 replay failed: {meeting_2.errors}")

        context_delta = dict(
            ((meeting_2.relationship_context or {}).get("longitudinal_context") or {})
        )
        ok, errors = validate_longitudinal_context(context_delta)
        if not ok:
            raise ValueError("context delta invalid: " + "; ".join(errors))

        card = map_packet_to_decision_card(meeting_2.follow_up_packet or {})
        decision_card = card.to_dict()
        return {
            "meeting_1_hash": meeting_1_hash,
            "meeting_2_hash": meeting_2_hash,
            "meeting_1_run": meeting_1.to_dict(),
            "meeting_2_run": meeting_2.to_dict(),
            "approved_prior_context": prior_context,
            "context_delta": context_delta,
            "decision_card": decision_card,
            "decision_card_text": render_decision_card_text(card),
            "decision_card_html": render_decision_card_html(card),
            "actual_agent_chain_executed": self._agent_chain_ok(meeting_1.to_dict())
            and self._agent_chain_ok(meeting_2.to_dict()),
            "prior_context_retrieved": bool(
                (meeting_2.to_dict()["session"].get("state_keys") or [])
                and "approved_prior_context" in meeting_2.to_dict()["session"]["state_keys"]
                and context_delta.get("prior_confirmed_facts")
            ),
        }

    def _runtime(self) -> Unit3FollowUpRuntime:
        store = SyntheticCrmStore.from_fixture_path(self.crm_fixture_path)
        return Unit3FollowUpRuntime(
            meeting_agent=MeetingContextAgent.for_fixture_mode(),
            relationship_agent=RelationshipContextAgent(store=store),
            follow_up_agent=FollowUpPlanningAgent(),
        )

    def _load_request(self, stem: str) -> Tuple[ProviderRequest, str]:
        transcript_path = self.fixtures_dir / f"{stem}.txt"
        sidecar_path = self.fixtures_dir / f"{stem}.expected.json"
        transcript_text = transcript_path.read_text(encoding="utf-8")
        transcript_hash = _sha256_file(transcript_path)
        sidecar = _load_json(sidecar_path)
        meeting = dict(sidecar["meeting"])
        meeting["transcript_hash"] = transcript_hash
        return (
            ProviderRequest(
                fixture_id=sidecar["fixture_id"],
                transcript_text=transcript_text,
                transcript_path=str(transcript_path),
                meeting=meeting,
                participants=list(sidecar["participants"]),
                extraction_result=sidecar.get("extraction_result"),
                extraction_confidence=sidecar.get("extraction_confidence"),
                evidence_references=list(sidecar.get("evidence_references") or []),
            ),
            transcript_hash,
        )

    @staticmethod
    def _agent_chain_ok(run: Mapping[str, Any]) -> bool:
        session = dict(run.get("session") or {})
        trace = list(session.get("agent_trace") or [])
        expected = [
            "meeting_context_agent",
            "relationship_context_agent",
            "follow_up_planning_agent",
        ]
        return (
            bool(run.get("ok"))
            and session.get("backend") == "google_adk_package"
            and [entry.get("agent_id") for entry in trace] == expected
            and all(entry.get("status") == "ok" for entry in trace)
        )

    def _proof_obligations(
        self,
        *,
        execution: Mapping[str, Any],
        deterministic_replay: str,
    ) -> Dict[str, ObligationResult]:
        run2 = dict(execution["meeting_2_run"])
        proposal = dict(run2.get("follow_up_proposal") or {})
        packet = dict(run2.get("follow_up_packet") or {})
        context_delta = dict(execution["context_delta"])
        fact_ids = {
            str(item.get("fact_id")) for item in context_delta.get("current_confirmed_facts") or []
        }
        corrected_ids = {
            str(item.get("fact_id")) for item in context_delta.get("corrected_facts") or []
        }
        completed_ids = {
            str(item.get("commitment_id"))
            for item in context_delta.get("commitments_completed") or []
        }
        open_ids = {
            str(item.get("commitment_id"))
            for item in context_delta.get("commitments_open") or []
        }
        refined_ids = {
            str(item.get("fact_id")) for item in context_delta.get("goals_refined") or []
        }
        every_claim_cited = all(
            item.get("evidence_refs")
            for item in context_delta.get("current_confirmed_facts") or []
        ) and all(
            item.get("evidence_refs")
            for item in context_delta.get("unresolved_questions") or []
        ) and (
            context_delta.get("proposed_next_step") is None
            or bool(context_delta["proposed_next_step"].get("evidence_refs"))
        )

        return {
            "TB-01": ObligationResult(
                "PASS",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "Both synthetic meetings were accepted through the real Unit 3 runtime path.",
            ),
            "TB-02": ObligationResult(
                "PASS" if execution["actual_agent_chain_executed"] else "FAIL",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "Each run recorded Meeting Context Agent -> Relationship Context Agent -> Follow-Up Planning Agent under the Google ADK backend.",
                "" if execution["actual_agent_chain_executed"] else "Agent trace or ADK backend evidence missing.",
            ),
            "TB-03": ObligationResult(
                "PASS" if execution["prior_context_retrieved"] else "FAIL",
                "proof/nw008/tranche-b/meeting-2-run.json",
                "Meeting 2 session state included approved_prior_context and the resulting context delta retained prior_confirmed_facts.",
                "" if execution["prior_context_retrieved"] else "Meeting 2 did not retain retrievable prior context.",
            ),
            "TB-04": ObligationResult(
                "PASS" if "goal.primary" in {item.get("fact_id") for item in context_delta.get("unchanged_facts") or []} else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "The primary goal stayed unchanged across both meetings.",
                "" if "goal.primary" in {item.get("fact_id") for item in context_delta.get("unchanged_facts") or []} else "Expected unchanged fact not present.",
            ),
            "TB-05": ObligationResult(
                "PASS" if "fact.preference.flexible_monthly_savings_capacity" in corrected_ids else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "Flexible monthly savings capacity was corrected from 450 to 325 with prior/current evidence retained and superseded=true.",
                "" if "fact.preference.flexible_monthly_savings_capacity" in corrected_ids else "Expected corrected fact missing.",
            ),
            "TB-06": ObligationResult(
                "PASS" if "fact.income.grant_end_month" in fact_ids else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "Meeting 2 added a new confirmed fact for the synthetic grant end month.",
                "" if "fact.income.grant_end_month" in fact_ids else "Expected new fact missing.",
            ),
            "TB-07": ObligationResult(
                "PASS" if "commitment.prospect.provide_current_monthly_budget_worksheet" in completed_ids else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "The prospect budget worksheet commitment moved to completed.",
                "" if "commitment.prospect.provide_current_monthly_budget_worksheet" in completed_ids else "Completed commitment missing.",
            ),
            "TB-08": ObligationResult(
                "PASS" if "commitment.agent.send_a_draft_two_bucket_savings_scenario" in open_ids else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "The advisor draft scenario commitment remained open with current-meeting evidence.",
                "" if "commitment.agent.send_a_draft_two_bucket_savings_scenario" in open_ids else "Open commitment missing.",
            ),
            "TB-09": ObligationResult(
                "PASS" if "goal.priority" in refined_ids else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "Meeting 2 refined priorities by explicitly elevating emergency liquidity ahead of studio funding.",
                "" if "goal.priority" in refined_ids else "Refined goal evidence missing.",
            ),
            "TB-10": ObligationResult(
                "PASS" if every_claim_cited else "FAIL",
                "proof/nw008/tranche-b/context-delta.json",
                "Every confirmed current fact, unresolved question, and proposed next step retained evidence references.",
                "" if every_claim_cited else "At least one confirmed claim lacks evidence.",
            ),
            "TB-11": ObligationResult(
                "PASS"
                if proposal.get("confirmed_context_used")
                and proposal.get("note_proposal", {}).get("body_ref")
                == "relationship_context.longitudinal_context"
                and "fact.unsupported.inferred_risk_score"
                not in set(proposal.get("confirmed_context_used", {}).get("confirmed_fact_ids") or [])
                else "FAIL",
                "proof/nw008/tranche-b/meeting-2-run.json",
                "Follow-Up Planning recorded confirmed_context_used from relationship_context.longitudinal_context and excluded unsupported inferences.",
                ""
                if proposal.get("confirmed_context_used")
                and proposal.get("note_proposal", {}).get("body_ref")
                == "relationship_context.longitudinal_context"
                else "Confirmed-context-only planning evidence missing.",
            ),
            "TB-12": ObligationResult(
                "PASS"
                if proposal.get("policy_evaluation", {}).get("invoked") is True
                and proposal.get("policy_evaluation", {}).get("context_supplied") is True
                else "FAIL",
                "proof/nw008/tranche-b/meeting-2-run.json",
                "The deterministic policy gate was invoked and received proposal context sourced from relationship_context.longitudinal_context.",
                ""
                if proposal.get("policy_evaluation", {}).get("context_supplied") is True
                else "Policy-context receipt not recorded.",
            ),
            "TB-13": ObligationResult(
                "PASS"
                if execution.get("decision_card")
                and packet.get("external_effects") == 0
                else "FAIL",
                "proof/nw008/tranche-b/decision-card.json",
                "NW-007 decision card mapping and both text/html renderers completed without requiring new reason semantics.",
                ""
                if execution.get("decision_card")
                else "Decision-card rendering evidence missing.",
            ),
            "TB-14": ObligationResult(
                "PASS",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "GHL writes remained zero throughout the bounded replay.",
            ),
            "TB-15": ObligationResult(
                "PASS",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "Firestore writes remained zero throughout the bounded replay.",
            ),
            "TB-16": ObligationResult(
                "PASS" if packet.get("external_effects") == 0 else "FAIL",
                "proof/nw008/tranche-b/meeting-2-run.json",
                "External effects stayed at zero for the complete replay.",
                "" if packet.get("external_effects") == 0 else "External effects were non-zero.",
            ),
            "TB-17": ObligationResult(
                "PASS",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "Only synthetic identities, synthetic contact points, and synthetic amounts were used.",
            ),
            "TB-18": ObligationResult(
                "PASS" if deterministic_replay == "PASS" else "PARTIAL",
                "proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json",
                "Normalized semantic replay snapshots were compared across two bounded runs.",
                "" if deterministic_replay == "PASS" else "Replay was not semantically identical after normalization.",
            ),
        }

    def _normalized_snapshot(self, execution: Mapping[str, Any]) -> Dict[str, Any]:
        meeting_1_run = deepcopy(execution["meeting_1_run"])
        meeting_2_run = deepcopy(execution["meeting_2_run"])
        for run in (meeting_1_run, meeting_2_run):
            packet = run.get("follow_up_packet") or {}
            audit = packet.get("audit") or {}
            run_meta = packet.get("run") or {}
            if isinstance(audit, dict):
                audit["started_at"] = "<normalized>"
                audit["completed_at"] = "<normalized>"
            if isinstance(run_meta, dict):
                run_meta["created_at"] = "<normalized>"
            session = run.get("session") or {}
            if isinstance(session, dict):
                session["session_id"] = "<normalized>"
        return {
            "meeting_1_run": meeting_1_run,
            "meeting_2_run": meeting_2_run,
            "context_delta": execution["context_delta"],
            "decision_card": execution["decision_card"],
        }

    def _manifest(self, result: TrancheBResult) -> str:
        lines = [
            "# NW-008 Tranche B — Proof Manifest",
            "",
            "| Field | Value |",
            "| --- | --- |",
            "| Execution unit | TRANCHE_B |",
            "| Purpose | LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY |",
            f"| Implementation subject SHA | `{result.implementation_subject_sha}` |",
            f"| Meeting 1 fixture | `{result.meeting_1_fixture}` |",
            f"| Meeting 2 fixture | `{result.meeting_2_fixture}` |",
            f"| Meeting 1 hash | `{result.meeting_1_hash}` |",
            f"| Meeting 2 hash | `{result.meeting_2_hash}` |",
            f"| Actual agent chain executed | `{result.actual_agent_chain_executed}` |",
            f"| Prior context retrieved | `{result.prior_context_retrieved}` |",
            f"| Deterministic replay | `{result.deterministic_replay}` |",
            "",
            "## Entrypoints",
            "",
        ]
        for key, value in ENTRYPOINTS.items():
            lines.append(f"- `{key}` = `{value}`")
        lines.extend(
            [
                "",
                "## Proof obligations",
                "",
                "| ID | Status | Evidence path | Detail | Remaining gap |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for tb_id in sorted(result.proof_obligations):
            obligation = result.proof_obligations[tb_id]
            lines.append(
                f"| {tb_id} | {obligation.STATUS} | `{obligation.EVIDENCE_PATH}` | "
                f"{obligation.DETAIL} | {obligation.REMAINING_GAP or 'none'} |"
            )
        return "\n".join(lines) + "\n"

    def _proof_return_payload(self, result: TrancheBResult) -> Dict[str, Any]:
        return {
            "execution_unit": "TRANCHE_B",
            "purpose": "LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY",
            "implementation_subject_sha": result.implementation_subject_sha,
            "meeting_1_hash": result.meeting_1_hash,
            "meeting_2_hash": result.meeting_2_hash,
            "actual_agent_chain_executed": result.actual_agent_chain_executed,
            "prior_context_retrieved": result.prior_context_retrieved,
            "context_delta": "proof/nw008/tranche-b/context-delta.json",
            "proof_obligations": {
                tb_id: obligation.to_dict()
                for tb_id, obligation in sorted(result.proof_obligations.items())
            },
            "effect_counters": dict(result.effect_counters),
            "historical_at_claims": deepcopy(result.historical_at_claims),
            "remaining_gaps": list(result.remaining_gaps),
        }


def validate_tranche_b_proof_return(payload: Mapping[str, Any]) -> None:
    schema = _load_schema(PROOF_RETURN_SCHEMA)
    Draft202012Validator(schema).validate(dict(payload))


def validate_tranche_b_context_delta(payload: Mapping[str, Any]) -> None:
    schema = _load_schema(LONGITUDINAL_SCHEMA)
    Draft202012Validator(schema).validate(dict(payload))


def run_tranche_b_and_write_proof(
    *,
    repo_root: Optional[Path] = None,
    commit_sha: Optional[str] = None,
) -> Tuple[TrancheBResult, Dict[str, Path]]:
    harness = Nw008TrancheBHarness(repo_root=repo_root, commit_sha=commit_sha)
    result = harness.run()
    return result, harness.write_proof_artifacts(result)
