# Start Here — Judges

> **Historical Google All Things Agentic judge guide.** This page documents
> the Google All Things Agentic Hackathon submission. If you are judging
> **The WebMCP Challenge**, start at
> [`competition/webmcp/README.md`](competition/webmcp/README.md) instead.

This page is the shortest path through the MG Guide competition repository.

```text
SURFACE=JUDGE_START_HERE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
COMPETITION=Google All Things Agentic Hackathon
```

## What MG Guide is

MG Guide turns a meeting transcript into structured relationship context and a
governed follow-up plan so salespeople can move from conversation to action
without rebuilding context manually.

It is a bounded agentic sales workspace: specialized agents understand the
meeting and propose the next step, deterministic policy decides what is allowed,
and external CRM effects remain separately governed.

This competition slice uses synthetic / test data. It does not claim production
CRM automation or same-run transcript-to-live-CRM writes.

## The problem

Before COVID, much financial-services relationship work happened face to face.
Today many of those conversations happen online.

The meeting is digital, but the work after the meeting is still fragmented:
reviewing what was said, remembering personal and business context, finding the
correct CRM relationship, documenting the conversation, determining the next
step, and preparing future follow-up.

MG Guide is designed to close that post-meeting gap.

## What we built

```text
Meeting transcript
  -> Meeting Context
  -> Relationship Context
  -> Follow-Up Planning
  -> deterministic policy
  -> salesperson follow-up state
```

In the success path, the salesperson sees a completed follow-up plan. When
contact identity is ambiguous, the workflow fail-closes into needs-review and
does not attempt unauthorized CRM effects.

## Where it runs

**Google Cloud Agent Runtime** hosts one orchestrator deployment:

- Display name: `mg-guide-orchestrator`
- Framework: Google ADK
- Root agent: `SequentialAgent`

The three specialized agents run as an internal sequence of that one hosted
orchestrator:

1. `meeting_context_agent`
2. `relationship_context_agent`
3. `follow_up_planning_agent`

Supporting surfaces:

- Gemini 3.5 Flash
- Cloud Run (competition judge / Workspace adapter)
- Firestore (audit proof)
- Google Workspace add-on (thin presentation and routing)
- HighLevel REST v3 bounded adapter (current CRM boundary)

Cloud Run is not the hosted three-agent runtime. Agent Runtime hosts the
three-agent graph.

## Judge account

Email: `mg_guide.judge@themiliare-group.com`

This is a controlled competition Google Workspace account. Credentials are
provided privately through the competition testing instructions and are
intentionally not stored in this public repository.

See [docs/judges/JUDGE_ACCESS.md](docs/judges/JUDGE_ACCESS.md).

## What to try

Use only the provided competition Workspace account.

1. Sign into `mg_guide.judge@themiliare-group.com`.
2. Open Gmail or Calendar in Google Workspace.
3. Launch **MG Guide**.
4. Run **Meeting Follow-Up**.
5. Try the two required demonstrations:

| Demo | What you should see |
| --- | --- |
| **SUCCESS** | Completed follow-up state |
| **AMBIGUOUS_CONTACT** | Needs-review / fail-closed state |

The add-on is a thin presentation and routing adapter. It does not own policy,
CRM mutation, agent reasoning, or workflow truth. Demonstration data is
synthetic / test data.

## What to look for

- Transcript understanding from Meeting Context
- Relationship context attached to the meeting
- Recommended follow-up from Follow-Up Planning
- Fail-closed behavior when identity is ambiguous
- Google Cloud hosted proof for the three-agent orchestrator

## Evidence

Five starting links:

1. [Judge documentation index](docs/judges/README.md)
2. [Competition architecture](docs/architecture/meeting-follow-up-v1-competition-architecture.md)
3. [Hosted Agent Runtime acceptance](proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md)
4. [HighLevel REST v3 exact synthetic contact read](proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md)
5. [Proof index](docs/judges/PROOF_INDEX.md)

Deeper engineering history lives under [`proof/`](proof/README.md) and
[`competition/NEW_WORK_LEDGER.md`](competition/NEW_WORK_LEDGER.md). Judges do
not need that tree first.
