# NW-008 AT8W27 R1B Execution-Store Initialization Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W27_R1B_EXECUTION_STORE_INITIALIZATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w27-r1b-execution-store-initialization-authorization-001.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w27-r1b-execution-store-initialization-authorization-001

BASE_REF=origin/main
BASE_SHA=
  bf11bbdb7a022eb33a01a4fb6d5bfe9ecc4fad5f

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=HUMAN_MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
```

This artifact is planning-only. Creating, reviewing, or merging it does not
impersonate a service account, mint a token, read a Secret Manager payload,
open or create SQLite, call HighLevel, mutate CRM or IAM, assemble production
runtime, or start production runtime.

The bounded grant becomes usable only after human review and merge places this
exact artifact on `main`, followed by independent verification by the sole
authorized execution consumer.

```text
EXECUTION_PERFORMED_IN_THIS_UNIT=NO
SERVICE_ACCOUNT_IMPERSONATION_IN_THIS_UNIT=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_IN_THIS_UNIT=0
SECRET_MANAGER_ACCESS_PERFORMED_IN_THIS_UNIT=NO
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
HIGHLEVEL_CALLS_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
SQLITE_CREATION_IN_THIS_UNIT=0
SQLITE_OPEN_IN_THIS_UNIT=0
AT1_EXECUTION_STORE_CONSTRUCTIONS_IN_THIS_UNIT=0
IAM_MUTATIONS_IN_THIS_UNIT=0
DEPLOYMENTS_IN_THIS_UNIT=0
PRODUCTION_RUNTIME_STARTS_IN_THIS_UNIT=0
AUTHORIZATION_CONSUMED_IN_THIS_UNIT=NO
```

## 2. Purpose and explicit non-authority

This artifact conditionally authorizes one later bounded initialization and
reopen validation of the exact designated At1ExecutionStore. The future
execution consumer may establish only whether:

1. a fresh short-lived runtime-SA identity can be acquired once;
2. the exact C4 commitment-key version can be read once under that identity;
3. At1ExecutionStore can be constructed once at the exact designated path,
   creating the store file and constructor-required schema/metadata only;
4. the store can be closed and reopened once using the same in-memory C4
   material; and
5. constructor-level metadata/schema checks succeed on both constructions.

```text
PURPOSE=
  ONE_BOUNDED_INITIALIZATION_AND_REOPEN_VALIDATION_OF_EXACT_DESIGNATED_AT1_EXECUTION_STORE

PRODUCTION_RUNTIME_EXECUTION_AUTHORIZED=NO
PRODUCTION_RUNTIME_ASSEMBLY_AUTHORIZED=NO
HIGHLEVEL_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
B2_SECRET_READ_AUTHORIZED=NO
BUSINESS_EXECUTION_AUTHORIZED=NO
EXECUTION_CLAIM_AUTHORIZED=NO
ATTEMPT_RECORD_AUTHORIZED=NO
PROTOCOL_LEDGER_WRITE_AUTHORIZED=NO
BUSINESS_LEDGER_WRITE_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATE_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
STANDING_TOKEN_AUTHORITY=NO
```

A successful R1B proves only designated-store initialization and reopen under
the bound runtime principal, exact C4 material, and constructor-level schema
checks. It does not authorize business execution, execution claims, attempts,
HighLevel, B2, CRM mutation, runtime assembly, production runtime start, IAM
mutation, key creation, deployment, or any later gate (R2/R3/R4).

## 3. Durable source prerequisites

```text
SOURCE_R1A_PROOF_PR=203
SOURCE_R1A_PROOF_PR_STATE=MERGED
SOURCE_R1A_PROOF_MERGE_COMMIT=
  bf11bbdb7a022eb33a01a4fb6d5bfe9ecc4fad5f
SOURCE_R1A_PROOF_MERGE_ON_ORIGIN_MAIN=YES
SOURCE_R1A_PROOF=
  proof/nw008/at-8w26/nw008-at8w26-r1a-exact-secret-runtime-validation-execution-proof-001.md
SOURCE_R1A_PROOF_ON_ORIGIN_MAIN=YES
SOURCE_R1A_RESULT=PASS
SOURCE_R1A_GATE_COMPLETE=YES

SOURCE_R1A_AUTHORIZATION=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-002.md
SOURCE_R1A_AUTHORIZATION_PR=202
SOURCE_R1A_AUTHORIZATION_MERGE=
  9b5fd1603d241aa78fc4b61fea6b1153fff90c60
SOURCE_R1A_AUTHORIZATION_STATE=CONSUMED
SOURCE_R1A_AUTHORIZATION_REUSABLE=NO
SOURCE_R1A_AUTHORIZATION_TRANSFERABLE=NO

SOURCE_IMPLEMENTATION_PR=200
SOURCE_IMPLEMENTATION_MERGE=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
SOURCE_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w25/nw008-at8w25-b2-c4-c3-c2-offline-implementation-proof-001.md
SOURCE_IMPLEMENTATION_PROOF_ON_ORIGIN_MAIN=YES

C4_IMPLEMENTATION_DURABLE=YES
AT1_EXECUTION_STORE_IMPLEMENTATION_DURABLE=YES
GOOGLE_CLOUD_SECRET_MANAGER_VERSION=2.27.0
```

R1A is complete and consumed. This R1B authorization does not reopen, reuse,
or extend the R1A grant. R1A success does not itself authorize R1B; R1B requires
this separate human-governed authorization after merge and consumer
verification.

## 4. Identity binding

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
impersonation from the operator's local user ADC. The consumer must not:

- publish or persist the operator principal identity;
- use a user-managed service-account key;
- use direct user ADC as the Secret Manager access principal;
- accept a caller-supplied runtime identity override; or
- impersonate any principal other than the exact target runtime SA above.

Proof may reference only the opaque attestation ref
`NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af` for the source principal
class, not the human operator email or other identifying material.

## 5. Identity effect budget

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1

IAM_MUTATIONS_MAX=0
IAM_POLICY_WRITES_MAX=0
SERVICE_ACCOUNT_KEY_CREATE_MAX=0

SECOND_TOKEN_MINT_OR_REFRESH=FORBIDDEN

TOKEN_LOGGING_ALLOWED=NO
TOKEN_PERSISTENCE_ALLOWED=NO
TOKEN_HASHING_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
TOKEN_STDOUT_STDERR_ALLOWED=NO

TOKEN_USE_SCOPE=
  R1B_EXACT_C4_READ_ONLY

TOKEN_REUSE_AFTER_R1B=FORBIDDEN
TOKEN_LIFETIME=SHORT_LIVED_MINIMUM_NECESSARY
```

Exactly one impersonation attempt and exactly one short-lived access-token mint
are permitted for the exact target runtime SA. The token may be used only for
the exact C4 secret read in this unit. After R1B ends (success or fail-closed
stop), the token must not be reused, refreshed, logged, persisted, hashed for
proof, or captured in fragments.

## 6. Exact secret resources and secret effect budget

Exactly one Secret Manager resource is permitted:

```text
C4_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

PERMITTED_SECRET_RESOURCE_COUNT=1
OTHER_SECRET_RESOURCES_PERMITTED=NO
```

```text
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=0
OTHER_SECRET_READ_ATTEMPTS_MAX=0
TOTAL_SECRET_READ_ATTEMPTS_MAX=1

C4_RETRIES_MAX=0

SECRET_LIST_CALLS_MAX=0
SECRET_VERSION_LIST_CALLS_MAX=0
SECRET_METADATA_DISCOVERY_CALLS_MAX=0

LATEST_ALLOWED=NO
ALIAS_RESOLUTION_ALLOWED=NO
VERSION_DISCOVERY_ALLOWED=NO
SECRET_DISCOVERY_ALLOWED=NO
CALLER_RESOURCE_OVERRIDE_ALLOWED=NO
```

The exact C4 resource string above is normative. The consumer may not
substitute project number/id forms, change secret names, change numeric
versions, use `latest`, resolve aliases, list secrets/versions, discover
alternatives, accept caller overrides, read B2, read any other secret, or retry
the C4 read.

```text
C4_PAYLOAD_PROCESS_MEMORY_ONLY=YES
C4_PAYLOAD_PERSISTED_ALLOWED=NO
C4_PAYLOAD_PUBLISHED_ALLOWED=NO
C4_PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
C4_PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
```

C4 payload may exist only in process memory for the minimum lifetime required
to construct At1ExecutionStore twice (initial creation and controlled reopen)
and to complete constructor-level validation. It must not be written into the
SQLite file as raw key material beyond whatever the existing constructor
already persists as the non-secret
`commitment_key_version_resource` metadata string.

## 7. Exact designated store target

```text
DESIGNATED_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

DESIGNATED_PRIMARY_SQLITE_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

DESIGNATED_DB_PARENT=
  /Users/achandler/Library/Application Support/mg-guide/nw008

OTHER_DB_PATHS_ALLOWED=NO
OTHER_PRIMARY_DB_PATHS_ALLOWED=NO
SECOND_DURABLE_DATABASE_ALLOWED=NO
ALTERNATE_DATABASE_PATH_ALLOWED=NO
CALLER_DB_PATH_OVERRIDE_ALLOWED=NO

EXPECTED_PRE_EXECUTION_DB_STATE=ABSENT

EXPECTED_SCHEMA_VERSION=1

EXPECTED_COMMITMENT_KEY_VERSION_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
```

Only the exact designated primary path may be created or opened as the durable
At1ExecutionStore database. No alternate path, temporary validation DB, copied
DB, backup DB, test path, or caller override is permitted under this grant.

### 7.1 Primary DB versus SQLite-engine transient sidecars

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
sidecars (for example rollback/WAL/journal companions) in the same directory as
the designated primary DB only, solely as an incidental effect of the already
authorized At1ExecutionStore constructor/open lifecycle.

This does **not** authorize:

- a second durable database;
- an alternate primary DB path;
- operator-created journal, backup, copy, or temporary validation DB files;
- operator-managed sidecar deletion or cleanup mutation.

`DB_DELETE_ALLOWED=NO` means no operator/application deletion of the primary DB
and no cleanup mutation by the consumer. It does **not** prohibit SQLite's
internal automatic transaction-journal create/remove lifecycle.

## 8. Pre-execution fail-closed checks

Before impersonation or any Secret Manager call, the execution consumer must
perform the following existence/type checks only, in order, and must not mutate
filesystem state.

### 8.1 Parent directory pre-consumption check

```text
DESIGNATED_DB_PARENT=
  /Users/achandler/Library/Application Support/mg-guide/nw008

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

If the exact parent path does not exist or is not a directory, the consumer must
stop immediately and return to governance. In that fail-closed stop the consumer
must not:

- create the parent directory;
- chmod/chown or otherwise repair the path;
- impersonate the runtime SA;
- mint a token;
- read C4;
- touch or create SQLite;
- construct At1ExecutionStore.

### 8.2 Designated primary DB pre-existence check

```text
PRE_EXECUTION_DB_CHECK=
  EXACT_DESIGNATED_PRIMARY_PATH_EXISTENCE_ONLY

IF_DESIGNATED_DB_FILE_EXISTS=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=DESIGNATED_SQLITE_PREEXISTS_UNEXPECTEDLY
  STOP=YES
```

If the designated primary file already exists, the consumer must stop
immediately and return to governance. In that fail-closed stop the consumer
must not:

- delete, rename, truncate, or repair the file;
- inspect payload rows;
- open the file with sqlite3 or any SQLite API;
- read C4;
- impersonate the runtime SA;
- mint a token;
- construct At1ExecutionStore.

Existence/type-only checking of the exact parent and designated primary path is
permitted. No other filesystem mutation is permitted by the pre-checks.

## 9. Store effect budget

```text
DESIGNATED_SQLITE_CREATE_MAX=1

AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=2
AT1_EXECUTION_STORE_INITIAL_CREATION_MAX=1
AT1_EXECUTION_STORE_REOPEN_MAX=1

OTHER_DB_PATHS_ALLOWED=NO
OTHER_PRIMARY_DB_PATHS_ALLOWED=NO
SECOND_DURABLE_DATABASE_ALLOWED=NO
ALTERNATE_DATABASE_PATH_ALLOWED=NO

DB_DELETE_ALLOWED=NO
DB_RENAME_ALLOWED=NO
DB_TRUNCATE_ALLOWED=NO
DB_REPAIR_ALLOWED=NO

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
OPERATOR_CREATED_SIDECARS_ALLOWED=NO
OPERATOR_MANAGED_SIDECAR_DELETE_ALLOWED=NO
```

The first At1ExecutionStore construction may create, at the exact designated
primary path only:

- the primary SQLite file;
- table `at1_store_metadata`;
- table `execution_claims`;
- table `attempts`;
- table `protocol_ledger`;
- table `business_ledger`;
- exactly one metadata row required by the existing implementation.

Incidental SQLite-engine-managed transient sidecars in the same parent directory
remain permitted solely under §7.1 and do not count as a second durable database
or as an additional `DESIGNATED_SQLITE_CREATE`.

Permitted immutable metadata values:

```text
schema_version=1

commitment_key_version_resource=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
```

### 9.1 Connection-close lifecycle

```text
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=2
FIRST_STORE_CONNECTION_CLOSE_REQUIRED_BEFORE_REOPEN=YES
FINAL_REOPENED_STORE_CONNECTION_CLOSE_REQUIRED=YES

NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO
```

The second construction is a controlled reopen only. It must use the same
in-memory C4 material and the same exact designated primary path. It may
validate constructor-level metadata/schema checks. It must not recreate schema
as a repair path, must not delete or replace the primary file, and must not
write business or protocol rows.

After initial construction succeeds, the R1B execution consumer must
deterministically close the connection from the first At1ExecutionStore instance
before constructing the second instance. After successful reopen validation, the
second store connection must also be closed before the execution unit
terminates.

Exactly two store connection-close events are required:

1. close of the initial-construction store connection before reopen; and
2. close of the reopened store connection before unit termination.

Additional constructions, path changes, or reopen loops are forbidden. This
authorization does not authorize a new store-close API, source-code change, or
any `src/**` / `tests/**` modification. The consumer must use the already
existing connection lifecycle surface.

## 10. Business / protocol write budget

```text
EXECUTION_CLAIMS_MAX=0
ATTEMPT_RECORDS_MAX=0
PROTOCOL_LEDGER_EVENT_WRITES_MAX=0
BUSINESS_LEDGER_EVENT_WRITES_MAX=0

HIGHLEVEL_CALLS_MAX=0
CRM_MUTATIONS_MAX=0
NOTE_WRITES_MAX=0
STAGE_TRANSITIONS_MAX=0
```

No methods that create execution or business state may be invoked. Forbidden
examples include, without limitation:

```text
FORBIDDEN_METHOD_EXAMPLES=
  acquire_claim|
  record_attempt|
  mark_dispatched|
  capture_response|
  append_protocol_call
```

Constructor-required empty table creation and the single metadata row are not
business/protocol event writes. Any insert into `execution_claims`,
`attempts`, `protocol_ledger`, or `business_ledger` beyond empty schema
creation is forbidden.

## 11. Runtime boundary

```text
PRODUCTION_RUNTIME_STARTS_MAX=0
PRODUCTION_RUNTIME_ASSEMBLY_MAX=0
HIGHLEVEL_HTTP_CLIENT_INSTANTIATION_MAX=0
HIGHLEVEL_TRANSPORT_INSTANTIATION_MAX=0
```

Do not call:

```text
assemble_bound_live_note_runtime()
```

Do not instantiate the HighLevel HTTP client or transport. Do not assemble or
start production runtime under any framing.

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
  c4_read_attempt_count|
  designated_db_path|
  designated_db_parent|
  parent_directory_preflight_result|
  designated_db_pre_execution_state|
  designated_sqlite_created|
  at1_execution_store_initial_construction_result|
  first_store_connection_close_before_reopen_result|
  at1_execution_store_reopen_result|
  final_reopened_store_connection_close_result|
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
  NW008_AT8W27_R1B_EXECUTION_STORE_INITIALIZATION_EXECUTION_001
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

Exception: if either pre-execution filesystem check fails closed before any
impersonation attempt with

- `STOP_CODE=DESIGNATED_SQLITE_PARENT_NOT_READY`, or
- `STOP_CODE=DESIGNATED_SQLITE_PREEXISTS_UNEXPECTEDLY`,

the authorization remains unconsumed (`AUTHORIZATION_CONSUMED=NO`) and no R1B
execution effects may proceed under this artifact until governance disposition.

Before the first impersonation attempt, the execution consumer must
independently verify:

```text
PRE_EXECUTION_REQUIRED=
  EXACT_AUTHORIZATION_001_ARTIFACT_MERGED_TO_MAIN|
  EXACT_AUTHORIZATION_001_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_R1A_PROOF_MERGE_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_R1A_PROOF_PRESENT_ON_ORIGIN_MAIN|
  SOURCE_R1A_RESULT_PASS|
  SOURCE_R1A_AUTHORIZATION_CONSUMED_AND_NOT_REUSABLE|
  EXACT_TARGET_RUNTIME_PRINCIPAL_MATCH|
  EXACT_IDENTITY_MECHANISM_MATCH|
  EXACT_C4_RESOURCE_MATCH|
  EXACT_DESIGNATED_DB_PATH_MATCH|
  EXACT_DESIGNATED_DB_PARENT_MATCH|
  PARENT_DIRECTORY_EXISTS|
  PARENT_PATH_IS_DIRECTORY|
  DESIGNATED_DB_ABSENT|
  IDENTITY_SECRET_AND_STORE_EFFECT_BUDGETS_ENFORCED|
  BUSINESS_PROTOCOL_AND_RUNTIME_ZERO_BUDGETS_ENFORCED|
  STORE_CONNECTION_CLOSE_LIFECYCLE_ENFORCED|
  PAYLOAD_AND_TOKEN_NON_DISCLOSURE_ENFORCED
```

## 14. Success condition

R1B succeeds only if all of the following hold within the fixed budgets and
with zero forbidden effects or disclosures:

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=1

C4_READ_ATTEMPTS=1
C4_EXACT_SECRET_ACCESS=PASS

DESIGNATED_SQLITE_CREATED=YES

AT1_EXECUTION_STORE_INITIAL_CONSTRUCTION=PASS
FIRST_STORE_CONNECTION_CLOSE_BEFORE_REOPEN=PASS
AT1_EXECUTION_STORE_REOPEN=PASS
FINAL_REOPENED_STORE_CONNECTION_CLOSE=PASS
STORE_CONNECTION_CLOSE_EVENTS=2

SCHEMA_VERSION_VALIDATED=1

COMMITMENT_KEY_VERSION_RESOURCE_VALIDATED=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

EXECUTION_CLAIMS_CREATED=0
ATTEMPT_RECORDS_CREATED=0
PROTOCOL_LEDGER_EVENT_WRITES=0
BUSINESS_LEDGER_EVENT_WRITES=0

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
B2_SECRET_READ_ATTEMPTS=0

PRODUCTION_RUNTIME_STARTS=0
PRODUCTION_RUNTIME_ASSEMBLY=0

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
```

An access result is PASS only when Secret Manager returns the payload for the
exact requested numeric-version C4 resource under the impersonated runtime
principal, without resource or principal substitution. Store construction and
reopen are PASS only when the existing At1ExecutionStore constructor completes
successfully at the exact designated primary path and validates
`schema_version=1` plus the exact commitment-key version resource string, with
the required two connection-close events completed using the existing lifecycle
surface and without source-code or new close-API changes.

## 15. Fail-closed behavior

If parent preflight, designated-DB preflight, impersonation, token mint, C4
read, initial construction, required first close, reopen, or final close fails,
the execution consumer must STOP.

```text
FAIL_CLOSED=YES
RETRY_ON_FAILURE=NO
SECOND_TOKEN_MINT_OR_REFRESH_ON_FAILURE=NO
SECOND_C4_READ_ON_FAILURE=NO
DISCOVER_ANOTHER_VERSION_ON_FAILURE=NO
USE_LATEST_ON_FAILURE=NO
ALTER_IAM_ON_FAILURE=NO
CHANGE_RESOURCE_IDENTITY_ON_FAILURE=NO
CHANGE_RUNTIME_PRINCIPAL_ON_FAILURE=NO
CREATE_PARENT_DIRECTORY_ON_FAILURE=NO
CHMOD_CHOWN_PARENT_ON_FAILURE=NO
DB_REPAIR_ON_FAILURE=NO
DB_DELETE_ON_FAILURE=NO
DB_RENAME_ON_FAILURE=NO
DB_TRUNCATE_ON_FAILURE=NO
OPERATOR_SIDECAR_DELETE_ON_FAILURE=NO
CLEANUP_MUTATION_ON_FAILURE=NO
START_PRODUCTION_RUNTIME_ON_FAILURE=NO
ASSEMBLE_PRODUCTION_RUNTIME_ON_FAILURE=NO
CALL_HIGHLEVEL_ON_FAILURE=NO
READ_B2_ON_FAILURE=NO
IMPLEMENT_NEW_STORE_CLOSE_API_ON_FAILURE=NO
SOURCE_CODE_CHANGE_ON_FAILURE=NO
FALL_BACK_TO_DIRECT_USER_ADC_SECRET_ACCESS_ON_FAILURE=NO
FALL_BACK_TO_R1A_AUTHORIZATION_ON_FAILURE=NO
```

No retry. No second token. No second C4 read. No DB repair. No cleanup
mutation. No parent-path repair. No operator sidecar deletion. No source-code
or new close-API implementation under this grant.

Safe failure categories may identify non-sensitive classes such as
authentication unavailable, impersonation denied, permission denied, resource
not found, disabled version, dependency unavailable, designated parent not
ready, designated path pre-exists, schema/metadata mismatch, connection-close
failure, or sanitized transport/store failure. They must not include payload,
token, credential, header, or operator principal material.

## 16. Non-escalation

```text
R1B_SUCCESS_AUTHORIZES_R2=NO
R1B_SUCCESS_AUTHORIZES_R3=NO
R1B_SUCCESS_AUTHORIZES_R4=NO

R1B_SUCCESS_AUTHORIZES_HIGHLEVEL=NO
R1B_SUCCESS_AUTHORIZES_CRM_MUTATION=NO
R1B_SUCCESS_AUTHORIZES_RUNTIME_ASSEMBLY=NO
R1B_SUCCESS_AUTHORIZES_PRODUCTION_RUNTIME=NO
R1B_SUCCESS_AUTHORIZES_B2_READ=NO
R1B_SUCCESS_AUTHORIZES_BUSINESS_EXECUTION=NO
R1B_SUCCESS_AUTHORIZES_EXECUTION_CLAIMS=NO
R1B_SUCCESS_AUTHORIZES_ATTEMPT_RECORDS=NO
R1B_SUCCESS_AUTHORIZES_IAM_MUTATION=NO
R1B_SUCCESS_AUTHORIZES_STANDING_TOKEN=NO
R1B_SUCCESS_AUTHORIZES_DEPLOYMENT=NO
```

Every later runtime-validation or business-execution gate requires a separate,
explicit human-governed authorization.

## 17. Authoring pre-flight and zero-effect attestation

```text
PREFLIGHT_PWD=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=
  auth/nw008-at8w27-r1b-execution-store-initialization-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_SHA=
  bf11bbdb7a022eb33a01a4fb6d5bfe9ecc4fad5f
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO

PR203_MERGED=YES
R1A_PROOF_ON_ORIGIN_MAIN=YES
R1A_RESULT=PASS
R1A_GATE_COMPLETE=YES
SOURCE_R1A_AUTHORIZATION_STATE=CONSUMED
SOURCE_R1A_AUTHORIZATION_REUSABLE=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=1
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
SERVICE_ACCOUNT_IMPERSONATION=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
SECRET_PAYLOAD_READS=0
SQLITE_OPENED=NO
SQLITE_CREATED=NO
AT1_EXECUTION_STORE_CONSTRUCTIONS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

Authoring performed existence-only observation that the designated DB path was
absent at authoring time. That observation is not execution, does not open
SQLite, and does not consume this authorization.

## 18. Review disposition

```text
R1B_DESIGNABLE=YES
R1B_EXECUTION_READY_AFTER_MERGE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=0
DESIGNATED_SQLITE_CREATE_MAX=1
AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=2
AT1_EXECUTION_STORE_INITIAL_CREATION_MAX=1
AT1_EXECUTION_STORE_REOPEN_MAX=1
HIGHLEVEL_CALLS_MAX=0
CRM_MUTATIONS_MAX=0
PRODUCTION_RUNTIME_ASSEMBLY_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=2
NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO

R1B_SUCCESS_AUTHORIZES_R2=NO
R1B_SUCCESS_AUTHORIZES_R3=NO
R1B_SUCCESS_AUTHORIZES_R4=NO

EXECUTION_PERFORMED=NO
SQLITE_CREATED=NO
SECRET_PAYLOAD_READS=0

NEXT=
  return amended PR #204 to ChatGPT for exact-head reviewer disposition
```
