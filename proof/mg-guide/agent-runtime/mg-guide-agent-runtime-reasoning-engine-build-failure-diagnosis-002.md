# MG Guide Agent Runtime Reasoning Engine Build Failure Diagnosis 002

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_BUILD_FAILURE_DIAGNOSIS_002
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-reasoning-engine-build-failure-diagnosis-002.md
PR_CLASS=BOUNDED_PROOF
MODE=READ_ONLY_BUILD_FAILURE_DIAGNOSIS
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZED_ATTEMPT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_ATTEMPT_003
RUN_ID=
  mg-guide-agent-runtime-deploy-003-20260831T070019Z-85e0a83c

ATTEMPT_003_TERMINAL_COMMIT=
  bba46a1a5e0aeade611f490a505790d379543b5c
ATTEMPT_003_TERMINAL_BRANCH=
  proof/mg-guide-agent-runtime-deployment-preparation-003
```

This proof records a read-only diagnosis of the terminal Attempt 003 Reasoning
Engine build failure. It does not authorize another deployment, retry apply,
create Authorization 004, mutate IAM, secrets, or service accounts, change
package dependencies, or perform any cloud write.

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
AUTHORIZATION_004_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
PACKAGE_DEPENDENCIES_CHANGED=NO
DEPLOYMENT_EXECUTED=NO
```

## 2. Attempt 003 remains terminal and non-reusable

```text
ATTEMPT_003_RESULT=
  FAILED_REASONING_ENGINE_BUILD
ATTEMPT_003_TERMINAL=YES
ATTEMPT_003_AUTHORITY_CONSUMED=YES
ATTEMPT_003_APPLY_ATTEMPTS=1
ATTEMPT_003_RETRY_AUTHORIZED=NO
AUTHORIZATION_003_REUSABLE=NO
ACTIVATION_003_REUSABLE=NO
AGENT_RUNTIME_RESOURCES_CREATED=0

AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_003
AUTHORIZATION_PR=390
AUTHORIZATION_MERGE_SHA=
  66eda45252d2e368a9a2883da40836617deb9583

ACTIVATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_003
ACTIVATION_PR=391
ACTIVATION_MERGE_SHA=
  13e9b4370f95f059fe739d3c705396e5b5172edc

APPLY_DISPATCHED_AT_UTC=2026-08-31T07:50:37Z
APPLY_COMPLETED_AT_UTC=2026-08-31T07:51:19Z
APPLY_LOG_SHA256=
  76659fbd9565b1de7bc242616777880a56638806ad2b65489f72ba5237a438b2

SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_SHA256=
  1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752
```

## 3. Local apply-log evidence

The complete local apply log matching `APPLY_LOG_SHA256` contains no application
container image ID. The provider error is only:

```text
Error waiting to create ReasoningEngine: Error waiting for Creating
ReasoningEngine: Error code 3, message: Build failed. The issue might be
caused by incorrect code, requirements.txt file or other dependencies.
```

```text
PROVIDER_ERROR_CODE=3
PROVIDER_ERROR_CLASS=REASONING_ENGINE_BUILD_FAILED
APPLY_LOG_CONTAINS_BUILD_ID=NO
APPLY_LOG_CONTAINS_REASONING_ENGINE_ID=NO
APPLY_LOG_CONTAINS_OPERATION_NAME=NO
```

The provider message is generic and is not by itself a proven root cause. Cloud
Logging and the create-operation metadata supply the exact first failure.

## 4. Identifiers recovered from Cloud Logging and operation metadata

Read-only sources:

```text
gcloud logging read
  logName=
    projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_build
  timestamp 2026-08-31T07:50:30Z through 2026-08-31T07:52:00Z
  project=ai-rolodex-to-crm

gcloud ai operations describe 7388331316720173056
  --project=ai-rolodex-to-crm
  --region=us-east1
```

```text
PROJECT=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
REGION=us-east1
REASONING_ENGINE_ID=1107656809914564608
OPERATION_NAME=
  projects/831270426395/locations/us-east1/reasoningEngines/1107656809914564608/operations/7388331316720173056
METHOD=
  google.cloud.aiplatform.v1beta1.ReasoningEngineService.CreateReasoningEngine
BUILD_ID=38f5f3cb-cbab-4a76-ab28-70dfa6dcdd89
BUILD_LOG_NAME=
  projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_build
REASONING_ENGINE_BUILD_LOG_COUNT=51

GCS_DOCKERFILE_OBJECT=
  gs://831270426395-1107656809914564608-1788162639127/Dockerfile.zip
GCS_SOURCE_OBJECT=
  gs://831270426395-1107656809914564608-1788162639127/source_archive.tar.gz

STEP_0_IMAGE=ubuntu:latest
STEP_0_IMAGE_DIGEST=
  sha256:2260313b31c8c011cd2eebe728008efac1b3982be73eb71348ea2648d2c0e09b
APPLICATION_CONTAINER_IMAGE_ID=NOT_PRODUCED
```

The create operation completed with `done=true` and the same Error code 3
message returned by Terraform. No Reasoning Engine resource remained after the
failed create (`VERTEX_REASONING_ENGINES_RETURNED=0` in Attempt 003 terminal
proof). GCS object download for the ephemeral builder bucket was denied to the
diagnostic principal (`storage.objects.get/list` 403); identifiers above come
from Cloud Logging text and the operation name.

## 5. Exact build-step sequence (cloud logs)

Chronological excerpts from
`aiplatform.googleapis.com/reasoning_engine_build` for `BUILD_ID` above:

```text
starting build "38f5f3cb-cbab-4a76-ab28-70dfa6dcdd89"
FETCHSOURCE
Fetching storage object: .../Dockerfile.zip
Archive:  /tmp/source-archive.zip
  inflating: /workspace/Dockerfile
BUILD
Starting Step #0
Step #0: Pulling image: ubuntu
Step #0: Digest: sha256:2260313b31c8c011cd2eebe728008efac1b3982be73eb71348ea2648d2c0e09b
Finished Step #0
Starting Step #1
Step #1: Copying gs://.../source_archive.tar.gz to file://source_archive.tar.gz
Finished Step #1
Starting Step #2
Step #2: Already have image (with digest): ubuntu
Finished Step #2
Starting Step #3
Step #3: Already have image (with digest): gcr.io/cloud-builders/docker
Step #3: unable to prepare context: unable to evaluate symlinks in Dockerfile path: lstat /workspace/user_code/Dockerfile: no such file or directory
Finished Step #3
ERROR
ERROR: build step 3 "gcr.io/cloud-builders/docker" failed: step exited with non-zero status: 1
```

```text
SOURCE_EXTRACT=PASS
REQUIREMENTS_INSTALL=NOT_REACHED
ENTRYPOINT_IMPORT=NOT_REACHED
APP_CONSTRUCTION=NOT_REACHED

FIRST_FAILURE_STEP=Step #3 docker build
EXACT_BUILD_ERROR=
  unable to prepare context: unable to evaluate symlinks in Dockerfile path: lstat /workspace/user_code/Dockerfile: no such file or directory
  ERROR: build step 3 "gcr.io/cloud-builders/docker" failed: step exited with non-zero status: 1
```

Unlike Attempt 002, Step #2 completed without `gzip`/`tar` rejection. The
TAR_GZIP package repair therefore cleared the prior unpack failure. The build
never reached `pip`, `requirements.txt` installation, Python import, or ADK
application construction. Searches of the 51 Reasoning Engine build payloads
for `pip`, `requirements`, `ModuleNotFoundError`, and `import` return no
dependency or import failures.

## 6. Deployment-spec / package contract comparison

Authoritative Terraform (`infra/agent-runtime/service.tf`) binds:

```hcl
source_code_spec {
  inline_source {
    source_archive = var.agent_source_archive_b64
  }
  image_spec {}
}
```

```text
AGENT_FRAMEWORK=google-adk
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=YES
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=NO
```

`image_spec` selects the Dockerfile-in-source / BYOC image build path. Platform
docs describe `ImageSpec` as building from the Dockerfile in the source
directory. After extraction the builder therefore expects
`/workspace/user_code/Dockerfile`.

Current deployment requirements (unchanged in this diagnosis):

```text
google-adk==1.18.0
jsonschema==4.23.0
PyYAML==6.0.2
```

Exact Attempt 003 package inventory (SHA-256
`1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752`):

```text
SOURCE_PACKAGE_FORMAT=TAR_GZIP
IS_GZIP=YES
IS_TAR_GZIP=YES
FILE_COUNT=54
HAS_REQUIREMENTS_TXT=YES
HAS_APP_AGENT=YES
HAS_DOCKERFILE=NO
TOP_LEVEL_PREFIXES=
  SOURCE_MANIFEST.sha256
  app
  contracts
  fixtures
  requirements.txt
  src
```

```text
DEPENDENCY_CONTRACT_MATCHES_REMOTE_FIRST_FAILURE=NO
REQUIREMENTS_TXT_BLAMED_BY_PROVIDER_MESSAGE=YES
REQUIREMENTS_TXT_SUPPORTED_BY_BUILD_LOG=NO
```

## 7. Clean local environment corroboration (off-repo, non-mutating)

Off-repository temporary Python 3.12 venv. Exact TAR_GZIP candidate extracted
to a `user_code/` directory. No GHL calls. No CRM calls. No cloud writes.
Requirements file not edited.

Structural reproduction of the remote first failure:

```text
tar -xzf <candidate.tar.gz> -C user_code/
USER_CODE_DOCKERFILE=NO
LOCAL_STRUCTURAL_ERROR=
  lstat .../user_code/Dockerfile: no such file or directory
REMOTE_DOCKERFILE_PATH_FAILURE_REPRODUCED_LOCALLY=YES
```

Dependency/import path (not indicated by remote logs; run as negative
corroboration only):

```text
pip install -r requirements.txt
PIP_INSTALL=PASS
python -c "import app.agent; print(type(app.agent.root_agent)); print(type(app.agent.app))"
IMPORT_APP_AGENT=PASS
ROOT_AGENT_TYPE=google.adk.agents.sequential_agent.SequentialAgent
APP_TYPE=google.adk.apps.app.App
```

```text
REMOTE_FAILURE_REPRODUCED_LOCALLY=YES
REMOTE_FAILURE_REPRO_CLASS=MISSING_USER_CODE_DOCKERFILE
REMOTE_DEP_OR_IMPORT_FAILURE_REPRODUCED_LOCALLY=NO
LOCAL_REQUIREMENTS_INSTALL_PASS=YES
LOCAL_ENTRYPOINT_IMPORT_PASS=YES
```

The remote first failure is therefore not a missing runtime dependency, ADK
version install failure, or `app.agent` import failure under the current
requirements contract.

## 8. Classification

```text
ROOT_CAUSE_CLASS=PACKAGE_LAYOUT
EXACT_BUILD_ERROR=
  unable to prepare context: unable to evaluate symlinks in Dockerfile path: lstat /workspace/user_code/Dockerfile: no such file or directory
  ERROR: build step 3 "gcr.io/cloud-builders/docker" failed: step exited with non-zero status: 1
EVIDENCE_SOURCE=
  cloud log
  operation metadata
  apply log
  terraform source_code_spec
  local package extract
REPAIR_REQUIRED=YES

NOT_DEPENDENCY_INSTALL=YES
NOT_MISSING_RUNTIME_DEPENDENCY=YES
NOT_ADK_VERSION_COMPATIBILITY=YES
NOT_ENTRYPOINT_IMPORT=YES
NOT_APPLICATION_CONSTRUCTION=YES
NOT_PLATFORM_TRANSIENT=YES
NOT_UNKNOWN=YES
```

Primary class is `PACKAGE_LAYOUT` because the builder reached post-extract
Docker image construction and failed on a missing
`/workspace/user_code/Dockerfile`, while the submitted archive contains no
`Dockerfile`. That expectation is created by the authoritative Terraform
`image_spec {}` binding (Dockerfile-in-source path) together with an ADK
source package that only carries `app/`, `src/`, contracts/fixtures, and
`requirements.txt`.

Dependency-oriented classes from the diagnosis brief are excluded by the build
log and by local `pip install -r requirements.txt` plus `import app.agent`
success. `PLATFORM` transient is not selected: Step #0/#1/#2 succeeded, the
failure is deterministic for this package+spec pair, and the missing path is
exactly what `image_spec` requires in the source directory.

The generic Terraform/provider text blaming `requirements.txt` is not supported
by the Reasoning Engine build log.

## 9. Zero-effect ledger for this diagnosis unit

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
AUTHORIZATION_004_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
RESOURCES_CREATED=0
RESOURCES_DESTROYED=0
PACKAGE_DEPENDENCIES_CHANGED=NO
RETRY_AUTHORIZED=NO
```

## 10. STOP / NEXT

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_BUILD_FAILURE_DIAGNOSED_002
ATTEMPT_003_RETRY_AUTHORIZED=NO
AUTHORIZATION_003_REUSABLE=NO
ACTIVATION_003_REUSABLE=NO

REPAIR_REQUIRED=YES
NEXT=BOUNDED_BUILD_REPAIR_002
```

A future bounded repair must make the deployment package/spec pair consistent
for Agent Runtime image construction—either by supplying the Dockerfile
required by `image_spec`, or by replacing `image_spec {}` with an approved
`python_spec` entrypoint binding for `google-adk`—under a new independently
reviewed authorization. It must not reuse Attempt 003 authority, must not edit
`requirements.txt` until a dependency failure is separately proven, must not
create Authorization 004 in this diagnosis unit, and must not apply Terraform
under this proof.
