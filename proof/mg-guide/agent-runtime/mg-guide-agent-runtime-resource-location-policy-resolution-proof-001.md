# MG Guide Agent Runtime Resource Location Policy Resolution Proof 001

## 1. Identity and scope

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_RESOURCE_LOCATION_POLICY_RESOLUTION_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-resource-location-policy-resolution-proof-001.md
PR_CLASS=BOUNDED_PROOF
MODE=POST_REMEDIATION_POLICY_AND_FRESH_PLAN_PROOF
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
```

This proof records that Attempt 001 is terminal and non-reusable, that the
post-remediation effective `gcp.resourceLocations` policy now permits the
immutable Agent Runtime placement, and that a fresh non-mutating Terraform plan
still matches the authorized one-add shape. It does not authorize deployment.

## 2. Attempt 001 terminal closure

```text
PR_384_MERGE_SHA=
  0633377a108a1f0b04c6a68dca595224f961cfba
PR_384_ROLE=
  ATTEMPT_001_TERMINAL_DEPLOYMENT_RESULT_BASELINE
PR_384_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

ATTEMPT_001_RESULT=
  FAILED_ORG_POLICY_GCP_RESOURCE_LOCATIONS
ATTEMPT_001_TERMINAL=YES
ATTEMPT_001_AUTHORITY_CONSUMED=YES
ATTEMPT_001_APPLY_ATTEMPTS=1
ATTEMPT_001_RETRY_AUTHORIZED=NO

AUTHORIZATION_001_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
AUTHORIZATION_001_MERGE_SHA=
  44f19b57f19a2caabf1b9895d75a67afa54d2de3
AUTHORIZATION_001_REUSABLE=NO

ACTIVATION_001_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_HUMAN_ACTIVATION_001
ACTIVATION_001_MERGE_SHA=
  dff7b6875c4c9a319f2d215407e484af382ed572
ACTIVATION_001_REUSABLE=NO

CONSUMPTION_RECORD_001=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-consumption-record-001.md
EXECUTION_PROOF_001=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-execution-proof-001.md
```

Attempt 001 authority was consumed on the first Terraform apply attempt. No
retry, second apply, fallback deployment, or reuse of Authorization 001 /
Activation 001 is authorized.

## 3. Post-remediation effective policy evidence

Observed with:

```text
gcloud org-policies describe \
  gcp.resourceLocations \
  --project=ai-rolodex-to-crm \
  --effective
```

```text
POLICY_NAME=
  projects/831270426395/policies/gcp.resourceLocations
POLICY_SCOPE=PROJECT_EFFECTIVE
CONSTRAINT=constraints/gcp.resourceLocations

POLICY_REMEDIATION_EFFECTIVE=YES
EFFECTIVE_POLICY_ALLOWS_US_EAST1=YES
EFFECTIVE_POLICY_ALLOWS_GLOBAL=YES
POST_REMEDIATION_US_EAST1_ALLOWED=YES
POST_REMEDIATION_GLOBAL_ALLOWED=YES

SANITIZED_ALLOWED_VALUES_EVIDENCE=
  us-east1
  us-east1-locations
  us-east1-a
  us-east1-b
  us-east1-c
  us-east1-d
  us-locations
  us
  US
  global

TERRAFORM_REGION_CHANGE_REQUIRED=NO
SELECTED_AGENT_RUNTIME_REGION=us-east1
```

The full effective allow-list contained 82 values under the US/global placement
family already returned by the project policy. Only the sanitized subset above
is recorded here. No policy mutation was performed in this unit.

## 4. Immutable deployment binding reconfirmed

```text
PROJECT=ai-rolodex-to-crm
REGION=us-east1
SOURCE_BUILD_COMMIT=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
SOURCE_PACKAGE_SIZE_BYTES=343228
SOURCE_PACKAGE_FILE_COUNT=54
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
EXPECTED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
EXPECTED_PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
```

## 5. Off-repo package rebuild and validation

Two independent off-repository rebuilds from `SOURCE_BUILD_COMMIT` using
`scripts/build_agent_runtime_source.py` produced byte-identical archives. The
archive bytes were not committed.

```text
SOURCE_PACKAGE_SHA256_MATCH=YES
SOURCE_PACKAGE_REBUILD_BYTE_IDENTICAL=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO

PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS
ROOT_AGENT_MODULE=app.agent
ROOT_AGENT_FACTORY=
  agents.follow_up_planning.runtime.build_unit3_root_agent
GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

## 6. Fresh non-mutating Terraform plan

```text
TERRAFORM_VERSION=1.9.8
GOOGLE_PROVIDER=hashicorp/google-beta
GOOGLE_PROVIDER_VERSION=7.28.0
```

Commands (non-mutating only):

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan \
  -refresh=false \
  -input=false \
  -no-color \
  -var-file=environments/dev.tfvars \
  -var-file=<SESSION_EPHEMERAL_ARCHIVE_TFVARS> \
  -out=<SESSION_EPHEMERAL_PLAN_FILE>
```

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS

PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES
PLANNED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES

PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_DESTROYS_RESOURCE=NO

PLAN_FILE_SHA256=
  a44077a8845cfd19bb0088a73b147ba562c794cea75d4f35f0771974f503129d
PLAN_FILE_COMMITTED_TO_REPOSITORY=NO
DEPLOYMENT_BYTES_COMMITTED=NO
DEPLOYMENT_EXECUTED=NO
```

Terraform redacted `source_archive` as `(sensitive value)`. The exact input
digest remains the frozen `SOURCE_PACKAGE_SHA256` above.

## 7. Attempt 002 authority posture

```text
ATTEMPT_002_REQUIRES_FRESH_AUTHORIZATION=YES
ATTEMPT_002_REQUIRES_FRESH_HUMAN_ACTIVATION=YES
ATTEMPT_001_AUTHORITY_REUSABLE=NO
AUTHORIZATION_001_REUSABLE=NO
ACTIVATION_001_REUSABLE=NO

NEXT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_002
STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_ANY_APPLY
```

This proof does not activate execution authority, does not open an apply window,
and does not permit `terraform apply` or `agents-cli deploy`.
