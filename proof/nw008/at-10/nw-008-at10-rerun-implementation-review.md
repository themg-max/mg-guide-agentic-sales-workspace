# NW-008 AT-10 — Rerun Recovery Implementation Review

This packet presents the repository-owned rerun executor for formal
implementation review. It does not authorize Firestore execution or an AT-10
completion claim.

```text
EXECUTION_ATTEMPT_1_RECONCILED=YES

NEW_IMPLEMENTATION_SUBJECT_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
NEW_EXECUTION_CODE_SHA=3a3ff660b7cc6fe34eae9856eaca4fc643d84c0b
SHA_EQUALITY=PASS

OFFLINE_VALIDATION_RESULT=PASS
PHASE1_DETERMINISTIC=PASS
UNMERGED_GRANT_REJECTION=PASS
NETWORK_CALLS=0
FIRESTORE_NETWORK_OPERATIONS=0
EXTERNAL_EFFECTS=0

AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO

REVIEWER_DISPOSITION=PENDING
STOP_CODE=NW008_AT10_RERUN_IMPLEMENTATION_R1_READY_FOR_FINAL_REVIEW
```

## Reviewed implementation scope

- `scripts/nw008/run_at10_bounded_execution.py`
- `tests/test_nw008_at10_bounded_execution.py`
- `proof/nw008/at-10/nw-008-at10-execution-attempt-1-review.md`
- the five preserved execution-attempt-1 proof files under
  `proof/nw008/at-10/acceptance-demo/`

## Bound executor properties

```text
PROJECT=mg-devpost
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs

MAX_DISTINCT_RUN_IDS=4
MAX_DOCUMENT_CREATES=4
MAX_DOCUMENT_READS=12
MAX_DOCUMENT_DELETES=4
MAX_NETWORK_CALLS=20
MAX_EXECUTION_MINUTES=10

FIRESTORE_LIST_AUTHORIZED=NO
FIRESTORE_QUERY_AUTHORIZED=NO
COLLECTION_SWEEP_AUTHORIZED=NO
NO_OUT_OF_BAND_PROBES=YES
SAME_LIFECYCLE_CLEANUP=YES
SAME_EXECUTOR_PROOF_EMISSION=YES
AT10_COMPLETE_HARD_CODED_NO=YES

AUTHORIZATION_DECISION_SHA_REQUIRED=YES
AUTHORIZATION_DECISION_FULL_40_CHAR_SHA_REQUIRED=YES
AUTHORIZATION_DECISION_IS_ANCESTOR_OF_ORIGIN_MAIN_REQUIRED=YES
APPROVED_GRANT_PRESENT_ON_ORIGIN_MAIN_REQUIRED=YES
APPROVED_GRANT_EXACT_BLOB_MATCH_REQUIRED=YES
FIRESTORE_CLIENT_CREATED_BEFORE_MERGED_GRANT_PROVENANCE=NO
```

The exact run allowlist is:

```text
run_nw006_success_001
run_nw006_stage_denied_001
run_nw006_ambiguous_contact_001
run_nw006_failed_001
```

All Firestore create, exact get, and delete calls flow through one gateway and
one pre-call counter. The CLI verifies committed human authority, exact SHA
binding, fixed target, caps, allowlist, source-tree equality, a clean
execution-source worktree, a full authorization decision SHA that is an
ancestor of `origin/main`, and exact approved-grant blob equality at both the
decision commit and live `origin/main` before constructing a Firestore client.

## Offline validation

The focused test suite proves:

- a fifth run ID fails before network activity;
- fifth create, thirteenth read, fifth delete, and twenty-first total operation
  fail before network activity;
- an operation after ten minutes fails before network activity;
- list, query, stream, and sweep surfaces are absent;
- precreate and postdelete exact checks count toward the 12 reads;
- static call-site validation rejects helper bypass of the bounded counter;
- emitted proof counters equal the executor counter;
- an approved but locally committed/unmerged grant is rejected before Firestore
  client construction with zero network calls;
- all emitted completion markers remain `AT10_COMPLETE=NO`.

```text
OFFLINE_TESTS=12
OFFLINE_TESTS_PASSED=12
OFFLINE_VALIDATION_RESULT=PASS
APPROVED_BUT_UNMERGED_AUTHORIZATION_REJECTED=PASS
FIRESTORE_CLIENT_CREATED=NO
NETWORK_CALLS=0
UNMERGED_GRANT_REJECTION=PASS
```

Deterministic Phase 1 validation also passed:

```text
YAML_PARSE=PASS
PACKET_SCHEMA_VALIDATION=PASS
THREE_FIXTURE_OUTCOMES=PASS
REPLAY_IDEMPOTENCY=PASS
MUTATION_INTENT_BOUNDS=PASS
PROOF_RETURN_SCHEMA_VALIDATION=PASS
PHASE1_DETERMINISTIC=PASS
```

## Authority state

PR #53 authority is exhausted and bound to a different execution code SHA. It
must not be reused. A future rerun requires this implementation review to
complete and a separate new human-approved execution authorization artifact
bound to the exact SHA above.

```text
PR53_AUTHORITY_REUSABLE=NO
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```
