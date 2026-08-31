# MG Guide Agent Runtime Deployment Authorization 004

## 1. Authorization identity and current boundary

```text
AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_004
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_004
ARTIFACT_PATH=
  governance/authorizations/mg-guide-agent-runtime-deployment-authorization-004.md
CLASSIFICATION=DEPLOYMENT_EXECUTION_AUTHORIZATION_DEFINITION
PR_CLASS=authorization
MODE=DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS_AT_AUTHORING=
  PROPOSED_PENDING_INDEPENDENT_REVIEW_THEN_FRESH_HUMAN_ACTIVATION_004
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
DO_NOT_APPLY_IN_THIS_UNIT=YES
DO_NOT_DEPLOY_IN_THIS_UNIT=YES
HUMAN_ACTIVATION_004_CREATED_IN_THIS_UNIT=NO
```

This artifact defines a bounded future authorization that may later permit at
most one exact Terraform apply of the authoritative MG Guide Agent Runtime root
for Attempt 004 only. Creating, reviewing, or merging this artifact does not
activate execution authority, run `terraform apply`, run `agents-cli deploy`,
create Human Activation 004, create a service account or key, mutate IAM, read
or mutate a secret, call HighLevel, access or mutate CRM, or perform any cloud
deployment.

```text
HUMAN_ACTIVATION_REQUIRED=YES
EXPLICIT_HUMAN_EXECUTION_AUTHORITY_REQUIRED=YES
ARTIFACT_MERGE_IS_EXECUTION_AUTHORITY=NO
SELF_ACTIVATION=FORBIDDEN
```

## 2. Terminal prior attempts and non-reuse

```text
ATTEMPT_001_TERMINAL=YES
ATTEMPT_001_RESULT=
  FAILED_ORG_POLICY_GCP_RESOURCE_LOCATIONS
AUTHORIZATION_001_REUSABLE=NO
ACTIVATION_001_REUSABLE=NO

ATTEMPT_002_TERMINAL=YES
ATTEMPT_002_RESULT=
  FAILED_REASONING_ENGINE_BUILD_PACKAGE_LAYOUT
AUTHORIZATION_002_REUSABLE=NO
ACTIVATION_002_REUSABLE=NO

ATTEMPT_003_TERMINAL=YES
ATTEMPT_003_RESULT=
  FAILED_REASONING_ENGINE_BUILD
ATTEMPT_003_ROOT_CAUSE=
  IMAGE_SPEC_SELECTED_DOCKERFILE_PATH
ATTEMPT_003_EXACT_FAILURE=
  MISSING_/workspace/user_code/Dockerfile
AUTHORIZATION_003_REUSABLE=NO
ACTIVATION_003_REUSABLE=NO
```

Attempts 001–003 are terminal and non-reusable. Authorization 004 is fresh
one-shot authority only for a future Attempt 004, and only after a separate
Human Activation 004 is independently reviewed and merged.

## 3. Required merged baselines and readiness binding

```text
MAIN_BASELINE=
  912e8815c2531b0fd81b6940290d3d0596ae0c04

PR_392_MERGE_SHA=
  73a571cb00bb05b32abeb898ef5de1b6c5b67b19
PR_392_ROLE=
  PYTHON_SPEC_SOURCE_ENTRYPOINT_REPAIR
PR_392_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

PR_393_MERGE_SHA=
  04eef52413e9aa383bdf48930fec667b7015ef37
PR_393_ROLE=
  ATTEMPT_003_BUILD_FAILURE_DIAGNOSIS_002
PR_393_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

PR_394_MERGE_SHA=
  912e8815c2531b0fd81b6940290d3d0596ae0c04
PR_394_ROLE=
  ATTEMPT_003_TERMINAL_DEPLOYMENT_RESULT
PR_394_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

READINESS_PROOF=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-readiness-proof-004.md
ALL_REQUIRED_MERGE_SHAS_ON_ORIGIN_MAIN=YES
```

Absence of any listed baseline or readiness proof mismatch is a hard stop before
future activation or execution.

## 4. Merged PythonSpec contract and source package

```text
AUTHORITATIVE_TERRAFORM_ROOT=
  infra/agent-runtime
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO
ENTRYPOINT_MODULE=app.agent
ENTRYPOINT_OBJECT=root_agent
REQUIREMENTS_FILE=requirements.txt
PYTHON_VERSION=3.12
AGENT_FRAMEWORK=google-adk

SOURCE_PACKAGE_FORMAT=TAR_GZIP
SOURCE_PACKAGE_SHA256=
  1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752
SOURCE_PACKAGE_SIZE_BYTES=67778
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_SHA256_MATCH=YES
HAS_DOCKERFILE=NO
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS

CLEAN_VENV_PIP_INSTALL=PASS
ENTRYPOINT_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
APP_LOAD=PASS
GHL_CALLS=0
CRM_MUTATIONS=0
```

The future execution consumer must rebuild or supply only the archive whose
SHA-256 equals the frozen digest above. Any digest mismatch is a hard stop.

Archive bytes and base64 payload remain outside the repository. The checked-in
placeholder in `infra/agent-runtime/environments/dev.tfvars` must not be
replaced in-repo with deployment bytes.

## 5. Exact deployment binding and fresh plan gate

```text
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

EFFECTIVE_RESOURCE_LOCATION_POLICY_RECHECK=PASS
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
EFFECTIVE_POLICY_EVIDENCE_SHA256=
  9e62a83d2cb234fba19ea2a18b6218740a8728c0f13b34068e6fe50e55b4b947

AUTHORIZATION_004_PLAN_FILE_SHA256=
  a5c6d5e3e6383aeca6c34425d6bf0b007c01b90c93eb2c4502c0e03e6bad196f
FRESH_PLAN_SUMMARY_MATCH=YES
EXPECTED_RESOURCE_ONLY=YES
PLANNED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES
SOURCE_CODE_SPEC_USES_PYTHON_SPEC=YES
SOURCE_CODE_SPEC_USES_IMAGE_SPEC=NO

PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_DESTROYS_RESOURCE=NO
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS
```

The authoring-time plan was generated with `terraform plan -refresh=false` and
the current-main tar.gz bytes supplied only through an ephemeral session-local
Terraform variable file. The plan file, plan JSON, archive, and base64 payload
are not committed to the repository.

The future plan presented at apply time must show exactly one create of
`google_vertex_ai_reasoning_engine.mg_guide`, bind `python_spec` only with
`app.agent` / `root_agent`, bind the approved runtime service account email
directly, and show no service-account, key, project IAM, Vertex IAM, secret, or
destroy effects. The fresh plan digest above is evidence at authoring time; the
execution consumer must regenerate and re-gate a current plan before any apply.

## 6. Ceilings and hard prohibitions

```text
MAX_DEPLOYMENTS=1
MAX_SUCCESSFUL_DEPLOYMENTS=1
MAX_TERRAFORM_APPLY_ATTEMPTS=1
MAX_AGENT_RUNTIME_RESOURCES_CREATED=1

NO_RETRY=YES
NO_SECOND_APPLY=YES
NO_FALLBACK_DEPLOYMENT=YES
NO_COMPENSATING_MUTATION=YES
NO_AGENTS_CLI_DEPLOY=YES
NO_ALTERNATE_TERRAFORM_ROOT=YES
NO_ALTERNATE_PROJECT=YES
NO_ALTERNATE_REGION=YES
NO_ALTERNATE_RUNTIME_SERVICE_ACCOUNT=YES
NO_ALTERNATE_SOURCE_PACKAGE=YES
NO_IMAGE_SPEC=YES

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

Any plan or apply effect outside the exact one-add reasoning-engine shape, or
any return to `image_spec`, is a hard stop:

```text
STOP_ON_UNEXPECTED_PLAN_EFFECT=
  UNEXPECTED_TERRAFORM_PLAN_EFFECT
```

## 7. Authority semantics

```text
AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO
ATTEMPT_004_FRESH_ONE_SHOT_AUTHORITY=YES
```

Drafting, opening, reviewing, or merging this authorization does not authorize
deployment. No automation may treat presence of this file, its PR, or its merge
as execution authority.

## 8. Required future Human Activation 004

After independent review and merge of this exact authorization, a separate
artifact is required:

```text
NEXT_AFTER_THIS_AUTHORIZATION_MERGES=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_004
```

Human Activation 004 must separately bind:

```text
ACTIVATION_MUST_BIND=
  - this exact authorization artifact and its merge SHA
  - a fresh run ID
  - a fixed UTC execution window of at most 60 minutes
  - one attempt only
  - consumption on the first apply attempt
  - explicit human execution authority
```

```text
ACTIVATION_004_REQUIRES_NEW_RUN_ID=YES
ACTIVATION_004_REQUIRES_FIXED_UTC_WINDOW=YES
ACTIVATION_004_REQUIRES_NEW_CONSUMPTION_RECORD=YES
ACTIVATION_004_MAY_REUSE_PRIOR_RUN_ID=NO
ACTIVATION_004_MAY_REUSE_PRIOR_WINDOW=NO
ACTIVATION_004_MAY_REUSE_ACTIVATION_001=NO
ACTIVATION_004_MAY_REUSE_ACTIVATION_002=NO
ACTIVATION_004_MAY_REUSE_ACTIVATION_003=NO
ACTIVATION_004_CONSUMES_ON_FIRST_APPLY_ATTEMPT=YES
ACTIVATION_004_SELF_ACTIVATION=FORBIDDEN
ACTIVATION_REUSABLE=NO
WINDOW_EXTENDABLE=NO
```

This authorization unit must not create Human Activation 004.

## 9. Future one-shot execution contract

Only after all of the following are true may a future consumer attempt apply:

1. this authorization is independently reviewed and merged;
2. Human Activation 004 is independently reviewed and merged;
3. a fresh consumption record exists and is unconsumed;
4. explicit human execution authority is present for the fixed window;
5. the required baseline merge SHAs remain ancestors of `origin/main`;
6. the supplied source archive SHA-256 equals the frozen digest;
7. effective `gcp.resourceLocations` still permits `us-east1` and `global`;
8. a non-mutating plan reconfirms
   `1 to add, 0 to change, 0 to destroy` for only
   `google_vertex_ai_reasoning_engine.mg_guide`;
9. the plan uses `python_spec` only (`app.agent` / `root_agent`) and not
   `image_spec`;
10. the plan binds
   `mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`;
11. the plan creates no SA, SA key, IAM binding, secret, or destroy effect.

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
CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES
NO_SECOND_APPLY=YES
NO_RETRY=YES
NO_COMPENSATING_MUTATION=YES
```

If the apply fails or the post-apply ledger is incomplete, authority remains
consumed and no retry is authorized by this artifact or its activation.

## 10. Current non-authority and zero-effect ledger

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

HUMAN_ACTIVATION_004_CREATED_IN_THIS_UNIT=NO
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
```

## 11. STOP

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_004_DEFINED
STOP=INDEPENDENT_REVIEW_REQUIRED

AUTHORIZATION_EFFECTIVE=NO
ACTIVATION_EFFECTIVE=NO
MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION_ALLOWED=NO
EXECUTION_AUTHORIZED_NOW=NO
DEPLOYMENT_AUTHORIZED_NOW=NO
AUTHORIZATION_CONSUMED=NO

DO_NOT_CREATE_HUMAN_ACTIVATION_004=YES
DO_NOT_RUN_TERRAFORM_APPLY=YES
DO_NOT_RUN_AGENTS_CLI_DEPLOY=YES
```
