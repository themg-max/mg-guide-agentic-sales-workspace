# MG Guide Agent Runtime Deployment Authorization 005

## 1. Authorization identity and boundary

```text
AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_005
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_005
ARTIFACT_PATH=governance/authorizations/mg-guide-agent-runtime-deployment-authorization-005.md
CLASSIFICATION=DEPLOYMENT_EXECUTION_AUTHORIZATION_DEFINITION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T12:54:44Z

STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW_THEN_FRESH_HUMAN_ACTIVATION_005
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
DO_NOT_CREATE_HUMAN_ACTIVATION_005=YES
DO_NOT_APPLY_IN_THIS_UNIT=YES
DO_NOT_DEPLOY_IN_THIS_UNIT=YES
```

This artifact defines a bounded future one-shot authorization for one exact
Attempt-005 MG Guide Agent Runtime creation. Creating, reviewing, or merging
this artifact does not make the authorization effective, does not create Human
Activation 005, and does not authorize or execute Terraform, deployment,
runtime activation, IAM, secret, service-account, GHL, or CRM actions.

```text
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
ARTIFACT_MERGE_IS_EXECUTION_AUTHORITY=NO
SELF_ACTIVATION=FORBIDDEN
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
```

## 2. Prior attempts and non-reuse

Prior deployment attempts and their authorizations are terminal and cannot be
reused for Attempt 005.

```text
ATTEMPT_001_TERMINAL=YES
ATTEMPT_001_RESULT=FAILED_ORG_POLICY_GCP_RESOURCE_LOCATIONS
AUTHORIZATION_001_REUSABLE=NO
ACTIVATION_001_REUSABLE=NO

ATTEMPT_002_TERMINAL=YES
ATTEMPT_002_RESULT=FAILED_REASONING_ENGINE_BUILD_PACKAGE_LAYOUT
AUTHORIZATION_002_REUSABLE=NO
ACTIVATION_002_REUSABLE=NO

ATTEMPT_003_TERMINAL=YES
ATTEMPT_003_RESULT=FAILED_REASONING_ENGINE_BUILD
AUTHORIZATION_003_REUSABLE=NO
ACTIVATION_003_REUSABLE=NO

ATTEMPT_004_TERMINAL=YES
ATTEMPT_004_RESULT=FAILED_REASONING_ENGINE_START_REGISTERED_OPERATION_DISCOVERY
AUTHORIZATION_004_REUSABLE=NO
ACTIVATION_004_REUSABLE=NO
```

Attempt 004's logged root cause was the registered-operation failure on a raw
`SequentialAgent`. PR #400 repaired the serving-object contract by exposing the
existing graph through `vertexai.agent_engines.AdkApp`; the normalized Readiness
005 proof verified that repair. Attempt 005 is a new one-shot authority and
does not retry or revive any prior attempt.

## 3. Exact current baseline and readiness binding

```text
CURRENT_MAIN_EXACT_SHA=e2421d4bf86de06cfd6b1824c6bab18128be7412
PR_404_HEAD=8d547d0cabfd110bb7581d359b8dcc062a0fb986
PR_404_MERGE_SHA=e2421d4bf86de06cfd6b1824c6bab18128be7412
PR_404_HEAD_ANCESTOR_OF_CURRENT_MAIN=YES

READINESS_ARTIFACT=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-005-normalized.md
READINESS_FOR_AUTHORIZATION_005=YES
IDENTITY_MODEL_NORMALIZATION_005=PASS
ATTEMPT_004_LOGGED_ROOT_CAUSE_RESOLVED=YES
```

The readiness artifact is the required fresh, non-mutating basis for this
definition. Its exact current-main package, cold SDK, policy, and Terraform
plan gates passed before this authorization artifact was written.

## 4. Serving contract

Attempt 005 must use the merged serving wrapper. The old raw `root_agent`
entrypoint is not an allowed deployment binding.

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
AGENT_FRAMEWORK=google-adk
WRAPPER_IMPORT=from vertexai import agent_engines
ADKAPP_CONSTRUCTION=agent_engines.AdkApp(agent=root_agent)
```

The existing Unit 3 graph remains the `SequentialAgent`; the serving object is
the `AdkApp` wrapper. The package keeps `google-adk==1.18.0`, and no graph,
delegate, or dependency change is authorized by this artifact.

## 5. Exact deployment binding

```text
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
PROJECT=ai-rolodex-to-crm
REGION=us-east1

APPROVED_RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PLANNED_RUNTIME_SERVICE_ACCOUNT_EQUALS_APPROVED_SERVICE_ACCOUNT=YES
RUNTIME_SERVICE_ACCOUNT_REUSE_EXISTING=YES
TERRAFORM_OWNS_RUNTIME_SERVICE_ACCOUNT=NO
TERRAFORM_OWNS_RUNTIME_SA_KEYS=NO
TERRAFORM_OWNS_VERTEX_PROJECT_IAM=NO

EXPECTED_RESOURCE=google_vertex_ai_reasoning_engine.mg_guide
```

The local SDK authentication predicate is separate from the deployed workload
identity. Local ADC principal equality with the approved runtime service account
is not required; the fresh readiness proof established SDK authentication was
available and the planned Terraform service account matches the approved one.

```text
LOCAL_SDK_AUTHENTICATION_AVAILABLE=YES
LOCAL_ADC_PRINCIPAL_EQUALS_RUNTIME_SERVICE_ACCOUNT=NOT_REQUIRED
NO_SERVICE_ACCOUNT_KEY_CREATED=YES
NO_UNAUTHORIZED_IAM_CHANGE=YES
```

## 6. Frozen source package and plan evidence

The source package and plan values below are authoring-time evidence. A future
consumer must regenerate both from the then-current approved baseline and stop
if any value or predicate changes.

```text
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67896
SOURCE_PACKAGE_SHA256=4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57
SOURCE_PACKAGE_SHA256_MATCH=YES
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
PACKAGE_VERIFICATION=PASS
COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
REGISTER_OPERATIONS_CALL=PASS
ASYNC_STREAM_QUERY_REGISTERED=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

The effective location policy was freshly rechecked and allowed both the target
region and the global control-plane location:

```text
EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
```

The fresh non-mutating plan used the exact package bytes through an ephemeral
tfvars file:

```text
AUTHORIZATION_005_PLAN_FILE_SHA256=2bb8cbe4d544ba0abe62b90f51a6e38f8970b446f05f58fc2a808cdcbcc85e3c
AUTHORIZATION_005_PLAN_JSON_SHA256=044f421d3c2e328691dad1b7a772159e10e7249ee85ab9313984063a6a924678
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES

PLANNED_RESOURCE=google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES

SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
PLANNED_ENTRYPOINT_MODULE=app.agent
PLANNED_ENTRYPOINT_OBJECT=agent_runtime_app
PLANNED_REQUIREMENTS_FILE=requirements.txt
PLANNED_PYTHON_VERSION=3.12

PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_DESTROYS_RESOURCE=NO
```

Terraform authoring used version 1.9.8 with `google-beta` provider 7.28.0.
The checked-in `dev.tfvars` placeholder remains unchanged; package bytes,
base64 payload, tfvars, and saved plans remain outside the repository.

## 7. Authorization ceilings and hard prohibitions

If and only if a separate Human Activation 005 is independently reviewed and
merged, these ceilings define the maximum future execution scope:

```text
MAX_DEPLOYMENTS=1
MAX_SUCCESSFUL_DEPLOYMENTS=1
MAX_TERRAFORM_APPLY_ATTEMPTS=1
MAX_AGENT_RUNTIME_RESOURCES_CREATED=1

NO_RETRY=YES
NO_SECOND_APPLY=YES
NO_FALLBACK_DEPLOYMENT=YES
NO_COMPENSATING_MUTATION=YES
NO_AGENTS_CLI_DEPLOY=YES
NO_ALTERNATE_TERRAFORM_ROOT=YES
NO_ALTERNATE_PROJECT=YES
NO_ALTERNATE_REGION=YES
NO_ALTERNATE_RUNTIME_SERVICE_ACCOUNT=YES
NO_ALTERNATE_SOURCE_PACKAGE=YES
NO_IMAGE_SPEC=YES

RESOURCE_DESTROY_ALLOWED=NO
SERVICE_ACCOUNT_CREATE_ALLOWED=NO
SERVICE_ACCOUNT_KEY_CREATE_ALLOWED=NO
IAM_MUTATION_ALLOWED=NO
SECRET_MUTATION_ALLOWED=NO
SECRET_PAYLOAD_READ_ALLOWED=NO
GHL_CALL_ALLOWED=NO
CRM_MUTATION_ALLOWED=NO
CRM_WRITE_ALLOWED=NO
```

Any unexpected plan effect, digest mismatch, baseline mismatch, serving-object
mismatch, policy failure, or missing fresh activation is a hard stop. This
authorization does not authorize retries, alternate regions/projects, a raw
`root_agent` entrypoint, `image_spec`, a second apply, fallback deployment, or
compensating mutation.

## 8. Future Human Activation 005 requirement

This unit does not create Human Activation 005. After independent review and
merge of this exact authorization, a separate activation artifact must be
created and independently reviewed.

```text
NEXT_AFTER_THIS_AUTHORIZATION_MERGES=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_005
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
HUMAN_ACTIVATION_005_CREATED=NO
```

Human Activation 005 must bind all of the following before any future apply:

```text
ACTIVATION_MUST_BIND=
  - this exact authorization artifact and its merge SHA
  - a fresh run ID
  - a fixed UTC execution window of at most 60 minutes
  - one attempt only
  - consumption on the first apply attempt
  - explicit human execution authority
```

```text
ACTIVATION_005_REQUIRES_NEW_RUN_ID=YES
ACTIVATION_005_REQUIRES_FIXED_UTC_WINDOW=YES
ACTIVATION_005_REQUIRES_NEW_CONSUMPTION_RECORD=YES
ACTIVATION_005_MAY_REUSE_PRIOR_RUN_ID=NO
ACTIVATION_005_MAY_REUSE_PRIOR_WINDOW=NO
ACTIVATION_005_CONSUMES_ON_FIRST_APPLY_ATTEMPT=YES
ACTIVATION_005_SELF_ACTIVATION=FORBIDDEN
ACTIVATION_REUSABLE=NO
WINDOW_EXTENDABLE=NO
```

No consumption record is created in this authorization unit.

## 9. Future one-shot execution contract

Only after this authorization and a separate Human Activation 005 are
independently reviewed and merged, and a fresh unconsumed consumption record
exists, may a future consumer consider one apply. The consumer must revalidate
all of the following immediately before mutation:

```text
REQUIRED_PRE_APPLY_RECHECKS=
  - current required merge SHAs remain ancestors of origin/main
  - source package is rebuilt from the exact approved baseline
  - source package SHA256 equals 4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57
  - effective gcp.resourceLocations permits us-east1 and global
  - plan is exactly 1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
  - plan contains only google_vertex_ai_reasoning_engine.mg_guide
  - plan uses python_spec only, never image_spec
  - plan binds app.agent:agent_runtime_app and AdkApp
  - plan binds the approved runtime service account
  - plan creates no service account, key, IAM binding, secret, or destroy effect
```

The sole allowed future mutation is one Terraform apply against the
authoritative root, after consumption and explicit human execution authority:

```text
ALLOWED_FUTURE_COMMAND_CLASS=
  terraform apply against infra/agent-runtime
  with ephemeral exact source archive input
  one attempt only

FORBIDDEN_FUTURE_COMMAND_CLASSES=
  agents-cli deploy
  second terraform apply
  retry after failure or partial success
  terraform destroy
  service account create
  service account key create
  project or Vertex IAM mutation
  secret mutation or secret payload read
  GHL call
  CRM mutation
```

```text
CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES
NO_SECOND_APPLY=YES
NO_RETRY=YES
NO_COMPENSATING_MUTATION=YES
```

If the future apply fails or its post-apply ledger is incomplete, authority is
consumed and this artifact authorizes no retry or recovery mutation.

## 10. Current non-authority and zero-effect ledger

```text
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO

HUMAN_ACTIVATION_005_CREATED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
RESOURCES_CREATED=0
RESOURCES_CHANGED=0
RESOURCES_DESTROYED=0

SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEYS_CREATED=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
GHL_CALLS=0
CRM_MUTATIONS=0
CRM_CALLS=0
```

## 11. Stop state

```text
STOP_CODE=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_005_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED
DO_NOT_CREATE_HUMAN_ACTIVATION_005=YES
DO_NOT_CREATE_CONSUMPTION_RECORD_005=YES
DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_DEPLOY=YES
```

This is a definition-only authorization candidate. It does not activate
execution and must not be treated as effective merely because it is committed,
reviewed, merged, or present in the repository.
