# NW-008 AT-8M2 — Offline Execution Store Substrate Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

PLANNING_IDENTIFIER=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001.md
AUTHORIZATION_BRANCH=nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001

PREDECESSOR_PR=123
PR123_STATE=MERGED
PR123_REVIEWED_HEAD=ab1c8f1ac072519e86e9b3390cc256eb13c9ab19
PR123_REVIEWED_HEAD_MATCH=YES
PR123_MERGE_SHA=b602318e130b8d5cd04c7669c6fc4d9697a7dff3
PR123_MERGE_VERIFIED_ON_ORIGIN_MAIN=YES
PR123_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES
PR123_MERGE_SHA_REACHABLE_FROM_MAIN=YES

SOURCE_AT8M_ARTIFACT=docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001.md
SOURCE_AT8M_BLOB_SHA=1f5b2c123a49c56427bfef6e78f55fe60c4fc04a
SOURCE_AT8M1_ARTIFACT=docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md
SOURCE_AT8M1_BLOB_SHA=4fc58b65fbec9324fae47788db34985ffb1145b2

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE

GRANT=OFFLINE_DETERMINISTIC_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
AUTHORIZATION_EFFECTIVE=NO
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_PATH=proof/nw008/at-8m2/nw008-at8m2-offline-execution-store-substrate-implementation-consumption-001.md

MODE_GRANT_ALIAS=OFFLINE_DETERMINISTIC_IMPLEMENTATION_GRANT
IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does **not** implement store schema versioning, does not create
`at1_commitment_key_provider.py`, does not modify tests, does not read secret
payload, does not call HighLevel, does not mutate CRM, does not change IAM/GCP,
does not deploy, and does not authorize live mutation or live production store
activation.

AT8M2 itself is `AUTHORIZATION_ARTIFACT_ONLY`. It authorizes a later offline
deterministic implementation consumer after independent human review and merge.
It must not implement anything in this authorization PR.

### Conditional grant semantics

```text
GRANT=OFFLINE_DETERMINISTIC_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the
artifact defines a bounded one-shot offline implementation permission that
becomes usable only when both of the following are true:

1. the exact authorization artifact path is present on `main` via human review
   and merge; and
2. the authorized consumer unit
   `NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001`
   verifies that merge (exact path on `origin/main` / merge ancestry) before
   writing any authorized consumer path.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is not standing implementation authority, not live-mutation
authority, not real Secret Manager authority, not commitment-key live-read
authority, not IAM authority, not HighLevel authority, not CRM mutation
authority, not deployment authority, not production runtime activation
authority, and not a reusable grant.

The sole authorized consumer is
`NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001`.
No other unit may consume this grant.

The implementation consumer must record one-shot consumption in
`proof/nw008/at-8m2/nw008-at8m2-offline-execution-store-substrate-implementation-consumption-001.md`.
It must not modify this authorization artifact.

```text
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

## 2. Predecessor merge verification (PR123)

Verified before authoring this artifact:

```text
PR123_MERGED=YES
PR123_STATE=MERGED
PR123_MERGED_AT=2026-08-21T22:43:24Z
PR123_TITLE=docs(nw008): AT8M1 execution-store schema and key-versioning design
PR123_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/123
PR123_REVIEWED_HEAD=ab1c8f1ac072519e86e9b3390cc256eb13c9ab19
PR123_HEAD_REF_OID_AT_MERGE=ab1c8f1ac072519e86e9b3390cc256eb13c9ab19
PR123_REVIEWED_HEAD_MATCH=YES
PR123_MERGE_SHA=b602318e130b8d5cd04c7669c6fc4d9697a7dff3
PR123_MERGE_SHA_REACHABLE_FROM_MAIN=YES
PR123_MERGE_SUBJECT=Merge pull request #123 from themg-max/nw008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001
ORIGIN_MAIN_SHA_AT_AUTHORING=b602318e130b8d5cd04c7669c6fc4d9697a7dff3
AT8M1_ARTIFACT_ON_MAIN=YES
AT8M1_ARTIFACT_PATH=docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md
AT8M1_ARTIFACT_BLOB_SHA=4fc58b65fbec9324fae47788db34985ffb1145b2
AT8M_ARTIFACT_ON_MAIN=YES
AT8M_ARTIFACT_PATH=docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001.md
AT8M_ARTIFACT_BLOB_SHA=1f5b2c123a49c56427bfef6e78f55fe60c4fc04a
```

Verification commands used (read-only):

```text
gh pr view 123 --repo themg-max/mg-guide-agentic-sales-workspace \
  --json state,mergedAt,mergeCommit,headRefOid,title,url
# state=MERGED
# headRefOid=ab1c8f1ac072519e86e9b3390cc256eb13c9ab19
# mergeCommit.oid=b602318e130b8d5cd04c7669c6fc4d9697a7dff3

git fetch origin main
git rev-parse origin/main
# b602318e130b8d5cd04c7669c6fc4d9697a7dff3

git merge-base --is-ancestor \
  ab1c8f1ac072519e86e9b3390cc256eb13c9ab19 \
  origin/main
# exit 0

git cat-file -e \
  origin/main:docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md
# exit 0

git rev-parse \
  origin/main:docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md
# 4fc58b65fbec9324fae47788db34985ffb1145b2
```

PR123 closed AT8M1 store-internal architecture decisions. This authorization
does not reopen AT8M host-class, identity-mechanism, production DB-path policy,
or live-activation decisions. It consumes only the offline-designable store
substrate surface frozen by AT8M1.

## 3. Pre-flight (authorization authoring)

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_REF=origin/main
PREFLIGHT_BASE_SHA=b602318e130b8d5cd04c7669c6fc4d9697a7dff3
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_UNTRACKED_FILES_BEFORE_ARTIFACT=0
PREFLIGHT_RECORDED_AT_LOCAL=2026-08-21T18:45:29-0400
PREFLIGHT_RECORDED_AT_UTC=2026-08-21T22:45:29Z
```

Abort conditions did not fire: branch is not `main`; worktree had no unrelated
changes before artifact creation.

## 4. Fresh main consumer inventory re-inspection

```text
AT1_EXECUTION_STORE_SOURCE_CONSUMERS_REINSPECTED=YES
AT1_EXECUTION_STORE_TEST_CONSUMERS_REINSPECTED=YES
INVENTORY_BASE=origin/main@b602318e130b8d5cd04c7669c6fc4d9697a7dff3
INVENTORY_METHOD=git grep At1ExecutionStore( and At1ExecutionStore on origin/main
NEW_CONSUMERS_SINCE_AT8M1=0
```

### 4.1 Source references on main (read-only)

```text
SRC_CLASS_DEFINITION=
  src/integrations/ghl/at1_execution_store.py
  (class At1ExecutionStore)

SRC_TYPE_OR_IMPORT_REFERENCES_NOT_CONSTRUCTING_WITH_NEW_API_OWNERS=
  src/integrations/ghl/__init__.py
  src/integrations/ghl/at1_live_transport_adapter.py
  src/integrations/ghl/highlevel_rest/live_note_runtime.py
  src/integrations/ghl/highlevel_rest/live_note_transport.py
  src/integrations/ghl/highlevel_rest/note_path.py
```

Source modules other than `at1_execution_store.py` reference the store type for
typing/import/composition boundaries. They are **not** authorized writable paths
under this grant. Composition-root production store construction remains out of
scope (AT8M / AT8L separation preserved).

### 4.2 Deterministic construction consumers on main

Direct `At1ExecutionStore(...)` construction sites remain exactly the AT8M1
frozen set:

```text
CONSTRUCTION_TEST_FILES=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

Non-construction test reference (not a constructor consumer; not writable under
this grant solely by reference):

```text
NON_CONSTRUCTION_TEST_REFERENCE=
  tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py
```

### 4.3 Delta since AT8M1

```text
AT8M1_FROZEN_CONSTRUCTION_TEST_FILES=4
CURRENT_CONSTRUCTION_TEST_FILES=4
NEW_CONSTRUCTION_TEST_FILES=0
NEW_SRC_CONSTRUCTOR_CALL_SITES=0
NEW_CONSUMERS_SINCE_AT8M1=0
```

No new consumers appeared on main after PR123. Writable consumer scope may
proceed from the AT8M1 freeze plus the explicit new provider module/test path
authorized below.

If a future pre-implementation re-inspection finds `NEW_CONSUMERS_SINCE_AT8M1>0`,
the consumer must STOP and obtain scope amendment before writing code.

## 5. Durable AT8M1 fields consumed by this grant

Only durable fields from merged AT8M1 / AT8M on `origin/main` are treated as
design origin. This authorization freezes implementation grant boundaries; it
does not reopen AT8M live blockers.

```text
COMMITMENT_KEY_VERSIONING_MODEL=PIN_STORE_TO_EXACT_SECRET_VERSION
STORE_COMMITMENT_KEY_VERSION_IMMUTABLE_AFTER_INITIALIZATION=YES
SILENT_COMMITMENT_KEY_ROTATION=FORBIDDEN
PER_RECORD_KEY_VERSION_COLUMN_REQUIRED=NO
COMMITMENT_KEY_VERSION_RESOURCE_MUST_BE_EXACT_VERSION=YES
COMMITMENT_KEY_VERSION_ALIAS_ALLOWED=NO
COMMITMENT_KEY_VERSION_LATEST_ALLOWED=NO
COMMITMENT_KEY_PAYLOAD_STORED_IN_DB=NO

STORE_SCHEMA_VERSIONING_SCOPE_RESOLVED=YES
STORE_SCHEMA_VERSIONING_OWNER=At1ExecutionStore
STORE_SCHEMA_VERSIONING_REQUIRED=YES
INITIAL_STORE_SCHEMA_VERSION=1
LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
FORWARD_ONLY_SCHEMA_MIGRATIONS=YES
UNKNOWN_NEWER_SCHEMA_VERSION=FAIL_CLOSED
MISSING_OR_INVALID_SCHEMA_METADATA=FAIL_CLOSED
NEW_STORE_INITIALIZATION_ATOMIC=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
COMMITMENT_KEY_VERSION_RESOURCE_METADATA_MUTABLE=NO
SCHEMA_VERSION_METADATA_MUTABLE=FORWARD_ONLY_MIGRATION

COMMITMENT_KEY_USES_LIVE_NOTE_SECRET_ACCESSOR=NO
COMMITMENT_KEY_PROVIDER_INTERFACE_REQUIRED=YES
COMMITMENT_KEY_PROVIDER_PUBLIC_PURPOSE=EXECUTION_STORE_COMMITMENT_KEY_ONLY
OFFLINE_IMPLEMENTATION_SYNTHETIC_PROVIDER_ALLOWED=YES
REAL_SECRET_MANAGER_COMMITMENT_KEY_PROVIDER_AUTHORIZED=NO
REAL_COMMITMENT_KEY_READ_AUTHORIZED=NO
COMMITMENT_KEY_AND_VERSION_RESOURCE_SAME_PROVIDER_RESULT=YES
INDEPENDENT_KEY_AND_VERSION_CALLER_INPUTS=FORBIDDEN

OFFLINE_STORE_SUBSTRATE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO

PRODUCTION_RUNTIME_READY=NO
LIVE_CREDENTIAL_USE_READY=NO
LIVE_HIGHLEVEL_EXECUTION_READY=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## 6. Frozen implementation mode (normative)

```text
IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS
MODE=OFFLINE_DETERMINISTIC_IMPLEMENTATION_GRANT

REAL_SECRET_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_PAYLOAD_READS_DURING_IMPLEMENTATION=0
REAL_SECRET_PAYLOAD_READS=0
REAL_COMMITMENT_KEY_READS=0

REAL_SECRET_MANAGER_ACCESS=FORBIDDEN
REAL_SECRET_MANAGER_PROVIDER_IMPLEMENTATION_AUTHORIZED=NO
SYNTHETIC_PROVIDER_IMPLEMENTATION_AUTHORIZED=YES

REAL_CREDENTIAL_USE=NO
TOKEN_VALUE_EXPOSURE=NO

LIVE_NETWORK_CALLS=0
HIGHLEVEL_CALLS=FORBIDDEN
CRM_MUTATIONS=FORBIDDEN

GCP_MUTATIONS=0
IAM_CHANGE=NO
SECRET_CREATE=FORBIDDEN
SECRET_CREATION=FORBIDDEN
SECRET_IAM=FORBIDDEN
SECRET_POLICY_CHANGE=NO
DEPLOYMENT=FORBIDDEN
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_CHANGE=NO
RUNTIME_SA_IMPERSONATION=NO
SERVICE_ACCOUNT_ATTACHMENT=NO
SERVICE_ACCOUNT_KEY_CREATE=NO
SERVICE_ACCOUNT_KEY_DOWNLOAD=NO

LIVE_TRANSPORT_EXECUTION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_NOTE_READ_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZATION_CREATION_AUTHORIZED=NO
LIVE_RUNTIME_ACTIVATION_AUTHORIZED=NO
LIVE_PRODUCTION_STORE_ACTIVATION=FORBIDDEN
PRODUCTION_STORE_CONSTRUCTION_ACTIVATION_AUTHORIZED=NO
PRODUCTION_COMPOSITION_ROOT_STORE_WIRING=FORBIDDEN

LIVE_NOTE_SECRET_ACCESSOR_REUSE_FOR_COMMITMENT_KEY=FORBIDDEN
PR120_AUTHORITY_REUSE=FORBIDDEN
AT8K2_AUTHORITY_REUSE=FORBIDDEN

DEPENDENCY_CHANGES_AUTHORIZED=NO
PACKAGE_MANIFEST_CHANGES_AUTHORIZED=NO
NEW_HTTP_LIBRARY_DEPENDENCY_AUTHORIZED=NO
NEW_SECRET_MANAGER_LIBRARY_DEPENDENCY_AUTHORIZED=NO

EXTERNAL_EFFECTS_ALLOWED=0
EXTERNAL_EFFECTS=0
```

## 7. Authoring vs consumer writable scope (normative)

These scopes are disjoint. Authorization authoring must not write consumer
implementation files. The implementation consumer must not rewrite this
authorization artifact. Consumption is recorded only in the consumption record
path.

```text
AUTHORIZATION_PR_WRITABLE_SCOPE=
governance/authorizations/nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001.md

AUTHORIZED_CONSUMER_UNIT=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001
```

### 7.1 Authorization PR writable scope

```text
governance/authorizations/nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001.md
```

No other path is writable in this authorization PR.

AT8M2 must not implement anything in this PR.

### 7.2 Authorized consumer writable scope (future only; exact freeze)

Exact future consumer writable paths, reserved for
`NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001` after this
artifact is merged and independently verified:

#### Authorized source paths

```text
AUTHORIZED_SOURCE_PATHS=
  src/integrations/ghl/at1_execution_store.py
  src/integrations/ghl/at1_commitment_key_provider.py
```

#### Authorized test paths

```text
AUTHORIZED_TEST_PATHS=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
  tests/integrations/ghl/test_at1_commitment_key_provider.py
```

Notes:

- The first four test paths are the AT8M1-frozen construction consumers and
  **must** move to the canonical provenance-bound material construction path.
  No raw-key-only constructor retention and no test-only compat seam are
  authorized.
- `tests/integrations/ghl/test_at1_commitment_key_provider.py` is authorized as a
  **new** deterministic provider-focused test module (create-or-extend within
  that exact path only).

#### Authorized proof/doc paths

```text
AUTHORIZED_PROOF_PATHS=
  proof/nw008/at-8m2/**

AUTHORIZED_DOC_PATH_EXACT=
  docs/nw008/nw-008-at8m2-offline-execution-store-substrate-implementation-001.md
```

Multiple proof files under `proof/nw008/at-8m2/**` are allowed because
deterministic implementation proof may require more than one proof artifact.
The documentation path is exact (no broad `nw-008-at8m2-*` glob).

Required consumption record path (under proof glob):

```text
proof/nw008/at-8m2/nw008-at8m2-offline-execution-store-substrate-implementation-consumption-001.md
```

#### Combined exact consumer writable freeze

```text
AT8M2_CONSUMER_WRITABLE_SCOPE_EXACT=
  src/integrations/ghl/at1_execution_store.py
  src/integrations/ghl/at1_commitment_key_provider.py
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
  tests/integrations/ghl/test_at1_commitment_key_provider.py
  proof/nw008/at-8m2/**
  docs/nw008/nw-008-at8m2-offline-execution-store-substrate-implementation-001.md
```

No other path is writable by the consumer under this grant.

### 7.3 Authorized consumer optional paths

```text
AUTHORIZED_CONSUMER_OPTIONAL_PATHS=
  (none)
```

```text
PACKAGE_EXPORT_CHANGE_REQUIRED=NO
PACKAGE_EXPORT_CHANGE_OPTIONAL=NO
SRC_INTEGRATIONS_GHL_INIT_WRITABLE=NO
```

Package export of the new provider is not required and not authorized in this
unit. Consumers may import the provider module by explicit module path in tests
and store construction code within authorized source paths.

### 7.4 Authorized consumer blocked paths

```text
src/integrations/ghl/highlevel_rest/live_note_runtime.py=BLOCKED
src/integrations/ghl/highlevel_rest/live_note_transport.py=BLOCKED
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py=BLOCKED
src/integrations/ghl/highlevel_rest/live_note_http_client.py=BLOCKED
src/integrations/ghl/highlevel_rest/note_path.py=BLOCKED
src/integrations/ghl/highlevel_rest/fake_transport.py=BLOCKED
src/integrations/ghl/highlevel_rest/__init__.py=BLOCKED

src/integrations/ghl/__init__.py=BLOCKED
src/integrations/ghl/at1_live_transport_adapter.py=BLOCKED
src/integrations/ghl/at1_live_transport_serializer.py=BLOCKED
src/integrations/ghl/bounded_at1_executor.py=BLOCKED
src/integrations/ghl/read_adapter.py=BLOCKED

tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py=BLOCKED

src/orchestration/**=BLOCKED
src/agents/**=BLOCKED
src/mg_guide/**=BLOCKED
workspace_addon/**=BLOCKED
contracts/**=BLOCKED
fixtures/**=BLOCKED
.github/**=BLOCKED
scripts/**=BLOCKED
local/**=BLOCKED

requirements.txt=BLOCKED
pyproject.toml=BLOCKED
Dockerfile=BLOCKED
.env.example=BLOCKED

competition/NEW_WORK_LEDGER.md=BLOCKED
docs/COMPETITION_BASELINE.md=BLOCKED

proof/nw008/at-8k2/**=BLOCKED
proof/nw008/at-8l/**=BLOCKED
proof/nw008/at-8i/**=BLOCKED
proof/nw008/at-8h/**=BLOCKED
proof/nw008/at-8g/**=BLOCKED
docs/nw008/nw-008-at8m-*=BLOCKED_EXCEPT_READ
docs/nw008/nw-008-at8m1-*=BLOCKED_EXCEPT_READ
docs/nw008/nw-008-at8m2-*=BLOCKED_EXCEPT_EXACT_AUTHORIZED_DOC_PATH
governance/authorizations/**=BLOCKED_EXCEPT_THIS_ARTIFACT_ALREADY_MERGED
```

Also blocked surfaces (non-path class):

```text
IAM_GCP_MUTATION_SURFACES=BLOCKED
SECRET_PAYLOAD_ACCESS=BLOCKED
REAL_COMMITMENT_KEY_SECRET_ACCESS=BLOCKED
MG_GUIDE_PIT_GHL_VERSIONS_ACCESS=BLOCKED
RUNTIME_SA_IMPERSONATION=BLOCKED
SERVICE_ACCOUNT_ATTACHMENT=BLOCKED
SERVICE_ACCOUNT_KEYS=BLOCKED
HIGHLEVEL_LIVE_CALLS=BLOCKED
CRM_LIVE_MUTATIONS=BLOCKED
DEPLOYMENT_PRODUCTION_PLATFORM_BIND=BLOCKED
LIVE_MUTATION_AUTHORIZATION_ARTIFACTS=BLOCKED
PACKAGE_MANIFESTS=BLOCKED
LIVE_NOTE_SECRET_ACCESSOR_REUSE=BLOCKED
PR120_AUTHORITY_SURFACE=BLOCKED
AT8K2_AUTHORITY_SURFACE=BLOCKED
PRODUCTION_COMPOSITION_ROOT_STORE_WIRING=BLOCKED
LIVE_PRODUCTION_STORE_ACTIVATION=BLOCKED
```

## 8. Freeze provider contract (normative)

```text
PROVIDER_SCOPE=EXECUTION_STORE_COMMITMENT_KEY_ONLY
PROVIDER_MODULE=src/integrations/ghl/at1_commitment_key_provider.py

PROVIDER_RESULT_BINDS_PAYLOAD_AND_VERSION_RESOURCE=YES
PROVIDER_RESULT_IS_PROVENANCE_AUTHORITY=YES
INDEPENDENT_KEY_AND_VERSION_INPUTS=FORBIDDEN

PROVIDER_RESOLUTION_OCCURS_OUTSIDE_STORE=YES
STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
STORE_ACCEPTS_PROVENANCE_BOUND_MATERIAL=YES

VERSION_RESOURCE_MUST_MATCH=
projects/<project>/secrets/<secret>/versions/<numeric-version>

NUMERIC_VERSION_MUST_BE_POSITIVE_INTEGER=YES
LATEST_ALLOWED=NO
ALIASES_ALLOWED=NO
QUERY_STRING_ALLOWED=NO
FRAGMENT_ALLOWED=NO
WHITESPACE_ALLOWED=NO

SYNTHETIC_PROVIDER_IMPLEMENTATION_AUTHORIZED=YES
REAL_SECRET_MANAGER_PROVIDER_IMPLEMENTATION_AUTHORIZED=NO

COMMITMENT_KEY_USES_LIVE_NOTE_SECRET_ACCESSOR=NO
LIVE_NOTE_SECRET_ACCESSOR_REUSE=FORBIDDEN
```

### 8.1 Provider purpose and module placement

The commitment-key provider is purpose-limited to execution-store commitment-key
delivery only. It must not become a general secret accessor, must not serve GHL
PIT credentials, and must not wrap or call `LiveNoteSecretAccessor`.

Exact public symbol names inside
`src/integrations/ghl/at1_commitment_key_provider.py` are an implementation
detail of the consumer, subject to the contracts frozen here.

### 8.2 Provenance-bound provider result and store boundary

The provider must return **one** logical material object / result that binds
together:

1. commitment-key payload bytes/string material; and
2. exact pinned commitment-key version resource identity.

```text
PROVIDER_RESULT_BINDS_PAYLOAD_AND_VERSION_RESOURCE=YES
PROVIDER_RESULT_IS_PROVENANCE_AUTHORITY=YES
INDEPENDENT_KEY_AND_VERSION_INPUTS=FORBIDDEN
```

Provider resolution occurs **outside** the store:

```text
PROVIDER_RESOLUTION_OCCURS_OUTSIDE_STORE=YES
STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
STORE_ACCEPTS_PROVENANCE_BOUND_MATERIAL=YES
```

`At1ExecutionStore` must accept already-resolved provenance-bound material. It
must **not** accept a commitment-key provider object, must not invoke provider
I/O, and must not resolve secrets.

Store verification duties vs non-duties:

```text
STORE_VERIFIES_VERSION_RESOURCE_EQUALITY=YES
STORE_VERIFIES_PAYLOAD_ORIGIN_FROM_SECRET_MANAGER=NO
```

Explanation (normative):

The provider result binds payload + exact version resource and is the
provenance authority for that pairing. `At1ExecutionStore` may validate the
version-resource identity shape and compare it with persisted metadata, but it
does **not** independently prove that arbitrary payload bytes originated from
Google Secret Manager. Secret-origin attestation is outside store scope and is
not authorized as a store responsibility under this grant.

Callers must not be able to pair arbitrary key payload with an independently
supplied version resource through any production-capable API.

### 8.3 Version resource acceptance rules

Accepted version resource shape must be an immutable exact Secret Manager
version resource name:

```text
projects/<project>/secrets/<secret>/versions/<numeric-version>
```

Additional shape constraints:

```text
NUMERIC_VERSION_MUST_BE_POSITIVE_INTEGER=YES
LATEST_ALLOWED=NO
ALIASES_ALLOWED=NO
QUERY_STRING_ALLOWED=NO
FRAGMENT_ALLOWED=NO
WHITESPACE_ALLOWED=NO
```

Normative refusals:

```text
VERSION_RESOURCE_LATEST=REJECT
VERSION_RESOURCE_ALIAS=REJECT
VERSION_RESOURCE_MISSING_NUMERIC_VERSION=REJECT
VERSION_RESOURCE_NON_POSITIVE_NUMERIC_VERSION=REJECT
VERSION_RESOURCE_NON_MATCHING_SHAPE=REJECT
VERSION_RESOURCE_WITH_QUERY_STRING=REJECT
VERSION_RESOURCE_WITH_FRAGMENT=REJECT
VERSION_RESOURCE_WITH_WHITESPACE=REJECT
EMPTY_VERSION_RESOURCE=REJECT
```

### 8.4 Synthetic vs real provider

```text
SYNTHETIC_PROVIDER_IMPLEMENTATION_AUTHORIZED=YES
REAL_SECRET_MANAGER_PROVIDER_IMPLEMENTATION_AUTHORIZED=NO
REAL_COMMITMENT_KEY_READ_AUTHORIZED=NO
REAL_SECRET_MANAGER_ACCESS=FORBIDDEN
REAL_COMMITMENT_KEY_READS=FORBIDDEN
```

The consumer may implement a synthetic/offline provider that emits deterministic
key material and an exact synthetic version resource string for tests and local
offline store initialization proofs.

The consumer must **not** implement a real Secret Manager-backed provider under
this grant, must not perform real secret reads, must not create secrets, and
must not configure secret IAM.

### 8.5 Material security (payload exposure)

```text
COMMITMENT_MATERIAL_PAYLOAD_LOGGING=FORBIDDEN
COMMITMENT_MATERIAL_PAYLOAD_REPR_EXPOSURE=FORBIDDEN
COMMITMENT_MATERIAL_PAYLOAD_SERIALIZATION=FORBIDDEN
COMMITMENT_MATERIAL_VERSION_RESOURCE_LOGGABLE=YES
COMMITMENT_KEY_PAYLOAD_STORED_IN_DB=NO
```

Commitment-key payload must not appear in logs, `repr`/`str` debug surfaces,
exception messages, serialized public projections, or SQLite. The non-secret
version resource identity may be logged and may be persisted as store metadata.

## 9. Freeze store contract (normative)

```text
INITIAL_STORE_SCHEMA_VERSION=1
CURRENT_STORE_SCHEMA_VERSION=1
SUPPORTED_STORE_SCHEMA_VERSIONS=1

LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED

AT8M2_FORWARD_MIGRATION_STEP_IMPLEMENTED=NO
FORWARD_MIGRATION_FRAMEWORK_POLICY=FORWARD_ONLY_WHEN_A_FUTURE_VERSION_EXISTS
UNKNOWN_NEWER_SCHEMA_VERSION=FAIL_CLOSED
MISSING_OR_INVALID_SCHEMA_METADATA=FAIL_CLOSED

NEW_STORE_INITIALIZATION_ATOMIC=YES
INITIALIZATION_SCHEMA_AND_METADATA_ATOMIC=YES
INITIALIZATION_FAILURE_MUST_NOT_PRODUCE_ACCEPTABLE_PARTIAL_STORE=YES
REOPEN_AFTER_INTERRUPTED_INITIALIZATION=FAIL_CLOSED
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED

COMMITMENT_KEY_VERSION_RESOURCE_METADATA_MUTABLE=NO
SCHEMA_VERSION_METADATA_MUTABLE=FORWARD_ONLY_MIGRATION

COMMITMENT_KEY_PAYLOAD_STORED_IN_DB=NO

STORE_SCHEMA_VERSIONING_OWNER=At1ExecutionStore
STORE_METADATA_TABLE_REQUIRED=YES
STORE_METADATA_FIELDS=
  schema_version
  commitment_key_version_resource

COMMITMENT_KEY_VERSIONING_MODEL=PIN_STORE_TO_EXACT_SECRET_VERSION
STORE_COMMITMENT_KEY_VERSION_IMMUTABLE_AFTER_INITIALIZATION=YES
SILENT_COMMITMENT_KEY_ROTATION=FORBIDDEN

STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
STORE_ACCEPTS_PROVENANCE_BOUND_MATERIAL=YES
STORE_VERIFIES_VERSION_RESOURCE_EQUALITY=YES
STORE_VERIFIES_PAYLOAD_ORIGIN_FROM_SECRET_MANAGER=NO
```

### 9.1 Schema v1 reality (AT8M2)

AT8M2 implements schema version **1** only:

```text
INITIAL_STORE_SCHEMA_VERSION=1
CURRENT_STORE_SCHEMA_VERSION=1
SUPPORTED_STORE_SCHEMA_VERSIONS=1
AT8M2_FORWARD_MIGRATION_STEP_IMPLEMENTED=NO
```

There is no AT8M2 migration step from v1 to a later version because no later
supported version exists in this unit. Forward-only migration remains the
**framework policy** for a future version when one is authorized later:

```text
FORWARD_MIGRATION_FRAMEWORK_POLICY=FORWARD_ONLY_WHEN_A_FUTURE_VERSION_EXISTS
```

AT8M2 must still fail closed on:

- legacy unversioned stores;
- missing/corrupt/invalid metadata;
- unknown newer schema versions than the running code understands.

AT8M2 must **not** claim or prove a forward migration step behavior as an
implementation requirement of this unit.

### 9.2 Metadata bootstrap rules

On first initialization of a new store file:

1. create required schema tables and metadata in one atomic initialization
   boundary;
2. write `schema_version=1` and the pinned `commitment_key_version_resource`
   from the provenance-bound material object;
3. never persist commitment-key payload bytes in SQLite, logs, or public
   projections.

On reopen:

1. require metadata present and valid; fail closed if missing, corrupt, empty,
   or unrecognized;
2. require supplied material object's version resource to equal the pinned
   metadata version resource; fail closed on mismatch;
3. never silently re-pin or rewrite `commitment_key_version_resource`;
4. if `schema_version` equals supported current (1): open normally;
5. if `schema_version` is newer than the running code understands: fail closed;
6. if a future authorized version introduces migrations, apply only forward-only
   store-owned migrations under a later grant — not under AT8M2.

Legacy unversioned stores (claims/attempts/ledgers without authoritative
metadata) must fail closed. Auto-migration of legacy unversioned stores is
forbidden. Commitment-key provenance must not be inferred post hoc for legacy
files.

### 9.3 Atomic initialization

```text
NEW_STORE_INITIALIZATION_ATOMIC=YES
INITIALIZATION_SCHEMA_AND_METADATA_ATOMIC=YES
INITIALIZATION_FAILURE_MUST_NOT_PRODUCE_ACCEPTABLE_PARTIAL_STORE=YES
REOPEN_AFTER_INTERRUPTED_INITIALIZATION=FAIL_CLOSED
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
```

Schema tables and metadata must initialize as one acceptable store boundary.
Initialization failure must not leave behind a store file that subsequent open
treats as valid. Reopen after interrupted initialization must fail closed.

Exact SQLite transaction mechanics remain an implementation detail of the
consumer, provided the atomicity and fail-closed reopen contracts hold.

## 10. Constructor / API decision (normative)

Freeze one canonical construction path where key payload and exact version
resource arrive as one provenance-bound material object.

```text
CANONICAL_CONSTRUCTION_PATH=PROVENANCE_BOUND_MATERIAL_OBJECT_ONLY
INDEPENDENT_KEY_AND_VERSION_PRODUCTION_INPUTS=FORBIDDEN
RAW_KEY_PLUS_SEPARATE_VERSION_RESOURCE_PRODUCTION_API=FORBIDDEN
RAW_KEY_ONLY_STORE_CONSTRUCTOR_RETAINED=NO
TEST_ONLY_COMPAT_SEAM_ALLOWED=NO
STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
STORE_ACCEPTS_PROVENANCE_BOUND_MATERIAL=YES
```

Do not leave raw key + separately supplied version resource as independent
production-capable inputs. Do not retain a raw-key-only store constructor.

Current main constructor shape (historical; must be removed/replaced by
consumer — not retained even as test-only):

```text
At1ExecutionStore(db_path=..., commitment_key=...)
```

That historical shape supplies key payload without pinned version provenance and
is incompatible with the AT8M1 pin model.

### 10.1 Required construction invariant

Any `At1ExecutionStore` construction path authorized for retention after this
consumer must:

1. accept commitment-key material only as a provenance-bound object that already
   pairs payload + exact version resource; and
2. refuse provider objects as store constructor inputs; and
3. refuse independent key/version injection; and
4. refuse raw-key-only construction.

Exact symbol names and parameter spellings are consumer implementation details
inside authorized source paths, provided the invariant holds.

### 10.2 No test-only compatibility seam

```text
TEST_ONLY_COMPAT_SEAM_ALLOWED=NO
RAW_KEY_ONLY_STORE_CONSTRUCTOR_RETAINED=NO
```

A test-only compatibility seam is **not** authorized. All four frozen
constructor-consumer tests must move to the canonical provenance-bound material
path:

```text
tests/integrations/ghl/test_at1_live_transport_remediation.py
tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

## 11. One-shot consumption event (normative)

```text
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

AUTHORIZATION_CONSUMPTION_EVENT=
FIRST_COMMITTED_MUTATION_TO_ANY_AUTHORIZED_CONSUMER_SOURCE_OR_TEST_PATH

PARTIAL_IMPLEMENTATION_CONSUMES_AUTHORIZATION=YES
FAILED_IMPLEMENTATION_CONSUMES_AUTHORIZATION=YES
ABANDONED_IMPLEMENTATION_AFTER_FIRST_MUTATION_CONSUMES_AUTHORIZATION=YES
RETRY_AFTER_CONSUMPTION_REQUIRES_NEW_AUTHORIZATION=YES
PRE-CONSUMPTION_READ_ONLY_VALIDATION_DOES_NOT_CONSUME_AUTHORIZATION=YES
```

Consumption occurs at the first **committed** mutation to any authorized
consumer source or test path listed in §7.2. After that event:

- partial implementation has consumed the grant;
- failed implementation has consumed the grant;
- abandoned implementation after first mutation has consumed the grant;
- retry requires a **new** authorization artifact/unit.

Read-only pre-consumption validation (fetch, merge-base checks, blob-sha
verification, inventory re-grep, local non-committed experiments that are
discarded without commit to authorized paths) does **not** consume the grant.

Proof/doc path writes under authorized proof/doc paths should record
consumption but do not redefine the consumption event away from first committed
source/test mutation. The consumer must still emit the required consumption
record.

## 12. Implementation ancestry and pre-mutation recording (normative)

```text
CONSUMER_BRANCH_MUST_DESCEND_FROM_AUTHORIZATION_MERGE_SHA=YES
AUTHORIZATION_ARTIFACT_BLOB_SHA_MUST_MATCH_REVIEWED_MERGED_BLOB=YES
```

Before any mutation to an authorized consumer source or test path, the consumer
must verify and record:

```text
AUTHORIZATION_PR=<future number>
AUTHORIZATION_REVIEWED_HEAD=<future SHA>
AUTHORIZATION_MERGE_SHA=<future SHA>
AUTHORIZATION_ARTIFACT_BLOB_SHA=<future SHA>
```

Rules:

1. consumer branch must descend from the authorization merge SHA;
2. the authorization artifact blob SHA on the consumer base must match the
   reviewed merged blob SHA of this artifact on `main`;
3. mismatch → STOP; do not mutate authorized paths;
4. record the four fields above in the consumption record (and any
   implementation doc) before first authorized source/test mutation.

Placeholders remain `<future …>` until this authorization PR is reviewed and
merged; the consumer fills concrete values at consumption time.

## 13. Authorized implementation objectives (future consumer)

When effective, the consumer may implement only:

1. store metadata table and schema version marker in `At1ExecutionStore`
   (`schema_version=1` current);
2. atomic new-store initialization and fail-closed partial/interrupted-init
   handling;
3. pin of `commitment_key_version_resource` at initialization (immutable after);
4. fail-closed open rules for legacy unversioned stores, missing/corrupt
   metadata, and unknown newer schema;
5. synthetic commitment-key provider module at the exact authorized path
   (provider resolution outside store);
6. canonical provenance-bound material construction path only (no raw-key
   constructor; no test-only compat seam; store does not accept provider
   objects);
7. adaptations of all four frozen construction-consumer tests to the canonical
   path;
8. new provider tests at the exact authorized provider test path;
9. proof under `proof/nw008/at-8m2/**` and the exact implementation doc path,
   including one-shot consumption record.

AT8M2 does **not** implement a forward migration step.

## 14. Required implementation proof (later consumer; normative checklist)

The implementation consumer must include deterministic tests covering at least:

```text
REQUIRED_DETERMINISTIC_PROOFS=
  - new store initialization
  - schema v1 initialization succeeds
  - schema v1 reopen succeeds
  - atomic initialization failure
  - initialization failure must not produce acceptable partial store
  - reopen after interrupted initialization fails closed
  - exact numeric version acceptance
  - latest/alias rejection
  - query-string/fragment/whitespace version rejection
  - non-positive numeric version rejection
  - reopen with same version succeeds
  - reopen with different version fails
  - missing metadata fails
  - corrupt metadata fails
  - legacy/unversioned store fails closed
  - unknown newer schema fails closed
  - AT8M2 performs no migration step
  - commitment-key payload never stored
  - commitment-key payload not logged/repr/serialized
  - independent key/version injection impossible
  - store rejects provider object construction input
  - store accepts only provenance-bound material
```

Removed from AT8M2 required proofs (explicitly not an AT8M2 implementation
requirement):

```text
AT8M2_NOT_REQUIRED_PROOFS=
  - schema forward migration behavior
```

Proof expectations:

- tests are offline and deterministic;
- `IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS`;
- no real Secret Manager access;
- no HighLevel / CRM / IAM / deployment side effects;
- consumption record cites which tests cover each required proof bullet.

## 15. Explicit non-authority / forbidden

```text
AT8M2_AUTHORIZATION_IMPLEMENTS_CODE=NO
AT8M2_AUTHORIZATION_PR_WRITES_SRC=NO
AT8M2_AUTHORIZATION_PR_WRITES_TESTS=NO

REAL_SECRET_MANAGER_ACCESS=FORBIDDEN
REAL_COMMITMENT_KEY_READS=FORBIDDEN
SECRET_CREATION=FORBIDDEN
SECRET_IAM=FORBIDDEN
SERVICE_ACCOUNT_IMPERSONATION=FORBIDDEN
SERVICE_ACCOUNT_ATTACHMENT=FORBIDDEN
HIGHLEVEL_CALLS=FORBIDDEN
CRM_MUTATIONS=FORBIDDEN
DEPLOYMENT=FORBIDDEN
LIVE_RUNTIME_ACTIVATION=FORBIDDEN
LIVE_NOTE_SECRET_ACCESSOR_REUSE=FORBIDDEN
PR120_AUTHORITY_REUSE=FORBIDDEN
AT8K2_AUTHORITY_REUSE=FORBIDDEN

LIVE_PRODUCTION_STORE_ACTIVATION=FORBIDDEN
PRODUCTION_COMPOSITION_ROOT_STORE_WIRING=FORBIDDEN
LIVE_MUTATION_AUTHORIZATION_CREATION=FORBIDDEN
PACKAGE_MANIFEST_MUTATION=FORBIDDEN
DEPENDENCY_MANIFEST_MUTATION=FORBIDDEN

TEST_ONLY_COMPAT_SEAM_ALLOWED=NO
RAW_KEY_ONLY_STORE_CONSTRUCTOR_RETAINED=NO
STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
AT8M2_FORWARD_MIGRATION_STEP_IMPLEMENTED=NO
```

### Non-transitivity

```text
PR123_AT8M1_GRANTS_AT8M2_IMPLEMENTATION=NO
AT8M_GRANTS_AT8M2_IMPLEMENTATION=NO
AT8M1_GRANTS_AT8M2_IMPLEMENTATION=NO
PR120_GRANTS_AT8M2=NO
AT8K2_GRANTS_AT8M2=NO
AT8L_GRANTS_AT8M2=NO
AT8M2_GRANTS_LIVE_PRODUCTION_STORE_ACTIVATION=NO
AT8M2_GRANTS_REAL_SECRET_MANAGER_PROVIDER=NO
AT8M2_GRANTS_HIGHLEVEL_OR_CRM=NO
AT8M2_GRANTS_IAM_OR_DEPLOYMENT=NO
```

AT8M1 made offline store-substrate implementation authorization designable. That
designability is not implementation authority. This artifact is the one-shot
implementation grant proposal; it becomes usable only after merge + consumer
verification. Even after effectiveness, it does not grant live activation or
real secret access.

## 16. Live blockers intentionally out of scope

Preserved from AT8M / AT8M1; not closed by this authorization:

```text
LIVE_BLOCKERS_REMAINING=
  runtime-identity-mechanism
  commitment-key-secret-resource
  commitment-key-access-principal
  commitment-key-secret-IAM
  real-commitment-key-provider
  real-secret-access

LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO
PRODUCTION_RUNTIME_READY=NO
LIVE_CREDENTIAL_USE_READY=NO
LIVE_HIGHLEVEL_EXECUTION_READY=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## 17. Validation (this authorization PR)

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=governance/authorizations/nw008-at8m2-offline-execution-store-substrate-implementation-authorization-001.md
SRC_CHANGES=0
TEST_CHANGES=0
SECRET_CHANGES=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
CONTRACT_CHANGES=0
PACKAGE_MANIFEST_CHANGES=0
EXTERNAL_EFFECTS=0
IMPLEMENTATION_CHANGE=NO
```

Expected validation commands after artifact creation/normalization:

```text
git diff --name-status origin/main...HEAD
git diff --check origin/main...HEAD
# name-status must list exactly the one authorization artifact
```

## 18. Return

```text
AT8M2_AUTHORIZATION_ARTIFACT_CREATED=YES
AT8M2_AUTHORIZATION_NORMALIZATION_COMPLETE=YES
AT8M2_AUTHORIZATION_PR_CLASS=authorization
AT8M2_MODE=AUTHORIZATION_ARTIFACT_ONLY
AT8M2_IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS
AT8M2_GRANT=OFFLINE_DETERMINISTIC_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION
AT8M2_AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AT8M2_AUTHORIZATION_REUSABLE=NO
AT8M2_AUTHORIZATION_TRANSFERABLE=NO

PR123_MERGED=YES
PR123_REVIEWED_HEAD=ab1c8f1ac072519e86e9b3390cc256eb13c9ab19
PR123_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES
AT8M1_ARTIFACT_ON_MAIN=YES

AT1_EXECUTION_STORE_SOURCE_CONSUMERS_REINSPECTED=YES
AT1_EXECUTION_STORE_TEST_CONSUMERS_REINSPECTED=YES
NEW_CONSUMERS_SINCE_AT8M1=0

AUTHORIZED_SOURCE_PATHS=
  src/integrations/ghl/at1_execution_store.py
  src/integrations/ghl/at1_commitment_key_provider.py

AUTHORIZED_TEST_PATHS=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
  tests/integrations/ghl/test_at1_commitment_key_provider.py

AUTHORIZED_PROOF_PATHS=
  proof/nw008/at-8m2/**

AUTHORIZED_DOC_PATH_EXACT=
  docs/nw008/nw-008-at8m2-offline-execution-store-substrate-implementation-001.md

PROVIDER_SCOPE=EXECUTION_STORE_COMMITMENT_KEY_ONLY
PROVIDER_MODULE=src/integrations/ghl/at1_commitment_key_provider.py
PROVIDER_RESULT_BINDS_PAYLOAD_AND_VERSION_RESOURCE=YES
PROVIDER_RESULT_IS_PROVENANCE_AUTHORITY=YES
PROVIDER_RESOLUTION_OCCURS_OUTSIDE_STORE=YES
STORE_ACCEPTS_COMMITMENT_KEY_PROVIDER=NO
STORE_ACCEPTS_PROVENANCE_BOUND_MATERIAL=YES
STORE_VERIFIES_VERSION_RESOURCE_EQUALITY=YES
STORE_VERIFIES_PAYLOAD_ORIGIN_FROM_SECRET_MANAGER=NO
INDEPENDENT_KEY_AND_VERSION_INPUTS=FORBIDDEN
LATEST_ALLOWED=NO
ALIASES_ALLOWED=NO
QUERY_STRING_ALLOWED=NO
FRAGMENT_ALLOWED=NO
WHITESPACE_ALLOWED=NO
NUMERIC_VERSION_MUST_BE_POSITIVE_INTEGER=YES
SYNTHETIC_PROVIDER_IMPLEMENTATION_AUTHORIZED=YES
REAL_SECRET_MANAGER_PROVIDER_IMPLEMENTATION_AUTHORIZED=NO

COMMITMENT_MATERIAL_PAYLOAD_LOGGING=FORBIDDEN
COMMITMENT_MATERIAL_PAYLOAD_REPR_EXPOSURE=FORBIDDEN
COMMITMENT_MATERIAL_PAYLOAD_SERIALIZATION=FORBIDDEN
COMMITMENT_MATERIAL_VERSION_RESOURCE_LOGGABLE=YES

INITIAL_STORE_SCHEMA_VERSION=1
CURRENT_STORE_SCHEMA_VERSION=1
SUPPORTED_STORE_SCHEMA_VERSIONS=1
AT8M2_FORWARD_MIGRATION_STEP_IMPLEMENTED=NO
FORWARD_MIGRATION_FRAMEWORK_POLICY=FORWARD_ONLY_WHEN_A_FUTURE_VERSION_EXISTS
LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
UNKNOWN_NEWER_SCHEMA_VERSION=FAIL_CLOSED
NEW_STORE_INITIALIZATION_ATOMIC=YES
INITIALIZATION_SCHEMA_AND_METADATA_ATOMIC=YES
INITIALIZATION_FAILURE_MUST_NOT_PRODUCE_ACCEPTABLE_PARTIAL_STORE=YES
REOPEN_AFTER_INTERRUPTED_INITIALIZATION=FAIL_CLOSED
COMMITMENT_KEY_VERSION_RESOURCE_METADATA_MUTABLE=NO
SCHEMA_VERSION_METADATA_MUTABLE=FORWARD_ONLY_MIGRATION
COMMITMENT_KEY_PAYLOAD_STORED_IN_DB=NO

CANONICAL_CONSTRUCTION_PATH=PROVENANCE_BOUND_MATERIAL_OBJECT_ONLY
RAW_KEY_ONLY_STORE_CONSTRUCTOR_RETAINED=NO
TEST_ONLY_COMPAT_SEAM_ALLOWED=NO

AUTHORIZATION_CONSUMPTION_EVENT=
FIRST_COMMITTED_MUTATION_TO_ANY_AUTHORIZED_CONSUMER_SOURCE_OR_TEST_PATH
AUTHORIZATION_CONSUMPTION_EVENT_FROZEN=YES
PARTIAL_IMPLEMENTATION_CONSUMES_AUTHORIZATION=YES
FAILED_IMPLEMENTATION_CONSUMES_AUTHORIZATION=YES
ABANDONED_IMPLEMENTATION_AFTER_FIRST_MUTATION_CONSUMES_AUTHORIZATION=YES
RETRY_AFTER_CONSUMPTION_REQUIRES_NEW_AUTHORIZATION=YES
PRE-CONSUMPTION_READ_ONLY_VALIDATION_DOES_NOT_CONSUME_AUTHORIZATION=YES

CONSUMER_BRANCH_MUST_DESCEND_FROM_AUTHORIZATION_MERGE_SHA=YES
AUTHORIZATION_ARTIFACT_BLOB_SHA_MUST_MATCH_REVIEWED_MERGED_BLOB=YES

EXTERNAL_EFFECTS=0
IMPLEMENTATION_PERFORMED=NO
```

STOP after authorization artifact + validation.
Do not implement.
