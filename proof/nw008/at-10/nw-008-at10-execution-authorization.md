# NW-008 AT-10 — Bounded Firestore Execution Authorization

**This is an execution-authorization decision artifact only.**

It does **not** itself execute Firestore, claim AT-10 complete, or authorize
completion claims. Self-activation is **FORBIDDEN**.

Human decision is required before any Firestore network operation.

```text
AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1
PACKET_KIND=AT10_BOUNDED_FIRESTORE_EXECUTION_AUTHORIZATION
STATUS=PENDING_HUMAN_DECISION
SELF_ACTIVATION=FORBIDDEN

DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO

AUTHORIZATION_PACKET_SHA=6702cb138195a48b9dbbb9b447ae742a57f07f31
IMPLEMENTATION_SUBJECT_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
EXECUTION_CODE_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
IMPLEMENTATION_REVIEW_PR=52
IMPLEMENTATION_REVIEW_MERGE_SHA=1609cc463741b84faa90845749171e31e01079f0
REVIEWER_DISPOSITION=FAVORABLE_HUMAN_CONFIRMED
```

## Purpose

Record the separate post-implementation-review lane that may, **only after an
explicit human decision on a merged revision of this artifact**, authorize a
single bounded AT-10 Firestore acceptance-demo execution against the frozen
synthetic run set.

Until human decision flips the grant:

```text
DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
FIRESTORE_READS_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
FIRESTORE_DELETES_AUTHORIZED=NO
NETWORK_OPERATIONS_AUTHORIZED=NO
```

## Authority sequence (AR-08) — satisfied predecessors

1. Authorization packet reviewed/merged:
   `AUTHORIZATION_PACKET_SHA=6702cb138195a48b9dbbb9b447ae742a57f07f31`
2. Implementation-only grant human-approved and merged
   (`proof/nw008/at-10/nw-008-at10-implementation-authorization.md`).
3. Offline implementation + offline validation bound as
   `IMPLEMENTATION_SUBJECT_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd`.
4. Implementation review PR **#52** human-approved and merged:
   `IMPLEMENTATION_REVIEW_MERGE_SHA=1609cc463741b84faa90845749171e31e01079f0`
   with `REVIEWER_DISPOSITION=FAVORABLE_HUMAN_CONFIRMED`.
5. **This** execution authorization decision artifact (current step) —
   pending human decision.
6. Execution only under a later human-approved grant on this artifact
   (`AT10_EXECUTION_AUTHORIZED=YES`).
7. Completion claim only under a separate later
   `AT10_COMPLETION_CLAIM_AUTHORIZED=YES` (not this step).

```text
EXECUTION_CODE_SHA_MUST_EQUAL_IMPLEMENTATION_SUBJECT_SHA=YES
EXECUTION_CODE_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
IMPLEMENTATION_SUBJECT_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
SHA_EQUALITY=PASS
IMPLEMENTATION_SUBJECT_IS_ANCESTOR_OF_MAIN=YES
```

## Authorized execution target (if and only if later approved)

If and only if a human later sets on a **merged** revision of this artifact:

```text
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
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

AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

Also forbidden:

- treating this pending artifact as an active execution grant;
- agent/orchestrator self-activation;
- any Firestore create/get/delete/list/query while
  `AT10_EXECUTION_AUTHORIZED=NO`;
- any network call to GCP or third parties while this decision is pending;
- mutating IAM, secrets, Cloud Run, or GHL/CRM;
- using real customer data;
- claiming AT-10 complete from this authorization step alone;
- reopening NW-005 Stage B smoke as a substitute for AT-10.

## What this pending PR authorizes right now

```text
AUTHORIZED_NOW=DOCUMENTATION_OF_PENDING_EXECUTION_DECISION_ONLY
FIRESTORE_EXECUTION_OCCURRED=NO
NETWORK_CALLS=0
FIRESTORE_NETWORK_OPERATIONS=0
EXTERNAL_EFFECTS=0
```

Creating and merging a **pending** form of this artifact does not authorize
execution. Only an explicit human flip to
`DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION` with
`HUMAN_SIGNATURE=APPROVED` and `AT10_EXECUTION_AUTHORIZED=YES` on a merged
revision authorizes bounded execution.

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
STOP_CODE=NW008_AT10_EXECUTION_AUTHORIZATION_PR_READY_FOR_HUMAN_DECISION
DECISION=PENDING_HUMAN_EXECUTION_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
DO_NOT_EXECUTE_FIRESTORE=YES
DO_NOT_CLAIM_AT10_COMPLETE=YES
```
