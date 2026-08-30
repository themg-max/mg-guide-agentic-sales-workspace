# NW-008 AT1 GHL Workflow Identity Chain Diagnostic Authorization 001

## 0. Authorization identity and boundary

```text
AUTHORIZATION_ID=
  NW008_AT1_GHL_WORKFLOW_IDENTITY_CHAIN_DIAGNOSTIC_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/
  nw-008-at1-ghl-workflow-identity-chain-diagnostic-authorization-001.md
CLASSIFICATION=ONE_SHOT_CREDENTIAL_CHAIN_DIAGNOSTIC_AUTHORIZATION
PR_CLASS=authorization
MODE=DEFINITION_ONLY_NO_WORKFLOW_DISPATCH
OWNER=VS_CODE_MG_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS=PROPOSED_PENDING_INDEPENDENT_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE_NOW=NO
WORKFLOW_DISPATCH_AUTHORIZED_IN_THIS_PR=NO
MERGE_ALONE_AUTHORIZES_DISPATCH=NO
FRESH_ACTIVATION_REQUIRED=YES
```

This artifact defines one future diagnostic chain from GitHub OIDC through the
dedicated workflow service account to the exact note-runtime service account.
It authorizes no Secret Manager access, HighLevel request, CRM operation, IAM
mutation, provider mutation, key creation, or deployment.

## 1. Merged implementation and topology

```text
WIF_TOPOLOGY_PROOF_PR=348
WIF_TOPOLOGY_REVIEW_ID=5060407056
WIF_TOPOLOGY_REVIEWED_HEAD=
  59f6f646e34bed0b9eb0dbe9af30c8fcf3cec6c1
WIF_TOPOLOGY_MERGE_SHA=
  d3cbdc4386a48c7b8838bac279f57c83d1f70806
WIF_EFFECTIVE_TOPOLOGY_READY=YES

WORKFLOW_IMPLEMENTATION_PR=349
WORKFLOW_IMPLEMENTATION_REVIEW_ID=5060466645
WORKFLOW_IMPLEMENTATION_REVIEWED_HEAD=
  e60e3d4d04ad82ac4e683c3906dd010a62672c77
WORKFLOW_IMPLEMENTATION_MERGE_SHA=
  c23ed435bea89e983e43117db6bb226510bdcbcd
WORKFLOW_IMPLEMENTATION_CI=SUCCESS

WORKFLOW_PATH=
  .github/workflows/nw008-at1-ghl-identity-diagnostic.yml
WORKFLOW_BLOB_SHA=
  1db76eb67c8ad0f5527059316a451b8739f4f9aa
DIAGNOSTIC_HARNESS_BLOB_SHA=
  6848c572f919c68916263fbd18767bcab45c5946
RUNTIME_SOURCE_GATE_BLOB_SHA=
  d0433752c8746176129331b437bcd409a344c1f7
```

## 2. Exact authorized chain

```text
WORKFLOW_REF=main
WORKLOAD_IDENTITY_PROVIDER=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/mg-guide-github-provider-v1

OBSERVED_WORKFLOW_SOURCE_PRINCIPAL_REQUIRED=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_PRINCIPAL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

MAX_WORKFLOW_DISPATCHES=1
MAX_GITHUB_OIDC_EXCHANGES=1
MAX_WORKFLOW_IDENTITY_MATERIALIZATIONS=1
MAX_NOTE_RUNTIME_IMPERSONATION_ATTEMPTS=1
MAX_TARGET_CREDENTIAL_REFRESH_ATTEMPTS=1
```

The GitHub auth action may request the GitHub OIDC assertion needed to create
its ephemeral external-account file. The diagnostic target refresh may perform
exactly one STS exchange to materialize the workflow identity and one
`generateAccessToken` operation for the note-runtime target. No application or
operator retry is permitted.

```text
NO_APPLICATION_RETRY=YES
NO_OPERATOR_RETRY=YES
NO_SECOND_WORKFLOW_DISPATCH=YES
NO_ALTERNATE_REF=YES
NO_ALTERNATE_PROVIDER=YES
NO_ALTERNATE_SOURCE_PRINCIPAL=YES
NO_ALTERNATE_TARGET_PRINCIPAL=YES
```

## 3. Required credential handling

```text
EPHEMERAL_EXTERNAL_ACCOUNT_FILE_ALLOWED=YES
EXPLICIT_CREDENTIAL_FILE_BRIDGE_REQUIRED=
  MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG
AMBIENT_ADC_RUNTIME_FALLBACK=NO
SERVICE_ACCOUNT_KEYS_CREATED=0

CREDENTIAL_VALUES_PRINTED=NO
CREDENTIAL_VALUES_PERSISTED=NO
ACCESS_TOKENS_PRINTED=NO
ACCESS_TOKENS_PERSISTED=NO
OIDC_TOKENS_PRINTED=NO
OIDC_TOKENS_PERSISTED=NO
TOKEN_HASHES_PUBLISHED=NO
```

## 4. Explicit non-authority

```text
SECRET_MANAGER_CALLS_ALLOWED=0
SECRET_PAYLOAD_READS_ALLOWED=0
GHL_REST_CALLS_ALLOWED=0
CRM_CALLS_ALLOWED=0
CRM_MUTATIONS_ALLOWED=0
IAM_MUTATIONS_ALLOWED=0
PROVIDER_MUTATIONS_ALLOWED=0
SERVICE_ACCOUNT_KEYS_ALLOWED=0
DEPLOYMENTS_ALLOWED=0
```

This authorization does not permit testing Secret Manager access or calling
HighLevel after a successful identity chain. Those operations require later
fresh authorizations.

## 5. Required activation and consumption

The later activation must bind:

```text
SOURCE_AUTHORIZATION_ID=
  NW008_AT1_GHL_WORKFLOW_IDENTITY_CHAIN_DIAGNOSTIC_AUTHORIZATION_001
SOURCE_AUTHORIZATION_MERGE_SHA=REQUIRED
SOURCE_AUTHORIZATION_BLOB_SHA=REQUIRED
FRESH_RUN_ID=REQUIRED
BOUNDED_ACTIVATION_WINDOW=REQUIRED
WORKFLOW_HEAD_SHA=c23ed435bea89e983e43117db6bb226510bdcbcd
WORKFLOW_REF=main
```

Immediately before dispatch, require the merged workflow blob, dedicated
provider, exact workflow binding, exact source and target contract, open
window, and unconsumed authority. Durably consume authority before the sole
workflow dispatch.

## 6. Required terminal result

Success requires:

```text
WORKFLOW_DISPATCHES=1
GITHUB_OIDC_EXCHANGES=1
OBSERVED_WORKFLOW_SOURCE_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_PRINCIPAL_MATCH=YES
TARGET_PRINCIPAL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_PRINCIPAL_MATCH=YES
NOTE_RUNTIME_IMPERSONATION_ATTEMPTS=1
TARGET_IMPERSONATION_SUCCEEDED=YES
NO_UNEXPECTED_RETRY=YES
```

Failure is terminal, consumes the authority, and permits no second dispatch.
The execution proof must contain safe identity/status metadata only.

## 7. Current zero-effect ledger

```text
WORKFLOW_DISPATCHES=0
GITHUB_OIDC_EXCHANGES=0
WORKFLOW_IDENTITY_MATERIALIZATIONS=0
NOTE_RUNTIME_IMPERSONATION_ATTEMPTS=0
TARGET_CREDENTIAL_REFRESH_ATTEMPTS=0
SECRET_MANAGER_CALLS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
CRM_CALLS=0
IAM_MUTATIONS=0
PROVIDER_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
```

## 8. Decision

```text
AUTHORIZATION_DEFINITION_COMPLETE=YES
AUTHORIZATION_EFFECTIVE_NOW=NO
AUTHORITY_CONSUMED=NO
NEXT=INDEPENDENT_REVIEW_AND_MERGE_THEN_FRESH_ACTIVATION
```
