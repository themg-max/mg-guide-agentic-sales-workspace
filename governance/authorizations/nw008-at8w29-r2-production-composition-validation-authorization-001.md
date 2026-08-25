# NW-008 AT8W29 R2 Production-Composition Validation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W29_R2_PRODUCTION_COMPOSITION_VALIDATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w29-r2-production-composition-validation-authorization-001.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w29-r2-production-composition-validation-authorization-001

BASE_REF=origin/main
BASE_SHA=
  f5ec221a667db91e43684f3acad98913b6e00bfa

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=HUMAN_MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
```

This artifact is planning-only. Creating, reviewing, or merging it does not
impersonate a service account, mint a token, read a Secret Manager payload,
open or create SQLite, construct At1ExecutionStore, assemble production runtime,
instantiate HighLevel HTTP client or transport, call HighLevel, mutate CRM or
IAM, or deploy.

The bounded grant becomes usable only after human review and merge places this
exact artifact on `main`, followed by independent verification by the sole
authorized execution consumer.

```text
EXECUTION_PERFORMED_IN_THIS_UNIT=NO
SERVICE_ACCOUNT_IMPERSONATION_IN_THIS_UNIT=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_IN_THIS_UNIT=0
SECRET_MANAGER_ACCESS_PERFORMED_IN_THIS_UNIT=NO
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
C4_SECRET_READ_ATTEMPTS_IN_THIS_UNIT=0
B2_SECRET_READ_ATTEMPTS_IN_THIS_UNIT=0
HIGHLEVEL_CALLS_IN_THIS_UNIT=0
HTTP_REQUEST_DISPATCHES_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
SQLITE_CREATION_IN_THIS_UNIT=0
SQLITE_OPEN_IN_THIS_UNIT=0
AT1_EXECUTION_STORE_CONSTRUCTIONS_IN_THIS_UNIT=0
PRODUCTION_RUNTIME_ASSEMBLY_IN_THIS_UNIT=0
IAM_MUTATIONS_IN_THIS_UNIT=0
DEPLOYMENTS_IN_THIS_UNIT=0
PRODUCTION_RUNTIME_STARTS_IN_THIS_UNIT=0
AUTHORIZATION_CONSUMED_IN_THIS_UNIT=NO
```

## 2. Purpose and explicit non-authority

This artifact conditionally authorizes one later bounded production-composition
validation of the actual production root. The future execution consumer may
establish only whether:

1. a fresh short-lived runtime-SA identity can be acquired once and injected as
   process Application Default Credentials for both production Secret Manager
   clients;
2. a process-local synthetic/competition-safe issued verified capability can be
   precreated and accepted by `_validate_issued_capability()` /
   `_require_issued_verified_capability()`;
3. `assemble_bound_live_note_runtime(verified_capability=...)` can run exactly
   once and return a `NotePathAdapter` after:
   - verified capability validation;
   - DB path resolution from `MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH`;
   - exact C4 resolution;
   - existing At1ExecutionStore construction at the designated path;
   - exact B2 credential resolution into `InjectedLiveNoteCredential`;
   - one `ConcreteLiveNoteHttpClient` construction;
   - one `BoundedLiveNoteTransport` construction;
   - one `NotePathAdapter` construction;
   - return without invoking any adapter business method;
4. composition succeeds with zero HTTP request dispatch and zero CRM/business
   effects; and
5. the single store connection is deterministically closed afterward without
   business/protocol writes.

```text
PURPOSE=
  ONE_BOUNDED_PRODUCTION_COMPOSITION_VALIDATION_OF_ASSEMBLE_BOUND_LIVE_NOTE_RUNTIME

PRODUCTION_RUNTIME_ASSEMBLY_AUTHORIZED=YES_ONCE_ONLY
PRODUCTION_RUNTIME_START_AUTHORIZED=NO
HIGHLEVEL_DISPATCH_AUTHORIZED=NO
HIGHLEVEL_HTTP_REQUEST_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
BUSINESS_EXECUTION_AUTHORIZED=NO
NOTE_WRITE_AUTHORIZED=NO
STAGE_TRANSITION_AUTHORIZED=NO
EXECUTION_CLAIM_AUTHORIZED=NO
ATTEMPT_RECORD_AUTHORIZED=NO
PROTOCOL_LEDGER_WRITE_AUTHORIZED=NO
BUSINESS_LEDGER_WRITE_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATE_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
STANDING_TOKEN_AUTHORITY=NO
DB_CREATE_AUTHORIZED=NO
DB_DELETE_AUTHORIZED=NO
DB_RECREATE_AUTHORIZED=NO
DB_REPAIR_AUTHORIZED=NO
R3_AUTHORIZED=NO
R4_AUTHORIZED=NO
```

A successful R2 production-composition validation proves only that the
production root can assemble once under the bound runtime principal, exact C4
and B2 numeric secret versions, the existing designated store, one HTTP client,
and one bounded transport, while remaining network-dormant and business-dormant.
It does not authorize HighLevel dispatch, CRM mutation, note write, stage
transition, business execution, execution claims, attempts, ledger writes,
production runtime start, IAM mutation, key creation, deployment, DB
create/recreate/repair/delete, or any later gate (R3/R4).

This grant does **not** revive, transfer, reuse, or extend the consumed AT8W28
R1B revalidation authorization (PR #206) or any earlier consumed grant.

## 3. Durable source prerequisites and R1B completion

```text
R1B_PROOF_PR=207
R1B_PROOF_PR_STATE=MERGED
R1B_PROOF_HEAD=
  ae9d18a61955aa70f5557bda5f87cb94b9034d14
R1B_PROOF_MERGE_COMMIT=
  f5ec221a667db91e43684f3acad98913b6e00bfa
R1B_PROOF_MERGE_ON_ORIGIN_MAIN=YES
R1B_PROOF=
  proof/nw008/at-8w28/nw008-at8w28-r1b-existing-store-revalidation-execution-proof-001.md
R1B_PROOF_ON_ORIGIN_MAIN=YES
R1B_RESULT=PASS
R1B_GATE_COMPLETE=YES

R1B_AUTHORIZATION=
  governance/authorizations/nw008-at8w28-r1b-existing-store-revalidation-authorization-001.md
R1B_AUTHORIZATION_PR=206
R1B_AUTHORIZATION_MERGE=
  68dd94a0a7c2c6745681be36c6ce3c7dc9796ba3
R1B_AUTHORIZATION_STATE=CONSUMED
R1B_AUTHORIZATION_REUSABLE=NO
R1B_AUTHORIZATION_TRANSFERABLE=NO

SOURCE_R1A_PROOF_PR=203
SOURCE_R1A_RESULT=PASS
SOURCE_R1A_GATE_COMPLETE=YES

SOURCE_IMPLEMENTATION_PR=200
SOURCE_IMPLEMENTATION_MERGE=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
SOURCE_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w25/nw008-at8w25-b2-c4-c3-c2-offline-implementation-proof-001.md
SOURCE_IMPLEMENTATION_PROOF_ON_ORIGIN_MAIN=YES

PRODUCTION_RUNTIME_ENTRYPOINT=
  assemble_bound_live_note_runtime
PRODUCTION_RUNTIME_ENTRYPOINT_MODULE=
  src/integrations/ghl/highlevel_rest/live_note_runtime.py
PRODUCTION_RUNTIME_ENTRYPOINT_RESOLVED=YES

C4_IMPLEMENTATION_DURABLE=YES
B2_IMPLEMENTATION_DURABLE=YES
AT1_EXECUTION_STORE_IMPLEMENTATION_DURABLE=YES
LIVE_NOTE_HTTP_CLIENT_IMPLEMENTATION_DURABLE=YES
BOUNDED_TRANSPORT_IMPLEMENTATION_DURABLE=YES
NOTE_PATH_ADAPTER_IMPLEMENTATION_DURABLE=YES
GOOGLE_CLOUD_SECRET_MANAGER_VERSION=2.27.0
SOURCE_CODE_CHANGE_REQUIRED=NO
```

PR #207 records governed R1B existing-store revalidation `RESULT=PASS` and
`R1B_GATE_COMPLETE=YES` under consumed PR #206. The designated store file is
therefore expected to be present. This AT8W29 authorization is a fresh one-shot
production-composition grant only. It does not reopen, reuse, or extend the
consumed AT8W28 R1B grant.

## 4. Source-only production-composition preflight (authoring)

Source inspection on `origin/main` at
`f5ec221a667db91e43684f3acad98913b6e00bfa` resolved the production root without
source changes.

### 4.1 Assembly sequence evidence

`assemble_bound_live_note_runtime(*, verified_capability)` performs, in order:

```text
1. _validate_issued_capability(verified_capability)
     -> note_path._require_issued_verified_capability(...)
2. _resolve_root_owned_runtime_dependencies():
     a. db_path = os.environ["MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH"]
     b. GoogleSecretManagerLiveNoteSecretAccessor()
     c. RootOwnedLiveNoteCredentialInjection(
          accessor=...,
          resource_name=
            projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1
        )
     d. GoogleSecretManagerCommitmentKeyProvider().resolve()  # exact C4
     e. At1ExecutionStore(db_path=db_path, commitment_material=...)
3. dependencies.credential_injection.build_provider().get_credential()
     -> InjectedLiveNoteCredential  # exact B2 read occurs here
4. ConcreteLiveNoteHttpClient()
5. BoundedLiveNoteTransport(
     bound_contact_id=...,
     credential=...,
     http_client=...
   )
6. NotePathAdapter(...; execution_store=...)
7. adapter._verified_contact_binding_capability = validated_capability
8. return adapter
```

```text
ASSEMBLY_HTTP_DISPATCH_BY_ITSELF=NO
ASSEMBLY_CRM_MUTATION_BY_ITSELF=NO
ASSEMBLY_BUSINESS_METHOD_INVOCATION_BY_ITSELF=NO
RETURNED_OBJECT_TYPE=NotePathAdapter
```

HTTP dispatch exists only on later `BoundedLiveNoteTransport.dispatch(...)` /
`ConcreteLiveNoteHttpClient.request(...)` paths. Assembly constructs those
objects and returns without calling adapter business methods or transport
dispatch.

### 4.2 Identity propagation preflight

```text
TARGET_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

IDENTITY_MECHANISM=
  LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION

PRODUCTION_ADC_IDENTITY_INJECTION_PATH_RESOLVED=YES
C4_SECRET_MANAGER_CLIENT_USES_TARGET_RUNTIME_SA=YES
B2_SECRET_MANAGER_CLIENT_USES_TARGET_RUNTIME_SA=YES
DIRECT_USER_ADC_SECRET_ACCESS=NO
SERVICE_ACCOUNT_KEY_REQUIRED=NO
SOURCE_CODE_CHANGE_REQUIRED=NO
```

Exact production client construction paths:

```text
C4_CLIENT_FACTORY=
  at1_commitment_key_provider._new_secret_manager_client()
  -> google.cloud.secretmanager.SecretManagerServiceClient()
  # no credentials= argument; process ADC only

B2_CLIENT_FACTORY=
  live_note_credential_provider._new_secret_manager_client()
  -> google.cloud.secretmanager.SecretManagerServiceClient()
  # no credentials= argument; process ADC only
```

Resolved process-level injection path (execution consumer, after merge):

1. authenticate as the operator local user ADC source principal class only;
2. perform exactly one short-lived impersonation of the exact target runtime SA;
3. mint exactly one short-lived access token for that target SA;
4. install that impersonated credential as process Application Default
   Credentials **before** calling `assemble_bound_live_note_runtime`;
5. allow both production Secret Manager clients constructed during assembly to
   inherit the same process ADC and therefore authenticate only as the target
   runtime SA;
6. forbid direct user-ADC Secret Manager access, caller-supplied runtime
   identity override, user-managed service-account keys, and any principal
   other than the exact target runtime SA.

Because both clients omit explicit credentials and resolve default ADC, one
process-level impersonated ADC injection serves C4 and B2 without source change.

### 4.3 Verified capability preflight

```text
R2_VERIFIED_CAPABILITY_SOURCE_RESOLVED=YES
R2_VERIFIED_CAPABILITY_SYNTHETIC_OR_COMPETITION_SAFE=YES
R2_VERIFIED_CAPABILITY_PRECREATABLE_BEFORE_LIVE_EXECUTION=YES
R2_VERIFIED_CAPABILITY_PRIVATE_PRODUCTION_CUSTOMER_RECORD=NO
```

Accepted capability mechanism:

```text
VALIDATOR=
  live_note_runtime._validate_issued_capability
  -> note_path._require_issued_verified_capability

PERMITTED_ISSUANCE_SURFACE_FOR_R2=
  NotePathAdapter._build_at8_shaped_test_capability
  / note_path._issue_synthetic_test_capability

PERMITTED_CAPABILITY_SHAPE=
  process-local issued _VerifiedContactBindingCapability
  with location_id and contact_id both prefixed synthetic-
  and competition-safe consumer identity fields
```

The capability must be issued in the same process that performs assembly.
Caller-forged objects, private production/customer contact records, live bound-
contact GET verification, and non-synthetic location/contact identifiers are
forbidden for this R2 unit.

```text
R2_AUTHORIZATION_DESIGNABLE=YES
STOP_CODE=NONE
```

## 5. Identity binding

```text
TARGET_RUNTIME_PRINCIPAL=
  serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

TARGET_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SOURCE_PRINCIPAL_CLASS=
  HUMAN_OPERATOR_USER_ADC

SOURCE_PRINCIPAL_PRIVATE_ATTESTATION_REF=
  NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af

DO_NOT_PUBLISH_SOURCE_PRINCIPAL=YES
SOURCE_PRINCIPAL_PUBLICATION_ALLOWED=NO
SOURCE_PRINCIPAL_PERSISTENCE_ALLOWED=NO

IDENTITY_MECHANISM=
  LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION

CALLER_SUPPLIED_RUNTIME_IDENTITY_OVERRIDE=FORBIDDEN
USER_MANAGED_SERVICE_ACCOUNT_KEY=FORBIDDEN
DIRECT_USER_ADC_AS_SECRET_ACCESS_PRINCIPAL=FORBIDDEN
```

The execution consumer must authenticate Secret Manager only as the exact
target runtime service account, obtained solely through short-lived
impersonation from the operator's local user ADC and injected as process ADC
for both C4 and B2 clients. The consumer must not:

- publish or persist the operator principal identity;
- use a user-managed service-account key;
- use direct user ADC as the Secret Manager access principal;
- accept a caller-supplied runtime identity override; or
- impersonate any principal other than the exact target runtime SA above.

Proof may reference only the opaque attestation ref
`NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af` for the source principal
class, not the human operator email or other identifying material.

## 6. Identity effect budget

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1

IAM_MUTATIONS_MAX=0
IAM_POLICY_WRITES_MAX=0
SERVICE_ACCOUNT_KEY_CREATE_MAX=0

SECOND_TOKEN_MINT_OR_REFRESH=FORBIDDEN
RETRY=FORBIDDEN

TOKEN_LOGGING_ALLOWED=NO
TOKEN_PERSISTENCE_ALLOWED=NO
TOKEN_HASHING_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
TOKEN_STDOUT_STDERR_ALLOWED=NO

TOKEN_USE_SCOPE=
  R2_PRODUCTION_COMPOSITION_EXACT_C4_AND_B2_READS_ONLY

TOKEN_REUSE_AFTER_R2_COMPOSITION=FORBIDDEN
TOKEN_LIFETIME=SHORT_LIVED_MINIMUM_NECESSARY
```

Exactly one impersonation attempt and exactly one short-lived access-token mint
are permitted for the exact target runtime SA. That single process ADC
injection must cover both exact C4 and exact B2 Secret Manager reads performed
during the one authorized assembly. After R2 composition validation ends
(success or fail-closed stop), the token must not be reused, refreshed, logged,
persisted, hashed for proof, or captured in fragments.

## 7. Exact secret resources and secret effect budget

Exactly two Secret Manager resources are permitted:

```text
EXACT_C4_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

EXACT_B2_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1

PERMITTED_SECRET_RESOURCE_COUNT=2
OTHER_SECRET_RESOURCES_PERMITTED=NO
```

```text
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=1
OTHER_SECRET_READ_ATTEMPTS_MAX=0
TOTAL_SECRET_READ_ATTEMPTS_MAX=2

C4_RETRIES_MAX=0
B2_RETRIES_MAX=0

SECRET_LIST_CALLS_MAX=0
SECRET_VERSION_LIST_CALLS_MAX=0
SECRET_METADATA_DISCOVERY_CALLS_MAX=0

LATEST_ALLOWED=NO
ALIAS_RESOLUTION_ALLOWED=NO
VERSION_DISCOVERY_ALLOWED=NO
SECRET_DISCOVERY_ALLOWED=NO
CALLER_RESOURCE_OVERRIDE_ALLOWED=NO
RETRY_ALLOWED=NO
```

The exact C4 and B2 resource strings above are normative. The consumer may not
substitute project number/id forms, change secret names, change numeric
versions, use `latest`, resolve aliases, list secrets/versions, discover
alternatives, accept caller overrides, read any other secret, or retry either
read.

```text
C4_PAYLOAD_PROCESS_MEMORY_ONLY=YES
B2_PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_PERSISTED_ALLOWED=NO
PAYLOAD_PUBLISHED_ALLOWED=NO
PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
```

C4 and B2 payloads may exist only in process memory for the minimum lifetime
required to complete one production assembly and the required post-assembly
store connection close. They must not be written into the SQLite file as raw
key/token material beyond whatever the existing constructor already persists as
the non-secret `commitment_key_version_resource` metadata string.

## 8. Exact designated store and environment targets

```text
EXACT_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

DESIGNATED_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

DESIGNATED_PRIMARY_SQLITE_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

DESIGNATED_DB_PARENT=
  /Users/achandler/Library/Application Support/mg-guide/nw008

ROOT_OWNED_DB_ENV_KEY=
  MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH

ROOT_OWNED_DB_ENV_VALUE_REQUIRED=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

OTHER_DB_PATHS_ALLOWED=NO
OTHER_PRIMARY_DB_PATHS_ALLOWED=NO
SECOND_DURABLE_DATABASE_ALLOWED=NO
ALTERNATE_DATABASE_PATH_ALLOWED=NO
ALTERNATE_DB_PATH_ALLOWED=NO
CALLER_DB_PATH_OVERRIDE_ALLOWED=NO

EXPECTED_DESIGNATED_DB_STATE=PRESENT
EXPECTED_PRE_EXECUTION_DB_STATE=PRESENT

EXPECTED_SCHEMA_VERSION=1

EXPECTED_COMMITMENT_KEY_VERSION_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
```

Only the exact designated primary path may be opened as the durable
At1ExecutionStore database, and only via the production root env key above. No
alternate path, temporary validation DB, copied DB, backup DB, test path, or
caller override is permitted under this grant.

### 8.1 Primary DB versus SQLite-engine transient sidecars

```text
SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECAR_SCOPE=
  SAME_DIRECTORY_AS_DESIGNATED_PRIMARY_DB_ONLY

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECAR_PURPOSE=
  SQLITE_INTERNAL_TRANSACTION_DURABILITY_ONLY

SQLITE_ENGINE_AUTOMATIC_SIDECAR_CREATE_REMOVE=
  PERMITTED_AS_INCIDENTAL_EFFECT_OF_AUTHORIZED_CONSTRUCTOR_ONLY

OPERATOR_CREATED_SIDECARS_ALLOWED=NO
OPERATOR_MANAGED_SIDECAR_DELETE_ALLOWED=NO
```

SQLite may automatically create and remove engine-managed transient transaction
sidecars in the same directory as the designated primary DB only, solely as an
incidental effect of the already authorized At1ExecutionStore constructor/open
lifecycle.

## 9. Pre-execution fail-closed checks

Before impersonation or any Secret Manager call, the execution consumer must
perform the following checks only, in order, and must not mutate filesystem
state.

### 9.1 Parent directory pre-consumption check

```text
PRE_EXECUTION_PARENT_CHECK=
  EXACT_PARENT_EXISTENCE_AND_DIRECTORY_TYPE_ONLY

REQUIRE_BEFORE_IMPERSONATION=
  PARENT_DIRECTORY_EXISTS=YES
  PARENT_PATH_IS_DIRECTORY=YES

IF_PARENT_MISSING_OR_NOT_DIRECTORY=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=DESIGNATED_SQLITE_PARENT_NOT_READY
  STOP=YES
```

### 9.2 Designated primary DB pre-existence check (must be PRESENT)

```text
PRE_EXECUTION_DB_CHECK=
  EXACT_DESIGNATED_PRIMARY_PATH_EXISTENCE_ONLY

REQUIRE_BEFORE_IMPERSONATION=
  DESIGNATED_DB_FILE_EXISTS=YES

IF_DESIGNATED_DB_FILE_ABSENT=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=DESIGNATED_SQLITE_MISSING_FOR_R2_COMPOSITION
  STOP=YES
```

Existence/type-only checking of the exact parent and designated primary path is
permitted. Opening SQLite, creating paths, or any other filesystem mutation is
forbidden by the pre-checks.

### 9.3 Capability precreation check

```text
REQUIRE_BEFORE_IMPERSONATION=
  R2_SYNTHETIC_VERIFIED_CAPABILITY_PRECREATED_IN_PROCESS=YES
  R2_VERIFIED_CAPABILITY_LOCATION_ID_SYNTHETIC_PREFIX=YES
  R2_VERIFIED_CAPABILITY_CONTACT_ID_SYNTHETIC_PREFIX=YES

IF_CAPABILITY_NOT_PRECREATABLE_OR_NOT_SYNTHETIC=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=R2_VERIFIED_CAPABILITY_UNRESOLVED
  STOP=YES
```

## 10. Composition and store effect budget

```text
DESIGNATED_SQLITE_CREATE_MAX=0
DB_CREATE_ALLOWED=NO
DB_DELETE_ALLOWED=NO
DB_RECREATE_ALLOWED=NO
DB_REPAIR_ALLOWED=NO
DB_RENAME_ALLOWED=NO
DB_TRUNCATE_ALLOWED=NO
ALTERNATE_DB_PATH_ALLOWED=NO

AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=1
AT1_EXECUTION_STORE_INITIAL_CREATION_MAX=0
AT1_EXECUTION_STORE_REOPEN_MAX=0
AT1_EXECUTION_STORE_EXISTING_OPEN_MAX=1

PRODUCTION_RUNTIME_ASSEMBLY_MAX=1
PRODUCTION_RUNTIME_STARTS_MAX=0

HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS_MAX=1
HIGHLEVEL_TRANSPORT_INSTANTIATIONS_MAX=1
NOTE_PATH_ADAPTER_ASSEMBLIES_MAX=1

ASSEMBLE_BOUND_LIVE_NOTE_RUNTIME_CALLS_MAX=1
SECOND_ASSEMBLY_ALLOWED=NO
```

Exactly one production assembly is permitted via:

```text
assemble_bound_live_note_runtime(verified_capability=<precreated synthetic capability>)
```

That assembly must open the already-present designated primary path only. It
must not create the primary SQLite file.

### 10.1 Connection-close lifecycle

```text
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
FINAL_STORE_CONNECTION_CLOSE_REQUIRED=YES

NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO
```

After successful assembly and composition validation, the R2 execution consumer
must deterministically close the single store connection before the execution
unit terminates, using the already existing connection lifecycle surface
(`store._connection.close()` or equivalent existing surface reachable from the
assembled object graph), without invoking adapter business methods.

Exactly one store connection-close event is required:

1. close of the single existing-store construction connection before unit
   termination.

Additional constructions, path changes, create/recreate loops, reopen loops, or
second assemblies are forbidden.

## 11. Network / CRM / business write budget

```text
HIGHLEVEL_CALLS_MAX=0
HTTP_REQUEST_DISPATCHES_MAX=0
CRM_MUTATIONS_MAX=0
NOTE_WRITES_MAX=0
STAGE_TRANSITIONS_MAX=0

EXECUTION_CLAIMS_MAX=0
ATTEMPT_RECORDS_MAX=0
PROTOCOL_LEDGER_EVENT_WRITES_MAX=0
BUSINESS_LEDGER_EVENT_WRITES_MAX=0
```

No methods that create execution or business state may be invoked. Forbidden
examples include, without limitation:

```text
FORBIDDEN_METHOD_EXAMPLES=
  adapter.create_meeting_note|
  adapter.verify_meeting_note|
  transport.dispatch|
  http_client.request|
  acquire_claim|
  record_attempt|
  mark_dispatched|
  capture_response|
  append_protocol_call
```

Any insert into `execution_claims`, `attempts`, `protocol_ledger`, or
`business_ledger` is forbidden. Constructor-level metadata validation against
the existing store and in-memory composition binding are not business/protocol
event writes.

## 12. Payload, token, and identity privacy

```text
PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_MINIMUM_LIFETIME_REQUIRED=YES
PAYLOAD_PUBLISHED_ALLOWED=NO
PAYLOAD_PERSISTED_ALLOWED=NO
PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
```

Forbidden disclosures include:

- stdout/stderr payload or token printing;
- file, repository, log, telemetry, or proof persistence of payload or token
  material;
- payload or token hashing for proof;
- payload length as proof;
- token or credential fragments;
- screenshots containing payload or token material;
- shell history or command arguments containing payload or token material;
- exception messages/tracebacks containing payload or token material;
- publication of the operator source principal identity.

Proof may record only:

```text
PERMITTED_PROOF_FIELDS=
  authorization_artifact_identity|
  opaque_source_principal_attestation_reference|
  target_runtime_service_account_resource|
  impersonation_attempt_count|
  token_mint_count|
  exact_c4_resource_identifier|
  exact_b2_resource_identifier|
  c4_read_attempt_count|
  b2_read_attempt_count|
  designated_db_path|
  designated_db_parent|
  root_owned_db_env_key|
  parent_directory_preflight_result|
  designated_db_pre_execution_state|
  designated_sqlite_created|
  verified_capability_origin_class|
  verified_capability_synthetic_prefix_result|
  production_runtime_assembly_result|
  returned_object_type|
  verified_capability_bound|
  execution_store_bound|
  live_credential_bound|
  bounded_transport_bound|
  highlevel_http_client_instantiation_count|
  highlevel_transport_instantiation_count|
  note_path_adapter_assembly_count|
  http_request_dispatch_count|
  final_store_connection_close_result|
  store_connection_close_event_count|
  schema_version_validated|
  commitment_key_version_resource_validated|
  second_durable_database_created|
  operator_created_sidecars|
  success_or_failure|
  safe_sanitized_error_category_or_stop_code|
  forbidden_effect_zero_ledger
```

## 13. Authorized consumer and one-shot semantics

```text
AUTHORIZED_CONSUMER_UNIT=
  NW008_AT8W29_R2_PRODUCTION_COMPOSITION_VALIDATION_EXECUTION_001
AUTHORIZED_CONSUMER_CLASS=execution_proof

ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO

AUTHORIZATION_STATE_BEFORE_EXECUTION=
  AVAILABLE_IF_MERGED_AND_VERIFIED

AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_SERVICE_ACCOUNT_IMPERSONATION_ATTEMPT

AUTHORIZATION_STATE_ON_FIRST_IMPERSONATION_ATTEMPT=
  CONSUMED
AUTHORIZATION_STATE_AFTER_FIRST_IMPERSONATION_ATTEMPT=
  CONSUMED

FAILURE_RESTORES_AUTHORITY=NO
```

The grant is consumed when the future execution consumer begins the first
service-account impersonation attempt, regardless of success or failure.
Failure does not restore the grant. No other unit may consume or inherit it.

Exception: if a pre-execution filesystem or capability check fails closed before
any impersonation attempt with

- `STOP_CODE=DESIGNATED_SQLITE_PARENT_NOT_READY`,
- `STOP_CODE=DESIGNATED_SQLITE_MISSING_FOR_R2_COMPOSITION`, or
- `STOP_CODE=R2_VERIFIED_CAPABILITY_UNRESOLVED`,

the authorization remains unconsumed (`AUTHORIZATION_CONSUMED=NO`) and no R2
composition execution effects may proceed under this artifact until governance
disposition.

Before the first impersonation attempt, the execution consumer must
independently verify:

```text
PRE_EXECUTION_REQUIRED=
  EXACT_AUTHORIZATION_001_ARTIFACT_MERGED_TO_MAIN|
  EXACT_AUTHORIZATION_001_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  R1B_PROOF_MERGE_ANCESTOR_OF_ORIGIN_MAIN|
  R1B_PROOF_PRESENT_ON_ORIGIN_MAIN|
  R1B_RESULT_PASS|
  R1B_GATE_COMPLETE_YES|
  R1B_AUTHORIZATION_CONSUMED_AND_NOT_REUSABLE|
  PRODUCTION_RUNTIME_ENTRYPOINT_RESOLVED|
  PRODUCTION_ADC_IDENTITY_INJECTION_PATH_RESOLVED|
  C4_AND_B2_CLIENTS_USE_PROCESS_ADC|
  R2_VERIFIED_CAPABILITY_SOURCE_RESOLVED|
  R2_VERIFIED_CAPABILITY_SYNTHETIC_OR_COMPETITION_SAFE|
  EXACT_TARGET_RUNTIME_PRINCIPAL_MATCH|
  EXACT_IDENTITY_MECHANISM_MATCH|
  EXACT_C4_RESOURCE_MATCH|
  EXACT_B2_RESOURCE_MATCH|
  EXACT_DESIGNATED_DB_PATH_MATCH|
  EXACT_DESIGNATED_DB_PARENT_MATCH|
  ROOT_OWNED_DB_ENV_KEY_AND_VALUE_MATCH|
  PARENT_DIRECTORY_EXISTS|
  PARENT_PATH_IS_DIRECTORY|
  DESIGNATED_DB_PRESENT|
  SYNTHETIC_CAPABILITY_PRECREATED_IN_PROCESS|
  IDENTITY_SECRET_STORE_AND_COMPOSITION_BUDGETS_ENFORCED|
  NETWORK_CRM_BUSINESS_ZERO_BUDGETS_ENFORCED|
  STORE_CONNECTION_CLOSE_LIFECYCLE_ENFORCED|
  ZERO_DB_CREATE_ENFORCED|
  PAYLOAD_AND_TOKEN_NON_DISCLOSURE_ENFORCED
```

## 14. Success condition

R2 production-composition validation succeeds only if all of the following hold
within the fixed budgets and with zero forbidden effects or disclosures:

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=1

C4_READ_ATTEMPTS=1
B2_READ_ATTEMPTS=1
C4_EXACT_SECRET_ACCESS=PASS
B2_EXACT_SECRET_ACCESS=PASS

DESIGNATED_SQLITE_CREATED=NO
DESIGNATED_DB_PRE_EXECUTION_STATE=PRESENT

PRODUCTION_RUNTIME_ASSEMBLY=PASS
RETURNED_OBJECT_TYPE=NotePathAdapter

VERIFIED_CAPABILITY_BOUND=YES
EXECUTION_STORE_BOUND=YES
LIVE_CREDENTIAL_BOUND=YES
BOUNDED_TRANSPORT_BOUND=YES

HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS=1
HIGHLEVEL_TRANSPORT_INSTANTIATIONS=1
NOTE_PATH_ADAPTER_ASSEMBLIES=1

FINAL_STORE_CONNECTION_CLOSE=PASS
STORE_CONNECTION_CLOSE_EVENTS=1

SCHEMA_VERSION_VALIDATED=1

COMMITMENT_KEY_VERSION_RESOURCE_VALIDATED=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

EXECUTION_CLAIMS_CREATED=0
ATTEMPT_RECORDS_CREATED=0
PROTOCOL_LEDGER_EVENT_WRITES=0
BUSINESS_LEDGER_EVENT_WRITES=0

HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
NOTE_WRITES=0
STAGE_TRANSITIONS=0

PRODUCTION_RUNTIME_STARTS=0

IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0

SECOND_DURABLE_DATABASE_CREATED=NO
OPERATOR_CREATED_SIDECARS=NO
OPERATOR_MANAGED_SIDECAR_DELETES=NO

PAYLOADS_PUBLISHED=NO
PAYLOADS_PERSISTED=NO
TOKENS_PUBLISHED=NO
TOKENS_PERSISTED=NO

R2_GATE_COMPLETE=YES
```

An access result is PASS only when Secret Manager returns the payload for the
exact requested numeric-version resource under the impersonated runtime
principal, without resource or principal substitution. Production assembly is
PASS only when `assemble_bound_live_note_runtime` returns a `NotePathAdapter`
after the full composition sequence above, with existing-store construction at
the exact designated primary path, without creating the primary file, without
HTTP dispatch, and without CRM/business method invocation, followed by the
required one connection-close event.

## 15. Fail-closed behavior

If parent preflight, designated-DB preflight, capability precreation,
impersonation, token mint, C4 read, B2 read, existing-store construction,
metadata validation, production assembly, composition binding checks, or
required connection close fails, the execution consumer must STOP.

```text
FAIL_CLOSED=YES
RETRY_ON_FAILURE=NO
SECOND_TOKEN_MINT_OR_REFRESH_ON_FAILURE=NO
SECOND_C4_READ_ON_FAILURE=NO
SECOND_B2_READ_ON_FAILURE=NO
SECOND_ASSEMBLY_ON_FAILURE=NO
DISCOVER_ANOTHER_VERSION_ON_FAILURE=NO
USE_LATEST_ON_FAILURE=NO
ALTER_IAM_ON_FAILURE=NO
CHANGE_RESOURCE_IDENTITY_ON_FAILURE=NO
CHANGE_RUNTIME_PRINCIPAL_ON_FAILURE=NO
CREATE_PARENT_DIRECTORY_ON_FAILURE=NO
CHMOD_CHOWN_PARENT_ON_FAILURE=NO
DB_CREATE_ON_FAILURE=NO
DB_REPAIR_ON_FAILURE=NO
DB_DELETE_ON_FAILURE=NO
DB_RECREATE_ON_FAILURE=NO
DB_RENAME_ON_FAILURE=NO
DB_TRUNCATE_ON_FAILURE=NO
OPERATOR_SIDECAR_DELETE_ON_FAILURE=NO
CLEANUP_MUTATION_ON_FAILURE=NO
START_PRODUCTION_RUNTIME_ON_FAILURE=NO
CALL_HIGHLEVEL_ON_FAILURE=NO
HTTP_DISPATCH_ON_FAILURE=NO
CRM_MUTATION_ON_FAILURE=NO
IMPLEMENT_NEW_STORE_CLOSE_API_ON_FAILURE=NO
SOURCE_CODE_CHANGE_ON_FAILURE=NO
FALL_BACK_TO_DIRECT_USER_ADC_SECRET_ACCESS_ON_FAILURE=NO
FALL_BACK_TO_AT8W28_R1B_AUTHORIZATION_ON_FAILURE=NO
ESCALATE_TO_R3_ON_FAILURE=NO
ESCALATE_TO_R4_ON_FAILURE=NO
```

No retry. No second token. No second secret read. No second assembly. No store
repair. No DB delete. No DB recreate. No HighLevel dispatch. No parent-path
repair. No operator sidecar deletion. No source-code or new close-API
implementation under this grant.

If failure occurs after the first impersonation attempt:

```text
AUTHORIZATION_STATE=CONSUMED
FAILURE_RESTORES_AUTHORITY=NO
```

Safe failure categories may identify non-sensitive classes such as
authentication unavailable, impersonation denied, permission denied, resource
not found, disabled version, dependency unavailable, designated parent not
ready, designated path missing for R2 composition, capability unresolved,
schema/metadata mismatch, assembly failure, connection-close failure, or
sanitized transport/store failure. They must not include payload, token,
credential, header, or operator principal material.

## 16. Non-escalation

```text
R2_SUCCESS_AUTHORIZES_R3=NO
R2_SUCCESS_AUTHORIZES_R4=NO
R2_SUCCESS_AUTHORIZES_HIGHLEVEL_DISPATCH=NO
R2_SUCCESS_AUTHORIZES_HTTP_REQUEST_DISPATCH=NO
R2_SUCCESS_AUTHORIZES_CRM_MUTATION=NO
R2_SUCCESS_AUTHORIZES_NOTE_WRITE=NO
R2_SUCCESS_AUTHORIZES_STAGE_TRANSITION=NO
R2_SUCCESS_AUTHORIZES_BUSINESS_EXECUTION=NO
R2_SUCCESS_AUTHORIZES_EXECUTION_CLAIMS=NO
R2_SUCCESS_AUTHORIZES_ATTEMPT_RECORDS=NO
R2_SUCCESS_AUTHORIZES_PRODUCTION_RUNTIME_START=NO
R2_SUCCESS_AUTHORIZES_IAM_MUTATION=NO
R2_SUCCESS_AUTHORIZES_STANDING_TOKEN=NO
R2_SUCCESS_AUTHORIZES_DEPLOYMENT=NO
```

Every later runtime-validation or business-execution gate requires a separate,
explicit human-governed authorization.

## 17. Authoring pre-flight and zero-effect attestation

```text
PREFLIGHT_PWD=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=
  auth/nw008-at8w29-r2-production-composition-validation-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_SHA=
  f5ec221a667db91e43684f3acad98913b6e00bfa
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO

R1B_PROOF_PR=207
R1B_PROOF_MERGE_COMMIT=
  f5ec221a667db91e43684f3acad98913b6e00bfa
R1B_RESULT=PASS
R1B_GATE_COMPLETE=YES
R1B_AUTHORIZATION_STATE=CONSUMED
R1B_AUTHORIZATION_REUSABLE=NO

PRODUCTION_RUNTIME_ENTRYPOINT_RESOLVED=YES
PRODUCTION_ADC_IDENTITY_INJECTION_PATH_RESOLVED=YES
C4_SECRET_MANAGER_CLIENT_USES_TARGET_RUNTIME_SA=YES
B2_SECRET_MANAGER_CLIENT_USES_TARGET_RUNTIME_SA=YES
DIRECT_USER_ADC_SECRET_ACCESS=NO
R2_VERIFIED_CAPABILITY_SOURCE_RESOLVED=YES
R2_VERIFIED_CAPABILITY_SYNTHETIC_OR_COMPETITION_SAFE=YES
ASSEMBLY_HTTP_DISPATCH_BY_ITSELF=NO
ASSEMBLY_CRM_MUTATION_BY_ITSELF=NO
R2_AUTHORIZATION_DESIGNABLE=YES
SOURCE_CODE_CHANGE_REQUIRED=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=1
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
C4_SECRET_READ_ATTEMPTS=0
B2_SECRET_READ_ATTEMPTS=0
SECRET_PAYLOAD_READS=0
SQLITE_OPENED=NO
SQLITE_CREATED=NO
AT1_EXECUTION_STORE_CONSTRUCTIONS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
PRODUCTION_RUNTIME_ASSEMBLY=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

Authoring performed source-only inspection of main-branch implementation files
and existence-only observation that the designated DB path is expected present
from R1B completion. That observation is not execution, does not open SQLite,
does not read secrets, does not assemble runtime, and does not consume this
authorization.

## 18. Review disposition

```text
R2_PRODUCTION_COMPOSITION_VALIDATION_DESIGNABLE=YES
R2_PRODUCTION_COMPOSITION_VALIDATION_EXECUTION_READY_AFTER_MERGE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=1
DESIGNATED_SQLITE_CREATE_MAX=0
AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=1
PRODUCTION_RUNTIME_ASSEMBLY_MAX=1
HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS_MAX=1
HIGHLEVEL_TRANSPORT_INSTANTIATIONS_MAX=1
NOTE_PATH_ADAPTER_ASSEMBLIES_MAX=1
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
HIGHLEVEL_CALLS_MAX=0
HTTP_REQUEST_DISPATCHES_MAX=0
CRM_MUTATIONS_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO

R2_SUCCESS_AUTHORIZES_R3=NO
R2_SUCCESS_AUTHORIZES_R4=NO
R2_SUCCESS_AUTHORIZES_HIGHLEVEL_DISPATCH=NO
R2_SUCCESS_AUTHORIZES_CRM_MUTATION=NO

EXECUTION_PERFORMED=NO
SQLITE_OPENED=NO
SQLITE_CREATED=NO
SECRET_PAYLOAD_READS=0
PRODUCTION_RUNTIME_ASSEMBLY=0

NEXT=
  return authorization PR to ChatGPT for independent reviewer disposition
```
