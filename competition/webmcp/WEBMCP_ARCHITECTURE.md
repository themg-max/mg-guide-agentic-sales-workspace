# WebMCP Architecture — MG Guide Competition Adapter

```text
SCOPE=COMPETITION_ADAPTER_ONLY
DOES_NOT_MODIFY=meeting_follow_up_v1 core workflow, judge_surface auth, agents, policy
SEPARATE_WEB_SURFACE_REQUIRED=NO
EXISTING_AI_ROLODEX_SURFACE_REUSED=YES
SEPARATE_WEBMCP_BACKEND_BOUNDARY=YES
SERVER_SESSION_STATE_REQUIRED=NO
WEBMCP_BROWSER_STATE=YES
```

## Topology

```text
Judge / browser agent
  -> existing A.I. Rolodex Cloud Run website
     https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
  -> document.modelContext.registerTool(...)
  -> bounded MG Guide WebMCP backend (mg-guide-webmcp)
  -> existing WorkflowRunner
  -> existing Meeting Context / Relationship Context / Follow-Up Planning
  -> synthetic safe result
```

```text
PUBLIC MG GUIDE REPO (themg-max/mg-guide-agentic-sales-workspace)  <-- CANONICAL
        |
        +-- webmcp/static/           (frontend source of truth)
        |
        +-- src/mg_guide/webmcp/     (bounded synthetic WebMCP backend)
        |     app.py     -- WebMCPSurfaceApp (WSGI, *stateless*)
        |     scenarios.py -- two-value allow-list (SUCCESS, AMBIGUOUS_CONTACT)
        |     server.py   -- stdlib HTTP server (API + optional static for local)
        |
        +-- deployment/webmcp/Dockerfile
                    |
                    v
        public Cloud Run backend (mg-guide-webmcp)

PRIVATE A.I. ROLODEX LANDING (themg-max/A.I-Rolodex---Context)
  HOST_INTEGRATION_ONLY
  landing-page/public/mg-guide/  <-- copy of public webmcp/static at known SHA
  window.MG_GUIDE_WEBMCP_API_BASE = <backend URL>
```

The private landing repo is **not** MG Guide domain-logic owner, WebMCP
canonical source, contest runtime authority, or a private-data source.

This adapter is deliberately separate from `src/mg_guide/judge_surface/*`.
The existing authenticated `/demo/meeting-follow-up` route, its
`_enforce_addon_auth()` gate, and the Google Workspace add-on integration are
untouched.

## Stateless backend + browser state

`WebMCPSurfaceApp` holds **no** `_last_state`, no locks, no Firestore, no
cookies, no session database. Every `POST /webmcp/meeting-follow-up` returns
the full safe projected payload, including the bounded draft projection when
READY.

The page holds `currentWebMCPState` in JavaScript memory:

| Tool | Where it runs | Server call? |
| --- | --- | --- |
| `process_meeting_follow_up` | browser tool → `POST /webmcp/meeting-follow-up` | YES |
| `get_current_follow_up_state` | browser tool → reads `currentWebMCPState` | NO |
| `get_follow_up_draft` | browser tool → reads draft from `currentWebMCPState` | NO |

```text
SERVER_SESSION_STATE_REQUIRED=NO
WEBMCP_BROWSER_STATE=YES
```

No sticky routing. No min-instances=1 requirement.

## Reuse, not reimplementation

`WebMCPSurfaceApp._process()` calls:

1. `orchestration.runner.WorkflowRunner.run_fixture(...)`
2. `mg_guide.meeting_follow_up_card.mapper.map_packet_to_card(...)`
3. `mg_guide.judge_surface.demo_stages.project_demo_payload(...)`

## Public API surface

| Route | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | liveness + provenance, no auth |
| `/webmcp/meeting-follow-up` | POST | run a bounded synthetic scenario; returns full safe payload |

### Input boundary (`POST /webmcp/meeting-follow-up`)

Accepted body: `{"scenario": "SUCCESS"}` or `{"scenario":
"AMBIGUOUS_CONTACT"}` only.

Rejected (HTTP 400, `authority_field_rejected`): `live`, `crm_write`,
`send_email`, `provider`, `contact_id`, `location_id`, `url`, `credentials`,
`instructions`, `transcript`, or any other unexpected field.

### Response fields (safe projection)

`status`, `scenario`, `workflow_status`, `ux_state`, `meeting_summary`,
`relationship_status`, `salesperson_next_step`, `crm_note_status`,
`follow_up_draft_status`, `follow_up_draft` (bounded: status / recipient_name /
subject / body_preview / requires_human_send or NOT_AVAILABLE),
`external_effects`, `cloud_mutation`.

## Frontend configuration

```js
// Production (set by landing host before app.js):
window.MG_GUIDE_WEBMCP_API_BASE = "https://<mg-guide-webmcp-backend>";

// Local same-origin fallback when unset:
const API_BASE = "";
```

No credentials in browser source.

## CORS

Production allowlist (default):

- `https://ai-rolodex-landing-831270426395.us-east4.run.app`

Additional origins via `WEBMCP_CORS_ORIGINS` (comma-separated).

`WEBMCP_CORS_MODE=local` additionally permits `http://localhost:*` and
`http://127.0.0.1:*`. Production containers set `WEBMCP_CORS_MODE=production`.

**No** `Access-Control-Allow-Origin: *`.

## Security posture

- Tool descriptions are static, factual strings.
- Draft body/subject rendered through `textContent` / `escapeHtml`.
- No secrets, tokens, or credentials exposed to browser JavaScript.
- No HighLevel, CRM mutation, or email send paths in this adapter.

## What is intentionally out of scope

- Live Gmail draft/send
- HighLevel/CRM calls
- Live Agent Runtime three-agent orchestrator calls (fixture runner only)
- R5, IAM, Terraform, production governance mutation
