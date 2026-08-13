# NW-005 Stage B Wave 1 Firestore Persistence Proof

## Authorization baseline

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
BASELINE_MERGE_SHA=1d9ff931dd431ce04f47ad907b08252b433d23c9
IMPLEMENTATION_HEAD_SHA=e71f2130e5eee138989ec0cf418d74c3ff1c7e1a
EXECUTION_CODE_SHA=e71f2130e5eee138989ec0cf418d74c3ff1c7e1a
PROVENANCE_REPAIR_RERUN=YES
PROVENANCE_REPAIR_REASON=initial smoke runner was uncommitted at first execution
RUN_ID=run_nw006_success_001

PROJECT=mg-devpost
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs
```

## Execution summary

```text
FIRESTORE_CREATE_ATTEMPTED=YES
FIRESTORE_CREATE_VERIFIED=YES
FIRESTORE_READBACK_VERIFIED=YES

RUN_ID_MATCH=YES
SCHEMA_VALID_AFTER_READBACK=YES

EXPECTED_PROJECTED_CONTENT_FINGERPRINT=e2e052758823451ac2cbdba467972bbf83545cd7e6e18f19fc4d08d692f3d2a5
STORED_CONTENT_FINGERPRINT=e2e052758823451ac2cbdba467972bbf83545cd7e6e18f19fc4d08d692f3d2a5
RECOMPUTED_READBACK_CONTENT_FINGERPRINT=e2e052758823451ac2cbdba467972bbf83545cd7e6e18f19fc4d08d692f3d2a5
CONTENT_FINGERPRINT_MATCH=YES

DELETE_ATTEMPTED=YES
DELETE_VERIFIED=YES
DELETE_GET_NOT_FOUND=YES

STAGE_B_DOCUMENT_CREATES=1
STAGE_B_DOCUMENT_READS=2
STAGE_B_DOCUMENT_DELETES=1
STAGE_B_NETWORK_CALLS=4
STAGE_B_AUTHORIZED_MUTATING_EXTERNAL_EFFECTS=2

WAVE1_CUMULATIVE_DOCUMENT_CREATES=2
WAVE1_CUMULATIVE_DOCUMENT_READS=4
WAVE1_CUMULATIVE_DOCUMENT_DELETES=2
WAVE1_CUMULATIVE_NETWORK_CALLS=8
WAVE1_CUMULATIVE_MUTATING_EXTERNAL_EFFECTS=4

REAL_CUSTOMER_DATA=0
GHL_LIVE_CALLS=0

CLEANUP_STATUS=SUCCESS
RESULT=PASS
STARTED_AT=2026-08-13T14:21:15.863840+00:00
COMPLETED_AT=2026-08-13T14:21:17.255386+00:00
```

## Authorized call graph executed

1. `create workflow_runs/run_nw006_success_001` — verified created
2. `exact get workflow_runs/run_nw006_success_001` — verified exists
3. `validate schema` — `workflow_run_audit_v1` schema and invariants passed
4. `verify exact run_id` — readback `run_id` equals `run_nw006_success_001`
5. `recompute readback content fingerprint` using merged Stage A canonicalizer (`nw005_canonical_json_v1` + SHA-256 hex)
6. Required triple equality held:
   - `RECOMPUTED_READBACK_CONTENT_FINGERPRINT`
   - `== STORED_CONTENT_FINGERPRINT`
   - `== EXPECTED_PROJECTED_CONTENT_FINGERPRINT`
7. `exact delete workflow_runs/run_nw006_success_001` — verified deleted
8. `exact get workflow_runs/run_nw006_success_001` expecting `NOT_FOUND` — verified
9. `STOP`

## Scope and constraints observed

- Only the Wave-1-authorized run ID `run_nw006_success_001` was executed.
- No set/overwrite, update, list, query, batch, transaction, or wildcard access was used.
- Only `create_exact`, `get_exact`, and `delete_exact` methods were invoked against Firestore.
- Application Default Credentials were used; no service-account JSON key was created or downloaded.
- No IAM, Secret Manager, Cloud Run, GHL, or CRM mutation occurred.
- All data was synthetic, sourced from `fixtures/nw005/packets/packet-success.completed.json`.
- Operation counters remained well within caps:
  - creates 1 / 10 for this repair rerun
  - reads 2 / 20 for this repair rerun
  - deletes 1 / 10 for this repair rerun
  - cumulative authorized Wave 1 totals remain valid: creates 2 / 10, reads 4 / 20, deletes 2 / 10, network calls 8 / 20, mutating external effects 4 / requested cap
- Document cleanup succeeded; post-delete `get_exact` returned `NOT_FOUND`.

## What is NOT claimed

```text
AT10_COMPLETE=NO
ACCEPTANCE_DEMO_COMPLETE=NO
PRODUCTION_READY=NO
```

## Stop condition

```text
STOP_CODE=NW005_STAGE_B_WAVE1_SMOKE_COMPLETE_READY_FOR_REVIEW
```
