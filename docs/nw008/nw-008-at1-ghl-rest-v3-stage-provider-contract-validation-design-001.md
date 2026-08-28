# NW-008 AT-1 — GHL REST v3 Stage Provider Contract Validation Design 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_DESIGN_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-design-001.md
PR_CLASS=planning_only
OWNER=VS_CODE_ORCHESTRATOR_GOVERNANCE_PROVIDER_CONTRACT_LANE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=9af28597af01c81ad8b4cde9fa43a816fcc150be
PLAN_BRANCH=
  plan/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-design-001
BRANCH_IS_MAIN=NO

IMPLEMENTATION_IN_SCOPE=NO
CONTRACT_FILE_MUTATION_IN_SCOPE=NO
RUNTIME_CODE_MUTATION_IN_SCOPE=NO
AUTHORIZATION_ARTIFACT_IN_SCOPE=NO
VALIDATION_EXECUTION_IN_SCOPE=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

VALIDATION_EXECUTION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO

NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO
```

This unit designs the **smallest fail-closed live provider validation** that can
resolve remaining HighLevel REST v3 stage-update runtime semantics after static
reconciliation. It is planning only.

It does **not**:

- implement `STAGE_PATH`
- mutate `contracts/**`, `src/**`, `tests/**`, or runtime surfaces
- create or issue an authorization artifact
- execute any REST/network/HighLevel call
- mutate CRM
- freeze a minimum stage body as already proven
- clear the stage-path blocker by assumption

Merging or reviewing this design confers no implementation, live-read,
live-mutation, validation-execution, or grant authority.

## 2. Controlling predecessor

```text
PR262_MERGED=YES
PR262_MERGE_SHA=9af28597af01c81ad8b4cde9fa43a816fcc150be
PR262_ARTIFACT=
  docs/nw008/nw-008-at1-ghl-rest-v3-stage-contract-reconciliation-001.md

PR261_MERGED=YES
PR261_MERGE_SHA=f4f1b73238a3106dd55cfe8a118c9ca04586fa0b
PR261_ARTIFACT=
  docs/nw008/nw-008-at1-ghl-transport-viability-kill-gate-001.md

COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3
MCP_COMPETITION_PATH=STOP

EXISTING_REST_ARCHITECTURE_PRESENT=YES
EXISTING_REST_ARCHITECTURE_ARTIFACT=
  docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
EXISTING_REST_CONTRACT_PRESENT=YES
EXISTING_REST_CONTRACT_ARTIFACT=
  contracts/highlevel_rest_adapter_v1.yaml

NOTE_PATH_ARCHITECTURE_READY=YES

STATIC_STAGE_CONTRACT_SUFFICIENT=NO
STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_BLOCKER=
  MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED

PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES
```

PR #262 reaffirmed the historical stage blocker after offline OpenAPI
reconciliation and required a **separate** provider-contract validation unit.
This design answers that requirement at the planning layer only.

## 3. Safety rules (binding)

```text
DO_NOT_INFER_PIPELINE_STAGE_ID_ONLY_FROM_EXAMPLE_BODY=YES
DO_NOT_ADD_UNRELATED_MUTABLE_FIELDS_MERELY_TO_SATISFY_PUT=YES
DO_NOT_TREAT_PUT_SUCCESS_AS_FINAL_STATE_VERIFICATION=YES

POST_UPDATE_EXACT_GET_REQUIRED=YES
PUT_RESPONSE_USED_AS_FINAL_VERIFICATION=NO

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_ALTERNATE_BODY=YES
NO_ALTERNATE_TARGET=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES

PUBLIC_OPPORTUNITY_ID=FORBIDDEN
PUBLIC_PIPELINE_ID=FORBIDDEN
PUBLIC_STAGE_IDS=FORBIDDEN
PUBLIC_RAW_INVARIANT_VALUES=NO

FUTURE_ACCEPTANCE_OPPORTUNITY_AS_VALIDATION_TARGET=FORBIDDEN
```

Fail-closed defaults:

- any prewrite mismatch → stop before write
- any hard HTTP failure on the single PUT → fail, no retry
- any ambiguous write delivery → fail ambiguous, no retry, no compensate
- any postwrite mismatch or invariant drift → validation fail; blocker retained
- unknown remains unknown until proven by this validation design’s future
  authorized execution

## 4. Normalize static findings (from PR #262)

Recorded offline findings carried forward. This design does **not** change them
by assumption.

```text
PIPELINE_STAGE_ID_DOCUMENTED=YES

PIPELINE_STAGE_ID_ONLY_BODY_SCHEMA_VALID=YES
PIPELINE_STAGE_ID_ONLY_BODY_RUNTIME_ACCEPTED=UNKNOWN

UNRELATED_MUTABLE_FIELDS_SCHEMA_REQUIRED=NO
UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=UNKNOWN

OMITTED_FIELDS_PRESERVED=UNKNOWN
UPDATE_RUNTIME_SEMANTICS_SAFE=UNKNOWN

RESPONSE_SELECTOR_PATHS_DOCUMENTED=YES
RESPONSE_SELECTOR_REQUIRED_PRESENCE_PROVEN=NO

PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO

MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO
MINIMUM_ALLOWED_STAGE_BODY=
```

Interpretation:

| Finding | Meaning for this design |
| --- | --- |
| `PIPELINE_STAGE_ID_ONLY_BODY_SCHEMA_VALID=YES` | OpenAPI documents `pipelineStageId` and does not schema-require sibling fields; a stage-only body is schema-admissible to attempt under validation |
| `PIPELINE_STAGE_ID_ONLY_BODY_RUNTIME_ACCEPTED=UNKNOWN` | Runtime acceptance is the primary unknown this validation is designed to resolve |
| `UNRELATED_MUTABLE_FIELDS_SCHEMA_REQUIRED=NO` | Schema does not force unrelated mutable fields |
| `UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=UNKNOWN` | Runtime may still reject stage-only bodies; validation must not invent replay fields |
| `OMITTED_FIELDS_PRESERVED=UNKNOWN` | Partial vs replacement semantics unresolved |
| `UPDATE_RUNTIME_SEMANTICS_SAFE=UNKNOWN` | Safety of stage-only mutation unresolved until invariant-preserving proof |
| contracts frozen flags `NO` | Validation may observe runtime facts; freeze of production STAGE_PATH contracts remains a later architecture step after PASS |

Blank `MINIMUM_ALLOWED_STAGE_BODY` remains intentional until a future authorized
validation run produces PASS evidence and a subsequent architecture freeze unit
consumes it.

## 5. Provider authority (immutable pin)

```text
PROVIDER=HighLevel
API_FAMILY=REST
API_VERSION_HEADER=v3
OPENAPI_DOCUMENT_TITLE=Opportunities API v3

AUTHORITY_SOURCE_KIND=OFFICIAL_PROVIDER_OPENAPI
AUTHORITY_REPO=GoHighLevel/highlevel-api-docs
AUTHORITY_PATH=apps/v3/opportunities-v3.json

AUTHORITY_COMMIT=f0da4f8054b6aeee18482afe0079a0259a72b569
AUTHORITY_IMMUTABLE_LOCATOR=
  https://github.com/GoHighLevel/highlevel-api-docs/blob/f0da4f8054b6aeee18482afe0079a0259a72b569/apps/v3/opportunities-v3.json

AUTHORITY_CONTENT_SHA=dd13c44c4bbd1f282f574e0e9537bdfe7b42d4a5
AUTHORITY_SHA256=
  f7d5b0af7ca6cc283430742093217fa254bfbc3ec01f049264a23a43c5339aef

UPDATE_OPPORTUNITY_METHOD=PUT
UPDATE_OPPORTUNITY_PATH=/opportunities/{opportunityId}
OPENAPI_PATH_TEMPLATE=/opportunities/{id}
OPENAPI_OPERATION_ID=update-opportunity
OPENAPI_REQUEST_SCHEMA=UpdateOpportunityDtoV3

GET_OPPORTUNITY_METHOD=GET
GET_OPPORTUNITY_PATH=/opportunities/{opportunityId}
OPENAPI_GET_OPERATION_ID=get-opportunity
GET_SUCCESS_ENVELOPE_PROPERTY=opportunity
```

Durable source fields MUST use the immutable commit locator above. Do **not**
treat `/blob/main/...` as durable authority for this unit.

Out-of-scope endpoints remain forbidden for this validation:

```text
NOT_SELECTED=POST /opportunities/
NOT_SELECTED=POST /opportunities/upsert
NOT_SELECTED=PUT /opportunities/{id}/status
NOT_SELECTED=GET /opportunities/search
NOT_SELECTED=POST /opportunities/search
NOT_SELECTED=GET /opportunities/pipelines
NOT_SELECTED=ANY_SEARCH_LIST_OR_PAGINATED_SURFACE
```

## 6. Validation purpose and non-purpose

### 6.1 Purpose

Resolve, with the smallest possible live surface, whether a stage-only PUT body
is runtime-accepted **and** preserves non-stage fields on a dedicated private
synthetic opportunity:

```text
INTENDED_CHANGED_FIELD=pipelineStageId
INTENDED_VALIDATION_BODY_SHAPE=
  {"pipelineStageId":"<private_validation_final_stage_id>"}

QUESTIONS_TO_RESOLVE=
  1. Does the provider accept the exact stage-only body at runtime?
  2. Does a single stage-only PUT leave the bounded invariant field set unchanged?
  3. Does postwrite exact GET show the authorized final stage on the same
     opportunity and pipeline?
```

Only a full PASS may later support:

```text
STAGE_ONLY_BODY_RUNTIME_ACCEPTED=YES
VALIDATED_OMITTED_FIELDS_PRESERVED=YES
UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=NO
UPDATE_RUNTIME_SEMANTICS_SAFE=YES
PROVIDER_STAGE_CONTRACT_VALIDATION=PASS
```

Those outcomes are **not** claimed by this design unit.

### 6.2 Non-purpose

```text
NOT_A_STAGE_PATH_IMPLEMENTATION=YES
NOT_A_PRODUCTION_CONTRACT_FREEZE=YES
NOT_AN_ACCEPTANCE_RUN=YES
NOT_A_GRANT=YES
NOT_A_RETRY_HARNESS=YES
NOT_A_MULTI_BODY_EXPERIMENT=YES
NOT_A_PUBLIC_ID_DISCLOSURE=YES
NOT_A_CLEANUP_OR_RESTORE_JOB=YES
```

This validation is intentionally narrower than full `STAGE_PATH` architecture
readiness. PASS evidence feeds a later freeze/architecture unit; it does not
itself mark `STAGE_PATH_ARCHITECTURE_READY=YES`.

## 7. Validation target class

```text
VALIDATION_TARGET_CLASS=
  SYNTHETIC_STAGE_CONTRACT_VALIDATION_OPPORTUNITY

PRIVATE_BINDING_REQUIRED=YES
SYNTHETIC_ONLY=YES
EXACT_ID_TARGETING_REQUIRED=YES

PUBLIC_OPPORTUNITY_ID=FORBIDDEN
PUBLIC_PIPELINE_ID=FORBIDDEN
PUBLIC_STAGE_IDS=FORBIDDEN

USE_FUTURE_ACCEPTANCE_OPPORTUNITY=NO
USE_NOTE_PATH_CONTACT_AS_MUTATION_TARGET=NO
USE_SEARCH_TO_DISCOVER_TARGET=NO
```

### 7.1 Private binding set (names only; values never published here)

A future authorization/execution packet must bind privately, out of public PR
text:

```text
PRIVATE_BINDING_SYMBOLS=
  location_id
  contact_id
  opportunity_id
  pipeline_id
  validation_initial_stage_id
  validation_final_stage_id
```

Binding rules:

```text
location_id=
  private location that owns the synthetic validation opportunity
contact_id=
  required when relationship validation is authoritative/available on GET
opportunity_id=
  dedicated synthetic validation opportunity; not the future acceptance
  opportunity; not any real-customer opportunity
pipeline_id=
  exact pipeline expected on that opportunity
validation_initial_stage_id=
  exact stage that must be observed on prewrite GET before mutation
validation_final_stage_id=
  exact distinct authorized stage for the single PUT body
  MUST differ from validation_initial_stage_id
```

```text
INITIAL_AND_FINAL_STAGE_MUST_DIFFER=YES
DEDICATED_VALIDATION_OPPORTUNITY_REQUIRED=YES
SHARED_ACCEPTANCE_TARGET_FORBIDDEN=YES
```

No raw CRM identifiers, tokens, or field values appear in this artifact.

### 7.2 Target lifecycle expectations (design only)

```text
TARGET_PRECREATED_OUTSIDE_THIS_VALIDATION=YES
VALIDATION_DOES_NOT_CREATE_OPPORTUNITY=YES
VALIDATION_DOES_NOT_DELETE_OPPORTUNITY=YES
VALIDATION_DOES_NOT_AUTO_RESTORE_INITIAL_STAGE=YES
NO_AUTOMATIC_CLEANUP=YES
```

If post-validation restore is ever desired, it requires a **separate** explicit
authorization and is outside this three-call budget. This design forbids
compensating mutation inside the validation run.

## 8. Exact validation protocol

### 8.1 Call budget

```text
CALL_1=GET /opportunities/{private_validation_opportunity_id}
CALL_2=PUT /opportunities/{private_validation_opportunity_id}
CALL_3=GET /opportunities/{private_validation_opportunity_id}

MAX_READS=2
MAX_WRITES=1
MAX_TOTAL_BUSINESS_CALLS=3

VALIDATION_CALL_BUDGET=3
VALIDATION_WRITE_BUDGET=1

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_ALTERNATE_BODY=YES
NO_ALTERNATE_TARGET=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES
```

Exactly these three business calls. Zero additional provider probes.

### 8.2 CALL_1 — prewrite exact GET

```text
METHOD=GET
PATH=/opportunities/{private_validation_opportunity_id}
PURPOSE=PREWRITE_STATE_CAPTURE_AND_GATE
```

Required prewrite predicates (all must be YES or the run stops before write):

```text
EXACT_OPPORTUNITY_ID_MATCH=YES
EXACT_PIPELINE_ID_MATCH=YES
EXACT_INITIAL_STAGE_MATCH=YES
```

If authoritative/available on the GET payload:

```text
EXACT_CONTACT_ID_MATCH=YES
EXACT_LOCATION_ID_MATCH=YES
```

Selector candidates (consume-minimized; not a production freeze):

```text
PREWRITE_SELECTORS=
  opportunity.id
  opportunity.pipelineId
  opportunity.pipelineStageId
  opportunity.contactId
  opportunity.locationId
```

```text
STOP_BEFORE_WRITE_ON_ANY_MISMATCH=YES
STOP_BEFORE_WRITE_ON_MISSING_REQUIRED_SELECTOR=YES
STOP_BEFORE_WRITE_ON_TRANSPORT_FAILURE=YES
```

On any prewrite stop:

```text
CALL_2_EXECUTED=NO
PROVIDER_STAGE_CONTRACT_VALIDATION=FAIL
STAGE_PATH_BLOCKER_CLEARED=NO
```

### 8.3 CALL_2 — single stage-only PUT

```text
METHOD=PUT
PATH=/opportunities/{private_validation_opportunity_id}
CONTENT_TYPE=application/json

CALL_2_BODY_EXACT=
  {"pipelineStageId":"<private_validation_final_stage_id>"}

ALTERNATE_BODY_FORBIDDEN=YES
FIELD_REPLAY_FORBIDDEN=YES
BODY_EXPANSION_FORBIDDEN=YES
```

The body contains exactly one property: `pipelineStageId`, set to the privately
bound final validation stage ID. No `name`, `status`, `pipelineId`,
`monetaryValue`, `assignedTo`, forecast fields, or `customFields` may be added
to “make PUT work.”

```text
PUT_ATTEMPTS_MAX=1
PUT_RESPONSE_USED_AS_FINAL_VERIFICATION=NO
PUT_RESPONSE_ROLE=TRANSPORT_EVIDENCE_ONLY
```

### 8.4 CALL_3 — postwrite exact GET

```text
METHOD=GET
PATH=/opportunities/{private_validation_opportunity_id}
PURPOSE=POSTWRITE_STATE_VERIFICATION
REQUIRED_AFTER_NON_AMBIGUOUS_PUT=YES
```

CALL_3 is mandatory after a PUT that is not classified as
`FAIL_AMBIGUOUS_WRITE` transport failure before any request could have been
delivered. If PUT fails with a definitive provider error response
(400/401/403/404/409/422), CALL_3 is still allowed only as optional forensic
read under a future authorization packet’s explicit rule; **this design’s
default PASS path requires CALL_3 after a non-error PUT completion**. For the
minimum budgeted PASS protocol:

```text
PASS_PATH_REQUIRES_CALL_3=YES
```

Postwrite predicates (all must be YES for PASS):

```text
POST_EXACT_OPPORTUNITY_ID_MATCH=YES
POST_EXACT_PIPELINE_ID_MATCH=YES
POST_FINAL_STAGE_MATCH=YES
INVARIANT_FIELDS_UNCHANGED=YES
```

## 9. Invariant-field proof design

### 9.1 Purpose

Prove that the stage-only mutation did not alter non-stage business fields
returned by GET, without publishing raw CRM values.

### 9.2 Canonical candidate invariant set

Fields drawn from GET opportunity object candidates that must not change as a
result of the authorized stage-only mutation:

```text
INVARIANT_CANDIDATE_FIELDS=
  name
  status
  pipelineId
  monetaryValue
  assignedTo
  forecastExpectedCloseDate
  forecastProbability
  customFields
```

```text
INVARIANT_EXCLUDED_FIELDS=
  pipelineStageId
```

`pipelineStageId` is excluded from the invariant digest because it is the one
authorized changed field. `id` is enforced by exact match predicates rather than
invariant digest membership. Nested PII-heavy objects (for example full nested
`contact`) are not added to the invariant set.

### 9.3 Digest commitments (values never published)

A future execution packet records only:

```text
INVARIANT_SET_VERSION=NW008_STAGE_VALIDATION_INVARIANT_SET_V1
INVARIANT_SET_PRE_SHA256=<sha256 over canonical prewrite invariant subset>
INVARIANT_SET_POST_SHA256=<sha256 over canonical postwrite invariant subset>
INVARIANT_FIELDS_UNCHANGED=YES|NO
```

Canonicalization rules for the future executor (design constraints):

```text
CANONICAL_JSON=UTF8_UTF8_SORT_KEYS_NO_INSIGNIFICANT_WHITESPACE
MISSING_FIELD_TOKEN=FIELD_ABSENT
NULL_DISTINCT_FROM_ABSENT=YES
ARRAY_ORDER_PRESERVED_FOR_CUSTOMFIELDS=YES
RAW_VALUES_IN_PUBLIC_ARTIFACTS=FORBIDDEN
RAW_VALUES_IN_PR_TEXT=FORBIDDEN
```

```text
INVARIANT_SET_DEFINED=YES
PUBLIC_RAW_INVARIANT_VALUES=NO
```

`INVARIANT_FIELDS_UNCHANGED=YES` only if pre and post digests are identical and
no invariant candidate present prewrite is absent postwrite with a divergent
semantic (executor must treat digest inequality as fail-closed `NO`).

### 9.4 pipelineId double-bind

`pipelineId` appears both in exact match predicates and in the invariant set.
That is intentional:

- exact match enforces authorized pipeline binding
- invariant digest detects unexpected pipeline drift encoded among sibling fields

## 10. PUT handling matrix

Exactly one PUT attempt.

| Outcome class | HTTP / transport signal | Result | Retry | Compensate | CALL_3 |
| --- | --- | --- | --- | --- | --- |
| Definitive client/provider rejection | 400, 401, 403, 404, 409, 422 | `FAIL` | NO | NO | NOT required for FAIL disposition |
| Definitive success transport | 2xx with completed response | continue to CALL_3 | NO | NO | YES required |
| Ambiguous delivery | timeout, disconnect, unknown whether applied | `FAIL_AMBIGUOUS_WRITE` | NO | NO | NO automatic; no compensate |
| Other unexpected status | any non-listed status | `FAIL` | NO | NO | fail-closed |

```text
PUT_ATTEMPTS_MAX=1
NO_RETRY=YES
NO_COMPENSATING_MUTATION=YES
NO_ALTERNATE_BODY_ON_REJECTION=YES

ON_HTTP_400_401_403_404_409_422=FAIL
ON_TIMEOUT_DISCONNECT_AMBIGUOUS_DELIVERY=FAIL_AMBIGUOUS_WRITE

PUT_RESPONSE_USED_AS_FINAL_VERIFICATION=NO
PUT_RESPONSE_ROLE=TRANSPORT_EVIDENCE_ONLY
```

Ambiguous write is poison: the run may not “fix” with a second PUT, may not
guess restore, and may not declare omitted-field preservation.

## 11. PASS / FAIL disposition

### 11.1 PASS (all required)

```text
PREWRITE_GATES=PASS
PUT_TRANSPORT=NON_AMBIGUOUS_SUCCESS
POST_EXACT_OPPORTUNITY_ID_MATCH=YES
POST_EXACT_PIPELINE_ID_MATCH=YES
POST_FINAL_STAGE_MATCH=YES
INVARIANT_FIELDS_UNCHANGED=YES
```

Only then may a future execution result packet record:

```text
STAGE_ONLY_BODY_RUNTIME_ACCEPTED=YES
VALIDATED_OMITTED_FIELDS_PRESERVED=YES
UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=NO
UPDATE_RUNTIME_SEMANTICS_SAFE=YES
PROVIDER_STAGE_CONTRACT_VALIDATION=PASS
```

Even after PASS:

```text
STAGE_PATH_ARCHITECTURE_READY remains NO until a later freeze/architecture unit
MINIMUM_ALLOWED_STAGE_BODY_FROZEN remains NO until that later unit freezes it
STAGE_PATH_IMPLEMENTATION remains unauthorized by this design
```

### 11.2 FAIL

Any of:

- prewrite mismatch / missing selector / prewrite transport failure
- definitive PUT rejection
- postwrite identity/pipeline/stage mismatch
- invariant digest inequality or invariant proof unavailable
- protocol deviation (extra call, alternate body, retry, search, cleanup)

```text
PROVIDER_STAGE_CONTRACT_VALIDATION=FAIL
STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO
```

### 11.3 FAIL_AMBIGUOUS_WRITE

```text
PROVIDER_STAGE_CONTRACT_VALIDATION=FAIL_AMBIGUOUS_WRITE
STAGE_PATH_BLOCKER_CLEARED=NO
NO_RETRY=YES
NO_COMPENSATING_MUTATION=YES
OMITTED_FIELDS_PRESERVED remains UNKNOWN
```

## 12. What PASS does and does not freeze

### 12.1 Evidence PASS may support later

```text
CANDIDATE_FUTURE_FREEZE_INPUTS=
  stage-only body runtime acceptance
  omitted-field preservation under invariant set V1
  unrelated mutable fields not runtime-required for this provider behavior
  postwrite exact GET as verification seam
```

### 12.2 Still required after PASS (separate units)

```text
STILL_REQUIRED_AFTER_PASS=
  authorization-consuming execution proof artifact
  architecture unit to freeze MINIMUM_ALLOWED_STAGE_BODY
  freeze PREWRITE_READ_CONTRACT / POSTWRITE_READBACK_CONTRACT for STAGE_PATH
  STAGE_PATH implementation authorization (if ever)
  live STAGE_PATH execution grant (if ever)
```

This design does not perform those steps.

## 13. Authority separation and next authorization

```text
THIS_ARTIFACT_DESIGNS_VALIDATION_ONLY=YES
IMPLEMENTATION_IN_SCOPE=NO
REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

VALIDATION_EXECUTION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
```

A separate authorization artifact is required before any live call:

```text
NEXT_AUTHORIZATION_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_AUTHORIZATION_001

NEXT_AUTHORIZATION_CLASS=governance_authorization
NEXT_AUTHORIZATION_MUST_BIND=
  private synthetic validation opportunity bindings
  call budget MAX_TOTAL_BUSINESS_CALLS=3
  exact CALL_2 body shape
  invariant set version
  no-retry / no-compensate / no-search rules
  one-shot consumption semantics
```

```text
DESIGN_DOES_NOT_ISSUE_AUTHORIZATION=YES
DESIGN_DOES_NOT_PREPARE_GRANT=YES
DESIGN_DOES_NOT_CREATE_governance/authorizations/**=YES
```

Suggested authorization sequencing (informative, not issued here):

1. Governance review of this design PR
2. `NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_AUTHORIZATION_001`
3. Private binding packet / execution packet (non-public IDs)
4. One-shot validation execution proof
5. Only on PASS: later architecture freeze unit for minimum body / selectors

## 14. Explicit non-actions of this unit

```text
DID_NOT_EXECUTE_VALIDATION=YES
DID_NOT_CALL_HIGHLEVEL=YES
DID_NOT_MUTATE_CRM=YES
DID_NOT_CLEAR_STAGE_PATH_BLOCKER=YES
DID_NOT_FREEZE_MINIMUM_ALLOWED_STAGE_BODY=YES
DID_NOT_IMPLEMENT_STAGE_PATH=YES
DID_NOT_MUTATE_CONTRACTS_OR_SRC=YES
DID_NOT_CREATE_AUTHORIZATION_ARTIFACT=YES
DID_NOT_PREPARE_GRANT=YES
DID_NOT_PUBLISH_PRIVATE_IDS_OR_RAW_FIELD_VALUES=YES
```

## 15. Decision summary

```text
PIPELINE_STAGE_ID_DOCUMENTED=YES
PIPELINE_STAGE_ID_ONLY_BODY_SCHEMA_VALID=YES
PIPELINE_STAGE_ID_ONLY_BODY_RUNTIME_ACCEPTED=UNKNOWN

UNRELATED_MUTABLE_FIELDS_SCHEMA_REQUIRED=NO
UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=UNKNOWN

OMITTED_FIELDS_PRESERVED=UNKNOWN
UPDATE_RUNTIME_SEMANTICS_SAFE=UNKNOWN

RESPONSE_SELECTOR_PATHS_DOCUMENTED=YES
RESPONSE_SELECTOR_REQUIRED_PRESENCE_PROVEN=NO
PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO
MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO

VALIDATION_TARGET_CLASS=
  SYNTHETIC_STAGE_CONTRACT_VALIDATION_OPPORTUNITY

VALIDATION_CALL_BUDGET=3
VALIDATION_WRITE_BUDGET=1
INVARIANT_SET_DEFINED=YES
PUBLIC_RAW_INVARIANT_VALUES=NO

VALIDATION_EXECUTION_AUTHORIZED=NO
PROVIDER_STAGE_CONTRACT_VALIDATION=NOT_EXECUTED

STATIC_STAGE_CONTRACT_SUFFICIENT=NO
STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO
PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES

COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3
NOTE_PATH_ARCHITECTURE_READY=YES

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO

NEXT_AUTHORIZATION_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_AUTHORIZATION_001

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW

STOP_CODE=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_DESIGN_001_COMPLETE_PLANNING_ONLY
```

## 16. Required return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_DESIGN_001

BASE_SHA=9af28597af01c81ad8b4cde9fa43a816fcc150be

PR_NUMBER=EXTERNAL_METADATA
HEAD_SHA=EXTERNAL_METADATA

PIPELINE_STAGE_ID_ONLY_BODY_SCHEMA_VALID=YES
PIPELINE_STAGE_ID_ONLY_BODY_RUNTIME_ACCEPTED=UNKNOWN

UNRELATED_MUTABLE_FIELDS_SCHEMA_REQUIRED=NO
UNRELATED_MUTABLE_FIELDS_RUNTIME_REQUIRED=UNKNOWN

OMITTED_FIELDS_PRESERVED=UNKNOWN
UPDATE_RUNTIME_SEMANTICS_SAFE=UNKNOWN

VALIDATION_TARGET_CLASS=
  SYNTHETIC_STAGE_CONTRACT_VALIDATION_OPPORTUNITY

VALIDATION_CALL_BUDGET=3
VALIDATION_WRITE_BUDGET=1

INVARIANT_SET_DEFINED=YES
PUBLIC_RAW_INVARIANT_VALUES=NO

VALIDATION_EXECUTION_AUTHORIZED=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW

STOP_CODE=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_DESIGN_001_COMPLETE_PLANNING_ONLY
```

`PR_NUMBER` and `HEAD_SHA` remain `EXTERNAL_METADATA` inside this durable
artifact. The planning PR return may populate their concrete GitHub values
separately for governance handoff. Return that PR to ChatGPT for governance
review before any authorization artifact, validation execution, REST call,
implementation, or grant preparation.
