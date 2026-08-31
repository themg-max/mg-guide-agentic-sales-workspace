"""Pure CardService view-model projection from judge /demo/meeting-follow-up JSON.

No CRM, no policy re-evaluation, no agent calls. Apps Script renders the same
fields; this module is the testable contract for judge-visible content.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

JSONType = Dict[str, Any]

PRODUCT_NAME = "MG Guide"
PRODUCT_ATTRIBUTION = "Powered by AI Rolodex"
PRIMARY_CAPABILITY = "Meeting Follow-Up"

ERROR_AUTH = "AUTH_ERROR"
ERROR_BACKEND = "BACKEND_UNAVAILABLE"
ERROR_INVALID = "INVALID_RESPONSE"
ERROR_SCENARIO_BLOCKED = "SCENARIO_BLOCKED"

PRIMARY_SCENARIOS = ("SUCCESS", "AMBIGUOUS_CONTACT")
OPTIONAL_SCENARIOS = ("STAGE_CHANGE_DENIED",)

# Narrow CRM note display contract (mirrors the backend truth emitted in
# ux_experience.crm_note_status). VERIFIED wording is only ever rendered when
# the backend reports live execution with durable verified-effect evidence.
CRM_NOTE_STATUS_DISPLAY = {
    "NOT_EXECUTED": "CRM note not executed in competition mode",
    "BLOCKED": "CRM update blocked. No change performed.",
    "VERIFIED": "CRM note verified",
    "UNKNOWN": "CRM note status unavailable. No CRM change confirmed.",
}

DRAFT_COMPOSE_FUNCTION = "createFollowUpDraft"
DRAFT_COMPOSE_BUTTON_TEXT = "Open Draft in Gmail"

STAGE_TITLES = (
    "Meeting ready",
    "Meeting Context",
    "Relationship Resolution",
    "Follow-Up Planning",
    "Policy Evaluation",
    "Meeting Follow-Up result",
)


def project_cardservice_home() -> JSONType:
    """Homepage card model: product-first Meeting Follow-Up experience.

    The primary call to action is the salesperson journey; judge-only
    fail-closed scenarios live in a separate secondary section.
    """
    return {
        "card_id": "mg_guide_home",
        "header": {
            "title": PRODUCT_NAME,
            "subtitle": PRODUCT_ATTRIBUTION,
        },
        "sections": [
            {
                "header": PRIMARY_CAPABILITY,
                "widgets": [
                    {
                        "type": "text",
                        "text": (
                            f"<b>{PRIMARY_CAPABILITY}</b><br>"
                            "Turn a completed meeting into relationship context, "
                            "CRM-ready documentation, and a follow-up draft."
                        ),
                    },
                    {
                        "type": "text",
                        "text": (
                            "<b>Competition mode</b><br>"
                            "Approved synthetic transcript · governed CRM boundary"
                        ),
                    },
                    {
                        "type": "button",
                        "text": "Process Meeting Follow-Up",
                        "action": "runScenario",
                        "parameters": {"scenario": "SUCCESS"},
                        "style": "filled",
                    },
                ],
            },
            {
                "header": "Judge test scenarios",
                "widgets": [
                    {
                        "type": "text",
                        "text": (
                            "Fail-closed test scenarios for judges. "
                            "No CRM writes on this path."
                        ),
                    },
                    {
                        "type": "button",
                        "text": "Ambiguous contact",
                        "action": "runScenario",
                        "parameters": {"scenario": "AMBIGUOUS_CONTACT"},
                        "style": "text",
                    },
                    {
                        "type": "button",
                        "text": "Policy guardrail",
                        "action": "runScenario",
                        "parameters": {"scenario": "STAGE_CHANGE_DENIED"},
                        "style": "text",
                    },
                ],
            },
        ],
        "fixed_footer": {
            "primary_text": PRODUCT_NAME,
            "secondary_text": PRODUCT_ATTRIBUTION,
        },
    }


def project_error_card(
    code: str,
    message: str,
    *,
    external_effects: int = 0,
) -> JSONType:
    """Fail-visible error card. Never implies a mutation occurred."""
    human = {
        ERROR_AUTH: "Authentication failed. Sign in with the controlled judge Workspace account and retry.",
        ERROR_BACKEND: "MG Guide backend is unavailable. No CRM changes were made.",
        ERROR_INVALID: "The backend returned an invalid response. No CRM changes were made.",
        ERROR_SCENARIO_BLOCKED: "That scenario is not available on the judge path. No CRM changes were made.",
    }.get(code, message)
    return {
        "card_id": "mg_guide_error",
        "header": {"title": PRODUCT_NAME, "subtitle": PRODUCT_ATTRIBUTION},
        "error": {
            "code": code,
            "message": human,
            "external_effects": external_effects,
            "crm_mutations_performed": False,
            "LIVE_CRM_EXECUTION": "NOT_PERFORMED",
        },
        "sections": [
            {
                "header": f"Error · {code}",
                "widgets": [
                    {"type": "text", "text": human},
                    {
                        "type": "key_value",
                        "top_label": "external_effects",
                        "content": str(external_effects),
                    },
                    {
                        "type": "key_value",
                        "top_label": "LIVE_CRM_EXECUTION",
                        "content": "NOT_PERFORMED",
                    },
                    {
                        "type": "text",
                        "text": "No CRM changes were made.",
                    },
                    {
                        "type": "button",
                        "text": "Back to MG Guide home",
                        "action": "showHome",
                        "parameters": {},
                        "style": "text",
                    },
                ],
            }
        ],
    }


def project_cardservice_result(judge_response: Mapping[str, Any]) -> JSONType:
    """Project a successful judge JSON body into CardService sections."""
    if not isinstance(judge_response, Mapping):
        return project_error_card(ERROR_INVALID, "Response is not an object.")

    required = (
        "scenario",
        "workflow_status",
        "policy_decision",
        "demo_stages",
        "ux_experience",
        "external_effects",
        "demo_truth",
    )
    missing = [k for k in required if k not in judge_response]
    if missing:
        return project_error_card(
            ERROR_INVALID, f"Missing fields: {', '.join(missing)}"
        )

    ux = _mapping(judge_response.get("ux_experience"))
    stages = judge_response.get("demo_stages")
    if not isinstance(stages, list) or len(stages) != 6:
        return project_error_card(ERROR_INVALID, "demo_stages must contain 6 stages.")

    ux_state = str(ux.get("ux_state") or "")
    scenario = str(judge_response.get("scenario") or "")
    workflow_status = str(judge_response.get("workflow_status") or "")
    policy = _mapping(judge_response.get("policy_decision"))
    audit = _mapping(judge_response.get("audit_summary"))
    ux_audit = _mapping(ux.get("audit_status"))
    truth = _mapping(judge_response.get("demo_truth"))
    external_effects = _as_int(judge_response.get("external_effects"), default=0)
    live_crm = str(
        truth.get("LIVE_CRM_EXECUTION")
        or _mapping(ux.get("permitted_action_result")).get("LIVE_CRM_EXECUTION")
        or "NOT_PERFORMED"
    )
    crm_note_status = _crm_note_status_view(ux)
    draft = _mapping(ux.get("follow_up_draft"))
    draft_ready = ux_state == "COMPLETED" and str(draft.get("status")) == "READY"

    sections: List[JSONType] = []
    if ux_state == "NEEDS_REVIEW":
        sections.append(_needs_review_overview_section(ux, crm_note_status))
    else:
        sections.append(_follow_up_ready_section(ux, draft, crm_note_status))
    sections.append(_processing_status_section(ux_state, workflow_status, stages))
    sections.append(_what_we_heard_section(ux))
    sections.append(_relationship_section(ux))
    sections.append(_crm_section(ux, crm_note_status))
    if draft_ready:
        sections.append(_draft_preview_section(draft))
        sections.append(_compose_action_section(scenario))
    sections.append(
        _audit_integrity_section(
            ux, policy, audit, ux_audit, stages, external_effects, live_crm, ux_state
        )
    )

    return {
        "card_id": "mg_guide_meeting_follow_up_result",
        "header": {"title": PRODUCT_NAME, "subtitle": PRODUCT_ATTRIBUTION},
        "scenario": scenario,
        "ux_state": ux_state,
        "workflow_status": workflow_status,
        "policy_decision": {
            "note_write": policy.get("note_write"),
            "stage_write": policy.get("stage_write"),
            "reason_codes": list(_list(policy.get("reason_codes"))),
        },
        "external_effects": external_effects,
        "LIVE_CRM_EXECUTION": live_crm,
        "crm_note_status": crm_note_status,
        "follow_up_draft": _draft_card_model(draft),
        "salesperson_next_step": ux.get("salesperson_next_step"),
        "audit_status": ux_audit.get("display") or ux_audit.get("final_disposition"),
        "sections": sections,
        "fixed_footer": {
            "primary_text": PRODUCT_NAME,
            "secondary_text": PRODUCT_ATTRIBUTION,
        },
        "visible_field_index": _visible_field_index(
            ux, policy, stages, external_effects, live_crm, ux_audit
        ),
    }


def _kv(label: str, value: Any) -> JSONType:
    text = "" if value is None else str(value)
    return {
        "type": "key_value",
        "top_label": label,
        "content": text if text.strip() else "—",
    }


def _relationship_display(status: Any) -> str:
    raw = str(status or "").strip()
    return {
        "matched": "Matched",
        "ambiguous": "Ambiguous",
        "not_found": "Not found",
    }.get(raw, raw or "—")


def _crm_note_status_view(ux: Mapping[str, Any]) -> JSONType:
    """Presentation-layer guard over the backend CRM note status.

    Fail closed: only the four contract states render, and VERIFIED wording
    can never appear unless the backend reports live execution performed.
    Policy permission is never execution proof.
    """
    raw = _mapping(ux.get("crm_note_status"))
    state = str(raw.get("state") or "")
    display = str(raw.get("display") or "")
    live = str(
        _mapping(ux.get("permitted_action_result")).get("LIVE_CRM_EXECUTION")
        or "NOT_PERFORMED"
    )
    if state == "VERIFIED" and live != "PERFORMED":
        state = "UNKNOWN"
        display = ""
    if state not in CRM_NOTE_STATUS_DISPLAY:
        state = "UNKNOWN"
        display = ""
    if not display:
        display = CRM_NOTE_STATUS_DISPLAY[state]
    return {"state": state, "display": display}


def _follow_up_ready_section(
    ux: Mapping[str, Any],
    draft: Mapping[str, Any],
    crm_note_status: Mapping[str, Any],
) -> JSONType:
    rel = _mapping(ux.get("relationship_context"))
    relationship_word = "Matched" if rel.get("contact_resolved") else "Needs review"
    meeting_word = "Understood" if ux.get("summary") else "Not available"
    draft_word = "Ready" if str(draft.get("status")) == "READY" else "Not available"
    return {
        "header": "Follow-up ready",
        "widgets": [
            {"type": "text", "text": "<b>FOLLOW-UP READY</b>"},
            _kv("Transcript", "Processed"),
            _kv("Meeting", meeting_word),
            _kv("Relationship", relationship_word),
            _kv("CRM note", crm_note_status.get("display")),
            _kv("Follow-up draft", draft_word),
        ],
    }


def _needs_review_overview_section(
    ux: Mapping[str, Any],
    crm_note_status: Mapping[str, Any],
) -> JSONType:
    needs = _mapping(ux.get("needs_review"))
    rel = _mapping(ux.get("relationship_context"))
    return {
        "header": "Needs review",
        "widgets": [
            {"type": "text", "text": "<b>NEEDS REVIEW</b>"},
            _kv("Relationship", _relationship_display(rel.get("resolution_status"))),
            _kv("CRM", crm_note_status.get("display")),
            _kv("Draft", "Not created"),
            {
                "type": "text",
                "text": f"<b>Why:</b> {needs.get('reason') or 'Follow-up requires review.'}",
            },
            {
                "type": "text",
                "text": str(needs.get("explicit_next_action") or ""),
            },
        ],
    }


def _processing_status_section(
    ux_state: str,
    workflow_status: str,
    stages: Sequence[Any],
) -> JSONType:
    recorded = sum(1 for raw in stages if _mapping(raw).get("status"))
    return {
        "header": "Processing status",
        "widgets": [
            _kv("UX_STATE", ux_state),
            _kv("Workflow", workflow_status),
            _kv("Stages recorded", f"{recorded} of {len(list(stages))}"),
        ],
    }


def _what_we_heard_section(ux: Mapping[str, Any]) -> JSONType:
    proposed = _mapping(ux.get("proposed_follow_up"))
    widgets: List[JSONType] = [_kv("Summary", ux.get("summary"))]
    needs = _list(proposed.get("needs"))
    if needs:
        widgets.append(_kv("Key needs", _compact(needs)))
    objections = _list(proposed.get("objections"))
    if objections:
        widgets.append(_kv("Objections", _compact(objections)))
    widgets.append(_kv("Salesperson next step", ux.get("salesperson_next_step")))
    return {"header": "What we heard", "widgets": widgets}


def _relationship_section(ux: Mapping[str, Any]) -> JSONType:
    rel = _mapping(ux.get("relationship_context"))
    return {
        "header": "Relationship",
        "widgets": [
            _kv("Status", _relationship_display(rel.get("resolution_status"))),
            _kv("Match basis", rel.get("match_basis")),
            _kv("candidate_count", rel.get("candidate_count")),
        ],
    }


def _crm_section(
    ux: Mapping[str, Any], crm_note_status: Mapping[str, Any]
) -> JSONType:
    widgets: List[JSONType] = [_kv("CRM note", crm_note_status.get("display"))]
    if str(ux.get("ux_state")) == "NEEDS_REVIEW":
        needs = _mapping(ux.get("needs_review"))
        widgets.append(
            {
                "type": "text",
                "text": str(
                    needs.get("zero_unauthorized_effects_message")
                    or "No CRM changes were made."
                ),
            }
        )
    else:
        widgets.append(
            {
                "type": "text",
                "text": (
                    "Policy permission is not execution proof. "
                    "No live CRM write was performed."
                ),
            }
        )
    return {"header": "CRM", "widgets": widgets}


def _body_preview(text: Any, limit: int = 240) -> str:
    body = str(text or "").strip()
    if len(body) <= limit:
        return body
    return body[: limit - 1].rstrip() + "…"


def _draft_preview_section(draft: Mapping[str, Any]) -> JSONType:
    recipient = str(draft.get("recipient_email") or "")
    if draft.get("recipient_name"):
        recipient = f"{draft['recipient_name']} <{draft['recipient_email']}>"
    return {
        "header": "Follow-up draft",
        "widgets": [
            _kv("To", recipient),
            _kv("Subject", draft.get("subject")),
            {"type": "text", "text": _body_preview(draft.get("body_text"))},
            {
                "type": "text",
                "text": (
                    "Human review and send required. "
                    "MG Guide never sends automatically."
                ),
            },
        ],
    }


def _compose_action_section(scenario: str) -> JSONType:
    return {
        "header": "Send follow-up",
        "widgets": [
            {
                "type": "text",
                "text": (
                    "Opens an editable Gmail draft. "
                    "You review it and decide whether to send."
                ),
            },
            {
                "type": "button",
                "text": DRAFT_COMPOSE_BUTTON_TEXT,
                "action": DRAFT_COMPOSE_FUNCTION,
                "action_type": "compose",
                "composed_email_type": "STANDALONE_DRAFT",
                "parameters": {"scenario": scenario},
                "style": "filled",
            },
        ],
    }


def _draft_card_model(draft: Mapping[str, Any]) -> JSONType:
    if not draft:
        return {
            "status": "NOT_AVAILABLE",
            "source": "meeting_follow_up_v1",
            "requires_human_send": True,
        }
    return {
        "status": str(draft.get("status") or "NOT_AVAILABLE"),
        "recipient_name": draft.get("recipient_name"),
        "recipient_email": draft.get("recipient_email"),
        "subject": draft.get("subject"),
        "body_preview": _body_preview(draft.get("body_text")),
        "source": draft.get("source") or "meeting_follow_up_v1",
        "requires_human_send": True,
    }


def _audit_integrity_section(
    ux: Mapping[str, Any],
    policy: Mapping[str, Any],
    audit: Mapping[str, Any],
    ux_audit: Mapping[str, Any],
    stages: Sequence[Any],
    external_effects: int,
    live_crm: str,
    ux_state: str,
) -> JSONType:
    widgets: List[JSONType] = []
    for index, raw in enumerate(stages):
        stage = _mapping(raw)
        title = str(stage.get("title") or STAGE_TITLES[index])
        display_title = title.replace(" result card", "").strip()
        if index == 5 and display_title == "Meeting Follow-Up":
            display_title = "Meeting Follow-Up result"
        widgets.append(_kv(f"{index + 1}. {display_title}", stage.get("status")))
    widgets.extend(
        [
            _kv("policy.note_write", policy.get("note_write")),
            _kv("policy.stage_write", policy.get("stage_write")),
            _kv("policy.reason_codes", _compact(_list(policy.get("reason_codes")))),
            _kv(
                "Audit status",
                ux_audit.get("display")
                or ux_audit.get("final_disposition")
                or audit.get("final_disposition"),
            ),
            {
                "type": "text",
                "text": (
                    f"UX_STATE={ux_state} · external_effects={external_effects} · "
                    f"LIVE_CRM_EXECUTION={live_crm} · CRM_MUTATIONS_PERFORMED=NO · "
                    "EMAIL_AUTO_SEND=FORBIDDEN"
                ),
            },
            {
                "type": "button",
                "text": "Back to MG Guide home",
                "action": "showHome",
                "parameters": {},
                "style": "text",
            },
        ]
    )
    return {"header": "Audit and integrity", "widgets": widgets}


def _visible_field_index(
    ux: Mapping[str, Any],
    policy: Mapping[str, Any],
    stages: Sequence[Any],
    external_effects: int,
    live_crm: str,
    ux_audit: Mapping[str, Any],
) -> JSONType:
    rel = _mapping(ux.get("relationship_context"))
    draft = _mapping(ux.get("follow_up_draft"))
    crm_note_status = _crm_note_status_view(ux)
    draft_ready = (
        str(ux.get("ux_state")) == "COMPLETED"
        and str(draft.get("status")) == "READY"
    )
    return {
        "ux_state": ux.get("ux_state"),
        "summary_present": bool(ux.get("summary")),
        "relationship_status": rel.get("resolution_status"),
        "match_basis": rel.get("match_basis"),
        "candidate_count": rel.get("candidate_count"),
        "proposed_follow_up_present": bool(_mapping(ux.get("proposed_follow_up"))),
        "note_write": policy.get("note_write"),
        "stage_write": policy.get("stage_write"),
        "reason_codes": list(_list(policy.get("reason_codes"))),
        "salesperson_next_step_present": bool(ux.get("salesperson_next_step")),
        "audit_status_present": bool(
            ux_audit.get("display") or ux_audit.get("final_disposition")
        ),
        "external_effects": external_effects,
        "LIVE_CRM_EXECUTION": live_crm,
        "crm_note_status": crm_note_status["state"],
        "follow_up_draft_status": str(draft.get("status") or "NOT_AVAILABLE"),
        "compose_action_count": 1 if draft_ready else 0,
        "stage_count": len(list(stages)),
        "stage_titles": [
            str(_mapping(s).get("title") or "").replace(" result card", "").strip()
            for s in stages
        ],
    }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _list(value: Any) -> List[Any]:
    return list(value) if isinstance(value, list) else []


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _compact(value: Any) -> str:
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, Mapping):
                parts.append(
                    str(
                        item.get("summary")
                        or item.get("name")
                        or item.get("email")
                        or item
                    )
                )
            else:
                parts.append(str(item))
        return "; ".join(parts)
    if isinstance(value, Mapping):
        return ", ".join(f"{k}={v}" for k, v in value.items())
    return str(value)
