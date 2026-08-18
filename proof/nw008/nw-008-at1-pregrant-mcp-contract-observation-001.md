# NW-008 AT-1 Pre-Grant MCP Contract Observation 001

## 1. Execution identity and authority binding

```text
CLASSIFICATION=execution_proof
ARTIFACT_KIND=PREGRANT_MCP_CONTRACT_OBSERVATION_RESULT
PROOF_ID=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001
OWNER=VS Code / MG Orchestrator
PROOF_BRANCH=proof/nw008-at1-pregrant-mcp-contract-observation-001
PROOF_BASE_REF=origin/main
PROOF_BASE_SHA=c55bf90bd652b94dc3cbea8085357205f64676f1

AUTHORIZATION_ID=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001
AUTHORIZATION_PATH=governance/authorizations/nw008-at1-pregrant-mcp-contract-observation-001.md
AUTHORIZATION_REVIEWED_HEAD=ec61a43131db1cde21581d651f2d04e970144573
AUTHORIZATION_MERGE_SHA=c55bf90bd652b94dc3cbea8085357205f64676f1
AUTHORIZATION_PR=77

SOURCE_PLANNING_UNIT=proof/nw008/nw-008-at1-mcp-response-source-capture.md
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25

OBSERVATION_STARTED_AT_UTC=2026-08-18T10:10:10Z
INITIALIZE_FINISHED_AT_UTC=2026-08-18T10:10:10Z
TOOLS_LIST_STARTED_AT_UTC=2026-08-18T10:10:39Z
TOOLS_LIST_FINISHED_AT_UTC=2026-08-18T10:10:39Z
OBSERVATION_FINISHED_AT_UTC=2026-08-18T10:11:22Z
RECORDED_AT_UTC=2026-08-18T10:11:22Z
```

This unit executes only the merged pre-grant MCP protocol and advertised-tool
contract observation authorized by PR #77. It does not implement parser,
session, adapter, or runtime code. It does not call `tools/call`,
`execute_operation`, or any other advertised tool. It does not perform GHL
business reads or mutations.

## 2. Preflight

| Check | Result |
| --- | --- |
| Working branch is not `main` at execution start | YES (`auth/nw008-at1-pregrant-mcp-contract-observation-001`) |
| `git fetch origin` | YES |
| PR #77 reviewed head `ec61a43131db1cde21581d651f2d04e970144573` is ancestor of `origin/main` | YES |
| PR #77 merge SHA | `c55bf90bd652b94dc3cbea8085357205f64676f1` |
| Authorization artifact on `origin/main` | YES |

```text
PR77_REVIEWED_HEAD=ec61a43131db1cde21581d651f2d04e970144573
PR77_MERGE_SHA=c55bf90bd652b94dc3cbea8085357205f64676f1
PR77_MAIN_REACHABLE=YES
AUTHORIZATION_ON_MAIN=YES
```

## 3. Observation surface (sanitized)

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
TRANSPORT_CLASS=streamable_http_sse
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
PIT_IN_PROOF=NO
PRIVATE_RECORD_IDS_IN_PROOF=NO
CUSTOMER_DATA_IN_PROOF=NO
MCP_SESSION_ID_OBSERVED=NO
```

Transport notes:

1. Responses used `Content-Type: text/event-stream` with one `event: message`
   JSON-RPC payload per response body.
2. No `Mcp-Session-Id` response header was observed on initialize or
   `tools/list`.
3. After initialize, one protocol-required `notifications/initialized`
   notification was posted (HTTP 202, empty body). That notification is not an
   additional `initialize` call and is not a catalog sequence.
4. Subsequent requests carried `MCP-Protocol-Version: 2025-11-25`.

## 4. Required result fields

```text
NEGOTIATED_PROTOCOL_VERSION=2025-11-25
PROTOCOL_VERSION_MATCH=YES
EXECUTE_OPERATION_TOOL_PRESENT=YES
EXECUTE_OPERATION_INPUT_SCHEMA_CAPTURED=YES
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE

MCP_INITIALIZE_CALLS=1
MCP_TOOLS_LIST_SEQUENCES=1
MCP_TOOLS_LIST_REQUESTS=1
MCP_EXECUTE_OPERATION_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
GRANT009_EXECUTIONS=0

FAIL_CLOSED=NO
STOP_REASON=OBSERVATION_COMPLETE_CATALOG_CAPTURED_OUTPUT_SCHEMA_ABSENT

HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

Freeze rationale: `execute_operation` was advertised and its exact
`inputSchema` was captured, but the provider did not advertise
`outputSchema`. Per the authorization, member absence is recorded as absence
and does not authorize schema invention. Therefore
`EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE`,
`HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO`, and
`COMPOSITE_CONTRACT_FREEZE_READY=NO`.

## 5. Initialize exchange

### 5.1 Offered request (byte-exact JSON body)

Request id: `1`

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mg-guide-nw008-at1-pregrant-observation","version":"0.0.1"}}}
```

```text
INITIALIZE_REQUEST_JSON_SHA256=8ee5a7ecadcafe168a3f51d480d143fef32cd25a0157327845657f896370ff93
OFFERED_PROTOCOL_VERSION=2025-11-25
```

### 5.2 Initialize response (byte-exact SSE body)

HTTP 200. Finished at `2026-08-18T10:10:10Z`.

```text
event: message
data: {"result":{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"ghl-mcp","version":"1.0.0"}},"jsonrpc":"2.0","id":1}
```

```text
INITIALIZE_RESPONSE_SSE_SHA256=30bd5115210b5c8fb248a21e55f82904e8f8f25beb3a89a8f96718256dd22e40
```

Parsed JSON-RPC payload (same bytes as the SSE `data:` line; pretty-printed
only for review):

```json
{
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "ghl-mcp",
      "version": "1.0.0"
    }
  },
  "jsonrpc": "2.0",
  "id": 1
}
```

```text
INITIALIZE_RESPONSE_JSON_JCS_SHA256=696ea38a6f9320d096364bb4f5df32d0f7a200c9622db3cf9c4321d2931c0d75
NEGOTIATED_PROTOCOL_VERSION=2025-11-25
PROTOCOL_VERSION_MATCH=YES
SERVER_INFO_NAME=ghl-mcp
SERVER_INFO_VERSION=1.0.0
CAPABILITIES_JSON={"tools":{}}
REQUEST_RESPONSE_ID_BINDING=YES (id=1)
```

### 5.3 Sanitized initialize response headers

```text
HTTP/2 200 
date: Tue, 18 Aug 2026 10:10:10 GMT
content-type: text/event-stream
content-length: 167
cf-ray: a2d020923cb60f96-ORD
cf-cache-status: DYNAMIC
access-control-allow-origin: *
cache-control: no-cache
server: cloudflare
strict-transport-security: max-age=31536000
vary: Origin, Authorization, Accept-Encoding
access-control-max-age: 31536000
x-content-type-options: nosniff
x-content-type-options: nosniff
access-control-allow-headers: Content-Type, Authorization, Accept, locationId, MCP-Protocol-Version, Mcp-Session-Id, Last-Event-ID, X-Anthropic-Client
access-control-allow-methods: GET, HEAD, POST, OPTIONS
access-control-expose-headers: WWW-Authenticate, MCP-Protocol-Version, Mcp-Session-Id
timing-allow-origin: *
x-envoy-upstream-service-time: 4
set-cookie: ***REDACTED***
```

Cookie values and any credential material are redacted. No
`Mcp-Session-Id` header was present.

### 5.4 Initialize evidence digest subject

RFC 8785 JSON-canonicalized initialize evidence object (includes offered
version, request, response, and transport metadata):

```text
INITIALIZE_EVIDENCE_JCS_SHA256=f85fa7295e7ab505581f3c23b13b397787e6d68c2847dd5bcdbe961e9b661ee4
JCS_IMPLEMENTATION=local_minimal_rfc8785_subset_no_floats
```

Canonical bytes:

```text
{"offeredProtocolVersion":"2025-11-25","request":{"id":1,"jsonrpc":"2.0","method":"initialize","params":{"capabilities":{},"clientInfo":{"name":"mg-guide-nw008-at1-pregrant-observation","version":"0.0.1"},"protocolVersion":"2025-11-25"}},"response":{"id":1,"jsonrpc":"2.0","result":{"capabilities":{"tools":{}},"protocolVersion":"2025-11-25","serverInfo":{"name":"ghl-mcp","version":"1.0.0"}}},"transport":{"class":"streamable_http_sse","endpoint":"https://services.leadconnectorhq.com/mcp/anthropic/v2","httpStatus":200,"mcpProtocolVersionHeaderOnInitialize":null,"mcpSessionIdObserved":false,"responseContentType":"text/event-stream"}}
```

### 5.5 Version gate

```text
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
NEGOTIATED_PROTOCOL_VERSION=2025-11-25
PROTOCOL_VERSION_MATCH=YES
FAIL_CLOSED=NO
TOOLS_LIST_AUTHORIZED_BY_VERSION_GATE=YES
```

Because the negotiated version exactly matched the frozen supported version,
exactly one bounded `tools/list` pagination sequence proceeded.

## 6. tools/list pagination sequence

### 6.1 Sequence bounds

```text
MCP_TOOLS_LIST_SEQUENCES=1
MCP_TOOLS_LIST_REQUESTS=1
NEXT_CURSOR_PRESENT_ON_FINAL_PAGE=NO
PAGINATION_COMPLETE=YES
RETRY_USED=NO
SECOND_CATALOG_SEQUENCE=NO
```

### 6.2 Request 01 (byte-exact JSON body)

Request id: `2`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

```text
TOOLS_LIST_REQUEST_01_JSON_SHA256=aa4597ff6cde6df7ad1134bdbeefe00d234cc87c2a4db91b43c0f5b0b4c6063e
MCP_PROTOCOL_VERSION_HEADER=2025-11-25
```

### 6.3 Response 01 (byte-exact SSE body)

HTTP 200. Started `2026-08-18T10:10:39Z`; finished
`2026-08-18T10:10:39Z`.

```text
event: message
data: {"result":{"tools":[{"name":"search_operations","description":"Find an executable GHL public API operation, including operations that search for specific records by name, email, phone, or other fields. Call describe_operation for the selected operationId when hasRequestBody is true or params are unclear, then call execute_operation.","inputSchema":{"type":"object","additionalProperties":false,"properties":{"query":{"type":"string","description":"Natural language operation search query."},"domains":{"type":"array","items":{"type":"string"},"description":"Optional operation domains to constrain search."},"kind":{"type":"string","enum":["read","write","delete","money_movement"],"description":"Optional operation kind filter."},"limit":{"type":"number","description":"Maximum operation result count."}},"required":["query"]},"annotations":{"title":"Search Operations","readOnlyHint":true,"destructiveHint":false,"idempotentHint":true,"openWorldHint":false}},{"name":"describe_operation","description":"Inspect one operationId from search_operations. Returns compact public params, requestBodyFields, one sanitized payloadExample, scopes, safety metadata, and idempotency constraints before calling execute_operation.","inputSchema":{"type":"object","additionalProperties":false,"properties":{"operationId":{"type":"string","description":"Operation ID returned by search_operations."}},"required":["operationId"]},"annotations":{"title":"Describe Operation","readOnlyHint":true,"destructiveHint":false,"idempotentHint":true,"openWorldHint":false}},{"name":"execute_operation","description":"Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.","inputSchema":{"type":"object","additionalProperties":false,"properties":{"operationId":{"type":"string","description":"Operation ID returned by search_operations."},"params":{"type":"object","description":"Path, query, header, and body params for the operation."},"locationId":{"type":"string","description":"Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options."},"dryRun":{"type":"boolean","description":"When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract."},"idempotencyKey":{"type":"string","description":"Required for writes before broad rollout."},"reason":{"type":"string","description":"Short user-facing reason for the operation."}},"required":["operationId"]},"annotations":{"title":"Execute Operation","readOnlyHint":false,"destructiveHint":false,"idempotentHint":false,"openWorldHint":false}},{"name":"list_locations","description":"List the sub-accounts (locations) this connection can operate on, so the user can pick one. When the user names a location, pass `query` with that name instead of paginating. When many locations exist and none was named, ask the user which one rather than enumerating pages. Returns location names and ids only — never credentials. On a single-location connection this returns exactly the one bound location.","inputSchema":{"type":"object","additionalProperties":false,"properties":{"query":{"type":"string","description":"Optional name search to narrow the returned locations."},"pageToken":{"type":"string","description":"Opaque pagination token from a previous list_locations response."}}},"annotations":{"title":"List Locations","readOnlyHint":true,"destructiveHint":false,"idempotentHint":true,"openWorldHint":false}}]},"jsonrpc":"2.0","id":2}
```

```text
TOOLS_LIST_RESPONSE_01_SSE_SHA256=6522edcc63c7c19bef1114322bd3e07943352f5d5e2716f52267d1569a210a6e
```

Parsed JSON-RPC payload (pretty-printed for review; digest subjects use the
canonical forms below):

```json
{
  "result": {
    "tools": [
      {
        "name": "search_operations",
        "description": "Find an executable GHL public API operation, including operations that search for specific records by name, email, phone, or other fields. Call describe_operation for the selected operationId when hasRequestBody is true or params are unclear, then call execute_operation.",
        "inputSchema": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "query": {
              "type": "string",
              "description": "Natural language operation search query."
            },
            "domains": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Optional operation domains to constrain search."
            },
            "kind": {
              "type": "string",
              "enum": [
                "read",
                "write",
                "delete",
                "money_movement"
              ],
              "description": "Optional operation kind filter."
            },
            "limit": {
              "type": "number",
              "description": "Maximum operation result count."
            }
          },
          "required": [
            "query"
          ]
        },
        "annotations": {
          "title": "Search Operations",
          "readOnlyHint": true,
          "destructiveHint": false,
          "idempotentHint": true,
          "openWorldHint": false
        }
      },
      {
        "name": "describe_operation",
        "description": "Inspect one operationId from search_operations. Returns compact public params, requestBodyFields, one sanitized payloadExample, scopes, safety metadata, and idempotency constraints before calling execute_operation.",
        "inputSchema": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "operationId": {
              "type": "string",
              "description": "Operation ID returned by search_operations."
            }
          },
          "required": [
            "operationId"
          ]
        },
        "annotations": {
          "title": "Describe Operation",
          "readOnlyHint": true,
          "destructiveHint": false,
          "idempotentHint": true,
          "openWorldHint": false
        }
      },
      {
        "name": "execute_operation",
        "description": "Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.",
        "inputSchema": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "operationId": {
              "type": "string",
              "description": "Operation ID returned by search_operations."
            },
            "params": {
              "type": "object",
              "description": "Path, query, header, and body params for the operation."
            },
            "locationId": {
              "type": "string",
              "description": "Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options."
            },
            "dryRun": {
              "type": "boolean",
              "description": "When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract."
            },
            "idempotencyKey": {
              "type": "string",
              "description": "Required for writes before broad rollout."
            },
            "reason": {
              "type": "string",
              "description": "Short user-facing reason for the operation."
            }
          },
          "required": [
            "operationId"
          ]
        },
        "annotations": {
          "title": "Execute Operation",
          "readOnlyHint": false,
          "destructiveHint": false,
          "idempotentHint": false,
          "openWorldHint": false
        }
      },
      {
        "name": "list_locations",
        "description": "List the sub-accounts (locations) this connection can operate on, so the user can pick one. When the user names a location, pass `query` with that name instead of paginating. When many locations exist and none was named, ask the user which one rather than enumerating pages. Returns location names and ids only — never credentials. On a single-location connection this returns exactly the one bound location.",
        "inputSchema": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "query": {
              "type": "string",
              "description": "Optional name search to narrow the returned locations."
            },
            "pageToken": {
              "type": "string",
              "description": "Opaque pagination token from a previous list_locations response."
            }
          }
        },
        "annotations": {
          "title": "List Locations",
          "readOnlyHint": true,
          "destructiveHint": false,
          "idempotentHint": true,
          "openWorldHint": false
        }
      }
    ]
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

```text
TOOLS_LIST_RESPONSE_01_JSON_JCS_SHA256=2c8296ebaa4657ab658f95dfa1dffdf308fc4ad1a4c33628d83b4a6d280d45c8
REQUEST_RESPONSE_ID_BINDING=YES (id=2)
TOOL_COUNT=4
TOOL_NAMES_IN_PROVIDER_ORDER=search_operations,describe_operation,execute_operation,list_locations
NEXT_CURSOR=ABSENT
```

### 6.4 Sanitized tools/list response headers

```text
HTTP/2 200 
date: Tue, 18 Aug 2026 10:10:39 GMT
content-type: text/event-stream
cf-ray: a2d02142de05f7fc-ORD
cf-cache-status: DYNAMIC
access-control-allow-origin: *
cache-control: no-cache
set-cookie: ***REDACTED***
server: cloudflare
strict-transport-security: max-age=31536000
vary: Origin, Authorization, Accept-Encoding
access-control-max-age: 31536000
x-content-type-options: nosniff
x-content-type-options: nosniff
access-control-allow-headers: Content-Type, Authorization, Accept, locationId, MCP-Protocol-Version, Mcp-Session-Id, Last-Event-ID, X-Anthropic-Client
access-control-allow-methods: GET, HEAD, POST, OPTIONS
access-control-expose-headers: WWW-Authenticate, MCP-Protocol-Version, Mcp-Session-Id
timing-allow-origin: *
x-envoy-upstream-service-time: 5
```

### 6.5 Ordered catalog evidence digest

Complete ordered catalog evidence (single-page sequence, provider order
preserved):

```text
ORDERED_CATALOG_EVIDENCE_JCS_SHA256=f267a76409d81a8694e3af43cf6429b20b6a168e5ab3fb1f599006a0d6812429
```

Canonical bytes:

```text
{"paginationComplete":true,"requests":[{"httpStatus":200,"nextCursorPresent":false,"ordinal":1,"request":{"id":2,"jsonrpc":"2.0","method":"tools/list","params":{}},"response":{"id":2,"jsonrpc":"2.0","result":{"tools":[{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"Search Operations"},"description":"Find an executable GHL public API operation, including operations that search for specific records by name, email, phone, or other fields. Call describe_operation for the selected operationId when hasRequestBody is true or params are unclear, then call execute_operation.","inputSchema":{"additionalProperties":false,"properties":{"domains":{"description":"Optional operation domains to constrain search.","items":{"type":"string"},"type":"array"},"kind":{"description":"Optional operation kind filter.","enum":["read","write","delete","money_movement"],"type":"string"},"limit":{"description":"Maximum operation result count.","type":"number"},"query":{"description":"Natural language operation search query.","type":"string"}},"required":["query"],"type":"object"},"name":"search_operations"},{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"Describe Operation"},"description":"Inspect one operationId from search_operations. Returns compact public params, requestBodyFields, one sanitized payloadExample, scopes, safety metadata, and idempotency constraints before calling execute_operation.","inputSchema":{"additionalProperties":false,"properties":{"operationId":{"description":"Operation ID returned by search_operations.","type":"string"}},"required":["operationId"],"type":"object"},"name":"describe_operation"},{"annotations":{"destructiveHint":false,"idempotentHint":false,"openWorldHint":false,"readOnlyHint":false,"title":"Execute Operation"},"description":"Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.","inputSchema":{"additionalProperties":false,"properties":{"dryRun":{"description":"When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract.","type":"boolean"},"idempotencyKey":{"description":"Required for writes before broad rollout.","type":"string"},"locationId":{"description":"Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options.","type":"string"},"operationId":{"description":"Operation ID returned by search_operations.","type":"string"},"params":{"description":"Path, query, header, and body params for the operation.","type":"object"},"reason":{"description":"Short user-facing reason for the operation.","type":"string"}},"required":["operationId"],"type":"object"},"name":"execute_operation"},{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"List Locations"},"description":"List the sub-accounts (locations) this connection can operate on, so the user can pick one. When the user names a location, pass `query` with that name instead of paginating. When many locations exist and none was named, ask the user which one rather than enumerating pages. Returns location names and ids only — never credentials. On a single-location connection this returns exactly the one bound location.","inputSchema":{"additionalProperties":false,"properties":{"pageToken":{"description":"Opaque pagination token from a previous list_locations response.","type":"string"},"query":{"description":"Optional name search to narrow the returned locations.","type":"string"}},"type":"object"},"name":"list_locations"}]}},"responseContentType":"text/event-stream"}],"sequence":1,"toolNamesInProviderOrder":["search_operations","describe_operation","execute_operation","list_locations"],"toolsInProviderOrder":[{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"Search Operations"},"description":"Find an executable GHL public API operation, including operations that search for specific records by name, email, phone, or other fields. Call describe_operation for the selected operationId when hasRequestBody is true or params are unclear, then call execute_operation.","inputSchema":{"additionalProperties":false,"properties":{"domains":{"description":"Optional operation domains to constrain search.","items":{"type":"string"},"type":"array"},"kind":{"description":"Optional operation kind filter.","enum":["read","write","delete","money_movement"],"type":"string"},"limit":{"description":"Maximum operation result count.","type":"number"},"query":{"description":"Natural language operation search query.","type":"string"}},"required":["query"],"type":"object"},"name":"search_operations"},{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"Describe Operation"},"description":"Inspect one operationId from search_operations. Returns compact public params, requestBodyFields, one sanitized payloadExample, scopes, safety metadata, and idempotency constraints before calling execute_operation.","inputSchema":{"additionalProperties":false,"properties":{"operationId":{"description":"Operation ID returned by search_operations.","type":"string"}},"required":["operationId"],"type":"object"},"name":"describe_operation"},{"annotations":{"destructiveHint":false,"idempotentHint":false,"openWorldHint":false,"readOnlyHint":false,"title":"Execute Operation"},"description":"Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.","inputSchema":{"additionalProperties":false,"properties":{"dryRun":{"description":"When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract.","type":"boolean"},"idempotencyKey":{"description":"Required for writes before broad rollout.","type":"string"},"locationId":{"description":"Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options.","type":"string"},"operationId":{"description":"Operation ID returned by search_operations.","type":"string"},"params":{"description":"Path, query, header, and body params for the operation.","type":"object"},"reason":{"description":"Short user-facing reason for the operation.","type":"string"}},"required":["operationId"],"type":"object"},"name":"execute_operation"},{"annotations":{"destructiveHint":false,"idempotentHint":true,"openWorldHint":false,"readOnlyHint":true,"title":"List Locations"},"description":"List the sub-accounts (locations) this connection can operate on, so the user can pick one. When the user names a location, pass `query` with that name instead of paginating. When many locations exist and none was named, ask the user which one rather than enumerating pages. Returns location names and ids only — never credentials. On a single-location connection this returns exactly the one bound location.","inputSchema":{"additionalProperties":false,"properties":{"pageToken":{"description":"Opaque pagination token from a previous list_locations response.","type":"string"},"query":{"description":"Optional name search to narrow the returned locations.","type":"string"}},"type":"object"},"name":"list_locations"}],"toolsListRequestCount":1}
```

## 7. execute_operation advertisement

### 7.1 Presence

```text
EXECUTE_OPERATION_TOOL_PRESENT=YES
EXECUTE_OPERATION_CATALOG_ORDINAL=3
EXECUTE_OPERATION_INPUT_SCHEMA_CAPTURED=YES
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
EXECUTE_OPERATION_OUTPUT_SCHEMA_MEMBER=ABSENT
EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE
```

`outputSchema` was not a member of the advertised tool descriptor. No schema
was inferred. No RFC 8785 schema digest subject of the form
`{"inputSchema":...,"outputSchema":...}` is emitted because `outputSchema`
is absent.

### 7.2 Exact advertised descriptor

Exact provider-returned `execute_operation` object (pretty-printed):

```json
{
  "name": "execute_operation",
  "description": "Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "operationId": {
        "type": "string",
        "description": "Operation ID returned by search_operations."
      },
      "params": {
        "type": "object",
        "description": "Path, query, header, and body params for the operation."
      },
      "locationId": {
        "type": "string",
        "description": "Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options."
      },
      "dryRun": {
        "type": "boolean",
        "description": "When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract."
      },
      "idempotencyKey": {
        "type": "string",
        "description": "Required for writes before broad rollout."
      },
      "reason": {
        "type": "string",
        "description": "Short user-facing reason for the operation."
      }
    },
    "required": [
      "operationId"
    ]
  },
  "annotations": {
    "title": "Execute Operation",
    "readOnlyHint": false,
    "destructiveHint": false,
    "idempotentHint": false,
    "openWorldHint": false
  }
}
```

RFC 8785 JSON-canonicalized exact descriptor bytes and digest:

```text
EXECUTE_OPERATION_DESCRIPTOR_JCS_SHA256=8802c3d1077e9733564762cc1e624eb178bb7694cd09f6410f20447d12561884
```

```text
{"annotations":{"destructiveHint":false,"idempotentHint":false,"openWorldHint":false,"readOnlyHint":false,"title":"Execute Operation"},"description":"Execute one active operation from the generated GHL public operation registry after server-side scope, permission, safety, idempotency, and tenant checks. Params may be grouped as {path, query, header, body} or provided flat; the server maps known path/query/body fields and applies Authorization and Version. Location handling depends on the connection: a single-location connection injects its bound location automatically; a multi-location connection requires locationId (call list_locations first) and authorizes it before executing. Call describe_operation first when the body or params are unclear.","inputSchema":{"additionalProperties":false,"properties":{"dryRun":{"description":"When true, preview the operation and supplied params without upstream execution or idempotencyKey. Use describe_operation for the request body contract.","type":"boolean"},"idempotencyKey":{"description":"Required for writes before broad rollout.","type":"string"},"locationId":{"description":"Sub-account (location) to operate on. Omit if this connection is bound to a single location. Required when connected to multiple locations — call list_locations to see options.","type":"string"},"operationId":{"description":"Operation ID returned by search_operations.","type":"string"},"params":{"description":"Path, query, header, and body params for the operation.","type":"object"},"reason":{"description":"Short user-facing reason for the operation.","type":"string"}},"required":["operationId"],"type":"object"},"name":"execute_operation"}
```

### 7.3 inputSchema members observed

```text
INPUT_SCHEMA_TYPE=object
INPUT_SCHEMA_ADDITIONAL_PROPERTIES=false
INPUT_SCHEMA_REQUIRED=operationId
INPUT_SCHEMA_PROPERTIES=operationId,params,locationId,dryRun,idempotencyKey,reason
OUTPUT_SCHEMA=ABSENT
```

## 8. Caps and prohibitions compliance

| Cap / rule | Required | Observed |
| --- | --- | --- |
| `MCP_INITIALIZE_CALLS` | <=1 | 1 |
| `MCP_TOOLS_LIST_SEQUENCES` | <=1 | 1 |
| `MCP_TOOLS_LIST_REQUESTS` | pagination-bounded | 1 |
| `MCP_EXECUTE_OPERATION_CALLS` | 0 | 0 |
| `GHL_BUSINESS_READS` | 0 | 0 |
| `GHL_MUTATIONS` | 0 | 0 |
| `GRANT009_EXECUTIONS` | 0 | 0 |
| `tools/call` | FORBIDDEN | not issued |
| `execute_operation` call | FORBIDDEN | not issued |
| `get-contact` / `get-opportunity` / `create-note` / `get-note` / `update-opportunity` | FORBIDDEN | not issued |
| any other advertised tool call | FORBIDDEN | not issued |
| raw REST | FORBIDDEN | not used |
| parser/session/runtime implementation | FORBIDDEN | not performed |
| IAM / secret / deployment changes | FORBIDDEN | not performed |
| protocol downgrade / version selection | FORBIDDEN | offered only 2025-11-25; accepted exact match |
| retry creating second catalog sequence | FORBIDDEN | not performed |
| private/customer data in proof | FORBIDDEN | none |

```text
DID_NOT_CALL_TOOLS_CALL=YES
DID_NOT_CALL_EXECUTE_OPERATION=YES
DID_NOT_CALL_SEARCH=YES
DID_NOT_CALL_FETCH=YES
DID_NOT_CALL_SEARCH_OPERATIONS=YES
DID_NOT_CALL_DESCRIBE_OPERATION=YES
DID_NOT_CALL_LIST_LOCATIONS=YES
DID_NOT_RAW_REST=YES
DID_NOT_IMPLEMENT_PARSER_OR_RUNTIME=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_CHANGE_IAM_SECRETS_OR_DEPLOYMENT=YES
DID_NOT_DOWNGRADE_PROTOCOL_VERSION=YES
```

## 9. Digest register

```text
INITIALIZE_REQUEST_JSON_SHA256=8ee5a7ecadcafe168a3f51d480d143fef32cd25a0157327845657f896370ff93
INITIALIZE_RESPONSE_SSE_SHA256=30bd5115210b5c8fb248a21e55f82904e8f8f25beb3a89a8f96718256dd22e40
INITIALIZE_RESPONSE_JSON_JCS_SHA256=696ea38a6f9320d096364bb4f5df32d0f7a200c9622db3cf9c4321d2931c0d75
INITIALIZE_EVIDENCE_JCS_SHA256=f85fa7295e7ab505581f3c23b13b397787e6d68c2847dd5bcdbe961e9b661ee4
TOOLS_LIST_REQUEST_01_JSON_SHA256=aa4597ff6cde6df7ad1134bdbeefe00d234cc87c2a4db91b43c0f5b0b4c6063e
TOOLS_LIST_RESPONSE_01_SSE_SHA256=6522edcc63c7c19bef1114322bd3e07943352f5d5e2716f52267d1569a210a6e
TOOLS_LIST_RESPONSE_01_JSON_JCS_SHA256=2c8296ebaa4657ab658f95dfa1dffdf308fc4ad1a4c33628d83b4a6d280d45c8
ORDERED_CATALOG_EVIDENCE_JCS_SHA256=f267a76409d81a8694e3af43cf6429b20b6a168e5ab3fb1f599006a0d6812429
EXECUTE_OPERATION_DESCRIPTOR_JCS_SHA256=8802c3d1077e9733564762cc1e624eb178bb7694cd09f6410f20447d12561884
EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE
JCS_IMPLEMENTATION=local_minimal_rfc8785_subset_no_floats
```

Byte-exact SSE bodies and the canonical digest subjects above are retained in
this proof so a reviewer can reproduce every digest without consulting sample
business responses.

## 10. Freeze decision after observation

```text
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES
PROTOCOL_VERSION_MATCH=YES

MCP_ADVERTISED_SCHEMA_SUPPORTED_BY_SELECTED_VERSION=YES
PREGRANT_ADVERTISED_SCHEMA_PATH_ELIGIBLE=YES

EXECUTE_OPERATION_TOOL_PRESENT=YES
EXECUTE_OPERATION_INPUT_SCHEMA_CAPTURED=YES
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE

HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

The conditional pre-grant advertised-schema authority path remains eligible at
the MCP-spec layer, but this observation did not obtain a provider-advertised
`outputSchema` for `execute_operation`. Provider-wrapper freeze is therefore
not established by this unit. No grant-009-class authorization is drafted or
executed here.

## 11. STOP

```text
STOP_REASON=OBSERVATION_COMPLETE_CATALOG_CAPTURED_OUTPUT_SCHEMA_ABSENT
FAIL_CLOSED=NO
MCP_INITIALIZE_CALLS=1
MCP_TOOLS_LIST_SEQUENCES=1
MCP_TOOLS_LIST_REQUESTS=1
MCP_EXECUTE_OPERATION_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
GRANT009_EXECUTIONS=0
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
PARSER_RUNTIME_IMPLEMENTATION=NOT_PERFORMED
NEXT=HUMAN_REVIEW_OF_EXECUTION_PROOF
```
