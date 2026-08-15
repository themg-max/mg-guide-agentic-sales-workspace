# NW-008 AT-10 — Bounded Firestore Execution Authorization

**This is an execution-authorization decision artifact only.**

It does **not** itself execute Firestore, claim AT-10 complete, or authorize
completion claims. Self-activation is **FORBIDDEN**.

Human approval on this artifact authorizes a **single bounded** AT-10 Firestore
acceptance-demo execution against the frozen synthetic run set only. Completion
claim authority remains separate and is **not** granted here.

```text
AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1
PACKET_KIND=AT10_BOUNDED_FIRESTORE_EXECUTION_AUTHORIZATION
STATUS=HUMAN_APPROVED
SELF_ACTIVATION=FORBIDDEN

DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
HUMAN_SIGNATURE=APPROVED
HUMAN_APPROVER=themg@themiliare-group.com
APPROVED_AT=2026-08-15T11:28:00-04:00

AT10_EXECUTION_AUTHORIZED=YES
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO

NETWORK_OPERATIONS_AUTHORIZED=YES
FIRESTORE_CREATES_AUTHORIZED=YES
FIRESTORE_READS_AUTHORIZED=YES
FIRESTORE_DELETES_AUTHORIZED=YES
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO

AUTHORIZATION_PACKET_SHA=6702cb138195a48b9dbbb9b447ae742a57f07f31
IMPLEMENTATION_SUBJECT_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
EXECUTION_CODE_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
IMPLEMENTATION_REVIEW_PR=52
IMPLEMENTATION_REVIEW_MERGE_SHA=1609cc463741b84faa90845749171e31e01079f0
REVIEWER_DISPOSITION=FAVORABLE_HUMAN_CONFIRMED
```

## Purpose

Record the separate post-implementation-review human execution grant for a
single bounded AT-10 Firestore acceptance-demo run against the frozen synthetic
allowlist. This grant is active only for the exact identity, target, caps, and
operation permissions bound below.

```text
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
AT10_EXECUTION_AUTHORIZED=YES
NETWORK_OPERATIONS_AUTHORIZED=YES
FIRESTORE_CREATES_AUTHORIZED=YES
FIRESTORE_READS_AUTHORIZED=YES
FIRESTORE_DELETES_AUTHORIZED=YES
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
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
5. **This** execution authorization decision artifact — human-approved bounded
   Firestore execution grant (`DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION`).
6. Bounded execution only under this grant with
   `AT10_EXECUTION_AUTHORIZED=YES` and the operation permissions below.
7. Completion claim only under a separate later
   `AT10_COMPLETION_CLAIM_AUTHORIZED=YES` (not this artifact).

```text
EXECUTION_CODE_SHA_MUST_EQUAL_IMPLEMENTATION_SUBJECT_SHA=YES
EXECUTION_CODE_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
IMPLEMENTATION_SUBJECT_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
SHA_EQUALITY=PASS
IMPLEMENTATION_SUBJECT_IS_ANCESTOR_OF_MAIN=YES
```

## Authorized execution target

The authorized target is exactly:

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

## Operation permissions (bounded call graph)

```text
NETWORK_OPERATIONS_AUTHORIZED=YES
FIRESTORE_CREATES_AUTHORIZED=YES
FIRESTORE_READS_AUTHORIZED=YES
FIRESTORE_DELETES_AUTHORIZED=YES
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
NO_COLLECTION_SWEEP=YES
COLLECTION_FANOUT=1
```

Allowed operations are limited to explicit document-path create, get/read, and
delete for the four allowlisted run ids. Collection list, query, and sweep are
prohibited.

## Caps (hard bounds)

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

## Prohibited (always under this grant)

```text
GHL_CRM_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
CLOUD_RUN_AUTHORIZED=NO
REAL_CUSTOMER_DATA_AUTHORIZED=NO

FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO

AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

Also forbidden:

- agent/orchestrator self-activation without this human-approved grant;
- any project/database/collection/run id outside the bound target/allowlist;
- mutating IAM, secrets, Cloud Run, or GHL/CRM;
- using real customer data;
- claiming AT-10 complete from this authorization alone;
- reopening NW-005 Stage B smoke as a substitute for AT-10.

## Current grant state

```text
STATUS=HUMAN_APPROVED
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
HUMAN_SIGNATURE=APPROVED
HUMAN_APPROVER=themg@themiliare-group.com
APPROVED_AT=2026-08-15T11:28:00-04:00
AT10_EXECUTION_AUTHORIZED=YES
NETWORK_OPERATIONS_AUTHORIZED=YES
FIRESTORE_CREATES_AUTHORIZED=YES
FIRESTORE_READS_AUTHORIZED=YES
FIRESTORE_DELETES_AUTHORIZED=YES
FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
FIRESTORE_EXECUTION_OCCURRED=NO
```

This artifact authorizes bounded execution only. It does not record that
execution has occurred and does not authorize an AT-10 completion claim.

## Human decision block (approved)

```text
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
HUMAN_SIGNATURE=APPROVED
HUMAN_APPROVER=themg@themiliare-group.com
APPROVED_AT=2026-08-15T11:28:00-04:00
AT10_EXECUTION_AUTHORIZED=YES
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

A chat acknowledgement is not a substitute for this explicit repository
decision. Approval is limited to the bounded target, allowlist, caps, and
operation permissions above.

## Stop

```text
STOP_CODE=NW008_AT10_BOUNDED_EXECUTION_GRANT_READY_FOR_FORMAL_REVIEW
DECISION=AUTHORIZED_FOR_BOUNDED_FIRESTORE_EXECUTION
STATUS=HUMAN_APPROVED
HUMAN_SIGNATURE=APPROVED
AT10_EXECUTION_AUTHORIZED=YES
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
DO_NOT_CLAIM_AT10_COMPLETE=YES
```
