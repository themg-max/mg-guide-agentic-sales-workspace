"""Deterministic fixture runner for meeting_follow_up_v1 Phase 1."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .models import FixtureSidecar, RunRegistry, base_packet
from .policy import bound_intents, evaluate_policy
from .state_machine import StateMachine, TransitionError

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKFLOW = REPO_ROOT / "contracts" / "workflow_states.yaml"
DEFAULT_FIXTURES = REPO_ROOT / "fixtures"


class DuplicateRunError(RuntimeError):
    """Raised when a terminal run_id is replayed."""


@dataclass
class RunResult:
    packet: Dict[str, Any]
    final_state: str
    reason_codes: List[str]
    mutation_intents: Dict[str, List[Dict[str, Any]]]
    external_effects: int
    validation_ok: bool
    rejected_duplicate: bool = False
    error: Optional[str] = None


def _utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _hash_transcript(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def load_sidecar(path: Path) -> FixtureSidecar:
    data = json.loads(path.read_text(encoding="utf-8"))
    return FixtureSidecar.from_dict(data)


class WorkflowRunner:
    def __init__(
        self,
        state_machine: Optional[StateMachine] = None,
        registry: Optional[RunRegistry] = None,
        fixtures_dir: Optional[Path] = None,
    ):
        self.sm = state_machine or StateMachine.from_yaml(DEFAULT_WORKFLOW)
        self.registry = registry or RunRegistry()
        self.fixtures_dir = fixtures_dir or DEFAULT_FIXTURES

    def run_fixture(
        self,
        sidecar_path: Path,
        *,
        run_id_override: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> RunResult:
        sidecar = load_sidecar(sidecar_path)
        run_id = run_id_override or sidecar.run_id

        if self.registry.is_terminal(run_id):
            return RunResult(
                packet={},
                final_state=self.registry.terminal_runs[run_id],
                reason_codes=[],
                mutation_intents={"note": [], "stage": []},
                external_effects=0,
                validation_ok=False,
                rejected_duplicate=True,
                error=f"duplicate run_id rejected: {run_id}",
            )

        ts = created_at or _utc_now()
        meeting = deepcopy(sidecar.meeting)
        # Ensure transcript hash present; prefer sidecar, else hash linked transcript.
        if "transcript_hash" not in meeting or not meeting["transcript_hash"]:
            transcript_name = sidecar.policy_inputs.get(
                "transcript_file", f"{sidecar.fixture_id}.txt"
            )
            tpath = self.fixtures_dir / transcript_name
            if tpath.exists():
                meeting["transcript_hash"] = _hash_transcript(tpath)
            else:
                # Deterministic hash of meeting_id for synthetic isolation.
                meeting["transcript_hash"] = hashlib.sha256(
                    meeting["meeting_id"].encode("utf-8")
                ).hexdigest()

        packet = base_packet(
            run_id=run_id,
            status="received",
            meeting=meeting,
            participants=deepcopy(sidecar.participants),
            created_at=ts,
            started_at=ts,
        )

        try:
            packet = self._advance(packet, "extracting", when="transcript_accepted")
            packet = self._apply_extraction(packet, sidecar)
            conf = packet["evidence"]["extraction_confidence"]
            if conf is None or conf < self.sm.extraction_abort_threshold:
                packet = self._abort_extraction(packet)
                return self._finalize(
                    packet,
                    "blocked",
                    when="extraction_confidence_lt_extraction_abort_threshold",
                    reason_codes=["LOW_EXTRACTION_CONFIDENCE"],
                )

            packet = self._advance(
                packet,
                "resolving",
                when="extraction_confidence_gte_extraction_abort_threshold",
            )
            packet = self._apply_crm(packet, sidecar)
            crm_status = packet["crm_resolution"]["status"]
            if crm_status == "tool_failure":
                return self._finalize(
                    packet,
                    "failed",
                    when="required_crm_resolution_tool_read_failure",
                    reason_codes=["GHL_TOOL_FAILURE"],
                )
            if crm_status == "ambiguous":
                return self._finalize(
                    packet,
                    "blocked",
                    when="contact_ambiguous",
                    reason_codes=["AMBIGUOUS_CONTACT"],
                )
            if crm_status == "not_found":
                return self._finalize(
                    packet,
                    "blocked",
                    when="contact_not_found",
                    reason_codes=["CONTACT_NOT_FOUND"],
                )
            if crm_status == "opportunity_missing":
                return self._finalize(
                    packet,
                    "blocked",
                    when="opportunity_missing",
                    reason_codes=["OPPORTUNITY_NOT_FOUND"],
                )
            if crm_status != "matched":
                raise RuntimeError(f"unexpected crm status: {crm_status}")

            packet = self._advance(
                packet, "evaluating", when="contact_matched_and_opportunity_present"
            )
            decision = evaluate_policy(
                self.sm,
                extraction_confidence=float(conf),
                crm=packet["crm_resolution"],
                policy_inputs=sidecar.policy_inputs,
                extraction_result=sidecar.extraction_result,
            )
            packet["policy"] = {
                "lifecycle": "complete",
                "note_write": decision.note_write,
                "stage_write": decision.stage_write,
                "reason_codes": list(decision.reason_codes),
            }

            if not decision.any_permitted:
                # Ensure NOTE_WRITE_BLOCKED is explicit when note denied and nothing left.
                codes = list(decision.reason_codes)
                if "NOTE_WRITE_BLOCKED" not in codes and decision.note_write == "blocked":
                    codes.append("NOTE_WRITE_BLOCKED")
                packet["policy"]["reason_codes"] = codes
                packet["mutation_intents"] = {"note": [], "stage": []}
                return self._finalize(
                    packet,
                    "blocked",
                    when="note_policy_blocked_and_no_permitted_action_remains",
                    reason_codes=codes,
                )

            packet = self._advance(
                packet, "writing", when="at_least_one_mutation_intent_permitted"
            )
            intents = bound_intents(
                decision,
                max_note=self.sm.max_note_intents,
                max_stage=self.sm.max_stage_intents,
            )
            packet["mutation_intents"] = intents
            packet["mutations"] = {
                "lifecycle": "intent_only",
                "note": {
                    "attempted": False,
                    "verified": False,
                    "record_id": None,
                },
                "opportunity_stage": {
                    "attempted": False,
                    "from_stage": packet["crm_resolution"].get("current_stage"),
                    "to_stage": (
                        intents["stage"][0]["to_stage"] if intents["stage"] else None
                    ),
                    "verified": False,
                },
            }
            # Phase 1: no external mutation execution.
            packet["external_effects"] = 0
            packet = self._apply_brief(packet, decision)

            review_codes = [
                c
                for c in decision.reason_codes
                if c == "STAGE_TRANSITION_NOT_ALLOWED"
            ]
            if review_codes or (
                intents["note"] and not intents["stage"] and decision.stage_write != "allowed"
            ):
                return self._finalize(
                    packet,
                    "completed_with_review",
                    when="note_intent_recorded_and_stage_suppressed_or_review_required",
                    reason_codes=list(decision.reason_codes),
                )
            return self._finalize(
                packet,
                "completed",
                when="intents_recorded_and_no_review_flags",
                reason_codes=list(decision.reason_codes),
            )
        except TransitionError as exc:
            return RunResult(
                packet=packet,
                final_state=packet["run"]["status"],
                reason_codes=[],
                mutation_intents=packet.get("mutation_intents", {"note": [], "stage": []}),
                external_effects=0,
                validation_ok=False,
                error=str(exc),
            )

    def _advance(self, packet: Dict[str, Any], target: str, *, when: str) -> Dict[str, Any]:
        source = packet["run"]["status"]
        self.sm.validate_transition(source, target, when=when)
        packet["run"]["status"] = target
        if target not in {"completed", "completed_with_review", "blocked", "failed"}:
            packet["audit"]["final_disposition"] = "pending"
        return packet

    def _apply_extraction(
        self, packet: Dict[str, Any], sidecar: FixtureSidecar
    ) -> Dict[str, Any]:
        conf = sidecar.extraction_confidence
        packet["evidence"] = {
            "transcript_spans": deepcopy(sidecar.evidence_references),
            "extraction_confidence": conf,
        }
        if conf is not None and conf < self.sm.extraction_abort_threshold:
            packet["extraction"] = {
                "lifecycle": "aborted",
                "summary": None,
                "needs": [],
                "objections": [],
                "commitments": [],
                "next_step": None,
                "opportunity_signal": None,
            }
            packet["audit"]["agents_used"] = ["transcript_extractor:v1"]
            return packet

        result = deepcopy(sidecar.extraction_result or {})
        packet["extraction"] = {
            "lifecycle": "complete",
            "summary": result.get("summary"),
            "needs": list(result.get("needs") or []),
            "objections": list(result.get("objections") or []),
            "commitments": list(result.get("commitments") or []),
            "next_step": result.get("next_step"),
            "opportunity_signal": result.get("opportunity_signal"),
        }
        packet["audit"]["agents_used"] = ["transcript_extractor:v1"]
        return packet

    def _abort_extraction(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        packet["extraction"]["lifecycle"] = "aborted"
        return packet

    def _apply_crm(
        self, packet: Dict[str, Any], sidecar: FixtureSidecar
    ) -> Dict[str, Any]:
        stub = deepcopy(sidecar.crm_resolution_stub)
        status = stub.get("status", "not_found")
        lifecycle = "failed" if status == "tool_failure" else "complete"
        packet["crm_resolution"] = {
            "lifecycle": lifecycle,
            "status": status,
            "contact_id": stub.get("contact_id"),
            "opportunity_id": stub.get("opportunity_id"),
            "match_basis": stub.get("match_basis", "none"),
            "candidate_count": int(stub.get("candidate_count") or 0),
            "current_stage": stub.get("current_stage"),
        }
        agents = list(packet["audit"]["agents_used"])
        if "crm_resolver:v1" not in agents:
            agents.append("crm_resolver:v1")
        packet["audit"]["agents_used"] = agents
        # Phase 1 never records live tool identifiers.
        packet["audit"]["tools_used"] = []
        return packet

    def _apply_brief(self, packet: Dict[str, Any], decision) -> Dict[str, Any]:
        summary = packet["extraction"].get("summary") or ""
        actions = []
        if decision.note_write == "allowed":
            actions.append("plan_note_intent")
        if decision.stage_write == "allowed":
            actions.append("plan_stage_intent")
        attention = bool(decision.reason_codes) or decision.stage_write != "allowed"
        packet["brief"] = {
            "lifecycle": "complete",
            "headline": "Meeting follow-up evaluated (Phase 1 intent-only)",
            "meeting_summary": summary,
            "crm_actions": actions,
            "next_action": (
                packet["extraction"].get("next_step") or {}
            ).get("action")
            if packet["extraction"].get("next_step")
            else "Review follow-up brief",
            "salesperson_attention_required": attention,
        }
        agents = list(packet["audit"]["agents_used"])
        for a in ("followup_evaluator:v1", "crm_action:v1"):
            if a not in agents:
                agents.append(a)
        packet["audit"]["agents_used"] = agents
        return packet

    def _finalize(
        self,
        packet: Dict[str, Any],
        target: str,
        *,
        when: str,
        reason_codes: List[str],
    ) -> RunResult:
        source = packet["run"]["status"]
        self.sm.validate_transition(source, target, when=when)
        packet["run"]["status"] = target
        packet["audit"]["completed_at"] = _utc_now()
        packet["audit"]["final_disposition"] = target
        # Preserve policy reason codes; ensure provided codes present.
        existing = list(packet.get("policy", {}).get("reason_codes") or [])
        merged = existing[:]
        for code in reason_codes:
            if code not in merged:
                merged.append(code)
        if packet.get("policy"):
            packet["policy"]["reason_codes"] = merged
        if target in {"blocked", "failed"} and packet["brief"]["lifecycle"] == "not_attempted":
            packet["brief"] = {
                "lifecycle": "complete",
                "headline": f"Run {target}",
                "meeting_summary": packet["extraction"].get("summary"),
                "crm_actions": [],
                "next_action": "Human review required" if target == "blocked" else "Investigate failure",
                "salesperson_attention_required": True,
            }
        packet["external_effects"] = 0
        self.registry.mark_terminal(packet["run"]["run_id"], target)
        intents = packet.get("mutation_intents") or {"note": [], "stage": []}
        return RunResult(
            packet=packet,
            final_state=target,
            reason_codes=list(packet.get("policy", {}).get("reason_codes") or reason_codes),
            mutation_intents=intents,
            external_effects=0,
            validation_ok=True,
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 1 deterministic meeting_follow_up_v1 runner (no network)"
    )
    parser.add_argument(
        "sidecar",
        help="Path to fixture sidecar JSON (e.g. fixtures/transcript-success.expected.json)",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run_id override",
    )
    args = parser.parse_args(argv)
    runner = WorkflowRunner()
    result = runner.run_fixture(Path(args.sidecar), run_id_override=args.run_id)
    out = {
        "final_state": result.final_state,
        "reason_codes": result.reason_codes,
        "mutation_intents": result.mutation_intents,
        "external_effects": result.external_effects,
        "validation_ok": result.validation_ok,
        "rejected_duplicate": result.rejected_duplicate,
        "error": result.error,
        "packet": result.packet,
    }
    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    if result.rejected_duplicate or not result.validation_ok:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
