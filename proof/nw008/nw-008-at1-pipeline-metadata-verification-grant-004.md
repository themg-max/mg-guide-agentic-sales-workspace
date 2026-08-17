# NW-008 AT-1 -- Pipeline Metadata Verification Grant 004

```text
GRANT_ID=NW008_AT1_PIPELINE_METADATA_VERIFY_004
GRANT_TYPE=READ_ONLY_LOCATION_SCOPED_PIPELINE_METADATA_VERIFICATION
ARTIFACT_KIND=BOUNDED_READ_ONLY_LOCATION_SCOPED_PIPELINE_METADATA_VERIFICATION_GRANT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
AUTHORIZED_GRANT_003_SHA=b0bb8fe3d0b80eef3e002345734203066501c22e
RESULT_003_COMPLETED_SHA=5135c7d05612f701db3ac0c3a09e50efb4f8f162
GRANT_STATE=AUTHORIZED_READ_ONLY_LOCATION_SCOPED_PIPELINE_METADATA_VERIFICATION
SELF_ACTIVATION=FORBIDDEN
```

This grant corrects the Grant 003 fail-closed stop
(`GRANT003_GET_PIPELINES_LOCATION_ID_REQUIRED`) by authorizing exactly one
location-scoped `get-pipelines` metadata call. It carries forward Result 002
private current-stage evidence and the private location binding
`NW008_GHL_LOCATION_PRIVATE_V1`. No private identifier may be printed,
committed, or otherwise published.

## Frozen authority and caps

```text
GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1
PIPELINE_METADATA_LIST_CALLS_MAX=1

CRM_RECORD_READS_MAX=0
MUTATION_CALLS_MAX=0

PRIVATE_LOCATION_ID_REQUIRED=YES
PRIVATE_CURRENT_STAGE_ID_REQUIRED=YES
PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LOCATION_PRIVATE_V1

ALLOWED_EXECUTE_OPERATION_GET_PIPELINES=YES

SEARCH=NO
FETCH=NO
LIST_LOCATIONS=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO

PIPELINE_MATCH_RULE=EXACTLY_ONE_PIPELINE_CONTAINS_PRIVATE_CURRENT_STAGE_ID

PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

The sole permitted business call is `execute_operation:get-pipelines`, exactly
once, with the private location id supplied in the operation parameters as
required by the live operation contract. No pagination, search, retry, CRM
record read, mutation, or raw REST fallback is authorized.

## Bound execution surface

```text
EXECUTION_SURFACE=GHL_ANTHROPIC_V2_MCP
EXECUTION_ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
EXECUTION_OPERATION=execute_operation:get-pipelines
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
MCP_PROTOCOL_INITIALIZE_ALLOWED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_METADATA_CALL=NO
GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1
PIPELINE_METADATA_LIST_CALLS_MAX=1
MUTATION_CALLS_MAX=0
```

## Continuity from Grant 003

```text
PRIOR_STOP_CODE=GRANT003_GET_PIPELINES_LOCATION_ID_REQUIRED
PRIOR_RESULT=PIPELINE_METADATA_VERIFICATION_FAILED
PRIOR_GET_PIPELINES_EXECUTION_ATTEMPTS=1
CORRECTION=SUPPLY_PRIVATE_LOCATION_ID_ONCE_UNDER_NEW_GRANT
RETRY_OF_GRANT_003=NO
```

Grant 004 is a new single-attempt authorization. It is not a retry under Grant
003.

## Mandatory human countersignature

The human GHL space owner countersigns immediately before execution. The
authorization expires 60 minutes after this countersignature. A missing,
expired, or ambiguous countersignature means no external call is authorized.

```text
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_COUNTERSIGNATURE=APPROVED
HUMAN_APPROVER=THEMG@themiliare-group.com
APPROVED_AT_UTC=2026-08-17T09:07:57Z
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
EXPIRES_AT_UTC=2026-08-17T10:07:57Z
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
```

Required countersignature statement:

```text
I authorize exactly one read-only execute_operation:get-pipelines call under
NW008_AT1_PIPELINE_METADATA_VERIFY_004, bound to baseline
7e5982e2ffe3cd873550f18e8a2f37a97d497e8a, authorized Grant 003
b0bb8fe3d0b80eef3e002345734203066501c22e, and Result 003 completed
5135c7d05612f701db3ac0c3a09e50efb4f8f162. The call may use the private
locationId from NW008_GHL_LOCATION_PRIVATE_V1 and may match pipelines only by
the privately recovered current stage id from Result 002 evidence. Exactly one
authorized final stage may be selected privately and must differ from the
current stage. Zero retries, zero CRM record reads, zero mutations, and no
publication of location, pipeline, or stage identifiers are permitted. This
does not authorize AT-1 execution.
```

## Private operator procedure after countersignature

1. Confirm private `locationId` from `NW008_GHL_LOCATION_PRIVATE_V1` without
   publishing it.
2. Recover private `current_stage_id` from Result 002 private operator evidence
   without publishing it.
3. Resolve direct GHL PIT from Secret Manager secret `GHL_MCP_PRIVATE_TOKEN`
   in project `ai-rolodex-to-crm`. Do not print the token.
4. MCP `initialize` once on the anthropic_v2 endpoint (does not count as the
   metadata call).
5. Execute `tools/call` → `execute_operation` / `get-pipelines` exactly once
   with the private locationId in operation parameters. No retry.
6. In memory only, find all returned pipelines that contain
   `PRIVATE_CURRENT_STAGE_ID`.
7. Require `MATCH_COUNT=1`. If not, stop with
   `GRANT004_CURRENT_STAGE_PIPELINE_MATCH_NOT_UNIQUE` and make no further API
   call.
8. If unique, privately bind `target_pipeline_id`, verify the current stage
   exists, and bind it as `expected_initial_stage_id`.
9. On the private operator surface, show only that target pipeline's stages.
   The human/owner lane selects exactly one different permitted final stage
   and binds it as `authorized_final_stage_id`. Do not auto-pick first, next,
   or adjacent stage by positional default.
10. Record only sanitized Boolean outcomes in the public result artifact.

## Required private decision record

```text
PRIVATE_LOCATION_ID_USED=YES|NO
PRIVATE_TARGET_PIPELINE_MATCH=YES|NO
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=0|1|>1
CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES|NO
EXPECTED_INITIAL_STAGE_BOUND=YES|NO
AUTHORIZED_FINAL_STAGE_VERIFIED=YES|NO
AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=0|1
PRIVATE_BINDING_PUBLICATION=NO
```

## Expected authorized-execution result

These are expected outcomes only after the countersigned single-call procedure
and private final-stage decision complete successfully. They are not claimed by
this grant.

```text
RESULT=PIPELINE_METADATA_VERIFIED

DIRECT_GHL_SECRET_SOURCE_RESOLVED=YES
GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1
PRIVATE_LOCATION_ID_USED=YES
PRIVATE_TARGET_PIPELINE_MATCH=YES
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=1
CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES
EXPECTED_INITIAL_STAGE_BOUND=YES
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ
AUTHORIZED_FINAL_STAGE_VERIFIED=YES
AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=1
CRM_RECORD_READS_EXECUTED=0
MUTATION_CALLS_EXECUTED=0
PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Explicit non-actions

```text
DID_NOT_AUTHORIZE_CRM_RECORD_READS=YES
DID_NOT_AUTHORIZE_SEARCH=YES
DID_NOT_AUTHORIZE_FETCH=YES
DID_NOT_AUTHORIZE_LIST_LOCATIONS=YES
DID_NOT_AUTHORIZE_PAGINATION=YES
DID_NOT_AUTHORIZE_RETRY=YES
DID_NOT_AUTHORIZE_RAW_REST_FALLBACK=YES
DID_NOT_AUTHORIZE_MUTATIONS=YES
DID_NOT_AUTHORIZE_AT1_EXECUTION=YES
DID_NOT_AUTHORIZE_PRIVATE_BINDING_PUBLICATION=YES
DID_NOT_AUTHORIZE_ENVIRONMENT_READY=YES
```

## STOP after the single permitted call

```text
STOP_CODE=NW008_AT1_PIPELINE_METADATA_VERIFY_004_EXECUTE_ONCE_THEN_STOP
NEXT=PRIVATE_METADATA_VERIFICATION_ONLY_WITHIN_COUNTERSIGNATURE_EXPIRY
RETURN_AFTER_RESULT=LOCATION_POLICY_AND_READINESS_REVIEW
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```
