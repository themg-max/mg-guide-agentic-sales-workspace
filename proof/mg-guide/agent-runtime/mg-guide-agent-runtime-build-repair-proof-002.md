# MG Guide Agent Runtime Build Repair Proof 002

## 1. Identity and boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_BUILD_REPAIR_PROOF_002
ARTIFACT_PATH=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-build-repair-proof-002.md
PR_CLASS=workflow_or_infra
MODE=BOUNDED_BUILD_REPAIR
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
IMPLEMENTATION_BRANCH=impl/mg-guide-agent-runtime-build-repair-002
BASE_COMMIT=cbda336b9cdcb3806e54b0805a0e6e38d925e981
```

This repair changes only the Reasoning Engine source-code selection in
`infra/agent-runtime/service.tf` and records its offline evidence here. It does
not change the source-package builder, `requirements.txt`, the agent graph,
delegates, runtime service account, IAM, secrets, GHL, CRM, project, or region.

```text
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
AUTHORIZATION_004_CREATE=NO
HUMAN_ACTIVATION_004_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Diagnosis binding

```text
DIAGNOSIS_002_COMMIT=cbda336b9cdcb3806e54b0805a0e6e38d925e981
DIAGNOSIS_002_ARTIFACT=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-reasoning-engine-build-failure-diagnosis-002.md
ATTEMPT_003_TERMINAL_COMMIT=bba46a1a5e0aeade611f490a505790d379543b5c
ATTEMPT_003_RESULT=FAILED_REASONING_ENGINE_BUILD
ATTEMPT_003_AUTHORITY_CONSUMED=YES
ATTEMPT_003_RETRY_AUTHORIZED=NO
ROOT_CAUSE_CLASS=PACKAGE_LAYOUT
FIRST_FAILURE_STEP=STEP_3_DOCKER_BUILD
EXACT_FAILURE=MISSING_/workspace/user_code/Dockerfile
```

Diagnosis 002 established that the TAR_GZIP package extracted successfully, but
`image_spec {}` selected the Dockerfile-driven build path. The builder failed
before requirements installation or Python import because the Python-source
package intentionally contains no Dockerfile.

## 3. Bounded Terraform repair

The former empty `image_spec {}` block was replaced with this Python-source
contract. No other Terraform resource or source-package behavior changed.

```hcl
source_code_spec {
  inline_source {
    source_archive = var.agent_source_archive_b64
  }

  python_spec {
    entrypoint_module = "app.agent"
    entrypoint_object = "root_agent"
    requirements_file = "requirements.txt"
    version           = "3.12"
  }
}
```

```text
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=root_agent
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
```

## 4. Unchanged deterministic source package

The merged deterministic builder rebuilt the same package source at
`SOURCE_BUILD_COMMIT`. The archive stayed outside the repository and was not
committed or supplied to any deployment operation.

```text
SOURCE_BUILD_COMMIT=cbda336b9cdcb3806e54b0805a0e6e38d925e981
SOURCE_PACKAGE_FORMAT=TAR_GZIP
REPAIRED_SOURCE_PACKAGE_SHA256=1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752
SOURCE_PACKAGE_SIZE_BYTES=67778
SOURCE_PACKAGE_FILE_COUNT=54
IS_GZIP=YES
IS_TAR_GZIP=YES
IS_ZIP=NO
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
HAS_REQUIREMENTS_TXT=YES
HAS_APP_AGENT=YES
HAS_DOCKERFILE=NO
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
```

## 5. Clean Python 3.12 reproduction

An off-repository Python 3.12.13 virtual environment extracted the exact
candidate, installed the unchanged requirements with `pip install -r
requirements.txt`, then imported `app.agent`.

```text
REQUIREMENTS_TXT_CHANGED=NO
CLEAN_VENV_PIP_INSTALL=PASS
ENTRYPOINT_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
APP_LOAD=PASS
ROOT_AGENT_TYPE=SequentialAgent
APP_TYPE=App
GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

The archive safety regression suite ran in the same ephemeral Python 3.12
environment after installing the test-only `pytest` runner. Production
requirements and source-package contents remained unchanged.

```text
FOCUSED_SOURCE_PACKAGE_TESTS=PASS
FOCUSED_SOURCE_PACKAGE_TEST_COUNT=10
```

## 6. Fresh non-mutating Terraform plan

The repaired TAR_GZIP bytes were passed only as an ephemeral sensitive
Terraform variable. `terraform init -backend=false -input=false`, validation,
and the plan completed without applying infrastructure changes.

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS
PLAN_FILE_SHA256=398ee7c702bad0a36a58e7a0b6490512bd7c77806b40b83c42b572fb9978bb38
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES
PLANNED_RESOURCE=google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_DESTROYS_RESOURCE=NO
```

The plan contains only one resource change, a create for
`google_vertex_ai_reasoning_engine.mg_guide`. The plan file, source archive,
and base64 payload remain outside the repository.

## 7. Additional local checks

```text
TERRAFORM_OWNERSHIP_POLICY=PASS
NO_GOOGLE_SERVICE_ACCOUNT_RESOURCE=PASS
NO_SERVICE_ACCOUNT_KEY_RESOURCE=PASS
NO_PROJECT_VERTEX_IAM_RESOURCE=PASS
NO_SECRET_RESOURCE=PASS
DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA=PASS
GIT_DIFF_CHECK=PASS
```

## 8. Stop condition

```text
STOP=INDEPENDENT_REVIEW_REQUIRED
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
AUTHORIZATION_004_CREATE=NO
HUMAN_ACTIVATION_004_CREATE=NO
```

This proof validates a source-spec repair only. Any future deployment attempt
requires separate, fresh authority and must not reuse Attempt 003 authority.
