# MG Guide Agent Runtime Principal Creation Countersignature 001

## 1. Countersignature identity

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_COUNTERSIGNATURE_001
ARTIFACT_PATH=
  governance/authorizations/mg-guide-agent-runtime-principal-creation-countersignature-001.md
CLASSIFICATION=COUNTERSIGNATURE
PR_CLASS=AUTHORIZATION
MODE=EXPLICIT_HUMAN_COUNTERSIGNATURE_RECORD
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_AUTHORIZATION_001
AUTHORIZATION_ARTIFACT=
  governance/authorizations/mg-guide-agent-runtime-principal-creation-authorization-001.md
AUTHORIZATION_PR=292
AUTHORIZATION_MERGE_SHA=
  3cdf2b1b9fc604a3f8c9c0b0fcc2eca4aa17cccc
AUTHORIZATION_ARTIFACT_BLOB_SHA=
  62d9e26ddba0957d8e28f7aed8fa80e6d3a75211

AUTHORIZATION_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES
AUTHORIZATION_MERGE_SHA_MATCH=YES
AUTHORIZATION_ARTIFACT_BLOB_MATCH=YES
```

## 2. Human decision and selected principal

The human governance owner explicitly countersigns the exact merged
authorization and selected principal below. This records approval to prepare a
separate IAM execution authorization. It does not create the principal or
mutate IAM.

```text
COUNTERSIGNATURE_SOURCE=EXPLICIT_USER_HUMAN_ACT
HUMAN_COUNTERSIGNATURE_PRESENT=YES
HUMAN_FINALIZED_INPUTS_SUPPLIED_TO_THIS_UNIT=YES
HUMAN_FINALIZED_INPUTS_INVENTED=NO
HUMAN_APPROVER_NAMED_IDENTITY_SUPPLIED=NO
USER_STATED_COUNTERSIGNATURE_AT_LOCAL=2026-08-29T09:16:00.627-04:00

SELECTED_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SELECTED_PROJECT=ai-rolodex-to-crm
SELECTED_SERVICE_ACCOUNT_ID=mg-guide-agent-runtime

AUTHORIZATION_COUNTERSIGNED=YES
IAM_MUTATION_AUTHORIZED_NOW=NO
IAM_EXECUTION_AUTHORIZED_BY_COUNTERSIGNATURE_ALONE=NO
SEPARATE_IAM_EXECUTION_AUTHORIZATION_REQUIRED=YES
COUNTERSIGNATURE_MERGE_REQUIRED_BEFORE_EXECUTION_AUTHORIZATION_AUTHORING=YES
SELF_ACTIVATION=FORBIDDEN
```

## 3. Frozen future IAM execution-authorization bounds

After this countersignature is reviewed and merged, a separate execution
authorization may propose only:

```text
PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

MAX_SERVICE_ACCOUNT_CREATES=1
MAX_IAM_BINDINGS=1
MAX_SERVICE_ACCOUNT_KEYS=0

PROPOSED_ROLE=roles/aiplatform.user
LEAST_PRIVILEGE_REVIEW_REQUIRED=YES
```

The future IAM execution authorization must independently review whether
`roles/aiplatform.user` is the narrowest suitable role. Review may narrow or
reject the role, but may not silently broaden it or add bindings.

```text
GHL_ACCESS=NO
CRM_AUTHORITY=NO
SECRET_ACCESS=NO
PRODUCTION_AUTHORITY=NO
DEPLOYMENT_AUTHORITY=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
```

This countersignature does not assert that the service account is absent or that
creation is required. The separate execution lane must perform a fresh
read-only preflight and fail closed if actual state conflicts with its frozen
mutation plan.

```text
FRESH_IAM_PREFLIGHT_REQUIRED=YES
SERVICE_ACCOUNT_CREATE_EXECUTED_IN_THIS_UNIT=NO
IAM_BINDING_EXECUTED_IN_THIS_UNIT=NO
IAM_EXECUTION_AUTHORIZATION_CREATED_IN_THIS_UNIT=NO
```

## 4. Execution eligibility rule

No IAM mutation may occur unless the separate execution authorization:

1. binds this exact merged countersignature;
2. is independently reviewed and merged;
3. is effective under its own explicit human authority;
4. confirms the fresh preflight and least-privilege decision; and
5. freezes verification, rollback, and one-shot consumption semantics.

```text
COUNTERSIGNATURE_MERGE_ALONE_AUTHORIZES_IAM_MUTATION=NO
EXECUTION_AUTHORIZATION_MERGE_ALONE_AUTHORIZES_IAM_MUTATION=NO
INDEPENDENT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
EXECUTION_AUTHORIZATION_REUSABLE=NO
```

## 5. Unit attestations

```text
LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0

NO_HIGHLEVEL_CALL_IN_THIS_UNIT=YES
NO_IAM_MUTATION_IN_THIS_UNIT=YES
NO_AGENT_RUNTIME_DEPLOYMENT=YES
NO_SECRET_MUTATION_IN_THIS_UNIT=YES

IAM_EXECUTION_AUTHORIZATION_ELIGIBLE_AFTER_THIS_PR_MERGES=YES
IAM_EXECUTION_AUTHORIZATION_ELIGIBLE_NOW=NO
```
