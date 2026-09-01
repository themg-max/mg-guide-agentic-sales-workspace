# WebMCP Architecture — MG Guide Competition Adapter

```text
SCOPE=COMPETITION_ADAPTER_ONLY
DOES_NOT_MODIFY=meeting_follow_up_v1 core workflow, judge_surface auth, agents, policy
```

## Topology

```text
PUBLIC MG GUIDE REPO (themg-max/mg-guide-agentic-sales-workspace)
        |
        +-- webmcp/static/           (WebMCP frontend: index.html, style.css, app.js)
        |
        +-- src/mg_guide/webmcp/     (bounded synthetic WebMCP backend adapter)
        |     app.py     -- WebMCPSurfaceApp (WSGI)
        |     scenarios.py -- two-value allow-list (SUCCESS, AMBIGUOUS_CONTACT)
        |     server.py   -- stdlib HTTP server serving API + static files
        |
        +-- deployment/webmcp/Dockerfile  (competition-only container image)
                    |
                    v
        public Cloud Run WebMCP URL
```

This adapter is deliberately separate from `src/mg_guide/judge_surface/*`.
The existing authenticated `/demo/meeting-follow-up` route, its
`_enforce_addon_auth()` gate, and the Google Workspace add-on integration are
untouched. The WebMCP route is a new, smaller, public, read-mostly surface.

## Reuse, not reimplementation

`WebMCPSurfaceApp._process()` calls:

1. `orchestration.runner.WorkflowRunner.run_fixture(...)` — the exact
   deterministic fixture runner already used by judge_surface.
2. `mg_guide.meeting_follow_up_card.mapper.map_packet_to_card(...)` —
   unmodified.
3. `mg_guide.judge_surface.demo_stages.project_demo_payload(...)` —
   unmodified; produces `ux_experience`, including `ux_state`,
   `crm_note_status`, and `follow_up_draft`.

The WebMCP adapter then narrows that payload to the seven public fields
specified by the competition contract (`workflow_status`, `ux_state`,
`meeting_summary`, `relationship_status`, `salesperson_next_step`,
`crm_note_status`, `follow_up_draft_status`) and stores an in-process
snapshot for the `state` and `follow-up-draft` routes.

## Public API surface

| Route | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | liveness + provenance, no auth |
| `/webmcp/meeting-follow-up` | POST | run a bounded synthetic scenario |
| `/webmcp/state` | GET | read the last processed state (no side effects) |
| `/webmcp/follow-up-draft` | GET | read the deterministic draft only |

### Input boundary (`POST /webmcp/meeting-follow-up`)

Accepted body: `{"scenario": "SUCCESS"}` or `{"scenario":
"AMBIGUOUS_CONTACT"}` only.

Rejected (HTTP 400, `authority_field_rejected`): `live`, `crm_write`,
`send_email`, `provider`, `contact_id`, `location_id`, `url`, `credentials`,
`instructions`, `transcript`, or any other unexpected field
(`unexpected_field`).

### State model

State is held in a single in-process Python object
(`WebMCPSurfaceApp._last_state`), guarded by a lock. It is intentionally
**not** persisted to Firestore or any external store — this keeps the demo
bounded to a single Cloud Run instance and avoids any new durable-storage
surface for the competition slice. A fresh process (cold start / redeploy)
resets to `NOT_PROCESSED`.

## Frontend

`webmcp/static/app.js` performs real feature detection:

```js
if (!(window.document && document.modelContext && document.modelContext.registerTool)) {
  // WebMCP unsupported: human controls remain fully usable, no polyfill.
}
```

When supported, it registers exactly three tools using the standards API
`document.modelContext.registerTool(...)`:

1. `process_meeting_follow_up` — `{scenario: "SUCCESS"|"AMBIGUOUS_CONTACT"}`,
   `additionalProperties: false`
2. `get_current_follow_up_state` — empty object schema
3. `get_follow_up_draft` — empty object schema

Each tool's `execute` calls the same-origin `/webmcp/*` JSON API and updates
the same DOM elements a human sees, so agent actions are always visible.

## Security posture

- Same-origin fetches only; no cross-origin calls from tool `execute`.
- Tool descriptions are static, factual strings — never built from
  transcript content, provider output, or server data.
- No `innerHTML` used for untrusted server content; draft body/subject are
  rendered through `textContent`/`escapeHtml`.
- No secrets, tokens, or credentials are ever read by, or exposed to,
  browser JavaScript.
- CORS is permissive (`Access-Control-Allow-Origin: *`) only because the
  surface is a public, read-mostly, synthetic-fixture demo with no
  authentication and no mutation capability of any kind.

## What is intentionally out of scope

- Live Gmail draft/send integration — the `get_follow_up_draft` tool returns
  a text preview only (`requires_human_send: true`).
- HighLevel/CRM calls of any kind.
- The Google Cloud Agent Runtime hosted three-agent orchestrator — this
  adapter runs the same deterministic fixture runner used by judge_surface,
  not a live agent call.
- R5, IAM changes, Terraform changes, or any production governance mutation.
