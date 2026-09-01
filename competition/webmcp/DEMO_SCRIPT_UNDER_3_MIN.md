# Demo Script — Under 3 Minutes

```text
TARGET_RUNTIME=2:30_TO_2:40
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

This is a narration + action script for recording the WebMCP Challenge demo
video. Keep every segment tight — no dead loading time, no long pauses.

## 0:00–0:15 — Open on the live product, already working

**Action**: Show the live MG Guide page already loaded in a WebMCP-capable
browser at `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`.

**Say**:
> "The meeting is digital. The follow-up work after it is still fragmented."

## 0:15–0:35 — Introduce the three WebMCP tools

**Action**: Briefly show `document.modelContext.getTools()` (or the client's
tool list) with exactly three tools visible. Do not read the JSON schemas
aloud.

**Say**:
> "This page registers three WebMCP tools: one runs the follow-up workflow,
> and two let the agent read the state and the draft that are already on
> the page."

## 0:35–1:20 — Run SUCCESS through the actual WebMCP agent path

**Action**: Invoke `process_meeting_follow_up` with `{"scenario": "SUCCESS"}`
through the agent/client (not the human button), and show the page update
live.

**Show**:
- `COMPLETED`
- matched relationship
- recommended next step
- draft `READY`
- `requires_human_send: true`

**Say**:
> "The agent can prepare the work. The person still controls the customer
> action."

## 1:20–1:55 — Run AMBIGUOUS_CONTACT

**Action**: Invoke `process_meeting_follow_up` with `{"scenario":
"AMBIGUOUS_CONTACT"}` through the agent/client.

**Show**:
- `NEEDS_REVIEW`
- `NOT_AVAILABLE`
- `RELATIONSHIP_REVIEW_REQUIRED`

**Say**:
> "When identity is uncertain, MG Guide stops instead of guessing."

## 1:55–2:20 — Why WebMCP matters

**Say**:
> "Same page, same state, structured tools — the human and the agent are
> looking at and acting on the exact same thing. There's no separate
> agent-only interface to build or maintain."

## 2:20–2:40 — Close

**Say**:
> "This is new WebMCP Challenge work on top of an existing product: a live
> product, native browser discovery, real agent invocation, and the human
> still keeps final judgment."

## Do not

- Type long commands live on camera.
- Wait through loading screens — cut dead time in editing.
- Show private terminals, worktrees, or internal tooling.
- Expose any credentials, tokens, or private URLs.
- Claim any CRM write or email send occurred.
- Claim the entire MG Guide system (agents, workflow, judge surface,
  Workspace add-on) was built during the WebMCP Challenge — only the WebMCP
  adapter, frontend, and host integration are new for this challenge.
