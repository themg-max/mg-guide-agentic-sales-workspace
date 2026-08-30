# NW-008 AT1 GHL Workflow WIF Binding Readiness Proof 001

## 0. Proof identity and boundary

```text
PROOF_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_BINDING_READINESS_PROOF_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-workflow-wif-binding-readiness-proof-001.md
CLASSIFICATION=READ_ONLY_WIF_BINDING_READINESS_PROOF
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BRANCH=
  proof/nw008-at1-ghl-workflow-wif-binding-readiness-001
BRANCH_IS_MAIN=NO
AUTHORITATIVE_MERGED_BASE=
  9bd3b39ddc1f28e21b5de614dbafe6db4db601b0
PROOF_EXECUTED_AT_UTC=2026-08-30T08:13:11Z

MODE=READ_ONLY_NO_REFRESH_NO_TOKEN_NO_SECRET_NO_GHL_NO_IAM_MUTATION
```

This proof reads the exact IAM policy on the dedicated GHL workflow service
account and the referenced Workload Identity pool/provider configuration. It
does not authenticate through the provider, exchange an OIDC token, refresh a
credential, mint a Google access token, access Secret Manager, call HighLevel,
call CRM, deploy a workflow, or mutate IAM.

## 1. Merged runtime repair

```text
PR_342_REVIEW_ID=5060260888
PR_342_REVIEWED_HEAD=057affbb6dd75dabc64c13a60f325abd833ab9f9
PR_342_MERGE_SHA=9bd3b39ddc1f28e21b5de614dbafe6db4db601b0
PR_342_MERGE_PRESENT_ON_BASE=YES
```

The merged repair continues to require an explicit root-owned credential file
whose materialized service-account target is
`mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com`. This proof
does not revert that runtime to ambient ADC.

## 2. Project and service-account identity

Read-only project and service-account metadata resolved:

```text
PROJECT_ID=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
PROJECT_STATE=ACTIVE

SERVICE_ACCOUNT=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_PRESENT=YES
SERVICE_ACCOUNT_DISABLED=NO
SERVICE_ACCOUNT_UNIQUE_ID_PRESENT=YES
```

## 3. Exact workflow service-account IAM policy

The exact policy resource read was:

```text
RESOURCE=
  projects/ai-rolodex-to-crm/serviceAccounts/
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
POLICY_READS=1
POLICY_VERSION=1
POLICY_ETAG=BwZaPy3phtU=
POLICY_BINDING_COUNT=1
```

The sole binding was:

```text
ROLE=roles/iam.workloadIdentityUser
MEMBER_COUNT=1
MEMBER=
  principalSet://iam.googleapis.com/projects/831270426395/
  locations/global/workloadIdentityPools/github-actions-pool-v2/
  attribute.repository/themg-max/mg-guide-agentic-sales-workspace
CONDITION=NONE
```

Exact required comparison:

```text
EXPECTED_MEMBER_PREFIX=
  principalSet://iam.googleapis.com/projects/831270426395/
  locations/global/workloadIdentityPools/github-actions-pool-v2/
  attribute.repository/
EXPECTED_MEMBER_VALUE=themg-max/mg-guide-agentic-sales-workspace

EXACT_MEMBER_MATCH=YES
WORKFLOW_SERVICE_ACCOUNT_BOUND=YES
REPOSITORY_ATTRIBUTE_BOUND=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE
```

The service-account policy itself is least-privilege at the requested member
surface: it grants `roles/iam.workloadIdentityUser` to one
`attribute.repository` principal set, not to the whole pool, a user, a
deployer identity, Fleet, or `baby-bumps-runtime-b`.

## 4. Referenced Workload Identity pool

```text
WORKLOAD_IDENTITY_POOL_ID=github-actions-pool-v2
FULL_POOL_RESOURCE_NAME=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2
WIF_POOL_PRESENT=YES
WIF_POOL_STATE=ACTIVE
WIF_POOL_DISABLED=NO
GLOBAL_POOL_COUNT=1
```

## 5. Workload Identity provider

The pool contains one active provider:

```text
WORKLOAD_IDENTITY_PROVIDER_ID=github-actions-provider-v2
FULL_PROVIDER_RESOURCE_NAME=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/github-actions-provider-v2
WIF_PROVIDER_PRESENT=YES
WIF_PROVIDER_STATE=ACTIVE
WIF_PROVIDER_DISABLED=NO
POOL_PROVIDER_COUNT=1
OIDC_ISSUER_URI=https://token.actions.githubusercontent.com
```

The required repository claim is mapped:

```text
ATTRIBUTE_MAPPING_GOOGLE_SUBJECT=assertion.sub
ATTRIBUTE_MAPPING_ATTRIBUTE_ACTOR=assertion.actor
ATTRIBUTE_MAPPING_ATTRIBUTE_REF=assertion.ref
ATTRIBUTE_MAPPING_ATTRIBUTE_REPOSITORY=assertion.repository
REPOSITORY_ATTRIBUTE_MAPPING_PRESENT=YES
```

## 6. Effective provider-condition mismatch

The active provider has an attribute condition in addition to the
service-account binding. Its repository predicate is for a different
repository, and it also fixes a branch:

```text
PROVIDER_ATTRIBUTE_CONDITION_REPOSITORY=
  themg-max/A.I-Rolodex---Context
PROVIDER_ATTRIBUTE_CONDITION_REF=
  refs/heads/chore/finops-phase1
EXPECTED_REPOSITORY=
  themg-max/mg-guide-agentic-sales-workspace

PROVIDER_CONDITION_EXPECTED_REPOSITORY_MATCH=NO
PROVIDER_CONDITION_HAS_BRANCH_RESTRICTION=YES
EXPECTED_REPOSITORY_TOKEN_ELIGIBLE_UNDER_PROVIDER_CONDITION=NO
```

This is not an IAM member mismatch: the service-account member is exact.
However, GitHub OIDC assertions from
`themg-max/mg-guide-agentic-sales-workspace` cannot satisfy the sole active
provider's current repository condition. The complete effective topology is
therefore not ready to materialize the workflow service account.

```text
WIF_BINDING_UI_OBSERVED=YES
SERVICE_ACCOUNT_POLICY_EXACT_MEMBER_MATCH=YES
WIF_PROVIDER_EFFECTIVE_FOR_EXPECTED_REPOSITORY=NO
WIF_EFFECTIVE_TOPOLOGY_READY=NO
```

## 7. Fail-closed readiness decision

The requested repository-scoped member exists exactly and no pool-wide or
unexpected WIF member is present. The provider eligibility predicate is
nevertheless incompatible with that member's repository value.

```text
WIF_PROVIDER_PRESENT=YES
WORKFLOW_SERVICE_ACCOUNT_BOUND=YES
REPOSITORY_ATTRIBUTE_BOUND=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE

WIF_BINDING_READINESS=FAIL_CLOSED
FAILURE_CLASS=WIF_PROVIDER_ATTRIBUTE_CONDITION_REPOSITORY_MISMATCH
IAM_MUTATION_REQUIRED=NOT_INFERRED
AUTOMATIC_REPAIR_ALLOWED=NO
```

No provider condition or service-account policy was changed. Architecture
review must decide whether to create a distinct repository-scoped provider or
perform a separately governed update to an existing provider. This proof does
not authorize either action.

## 8. Separate workflow implementation gate

The requested GitHub Actions identity-materialization implementation belongs
in a separate `workflow_or_infra` PR only after this proof is independently
reviewed and merged and the provider-condition mismatch is resolved.

The future implementation contract remains:

```text
GITHUB_PERMISSIONS_CONTENTS=READ
GITHUB_PERMISSIONS_ID_TOKEN=WRITE
WORKLOAD_IDENTITY_PROVIDER=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/<ARCHITECTURE_REVIEWED_PROVIDER_ID>
SERVICE_ACCOUNT=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
EXPLICIT_WORKFLOW_CONFIG_BRIDGE=
  MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG=
  <credential-file path produced by the GitHub auth step>

AMBIENT_ADC_RUNTIME_FALLBACK=NO
SERVICE_ACCOUNT_KEYS=0
TOKEN_CREATOR_WORKAROUND_GRANTS=0
```

Because the effective provider topology is not ready and this proof is not yet
merged:

```text
SEPARATE_WORKFLOW_IMPLEMENTATION_PR_CREATED=NO
GITHUB_ID_TOKEN_REQUESTS=0
OIDC_TOKEN_EXCHANGES=0
WORKFLOW_CREDENTIAL_FILES_GENERATED=0
DEPLOYMENTS=0
```

## 9. Zero-effect ledger

```text
PROJECT_METADATA_READS=1
WORKFLOW_SERVICE_ACCOUNT_METADATA_READS=1
WORKFLOW_SERVICE_ACCOUNT_POLICY_READS=1
WORKLOAD_IDENTITY_POOL_LIST_READS=1
WORKLOAD_IDENTITY_PROVIDER_LIST_READS=1

CREDENTIAL_REFRESHES=0
GENERATE_ACCESS_TOKEN_CALLS=0
TOKEN_MINTS=0
OIDC_TOKEN_EXCHANGES=0
ACCESS_SECRET_VERSION_CALLS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
CRM_CALLS=0
IAM_MUTATIONS=0
IAM_BINDINGS_ADDED=0
IAM_BINDINGS_REMOVED=0
IAM_PROVIDER_CHANGES=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
```

## 10. Stop

```text
EXACT_SERVICE_ACCOUNT_BINDING_PROVEN=YES
REPOSITORY_SCOPED_MEMBER_PROVEN=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE
WIF_PROVIDER_PRESENT=YES
WIF_PROVIDER_EFFECTIVE_FOR_EXPECTED_REPOSITORY=NO

WIF_BINDING_READINESS=FAIL_CLOSED
STOP=RETURN_FOR_ARCHITECTURE_REVIEW
NEXT_AFTER_ARCHITECTURE_REPAIR=
  INDEPENDENT_PROOF_REVIEW_AND_MERGE
  THEN_SEPARATE_WORKFLOW_OR_INFRA_IMPLEMENTATION_PR
```

Stop here. No credential refresh, token mint, Secret Manager access, HighLevel
call, CRM call, IAM mutation, provider mutation, or deployment occurred.
