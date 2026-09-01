# Devpost Submission Draft — WebMCP Challenge

```text
STATUS=DRAFT_ONLY
FINAL_SUBMISSION_EXECUTED=NO
```

This is a draft for the Devpost submission form. All statements are grounded
in current public evidence — see
[`SUBMISSION_PACKET.md`](SUBMISSION_PACKET.md) and
[`proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md).
No invented metrics, users, revenue, or effects are included below.

## Project tagline

MG Guide exposes a governed meeting-follow-up workflow directly to browser
agents via WebMCP — the agent prepares the work, the person still sends it.

## Project description

MG Guide turns a meeting transcript into structured relationship context and
a governed follow-up plan. For The WebMCP Challenge, the same experience now
exposes three structured, schema-bounded tools directly to a browser agent
via `document.modelContext.registerTool(...)`, live at
`https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`. The
agent can run the workflow and inspect state and draft output; a human
retains sole authority to send anything customer-facing.

## Problem

Meetings are digital, but the work after a meeting — matching it to the
right relationship, deciding the next step, and preparing a follow-up — is
still fragmented across notes, memory, and separate tools, costing time and
delaying a well-informed follow-up.

## Solution

MG Guide's existing `meeting_follow_up_v1` workflow already does this
matching and drafting. The new WebMCP adapter puts that same workflow one
tool call away for a browser agent, on the same page a human already uses,
without requiring a separate agent-specific integration.

## Why WebMCP is a strong fit

WebMCP lets a page expose a small number of narrow, typed, discoverable
tools instead of forcing an agent to infer meaning from arbitrary DOM or
navigation, or requiring a bespoke agent-only API. The agent reads and
updates the same browser-held workflow state the human sees; there is no separate server-side session or agent-only state store.

## How people and agents work together

The agent can invoke the workflow (`process_meeting_follow_up`) and read
state/draft (`get_current_follow_up_state`, `get_follow_up_draft`). Every
follow-up draft carries `requires_human_send: true`. The agent cannot send
email, write to a CRM, or call HighLevel — those actions remain exclusively
human.

## Implementation

- Backend: `src/mg_guide/webmcp/` — a stateless WSGI adapter
  (`WebMCPSurfaceApp`) exposing `GET /health` and `POST
  /webmcp/meeting-follow-up`, reusing the existing `WorkflowRunner` and
  judge-surface projections without modification.
- Frontend: `webmcp/static/` — `index.html`, `style.css`, `config.js`,
  `app.js`; registers three tools via
  `document.modelContext.registerTool(...)`; holds `currentWebMCPState` in
  browser memory; feature-detects WebMCP without polyfilling it.
- Deployment: `deployment/webmcp/Dockerfile` — a competition-only container
  image, deployed as the dedicated `mg-guide-webmcp` Cloud Run backend.
- Host integration: the frontend assets are served from the existing A.I.
  Rolodex Cloud Run site at `/mg-guide/`; the backend is a separate, bounded
  Cloud Run service.

## The exactly 3 tools

1. `process_meeting_follow_up` — runs the bounded synthetic workflow
   (`SUCCESS` or `AMBIGUOUS_CONTACT` only); rejects any authority/live field
   with HTTP 400.
2. `get_current_follow_up_state` — client-only reader of visible workflow
   state; no server call.
3. `get_follow_up_draft` — client-only reader of the generated follow-up
   draft; no server call.

## Live URL

```text
https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

## Public repository

```text
https://github.com/themg-max/mg-guide-agentic-sales-workspace
LICENSE=Apache-2.0
```

## Judge testing instructions

See [`competition/webmcp/JUDGE_TESTING.md`](JUDGE_TESTING.md) for the full
step-by-step judge testing journey, including local setup and live-product
verification steps.

## Existing project vs. new WebMCP work

MG Guide is an existing project (also submitted separately to the Google All
Things Agentic Hackathon). The WebMCP Challenge submission is a new,
additive delta: the WebMCP backend adapter, browser frontend, test suite,
deployment image, and host integration. See
[`competition/webmcp/COMPETITION_DELTA.md`](COMPETITION_DELTA.md) for the
exact pre-existing vs. new-work boundary with commit SHAs.

## Supported / tested WebMCP client

Google Chrome with `--enable-features=WebMCP,ModelContextProtocol` enabled,
exercising `document.modelContext.getTools()`, `registerTool`, and
`executeTool` natively against the live production page — no mocks or
polyfills.

## AI development tools used

VS Code with GitHub Copilot (Copilot CLI runtime) was used throughout
implementation, documentation, and validation of this WebMCP delta.

## Learning questions

- How does a page safely expose write-adjacent capability (running a
  workflow) to a browser agent while keeping the human as the sole authority
  for any customer-facing action?
- How should a stateless backend and browser-held state be divided so an
  agent can read state without requiring server-side sessions?

## Technical challenges

- Keeping the backend fully stateless while still supporting read-only state
  and draft tools required moving state ownership to the browser
  (`currentWebMCPState`) rather than the server.
- Hosting the WebMCP frontend under an existing site's subpath
  (`/mg-guide/`) required relative asset paths and a small runtime
  `config.js` shim so the same public frontend source works both locally
  and on the production host without modification.
- Constraining the tool input surface so that no authority/live field
  (`live`, `crm_write`, `send_email`, credentials, raw transcript, etc.) can
  ever reach the backend, while still allowing a real, useful demo scenario.

## Accomplishments

- Exactly three real, native WebMCP tools registered and verified on a live
  production URL with a real WebMCP-capable browser (no mocks).
- A fail-closed ambiguous-contact path that produces zero draft and zero
  external effect when relationship identity is uncertain.
- A stateless backend with zero secret/credential exposure to browser
  JavaScript, and zero live CRM/email/HighLevel calls anywhere in the
  adapter.

## What comes next

- Finalize and upload the public YouTube demo video.
- Complete the Devpost submission form.
- Final submission remains a human-controlled action.
