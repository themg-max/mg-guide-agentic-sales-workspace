# MG Guide | Agent-Native Follow-Up — WebMCP Judge Start

**Live demo:** https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/

**Public source:** https://github.com/themg-max/mg-guide-agentic-sales-workspace

**WebMCP implementation:** [`webmcp/static/app.js`](../../webmcp/static/app.js)

**Trust boundary:** **Agent can prepare. Only a person can review and send.**

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
| Judge testing | [`JUDGE_TESTING.md`](JUDGE_TESTING.md) |
| Demo script | [`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md) |
| Submission draft | [`DEVPOST_SUBMISSION_DRAFT.md`](DEVPOST_SUBMISSION_DRAFT.md) |

---

## Judging-criteria map

| Criterion | What to look for |
| --- | --- |
| **WebMCP Leverage** | Real `document.modelContext.registerTool` registration; exactly three schema-bounded tools; native discovery and invocation; shared browser-held state |
| **Execution** | One coherent live product page with SUCCESS, read-state/read-draft, and fail-closed AMBIGUOUS behavior |
| **Potential Impact** | Reduces repetitive post-meeting preparation while preserving salesperson judgment and customer-facing control |
| **Creativity & Ambition** | Turns a relationship-intelligence workspace into a standards-based human+agent surface instead of building an agent-only UI or brittle automation layer |

---

## Demo outcome in one sentence

**MG Guide turns post-meeting follow-up into a safe agent-human workflow:
action, state, artifact, then human control.**
