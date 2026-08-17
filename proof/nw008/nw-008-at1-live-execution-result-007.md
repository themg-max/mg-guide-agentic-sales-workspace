# NW-008 AT-1 -- Live Execution Result 007

```text
GRANT_ID=NW008_AT1_LIVE_EXECUTION_007
AUTHORIZED_GRANT_007_SHA=86b8d6503274e89a7a018be844e135fbd1fe57c6
ARTIFACT_KIND=ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION_RESULT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
AUTHORIZED_DRAFT_SHA=9051679699e981ce60aefb37716a470bb336b0a9
TRACK_A_CLOSEOUT_SHA=57f4fd390ba0705fb819a36028e6db02d4f1c09e
MERGED_AT1_EXECUTOR_SHA=998564cdfac6c24d5a414289798979a7f6220082
APPROVED_AT_UTC=2026-08-17T11:38:17Z
EXPIRES_AT_UTC=2026-08-17T12:38:17Z
RUN_STARTED_AT_UTC=2026-08-17T11:40:21Z
RUN_FINISHED_AT_UTC=2026-08-17T11:40:22Z
RECORDED_AT_UTC=2026-08-17T11:41:18Z
```

## Disposition

One countersigned live synthetic AT-1 attempt was executed under Grant 007 using
the reviewed bounded AT-1 executor
(`998564cdfac6c24d5a414289798979a7f6220082`) with a live MCP transport limited to the
authorized operation surface. Authorization commit
`86b8d6503274e89a7a018be844e135fbd1fe57c6` predates the first GHL business call. The
authorization window remained valid at run start.

Fresh precondition reads succeeded:

- exact synthetic contact binding verified
- exact synthetic opportunity binding verified
- live location exact
- target pipeline exact
- contact/opportunity relationship exact
- current stage matched expected initial stage

`EXPECTED_INITIAL_STAGE_VERIFIED=YES` from those fresh reads.

The single authorized `create-note` dispatch was attempted and rejected. Per
frozen grant semantics the run stopped terminal with no stage write, no retry,
no compensating mutation, no alternate operation, and no raw REST fallback.

```text
EXECUTION_RESULT=AT1_LIVE_SYNTHETIC_EXECUTION_FAILED_NOTE_WRITE_REJECTED
EXECUTOR_DISPOSITION=failed
EXECUTOR_FAILURE_CODE=NOTE_WRITE_REJECTED
STOP_CODE=NW008_AT1_LIVE_EXECUTION_007_TERMINAL_NOTE_WRITE_REJECTED

EXPECTED_INITIAL_STAGE_VERIFIED=YES

TOTAL_GHL_CALLS_EXECUTED=3

NOTE_WRITE_ATTEMPTS=1
NOTE_WRITES_SUCCEEDED=0
NOTE_READBACK_VERIFIED=NO

STAGE_WRITE_ATTEMPTS=0
STAGE_WRITES_SUCCEEDED=0
FINAL_STAGE_READBACK_VERIFIED=NO

SEARCH_CALLS_EXECUTED=0
LIST_CALLS_EXECUTED=0
PAGINATION_USED=NO
RETRY_USED=NO
RAW_REST_FALLBACK_USED=NO
COMPENSATING_MUTATION_USED=NO

PRIVATE_BINDING_PUBLICATION=NO
AT1_COMPLETE=NO
```

## Execution surface (sanitized)

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_BUSINESS_CALL=NO
INIT_HTTP=200
BOUNDED_EXECUTOR=src/integrations/ghl/bounded_at1_executor.py
BOUNDED_EXECUTOR_SHA=998564cdfac6c24d5a414289798979a7f6220082
BUSINESS_OPERATION_ORDER_OBSERVED=get-contact,get-opportunity,create-note
CREATE_NOTE_TRANSPORT_HTTP=200
```

## Caps compliance

| Cap / rule | Required | Observed |
| --- | --- | --- |
| authorization commit before first business call | YES | YES |
| authorization window valid at start | YES | YES |
| modeled total GHL business calls max | 6 | 3 |
| note write attempts max | 1 | 1 |
| stage write attempts max | 1 | 0 |
| search | NO | 0 |
| list | NO | 0 |
| pagination | NO | NO |
| retry | NO | NO |
| raw REST fallback | NO | NO |
| compensating mutation | NO | NO |
| automatic cleanup | NO | NO |
| private binding publication | NO | NO |
| non-synthetic mutation | NO | NO |

## Explicit non-actions after terminal note rejection

```text
DID_NOT_RETRY_CREATE_NOTE=YES
DID_NOT_EXECUTE_GET_NOTE=YES
DID_NOT_EXECUTE_UPDATE_OPPORTUNITY=YES
DID_NOT_EXECUTE_FINAL_GET_OPPORTUNITY=YES
DID_NOT_SEARCH=YES
DID_NOT_LIST=YES
DID_NOT_PAGINATE=YES
DID_NOT_RAW_REST_FALLBACK=YES
DID_NOT_COMPENSATING_MUTATION=YES
DID_NOT_AUTOMATIC_CLEANUP=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_PUBLISH_PRIVATE_BINDING_IDS=YES
DID_NOT_CLAIM_AT1_COMPLETE=YES
```

## Continuity notes

1. Grant 007 countersignature authorized exactly one live synthetic AT-1 path.
2. Fresh pre-write reads verified expected initial stage and synthetic bindings.
3. Note write consumed the single attempt budget and failed closed.
4. Stage write attempt budget remains unconsumed (`STAGE_WRITE_ATTEMPTS=0`).
5. `AT1_COMPLETE` remains `NO` because the authorized path did not fully succeed
   with both readbacks verified.

## STOP

```text
STOP_CODE=NW008_AT1_LIVE_EXECUTION_007_TERMINAL_NOTE_WRITE_REJECTED
EXECUTION_RESULT=AT1_LIVE_SYNTHETIC_EXECUTION_FAILED_NOTE_WRITE_REJECTED
AUTHORIZED_GRANT_007_SHA=86b8d6503274e89a7a018be844e135fbd1fe57c6
TOTAL_GHL_CALLS_EXECUTED=3
EXPECTED_INITIAL_STAGE_VERIFIED=YES
NOTE_WRITE_ATTEMPTS=1
NOTE_WRITES_SUCCEEDED=0
NOTE_READBACK_VERIFIED=NO
STAGE_WRITE_ATTEMPTS=0
STAGE_WRITES_SUCCEEDED=0
FINAL_STAGE_READBACK_VERIFIED=NO
RETRY_USED=NO
COMPENSATING_MUTATION_USED=NO
PRIVATE_BINDING_PUBLICATION=NO
AT1_COMPLETE=NO
NEXT=HUMAN_REVIEW_OF_NOTE_WRITE_REJECTION_NO_AUTOMATIC_RETRY
```
