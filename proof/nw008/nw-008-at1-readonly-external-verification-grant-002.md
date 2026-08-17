# NW-008 AT-1 — Read-Only External Verification Grant 002

```text
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_002
GRANT_TYPE=READ_ONLY_EXTERNAL_VERIFICATION
ARTIFACT_KIND=BOUNDED_READ_ONLY_EXTERNAL_VERIFICATION_GRANT
OWNER_LANE=VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
SUPERSEDES_GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_001
SUPERSEDED_GRANT_RESULT_SHA=31f5ce52cc681519928aed7b5a6bb1580a4660b7
SUPERSEDED_GRANT_RESULT=BLOCKED_FAIL_CLOSED
SUPERSEDED_STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST
AUTHORIZED_GRANT_001_SHA=784c6565bb5d7bb1cefba255232256ba60e71b0a
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
BOUND_TRACK_A_BASELINE_PATH=proof/nw008/nw-008-at1-safe-environment-readiness.md
DRAFT_STATE=DRAFT_NOT_COUNTERSIGNED
GRANT_STATE=DRAFT_AWAITING_HUMAN_COUNTERSIGNATURE
SELF_ACTIVATION=FORBIDDEN
```

This artifact is a **DRAFT AUTHORIZATION ONLY** for a second bounded **read-only**
external GHL environment verification lane. It is **not** active until human
countersignature is recorded in a follow-on commit.

It does **not** authorize AT-1 mutation execution, write operations, credential
create/expand, IAM/secrets/deployment changes, Firestore mutation, raw REST
fallback, generic HighLevel record search, private binding publication, retry,
or compensating mutation.

## Why grant 002 exists

Grant 001 closed fail-closed:

```text
GRANT_001_RESULT=BLOCKED_FAIL_CLOSED
STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST
EXACT_AUTHORIZED_CRM_READS_COMPLETED=0
MUTATION_CALLS_EXECUTED=0
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Root cause (sanitized): connector control-plane discovery routed through a
**record** search/list surface (`search` / list-class tools) rather than staying
inside pure tools/list + operation schema inspection. Grant 002 therefore
**forbids generic HighLevel search** and authorizes only **explicit GHL MCP
exact-read operations** identified from the local control-plane inventory.

## Local GHL MCP capability inspection (schema only; no CRM data)

Inspection mode for this draft:

```text
ALLOWED=tools/list_equivalent_inventory;schema/description_inspection
BLOCKED=CRM_record_reads;CRM_search;CRM_lists;mutations;PIT_output;secret_output
LIVE_CRM_RECORD_CALLS_THIS_DRAFT=0
LIVE_MUTATION_CALLS_THIS_DRAFT=0
INVENTORY_SOURCES=
  contracts/ghl_tool_manifest.yaml
  proof/phase2/tools/tools-anthropic_v2.json
  proof/phase2/tools/original-mcp-relevant-tools.json
  proof/phase2/operations/op-*.json
  proof/phase2/discovery-report.md
  proof/nw008/nw-008-at1-readonly-external-verification-result-001.md
GHL_MCP_SURFACE_IDENTIFIED=YES
```

### Endpoint surfaces (public URLs only)

| Surface | URL | tools/list shape |
| --- | --- | --- |
| original_mcp | `https://services.leadconnectorhq.com/mcp/` | discrete tools |
| anthropic_v2 (recommended) | `https://services.leadconnectorhq.com/mcp/anthropic/v2` | 6 unified control-plane tools |

Auth mode (sanitized): private integration token bearer via existing secret /
local MCP config only. PIT values are never printed, committed, or logged.

### Anthropic v2 unified tools (names + intent only)

| Tool | Control-plane vs record | Grant 002 posture |
| --- | --- | --- |
| `search_operations` | operation catalog meta | ALLOWED (discovery) |
| `describe_operation` | operation schema meta | ALLOWED (discovery) |
| `execute_operation` | runs catalog op by `operationId` | ALLOWED only for exact-read op allowlist below |
| `list_locations` | location **list** | **BLOCKED** as list/search class |
| `search` | customer/business **record** search | **BLOCKED** (generic HL search) |
| `fetch` | hydrate ids from search | **BLOCKED** (search-dependent) |

### SANITIZED_REQUIRED_TOOL_MAPPING

```text
exact-location-read=
  surface=anthropic_v2|original_mcp
  mapped_tool=NONE_DEDICATED_GET_LOCATION_BY_ID
  nearest_surface=list_locations
  exact_by_id=NO
  grant_002_use=NOT_AUTHORIZED_AS_LIST
  note=location identity remains private binding / connection-bound only under this draft

exact-contact-read=
  surface=anthropic_v2.execute_operation|original_mcp
  mapped_tool=execute_operation:get-contact|contacts_get-contact
  method_path=GET /contacts/{contactId}
  required_params=contactId
  exact_by_id=YES
  grant_002_use=AUTHORIZED_EXACT_READ

exact-opportunity-read=
  surface=anthropic_v2.execute_operation|original_mcp
  mapped_tool=execute_operation:get-opportunity|opportunities_get-opportunity
  method_path=GET /opportunities/{id}
  required_params=id
  exact_by_id=YES
  grant_002_use=AUTHORIZED_EXACT_READ

exact-pipeline-read=
  surface=anthropic_v2.execute_operation|original_mcp
  mapped_tool=execute_operation:get-pipelines|opportunities_get-pipelines
  method_path=GET /opportunities/pipelines
  required_params=NONE
  exact_by_id=NO
  returns=pipeline_list_not_by_id
  grant_002_use=NOT_AUTHORIZED_AS_LIST
  note=no dedicated get-pipeline-by-id in inventory

create-note=
  surface=anthropic_v2.execute_operation
  mapped_tool=execute_operation:create-note
  method_path=POST /contacts/{contactId}/notes
  original_discrete=ABSENT
  grant_002_use=SCHEMA_VERIFY_ONLY_NOT_EXECUTE

get-note=
  surface=anthropic_v2.execute_operation
  mapped_tool=execute_operation:get-note
  method_path=GET /contacts/{contactId}/notes/{id}
  original_discrete=ABSENT
  grant_002_use=SCHEMA_VERIFY_ONLY_NOT_EXECUTE_UNLESS_FUTURE_READBACK_GRANT

update-opportunity=
  surface=anthropic_v2.execute_operation|original_mcp
  mapped_tool=execute_operation:update-opportunity|opportunities_update-opportunity
  method_path=PUT /opportunities/{id}
  grant_002_use=SCHEMA_VERIFY_ONLY_NOT_EXECUTE
```

### Exact-read availability summary

```text
EXACT_READS_AVAILABLE=YES
EXACT_CONTACT_READ_AVAILABLE=YES
EXACT_OPPORTUNITY_READ_AVAILABLE=YES
EXACT_LOCATION_READ_BY_ID_AVAILABLE=NO
EXACT_PIPELINE_READ_BY_ID_AVAILABLE=NO
PREFERRED_SURFACE=anthropic_v2
```

### Bounded search contract enforceability

Generic MCP `search` schema (inventory) requires only `query`. Optional fields
include `limit`, `cursor` (pagination), and `locationId` (not always required).
No schema-enforced synthetic discriminator. Therefore:

```text
GENERIC_HIGHLEVEL_SEARCH_AUTHORIZED=NO
BOUNDED_SEARCH_AUTHORIZED=NO
BOUNDED_SEARCH_CONTRACT_ENFORCEABLE=NO
STOP_CODE_IF_SEARCH_REQUESTED=BOUNDED_SEARCH_CONTRACT_NOT_ENFORCEABLE
SEARCH_CALLS_MAX=0
SEARCH_RESULTS_MAX=0
SEARCH_PAGINATION=NO
SEARCH_RETRY=NO
SEARCH_CROSS_LOCATION=NO
```

Grant 002 does **not** fall back to a one-shot bounded search lane.

## Authorization posture (preferred path)

```text
GENERIC_HIGHLEVEL_SEARCH_AUTHORIZED=NO
EXPLICIT_GHL_MCP_EXACT_READS_AUTHORIZED=YES
BOUNDED_SEARCH_AUTHORIZED=NO
BOUNDED_SEARCH_CONTRACT_ENFORCEABLE=NO
```

## Hard caps (frozen for grant 002)

```text
CRM_EXACT_READS_MAX=4
MUTATION_CALLS_MAX=0
MCP_TOOLS_LIST_MAX=1
MCP_SCHEMA_DISCOVERY_MAX=UNBOUNDED_WITHIN_ALLOWED_OPERATION_SET_ONLY
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
RAW_REST_FALLBACK=NO
SEARCH_LIST_PAGINATION=NO
GENERIC_HIGHLEVEL_SEARCH=NO
FIRESTORE_MUTATION=NO
IAM_SECRETS_DEPLOYMENT_CHANGE=NO
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
```

## ALLOWED (only after human countersignature)

```text
ALLOWED_MCP_TOOLS_LIST=YES
ALLOWED_MCP_OPERATION_DISCOVERY=YES
ALLOWED_MCP_OPERATION_SCHEMA_DESCRIPTION=YES
ALLOWED_EXACT_CONTACT_READ=YES
ALLOWED_EXACT_OPPORTUNITY_READ=YES
ALLOWED_EXECUTE_OPERATION_GET_CONTACT=YES
ALLOWED_EXECUTE_OPERATION_GET_OPPORTUNITY=YES
ALLOWED_ORIGINAL_DISCRETE_CONTACTS_GET_CONTACT=YES
ALLOWED_ORIGINAL_DISCRETE_OPPORTUNITIES_GET_OPPORTUNITY=YES
```

Exact CRM reads that count toward `CRM_EXACT_READS_MAX=4`:

1. contact — exact private contact id via `get-contact` / `contacts_get-contact`
2. opportunity — exact private opportunity id via `get-opportunity` / `opportunities_get-opportunity`
3. reserved slot — only if a later countersigned amendment adds another **exact-by-id** read
4. reserved slot — same constraint

From opportunity exact read, operator may record **privately** (not in public proof):

```text
opportunity.location_binding
opportunity.contact_binding
opportunity.pipelineId
opportunity.current_pipelineStageId
```

## BLOCKED (always in this grant)

```text
BLOCKED_GENERIC_HIGHLEVEL_SEARCH=YES
BLOCKED_MCP_TOOL_SEARCH=YES
BLOCKED_MCP_TOOL_FETCH=YES
BLOCKED_LIST_LOCATIONS_CALL=YES
BLOCKED_GET_PIPELINES_LIST_CALL=YES
BLOCKED_RECORD_SEARCH=YES
BLOCKED_RECORD_LIST_PAGINATION=YES
BLOCKED_BOUNDED_SEARCH_FALLBACK=YES
BLOCKED_CREATE_NOTE_EXECUTION=YES
BLOCKED_GET_NOTE_EXECUTION=YES
BLOCKED_UPDATE_OPPORTUNITY_EXECUTION=YES
BLOCKED_ANY_OTHER_MUTATION=YES
BLOCKED_RAW_REST_FALLBACK=YES
BLOCKED_FIRESTORE_MUTATION=YES
BLOCKED_IAM_SECRETS_DEPLOYMENT_CHANGES=YES
BLOCKED_RETRY=YES
BLOCKED_COMPENSATING_MUTATION=YES
BLOCKED_PRODUCTION_CRM=YES
BLOCKED_PRIVATE_ID_PUBLICATION_TO_PUBLIC_REPO=YES
BLOCKED_AT1_MUTATION_EXECUTION=YES
BLOCKED_CREDENTIAL_CREATE_OR_EXPAND=YES
```

Schema presence verification (describe_operation / local inventory only) remains
allowed for `create-note`, `get-note`, and `update-opportunity` without execution.

## Known inventory gaps (fail-closed rules)

```text
EXACT_LOCATION_GET_BY_ID=MISSING
EXACT_PIPELINE_GET_BY_ID=MISSING
```

Operator handling under this draft:

```text
IF exact location live read required AND only list_locations available:
  STOP_CODE=EXACT_LOCATION_READ_UNAVAILABLE
  EXTERNAL_ENVIRONMENT_VERIFIED=NO
  ENVIRONMENT_READY=NO
  DO_NOT_CALL_list_locations

IF exact pipeline live read required AND only get-pipelines list available:
  STOP_CODE=EXACT_PIPELINE_READ_UNAVAILABLE
  EXTERNAL_ENVIRONMENT_VERIFIED=NO
  ENVIRONMENT_READY=NO
  DO_NOT_CALL_get-pipelines

IF connector UX forces record search/list during discovery:
  STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST
  EXTERNAL_ENVIRONMENT_VERIFIED=NO
  ENVIRONMENT_READY=NO
  DO_NOT_CONTINUE_EXACT_READS
```

Location binding may remain satisfied only by prior private binding / single-location
connection evidence without a live list call. That does **not** alone flip
`EXTERNAL_ENVIRONMENT_VERIFIED=YES`.

## Credential scope gate (carry-forward; re-confirm if credential changed)

```text
CREDENTIAL_SCOPE_GATE=PASS_PRIOR_GRANT_001
LOCATIONS_READONLY_VERIFIED=YES
CONTACTS_READONLY_VERIFIED=YES
OPPORTUNITIES_READONLY_VERIFIED=YES
WRITE_SCOPES_OBSERVED=NO
EXPECTED_READONLY_SCOPES=locations.readonly;contacts.readonly;opportunities.readonly
```

If write or unrelated broad scopes appear:

```text
STOP_CODE=CREDENTIAL_SCOPE_TOO_BROAD
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

Do **not** create or expand credentials in this lane.

## PIT / token handling

```text
PIT_IN_CHAT=FORBIDDEN
PIT_IN_COMMIT=FORBIDDEN
PIT_IN_TERMINAL_LOGS=FORBIDDEN
PIT_IN_PROOF=FORBIDDEN
PIT_STORAGE=EXISTING_SECRET_STORAGE_OR_LOCAL_MCP_CONFIG_ONLY
```

## Private binding (operator lane only)

```text
PRIVATE_LOCATION_ID_SOURCE=BUSINESS_PROFILE_SCREENSHOT
PRIVATE_CONTACT_ID_SOURCE=SYNTHETIC_CONTACT_AUDIT_LOG
PRIVATE_OPPORTUNITY_ID_SOURCE=SYNTHETIC_OPPORTUNITY_AUDIT_LOG
PRIVATE_BINDING_PUBLICATION=NO
CONTACT_REUSE_PROVENANCE_REQUIRED=YES
CONTACT_REUSE_PROVENANCE_STATUS=PENDING_OPERATOR_RECORD_IN_PRIVATE_LANE
NW008_BINDING_OF_REUSED_SYNTHETIC_CONTACT=ALLOWED_ONLY_AFTER_PROVENANCE_RECORDED_PRIVATELY
```

Do **not** copy private IDs into this public proof artifact.

## Authority and countersignature (inactive until signed)

```text
REQUEST_INITIATOR=VS_CODE_ORCHESTRATOR_OPERATOR_LANE
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_COUNTERSIGNATURE=PENDING
HUMAN_APPROVER=
APPROVED_AT=
APPROVAL_STATEMENT=
GRANT_STATE=DRAFT_AWAITING_HUMAN_COUNTERSIGNATURE
SELF_ACTIVATION=FORBIDDEN
EXPIRY=60_MINUTES_AFTER_COUNTERSIGNATURE
EXTERNAL_READS_AUTHORIZED=NO_UNTIL_COUNTERSIGNATURE
MCP_DISCOVERY_AUTHORIZED=NO_UNTIL_COUNTERSIGNATURE
OPERATOR_EXECUTION_AUTHORIZED=NO_UNTIL_COUNTERSIGNATURE
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

### Countersignature template (human only)

```text
HUMAN_COUNTERSIGNATURE=APPROVED
HUMAN_APPROVER=<email>
APPROVED_AT=<ISO-8601>
APPROVAL_STATEMENT=I authorize NW008_AT1_RO_EXTERNAL_VERIFY_002 read-only external verification only, bound to TRACK_A_READINESS_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a and SUPERSEDED_GRANT_RESULT_SHA=31f5ce52cc681519928aed7b5a6bb1580a4660b7, with GENERIC_HIGHLEVEL_SEARCH_AUTHORIZED=NO, EXPLICIT_GHL_MCP_EXACT_READS_AUTHORIZED=YES, CRM_EXACT_READS_MAX=4, MUTATION_CALLS_MAX=0, BOUNDED_SEARCH_AUTHORIZED=NO, expiry 60 minutes after approval. AT-1 execution remains unauthorized.
GRANT_STATE=AUTHORIZED_READ_ONLY_EXTERNAL_VERIFICATION
```

## Post-countersignature operator procedure (authorized within expiry)

### A. MCP discovery (control-plane only)

1. At most one tools/list (or equivalent) against anthropic_v2 preferred surface.
2. describe_operation / schema inspect only for allowlisted exact-read and
   future-mutation schema ops: `get-contact`, `get-opportunity`, `create-note`,
   `get-note`, `update-opportunity`.
3. If discovery UX invokes `search`, `fetch`, `list_locations`, contact/opportunity
   list tools, or any record list → **STOP** with
   `GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST`.

### B. Exact CRM reads (max 4; exact IDs only)

Authorized executions only:

1. `execute_operation:get-contact` or `contacts_get-contact` with exact private contactId
2. `execute_operation:get-opportunity` or `opportunities_get-opportunity` with exact private id

Do not call:

- `search` / `fetch`
- `list_locations`
- `get-pipelines` / `opportunities_get-pipelines`
- any `*/search*` operation
- any mutation operationId

### C. Success / failure disposition

Partial success path (exact contact + opportunity only; location/pipeline live
exact-by-id still missing):

```text
PARTIAL:
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
STOP_CODE=EXACT_LOCATION_OR_PIPELINE_READ_UNAVAILABLE
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Full success still requires a later amendment that solves location/pipeline exact
read gaps without list/search. This draft alone cannot set:

```text
EXTERNAL_ENVIRONMENT_VERIFIED=YES
ENVIRONMENT_READY=YES
```

Any stop, cap breach, or search/list activation:

```text
FAILURE:
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
<specific STOP_CODE>
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

This grant never flips `AT1_EXECUTION_AUTHORIZED` to YES.

## Flags preserved

```text
CRM_EXACT_READS_MAX=4
MUTATION_CALLS_MAX=0
RAW_REST_FALLBACK=NO
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

## Relationship to Track A readiness

| Surface | State at draft commit |
| --- | --- |
| Deterministic executor (fixtures) | VERIFIED (`DETERMINISTIC_EXECUTOR_READY=YES`) |
| Grant 001 RO external verify | CLOSED `BLOCKED_FAIL_CLOSED` |
| This grant 002 | `DRAFT_AWAITING_HUMAN_COUNTERSIGNATURE` |
| External GHL environment | NOT VERIFIED |
| AT-1 mutation execution | UNAUTHORIZED |

## STOP

```text
STOP_CODE=NW008_AT1_RO_EXTERNAL_VERIFY_GRANT_002_DRAFTED
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_002
GRANT_STATE=DRAFT_AWAITING_HUMAN_COUNTERSIGNATURE
GENERIC_HIGHLEVEL_SEARCH_AUTHORIZED=NO
EXPLICIT_GHL_MCP_EXACT_READS_AUTHORIZED=YES
BOUNDED_SEARCH_AUTHORIZED=NO
BOUNDED_SEARCH_CONTRACT_ENFORCEABLE=NO
CRM_EXACT_READS_MAX=4
MUTATION_CALLS_MAX=0
RAW_REST_FALLBACK=NO
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=HUMAN_COUNTERSIGNATURE_REQUIRED_BEFORE_ANY_EXTERNAL_READ
```
