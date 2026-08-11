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
- Clean MCP story: MG MCP for trusted organizational context (read-only),
  GHL MCP as the standardized boundary for external business-system actions.
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
> Google ADK/Gemini, OL3 workflow enforcement, GHL MCP CRM tools, Firestore
> audit state, and a new MG Guide sales-workspace experience.

Concretely:

1. `meeting_follow_up_v1` workflow and state machine (§9).
2. Four ADK agents (§7) with Gemini extraction/evaluation.
3. GHL MCP integration as the CRM boundary (§11).
4. GHL test-account write policy and mutation allowlist (§12).
5. Firestore run-audit schema and records (§13).
6. MG Guide Meeting Follow-Up card UI (§14).
7. Google Cloud deployment of the slice (planned Cloud Run; not provisioned here).
8. Synthetic demo fixtures and proof flow (§15, §18).

---

## 5. Scope / non-scope

### In scope (frozen)

- One workflow: `meeting_follow_up_v1`.
- Input: one synthetic meeting transcript (fixture, §15).
- CRM environment: **isolated/test GHL location/account only**.
- Mutations per run: at most **one** contact note create and at most **one**
  opportunity-stage change (single predefined transition, §12).
- Read-back verification of every mutation.
- Firestore audit record per run.
- MG Guide Meeting Follow-Up card (success + needs-review states).

### Non-scope (blocked for the competition period)

- Production CRM writes of any kind.
- Real customer/CRM data in fixtures, demos, or public artifacts.
- Email/SMS sending; calendar mutation.
- Contact creation or deletion; opportunity creation or deletion.
- Bulk CRM operations; arbitrary stage movement; pipeline/workflow modification.
- Monetary-value edits, owner changes, tagging, communications.
- End-to-end sales lifecycle automation.
- Production activation, IAM/env/secret changes, MG MCP writes.
- Raw GoHighLevel REST integration as a substitute for GHL MCP (§11).

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
│ Google ADK + GHL MCP  │
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
via GHL MCP          via GHL MCP
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

Agent → GHL REST API           Agent
                                ↓
                               OL3 authorization
                                ↓
                               GHL MCP Client
                                ↓
                               GHL MCP Server
                                ↓
                               GoHighLevel Test CRM
```

Roles:

- **MG Guide:** salesperson workspace (application surface, not authority).
- **OL3:** workflow authority/control; deterministic mutation gate.
- **ADK/Gemini:** specialized reasoning agents (propose, never decide).
- **MG MCP:** trusted organizational context — governed, read-only.
- **GHL MCP:** governed external business-system tools (CRM boundary).
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
- Tools: **GHL MCP read tools only**.
- Resolution ladder (strict order):

```text
email exact match
  ↓
phone exact match
  ↓
safe normalized match
  ↓
ambiguous / not-found
```

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

- Only agent possessing GHL MCP mutation capability.
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
   │  crm_resolver:v1 resolves identity via GHL MCP reads
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
   │  crm_action:v1 performs allowlisted mutations via GHL MCP
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
  test-account GHL mutation authorization** before write phases (§12, §16).

---

## 11. GHL MCP tool contract

### 11.1 Discovery status

**Public foundation status:**

- No live GHL MCP server is connected to this repository bootstrap.
- **No live tool-schema inventory is claimed here.**
- All authorized tool names, input schemas, output schemas, and error behaviors
  remain `UNKNOWN` until discovery against an authorized test account.

**Documentation-derived candidate inventory (public HighLevel MCP docs only —
candidate evidence, NOT verified against an authorized test account):**

Public docs describe a unified v2-style toolset that may include conceptual
operations such as search/fetch/describe/execute patterns for contacts and
opportunities. Those documented names are **not** frozen as implementation
identifiers in this repository.

### 11.2 Required capability inventory (implementation preflight)

Each row must be verified via live discovery against the **authorized test
account** before any implementation. Do not code against placeholder names.

| Required capability | Exact tool/operation | Input schema | Output schema | Auth/scopes | Write semantics | Error behavior | Idempotency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Contact search | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| Contact fetch | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| Opportunity search (per contact) | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| Pipeline/stage metadata fetch | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |
| Contact note create | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Opportunity stage update | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Mutation read-back / verification | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | n/a (read) | UNKNOWN | UNKNOWN |

**Hard stop:** if note-create or opportunity-stage-update does not exist in
the authorized MCP server, STOP. Do not silently switch to raw GHL APIs — that
substitution requires a new architecture decision through governance.

### 11.3 Workflow tool manifest (contract template)

See [`../contracts/ghl_tool_manifest.yaml`](../contracts/ghl_tool_manifest.yaml).
Placeholder logical names MUST be replaced with discovered names before
implementation.

---

## 12. GHL mutation policy

- Environment: isolated/test GHL location/account only. **No production CRM
  writes.**
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
  emails/phones intended for an isolated test GHL location.
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
| 2 | **GHL MCP contract discovery** (§11.2) against the test account | All UNKNOWN rows resolved or STOP |
| 3 | Read-only vertical slice: transcript → extraction → GHL MCP resolution → proposed note/stage → Firestore → MG Guide | End-to-end read-only proof, zero mutations |
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
| 0:45–1:30 | Multi-agent work | Transcript Agent ✓ · CRM Resolution ✓ (GHL MCP) · Policy Evaluator ✓ · CRM Action running — Gemini/ADK genuinely doing the work |
| 1:30–2:15 | Actual action | Test GoHighLevel CRM before (no note, stage = Discovery Scheduled) / after (structured note added, stage = Discovery Complete) |
| 2:15–2:45 | Governance proof | Firestore audit + MG Guide next-step brief |
| 2:45–3:20 | Failure proof | Ambiguous fixture: two candidates → `AMBIGUOUS_CONTACT`, `CRM writes: 0` |
| 3:20–3:45 | Architecture | MG Guide → OL3 → ADK+Gemini → MG MCP (context) + GHL MCP (CRM actions) → Firestore (proof) |
| 3:45–4:00 | Close | "MG Guide turns meetings into governed sales work — not another transcript summary." |

---

## 19. Security / privacy

See [`SECURITY.md`](SECURITY.md).

- **Data guard:** synthetic transcripts and an isolated/test GHL
  location/account only. No production CRM writes. No real customer/CRM data
  in competition artifacts, fixtures, or public material.
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

1. §11.2 capability inventory fully resolved against the authorized test
   account (no `UNKNOWN` rows) — or an explicit governed STOP decision exists.
2. Bounded test-account GHL mutation authorization recorded before any write
   phase.
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
| GHL MCP server connected to this public foundation repo | Absent at bootstrap |
| Live GHL/HighLevel tool schema inventory | Not captured — UNKNOWN |
| Public HighLevel MCP documentation | Consulted as candidate evidence only |
| Mutation tools verified against authorized test account | NOT VERIFIED — UNKNOWN |
| Private MG infrastructure details | Intentionally omitted from public artifact |

---

## Appendix B — Blocked actions (competition period)

- Production CRM writes
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
