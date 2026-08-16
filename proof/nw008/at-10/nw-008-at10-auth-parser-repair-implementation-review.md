# NW-008 AT-10 Auth Parser R1.1 Repair Implementation Review

This packet presents the fail-closed authorization parser repair for formal
implementation review. It does not authorize Firestore execution, activation
of PR #55, or an AT-10 completion claim.

```text
SUPERSEDED_INTERMEDIATE_SUBJECT=7029c7087cad0039c12e65da82dadaecd5dad869

FINAL_IMPLEMENTATION_SUBJECT_SHA=a20becf273c0d65404edb8c4fdeb4ddee37af5e2
FINAL_EXECUTION_CODE_SHA=a20becf273c0d65404edb8c4fdeb4ddee37af5e2
SHA_EQUALITY=PASS

AUTH_PARSER_FAIL_CLOSED=PASS
ACTIVE_GRANT_SCHEMA_COMPLETE=PASS
VALID_ISO8601_DATETIME_ENFORCED=PASS

OFFLINE_TESTS=29
OFFLINE_TESTS_PASSED=29
OFFLINE_VALIDATION_RESULT=PASS
PHASE1_DETERMINISTIC=PASS
GIT_DIFF_CHECK=PASS

NETWORK_CALLS=0
FIRESTORE_NETWORK_OPERATIONS=0
EXTERNAL_EFFECTS=0

AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO

REVIEWER_DISPOSITION=PENDING
STOP_CODE=NW008_AT10_AUTH_PARSER_R1_1_READY_FOR_FORMAL_IMPLEMENTATION_REVIEW
```

## Reviewed implementation scope

- `scripts/nw008/run_at10_bounded_execution.py`
- `tests/test_nw008_at10_bounded_execution.py`

The canonical ACTIVE GRANT now requires explicit authorization for network
operations, Firestore creates, exact reads, and deletes, with every Firestore
operation constrained to the bounded executor. It also requires
synthetic-only data, collection fanout of one, no collection sweep, and
explicit denials for GHL CRM, IAM mutation, secret mutation, Cloud Run, and
real customer data.

The existing list, query, collection sweep, out-of-band Firestore probe, and
PR #53 authority-reuse denials remain mandatory.

After canonical offset-aware ISO format validation, `APPROVED_AT` is parsed as
a datetime. Invalid calendar dates, clock values, UTC offsets, and
timezone-naive timestamps are rejected.

## Offline validation

The focused suite passed all parser regressions and bounded 4/12/4/20
operation tests. The existing pending-block-with-approved-prose,
duplicate-key, multiple-block, and approved-but-unmerged grant cases continue
to reject fail-closed before Firestore client construction.

Deterministic Phase 1 verification passed YAML parsing, packet schema
validation, all three fixture outcomes, replay/idempotency, mutation intent
bounds, and proof-return schema validation.

No Firestore client was constructed and no network operation was executed.
