# MG Guide Agent Runtime Deployment Source Designation 001

## Decision

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_SOURCE_DESIGNATION_001
ARTIFACT_PATH=
  docs/architecture/mg-guide-agent-runtime-deployment-source-designation-001.md
ACTION=DESIGNATE_AUTHORITATIVE_DEPLOYMENT_SOURCE
OWNER=VS_CODE_MG_ORCHESTRATOR_STRONGEST_CODING_LANE
PR_CLASS=PLANNING_ONLY_ARCHITECTURE

DEPLOYMENT_SOURCE_MODEL=CHECKED_IN_TERRAFORM
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime

GENERATED_AGENTS_CLI_TERRAFORM_IS_AUTHORITY=NO
GENERATED_AGENTS_CLI_TERRAFORM_USE=REFERENCE_AND_BOOTSTRAP_ONLY
GENERATOR_REFERENCE=agents-cli 1.4.2
```

`infra/agent-runtime` is hereby designated as the sole authoritative source for
the MG Guide Agent Runtime deployment configuration. It is intentionally
checked in, reviewable, and the only Terraform root permitted to receive the
runtime identity repair and future deployment change review.

The locally generated Agents CLI scaffold at
`mg-guide-orchestrator/deployment/terraform/single-project` remains a
non-authoritative reference for resource structure and bootstrap behavior. It
must not be applied, treated as the source of record, or copied wholesale into
the authoritative root.

## Runtime identity ownership

```text
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

TERRAFORM_OWNS_RUNTIME_SERVICE_ACCOUNT=NO
TERRAFORM_OWNS_RUNTIME_SA_KEYS=NO
TERRAFORM_OWNS_VERTEX_PROJECT_IAM=NO

CREATE_SECOND_RUNTIME_IDENTITY=FORBIDDEN
CREATE_SERVICE_ACCOUNT_KEY=FORBIDDEN
ADD_VERTEX_PROJECT_IAM=FORBIDDEN
```

The authoritative root must accept the approved runtime service-account email
as an explicit deployment input. It must reuse that existing account and must
not contain any service-account creation, service-account key, or Vertex
project-IAM-member resource.

The generated name `mg-guide-orchestrator-app` is prohibited from the
authoritative Terraform root.

## State, secrets, and deployment boundary

```text
STATE_FILES_IN_REPO=NO
SECRET_TFVARS_IN_REPO=NO
DEPLOYMENT_AUTHORIZED=NO
AGENT_RUNTIME_DEPLOYMENTS=0
```

Terraform state and secret-bearing variable files remain outside the
repository. The checked-in development variable file may bind only the approved
non-secret runtime service-account email; it must not embed credentials,
service-account keys, or other secret values.

This designation does not authorize `terraform apply`, `agents-cli deploy`, an
IAM mutation, or any other external effect.

## Required Phase 2 implementation boundary

After this planning-only record is independently reviewed and merged, the
implementation must create the minimal `infra/agent-runtime` source set:

```text
versions.tf
providers.tf
variables.tf
service.tf
outputs.tf
environments/dev.tfvars
README.md
```

The implementation must add static policy checks that fail if the
authoritative root contains:

- `resource "google_service_account"`;
- `resource "google_service_account_key"`;
- `mg-guide-orchestrator-app`; or
- prohibited project IAM member resources.

The required non-secret development binding is:

```hcl
runtime_service_account_email =
  "mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
```

Only the Phase 2 implementation may run the bounded Terraform formatting,
initialization without a backend, validation, and non-mutating plan against
this root. Deployment remains prohibited after those checks unless separately
authorized.

```text
PHASE_1_STATUS=AWAITING_INDEPENDENT_REVIEW_AND_MERGE
PHASE_2_IMPLEMENTATION_AUTHORIZED_BY_THIS_ARTIFACT=NO
NEXT_AFTER_IMPLEMENTATION_MERGE=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
```
