# NW-008 AT-1 -- Completion Decision 001

```text
DECISION_ID=NW008_AT1_COMPLETION_DECISION_001
DECISION_TYPE=POST_EXECUTION_COMPLETION_DECISION
ARTIFACT_KIND=POST_EXECUTION_COMPLETION_DECISION
OWNER_LANE=VS Code / Orchestrator
BRANCH=decision/nw008-at1-completion-001

SOURCE_RESULT008_SHA=2b901ca234e55952439a3a995e0b1d039e3aea68
SOURCE_RECONCILIATION_COMMIT_SHA=04dca73fcc9862c3e7fa5a88b2fd8aabd0c7312d
SOURCE_RECONCILIATION_MERGE_SHA=ff2bc2a415daa08ae85eff142f55db4e83949b3a
PR68_MERGE_SHA=ff2bc2a415daa08ae85eff142f55db4e83949b3a
AUTHORIZED_GRANT_008_SHA=cd2d25f26c3a07bfb2dcd3beb0c6310d2a592ce2

RECORDED_AT_UTC=2026-08-17T18:45:00Z
NETWORK_TRANSPORT=NO
```

## Disposition

Grant 008 one-shot live synthetic AT-1 execution **occurred**. The
controlling post-execution evidence is the PR #68 reconciliation merged to
main. That reconciliation failed the required AT-1 completion predicates.
Therefore AT-1 is **not complete**, and Grant 008 remains permanently
consumed with no retry and no new GHL authority.

```text
AT1_EXECUTION_OCCURRED=YES

AT1_COMPLETION_RECONCILIATION=FAIL
AT1_COMPLETE=NO

GRANT_008_STATE=CONSUMED
GRANT_008_RETRY_AUTHORIZED=NO
GRANT_008_REAUTHORIZATION_BY_AMENDMENT=NO

RESULT008_STATUS=HISTORICAL_EXECUTION_CLAIM
RESULT008_RECONCILIATION_STATUS=CONTROLLING_POST_EXECUTION_EVIDENCE

BUSINESS_EFFECT_TRUTH=PARTIALLY_UNKNOWN_DUE_TO_MISSING_RESPONSE_EVIDENCE
COMPLETION_FAILURE_CLASS=EXECUTION_PROOF_AND_RUNTIME_CONTRACT_NONCONFORMANCE

NEW_GHL_AUTHORITY=NO
ADDITIONAL_GHL_CALLS_EXECUTED=0
ADDITIONAL_MUTATION_CALLS_EXECUTED=0

NEXT=AT1_LIVE_TRANSPORT_AND_EVIDENCE_CAPTURE_REMEDIATION
```

## Evidence binding

| Role | SHA / artifact | Status |
| --- | --- | --- |
| Contemporaneous execution claim | Result 008 at `2b901ca234e55952439a3a995e0b1d039e3aea68` | HISTORICAL_EXECUTION_CLAIM |
| Controlling post-execution evidence | Reconciliation commit `04dca73fcc9862c3e7fa5a88b2fd8aabd0c7312d` | FAIL / CONTROLLING |
| Durable merge of controlling evidence | PR #68 merge `ff2bc2a415daa08ae85eff142f55db4e83949b3a` | main-reachable |
| Consumed authorization | Grant 008 countersign `cd2d25f26c3a07bfb2dcd3beb0c6310d2a592ce2` | CONSUMED |

Controlling public artifact path:

`proof/nw008/nw-008-at1-live-execution-result-008-reconciliation.md`

## What is decided

1. **Execution occurred.** A Grant 008-scoped live synthetic AT-1 attempt
   ran and produced Result 008 as a contemporaneous claim.
2. **Completion failed.** Required completion predicates from the
   reconciliation are not all YES. Material failures include:
   - `OP3_CREATED_NOTE_ID_VERIFIED=NO`
   - `OP4_NOTE_READBACK_MATCH=NO`
   - `BUSINESS_CALL_COUNT_RECONCILED=NO`
   - multiple other required predicates UNKNOWN due to missing retained
     MCP response bodies
   - `RETRY_USED=YES` against grant no-retry boundary
   - actual wire shape did not match the reviewed serializer
3. **AT1_COMPLETE=NO.** Result 008’s `AT1_COMPLETE=YES` claim is superseded
   by the controlling reconciliation.
4. **Grant 008 is consumed.** No retry, no amendment reauthorization, and
   no new GHL authority are granted by this decision.
5. **Business-effect truth is partially unknown.** Missing response-body
   evidence means this decision does **not** assert that note write
   definitely failed, stage write definitely failed, or that no business
   effect occurred.

## Explicit non-claims

```text
NOTE_WRITE_DEFINITELY_FAILED=NOT_CLAIMED
STAGE_WRITE_DEFINITELY_FAILED=NOT_CLAIMED
NO_BUSINESS_EFFECT_OCCURRED=NOT_CLAIMED
```

## Grant 008 terminal state

```text
GRANT_008_STATE=CONSUMED
GRANT_008_RETRY_AUTHORIZED=NO
GRANT_008_REAUTHORIZATION_BY_AMENDMENT=NO
NEW_GHL_AUTHORITY=NO
OPERATOR_EXECUTION_AUTHORIZED=NO
SELF_ACTIVATION=FORBIDDEN
```

Any future AT-1 live attempt requires a **separate** future authority and
must not treat Grant 008, Result 008, or this decision as execution
authorization.

## Non-actions of this decision unit

```text
DID_NOT_CALL_GHL=YES
DID_NOT_MCP_INITIALIZE=YES
DID_NOT_EXECUTE_OPERATION=YES
DID_NOT_RETRY=YES
DID_NOT_COMPENSATE=YES
DID_NOT_CLEANUP=YES
DID_NOT_CREATE_GRANT009=YES
DID_NOT_IMPLEMENT_REMEDIATION=YES
DID_NOT_MUTATE_RUNTIME=YES
ADDITIONAL_GHL_CALLS_EXECUTED=0
ADDITIONAL_MUTATION_CALLS_EXECUTED=0
```

## Next (planning only; not authorized here)

```text
NEXT=AT1_LIVE_TRANSPORT_AND_EVIDENCE_CAPTURE_REMEDIATION
PLANNING_UNIT_HINT=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_001
```

Remediation objectives are deferred to a separate planning unit and are
**not** authorized for live GHL execution by this decision.

## STOP

```text
STOP_CODE=NW008_AT1_COMPLETION_DECISION_001_RECORDED
DECISION_ID=NW008_AT1_COMPLETION_DECISION_001
AT1_EXECUTION_OCCURRED=YES
AT1_COMPLETION_RECONCILIATION=FAIL
AT1_COMPLETE=NO
GRANT_008_STATE=CONSUMED
GRANT_008_RETRY_AUTHORIZED=NO
NEW_GHL_AUTHORITY=NO
SOURCE_RECONCILIATION_MERGE_SHA=ff2bc2a415daa08ae85eff142f55db4e83949b3a
NEXT=COMPLETION_DECISION_REVIEW
```
