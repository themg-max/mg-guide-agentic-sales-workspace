# NW-008 AT-1 -- GHL Credential/Location Exact-Opportunity Diagnostic Grant 005

```text
GRANT_ID=NW008_AT1_GHL_CREDENTIAL_LOCATION_DIAGNOSTIC_005
GRANT_TYPE=READ_ONLY_EXACT_OPPORTUNITY_LOCATION_DIAGNOSTIC
ARTIFACT_KIND=BOUNDED_READ_ONLY_EXACT_OPPORTUNITY_LOCATION_DIAGNOSTIC_GRANT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
RESULT_002_COMMIT_SHA=897db6e74f1d022260d385a4852269a7bb1d1a49
RESULT_004_SHA=b641e1dc87b4a00c46c716b977b1918c1cf7e56c
RECONCILIATION_SHA=b311cf2e5ef28d2d209d9e1f6531aa57c87e8a9a
GRANT_STATE=AUTHORIZED_READ_ONLY_EXACT_OPPORTUNITY_LOCATION_DIAGNOSTIC
SELF_ACTIVATION=FORBIDDEN
```

This grant authorizes exactly one exact-opportunity diagnostic read to test
whether the current direct GHL PIT can access the canonical NW-013/NW-008
private synthetic opportunity and to compare the returned location against
private binding `NW008_GHL_LOCATION_PRIVATE_V1`.

It continues from:

1. Result 002 partial external binding verification
   (`897db6e74f1d022260d385a4852269a7bb1d1a49`)
2. Grant 004 fail-closed location-token access denial
   (`b641e1dc87b4a00c46c716b977b1918c1cf7e56c`)
3. Credential/location reconciliation binding-unknown checkpoint
   (`b311cf2e5ef28d2d209d9e1f6531aa57c87e8a9a`)

No private identifier may be printed, committed, or otherwise published.

## Frozen authority and caps

```text
EXACT_OPPORTUNITY_READ_ATTEMPTS_MAX=1
CRM_RECORD_READS_MAX=1
MUTATION_CALLS_MAX=0

ALLOWED_OPERATION_GET_OPPORTUNITY=YES

PRIVATE_OPPORTUNITY_ID_REQUIRED=YES
PRIVATE_NW008_LOCATION_ID_REQUIRED=YES
PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LOCATION_PRIVATE_V1
PRIVATE_OPPORTUNITY_BINDING_REF=NW013_CANONICAL_SYNTHETIC_OPPORTUNITY

SEARCH=NO
FETCH=NO
LIST_LOCATIONS=NO
GET_PIPELINES=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO

CREDENTIAL_CREATE_AUTHORIZED=NO
CREDENTIAL_ROTATION_AUTHORIZED=NO
SECRET_MANAGER_WRITE_AUTHORIZED=NO
IAM_CHANGE_AUTHORIZED=NO

PRIVATE_BINDING_PUBLICATION=NO

ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

The sole permitted business call is `execute_operation:get-opportunity`, exactly
once, with the private synthetic opportunity id supplied in the operation path
parameters. No search, list, pagination, retry, mutation, credential change, or
raw REST fallback is authorized.

## Bound execution surface

```text
EXECUTION_SURFACE=GHL_ANTHROPIC_V2_MCP
EXECUTION_ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
EXECUTION_OPERATION=execute_operation:get-opportunity
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
MCP_PROTOCOL_INITIALIZE_ALLOWED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_CRM_READ=NO
EXACT_OPPORTUNITY_READ_ATTEMPTS_MAX=1
CRM_RECORD_READS_MAX=1
MUTATION_CALLS_MAX=0
```

## Continuity from reconciliation

```text
PRIOR_CHECK_ID=NW008_AT1_GHL_CREDENTIAL_LOCATION_RECON_005
PRIOR_RESULT=RECONCILIATION_COMPLETE_BINDING_UNKNOWN
SECRET_CHANGED_AFTER_RESULT_002=NO
RESULT002_PRIVATE_LOCATION_RECOVERED=NO
LOCATION_BINDING_MATCH_BEFORE_GRANT=UNKNOWN
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS_BEFORE_GRANT=NOT_TESTED
CORRECTION=ONE_EXACT_GET_OPPORTUNITY_TO_REESTABLISH_TOKEN_ACCESSIBLE_LOCATION
RETRY_OF_GRANT_004=NO
```

Grant 005 is a new single-attempt diagnostic authorization. It is not a retry
under Grant 004 and does not authorize `get-pipelines`.

## Mandatory human countersignature

The human GHL space owner countersigns immediately before execution. The
authorization expires 60 minutes after this countersignature. A missing,
expired, or ambiguous countersignature means no external call is authorized.

```text
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_COUNTERSIGNATURE=APPROVED
HUMAN_APPROVER=THEMG@themiliare-group.com
APPROVED_AT_UTC=2026-08-17T10:01:05Z
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
EXPIRES_AT_UTC=2026-08-17T11:01:05Z
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
```

Required countersignature statement:

```text
I authorize exactly one read-only execute_operation:get-opportunity call under
NW008_AT1_GHL_CREDENTIAL_LOCATION_DIAGNOSTIC_005, bound to Result 002
897db6e74f1d022260d385a4852269a7bb1d1a49, Result 004
b641e1dc87b4a00c46c716b977b1918c1cf7e56c, and reconciliation
b311cf2e5ef28d2d209d9e1f6531aa57c87e8a9a. The call may use the private
synthetic opportunity id from the NW-013/NW-008 canonical private binding and
may privately compare the returned location id to
NW008_GHL_LOCATION_PRIVATE_V1. Private capture of returned pipeline id and
pipeline stage id is permitted for control-plane evidence only. Exactly zero
search/list/pagination calls, zero retries, zero mutations, zero credential
creates/rotations/IAM changes, and no publication of private identifiers are
permitted. This does not authorize AT-1 execution or mark ENVIRONMENT_READY.
```

## Private operator procedure after countersignature

1. Confirm private opportunity id from the NW-013/NW-008 canonical synthetic
   binding control plane without publishing it.
2. Confirm private expected location id from
   `NW008_GHL_LOCATION_PRIVATE_V1` / binding `location_id_value` without
   publishing it.
3. Resolve direct GHL PIT from Secret Manager secret `GHL_MCP_PRIVATE_TOKEN`
   in project `ai-rolodex-to-crm`. Do not print the token. Do not create or
   rotate credentials.
4. MCP `initialize` once on the anthropic_v2 endpoint (does not count as the
   CRM read).
5. Execute `tools/call` → `execute_operation` / `get-opportunity` exactly once
   with the private opportunity id in operation path parameters. No retry.
6. If access is denied or the operation fails closed on authorization:
   set `CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=NO`,
   `LOCATION_BINDING_MATCH=UNKNOWN`, and STOP.
7. If the read succeeds:
   set `CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES`;
   privately capture `returned_location_id`, `returned_pipeline_id`, and
   `returned_pipeline_stage_id`;
   compare `returned_location_id` to `NW008_GHL_LOCATION_PRIVATE_V1`;
   set `LOCATION_BINDING_MATCH=YES|NO`;
   persist private fingerprints/control-plane evidence only.
8. Record only sanitized Boolean / enum outcomes in the public result artifact.
   Never publish raw IDs, tokens, or payloads.

## Required private decision record

```text
PRIVATE_OPPORTUNITY_ID_USED=YES|NO
PRIVATE_EXPECTED_LOCATION_ID_PRESENT=YES|NO
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES|NO
RETURNED_LOCATION_ID_PRESENT=YES|NO
RETURNED_PIPELINE_ID_PRESENT=YES|NO
RETURNED_PIPELINE_STAGE_ID_PRESENT=YES|NO
LOCATION_BINDING_MATCH=YES|NO|UNKNOWN
PRIVATE_BINDING_FINGERPRINT_RECORDED=YES|NO
PRIVATE_BINDING_PUBLICATION=NO
```

## Expected authorized-execution public result shapes

Success path:

```text
RESULT=EXACT_OPPORTUNITY_DIAGNOSTIC_COMPLETE
EXACT_OPPORTUNITY_READ_ATTEMPTS=1
CRM_RECORD_READS_EXECUTED=1
MUTATION_CALLS_EXECUTED=0
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES
RETURNED_LOCATION_ID_PRESENT=YES|NO
RETURNED_PIPELINE_ID_PRESENT=YES|NO
RETURNED_PIPELINE_STAGE_ID_PRESENT=YES|NO
LOCATION_BINDING_MATCH=YES|NO
PRIVATE_BINDING_FINGERPRINT_RECORDED=YES|NO
PRIVATE_BINDING_PUBLICATION=NO
CREDENTIAL_CHANGE_AUTHORIZED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Access-denied path:

```text
RESULT=BLOCKED_CURRENT_PIT_OPPORTUNITY_ACCESS
EXACT_OPPORTUNITY_READ_ATTEMPTS=1
CRM_RECORD_READS_EXECUTED=1|0
MUTATION_CALLS_EXECUTED=0
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=NO
LOCATION_BINDING_MATCH=UNKNOWN
PRIVATE_BINDING_PUBLICATION=NO
CREDENTIAL_CHANGE_AUTHORIZED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Decision table after result

```text
IF CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES AND LOCATION_BINDING_MATCH=YES:
  NEXT=INVESTIGATE_GET_PIPELINES_OPERATION_SPECIFIC_AUTHORIZATION
  NEW_PIT_REQUIRED=NO

IF CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES AND LOCATION_BINDING_MATCH=NO:
  NEXT=HUMAN_RECONCILE_NW008_PRIVATE_LOCATION_AUTHORITY
  NEW_PIT_REQUIRED=NO_PENDING_LOCATION_DECISION

IF CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=NO:
  NEXT=OPEN_SEPARATE_PIT_SUBACCOUNT_REMEDIATION_LANE
  NEW_PIT_REQUIRED=UNKNOWN_PENDING_CREDENTIAL_REVIEW
```

## Explicit non-actions

```text
DID_NOT_AUTHORIZE_SEARCH=YES
DID_NOT_AUTHORIZE_FETCH=YES
DID_NOT_AUTHORIZE_LIST_LOCATIONS=YES
DID_NOT_AUTHORIZE_GET_PIPELINES=YES
DID_NOT_AUTHORIZE_PAGINATION=YES
DID_NOT_AUTHORIZE_RETRY=YES
DID_NOT_AUTHORIZE_RAW_REST_FALLBACK=YES
DID_NOT_AUTHORIZE_MUTATIONS=YES
DID_NOT_AUTHORIZE_CREDENTIAL_CREATE=YES
DID_NOT_AUTHORIZE_CREDENTIAL_ROTATION=YES
DID_NOT_AUTHORIZE_SECRET_MANAGER_WRITE=YES
DID_NOT_AUTHORIZE_IAM_CHANGE=YES
DID_NOT_AUTHORIZE_PRIVATE_BINDING_PUBLICATION=YES
DID_NOT_AUTHORIZE_AT1_EXECUTION=YES
DID_NOT_AUTHORIZE_ENVIRONMENT_READY=YES
```

## STOP after the single permitted call

```text
STOP_CODE=NW008_AT1_GHL_CREDENTIAL_LOCATION_DIAGNOSTIC_005_EXECUTE_ONCE_THEN_STOP
NEXT=PUBLIC_RESULT_005_THEN_DECISION_TABLE
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```
