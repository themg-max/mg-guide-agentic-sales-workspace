# NW-007 Stage A Bootstrap Proof (Execution Lane)

ARTIFACT_ID=MG_GUIDE_NW007_STAGE_A_BOOTSTRAP_PROOF_V2
ARTIFACT_KIND=STAGE_A_BOOTSTRAP_EXECUTION_PROOF
OWNER_LANE=VS Code / Orchestrator Stage A execution lane
CREATED_AT=2026-08-13T13:15:00-04:00
UPDATED_AT=2026-08-13T13:22:25-04:00

This artifact records the actual post-merge Stage A bootstrap execution for
NW-007. All mutations are bounded to the authority in PR #27 and the signed
grant in PR #26. No image build, Cloud Run deployment, Firestore write,
Secret Manager mutation, CRM mutation, customer-data access, or public
unauthenticated access occurred in this lane.

## Parent authority

```
STAGE_A_ACTIVATION_PR=27
STAGE_A_ACTIVATION_MERGE_SHA=6a04999e3eec8f476def821796410754b5c6c366
STAGE_A_ACTIVATION_MERGED_AT=2026-08-13T17:13:20Z
SIGNED_GRANT_PR=26
SIGNED_GRANT_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
```

## Execution window

```
STAGE_A_EXECUTION_STARTED_AT=2026-08-13T17:19:20Z
STAGE_A_EXECUTION_COMPLETED_AT=2026-08-13T17:22:25Z
```

## Required preflight

Commands executed:

```bash
pwd
# /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git branch --show-current
# plan/nw007-stage-a-bootstrap-execution-proof

git status --short --untracked-files=all
# (empty)
```

Preflight result: branch is not `main`, working tree is clean.

## Stage A bootstrap authority retained

```
API_ENABLEMENT_AUTHORIZED=YES
IAM_MUTATION_AUTHORIZED=YES
SERVICE_ACCOUNT_CREATION_AUTHORIZED=YES
ARTIFACT_REGISTRY_CREATION_AUTHORIZED=YES
IAP_CONFIGURATION_AUTHORIZED=YES
IMAGE_BUILD_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

## Execution guardrails in force

```
IMAGE_BUILDS=0
CLOUD_RUN_DEPLOYMENTS=0
FIRESTORE_RUNTIME_WRITES=0
GHL_CRM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0
REAL_CUSTOMER_DATA=0
PUBLIC_UNAUTHENTICATED_ACCESS=NO
SELF_ACTIVATION=FORBIDDEN
SERVICE_ACCOUNT_KEYS_CREATED=0
LIVE_GEMINI_MODE=NO
PRODUCTION_PROMOTION=NO
```

---

## 1. API enablement

Intended effect: enable only `run.googleapis.com`,
`cloudbuild.googleapis.com`, `artifactregistry.googleapis.com`,
`iap.googleapis.com`, and `iam.googleapis.com` in `mg-devpost`.

Command:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com iap.googleapis.com iam.googleapis.com \
  --project=mg-devpost
```

Before state: none of the five APIs were enabled (service-list filters returned
empty; Artifact Registry and Cloud Run API calls returned `SERVICE_DISABLED`).

Result:

```
Operation "operations/acf.p2-985566250549-6aea4cce-ddea-4d04-81c2-ff03fdcbe3da" finished successfully.
```

After state:

```
artifactregistry.googleapis.com
cloudbuild.googleapis.com
iam.googleapis.com
iap.googleapis.com
run.googleapis.com
```

Created vs reused vs skipped: created (enabled) five APIs; no other APIs enabled.
Unexpected conditions: API enablement auto-provisioned Google-managed service
agent roles (e.g., `roles/artifactregistry.serviceAgent`,
`roles/cloudbuild.serviceAgent`, `roles/run.serviceAgent`). These are
Google-managed and out of scope for the user-managed cap.

```
API_ENABLEMENT_RESULT=SUCCESS
```

---

## 2. Artifact Registry inspection and conditional repository creation

After `artifactregistry.googleapis.com` succeeded, the lane inspected
repositories in `us-east4`.

Command:

```bash
gcloud artifacts repositories list --project=mg-devpost --location=us-east4
```

Before state: API disabled; listing failed with `PERMISSION_DENIED` /
`SERVICE_DISABLED`.

After API enablement, listing result: zero repositories in `us-east4`.

Because no approved repository existed after successful inspection, the lane
created one repository as authorized.

Command:

```bash
gcloud artifacts repositories create mg-guide-judge --project=mg-devpost \
  --repository-format=docker --location=us-east4 \
  --description='NW-007 judge surface Artifact Registry repository (us-east4)'
```

Result:

```
Create request issued for: [mg-guide-judge]
Waiting for operation [projects/mg-devpost/locations/us-east4/operations/1d6698eb-6495-4d08-a16a-db71abda5896] to complete...
done.
Created repository [mg-guide-judge].
```

After state:

```
REPOSITORY      FORMAT  MODE                 DESCRIPTION
mg-guide-judge  DOCKER  STANDARD_REPOSITORY  NW-007 judge surface Artifact Registry repository (us-east4)
```

Created vs reused vs skipped: created one repository (`mg-guide-judge`);
`MAX_AR_REPOSITORIES_CREATED=1` not exceeded.

```
AR_INSPECTION_RESULT=0_REPOS_BEFORE_CREATION
AR_REPOSITORY_CREATED=YES
AR_CREATION_COUNT_USED=1
```

---

## 3. Service account creation

Intended effect: create exactly the two named user-managed service accounts,
with zero user-managed keys.

Commands:

```bash
gcloud iam service-accounts create mg-guide-devpost-build --project=mg-devpost \
  --display-name='NW-007 Cloud Build service account'

gcloud iam service-accounts create mg-guide-devpost-runtime --project=mg-devpost \
  --display-name='NW-007 Cloud Run runtime service account'
```

Before state: neither account existed.

Result: both created successfully.

After state:

```
mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com    NW-007 Cloud Build service account
mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com  NW-007 Cloud Run runtime service account
```

Key inspection (user-managed only):

```bash
gcloud iam service-accounts keys list \
  --iam-account=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com \
  --project=mg-devpost --filter='keyType=USER_MANAGED'

gcloud iam service-accounts keys list \
  --iam-account=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com \
  --project=mg-devpost --filter='keyType=USER_MANAGED'
```

Both returned empty tables. Each service account has two `SYSTEM_MANAGED`,
`GOOGLE_PROVIDED` keys auto-provisioned by GCP; these are not user-managed JSON
keys and are not counted against the grant's key prohibition.

```
BUILD_SA_CREATED=YES
RUNTIME_SA_CREATED=YES
SERVICE_ACCOUNT_KEYS_CREATED=0
```

---

## 4. IAM bindings

Applied only the rows authorized by the signed grant (PR #26).

### Applied bindings

#### B1 — build SA writer on `mg-guide-judge`

Command:

```bash
gcloud artifacts repositories add-iam-policy-binding mg-guide-judge \
  --project=mg-devpost --location=us-east4 \
  --member=serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com \
  --role=roles/artifactregistry.writer
```

Before state: repository did not exist; no bindings.
After state: binding present on repository IAM.

Result repository IAM:

```yaml
bindings:
- members:
  - serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
  role: roles/artifactregistry.writer
```

#### B2 — build SA `roles/logging.logWriter` at project

Command:

```bash
gcloud projects add-iam-policy-binding mg-devpost \
  --member=serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com \
  --role=roles/logging.logWriter
```

Result: binding present in project IAM.

#### D1 — deployment principal `roles/iam.serviceAccountUser` on build SA

Command:

```bash
gcloud iam service-accounts add-iam-policy-binding \
  mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com \
  --project=mg-devpost --member=user:themg@themiliare-group.com \
  --role=roles/iam.serviceAccountUser
```

Result: binding present on build SA IAM.

#### D2 — deployment principal `roles/iam.serviceAccountUser` on runtime SA

Command:

```bash
gcloud iam service-accounts add-iam-policy-binding \
  mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com \
  --project=mg-devpost --member=user:themg@themiliare-group.com \
  --role=roles/iam.serviceAccountUser
```

Result: binding present on runtime SA IAM.

#### D3 — deployment principal Cloud Build submission authority

Command:

```bash
gcloud projects add-iam-policy-binding mg-devpost \
  --member=user:themg@themiliare-group.com \
  --role=roles/cloudbuild.builds.editor
```

Result: binding present in project IAM.

#### D4 — deployment principal Cloud Run deploy authority (service-scoped)

Command:

```bash
gcloud projects add-iam-policy-binding mg-devpost \
  --member=user:themg@themiliare-group.com --role=roles/run.developer \
  --condition='expression=resource.name == "projects/mg-devpost/locations/us-east4/services/mg-guide-agentic-sales-workspace-judge",title=NW007 judge service only,description=Restricts Cloud Run deploy authority to the authorized judge service'
```

Result: conditional binding present in project IAM. The condition restricts the
role to the authorized Cloud Run service, matching the grant's
`AUTHORIZED_SERVICE` scope.

#### D5 — deployment principal Artifact Registry reader on `mg-guide-judge`

Command:

```bash
gcloud artifacts repositories add-iam-policy-binding mg-guide-judge \
  --project=mg-devpost --location=us-east4 \
  --member=user:themg@themiliare-group.com \
  --role=roles/artifactregistry.reader
```

Result: binding present on repository IAM.

### Skipped bindings

- **B3** (`roles/storage.objectViewer` on a Cloud Build source bucket) skipped
  because the Stage A lane does not perform a build and no source bucket is in
  use. The conditional binding will be applied only if the chosen Stage B build
  path requires it.
- **J1** (`roles/iap.httpsResourceAccessor` for the judge group) skipped because
  the authorized Cloud Run service `mg-guide-agentic-sales-workspace-judge` does
  not yet exist. It will be applied to the service's IAP policy during Stage B
  deployment.
- **IAP1** (`roles/run.invoker` for the Google-managed IAP service agent on the
  Cloud Run service) skipped for the same reason: no Cloud Run service exists yet.

Project IAM after all bindings (relevant excerpts):

```json
{
  "bindings": [
    {
      "members": ["serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com"],
      "role": "roles/logging.logWriter"
    },
    {
      "members": ["user:themg@themiliare-group.com"],
      "role": "roles/cloudbuild.builds.editor"
    },
    {
      "condition": {
        "description": "Restricts Cloud Run deploy authority to the authorized judge service",
        "expression": "resource.name == \"projects/mg-devpost/locations/us-east4/services/mg-guide-agentic-sales-workspace-judge\"",
        "title": "NW007 judge service only"
      },
      "members": ["user:themg@themiliare-group.com"],
      "role": "roles/run.developer"
    }
  ]
}
```

Repository IAM after bindings:

```json
{
  "bindings": [
    {
      "members": ["user:themg@themiliare-group.com"],
      "role": "roles/artifactregistry.reader"
    },
    {
      "members": ["serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com"],
      "role": "roles/artifactregistry.writer"
    }
  ]
}
```

```
IAM_BINDINGS_RESULT=APPLIED_B1_B2_D1_D2_D3_D4_D5_SKIPPED_B3_J1_IAP1_PREREQUISITE_MISSING
```

---

## 5. IAP and OAuth configuration

Configuration recorded (no legacy IAP OAuth Admin API automation used):

```
IAP_MODE=DIRECT_CLOUD_RUN
IAP_OAUTH_MODE=CUSTOM
CUSTOM_OAUTH_CREATION_PATH=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW=ACTIVE
LEGACY_IAP_OAUTH_ADMIN_API_USED=NO
```

Because the authorized Cloud Run service does not exist yet, direct Cloud Run IAP
could not be enabled on a service in this lane. The IAP application settings were
inspected after enabling `iap.googleapis.com`:

```bash
gcloud iap settings get --project=mg-devpost --format=json
```

Result:

```json
{
  "name": "projects/985566250549"
}
```

Custom OAuth client creation is intentionally deferred to the current Google
Auth Platform / IAP console flow, per the signed grant's `CUSTOM_OAUTH_CREATION_PATH`.

```
IAP_CONFIGURATION_RESULT=DIRECT_CLOUD_RUN_MODE_RECORDED_SERVICE_NOT_YET_CREATED
CUSTOM_OAUTH_CONFIGURATION_RESULT=CURRENT_FLOW_DEFERRED_TO_CONSOLE_NO_API_AUTOMATION
JUDGE_ACCESS_BINDING_RESULT=SKIPPED_SERVICE_ABSENT_WILL_BIND_DURING_STAGE_B
```

---

## 6. Temporary bootstrap authority cleanup

The bootstrap operator is `user:themg@themiliare-group.com`, who holds
`roles/owner` on `mg-devpost`. No separate BS1–BS7 role bindings were added
during this lane because owner authority already covers the required bootstrap
actions. To satisfy the signed grant's `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES`
requirement, the lane attempted removal of each temporary bootstrap role from
the operator:

```bash
for ROLE in roles/serviceusage.serviceUsageAdmin roles/artifactregistry.admin \
  roles/iam.serviceAccountAdmin roles/resourcemanager.projectIamAdmin \
  roles/iap.admin roles/oauthconfig.editor roles/run.admin; do
  gcloud projects remove-iam-policy-binding mg-devpost \
    --member=user:themg@themiliare-group.com --role=$ROLE
done
```

Each command exited `0` with no policy change because the roles were not present
as separate bindings.

After cleanup, the operator's explicit project-level bindings remain:

```
roles/cloudbuild.builds.editor
roles/owner
roles/run.developer (condition: resource.name == "projects/mg-devpost/locations/us-east4/services/mg-guide-agentic-sales-workspace-judge")
```

The deployment-principal bindings (`cloudbuild.builds.editor` and conditional
`run.developer`) are standing while the grant is active and are not temporary
bootstrap authority.

```
TEMPORARY_BOOTSTRAP_AUTHORITY_CLEANUP_RESULT=NO_SEPARATE_BS_BINDINGS_TO_REVOKE_CEASE_USE_RECORDED
```

---

## 7. Prohibited-effect verification

No prohibited mutations occurred:

```
IMAGE_BUILDS=0
CLOUD_RUN_DEPLOYMENTS=0
FIRESTORE_RUNTIME_WRITES=0
GHL_CRM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0
REAL_CUSTOMER_DATA=0
SERVICE_ACCOUNT_KEYS_CREATED=0
LIVE_GEMINI_MODE=NO
PRODUCTION_PROMOTION=NO
PUBLIC_UNAUTHENTICATED_ACCESS=NO
```

---

## Final state summary

| Resource | Before | After |
| --- | --- | --- |
| Required APIs enabled | none | all 5 enabled |
| AR repos in `us-east4` | 0 | 1 (`mg-guide-judge`, docker) |
| Build SA | absent | created, no user-managed keys |
| Runtime SA | absent | created, no user-managed keys |
| B1 (AR writer on repo) | absent | applied |
| B2 (logWriter) | absent | applied |
| B3 (storage.objectViewer) | absent | skipped (no source bucket) |
| D1/D2 (serviceAccountUser) | absent | applied |
| D3 (cloudbuild.builds.editor) | absent | applied |
| D4 (run.developer, service-scoped) | absent | applied with condition |
| D5 (AR reader on repo) | absent | applied |
| J1 (iap.httpsResourceAccessor) | absent | skipped (service absent) |
| IAP1 (IAP SA run.invoker) | absent | skipped (service absent) |
| Cloud Run services in `us-east4` | 0 | 0 (not created in Stage A) |
| Bootstrap admin roles on operator | owner only | owner only; temporary roles not added |

---

## Final proof fields

```
STAGE_A_EXECUTION_STARTED_AT=2026-08-13T17:19:20Z
STAGE_A_EXECUTION_COMPLETED_AT=2026-08-13T17:22:25Z

API_ENABLEMENT_RESULT=SUCCESS
AR_INSPECTION_RESULT=0_REPOS_BEFORE_CREATION
AR_REPOSITORY_CREATED=YES
AR_CREATION_COUNT_USED=1

BUILD_SA_CREATED=YES
RUNTIME_SA_CREATED=YES
SERVICE_ACCOUNT_KEYS_CREATED=0

IAM_BINDINGS_RESULT=APPLIED_B1_B2_D1_D2_D3_D4_D5_SKIPPED_B3_J1_IAP1_PREREQUISITE_MISSING
IAP_CONFIGURATION_RESULT=DIRECT_CLOUD_RUN_MODE_RECORDED_SERVICE_NOT_YET_CREATED
CUSTOM_OAUTH_CONFIGURATION_RESULT=CURRENT_FLOW_DEFERRED_TO_CONSOLE_NO_API_AUTOMATION
JUDGE_ACCESS_BINDING_RESULT=SKIPPED_SERVICE_ABSENT_WILL_BIND_DURING_STAGE_B

TEMPORARY_BOOTSTRAP_AUTHORITY_CLEANUP_RESULT=NO_SEPARATE_BS_BINDINGS_TO_REVOKE_CEASE_USE_RECORDED

IMAGE_BUILDS=0
CLOUD_RUN_DEPLOYMENTS=0
FIRESTORE_RUNTIME_WRITES=0
GHL_CRM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0
REAL_CUSTOMER_DATA=0
PUBLIC_UNAUTHENTICATED_ACCESS=NO

STAGE_A_FINAL_DISPOSITION=BOOTSTRAP_SETUP_COMPLETE_NO_BUILD_NO_DEPLOY
```

---

STOP_CODE=NW007_STAGE_A_BOOTSTRAP_EXECUTION_COMPLETE_READY_FOR_PROOF_REVIEW
