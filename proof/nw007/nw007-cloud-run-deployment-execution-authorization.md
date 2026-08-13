# NW-007 — Cloud Run Deployment Execution-Authorization Planning Artifact

ARTIFACT_ID=MG_GUIDE_NW007_CLOUD_RUN_DEPLOYMENT_EXECUTION_AUTHORIZATION_V1
ARTIFACT_KIND=EXECUTION_AUTHORIZATION_PLANNING
OWNER_LANE=VS Code / Orchestrator planning lane
CREATED_AT=2026-08-13

This artifact is **PLANNING ONLY**. It resolves the execution prerequisites for
the NW-007 Cloud Run judge-surface deployment described in
`proof/nw007/nw007-cloud-run-judge-surface-authorization.md` (PR #24).
Nothing in this artifact deploys, enables, creates, or mutates any cloud
resource. All inspection performed for this artifact was read-only.

---

## Durable Baseline

- PR=24
- HEAD=c3baff93dd6a2c05b547dcc0bca0b76ac041d767
- MERGE_SHA=3f47d443c41013866a6a7d75da2cc8985c17aa07
- MERGED_AT=2026-08-13T14:50:56Z
- Planning branch: `plan/nw007-cloud-run-judge-surface-authorization`
  (execution on `main` was not performed; preflight branch check passed)

Target binding (carried from PR #24 packet):

- PROJECT=mg-devpost (project number 985566250549)
- PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
- REGION=us-east4
- SERVICE_NAME=mg-guide-agentic-sales-workspace-judge
- SERVICE_CLASS=JUDGE_SAFE_SYNTHETIC_NON_PRODUCTION

---

## Resolved Prerequisites (read-only inspection only)

Repository inspection plus read-only `gcloud` queries against project
`mg-devpost` (no write/enable/create/delete commands were issued). Values that
could not be verified are recorded as UNKNOWN — never interpreted as absence.

| Key | Value | Evidence |
| --- | --- | --- |
| BUILD_STRATEGY | UNKNOWN — no build path exists yet. No `Dockerfile`, `cloudbuild.yaml`, `.dockerignore`, or Cloud Run `service.yaml` in the repository (`CONTAINERFILE_PRESENT=NO` per PR #24 Phase 1). Proposed (not authorized): Cloud Build buildpacks/Docker build to Artifact Registry, then `gcloud run deploy --image`. | Repository tree at HEAD c3baff9; PR #24 packet Phase 1. |
| ARTIFACT_REGISTRY_REPOSITORY | UNKNOWN (proposed name for human approval: `mg-guide-judge`, location `us-east4`, format `docker`). No repository is verifiable in the project. | `gcloud artifacts repositories list` blocked: API disabled. |
| ARTIFACT_REGISTRY_REPOSITORY_EXISTS | UNKNOWN — cannot be listed because the Artifact Registry API is disabled in `mg-devpost`. Recorded as UNKNOWN, not as absence. | `gcloud artifacts repositories list --project=mg-devpost --location=us-east4` → 403 "Artifact Registry API has not been used in project mg-devpost before or it is disabled." |
| ARTIFACT_REGISTRY_CREATION_REQUIRED | CONDITIONAL_IF_NO_EXISTING_APPROVED_REPOSITORY — no repository could be verified while the API is disabled. Execution preflight must list repositories after the Artifact Registry API becomes available and create one only if no approved repository already exists (under explicit authorization). | Above; no registry config anywhere in repo. |
| BUILD_SERVICE_ACCOUNT | UNKNOWN — Cloud Build is currently disabled and no authorized build identity was established by this inspection. Do not infer historical/default service-agent existence. Proposed execution design uses a dedicated least-privilege build SA (e.g. `mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com`), NOT created. | `gcloud builds list --project=mg-devpost` → PERMISSION_DENIED "Cloud Build has not been used in project 985566250549 before or it is disabled." (`cloudbuild.googleapis.com` absent from enabled-services list). |
| CLOUD_BUILD_API_STATUS | DISABLED | Same read-only `gcloud builds list` probe; `cloudbuild.googleapis.com` absent from `gcloud services list --enabled`. |
| ARTIFACT_REGISTRY_API_STATUS | DISABLED | 403 probe above; `artifactregistry.googleapis.com` absent from enabled-services list. |
| DEPLOYER_PRINCIPAL | PROPOSED: `user:themg@themiliare-group.com`. Final deployer identity must be confirmed by the human approver; this artifact does not grant or assume deployment rights. | Read-only project IAM (`gcloud projects get-iam-policy mg-devpost`) showed this identity as the visible project-level `roles/owner` binding (plus Google-managed firebaserules/firestore service agents). Inherited/effective permissions were not evaluated and no exclusivity claim is made. |
| DEPLOYER_REQUIRED_ROLES | TO_BE_MINIMIZED_DURING_EXECUTION_PREFLIGHT — no fixed project-wide role is recommended here. Current Google Cloud documentation supports narrower deployment permissions and a dedicated build service account; exact grants are to be determined and minimized at execution preflight. No roles are granted in this planning lane. | Derived from the proposed deployment shape in PR #24 Phase 2; revised per human direction to defer and minimize role selection. |
| RUNTIME_SERVICE_ACCOUNT | PROPOSED_NOT_CREATED: `mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com`. No such service account exists in the project IAM policy today. | PR #24 packet Phase 3; project IAM policy contains no user-managed service accounts. |
| RUNTIME_REQUIRED_ROLES | NONE for the judge default (`MEETING_CONTEXT_GEMINI_MODE=stub`, fixture replay, no GCP egress). `roles/secretmanager.secretAccessor` on exactly one Gemini API-key secret ONLY if live-Gemini mode is separately approved. `roles/aiplatform.user` NOT applicable (`VERTEX_AI_SUPPORTED_BY_CURRENT_RUNTIME=NO`). No Firestore roles. | PR #24 packet Phase 3; `src/agents/meeting_context/providers/gemini_adk_provider.py`. |
| JUDGE_GOOGLE_GROUP | buildweek-evaluator@themiliare-group.com (human-supplied, recorded exactly; group membership/configuration not independently verified — see reviewer note) | Human approver supplied the evaluator group address during this revision. |
| JUDGE_PRINCIPAL_CLASS | GOOGLE_GROUP — the judge Google group bound via IAP (or, as fallback, Cloud Run Invoker). Individual user principals are the fallback class, never `allUsers`/`allAuthenticatedUsers`. | PR #24 packet Phase 4. |
| JUDGE_MEMBER_IDENTITY_SCOPE | UNKNOWN — whether all evaluator-group members are in-organization (Google Workspace) identities or external/mixed is not verifiable from this planning lane. This determination drives the IAP OAuth mode decision below and must be resolved before IAP configuration. | Not verifiable via read-only inspection available here; human confirmation required at execution preflight. |
| IAP_OAUTH_CLIENT_REQUIREMENT | CONDITIONAL_ON_JUDGE_IDENTITY — under current Google Cloud IAP-for-Cloud-Run requirements, if all judge identities are in-organization, IAP can use Google-managed authentication and no custom OAuth client is required; if judge identities are external or mixed, a custom OAuth client (and OAuth consent brand) is required. `iap.googleapis.com` remains DISABLED in `mg-devpost`; any OAuth consent brand/client configuration requires explicit authorization. | Enabled-services list (read-only); current IAP program requirements for Cloud Run. |
| DIRECT_CLOUD_RUN_IAP_VIABILITY | VIABLE_WITH_PREREQUISITES — Cloud Run supports IAP directly at the service level, but only after: IAP API enablement, judge Google group binding, and resolution of the conditional OAuth mode below. LOAD_BALANCER_REQUIRED=NO — direct Cloud Run IAP does not require a load balancer. All prerequisites are currently absent/disabled, so IAP cannot be activated without the authorizations below. The fallback (Cloud Run Invoker IAM on the judge group, `PUBLIC_UNAUTHENTICATED_ACCESS=NO`) remains available under the same human signature. | PR #24 packet Phases 2 and 4; read-only API status findings above; current IAP-for-Cloud-Run documentation. |

IAP OAuth mode decision (recorded, conditional, not applied):

```
IF JUDGE_MEMBER_IDENTITY_SCOPE=IN_ORG:
  IAP_OAUTH_MODE=GOOGLE_MANAGED
  CUSTOM_OAUTH_CLIENT_REQUIRED=NO

IF JUDGE_MEMBER_IDENTITY_SCOPE=EXTERNAL_OR_MIXED:
  IAP_OAUTH_MODE=CUSTOM
  CUSTOM_OAUTH_CLIENT_REQUIRED=YES
```

JUDGE_MEMBER_IDENTITY_SCOPE is currently UNKNOWN; the human approver must
resolve it before any IAP configuration is authorized.

Additional read-only API findings (context, not requested for enablement here):
`run.googleapis.com` and `iap.googleapis.com` are also DISABLED in
`mg-devpost`; both would need enabling under the deployment authorization.

MG_MCP_RETRIEVAL_GAP_NW007=UNKNOWN — no MG MCP retrieval for NW-007 context
was available to this planning lane. This gap is recorded as UNKNOWN and is
**not** interpreted as absence of relevant organizational context; the human
reviewer should supply any MG MCP context at authorization time.

---

## Preserved Constraints (unchanged from PR #24)

- JUDGE_AI_MODE=STUB
- FIRESTORE_RUNTIME_WRITES=NO
- GHL_CRM_MUTATION=NO
- REAL_CUSTOMER_DATA=NO
- PUBLIC_UNAUTHENTICATED_ACCESS=NO

---

## Execution Flags (all NO pending explicit human authorization)

- DEPLOYMENT_AUTHORIZED=NO
- IAM_MUTATION_AUTHORIZED=NO
- SERVICE_ACCOUNT_CREATION_AUTHORIZED=NO
- ARTIFACT_REGISTRY_CREATION_AUTHORIZED=NO
- IAP_CONFIGURATION_AUTHORIZED=NO
- HUMAN_SIGNATURE=PENDING
- SELF_ACTIVATION=FORBIDDEN

---

## What Human Authorization Would Unblock (not executed here)

1. Enable `run.googleapis.com`, `cloudbuild.googleapis.com`,
   `artifactregistry.googleapis.com` (and `iap.googleapis.com` if the IAP
   path is chosen) in `mg-devpost`.
2. Create one Artifact Registry docker repository in `us-east4`.
3. Create the build and runtime service identities (no JSON keys — keys are
   FORBIDDEN per PR #24).
4. Build and push the judge-surface image; deploy one Cloud Run service
   (min 0 / max 1 instances, request-time CPU, authenticated invocation only).
5. Bind judge access: IAP + judge Google group
   (`buildweek-evaluator@themiliare-group.com`, preferred) or Cloud Run
   Invoker on the judge group (fallback) — with the OAuth mode selected per
   the resolved `JUDGE_MEMBER_IDENTITY_SCOPE`.
6. Run bounded smoke checks (`GET /healthz`, SUCCESS and
   STAGE_CHANGE_DENIED synthetic scenarios only).

NOT_REQUESTED: Firestore runtime writes, GHL/CRM mutation, production data,
broad project IAM, service-account keys, Secret Manager mutation (Gemini key
secret only under separate approval), production promotion.

---

## Reviewer Note

The supplied evaluator-group address is
`buildweek-evaluator@themiliare-group.com`. The provided screenshot displays a
different group, `mg-mcp-developer-MG@themiliare-group.com`, so screenshot
evidence does not yet verify the evaluator group's exact
membership/configuration. The evaluator group's membership and identity scope
(`JUDGE_MEMBER_IDENTITY_SCOPE`) must be confirmed by the human reviewer before
IAP configuration is authorized.

---

STOP_CODE=NW007_PR25_REVISED_READY_FOR_FINAL_REVIEW
