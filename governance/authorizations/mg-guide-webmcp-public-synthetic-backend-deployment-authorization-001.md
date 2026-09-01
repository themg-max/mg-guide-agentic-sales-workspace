# MG Guide WebMCP Public Synthetic Backend Deployment Authorization 001

## 1. Authorization identity and boundary

```text
AUTHORIZATION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_AUTHORIZATION_001
ARTIFACT_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_AUTHORIZATION_001
ARTIFACT_PATH=governance/authorizations/mg-guide-webmcp-public-synthetic-backend-deployment-authorization-001.md
CLASSIFICATION=DEPLOYMENT_EXECUTION_AUTHORIZATION_DEFINITION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-09-01T19:35:00Z
BASE_MAIN_SHA=2847f5a26dbc61716736b60eedb66e399c102a33

STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW_THEN_FRESH_HUMAN_ACTIVATION
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
DO_NOT_APPLY_IN_THIS_UNIT=YES
DO_NOT_DEPLOY_IN_THIS_UNIT=YES
```

This artifact **proposes** a bounded one-shot authorization to create and deploy
a public, synthetic-only WebMCP competition backend for MG Guide. Creating,
reviewing, or merging this artifact does **not** make the authorization
effective, does **not** create a service account, and does **not** authorize or
execute any IAM, Cloud Run, Secret Manager, CRM, HighLevel, Gmail, Workspace,
Agent Runtime, or private-repository action.

```text
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
ARTIFACT_MERGE_IS_EXECUTION_AUTHORITY=NO
SELF_ACTIVATION=FORBIDDEN
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
```

## 2. Scope of authorized effects (requested, not yet granted)

Upon and only upon an explicit, fresh human activation that references this
exact artifact and its recorded source SHA, the following are requested:

```text
PROJECT=ai-rolodex-to-crm
REGION=us-east4
SERVICE=mg-guide-webmcp
SOURCE_BASE=2847f5a26dbc61716736b60eedb66e399c102a33
SOURCE_PATH=deployment/webmcp/Dockerfile
RUNTIME_IDENTITY=mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
IMAGE_REPOSITORY=us-east4-docker.pkg.dev/ai-rolodex-to-crm/cloud-run-source-deploy/mg-guide-webmcp
```

AUTHORIZED_EFFECTS_REQUESTED (each must remain true at execution time):

1. Create the dedicated service account
   `mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`
   **only if it does not already exist**.
2. Grant the runtime identity **only** the minimum execution permissions Cloud
   Run itself needs to run the container (no application-data roles).
3. Build the container image **exclusively** from the public MG Guide
   repository at `SOURCE_BASE` using `deployment/webmcp/Dockerfile`.
4. Deploy the `mg-guide-webmcp` Cloud Run service in `us-east4`.
5. Permit public synthetic ingress **if** org policy permits and the human
   activation explicitly confirms it.
6. Set exactly these environment variables and no others:
   `MEETING_CONTEXT_GEMINI_MODE=stub`, `WEBMCP_CORS_MODE=production`.

## 3. Explicitly denied

The runtime identity and the service must **not** receive, read, mount, or
inherit any of the following. Any one of these is an automatic stop.

```text
SECRET_ACCESS=DENIED
SECRET_PAYLOAD_READS=DENIED
SECRET_ENV_BINDINGS=DENIED
SECRET_VOLUME_BINDINGS=DENIED
CRM_ACCESS=DENIED
CRM_MUTATION_ACCESS=DENIED
HIGHLEVEL_ACCESS=DENIED
GMAIL_ACCESS=DENIED
WORKSPACE_ACCESS=DENIED
FIRESTORE_WRITE_ACCESS=DENIED
DATASTORE_WRITE_ACCESS=DENIED
BIGQUERY_DATA_ACCESS=DENIED
IAM_ADMIN_ACCESS=DENIED
CLOUD_RUN_ADMIN_ACCESS=DENIED
SERVICE_ACCOUNT_KEY_CREATION=DENIED
ARBITRARY_ROLE_GRANTS=DENIED
UNRELATED_CLOUD_RUN_MUTATION=DENIED
PRIVATE_REPO_BUILD_DEPENDENCY=DENIED
PRIVATE_REPO_RUNTIME_DEPENDENCY=DENIED
```

The default compute service account
`831270426395-compute@developer.gserviceaccount.com` is **explicitly denied**
as the WebMCP runtime identity because read-only inspection confirms it holds
project-level `roles/secretmanager.secretAccessor`, `roles/run.admin`,
`roles/datastore.owner`, `roles/bigquery.dataEditor`, and other broad roles.

## 4. Public ingress feasibility (read-only finding)

```text
constraints/run.allowedIngress allows: internal-and-cloud-load-balancing, internal, all
PUBLIC_INGRESS_POSSIBLE_AT_CONSTRAINT_LEVEL=YES
iam.allowedPolicyMemberDomains=C01p1cpk2 (domain-restricted)
DEFAULT_COMPUTE_SA_SAFE_FOR_PUBLIC_WEBMCP=NO
EXISTING_SAFE_RUNTIME_IDENTITY=NO (no pre-existing dedicated webmcp runtime SA)
```

If at execution time the human activation selects **private backend +
load-balancer front** over direct public Cloud Run ingress, that choice must be
recorded in the activation record; this authorization does not by itself
authorize any load-balancer, URL-map, NEG, or backend-service mutation.

## 5. Rollback

Rollback authority is limited to deleting or disabling **only** the resources
created by this exact lane:

- Cloud Run service `mg-guide-webmcp` (revisions created by this lane)
- service account `mg-guide-webmcp-runtime@...` **only if** this lane created it

No other service, identity, route, or configuration may be touched by rollback.

## 6. Acceptance required before traffic or judge use

Deployment under this authorization is not complete until the deployed service
passes the acceptance checks in `competition/webmcp/JUDGE_TESTING.md` and the
effect counters read exactly:

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
SECRET_PAYLOAD_READS=0
REAL_CUSTOMER_DATA=0
```

## 7. How to authorize

A human with execution authority must create a separate, fresh
**human-activation** artifact (or equivalent governed record) that:

1. references this artifact's `AUTHORIZATION_ID` and `BASE_MAIN_SHA` exactly;
2. restates the runtime identity, service name, region, and environment;
3. records who is consuming it and when;
4. confirms each denial in Section 3 remains true.

Only that activation record — not the merge of this proposal — makes execution
authorized.
