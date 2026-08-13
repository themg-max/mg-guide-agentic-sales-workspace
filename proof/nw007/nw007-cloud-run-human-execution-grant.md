# NW-007 — Cloud Run Human Execution-Grant Artifact

ARTIFACT_ID=MG_GUIDE_NW007_CLOUD_RUN_HUMAN_EXECUTION_GRANT_V1
ARTIFACT_KIND=BOUNDED_HUMAN_EXECUTION_GRANT
OWNER_LANE=VS Code / Orchestrator authorization lane
CREATED_AT=2026-08-13

This artifact is **AUTHORIZATION ONLY**. It packages the completed read-only
execution preflight into an explicit, resource-capped human grant request for
the NW-007 Cloud Run judge-surface deployment. Nothing in this artifact enables
APIs, creates resources, changes IAM, configures IAP, builds images, deploys
services, writes secrets, or mutates Firestore/CRM.

Self-activation is **FORBIDDEN**. No effect listed below may run until
`HUMAN_SIGNATURE` is non-pending and the corresponding execution flag is flipped
by a human approver in a subsequent authorized execution lane.

---

## Durable Baseline

```
BASELINE_PR=25
BASELINE_HEAD=873ccdcfc70fc2353d5f2382e6a971245fbfd2df
BASELINE_MERGE_SHA=87e0ff6b7e9571cb9462611dd6bac12adada6ead
BASELINE_MERGED_AT=2026-08-13T16:04:38Z
PREFLIGHT_STOP_CODE=NW007_EXECUTION_PREFLIGHT_READY_FOR_HUMAN_AUTHORIZATION
```

Upstream authorization chain (planning only; not re-opened here):

- PR #24 judge-surface authorization:
  `proof/nw007/nw007-cloud-run-judge-surface-authorization.md`
- PR #25 deployment execution-authorization planning:
  `proof/nw007/nw007-cloud-run-deployment-execution-authorization.md`
- Read-only execution preflight (session packet; no cloud mutation):
  STOP_CODE=`NW007_EXECUTION_PREFLIGHT_READY_FOR_HUMAN_AUTHORIZATION`

Planning branch at grant authoring (execution on `main` not performed):

- Branch: `plan/nw007-cloud-run-judge-surface-authorization`
- HEAD: `873ccdcfc70fc2353d5f2382e6a971245fbfd2df`
- `origin/main` tip equals `BASELINE_MERGE_SHA`

---

## Authorized Target Binding (hard caps)

```
AUTHORIZED_PROJECT=mg-devpost
AUTHORIZED_PROJECT_NUMBER=985566250549
AUTHORIZED_PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
AUTHORIZED_REGION=us-east4
AUTHORIZED_SERVICE=mg-guide-agentic-sales-workspace-judge
AUTHORIZED_SERVICE_CLASS=JUDGE_SAFE_SYNTHETIC_NON_PRODUCTION
AUTHORIZED_AR_REPOSITORY=mg-guide-judge
AUTHORIZED_AR_LOCATION=us-east4
AUTHORIZED_AR_FORMAT=docker
JUDGE_AI_MODE=STUB
BUILD_STRATEGY=CLOUD_BUILD_DOCKERFILE_TO_ARTIFACT_REGISTRY_THEN_RUN_DEPLOY
```

Resource caps (authorization ceiling — not a blank IAM/mutation permit):

```
MAX_AR_REPOSITORIES_CREATED=1
MAX_BUILD_SERVICE_ACCOUNTS_CREATED=1
MAX_RUNTIME_SERVICE_ACCOUNTS_CREATED=1
MAX_CLOUD_RUN_SERVICES_CREATED=1
MAX_CLOUD_RUN_INSTANCES=1
MIN_CLOUD_RUN_INSTANCES=0
CPU_ALLOCATION=REQUEST_TIME_ONLY
PUBLIC_UNAUTHENTICATED_ACCESS=NO
```

Any create/bind/deploy action outside these names, region, project, or counts is
**out of grant** and remains unauthorized.

---

## Corrected Judge Access Principal

```
JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL_CLASS=GOOGLE_GROUP
JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED
```

### Principal correction (mandatory)

| Address | Cloud Identity class | Role in this grant |
| --- | --- | --- |
| `mg-mcp-developer-mg@themiliare-group.com` | GOOGLE_GROUP (verified) | **JUDGE_ACCESS_PRINCIPAL** — the only approved evaluator access group |
| `buildweek-evaluator@themiliare-group.com` | USER (verified) | Member of the group above; **not** a Google Group; **must not** be labeled `JUDGE_GOOGLE_GROUP` |

Do **not** record `buildweek-evaluator@themiliare-group.com` as
`JUDGE_GOOGLE_GROUP`. Preflight evidence:

- `gcloud identity groups describe buildweek-evaluator@themiliare-group.com`
  → no such group
- Membership list of `mg-mcp-developer-mg@themiliare-group.com` shows
  `buildweek-evaluator@themiliare-group.com` with `type=USER`
- Same group contains external members
  `build-week-event@openai.com` (GROUP) and `testing@devpost.com` (GROUP),
  establishing `JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED`

Judge binding target for IAP (or Invoker fallback): **only**
`group:mg-mcp-developer-mg@themiliare-group.com`.
Never `allUsers` / `allAuthenticatedUsers`.

---

## IAP / OAuth Mode (requested, not configured)

```
IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
IAP_OAUTH_MODE=CUSTOM
CUSTOM_OAUTH_CLIENT_REQUIRED=YES
CUSTOM_OAUTH_CREATION_PATH=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO
```

Rationale:

- Scope is `EXTERNAL_OR_MIXED` → custom OAuth client required under the PR #25
  decision tree.
- Direct Cloud Run IAP remains the preferred path; no HTTPS load balancer is
  required for this grant.
- Legacy `gcloud iap oauth-brands` / IAP OAuth Admin API path is **not**
  authorized (`LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO`). Preflight observed
  deprecation/shutdown messaging for those APIs; execution must use the
  **current** Google Auth Platform or IAP console flow only.
- Fallback under the **same** human signature (not self-selectable): Cloud Run
  Invoker IAM on `JUDGE_ACCESS_PRINCIPAL` only, still
  `PUBLIC_UNAUTHENTICATED_ACCESS=NO`.

---

## Separated Authority Model

Bootstrap authority and ongoing deployment authority are **logically separated**
even when the same human principal performs both. Broad bootstrap admin roles
are **not** permanent deployer roles.

```
BOOTSTRAP_OPERATOR=user:themg@themiliare-group.com
DEPLOYMENT_PRINCIPAL=user:themg@themiliare-group.com
```

Same human is acceptable. Permissions and effects remain separated as below.

### A) Bootstrap operator — one-time setup effects only

```
BOOTSTRAP_EFFECTS_REQUESTED=
enable_enumerated_apis;
inspect_and_create_one_ar_repo_if_absent;
create_build_sa;
create_runtime_sa;
bind_only_enumerated_roles;
configure_direct_cloud_run_iap;
configure_custom_oauth;
bind_judge_access
```

Enumerated APIs (bootstrap enablement only; nothing else):

```
APIS_REQUIRED=
run.googleapis.com;
cloudbuild.googleapis.com;
artifactregistry.googleapis.com;
iap.googleapis.com;
iam.googleapis.com
```

Bootstrap-only role **capabilities** (temporary setup authority — not the
steady-state deployer profile). These may be exercised solely to complete
`BOOTSTRAP_EFFECTS_REQUESTED` within resource caps, then should be dropped or
left unused for routine deploys:

| Bootstrap capability (temporary) | Purpose (bounded) |
| --- | --- |
| Service Usage admin on project | Enable only `APIS_REQUIRED` |
| Artifact Registry repo create on `us-east4` | Create at most one docker repo named `mg-guide-judge` **if** none approved already exists after API enablement + inspect |
| Service Account Admin | Create **exactly two** user-managed SAs named below (no keys) |
| Project IAM bind (narrow, enumerated members/roles only) | Bind only roles listed in this grant |
| IAP admin / settings admin | Direct Cloud Run IAP on `AUTHORIZED_SERVICE` only |
| OAuth config editor (current console/platform flow) | Custom OAuth client via `CUSTOM_OAUTH_CREATION_PATH` only |

IAP bootstrap roles, if needed during bootstrap only:

```
BOOTSTRAP_IAP_ROLES_IF_NEEDED=
roles/iap.admin;
roles/iap.settingsAdmin;
roles/oauthconfig.editor
```

**Explicit non-permanent statement:**

- Do **not** describe `roles/resourcemanager.projectIamAdmin`,
  `roles/iam.serviceAccountAdmin`, or `roles/artifactregistry.admin` as
  permanent deployer roles.
- Those capabilities exist only inside the bootstrap envelope to create the
  capped resources and enumerated bindings once.
- Steady-state deploys use `DEPLOYMENT_EFFECTS_REQUESTED` and
  `DEPLOYMENT_ROLE_TARGET` below.

### B) Deployment principal — post-bootstrap steady-state

```
DEPLOYMENT_EFFECTS_REQUESTED=
submit_one_dockerfile_cloud_build_via_build_sa;
push_image_to_authorized_ar_repository_only;
deploy_or_update_authorized_cloud_run_service_only;
run_bounded_smoke_checks
```

Deployment role target after bootstrap (logical least privilege for
`DEPLOYMENT_PRINCIPAL`):

| Target permission | Scope |
| --- | --- |
| Cloud Run Developer (or equivalent service-scoped deploy authority) | `AUTHORIZED_SERVICE` in `AUTHORIZED_REGION` only |
| Artifact Registry Reader | approved repository `mg-guide-judge` only |
| Service Account User | runtime SA only (for `gcloud run deploy --service-account=...`) |
| Cloud Build submission authority | project build submit for the frozen Dockerfile path only |
| Service Account User | build SA only (for Cloud Build `actAs`) |

Smoke checks authorized after deploy (synthetic only):

- `GET /healthz`
- SUCCESS scenario
- STAGE_CHANGE_DENIED scenario

No other scenarios, arbitrary transcripts, CRM actions, or persistence checks.

---

## Build Identity (proposed; not created)

```
BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
MAX_BUILD_SERVICE_ACCOUNTS_CREATED=1
SERVICE_ACCOUNT_KEYS=FORBIDDEN
```

Core build permissions (bind only these; prefer resource-scoped where possible):

| Permission | Scope |
| --- | --- |
| `roles/artifactregistry.writer` | repository `mg-guide-judge` (`us-east4`) only |
| `roles/logging.logWriter` | project (build logs) |

```
STORAGE_OBJECT_VIEWER=CONDITIONAL_BUCKET_SCOPED_ONLY_IF_BUILD_SOURCE_REQUIRES
```

- `roles/storage.objectViewer` is **not** a default standing grant.
- Authorize it only if the chosen Cloud Build source path requires GCS object
  read, and only on the specific source bucket/prefix — never project-wide
  storage admin.

Build path (frozen for this grant; not executed here):

```
BUILD_STRATEGY=CLOUD_BUILD_DOCKERFILE_TO_ARTIFACT_REGISTRY_THEN_RUN_DEPLOY
```

1. Implementation work (separate code PR) supplies one Dockerfile and minimal
   HTTP adapter (`CONTAINERFILE_PRESENT=NO` / `HTTP_SERVER_PRESENT=NO` at
   baseline HEAD).
2. Cloud Build runs as `BUILD_SERVICE_ACCOUNT` and pushes:
   `us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge:<git-sha>`
3. Deploy uses that image only — no buildpacks, no `--source` ambiguity, no
   multi-image matrix.

Preflight existence: build SA **does not exist** today (project user-managed SA
list empty; describe → NOT_FOUND). Creation requires human signature +
`SERVICE_ACCOUNT_CREATION_AUTHORIZED=YES`.

---

## Runtime Identity (proposed; not created)

```
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MAX_RUNTIME_SERVICE_ACCOUNTS_CREATED=1
RUNTIME_REQUIRED_ROLES=NONE
RUNTIME_CREDENTIAL_SOURCE=CLOUD_RUN_SERVICE_IDENTITY_METADATA
SERVICE_ACCOUNT_KEYS=FORBIDDEN
```

- Judge default `JUDGE_AI_MODE=STUB` / fixture replay requires **no** GCP API
  roles on the runtime SA.
- Do not grant Secret Manager, Vertex AI, Firestore, or CRM roles under this
  grant.
- Preflight existence: runtime SA **does not exist** (describe → NOT_FOUND).

---

## Artifact Registry (inspect-then-conditional-create)

```
ARTIFACT_REGISTRY_REPOSITORY=mg-guide-judge
ARTIFACT_REGISTRY_LOCATION=us-east4
ARTIFACT_REGISTRY_FORMAT=docker
ARTIFACT_REGISTRY_REPOSITORY_EXISTS=UNKNOWN
ARTIFACT_REGISTRY_API_STATUS=DISABLED_AT_PREFLIGHT
ARTIFACT_REGISTRY_CREATION_REQUIRED=CONDITIONAL_IF_NO_EXISTING_APPROVED_REPOSITORY
MAX_AR_REPOSITORIES_CREATED=1
```

Bootstrap sequence after API enablement:

1. List repositories in `us-east4`.
2. If an approved docker repository already exists for this grant, reuse it and
   set creation count used = 0.
3. If none exists, create **at most one** repository named `mg-guide-judge`.
4. UNKNOWN must not be treated as absence before the API is enabled and list
   succeeds.

---

## Cloud Run Service Caps

```
AUTHORIZED_SERVICE=mg-guide-agentic-sales-workspace-judge
MAX_CLOUD_RUN_SERVICES_CREATED=1
MIN_CLOUD_RUN_INSTANCES=0
MAX_CLOUD_RUN_INSTANCES=1
CPU_ALLOCATION=REQUEST_TIME_ONLY
INGRESS=compatible with direct Cloud Run IAP (final value recorded at execution)
INVOCATION=authenticated only
PUBLIC_UNAUTHENTICATED_ACCESS=NO
```

---

## Compact Requested-Effects Packet

```
BASELINE_PR=25
BASELINE_MERGE_SHA=87e0ff6b7e9571cb9462611dd6bac12adada6ead
PREFLIGHT_STOP_CODE=NW007_EXECUTION_PREFLIGHT_READY_FOR_HUMAN_AUTHORIZATION

JUDGE_ACCESS_PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
JUDGE_ACCESS_PRINCIPAL_CLASS=GOOGLE_GROUP
JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED

IAP_MODE=DIRECT_CLOUD_RUN
LOAD_BALANCER_REQUIRED=NO
IAP_OAUTH_MODE=CUSTOM
CUSTOM_OAUTH_CLIENT_REQUIRED=YES
CUSTOM_OAUTH_CREATION_PATH=GOOGLE_AUTH_PLATFORM_OR_IAP_CONSOLE_CURRENT_FLOW
LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO

BOOTSTRAP_OPERATOR=user:themg@themiliare-group.com
BOOTSTRAP_EFFECTS_REQUESTED=
enable_enumerated_apis;
inspect_and_create_one_ar_repo_if_absent;
create_build_sa;
create_runtime_sa;
bind_only_enumerated_roles;
configure_direct_cloud_run_iap;
configure_custom_oauth;
bind_judge_access

DEPLOYMENT_PRINCIPAL=user:themg@themiliare-group.com
DEPLOYMENT_EFFECTS_REQUESTED=
submit_one_dockerfile_cloud_build_via_build_sa;
push_image_to_authorized_ar_repository_only;
deploy_or_update_authorized_cloud_run_service_only;
run_bounded_smoke_checks

BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
BUILD_CORE_ROLES=roles/artifactregistry.writer@repo:mg-guide-judge;roles/logging.logWriter
STORAGE_OBJECT_VIEWER=CONDITIONAL_BUCKET_SCOPED_ONLY_IF_BUILD_SOURCE_REQUIRES

RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
RUNTIME_REQUIRED_ROLES=NONE

AUTHORIZED_PROJECT=mg-devpost
AUTHORIZED_REGION=us-east4
AUTHORIZED_SERVICE=mg-guide-agentic-sales-workspace-judge
AUTHORIZED_AR_REPOSITORY=mg-guide-judge
MAX_AR_REPOSITORIES_CREATED=1
MAX_BUILD_SERVICE_ACCOUNTS_CREATED=1
MAX_RUNTIME_SERVICE_ACCOUNTS_CREATED=1
MAX_CLOUD_RUN_SERVICES_CREATED=1
MAX_CLOUD_RUN_INSTANCES=1
```

---

## Exact IAM Binding Manifest (permissible bindings only)

Every IAM binding authorized under this grant must match a row below. Bindings
not listed are **out of grant**. This is not blanket project IAM authority and
is not standing Owner/Admin expansion.

Legend for `LIFETIME`:

- `STANDING_WHILE_GRANT_ACTIVE` — may remain for the competition-bounded grant
  lifetime; still subject to cleanup/closeout.
- `TEMPORARY_BOOTSTRAP_ONLY` — setup only; not a permanent deployer role;
  `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES`.
- `CONDITIONAL` — only if a stated prerequisite is true; otherwise do not bind.

| ID | PRINCIPAL | ROLE_OR_CAPABILITY | RESOURCE_SCOPE | PURPOSE | LIFETIME |
| --- | --- | --- | --- | --- | --- |
| B1 | `serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com` | `roles/artifactregistry.writer` | Artifact Registry repository `mg-guide-judge` in `us-east4` only (`AUTHORIZED_AR_REPOSITORY`) | Push the single judge-surface image produced by the frozen Dockerfile Cloud Build path | `STANDING_WHILE_GRANT_ACTIVE` |
| B2 | `serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com` | `roles/logging.logWriter` | Project `mg-devpost` (Cloud Build / SA log writes) | Emit build logs for the authorized build path | `STANDING_WHILE_GRANT_ACTIVE` |
| B3 | `serviceAccount:mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com` | `roles/storage.objectViewer` | **Conditional:** one specific Cloud Build source bucket/prefix only, if and only if the chosen source path requires GCS object read | Read build source objects when required | `CONDITIONAL` — `STORAGE_OBJECT_VIEWER=CONDITIONAL_BUCKET_SCOPED_ONLY_IF_BUILD_SOURCE_REQUIRES`; do not bind project-wide storage roles |
| D1 | `user:themg@themiliare-group.com` (`DEPLOYMENT_PRINCIPAL`) | `roles/iam.serviceAccountUser` | Service account `mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com` only | `actAs` the build SA when submitting the authorized Cloud Build | `STANDING_WHILE_GRANT_ACTIVE` |
| D2 | `user:themg@themiliare-group.com` (`DEPLOYMENT_PRINCIPAL`) | `roles/iam.serviceAccountUser` | Service account `mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com` only | `actAs` the runtime SA when deploying/updating the authorized Cloud Run service | `STANDING_WHILE_GRANT_ACTIVE` |
| D3 | `user:themg@themiliare-group.com` (`DEPLOYMENT_PRINCIPAL`) | Cloud Build submission authority (e.g. `roles/cloudbuild.builds.editor` or narrower equivalent sufficient to submit the frozen path) | Project `mg-devpost`, frozen Dockerfile → `mg-guide-judge` image path only | Submit the one authorized container build | `STANDING_WHILE_GRANT_ACTIVE` |
| D4 | `user:themg@themiliare-group.com` (`DEPLOYMENT_PRINCIPAL`) | Cloud Run deploy authority (e.g. `roles/run.developer` or service-scoped equivalent) | Cloud Run service `mg-guide-agentic-sales-workspace-judge` in `us-east4` only (`AUTHORIZED_SERVICE`) | Deploy/update the single authorized judge service (min 0 / max 1, request-time CPU, authenticated only) | `STANDING_WHILE_GRANT_ACTIVE` |
| D5 | `user:themg@themiliare-group.com` (`DEPLOYMENT_PRINCIPAL`) | Artifact Registry Reader (e.g. `roles/artifactregistry.reader`) | Repository `mg-guide-judge` in `us-east4` only | Read/pull the authorized image for deploy | `STANDING_WHILE_GRANT_ACTIVE` |
| J1 | `group:mg-mcp-developer-mg@themiliare-group.com` (`JUDGE_ACCESS_PRINCIPAL`) | `roles/iap.httpsResourceAccessor` | IAP policy for Cloud Run service `mg-guide-agentic-sales-workspace-judge` / `us-east4` only | Authenticated evaluator access via IAP; never `allUsers` / `allAuthenticatedUsers` | `STANDING_WHILE_GRANT_ACTIVE` |
| J1-FALLBACK | `group:mg-mcp-developer-mg@themiliare-group.com` | `roles/run.invoker` | Same authorized Cloud Run service only | **Fallback only** under the same human signature if IAP path is abandoned; still `PUBLIC_UNAUTHENTICATED_ACCESS=NO`; not self-selectable alongside open public access | `STANDING_WHILE_GRANT_ACTIVE` (only if fallback path chosen) |
| IAP1 | `serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com` | `roles/run.invoker` | Cloud Run service `mg-guide-agentic-sales-workspace-judge` / `us-east4` only | Allow the direct IAP service agent to invoke the protected judge service | `STANDING_WHILE_GRANT_ACTIVE` |
| R1 | `serviceAccount:mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com` | *(none — `RUNTIME_REQUIRED_ROLES=NONE`)* | N/A for STUB judge mode | Runtime identity attachment only; no GCP API roles for fixture/stub path | `STANDING_WHILE_GRANT_ACTIVE` (SA may exist; **zero** project API role bindings required) |

J1 exact contract (expanded):

```
ID=J1
PRINCIPAL=group:mg-mcp-developer-mg@themiliare-group.com
ROLE_OR_CAPABILITY=roles/iap.httpsResourceAccessor
RESOURCE_SCOPE=IAP policy for Cloud Run service mg-guide-agentic-sales-workspace-judge / us-east4
PURPOSE=authenticated evaluator access via IAP
LIFETIME=STANDING_WHILE_GRANT_ACTIVE
```

IAP1 (Google-managed IAP service agent):

```
ID=IAP1
PRINCIPAL=serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com
ROLE_OR_CAPABILITY=roles/run.invoker
RESOURCE_SCOPE=Cloud Run service mg-guide-agentic-sales-workspace-judge / us-east4 only
PURPOSE=allow direct IAP service agent to invoke the protected judge service
LIFETIME=STANDING_WHILE_GRANT_ACTIVE

IAP_SERVICE_AGENT_IS_GOOGLE_MANAGED=YES
IAP_SERVICE_AGENT_COUNTS_TOWARD_USER_MANAGED_SA_CAP=NO
```

The IAP service agent is Google-managed. It is **not** counted against
`MAX_BUILD_SERVICE_ACCOUNTS_CREATED` or `MAX_RUNTIME_SERVICE_ACCOUNTS_CREATED`
and does not relax the two-user-managed-SA cap in this grant.

### Bootstrap-only bindings / capabilities

These rows authorize **temporary** setup authority for
`BOOTSTRAP_OPERATOR=user:themg@themiliare-group.com`. They are **not** permanent
deployer roles.

For every bootstrap row below:

```
LIFETIME=TEMPORARY_BOOTSTRAP_ONLY
PERMANENT_DEPLOYER_ROLE=NO
REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES
```

| ID | PRINCIPAL | ROLE_OR_CAPABILITY | RESOURCE_SCOPE | PURPOSE | LIFETIME |
| --- | --- | --- | --- | --- | --- |
| BS1 | `user:themg@themiliare-group.com` (`BOOTSTRAP_OPERATOR`) | Service Usage enablement authority (e.g. `roles/serviceusage.serviceUsageAdmin`) | Project `mg-devpost`; APIs limited to `APIS_REQUIRED` only | Enable enumerated NW-007 APIs | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS2 | `user:themg@themiliare-group.com` | Artifact Registry repository create authority (e.g. `roles/artifactregistry.admin` **only if** required to create the one repo) | `us-east4`; at most one docker repository named `mg-guide-judge` after inspect-if-absent | Inspect and conditionally create `AUTHORIZED_AR_REPOSITORY` | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS3 | `user:themg@themiliare-group.com` | Service Account create authority (e.g. `roles/iam.serviceAccountAdmin`) | Project `mg-devpost`; create exactly the two named SAs; **no keys** | Create build SA + runtime SA within caps | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS4 | `user:themg@themiliare-group.com` | Enumerated IAM bind authority (project IAM admin **only if** required to place rows B1–B3, D1–D5, J1 / J1-FALLBACK, and bootstrap IAP rows) | Bind **only** principals/roles/scopes listed in this manifest; no other members/roles | Place exact NW-007 bindings | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS5 | `user:themg@themiliare-group.com` | `roles/iap.admin` and/or `roles/iap.settingsAdmin` | `IAM_GRANT_SCOPE=project:mg-devpost`; `AUTHORIZED_USE_SCOPE=NW-007 judge service / IAP settings for that service only` | Configure direct Cloud Run IAP for NW-007 | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS6 | `user:themg@themiliare-group.com` | `roles/oauthconfig.editor` (or current Google Auth Platform / IAP console equivalent) | `IAM_GRANT_SCOPE=project:mg-devpost`; `AUTHORIZED_USE_SCOPE=NW-007 custom OAuth setup only` via `CUSTOM_OAUTH_CREATION_PATH`; `LEGACY_IAP_OAUTH_ADMIN_API_ALLOWED=NO` | Configure current-flow custom OAuth for external/mixed judge identities | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |
| BS7 | `user:themg@themiliare-group.com` | `roles/run.admin` | `IAM_GRANT_SCOPE=project:mg-devpost`; `AUTHORIZED_USE_SCOPE=create/configure only mg-guide-agentic-sales-workspace-judge / us-east4` | Initial Cloud Run service creation and direct IAP configuration | `TEMPORARY_BOOTSTRAP_ONLY` — `PERMANENT_DEPLOYER_ROLE=NO`; `REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES` |

Grant-scope vs use-scope distinction (binding contract):

```
BS5_IAM_GRANT_SCOPE=project:mg-devpost
BS5_AUTHORIZED_USE_SCOPE=NW-007 judge service / IAP settings only

BS6_IAM_GRANT_SCOPE=project:mg-devpost
BS6_AUTHORIZED_USE_SCOPE=NW-007 custom OAuth setup only

BS7_ID=BS7
BS7_PRINCIPAL=user:themg@themiliare-group.com
BS7_ROLE_OR_CAPABILITY=roles/run.admin
BS7_IAM_GRANT_SCOPE=project:mg-devpost
BS7_AUTHORIZED_USE_SCOPE=create/configure only mg-guide-agentic-sales-workspace-judge / us-east4
BS7_PURPOSE=initial Cloud Run service creation and direct IAP configuration
BS7_LIFETIME=TEMPORARY_BOOTSTRAP_ONLY
BS7_PERMANENT_DEPLOYER_ROLE=NO
BS7_REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES
```

Project-scoped `IAM_GRANT_SCOPE` on BS5–BS7 does **not** authorize use on any
other Cloud Run service, IAP setting, OAuth client, or resource. Only the
`AUTHORIZED_USE_SCOPE` named per row is in-grant.

**Hard exclusions for this manifest:**

- No additional Owner bindings.
- No standing project-wide `roles/owner`, `roles/editor`, or unbounded Admin
  expansion as “deployer.”
- No treatment of BS1–BS7 as `DEPLOYMENT_ROLE_TARGET`.
- No runtime SA API roles under STUB mode.
- No Firestore, Secret Manager, Vertex AI, or CRM role bindings.
- No expansion of resource caps (see caps above — unchanged).

---

## Prohibited Effects (hard NO)

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

Additional permanent exclusions:

- No service-account JSON keys under any circumstance.
- No project-wide standing Storage Admin / broad Owner expansion as “deployer”.
- No treatment of bootstrap admin capabilities as permanent deployer roles.
- No second Cloud Run service, second AR repo, or extra user-managed SAs beyond caps.
- No load balancer requirement for the preferred IAP path.
- No legacy IAP OAuth Admin API brand/client automation.
- No execution work on `main` without an explicit human grant activation lane.
- No self-activation by an agent when flags remain `NO` / `PENDING`.

---

## Lifecycle / Cleanup Obligations

```
GRANT_LIFETIME=DEVPOST_COMPETITION_ONLY
CLEANUP_REQUIRED=YES
POST_HACKATHON_REVIEW_REQUIRED=YES
RETENTION_REQUIRES_EXPLICIT_CLOSEOUT_DECISION=YES
```

This grant is competition-bounded. It does not authorize indefinite retention of
judge-facing exposure, competition-only access paths, or competition-only IAM
without an explicit closeout decision after the DevPost / hackathon window.

### Required cleanup coverage

Cleanup **must** cover at least:

| Asset class | Cleanup obligation |
| --- | --- |
| Cloud Run judge service | Delete (or fully disable and remove public/judge exposure from) `mg-guide-agentic-sales-workspace-judge` in `us-east4` |
| Competition-only image revisions/images | Delete or otherwise retire judge-surface images/tags/revisions in `mg-guide-judge` that exist solely for this competition deploy, where appropriate |
| Competition-only IAP / OAuth configuration | Remove direct Cloud Run IAP enablement/settings and competition-only custom OAuth client/brand configuration created for this grant path |
| Competition-only IAM bindings | Remove standing-while-grant and fallback bindings from the Exact IAM Binding Manifest (B\*, D\*, J\*, and any remaining bootstrap binds) that are not explicitly retained at closeout |

### Explicit closeout decision required (not automatic delete)

Do **not** automatically require deletion of potentially reusable platform
assets. At post-hackathon review, a human must record an explicit
`RETAIN` or `DELETE` decision for each of:

| Asset | Closeout decision required |
| --- | --- |
| Artifact Registry repository `mg-guide-judge` | `RETAIN` / `DELETE` |
| Build SA `mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com` | `RETAIN` / `DELETE` |
| Runtime SA `mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com` | `RETAIN` / `DELETE` |

```
CLOSEOUT_AR_REPOSITORY_DECISION=PENDING
CLOSEOUT_BUILD_SA_DECISION=PENDING
CLOSEOUT_RUNTIME_SA_DECISION=PENDING
```

Until those decisions are recorded, `RETENTION_REQUIRES_EXPLICIT_CLOSEOUT_DECISION=YES`
remains in force: silence is not retention authority for judge access paths,
and silence is not automatic deletion authority for the reusable AR/SA assets.

### Post-hackathon review checklist (authorization obligation)

1. Confirm judge service removed or non-invocable by the evaluator group.
2. Confirm competition-only IAP/OAuth configuration removed.
3. Confirm competition-only IAM bindings removed or explicitly re-authorized
   under a new grant.
4. Record `RETAIN`/`DELETE` for AR repository and both SAs.
5. Confirm prohibited effects remain `NO` (no Firestore/CRM/customer-data
   residue from this grant path).

---

## Execution Flags (remain NO)

```
DEPLOYMENT_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_CREATION_AUTHORIZED=NO
ARTIFACT_REGISTRY_CREATION_AUTHORIZED=NO
IAP_CONFIGURATION_AUTHORIZED=NO
API_ENABLEMENT_AUTHORIZED=NO
IMAGE_BUILD_AUTHORIZED=NO
SELF_ACTIVATION=FORBIDDEN
```

Authorization model note: this grant does **not** issue a blanket
“IAM mutation authorized.” When a human later activates execution, activation
must reference **resource caps + enumerated bootstrap/deployment effects** in
this artifact — not open-ended project IAM authority.

---

## Human Decision Block

```
REQUESTED_DECISION=AUTHORIZE_BOUNDED_NW007_EXECUTION_UNDER_THIS_GRANT
CURRENT_DECISION=APPROVED
HUMAN_SIGNATURE=APPROVED
SIGNED_AT=2026-08-13T12:47:00-04:00
SIGNED_BY=AARON PRESTON CHANDLER
```

What human signature would unblock (still not executed by this artifact):

1. Flip the execution flags required for the chosen lane (bootstrap and/or
   deploy) while leaving prohibited effects `NO`.
2. Bootstrap operator performs only `BOOTSTRAP_EFFECTS_REQUESTED` inside caps.
3. Deployment principal performs only `DEPLOYMENT_EFFECTS_REQUESTED` with
   post-bootstrap deployment role targets.
4. Bind judge access exclusively to
   `group:mg-mcp-developer-mg@themiliare-group.com`.
5. Run bounded synthetic smoke checks only.

---

## Verification (authorization-lane authoring)

| Check | Result |
| --- | --- |
| Artifact path | `proof/nw007/nw007-cloud-run-human-execution-grant.md` (update) |
| Cloud mutation in this lane | NONE intended; none authorized |
| Corrected judge principal explicit | YES — `group:mg-mcp-developer-mg@themiliare-group.com` |
| `buildweek-evaluator@...` not labeled JUDGE_GOOGLE_GROUP | YES — recorded as USER only |
| Bootstrap vs deployment separated | YES |
| Exact IAM binding manifest | YES — principal + role/capability + resource scope + purpose + lifetime |
| Bootstrap admin lifetime | TEMPORARY_BOOTSTRAP_ONLY; PERMANENT_DEPLOYER_ROLE=NO; REVOKE_OR_CEASE_USE_AFTER_BOOTSTRAP=YES |
| Broad admin roles not permanent deployer roles | YES |
| J1 exact (`roles/iap.httpsResourceAccessor` on judge-service IAP policy) | YES |
| IAP1 present (Google-managed IAP service agent `run.invoker` on judge service) | YES |
| BS7 present and temporary (`roles/run.admin`, project grant scope, judge-service use scope only) | YES |
| BS5/BS6 grant-scope vs use-scope distinction | YES |
| Lifecycle / cleanup obligations | YES — competition-only; cleanup required; AR/SA RETAIN/DELETE closeout (unchanged) |
| Resource caps explicit | YES (unchanged) |
| Scope expansion vs prior grant revision | NO |
| All execution flags | NO (human approval is provenance-only; execution remains blocked) |
| Self-activation | FORBIDDEN |

---

```
STOP_CODE=NW007_SIGNED_GRANT_READY_FOR_DURABLE_PR
```
