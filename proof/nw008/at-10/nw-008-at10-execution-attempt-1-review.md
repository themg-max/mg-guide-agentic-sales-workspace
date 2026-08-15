# NW-008 AT-10 — Execution Attempt 1 Review

This artifact preserves the result of execution attempt 1 without accepting it
as AT-10 completion proof or as authority for another Firestore execution.

```text
EXECUTION_ATTEMPT=1
FUNCTIONAL_RESULT=PASS
CLEANUP_RESULT=PASS
GOVERNANCE_RESULT=CONTRADICTORY_EVIDENCE

AUTHORIZED_EXECUTION_CODE_SHA=156cc85679cf87733f1a8a0b1d0a3a8340994fdd
ACTUAL_EXECUTION_CODE=session-local run_at10_bounded_execution.py
ACTUAL_EXECUTION_CODE_CONTAINED_IN_AUTHORIZED_SUBJECT=NO

AUTHORIZED_MAX_NETWORK_CALLS=20
PRE_RUN_FIRESTORE_GETS=1
RUNNER_COUNTED_FIRESTORE_OPERATIONS=20
POST_RUN_FIRESTORE_GETS=4
MINIMUM_OBSERVED_FIRESTORE_OPERATIONS=25
NETWORK_OPERATION_BOUND_SATISFIED=NO

PR53_AUTHORITY_REUSABLE=NO
ATTEMPT_1_PROOF_ACCEPTED_AS_AT10_COMPLETION_PROOF=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```

## Preserved proof

The five files under `proof/nw008/at-10/acceptance-demo/` are preserved as the
raw proof emitted by attempt 1. Their functional and cleanup results remain
evidence of what occurred, but any embedded authorization conclusion is
superseded by this review's contradictory-evidence finding.

The contradiction requires a new repository-owned runner, new implementation
subject SHA, separate implementation review, and separate future execution
authorization before any rerun.

```text
EXECUTION_ATTEMPT_1_RECONCILED=YES
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
AT10_COMPLETE=NO
```
