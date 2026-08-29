# MG Guide Agent Runtime Principal Creation Authorization 001

## 1. Identity and review state

```text
AUTHORIZATION_ID=MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_AUTHORIZATION_001
CLASSIFICATION=PLANNING_AND_AUTHORIZATION_ARTIFACT
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR
PROJECT=ai-rolodex-to-crm

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW
MG_GUIDE_PRINCIPAL_AUTHORIZATION_READY_FOR_REVIEW=YES
AUTHORIZATION_EFFECTIVE=NO
SELF_ACTIVATION=FORBIDDEN
IAM_MUTATION_AUTHORIZED_BY_ARTIFACT_MERGE=NO
SEPARATE_HUMAN_COUNTERSIGNATURE_REQUIRED=YES
SEPARATE_EXECUTION_AUTHORITY_REQUIRED=YES
```

This artifact records the bounded principal architecture for human review. Its
creation, review, or merge does not create a service account, mutate IAM, deploy
an Agent Runtime, access secrets, invoke Vertex AI, call HighLevel, or mutate
CRM. A separate human countersignature and a separate execution authority are
required before any control-plane mutation.

## 2. Selected principal architecture

```text
SELECTED_OPTION=DEDICATED_MG_GUIDE_RUNTIME_SERVICE_ACCOUNT
DEDICATED_PRINCIPAL_REQUIRED=YES

PROPOSED_SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
PROPOSED_SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROPOSED_DISPLAY_NAME=MG Guide Agent Runtime

PROPOSED_ROLE=roles/aiplatform.user
PURPOSE=AIPLATFORM_ENDPOINTS_PREDICT_AND_AGENT_RUNTIME_MODEL_INFERENCE
ROLE_USE_SCOPE=MG_GUIDE_SYNTHETIC_AGENT_RUNTIME_AND_VERTEX_INFERENCE_ONLY
```

The dedicated principal must not be reused as a HighLevel or general CRM
principal. The proposed role is subject to separate human review of least
privilege before any later execution authorization is issued.

## 3. Explicit non-authority

```text
SERVICE_ACCOUNT_CREATION_AUTHORIZED_NOW=NO
SERVICE_ACCOUNT_CREATED_IN_THIS_UNIT=NO
IAM_BINDING_AUTHORIZED_NOW=NO
IAM_MUTATIONS_IN_THIS_UNIT=0

LIVE_GHL_ACCESS=NO
CRM_AUTHORITY=NO
GHL_SECRET_ACCESS=NO
AGENT_RUNTIME_DEPLOYMENT_AUTHORITY=NO
VERTEX_INFERENCE_EXECUTION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
SERVICE_ACCOUNT_IMPERSONATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO

NO_HIGHLEVEL_CALL=YES
NO_IAM_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOY=YES
NO_SECRET_MUTATION=YES
```

No authority in this artifact may be inferred for:

- creating or deleting any service account or key;
- adding, removing, or changing an IAM policy binding;
- deploying, updating, or invoking an Agent Runtime;
- reading or mutating a Secret Manager resource;
- obtaining HighLevel credentials or calling any HighLevel endpoint; or
- reading or mutating CRM data.

## 4. Required future authorization chain

Any future principal creation or role binding must be performed in a separate
unit and must stop unless both of these durable approvals exist:

```text
HUMAN_COUNTERSIGNATURE_PRESENT=YES
SEPARATE_EXECUTION_AUTHORIZATION_PRESENT=YES
```

That future execution authorization must freeze the exact service-account
identity, project, role, IAM resource scope, mutation count, executing human or
automation identity, verification commands, rollback procedure, and
consumption record. It must independently revalidate least privilege and may
not treat merge of this artifact as mutation authority.

```text
MAX_SERVICE_ACCOUNT_CREATES_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_IAM_POLICY_MUTATIONS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_SERVICE_ACCOUNT_KEYS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_DEPLOYMENTS_AUTHORIZED_BY_THIS_ARTIFACT=0
MAX_VERTEX_INVOCATIONS_AUTHORIZED_BY_THIS_ARTIFACT=0
```

## 5. HighLevel separation and next unit

This principal planning unit neither grants nor consumes HighLevel authority.
It does not alter any PIT, OAuth scope, stage grant, secret, or CRM target.

```text
NO_GHL_CALLS=YES
NO_NEW_GHL_GRANT=YES
NO_STAGE_GRANT_003=YES
NO_PIT_ROTATION=YES
NO_SCOPE_EDIT=YES

NEXT_GHL_UNIT=OPPORTUNITY_READ_DIAGNOSTIC_AUTHORIZATION_001
NEXT_GHL_UNIT_DEPENDS_ON=REPAIRED_PR290_MERGED

FUTURE_METHOD=GET
FUTURE_PATH=/opportunities/{private_validation_opportunity_id}
FUTURE_MAX_READS=1
FUTURE_MAX_WRITES=0
FUTURE_NO_RETRY=YES
FUTURE_PRIVATE_DIAGNOSTIC_PERSISTENCE_REQUIRED=YES

FUTURE_OPERATION_AUTHORIZED_BY_THIS_ARTIFACT=NO
```

The named future operation is a planning pointer only. It requires its own
separately reviewed authorization after the repaired PR #290 is merged.

## 6. Review checklist

```text
PROJECT_BOUND=YES
DEDICATED_PRINCIPAL_BOUND=YES
PROPOSED_ROLE_BOUND=YES
INFERENCE_PURPOSE_BOUND=YES
LIVE_GHL_EXCLUDED=YES
CRM_AUTHORITY_EXCLUDED=YES
GHL_SECRET_ACCESS_EXCLUDED=YES
DEPLOYMENT_AUTHORITY_EXCLUDED=YES
MERGE_DOES_NOT_AUTHORIZE_IAM_MUTATION=YES
HUMAN_COUNTERSIGNATURE_REQUIRED=YES
SEPARATE_EXECUTION_AUTHORITY_REQUIRED=YES

MG_GUIDE_PRINCIPAL_AUTHORIZATION_READY_FOR_REVIEW=YES
```
