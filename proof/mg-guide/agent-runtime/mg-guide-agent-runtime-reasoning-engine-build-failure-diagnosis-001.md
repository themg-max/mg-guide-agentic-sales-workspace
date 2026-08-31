# MG Guide Agent Runtime Reasoning Engine Build Failure Diagnosis 001

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_BUILD_FAILURE_DIAGNOSIS_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-reasoning-engine-build-failure-diagnosis-001.md
PR_CLASS=BOUNDED_PROOF
MODE=READ_ONLY_BUILD_FAILURE_DIAGNOSIS
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PR_387_MERGE_SHA=
  36722e1a592f183d328f851f1a07844cee94191b
PR_387_ROLE=
  ATTEMPT_002_TERMINAL_DEPLOYMENT_RESULT_BASELINE
PR_387_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

AUTHORIZED_ATTEMPT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_ATTEMPT_002
RUN_ID=
  mg-guide-agent-runtime-deploy-002-20260831T052416Z-44b98374
```

This proof records a read-only diagnosis of the terminal Attempt 002 Reasoning
Engine build failure. It does not authorize another deployment, retry apply,
mutate IAM, secrets, or service accounts, change package dependencies, or
perform any cloud write.

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
PACKAGE_DEPENDENCIES_CHANGED=NO
DEPLOYMENT_EXECUTED=NO
```

## 2. Attempt 002 remains terminal and non-reusable

```text
ATTEMPT_002_RESULT=
  FAILED_REASONING_ENGINE_BUILD
ATTEMPT_002_TERMINAL=YES
ATTEMPT_002_AUTHORITY_CONSUMED=YES
ATTEMPT_002_APPLY_ATTEMPTS=1
ATTEMPT_002_RETRY_AUTHORIZED=NO
AUTHORIZATION_002_REUSABLE=NO
ACTIVATION_002_REUSABLE=NO
AGENT_RUNTIME_RESOURCES_CREATED=0

AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_002
AUTHORIZATION_PR=385
AUTHORIZATION_MERGE_SHA=
  47c81e25f78812e12daa8db00e68d8c9b5a0e440

ACTIVATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_002
ACTIVATION_PR=386
ACTIVATION_MERGE_SHA=
  006b7acbdcde802c6f4e39eba932e2a4e04fe729

FAILURE_WINDOW_START_UTC=2026-08-31T05:37:14Z
FAILURE_WINDOW_END_UTC=2026-08-31T05:39:19Z
APPLY_LOG_SHA256=
  fe56fdf063abf608758dc3aa2814149544af2fdef00f72e48f7628c336c5a389
```

## 3. Local apply-log evidence

The complete local apply log matching `APPLY_LOG_SHA256` contains no operation
name, Reasoning Engine ID, build ID, or application container/image ID. The
provider error is only:

```text
Error waiting to create ReasoningEngine: Error waiting for Creating
ReasoningEngine: Error code 3, message: Build failed. The issue might be
caused by incorrect code, requirements.txt file or other dependencies.
```

```text
APPLY_LOG_CONTAINS_OPERATION_NAME=NO
APPLY_LOG_CONTAINS_REASONING_ENGINE_ID=NO
APPLY_LOG_CONTAINS_BUILD_ID=NO
APPLY_LOG_CONTAINS_CONTAINER_IMAGE_ID=NO
PROVIDER_ERROR_CODE=3
PROVIDER_ERROR_CLASS=REASONING_ENGINE_BUILD_FAILED
```

The provider message is generic and is not by itself a proven root cause.
Cloud Logging and the create-operation metadata supply the exact build failure.

## 4. Identifiers recovered from Cloud Logging and operation metadata

Read-only sources:

```text
gcloud logging read
  resource.type="aiplatform.googleapis.com/ReasoningEngine"
  timestamp 2026-08-31T05:37:14Z through 2026-08-31T05:39:19Z
  project=ai-rolodex-to-crm

gcloud ai operations describe 1002825179434319872
  --project=ai-rolodex-to-crm
  --region=us-east1
```

```text
PROJECT=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
REGION=us-east1
REASONING_ENGINE_ID=2963139856391208960
OPERATION_NAME=
  projects/831270426395/locations/us-east1/reasoningEngines/2963139856391208960/operations/1002825179434319872
METHOD=
  google.cloud.aiplatform.v1beta1.ReasoningEngineService.CreateReasoningEngine
BUILD_ID=f519c93d-306d-4d34-85b1-6d149c8ad625
BUILD_LOG_NAME=
  projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_build
REASONING_ENGINE_BUILD_LOG_COUNT=33

GCS_DOCKERFILE_OBJECT=
  gs://831270426395-2963139856391208960-1788154637740/Dockerfile.zip
GCS_SOURCE_OBJECT=
  gs://831270426395-2963139856391208960-1788154637740/source_archive.tar.gz

STEP_0_IMAGE=ubuntu:latest
STEP_0_IMAGE_DIGEST=
  sha256:2260313b31c8c011cd2eebe728008efac1b3982be73eb71348ea2648d2c0e09b
APPLICATION_CONTAINER_IMAGE_ID=NOT_PRODUCED
```

The create operation completed with `done=true` and the same Error code 3
message returned by Terraform. No Reasoning Engine resource remained after
the failed create (Attempt 002 already recorded
`VERTEX_REASONING_ENGINES_RETURNED=0`).

## 5. Exact build-step sequence (cloud logs)

Chronological excerpts from
`aiplatform.googleapis.com/reasoning_engine_build` for `BUILD_ID` above:

```text
starting build "f519c93d-306d-4d34-85b1-6d149c8ad625"
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
Step #2: gzip: stdin has more than one entry--rest ignored
Step #2: tar: This does not look like a tar archive
Step #2: tar: Skipping to next header
Step #2: tar: Child returned status 2
Step #2: tar: Error is not recoverable: exiting now
Finished Step #2
ERROR
ERROR: build step 2 "ubuntu" failed: step exited with non-zero status: 2
```

The 33 Reasoning Engine log payloads were searched for `pip`,
`requirements`, `ModuleNotFoundError`, `import`, `serialization`,
`entrypoint`, `permission`, `denied`, `403`, and `401`. None appear.

The build never reached dependency installation, Python import, agent
entrypoint loading, or pickle/serialization. It failed while unpacking
`source_archive.tar.gz` in Step #2.

## 6. Local source-package corroboration (off-repo, non-mutating)

The Attempt 002 source package used at apply time remains the frozen ZIP:

```text
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
SOURCE_PACKAGE_SIZE_BYTES=343228
SOURCE_PACKAGE_FILE_COUNT=54
MAGIC_HEX=504b0304
IS_ZIP=YES
IS_GZIP=NO
ZIP_COMPRESS_TYPES=STORED(0)
HAS_REQUIREMENTS_TXT=YES
HAS_APP_AGENT=YES
```

`gzip -t` on that ZIP reports `not in gzip format`. The bytes are a PKZIP
archive, not a gzip-compressed tar. The Vertex builder named and unpacked
the uploaded object as `source_archive.tar.gz` using `gzip`/`tar` on
`ubuntu`, which failed with the Step #2 errors above.

This diagnosis does not change the package, rebuild it, or alter
`requirements.txt`.

## 7. Classification

```text
ROOT_CAUSE_CLASS=PACKAGE_LAYOUT
EXACT_BUILD_ERROR=
  gzip: stdin has more than one entry--rest ignored
  tar: This does not look like a tar archive
  tar: Skipping to next header
  tar: Child returned status 2
  tar: Error is not recoverable: exiting now
  ERROR: build step 2 "ubuntu" failed: step exited with non-zero status: 2
EVIDENCE_SOURCE=
  cloud log
  operation metadata
  apply log
REPAIR_REQUIRED=YES

NOT_DEPENDENCY=YES
NOT_ENTRYPOINT=YES
NOT_SERIALIZATION=YES
NOT_PERMISSION=YES
NOT_UNKNOWN=YES
```

Primary class is `PACKAGE_LAYOUT` because the builder consumed a file named
`source_archive.tar.gz` and `tar`/`gzip` rejected it before any later build
step. The submitted Agent Runtime source is a ZIP (`PK\x03\x04`), not a gzip
tar. The generic provider text blaming `requirements.txt` is not supported by
the build log.

`PLATFORM_PROVISIONING` is not selected: the copy of
`source_archive.tar.gz` succeeded, Ubuntu image pull succeeded, and the
failure is the unpack of the source object. `PERMISSION` is not selected:
`aiplatform.reasoningEngines.create` was granted and GCS copy of the source
object succeeded.

## 8. Zero-effect ledger for this diagnosis unit

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
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

## 9. STOP / NEXT

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_BUILD_FAILURE_DIAGNOSED
ATTEMPT_002_RETRY_AUTHORIZED=NO
AUTHORIZATION_002_REUSABLE=NO
ACTIVATION_002_REUSABLE=NO

NEXT=BOUNDED_BUILD_REPAIR_PR
```

A future bounded repair may change source archive layout/format so the
Reasoning Engine builder can unpack it as `source_archive.tar.gz`. It must
not reuse Attempt 002 authority, must not change dependencies until that
repair is separately reviewed, and must not apply Terraform under this
proof.
