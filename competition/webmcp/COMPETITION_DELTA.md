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
    - `WebMCPSurfaceApp`: WSGI app exposing `/health`, `POST
      /webmcp/meeting-follow-up`, `GET /webmcp/state`, `GET
      /webmcp/follow-up-draft`
    - Reuses the existing `WorkflowRunner` and existing judge_surface
      `map_packet_to_card` / `project_demo_payload` projections without
      modification
    - Two-value scenario allow-list only (`SUCCESS`, `AMBIGUOUS_CONTACT`);
      rejects any additional/authority field (`live`, `crm_write`,
      `send_email`, `provider`, `contact_id`, `location_id`, `url`,
      `credentials`, `instructions`, `transcript`)
- `webmcp/static/` — new browser-native WebMCP frontend
    - `index.html`, `style.css`: human-operable page with seven required
      sections (Meeting, processing state, Meeting Context, Relationship
      Context, Follow-Up Planning, Follow-Up Draft, Trust boundary)
    - `app.js`: real `document.modelContext.registerTool(...)` registration
      of three tools (`process_meeting_follow_up`,
      `get_current_follow_up_state`, `get_follow_up_draft`); feature-detects
      WebMCP support and does not polyfill or emulate it
- `tests/webmcp/` — new test suite
    - `test_webmcp_app.py`: HTTP-layer acceptance for health, state,
      SUCCESS/AMBIGUOUS_CONTACT flows, authority-field rejection, and
      no-secret-leak checks
    - `test_tool_registration_source.py`: static-source checks for the
      required registration API call, feature-detection guard, tool naming,
      schema shape, and scenario enum bound
- `deployment/webmcp/Dockerfile` — new competition-only container image,
  built entirely from this public repository, serving both the static
  frontend and the bounded WebMCP JSON API
- `competition/webmcp/` — this delta, the brief, the architecture note, the
  judge testing guide, and the submission checklist
- `proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md` — end-to-end
  acceptance evidence

No prior MG Guide work is claimed as new WebMCP work. The WebMCP adapter is
strictly additive: it does not modify `src/mg_guide/judge_surface/*`,
`src/orchestration/*`, `src/agents/*`, or any authentication contract.
