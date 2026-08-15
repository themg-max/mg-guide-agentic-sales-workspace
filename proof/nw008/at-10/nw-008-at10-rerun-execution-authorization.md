# NW-008 AT-10 — Rerun Bounded Firestore Execution Authorization

**This is a fresh rerun execution-authorization decision artifact only.**

It does **not** itself execute Firestore, claim AT-10 complete, or authorize
completion claims. Self-activation is **FORBIDDEN**.

PR #53 authority is exhausted and **must not** be reused. This artifact is a
new grant lane bound to the PR #54 rerun recovery implementation subject.

Human decision is required before any Firestore network operation.

```text
AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_RERUN_V1
PACKET_KIND=AT10_BOUNDED_FIRESTORE_RERUN_EXECUTION_AUTHORIZATION
STATUS=PENDING_HUMAN_DECISION
SELF_ACTIVATION=FORBIDDEN

DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO

IMPLEMENTATION_SUBJECT_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
EXECUTION_CODE_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
IMPLEMENTATION_REVIEW_PR=54
IMPLEMENTATION_REVIEW_MERGE_SHA=82360d225069b2da7cd3ac93c8a330e69d2ed4c7
PR53_AUTHORITY_REUSABLE=NO
REVIEWER_DISPOSITION=FAVORABLE_HUMAN_CONFIRMED

OFFLINE_VALIDATION_RESULT=PASS
UNMERGED_GRANT_REJECTION=PASS
PHASE1_DETERMINISTIC=PASS
```

## Purpose

Record the separate post-rerun-implementation-review lane that may, **only after
an explicit human decision on a merged revision of this artifact**, authorize a
single bounded AT-10 Firestore acceptance-demo **rerun** against the frozen
synthetic run set, using the repository-owned governed executor merged via
PR #54.

Until human decision flips the grant:

```text
DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
NETWORK_OPERATIONS_AUTHORIZED=NO
FIRESTORE_CREATES_AUTHORIZED=NO
FIRESTORE_READS_AUTHORIZED=NO
FIRESTORE_DELETES_AUTHORIZED=NO
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED=NO
```

## Authority sequence (AR-08) — satisfied predecessors

1. Execution attempt 1 reconciled as contradictory evidence; PR #53 authority
   exhausted (`PR53_AUTHORITY_REUSABLE=NO`).
2. Rerun recovery implementation + offline validation bound as
   `IMPLEMENTATION_SUBJECT_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b`
   with `EXECUTION_CODE_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b`.
3. Rerun implementation review PR **#54** human-confirmed and merged:
   `IMPLEMENTATION_REVIEW_MERGE_SHA=82360d225069b2da7cd3ac93c8a330e69d2ed4c7`
   with head `5285cd34701c52049962325ca19a2fb8f4ca3274`, green Phase 1 CI, and
   `REVIEWER_DISPOSITION=FAVORABLE_HUMAN_CONFIRMED`.
4. Offline validation on the bound subject:
   `OFFLINE_VALIDATION_RESULT=PASS`,
   `UNMERGED_GRANT_REJECTION=PASS`,
   `PHASE1_DETERMINISTIC=PASS`.
5. **This** fresh rerun execution authorization decision artifact (current step)
   — pending human decision.
6. Execution only under a later human-approved grant on this artifact
   (`AT10_EXECUTION_AUTHORIZED=YES`) with the exact bindings below.
7. Completion claim only under a separate later
   `AT10_COMPLETION_CLAIM_AUTHORIZED=YES` (not this step).

```text
EXECUTION_CODE_SHA_MUST_EQUAL_IMPLEMENTATION_SUBJECT_SHA=YES
EXECUTION_CODE_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
IMPLEMENTATION_SUBJECT_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
SHA_EQUALITY=PASS
IMPLEMENTATION_SUBJECT_IS_ANCESTOR_OF_MAIN=YES
PR53_AUTHORITY_REUSABLE=NO
DO_NOT_REUSE_PR53_AUTHORITY=YES
```

## Authorized execution target (if and only if later approved)

If and only if a human later sets on a **merged** revision of this artifact:

```text
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
STATUS=HUMAN_APPROVED
HUMAN_SIGNATURE=APPROVED
AT10_EXECUTION_AUTHORIZED=YES
```

then — and only then — the authorized target is exactly:

```text
PROJECT=mg-devpost
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs

DATA=synthetic_only

RUN_IDS=
run_nw006_success_001
run_nw006_stage_denied_001
run_nw006_ambiguous_contact_001
run_nw006_failed_001
```

No other project, database, location, collection, or run id is authorized by
this artifact.

## Operation permissions (if and only if later approved)

```text
NETWORK_OPERATIONS_AUTHORIZED=YES
FIRESTORE_CREATES_AUTHORIZED=YES
FIRESTORE_READS_AUTHORIZED=YES
FIRESTORE_DELETES_AUTHORIZED=YES
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED=NO
ALL_FIRESTORE_OPERATIONS_MUST_FLOW_THROUGH_BOUNDED_EXECUTOR=YES
```

Allowed operations are limited to explicit document-path create, get/read, and
delete for the four allowlisted run ids, exclusively through
`scripts/nw008/run_at10_bounded_execution.py` at the bound execution code SHA.
Collection list, query, sweep, and any out-of-band Firestore probe are
prohibited.

## Caps (hard bounds if later approved)

```text
MAX_DISTINCT_RUN_IDS=4
MAX_DOCUMENT_CREATES=4
MAX_DOCUMENT_READS=12
MAX_DOCUMENT_DELETES=4
MAX_NETWORK_CALLS=20
MAX_EXECUTION_MINUTES=10

COLLECTION_FANOUT=1
NO_COLLECTION_SWEEP=YES
```

Execution must stop on first bound breach. Collection listing/sweep beyond the
four explicit run document paths is forbidden.

## Prohibited (always, including after any future approval of this artifact)

```text
GHL_CRM_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
CLOUD_RUN_AUTHORIZED=NO
REAL_CUSTOMER_DATA_AUTHORIZED=NO

FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
OUT_OF_BAND_FIRESTORE_PROBES_AUTHORIZED=NO

PR53_AUTHORITY_REUSABLE=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

Also forbidden:

- treating this pending artifact as an active execution grant;
- agent/orchestrator self-activation;
- reusing PR #53 or any prior execution grant authority;
- any Firestore create/get/delete/list/query while
  `AT10_EXECUTION_AUTHORIZED=NO`;
- any out-of-band Firestore probe outside the bounded executor;
- any network call to GCP or third parties while this decision is pending;
- mutating IAM, secrets, Cloud Run, or GHL/CRM;
- using real customer data;
- claiming AT-10 complete from this authorization step alone;
- reopening NW-005 Stage B smoke as a substitute for AT-10.

## What this pending PR authorizes right now

```text
AUTHORIZED_NOW=DOCUMENTATION_OF_PENDING_RERUN_EXECUTION_DECISION_ONLY
FIRESTORE_EXECUTION_OCCURRED=NO
NETWORK_CALLS=0
FIRESTORE_NETWORK_OPERATIONS=0
EXTERNAL_EFFECTS=0
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

Creating and merging a **pending** form of this artifact does not authorize
execution. Only an explicit human flip to
`DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION` with
`STATUS=HUMAN_APPROVED`, `HUMAN_SIGNATURE=APPROVED`, and
`AT10_EXECUTION_AUTHORIZED=YES` on a merged revision authorizes bounded
rerun execution through the bound executor.

## Human decision block (required)

```text
DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
HUMAN_SIGNATURE=PENDING
HUMAN_APPROVER=
APPROVED_AT=
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

A chat acknowledgement is not a substitute for an explicit repository decision
on this artifact.

## Stop

```text
STOP_CODE=NW008_AT10_RERUN_AUTHORIZATION_READY_FOR_HUMAN_DECISION
DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
DO_NOT_EXECUTE_FIRESTORE=YES
DO_NOT_CLAIM_AT10_COMPLETE=YES
DO_NOT_REUSE_PR53_AUTHORITY=YES
```
