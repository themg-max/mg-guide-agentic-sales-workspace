# NW-008 AT-1 -- Pipeline Metadata Verification Result 003 Completed

```text
GRANT_ID=NW008_AT1_PIPELINE_METADATA_VERIFY_003
AUTHORIZED_GRANT_003_SHA=b0bb8fe3d0b80eef3e002345734203066501c22e
ARTIFACT_KIND=BOUNDED_READ_ONLY_PIPELINE_METADATA_VERIFICATION_RESULT
OWNER_LANE=VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
AUTHORIZED_GRANT_002_SHA=606670cec59ec6366e196ff99d0a1acf7ab10db6
RESULT_002_COMMIT_SHA=897db6e74f1d022260d385a4852269a7bb1d1a49
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED
STOP_CODE=GRANT003_GET_PIPELINES_LOCATION_ID_REQUIRED
RECORDED_AT_UTC=2026-08-17T01:40:08Z
```

## Disposition

Direct GHL PIT resolution from Secret Manager succeeded. Result 002 private
current-stage evidence was available without publication. Exactly one
`execute_operation:get-pipelines` call was executed on the proven anthropic_v2
surface. The MCP transport returned HTTP 200; the operation payload reported
failure because `locationId` was required and was not supplied. Grant 003
forbids retry, pagination, raw REST fallback, CRM record reads, and mutations,
so execution stopped fail-closed after that single attempt.

```text
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED

DIRECT_GHL_SECRET_SOURCE_RESOLVED=YES
DIRECT_GHL_PIT_PRESENT=YES
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm

PRIVATE_PIPELINE_ID_PRESENT=NO
PRIVATE_CURRENT_STAGE_ID_PRESENT=YES
PRIVATE_LOCATION_ID_PRESENT=YES
PRIVATE_BINDING_PUBLICATION=NO

GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1
MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_METADATA_CALL=NO

PIPELINE_METADATA_VERIFIED=NO
PRIVATE_TARGET_PIPELINE_MATCH=NO
PRIVATE_CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=NO

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
INIT_HTTP=200
GET_PIPELINES_TRANSPORT_HTTP=200
GET_PIPELINES_OPERATION_SUCCESS=NO
GET_PIPELINES_OPERATION_STATUS=422
GET_PIPELINES_FAILURE_CLASS=LOCATION_ID_REQUIRED
FAILURE_MESSAGE_SANITIZED=locationId can't be undefined
```

Local inventory for `get-pipelines` previously showed no required parameters.
The live operation rejected the call without an explicit `locationId`. A private
location id is present from the NW-013 synthetic binding control plane, but
Grant 003 freezes `GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1` and `RETRY=NO`, so
no corrected second call was made.

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
```

## Continuity notes

1. Prior blocked attempt
   `nw-008-at1-pipeline-metadata-verification-result-003-executed.md` remains
   unaltered as the credential-unavailable pre-execution record.
2. This completed continuation resolves the direct GHL PIT and executes the one
   permitted metadata call, then stops on the first API failure.
3. A future grant would need to authorize at most one corrected
   `get-pipelines` call with private `locationId` binding if metadata
   verification is still required. That is out of scope for Grant 003.

## STOP

```text
STOP_CODE=GRANT003_GET_PIPELINES_LOCATION_ID_REQUIRED
RESULT=PIPELINE_METADATA_VERIFICATION_FAILED
PIPELINE_METADATA_VERIFIED=NO
GET_PIPELINES_EXECUTION_ATTEMPTS=1
MUTATION_CALLS_EXECUTED=0
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=LOCATION_POLICY_AND_TRACK_A_READINESS_REVIEW
```
