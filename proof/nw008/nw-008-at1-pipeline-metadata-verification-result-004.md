# NW-008 AT-1 -- Pipeline Metadata Verification Result 004

```text
GRANT_ID=NW008_AT1_PIPELINE_METADATA_VERIFY_004
AUTHORIZED_GRANT_004_SHA=4bbf4fe2851beb79927add8a8f58378b974843d8
ARTIFACT_KIND=BOUNDED_READ_ONLY_LOCATION_SCOPED_PIPELINE_METADATA_VERIFICATION_RESULT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
AUTHORIZED_GRANT_003_SHA=b0bb8fe3d0b80eef3e002345734203066501c22e
RESULT_003_COMPLETED_SHA=5135c7d05612f701db3ac0c3a09e50efb4f8f162
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED
STOP_CODE=GRANT004_GET_PIPELINES_LOCATION_TOKEN_ACCESS_DENIED
RECORDED_AT_UTC=2026-08-17T09:14:20Z
```

## Disposition

Direct GHL PIT resolution from Secret Manager succeeded. Private location binding
`NW008_GHL_LOCATION_PRIVATE_V1` and Result 002 private current-stage evidence were
available without publication. Within the Grant 004 countersignature window,
exactly one `execute_operation:get-pipelines` call was executed on the proven
anthropic_v2 surface with the private location id supplied in operation query
parameters.

The MCP transport returned HTTP 200. The operation payload reported failure
because the token does not have access to the supplied location. Grant 004
freezes `GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1` and `RETRY=NO`, so execution
stopped fail-closed after that single attempt. No second call, CRM record read,
mutation, search, pagination, or raw REST fallback was performed.

```text
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED

DIRECT_GHL_SECRET_SOURCE_RESOLVED=YES
DIRECT_GHL_PIT_PRESENT=YES
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm

PRIVATE_LOCATION_ID_USED=YES
PRIVATE_CURRENT_STAGE_ID_PRESENT=YES
PRIVATE_TARGET_PIPELINE_MATCH=NO
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=0
PRIVATE_BINDING_PUBLICATION=NO

GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1
MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_METADATA_CALL=NO

CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=NO

EXPECTED_INITIAL_STAGE_BOUND=NO
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ
AUTHORIZED_FINAL_STAGE_VERIFIED=NO
AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=0

CRM_RECORD_READS_EXECUTED=0
MUTATION_CALLS_EXECUTED=0
SEARCH_CALLS_EXECUTED=0
FETCH_CALLS_EXECUTED=0
LIST_LOCATIONS_CALLS_EXECUTED=0
PAGINATION_USED=NO
RETRY_USED=NO
RAW_REST_FALLBACK_USED=NO

ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Execution surface (sanitized)

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
OPERATION=execute_operation:get-pipelines
LOCATION_SCOPED_PARAMS=YES
INIT_HTTP=200
GET_PIPELINES_TRANSPORT_HTTP=200
GET_PIPELINES_OPERATION_SUCCESS=NO
GET_PIPELINES_OPERATION_STATUS=403
GET_PIPELINES_FAILURE_CLASS=LOCATION_TOKEN_ACCESS_DENIED
FAILURE_MESSAGE_SANITIZED=token does not have access to this location
```

## Caps compliance

| Cap / rule | Required | Observed |
| --- | --- | --- |
| `PIPELINE_METADATA_LIST_CALLS_MAX` | 1 | 1 |
| `GET_PIPELINES_EXECUTION_ATTEMPTS_MAX` | 1 | 1 |
| `CRM_RECORD_READS_MAX` | 0 | 0 |
| `MUTATION_CALLS_MAX` | 0 | 0 |
| `SEARCH` | NO | not called |
| `FETCH` | NO | not called |
| `LIST_LOCATIONS` | NO | not called |
| `PAGINATION` | NO | not used |
| `RETRY` | NO | not used |
| `RAW_REST_FALLBACK` | NO | not used |
| private binding publication | NO | no IDs or payloads published |
| MG MCP proxy credential | FORBIDDEN | not used |
| credential create/modify | FORBIDDEN | not performed |

## Explicit non-actions

```text
DID_NOT_CALL_SEARCH=YES
DID_NOT_CALL_FETCH=YES
DID_NOT_CALL_LIST_LOCATIONS=YES
DID_NOT_CALL_GET_CONTACT=YES
DID_NOT_CALL_GET_OPPORTUNITY=YES
DID_NOT_PAGINATE=YES
DID_NOT_RETRY_GET_PIPELINES=YES
DID_NOT_RAW_REST_FALLBACK=YES
DID_NOT_EXECUTE_CREATE_NOTE=YES
DID_NOT_EXECUTE_GET_NOTE=YES
DID_NOT_EXECUTE_UPDATE_OPPORTUNITY=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_MODIFY_CREDENTIALS=YES
DID_NOT_PUBLISH_PRIVATE_BINDING_IDS=YES
DID_NOT_AUTHORIZE_AT1_EXECUTION=YES
DID_NOT_CLAIM_ENVIRONMENT_READY=YES
```

## Continuity notes

1. Grant 003 stopped on `locationId can't be undefined` after one unscoped
   `get-pipelines` call.
2. Grant 004 authorized exactly one corrected location-scoped call and executed
   it once with private location binding.
3. The live operation rejected the token/location pairing with HTTP 403 operation
   status. Because retry is forbidden, no alternate location, parameter shape,
   or second metadata call was attempted.
4. Expected-initial and authorized-final stage bindings remain unbound.
5. Any future attempt requires a new grant, a validated private location that the
   direct GHL PIT can access, and a fresh countersignature.

## STOP

```text
STOP_CODE=GRANT004_GET_PIPELINES_LOCATION_TOKEN_ACCESS_DENIED
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED
PIPELINE_METADATA_VERIFIED=NO
GET_PIPELINES_EXECUTION_ATTEMPTS=1
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=0
EXPECTED_INITIAL_STAGE_BOUND=NO
AUTHORIZED_FINAL_STAGE_VERIFIED=NO
MUTATION_CALLS_EXECUTED=0
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=LOCATION_POLICY_AND_TRACK_A_READINESS_REVIEW
```
