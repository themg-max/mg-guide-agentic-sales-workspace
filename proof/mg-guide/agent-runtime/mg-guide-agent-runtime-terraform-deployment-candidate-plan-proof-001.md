# MG Guide Agent Runtime Terraform Deployment Candidate Plan Proof 001

## Bound candidate

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_TERRAFORM_DEPLOYMENT_CANDIDATE_PLAN_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-terraform-deployment-candidate-plan-proof-001.md
PR_CLASS=BOUNDED_PROOF

PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
SOURCE_BASE_COMMIT=
  eebd09055de2e72c7dce6ebf0f202a415a362a81
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
SOURCE_PACKAGE_SIZE_BYTES=343228
SOURCE_PACKAGE_FILE_COUNT=54

AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
PROJECT=ai-rolodex-to-crm
REGION=us-east1
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

The source ZIP remained outside the repository. Its base64 encoding was written
to a mode-`0600`, off-repository ephemeral tfvars file. Decoding that exact
Terraform input produced:

```text
EPHEMERAL_INPUT_DECODED_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
EPHEMERAL_INPUT_DECODED_SIZE_BYTES=343228
EPHEMERAL_INPUT_MATCHES_SOURCE_PACKAGE=YES
CHECKED_IN_EMPTY_ZIP_PLACEHOLDER_REPLACED=NO
DEPLOYMENT_BYTES_COMMITTED=NO
```

## Toolchain and commands

```text
TERRAFORM_VERSION=1.9.8
GOOGLE_PROVIDER=hashicorp/google-beta
GOOGLE_PROVIDER_VERSION=7.28.0
```

The following non-mutating sequence ran against only the authoritative root:

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan \
  -refresh=false \
  -input=false \
  -no-color \
  -var-file=environments/dev.tfvars \
  -var-file=<SESSION_EPHEMERAL_ARCHIVE_TFVARS>
```

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS
```

## Sanitized plan classification

Terraform redacted `source_archive` as `(sensitive value)`. The exact input
digest is established above without publishing the base64 bytes.

```text
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_AGENT_RUNTIME_CHANGES=1
PLANNED_RESOURCE=google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES

PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_VERTEX_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_CREATES_MG_GUIDE_ORCHESTRATOR_APP=NO
PLAN_DESTROYS_RESOURCE=NO
```

The authoritative Terraform policy verifier also passed:

```text
NO_GOOGLE_SERVICE_ACCOUNT_RESOURCE=PASS
NO_SERVICE_ACCOUNT_KEY_RESOURCE=PASS
NO_PROJECT_VERTEX_IAM_RESOURCE=PASS
NO_SECRET_RESOURCE=PASS
NO_MG_GUIDE_ORCHESTRATOR_APP=PASS
RUNTIME_SA_VARIABLE_REQUIRED=PASS
RUNTIME_RESOURCE_USES_SA_VARIABLE=PASS
DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA=PASS
NO_TERRAFORM_STATE_FILES=PASS
```

## Repository validation and effect ledger

```text
GIT_DIFF_CHECK=PASS
PHASE1_DETERMINISTIC_VERIFIER=PASS
PYTEST=PASS
PYTEST_RESULT=832_PASSED

TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
AGENT_RUNTIME_DEPLOYMENTS=0

SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

## Review boundary

This proof fixes the exact source candidate and demonstrates its non-mutating
Terraform plan. It does not authorize deployment.

Any later `MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001` must bind all
of the following without substitution:

```text
PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROJECT=ai-rolodex-to-crm
REGION=us-east1
MAX_DEPLOYMENTS=1
```

```text
NEXT=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
STOP=INDEPENDENT_REVIEW_REQUIRED
```
