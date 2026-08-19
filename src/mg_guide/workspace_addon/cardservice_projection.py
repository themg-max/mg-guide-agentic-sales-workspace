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

STAGE_TITLES = (
    "Meeting ready",
    "Meeting Context",
    "Relationship Resolution",
    "Follow-Up Planning",
    "Policy Evaluation",
    "Meeting Follow-Up result",
)


def project_cardservice_home() -> JSONType:
    """Homepage card model: branding + scenario selectors."""
    return {
        "card_id": "mg_guide_home",
        "header": {
            "title": PRODUCT_NAME,
            "subtitle": PRODUCT_ATTRIBUTION,
        },
        "sections": [
            {
                "header": PRODUCT_NAME,
                "widgets": [
                    {"type": "text", "text": f"<b>{PRODUCT_NAME}</b>"},
                    {"type": "text", "text": PRODUCT_ATTRIBUTION},
                    {
                        "type": "text",
                        "text": (
                            f"Primary experience: <b>{PRIMARY_CAPABILITY}</b>. "
                            "Synthetic competition scenarios only. "
                            "LIVE_CRM_EXECUTION=NOT_PERFORMED."
                        ),
                    },
                ],
            },
            {
                "header": PRIMARY_CAPABILITY,
                "widgets": [
                    {
                        "type": "button",
                        "text": "Run SUCCESS",
                        "action": "runScenario",
                        "parameters": {"scenario": "SUCCESS"},
                        "style": "filled",
                    },
                    {
                        "type": "button",
                        "text": "Run AMBIGUOUS_CONTACT",
                        "action": "runScenario",
                        "parameters": {"scenario": "AMBIGUOUS_CONTACT"},
                        "style": "filled",
                    },
                    {
                        "type": "button",
                        "text": "Run STAGE_CHANGE_DENIED (optional)",
                        "action": "runScenario",
                        "parameters": {"scenario": "STAGE_CHANGE_DENIED"},
                        "style": "text",
                    },
                ],
            },
            {
                "header": "Truth boundary",
                "widgets": [
                    {
                        "type": "text",
                        "text": (
                            "No live CRM writes. external_effects stay 0 on this "
                            "judge path. CRM mutations are not performed."
                        ),
                    }
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

    sections: List[JSONType] = [
        {
            "header": f"{PRODUCT_NAME} · {PRIMARY_CAPABILITY}",
            "widgets": [
                {"type": "text", "text": f"<b>{PRODUCT_NAME}</b>"},
                {"type": "text", "text": PRODUCT_ATTRIBUTION},
                {
                    "type": "key_value",
                    "top_label": "Scenario",
                    "content": scenario,
                },
                {
                    "type": "key_value",
                    "top_label": "UX_STATE",
                    "content": ux_state,
                },
                {
                    "type": "key_value",
                    "top_label": "workflow_status",
                    "content": workflow_status,
                },
            ],
        }
    ]

    sections.extend(_stage_sections(stages))
    sections.append(_result_section(ux, policy, audit, ux_audit, external_effects, live_crm))
    sections.append(_truth_section(external_effects, live_crm, ux_state))

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


def _stage_sections(stages: Sequence[Any]) -> List[JSONType]:
    out: List[JSONType] = []
    for index, raw in enumerate(stages):
        stage = _mapping(raw)
        title = str(stage.get("title") or STAGE_TITLES[index])
        # Normalize optional "result card" suffix for display contract.
        display_title = title.replace(" result card", "").strip()
        if index == 5 and display_title == "Meeting Follow-Up":
            display_title = "Meeting Follow-Up result"
        evidence = _mapping(stage.get("evidence"))
        widgets: List[JSONType] = [
            {
                "type": "key_value",
                "top_label": "Stage status",
                "content": str(stage.get("status") or ""),
            }
        ]
        widgets.extend(_evidence_widgets(index, evidence))
        out.append(
            {
                "header": f"{index + 1}. {display_title}",
                "stage_number": index + 1,
                "stage_id": stage.get("stage_id"),
                "title": display_title,
                "widgets": widgets,
            }
        )
    return out


def _evidence_widgets(index: int, evidence: Mapping[str, Any]) -> List[JSONType]:
    widgets: List[JSONType] = []

    def kv(label: str, value: Any) -> None:
        if value is None or value == "" or value == []:
            return
        if isinstance(value, (list, dict)):
            content = _compact(value)
        else:
            content = str(value)
        widgets.append({"type": "key_value", "top_label": label, "content": content})

    if index == 0:
        kv("title", evidence.get("title"))
        kv("source", evidence.get("source"))
        kv("participants", evidence.get("participants"))
    elif index == 1:
        kv("summary", evidence.get("summary"))
        kv("needs", evidence.get("needs"))
        kv("next_step", evidence.get("next_step"))
        kv("extraction_confidence", evidence.get("extraction_confidence"))
    elif index == 2:
        kv("resolution_status", evidence.get("resolution_status"))
        kv("match_basis", evidence.get("match_basis"))
        kv("candidate_count", evidence.get("candidate_count"))
        kv("current_stage", evidence.get("current_stage"))
    elif index == 3:
        kv("note_intents", evidence.get("note_intents"))
        kv("stage_intents", evidence.get("stage_intents"))
        kv("note_execution_attempted", evidence.get("note_execution_attempted"))
        kv("stage_execution_attempted", evidence.get("stage_execution_attempted"))
    elif index == 4:
        kv("note_write", evidence.get("note_write"))
        kv("stage_write", evidence.get("stage_write"))
        kv("reason_codes", evidence.get("reason_codes"))
    else:
        framing = _mapping(evidence.get("framing"))
        brief = _mapping(evidence.get("brief"))
        kv("card_state", evidence.get("card_state"))
        kv("workflow_status", evidence.get("workflow_status"))
        kv("headline", framing.get("headline") or brief.get("headline"))
        kv("body", framing.get("body"))
        kv("next_action", brief.get("next_action"))
        kv("no_crm_changes_made", framing.get("no_crm_changes_made"))
        kv("external_effects", _mapping(evidence.get("integrity")).get("external_effects"))
        kv("LIVE_CRM_EXECUTION", evidence.get("LIVE_CRM_EXECUTION"))
    return widgets


def _result_section(
    ux: Mapping[str, Any],
    policy: Mapping[str, Any],
    audit: Mapping[str, Any],
    ux_audit: Mapping[str, Any],
    external_effects: int,
    live_crm: str,
) -> JSONType:
    widgets: List[JSONType] = [
        {
            "type": "key_value",
            "top_label": "UX_STATE",
            "content": str(ux.get("ux_state") or ""),
        },
        {
            "type": "key_value",
            "top_label": "Meeting summary",
            "content": str(ux.get("summary") or ""),
        },
    ]
    rel = _mapping(ux.get("relationship_context"))
    widgets.extend(
        [
            {
                "type": "key_value",
                "top_label": "Relationship status",
                "content": str(rel.get("resolution_status") or ""),
            },
            {
                "type": "key_value",
                "top_label": "match_basis",
                "content": str(rel.get("match_basis") or ""),
            },
            {
                "type": "key_value",
                "top_label": "candidate_count",
                "content": str(rel.get("candidate_count")),
            },
        ]
    )
    proposed = _mapping(ux.get("proposed_follow_up"))
    widgets.append(
        {
            "type": "key_value",
            "top_label": "Proposed follow-up",
            "content": str(
                proposed.get("headline")
                or proposed.get("summary")
                or "See stage evidence"
            ),
        }
    )
    widgets.extend(
        [
            {
                "type": "key_value",
                "top_label": "policy.note_write",
                "content": str(policy.get("note_write") or ""),
            },
            {
                "type": "key_value",
                "top_label": "policy.stage_write",
                "content": str(policy.get("stage_write") or ""),
            },
            {
                "type": "key_value",
                "top_label": "policy.reason_codes",
                "content": _compact(_list(policy.get("reason_codes"))),
            },
            {
                "type": "key_value",
                "top_label": "Salesperson next step",
                "content": str(ux.get("salesperson_next_step") or ""),
            },
            {
                "type": "key_value",
                "top_label": "Audit status",
                "content": str(
                    ux_audit.get("display")
                    or ux_audit.get("final_disposition")
                    or audit.get("final_disposition")
                    or ""
                ),
            },
            {
                "type": "key_value",
                "top_label": "external_effects",
                "content": str(external_effects),
            },
            {
                "type": "key_value",
                "top_label": "LIVE_CRM_EXECUTION",
                "content": live_crm,
            },
        ]
    )

    if str(ux.get("ux_state")) == "NEEDS_REVIEW":
        needs = _mapping(ux.get("needs_review"))
        widgets.extend(
            [
                {
                    "type": "text",
                    "text": f"<b>Needs review:</b> {needs.get('reason') or ''}",
                },
                {
                    "type": "text",
                    "text": str(
                        needs.get("zero_unauthorized_effects_message")
                        or "No CRM changes were made."
                    ),
                },
                {
                    "type": "text",
                    "text": (
                        "Resolve contact identity before any CRM write."
                        if "AMBIGUOUS_CONTACT"
                        in [
                            str(c)
                            for c in _list(
                                _mapping(needs.get("block_context")).get("reason_codes")
                            )
                        ]
                        else str(needs.get("explicit_next_action") or "")
                    ),
                },
            ]
        )
    else:
        completed = _mapping(ux.get("completed"))
        widgets.append(
            {
                "type": "text",
                "text": str(
                    completed.get("body")
                    or "Governed follow-up intents are prepared. No live CRM write was performed."
                ),
            }
        )

    widgets.append(
        {
            "type": "button",
            "text": "Back to MG Guide home",
            "action": "showHome",
            "parameters": {},
            "style": "text",
        }
    )
    return {"header": "Meeting Follow-Up result", "widgets": widgets}


def _truth_section(external_effects: int, live_crm: str, ux_state: str) -> JSONType:
    return {
        "header": "Integrity",
        "widgets": [
            {
                "type": "text",
                "text": (
                    f"UX_STATE={ux_state} · external_effects={external_effects} · "
                    f"LIVE_CRM_EXECUTION={live_crm} · CRM_MUTATIONS_PERFORMED=NO"
                ),
            }
        ],
    }


def _visible_field_index(
    ux: Mapping[str, Any],
    policy: Mapping[str, Any],
    stages: Sequence[Any],
    external_effects: int,
    live_crm: str,
    ux_audit: Mapping[str, Any],
) -> JSONType:
    rel = _mapping(ux.get("relationship_context"))
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
