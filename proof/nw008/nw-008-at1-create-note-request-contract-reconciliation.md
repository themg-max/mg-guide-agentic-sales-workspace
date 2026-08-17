# NW-008 AT-1 -- Create-Note Request Contract Reconciliation

```text
DIAGNOSTIC_ID=NW008_AT1_CREATE_NOTE_REQUEST_CONTRACT_RECON_002
ARTIFACT_KIND=CREATE_NOTE_REQUEST_CONTRACT_RECONCILIATION
OWNER_LANE=VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
ACTION=CREATE

SOURCE_RESULT_007_SHA=4bd9e4d6ee23661e4e7b00ca49234e7ebdd0a058
SOURCE_DIAGNOSTIC_001_SHA=161bdc19c7d0087a207a7b63d7347b138af7c796
ROOT_CAUSE_CLASS_PRIOR=REQUEST_SCHEMA_MISMATCH_OR_VALIDATION

GRANT_007_RETRY_AUTHORIZED=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO

GHL_BUSINESS_CALLS_EXECUTED=0
CRM_MUTATIONS_EXECUTED=0
RECORDED_AT_UTC=2026-08-17T12:11:04Z
```

## Purpose

Compare the live MCP `create-note` operation / `execute_operation` request
contract with the sanitized key/type shape actually emitted by Grant 007.
Identify the exact contract mismatch before any implementation change or
Grant 008 preparation.

This step performs **metadata/schema inspection and private local evidence
review only**. No business transport calls and no CRM mutations were executed.

## Evidence sources (no raw secrets / no business IDs / no note content)

```text
LIVE_SCHEMA_SOURCE_1=preserved_live_describe_operation(create-note)_during_grant007_prep
LIVE_SCHEMA_SOURCE_2=proof/phase2/operations/op-create-note.json
EXECUTE_OPERATION_TOOL_SCHEMA=proof/phase2/tools/tools-anthropic_v2.json
MANIFEST_CROSSCHECK=contracts/ghl_tool_manifest.yaml (idempotency: required_true_per_catalog)
ACTUAL_REQUEST_SOURCE=Grant_007_live_MCP_transport_adapter_dispatch_mapping
PRIVATE_ERROR_SOURCE=/tmp/nw008_grant007_run/call_03_create-note.raw.txt
BOUNDED_EXECUTOR_REF=src/integrations/ghl/bounded_at1_executor.py
RAW_PRIVATE_RESPONSE_PRINTED=NO
RAW_PRIVATE_RESPONSE_COMMITTED=NO
BUSINESS_ID_PRINTED=NO
NOTE_CONTENT_PRINTED=NO
```

## Step 1 — Live create-note contract (structure only)

```text
LIVE_CREATE_NOTE_SCHEMA_RETRIEVED=YES
OPERATION_ID=create-note
METHOD=POST
PATH_TEMPLATE=/contacts/{contactId}/notes
```

### Path parameters

| Name | Required | Type |
| --- | --- | --- |
| `contactId` | YES | string |

```text
REQUIRED_PATH_PARAMETER_NAMES=[contactId]
OPTIONAL_PATH_PARAMETER_NAMES=[]
```

### Query parameters

```text
REQUIRED_QUERY_PARAMETER_NAMES=[]
OPTIONAL_QUERY_PARAMETER_NAMES=[]
```

### Body fields (operation request body object)

| Name | Required | Type | Notes |
| --- | --- | --- | --- |
| `body` | YES | string | Note content |
| `userId` | NO | string | Author user id |

```text
REQUIRED_BODY_FIELD_NAMES=[body]
OPTIONAL_BODY_FIELD_NAMES=[userId]
BODY_NESTING=params.body is an object containing field body (string)
```

`payloadExample` also shows `params.body.contactId` as an example companion
field. It is **not** listed in `requestBodyFields` as required; Grant 007 did
not send it. That absence is not classified as the failing required field.

### Operation-level write flags (describe_operation)

```text
hasRequestBody=YES
idempotencyRequired=YES
requiresApproval=YES
requiredScopes=[contacts.write]
```

### execute_operation tool envelope (anthropic_v2)

From the live tool catalog / phase-2 tool schema, `execute_operation` accepts:

| Top-level field | Type | Role |
| --- | --- | --- |
| `operationId` | string | required by tool schema |
| `params` | object | path/query/header/body bundle |
| `locationId` | string | optional/tool-level |
| `dryRun` | boolean | optional preview |
| `idempotencyKey` | string | **Required for writes before broad rollout** |
| `reason` | string | short user-facing reason |

```text
EXECUTE_OPERATION_TOP_LEVEL_KEYS=
  [operationId, params, locationId, dryRun, idempotencyKey, reason]
IDEMPOTENCY_KEY_FIELD=idempotencyKey
IDEMPOTENCY_KEY_LOCATION=execute_operation top-level (NOT inside params.body)
IDEMPOTENCY_KEY_TYPE=string
```

## Step 2 — Grant 007 actual request key/type shape (values withheld)

Recovered from the Grant 007 live MCP transport adapter `dispatch()` mapping
used for the consumed one-shot run (sanitized keys/types only):

### Executor internal arguments (fixture/public seam)

```text
EXECUTOR_CREATE_NOTE_ARG_KEYS=[location_id, contact_id, content_or_fingerprint]
EXECUTOR_CREATE_NOTE_ARG_TYPES={
  location_id: string,
  contact_id: string,
  content_or_fingerprint: string
}
```

These internal names are **not** the MCP wire contract. They are mapped by the
live transport adapter.

### Actual MCP `execute_operation` arguments emitted for create-note

```text
ACTUAL_REQUEST_KEY_SHAPE_RECOVERED=YES

ACTUAL_TOP_LEVEL_KEYS=[operationId, params, reason]
ACTUAL_TOP_LEVEL_TYPES={
  operationId: string,          # literal create-note
  params: object,
  reason: string
}

ACTUAL_PATH_KEYS=[contactId]
ACTUAL_PATH_FIELD_TYPES={contactId: string}

ACTUAL_QUERY_KEYS=[]            # empty object present
ACTUAL_QUERY_FIELD_TYPES={}

ACTUAL_BODY_KEYS=[body]
ACTUAL_BODY_FIELD_TYPES={body: string}
ACTUAL_BODY_NESTING=params.body.body  (object -> string field)

ACTUAL_IDEMPOTENCY_KEY_PRESENT=NO
ACTUAL_DRY_RUN_PRESENT=NO
ACTUAL_LOCATION_ID_TOP_LEVEL_PRESENT=NO
ACTUAL_USER_ID_BODY_PRESENT=NO
```

Conceptual wire shape (types only; no values):

```text
execute_operation.arguments = {
  operationId: string("create-note"),
  params: {
    path:  { contactId: string },
    query: {},
    body:  { body: string }
  },
  reason: string
  # idempotencyKey: ABSENT
}
```

## Step 3 — Private error classification (no verbatim text)

Preserved nested operation payload from Grant 007 `create-note` response was
inspected privately. Verbatim `error` / `nextStep` strings are not reproduced.

```text
PRIVATE_ERROR_INSPECTED=YES
CREATE_NOTE_OPERATION_STATUS=400
CREATE_NOTE_OPERATION_SUCCESS=false
MCP_IS_ERROR=YES

VALIDATION_TARGET_FIELDS=[idempotencyKey]
ERROR_INDICATES_MISSING_REQUIRED_FIELD=YES
ERROR_INDICATES_INVALID_FIELD_NAME=NO
ERROR_INDICATES_INVALID_TYPE=NO
ERROR_INDICATES_BODY_SHAPE=NO
ERROR_INDICATES_PATH_PARAMETER=NO

ERROR_CLASS_SUMMARY=
  operation-level rejection stating create-note requires idempotency;
  next-step class directs caller to supply idempotencyKey
  (or use dryRun preview) on execute_operation
```

Token-class confirmation (equality flags only; body text not printed):

```text
ERROR_MATCHES_CREATE_NOTE=YES
ERROR_MATCHES_REQUIRES=YES
ERROR_MATCHES_IDEMPOTENCY=YES
NEXT_STEP_MATCHES_IDEMPOTENCY_KEY=YES
NEXT_STEP_MATCHES_EXECUTE_OPERATION=YES
```

## Step 4 — Structural diff

| Check | Result | Notes |
| --- | --- | --- |
| PATH_KEYS_MATCH | **YES** | `contactId` present and required |
| QUERY_KEYS_MATCH | **YES** | none required; empty query object OK |
| BODY_KEYS_MATCH | **YES** | required field `body` present under body object |
| BODY_NESTING_MATCH | **YES** | `params.body` is object, not bare string |
| BODY_TYPES_MATCH | **YES** | `body` field is string |
| REQUIRED_FIELDS_PRESENT | **NO** | missing execute_operation top-level `idempotencyKey` |

```text
PATH_KEYS_MATCH=YES
QUERY_KEYS_MATCH=YES
BODY_KEYS_MATCH=YES
BODY_NESTING_MATCH=YES
BODY_TYPES_MATCH=YES
REQUIRED_FIELDS_PRESENT=NO

VALIDATION_TARGET_CLASS=MISSING_REQUIRED_FIELD
MISSING_REQUIRED_FIELD_NAME=idempotencyKey
MISSING_REQUIRED_FIELD_LOCATION=execute_operation.arguments.idempotencyKey
MISSING_REQUIRED_FIELD_TYPE=string
```

### Classification decision

Exactly one target class is selected:

```text
VALIDATION_TARGET_CLASS=MISSING_REQUIRED_FIELD
```

Rationale:

1. Path/body nesting/types match the live create-note operation schema.
2. Operation catalog flags `idempotencyRequired=true` for create-note.
3. Tool schema documents `idempotencyKey` as required for writes.
4. Grant 007 transport omitted `idempotencyKey` entirely.
5. Live 400 rejection class names idempotency / `idempotencyKey`, not body/path
   field names.

Not selected:

- `PATH_PARAMETER` — path matched
- `BODY_NESTING` — nesting matched
- `FIELD_NAME` — no invalid body field name signal
- `FIELD_TYPE` — no type mismatch signal
- `UNKNOWN` — evidence is sufficient

## Step 5 — Implementation boundary (no code changes)

Inspected:

```text
BOUNDED_EXECUTOR=src/integrations/ghl/bounded_at1_executor.py
LIVE_TRANSPORT=Grant_007_one_shot_live_MCP_dispatch_adapter
```

### Bounded executor

The fixture-facing executor dispatches internal args:

```text
create-note -> {location_id, contact_id, content_or_fingerprint}
get-note    -> {location_id, contact_id, note_id}
```

It does **not** serialize MCP `execute_operation` envelopes. Omitting
`idempotencyKey` is therefore **not** an input-binding defect and **not** a
defect inside the frozen six-operation executor argument seam itself.

```text
INPUT_CONTRACT_DEFECT=NO
EXECUTOR_REQUEST_MAPPING_DEFECT=NO
```

### Live MCP transport adapter

The Grant 007 live adapter mapped path/body correctly but never set
`idempotencyKey` on write operations (`create-note`, and the same omission
exists on the unused `update-opportunity` branch).

```text
MCP_TRANSPORT_SERIALIZATION_DEFECT=YES
IMPLEMENTATION_CHANGE_REQUIRED=YES
IMPLEMENTATION_CHANGE_SCOPE=
  live execute_operation write envelope must supply a unique string
  idempotencyKey when target operation idempotencyRequired=true
FROZEN_SIX_OPERATION_SEMANTICS_CHANGE_REQUIRED=NO
NOTE_ATTEMPT_COUNTER_CHANGE_REQUIRED=NO
RETRY_INTRODUCTION_REQUIRED=NO
```

No code was changed in this diagnostic step.

## Step 6 — Precheck operation 4 (`get-note`)

### Live get-note contract (structure)

```text
GET_NOTE_SCHEMA_SOURCE=proof/phase2/operations/op-get-note.json
OPERATION_ID=get-note
METHOD=GET
PATH_TEMPLATE=/contacts/{contactId}/notes/{id}
REQUIRED_PATH_PARAMETER_NAMES=[contactId, id]
OPTIONAL_PATH_PARAMETER_NAMES=[]
REQUIRED_QUERY_PARAMETER_NAMES=[]
HAS_REQUEST_BODY=NO
IDEMPOTENCY_REQUIRED=NO
```

### Grant 007 adapter mapping for get-note

```text
ACTUAL_GET_NOTE_TOP_LEVEL_KEYS=[operationId, params, reason]
ACTUAL_GET_NOTE_PATH_KEYS=[contactId, id]
ACTUAL_GET_NOTE_QUERY_KEYS=[]
ACTUAL_GET_NOTE_BODY_PRESENT=NO
ACTUAL_GET_NOTE_IDEMPOTENCY_KEY_PRESENT=NO   # acceptable: idempotencyRequired=false
```

```text
GET_NOTE_MAPPING_REVIEWED=YES
GET_NOTE_PATH_KEYS_MATCH=YES
GET_NOTE_BODY_MAPPING_OK=YES
GET_NOTE_MAPPING_DEFECT_FOUND=NO
```

Note: `get-note` remains unreachable until create-note succeeds and returns a
note id. No Grant 008 execution is authorized by this document.

### Secondary write precheck (not executed; mapping only)

`update-opportunity` is also `idempotencyRequired=true` per catalog and the
Grant 007 adapter branch likewise omits `idempotencyKey`. Any future write
mapping fix should cover **all** idempotency-required writes in the AT-1
surface, not only create-note, to avoid the next avoidable contract failure
after note success.

```text
UPDATE_OPPORTUNITY_IDEMPOTENCY_KEY_PRESENT_IN_GRANT007_ADAPTER=NO
UPDATE_OPPORTUNITY_SAME_CLASS_DEFECT_LATENT=YES
```

## Public result block

```text
DIAGNOSTIC_ID=NW008_AT1_CREATE_NOTE_REQUEST_CONTRACT_RECON_002
SOURCE_RESULT_007_SHA=4bd9e4d6ee23661e4e7b00ca49234e7ebdd0a058
SOURCE_DIAGNOSTIC_001_SHA=161bdc19c7d0087a207a7b63d7347b138af7c796

GHL_BUSINESS_CALLS_EXECUTED=0
CRM_MUTATIONS_EXECUTED=0

LIVE_CREATE_NOTE_SCHEMA_RETRIEVED=YES
ACTUAL_REQUEST_KEY_SHAPE_RECOVERED=YES

PATH_KEYS_MATCH=YES
QUERY_KEYS_MATCH=YES
BODY_KEYS_MATCH=YES
BODY_NESTING_MATCH=YES
BODY_TYPES_MATCH=YES
REQUIRED_FIELDS_PRESENT=NO

VALIDATION_TARGET_CLASS=MISSING_REQUIRED_FIELD
MISSING_REQUIRED_FIELD_NAME=idempotencyKey

INPUT_CONTRACT_DEFECT=NO
EXECUTOR_REQUEST_MAPPING_DEFECT=NO
MCP_TRANSPORT_SERIALIZATION_DEFECT=YES

GET_NOTE_MAPPING_REVIEWED=YES
GET_NOTE_MAPPING_DEFECT_FOUND=NO

IMPLEMENTATION_CHANGE_REQUIRED=YES

RETRY_AUTHORIZED=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
GRANT_008_PREPARATION_AUTHORIZED=NO
```

## Explicit non-actions

```text
DID_NOT_CALL_GET_CONTACT=YES
DID_NOT_CALL_GET_OPPORTUNITY=YES
DID_NOT_CALL_CREATE_NOTE=YES
DID_NOT_CALL_GET_NOTE=YES
DID_NOT_CALL_UPDATE_OPPORTUNITY=YES
DID_NOT_CALL_GET_PIPELINES=YES
DID_NOT_SEARCH=YES
DID_NOT_LIST=YES
DID_NOT_RAW_REST=YES
DID_NOT_RETRY_CREATE_NOTE=YES
DID_NOT_CHANGE_CODE=YES
DID_NOT_PRINT_RAW_PRIVATE_RESPONSE=YES
DID_NOT_COMMIT_RAW_PRIVATE_RESPONSE=YES
DID_NOT_PRINT_BUSINESS_IDS=YES
DID_NOT_PRINT_NOTE_CONTENT=YES
DID_NOT_AUTHORIZE_GRANT_008=YES
DID_NOT_CLAIM_AT1_COMPLETE=YES
```

## STOP

```text
STOP_CODE=NW008_AT1_CREATE_NOTE_REQUEST_CONTRACT_RECON_002_RECORDED
DIAGNOSTIC_ID=NW008_AT1_CREATE_NOTE_REQUEST_CONTRACT_RECON_002
VALIDATION_TARGET_CLASS=MISSING_REQUIRED_FIELD
MISSING_REQUIRED_FIELD_NAME=idempotencyKey
MCP_TRANSPORT_SERIALIZATION_DEFECT=YES
IMPLEMENTATION_CHANGE_REQUIRED=YES
RETRY_AUTHORIZED=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=BOUNDED_CREATE_NOTE_REQUEST_MAPPING_FIX
```
