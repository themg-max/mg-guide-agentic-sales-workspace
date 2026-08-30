# NW-008 AT1 GHL Runtime Source-Principal Resolution Diagnostic 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_RUNTIME_SOURCE_PRINCIPAL_RESOLUTION_DIAGNOSTIC_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-runtime-source-principal-resolution-diagnostic-001.md
CLASSIFICATION=READ_ONLY_RUNTIME_IDENTITY_RESOLUTION_DIAGNOSTIC
PR_CLASS=proof_only
OWNER=VS_CODE_MG_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BRANCH=
  diagnostic/nw008-at1-ghl-runtime-source-principal-resolution-001
BRANCH_IS_MAIN=NO
AUTHORITATIVE_MERGED_BASE=
  bf1ac645c2d2a98e9255b83ece339f54229cb2e7

MODE=READ_ONLY_DIAGNOSTIC_NO_MINT_NO_SECRET_NO_GHL_NO_IAM_MUTATION
DIAGNOSTIC_EXECUTED_AT_UTC=2026-08-30T07:25:59.000Z
```

This unit diagnoses the runtime source-principal mismatch exposed by terminal
execution proof 001. It resolved the actual credential materialized by
`google.auth.default()` in the failed execution context, compared it against the
required dedicated workflow identity, and proved the exact existing
workflow→note-runtime IAM relationship read-only. It performed **no** token
mint, **no** `generateAccessToken` call, **no** Secret Manager access, **no**
HighLevel call, **no** CRM operation, **no** IAM mutation, **no** retry of the
consumed GHL read, and **no** reuse of PR #336/#337/#338 authority. Issue #339
remains closed and terminal.

## 1. Authoritative failure binding

```text
EXECUTION_PROOF=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_EXECUTION_PROOF_001
EXECUTION_PROOF_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-execution-proof-001.md
PR_340_HEAD=
  3b451fae89331489d8085a1634165440ed4e8324

CONSUMPTION_RECORD_ISSUE=339
ISSUE_339_STATE=CONSUMED_TERMINAL_NON_REUSABLE
ISSUE_339_REOPENED_BY_THIS_UNIT=NO

FAILURE_CLASS=RUNTIME_IMPERSONATION_PERMISSION_DENIED
DENIED_PERMISSION=iam.serviceAccounts.getAccessToken

SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
GLOBAL_NO_RETRY_REQUIREMENT_SATISFIED=NO

PR_336_337_338_AUTHORITY_REUSED=NO
CONSUMED_GHL_READ_RETRIED=NO
```

## 2. Intended identity chain (frozen reference)

```text
EXPECTED_SOURCE_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_PRINCIPAL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
EXPECTED_PERMISSION=
  iam.serviceAccounts.getAccessToken
EXPECTED_ROLE=
  roles/iam.serviceAccountTokenCreator
```

## 3. Diagnostic method (no token mint)

The diagnostic loaded credentials in the exact failed execution context — the
same interpreter selection path chose the same virtual environment interpreter
used by the terminal attempt — and inspected credential class and identity
attributes only. `google.auth.default()` loads credential objects without
minting a token; no `refresh()` was invoked, no `generateAccessToken` was
called, and no impersonated target credential was constructed.

```text
INTERPRETER_SELECTION_MATCHES_FAILED_EXECUTION_CONTEXT=YES
GOOGLE_APPLICATION_CREDENTIALS_ENV=UNSET
ADC_RESOLUTION_PATH=GCLOUD_WELL_KNOWN_FILE
ADC_FILE_PRESENT=YES

TOKEN_MINTED_BY_DIAGNOSTIC=NO
CREDENTIAL_REFRESH_INVOKED=NO
GENERATE_ACCESS_TOKEN_CALLS=0
TARGET_IMPERSONATION_CONSTRUCTED_BY_DIAGNOSTIC=NO
SECRET_MANAGER_CALLS=0
GHL_CALLS=0
```

Safe field inspection of the well-known ADC file recorded credential type and
identity-bearing fields only. No refresh token, private key, or secret material
was read out, printed, logged, or persisted.

## 4. Resolved ADC credential (required record)

```text
ADC_CREDENTIAL_CLASS=
  google.auth.impersonated_credentials.Credentials

OBSERVED_SOURCE_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com

EXPECTED_SOURCE_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com

SOURCE_PRINCIPAL_MATCH=NO
```

Supporting resolution detail:

```text
ADC_FILE_TYPE=impersonated_service_account
ADC_IMPERSONATION_TARGET=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
ADC_DELEGATES=[]
ADC_SOURCE_CREDENTIALS_TYPE=authorized_user
ADC_SOURCE_CLIENT_EMAIL=NONE_IN_FILE
ADC_QUOTA_PROJECT=NONE
ADC_DEFAULT_PROJECT=ai-rolodex-to-crm

CREDS_SERVICE_ACCOUNT_EMAIL_ATTRIBUTE=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_PRINCIPAL_RESOLUTION_BASIS=
  IMPERSONATED_CREDENTIALS_TARGET_IS_THE_EFFECTIVE_CALLING_PRINCIPAL
```

Interpretation: in the failed execution context, `google.auth.default()` did not
materialize the dedicated GHL workflow identity. It materialized a pre-existing
local ADC impersonation chain (`authorized_user` →
`baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com`). The terminal
attempt then layered runtime impersonation of the note-runtime target on top of
that chain, so the effective principal presenting
`iam.serviceAccounts.getAccessToken` against the note-runtime service account
was `baby-bumps-runtime-b`, not `mg-guide-ghl-workflow`.

## 5. Target service-account IAM policy (read-only)

Exactly one read of the note-runtime service-account IAM policy was performed.

```text
IAM_POLICY_READS=1
IAM_POLICY_RESOURCE=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
IAM_POLICY_ETAG=BwZaPFy2B8E=
IAM_POLICY_VERSION=1

BINDING_COUNT=1
BINDING_1_ROLE=roles/iam.serviceAccountTokenCreator
BINDING_1_MEMBER_COUNT=1
BINDING_1_MEMBER_1=
  serviceAccount:mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
BINDING_1_CONDITION=NONE

EXACT_EXPECTED_BINDING_PRESENT=YES
EXPECTED_MEMBER_MATCH=YES
EXPECTED_ROLE_MATCH=YES
EXPECTED_SCOPE_EXACT_TARGET_SA=YES
UNEXPECTED_TOKEN_CREATOR_MEMBERS=NONE
OBSERVED_SOURCE_PRINCIPAL_PRESENT_IN_POLICY=NO
```

The required grant `workflow → Token Creator → note-runtime` exists exactly as
designed, scoped to the exact target service account, with the workflow identity
as the sole Token Creator member.

## 6. Policy Troubleshooter results (read-only)

```text
POLICY_TROUBLESHOOTER_CHECKS=2

CHECK_1_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
CHECK_1_PERMISSION=iam.serviceAccounts.getAccessToken
CHECK_1_RESOURCE=
  //iam.googleapis.com/projects/ai-rolodex-to-crm/serviceAccounts/mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
CHECK_1_ACCESS=GRANTED

CHECK_2_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
CHECK_2_PERMISSION=iam.serviceAccounts.getAccessToken
CHECK_2_RESOURCE=
  //iam.googleapis.com/projects/ai-rolodex-to-crm/serviceAccounts/mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
CHECK_2_ACCESS=NOT_GRANTED
```

The troubleshooter confirms the observed 403 exactly: the intended workflow
identity **is** granted the required permission, while the actually-materialized
source principal **is not** granted it. Check 2 was run because
`OBSERVED_SOURCE_PRINCIPAL` was known and differed from the workflow identity,
as required.

## 7. Root-cause decision

```text
SOURCE_PRINCIPAL_MATCH=NO

ROOT_CAUSE=
  EXECUTION_RUNTIME_DID_NOT_MATERIALIZE_DEDICATED_GHL_WORKFLOW_IDENTITY

ROOT_CAUSE_DETAIL=
  LOCAL_ADC_WELL_KNOWN_FILE_BINDS_AN_UNRELATED_IMPERSONATION_CHAIN
  AUTHORIZED_USER_TO_BABY_BUMPS_RUNTIME_B
  RUNTIME_LAYERED_NOTE_RUNTIME_IMPERSONATION_ON_TOP_OF_WRONG_SOURCE

IAM_GRANT_REPAIR_REQUIRED=NO
RUNTIME_IDENTITY_MATERIALIZATION_REPAIR_REQUIRED=YES

IAM_CONTRADICTION_PRESENT=NO
EXPECTED_GRANT_INTACT=YES
DENIAL_FULLY_EXPLAINED_BY_WRONG_SOURCE_PRINCIPAL=YES
```

The IAM design is correct and intact; no IAM binding change is required or
authorized. The repair belongs in runtime identity materialization: any future
execution unit must present `mg-guide-ghl-workflow` as the source principal
(for example via an execution context whose ADC resolves to the dedicated
workflow identity, or an explicit root-composed source credential bound to the
workflow identity) before layering note-runtime impersonation. Repair design and
any future attempt require fresh authorization and fresh activation; nothing is
retried under the consumed RUN_ID/window.

## 8. Retry-control defect (recorded separately)

```text
CLIENT_LIBRARY_CREDENTIAL_METADATA_RETRY_OBSERVED=YES
CLIENT_LIBRARY_RETRY_DETAIL=
  GOOGLE_API_CORE_RETRIED_UNAVAILABLE_METADATA_FAILURE_UNTIL_60_SECOND_TIMEOUT
GLOBAL_NO_RETRY_REQUIREMENT_SATISFIED=NO
RETRY_CONTROL_REPAIR_REQUIRED=YES

RETRY_CONTROL_REPAIR_SCOPE=
  DISABLE_OR_BOUND_CLIENT_LIBRARY_INTERNAL_RETRY_ON_CREDENTIAL_AND_SECRET_PATHS
RETRY_CONTROL_REPAIR_AUTHORIZED_BY_THIS_UNIT=NO
```

This defect is independent of the identity mismatch: even with a correct source
principal, the credential/secret client paths must be configured so a terminal
failure cannot be internally retried by the client library.

## 9. Non-reuse and non-action freeze

```text
CONSUMED_GHL_READ_RETRIED=NO
ISSUE_339_REOPENED=NO
RUN_ID_REUSED=NO
WINDOW_REUSED=NO
PR_336_AUTHORITY_REUSED=NO
PR_337_AUTHORITY_REUSED=NO
PR_338_AUTHORITY_REUSED=NO

IAM_MUTATION_PERFORMED=NO
IAM_BINDING_ADDED=NO
IAM_BINDING_REMOVED=NO
IAM_BINDING_MODIFIED=NO

GENERATE_ACCESS_TOKEN_CALLS=0
TOKEN_MINT_ATTEMPTS=0
TOKEN_MINTS=0
ACCESS_SECRET_VERSION_CALLS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
GHL_READ_ATTEMPTS=0
HTTP_REQUEST_DISPATCHES_TO_GHL=0
CRM_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENTS=0
LANE_A_WORK=0
```

## 10. Read-only operation ledger (this unit)

```text
ADC_CREDENTIAL_OBJECT_LOADS=1
ADC_WELL_KNOWN_FILE_SAFE_FIELD_READS=1
GCLOUD_AUTH_LIST_READS=1
GCLOUD_CONFIG_READS=1
IAM_POLICY_READS=1
POLICY_TROUBLESHOOTER_CHECKS=2

SECRET_MATERIAL_READ=NO
REFRESH_TOKEN_READ_OR_PRINTED=NO
PRIVATE_KEY_READ_OR_PRINTED=NO
TOKEN_VALUES_PRINTED=NO
EXECUTION_PERFORMED=NO
EXTERNAL_MUTATIONS=0
```

## 11. Required next governed actions

```text
NEXT_ACTION_1=
  INDEPENDENT_DIAGNOSTIC_REVIEW_AND_MERGE
NEXT_ACTION_2=
  RUNTIME_IDENTITY_MATERIALIZATION_REPAIR_DESIGN
  (EXECUTION_CONTEXT_MUST_PRESENT_DEDICATED_GHL_WORKFLOW_IDENTITY_AS_SOURCE)
NEXT_ACTION_3=
  RETRY_CONTROL_REPAIR_DESIGN
  (CLIENT_LIBRARY_INTERNAL_RETRY_MUST_BE_DISABLED_OR_BOUNDED_ON_CREDENTIAL_PATHS)
NEXT_ACTION_4=
  FRESH_AUTHORIZATION_AND_FRESH_ACTIVATION_REQUIRED_FOR_ANY_LATER_BOUNDED_READ

DO_NOT_MUTATE_IAM=YES
DO_NOT_MINT_TOKENS=YES
DO_NOT_ACCESS_SECRETS=YES
DO_NOT_CALL_HIGHLEVEL=YES
DO_NOT_REOPEN_ISSUE_339=YES
DO_NOT_REUSE_CONSUMED_AUTHORITY=YES
```

## 12. STOP

```text
STOP_CODE=
  NW008_AT1_GHL_RUNTIME_SOURCE_PRINCIPAL_RESOLUTION_DIAGNOSTIC_001_COMPLETE
STOP=FOR_INDEPENDENT_DIAGNOSTIC_REVIEW

SOURCE_PRINCIPAL_MATCH=NO
ROOT_CAUSE=
  EXECUTION_RUNTIME_DID_NOT_MATERIALIZE_DEDICATED_GHL_WORKFLOW_IDENTITY
IAM_GRANT_REPAIR_REQUIRED=NO
RUNTIME_IDENTITY_MATERIALIZATION_REPAIR_REQUIRED=YES
RETRY_CONTROL_REPAIR_REQUIRED=YES

GENERATE_ACCESS_TOKEN_CALLS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
IAM_MUTATIONS=0
```

Stop here. No IAM change, token mint, secret access, HighLevel call, or retry
occurred in this unit.
