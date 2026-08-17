# NW-008 AT-1 -- Live Location Pipeline Metadata Grant 006

```text
GRANT_ID=NW008_AT1_LIVE_LOCATION_PIPELINE_METADATA_VERIFY_006
GRANT_TYPE=READ_ONLY_LIVE_LOCATION_PIPELINE_METADATA_VERIFICATION
ARTIFACT_KIND=BOUNDED_READ_ONLY_LIVE_LOCATION_PIPELINE_METADATA_VERIFICATION_GRANT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness

RESULT_005_SHA=747bf4260afba03af49b6b3b0248d664c39a641d
AUTHORIZED_GRANT_005_SHA=8759eafc127ab9b12761eaedeb47f92c7f9bc491
LIVE_LOCATION_EXCEPTION_SHA=85f95e9c55a053b44c48ede5aa86dd4e71f4638a

TARGET_LOCATION_CLASS=BUSINESS_ACTIVE_GHL_LOCATION
LIVE_LOCATION_EXCEPTION_VERIFIED=YES
SYNTHETIC_ONLY_BOUNDARY_REQUIRED=YES

PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
PRIVATE_PIPELINE_BINDING_REF=NW008_GHL_PIPELINE_PRIVATE_V1
PRIVATE_CURRENT_STAGE_BINDING_REF=NW008_GHL_CURRENT_STAGE_PRIVATE_V1

GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1
PIPELINE_METADATA_LIST_CALLS_MAX=1
CRM_RECORD_READS_MAX=0
MUTATION_CALLS_MAX=0

ALLOWED_OPERATION_GET_PIPELINES=YES

SEARCH=NO
FETCH=NO
LIST_LOCATIONS=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO

FILTER_RETURNED_METADATA_TO_PRIVATE_PIPELINE_ID=YES
PRIVATE_TARGET_PIPELINE_MATCH_COUNT_REQUIRED=1
FINAL_STAGE_MUST_DIFFER_FROM_INITIAL_STAGE=YES

PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO

GRANT_STATE=AUTHORIZED_READ_ONLY_LIVE_LOCATION_PIPELINE_METADATA_VERIFICATION
SELF_ACTIVATION=FORBIDDEN
```

## Continuity

This grant continues from:

1. Result 005 exact-opportunity diagnostic
   (`747bf4260afba03af49b6b3b0248d664c39a641d`) which proved current PIT access
   to the synthetic opportunity and privately captured returned location,
   pipeline, and stage identifiers with `LOCATION_BINDING_MATCH=NO` against
   `NW008_GHL_LOCATION_PRIVATE_V1`.
2. Live-location synthetic-only exception
   (`85f95e9c55a053b44c48ede5aa86dd4e71f4638a`) which supersedes the
   unattainable isolated-test-location prerequisite and rebinds NW-008 privately
   to `NW008_GHL_LIVE_LOCATION_PRIVATE_V2`.
3. Authorized Grant 005
   (`8759eafc127ab9b12761eaedeb47f92c7f9bc491`) as the prior bounded diagnostic
   authority.

No private identifier may be printed, committed, or otherwise published.

## Frozen authority and caps

```text
GET_PIPELINES_EXECUTION_ATTEMPTS_MAX=1
PIPELINE_METADATA_LIST_CALLS_MAX=1
CRM_RECORD_READS_MAX=0
MUTATION_CALLS_MAX=0

ALLOWED_OPERATION_GET_PIPELINES=YES
SEARCH=NO
FETCH=NO
LIST_LOCATIONS=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO

PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
PRIVATE_PIPELINE_BINDING_REF=NW008_GHL_PIPELINE_PRIVATE_V1
PRIVATE_CURRENT_STAGE_BINDING_REF=NW008_GHL_CURRENT_STAGE_PRIVATE_V1

FILTER_RETURNED_METADATA_TO_PRIVATE_PIPELINE_ID=YES
PRIVATE_TARGET_PIPELINE_MATCH_COUNT_REQUIRED=1
FINAL_STAGE_MUST_DIFFER_FROM_INITIAL_STAGE=YES

PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

The sole permitted business call is `execute_operation:get-pipelines`, exactly
once, with the private live location id from
`NW008_GHL_LIVE_LOCATION_PRIVATE_V2` supplied in the operation parameters. No
pagination, search, retry, CRM record read, mutation, or raw REST fallback is
authorized.

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

## Mandatory human countersignature

The human GHL space owner countersigns immediately before execution. The
authorization expires 60 minutes after this countersignature. A missing,
expired, or ambiguous countersignature means no external call is authorized.

```text
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_COUNTERSIGNATURE=APPROVED
HUMAN_APPROVER=THEMG@themiliare-group.com
APPROVED_AT_UTC=2026-08-17T10:28:45Z
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
EXPIRES_AT_UTC=2026-08-17T11:28:45Z
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
GRANT_STATE=AUTHORIZED_READ_ONLY_LIVE_LOCATION_PIPELINE_METADATA_VERIFICATION
```

Required countersignature statement:

```text
I authorize exactly one read-only execute_operation:get-pipelines call under
NW008_AT1_LIVE_LOCATION_PIPELINE_METADATA_VERIFY_006, bound to Result 005
747bf4260afba03af49b6b3b0248d664c39a641d, authorized Grant 005
8759eafc127ab9b12761eaedeb47f92c7f9bc491, and live-location synthetic-only
exception 85f95e9c55a053b44c48ede5aa86dd4e71f4638a.

I acknowledge that:
- the target is a business-active live GHL location (non-isolated);
- the synthetic-only exception is active;
- exactly one get-pipelines call is authorized;
- only the exact private location/pipeline/stage bindings
  NW008_GHL_LIVE_LOCATION_PRIVATE_V2 / NW008_GHL_PIPELINE_PRIVATE_V1 /
  NW008_GHL_CURRENT_STAGE_PRIVATE_V1 may be used;
- no customer-record mutation is authorized;
- no retry or pagination is authorized;
- this does not authorize AT-1 execution.

Zero CRM record reads, zero mutations, and no publication of location,
pipeline, or stage identifiers are permitted.
```

## Private operator procedure after countersignature

1. Confirm private live location id from
   `NW008_GHL_LIVE_LOCATION_PRIVATE_V2` without publishing it.
2. Confirm private target pipeline id from
   `NW008_GHL_PIPELINE_PRIVATE_V1` and private current stage id from
   `NW008_GHL_CURRENT_STAGE_PRIVATE_V1` without publishing them.
3. Resolve direct GHL PIT from Secret Manager secret `GHL_MCP_PRIVATE_TOKEN`
   in project `ai-rolodex-to-crm`. Do not print the token.
4. MCP `initialize` once on the anthropic_v2 endpoint (does not count as the
   metadata call).
5. Execute `tools/call` → `execute_operation` / `get-pipelines` exactly once
   with the private live location id in operation parameters. No retry.
6. In memory only, filter returned metadata to
   `NW008_GHL_PIPELINE_PRIVATE_V1`.
7. Require `PRIVATE_TARGET_PIPELINE_MATCH_COUNT=1`. If not, stop with
   `GRANT006_PRIVATE_PIPELINE_MATCH_NOT_EXACTLY_ONE` and make no further API
   call.
8. Verify `NW008_GHL_CURRENT_STAGE_PRIVATE_V1` exists in the target pipeline
   and bind it as `expected_initial_stage_id`.
9. Set `EXPECTED_INITIAL_STAGE_BOUND=YES` and
   `EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ`.
10. On the private operator surface, show only that target pipeline's stages.
    The human/owner lane selects exactly one different permitted final stage
    and binds it as `authorized_final_stage_id`. Do not auto-pick first, next,
    or adjacent stage by positional default.
11. Require `AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=1` and
    `FINAL_STAGE_DIFFERS_FROM_INITIAL_STAGE=YES`.
12. Record only sanitized Boolean outcomes in the public result artifact.

## Required private decision record

```text
PRIVATE_LOCATION_ID_USED=YES|NO
PRIVATE_TARGET_PIPELINE_MATCH=YES|NO
PRIVATE_TARGET_PIPELINE_MATCH_COUNT=0|1|>1
CURRENT_STAGE_EXISTS_IN_TARGET_PIPELINE=YES|NO
EXPECTED_INITIAL_STAGE_BOUND=YES|NO
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ
AUTHORIZED_FINAL_STAGE_VERIFIED=YES|NO
AUTHORIZED_FINAL_STAGE_SELECTION_COUNT=0|1
FINAL_STAGE_DIFFERS_FROM_INITIAL_STAGE=YES|NO
PRIVATE_BINDING_PUBLICATION=NO
```

## Expected authorized-execution public result shape

These are expected outcomes only after the countersigned single-call procedure
and private final-stage decision complete successfully. They are not claimed by
this grant itself.

```text
RESULT=LIVE_LOCATION_PIPELINE_METADATA_VERIFIED

GET_PIPELINES_EXECUTION_ATTEMPTS=1
PIPELINE_METADATA_LIST_CALLS_EXECUTED=1

LIVE_LOCATION_BINDING_VERIFIED=YES
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
STOP_CODE=NW008_AT1_LIVE_LOCATION_PIPELINE_METADATA_VERIFY_006_SINGLE_CALL
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```
