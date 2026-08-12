"""Deterministic packet -> card mapper for NW-006."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping

from jsonschema import Draft202012Validator

from .models import CARD_SCHEMA, MAPPER_ID, SOURCE_SCHEMA, CardViewModel, IntentDisplay, intent_to_dict

TERMINAL_STATES = {"completed", "completed_with_review", "blocked", "failed"}
NON_TERMINAL_STATES = {"received", "extracting", "resolving", "evaluating", "writing"}
VALID_MUTATION_LIFECYCLES = {"not_attempted", "intent_only"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def _packet_validator() -> Draft202012Validator:
    schema_path = _repo_root() / "contracts" / "meeting_follow_up_packet.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _error_messages(errors: List[Any]) -> List[str]:
    messages = []
    for error in errors:
        path = ".".join(str(p) for p in error.path) or "<root>"
        messages.append(f"{path}: {error.message}")
    return messages


def _invariant_violations(packet: Mapping[str, Any]) -> List[str]:
    mutations = packet.get("mutations") if isinstance(packet.get("mutations"), Mapping) else {}
    note = mutations.get("note") if isinstance(mutations.get("note"), Mapping) else {}
    stage = (
        mutations.get("opportunity_stage")
        if isinstance(mutations.get("opportunity_stage"), Mapping)
        else {}
    )
    violations: List[str] = []
    if packet.get("external_effects") != 0:
        violations.append("packet.external_effects must be 0")
    if mutations.get("lifecycle") not in VALID_MUTATION_LIFECYCLES:
        violations.append("packet.mutations.lifecycle must be not_attempted or intent_only")
    if note.get("attempted") is not False:
        violations.append("packet.mutations.note.attempted must be false")
    if note.get("verified") is not False:
        violations.append("packet.mutations.note.verified must be false")
    if stage.get("attempted") is not False:
        violations.append("packet.mutations.opportunity_stage.attempted must be false")
    if stage.get("verified") is not False:
        violations.append("packet.mutations.opportunity_stage.verified must be false")
    return violations


def _human_actions(card_state: str) -> List[str]:
    if card_state == "completed":
        return ["acknowledge", "copy_note_text_offline"]
    if card_state == "completed_with_review":
        return ["acknowledge", "copy_note_text_offline", "escalate_offline"]
    if card_state in {"blocked", "failed"}:
        return ["escalate_offline"]
    return ["wait"]


def _framing(
    status: str,
    *,
    out_of_scope: bool = False,
    invalid_input: bool = False,
) -> Dict[str, Any]:
    # no_crm_changes_made always describes this card path (never upstream CRM claims).
    card_did_not_mutate = True
    if out_of_scope:
        return {
            "tone": "failed",
            "headline": "Follow-up input out of scope",
            "body": (
                "Input is outside the NW-006 zero-effect display envelope. "
                "This card did not perform CRM changes."
            ),
            "no_crm_changes_made": card_did_not_mutate,
        }
    if invalid_input and status == "failed":
        return {
            "tone": "failed",
            "headline": "Follow-up input invalid",
            "body": (
                "Card input could not be mapped under NW-006 rules. "
                "This card did not perform CRM changes."
            ),
            "no_crm_changes_made": card_did_not_mutate,
        }
    if status == "completed":
        return {
            "tone": "success",
            "headline": "Follow-up card ready",
            "body": "Deterministic follow-up intents are prepared for offline review.",
            "no_crm_changes_made": card_did_not_mutate,
        }
    if status == "completed_with_review":
        return {
            "tone": "review",
            "headline": "Follow-up requires review",
            "body": "Policy reason codes indicate human review is required before any downstream action.",
            "no_crm_changes_made": card_did_not_mutate,
        }
    if status == "blocked":
        return {
            "tone": "blocked",
            "headline": "Follow-up blocked",
            "body": "No CRM changes were made by this card.",
            "no_crm_changes_made": card_did_not_mutate,
        }
    if status == "failed":
        return {
            "tone": "failed",
            "headline": "Follow-up failed",
            "body": (
                "Rendering is constrained to packet output only. "
                "This card did not perform CRM changes."
            ),
            "no_crm_changes_made": card_did_not_mutate,
        }
    return {
        "tone": "in_progress",
        "headline": "Follow-up not ready",
        "body": "Packet status is non-terminal.",
        "no_crm_changes_made": card_did_not_mutate,
    }


def _meeting_title(packet: Mapping[str, Any]) -> str:
    participants = packet.get("participants")
    if isinstance(participants, list):
        for participant in participants:
            if isinstance(participant, Mapping) and participant.get("role") == "prospect":
                name = participant.get("name")
                if isinstance(name, str) and name:
                    return f"{name} - Discovery Meeting"
    return "Meeting Follow-Up"


def _intent_summary(intent: Mapping[str, Any]) -> str:
    kind = str(intent.get("kind") or "intent")
    status = str(intent.get("status") or "unknown")
    if kind == "stage":
        from_stage = intent.get("from_stage")
        to_stage = intent.get("to_stage")
        return f"Stage intent {status}: {from_stage or 'unknown'} -> {to_stage or 'unknown'}"
    body_ref = intent.get("body_ref")
    if body_ref:
        return f"Note intent {status}: source {body_ref}"
    return f"Note intent {status}"


def _build_intents(packet: Mapping[str, Any]) -> Dict[str, Any]:
    mutation_intents = (
        packet.get("mutation_intents")
        if isinstance(packet.get("mutation_intents"), Mapping)
        else {"note": [], "stage": []}
    )
    note_intents = mutation_intents.get("note")
    stage_intents = mutation_intents.get("stage")

    notes: List[Dict[str, Any]] = []
    if isinstance(note_intents, list):
        for intent in note_intents:
            if not isinstance(intent, Mapping):
                continue
            notes.append(
                intent_to_dict(
                    IntentDisplay(
                        kind="note",
                        status=intent.get("status") if isinstance(intent.get("status"), str) else None,
                        summary=_intent_summary(intent),
                        from_stage=None,
                        to_stage=None,
                    )
                )
            )

    stages: List[Dict[str, Any]] = []
    if isinstance(stage_intents, list):
        for intent in stage_intents:
            if not isinstance(intent, Mapping):
                continue
            stages.append(
                intent_to_dict(
                    IntentDisplay(
                        kind="stage",
                        status=intent.get("status") if isinstance(intent.get("status"), str) else None,
                        summary=_intent_summary(intent),
                        from_stage=intent.get("from_stage")
                        if isinstance(intent.get("from_stage"), str)
                        else None,
                        to_stage=intent.get("to_stage")
                        if isinstance(intent.get("to_stage"), str)
                        else None,
                    )
                )
            )

    mutations = packet.get("mutations") if isinstance(packet.get("mutations"), Mapping) else {}
    note_mutation = mutations.get("note") if isinstance(mutations.get("note"), Mapping) else {}
    stage_mutation = (
        mutations.get("opportunity_stage")
        if isinstance(mutations.get("opportunity_stage"), Mapping)
        else {}
    )
    return {
        "note": notes,
        "stage": stages,
        "note_execution_attempted": bool(note_mutation.get("attempted")),
        "stage_execution_attempted": bool(stage_mutation.get("attempted")),
    }


def map_packet_to_card(packet: Mapping[str, Any]) -> Dict[str, Any]:
    data = dict(packet)
    ui_errors: List[str] = []
    schema_errors = sorted(
        _packet_validator().iter_errors(data),
        key=lambda err: tuple(str(p) for p in err.absolute_path),
    )
    if schema_errors:
        ui_errors.append("CARD_INPUT_INVALID")

    status = (
        data.get("run", {}).get("status")
        if isinstance(data.get("run"), Mapping)
        else None
    )
    if not isinstance(status, str) or status not in TERMINAL_STATES | NON_TERMINAL_STATES:
        if "CARD_INPUT_INVALID" not in ui_errors:
            ui_errors.append("CARD_INPUT_INVALID")
        status = "failed"

    invariant_violations = _invariant_violations(data)
    out_of_scope = bool(invariant_violations)
    if out_of_scope:
        ui_errors.append("CARD_INPUT_OUT_OF_SCOPE")
        status = "failed"

    card_state = status if status in TERMINAL_STATES else "in_progress"
    if status == "failed":
        card_state = "failed"

    meeting = data.get("meeting") if isinstance(data.get("meeting"), Mapping) else {}
    run = data.get("run") if isinstance(data.get("run"), Mapping) else {}
    crm_resolution = (
        data.get("crm_resolution") if isinstance(data.get("crm_resolution"), Mapping) else {}
    )
    extraction = data.get("extraction") if isinstance(data.get("extraction"), Mapping) else {}
    policy = data.get("policy") if isinstance(data.get("policy"), Mapping) else {}
    brief = data.get("brief") if isinstance(data.get("brief"), Mapping) else {}
    reason_codes = policy.get("reason_codes") if isinstance(policy.get("reason_codes"), list) else []

    attention = brief.get("salesperson_attention_required")
    if attention is not None and not isinstance(attention, bool):
        attention = None

    card = CardViewModel(
        schema=CARD_SCHEMA,
        card_state=card_state,
        run={
            "run_id": run.get("run_id"),
            "workflow": run.get("workflow"),
            "packet_status": run.get("status"),
            "created_at": run.get("created_at"),
        },
        meeting={
            "meeting_id": meeting.get("meeting_id"),
            "occurred_at": meeting.get("occurred_at"),
            "title": _meeting_title(data),
        },
        framing=_framing(
            card_state,
            out_of_scope=out_of_scope,
            invalid_input="CARD_INPUT_INVALID" in ui_errors and not out_of_scope,
        ),
        policy_display={
            "note_write": policy.get("note_write"),
            "stage_write": policy.get("stage_write"),
            "reason_codes": [str(code) for code in reason_codes],
        },
        ui_integrity={
            "errors": ui_errors,
            "schema_validation_errors": _error_messages(schema_errors),
            "invariant_violations": invariant_violations,
        },
        crm_display={
            "resolution_status": crm_resolution.get("status"),
            "match_basis": crm_resolution.get("match_basis"),
            "candidate_count": crm_resolution.get("candidate_count"),
            "current_stage": crm_resolution.get("current_stage"),
        },
        metadata={
            "contact_id": crm_resolution.get("contact_id"),
            "opportunity_id": crm_resolution.get("opportunity_id"),
        },
        learning={
            "summary": extraction.get("summary"),
            "needs": extraction.get("needs") if isinstance(extraction.get("needs"), list) else [],
            "objections": extraction.get("objections")
            if isinstance(extraction.get("objections"), list)
            else [],
            "next_step_action": (
                extraction.get("next_step", {}).get("action")
                if isinstance(extraction.get("next_step"), Mapping)
                else None
            ),
            "next_step_owner": (
                extraction.get("next_step", {}).get("owner")
                if isinstance(extraction.get("next_step"), Mapping)
                else None
            ),
        },
        intents_display=_build_intents(data),
        brief_display={
            "headline": brief.get("headline"),
            "next_action": brief.get("next_action"),
            "crm_actions": brief.get("crm_actions")
            if isinstance(brief.get("crm_actions"), list)
            else [],
            "salesperson_attention_required": attention,
        },
        controls={
            "mutation_controls_enabled": False,
            "agent_rerun_enabled": False,
            "policy_reeval_enabled": False,
            "allowed_human_actions": _human_actions(card_state),
        },
        integrity={
            "external_effects": 0,
            "source_schema": SOURCE_SCHEMA,
            "mapper_id": MAPPER_ID,
        },
    )
    return card.to_dict()

