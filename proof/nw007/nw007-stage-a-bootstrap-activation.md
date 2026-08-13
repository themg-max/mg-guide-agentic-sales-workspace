# NW-007 Stage A — Bootstrap Activation Authorization Artifact

ARTIFACT_ID=MG_GUIDE_NW007_STAGE_A_BOOTSTRAP_ACTIVATION_V1
ARTIFACT_KIND=BOOTSTRAP_ONLY_ACTIVATION
OWNER_LANE=VS Code / Orchestrator authorization lane
CREATED_AT=2026-08-13

This artifact is **authorization-only planning for Stage A bootstrap execution**.
It does not perform any cloud mutation. It inherits parent authority without
expansion from the signed NW-007 grant and authorizes only the Stage A
bootstrap effects listed below.

## Parent grant baseline

```
PARENT_SIGNED_GRANT_PR=26
PARENT_SIGNED_GRANT_HEAD_SHA=49caef4a441943af350d44a2c5755bec14fdd3bf
PARENT_SIGNED_GRANT_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
PARENT_SIGNED_GRANT_MERGED_AT=2026-08-13T16:58:41Z
PARENT_SIGNED_GRANT_PATH=proof/nw007/nw007-cloud-run-human-execution-grant.md
PARENT_SIGNED_GRANT_STOP_CODE=NW007_SIGNED_GRANT_READY_FOR_DURABLE_PR
STAGE=NW007_STAGE_A_BOOTSTRAP
```

## Stage A activation state

```
API_ENABLEMENT_AUTHORIZED=YES
IAM_MUTATION_AUTHORIZED=YES
SERVICE_ACCOUNT_CREATION_AUTHORIZED=YES
ARTIFACT_REGISTRY_CREATION_AUTHORIZED=YES
IAP_CONFIGURATION_AUTHORIZED=YES
IMAGE_BUILD_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

The only Stage A bootstrap effects authorized are:

```
STAGE_A_BOOTSTRAP_EFFECTS_REQUESTED=
enable_enumerated_apis;
inspect_and_create_one_ar_repo_if_absent;
create_build_sa;
create_runtime_sa;
bind_only_enumerated_roles;
configure_direct_cloud_run_iap;
configure_custom_oauth;
bind_judge_access
```

Must remain NO / FORBIDDEN under this stage:

```
IMAGE_BUILD_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
FIRESTORE_RUNTIME_WRITES=NO
GHL_CRM_MUTATION=NO
REAL_CUSTOMER_DATA=NO
SECRET_MANAGER_MUTATION=NO
LIVE_GEMINI_MODE=NO
PUBLIC_UNAUTHENTICATED_ACCESS=NO
SELF_ACTIVATION=FORBIDDEN
```

This activation must inherit without expansion:

```
AUTHORIZED_PROJECT=mg-devpost
AUTHORIZED_REGION=us-east4
AUTHORIZED_SERVICE=mg-guide-agentic-sales-workspace-judge
AUTHORIZED_AR_REPOSITORY=mg-guide-judge
BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL_CLASS=GOOGLE_GROUP
JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED
IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
IAP_OAUTH_MODE=CUSTOM
CUSTOM_OAUTH_CLIENT_REQUIRED=YES
CUSTOM_OAUTH_CREATION_PATH=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO
MAX_AR_REPOSITORIES_CREATED=1
MAX_BUILD_SERVICE_ACCOUNTS_CREATED=1
MAX_RUNTIME_SERVICE_ACCOUNTS_CREATED=1
MAX_CLOUD_RUN_SERVICES_CREATED=1
MAX_CLOUD_RUN_INSTANCES=1
```

Exact IAM manifest inheritance (unchanged):

- B1–B3 build SA roles remain in-force under the same repository/project scope.
- D1–D5 deployment principal roles remain limited to the same authorized
  service / repo / runtime / build relationship.
- J1 and IAP1 remain exact and scoped to the authorized judge service.
- BS1–BS7 remain temporary bootstrap authority only; no permanent deployer
  role expansion is added.
- The Stage A activation does not add, remove, or reinterpret any parent grant
  binding, cap, or lifecycle rule.

Protected effects remain NO:

```
FIRESTORE_RUNTIME_WRITES=NO
GHL_CRM_MUTATION=NO
REAL_CUSTOMER_DATA=NO
PUBLIC_UNAUTHENTICATED_ACCESS=NO
SERVICE_ACCOUNT_KEYS=FORBIDDEN
SECRET_MANAGER_MUTATION=NO
LIVE_GEMINI_MODE=NO
VERTEX_AI_ROLES=NO
PRODUCTION_PROMOTION=NO
```

## Lifecycle and cleanup

```
GRANT_LIFETIME=DEVPOST_COMPETITION_ONLY
CLEANUP_REQUIRED=YES
POST_HACKATHON_REVIEW_REQUIRED=YES
RETENTION_REQUIRES_EXPLICIT_CLOSEOUT_DECISION=YES
```

This Stage A activation is confined to bootstrap setup only. It does not permit
build or deployment effects, and it preserves the signed grant lifecycle and
cleanup obligations for the competition-only deployment window.

---

STOP_CODE=NW007_STAGE_A_BOOTSTRAP_ACTIVATION_READY_FOR_REVIEW
