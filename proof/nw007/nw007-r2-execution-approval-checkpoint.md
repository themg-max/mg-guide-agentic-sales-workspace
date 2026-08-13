# NW-007 R2 Execution-Approval Proof Checkpoint

```text
STOP_CODE=NW007_R2_SIGNED_APPROVAL_READY_FOR_FINAL_REVIEW
ARTIFACT_KIND=R2_EXECUTION_APPROVAL_CHECKPOINT
OWNER_LANE=VS Code / Orchestrator R2 planning/proof lane
CREATED_AT=2026-08-13T20:44:00Z
UPDATED_AT=2026-08-13T21:02:00Z
```

This artifact is **planning/approval only**. Creating, reviewing, or merging it
does **not** execute R2 cloud mutation. Human R2 execution approval has been
signed; execution remains blocked until the signed approval is merged.

```text
R2_EXECUTION_SELF_ACTIVATION=FORBIDDEN
CLOUD_MUTATION=NONE
```

## Authority binding

```text
AUTHORIZATION_PR=32
AUTHORIZATION_MERGE_SHA=031b99a2df02dde358f99582622fd351eed1368e
R1_IMPLEMENTATION_PR=33
R1_IMPLEMENTATION_HEAD_SHA=9dac58e058540f017dea942fe5a54fe40dc57b99
R1_IMPLEMENTATION_MERGE_SHA=d3f752b907bc8c6e0586fb45fc46cb08b933a530
R1_IMPLEMENTATION_MERGED_AT=2026-08-13T20:28:26Z
R1_IMPLEMENTATION_CI_RUN=31740101261
R1_IMPLEMENTATION_CI_RESULT=SUCCESS
```

Exact-head review evidence retained from the reviewed PR state:

```text
REVIEWER_DISPOSITION=APPROVE
PR33_REVIEWED_HEAD_SHA=9dac58e058540f017dea942fe5a54fe40dc57b99
PR33_EXACT_HEAD_CI_RUN=31740101261
PR33_EXACT_HEAD_CI_RESULT=SUCCESS
```

GitHub merge provenance as recorded from the actual merged PR state:

```text
PR33_ACTUAL_GITHUB_STATE=MERGED
PR33_ACTUAL_MERGE_COMMIT=d3f752b907bc8c6e0586fb45fc46cb08b933a530
PR33_ACTUAL_MERGED_AT=2026-08-13T20:28:26Z
PR33_ACTUAL_BASE_SHA=031b99a2df02dde358f99582622fd351eed1368e
PR33_ACTUAL_HEAD_SHA=9dac58e058540f017dea942fe5a54fe40dc57b99
```

Human merge authority requirement satisfied by recorded GitHub provenance; the
pre-merge prospective merge_commit_sha was not used.

## Main sync and ancestry verification

```bash
git checkout main
git pull --ff-only origin main
git rev-parse HEAD
```

Observed state:

```text
CURRENT_MAIN_HEAD=d3f752b907bc8c6e0586fb45fc46cb08b933a530
MAIN_ANCESTRY_CHECK=PASS
ACTUAL_PR33_MERGE_SHA_IS_IN_MAIN_ANCESTRY=YES
```

## Fresh non-main proof branch

```bash
pwd
git branch --show-current
git status --short --untracked-files=all
```

Observed state:

```text
PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH=plan/nw007-r2-execution-approval
STATUS=(clean before this checkpoint update; only this artifact is in scope)
```

This branch was created after syncing `main` and before any write/mutation
activity in this R2 approval lane. Abort conditions (on `main`, unrelated
changes) were not met.

## R2 target binding

```text
PROJECT=mg-devpost
REGION=us-east4
SERVICE=mg-guide-agentic-sales-workspace-judge
AR_REPOSITORY=mg-guide-judge
RUNTIME_SA=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_INSTANCES=0
MAX_INSTANCES=1
```

## R2 planned scope

```text
R2_PLANNED_SCOPE=
ONE_CLOUD_BUILD
ONE_IMAGE
ONE_PUSH_TO_EXISTING_AR_REPO
ONE_EXISTING_SERVICE_UPDATE
ONE_NEW_REVISION
AUTHENTICATED_SMOKE
```

## Read-only preflight (before human R2 approval)

This checkpoint intentionally includes no mutation or launch commands.
Read-only preflight **passed**. No cloud mutation was performed.

### 1) Current Cloud Run service / revision / digest

```bash
gcloud run services describe mg-guide-agentic-sales-workspace-judge --project=mg-devpost --region=us-east4 --format='value(metadata.name,status.latestReadyRevisionName,status.latestCreatedRevisionName,spec.template.spec.containers[0].image,metadata.annotations."run.googleapis.com/minScale",metadata.annotations."run.googleapis.com/maxScale",metadata.annotations."run.googleapis.com/iap-enabled",metadata.annotations."run.googleapis.com/ingress")'
```

Observed state:

```text
SERVICE_NAME=mg-guide-agentic-sales-workspace-judge
LATEST_READY_REVISION=mg-guide-agentic-sales-workspace-judge-00001-gjl
LATEST_CREATED_REVISION=mg-guide-agentic-sales-workspace-judge-00001-gjl
IMAGE=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge@sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0
MIN_INSTANCES=0
MAX_INSTANCES=1
IAP_ENABLED=true
INGRESS=all
```

### 2) Runtime SA existence and binding

```bash
gcloud iam service-accounts describe mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com --project=mg-devpost --format='value(email,displayName,disabled)'
```

Observed state:

```text
RUNTIME_SA_EMAIL=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
RUNTIME_SA_DISPLAY_NAME=NW-007 Cloud Run runtime service account
RUNTIME_SA_DISABLED=false
```

### 3) Build SA existence

```bash
gcloud iam service-accounts describe mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com --project=mg-devpost --format='value(email,displayName,disabled)'
```

Observed state:

```text
BUILD_SA_EMAIL=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
BUILD_SA_DISPLAY_NAME=NW-007 Cloud Build service account
BUILD_SA_DISABLED=false
```

### 4) Service IAM

```bash
gcloud run services get-iam-policy mg-guide-agentic-sales-workspace-judge --project=mg-devpost --region=us-east4 --format='flattened(bindings)'
```

Observed state:

```text
bindings[0].members[0]: serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com
bindings[0].role: roles/run.invoker
```

No `allUsers` and no `allAuthenticatedUsers` identities are present in the
service IAM policy.

### 5) IAP / custom OAuth state

```bash
gcloud iap settings get --project=mg-devpost --format='json'
gcloud iap oauth-brands list --project=mg-devpost --format='table(name,displayName,createTime)'
```

Observed state:

```json
{
  "name": "projects/985566250549"
}
```

```text
IAP_OAUTH_BRANDS_LIST=DEPRECATED_API_WARNING_ONLY
CUSTOM_OAUTH_CURRENT_CLI_OBSERVABILITY=NOT_AVAILABLE_VIA_DEPRECATED_IAP_OAUTH_ADMIN_API
CUSTOM_OAUTH_B2_VERIFIED_BASELINE=CONFIGURED_AND_AUTHENTICATED_JUDGE_ACCESS_PASS
CUSTOM_OAUTH_DRIFT_INFERRED_FROM_EMPTY_BRAND_QUERY=NO
CUSTOM_OAUTH_RECONFIGURATION_REQUIRED=NO
IAP_RECONFIGURATION_REQUIRED=NO
IAM_RECONFIGURATION_REQUIRED=NO
```

Interpretation (read-only, non-mutating):

- The OAuth brand command emits the deprecation warning for the IAP OAuth Admin
  APIs. No active custom OAuth brand configuration is surfaced by that
  deprecated CLI path. This is an **observability limitation**, not evidence of
  missing OAuth configuration.
- The durable Stage B B2 proof baseline (PR #31) already verified custom OAuth
  configuration and authenticated judge access. That baseline is carried forward
  without reinterpretation.
- Empty brand-query output is **not** treated as drift and does **not** authorize
  OAuth, IAP, or IAM reconfiguration under this R2 approval packet.
- No OAuth/IAP/IAM mutation has been executed in this lane.

### 6) Artifact Registry existing repo

```bash
gcloud artifacts repositories list --project=mg-devpost --location=us-east4 --format='table(name,format,mode,description)'
```

Observed state:

```text
REPOSITORY=mg-guide-judge
FORMAT=DOCKER
MODE=STANDARD_REPOSITORY
DESCRIPTION=NW-007 judge surface Artifact Registry repository (us-east4)
```

### 7) Stub mode and service drift check

```text
MEETING_CONTEXT_GEMINI_MODE=stub
SERVICE_ANNOTATION_run.googleapis.com/iap-enabled=true
SERVICE_ANNOTATION_run.googleapis.com/maxScale=1
SERVICE_ANNOTATION_run.googleapis.com/minScale=0 (effectively absent / default, matching target)
SERVICE_DID_NOT_DRIFT_FROM_EXPECTED_TARGET=YES
```

### 8) No unexpected drift

```text
EXPECTED_PROJECT=mg-devpost
EXPECTED_REGION=us-east4
EXPECTED_SERVICE=mg-guide-agentic-sales-workspace-judge
EXPECTED_AR_REPOSITORY=mg-guide-judge
EXPECTED_RUNTIME_SA=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
EXPECTED_MIN_INSTANCES=0
EXPECTED_MAX_INSTANCES=1
NO_UNEXPECTED_DRIFT=YES
READ_ONLY_PREFLIGHT=PASS
```

## Forbidden actions gate

This checkpoint is intentionally read-only and therefore does not execute any of
the following; human R2 execution approval has been signed, and execution remains
blocked until the signed approval is merged:

- `gcloud builds submit`
- docker/image push to Artifact Registry
- `gcloud run deploy/update`
- IAM mutation
- IAP mutation
- OAuth mutation
- new principal
- new service
- new AR repo
- new SA
- Secret Manager mutation
- Firestore write
- CRM mutation
- live Gemini

```text
R2_EXECUTION_SELF_ACTIVATION=FORBIDDEN
```

## Human R2 approval decision block

```text
R2_REQUESTED_DECISION=APPROVE_BOUNDED_REDEPLOY
CURRENT_DECISION=APPROVED
HUMAN_SIGNATURE=APPROVED
SIGNED_AT=2026-08-13T16:53:03-04:00
SIGNED_BY=Aaron Chandler
R2_EXECUTION_SELF_ACTIVATION=FORBIDDEN
```

Approved scope becomes executable only after this signed approval is merged:

```text
R2_PLANNED_SCOPE=
ONE_CLOUD_BUILD
ONE_IMAGE
ONE_PUSH_TO_EXISTING_AR_REPO
ONE_EXISTING_SERVICE_UPDATE
ONE_NEW_REVISION
AUTHENTICATED_SMOKE
```

Hard constraints that remain in force even after this signed human approval:

```text
PROJECT=mg-devpost
REGION=us-east4
SERVICE=mg-guide-agentic-sales-workspace-judge
AR_REPOSITORY=mg-guide-judge
RUNTIME_SA=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_INSTANCES=0
MAX_INSTANCES=1
CUSTOM_OAUTH_RECONFIGURATION_REQUIRED=NO
IAP_RECONFIGURATION_REQUIRED=NO
IAM_RECONFIGURATION_REQUIRED=NO
```

`CURRENT_DECISION=APPROVED` and `HUMAN_SIGNATURE=APPROVED` are recorded in this
durable artifact. R2 execution remains blocked until this signed approval is
merged:

```text
R2_EXECUTION=BLOCKED
CLOUD_MUTATION=NONE
```

## Human R2 approval request summary

The read-only preflight confirms:

- PR #32 is the authorization authority (`031b99a2df02dde358f99582622fd351eed1368e`)
- PR #33 R1 implementation is merged at actual SHA
  `d3f752b907bc8c6e0586fb45fc46cb08b933a530` and is in `main` ancestry
- PR #33 exact-head CI run `31740101261` result was `SUCCESS`
- the service and runtime identity are present in the expected target
  project/region
- public access is absent
- min/max scale matches the approved target
- the existing Artifact Registry repository is already in place
- custom OAuth CLI brand listing is not available via the deprecated IAP OAuth
  Admin API; B2 verified baseline remains
  `CONFIGURED_AND_AUTHENTICATED_JUDGE_ACCESS_PASS`
- no OAuth/IAP/IAM reconfiguration is required or authorized by empty brand query

Human R2 execution approval has been signed; execution remains blocked until
the signed approval is merged. No cloud mutation has been performed.

```text
STOP_CODE=NW007_R2_SIGNED_APPROVAL_READY_FOR_FINAL_REVIEW
CURRENT_DECISION=APPROVED
HUMAN_SIGNATURE=APPROVED
SIGNED_AT=2026-08-13T16:53:03-04:00
SIGNED_BY=Aaron Chandler
CLOUD_MUTATION=NONE
```
