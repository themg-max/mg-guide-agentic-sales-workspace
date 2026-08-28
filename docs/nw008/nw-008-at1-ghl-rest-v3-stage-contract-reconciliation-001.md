# NW-008 AT-1 — GHL REST v3 Stage Contract Reconciliation 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001
ARTIFACT_PATH=docs/nw008/nw-008-at1-ghl-rest-v3-stage-contract-reconciliation-001.md
PR_CLASS=planning_only
OWNER=VS_CODE_ORCHESTRATOR_GOVERNANCE_ARCHITECTURE_PROVIDER_CONTRACT_LANE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=f4f1b73238a3106dd55cfe8a118c9ca04586fa0b
PLAN_BRANCH=plan/nw008-at1-ghl-rest-v3-stage-contract-reconciliation-001
BRANCH_IS_MAIN=NO

IMPLEMENTATION_IN_SCOPE=NO
CONTRACT_FILE_MUTATION_IN_SCOPE=NO
RUNTIME_CODE_MUTATION_IN_SCOPE=NO

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO
```

This unit reconciles **current authoritative HighLevel REST v3**
`Get Opportunity` and `Update Opportunity` contracts against the historical
stage-path blocker:

```text
STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

It is offline planning only. It does not implement STAGE_PATH, mutate
`contracts/**` or `src/**`, issue any HighLevel request, probe credentials, or
prepare a grant.

Merging or reviewing this reconciliation confers no implementation, live-read,
live-mutation, or grant authority.

## 2. Controlling predecessor

```text
PR261_MERGED=YES
PR261_MERGE_SHA=f4f1b73238a3106dd55cfe8a118c9ca04586fa0b
PR261_ARTIFACT=docs/nw008/nw-008-at1-ghl-transport-viability-kill-gate-001.md

MCP_COMPETITION_PATH=STOP
COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3

EXISTING_REST_ARCHITECTURE_PRESENT=YES
EXISTING_REST_ARCHITECTURE_ARTIFACT=
  docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
EXISTING_REST_CONTRACT_PRESENT=YES
EXISTING_REST_CONTRACT_ARTIFACT=
  contracts/highlevel_rest_adapter_v1.yaml

NOTE_PATH_ARCHITECTURE_READY=YES

STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_BLOCKER=
MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED

REST_STAGE_PATH_REVALIDATION_REQUIRED=YES
```

PR #261 stopped competition MCP transport and selected bounded HighLevel REST
v3. It required this unit to revalidate the historical stage blocker against
current provider authority without silently clearing it.

## 3. Safety rules applied

The following rules are binding for this reconciliation and any later stage-path
work:

```text
DO_NOT_INFER_PIPELINE_STAGE_ID_ONLY_FROM_EXAMPLE_BODY=YES
DO_NOT_ADD_UNRELATED_MUTABLE_FIELDS_MERELY_TO_SATISFY_PUT=YES
DO_NOT_TREAT_PUT_SUCCESS_AS_FINAL_STATE_VERIFICATION=YES

POST_UPDATE_EXACT_GET_REQUIRED=YES
PUT_RESPONSE_USED_AS_FINAL_VERIFICATION=NO

NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_ALTERNATE_TARGET=YES
NO_COMPENSATING_MUTATION=YES
```

Absence of OpenAPI `required` markers is **not** affirmative proof that a
`pipelineStageId`-only body is runtime-valid. Third-party summaries that claim
`pipelineId` / `name` / `status` are required are **not** elevated over the
provider OpenAPI document, and they also do **not** authorize replaying those
fields without a frozen minimum-body decision.

## 4. Authoritative provider sources (offline)

### 4.1 Selected authority

```text
PROVIDER=HighLevel
API_FAMILY=REST
API_VERSION_HEADER=v3
OPENAPI_DOCUMENT_TITLE=Opportunities API v3
OPENAPI_DOCUMENT_VERSION=v3
OPENAPI_SPEC_VERSION=3.0.0

AUTHORITY_SOURCE_KIND=OFFICIAL_PROVIDER_OPENAPI
AUTHORITY_REPO=GoHighLevel/highlevel-api-docs
AUTHORITY_PATH=apps/v3/opportunities-v3.json
AUTHORITY_HTML_URL=
  https://github.com/GoHighLevel/highlevel-api-docs/blob/main/apps/v3/opportunities-v3.json
AUTHORITY_GITHUB_CONTENT_SHA=dd13c44c4bbd1f282f574e0e9537bdfe7b42d4a5
AUTHORITY_PATH_LAST_COMMIT_SHA=f0da4f8054b6aeee18482afe0079a0259a72b569
AUTHORITY_PATH_LAST_COMMIT_DATE_UTC=2026-06-19T09:21:21Z
AUTHORITY_BYTES=73037
AUTHORITY_SHA256=
  f7d5b0af7ca6cc283430742093217fa254bfbc3ec01f049264a23a43c5339aef

MARKETPLACE_UPDATE_DOC_URL=
  https://marketplace.gohighlevel.com/docs/ghl/opportunities/update-opportunity/
MARKETPLACE_GET_DOC_URL=
  https://marketplace.gohighlevel.com/docs/ghl/opportunities/get-opportunity/
```

The OpenAPI file is treated as the primary machine-readable provider authority
for endpoint identity, DTO property names, and documented response envelope
shape. Marketplace HTML pages were cross-checked and list the same update-body
property names; they do not add explicit partial-vs-replacement semantics or a
frozen minimum stage-only body.

No HighLevel business endpoint was called. No credential was used.

### 4.2 Non-authority / secondary evidence (not used to clear the blocker)

| Source | Role | Disposition |
| --- | --- | --- |
| `contracts/highlevel_rest_adapter_v1.yaml` | Local NW008 architecture contract | Records unresolved minimum body; not provider authority |
| `docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md` | Local architecture | Defines intended protocol and blocker |
| `proof/phase2/operations/op-update-opportunity.json` | Historical MCP/operation catalog extract | Secondary; body fields marked `required: false`; not sufficient to freeze runtime minimum body |
| Unofficial web summaries claiming four required PUT fields | Third-party paraphrase | **Rejected** as authority; conflicts with OpenAPI `required` absence and must not force field replay |

## 5. Endpoint identity reconciliation

```text
UPDATE_OPPORTUNITY_METHOD=PUT
UPDATE_OPPORTUNITY_PATH=/opportunities/{opportunityId}

OPENAPI_PATH_TEMPLATE=/opportunities/{id}
OPENAPI_OPERATION_ID=update-opportunity
OPENAPI_REQUEST_CONTENT_TYPE=application/json
OPENAPI_REQUEST_BODY_REQUIRED=YES
OPENAPI_REQUEST_SCHEMA=UpdateOpportunityDtoV3
OPENAPI_SUCCESS_RESPONSE_SCHEMA=GetPostOpportunitySuccessfulResponseDto

GET_OPPORTUNITY_METHOD=GET
GET_OPPORTUNITY_PATH=/opportunities/{opportunityId}
OPENAPI_GET_OPERATION_ID=get-opportunity
OPENAPI_GET_SUCCESS_RESPONSE_SCHEMA=GetPostOpportunitySuccessfulResponseDto
```

Path parameter naming `{id}` vs local `{opportunityId}` is template-label only.
The bounded adapter continues to inject the private opportunity ID; callers
still may not supply path IDs.

```text
UPDATE_ENDPOINT_AUTHORITY_IDENTIFIED=YES
```

Out-of-scope adjacent endpoints (explicitly **not** selected for STAGE_PATH):

```text
NOT_SELECTED=POST /opportunities/
NOT_SELECTED=POST /opportunities/upsert
NOT_SELECTED=PUT /opportunities/{id}/status
NOT_SELECTED=GET /opportunities/search
NOT_SELECTED=POST /opportunities/search
NOT_SELECTED=GET /opportunities/pipelines
```

## 6. Update Opportunity body contract findings

### 6.1 Documented DTO properties (`UpdateOpportunityDtoV3`)

| Property | OpenAPI type | In `required[]` | Notes |
| --- | --- | --- | --- |
| `pipelineId` | string | **absent** | Documented; not schema-required |
| `name` | string | **absent** | Documented; architecture forbids intended mutation |
| `pipelineStageId` | string | **absent** | Documented stage identifier |
| `status` | string enum `open\|won\|lost\|abandoned\|all` | **absent** | Documented; architecture forbids intended mutation |
| `monetaryValue` | number | **absent** | Architecture forbids intended mutation |
| `forecastExpectedCloseDate` | string | **absent** | Architecture forbids intended mutation |
| `forecastProbability` | number | **absent** | Architecture forbids intended mutation |
| `assignedTo` | string | **absent** | Architecture forbids intended mutation |
| `customFields` | array | **absent** | Architecture forbids intended mutation |

```text
PIPELINE_STAGE_ID_DOCUMENTED=YES
UPDATE_DTO_REQUIRED_ARRAY_PRESENT=NO
UPDATE_DTO_REQUIRED_ARRAY=NONE
OPENAPI_ADDITIONAL_PROPERTIES_EXPLICIT=NO
```

### 6.2 Stage-only body question

Historical intended body:

```text
INTENDED_CHANGED_FIELD=pipelineStageId
INTENDED_BODY_SHAPE={ "pipelineStageId": "<authorized_final_stage_id>" }
```

Authoritative support assessment:

```text
PIPELINE_STAGE_ID_ONLY_BODY_AUTHORITATIVELY_SUPPORTED=UNKNOWN
```

Rationale:

1. OpenAPI documents `pipelineStageId` and does **not** mark any sibling field
   as schema-required.
2. OpenAPI still requires **a** JSON request body (`requestBody.required=true`)
   without defining the minimum non-empty property set for a stage-only change.
3. OpenAPI does **not** state that omitted properties are preserved (partial
   update) versus cleared or rejected (replacement / incomplete body).
4. Safety rule forbids inferring stage-only validity from examples that also
   show `pipelineId`, `name`, and `status`.
5. Safety rule forbids adding unrelated mutable fields merely to make PUT
   succeed.
6. No offline source provides a provider-owned normative sentence that
   “`pipelineStageId` alone is sufficient and safe for a stage transition.”
7. Conflicting unofficial summaries claim multiple required fields; even if
   true at runtime, that would **increase** lost-update risk under replacement
   semantics and still would not authorize silent replay without a frozen
   minimum-body architecture decision.

Therefore the minimum allowed stage body **cannot** be frozen from static
docs alone.

```text
MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO
MINIMUM_ALLOWED_STAGE_BODY=
```

Blank `MINIMUM_ALLOWED_STAGE_BODY` is intentional: unknown, not a wildcard.

### 6.3 Update semantics and lost-update risk

```text
UPDATE_SEMANTICS=UNKNOWN
UNRELATED_MUTABLE_FIELDS_REQUIRED=UNKNOWN
FRESH_STATE_FIELDS_MUST_BE_REPLAYED=UNKNOWN
LOST_UPDATE_RISK=UNKNOWN
UPDATE_SEMANTICS_SAFE_FOR_BOUNDED_STAGE_CHANGE=UNKNOWN
```

Interpretation under fail-closed governance:

- If runtime semantics are **partial**, a `pipelineStageId`-only body might be
  viable after separate validation — still unproven here.
- If runtime semantics are **replacement** (or “omit = clear/default”), sending
  only `pipelineStageId` could destroy name, status, money, assignment, or
  custom fields — unacceptable for competition CRM.
- If runtime **requires** replaying `name` / `status` / `pipelineId` without
  documenting partial safety, the architecture still forbids guessing those
  values and forbids treating PUT success as proof of unchanged siblings.

Local architecture already forbids intended modification of:

```text
monetaryValue
assignedTo
forecastExpectedCloseDate
forecastProbability
customFields
status
name
```

Those prohibitions remain. This unit does **not** enlarge the allowlist to
satisfy an unresolved PUT contract.

## 7. Get Opportunity response contract findings

### 7.1 Envelope

```text
GET_SUCCESS_ENVELOPE_SCHEMA=GetPostOpportunitySuccessfulResponseDto
GET_SUCCESS_ENVELOPE_PROPERTY=opportunity
GET_SUCCESS_ENVELOPE_REQUIRED_ARRAY=NONE
GET_OPPORTUNITY_OBJECT_SCHEMA=SearchOpportunitiesResponseSchema
```

Marketplace get-opportunity page likewise surfaces an `opportunity` object. The
OpenAPI example for the nested object is empty (`{}`), so examples are not
binding field-presence proofs.

### 7.2 Candidate binding/state fields (documented properties)

Documented on `SearchOpportunitiesResponseSchema` (none listed in a schema
`required[]`):

| Field | Relevance to bounded protocol |
| --- | --- |
| `id` | Exact opportunity identity check |
| `pipelineId` | Expected pipeline check |
| `pipelineStageId` | Initial-stage and final-stage checks |
| `contactId` | Contact relationship where present |
| `locationId` | Location relationship where present |
| `contact` (nested object) | Optional nested contact details; may include PII; not required for stage gate if `contactId` suffices |
| `status`, `name`, monetary/forecast fields | Must **not** be mutated by stage path; useful only if a future frozen body requires verified replay — currently unresolved |
| `notes`, `tasks`, `calendarEvents`, `followers`, `customFields` | Out of stage-path consume set; data-minimization continues to forbid full-response persistence |

```text
CANDIDATE_PREWRITE_SELECTORS=
  opportunity.id
  opportunity.pipelineId
  opportunity.pipelineStageId
  opportunity.contactId
  opportunity.locationId

CANDIDATE_POSTWRITE_SELECTORS=
  opportunity.id
  opportunity.pipelineId
  opportunity.pipelineStageId
```

### 7.3 Freeze status

Documented property names are **not** the same as a frozen NW008 response
contract. Missing pieces for freeze:

- no schema `required[]` proving always-present binding fields;
- empty nested example;
- no NW008 digest-bound composite response contract version;
- local REST contract still has `get_opportunity.architecture_ready=false` and
  does not define frozen selectors;
- PUT success response reuses the same envelope schema but **must not** replace
  post-update exact GET verification.

```text
GET_OPPORTUNITY_RESPONSE_CONTRACT_FROZEN=NO
UPDATE_OPPORTUNITY_RESPONSE_CONTRACT_FROZEN=NO
PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO
```

## 8. Required bounded STAGE_PATH protocol (preserved)

The intended protocol is preserved unchanged. It remains architecture-defined
and **not** implementation-authorized:

1. `GET` exact privately bound opportunity.
2. Verify exact opportunity ID.
3. Verify expected pipeline.
4. Verify expected initial stage.
5. Verify contact/location relationship only where authoritative schema
   supports it and the frozen consume set includes those fields.
6. Construct provider update body **internally** from verified state and the
   frozen minimum allowed stage body (not yet frozen).
7. `PUT` exactly once to the same exact opportunity.
8. `GET` the exact same opportunity again.
9. Verify exact pipeline and authorized final stage.

```text
POST_UPDATE_EXACT_GET_REQUIRED=YES
PUT_RESPONSE_USED_AS_FINAL_VERIFICATION=NO
STAGE_WRITE_ATTEMPTS_MAX=1
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
SEARCH_LIST_PAGINATION_ALTERNATE_TARGET=FORBIDDEN
```

## 9. Minimum body gate evaluation

Static closure may PASS only if all predicates are proven `YES`.

| Gate predicate | Value | Notes |
| --- | --- | --- |
| `UPDATE_ENDPOINT_AUTHORITY_IDENTIFIED` | **YES** | Official OpenAPI `PUT /opportunities/{id}` `update-opportunity` |
| `PIPELINE_STAGE_ID_DOCUMENTED` | **YES** | `UpdateOpportunityDtoV3.pipelineStageId` |
| `MINIMUM_ALLOWED_STAGE_BODY_FROZEN` | **NO** | Stage-only body not authoritatively proven; body left blank |
| `UNRELATED_MUTABLE_FIELDS_REQUIRED` | **UNKNOWN** | Cannot assert `NO` from docs alone |
| `UPDATE_SEMANTICS_SAFE_FOR_BOUNDED_STAGE_CHANGE` | **UNKNOWN** | Partial vs replacement undocumented |
| `PREWRITE_READ_CONTRACT_FROZEN` | **NO** | Candidate selectors only |
| `POSTWRITE_READBACK_CONTRACT_FROZEN` | **NO** | Post-GET required; contract not frozen |

Normalized gate block:

```text
UPDATE_ENDPOINT_AUTHORITY_IDENTIFIED=YES
PIPELINE_STAGE_ID_DOCUMENTED=YES
MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO
UNRELATED_MUTABLE_FIELDS_REQUIRED=UNKNOWN
UPDATE_SEMANTICS_SAFE_FOR_BOUNDED_STAGE_CHANGE=UNKNOWN
PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO
```

### 9.1 Gate result

Because one or more predicates are `NO` or `UNKNOWN`:

```text
STATIC_STAGE_CONTRACT_SUFFICIENT=NO
STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_BLOCKER=
MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES
```

The historical blocker is **reaffirmed**, not silently removed.

```text
NOTE_PATH_ARCHITECTURE_READY=YES
NOTE_PATH_UNCHANGED_BY_THIS_UNIT=YES
```

## 10. What remains blocked / what is newly known

### 10.1 Newly established (still offline)

```text
KNOWN_UPDATE_METHOD=PUT
KNOWN_UPDATE_PATH=/opportunities/{opportunityId}
KNOWN_UPDATE_DTO=UpdateOpportunityDtoV3
KNOWN_PIPELINE_STAGE_ID_PROPERTY=YES
KNOWN_GET_ENVELOPE=opportunity
KNOWN_CANDIDATE_STATE_FIELDS=
  id,pipelineId,pipelineStageId,contactId,locationId
KNOWN_OPENAPI_AUTHORITY_SHA256=
  f7d5b0af7ca6cc283430742093217fa254bfbc3ec01f049264a23a43c5339aef
```

### 10.2 Still unresolved (blocker content)

```text
UNRESOLVED_MINIMUM_VALID_STAGE_PUT_BODY=YES
UNRESOLVED_UPDATE_SEMANTICS_PARTIAL_VS_REPLACEMENT=YES
UNRESOLVED_WHETHER_NAME_STATUS_PIPELINEID_MUST_BE_PRESENT=YES
UNRESOLVED_FROZEN_PREWRITE_SELECTOR_SET=YES
UNRESOLVED_FROZEN_POSTWRITE_SELECTOR_SET=YES
UNRESOLVED_WHETHER_CONTACT_NESTED_OBJECT_REQUIRED_FOR_BINDING=YES
```

### 10.3 Explicit non-actions

```text
DID_NOT_CLEAR_STAGE_PATH_BLOCKER=YES
DID_NOT_MUTATE_contracts/highlevel_rest_adapter_v1.yaml=YES
DID_NOT_IMPLEMENT_STAGE_PATH=YES
DID_NOT_AUTHORIZE_PROVIDER_CONTRACT_VALIDATION_EXECUTION=YES
DID_NOT_AUTHORIZE_LIVE_READ_OR_MUTATION=YES
DID_NOT_PREPARE_GRANT=YES
```

`PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES` is a **planning finding**, not an
execution authorization. Any future validation unit requires separate
governance, synthetic-only exact-ID targets, private bindings, and an explicit
authorization artifact. This unit does not design or authorize that validation
run.

## 11. Decision summary

```text
PIPELINE_STAGE_ID_DOCUMENTED=YES
PIPELINE_STAGE_ID_ONLY_BODY_AUTHORITATIVELY_SUPPORTED=UNKNOWN
UPDATE_SEMANTICS=UNKNOWN
UNRELATED_MUTABLE_FIELDS_REQUIRED=UNKNOWN
MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO
PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO

STATIC_STAGE_CONTRACT_SUFFICIENT=NO
STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO
PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES

COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3
NOTE_PATH_ARCHITECTURE_READY=YES

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW
STOP_CODE=
  NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001_COMPLETE_OFFLINE_BLOCKER_RETAINED
```

## 12. Required return block

```text
ARTIFACT_ID=NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001

BASE_SHA=f4f1b73238a3106dd55cfe8a118c9ca04586fa0b
PR_NUMBER=
HEAD_SHA=

PIPELINE_STAGE_ID_DOCUMENTED=YES

PIPELINE_STAGE_ID_ONLY_BODY_AUTHORITATIVELY_SUPPORTED=UNKNOWN

UPDATE_SEMANTICS=UNKNOWN

UNRELATED_MUTABLE_FIELDS_REQUIRED=UNKNOWN

MINIMUM_ALLOWED_STAGE_BODY_FROZEN=NO

PREWRITE_READ_CONTRACT_FROZEN=NO
POSTWRITE_READBACK_CONTRACT_FROZEN=NO

STATIC_STAGE_CONTRACT_SUFFICIENT=NO

STAGE_PATH_BLOCKER_CLEARED=NO
STAGE_PATH_ARCHITECTURE_READY=NO

PROVIDER_CONTRACT_VALIDATION_REQUIRED=YES

REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO

NEXT=RETURN_PR_TO_CHATGPT_FOR_GOVERNANCE_REVIEW

STOP_CODE=
  NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001_COMPLETE_OFFLINE_BLOCKER_RETAINED
```

`PR_NUMBER` and `HEAD_SHA` are filled by the planning PR that carries this
artifact. Return that PR to ChatGPT for governance review before any
implementation, provider-contract validation execution, REST call, or grant
preparation.
