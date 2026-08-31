# MG Guide Agent Runtime Terraform

This directory is the authoritative, checked-in Terraform source for the MG
Guide Agent Runtime. The generated Terraform under
`mg-guide-orchestrator/deployment/terraform` is reference and bootstrap material
only and must not be applied.

## Ownership boundary

This Terraform root creates only the Agent Runtime reasoning-engine resource. It
reuses the existing runtime service account:

```text
mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

It must not create or manage:

- service accounts or service-account keys;
- project IAM or Vertex IAM bindings;
- Secret Manager resources or secret payloads; or
- Terraform state in the repository.

`environments/dev.tfvars` contains only non-secret deployment identifiers and
an empty ZIP archive used as a schema-complete placeholder source archive. A
real source archive or image selection must be supplied only by a separately
authorized deployment workflow.

## Non-mutating validation

Run from this directory:

```bash
terraform fmt -check
terraform init -backend=false
terraform validate
terraform plan -refresh=false -input=false -var-file=environments/dev.tfvars
```

Before Terraform commands, run the deterministic policy verifier from the
repository root:

```bash
python3 scripts/verify_agent_runtime_terraform_policy.py
```

Do not run `terraform apply` or `agents-cli deploy` without the separate
`MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001` authorization.
