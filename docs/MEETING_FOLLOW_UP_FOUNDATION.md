# MG Guide Agentic Sales Workspace — Meeting Follow-Up Foundation

**Artifact:** `docs/MEETING_FOLLOW_UP_FOUNDATION.md`
**Workflow:** `meeting_follow_up_v1`
**Public status:** `FOUNDATION` (sanitized from reviewed PROPOSED architecture)
**Phase:** Planning / architecture freeze — **no runtime implementation** in the
bootstrap commit that introduced this file
**Competition:** Google All Things Agentic Hackathon
**Track target:** Fortified Enterprise Fleet
**Governance note:** Conceptual design approved for public foundation publication
with synthetic data only. This document does **not** authorize CRM writes,
cloud provisioning, IAM changes, or secret configuration.

> **Environment-semantics normalization (current authority):** the GoHighLevel
> target is the **business-active canonical CRM under synthetic-only bounded
> execution controls**. No isolated/dedicated GHL test location exists or is
> required; safety derives from deterministic controls and the private exact-ID
> allowlist, not from environmental isolation. Environment readiness does not
> authorize mutation. See
> [`nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](nw008/nw-008-active-crm-synthetic-only-normalization-001.md)
> (`NW008_ACTIVE_CRM_SYNTHETIC_ONLY_NORMALIZATION_001`) — the controlling
> superseding interpretation wherever earlier sections of this document retain
> historical isolated/test-account phrasing.

> **Sanitization:** Private/internal repository paths, lane identifiers, private
> endpoints, project IDs, service accounts, and non-public hostnames have been
> removed or replaced with `UNKNOWN` / generic labels for public release.

---

## 1. Product objective

After a sales meeting ends, MG Guide turns the meeting transcript into a governed
CRM follow-up record without the salesperson manually summarizing the
conversation, finding the CRM record, determining the appropriate pipeline
state, and documenting the next step.

**Vertical slice promise:** one synthetic transcript in → one verified CRM note,
at most one policy-permitted opportunity-stage change, one Firestore audit
record, and one MG Guide next-step brief out.

This artifact freezes the `meeting_follow_up_v1` vertical slice for the
2026 "All Things Agentic" competition. Anything not listed in §5 Scope is out of
scope for the competition period.

---

## 2. Judge / user value

**For the salesperson (user):**

- Eliminates post-meeting administrative work: summarization, CRM lookup,
  pipeline-state judgment, next-step documentation.
- Surfaces a next-step brief with evidence rather than another transcript dump.
- Blocked/ambiguous outcomes are surfaced explicitly instead of silently
  writing to the wrong record.

**For competition judges:**

- Multi-agent system (Google ADK + Gemini 3.5+) performing *operational* CRM work,
  not conversational Q&A.
- Governance is behavioral, not marketing copy: the demo shows a failure
  fixture producing contact-ambiguity block with **zero CRM writes**.
- Clean transport story: MG MCP for trusted organizational context (read-only);
  historical GHL MCP discovery evidence is preserved, while the current CRM
  transport planning direction is a governed HighLevel REST v3 adapter with no
  implementation or execution authorization yet.
- Deterministic policy gate between agent recommendation and CRM mutation.
- Full audit trail in Firestore proving what happened and why.

---

## 3. Pre-existing baseline (NOT competition work)

The following capabilities predate the competition period and must not be
presented as invented for this hackathon:

| Capability | Status before competition |
| --- | --- |
| MG MCP retrieval / trust handling / governed context | Pre-existing |
| MG Guide application surface (authenticated route) | Pre-existing |
| OL3 orchestration authority, contracts, runtime-contract concepts | Pre-existing |
| Governance framework concepts (lanes, gates, proof packets, boundary checks) | Pre-existing |
| Basic orchestration concept and layered instruction architecture | Pre-existing |

See also [`COMPETITION_BASELINE.md`](COMPETITION_BASELINE.md).

---

## 4. Competition-period new work

The new-work claim centers on:

> A competition-period meeting-follow-up agent workflow that integrates
> Google ADK/Gemini, OL3 workflow enforcement, governed CRM transport, Firestore
> audit state, and a new MG Guide sales-workspace experience.

Concretely:

1. `meeting_follow_up_v1` workflow and state machine (§9).
2. Four ADK agents (§7) with Gemini extraction/evaluation.
3. Governed CRM transport boundary (§11).
4. Synthetic-only bounded GHL write policy and mutation allowlist on the
   business-active canonical CRM (§12).
5. Firestore run-audit schema and records (§13).
6. MG Guide Meeting Follow-Up card UI (§14).
7. Google Cloud deployment of the slice (planned Cloud Run; not provisioned here).
8. Synthetic demo fixtures and proof flow (§15, §18).

---

## 5. Scope / non-scope

### In scope (frozen)

- One workflow: `meeting_follow_up_v1`.
- Input: one synthetic meeting transcript (fixture, §15).
- CRM environment: **business-active canonical CRM under synthetic-only
  bounded execution controls** — private exact-ID allowlist, preverified
  synthetic contact/opportunity only; no isolated/dedicated GHL test location
  exists or is required (see
  [`nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](nw008/nw-008-active-crm-synthetic-only-normalization-001.md)).
- Mutations per run: at most **one** contact note create and at most **one**
  opportunity-stage change (single predefined transition, §12).
- Read-back verification of every mutation.
- Firestore audit record per run.
- MG Guide Meeting Follow-Up card (success + needs-review states).

### Non-scope (blocked for the competition period)

- Real-customer and non-allowlisted CRM mutation is forbidden. Bounded CRM
  mutation against the privately allowlisted preverified synthetic records may
  occur only under a separate human-reviewed execution authorization bound to
  exact transport, credential, private IDs, allowed transition, operation
  budget, and proof requirements. This artifact does **not** authorize such
  execution now (`LIVE_CRM_MUTATION_AUTHORIZED=NO`;
  `SEPARATE_HUMAN_MUTATION_AUTHORIZATION_REQUIRED=YES`;
  `REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO`).
- Real customer/CRM data in fixtures, demos, or public artifacts.
- Email/SMS sending; calendar mutation.
- Contact creation or deletion; opportunity creation or deletion.
- Bulk CRM operations; arbitrary stage movement; pipeline/workflow modification.
- Monetary-value edits, owner changes, tagging, communications.
- End-to-end sales lifecycle automation.
- Production activation, IAM/env/secret changes, MG MCP writes.
- Unapproved raw GoHighLevel REST calls or REST adapter implementation/execution
  without a separate architecture decision and execution authorization (§11).

---

## 6. Architecture

```text
Synthetic Meeting Transcript
          │
          ▼
    OL3 Run Created
          │
          ▼
┌───────────────────────┐
│ Transcript Analyst    │
│ Gemini / Google ADK   │
└──────────┬────────────┘
           │ structured extraction
           ▼
┌───────────────────────┐
│ Meeting Evaluator     │
│ confidence/evidence   │
└──────────┬────────────┘
           │
           ├──────────────► MG MCP
           │                governed playbook/
           │                policy context (read-only)
           ▼
┌───────────────────────┐
│ CRM Resolution Agent  │
│ Google ADK + CRM      │
│ transport             │
└──────────┬────────────┘
           │ exact CRM identity
           ▼
┌───────────────────────┐
│ Workflow Policy Gate  │
│ deterministic / OL3   │
└──────────┬────────────┘
           │
      ┌────┴──────────────┐
      │                   │
      ▼                   ▼
Create CRM Note      Stage Proposal
via governed         via governed
CRM transport        CRM transport
      │                   │
      │            policy permits?
      │              │         │
      │             YES        NO
      │              │         │
      └───────┬──────┘         ▼
              │            leave unchanged
              ▼
         Verify CRM
          mutation
              │
              ▼
      Firestore Audit Record
              │
              ▼
           MG Guide
       Next-Step Brief
```

### Integration boundary (mandatory abstraction)

```text
Incorrect abstraction          Recommended abstraction

Agent → arbitrary CRM API      Agent
                                ↓
                               OL3 authorization
                                ↓
                               Governed CRM transport adapter
                                ↓
                               GoHighLevel Canonical CRM
                               (business-active; synthetic-only
                               bounded controls)
```

Roles:

- **MG Guide:** salesperson workspace (application surface, not authority).
- **OL3:** workflow authority/control; deterministic mutation gate.
- **ADK/Gemini:** specialized reasoning agents (propose, never decide).
- **MG MCP:** trusted organizational context — governed, read-only.
- **CRM transport:** next planning direction is a governed HighLevel REST v3
  adapter; historical GHL MCP evidence is preserved, but generic GHL MCP
  implementation is blocked.
- **Firestore:** runtime/audit state.
- **Cloud Run (planned):** future host for the slice runtime.

Authority rule: agents propose facts/actions; deterministic policy and OL3
workflow state determine whether a GHL mutation is allowed.

---

## 7. Agent responsibilities

Maximum **four** agents.

### A. Transcript Extraction Agent (`transcript_extractor:v1`)

- Model: Gemini 3.5+ via Google ADK.
- Input: transcript only.
- Output: strictly structured meeting extraction (`extraction` block, §8).
- Cannot: call GHL, choose final workflow transitions, mutate anything.

### B. CRM Resolution Agent (`crm_resolver:v1`)

- Input: normalized participant identifiers.
- Tools: exact-ID CRM read operations only, through a separately governed
  transport contract.
- **Offline synthetic fixture behavior only** — the email / phone /
  safe-normalized matching ladder below applies to offline fixture resolution
  in the synthetic harness. It is **not** a live CRM search contract.

```text
email exact match
  ↓
phone exact match
  ↓
safe normalized match
  ↓
ambiguous / not-found
```

- **Future live canonical CRM access:** preverified private exact IDs only.
  No search. No list. No pagination. No alternate target. Binding mismatch
  ⇒ fail closed (zero writes).
- Critical rule: the LLM must never simply "pick the closest contact."
  Ambiguous match ⇒ `AMBIGUOUS_CONTACT` (fail closed, zero writes).

### C. Follow-Up Policy Agent / Evaluator (`followup_evaluator:v1`)

- May use Gemini for interpretation; the actual mutation gate is deterministic.
- Compares extraction against: permitted sales workflow, current opportunity
  state, allowed stage-transition matrix, confidence threshold, required
  evidence, MG MCP governed policy/context.
- Example transition rule:

```yaml
stage_transition:
  from: discovery_scheduled
  to: discovery_complete
  allowed_when:
    contact_match: exact
    meeting_completed: true
    extraction_confidence_min: 0.90
    evidence_present: true
```

- The agent **recommends**; OL3 policy logic **decides**.

### D. CRM Action Agent (`crm_action:v1`)

- Only agent allowed to request CRM mutations after separate human execution
  authorization.
- Allowed: (1) create one meeting note; (2) optionally move **one**
  opportunity stage.
- Blocked: creating contacts, deleting records, bulk mutations, editing
  monetary value, changing owner, tagging, sending communications, changing
  workflows, modifying pipelines.
- This is the blast-radius control.

---

## 8. `meeting_follow_up_packet_v1`

One canonical object passed between agents; no free-form prose handoffs.

Machine-readable schema: [`../contracts/meeting_follow_up_packet.schema.json`](../contracts/meeting_follow_up_packet.schema.json)

```yaml
schema: meeting_follow_up_packet_v1

run:
  run_id: string
  workflow: meeting_follow_up_v1
  created_at: datetime
  status: received|extracting|resolving|evaluating|writing|completed|blocked|failed|completed_with_review

meeting:
  meeting_id: string
  occurred_at: datetime
  source: synthetic_demo
  transcript_hash: sha256

participants:
  - name: string
    email: string|null
    phone: string|null
    role: prospect|client|agent|unknown

extraction:
  summary: string
  needs:
    - string
  objections:
    - string
  commitments:
    - owner: string
      action: string
      due_date: date|null
  next_step:
    action: string
    owner: string
    target_date: date|null
  opportunity_signal:
    recommended_stage: string|null
    rationale: string|null

evidence:
  transcript_spans:
    - field: string
      excerpt_id: string
  extraction_confidence: number

crm_resolution:
  status: matched|ambiguous|not_found
  contact_id: string|null
  opportunity_id: string|null
  match_basis: email|phone|name|none
  candidate_count: integer

policy:
  note_write: allowed|blocked
  stage_write: allowed|approval_required|blocked
  reason_codes:
    - string

mutations:
  note:
    attempted: boolean
    verified: boolean
    record_id: string|null

  opportunity_stage:
    attempted: boolean
    from_stage: string|null
    to_stage: string|null
    verified: boolean

brief:
  headline: string
  meeting_summary: string
  crm_actions: [string]
  next_action: string
  salesperson_attention_required: boolean

audit:
  started_at: datetime
  completed_at: datetime|null
  agents_used: [string]
  tools_used: [string]
  warnings: [string]
  final_disposition: completed|completed_with_review|blocked|failed
```

---

## 9. OL3 state machine

Machine-readable states: [`../contracts/workflow_states.yaml`](../contracts/workflow_states.yaml)

```text
received
   │  transcript accepted, run_id assigned
   ▼
extracting
   │  transcript_extractor:v1 returns structured extraction
   │  ├─ confidence < threshold ──────────► blocked (LOW_EXTRACTION_CONFIDENCE)
   ▼
resolving
   │  crm_resolver:v1 resolves identity via exact-ID CRM reads
   │  ├─ ambiguous ───────────────────────► blocked (AMBIGUOUS_CONTACT)
   │  ├─ not found ───────────────────────► blocked (CONTACT_NOT_FOUND)
   │  ├─ opportunity missing ─────────────► blocked (OPPORTUNITY_NOT_FOUND)
   ▼
evaluating
   │  followup_evaluator:v1 + deterministic OL3 policy gate
   │  ├─ transition disallowed ───────────► writing (note only; stage unchanged,
   │  │                                     reason STAGE_TRANSITION_NOT_ALLOWED)
   ▼
writing
   │  crm_action:v1 performs allowlisted mutations via governed CRM transport
   │  ├─ tool failure ────────────────────► failed (GHL_TOOL_FAILURE)
   │  ├─ read-back mismatch ──────────────► failed (GHL_WRITE_NOT_VERIFIED)
   ▼
completed | completed_with_review
```

Invariants:

- Every `blocked`/`failed` state fails **closed**: zero further CRM writes.
- A tool returning success is **not** completion; read-back verification is
  required before the workflow declares a mutation verified.
- Max one note write and one stage write per run, enforced by OL3 policy,
  not by agent self-restraint.

---

## 10. MG MCP context contract

- MG MCP remains **read-only** context authority. No MG MCP writes in this
  workflow, ever.
- Consumed context: sales playbook/policy context used by the evaluator
  (stage-transition policy, confidence thresholds, evidence requirements).
- **UNKNOWN (public foundation):** concrete MG MCP endpoint, alias set, and
  index names are not published here. Implementation must resolve them under
  separate governed authority without exposing private infrastructure.
- Existing governance treats GHL/CRM mutation as blocked unless separately
  authorized. The competition implementation requires its **own bounded
  synthetic-only GHL mutation authorization** against the privately bound
  canonical location before write phases (§12, §16) — a separate human-reviewed
  execution authorization bound to exact transport, credential, location,
  synthetic IDs, allowed stage transition, operation budget, and proof
  requirements.

---

## 11. CRM transport contract

### 11.1 Discovery status

**Public foundation status:**

- No live CRM transport is connected to this repository bootstrap.
- **No live tool-schema inventory is claimed here.**
- All authorized operation names, input schemas, output schemas, and error
  behaviors remain `UNKNOWN` until a separately authorized architecture unit
  against the authorized CRM binding.

**Documentation-derived candidate inventory (historical provider docs only —
candidate evidence, NOT verified against the authorized CRM binding):**

Historical provider docs described conceptual operations for contacts and
opportunities. Those documented names are **not** frozen as implementation
identifiers in this repository, and they do not authorize generic search, list,
pagination, arbitrary provider request bodies, or live calls.

### 11.2 Required capability inventory (implementation preflight)

Each row must be designed in the next architecture lane against the
**authorized CRM binding** (business-active canonical CRM under synthetic-only
bounded controls) before any implementation. Do not code against placeholder
names, generic search/list/pagination, or arbitrary provider request bodies.

| Required capability | Exact tool/operation | Input schema | Output schema | Auth/scopes | Write semantics | Error behavior | Idempotency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GET exact contact | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| GET exact opportunity | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| POST one note | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | max one note create | UNKNOWN | UNKNOWN |
| GET exact note for readback | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (readback) | UNKNOWN | UNKNOWN |
| PUT bounded opportunity stage update | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | max one predefined stage update | UNKNOWN | UNKNOWN |
| GET exact opportunity for readback | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (readback) | UNKNOWN | UNKNOWN |
| Mutation read-back / verification | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |

**Hard stop:** if the next architecture unit cannot authoritatively resolve
the exact HighLevel REST operations, schemas, required fields/scopes, error
behavior, and read-back verification contract, STOP. Do not invent operation
names, broad search/list behavior, alternate-target discovery, or arbitrary
provider request bodies.

### 11.3 Workflow tool manifest (historical evidence — not REST authority)

[`../contracts/ghl_tool_manifest.yaml`](../contracts/ghl_tool_manifest.yaml):

```text
contracts/ghl_tool_manifest.yaml
  = historical Phase 2A MCP discovery evidence
  = not the planned REST implementation contract
  = no REST execution authority
```

Do not treat that manifest as the HighLevel REST adapter contract, as current
transport authority, or as mutation authorization. Placeholder logical names
and historical MCP identifiers remain discovery evidence only until a separate
architecture unit resolves the exact REST operations and schemas.

---

## 12. GHL mutation policy

- Environment: the target CRM is the **business-active canonical GoHighLevel
  environment** under synthetic-only bounded execution controls. Competition
  live proof is restricted to privately allowlisted synthetic records and
  exact-ID operations. **No real customer record may be searched, read, or
  mutated.** Environment readiness does not authorize mutation. Any note
  creation or opportunity-stage update requires a separate human-reviewed
  execution authorization bound to the exact transport, credential, location,
  synthetic IDs, allowed stage transition, operation budget, and proof
  requirements. No broad search, no list/pagination expansion, no
  alternate-target discovery, no automatic retry, no compensating mutation.
- Allowlist per run: max **one** `note_create`, max **one**
  `opportunity_stage_update`.
- Stage mutation is restricted to **one predefined transition** for the demo
  (`discovery_scheduled → discovery_complete`); arbitrary pipeline movement
  must not be possible.
- Preconditions for stage mutation (all required):
  - `crm_resolution.status == matched` with `match_basis` in {email, phone};
  - `extraction_confidence >= 0.90`;
  - evidence spans present for the recommended stage;
  - transition present in the allowed-transition matrix;
  - policy gate returns `allowed` (deterministic, OL3-owned).
- Every mutation requires read-back verification before being recorded as
  `verified: true`.
- Mutation authorization is a separate, explicit grant: this artifact does
  **not** authorize CRM writes.

---

## 13. Firestore audit contract

Document path: `workflow_runs/{run_id}`

```yaml
workflow: meeting_follow_up_v1
status: completed

input:
  meeting_id: demo_meeting_001
  transcript_hash: ...

agents:
  - transcript_extractor:v1
  - crm_resolver:v1
  - followup_evaluator:v1
  - crm_action:v1

crm:
  contact_resolution: matched
  note_write: verified
  stage_transition: verified

policy:
  stage_transition_allowed: true
  reason_codes:
    - MEETING_COMPLETED
    - EXACT_CONTACT_MATCH

tool_calls:
  ghl_mcp:
    reads: 3
    writes: 2

timestamps:
  started_at: ...
  completed_at: ...

final_disposition: completed
```

Storage rules:

- Do **not** store the entire transcript unnecessarily.
- Store: transcript hash, synthetic fixture ID, structured output, action
  evidence.
- Firestore records operational proof, not chat memory.

---

## 14. MG Guide UX — Meeting Follow-Up card

Not another chat response. A dedicated **Meeting Follow-Up card** with two
demo states.

### State 1 — Completed

> **Taylor Morgan — Discovery Meeting**
>
> Meeting processed successfully.
>
> **What we learned**
> - Primary need: retirement income planning
> - Key concern: liquidity
> - Timeline: next 60 days
>
> **CRM**
> ✓ Contact resolved
> ✓ Meeting note created
> ✓ Opportunity moved: Discovery Scheduled → Discovery Complete
>
> **Next step**
> Prepare recommendation review and follow up within 48 hours.
>
> **Evidence**
> `4 agents · 7 governed tool calls · policy PASS · audit recorded`

### State 2 — Needs review

> Contact resolution returned two candidates.
>
> **No CRM changes were made.**

The blocked state is a first-class demo outcome, equal in importance to the
success state.

---

## 15. Synthetic fixtures

All fixtures are synthetic; no real customer/CRM data may appear in fixtures,
demos, or public artifacts.

```text
fixtures/
  transcript-success.txt            # exact-match contact, permitted transition
  transcript-ambiguous-contact.txt  # two candidate contacts → BLOCKED, 0 writes
  transcript-no-stage-change.txt    # note allowed, stage transition not allowed
```

Fixture requirements:

- Synthetic participant identities (e.g., "Taylor Morgan") with fixture-only
  emails/phones corresponding to the preverified synthetic records on the
  canonical location (private exact-ID allowlist; IDs never published).
- Each fixture maps to exactly one expected `final_disposition` and expected
  reason codes.
- Fixture IDs are recorded in the Firestore audit record (§13).

---

## 16. Failure codes

All failure paths fail **closed** (no further CRM writes).

Canonical list: [`../contracts/failure_codes.yaml`](../contracts/failure_codes.yaml)

```text
AMBIGUOUS_CONTACT
CONTACT_NOT_FOUND
OPPORTUNITY_NOT_FOUND
LOW_EXTRACTION_CONFIDENCE
STAGE_TRANSITION_NOT_ALLOWED
GHL_TOOL_FAILURE
GHL_WRITE_NOT_VERIFIED
```

### Implementation sequence (phased, gated)

| Phase | Content | Gate |
| --- | --- | --- |
| 0 | Competition contract: baseline vs. new-work charter | This public foundation |
| 1 | Packet schema, deterministic state machine, transition rules, error codes, fixtures | Schema tests pass; no AI, no GHL |
| 2 | **CRM transport contract architecture** (§11.2) against the authorized CRM binding | All UNKNOWN rows resolved or STOP |
| 3 | Read-only vertical slice: transcript → extraction → exact-ID CRM resolution → proposed note/stage → Firestore → MG Guide | End-to-end read-only proof, zero mutations |
| 4 | Note mutation only (one write + read-back verification) | Bounded mutation authorization granted |
| 5 | Stage mutation (single predefined transition + read-back verification) | Same authorization; transition matrix enforced |
| 6 | Failure paths: all §16 codes demonstrably fail closed | Acceptance tests pass |

---

## 17. Acceptance tests

| # | Test | Expected outcome |
| --- | --- | --- |
| AT-1 | `transcript-success.txt` full run | `completed`; note `verified`; stage `discovery_scheduled → discovery_complete` `verified`; audit record present; MG Guide card State 1 |
| AT-2 | `transcript-ambiguous-contact.txt` | `blocked` with `AMBIGUOUS_CONTACT`; **0 CRM writes**; MG Guide card State 2 |
| AT-3 | `transcript-no-stage-change.txt` | Note `verified`; stage unchanged with `STAGE_TRANSITION_NOT_ALLOWED` reason; disposition `completed_with_review` |
| AT-4 | Contact not found | `blocked` with `CONTACT_NOT_FOUND`; 0 writes |
| AT-5 | Extraction confidence below threshold | `blocked` with `LOW_EXTRACTION_CONFIDENCE`; 0 writes |
| AT-6 | GHL tool failure during write | `failed` with `GHL_TOOL_FAILURE`; mutation recorded `attempted: true, verified: false` |
| AT-7 | Write succeeds but read-back mismatch | `failed` with `GHL_WRITE_NOT_VERIFIED`; no completion declared |
| AT-8 | Per-run mutation caps | Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice |
| AT-9 | Blocked tool invocation (e.g., contact create) | Refused at tool-manifest layer; recorded in audit warnings |
| AT-10 | Audit completeness | Every run (success, blocked, failed) produces a `workflow_runs/{run_id}` record with agents, tool counts, reason codes, disposition |

---

## 18. Demo proof (~4-minute flow)

| Time | Beat | Content |
| --- | --- | --- |
| 0:00–0:25 | Friction | Salesperson finishes a meeting and must interpret notes, find the CRM record, write a useful summary, decide the next pipeline state, remember the next action |
| 0:25–0:45 | Trigger | Drop in a synthetic transcript; show `Meeting Follow-Up — RUNNING` |
| 0:45–1:30 | Multi-agent work | Transcript Agent ✓ · CRM Resolution ✓ (exact-ID CRM transport) · Policy Evaluator ✓ · CRM Action running — Gemini/ADK genuinely doing the work |
| 1:30–2:15 | Actual action | Synthetic records on the canonical GoHighLevel CRM before (no note, stage = Discovery Scheduled) / after (structured note added, stage = Discovery Complete), under a separately authorized synthetic-only bounded execution grant |
| 2:15–2:45 | Governance proof | Firestore audit + MG Guide next-step brief |
| 2:45–3:20 | Failure proof | Ambiguous fixture: two candidates → `AMBIGUOUS_CONTACT`, `CRM writes: 0` |
| 3:20–3:45 | Architecture | MG Guide → OL3 → ADK+Gemini → MG MCP (context) + governed CRM transport → Firestore (proof) |
| 3:45–4:00 | Close | "MG Guide turns meetings into governed sales work — not another transcript summary." |

---

## 19. Security / privacy

See [`SECURITY.md`](SECURITY.md).

- **Data guard:** synthetic transcripts, and CRM access limited to the
  business-active canonical CRM under synthetic-only bounded execution
  controls (private exact-ID allowlist; preverified synthetic
  contact/opportunity only). No real customer record search, read, or
  mutation. No real customer/CRM data in competition artifacts, fixtures, or
  public material.
- **Least privilege:** explicit tool allowlists; blocked tools enumerated.
- **Prompt-injection posture:** retrieved data and transcript content are
  treated as **data, not instructions**.
- **Human/authority boundary:** risky mutation surfaces sit behind
  deterministic policy plus explicit bounded authorization.
- **Secrets:** never committed to the repository.
- **Audit:** every run leaves a Firestore record with reason codes and
  tool-call counts.

---

## 20. Definition of done

`meeting_follow_up_v1` is DONE for the competition when all of the following
hold:

1. §11.2 capability inventory fully resolved against the authorized CRM
   binding (no `UNKNOWN` rows) — or an explicit governed STOP decision exists.
2. Bounded synthetic-only GHL mutation authorization against the canonical
   location recorded before any write phase.
3. All acceptance tests AT-1 … AT-10 pass with recorded evidence.
4. The three fixtures (§15) each produce their expected disposition
   end-to-end in the deployed environment.
5. Read-back verification demonstrated for both mutation types.
6. Firestore audit records exist for every demo run.
7. MG Guide card renders both Completed and Needs-review states.
8. The ~4-minute demo (§18) is executable start-to-finish without production
   data.
9. Submission material explicitly separates pre-existing baseline (§3) from
   competition-period work (§4).
10. Proof packet and branch/PR closeout completed under repository governance.

---

## Appendix A — Discovery evidence log (sanitized)

| Check | Result |
| --- | --- |
| Live CRM transport connected to this public foundation repo | Absent at bootstrap |
| Live GHL/HighLevel operation schema inventory | Not captured — UNKNOWN |
| Public provider documentation | Consulted as historical candidate evidence only |
| Mutation tools verified against the authorized CRM binding | NOT VERIFIED — UNKNOWN |
| Private MG infrastructure details | Intentionally omitted from public artifact |

---

## Appendix B — Blocked actions (competition period)

- Real-customer and non-allowlisted CRM mutation (forbidden). Bounded CRM
  mutation against privately allowlisted preverified synthetic records requires
  a separate human-reviewed execution authorization
  (`LIVE_CRM_MUTATION_AUTHORIZED=NO`;
  `SEPARATE_HUMAN_MUTATION_AUTHORIZATION_REQUIRED=YES`;
  `REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO`)
- Real customer data
- Email/SMS
- Calendar mutation
- Contact creation/deletion
- Bulk CRM operations
- Arbitrary stage movement
- Production activation
- IAM/env/secrets changes in foundation phases without activation authority
- MG MCP writes
- Direct implementation on `main` after bootstrap
