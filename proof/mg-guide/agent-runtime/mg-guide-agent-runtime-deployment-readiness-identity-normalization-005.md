# MG Guide Agent Runtime Deployment Readiness Identity Normalization 005

## 1. Identity and boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_READINESS_IDENTITY_NORMALIZATION_005
ARTIFACT_PATH=proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-identity-normalization-005.md
PR_CLASS=proof_only
MODE=PRE_AUTHORIZATION_IDENTITY_MODEL_NORMALIZATION
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
BASE_MAIN_SHA=a30350e6a14001191dad851bf5a96193b5efd8b4

DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AUTHORIZATION_005_CREATED=NO
HUMAN_ACTIVATION_005_CREATED=NO
IAM_MUTATION=NO
SERVICE_ACCOUNT_KEY_CREATED=NO
SECRET_MUTATION=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

This proof normalizes the identity predicate that blocked Deployment Readiness
Proof 005. It does not authorize or execute a deployment. It does not change
IAM, credentials, service accounts, Terraform, application code, or the Unit 3
agent graph.

## 2. Bound merged evidence

```text
PR_400_ROLE=VERTEX_SDK_ADKAPP_RUNTIME_START_REPAIR_003
PR_400_MERGED=YES
PR_401_ROLE=DEPLOYMENT_READINESS_PROOF_005_HISTORICAL_FAIL_CLOSED
PR_401_MERGED=YES
PR_402_ROLE=CLOUD_LOGGING_DIAGNOSIS_004
PR_402_MERGE_SHA=a30350e6a14001191dad851bf5a96193b5efd8b4
PR_402_MERGED=YES
```

PR #402 independently recovered the Attempt 004 Reasoning Engine logs and
confirmed the first causal exception was registered-operation discovery on a
raw `SequentialAgent`. The build completed successfully, the runtime reached
Uvicorn startup, and no independent IAM, credential, project/location,
dependency-installer, or VPC failure was identified in the retrieved failure
window.

```text
ATTEMPT_004_ROOT_CAUSE_CLASS=entrypoint_contract
PR399_DIAGNOSIS_CORROBORATED=YES
PR400_REPAIR_ADDRESSES_LOGGED_CAUSE=YES
INDEPENDENT_UNRESOLVED_RUNTIME_DEFECT_FROM_ATTEMPT_004_LOGS=NO
```

This evidence does not claim a future live start has succeeded.

## 3. Historical Readiness 005 blocker

Merged Deployment Readiness Proof 005 recorded all of the following as passing:

```text
MERGED_SERVING_CONTRACT=PASS
POST_MERGE_PACKAGE_DIGEST_MATCH=PASS
COLD_IMPORT_WITH_PROJECT_REGION_ENV=PASS
AGENT_RUNTIME_APP_CONSTRUCTION=PASS
ENTRYPOINT_OBJECT_TYPE=AdkApp
REGISTER_OPERATIONS_CALL=PASS
ASYNC_STREAM_QUERY_REGISTERED=YES
RESOURCE_LOCATION_POLICY=PASS
FRESH_TERRAFORM_PLAN=PASS
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
PLANNED_RUNTIME_SERVICE_ACCOUNT=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES
```

The proof failed closed only because local Application Default Credentials were
user credentials rather than an impersonated instance of the approved runtime
service account:

```text
ADC_CREDENTIAL_CLASS=google.oauth2.credentials.Credentials
ADC_IS_IMPERSONATED=NO
ADC_TARGET_PRINCIPAL=UNKNOWN
APPROVED_ADC_IDENTITY_CONFIRMED_IN_LOCAL_COLD_PROCESS=NO
```

The historical artifact must remain unchanged as an accurate record of the
predicate it evaluated at that time.

## 4. Google Cloud identity model

Current Google Cloud Reasoning Engine documentation defines
`ReasoningEngineSpec.service_account` as the service account that the Reasoning
Engine artifact runs as. When set, that service account is the workload
identity used by the deployed Reasoning Engine artifact.

Authoritative references:

- https://docs.cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform_v1.types.ReasoningEngineSpec
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/rest/v1beta1/ReasoningEngineSpec

Google Cloud ADC documentation separately describes Application Default
Credentials as an environment-sensitive credential discovery mechanism. A
local development workstation can use user ADC; production code running on a
Google Cloud resource uses the identity attached to that resource. Google
recommends attaching a service account to the production resource rather than
using a service-account key.

Authoritative references:

- https://docs.cloud.google.com/docs/authentication/application-default-credentials
- https://docs.cloud.google.com/docs/authentication/set-up-adc-attached-service-account
- https://docs.cloud.google.com/iam/docs/attach-service-accounts

Therefore the local operator/development ADC principal and the deployed
Reasoning Engine workload principal are separate identity concerns.

## 5. Normalized readiness predicate

The following predicate is retired for Attempt 005 readiness because it tests a
parity condition Google Cloud does not require for a Reasoning Engine whose
runtime service account is explicitly bound:

```text
RETIRED_PREDICATE=
  LOCAL_ADC_PRINCIPAL_EQUALS_APPROVED_RUNTIME_SERVICE_ACCOUNT
RETIRED_PREDICATE_REQUIRED=NO
```

The replacement readiness identity contract is:

```text
LOCAL_SDK_AUTHENTICATION_AVAILABLE=REQUIRED
LOCAL_ADC_PRINCIPAL_EQUALS_RUNTIME_SERVICE_ACCOUNT=NOT_REQUIRED

PLANNED_RUNTIME_SERVICE_ACCOUNT_EQUALS_APPROVED_SERVICE_ACCOUNT=REQUIRED
NO_SERVICE_ACCOUNT_KEY_CREATED=REQUIRED
NO_UNAUTHORIZED_IAM_CHANGE=REQUIRED
LOCAL_COLD_PACKAGE_CONSTRUCTION_PASS=REQUIRED
REGISTERED_OPERATIONS_DISCOVERY_PASS=REQUIRED
```

For the next live deployment, workload identity must be verified from the
created Reasoning Engine resource after deployment rather than inferred from
local workstation ADC:

```text
POST_DEPLOYMENT_RUNTIME_IDENTITY_VERIFICATION=REQUIRED
EXPECTED_EFFECTIVE_RUNTIME_IDENTITY=mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

## 6. What this proof establishes

```text
LOCAL_ADC_ROLE=LOCAL_SDK_AND_OPERATOR_AUTHENTICATION
RUNTIME_SERVICE_ACCOUNT_ROLE=DEPLOYED_REASONING_ENGINE_WORKLOAD_IDENTITY
LOCAL_ADC_RUNTIME_IDENTITY_PARITY_REQUIRED=NO

PR401_BLOCKING_PREDICATE_SEMANTICALLY_NORMALIZED=YES
IAM_REPAIR_REQUIRED=NO
SERVICE_ACCOUNT_KEY_REQUIRED=NO
APPLICATION_CODE_REPAIR_REQUIRED_FOR_ADC_PARITY=NO
TERRAFORM_IDENTITY_BINDING_CHANGE_REQUIRED=NO
```

No service-account impersonation is required merely to make local ADC look like
the runtime workload identity. If impersonation is independently needed for a
specific operator action, it must be justified and authorized separately; it
is not a Deployment Readiness 005 parity requirement.

## 7. Freshness boundary

This artifact normalizes the readiness predicate only. Because `main` advanced
after the historical Readiness Proof 005, this proof does not silently reuse an
old saved plan, package digest, or authorization decision as fresh execution
authority.

Before Authorization 005 can be authored, a new bounded non-mutating readiness
recheck must confirm the current merged baseline and produce fresh evidence for:

```text
CURRENT_MAIN_EXACT_SHA
PR_400_ANCESTRY
PR_402_ANCESTRY
CURRENT_SERVING_ENTRYPOINT=app.agent:agent_runtime_app
CURRENT_SERVING_OBJECT_TYPE=AdkApp
CURRENT_SOURCE_PACKAGE_DIGEST
COLD_PACKAGE_IMPORT
REGISTER_OPERATIONS_CALL
ASYNC_STREAM_QUERY_REGISTERED
RESOURCE_LOCATION_POLICY
FRESH_TERRAFORM_PLAN
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
PLANNED_RUNTIME_SERVICE_ACCOUNT_MATCH=YES
NO_IAM_OR_SECRET_MUTATION_IN_PLAN=YES
```

## 8. Readiness decision

```text
IDENTITY_MODEL_NORMALIZATION_005=PASS
ADC_PARITY_BLOCKER_CLOSED=YES

READINESS_FOR_AUTHORIZATION_005=NOT_YET_RECOMPUTED
AUTHORIZATION_005_CREATE=NO
DEPLOYMENT_ATTEMPT_005=NO

NEXT=FRESH_NORMALIZED_DEPLOYMENT_READINESS_PROOF_005
STOP=INDEPENDENT_REVIEW_AND_FRESH_READINESS_RECHECK_REQUIRED
```

The next unit is a fresh non-mutating readiness recheck under the normalized
identity predicate. Only if that unit passes exact-current-main package,
serving-contract, policy, Terraform-plan, and runtime-service-account gates may
a separate Deployment Authorization 005 be proposed.