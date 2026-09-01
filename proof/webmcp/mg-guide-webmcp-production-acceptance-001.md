# MG Guide WebMCP Production Acceptance 001

```text
PROOF_ID=MG_GUIDE_WEBMCP_PRODUCTION_ACCEPTANCE_001
RECORDED_AT_UTC=2026-09-01T21:40:00Z
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PUBLIC_SOURCE_SHA=2847f5a26dbc61716736b60eedb66e399c102a33

LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
PRODUCT_PATH=/mg-guide/
```

## 1. Verified Live Host Surface

The MG Guide WebMCP frontend assets (`index.html`, `style.css`, `app.js`, `config.js`)
built from public source `2847f5a26dbc61716736b60eedb66e399c102a33` are fully
integrated and serving live at the production product origin.

```text
STABLE_ORIGIN_ROUTES:
  /               = HTTP 200
  /mg-guide/      = HTTP 200
  /mg-guide/style.css  = HTTP 200
  /mg-guide/config.js  = HTTP 200
  /mg-guide/app.js     = HTTP 200
  /privacy        = HTTP 200
  /terms          = HTTP 200
```

`config.js` on the live host binds only the approved stateless public backend URL:

```js
window.MG_GUIDE_WEBMCP_API_BASE =
  "https://mg-guide-webmcp-831270426395.us-east4.run.app";
```

## 2. Real WebMCP Native Tool Discovery

Tested using a real, supported WebMCP client (Google Chrome with
`--enable-features=WebMCP,ModelContextProtocol` enabled, operating on the live
production page URL without mocks or polyfills).

`document.modelContext` evaluated as a native `ModelContext` object with standard
methods (`getTools`, `registerTool`, `executeTool`, `ontoolchange`).

### Discovered Tools (Exactly 3)

```text
document.modelContext.getTools() ->
  1. process_meeting_follow_up
  2. get_current_follow_up_state
  3. get_follow_up_draft
```

```text
EXACT_TOOL_NAMES=["process_meeting_follow_up", "get_current_follow_up_state", "get_follow_up_draft"]
TOOL_COUNT=3
WEBMCP_BROWSER_DISCOVERY=PASS
```

## 3. WebMCP Agent Invocation & Workflow Flows

### SUCCESS Flow

Invoked `process_meeting_follow_up` with `{"scenario": "SUCCESS"}` via
`document.modelContext.executeTool(...)`:

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

Read tools inspection:
- `get_current_follow_up_state` -> `status: PROCESSED`, `ux_state: COMPLETED`, `cloud_mutation: NONE`
- `get_follow_up_draft` -> `status: READY`, `recipient_name: Taylor Morgan`, `requires_human_send: true`

```text
WEBMCP_AGENT_INVOCATION=PASS
WEBMCP_SUCCESS_FLOW=PASS
```

### AMBIGUOUS_CONTACT Fail-Closed Flow

Invoked `process_meeting_follow_up` with `{"scenario": "AMBIGUOUS_CONTACT"}` via
`document.modelContext.executeTool(...)`:

```json
{
  "workflow_status": "blocked",
  "ux_state": "NEEDS_REVIEW",
  "meeting_summary": "High-level conversation without unique contact identifiers.",
  "relationship_status": "ambiguous",
  "salesperson_next_step": "Resolve contact identity offline before any CRM write.",
  "crm_note_status": "BLOCKED",
  "follow_up_draft_status": "NOT_AVAILABLE"
}
```

Read tools inspection:
- `get_current_follow_up_state` -> `status: PROCESSED`, `ux_state: NEEDS_REVIEW`, `crm_note_status: BLOCKED`, `cloud_mutation: NONE`
- `get_follow_up_draft` -> `status: NOT_AVAILABLE`, `reason: RELATIONSHIP_REVIEW_REQUIRED`

```text
WEBMCP_AMBIGUOUS_FAIL_CLOSED=PASS
```

## 4. Human-Operable Path (Live Product Origin)

Verified via direct browser UI interaction on the live page:
- "Run SUCCESS demo" button: updates page state to `COMPLETED` with follow-up draft rendered.
- "Run AMBIGUOUS_CONTACT demo" button: updates page state to `NEEDS_REVIEW` with `NOT_AVAILABLE — RELATIONSHIP_REVIEW_REQUIRED` draft notice.
- `requires_human_send: true` enforced on all follow-up drafts.

## 5. Effect Counters

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
SECRET_PAYLOAD_READS=0
REAL_CUSTOMER_DATA=0
```

## 6. Summary of Acceptance Status

| Item | Result |
| --- | --- |
| Live Product Route Resolution | PASS |
| Static Asset Hash & Config Integrity | PASS |
| CORS Origin Boundary | PASS |
| Native WebMCP Tool Discovery (3 tools) | PASS |
| Native WebMCP Agent Invocation | PASS |
| SUCCESS Scenario Execution | PASS |
| AMBIGUOUS_CONTACT Fail-Closed Execution | PASS |
| Human Send Safety Boundary | PASS |
| Zero Live External Effects | PASS |
| Final Acceptance Status | **PASS** |
