# MG Guide Agent Runtime ADK Compatibility Repair Proof 006

## 1. Identity and boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_ADK_COMPATIBILITY_REPAIR_PROOF_006
ARTIFACT_PATH=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-adk-compatibility-repair-proof-006.md
PR_CLASS=repair_proof
MODE=DEPENDENCY_COMPATIBILITY_REPAIR_ONLY
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T14:25:00Z

AUTHORIZED_BRANCH=repair/mg-guide-agent-runtime-adk-compatibility-006
BRANCH_IS_MAIN=NO
BASE_MAIN_SHA=29a58a33205022c13ce45c49a2f191ddc8f330ff
ORIGIN_MAIN_MATCHES_EXPECTED=YES
WORKTREE_CLEAN_BEFORE_ARTIFACT=YES
```

This proof repairs the Attempt 005 dependency blocker only. It does not
retry Attempt 005, create Authorization 006, create Human Activation 006,
run `terraform apply`, deploy, mutate IAM or secrets, create service-account
keys, call GHL, or mutate CRM.

```text
ATTEMPT_006_AUTHORIZED=NO
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Bound diagnosis

```text
ATTEMPT_005_ENGINE_ID=6699297959760101376
ATTEMPT_005_RESULT=FAILED_REASONING_ENGINE_START
ATTEMPT_005_ROOT_CAUSE=ADK_RUNTIME_VERSION_COMPATIBILITY
FIRST_CAUSAL_EXCEPTION=TypeError: Runner.__init__() got an unexpected keyword argument 'auto_create_session'
CALLING_FRAME=vertexai.agent_engines.AdkApp.set_up()
PINNED_GOOGLE_ADK_AT_FAILURE=1.18.0
ATTEMPT_004_GAP_CLOSED=YES
DO_NOT_RETRY_ATTEMPT_005=YES
```

`vertexai.agent_engines.AdkApp.set_up()` constructs
`Runner(..., auto_create_session=True)`. The pinned `google-adk==1.18.0`
`Runner.__init__` does not expose `auto_create_session`, so the engine
failed to start during serving setup. The full serving lifecycle gate
(`AdkApp.set_up()`) was missing from prior cold gates; it is now part of
the repair evidence below and is required before any future readiness claim.

## 3. Repair scope

Single-line dependency pin change. No entrypoint, infrastructure,
governance, identity, or serving-contract change.

```text
FILES_CHANGED=1
CHANGED_PATH=deployment/agent-runtime/requirements.txt
CHANGE=google-adk==1.18.0 -> google-adk==1.23.0
APP_AGENT_MODIFIED=NO
INFRA_MODIFIED=NO
GOVERNANCE_MODIFIED=NO
ROOT_REQUIREMENTS_TXT_MODIFIED=NO

ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=agent_runtime_app
SERVING_OBJECT_TYPE=AdkApp
ROOT_AGENT_TYPE=SequentialAgent
SERVING_CONTRACT_PRESERVED=YES
```

## 4. Dependency gate

Fresh Python 3.12 environment, first candidate only (no automatic upgrade
to latest):

```text
CANDIDATE_TESTED_FIRST=google-adk==1.23.0
PIP_INSTALL=PASS
PIP_CHECK=PASS
SELECTED_GOOGLE_ADK_VERSION=1.23.0
GOOGLE_CLOUD_AIPLATFORM_VERSION=1.165.1
RUNNER_AUTO_CREATE_SESSION_PARAMETER_PRESENT=YES
FALLBACK_MATRIX_NEEDED=NO
```

## 5. Full serving lifecycle gate

Fresh cold import from the extracted rebuilt package (no pre-seeded
`vertexai.init()`; `GOOGLE_CLOUD_PROJECT`/`GOOGLE_CLOUD_REGION` env only):

```text
COLD_IMPORT_APP_AGENT=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
ENTRYPOINT_OBJECT_TYPE=AdkApp
REGISTER_OPERATIONS_CALL=PASS
ADKAPP_REGISTER_OPERATIONS=PASS
REGISTERED_OPERATION_COUNT=13
REGISTERED_OPERATION_COUNT_GT_ZERO=YES
ASYNC_STREAM_QUERY_REGISTERED=YES

ADKAPP_SET_UP_CALL=EXECUTED
ADKAPP_SET_UP=PASS
ADKAPP_SET_UP_EXCEPTION=NONE
ADKAPP_TEARDOWN=NOT_APPLICABLE_NO_TEARDOWN_SURFACE
```

`AdkApp.set_up()` now completes without exception; the exact Attempt 005
first-causal exception is eliminated.

## 6. Deterministic package rebuild

```text
BUILD_COMMAND=python3.12 scripts/build_agent_runtime_source.py --source-commit ecdd97ffcdeb0ebe9d73096471ebcb07ec70aa54 --output <ephemeral>/mg-guide-agent-runtime-source-006.tar.gz
SOURCE_BASE_COMMIT=ecdd97ffcdeb0ebe9d73096471ebcb07ec70aa54
SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SIZE_BYTES=67890
PACKAGE_SHA256=6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
SOURCE_PACKAGE_SHA256=6dbd7e381f5a9e65990aca30611108f889e3cab97d8e66d296c46b89f2382dcf
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

## 7. Canonical validation

Fresh Python 3.9 venv from the repository root `requirements.txt`:

```text
CANONICAL_VALIDATION=PASS
LOCAL_PHASE1_DETERMINISTIC=PASS
PYTEST=PASS
PYTEST_EXIT=0
GIT_DIFF_CHECK=PASS
```

## 8. Closure decision and stop

```text
ATTEMPT_005_ROOT_CAUSE_CLOSED=YES
ADKAPP_REGISTER_OPERATIONS=PASS
ADKAPP_SET_UP=PASS
ATTEMPT_006_AUTHORIZED=NO
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO

STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_READINESS_006
```

This proof closes the Attempt 005 blocker
`ADK_RUNTIME_VERSION_COMPATIBILITY`. It does not authorize, activate, or
deploy Attempt 006. Any future deployment readiness claim for the Agent
Runtime must re-run the full serving lifecycle gate of section 5, including
`AdkApp.set_up()`, inside a fresh readiness lane.
