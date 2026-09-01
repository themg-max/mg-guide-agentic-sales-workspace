# MG Guide | Agentic Sales Workspace — WebMCP Challenge Brief

```text
COMPETITION=The WebMCP Challenge
OWNER=VS Code / MG Orchestrator
PUBLIC_REPO=themg-max/mg-guide-agentic-sales-workspace
STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
```

## What this is

MG Guide already turns a meeting transcript into structured relationship
context and a governed follow-up plan (`meeting_follow_up_v1`). For The
WebMCP Challenge we added a new, bounded, browser-native agent interface so
the same experience can expose structured capabilities directly to a user's
browser agent — without weakening the existing authenticated judge/add-on
surface, and without any new live CRM effect.

See [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) for the exact pre-existing
vs. newly-added-for-WebMCP boundary with commit SHAs.

## The story for judges

1. A human opens the MG Guide WebMCP page and sees a synthetic meeting.
2. A browser agent discovers three structured WebMCP tools on the page.
3. The agent invokes `process_meeting_follow_up({scenario: "SUCCESS"})`.
4. The same page visibly updates: Meeting Context, Relationship Context, and
   Follow-Up Planning move from empty to populated, and Follow-Up Draft
   becomes `READY`.
5. The agent inspects state (`get_current_follow_up_state`) and reads the
   deterministic draft (`get_follow_up_draft`) — a human must still review
   and send it.
6. The agent then invokes `process_meeting_follow_up({scenario:
   "AMBIGUOUS_CONTACT"})`. The page moves to `NEEDS_REVIEW`, and
   `get_follow_up_draft` now returns `NOT_AVAILABLE` /
   `RELATIONSHIP_REVIEW_REQUIRED`. No draft, no CRM effect, no email —
   identity ambiguity fails closed.

People retain judgment. Agents gain structured, schema-bounded access to a
real product capability instead of scraping the DOM or guessing at hidden
form fields.

## Boundary (what this demo will never do)

- No live HighLevel/CRM calls, no CRM mutations, no email sends.
- No arbitrary transcript, raw CRM identifier, live-mode selector, or
  credential ever accepted by the public API or tool schemas.
- Ambiguous relationship identity always fails closed.
- The existing authenticated `/demo/meeting-follow-up` judge/add-on route is
  untouched and remains authenticated.

## Judging-dimension evidence map

| Dimension | Evidence |
| --- | --- |
| WebMCP leverage | Real `document.modelContext.registerTool` tools, narrow JSON Schemas, actual agent invocation updating visible page state, fail-closed tool behavior |
| Execution | Live URL, complete page (7 sections), both SUCCESS and AMBIGUOUS_CONTACT flows working, browser acceptance evidence |
| Potential impact | Solves the real meeting-to-follow-up administrative gap; a browser agent removes manual navigation while the human keeps sign-off |
| Creativity & ambition | The same relationship-intelligence workspace serves both a human and a browser agent through structured, standards-based capabilities rather than UI scraping |

See [`WEBMCP_ARCHITECTURE.md`](WEBMCP_ARCHITECTURE.md) for the technical
design, [`JUDGE_TESTING.md`](JUDGE_TESTING.md) for testing instructions, and
[`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) for the packaging
checklist.
