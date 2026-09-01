# MG Guide WebMCP Public Synthetic Backend Deployment Human Activation 001

## 1. Activation identity

```text
ACTIVATION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_HUMAN_ACTIVATION_001
CLASSIFICATION=HUMAN_EXECUTION_ACTIVATION
PR_CLASS=authorization
MODE=ONE_SHOT_EXECUTION_ACTIVATION
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-09-01T20:24:00Z
BASE_MAIN_SHA=a42972652a837897004eb1648c550ab4abb96203

SOURCE_AUTHORIZATION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_AUTHORIZATION_001
SOURCE_AUTHORIZATION_MERGE_SHA=a42972652a837897004eb1648c550ab4abb96203
WEBMCP_DEPLOY_SOURCE_SHA=2847f5a26dbc61716736b60eedb66e399c102a33
WEBMCP_DEPLOY_SOURCE_PATH=deployment/webmcp/Dockerfile

HUMAN_GOVERNANCE_GRANT_RECEIVED=YES
GRANT_SOURCE=CURRENT_HUMAN_REQUEST
HUMAN_ACTIVATION_INTENT=GRANTED
EXECUTION_CONSUMER=VS Code / MG Orchestrator
ACTIVATION_RECORDED_AT_UTC=2026-09-01T20:24:00Z
ACTIVATION_EFFECTIVE_AFTER_DURABLE_RECORD_MERGE=YES
EXECUTION_AUTHORIZED_AFTER_ACTIVATION_MERGE=YES
NO_ADDITIONAL_HUMAN_CONFIRMATION_REQUIRED_FOR_BACKEND_LANE=YES

SELF_ACTIVATION=NO
ONE_SHOT=YES
REUSE_ALLOWED=NO
AUTHORITY_CONSUMED=NO
```

This durable record preserves the current human governance grant. The
orchestrator is recording and consuming a human-supplied grant, not
self-activating. This activation is effective only after its exact record is
merged and does not authorize any action outside the bounded backend lane.

## 2. Frozen execution target

```text
PROJECT=ai-rolodex-to-crm
REGION=us-east4
SERVICE=mg-guide-webmcp
RUNTIME_IDENTITY=mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
INGRESS_MODE=DIRECT_PUBLIC_CLOUD_RUN_PENDING_BINDING_PROOF

MAX_SERVICE_ACCOUNT_CREATES=1
MAX_CLOUD_RUN_SERVICES_CREATED=1
MAX_APPLICATION_ENV_VARS=2
MAX_SECRET_BINDINGS=0
MAX_SECRET_READS=0
MAX_CRM_CALLS=0
MAX_HIGHLEVEL_CALLS=0
MAX_EMAIL_SENDS=0
MAX_LOAD_BALANCER_MUTATIONS=0
MAX_URL_MAP_MUTATIONS=0
MAX_NEG_MUTATIONS=0
MAX_ORG_POLICY_MUTATIONS=0
```

Only the following application environment variables are allowed:

```text
MEETING_CONTEXT_GEMINI_MODE=stub
WEBMCP_CORS_MODE=production
```

The exact permitted service-account creation is:

```text
mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

It may be created only if absent, without a service-account key and without
any project-level application or data role. Required post-create state:

```text
RUNTIME_PROJECT_ROLE_COUNT=0
```

The exact permitted Cloud Run service creation is:

```text
mg-guide-webmcp
```

## 3. Preserved denials

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

IAM_ADMIN_ACCESS_FOR_RUNTIME=DENIED
CLOUD_RUN_ADMIN_ACCESS_FOR_RUNTIME=DENIED

SERVICE_ACCOUNT_KEY_CREATION=DENIED
ARBITRARY_ROLE_GRANTS=DENIED

PRIVATE_REPO_BUILD_DEPENDENCY=DENIED
PRIVATE_REPO_RUNTIME_DEPENDENCY=DENIED

R5_EXECUTION=DENIED
LANDING_DEPLOYMENT=NOT_AUTHORIZED_BY_THIS_ACTIVATION
LANDING_TRAFFIC_PROMOTION=NOT_AUTHORIZED_BY_THIS_ACTIVATION
LOAD_BALANCER_MUTATION=DENIED
URL_MAP_MUTATION=DENIED
NEG_MUTATION=DENIED
BACKEND_SERVICE_MUTATION_OUTSIDE_MG_GUIDE_WEBMCP=DENIED
UNRELATED_CLOUD_RUN_MUTATION=DENIED
ORG_POLICY_MUTATION=DENIED
DOMAIN_POLICY_MUTATION=DENIED
```

The default compute service account is explicitly prohibited:

```text
DEFAULT_COMPUTE_SA_ALLOWED=NO
```

It has independently observed Secret Manager and broad data/admin access and
therefore cannot be the public WebMCP runtime.

## 4. Ingress condition and stop

Direct public Cloud Run ingress is authorized only if current policy accepts
the minimum required invoker posture without an organization-policy,
domain-policy, load-balancer, URL-map, or NEG mutation.

```text
PUBLIC_SYNTHETIC_INGRESS=YES_CONDITIONAL
PUBLIC_INGRESS_POLICY_MUTATION=DENIED
```

If the required direct-public invoker binding is rejected, execution must stop
with:

```text
STOP=WEBMCP_PUBLIC_FRONT_DOOR_SEPARATE_AUTHORIZATION_REQUIRED
```

No substitute front-door workaround is authorized by this activation.

## 5. Required validation and one-shot consumption

Before the first GCP mutation, a consumption record must bind this activation
to the source authorization, their merge SHAs, and the frozen deployment
source SHA, and must record the consuming operator and timestamp. It must
declare:

```text
CONSUMPTION_CONSUMER=VS Code / MG Orchestrator
CONSUMPTION_OPENED_AT_UTC=<actual pre-mutation UTC timestamp>
AUTHORITY_CONSUMED_FOR_EXECUTION=YES
AUTHORITY_REUSE_ALLOWED=NO
CONSUMPTION_ATTEMPTS_MAX=1
```

The accepted backend must prove:

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
SECRET_PAYLOAD_READS=0
REAL_CUSTOMER_DATA=0
```

It must also pass `/health`, `SUCCESS`, `AMBIGUOUS_CONTACT`, negative input,
and approved-origin CORS acceptance before it is handed to the private
host-integration lane.
