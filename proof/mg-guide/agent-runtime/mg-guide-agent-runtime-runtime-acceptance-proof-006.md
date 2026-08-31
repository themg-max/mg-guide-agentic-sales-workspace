# MG Guide Agent Runtime Runtime Acceptance Proof 006

This unit is RUNTIME ACCEPTANCE ONLY for the already-deployed Attempt 006
Reasoning Engine. It does not run `terraform apply`, retry deployment,
destroy, mutate IAM or secrets, call live GHL, or mutate CRM.

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_RUNTIME_ACCEPTANCE_PROOF_006
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md
PR_CLASS=execution_proof
MODE=RUNTIME_ACCEPTANCE_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T15:54:00Z

BRANCH=proof/mg-guide-agent-runtime-runtime-acceptance-006
BRANCH_IS_MAIN=NO
CURRENT_MAIN=027e8fcded119700ede2de4c35849894d1568e89
PR_414_MERGE_SHA=027e8fcded119700ede2de4c35849894d1568e89
```

## 1. Deployment binding

```text
ATTEMPT_006_TERMINAL=YES
ATTEMPT_006_AUTHORITY_CONSUMED=YES
ATTEMPT_006_AUTHORITY_REUSABLE=NO
DEPLOYMENT_RESULT=SUCCESS

REASONING_ENGINE_ID=5719342828341952512
REASONING_ENGINE_RESOURCE=
  projects/ai-rolodex-to-crm/locations/us-east1/reasoningEngines/5719342828341952512
EXPECTED_DISPLAY_NAME=mg-guide-orchestrator
EXPECTED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
EXPECTED_ENTRYPOINT_MODULE=app.agent
EXPECTED_ENTRYPOINT_OBJECT=agent_runtime_app
EXPECTED_SERVING_OBJECT=AdkApp
EXPECTED_ROOT_AGENT=SequentialAgent
```

## 2. Read-only resource verification

Fetched via:

```text
GET https://us-east1-aiplatform.googleapis.com/v1beta1/projects/ai-rolodex-to-crm/locations/us-east1/reasoningEngines/5719342828341952512
```

```text
RESOURCE_FETCH=PASS
RESOURCE_FETCH_RESULT=PASS
RESOURCE_EXISTS=YES
RESOURCE_HTTP=200

REGION_MATCH=YES
DISPLAY_NAME_MATCH=YES
SERVICE_ACCOUNT_MATCH=YES
AGENT_FRAMEWORK_MATCH=YES
ENTRYPOINT_MODULE_MATCH=YES
ENTRYPOINT_OBJECT_MATCH=YES
PYTHON_VERSION_MATCH=YES

OBSERVED_DISPLAY_NAME=mg-guide-orchestrator
OBSERVED_AGENT_FRAMEWORK=google-adk
OBSERVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_ENTRYPOINT_MODULE=app.agent
OBSERVED_ENTRYPOINT_OBJECT=agent_runtime_app
OBSERVED_PYTHON_VERSION=3.12
OBSERVED_REQUIREMENTS_FILE=requirements.txt
OBSERVED_CREATE_TIME=2026-08-31T15:34:51.484167Z
OBSERVED_UPDATE_TIME=2026-08-31T15:38:41.948052Z
```

No resource mutation.

## 3. Runtime acceptance boundary

The deployed graph is fixture-mode Unit 3:

```text
build_unit3_root_agent()
  meeting_agent=MeetingContextAgent.for_fixture_mode()
  relationship_agent=RelationshipContextAgent()  # SyntheticCrmStore + OfflineGhlReadAdapter
  follow_up_agent=FollowUpPlanningAgent()        # intent-only; no live GHL
```

`OfflineGhlReadAdapter` has no network I/O. `SyntheticCrmStore` never increments
`live_calls` or `writes`. Follow-up planning does not execute CRM mutation.

```text
LIVE_GHL_ADAPTER_ENABLED=NO
GHL_CALLS_ALLOWED=NO
CRM_MUTATIONS_ALLOWED=NO
PRIVATE_DATA_ALLOWED=NO
REQUEST_CLASS=SYNTHETIC_NO_WRITE
```

Request used a synthetic non-customer prompt only. No real transcript,
contact, opportunity, client, or CRM data was supplied.

## 4. Safe hosted invocation

Invoked the deployed AdkApp through the Vertex Reasoning Engine execution
client. Did not use `agents-cli deploy`. Did not mutate configuration.

```text
RUNTIME_OPERATION=stream_query
CLASS_METHOD=stream_query
REQUEST_CLASS=SYNTHETIC_NO_WRITE
USER_ID=runtime-acceptance-006-synthetic
MESSAGE=run the synthetic MG Guide follow-up graph

INVOCATION_STARTED_AT_UTC=2026-08-31T15:53:02Z
INVOCATION_COMPLETED_AT_UTC=2026-08-31T15:53:04Z
HTTP_OR_SDK_STATUS=OK
INVOCATION_RESULT=PASS
RESPONSE_RECEIVED=YES
EVENT_COUNT=3
RESPONSE_SHA256=
  bbf75a63e534e281a7c1d0bdff66a5bb9188fab7f7f5fba9607901c52d50a04a
```

Normalized non-sensitive event authors, in order:

```text
meeting_context_agent
relationship_context_agent
follow_up_planning_agent
```

Raw event payloads, credentials, and tokens were not committed.

## 5. Functional gates

```text
REASONING_ENGINE_REACHABLE=YES
ADKAPP_REQUEST_ACCEPTED=YES
SEQUENTIAL_AGENT_EXECUTED=YES
RESPONSE_RECEIVED=YES

GHL_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
DESTROYS=0
TERRAFORM_APPLY_EXECUTED=NO
```

## 6. Acceptance result

```text
FUNCTIONAL_RUNTIME_ACCEPTANCE=PASS
DEPLOYMENT_ACCEPTANCE=PASS
```

This proves the deployed AdkApp accepted a bounded synthetic no-write
request and returned a sequential three-agent response. It does not
authorize live GHL, CRM mutation, or a new deployment.

## 7. Canonical validation

```text
CANONICAL_VALIDATION=PASS
LOCAL_PHASE1_DETERMINISTIC=PASS
PYTEST=PASS
GIT_DIFF_CHECK=PASS
CI_STATUS=PENDING
```

## 8. Stop

```text
ATTEMPT_006_AUTHORITY_REUSABLE=NO
EXECUTION_AUTHORIZED_NOW=NO
RETRY_AUTHORIZED=NO

STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_DEPLOYMENT_COMPLETION_DECISION
```
