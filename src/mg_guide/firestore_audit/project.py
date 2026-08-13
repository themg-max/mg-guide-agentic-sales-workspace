"""Pure projector: meeting_follow_up_packet_v1 → workflow_run_audit_v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, Mapping, Optional

from .canonicalize import fingerprint_hex
from .models import (
    AUDIT_SCHEMA,
    AUDIT_STATUS_MAPPER_ID,
    IDEMPOTENCY_STRATEGY,
    NON_TERMINAL_STATES,
    PACKET_SCHEMA,
    PROJECTION_VERSION,
    TERMINAL_STATES,
    WORKFLOW_ID,
    ProjectionContext,
)

AUDIT_PROJECTION_INCONSISTENT = "AUDIT_PROJECTION_INCONSISTENT"
AUDIT_INVALID_PACKET = "AUDIT_INVALID_PACKET"
AUDIT_INVALID_WORKFLOW = "AUDIT_INVALID_WORKFLOW"


class AuditProjectionError(ValueError):
    """Fail-closed projection error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def map_terminal_state(run_status: str, final_disposition: Any) -> str:
    """Map packet run.status + audit.final_disposition → terminal_state."""
    if run_status in TERMINAL_STATES:
        if final_disposition != run_status:
            raise AuditProjectionError(
                AUDIT_PROJECTION_INCONSISTENT,
                f"run.status={run_status!r} does not match "
                f"audit.final_disposition={final_disposition!r}",
            )
        return run_status
    if run_status in NON_TERMINAL_STATES:
        if final_disposition not in (None, "pending"):
            raise AuditProjectionError(
                AUDIT_PROJECTION_INCONSISTENT,
                f"non-terminal run.status={run_status!r} requires "
                f"final_disposition pending|null, got {final_disposition!r}",
            )
        return "non_terminal"
    raise AuditProjectionError(
        AUDIT_PROJECTION_INCONSISTENT,
        f"unknown run.status={run_status!r}",
    )


def map_card_state(run_status: str) -> str:
    """Frozen audit-local status mapper (audit_status_mapper_v1).

    Must not import mg_guide.meeting_follow_up_card.
    """
    if run_status in TERMINAL_STATES:
        return run_status
    if run_status in NON_TERMINAL_STATES:
        return "in_progress"
    raise AuditProjectionError(
        AUDIT_PROJECTION_INCONSISTENT,
        f"cannot map card_state for run.status={run_status!r}",
    )


def _require_mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AuditProjectionError(AUDIT_INVALID_PACKET, f"{path} must be an object")
    return value


def _copy_list_of_str(value: Any) -> list:
    if value is None:
        return []
    if not isinstance(value, list):
        raise AuditProjectionError(AUDIT_INVALID_PACKET, "expected list of strings")
    return [str(item) for item in value]


def _packet_external_effects(packet: Mapping[str, Any]) -> int:
    raw = packet.get("external_effects", 0)
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise AuditProjectionError(
            AUDIT_INVALID_PACKET,
            "packet.external_effects must be an integer",
        )
    if raw < 0:
        raise AuditProjectionError(
            AUDIT_INVALID_PACKET,
            "packet.external_effects must be >= 0",
        )
    return raw


def _build_crm_resolution(crm: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "lifecycle": crm.get("lifecycle"),
        "status": crm.get("status"),
        "match_basis": crm.get("match_basis"),
        "candidate_count": crm.get("candidate_count"),
        "contact_id": crm.get("contact_id"),
        "opportunity_id": crm.get("opportunity_id"),
    }


def _build_mutation_intents(intents: Mapping[str, Any]) -> Dict[str, Any]:
    note_out = []
    for item in intents.get("note") or []:
        if not isinstance(item, Mapping):
            raise AuditProjectionError(AUDIT_INVALID_PACKET, "mutation_intents.note item invalid")
        entry: Dict[str, Any] = {
            "kind": item.get("kind"),
            "status": item.get("status"),
        }
        if "body_ref" in item:
            entry["body_ref"] = item.get("body_ref")
        note_out.append(entry)

    stage_out = []
    for item in intents.get("stage") or []:
        if not isinstance(item, Mapping):
            raise AuditProjectionError(AUDIT_INVALID_PACKET, "mutation_intents.stage item invalid")
        entry = {
            "kind": item.get("kind"),
            "status": item.get("status"),
        }
        if "from_stage" in item:
            entry["from_stage"] = item.get("from_stage")
        if "to_stage" in item:
            entry["to_stage"] = item.get("to_stage")
        stage_out.append(entry)

    return {"note": note_out, "stage": stage_out}


def _build_mutations(mutations: Mapping[str, Any]) -> Dict[str, Any]:
    note = _require_mapping(mutations.get("note"), "mutations.note")
    stage = _require_mapping(
        mutations.get("opportunity_stage"), "mutations.opportunity_stage"
    )
    return {
        "lifecycle": mutations.get("lifecycle"),
        "note": {
            "attempted": bool(note.get("attempted")),
            "verified": bool(note.get("verified")),
            "record_id": note.get("record_id"),
        },
        "opportunity_stage": {
            "attempted": bool(stage.get("attempted")),
            "verified": bool(stage.get("verified")),
            "from_stage": stage.get("from_stage"),
            "to_stage": stage.get("to_stage"),
        },
    }


def _build_errors(terminal_state: str, final_disposition: Any, reason_codes: list) -> list:
    if terminal_state != "failed":
        return []
    crumbs = []
    if final_disposition is not None:
        crumbs.append(f"final_disposition={final_disposition}")
    for code in reason_codes:
        crumbs.append(str(code))
    return crumbs


def _projection_input_body(audit_without_clock_and_integrity: Mapping[str, Any]) -> Dict[str, Any]:
    """Packet-derived mapped-input subset for projection_input_fingerprint.

    Excludes writer clock (recorded_at), integrity, and context-only provenance
    fields (fixture_id, source_refs, writer) so idempotency keys track packet
    truth rather than harness metadata.
    """
    prov = audit_without_clock_and_integrity["provenance"]
    return {
        "schema": audit_without_clock_and_integrity["schema"],
        "run_id": audit_without_clock_and_integrity["run_id"],
        "workflow_id": audit_without_clock_and_integrity["workflow_id"],
        "started_at": audit_without_clock_and_integrity["started_at"],
        "completed_at": audit_without_clock_and_integrity["completed_at"],
        "terminal_state": audit_without_clock_and_integrity["terminal_state"],
        "provenance": {
            "packet_schema": prov["packet_schema"],
            "meeting_id": prov["meeting_id"],
            "meeting_source": prov["meeting_source"],
            "transcript_hash": prov["transcript_hash"],
            "packet_run_status": prov["packet_run_status"],
        },
        "agent_steps": audit_without_clock_and_integrity["agent_steps"],
        "policy": audit_without_clock_and_integrity["policy"],
        "reason_codes": audit_without_clock_and_integrity["reason_codes"],
        "tool_call_counts": audit_without_clock_and_integrity["tool_call_counts"],
        "mutation_intents": audit_without_clock_and_integrity["mutation_intents"],
        "mutations": audit_without_clock_and_integrity["mutations"],
        "crm_resolution": audit_without_clock_and_integrity["crm_resolution"],
        "mg_guide_card": audit_without_clock_and_integrity["mg_guide_card"],
        "external_effects": audit_without_clock_and_integrity["external_effects"],
        "warnings": audit_without_clock_and_integrity["warnings"],
        "errors": audit_without_clock_and_integrity["errors"],
        "final_disposition": audit_without_clock_and_integrity["final_disposition"],
        "brief_headline": audit_without_clock_and_integrity["brief_headline"],
        "idempotency": audit_without_clock_and_integrity["idempotency"],
    }


def _content_fingerprint_body(audit_with_recorded_at: Mapping[str, Any]) -> Dict[str, Any]:
    """Immutable audit body for content_fingerprint (excludes recorded_at + integrity)."""
    body = {k: v for k, v in audit_with_recorded_at.items() if k not in {"recorded_at", "integrity"}}
    return body


def project_workflow_run_audit(
    packet: Mapping[str, Any],
    projection_context: ProjectionContext,
    *,
    card_state: Optional[str] = None,
) -> Dict[str, Any]:
    """Pure deterministic projector.

    Same packet + same projection_context ⇒ byte-identical output (including
    fingerprints). Reads no clocks, env, randomness, or I/O.
    """
    if not isinstance(projection_context, ProjectionContext):
        raise AuditProjectionError(
            AUDIT_INVALID_PACKET,
            "projection_context must be a ProjectionContext instance",
        )

    packet = _require_mapping(packet, "packet")
    if packet.get("schema") != PACKET_SCHEMA:
        raise AuditProjectionError(
            AUDIT_INVALID_PACKET,
            f"packet.schema must be {PACKET_SCHEMA}",
        )

    run = _require_mapping(packet.get("run"), "packet.run")
    meeting = _require_mapping(packet.get("meeting"), "packet.meeting")
    audit = _require_mapping(packet.get("audit"), "packet.audit")
    policy = _require_mapping(packet.get("policy"), "packet.policy")
    mutations = _require_mapping(packet.get("mutations"), "packet.mutations")
    mutation_intents = _require_mapping(
        packet.get("mutation_intents"), "packet.mutation_intents"
    )
    crm = _require_mapping(packet.get("crm_resolution"), "packet.crm_resolution")
    brief = packet.get("brief") if isinstance(packet.get("brief"), Mapping) else {}

    run_id = run.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise AuditProjectionError(AUDIT_INVALID_PACKET, "packet.run.run_id is required")

    workflow = run.get("workflow")
    if workflow != WORKFLOW_ID:
        raise AuditProjectionError(
            AUDIT_INVALID_WORKFLOW,
            f"packet.run.workflow must be {WORKFLOW_ID}, got {workflow!r}",
        )

    run_status = run.get("status")
    if not isinstance(run_status, str):
        raise AuditProjectionError(AUDIT_INVALID_PACKET, "packet.run.status is required")

    final_disposition = audit.get("final_disposition")
    terminal_state = map_terminal_state(run_status, final_disposition)

    if card_state is None:
        resolved_card_state = map_card_state(run_status)
    else:
        if card_state not in {
            "completed",
            "completed_with_review",
            "blocked",
            "failed",
            "in_progress",
        }:
            raise AuditProjectionError(
                AUDIT_PROJECTION_INCONSISTENT,
                f"invalid caller-supplied card_state={card_state!r}",
            )
        expected = map_card_state(run_status)
        if card_state != expected:
            raise AuditProjectionError(
                AUDIT_PROJECTION_INCONSISTENT,
                f"caller card_state={card_state!r} disagrees with "
                f"audit_status_mapper_v1 expected={expected!r}",
            )
        resolved_card_state = card_state

    reason_codes = _copy_list_of_str(policy.get("reason_codes"))
    agents_used = _copy_list_of_str(audit.get("agents_used"))
    tools_used = _copy_list_of_str(audit.get("tools_used"))
    warnings = _copy_list_of_str(audit.get("warnings"))
    packet_effects = _packet_external_effects(packet)

    # Competition packets carry integer external_effects and empty tools_used → zeros.
    ghl_reads = 0
    ghl_writes = 0

    draft: Dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "run_id": run_id,
        "workflow_id": WORKFLOW_ID,
        "started_at": audit.get("started_at"),
        "completed_at": audit.get("completed_at"),
        "terminal_state": terminal_state,
        "recorded_at": projection_context.recorded_at,
        "provenance": {
            "packet_schema": PACKET_SCHEMA,
            "meeting_id": meeting.get("meeting_id"),
            "meeting_source": meeting.get("source"),
            "transcript_hash": meeting.get("transcript_hash"),
            "fixture_id": projection_context.fixture_id,
            "packet_run_status": run_status,
            "source_refs": list(projection_context.source_refs),
            "writer": {
                "component": projection_context.writer_component,
                "component_version": projection_context.writer_component_version,
                "projection_version": PROJECTION_VERSION,
                "mode": projection_context.writer_mode,
            },
        },
        "agent_steps": {
            "agents_used": agents_used,
            "tools_used": tools_used,
        },
        "policy": {
            "lifecycle": policy.get("lifecycle"),
            "note_write": policy.get("note_write"),
            "stage_write": policy.get("stage_write"),
            "reason_codes": list(reason_codes),
        },
        "reason_codes": list(reason_codes),
        "tool_call_counts": {
            "tools_listed_count": len(tools_used),
            "ghl_mcp": {
                "reads": ghl_reads,
                "writes": ghl_writes,
            },
            "other": 0,
        },
        "mutation_intents": _build_mutation_intents(mutation_intents),
        "mutations": _build_mutations(mutations),
        "crm_resolution": _build_crm_resolution(crm),
        "mg_guide_card": {
            "card_state": resolved_card_state,
            "projection_source": AUDIT_STATUS_MAPPER_ID,
        },
        "external_effects": {
            "packet_external_effects": packet_effects,
            "counters": {
                "GHL_READS": ghl_reads,
                "GHL_WRITES": ghl_writes,
                "EXTERNAL_EFFECTS": packet_effects,
            },
        },
        "warnings": warnings,
        "errors": _build_errors(terminal_state, final_disposition, reason_codes),
        "final_disposition": final_disposition,
        "brief_headline": brief.get("headline") if brief else None,
        "idempotency": {
            "key": run_id,
            "strategy": IDEMPOTENCY_STRATEGY,
        },
    }

    projection_input_fp = fingerprint_hex(_projection_input_body(draft))
    content_fp = fingerprint_hex(_content_fingerprint_body(draft))

    result = copy.deepcopy(draft)
    result["integrity"] = {
        "projection_input_fingerprint": projection_input_fp,
        "content_fingerprint": content_fp,
    }
    return result
