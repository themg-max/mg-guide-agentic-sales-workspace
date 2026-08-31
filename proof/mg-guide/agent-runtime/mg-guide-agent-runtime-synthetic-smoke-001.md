# MG Guide Agent Runtime — Synthetic Smoke 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_SYNTHETIC_SMOKE_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-synthetic-smoke-001.md
CLASSIFICATION=SYNTHETIC_ONLY_AGENT_RUNTIME_SMOKE_AND_EVAL_PROOF
PR_CLASS=execution_proof
MODE=SYNTHETIC_ONLY_NO_DEPLOY_NO_GHL
OWNER=VS_CODE_MG_ORCHESTRATOR
SECURITY_OWNER=HUMAN_SECURITY_OPERATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T01:32:30Z

BRANCH_AT_AUTHORING=
  proof/mg-guide-agent-runtime-synthetic-smoke-001
BRANCH_IS_MAIN=NO
```

This unit executes synthetic-only Agent Runtime smoke and deterministic
evaluation under the repaired `mg-guide-agent-runtime` ADC identity. It does
**not** deploy Agent Runtime, call HighLevel, mutate CRM, grant IAM, or publish
credentials.

```text
INITIAL_MODE=SYNTHETIC_ONLY
LIVE_GHL_ADAPTER_ENABLED=NO
CRM_MUTATION_AUTHORIZED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
```

## 1. Authority and gate chain

```text
PR_376_MERGE_SHA=
  3c146c66a99cc262e4677fef6b0b3806b49eca13
PR_376_PRESENT_ON_ORIGIN_MAIN=YES

IDENTITY_REPAIR=
  docs/architecture/mg-guide-agent-runtime-identity-selection-repair-001.md
SECURITY_ATTESTATION=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-gemini-key-security-attestation-001.md

EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=YES
SECURITY_GATE_SATISFIED=YES
AGENT_RUNTIME_IAM_READY=YES
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
BOTH_GATES_PASS_BEFORE_SMOKE=YES
```

## 2. Runtime identity

```text
INTENDED_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_PRINCIPAL_MATCH=YES
OBSERVED_LOCAL_ADC_PRINCIPAL_EQUALS_INTENDED=YES
ADC_CREDENTIAL_TYPE=impersonated_service_account
GOOGLE_APPLICATION_CREDENTIALS=UNSET
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=ai-rolodex-to-crm
GOOGLE_CLOUD_LOCATION=global
MODEL_LOCATION=global
MODEL=gemini-3.7-flash
GEMINI_API_KEY_IN_PROCESS_ENV=NO
GOOGLE_API_KEY_IN_PROCESS_ENV=NO
```

## 3. Architecture freezes honored

```text
REUSE_EXISTING_AGENT_GRAPH=YES
REUSE_EXISTING_DELEGATES=YES
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO

AGENT_RUNTIME_SURFACE=
  mg-guide-orchestrator/app (agents-cli Agent Runtime target)
EXISTING_PHASE3_ADK_GRAPH=
  src/agents/follow_up_planning (SequentialAgent + deterministic delegates)
NESTED_SECOND_ADK_RUNNER_STARTED=NO
```

This smoke exercises the Agent Runtime surface (`mg-guide-orchestrator`) under
the approved principal. The Phase 3 SequentialAgent graph remains the durable
business-graph reuse target behind the shared root factory and was not replaced
by a nested second runner. Scaffold tools (`get_weather`, `get_current_time`)
are synthetic fixtures used for routing proof only.

## 4. Root agent smoke

```text
COMMAND_CLASS=agents-cli.run
PROMPT_CLASS=SYNTHETIC_GREETING
LIVE_GHL=NO
ROOT_SMOKE_EXIT=0
ROOT_NONEMPTY_RESPONSE=YES
ROOT_AGENT_NAME_OBSERVED=root_agent
VERTEX_MODEL_INVOCATION=PASS
ROOT_AGENT_SMOKE=PASS
```

Observed behavior: local ADK server booted, `root_agent` returned a non-empty
assistant response, server stopped. No provider 403 / permission denial.

## 5. Delegate / tool routing smoke

```text
COMMAND_CLASS=agents-cli.run
PROMPT_CLASS=SYNTHETIC_WEATHER_TOOL_ROUTE
TOOL_SMOKE_EXIT=0
TOOL_CALL_OBSERVED=get_weather
TOOL_RESPONSE_FIXTURE_HIT=YES
TOOL_FIXTURE_PHRASE_CLASS=SYNTHETIC_SF_WEATHER_60_FOGGY
DELEGATE_ROUTING=PASS
```

Routing proof: the root agent issued `get_weather` with a San Francisco query
and consumed the synthetic fixture response ("60 degrees and foggy") in the
final user-visible answer. This is fixture/tool routing, not live CRM or GHL.

## 6. Deterministic evaluation hard gates

```text
COMMAND_CLASS=agents-cli.eval.run
DATASET=tests/eval/datasets/basic-dataset.json
EVAL_CONFIG=tests/eval/eval_config.yaml
EVAL_RUN_EXIT=0
CASES_TOTAL=3
CASES_GENERATED=3
CASES_VALID=3
CASES_ERROR=0
GENERATE_AUTH_FAILURES=0
```

Primary metric result (`custom_response_quality`):

```text
NUM_CASES_TOTAL=3
NUM_CASES_VALID=3
NUM_CASES_ERROR=0
MEAN_SCORE=5.0
STDEV_SCORE=0.0
PER_CASE_SCORES=5.0,5.0,5.0
```

Hard-gate evaluation (fail-closed checklist):

```text
HARD_GATE_ALL_CASES_GENERATED=PASS
HARD_GATE_ZERO_CASE_ERRORS=PASS
HARD_GATE_ZERO_AUTH_FAILURES=PASS
HARD_GATE_ROOT_AGENT_RESPONDED=PASS
HARD_GATE_TOOL_ROUTING_OBSERVED_IN_SMOKE=PASS
HARD_GATE_RUNTIME_PRINCIPAL_MATCH=PASS
HARD_GATE_NO_GHL_CALLS=PASS
HARD_GATE_NO_CRM_MUTATIONS=PASS
DETERMINISTIC_EVALUATION_HARD_GATES=PASS
```

```text
LLM_AS_JUDGE=SECONDARY_QUALITY_SIGNAL_ONLY
LLM_AS_JUDGE_METRIC=custom_response_quality
LLM_AS_JUDGE_MEAN_SCORE=5.0
LLM_AS_JUDGE_USED_AS_HARD_GATE_SOLE_CRITERION=NO
```

The LLM-as-judge score is recorded as a secondary quality signal only. Hard
gates above are structural/operational and passed independently.

## 7. Effect ledger

```text
VERTEX_MODEL_INVOCATION=PASS
ROOT_AGENT_SMOKE=PASS
DELEGATE_ROUTING=PASS
DETERMINISTIC_EVALUATION_HARD_GATES=PASS

GHL_CALLS=0
CRM_MUTATIONS=0
CRM_READS=0
HIGHLEVEL_HOST_CONTACTED=NO
NETWORK_PROVIDER_GHL=0

IAM_MUTATIONS=0
SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
AGENT_RUNTIME_DEPLOYMENTS=0
```

## 8. Deployment hold

```text
DEPLOYMENT_EXECUTED=NO
AGENTS_CLI_DEPLOY_INVOKED=NO

DEFAULT_APP_SERVICE_ACCOUNT_SCAFFOLD=
  mg-guide-orchestrator-app
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
DEPLOYMENT_IDENTITY_CONFIGURATION_REPAIR_REQUIRED=YES
CREATE_SECOND_RUNTIME_IDENTITY=FORBIDDEN
```

Before any deployment authorization, deployment configuration must be repaired
to **reuse** the existing approved runtime SA. Do not create a second runtime
identity from the scaffold default.

## 9. Disclosure boundary

```text
ACCESS_TOKENS_PUBLISHED=NO
REFRESH_TOKENS_PUBLISHED=NO
API_KEYS_PUBLISHED=NO
FULL_EVAL_TRACE_BODIES_COMMITTED=NO
GRADE_HTML_COMMITTED=NO
SMOKE_STDOUT_COMMITTED=NO
```

Local workstation smoke/eval outputs were kept off-repo under a temp directory
and are not committed. Only the public pass/fail ledger is recorded here.

## 10. Return board

```text
SECURITY_GATE_SATISFIED=YES
RUNTIME_PRINCIPAL_MATCH=YES
VERTEX_MODEL_INVOCATION=PASS
ROOT_AGENT_SMOKE=PASS
DELEGATE_ROUTING=PASS
DETERMINISTIC_EVALUATION_HARD_GATES=PASS
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 11. Next / stop

```text
ALL_SYNTHETIC_GATES_PASS=YES
NEXT=
  DEPLOYMENT_IDENTITY_CONFIGURATION_REPAIR
THEN=
  SEPARATE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION

STOP=
  MG_GUIDE_AGENT_RUNTIME_SYNTHETIC_SMOKE_001_COMPLETE
```
