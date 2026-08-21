# NW-008 AT-8K2 — GHL REST Production Runtime Principal IAM Apply Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

PLANNING_IDENTIFIER=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md
AUTHORIZATION_BRANCH=nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001

PREDECESSOR_PR=116
PR116_STATE=MERGED
PR116_REVIEWED_HEAD=f04a4d1d103dce3bf26dd7d77c800a8356871096
PR116_MERGE_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
PR116_MERGE_VERIFIED_ON_ORIGIN_MAIN=YES
PR116_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES

SOURCE_DESIGN_UNIT=NW008_AT8K1_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_DESIGN_001
SOURCE_DESIGN_ARTIFACT=docs/nw008/nw-008-at8k1-ghl-rest-production-runtime-principal-design-001.md
SOURCE_AT8K_ARTIFACT=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
SOURCE_AT8J_ARTIFACT=docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE

GRANT=GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
AUTHORIZATION_EFFECTIVE=NO
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_PATH=proof/nw008/at-8k2/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-consumption-001.md
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does **not** create a service account, bind IAM, create keys, read secret
payload, call HighLevel, mutate CRM, deploy, implement AT8L, or execute any of
the authorized-future mutations described below.

AT8K2 itself is `AUTHORIZATION_ARTIFACT_ONLY`. It authorizes a later bounded
execution consumer after independent human review and merge. It must not execute
the mutations.

### Conditional grant semantics

```text
GRANT=GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the
artifact defines a bounded one-shot GCP control-plane permission that becomes
usable only when both of the following are true:

1. the exact authorization artifact path is present on `main` via human review
   and merge; and
2. the authorized consumer unit
   `NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001`
   verifies that merge (exact path on `origin/main` / merge ancestry) before
   performing either authorized mutation.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is not standing IAM authority, not project-wide secret access, not
payload-read authority, not HighLevel authority, not CRM mutation authority,
not AT8L implementation authority, and not a reusable grant.

## 2. Verified prerequisites and source authority

Preflight was run before this artifact was authored:

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_HEAD_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
PREFLIGHT_ORIGIN_MAIN_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_RECORDED_AT_LOCAL=2026-08-21T09:15:32-0400

PR116_STATE=MERGED
PR116_REVIEWED_HEAD=f04a4d1d103dce3bf26dd7d77c800a8356871096
PR116_MERGE_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
PR116_MERGE_SHA_EQUALS_ORIGIN_MAIN=YES
PR116_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES
PR116_MERGE_SHA_REACHABLE_FROM_ORIGIN_MAIN=YES

SOURCE_DESIGN_ARTIFACT_PRESENT=YES
SOURCE_AT8K_ARTIFACT_PRESENT=YES
SOURCE_AT8J_ARTIFACT_PRESENT=YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #116 state | MERGED |
| PR #116 reviewed head | `f04a4d1d103dce3bf26dd7d77c800a8356871096` |
| PR #116 merge commit | `4adad8f2345227a841f71de9c60ac631ce9c61a4` |
| PR #116 merge commit equals `origin/main` at authoring | YES |
| PR #116 merge commit reachable from `origin/main` | YES |
| PR #116 reviewed head is an ancestor of `origin/main` | YES |
| AT8K1 design artifact present on base | YES |
| This unit executed service-account create | NO |
| This unit executed IAM bind | NO |
| This unit read secret payload | NO |
| This unit invoked HighLevel | NO |
| This unit mutated CRM | NO |

Bound durable source inputs (read-only for the future execution lane):

```text
SOURCE_DESIGN_PR=116
SOURCE_DESIGN_HEAD=f04a4d1d103dce3bf26dd7d77c800a8356871096
SOURCE_DESIGN_MERGE_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
SOURCE_DESIGN_ARTIFACT=docs/nw008/nw-008-at8k1-ghl-rest-production-runtime-principal-design-001.md
SOURCE_AT8K_ARTIFACT=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
SOURCE_AT8J_ARTIFACT=docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md
```

PR #116 merged AT8J + AT8K + AT8K1 planning-only design. That merge is a
prerequisite for this IAM-apply authorization. It does not itself authorize
service-account create, IAM mutation, payload access, HighLevel, CRM mutation,
or AT8L implementation. The future execution consumer may not reinterpret PR
#116 / AT8K1 as live-mutation authority, payload-read authority, or AT8L
implementation authority.

## 3. Frozen authorized-future mutation design (normative)

Exactly two future mutations are nameable by this grant. No third mutation is
authorized. This authorization unit must not execute either mutation.

### 3.1 MUTATION_1 — service account create

```text
MUTATION_1_NAME=SERVICE_ACCOUNT_CREATE
MUTATION_1_AUTHORIZED_WHEN_GRANT_EFFECTIVE=YES
MUTATION_1_EXECUTED_BY_THIS_UNIT=NO

SERVICE_ACCOUNT_ID=mg-guide-ghl-note-runtime
SERVICE_ACCOUNT_PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_PROJECT_NUMBER=831270426395
SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide GHL Note Runtime
SERVICE_ACCOUNT_DESCRIPTION=Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access
SERVICE_ACCOUNT_SINGLE_PURPOSE=YES

DESIGNED_CREATE_SHAPE=
  gcloud iam service-accounts create mg-guide-ghl-note-runtime \
    --project=ai-rolodex-to-crm \
    --display-name='MG Guide GHL Note Runtime' \
    --description='Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access'
```

### 3.2 MUTATION_2 — single-secret IAM bind

```text
MUTATION_2_NAME=SINGLE_SECRET_IAM_BIND
MUTATION_2_AUTHORIZED_WHEN_GRANT_EFFECTIVE=YES
MUTATION_2_EXECUTED_BY_THIS_UNIT=NO

SECRET_ACCESS_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_ACCESS_RESOURCE_ID=MG_GUIDE_PIT_GHL
SECRET_ACCESS_PROJECT=ai-rolodex-to-crm
SECRET_ACCESS_PROJECT_NUMBER=831270426395

SECRET_ACCESS_MEMBER=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SECRET_ACCESS_ROLE=roles/secretmanager.secretAccessor
SECRET_ACCESS_SCOPE=SINGLE_SECRET_ONLY
IAM_SCOPE=SINGLE_SECRET_ONLY
PROJECT_WIDE_SECRET_ACCESSOR=NO

DESIGNED_IAM_BIND_SHAPE=
  gcloud secrets add-iam-policy-binding MG_GUIDE_PIT_GHL \
    --project=ai-rolodex-to-crm \
    --member='serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com' \
    --role='roles/secretmanager.secretAccessor'
```

### 3.3 Sequencing and attempt guards (normative)

```text
MUTATION_ORDER=MUTATION_1_THEN_MUTATION_2
SECOND_MUTATION_REQUIRES_FIRST_READBACK_PASS=YES

SERVICE_ACCOUNT_CREATE_ATTEMPTS_MAX=1
SECRET_IAM_BIND_ATTEMPTS_MAX=1

AUTOMATIC_RETRY=NO
AUTOMATIC_CLEANUP=NO
COMPENSATING_MUTATION=NO
```

Normative consumer rules:

1. Attempt MUTATION_1 at most once.
2. After MUTATION_1, perform a read-only describe/list readback proving the
   designed service-account email exists before any IAM bind attempt.
3. If MUTATION_1 readback fails, stop. Do not attempt MUTATION_2. Do not retry
   create automatically. Do not run compensating delete/create.
4. Attempt MUTATION_2 at most once, and only after MUTATION_1 readback pass.
5. After MUTATION_2, perform a read-only IAM policy readback proving the exact
   member+role binding exists on the exact single secret resource.
6. If MUTATION_2 fails, stop. Do not retry automatically. Do not compensate.
7. Never create a service-account key at any step.
8. Never bind project-wide `roles/secretmanager.secretAccessor`.
9. Never bind an alternate principal, alternate secret, or additional role.
10. Never read secret payload versions as part of this apply lane.
11. Never invoke HighLevel or mutate CRM as part of this apply lane.
12. Never start AT8L implementation from this grant.

### 3.4 What the designed IAM grants and does not grant

```text
DESIGNED_IAM_GRANTS=
  - ability for the dedicated SA to call Secret Manager AccessSecretVersion
    on MG_GUIDE_PIT_GHL only (once applied by the authorized consumer)

DESIGNED_IAM_DOES_NOT_GRANT=
  - project-wide secret access
  - HighLevel network authorization
  - CRM mutation authorization
  - AT8L implementation authority
  - live mutation authorization
  - payload inspection by humans or orchestrator users during apply
  - service-account key based auth
  - deployment / runtime platform bind
  - standing reusable IAM authority
```

## 4. Authoring vs consumer writable scope (normative)

These scopes are disjoint. Authorization authoring must not execute GCP
mutations and must not write consumer execution proof files. The execution
consumer must not rewrite this authorization artifact. Consumption is recorded
only in the consumption record path; it is not recorded by mutating this grant.

```text
AUTHORIZATION_PR_WRITABLE_SCOPE=
governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md

AUTHORIZED_CONSUMER_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001
```

### 4.1 Authorization PR writable scope

```text
governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md
```

No other path is writable in this authorization PR.

### 4.2 Authorized consumer writable scope

Exact future consumer writable paths, reserved for
`NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001`
after this artifact is merged and independently verified:

```text
proof/nw008/at-8k2/**
docs/nw008/nw-008-at8k2-*
```

Consumer may write only execution proof / consumption / readback evidence under
those paths. Consumer must not modify this authorization artifact.

### 4.3 Authorized consumer blocked paths

```text
src/**=BLOCKED
tests/**=BLOCKED
contracts/**=BLOCKED
fixtures/**=BLOCKED
.github/**=BLOCKED
requirements.txt=BLOCKED
pyproject.toml=BLOCKED
Dockerfile=BLOCKED
.env.example=BLOCKED
scripts/**=BLOCKED
local/**=BLOCKED
workspace_addon/**=BLOCKED
src/integrations/ghl/**=BLOCKED
src/orchestration/**=BLOCKED
src/agents/**=BLOCKED
src/mg_guide/**=BLOCKED
proof/nw008/at-8i/**=BLOCKED
proof/nw008/at-8h/**=BLOCKED
proof/nw008/at-10/**=BLOCKED
competition/NEW_WORK_LEDGER.md=BLOCKED
docs/COMPETITION_BASELINE.md=BLOCKED
governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md=BLOCKED_FOR_CONSUMER
```

Also blocked for the consumer: AT8L implementation, live HighLevel transport
execution, secret payload reads for proof content, deployment changes, and any
IAM surface other than the exact MUTATION_1 / MUTATION_2 pair above.

## 5. Explicit guards and forbidden actions (normative)

```text
SERVICE_ACCOUNT_KEY_CREATION=NO
PROJECT_WIDE_SECRET_ACCESSOR=NO
ALTERNATE_PRINCIPAL=NO
ALTERNATE_SECRET=NO
ADDITIONAL_ROLE_GRANTS=NO

AUTOMATIC_RETRY=NO
AUTOMATIC_CLEANUP=NO
COMPENSATING_MUTATION=NO

REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0

DEVPOST_SECRET_COPY=NO
TOKEN_VALUE_EXPOSURE=NO
AT8L_IMPLEMENTATION_AUTHORIZED=NO
AT8L_AUTHORIZATION_CREATION_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_NOTE_READ_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
LIVE_TRANSPORT_EXECUTION_AUTHORIZED=NO
```

### Forbidden principals (must not be created or bound by this grant)

```text
FORBIDDEN_PRODUCTION_RUNTIME_PRINCIPALS=
  - ai-rolodex-ci@ai-rolodex-to-crm.iam.gserviceaccount.com
  - user:themg@themiliare-group.com
  - user:buildweek-evaluator@themiliare-group.com
  - mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
  - any mg-devpost project service account reused for live-note REST
  - any shared multi-purpose SA without single-purpose live-note scope
  - any principal other than
    serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

### Forbidden practices

```text
FORBIDDEN_PRACTICES=
  - service-account key creation
  - service-account key upload
  - service-account key commit to repository
  - project-wide roles/secretmanager.secretAccessor
  - binding any role other than roles/secretmanager.secretAccessor
  - binding any secret other than MG_GUIDE_PIT_GHL
  - binding any member other than the designed SA email
  - Devpost secret duplication
  - secret payload access in the apply lane
  - HighLevel execution in the apply lane
  - CRM mutation in the apply lane
  - automatic retry of create or bind
  - automatic cleanup / compensating mutation
  - treating this authorization merge as AT8L or live-mutation authority
  - executing mutations from the authorization PR itself
```

## 6. Known locked design inputs from AT8K1

```text
PRODUCTION_RUNTIME_PRINCIPAL_CLASS=SERVICE_ACCOUNT
PRODUCTION_RUNTIME_PRINCIPAL_DESIGNED=YES

PROPOSED_SERVICE_ACCOUNT_ID=mg-guide-ghl-note-runtime
PROPOSED_SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_PROJECT_NUMBER=831270426395

SECRET_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_RESOURCE_ID=MG_GUIDE_PIT_GHL
SECRET_HOST_PROJECT_LOGICAL=ai-rolodex-to-crm
SECRET_HOST_PROJECT_NUMBER=831270426395

SECRET_ACCESS_ROLE=roles/secretmanager.secretAccessor
SECRET_ACCESS_SCOPE=SINGLE_SECRET_ONLY
PROJECT_WIDE_SECRET_ACCESSOR=NO
DEVPOST_SECRET_COPY_REQUIRED=NO

SECRET_RESOURCE_READY=YES
SECRET_METADATA_ACCESS_VERIFIED=YES
IAM_AUTHORIZATION_DESIGNABLE=YES

# State at AT8K1 design time (not re-probed by this authorization unit):
SERVICE_ACCOUNT_CREATED=NO
IAM_CHANGE_APPLIED=NO
CURRENT_SECRET_HAS_ACCESSOR_BINDING=NO
CURRENT_SECRET_IAM_BINDINGS_COUNT=0
PROPOSED_SERVICE_ACCOUNT_ID_AVAILABLE=YES

LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
AT8L_IMPLEMENTATION_AUTHORIZED_BY_THIS_GRANT=NO
```

Payload identity remains out of scope. This unit and its consumer must not
access, print, echo, diff, or otherwise inspect secret payload bytes.

## 7. Consumer verification obligations before mutation

Before any mutation, the authorized consumer must verify:

```text
CONSUMER_MUST_VERIFY=
  1. exact authorization artifact path present on origin/main
  2. this artifact's merge ancestry / effectiveness by repo state
  3. PR116 merge SHA still reachable from origin/main
  4. designed SA email still absent OR already exactly matches designed id
     (if already present with exact email, MUTATION_1 is skipped as
      already-satisfied; it is not re-created and does not count as a retry)
  5. designed secret resource still exists (metadata-only; no payload)
  6. no project-wide secretAccessor grant is being requested
  7. no key creation flag is present in the execution plan
  8. AT8L implementation is not started from this grant
  9. REAL_SECRET_PAYLOAD_READS remain 0 for the apply lane
  10. HIGHLEVEL_CALLS remain 0
  11. CRM_MUTATIONS remain 0
  12. DEPLOYMENT_CHANGES remain 0
```

If the designed SA already exists with the exact email before MUTATION_1, the
consumer records `MUTATION_1_ALREADY_SATISFIED=YES`, does not re-create, and may
proceed to MUTATION_2 only after readback confirms the exact email. If a
different SA occupies the id, stop closed; do not rename, delete, or substitute.

If the exact member+role binding already exists on the exact secret before
MUTATION_2, the consumer records `MUTATION_2_ALREADY_SATISFIED=YES` and does not
re-bind. Any other binding state requires stop-closed human review; no automatic
repair.

## 8. Required consumer proof obligations

```text
PROOF_AUTHORIZATION_MERGE_VERIFIED=REQUIRED
PROOF_MUTATION_1_ATTEMPT_COUNT_LE_1=REQUIRED
PROOF_MUTATION_1_READBACK_OR_ALREADY_SATISFIED=REQUIRED
PROOF_MUTATION_2_ATTEMPT_COUNT_LE_1=REQUIRED
PROOF_MUTATION_2_REQUIRES_MUTATION_1_READBACK_PASS=REQUIRED
PROOF_MUTATION_2_READBACK_OR_ALREADY_SATISFIED=REQUIRED
PROOF_NO_SERVICE_ACCOUNT_KEY=REQUIRED
PROOF_NO_PROJECT_WIDE_SECRET_ACCESSOR=REQUIRED
PROOF_EXACT_MEMBER_ROLE_RESOURCE_ONLY=REQUIRED
PROOF_REAL_SECRET_PAYLOAD_READS_0=REQUIRED
PROOF_HIGHLEVEL_CALLS_0=REQUIRED
PROOF_CRM_MUTATIONS_0=REQUIRED
PROOF_DEPLOYMENT_CHANGES_0=REQUIRED
PROOF_ONE_SHOT_CONSUMPTION_RECORDED=REQUIRED
PROOF_AUTHORIZATION_ARTIFACT_UNMODIFIED_BY_CONSUMER=REQUIRED
```

Proof content must not include secret payload bytes, token values, or private
CRM record bodies.

## 9. Explicit non-authorizations

```text
AT8K2_AUTHORIZES_SERVICE_ACCOUNT_CREATE_IN_THIS_PR=NO
AT8K2_AUTHORIZES_IAM_BIND_IN_THIS_PR=NO
AT8K2_EXECUTES_MUTATIONS=NO

HIGHLEVEL_CALL_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_NOTE_READ_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REAL_SECRET_VALUE_READ_AUTHORIZED=NO
REAL_TOKEN_RUNTIME_USE_AUTHORIZED=NO
LIVE_MUTATION_GRANT_CREATION_AUTHORIZED=NO
AT8L_IMPLEMENTATION_AUTHORIZED=NO
AT8L_AUTHORIZATION_CREATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
PROJECT_WIDE_SECRET_ACCESSOR_AUTHORIZED=NO
ALTERNATE_PRINCIPAL_AUTHORIZED=NO
ALTERNATE_SECRET_AUTHORIZED=NO
ADDITIONAL_ROLE_GRANT_AUTHORIZED=NO
DEPLOYMENT_CHANGE_AUTHORIZED=NO
SRC_IMPLEMENTATION_AUTHORIZED=NO
PACKAGE_MANIFEST_CHANGE_AUTHORIZED=NO
```

When the conditional grant is effective, only the named consumer may perform the
exact MUTATION_1 and MUTATION_2 pair under the guards above. Effectiveness does
not authorize payload reads, HighLevel, CRM mutation, AT8L, keys, or any other
GCP mutation.

## 10. Non-transitivity

```text
PR116_PLANNING_AUTHORITY_GRANTS_IAM_APPLY=NO
AT8K1_DESIGN_AUTHORITY_GRANTS_IAM_APPLY=NO
AT8K_DESIGN_AUTHORITY_GRANTS_IAM_APPLY=NO
AT8I_AUTHORIZATION_GRANTS_IAM_APPLY=NO
AT8H_AUTHORIZATION_GRANTS_IAM_APPLY=NO
PR114_AUTHORIZATION_REUSED=NO
AT8I_AUTHORIZATION_REUSED=NO

AT8K2_AUTHORIZATION_GRANTS_AT8L=NO
AT8K2_AUTHORIZATION_GRANTS_LIVE_MUTATION=NO
AT8K2_AUTHORIZATION_GRANTS_LIVE_TRANSPORT_EXECUTION=NO
AT8K2_AUTHORIZATION_GRANTS_REAL_CREDENTIAL_USE=NO
AT8K2_AUTHORIZATION_GRANTS_SECRET_PAYLOAD_READ=NO
AT8K2_AUTHORIZATION_GRANTS_DEPLOYMENT_CHANGE=NO
AT8K2_AUTHORIZATION_GRANTS_STANDING_IAM=NO
```

PR #116 closed AT8K1 principal/IAM design. That closure removes a predecessor
blocker and makes this authorization designable; it does not grant IAM apply.
This authorization, even after merge, does not grant AT8L implementation, live
mutation, payload read, HighLevel, CRM mutation, keys, or deployment change.

## 11. Competition delta handling boundary

This authorization lane does not authorize creating or modifying competition
delta governance artifacts. Competition delta checks are informational unless
separately approved as writable scope.

```text
competition/NEW_WORK_LEDGER.md=BLOCKED
docs/COMPETITION_BASELINE.md=BLOCKED
```

## 12. Authoring-lane non-actions and zero-effects

```text
MODE=AUTHORIZATION_ARTIFACT_ONLY
AUTHORIZATION_ONLY=YES
GCP_MUTATIONS=0

SERVICE_ACCOUNT_CREATE_COMMANDS=0
SERVICE_ACCOUNT_KEY_CREATE_COMMANDS=0
IAM_POLICY_MUTATION_COMMANDS=0
SECRET_MANAGER_PAYLOAD_INVOCATIONS=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0

SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0

REAL_SECRET_PAYLOAD_READS=0
REAL_SECRET_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
TOKEN_VALUE_EXPOSURE=NO

SERVICE_ACCOUNT_CREATED=NO
IAM_CHANGE_APPLIED=NO
SERVICE_ACCOUNT_KEY_CREATION=NO
AT8L_IMPLEMENTATION_STARTED=NO
AT8L_AUTHORIZATION_CREATED=NO
```

## 13. Final return fields (authoring lane)

```text
PR116_MERGED=YES
PR116_MERGE_SHA=4adad8f2345227a841f71de9c60ac631ce9c61a4
MERGE_SHA_REACHABLE_FROM_MAIN=YES

UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_AUTHORIZATION_001
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
AT8K2_AUTHORIZATION_ONLY=YES

MUTATION_1=SERVICE_ACCOUNT_CREATE
MUTATION_1_ID=mg-guide-ghl-note-runtime
MUTATION_1_PROJECT=ai-rolodex-to-crm

MUTATION_2=SINGLE_SECRET_IAM_BIND
MUTATION_2_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
MUTATION_2_MEMBER=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
MUTATION_2_ROLE=roles/secretmanager.secretAccessor

SERVICE_ACCOUNT_CREATE_ATTEMPTS_MAX=1
SECRET_IAM_BIND_ATTEMPTS_MAX=1
SECOND_MUTATION_REQUIRES_FIRST_READBACK_PASS=YES

SERVICE_ACCOUNT_KEY_CREATION=NO
PROJECT_WIDE_SECRET_ACCESSOR=NO
ALTERNATE_PRINCIPAL=NO
ALTERNATE_SECRET=NO
ADDITIONAL_ROLE_GRANTS=NO
AUTOMATIC_RETRY=NO
AUTOMATIC_CLEANUP=NO
COMPENSATING_MUTATION=NO

REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
GCP_MUTATIONS=0

AT8K2_MUST_NOT_EXECUTE_THE_MUTATIONS=YES
AUTHORIZED_CONSUMER_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001
```

STOP after this authorization artifact is opened as a PR. Do not execute
MUTATION_1. Do not execute MUTATION_2. Do not create keys. Do not read payload.
Do not invoke HighLevel. Do not mutate CRM. Do not start AT8L.
