# NW-008 AT-8K2 — GHL REST Production Runtime Principal IAM Apply Consumption 001

## Authorization consumption record

```text
UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001
CLASSIFICATION=execution_proof
PR_CLASS=execution_proof
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZED_ONE_SHOT_IAM_APPLY_CONSUMER

PLANNING_IDENTIFIER=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY
AUTHORIZED_CONSUMER_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001
SOLE_CONSUMER_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_EXECUTION_001

AUTHORIZATION_UNIT=NW008_AT8K2_GHL_REST_PRODUCTION_RUNTIME_PRINCIPAL_IAM_APPLY_AUTHORIZATION_001
AUTHORIZATION_ARTIFACT_PATH=
governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md
AUTHORIZATION_PR=117
AUTHORIZATION_REVIEWED_HEAD=e41e88297b01cd8d5656159cd820f68005fd52fb
AUTHORIZATION_MERGE_SHA=e763b360512967a2d8be3805f5ead1a04ad67532
AUTHORIZATION_BLOB_SHA=e0be4e0503ec9ef6d80ad6dbfe6c00601a23e5e9

CONSUMPTION_RECORD_PATH=
proof/nw008/at-8k2/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-consumption-001.md

CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_EXPIRATION=ONE_SHOT_ONLY
AUTHORIZATION_REUSE_PERMITTED=NO
AUTHORIZATION_TRANSFER_PERMITTED=NO
REUSE_ATTEMPT_BEHAVIOR=REJECT
TRANSFER_ATTEMPT_BEHAVIOR=REJECT

BASE_REF=origin/main
BASE_SHA=e763b360512967a2d8be3805f5ead1a04ad67532
EXECUTION_BRANCH=nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-execution-001
RECORDED_AT_UTC=2026-08-21T13:32:11Z
RECORDED_AT_LOCAL=2026-08-21T09:32:11-0400
ACTIVE_GCLOUD_ACCOUNT=themg@themiliare-group.com
```

## Local reconciliation (post-initial abort)

Initial consumer pass aborted fail-closed when the local Git object/path lookup
for the authorization artifact at the merge SHA failed. No GCP mutations were
performed on that initial pass.

This resume pass reconciled the local Git view against the authoritative exact
merge SHA before any mutation:

```text
INITIAL_CONSUMER_RESULT=ABORTED_FAIL_CLOSED
INITIAL_GCP_MUTATIONS=0
INITIAL_SECRET_PAYLOAD_READS=0
INITIAL_HIGHLEVEL_CALLS=0
INITIAL_CRM_MUTATIONS=0

PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PRE_MUTATION_BRANCH_DURING_RECONCILIATION=
nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001

git fetch --prune origin +refs/heads/main:refs/remotes/origin/main
ORIGIN_MAIN_SHA=e763b360512967a2d8be3805f5ead1a04ad67532
LOCAL_PR117_MERGE_SHA_OBJECT_PRESENT=YES
LOCAL_PR117_MERGE_SHA_OBJECT_TYPE=commit
LOCAL_PR117_MERGE_SHA_REACHABLE_FROM_ORIGIN_MAIN=YES
LOCAL_AUTHORIZATION_ARTIFACT_AT_EXACT_MERGE_SHA=YES
LOCAL_AUTHORIZATION_ARTIFACT_AT_CURRENT_ORIGIN_MAIN=YES
LOCAL_RECONCILIATION_PASS=YES
REMOTE_TRACKING_REF_INCONSISTENCY=NO

AUTHORIZATION_MERGE_VERIFIED=YES
AUTHORIZATION_ARTIFACT_ON_MAIN=YES
AUTHORIZATION_EFFECTIVE_FOR_NAMED_CONSUMER=YES
AUTHORIZATION_ARTIFACT_MODIFIED_BY_CONSUMER=NO
```

Verification commands used (read-only):

```text
git rev-parse origin/main
# e763b360512967a2d8be3805f5ead1a04ad67532

git cat-file -t e763b360512967a2d8be3805f5ead1a04ad67532
# commit

git merge-base --is-ancestor \
  e763b360512967a2d8be3805f5ead1a04ad67532 \
  origin/main
# exit 0

git ls-tree -r --name-only e763b360512967a2d8be3805f5ead1a04ad67532 \
  | grep '^governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md$'
# governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md

git cat-file -e \
'e763b360512967a2d8be3805f5ead1a04ad67532:governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md'
# exit 0

git show \
'e763b360512967a2d8be3805f5ead1a04ad67532:governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md' \
>/dev/null
# exit 0

git rev-parse \
'e763b360512967a2d8be3805f5ead1a04ad67532:governance/authorizations/nw008-at8k2-ghl-rest-production-runtime-principal-iam-apply-authorization-001.md'
# e0be4e0503ec9ef6d80ad6dbfe6c00601a23e5e9
```

Known authoritative state confirmed:

```text
PR117_MERGED=YES
PR117_REVIEWED_HEAD=e41e88297b01cd8d5656159cd820f68005fd52fb
PR117_MERGE_SHA=e763b360512967a2d8be3805f5ead1a04ad67532
GITHUB_AUTHORIZATION_ARTIFACT_AT_MERGE_SHA=YES
GITHUB_AUTHORIZATION_ARTIFACT_ON_MAIN=YES
```

## Pre-mutation read-only checks

### Service account preflight

```text
SERVICE_ACCOUNT_ID=mg-guide-ghl-note-runtime
SERVICE_ACCOUNT_PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_PROJECT_NUMBER=831270426395
SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

gcloud iam service-accounts describe \
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com \
  --project=ai-rolodex-to-crm
# NOT_FOUND: Unknown service account.

MUTATION_1_ALREADY_SATISFIED=NO
MUTATION_1_REQUIRED=YES
```

### Secret metadata preflight (no payload access)

```text
SECRET=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_ID=MG_GUIDE_PIT_GHL
SECRET_PROJECT_NUMBER=831270426395

gcloud secrets describe MG_GUIDE_PIT_GHL --project=831270426395
# name: projects/831270426395/secrets/MG_GUIDE_PIT_GHL
# createTime: 2026-08-21T12:36:11.892087Z
# replication.automatic present
# payload NOT accessed
```

### Secret IAM preflight classification

```text
gcloud secrets get-iam-policy MG_GUIDE_PIT_GHL --project=831270426395 --format=json
# {
#   "etag": "ACAB"
# }

EXACT_MEMBER=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
EXACT_ROLE=roles/secretmanager.secretAccessor
EXACT_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL

EXACT_MEMBER_ROLE_RESOURCE_BINDING_PRESENT=NO
CONFLICTING_OR_AMBIGUOUS_IAM_STATE=NO
PROJECT_WIDE_SECRET_ACCESSOR_ALREADY_PRESENT_FOR_PRINCIPAL=NO

MUTATION_2_PREFLIGHT_STATE=STATE_2
MUTATION_2_PREFLIGHT_STATE_MEANING=EXACT_MEMBER_ROLE_RESOURCE_BINDING_ABSENT
MUTATION_2_EXACT_BINDING_ABSENT_IS_AUTHORIZED_PRESTATE=YES
```

## Authorized Mutation 1 — service account create

```text
MUTATION_1_NAME=SERVICE_ACCOUNT_CREATE
MUTATION_1_ATTEMPTS=1
SERVICE_ACCOUNT_CREATE_ATTEMPTS_MAX=1
AUTOMATIC_RETRY=NO
```

Command executed once:

```text
gcloud iam service-accounts create mg-guide-ghl-note-runtime \
  --project=ai-rolodex-to-crm \
  --display-name='MG Guide GHL Note Runtime' \
  --description='Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access'
```

Create result:

```text
MUTATION_1_RESULT=CREATED
SERVICE_ACCOUNT_EMAIL=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_UNIQUE_ID=109958193780365695003
SERVICE_ACCOUNT_NAME=
projects/ai-rolodex-to-crm/serviceAccounts/mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide GHL Note Runtime
SERVICE_ACCOUNT_DESCRIPTION=
Single-purpose production runtime principal for bounded MG Guide HighLevel REST live-note credential access
SERVICE_ACCOUNT_PROJECT_ID=ai-rolodex-to-crm
```

### Mutation 1 readback

```text
gcloud iam service-accounts describe \
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com \
  --project=ai-rolodex-to-crm

SERVICE_ACCOUNT_EXISTS=YES
SERVICE_ACCOUNT_EMAIL_MATCH=YES
MUTATION_1_READBACK_PASS=YES

gcloud iam service-accounts keys list \
  --iam-account=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com \
  --project=ai-rolodex-to-crm \
  --filter='keyType=USER_MANAGED'
# []

USER_MANAGED_SERVICE_ACCOUNT_KEYS=0
SERVICE_ACCOUNT_KEY_CREATED_BY_THIS_CONSUMER=NO
```

Observed system-managed keys only (not created by this consumer; no user-managed
keys present). No key create/download was performed.

Project-wide secretAccessor pre-check for this principal before Mutation 2:

```text
gcloud projects get-iam-policy ai-rolodex-to-crm \
  --flatten='bindings[].members' \
  --filter='bindings.role=roles/secretmanager.secretAccessor AND bindings.members:serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com'
# []

PROJECT_WIDE_SECRET_ACCESSOR_ADDED=NO
```

## Authorized Mutation 2 — single-secret IAM bind

```text
MUTATION_2_NAME=SINGLE_SECRET_IAM_BIND
MUTATION_2_PREFLIGHT_STATE=STATE_2
MUTATION_1_READBACK_PASS=YES
MUTATION_2_AUTHORIZED_TO_ATTEMPT=YES
MUTATION_2_ATTEMPTS=1
SECRET_IAM_BIND_ATTEMPTS_MAX=1
AUTOMATIC_RETRY=NO
```

Command executed once:

```text
gcloud secrets add-iam-policy-binding MG_GUIDE_PIT_GHL \
  --project=ai-rolodex-to-crm \
  --member='serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'
```

Bind result (command output policy):

```text
MUTATION_2_RESULT=BOUND
bindings:
  - members:
      - serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
    role: roles/secretmanager.secretAccessor
etag: BwZZjqmJGAM=
version: 1
```

### Mutation 2 readback

```text
gcloud secrets get-iam-policy MG_GUIDE_PIT_GHL --project=831270426395 --format=json
# {
#   "bindings": [
#     {
#       "members": [
#         "serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
#       ],
#       "role": "roles/secretmanager.secretAccessor"
#     }
#   ],
#   "etag": "BwZZjqmJGAM=",
#   "version": 1
# }

SECRET_IAM_BINDING_PRESENT=YES
SECRET_IAM_MEMBER_MATCH=YES
SECRET_IAM_ROLE_MATCH=YES
SECRET_IAM_RESOURCE_MATCH=YES
SECRET_ACCESS_ROLE_CONFIGURED=YES
MUTATION_2_READBACK_PASS=YES
```

## Required proof summary

```text
SERVICE_ACCOUNT_EXISTS=YES
SERVICE_ACCOUNT_EMAIL_MATCH=YES
USER_MANAGED_SERVICE_ACCOUNT_KEYS=0

MUTATION_1_ATTEMPTS=1
MUTATION_1_ALREADY_SATISFIED=NO
MUTATION_1_READBACK_PASS=YES

MUTATION_2_PREFLIGHT_STATE=STATE_2
MUTATION_2_ATTEMPTS=1
MUTATION_2_READBACK_PASS=YES

SECRET_IAM_BINDING_PRESENT=YES
SECRET_IAM_MEMBER_MATCH=YES
SECRET_IAM_ROLE_MATCH=YES

PROJECT_WIDE_SECRET_ACCESSOR_ADDED=NO

SECRET_ACCESS_ROLE_CONFIGURED=YES
SECRET_PAYLOAD_ACCESS_EXECUTED=NO

REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0

GCP_MUTATIONS=2
# Mutation 1: service account create
# Mutation 2: single-secret IAM bind

LOCAL_PR117_MERGE_SHA_OBJECT_PRESENT=YES
LOCAL_PR117_MERGE_SHA_REACHABLE_FROM_ORIGIN_MAIN=YES
LOCAL_AUTHORIZATION_ARTIFACT_AT_EXACT_MERGE_SHA=YES
LOCAL_AUTHORIZATION_ARTIFACT_AT_CURRENT_ORIGIN_MAIN=YES
LOCAL_RECONCILIATION_PASS=YES
AUTHORIZATION_EFFECTIVE_FOR_NAMED_CONSUMER=YES
AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

## Forbidden actions not performed

```text
SERVICE_ACCOUNT_KEYS_CREATED=NO
PROJECT_WIDE_SECRET_ACCESSOR_BOUND=NO
ALTERNATE_PRINCIPAL_BOUND=NO
ALTERNATE_SECRET_BOUND=NO
ADDITIONAL_ROLES_BOUND=NO
AUTOMATIC_RETRY=NO
AUTOMATIC_CLEANUP=NO
COMPENSATING_MUTATION=NO
SECRET_PAYLOAD_ACCESS=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
AT8L_STARTED=NO
AUTHORIZATION_ARTIFACT_MODIFIED=NO
```

## Boundary statements

This one-shot consumer applied only the exact authorized pair:

1. create `mg-guide-ghl-note-runtime` in project `ai-rolodex-to-crm`; and
2. bind that principal as `roles/secretmanager.secretAccessor` on
   `projects/831270426395/secrets/MG_GUIDE_PIT_GHL` only.

This record does **not** authorize:

- secret payload reads by humans or orchestrator users;
- HighLevel / CRM live calls;
- service-account key creation;
- project-wide Secret Accessor;
- deployment / runtime platform bind;
- AT8L implementation;
- reuse or transfer of PR #117 authorization.

```text
AT8K2_IAM_APPLY_CONSUMER_COMPLETE=YES
AT8L_STARTED=NO
STOP_AFTER_EXECUTION_PROOF=YES
```
