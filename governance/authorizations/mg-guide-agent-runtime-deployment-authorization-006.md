# MG Guide Agent Runtime Deployment Authorization 006

## 1. Authorization identity and boundary

```text
AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_006
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_006
ARTIFACT_PATH=governance/authorizations/mg-guide-agent-runtime-deployment-authorization-006.md
CLASSIFICATION=DEPLOYMENT_EXECUTION_AUTHORIZATION_DEFINITION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T14:52:00Z
BASE_MAIN_SHA=7e1e597dd115a6470e116ab231bf317423e24402

STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW_THEN_FRESH_HUMAN_ACTIVATION_006
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
DO_NOT_CREATE_HUMAN_ACTIVATION_006=YES
DO_NOT_CREATE_CONSUMPTION_RECORD_006=YES
DO_NOT_APPLY_IN_THIS_UNIT=YES
DO_NOT_DEPLOY_IN_THIS_UNIT=YES
```

This artifact defines a bounded future one-shot authorization for one exact
Attempt-006 MG Guide Agent Runtime creation from merged Readiness 006. Creating,
reviewing, or merging this artifact does not make the authorization effective,
does not create Human Activation 006, does not create Consumption Record 006, and
does not authorize or execute Terraform, deployment, runtime activation, IAM,
secret, service-account, GHL, or CRM actions.

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
reused for Attempt 006.

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
ATTEMPT_004_ROOT_CAUSE_CLOSED=YES

ATTEMPT_005_TERMINAL=YES
ATTEMPT_005_RESULT=FAILED_REASONING_ENGINE_START
ATTEMPT_005_ENGINE_ID=6699297959760101376
ATTEMPT_005_ROOT_CAUSE=ADK_RUNTIME_VERSION_COMPATIBILITY
ATTEMPT_005_ROOT_CAUSE_CLOSED=YES
AUTHORIZATION_005_REUSABLE=NO
ACTIVATION_005_REUSABLE=NO
DO_NOT_RETRY_ATTEMPT_005=YES
```

Attempt 004 failed on registered-operation discovery against a raw
`SequentialAgent`; PR #400 closed that gap with `AdkApp`. Attempt 005 failed
because `AdkApp.set_up()` called `Runner(auto_create_session=True)` while the
runtime package pinned `google-adk==1.18.0`; PR #409 closed that gap by pinning
`google-adk==1.23.0`. Readiness 006 revalidated the full serving lifecycle,
including `AdkApp.set_up()`. Attempt 006 is a new one-shot authority and does
not retry or revive any prior attempt.

## 3. Exact current baseline and readiness binding

```text
CURRENT_MAIN_EXACT_SHA=7e1e597dd115a6470e116ab231bf317423e24402
BASE_MAIN_SHA=7e1e597dd115a6470e116ab231bf317423e24402

READINESS_PR=410
READINESS_HEAD=6c1c49a9caecbfc943a198326bfe6bc4aedeb254
READINESS_MERGE_SHA=7e1e597dd115a6470e116ab231bf317423e24402
READINESS_HEAD_ANCESTOR_OF_CURRENT_MAIN=YES
READINESS_MERGE_SHA_EQUALS_ORIGIN_MAIN=YES

READINESS_ARTIFACT=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-006.md
READINESS_FOR_AUTHORIZATION_006=YES

REPAIR_PR=409
REPAIR_HEAD=c0232d90e38441ff5a520f3bfd121a8f0505ac28
REPAIR_MERGE_SHA=b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
REPAIR_MERGE_SHA_ANCESTOR_OF_CURRENT_MAIN=YES

ATTEMPT_004_ROOT_CAUSE_CLOSED=YES
ATTEMPT_005_ROOT_CAUSE_CLOSED=YES
```

The readiness artifact is the required fresh, non-mutating basis for this
definition. Its package, cold SDK lifecycle (including `AdkApp.set_up()`),
policy, and Terraform plan gates passed before this authorization artifact was
written.

## 4. Serving contract

Attempt 006 must use the merged AdkApp serving wrapper and the repaired ADK pin.
The old raw `root_agent` entrypoint and `google-adk==1.18.0` are not allowed
deployment bindings.

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

GOOGLE_ADK_VERSION=1.23.0
GOOGLE_CLOUD_AIPLATFORM_VERSION=1.165.1
RUNNER_AUTO_CREATE_SESSION_PARAMETER_PRESENT=YES
ADKAPP_REGISTER_OPERATIONS=PASS
ADKAPP_SET_UP=PASS
REGISTERED_OPERATION_COUNT=13
ASYNC_STREAM_QUERY_REGISTERED=YES
```

The existing Unit 3 graph remains the `SequentialAgent`; the serving object is
the `AdkApp` wrapper. The runtime package pin is `google-adk==1.23.0`. No graph
or delegate change is authorized by this artifact.

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

SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
```

The local SDK authentication predicate is separate from the deployed workload
identity. Local ADC principal equality with the approved runtime service account
is not required; Readiness 006 established SDK authentication was available and
the planned Terraform service account matches the approved one.

```text
LOCAL_SDK_AUTHENTICATION_AVAILABLE=YES
LOCAL_ADC_PRINCIPAL_EQUALS_RUNTIME_SERVICE_ACCOUNT=NOT_REQUIRED
NO_SERVICE_ACCOUNT_KEY_CREATED=YES
NO_UNAUTHORIZED_IAM_CHANGE=YES
```

## 6. Frozen source package and readiness plan evidence

The source package and readiness plan values below are authoring-time evidence
from Readiness 006. A future consumer must regenerate a fresh execution-time
plan and package verification from the then-current approved baseline and stop
if any required value or predicate changes.

```text
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67890
SOURCE_PACKAGE_SHA256=6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
SOURCE_PACKAGE_SHA256_MATCH=YES
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
PACKAGE_VERIFICATION=PASS
COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
REGISTER_OPERATIONS_CALL=PASS
ADKAPP_SET_UP=PASS
ASYNC_STREAM_QUERY_REGISTERED=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

The effective location policy was freshly rechecked in Readiness 006 and allowed
both the target region and the global control-plane location:

```text
EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
```

Readiness 006 plan evidence (authoring-time only; not an execution plan):

```text
READINESS_006_PLAN_FILE_SHA256=ba99d9820c88c42feadadff96128c1a9554349cde51f117922861a45329e9285
READINESS_006_PLAN_JSON_SHA256=72986aa98f736f0d05171124a27f39b725b711317e4113490ac58de86a89b58f
READINESS_PLAN_IS_EXECUTION_PLAN=NO
FRESH_EXECUTION_TIME_PLAN_REQUIRED=YES

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

If and only if a separate Human Activation 006 is independently reviewed and
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
mismatch, ADK version mismatch, missing `AdkApp.set_up` revalidation, policy
failure, or missing fresh activation is a hard stop. This authorization does not
authorize retries, alternate regions/projects, a raw `root_agent` entrypoint,
`image_spec`, a second apply, fallback deployment, or compensating mutation.

## 8. Future Human Activation 006 requirement

This unit does not create Human Activation 006. After independent review and
merge of this exact authorization, a separate activation artifact must be
created and independently reviewed.

```text
NEXT_AFTER_THIS_AUTHORIZATION_MERGES=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_006
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
HUMAN_ACTIVATION_006_CREATED=NO
CONSUMPTION_RECORD_006_CREATED=NO
```

Human Activation 006 must bind all of the following before any future apply:

```text
ACTIVATION_MUST_BIND=
  - this exact authorization artifact
  - AUTHORIZATION_PR=<future exact PR number after Authorization 006 merges>
  - AUTHORIZATION_HEAD=<future exact head SHA>
  - AUTHORIZATION_MERGE_SHA=<future exact merge SHA of Authorization 006>
  - a fresh unique RUN_ID (not chosen in this authorization unit)
  - a fixed UTC execution window of at most 60 minutes
  - WINDOW_EXTENDABLE=NO
  - ACTIVATION_REUSABLE=NO
  - ACTIVATION_TRANSFERABLE=NO
  - one attempt only
  - CONSUMPTION_TRIGGER=FIRST_TERRAFORM_APPLY_ATTEMPT
  - CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES
  - explicit human execution authority
```

```text
ACTIVATION_006_REQUIRES_NEW_RUN_ID=YES
ACTIVATION_006_REQUIRES_FIXED_UTC_WINDOW=YES
ACTIVATION_006_REQUIRES_NEW_CONSUMPTION_RECORD=YES
ACTIVATION_006_MAY_REUSE_PRIOR_RUN_ID=NO
ACTIVATION_006_MAY_REUSE_PRIOR_WINDOW=NO
ACTIVATION_006_CONSUMES_ON_FIRST_APPLY_ATTEMPT=YES
ACTIVATION_006_SELF_ACTIVATION=FORBIDDEN
ACTIVATION_REUSABLE=NO
WINDOW_EXTENDABLE=NO
WINDOW_DURATION_MINUTES_MAX=60
```

No RUN_ID or activation window is chosen in this authorization unit. No
consumption record is created in this authorization unit.

## 9. Future one-shot execution contract

Only after this authorization and a separate Human Activation 006 are
independently reviewed and merged, and a fresh unconsumed Consumption Record 006
exists, may a future consumer consider one apply. The consumer must revalidate
all of the following immediately before mutation:

```text
REQUIRED_PRE_APPLY_RECHECKS=
  - current required merge SHAs remain ancestors of origin/main
  - Authorization 006 and Activation 006 merge SHAs are ancestors of origin/main
  - source package is rebuilt from the exact approved baseline
  - source package SHA256 equals 6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
  - google-adk==1.23.0 is present in the package requirements
  - Runner auto_create_session parameter is present
  - register_operations PASS with 13 operations
  - async_stream_query registered YES
  - AdkApp.set_up PASS with no exception
  - effective gcp.resourceLocations permits us-east1 and global
  - local SDK authentication available
  - FRESH execution-time saved Terraform plan is produced (readiness plan is not reusable)
  - execution plan binary SHA256 and plan JSON SHA256 are recorded
  - plan is exactly 1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
  - plan contains only google_vertex_ai_reasoning_engine.mg_guide
  - plan uses python_spec only, never image_spec
  - plan binds app.agent:agent_runtime_app and AdkApp
  - plan binds the approved runtime service account
  - plan creates no service account, key, IAM binding, secret, or destroy effect
  - fixed activation window is current and unexpired
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
CONSUMPTION_TRIGGER=FIRST_TERRAFORM_APPLY_ATTEMPT
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

HUMAN_ACTIVATION_006_CREATED=NO
CONSUMPTION_RECORD_006_CREATED=NO
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

## 11. Parallel template rule (non-finalization)

Non-durable draft templates for Human Activation 006 and Consumption Record 006
may be prepared outside this authorization unit for sequencing readiness. They
must not be finalized, committed, PR'd, activated, consumed, applied, or
deployed until the exact Authorization 006 merge SHA (for activation) and the
exact Activation 006 merge SHA plus fresh execution-time evidence (for
consumption) are available.

```text
ACTIVATION_006_TEMPLATE_DRAFT_ALLOWED=YES
CONSUMPTION_006_TEMPLATE_DRAFT_ALLOWED=YES
ACTIVATION_006_FINALIZATION_ALLOWED_NOW=NO
ACTIVATION_006_PR_ALLOWED_NOW=NO
CONSUMPTION_006_EXECUTION_EVIDENCE_ALLOWED_NOW=NO
CONSUMPTION_006_PR_ALLOWED_NOW=NO
```

## 12. Stop state

```text
STOP_CODE=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_006_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_HUMAN_ACTIVATION_006
DO_NOT_CREATE_HUMAN_ACTIVATION_006=YES
DO_NOT_CREATE_CONSUMPTION_RECORD_006=YES
DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_DEPLOY=YES
```

This is a definition-only authorization candidate. It does not activate
execution and must not be treated as effective merely because it is committed,
reviewed, merged, or present in the repository.
