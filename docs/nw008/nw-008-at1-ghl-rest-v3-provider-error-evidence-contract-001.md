# NW-008 AT-1 — GHL REST v3 Provider Error Evidence Contract 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PROVIDER_ERROR_EVIDENCE_CONTRACT_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-rest-v3-provider-error-evidence-contract-001.md
PR_CLASS=implementation_contract
OWNER=VS_CODE_ORCHESTRATOR

ACTION=
  IMPLEMENT_NW008_BOUNDED_PROVIDER_ERROR_EVIDENCE_SURFACE

PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
IMPLEMENTATION_BRANCH=
  impl/nw008-at1-ghl-rest-v3-provider-error-evidence-surface-001
BRANCH_IS_MAIN=NO
ABORT_IF_BRANCH_MAIN=YES

BASE_REF=origin/main
```

## 2. Controlling predecessor findings

Execution Proof 002 established a consumed GRANT_002 stop before write:

```text
GRANT_002_CONSUMED=YES
CALL_1_HTTP_STATUS=403
CALL_2_RESULT=NOT_EXECUTED
CALL_3_RESULT=NOT_EXECUTED
CRM_MUTATIONS=0
RETRY_PERFORMED=NO
PROVIDER_CONTRACT_EVALUATED=NO
PROVIDER_RUNTIME_RESULT=UNKNOWN
STAGE_PATH_BLOCKER_CLEARED=NO
```

Human HighLevel scope evidence (names only; no PIT material):

```text
PRIVATE_INTEGRATION_NAME=MG_Guide
OPPORTUNITIES_READONLY_PRESENT=YES
OPPORTUNITIES_WRITE_PRESENT=YES
CONTACTS_READONLY_PRESENT=YES
CONTACTS_WRITE_PRESENT=YES
LOCATIONS_READONLY_PRESENT=YES
GHL_SCOPE_REMEDIATION_REQUIRED=NO
```

This unit does **not** create GRANT_003, rotate PIT, edit scopes, call HighLevel,
refresh credentials, impersonate the runtime SA, or access Secret Manager.

```text
NO_LIVE_GHL_CALLS=YES
NO_SECRET_MANAGER_ACCESS=YES
NO_TARGET_SA_IMPERSONATION=YES
NO_CREDENTIAL_REFRESH=YES
DO_NOT_CREATE_GRANT_003=YES
DO_NOT_ROTATE_PIT=YES
DO_NOT_EDIT_GHL_SCOPES=YES
```

## 3. Problem statement

Proof 002 could record only HTTP status for CALL_1. The bounded HTTP result
surface did not carry response headers, so offline executors could not derive a
private diagnostic envelope or a public-safe presence projection for definitive
non-2xx provider responses.

This contract freezes the minimum offline evidence surface required before any
future countersigned re-validation grant.

## 4. Response structure contract

`LiveNoteHttpResult` MUST carry:

```text
status_code: int
body: bytes
headers: Mapping[str, str]
```

```text
HEADERS_OPTIONAL_FOR_BACK_COMPAT=YES
DEFAULT_HEADERS_EMPTY_MAPPING=YES
HEADERS_NOT_PUBLIC_WHOLESALE=YES
```

Concrete stdlib session capture MUST populate `headers` from the definitive
provider response (including HTTPError responses) while dropping credential-
bearing header names during normalization.

Preserved transport/client invariants:

```text
AUTOMATIC_RETRY=NO
ALTERNATE_ROUTE=NO
GENERIC_REST_FALLBACK=NO
allow_redirects=False
REQUEST_TIMEOUT_SECONDS=10.0
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
CONTACT_GET_ATTEMPTS_MAX=1
```

## 5. Private provider error evidence

For definitive non-2xx responses only, derive privately:

```text
PROVIDER_HTTP_STATUS
CONTENT_TYPE
CONTENT_TYPE_CLASS
RESPONSE_BODY_LENGTH
RESPONSE_BODY_SHA256

PROVIDER_ERROR_ENVELOPE_PARSEABLE
PROVIDER_ERROR_CODE
PROVIDER_ERROR_MESSAGE

PROVIDER_REQUEST_ID
PROVIDER_CORRELATION_ID

PROVIDER_ERROR_CLASS
PROVIDER_ERROR_CAUSE
```

Rules:

```text
NON_2XX_ONLY=YES
SUCCESS_PATH_DOES_NOT_DERIVE_ERROR_EVIDENCE=YES
AUTHORIZATION_REQUEST_HEADER_NEVER_ENTERED=YES
UNKNOWN_HEADERS_IGNORED_FOR_PUBLIC_PROJECTION=YES
```

Request/correlation ID capture uses a small explicit alias allowlist only:

```text
REQUEST_ID_ALIASES=
  x-request-id
  request-id
  x-amzn-requestid
  x-amz-request-id
  x-amzn-trace-id

CORRELATION_ID_ALIASES=
  x-correlation-id
  correlation-id
  x-correlationid
  cf-ray
  traceparent
  x-trace-id
  trace-id
```

Content-type class:

```text
PROVIDER_CONTENT_TYPE_CLASS=
  JSON | TEXT | HTML | EMPTY | OTHER | UNKNOWN
```

## 6. Public projection contract

Public artifacts may expose only:

```text
PROVIDER_HTTP_STATUS

PROVIDER_CONTENT_TYPE_CLASS=
  JSON|TEXT|HTML|EMPTY|OTHER|UNKNOWN

PROVIDER_ERROR_ENVELOPE_PRESENT=YES|NO|UNKNOWN
PROVIDER_ERROR_CODE_PRESENT=YES|NO
PROVIDER_ERROR_MESSAGE_PRESENT=YES|NO

PROVIDER_REQUEST_ID_PRESENT=YES|NO
PROVIDER_CORRELATION_ID_PRESENT=YES|NO

PROVIDER_ERROR_CLASS=
  AUTHENTICATION|
  AUTHORIZATION|
  REQUEST_VALIDATION|
  NOT_FOUND|
  CONFLICT|
  RATE_LIMIT|
  PROVIDER_FAILURE|
  UNKNOWN

PROVIDER_ERROR_CAUSE=
  <bounded classification or UNKNOWN>

RAW_PROVIDER_RESPONSE_PUBLISHED=NO
PROVIDER_ERROR_MESSAGE_PUBLISHED=NO
PROVIDER_REQUEST_ID_PUBLISHED=NO
PROVIDER_CORRELATION_ID_PUBLISHED=NO
AUTHORIZATION_HEADER_PUBLISHED=NO
TOKEN_OR_PIT_PUBLISHED=NO
```

```text
RAW_PROVIDER_BODY_PUBLIC=FORBIDDEN
RAW_PROVIDER_HEADERS_PUBLIC=FORBIDDEN
RAW_ERROR_MESSAGE_PUBLIC=FORBIDDEN
RAW_REQUEST_ID_PUBLIC=FORBIDDEN
RAW_CORRELATION_ID_PUBLIC=FORBIDDEN
PIT_OR_TOKEN_PUBLIC=FORBIDDEN
```

## 7. Classification contract

HTTP class mapping:

```text
400/422 -> REQUEST_VALIDATION
401     -> AUTHENTICATION
403     -> AUTHORIZATION
404     -> NOT_FOUND
409     -> CONFLICT
429     -> RATE_LIMIT
5xx     -> PROVIDER_FAILURE
other   -> UNKNOWN
```

```text
HTTP_CLASS_DOES_NOT_ESTABLISH_DETAILED_CAUSE=YES
DEFAULT_PROVIDER_ERROR_CAUSE=UNKNOWN
```

Example for Proof 002-class 403:

```text
PROVIDER_HTTP_STATUS=403
PROVIDER_ERROR_CLASS=AUTHORIZATION
PROVIDER_ERROR_CAUSE=UNKNOWN
```

unless a later bounded private parser supplies stronger cause evidence under a
separate authorization.

## 8. Implementation binding

```text
IMPLEMENTATION_MODULES=
  src/integrations/ghl/highlevel_rest/live_note_transport.py
  src/integrations/ghl/highlevel_rest/live_note_http_client.py

TEST_MODULES=
  tests/integrations/ghl/highlevel_rest/test_provider_error_evidence.py
  tests/integrations/ghl/highlevel_rest/test_live_note_http_client.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py

PUBLIC_HELPERS=
  LiveNoteHttpResult
  PrivateProviderErrorEvidence
  PublicProviderErrorProjection
  normalize_provider_response_headers
  classify_content_type
  classify_provider_error_class
  derive_private_provider_error_evidence
  project_public_provider_error_evidence
  public_provider_error_projection_from_result
```

## 9. Deterministic fixture obligations

Network-zero fixtures MUST cover:

```text
403 JSON + correlation/request headers
403 JSON no correlation headers
403 non-JSON
403 empty body
401 JSON
422 validation envelope
429 response
500 text/HTML
malformed JSON
existing 2xx success path unchanged
```

Required verification predicates:

```text
NON_2XX_STATUS_CAPTURED=YES
CONTENT_TYPE_CLASSIFIED=YES
ERROR_ENVELOPE_CLASSIFIED=YES
REQUEST_ID_PRESENCE_CAPTURED=YES
SUCCESS_PATH_UNCHANGED=YES
AUTOMATIC_RETRY=NO
ALTERNATE_ROUTE=NO
CALL_BUDGET_UNCHANGED=YES
AUTHORIZATION_HEADER_NEVER_PERSISTED=YES
RAW_TOKEN_NEVER_PERSISTED=YES
RAW_PROVIDER_ERROR_NOT_PUBLIC=YES
```

## 10. Explicit non-actions

```text
DID_NOT_CALL_HIGHLEVEL=YES
DID_NOT_ACCESS_SECRET_MANAGER=YES
DID_NOT_IMPERSONATE_TARGET_SA=YES
DID_NOT_REFRESH_CREDENTIALS=YES
DID_NOT_CREATE_GRANT_003=YES
DID_NOT_ROTATE_PIT=YES
DID_NOT_EDIT_GHL_SCOPES=YES
DID_NOT_RETRY_GRANT_002=YES
DID_NOT_PUBLISH_RAW_PROVIDER_BODY=YES
DID_NOT_PUBLISH_RAW_PROVIDER_HEADERS=YES
DID_NOT_PUBLISH_TOKEN_OR_PIT=YES
```

## 11. Required return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PROVIDER_ERROR_EVIDENCE_CONTRACT_001

NON_2XX_EVIDENCE_SURFACE_READY=YES
NO_LIVE_GHL_ACTIVITY=YES
NO_GRANT_003_CREATED=YES

PROVIDER_HTTP_RESULT_HEADERS_BOUND=YES
PRIVATE_ERROR_EVIDENCE_DERIVATION_BOUND=YES
PUBLIC_ERROR_PROJECTION_BOUND=YES
CLASSIFICATION_BOUND=YES
SUCCESS_PATH_UNCHANGED=YES

NEXT=RETURN_IMPLEMENTATION_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
```

## 12. Stop

```text
STOP
```
