# MG Guide WebMCP Challenge — Competition Delta

```text
COMPETITION=The WebMCP Challenge
DEADLINE_PT=2026-09-03T13:00:00-07:00
DEADLINE_ET=2026-09-03T16:00:00-04:00
MG_GUIDE_BASE_SHA=bc9a723f84e72ec3605da495ad16fbf78f3a99a9
MG_GUIDE_BASE_SHA_DATE=2026-08-31T19:16:51-04:00
AI_ROLODEX_REFERENCE_REPO=themg-max/A.I-Rolodex---Context
AI_ROLODEX_REFERENCE_SHA=3ed7ede9083d7c95d2dbf504c8f0de1e567be4a7
AI_ROLODEX_REFERENCE_SHA_DATE=2026-08-31T14:55:12-04:00
WEBMCP_BRANCH=impl/webmcp-mg-guide-agentic-workspace-001
```

The A.I-Rolodex reference SHA is recorded read-only. That private repository
is not a build, runtime, or deploy dependency for this competition slice.

---

## PRE_EXISTING (as of `MG_GUIDE_BASE_SHA`, not new WebMCP work)

- MG Guide product direction and README narrative
- `meeting_follow_up_v1` deterministic workflow (`src/orchestration/runner.py`,
  `contracts/workflow_states.yaml`)
- Meeting Context Agent, Relationship Context Agent, Follow-Up Planning Agent
  (`src/agents/*`)
- Deterministic policy (`src/orchestration/policy.py`)
- `src/mg_guide/judge_surface/*` — authenticated judge-safe demo adapter,
  scenario catalog (SUCCESS, STAGE_CHANGE_DENIED, AMBIGUOUS_CONTACT), and the
  `project_demo_stages` / `project_ux_experience` / `project_demo_payload`
  presenter projection used again (unmodified) by the new WebMCP adapter
- Google Workspace add-on (`workspace_addon/`, `src/mg_guide/workspace_addon/`)
- Existing Cloud Run judge/add-on infrastructure and Google Cloud Agent
  Runtime hosted orchestrator (`mg-guide-orchestrator`)
- Historical/current HighLevel CRM integration work (`src/integrations/ghl/*`)
- R5 governance machinery and related proof/authorization artifacts
- Existing A.I Rolodex landing site
  (`https://ai-rolodex-landing-831270426395.us-east4.run.app/`)

## NEW_WEBMCP_WORK (added after `MG_GUIDE_BASE_SHA`, this submission period)

- `src/mg_guide/webmcp/` — new public, unauthenticated, synthetic-only WebMCP
  competition adapter package (`app.py`, `scenarios.py`, `server.py`)
    - `WebMCPSurfaceApp`: stateless WSGI app exposing `/health` and `POST
      /webmcp/meeting-follow-up` only
    - Reuses the existing `WorkflowRunner` and existing judge_surface
      `map_packet_to_card` / `project_demo_payload` projections without
      modification
    - Two-value scenario allow-list only (`SUCCESS`, `AMBIGUOUS_CONTACT`);
      rejects any additional/authority field (`live`, `crm_write`,
      `send_email`, `provider`, `contact_id`, `location_id`, `url`,
      `credentials`, `instructions`, `transcript`)
    - Returns the complete safe projected result needed by the browser; no
      server-side session/state endpoint is required
- `webmcp/static/` — new browser-native WebMCP frontend
    - `index.html`, `style.css`: human-operable page with seven required
      sections (Meeting, processing state, Meeting Context, Relationship
      Context, Follow-Up Planning, Follow-Up Draft, Trust boundary)
    - `index.html` uses relative `./style.css`, `./config.js`, and `./app.js`
      so the same frontend can be hosted below the A.I. Rolodex `/mg-guide/`
      path without root-asset collisions
    - `config.js`: runtime configuration shim with same-origin default; the
      private host integration may set only the approved public backend URL
    - `app.js`: real `document.modelContext.registerTool(...)` registration
      of three tools (`process_meeting_follow_up`,
      `get_current_follow_up_state`, `get_follow_up_draft`); feature-detects
      WebMCP support and does not polyfill or emulate it
    - Holds `currentWebMCPState` in browser memory; state/draft tools are
      client-only readers
    - Supports configurable `window.MG_GUIDE_WEBMCP_API_BASE`
- `tests/webmcp/` — new test suite
    - `test_webmcp_app.py`: HTTP-layer acceptance for health, stateless route
      rejection, SUCCESS/AMBIGUOUS_CONTACT, authority-field rejection, CORS,
      and no-secret-leak checks
    - `test_tool_registration_source.py`: static-source checks for the
      required registration API call, feature-detection guard, tool naming,
      schema shape, bounded scenario enum, browser-held state, API-base
      configuration, and subpath-safe host assets
- `deployment/webmcp/Dockerfile` — new competition-only container image,
  built entirely from this public repository, serving the bounded WebMCP
  backend plus optional static frontend for local same-origin testing
- `competition/webmcp/` — this delta, the brief, architecture note, judge
  testing guide, submission checklist, and landing host-integration plan
- `proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md` — acceptance
  evidence with mocked WebMCP registration clearly distinguished from
  actual WebMCP browser proof
- `proof/webmcp/mg-guide-webmcp-live-backend-deployment-acceptance-001.md` —
  acceptance evidence for the live deployed Cloud Run backend
- `proof/webmcp/mg-guide-webmcp-production-acceptance-001.md` — full production
  acceptance proof on the live product URL (`/mg-guide/`) with native WebMCP
  discovery and agent invocation verified

No prior MG Guide work is claimed as new WebMCP work. The WebMCP adapter is
strictly additive: it does not modify `src/mg_guide/judge_surface/*`,
`src/orchestration/*`, `src/agents/*`, or any authentication contract.

## PRODUCTION_HOST_INTEGRATION_AND_ACCEPTANCE (verified this submission period)

```text
STATUS=PROVEN_IN_PRODUCTION
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
```

- **Live Host Surface**: The static WebMCP assets are served directly at
  `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/` with
  `window.MG_GUIDE_WEBMCP_API_BASE` pointing to the dedicated `mg-guide-webmcp`
  backend.
- **Native WebMCP Discovery**: Verified with a real WebMCP-capable browser
  (Google Chrome with native WebMCP testing flag enabled; `document.modelContext`
  native `ModelContext` instance). Exactly three tools discovered:
  1. `process_meeting_follow_up`
  2. `get_current_follow_up_state`
  3. `get_follow_up_draft`
- **Agent Invocation**: Verified via `document.modelContext.executeTool(...)`.
- **SUCCESS flow**: Produces `ux_state=COMPLETED`, `follow_up_draft_status=READY`,
  populates visible page state with meeting summary, matched relationship context,
  and follow-up draft marked `requires_human_send: true`.
- **AMBIGUOUS_CONTACT fail-closed flow**: Produces `ux_state=NEEDS_REVIEW`,
  `follow_up_draft_status=NOT_AVAILABLE`, `reason=RELATIONSHIP_REVIEW_REQUIRED`,
  blocking all CRM and draft actions.
- **Effect Counters**: 0 HighLevel calls, 0 CRM mutations, 0 emails sent, 0 real customer data.

## ADDED_AFTER_INITIAL_PR_432_CORRECTION (same submission period)

```text
CORRECTION_ID=STATELESS_BROWSER_STATE_CORRECTION
HOST_TOPOLOGY=A.I. Rolodex /mg-guide/ + separate bounded backend
```

- Backend made **stateless**: removed process-memory `_last_state`; removed
  server `GET /webmcp/state` and `GET /webmcp/follow-up-draft`
- `POST /webmcp/meeting-follow-up` now returns full safe payload including
  bounded `follow_up_draft` projection
- Frontend holds `currentWebMCPState` in page JS; state/draft tools are
  client-only readers
- Configurable `window.MG_GUIDE_WEBMCP_API_BASE` (same-origin default)
- CORS tightened: explicit allowlist for
  `https://ai-rolodex-landing-831270426395.us-east4.run.app`; no `*`;
  localhost only when `WEBMCP_CORS_MODE=local`
- Acceptance claims corrected: mocked modelContext ≠ actual WebMCP browser proof
- Architecture artifacts updated for A.I. Rolodex host surface reuse
- Subpath-hosting bug repaired: frontend assets now use relative paths and
  load a bounded runtime `config.js` before `app.js`
