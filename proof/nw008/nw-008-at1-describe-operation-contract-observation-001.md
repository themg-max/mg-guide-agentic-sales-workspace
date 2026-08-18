# NW-008 AT-1 Describe Operation Contract Observation 001

## 1. Execution identity and authority binding

```text
CLASSIFICATION=execution_proof
ARTIFACT_KIND=DESCRIBE_OPERATION_CONTRACT_OBSERVATION_RESULT
PROOF_ID=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001
OWNER=VS Code / MG Orchestrator
PROOF_BRANCH=proof/nw008-at1-describe-operation-contract-observation-001
PROOF_BASE_REF=origin/main
PROOF_BASE_SHA=f40ffa65cfa36fdf9a9d8486888f600f23465ae1

AUTHORIZATION_ID=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001
AUTHORIZATION_PATH=governance/authorizations/nw008-at1-describe-operation-contract-observation-001.md
AUTHORIZATION_PR81=81
PR81_AUTHORIZATION_REVIEWED_HEAD=6c4256e6872fcf0f3cef0b52618cd6d1e9c959bc
PR81_AUTHORIZATION_MERGE_SHA=44f3daadf4e3d2dfd10d0fe3c180a7f425f39029
PR82_REFINEMENT_REVIEWED_HEAD=61cb37e9d48c95e0e34aa7db489225236a3b355c
PR82_REFINEMENT_MERGE_SHA=f40ffa65cfa36fdf9a9d8486888f600f23465ae1
PR82_REFINED_EVIDENCE_RULES_EFFECTIVE=YES

SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25

OBSERVATION_STARTED_AT_UTC=2026-08-18T11:32:10Z
INITIALIZE_STARTED_AT_UTC=2026-08-18T11:32:12Z
INITIALIZE_FINISHED_AT_UTC=2026-08-18T11:32:12Z
OBSERVATION_FINISHED_AT_UTC=2026-08-18T11:32:12Z
RECORDED_AT_UTC=2026-08-18T11:33:36Z

OBSERVATION_EXECUTION_OCCURRED=YES
OBSERVATION_AUTHORITY_CONSUMED=YES
FAIL_CLOSED=YES
```

This unit is the single authorized execution of the merged
describe-operation contract observation (PR #81 authority, PR #82 refined
evidence rules). The one-shot authority was consumed when the `initialize`
request was transmitted at `2026-08-18T11:32:12Z`. The observation stopped
immediately on the first fail-closed condition. No `execute_operation`, no
GHL business read or mutation, no raw REST, no implementation work, and no
Grant009 activity occurred.

## 2. Preflight

Executed before the observation, in this order: `pwd`
(`/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace`),
`git branch --show-current`
(`auth/nw008-at1-describe-operation-contract-observation-001`, not `main`),
`git status --short --untracked-files=all` (empty), `git fetch origin`.

| Precondition | Result |
| --- | --- |
| Working branch is not `main` at execution start | YES (`auth/nw008-at1-describe-operation-contract-observation-001`) |
| `git fetch origin` completed | YES |
| PR #82 reviewed head `61cb37e9d48c95e0e34aa7db489225236a3b355c` is ancestor of `origin/main` | YES (`git merge-base --is-ancestor` exit 0) |
| PR #82 merge commit on `origin/main` | `f40ffa65cfa36fdf9a9d8486888f600f23465ae1` (equals `origin/main` tip) |
| Refined authorization artifact present on `origin/main` | YES (`git cat-file -e` exit 0) |
| Worktree clean at execution start | YES |
| Execution lane separate from `main` | YES (execution recorded on `proof/nw008-at1-describe-operation-contract-observation-001`, created from fetched `origin/main`) |

```text
PR82_REVIEWED_HEAD=61cb37e9d48c95e0e34aa7db489225236a3b355c
PR82_MERGE_SHA=f40ffa65cfa36fdf9a9d8486888f600f23465ae1
PR82_MAIN_REACHABLE=YES
AUTHORIZATION_ON_MAIN=YES
WORKTREE_CLEAN_AT_START=YES
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
SESSION_IDENTIFIER_IN_PROOF=NO
TRANSPORT_CLIENT=python_urllib_stdlib (Python 3.9.6, default User-Agent)
```

Request headers sent (names only, values non-secret except redacted
credential): `Content-Type: application/json`,
`Accept: application/json, text/event-stream`, `Authorization: Bearer
***REDACTED***`. The `MCP-Protocol-Version` and `Mcp-Session-Id` headers were
never sent: the protocol header is only required after a successful
initialize, and no session identifier was issued.

## 4. Execution lifecycle and fail-closed stop

| Step | Budget | Attempted | Outcome |
| --- | --- | --- | --- |
| `initialize` (id `1`) | 1 | 1 | HTTP 403 Cloudflare edge error 1010; no JSON-RPC envelope |
| `notifications/initialized` | 1 | 0 | NOT_SENT (version gate never passed) |
| `describe_operation` x5 | 5 | 0 | NOT_OBSERVED (fail-closed stop before first call) |

The `initialize` request was transmitted once at `2026-08-18T11:32:12Z`. The
response was an HTTP 403 produced at the Cloudflare edge
(`error_code: 1010`, `error_name: browser_signature_banned`,
`retryable: false`), not an MCP/JSON-RPC response. Under authorization
section 6 this is a terminal fail-closed condition (no capturable JSON-RPC
response; negotiated protocol version unavailable). The authorization permits
no retry, no replacement call, no second session, and no second `initialize`
(`MCP_INITIALIZE_CALLS_MAX=1`, `MCP_SESSION_RESTARTS_MAX=0`). The edge
response body itself also instructs `**Do not retry.**`. The unit therefore
stopped immediately after the first completed HTTP exchange.

```text
OBSERVATION_EXECUTION_OCCURRED=YES
OBSERVATION_AUTHORITY_CONSUMED=YES
MCP_INITIALIZE_CALLS=1
MCP_INITIALIZED_NOTIFICATIONS=0
MCP_DESCRIBE_OPERATION_CALLS=0
FAIL_CLOSED=YES
FAIL_CLOSED_CONDITION=INITIALIZE_RESPONSE_NOT_JSONRPC_HTTP_403_CLOUDFLARE_ERROR_1010
RETRY_ATTEMPTED=NO
REPLACEMENT_CALL_ATTEMPTED=NO
SECOND_SESSION_ATTEMPTED=NO
```

## 5. Initialize exchange (only transmitted call)

### 5.1 Offered request (byte-exact JSON body)

Request id: `1`. Pre-transmission SHA-256 was computed over the exact bytes
below before sending.

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mg-guide-nw008-at1-describe-operation-observation","version":"0.0.1"}}}
```

```text
INITIALIZE_REQUEST_JSON_SHA256=12bcd905da9c686cd3b3d642a9349ecf96350e18a614a2847a834016b3f6951f
OFFERED_PROTOCOL_VERSION=2025-11-25
```

### 5.2 Initialize response (byte-exact body)

HTTP 403. Started `2026-08-18T11:32:12Z`; finished `2026-08-18T11:32:12Z`.
`Content-Type: application/json; charset=utf-8`. 718 bytes, including the
trailing newline shown.

```json
{"type":"https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/error-1010/","title":"Error 1010: Access denied","status":403,"detail":"The site owner has blocked access based on your browser's signature.","instance":"a2d098b80e25eac0","error_code":1010,"error_name":"browser_signature_banned","error_category":"access_denied","ray_id":"a2d098b80e25eac0","timestamp":"2026-08-18T11:32:12Z","zone":"services.leadconnectorhq.com","cloudflare_error":true,"retryable":false,"owner_action_required":true,"what_you_should_do":"**Do not retry.** Your user-agent has been banned by the site owner.","footer":"This error was generated by Cloudflare on behalf of the website owner."}
```

```text
INITIALIZE_RESPONSE_RAW_SHA256=a1b5d6aaacbb4ca7eaa1c3d2675b019b858f3a08fbe4c013ae27e487f4410450
INITIALIZE_RESPONSE_BYTES=718
INITIALIZE_RESPONSE_CONTENT_TYPE=application/json; charset=utf-8
INITIALIZE_RESPONSE_SSE_FRAMING=NO
INITIALIZE_RESPONSE_JSONRPC_ENVELOPE=ABSENT
INITIALIZE_RESPONSE_JSON_JCS_SHA256=NOT_AVAILABLE
NEGOTIATED_PROTOCOL_VERSION=NOT_NEGOTIATED
PROTOCOL_VERSION_MATCH=NOT_NEGOTIATED
REQUEST_RESPONSE_ID_BINDING=NOT_OBSERVABLE
SERVER_INFO=NOT_OBSERVED
CAPABILITIES=NOT_OBSERVED
```

The body is an edge-generated error document, not a JSON-RPC envelope; no
`result`, `error`, `id`, or `jsonrpc` member exists to parse as an MCP
message. No JCS digest is computed over it as an MCP payload; the raw
byte-exact digest above is the transport evidence. No `Mcp-Session-Id`
response header was present.

### 5.3 Sanitized initialize response headers

```text
HTTP 403
date: Tue, 18 Aug 2026 11:32:12 GMT
content-type: application/json; charset=utf-8
content-length: 718
connection: close
cache-control: private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0
expires: Thu, 01 Jan 1970 00:00:01 GMT
referrer-policy: same-origin
x-frame-options: SAMEORIGIN
set-cookie: ***REDACTED***
access-control-max-age: 31536000
x-content-type-options: nosniff
server: cloudflare
cf-ray: a2d098b80e25eac0-ORD
```

Cookie values are redacted. No `Mcp-Session-Id` header was present. `cf-ray`,
`instance`, and `ray_id` are provider edge diagnostic identifiers, not
tenant, customer, credential, or session material.

### 5.4 Version gate

```text
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
NEGOTIATED_PROTOCOL_VERSION=NOT_NEGOTIATED
PROTOCOL_VERSION_MATCH=NOT_NEGOTIATED
VERSION_GATE_PASSED=NO
DESCRIBE_OPERATION_AUTHORIZED_BY_VERSION_GATE=NO
FAIL_CLOSED=YES
```

Because no protocol version was negotiated, the protocol-required
`notifications/initialized` message was not sent and none of the five
`describe_operation` calls was attempted.

## 6. Initialized notification

```text
INITIALIZED_NOTIFICATION_SENT=NO
INITIALIZED_NOTIFICATION_HTTP_STATUS=NOT_SENT
INITIALIZED_NOTIFICATION_RESPONSE_BODY_SHA256=NOT_SENT
MCP_INITIALIZED_NOTIFICATIONS=0
```

Pre-computed request digest (body never transmitted):

```text
INITIALIZED_NOTIFICATION_REQUEST_JSON_SHA256=59951ca0b212b103876fa23a9e58bcbbc8fbcc0120e3f5ee7214461e2bd1cd5e
INITIALIZED_NOTIFICATION_TRANSMITTED=NO
```

## 7. describe_operation calls 1-5: NOT_OBSERVED

No `describe_operation` call was transmitted. All five calls are recorded
`NOT_OBSERVED` per the authorization ("Unattempted calls must be marked
`NOT_OBSERVED`; no replacement call is authorized"). Pre-transmission
SHA-256 digests of the exact authorized request bodies were computed before
the observation began; the bodies were never sent.

| Call ordinal | JSON-RPC id | Exact operation ID | Request SHA-256 (pre-computed) | Transmitted |
| --- | --- | --- | --- | --- |
| 1 | `2` | `get-contact` | `09b35192af7746a172e06c388d609036942ee1a98b9816a3a3f4e478d361db9c` | NO |
| 2 | `3` | `get-opportunity` | `c5516f5e8d8dcdf0cda0e668842718124fbc4afe28b99300d0adb0fedf81ce51` | NO |
| 3 | `4` | `create-note` | `dd056c3a36f3aed64936138c0d34de5841b9edf0df7af82a9ba63fe9535c1655` | NO |
| 4 | `5` | `get-note` | `fae7afb695516bb7df7f8f6ceacfef617914e8ac1158db370a0e94edf3df469a` | NO |
| 5 | `6` | `update-opportunity` | `e5a72f51b3746206d7e171dc9b95b168b11395d639ad821db9d4738082f80a95` | NO |

### 7.1 Per-operation result-representation summaries

For each of the five operations (`get-contact`, `get-opportunity`,
`create-note`, `get-note`, `update-opportunity`), identically:

```text
DESCRIBE_OPERATION_RESULT_REPRESENTATION=NOT_OBSERVED
DESCRIBE_OPERATION_METADATA_PARSE_MODE=NONE
CONTENT_TEXT_SHA256=NOT_AVAILABLE
OUTER_JSON_POINTER=NONE
INNER_VALUE_JCS_SHA256=NOT_AVAILABLE
CALLTOOLRESULT_JCS_SHA256=NOT_AVAILABLE
DESCRIBE_OPERATION_INPUT_SCHEMA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_RESPONSE_SCHEMA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_SUCCESS_METADATA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_ERROR_METADATA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_PAYLOAD_EXAMPLE_ONLY=NOT_OBSERVED
```

`DESCRIBE_OPERATION_METADATA_PARSE_MODE=NONE` per authorization section 7.1:
no JSON metadata object is available to inventory because no tool result was
captured.

### 7.2 Required metadata field inventory (all five operations)

No `CallToolResult` was captured for any operation, so every required field
row is `NOT_OBSERVED`. One table is provided per operation with one row for
each required field name. Common row values: `presence=NOT_OBSERVED`,
`jsonPointer=NONE`, `outerJsonPointer=NONE`, `innerJsonPointer=NONE`,
`exactValue=NOT_OBSERVED`, `valueJcsSha256=NOT_AVAILABLE`,
`classification=UNKNOWN`, `rationale=call not completed; no tool result
captured (fail-closed stop before transmission)`.

#### get-contact

| operationId | fieldName | presence | jsonPointer | outerJsonPointer | innerJsonPointer | exactValue | valueJcsSha256 | classification | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| get-contact | operationId | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | params | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | required | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | optional | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | requestBodyFields | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | requestSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | payloadExample | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | responses | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | response | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | responseSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | outputSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | successResponse | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | successSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | errorSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | statusCodes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | responseBody | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | responseType | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | resultSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | schemaRef | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | dto | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | scopes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | safety | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-contact | idempotency | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |

#### get-opportunity

| operationId | fieldName | presence | jsonPointer | outerJsonPointer | innerJsonPointer | exactValue | valueJcsSha256 | classification | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| get-opportunity | operationId | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | params | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | required | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | optional | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | requestBodyFields | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | requestSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | payloadExample | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | responses | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | response | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | responseSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | outputSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | successResponse | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | successSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | errorSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | statusCodes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | responseBody | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | responseType | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | resultSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | schemaRef | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | dto | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | scopes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | safety | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-opportunity | idempotency | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |

#### create-note

| operationId | fieldName | presence | jsonPointer | outerJsonPointer | innerJsonPointer | exactValue | valueJcsSha256 | classification | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| create-note | operationId | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | params | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | required | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | optional | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | requestBodyFields | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | requestSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | payloadExample | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | responses | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | response | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | responseSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | outputSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | successResponse | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | successSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | errorSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | statusCodes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | responseBody | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | responseType | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | resultSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | schemaRef | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | dto | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | scopes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | safety | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| create-note | idempotency | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |

#### get-note

| operationId | fieldName | presence | jsonPointer | outerJsonPointer | innerJsonPointer | exactValue | valueJcsSha256 | classification | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| get-note | operationId | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | params | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | required | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | optional | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | requestBodyFields | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | requestSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | payloadExample | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | responses | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | response | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | responseSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | outputSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | successResponse | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | successSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | errorSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | statusCodes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | responseBody | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | responseType | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | resultSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | schemaRef | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | dto | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | scopes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | safety | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| get-note | idempotency | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |

#### update-opportunity

| operationId | fieldName | presence | jsonPointer | outerJsonPointer | innerJsonPointer | exactValue | valueJcsSha256 | classification | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| update-opportunity | operationId | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | params | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | required | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | optional | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | requestBodyFields | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | requestSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | payloadExample | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | responses | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | response | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | responseSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | outputSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | successResponse | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | successSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | errorSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | statusCodes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | responseBody | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | responseType | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | resultSchema | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | schemaRef | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | dto | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | scopes | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | safety | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |
| update-opportunity | idempotency | NOT_OBSERVED | NONE | NONE | NONE | NOT_OBSERVED | NOT_AVAILABLE | UNKNOWN | call not completed; no tool result captured |

### 7.3 Additional provider-returned fields

No tool result was captured for any operation; there are no additional
provider-returned fields to inventory.

```text
ADDITIONAL_PROVIDER_FIELDS_CAPTURED=NONE
```

## 8. Pinned JCS canonicalization identity

```text
JCS_IMPLEMENTATION=local_minimal_rfc8785_subset_no_floats
JCS_IMPLEMENTATION_VERSION=jcs.py @ Python 3.9.6 (darwin), session-scoped capture harness
JCS_IMPLEMENTATION_REVISION=sha256:1656a237ede7ed62e7c002e1541f7d13cdc5096f08f4dd0a2ee7117cb5b03213
JCS_CONFORMANCE_VECTOR_PASS=YES
JCS_UNSUPPORTED_VALUE_POLICY=FAIL_CLOSED
MULTI_REPRESENTATION_EQUIVALENCE=PARSED_JSON_VALUES_MUST_HAVE_IDENTICAL_RFC8785_JCS_BYTES
```

The pinned implementation is a minimal RFC 8785 subset (integers, strings,
arrays, objects, booleans, null only; UTF-16BE code-unit member ordering;
mandatory-only string escapes; floats, non-finite constants, and duplicate
object members fail closed). Before the observation it passed 12 local
conformance vectors covering member ordering (including astral-plane UTF-16
surrogate ordering vs BMP), escape handling, whitespace elimination, empty
containers, large and negative integers, plus 5 float/non-finite rejections
and duplicate-member rejection (`JCS_CONFORMANCE_VECTOR_PASS=YES`). The
implementation revision above is the SHA-256 of the exact script file that
produced the conformance run and that would have produced every JCS digest
in this proof, so a reviewer can reproduce the digests byte-for-byte. No JCS
digest over a captured tool result exists in this proof because no tool
result was captured; the raw transport-body digest in section 5.2 hashes the
exact received bytes with no newline normalization and no credential or
session material.

## 9. Call counts and budget compliance

| Counter | Budget | Actual |
| --- | --- | --- |
| `MCP_INITIALIZE_CALLS` | <=1 | 1 |
| `MCP_INITIALIZED_NOTIFICATIONS` | <=1 | 0 |
| `MCP_DESCRIBE_OPERATION_CALLS` | <=5 | 0 |
| `MCP_EXECUTE_OPERATION_CALLS` | 0 | 0 |
| `MCP_TOOLS_LIST_CALLS` | 0 | 0 |
| `MCP_SEARCH_OPERATIONS_CALLS` | 0 | 0 |
| `MCP_SEARCH_FETCH_CALLS` | 0 | 0 |
| `GHL_BUSINESS_READS` | 0 | 0 |
| `GHL_MUTATIONS` | 0 | 0 |
| `RAW_REST_CALLS` | 0 | 0 |
| `GRANT009_EXECUTIONS` | 0 | 0 |
| `MCP_SESSION_RESTARTS` | 0 | 0 |

| Prohibition | Compliance |
| --- | --- |
| retry / replacement call | none attempted |
| second session / reconnect re-initialize | none attempted |
| substituted operation ID | none |
| `tools/list`, `search`, `fetch`, `search_operations`, `list_locations` | not issued |
| business-operation invocation (`get-contact` etc. via `execute_operation`) | not issued |
| GHL business read/write, private-record access | none |
| raw REST / schema-reference retrieval | none |
| session-identifier synthesis or durable capture | none (no identifier issued; none forwarded; none recorded) |
| credential/private identifier in proof | none (`Authorization` value and cookie redacted; token held in memory only) |
| parser/adapter/session/transport/workflow/runtime implementation | not performed (throwaway capture harness only; no repo code changed) |
| Grant009 drafting/preparation/activation/execution | none |
| IAM/secret/deployment/infrastructure changes | none (read-only Secret Manager access of the existing `GHL_MCP_PRIVATE_TOKEN` version for transport auth only) |

## 10. Required result block

```text
AUTHORIZATION_ID=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001
PR81_AUTHORIZATION_MERGE_SHA=44f3daadf4e3d2dfd10d0fe3c180a7f425f39029
PR82_REFINEMENT_REVIEWED_HEAD=61cb37e9d48c95e0e34aa7db489225236a3b355c
PR82_REFINEMENT_MERGE_SHA=f40ffa65cfa36fdf9a9d8486888f600f23465ae1

OBSERVATION_EXECUTION_OCCURRED=YES
OBSERVATION_AUTHORITY_CONSUMED=YES

DESCRIBE_OPERATION_CALLS=0
DESCRIBE_OPERATION_EXACT_RESPONSE_CAPTURED=NO
DESCRIBE_OPERATION_INPUT_SCHEMA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_RESPONSE_SCHEMA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_SUCCESS_METADATA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_ERROR_METADATA_DEFINED=NOT_OBSERVED
DESCRIBE_OPERATION_PAYLOAD_EXAMPLE_ONLY=NOT_OBSERVED

DESCRIBE_OPERATION_RESULT_REPRESENTATION=NOT_OBSERVED
DESCRIBE_OPERATION_METADATA_PARSE_MODE=NOT_OBSERVED

OPERATION_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=NOT_OBSERVED
OPERATION_RESPONSE_SCHEMA_BINDABLE_TO_FROZEN_OPENAPI=NOT_OBSERVED
BUSINESS_PAYLOAD_SCHEMA_SOURCE=NOT_OBSERVED

EXECUTE_OPERATION_RESULT_BINDING_STILL_UNKNOWN=NOT_OBSERVED
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
NEXT=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_HUMAN_REVIEW

NEGOTIATED_PROTOCOL_VERSION=NOT_NEGOTIATED
PROTOCOL_VERSION_MATCH=NOT_NEGOTIATED
EXACT_OPERATION_IDS_QUERIED=NONE
MCP_INITIALIZE_CALLS=1
MCP_INITIALIZED_NOTIFICATIONS=0
INITIALIZED_NOTIFICATION_HTTP_STATUS=NOT_SENT
INITIALIZED_NOTIFICATION_RESPONSE_BODY_SHA256=NOT_SENT
MCP_DESCRIBE_OPERATION_CALLS=0
MCP_EXECUTE_OPERATION_CALLS=0
MCP_TOOLS_LIST_CALLS=0
MCP_SEARCH_OPERATIONS_CALLS=0
MCP_SEARCH_FETCH_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
RAW_REST_CALLS=0
GRANT009_EXECUTIONS=0
MCP_SESSION_IDENTIFIER_FORWARDING=NOT_APPLICABLE
MCP_SESSION_IDENTIFIER_ISSUED=NOT_OBSERVED
MCP_SESSION_IDENTIFIER_FORWARDED=NO
MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_RESTARTS=0
FAIL_CLOSED=YES
STOP_REASON=INITIALIZE_EDGE_BLOCKED_HTTP_403_CLOUDFLARE_ERROR_1010_NO_RETRY_OR_REPLACEMENT_AUTHORIZED
```

`MCP_SESSION_IDENTIFIER_FORWARDING=NOT_APPLICABLE`: the same-session
forwarding rule never engaged because no successful `initialize` response
existed to issue an identifier. `MCP_SESSION_IDENTIFIER_ISSUED=NOT_OBSERVED`:
the only response received was an edge error document carrying no
`Mcp-Session-Id` header; no MCP initialize response was observable.
`EXECUTE_OPERATION_RESULT_BINDING_STILL_UNKNOWN=NOT_OBSERVED` because the
observation never reached any provider metadata; the pre-existing unknown
state is unchanged rather than re-established by evidence.

## 11. Digest register

```text
INITIALIZE_REQUEST_JSON_SHA256=12bcd905da9c686cd3b3d642a9349ecf96350e18a614a2847a834016b3f6951f
INITIALIZE_RESPONSE_RAW_SHA256=a1b5d6aaacbb4ca7eaa1c3d2675b019b858f3a08fbe4c013ae27e487f4410450
INITIALIZE_RESPONSE_JSON_JCS_SHA256=NOT_AVAILABLE
INITIALIZED_NOTIFICATION_REQUEST_JSON_SHA256=59951ca0b212b103876fa23a9e58bcbbc8fbcc0120e3f5ee7214461e2bd1cd5e (NOT_TRANSMITTED)
DESCRIBE_REQUEST_GET_CONTACT_JSON_SHA256=09b35192af7746a172e06c388d609036942ee1a98b9816a3a3f4e478d361db9c (NOT_TRANSMITTED)
DESCRIBE_REQUEST_GET_OPPORTUNITY_JSON_SHA256=c5516f5e8d8dcdf0cda0e668842718124fbc4afe28b99300d0adb0fedf81ce51 (NOT_TRANSMITTED)
DESCRIBE_REQUEST_CREATE_NOTE_JSON_SHA256=dd056c3a36f3aed64936138c0d34de5841b9edf0df7af82a9ba63fe9535c1655 (NOT_TRANSMITTED)
DESCRIBE_REQUEST_GET_NOTE_JSON_SHA256=fae7afb695516bb7df7f8f6ceacfef617914e8ac1158db370a0e94edf3df469a (NOT_TRANSMITTED)
DESCRIBE_REQUEST_UPDATE_OPPORTUNITY_JSON_SHA256=e5a72f51b3746206d7e171dc9b95b168b11395d639ad821db9d4738082f80a95 (NOT_TRANSMITTED)
JCS_IMPLEMENTATION=local_minimal_rfc8785_subset_no_floats
JCS_IMPLEMENTATION_REVISION=sha256:1656a237ede7ed62e7c002e1541f7d13cdc5096f08f4dd0a2ee7117cb5b03213
```

The byte-exact initialize request and response bodies in section 5 are the
digest subjects; a reviewer can reproduce both digests from this artifact
alone without any secret or live session.

## 12. STOP

```text
STOP_REASON=INITIALIZE_EDGE_BLOCKED_HTTP_403_CLOUDFLARE_ERROR_1010_NO_RETRY_OR_REPLACEMENT_AUTHORIZED
FAIL_CLOSED=YES
OBSERVATION_EXECUTION_OCCURRED=YES
OBSERVATION_AUTHORITY_CONSUMED=YES
MCP_INITIALIZE_CALLS=1
MCP_INITIALIZED_NOTIFICATIONS=0
MCP_DESCRIBE_OPERATION_CALLS=0
MCP_EXECUTE_OPERATION_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
RAW_REST_CALLS=0
GRANT009_EXECUTIONS=0
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
NEXT=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_HUMAN_REVIEW
```

The one-shot observation authority is consumed. The edge block
(`browser_signature_banned`, `retryable:false`, `owner_action_required:true`)
is a provider-edge access condition outside this unit's authority to
remediate. Any further observation attempt requires a new human-reviewed
authorization; none is drafted here.
