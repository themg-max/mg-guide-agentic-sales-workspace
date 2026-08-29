# MG Guide Agent Runtime Principal One-Create Execution Proof 001

## 1. Proof identity and authority

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_ONE_CREATE_EXECUTION_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-principal-one-create-execution-proof-001.md
ARTIFACT_KIND=SANITIZED_ONE_CREATE_EXECUTION_PROOF
PR_CLASS=execution_proof
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BRANCH=
  proof/mg-guide-agent-runtime-principal-one-create-execution-proof-001
BRANCH_IS_MAIN=NO

EXPLICIT_HUMAN_IAM_EXECUTION_ACT_AT_LOCAL=
  2026-08-29T11:06:40.602-04:00
EXPLICIT_HUMAN_IAM_EXECUTION_ACT_AT_UTC=
  2026-08-29T15:06:40.602Z

ACTIVATION_PR=299
ACTIVATION_REVIEWED_HEAD=
  d75c52558ae4e5dce06667cc637097e6028df940
ACTIVATION_MERGE_SHA=
  bf329c5444dd87e32a7bbb6c79d8fc9976ff6856
ACTIVATION_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES
ACTIVATION_BLOB_SHA=
  3231131f2c15b30a33f7c34a0dc99c843fee88ee

BOUND_READONLY_PREFLIGHT_BLOB_SHA=
  3de851dec3c37ef4a1f02fa5d1125abe9cb90d2f
PARENT_EXECUTION_AUTHORIZATION_BLOB_SHA=
  e6907469f841250df71fe4469c5d004eb7e88531
```

## 2. Exact authorized ceiling

```text
PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide Agent Runtime

MAX_SERVICE_ACCOUNT_CREATES=1
MAX_IAM_BINDINGS=0
MAX_SERVICE_ACCOUNT_KEYS=0
```

This lane has no HighLevel authority and does not inherit or consume the
HighLevel grant.

## 3. Fresh exact-account observation

The exact project was active. A fresh exact `describe` plus exact-email filtered
list classified the service account as already present, unique, and
metadata-acceptable.

```text
FRESH_READ_ONLY_OBSERVATION=PASS
PROJECT_ACTIVE=YES
SERVICE_ACCOUNT_EXISTS=YES
EXACT_FILTERED_LIST_COUNT=1

SERVICE_ACCOUNT_EMAIL_MATCH=YES
SERVICE_ACCOUNT_DISPLAY_NAME_MATCH=YES
SERVICE_ACCOUNT_DISABLED=NO
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=YES
CONFLICTING_OR_AMBIGUOUS_STATE=NO
```

No unrelated service-account identities, operator identity, project number, or
IAM policy content is published.

## 4. Already-satisfied terminal path

Per the merged activation, an acceptable pre-existing exact account must not be
recreated.

```text
SERVICE_ACCOUNT_CREATE_ATTEMPTS=0
SERVICE_ACCOUNT_CREATE_RESULT=ALREADY_SATISFIED
SERVICE_ACCOUNT_CREATES=0

ONE_CREATE_AUTHORITY_CONSUMED=NO_NOT_REQUIRED_ALREADY_SATISFIED
NO_RETRY=YES
NO_DELETE=YES
NO_RECREATE=YES
NO_COMPENSATING_MUTATION=YES
```

The lane stopped immediately after exact metadata classification.

```text
NEXT=FRESH_BINDING_STATE_RECLASSIFICATION
STOP=YES
```

## 5. Mutation and side-effect ledger

```text
IAM_MUTATIONS=0
IAM_BINDINGS_ADDED=0
IAM_BINDING_RECLASSIFICATION_PERFORMED=NO
SERVICE_ACCOUNT_KEYS_CREATED=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
ADC_CONFIGURATIONS=0

AGENT_RUNTIME_DEPLOYMENTS=0
ADK_SMOKE_RUNS=0
ADK_EVAL_RUNS=0

LIVE_GHL_CALLS=0
CRM_READS=0
CRM_WRITES=0
SECRET_ACCESSES=0
SECRET_MUTATIONS=0
```

## 6. Cross-lane isolation

```text
HIGHLEVEL_GRANT_AUTHORITY_USED=NO
AUTHORITY_TRANSFERRED_FROM_HIGHLEVEL_LANE=NO
AUTHORITY_TRANSFERRED_TO_HIGHLEVEL_LANE=NO
```

No role binding, key creation, impersonation, ADC configuration, deployment,
ADK execution, HighLevel call, CRM access, or secret access occurred.

## 7. Deterministic validation

```text
PHASE1_DETERMINISTIC_VERIFICATION_SCRIPT=PASS
FULL_PYTEST=PASS
GIT_DIFF_CHECK=PASS
```
