# MG Guide Agent Runtime Reasoning Engine Start Failure Diagnosis 003

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_START_FAILURE_DIAGNOSIS_003
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-reasoning-engine-start-failure-diagnosis-003.md
PR_CLASS=BOUNDED_PROOF
MODE=READ_ONLY_RUNTIME_START_FAILURE_DIAGNOSIS
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PR_398_MERGE_SHA=
  e7bf11b3083eefabac8877aadd3e690444f5eb87
PR_398_ROLE=
  ATTEMPT_004_TERMINAL_DEPLOYMENT_RESULT
PR_398_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

AUTHORIZED_ATTEMPT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_ATTEMPT_004
RUN_ID=
  mg-guide-agent-runtime-deploy-004-20260831T092005Z-7bbf0996
```

This proof records a read-only diagnosis of the terminal Attempt 004 Reasoning
Engine start failure. It does not authorize another deployment, retry apply,
create Authorization 005 or Human Activation 005, mutate IAM, secrets, or
service accounts, change package dependencies, add an `agent.py` shim, upgrade
`google-adk`, or perform any cloud write.

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
AUTHORIZATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GOOGLE_ADK_UPGRADED=NO
AGENT_PY_SHIM_ADDED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
PACKAGE_DEPENDENCIES_CHANGED=NO
DEPLOYMENT_EXECUTED=NO
```

## 2. Attempt 004 remains terminal and non-reusable

```text
ATTEMPT_004_RESULT=
  FAILED_REASONING_ENGINE_START
ATTEMPT_004_TERMINAL=YES
ATTEMPT_004_AUTHORITY_CONSUMED=YES
ATTEMPT_004_APPLY_ATTEMPTS=1
ATTEMPT_004_RETRY_AUTHORIZED=NO
AUTHORIZATION_004_REUSABLE=NO
ACTIVATION_004_REUSABLE=NO

REASONING_ENGINE_ID=7801553968559030272
APPLY_DISPATCHED_AT_UTC=2026-08-31T09:39:03Z
APPLY_COMPLETED_AT_UTC=2026-08-31T09:43:29Z
APPLY_LOG_SHA256=
  ba472ef530f2a9f17671778f2b9e057a86c53021458fd952ca83e18012f12202

PROJECT=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
REGION=us-east1
```

The Terraform apply log matching `APPLY_LOG_SHA256` reports only that the
Reasoning Engine failed to start and cannot serve traffic. That provider
message is not by itself a proven root cause. Cloud Logging supplies the first
runtime exception.

## 3. Read-only log retrieval

Queries (order=asc) for
`resource.labels.reasoning_engine_id="7801553968559030272"` between
`2026-08-31T09:38:30Z` and `2026-08-31T09:44:30Z`:

```text
logName=.../aiplatform.googleapis.com%2Freasoning_engine_build
logName=.../aiplatform.googleapis.com%2Freasoning_engine_stderr
logName=.../aiplatform.googleapis.com%2Freasoning_engine_stdout
```

Sanitized payloads were stored off-repository under
`/tmp/mg-guide-attempt-004-start-diag`. Raw Cloud Logging JSON is not committed.

```text
BUILD_LOG_COUNT=602
STDERR_LOG_COUNT=900
STDOUT_LOG_COUNT=18
BUILD_ID=341103b2-1705-4371-94da-c85f233591fc
APPLICATION_CONTAINER_IMAGE_DIGEST=
  sha256:fb64718e0331f13cb0940f186d91260699ac3b6a076b03b3df162560ec12202e
```

`STDERR_LOG_COUNT` is the retrieved page total (`200+200+500`). Additional
later worker-restart frames exist after the first exception; they repeat the
same class/message and do not change classification.

## 4. Build phase

Chronological build excerpts:

```text
starting build "341103b2-1705-4371-94da-c85f233591fc"
FETCHSOURCE
  inflating: /workspace/Dockerfile
Step #1: Copying .../source_archive.tar.gz
Finished Step #2
Step #3: Sending build context to Docker daemon
Step #3: FROM .../assembly-service-py312:prod
Step #3: Collecting google-adk==1.18.0 (from -r ./requirements.txt)
... pip install of requirements ...
latest: digest: sha256:fb64718e0331f13cb0940f186d91260699ac3b6a076b03b3df162560ec12202e
DONE
```

```text
BUILD_PHASE_RESULT=PASS
SOURCE_EXTRACT=PASS
REQUIREMENTS_INSTALL=PASS
IMAGE_PUSH=PASS
BUILD_ERROR=NO
```

Unlike Attempts 002/003, the builder unpacked TAR_GZIP, installed
`requirements.txt` including `google-adk==1.18.0`, and pushed an application
image. The start failure is post-build.

## 5. First runtime exception (stderr)

Stdout shows the platform entrypoint launching Uvicorn repeatedly after the
first crash:

```text
2026-08-31T09:41:52.652542Z
  Entrypoint: Launching main application with .venv/bin/python...
```

Uvicorn started:

```text
2026-08-31T09:41:53.496390Z
  INFO: Uvicorn running on http://0.0.0.0:8080
```

First exact exception (sanitized; no secrets):

```text
FIRST_RUNTIME_EXCEPTION_AT_UTC=2026-08-31T09:42:08.827777Z
FIRST_RUNTIME_EXCEPTION_CLASS=
  app.api.factory.utils.RegisteredOperationsValueError
FIRST_RUNTIME_EXCEPTION=
  Class SequentialAgent is missing all methods `query`, `async_query`,
  `stream_query`, `bidi_stream_query` and `async_stream_query`. Default
  registered operations requires the object to define at least one of
  these methods.
```

Control-plane wrapper immediately after:

```text
UserCodeControlPlaneError:
  Control plane operation failed due to user code: Class SequentialAgent
  is missing all methods `query`, `async_query`, `stream_query`,
  `bidi_stream_query` and `async_stream_query`. Default registered
  operations requires the object to define at least one of these methods.
```

Platform context (sanitized):

```text
Error when getting registered operations. Service terminating.
Please check .../agent-engine/develop/custom#custom-methods
fix the error in `register_operations()` and re-deploy the application.

File /code/app/api/factory/python_file_api_builder.py
  create_apis_from_object
  _get_registered_operations_or_raise
  _default_registered_operations
```

No `ModuleNotFoundError`, `ImportError`, `PermissionDenied`,
`resourcemanager.projects.get`, VPC/egress, or credentials failures appear in
the retrieved build/stderr/stdout set. `app.agent` import itself succeeded far
enough for the control plane to inspect class `SequentialAgent`.

## 6. Bound Attempt-004 entrypoint contract

Authoritative Terraform `python_spec` on the Attempt 004 apply:

```text
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=root_agent
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
GOOGLE_ADK_VERSION=1.18.0
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
```

Package module `app/agent.py` exports both:

```text
root_agent = build_unit3_root_agent()   # SequentialAgent
app = App(root_agent=root_agent, name="app")
```

The deployed object selected by `ENTRYPOINT_OBJECT=root_agent` is
`SequentialAgent`. Agent Runtime default registered operations require
`query` / `async_query` / `stream_query` / `bidi_stream_query` /
`async_stream_query`. `SequentialAgent` defines none of those methods. That
matches the first stderr exception exactly.

## 7. High-priority upstream correlation (not proof)

Public ADK issues remain correlation-only unless stderr matches:

```text
UPSTREAM_ISSUE=
  google/adk-python#4237
  Agent Engine start failures at google-adk 1.18.0+
UPSTREAM_PR=
  google/adk-python#4243
  deployment import defects involving app/ agent layouts
UPSTREAM_MATCH_TO_ATTEMPT_004_STDERR=
  CORRELATION_ONLY
GOOGLE_ADK_UPGRADE_AUTHORIZED=NO
AGENT_PY_SHIM_AUTHORIZED=NO
```

Attempt 004 stderr does not show a missing-module import of `app.agent` or a
generic 1.18.0 installer crash. It shows a successful import of a
`SequentialAgent` object that the control plane then rejects for missing query
operations. That is an entrypoint-object compatibility failure under the
current `python_spec`, not a proven need to upgrade `google-adk` or add a
top-level `agent.py` shim.

## 8. Classification

```text
ROOT_CAUSE_CLASS=ADK_ENTRYPOINT_IMPORT_COMPATIBILITY
EVIDENCE_SOURCE=
  reasoning_engine_build
  reasoning_engine_stderr
  reasoning_engine_stdout
  apply log
  python_spec entrypoint binding
  app/agent.py exports
REPAIR_REQUIRED=YES

NOT_ADK_RUNTIME_VERSION_COMPATIBILITY=YES
NOT_RUNTIME_DEPENDENCY=YES
NOT_RUNTIME_IDENTITY_IAM=YES
NOT_RUNTIME_NETWORK_POLICY=YES
NOT_RUNTIME_ENVIRONMENT_BINDING=YES
NOT_PLATFORM_RUNTIME=YES
NOT_UNKNOWN=YES
```

`ADK_ENTRYPOINT_IMPORT_COMPATIBILITY` is selected because the first exception
is the Agent Runtime control plane rejecting `Class SequentialAgent` as the
entrypoint object bound by `app.agent:root_agent`. Import of the module
occurred; the imported object type is incompatible with default registered
operations.

IAM/network classes are excluded: no `PermissionDenied` / `403` /
`resourcemanager.projects.get` / VPC/egress/credentials hits. Platform
transient is excluded: build `DONE`, image digest produced, then a
deterministic user-code control-plane error. A `google-adk` version bump is
not proven by this stderr.

## 9. Zero-effect ledger for this diagnosis unit

```text
TERRAFORM_APPLY=NO
AGENTS_CLI_DEPLOY=NO
AUTHORIZATION_005_CREATE=NO
HUMAN_ACTIVATION_005_CREATE=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
GOOGLE_ADK_UPGRADED=NO
AGENT_PY_SHIM_ADDED=NO
REQUIREMENTS_TXT_CHANGED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
RESOURCES_CREATED=0
RESOURCES_DESTROYED=0
RETRY_AUTHORIZED=NO
```

## 10. STOP / NEXT

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_REASONING_ENGINE_START_FAILURE_DIAGNOSED_003
ATTEMPT_004_RETRY_AUTHORIZED=NO
AUTHORIZATION_004_REUSABLE=NO
ACTIVATION_004_REUSABLE=NO

REPAIR_REQUIRED=YES
NEXT=BOUNDED_RUNTIME_START_REPAIR_003
```

A future bounded repair must make the Agent Runtime entrypoint object satisfy
default registered operations (for example by binding the already-exported
`App` object rather than `SequentialAgent` `root_agent`) under new
independently reviewed authority. It must not reuse Attempt 004 authority,
must not upgrade `google-adk` or add an `agent.py` shim unless a later proof
requires that exact change, and must not apply Terraform under this diagnosis.
