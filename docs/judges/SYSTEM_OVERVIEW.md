# System overview — judge-facing summary

```text
SURFACE=docs/judges/SYSTEM_OVERVIEW.md
STATUS=JUDGE_FACING_SUMMARY_ONLY
AUTHORITY=NON_AUTHORITATIVE_NAVIGATION
CANONICAL_ARCHITECTURE=docs/architecture/meeting-follow-up-v1-competition-architecture.md
```

This is a navigation overview for judges. It does not replace the competition
architecture document.

## Flow

```text
GOOGLE WORKSPACE
  meeting / transcript source
    ->
GOOGLE CLOUD AGENT RUNTIME
  mg-guide-orchestrator
  Google ADK SequentialAgent
    ->
  1. Meeting Context Agent
  2. Relationship Context Agent
  3. Follow-Up Planning Agent
    ->
DETERMINISTIC POLICY
    ->
MG GUIDE EXPERIENCE
FIRESTORE AUDIT
BOUNDED HIGHLEVEL REST v3 BOUNDARY
```

There is **one** deployed orchestrator runtime containing the three-agent
sequence. This is not three separate Agent Runtime deployments.

Cloud Run is the competition judge / Workspace adapter surface. It is not the
hosted three-agent runtime.

## Authority split

```text
Agents understand and propose.
Policy decides.
External effects remain separately governed.
```

| Layer | Owns | Does not own |
| --- | --- | --- |
| Meeting Context Agent | What happened in the meeting | CRM writes |
| Relationship Context Agent | Connecting the meeting to relationship context | Policy decisions |
| Follow-Up Planning Agent | Recommended next steps | Unilateral external effects |
| Deterministic policy | Allow / block / needs-review | Agent reasoning |
| Workspace add-on | Presentation and routing | Policy, CRM mutation, agent reasoning, workflow truth |
| HighLevel REST v3 adapter | Bounded CRM boundary | Open-ended CRM automation |

## Current CRM honesty

```text
LIVE_REST_V3_EXACT_CONTACT_READ=PASS
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
```

Historical HighLevel MCP evidence and historical Grant 008 live synthetic
note+stage proof remain supporting history. They are not the current transport
centerpiece.

## Not claimed here

This summary does not draw or claim:

- Agent Registry
- Memory Bank
- Agent Gateway
- Model Armor
- three separate Agent Runtime deployments
- current REST note-write completion
- production CRM automation
