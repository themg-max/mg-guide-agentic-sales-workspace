"""Pure projection of packet + card into demo stages and salesperson UX.

No I/O, no CRM, no policy re-evaluation, no agent calls.
Consumes already-produced meeting_follow_up_packet_v1 + CardViewModel dicts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

JSONType = Dict[str, Any]

UX_COMPLETED = "COMPLETED"
UX_NEEDS_REVIEW = "NEEDS_REVIEW"

# Deterministic follow-up draft projection (UX v2). Derived only from already
# approved ux_experience fields; no model invocation, no CRM identifiers.
DRAFT_READY = "READY"
DRAFT_NOT_AVAILABLE = "NOT_AVAILABLE"
FOLLOW_UP_DRAFT_SOURCE = "meeting_follow_up_v1"

# Narrow CRM note display contract. VERIFIED requires explicit durable
# verified-effect evidence from a future live backend response; policy
# permission (note_write=allowed) is never execution proof.
CRM_NOTE_STATUS_DISPLAY: Dict[str, str] = {
    "NOT_EXECUTED": "CRM note not executed in competition mode",
    "BLOCKED": "CRM update blocked. No change performed.",
    "VERIFIED": "CRM note verified",
    "UNKNOWN": "CRM note status unavailable. No CRM change confirmed.",
}

STAGE_SPECS: Sequence[Dict[str, Any]] = (
    {"stage_number": 1, "stage_id": "meeting_ready", "title": "Meeting ready"},
    {"stage_number": 2, "stage_id": "meeting_context", "title": "Meeting Context"},
    {
        "stage_number": 3,
        "stage_id": "relationship_resolution",
        "title": "Relationship Resolution",
    },
    {
        "stage_number": 4,
        "stage_id": "follow_up_planning",
        "title": "Follow-Up Planning",
    },
    {
        "stage_number": 5,
        "stage_id": "policy_evaluation",
        "title": "Policy Evaluation",
    },
    {
        "stage_number": 6,
        "stage_id": "meeting_follow_up_result",
        "title": "Meeting Follow-Up result card",
    },
)

DEMO_TRUTH: JSONType = {
    "LIVE_CRM_EXECUTION": "NOT_PERFORMED",
    "EXTERNAL_EFFECTS": 0,
    "cloud_mutation": "NONE",
    "CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO": True,
    "PRESENTER_MAY_USE_NARRATIVE_ALIAS": False,
    "PRIVATE_MODEL_REASONING_DISPLAYED": False,
}

_REASON_LABELS = {
    "AMBIGUOUS_CONTACT": (
        "Contact resolution returned multiple candidates. Identity must be "
        "confirmed before any CRM write."
    ),
    "STAGE_TRANSITION_NOT_ALLOWED": (
        "The proposed stage change is not permitted by policy. Note follow-up "
        "may still be reviewed offline."
    ),
    "CONTACT_NOT_FOUND": "No matching CRM contact was found for this meeting.",
    "OPPORTUNITY_NOT_FOUND": "No matching CRM opportunity was found.",
    "LOW_EXTRACTION_CONFIDENCE": (
        "Meeting extraction confidence is below the governed threshold."
    ),
    "GHL_TOOL_FAILURE": "A CRM tool call failed; the run failed closed.",
    "GHL_WRITE_NOT_VERIFIED": (
        "A CRM write could not be verified; completion was not declared."
    ),
}


def demo_truth() -> JSONType:
    """Return the constant presenter/judge truth banner (copy-safe)."""
    return dict(DEMO_TRUTH)


def project_demo_stages(
    packet: Mapping[str, Any],
    card: Mapping[str, Any],
    *,
    workflow_status: Optional[str] = None,
) -> List[JSONType]:
    """Project live packet + card into the six presenter-facing stages."""
    meeting = _mapping(packet.get("meeting"))
    participants = _participants(packet.get("participants"))
    extraction = _mapping(packet.get("extraction"))
    evidence = _mapping(packet.get("evidence"))
    crm = _mapping(packet.get("crm_resolution"))
    policy = _mapping(packet.get("policy"))
    audit = _mapping(packet.get("audit"))
    intents = _mapping(card.get("intents_display"))
    framing = _mapping(card.get("framing"))
    brief = _mapping(card.get("brief_display"))
    controls = _mapping(card.get("controls"))
    integrity = _mapping(card.get("integrity"))
    learning = _mapping(card.get("learning"))

    final_disposition = audit.get("final_disposition")
    status = workflow_status or card.get("card_state") or _mapping(packet.get("run")).get("status")

    stages: List[JSONType] = [
        {
            **STAGE_SPECS[0],
            "status": "ready",
            "evidence": {
                "meeting_id": meeting.get("meeting_id"),
                "occurred_at": meeting.get("occurred_at"),
                "source": meeting.get("source"),
                "title": _mapping(card.get("meeting")).get("title")
                or learning.get("summary")
                or "Meeting Follow-Up",
                "participants": participants,
            },
        },
        {
            **STAGE_SPECS[1],
            "status": "complete" if extraction else "empty",
            "evidence": {
                "summary": extraction.get("summary"),
                "needs": _list(extraction.get("needs")),
                "objections": _list(extraction.get("objections")),
                "commitments": _list(extraction.get("commitments")),
                "next_step": extraction.get("next_step")
                if isinstance(extraction.get("next_step"), Mapping)
                else None,
                "extraction_confidence": evidence.get("extraction_confidence"),
            },
        },
        {
            **STAGE_SPECS[2],
            "status": str(crm.get("status") or "unknown"),
            "evidence": {
                "resolution_status": crm.get("status"),
                "match_basis": crm.get("match_basis"),
                "candidate_count": crm.get("candidate_count"),
                "current_stage": crm.get("current_stage"),
                "contact_id": crm.get("contact_id"),
                "opportunity_id": crm.get("opportunity_id"),
            },
        },
        {
            **STAGE_SPECS[3],
            "status": "planned"
            if (_list(intents.get("note")) or _list(intents.get("stage")))
            else "none",
            "evidence": {
                "note_intents": [
                    {"status": i.get("status"), "summary": i.get("summary")}
                    for i in _list(intents.get("note"))
                    if isinstance(i, Mapping)
                ],
                "stage_intents": [
                    {
                        "status": i.get("status"),
                        "summary": i.get("summary"),
                        "from_stage": i.get("from_stage"),
                        "to_stage": i.get("to_stage"),
                    }
                    for i in _list(intents.get("stage"))
                    if isinstance(i, Mapping)
                ],
                "note_execution_attempted": bool(intents.get("note_execution_attempted")),
                "stage_execution_attempted": bool(
                    intents.get("stage_execution_attempted")
                ),
            },
        },
        {
            **STAGE_SPECS[4],
            "status": "evaluated",
            "evidence": {
                "note_write": policy.get("note_write"),
                "stage_write": policy.get("stage_write"),
                "reason_codes": [str(c) for c in _list(policy.get("reason_codes"))],
            },
        },
        {
            **STAGE_SPECS[5],
            "status": str(card.get("card_state") or status or "unknown"),
            "evidence": {
                "card_state": card.get("card_state"),
                "framing": {
                    "tone": framing.get("tone"),
                    "headline": framing.get("headline"),
                    "body": framing.get("body"),
                    "no_crm_changes_made": framing.get("no_crm_changes_made"),
                },
                "brief": {
                    "headline": brief.get("headline"),
                    "next_action": brief.get("next_action"),
                    "salesperson_attention_required": brief.get(
                        "salesperson_attention_required"
                    ),
                },
                "controls": {
                    "allowed_human_actions": _list(
                        controls.get("allowed_human_actions")
                    ),
                    "mutation_controls_enabled": bool(
                        controls.get("mutation_controls_enabled")
                    ),
                },
                "integrity": {
                    "external_effects": integrity.get("external_effects", 0),
                },
                "workflow_status": status,
                "final_disposition": final_disposition,
                "LIVE_CRM_EXECUTION": DEMO_TRUTH["LIVE_CRM_EXECUTION"],
            },
        },
    ]
    return stages


def project_ux_experience(
    packet: Mapping[str, Any],
    card: Mapping[str, Any],
    *,
    workflow_status: Optional[str] = None,
) -> JSONType:
    """Build salesperson-facing COMPLETED / NEEDS_REVIEW experience.

    Operational meaning only — no internal governance noise, no private reasoning.
    Truthful about proposed intents and zero external effects.
    """
    meeting = _mapping(packet.get("meeting"))
    card_meeting = _mapping(card.get("meeting"))
    participants = _participants(packet.get("participants"))
    extraction = _mapping(packet.get("extraction"))
    evidence = _mapping(packet.get("evidence"))
    crm = _mapping(packet.get("crm_resolution"))
    policy = _mapping(packet.get("policy"))
    audit = _mapping(packet.get("audit"))
    intents = _mapping(card.get("intents_display"))
    framing = _mapping(card.get("framing"))
    brief = _mapping(card.get("brief_display"))
    learning = _mapping(card.get("learning"))
    controls = _mapping(card.get("controls"))
    integrity = _mapping(card.get("integrity"))
    run = _mapping(packet.get("run"))

    card_state = str(card.get("card_state") or "")
    status = str(
        workflow_status
        or card_state
        or run.get("status")
        or audit.get("final_disposition")
        or "unknown"
    )
    reason_codes = [str(c) for c in _list(policy.get("reason_codes"))]
    external_effects = 0
    if packet.get("external_effects") is not None:
        try:
            external_effects = int(packet.get("external_effects"))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            external_effects = 0
    elif integrity.get("external_effects") is not None:
        try:
            external_effects = int(integrity.get("external_effects"))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            external_effects = 0

    ux_state = (
        UX_COMPLETED
        if card_state == "completed" and status == "completed"
        else UX_NEEDS_REVIEW
    )

    prospect = next((p for p in participants if p.get("role") == "prospect"), None)
    agent = next((p for p in participants if p.get("role") == "agent"), None)

    meeting_context = {
        "title": card_meeting.get("title") or "Meeting Follow-Up",
        "meeting_id": meeting.get("meeting_id") or card_meeting.get("meeting_id"),
        "occurred_at": meeting.get("occurred_at") or card_meeting.get("occurred_at"),
        "source": meeting.get("source"),
        "prospect": prospect,
        "agent": agent,
    }

    summary = extraction.get("summary") or learning.get("summary")
    relationship_context = {
        "resolution_status": crm.get("status"),
        "match_basis": crm.get("match_basis"),
        "candidate_count": crm.get("candidate_count"),
        "current_stage": crm.get("current_stage"),
        "contact_resolved": crm.get("status") == "matched",
    }

    note_intents = [
        i.get("summary")
        for i in _list(intents.get("note"))
        if isinstance(i, Mapping) and i.get("summary")
    ]
    stage_intents = [
        {
            "summary": i.get("summary"),
            "from_stage": i.get("from_stage"),
            "to_stage": i.get("to_stage"),
        }
        for i in _list(intents.get("stage"))
        if isinstance(i, Mapping)
    ]

    proposed_follow_up = {
        "headline": brief.get("headline"),
        "summary": summary,
        "needs": _list(extraction.get("needs") or learning.get("needs")),
        "objections": _list(extraction.get("objections") or learning.get("objections")),
        "note_intents": note_intents,
        "stage_intents": stage_intents,
        "execution_attempted": {
            "note": bool(intents.get("note_execution_attempted")),
            "stage": bool(intents.get("stage_execution_attempted")),
        },
        "label": "proposed_intents_only",
    }

    policy_decision = {
        "note_write": policy.get("note_write"),
        "stage_write": policy.get("stage_write"),
        "reason_codes": reason_codes,
        "human_review_required": bool(
            brief.get("salesperson_attention_required")
            or ux_state == UX_NEEDS_REVIEW
        ),
    }

    permitted_action_result = {
        "note_write": policy.get("note_write"),
        "stage_write": policy.get("stage_write"),
        "crm_changes_made": False
        if framing.get("no_crm_changes_made") is not False
        else True,
        "external_effects": external_effects,
        "LIVE_CRM_EXECUTION": DEMO_TRUTH["LIVE_CRM_EXECUTION"],
        "cloud_mutation": DEMO_TRUTH["cloud_mutation"],
        "result_label": _result_label(policy, intents, ux_state),
    }

    audit_status = {
        "run_id": run.get("run_id"),
        "workflow": run.get("workflow") or "meeting_follow_up_v1",
        "final_disposition": audit.get("final_disposition") or status,
        "workflow_status": status,
        "agents_used": _list(audit.get("agents_used")),
        "recorded": bool(audit.get("final_disposition") or run.get("run_id")),
        "display": _audit_display(audit, status, external_effects, policy_decision),
    }

    salesperson_next_step = _salesperson_next_step(
        ux_state=ux_state,
        learning=learning,
        brief=brief,
        reason_codes=reason_codes,
        controls=controls,
    )

    base: JSONType = {
        "ux_state": ux_state,
        "meeting_context": meeting_context,
        "summary": summary,
        "relationship_context": relationship_context,
        "proposed_follow_up": proposed_follow_up,
        "policy_decision": policy_decision,
        "permitted_action_result": permitted_action_result,
        "crm_note_status": _crm_note_status(card, ux_state),
        "follow_up_draft": _project_follow_up_draft(
            ux_state=ux_state,
            meeting_context=meeting_context,
            summary=summary,
            proposed_follow_up=proposed_follow_up,
            salesperson_next_step=salesperson_next_step,
        ),
        "audit_status": audit_status,
        "salesperson_next_step": salesperson_next_step,
        "extraction_confidence": evidence.get("extraction_confidence"),
    }

    if ux_state == UX_NEEDS_REVIEW:
        base["needs_review"] = {
            "reason": _human_reason(reason_codes, framing, crm, status),
            "zero_unauthorized_effects": external_effects == 0,
            "zero_unauthorized_effects_message": (
                "No CRM changes were made. Unauthorized effects: 0."
            ),
            "block_context": {
                "resolution_status": crm.get("status"),
                "candidate_count": crm.get("candidate_count"),
                "reason_codes": reason_codes,
                "workflow_status": status,
                "final_disposition": audit.get("final_disposition") or status,
                "note_write": policy.get("note_write"),
                "stage_write": policy.get("stage_write"),
            },
            "explicit_next_action": salesperson_next_step,
        }
    else:
        base["completed"] = {
            "headline": framing.get("headline") or "Follow-up ready",
            "body": framing.get("body")
            or "Governed follow-up intents are prepared for offline review.",
            "contact_resolved": relationship_context["contact_resolved"],
            "proposed_note": bool(note_intents),
            "proposed_stage_change": bool(stage_intents),
            "policy_pass": not reason_codes
            and policy.get("note_write") == "allowed"
            and policy.get("stage_write") == "allowed",
        }

    return base


def project_demo_payload(
    packet: Mapping[str, Any],
    card: Mapping[str, Any],
    *,
    workflow_status: Optional[str] = None,
) -> JSONType:
    """Full additive demo projection attached to the judge response."""
    return {
        "demo_stages": project_demo_stages(
            packet, card, workflow_status=workflow_status
        ),
        "demo_truth": demo_truth(),
        "ux_experience": project_ux_experience(
            packet, card, workflow_status=workflow_status
        ),
    }


def _crm_note_status(card: Mapping[str, Any], ux_state: str) -> JSONType:
    """Narrow CRM note display state for the add-on.

    VERIFIED is reachable only when a future live backend response carries
    explicit durable verified-effect evidence (provider readback) AND live
    execution was performed. Competition mode always resolves to NOT_EXECUTED
    (completed) or BLOCKED (needs review); anything else fails closed to
    UNKNOWN without verified wording.
    """
    effect = _mapping(card.get("crm_effect"))
    live = str(effect.get("LIVE_CRM_EXECUTION") or DEMO_TRUTH["LIVE_CRM_EXECUTION"])
    verified_evidence = (
        effect.get("verified") is True
        and effect.get("evidence") == "provider_readback"
    )
    if live == "PERFORMED" and verified_evidence:
        state = "VERIFIED"
    elif ux_state == UX_NEEDS_REVIEW:
        state = "BLOCKED"
    elif live == "NOT_PERFORMED":
        state = "NOT_EXECUTED"
    else:
        state = "UNKNOWN"
    return {"state": state, "display": CRM_NOTE_STATUS_DISPLAY[state]}


def _project_follow_up_draft(
    *,
    ux_state: str,
    meeting_context: Mapping[str, Any],
    summary: Any,
    proposed_follow_up: Mapping[str, Any],
    salesperson_next_step: Any,
) -> JSONType:
    """Deterministic Gmail follow-up draft from approved UX fields only.

    Permitted inputs: prospect name/email, agent name, meeting title, summary,
    proposed follow-up summary, salesperson next step. Never raw CRM IDs,
    provider responses, secrets, or private reasoning. The human sender is
    always the only sender (requires_human_send=True); the add-on compose
    action only ever creates an editable draft.
    """
    draft: JSONType = {
        "status": DRAFT_NOT_AVAILABLE,
        "recipient_name": None,
        "recipient_email": None,
        "subject": None,
        "body_text": None,
        "source": FOLLOW_UP_DRAFT_SOURCE,
        "requires_human_send": True,
    }
    # A blocked or ambiguous relationship never gets a draft.
    if ux_state != UX_COMPLETED:
        return draft
    prospect = _mapping(meeting_context.get("prospect"))
    agent = _mapping(meeting_context.get("agent"))
    recipient_email = str(prospect.get("email") or "").strip()
    if not recipient_email:
        return draft
    recipient_name = str(prospect.get("name") or "").strip()
    draft["recipient_name"] = recipient_name or None
    draft["recipient_email"] = recipient_email
    title = str(meeting_context.get("title") or "").strip() or "Meeting Follow-Up"
    draft["subject"] = _draft_subject(title)
    paragraph = str(proposed_follow_up.get("summary") or summary or "").strip()
    if not paragraph:
        paragraph = "It was a pleasure connecting with you."
    next_step = str(salesperson_next_step or "").strip()
    if not next_step:
        next_step = "We will confirm the next step offline."
    draft["body_text"] = _draft_body(
        recipient_first_name=_first_name(recipient_name),
        paragraph=paragraph,
        next_step=next_step,
        agent_first_name=_first_name(str(agent.get("name") or "").strip())
        or "MG Guide",
    )
    draft["status"] = DRAFT_READY
    return draft


def _draft_subject(title: str) -> str:
    clean = " ".join(str(title).split())[:120].strip() or "Meeting Follow-Up"
    return f"Follow-up: {clean}"


def _draft_body(
    *,
    recipient_first_name: str,
    paragraph: str,
    next_step: str,
    agent_first_name: str,
) -> str:
    greeting = recipient_first_name or "there"
    return (
        f"Hi {greeting},\n\n"
        "Thank you for your time today.\n\n"
        f"{paragraph}\n\n"
        "Next step:\n"
        f"{next_step}\n\n"
        "Please let me know if I missed anything or if you would like to "
        "adjust the next step.\n\n"
        "Best,\n"
        f"{agent_first_name}"
    )


def _first_name(name: Optional[str]) -> str:
    if not name:
        return ""
    parts = str(name).strip().split()
    return parts[0] if parts else ""


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, list) else []


def _participants(value: Any) -> List[JSONType]:
    out: List[JSONType] = []
    if not isinstance(value, list):
        return out
    for item in value:
        if not isinstance(item, Mapping):
            continue
        out.append(
            {
                "name": item.get("name"),
                "email": item.get("email"),
                "phone": item.get("phone"),
                "role": item.get("role"),
            }
        )
    return out


def _result_label(
    policy: Mapping[str, Any], intents: Mapping[str, Any], ux_state: str
) -> str:
    if ux_state == UX_NEEDS_REVIEW:
        codes = _list(policy.get("reason_codes"))
        if "AMBIGUOUS_CONTACT" in codes:
            return "blocked_before_crm_write"
        if policy.get("stage_write") in {"blocked", "approval_required", "not_attempted"}:
            return "review_required_before_stage_change"
        return "needs_review_zero_effects"
    note_planned = bool(_list(intents.get("note")))
    stage_planned = bool(_list(intents.get("stage")))
    if note_planned and stage_planned:
        return "note_and_stage_intents_permitted"
    if note_planned:
        return "note_intent_permitted"
    return "follow_up_prepared"


def _audit_display(
    audit: Mapping[str, Any],
    status: str,
    external_effects: int,
    policy_decision: Mapping[str, Any],
) -> str:
    agents = _list(audit.get("agents_used"))
    agent_count = len(agents) if agents else 0
    tools = _list(audit.get("tools_used"))
    tool_count = len(tools)
    policy_pass = "PASS" if not _list(policy_decision.get("reason_codes")) else "REVIEW"
    if status in {"blocked", "failed"}:
        policy_pass = "FAIL_CLOSED"
    parts = []
    if agent_count:
        parts.append(f"{agent_count} agents")
    if tool_count:
        parts.append(f"{tool_count} governed tool calls")
    else:
        parts.append("governed offline path")
    parts.append(f"policy {policy_pass}")
    parts.append("audit recorded" if audit.get("final_disposition") else "audit pending")
    parts.append(f"external_effects={external_effects}")
    return " · ".join(parts)


def _human_reason(
    reason_codes: Sequence[str],
    framing: Mapping[str, Any],
    crm: Mapping[str, Any],
    status: str,
) -> str:
    for code in reason_codes:
        if code in _REASON_LABELS:
            return _REASON_LABELS[code]
    if crm.get("status") == "ambiguous":
        count = crm.get("candidate_count")
        return (
            f"Contact resolution returned {count} candidates. "
            "No CRM changes were made."
        )
    body = framing.get("body")
    if isinstance(body, str) and body.strip():
        return body.strip()
    headline = framing.get("headline")
    if isinstance(headline, str) and headline.strip():
        return headline.strip()
    return f"Follow-up requires review (status: {status})."


def _salesperson_next_step(
    *,
    ux_state: str,
    learning: Mapping[str, Any],
    brief: Mapping[str, Any],
    reason_codes: Sequence[str],
    controls: Mapping[str, Any],
) -> str:
    brief_next = brief.get("next_action")
    learning_action = learning.get("next_step_action")
    owner = learning.get("next_step_owner")

    if ux_state == UX_COMPLETED:
        if isinstance(learning_action, str) and learning_action.strip():
            if isinstance(owner, str) and owner.strip():
                return f"{learning_action} (owner: {owner})"
            return learning_action
        if isinstance(brief_next, str) and brief_next.strip():
            return brief_next
        return "Review prepared note and stage intents offline."

    if "AMBIGUOUS_CONTACT" in reason_codes:
        return "Resolve contact identity offline before any CRM write."
    if "STAGE_TRANSITION_NOT_ALLOWED" in reason_codes:
        return "Keep current stage and review the note intent offline."
    actions = _list(controls.get("allowed_human_actions"))
    if "escalate_offline" in actions:
        if isinstance(brief_next, str) and brief_next.strip():
            return brief_next
        return "Escalate offline — no CRM write was attempted."
    if isinstance(brief_next, str) and brief_next.strip():
        return brief_next
    if isinstance(learning_action, str) and learning_action.strip():
        return learning_action
    return "Review required before any further action."
