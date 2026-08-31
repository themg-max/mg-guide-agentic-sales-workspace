# MG Guide Agent Runtime Human Activation 006

## 1. Activation identity and boundary

```text
AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_006
AUTHORIZATION_PR=411
AUTHORIZATION_HEAD=ea1645b4d462d814ef516058b2069f667d9963e0
AUTHORIZATION_MERGE_SHA=4225c68e6047b5158a70b4392b214ad6d678ba61
ACTIVATION_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_006
ARTIFACT_PATH=governance/authorizations/mg-guide-agent-runtime-deployment-human-activation-006.md
CLASSIFICATION=HUMAN_EXECUTION_ACTIVATION_DEFINITION
PR_CLASS=authorization
MODE=ACTIVATION_PREPARATION_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T15:03:21Z
STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW
```

This artifact defines a bounded Human Activation 006 from the merged
Deployment Authorization 006. It is not an execution act, does not consume
authority, and does not create the future Consumption Record 006.

```text
CURRENT_MAIN_EXACT_SHA=4225c68e6047b5158a70b4392b214ad6d678ba61
BASE_MAIN_SHA=4225c68e6047b5158a70b4392b214ad6d678ba61
AUTHORIZATION_ARTIFACT=governance/authorizations/mg-guide-agent-runtime-deployment-authorization-006.md
AUTHORIZATION_ARTIFACT_ON_ORIGIN_MAIN=YES
AUTHORIZATION_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES
AUTHORIZATION_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES
AUTHORIZATION_ARTIFACT_BINDING_VERIFIED=YES
READINESS_FOR_AUTHORIZATION_006=YES
READINESS_PR=410
READINESS_MERGE_SHA=7e1e597dd115a6470e116ab231bf317423e24402
ATTEMPT_004_ROOT_CAUSE_CLOSED=YES
ATTEMPT_005_ROOT_CAUSE_CLOSED=YES
```

## 2. Deployment contract

```text
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
PROJECT=ai-rolodex-to-crm
REGION=us-east1
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_SHA256=6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
GOOGLE_ADK_VERSION=1.23.0
GOOGLE_CLOUD_AIPLATFORM_VERSION=1.165.1
RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
```

## 3. Fresh activation identity

```text
RUN_ID=mg-guide-agent-runtime-deploy-006-20260831T150305Z-1c2d
RUN_ID_FINALIZED=YES
RUN_ID_REUSES_PRIOR_ACTIVATION=NO
WINDOW_START_UTC=2026-08-31T15:03:05Z
WINDOW_END_UTC=2026-08-31T15:58:05Z
WINDOW_DURATION_MINUTES=55
WINDOW_DURATION_MINUTES_LE_60=YES
WINDOW_START_BEFORE_END=YES
WINDOW_EXTENDABLE=NO
ACTIVATION_REUSABLE=NO
ACTIVATION_TRANSFERABLE=NO
```

## 4. Authority semantics

```text
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
```

The activation becomes effective only after independent review, merge, and a
separate explicit human execution act. Merging this artifact cannot itself
start Terraform, deploy a runtime, or consume Authorization 006.

## 5. One-shot ceilings and prohibitions

```text
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
```

## 6. Future Consumption Record 006 contract

```text
PROPOSED_CONSUMPTION_STATE=PREPARED_UNCONSUMED
CONSUMPTION_RECORD_006_CREATED_IN_THIS_UNIT=NO
CONSUMPTION_RECORD_CONSUMED_IN_THIS_UNIT=NO
CONSUMPTION_TRIGGER=FIRST_TERRAFORM_APPLY_ATTEMPT
CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES
```

The future Consumption Record 006 must be newly generated at execution time
and bind all of the following before the first apply attempt:

- current main ancestry for Authorization 006 and this Activation 006 merge SHAs
- rebuilt source package digest exact match:
  `6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf`
- `google-adk==1.23.0` and resolved `google-cloud-aiplatform` compatibility
- `Runner` `auto_create_session` parameter present
- `register_operations` PASS with 13 operations
- `async_stream_query` registered YES
- `AdkApp.set_up` PASS with no exception
- current read-only location-policy evidence (`us-east1` and `global`)
- local SDK authentication available
- a **fresh** execution-time saved Terraform plan and its exact binary + JSON
  SHA256 values (Readiness 006 plan SHAs are not reusable as execution plans)
- `1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY`
- only `google_vertex_ai_reasoning_engine.mg_guide`
- `app.agent:agent_runtime_app` of type `AdkApp`
- approved runtime service account
  `mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`
- no IAM, secret, key, or destroy effects
- the still-valid fixed activation window for this RUN_ID

The future record must also revalidate the exact project `ai-rolodex-to-crm`,
region `us-east1`, Terraform root `infra/agent-runtime`, requirements file,
and Python 3.12 contract. A failed first apply attempt consumes the authority
and permits no retry.

## 7. Preconditions for any future execution

Before any future apply attempt, all of these are required:

- this Human Activation 006 is independently reviewed and merged;
- Authorization 006 is independently reviewed and merged;
- Consumption Record 006 is created separately, fresh, and unconsumed;
- an explicit human execution authority act is recorded separately;
- the run ID is unique and the fixed window is current and unexpired;
- current main ancestry, package digest, ADK lifecycle gates, location policy,
  authentication, and execution-time Terraform plan are revalidated;
- the exact source entrypoint remains `app.agent:agent_runtime_app` of type
  `AdkApp` with `google-adk==1.23.0`; and
- no image spec, alternate binding, IAM change, secret mutation, key creation,
  destroy, retry, fallback, GHL call, or CRM mutation is introduced.

## 8. Current unit zero-effect ledger

```text
HUMAN_ACTIVATION_ARTIFACT_CREATED=YES
CONSUMPTION_RECORD_006_CREATED=NO
AUTHORIZATION_CONSUMED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
RUNTIME_ACTIVATED=NO
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 9. Stop state

```text
STOP_CODE=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_006_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_CONSUMPTION_RECORD_006
DO_NOT_CREATE_CONSUMPTION_RECORD_006=YES
DO_NOT_CONSUME_AUTHORITY=YES
DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_DEPLOY=YES
```
