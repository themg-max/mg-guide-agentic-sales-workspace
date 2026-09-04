# MG Guide WebMCP Challenge — Competition Delta

```text
COMPETITION=The WebMCP Challenge
SUBMISSION_PERIOD_START=2026-08-25T12:00:00-07:00
DEADLINE_PT=2026-09-04T01:00:00-07:00
DEADLINE_ET=2026-09-04T04:00:00-04:00
DEADLINE_UTC=2026-09-04T08:00:00Z
DEADLINE_SOURCE=Devpost 12-hour extension announced 2026-09-03
PROJECT_STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
MG_GUIDE_BASE_SHA=bc9a723f84e72ec3605da495ad16fbf78f3a99a9
MG_GUIDE_BASE_SHA_DATE=2026-08-31T19:16:51-04:00
AI_ROLODEX_REFERENCE_REPO=themg-max/A.I-Rolodex---Context
AI_ROLODEX_REFERENCE_SHA=3ed7ede9083d7c95d2dbf504c8f0de1e567be4a7
AI_ROLODEX_REFERENCE_SHA_DATE=2026-08-31T14:55:12-04:00
WEBMCP_INITIAL_BRANCH=impl/webmcp-mg-guide-agentic-workspace-001
```

The official submission deadline was extended by Devpost/OpenAI from the
original September 3 deadline to **September 4, 2026 at 1:00 AM PT / 4:00 AM
ET**. The timestamps above use that final announced deadline.

The A.I-Rolodex reference SHA is recorded read-only. That private repository
is not a build, runtime, or deploy dependency for this competition slice.

`MG_GUIDE_BASE_SHA` is the recorded **pre-WebMCP implementation baseline** used
for this repository delta. It does not imply that the repository was frozen at
the August 25 challenge start. Challenge-period evidence is tracked separately
in [`CHALLENGE_PERIOD_EVIDENCE.md`](CHALLENGE_PERIOD_EVIDENCE.md).

---

## PRE_EXISTING — MG Guide foundation

The following capabilities existed before the WebMCP extension and are not
claimed as new challenge work:

- MG Guide product direction and core meeting-follow-up domain;
- `meeting_follow_up_v1` deterministic workflow (`src/orchestration/runner.py`,
  `contracts/workflow_states.yaml`);
- Meeting Context Agent, Relationship Context Agent, and Follow-Up Planning
  Agent (`src/agents/*`);
- deterministic policy (`src/orchestration/policy.py`);
- authenticated judge-safe presentation/adaptor capabilities under
  `src/mg_guide/judge_surface/*`, including the scenario model and projection
  functions used by the broader MG Guide demo experience;
- Google Workspace add-on (`workspace_addon/`, `src/mg_guide/workspace_addon/`);
- existing Cloud Run judge/add-on infrastructure and Google Cloud Agent
  Runtime hosted orchestrator (`mg-guide-orchestrator`);
- historical/current HighLevel CRM integration work (`src/integrations/ghl/*`);
- R5 governance machinery and related proof/authorization artifacts;
- existing A.I. Rolodex landing site
  (`https://ai-rolodex-landing-831270426395.us-east4.run.app/`).

The WebMCP challenge does **not** claim these foundational capabilities as new.

---

## NEW_WEBMCP_WORK — meaningful challenge-period extension

The WebMCP extension is additive around the existing MG Guide workflow and
agents. It does not replace the core `meeting_follow_up_v1` orchestration,
Meeting Context / Relationship Context / Follow-Up Planning agents, or
deterministic policy.

During the challenge period, the existing judge-safe presentation projection
was also **narrowly extended** to support the stronger deterministic follow-up
draft and shared WebMCP-facing presentation semantics used by the new browser
surface. This is why the baseline-to-current diff includes changes in
`src/mg_guide/judge_surface/demo_stages.py` and its tests. Those targeted
presentation changes are part of the WebMCP integration; they are not a rewrite
of the underlying workflow, agent graph, or policy engine.

### Layer 1 — Browser-agent contract

- Added real `document.modelContext.registerTool(...)` registration in
  `webmcp/static/app.js`.
- Exposed exactly three tools:
  1. `process_meeting_follow_up` — **ACTION**
  2. `get_current_follow_up_state` — **STATE**
  3. `get_follow_up_draft` — **ARTIFACT**
- Feature-detects native WebMCP support instead of polyfilling/emulating it.
- Uses narrow input schemas and does not expose autonomous email-send or CRM
  mutation tools.

### Layer 2 — New Web product surface

- Added `webmcp/static/` as a browser-native WebMCP frontend.
- Added a human-operable MG Guide page where person and agent share the same
  visible workflow state.
- Added `currentWebMCPState` in browser memory so STATE and ARTIFACT tools can
  inspect the current result without rerunning the workflow.
- Added host-safe relative assets and runtime `config.js` for the existing
  `/mg-guide/` product path.
- Added browser-local Agent Activity presentation and explicit
  **ACTION → STATE → ARTIFACT → HUMAN CONTROL** framing.

### Layer 3 — Bounded WebMCP adapter

- Added `src/mg_guide/webmcp/` with `app.py`, `scenarios.py`, and `server.py`.
- Added `WebMCPSurfaceApp`, a stateless WSGI application exposing only
  `/health` and `POST /webmcp/meeting-follow-up`.
- Reuses the existing `WorkflowRunner` and judge-safe output projections rather
  than duplicating the core workflow.
- Accepts only `SUCCESS` and `AMBIGUOUS_CONTACT` scenarios.
- Rejects authority-bearing/unbounded fields including `live`, `crm_write`,
  `send_email`, `provider`, `contact_id`, `location_id`, `url`, `credentials`,
  `instructions`, and arbitrary `transcript` input.
- Returns the complete safe projected browser payload with no server-side
  session/state dependency.

### Layer 4 — Safety and experience model

- Added deterministic follow-up draft projection for the WebMCP SUCCESS path.
- Every usable draft preserves `requires_human_send=true`.
- Added fail-closed `AMBIGUOUS_CONTACT` experience:
  `NEEDS_REVIEW → draft NOT_AVAILABLE → RELATIONSHIP_REVIEW_REQUIRED`.
- Improved latest-run/browser presentation semantics so a second invocation
  does not expose stale state from the first run.
- Preserved competition effect counters:

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

### Layer 5 — Test / deploy / proof surface

- Added `tests/webmcp/` for WebMCP-specific source, HTTP, presentation,
  multi-run, CORS, authority-field rejection, and no-secret-leak validation.
- Added `deployment/webmcp/Dockerfile` for the bounded competition backend.
- Added `competition/webmcp/` judge, architecture, delta, testing, demo, and
  submission materials.
- Added `proof/webmcp/` production/native acceptance evidence.
- Integrated the frontend on the existing A.I. Rolodex `/mg-guide/` host and a
  separate bounded `mg-guide-webmcp` backend.
- Verified native browser discovery and invocation of exactly three tools.

This five-layer delta changes **how an AI agent can safely interact with the MG
Guide web product**. It is not a documentation-only relabeling of pre-existing
MG Guide functionality.

---

## PRODUCTION_HOST_INTEGRATION_AND_ACCEPTANCE

```text
STATUS=PROVEN_IN_PRODUCTION
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
```

- **Live Host Surface:** WebMCP assets are served at the existing MG Guide
  `/mg-guide/` path with a bounded backend URL configured at runtime.
- **Native WebMCP Discovery:** Verified with a real WebMCP-capable browser.
  Exactly three tools were discovered.
- **Agent Invocation:** Verified through native WebMCP execution.
- **SUCCESS:** `ux_state=COMPLETED`, relationship matched, draft `READY`, and
  `requires_human_send=true`.
- **AMBIGUOUS_CONTACT:** `ux_state=NEEDS_REVIEW`, draft `NOT_AVAILABLE`, reason
  `RELATIONSHIP_REVIEW_REQUIRED`, and zero external effects.
- **Effect Counters:** 0 HighLevel calls, 0 CRM mutations, 0 emails sent, 0
  real customer data.

---

## CORRECTIONS AND HARDENING AFTER THE INITIAL WEBMCP MERGE

```text
CORRECTION_ID=STATELESS_BROWSER_STATE_AND_PRESENTATION_HARDENING
HOST_TOPOLOGY=A.I. Rolodex /mg-guide/ + separate bounded backend
```

Challenge-period follow-up work after the initial WebMCP merge included:

- backend made stateless by removing process-memory `_last_state` and server
  state/draft GET endpoints;
- `POST /webmcp/meeting-follow-up` returns the complete safe payload;
- browser-held `currentWebMCPState` powers read-only STATE and ARTIFACT tools;
- configurable `window.MG_GUIDE_WEBMCP_API_BASE` with same-origin default;
- CORS restricted to the production host, with localhost allowed only in local
  mode;
- acceptance semantics corrected so mocked modelContext evidence is not
  represented as native browser proof;
- `/mg-guide/` subpath asset loading repaired with relative asset URLs;
- deterministic follow-up draft quality improved;
- browser-local Agent Activity and ACTION / STATE / ARTIFACT framing added;
- multi-run presentation logic corrected to prevent stale state;
- judge-facing frontend presentation elevated without changing the exact
  three-tool contract.

---

## Boundary statement

No pre-existing MG Guide workflow, agent, policy, Workspace, CRM, or broader
cloud architecture is represented as newly created for The WebMCP Challenge.
The new work is the WebMCP browser-agent contract, browser product surface,
bounded adapter, safety/experience integration, and dedicated test/deploy/proof
surface described above.

For dated commit/PR evidence, see
[`CHALLENGE_PERIOD_EVIDENCE.md`](CHALLENGE_PERIOD_EVIDENCE.md).
