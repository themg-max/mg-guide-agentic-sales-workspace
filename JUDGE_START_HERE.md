# Start Here — Judges

```text
SURFACE=JUDGE_START_HERE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
COMPETITION=The WebMCP Challenge (CURRENT)
```

## MG Guide | Agent-Native Follow-Up

**Live demo:** https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/

**Trust boundary:** **Agent can prepare. Only a person can review and send.**

**The WebMCP Challenge is the current judge path.** This page is the front
door for it.

## What this is

MG Guide turns a meeting transcript into structured relationship context and
a governed follow-up plan. For the WebMCP Challenge, the same human-facing
page exposes a small, typed tool surface directly to a browser agent via
`document.modelContext.registerTool`.

Exactly **3 tools** are registered — no more, no fewer:

1. `process_meeting_follow_up` — **ACTION** — run one approved synthetic
   meeting-follow-up scenario.
2. `get_current_follow_up_state` — **STATE** — read the current browser-held
   workflow state without rerunning the workflow.
3. `get_follow_up_draft` — **ARTIFACT** — read the follow-up draft already
   prepared on the page.

```text
ACTION → STATE → ARTIFACT → HUMAN CONTROL
```

## Expected results

**SUCCESS:**

```text
SUCCESS
→ relationship matched
→ workflow COMPLETED
→ follow-up draft READY
→ requires_human_send=true
```

**AMBIGUOUS_CONTACT (safe-stop):**

```text
AMBIGUOUS_CONTACT
→ relationship ambiguous
→ NEEDS_REVIEW
→ draft NOT_AVAILABLE
→ RELATIONSHIP_REVIEW_REQUIRED
→ no external effect
```

`requires_human_send=true` on every usable draft. Zero external effects
(no CRM mutation, no email send, no live-mode) in the challenge path.

## Judge path

1. [`competition/webmcp/README.md`](competition/webmcp/README.md) — full
   judge start and judging-criteria map
2. [`competition/webmcp/JUDGE_TESTING.md`](competition/webmcp/JUDGE_TESTING.md) — step-by-step testing
3. [`competition/webmcp/WEBMCP_ARCHITECTURE.md`](competition/webmcp/WEBMCP_ARCHITECTURE.md) — architecture
4. [`competition/webmcp/COMPETITION_DELTA.md`](competition/webmcp/COMPETITION_DELTA.md) — pre-existing foundation vs. new WebMCP work
5. [`competition/webmcp/CHALLENGE_PERIOD_EVIDENCE.md`](competition/webmcp/CHALLENGE_PERIOD_EVIDENCE.md) — dated challenge-period evidence

## Historical

**Google All Things Agentic Hackathon judge guide (historical):**
[`competition/google-all-things-agentic/JUDGE_GUIDE.md`](competition/google-all-things-agentic/JUDGE_GUIDE.md)
