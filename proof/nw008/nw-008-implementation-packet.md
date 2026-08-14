# NW-008 Implementation Packet — Acceptance + Demo Proof

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Title | Acceptance tests AT-1…AT-10 + demo proof |
| Packet status | **TRANCHE_A_EXECUTION** |
| Implementation in this unit | **OFFLINE_SYNTHETIC_ACCEPTANCE_EVIDENCE (Tranche A only)** |
| Runtime / cloud / CRM live changes in this unit | **NONE** |
| Ledger status target after this unit | **IN_PROGRESS** (Tranche A evidence package; not full NW-008 closeout) |
| Readiness matrix | [`nw-008-readiness-matrix.md`](./nw-008-readiness-matrix.md) |
| Historical AT source | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17–§18, §20 |
| Data rule | Synthetic / authorized test identities only — **no production or real customer data** |
| Tranche A proof | [`tranche-a/proof-manifest.md`](./tranche-a/proof-manifest.md), [`tranche-a/proof-return.yaml`](./tranche-a/proof-return.yaml) |

## Tranche A execution freeze

```text
NW008_EXECUTION_UNIT=TRANCHE_A
NW008_EXECUTION_MODE=OFFLINE_SYNTHETIC_ACCEPTANCE_EVIDENCE

COMPLETION_CANDIDATES:
AT-2
AT-4
AT-5

SUPPORTING_PARTIAL_PROOFS:
AT-8
AT-9

BLOCKED_NOT_EXECUTED:
AT-1
AT-3
AT-6
AT-7

DEFERRED_NOT_EXECUTED:
AT-10
```

Historical AT definitions are **unchanged** (foundation §17 verbatim). This unit
records offline/synthetic evidence against those definitions. It does **not**
silently rewrite the acceptance bar.

## Authority (Tranche A)

```text
GHL_LIVE_CALLS_AUTHORIZED=NO
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
NW013_EXECUTION_IN_SCOPE=NO
DEPLOYMENT_AUTHORIZED=NO
REAL_CUSTOMER_DATA=FORBIDDEN
RAW_REST=FORBIDDEN
NW005_STAGE_B_ACTIVATED=NO
```

## Source-authority rule (mandatory separation)

Keep separate:

1. **AUTHORITATIVE_WORKFLOW_REASON** — WorkflowRunner / contracts / deterministic policy
2. **DECISION_CARD_PRESENTATION** — NW-007 decision-card mapper/renderers
3. **HISTORICAL_AT_COMPLETION** — unchanged foundation §17 clauses only

Do **not** expand or change NW-007 decision-card reason semantics.

| AT | Historical authoritative reason | Card presentation note |
| --- | --- | --- |
| AT-4 | `CONTACT_NOT_FOUND` | Must be proven from workflow/policy/packet source. If the NW-007 card does not expose a named scenario, preserve fail-closed presentation. Do **not** modify the decision-card mapper to invent presentation semantics. |
| AT-5 | `LOW_EXTRACTION_CONFIDENCE` | Same rule as AT-4. |

## Upstream truth bindings

```text
NW006_STATUS=MERGED_COMPLETE
NW006_PR=15
NW006_FINAL_REVIEWED_HEAD=c7d25b447db0a961c17ae26e326ada230b7e4627
NW006_EXACT_HEAD_CI_RUN=31630399411
NW006_EXACT_HEAD_CI_RESULT=SUCCESS
NW006_MERGE_SHA=e22eb861442a37be0797d6d7aec8bb17001fb7a3
NW006_MERGED_AT=2026-08-12T19:12:33Z
NW007_STATUS=MERGED_COMPLETE
NW007_PR=37
NW007_FINAL_REVIEWED_HEAD=22a3b0b3c20373100ca0158cda7a74b4fbc1fb76
NW007_MERGE_SHA=f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6
NW007_MERGED_AT=2026-08-14T09:35:35Z
NW007_DECISION_CARD_STATUS=MERGED_COMPLETE
NW007_STAGE_B2_DEPLOYMENT_EVIDENCE=AVAILABLE
NW007_DEPLOYMENT_AUTHORIZATION=NO
EXTERNAL_EFFECTS=0

NW005_STATUS=PLANNED
NW005_STAGE_B_STATUS=PLANNED_NOT_AUTHORIZED
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
ISOLATED_GHL_TEST_LOCATION=NO
CANONICAL_GHL_LOCATION_IS_TEST_ENV=NO
RAW_REST=FORBIDDEN
DETERMINISTIC_POLICY=SOLE_CONSEQUENTIAL_ACTION_AUTHORIZATION_SURFACE
```

## Bounded dependency sequence (unchanged)

```text
1) NW-006 closeout                          [MERGED_COMPLETE]
        ↓
2) optional NW-013 bounded synthetic        [AUTHORIZED_NOT_EXECUTED today]
   live-read execution
        ↓
3) NW-005 Firestore audit                   [PLANNED / Stage B NOT_AUTHORIZED]
        ↓
4) NW-007 bounded Cloud Run / decision card [MERGED_COMPLETE]
        ↓
5) NW-008 acceptance / demo proof           [TRANCHE_A offline evidence in progress]
        ↓
6) CRM mutation only under a future         [NOT AUTHORIZED NOW]
   separately authorized safe-environment
   lane
```

## Shared evidence harness

- Module: `src/orchestration/nw008_harness.py`
- Single deterministic harness; **no** parallel orchestration engine
- Reuses:
  - canonical synthetic fixtures
  - `WorkflowRunner` / deterministic policy surfaces
  - packet contracts
  - NW-007 decision-card mapper/renderers + NW-006 card mapper
  - offline GHL adapter / tool-manifest surfaces
- Common evidence result fields:

```text
AT_ID
HISTORICAL_EXPECTED_OUTCOME
EVIDENCE_CLASS
SOURCE_FIXTURE
RUN_ID
INPUT_HASH
ACTUAL_WORKFLOW_STATUS
AUTHORITATIVE_REASON_CODES
CARD_POLICY_STATE
CARD_REASON_CODE
CARD_NEXT_ACTION
HISTORICAL_CLAUSE_COVERAGE
GHL_LIVE_CALLS
GHL_READS
GHL_WRITES
FIRESTORE_WRITES
EXTERNAL_EFFECTS
REAL_CUSTOMER_DATA
HISTORICAL_AT_COMPLETE
REMAINING_GAP
COMMIT_SHA
TEST_RESULT
```

All Tranche A results **must** report:

```text
GHL_LIVE_CALLS=0
GHL_READS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0
```

Any non-zero external effect → **FAIL CLOSED and STOP**.

## Historical acceptance criteria (verbatim from foundation §17)

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

## Tranche A AT plan

### AT-2 — COMPLETION_CANDIDATE

- Fixture: `fixtures/transcript-ambiguous-contact.expected.json`
- Required clauses: `blocked`, `AMBIGUOUS_CONTACT`, `0 CRM writes`, MG Guide blocked / State-2-equivalent decision card
- Evidence: `proof/nw008/at-02/`

### AT-4 — COMPLETION_CANDIDATE

- Fixture: `fixtures/transcript-contact-not-found.expected.json` (synthetic only; no live CRM lookup)
- Required clauses: `CONTACT_NOT_FOUND`, `blocked`, `0 writes`
- Authoritative reason from workflow/policy — not invented card semantics
- Evidence: `proof/nw008/at-04/`

### AT-5 — COMPLETION_CANDIDATE

- Fixture: `fixtures/transcript-insufficient-context.expected.json`
- Required clauses: extraction below threshold, `LOW_EXTRACTION_CONFIDENCE`, `blocked`, `0 writes`
- Authoritative reason from workflow/policy — do not alter policy to force PASS
- Evidence: `proof/nw008/at-05/`

### AT-8 — PARTIAL_SUPPORTING_PROOF

- `HISTORICAL_AT_COMPLETE=NO`
- Prove deterministic policy-cap behavior only (no live mutation)
- Remaining gap: active mutation-execution trace showing second attempt refusal by policy
- Evidence: `proof/nw008/at-08/`

### AT-9 — PARTIAL_SUPPORTING_PROOF

- `HISTORICAL_AT_COMPLETE=NO`
- Prove tool-manifest refusal offline (no live GHL invocation)
- Remaining gap: durable audit warning under authorized audit sink
- NW-005 Stage B must **not** be activated implicitly
- Evidence: `proof/nw008/at-09/`

## Proof artifact layout

```text
proof/nw008/tranche-a/proof-manifest.md
proof/nw008/tranche-a/proof-return.yaml
proof/nw008/at-02/
proof/nw008/at-04/
proof/nw008/at-05/
proof/nw008/at-08/
proof/nw008/at-09/
```

Use hashes/references instead of copying large raw fixture contents.

## Non-goals (still enforced)

- Do not execute AT-1 / AT-3 / AT-6 / AT-7 write-path historical clauses.
- Do not claim AT-10 without NW-005 Stage B authority.
- Do not execute NW-013.
- Do not deploy.
- Do not authorize CRM mutation.
- Do not revise foundation acceptance text.
- Do not modify NW-007 decision-card mapper solely to make AT-4/AT-5 look complete.
- Do not activate NW-005 Stage B.

## Exit criteria for full NW-008 closeout (preview; not this tranche)

NW-008 may move beyond partial tranche evidence only when:

1. Each executed AT has evidence against the **unchanged** historical expected outcome.
2. Unexecuted ATs are explicitly labeled BLOCKED/DEFERRED with authority citations — not hidden.
3. Effect counters are recorded and truthful.
4. Demo proof either runs within authorized environment bounds or records a governed STOP.
5. Ledger/collab log/proof return agree on SHAs, grants, and non-claims.

## STOP (Tranche A implementation unit)

```text
PACKET_MODE=TRANCHE_A_EXECUTION
NW008_EXECUTION_UNIT=TRANCHE_A
NW008_EXECUTION_MODE=OFFLINE_SYNTHETIC_ACCEPTANCE_EVIDENCE
NW005_RUNTIME_CHANGES=0
NW007_POLICY_SEMANTICS_CHANGE=NO
CRM_MUTATION_CHANGES=0
DEPLOYMENT_CHANGES=0
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0
STOP_CODE=NW008_TRANCHE_A_ACCEPTANCE_EVIDENCE_READY_FOR_PR_REVIEW
```
