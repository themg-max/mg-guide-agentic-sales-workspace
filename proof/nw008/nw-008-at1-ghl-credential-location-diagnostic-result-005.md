# NW-008 AT-1 -- GHL Credential/Location Exact-Opportunity Diagnostic Result 005

```text
GRANT_ID=NW008_AT1_GHL_CREDENTIAL_LOCATION_DIAGNOSTIC_005
AUTHORIZED_GRANT_005_SHA=8759eafc127ab9b12761eaedeb47f92c7f9bc491
ARTIFACT_KIND=BOUNDED_READ_ONLY_EXACT_OPPORTUNITY_LOCATION_DIAGNOSTIC_RESULT
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
RESULT_002_COMMIT_SHA=897db6e74f1d022260d385a4852269a7bb1d1a49
RESULT_004_SHA=b641e1dc87b4a00c46c716b977b1918c1cf7e56c
RECONCILIATION_SHA=b311cf2e5ef28d2d209d9e1f6531aa57c87e8a9a
RESULT=EXACT_OPPORTUNITY_DIAGNOSTIC_COMPLETE
RECORDED_AT_UTC=2026-08-17T10:03:29Z
```

## Disposition

Direct GHL PIT resolution from Secret Manager succeeded. Private opportunity and
expected-location bindings were loaded from the NW-013/NW-008 canonical synthetic
control plane (`NW008_GHL_LOCATION_PRIVATE_V1`) without publication. Within the
Grant 005 countersignature window, MCP `initialize` completed and exactly one
`execute_operation:get-opportunity` call was executed on the proven anthropic_v2
surface with the private synthetic opportunity id in path parameters.

The MCP transport returned HTTP 200 and the operation succeeded. The returned
opportunity id matched the private allowlisted synthetic opportunity id. Returned
location, pipeline, and pipeline-stage identifiers were present and captured only
in private operator/control-plane evidence (fingerprints retained; raw IDs not
published).

Private comparison of the returned location id against
`NW008_GHL_LOCATION_PRIVATE_V1` evaluated to **NO**. Therefore the current PIT
can read the exact synthetic opportunity, but the opportunity's live location
does not match the NW-008 private location binding used for Grant 004
`get-pipelines`. No retry, search, list, pagination, mutation, or credential
change was performed.

```text
RESULT=EXACT_OPPORTUNITY_DIAGNOSTIC_COMPLETE

EXACT_OPPORTUNITY_READ_ATTEMPTS=1
CRM_RECORD_READS_EXECUTED=1
MUTATION_CALLS_EXECUTED=0

CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES

RETURNED_LOCATION_ID_PRESENT=YES
RETURNED_PIPELINE_ID_PRESENT=YES
RETURNED_PIPELINE_STAGE_ID_PRESENT=YES

LOCATION_BINDING_MATCH=NO

PRIVATE_BINDING_FINGERPRINT_RECORDED=YES
PRIVATE_BINDING_PUBLICATION=NO

CREDENTIAL_CHANGE_AUTHORIZED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Execution surface (sanitized)

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
DIRECT_GHL_SECRET_SOURCE_RESOLVED=YES
DIRECT_GHL_PIT_PRESENT=YES
OPERATION=execute_operation:get-opportunity
PRIVATE_OPPORTUNITY_ID_USED=YES
PRIVATE_EXPECTED_LOCATION_BINDING_REF=NW008_GHL_LOCATION_PRIVATE_V1
MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_CRM_READ=NO
INIT_HTTP=200
GET_OPPORTUNITY_TRANSPORT_HTTP=200
GET_OPPORTUNITY_OPERATION_SUCCESS=YES
OPPORTUNITY_ID_BINDING_MATCH=YES
SEARCH_CALLS_EXECUTED=0
FETCH_CALLS_EXECUTED=0
LIST_LOCATIONS_CALLS_EXECUTED=0
GET_PIPELINES_CALLS_EXECUTED=0
PAGINATION_USED=NO
RETRY_USED=NO
RAW_REST_FALLBACK_USED=NO
```

## Private fingerprint / control-plane evidence (no raw IDs)

```text
PRIVATE_BINDING_FINGERPRINT_RECORDED=YES
PRIVATE_BINDING_PUBLICATION=NO
EXPECTED_LOCATION_FP=aa53db90f0dad317
RETURNED_LOCATION_FP=5e14ac52bf731569
RETURNED_PIPELINE_FP=2ca9c0cd5bd28d2b
RETURNED_PIPELINE_STAGE_FP=8a4d12b7122f0f0e
RETURNED_OPPORTUNITY_FP=4e83afec7e94a109
LOCATION_FP_EQUAL=NO
```

Fingerprints are truncated SHA-256 prefixes for operator correlation only. Raw
location/pipeline/stage identifiers remain outside the public repository in the
private control-plane evidence file associated with the NW-013 synthetic binding
lane.

## Caps compliance

| Cap / rule | Required | Observed |
| --- | --- | --- |
| `EXACT_OPPORTUNITY_READ_ATTEMPTS_MAX` | 1 | 1 |
| `CRM_RECORD_READS_MAX` | 1 | 1 |
| `MUTATION_CALLS_MAX` | 0 | 0 |
| `ALLOWED_OPERATION_GET_OPPORTUNITY` | YES | called once |
| `SEARCH` | NO | not called |
| `FETCH` | NO | not called |
| `LIST_LOCATIONS` | NO | not called |
| `GET_PIPELINES` | NO | not called |
| `PAGINATION` | NO | not used |
| `RETRY` | NO | not used |
| `RAW_REST_FALLBACK` | NO | not used |
| credential create/rotate/IAM | NO | not performed |
| private binding publication | NO | no IDs or payloads published |
| MG MCP proxy credential | FORBIDDEN | not used |

## Decision

```text
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES
LOCATION_BINDING_MATCH=NO
NEXT=HUMAN_RECONCILE_NW008_PRIVATE_LOCATION_AUTHORITY
NEW_PIT_REQUIRED=NO_PENDING_LOCATION_DECISION
```

Rationale: the current PIT successfully performed an exact opportunity read, so
a blanket “token cannot read opportunities” failure mode is excluded. The live
opportunity location does **not** match `NW008_GHL_LOCATION_PRIVATE_V1`, which
explains why Grant 004's location-scoped `get-pipelines` call received
location-token access denial when using the NW-008 private location binding.
Remediation is a human location-authority reconciliation (update the private
NW-008 location binding to the token-accessible opportunity location, or move
the synthetic opportunity / authorize the bound location), not an immediate PIT
rotation.

## Explicit non-actions

```text
DID_NOT_CALL_SEARCH=YES
DID_NOT_CALL_FETCH=YES
DID_NOT_CALL_LIST_LOCATIONS=YES
DID_NOT_CALL_GET_PIPELINES=YES
DID_NOT_CALL_GET_CONTACT=YES
DID_NOT_PAGINATE=YES
DID_NOT_RETRY_GET_OPPORTUNITY=YES
DID_NOT_RAW_REST_FALLBACK=YES
DID_NOT_EXECUTE_CREATE_NOTE=YES
DID_NOT_EXECUTE_GET_NOTE=YES
DID_NOT_EXECUTE_UPDATE_OPPORTUNITY=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_CREATE_OR_ROTATE_PIT=YES
DID_NOT_MODIFY_CREDENTIALS=YES
DID_NOT_WRITE_SECRET_MANAGER=YES
DID_NOT_MODIFY_IAM=YES
DID_NOT_PUBLISH_PRIVATE_BINDING_IDS=YES
DID_NOT_AUTHORIZE_AT1_EXECUTION=YES
DID_NOT_CLAIM_ENVIRONMENT_READY=YES
```

## Continuity notes

1. Reconciliation established `SECRET_CHANGED_AFTER_RESULT_002=NO` and
   `LOCATION_BINDING_MATCH=UNKNOWN` because Result 002's observed location had
   been redacted at capture time.
2. Grant 005 re-read the exact synthetic opportunity once and re-established the
   token-accessible location privately.
3. `LOCATION_BINDING_MATCH=NO` is now a positive diagnostic finding, not an
   unknown.
4. Grant 004's fail-closed stop
   (`GRANT004_GET_PIPELINES_LOCATION_TOKEN_ACCESS_DENIED`) remains consistent
   with a location-binding mismatch under an otherwise valid PIT.
5. No AT-1 execution authority is granted by this result.

## STOP

```text
STOP_CODE=NW008_AT1_GHL_CREDENTIAL_LOCATION_DIAGNOSTIC_005_COMPLETE
RESULT=EXACT_OPPORTUNITY_DIAGNOSTIC_COMPLETE
EXACT_OPPORTUNITY_READ_ATTEMPTS=1
CRM_RECORD_READS_EXECUTED=1
MUTATION_CALLS_EXECUTED=0
CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=YES
LOCATION_BINDING_MATCH=NO
RETURNED_PIPELINE_ID_PRESENT=YES
RETURNED_PIPELINE_STAGE_ID_PRESENT=YES
PRIVATE_BINDING_FINGERPRINT_RECORDED=YES
PRIVATE_BINDING_PUBLICATION=NO
NEW_PIT_REQUIRED=NO_PENDING_LOCATION_DECISION
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=HUMAN_RECONCILE_NW008_PRIVATE_LOCATION_AUTHORITY
```
