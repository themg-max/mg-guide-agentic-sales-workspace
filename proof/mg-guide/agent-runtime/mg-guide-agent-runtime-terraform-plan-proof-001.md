# MG Guide Agent Runtime Terraform Plan Proof 001

## Scope and command boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_TERRAFORM_PLAN_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-terraform-plan-proof-001.md
PR_CLASS=IMPLEMENTATION
DEPLOYMENT_SOURCE_MODEL=CHECKED_IN_TERRAFORM
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime

GENERATED_AGENTS_CLI_TERRAFORM_IS_AUTHORITY=NO
GENERATED_AGENTS_CLI_TERRAFORM_USE=REFERENCE_AND_BOOTSTRAP_ONLY

TERRAFORM_VERSION=1.9.8
GOOGLE_PROVIDER=hashicorp/google-beta
GOOGLE_PROVIDER_VERSION=7.28.0
```

Only `infra/agent-runtime` was initialized and planned. Terraform initialization
used `-backend=false`; no remote state was configured or written. The plan used
`-refresh=false -input=false` and was not saved as an applyable plan file.

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS

DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
```

## Deterministic policy verification

`python3 scripts/verify_agent_runtime_terraform_policy.py` completed with the
following results:

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

The variable is required (it has no default) and the checked-in non-secret
development binding is:

```text
RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES
TERRAFORM_OWNS_RUNTIME_SERVICE_ACCOUNT=NO
```

## Sanitized plan evidence

The non-mutating plan has one resource action:

```text
EXPECTED_AGENT_RUNTIME_CHANGES=1
PLAN_SUMMARY=1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY

PLANNED_RESOURCE=google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_ARCHIVE=(sensitive value)
```

The plan contains no prohibited resource or mutation type:

```text
PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_VERTEX_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_CREATES_MG_GUIDE_ORCHESTRATOR_APP=NO
```

The plan output intentionally does not include the source archive value. It
shows Terraform's `(sensitive value)` redaction.

## Repository validation

```text
PYTHONPATH_SRC_VERIFY_PHASE1_DETERMINISTIC=PASS
PYTEST=PASS
PYTEST_RESULT=831_PASSED
GIT_DIFF_CHECK=PASS
```

The repository’s default `pytest` command could not collect a root-level
`scripts` namespace in this environment because its configured Python path
contains only `src`. The suite was therefore run as
`PYTHONPATH=.:src <isolated-venv>/bin/pytest`, preserving its existing test
layout without changing repository configuration.

No deployment authorization is implied by this proof. The next action after
independent implementation review and merge remains
`MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001`.
