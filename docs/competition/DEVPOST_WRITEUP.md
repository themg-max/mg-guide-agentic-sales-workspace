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
```

Acceptance packet:
`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`

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
- ADK package-bound multi-agent runtime proof
- Cloud Run Ready + Firestore Stage B audit smoke PASS
- Competition packet: architecture, demo script, acceptance proof, Devpost copy

## What's next

- Human-recorded 4-minute demo video from the script
- Optional IAP-authenticated hosted walkthrough
- Future separately authorized safe-environment CRM mutation lane (out of scope
  for this packet)

## Team / repo

- Repository: `themg-max/mg-guide-agentic-sales-workspace`
- Branch: `competition/meeting-follow-up-v1-acceptance-finalization-001`

## Cover / media checklist

- [ ] Architecture diagram export (from mermaid doc)
- [ ] SUCCESS card screenshot
- [ ] FAIL-CLOSED needs-review screenshot
- [ ] Cloud Run Ready screenshot
- [ ] Demo video (~4 min)
