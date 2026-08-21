# NW-008 AT-8M2R1 — Offline Execution Store Failed-Initialization Reopen Repair Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8M2R1_OFFLINE_EXECUTION_STORE_FAILED_INIT_REOPEN_REPAIR_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-authorization-001.md
AUTHORIZATION_BRANCH=nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-authorization-001

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE

GRANT=OFFLINE_DETERMINISTIC_EXECUTION_STORE_FAILED_INIT_REOPEN_REPAIR
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
AUTHORIZATION_EFFECTIVE=NO
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8M2R1_OFFLINE_EXECUTION_STORE_FAILED_INIT_REOPEN_REPAIR_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_PATH=proof/nw008/at-8m2r1/nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-consumption-001.md

IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does **not** modify `At1ExecutionStore`, does not modify tests, does not
create or change a provider, does not read secret payload, does not call
HighLevel, does not mutate CRM, does not change IAM/GCP, does not deploy, and
does not authorize live mutation or production runtime activation.

AT8M2R1 itself is `AUTHORIZATION_ARTIFACT_ONLY`. It authorizes a later,
separately reviewed, offline deterministic repair consumer only after merge and
independent merge/blob verification. It must not implement anything in this
authorization PR.

## 2. Prior-authority consumption and PR125 repair target

```text
PR125=125
PR125_STATE_AT_AUTHORIZATION_AUTHORING=OPEN
PR125_TITLE=feat(nw008-at8m2): implement offline execution-store substrate
PR125_REVIEWED_HEAD=6d2fd608f134f0d1a29131e4303978f568a4fd3d
PR125_REVIEWED_HEAD_MATCH=YES
PR125_FORMAL_VERDICT=CHANGE_REQUEST
PR125_MERGED=NO

PR124_AUTHORIZATION_PR=124
PR124_AUTHORIZATION_MERGE_SHA=a02784ada82d1bc7b29ad2065d747f02690b456f
PR124_AUTHORIZATION_REVIEWED_HEAD=44464d4fdb564e73a86d9a6af8bde054cef43546
PR124_AUTHORIZATION_CONSUMED=YES
PR124_AUTHORIZATION_REUSABLE=NO
PR124_RETRY_AFTER_CONSUMPTION_REQUIRES_NEW_AUTHORIZATION=YES

PR125_CONSUMPTION_RECORD_PATH=proof/nw008/at-8m2/nw008-at8m2-offline-execution-store-substrate-implementation-consumption-001.md
PR125_RECORDED_AUTHORIZATION_CONSUMED=YES
```

The formal `CHANGE_REQUEST` disposition is supplied by the human owner for
PR125. GitHub currently reports PR125 as open at the reviewed head above; no
GitHub merge has occurred.

PR124's authority was consumed by the first committed mutation to an authorized
consumer source/test path on the PR125 reviewed head. It is non-reusable. The
PR125 failure therefore cannot be retried, amended, or repaired under PR124;
this distinct AT8M2R1 authorization is required.

This grant does not approve, merge, or reactivate PR125. It only proposes a
new, bounded future repair permission after AT8M2R1 merge.

## 3. Pre-flight and source verification

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_REF=origin/main
PREFLIGHT_BASE_SHA=a02784ada82d1bc7b29ad2065d747f02690b456f
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_UNTRACKED_FILES_BEFORE_ARTIFACT=0

PR124_MERGED=YES
PR124_MERGE_SHA=a02784ada82d1bc7b29ad2065d747f02690b456f
PR124_REVIEWED_HEAD=44464d4fdb564e73a86d9a6af8bde054cef43546
PR124_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES
```

The authorization branch begins at fresh `origin/main` after PR124 merge.
Pre-flight abort conditions did not fire: the branch is not `main` and there
were no unrelated worktree changes.

Read-only PR125 review-target checks:

```text
PR125_GITHUB_STATE=OPEN
PR125_GITHUB_HEAD_REF_OID=6d2fd608f134f0d1a29131e4303978f568a4fd3d
PR125_GITHUB_MERGE_COMMIT=NONE
PR125_REVIEWED_HEAD_MATCH=YES
```

## 4. Repair contract (normative)

```text
FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED
ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
```

### 4.1 Required distinction

A future consumer must distinguish a path that did **not** exist before store
open from an already-existing empty SQLite artifact:

1. a **fresh non-existent** store path may initialize schema and metadata;
2. an existing artifact left after failed initialization must fail closed on
   reopen, even if it currently contains no user tables;
3. any preexisting empty store artifact must fail closed; it must not be treated
   as a fresh initialization target;
4. partial schema and legacy unversioned stores must fail closed.

The repair must not infer authorization to erase, replace, auto-migrate, or
otherwise make an existing artifact acceptable. Exact SQLite mechanics for
determining preexistence and preserving failure state are implementation details,
provided all fields above hold.

### 4.2 Atomicity remains mandatory

```text
ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
```

Schema tables and authoritative metadata must form one valid initialization
boundary. A failed or interrupted initialization must not produce an artifact
that a subsequent open accepts. A rollback to an empty but preexisting SQLite
file is **not** a fresh non-existent store and must fail closed.

## 5. Future consumer ancestry and bounded baseline

The future repair consumer must independently verify the merged AT8M2R1
authorization before writing any authorized consumer source/test path.

```text
CONSUMER_BRANCH_MUST_DESCEND_FROM_AUTHORIZATION_MERGE_SHA=YES
AUTHORIZATION_ARTIFACT_BLOB_SHA_MUST_MATCH_REVIEWED_MERGED_BLOB=YES

REPAIR_CONSUMER_MUST_INCLUDE_PR125_REVIEWED_HEAD=YES
PR125_REVIEWED_HEAD=6d2fd608f134f0d1a29131e4303978f568a4fd3d
PR125_BASELINE_MUST_REMAIN_UNMODIFIED_OUTSIDE_AT8M2R1_WRITABLE_SCOPE=YES
```

The PR125 reviewed head is the failed implementation baseline, not a grant to
modify arbitrary PR125 paths. The repair consumer must include that reviewed
head and the merged authorization in its ancestry, while changing only the
AT8M2R1 writable paths below.

Before the first authorized source/test mutation, record:

```text
AUTHORIZATION_PR=<future number>
AUTHORIZATION_REVIEWED_HEAD=<future SHA>
AUTHORIZATION_MERGE_SHA=<future SHA>
AUTHORIZATION_ARTIFACT_BLOB_SHA=<future SHA>
PR125_REVIEWED_HEAD=6d2fd608f134f0d1a29131e4303978f568a4fd3d
```

## 6. One-shot consumption (normative)

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

This is a new, independently consumed one-shot grant. Its first committed
mutation to an authorized future consumer source/test path consumes it. Partial,
failed, or abandoned work after that event does not restore authority.

## 7. Authoring versus future consumer writable scope

These scopes are disjoint. Authorization authoring must not write consumer
implementation files. The implementation consumer must not rewrite this
authorization artifact.

### 7.1 Authorization PR writable scope

```text
AUTHORIZATION_PR_WRITABLE_SCOPE=
  governance/authorizations/nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-authorization-001.md
```

No other path is writable in this authorization PR.

### 7.2 Authorized future consumer writable scope (exact)

```text
AUTHORIZED_SOURCE_PATHS=
  src/integrations/ghl/at1_execution_store.py

AUTHORIZED_TEST_PATHS=
  tests/integrations/ghl/test_at1_commitment_key_provider.py

AUTHORIZED_PROOF_PATHS=
  proof/nw008/at-8m2r1/**

AUTHORIZED_DOC_PATH_EXACT=
  docs/nw008/nw-008-at8m2r1-failed-init-reopen-repair-001.md
```

The paths above are the **minimum and maximum** writable consumer scope for this
grant. No other source/test/doc path is authorized.

### 7.3 Optional provider hardening explicitly excluded

```text
OPTIONAL_PROVIDER_HARDENING_HUMAN_SCOPE_INCLUDED=NO
SYNTHETIC_PROVIDER_PAYLOAD_SERIALIZATION=NOT_AUTHORIZED_BY_THIS_GRANT
src/integrations/ghl/at1_commitment_key_provider.py=BLOCKED
```

Provider serialization refusal was not explicitly included by a human scope
decision for this authorization. It is therefore not authorized implicitly.
Any future provider hardening requires a separate explicit human-scoped
authorization that adds exactly
`src/integrations/ghl/at1_commitment_key_provider.py` and freezes
`SYNTHETIC_PROVIDER_PAYLOAD_SERIALIZATION=FORBIDDEN`.

### 7.4 Blocked paths and surfaces

```text
src/**=BLOCKED_EXCEPT_src/integrations/ghl/at1_execution_store.py
tests/**=BLOCKED_EXCEPT_tests/integrations/ghl/test_at1_commitment_key_provider.py

src/integrations/ghl/at1_commitment_key_provider.py=BLOCKED
src/integrations/ghl/__init__.py=BLOCKED
src/integrations/ghl/highlevel_rest/**=BLOCKED
tests/integrations/ghl/test_at1_live_transport_remediation.py=BLOCKED
tests/integrations/ghl/highlevel_rest/**=BLOCKED

governance/authorizations/**=BLOCKED_EXCEPT_THIS_ARTIFACT_ALREADY_MERGED
docs/nw008/**=BLOCKED_EXCEPT_docs/nw008/nw-008-at8m2r1-failed-init-reopen-repair-001.md
proof/nw008/**=BLOCKED_EXCEPT_proof/nw008/at-8m2r1/**

requirements.txt=BLOCKED
pyproject.toml=BLOCKED
Dockerfile=BLOCKED
.github/**=BLOCKED
```

```text
IAM=BLOCKED
SECRET_MANAGER=BLOCKED
REAL_SECRET_READS=BLOCKED
SERVICE_ACCOUNT_MUTATION=BLOCKED
HIGHLEVEL=BLOCKED
CRM_MUTATION=BLOCKED
DEPLOYMENT=BLOCKED
PRODUCTION_RUNTIME_ACTIVATION=BLOCKED
PACKAGE_DEPENDENCY_CHANGES=BLOCKED
```

## 8. Required future deterministic proof

The consumer must produce offline deterministic proof at least for:

```text
REQUIRED_REPAIR_PROOFS=
  - fresh non-existent store initialization is allowed
  - schema and metadata initialize atomically
  - failed-initialization artifact reopen fails closed
  - preexisting empty store open fails closed
  - partial schema initialization fails closed
  - legacy unversioned store open fails closed
  - no real Secret Manager access
  - zero external effects
```

The repair is limited to the failed-initialization reopen distinction. It does
not reopen AT8M2 commitment-material/provider contracts, schema-version policy,
or any live-runtime authority.

## 9. Explicit non-authority

```text
AT8M2R1_AUTHORIZATION_IMPLEMENTS_CODE=NO
AT8M2R1_AUTHORIZATION_PR_WRITES_SRC=NO
AT8M2R1_AUTHORIZATION_PR_WRITES_TESTS=NO

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
PRODUCTION_COMPOSITION_ROOT_STORE_WIRING=FORBIDDEN
PACKAGE_MANIFEST_MUTATION=FORBIDDEN
DEPENDENCY_MANIFEST_MUTATION=FORBIDDEN
PR120_AUTHORITY_REUSE=FORBIDDEN
AT8K2_AUTHORITY_REUSE=FORBIDDEN

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

## 10. Authorization PR validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=governance/authorizations/nw008-at8m2r1-offline-execution-store-failed-init-reopen-repair-authorization-001.md
SRC_CHANGES=0
TEST_CHANGES=0
IAM_CHANGES=0
SECRET_CHANGES=0
DEPLOYMENT_CHANGES=0
IMPLEMENTATION_CHANGE=NO
EXTERNAL_EFFECTS=0
```

Required validation:

```text
git diff --name-status origin/main...HEAD
git diff --check origin/main...HEAD
```

The branch diff must list exactly this one authorization artifact.

## 11. Return

```text
AT8M2R1_AUTHORIZATION_CREATED=YES
AT8M2R1_AUTHORIZATION_PR_CLASS=authorization
AT8M2R1_MODE=AUTHORIZATION_ARTIFACT_ONLY
AT8M2R1_IMPLEMENTATION_PERFORMED=NO

FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED
ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED

AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

OPTIONAL_PROVIDER_HARDENING_HUMAN_SCOPE_INCLUDED=NO
SYNTHETIC_PROVIDER_PAYLOAD_SERIALIZATION=NOT_AUTHORIZED_BY_THIS_GRANT

EXTERNAL_EFFECTS=0
```

STOP for formal authorization-PR review.
Do not implement repair.
