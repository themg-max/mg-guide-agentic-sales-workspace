# NW-008 AT1 GHL Workflow WIF Provider Create Authorization 001

## 0. Authorization identity and boundary

```text
AUTHORIZATION_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/
  nw-008-at1-ghl-workflow-wif-provider-create-authorization-001.md
CLASSIFICATION=WORKLOAD_IDENTITY_PROVIDER_CREATE_AUTHORIZATION
PR_CLASS=authorization
MODE=DEFINITION_ONLY_NO_EXECUTION
OWNER=VS_CODE_MG_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS=
  PROPOSED_PENDING_INDEPENDENT_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE_NOW=NO
PROVIDER_CREATE_AUTHORIZED_IN_THIS_PR=NO
SELF_ACTIVATION=FORBIDDEN
MERGE_ALONE_AUTHORIZES_PROVIDER_CREATE=NO
FRESH_ACTIVATION_REQUIRED=YES
```

This artifact defines a bounded future authorization for at most one creation
of the exact dedicated MG Guide GitHub OIDC provider. It does not create,
update, or delete a provider; mutate the existing pool; write service-account
IAM; create a service-account key; request or exchange an OIDC token; mint an
access token; read a secret payload; call HighLevel or CRM; or deploy anything.

## 1. Durable decision inputs

```text
CURRENT_MERGED_BASE=
  0d3907f9fc09c79b0b193eff590ba1b054c39468

RUNTIME_REPAIR_PR=342
RUNTIME_REPAIR_REVIEW_ID=5060260888
RUNTIME_REPAIR_REVIEWED_HEAD=
  057affbb6dd75dabc64c13a60f325abd833ab9f9
RUNTIME_REPAIR_MERGE_SHA=
  9bd3b39ddc1f28e21b5de614dbafe6db4db601b0

WIF_READINESS_PROOF_PR=343
WIF_READINESS_PROOF_REVIEW_ID=5060312078
WIF_READINESS_PROOF_REVIEWED_HEAD=
  543d454ba65f6ff904d3e89b3fc0cd261c2ee603
WIF_READINESS_PROOF_MERGE_SHA=
  0d3907f9fc09c79b0b193eff590ba1b054c39468
WIF_READINESS_PROOF_RESULT=FAIL_CLOSED_EXPECTED
FAILURE_CLASS=
  WIF_PROVIDER_ATTRIBUTE_CONDITION_REPOSITORY_MISMATCH

ARCHITECTURE_DECISION=CREATE_DEDICATED_MG_GUIDE_PROVIDER
EXISTING_PROVIDER_MUTATION_ALLOWED=NO
```

PR #343 established that the repository-scoped Workload Identity User member
on the workflow service account is exact, while the sole existing provider is
owned by another repository lane and cannot admit this repository. The
dedicated-provider decision resolves that mismatch without modifying or
broadening the existing provider or service-account IAM binding.

## 2. Exact provider target

```text
PROJECT_ID=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
LOCATION=global
POOL_ID=github-actions-pool-v2

POOL_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2

EXISTING_PROVIDER_ID=github-actions-provider-v2
EXISTING_PROVIDER_OWNER=A.I-Rolodex---Context FinOps lane
EXISTING_PROVIDER_IMMUTABLE_FOR_THIS_AUTHORIZATION=YES

PROVIDER_ID=mg-guide-github-provider-v1
PROVIDER_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/mg-guide-github-provider-v1
```

No alternate project, pool, provider ID, or provider resource is authorized.

## 3. Exact OIDC configuration

```text
OIDC_ISSUER=https://token.actions.githubusercontent.com

ATTRIBUTE_MAPPING_GOOGLE_SUBJECT=assertion.sub
ATTRIBUTE_MAPPING_ATTRIBUTE_ACTOR=assertion.actor
ATTRIBUTE_MAPPING_ATTRIBUTE_REPOSITORY=assertion.repository
ATTRIBUTE_MAPPING_ATTRIBUTE_REF=assertion.ref

ATTRIBUTE_MAPPING_EXACT=
  google.subject=assertion.sub,
  attribute.actor=assertion.actor,
  attribute.repository=assertion.repository,
  attribute.ref=assertion.ref

ATTRIBUTE_CONDITION=
  assertion.repository == 'themg-max/mg-guide-agentic-sales-workspace'
  &&
  assertion.ref == 'refs/heads/main'
```

The future create must use exactly this issuer, these four mappings, and this
repository-and-main-ref condition. No wildcard repository, alternate ref,
pull-request ref, tag ref, owner-wide condition, or pool-wide eligibility is
authorized.

## 4. Authorized ceilings

```text
MAX_PROVIDER_CREATES=1
MAX_PROVIDER_UPDATES=0
MAX_PROVIDER_DELETES=0

EXISTING_PROVIDER_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
```

```text
NO_RETRY=YES
NO_SECOND_CREATE_ATTEMPT=YES
NO_COMPENSATING_MUTATION=YES
NO_PROVIDER_UPDATE_AFTER_CREATE=YES
NO_PROVIDER_DELETE=YES
NO_EXISTING_PROVIDER_CHANGE=YES
NO_POOL_CHANGE=YES
NO_SERVICE_ACCOUNT_IAM_CHANGE=YES
NO_SERVICE_ACCOUNT_KEY=YES
NO_PROJECT_LEVEL_TOKEN_CREATOR=YES
NO_POOL_WIDE_WORKLOAD_IDENTITY_USER_GRANT=YES
NO_ALTERNATE_PROVIDER=YES
```

## 5. Current PR zero-execution boundary

```text
PROVIDER_CREATE_ATTEMPTS=0
PROVIDER_CREATES=0
PROVIDER_UPDATES=0
PROVIDER_DELETES=0
EXISTING_PROVIDER_MUTATIONS=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0

OIDC_TOKEN_REQUESTS=0
OIDC_TOKEN_EXCHANGES=0
GENERATE_ACCESS_TOKEN_CALLS=0
TOKEN_MINTS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
CRM_CALLS=0
DEPLOYMENTS=0
```

## 6. Required fresh activation and one-shot execution contract

This authorization may be consumed only after it is independently reviewed
and merged and a separate durable activation binds all of the following:

```text
SOURCE_AUTHORIZATION_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_AUTHORIZATION_001
SOURCE_AUTHORIZATION_MERGE_SHA=REQUIRED
SOURCE_AUTHORIZATION_BLOB_SHA=REQUIRED
FRESH_RUN_ID=REQUIRED
BOUNDED_ACTIVATION_WINDOW=REQUIRED
MAX_PROVIDER_CREATES=1
NO_PROVIDER_UPDATES=YES
NO_PROVIDER_DELETES=YES
```

Immediately before any authority is consumed, the execution consumer must
perform read-only reconciliation and require:

```text
POOL_PRESENT=YES
POOL_ACTIVE=YES
NEW_PROVIDER_PRESENT=NO
EXISTING_PROVIDER_PRESENT=YES
EXISTING_PROVIDER_UNCHANGED=YES
WORKFLOW_SERVICE_ACCOUNT_WIF_BINDING_EXACT=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE
ACTIVATION_WINDOW_OPEN=YES
AUTHORITY_UNCONSUMED=YES
```

Any mismatch yields:

```text
STOP=PROVIDER_PRECONDITION_DRIFT
PROVIDER_CREATE_ATTEMPTS=0
```

If every gate passes, the consumer must durably consume the one-shot authority
before dispatch, perform exactly one provider-create operation, perform
read-only exact-resource verification, and stop. The same execution must not
modify or delete the newly created provider.

## 7. Required terminal proof

The separate execution proof must record only non-secret configuration and
effect evidence:

```text
PROVIDER_RESOURCE=EXACT_RESOURCE_REQUIRED
OIDC_ISSUER=EXACT_MATCH_REQUIRED
ATTRIBUTE_MAPPING=EXACT_MATCH_REQUIRED
ATTRIBUTE_CONDITION=EXACT_MATCH_REQUIRED
CREATION_RESULT=REQUIRED
AUTHORITY_CONSUMED=YES
AUTHORITY_REUSABLE=NO

PROVIDER_CREATE_ATTEMPTS=1
PROVIDER_CREATES=1
PROVIDER_UPDATES=0
PROVIDER_DELETES=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
```

If the single create attempt fails, the authority is still terminally consumed
and no retry is authorized. The proof must record the safe failure class and
the bounded zero-or-one effect ledger without credential or token material.

## 8. Non-authority and forbidden disclosures

This artifact does not authorize GitHub workflow implementation, an OIDC
exchange, target-service-account impersonation, Secret Manager access,
HighLevel access, CRM access, deployment, or any Fleet operation. It must
never be interpreted as authority to alter `github-actions-provider-v2` or to
widen the exact existing repository-attribute service-account binding.

```text
CREDENTIAL_VALUES_PUBLISHED=NO
ACCESS_TOKENS_PUBLISHED=NO
OIDC_TOKENS_PUBLISHED=NO
SECRET_PAYLOADS_PUBLISHED=NO
PRIVATE_CRM_DATA_PUBLISHED=NO
```

## 9. Authorization decision

```text
AUTHORIZATION_DEFINITION_COMPLETE=YES
CURRENT_PR_EXECUTION_EFFECT=ZERO
PROVIDER_CREATE_AUTHORIZED_NOW=NO

NEXT=
  INDEPENDENT_REVIEW_AND_MERGE
  THEN_FRESH_PROVIDER_CREATE_ACTIVATION_WITH_NEW_RUN_ID
```
