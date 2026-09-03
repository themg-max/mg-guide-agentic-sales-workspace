# Devpost Submission Draft — The WebMCP Challenge

```text
PROJECT_NAME=MG Guide | Agent-Native Follow-Up
APP_STATUS=Existing
STATUS=DRAFT_ONLY
FINAL_SUBMISSION_EXECUTED=NO
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
PUBLIC_REPOSITORY=https://github.com/themg-max/mg-guide-agentic-sales-workspace
```

This draft is organized around the current WebMCP Challenge submission form
and the four equally weighted judging criteria. Do not submit claims marked as
pending until final runtime acceptance/freeze confirms them.

---

## Tagline

**A WebMCP-native meeting follow-up workspace where agents prepare action,
state, and draft artifacts while people keep final send authority.**

---

## Project description

### What we built

MG Guide helps a salesperson turn a meeting into relationship-aware follow-up:
understand what happened, connect the conversation to the right relationship,
decide the next step, and prepare a useful draft.

For The WebMCP Challenge, we extended the existing MG Guide product with a
browser-native WebMCP interface. The live page now exposes exactly three
structured tools directly to a browser agent:

1. `process_meeting_follow_up` — **ACTION** — runs one bounded synthetic
   follow-up scenario.
2. `get_current_follow_up_state` — **STATE** — reads the current browser-held
   workflow state without rerunning it.
3. `get_follow_up_draft` — **ARTIFACT** — reads the deterministic follow-up
   draft already prepared on the page.

The result is one shared human-and-agent workspace rather than a human UI plus
a separate agent-only integration.

### Why this is a strong fit for WebMCP

Without WebMCP, an agent would need either a bespoke integration or brittle
DOM/navigation inference to use a web workflow. MG Guide instead declares a
small, typed tool contract through `document.modelContext.registerTool(...)`.
The agent sees named capabilities with narrow schemas, while the person sees
the same state change on the same page.

WebMCP matters here because post-meeting follow-up is naturally collaborative:
the agent can remove repetitive preparation, but a person should retain
relationship judgment and customer-facing authority.

### How it creates a better user experience

A person no longer has to choose between manually navigating every follow-up
step and handing the whole process to opaque automation. The browser agent can
invoke the structured workflow and inspect its result directly.

On `SUCCESS`:

```text
ACTION
→ relationship matched
→ workflow COMPLETED
→ draft READY

STATE
→ agent reads the same current follow-up state shown on the page

ARTIFACT
→ agent reads the prepared follow-up draft
→ requires_human_send=true
```

The agent prepares the work; the person retains final review and send control.

### What people and agents can now do together

The human and agent operate on the same visible browser-held state. The agent
can process the meeting-follow-up scenario, inspect the resulting relationship
and next-step state, and retrieve the draft for review. The human keeps final
judgment and customer-facing action.

The collaboration is also deliberately fail-closed. On
`AMBIGUOUS_CONTACT`, MG Guide returns:

```text
NEEDS_REVIEW
relationship=ambiguous
draft=NOT_AVAILABLE
reason=RELATIONSHIP_REVIEW_REQUIRED
```

The system does not invent a contact match or prepare a customer-facing draft
when identity is uncertain.

### How we implemented WebMCP

- **Browser tool layer:** `webmcp/static/app.js` registers exactly three tools
  using `document.modelContext.registerTool(...)` and feature-detects native
  WebMCP rather than polyfilling it.
- **Shared browser state:** `currentWebMCPState` holds the current safe result;
  the STATE and ARTIFACT tools are client-only readers of what the human sees.
- **Bounded backend:** `src/mg_guide/webmcp/` provides a stateless synthetic API
  that reuses the existing MG Guide `meeting_follow_up_v1` workflow.
- **Input boundary:** only `SUCCESS` and `AMBIGUOUS_CONTACT` scenarios are
  accepted. Authority-bearing fields such as live mode, CRM writes, email
  sends, credentials, arbitrary transcripts, and customer identifiers are
  rejected.
- **Deployment:** the WebMCP page is hosted on the existing MG Guide/A.I.
  Rolodex web surface and calls a separate bounded Cloud Run backend.
- **Tests and proof:** `tests/webmcp/`, `competition/webmcp/`, and
  `proof/webmcp/` contain the implementation checks, competition delta, judge
  path, and public acceptance evidence.

### Human-control and data boundary

The challenge demo uses fixed synthetic data only.

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

Every usable draft is marked `requires_human_send=true`.

**Agent can prepare. Only a person can review and send.**

### Existing project vs. new challenge-period work

MG Guide existed before the WebMCP Challenge. Pre-existing work includes the
core `meeting_follow_up_v1` workflow, specialized Meeting Context / Relationship
Context / Follow-Up Planning agents, deterministic policy, Google Workspace
integration, and broader MG Guide cloud architecture.

The WebMCP Challenge delta was added during the submission period and includes:

- the browser-native WebMCP frontend;
- the bounded stateless WebMCP adapter;
- exactly-three-tool registration and schemas;
- browser-held shared state for read-only tools;
- WebMCP-specific tests;
- dedicated competition deployment packaging;
- host integration and native browser acceptance;
- challenge-specific presentation and judge/submission documentation.

The dated commit/PR history and exact boundary are documented in
[`COMPETITION_DELTA.md`](COMPETITION_DELTA.md).

---

## Live URL

```text
https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

Before submission, run final clean-browser acceptance against this exact URL
and freeze the accepted runtime.

---

## Public repository

```text
https://github.com/themg-max/mg-guide-agentic-sales-workspace
```

License: Apache-2.0.

Judge start:
[`competition/webmcp/README.md`](README.md)

---

## Testing instructions — suggested Devpost field copy

No login is required. Open the live URL in ChatGPT's in-app browser or Google
Chrome 149+ with `chrome://flags/#enable-webmcp-testing` enabled and the
browser restarted.

Ask the browser agent:

> Use the WebMCP tools exposed by this page. First process the SUCCESS meeting,
> then read the current follow-up state and the follow-up draft.

Expected: workflow `COMPLETED`, relationship `matched`, draft `READY`, and
`requires_human_send=true`.

Then ask:

> Now process AMBIGUOUS_CONTACT and tell me whether a follow-up draft is
> available.

Expected: `NEEDS_REVIEW`, relationship `ambiguous`, draft `NOT_AVAILABLE`, and
`RELATIONSHIP_REVIEW_REQUIRED`.

The demo is synthetic-only: no CRM mutation or email send occurs.

Full testing guide:
`competition/webmcp/JUDGE_TESTING.md`.

---

## Required form answers — source-backed vs. human-supplied

| Devpost field | Draft answer / action |
| --- | --- |
| Submitter Type | **HUMAN INPUT REQUIRED** — Individual / Team of Individuals / Organization |
| Country of residence | **HUMAN INPUT REQUIRED** |
| Organization name | **HUMAN INPUT REQUIRED if submitting as an organization** |
| App Status | `Existing` |
| Existing-project update | Use the challenge-period delta paragraph below |
| Live URL | `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/` |
| Testing instructions | Use the testing copy above |
| Public code repo | `https://github.com/themg-max/mg-guide-agentic-sales-workspace` |
| Agents/clients tested | Use only clients actually validated before submission; current public evidence supports native Google Chrome WebMCP testing. Add ChatGPT in-app browser only after final direct validation. |
| AI tools leveraged | VS Code / GitHub Copilot were used in implementation and validation; add any other tools only if actually used for this project |
| Learning level | **HUMAN INPUT REQUIRED** — None / Moderate / Significant |
| AI career value | **HUMAN INPUT REQUIRED** — Yes / No |

### Existing-project update — suggested field copy

> MG Guide existed before August 25. During the WebMCP submission period we
> meaningfully extended it with a new browser-native WebMCP layer: a bounded
> stateless backend adapter, exactly three `document.modelContext.registerTool`
> tools, shared browser-held state, WebMCP-specific tests, live host
> integration, native browser invocation, fail-closed ambiguous-identity
> behavior, and challenge-specific presentation/judge documentation. The
> public repository's `competition/webmcp/COMPETITION_DELTA.md` and dated
> commit history distinguish this work from the pre-existing MG Guide
> workflow and agents.

### Agents/clients tested — conservative current answer

> Google Chrome 149+ with native WebMCP testing enabled was used to verify
> native tool discovery and invocation on the live product. Exactly three
> tools were discovered and the SUCCESS and AMBIGUOUS_CONTACT paths were
> exercised. Add ChatGPT's in-app browser here only after it is directly
> validated in the final acceptance pass.

### AI tools used — current source-backed answer

> VS Code with GitHub Copilot/Copilot-assisted development was used for
> implementation, debugging, test iteration, and documentation. ChatGPT was
> used for architecture review, competition analysis, governance-bound
> planning, and submission packaging.

---

## Rubric evidence map

| Judging criterion | Submission evidence |
| --- | --- |
| **WebMCP Leverage** | Real native registration, exactly three typed tools, ACTION/STATE/ARTIFACT pattern, native discovery/invocation, shared browser state |
| **Execution** | Working live page, coherent SUCCESS path, read tools, fail-closed AMBIGUOUS path, human-visible state |
| **Potential Impact** | Concrete post-meeting follow-up burden for relationship-driven sales work; agent removes preparation/navigation while person keeps judgment |
| **Creativity & Ambition** | Standards-based human+agent relationship workspace on the same page instead of a separate agent UI or DOM automation layer |

---

## Video requirement

Final video must:

- be public on YouTube;
- be under three minutes;
- include clear audio;
- show the project functioning;
- show actual WebMCP use, with all three tools visible or exercised;
- avoid private terminals, credentials, customer data, copyrighted music, or
  unsupported production claims.

Use [`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md).

---

## Final submission gate

Do not submit until all are true:

```text
FINAL_LIVE_RUNTIME_ACCEPTANCE=PASS
FINAL_RUNTIME_FREEZE=BOUND
PUBLIC_REPO_JUDGE_DOCS=MERGED
PUBLIC_REPO_INCOGNITO_CHECK=PASS
LICENSE_VISIBLE=PASS
VIDEO_PUBLIC_YOUTUBE=YES
VIDEO_RUNTIME_LT_3_MIN=YES
VIDEO_AUDIO=PASS
DEVPOST_REQUIRED_FIELDS=COMPLETE
SUBMISSION_STATUS=SUBMITTED
```

After the submission deadline, do not modify the submitted repo, live site,
video, or submission during judging except as expressly permitted by the
competition administrators.
