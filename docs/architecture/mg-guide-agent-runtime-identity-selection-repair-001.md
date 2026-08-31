# MG Guide — Agent Runtime Identity Selection Repair 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_IDENTITY_SELECTION_REPAIR_001
ARTIFACT_PATH=
  docs/architecture/mg-guide-agent-runtime-identity-selection-repair-001.md
CLASSIFICATION=IDENTITY_SELECTION_REPAIR_AND_PREDICT_REPROOF
PR_CLASS=architecture
MODE=LOCAL_ADC_IDENTITY_REPAIR_NO_IAM_ROLE_ADDITION
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T01:22:00Z

BRANCH_AT_AUTHORING=
  docs/mg-guide-agent-runtime-identity-selection-repair-001
BRANCH_IS_MAIN=NO

PARENT_BINDING_ARTIFACT=
  docs/architecture/mg-guide-agent-runtime-principal-binding-001.md
PARENT_BINDING_PR=375
PARENT_BINDING_MERGE_SHA=
  ebca138a10b91663ce978d8944be1d46b9beeba9
PARENT_BINDING_PRESENT_ON_ORIGIN_MAIN=YES
```

This unit repairs **local identity selection** so Application Default Credentials
resolve to the durable MG Guide Agent Runtime principal, then re-proves
`aiplatform.endpoints.predict` as that principal.

```text
VERTEX_IAM_ROLE_ADDITIONS=0
ROLES_AIPLATFORM_USER_GRANTS=0
SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
GHL_CALLS=0
CRM_MUTATIONS=0
SECRET_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
IAM_POLICY_WRITES=0
```

Forbidden effects were not performed:

```text
NO_VERTEX_IAM_ROLE_ADDITION=YES
NO_GRANT_TO_BABY_BUMPS=YES
NO_SERVICE_ACCOUNT_KEY_CREATE=YES
NO_NEW_SERVICE_ACCOUNT_CREATE=YES
NO_GHL_CALL=YES
NO_CRM_MUTATION=YES
NO_SECRET_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOY=YES
NO_GEMINI_KEY_PUBLICATION=YES
```

## 1. Durable current state (inputs)

```text
NW008_GHL_403_BLOCKER=CLOSED
PROVIDER_403_RESOLVED=YES

INTENDED_DURABLE_MG_GUIDE_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

PRE_REPAIR_OBSERVED_ADC_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com

PRE_REPAIR_OBSERVED_ADC_EQUALS_INTENDED_RUNTIME=NO

INTENDED_PRINCIPAL_ALREADY_HAS_ROLES_AIPLATFORM_USER=YES
NEW_PROJECT_VERTEX_ROLE_ADDITION_REQUIRED=NO
DO_NOT_GRANT_VERTEX_TO_BABY_BUMPS_FOR_MG_GUIDE=YES
```

## 2. Identity selection inspection (read-only)

### 2.1 Local ADC

```text
LOCAL_ADC_CREDENTIAL_TYPE=other
LOCAL_ADC_CREDENTIAL_SUBTYPE=impersonated_service_account
LOCAL_ADC_FILE=
  ~/.config/gcloud/application_default_credentials.json
LOCAL_ADC_FILE_TYPE_FIELD=impersonated_service_account
LOCAL_ADC_SOURCE_CREDENTIALS_TYPE=authorized_user
LOCAL_ADC_DELEGATES=[]

PRE_REPAIR_LOCAL_ADC_CURRENT_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
LOCAL_ADC_TARGET_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
LOCAL_ADC_REPAIR_REQUIRED=YES
```

No access token, refresh token, credential JSON body, private key, or client
secret is published in this artifact. Inspection used key names and the
impersonation URL's service-account email only.

### 2.2 Environment variables affecting Google auth

```text
GOOGLE_APPLICATION_CREDENTIALS=UNSET
CLOUDSDK_AUTH_IMPERSONATE_SERVICE_ACCOUNT=UNSET
GOOGLE_CLOUD_PROJECT=UNSET
GOOGLE_GENAI_USE_VERTEXAI=UNSET
GOOGLE_CLOUD_LOCATION=UNSET
GEMINI_API_KEY=UNSET
GOOGLE_API_KEY=UNSET
```

Local resolution therefore depended on the well-known ADC file under the active
gcloud config, not on an env-forced credential path.

### 2.3 gcloud active configuration

```text
GCLOUD_CORE_ACCOUNT=themg@themiliare-group.com
GCLOUD_CORE_PROJECT=ai-rolodex-to-crm
GCLOUD_AUTH_IMPERSONATE_SERVICE_ACCOUNT=None
```

`gcloud` CLI impersonation was not set; only the ADC file targeted Baby Bumps.

### 2.4 Impersonation capability (permission probe only)

```text
CALLER_CAN_GET_ACCESS_TOKEN_FOR_INTENDED_PRINCIPAL=YES
CALLER_CAN_ACT_AS_INTENDED_PRINCIPAL=YES
TOKEN_MINT_PERMISSION_PROBE_CLASS=testIamPermissions
TOKEN_VALUE_PRINTED=NO
```

Project-level `roles/iam.serviceAccountTokenCreator` on the operator account
covers the intended principal. No SA-level binding change was required or made.

### 2.5 Deployed runtime / scaffold identity

```text
DEPLOYED_RUNTIME_SERVICE_ACCOUNT_CURRENT=NOT_YET_DEPLOYED
DEPLOYMENT_METADATA_REMOTE_AGENT_RUNTIME_ID=None
DEPLOYMENT_METADATA_DEPLOYMENT_TIMESTAMP=None

DEPLOYED_RUNTIME_SERVICE_ACCOUNT_TARGET=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SCAFFOLD_TERRAFORM_APP_SA_ACCOUNT_ID_PATTERN=
  ${project_name}-app  →  mg-guide-orchestrator-app
SCAFFOLD_DEFAULT_WOULD_CREATE_SEPARATE_SA=YES
SCAFFOLD_DEFAULT_EQUALS_INTENDED=NO

DEPLOYMENT_IDENTITY_REPAIR_REQUIRED=
  NOT_YET_DEPLOYED_BUT_SCAFFOLD_MUST_BIND_INTENDED_BEFORE_DEPLOY
```

The generated Agent Runtime Terraform still defaults to creating
`mg-guide-orchestrator-app@...`. That is **not** the durable MG Guide principal.
No deploy was performed. Before any future deploy authorization, the runtime
service account must be bound to
`mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com` (reuse
existing SA; do not create a second runtime identity by scaffold default).

### 2.6 Repo-local runtime credential selection

```text
ORCHESTRATOR_ENV_EXAMPLE_AUTH_MODE=GOOGLE_CLOUD_ADC_FOR_AGENT_RUNTIME
ORCHESTRATOR_ENV_EXAMPLE_PROJECT=ai-rolodex-to-crm
ORCHESTRATOR_CHECKED_IN_FORCE_OF_BABY_BUMPS=NO
LOCAL_ADC_WAS_SOLE_WRONG_PRINCIPAL_SOURCE=YES
```

## 3. Local ADC repair (executed)

```text
REPAIR_CLASS=
  REWRITE_ADC_IMPERSONATION_TARGET_ONLY
REPAIR_METHOD=
  Atomic rewrite of application_default_credentials.json
  service_account_impersonation_url host SA email
SOURCE_CREDENTIALS_MODIFIED=NO
DELEGATES_MODIFIED=NO
NEW_KEY_CREATED=NO
INTERACTIVE_ADC_LOGIN=NO
```

Pre-repair backup (local workstation only; never committed):

```text
ADC_BACKUP_CREATED=YES
ADC_BACKUP_BASENAME=
  application_default_credentials.json.pre-mg-guide-agent-runtime-repair-20260831T011904Z
ADC_BACKUP_COMMITTED=NO
ADC_FILE_MODE=0600
```

Post-repair ADC observation:

```text
POST_REPAIR_ADC_FILE_TYPE=impersonated_service_account
POST_REPAIR_LOCAL_ADC_CURRENT_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_LOCAL_ADC_PRINCIPAL_EQUALS_INTENDED=YES
ADC_DEFAULT_TOKEN_MINTABLE=YES
EXPLICIT_IMPERSONATION_TOKEN_MINTABLE_AS_INTENDED=YES
TOKEN_VALUES_PUBLISHED=NO
```

```text
LOCAL_ADC_REPAIR_RESULT=PASS
LOCAL_ADC_REPAIR_REQUIRED_AFTER=NO
```

## 4. Vertex role binding — unchanged

Read-only project IAM inspection after repair:

```text
ROLE=roles/aiplatform.user
ROLE_BINDING_COUNT_FOR_AIPLATFORM_USER=1
INTENDED_PRINCIPAL_IN_AIPLATFORM_USER=YES
INTENDED_MEMBER_ROLE_BINDING_COUNT=1
BABY_BUMPS_IN_AIPLATFORM_USER=NO

IAM_POLICY_WRITES_THIS_UNIT=0
EXISTING_VERTEX_ROLE_BINDING_MUTATED=NO
NEW_PROJECT_VERTEX_ROLE_ADDITION_PERFORMED=NO
```

The existing exact-member addition for
`serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`
on `roles/aiplatform.user` remains in place. Baby Bumps was not granted.

## 5. Predict permission reproof (as intended principal)

### 5.1 Policy Troubleshooter

```text
PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PERMISSION=aiplatform.endpoints.predict
RESOURCE=
  //cloudresourcemanager.googleapis.com/projects/ai-rolodex-to-crm
PT_OVERALL_ACCESS=GRANTED
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
```

### 5.2 testIamPermissions as intended principal

```text
TEST_IAM_PERMISSIONS_CALLER=
  access token minted for mg-guide-agent-runtime@... (value not published)
TEST_IAM_RESOURCE=projects/ai-rolodex-to-crm
TEST_IAM_PERMISSION=aiplatform.endpoints.predict
TEST_IAM_PREDICT=YES
```

### 5.3 IAM readiness

```text
OBSERVED_LOCAL_ADC_PRINCIPAL_EQUALS_INTENDED=YES
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
AGENT_RUNTIME_IAM_READY=YES
VERTEX_PREDICT_PERMISSION_REPROOF=PASS
```

## 6. Security gate (still independent)

```text
EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=
  PENDING_HUMAN_ATTESTATION
SECURITY_GATE_SATISFIED=NO
DEPLOYMENT_ALLOWED_BEFORE_SECURITY_GATE=NO

SYNTHETIC_SMOKE_ALLOWED=
  ONLY_AFTER_IAM_READY_AND_SECURITY_GATE_PASS
SYNTHETIC_SMOKE_EXECUTED_IN_THIS_UNIT=NO
```

Both gates are required before synthetic smoke:

| Gate | Status |
| --- | --- |
| `AGENT_RUNTIME_IAM_READY` | YES |
| `EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED` | PENDING_HUMAN_ATTESTATION |

Because the security gate is not yet attested, this unit **does not** run
synthetic-only Agent Runtime smoke, eval generation, or deploy.

## 7. Deferred synthetic smoke contract (not executed)

When human attestation sets
`EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=YES`, a separate unit may run:

```text
INITIAL_MODE=SYNTHETIC_ONLY
LIVE_GHL_ADAPTER_ENABLED=NO
CRM_MUTATION_AUTHORIZED=NO
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO
EXISTING_AGENT_GRAPH=YES
EXISTING_DELEGATES=YES
REQUIRE_DETERMINISTIC_EVAL_HARD_GATES=PASS
```

Then STOP for separate Agent Runtime deployment authorization. Deploy identity
must use the intended principal (section 2.5), not the scaffold default app SA.

## 8. GHL lane separation

```text
NW008_GHL_403_BLOCKER=CLOSED
PROVIDER_403_RESOLVED=YES
GHL_CALLS_IN_THIS_UNIT=0
LIVE_GHL_ADAPTER_ENABLED=NO
PIT_BOUND_TO_AGENT_RUNTIME=NO
```

## 9. Decision board and stop

```text
LOCAL_ADC_CURRENT_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
LOCAL_ADC_TARGET_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
LOCAL_ADC_REPAIR_REQUIRED=NO
OBSERVED_LOCAL_ADC_PRINCIPAL_EQUALS_INTENDED=YES

DEPLOYED_RUNTIME_SERVICE_ACCOUNT_CURRENT=NOT_YET_DEPLOYED
DEPLOYED_RUNTIME_SERVICE_ACCOUNT_TARGET=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
DEPLOYMENT_IDENTITY_REPAIR_REQUIRED=
  NOT_YET_DEPLOYED_BUT_SCAFFOLD_MUST_BIND_INTENDED_BEFORE_DEPLOY

EXISTING_ROLES_AIPLATFORM_USER_UNCHANGED=YES
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
AGENT_RUNTIME_IAM_READY=YES

EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=
  PENDING_HUMAN_ATTESTATION
SYNTHETIC_SMOKE_EXECUTED=NO

NEXT=
  HUMAN_ATTEST_EXPOSED_GEMINI_KEY_ROTATED_OR_REVOKED
  THEN_SYNTHETIC_ONLY_SMOKE_AND_DETERMINISTIC_EVAL
  THEN_SEPARATE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION
  (deploy SA must be intended principal; do not create scaffold default app SA
   as a second runtime identity)

STOP=
  MG_GUIDE_AGENT_RUNTIME_IDENTITY_SELECTION_REPAIR_001_COMPLETE
```
