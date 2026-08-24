# NW-008 AT8W24 Lane B Commitment Key Accessor Closure Proof 001

## 1. Unit identity

```text
UNIT=NW008_AT8W24_LANE_B_COMMITMENT_KEY_ACCESSOR_CLOSURE_001
MODE=HUMAN_GOVERNED_CONDITIONAL_SECRET_IAM_REMEDIATION
WORKSTREAM=NW-008
CLASSIFICATION=execution_proof
PR_CLASS=execution_proof
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_STATE=GRANTED_BY_HUMAN_GOVERNANCE
AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_EXPIRATION=ONE_SHOT_ONLY

SOURCE_PLAN=
  docs/nw008/nw-008-at8w23-external-prerequisite-remediation-plan-001.md
PROOF_ARTIFACT=
  proof/nw008/at-8w24/nw008-at8w24-lane-b-commitment-key-accessor-closure-proof-001.md

PROJECT=ai-rolodex-to-crm
PROJECT_NUMBER=831270426395
SECRET=MG_GUIDE_NW008_COMMITMENT_KEY
EXACT_SECRET_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
EXACT_SECRET_FULL_RESOURCE_NAME=
  //secretmanager.googleapis.com/projects/831270426395/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
EXACT_VERSION=1
RUNTIME_PRINCIPAL=
  serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
ROLE=roles/secretmanager.secretAccessor
PERMISSION_EVALUATED=secretmanager.versions.access

BASE_REF=origin/main
BASE_SHA=a208d1f2455d4104588c650de875ef35957acc52
EXECUTION_BRANCH=
  nw008-at8w24-lane-b-commitment-key-accessor-closure-001
WORKTREE=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace-nw008-at8w24-lane-b
RECORDED_AT_UTC=2026-08-24T14:32:17Z
RECORDED_AT_LOCAL=2026-08-24T10:32:17-0400
ACTIVE_GCLOUD_ACCOUNT=themg@themiliare-group.com
```

## 2. Precondition verification

```text
PR194_MERGED=YES
  EVIDENCE=
    gh pr view 194 --json state,mergedAt,title
    state=MERGED
    mergedAt=2026-08-24T14:11:44Z
    title=docs(nw008): AT8W23 external prerequisite remediation plan
    merge_commit_on_origin_main=a208d1f2455d4104588c650de875ef35957acc52

AT8W23_MAIN_CONTENT_VERIFIED=YES
  EVIDENCE=
    origin/main contains
    docs/nw008/nw-008-at8w23-external-prerequisite-remediation-plan-001.md
    path blob at origin/main tip reachable from PR194 merge
    LANE_B section present (EXACT_SECRET_COMMITMENT_KEY_ACCESSOR_CLOSURE)

SECRET_EXISTS=YES
  EVIDENCE=
    gcloud secrets describe MG_GUIDE_NW008_COMMITMENT_KEY
      --project=ai-rolodex-to-crm
    name=projects/831270426395/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
    labels.purpose=nw008-execution-commitment-key
    labels.workstream=nw-008

EXACT_VERSION_EXISTS=YES
EXACT_VERSION=1
EXACT_VERSION_STATE=ENABLED
  EVIDENCE=
    gcloud secrets versions describe 1
      --secret=MG_GUIDE_NW008_COMMITMENT_KEY
      --project=ai-rolodex-to-crm
    name=.../versions/1
    state=ENABLED

RUNTIME_SA_EXISTS=YES
  EVIDENCE=
    gcloud iam service-accounts describe
      mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
    email present; disabled not set

PRECONDITION_GATE=PASSED
```

Fresh proof branch/worktree created from `origin/main` (not `main` checkout
with dirty local state). No `git add .` used.

## 3. Forbidden-effects ledger (unit-wide)

```text
SECRET_PAYLOAD_READ=0
SECRET_PAYLOAD_READS=0
PROJECT_WIDE_SECRET_ACCESSOR_GRANT=0
PROJECT_WIDE_SECRET_ACCESSOR_USED=NO
SECRET_MUTATION=0
SECRET_VERSION_MUTATION=0
TOKEN_MINT=0
SERVICE_ACCOUNT_IMPERSONATION=0
CONFIG_MUTATION=0
STORE_WRITE=0
RUNTIME_CODE_EDIT=0
HIGHLEVEL_CALL=0
CRM_MUTATION=0
```

Methods deliberately not used:

- no `gcloud secrets versions access`
- no `--impersonate-service-account`
- no access-token mint for the runtime SA
- no project-level `add-iam-policy-binding` for secretAccessor

## 4. STEP B1 — Read-only effective IAM evaluation

### 4.1 Direct binding facts (pre-mutation)

```text
DIRECT_SECRET_ACCESSOR_BINDING=NO
  EVIDENCE=
    gcloud secrets get-iam-policy MG_GUIDE_NW008_COMMITMENT_KEY
      --project=ai-rolodex-to-crm --format=json
    policy body:
      { "etag": "ACAB" }
    (empty bindings; default empty secret IAM policy)

PROJECT_WIDE_SECRET_ACCESSOR=NO
  EVIDENCE=
    gcloud projects get-iam-policy ai-rolodex-to-crm
      --flatten=bindings[].members
      --filter='bindings.role:roles/secretmanager.secretAccessor
                AND bindings.members:serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com'
    result empty for runtime principal
  NOTE=
    Other project members hold roles/secretmanager.secretAccessor
    (compute default SA, a-i-rolodex-backend, github-ci-deployer,
     iap-oauth-sa, oauth-public-invoker). Runtime SA is not among them.
    No project-wide grant was added or altered by this unit.

RUNTIME_SA_PROJECT_BINDINGS_ANY=
  none observed for
  serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
```

### 4.2 Effective evaluation (Policy Troubleshooter)

```text
EVALUATOR=gcloud policy-troubleshoot iam
RESOURCE=
  //secretmanager.googleapis.com/projects/831270426395/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
PRINCIPAL_EMAIL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PERMISSION=secretmanager.versions.access

PRE_MUTATION_ACCESS=NOT_GRANTED
  explainedPolicies include:
    secret resource policy etag=ACAB → NOT_GRANTED
    project / org inherited policies → NOT_GRANTED for this principal+permission
  (deny-explanation sub-error ERROR_IAM_DENY observed as non-blocking
   diagnostic noise; allow-policy explanation still returned NOT_GRANTED)

EFFECTIVE_SECRET_ACCESSOR_READY=NO
DIRECT_SECRET_ACCESSOR_BINDING=NO
PROJECT_WIDE_SECRET_ACCESSOR=NO

IAM_MUTATION_REQUIRED=YES
B1_OUTCOME=PROCEED_TO_B2
```

## 5. STEP B2 — Conditional exact-secret IAM grant

Authorized only because B1 resolved `EFFECTIVE_SECRET_ACCESSOR_READY=NO`.

```text
IAM_MUTATION_BUDGET=1
RETRY_BUDGET=0
SCOPE=EXACT_SECRET_ONLY
PROJECT_WIDE_GRANT_ALLOWED=NO

APPLY_COMMAND=
  gcloud secrets add-iam-policy-binding MG_GUIDE_NW008_COMMITMENT_KEY
    --project=ai-rolodex-to-crm
    --member=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
    --role=roles/secretmanager.secretAccessor

APPLY_EXIT=0
IAM_MUTATIONS=1

POST_MUTATION_SECRET_IAM_POLICY=
{
  "bindings": [
    {
      "members": [
        "serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
      ],
      "role": "roles/secretmanager.secretAccessor"
    }
  ],
  "etag": "BwZZy9kl8ro=",
  "version": 1
}

UNRELATED_IAM_MEMBER_OR_ROLE_CHANGE=NO
  single binding present on exact secret after apply;
  project IAM secretAccessor set for other principals unchanged by this unit
```

## 6. STEP B3 — Read-only verification

```text
SECRET_EXISTS=YES
EXACT_VERSION=1
EXACT_VERSION_STATE=ENABLED

DIRECT_SECRET_ACCESSOR_BINDING=YES
  EVIDENCE=secret IAM policy binding above (etag BwZZy9kl8ro=)

PROJECT_WIDE_SECRET_ACCESSOR=NO
  EVIDENCE=
    post-mutation project IAM filter for runtime SA +
    roles/secretmanager.secretAccessor still empty

EFFECTIVE_SECRET_ACCESSOR_READY=YES
  EVIDENCE=
    gcloud policy-troubleshoot iam
      //secretmanager.googleapis.com/projects/831270426395/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
      --principal-email=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
      --permission=secretmanager.versions.access
    access=GRANTED
    binding explanation on exact secret:
      role=roles/secretmanager.secretAccessor
      access=GRANTED
      rolePermission=ROLE_PERMISSION_INCLUDED
      membership=MEMBERSHIP_INCLUDED for runtime SA
    project resource explanation: NOT_GRANTED
    organization resource explanation: NOT_GRANTED
    → access is exact-secret scope, not project-wide inheritance

COMMITMENT_KEY_IAM_READY=YES
C4_EXTERNAL_PREREQUISITES_READY=YES
  SCOPE_NOTE=
    C4 external prerequisite closed by this unit is the commitment-key
    effective accessor readiness path from AT8W23 Lane B / C4 gate material.
    This unit does not claim Lane A identity closure or Lane C store closure.
```

## 7. Return block

```text
UNIT=NW008_AT8W24_LANE_B_COMMITMENT_KEY_ACCESSOR_CLOSURE_001

EFFECTIVE_SECRET_ACCESSOR_READY=YES
IAM_MUTATION_REQUIRED=YES
IAM_MUTATIONS=1
IAM_MUTATION_BUDGET=1

COMMITMENT_KEY_IAM_READY=YES
C4_EXTERNAL_PREREQUISITES_READY=YES

SECRET_PAYLOAD_READS=0
PROJECT_WIDE_SECRET_ACCESSOR_USED=NO

AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO

NEXT=LANE_B_COMPLETE
```

## 8. Validation gates

```text
C4_EXTERNAL_PREREQUISITES_READY=YES
IAM_MUTATIONS<=1          (actual=1)
SECRET_PAYLOAD_READS=0
PROJECT_WIDE_SECRET_ACCESSOR_USED=NO
DIRECT_SECRET_ACCESSOR_BINDING=YES
EFFECTIVE_SECRET_ACCESSOR_READY=YES
COMMITMENT_KEY_IAM_READY=YES
LANE_B_STATUS=COMPLETE
```
