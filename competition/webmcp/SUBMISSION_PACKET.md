# MG Guide | Agent-Native Follow-Up — WebMCP Submission Packet

```text
PROJECT_NAME=MG Guide | Agent-Native Follow-Up
COMPETITION=The WebMCP Challenge
STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
PUBLIC_SOURCE_SHA=2847f5a26dbc61716736b60eedb66e399c102a33
LICENSE=Apache-2.0
```

This document is the primary control document for the WebMCP Challenge
submission. It consolidates the problem, solution, live evidence, and
remaining human-controlled submission steps in one place.

## A. Problem

Before COVID, much financial-services relationship work happened face to
face. Today many of those conversations happen online, and the meeting
itself is captured digitally. But the work *after* the meeting — matching
the conversation to the right relationship context, deciding the right next
step, and drafting a follow-up — is still fragmented across notes, memory,
and separate tools. That gap costs salespeople time and costs customers a
prompt, well-informed follow-up.

## B. Solution

MG Guide already turns a meeting transcript into structured relationship
context and a governed follow-up plan (`meeting_follow_up_v1`): it matches
the meeting to a relationship, produces a recommended next step, and
prepares a follow-up draft — while keeping a human in control of anything
customer-facing.

For The WebMCP Challenge, MG Guide adds a new, bounded, browser-native agent
interface to that same experience. A browser agent can now discover and
invoke the same workflow directly on the page a human already sees, using
standard WebMCP tools instead of a separate agent-specific integration.

## C. Why WebMCP

Without WebMCP, giving an agent access to this workflow would mean either:

- building and maintaining a separate, agent-specific API/interface, or
- asking the agent to infer meaning from arbitrary page DOM/navigation,
  which is brittle and impossible to bound safely.

WebMCP lets the same page expose a small number of structured, schema-bounded
tools directly to the agent, via `document.modelContext.registerTool(...)`.
The agent gets a narrow, typed, discoverable contract — not free rein over
the page — and the human sees the exact same state the agent is acting on,
in real time, in the same browser tab. This keeps the human and the agent
working from one shared source of truth instead of two divergent surfaces.

## D. Live product

```text
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

Production host integration is complete. The page is served from the
existing A.I. Rolodex Cloud Run site, with a separate bounded backend
(`mg-guide-webmcp`) providing the stateless synthetic API.

## E. Public source

```text
REPOSITORY=https://github.com/themg-max/mg-guide-agentic-sales-workspace
LICENSE=Apache-2.0
PUBLIC_SOURCE_SHA=2847f5a26dbc61716736b60eedb66e399c102a33
```

The public repository is the canonical source for all WebMCP code: the
backend adapter (`src/mg_guide/webmcp/`), the browser frontend
(`webmcp/static/`), and the automated test suite (`tests/webmcp/`).

## F. Exactly three tools

### 1. `process_meeting_follow_up`

- **Purpose**: runs the `meeting_follow_up_v1` workflow against a bounded
  synthetic scenario (`SUCCESS` or `AMBIGUOUS_CONTACT`).
- **Human-visible effect**: the same page the human sees updates live —
  Meeting Context, Relationship Context, and Follow-Up Planning sections
  populate, and the Follow-Up Draft section either becomes `READY` or shows
  `NOT_AVAILABLE — RELATIONSHIP_REVIEW_REQUIRED`.
- **Safety boundary**: accepts only `{"scenario": "SUCCESS" |
  "AMBIGUOUS_CONTACT"}`; any additional/authority field (`live`,
  `crm_write`, `send_email`, `provider`, `contact_id`, `location_id`, `url`,
  `credentials`, `instructions`, `transcript`) is rejected with HTTP 400.

### 2. `get_current_follow_up_state`

- **Purpose**: reads the current visible workflow state without rerunning
  the workflow.
- **Human-visible effect**: none — read-only inspection of state already
  shown on the page.
- **Safety boundary**: client-only reader; no server call; cannot mutate
  anything.

### 3. `get_follow_up_draft`

- **Purpose**: reads the deterministic follow-up draft already produced by
  the existing projection.
- **Human-visible effect**: none — read-only inspection of the draft already
  shown on the page.
- **Safety boundary**: client-only reader; returns `NOT_AVAILABLE` when no
  draft exists (e.g. after `AMBIGUOUS_CONTACT`); never sends anything.

## G. SUCCESS

```text
meeting context
  -> matched relationship
  -> follow-up plan
  -> draft READY
  -> requires_human_send=true
```

Invoking `process_meeting_follow_up({"scenario": "SUCCESS"})` produces
`ux_state=COMPLETED`, matches the meeting to a relationship, recommends a
salesperson next step, and marks the follow-up draft `READY` with
`requires_human_send: true`. The agent can prepare the work; a human must
still review and send anything customer-facing.

## H. AMBIGUOUS_CONTACT

```text
ambiguous relationship
  -> NEEDS_REVIEW
  -> draft NOT_AVAILABLE
  -> RELATIONSHIP_REVIEW_REQUIRED
  -> no external effect
```

Invoking `process_meeting_follow_up({"scenario": "AMBIGUOUS_CONTACT"})`
produces `ux_state=NEEDS_REVIEW`, `follow_up_draft_status=NOT_AVAILABLE`,
`reason=RELATIONSHIP_REVIEW_REQUIRED`. No draft is produced, no CRM action is
taken, and no email is sent. When relationship identity is uncertain, the
system stops instead of guessing.

## I. Human + agent collaboration

The human and the agent operate on the exact same browser-held state
(`currentWebMCPState`) on the exact same page — there is no separate
agent-only surface. The agent can invoke the workflow and read state/draft
tools; it can never send a customer-facing email or write to a CRM. Every
follow-up draft is tagged `requires_human_send: true`, and only a human can
act on it.

## J. Competition Delta

```text
PRE_EXISTING_MG_GUIDE:
  meeting_follow_up_v1 workflow, agents, policy, judge_surface adapter,
  Workspace add-on, existing A.I. Rolodex landing site, existing Cloud Run
  judge/add-on infrastructure

NEW_WEBMCP_CHALLENGE_WORK:
  src/mg_guide/webmcp/ (bounded stateless backend adapter)
  webmcp/static/ (browser-native WebMCP frontend, 3 registered tools)
  tests/webmcp/ (new automated test suite)
  deployment/webmcp/Dockerfile (new competition-only container image)
  competition/webmcp/ (this delta, brief, architecture, judge testing,
    submission checklist and packet, landing integration record)
  proof/webmcp/ (end-to-end and production acceptance proof)
```

Full detail with commit SHAs:
[`competition/webmcp/COMPETITION_DELTA.md`](COMPETITION_DELTA.md).

## K. Proof links

- Production acceptance:
  [`proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md)
- End-to-end acceptance:
  [`proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md)
- Judge testing:
  [`competition/webmcp/JUDGE_TESTING.md`](JUDGE_TESTING.md)

## L. Remaining submission operations

The following remain as human-controlled steps only; no technical/runtime
work remains:

1. Finalize the under-3-minute demo video (with audio).
2. Upload the public YouTube video.
3. Complete the Devpost submission form.
4. Final submission remains a human-controlled action.
