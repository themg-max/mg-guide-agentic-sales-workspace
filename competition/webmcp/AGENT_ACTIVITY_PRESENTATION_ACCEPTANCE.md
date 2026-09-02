# Agent Activity + Presentation Acceptance (Slices A, B, D)

**Status:** IMPLEMENTATION COMPLETE — NOT DEPLOYED
**Lane:** impl/webmcp-agent-activity-presentation-001
**Source authority:** `themg-max/A.I-Rolodex---Context`
`competition/webmcp/COMPETITION_ELEVATION_PLAN.md`, merged via planning PR #3198
**Slices implemented here:** A (Agent Activity Model), B (Visible Agent
Activity Panel), D (Capability Presentation)
**Slices explicitly out of scope for this lane:** C (evaluation only, run
separately post-deployment), E (not authorized)

---

## 1. Baseline — unchanged

```
WEBMCP_TOOL_COUNT=3

TOOLS=
  process_meeting_follow_up
  get_current_follow_up_state
  get_follow_up_draft

NATIVE_BROWSER_DISCOVERY=PASS
NATIVE_AGENT_INVOCATION=PASS
SUCCESS_FLOW=PASS
FLUENT_DRAFT_VISIBLE=PASS
READ_TOOLS_PASS=PASS
AMBIGUOUS_FAIL_CLOSED=PASS
EXTERNAL_EFFECTS=0
```

No tool was renamed, removed, or added. No public tool `inputSchema` was
changed. No backend route was added, removed, or changed. The backend
remains stateless; the activity ledger described below is entirely
browser-local JavaScript state.

### Multi-run presentation regression contract

```
ACTIVITY_LIST_SCOPE=SESSION_HISTORY
ACTIVITY_SUMMARY_SCOPE=LATEST_WORKFLOW
ACTIVITY_HANDOFF_SCOPE=LATEST_WORKFLOW

MULTI_RUN_SUCCESS_THEN_AMBIGUOUS=PASS
MULTI_RUN_AMBIGUOUS_THEN_SUCCESS=PASS
CUMULATIVE_ACTIVITY_HISTORY_PRESERVED=PASS

WEBMCP_TOOL_COUNT=3
EXTERNAL_EFFECTS=0
DEPLOYMENT_EXECUTED=NO
```

`currentWebMCPActivity` remains cumulative for the browser session. Every
`WORKFLOW_PROCESS` event begins a new presentation segment: only events after
the latest such event derive the visible summary and human handoff. Earlier
`SAFE_STOP`, `DRAFT_READY`, and `HUMAN_HANDOFF_REQUIRED` events remain visible
in history but cannot describe a later workflow.

Verified by: `tests/webmcp/test_tool_registration_source.py` (all
pre-existing assertions unchanged and passing) and
`tests/webmcp/test_agent_activity_presentation.py::test_exactly_three_tools_still_registered`.

---

## 2. What was implemented

### Files changed

- `webmcp/static/app.js` — added `currentWebMCPActivity` ledger,
  `recordActivity()`, `renderActivity()`, actor-aware `processMeeting(scenario, actor)`,
  and activity recording calls inside each of the 3 existing WebMCP tool
  `execute()` handlers and the human button handlers.
- `webmcp/static/index.html` — added `#section-activity` ("Agent Activity"
  panel) and reworked the former raw tool-list section into
  `#section-capabilities` ("Agent Capabilities": ACTION / STATE / ARTIFACT
  cards + trust statement + preserved tool-list).
- `webmcp/static/style.css` — added scoped styling for the new activity
  list/summary/handoff elements and capability cards; no existing selectors
  removed or repurposed.
- `tests/webmcp/test_agent_activity_presentation.py` — new focused test
  file covering Slices A, B, D (21 tests).

No backend (`src/mg_guide/webmcp/`) file was touched. No deployment
manifest, IAM, secret, or environment configuration was touched.

### Slice A — Agent Activity Model

- `currentWebMCPActivity` (array) and `activitySequence` (monotonic
  integer counter) are declared as browser-local `let` variables inside the
  existing IIFE, entirely separate from `currentWebMCPState`. No
  `localStorage`/`sessionStorage`/`indexedDB`/network write is used for
  activity — verified by
  `test_activity_ledger_is_browser_local_and_separate_from_workflow_state`.
- Every event carries `sequence` (deterministic, monotonically increasing),
  `actor` (`AGENT`|`HUMAN`|`SYSTEM`), `event`, `source`
  (`tool_call`|`human_action`|`derived_state`|`system_check`), `tool`
  (nullable), `status`, and `message`.
- `TOOL_DISCOVERY` is deliberately **not** part of the implemented event
  vocabulary — registering a tool via `document.modelContext.registerTool`
  only proves the page registered it, not that any agent discovered or
  used it. Instead, a `SYSTEM`-sourced `WEBMCP_AVAILABLE` event records the
  observable, provable fact ("N WebMCP tools registered"). Verified by
  `test_tool_discovery_not_synthesized_from_registration_alone`.
- Real agent tool invocations (`process_meeting_follow_up`,
  `get_current_follow_up_state`, `get_follow_up_draft`) each record an
  `AGENT`-actor, `tool_call`-sourced event **inside** the real `execute()`
  handler — i.e. only when the tool is actually invoked. Verified by
  `test_agent_tool_invocations_recorded_with_tool_call_source`.
- The human demo buttons call `processMeeting(scenario, "HUMAN")`, and the
  `process_meeting_follow_up` tool's `execute()` calls
  `processMeeting(args.scenario, "AGENT")` — the same function, but the
  caller must supply the true actor. Verified by
  `test_human_button_invocation_recorded_as_human_not_agent`.
- Derived workflow outcomes (`RELATIONSHIP_MATCHED`, `DRAFT_READY`,
  `RELATIONSHIP_REVIEW_REQUIRED`, `SAFE_STOP`, `HUMAN_HANDOFF_REQUIRED`) are
  recorded as `SYSTEM`/`derived_state` events describing only what the
  already-existing backend response actually contained
  (`ux_state`, `follow_up_draft_status`) — no new backend field was added
  or required. Verified by
  `test_derived_workflow_outcomes_are_system_sourced`.
- No string literal in the shipped source claims "agent reasoned",
  "agent decided internally", or "agent discovered" — verified by
  `test_no_hidden_reasoning_claims_in_string_literals`.

### Slice B — Visible Agent Activity Panel

- `#section-activity` ships in `index.html` with only an empty-state
  message ("Waiting for activity...") — no expected/future step is
  pre-rendered. Verified by
  `test_activity_panel_does_not_prerender_expected_sequence`.
- `renderActivity()` is driven entirely by iterating
  `currentWebMCPActivity`; if it is empty, only the waiting message shows.
  Verified by `test_render_activity_only_reflects_recorded_events`.
- Rendered actor labels come from `ACTOR_LABEL[item.actor]`, i.e. from the
  actually-recorded actor, never hardcoded — so a human-triggered click is
  rendered as "Human: ran the SUCCESS demo", never as an agent action.
  Verified by `test_human_action_not_mislabeled_as_agent_in_render`.
- SUCCESS-path and AMBIGUOUS-path copy matches the plan's presentation
  concepts (relationship matched / draft ready / review and send vs.
  review required / draft withheld / confirm relationship). The SUCCESS
  completion summary is actor-aware: it consults the recorded
  `WORKFLOW_PROCESS` initiator and renders "Agent work complete" only for
  AGENT-originated SUCCESS, "Human-run workflow complete" for
  HUMAN-originated SUCCESS, and "Stopped safely" for AMBIGUOUS. DRAFT_READY
  alone never implies agent attribution.
  Verified by `test_success_activity_events_present`,
  `test_ambiguous_activity_events_present`,
  `test_activity_summary_distinguishes_complete_vs_stopped`,
  `test_human_success_summary_not_labeled_agent_work_complete`.

### Slice D — Capability Presentation

- `#section-capabilities` ("Agent Capabilities") presents three cards
  labeled `ACTION`, `STATE`, `ARTIFACT`, each pairing a plain-language
  description with the **exact, unmodified** technical tool name in a
  `<code>` element. Verified by
  `test_capability_section_present_with_action_state_artifact` and
  `test_capability_cards_preserve_exact_technical_tool_names`.
- The trust statement "Agent can prepare. Only a person can send." is
  present verbatim. Verified by `test_capability_trust_statement_present`.
- The pre-existing "WebMCP tools registered on this page" list (`#tool-list`)
  is preserved unchanged inside the new section — the raw technical list
  was not removed, only supplemented. Verified by
  `test_capability_section_still_lists_registered_tools`.

---

## 3. UI scope discipline

Only the activity panel, capability cards, and their directly required
CSS were added. The existing simple static HTML/CSS/JS architecture is
unchanged: no build tool, framework, or bundler was introduced; no
navigation system was added; no unrelated section was redesigned.

---

## 4. Denied scope — confirmed untouched

No fourth WebMCP tool. No renamed tool. No backend route/API change. No
backend session or persistence. No database. No model/prompt dependency.
No CRM/HighLevel/email calls. No customer data. No auth/IAM/secret
changes. No cloud service or deployment change. No landing-host mutation.
Slice C (native orchestration evaluation) and Slice E (bounded internal
coordinator) were not implemented in this lane.

---

## 5. Test results

Command: `pytest tests/webmcp/ -q` (from a fresh virtualenv with
`pip install -e ".[dev]"`)

```
61 passed
```

Command: `pytest -q` (full repository suite)

```
all dots (0 F, 0 E) across every collected test — no failures, no errors
```

Only pre-existing, unrelated `DeprecationWarning`/`PydanticDeprecatedSince212`/
`UserWarning` warnings from third-party ADK/genai/vertexai dependencies
were emitted (unrelated to this change).

### Acceptance criteria mapping

| Criterion | Result | Evidence |
|---|---|---|
| `EXACTLY_THREE_TOOLS` | PASS | `test_exactly_three_tools_still_registered` |
| `ACTIVITY_BROWSER_LOCAL` | PASS | `test_activity_ledger_is_browser_local_and_separate_from_workflow_state` |
| `ACTIVITY_SEQUENCE_DETERMINISTIC` | PASS | `test_activity_sequence_is_deterministic_monotonic_counter` |
| `AGENT_ACTIVITY_SOURCE_ACCURATE` | PASS | `test_agent_tool_invocations_recorded_with_tool_call_source`, `test_derived_workflow_outcomes_are_system_sourced`, `test_no_hidden_reasoning_claims_in_string_literals` |
| `WEBMCP_AVAILABILITY_VISIBLE` | PASS | `test_tool_discovery_not_synthesized_from_registration_alone` (WEBMCP_AVAILABLE present) |
| `UNPROVEN_TOOL_DISCOVERY_NOT_CLAIMED` | PASS | `test_tool_discovery_not_synthesized_from_registration_alone` (TOOL_DISCOVERY absent) |
| `AGENT_TOOL_INVOCATION_RECORDED` | PASS | `test_agent_tool_invocations_recorded_with_tool_call_source` |
| `HUMAN_BUTTON_INVOCATION_RECORDED_AS_HUMAN` | PASS | `test_human_button_invocation_recorded_as_human_not_agent` |
| `HUMAN_ACTION_NOT_MISLABELED_AS_AGENT` | PASS | `test_human_action_not_mislabeled_as_agent_in_render`, `test_human_success_summary_not_labeled_agent_work_complete` |
| `LATEST_WORKFLOW_SUMMARY_AND_HANDOFF` | PASS | `test_latest_workflow_presentation_uses_current_run_only` (single SUCCESS, single AMBIGUOUS, SUCCESS→AMBIGUOUS, AMBIGUOUS→SUCCESS) |
| `CUMULATIVE_ACTIVITY_HISTORY_PRESERVED` | PASS | `test_activity_list_stays_cumulative_while_presentation_is_latest_workflow` |
| `SUCCESS_RELATIONSHIP_MATCHED_VISIBLE` | PASS | `test_success_activity_events_present` |
| `SUCCESS_DRAFT_READY_VISIBLE` | PASS | `test_success_activity_events_present` |
| `SUCCESS_HUMAN_HANDOFF_VISIBLE` | PASS | `test_success_activity_events_present` |
| `AMBIGUOUS_REVIEW_REQUIRED_VISIBLE` | PASS | `test_ambiguous_activity_events_present` |
| `AMBIGUOUS_SAFE_STOP_VISIBLE` | PASS | `test_activity_summary_distinguishes_complete_vs_stopped` |
| `AMBIGUOUS_DRAFT_WITHHELD_VISIBLE` | PASS | `test_ambiguous_activity_events_present` |
| `CAPABILITY_ACTION_VISIBLE` | PASS | `test_capability_section_present_with_action_state_artifact` |
| `CAPABILITY_STATE_VISIBLE` | PASS | `test_capability_section_present_with_action_state_artifact` |
| `CAPABILITY_ARTIFACT_VISIBLE` | PASS | `test_capability_section_present_with_action_state_artifact` |
| `REQUIRES_HUMAN_SEND` | TRUE (unchanged; still asserted by `test_webmcp_app.py`) | pre-existing `test_success_flow_returns_full_safe_payload` |
| `EXTERNAL_EFFECTS` | 0 | no backend change; `test_no_secret_values_in_any_response`, `test_authority_fields_rejected` still pass |

---

## 6. Summary values

```
AGENT_ACTIVITY_MODEL=IMPLEMENTED
AGENT_ACTIVITY_BROWSER_LOCAL=PASS
AGENT_ACTIVITY_SOURCE_ACCURATE=PASS
AGENT_ACTIVITY_SEQUENCE_DETERMINISTIC=PASS

HUMAN_ACTION_NOT_MISLABELED_AS_AGENT=PASS

WEBMCP_AVAILABILITY_VISIBLE=PASS
UNPROVEN_DISCOVERY_NOT_CLAIMED=PASS

SUCCESS_ACTIVITY_PRESENTATION=PASS
AMBIGUOUS_ACTIVITY_PRESENTATION=PASS
HUMAN_HANDOFF_VISIBLE=PASS

CAPABILITY_ACTION_STATE_ARTIFACT=PASS

WEBMCP_TOOL_COUNT=3
REQUIRES_HUMAN_SEND=TRUE
EXTERNAL_EFFECTS=0

DEPLOYMENT_EXECUTED=NO
```

---

## 7. Stop condition

This lane stops after: implementation complete, focused tests pass,
canonical repository test suite passes, this proof artifact recorded,
exact changed paths inspected, and a public pull request opened (not
merged). Slice C evaluation and any Slice E authorization are separate,
future, explicit decisions and were not started here. No deployment,
landing-host mutation, or private A.I. Rolodex host change was made.
