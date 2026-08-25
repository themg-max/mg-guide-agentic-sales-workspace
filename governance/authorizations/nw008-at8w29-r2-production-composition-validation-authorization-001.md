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
  e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3

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
validation of the actual production root as repaired and durable on main via
merged PR #210. The future execution consumer may establish only whether:

1. the composition root can resolve source ADC solely as the impersonation
   source, construct exactly one short-lived target-runtime credential object
   for `mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`,
   and bind exactly one Secret Manager client to that credential object;
2. C4 and B2 both receive that same root-owned shared Secret Manager client;
3. a process-local synthetic/competition-safe issued verified capability can be
   precreated and accepted by `_validate_issued_capability()` /
   `_require_issued_verified_capability()`;
4. `assemble_bound_live_note_runtime(verified_capability=...)` can run exactly
   once and return a `NotePathAdapter` after:
   - verified capability validation;
   - DB path resolution from `MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH`;
   - root-owned source-ADC resolution and target-runtime credential construction;
   - one shared Secret Manager client construction;
   - exact C4 resolution through the shared client;
   - existing At1ExecutionStore construction at the designated path;
   - exact B2 credential resolution into `InjectedLiveNoteCredential` through the
     same shared client;
   - one `ConcreteLiveNoteHttpClient` construction;
   - one `BoundedLiveNoteTransport` construction;
   - one `NotePathAdapter` construction;
   - ownership transfer of the constructed store to the returned object graph;
   - return without invoking any adapter business method;
5. composition succeeds with zero HTTP request dispatch and zero CRM/business
   effects; and
6. the single store connection is closed exactly once according to the ownership
   model in section 10.1.

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

A successful R2 production-composition validation proves only that the repaired
production root can assemble once under the sealed target-runtime principal,
exact C4 and B2 numeric secret versions, the existing designated store, one
shared Secret Manager client, one HTTP client, and one bounded transport, while
remaining network-dormant and business-dormant. It does not authorize HighLevel
dispatch, CRM mutation, note write, stage transition, business execution,
execution claims, attempts, ledger writes, production runtime start, IAM
mutation, key creation, deployment, DB create/recreate/repair/delete, or any
later gate (R3/R4).

This grant does **not** revive, transfer, reuse, or extend:

- the consumed AT8W28 R1B revalidation authorization (PR #206); or
- the consumed R2 composition-root contract repair authorization (PR #209).

## 3. Durable source prerequisites, R1B completion, and PR #210 repair gate

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

COMPOSITION_ROOT_REPAIR_PR=210
COMPOSITION_ROOT_REPAIR_REVIEWED_HEAD=
  f31e490ca55499264a368d4efbc5ea75e37bce6d
COMPOSITION_ROOT_REPAIR_MERGE_COMMIT=
  e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3
COMPOSITION_ROOT_REPAIR_RECONCILIATION=PASS
COMPOSITION_ROOT_REPAIR_ON_ORIGIN_MAIN=YES

COMPOSITION_ROOT_REPAIR_AUTHORIZATION_PR=209
COMPOSITION_ROOT_REPAIR_AUTHORIZATION_STATE=CONSUMED
COMPOSITION_ROOT_REPAIR_AUTHORIZATION_REUSABLE=NO
COMPOSITION_ROOT_REPAIR_AUTHORIZATION_TRANSFERABLE=NO

IMPLEMENTATION_PROOF=
  proof/nw008/at-8w29/nw008-at8w29-r2-composition-root-contract-repair-implementation-proof-001.md
IMPLEMENTATION_PROOF_ON_ORIGIN_MAIN=YES

CREDENTIAL_OWNERSHIP_REPAIR_DURABLE=YES
TARGET_RUNTIME_SERVICE_ACCOUNT_SEALED=YES
TARGET_RUNTIME_SCOPES_SEALED=YES
TARGET_RUNTIME_CREDENTIAL_LIFETIME_SEALED=YES
SHARED_RUNTIME_CREDENTIAL_OBJECT_DURABLE=YES
SHARED_SECRET_MANAGER_CLIENT_DURABLE=YES
C4_AND_B2_SHARED_CLIENT_DURABLE=YES
STORE_LIFECYCLE_REPAIR_DURABLE=YES
POST_STORE_FAILURE_CLOSE_GUARANTEE_DURABLE=YES
SUCCESSFUL_STORE_OWNERSHIP_TRANSFER_DURABLE=YES

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

# Historical authoring note: pre-PR #210 drafts assumed SOURCE_CODE_CHANGE_REQUIRED=NO
# under a process-ADC client model. That model is SUPERSEDED by merged PR #210.
# The durable repaired root is now the sole production composition contract.
SOURCE_CODE_CHANGE_REQUIRED_FOR_R2_EXECUTION=NO
ADDITIONAL_SOURCE_CHANGE_AUTHORIZED_BY_THIS_GRANT=NO
```

PR #207 records governed R1B existing-store revalidation `RESULT=PASS` and
`R1B_GATE_COMPLETE=YES` under consumed PR #206. The designated store file is
therefore expected to be present.

PR #210 records the durable composition-root ownership repair under consumed
PR #209. This AT8W29 authorization is a fresh one-shot production-composition
grant only. It does not reopen, reuse, or extend the consumed AT8W28 R1B grant
or the consumed PR #209 repair grant.

## 4. Source-only production-composition preflight (authoring)

Source inspection on `origin/main` at
`e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3` resolved the repaired production root
without additional source changes under this authorization unit.

### 4.1 Assembly sequence evidence

`assemble_bound_live_note_runtime(*, verified_capability)` performs, in order:

```text
1. _validate_issued_capability(verified_capability)
     -> note_path._require_issued_verified_capability(...)
2. _resolve_root_owned_runtime_dependencies():
     a. db_path = os.environ["MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH"]
     b. source_credentials = _resolve_source_application_credentials()
        # source ADC is impersonation source only
     c. target_runtime_credentials =
          _impersonate_target_runtime_credentials(source_credentials)
        # one sealed target-runtime credential object
     d. secret_manager_client =
          _new_secret_manager_client(target_runtime_credentials)
        # one root-owned shared Secret Manager client
     e. GoogleSecretManagerLiveNoteSecretAccessor(
          client=secret_manager_client
        )
     f. RootOwnedLiveNoteCredentialInjection(
          accessor=...,
          resource_name=
            projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1
        )
     g. GoogleSecretManagerCommitmentKeyProvider(
          client=secret_manager_client
        ).resolve()  # exact C4 through shared client
     h. At1ExecutionStore(db_path=db_path, commitment_material=...)
3. store_ownership = _StoreOwnershipGuard(execution_store)
4. try:
     a. dependencies.credential_injection.build_provider().get_credential()
          -> InjectedLiveNoteCredential  # exact B2 read occurs here
     b. ConcreteLiveNoteHttpClient()
     c. BoundedLiveNoteTransport(
          bound_contact_id=...,
          credential=...,
          http_client=...
        )
     d. NotePathAdapter(...; execution_store=...)
     e. adapter._verified_contact_binding_capability = validated_capability
   except Exception:
     store_ownership.close_after_failed_assembly()
     raise
5. store_ownership.transfer_to_returned_adapter()
6. return adapter
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

### 4.2 Identity and client ownership preflight

```text
SOURCE_ADC_ROLE=
  IMPERSONATION_SOURCE_ONLY

TARGET_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

TARGET_RUNTIME_CREDENTIAL_OWNERSHIP=
  COMPOSITION_ROOT

TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS_MAX=1
TARGET_RUNTIME_SERVICE_ACCOUNT_SEALED=YES
TARGET_RUNTIME_SCOPES=
  https://www.googleapis.com/auth/cloud-platform
TARGET_RUNTIME_CREDENTIAL_LIFETIME_SECONDS=3600

SECRET_MANAGER_CLIENT_OWNERSHIP=
  COMPOSITION_ROOT
SECRET_MANAGER_CLIENT_INSTANTIATIONS_MAX=1
C4_AND_B2_USE_SAME_SECRET_MANAGER_CLIENT=YES

C4_CLIENT_BINDING=
  GoogleSecretManagerCommitmentKeyProvider(
    client=<root_owned_shared_secret_manager_client>
  )

B2_CLIENT_BINDING=
  GoogleSecretManagerLiveNoteSecretAccessor(
    client=<same_root_owned_shared_secret_manager_client>
  )

DIRECT_USER_ADC_SECRET_ACCESS=NO
CALLER_SUPPLIED_RUNTIME_PRINCIPAL=FORBIDDEN
CALLER_SUPPLIED_SECRET_MANAGER_CLIENT=FORBIDDEN
USER_MANAGED_SERVICE_ACCOUNT_KEY=FORBIDDEN
PROCESS_ADC_OVERRIDE_REQUIRED=NO
PROCESS_ADC_OVERRIDE_ALLOWED=NO
SERVICE_ACCOUNT_KEY_REQUIRED=NO
ADDITIONAL_SOURCE_CHANGE_AUTHORIZED_BY_THIS_GRANT=NO
```

Exact production ownership path (execution consumer, after merge):

1. precreate the synthetic verified capability and complete pre-execution
   filesystem checks;
2. invoke `assemble_bound_live_note_runtime` once;
3. allow the composition root itself to:
   - resolve source ADC only as the impersonation source;
   - construct exactly one short-lived target-runtime credential object for the
     sealed target runtime SA, sealed scopes, and lifetime 3600;
   - construct exactly one Secret Manager client with that credential object;
   - bind C4 and B2 to that same shared client;
4. forbid process-ADC override, installing impersonated credentials as process
   ADC, direct user-ADC Secret Manager access, caller-supplied runtime principal,
   caller-supplied Secret Manager client, user-managed service-account keys, and
   any principal other than the exact target runtime SA.

### 4.3 Historical / superseded process-ADC model

```text
HISTORICAL_PROCESS_ADC_MODEL=SUPERSEDED_BY_PR_210
HISTORICAL_C4_AND_B2_SEPARATE_DEFAULT_CLIENTS=SUPERSEDED_BY_PR_210
HISTORICAL_PROCESS_ADC_INJECTION_AS_PRODUCTION_CONTRACT=SUPERSEDED
CURRENT_PRODUCTION_CONTRACT=
  ROOT_OWNED_TARGET_RUNTIME_CREDENTIAL_PLUS_SHARED_SECRET_MANAGER_CLIENT
```

Any earlier draft language asserting that impersonated credentials are installed
as process ADC, that C4/B2 create separate default clients without
`credentials=`, or that process ADC identity propagation is the production
contract is historical evidence only and is not current execution authority.

### 4.4 Verified capability preflight

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

SOURCE_ADC_ROLE=
  IMPERSONATION_SOURCE_ONLY

SOURCE_PRINCIPAL_PRIVATE_ATTESTATION_REF=
  NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af

DO_NOT_PUBLISH_SOURCE_PRINCIPAL=YES
SOURCE_PRINCIPAL_PUBLICATION_ALLOWED=NO
SOURCE_PRINCIPAL_PERSISTENCE_ALLOWED=NO

IDENTITY_MECHANISM=
  COMPOSITION_ROOT_OWNED_SOURCE_ADC_PLUS_SHORT_LIVED_TARGET_RUNTIME_IMPERSONATION

CALLER_SUPPLIED_RUNTIME_IDENTITY_OVERRIDE=FORBIDDEN
CALLER_SUPPLIED_RUNTIME_PRINCIPAL=FORBIDDEN
CALLER_SUPPLIED_SECRET_MANAGER_CLIENT=FORBIDDEN
USER_MANAGED_SERVICE_ACCOUNT_KEY=FORBIDDEN
DIRECT_USER_ADC_AS_SECRET_ACCESS_PRINCIPAL=FORBIDDEN
PROCESS_ADC_OVERRIDE_REQUIRED=NO
PROCESS_ADC_OVERRIDE_ALLOWED=NO
```

The execution consumer must allow the composition root to authenticate Secret
Manager only as the exact target runtime service account, obtained solely through
one root-owned short-lived impersonated credential object constructed from the
operator source ADC. The consumer must not:

- publish or persist the operator principal identity;
- use a user-managed service-account key;
- use direct user ADC as the Secret Manager access principal;
- install or override process ADC for identity propagation;
- accept a caller-supplied runtime identity override or Secret Manager client; or
- impersonate any principal other than the exact target runtime SA above.

Proof may reference only the opaque attestation ref
`NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af` for the source principal
class, not the human operator email or other identifying material.

## 6. Identity effect budget

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1
TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS_MAX=1
SECRET_MANAGER_CLIENT_INSTANTIATIONS_MAX=1

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

Exactly one impersonation attempt, exactly one target-runtime credential object
construction, and exactly one short-lived access-token mint are permitted for
the exact target runtime SA. Credential-object construction is not equivalent to
token mint; R2 proof must record the actual token-mint/refresh count separately
from credential-object construction count.

The single root-owned credential object and single shared Secret Manager client
must cover both exact C4 and exact B2 Secret Manager reads performed during the
one authorized assembly. After R2 composition validation ends (success or
fail-closed stop), the token must not be reused, refreshed, logged, persisted,
hashed for proof, or captured in fragments.

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

### 9.4 Durable repair-gate check

```text
REQUIRE_BEFORE_IMPERSONATION=
  COMPOSITION_ROOT_REPAIR_PR_210_MERGED_TO_MAIN=YES
  COMPOSITION_ROOT_REPAIR_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES
  CREDENTIAL_OWNERSHIP_REPAIR_DURABLE=YES
  STORE_LIFECYCLE_REPAIR_DURABLE=YES
  IMPLEMENTATION_PROOF_PRESENT_ON_ORIGIN_MAIN=YES

IF_REPAIR_GATE_NOT_SATISFIED=
  AUTHORIZATION_CONSUMED=NO
  STOP_CODE=COMPOSITION_ROOT_REPAIR_NOT_DURABLE
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

### 10.1 Connection-close lifecycle and ownership transfer

```text
NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO
SECOND_CLOSE_ALLOWED=NO
TOTAL_STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
```

Ownership is case-split:

```text
FAILURE_BEFORE_STORE_CONSTRUCTION=
  STORE_CLOSE_EVENTS_REQUIRED=0
  NO_STORE_CLOSE_EXISTS_TO_PERFORM=YES

FAILURE_AFTER_STORE_CONSTRUCTION_BEFORE_ADAPTER_RETURN=
  IF_AT1_EXECUTION_STORE_CONSTRUCTED=YES
  AND_NOTE_PATH_ADAPTER_SUCCESSFULLY_RETURNED=NO
  THEN_STORE_CLOSE_OWNER=COMPOSITION_ROOT
  STORE_CLOSE_EVENTS_REQUIRED=1
  CONSUMER_CLEANUP_MUTATION_REQUIRED=NO

SUCCESSFUL_ASSEMBLY=
  IF_NOTE_PATH_ADAPTER_SUCCESSFULLY_RETURNED=YES
  THEN_STORE_OWNERSHIP_TRANSFERRED_TO_RETURNED_OBJECT_GRAPH=YES
  R2_CONSUMER_FINAL_STORE_CLOSE_REQUIRED=YES
  STORE_CLOSE_EVENTS_REQUIRED=1
```

On successful assembly and composition validation, the R2 execution consumer must
deterministically close only the successfully transferred store connection before
the execution unit terminates, using the already existing connection lifecycle
surface (`store._connection.close()` or equivalent existing surface reachable
from the assembled object graph), without invoking adapter business methods.

On failure after store construction but before adapter return, the production
composition root must close exactly once automatically. No consumer cleanup
mutation is required after that root-owned failure close.

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
  target_runtime_credential_object_construction_count|
  secret_manager_client_instantiation_count|
  c4_and_b2_shared_client_bound|
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
  store_ownership_transferred|
  highlevel_http_client_instantiation_count|
  highlevel_transport_instantiation_count|
  note_path_adapter_assembly_count|
  http_request_dispatch_count|
  final_store_connection_close_result|
  store_connection_close_event_count|
  store_close_owner|
  schema_version_validated|
  commitment_key_version_resource_validated|
  composition_root_repair_pr|
  composition_root_repair_merge_commit|
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
This normalization unit does not consume the grant.

Exception: if a pre-execution filesystem, capability, or repair-gate check fails
closed before any impersonation attempt with

- `STOP_CODE=DESIGNATED_SQLITE_PARENT_NOT_READY`,
- `STOP_CODE=DESIGNATED_SQLITE_MISSING_FOR_R2_COMPOSITION`,
- `STOP_CODE=R2_VERIFIED_CAPABILITY_UNRESOLVED`, or
- `STOP_CODE=COMPOSITION_ROOT_REPAIR_NOT_DURABLE`,

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
  COMPOSITION_ROOT_REPAIR_PR_210_MERGED_TO_MAIN|
  COMPOSITION_ROOT_REPAIR_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  COMPOSITION_ROOT_REPAIR_AUTHORIZATION_209_CONSUMED_AND_NOT_REUSABLE|
  CREDENTIAL_OWNERSHIP_REPAIR_DURABLE|
  STORE_LIFECYCLE_REPAIR_DURABLE|
  IMPLEMENTATION_PROOF_PRESENT_ON_ORIGIN_MAIN|
  PRODUCTION_RUNTIME_ENTRYPOINT_RESOLVED|
  ROOT_OWNED_TARGET_RUNTIME_CREDENTIAL_MODEL|
  SHARED_SECRET_MANAGER_CLIENT_MODEL|
  C4_AND_B2_USE_SAME_SECRET_MANAGER_CLIENT|
  PROCESS_ADC_OVERRIDE_FORBIDDEN|
  R2_VERIFIED_CAPABILITY_SOURCE_RESOLVED|
  R2_VERIFIED_CAPABILITY_SYNTHETIC_OR_COMPETITION_SAFE|
  EXACT_TARGET_RUNTIME_PRINCIPAL_MATCH|
  EXACT_TARGET_RUNTIME_SCOPES_MATCH|
  EXACT_TARGET_RUNTIME_CREDENTIAL_LIFETIME_MATCH|
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
  STORE_OWNERSHIP_AND_CLOSE_LIFECYCLE_ENFORCED|
  ZERO_DB_CREATE_ENFORCED|
  PAYLOAD_AND_TOKEN_NON_DISCLOSURE_ENFORCED
```

## 14. Success condition

R2 production-composition validation succeeds only if all of the following hold
within the fixed budgets and with zero forbidden effects or disclosures:

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=1

TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS=1
TARGET_RUNTIME_SERVICE_ACCOUNT_MATCH=YES
TARGET_RUNTIME_SCOPES_MATCH=YES
TARGET_RUNTIME_CREDENTIAL_LIFETIME_MATCH=YES

SECRET_MANAGER_CLIENT_INSTANTIATIONS=1
C4_PROVIDER_SHARED_CLIENT_BOUND=YES
B2_ACCESSOR_SHARED_CLIENT_BOUND=YES
C4_AND_B2_USE_SAME_SECRET_MANAGER_CLIENT=YES

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

STORE_OWNERSHIP_TRANSFERRED=YES
FINAL_STORE_CONNECTION_CLOSE=PASS
STORE_CONNECTION_CLOSE_EVENTS=1
R2_CONSUMER_FINAL_STORE_CLOSE=PASS

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
exact requested numeric-version resource under the root-owned target-runtime
credential and shared client, without resource or principal substitution.
Production assembly is PASS only when `assemble_bound_live_note_runtime` returns
a `NotePathAdapter` after the full composition sequence above, with existing-
store construction at the exact designated primary path, without creating the
primary file, without HTTP dispatch, and without CRM/business method invocation,
followed by ownership transfer and the required one consumer connection-close
event.

## 15. Fail-closed behavior

If parent preflight, designated-DB preflight, capability precreation, repair-gate
preflight, impersonation, token mint, C4 read, B2 read, existing-store
construction, metadata validation, production assembly, composition binding
checks, ownership transfer, or required connection close fails, the execution
consumer must STOP.

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
FALL_BACK_TO_PROCESS_ADC_OVERRIDE_ON_FAILURE=NO
FALL_BACK_TO_AT8W28_R1B_AUTHORIZATION_ON_FAILURE=NO
FALL_BACK_TO_PR209_REPAIR_AUTHORIZATION_ON_FAILURE=NO
ESCALATE_TO_R3_ON_FAILURE=NO
ESCALATE_TO_R4_ON_FAILURE=NO
```

Normalized close ownership on failure:

```text
IF_FAILURE_BEFORE_STORE_CONSTRUCTION=
  STORE_CLOSE_EVENTS=0

IF_FAILURE_AFTER_STORE_CONSTRUCTION_BEFORE_ADAPTER_RETURN=
  COMPOSITION_ROOT_CLOSES_STORE_EXACTLY_ONCE=YES
  CONSUMER_CLOSE_REQUIRED=NO

IF_FAILURE_AFTER_SUCCESSFUL_ADAPTER_RETURN=
  R2_CONSUMER_OWNS_RETURNED_STORE=YES
  R2_CONSUMER_MUST_CLOSE_EXACTLY_ONCE_BEFORE_EXIT=YES
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
repair gate not durable, schema/metadata mismatch, assembly failure,
connection-close failure, or sanitized transport/store failure. They must not
include payload, token, credential, header, or operator principal material.

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
  e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=
  proof/nw008/at-10/** excluded and unstaged only

R1B_PROOF_PR=207
R1B_PROOF_MERGE_COMMIT=
  f5ec221a667db91e43684f3acad98913b6e00bfa
R1B_RESULT=PASS
R1B_GATE_COMPLETE=YES
R1B_AUTHORIZATION_STATE=CONSUMED
R1B_AUTHORIZATION_REUSABLE=NO

COMPOSITION_ROOT_REPAIR_PR=210
COMPOSITION_ROOT_REPAIR_MERGE_COMMIT=
  e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3
COMPOSITION_ROOT_REPAIR_RECONCILIATION=PASS
CREDENTIAL_OWNERSHIP_REPAIR_DURABLE=YES
STORE_LIFECYCLE_REPAIR_DURABLE=YES
COMPOSITION_ROOT_REPAIR_AUTHORIZATION_STATE=CONSUMED

PRODUCTION_RUNTIME_ENTRYPOINT_RESOLVED=YES
ROOT_OWNED_TARGET_RUNTIME_CREDENTIAL_MODEL=YES
SHARED_SECRET_MANAGER_CLIENT_MODEL=YES
C4_AND_B2_USE_SAME_SECRET_MANAGER_CLIENT=YES
PROCESS_ADC_MODEL_REMOVED=YES
DIRECT_USER_ADC_SECRET_ACCESS=NO
R2_VERIFIED_CAPABILITY_SOURCE_RESOLVED=YES
R2_VERIFIED_CAPABILITY_SYNTHETIC_OR_COMPETITION_SAFE=YES
ASSEMBLY_HTTP_DISPATCH_BY_ITSELF=NO
ASSEMBLY_CRM_MUTATION_BY_ITSELF=NO
R2_AUTHORIZATION_DESIGNABLE=YES
ADDITIONAL_SOURCE_CHANGE_AUTHORIZED_BY_THIS_GRANT=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=0
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
R2_EXECUTION_PERFORMED=NO
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
and the durable PR #210 repair proof. That observation is not execution, does
not open SQLite, does not read secrets, does not assemble runtime, and does not
consume this authorization.

## 18. Review disposition

```text
R2_PRODUCTION_COMPOSITION_VALIDATION_DESIGNABLE=YES
R2_PRODUCTION_COMPOSITION_VALIDATION_EXECUTION_READY_AFTER_MERGE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1
TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS_MAX=1
SECRET_MANAGER_CLIENT_INSTANTIATIONS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
B2_SECRET_READ_ATTEMPTS_MAX=1
DESIGNATED_SQLITE_CREATE_MAX=0
AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX=1
PRODUCTION_RUNTIME_ASSEMBLY_MAX=1
HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS_MAX=1
HIGHLEVEL_TRANSPORT_INSTANTIATIONS_MAX=1
NOTE_PATH_ADAPTER_ASSEMBLIES_MAX=1
STORE_FAILURE_CLOSE_OWNER=COMPOSITION_ROOT
STORE_SUCCESS_OWNERSHIP_TRANSFER=YES
R2_CONSUMER_FINAL_STORE_CLOSE_REQUIRED=YES
TOTAL_STORE_CONNECTION_CLOSE_EVENTS_REQUIRED=1
HIGHLEVEL_CALLS_MAX=0
HTTP_REQUEST_DISPATCHES_MAX=0
CRM_MUTATIONS_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0

SQLITE_ENGINE_MANAGED_TRANSIENT_SIDECARS_ALLOWED=YES
NEW_STORE_CLOSE_API_IMPLEMENTATION_AUTHORIZED=NO
SOURCE_CODE_CHANGE_AUTHORIZED=NO

PR210_REPAIR_BOUND=YES
PR210_MERGE_COMMIT=
  e127b3d2723e58ff1a91e5ab3ff94bf170e6dfd3
PROCESS_ADC_MODEL_REMOVED=YES
ROOT_OWNED_TARGET_CREDENTIAL_MODEL=YES
SHARED_SECRET_MANAGER_CLIENT_MODEL=YES

R2_SUCCESS_AUTHORIZES_R3=NO
R2_SUCCESS_AUTHORIZES_R4=NO
R2_SUCCESS_AUTHORIZES_HIGHLEVEL_DISPATCH=NO
R2_SUCCESS_AUTHORIZES_CRM_MUTATION=NO

EXECUTION_PERFORMED=NO
R2_EXECUTION_PERFORMED=NO
SQLITE_OPENED=NO
SQLITE_CREATED=NO
SECRET_PAYLOAD_READS=0
PRODUCTION_RUNTIME_ASSEMBLY=0

NEXT=
  return normalized authorization PR to ChatGPT for independent reviewer disposition
```
