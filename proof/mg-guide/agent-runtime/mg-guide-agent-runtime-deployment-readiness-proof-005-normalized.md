# MG Guide Agent Runtime Deployment Readiness Proof 005 Normalized

## 1. Identity and boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_READINESS_PROOF_005_NORMALIZED
ARTIFACT_PATH=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-005-normalized.md
PR_CLASS=proof_only
MODE=PRE_AUTHORIZATION_READINESS_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T12:40:43Z

AUTHORIZED_BRANCH=proof/mg-guide-agent-runtime-deployment-readiness-normalized-005
BRANCH_IS_MAIN=NO
WORKTREE_CLEAN_BEFORE_ARTIFACT=YES

CURRENT_MAIN_EXACT_SHA=291828972065b7d90f205f7af26b18b317dfdbbd
BASE_MAIN_SHA=291828972065b7d90f205f7af26b18b317dfdbbd
```

This is a fresh non-mutating recheck from the exact current `origin/main`.
This proof does not create Authorization 005, create Human Activation 005,
apply Terraform, deploy, activate a runtime, mutate IAM or secrets, call GHL,
or mutate CRM.

```text
AUTHORIZATION_005_CREATE=NO
AUTHORIZATION_005_CREATED=NO
HUMAN_ACTIVATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
RUNTIME_ACTIVATION=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_KEY_CREATED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Merged baselines

The required merged baselines were checked after `git fetch --prune origin`.
Each listed merge SHA is an ancestor of the exact current `origin/main`.

```text
PR_400_ROLE=ADKAPP_SERVING_WRAPPER_REPAIR
PR_400_MERGE_SHA=22c1238523f565a66625f6e572e6ab850bc07146
PR_400_MERGE_SHA_ANCESTOR_OF_CURRENT_MAIN=YES

PR_401_ROLE=HISTORICAL_FAIL_CLOSED_READINESS_005
PR_401_MERGE_SHA=d4e0d2923b91b7f8bec54dfd0da9fb068c13078c
PR_401_MERGE_SHA_ANCESTOR_OF_CURRENT_MAIN=YES

PR_402_ROLE=CLOUD_LOGGING_DIAGNOSIS_004
PR_402_MERGE_SHA=a30350e6a14001191dad851bf5a96193b5efd8b4
PR_402_MERGE_SHA_ANCESTOR_OF_CURRENT_MAIN=YES

PR_403_ROLE=IDENTITY_MODEL_NORMALIZATION_005
PR_403_MERGE_SHA=291828972065b7d90f205f7af26b18b317dfdbbd
PR_403_MERGE_SHA_ANCESTOR_OF_CURRENT_MAIN=YES

ALL_REQUIRED_MERGE_SHAS_ANCESTORS_OF_CURRENT_MAIN=YES
```

PR #402 bound the Attempt 004 Cloud Logging diagnosis to the raw
`SequentialAgent` registered-operation failure. PR #400 changed the serving
entrypoint to the public Vertex SDK `AdkApp` surface. The fresh cold gate below
confirms the logged cause is resolved without claiming a deployment occurred.

```text
ATTEMPT_004_LOGGED_ROOT_CAUSE=REGISTERED_OPERATION_DISCOVERY_ON_RAW_SEQUENTIAL_AGENT
ATTEMPT_004_LOGGED_ROOT_CAUSE_RESOLVED=YES
INDEPENDENT_UNRESOLVED_ATTEMPT_004_RUNTIME_DEFECT=NO
```

## 3. Identity contract

The normalized contract separates local SDK authentication from the workload
identity attached by Terraform to the deployed Reasoning Engine. Local ADC
principal equality with that workload identity is not a readiness predicate.

```text
LOCAL_SDK_AUTHENTICATION_AVAILABLE=YES
ADC_CREDENTIAL_CLASS=Credentials
ADC_PROJECT_DETECTED=ai-rolodex-to-crm
LOCAL_ADC_PRINCIPAL_EQUALS_RUNTIME_SERVICE_ACCOUNT=NOT_REQUIRED

APPROVED_RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PLANNED_RUNTIME_SERVICE_ACCOUNT_EQUALS_APPROVED_SERVICE_ACCOUNT=YES
SERVICE_ACCOUNT_KEY_CREATED=NO
UNAUTHORIZED_IAM_CHANGE=NO
```

`google.auth.default()` succeeded in the fresh Python 3.12 environment without
printing tokens, credential payloads, or account secrets. No service-account
key was created or requested.

## 4. Serving contract

The merged source was inspected at `deployment/agent-runtime/app/agent.py` and
`infra/agent-runtime/service.tf` on `CURRENT_MAIN_EXACT_SHA`.

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
WRAPPER_IMPORT=from vertexai import agent_engines
ADKAPP_CONSTRUCTION=agent_engines.AdkApp(agent=root_agent)

ROOT_AGENT_GRAPH_CHANGED=NO
DELEGATES_CHANGED=NO
GOOGLE_ADK_VERSION_CHANGED=NO
GOOGLE_ADK_VERSION=google-adk==1.18.0
```

Terraform binds `python_spec.entrypoint_module = "app.agent"` and
`python_spec.entrypoint_object = "agent_runtime_app"`; the package requirements
remain `requirements.txt` and the Python version remains `3.12`.

## 5. Fresh package gates

The package was rebuilt off-repository from the exact current main commit:

```text
BUILD_COMMAND=python3.12 scripts/build_agent_runtime_source.py --source-commit 291828972065b7d90f205f7af26b18b317dfdbbd --output <ephemeral>/mg-guide-agent-runtime-source.tar.gz
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67896
SOURCE_PACKAGE_SHA256=4fd2a46facbb7aa6b29e343d3476ef60573f388759a50363caa23cb2f05c0c57

GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
PACKAGE_VERIFICATION=PASS
PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS
LIVE_GHL_ADAPTER_ENABLED=NO
SECRETS_INCLUDED=NO
PRIVATE_DATA_INCLUDED=NO
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

The package verification reported `GHL_CALLS=0` and `CRM_MUTATIONS=0`.

## 6. Cold package gate

A fresh Python 3.12 venv was created from the extracted package. Only the
extracted `requirements.txt` was installed, and `pip check` passed.

```text
PYTHON_VERSION=Python 3.12.13
INSTALL_SOURCE=extracted package requirements.txt
PIP_INSTALL=PASS
PIP_CHECK=PASS

VERTEXAI_INIT_PRESEEDED=NO
GOOGLE_CLOUD_PROJECT=ai-rolodex-to-crm
GOOGLE_CLOUD_REGION=us-east1

COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
ENTRYPOINT_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
HAS_REGISTER_OPERATIONS=YES
HAS_ASYNC_STREAM_QUERY=YES
REGISTER_OPERATIONS_CALL=PASS
REGISTERED_OPERATION_COUNT=13
REGISTERED_OPERATION_COUNT_GT_ZERO=YES
ASYNC_STREAM_QUERY_REGISTERED=YES
```

The observed registered operations were:

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

The cold command imported `app.agent` directly from the extracted package and
did not call `vertexai.init()` before entrypoint construction. It proved local
SDK authentication was available; it did not require or infer local ADC
principal equality with the planned runtime service account.

## 7. Resource-location policy gate

The effective policy was freshly inspected read-only with:

```text
gcloud org-policies describe gcp.resourceLocations --project=ai-rolodex-to-crm --effective --format=yaml
```

```text
EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
EFFECTIVE_POLICY_ALLOWED_VALUE_COUNT=82
EFFECTIVE_POLICY_SHA256=1d92ba86359444afde3bd972c7aaf053bb1e39d47b90319f2fe768127391c066
```

## 8. Terraform gate

The authoritative Terraform root was `infra/agent-runtime`. Only non-mutating
preparation and planning were run:

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan -refresh=false -input=false -var-file=<ephemeral-readiness005-tfvars> -out=<ephemeral-readiness005-plan>
```

```text
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS
TERRAFORM_VERSION=1.9.8
GOOGLE_BETA_PROVIDER_VERSION=7.28.0

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

READINESS_PLAN_SHA256=2571da4d5e3c792cdb4d503fb5f6ee0f805aa65cd152126306cc699bb189a1a1
READINESS_PLAN_JSON_SHA256=8216934031a5d06572617014d4d39a7f838d6de50f3878e30dbd8478157685c8
```

The ephemeral tfvars substituted the exact package bytes and approved binding;
the repository placeholder and Terraform source files were not changed.
The repository policy script also passed all ownership checks:

```text
NO_GOOGLE_SERVICE_ACCOUNT_RESOURCE=PASS
NO_SERVICE_ACCOUNT_KEY_RESOURCE=PASS
NO_PROJECT_VERTEX_IAM_RESOURCE=PASS
NO_SECRET_RESOURCE=PASS
RUNTIME_SA_VARIABLE_REQUIRED=PASS
RUNTIME_RESOURCE_USES_SA_VARIABLE=PASS
DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA=PASS
NO_TERRAFORM_STATE_FILES=PASS
```

## 9. Canonical validation

The local equivalents of the repository-required checks passed in a fresh
Python 3.9 venv using the repository `requirements.txt`:

```text
LOCAL_PHASE1_DETERMINISTIC=PASS
LOCAL_PYTEST=PASS
```

The local Python 3.9 macOS environment emitted a platform support warning for
`grpcio` when `pip check` was probed; the canonical GitHub workflow does not
run that probe. The deterministic verification script and full pytest suite
both completed successfully. The deployment-package Python 3.12 venv above
passed its required `pip check`.

## 10. Readiness decision and stop

```text
IDENTITY_MODEL_NORMALIZATION_005=PASS
ATTEMPT_004_LOGGED_ROOT_CAUSE_RESOLVED=YES
READINESS_FOR_AUTHORIZATION_005=YES

AUTHORIZATION_005_CREATE=NO
AUTHORIZATION_005_CREATED=NO
HUMAN_ACTIVATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
GHL_CALLS=0
CRM_MUTATIONS=0

STOP=INDEPENDENT_REVIEW_REQUIRED
```

This proof records readiness evidence only. It does not create Authorization
005 or grant any deployment, activation, IAM, secret, or runtime authority.
