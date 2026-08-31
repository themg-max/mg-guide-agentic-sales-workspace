# MG Guide Agent Runtime — Bounded Live Provider End-to-End Validation Plan 001

This unit is PLANNING ONLY. It defines the next governed board
`BOUNDED_LIVE_PROVIDER_END_TO_END_VALIDATION` after Attempt 006 closeout.
It does not invoke GHL, mutate CRM, run Terraform, deploy, or create or
consume execution authority.

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_BOUNDED_LIVE_PROVIDER_E2E_VALIDATION_PLAN_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-bounded-live-provider-e2e-validation-plan-001.md
PR_CLASS=planning_only
MODE=LIVE_PROVIDER_E2E_VALIDATION_PLANNING_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T16:17:22Z

BRANCH=plan/mg-guide-bounded-live-provider-e2e-validation-001
BRANCH_IS_MAIN=NO
BASE_MAIN_SHA=78e77992ab07249b18007e9a980117d7421c3d12

NEXT_PHASE=BOUNDED_LIVE_PROVIDER_END_TO_END_VALIDATION
NEXT_PHASE_AUTHORIZED_NOW=NO
NEXT_PHASE_REQUIRES_NEW_AUTHORITY=YES

LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
GHL_CALLS_AUTHORIZED=NO
CRM_MUTATIONS_AUTHORIZED=NO
ATTEMPT_006_AUTHORITY_MAY_BE_REUSED=NO

EXECUTION_PERFORMED_IN_THIS_UNIT=NO
DEPLOYMENT_PERFORMED_IN_THIS_UNIT=NO
GHL_CALLS_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
```

## 1. Closed deployment binding

Attempt 006 is closed and must not be reused.

```text
CLOSED_DEPLOYMENT_ATTEMPT=MG_GUIDE_AGENT_RUNTIME_ATTEMPT_006
DEPLOYMENT_COMPLETION_PR=416
DEPLOYMENT_COMPLETION_MERGE_SHA=78e77992ab07249b18007e9a980117d7421c3d12

ATTEMPT_006_CLOSED=YES
ATTEMPT_006_AUTHORITY_CONSUMED=YES
ATTEMPT_006_AUTHORITY_REUSABLE=NO

REASONING_ENGINE_ID=5719342828341952512
REASONING_ENGINE_RESOURCE=
  projects/ai-rolodex-to-crm/locations/us-east1/reasoningEngines/5719342828341952512

DEPLOYMENT_ACCEPTANCE=PASS
FUNCTIONAL_RUNTIME_ACCEPTANCE=PASS
DEPLOYMENT_EXISTENCE_PROOF=PASS
```

Hosted synthetic `stream_query` already proved SequentialAgent execution
without live GHL. This plan is the next phase after that boundary.

## 2. End-to-end target

```text
INPUT=fixtures/transcript-success.txt
INPUT_CLASS=SYNTHETIC_APPROVED_FIXTURE
PRIVATE_CLIENT_OR_CUSTOMER_DATA=NO

ORCHESTRATION=
  meeting_context_agent
  -> relationship_context_agent
  -> follow_up_planning_agent

SERVING_OBJECT=AdkApp
ROOT_AGENT=SequentialAgent
RUNTIME=REASONING_ENGINE_5719342828341952512

PROVIDER=HighLevel REST v3
PROVIDER_CONTRACT=contracts/highlevel_rest_adapter_v1.yaml
CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM
SYNTHETIC_ONLY=YES
PRIVATE_ALLOWLIST_REQUIRED=YES
EXACT_ID_TARGETING_REQUIRED=YES
PRIVATE_BINDING_PUBLICATION=NO
```

Intended vertical slice: synthetic transcript into the already-deployed
Agent Runtime, then a separately authorized bounded HighLevel REST v3
note-path mutation and exact-ID readback. Stage-path mutation is part of
the intended full slice but remains gated by the existing architecture
blocker recorded in section 3.

## 3. Required provider operations

Exact operations from `contracts/highlevel_rest_adapter_v1.yaml`. Callers
may not supply IDs, query strings, or provider bodies. Private bindings
are not published in this plan.

### 3.1 get_contact

```text
OPERATION_NAME=get_contact
HTTP_METHOD_OR_PROVIDER_ACTION=GET /contacts/{contactId}
RESOURCE_TYPE=contact
INPUT_FIELDS=contactId from private_binding.contact_id only
EXPECTED_OUTPUT=contact.id and contact.locationId
MUTATION_OR_READ=READ
READBACK_REQUIRED=NO  (this is the preflight/readback primitive)
FAIL_CLOSED_BEHAVIOR=
  non-200, missing id, or locationId mismatch with private binding
  => GHL_TOOL_FAILURE or CONTACT_NOT_FOUND; no mutation
QUERY_ALLOWED=NO
SEARCH_ALLOWED=NO
RUNTIME_ENABLED_IN_CONTRACT=YES
IMPLEMENTATION_SLICE=NOTE_PATH
```

### 3.2 create_note

```text
OPERATION_NAME=create_note
HTTP_METHOD_OR_PROVIDER_ACTION=POST /contacts/{contactId}/notes
RESOURCE_TYPE=note
INPUT_FIELDS=
  contactId from private_binding.contact_id
  body only (internally constructed note_contract)
EXPECTED_OUTPUT=note.id, note.body, note.contactId
MUTATION_OR_READ=MUTATION
READBACK_REQUIRED=YES  (get_note by exact note.id)
FAIL_CLOSED_BEHAVIOR=
  non-200, missing note.id, or contactId mismatch
  => GHL_TOOL_FAILURE; no retry; no compensating mutation
ALLOWED_BODY_FIELDS=body
DENIED_BODY_FIELDS=userId, title, color, pinned
REQUIRED_CAPABILITY=AUTH_CAPABILITY_NOTE_CREATE
RUNTIME_ENABLED_IN_CONTRACT=YES
IMPLEMENTATION_SLICE=NOTE_PATH
```

### 3.3 get_note

```text
OPERATION_NAME=get_note
HTTP_METHOD_OR_PROVIDER_ACTION=GET /contacts/{contactId}/notes/{noteId}
RESOURCE_TYPE=note
INPUT_FIELDS=
  contactId from private_binding.contact_id
  noteId from same-run create_note response
EXPECTED_OUTPUT=
  note.id equals created note.id
  note.contactId equals private_binding.contact_id
  note.body digest equals adapter-internal expected digest
MUTATION_OR_READ=READ
READBACK_REQUIRED=YES  (this is the readback)
FAIL_CLOSED_BEHAVIOR=
  mismatch => GHL_WRITE_NOT_VERIFIED; no completion; no retry
RUNTIME_ENABLED_IN_CONTRACT=YES
IMPLEMENTATION_SLICE=NOTE_PATH
```

### 3.4 get_opportunity

```text
OPERATION_NAME=get_opportunity
HTTP_METHOD_OR_PROVIDER_ACTION=GET /opportunities/{opportunityId}
RESOURCE_TYPE=opportunity
INPUT_FIELDS=opportunityId from private_binding.opportunity_id only
EXPECTED_OUTPUT=
  identity plus current pipelineStageId for preflight/readback
MUTATION_OR_READ=READ
READBACK_REQUIRED=YES  (preflight and post-stage verify)
FAIL_CLOSED_BEHAVIOR=
  non-200, id mismatch, or stage != expected
  => OPPORTUNITY_NOT_FOUND or GHL_WRITE_NOT_VERIFIED; no mutation/retry
QUERY_ALLOWED=NO
SEARCH_ALLOWED=NO
IMPLEMENTATION_SLICE=STAGE_PATH
ARCHITECTURE_READY=NO
RUNTIME_ENABLED_IN_CONTRACT=NO
BLOCKED_BY=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

### 3.5 update_opportunity_stage

```text
OPERATION_NAME=update_opportunity_stage
HTTP_METHOD_OR_PROVIDER_ACTION=PUT /opportunities/{opportunityId}
RESOURCE_TYPE=opportunity
INPUT_FIELDS=
  opportunityId from private_binding.opportunity_id
  internally constructed body from fresh verified state
  intended changed field: pipelineStageId only
EXPECTED_OUTPUT=opportunity at authorized final stage
MUTATION_OR_READ=MUTATION
READBACK_REQUIRED=YES  (get_opportunity)
FAIL_CLOSED_BEHAVIOR=
  non-200 or stage mismatch => GHL_TOOL_FAILURE / GHL_WRITE_NOT_VERIFIED
  no retry, no compensating mutation
FORBIDDEN_FIELDS=
  monetaryValue, assignedTo, forecastExpectedCloseDate,
  forecastProbability, customFields, status, name
REQUIRED_CAPABILITY=AUTH_CAPABILITY_STAGE_UPDATE
IMPLEMENTATION_SLICE=STAGE_PATH
ARCHITECTURE_READY=NO
RUNTIME_ENABLED_IN_CONTRACT=NO
BLOCKED_BY=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

### 3.6 Forbidden operations

```text
FORBIDDEN_PROVIDER_OPERATIONS=
  contact_search
  contact_list
  opportunity_search
  opportunity_list
  note_list
  pagination
  batch
  arbitrary_url
  arbitrary_method
  generic_execute
  contact_create
  contact_delete
  opportunity_create
  opportunity_delete
  email_sms
  calendar_mutation
```

```text
REQUIRED_PROVIDER_OPERATIONS_DEFINED=YES
NOTE_PATH_OPERATIONS_EXECUTABLE_UNDER_LATER_AUTHORITY=YES
STAGE_PATH_OPERATIONS_EXECUTABLE_UNDER_LATER_AUTHORITY=NO
STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

A later authorization may cover note-path only until STAGE_PATH is frozen.
This plan does not clear the stage blocker.

## 4. Frozen test targets

Exact HighLevel location, contact, and opportunity IDs remain in the
private exact-ID allowlist. They are not published here.

```text
GHL_TARGET_ACCOUNT_OR_LOCATION=
  ACTIVE_CANONICAL_BUSINESS_CRM
  bound by private adapter infrastructure only
  ISOLATED_GHL_TEST_LOCATION=NO
GHL_TARGET_SCOPE_RESOLVED=YES
PRIVATE_BINDING_PUBLICATION=NO

TEST_CONTACT=
  privately allowlisted preverified synthetic contact
  exact-ID only; caller may not override
SYNTHETIC_CONTACT_READY=YES

TEST_OPPORTUNITY=
  privately allowlisted preverified synthetic opportunity
  exact-ID only; caller may not override
SYNTHETIC_OPPORTUNITY_READY=YES

EXPECTED_INITIAL_STAGE=discovery_scheduled
EXPECTED_INITIAL_STAGE_BOUND=YES
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ

AUTHORIZED_FINAL_STAGE=discovery_complete
AUTHORIZED_FINAL_STAGE_DEFINED=YES
AUTHORIZED_TRANSITION=discovery_scheduled -> discovery_complete
```

`EXPECTED_INITIAL_STAGE_VERIFIED` remains a fresh pre-execution exact-ID
read under later authority. This planning unit does not perform that read.

No private client or customer data is used. Input is
`fixtures/transcript-success.txt` plus the synthetic CRM fixture
`fixtures/ghl/relationship-context-crm.json` for the hosted graph side.

## 5. Mutation budget

Preserved frozen ceilings:

```text
MAX_CONTACT_MUTATIONS=0
MAX_NOTE_CREATIONS=1
MAX_OPPORTUNITY_STAGE_TRANSITIONS=1
MAX_TOTAL_GHL_MUTATIONS=2

NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1

NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_FALLBACK_OPERATION=YES
NO_AUTOMATIC_CLEANUP=YES
NO_COMPENSATING_MUTATION=YES

BROAD_SEARCH_AUTHORIZED=NO
LIST_PAGINATION_EXPANSION_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO

MUTATION_BUDGET_DEFINED=YES
```

Exact-ID reads (`get_contact`, `get_note`, `get_opportunity`) are not
mutations and are not search/list. They remain bounded to the private
allowlist.

Until STAGE_PATH is architecture-ready, an authorized first live slice
must cap at:

```text
FIRST_AUTHORIZABLE_SLICE=NOTE_PATH_ONLY
FIRST_SLICE_MAX_TOTAL_GHL_MUTATIONS=1
FIRST_SLICE_MAX_NOTE_CREATIONS=1
FIRST_SLICE_MAX_OPPORTUNITY_STAGE_TRANSITIONS=0
```

## 6. Success contract

Defined, not authorized:

```text
1. transcript accepted (synthetic fixture)
2. meeting context produced
3. relationship context produced
4. follow-up plan produced (intent-only until mutation authority)
5. bounded provider mutation executed (create_note; stage only if STAGE_PATH ready and separately authorized)
6. provider readback succeeds (get_note; get_opportunity if stage authorized)
7. expected final CRM state verified
8. audit/proof packet generated
```

Full-slice expected CRM end state, if both note-path and stage-path are
later authorized:

```text
NOTE_PRESENT=YES
NOTE_VERIFIED=YES
STAGE=discovery_complete
STAGE_VERIFIED=YES
EXTERNAL_EFFECTS=bounded mutations only, within budget
```

Note-path-only expected CRM end state, if that is the first authorized
slice:

```text
NOTE_PRESENT=YES
NOTE_VERIFIED=YES
STAGE=unchanged from verified initial stage
STAGE_MUTATION_ATTEMPTED=NO
```

This sequence is not authorized by this plan.

## 7. Failure contract

Default for every external provider call:

```text
NO_RETRY=YES
NO_ALTERNATE_OPERATION=YES
NO_COMPENSATING_MUTATION=YES
AUTHORITY_CONSUMED_ON_FIRST_DISPATCH=YES
CONSUMED_ON_ATTEMPT_NOT_SUCCESS=YES
```

| Call | Expected status | Acceptable shape | Fail-closed | Authority |
| --- | --- | --- | --- | --- |
| get_contact | 200 | `{contact:{id,locationId}}` matching private binding | stop; no mutation | if this is the first live dispatch under a later grant, consume |
| create_note | 201/200 | `{note:{id,body,contactId}}` | GHL_TOOL_FAILURE; no retry | consumed |
| get_note | 200 | id/contact/body digest match | GHL_WRITE_NOT_VERIFIED | already consumed |
| get_opportunity | 200 | identity + stage | OPPORTUNITY_NOT_FOUND / GHL_WRITE_NOT_VERIFIED | consume if first dispatch |
| update_opportunity_stage | 200 | pipelineStageId == authorized final | GHL_TOOL_FAILURE | consumed |

Orchestration fail-closed codes remain:

```text
AMBIGUOUS_CONTACT
CONTACT_NOT_FOUND
OPPORTUNITY_NOT_FOUND
LOW_EXTRACTION_CONFIDENCE
STAGE_TRANSITION_NOT_ALLOWED
GHL_TOOL_FAILURE
GHL_WRITE_NOT_VERIFIED
NOTE_WRITE_BLOCKED
```

Ambiguous contact, missing opportunity, or low extraction confidence must
yield **zero** provider mutations.

```text
FAIL_CLOSED_CONTRACT_DEFINED=YES
```

## 8. Authority boundary

```text
LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
GHL_CALLS_AUTHORIZED=NO
CRM_MUTATIONS_AUTHORIZED=NO
REST_ADAPTER_EXECUTION_AUTHORIZED=NO
NEW_DEPLOYMENT_AUTHORITY=NOT_GRANTED

ATTEMPT_006_AUTHORITY_MAY_BE_REUSED=NO
ATTEMPT_006_CLOSED=YES

NEXT_PHASE=BOUNDED_LIVE_PROVIDER_END_TO_END_VALIDATION
NEXT_PHASE_AUTHORIZED_NOW=NO
NEXT_PHASE_REQUIRES_NEW_AUTHORITY=YES
```

A later separate authorization / activation / consumption chain is
required. That chain must bind:

- this plan
- `REASONING_ENGINE_ID=5719342828341952512`
- private exact-ID allowlist
- exact operation list
- exact mutation budget
- one-shot consume-on-dispatch semantics

This plan grants none of that.

## 9. Canonical validation

```text
CANONICAL_VALIDATION=PASS
LOCAL_PHASE1_DETERMINISTIC=PASS
PYTEST=PASS
GIT_DIFF_CHECK=PASS
CI_STATUS=PENDING
```

## 10. Stop

```text
LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
NEXT_PHASE_AUTHORIZED_NOW=NO

STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_LIVE_PROVIDER_AUTHORIZATION
```
