# Devpost write-up — MG Guide | Agentic Sales Workspace

Copy/adapt into the Devpost submission form. Keep claims aligned with
`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`.

---

## Project name

**MG Guide | Agentic Sales Workspace**

## Tagline

Governed multi-agent sales follow-up: Gemini proposes, Google ADK orchestrates, OL3 decides.

## Competition / track

- **Hackathon:** Google All Things Agentic  
- **Track:** Fortified Enterprise Fleet  
- **Hero workflow:** `meeting_follow_up_v1`

## Elevator pitch (≤ 500 chars)

After a sales meeting, reps still retype notes, find the CRM contact, and guess
pipeline stage. MG Guide runs a synthetic-data vertical slice where Gemini 3.5
extracts meeting context, Google ADK sequences specialized agents, and a
deterministic OL3 policy gate either permits the follow-up path or fail-closes
on ambiguous identity — with Cloud Run hosting and Firestore audit proof on
Google Cloud.

## The problem

Sales follow-up is high-stakes and repetitive. Manual CRM hygiene loses deals
and creates inconsistent records. Fully autonomous writes without governance are
unacceptable in enterprise fleets. Teams need **agentic speed with deterministic
control**.

## What we built

A bounded vertical slice, not a broad CRM rewrite:

1. **Meeting Context Agent** — Gemini 3.5 Flash extracts summary, needs,
   objections, commitments, next step, and opportunity signal.
2. **Relationship Context Agent** — resolves synthetic CRM contact/opportunity
   context offline.
3. **Follow-Up Planning Agent** — proposes a structured follow-up plan.
4. **OL3 deterministic policy gate** — sole authority for allow/block.
5. **MG Guide card / judge surface** — salesperson-visible success and
   needs-review states.
6. **Cloud Run** — competition judge service on Google Cloud.
7. **Firestore** — authorized `workflow_runs` audit persistence proof.

## How it works (SUCCESS)

Synthetic transcript → Meeting Context → Relationship Context → Follow-Up
Planning → OL3 authorization → permitted synthetic effect/audit labels → MG
Guide completed next-step state. Demo path keeps `external_effects=0` for
unauthorized external CRM mutation while showing the governed completion state.

## How it works (FAIL-CLOSED)

Ambiguous contact identity → agents may still propose → OL3 emits
`AMBIGUOUS_CONTACT` → writes not attempted → workflow `blocked` / needs-review
→ **zero unauthorized effects**.

## Google technologies used (exact)

| Layer | Exact declaration |
| --- | --- |
| Model | **Gemini 3.5 Flash** (`gemini-3.5-flash`) via **Vertex AI** (`global`) |
| Agent framework | **Google ADK** `google-adk==1.18.0` (`Runner`, `SequentialAgent`, `InMemorySessionService`) |
| Model SDK | `google-genai` Vertex client |
| Compute | **Cloud Run** service `mg-guide-agentic-sales-workspace-judge` · **us-east4** |
| Data / audit | **Cloud Firestore** database `devpost-google-contest` · collection `workflow_runs` |
| Project | **mg-devpost** |
| APIs | Vertex AI / Generative Language as enabled for the project |

## Architecture (short)

```text
Transcript → [ADK agents + Gemini] → OL3 policy gate
                ↓ allow                    ↓ block
         MG Guide completed          MG Guide needs-review
                ↓
     Firestore audit (authorized)
CRM/tool boundary never accepts unilateral agent writes.
```

Full diagram:
`docs/architecture/meeting-follow-up-v1-competition-architecture.md`

## Demo

- Local judge: `POST /demo/meeting-follow-up` with `SUCCESS` / `AMBIGUOUS_CONTACT`
- Hosted (IAP): Cloud Run URL for `mg-guide-agentic-sales-workspace-judge`
- Script: `docs/demo/meeting-follow-up-v1-4min-demo-script.md`
- Demo truth boundary: `docs/demo/meeting-follow-up-demo-v1.md`

## Proof markers (competition)

```text
GEMINI_EXECUTION=PASS
ADK_EXECUTION=PASS
CLOUD_RUN_DEPLOYMENT=PASS
FIRESTORE_AUDIT=PASS
SUCCESS_SCENARIO=PASS
FAIL_CLOSED_SCENARIO=PASS
UNAUTHORIZED_EXTERNAL_EFFECTS=0
JUDGE_DEMO_LIVE_GHL_MUTATION=NO

BUSINESS_CONTENT_INGESTION_PROVEN=YES
PROVIDER_CONTRACT_INGESTION_PROVEN=YES
GHL_LIVE_SYNTHETIC_WRITE_PROVEN=YES
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO

CONTEST_RUNTIME_CODE_GAP_EXISTS=NO
END_TO_END_LIVE_EVIDENCE_GAP_EXISTS=YES
```

Acceptance packet:
`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`

Historical live synthetic CRM packet (one-shot Grant 008; consumed; not judge demo):
`proof/nw008/nw-008-at1-live-execution-result-008.md`

Provider-contract ingestion packets:
`proof/nw008/nw-008-at1-write-credential-readiness.md`,
`proof/nw008/nw-008-at1-create-note-request-contract-reconciliation.md`

### Evidence lanes (do not collapse)

A synthetic meeting transcript was successfully ingested and extracted through
live Gemini into schema-valid meeting context. Separately, a one-shot
human-authorized live synthetic GoHighLevel execution successfully created and
verified a CRM note and updated and verified an opportunity stage. HighLevel MCP
operation metadata and schemas were also retrieved and used to reconcile the
write transport contract. The current evidence does not claim that the exact
Gemini-derived note content was written to GoHighLevel in the same live
execution. The judge demo remains deterministic and performs no live CRM
mutation. Any additional live GoHighLevel execution requires a new
authorization.

## Built with

- Python 3
- Google ADK
- Gemini 3.5 Flash (Vertex AI)
- Cloud Run
- Cloud Firestore
- Deterministic OL3 policy engine
- Synthetic fixtures only (competition safety)

## Challenges

- Separating **proposal** (agents) from **authorization** (policy) without
  diluting the demo.
- Proving **Gemini 3.5+** on Vertex (`global`) while keeping CI deterministic
  via stub mode.
- IAP-gated Cloud Run requires human 2FA for browser walks; local parity keeps
  the scenario contract honest.
- Closing read-only Marketplace source-authority investigation without
  reconciliation mutation.

## Accomplishments

- End-to-end SUCCESS and fail-closed paths with zero unauthorized effects
- Live Gemini 3.5 meeting-context extraction with schema validation
  (`BUSINESS_CONTENT_INGESTION_PROVEN=YES`; `schema_valid=true`;
  `extraction_confidence=0.98`)
- HighLevel MCP provider-contract ingestion and create-note transport
  reconciliation (`PROVIDER_CONTRACT_INGESTION_PROVEN=YES`;
  `idempotencyRequired=YES` / `idempotencyKey` before Grant 008)
- Historical one-shot live synthetic GoHighLevel note+stage with readback
  under consumed Grant 008 (`GHL_LIVE_SYNTHETIC_WRITE_PROVEN=YES`;
  `TOTAL_GHL_CALLS_EXECUTED=6`; `MODELED_GHL_WRITES=2`; `AT1_COMPLETE=YES`)
- ADK package-bound multi-agent runtime proof
- Cloud Run Ready + Firestore Stage B audit smoke PASS
- Competition packet: architecture, demo script, acceptance proof, Devpost copy
- Explicit honesty that transcript-to-live-GHL is **not** claimed as one run
  (`INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO`)

## What's next

- Human-recorded 4-minute demo video from the script
- Optional IAP-authenticated hosted walkthrough
- Optional **new** human-authorized live synthetic CRM execution if a single
  transcript→Gemini→live-GHL evidence run is required for a later packet
  (Grant 008 is **consumed and non-reusable**; private exact-ID allowlist;
  no real customer records; judge demo stays non-mutating)

Do **not** read “what's next” as “CRM mutation was never proven.” Live
synthetic note+stage already succeeded historically under Grant 008. What
remains is the **end-to-end live evidence** join (same-run Gemini-derived
content into live GHL), not a contest runtime code gap.

## Team / repo

- Repository: `themg-max/mg-guide-agentic-sales-workspace`
- Branch: `plan/nw008-contest-ingestion-crm-claim-normalization-001`

## Cover / media checklist

- [ ] Architecture diagram export (from mermaid doc)
- [ ] SUCCESS card screenshot
- [ ] FAIL-CLOSED needs-review screenshot
- [ ] Cloud Run Ready screenshot
- [ ] Demo video (~4 min)
