# NW-008 AT-1 -- Pipeline Metadata Verification Grant 003

```text
GRANT_ID=NW008_AT1_PIPELINE_METADATA_VERIFY_003
GRANT_TYPE=READ_ONLY_PIPELINE_METADATA_VERIFICATION
ARTIFACT_KIND=BOUNDED_READ_ONLY_PIPELINE_METADATA_VERIFICATION_GRANT
OWNER_LANE=VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
AUTHORIZED_GRANT_002_SHA=606670cec59ec6366e196ff99d0a1acf7ab10db6
RESULT_002_COMMIT_SHA=897db6e74f1d022260d385a4852269a7bb1d1a49
GRANT_STATE=AUTHORIZED_READ_ONLY_PIPELINE_METADATA_VERIFICATION
SELF_ACTIVATION=FORBIDDEN
```

This grant is narrowly limited to a single, read-only pipeline metadata call.
It carries forward Result 002's private capture of the target pipeline binding
and currently observed pipeline stage. Neither value may be printed, committed,
or otherwise published.

## Frozen authority and caps

```text
PIPELINE_METADATA_LIST_CALLS_MAX=1
CRM_RECORD_READS_MAX=0
MUTATION_CALLS_MAX=0

ALLOWED_EXECUTE_OPERATION_GET_PIPELINES=YES

SEARCH=NO
FETCH=NO
LIST_LOCATIONS=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO

KNOWN_TARGET_PIPELINE_ID_REQUIRED=YES
FILTER_RETURNED_METADATA_TO_TARGET_PIPELINE_ONLY=YES

PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
ENVIRONMENT_READY=NO
```

The sole permitted call is `execute_operation:get-pipelines`, exactly once,
without pagination, search, retry, or fallback. It is authorized only to
inspect the returned metadata locally and filter it to the already privately
bound target pipeline. It does not authorize a general pipeline discovery or
publication of any pipeline or stage ID.

## Bound execution surface

```text
EXECUTION_SURFACE=GHL_ANTHROPIC_V2_MCP
EXECUTION_ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
EXECUTION_OPERATION=execute_operation:get-pipelines
EXECUTION_SURFACE_PREVIOUSLY_PROVEN_BY=897db6e74f1d022260d385a4852269a7bb1d1a49
MCP_PROTOCOL_INITIALIZE_ALLOWED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_METADATA_CALL=NO
GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1
PIPELINE_METADATA_LIST_CALLS_MAX=1
MUTATION_CALLS_MAX=0
```

## Mandatory human countersignature

The human GHL space owner must countersign immediately before execution. The
authorization expires 60 minutes after that countersignature. A missing,
expired, or ambiguous countersignature means no external call is authorized.

```text
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_COUNTERSIGNATURE=APPROVED
HUMAN_APPROVER=THEMG@themiliare-group.com
APPROVED_AT_UTC=2026-08-17T01:15:00Z
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
EXPIRES_AT_UTC=2026-08-17T02:15:00Z
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
```

Required countersignature statement:

```text
I authorize exactly one read-only execute_operation:get-pipelines call under
NW008_AT1_PIPELINE_METADATA_VERIFY_003, bound to baseline
7e5982e2ffe3cd873550f18e8a2f37a97d497e8a, Grant 002
606670cec59ec6366e196ff99d0a1acf7ab10db6, and Result 002
897db6e74f1d022260d385a4852269a7bb1d1a49. The call may be used only to
verify the privately bound target pipeline and its stage metadata. One
authorized final stage may be selected privately. No IDs may be published,
CRM record reads, searches, pagination, retries, fallbacks, or mutations may
occur. This does not authorize AT-1 execution.
```

## Private operator procedure after countersignature

1. Confirm the private target `pipelineId` and the currently observed
   `pipelineStageId` are available from the Result 002 private operator
   evidence. Do not copy either value into this artifact or any public output.
2. Execute `get-pipelines` once. Do not use a cursor, page token, search,
   `fetch`, `list_locations`, retry, or raw REST fallback.
3. In the returned metadata, locate only the private target pipeline and
   discard all other returned pipeline metadata from the verification record.
4. Verify the privately observed current stage exists in that target pipeline.
5. Bind that current stage privately as `expected_initial_stage_id`.
6. The human stage decision selects exactly one different permitted target
   stage from that same pipeline and binds it privately as
   `authorized_final_stage_id`.
7. Record only the sanitized Boolean outcomes in the result artifact. No
   pipeline name, stage name, pipeline ID, stage ID, or raw response belongs
   in public proof.

## Required private decision record

```text
PRIVATE_TARGET_PIPELINE_MATCH=YES|NO
PRIVATE_CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES|NO
PRIVATE_EXPECTED_INITIAL_STAGE_ID_BOUND=YES|NO
PRIVATE_AUTHORIZED_FINAL_STAGE_ID_BOUND=YES|NO
PRIVATE_AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=1
PRIVATE_BINDING_PUBLICATION=NO
```

If the target pipeline or current stage cannot be found, if more than one final
stage is selected, or if the metadata call cannot remain within the frozen
caps, stop without additional calls. Preserve zero mutation authority and
record a fail-closed result with `ENVIRONMENT_READY=NO`.

## Expected authorized-execution result

These are expected outcomes only after the countersigned single-call procedure
and private human stage decision complete successfully. They are not claimed by
this grant.

```text
PIPELINE_METADATA_VERIFIED=YES
CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES
EXPECTED_INITIAL_STAGE_BOUND=YES
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ
AUTHORIZED_FINAL_STAGE_VERIFIED=YES

MUTATION_CALLS_EXECUTED=0
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
ENVIRONMENT_READY=NO
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
```

## STOP after the single permitted call

```text
STOP_CODE=NW008_AT1_PIPELINE_METADATA_VERIFY_003_EXECUTE_ONCE_THEN_STOP
NEXT=PRIVATE_METADATA_VERIFICATION_ONLY_WITHIN_COUNTERSIGNATURE_EXPIRY
RETURN_AFTER_RESULT=LOCATION_POLICY_AND_READINESS_REVIEW
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```
