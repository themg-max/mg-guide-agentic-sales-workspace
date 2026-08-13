# NW-007 Stage B — B2 Cloud Deployment Proof (Execution Lane)

ARTIFACT_ID=MG_GUIDE_NW007_STAGE_B_CLOUD_DEPLOYMENT_PROOF_V1
ARTIFACT_KIND=STAGE_B_B2_DEPLOYMENT_EXECUTION_PROOF
OWNER_LANE=VS Code / Orchestrator Stage B B2 deployment lane
CREATED_AT=2026-08-13
UPDATED_AT=2026-08-13T19:30:00Z
STATUS=B2_DEPLOYMENT_CORE_COMPLETE_PRE_JUDGE_GATE_PENDING

This artifact is created before any B2 cloud mutation and is updated during
bounded execution. It records the actual post-merge B2 cloud deployment for
NW-007 under the Stage B deployment activation (PR #29) and the parent signed
grant (PR #26), bound to the exact Stage B implementation merge SHA (PR #30).

## Parent authority chain (exact)

```
SIGNED_GRANT_PR=26
SIGNED_GRANT_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
SIGNED_GRANT_PATH=proof/nw007/nw007-cloud-run-human-execution-grant.md

STAGE_B_ACTIVATION_PR=29
STAGE_B_ACTIVATION_MERGE_SHA=17d1b2798a1511e8c938c8b6a371f4b77a1737ed
STAGE_B_ACTIVATION_PATH=proof/nw007/nw007-stage-b-deployment-activation.md

STAGE_B_IMPLEMENTATION_PR=30
STAGE_B_IMPLEMENTATION_HEAD_SHA=5a09916f08350f911911cbc4d46f782ae5acc66d
STAGE_B_IMPLEMENTATION_MERGE_SHA=14b97c5517e61733783d6b14facd8d33757c897d
STAGE_B_IMPLEMENTATION_MERGED_AT=2026-08-13T18:06:57Z
STAGE_B_IMPLEMENTATION_MERGED_BY=Achandler21
STAGE_B_IMPLEMENTATION_CI_RUN=31728698726
STAGE_B_IMPLEMENTATION_CI_RESULT=SUCCESS
```

## Pre-merge verification (PR #30, recorded before merge acceptance)

```
PR30_REVIEWER_DISPOSITION=APPROVE
READY_FOR_MERGE=YES
REVIEWED_HEAD_SHA=5a09916f08350f911911cbc4d46f782ae5acc66d
PR30_HEAD_SHA_OBSERVED=5a09916f08350f911911cbc4d46f782ae5acc66d
PR30_CHANGED_FILES=8
PR30_NEW_COMMITS_AFTER_REVIEW=NO
EXACT_HEAD_CI_RUN=31728698726
EXACT_HEAD_CI_RESULT=SUCCESS
CONTAINER_BUILD=PASS
CONTAINER_SMOKE=PASS
```

Reviewer disposition on PR #30 (exact-head review by Achandler21) recorded
CONTAINER_BUILD=PASS, CONTAINER_SMOKE=PASS, EXACT_HEAD_CI=PASS,
CLOUD_MUTATION=NONE. Head SHA observed via `gh pr view 30` matched the
reviewed head exactly; file count = 8; merge performed by human merge
authority (Achandler21) at 2026-08-13T18:06:57Z, producing merge commit
14b97c5517e61733783d6b14facd8d33757c897d on `main`.

## Required preflight

Commands executed before any proof edits (branch created from synced `main`
at merge SHA 14b97c5517e61733783d6b14facd8d33757c897d):

```bash
pwd
# /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git branch --show-current
# deploy/nw007-stage-b-cloud-deployment-proof

git status --short --untracked-files=all
# (empty)
```

Preflight result: branch is not `main`; working tree clean; no unrelated
changes.

## B2 prerequisite verification (before any mutation)

```
STAGE_B_ACTIVATION_PR=29
STAGE_B_ACTIVATION_MERGE_SHA=17d1b2798a1511e8c938c8b6a371f4b77a1737ed
STAGE_B_IMPLEMENTATION_PR=30
STAGE_B_IMPLEMENTATION_MERGE_SHA=14b97c5517e61733783d6b14facd8d33757c897d
B2_EXECUTION_MUST_RECORD_AND_VERIFY_IMPLEMENTATION_PR_MERGE_SHA=YES
B2_EXECUTION_MUST_VERIFY_IMPLEMENTATION_PR_MERGE_SHA_BEFORE_CLOUD_BUILD_OR_DEPLOYMENT_MUTATION=YES
```

Verified: PR #29 merge commit on `main` is
17d1b2798a1511e8c938c8b6a371f4b77a1737ed (verified via `gh pr view 29`).
PR #30 merge commit on `main` is
14b97c5517e61733783d6b14facd8d33757c897d (verified via `gh pr view 30` and
local `git rev-parse HEAD` after `git pull --ff-only origin main`).

<!-- SECTIONS BELOW UPDATED DURING BOUNDED EXECUTION -->

## 1. Pre-mutation state capture

Captured before any B2 cloud mutation (2026-08-13, active gcloud account
`themg@themiliare-group.com`, configuration `devpost-competitions`, project
`mg-devpost`).

### Enabled APIs

```bash
gcloud services list --enabled --project=mg-devpost --format='value(config.name)'
```

Stage A APIs remain enabled; no additional APIs were enabled by this lane:

```
artifactregistry.googleapis.com
cloudbuild.googleapis.com
iam.googleapis.com
iap.googleapis.com
run.googleapis.com
```

(Other listed APIs — bigquery*, dataform, firestore, pubsub, storage, etc. —
are pre-existing project state, untouched by this lane.)

### Artifact Registry state

```bash
gcloud artifacts repositories list --project=mg-devpost --location=us-east4
```

```
REPOSITORY      FORMAT  MODE                 DESCRIPTION
mg-guide-judge  DOCKER  STANDARD_REPOSITORY  NW-007 judge surface Artifact Registry repository (us-east4)
```

Exactly one repository (`mg-guide-judge`, created in Stage A); size 0 MB (no
images pushed yet). Repository IAM (B1 writer + D5 reader, unchanged):

```yaml
bindings:
- members:
  - user:themg@themiliare-group.com
  role: roles/artifactregistry.reader
- members:
  - serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
  role: roles/artifactregistry.writer
```

### Service accounts

```bash
gcloud iam service-accounts describe mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
gcloud iam service-accounts describe mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
```

Both exist from Stage A:

```
mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com    NW-007 Cloud Build service account
mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com  NW-007 Cloud Run runtime service account
```

User-managed key inspection on both returned `Listed 0 items.`
(`SERVICE_ACCOUNT_KEYS_CREATED=0` retained).

### Relevant IAM (pre-mutation)

Project IAM (relevant bindings, B2/D3/D4 plus pre-existing owner and
Google-managed agents):

```json
{"members": ["serviceAccount:985566250549@cloudbuild.gserviceaccount.com"], "role": "roles/cloudbuild.builds.builder"}
{"members": ["user:themg@themiliare-group.com"], "role": "roles/cloudbuild.builds.editor"}
{"members": ["serviceAccount:service-985566250549@gcp-sa-cloudbuild.iam.gserviceaccount.com"], "role": "roles/cloudbuild.serviceAgent"}
{"members": ["serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com"], "role": "roles/logging.logWriter"}
{"members": ["user:themg@themiliare-group.com"], "role": "roles/owner"}
{"condition": {"description": "Restricts Cloud Run deploy authority to the authorized judge service", "expression": "resource.name == \"projects/mg-devpost/locations/us-east4/services/mg-guide-agentic-sales-workspace-judge\"", "title": "NW007 judge service only"}, "members": ["user:themg@themiliare-group.com"], "role": "roles/run.developer"}
```

Service account IAM (D1/D2, unchanged):

```yaml
# build SA
bindings:
- members: [user:themg@themiliare-group.com]
  role: roles/iam.serviceAccountUser
# runtime SA
bindings:
- members: [user:themg@themiliare-group.com]
  role: roles/iam.serviceAccountUser
```

### Cloud Run service inventory

```bash
gcloud run services list --project=mg-devpost --region=us-east4
```

```
Listed 0 items.
```

Zero Cloud Run services in `us-east4` before B2 execution.

### IAP state

```bash
gcloud iap settings get --project=mg-devpost --format=json
```

```json
{
  "name": "projects/985566250549"
}
```

Bare project-level settings only; no IAP application configured (service does
not yet exist).

```
PRE_MUTATION_STATE_CAPTURE=COMPLETE
```

## 2. B3 requirement determination

Chosen build path (frozen by signed grant):

```
BUILD_STRATEGY=CLOUD_BUILD_DOCKERFILE_TO_ARTIFACT_REGISTRY_THEN_RUN_DEPLOY
```

Cloud Build runs as `BUILD_SERVICE_ACCOUNT`
(`mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com`) against local
source staged by `gcloud builds submit`. The custom build service account
must read the staged source tarball from the Cloud Build staging bucket, so
the conditional B3 binding (`roles/storage.objectViewer`, bucket-scoped, build
SA only) IS required for this source path.

```
B3_REQUIREMENT=REQUIRED_SOURCE_BUCKET_GCS_OBJECT_READ
B3_SCOPE=BUCKET_SCOPED_ONLY_BUILD_SA_ONLY
```

The exact staging bucket is determined at submit time from gcloud output and
the binding is applied to that bucket only before/while the authorized build
reads from it.

## 3. Image build and push

Exactly one image built; pushed only to `mg-guide-judge`.

Build path execution notes:

1. First `gcloud builds submit` attempt was rejected by the API with
   `INVALID_ARGUMENT` (custom build SA requires an explicit logging option)
   **after** gcloud auto-created the staging bucket
   `gs://mg-devpost_cloudbuild` (location US) and uploaded the source tarball.
   **No build was created and no image was produced by that attempt** (request
   rejected at validation; no build ID assigned).
2. Conditional binding **B3** was then determined required and applied,
   bucket-scoped only:

   ```bash
   gcloud storage buckets add-iam-policy-binding gs://mg-devpost_cloudbuild \
     --member=serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com \
     --role=roles/storage.objectViewer --project=mg-devpost
   ```

   ```
   B3_APPLIED=YES
   B3_ROLE=roles/storage.objectViewer
   B3_SCOPE=gs://mg-devpost_cloudbuild (bucket-scoped only)
   B3_MEMBER=serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
   ```

3. The build was resubmitted with an equivalent transient config
   (`/tmp/nw007-judge-build.yaml`, not committed) identical to the frozen
   `--tag` path (docker build + push of the single image) plus
   `options.logging: CLOUD_LOGGING_ONLY` — the mandatory logging mode for a
   custom build SA, covered by standing binding B2 (`roles/logging.logWriter`).
   Build ran as `BUILD_SERVICE_ACCOUNT`.

```bash
gcloud builds submit --project=mg-devpost \
  --config=/tmp/nw007-judge-build.yaml .
```

Result:

```
BUILD_ID=53d55d97-0db1-486c-9b7b-004ea0ca6427
BUILD_STATUS=SUCCESS
BUILD_DURATION=1M36S
BUILD_SERVICE_ACCOUNT=projects/mg-devpost/serviceAccounts/mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
BUILD_LOGGING=CLOUD_LOGGING_ONLY
BUILD_SOURCE=gs://mg-devpost_cloudbuild/source/1786645088.181122-96a9ab681c8448dda9868da8aed3bb2b.tgz

IMAGE_TAG=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge:14b97c5517e61733783d6b14facd8d33757c897d
IMAGE_TAG_GIT_SHA=14b97c5517e61733783d6b14facd8d33757c897d (= STAGE_B_IMPLEMENTATION_MERGE_SHA)
IMAGE_DIGEST=sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0
IMAGE_PUSHED_TO=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge ONLY
IMAGE_BUILD_COUNT=1
```

```
IMAGE_BUILD_RESULT=SUCCESS
IMAGE_PUSH_RESULT=SUCCESS_MG_GUIDE_JUDGE_ONLY
```

## 4. Cloud Run deployment

Exactly one Cloud Run service created (`MAX_CLOUD_RUN_SERVICES_CREATED=1` not
exceeded). Deploy used the digest-pinned image only — no buildpacks, no
`--source`, no multi-image matrix.

```bash
gcloud run deploy mg-guide-agentic-sales-workspace-judge \
  --project=mg-devpost --region=us-east4 \
  --image=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge@sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0 \
  --service-account=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com \
  --no-allow-unauthenticated \
  --min-instances=0 --max-instances=1 \
  --set-env-vars=MEETING_CONTEXT_GEMINI_MODE=stub,GIT_COMMIT=14b97c5517e61733783d6b14facd8d33757c897d
```

Result:

```
SERVICE=mg-guide-agentic-sales-workspace-judge
REGION=us-east4
REVISION=mg-guide-agentic-sales-workspace-judge-00001-gjl
SERVICE_URL=https://mg-guide-agentic-sales-workspace-judge-985566250549.us-east4.run.app
IMAGE_PINNED=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge@sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
GIT_COMMIT=14b97c5517e61733783d6b14facd8d33757c897d
ALLOW_UNAUTHENTICATED=NO
TRAFFIC=100% to mg-guide-agentic-sales-workspace-judge-00001-gjl
DEPLOYED_AT=2026-08-13T18:21:06Z
DEPLOYED_BY=themg@themiliare-group.com
```

Scaling reconciliation: the new-service default left a service-level
`run.googleapis.com/maxScale: '100'` annotation alongside the revision-level
`autoscaling.knative.dev/maxScale: '1'`. To bind the grant's
`MAX_CLOUD_RUN_INSTANCES=1` at both levels, the lane applied:

```bash
gcloud run services update mg-guide-agentic-sales-workspace-judge \
  --project=mg-devpost --region=us-east4 --max=1
```

Post-update describe confirms:

```
Scaling: Auto (Min: 0, Max: 1)          # service level
  Revision mg-guide-agentic-sales-workspace-judge-00001-gjl
  Scaling:
    Max instances:   1                  # revision level
```

```
MIN_CLOUD_RUN_INSTANCES=0
MAX_CLOUD_RUN_INSTANCES=1
CLOUD_RUN_DEPLOYMENT_RESULT=SUCCESS_ONE_SERVICE_ONE_REVISION
```

## 5. Post-create IAP / J1 / OAuth configuration

### IAP1 — Google-managed IAP service agent `roles/run.invoker`

Direct IAP enablement (below) provisioned the IAP service agent and gcloud
attached the authorized binding (`Setting IAP service agent ... done`).
Verified on the service IAM policy:

```yaml
bindings:
- members:
  - serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com
  role: roles/run.invoker
```

```
IAP1_RESULT=APPLIED_RUN_INVOKER_IAP_SERVICE_AGENT_ON_AUTHORIZED_SERVICE
```

### Direct Cloud Run IAP enablement

```bash
gcloud beta run services update mg-guide-agentic-sales-workspace-judge \
  --project=mg-devpost --region=us-east4 --iap
```

Verified annotation: `run.googleapis.com/iap-enabled: 'true'`.

```
DIRECT_CLOUD_RUN_IAP=ENABLED
IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
```

### J1 — judge group `roles/iap.httpsResourceAccessor`

```bash
gcloud iap web add-iam-policy-binding --resource-type=cloud-run \
  --service=mg-guide-agentic-sales-workspace-judge --region=us-east4 \
  --project=mg-devpost \
  --member=group:mg-mcp-developer-mg@themiliare-group.com \
  --role=roles/iap.httpsResourceAccessor
```

Result: `Updated IAM policy for cloud run
[projects/985566250549/iap_web/cloud_run-us-east4/services/mg-guide-agentic-sales-workspace-judge]`.

Verified IAP policy (API-echoed member casing preserved):

```yaml
bindings:
- members:
  - group:mg-mcp-developer-MG@themiliare-group.com
  role: roles/iap.httpsResourceAccessor
```

```
J1_RESULT=APPLIED_JUDGE_GROUP_ONLY
JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL_CLASS=GOOGLE_GROUP
```

### allUsers / allAuthenticatedUsers absence verification

Service IAM policy (`gcloud run services get-iam-policy`): only
`serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com` with
`roles/run.invoker`.

IAP web policy (`gcloud iap web get-iam-policy --resource-type=cloud-run`):
only `group:mg-mcp-developer-MG@themiliare-group.com` with
`roles/iap.httpsResourceAccessor`.

```
ALLUSERS_PRESENT=NO
ALLAUTHENTICATEDUSERS_PRESENT=NO
```

### Custom OAuth configuration (current flow)

Findings:

- The legacy IAP OAuth Admin API is shut down (gcloud deprecation banner:
  new projects cannot use these APIs) and the grant independently forbids it
  (`LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO`). `gcloud iap oauth-brands list`
  returns 0 items.
- Current gcloud IAP surfaces (`gcloud [beta] iap settings`) expose no
  OAuth-client creation for the custom flow; the only authorized path is
  `GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW` — an interactive console
  action on the operator's Google account, which this lane cannot and must
  not automate (credential/console-UI boundary).
- Direct Cloud Run IAP with no OAuth client attached is **fail-closed**:
  unauthenticated `GET /healthz` returns `HTTP 404` (generic Google error
  page; service existence not leaked), and a request bearing a valid
  Google-issued ID token (runtime-SA impersonation, `aud` = service URL) also
  returns `HTTP 404`. No traffic reaches the application until the custom
  OAuth client is attached in the console.

```
CUSTOM_OAUTH_CONFIGURATION_RESULT=FAIL_CLOSED_PENDING_CONSOLE_FLOW
CUSTOM_OAUTH_CONSOLE_FLOW=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
LEGACY_IAP_OAUTH_ADMIN_API_USED=NO
IAP_FAIL_CLOSED_VERIFIED=YES
IAP_AUTHENTICATED_ACCESS_VERIFICATION=DEFERRED_REQUIRES_CUSTOM_OAUTH_CLIENT
```

This matches the activation's pre-judge gate
(`STAGE_B_PRE_JUDGE_REQUIRED=CUSTOM_OAUTH_CLIENT_CONFIGURATION;IAP_AUTHENTICATED_ACCESS_VERIFICATION`):
judge access verification happens after the human attaches the custom OAuth
client in the console.

### Custom OAuth — post-console-action update (2026-08-13T19:23-19:30Z)

The human operator completed the authorized console action (current Google
Auth Platform / IAP flow; legacy IAP OAuth Admin API not used — it is shut
down and forbidden). Observed evidence (read-only, no secrets recorded):

- Unauthenticated browser-like `GET /` now returns `HTTP 302` with
  `x-goog-iap-generated-response: true` redirecting to
  `accounts.google.com/o/oauth2/v2/auth` using the operator-configured custom
  OAuth client
  (`client_id=369001918367-t5qrahnqdaasaifvk6akpqkpjk9vli58.apps.googleusercontent.com`;
  OAuth client IDs are public identifiers, not secrets).
- Unauthenticated `GET /healthz` still returns `HTTP 404` (generic Google
  error page; no application content served). Unauthenticated access remains
  denied on every observed path (302 → login, or 404).
- Audience enforcement verified: a request bearing a valid Google-issued ID
  token for `themg@themiliare-group.com` whose audience is the gcloud CLI
  client (not the IAP client) still returns `HTTP 404` — IAP accepts only
  tokens minted for the configured custom OAuth client.
- Service IAM and IAP IAM policies are byte-identical to the B2 lane state
  (etags `BwZY8c_rkQo=` / `BwZY8dEzOSw=`): the console action changed no IAM
  bindings. No principals, roles, or scopes were loosened.
- The console OAuth client belongs to the operator-managed Auth Platform
  configuration; no OAuth client secret was requested, handled, or recorded
  by this lane.

```
CUSTOM_OAUTH_CONFIGURATION_RESULT=COMPLETED_CURRENT_GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_FLOW
CUSTOM_OAUTH_CLIENT_SECRET_RECORDED_IN_REPO=NO
CUSTOM_OAUTH_CLIENT_ID_OBSERVED=369001918367-t5qrahnqdaasaifvk6akpqkpjk9vli58.apps.googleusercontent.com
LEGACY_IAP_OAUTH_ADMIN_API_USED=NO
UNAUTHENTICATED_ACCESS_STILL_DENIED=YES
IAM_UNCHANGED_BY_CONSOLE_ACTION=YES
IAP_AUDIENCE_ENFORCEMENT_VERIFIED=YES
```

Remaining pre-judge gate item: an authenticated run of the judge smoke by an
actual confirmed member of `group:mg-mcp-developer-mg@themiliare-group.com`
requires that member's interactive browser session (IAP accepts only tokens
minted for the custom OAuth client via the interactive flow; this lane holds
no OAuth client secret and will not impersonate judge identities). The
orchestrator's integrated browser has no Google session and credential entry
is out of lane bounds. Verification steps are scripted below for the human
operator; the gate fields will be flipped to PASS with the observed evidence
once completed.

```
IAP_AUTHENTICATED_ACCESS_VERIFICATION=PENDING_HUMAN_JUDGE_BROWSER_SESSION
```

## 6. Authenticated smoke tests

### Through-IAP smoke (public URL)

Attempted against
`https://mg-guide-agentic-sales-workspace-judge-985566250549.us-east4.run.app`:

```
UNAUTHENTICATED GET /healthz => HTTP 404 (fail-closed, generic Google error page)
AUTHENTICATED GET /healthz (runtime-SA impersonation ID token, aud=service URL) => HTTP 404 (fail-closed: no OAuth client attached yet)
```

Through-IAP authenticated smoke is **blocked by design** until the custom
OAuth client is configured in the console (Section 5). No principal was added
and no policy was loosened to force a green result.

#### Post-console-action probes (2026-08-13T19:23-19:30Z)

After the operator completed the console OAuth configuration:

```
UNAUTHENTICATED GET /         => HTTP 302 -> accounts.google.com (x-goog-iap-generated-response: true; custom OAuth client flow active)
UNAUTHENTICATED GET /healthz  => HTTP 404 (denied; no application content)
WRONG-AUDIENCE ID TOKEN (user themg@, aud=gcloud CLI client) GET /healthz => HTTP 404 (IAP audience enforcement)
```

Scripted judge verification (to be run by a confirmed member of
`group:mg-mcp-developer-mg@themiliare-group.com` in their browser session; no
credentials pass through this lane):

```
1. Open https://mg-guide-agentic-sales-workspace-judge-985566250549.us-east4.run.app/healthz
   Sign in with the judge-group account => expect HTTP 200 JSON (status=ok,
   judge_mode=stub, commit=14b97c5517e61733783d6b14facd8d33757c897d).
2. POST /demo/meeting-follow-up {"scenario":"SUCCESS"}
   => expect HTTP 200, workflow_status=completed.
3. POST /demo/meeting-follow-up {"scenario":"STAGE_CHANGE_DENIED"}
   => expect HTTP 200, workflow_status=completed_with_review,
   policy_decision.stage_write=blocked.
```

```
THROUGH_IAP_JUDGE_SMOKE=AWAITING_HUMAN_JUDGE_BROWSER_SESSION
```

### Deployed-image smoke (exact digest, local container)

The exact deployed image digest was pulled from `mg-guide-judge` (as
`user:themg@themiliare-group.com`, D5 reader) and run locally with the same
environment (`MEETING_CONTEXT_GEMINI_MODE=stub`,
`GIT_COMMIT=14b97c5517e61733783d6b14facd8d33757c897d`):

```
docker run -p 18080:8080 \
  us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge@sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0
```

Results:

```
GET /healthz => HTTP 200
  status=ok service=mg-guide-agentic-sales-workspace-judge version=0.1.0
  commit=14b97c5517e61733783d6b14facd8d33757c897d judge_mode=stub
  scenario_catalog_hash=9ad5733da520547fdb20c35e357d4b05e68c6a39f2d4ddfe7910f052595b69fe
  scenario_names=[AMBIGUOUS_CONTACT, STAGE_CHANGE_DENIED, SUCCESS]

POST /demo/meeting-follow-up {"scenario":"SUCCESS"} => HTTP 200
  workflow_status=completed
  resolution={status=matched, match_basis=email, candidate_count=1, current_stage=discovery_scheduled}
  policy={note_write=allowed, stage_write=allowed, reason_codes=[]}
  external_effects=0 cloud_mutation=NONE

POST /demo/meeting-follow-up {"scenario":"STAGE_CHANGE_DENIED"} => HTTP 200
  workflow_status=completed_with_review
  resolution={status=matched, match_basis=email, candidate_count=1, current_stage=discovery_scheduled}
  policy={note_write=allowed, stage_write=blocked, reason_codes=[STAGE_TRANSITION_NOT_ALLOWED]}
  external_effects=0 cloud_mutation=NONE

POST /demo/meeting-follow-up {"scenario":"AMBIGUOUS_CONTACT"} => HTTP 200 (optional scenario)
  workflow_status=blocked
  resolution={status=ambiguous, match_basis=name, candidate_count=2, current_stage=null}
  policy={note_write=not_attempted, stage_write=not_attempted, reason_codes=[AMBIGUOUS_CONTACT]}
  external_effects=0 cloud_mutation=NONE
```

The local container was stopped and removed after the smoke run.

```
IMAGE_SMOKE_RESULT=PASS_ALL_SCENARIOS_ZERO_EXTERNAL_EFFECTS
THROUGH_IAP_SMOKE_RESULT=BLOCKED_FAIL_CLOSED_PENDING_CUSTOM_OAUTH_CLIENT
```

## 6b. Read-only configuration verification (2026-08-13T19:27Z)

Post-console-action read-only capture of the actual Cloud Run state (no
mutations; no rebuild, no redeploy — image digest and revision unchanged):

```
REVISION=mg-guide-agentic-sales-workspace-judge-00001-gjl (unchanged since deploy)
IMAGE_DIGEST=sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0 (unchanged)
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub (live Gemini NO)
GIT_COMMIT=14b97c5517e61733783d6b14facd8d33757c897d
CPU_ALLOCATION=REQUEST_BASED (run.googleapis.com/cpu-throttling unset; Cloud Run
  default = CPU allocated only during request processing; container cpu limit 1000m)
INGRESS=all (required for direct Cloud Run IAP fronting; no unauthenticated
  invoker binding exists, IAP enforces access)
MIN_INSTANCES=0 (revision minScale unset = 0; service minScale unset = 0)
MAX_INSTANCES=1 (revision autoscaling.knative.dev/maxScale=1; service
  run.googleapis.com/maxScale=1)
IAP_ENABLED=true (run.googleapis.com/iap-enabled)
SERVICE_IAM=roles/run.invoker -> serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com ONLY (etag BwZY8c_rkQo=)
IAP_IAM=roles/iap.httpsResourceAccessor -> group:mg-mcp-developer-MG@themiliare-group.com ONLY (etag BwZY8dEzOSw=)
ALLUSERS_PRESENT=NO
ALLAUTHENTICATEDUSERS_PRESENT=NO
```

## 7. Prohibited-effect verification

```
FIRESTORE_RUNTIME_WRITES=0          # stub judge mode; fixture replay only; no Firestore client used
GHL_CRM_MUTATIONS=0                 # no CRM calls; scenario packets are fixed fixtures
SECRET_MANAGER_MUTATIONS=0          # Secret Manager never touched by this lane
REAL_CUSTOMER_DATA=0
LIVE_GEMINI_MODE=NO                 # MEETING_CONTEXT_GEMINI_MODE=stub; app fails closed otherwise (503)
PUBLIC_UNAUTHENTICATED_ACCESS=NO    # unauthenticated /healthz => 404; no allUsers/allAuthenticatedUsers anywhere
PRODUCTION_PROMOTION=NO
SERVICE_ACCOUNT_KEYS_CREATED=0      # user-managed key lists re-verified empty pre-mutation; no keys created
VERTEX_AI_ROLES=NO
NEW_AR_REPOSITORIES_CREATED=0       # exactly 1 repo (mg-guide-judge) before and after
NEW_SERVICE_ACCOUNTS_CREATED=0      # exactly the 2 Stage A SAs; observed 985566250549-compute default SA
                                    # is Google-auto-provisioned (audit log: created 2026-08-13T17:19:40Z
                                    # during Stage A API enablement, empty principal), not by this lane
NEW_USER_MANAGED_SERVICE_ACCOUNTS_CREATED=0
GOOGLE_MANAGED_IAP_SERVICE_AGENT_PROVISIONED=YES  # service-985566250549@gcp-sa-iap.iam.gserviceaccount.com,
                                                  # auto-provisioned by Google when direct IAP was enabled
IAP_SERVICE_AGENT_COUNTS_TOWARD_USER_MANAGED_SA_CAP=NO

# Cloud Build staging bucket accounting (resource created during B2 build path):
CLOUD_BUILD_STAGING_BUCKET_CREATED=YES
CLOUD_BUILD_STAGING_BUCKET=gs://mg-devpost_cloudbuild
CLOUD_BUILD_STAGING_BUCKET_LOCATION=US
CLOUD_BUILD_STAGING_BUCKET_CREATION_MODE=GCLOUD_BUILDS_SUBMIT_AUTO_CREATE
CLOSEOUT_STAGING_BUCKET_DECISION=PENDING
NEW_PRINCIPALS_INTRODUCED=0         # bindings touch only grant-listed principals
CLOUD_RUN_SERVICES_IN_US_EAST4=1    # exactly the authorized service
IMAGES_BUILT=1
```

## Final proof fields

```
STAGE_B_ACTIVATION_PR=29
STAGE_B_ACTIVATION_MERGE_SHA=17d1b2798a1511e8c938c8b6a371f4b77a1737ed

STAGE_B_IMPLEMENTATION_PR=30
STAGE_B_IMPLEMENTATION_HEAD_SHA=5a09916f08350f911911cbc4d46f782ae5acc66d
STAGE_B_IMPLEMENTATION_MERGE_SHA=14b97c5517e61733783d6b14facd8d33757c897d
STAGE_B_IMPLEMENTATION_MERGED_AT=2026-08-13T18:06:57Z
STAGE_B_IMPLEMENTATION_CI_RUN=31728698726
STAGE_B_IMPLEMENTATION_CI_RESULT=SUCCESS

IMAGE_TAG=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge:14b97c5517e61733783d6b14facd8d33757c897d
IMAGE_DIGEST=sha256:0e5c67cd633006006135a2179f7c53c3e1250835956c3b793152adbf9b1583c0
CLOUD_BUILD_ID=53d55d97-0db1-486c-9b7b-004ea0ca6427
BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com

SERVICE=mg-guide-agentic-sales-workspace-judge
REGION=us-east4
SERVICE_REVISION=mg-guide-agentic-sales-workspace-judge-00001-gjl
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_CLOUD_RUN_INSTANCES=0
MAX_CLOUD_RUN_INSTANCES=1

B3_RESULT=APPLIED_BUCKET_SCOPED_gs://mg-devpost_cloudbuild_roles/storage.objectViewer_BUILD_SA_ONLY
IAP1_RESULT=APPLIED_RUN_INVOKER_IAP_SERVICE_AGENT_ON_AUTHORIZED_SERVICE
J1_RESULT=APPLIED_JUDGE_GROUP_ONLY
DIRECT_CLOUD_RUN_IAP=ENABLED
IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
CUSTOM_OAUTH_CONFIGURATION_RESULT=COMPLETED_CURRENT_GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_FLOW
CUSTOM_OAUTH_CLIENT_SECRET_RECORDED_IN_REPO=NO
LEGACY_IAP_OAUTH_ADMIN_API_USED=NO
JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
ALLUSERS_PRESENT=NO
ALLAUTHENTICATEDUSERS_PRESENT=NO

CPU_ALLOCATION=REQUEST_BASED
INGRESS=all

CLOUD_BUILD_STAGING_BUCKET_CREATED=YES
CLOUD_BUILD_STAGING_BUCKET=gs://mg-devpost_cloudbuild
CLOUD_BUILD_STAGING_BUCKET_LOCATION=US
CLOUD_BUILD_STAGING_BUCKET_CREATION_MODE=GCLOUD_BUILDS_SUBMIT_AUTO_CREATE
CLOSEOUT_STAGING_BUCKET_DECISION=PENDING

NEW_USER_MANAGED_SERVICE_ACCOUNTS_CREATED=0
GOOGLE_MANAGED_IAP_SERVICE_AGENT_PROVISIONED=YES
IAP_SERVICE_AGENT_COUNTS_TOWARD_USER_MANAGED_SA_CAP=NO

SMOKE_UNAUTHENTICATED_HEALTHZ=HTTP_404_DENIED
SMOKE_UNAUTHENTICATED_ROOT=HTTP_302_TO_CUSTOM_OAUTH_LOGIN
SMOKE_THROUGH_IAP_AUTHENTICATED=PENDING_HUMAN_JUDGE_BROWSER_SESSION
IAP_AUTHENTICATED_ACCESS_VERIFICATION=PENDING_HUMAN_JUDGE_BROWSER_SESSION
SMOKE_IMAGE_DIGEST_HEALTHZ=HTTP_200
SMOKE_IMAGE_DIGEST_SUCCESS=HTTP_200_COMPLETED
SMOKE_IMAGE_DIGEST_STAGE_CHANGE_DENIED=HTTP_200_COMPLETED_WITH_REVIEW_STAGE_BLOCKED
SMOKE_IMAGE_DIGEST_AMBIGUOUS_CONTACT=HTTP_200_BLOCKED

FIRESTORE_RUNTIME_WRITES=0
GHL_CRM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0
LIVE_GEMINI_MODE=NO
PUBLIC_UNAUTHENTICATED_ACCESS=NO

STAGE_B_B2_FINAL_DISPOSITION=DEPLOYED_OAUTH_CONFIGURED_AUTHENTICATED_JUDGE_VERIFICATION_PENDING
```

> Note for reviewer: `STAGE_B_B2_FINAL_DISPOSITION` flips to
> `DEPLOYED_AUTHENTICATED_JUDGE_ACCESS_VERIFIED`, `STATUS` flips to
> `B2_EXECUTION_COMPLETE_READY_FOR_FINAL_PROOF_REVIEW`, and
> `IAP_AUTHENTICATED_ACCESS_VERIFICATION` flips to `PASS` with observed
> evidence as soon as a confirmed judge-group member completes the scripted
> through-IAP smoke (Section 6) in their own browser session. No cloud
> mutation remains for this lane; the only outstanding item is that human
> interactive verification.

---

STOP_CODE=NW007_STAGE_B_B2_DEPLOYMENT_READY_FOR_FINAL_PROOF_REVIEW
