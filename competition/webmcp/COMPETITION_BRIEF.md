# MG Guide | Agentic Sales Workspace — WebMCP Challenge Brief

```text
COMPETITION=The WebMCP Challenge
OWNER=VS Code / MG Orchestrator
PUBLIC_REPO=themg-max/mg-guide-agentic-sales-workspace
STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
SEPARATE_WEB_SURFACE_REQUIRED=NO
EXISTING_AI_ROLODEX_SURFACE_REUSED=YES
SEPARATE_WEBMCP_BACKEND_BOUNDARY=YES
```

## What this is

MG Guide already turns a meeting transcript into structured relationship
context and a governed follow-up plan (`meeting_follow_up_v1`). For The
WebMCP Challenge we added a new, bounded, browser-native agent interface so
the same experience can expose structured capabilities directly to a user's
browser agent — without weakening the existing authenticated judge/add-on
surface, and without any new live CRM effect.

The **product page** lives on the existing A.I. Rolodex website at
`/mg-guide/`. A separate bounded backend (`mg-guide-webmcp`) runs the
synthetic workflow. The public MG Guide repository remains the canonical
source of WebMCP code.

See [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) for the exact pre-existing
vs. newly-added-for-WebMCP boundary with commit SHAs.

## The story for judges

1. A human opens `…/mg-guide/` on the A.I. Rolodex site and sees a synthetic meeting.
2. A browser agent discovers three structured WebMCP tools on the page.
3. The agent invokes `process_meeting_follow_up({scenario: "SUCCESS"})`.
4. The same page visibly updates: Meeting Context, Relationship Context, and
   Follow-Up Planning populate; Follow-Up Draft becomes `READY`.
5. The agent inspects state (`get_current_follow_up_state`) and reads the
   deterministic draft (`get_follow_up_draft`) from **browser memory** — a
   human must still review and send it.
6. The agent then invokes `process_meeting_follow_up({scenario:
   "AMBIGUOUS_CONTACT"})`. The page moves to `NEEDS_REVIEW`, and
   `get_follow_up_draft` returns `NOT_AVAILABLE` /
   `RELATIONSHIP_REVIEW_REQUIRED`. No draft, no CRM effect, no email.

People retain judgment. Agents gain structured, schema-bounded access.

## Boundary

- No live HighLevel/CRM calls, no CRM mutations, no email sends.
- No arbitrary transcript, raw CRM identifier, live-mode selector, or credential.
- Ambiguous relationship identity always fails closed.
- Backend is **stateless**; browser holds `currentWebMCPState`.
- Existing authenticated `/demo/meeting-follow-up` remains authenticated and untouched.

## Judging-dimension evidence map

| Dimension | Evidence |
| --- | --- |
| WebMCP leverage | Real `document.modelContext.registerTool` tools, narrow JSON Schemas, page-visible agent actions, fail-closed tool behavior |
| Execution | Live product URL on existing A.I. Rolodex site, complete page (7 sections), SUCCESS + AMBIGUOUS flows |
| Potential impact | Meeting-to-follow-up administrative gap; agent removes navigation; human keeps sign-off |
| Creativity & ambition | Same relationship-intelligence workspace for human + browser agent via standards-based tools, hosted on the existing brand surface |

See [`WEBMCP_ARCHITECTURE.md`](WEBMCP_ARCHITECTURE.md),
[`JUDGE_TESTING.md`](JUDGE_TESTING.md),
[`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md).
