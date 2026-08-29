# NW-008 AT-1 — GHL REST v3 PIT / Sub-Account Binding Validation Design 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PIT_SUBACCOUNT_BINDING_VALIDATION_DESIGN_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-rest-v3-pit-subaccount-binding-validation-design-001.md
PR_CLASS=planning_only
OWNER=VS_CODE_ORCHESTRATOR

ACTION=
  CLOSE_EXECUTION_PROOF_002_AND_PREPARE_PIT_SUBACCOUNT_BINDING_VALIDATION

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=19e92ad8aed498d47890fbad6c9fb0f38f91b2f6
PLAN_BRANCH=
  plan/nw008-at1-ghl-rest-v3-pit-subaccount-binding-validation-design-001
BRANCH_IS_MAIN=NO
ABORT_IF_BRANCH_MAIN=YES

IMPLEMENTATION_IN_SCOPE=NO
RUNTIME_CODE_MUTATION_IN_SCOPE=NO
AUTHORIZATION_ARTIFACT_IN_SCOPE=NO
GRANT_ARTIFACT_IN_SCOPE=NO
VALIDATION_EXECUTION_IN_SCOPE=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0
SECRET_MANAGER_SECRET_READS=0
TARGET_SA_IMPERSONATION_ATTEMPTS=0

VALIDATION_EXECUTION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO

GRANT_003_CREATED=NO
GRANT_002_REUSE_AUTHORIZED=NO
```

This unit is **planning only**. It designs the smallest fail-closed live read
that can determine whether the designated `MG_GUIDE_PIT_GHL` private integration
token is bound to the privately sealed validation sub-account / location.

Merging or reviewing this design confers no implementation, live-read,
authorization, grant, PIT-rotation, or scope-edit authority.

## 2. Controlling predecessors

```text
PR281_MERGE_SHA=
  19e92ad8aed498d47890fbad6c9fb0f38f91b2f6
PR281_ARTIFACTS=
  docs/nw008/nw-008-at1-ghl-rest-v3-provider-error-evidence-contract-001.md
  proof/nw008/nw-008-at1-ghl-rest-v3-provider-error-evidence-remediation-001.md
NON_2XX_EVIDENCE_SURFACE_READY=YES

EXECUTION_PROOF_002_ARTIFACT=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-execution-proof-002.md
EXECUTION_PROOF_002_PR=
  proof/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-execution-proof-002
  (dedicated execution_proof PR; not mixed with live re-execution)

GRANT_002_CONSUMED=YES
GRANT_002_REUSE_AUTHORIZED=NO
CALL_1_HTTP_STATUS=403
BUSINESS_CALLS_ATTEMPTED=1
READS_ATTEMPTED=1
WRITES_ATTEMPTED=0
CRM_MUTATIONS=0
RETRY_PERFORMED=NO
PROVIDER_CONTRACT_EVALUATED=NO
PROVIDER_RUNTIME_RESULT=UNKNOWN
STAGE_PATH_BLOCKER_CLEARED=NO

HUMAN_SCOPE_EVIDENCE=
  PRIVATE_INTEGRATION_NAME=MG_Guide
  OPPORTUNITIES_READONLY_PRESENT=YES
  OPPORTUNITIES_WRITE_PRESENT=YES
  CONTACTS_READONLY_PRESENT=YES
  CONTACTS_WRITE_PRESENT=YES
  LOCATIONS_READONLY_PRESENT=YES
  GHL_SCOPE_REMEDIATION_REQUIRED=NO

PACKAGE_ID=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001
VALIDATION_PACKAGE_DIGEST=
  1f75f5956476824c976c2d1c0a79a892ec4129c5bb55a8ba636f85d30af75c8d
PRIVATE_VALIDATION_LOCATION_BINDING_PRESENT=YES
```

Interpretation of Proof 002:

1. GRANT_002 is fully consumed and may not be reused.
2. CALL_1 definitive HTTP 403 stopped the stage-provider three-call protocol
   before any opportunity envelope or stage-body evaluation.
3. Human scope evidence indicates required HighLevel scopes appear present; the
   residual uncertainty is therefore **not** "add missing scopes" by default.
4. A distinct, narrower binding probe is required to determine whether the
   designated PIT is bound to the sealed private validation location /
   sub-account before any future stage-provider grant is drafted.

```text
GHL_SCOPE_REMEDIATION_REQUIRED=NO
PIT_ROTATION_REQUIRED=UNKNOWN
PIT_SUBACCOUNT_BINDING_VALIDATION_REQUIRED=YES
GRANT_003_READY_TO_DRAFT=NO
```

## 3. Purpose and non-purpose

### 3.1 Purpose

Resolve, with one exact read, whether the designated production PIT can retrieve
the privately bound validation location under REST v3:

```text
QUESTION=
  Does GET /locations/{private_validation_location_id} with the designated
  MG_GUIDE_PIT_GHL credential return HTTP 200 and an exact location envelope
  whose id matches the sealed private validation location binding?

SUCCESS_MEANS=
  PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=YES

FAILURE_OR_UNKNOWN_MEANS=
  future stage-provider grant drafting remains blocked pending separate
  diagnosis; no automatic PIT rotation, scope edit, or GRANT_003 creation
```

### 3.2 Non-purpose

```text
NOT_A_STAGE_PROVIDER_RETRY=YES
NOT_A_GRANT_002_REUSE=YES
NOT_A_GRANT_003=YES
NOT_A_STAGE_PATH_IMPLEMENTATION=YES
NOT_AN_OPPORTUNITY_READ_OR_WRITE=YES
NOT_A_NOTE_PATH_EXECUTION=YES
NOT_A_PIT_ROTATION=YES
NOT_A_SCOPE_EDIT=YES
NOT_A_SEARCH_OR_LIST_PROBE=YES
NOT_A_PUBLIC_ID_DISCLOSURE=YES
```

## 4. Exact future operation (frozen design)

```text
CALL_1=
  GET /locations/{private_validation_location_id}

VERSION_HEADER=v3
BASE_URL=https://services.leadconnectorhq.com

CALL_SEQUENCE=GET
ORDER_EXACT=YES
ALTERNATE_ORDER=NO

MAX_READS=1
MAX_WRITES=0
MAX_TOTAL_BUSINESS_CALLS=1
CALL_BUDGET_BOUND=YES

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_ALTERNATE_TARGET=YES
NO_ALTERNATE_CREDENTIAL=YES
NO_ALTERNATE_OPERATION=YES
NO_MUTATION=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES
```

Out-of-scope endpoints remain forbidden for this validation:

```text
NOT_SELECTED=GET /opportunities/{id}
NOT_SELECTED=PUT /opportunities/{id}
NOT_SELECTED=GET /opportunities/search
NOT_SELECTED=POST /opportunities/search
NOT_SELECTED=GET /opportunities/pipelines
NOT_SELECTED=GET /locations/
NOT_SELECTED=GET /locations/search
NOT_SELECTED=ANY_LIST_OR_PAGINATED_SURFACE
NOT_SELECTED=ANY_WRITE_SURFACE
NOT_SELECTED=MCP_ANY
```

## 5. Credential route (frozen; repository-owned)

```text
CREDENTIAL_ROUTE=
  authorized_user ADC
  ->
  exact target runtime SA impersonation
  ->
  Secret Manager client using target credentials
  ->
  exact MG_GUIDE_PIT_GHL accessor

TARGET_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_SECRET=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1

ALTERNATE_CREDENTIALS_FORBIDDEN=YES
SERVICE_ACCOUNT_KEY_FORBIDDEN=YES
GCLOUD_SECRET_ACCESS_FALLBACK_FORBIDDEN=YES
ENVIRONMENT_TOKEN_FALLBACK_FORBIDDEN=YES
IAM_MUTATION_FORBIDDEN=YES
```

```text
AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_PRIVILEGED_CREDENTIAL_PLANE_ACTION
```

A future grant for this design, if ever countersigned, is consumed on the first
privileged credential-plane action, regardless of success or failure.

## 6. Private binding symbols (names only)

```text
PRIVATE_BINDING_SYMBOLS=
  private_validation_location_id

PACKAGE_ID=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001
VALIDATION_PACKAGE_DIGEST=
  1f75f5956476824c976c2d1c0a79a892ec4129c5bb55a8ba636f85d30af75c8d

TARGET_MUST_EQUAL_PRIVATE_VALIDATION_LOCATION_ID=YES
TARGET_SUBSTITUTION_FORBIDDEN=YES
ACCEPTANCE_TARGET_REUSE_ALLOWED=NO
```

Raw location IDs remain private and must never appear in public proof text.

## 7. Success / fail predicates

### 7.1 PASS (all required)

```text
HTTP_STATUS=200
LOCATION_ENVELOPE_PRESENT=YES
RETURNED_LOCATION_ID_MATCH=YES
PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=YES
```

Selector candidates (consume-minimized):

```text
LOCATION_SELECTORS=
  location.id
  # or top-level id when provider returns bare location object
```

```text
PASS_REQUIRES_EXACT_ID_MATCH_ONLY=YES
PASS_DOES_NOT_PUBLISH_LOCATION_PAYLOAD=YES
```

### 7.2 FAIL / UNKNOWN dispositions

| Outcome class | Signal | Result | Retry | Binding claim |
| --- | --- | --- | --- | --- |
| Definitive success + id match | 200 + envelope + id match | `PASS` | NO | `PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=YES` |
| Definitive authn failure | 401 | `FAIL` | NO | binding unresolved; class=`AUTHENTICATION` |
| Definitive authz failure | 403 | `FAIL` | NO | binding unresolved; class=`AUTHORIZATION` |
| Definitive not found | 404 | `FAIL` | NO | binding unresolved; class=`NOT_FOUND` |
| Definitive validation failure | 400/422 | `FAIL` | NO | class=`REQUEST_VALIDATION` |
| Rate limit | 429 | `FAIL` | NO | class=`RATE_LIMIT` |
| Provider 5xx | 5xx | `FAIL` | NO | class=`PROVIDER_FAILURE` |
| Transport ambiguity | timeout/disconnect | `FAIL_AMBIGUOUS_READ` | NO | binding unresolved |
| 200 without envelope/id match | malformed/mismatch | `FAIL` | NO | binding unresolved |

```text
HTTP_CLASS_DOES_NOT_ESTABLISH_DETAILED_CAUSE=YES
DEFAULT_PROVIDER_ERROR_CAUSE=UNKNOWN
NO_RETRY=YES
```

## 8. PR281 provider-error evidence wiring (mandatory for future executor)

Before any future live grant under this design is authorized, the stage /
binding validation executor MUST invoke the merged PR #281 helpers on every
definitive non-2xx response:

```text
PR281_MERGE_SHA=
  19e92ad8aed498d47890fbad6c9fb0f38f91b2f6
NON_2XX_EVIDENCE_SURFACE_READY=YES

REQUIRED_ON_DEFINITIVE_NON_2XX=
  1. retain LiveNoteHttpResult.status_code + body + headers privately
  2. derive_private_provider_error_evidence(result)
  3. project_public_provider_error_evidence(private_evidence)
  4. publish ONLY the public projection fields
```

Required public projection fields (presence/class only):

```text
PROVIDER_HTTP_STATUS
PROVIDER_CONTENT_TYPE_CLASS
PROVIDER_ERROR_ENVELOPE_PRESENT
PROVIDER_ERROR_CODE_PRESENT
PROVIDER_ERROR_MESSAGE_PRESENT
PROVIDER_REQUEST_ID_PRESENT
PROVIDER_CORRELATION_ID_PRESENT
PROVIDER_ERROR_CLASS
PROVIDER_ERROR_CAUSE
RAW_PROVIDER_RESPONSE_PUBLISHED=NO
PROVIDER_ERROR_MESSAGE_PUBLISHED=NO
PROVIDER_REQUEST_ID_PUBLISHED=NO
PROVIDER_CORRELATION_ID_PUBLISHED=NO
AUTHORIZATION_HEADER_PUBLISHED=NO
TOKEN_OR_PIT_PUBLISHED=NO
```

```text
FUTURE_EXECUTOR_WITHOUT_ERROR_EVIDENCE_WIRING=FORBIDDEN
GRANT_002_INLINE_STATUS_ONLY_CAPTURE=INSUFFICIENT_FOR_FUTURE_GRANTS
```

Proof 002 is historical evidence that status-only capture is insufficient once
the evidence surface exists. Future grants must not regress.

This design unit does **not** implement the executor wiring and does **not**
mutate `src/**`.

## 9. Public privacy contract

```text
RAW_LOCATION_ID_PUBLIC=NO
RAW_LOCATION_PAYLOAD_PUBLIC=NO
RAW_PIT_PUBLIC=NO
TOKEN_FRAGMENT_PUBLIC=NO
ADC_JSON_CONTENTS_PUBLIC=NO
SOURCE_PRINCIPAL_PUBLIC=NO
RAW_PROVIDER_BODY_PUBLIC=NO
RAW_PROVIDER_HEADERS_PUBLIC=NO
```

Public success proof may record only:

```text
HTTP_STATUS=200
LOCATION_ENVELOPE_PRESENT=YES
RETURNED_LOCATION_ID_MATCH=YES
PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=YES
PACKAGE_ID_MATCH=YES
PACKAGE_DIGEST_MATCH=YES
BUSINESS_CALLS_ATTEMPTED=1
READS_ATTEMPTED=1
WRITES_ATTEMPTED=0
CRM_MUTATIONS=0
RETRY_PERFORMED=NO
```

Public failure proof may add the PR281 public error projection fields only.

## 10. Future authority separation

```text
THIS_DESIGN_CREATES_NO_GRANT=YES
THIS_DESIGN_CREATES_NO_AUTHORIZATION=YES
THIS_DESIGN_CREATES_NO_COUNTERSIGNATURE=YES

FUTURE_UNITS_REQUIRED_BEFORE_LIVE_CALL=
  1. optional offline executor wiring implementation (PR281 helpers)
  2. separate authorization artifact
  3. separate one-shot grant definition
  4. explicit human countersignature + fresh window
  5. non-consuming local gates (venv/ADC/package digest/window)
  6. single authorized attempt under the frozen call budget
```

```text
GRANT_003_CREATED_BY_THIS_UNIT=NO
GRANT_003_MAY_BE_DRAFTED_ONLY_AFTER_SEPARATE_AUTHORITY=YES
GRANT_002_REUSE_AUTHORIZED=NO
```

If the future binding validation PASSes, a later separate unit may reconsider
stage-provider validation grant drafting. PASS here does **not** clear the stage
path blocker by itself and does **not** authorize opportunity PUT.

## 11. Explicit non-actions of this unit

```text
DID_NOT_CALL_HIGHLEVEL=YES
DID_NOT_CREATE_GRANT_003=YES
DID_NOT_REUSE_GRANT_002=YES
DID_NOT_ROTATE_PIT=YES
DID_NOT_EDIT_GHL_SCOPES=YES
DID_NOT_ACCESS_SECRET_MANAGER=YES
DID_NOT_IMPERSONATE_TARGET_SA=YES
DID_NOT_REFRESH_CREDENTIALS=YES
DID_NOT_MUTATE_SRC_TESTS_CONTRACTS=YES
DID_NOT_PUBLISH_RAW_LOCATION_ID=YES
DID_NOT_PUBLISH_TOKEN_OR_PIT=YES
```

## 12. Required return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PIT_SUBACCOUNT_BINDING_VALIDATION_DESIGN_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-rest-v3-pit-subaccount-binding-validation-design-001.md

PR_CLASS=planning_only
MODE=DESIGN_ONLY_NO_LIVE_ACTIVITY

PR281_MERGE_SHA=
  19e92ad8aed498d47890fbad6c9fb0f38f91b2f6
NON_2XX_EVIDENCE_SURFACE_READY=YES

GRANT_002_CONSUMED=YES
GRANT_002_REUSE_AUTHORIZED=NO
GRANT_003_CREATED=NO

FUTURE_CALL=
  GET /locations/{private_validation_location_id}
VERSION_HEADER=v3
MAX_READS=1
MAX_WRITES=0
MAX_TOTAL_BUSINESS_CALLS=1
NO_MUTATION=YES
NO_RETRY=YES

SUCCESS_PREDICATES=
  HTTP_STATUS=200
  LOCATION_ENVELOPE_PRESENT=YES
  RETURNED_LOCATION_ID_MATCH=YES
  PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=YES

FUTURE_EXECUTOR_MUST_WIRE_PR281_NON_2XX_EVIDENCE=YES

LIVE_GHL_CALLS=0
CRM_MUTATIONS=0
VALIDATION_EXECUTION_AUTHORIZED=NO

STOP_CODE=
  NW008_PIT_SUBACCOUNT_BINDING_VALIDATION_DESIGNED_NO_GRANT_NO_LIVE_CALL

NEXT=RETURN_DESIGN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
```

## 13. Stop

```text
STOP
NO_GRANT_003
NO_LIVE_GHL_CALLS
NO_PIT_ROTATION
NO_SCOPE_EDIT
```
