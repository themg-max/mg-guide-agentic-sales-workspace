# NW-008 Tranche D — D2 (AT-8) Execution Packet

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Tranche | D |
| Subunit | D2 / AT-8 |
| Purpose | `HISTORICAL_AT8_WRITE_ATTEMPT_CAP_OFFLINE_ACCEPTANCE` |
| Planning branch | `feat/nw008-tranche-d-d2-at8` |
| Base SHA | `dcb5c94e79bf0dfc78c7c9e75c0d8f410f2b6a93` (PR #48 merge = `origin/main` at planning start) |
| Historical criterion source | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Tranche D plan reference | [`nw-008-tranche-d-implementation-packet.md`](./nw-008-tranche-d-implementation-packet.md) |
| D1 closeout reference | [`nw-008-tranche-d-d1-governance-closeout.md`](./nw-008-tranche-d-d1-governance-closeout.md) |
| Cap source | [`contracts/workflow_states.yaml`](../../contracts/workflow_states.yaml) `invariants` |
| Planning posture | **PLANNING_ONLY=YES** — no application/runtime/test/policy/contract mutation in this pass |

```text
NW008_TRANCHE_D_STATUS=D1_CLOSED_D2_PLANNED_NOT_IMPLEMENTED
D1=AT-9
D2=AT-8
D2_REQUIRES_D1_GREEN=YES
D1_STATUS=CLOSED
D2_IMPLEMENTATION_STARTED=NO

PLANNING_ONLY=YES
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
TESTS_CHANGED=NO
CONTRACTS_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
POLICY_NUMERIC_CAP_CHANGE=NO
TOOL_MANIFEST_CHANGED=NO
AUDIT_SCHEMA_CHANGED=NO
MEETING_FOLLOW_UP_PACKET_SCHEMA_CHANGE=NO

GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0

NW013_EXECUTED=NO
NW005_STAGE_B_ACTIVATED=NO
GOOGLE_WORKSPACE_RUNTIME=NO
DEPLOYMENT=NO
```

---

## 1. D1 inherited truth (required gate)

```text
PR48_STATUS=MERGED_COMPLETE
PR48_MERGE_SHA=dcb5c94e79bf0dfc78c7c9e75c0d8f410f2b6a93
PR48_MERGE_IS_ANCESTOR_OF_ORIGIN_MAIN=YES

D1_AT9_STATUS=HISTORICAL_COMPLETE
D1_RUNTIME_BEHAVIOR=GREEN
D1_PROOF_INTEGRITY=GREEN
D1_GOVERNANCE_CLOSEOUT=COMPLETE
D1_GATE_FOR_D2=TECHNICALLY_OPEN
D1_HUMAN_REVIEW_REQUIRED_BEFORE_D2=SATISFIED
D1_STATUS=CLOSED

A1R2=ab17da29fce5c134eb865e07c30f208e8d61b394
P1R2=64daa993b1e7a37455e0c4d41f62e55168eedc3b
```

D2 planning is allowed only because D1/AT-9 is closed green on main via PR #48.
This packet does not reopen D1, mutate D1 proof, or alter D1 manifest-gate semantics.

---

## 2. Frozen AT-8 acceptance criterion

Source: `docs/MEETING_FOLLOW_UP_FOUNDATION.md` §17 — preserved verbatim:

> **AT-8** — Per-run mutation caps — **Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice.**

```text
AT8_CRITERION_FROZEN=YES
AT8_CAP_SEMANTIC=WRITE_ATTEMPT_CAP
AT8_INTENT_CAP_IS_NOT_SUBSTITUTE=YES
AT8_LIVE_CRM_WRITE_REQUIRED_ON_ATTEMPT_1=NO
AT8_TRANSPORT_REQUIRED=NO
```

What AT-8 does **not** require:
- live GHL/CRM transport on attempt #1
- agent self-restraint or prompt-only refusal
- harness-simulated refusal without OL3 policy ownership
- intent-cardinality (`bound_intents`) alone as a substitute for write-attempt caps

---

## 3. Required authority model

```text
CAP_SOURCE=contracts/workflow_states.yaml
CAP_NODE=invariants
CAP_FIELDS=max_note_writes_per_run,max_stage_writes_per_run
LEDGER_STATE_OWNER=WRITE_ATTEMPT_LEDGER
ENFORCEMENT_DECISION_OWNER=OL3_ORCHESTRATION_POLICY
RUNNER_AUTHORITY=ORCHESTRATION_ONLY
AGENT_CAP_AUTHORITY=NO
HARNESS_CAP_AUTHORITY=NO
OFFLINE_ADAPTER_AUTHORITY=SECONDARY_FAIL_CLOSED_ONLY
```

The ledger owns only per-run note and stage counter state. It must not decide
whether an attempt is permitted or refused. OL3 orchestration policy owns every
`PERMIT` / `REFUSE` decision, and the runner invokes that policy decision before
any transport path. A ledger-only refusal cannot be labeled as policy authority.

Contractual numeric caps (unchanged; no policy numeric change authorized):

```yaml
invariants:
  - max_note_writes_per_run: 1
  - max_stage_writes_per_run: 1
  - max_note_intents_per_run: 1
  - max_stage_intents_per_run: 1
```

Contract-loading repair is in scope for implementation later:
`StateMachine` currently hard-codes intent limits and does not load write caps from the contract.
Loading `max_note_writes_per_run` / `max_stage_writes_per_run` from
`contracts/workflow_states.yaml` is classified as **`CONTRACT_LOADING_REPAIR`**, not
new policy semantics, because contracted values and meanings remain `1` / `1`.

---

## 4. Frozen D2 semantics

```text
LEDGER_SCOPE=RUN_SCOPED
LEDGER_KEY=run_id
LEDGER_LIFETIME=ONE_WORKFLOW_RUN_EXECUTION
LEDGER_PERSISTENCE=NONE
PROCESS_GLOBAL_LEDGER=NO
FIRESTORE_LEDGER=NO
RUN_ID_IS_SCOPE_IDENTITY=YES
NOTE_COUNTER=INDEPENDENT
STAGE_COUNTER=INDEPENDENT
CONTRACTUAL_MAX_NOTE_WRITES_PER_RUN=1
CONTRACTUAL_MAX_STAGE_WRITES_PER_RUN=1

ATTEMPT_INCREMENTS_AT=POLICY_ADMISSION
ATTEMPT_INCREMENTS_BEFORE_TRANSPORT=YES
LEDGER_COUNTS_ADMITTED_ATTEMPTS_ONLY=YES
REFUSED_ATTEMPT_INCREMENTS_LEDGER=NO

ATTEMPT_1_ADMITTED_LOCALLY=YES
ATTEMPT_2_REFUSED_DETERMINISTICALLY=YES
NEW_RUN_ID_RECEIVES_FRESH_LEDGER=YES

NO_LIVE_TRANSPORT_IN_D2=YES
TRANSPORT_ATTEMPTED=false
CANONICAL_PACKET_MUTATION_ATTEMPTED=false
CANONICAL_PACKET_MUTATION_VERIFIED=false
EXTERNAL_EFFECTS=0
```

### 4.1 Admission / refusal arithmetic (per counter)

```text
# Attempt #1 (note or stage)
ADMITTED_WRITE_ATTEMPTS_BEFORE_REQUEST=0
REQUESTED_ATTEMPT_ORDINAL=1
MAX_WRITES_PER_RUN=1
CAP_CHECK=PERMIT
ADMITTED_WRITE_ATTEMPTS_AFTER_REQUEST=1
TRANSPORT_ATTEMPTED=false

# Attempt #2 same run / same counter
ADMITTED_WRITE_ATTEMPTS_BEFORE_REQUEST=1
REQUESTED_ATTEMPT_ORDINAL=2
MAX_WRITES_PER_RUN=1
CAP_CHECK=REFUSE   # BEFORE >= MAX
ADMITTED_WRITE_ATTEMPTS_AFTER_REQUEST=1
TRANSPORT_ATTEMPTED=false
REFUSAL_OWNER=OL3_ORCHESTRATION_POLICY
```

### 4.2 Target data flow

```text
proposal requests note|stage write attempt
        ↓
runner calls OL3 orchestration policy before any transport
        ↓
OL3 policy reads / updates run-scoped write-attempt ledger state
        ↓
attempt #1 admitted locally (ledger AFTER=1); no transport
        ↓
same run_id requests attempt #2 for same counter
        ↓
ledger refuses (BEFORE=1 >= MAX=1); no transport
        ↓
refusal attributed to OL3 policy, not agent choice / harness
        ↓
new run_id → fresh ledger → attempt #1 admitted again
```

---

## 5. Current repo surfaces (planning inspection)

| Component | Path / symbol | Current state | D2 role |
| --- | --- | --- | --- |
| Workflow contract | `contracts/workflow_states.yaml` `invariants` | Caps declared (`1`/`1`) | **CAP_SOURCE** (read-only) |
| State machine | `src/orchestration/state_machine.py` | Hard-codes `max_note_intents=1`, `max_stage_intents=1`; write caps not loaded | Contract-loading repair target |
| Policy | `src/orchestration/policy.py` `bound_intents()` | Intent-cardinality only | Planned OL3 decision owner for write-attempt `PERMIT` / `REFUSE` |
| Runner | `src/orchestration/runner.py` | Orchestrates Phase 1 offline run | Calls policy before any transport; does not own cap decisions |
| Attempt ledger | `src/orchestration/attempt_ledger.py` | **Absent** | Planned D2 surface |
| D1 gate | `src/orchestration/manifest_gate.py` | Present (closed D1) | **Out of scope / do not mutate** |
| D1 proof | `proof/nw008/tranche-d/at-09-*`, closeout | Present | **Do not mutate** |
| Prior AT-8 partial | `proof/nw008/at-08/` | `PARTIAL_SUPPORTING_PROOF`; gap = authoritative second-attempt refusal trace | Superseded by D2 durable proof when implemented |

---

## 6. Required proof obligations (frozen)

| ID | Obligation | Target verification |
| --- | --- | --- |
| **TD2-01** | Contract-derived note cap | `max_note_writes_per_run` loaded from `contracts/workflow_states.yaml` invariants |
| **TD2-02** | Contract-derived stage cap | `max_stage_writes_per_run` loaded from same contract |
| **TD2-03** | Note attempt #1 admitted | Same `run_id`; note counter BEFORE=0 → PERMIT → AFTER=1; no transport |
| **TD2-04** | Note attempt #2 refused by OL3 policy | Same `run_id`; note refused; `REFUSAL_OWNER=OL3_ORCHESTRATION_POLICY` |
| **TD2-05** | Stage attempt #1 admitted | Same or dedicated run; stage counter BEFORE=0 → PERMIT → AFTER=1; no transport |
| **TD2-06** | Stage attempt #2 refused by OL3 policy | Same `run_id` as stage #1; stage refused by OL3 policy |
| **TD2-07** | Independent counters | Note exhaustion does not refuse stage #1 (and vice versa) |
| **TD2-08** | New run resets effective ledger | Distinct `run_id` admits attempt #1 again for each counter |
| **TD2-09** | Refusal before transport | No transport / executor call on refused attempt (and none required on admitted offline attempt) |
| **TD2-10** | Deterministic replay | Identical inputs → identical admission/refusal decisions |
| **TD2-11** | Zero GHL / Firestore / external effects | `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0` |
| **TD2-12** | Durable proof bound to exact implementation SHA | Proof artifacts record `IMPLEMENTATION_SUBJECT_SHA=<A2>`; SHA is ancestor of proof commit |

```text
PROOF_STATUS_SOURCE=COMPUTED_RUNTIME_EVIDENCE
HANDWRITTEN_CONTROL_PASS_FORBIDDEN=YES
VALIDATOR_SELF_ASSERTION_FORBIDDEN=YES
FINAL_ARTIFACT_REPLAY_HASH_COMPARISON=REQUIRED
```

TD2 and NC-D2 results must be computed from executed controls. A handwritten
`PASS`, including one merely repeated by the validator without independently
computed runtime evidence, is invalid. The generated final D2 proof artifacts
must be deterministically replayed and compared by hash with the final committed
artifacts; mismatch fails validation.

---

## 7. Required negative controls (frozen)

| ID | Control | Expected |
| --- | --- | --- |
| **NC-D2-1** | Harness cannot override caps | Harness/test double cannot force admit attempt #2 |
| **NC-D2-2** | Note first attempt allowed | Note attempt #1 admitted |
| **NC-D2-3** | Note second attempt refused | Note attempt #2 refused by OL3 policy |
| **NC-D2-4** | Stage first attempt allowed | Stage attempt #1 admitted |
| **NC-D2-5** | Stage second attempt refused | Stage attempt #2 refused by OL3 policy |
| **NC-D2-6** | Counters independent | Note and stage ledgers do not share exhaustion |
| **NC-D2-7** | New `run_id` resets | Fresh ledger admits attempt #1 |
| **NC-D2-8** | Nonzero effect forces validator FAIL | Any nonzero GHL/Firestore/external effect → proof validator FAIL |
| **NC-D2-9** | Contract authority negative | Temporary test contract with note cap `2`: attempts #1/#2 permit and #3 refuses; production contract remains unchanged |
| **NC-D2-10** | Malformed or missing write cap fails closed | Missing, malformed, or non-valid write cap refuses admission and fails proof validation |

---

## 8. Planned implementation surfaces (future only)

```text
PLANNED_ALLOWED_IMPLEMENTATION_FILES:
  src/orchestration/attempt_ledger.py          # run-scoped note/stage write-attempt ledger
  src/orchestration/state_machine.py           # CONTRACT_LOADING_REPAIR for write caps
  src/orchestration/policy.py                  # OL3 owns PERMIT / REFUSE decisions
  src/orchestration/runner.py                  # calls policy before any transport
  src/orchestration/nw008_tranche_d.py         # D2 offline harness / proof emitter (additive)
  tests/test_write_attempt_ledger.py           # unit + NC-D2-1..10
  tests/test_nw008_tranche_d_acceptance.py     # additive D2 acceptance / proof checks
  proof/nw008/tranche-d/d2-at8/at-08-run.json
  proof/nw008/tranche-d/d2-at8/at-08-attempt-trace.json
  proof/nw008/tranche-d/d2-at8/proof-manifest.md
  proof/nw008/tranche-d/d2-at8/proof-return.yaml
  proof/nw008/nw-008-tranche-d-d2-*-closeout*  # future governance closeout only

PLANNED_BLOCKED_FILES_AND_SURFACES:
  contracts/**                                 # no semantic or numeric cap changes
  contracts/ghl_tool_manifest.yaml             # D1 surface — no change
  src/orchestration/manifest_gate.py           # D1 surface — no change
  proof/nw008/tranche-c/**                     # immutable
  proof/nw008/tranche-d/at-09-run.json         # D1 immutable
  proof/nw008/tranche-d/at-09-workflow-run-audit.json # D1 immutable
  proof/nw008/tranche-d/proof-manifest.md      # D1 immutable
  proof/nw008/tranche-d/proof-return.yaml      # D1 immutable
  proof/nw008/nw-008-tranche-d-d1-governance-closeout.md # D1 immutable
  deploy/**
  infra/**
  .github/workflows/**
  IAM / secrets / cloud
  GHL live calls/writes
  Firestore Stage B
  production deployment
  meeting_follow_up_packet / workflow_run_audit schema changes
```

### 8.1 Commit discipline (future implementation)

```text
A2 = stable D2 implementation subject commit
P2 = D2 proof commit binding IMPLEMENTATION_SUBJECT_SHA=A2
```

Do not self-bind proof to the proof commit. Do not amend D1 subjects A1R2/P1R2.

---

## 9. Validation plan (future implementation)

1. `pytest tests/test_write_attempt_ledger.py` — TD2-01..12 unit coverage + NC-D2-1..10
2. `pytest tests/test_nw008_tranche_d_acceptance.py` — D2 acceptance + durable proof assertions
3. `pytest` — full suite green; D1 tests remain green (no D1 regression)
4. Deterministic D2 proof replay + computed-evidence validator PASS
5. Compare deterministic-replay hashes to final committed D2 artifacts; any mismatch FAILS
6. Effect counters all zero
7. Exact-head Phase 1 Deterministic CI PASS
8. Capture byte-identifying Git object IDs before targeted D2 tests, full
   `pytest`, and D2 proof generation; after each operation, require exact
   equality for:
   - `proof/nw008/tranche-d/at-09-run.json`
   - `proof/nw008/tranche-d/at-09-workflow-run-audit.json`
   - `proof/nw008/tranche-d/proof-manifest.md`
   - `proof/nw008/tranche-d/proof-return.yaml`
   - `proof/nw008/nw-008-tranche-d-d1-governance-closeout.md`
9. Confirm `git rev-parse HEAD:proof/nw008/tranche-c` remains
   `33257929a2b16cf005fd5a95a914e2dc7389c71a` after each operation.

```text
D1_PROOF_IMMUTABLE=YES
TRANCHE_C_PROOF_IMMUTABLE=YES
IMMUTABILITY_CHECK_METHOD=EXACT_GIT_OBJECT_ID_COMPARISON
IMMUTABILITY_CHECK_TIMES=AFTER_TARGETED_D2_TESTS,AFTER_FULL_PYTEST,AFTER_D2_PROOF_GENERATION
```

---

## 10. Stop conditions

STOP immediately and return for architecture review if implementation would require any of:

1. Live GHL network access or CRM mutation authorization
2. Firestore Stage B online writes
3. Schema changes to packet or audit contracts
4. Numeric policy cap changes in `contracts/workflow_states.yaml`
5. D1 manifest-gate semantic changes
6. Mutation of Tranche C proof or any frozen D1 proof artifact
7. Attribution of second-attempt refusal to agent choice or harness authority
8. Non-zero external effects

---

## 11. Machine-readable planning return

```text
D2_BRANCH=feat/nw008-tranche-d-d2-at8
D2_BASE_SHA=dcb5c94e79bf0dfc78c7c9e75c0d8f410f2b6a93
D2_PACKET=proof/nw008/nw-008-tranche-d-d2-at8-execution-packet.md

PR48_STATUS=MERGED_COMPLETE
PR48_MERGE_SHA=dcb5c94e79bf0dfc78c7c9e75c0d8f410f2b6a93
D1_AT9_STATUS=HISTORICAL_COMPLETE
D1_RUNTIME_BEHAVIOR=GREEN
D1_PROOF_INTEGRITY=GREEN
D1_STATUS=CLOSED

AT8_CRITERION_FROZEN=YES
AT8_CAP_SEMANTIC=WRITE_ATTEMPT_CAP
CAP_SOURCE=contracts/workflow_states.yaml
LEDGER_STATE_OWNER=WRITE_ATTEMPT_LEDGER
ENFORCEMENT_DECISION_OWNER=OL3_ORCHESTRATION_POLICY
RUNNER_AUTHORITY=ORCHESTRATION_ONLY
AGENT_CAP_AUTHORITY=NO
HARNESS_CAP_AUTHORITY=NO

TD2_01..TD2_12=FROZEN
NC_D2_01..NC_D2_10=FROZEN
D2_PROOF_NAMESPACE=proof/nw008/tranche-d/d2-at8
D1_PROOF_IMMUTABLE=YES
TRANCHE_C_PROOF_IMMUTABLE=YES

PLANNING_ONLY=YES
D2_IMPLEMENTATION_STARTED=NO
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
TESTS_CHANGED=NO
CONTRACTS_CHANGED=NO
POLICY_NUMERIC_CAP_CHANGE=NO
EXTERNAL_EFFECTS=0
WORKTREE_CLEAN=YES

STOP_CODE=NW008_D2_AT8_PLANNING_REPAIR_READY_FOR_IMPLEMENTATION_REVIEW
```

## STOP

```text
STOP_CODE=NW008_D2_AT8_PLANNING_REPAIR_READY_FOR_IMPLEMENTATION_REVIEW
```

This lane stops before D2 implementation. Implementation requires a separate authorized execution pass against this frozen packet.
