# MG Guide Agent Runtime Deployment Authorization 001

## 1. Authorization identity and current boundary

```text
AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/mg-guide-agent-runtime-deployment-authorization-001.md
CLASSIFICATION=DEPLOYMENT_EXECUTION_AUTHORIZATION_DEFINITION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS_AT_AUTHORING=
  PROPOSED_PENDING_INDEPENDENT_REVIEW_THEN_FRESH_HUMAN_ACTIVATION_001
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
DO_NOT_APPLY_IN_THIS_UNIT=YES
DO_NOT_DEPLOY_IN_THIS_UNIT=YES
```

This artifact defines a bounded future authorization that may later permit at
most one exact Terraform apply of the authoritative MG Guide Agent Runtime root.
Creating, reviewing, or merging this artifact does not activate execution
authority, run `terraform apply`, run `agents-cli deploy`, create a service
account or key, mutate IAM, read or mutate a secret, call HighLevel, access or
mutate CRM, or perform any cloud deployment.

```text
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
ARTIFACT_MERGE_IS_EXECUTION_AUTHORITY=NO
SELF_ACTIVATION=FORBIDDEN
```

## 2. Required merged baselines

```text
PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
PR_379_ROLE=
  AUTHORITATIVE_TERRAFORM_ROOT_BASELINE
PR_379_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

PR_380_MERGE_SHA=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
PR_380_ROLE=
  CANDIDATE_SOURCE_PACKAGE_AND_EXACT_PLAN_BASELINE
PR_380_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

PR_381_MERGE_SHA=
  2ed86deb098cc65cd58fbc90a91c9321f93cc685
PR_381_ROLE=
  POST_MERGE_EQUIVALENCE_AND_EXTRACTION_VERIFICATION_BASELINE
PR_381_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES
```

All three merge SHAs must remain ancestors of `origin/main` before any future
activation or execution consumer may proceed. Absence of any baseline is a hard
stop.

## 3. Source package and verification binding

```text
SOURCE_BUILD_COMMIT=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
SOURCE_PACKAGE_SIZE_BYTES=343228
SOURCE_PACKAGE_FILE_COUNT=54

POST_MERGE_EQUIVALENCE_PROOF=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-candidate-post-merge-equivalence-proof-001.md
POST_MERGE_PACKAGE_MATCH=YES
POST_MERGE_REBUILD_BYTE_IDENTICAL=YES

PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS
GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

ROOT_AGENT_MODULE=app.agent
ROOT_AGENT_FACTORY=
  agents.follow_up_planning.runtime.build_unit3_root_agent
REUSE_EXISTING_AGENT_GRAPH=YES
REUSE_EXISTING_DELEGATES=YES
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO
```

The future execution consumer must rebuild or supply only the archive whose
SHA-256 equals the frozen digest above. Any digest mismatch is a hard stop:

```text
STOP_ON_DIGEST_MISMATCH=
  POST_MERGE_SOURCE_PACKAGE_DIGEST_MISMATCH
```

The archive bytes and base64 payload remain outside the repository. The
checked-in empty ZIP placeholder in
`infra/agent-runtime/environments/dev.tfvars` must not be replaced in-repo with
deployment bytes.

## 4. Exact deployment binding

```text
AUTHORITATIVE_TERRAFORM_ROOT=
  infra/agent-runtime
DEPLOYMENT_SOURCE_MODEL=
  CHECKED_IN_TERRAFORM
GENERATED_AGENTS_CLI_TERRAFORM_IS_AUTHORITY=NO
GENERATED_AGENTS_CLI_TERRAFORM_USE=
  REFERENCE_AND_BOOTSTRAP_ONLY

PROJECT=
  ai-rolodex-to-crm
REGION=
  us-east1

APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_REUSE_EXISTING=YES
TERRAFORM_OWNS_RUNTIME_SERVICE_ACCOUNT=NO
TERRAFORM_OWNS_RUNTIME_SA_KEYS=NO
TERRAFORM_OWNS_VERTEX_PROJECT_IAM=NO

EXPECTED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
EXPECTED_PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_ADD_COUNT=1
EXPECTED_CHANGE_COUNT=0
EXPECTED_DESTROY_COUNT=0
```

The future plan must show exactly one create of
`google_vertex_ai_reasoning_engine.mg_guide`, bind the approved runtime service
account email directly, and show no service-account, key, project IAM, Vertex
IAM, secret, or destroy effects.

## 5. Ceilings and hard prohibitions

```text
MAX_DEPLOYMENTS=1
MAX_TERRAFORM_APPLY_ATTEMPTS=1
MAX_AGENT_RUNTIME_RESOURCES_CREATED=1

NO_RETRY=YES
NO_SECOND_APPLY=YES
NO_FALLBACK_DEPLOYMENT=YES
NO_AGENTS_CLI_DEPLOY=YES
NO_ALTERNATE_TERRAFORM_ROOT=YES
NO_ALTERNATE_PROJECT=YES
NO_ALTERNATE_REGION=YES
NO_ALTERNATE_RUNTIME_SERVICE_ACCOUNT=YES
NO_ALTERNATE_SOURCE_PACKAGE=YES

RESOURCE_DESTROY_ALLOWED=NO
SERVICE_ACCOUNT_CREATE_ALLOWED=NO
SERVICE_ACCOUNT_KEY_CREATE_ALLOWED=NO
IAM_MUTATION_ALLOWED=NO
SECRET_MUTATION_ALLOWED=NO
SECRET_PAYLOAD_READ_ALLOWED=NO
GHL_CALL_ALLOWED=NO
CRM_MUTATION_ALLOWED=NO
CRM_WRITE_ALLOWED=NO
```

Any plan or apply effect outside the exact one-add reasoning-engine shape is a
hard stop:

```text
STOP_ON_UNEXPECTED_PLAN_EFFECT=
  UNEXPECTED_TERRAFORM_PLAN_EFFECT
```

## 6. Authority semantics

```text
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
```

Drafting, opening, reviewing, or merging this authorization does not authorize
deployment. No automation may treat presence of this file, its PR, or its merge
as execution authority.

## 7. Required future Human Activation 001

After independent review and merge of this exact authorization, a separate
artifact is required:

```text
NEXT_AFTER_THIS_AUTHORIZATION_MERGES=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_001
```

Human Activation 001 must separately bind:

```text
ACTIVATION_MUST_BIND=
  - this exact authorization artifact and its merge SHA
  - a fresh run ID
  - a fixed UTC execution window
  - one attempt only
  - consumption on the first apply attempt
  - explicit human execution authority
```

```text
ACTIVATION_001_REQUIRES_NEW_RUN_ID=YES
ACTIVATION_001_REQUIRES_FIXED_UTC_WINDOW=YES
ACTIVATION_001_REQUIRES_NEW_CONSUMPTION_RECORD=YES
ACTIVATION_001_MAY_REUSE_PRIOR_RUN_ID=NO
ACTIVATION_001_MAY_REUSE_PRIOR_WINDOW=NO
ACTIVATION_001_CONSUMES_ON_FIRST_APPLY_ATTEMPT=YES
ACTIVATION_001_SELF_ACTIVATION=FORBIDDEN
```

Activation without those bindings is invalid. Activation alone still does not
execute; explicit human execution authority remains required at apply time.

## 8. Future one-shot execution contract

Only after all of the following are true may a future consumer attempt apply:

1. this authorization is independently reviewed and merged;
2. Human Activation 001 is independently reviewed and merged;
3. a fresh consumption record exists and is unconsumed;
4. explicit human execution authority is present for the fixed window;
5. the three baseline merge SHAs remain ancestors of `origin/main`;
6. the supplied source archive SHA-256 equals the frozen digest;
7. a non-mutating plan reconfirms
   `1 to add, 0 to change, 0 to destroy` for only
   `google_vertex_ai_reasoning_engine.mg_guide`;
8. the plan binds
   `mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`;
9. the plan creates no SA, SA key, IAM binding, secret, or destroy effect.

Then the consumer may:

1. consume the one-shot authority before mutation;
2. run at most one `terraform apply` against `infra/agent-runtime`;
3. record the exact result;
4. stop without retry, second apply, fallback deploy, or compensating mutation.

```text
ALLOWED_FUTURE_COMMAND_CLASS=
  terraform apply
  against AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
  with ephemeral exact source archive input
  one attempt only

FORBIDDEN_FUTURE_COMMAND_CLASSES=
  agents-cli deploy
  second terraform apply
  retry after failure or partial success
  terraform destroy
  service account create
  service account key create
  project or Vertex IAM mutation
  secret mutation
  GHL call
  CRM mutation
```

```text
POST_APPLY_REQUIRED_IF_SUCCESS=
  AGENT_RUNTIME_RESOURCES_CREATED=1
  EXPECTED_RESOURCE_PRESENT=YES
  RUNTIME_SERVICE_ACCOUNT_MATCH=YES
  SERVICE_ACCOUNTS_CREATED=0
  SERVICE_ACCOUNT_KEYS_CREATED=0
  IAM_MUTATIONS=0
  SECRET_MUTATIONS=0
  GHL_CALLS=0
  CRM_MUTATIONS=0
  DESTROYS=0

NO_SECOND_APPLY=YES
NO_RETRY=YES
NO_COMPENSATING_MUTATION=YES
```

If the apply fails or the post-apply ledger is incomplete, authority remains
consumed and no retry is authorized by this artifact or its activation.

## 9. Current non-authority and zero-effect ledger

```text
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO

TERRAFORM_APPLY_ATTEMPTS=0
AGENT_RUNTIME_DEPLOYMENTS=0
AGENTS_CLI_DEPLOY_ATTEMPTS=0
RESOURCES_CREATED=0
RESOURCES_CHANGED=0
RESOURCES_DESTROYED=0

SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEYS_CREATED=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
GHL_CALLS=0
CRM_MUTATIONS=0
CRM_CALLS=0

LANE_B_WORK_EXECUTED_IN_THIS_UNIT=NO
FLEET_AND_GHL_AUTHORITY_JOINED=NO
```

## 10. STOP

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED

AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO

DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_RUN_AGENTS_CLI_DEPLOY=YES

NEXT=
  INDEPENDENT_REVIEW_AND_MERGE
  THEN_MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_001

STOP
```
