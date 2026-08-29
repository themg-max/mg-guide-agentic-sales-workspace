# MG Guide Agent Runtime Principal Creation Authorization 001

## 1. Authorization identity and review state

```text
AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_AUTHORIZATION_001
CLASSIFICATION=AUTHORIZATION
PR_CLASS=AUTHORIZATION
MODE=AUTHORIZATION_DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PROJECT=ai-rolodex-to-crm
PR290_MERGE_SHA=
  be6066d80632ea84544ee31853d5ec326664369b
PR290_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW
MG_GUIDE_PRINCIPAL_AUTHORIZATION_READY_FOR_REVIEW=YES
AUTHORIZATION_EFFECTIVE=NO
IAM_MUTATION_AUTHORIZED_NOW=NO
SELF_ACTIVATION=FORBIDDEN
MERGE_ALONE_AUTHORIZES_IAM_MUTATION=NO
```

This artifact restores the dedicated MG Guide runtime-principal proposal on its
own review lane. Creating, reviewing, or merging it does not create a service
account, mutate IAM, mint credentials, invoke Vertex AI, deploy an Agent
Runtime, access a secret, call HighLevel, or read or mutate CRM.

```text
HUMAN_COUNTERSIGNATURE_REQUIRED=YES
SEPARATE_IAM_EXECUTION_AUTHORIZATION_REQUIRED=YES
ARTIFACT_MERGE_IS_EXECUTION_AUTHORITY=NO
```

## 2. Selected principal architecture

```text
SELECTED_OPTION=DEDICATED_MG_GUIDE_RUNTIME_SERVICE_ACCOUNT
DEDICATED_PRINCIPAL_REQUIRED=YES

PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide Agent Runtime

REUSE_BABY_BUMPS_RUNTIME_B=NO
PRINCIPAL_REUSE_ALLOWED=NO

PROPOSED_ROLE=roles/aiplatform.user
PURPOSE=MG_GUIDE_SYNTHETIC_AGENT_RUNTIME_VERTEX_INFERENCE
ROLE_SCOPE=PROJECT_ai-rolodex-to-crm
```

The principal is dedicated to synthetic MG Guide Agent Runtime and Vertex model
inference. It must not reuse Baby Bumps Runtime B or any HighLevel, CRM,
deployment, or general production principal. The proposed role remains subject
to independent human least-privilege review before a separate IAM execution
authorization can be issued.

## 3. Explicit non-authority

```text
SERVICE_ACCOUNT_CREATION_AUTHORIZED_NOW=NO
SERVICE_ACCOUNT_CREATED_IN_THIS_UNIT=NO
IAM_BINDING_AUTHORIZED_NOW=NO
IAM_MUTATION_AUTHORIZED_NOW=NO

SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
SERVICE_ACCOUNT_IMPERSONATION_AUTHORIZED=NO
LIVE_GHL_ACCESS=NO
GHL_SECRET_ACCESS=NO
CRM_AUTHORITY=NO
PRODUCTION_AUTHORITY=NO
AGENT_RUNTIME_DEPLOYMENT_AUTHORITY=NO
VERTEX_INFERENCE_EXECUTION_AUTHORIZED_NOW=NO
SECRET_ACCESS_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO

MAX_SERVICE_ACCOUNT_CREATES_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_IAM_POLICY_MUTATIONS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_SERVICE_ACCOUNT_KEYS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_AGENT_RUNTIME_DEPLOYMENTS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_VERTEX_INFERENCE_CALLS_AUTHORIZED_BY_THIS_ARTIFACT=0
```

No authority may be inferred for service-account creation or deletion, IAM
policy mutation, service-account keys, impersonation, token minting, Secret
Manager access, HighLevel access, CRM access, production workloads, Vertex
inference, or Agent Runtime deployment.

## 4. Required future IAM authorization chain

A future principal-creation unit must have both a durable human countersignature
and a separate IAM execution authorization. It must not treat merge of this
artifact as mutable authority.

```text
THIS_EXACT_ARTIFACT_HUMAN_REVIEWED=YES
THIS_EXACT_ARTIFACT_MERGED_TO_MAIN=YES
HUMAN_COUNTERSIGNATURE_DURABLE=YES
SEPARATE_IAM_EXECUTION_AUTHORIZATION_DURABLE=YES
```

The future IAM authorization must freeze:

- the exact service-account ID, email, display name, and project;
- the exact proposed role and project-level binding scope;
- the executing human or automation identity;
- one bounded service-account creation and one bounded IAM binding, if approved;
- preflight, verification, rollback, and consumption procedures; and
- confirmation that no service-account key is created.

Independent least-privilege review may narrow or reject
`roles/aiplatform.user`. It may not silently broaden the role or resource scope.

## 5. Post-IAM validation plan

Only after separately authorized principal creation and IAM binding may a later
validation lane use:

```text
ADC_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

REQUIRED_PERMISSION_PROOF=aiplatform.endpoints.predict=GRANTED
```

After that proof succeeds, separately authorized validation may proceed in this
order:

```text
1=agents-cli run smoke
2=agents-cli eval generate
3=deterministic eval
4=LLM quality eval secondary
```

This is a plan, not current execution authority. Deployment remains prohibited
until every gate passes and a later deployment authorization is independently
reviewed and effective.

```text
NO_DEPLOY_UNTIL_ALL_GATES_PASS=YES
POST_IAM_PERMISSION_PROOF_EXECUTED_IN_THIS_UNIT=NO
AGENTS_CLI_SMOKE_EXECUTED_IN_THIS_UNIT=NO
AGENTS_CLI_EVAL_GENERATE_EXECUTED_IN_THIS_UNIT=NO
DETERMINISTIC_EVAL_EXECUTED_IN_THIS_UNIT=NO
LLM_QUALITY_EVAL_EXECUTED_IN_THIS_UNIT=NO
```

## 6. HighLevel separation and unit attestations

```text
LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
SECRET_MUTATIONS=0
PIT_ROTATIONS=0
GHL_SCOPE_EDITS=0

NO_HIGHLEVEL_CALL=YES
NO_IAM_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOY=YES
NO_SECRET_MUTATION=YES
NO_PIT_ROTATION=YES
NO_GHL_SCOPE_EDIT=YES

MG_GUIDE_PRINCIPAL_AUTHORIZATION_READY_FOR_REVIEW=YES
```

This principal lane does not grant, consume, alter, or extend any HighLevel
authorization, PIT, OAuth scope, CRM authority, or private diagnostic execution
grant.
