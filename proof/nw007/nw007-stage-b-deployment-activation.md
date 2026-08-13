# NW-007 Stage B — Deployment Activation Authorization Artifact

ARTIFACT_ID=MG_GUIDE_NW007_STAGE_B_DEPLOYMENT_ACTIVATION_V1
ARTIFACT_KIND=DEPLOYMENT_ACTIVATION_AUTHORIZATION
OWNER_LANE=VS Code / Orchestrator Stage B authorization lane
CREATED_AT=2026-08-13

This artifact is **authorization-only planning for Stage B deployment
activation**. Creating or merging this artifact does **not** perform image
build, image push, Cloud Run deployment, J1/IAP1 mutations, IAP enablement, or
OAuth mutation. Those effects remain deferred until a separate, explicitly
authorized Stage B execution lane runs under this activation and the parent
signed grant.

## Parent authority chain (exact)

```
SIGNED_GRANT_PR=26
SIGNED_GRANT_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
SIGNED_GRANT_PATH=proof/nw007/nw007-cloud-run-human-execution-grant.md

STAGE_A_ACTIVATION_PR=27
STAGE_A_ACTIVATION_MERGE_SHA=6a04999e3eec8f476def821796410754b5c6c366
STAGE_A_ACTIVATION_PATH=proof/nw007/nw007-stage-a-bootstrap-activation.md

STAGE_A_PROOF_PR=28
STAGE_A_PROOF_HEAD_SHA=39e290a3578253a1f23594e75d60f056bf3f0bb3
STAGE_A_PROOF_MERGE_SHA=dc524f227eee5e52d2c41e55c33344628d318224
STAGE_A_PROOF_MERGED_AT=2026-08-13T17:37:37Z
STAGE_A_PROOF_PATH=proof/nw007/nw007-stage-a-bootstrap-proof.md

STAGE=NW007_STAGE_B_DEPLOYMENT_ACTIVATION
SELF_ACTIVATION=FORBIDDEN
```

Stage A final disposition carried forward without reinterpretation:

```
STAGE_A_FINAL_DISPOSITION=BOOTSTRAP_CORE_COMPLETE_SERVICE_DEPENDENCIES_DEFERRED
STAGE_A_COMPLETED=API_ENABLEMENT;AR_INSPECT_AND_CREATE;BUILD_SA_CREATE;RUNTIME_SA_CREATE;B1;B2;D1;D2;D3;D4;D5
```

## Human activation decision (provenance only)

```
REQUESTED_DECISION=ACTIVATE_NW007_STAGE_B_DEPLOYMENT_UNDER_SIGNED_GRANT_PR26_AND_STAGE_A_PROOF_PR28
CURRENT_DECISION=APPROVED

HUMAN_ACTIVATION=APPROVED
ACTIVATED_BY=AARON PRESTON CHANDLER
ACTIVATED_AT=2026-08-13T13:44:57.012-04:00
ACTIVATION_OWNER=VS Code / Orchestrator Stage B authorization lane

PARENT_AUTHORITY_PR=26
PARENT_AUTHORITY_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
STAGE_A_PROOF_PR=28
STAGE_A_PROOF_MERGE_SHA=dc524f227eee5e52d2c41e55c33344628d318224

SELF_ACTIVATION=FORBIDDEN
```

Actual human approval is recorded above. This artifact does not self-activate,
never attributes ChatGPT reviewer disposition as human approval, and does not
expand the signed grant.

## Stage A → Stage B carry-forward (exact)

```
STAGE_B_BUILD_CONDITIONAL=
B3_IF_SOURCE_BUCKET_REQUIRED

STAGE_B_POST_SERVICE_CREATE_REQUIRED=
J1;
IAP1;
DIRECT_CLOUD_RUN_IAP_ENABLEMENT;
JUDGE_ACCESS_BINDING

STAGE_B_PRE_JUDGE_REQUIRED=
CUSTOM_OAUTH_CLIENT_CONFIGURATION;
IAP_AUTHENTICATED_ACCESS_VERIFICATION
```

These strings are inherited exactly from the Stage A proof final fields. Stage B
execution may satisfy them only within the hard constraints below and only after
this activation is approved and merged.

```
STAGE_B_EXECUTION_SEQUENCE=
B1_REPO_IMPLEMENTATION;
B2_CLOUD_DEPLOYMENT

STAGE_B_B1_SCOPE=
HTTP_ADAPTER_IMPLEMENTATION;
DOCKERFILE_CONTAINER_PACKAGING;
TESTS;
IMPLEMENTATION_PR

STAGE_B_B1_CLOUD_MUTATION=NO

STAGE_B_B2_PREREQUISITE=
APPROVED_AND_MERGED_STAGE_B_IMPLEMENTATION_PR

STAGE_B_B2_SCOPE=
CLOUD_BUILD;
IMAGE_PUSH;
CLOUD_RUN_DEPLOYMENT;
CONDITIONAL_B3;
J1;
IAP1;
DIRECT_CLOUD_RUN_IAP_ENABLEMENT;
CUSTOM_OAUTH_CONFIGURATION;
JUDGE_ACCESS_BINDING;
SYNTHETIC_AUTHENTICATED_SMOKE_TESTS

B2_EXECUTION_MUST_RECORD_AND_VERIFY_IMPLEMENTATION_PR_MERGE_SHA=YES
B2_EXECUTION_MUST_VERIFY_IMPLEMENTATION_PR_MERGE_SHA_BEFORE_CLOUD_BUILD_OR_DEPLOYMENT_MUTATION=YES
```

B1 is the repository implementation lane only. B1 must not mutate cloud
resources. B2 is the cloud deployment lane and must record and verify the exact
implementation PR merge SHA before any Cloud Build or deployment mutation occurs.

## Stage B activation state (authorization intent)

```
IMAGE_BUILD_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
IMAGE_PUSH_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
DEPLOYMENT_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
HTTP_ADAPTER_IMPLEMENTATION_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
DOCKERFILE_CONTAINER_PACKAGING_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
CLOUD_BUILD_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
RUNTIME_SA_ATTACHMENT_AUTHORIZED=YES_AFTER_ACTIVATION_MERGE_AND_EXECUTION_LANE
CONDITIONAL_B3_AUTHORIZED=YES_IF_SOURCE_BUCKET_REQUIRED
J1_AUTHORIZED=YES_AFTER_SERVICE_EXISTS
IAP1_AUTHORIZED=YES_AFTER_SERVICE_EXISTS
DIRECT_CLOUD_RUN_IAP_ENABLEMENT_AUTHORIZED=YES_AFTER_SERVICE_EXISTS
CUSTOM_OAUTH_CONFIGURATION_AUTHORIZED=YES_CURRENT_CONSOLE_FLOW_ONLY
JUDGE_GROUP_AUTHENTICATED_ACCESS_AUTHORIZED=YES
SYNTHETIC_SMOKE_TESTS_AUTHORIZED=YES
```

While this PR is open (authorization artifact only), all of the following remain
**not performed by this lane**:

```
IMAGE_BUILD_PERFORMED_BY_THIS_ARTIFACT=NO
IMAGE_PUSH_PERFORMED_BY_THIS_ARTIFACT=NO
CLOUD_RUN_DEPLOYMENT_PERFORMED_BY_THIS_ARTIFACT=NO
J1_IAP1_MUTATION_PERFORMED_BY_THIS_ARTIFACT=NO
IAP_ENABLEMENT_PERFORMED_BY_THIS_ARTIFACT=NO
OAUTH_MUTATION_PERFORMED_BY_THIS_ARTIFACT=NO
```

## Stage B requested capabilities (may include)

Under parent grant PR #26 and after this activation is approved/merged, a
separate Stage B execution lane may implement only:

- HTTP adapter implementation for the judge-safe surface
- Dockerfile / container packaging
- Cloud Build of the authorized image path
- Image push to existing Artifact Registry repository `mg-guide-judge`
- Creation/update of **one** Cloud Run service
  `mg-guide-agentic-sales-workspace-judge` in `us-east4`
- Runtime service account attachment
  (`mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com`)
- Conditional B3 (`roles/storage.objectViewer` on build SA) **only if** a source
  bucket is required for the frozen build path
- J1 (`roles/iap.httpsResourceAccessor` for judge group on the authorized
  service IAP policy)
- IAP1 (Google-managed IAP service agent `roles/run.invoker` on the authorized
  service)
- Direct Cloud Run IAP enablement (`IAP_MODE=DIRECT_CLOUD_RUN`,
  `LOAD_BALANCER_REQUIRED=NO`)
- Current custom OAuth client configuration path (console / Google Auth Platform
  current flow; no legacy IAP OAuth Admin API automation)
- Judge-group authenticated access binding
  (`group:mg-mcp-developer-mg@themiliare-group.com`)
- Synthetic smoke tests only (no real customer data)

## Hard constraints (inherit without expansion)

```
AUTHORIZED_PROJECT=mg-devpost
AUTHORIZED_REGION=us-east4
AUTHORIZED_SERVICE=mg-guide-agentic-sales-workspace-judge
AUTHORIZED_AR_REPOSITORY=mg-guide-judge

BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
DEPLOYMENT_PRINCIPAL=user:themg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL_CLASS=GOOGLE_GROUP
JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED

IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
IAP_OAUTH_MODE=CUSTOM
CUSTOM_OAUTH_CLIENT_REQUIRED=YES
CUSTOM_OAUTH_CREATION_PATH=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO

MAX_CLOUD_RUN_SERVICES_CREATED=1
MAX_CLOUD_RUN_INSTANCES=1
MIN_CLOUD_RUN_INSTANCES=0
MAX_AR_REPOSITORIES_CREATED=1
```

Protected effects remain NO / FORBIDDEN:

```
FIRESTORE_RUNTIME_WRITES=NO
GHL_CRM_MUTATION=NO
REAL_CUSTOMER_DATA=NO
SECRET_MANAGER_MUTATION=NO
LIVE_GEMINI_MODE=NO
PUBLIC_UNAUTHENTICATED_ACCESS=NO
PRODUCTION_PROMOTION=NO
SERVICE_ACCOUNT_KEYS=FORBIDDEN
SELF_ACTIVATION=FORBIDDEN
VERTEX_AI_ROLES=NO
```

## IAM / post-create obligations (exact, deferred to execution)

Standing parent-grant rows remain in force. Stage B execution must complete only
the deferred/conditional rows carried from Stage A proof:

| ID | Status entering Stage B | Stage B obligation |
| --- | --- | --- |
| B1–B2 | Applied in Stage A | Retain; do not broaden |
| B3 | Skipped (no source bucket) | Apply **only if** source bucket is required for frozen build path |
| D1–D5 | Applied in Stage A | Retain; use for authorized build/deploy only |
| J1 | Skipped (service absent) | Apply after authorized Cloud Run service exists |
| IAP1 | Skipped (service absent) | Apply after authorized Cloud Run service exists |
| Direct Cloud Run IAP | Mode recorded; service absent | Enable only on `AUTHORIZED_SERVICE` after create |
| Custom OAuth | Deferred to current console flow | Configure before judge authenticated-access verification |
| Judge access binding | Skipped (service absent) | Bind judge group only; never `allUsers` / `allAuthenticatedUsers` |

No new principals, roles, projects, regions, services, or repositories may be
introduced beyond the parent signed grant.

## Explicit non-actions for this authorization PR

This Stage B authorization lane **must not** perform:

- image build
- image push
- Cloud Run deployment / service create
- J1 / IAP1 IAM mutations
- IAP enablement on Cloud Run
- OAuth client creation or mutation
- Secret Manager, Firestore, GHL/CRM, or production promotion actions

Those actions require a later execution lane operating only after this
activation artifact is approved and merged.

## Lifecycle and cleanup

```
GRANT_LIFETIME=DEVPOST_COMPETITION_ONLY
CLEANUP_REQUIRED=YES
POST_HACKATHON_REVIEW_REQUIRED=YES
RETENTION_REQUIRES_EXPLICIT_CLOSEOUT_DECISION=YES
```

Stage B inherits the competition-only lifetime and cleanup obligations of the
signed grant. Approval of this activation does not authorize production
promotion or permanent retention.

## Merge return block (Stage A proof already merged)

```
STAGE_A_PROOF_PR=28
STAGE_A_PROOF_HEAD_SHA=39e290a3578253a1f23594e75d60f056bf3f0bb3
STAGE_A_PROOF_MERGE_SHA=dc524f227eee5e52d2c41e55c33344628d318224
STAGE_A_PROOF_MERGED_AT=2026-08-13T17:37:37Z
```

## Stop / handoff

```
STOP_CODE=NW007_STAGE_B_DEPLOYMENT_ACTIVATION_READY_FOR_REVIEW
NEXT_ACTION=REVIEWER_DISPOSITION_ON_STAGE_B_AUTHORIZATION_PR
BUILD_OR_DEPLOY_NOW=NO
```

---

STOP_CODE=NW007_STAGE_B_DEPLOYMENT_ACTIVATION_READY_FOR_REVIEW
