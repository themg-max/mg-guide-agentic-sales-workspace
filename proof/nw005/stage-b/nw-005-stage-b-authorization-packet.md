# NW-005 Stage B — Firestore Smoke-Proof Authorization Packet

**This is a planning artifact only.** No Stage B runtime code, Firestore client,
network call, IAM change, or deployment is created or authorized by this
document. Execution requires a separate explicit human authorization.

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
STATUS=PROPOSED_NOT_AUTHORIZED
```

## Objective (bounded smoke proof)

```text
workflow_run_audit_v1
  → Firestore create-only write
  → exact get
  → content_fingerprint verification
  → cleanup
  → STOP
```

Stage B's sole purpose is to prove that a Stage A-projected
`workflow_run_audit_v1` document can be durably written to a Firestore test
project, read back exactly, verified against its `content_fingerprint`, and
cleaned up — nothing more.

## Required environment fields

| Field | Value |
| --- | --- |
| `GCP_TEST_PROJECT_ID` | `UNKNOWN` — required before authorization |
| `FIRESTORE_DATABASE_ID` | `UNKNOWN` — required before authorization |
| `REGION` | `UNKNOWN` — required before authorization |
| `EXECUTION_PRINCIPAL` | `UNKNOWN` — required before authorization |
| `CREDENTIAL_SOURCE` | `UNKNOWN` — required before authorization |
| `IAM_CHANGE_REQUIRED` | `UNKNOWN` — required before authorization |

**Blocking rule:** if any required environment field remains `UNKNOWN` at
review time, Stage B implementation remains blocked. As of this packet, all
six fields are `UNKNOWN`, so Stage B is **NOT_AUTHORIZED** and must not be
implemented.

## Permitted Firestore call graph (complete and exhaustive)

1. `create workflow_runs/{allowlisted_synthetic_run_id}` (create-only; fails
   if document exists)
2. `get workflow_runs/{same_run_id}` (exact document get, no query)
3. Verify schema / `run_id` / `content_fingerprint` locally after readback
4. `delete workflow_runs/{same_run_id}` for `stage_b_smoke` cleanup
5. STOP

## Explicitly prohibited

- `set` / overwrite semantics
- `update` (any partial or full update)
- collection `list`
- `query` of any kind
- wildcard document access in application logic
- production / customer data of any kind
- GHL / CRM calls
- policy re-evaluation
- agent rerun
- Cloud Run deployment
- Secret Manager mutation
- IAM mutation without separate explicit human authorization

## Operation caps

```text
MAX_DOCUMENT_CREATES=10
MAX_DOCUMENT_READS=20
MAX_DOCUMENT_DELETES=10
MAX_EXECUTION_MINUTES=10
DATA=synthetic_only
```

## Retention modes

| Mode | Status | Behavior |
| --- | --- | --- |
| `stage_b_smoke` | In scope (once authorized) | `create → get → verify → delete`; no residual documents |
| `acceptance_demo` | `NOT_AUTHORIZED` | Deferred to NW-008; requires a temporary retention window before cleanup |

## Required Stage B proof fields (to be collected at execution, not now)

```text
FIRESTORE_CREATE_ATTEMPTED=
FIRESTORE_CREATE_VERIFIED=
FIRESTORE_READBACK_VERIFIED=
RUN_ID_MATCH=
CONTENT_FINGERPRINT_MATCH=
SCHEMA_VALID_AFTER_READBACK=
DELETE_ATTEMPTED=
DELETE_VERIFIED=
FIRESTORE_WRITES=
FIRESTORE_READS=
FIRESTORE_DELETES=
REAL_CUSTOMER_DATA=
GHL_LIVE_CALLS=
EXTERNAL_EFFECTS=
TEST_PROJECT_ID=
DATABASE_ID=
PRINCIPAL=
STARTED_AT=
COMPLETED_AT=
```

All fields are blank at planning time; they may only be filled by actual
authorized Stage B execution evidence.

## Acceptance-test boundary

**AT-10 must NOT be claimed complete from `stage_b_smoke`.** The smoke proof
demonstrates write/readback/cleanup mechanics only. Honest AT-10 completion
is deferred to NW-008 with the `acceptance_demo` retention mode, which is
separately NOT_AUTHORIZED here.

## Current truth

```text
NW005_STAGE_A=MERGED_COMPLETE
NW005_STAGE_A_PR18_MERGE_SHA=63aadc5c90569cfa119af7cc7e30fbac62f8544b
NW005_STAGE_A_PR18_FINAL_HEAD=695bf3dcae3c9a82ef3af9be9cf264a669485939
NW005_STAGE_A_PR18_MERGED_AT=2026-08-13T01:15:44Z
NW005_STAGE_B=PLANNING_NOT_AUTHORIZED
FIRESTORE_NETWORK_OPERATIONS=0
FIRESTORE_WRITES=0
FIRESTORE_READS=0
FIRESTORE_DELETES=0
GHL_LIVE_CALLS=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS=0
```

`STOP_CODE=NW005_STAGE_B_AUTHORIZATION_PACKET_READY_FOR_REVIEW`
