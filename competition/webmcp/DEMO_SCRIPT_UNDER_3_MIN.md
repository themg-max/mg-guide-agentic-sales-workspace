# Demo Script — WebMCP Challenge (<3 Minutes)

```text
TARGET_RUNTIME=2:35_TO_2:50
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
PRIMARY_STORY=ACTION_STATE_ARTIFACT_HUMAN_CONTROL
```

The goal is to show a working WebMCP experience immediately, demonstrate all
three native tools, show one useful success path and one meaningful safe stop,
and finish with why this is better than DOM guessing or a separate agent-only
integration.

## 0:00–0:12 — Open on the working live product

**Action:** Start with the live MG Guide page already loaded in a WebMCP-capable
browser. No title card, setup screen, login flow, or terminal.

**Say:**

> "A meeting can be digital, but the follow-up work after it is still
> fragmented. MG Guide turns that work into a structured human-and-agent
> workflow."

On-screen text, if useful:

```text
Meeting → relationship context → follow-up plan → draft
```

## 0:12–0:28 — Show exactly three native WebMCP tools

**Action:** Show the browser agent's native tool list with exactly these names:

1. `process_meeting_follow_up`
2. `get_current_follow_up_state`
3. `get_follow_up_draft`

Do not read schemas or JSON aloud.

**Say:**

> "The page exposes three WebMCP tools: ACTION runs the workflow, STATE reads
> the current result, and ARTIFACT reads the prepared follow-up draft."

On-screen text:

```text
ACTION → STATE → ARTIFACT
```

## 0:28–1:08 — ACTION: run SUCCESS through the agent

**Action:** Ask the browser agent to use `process_meeting_follow_up` with the
`SUCCESS` scenario. Show the page update visibly.

**Show:**

- workflow `COMPLETED`;
- relationship `matched`;
- recommended next step;
- follow-up draft `READY`;
- `requires_human_send=true`.

**Say:**

> "The agent invokes the same follow-up capability the person sees on the
> page. It resolves the synthetic relationship, prepares the next step, and
> creates a deterministic follow-up draft."

## 1:08–1:32 — STATE + ARTIFACT: read what is already on the page

**Action:** Have the agent call:

- `get_current_follow_up_state`; then
- `get_follow_up_draft`.

Briefly show the returned state and draft alongside the same human-visible
page state.

**Say:**

> "The other two tools do not rerun the workflow. They read the same browser
> state the person is looking at. The draft is ready, but it still requires a
> human to review and send it."

On-screen text:

```text
Agent can prepare. Only a person can review and send.
```

## 1:32–2:02 — Safe stop: AMBIGUOUS_CONTACT

**Action:** Ask the agent to run `process_meeting_follow_up` with
`AMBIGUOUS_CONTACT`, then ask whether a draft is available.

**Show:**

- `NEEDS_REVIEW`;
- relationship `ambiguous`;
- draft `NOT_AVAILABLE`;
- `RELATIONSHIP_REVIEW_REQUIRED`.

**Say:**

> "When relationship identity is uncertain, MG Guide stops instead of
> guessing. There is no draft, no CRM mutation, and no email send."

## 2:02–2:30 — Why WebMCP is the right interface

**Action:** Keep the live product visible; optionally flash the three tool
names again.

**Say:**

> "Without WebMCP, an agent would need a separate integration or would have
> to infer meaning from page structure and navigation. Here the website
> declares a small, typed tool contract, and the human and agent work from the
> same visible state."

## 2:30–2:48 — Close on the competition delta

**Say:**

> "MG Guide existed before this challenge. The new WebMCP work is the
> browser-native tool layer, bounded adapter, tests, live host integration,
> and native agent experience. MG Guide turns post-meeting follow-up into a
> safe agent-human workflow: action, state, artifact, then human control."

End on the live product, not a terminal or slide.

---

## Capture checklist

Before recording, verify:

- the live URL is already loaded in the WebMCP-capable browser;
- exactly three native tools are discoverable;
- SUCCESS completes;
- both read tools return the current state/draft;
- AMBIGUOUS_CONTACT fails closed;
- no stale state remains between scenarios;
- the draft still shows `requires_human_send=true`;
- the browser viewport has no clipping or horizontal overflow;
- no credentials, private URLs, terminals, worktrees, or internal governance
  surfaces appear in frame.

## Do not show or claim

- Do not film setup, sign-in, dependency installation, build logs, Cloud Run
  recovery work, or internal governance.
- Do not spend demo time explaining Agent Activity internals.
- Do not claim a live CRM write, email send, or HighLevel call occurred.
- Do not claim the broader MG Guide agents/workflow were created during the
  WebMCP Challenge.
- Do not imply autonomous customer-facing authority.
- Do not use copyrighted music or third-party material without permission.

The video should be public on YouTube, include clear audio, remain under three
minutes, and show the working project and actual WebMCP use.
