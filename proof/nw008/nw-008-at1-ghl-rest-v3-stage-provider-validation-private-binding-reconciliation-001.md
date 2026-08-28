# NW-008 AT-1 — GHL REST v3 Stage Provider Validation Private Binding Reconciliation 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PRIVATE_BINDING_RECONCILIATION_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-validation-private-binding-reconciliation-001.md
ARTIFACT_KIND=SANITIZED_PRIVATE_BINDING_RECONCILIATION_PROOF
PR_CLASS=proof_only
OWNER=VS_CODE_ORCHESTRATOR_PRIVATE_BINDING_GOVERNANCE_LANE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=8a32e31eb12c69bb7eead8b1ded118041070c2c2
PLAN_BRANCH=
  plan/nw008-at1-ghl-rest-v3-stage-provider-validation-private-binding-reconciliation-001
BRANCH_IS_MAIN=NO

MODE=OFFLINE_PRIVATE_RECONCILIATION_ONLY
IMPLEMENTATION_IN_SCOPE=NO
AUTHORIZATION_ARTIFACT_IN_SCOPE=NO
VALIDATION_EXECUTION_IN_SCOPE=NO
CRM_TARGET_CREATION_IN_SCOPE=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NO_HIGHLEVEL_SEARCH=YES
NO_HIGHLEVEL_LIST=YES
NO_HIGHLEVEL_GET=YES
NO_HIGHLEVEL_PUT=YES

VALIDATION_EXECUTION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO
```

This unit resolves whether a **dedicated synthetic NON-ACCEPTANCE opportunity**
already exists, under governed private/local binding surfaces only, for the
merged PR #263 stage-provider validation design.

It is offline proof only. It does **not** call HighLevel, mutate CRM, create an
opportunity, choose a substitute CRM record, seal a validation package against
the acceptance target, issue authorization, or prepare a grant.

## 2. Controlling merged design

```text
PR263_MERGED=YES
PR263_MERGE_SHA=8a32e31eb12c69bb7eead8b1ded118041070c2c2
SOURCE_DESIGN=
  docs/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-design-001.md

VALIDATION_TARGET_CLASS_REQUIRED=
  SYNTHETIC_STAGE_CONTRACT_VALIDATION_OPPORTUNITY

DEDICATED_VALIDATION_OPPORTUNITY_REQUIRED=YES
FUTURE_ACCEPTANCE_OPPORTUNITY_AS_VALIDATION_TARGET=FORBIDDEN
GRANT008_OR_ACCEPTANCE_TARGET_REUSE=FORBIDDEN

PRIVATE_BINDING_SYMBOLS_REQUIRED=
  location_id
  contact_id
  opportunity_id
  pipeline_id
  validation_initial_stage_id
  validation_final_stage_id

PACKAGE_ID_DESIGNATED=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001

CALL_BUDGET_DESIGNATED=
  MAX_READS=2
  MAX_WRITES=1
  MAX_TOTAL_BUSINESS_CALLS=3

INVARIANT_SET_VERSION_DESIGNATED=
  NW008_STAGE_VALIDATION_INVARIANT_SET_V1
```

## 3. Inspection scope (private/local only)

Inspected offline, without printing raw IDs or CRM values:

| Surface | Role | Disposition for this unit |
| --- | --- | --- |
| `local/private/grant008_private_package.json` | Historical Grant 008 private package (gitignored) | Present; acceptance/historical AT-1 synthetic target lineage |
| `local/private/nw008-fresh-private-execution-package-001.json` | Fresh E2E/private execution package (gitignored) | Present; reuses Grant 008 **identity** fields for acceptance continuity |
| `local/private/nw008-fresh-private-binding-reconciliation-result-001.json` | Fresh package machine result | Present; public commitments already published under fresh reconciliation proof |
| `proof/nw008/nw-008-fresh-private-binding-reconciliation-001.md` | Public fresh binding proof | Documents acceptance-target continuity from Grant 008 identity fields |
| `proof/nw008/nw-008-at1-grant008-private-binding-reconciliation-pass-001.md` | Public Grant 008 binding proof | Historical acceptance/AT-1 package lineage |
| `local/private/*stage*provider*` / `*validation*package*` | Dedicated stage-provider validation package | **Absent** |
| HighLevel network | Live CRM | **Not contacted** |

```text
INSPECTED_PUBLIC_REPO_ONLY_PLUS_LOCAL_PRIVATE=YES
PRIVATE_PACKAGE_FILES_REMAIN_GITIGNORED=YES
RAW_IDS_READ_FOR_COMPARISON_ONLY=YES
RAW_IDS_PUBLISHED=NO
RAW_CRM_VALUES_PUBLISHED=NO
TOKEN_OR_PIT_PUBLISHED=NO
```

No other governed private package was found that declares a distinct stage-
provider validation opportunity.

## 4. Dedicated target determination (computed)

### 4.1 Required predicates

```text
DEDICATED_VALIDATION_OPPORTUNITY_READY=NO
VALIDATION_TARGET_SYNTHETIC=UNKNOWN
VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET=NO
```

Rationale:

1. PR #263 requires a **dedicated** synthetic opportunity of class
   `SYNTHETIC_STAGE_CONTRACT_VALIDATION_OPPORTUNITY`.
2. Existing private packages that bind an opportunity are:
   - Grant 008 private package
   - Fresh E2E private execution package
3. Those two packages bind the **same** `opportunity_id` (identity equality
   verified offline by fingerprint comparison; raw ID not published).
4. Fresh package construction authority explicitly copied Grant 008 identity
   fields for **acceptance / E2E target continuity**, not for a non-acceptance
   validation target.
5. No private file exists for
   `NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001`.
6. Reusing the Grant 008 / future E2E acceptance opportunity is **forbidden** by
   the controlling design.
7. This lane must **not** create a CRM opportunity, must **not** search
   HighLevel, and must **not** pick another existing CRM opportunity as a
   substitute.

Therefore a dedicated independently bound validation opportunity is **not
available**.

```text
ACCEPTANCE_OR_GRANT008_OPPORTUNITY_PRESENT_IN_PRIVATE_PACKAGES=YES
ACCEPTANCE_OR_GRANT008_OPPORTUNITY_REUSE_ALLOWED_FOR_STAGE_PROVIDER_VALIDATION=NO
INDEPENDENT_DEDICATED_VALIDATION_OPPORTUNITY_BOUND=NO
SUBSTITUTE_TARGET_SELECTION_PERFORMED=NO
CRM_OPPORTUNITY_CREATED_BY_THIS_UNIT=NO
HIGHLEVEL_SEARCH_FOR_SUBSTITUTE=NO
```

### 4.2 Private binding completeness against dedicated package

Because no dedicated validation package/target exists, dedicated binding
predicates are fail-closed **NO** (not satisfied for the required package):

```text
PRIVATE_LOCATION_BINDING_PRESENT=NO
PRIVATE_CONTACT_BINDING_PRESENT=NO
PRIVATE_OPPORTUNITY_BINDING_PRESENT=NO
PRIVATE_PIPELINE_BINDING_PRESENT=NO
PRIVATE_INITIAL_STAGE_BINDING_PRESENT=NO
PRIVATE_FINAL_STAGE_BINDING_PRESENT=NO

INITIAL_FINAL_STAGE_DISTINCT=NO
PRIVATE_BINDING_COMPLETE=NO
```

Notes:

- Historical acceptance packages do contain location/contact/opportunity/
  pipeline/stage fields for the **acceptance** target. Those fields are **not**
  counted as satisfying the dedicated validation package binding set.
- Counting them as YES would violate
  `VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET` and the design forbid on
  acceptance-target reuse.

## 5. Package seal status

```text
PACKAGE_ID=
  NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001

PRIVATE_VALIDATION_PACKAGE_SEALED=NO
PRIVATE_VALIDATION_PACKAGE_PATH=ABSENT
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO

VALIDATION_PACKAGE_DIGEST=
CALL_2_BODY_COMMITMENT=

LOCATION_FINGERPRINT=
CONTACT_FINGERPRINT=
OPPORTUNITY_FINGERPRINT=
PIPELINE_FINGERPRINT=
INITIAL_STAGE_FINGERPRINT=
FINAL_STAGE_FINGERPRINT=
```

Blank digests/fingerprints are intentional: no dedicated package was sealed, so
no validation-package commitments are published or implied.

### 5.1 Protocol binding (design-retained; not execution-ready)

The PR #263 protocol remains the designated shape for a **future** package once
a dedicated target exists. It is recorded here as design retention only:

```text
CALL_1_METHOD=GET
CALL_1_PATH=/opportunities/{private_opportunity_id}

CALL_2_METHOD=PUT
CALL_2_PATH=/opportunities/{private_opportunity_id}
CALL_2_BODY_EXACT=
  {"pipelineStageId":"<private_validation_final_stage_id>"}

CALL_3_METHOD=GET
CALL_3_PATH=/opportunities/{private_opportunity_id}

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
```

This unit does **not** bind those calls to any private opportunity ID.

## 6. Invariant proof contract (design-retained; not executed)

```text
INVARIANT_SET_VERSION=NW008_STAGE_VALIDATION_INVARIANT_SET_V1

INVARIANT_FIELDS=
  name
  status
  pipelineId
  monetaryValue
  assignedTo
  forecastExpectedCloseDate
  forecastProbability
  customFields

AUTHORIZED_CHANGED_FIELD=pipelineStageId

CANONICAL_JSON_SPEC=NW008_CANONICAL_JSON_V1
CANONICAL_JSON_RULES=
  UTF-8
  object keys sorted lexicographically
  no insignificant whitespace
  null distinct from absent
  array order preserved
  customFields array order preserved

INVARIANT_SET_PRE_SHA256=
INVARIANT_SET_POST_SHA256=
INVARIANT_FIELDS_UNCHANGED=
```

Invariant digests remain blank because no validation run and no sealed package
prestate capture occurred.

## 7. Grant-preparation result

```text
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO
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

Authorization/grant drafting is blocked until a dedicated synthetic
non-acceptance opportunity is independently bound outside this lane and a
subsequent private-package reconciliation can seal
`NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001`.

## 8. Explicit non-actions

```text
DID_NOT_CALL_HIGHLEVEL=YES
DID_NOT_SEARCH_LIST_GET_OR_PUT=YES
DID_NOT_MUTATE_CRM=YES
DID_NOT_CREATE_OPPORTUNITY=YES
DID_NOT_SELECT_SUBSTITUTE_EXISTING_CRM_OPPORTUNITY=YES
DID_NOT_REUSE_GRANT008_OR_ACCEPTANCE_OPPORTUNITY_AS_VALIDATION_TARGET=YES
DID_NOT_SEAL_VALIDATION_PACKAGE=YES
DID_NOT_PUBLISH_RAW_IDS=YES
DID_NOT_PUBLISH_RAW_CRM_VALUES=YES
DID_NOT_PUBLISH_TOKEN_OR_PIT=YES
DID_NOT_CREATE_AUTHORIZATION_OR_GRANT=YES
DID_NOT_AUTHORIZE_VALIDATION_EXECUTION=YES
DID_NOT_MUTATE_CONTRACTS_SRC_TESTS_WORKFLOWS_DEPLOY_IAM_SECRETS=YES
```

## 9. Decision summary

```text
DEDICATED_VALIDATION_OPPORTUNITY_READY=NO
VALIDATION_TARGET_SYNTHETIC=UNKNOWN
VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET=NO

PRIVATE_BINDING_COMPLETE=NO
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO
VALIDATION_PACKAGE_DIGEST=
CALL_2_BODY_COMMITMENT=
INVARIANT_SET_VERSION=NW008_STAGE_VALIDATION_INVARIANT_SET_V1

VALIDATION_AUTHORIZATION_PREPARATION_READY=NO
VALIDATION_EXECUTION_AUTHORIZED=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

SUBMISSION_READY=NO

STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_DEDICATED_TARGET_NOT_AVAILABLE

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
```

## 10. Required public return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PRIVATE_BINDING_RECONCILIATION_001

BASE_SHA=8a32e31eb12c69bb7eead8b1ded118041070c2c2

PR_NUMBER=EXTERNAL_METADATA
HEAD_SHA=EXTERNAL_METADATA

DEDICATED_VALIDATION_OPPORTUNITY_READY=NO
VALIDATION_TARGET_SYNTHETIC=UNKNOWN
VALIDATION_TARGET_DISTINCT_FROM_ACCEPTANCE_TARGET=NO

PRIVATE_BINDING_COMPLETE=NO
PRIVATE_VALIDATION_PACKAGE_RECONCILED=NO
VALIDATION_PACKAGE_DIGEST=

CALL_2_BODY_COMMITMENT=
INVARIANT_SET_VERSION=NW008_STAGE_VALIDATION_INVARIANT_SET_V1

VALIDATION_AUTHORIZATION_PREPARATION_READY=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

VALIDATION_EXECUTION_AUTHORIZED=NO
SUBMISSION_READY=NO

STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_DEDICATED_TARGET_NOT_AVAILABLE

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
```

`PR_NUMBER` and `HEAD_SHA` remain `EXTERNAL_METADATA` inside this durable
artifact. The proof PR return may populate concrete GitHub values separately for
governance handoff.

## 11. Governance handoff note

Required before authorization preparation can become ready:

1. Human/governance provisions a **dedicated** synthetic opportunity that is not
   the Grant 008 / future E2E acceptance opportunity.
2. Private bindings for location, contact, opportunity, pipeline, initial stage,
   and final stage are placed in a gitignored private package for
   `NW008_GHL_REST_V3_STAGE_PROVIDER_VALIDATION_PACKAGE_001`.
3. A subsequent offline reconciliation unit seals public-safe digests/fingerprints
   only and re-evaluates `DEDICATED_VALIDATION_OPPORTUNITY_READY`.

This unit stops fail-closed and does not perform those provisioning steps.
