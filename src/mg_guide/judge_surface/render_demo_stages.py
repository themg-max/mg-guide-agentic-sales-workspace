"""Static HTML/text renderers for demo stages and salesperson UX experience."""

from __future__ import annotations

from html import escape
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

JSONType = Dict[str, Any]


def render_demo_stages_html(
    demo_stages: Sequence[Mapping[str, Any]],
    demo_truth: Mapping[str, Any],
    ux_experience: Optional[Mapping[str, Any]] = None,
) -> str:
    """Render six-stage walkthrough + salesperson UX as static HTML."""
    truth_banner = _truth_banner_html(demo_truth)
    stage_sections = "".join(_stage_section_html(stage) for stage in demo_stages)
    ux_section = _ux_section_html(ux_experience) if ux_experience else ""
    return (
        "<section class='mg-guide-demo-stages'>"
        "<h1>MG Guide Meeting Follow-Up</h1>"
        "<p class='attribution'>Powered by AI Rolodex</p>"
        f"{truth_banner}"
        f"{ux_section}"
        "<h2>Workflow stages</h2>"
        f"{stage_sections}"
        "</section>"
    )


def render_demo_stages_text(
    demo_stages: Sequence[Mapping[str, Any]],
    demo_truth: Mapping[str, Any],
    ux_experience: Optional[Mapping[str, Any]] = None,
) -> str:
    """Plain-text walkthrough for stages + salesperson UX."""
    lines: List[str] = [
        "MG Guide Meeting Follow-Up",
        "Powered by AI Rolodex",
        _truth_banner_text(demo_truth),
        "",
    ]
    if ux_experience:
        lines.extend(_ux_section_text(ux_experience))
        lines.append("")
    lines.append("Workflow stages")
    for stage in demo_stages:
        number = stage.get("stage_number")
        title = stage.get("title")
        status = stage.get("status")
        lines.append(f"{number}. {title} [{status}]")
        evidence = stage.get("evidence") if isinstance(stage.get("evidence"), Mapping) else {}
        for key, value in evidence.items():
            lines.append(f"   - {key}: {_fmt(value)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _truth_banner_html(demo_truth: Mapping[str, Any]) -> str:
    live = escape(str(demo_truth.get("LIVE_CRM_EXECUTION", "NOT_PERFORMED")), quote=True)
    effects = escape(str(demo_truth.get("EXTERNAL_EFFECTS", 0)), quote=True)
    mutation = escape(str(demo_truth.get("cloud_mutation", "NONE")), quote=True)
    return (
        "<aside class='demo-truth-banner'>"
        f"<p><strong>LIVE_CRM_EXECUTION</strong>={live}</p>"
        f"<p><strong>EXTERNAL_EFFECTS</strong>={effects}</p>"
        f"<p><strong>cloud_mutation</strong>={mutation}</p>"
        "</aside>"
    )


def _truth_banner_text(demo_truth: Mapping[str, Any]) -> str:
    return (
        f"LIVE_CRM_EXECUTION={demo_truth.get('LIVE_CRM_EXECUTION', 'NOT_PERFORMED')} | "
        f"EXTERNAL_EFFECTS={demo_truth.get('EXTERNAL_EFFECTS', 0)} | "
        f"cloud_mutation={demo_truth.get('cloud_mutation', 'NONE')}"
    )


def _stage_section_html(stage: Mapping[str, Any]) -> str:
    number = escape(str(stage.get("stage_number", "")), quote=True)
    title = escape(str(stage.get("title", "")), quote=True)
    status = escape(str(stage.get("status", "")), quote=True)
    evidence = stage.get("evidence") if isinstance(stage.get("evidence"), Mapping) else {}
    rows = "".join(
        f"<li><strong>{escape(str(key), quote=True)}:</strong> "
        f"{escape(_fmt(value), quote=True)}</li>"
        for key, value in evidence.items()
    )
    return (
        f"<section class='demo-stage' data-stage-id='{escape(str(stage.get('stage_id', '')), quote=True)}'>"
        f"<h3>Stage {number}: {title}</h3>"
        f"<p><strong>Status:</strong> {status}</p>"
        f"<ul>{rows or '<li>(none)</li>'}</ul>"
        "</section>"
    )


def _ux_section_html(ux: Mapping[str, Any]) -> str:
    state = str(ux.get("ux_state") or "UNKNOWN")
    state_class = "ux-completed" if state == "COMPLETED" else "ux-needs-review"
    headline = "Completed" if state == "COMPLETED" else "Needs review"
    meeting = _mapping(ux.get("meeting_context"))
    relationship = _mapping(ux.get("relationship_context"))
    policy = _mapping(ux.get("policy_decision"))
    permitted = _mapping(ux.get("permitted_action_result"))
    audit = _mapping(ux.get("audit_status"))
    proposed = _mapping(ux.get("proposed_follow_up"))
    next_step = escape(str(ux.get("salesperson_next_step") or ""), quote=True)
    summary = escape(str(ux.get("summary") or ""), quote=True)
    title = escape(str(meeting.get("title") or "Meeting Follow-Up"), quote=True)

    policy_block = (
        f"<p><strong>Policy decision:</strong> "
        f"note_write={escape(str(policy.get('note_write')), quote=True)}; "
        f"stage_write={escape(str(policy.get('stage_write')), quote=True)}; "
        f"reason_codes={escape(_fmt(policy.get('reason_codes')), quote=True)}</p>"
    )
    audit_block = (
        f"<p><strong>Audit status:</strong> "
        f"{escape(str(audit.get('display') or audit.get('final_disposition') or ''), quote=True)}"
        f" (disposition={escape(str(audit.get('final_disposition')), quote=True)})</p>"
    )
    next_block = f"<p><strong>Salesperson next step:</strong> {next_step}</p>"
    result_block = (
        f"<p><strong>Permitted action / result:</strong> "
        f"{escape(str(permitted.get('result_label')), quote=True)}; "
        f"external_effects={escape(str(permitted.get('external_effects')), quote=True)}; "
        f"LIVE_CRM_EXECUTION={escape(str(permitted.get('LIVE_CRM_EXECUTION')), quote=True)}</p>"
    )

    if state == "COMPLETED":
        completed = _mapping(ux.get("completed"))
        body = (
            f"<p class='ux-headline'>{escape(str(completed.get('headline') or 'Follow-up ready'), quote=True)}</p>"
            f"<p>{escape(str(completed.get('body') or ''), quote=True)}</p>"
            f"<p><strong>Meeting:</strong> {title}</p>"
            f"<p><strong>Summary:</strong> {summary}</p>"
            f"<p><strong>Relationship:</strong> "
            f"status={escape(str(relationship.get('resolution_status')), quote=True)}; "
            f"basis={escape(str(relationship.get('match_basis')), quote=True)}; "
            f"candidates={escape(str(relationship.get('candidate_count')), quote=True)}; "
            f"stage={escape(str(relationship.get('current_stage')), quote=True)}</p>"
            f"<p><strong>Proposed follow-up:</strong> "
            f"{escape(_fmt(proposed.get('note_intents')), quote=True)}; "
            f"stage={escape(_fmt(proposed.get('stage_intents')), quote=True)}</p>"
            f"{policy_block}{result_block}{audit_block}{next_block}"
        )
    else:
        needs = _mapping(ux.get("needs_review"))
        body = (
            f"<p class='ux-headline'>{escape(str(needs.get('reason') or 'Review required'), quote=True)}</p>"
            f"<p class='zero-effects'>"
            f"{escape(str(needs.get('zero_unauthorized_effects_message') or 'No CRM changes were made.'), quote=True)}"
            f"</p>"
            f"<p><strong>Meeting:</strong> {title}</p>"
            f"<p><strong>Summary:</strong> {summary}</p>"
            f"<p><strong>Block context:</strong> "
            f"{escape(_fmt(needs.get('block_context')), quote=True)}</p>"
            f"{policy_block}{result_block}{audit_block}"
            f"<p><strong>Salesperson next step:</strong> "
            f"{escape(str(needs.get('explicit_next_action') or next_step), quote=True)}</p>"
        )

    return (
        f"<section class='mg-guide-ux-experience {state_class}' data-ux-state='{escape(state, quote=True)}'>"
        f"<h2>Salesperson view — {escape(headline, quote=True)}</h2>"
        f"<p><strong>UX state:</strong> {escape(state, quote=True)}</p>"
        f"{body}"
        "</section>"
    )


def _ux_section_text(ux: Mapping[str, Any]) -> List[str]:
    state = str(ux.get("ux_state") or "UNKNOWN")
    lines = [
        f"Salesperson view — {'Completed' if state == 'COMPLETED' else 'Needs review'}",
        f"UX state: {state}",
        f"Meeting: {_fmt(_mapping(ux.get('meeting_context')).get('title'))}",
        f"Summary: {_fmt(ux.get('summary'))}",
        f"Relationship: {_fmt(ux.get('relationship_context'))}",
        f"Proposed follow-up: {_fmt(ux.get('proposed_follow_up'))}",
        f"Policy decision: {_fmt(ux.get('policy_decision'))}",
        f"Permitted action/result: {_fmt(ux.get('permitted_action_result'))}",
        f"Audit status: {_fmt(_mapping(ux.get('audit_status')).get('display'))}",
        f"Salesperson next step: {_fmt(ux.get('salesperson_next_step'))}",
    ]
    if state == "NEEDS_REVIEW":
        needs = _mapping(ux.get("needs_review"))
        lines.append(f"Review reason: {_fmt(needs.get('reason'))}")
        lines.append(
            f"Zero unauthorized effects: {_fmt(needs.get('zero_unauthorized_effects_message'))}"
        )
        lines.append(f"Block context: {_fmt(needs.get('block_context'))}")
    return lines


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _fmt(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, Mapping):
        parts = [f"{k}={_fmt(v)}" for k, v in value.items()]
        return "{" + ", ".join(parts) + "}"
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        items = [_fmt(v) for v in value]
        return "[" + ", ".join(items) + "]"
    return str(value)
