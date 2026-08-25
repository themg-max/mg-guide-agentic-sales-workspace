# NW008 AT8W30 R3 Exact GET Contact Transport Capability Authorization 001

## 1. Authorization identity and classification

```text
AUTHORIZATION_ID=
  NW008_AT8W30_R3_EXACT_GET_CONTACT_TRANSPORT_CAPABILITY_AUTHORIZATION_001
UNIT=
  NW008_AT8W30_R3_EXACT_GET_CONTACT_TRANSPORT_CAPABILITY_AUTHORIZATION_001

CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=IMPLEMENTATION_AUTHORIZATION_ONLY

PURPOSE=
  AUTHORIZE_ONE_BOUNDED_FUTURE_REPOSITORY_IMPLEMENTATION_THAT_ADDS_THE
  ALREADY_CONTRACTED_EXACT_BOUND_CONTACT_READ_ONLY_GET_CAPABILITY_TO_THE
  EXISTING_BOUNDED_LIVE_NOTE_TRANSPORT

THIS_ARTIFACT_IMPLEMENTATION=NO
THIS_ARTIFACT_EXECUTES_R3=NO
THIS_ARTIFACT_CALLS_HIGHLEVEL=NO
AUTHORIZATION_ONLY=YES
```

This artifact grants narrowly bounded implementation authority only. It does
not implement the transport capability, invoke the production runtime, execute
R3, or authorize any external effect.

## 2. Durable PR212 prerequisite

The grant is based on the canonical `origin/main` state containing merged PR
#212 and its unchanged reviewed authorization blob.

```text
PR212_MERGED=YES
PR212_MERGE_COMMIT=
  3a221fcea0191100860f5bde38a4d34f871997cf

PR212_REVIEWED_HEAD=
  dbf07f88e9db3b36d8ef39af8fdd5a67e90665f0

PR212_REVIEWED_HEAD_ANCESTRY=PASS
PR212_AUTHORIZATION_ON_MAIN=YES
PR212_AUTHORIZATION_BLOB_MATCH=YES

R3_AUTHORIZATION_DESIGN_DURABLE=YES

CURRENT_GET_BOUND_CONTACT_SUCCESS_PATH_REACHABLE=NO
R3_EXECUTION_AUTHORIZABLE_NOW=NO
R3_AUTHORIZATION_READY=NO

R3_EXECUTION_BLOCKED_ON=
  EXACT_GET_CONTACT_TRANSPORT_CAPABILITY_NOT_DURABLE

NEXT_REQUIRED_UNIT=
  NW008_AT8W30_R3_EXACT_GET_CONTACT_TRANSPORT_CAPABILITY_AUTHORIZATION_001
```

If any statement in this prerequisite block is false, this authorization is
invalid and the future implementation must stop without repository mutation:

```text
STOP_CODE=PR212_DURABLE_PREREQUISITE_FAILED
```

## 3. Existing contract binding

The future implementation is bound to the existing operation:

```text
CONTRACT=
  contracts/highlevel_rest_adapter_v1.yaml#get_contact

METHOD=GET
PATH=/contacts/{contactId}
CONTACT_ID_SOURCE=PRIVATE_BOUND_CONTACT_ONLY
QUERY_ALLOWED=NO
MUTATION=NO
PURPOSE=verify_bound_contact
IMPLEMENTATION_SLICE=NOTE_PATH

CONSUME_ONLY=
  contact.id|
  contact.locationId

CONTRACT_CHANGE_AUTHORIZED=NO
```

The contract must not be modified under this grant.

## 4. Authorized future implementation paths

Only these paths may be changed by the future implementation:

```text
AUTHORIZED_FUTURE_PATHS=
  src/integrations/ghl/highlevel_rest/live_note_transport.py|
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py|
  proof/nw008/at-8w30/nw008-at8w30-r3-exact-get-contact-transport-capability-implementation-proof-001.md
```

Any additional path requires an immediate stop and separate authorization.

The following paths and path classes are not authorized by default:

```text
NOT_AUTHORIZED_BY_DEFAULT=
  src/integrations/ghl/highlevel_rest/note_path.py|
  src/integrations/ghl/highlevel_rest/live_note_runtime.py|
  contracts/**|
  requirements*|
  .github/workflows/**|
  deploy/**|
  infra/**
```

## 5. Required exact bound-contact capability

```text
EXACT_BOUND_CONTACT_GET_REQUIRED=YES
EXACT_ROUTE=
  GET /contacts/{bound_contact_id}

BOUND_CONTACT_ONLY=YES
GET_ONLY=YES
REQUEST_BODY_ALLOWED=NO
QUERY_ALLOWED=NO

ALTERNATE_CONTACT_ALLOWED=NO
CALLER_CONTACT_OVERRIDE_ALLOWED=NO
CALLER_URL_OVERRIDE_ALLOWED=NO
CALLER_ROUTE_OVERRIDE_ALLOWED=NO

SEARCH_ALLOWED=NO
LIST_ALLOWED=NO
PAGINATION_ALLOWED=NO
RAW_REST_ALLOWED=NO
GENERIC_EXECUTE_ALLOWED=NO
RETRY_ALLOWED=NO
FALLBACK_ALLOWED=NO

CONTACT_GET_MUTATION_COUNT=0
```

The capability may target only the privately bound contact identifier. It may
not expose a generic request surface or accept caller-selected targets, URLs,
routes, query parameters, fragments, request bodies, or alternate contact
identifiers.

## 6. Response minimization and fail-closed behavior

The provider response may contain additional contact data. The future
transport output must expose only:

```text
RESPONSE_MINIMIZATION=
  contact.id|
  contact.locationId

FULL_CONTACT_PAYLOAD_LOGGING=FORBIDDEN
FULL_CONTACT_PAYLOAD_PERSISTENCE=FORBIDDEN
UNRELATED_CONTACT_FIELDS_PUBLISHED=NO
```

The future implementation must fail closed for every one of these conditions:

- malformed provider envelope;
- missing `contact.id`;
- missing `contact.locationId`;
- non-2xx response;
- identifier mismatch during semantic validation; or
- transport uncertainty.

No full provider contact payload may be logged, persisted, returned, published,
or included in proof.

## 7. Existing NOTE-route preservation

The future implementation must preserve these exact existing routes and their
behavior:

```text
EXISTING_NOTE_ROUTES=
  POST /contacts/{bound_contact_id}/notes|
  GET /contacts/{bound_contact_id}/notes/{same_run_note_id}

EXISTING_NOTE_ROUTE_BEHAVIOR_CHANGE_AUTHORIZED=NO
EXISTING_NOTE_ROUTES_UNCHANGED_REQUIRED=YES

NOTE_POST_BUDGET_WEAKENING_AUTHORIZED=NO
NOTE_GET_BUDGET_WEAKENING_AUTHORIZED=NO

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_RAW_REST=YES
NO_ALTERNATE_TARGET=YES
NO_ALTERNATE_ROUTE=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES
```

## 8. Network-budget design guard

The current transport has:

```text
CURRENT_TOTAL_NETWORK_CALLS_MAX=2
```

The future implementation must not simply increase that value to three. It
must prove the intended contact-preflight plus NOTE-workflow state model while
preserving the frozen NOTE-path budget.

Explicit route- and state-specific counters and guards are preferred. The
implementation and deterministic tests must prove:

```text
CONTACT_GET_ATTEMPTS_MAX=1
SECOND_CONTACT_GET=REJECTED

CONTACT_GET_DOES_NOT_AUTHORIZE_OR_INCREMENT_MUTATION=YES
NOTE_POST_EXISTING_LIMITS_UNCHANGED=YES
NOTE_READBACK_EXISTING_LIMITS_UNCHANGED=YES
```

If the existing object lifecycle makes any of these requirements
contradictory, implementation must stop. It must not improvise or authorize a
broader network budget.

```text
STOP_CODE=TRANSPORT_NETWORK_BUDGET_MODEL_REQUIRES_DESIGN_REVIEW
```

## 9. Deterministic test obligations

The future implementation must add synthetic, offline deterministic coverage
for at least:

```text
CASE_EXACT_BOUND_CONTACT_GET=PASS
CASE_CONTACT_GET_MINIMIZES_RESPONSE=PASS
CASE_CONTACT_GET_REJECTS_BODY=PASS
CASE_CONTACT_GET_REJECTS_ALTERNATE_CONTACT=PASS
CASE_CONTACT_GET_REJECTS_QUERY=PASS
CASE_CONTACT_GET_REJECTS_FRAGMENT=PASS
CASE_CONTACT_GET_MAX_ONE_ATTEMPT=PASS
CASE_SECOND_CONTACT_GET_REJECTED=PASS
CASE_CONTACT_GET_NETWORK_FAILURE_FAILS_CLOSED=PASS

CASE_NOTE_POST_UNCHANGED=PASS
CASE_NOTE_GET_UNCHANGED=PASS

CASE_NO_SEARCH_LIST_PAGINATION=PASS
CASE_NO_GENERIC_RAW_REST=PASS
CASE_ZERO_MUTATION_FOR_CONTACT_GET=PASS

ALL_TESTS_SYNTHETIC_OFFLINE=YES
SOCKET_NETWORK_CALLS=0
REAL_HIGHLEVEL_CALLS=0
REAL_SECRET_READS=0
```

No test under this grant may dispatch a socket network call, invoke the real
provider, read a real secret, mint a token, open a live SQLite store, mutate
CRM state, or exercise production runtime.

## 10. One-shot implementation authority

```text
ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
FAILURE_RESTORES_AUTHORITY=NO

AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_AUTHORIZED_REPOSITORY_IMPLEMENTATION_MUTATION_ATTEMPT
```

Once consumed, this authority permits no widening writable scope, live
validation, alternate implementation surface, contract change, runtime
invocation, or external repair. Any scope defect after consumption fails
closed and requires fresh authority.

## 11. External-effect budget

Both this authorization unit and the future repository implementation are
bounded to zero real external effects:

```text
HIGHLEVEL_CALLS_MAX=0
HTTP_REQUEST_DISPATCHES_TO_REAL_PROVIDER_MAX=0

SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=0

SECRET_PAYLOAD_READS_MAX=0
SQLITE_LIVE_OPENS_MAX=0

CRM_MUTATIONS_MAX=0
NOTE_WRITES_MAX=0
STAGE_TRANSITIONS_MAX=0

IAM_MUTATIONS_MAX=0
SERVICE_ACCOUNT_KEYS_CREATED_MAX=0

DEPLOYMENTS_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0

R3_EXECUTION_AUTHORIZED_BY_THIS_GRANT=NO
R4_AUTHORIZED=NO
```

## 12. Required future implementation proof

The future implementation must create:

```text
REQUIRED_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w30/nw008-at8w30-r3-exact-get-contact-transport-capability-implementation-proof-001.md
```

That proof must record:

```text
AUTHORIZATION_ID
AUTHORIZATION_STATE=CONSUMED
AUTHORIZED_CHANGED_PATHS
ACTUAL_CHANGED_PATHS

EXACT_BOUND_CONTACT_GET_IMPLEMENTED=<YES|NO>

CONTACT_GET_ATTEMPTS_MAX=1

RESPONSE_MINIMIZATION=
  contact.id|contact.locationId

EXISTING_NOTE_ROUTES_UNCHANGED=<YES|NO>

DETERMINISTIC_TESTS=<PASS|FAIL>

HIGHLEVEL_CALLS=0
REAL_HTTP_REQUESTS=0
REAL_SECRET_READS=0
TOKEN_MINTS=0
SQLITE_LIVE_OPENS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

RESULT=<PASS|FAIL>
STOP_CODE=<NONE|exact code>

IMPLEMENTATION_SUCCESS_AUTHORIZES_R3_EXECUTION=NO
```

The proof may contain only deterministic repository evidence and minimized,
non-secret results. Implementation success does not authorize R3 execution.

## 13. Scope of this authorization PR

This authorization PR itself may change only:

```text
AUTHORIZED_PR_PATH=
  governance/authorizations/nw008-at8w30-r3-exact-get-contact-transport-capability-authorization-001.md
```

```text
TRANSPORT_IMPLEMENTED_IN_THIS_PR=NO
R3_EXECUTION_PERFORMED=NO
RUNTIME_SOURCE_CHANGES_IN_THIS_PR=0
```

The authorization artifact must be the sole changed path in this PR. It must
be staged explicitly; broad staging such as `git add .` is forbidden.

## 14. Authorization-unit effect attestation

Creation and validation of this artifact use repository-only inspection and
Git operations. They do not assemble or start runtime code.

```text
AUTHORIZATION_ARTIFACTS_CREATED=1
REPOSITORY_PATHS_MODIFIED=1
RUNTIME_SOURCE_CHANGES=0

HIGHLEVEL_CALLS=0
REAL_HTTP_REQUESTS=0
HTTP_REQUEST_DISPATCHES_TO_REAL_PROVIDER=0

SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
TOKEN_MINTS=0
REAL_SECRET_READS=0
SQLITE_LIVE_OPENS=0

CRM_MUTATIONS=0
NOTE_WRITES=0
STAGE_TRANSITIONS=0

IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0

DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0

R3_EXECUTION_PERFORMED=NO
R4_AUTHORIZED=NO
```

## 15. Review disposition

```text
PR_CLASS=authorization
AUTHORIZATION_ONLY=YES

PR212_DURABLE=YES
EXACT_BOUND_CONTACT_GET_REQUIRED=YES
EXACT_ROUTE=
  GET /contacts/{bound_contact_id}

CONTACT_GET_ATTEMPTS_MAX=1
EXISTING_NOTE_ROUTES_UNCHANGED_REQUIRED=YES

ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO

HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

AUTHORIZATION_READY_FOR_REVIEW=YES

NEXT=
  RETURN_AUTHORIZATION_PR_AND_EXACT_HEAD_TO_CHATGPT_FOR_INDEPENDENT
  GOVERNANCE_REVIEW
```
