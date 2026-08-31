# MG Guide Agent Runtime Deployment Readiness Proof 006

## 1. Identity and boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_READINESS_PROOF_006
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-006.md
PR_CLASS=proof_only
MODE=PRE_AUTHORIZATION_READINESS_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
TARGET_REMOTE_URL=
  https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
RECORDED_AT_UTC=2026-08-31T14:34:54Z

READINESS_WORKTREE=
  /Users/achandler/Google_DevPost/mg-guide-agent-runtime-readiness-006
READINESS_BRANCH=
  proof/mg-guide-agent-runtime-deployment-readiness-006
BRANCH_IS_MAIN=NO
DEDICATED_LANE_WORKTREE=YES
WORKTREE_CLEAN=YES
REPOSITORY_REMOTE_MATCH=YES
ORIGIN_MAIN_MATCHES_EXPECTED=YES
HEAD_BASED_ON_EXPECTED_MAIN=YES
```

This is a fresh non-mutating recheck from the exact current `origin/main`
after merged PR #409. It does not authorize Attempt 006, activate a runtime,
apply Terraform, deploy, mutate IAM or secrets, call HighLevel, or mutate CRM.

```text
ATTEMPT_006_AUTHORIZED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
RUNTIME_ACTIVATION=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_KEY_CREATED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Repository preflight

Verified local checkout origin before any worktree creation:

```text
TARGET_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
TARGET_REMOTE_URL=
  https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
EXPECTED_ORIGIN_MAIN=
  b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
TARGET_MAIN=
  b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
BASE_MAIN_SHA=
  b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
```

Worktree created from exact `origin/main`:

```text
git worktree add -b proof/mg-guide-agent-runtime-deployment-readiness-006 \
  /Users/achandler/Google_DevPost/mg-guide-agent-runtime-readiness-006 \
  origin/main
```

Hard preflight inside the new worktree:

```text
pwd=/Users/achandler/Google_DevPost/mg-guide-agent-runtime-readiness-006
BRANCH=proof/mg-guide-agent-runtime-deployment-readiness-006
HEAD=b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
ORIGIN_MAIN=b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
git status --short --untracked-files=all = empty
```

## 3. Merged repair bindings

```text
REPAIR_PR=409
REPAIR_HEAD=c0232d90e38441ff5a520f3bfd121a8f0505ac28
REPAIR_MERGE_SHA=b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
REPAIR_MERGE_SHA_EQUALS_ORIGIN_MAIN=YES

ATTEMPT_005_ROOT_CAUSE=ADK_RUNTIME_VERSION_COMPATIBILITY
ATTEMPT_005_ROOT_CAUSE_CLOSED=YES
EXPECTED_GOOGLE_ADK_VERSION=1.23.0
EXPECTED_GOOGLE_CLOUD_AIPLATFORM_VERSION=1.165.1
```

Serving contract on this SHA:

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
WRAPPER_IMPORT=from vertexai import agent_engines
ADKAPP_CONSTRUCTION=agent_engines.AdkApp(agent=root_agent)
DEPLOYMENT_GOOGLE_ADK_PIN=google-adk==1.23.0
```

## 4. Deterministic runtime package rebuild

Rebuilt off-repository from exact `origin/main`:

```text
BUILD_COMMAND=
  python3.12 scripts/build_agent_runtime_source.py
    --source-commit b2c58ee5568a90dbb1ea3d09be6d4bc35e727ba5
    --output <ephemeral>/mg-guide-agent-runtime-source.tar.gz

SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67890
SOURCE_PACKAGE_SHA256=
  6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
PRIOR_REPAIR_SOURCE_PACKAGE_SHA256=
  6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
SOURCE_PACKAGE_SHA256_MATCH_PRIOR_REPAIR=YES

GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
SYNTHETIC_SMOKE=PASS
LIVE_GHL_ADAPTER_ENABLED=NO
SECRETS_INCLUDED=NO
PRIVATE_DATA_INCLUDED=NO
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

The archive digest matches the PR #409 repair proof. Content is identical
because the merge commit does not change package members relative to the
repair head.

## 5. Fresh Python 3.12 dependency install

Fresh venv from extracted package `requirements.txt` only:

```text
PYTHON_VERSION=Python 3.12.13
PIP_INSTALL=PASS
PIP_CHECK=PASS
GOOGLE_ADK_VERSION=1.23.0
GOOGLE_CLOUD_AIPLATFORM_VERSION=1.165.1
RUNNER_AUTO_CREATE_SESSION_PARAMETER_PRESENT=YES
```

## 6. Cold serving lifecycle gate

No pre-seeded `vertexai.init()`. Environment only:

```text
VERTEXAI_INIT_PRESEEDED=NO
GOOGLE_CLOUD_PROJECT=ai-rolodex-to-crm
GOOGLE_CLOUD_REGION=us-east1
LOCAL_SDK_AUTHENTICATION_AVAILABLE=YES
ADC_CREDENTIAL_CLASS=Credentials
ADC_PROJECT_DETECTED=ai-rolodex-to-crm
ADC_TOKEN_PRINTED=NO
LOCAL_ADC_PRINCIPAL_EQUALS_RUNTIME_SERVICE_ACCOUNT=NOT_REQUIRED
```

Results:

```text
COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
ENTRYPOINT_OBJECT_TYPE=AdkApp
ENTRYPOINT_OBJECT_MODULE=vertexai.agent_engines.templates.adk
ROOT_AGENT_TYPE=SequentialAgent

REGISTER_OPERATIONS_CALL=PASS
REGISTERED_OPERATION_COUNT=13
REGISTERED_OPERATION_COUNT_GT_ZERO=YES
ASYNC_STREAM_QUERY_REGISTERED=YES

ADKAPP_SET_UP=PASS
ADKAPP_SET_UP_EXCEPTION=NONE
```

Flattened registered operations (13):

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

`AdkApp.register_operations()` returns a grouped dict; the count is the
flattened leaf names, matching prior readiness proofs.

## 7. Resource-location policy

Read-only effective policy:

```text
gcloud org-policies describe gcp.resourceLocations
  --project=ai-rolodex-to-crm --effective --format=yaml
```

```text
LOCATION_POLICY_PASS=YES
EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
EFFECTIVE_POLICY_ALLOWED_VALUE_COUNT=82
EFFECTIVE_POLICY_SHA256=
  6bac4fc11b0370bd72f02664d2fc0d24a478d14fd2ba1303e0c6d4cb5d00af07
```

## 8. Terraform gate

Authoritative root `infra/agent-runtime`. Non-mutating only. Backend false.
Plan saved off-repository. Ephemeral tfvars substituted the rebuilt package
bytes; repository files were not changed.

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan -refresh=false -input=false
  -var-file=<ephemeral-readiness006-tfvars>
  -out=<ephemeral-readiness006-plan>
python3 scripts/verify_agent_runtime_terraform_policy.py
```

```text
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

READINESS_006_PLAN_FILE_SHA256=
  ba99d9820c88c42feadadff96128c1a9554349cde51f117922861a45329e9285
READINESS_006_PLAN_JSON_SHA256=
  72986aa98f736f0d05171124a27f39b725b711317e4113490ac58de86a89b58f
```

Policy script:

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

Fresh Python 3.9 venv from repository-root `requirements.txt`:

```text
CANONICAL_VALIDATION=PASS
LOCAL_PHASE1_DETERMINISTIC=PASS
PYTEST=PASS
PYTEST_EXIT=0
GIT_DIFF_CHECK=PASS
CI_STATUS=PENDING
```

The repository-root pin remains `google-adk==1.18.0` for Phase 1 CI. The
Agent Runtime package pin is `google-adk==1.23.0`. Those are separate
surfaces.

## 10. Readiness decision and stop

```text
READINESS_FOR_AUTHORIZATION_006=YES

ATTEMPT_006_AUTHORIZED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO

STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_AUTHORIZATION_006
```

This proof records readiness evidence only. It does not create Authorization
006 or grant any deployment, activation, IAM, secret, or runtime authority.
