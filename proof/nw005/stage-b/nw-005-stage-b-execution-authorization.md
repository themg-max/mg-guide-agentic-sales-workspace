# NW-005 Stage B — Execution Authorization Decision Artifact

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
DECISION=AUTHORIZED_FOR_EXECUTION
REQUESTED_DECISION=AUTHORIZED_FOR_EXECUTION
REQUESTED_MODE=stage_b_smoke

PROJECT=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs

INITIAL_RUN_ID=run_nw006_success_001

ALLOWLIST:
run_nw006_success_001
run_nw006_stage_denied_001
run_nw006_ambiguous_contact_001
run_nw006_failed_001

ALLOWLIST_COUNT=4
ALLOWLIST_MATCH_MODE=EXACT_STRING_EQUALITY_ONLY

MAX_DOCUMENT_CREATES=10
MAX_DOCUMENT_READS=20
MAX_DOCUMENT_DELETES=10
MAX_EXECUTION_MINUTES=10

DATA=synthetic_only
IAM_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
CLOUD_RUN_AUTHORIZED=NO
GHL_CRM_AUTHORIZED=NO
ACCEPTANCE_DEMO_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO

CURRENT_EXECUTION_STATE=AUTHORIZED_NOT_STARTED
HUMAN_SIGNATURE=APPROVED
HUMAN_APPROVER=Achandler21
APPROVED_AT=2026-08-13T02:22:25Z

AUTHORIZED_MODE=stage_b_smoke
AUTHORIZED_PROJECT=mg-devpost
AUTHORIZED_DATABASE=devpost-google-contest
AUTHORIZED_LOCATION=us-east4
AUTHORIZED_COLLECTION=workflow_runs

EXECUTION_WAVE=1
MAX_DISTINCT_RUN_IDS_THIS_EXECUTION=1
AUTHORIZED_INITIAL_RUN_ID=run_nw006_success_001
```

## Purpose

This artifact records the authorization request for a future Stage B smoke proof
on the dedicated Firestore Native database in project `mg-devpost`.

This document is a planning / approval artifact only. It does not authorize any
Firestore document operations, does not create collections or documents, and
must not be used to self-activate execution.

## Decision request

Human approval is required before any execution may proceed under:

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
REQUESTED_DECISION=AUTHORIZED_FOR_EXECUTION
REQUESTED_MODE=stage_b_smoke
PROJECT=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs
```

## Allowed future call graph (only after an explicit human approval)

```text
create workflow_runs/{allowlisted_run_id}
-> exact get same document
-> verify schema
-> verify exact run_id
-> recompute read-back content fingerprint
-> require triple equality
-> exact delete
-> exact get expecting NOT_FOUND
-> STOP
```

The future execution path may address only the exact allowlisted synthetic
`run_id` values above. No wildcard access, no list/query calls, no updates, no
set/overwrite semantics, and no non-allowlisted run IDs are permitted.

## Prohibited actions

The following are forbidden in this artifact and in any Stage B operation under
this request unless a separate explicit approval is recorded:

- set / overwrite semantics
- update
- list
- query
- wildcard access
- non-allowlisted run_id
- non-terminal write
- production / customer data
- GHL / CRM
- policy reevaluation
- agent rerun
- Cloud Run
- IAM mutation
- Secret Manager mutation
- acceptance_demo retention
- AT-10 completion claim

## Execution posture

```text
CURRENT_EXECUTION_STATE=AUTHORIZED_NOT_STARTED
HUMAN_SIGNATURE=APPROVED
SELF_ACTIVATION=FORBIDDEN
```

The human decision has been recorded. This artifact itself does not perform
any runtime action.

## Binding evidence summary

```text
GCP_TEST_PROJECT_ID=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
FIRESTORE_DATABASE_ID=devpost-google-contest
FIRESTORE_LOCATION_ID=us-east4
FIRESTORE_API_STATUS=ENABLED
FIRESTORE_EDITION=STANDARD
FIRESTORE_MODE=NATIVE
ENCRYPTION_MODE=GOOGLE_MANAGED
ENVIRONMENT_BINDING_COMPLETE=YES
CURRENT_GRANT_STATE=AUTHORIZED_NOT_STARTED
BLOCKERS=NONE
```

## Stop condition

```text
STOP_CODE=NW005_STAGE_B_EXECUTION_AUTHORIZED_READY_FOR_PR_REVIEW
```
