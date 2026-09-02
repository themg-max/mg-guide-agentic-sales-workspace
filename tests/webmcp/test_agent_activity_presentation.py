"""Static-source checks for Competition Elevation Plan Slices A, B, D.

These tests do not execute a browser; they verify (in the shipped static
source) that:

* Slice A: a browser-local, ephemeral activity ledger exists, is separate
  from ``currentWebMCPState``, records a closed set of actors, and never
  claims tool discovery it cannot prove.
* Slice B: an "Agent Activity" panel renders only observed events (no
  pre-rendered expected sequence), and human-triggered actions are never
  labeled as agent-originated.
* Slice D: an "Agent Capabilities" section presents ACTION / STATE /
  ARTIFACT framing with the exact technical tool names preserved, plus the
  required trust statement.

Full browser acceptance is recorded separately in ``proof/webmcp/`` and in
``competition/webmcp/AGENT_ACTIVITY_PRESENTATION_ACCEPTANCE.md``.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_ROOT = REPO_ROOT / "webmcp" / "static"
APP_JS = STATIC_ROOT / "app.js"
INDEX_HTML = STATIC_ROOT / "index.html"

REQUIRED_TOOL_NAMES = [
    "process_meeting_follow_up",
    "get_current_follow_up_state",
    "get_follow_up_draft",
]


def _app_js() -> str:
    return APP_JS.read_text(encoding="utf-8")


def _index_html() -> str:
    return INDEX_HTML.read_text(encoding="utf-8")


def _derive_latest_workflow_presentation(activity: list[dict[str, str]]) -> dict[str, str | bool | int]:
    """Execute the shipped pure helper without requiring a browser framework."""
    node = shutil.which("node")
    assert node is not None, "Node.js is required to execute the shipped frontend helper"

    src = _app_js()
    helper_start = src.index("function deriveLatestWorkflowPresentation(activity)")
    helper_end = src.index("\n  /**\n   * Render the Agent Activity panel", helper_start)
    helper = src[helper_start:helper_end]
    program = (
        '"use strict";\n'
        + helper
        + "\nconst activity = JSON.parse(process.argv[1]);\n"
        + "const before = JSON.stringify(activity);\n"
        + "const presentation = deriveLatestWorkflowPresentation(activity);\n"
        + "process.stdout.write(JSON.stringify({ presentation, "
        + "historyUnchanged: JSON.stringify(activity) === before, "
        + "historyLength: activity.length }));\n"
    )
    completed = subprocess.run(
        [node, "-e", program, json.dumps(activity)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _event(actor: str, event: str, message: str) -> dict[str, str]:
    return {"actor": actor, "event": event, "message": message}


SUCCESS_ACTIVITY = [
    _event("HUMAN", "WORKFLOW_PROCESS", "ran the SUCCESS demo"),
    _event("SYSTEM", "RELATIONSHIP_MATCHED", "relationship matched"),
    _event("SYSTEM", "DRAFT_READY", "follow-up draft became ready"),
    _event("SYSTEM", "HUMAN_HANDOFF_REQUIRED", "Review and send"),
]

AMBIGUOUS_ACTIVITY = [
    _event("HUMAN", "WORKFLOW_PROCESS", "ran the AMBIGUOUS_CONTACT demo"),
    _event(
        "SYSTEM",
        "RELATIONSHIP_REVIEW_REQUIRED",
        "relationship identity requires review",
    ),
    _event("SYSTEM", "SAFE_STOP", "follow-up draft withheld"),
    _event("SYSTEM", "HUMAN_HANDOFF_REQUIRED", "Confirm relationship"),
]


# ---------------------------------------------------------------------------
# Baseline preservation
# ---------------------------------------------------------------------------


def test_exactly_three_tools_still_registered() -> None:
    src = _app_js()
    found = re.findall(r'name:\s*"([a-z_]+)"', src)
    tool_names = [n for n in found if n in REQUIRED_TOOL_NAMES]
    assert sorted(set(tool_names)) == sorted(REQUIRED_TOOL_NAMES)
    assert len(tool_names) == len(REQUIRED_TOOL_NAMES)


# ---------------------------------------------------------------------------
# Slice A — browser-local activity model
# ---------------------------------------------------------------------------


def test_activity_ledger_is_browser_local_and_separate_from_workflow_state() -> None:
    src = _app_js()
    assert "currentWebMCPActivity" in src
    assert "activitySequence" in src
    assert "currentWebMCPState" in src
    # Must not be persisted or sent anywhere.
    assert "localStorage" not in src
    assert "sessionStorage" not in src
    assert "indexedDB" not in src


def test_activity_sequence_is_deterministic_monotonic_counter() -> None:
    src = _app_js()
    assert "activitySequence += 1" in src
    assert "sequence: activitySequence" in src


def test_activity_actor_closed_set_used() -> None:
    src = _app_js()
    for actor in ("AGENT", "HUMAN", "SYSTEM"):
        assert f'"{actor}"' in src


def test_tool_discovery_not_synthesized_from_registration_alone() -> None:
    src = _app_js()
    # The closed event vocabulary must not include a bare "TOOL_DISCOVERY"
    # event recorded merely because registerTool() succeeded.
    assert "TOOL_DISCOVERY" not in src
    # WEBMCP_AVAILABLE (system fact: tools registered) is allowed and must
    # be SYSTEM-sourced.
    assert '"WEBMCP_AVAILABLE"' in src
    webmcp_available_call = re.search(
        r'recordActivity\(\s*"SYSTEM",\s*"WEBMCP_AVAILABLE"', src
    )
    assert webmcp_available_call is not None


def test_agent_tool_invocations_recorded_with_tool_call_source() -> None:
    src = _app_js()
    assert re.search(
        r'recordActivity\(\s*"AGENT",\s*"WORKFLOW_PROCESS",\s*"tool_call"', src
    )
    assert re.search(
        r'recordActivity\(\s*"AGENT",\s*"STATE_READ",\s*"tool_call"', src
    )
    assert re.search(
        r'recordActivity\(\s*"AGENT",\s*"DRAFT_READ",\s*"tool_call"', src
    )


def test_human_button_invocation_recorded_as_human_not_agent() -> None:
    src = _app_js()
    assert re.search(
        r'recordActivity\(\s*"HUMAN",\s*"WORKFLOW_PROCESS",\s*"human_action"', src
    )
    # processMeeting must accept an actor parameter distinguishing the two
    # call paths, and the human buttons must pass "HUMAN" explicitly.
    assert 'processMeeting(scenario, actor)' in src or re.search(
        r"processMeeting\(scenario,\s*actor\)", src
    )
    assert 'processMeeting("SUCCESS", "HUMAN")' in src
    assert 'processMeeting("AMBIGUOUS_CONTACT", "HUMAN")' in src
    assert 'processMeeting(args.scenario, "AGENT")' in src


def test_derived_workflow_outcomes_are_system_sourced() -> None:
    src = _app_js()
    for event in (
        "RELATIONSHIP_MATCHED",
        "DRAFT_READY",
        "RELATIONSHIP_REVIEW_REQUIRED",
        "SAFE_STOP",
        "HUMAN_HANDOFF_REQUIRED",
    ):
        assert re.search(
            r'recordActivity\(\s*"SYSTEM",\s*"' + event + r'"', src
        ), f"expected SYSTEM-sourced {event} event"


def test_no_hidden_reasoning_claims_in_string_literals() -> None:
    src = _app_js()
    # Strip // line comments before scanning, so this check targets actual
    # runtime string literals (rendered/recorded copy), not code comments
    # describing what must never be written.
    without_comments = re.sub(r"//[^\n]*", "", src)
    literals = " ".join(re.findall(r'"([^"]*)"', without_comments)).lower()
    for banned in ("agent reasoned", "agent decided internally", "agent discovered"):
        assert banned not in literals


# ---------------------------------------------------------------------------
# Slice B — visible agent activity panel
# ---------------------------------------------------------------------------


def test_activity_panel_present_in_html() -> None:
    html = _index_html()
    assert 'id="section-activity"' in html
    assert "Agent Activity" in html
    assert 'id="activity-list"' in html
    assert 'id="activity-summary"' in html
    assert 'id="activity-handoff"' in html


def test_activity_panel_does_not_prerender_expected_sequence() -> None:
    html = _index_html()
    # The only static list item shipped in HTML must be the empty-state
    # message, not a pre-populated set of expected steps.
    activity_section = html[
        html.index('id="section-activity"') : html.index('id="section-processing"')
    ]
    assert "Waiting for activity" in activity_section
    for banned in (
        "Current state inspected",
        "Meeting processed",
        "Relationship matched",
        "Follow-up prepared",
        "Draft retrieved",
    ):
        assert banned not in activity_section


def test_render_activity_only_reflects_recorded_events() -> None:
    src = _app_js()
    assert "function renderActivity()" in src
    assert "currentWebMCPActivity.length === 0" in src
    # Must iterate the actual recorded ledger, not a static template.
    assert "for (let i = 0; i < currentWebMCPActivity.length; i++)" in src


def test_human_action_not_mislabeled_as_agent_in_render() -> None:
    src = _app_js()
    assert "ACTOR_LABEL" in src
    assert '"AGENT": "Agent"' in src or 'AGENT: "Agent"' in src
    assert '"HUMAN": "Human"' in src or 'HUMAN: "Human"' in src
    # Rendered actor label is driven by item.actor (the recorded, truthful
    # actor), never hardcoded to "Agent" for a human-originated event.
    assert "ACTOR_LABEL[item.actor]" in src


def test_success_activity_events_present() -> None:
    src = _app_js()
    assert '"relationship matched"' in src
    assert '"follow-up draft became ready"' in src
    assert '"Review and send"' in src


def test_ambiguous_activity_events_present() -> None:
    src = _app_js()
    assert '"relationship identity requires review"' in src
    assert '"follow-up draft withheld"' in src
    assert '"Confirm relationship"' in src


def test_activity_summary_distinguishes_complete_vs_stopped() -> None:
    src = _app_js()
    assert '"Agent work complete"' in src
    assert '"Human-run workflow complete"' in src
    assert '"Stopped safely"' in src


def test_human_success_summary_not_labeled_agent_work_complete() -> None:
    """HUMAN-originated SUCCESS must not render 'Agent work complete'.

    Regression for HUMAN_ACTION_NOT_MISLABELED_AS_AGENT at the summary level:
    DRAFT_READY alone is insufficient — the summary must consult the recorded
    WORKFLOW_PROCESS actor.
    """
    src = _app_js()
    # Initiator is derived from the WORKFLOW_PROCESS event actor.
    assert "workflowInitiator" in src
    assert 'item.event === "WORKFLOW_PROCESS"' in src
    assert 'workflowInitiator = item.actor' in src
    # HUMAN SUCCESS path uses non-agent copy.
    assert re.search(
        r'workflowInitiator === "HUMAN"[\s\S]*?"Human-run workflow complete"',
        src,
    )
    # AGENT SUCCESS path may still use agent copy.
    assert re.search(
        r'workflowInitiator === "AGENT"[\s\S]*?"Agent work complete"',
        src,
    )
    # Guard: draftReady alone must not unconditionally set agent copy.
    # The agent string must appear only inside the AGENT initiator branch.
    agent_complete_sites = [
        m.start() for m in re.finditer(r'"Agent work complete"', src)
    ]
    assert agent_complete_sites, "expected Agent work complete for AGENT path"
    for pos in agent_complete_sites:
        window = src[max(0, pos - 200) : pos]
        assert 'workflowInitiator === "AGENT"' in window, (
            "Agent work complete must be gated on AGENT workflow initiator"
        )


@pytest.mark.parametrize(
    ("case", "activity", "summary", "handoff"),
    [
        (
            "single SUCCESS",
            SUCCESS_ACTIVITY,
            "Human-run workflow complete",
            "Review and send",
        ),
        (
            "single AMBIGUOUS",
            AMBIGUOUS_ACTIVITY,
            "Stopped safely",
            "Confirm relationship",
        ),
        (
            "SUCCESS then AMBIGUOUS",
            SUCCESS_ACTIVITY + AMBIGUOUS_ACTIVITY,
            "Stopped safely",
            "Confirm relationship",
        ),
        (
            "AMBIGUOUS then SUCCESS",
            AMBIGUOUS_ACTIVITY + SUCCESS_ACTIVITY,
            "Human-run workflow complete",
            "Review and send",
        ),
    ],
)
def test_latest_workflow_presentation_uses_current_run_only(
    case: str,
    activity: list[dict[str, str]],
    summary: str,
    handoff: str,
) -> None:
    """Summary/handoff follow the last WORKFLOW_PROCESS; history stays cumulative."""
    result = _derive_latest_workflow_presentation(activity)
    presentation = result["presentation"]
    assert presentation["summary"] == summary, case
    assert presentation["handoffMessage"] == handoff, case
    assert result["historyUnchanged"] is True
    assert result["historyLength"] == len(activity)


def test_agent_success_summary_remains_actor_aware() -> None:
    activity = [
        _event("AGENT", "WORKFLOW_PROCESS", "processed the meeting"),
        _event("SYSTEM", "DRAFT_READY", "follow-up draft became ready"),
        _event("SYSTEM", "HUMAN_HANDOFF_REQUIRED", "Review and send"),
    ]
    result = _derive_latest_workflow_presentation(activity)
    assert result["presentation"]["summary"] == "Agent work complete"
    assert result["presentation"]["handoffMessage"] == "Review and send"


def test_activity_list_stays_cumulative_while_presentation_is_latest_workflow() -> None:
    src = _app_js()
    render_start = src.index("function renderActivity()")
    render_end = src.index("\n  function apiUrl", render_start)
    render_body = src[render_start:render_end]
    assert "for (let i = 0; i < currentWebMCPActivity.length; i++)" in render_body
    assert "deriveLatestWorkflowPresentation(currentWebMCPActivity)" in render_body


# ---------------------------------------------------------------------------
# Slice D — capability presentation
# ---------------------------------------------------------------------------


def test_capability_section_present_with_action_state_artifact() -> None:
    html = _index_html()
    assert 'id="section-capabilities"' in html
    assert "Agent Capabilities" in html
    assert ">ACTION<" in html
    assert ">STATE<" in html
    assert ">ARTIFACT<" in html


def test_capability_cards_preserve_exact_technical_tool_names() -> None:
    html = _index_html()
    for name in REQUIRED_TOOL_NAMES:
        assert f"<code class=\"capability-tool\">{name}</code>" in html


def test_capability_trust_statement_present() -> None:
    html = _index_html()
    assert "Agent can prepare. Only a person can send." in html


def test_capability_section_still_lists_registered_tools() -> None:
    html = _index_html()
    assert 'id="tool-list"' in html
