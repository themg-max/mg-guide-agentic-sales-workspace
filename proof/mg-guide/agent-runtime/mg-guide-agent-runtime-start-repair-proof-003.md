# MG Guide Agent Runtime Start Repair Proof 003

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_START_REPAIR_PROOF_003
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-start-repair-proof-003.md
PR_CLASS=implementation
MODE=BOUNDED_RUNTIME_START_REPAIR
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
IMPLEMENTATION_COMMIT=
  c3795d2dad07293ba44a0dfdbaf4387e6b006a26
```

This unit wraps the existing Unit 3 SequentialAgent graph in an Agent Platform
`AdkApp` serving object and retargets Terraform `python_spec` at that object.
It does not redesign domain agents, nest a local Runner at import time, change
GHL/CRM/IAM, upgrade `google-adk`, add a top-level `agent.py` shim, create
Authorization 005, or deploy.

```text
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
AUTHORIZATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GOOGLE_ADK_UPGRADED=NO
AGENT_PY_SHIM_ADDED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Diagnosis binding

```text
DIAGNOSIS_003_ARTIFACT=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-reasoning-engine-start-failure-diagnosis-003.md
ATTEMPT_004_RESULT=
  FAILED_REASONING_ENGINE_START
ATTEMPT_004_AUTHORITY_CONSUMED=YES
ATTEMPT_004_RETRY_AUTHORIZED=NO

ROOT_CAUSE_CLASS=
  AGENT_RUNTIME_ENTRYPOINT_CONTRACT
FAILED_ENTRYPOINT_MODULE=app.agent
FAILED_ENTRYPOINT_OBJECT=root_agent
FAILED_ENTRYPOINT_TYPE=SequentialAgent
EXACT_FAILURE=
  SequentialAgent missing query/async_query/stream_query/
  bidi_stream_query/async_stream_query
REGISTERED_OPERATION_DISCOVERY=FAIL
```

## 3. Bounded repair surfaces

Changed:

```text
deployment/agent-runtime/app/agent.py
deployment/agent-runtime/app/__init__.py
infra/agent-runtime/service.tf
tests/agents/test_agent_runtime_adkapp_entrypoint.py
```

Unchanged:

```text
KEEP_EXISTING_AGENT_GRAPH=YES
KEEP_EXISTING_DELEGATES=YES
KEEP_ROOT_AGENT_FACTORY=YES
NO_NESTED_RUNNER=YES
deployment/agent-runtime/requirements.txt
google-adk==1.18.0
project=ai-rolodex-to-crm
region=us-east1
runtime service account
IAM / secrets / GHL / CRM
```

Exact import resolved in a clean Python 3.12 environment with only deployment
requirements:

```text
from agentplatform.agent_engines import AdkApp
```

Serving contract:

```python
root_agent = build_unit3_root_agent()
app = App(root_agent=root_agent, name="app")
agent_runtime_app = AdkApp(agent=root_agent)
```

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
ENTRYPOINT_OBJECT_TYPE=AdkApp
HAS_REGISTER_OPERATIONS=YES
HAS_ASYNC_STREAM_QUERY=YES
NO_TERRAFORM_CLASS_METHODS=YES
```

`class_methods` was not added. `AdkApp.register_operations()` already returns a
non-empty operation map including `async_stream_query`.

## 4. Offline registered-operations proof

Clean off-repo Python 3.12 venv. Installed only
`deployment/agent-runtime/requirements.txt`. No GHL or CRM calls.

```text
PIP_INSTALL=PASS
PIP_CHECK=PASS
ENTRYPOINT_IMPORT=PASS
REGISTER_OPERATIONS_CALL=PASS
REGISTERED_OPERATION_COUNT=20
REGISTERED_OPERATION_COUNT_GT_ZERO=YES
ASYNC_STREAM_QUERY_REGISTERED=YES
AGENT_RUNTIME_ENTRYPOINT_CONTRACT=PASS
ROOT_AGENT_TYPE=SequentialAgent
GHL_CALLS=0
CRM_MUTATIONS=0
```

Observed `register_operations()` map (keys only; values listed in the clean-env
run):

```text
"" -> get_session, list_sessions, create_session, delete_session
async -> async_get_session, async_list_sessions, async_create_session,
         async_delete_session, async_add_session_to_memory,
         async_search_memory, async_save_artifact, async_load_artifact,
         async_list_artifact_keys, async_delete_artifact,
         async_list_versions, async_list_artifact_versions,
         async_get_artifact_version
stream -> stream_query
async_stream -> async_stream_query, streaming_agent_run_with_events
```

Focused automated coverage:
`tests/agents/test_agent_runtime_adkapp_entrypoint.py`.

## 5. Package rebuild

Off-repository rebuild from `IMPLEMENTATION_COMMIT`:

```text
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_SHA256=
  57b87eeac6f737a11cc4fd13322c22476594bcd8bf716fa845ccb020dbac972d
SOURCE_PACKAGE_SIZE_BYTES=67895
SOURCE_PACKAGE_FILE_COUNT=54
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
HAS_APP_AGENT=YES
HAS_AGENT_RUNTIME_APP=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

Digest changed from Attempt 004
`1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752` because the
entrypoint module now constructs `agent_runtime_app`. That change is expected
and bounded to the serving wrapper.

## 6. Fresh non-mutating Terraform plan

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

REPAIR_003_PLAN_FILE_SHA256=
  2ce3c8315311c71e049385accdc7af041a7090348ee713cbba2eef0bef7ade16
PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES
PLANNED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
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

PLAN_FILE_COMMITTED_TO_REPOSITORY=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
```

## 7. STOP / NEXT

```text
STOP=INDEPENDENT_REVIEW_REQUIRED
AUTHORIZATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATE=NO
ATTEMPT_004_RETRY_AUTHORIZED=NO

NEXT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_005
  after independent review and merge of this repair
```

Any future deployment still requires a fresh independently reviewed
authorization and human activation. This proof does not activate execution
authority.
