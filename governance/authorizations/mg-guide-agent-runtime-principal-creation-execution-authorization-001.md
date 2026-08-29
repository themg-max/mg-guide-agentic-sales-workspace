# MG Guide Agent Runtime Principal Creation Execution Authorization 001

## 1. Authorization identity and current state

```text
AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_EXECUTION_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/mg-guide-agent-runtime-principal-creation-execution-authorization-001.md
CLASSIFICATION=IAM_EXECUTION_AUTHORIZATION
PR_CLASS=AUTHORIZATION
MODE=PROPOSED_EXECUTION_AUTHORIZATION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS=
  PROPOSED_PENDING_INDEPENDENT_REVIEW_AND_HUMAN_EXECUTION_AUTHORITY
AUTHORIZATION_EFFECTIVE=NO
IAM_MUTATION_AUTHORIZED_NOW=NO
SELF_ACTIVATION=FORBIDDEN
DO_NOT_MUTATE_IAM_IN_THIS_UNIT=YES
```

This artifact defines maximum future IAM mutation bounds. It does not observe
current IAM state, create a service account, add a binding, create a key, or
activate mutation authority. A later human execution authority must bind a
fresh read-only preflight after this artifact is independently reviewed and
merged.

## 2. Durable authority chain

```text
PRINCIPAL_AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_AUTHORIZATION_001
AUTHORIZATION_MERGE_SHA=
  3cdf2b1b9fc604a3f8c9c0b0fcc2eca4aa17cccc
AUTHORIZATION_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

COUNTERSIGNATURE_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_COUNTERSIGNATURE_001
COUNTERSIGNATURE_MERGE_SHA=
  dfcf8fa69677d2ca51fb3dba8cfd62a21f92de2c
COUNTERSIGNATURE_BLOB_SHA=
  9339f78d1374ae614aedbacb3f433eb0aebf45cd
COUNTERSIGNATURE_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES
COUNTERSIGNATURE_BLOB_SHA_MATCH=YES
```

Any durable-chain mismatch fails closed and authorizes no mutation.

## 3. Exact principal and maximum future bounds

```text
PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

MAX_SERVICE_ACCOUNT_CREATES=1
MAX_IAM_BINDINGS=1
MAX_SERVICE_ACCOUNT_KEYS=0

PROPOSED_ROLE=roles/aiplatform.user
PROPOSED_MEMBER=
  serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROPOSED_BINDING_SCOPE=PROJECT_ai-rolodex-to-crm
LEAST_PRIVILEGE_REVIEW_REQUIRED=YES
```

The maxima are ceilings, not required mutation counts. An already-satisfied
exact state must not be recreated or rebound.

```text
AUTOMATIC_RETRY=NO
AUTOMATIC_COMPENSATING_MUTATION=NO
ALTERNATE_PROJECT_ALLOWED=NO
ALTERNATE_SERVICE_ACCOUNT_ALLOWED=NO
ALTERNATE_MEMBER_ALLOWED=NO
ALTERNATE_ROLE_ALLOWED=NO
ADDITIONAL_BINDING_ALLOWED=NO
```

## 4. Fresh read-only IAM preflight

Before any later human authority may activate mutation, the execution consumer
must perform a fresh, read-only observation of the exact project, service
account, and relevant project IAM policy.

```text
FRESH_READ_ONLY_IAM_PREFLIGHT_REQUIRED=YES

SERVICE_ACCOUNT_EXISTS=OBSERVED_NOT_ASSUMED
CURRENT_PRINCIPAL_BINDINGS=OBSERVED_NOT_ASSUMED
SERVICE_ACCOUNT_METADATA=OBSERVED_NOT_ASSUMED
PROPOSED_EXACT_BINDING_STATE=OBSERVED_NOT_ASSUMED

IAM_PREFLIGHT_EXECUTED_IN_THIS_UNIT=NO
IAM_STATE_INVENTED_BY_THIS_ARTIFACT=NO
```

The preflight must classify the service-account state:

```text
SERVICE_ACCOUNT_STATE_1=
  ABSENT_AND_EXACT_CREATION_PLAN_CONFLICT_FREE
SERVICE_ACCOUNT_STATE_1_ACTION=
  ELIGIBLE_FOR_AT_MOST_ONE_CREATE_AFTER_HUMAN_ACTIVATION

SERVICE_ACCOUNT_STATE_2=
  EXACT_SERVICE_ACCOUNT_ALREADY_PRESENT_AND_METADATA_ACCEPTABLE
SERVICE_ACCOUNT_STATE_2_ACTION=
  CREATE_ALREADY_SATISFIED_ZERO_CREATE_ATTEMPTS

SERVICE_ACCOUNT_STATE_3=
  PRESENT_WITH_CONFLICTING_METADATA_OR_AMBIGUOUS_OBSERVATION
SERVICE_ACCOUNT_STATE_3_ACTION=FAIL_CLOSED_NO_MUTATION_RETURN_FOR_REVIEW
```

After an exact account exists or a separately authorized create has verified
readback, the preflight must classify the proposed binding:

```text
BINDING_STATE_1=EXACT_MEMBER_ROLE_SCOPE_BINDING_PRESENT
BINDING_STATE_1_ACTION=BINDING_ALREADY_SATISFIED_ZERO_BIND_ATTEMPTS

BINDING_STATE_2=
  EXACT_BINDING_ABSENT_AND_NO_CONFLICTING_OR_AMBIGUOUS_STATE
BINDING_STATE_2_ACTION=
  ELIGIBLE_FOR_AT_MOST_ONE_BIND_AFTER_HUMAN_ACTIVATION

BINDING_STATE_3=CONFLICTING_OR_AMBIGUOUS_IAM_STATE
BINDING_STATE_3_ACTION=FAIL_CLOSED_NO_MUTATION_RETURN_FOR_REVIEW
```

```text
IF_OBSERVED_STATE_CONFLICTS_WITH_PROPOSED_PLAN=
  FAIL_CLOSED
  NO_MUTATION
  RETURN_FOR_REVIEW
```

## 5. Least-privilege and non-authority boundaries

Independent review must confirm that `roles/aiplatform.user` is the narrowest
suitable role for the stated synthetic Agent Runtime and Vertex inference
purpose. A narrower role may be substituted only through explicit review of an
updated artifact. A broader role is not authorized.

```text
GHL_ACCESS=NO
CRM_AUTHORITY=NO
SECRET_ACCESS=NO
PRODUCTION_AUTHORITY=NO
DEPLOYMENT_AUTHORITY=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
SERVICE_ACCOUNT_IMPERSONATION_AUTHORIZED=NO
```

No key, secret grant, HighLevel grant, CRM authority, production workload,
deployment, extra role, or extra project binding is authorized.

## 6. Later activation, verification, and consumption

No IAM mutation may occur until this exact artifact is independently reviewed
and merged and a later human execution authority binds the fresh observed
preflight and least-privilege decision.

```text
INDEPENDENT_REVIEW_REQUIRED=YES
EXECUTION_AUTHORIZATION_MERGE_REQUIRED=YES
HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
FRESH_PREFLIGHT_BOUND_TO_HUMAN_AUTHORITY_REQUIRED=YES
LEAST_PRIVILEGE_DECISION_BOUND_TO_HUMAN_AUTHORITY_REQUIRED=YES

EXECUTION_AUTHORIZATION_REUSABLE=NO
EXECUTION_AUTHORIZATION_TRANSFERABLE=NO
EXECUTION_AUTHORIZATION_CONSUMED_AT_AUTHORING=NO
```

Any separately authorized mutation must verify exact readback before proceeding
to the next possible mutation. Failure or ambiguity stops without retry or
automatic compensation.

```text
SERVICE_ACCOUNT_CREATE_READBACK_REQUIRED=YES
IAM_BINDING_READBACK_REQUIRED=YES
FAILED_OR_AMBIGUOUS_MUTATION_RETRY_ALLOWED=NO
AUTOMATIC_ROLLBACK_MUTATION_AUTHORIZED=NO
RETURN_FOR_REVIEW_ON_FAILURE_OR_AMBIGUITY=YES
```

## 7. Unit attestations

```text
LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_CREATES=0
IAM_BINDINGS_ADDED=0
SERVICE_ACCOUNT_KEYS_CREATED=0

NO_HIGHLEVEL_CALL=YES
NO_IAM_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOYMENT=YES
NO_SECRET_MUTATION=YES
NO_PIT_ROTATION=YES
NO_GHL_SCOPE_EDIT=YES
```
