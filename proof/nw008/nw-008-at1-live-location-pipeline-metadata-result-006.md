# NW-008 AT-1 -- Live Location Pipeline Metadata Result 006

```text
GRANT_ID=NW008_AT1_LIVE_LOCATION_PIPELINE_METADATA_VERIFY_006
AUTHORIZED_GRANT_006_SHA=8a2ef895c8815c409284f4b8ebf0a211390a8a57
ARTIFACT_KIND=BOUNDED_READ_ONLY_LIVE_LOCATION_PIPELINE_METADATA_VERIFICATION_RESULT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
RESULT_005_SHA=747bf4260afba03af49b6b3b0248d664c39a641d
AUTHORIZED_GRANT_005_SHA=8759eafc127ab9b12761eaedeb47f92c7f9bc491
LIVE_LOCATION_EXCEPTION_SHA=85f95e9c55a053b44c48ede5aa86dd4e71f4638a
RESULT=LIVE_LOCATION_PIPELINE_METADATA_VERIFIED
RECORDED_AT_UTC=2026-08-17T10:32:18Z
```

## Disposition

Direct GHL PIT resolution from Secret Manager succeeded. Private live-location
binding `NW008_GHL_LIVE_LOCATION_PRIVATE_V2`, private pipeline binding
`NW008_GHL_PIPELINE_PRIVATE_V1`, and private current-stage binding
`NW008_GHL_CURRENT_STAGE_PRIVATE_V1` were loaded from the private control plane
without publication. Within the Grant 006 countersignature window, MCP
`initialize` completed and exactly one `execute_operation:get-pipelines` call
was executed on the proven anthropic_v2 surface with the private live location
id supplied in operation query parameters.

The MCP transport returned HTTP 200. Returned pipeline metadata was filtered in
memory to the private target pipeline id. Exact match count was 1. The private
current stage exists in that target pipeline and was bound as
`expected_initial_stage_id`. On the private operator surface, only that target
pipeline's stages were considered. Exactly one different permitted final stage
was selected and bound as `authorized_final_stage_id`.

No CRM record read, mutation, search, pagination, retry, or raw REST fallback
was performed. No private identifiers were published.

```text
RESULT=LIVE_LOCATION_PIPELINE_METADATA_VERIFIED

DIRECT_GHL_SECRET_SOURCE_RESOLVED=YES
DIRECT_GHL_PIT_PRESENT=YES
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm

GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1

LIVE_LOCATION_BINDING_VERIFIED=YES
PRIVATE_LOCATION_ID_USED=YES
PRIVATE_TARGET_PIPELINE_MATCH=YES
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=1

CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES

EXPECTED_INITIAL_STAGE_BOUND=YES
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ

AUTHORIZED_FINAL_STAGE_VERIFIED=YES
AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=1
FINAL_STAGE_DIFFERS_FROM_INITIAL_STAGE=YES

CRM_RECORD_READS_EXECUTED=0
MUTATION_CALLS_EXECUTED=0

PRIVATE_BINDING_PUBLICATION=NO

READ_ONLY_ENVIRONMENT_VERIFIED=YES
AT1_WRITE_CREDENTIAL_READY=UNKNOWN_PENDING_SCOPE_VERIFICATION

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
PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
PRIVATE_PIPELINE_BINDING_REF=NW008_GHL_PIPELINE_PRIVATE_V1
PRIVATE_CURRENT_STAGE_BINDING_REF=NW008_GHL_CURRENT_STAGE_PRIVATE_V1
MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_METADATA_CALL=NO
INIT_HTTP=200
GET_PIPELINES_TRANSPORT_HTTP=200
GET_PIPELINES_OPERATION_SUCCESS=YES
SEARCH_CALLS_EXECUTED=0
FETCH_CALLS_EXECUTED=0
LIST_LOCATIONS_CALLS_EXECUTED=0
PAGINATION_USED=NO
RETRY_USED=NO
RAW_REST_FALLBACK_USED=NO
```

## Caps compliance

| Cap / rule | Required | Observed |
| --- | --- | --- |
| `GET_PIPELINES_EXECUTION_ATTEMPTS_MAX` | 1 | 1 |
| `PIPELINE_METADATA_LIST_CALLS_MAX` | 1 | 1 |
| `CRM_RECORD_READS_MAX` | 0 | 0 |
| `MUTATION_CALLS_MAX` | 0 | 0 |
| `PRIVATE_TARGET_PIPELINE_MATCH_COUNT_REQUIRED` | 1 | 1 |
| `FINAL_STAGE_MUST_DIFFER_FROM_INITIAL_STAGE` | YES | YES |
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

1. Result 005 established exact synthetic opportunity access with
   `LOCATION_BINDING_MATCH=NO` against `NW008_GHL_LOCATION_PRIVATE_V1`.
2. The live-location synthetic-only exception superseded the isolated-location
   prerequisite and rebound NW-008 to `NW008_GHL_LIVE_LOCATION_PRIVATE_V2`.
3. Grant 006 authorized exactly one location-scoped `get-pipelines` call against
   that live location and completed successfully under the synthetic-only
   boundary.
4. Expected-initial stage is bound from the private current-stage binding and
   still requires a fresh pre-execution read before any future AT-1 write
   authorization.
5. Authorized-final stage is bound privately as exactly one non-initial stage
   selected on the private operator surface.
6. `AT1_WRITE_CREDENTIAL_READY` remains unknown pending separate scope
   verification. `ENVIRONMENT_READY=NO` and `AT1_EXECUTION_AUTHORIZED=NO`.

## STOP

```text
STOP_CODE=NW008_AT1_LIVE_LOCATION_PIPELINE_METADATA_VERIFY_006_COMPLETE
RESULT=LIVE_LOCATION_PIPELINE_METADATA_VERIFIED
GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1
LIVE_LOCATION_BINDING_VERIFIED=YES
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=1
EXPECTED_INITIAL_STAGE_BOUND=YES
AUTHORIZED_FINAL_STAGE_VERIFIED=YES
READ_ONLY_ENVIRONMENT_VERIFIED=YES
AT1_WRITE_CREDENTIAL_READY=UNKNOWN_PENDING_SCOPE_VERIFICATION
MUTATION_CALLS_EXECUTED=0
PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=AT1_WRITE_SCOPE_AND_ENVIRONMENT_READYNESS_REVIEW
```
