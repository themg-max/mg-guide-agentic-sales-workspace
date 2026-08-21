# NW-008 AT-8H — Bounded Live NOTE Transport Implementation Proof 001

## Authorization and mode declarations

```text
PROOF_UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY

SOLE_CONSUMER_UNIT=
NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001

PR111_REVIEWED_HEAD=92325fbb358c63f6d4a2ca5da5c3cde77f774d62
PR111_MERGE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
```

```text
LIVE_NETWORK_CALLS_DURING_IMPLEMENTATION=0
HIGHLEVEL_CALLS_DURING_IMPLEMENTATION=0
CRM_MUTATIONS_DURING_IMPLEMENTATION=0
CREDENTIAL_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_ACCESS_DURING_IMPLEMENTATION=NO
NOTE_PATH_MODIFIED=NO
AT1_EXECUTION_STORE_MODIFIED=NO
PR107_TRUST_BOUNDARY_WEAKENED=NO
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
AUTOMATIC_RETRY=NO
SEARCH=NO
LIST=NO
PAGINATION=NO
RAW_REST_FALLBACK=NO
AUTHORIZATION_HEADER_LOGGING=NO
TOKEN_LOGGING=NO
AMBIGUITY_TRUTH=UNKNOWN
TEST_SUITE_ALL_PASS=YES
PHASE1_DETERMINISTIC_VALIDATION=PASS
```

## §12 proof-return fields

```text
PROOF_UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
LIVE_NETWORK_CALLS_DURING_IMPLEMENTATION=0
HIGHLEVEL_CALLS_DURING_IMPLEMENTATION=0
CRM_MUTATIONS_DURING_IMPLEMENTATION=0
CREDENTIAL_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_ACCESS_DURING_IMPLEMENTATION=NO
NOTE_PATH_MODIFIED=NO
AT1_EXECUTION_STORE_MODIFIED=NO
PR107_TRUST_BOUNDARY_WEAKENED=NO
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
AUTOMATIC_RETRY=NO
SEARCH=NO
LIST=NO
PAGINATION=NO
RAW_REST_FALLBACK=NO
AUTHORIZATION_HEADER_LOGGING=NO
TOKEN_LOGGING=NO
AMBIGUITY_TRUTH=UNKNOWN
TEST_SUITE_ALL_PASS=YES
PHASE1_DETERMINISTIC_VALIDATION=PASS
```

## Implementation

Subject path:

```text
src/integrations/ghl/highlevel_rest/live_note_transport.py
```

Transport contract:

```text
BoundedLiveNoteTransport.dispatch(method, path, body=None) -> LiveNoteResponse
```

Behavior:

- Injected HTTP client only. No urllib/socket/requests/httpx import.
- Injected synthetic credential only. Token and Authorization header are not
  stored on public call records and are redacted from `repr`.
- Exact POST `/contacts/{bound_contact_id}/notes`.
- Exact GET `/contacts/{bound_contact_id}/notes/{same_run_note_id}`.
- Same-run note id is retained only in memory after a successful POST.
- Caller-supplied contact override, caller-supplied readback note id, search,
  list, pagination, generic execute, fallback, and automatic retry are rejected
  before HTTP.
- POST timeout / 5xx / unparseable success body classify `status=ambiguous`.
- Ambiguous POST consumes the one POST budget and does not unlock GET.
- Provider envelopes are normalized to `{note: {id, body, contactId}}`.

## Exact changed paths

1. `src/integrations/ghl/highlevel_rest/live_note_transport.py`
2. `tests/integrations/ghl/highlevel_rest/test_live_note_transport.py`
3. `docs/nw008/nw-008-at8h-ghl-rest-bounded-live-note-transport-implementation-001.md`
4. `proof/nw008/at-8h/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-consumption-001.md`
5. `proof/nw008/at-8h/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-proof-001.md`

## Blocked paths not modified

```text
src/integrations/ghl/highlevel_rest/note_path.py
src/integrations/ghl/at1_execution_store.py
src/integrations/ghl/at1_live_transport_adapter.py
src/integrations/ghl/at1_live_transport_serializer.py
src/integrations/ghl/bounded_at1_executor.py
src/integrations/ghl/read_adapter.py
src/integrations/ghl/highlevel_rest/fake_transport.py
src/integrations/ghl/__init__.py
src/integrations/ghl/highlevel_rest/__init__.py
contracts/**
fixtures/**
src/orchestration/**
src/agents/**
src/mg_guide/**
workspace_addon/**
.github/**
requirements.txt
pyproject.toml
Dockerfile
.env.example
scripts/**
local/**
proof/nw008/at-10/**
```

## Required deterministic tests

```text
TEST_EXACT_POST_ROUTE=PASS
TEST_EXACT_GET_ROUTE=PASS
TEST_BOUND_CONTACT_ONLY=PASS
TEST_SAME_RUN_NOTE_ID_ONLY=PASS
TEST_POST_MAX_ONE=PASS
TEST_GET_MAX_ONE=PASS
TEST_TOTAL_CALLS_MAX_TWO=PASS
TEST_NO_RETRY=PASS
TEST_NO_SEARCH_LIST_PAGINATION=PASS
TEST_NO_ALTERNATE_TARGET=PASS
TEST_NO_GENERIC_EXECUTE=PASS
TEST_AUTH_HEADER_NOT_LOGGED=PASS
TEST_TOKEN_NOT_LOGGED=PASS
TEST_RAW_PROVIDER_RESPONSE_NOT_PUBLISHED=PASS
TEST_POST_TIMEOUT_CLASSIFIED_AMBIGUOUS=PASS
TEST_NO_SECOND_POST_AFTER_AMBIGUITY=PASS
TEST_PROVIDER_RESPONSE_NORMALIZATION=PASS
TEST_PROVIDER_NOTE_ID_ONLY_IN_MEMORY_FOR_SAME_RUN_READBACK=PASS
TEST_AT8G_DURABLE_RESERVATION_CONTRACT_UNCHANGED=PASS
TEST_PR107_TRUST_BOUNDARY_UNCHANGED=PASS
TEST_ZERO_REAL_NETWORK_CALLS=PASS
```

## Validation

```text
AT8H_TRANSPORT_TESTS=PASS
HIGHLEVEL_REST_TESTS=PASS
FULL_PYTEST_SUITE=PASS
PHASE1_DETERMINISTIC_VALIDATION=PASS
GIT_DIFF_CHECK=PASS
LIVE_HIGHLEVEL_POST=NO
LIVE_HIGHLEVEL_GET=NO
```

## Non-transitivity

```text
AT8H_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8H_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8H_AUTHORIZES_LIVE_READ=NO
AT8H_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8H_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8H_AUTHORIZES_SECRET_ACCESS=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO
NEXT=AT8H_IMPLEMENTATION_PR_GOVERNANCE_REVIEW
```
