# NW-008 AT-8M1 — Execution Store Schema and Commitment Key Versioning Design 001

```text
UNIT=NW008_AT8M1_EXECUTION_STORE_SCHEMA_AND_COMMITMENT_KEY_VERSIONING_DESIGN_001
PR_CLASS=planning_only
PHASE=PLANNING_ONLY
MODE=READ_ONLY_ARCHITECTURE_DECISION
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=nw008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=e5249cbb121660379be546633b252ff950cb2db3
PLAN_HEAD_AT_START=e5249cbb121660379be546633b252ff950cb2db3

PR122_MERGED=YES
PR122_MERGE_SHA=e5249cbb121660379be546633b252ff950cb2db3
PR122_REVIEWED_HEAD=0deb2de445b6735ff7549aab37ac73fe0e854842
PR122_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES
AT8M_ARTIFACT_ON_MAIN=YES
AT8M_ARTIFACT_PATH=
docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001.md

PLANNING_ONLY=YES
IMPLEMENTATION_CHANGE=NO
RUNTIME_CHANGE=NO
TEST_CHANGE=NO
CONTRACT_CHANGE=NO
PACKAGE_MANIFEST_CHANGE=NO
AUTHORIZATION_ARTIFACT_CREATED=NO
LIVE_MUTATION_AUTHORIZATION_CREATED=NO

EXTERNAL_EFFECTS=0
```

## Pre-flight

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH_AT_START=nw008-at8m-production-runtime-substrate-and-execution-store-authority-design-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_ORIGIN_MAIN_SHA=e5249cbb121660379be546633b252ff950cb2db3
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_UNTRACKED_FILES=0
PREFLIGHT_RECORDED_AT_LOCAL=2026-08-21T18:25:30-0400
```

Abort conditions did not fire: starting branch was not `main`; worktree had no
unrelated changes. After PR122 verification, this unit branched from fresh
`origin/main` at the PR122 merge SHA.

## PR122 verification

```text
PR122_STATE=MERGED
PR122_MERGED_AT_UTC=2026-08-21T22:25:13Z
PR122_MERGE_SHA=e5249cbb121660379be546633b252ff950cb2db3
PR122_REVIEWED_HEAD=0deb2de445b6735ff7549aab37ac73fe0e854842
PR122_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES
AT8M_ARTIFACT_ON_MAIN=YES
```

PR122 is the merged AT8M planning unit. This unit does not reopen AT8M host
class, identity-mechanism, DB-path, or live-activation decisions. It closes only
the two remaining **store-internal** architecture decisions named as AT8M
blockers for offline store-substrate implementation authorization designability:

1. commitment-key versioning model
2. store schema-versioning scope / ownership

## Non-actions

```text
SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0
AT1_EXECUTION_STORE_MUTATIONS=0
LIVE_NOTE_RUNTIME_MUTATIONS=0
SECRET_MANAGER_INVOCATIONS=0
MG_GUIDE_PIT_GHL_READS=0
SERVICE_ACCOUNT_IMPERSONATION=0
SERVICE_ACCOUNT_ATTACHMENT=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0

REAL_SECRET_PAYLOAD_READS=0
REAL_COMMITMENT_KEY_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
GCP_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0

AT8M1_AUTHORIZATION_CREATED=NO
OFFLINE_STORE_SUBSTRATE_IMPLEMENTATION_AUTHORIZATION_CREATED=NO
```

Read-only sources consulted:

- `docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001.md`
- `src/integrations/ghl/at1_execution_store.py` (current unversioned schema surface)

This unit designs only. It does not implement store schema versioning, does not
modify `At1ExecutionStore`, does not create an authorization artifact, and does
not touch secrets, IAM, HighLevel, CRM, or deployment state.

## AT8M state preserved

```text
PRODUCTION_RUNTIME_HOST_CLASS=GOVERNED_SINGLE_INSTANCE_LONG_LIVED_LOCAL_PROCESS
PRODUCTION_RUNTIME_HOST_CLASS_DECIDED=YES
PRODUCTION_RUNTIME_IDENTITY_MECHANISM=UNRESOLVED
PRODUCTION_RUNTIME_IDENTITY_MECHANISM_DECIDED=NO
PRODUCTION_RUNTIME_PLATFORM_DECIDED=PARTIAL

PRODUCTION_RUNTIME_PRINCIPAL_IDENTIFIED=YES
PRODUCTION_RUNTIME_PRINCIPAL_CREATED=YES
PRODUCTION_RUNTIME_PRINCIPAL=
serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PRODUCTION_WORKLOAD_PRINCIPAL_ATTACHED=NO

SQLITE_PRODUCTION_SUITABLE=CONDITIONAL
PRODUCTION_DB_PATH_CONFIGURATION_REQUIRED=YES
PRODUCTION_DB_PATH_DEFAULT=NONE
MISSING_PRODUCTION_DB_PATH=FAIL_CLOSED

PRODUCTION_COMMITMENT_KEY_SOURCE_CLASS=GOOGLE_SECRET_MANAGER
COMMITMENT_KEY_SECRET_RESOURCE_IDENTIFIED=NO
COMMITMENT_KEY_SECRET_RESOURCE_CREATED=NO
COMMITMENT_KEY_SECRET_IAM_CONFIGURED=NO
COMMITMENT_KEY_ACCESS_PRINCIPAL_DECIDED=NO
COMMITMENT_KEY_ACCESS_PRINCIPAL=UNRESOLVED
SAME_PRINCIPAL_FOR_GHL_AND_COMMITMENT_KEY=UNRESOLVED
AT8K2_IAM_AUTHORITY_REUSABLE_FOR_COMMITMENT_KEY=NO

PRODUCTION_RUNTIME_READY=NO
LIVE_CREDENTIAL_USE_READY=NO
LIVE_HIGHLEVEL_EXECUTION_READY=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## Design question 1 — commitment-key versioning model

### Decision

```text
COMMITMENT_KEY_VERSIONING_MODEL=PIN_STORE_TO_EXACT_SECRET_VERSION
STORE_COMMITMENT_KEY_VERSION_IMMUTABLE_AFTER_INITIALIZATION=YES
SILENT_COMMITMENT_KEY_ROTATION=FORBIDDEN
KEY_ROTATION_REQUIRES_NEW_STORE_OR_AUTHORIZED_MIGRATION=YES
OLD_KEY_VERSION_MUST_REMAIN_AVAILABLE_WHILE_STORE_DEPENDS_ON_IT=YES
PER_RECORD_KEY_VERSION_COLUMN_REQUIRED=NO
KEY_VERSION_REQUIRED_FOR_HISTORICAL_VERIFICATION=YES
COMMITMENT_KEY_VERSION_RESOURCE_MUST_BE_EXACT_VERSION=YES
COMMITMENT_KEY_VERSION_ALIAS_ALLOWED=NO
COMMITMENT_KEY_VERSION_LATEST_ALLOWED=NO
```

### Rationale

AT8M recorded two undecided candidates. This unit selects
`PIN_STORE_TO_EXACT_SECRET_VERSION`:

1. Current `At1ExecutionStore` commitments are store-global HMAC digests under a
   single in-memory key (`_commitment_key`). A single pinned version matches the
   existing store semantics without a per-record key-version column.
2. Single-writer local SQLite already treats the store file as a durable unit of
   evidence. Pinning the key version to the store file keeps verification simple:
   open store → read pinned version resource → obtain that exact key material →
   verify all commitments.
3. Per-record version columns would add schema/API surface without benefit under
   the single-key store model and would invite silent multi-key coexistence that
   is harder to audit.

### Rotation and immutability rules

- After a store is initialized, its pinned commitment-key version resource is
  immutable for the life of that store file.
- Silent rotation is forbidden. Replacing key material while reusing the same
  store file without an authorized migration is forbidden.
- Key rotation requires either:
  - a new store file initialized under the new exact secret version; or
  - a separately authorized migration/rebuild path that re-commits evidence
    under the new version with explicit governance.
- While any live store depends on an old exact secret version, that version must
  remain available (enabled / readable under authorized access). Disabling or
  destroying a secret version that a store still pins is an operator integrity
  violation outside this design unit.

### What is stored vs not stored

```text
COMMITMENT_KEY_PAYLOAD_STORED_IN_DB=NO
COMMITMENT_KEY_VERSION_RESOURCE_IS_SECRET_PAYLOAD=NO
```

The store records only a non-secret version **resource identity** (for example a
Secret Manager version resource name or equivalent non-payload reference). The
key payload itself is never written to SQLite, never logged, and never returned
by store public projection APIs.

Accepted version-resource shape must resolve to an immutable exact Secret
Manager version, conceptually:

`projects/<project>/secrets/<secret>/versions/<numeric-version>`

Aliases such as `latest` are not valid store pin targets.

## Design question 2 — store schema versioning scope

### Decision

```text
STORE_SCHEMA_VERSIONING_SCOPE_RESOLVED=YES
STORE_SCHEMA_VERSIONING_OWNER=At1ExecutionStore
STORE_SCHEMA_VERSIONING_REQUIRED=YES
STORE_SCHEMA_VERSIONING_IMPLEMENTED=NO
INITIAL_STORE_SCHEMA_VERSION=1
LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
FORWARD_ONLY_SCHEMA_MIGRATIONS_APPLY_FROM_VERSION=1

STORE_METADATA_TABLE_REQUIRED=YES
STORE_METADATA_FIELDS=
  schema_version
  commitment_key_version_resource

FORWARD_ONLY_SCHEMA_MIGRATIONS=YES
UNKNOWN_NEWER_SCHEMA_VERSION=FAIL_CLOSED
MISSING_OR_INVALID_SCHEMA_METADATA=FAIL_CLOSED

COMMITMENT_KEY_VERSION_RESOURCE_METADATA_MUTABLE=NO
SCHEMA_VERSION_METADATA_MUTABLE=FORWARD_ONLY_MIGRATION
NEW_STORE_INITIALIZATION_ATOMIC=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
```

### Ownership and writable scope

Schema versioning is owned by `At1ExecutionStore`, not by the composition root
alone. The composition root remains the production construction authority for
path/provider assembly (per AT8M), but metadata bootstrap, schema markers,
forward-only migrations, and fail-closed open checks belong in the store class.

A later offline implementation authorization may include these writable paths:

```text
LATER_IMPLEMENTATION_WRITABLE_SCOPE_MAY_INCLUDE=
  src/integrations/ghl/at1_execution_store.py
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

This unit does not modify those paths and does not create that authorization.

### Metadata table design (design only)

Current store bootstrap is unversioned (`CREATE TABLE IF NOT EXISTS` for
claims/attempts/ledgers only). Production-grade open requires a store metadata
table (name is an implementation detail) holding at least:

1. `schema_version` — integer or monotonic version marker understood by
   `At1ExecutionStore`
2. `commitment_key_version_resource` — non-secret pinned version resource
   identity selected at initialization under the versioning model above

Rules:

- On first initialization of a new store: write metadata once with the current
  schema version and the pinned commitment-key version resource.
- New store initialization must be atomic: schema tables + metadata must be
  committed as one valid initialization boundary; partial initialization states
  are invalid and must fail closed on reopen.
- On reopen: require metadata present and valid; fail closed if missing, corrupt,
  empty, or unrecognized.
- Legacy unversioned stores (without authoritative metadata) must fail closed;
  they must not be auto-migrated and must not have commitment-key provenance
  inferred post hoc.
- If `schema_version` is older than the code's current version: apply only
  forward-only, store-owned migrations starting from version 1; no ad-hoc DDL
  outside the store.
- If `schema_version` is newer than the running code understands: fail closed.
- If `commitment_key_version_resource` is missing/empty or differs from the key
  material supplied for this open: fail closed. The store must not silently
  re-pin or accept a different key version.
- `commitment_key_version_resource` metadata is immutable after initialization;
  migrations may advance `schema_version` but must not silently rewrite the
  pinned commitment-key version resource.

### Explicit non-goals for schema versioning

- No automatic evidence deletion / compaction
- No multi-writer schema coordination
- No networked / multi-instance migration protocol
- No storage of commitment-key payload bytes in metadata or ledgers

## Design question 3 — commitment-key provider boundary

### Decision

```text
COMMITMENT_KEY_USES_LIVE_NOTE_SECRET_ACCESSOR=NO
COMMITMENT_KEY_PROVIDER_INTERFACE_REQUIRED=YES
COMMITMENT_KEY_PROVIDER_PUBLIC_PURPOSE=EXECUTION_STORE_COMMITMENT_KEY_ONLY
OFFLINE_IMPLEMENTATION_SYNTHETIC_PROVIDER_ALLOWED=YES
REAL_SECRET_MANAGER_COMMITMENT_KEY_PROVIDER_AUTHORIZED=NO
REAL_COMMITMENT_KEY_READ_AUTHORIZED=NO
COMMITMENT_KEY_AND_VERSION_RESOURCE_SAME_PROVIDER_RESULT=YES
INDEPENDENT_KEY_AND_VERSION_CALLER_INPUTS=FORBIDDEN
```

Preserves AT8M separation: the GHL live-note secret accessor path
(`LiveNoteSecretAccessor` / AT8N GHL PIT scope) must not deliver execution-store
commitment keys.

For a later offline store-substrate implementation:

- A narrow commitment-key provider interface is required, purpose-limited to
  execution-store commitment-key delivery only. The provider must return one
  logical result containing both (a) commitment-key payload and
  (b) exact pinned commitment-key version resource identity.
- A synthetic/offline provider is allowed under offline implementation authority
  so store schema + pin behavior can be tested deterministically with zero real
  secret reads.
- A real Secret Manager commitment-key provider is **not** authorized by this
  unit and is **not** designable for live activation until remaining live
  blockers close (resource identity, principal, IAM, identity mechanism).

Exact provider symbol names, package placement, and constructor injection shape
are deferred to the offline implementation authorization / implementation unit.
This unit freezes only the boundary and purpose separation.

## Consumer test inventory (deterministic At1ExecutionStore usage)

```text
AT1_EXECUTION_STORE_CONSUMER_TEST_INVENTORY_REQUIRED=YES
IMPLEMENTATION_TEST_SCOPE_MUST_BE_FROZEN_BEFORE_AUTHORIZATION=YES
```

Read-only search was run for all current `At1ExecutionStore` construction/usage
across `src/` and `tests/` (`rg "At1ExecutionStore\\("` plus `rg
"At1ExecutionStore"`). Deterministic test files with direct
`At1ExecutionStore(...)` construction that would require change under the
planned API are:

1. `tests/integrations/ghl/test_at1_live_transport_remediation.py`
2. `tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py`
3. `tests/integrations/ghl/highlevel_rest/test_live_note_transport.py`
4. `tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py`

Frozen writable set for AT8M2 authorization design:

```text
AT8M2_TEST_WRITABLE_PATHS=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

No tests are modified in AT8M1.

## Derived fields

```text
STORE_INTERNAL_ARCHITECTURE_COMPLETE=YES

COMMITMENT_KEY_VERSIONING_MODEL=PIN_STORE_TO_EXACT_SECRET_VERSION
COMMITMENT_KEY_VERSION_RESOURCE_MUST_BE_EXACT_VERSION=YES
COMMITMENT_KEY_VERSION_ALIAS_ALLOWED=NO
COMMITMENT_KEY_VERSION_LATEST_ALLOWED=NO
STORE_SCHEMA_VERSIONING_SCOPE_RESOLVED=YES
STORE_SCHEMA_VERSIONING_OWNER=At1ExecutionStore
INITIAL_STORE_SCHEMA_VERSION=1
LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED

OFFLINE_STORE_SUBSTRATE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO

LIVE_BLOCKERS_REMAINING=
  runtime-identity-mechanism
  commitment-key-secret-resource
  commitment-key-access-principal
  commitment-key-secret-IAM
  real-commitment-key-provider
  real-secret-access

PRODUCTION_RUNTIME_READY=NO
LIVE_CREDENTIAL_USE_READY=NO
LIVE_HIGHLEVEL_EXECUTION_READY=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO

AT1_EXECUTION_STORE_CONSUMER_TEST_INVENTORY_REQUIRED=YES
IMPLEMENTATION_TEST_SCOPE_MUST_BE_FROZEN_BEFORE_AUTHORIZATION=YES
AT8M2_TEST_WRITABLE_PATHS=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

### What “offline store-substrate implementation authorization designable” means

A later, separate, one-shot **offline** implementation authorization may now be
drafted to implement only:

1. store metadata table and schema version marker in `At1ExecutionStore`
2. forward-only migration / fail-closed open rules
3. pin of `commitment_key_version_resource` at initialization (immutable after)
4. synthetic commitment-key provider seam for deterministic tests
5. tests only within the frozen `AT8M2_TEST_WRITABLE_PATHS` list

That authorization must still forbid:

- real Secret Manager commitment-key reads
- real commitment-key resource create/IAM
- production composition-root live activation
- HighLevel / CRM live calls
- reuse of PR120 / AT8K2 / any live-mutation authority
- use of `LiveNoteSecretAccessor` for commitment keys

### What remains not designable

Live production store activation remains non-designable while the live blockers
above remain open. Closing AT8M1 does not make production runtime ready and does
not authorize real secret access.

## Non-authority

```text
AT8M1_AUTHORIZES_IMPLEMENTATION=NO
AT8M1_AUTHORIZES_OFFLINE_STORE_SUBSTRATE_IMPLEMENTATION=NO
AT8M1_AUTHORIZES_PRODUCTION_STORE_CONSTRUCTION=NO
AT8M1_AUTHORIZES_SECRET_RESOURCE_CREATION=NO
AT8M1_AUTHORIZES_SECRET_PAYLOAD_READ=NO
AT8M1_AUTHORIZES_COMMITMENT_KEY_READ=NO
AT8M1_AUTHORIZES_IAM_CHANGE=NO
AT8M1_AUTHORIZES_SERVICE_ACCOUNT_ATTACHMENT=NO
AT8M1_AUTHORIZES_DEPLOYMENT_CHANGE=NO
AT8M1_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8M1_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8M1_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8M1_CREATES_IMPLEMENTATION_AUTHORIZATION=NO
AT8M1_REUSES_PR120_AUTHORIZATION=NO
AT8M1_REUSES_AT8K2_IAM_AUTHORIZATION=NO
```

## Validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md
SRC_CHANGES=0
TEST_CHANGES=0
IAM_CHANGES=0
SECRET_CHANGES=0
DEPLOYMENT_CHANGES=0
GIT_DIFF_CHECK=PASS
EXTERNAL_EFFECTS=0
```

`git diff --name-status origin/main...HEAD` lists exactly the one planning
artifact above; `git diff --check origin/main...HEAD` is clean.

## Return

```text
AT8M1_PLANNING_COMPLETE=YES
AT8M1_FINAL_NORMALIZATION_COMPLETE=YES

COMMITMENT_KEY_VERSIONING_MODEL=PIN_STORE_TO_EXACT_SECRET_VERSION
STORE_COMMITMENT_KEY_VERSION_IMMUTABLE_AFTER_INITIALIZATION=YES
SILENT_COMMITMENT_KEY_ROTATION=FORBIDDEN
PER_RECORD_KEY_VERSION_COLUMN_REQUIRED=NO
COMMITMENT_KEY_VERSION_RESOURCE_MUST_BE_EXACT_VERSION=YES
COMMITMENT_KEY_VERSION_ALIAS_ALLOWED=NO
COMMITMENT_KEY_VERSION_LATEST_ALLOWED=NO

LEGACY_UNVERSIONED_STORE_AUTO_MIGRATION=NO
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
INITIAL_STORE_SCHEMA_VERSION=1
NEW_STORE_INITIALIZATION_ATOMIC=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED

STORE_SCHEMA_VERSIONING_SCOPE_RESOLVED=YES
STORE_SCHEMA_VERSIONING_OWNER=At1ExecutionStore
STORE_METADATA_TABLE_REQUIRED=YES

COMMITMENT_KEY_USES_LIVE_NOTE_SECRET_ACCESSOR=NO
COMMITMENT_KEY_PROVIDER_INTERFACE_REQUIRED=YES
OFFLINE_IMPLEMENTATION_SYNTHETIC_PROVIDER_ALLOWED=YES
REAL_SECRET_MANAGER_COMMITMENT_KEY_PROVIDER_AUTHORIZED=NO

STORE_INTERNAL_ARCHITECTURE_COMPLETE=YES
OFFLINE_STORE_SUBSTRATE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO

AT8M2_TEST_WRITABLE_PATHS=
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
  tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py

PRODUCTION_RUNTIME_READY=NO
LIVE_CREDENTIAL_USE_READY=NO
LIVE_HIGHLEVEL_EXECUTION_READY=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO

EXTERNAL_EFFECTS=0
```

STOP for architecture review.
