# MG Guide Agent Runtime Cloud Logging Diagnosis 004

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_CLOUD_LOGGING_DIAGNOSIS_004
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-cloud-logging-diagnosis-004.md
PR_CLASS=BOUNDED_PROOF
MODE=READ_ONLY_CLOUD_LOGGING_DIAGNOSIS
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

ORIGIN_MAIN_SHA=
  d4e0d2923b91b7f8bec54dfd0da9fb068c13078c
PR_399_MERGE_SHA=
  8b467b399fd74b9feb3d1d936a7d5c872a18b31c
PR_400_MERGE_SHA=
  22c1238523f565a66625f6e572e6ab850bc07146
PR_401_MERGE_SHA=
  d4e0d2923b91b7f8bec54dfd0da9fb068c13078c
ALL_LISTED_MERGE_SHAS_ANCESTOR_OF_ORIGIN_MAIN=YES
```

Read-only Cloud Logging diagnosis of terminal Attempt 004. This unit does not
deploy, mutate Terraform, change IAM/secrets, create Authorization 005, or
perform GHL/CRM calls.

```text
READ_ONLY=YES
CODE_CHANGE=NO
TERRAFORM_CHANGE=NO
TERRAFORM_APPLY=NO
DEPLOYMENT=NO
IAM_CHANGE=NO
SERVICE_ACCOUNT_KEY=NO
SECRET_CHANGE=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Attempt 004 terminal baseline

```text
ATTEMPT_004_RESULT=FAILED_REASONING_ENGINE_START
ATTEMPT_004_APPLY_EXIT=1
ATTEMPT_004_ENGINE_ID=7801553968559030272
ATTEMPT_004_WINDOW=
  2026-08-31T09:39:03Z through 2026-08-31T09:43:29Z
PROJECT=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
REGION=us-east1
```

## 3. Query and log IDs returned

Specified filter (location=`us-east1`) against:

```text
resource.type="aiplatform.googleapis.com/ReasoningEngine"
resource.labels.location="us-east1"
resource.labels.reasoning_engine_id="7801553968559030272"
timestamp>="2026-08-31T09:38:30Z"
timestamp<="2026-08-31T09:44:30Z"
log_id reasoning_engine_build OR reasoning_engine_stderr OR reasoning_engine_stdout
```

```text
SPECIFIED_FILTER_BUILD_COUNT=0
SPECIFIED_FILTER_STDERR_COUNT=1000
SPECIFIED_FILTER_STDOUT_COUNT=18

LOG_IDS_RETURNED_BY_SPECIFIED_FILTER=
  projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_stderr
  projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_stdout
```

Build logs for this engine exist but carry `resource.labels.location=""`, so
the specified `location="us-east1"` clause excludes them. Supplemental
read-only query without the location predicate recovered the build stream.

```text
SUPPLEMENTAL_BUILD_LOG_ID=
  projects/ai-rolodex-to-crm/logs/aiplatform.googleapis.com%2Freasoning_engine_build
SUPPLEMENTAL_BUILD_LOG_COUNT=602
BUILD_RESOURCE_LABELS_LOCATION=
  (empty string)
BUILD_ID=341103b2-1705-4371-94da-c85f233591fc
```

Raw JSON remains off-repo under `/tmp/mg-guide-cloud-logging-diag-004`.

## 4. Chronology

```text
BUILD_FIRST_TS=2026-08-31T09:39:16.347624845Z
BUILD_LAST_TS=2026-08-31T09:41:17.465720086Z
BUILD_PHASE_RESULT=PASS
IMAGE_DIGEST=
  sha256:fb64718e0331f13cb0940f186d91260699ac3b6a076b03b3df162560ec12202e
BUILD_DONE=YES

STDOUT_FIRST_TS=2026-08-31T09:41:52.652542Z
STDERR_FIRST_TS=2026-08-31T09:41:53.496390Z
FIRST_RUNTIME_EXCEPTION_AT_UTC=2026-08-31T09:42:08.827777Z
APPLY_COMPLETED_AT_UTC=2026-08-31T09:43:29Z
```

Stdout (platform bootstrap, repeating after crash):

```text
2026-08-31T09:41:52.652542Z  Entrypoint: Starting up services...
2026-08-31T09:41:52.652566Z  ./startup_scripts directory not found, skipping...
2026-08-31T09:41:52.652570Z  Entrypoint: Launching main application with .venv/bin/python...
... repeated at ~15s intervals through 09:43:12Z ...
```

Preceding initialization (stderr):

```text
2026-08-31T09:41:53.496390Z
  [1] INFO: Uvicorn running on http://0.0.0.0:8080
2026-08-31T09:41:53.496436Z
  [1] INFO: Started parent process [1]
2026-08-31T09:42:06.165752Z
  vertexai.preview.rag deprecation warning (google.adk.dependencies.vertexai)
2026-08-31T09:42:08.825871Z
  telemetry enabled but proceeding without gRPC/httpx/google-genai
  instrumentation (optional packages not installed)
```

No AdkApp, `root_agent`, auth, project, or location error strings appear in
the retrieved payloads.

## 5. First causal exception and traceback

```text
FIRST_RUNTIME_EXCEPTION_AT_UTC=2026-08-31T09:42:08.827777Z
INSERT_ID=6a954c70000ca181886516eb
FIRST_RUNTIME_EXCEPTION_CLASS=
  app.api.factory.utils.RegisteredOperationsValueError
FIRST_RUNTIME_EXCEPTION=
  Class SequentialAgent is missing all methods `query`, `async_query`,
  `stream_query`, `bidi_stream_query` and `async_stream_query`. Default
  registered operations requires the object to define at least one of
  these methods.
```

Complete traceback from the first worker ERROR line (sanitized; no secrets):

```text
Error when getting registered operations. Service terminating.
Please check .../agent-engine/develop/custom#custom-methods,
fix the error in `register_operations()` and re-deploy the application.

Traceback (most recent call last):
  File "/code/app/api/factory/python_file_api_builder.py", line 1424,
    in create_apis_from_object
      registered_operations = _get_registered_operations_or_raise(obj)
  File "/code/app/api/factory/python_file_api_builder.py", line 1098,
    in _get_registered_operations_or_raise
      return _default_registered_operations(obj)
  File "/code/app/api/factory/python_file_api_builder.py", line 1030,
    in _default_registered_operations
      raise utils.RegisteredOperationsValueError(
app.api.factory.utils.RegisteredOperationsValueError:
  Class SequentialAgent is missing all methods `query`, `async_query`,
  `stream_query`, `bidi_stream_query` and `async_stream_query`.
```

Sibling workers then raise the same error and wrap it as
`UserCodeControlPlaneError`. Stdout shows the platform entrypoint relaunching
Uvicorn until the create operation reports the engine failed to start.

```text
AdkApp_MENTIONS_IN_LOGS=0
root_agent_MENTIONS_IN_LOGS=0
register_operations_MENTIONS=38
SequentialAgent_MENTIONS=94
ModuleNotFoundError=0
ImportError=0
PermissionDenied=0
403=0
GOOGLE_CLOUD_PROJECT=0
GOOGLE_CLOUD_LOCATION=0
credentials=0
VPC=0
```

`pydantic` hits are build-time pip metadata, not a runtime validation crash.
Telemetry “instrumentation not installed” warnings are non-fatal and precede
the SequentialAgent operations error; they are not the causal exception.

Final platform failure (Terraform apply log, already recorded in Attempt 004
terminal proof): Reasoning Engine
`projects/831270426395/locations/us-east1/reasoningEngines/7801553968559030272`
failed to start and cannot serve traffic.

## 6. Classification vs merged PRs #399 / #400

```text
ROOT_CAUSE_CLASS=entrypoint_contract

PR399_DIAGNOSIS_CORROBORATED=YES
PR399_CLASS=
  AGENT_RUNTIME_ENTRYPOINT_OBJECT_CONTRACT
PR399_FAILED_OBJECT=
  app.agent:root_agent  (SequentialAgent)

PR400_REPAIR_ADDRESSES_CAUSE=YES
PR400_WRAPPER=
  vertexai.agent_engines.AdkApp(agent=root_agent)
PR400_ENTRYPOINT_OBJECT=
  agent_runtime_app
PR400_PYTHON_SPEC_ON_ORIGIN_MAIN=YES

INDEPENDENT_UNRESOLVED_RUNTIME_DEFECT=NO
```

PR #399’s merged diagnosis is corroborated: the first Cloud Logging exception
is exactly `RegisteredOperationsValueError` on class `SequentialAgent` during
default registered-operation discovery. Build passed; import reached object
inspection; IAM/project/network/dependency installer failures are absent.

PR #400’s merged repair addresses that exact cause on current `origin/main`:

- keep `root_agent = build_unit3_root_agent()` (`SequentialAgent` graph);
- add `agent_runtime_app = agent_engines.AdkApp(agent=root_agent)`;
- bind Terraform `python_spec.entrypoint_object = "agent_runtime_app"`.

`AdkApp.register_operations()` supplies `async_stream_query` and related
operations that Attempt 004’s `SequentialAgent` entrypoint lacked. No second
independent runtime defect is present in these Attempt 004 logs.

This comparison is log-to-merged-code. It does not claim a future live start
has already succeeded; Authorization 005 remains withheld (PR #401). It does
claim the **logged** Attempt 004 exception is the entrypoint-object contract
that PR #400 changes.

## 7. Zero-effect ledger

```text
READ_ONLY=YES
CODE_CHANGE=NO
TERRAFORM_CHANGE=NO
TERRAFORM_APPLY=NO
DEPLOYMENT=NO
IAM_CHANGE=NO
SERVICE_ACCOUNT_KEY=NO
SECRET_CHANGE=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 8. STOP

```text
STOP=ADC_IDENTITY_MODEL_NORMALIZATION_005_NEXT
PR399_DIAGNOSIS_CORROBORATED=YES
PR400_REPAIR_ADDRESSES_CAUSE=YES
INDEPENDENT_UNRESOLVED_RUNTIME_DEFECT=NO
```

Next work after this diagnosis is not another Attempt-004-class runtime-start
repair. Independent review of ADC/identity-model normalization for a future
authorization remains outside this read-only unit.
