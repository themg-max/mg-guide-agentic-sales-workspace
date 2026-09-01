# MG Guide WebMCP — End-to-End Acceptance Proof (001)

```text
PROOF_ID=mg-guide-webmcp-end-to-end-acceptance-001
BRANCH=impl/webmcp-mg-guide-agentic-workspace-001
BASE_SHA=bc9a723f84e72ec3605da495ad16fbf78f3a99a9
RECORDED_AT=2026-09-01T12:20:00-04:00
ENVIRONMENT=local (Python 3.12.13, Playwright-driven Chromium)
```

## Automated test evidence

```text
$ PYTHONPATH=src python -m pytest tests/webmcp -v
tests/webmcp/test_tool_registration_source.py ........   [ 30%]
tests/webmcp/test_webmcp_app.py ..................       [100%]
============================== 26 passed in 0.03s ===============================

$ PYTHONPATH=src python -m pytest tests/
927 passed, 155 warnings in 5.30s
```

No existing test regressed. All 927 previously-passing tests remain green
after the additive WebMCP change.

## WEBMCP-01..20 disposition

| ID | Check | Result |
| --- | --- | --- |
| WEBMCP-01 | Unique tool names | PASS — `test_all_required_tool_names_present_and_unique` |
| WEBMCP-02 | Stable tool names | PASS — literal string names in `app.js` |
| WEBMCP-03 | Non-empty descriptions | PASS — `test_tool_descriptions_non_empty` |
| WEBMCP-04 | Valid input schemas | PASS — inline JSON Schema objects in `app.js` |
| WEBMCP-05 | Scenario enum bounded | PASS — `test_scenario_enum_bounded_to_success_and_ambiguous` |
| WEBMCP-06 | `additionalProperties: false` | PASS — `test_input_schema_rejects_additional_properties` |
| WEBMCP-07 | No raw CRM identifiers accepted | PASS — `test_authority_fields_rejected[contact_id]`, `[location_id]` |
| WEBMCP-08 | No live execution selector | PASS — `test_authority_fields_rejected[live]` |
| WEBMCP-09 | No email-send selector | PASS — `test_authority_fields_rejected[send_email]` |
| WEBMCP-10 | No registration without `modelContext` | PASS — `test_no_registration_before_feature_check`; live-browser confirmation below |
| WEBMCP-11 | SUCCESS updates visible UI | PASS — browser evidence below |
| WEBMCP-12 | AMBIGUOUS_CONTACT updates NEEDS REVIEW UI | PASS — browser evidence below |
| WEBMCP-13 | Current state returns latest visible state | PASS — `test_success_flow_updates_state_and_draft`; browser evidence below |
| WEBMCP-14 | Draft READY only after SUCCESS | PASS — `test_success_flow_updates_state_and_draft` |
| WEBMCP-15 | Draft unavailable after ambiguous | PASS — `test_ambiguous_contact_fails_closed` |
| WEBMCP-16 | No GHL calls | PASS — adapter never imports `mg_guide.integrations.ghl`; `/health` reports `live_ghl_calls: 0` |
| WEBMCP-17 | No CRM mutations | PASS — `cloud_mutation: "NONE"` in every response; `/health` reports `live_crm_mutations: 0` |
| WEBMCP-18 | No email sends | PASS — draft tool returns preview text only, `requires_human_send: true`; `/health` reports `real_emails_sent: 0` |
| WEBMCP-19 | No secret values in output | PASS — `test_no_secret_values_in_any_response` |
| WEBMCP-20 | Source contains `document.modelContext.registerTool` | PASS — `test_source_uses_real_webmcp_registration_api`; confirmed present in `webmcp/static/app.js` |

## Live browser acceptance (Playwright-driven Chromium)

Server: `PORT=8092 PYTHONPATH=src python -m mg_guide.webmcp.server`, page
loaded at `http://localhost:8092/`.

### 1. Real WebMCP feature-detection (unsupported case)

Stock Chromium without `document.modelContext` present:

```text
WebMCP status banner: "WebMCP not supported in this browser/agent context.
Human controls remain fully usable."
```

Confirms no fake/emulated WebMCP fallback is claimed.

### 2. Human-operable path (no agent)

- Clicked "Run SUCCESS demo" → processing state became `COMPLETED
  (workflow_status=completed)`; Meeting Context, Relationship Context,
  Follow-Up Planning, and Follow-Up Draft sections all populated.
- Clicked "Run AMBIGUOUS_CONTACT demo" → processing state became
  `NEEDS_REVIEW (workflow_status=blocked)`; Follow-Up Draft section showed
  `NOT_AVAILABLE — RELATIONSHIP_REVIEW_REQUIRED`.

### 3. Simulated WebMCP-supported agent path

A `document.modelContext.registerTool` mock was installed
(`page.addInitScript`) to simulate a WebMCP-capable browser/agent runtime,
then the page was reloaded:

```json
{
  "names": [
    "process_meeting_follow_up",
    "get_current_follow_up_state",
    "get_follow_up_draft"
  ],
  "status": "WebMCP supported — 3 tools registered."
}
```

Agent invocation of `process_meeting_follow_up({"scenario": "SUCCESS"})`
via the registered tool's `execute()`:

```json
{
  "workflow_status": "completed",
  "ux_state": "COMPLETED",
  "meeting_summary": "Discovery call covering retirement income planning with liquidity constraints and a sixty-day timeline.",
  "relationship_status": "matched",
  "salesperson_next_step": "Send recommendation review follow-up (owner: Alex Rivera)",
  "crm_note_status": "NOT_EXECUTED",
  "follow_up_draft_status": "READY"
}
```

Page state after invocation: `#processing-state` textContent =
`"COMPLETED (workflow_status=completed)"` — confirms the tool invocation
visibly updated the page, satisfying WEBMCP-11 and WEBMCP-13.

Agent invocation of `get_current_follow_up_state({})` and
`get_follow_up_draft({})` (via `execute()`):

```json
{
  "status": "PROCESSED",
  "workflow_status": "completed",
  "ux_state": "COMPLETED",
  "follow_up_draft_status": "READY",
  "cloud_mutation": "NONE"
}
```
```json
{
  "status": "READY",
  "recipient_name": "Taylor Morgan",
  "subject": "Follow-up: Taylor Morgan - Discovery Meeting",
  "requires_human_send": true
}
```

Draft panel rendered the recipient, subject, and body preview with
`requires_human_send: true` displayed.

### 4. Fail-closed agent path

Server-side curl reproduction of `process_meeting_follow_up({"scenario":
"AMBIGUOUS_CONTACT"})`:

```json
{
  "workflow_status": "blocked",
  "ux_state": "NEEDS_REVIEW",
  "relationship_status": "ambiguous",
  "crm_note_status": "BLOCKED",
  "follow_up_draft_status": "NOT_AVAILABLE"
}
```

Follow-up `get_follow_up_draft` response:

```json
{"status": "NOT_AVAILABLE", "reason": "RELATIONSHIP_REVIEW_REQUIRED"}
```

Confirms WEBMCP-12 and WEBMCP-15: identity ambiguity fails closed end to
end, through both the human UI and the agent tool path.

## Boundary curl checks

```text
$ curl -sX POST /webmcp/meeting-follow-up -d '{"scenario":"SUCCESS","live":true}'
400 {"error": "authority_field_rejected", "fields": ["live"]}
```

## Deterministic global truth (recorded from `/health` and adapter code)

```text
CURRENT_TRANSCRIPT_SOURCE=synthetic_fixture
REAL_CUSTOMER_DATA=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
EMAILS_SENT=0
R5_STATE=UNCHANGED / OUT_OF_SCOPE
```

## Outstanding (not yet performed at time of this proof)

- Deployment to a public Cloud Run URL (tracked in
  `competition/webmcp/SUBMISSION_CHECKLIST.md`)
- Testing against an actual WebMCP-enabled browser build / real agent client
  (this proof used a scripted mock of `document.modelContext.registerTool`
  to validate the registration and execution contract deterministically;
  real-browser confirmation is a follow-up item before final submission)
