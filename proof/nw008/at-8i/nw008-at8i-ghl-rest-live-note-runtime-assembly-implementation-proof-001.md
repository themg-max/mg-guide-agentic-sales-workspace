# NW-008 AT-8I — GHL REST Live Note Runtime Assembly Implementation Proof 001

## Authorization and mode declarations

```text
PROOF_UNIT=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md
AUTHORIZATION_PR=114
AUTHORIZATION_REVIEWED_HEAD=58322a50f8339c8de00c64fdfb51942a8e460e85
AUTHORIZATION_MERGE_SHA=673a06a9a069a357d6acc5263c54e802b3b75539
AUTHORIZATION_BLOB_SHA=86ca56f3f9bb35e9f3a9292628e653a0b0241d61
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=673a06a9a069a357d6acc5263c54e802b3b75539
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY

SOLE_CONSUMER_UNIT=
NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001

IMPLEMENTATION_COMMIT_SHA=9f2973dec905d2ee2d8d00ab7a7e583f6a6742fb
IMPLEMENTATION_HEAD_SHA=c7f924c44e37512c9dec8bef87f303457e36ad35
```

```text
LIVE_NETWORK_CALLS_DURING_IMPLEMENTATION=0
HIGHLEVEL_CALLS_DURING_IMPLEMENTATION=0
CRM_MUTATIONS_DURING_IMPLEMENTATION=0
REAL_SECRET_READS=0
SECRET_PAYLOAD_READS=0
REAL_CREDENTIAL_USE=NO
TOKEN_VALUE_EXPOSURE=NO
CREDENTIAL_ACCESS_DURING_IMPLEMENTATION=SYNTHETIC_ONLY
SECRET_ACCESS_DURING_IMPLEMENTATION=SYNTHETIC_ONLY
NOTE_PATH_MODIFIED=NO
LIVE_NOTE_TRANSPORT_MODIFIED=NO
AT1_EXECUTION_STORE_MODIFIED=NO
PR107_TRUST_BOUNDARY_WEAKENED=NO
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
REQUEST_TIMEOUT_SECONDS=10.0
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
GIT_DIFF_CHECK=PASS
```

## Implementation

### HTTP client

```text
src/integrations/ghl/highlevel_rest/live_note_http_client.py
```

- `ConcreteLiveNoteHttpClient` satisfies `LiveNoteHttpClient.request(...)`.
- Default timeout equals imported frozen `REQUEST_TIMEOUT_SECONDS`.
- Injectable session for tests; dormant stdlib `urllib` session path only.
- One request attempt; no retry loop.
- `allow_redirects=False` required and preserved.
- No third-party HTTP dependency.
- No target authority.
- Tokens and Authorization header values are not logged; call history stores
  header names only.

### Credential provider

```text
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
```

- `LiveNoteCredentialProvider.get_credential()` returns
  `InjectedLiveNoteCredential`.
- Injectable `LiveNoteSecretAccessor` interface.
- `SyntheticLiveNoteSecretAccessor` for deterministic tests.
- No concrete Secret Manager network client.
- No `google-cloud-secretmanager` dependency.
- No gcloud/shell secret access.
- No environment token discovery.
- Token values redacted from provider/credential string forms.

## Exact changed paths

1. `src/integrations/ghl/highlevel_rest/live_note_http_client.py`
2. `src/integrations/ghl/highlevel_rest/live_note_credential_provider.py`
3. `tests/integrations/ghl/highlevel_rest/test_live_note_http_client.py`
4. `tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py`
5. `docs/nw008/nw-008-at8i-ghl-rest-live-note-runtime-assembly-implementation-001.md`
6. `proof/nw008/at-8i/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-consumption-001.md`
7. `proof/nw008/at-8i/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-proof-001.md`

## Blocked paths not modified

```text
src/integrations/ghl/highlevel_rest/live_note_transport.py
src/integrations/ghl/highlevel_rest/note_path.py
src/integrations/ghl/highlevel_rest/fake_transport.py
src/integrations/ghl/highlevel_rest/__init__.py
src/integrations/ghl/__init__.py
src/integrations/ghl/at1_execution_store.py
src/integrations/ghl/at1_live_transport_adapter.py
src/integrations/ghl/at1_live_transport_serializer.py
src/integrations/ghl/bounded_at1_executor.py
src/integrations/ghl/read_adapter.py
src/orchestration/**
src/agents/**
src/mg_guide/**
workspace_addon/**
contracts/**
fixtures/**
.github/**
proof/nw008/at-10/**
requirements.txt
pyproject.toml
Dockerfile
.env.example
scripts/**
local/**
competition/NEW_WORK_LEDGER.md
docs/COMPETITION_BASELINE.md
governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md
```

## Required deterministic tests

```text
TEST_CONCRETE_HTTP_CLIENT_CONFORMS_PROTOCOL=PASS
TEST_HTTP_CLIENT_EXPLICIT_TIMEOUT=PASS
TEST_HTTP_CLIENT_NO_AUTOMATIC_RETRY=PASS
TEST_HTTP_CLIENT_INJECTABLE_SESSION=PASS
TEST_HTTP_CLIENT_ZERO_REAL_NETWORK=PASS

TEST_CREDENTIAL_PROVIDER_INJECTABLE=PASS
TEST_CREDENTIAL_PROVIDER_SYNTHETIC_ONLY=PASS
TEST_ZERO_REAL_SECRET_READS=PASS
TEST_TOKEN_NOT_LOGGED=PASS
TEST_AUTHORIZATION_HEADER_NOT_LOGGED=PASS

TEST_PRIVATE_TARGET_BOUNDARY_UNCHANGED=PASS
TEST_CALLER_TARGET_OVERRIDE_FORBIDDEN=PASS
TEST_AT8H_TRANSPORT_CAPS_UNCHANGED=PASS
TEST_AT8G_RESERVATION_CONTRACT_UNCHANGED=PASS
TEST_AMBIGUITY_NO_RETRY_UNCHANGED=PASS

FULL_TEST_SUITE=PASS
PHASE1_DETERMINISTIC_VALIDATION=PASS
GIT_DIFF_CHECK=PASS
```

## External-effect totals

```text
REAL_SECRET_READS=0
REAL_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
```

## Validation commands and results

```text
PYTHONPATH=src:. .venv/bin/pytest tests/integrations/ghl/highlevel_rest/test_live_note_http_client.py tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py -q
-> PASS

PYTHONPATH=src:. .venv/bin/pytest tests/integrations/ghl/highlevel_rest/ -q
-> PASS

PYTHONPATH=src:. .venv/bin/pytest -o addopts='' -q -p no:warnings --tb=no
-> 631 passed

PYTHONPATH=src:. .venv/bin/python scripts/verify_phase1_deterministic.py
-> YAML parse: PASS
-> Packet schema validation: PASS
-> Three fixture outcomes: PASS
-> Replay / idempotency: PASS
-> Mutation intent bounds: PASS
-> Proof-return schema validation: PASS

GIT_DIFF_CHECK=PASS
AUTHORIZED_PATHS_ONLY=YES
```

## AT10 side-effect handling

```text
proof/nw008/at-10/acceptance-demo/** is BLOCKED for this lane.
OBSERVATION=full pytest rewrote tracked AT10 acceptance-demo evidence files
ACTION=restored from origin/main lane base via git checkout
CONFIRMATION=AT10 paths absent from final git status / diff
STAGED=NO
AT10_REPAIR_IN_THIS_LANE=NO
```

## Non-authority reminder

```text
LIVE_TRANSPORT_EXECUTION=NO
LIVE_NOTE_WRITE=NO
LIVE_NOTE_READ=NO
LIVE_CRM_MUTATION=NO
REAL_CREDENTIAL_USE=NO
SECRET_MANAGER_LIVE_INVOCATION=NO
LIVE_MUTATION_GRANT_CREATED=NO
```
