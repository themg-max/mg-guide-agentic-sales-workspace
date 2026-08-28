# NW-008 AT-1 — GHL REST v3 Stage Provider Validation Private Package Reconciliation 002

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PRIVATE_PACKAGE_RECONCILIATION_002
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-validation-private-package-reconciliation-002.md
ARTIFACT_KIND=SANITIZED_PRIVATE_PACKAGE_RECONCILIATION_PROOF
PR_CLASS=proof_only
OWNER=VS_CODE_ORCHESTRATOR_PRIVATE_BINDING_GOVERNANCE_LANE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=08d1770f3deba0398de78b78d7ec3e27172f3d88
PLAN_BRANCH=
  proof/nw008-at1-ghl-rest-v3-stage-provider-validation-private-package-reconciliation-002
BRANCH_IS_MAIN=NO

MODE=OFFLINE_PRIVATE_RECONCILIATION_ONLY
IMPLEMENTATION_IN_SCOPE=NO
AUTHORIZATION_ARTIFACT_IN_SCOPE=NO
VALIDATION_EXECUTION_IN_SCOPE=NO
CRM_TARGET_CREATION_IN_SCOPE=NO

COMPUTED_AT_UTC=2026-08-28T18:57:20Z
SOURCE_MACHINE_RESULT=
  local/private/nw008-ghl-rest-v3-stage-provider-validation-private-package-reconciliation-002-result.json
```

## 1. Authority boundary

This unit is offline proof only. It reconciles whether the newly human-created
GoHighLevel opportunity can be independently bound into the designated dedicated
stage-provider validation private package.

It does **not** call HighLevel, search/list CRM, mutate CRM, create another
opportunity, move stages, delete, retry provisioning, draft the three-call REST
validation authorization/grant, or publish raw identifiers.

```text
REST_NETWORK_CALLS=0
MCP_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NO_HIGHLEVEL_SEARCH=YES
NO_HIGHLEVEL_LIST=YES
NO_HIGHLEVEL_GET=YES
NO_HIGHLEVEL_PUT=YES

VALIDATION_EXECUTION_AUTHORIZED=NO
THREE_CALL_REST_VALIDATION_AUTHORIZED=NO
THREE_CALL_REST_VALIDATION_EXECUTED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO
SELF_ACTIVATION=FORBIDDEN
```

## 2. Controlling merged lineage

```text
PR263_MERGED=YES
PR263_MERGE_SHA=8a32e31eb12c69bb7eead8b1ded118041070c2c2

PR264_MERGED=YES
PR264_MERGE_SHA=6747fcd2457482a857484e1b451728f4abb1396c
PR264_STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_DEDICATED_TARGET_NOT_AVAILABLE

PR265_MERGED=YES
PR265_MERGE_SHA=58396345226f728c8a929a3ce7af097dfb24702f

PR266_MERGED=YES
PR266_MERGE_SHA=08d1770f3deba0398de78b78d7ec3e27172f3d88

CONTROLLING_AUTHORIZATION=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_TARGET_PROVISIONING_AUTHORIZATION_001
CONTROLLING_COUNTERSIGNATURE=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_TARGET_PROVISIONING_AUTHORIZATION_001_COUNTERSIGNATURE

PACKAGE_ID_DESIGNATED=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001
```

PR #264 established, fail-closed, that no dedicated validation opportunity was
independently bound. PR #265 drafted the inactive human-manual provisioning
authorization. PR #266 finalized the explicit human countersignature window.
This unit answers the post-create reconciliation obligation only.

## 3. Human provisioning execution result (recorded, not re-executed)

```text
PROVISIONING_EXECUTION=SUCCESS

CREATE_OPPORTUNITY_ATTEMPTS_USED=1
CREATE_OPPORTUNITY_SUCCEEDED=YES

PROVISIONING_CONSUMED=YES
NEW_CREATE_ATTEMPT_AUTHORIZED=NO

NEW_VALIDATION_OPPORTUNITY_DISPLAY_NAME=
  MG Guide Stage Validation Synthetic 001

NEW_VALIDATION_OPPORTUNITY_ID_CAPTURED_PRIVATE=NO
RAW_OPPORTUNITY_ID_PUBLIC=NO

HUMAN_RETURN_OR_SCREENSHOT_SUFFICIENT_TO_FREEZE_PRIVATE_BINDINGS=NO

REST_NETWORK_CALLS=0
MCP_CALLS=0
THREE_CALL_REST_VALIDATION_EXECUTED=NO
```

The human return / screenshot is evidence that a distinct visible opportunity
was created. It is **not** sufficient by itself to freeze private bindings.

## 4. Inspection scope (private/local only)

Inspected offline, without printing raw IDs or CRM values:

| Surface | Role | Disposition for this unit |
| --- | --- | --- |
| `local/private/grant008_private_package.json` | Historical Grant 008 private package (gitignored) | Present; binds the **acceptance** synthetic target |
| `local/private/nw008-fresh-private-execution-package-001.json` | Fresh E2E/private execution package (gitignored) | Present; same **acceptance** identity fields as Grant 008 |
| `local/private/nw008-fresh-private-binding-reconciliation-result-001.json` | Fresh package machine result | Present; public commitments already published |
| `proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-validation-private-binding-reconciliation-001.md` | Prior dedicated-target stop | Present; `DEDICATED_VALIDATION_OPPORTUNITY_READY=NO` |
| `local/private/*validation*package*` / designated package file | Dedicated stage-provider validation package | **Absent** |
| Any governed local capture of the new opportunity ID | Private opportunity binding source | **Absent** |
| HighLevel network | Live CRM | **Not contacted** |

```text
INSPECTED_PUBLIC_REPO_ONLY_PLUS_LOCAL_PRIVATE=YES
PRIVATE_PACKAGE_FILES_REMAIN_GITIGNORED=YES
RAW_IDS_READ_FOR_COMPARISON_ONLY=YES
RAW_IDS_PUBLISHED=NO
RAW_CRM_VALUES_PUBLISHED=NO
TOKEN_OR_PIT_PUBLISHED=NO
```

## 5. Required private predicates (computed)

Acceptance-package identity continuity was rechecked offline by equality and
fingerprint comparison only (raw IDs not published):

```text
GRANT008_AND_FRESH_LOCATION_IDENTITY_EQUAL=YES
GRANT008_AND_FRESH_CONTACT_IDENTITY_EQUAL=YES
GRANT008_AND_FRESH_OPPORTUNITY_IDENTITY_EQUAL=YES
GRANT008_AND_FRESH_PIPELINE_IDENTITY_EQUAL=YES
GRANT008_AND_FRESH_INITIAL_STAGE_IDENTITY_EQUAL=YES
GRANT008_AND_FRESH_FINAL_STAGE_IDENTITY_EQUAL=YES
GOVERNED_CANDIDATE_INITIAL_FINAL_STAGE_DISTINCT=YES
ACCEPTANCE_OR_GRANT008_OPPORTUNITY_PRESENT_IN_PRIVATE_PACKAGES=YES
ACCEPTANCE_OR_GRANT008_OPPORTUNITY_REUSE_ALLOWED_FOR_STAGE_PROVIDER_VALIDATION=NO
```

Those acceptance identity fields are **not** counted as dedicated validation
package bindings. Counting them as `YES` would violate
`VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET`.

Dedicated-package predicates:

```text
PRIVATE_LOCATION_BINDING_PRESENT=NO
PRIVATE_CONTACT_BINDING_PRESENT=NO
PRIVATE_OPPORTUNITY_BINDING_PRESENT=NO
PRIVATE_PIPELINE_BINDING_PRESENT=NO
PRIVATE_INITIAL_STAGE_BINDING_PRESENT=NO
PRIVATE_FINAL_STAGE_BINDING_PRESENT=NO

VALIDATION_TARGET_SYNTHETIC=UNKNOWN
VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET=UNKNOWN

VALIDATION_PIPELINE_MATCH=UNKNOWN
VALIDATION_INITIAL_STAGE_MATCH=UNKNOWN
INITIAL_FINAL_STAGE_DISTINCT=UNKNOWN

PRIVATE_BINDING_COMPLETE=NO
```

Rationale:

1. The human UI create consumed the one authorized attempt and reported success
   with display name `MG Guide Stage Validation Synthetic 001`.
2. No governed local/private file captures `private_validation_opportunity_id`.
3. Display name / screenshot cannot freeze `opportunity_id`, pipeline match,
   initial-stage match, or distinctness from the acceptance opportunity.
4. Existing private packages still bind only the Grant 008 / fresh **acceptance**
   opportunity. Explicit comparison of
   `private_validation_opportunity_id != private_acceptance_opportunity_id`
   cannot be completed because the left-hand ID is absent.
5. This lane must **not** search HighLevel, must **not** invent an opportunity
   ID, and must **not** reuse the acceptance opportunity.

```text
INDEPENDENT_DEDICATED_VALIDATION_OPPORTUNITY_BOUND=NO
SUBSTITUTE_TARGET_SELECTION_PERFORMED=NO
CRM_OPPORTUNITY_CREATED_BY_THIS_UNIT=NO
HIGHLEVEL_SEARCH_FOR_OPPORTUNITY_ID=NO
ACCEPTANCE_OPPORTUNITY_REUSED_AS_VALIDATION_TARGET=NO
```

## 6. Failure handling (applied)

Because required private predicates are `NO` or `UNKNOWN`:

```text
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO
DEDICATED_VALIDATION_OPPORTUNITY_READY=NO
VALIDATION_AUTHORIZATION_PREPARATION_READY=NO

THREE_CALL_VALIDATION_AUTHORIZED=NO
THREE_CALL_REST_VALIDATION_AUTHORIZED=NO
VALIDATION_EXECUTION_AUTHORIZED=NO

VALIDATION_PACKAGE_DIGEST=ABSENT
CALL_2_BODY_COMMITMENT=ABSENT

LOCATION_FINGERPRINT=
CONTACT_FINGERPRINT=
OPPORTUNITY_FINGERPRINT=
PIPELINE_FINGERPRINT=
INITIAL_STAGE_FINGERPRINT=
FINAL_STAGE_FINGERPRINT=

STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_PRIVATE_PACKAGE_RECONCILIATION_FAILED
```

Blank fingerprints are intentional: no dedicated package was sealed, so no
validation-package commitments are published or implied. Previously published
**acceptance** fingerprints are not reused here as validation commitments.

```text
DID_NOT_MODIFY_CRM=YES
DID_NOT_CREATE_ANOTHER_OPPORTUNITY=YES
DID_NOT_MOVE_STAGES=YES
DID_NOT_DELETE=YES
DID_NOT_RETRY_PROVISIONING=YES
```

## 7. Package seal status

```text
PACKAGE_ID=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001

PRIVATE_VALIDATION_PACKAGE_SEALED=NO
PRIVATE_VALIDATION_PACKAGE_PATH=ABSENT
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO
```

The designated three-call contract, invariant set, and canonical JSON rules
remain design-retained for a later unit **after** a governed private capture of
the dedicated opportunity ID exists. They are not bound or executed here.

```text
CALL_1=GET /opportunities/{private_validation_opportunity_id}
CALL_2=PUT /opportunities/{private_validation_opportunity_id}
CALL_2_BODY_EXACT={"pipelineStageId":"<private_validation_final_stage_id>"}
CALL_3=GET /opportunities/{private_validation_opportunity_id}

MAX_READS=2
MAX_WRITES=1
MAX_TOTAL_BUSINESS_CALLS=3

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_ALTERNATE_BODY=YES
NO_ALTERNATE_TARGET=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES

INVARIANT_SET_VERSION=NW008_STAGE_VALIDATION_INVARIANT_SET_V1
AUTHORIZED_CHANGED_FIELD=pipelineStageId
CANONICAL_JSON_SPEC=NW008_CANONICAL_JSON_V1

CALLS_BOUND_TO_PRIVATE_VALIDATION_OPPORTUNITY_ID=NO
```

## 8. Grant-preparation result

```text
VALIDATION_AUTHORIZATION_PREPARATION_READY=NO

NEXT_AUTHORIZATION_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_AUTHORIZATION_001
NEXT_GRANT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_GRANT_001

AUTHORIZATION_DRAFT_CREATED_BY_THIS_UNIT=NO
GRANT_DRAFT_CREATED_BY_THIS_UNIT=NO
GRANT_STATE=NOT_DRAFTED
GRANT_COUNTERSIGNED=NO
EXECUTION_AUTHORIZED=NO
SELF_ACTIVATION=FORBIDDEN
```

A later reconciliation may seal the dedicated package only after
`private_validation_opportunity_id` is present in the governed gitignored
private lane and every binding predicate is `YES`, including explicit private
inequality versus the acceptance opportunity ID.

## 9. Explicit non-actions

```text
DID_NOT_CALL_HIGHLEVEL=YES
DID_NOT_SEARCH_LIST_GET_OR_PUT=YES
DID_NOT_MUTATE_CRM=YES
DID_NOT_CREATE_OPPORTUNITY=YES
DID_NOT_RETRY_PROVISIONING=YES
DID_NOT_SELECT_SUBSTITUTE_EXISTING_CRM_OPPORTUNITY=YES
DID_NOT_REUSE_GRANT008_OR_ACCEPTANCE_OPPORTUNITY_AS_VALIDATION_TARGET=YES
DID_NOT_SEAL_VALIDATION_PACKAGE=YES
DID_NOT_INVENT_OPPORTUNITY_ID=YES
DID_NOT_PUBLISH_RAW_IDS=YES
DID_NOT_PUBLISH_RAW_CRM_VALUES=YES
DID_NOT_PUBLISH_TOKEN_OR_PIT=YES
DID_NOT_CREATE_AUTHORIZATION_OR_GRANT=YES
DID_NOT_AUTHORIZE_VALIDATION_EXECUTION=YES
DID_NOT_MUTATE_CONTRACTS_SRC_TESTS_WORKFLOWS_DEPLOY_IAM_SECRETS=YES
```

## 10. Required public return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PRIVATE_PACKAGE_RECONCILIATION_002

BASE_SHA=08d1770f3deba0398de78b78d7ec3e27172f3d88

PR_NUMBER=EXTERNAL_METADATA
HEAD_SHA=EXTERNAL_METADATA

PR_CLASS=proof_only

CREATE_OPPORTUNITY_ATTEMPTS_USED=1
CREATE_OPPORTUNITY_SUCCEEDED=YES

DEDICATED_VALIDATION_OPPORTUNITY_READY=NO
VALIDATION_TARGET_SYNTHETIC=UNKNOWN
VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET=UNKNOWN
VALIDATION_PIPELINE_MATCH=UNKNOWN
VALIDATION_INITIAL_STAGE_MATCH=UNKNOWN
INITIAL_FINAL_STAGE_DISTINCT=UNKNOWN

PRIVATE_BINDING_COMPLETE=NO
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO

VALIDATION_PACKAGE_DIGEST=ABSENT

VALIDATION_AUTHORIZATION_PREPARATION_READY=NO

LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

THREE_CALL_REST_VALIDATION_AUTHORIZED=NO
SUBMISSION_READY=NO

STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_PRIVATE_PACKAGE_RECONCILIATION_FAILED

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
```

`PR_NUMBER` and `HEAD_SHA` remain `EXTERNAL_METADATA` inside this durable
artifact. The proof PR return may populate concrete GitHub values separately
for governance handoff.

## 11. Stop

```text
STOP
```
