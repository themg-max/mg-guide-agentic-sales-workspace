# MG Guide | Agent-Native Follow-Up — WebMCP Submission Control Packet

```text
PROJECT_NAME=MG Guide | Agent-Native Follow-Up
COMPETITION=The WebMCP Challenge
STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
PACKAGING_BASE_SHA=8a9df7178e20fe8f3faf642ddf09858f6716e5da
FINAL_PUBLIC_FREEZE_SHA=PENDING
FINAL_RUNTIME_FREEZE=PENDING
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
LICENSE=Apache-2.0
```

This is the submission control document. It keeps the competition narrative,
truth boundaries, final readiness gates, and human-controlled submission work
in one place. Historical proof files keep the source SHAs that were true when
they were recorded; this packet instead tracks the final packaging/freeze
state.

---

## 1. Submission thesis

**MG Guide turns post-meeting follow-up into a safe agent-human workflow:
action, state, artifact, then human control.**

MG Guide existed before the WebMCP Challenge. The challenge-period extension
adds a standards-based browser-agent interface to the same human-facing
relationship-follow-up experience.

Exactly three tools are exposed:

```text
ACTION   process_meeting_follow_up
STATE    get_current_follow_up_state
ARTIFACT get_follow_up_draft
```

The agent can prepare and inspect. A person retains final customer-facing
judgment and send authority.

---

## 2. Problem

Meetings are increasingly digital, but the work after a conversation is still
fragmented: reconstruct what happened, connect it to relationship context,
decide the right next step, and prepare a useful follow-up.

That work is repetitive enough for an agent to help with, but relationship
identity and customer-facing action still require human judgment.

---

## 3. Why WebMCP

Without WebMCP, browser-agent access would require either:

- a separate agent-only API/interface; or
- brittle inference from DOM structure, page labels, and navigation.

WebMCP lets MG Guide publish a small, typed, discoverable tool contract on the
same page the person already uses. This keeps the agent bounded and gives the
human a visible shared state instead of creating a parallel automation surface.

---

## 4. Expected judge demo

### SUCCESS

```text
process_meeting_follow_up(SUCCESS)
→ COMPLETED
→ relationship matched
→ draft READY
→ requires_human_send=true
```

Then:

```text
get_current_follow_up_state
get_follow_up_draft
```

Both read the current browser-held state/artifact without rerunning the
workflow.

### AMBIGUOUS_CONTACT

```text
process_meeting_follow_up(AMBIGUOUS_CONTACT)
→ NEEDS_REVIEW
→ relationship ambiguous
→ draft NOT_AVAILABLE
→ RELATIONSHIP_REVIEW_REQUIRED
```

When identity is uncertain, the system stops instead of guessing.

---

## 5. Safety boundary

The WebMCP competition path uses fixed synthetic data only.

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

The tool surface rejects authority-bearing/unbounded inputs such as live mode,
CRM-write requests, send-email requests, credentials, arbitrary transcripts,
and raw CRM identifiers.

**Agent can prepare. Only a person can review and send.**

---

## 6. Existing project / challenge-period delta

### Pre-existing MG Guide

- `meeting_follow_up_v1` workflow;
- Meeting Context, Relationship Context, and Follow-Up Planning agents;
- deterministic policy;
- existing Google Workspace and broader cloud architecture;
- existing A.I. Rolodex/MG Guide product surface.

### New for The WebMCP Challenge

- `src/mg_guide/webmcp/` bounded stateless adapter;
- `webmcp/static/` browser-native WebMCP frontend;
- exactly three `document.modelContext.registerTool(...)` registrations;
- browser-held `currentWebMCPState` for read-only state/draft tools;
- `tests/webmcp/` competition tests;
- challenge deployment packaging;
- production host integration and native browser acceptance;
- follow-up draft-quality work for the demo;
- ACTION / STATE / ARTIFACT capability presentation;
- fail-closed multi-run/presentation regression fixes;
- native functional acceptance proof;
- final MG Guide frontend presentation elevation;
- competition judge/submission documentation.

The dated evidence is maintained in
[`COMPETITION_DELTA.md`](COMPETITION_DELTA.md).

---

## 7. Judge-facing source map

| Need | Artifact |
| --- | --- |
| Start here | [`README.md`](README.md) |
| Detailed testing | [`JUDGE_TESTING.md`](JUDGE_TESTING.md) |
| Architecture | [`WEBMCP_ARCHITECTURE.md`](WEBMCP_ARCHITECTURE.md) |
| New vs. existing work | [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) |
| Demo script | [`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md) |
| Devpost copy | [`DEVPOST_SUBMISSION_DRAFT.md`](DEVPOST_SUBMISSION_DRAFT.md) |
| Final checklist | [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) |
| Historical native production evidence | [`../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md) |

Public implementation:

```text
webmcp/static/app.js
src/mg_guide/webmcp/
tests/webmcp/
```

---

## 8. Judging-criteria strategy

### WebMCP Leverage

Show real native tools, all three roles, typed/bounded inputs, native agent
invocation, and shared browser state. Do not make the demo just a human button
click.

### Execution

Show one coherent live product: successful processing, state/draft inspection,
and a meaningful fail-closed path. Avoid internal engineering detail in the
video.

### Potential Impact

Keep the problem concrete: post-meeting relationship follow-up for a
relationship-driven salesperson. The value is reduced preparation/navigation,
not autonomous customer communication.

### Creativity & Ambition

Emphasize the standards-based shared human-agent workspace: one page, one
visible state, structured tools, explicit human authority — not a separate
agent console or screen-scraping automation.

---

## 9. Final runtime gate — still required

Historical production acceptance is preserved in public proof, but the final
judge-facing frontend runtime is undergoing a bounded render-delivery repair in
the private host-integration lane. Do not represent final submission runtime
freeze as complete until that repaired candidate is accepted and promoted.

Before recording/submitting require:

```text
FINAL_LIVE_RUNTIME_ACCEPTANCE=PASS
FRESH_BROWSER_RENDER=PASS
STALE_CACHE_BROWSER_RENDER=PASS
NARROW_BROWSER_RENDER=PASS
NATIVE_WEBMCP_TOOL_COUNT=3
SUCCESS_FINAL_SMOKE=PASS
AMBIGUOUS_FINAL_SMOKE=PASS
REQUIRES_HUMAN_SEND=TRUE
APPLICATION_EXTERNAL_EFFECTS=0
FINAL_RUNTIME_FREEZE=BOUND
```

Once these pass, record the immutable frontend revision/image fingerprint in
the private proof and freeze product/runtime changes.

---

## 10. Public-repo packaging gate

Current packaging branch adds/reconciles judge-facing documentation only. It
must pass the repo-local exact-head check and normal PR review before merge.

Before final submission:

```text
PUBLIC_PACKAGING_PR=MERGED
FINAL_PUBLIC_FREEZE_SHA=RECORDED
PUBLIC_REPO_INCOGNITO_CHECK=PASS
LICENSE_VISIBLE_IN_GITHUB_ABOUT=PASS
REPO_ABOUT_DESCRIPTION_ALIGNED=YES
REPO_HOMEPAGE_LIVE_URL=YES
```

Do not edit the public repo after the competition deadline.

---

## 11. Submission operations

Human-controlled remaining work:

1. complete final live runtime acceptance and freeze;
2. merge the judge-facing public documentation package;
3. update GitHub About metadata and verify the repo logged out;
4. update the Devpost project description/tagline from the approved draft;
5. collect the human-supplied submission fields;
6. record the under-three-minute demo using the frozen runtime;
7. upload it publicly to YouTube and verify the link logged out;
8. complete all Devpost required fields;
9. submit before 1:00 PM PT / 4:00 PM ET;
10. confirm Devpost marks the project **Submitted**, not Draft;
11. freeze the submitted repo/live site/video through judging.

Final submission itself remains a deliberate human-controlled action unless
the human explicitly instructs the connected Devpost tool to submit after all
required answers are complete.
