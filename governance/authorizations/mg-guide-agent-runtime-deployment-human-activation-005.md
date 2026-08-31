# MG Guide Agent Runtime Human Activation 005

## 1. Activation identity and boundary

AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_005
AUTHORIZATION_PR=405
AUTHORIZATION_HEAD=f208d05b718aad8dee51f2198ff5fb74e3d5e55a
AUTHORIZATION_MERGE_SHA=d8d51eaa3b0dd8c417de46ebccbcdaac6f51badd
ACTIVATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_005
ARTIFACT_PATH=governance/authorizations/mg-guide-agent-runtime-deployment-human-activation-005.md
CLASSIFICATION=HUMAN_EXECUTION_ACTIVATION_DEFINITION
PR_CLASS=AUTHORIZATION
MODE=ACTIVATION_PREPARATION_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T13:07:32Z
STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW

This artifact defines a bounded Human Activation 005 from the merged
Deployment Authorization 005. It is not an execution act, does not consume
authority, and does not create the future Consumption Record 005.

CURRENT_MAIN_EXACT_SHA=d8d51eaa3b0dd8c417de46ebccbcdaac6f51badd
AUTHORIZATION_ARTIFACT=governance/authorizations/mg-guide-agent-runtime-deployment-authorization-005.md
AUTHORIZATION_ARTIFACT_ON_ORIGIN_MAIN=YES
AUTHORIZATION_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES
AUTHORIZATION_ARTIFACT_BINDING_VERIFIED=YES
READINESS_FOR_AUTHORIZATION_005=YES
IDENTITY_MODEL_NORMALIZATION_005=PASS
ATTEMPT_004_LOGGED_ROOT_CAUSE_RESOLVED=YES

## 2. Deployment contract

AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
PROJECT=ai-rolodex-to-crm
REGION=us-east1
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_SHA256=4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57
RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO

## 3. Fresh activation identity

RUN_ID=mg-guide-agent-runtime-deploy-005-20260831T130732Z-21f2
RUN_ID_FINALIZED=YES
RUN_ID_REUSES_PRIOR_ACTIVATION=NO
WINDOW_START_UTC=2026-08-31T13:07:32Z
WINDOW_END_UTC=2026-08-31T14:02:32Z
WINDOW_DURATION_MINUTES=55
WINDOW_START_BEFORE_END=YES
WINDOW_EXTENDABLE=NO
ACTIVATION_REUSABLE=NO
ACTIVATION_TRANSFERABLE=NO

## 4. Authority semantics

HUMAN_ACTIVATION_FINALIZED=YES
ACTIVATION_EFFECTIVE=NO
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_PRESENT=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
AUTHORITY_CONSUMED_INITIAL=NO
ACTIVATION_MERGE_ALONE_EXECUTES=NO
SELF_ACTIVATION=FORBIDDEN
HUMAN_EXECUTION_ACT_REQUIRED=YES

The activation becomes effective only after independent review, merge, and a
separate explicit human execution act. Merging this artifact cannot itself
start Terraform, deploy a runtime, or consume Authorization 005.

## 5. One-shot ceilings and prohibitions

MAX_TERRAFORM_APPLY_ATTEMPTS=1
MAX_SUCCESSFUL_DEPLOYMENTS=1
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

## 6. Future Consumption Record 005 contract

PROPOSED_CONSUMPTION_STATE=PREPARED_UNCONSUMED
CONSUMPTION_RECORD_CREATED_IN_THIS_UNIT=NO
CONSUMPTION_RECORD_CONSUMED_IN_THIS_UNIT=NO
CONSUMPTION_TRIGGER=FIRST_TERRAFORM_APPLY_ATTEMPT
CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES

The future Consumption Record 005 must be newly generated at execution time
and bind all of the following before the first apply attempt:

- current source package digest: `4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57`
- current read-only location-policy evidence
- a fresh execution-time saved Terraform plan and its exact SHA256
- `1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY`
- only `google_vertex_ai_reasoning_engine.mg_guide`
- `app.agent:agent_runtime_app`
- `AdkApp`
- approved runtime service account `mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`
- no IAM, secret, key, or destroy effects

The future record must also revalidate the exact project `ai-rolodex-to-crm`,
region `us-east1`, Terraform root `infra/agent-runtime`, requirements file,
Python 3.12 contract, and the still-valid fixed activation window. A failed
first apply attempt consumes the authority and permits no retry.

## 7. Preconditions for any future execution

Before any future apply attempt, all of these are required:

- this Human Activation 005 is independently reviewed and merged;
- Authorization 005 is independently reviewed and merged;
- Consumption Record 005 is created separately, fresh, and unconsumed;
- an explicit human execution authority act is recorded separately;
- the run ID is unique and the fixed window is current and unexpired;
- current main ancestry, package digest, location policy, authentication, and
  execution-time Terraform plan are revalidated;
- the exact source entrypoint remains `app.agent:agent_runtime_app` of type
  `AdkApp`; and
- no image spec, alternate binding, IAM change, secret mutation, key creation,
  destroy, retry, fallback, GHL call, or CRM mutation is introduced.

## 8. Current unit zero-effect ledger

HUMAN_ACTIVATION_ARTIFACT_CREATED=YES
CONSUMPTION_RECORD_005_CREATED=NO
AUTHORIZATION_CONSUMED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
RUNTIME_ACTIVATED=NO
GHL_CALLS=0
CRM_MUTATIONS=0

## 9. Stop state

STOP_CODE=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_005_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED
DO_NOT_CREATE_CONSUMPTION_RECORD_005=YES
DO_NOT_CONSUME_AUTHORITY=YES
DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_DEPLOY=YES
