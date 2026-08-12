# Phase 3 Unit 3 Implementation Packet — Follow-Up Planning Agent

| Field | Value |
| --- | --- |
| Grant | `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` |
| Ledger | NW-004 |
| Parent grant status | `AUTHORIZED_FOR_IMPLEMENTATION` / `IN_PROGRESS` |
| Unit 1 | **MERGED_COMPLETE** (PR #10 / `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7`) |
| Unit 2 | **MERGED_COMPLETE** (PR #11 head `3ab0b1dfa0c2c20a711156d5cf88febb5d21dbfa` / merge `a3d5a5731d7342463fe365e597e5d974d3420d08`) |
| Unit 3 name | Follow-Up Planning Agent |
| Packet status | **BOUNDED_IMPLEMENTATION_PACKET_READY** |
| Implementation started | **NO** |
| Candidate branch | `feat/meeting-follow-up-v1-follow-up-planning-agent-unit3` |
| External effects target | `0` |

This packet defines the reviewed Unit 3 implementation envelope only. It does
**not** authorize live GHL, CRM writes, deployment, or policy bypass. Do **not**
implement Unit 3 until this packet is reviewed and a fresh bounded branch is
opened for coding.

---

## Objective

Consume already-produced `meeting_context_v1` and `relationship_context_v1`
artifacts, propose a structured follow-up plan through the Follow-Up Planning
Agent, evaluate that proposal under the deterministic policy gate, and emit a
reviewable `meeting_follow_up_packet_v1` with zero external effects.

---

## Proposed architecture

```text
meeting_context_v1
  + relationship_context_v1
  -> Follow-Up Planning Agent
  -> structured follow-up proposal
  -> deterministic policy gate
  -> reviewable meeting_follow_up_packet_v1
  -> STOP
```

Reuse:

- Unit 1 Meeting Context Agent / `meeting_context_v1`
- Unit 2 Relationship Context Agent / `relationship_context_v1`
- Unit 2 Google ADK package runtime (`google-adk` Runner / SequentialAgent /
  session primitives; no local fallback)

---

## Authority boundary

| Actor | Authority |
| --- | --- |
| Follow-Up Planning Agent | **Proposes** facts, next steps, and optional stage-change intent only |
| Deterministic policy gate | **Evaluates and authorizes** mutation intent; remains sole authorization surface |
| Agent must not | Bypass policy, self-authorize CRM mutation, invoke live GHL, or write CRM |

Authority rule: agents propose; deterministic policy and workflow state decide.

---

## Allowed planning scope

- Follow-Up Planning Agent implementation
- proposal/output contract if needed (additive, schema-valid)
- reuse existing Google ADK package runtime
- reuse `meeting_context_v1`
- reuse `relationship_context_v1`
- deterministic policy evaluation / gate invocation
- synthetic fixtures only
- tests (agent + policy + fixture scenarios)
- sanitized proof artifacts under `proof/phase3/unit3/**`
- competition ledger / grant reconciliation after implementation green

---

## Blocked surfaces

- live GHL reads
- all GHL writes
- real customer data
- broad CRM search
- Firestore writes
- Cloud Run deployment
- IAM mutation
- Secret Manager mutation
- raw REST
- L3A runtime promotion
- deterministic-policy bypass
- production activation

---

## Required proof markers

```text
FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED=YES
MEETING_CONTEXT_REUSED=YES
RELATIONSHIP_CONTEXT_REUSED=YES
GOOGLE_ADK_RUNTIME_REUSED=YES
FOLLOW_UP_PROPOSAL_OUTPUT=VALID
DETERMINISTIC_POLICY_GATE_INVOKED=YES
DETERMINISTIC_POLICY_BYPASS=NO
EXTERNAL_EFFECTS=0
```

Also preserve inherited posture:

```text
GHL_LIVE_CALLS=0
GHL_WRITES=0
REAL_CUSTOMER_DATA=0
L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED
FIRESTORE_WRITES=0
DEPLOYMENT=NO
```

---

## Required scenario proof

| Scenario | Required result |
| --- | --- |
| `SUCCESS` | **PASS** |
| `AMBIGUOUS_CONTACT` | **PASS** |
| `AMBIGUOUS_OPPORTUNITY` | **PASS** |
| `NO_OPPORTUNITY` | **PASS** |
| `STAGE_CHANGE_DENIED` | **PASS** |
| `INSUFFICIENT_CONTEXT` | **PASS** |

Fail-closed expectations:

- Ambiguous contact/opportunity → no CRM mutation intent authorized; needs-review packet
- Stage change denied by policy → proposal may exist; mutation not authorized
- Insufficient context → no fabricated CRM facts; needs-review or no-op proposal

---

## Suggested deliverables (implementation unit; not started)

- `src/agents/follow_up_planning/**` (or equivalent bounded module)
- optional additive proposal/packet contract under `contracts/` if required for schema validity
- fixture packages covering the six scenarios above (synthetic only)
- tests under `tests/agents/` (+ policy acceptance as needed)
- `proof/phase3/unit3/proof-return.yaml` + unit closeout after green CI
- grant/ledger reconciliation on the Unit 3 branch only after tests green

---

## Explicit non-goals for Unit 3

- Live CRM verification loops
- Firestore audit writer (NW-005)
- MG Guide card production experience (NW-006)
- Cloud Run deployment (NW-007)
- Broad acceptance-demo expansion beyond the Unit 3 scenario set

---

## Entry criteria

1. Unit 2 durable closeout merged or accepted (`PHASE3_UNIT2_STATUS=MERGED_COMPLETE`).
2. This packet reviewed.
3. Fresh branch opened from current public `main` (do not reuse Unit 2 branch).
4. Exact-path staging only; no `git add .`.

## Exit criteria

1. All required proof markers true.
2. All required scenarios PASS.
3. `EXTERNAL_EFFECTS=0`.
4. Public CI green on the Unit 3 PR head.
5. Stop before live GHL / deployment / policy-authority expansion.

---

## STOP (this reconciliation step)

Unit 3 is **planned only**. No Follow-Up Planning Agent code is authorized by
this closeout commit alone beyond preparing this packet.

`STOP_CODE=PHASE3_UNIT2_CLOSED_UNIT3_PLAN_READY_FOR_REVIEW`
