# NW-008 AT-8M — Production Runtime Substrate and Execution Store Authority Design 001

```text
UNIT=NW008_AT8M_PRODUCTION_RUNTIME_SUBSTRATE_AND_EXECUTION_STORE_AUTHORITY_DESIGN_001
PR_CLASS=planning_only
PHASE=PLANNING_ONLY
MODE=READ_ONLY_ARCHITECTURE_DECISION
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=nw008-at8m-production-runtime-substrate-and-execution-store-authority-design-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=642ee4e8edb2c9b63beaec10717c237457e948bd
PLAN_HEAD_AT_START=642ee4e8edb2c9b63beaec10717c237457e948bd

PR121_MERGED=YES
PR121_MERGE_SHA=642ee4e8edb2c9b63beaec10717c237457e948bd
PR121_MERGE_VERIFIED=YES

RUNTIME_COMPOSITION_ROOT_IMPLEMENTED=YES
COMPOSITION_ROOT_CAPABILITY_PROVENANCE_ENFORCED=YES

PRODUCTION_RUNTIME_READY=NO
CONCRETE_RUNTIME_SECRET_ACCESSOR_IMPLEMENTED=NO
PRODUCTION_EXECUTION_STORE_CONSTRUCTION_IMPLEMENTED=NO

PR120_AUTHORIZATION_CONSUMED=YES
PR120_AUTHORIZATION_REUSABLE=NO
PR120_AUTHORIZATION_REUSED_BY_THIS_UNIT=NO

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
PREFLIGHT_BRANCH_AT_START=nw008-at8l-live-note-runtime-implementation-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_ORIGIN_MAIN_SHA=642ee4e8edb2c9b63beaec10717c237457e948bd
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_UNTRACKED_FILES=0
PREFLIGHT_RECORDED_AT_LOCAL=2026-08-21T14:13:48-0400
```

Abort conditions did not fire after hygiene resolution: the starting branch was
not `main`; no unrelated changes existed; the only worktree modifications were
the five known AT10 test-generated files.

## Local hygiene resolution

At first receipt of this unit, local cleanup authority had not been granted, so
the unit stopped with `LOCAL_HYGIENE_BLOCKED=YES` without altering any state.
Cleanup authority was then separately granted by VS_CODE_ORCHESTRATOR, scoped
only to the five identified tracked AT10 test-generated files and only to local
worktree cleanup.

The five files were confirmed to be only local test-generated modifications
before restore:

- the committed `origin/main` versions hold the merged bounded Firestore
  acceptance-demo evidence;
- the working-tree versions were offline regenerations produced by
  `src/mg_guide/firestore_audit/acceptance_demo.py` (exercised by
  `tests/test_nw008_at10_acceptance_demo.py`) with `NETWORK_CALLS=0` /
  `EXTERNAL_EFFECTS=0`;
- the working-tree blobs additionally remain recoverable from session-history
  commits, so the restore discarded nothing irrecoverable.

Executed hygiene (grant-scoped, nothing else altered):

```text
AT10_TEST_GENERATED_FILES_RESTORED_TO_ORIGIN_MAIN=5
RESTORE_SCOPE=proof/nw008/at-10/acceptance-demo/ (five tracked files only)
RESTORE_SOURCE=origin/main
WORKTREE_CLEAN_AFTER_RESTORE=YES
GIT_ADD_ALL_USED=NO
OTHER_FILES_BRANCHES_STATE_ALTERED=NO
```

The AT8M artifact branch was created only after the clean-worktree verification,
from fresh `origin/main` at the PR121 merge SHA.

## Non-actions

```text
SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0
LIVE_NOTE_RUNTIME_MUTATIONS=0
AT1_EXECUTION_STORE_MUTATIONS=0
CREDENTIAL_PROVIDER_MUTATIONS=0
SECRET_MANAGER_INVOCATIONS=0
MG_GUIDE_PIT_GHL_READS=0
SERVICE_ACCOUNT_IMPERSONATION=0
SERVICE_ACCOUNT_ATTACHMENT=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0

REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
GCP_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0

AT8M_AUTHORIZATION_CREATED=NO
AT8N_AUTHORIZATION_CREATED=NO
```

Read-only sources consulted:

- `src/integrations/ghl/highlevel_rest/live_note_runtime.py` (AT8L composition root)
- `src/integrations/ghl/at1_execution_store.py` (store surface and schema)
- `src/integrations/ghl/highlevel_rest/live_note_credential_provider.py`
  (`LiveNoteSecretAccessor` protocol, `read_secret_payload`)
- `docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md`
- `docs/nw008/nw-008-at8k1-ghl-rest-production-runtime-principal-design-001.md`
- `docs/nw008/nw-008-at8l-ghl-rest-live-note-runtime-construction-path-implementation-001.md`
- `proof/nw008/at-8l/nw008-at8l-ghl-rest-live-note-runtime-construction-path-implementation-consumption-001.md`

This unit resolves architecture questions only. It does not implement
production store construction, does not create any authorization artifact, and
does not modify runtime, store, credential, manifest, IAM, or deployment state.

## Source state carried forward

From AT8L (merged PR121): `assemble_bound_live_note_runtime` accepts only
`verified_capability`, validates it via
`note_path._require_issued_verified_capability`, and fails closed
(`LiveNoteRuntimeAssemblyError`) because no root-owned production execution
store construction exists. The private deterministic seam
`_assemble_bound_live_note_runtime_for_tests` injects only
`SyntheticLiveNoteSecretAccessor` and an `At1ExecutionStore`. AT8L deterministic
evidence confirmed: no public production execution-store argument, no caller
resource/token/credential/http-client overrides, capability remint forbidden.

From AT8K/AT8K1: `PRODUCTION_RUNTIME_PLATFORM=UNDECIDED` was the open substrate
question this unit resolves. The production runtime principal is designed (not
created) as
`serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`
with single-secret `roles/secretmanager.secretAccessor` scope on
`projects/831270426395/secrets/MG_GUIDE_PIT_GHL`; no SA was created and no IAM
was applied.

## Architecture question 1 — PRODUCTION_RUNTIME_PLATFORM_CLASS

### Decision

```text
PRODUCTION_RUNTIME_PLATFORM_CLASS=GOVERNED_SINGLE_INSTANCE_LONG_LIVED_LOCAL_PROCESS
PRODUCTION_RUNTIME_PLATFORM_DECIDED=YES
```

The initial production substrate for the bounded live-note runtime is the
governed orchestrator-host lane: a single, long-lived local process under
VS_CODE_ORCHESTRATOR control — the direct production continuation of
`CURRENT_EXECUTION_LANE=VS_CODE_ORCHESTRATOR_LOCAL`. Container/serverless (for
example Cloud Run) and any other governed target are explicitly not selected
for the initial production substrate.

### Rationale

1. The composition root is invoked inside agent-orchestrated workflows driven
   by the orchestrator; no separate service frontend exists for this lane, and
   AT8K recorded that this lane is not the NW-007 Cloud Run judge surface.
2. `At1ExecutionStore` claim semantics (`execution_claims.owner_id`,
   `acquire_claim` / `assert_claim_owner`) are designed for a single owning
   writer; a single-instance process makes single-writer discipline
   enforceable without new infrastructure.
3. The AT8K1 principal decision is platform-independent by design, so selecting
   the local lane now does not invalidate the designed service account or its
   single-secret IAM shape.
4. Selecting serverless now would force an immediate persistence re-decision
   (ephemeral filesystems) and deployment construction that this planning unit
   is not authorized to build.

### Migration constraint

Any later move to a container/serverless/multi-instance target re-opens this
decision and requires a new planning unit plus re-derived persistence model
before any deployment change. The platform class is recorded as a decision with
an explicit re-evaluation gate, not as a permanent commitment.

## Architecture question 2 — EXECUTION_STORE_DURABILITY_REQUIREMENT

### Decision

```text
RECORDS_MUST_SURVIVE_PROCESS_RESTART=YES
RECORDS_MUST_SURVIVE_HOST_REBOOT=YES
RECORDS_MUST_SURVIVE_DEPLOYMENT_REPLACEMENT=NOT_REQUIRED_FOR_INITIAL_SUBSTRATE
MULTI_INSTANCE_CONCURRENCY_REQUIRED=NO
SINGLE_WRITER_ENFORCEMENT_REQUIRED=YES
REPLAY_RECOVERY_REQUIRED=YES
```

1. Restart survival: required. The store is the durable record of grant/run
   claims, attempt state, protocol ledger, and business ledger; losing it on
   restart would break `require_run_continuable` continuation gating and the
   evidence projection (`compute_public_projection` HMAC commitments).
2. Deployment replacement: not required for the initial single-instance local
   substrate (no deployment exists for this lane); the store file must
   nonetheless live on operator-governed durable disk so host-level backup
   practices can apply. This requirement flips to YES together with any future
   container/serverless re-decision.
3. Multi-instance concurrency: not required and actively excluded. Exactly one
   runtime instance may hold the store open for write; the claim table enforces
   ownership within the store, and the platform decision excludes concurrent
   instances.
4. Replay/recovery: required. A crash between `record_attempt`,
   `mark_dispatched`, `capture_response`, and `mark_terminal` must be
   recoverable by re-opening the store and resuming through the existing
   attempt state machine; ledgers are append-only to support audit replay.

## Architecture question 3 — SQLITE_PRODUCTION_SUITABILITY

### Decision

```text
SQLITE_PRODUCTION_SUITABLE=CONDITIONAL
```

SQLite (via the existing `At1ExecutionStore`) is suitable for the initial
production substrate if and only if all of the following conditions hold:

```text
CONDITION_1=single-instance single-writer long-lived process (per Q1 decision)
CONDITION_2=store file on operator-governed durable local disk (not tmpfs, not ephemeral)
CONDITION_3=no second process or instance ever opens the store file for write
CONDITION_4=open/init failure and lock contention fail closed (no silent proceed)
CONDITION_5=retention/cleanup performed only by explicitly authorized maintenance
```

Justification from Q2 requirements: restart/reboot survival and crash recovery
are satisfied by a durable local file with the store's autocommit
(`isolation_level=None`) writes and existing busy timeout (30 s). The
single-writer condition removes SQLite's multi-writer weakness from scope.
Conversely, SQLite is NOT suitable for multi-instance concurrency, networked
filesystems, or ephemeral-filesystem serverless targets; any platform migration
re-decides persistence (managed store selection would be a new planning unit).

## Architecture question 4 — PRODUCTION_DB_PATH_AUTHORITY

### Decision

```text
PRODUCTION_DB_PATH_AUTHORITY_IDENTIFIED=YES
PRODUCTION_DB_PATH_OWNER=RUNTIME_COMPOSITION_ROOT
PRODUCTION_DB_PATH_CONFIGURATION_SOURCE_CLASS=ORCHESTRATOR_GOVERNED_ENVIRONMENT_CONFIGURATION
PRODUCTION_DB_PATH_HARDCODED_IN_SOURCE=FORBIDDEN
CALLER_DB_PATH_OVERRIDE=FORBIDDEN
```

The composition root (`assemble_bound_live_note_runtime`) is the sole owner of
production store construction and therefore the sole resolver of the production
database path. The path is non-secret configuration: the root reads it from
orchestrator-governed environment configuration (a single dedicated
configuration value provisioned by the operator for the governed host), with a
root-owned default location under a governed data directory when the value is
absent. The public assembler signature remains `verified_capability` only
(AT8L freeze); no caller may pass a path, and no absolute path is hardcoded in
source. The exact configuration variable name and default directory are
implementation details frozen by the later implementation authorization, not by
this design.

## Architecture question 5 — PRODUCTION_COMMITMENT_KEY_AUTHORITY

### Decision

```text
PRODUCTION_COMMITMENT_KEY_AUTHORITY_IDENTIFIED=YES
PRODUCTION_COMMITMENT_KEY_CLASS=SECRET_MATERIAL
HARDCODED_PRODUCTION_COMMITMENT_KEY=FORBIDDEN
CALLER_SUPPLIED_PRODUCTION_COMMITMENT_KEY=FORBIDDEN
PRODUCTION_COMMITMENT_KEY_SOURCE_CLASS=GOOGLE_SECRET_MANAGER_VIA_ROOT_OWNED_ACCESSOR
PRODUCTION_COMMITMENT_KEY_READ_IN_THIS_UNIT=0
PRODUCTION_COMMITMENT_KEY_CREATED_IN_THIS_UNIT=0
```

The commitment key keys HMAC-SHA256 evidence commitments
(`At1ExecutionStore._commitment`); possession enables forging evidence
commitments, so it is secret material in full. The intended governed source is
a dedicated Google Secret Manager secret — a distinct resource from
`MG_GUIDE_PIT_GHL` (which is the HighLevel PIT credential and must not be
reused) — read at assembly time only by the composition root through a
root-owned secret accessor implementing the existing `LiveNoteSecretAccessor`
protocol (`read_secret_payload`), authenticating via ADC / workload identity as
the AT8K1-designed single-purpose runtime principal, under single-secret
`roles/secretmanager.secretAccessor` IAM.

This unit does not read, create, name-allocate, or bind the key resource.
Exact resource identity, version pinning, and rotation handling are deferred:
resource creation and IAM are later explicitly authorized units; the concrete
accessor contract is AT8N (below). Rotation constraint recorded for later
units: stored commitments verify only under the key that produced them, so key
rotation requires either per-record key-version pinning or an authorized
re-commitment migration; silent rotation is forbidden.

## Architecture question 6 — PRODUCTION_STORE_LIFECYCLE

### Decision (design only; nothing implemented)

```text
INITIALIZATION=composition root constructs At1ExecutionStore at assembly;
  root ensures the governed parent directory exists with restrictive
  permissions; existing idempotent CREATE TABLE IF NOT EXISTS bootstrap applies
MIGRATION_VERSIONING=current store carries no schema version; a root-owned
  schema_version marker with forward-only, root-applied migrations is a
  required precondition of the production store-construction implementation
  authorization; no ad-hoc DDL outside the root
RETENTION=retain-all for the bounded evidence lane; records are evidence;
  no automatic deletion in the production path; any retention limit is a
  separate governance decision
CLEANUP=cleanup seams remain test-only (synthetic stores); production cleanup
  occurs only under an explicit authorized maintenance action
RESTART_RECOVERY=re-open the existing store file; claims and attempt state
  resume through the existing state machine; require_run_continuable gates runs
  with unresolved prior attempts; ledgers remain append-only
FAILURE_MODE=fail closed: store open/init/migration failure aborts assembly
  through the composition-root error path; SQLITE_BUSY / lock contention fails
  closed; the runtime must never proceed without durable state
```

## Architecture question 7 — RUNTIME_IDENTITY_DEPENDENCY

### Decision

```text
STORE_DB_PATH_DEPENDS_ON_RUNTIME_PLATFORM_IDENTITY=NO
STORE_COMMITMENT_KEY_ACCESS_DEPENDS_ON_RUNTIME_PLATFORM_IDENTITY=YES
RUNTIME_PRINCIPAL_FOR_KEY_ACCESS=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com (designed, not created)
SERVICE_ACCOUNT_ATTACHED_BY_THIS_UNIT=NO
```

The database path is platform configuration and does not vary with runtime
identity. Commitment-key access, however, is bound to the runtime platform
identity: the AT8K1-designed single-purpose service account is the identity
class that will hold single-secret accessor rights on the commitment-key
secret, and the accessor must authenticate via ADC / workload identity only (SA
keys forbidden, per AT8K1 forbidden practices). This unit attaches no service
account to any resource and applies no IAM; binding remains a later authorized
lane exactly as AT8K1 designed.

## Derived fields

```text
PRODUCTION_RUNTIME_PLATFORM_DECIDED=YES
PRODUCTION_PERSISTENCE_MODEL_DECIDED=YES
SQLITE_PRODUCTION_SUITABLE=CONDITIONAL

PRODUCTION_DB_PATH_AUTHORITY_IDENTIFIED=YES
PRODUCTION_COMMITMENT_KEY_AUTHORITY_IDENTIFIED=YES

HARDCODED_PRODUCTION_COMMITMENT_KEY=FORBIDDEN
CALLER_SUPPLIED_PRODUCTION_COMMITMENT_KEY=FORBIDDEN

PRODUCTION_STORE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
```

Persistence model: embedded SQLite via `At1ExecutionStore` on governed durable
local disk under single-writer discipline, as decided in Q1–Q3.

`PRODUCTION_STORE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES` means a later,
separate, one-shot offline implementation authorization for root-owned
production execution-store construction can now be drafted. It must be
conditioned on: (a) this design merged on `main`; (b) the AT8N accessor
contract freeze (parallel planning unit below) or an equivalent root-owned
accessor seam for commitment-key delivery; (c) no real secret payload reads
during implementation; (d) no live transport execution. It does not authorize
secret resource creation, IAM, deployment, or live CRM mutation, and it does
not reuse PR120 authority (consumed; not reusable).

## Next parallel planning unit

```text
NEXT_PARALLEL_PLANNING_UNIT=NW008_AT8N_CONCRETE_SECRET_MANAGER_ACCESSOR_DESIGN_001
NEXT_PR_CLASS=planning_only
NEXT_MODE=READ_ONLY_ARCHITECTURE_DECISION
AT8N_PLANNING_RECOMMENDED=YES
```

AT8N must be PLANNING_ONLY initially. Its design must later freeze:

- `GoogleSecretManagerLiveNoteSecretAccessor` exact contract (implementing the
  existing `LiveNoteSecretAccessor` protocol `read_secret_payload`);
- ADC / workload identity only;
- exact `MG_GUIDE_PIT_GHL` resource identity
  (`projects/831270426395/secrets/MG_GUIDE_PIT_GHL`);
- caller resource override forbidden;
- environment token discovery forbidden;
- gcloud / shell secret retrieval forbidden;
- service-account keys forbidden;
- payload / token logging forbidden;
- retry policy;
- dependency / package change requirements;
- zero real payload reads during implementation;
- runtime principal attachment remains separate.

AT8N covers the accessor contract in general; its application to the
commitment-key secret (Q5) inherits the same freeze list, with the
commitment-key resource identity itself allocated only under a later explicitly
authorized unit.

## Non-authority

```text
AT8M_AUTHORIZES_IMPLEMENTATION=NO
AT8M_AUTHORIZES_PRODUCTION_STORE_CONSTRUCTION=NO
AT8M_AUTHORIZES_SECRET_RESOURCE_CREATION=NO
AT8M_AUTHORIZES_SECRET_PAYLOAD_READ=NO
AT8M_AUTHORIZES_IAM_CHANGE=NO
AT8M_AUTHORIZES_SERVICE_ACCOUNT_ATTACHMENT=NO
AT8M_AUTHORIZES_DEPLOYMENT_CHANGE=NO
AT8M_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8M_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8M_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8M_CREATES_AT8N_AUTHORIZATION=NO
AT8M_REUSES_PR120_AUTHORIZATION=NO
```

## Validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001
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
AT8M_PLANNING_COMPLETE=YES

PRODUCTION_RUNTIME_PLATFORM_DECIDED=YES
PRODUCTION_PERSISTENCE_MODEL_DECIDED=YES
SQLITE_PRODUCTION_SUITABLE=CONDITIONAL

PRODUCTION_DB_PATH_AUTHORITY_IDENTIFIED=YES
PRODUCTION_COMMITMENT_KEY_AUTHORITY_IDENTIFIED=YES

PRODUCTION_STORE_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES

AT8N_PLANNING_RECOMMENDED=YES

EXTERNAL_EFFECTS=0
```

STOP for architecture review.
