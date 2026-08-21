# NW-008 AT-8I — GHL REST Live Note Runtime Assembly Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

PLANNING_IDENTIFIER=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md

PREDECESSOR_PR=113
PR113_STATE=MERGED
PR113_REVIEWED_HEAD=e42fa13f36e49e075d35dbab1453149b8e81650f
PR113_MERGE_SHA=71f85fc32ed990d2a06fe94cff0c9fae5b988cc7
PR113_MERGE_VERIFIED_ON_ORIGIN_MAIN=YES

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE

GRANT=OFFLINE_RUNTIME_ASSEMBLY_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN

AUTHORIZED_CONSUMER_UNIT=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_PATH=proof/nw008/at-8i/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-consumption-001.md
```

This artifact grants implementation authority only for deterministic offline runtime assembly work. It does not authorize live transport execution, live note write/read, live CRM mutation, real secret reads, real credential use, IAM changes, deployment changes, or production configuration mutation.

Creating, reviewing, or merging this authorization does not implement the HTTP client, implement the credential provider, load credentials, access HighLevel, or grant live CRM mutation.

The sole authorized consumer is `NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001`. No other unit may consume this grant.

The implementation consumer must record one-shot consumption in `proof/nw008/at-8i/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-consumption-001.md`. It must not modify this authorization artifact.

## 2. Frozen implementation mode (normative)

```text
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY

REAL_SECRET_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_PAYLOAD_READS_DURING_IMPLEMENTATION=0

REAL_CREDENTIAL_USE=NO
TOKEN_VALUE_EXPOSURE=NO

LIVE_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0

IAM_CHANGE=NO
SECRET_POLICY_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_CHANGE=NO

LIVE_TRANSPORT_EXECUTION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_NOTE_READ_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO

SECRET_MANAGER_PROVIDER_CODE_IMPLEMENTATION_AUTHORIZED=YES
SECRET_MANAGER_ACCESSOR_INTERFACE_IMPLEMENTATION_AUTHORIZED=YES
CONCRETE_SECRET_MANAGER_NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
SECRET_MANAGER_PROVIDER_LIVE_INVOCATION_AUTHORIZED=NO
GCLOUD_SUBPROCESS_SECRET_ACCESS_IMPLEMENTATION_AUTHORIZED=NO
SHELL_SECRET_ACCESS_IMPLEMENTATION_AUTHORIZED=NO

HTTP_CLIENT_TIMEOUT_REQUIRED=YES
HTTP_CLIENT_TIMEOUT_MUST_BE_EXPLICIT=YES
HTTP_CLIENT_TIMEOUT_DEFAULT_MUST_MATCH_AT8H_FROZEN_TIMEOUT=YES

DEPENDENCY_CHANGES_AUTHORIZED=NO
PACKAGE_MANIFEST_CHANGES_AUTHORIZED=NO
```

## 3. Known reinspection inputs (locked)

```text
CONCRETE_LIVE_HTTP_CLIENT_IDENTIFIED=NO
HTTP_CLIENT_CONSTRUCTION_PATH_IDENTIFIED=NO

PRIVATE_TARGET_BINDING_RUNTIME_PATH_IDENTIFIED=YES
CALLER_TARGET_OVERRIDE_IMPOSSIBLE=YES

GHL_SECRET_RESOURCE_IDENTIFIED=YES
GHL_SECRET_METADATA_ACCESS_VERIFIED=YES
GHL_SECRET_PAYLOAD_ACCESS_CAPABILITY_VERIFIED=YES
REAL_TOKEN_VALUE_EXPOSED=NO

SUB_ACCOUNT_TOKEN_CLASS_VERIFIABLE=YES
CONTACTS_WRITE_SCOPE_VERIFIABLE=YES
CONTACTS_READONLY_SCOPE_VERIFIABLE=YES

CREDENTIAL_INJECTION_PATH_IDENTIFIED=NO
CREDENTIAL_LOGGING_PROHIBITION_VERIFIED=YES

SYNTHETIC_PRIVATE_TARGET_AVAILABLE=YES
GHL_SPACE_OWNER_COUNTERSIGNATURE_AVAILABLE=YES

LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## 4. Authoring vs consumer writable scope (normative)

These scopes are disjoint. Authorization authoring must not write consumer implementation files. The implementation consumer must not rewrite this authorization artifact. Consumption is recorded only in the consumption record path; it is not recorded by mutating this grant.

```text
AUTHORIZATION_PR_WRITABLE_SCOPE=
governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md

AUTHORIZED_CONSUMER_UNIT=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001
```

Existing HighLevel REST module convention inspected before freezing paths:

```text
EXISTING_PACKAGE=src/integrations/ghl/highlevel_rest/
EXISTING_PROTOCOL_MODULE=src/integrations/ghl/highlevel_rest/live_note_transport.py
EXISTING_PROTOCOL=LiveNoteHttpClient
EXISTING_CREDENTIAL_CONTRACT=InjectedLiveNoteCredential
EXISTING_TEST_DIR=tests/integrations/ghl/highlevel_rest/
EXISTING_DOC_PREFIX=docs/nw008/nw-008-at8*
EXISTING_PROOF_DIR_PATTERN=proof/nw008/at-8*/
```

No concrete `LiveNoteHttpClient` adapter module or credential-provider module exists yet. Proposed consumer filenames follow the existing `live_note_*` snake_case module and `test_<module>` pairing used by `live_note_transport.py` / `test_live_note_transport.py`. They are not invented outside that package.

### 4.1 Authorization PR writable scope

```text
governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md
```

No other path is writable in this authorization PR.

### 4.2 Authorized consumer writable scope

Exact future consumer writable paths, reserved for `NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001` after this artifact is merged and independently verified:

```text
src/integrations/ghl/highlevel_rest/live_note_http_client.py
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
tests/integrations/ghl/highlevel_rest/test_live_note_http_client.py
tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py
proof/nw008/at-8i/**
docs/nw008/nw-008-at8i-*
```

Conditional additional test files under the same test directory are permitted only when required to keep the two assembly proofs separated:

```text
tests/integrations/ghl/highlevel_rest/test_live_note_http_client_*.py
tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider_*.py
```

These writable path classes map to:

1. concrete `LiveNoteHttpClient` adapter
2. credential provider/injection adapter
3. directly corresponding deterministic tests
4. `proof/nw008/at-8i/**`
5. AT8I implementation documentation if required (`docs/nw008/nw-008-at8i-*`)

The consumer must implement the existing protocol/value contracts in `live_note_transport.py` without modifying that frozen module:

```text
CONCRETE_HTTP_CLIENT_MUST_SATISFY=LiveNoteHttpClient.request(...)
CREDENTIAL_PROVIDER_MUST_RETURN=InjectedLiveNoteCredential
EXISTING_TRANSPORT_MODULE=FROZEN
```

### 4.3 Authorized consumer blocked paths

```text
src/integrations/ghl/highlevel_rest/live_note_transport.py=BLOCKED
src/integrations/ghl/highlevel_rest/note_path.py=BLOCKED
src/integrations/ghl/highlevel_rest/fake_transport.py=BLOCKED
src/integrations/ghl/highlevel_rest/__init__.py=BLOCKED
src/integrations/ghl/__init__.py=BLOCKED
src/integrations/ghl/at1_execution_store.py=BLOCKED
src/integrations/ghl/at1_live_transport_adapter.py=BLOCKED
src/integrations/ghl/at1_live_transport_serializer.py=BLOCKED
src/integrations/ghl/bounded_at1_executor.py=BLOCKED
src/integrations/ghl/read_adapter.py=BLOCKED
src/orchestration/**=BLOCKED
src/agents/**=BLOCKED
src/mg_guide/**=BLOCKED
workspace_addon/**=BLOCKED
contracts/**=BLOCKED
fixtures/**=BLOCKED
.github/**=BLOCKED
proof/nw008/at-10/**=BLOCKED
requirements.txt=BLOCKED
pyproject.toml=BLOCKED
Dockerfile=BLOCKED
.env.example=BLOCKED
scripts/**=BLOCKED
local/**=BLOCKED
competition/NEW_WORK_LEDGER.md=BLOCKED
docs/COMPETITION_BASELINE.md=BLOCKED
```

Also blocked: IAM/policy surfaces, deployment surfaces, production configuration, and unrelated GHL adapters.

```text
DEPENDENCY_CHANGES_AUTHORIZED=NO
PACKAGE_MANIFEST_CHANGES_AUTHORIZED=NO
NEW_HTTP_LIBRARY_DEPENDENCY_AUTHORIZED=NO
NEW_SECRET_MANAGER_LIBRARY_DEPENDENCY_AUTHORIZED=NO
```

Repository evidence: `requirements.txt` / `pyproject.toml` do not include `requests`, `httpx`, `aiohttp`, or `google-cloud-secretmanager`. Stdlib HTTP (`urllib`) is already used elsewhere in-repo. A new dependency is not unavoidable. The consumer must use an injected session/client for tests and, if a dormant concrete HTTP adapter is required, standard-library HTTP only. Secret Manager access must be an injectable accessor seam, not a new package import.

## 4A. Authorized offline implementation scope

Exactly two missing assembly components are in scope for the future consumer:

1. concrete live-note HTTP client
2. private credential acquisition/injection adapter

No additional runtime capability, live execution path, or alternate authority path is authorized.

## 5. Design requirements (normative)

### 5.1 HTTP client

```text
HTTP_CLIENT_TIMEOUT_REQUIRED=YES
HTTP_CLIENT_TIMEOUT_MUST_BE_EXPLICIT=YES
HTTP_CLIENT_TIMEOUT_DEFAULT_MUST_MATCH_AT8H_FROZEN_TIMEOUT=YES
```

The HTTP client timeout must be explicit. The default must match the AT8H frozen timeout (`REQUEST_TIMEOUT_SECONDS` in `live_note_transport.py`). Do not modify `live_note_transport.py` to satisfy this requirement.

- Implement the existing `LiveNoteHttpClient` protocol contract with a concrete adapter in `live_note_http_client.py`.
- Support injected session/client for deterministic tests.
- Use explicit timeout configuration (`REQUEST_TIMEOUT_SECONDS` already frozen in transport).
- Do not implement hidden retries.
- Do not introduce generic REST fallback or alternate routes.
- Do not introduce contact-target authority.
- Never log auth header or token.
- Normalize provider response through the existing transport pipeline; do not bypass `BoundedLiveNoteTransport`.
- Do not import `requests`, `httpx`, `aiohttp`, or add HTTP libraries. Prefer injected session plus stdlib HTTP if a dormant concrete adapter is required.

### 5.2 Credential provider / Secret Manager seam

```text
SECRET_MANAGER_PROVIDER_CODE_IMPLEMENTATION_AUTHORIZED=YES
SECRET_MANAGER_ACCESSOR_INTERFACE_IMPLEMENTATION_AUTHORIZED=YES
CONCRETE_SECRET_MANAGER_NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
SECRET_MANAGER_PROVIDER_LIVE_INVOCATION_AUTHORIZED=NO
GCLOUD_SUBPROCESS_SECRET_ACCESS_IMPLEMENTATION_AUTHORIZED=NO
SHELL_SECRET_ACCESS_IMPLEMENTATION_AUTHORIZED=NO
REAL_SECRET_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_PAYLOAD_READS_DURING_IMPLEMENTATION=0
REAL_CREDENTIAL_USE=NO
TOKEN_VALUE_EXPOSURE=NO
GCLOUD_SECRET_PAYLOAD_ACCESS_IN_AT8I_PROOF=NO
```

- Return `InjectedLiveNoteCredential` (or strictly equivalent existing contract).
- Keep credential acquisition separate from transport behavior.
- The future consumer may implement the injectable provider seam, including a Secret Manager accessor interface.
- Concrete Secret Manager network-client implementation is not authorized.
- `gcloud` subprocess secret access and shell secret access are not authorized.
- Deterministic implementation validation must use an injected fake accessor and a synthetic token.
- Real Secret Manager call must be injectable and absent in tests.
- No `gcloud` secret payload access is part of AT8I implementation proof.
- Do not print, log, serialize, or persist token values.
- Do not expose secret payload in proof artifacts.
- Secret Manager resource identity may be configuration; the real value must never be embedded in the repository.
- Do not add `google-cloud-secretmanager` or any other new package.

## 6. Required invariants to preserve unchanged

```text
PR107_PRIVATE_AT8_CAPABILITY_BOUNDARY=UNCHANGED_REQUIRED
AT8G_DURABLE_RESERVATION_SEMANTICS=UNCHANGED_REQUIRED
AT8H_POST_GET_CAPS=UNCHANGED_REQUIRED
AMBIGUITY_TRUTH=UNKNOWN_REQUIRED
AMBIGUOUS_POST_RETRY=FORBIDDEN_REQUIRED
CALLER_TARGET_OVERRIDE=FORBIDDEN_REQUIRED
```

## 7. Deterministic proof obligations (all required)

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

All proofs must be produced without live HighLevel transport execution, secret payload reads, real credential usage, or CRM mutations.

## 8. Explicit non-authorizations

```text
HIGHLEVEL_CALL_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_NOTE_READ_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REAL_SECRET_VALUE_READ_AUTHORIZED=NO
REAL_TOKEN_RUNTIME_USE_AUTHORIZED=NO
LIVE_MUTATION_GRANT_CREATION_AUTHORIZED=NO
```

## 9. Competition delta handling boundary

This authorization lane does not authorize creating or modifying competition delta governance artifacts. Competition delta checks are informational unless separately approved as writable scope.

```text
competition/NEW_WORK_LEDGER.md=BLOCKED
docs/COMPETITION_BASELINE.md=BLOCKED
```

## 10. Non-transitivity

```text
PR113_COMPLETION_AUTHORITY_GRANTS_AT8I=NO
AT8H_AUTHORIZATION_GRANTS_AT8I=NO
AT8I_AUTHORIZATION_GRANTS_LIVE_MUTATION=NO
AT8I_AUTHORIZATION_GRANTS_LIVE_TRANSPORT_EXECUTION=NO
AT8I_AUTHORIZATION_GRANTS_REAL_CREDENTIAL_USE=NO
AT8I_AUTHORIZATION_GRANTS_SECRET_PAYLOAD_READ=NO
AT8I_AUTHORIZATION_GRANTS_PRODUCTION_CHANGE=NO
```

PR113 closed AT8H completion. That closure removes a predecessor blocker; it does not grant AT8I implementation. This authorization, even after merge, does not grant live mutation, live transport execution, real credential use, Secret Manager live invocation, or production configuration changes.
