# MG Guide Agent Runtime Deployment Readiness Proof 005

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_READINESS_PROOF_005
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-005.md
PR_CLASS=BOUNDED_PROOF
MODE=PRE_AUTHORIZATION_READINESS_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T10:57:50Z

BRANCH_AT_AUTHORING=
  proof/mg-guide-agent-runtime-deployment-readiness-proof-005
BRANCH_IS_MAIN=NO

CURRENT_MAIN=
  22c1238523f565a66625f6e572e6ab850bc07146
```

This proof records non-mutating readiness evidence after merged PRs 399 and
400. It does not deploy, run `terraform apply`, create Human Activation 005,
mutate IAM, mutate secrets, call HighLevel, mutate CRM, or store source archive
bytes in the repository.

```text
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
AUTHORIZATION_005_CREATED=NO
HUMAN_ACTIVATION_005_CREATED=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Required merged baselines

```text
PR_399_MERGE_SHA=
  8b467b399fd74b9feb3d1d936a7d5c872a18b31c
PR_399_ROLE=
  START_FAILURE_DIAGNOSIS_003_CORRECTED_ENTRYPOINT_OBJECT_CONTRACT
PR_399_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

PR_400_MERGE_SHA=
  22c1238523f565a66625f6e572e6ab850bc07146
PR_400_ROLE=
  VERTEX_SDK_ADKAPP_RUNTIME_START_REPAIR_003
PR_400_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

ALL_REQUIRED_MERGE_SHAS_ON_ORIGIN_MAIN=YES
```

Observed `origin/main` matched `CURRENT_MAIN` exactly after
`git fetch --prune origin`.

## 3. Merged serving contract

Inspected `deployment/agent-runtime/app/agent.py` and
`infra/agent-runtime/service.tf` on `CURRENT_MAIN`.

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app

ROOT_AGENT_TYPE=SequentialAgent
SERVING_OBJECT_TYPE=AdkApp

WRAPPER_IMPORT=
  from vertexai import agent_engines

ROOT_AGENT_GRAPH_CHANGED=NO
DELEGATES_CHANGED=NO
GOOGLE_ADK_VERSION_CHANGED=NO
GOOGLE_ADK_VERSION=
  google-adk==1.18.0
```

Serving object construction in merged source:

```python
root_agent = build_unit3_root_agent()
app = App(root_agent=root_agent, name="app")
agent_runtime_app = agent_engines.AdkApp(agent=root_agent)
```

Terraform PythonSpec binding:

```text
PLANNED_ENTRYPOINT_MODULE=app.agent
PLANNED_ENTRYPOINT_OBJECT=agent_runtime_app
PLANNED_REQUIREMENTS_FILE=requirements.txt
PLANNED_PYTHON_VERSION=3.12
AGENT_FRAMEWORK=google-adk
```

## 4. Post-merge package

Rebuilt from `CURRENT_MAIN` with
`scripts/build_agent_runtime_source.py --source-commit 22c1238523f565a66625f6e572e6ab850bc07146`.

```text
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67896

GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS

CURRENT_MAIN_SOURCE_PACKAGE_SHA256=
  4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57
EXPECTED_REPAIR_DIGEST=
  4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57
POST_MERGE_PACKAGE_DIGEST_MATCH=YES

SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

`scripts/verify_agent_runtime_source_package.py` passed against the exact
archive under the fresh Python 3.12 environment.

```text
PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS
LIVE_GHL_ADAPTER_ENABLED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
SECRETS_INCLUDED=NO
PRIVATE_DATA_INCLUDED=NO
```

## 5. Cold Agent Runtime parity gate

Fresh off-repo Python 3.12 venv:

```text
PYTHON_VERSION=Python 3.12.13
INSTALL_SOURCE=requirements.txt from extracted TAR_GZIP package
PIP_INSTALL=PASS
PIP_CHECK=PASS
VERTEXAI_INIT_PRESEEDED=NO
```

Cold import command used the extracted package only and set the Agent
Runtime-like reserved project and region environment:

```text
GOOGLE_CLOUD_PROJECT=ai-rolodex-to-crm
GOOGLE_CLOUD_REGION=us-east1
PYTHONPATH=<extracted-package>:<extracted-package>/src
```

Result:

```text
COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
ENTRYPOINT_OBJECT_TYPE=AdkApp
ENTRYPOINT_OBJECT_MODULE=vertexai.agent_engines.templates.adk
ADKAPP_CAPTURED_PROJECT=ai-rolodex-to-crm
ADKAPP_CAPTURED_LOCATION=us-east1

HAS_REGISTER_OPERATIONS=YES
HAS_ASYNC_STREAM_QUERY=YES
REGISTER_OPERATIONS_CALL=PASS
REGISTERED_OPERATION_COUNT=13
REGISTERED_OPERATION_COUNT_GT_ZERO=YES
ASYNC_STREAM_QUERY_REGISTERED=YES
```

Observed registered operations:

```text
get_session
list_sessions
create_session
delete_session
async_get_session
async_list_sessions
async_create_session
async_delete_session
async_add_session_to_memory
async_search_memory
stream_query
async_stream_query
streaming_agent_run_with_events
```

Negative control with empty `HOME`, empty `CLOUDSDK_CONFIG`, no
`GOOGLE_APPLICATION_CREDENTIALS`, and no `vertexai.init()` failed before
entrypoint construction completed:

```text
EMPTY_ADC_HOME_COLD_IMPORT=FAIL
FAILURE_CLASS=GoogleAuthError
FAILURE_SUMMARY=
  Unable to find your project. Please provide a project ID by:
  Passing a constructor argument, using vertexai.init(), setting gcloud
  project, or setting a GCP environment variable.
```

The installed SDK source explains the behavior: `AdkApp` reads
`google.cloud.aiplatform.initializer.global_config.project` and `.location`
during construction. The location fallback accepts `GOOGLE_CLOUD_REGION` or
`CLOUD_ML_REGION`; the project path still calls `google.auth.default()` when
`GOOGLE_CLOUD_PROJECT` or `CLOUD_ML_PROJECT_ID` is present so it can bind
credentials and normalize the project value.

## 6. Approved identity gate

The durable runtime principal is still the approved service account:

```text
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

The fresh Terraform plan binds that principal as the Agent Runtime service
account:

```text
RUNTIME_SERVICE_ACCOUNT_MATCH=YES
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

The local cold-import process did not prove that its current ADC resolved to
that approved service account. Read-only metadata from `google.auth.default()`
in the same venv showed:

```text
ADC_DEFAULT_PROJECT=ai-rolodex-to-crm
ADC_CREDENTIAL_CLASS=google.oauth2.credentials.Credentials
ADC_IS_IMPERSONATED=NO
ADC_TARGET_PRINCIPAL=UNKNOWN
ADC_TOKEN_PRINTED=NO
ADC_CREDENTIAL_PAYLOAD_PRINTED=NO

APPROVED_ADC_IDENTITY_CONFIRMED_IN_LOCAL_COLD_PROCESS=NO
```

This does not invalidate the Terraform runtime service-account binding, but it
does mean the stricter requested predicate "run the exact extracted package
under Agent Runtime-like reserved environment and approved ADC identity" is not
fully proven from the local cold process.

```text
FIRST_FAILING_LAYER=
  APPROVED_ADC_IDENTITY_NOT_CONFIRMED_IN_LOCAL_COLD_PROCESS
```

## 7. Policy and toolchain

Read-only policy command:

```text
gcloud org-policies describe gcp.resourceLocations \
  --project=ai-rolodex-to-crm \
  --effective \
  --format=yaml
```

```text
EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
EFFECTIVE_POLICY_ALLOWED_VALUE_COUNT=82
EFFECTIVE_POLICY_EVIDENCE_SHA256=
  90482c90adc929a92dc7a9b4e0c3cce38c4e9952fe81f94a8e069564177ba2b6
```

Toolchain:

```text
TERRAFORM_VERSION=1.9.8
GOOGLE_BETA_PROVIDER_VERSION=7.28.0
```

Repo-local Terraform policy check:

```text
NO_GOOGLE_SERVICE_ACCOUNT_RESOURCE=PASS
NO_SERVICE_ACCOUNT_KEY_RESOURCE=PASS
NO_PROJECT_VERTEX_IAM_RESOURCE=PASS
NO_SECRET_RESOURCE=PASS
NO_MG_GUIDE_ORCHESTRATOR_APP=PASS
RUNTIME_SA_VARIABLE_REQUIRED=PASS
RUNTIME_RESOURCE_USES_SA_VARIABLE=PASS
DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA=PASS
NO_TERRAFORM_STATE_FILES=PASS
```

## 8. Fresh non-mutating Terraform plan

Commands against `AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime` with the
exact current-main TAR_GZIP bytes supplied only through an ephemeral
session-local tfvars file:

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan -refresh=false -input=false
```

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS

READINESS_005_PLAN_FILE_SHA256=
  c0eeb6b912dac4e534568292a60ec646ef9345424715f4c01b7817f381d835d8
PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES

PLANNED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_AGENT_FRAMEWORK=google-adk
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
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

PLAN_FILE_COMMITTED_TO_REPOSITORY=NO
PLAN_JSON_COMMITTED_TO_REPOSITORY=NO
DEPLOYMENT_BYTES_COMMITTED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
```

## 9. Readiness conclusion

```text
READINESS_FOR_AUTHORIZATION_005=NO
AUTHORIZATION_005_CREATE=NO
AUTHORIZATION_005_CREATED=NO
HUMAN_ACTIVATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATED=NO

PASSING_GATES=
  REQUIRED_MERGE_SHAS_ON_MAIN
  MERGED_SERVING_CONTRACT
  POST_MERGE_PACKAGE_DIGEST_MATCH
  COLD_IMPORT_WITH_PROJECT_REGION_ENV
  REGISTERED_OPERATIONS_DISCOVERY
  RESOURCE_LOCATION_POLICY
  FRESH_TERRAFORM_PLAN_SHAPE

BLOCKING_GATE=
  APPROVED_ADC_IDENTITY_CONFIRMED_IN_LOCAL_COLD_PROCESS

STOP=
  APPROVED_ADC_IDENTITY_NOT_CONFIRMED_IN_LOCAL_COLD_PROCESS
```

No Deployment Authorization 005 definition is created by this proof because the
requested readiness predicate requiring the local cold package run to be under
the approved ADC identity was not fully proven. A separate bounded identity
parity repair or an approved Agent Runtime environment evidence path should
prove that `google.auth.default()` resolves to the approved runtime service
account before Authorization 005 is authored.
