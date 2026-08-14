# NW-008 Tranche D Implementation Packet

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Execution unit | TRANCHE_D |
| Purpose | HISTORICAL_AT8_AT9_OFFLINE_GOVERNANCE_COMPLETION |
| Planning branch | `chore/nw008-tranche-d-implementation-plan` |
| Base SHA | `4af506a90c9b6c6eaf75f6fdb3235ad94a1af5a9` (PR #46 merge = `origin/main` at planning start) |
| PR #46 head SHA | `ec6ac63d5b3971d500be2f6fbfd86f249966b126` |
| PR #46 merge SHA | `4af506a90c9b6c6eaf75f6fdb3235ad94a1af5a9` |
| PR #46 merged at | `2026-08-14T17:00:10Z` |
| PR46_MERGE_IS_ANCESTOR_OF_ORIGIN_MAIN | `YES` |
| Historical criteria source | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Feasibility reference | [`nw-008-tranche-d-at8-at9-feasibility-packet.md`](./nw-008-tranche-d-at8-at9-feasibility-packet.md) |
| Companion readiness matrix | [`nw-008-readiness-matrix.md`](./nw-008-readiness-matrix.md) |
| Planning posture | **PLANNING_ONLY=YES** — no application/runtime/test/policy/manifest/schema mutation in this pass |

```text
NW008_TRANCHE_D_STATUS=PLANNED_NOT_IMPLEMENTED
D1=AT-9
D2=AT-8
D2_REQUIRES_D1_GREEN=YES

PLANNING_ONLY=YES
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
TESTS_CHANGED=NO
CONTRACTS_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
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

AT2_STATUS=HISTORICAL_COMPLETE
AT4_STATUS=HISTORICAL_COMPLETE
AT5_STATUS=HISTORICAL_COMPLETE
AT8_STATUS=PARTIAL
AT9_STATUS=PARTIAL
NW008_OVERALL_STATUS=IN_PROGRESS
```

---

## 1. Governance / merge truth

### 1.1 Prior PR merge lineage

The durable state entering Tranche D planning rests on PR #46 (merged into `main`):

```text
PR46_STATUS=MERGED_COMPLETE
PR46_HEAD_SHA=ec6ac63d5b3971d500be2f6fbfd86f249966b126
PR46_MERGE_SHA=4af506a90c9b6c6eaf75f6fdb3235ad94a1af5a9
PR46_MERGED_AT=2026-08-14T17:00:10Z
PR46_MERGE_IS_ANCESTOR_OF_ORIGIN_MAIN=YES
```

### 1.2 Durable upstream work item state

- **Tranche A (PR #40)**: `MERGED_COMPLETE` — deterministic acceptance evidence substrate.
- **Tranche B (PR #42)**: `MERGED_COMPLETE` — longitudinal agent fleet transcript replay.
- **Tranche C (PR #44)**: `MERGED_COMPLETE` — failure-path transcript source envelope replay.
- **Tranche C Closeout (PR #45)**: `MERGED_COMPLETE` — historical AT-2, AT-4, AT-5 certified `HISTORICAL_COMPLETE`.
- **Tranche D Feasibility (PR #46)**: `MERGED_COMPLETE` — established offline executability for AT-8 and AT-9 without new authorization.

### 1.3 Feasibility results from PR #46

```text
AT8_FEASIBILITY=OFFLINE_EXECUTABLE
AT9_FEASIBILITY=OFFLINE_EXECUTABLE
AT8_NEW_AUTHORIZATION_REQUIRED=NO
AT9_NEW_AUTHORIZATION_REQUIRED=NO
RECOMMENDED_SEQUENCE=D1=AT-9,D2=AT-8
D2_REQUIRES_D1_GREEN=YES
```

---

## 2. Historical acceptance criteria

Source: [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 — **preserved verbatim without revision**:

| # | Test | Authoritative expected outcome (verbatim §17) |
| --- | --- | --- |
| **AT-8** | Per-run mutation caps | **Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice.** |
| **AT-9** | Blocked tool invocation (e.g. contact create) | **Refused at tool-manifest layer; recorded in audit warnings.** |

Neither criterion is weakened or strengthened. Specifically:
- **AT-8** tests enforcement of the **write-attempt cap** by deterministic OL3 policy; it does not require a live CRM write on attempt #1.
- **AT-9** tests refusal at the **tool-manifest layer** and recording in **audit warnings**; it does not require live Firestore Stage B online writes.

---

## 3. Current repo surfaces

Targeted inspection of current repository surfaces identified the following existing symbols, contracts, and components:

| Component | Path / symbol | Current state | Role in Tranche D |
| --- | --- | --- | --- |
| **Tool manifest** | [`contracts/ghl_tool_manifest.yaml`](../../contracts/ghl_tool_manifest.yaml) `ghl_mcp.blocked_capability_classes` | Contains `contact_create`, `contact_delete`, `opportunity_create`, `email_send`, etc. | Declarative authority for blocked capability classes |
| **Workflow contract** | [`contracts/workflow_states.yaml`](../../contracts/workflow_states.yaml) `invariants` | Declares `max_note_writes_per_run: 1`, `max_stage_writes_per_run: 1`, `max_note_intents_per_run: 1`, `max_stage_intents_per_run: 1` | Contractual authority for numeric caps |
| **State machine** | [`src/orchestration/state_machine.py`](../../src/orchestration/state_machine.py) `StateMachine` | Loads thresholds; hard-codes `self.max_note_intents = 1`, `self.max_stage_intents = 1` | Contract loading repair: load contracted `max_note_writes` / `max_stage_writes` |
| **Policy evaluation** | [`src/orchestration/policy.py`](../../src/orchestration/policy.py) `evaluate_policy()`, `bound_intents()` | Decides intents; bounds intent cardinality | Admitted intent policy authority |
| **Workflow runner** | [`src/orchestration/runner.py`](../../src/orchestration/runner.py) `WorkflowRunner` | Orchestrates Phase 1 fixture execution, sets `mutations.*.attempted=False` | Hosts the deterministic runtime manifest gate (D1) and run-scoped write-attempt ledger (D2) |
| **Data models** | [`src/orchestration/models.py`](../../src/orchestration/models.py) `base_packet`, `empty_mutations` | Has `audit.warnings: []`, `mutations.*` | Canonical packet shape; preserves `audit.warnings` |
| **Secondary offline adapter** | [`src/integrations/ghl/read_adapter.py`](../../src/integrations/ghl/read_adapter.py) `OfflineGhlReadAdapter` | Denies mutations and unlisted operations | Fail-closed secondary defense; zero I/O |
| **Audit projector** | [`src/mg_guide/firestore_audit/project.py`](../../src/mg_guide/firestore_audit/project.py) `project_workflow_run_audit` | Copies `packet.audit.warnings` → `workflow_run_audit_v1.warnings` | NW-005 Stage A deterministic projection to durable audit artifact |
| **Memory audit sink** | [`src/mg_guide/firestore_audit/memory_store.py`](../../src/mg_guide/firestore_audit/memory_store.py) `MemoryAuditStore` | In-memory terminal store | Supporting runtime/test sink only (not durable proof) |
| **Existing harness** | [`src/orchestration/nw008_harness.py`](../../src/orchestration/nw008_harness.py) `Nw008EvidenceHarness` | Tranche A harness with simulated second bag and unprojected tool refusal | Replaced / augmented by dedicated Tranche D harness |

---

## 4. Tranche D scope and non-goals

### 4.1 Scope

Tranche D executes the remaining two offline-governed acceptance tests in a strict sequential subunit discipline:

1. **Subunit D1 (AT-9)**: Implement a runtime-owned tool-manifest gate that enforces `contracts/ghl_tool_manifest.yaml` blocked classes prior to any transport, records structured audit warnings in `packet.audit.warnings`, projects them to `workflow_run_audit_v1` via NW-005 Stage A, and generates durable proof under `proof/nw008/tranche-d/`.
2. **Subunit D2 (AT-8)**: Enforce a run-scoped write-attempt cap ledger derived from `contracts/workflow_states.yaml`, admitting attempt #1 (with zero external transport) and deterministically refusing attempt #2 at the OL3 orchestration policy boundary (not by agent choice).

### 4.2 Non-goals and strict boundaries

```text
NEW_AGENT=NO
POLICY_NUMERIC_CAP_CHANGE=NO
POLICY_SEMANTICS_CHANGE=NO
TOOL_MANIFEST_BLOCKED_CLASS_CHANGE=NO
TOOL_MANIFEST_SEMANTICS_CHANGE=NO
MEETING_FOLLOW_UP_PACKET_SCHEMA_CHANGE=NO
AUDIT_SCHEMA_CHANGE=NO

GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS=0

NW013_EXECUTED=NO
NW005_STAGE_B_ACTIVATED=NO
GOOGLE_WORKSPACE_RUNTIME=NO
FLEET_POLICY_CONTEXT_RUNTIME=NO

CLOUD_MUTATION=NONE
DEPLOYMENT=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO

AT1_STATUS=INCOMPLETE
AT3_STATUS=INCOMPLETE
AT6_STATUS=INCOMPLETE
AT7_STATUS=INCOMPLETE
AT8_STATUS=PARTIAL
AT9_STATUS=PARTIAL
AT10_STATUS=INCOMPLETE

NW008_OVERALL_STATUS=IN_PROGRESS
```

---

## 5. D1 — AT-9 architecture

### 5.1 Historical requirement

> Blocked tool invocation (e.g. contact create) is refused at tool-manifest layer and recorded in audit warnings.

### 5.2 Architecture and data flow

```text
requested operation (e.g. "create-contact")
        ↓
runtime operation classifier
        ↓
capability class (e.g. "contact_create")
        ↓
tool-manifest blocked-class decision (contracts/ghl_tool_manifest.yaml)
        ↓
refusal before adapter / network transport (REFUSAL_LAYER=TOOL_MANIFEST)
        ↓
packet audit warning (packet.audit.warnings: ["TOOL_MANIFEST_REFUSED:contact_create"])
        ↓
NW-005 Stage A projection (project_workflow_run_audit)
        ↓
schema validation (workflow_run_audit.schema.json)
        ↓
durable proof JSON (proof/nw008/tranche-d/at-09-workflow-run-audit.json)
```

### 5.3 Authority separation

```text
OPERATION_CLASSIFIER_OWNER=RUNTIME_MANIFEST_GATE
BLOCK_DECISION_AUTHORITY=GHL_TOOL_MANIFEST
HARNESS_CLASSIFICATION_AUTHORITY=NO
ADAPTER_BLOCK_AUTHORITY=SECONDARY_FAIL_CLOSED_ONLY
```

- **Runtime manifest gate** owns mapping: `create-contact` → `contact_create`.
- **Tool manifest** (`contracts/ghl_tool_manifest.yaml`) owns the decision: `contact_create` is in `blocked_capability_classes` → `BLOCKED=true`.
- **Harness** has **no** authority to classify or refuse operations.
- **Adapter** acts only as a secondary fail-closed defense; refusal occurs at the manifest gate **before** the adapter is invoked.

### 5.4 Expected trace markers

```text
REQUESTED_OPERATION=create-contact
CAPABILITY_CLASS=contact_create
CLASSIFICATION_OWNER=RUNTIME_MANIFEST_GATE

BLOCKED=true
BLOCKED_SOURCE=contracts/ghl_tool_manifest.yaml
BLOCK_DECISION_AUTHORITY=GHL_TOOL_MANIFEST

TOOL_MANIFEST_REFUSED=true
REFUSAL_LAYER=TOOL_MANIFEST

TRANSPORT_ATTEMPTED=false
GHL_LIVE_CALLS=0
GHL_WRITES=0
EXTERNAL_EFFECTS=0

AUDIT_WARNING_RECORDED=true
AUDIT_WARNING_PROJECTED_STAGE_A=true
AUDIT_WARNING_DURABLE_PROOF=proof/nw008/tranche-d/at-09-workflow-run-audit.json

FIRESTORE_WRITES=0
NW005_STAGE_B_ACTIVATED=NO
```

---

## 6. D1 — proof obligations

| ID | Obligation | Target verification | Status |
| --- | --- | --- | --- |
| **TD1-01** | Runtime-owned manifest gate classifies `create-contact` → `contact_create` deterministically | Unit test of `RuntimeToolManifestGate` | PLANNED |
| **TD1-02** | Refusal evaluates `contracts/ghl_tool_manifest.yaml` `blocked_capability_classes` | Unit test verifying manifest lookup | PLANNED |
| **TD1-03** | Refusal occurs before any adapter invocation or network transport | Trace check: `TRANSPORT_ATTEMPTED=false`, adapter uncalled | PLANNED |
| **TD1-04** | Refusal appends structured warning to `packet.audit.warnings` | `packet["audit"]["warnings"]` contains `TOOL_MANIFEST_REFUSED:contact_create` | PLANNED |
| **TD1-05** | Warning projects cleanly to `workflow_run_audit_v1` via NW-005 Stage A | `project_workflow_run_audit()` produces schema-valid audit | PLANNED |
| **TD1-06** | Durable proof artifact committed under `proof/nw008/tranche-d/` | File existence, valid JSON, schema-compliant | PLANNED |
| **TD1-07** | Effect counters all zero | `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0` | PLANNED |
| **TD1-08** | No Firestore Stage B activation | `NW005_STAGE_B_ACTIVATED=NO`, `MemoryAuditStore` supporting only | PLANNED |

---

## 7. D1 — negative controls

The future D1 implementation must freeze and pass the following negative controls:

1. **NC-D1-1 (Harness-local mapping forbidden)**: Harness cannot supply custom mapping to trigger manifest refusal; classification must originate in `RuntimeToolManifestGate`.
2. **NC-D1-2 (Unblocked capability admitted)**: An unblocked, allowlisted capability class (e.g. `contact_search`) does not emit `TOOL_MANIFEST_REFUSED`.
3. **NC-D1-3 (Zero transport on refusal)**: Attempting transport for a blocked capability fails closed immediately with zero network requests.
4. **NC-D1-4 (Manifest authority negative control)**: Removing `contact_create` from a test manifest fixture causes the manifest gate refusal predicate to fail, proving refusal is driven by manifest data, not hard-coded string matching.
5. **NC-D1-5 (Audit warning absent on normal run)**: Runs without blocked tool invocations have empty `audit.warnings` (or no tool-refusal warnings).
6. **NC-D1-6 (Stage A warning fidelity)**: Stage A projection preserves the exact warning string byte-for-byte in `workflow_run_audit_v1.warnings`.
7. **NC-D1-7 (Nonzero effect failure)**: Injecting any non-zero GHL/Firestore counter fails evidence validation immediately.
8. **NC-D1-8 (No Stage B invocation)**: Proof suite verifies Firestore client is not instantiated or invoked during D1 execution.

---

## 8. D1 → D2 gate

Implementation of Subunit D2 (AT-8) is **strictly prohibited** until Subunit D1 passes all gate criteria:

```text
D2_EXECUTION_ALLOWED_ONLY_IF:
  D1_TESTS=PASS
  D1_PROOF=PASS
  D1_EXTERNAL_EFFECTS=0
  D1_GHL_LIVE_CALLS=0
  D1_GHL_WRITES=0
  D1_FIRESTORE_WRITES=0
  D1_POLICY_SEMANTICS_CHANGE=NO
  D1_TOOL_MANIFEST_SEMANTICS_CHANGE=NO
  D1_AUDIT_SCHEMA_CHANGE=NO
  D1_MEETING_FOLLOW_UP_PACKET_SCHEMA_CHANGE=NO
```

### Stop condition on D1 failure

If any D1 requirement or test fails:
```text
D1_GATE_FOR_D2=CLOSED
STOP_CODE=NW008_TRANCHE_D_D1_FAILED_DO_NOT_START_D2
```
Do not begin D2 implementation.

---

## 9. D2 — AT-8 architecture

### 9.1 Historical requirement

> Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice.

### 9.2 Semantic distinction: write attempt vs intent cardinality

```text
AT8_CAP_SEMANTIC=WRITE_ATTEMPT_CAP
AT8_INTENT_CAP_IS_NOT_SUBSTITUTE=YES
```

The workflow contract specifies both intent limits (`max_note_intents_per_run`, `max_stage_intents_per_run`) and write limits (`max_note_writes_per_run`, `max_stage_writes_per_run`). Proving that `bound_intents` limits a single intent bag does **not** satisfy AT-8. AT-8 specifically requires that a sequential **second write attempt** within one run is refused by deterministic policy.

### 9.3 Target architecture and data flow

```text
agent / proposal requests mutation write attempt
        ↓
deterministic orchestration policy permits intent (attempt #1)
        ↓
run-scoped write-attempt cap guard
        ↓
attempt #1 admitted (WRITE_ATTEMPT_COUNT=1 <= max_writes_per_run)
        ↓
no transport in offline lane (TRANSPORT_ATTEMPTED=false, CANONICAL_PACKET_MUTATION_ATTEMPTED=false)
        ↓
attempt #2 requested within the SAME workflow run
        ↓
run-scoped write-attempt cap guard
        ↓
refused because write-attempt cap exhausted (WRITE_ATTEMPT_COUNT=2 > max_writes_per_run)
        ↓
refusal recorded as POLICY_CAP_REFUSAL by DETERMINISTIC_POLICY
        ↓
zero transport / zero external effect (EXTERNAL_EFFECTS=0, GHL_WRITES=0)
```

### 9.4 Enforcement ownership

```text
ENFORCEMENT_OWNER=DETERMINISTIC_ORCHESTRATION_POLICY
AGENT_SELF_RESTRAINT_AUTHORITY=NO
HARNESS_AUTHORITY=NO
OFFLINE_ADAPTER_AUTHORITY=SECONDARY_FAIL_CLOSED_ONLY
```

### 9.5 Canonical packet semantics preserved

```text
CANONICAL_PACKET_MUTATION_ATTEMPTED=false
CANONICAL_PACKET_MUTATION_VERIFIED=false
MEETING_FOLLOW_UP_PACKET_SCHEMA_CHANGE=NO
```

Canonical packet fields (`packet.mutations.note.attempted`, `packet.mutations.opportunity_stage.attempted`) remain `false` because no live external transport occurs in Phase 1 / offline execution. The write-attempt refusal is recorded in an execution/policy trace artifact, preserving packet schema integrity.

---

## 10. D2 — write-attempt cap authority

### 10.1 Contract authority

The numeric caps are defined in [`contracts/workflow_states.yaml`](../../contracts/workflow_states.yaml):

```yaml
invariants:
  - max_note_writes_per_run: 1
  - max_stage_writes_per_run: 1
  - max_note_intents_per_run: 1
  - max_stage_intents_per_run: 1
```

### 10.2 Contract loading repair

`StateMachine` currently loads `max_note_intents = 1` and `max_stage_intents = 1` as hard-coded integers. In Tranche D:
- `StateMachine` will dynamically load `max_note_writes_per_run` and `max_stage_writes_per_run` (along with intent limits) directly from the invariants block in `contracts/workflow_states.yaml`.
- This is classified as **`CONTRACT_LOADING_REPAIR`**, not `NEW_POLICY_SEMANTICS`, because the contracted values (`1` and `1`) and meanings remain unchanged.

---

## 11. D2 — proof obligations

| ID | Obligation | Target verification | Status |
| --- | --- | --- | --- |
| **TD2-01** | `StateMachine` loads `max_note_writes` and `max_stage_writes` from contract invariants | Unit test verifying contract parsing | PLANNED |
| **TD2-02** | Run-scoped write-attempt ledger tracks admitted write attempts per `run_id` | Unit test of ledger isolation | PLANNED |
| **TD2-03** | Attempt #1 admitted by deterministic policy with zero external transport | Trace check: `FIRST_ATTEMPT_CAP_DECISION=PERMITTED`, `TRANSPORT_ATTEMPTED=false` | PLANNED |
| **TD2-04** | Attempt #2 for note in same run is refused by deterministic policy | `SECOND_ATTEMPT_REFUSED=true`, `SECOND_ATTEMPT_REFUSED_BY=DETERMINISTIC_POLICY` | PLANNED |
| **TD2-05** | Attempt #2 for stage in same run is refused by deterministic policy | `SECOND_ATTEMPT_REFUSED=true`, `SECOND_ATTEMPT_REFUSED_BY=DETERMINISTIC_POLICY` | PLANNED |
| **TD2-06** | Agent proposal proposing second write cannot bypass policy cap | Test where agent proposal requests 2 writes → policy refuses | PLANNED |
| **TD2-07** | Fresh `run_id` gets a separate ledger and admits attempt #1 | Test verifying run isolation | PLANNED |
| **TD2-08** | Canonical packet fields remain `attempted=false`, `verified=false` | Packet schema validation + inspection | PLANNED |
| **TD2-09** | Effect counters all zero | `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0` | PLANNED |
| **TD2-10** | Durable proof artifact committed under `proof/nw008/tranche-d/` | File existence, valid JSON, schema-compliant | PLANNED |

---

## 12. D2 — negative controls

The future D2 implementation must freeze and pass the following negative controls:

1. **NC-D2-1 (Agent proposal bypass prevention - note)**: Agent explicitly proposes two note writes in one run; policy ledger refuses the second attempt.
2. **NC-D2-2 (Agent proposal bypass prevention - stage)**: Agent explicitly proposes two stage writes in one run; policy ledger refuses the second attempt.
3. **NC-D2-3 (Run isolation)**: Re-running with a distinct `run_id` starts with a zeroed ledger and admits attempt #1.
4. **NC-D2-4 (Harness bypass prevention)**: Harness cannot override or suppress the run-scoped cap guard.
5. **NC-D2-5 (Contract-derived cap negative control)**: Supplying a test contract with `max_note_writes_per_run: 2` admits two attempts and refuses the third, proving enforcement derives from the contract rather than a hard-coded literal `1`.
6. **NC-D2-6 (Intent cardinality distinction)**: Unit test verifies that satisfying intent cardinality alone does not pass AT-8 write-attempt proof.
7. **NC-D2-7 (Zero transport on second attempt)**: No network transport or adapter write is invoked for either the admitted first attempt or the refused second attempt.
8. **NC-D2-8 (Canonical packet attempted fields intact)**: Verify `packet.mutations.note.attempted == False` and `packet.mutations.opportunity_stage.attempted == False`.
9. **NC-D2-9 (Nonzero effect failure)**: Non-zero write/effect counters fail validation immediately.
10. **NC-D2-10 (Duplicate run rejection preserved)**: Existing `RunRegistry` duplicate terminal `run_id` rejection remains intact.

---

## 13. Allowed / blocked files for future implementation

### 13.1 Planning pass (current PR)

```text
ALLOWED:
  proof/nw008/nw-008-tranche-d-implementation-packet.md

BLOCKED:
  src/**
  tests/**
  contracts/**
  fixtures/**
  .github/workflows/**
  deploy/**
  infra/**
```

### 13.2 Future implementation pass (post-plan approval)

```text
PLANNED_ALLOWED_IMPLEMENTATION_FILES:
  src/orchestration/manifest_gate.py       # runtime-owned tool-manifest gate (D1)
  src/orchestration/attempt_ledger.py      # run-scoped write-attempt ledger (D2)
  src/orchestration/state_machine.py       # contract loading repair for write caps
  src/orchestration/runner.py              # integrate gate and attempt ledger into workflow run
  src/orchestration/nw008_tranche_d.py     # dedicated Tranche D execution & evidence harness
  tests/test_manifest_gate.py              # D1 unit and negative control tests
  tests/test_write_attempt_ledger.py       # D2 unit and negative control tests
  tests/test_nw008_tranche_d_acceptance.py # full Tranche D acceptance and proof suite
  proof/nw008/tranche-d/**                 # generated durable proof artifacts

PLANNED_BLOCKED_FILES:
  contracts/meeting_follow_up_packet.schema.json  # NO schema changes
  contracts/workflow_run_audit.schema.json        # NO schema changes
  contracts/ghl_tool_manifest.yaml                # NO manifest modifications
  contracts/workflow_states.yaml                  # NO contract numeric changes
  deploy/**                                       # NO deployment
  infra/**                                        # NO cloud infra
  .github/workflows/**                            # NO CI workflow edits
```

---

## 14. Validation plan

### 14.1 Minimum Subunit D1 validation suite

1. `pytest tests/test_manifest_gate.py` — unit tests for classifier and manifest lookup.
2. `pytest tests/test_manifest_gate_negative_controls.py` — 8 negative controls.
3. `pytest tests/test_firestore_audit_project.py` — NW-005 Stage A projection with audit warnings.
4. Schema validation of projected `workflow_run_audit_v1` JSON against `contracts/workflow_run_audit.schema.json`.
5. Zero-effect counter assertion (`GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0`).

### 14.2 Minimum Subunit D2 validation suite

1. `pytest tests/test_write_attempt_ledger.py` — unit tests for run-scoped ledger and contract cap loading.
2. `pytest tests/test_write_attempt_negative_controls.py` — 10 negative controls.
3. `pytest tests/test_policy.py` — policy evaluation regression tests.
4. `pytest tests/test_runner.py` — runner regression and duplicate run rejection tests.
5. Zero-effect counter assertion (`GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0`).

### 14.3 Full integration validation

1. `pytest` — full test suite pass.
2. `git diff --check` — whitespace and formatting sanity.
3. Secret scan — ensure no secrets or tokens committed.
4. Exact-head Phase 1 Deterministic CI pass on GitHub Actions.

---

## 15. Proof layout and SHA integrity

### 15.1 Bounded proof directory layout

```text
proof/nw008/tranche-d/
├── at-09-run.json                        # D1 execution packet with audit.warnings
├── at-09-workflow-run-audit.json         # D1 projected Stage-A audit document
├── at-08-run.json                        # D2 execution trace showing attempt #1 admitted & attempt #2 refused
├── proof-manifest.md                     # Human-readable Tranche D proof manifest
└── proof-return.yaml                     # Machine-readable proof return block
```

### 15.2 Commit and proof generation discipline

To maintain strict immutable SHA integrity:

1. **Commit A1**: Stable Subunit D1 (AT-9) implementation commit.
2. **Commit P1**: D1 proof generation commit, recording `IMPLEMENTATION_SUBJECT_SHA=<A1>`.
3. *(D1 Promotion Gate evaluated)*
4. **Commit A2**: Stable Subunit D2 (AT-8) implementation commit.
5. **Commit P2**: Final Tranche D proof bundle commit, recording `IMPLEMENTATION_SUBJECT_SHA=<A2>`.

Every proof artifact must record the exact implementation commit SHA, verifiable via:
```bash
git cat-file -e "<IMPLEMENTATION_SUBJECT_SHA>^{commit}"
git merge-base --is-ancestor "<IMPLEMENTATION_SUBJECT_SHA>" HEAD
```

---

## 16. Competition / judge-visible value

### 16.1 Subunit D1 (AT-9) value

- **Capability-Level Tool Governance**: Demonstrates that dangerous or unapproved tool operations (`contact_create`) are refused at the declarative manifest layer before network transport can occur.
- **Durable Auditability**: Every refusal generates a structured audit warning preserved through the NW-005 Stage A pipeline, proving compliance is inspectable.
- **Fail-Closed Safety**: Proves zero CRM mutation and zero data leakage when unauthorized tools are requested.

### 16.2 Subunit D2 (AT-8) value

- **Orchestration-Enforced Run Caps**: Proves that OL3 deterministic orchestration policy—not agent self-restraint or prompt guidelines—enforces per-run mutation caps.
- **Agent Bypass Prevention**: Demonstrates that even if an AI agent repeatedly proposes or attempts writes, the orchestration layer deterministically halts attempt N+1.
- **Zero-Effect Isolation**: Validates all governance boundaries offline with zero external effects and zero risk to CRM data.

---

## 17. Implementation stop conditions

During future implementation, the orchestrator must **STOP** immediately and return for architecture review if:

1. Any requirement appears to require live GHL network access or mutation authorization.
2. Any requirement appears to require Firestore Stage B online writes.
3. Any schema modification to `meeting_follow_up_packet.schema.json` or `workflow_run_audit.schema.json` appears necessary.
4. Any numeric policy cap in `contracts/workflow_states.yaml` must be changed.
5. Any blocked capability class in `contracts/ghl_tool_manifest.yaml` must be changed.
6. Any D1 negative control or proof assertion fails.
7. Subunit D1 fails any promotion gate item before D2 starts.
8. Any non-zero external effect, GHL call, or Firestore write is observed.

---

## 18. Machine-readable return block

```text
BRANCH=chore/nw008-tranche-d-implementation-plan
BASE_SHA=4af506a90c9b6c6eaf75f6fdb3235ad94a1af5a9

PR46_STATUS=MERGED_COMPLETE
PR46_HEAD_SHA=ec6ac63d5b3971d500be2f6fbfd86f249966b126
PR46_MERGE_SHA=4af506a90c9b6c6eaf75f6fdb3235ad94a1af5a9
PR46_MERGED_AT=2026-08-14T17:00:10Z

PLANNING_ARTIFACT=proof/nw008/nw-008-tranche-d-implementation-packet.md
D1=AT-9
D2=AT-8
D2_REQUIRES_D1_GREEN=YES

AT9_CLASSIFICATION_OWNER=RUNTIME_MANIFEST_GATE
AT9_BLOCK_DECISION_AUTHORITY=GHL_TOOL_MANIFEST
AT9_STAGE_A_AUDIT_SUFFICIENT=YES
AT9_STAGE_B_REQUIRED=NO

AT8_CAP_SEMANTIC=WRITE_ATTEMPT_CAP
AT8_CAP_AUTHORITY=WORKFLOW_CONTRACT
AT8_INTENT_CAP_IS_NOT_SUBSTITUTE=YES
AT8_CANONICAL_PACKET_ATTEMPT_FIELDS_REUSED=NO

AT8_STATUS=PARTIAL
AT9_STATUS=PARTIAL
NW008_OVERALL_STATUS=IN_PROGRESS

PLANNING_ONLY=YES
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
TESTS_CHANGED=NO
CONTRACTS_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
EXTERNAL_EFFECTS=0

READY_FOR_IMPLEMENTATION_PLAN_REVIEW=YES
STOP_CODE=NW008_TRANCHE_D_IMPLEMENTATION_PLAN_READY_FOR_REVIEW
```
