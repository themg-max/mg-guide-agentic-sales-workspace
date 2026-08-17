# NW-008 AT-1 — Read-Only External Verification Result 001

```text
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_001
RESULT=BLOCKED_FAIL_CLOSED
AUTHORIZED_GRANT_SHA=784c6565bb5d7bb1cefba255232256ba60e71b0a
BRANCH=impl/nw008-at1-safe-environment-readiness
ARTIFACT_KIND=BOUNDED_READ_ONLY_EXTERNAL_VERIFICATION_RESULT
OWNER_LANE=VS Code / Orchestrator
RECORDED_AT_UTC=2026-08-17T00:19:00Z
```

## Disposition

```text
MCP_DISCOVERY_ATTEMPTED=YES
MCP_DISCOVERY_RESULT=INCOMPATIBLE_CONNECTOR_BEHAVIOR

PROHIBITED_RECORD_SEARCH_LIST_OCCURRED=YES
EXACT_CRM_READS_EXECUTED=0
EXACT_AUTHORIZED_CRM_READS_COMPLETED=0
MUTATION_CALLS_EXECUTED=0

STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST

EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Controlled fail-closed closeout for grant `NW008_AT1_RO_EXTERNAL_VERIFY_001`.
No exact CRM record reads and no mutations were executed under this result.
No live CRM record payloads are included in this artifact.

## Why blocked

MCP discovery against the configured HighLevel / GHL connector control plane did
**not** stay within pure control-plane enumeration semantics for this lane.

Observed incompatible behavior:

```text
EXPECTED=tools/list_and_or_operation_schema_discovery_only
OBSERVED=connector_control_plane_search_returned_record_list
PROHIBITED_UNDER_GRANT=BLOCKED_RECORD_SEARCH / BLOCKED_RECORD_LIST_PAGINATION
FAIL_CLOSED_ACTION=STOP_WITHOUT_EXACT_CRM_READS_OR_MUTATIONS
```

Because a prohibited record search/list surface activated during discovery, the
operator lane stopped. Exact location/contact/opportunity/pipeline reads were
**not** attempted after the stop.

## Caps compliance

| Cap / rule | Value | Observed |
| --- | --- | --- |
| `CRM_RECORD_READS_MAX` | 4 | `EXACT_CRM_READS_EXECUTED=0` |
| `MUTATION_CALLS_MAX` | 0 | `MUTATION_CALLS_EXECUTED=0` |
| `SEARCH_LIST_PAGINATION` | NO | violated by connector behavior → fail-closed |
| `RAW_REST_FALLBACK` | NO | not used |
| `AT1_EXECUTION_AUTHORIZED` | NO | remains NO |
| PIT print / commit / proof | FORBIDDEN | not exposed |

## Action 2 — Local GHL MCP control-plane / tool inventory (sanitized)

Inspection source (local repo inventory only; no CRM record calls in this closeout):

```text
GHL_MCP_SURFACE_IDENTIFIED=YES
INVENTORY_SOURCES=
  contracts/ghl_tool_manifest.yaml
  proof/phase2/tools/tools-anthropic_v2.json
  proof/phase2/tools/original-mcp-relevant-tools.json
  proof/phase2/operations/op-*.json
  proof/phase2/discovery-report.md
LIVE_TOOLS_LIST_CALL_THIS_CLOSEOUT=NO
LIVE_SEARCH_CALL_THIS_CLOSEOUT=NO
LIVE_EXECUTE_OPERATION_THIS_CLOSEOUT=NO
LIVE_CRM_RECORD_PAYLOADS=NONE
```

### Endpoint surfaces (from prior authorized meta-discovery inventory)

| Surface | URL (public) | tools/list shape |
| --- | --- | --- |
| original_mcp | `https://services.leadconnectorhq.com/mcp/` | discrete tools (inventory subset preserved locally) |
| anthropic_v2 (recommended) | `https://services.leadconnectorhq.com/mcp/anthropic/v2` | 6 unified control-plane tools |

Auth mode (sanitized): private integration token bearer via local secret / MCP config only.
PIT values are not printed here.

### Anthropic v2 unified tools/list (sanitized names + schema intent)

| Tool | Role | Required inputs (names only) | Notes |
| --- | --- | --- | --- |
| `search` | natural-language **record** find | `query` | **record search** — incompatible with grant search ban if exercised |
| `fetch` | hydrate ids from search | `ids` | depends on search-typed ids |
| `search_operations` | operation catalog discovery | `query` | control-plane meta |
| `describe_operation` | operation schema inspection | `operationId` | control-plane meta |
| `execute_operation` | run catalog operation | `operationId` | read or write depending on operationId; not exercised here |
| `list_locations` | list bound sub-accounts | optional `query`, `pageToken` | location **list**, not exact location-by-id get |

### Original MCP discrete tools relevant subset (sanitized names)

```text
contacts_get-contact
contacts_get-contacts          # list/search — blocked class under this grant
contacts_get-all-tasks
contacts_create-contact        # mutation class
contacts_update-contact        # mutation class
contacts_upsert-contact        # mutation class
contacts_add-tags              # mutation class
contacts_remove-tags           # mutation class
opportunities_get-opportunity
opportunities_search-opportunity  # search — blocked class under this grant
opportunities_get-pipelines
opportunities_update-opportunity  # mutation class
```

Original discrete surface: **no** first-class `create-note` / `get-note` tools in the preserved inventory.

### Required AT-1 / grant operation mapping (presence + schema only)

Sanitized mapping for required logical operations. Schemas from local
`describe_operation` inventory snapshots under `proof/phase2/operations/`.
**No execution** of these operations in result 001.

| Required logical op | Mapped surface | Exact tool / operationId | Method / path | Key params (names only) | Scopes (catalog) | Presence |
| --- | --- | --- | --- | --- | --- | --- |
| exact location read | anthropic_v2 control-plane | `list_locations` only (no dedicated `get-location` op in inventory) | n/a (tool) | optional `query`, `pageToken` | connection-bound | **PARTIAL / NON-EXACT** |
| exact contact read | anthropic_v2 `execute_operation` / original discrete | `get-contact` / `contacts_get-contact` | `GET /contacts/{contactId}` | path `contactId` | `contacts.readonly` | YES |
| exact opportunity read | anthropic_v2 `execute_operation` / original discrete | `get-opportunity` / `opportunities_get-opportunity` | `GET /opportunities/{id}` | path `id` | `opportunities.readonly` | YES |
| exact pipeline read | anthropic_v2 `execute_operation` / original discrete | `get-pipelines` / `opportunities_get-pipelines` | `GET /opportunities/pipelines` | none (returns pipeline **list**) | `opportunities.readonly` | **PARTIAL / NON-EXACT** (no pipelineId path get in inventory) |
| create-note | anthropic_v2 `execute_operation` only | `create-note` | `POST /contacts/{contactId}/notes` | path `contactId`; body `body` (req), `userId` (opt) | `contacts.write` | YES on anthropic_v2; **ABSENT** on original discrete |
| get-note | anthropic_v2 `execute_operation` only | `get-note` | `GET /contacts/{contactId}/notes/{id}` | path `contactId`, `id` | `contacts.readonly` | YES on anthropic_v2; **ABSENT** on original discrete |
| update-opportunity | anthropic_v2 `execute_operation` / original discrete | `update-opportunity` / `opportunities_update-opportunity` | `PUT /opportunities/{id}` | path `id`; body includes `pipelineStageId`, `pipelineId`, `status`, … | `opportunities.write` | YES (schema only; **not executed**) |

### SANITIZED_REQUIRED_TOOL_MAPPING

```text
exact_location_read=list_locations|NO_DEDICATED_GET_LOCATION_BY_ID
exact_contact_read=execute_operation:get-contact|contacts_get-contact
exact_opportunity_read=execute_operation:get-opportunity|opportunities_get-opportunity
exact_pipeline_read=execute_operation:get-pipelines|opportunities_get-pipelines|LIST_ALL_NOT_BY_ID
create-note=execute_operation:create-note|ORIGINAL_DISCRETE_ABSENT
get-note=execute_operation:get-note|ORIGINAL_DISCRETE_ABSENT
update-opportunity=execute_operation:update-opportunity|opportunities_update-opportunity
```

### MISSING_REQUIRED_OPERATIONS

```text
MISSING_REQUIRED_OPERATIONS=
  exact_location_get_by_id
  exact_pipeline_get_by_id
  original_mcp_create-note
  original_mcp_get-note
```

Notes:

- `create-note` / `get-note` are present on the **anthropic_v2 operation catalog** via
  `execute_operation`, so they are not globally missing on the recommended surface.
- They **are** missing as first-class tools on the original `/mcp/` discrete surface.
- Exact location-by-id and exact pipeline-by-id reads are not represented as dedicated
  path-parameter GET operations in the preserved inventory; only list-style tools/ops
  (`list_locations`, `get-pipelines`) appear.
- Grant-required mutations remain **schema-only** under this result
  (`MUTATION_CALLS_EXECUTED=0`).

## Incompatible connector finding (control-plane)

```text
FINDING_ID=NW008-AT1-RO-001-CF-CONNECTOR-SEARCH
SEVERITY=blocking
SUMMARY=GHL connector control-plane discovery path activated record search/list behavior
STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST
IMPLICATION=Cannot complete external environment verification under SEARCH_LIST_PAGINATION=NO
LIVE_RECORD_CONTENT_IN_PROOF=NO
```

The anthropic_v2 tool named `search` is explicitly a customer/business **record**
search tool. Any connector UX that routes “discovery” through that tool is
incompatible with this grant’s hard ban on record search/list/pagination.

## Flags frozen after result 001

```text
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
REQUIRED_GHL_OPERATIONS_VERIFIED=PARTIAL_SCHEMA_INVENTORY_ONLY
GRANT_001_STATE=CLOSED_BLOCKED_FAIL_CLOSED
```

## Explicit non-actions

```text
DID_NOT_EXECUTE_EXACT_LOCATION_READ=YES
DID_NOT_EXECUTE_EXACT_CONTACT_READ=YES
DID_NOT_EXECUTE_EXACT_OPPORTUNITY_READ=YES
DID_NOT_EXECUTE_EXACT_PIPELINE_READ=YES
DID_NOT_EXECUTE_CREATE_NOTE=YES
DID_NOT_EXECUTE_UPDATE_OPPORTUNITY=YES
DID_NOT_RAW_REST_FALLBACK=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_MODIFY_CREDENTIALS=YES
DID_NOT_PUBLISH_PRIVATE_BINDING_IDS=YES
```

## STOP

```text
STOP_CODE=GHL_CONNECTOR_CONTROL_PLANE_SEARCH_RETURNED_RECORD_LIST
RESULT=BLOCKED_FAIL_CLOSED
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_001
NEXT=DO_NOT_PROCEED_TO_AT1_EXECUTION
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```
