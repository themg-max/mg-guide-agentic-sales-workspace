# NW-008 AT-8K1 — GHL REST Production Runtime Principal Design 001

```text
UNIT=NW008_AT8K1_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_DESIGN_001
PR_CLASS=planning_only
PHASE=PLANNING_ONLY
MODE=READ_ONLY_INSPECTION_AND_PLANNING
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=nw008-at8k1-ghl-rest-production-runtime-principal-design-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PLAN_HEAD_AT_START=825cefc0e114179a6080546d846bf9e04c687c29
PR115_MERGE_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PR115_MERGE_VERIFIED=YES

SOURCE_EVIDENCE_AT8J=docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md
SOURCE_EVIDENCE_AT8K=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
SOURCE_AT8J_UNIT=NW008_AT8J_POST_AT8I_EXECUTION_BOUNDARY_REINSPECTION_001
SOURCE_AT8K_UNIT=NW008_AT8K_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_DESIGN_001
AT8J_EVIDENCE_AVAILABLE=YES
AT8K_EVIDENCE_AVAILABLE=YES

PLANNING_ONLY=YES
IMPLEMENTATION_CHANGE=NO
RUNTIME_CHANGE=NO
TEST_CHANGE=NO
CONTRACT_CHANGE=NO
PACKAGE_MANIFEST_CHANGE=NO
SERVICE_ACCOUNT_CREATED=NO
IAM_CHANGE_APPLIED=NO
SERVICE_ACCOUNT_KEY_CREATION=NO
AUTHORIZATION_ARTIFACT_CREATED=NO
LIVE_MUTATION_AUTHORIZATION_CREATED=NO
PR114_AUTHORIZATION_REUSED=NO
AT8I_AUTHORIZATION_REUSED=NO
AT8K_AUTHORIZATION_REUSED=NO

REAL_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
REAL_SECRET_PAYLOAD_READS=0
REAL_SECRET_READS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
TOKEN_VALUE_EXPOSURE=NO
```

## Pre-flight

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH_AT_START=nw008-at8k-ghl-rest-live-note-runtime-construction-path-design-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_HEAD_SHA=825cefc0e114179a6080546d846bf9e04c687c29
PREFLIGHT_ORIGIN_MAIN_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_AT8J_EVIDENCE_AVAILABLE=YES
PREFLIGHT_AT8K_EVIDENCE_AVAILABLE=YES
PREFLIGHT_ARTIFACT_BRANCH=nw008-at8k1-ghl-rest-production-runtime-principal-design-001
PREFLIGHT_ARTIFACT_BRANCH_BASE=nw008-at8k-ghl-rest-live-note-runtime-construction-path-design-001
PREFLIGHT_RECORDED_AT_LOCAL=2026-08-21T09:02:22-0400
```

Abort conditions did not fire: the artifact branch is not `main`; the worktree had
no unrelated changes at start; AT8J and AT8K source-evidence artifacts were
readable under `docs/nw008/`.

This unit does not consume, reuse, or extend PR114 / AT8I / AT8K authority as
implementation or live-mutation authority. AT8I implementation authority remains
one-shot and consumed. AT8K remains planning-only construction-path design. This
unit designs only the production runtime principal and the single-secret IAM
binding shape. It does not create the service account and does not apply IAM.

## Non-actions

```text
SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0
INIT_PY_MUTATIONS=0
LIVE_NOTE_TRANSPORT_MUTATIONS=0
SERVICE_ACCOUNT_CREATE_COMMANDS=0
SERVICE_ACCOUNT_KEY_CREATE_COMMANDS=0
IAM_POLICY_MUTATION_COMMANDS=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0
SECRET_MANAGER_PAYLOAD_INVOCATIONS=0
REAL_SECRET_PAYLOAD_READS=0
TOKEN_VALUES_PRINTED=NO
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENTS=0
LIVE_MUTATION_AUTHORIZATION_CREATED=NO
AT8L_AUTHORIZATION_CREATED=NO
```

Read-only sources consulted:

- `docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md`
- `docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md`

Read-only GCP control-plane observation used only to confirm the proposed
service-account id is not already allocated (describe → `NOT_FOUND`; list does
not include the proposed email). No create, no IAM bind, no payload access.

## Design question — why a dedicated production runtime principal

AT8K left the production principal undecided:

```text
PRODUCTION_RUNTIME_PRINCIPAL=UNKNOWN
RUNTIME_PRINCIPAL_DECISION_REQUIRED=YES
SECRET_ACCESS_MEMBER=<TBD>
CURRENT_SECRET_HAS_ACCESSOR_BINDING=NO
CURRENT_SECRET_IAM_BINDINGS_COUNT=0
```

AT8K also recorded that concrete Secret Manager accessor implementation is
blocked on a production runtime principal decision plus later implementation
grant plus single-secret accessor IAM — not blocked on resource identity or
metadata verify.

Without a decided principal:

1. single-secret `roles/secretmanager.secretAccessor` cannot be designed to a
   concrete member;
2. production assembly cannot name the identity that will call
   `GoogleSecretManagerLiveNoteSecretAccessor` later;
3. operator metadata-verify success under `themg@...` must not silently become
   permanent runtime authority;
4. NW-007 judge SA, CI SA, and ADC user identities must not be reused by
   default.

This unit closes only the principal decision and the IAM design shape. It does
not implement runtime code, create the SA, apply IAM, read payload, or authorize
live HighLevel / CRM mutation.

## Known verified state carried from AT8K readiness

```text
SECRET_RESOURCE_READY=YES
SECRET_METADATA_ACCESS_VERIFIED=YES

SECRET_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_RESOURCE_ID=MG_GUIDE_PIT_GHL
SECRET_HOST_PROJECT_LOGICAL=ai-rolodex-to-crm
SECRET_HOST_PROJECT_NUMBER=831270426395

SECRET_VERSION_1_ENABLED=YES
CURRENT_SECRET_IAM_BINDINGS_COUNT=0
CURRENT_SECRET_HAS_ACCESSOR_BINDING=NO

GHL_LOCATION_ID=XpWabhp6Ez8bXZTP7w3r
CONTACTS_READONLY_SCOPE=YES
CONTACTS_WRITE_SCOPE=YES
SCOPE_EXPANSION_REQUIRED=NO

LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN
DEVPOST_SECRET_COPY_REQUIRED=NO

LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

Payload identity remains `UNKNOWN`. This unit does not access, print, echo,
diff, or otherwise inspect secret payload bytes.

## Production runtime principal design

### Decision

```text
PRODUCTION_RUNTIME_PRINCIPAL_CLASS=SERVICE_ACCOUNT
PRODUCTION_RUNTIME_PRINCIPAL_DESIGNED=YES
RUNTIME_PRINCIPAL_DECISION_REQUIRED=NO

PROPOSED_SERVICE_ACCOUNT_ID=mg-guide-ghl-note-runtime
PROPOSED_SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_PROJECT_NUMBER=831270426395

SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide GHL Note Runtime
SERVICE_ACCOUNT_PURPOSE=Bounded MG Guide HighLevel REST live-note runtime
SERVICE_ACCOUNT_SINGLE_PURPOSE=YES
SERVICE_ACCOUNT_DESCRIPTION=Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access and later authorized live-note transport execution. Not CI. Not judge. Not operator user.
```

### Why service account (not user)

```text
PRINCIPAL_CLASS_RATIONALE=
  1. Production live-note runtime is a machine path (composition root + accessor),
     not an interactive operator session.
  2. User principals (themg@, buildweek-evaluator@) are suitable for planning /
     metadata verify / ADC probes only, not permanent runtime secretAccessor.
  3. A dedicated SA enables least-privilege single-secret IAM without project-wide
     secretAccessor and without key material.
  4. SA identity is durable, auditable, and rotatable without embedding human
     operator identity into runtime bindings.
```

### Proposed identity availability (read-only observation)

```text
PROPOSED_SERVICE_ACCOUNT_ID_AVAILABLE=YES
PROPOSED_SERVICE_ACCOUNT_DESCRIBE_RESULT=NOT_FOUND
PROPOSED_SERVICE_ACCOUNT_LIST_MATCH=NO
SERVICE_ACCOUNT_CREATED=NO
SERVICE_ACCOUNT_CREATE_ATTEMPTED=NO
```

Read-only `gcloud iam service-accounts describe` for
`mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com` returned
`NOT_FOUND`. Project SA list for `ai-rolodex-to-crm` does not include that
email. The proposed id is therefore available for a later authorized create
lane. This unit does not create it.

### Explicitly forbidden principals and practices

```text
FORBIDDEN_PRODUCTION_RUNTIME_PRINCIPALS=
  - ai-rolodex-ci@ai-rolodex-to-crm.iam.gserviceaccount.com (CI reuse)
  - user:themg@themiliare-group.com (operator user as permanent runtime)
  - user:buildweek-evaluator@themiliare-group.com (ADC/eval user as runtime)
  - mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com (NW-007 judge SA)
  - any mg-devpost project service account reused for live-note REST
  - any shared multi-purpose SA without single-purpose live-note scope

FORBIDDEN_PRACTICES=
  - service-account key creation
  - service-account key upload
  - service-account key commit to repository
  - project-wide roles/secretmanager.secretAccessor
  - Devpost secret duplication (DEVPOST_SECRET_COPY_REQUIRED=NO)
  - secret payload access in this lane
  - HighLevel execution in this lane
  - CRM mutation in this lane
  - IAM apply in this lane
  - treating metadata-verify success as runtime authorization
```

### Observed non-selected candidates (informational; not granted)

Carried forward from AT8K readiness and reaffirmed here:

```text
OBSERVED_OPERATOR_USER=user:themg@themiliare-group.com
OBSERVED_OPERATOR_USER_ROLE=METADATA_VERIFY_AND_PLANNING_OPERATOR_ONLY
OBSERVED_OPERATOR_USER_SELECTED_AS_PRODUCTION_RUNTIME=NO

OBSERVED_ADC_USER=user:buildweek-evaluator@themiliare-group.com
OBSERVED_ADC_USER_SELECTED_AS_PRODUCTION_RUNTIME=NO

OBSERVED_NW007_JUDGE_SA=serviceAccount:mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
OBSERVED_NW007_JUDGE_SA_SELECTED_AS_PRODUCTION_RUNTIME=NO
OBSERVED_NW007_JUDGE_SA_REASON=Different project (mg-devpost); judge/demo surface only; DEVPOST_SECRET_COPY_REQUIRED=NO

OBSERVED_CI_SA=serviceAccount:ai-rolodex-ci@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_CI_SA_SELECTED_AS_PRODUCTION_RUNTIME=NO
OBSERVED_CI_SA_REASON=CI principal; not single-purpose live-note runtime
```

### Platform note

```text
CURRENT_EXECUTION_LANE=VS_CODE_ORCHESTRATOR_LOCAL
PRODUCTION_RUNTIME_PLATFORM=UNDECIDED
PRODUCTION_RUNTIME_PROJECT=ai-rolodex-to-crm
PRODUCTION_RUNTIME_PRINCIPAL=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_COMPOSITION_ROOT_SYMBOL=assemble_bound_live_note_runtime
RUNTIME_COMPOSITION_ROOT_IMPLEMENTED=NO
RUNTIME_DEDICATED_SERVICE_ACCOUNT_BOUND=NO
```

`PRODUCTION_RUNTIME_PLATFORM` remains undecided (local orchestrator vs later
Cloud Run / batch / other). The principal identity is decided independently of
platform so IAM can be designed against one SA. Platform selection is a later
deployment design and is not authorized here.

## Secret IAM design (not applied)

### Designed binding

```text
SECRET_ACCESS_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_ACCESS_RESOURCE_ID=MG_GUIDE_PIT_GHL
SECRET_ACCESS_PROJECT=ai-rolodex-to-crm
SECRET_ACCESS_PROJECT_NUMBER=831270426395

SECRET_ACCESS_MEMBER=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SECRET_ACCESS_ROLE=roles/secretmanager.secretAccessor
SECRET_ACCESS_SCOPE=SINGLE_SECRET_ONLY
IAM_SCOPE=SINGLE_SECRET_ONLY

PROJECT_WIDE_SECRET_ACCESSOR=NO
DEVPOST_SECRET_DUPLICATION=NO
SERVICE_ACCOUNT_KEY_CREATION=NO

IAM_CHANGE_APPLIED=NO
IAM_CHANGES=0
CURRENT_SECRET_HAS_ACCESSOR_BINDING=NO
CURRENT_SECRET_IAM_BINDINGS_COUNT=0

IAM_AUTHORIZATION_DESIGNABLE=YES
```

`IAM_AUTHORIZATION_DESIGNABLE=YES` means a later separate authorization lane may
design a one-shot IAM-apply grant that names exactly this resource, member, and
role. It does **not** authorize IAM mutation in this lane. It does not authorize
payload reads. It does not authorize HighLevel or CRM mutation.

### Designed (not executed) create shape

For a later authorized service-account create lane only:

```text
gcloud iam service-accounts create mg-guide-ghl-note-runtime \
  --project=ai-rolodex-to-crm \
  --display-name='MG Guide GHL Note Runtime' \
  --description='Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access'
```

Do not create keys. Do not download JSON keys. Do not upload keys.

### Designed (not executed) IAM bind shape

For a later authorized IAM lane only, and only after the SA exists:

```text
gcloud secrets add-iam-policy-binding MG_GUIDE_PIT_GHL \
  --project=ai-rolodex-to-crm \
  --member='serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'
```

Normative constraints for any later apply lane:

```text
MUST_BIND_ONLY_SINGLE_SECRET=YES
MUST_NOT_GRANT_PROJECT_WIDE_SECRET_ACCESSOR=YES
MUST_NOT_COPY_SECRET_TO_MG_DEVPOST=YES
MUST_NOT_CREATE_SERVICE_ACCOUNT_KEY=YES
MUST_NOT_GRANT_JUDGE_SA=YES
MUST_NOT_GRANT_CI_SA=YES
MUST_NOT_GRANT_OPERATOR_USER_AS_RUNTIME=YES
MUST_NOT_READ_PAYLOAD_DURING_IAM_APPLY=YES
MUST_NOT_INVOKE_HIGHLEVEL=YES
MUST_NOT_MUTATE_CRM=YES
```

### What this IAM grants and does not grant

```text
DESIGNED_IAM_GRANTS=
  - ability for the dedicated SA to call Secret Manager AccessSecretVersion
    on MG_GUIDE_PIT_GHL only (once applied later)

DESIGNED_IAM_DOES_NOT_GRANT=
  - project-wide secret access
  - HighLevel network authorization
  - CRM mutation authorization
  - AT8L implementation authority
  - live mutation authorization
  - payload inspection by humans or orchestrator users
  - service-account key based auth
```

## AT8K normalizations carried forward

AT8K designed `assemble_bound_live_note_runtime(...)`. This unit normalizes two
construction-path items that affect later offline implementation without
implementing them.

### Execution store ownership

```text
CALLER_SUPPLIED_EXECUTION_STORE=NO
PRODUCTION_EXECUTION_STORE_ROOT_OWNED=YES
TEST_ONLY_EXECUTION_STORE_INJECTION=YES
```

Normative production rule:

1. Production assembly must not accept a caller-supplied `execution_store` as a
   public assembler argument that can redirect reservation durability.
2. The composition root owns production execution-store selection / construction
   (root-owned), consistent with AT8G reservation backend semantics.
3. Offline tests may inject a test-only execution store through a test-only seam
   owned by the composition root. That seam is not a production caller supply
   and is not a target/credential/HTTP authority override.

This supersedes the AT8K draft public signature allowance of
`execution_store: At1ExecutionStore | None = None` as a production caller input.
AT8K's allowance remains valid only as a historical design draft; AT8K1 makes
production caller supply `NO` and test-only injection `YES`.

### Package export

```text
PACKAGE_EXPORT_CHANGE_REQUIRED=NO
PACKAGE_EXPORT_CHANGE_OPTIONAL=YES
PACKAGE_EXPORT_IS_LIVE_MUTATION_BLOCKER=NO
```

Exporting `assemble_bound_live_note_runtime` (or related live-note types) from
`src/integrations/ghl/highlevel_rest/__init__.py` is optional cleanup for a
later offline implementation. Missing package exports do not block principal
design, IAM design, or live-mutation authorization designability on their own.
AT8K's earlier `PACKAGE_EXPORT_CHANGE_REQUIRED=YES` is normalized to
`REQUIRED=NO` / `OPTIONAL=YES`.

### Unchanged AT8K construction invariants

```text
RUNTIME_COMPOSITION_ROOT_DESIGNED=YES
COMPOSITION_ROOT_PROPOSED_PATH=src/integrations/ghl/highlevel_rest/live_note_runtime.py
COMPOSITION_ROOT_PROPOSED_SYMBOL=assemble_bound_live_note_runtime
CALLER_SUPPLIED_CONTACT_OVERRIDE=NO
CALLER_SUPPLIED_HTTP_CLIENT_TARGET=NO
CALLER_SUPPLIED_CREDENTIAL=NO
CALLER_TARGET_OVERRIDE_IMPOSSIBLE=YES
SEALED_LIVE_NOTE_REST_RESOURCE_NAME=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
RESOURCE_NAME_CALLER_OVERRIDE=FORBIDDEN
RESOURCE_NAME_ENV_DISCOVERY=FORBIDDEN
RESOURCE_NAME_EMBEDDED_HISTORICAL_MCP_ID=FORBIDDEN
UNBOUND_PRODUCTION_ASSEMBLY=FAIL_CLOSED
HISTORICAL_MCP_PIT_BOUND_AS_REST=NO
```

## Relationship to concrete secret accessor (still not implemented)

```text
CONCRETE_SECRET_ACCESSOR_INTERFACE_DESIGNED=YES
SECRET_ACCESSOR_PROPOSED_SYMBOL=GoogleSecretManagerLiveNoteSecretAccessor
SECRET_ACCESSOR_IMPLEMENTATION_REQUIRED=YES
SECRET_ACCESSOR_IMPLEMENTED=NO
SECRET_ACCESSOR_PRODUCTION_PRINCIPAL=
  serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

Future production accessor construction (later grant only) must:

1. run as / use ADC of the dedicated SA above (or an explicitly authorized
   workload identity binding to that SA);
2. read only `projects/831270426395/secrets/MG_GUIDE_PIT_GHL` as sealed by the
   composition root;
3. return payload only to `LiveNoteCredentialProvider`;
4. never log token bytes;
5. never use gcloud subprocess or shell secret reads;
6. never accept caller resource override.

This unit does not implement the accessor, add `google-cloud-secretmanager`, or
authorize that implementation.

## Authorization designability gates

```text
SECRET_RESOURCE_READY=YES
SECRET_METADATA_ACCESS_VERIFIED=YES
PRODUCTION_RUNTIME_PRINCIPAL_DESIGNED=YES
PROPOSED_SERVICE_ACCOUNT_ID_AVAILABLE=YES
SERVICE_ACCOUNT_CREATED=NO
IAM_CHANGE_APPLIED=NO
IAM_AUTHORIZATION_DESIGNABLE=YES

NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_MUTATION_PREREQUISITES_COMPLETE=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO

AT8L_READY_AFTER_IAM=YES
```

Interpretation:

- `IAM_AUTHORIZATION_DESIGNABLE=YES`: principal member is concrete; single-secret
  role and resource are concrete; a later IAM-apply authorization artifact can be
  written without inventing identity.
- `AT8L_READY_AFTER_IAM=YES`: after a later authorized SA create + the designed
  single-secret IAM bind, the production principal/IAM prerequisite track that
  AT8K marked blocking for concrete GSM accessor / production secret access is
  satisfied from the principal side. Offline AT8L assembler + `_attempt_http`
  transport-touch authorization remains separately designable per AT8K and does
  not itself require IAM apply; production secret-access implementation still
  requires SA+IAM first.
- `LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO`: construction root unimplemented,
  Authorization header transport-touch unimplemented, concrete accessor
  unimplemented, SA not created, IAM not applied, live transport flags remain
  false. Designing a live-mutation grant now would invent missing wiring.
- `NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES` remains limited to later
  offline one-shot implementation authorization for assembler and transport-touch
  (AT8L lineage), not live mutation, not payload reads, not IAM apply unless a
  distinct grant names IAM.

## Recommended next units (not created here)

```text
NEXT_RECOMMENDED_UNIT_A=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_AUTHORIZATION_001
NEXT_PR_CLASS_A=authorization
NEXT_MODE_A=AUTHORIZATION_ARTIFACT_ONLY
NEXT_SCOPE_A=
  1. authorize create of mg-guide-ghl-note-runtime SA in ai-rolodex-to-crm
  2. authorize single-secret IAM bind only
     resource=MG_GUIDE_PIT_GHL
     member=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
     role=roles/secretmanager.secretAccessor
  3. forbid keys, project-wide accessor, Devpost copy, payload read, HighLevel, CRM

NEXT_RECOMMENDED_UNIT_B=NW008_AT8L_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_IMPLEMENTATION_AUTHORIZATION_001
NEXT_PR_CLASS_B=authorization
NEXT_MODE_B=AUTHORIZATION_ARTIFACT_ONLY
NEXT_SCOPE_B=
  1. composition root live_note_runtime.assemble_bound_live_note_runtime
  2. transport-touch BoundedLiveNoteTransport._attempt_http Authorization header
  3. carry AT8K1 execution-store and package-export normalizations
  4. do not authorize concrete GSM accessor unless explicitly named
  5. do not authorize IAM, payload read, live HighLevel, CRM mutation
```

Order note: Unit A (SA create + IAM) and Unit B (offline AT8L assembler auth)
may be sequenced independently. Production secret-access implementation after
AT8L still requires Unit A outcomes first.

## Non-authority

```text
AT8K1_AUTHORIZES_SERVICE_ACCOUNT_CREATE=NO
AT8K1_AUTHORIZES_SERVICE_ACCOUNT_KEY_CREATE=NO
AT8K1_AUTHORIZES_IAM_CHANGE=NO
AT8K1_AUTHORIZES_IMPLEMENTATION=NO
AT8K1_AUTHORIZES_TRANSPORT_TOUCH=NO
AT8K1_AUTHORIZES_CONCRETE_GSM_ACCESSOR=NO
AT8K1_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8K1_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8K1_AUTHORIZES_LIVE_NOTE_READ=NO
AT8K1_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8K1_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8K1_AUTHORIZES_SECRET_PAYLOAD_READ=NO
AT8K1_AUTHORIZES_DEPLOYMENT_CHANGE=NO
AT8K1_REUSES_PR114_AUTHORIZATION=NO
AT8K1_REUSES_AT8I_AUTHORIZATION=NO
AT8K1_CREATES_AT8L_AUTHORIZATION=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## Validation

```text
SOURCE_RUNTIME_TEST_CHANGES=NO
EXTERNAL_EFFECTS=0
ARTIFACT_ONLY_DIFF=YES
GIT_DIFF_CHECK=PASS
TOKEN_MATERIAL_LEAK_SCAN=PASS

HIGHLEVEL_CALLS=0
REAL_SECRET_PAYLOAD_READS=0
REAL_SECRET_READS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
SERVICE_ACCOUNT_CREATED=NO
SERVICE_ACCOUNT_KEY_CREATION=NO
```

Planning-only body is artifact-only under `docs/nw008/`. Read-only SA describe /
list used solely to confirm proposed id availability. No create. No IAM bind.
No payload access. No HighLevel. No CRM. No src/test/runtime mutations.

## Final return fields

```text
PRODUCTION_RUNTIME_PRINCIPAL_DESIGNED=YES

PROPOSED_SERVICE_ACCOUNT_ID=mg-guide-ghl-note-runtime
PROPOSED_SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROPOSED_SERVICE_ACCOUNT_ID_AVAILABLE=YES

SERVICE_ACCOUNT_CREATED=NO
IAM_CHANGE_APPLIED=NO
SERVICE_ACCOUNT_KEY_CREATION=NO

SECRET_ACCESS_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_ACCESS_MEMBER=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SECRET_ACCESS_ROLE=roles/secretmanager.secretAccessor
SECRET_ACCESS_SCOPE=SINGLE_SECRET_ONLY
PROJECT_WIDE_SECRET_ACCESSOR=NO

IAM_AUTHORIZATION_DESIGNABLE=YES
AT8L_READY_AFTER_IAM=YES
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO

CALLER_SUPPLIED_EXECUTION_STORE=NO
PRODUCTION_EXECUTION_STORE_ROOT_OWNED=YES
TEST_ONLY_EXECUTION_STORE_INJECTION=YES
PACKAGE_EXPORT_CHANGE_REQUIRED=NO
PACKAGE_EXPORT_CHANGE_OPTIONAL=YES

ZERO_EFFECTS:
HIGHLEVEL_CALLS=0
REAL_SECRET_PAYLOAD_READS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
```

STOP before:

- service account creation
- IAM mutation
- service-account key creation
- secret payload access
- AT8L implementation
- AT8L authorization artifact creation
- live HighLevel execution
- CRM mutation
