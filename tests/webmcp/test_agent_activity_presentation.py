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

import re
from pathlib import Path

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
    assert '"Stopped safely"' in src


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
