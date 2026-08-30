# NW-008 AT1 GHL Workflow WIF Provider Create Human Activation 002

## 0. Activation identity and boundary

```text
ACTIVATION_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_HUMAN_ACTIVATION_002
ARTIFACT_PATH=
  governance/authorizations/
  nw-008-at1-ghl-workflow-wif-provider-create-human-activation-002.md
CLASSIFICATION=HUMAN_FINALIZED_ONE_SHOT_WIF_PROVIDER_CREATE_ACTIVATION
PR_CLASS=authorization
MODE=ACTIVATION_PREPARATION_ONLY_NO_PROVIDER_CREATE
OWNER=VS_CODE_MG_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW_AND_MERGE
HUMAN_EXECUTION_AUTHORITY_SOURCE=
  NW-008_AT1_CONTINUOUS_GOVERNED_EXECUTION_MISSION
HUMAN_EXECUTION_AUTHORITY_PRESENT=YES
ACTIVATION_EFFECTIVE_AT_AUTHORING=NO
ACTIVATION_EFFECTIVE_ONLY_AFTER_MERGE_AND_FRESH_GATES=YES
PROVIDER_CREATE_EXECUTED_IN_THIS_PR=NO
```

This artifact binds the merged provider-create authorization to a fresh run
identity and bounded execution window. It performs no provider, pool,
service-account IAM, credential, secret, HighLevel, CRM, or deployment
operation.

The locally prepared Activation 001 was never committed, merged, effective, or
consumed. Its run identity and window are terminally abandoned:

```text
ABANDONED_ACTIVATION_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_HUMAN_ACTIVATION_001
ABANDONED_RUN_ID=
  nw008-at1-ghl-wif-provider-create-20260830t083333z-200bb605
ABANDONED_ACTIVATION_COMMITTED=NO
ABANDONED_ACTIVATION_EFFECTIVE=NO
ABANDONED_AUTHORITY_CONSUMED=NO
ABANDONED_RUN_ID_REUSABLE=NO
```

## 1. Merged source authorization and repair chain

```text
SOURCE_AUTHORIZATION_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_AUTHORIZATION_001
SOURCE_AUTHORIZATION_PATH=
  governance/authorizations/
  nw-008-at1-ghl-workflow-wif-provider-create-authorization-001.md
SOURCE_AUTHORIZATION_PR=344
SOURCE_AUTHORIZATION_REVIEW_ID=5060341530
SOURCE_AUTHORIZATION_REVIEWED_HEAD=
  b331ac2fc7ae056ef89fc49c95d801df9a7430c7
SOURCE_AUTHORIZATION_MERGE_SHA=
  16083097b23ccf9343574f7160ab926e2cce1678
SOURCE_AUTHORIZATION_BLOB_SHA_AT_ACTIVATION_BASE=
  9bb2f510d254cb9d01202c7fd97054ab754c2e7b
SOURCE_AUTHORIZATION_PRESENT_ON_ORIGIN_MAIN=YES
SOURCE_AUTHORIZATION_STATE=MERGED_UNCONSUMED
SOURCE_AUTHORIZATION_CI=SUCCESS

TEST_PURITY_REPAIR_PR=345
TEST_PURITY_REPAIR_REVIEW_ID=5060366997
TEST_PURITY_REPAIR_REVIEWED_HEAD=
  3cad23b91c90e00c3796caf647d1273276a3444b
TEST_PURITY_REPAIR_MERGE_SHA=
  6f4881a066b5fcbe830c52790e0e431804f2f341
TEST_PURITY_REPAIR_PRESENT_ON_ORIGIN_MAIN=YES
TEST_PURITY_REPAIR_CI=SUCCESS

AUTHORITY_CHAIN_VERIFICATION=PASS
```

Any change to the bound authorization identity, blob, reviewed head, merge
chain, or unconsumed state fails closed before authority consumption.

## 2. Fresh read-only preconditions

Observed at `2026-08-30T08:49:00Z` through read-only Google Cloud CLI
operations:

```text
PROJECT_ID=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395

POOL_ID=github-actions-pool-v2
POOL_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2
POOL_PRESENT=YES
POOL_ACTIVE=YES

PROVIDER_ID=mg-guide-github-provider-v1
NEW_PROVIDER_PRESENT=NO
PROVIDER_COUNT=1

EXISTING_PROVIDER_ID=github-actions-provider-v2
EXISTING_PROVIDER_PRESENT=YES
EXISTING_PROVIDER_ACTIVE=YES
EXISTING_PROVIDER_ISSUER=
  https://token.actions.githubusercontent.com
EXISTING_PROVIDER_ATTRIBUTE_CONDITION=
  assertion.repository=='themg-max/A.I-Rolodex---Context'
  &&
  assertion.ref=='refs/heads/chore/finops-phase1'
EXISTING_PROVIDER_UNCHANGED=YES

WORKFLOW_SERVICE_ACCOUNT=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
WORKFLOW_SERVICE_ACCOUNT_WIF_BINDING_COUNT=1
WORKFLOW_SERVICE_ACCOUNT_WIF_BINDING_ROLE=
  roles/iam.workloadIdentityUser
WORKFLOW_SERVICE_ACCOUNT_WIF_BINDING_MEMBER=
  principalSet://iam.googleapis.com/projects/831270426395/
  locations/global/workloadIdentityPools/github-actions-pool-v2/
  attribute.repository/themg-max/mg-guide-agentic-sales-workspace
WORKFLOW_SERVICE_ACCOUNT_WIF_BINDING_EXACT=YES
REPOSITORY_ATTRIBUTE_BOUND=YES
POOL_WIDE_ACCESS_GRANTED=NO
UNEXPECTED_WIF_MEMBERS=NONE
WORKFLOW_SERVICE_ACCOUNT_USER_MANAGED_KEYS=0
```

These observations are preparation evidence only. The execution consumer must
repeat the exact checks immediately before consumption.

## 3. Fresh run identity and bounded window

```text
RUN_ID=
  nw008-at1-ghl-wif-provider-create-20260830t085016z-d292e873
RUN_ID_FINALIZED=YES
RUN_ID_FRESH=YES
RUN_ID_REUSABLE=NO

AUTHORIZATION_WINDOW_START_UTC=2026-08-30T08:50:16Z
AUTHORIZATION_WINDOW_END_UTC=2026-08-30T09:50:16Z
AUTHORIZATION_WINDOW_DURATION_SECONDS=3600
AUTHORIZATION_WINDOW_FINALIZED=YES
AUTHORIZATION_WINDOW_EXTENDABLE=NO
CURRENT_TIME_INSIDE_WINDOW_REQUIRED_AT_CONSUMPTION=YES
CURRENT_TIME_INSIDE_WINDOW_REQUIRED_AT_DISPATCH=YES
```

If the window is closed at consumption or dispatch, this activation is
terminally blocked and permits no extension, retry, or replacement inside the
same execution.

## 4. Exact create configuration

```text
LOCATION=global
POOL_ID=github-actions-pool-v2
PROVIDER_ID=mg-guide-github-provider-v1
PROVIDER_RESOURCE=
  projects/831270426395/locations/global/
  workloadIdentityPools/github-actions-pool-v2/
  providers/mg-guide-github-provider-v1

OIDC_ISSUER=https://token.actions.githubusercontent.com
ATTRIBUTE_MAPPING=
  google.subject=assertion.sub,
  attribute.actor=assertion.actor,
  attribute.repository=assertion.repository,
  attribute.ref=assertion.ref
ATTRIBUTE_CONDITION=
  assertion.repository == 'themg-max/mg-guide-agentic-sales-workspace'
  &&
  assertion.ref == 'refs/heads/main'
```

## 5. One-shot ceilings

```text
MAX_PROVIDER_CREATE_ATTEMPTS=1
MAX_PROVIDER_CREATES=1
MAX_PROVIDER_UPDATES=0
MAX_PROVIDER_DELETES=0

EXISTING_PROVIDER_MUTATIONS=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
```

```text
NO_APPLICATION_RETRY=YES
NO_OPERATOR_RETRY=YES
NO_SECOND_CREATE_ATTEMPT=YES
NO_COMPENSATING_MUTATION=YES
NO_UPDATE_AFTER_CREATE=YES
NO_DELETE=YES
NO_ALTERNATE_PROJECT=YES
NO_ALTERNATE_POOL=YES
NO_ALTERNATE_PROVIDER=YES
NO_EXISTING_PROVIDER_CHANGE=YES
NO_POOL_CHANGE=YES
NO_SERVICE_ACCOUNT_IAM_CHANGE=YES
NO_SERVICE_ACCOUNT_KEY=YES
NO_OIDC_EXCHANGE=YES
NO_TOKEN_MINT=YES
NO_SECRET_ACCESS=YES
NO_GHL_CALL=YES
NO_CRM_CALL=YES
NO_DEPLOYMENT=YES
```

## 6. Prepared consumption record

```text
CONSUMPTION_RECORD_ID=
  NW008_AT1_GHL_WORKFLOW_WIF_PROVIDER_CREATE_CONSUMPTION_002
CONSUMPTION_RECORD_RUN_ID=
  nw008-at1-ghl-wif-provider-create-20260830t085016z-d292e873
CONSUMPTION_RECORD_STATE=PREPARED_UNCONSUMED
AUTHORITY_CONSUMED=NO
AUTHORITY_CONSUMPTION_ATTEMPTS=0
AUTHORITY_REUSABLE_AFTER_CONSUMPTION=NO
AUTHORITY_TRANSFERABLE=NO
```

After every fresh gate passes, the mission runner must durably mark this exact
run's authority consumed before dispatch. A failed create still leaves the
authority terminally consumed and permits no retry.

## 7. Authorized execution sequence

After this exact activation is independently reviewed and merged, the mission
runner must:

1. re-read and require every section 2 precondition;
2. require the section 3 window to be open;
3. durably consume the section 6 one-shot authority;
4. perform exactly one create of the section 4 provider;
5. perform read-only exact-provider and legacy-provider readback;
6. stop and create a terminal execution proof.

The execution must not update or delete the new provider in the same run.

## 8. Required terminal return

```text
PROVIDER_CREATE_ATTEMPTS=1
PROVIDER_CREATES=<0_OR_1>
PROVIDER_UPDATES=0
PROVIDER_DELETES=0
EXISTING_PROVIDER_MUTATIONS=0
POOL_MUTATIONS=0
SERVICE_ACCOUNT_IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0

AUTHORITY_CONSUMED=YES
AUTHORITY_REUSABLE=NO
NO_UNEXPECTED_RETRY=YES
```

Success additionally requires exact issuer, mapping, condition, active-state,
and full-resource-name matches. Failure requires a safe terminal failure class
and no second request.

## 9. Current zero-effect ledger

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
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
CRM_CALLS=0
DEPLOYMENTS=0
```

## 10. Activation decision

```text
ACTIVATION_PREPARATION_COMPLETE=YES
CURRENT_PR_EXECUTION_EFFECT=ZERO
AUTHORITY_CONSUMED=NO

NEXT=
  INDEPENDENT_REVIEW_AND_MERGE
  THEN_FRESH_PREEXECUTION_RECONCILIATION
  THEN_ONE_SHOT_DURABLE_CONSUMPTION_AND_PROVIDER_CREATE
```
