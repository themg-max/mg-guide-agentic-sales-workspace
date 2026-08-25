# NW-008 AT8W28 R1B Existing-Store Revalidation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W28_R1B_EXISTING_STORE_REVALIDATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w28-r1b-existing-store-revalidation-authorization-001.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w28-r1b-existing-store-revalidation-authorization-001

BASE_REF=origin/main
BASE_SHA=
  d002a0e145019696825decee0d6a14b6c716b7d9

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

This artifact conditionally authorizes one later bounded revalidation of the
already-present exact designated At1ExecutionStore. The future execution
consumer may establish only whether:

1. a fresh short-lived runtime-SA identity can be acquired once;
2. the exact C4 commitment-key version can be read once under that identity;
3. At1ExecutionStore can be constructed once against the already-present
   designated primary SQLite path using that in-memory C4 material;
4. constructor-level metadata/schema checks succeed
   (`schema_version=1` and the exact commitment-key version resource); and
5. the single store connection is deterministically closed afterward.

```text
PURPOSE=
  ONE_BOUNDED_EXISTING_STORE_REVALIDATION_OF_EXACT_DESIGNATED_AT1_EXECUTION_STORE

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
DB_CREATE_AUTHORIZED=NO
DB_DELETE_AUTHORIZED=NO
DB_RECREATE_AUTHORIZED=NO
DB_REPAIR_AUTHORIZED=NO
```

A successful R1B existing-store revalidation proves only that the already
present designated store can be opened once under the bound runtime principal,
exact C4 material, and constructor-level schema checks, then closed once. It
does not authorize business execution, execution claims, attempts, HighLevel,
B2, CRM mutation, runtime assembly, production runtime start, IAM mutation, key
creation, deployment, DB create/recreate/repair/delete, or any later gate
(R2/R3/R4).

This grant does **not** revive, transfer, reuse, or extend the consumed AT8W27
R1B initialization authorization (PR #204).

## 3. Durable source prerequisites and exception proof

```text
SOURCE_EXCEPTION_PROOF_PR=205
SOURCE_EXCEPTION_PROOF_PR_STATE=MERGED
SOURCE_EXCEPTION_PROOF_HEAD=
  e4f4acadbee94aea26c0121dc171d6d024a6ab30
SOURCE_EXCEPTION_PROOF_MERGE_COMMIT=
  d002a0e145019696825decee0d6a14b6c716b7d9
SOURCE_EXCEPTION_PROOF_MERGE_ON_ORIGIN_MAIN=YES
SOURCE_EXCEPTION_PROOF=
  proof/nw008/at-8w27/nw008-at8w27-r1b-execution-store-initialization-execution-proof-001.md
SOURCE_EXCEPTION_PROOF_ON_ORIGIN_MAIN=YES

SOURCE_TECHNICAL_STORE_VALIDATION=PASS
SOURCE_GOVERNED_R1B_RESULT=AUTHORIZATION_BUDGET_EXCEEDED
SOURCE_R1B_GATE_COMPLETE=NO

SOURCE_R1B_AUTHORIZATION=
  governance/authorizations/nw008-at8w27-r1b-execution-store-initialization-authorization-001.md
SOURCE_R1B_AUTHORIZATION_PR=204
SOURCE_R1B_AUTHORIZATION_MERGE=
  f048034fe4992273568a367eb7dec4491708bc8b
SOURCE_R1B_AUTHORIZATION_STATE=CONSUMED
SOURCE_R1B_AUTHORIZATION_REUSABLE=NO
SOURCE_R1B_AUTHORIZATION_TRANSFERABLE=NO

SOURCE_R1A_PROOF_PR=203
SOURCE_R1A_PROOF_PR_STATE=MERGED
SOURCE_R1A_PROOF_MERGE_COMMIT=
  bf11bbdb7a022eb33a01a4fb6d5bfe9ecc4fad5f
SOURCE_R1A_PROOF_ON_ORIGIN_MAIN=YES
SOURCE_R1A_RESULT=PASS
SOURCE_R1A_GATE_COMPLETE=YES

SOURCE_R1A_AUTHORIZATION=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-002.md
SOURCE_R1A_AUTHORIZATION_PR=202
SOURCE_R1A_AUTHORIZATION_STATE=CONSUMED
SOURCE_R1A_AUTHORIZATION_REUSABLE=NO

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

PR #205 records that technical store validation passed under an unauthorized
retry after the first attempt already consumed the AT8W27 R1B grant, so the
governed R1B result is `AUTHORIZATION_BUDGET_EXCEEDED` and
`R1B_GATE_COMPLETE=NO`. The designated store file is therefore expected to be
present. This AT8W28 authorization is a fresh one-shot revalidation grant for
that existing store only. It does not reopen, reuse, or extend the consumed
AT8W27 R1B initialization grant.

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
RETRY=FORBIDDEN

TOKEN_LOGGING_ALLOWED=NO
TOKEN_PERSISTENCE_ALLOWED=NO
TOKEN_HASHING_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
TOKEN_STDOUT_STDERR_ALLOWED=NO

TOKEN_USE_SCOPE=
  R1B_EXISTING_STORE_REVALIDATION_EXACT_C4_READ_ONLY

TOKEN_REUSE_AFTER_R1B_REVALIDATION=FORBIDDEN
TOKEN_LIFETIME=SHORT_LIVED_MINIMUM_NECESSARY
```

Exactly one impersonation attempt and exactly one short-lived access-token mint
are permitted for the exact target runtime SA. The token may be used only for
the exact C4 secret read in this unit. After R1B revalidation ends (success or
fail-closed stop), the token must not be reused, refreshed, logged, persisted,
hashed for proof, or captured in fragments.

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
RETRY_ALLOWED=NO
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

PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_PERSISTED_ALLOWED=NO
PAYLOAD_PUBLISHED_ALLOWED=NO
PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
```

C4 payload may exist only in process memory for the minimum lifetime required
to construct At1ExecutionStore once against the existing designated path and to
complete constructor-level validation plus the required single connection close.
It must not be written into the SQLite file as raw key material beyond whatever
the existing constructor already persists as the non-secret
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
ALTERNATE_DB_PATH_ALLOWED=NO
CALLER_DB_PATH_OVERRIDE_ALLOWED=NO

EXPECTED_DESIGNATED_DB_STATE=PRESENT
EXPECTED_PRE_EXECUTION_DB_STATE=PRESENT

EXPECTED_SCHEMA_VERSION=1

EXPECTED_COMMITMENT_KEY_VERSION_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
```

Only the exact designated primary path may be opened as the durable
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
- operator-managed sidecar deletion or cleanup mutation;
- creation of the designated primary DB file.

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

### 8.2 Designated primary DB pre-existence check (must be PRESENT)

```text
PRE_EXECUTION_DB_CHECK=
  EXACT_DESIGNATED_PRIMARY_PATH_EXISTENCE_ONLY

REQUIRE_BEFORE_IMPERSONATION=
  DESIGNATED_DB_FILE_EXISTS=YES

IF_DESIGNATED_DB_FILE_ABSENT=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=DESIGNATED_SQLITE_MISSING_FOR_REVALIDATION
  STOP=YES
```

If the designated primary file is absent, the consumer must stop immediately
and return to governance. In that fail-closed stop the consumer must not:

- create the DB;
- delete, rename, truncate, or repair any path;
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

OTHER_DB_PATHS_ALLOWED=NO
OTHER_PRIMARY_DB_PATHS_ALLOWED=NO
SECOND_DURABLE_DATABASE_ALLOWED=NO
ALTERNATE_DATABASE_PATH_ALLOWED=NO

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
OPERATOR_CREATED_SIDECARS_ALLOWED=NO
OPERATOR_MANAGED_SIDECAR_DELETE_ALLOWED=NO
```

Exactly one At1ExecutionStore construction is permitted. That construction must
open the already-present designated primary path only. It must not create the
primary SQLite file. It may validate constructor-level metadata/schema checks
against the existing store.

Permitted validated immutable metadata values:

```text
schema_version=1

commitment_key_version_resource=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
```

Incidental SQLite-engine-managed transient sidecars in the same parent directory
remain permitted solely under §7.1 and do not count as a second durable database
or as a `DESIGNATED_SQLITE_CREATE`.

### 9.1 Connection-close lifecycle

```text
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
FINAL_STORE_CONNECTION_CLOSE_REQUIRED=YES

NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO
```

After successful existing-store construction and metadata validation, the R1B
revalidation execution consumer must deterministically close the single store
connection before the execution unit terminates.

Exactly one store connection-close event is required:

1. close of the single existing-store construction connection before unit
   termination.

Additional constructions, path changes, create/recreate loops, or reopen loops
are forbidden. This authorization does not authorize a new store-close API,
source-code change, or any `src/**` / `tests/**` modification. The consumer must
use the already existing connection lifecycle surface.

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

Any insert into `execution_claims`, `attempts`, `protocol_ledger`, or
`business_ledger` is forbidden. Constructor-level metadata validation against
the existing store is not a business/protocol event write.

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
  at1_execution_store_existing_construction_result|
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
  NW008_AT8W28_R1B_EXISTING_STORE_REVALIDATION_EXECUTION_001
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
- `STOP_CODE=DESIGNATED_SQLITE_MISSING_FOR_REVALIDATION`,

the authorization remains unconsumed (`AUTHORIZATION_CONSUMED=NO`) and no R1B
revalidation execution effects may proceed under this artifact until governance
disposition.

Before the first impersonation attempt, the execution consumer must
independently verify:

```text
PRE_EXECUTION_REQUIRED=
  EXACT_AUTHORIZATION_001_ARTIFACT_MERGED_TO_MAIN|
  EXACT_AUTHORIZATION_001_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_EXCEPTION_PROOF_MERGE_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_EXCEPTION_PROOF_PRESENT_ON_ORIGIN_MAIN|
  SOURCE_TECHNICAL_STORE_VALIDATION_PASS|
  SOURCE_GOVERNED_R1B_RESULT_AUTHORIZATION_BUDGET_EXCEEDED|
  SOURCE_R1B_GATE_COMPLETE_NO|
  SOURCE_R1B_AUTHORIZATION_CONSUMED_AND_NOT_REUSABLE|
  EXACT_TARGET_RUNTIME_PRINCIPAL_MATCH|
  EXACT_IDENTITY_MECHANISM_MATCH|
  EXACT_C4_RESOURCE_MATCH|
  EXACT_DESIGNATED_DB_PATH_MATCH|
  EXACT_DESIGNATED_DB_PARENT_MATCH|
  PARENT_DIRECTORY_EXISTS|
  PARENT_PATH_IS_DIRECTORY|
  DESIGNATED_DB_PRESENT|
  IDENTITY_SECRET_AND_STORE_EFFECT_BUDGETS_ENFORCED|
  BUSINESS_PROTOCOL_AND_RUNTIME_ZERO_BUDGETS_ENFORCED|
  STORE_CONNECTION_CLOSE_LIFECYCLE_ENFORCED|
  ZERO_DB_CREATE_ENFORCED|
  PAYLOAD_AND_TOKEN_NON_DISCLOSURE_ENFORCED
```

## 14. Success condition

R1B existing-store revalidation succeeds only if all of the following hold
within the fixed budgets and with zero forbidden effects or disclosures:

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=1

C4_READ_ATTEMPTS=1
C4_EXACT_SECRET_ACCESS=PASS

DESIGNATED_SQLITE_CREATED=NO
DESIGNATED_DB_PRE_EXECUTION_STATE=PRESENT

AT1_EXECUTION_STORE_EXISTING_CONSTRUCTION=PASS
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
principal, without resource or principal substitution. Existing-store
construction is PASS only when the existing At1ExecutionStore constructor
completes successfully at the exact designated primary path without creating
the primary file and validates `schema_version=1` plus the exact
commitment-key version resource string, with the required one connection-close
event completed using the existing lifecycle surface and without source-code or
new close-API changes.

## 15. Fail-closed behavior

If parent preflight, designated-DB preflight, impersonation, token mint, C4
read, existing-store construction, metadata validation, or required connection
close fails, the execution consumer must STOP.

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
DB_CREATE_ON_FAILURE=NO
DB_REPAIR_ON_FAILURE=NO
DB_DELETE_ON_FAILURE=NO
DB_RECREATE_ON_FAILURE=NO
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
FALL_BACK_TO_AT8W27_R1B_AUTHORIZATION_ON_FAILURE=NO
```

No retry. No second token. No second C4 read. No store repair. No DB delete. No
DB recreate. No HighLevel. No runtime assembly. No parent-path repair. No
operator sidecar deletion. No source-code or new close-API implementation under
this grant.

If failure occurs after the first impersonation attempt:

```text
AUTHORIZATION_STATE=CONSUMED
FAILURE_RESTORES_AUTHORITY=NO
```

Safe failure categories may identify non-sensitive classes such as
authentication unavailable, impersonation denied, permission denied, resource
not found, disabled version, dependency unavailable, designated parent not
ready, designated path missing for revalidation, schema/metadata mismatch,
connection-close failure, or sanitized transport/store failure. They must not
include payload, token, credential, header, or operator principal material.

## 16. Non-escalation

```text
R1B_RECOVERY_SUCCESS_AUTHORIZES_R2=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_R3=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_R4=NO

R1B_RECOVERY_SUCCESS_AUTHORIZES_HIGHLEVEL=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_CRM_MUTATION=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_RUNTIME_ASSEMBLY=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_PRODUCTION_RUNTIME=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_B2_READ=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_BUSINESS_EXECUTION=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_EXECUTION_CLAIMS=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_ATTEMPT_RECORDS=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_IAM_MUTATION=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_STANDING_TOKEN=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_DEPLOYMENT=NO

R1B_SUCCESS_AUTHORIZES_R2=NO
R1B_SUCCESS_AUTHORIZES_R3=NO
R1B_SUCCESS_AUTHORIZES_R4=NO
R1B_SUCCESS_AUTHORIZES_HIGHLEVEL=NO
R1B_SUCCESS_AUTHORIZES_CRM_MUTATION=NO
```

Every later runtime-validation or business-execution gate requires a separate,
explicit human-governed authorization.

## 17. Authoring pre-flight and zero-effect attestation

```text
PREFLIGHT_PWD=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=
  auth/nw008-at8w28-r1b-existing-store-revalidation-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_SHA=
  d002a0e145019696825decee0d6a14b6c716b7d9
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO

SOURCE_PR205_MERGED=YES
SOURCE_EXCEPTION_PROOF_ON_ORIGIN_MAIN=YES
SOURCE_TECHNICAL_STORE_VALIDATION=PASS
SOURCE_GOVERNED_R1B_RESULT=AUTHORIZATION_BUDGET_EXCEEDED
SOURCE_R1B_GATE_COMPLETE=NO
SOURCE_R1B_AUTHORIZATION_STATE=CONSUMED
SOURCE_R1B_AUTHORIZATION_REUSABLE=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=1
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
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
present at authoring time (`EXPECTED_DESIGNATED_DB_STATE=PRESENT`). That
observation is not execution, does not open SQLite, and does not consume this
authorization.

## 18. Review disposition

```text
R1B_EXISTING_STORE_REVALIDATION_DESIGNABLE=YES
R1B_EXISTING_STORE_REVALIDATION_EXECUTION_READY_AFTER_MERGE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=0
DESIGNATED_SQLITE_CREATE_MAX=0
AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=1
STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
HIGHLEVEL_CALLS_MAX=0
CRM_MUTATIONS_MAX=0
PRODUCTION_RUNTIME_ASSEMBLY_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO

R1B_RECOVERY_SUCCESS_AUTHORIZES_R2=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_R3=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_R4=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_HIGHLEVEL=NO
R1B_RECOVERY_SUCCESS_AUTHORIZES_CRM_MUTATION=NO

EXECUTION_PERFORMED=NO
SQLITE_OPENED=NO
SQLITE_CREATED=NO
SECRET_PAYLOAD_READS=0

NEXT=
  return authorization PR to ChatGPT for independent reviewer disposition
```
