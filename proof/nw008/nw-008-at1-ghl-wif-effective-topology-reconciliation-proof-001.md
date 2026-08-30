# NW-008 AT1 GHL WIF Effective Topology Reconciliation Proof 001

## 0. Proof identity and boundary

```text
PROOF_ID=
  NW008_AT1_GHL_WIF_EFFECTIVE_TOPOLOGY_RECONCILIATION_PROOF_001
ARTIFACT_PATH=
  proof/nw008/
  nw-008-at1-ghl-wif-effective-topology-reconciliation-proof-001.md
CLASSIFICATION=READ_ONLY_WIF_EFFECTIVE_TOPOLOGY_PROOF
PR_CLASS=proof_only
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
EXECUTED_AT_UTC=2026-08-30T09:03:15Z
MODE=READ_ONLY_NO_OIDC_NO_TOKEN_NO_SECRET_NO_GHL_NO_MUTATION
```

This proof reconciles the exact workload identity pool, both providers, and
the workflow service-account IAM policy after the one-shot dedicated-provider
create. It performs no OIDC exchange, credential refresh, token mint, secret
access, HighLevel request, CRM call, deployment, IAM write, or provider write.

## 1. Bound provider-create proof

```text
PROVIDER_EXECUTION_PROOF_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_EXECUTION_PROOF_001
PROVIDER_EXECUTION_PROOF_PR=347
PROVIDER_EXECUTION_PROOF_REVIEW_ID=5060395563
PROVIDER_EXECUTION_PROOF_REVIEWED_HEAD=
  6a8997e529b93352038abc810d6aad971ba37d36
PROVIDER_EXECUTION_PROOF_MERGE_SHA=
  9713289ea629586bce50f48555711f865a331e42
PROVIDER_EXECUTION_PROOF_PRESENT_ON_ORIGIN_MAIN=YES
PROVIDER_CREATE_RESULT=PASS
PROVIDER_CREATE_ATTEMPTS=1
PROVIDER_CREATES=1
PROVIDER_UPDATES=0
PROVIDER_DELETES=0
```

## 2. Workload Identity pool

```text
PROJECT_ID=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
POOL_ID=github-actions-pool-v2
POOL_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2
WIF_POOL_PRESENT=YES
WIF_POOL_STATE=ACTIVE
WIF_POOL_DISABLED=NO
POOL_PROVIDER_COUNT=2
```

## 3. Dedicated MG Guide provider

```text
PROVIDER_ID=mg-guide-github-provider-v1
PROVIDER_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/mg-guide-github-provider-v1
MG_GUIDE_PROVIDER_PRESENT=YES
MG_GUIDE_PROVIDER_ACTIVE=YES
MG_GUIDE_PROVIDER_DISABLED=NO

OIDC_ISSUER=https://token.actions.githubusercontent.com
OIDC_ISSUER_MATCH=YES

ATTRIBUTE_MAPPING_GOOGLE_SUBJECT=assertion.sub
ATTRIBUTE_MAPPING_ATTRIBUTE_ACTOR=assertion.actor
ATTRIBUTE_MAPPING_ATTRIBUTE_REPOSITORY=assertion.repository
ATTRIBUTE_MAPPING_ATTRIBUTE_REF=assertion.ref
ATTRIBUTE_MAPPING_EXACT=YES

ATTRIBUTE_CONDITION=
  assertion.repository == 'themg-max/mg-guide-agentic-sales-workspace'
  &&
  assertion.ref == 'refs/heads/main'
MG_GUIDE_PROVIDER_REPOSITORY_MATCH=YES
MG_GUIDE_PROVIDER_MAIN_REF_MATCH=YES
```

## 4. Legacy provider preservation

```text
LEGACY_PROVIDER_ID=github-actions-provider-v2
LEGACY_PROVIDER_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/github-actions-provider-v2
LEGACY_PROVIDER_PRESENT=YES
LEGACY_PROVIDER_ACTIVE=YES
LEGACY_PROVIDER_DISABLED=NO
LEGACY_PROVIDER_ISSUER=
  https://token.actions.githubusercontent.com
LEGACY_PROVIDER_REPOSITORY=
  themg-max/A.I-Rolodex---Context
LEGACY_PROVIDER_REF=
  refs/heads/chore/finops-phase1
LEGACY_PROVIDER_UNCHANGED=YES
```

No provider condition, mapping, issuer, state, or ownership field was changed
by this reconciliation.

## 5. Exact workflow service-account policy

```text
WORKFLOW_SERVICE_ACCOUNT=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
POLICY_VERSION=1
POLICY_BINDING_COUNT=1

ROLE=roles/iam.workloadIdentityUser
MEMBER_COUNT=1
MEMBER=
  principalSet://iam.googleapis.com/projects/831270426395/
  locations/global/workloadIdentityPools/github-actions-pool-v2/
  attribute.repository/themg-max/mg-guide-agentic-sales-workspace
CONDITION=NONE

WORKFLOW_SERVICE_ACCOUNT_BOUND=YES
REPOSITORY_ATTRIBUTE_BOUND=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE
WORKFLOW_SERVICE_ACCOUNT_USER_MANAGED_KEYS=0
```

## 6. Effective topology decision

```text
MG_GUIDE_PROVIDER_PRESENT=YES
MG_GUIDE_PROVIDER_ACTIVE=YES
MG_GUIDE_PROVIDER_REPOSITORY_MATCH=YES
MG_GUIDE_PROVIDER_MAIN_REF_MATCH=YES

LEGACY_PROVIDER_UNCHANGED=YES

WORKFLOW_SERVICE_ACCOUNT_BOUND=YES
REPOSITORY_ATTRIBUTE_BOUND=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE

WIF_EFFECTIVE_TOPOLOGY_READY=YES
```

The dedicated provider's `attribute.repository` mapping and repository
condition align with the sole repository-scoped Workload Identity User member
on the workflow service account. The provider additionally restricts
eligibility to `refs/heads/main`.

## 7. Zero-effect ledger

```text
POOL_READS=1
PROVIDER_LIST_READS=1
WORKFLOW_SERVICE_ACCOUNT_POLICY_READS=1
WORKFLOW_SERVICE_ACCOUNT_KEY_LIST_READS=1

OIDC_TOKEN_REQUESTS=0
OIDC_TOKEN_EXCHANGES=0
CREDENTIAL_REFRESHES=0
GENERATE_ACCESS_TOKEN_CALLS=0
TOKEN_MINTS=0
SECRET_ACCESSES=0
SECRET_PAYLOADS_PUBLISHED=0
GHL_REST_CALLS=0
CRM_CALLS=0
DEPLOYMENTS=0

PROVIDER_CREATES=0
PROVIDER_UPDATES=0
PROVIDER_DELETES=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
```

## 8. Decision

```text
WIF_EFFECTIVE_TOPOLOGY_READY=YES
PROOF_RESULT=PASS

NEXT=
  INDEPENDENT_REVIEW_AND_MERGE
  THEN_DEDICATED_GITHUB_WORKFLOW_IDENTITY_IMPLEMENTATION
```
