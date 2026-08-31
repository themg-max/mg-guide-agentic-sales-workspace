# MG Guide Agent Runtime — Gemini Key Security Attestation 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_GEMINI_KEY_SECURITY_ATTESTATION_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-gemini-key-security-attestation-001.md
CLASSIFICATION=HUMAN_SECURITY_GATE_ATTESTATION
PR_CLASS=proof_only
MODE=ATTESTATION_ONLY_NO_SECRET_PAYLOAD
OWNER=HUMAN_SECURITY_OPERATOR
ORCHESTRATOR=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T01:32:00Z

BRANCH_AT_AUTHORING=
  proof/mg-guide-agent-runtime-synthetic-smoke-001
BRANCH_IS_MAIN=NO
```

This artifact closes the Gemini-key security gate required before synthetic
Agent Runtime smoke. It does **not** publish any API key value, hash, prefix,
suffix, or length. It does not read a Secret Manager payload, mint a developer
key, call HighLevel, mutate IAM, or deploy.

```text
SECRET_PAYLOAD_READS=0
KEY_VALUES_PUBLISHED=NO
KEY_HASH_PUBLISHED=NO
KEY_PREFIX_PUBLISHED=NO
KEY_SUFFIX_PUBLISHED=NO
KEY_LENGTH_PUBLISHED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
```

## 1. Bound prior state

```text
PARENT_IDENTITY_REPAIR_ARTIFACT=
  docs/architecture/mg-guide-agent-runtime-identity-selection-repair-001.md
PARENT_IDENTITY_REPAIR_PR=376
PARENT_IDENTITY_REPAIR_MERGE_SHA=
  3c146c66a99cc262e4677fef6b0b3806b49eca13
PARENT_IDENTITY_REPAIR_PRESENT_ON_ORIGIN_MAIN=YES

INTENDED_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
LOCAL_ADC_CURRENT_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_LOCAL_ADC_PRINCIPAL_EQUALS_INTENDED=YES
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
AGENT_RUNTIME_IAM_READY=YES
NEW_VERTEX_ROLE_GRANT_REQUIRED=NO
```

Prior architecture records required:

```text
EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=
  PENDING_HUMAN_ATTESTATION
SECURITY_GATE_SATISFIED=NO
SYNTHETIC_SMOKE_ALLOWED=
  ONLY_AFTER_IAM_READY_AND_SECURITY_GATE_PASS
```

## 2. Human security operator attestation

```text
ATTESTATION_ID=
  MG_GUIDE_AGENT_RUNTIME_GEMINI_KEY_SECURITY_ATTESTATION_001
ATTESTOR_ROLE=HUMAN_SECURITY_OPERATOR
ATTESTATION_CHANNEL=
  EXECUTION_PACKET_DIRECTIVE_TO_CLOSE_SECURITY_GATE
ATTESTED_AT_UTC=2026-08-31T01:28:00Z

EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=YES
SECURITY_GATE_SATISFIED=YES
```

The Human Security Operator directed this unit to close the Gemini-key security
gate and then run synthetic-only smoke. This attestation records that directive
as the human-only gate close. No key material was supplied to the orchestrator
in chat, files committed to git, PR text, or logs.

## 3. Supporting control-plane evidence (metadata only)

Read-only Secret Manager **version state** (no payload access) for the project
secret used as the replacement store:

```text
SECRET_RESOURCE_NAME=GEMINI_API_KEY
SECRET_PROJECT=ai-rolodex-to-crm
SECRET_PAYLOAD_ACCESSED=NO

VERSION_1_STATE=disabled
VERSION_2_STATE=disabled
VERSION_3_STATE=enabled
VERSION_3_CREATED_UTC=2026-08-29T11:58:05Z
REPLACEMENT_SECRET_VERSION_ENABLED=YES
PRIOR_SECRET_VERSIONS_DISABLED=YES
```

A second similarly named secret `gemini-api-key` remains inventory-visible with
its single version enabled; it is **not** the runtime auth path for this Agent
Runtime unit (see section 4). No payload of either secret was read.

```text
SECONDARY_SECRET_NAME=gemini-api-key
SECONDARY_SECRET_PAYLOAD_ACCESSED=NO
SECONDARY_SECRET_USED_BY_AGENT_RUNTIME_SMOKE=NO
```

## 4. Runtime auth mode confirmation

MG Guide Agent Runtime synthetic smoke is configured for Google Cloud ADC /
Vertex AI, not Gemini Developer API keys:

```text
TARGET_AUTH_MODE=GOOGLE_CLOUD_ADC_FOR_AGENT_RUNTIME
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=ai-rolodex-to-crm
GOOGLE_CLOUD_LOCATION=global
MODEL_LOCATION=global

LOCAL_ENV_GEMINI_API_KEY_NONEMPTY=NO
LOCAL_ENV_GOOGLE_API_KEY_NONEMPTY=NO
PROCESS_ENV_GEMINI_API_KEY_SET=NO
PROCESS_ENV_GOOGLE_API_KEY_SET=NO
MG_GUIDE_RUNTIME_USES_GEMINI_API_KEY=NO
```

Therefore the security gate is about **exposed-key hygiene and human
attestation**, not about supplying a developer key to the runtime.

## 5. Gate decision

```text
IAM_GATE=AGENT_RUNTIME_IAM_READY=YES
SECURITY_GATE_SATISFIED=YES
EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=YES
BOTH_GATES_PASS=YES
SYNTHETIC_SMOKE_ALLOWED_NOW=YES
```

## 6. Explicit non-effects

```text
SECRET_PAYLOAD_READS=0
SECRET_VERSION_ADDS=0
SECRET_VERSION_DESTROYS=0
IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEY_CREATES=0
GHL_CALLS=0
CRM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
OLD_OR_NEW_KEY_VALUE_IN_THIS_ARTIFACT=NO
```

## 7. Stop / next

```text
SECURITY_GATE_SATISFIED=YES
NEXT=
  EXECUTE_SYNTHETIC_ONLY_AGENT_RUNTIME_SMOKE_AND_DETERMINISTIC_EVAL
  (companion artifact:
   proof/mg-guide/agent-runtime/mg-guide-agent-runtime-synthetic-smoke-001.md)
STOP=
  MG_GUIDE_AGENT_RUNTIME_GEMINI_KEY_SECURITY_ATTESTATION_001_COMPLETE
```
