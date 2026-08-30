# NW-008 AT1 GHL REST v3 Bounded-Read Authorization 001

## 0. Authorization identity and current state

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/nw-008-at1-ghl-rest-v3-bounded-read-authorization-001.md
CLASSIFICATION=AUTHORIZATION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_BRANCH=
  authorization/nw008-at1-ghl-rest-v3-bounded-read-authorization-001
BASE_REF=origin/main
BASE_SHA=
  2c154ab28a6967401f24343fd6586ff740f6bcb0
BRANCH_IS_MAIN=NO

AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
```

This artifact defines, but does not activate, the maximum bounds of one possible
future HighLevel REST v3 read. Authoring, reviewing, committing, pushing, or
merging this artifact does not authorize credential access, provider dispatch,
CRM access, or any mutation. The later read may occur only after every gate in
section 6 is satisfied by separate authority.

## 1. Exact merged PR #335 prerequisite

```text
PR_335=MERGED
PR_335_REVIEWED_HEAD=
  c55de028a1acca73ebbbd913a48c88834c1b0a63
PR_335_REVIEW_ID=
  5060126041
PR_335_MERGE_SHA=
  2c154ab28a6967401f24343fd6586ff740f6bcb0
PR_335_MERGE_PRESENT_ON_ORIGIN_MAIN=YES
AUTHORIZATION_BASE_EQUALS_PR_335_MERGE_SHA=YES
PR_335_REVIEWED_HEAD_IS_ANCESTOR_OF_ORIGIN_MAIN=YES

SOURCE_PROOF_ID=
  NW008_AT1_GHL_NOTE_RUNTIME_CREDENTIAL_BOUNDARY_DIAGNOSTIC_EXECUTION_PROOF_001
SOURCE_PROOF_PATH=
  proof/nw008/nw-008-at1-ghl-note-runtime-credential-boundary-diagnostic-execution-proof-001.md
SOURCE_PROOF_BLOB_SHA=
  bd629bb2c64672fe68165361caa49c4f47f8a1a5

CREDENTIAL_BOUNDARY_PROVEN=YES
CREDENTIAL_ACCESS_ATTEMPTS=1
ACCESS_SECRET_VERSION_CALLS=1
CREDENTIAL_ACCESS_RESULT=PASS

SECRET_VALUE_PUBLISHED=NO
SECRET_VALUE_PERSISTED=NO
SECRET_VALUE_LOGGED=NO
SECRET_VALUE_ECHOED=NO
SECRET_VALUE_EXPORTED=NO

GHL_CALLS=0
CRM_CALLS=0
```

The exact reviewed head, review record, merge commit, source-proof identity, and
source-proof blob above are inseparable. A mismatch invalidates this definition.
PR #335 proves only that the dedicated note-runtime identity crossed the frozen
credential boundary once without disclosing the secret and without contacting
HighLevel or CRM. It grants no provider-read or write authority.

## 2. Consumed prior authority

```text
ISSUE_334_REUSE_ALLOWED=NO
PR_333_ACTIVATION_REUSE_ALLOWED=NO
NO_SECOND_ACCESS_SECRET_VERSION_UNDER_THIS_ACTIVATION=YES

PR_335_USED_AS_CREDENTIAL_BOUNDARY_PROOF_ONLY=YES
PR_335_USED_AS_EXECUTION_AUTHORITY=NO
PR_333_USED_AS_THIS_READ_ACTIVATION=NO
ISSUE_334_USED_AS_THIS_READ_CONSUMPTION_RECORD=NO

PR_98_EXECUTION_AUTHORITY_REUSE_ALLOWED=NO
AT8_EXECUTION_AUTHORITY_REUSE_ALLOWED=NO
CANONICAL_PRIVATE_BINDING_USED_AS_TARGET_DATA_AUTHORITY_ONLY=YES
PRIOR_READ_AUTHORITY_REUSED=NO
```

Neither issue #334, the PR #333 activation, the PR #335 proof, nor any earlier
contact-read grant may be reused, revived, transferred, or treated as authority
for the later GET. The standing canonical private binding identifies the target
data only; it does not authorize execution.

## 3. Exact bounded-read contract

### 3.1 Resolved operation

```text
GHL_REST_API_VERSION=V3
GHL_BASE_URL=https://services.leadconnectorhq.com
HTTP_METHOD=GET
GHL_READ_ENDPOINT=
  https://services.leadconnectorhq.com/contacts/{PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT}

GHL_LOCATION_ID=PRIVATE_ALLOWLIST_EXACT_CANONICAL_LOCATION
GHL_OBJECT_TYPE=CONTACT
GHL_OBJECT_ID=PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT
EXPECTED_RESPONSE_ID=PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT

GHL_LOCATION_ID_RESOLVED=YES
GHL_OBJECT_TYPE_RESOLVED=YES
GHL_OBJECT_ID_RESOLVED=YES
EXPECTED_RESPONSE_ID_RESOLVED=YES
REQUIRED_FIELDS_UNKNOWN=NO
CONTRACT_RESOLUTION_COMPLETE=YES
```

`PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT` and
`PRIVATE_ALLOWLIST_EXACT_CANONICAL_LOCATION` are exact, non-caller-selectable
bindings maintained by the private control plane. They are not wildcards,
search terms, test-fixture literals, or permission to choose an alternate
record. Their raw values remain excluded from this public repository under the
standing binding boundary.

The endpoint resolves at later execution only by substituting the one privately
bound `GHL_OBJECT_ID` into the fixed `/contacts/{contactId}` contract. No other
path substitution or query component is allowed.

### 3.2 Repository and provider authority

```text
TRANSPORT_IMPLEMENTATION_AUTHORITY=
  src/integrations/ghl/highlevel_rest/live_note_transport.py
TRANSPORT_BASE_URL_SYMBOL=BASE_URL
TRANSPORT_BASE_URL_VALUE=https://services.leadconnectorhq.com
TRANSPORT_API_VERSION_SYMBOL=API_VERSION
TRANSPORT_API_VERSION_VALUE=v3

REST_CONTRACT_AUTHORITY=
  contracts/highlevel_rest_adapter_v1.yaml#provider_operations.get_contact
REST_CONTRACT_METHOD=GET
REST_CONTRACT_PATH=/contacts/{contactId}
REST_CONTRACT_PATH_BINDING=
  contactId=private_binding.contact_id
REST_CONTRACT_RESPONSE_ENVELOPE=contact
REST_CONTRACT_ID_SELECTOR=contact.id
REST_CONTRACT_LOCATION_SELECTOR=contact.locationId

CANONICAL_BINDING_AUTHORITY=
  governance/authorizations/MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1.yaml
CANONICAL_BINDING_EVIDENCE=
  proof/canonical-synthetic-read-binding-v1/synthetic-record-binding.yaml
SYNTHETIC_CONTACT_BOUND=YES
PRIVATE_ALLOWLIST_COMPLETE=YES
PIT_CANONICAL_LOCATION_VERIFIED=YES
RAW_IDENTIFIER_PUBLICATION_REQUIRED=NO

KNOWN_OBJECT_PROOF=
  proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md
KNOWN_OBJECT_PRIOR_EXACT_GET_EXECUTED=YES
KNOWN_OBJECT_PRIOR_CONTACT_ID_MATCH=YES
KNOWN_OBJECT_PRIOR_LOCATION_ID_MATCH=YES
KNOWN_OBJECT_CLASS=SYNTHETIC_ONLY
```

The earlier successful read is evidence that the exact private binding
identified one known synthetic contact in the canonical location. Its consumed
authority is not reused. The future execution must freshly revalidate that the
same exact object and location remain valid before consuming this authorization.

### 3.3 Required response identity proof

```text
ALLOWED_RESPONSE_FIELD_1=contact.id
ALLOWED_RESPONSE_FIELD_2=contact.locationId
OTHER_RESPONSE_FIELD_CONSUMPTION_ALLOWED=NO

REQUIRE_CONTACT_ID_MATCH=
  contact.id == PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT
REQUIRE_LOCATION_ID_MATCH=
  contact.locationId == PRIVATE_ALLOWLIST_EXACT_CANONICAL_LOCATION
EXPECTED_OBJECT_IDENTITY_PROOF_REQUIRED=YES
FULL_PROVIDER_RESPONSE_LOG_ALLOWED=NO
FULL_PROVIDER_RESPONSE_PERSIST_ALLOWED=NO
RAW_PROVIDER_RESPONSE_PUBLISH_ALLOWED=NO
```

A missing envelope, missing identity field, schema variation, object mismatch,
or location mismatch is terminal failure. It does not permit a search, fallback,
alternate target, second request, or mutation.

### 3.4 Unresolved-field stop rule

```text
IF_ANY_REQUIRED_FIELD_UNKNOWN_OR_MISMATCHED:
  AUTHORIZATION_EFFECTIVE=NO
  ACTIVATION_EFFECTIVE=NO
  EXECUTION_AUTHORIZED=NO
  STOP=RETURN_FOR_REVIEW
```

No unresolved value may be inferred from a credential, error response, search,
list, adjacent object, caller input, or test fixture.

## 4. Frozen ceilings and prohibitions

### 4.1 One-read ceiling

```text
MAX_GHL_REST_CALLS=1
MAX_GHL_READ_ATTEMPTS=1

NO_RETRY=YES
NO_SECOND_ATTEMPT=YES
NO_COMPENSATING_EXECUTION=YES

SEARCH_ALLOWED=NO
LIST_ALLOWED=NO
PAGINATION_ALLOWED=NO

ALTERNATE_ENDPOINT_ALLOWED=NO
ALTERNATE_LOCATION_ALLOWED=NO
ALTERNATE_OBJECT_ALLOWED=NO

QUERY_PARAMETERS_ALLOWED=NO
REQUEST_BODY_ALLOWED=NO
REDIRECT_FOLLOWING_ALLOWED=NO
FALLBACK_ALLOWED=NO
```

Timeout, disconnect, ambiguous completion, definitive non-2xx response,
unexpected schema, or identity mismatch consumes the future one-shot attempt
and requires an immediate stop.

### 4.2 Zero write authority

```text
POST_ALLOWED=NO
PUT_ALLOWED=NO
PATCH_ALLOWED=NO
DELETE_ALLOWED=NO

CRM_MUTATION_ALLOWED=NO
CONTACT_MUTATION_ALLOWED=NO
OPPORTUNITY_MUTATION_ALLOWED=NO
OPPORTUNITY_STAGE_CHANGE_ALLOWED=NO
NOTE_CREATE_ALLOWED=NO
NOTE_UPDATE_ALLOWED=NO

CRM_MUTATIONS_MAX=0
CONTACT_MUTATIONS_MAX=0
OPPORTUNITY_MUTATIONS_MAX=0
OPPORTUNITY_STAGE_CHANGES_MAX=0
NOTE_CREATES_MAX=0
NOTE_UPDATES_MAX=0
```

### 4.3 Secret, IAM, deployment, and lane boundaries

```text
SECRET_VALUE_PUBLISH_ALLOWED=NO
SECRET_VALUE_PERSIST_ALLOWED=NO
SECRET_VALUE_LOG_ALLOWED=NO
SECRET_VALUE_ECHO_ALLOWED=NO
SECRET_VALUE_EXPORT_ALLOWED=NO

IAM_MUTATION_ALLOWED=NO
SECRET_MUTATION_ALLOWED=NO
SERVICE_ACCOUNT_KEY_CREATE_ALLOWED=NO
DEPLOYMENT_ALLOWED=NO
LANE_A_WORK_ALLOWED=NO

FRESH_CREDENTIAL_ACCESS_AUTHORITY_REQUIRED=YES
CREDENTIAL_ACCESS_AUTHORIZED_BY_THIS_UNIT=NO
STANDING_TOKEN_AUTHORITY=NO
```

## 5. Authorization-unit zero-effect ledger

```text
GHL_REST_CALLS=0
GHL_READ_ATTEMPTS=0
GHL_CALLS=0
CRM_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0

CREDENTIAL_ACCESS_ATTEMPTS_IN_THIS_UNIT=0
ACCESS_SECRET_VERSION_CALLS_IN_THIS_UNIT=0
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_IN_THIS_UNIT=0
ACCESS_TOKEN_MINTS_IN_THIS_UNIT=0

IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
LANE_A_WORK=0

HTTP_REQUEST_DISPATCHES=0
NETWORK_OPERATIONS_AGAINST_GHL=0
CRM_OPERATIONS=0
EXECUTION_PERFORMED=NO
```

This authorization unit performs no GHL or CRM operation. It does not access a
secret value, mint a token, instantiate a provider client, open a provider
connection, or consume future execution authority.

## 6. Mandatory later authority chain

The bounded GET remains forbidden unless a later unit records and verifies all
of the following in order:

```text
INDEPENDENT_AUTHORIZATION_REVIEW_REQUIRED=YES
AUTHORIZATION_MERGE_REQUIRED=YES
SEPARATE_HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_EXECUTION_AUTHORITY_REQUIRED=YES

FRESH_ONE_SHOT_CONSUMPTION_REQUIRED=YES
CONSUMPTION_BEFORE_CREDENTIAL_OR_PROVIDER_ACCESS_REQUIRED=YES
CONSUMPTION_TERMINAL_NON_REUSABLE_REQUIRED=YES

IMMEDIATE_CREDENTIAL_REVALIDATION_REQUIRED=YES
IMMEDIATE_ENDPOINT_REVALIDATION_REQUIRED=YES
IMMEDIATE_OBJECT_REVALIDATION_REQUIRED=YES
IMMEDIATE_LOCATION_REVALIDATION_REQUIRED=YES

EXACTLY_ONE_GET_REQUIRED=YES
EXPECTED_OBJECT_IDENTITY_PROOF_REQUIRED=YES
TERMINAL_CONSUMPTION_REQUIRED=YES
EXECUTION_PROOF_REQUIRED=YES
```

The later activation and explicit execution authority must bind this exact
reviewed artifact, a fresh immutable window, a fresh run identity, the exact
credential source and consumer identity, the fixed base URL and endpoint, the
two exact private target bindings, the one-call budget, the terminal consumption
record, and the execution-proof destination.

```text
IF_REVIEW_ABSENT=STOP
IF_MERGE_ABSENT=STOP
IF_HUMAN_ACTIVATION_ABSENT=STOP
IF_EXPLICIT_EXECUTION_AUTHORITY_ABSENT=STOP
IF_FRESH_CONSUMPTION_ABSENT=STOP
IF_REVALIDATION_FAILS=STOP
IF_ANY_BOUND_VALUE_DRIFTS=STOP

AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
STOP=FOR_INDEPENDENT_AUTHORIZATION_REVIEW
```
