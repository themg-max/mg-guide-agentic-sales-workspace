# Devpost write-up — MG Guide | Agentic Sales Workspace

Copy/adapt into the Devpost submission form. Keep claims aligned with current
durable proof, especially:

- `proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`
- `proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md`
- `proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md`

This file does not alter the live Devpost submission automatically.

---

## Project name

**MG Guide | Agentic Sales Workspace**

## Tagline

MG Guide turns a meeting into structured relationship context and a governed
follow-up plan — agents propose, policy decides.

## Competition / track

- **Hackathon:** Google All Things Agentic
- **Track:** Fortified Enterprise Fleet
- **Hero workflow:** `meeting_follow_up_v1`

## Elevator pitch (≤ 500 chars)

After a sales meeting, reps still rebuild context by hand: what was said, who
it belongs to, and what to do next. MG Guide runs a bounded vertical slice
where Gemini extracts meeting context, Google ADK sequences three specialized
agents on Google Cloud Agent Runtime, and deterministic policy either permits
the follow-up path or fail-closes on ambiguous identity.

## The problem

Before COVID, much financial-services relationship work happened face to face.
Today many conversations happen online. The meeting is digital, but the work
after the meeting is still fragmented: reviewing what was said, remembering
personal and business context, finding the correct CRM relationship,
documenting the conversation, and determining the next step.

Fully autonomous CRM writes without governance are unacceptable in enterprise
fleets. Teams need agentic speed with deterministic control.

## What we built

A bounded vertical slice, not a broad CRM rewrite:

1. **Meeting Context Agent** — understands what happened.
2. **Relationship Context Agent** — connects the meeting to relationship context.
3. **Follow-Up Planning Agent** — recommends the next steps.
4. **Deterministic policy gate** — sole authority for allow / block / needs-review.
5. **MG Guide experience** — salesperson-visible success and needs-review states.
6. **Google Cloud Agent Runtime** — hosted `mg-guide-orchestrator` SequentialAgent.
7. **Cloud Run** — competition judge / Workspace adapter surface.
8. **Firestore** — authorized `workflow_runs` audit persistence proof.
9. **HighLevel REST v3 bounded adapter** — current CRM boundary.

## How it works (SUCCESS)

Meeting transcript → Meeting Context → Relationship Context → Follow-Up
Planning → deterministic policy → completed MG Guide follow-up state.

## How it works (FAIL-CLOSED)

Ambiguous contact identity → agents may still propose → policy emits
`AMBIGUOUS_CONTACT` → writes not attempted → needs-review → **zero unauthorized
effects**.

## Google technologies used

| Layer | Declaration |
| --- | --- |
| Hosted runtime | **Google Cloud Agent Runtime** · `mg-guide-orchestrator` · Google ADK `SequentialAgent` |
| Model | **Gemini 3.5 Flash** via **Vertex AI** |
| Agent framework | **Google ADK** |
| Judge / adapter compute | **Cloud Run** competition judge / Workspace adapter surface |
| Data / audit | **Cloud Firestore** `workflow_runs` |
| Workspace | Google Workspace add-on (thin presentation and routing) |
| CRM boundary | HighLevel REST v3 bounded adapter |

Cloud Run is not the hosted three-agent runtime. Agent Runtime hosts the
three-agent graph.

## Architecture (short)

```text
Google Workspace meeting / transcript
  -> mg-guide-orchestrator on Google Cloud Agent Runtime
  -> Meeting Context Agent
  -> Relationship Context Agent
  -> Follow-Up Planning Agent
  -> deterministic policy
  -> MG Guide experience / Firestore audit / bounded REST v3 boundary
```

There is one hosted orchestrator containing the three-agent sequence.

Full diagram:
`docs/architecture/meeting-follow-up-v1-competition-architecture.md`

## Judge access

Judge Workspace account:

`airolodex.judge@themiliare-group.com`

Password: provided privately through Devpost testing credentials; never stored
in this repository.

1. Sign into the provided Google Workspace account.
2. Open Gmail or Calendar.
3. Launch MG Guide.
4. Run Meeting Follow-Up.
5. Review SUCCESS (completed) and AMBIGUOUS_CONTACT (needs-review).

Details: `JUDGE_START_HERE.md` and `docs/judges/JUDGE_ACCESS.md`.

## Demo

- Workspace add-on Meeting Follow-Up: `SUCCESS` / `AMBIGUOUS_CONTACT`
- Local judge: `POST /demo/meeting-follow-up` with the same selectors
- Script: `docs/demo/meeting-follow-up-v1-4min-demo-script.md`
- Demo truth boundary: `docs/demo/meeting-follow-up-demo-v1.md`

## Proof markers (competition)

```text
GEMINI_EXECUTION=PASS
ADK_EXECUTION=PASS
HOSTED_AGENT_RUNTIME=PASS
HOSTED_THREE_AGENT_SEQUENCE=PASS
CLOUD_RUN_JUDGE_SURFACE=PASS
FIRESTORE_AUDIT=PASS
SUCCESS_SCENARIO=PASS
FAIL_CLOSED_SCENARIO=PASS
UNAUTHORIZED_EXTERNAL_EFFECTS=0
JUDGE_DEMO_LIVE_GHL_MUTATION=NO

LIVE_REST_V3_EXACT_CONTACT_READ=PASS
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
```

Acceptance packet:
`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`

Hosted runtime packet:
`proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md`

Current REST v3 exact synthetic contact read:
`proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md`

Historical live synthetic CRM packet (Grant 008; supporting evidence only; not
the current transport centerpiece):
`proof/nw008/nw-008-at1-live-execution-result-008.md`

### Evidence lanes (do not collapse)

A synthetic meeting transcript was successfully ingested and extracted through
live Gemini into schema-valid meeting context. Separately, a hosted Google ADK
SequentialAgent on Google Cloud Agent Runtime executed the three-agent graph
with zero hosted GHL calls. Separately, one HighLevel REST v3 exact synthetic
contact GET succeeded (`NETWORK_CALL_COUNT=1`, `MUTATION_CALL_COUNT=0`).
Current REST note create/readback is pending. The current evidence does not
claim that Gemini-derived note content was written to HighLevel in the same
live execution. The judge demo remains deterministic and performs no live CRM
mutation.

Historical HighLevel MCP operation-metadata evidence remains supporting
history, not the current primary transport.

## Built with

- Python 3
- Google Cloud Agent Runtime
- Google ADK
- Gemini 3.5 Flash (Vertex AI)
- Cloud Run
- Cloud Firestore
- Google Workspace add-on
- Deterministic policy engine
- Synthetic fixtures only (competition safety)

## Challenges

- Separating **proposal** (agents) from **authorization** (policy) without
  diluting the demo.
- Hosting the three-agent graph on Google Cloud Agent Runtime while keeping the
  Cloud Run judge / Workspace adapter as a distinct surface.
- Proving Gemini 3.5+ while keeping CI deterministic via stub mode.
- Keeping CRM claims honest: exact live read proven, current note path pending.

## Accomplishments

- End-to-end SUCCESS and fail-closed paths with zero unauthorized effects
- Live Gemini 3.5 meeting-context extraction
- Hosted `mg-guide-orchestrator` SequentialAgent execution
- HighLevel REST v3 exact synthetic contact live read
- Cloud Run judge surface + Firestore audit smoke PASS
- Workspace add-on thin presentation adapter for the judge account
- Explicit honesty that transcript-to-live-GHL is **not** claimed as one run

## What's next

- Current REST note create/readback remains pending
- Same-run transcript-to-live-CRM write remains not claimed
- Optional additional human-authorized live synthetic CRM execution would
  require a new grant

## Team / repo

- Repository: `themg-max/mg-guide-agentic-sales-workspace`
- Judge start: `JUDGE_START_HERE.md`

## Cover / media checklist

- [ ] Architecture diagram export (from mermaid doc)
- [ ] SUCCESS card screenshot
- [ ] FAIL-CLOSED needs-review screenshot
- [ ] Agent Runtime / Cloud proof screenshot
- [ ] Demo video (~4 min)
