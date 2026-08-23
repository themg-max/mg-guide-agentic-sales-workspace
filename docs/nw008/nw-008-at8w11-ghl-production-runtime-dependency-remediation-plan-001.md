# NW-008 AT8W11 GHL Production Runtime Dependency Remediation Plan 001

## 1. Unit identity and planning-only boundary

```text
UNIT=NW008_AT8W11_GHL_PRODUCTION_RUNTIME_DEPENDENCY_REMEDIATION_PLAN_001
PR_CLASS=planning_only
MODE=READ_ONLY_PRODUCTION_RUNTIME_REMEDIATION_PLANNING
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=
  nw008-at8w11-ghl-production-runtime-dependency-remediation-plan-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=
  24f127f219225f08b954652f5ba64122f0d98baa
PLAN_ARTIFACT=
  docs/nw008/nw-008-at8w11-ghl-production-runtime-dependency-remediation-plan-001.md

PLANNING_ONLY=YES
IMPLEMENTATION_PERFORMED=NO
RUNTIME_SOURCE_CHANGES=0
TEST_CHANGES=0
AUTHORIZATION_ARTIFACT_CREATED=NO
IMPLEMENTATION_AUTHORIZATION_CREATED=NO
LIVE_EXECUTION_AUTHORITY_CREATED=NO
EXTERNAL_EFFECTS=0
```

This unit is read-only production-runtime dependency remediation planning. It
determines exactly what remains between the merged AT8W10 failed-closed state
and `LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=YES`. It does not implement code,
apply IAM, mutate secrets or ADC, call HighLevel, read secret payloads, deploy,
change production configuration, claim or consume AT8W9, or retry AT8W10.

```text
MERGING_THIS_PLAN_CONFERS_IMPLEMENTATION_AUTHORITY=NO
MERGING_THIS_PLAN_CONFERS_LIVE_EXECUTION_AUTHORITY=NO
MERGING_THIS_PLAN_CREATES_AT8W12_AUTHORIZATION=NO
AT8W9_REUSE=FORBIDDEN
AT8W10_RETRY=FORBIDDEN
SUCCESSOR_LIVE_EXECUTION_REQUIRES_FRESH_ONE_SHOT_AUTHORIZATION=YES
```

## 2. Pre-flight and abort conditions

```text
PRE_FLIGHT=
  pwd|
  git branch --show-current|
  git status --short --untracked-files=all|
  git fetch origin

WORKING_DIRECTORY=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH_AT_PRE_FLIGHT=
  nw008-at8w10-ghl-one-shot-live-note-execution-proof-001
BRANCH_IS_MAIN=NO
UNEXPECTED_DIRTY_WORKTREE=NO
DIRTY_PATH_COUNT=0
ORIGIN_FETCHED=YES

ABORT_IF=
  branch_is_main|
  unexpected_dirty_worktree

ABORT_TRIGGERED=NO
```

Pre-flight completed cleanly. The worktree was clean, the active branch was not
`main`, and `origin` was fetched before verification and branch creation. The
planning branch was then created from the exact verified `origin/main` tip at
the AT8W10 merge commit.

## 3. PR176 / AT8W10 predecessor verification

```text
PR176=176
PR176_URL=
  https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/176
PR176_TITLE=proof(nw008): close AT8W10 failed-closed pre-consumption
PR176_STATE=MERGED
PR176_HUMAN_MERGED=YES
PR176_MERGED_AT=2026-08-23T17:37:26Z
PR176_BASE_REF=main
PR176_HEAD_REF=
  nw008-at8w10-ghl-one-shot-live-note-execution-proof-001

PR176_REVIEWED_HEAD=
  46c032ae2025d7dc9a34774bf472cf87ee0d9688
PR176_ACTUAL_MERGE_COMMIT=
  24f127f219225f08b954652f5ba64122f0d98baa

PR176_MERGE_PARENTS=
  92006b68855877bedf96079e897516ab1096515a
  46c032ae2025d7dc9a34774bf472cf87ee0d9688

PR176_SECOND_PARENT_IS_REVIEWED_HEAD=YES
PR176_REVIEWED_HEAD_ANCESTRY_VERIFIED=YES
PR176_MERGE_COMMIT_ON_ORIGIN_MAIN=YES
PR176_MERGE_COMMIT_EQUALS_ORIGIN_MAIN_AT_PLAN_BASE=YES

AT8W10_PROOF=
  proof/nw008/at-8w10/nw008-at8w10-ghl-one-shot-live-note-execution-proof-001.md
AT8W10_PROOF_PRESENT_ON_ORIGIN_MAIN=YES

VERIFY_BEFORE_WRITE=
  PR176_STATE=MERGED|
  PR176_MERGE_COMMIT_ON_ORIGIN_MAIN=YES|
  PR176_REVIEWED_HEAD_ANCESTRY_VERIFIED=YES|
  AT8W10_PROOF_PRESENT_ON_ORIGIN_MAIN=YES

VERIFY_PR176_STATE_MERGED=PASS
VERIFY_PR176_REVIEWED_HEAD_EXACT=PASS
VERIFY_PR176_MERGE_COMMIT_EXACT=PASS
VERIFY_PR176_REVIEWED_HEAD_ANCESTRY=PASS
VERIFY_PR176_MERGE_COMMIT_ON_ORIGIN_MAIN=PASS
VERIFY_AT8W10_PROOF_ON_ORIGIN_MAIN=PASS
```

GitHub reports PR176 as human-merged to `main` with reviewed head
`46c032ae2025d7dc9a34774bf472cf87ee0d9688` and merge commit
`24f127f219225f08b954652f5ba64122f0d98baa`. Local post-fetch verification
confirms the reviewed head is the second parent and an ancestor of the merge
commit, the merge commit is on `origin/main`, `origin/main` equals that merge
commit at plan-base time, and the AT8W10 proof is present on `origin/main`.

### 3.1 AT8W10 preserved disposition

```text
AT8W10_RESULT=FAILED_CLOSED_PRE_CONSUMPTION
AT8W10_STOP_REASON=ROOT_OWNED_PRODUCTION_RUNTIME_DEPENDENCIES_UNAVAILABLE
AT8W10_CLOSED=YES
AT8W10_RETRY=FORBIDDEN
DO_NOT_RETRY_AT8W10=YES

AT8W9_AUTHORIZATION_ARTIFACT_ON_MAIN=YES
AT8W9_AUTHORIZATION_CLAIMED=NO
AT8W9_AUTHORIZATION_CONSUMED=NO
AT8W10_CONSUMPTION_RECORD_CREATED=NO
UNUSED_ALLOWANCE_TRANSFER=NO

AT8W10_POST_ATTEMPTS=0
AT8W10_GET_ATTEMPTS=0
AT8W10_NETWORK_CALLS=0
AT8W10_HIGHLEVEL_CALLS=0
AT8W10_CRM_MUTATIONS=0
AT8W10_SECRET_PAYLOAD_READS=0
AT8W10_EXTERNAL_EFFECTS=0
```

AT8W10 is closed. This plan does not reopen it, transfer unused AT8W9 allowance,
or treat unclaimed AT8W9 as standing authority.

## 4. Scope: preserved gates and open gates

### 4.1 Preserved PASS gates (do not reopen)

```text
PRESERVE=
  A0_PRIVATE_BINDING_SOURCE_READINESS=PASS|
  A1_PRIVATE_BINDING_DELIVERY=PASS|
  B1_ROOT_OWNED_CREDENTIAL_INJECTION_SEAM=PASS|
  C1_COMPOSITION_ROOT_SHAPE_IMPLEMENTED=PASS|
  D_BOUNDED_TRANSPORT=PASS

DO_NOT_REOPEN=
  A0|
  A1|
  B1|
  C1|
  D
```

These gates remain PASS from the merged AT8W5/AT8W7/AT8W8/AT8W10 lineage.
AT8W11 does not re-litigate private-binding source readiness, private-binding
delivery, the sealed credential-injection seam shape, the composition-root
public shape, or the frozen bounded transport budget.

### 4.2 Open gates to reconcile

```text
RECONCILE=
  B2_CONCRETE_PRODUCTION_SECRET_ACCESSOR_READY|
  C2_ROOT_OWNED_RUNTIME_DEPENDENCY_RESOLUTION_READY|
  C3_PRODUCTION_EXECUTION_STORE_CONSTRUCTION_READY|
  C4_PRODUCTION_COMMITMENT_KEY_PROVIDER_READY|
  RUNTIME_IDENTITY_CHAIN_READY
```

### 4.3 Aggregate starting state (from merged AT8W10)

```text
LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=NO
AT8W10_STARTING_GATE_MAP=
  A0=PASS A1=PASS B1=PASS B2=NO
  C1=PASS C2=NO C3=NO C4=NO
  D=PASS
  RUNTIME_IDENTITY_CHAIN_READY=UNKNOWN
```

## 5. Read-only evidence base

Durable planning/proof sources (merged on `origin/main`):

- `proof/nw008/at-8w10/nw008-at8w10-ghl-one-shot-live-note-execution-proof-001.md`
- `governance/authorizations/nw008-at8w9-ghl-one-shot-live-note-execution-authorization-001.md`
- `docs/nw008/nw-008-at8w8-ghl-pre-network-readiness-reconciliation-001.md`
- `docs/nw008/nw-008-at8m-production-runtime-substrate-and-execution-store-authority-design-001.md`
- `docs/nw008/nw-008-at8m1-execution-store-schema-and-commitment-key-versioning-design-001.md`
- `docs/nw008/nw-008-at8m2-offline-execution-store-substrate-implementation-001.md`
- `docs/nw008/nw-008-at8o-production-runtime-identity-mechanism-design-001.md`
- `docs/nw008/nw-008-at8k1-ghl-rest-production-runtime-principal-design-001.md`
- `docs/nw008/nw-008-post-at8k2-execution-boundary-reinspection-001.md`
- `proof/nw008/at-8k2/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-consumption-001.md`

Merged runtime targets inspected read-only (no edits in AT8W11):

- `src/integrations/ghl/highlevel_rest/live_note_runtime.py`
- `src/integrations/ghl/highlevel_rest/live_note_credential_provider.py`
- `src/integrations/ghl/at1_execution_store.py`
- `src/integrations/ghl/at1_commitment_key_provider.py`
- `src/integrations/ghl/highlevel_rest/live_note_transport.py`

```text
SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0
SECRET_MANAGER_INVOCATIONS=0
SECRET_PAYLOAD_READS=0
IAM_CHANGES=0
ADC_MUTATIONS=0
DEPLOYMENTS=0
PRODUCTION_CONFIGURATION_MUTATIONS=0
```

## 6. Gate-by-gate reconciliation

Each open gate records current result, gap class, evidence, smallest next
action, authority required, and whether implementation is required.

### 6.1 Gate B2 — concrete production secret accessor ready

```text
GATE_ID=B2_CONCRETE_PRODUCTION_SECRET_ACCESSOR_READY
CURRENT_RESULT=NO
GAP_CLASS=CODE_GAP

EVIDENCE=
  live_note_credential_provider.py exposes LiveNoteSecretAccessor protocol +
  SyntheticLiveNoteSecretAccessor only;
  LiveNoteCredentialProvider.CONCRETE_SECRET_MANAGER_NETWORK_CLIENT=False;
  REAL_SECRET_READS_AUTHORIZED=False;
  no concrete production Secret Manager accessor class exists in merged source;
  AT8I deliberately excluded google-cloud-secretmanager wiring;
  requirements.txt has no google-cloud-secretmanager dependency.

SMALLEST_NEXT_ACTION=
  Authorize and implement one root-owned concrete production secret accessor
  that satisfies LiveNoteSecretAccessor, binds only to the sealed GHL PIT
  resource identity, and is constructible solely by the composition root under
  the selected runtime identity chain. Implementation must not enable payload
  reads outside authorized production assembly.

AUTHORITY_REQUIRED=
  Fresh one-shot offline implementation authorization for concrete production
  secret-accessor code (+ dependency wiring if required). Separate later
  authority is required before any real payload read.

IMPLEMENTATION_REQUIRED=YES
```

B1 remains PASS and is not reopened. B2 is the missing concrete accessor behind
the already-sealed injection seam.

### 6.2 Gate C2 — root-owned runtime dependency resolution ready

```text
GATE_ID=C2_ROOT_OWNED_RUNTIME_DEPENDENCY_RESOLUTION_READY
CURRENT_RESULT=NO
GAP_CLASS=CODE_GAP

EVIDENCE=
  live_note_runtime._resolve_root_owned_runtime_dependencies() unconditionally
  raises LiveNoteRuntimeAssemblyError(
    "production live-note runtime assembly requires root-owned dependencies"
  );
  module docstring states production assembly deliberately fails closed until
  root-owned execution-store construction and a concrete secret accessor exist;
  no production dependency graph is resolved today.

SMALLEST_NEXT_ACTION=
  Authorize and implement production body of
  _resolve_root_owned_runtime_dependencies() so it constructs, only inside the
  composition root:
    1) root-owned credential injection using the concrete B2 accessor + sealed
       GHL PIT resource name;
    2) production At1ExecutionStore from C3/C4 resolution;
  and continues to fail closed if any dependency is missing/invalid.
  Public assembler signature remains verified_capability-only.

AUTHORITY_REQUIRED=
  Fresh one-shot offline implementation authorization for production dependency
  resolution inside the existing composition root. Must not add a second
  composition root or caller override seams.

IMPLEMENTATION_REQUIRED=YES
```

C1 remains PASS. C2 is the fail-closed stub that blocks all production assembly.

### 6.3 Gate C3 — production execution-store construction ready

```text
GATE_ID=C3_PRODUCTION_EXECUTION_STORE_CONSTRUCTION_READY
CURRENT_RESULT=NO
GAP_CLASS=CODE_GAP+CONFIG_GAP

EVIDENCE=
  At1ExecutionStore exists as offline SQLite substrate (AT8M2) requiring
  db_path + CommitmentKeyMaterial;
  production assembly does not construct any store;
  only _assemble_bound_live_note_runtime_for_tests accepts an injected store;
  AT8M decided PRODUCTION_DB_PATH_OWNER=RUNTIME_COMPOSITION_ROOT,
  PRODUCTION_DB_PATH_DEFAULT=NONE, MISSING_PRODUCTION_DB_PATH=FAIL_CLOSED,
  CALLER_DB_PATH_OVERRIDE=FORBIDDEN, HARDCODED path FORBIDDEN;
  PRODUCTION_DB_PATH_CONFIGURED is not established on the governed host;
  PRODUCTION_DB_PATH_DURABILITY_VERIFIED is not established.

SMALLEST_NEXT_ACTION=
  1) Read-only resolve/attest the governed durable DB path configuration name
     and host path durability class (not tmpfs/ephemeral) without mutating
     production configuration in this unit.
  2) Authorize and implement root-owned production store construction that
     reads only orchestrator-governed path configuration, fails closed when
     missing, and never accepts caller path override.

AUTHORITY_REQUIRED=
  Private/config attestation or human-governed path designation for the durable
  DB location; then fresh offline implementation authorization for production
  store construction wiring. Path designation must not be performed as an
  unauthorized production-configuration mutation inside a code PR.

IMPLEMENTATION_REQUIRED=YES
```

### 6.4 Gate C4 — production commitment-key provider ready

```text
GATE_ID=C4_PRODUCTION_COMMITMENT_KEY_PROVIDER_READY
CURRENT_RESULT=NO
GAP_CLASS=CODE_GAP+PRIVATE_AUTHORITY_GAP+IAM_GAP

EVIDENCE=
  at1_commitment_key_provider.py provides SyntheticCommitmentKeyProvider only;
  no production Secret Manager commitment-key provider exists;
  AT8M: COMMITMENT_KEY_SECRET_DISTINCT_FROM_MG_GUIDE_PIT_GHL=YES;
  COMMITMENT_KEY_SECRET_RESOURCE_IDENTIFIED=NO;
  COMMITMENT_KEY_SECRET_RESOURCE_CREATED=NO;
  COMMITMENT_KEY_SECRET_IAM_CONFIGURED=NO;
  COMMITMENT_KEY_ACCESS_PRINCIPAL=UNRESOLVED;
  AT8K2_IAM_AUTHORITY_REUSABLE_FOR_COMMITMENT_KEY=NO;
  exact version resource required by validate_version_resource
  (projects/.../secrets/.../versions/N).

SMALLEST_NEXT_ACTION=
  1) Identify commitment-key secret resource + exact numeric version (metadata
     only; no payload read).
  2) Decide/confirm access principal (likely same runtime SA, but unresolved).
  3) Authorize and apply commitment-key secret IAM if needed.
  4) Authorize and implement production commitment-key provider that returns
     provider-resolved CommitmentKeyMaterial with exact version binding.
  5) Wire provider into C2/C3 production store construction only.

AUTHORITY_REQUIRED=
  Private authority / human designation for secret resource + exact version;
  separate IAM authorization if binding absent; separate offline implementation
  authorization for production provider code. AT8K2 grant is consumed and must
  not be reused.

IMPLEMENTATION_REQUIRED=YES
```

### 6.5 Gate RUNTIME_IDENTITY_CHAIN_READY

```text
GATE_ID=RUNTIME_IDENTITY_CHAIN_READY
CURRENT_RESULT=UNKNOWN
GAP_CLASS=PRIVATE_AUTHORITY_GAP+IAM_GAP+CONFIG_GAP

EVIDENCE=
  AT8O selected LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION;
  TARGET_RUNTIME_PRINCIPAL_IDENTIFIED=YES
    serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com;
  AT8K2 created that SA and bound secretAccessor on MG_GUIDE_PIT_GHL only;
  SOURCE_PRINCIPAL_IDENTIFIED=NO / SOURCE_PRINCIPAL=UNRESOLVED;
  TOKEN_CREATOR_BINDING_AUTHORIZATION_DESIGNABLE=NO at AT8O time;
  AUTHORIZED_USER_ADC_REQUIRED=YES;
  GENERIC_IMPLICIT_ADC_CHAIN_FOR_PRODUCTION=FORBIDDEN;
  GOOGLE_APPLICATION_CREDENTIALS_OVERRIDE=FORBIDDEN;
  USER_MANAGED_SERVICE_ACCOUNT_KEY_AS_BASE_CREDENTIAL=FORBIDDEN;
  PRODUCTION_WORKLOAD_PRINCIPAL_ATTACHED=NO;
  AT8W10 left this gate UNKNOWN rather than assumed PASS.

SMALLEST_NEXT_ACTION=
  Read-only resolve, without ADC mutation or impersonation attempts:
    1) SOURCE_PRINCIPAL_PRIVATE_BINDING_READY — exact operator principal
       identity designated for local authorized-user ADC;
    2) AUTHORIZED_USER_ADC_CORRELATION_READY — that principal's ADC is the
       active local base credential class (attest correlation; do not mutate);
    3) TOKEN_CREATOR_BINDING_READY — whether
       roles/iam.serviceAccountTokenCreator from that source principal onto the
       target runtime SA is present; if absent, design IAM apply authorization
       only after source principal is identified.
  Then mark RUNTIME_IDENTITY_CHAIN_READY=PASS only when all three are YES and
  the selected mechanism remains frozen.

AUTHORITY_REQUIRED=
  Human-governance principal designation / private binding attestation;
  possibly fresh one-shot IAM authorization for Token Creator bind;
  no implementation of impersonation code until identity chain is PASS and a
  later implementation authorization exists.

IMPLEMENTATION_REQUIRED=
  CONDITIONAL — identity-chain readiness itself is primarily authority/config/
  IAM; code that performs impersonated credential acquisition is a later
  implementation step gated by this readiness.
```

## 7. Read-only facts to resolve

These facts must be resolved without secret-payload reads, HighLevel calls,
IAM/secret/ADC mutation, or runtime edits. Current disposition uses only merged
public evidence; unresolved items require human/private attestation or
authorized metadata inspection in later units.

| Fact | Current disposition | Gap class | Notes |
| --- | --- | --- | --- |
| `GHL_PIT_SECRET_RESOURCE_IDENTIFIED` | YES (public sealed identity) | ALREADY_READY | Sealed resource `projects/831270426395/secrets/MG_GUIDE_PIT_GHL` is present in merged runtime constant and AT8K2 proof. Identification ≠ payload access. |
| `GHL_PIT_TARGET_PRINCIPAL_IAM_READY` | YES (historical AT8K2) | ALREADY_READY | AT8K2 bound `roles/secretmanager.secretAccessor` for `mg-guide-ghl-note-runtime@...` on that secret only. Reconfirm metadata-only before first production payload use; do not re-apply under consumed AT8K2 authority. |
| `SOURCE_PRINCIPAL_PRIVATE_BINDING_READY` | NO | PRIVATE_AUTHORITY_GAP | AT8O: source principal class known; exact principal unresolved. |
| `AUTHORIZED_USER_ADC_CORRELATION_READY` | UNKNOWN | CONFIG_GAP+PRIVATE_AUTHORITY_GAP | Requires correlation that the designated operator's authorized-user ADC is active locally without mutating ADC. |
| `TOKEN_CREATOR_BINDING_READY` | NO / UNKNOWN | IAM_GAP | Binding not designable until source principal identified; presence not proven on current main evidence. |
| `PRODUCTION_DB_PATH_CONFIGURED` | NO | CONFIG_GAP | AT8M requires orchestrator-governed env configuration; no default; not established as ready. |
| `PRODUCTION_DB_PATH_DURABILITY_VERIFIED` | NO | CONFIG_GAP | Must be operator-governed durable disk (not tmpfs/ephemeral); not yet attested. |
| `COMMITMENT_KEY_SECRET_RESOURCE_IDENTIFIED` | NO | PRIVATE_AUTHORITY_GAP | Distinct from GHL PIT; not identified in merged public evidence. |
| `COMMITMENT_KEY_EXACT_VERSION_IDENTIFIED` | NO | PRIVATE_AUTHORITY_GAP | Store requires exact `.../versions/N` resource string. |
| `COMMITMENT_KEY_IAM_READY` | NO | IAM_GAP | No commitment-key IAM configured; AT8K2 not reusable for this secret. |

```text
READ_ONLY_FACT_READY_COUNT=2
READ_ONLY_FACT_NOT_READY_COUNT=8
FACT_RESOLUTION_PERFORMS_PAYLOAD_READ=NO
FACT_RESOLUTION_PERFORMS_IAM_MUTATION=NO
```

## 8. Blocker matrix

One matrix from AT8W10 failed-closed state to production pre-network ready.

| Blocker ID | Blocks gate(s) | Gap class | Blocking condition | Unblock condition | May proceed in parallel with |
| --- | --- | --- | --- | --- | --- |
| BLK-ID-01 | RUNTIME_IDENTITY_CHAIN_READY | PRIVATE_AUTHORITY_GAP | Exact source principal unresolved | Human designates exact operator principal for local authorized-user ADC | BLK-CK-*, BLK-DB-* (metadata/design only) |
| BLK-ID-02 | RUNTIME_IDENTITY_CHAIN_READY | CONFIG_GAP | ADC correlation to designated principal not attested | Read-only attestation that active authorized-user ADC correlates to designated principal; no ADC mutation | After BLK-ID-01 |
| BLK-ID-03 | RUNTIME_IDENTITY_CHAIN_READY; B2/C2 runtime use | IAM_GAP | Token Creator binding absent or unproven | After source principal known: metadata check; if absent, fresh IAM authorization + apply Token Creator on target SA only | After BLK-ID-01 |
| BLK-B2-01 | B2 | CODE_GAP | No concrete production Secret Manager accessor | Fresh impl auth + implement accessor behind B1 seam | Identity chain design; not live payload use |
| BLK-C2-01 | C2 | CODE_GAP | `_resolve_root_owned_runtime_dependencies` always raises | Fresh impl auth + implement root-owned resolution using B2+C3+C4 | After B2/C3/C4 design freeze; code may land with fail-closed until config ready |
| BLK-C3-01 | C3 | CONFIG_GAP | Production DB path not configured | Governed durable path designated/configured under orchestrator authority | BLK-CK-*, identity facts |
| BLK-C3-02 | C3 | CONFIG_GAP | DB path durability not verified | Attest path is durable local disk, single-writer, non-ephemeral | After BLK-C3-01 |
| BLK-C3-03 | C3 | CODE_GAP | No production store construction in composition root | Fresh impl auth + wire At1ExecutionStore construction in root only | After C4 provider exists or is co-authorized |
| BLK-CK-01 | C4 | PRIVATE_AUTHORITY_GAP | Commitment-key secret resource unidentified | Identify distinct SM secret resource (metadata only) | Identity source-principal work |
| BLK-CK-02 | C4 | PRIVATE_AUTHORITY_GAP | Exact commitment-key version unidentified | Identify exact numeric version resource string | After BLK-CK-01 |
| BLK-CK-03 | C4 | IAM_GAP | Commitment-key IAM not ready | Decide access principal; authorize/apply secretAccessor on that secret only | After BLK-CK-01 and principal decision |
| BLK-CK-04 | C4 | CODE_GAP | No production commitment-key provider | Fresh impl auth + implement provider returning CommitmentKeyMaterial | After BLK-CK-01/02 at least identified for freeze |

```text
HARD_BLOCKERS_FOR_PRE_NETWORK_YES=
  BLK-ID-01|
  BLK-ID-02|
  BLK-ID-03|
  BLK-B2-01|
  BLK-C2-01|
  BLK-C3-01|
  BLK-C3-02|
  BLK-C3-03|
  BLK-CK-01|
  BLK-CK-02|
  BLK-CK-03|
  BLK-CK-04

AT8W9_IS_NOT_A_BLOCKER_CURE=YES
AT8W10_RETRY_IS_NOT_A_BLOCKER_CURE=YES
```

## 9. Authority-routing matrix

| Work item | Authority class required | Consumes AT8W9? | May mutate IAM/secret/ADC? | May edit runtime? | Successor unit class |
| --- | --- | --- | --- | --- | --- |
| Designate source principal | HUMAN_GOVERNANCE private designation / attestation | NO | NO | NO | planning_or_attestation |
| ADC correlation attestation | HUMAN_GOVERNANCE + read-only local observation | NO | NO | NO | planning_or_attestation |
| Token Creator IAM apply | Fresh one-shot IAM authorization + execution | NO | IAM yes (scoped) | NO | iam_apply_execution |
| Commitment-key secret identify + version | HUMAN_GOVERNANCE / private metadata authority | NO | NO (identify only) | NO | planning_or_attestation |
| Commitment-key secret create (if missing) | Fresh secret-create authorization | NO | secret create yes | NO | secret_governance_execution |
| Commitment-key IAM bind | Fresh one-shot IAM authorization + execution | NO | IAM yes (scoped) | NO | iam_apply_execution |
| Production DB path designate + durability attest | HUMAN_GOVERNANCE / orchestrator config authority | NO | config yes only under explicit grant | NO | config_attestation |
| Concrete SM secret accessor implementation | Fresh offline implementation authorization | NO | NO | YES (scoped) | implementation |
| Production commitment-key provider implementation | Fresh offline implementation authorization | NO | NO | YES (scoped) | implementation |
| Production dependency resolution + store construction | Fresh offline implementation authorization | NO | NO | YES (scoped) | implementation |
| Pre-network readiness reconciliation after remediation | planning_only reconciliation | NO | NO | NO | planning_only |
| Live one-shot note execution | Fresh one-shot live-execution authorization (not AT8W9) | NO — new grant required | NO during auth authoring | NO during auth authoring | authorization then execution_proof |

```text
AT8W9_REUSE=FORBIDDEN
AT8W10_RETRY=FORBIDDEN
AT8K2_IAM_AUTHORITY_REUSE=FORBIDDEN
RESIDUAL_AT8W1_AT8W2_AT8W6_AUTHORITY=FORBIDDEN
EACH_MUTATING_OR_IMPLEMENTING_STEP_NEEDS_OWN_GRANT=YES
```

## 10. Recommended sequence

```text
SEQUENCE_MODE=FAIL_CLOSED_BETWEEN_STEPS
NO_STEP_IMPLIES_NEXT_STEP_AUTHORITY=YES
```

1. **Freeze preserved gates**
   Record A0/A1/B1/C1/D remain PASS and must not be regressed by remediation.

2. **Resolve identity-chain facts (read-only / human designation)**
   Complete `SOURCE_PRINCIPAL_PRIVATE_BINDING_READY`, then
   `AUTHORIZED_USER_ADC_CORRELATION_READY`, then assess
   `TOKEN_CREATOR_BINDING_READY`.
   If Token Creator binding is absent, stop and open a dedicated IAM-apply
   authorization unit; do not improvise binds.

3. **Resolve commitment-key resource facts (metadata only)**
   Identify commitment-key secret resource and exact version; decide access
   principal; assess IAM readiness. Create/bind only under fresh authority.

4. **Resolve production DB path facts**
   Designate orchestrator-governed durable path configuration and attest
   durability/single-writer constraints per AT8M.

5. **Authorize offline production-dependency implementation (single or tightly
   sequenced grants)** covering the minimum code set:
   - concrete production secret accessor (B2);
   - production commitment-key provider (C4);
   - production store construction + `_resolve_root_owned_runtime_dependencies`
     body (C3/C2);
   - identity acquisition helper only as required by the frozen AT8O mechanism.
   Implementation units must keep fail-closed behavior when config/IAM facts are
   missing and must not perform live HighLevel calls or unauthorized payload
   reads.

6. **Post-implementation readiness reconciliation (planning-only)**
   Re-evaluate B2/C2/C3/C4/RUNTIME_IDENTITY_CHAIN_READY and the read-only fact
   set against merged proof. Set
   `LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=YES` only when the definition in
   §11 is fully satisfied.

7. **Only then** author a **fresh** one-shot live-note execution authorization
   (successor to AT8W9; does not reuse AT8W9). Consumer execution unit is a new
   proof unit (not AT8W10 retry).

```text
RECOMMENDED_FIRST_NON_IMPLEMENTATION_MOVE=
  HUMAN_DESIGNATION_OF_SOURCE_PRINCIPAL_AND_COMMITMENT_KEY_RESOURCE_FACTS
RECOMMENDED_FIRST_IMPLEMENTATION_MOVE=
  AFTER_IDENTITY_AND_COMMITMENT_KEY_AND_DB_PATH_FACTS_ARE_DESIGNABLE
PARALLELISM_ALLOWED=
  commitment-key fact resolution || DB path designation || source-principal designation
PARALLELISM_FORBIDDEN=
  live execution || AT8W9 claim || secret payload read during planning
```

## 11. Explicit definition — LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=YES

`LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY` is `YES` if and only if **all** of the
following hold on the then-current `origin/main` plus attested private/config
facts. Any single failure forces `NO` and fail-closed behavior before
authorization claim, consumption-record creation, secret payload read for live
use, or HighLevel contact.

### 11.1 Preserved capability gates

```text
A0_PRIVATE_BINDING_SOURCE_READINESS=PASS
A1_PRIVATE_BINDING_DELIVERY=PASS
B1_ROOT_OWNED_CREDENTIAL_INJECTION_SEAM=PASS
C1_COMPOSITION_ROOT_SHAPE_IMPLEMENTED=PASS
D_BOUNDED_TRANSPORT=PASS
```

### 11.2 Remediated production dependency gates

```text
B2_CONCRETE_PRODUCTION_SECRET_ACCESSOR_READY=PASS
C2_ROOT_OWNED_RUNTIME_DEPENDENCY_RESOLUTION_READY=PASS
C3_PRODUCTION_EXECUTION_STORE_CONSTRUCTION_READY=PASS
C4_PRODUCTION_COMMITMENT_KEY_PROVIDER_READY=PASS
RUNTIME_IDENTITY_CHAIN_READY=PASS
```

### 11.3 Required read-only / control-plane facts

```text
GHL_PIT_SECRET_RESOURCE_IDENTIFIED=YES
GHL_PIT_TARGET_PRINCIPAL_IAM_READY=YES
SOURCE_PRINCIPAL_PRIVATE_BINDING_READY=YES
AUTHORIZED_USER_ADC_CORRELATION_READY=YES
TOKEN_CREATOR_BINDING_READY=YES
PRODUCTION_DB_PATH_CONFIGURED=YES
PRODUCTION_DB_PATH_DURABILITY_VERIFIED=YES
COMMITMENT_KEY_SECRET_RESOURCE_IDENTIFIED=YES
COMMITMENT_KEY_EXACT_VERSION_IDENTIFIED=YES
COMMITMENT_KEY_IAM_READY=YES
```

### 11.4 Assembly and safety invariants

```text
PUBLIC_ASSEMBLER_ARGUMENTS=verified_capability_ONLY
CALLER_CONTACT_OVERRIDE=NO
CALLER_LOCATION_OVERRIDE=NO
CALLER_CREDENTIAL_OVERRIDE=NO
CALLER_HTTP_TARGET_OVERRIDE=NO
CALLER_EXECUTION_STORE_OVERRIDE=NO
CALLER_DB_PATH_OVERRIDE=NO
CALLER_COMMITMENT_KEY_OVERRIDE=NO
CALLER_RUNTIME_IDENTITY_OVERRIDE=NO
SECOND_COMPOSITION_ROOT=NO
USER_MANAGED_SERVICE_ACCOUNT_KEYS=0
GENERIC_IMPLICIT_ADC_CHAIN_FOR_PRODUCTION=FORBIDDEN
GOOGLE_APPLICATION_CREDENTIALS_OVERRIDE=FORBIDDEN
HARDCODED_PRODUCTION_COMMITMENT_KEY=FORBIDDEN
HARDCODED_PRODUCTION_DB_PATH=FORBIDDEN
PRODUCTION_ASSEMBLY_FAILS_CLOSED_IF_ANY_DEPENDENCY_MISSING=YES
TRANSPORT_BUDGET_UNCHANGED=
  POST_ATTEMPTS_MAX=1|
  POST_SUCCESSES_MAX=1|
  READBACK_GET_ATTEMPTS_MAX=1|
  TOTAL_NETWORK_CALLS_MAX=2|
  TOTAL_MUTATION_CALLS_MAX=1|
  AUTOMATIC_RETRY=NO
```

### 11.5 Authority invariants at readiness time

```text
CURRENT_LIVE_EXECUTION_AUTHORITY=NONE_UNTIL_FRESH_ONE_SHOT_GRANT
AT8W9_NOT_TREATED_AS_STANDING_AUTHORITY=YES
AT8W10_NOT_RETRIED=YES
READINESS_YES_DOES_NOT_AUTHORIZE_NETWORK=YES
READINESS_YES_DOES_NOT_AUTHORIZE_SECRET_PAYLOAD_READ=YES
FIRST_LIVE_USE_STILL_REQUIRES=
  fresh one-shot authorization merge|
  independent consumer re-verification|
  one-shot consumption record|
  then bounded POST + conditional same-run GET only
```

### 11.6 Evaluation rule

```text
IF_ALL_SECTIONS_11_1_THROUGH_11_5_SATISFIED=
  LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=YES
ELSE=
  LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=NO

CURRENT_EVALUATION_AT_AT8W11_AUTHORING=
  LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=NO
```

## 12. Hard boundary and effect ledger

```text
FORBIDDEN=
  AT8W9_REUSE|
  AT8W10_RETRY|
  HIGHLEVEL_CALL|
  SECRET_PAYLOAD_READ|
  RUNTIME_SOURCE_EDIT|
  TEST_EDIT|
  IAM_MUTATION|
  SECRET_MUTATION|
  ADC_MUTATION|
  DEPLOYMENT|
  PRODUCTION_CONFIGURATION_MUTATION|
  CONTACT_OR_NOTE_MUTATION

HARD_BOUNDARY=
  HIGHLEVEL_CALLS=0|
  CRM_MUTATIONS=0|
  SECRET_PAYLOAD_READS=0|
  NETWORK_CALLS=0|
  IAM_SECRET_DEPLOY_ADC_MUTATIONS=0|
  EXTERNAL_EFFECTS=0|
  RUNTIME_SOURCE_CHANGES=0|
  TEST_CHANGES=0|
  AUTHORIZATION_ARTIFACT_CREATED=NO|
  IMPLEMENTATION_AUTHORIZATION_CREATED=NO|
  LIVE_EXECUTION_PERFORMED=NO
```

AT8W11 remains strictly inside planning-only / read-only remediation planning.

## 13. Successor routing

```text
AT8W11_CREATES_IMPLEMENTATION_AUTHORIZATION=NO
AT8W11_BEGINS_REMEDIATION_IMPLEMENTATION=NO

AFTER_AT8W11_MERGE_NEXT_ALLOWED=
  human-governed fact resolution units and/or
  targeted authorization packets for IAM/config/implementation
  sequenced per §10

AFTER_REMEDIATION_AND_READINESS_YES_NEXT=
  fresh one-shot live-note execution authorization
  (new unit; not AT8W9 reuse; not AT8W10 retry)

FORBIDDEN_IMMEDIATE_SUCCESSORS_FROM_THIS_PACKET=
  runtime implementation without fresh authorization|
  IAM apply without fresh authorization|
  live execution|
  AT8W9 claim/consumption|
  AT8W10 retry
```

## 14. Final disposition

```text
PLANNING_ONLY=YES
SUCCESS_CRITERION_FOR_THIS_UNIT=
  exact production-runtime dependency gap map from AT8W10 to
  LIVE_NOTE_PRODUCTION_PRE_NETWORK_READY=YES is recorded for human review

CHANGED_FILE_COUNT=1
ONLY_PLANNING_ARTIFACT_CHANGED=YES
STOP_FOR_EXACT_HEAD_FORMAL_REVIEW=YES
HUMAN_MERGE_REQUIRED=YES
IMPLEMENTATION_STARTED=NO
LIVE_EXECUTION_STARTED=NO
```

AT8W11 stops at planning. Human governance retains merge authority for this
exact plan head. No remediation implementation, implementation authorization, or
live execution begins inside this unit.
