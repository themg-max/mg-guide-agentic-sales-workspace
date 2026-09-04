# MG Guide | Agent-Native Follow-Up — WebMCP Judge Start

**Live demo:** https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/

**Public source:** https://github.com/themg-max/mg-guide-agentic-sales-workspace

**WebMCP implementation:** [`webmcp/static/app.js`](../../webmcp/static/app.js)

**Trust boundary:** **Agent can prepare. Only a person can review and send.**

---

## Judge path

**Required first reading:**

1. This page — [`README.md`](README.md)
2. [`WEBMCP_ARCHITECTURE.md`](WEBMCP_ARCHITECTURE.md)
3. [`JUDGE_TESTING.md`](JUDGE_TESTING.md)
4. [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md)
5. [`LESSONS_AND_FUTURE_DIRECTION.md`](LESSONS_AND_FUTURE_DIRECTION.md)

**Supporting engineering / submission evidence (not required first reading):**

- [`CHALLENGE_PERIOD_EVIDENCE.md`](CHALLENGE_PERIOD_EVIDENCE.md)
- [`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md)
- [`DEVPOST_SUBMISSION_DRAFT.md`](DEVPOST_SUBMISSION_DRAFT.md)
- [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md)
- [`SUBMISSION_PACKET.md`](SUBMISSION_PACKET.md)
- [`COMPETITION_BRIEF.md`](COMPETITION_BRIEF.md)
- [`AGENT_ACTIVITY_PRESENTATION_ACCEPTANCE.md`](AGENT_ACTIVITY_PRESENTATION_ACCEPTANCE.md)
- [`DEMO_CAPTURE_CHECKLIST.md`](DEMO_CAPTURE_CHECKLIST.md)
- [`DEMO_DRAFT_QUALITY_ACCEPTANCE.md`](DEMO_DRAFT_QUALITY_ACCEPTANCE.md)
- [`FRONTEND_DEMO_ELEVATION_PLAN.md`](FRONTEND_DEMO_ELEVATION_PLAN.md)
- [`LANDING_INTEGRATION_PLAN.md`](LANDING_INTEGRATION_PLAN.md)

---

## What this project is

MG Guide turns a meeting transcript into structured relationship context, a
recommended follow-up plan, and a deterministic follow-up draft. The broader
MG Guide product existed before the WebMCP Challenge.

For this challenge, we added a browser-native WebMCP layer so the same page a
person uses exposes a small, typed tool surface directly to an AI agent. The
agent does not need to scrape the DOM, guess which button to click, or use a
separate agent-only interface.

The WebMCP challenge delta is intentionally bounded and easy to inspect:

1. `process_meeting_follow_up` — **ACTION** — run one approved synthetic
   meeting-follow-up scenario.
2. `get_current_follow_up_state` — **STATE** — read the current browser-held
   workflow state without rerunning the workflow.
3. `get_follow_up_draft` — **ARTIFACT** — read the follow-up draft already
   prepared on the page.

Exactly three tools are registered via `document.modelContext.registerTool`.
There is no fourth tool, no autonomous send action, and no CRM-write tool.

---

## Fastest judge journey

Use either:

- ChatGPT's in-app browser, which supports WebMCP; or
- Google Chrome 149+ with `chrome://flags/#enable-webmcp-testing` enabled and
  the browser restarted.

Open the live demo and ask the browser agent:

> Use the site's WebMCP tools to process the SUCCESS meeting. Then read the
> current follow-up state and the follow-up draft.

Expected result:

```text
SUCCESS
→ relationship matched
→ workflow COMPLETED
→ follow-up draft READY
→ requires_human_send=true
```

Then ask:

> Now process AMBIGUOUS_CONTACT and tell me whether a follow-up draft is
> available.

Expected result:

```text
AMBIGUOUS_CONTACT
→ relationship ambiguous
→ NEEDS_REVIEW
→ draft NOT_AVAILABLE
→ RELATIONSHIP_REVIEW_REQUIRED
→ no external effect
```

Full steps: [`JUDGE_TESTING.md`](JUDGE_TESTING.md).

---

## Why WebMCP matters here

Post-meeting follow-up is a natural human-agent collaboration problem. A
salesperson still owns judgment, relationship context, and customer-facing
action, while an agent can remove repetitive navigation and preparation.

Without WebMCP, an agent would need either a separate integration or brittle
UI/DOM inference. With WebMCP, the website declares exactly which capabilities
are available, the input schemas are narrow, and the human and agent operate
on the same visible page state.

That makes the experience better in four ways:

- **Discoverable:** the agent sees named tools instead of guessing from UI.
- **Bounded:** only the two approved synthetic scenarios are accepted.
- **Shared:** agent actions update the same page the human sees.
- **Human-controlled:** drafts require human review and send authority.

---

## What we learned

Building the challenge slice changed how we think about agent-native web
applications.

- **The page can be the shared contract.** The strongest pattern was not a
  separate agent UI; it was letting the human-facing page expose a narrow,
  discoverable tool surface.
- **ACTION / STATE / ARTIFACT is a useful composition.** One tool performs the
  bounded operation, while read-only tools let the agent inspect the exact
  current state and prepared output without rerunning the workflow.
- **Safe refusal is part of the UX.** `AMBIGUOUS_CONTACT` intentionally stops
  with `NEEDS_REVIEW` instead of guessing at identity.
- **Browser behavior is part of reliability.** Native client capability,
  exact-origin CORS, HTTPS canonicalization, and cache behavior all mattered
  to whether the tools worked correctly in a real agent-capable browser.
- **More context is not automatically better.** For MG Guide, external
  information only becomes useful when source provenance, user intent, and
  governance travel with it.

---

## Where we would take it next

The current challenge build proves MG Guide can expose its own governed
workflow to browser agents. The next opportunity is the reverse direction:
letting a person intentionally bring useful information from the open web into
the governed MG environment without turning the browser into an unbounded data
collection channel.

We would introduce a **source-aware governed intake packet** carrying the
source URL/title, capture time, user intent, selected content or structured
tool result, provenance/integrity metadata, sensitivity classification, and
the bounded MG workflow the information is allowed to inform. The intake layer
would validate and stage that evidence before MG Guide could retrieve it;
ingestion would not automatically authorize an external effect or permanent
memory promotion.

A **Google Chrome extension companion** is one practical way to provide that
bridge for sites that do not yet expose WebMCP. The user would explicitly
select relevant browser context and its intended MG Guide use, and the
extension would package it for the same governed intake boundary. On a site
that does expose WebMCP, we would prefer the site's declared structured tools
over DOM inference or scraping.

```text
WebMCP-capable external site
    → native structured tool result
    → governed intake packet

Non-WebMCP external site
    → explicit user-selected context in Chrome extension
    → governed intake packet

Both
    → validation / provenance / staging
    → MG Guide governed retrieval
    → human-reviewed downstream action
```

This is roadmap direction, not a claim about the current challenge runtime.
The submitted build does **not** perform arbitrary external-web ingestion and
there is no production Chrome extension in this submission.

Detailed lessons and future architecture:
[`LESSONS_AND_FUTURE_DIRECTION.md`](LESSONS_AND_FUTURE_DIRECTION.md).

---

## What is new for this challenge

MG Guide is an existing project. The WebMCP Challenge work was added during
the submission period and is documented separately from pre-existing work.

New challenge work includes:

- the browser-native WebMCP frontend in `webmcp/static/`;
- the bounded stateless adapter in `src/mg_guide/webmcp/`;
- exactly three registered WebMCP tools;
- browser-held current state for read-only state/draft tools;
- WebMCP-specific tests under `tests/webmcp/`;
- dedicated competition deployment packaging;
- live host integration on the existing MG Guide/A.I. Rolodex web surface;
- native browser acceptance and competition-specific presentation work.

For the concise dated history, see
[`CHALLENGE_PERIOD_EVIDENCE.md`](CHALLENGE_PERIOD_EVIDENCE.md). For the full
architectural boundary between pre-existing MG Guide and new WebMCP work, see
[`COMPETITION_DELTA.md`](COMPETITION_DELTA.md).

---

## Safety and demo boundaries

The WebMCP demo uses synthetic fixture data only.

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

The agent can prepare and inspect. It cannot send an email, mutate CRM, call
HighLevel, supply credentials, switch to a live mode, or provide arbitrary
transcript/contact identifiers through the competition tool surface.

When identity is ambiguous, the workflow fails closed instead of guessing.

---

## Where to inspect the implementation

| Surface | Path |
| --- | --- |
| Tool registration and browser state | [`webmcp/static/app.js`](../../webmcp/static/app.js) |
| Human-facing page | [`webmcp/static/index.html`](../../webmcp/static/index.html) |
| Bounded WebMCP backend | [`src/mg_guide/webmcp/`](../../src/mg_guide/webmcp/) |
| WebMCP tests | [`tests/webmcp/`](../../tests/webmcp/) |
| Architecture | [`WEBMCP_ARCHITECTURE.md`](WEBMCP_ARCHITECTURE.md) |
| Challenge-period evidence | [`CHALLENGE_PERIOD_EVIDENCE.md`](CHALLENGE_PERIOD_EVIDENCE.md) |
| Competition delta | [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) |
| Lessons + future direction | [`LESSONS_AND_FUTURE_DIRECTION.md`](LESSONS_AND_FUTURE_DIRECTION.md) |
| Judge testing | [`JUDGE_TESTING.md`](JUDGE_TESTING.md) |
| Demo script | [`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md) |
| Submission draft | [`DEVPOST_SUBMISSION_DRAFT.md`](DEVPOST_SUBMISSION_DRAFT.md) |

---

## Judging-criteria map

| Criterion | What to look for |
| --- | --- |
| **WebMCP Leverage** | Real `document.modelContext.registerTool` registration; exactly three schema-bounded tools; native discovery and invocation; shared browser-held state |
| **Execution** | One coherent live product page with SUCCESS, read-state/read-draft, and fail-closed AMBIGUOUS behavior |
| **Potential Impact** | Reduces repetitive post-meeting preparation while preserving salesperson judgment and customer-facing control; creates a path toward governed external evidence intake |
| **Creativity & Ambition** | Turns a relationship-intelligence workspace into a standards-based human+agent surface today, with a WebMCP-first / Chrome-extension compatibility path for future governed browser context |

---

## Demo outcome in one sentence

**MG Guide turns post-meeting follow-up into a safe agent-human workflow:
action, state, artifact, then human control.**
