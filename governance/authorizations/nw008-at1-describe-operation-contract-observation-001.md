# NW-008 AT-1 Describe Operation Contract Observation Authorization

## 1. Authorization identity and activation boundary

```text
CLASSIFICATION=authorization_proposal
PLANNING_ID=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001
OWNER=VS Code / MG Orchestrator
BASE_REF=origin/main
BASE_SHA=44f3daadf4e3d2dfd10d0fe3c180a7f425f39029
AUTHORIZATION_BRANCH=auth/nw008-at1-describe-operation-contract-observation-001

PRIOR_MERGED_AUTHORIZATION_PR=81
PRIOR_MERGED_AUTHORIZATION_HEAD=6c4256e6872fcf0f3cef0b52618cd6d1e9c959bc
PRIOR_MERGED_AUTHORIZATION_MERGE_SHA=44f3daadf4e3d2dfd10d0fe3c180a7f425f39029
REFINEMENT=PR81_EVIDENCE_RULES_RESULT_REPRESENTATION_SESSION_JCS_LIFECYCLE

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=HUMAN_REVIEW_AND_MERGE_TO_MAIN
SELF_ACTIVATION=FORBIDDEN
OBSERVATION_EXECUTION_OCCURRED=NO
```

This unit proposes a narrowly bounded, read-only observation of the provider's
`describe_operation` metadata for the five distinct AT-1 business operations
whose REST payload schemas are already frozen. It answers only:

```text
WHAT_EXACTLY_DOES_DESCRIBE_OPERATION_RETURN=
```

This revision refines the PR #81 evidence rules before any observation may run.
It adds explicit MCP result-representation classification, serialized-text JSON
parse rules, same-session transport limits, pinned JCS canonicalization
identity, and initialized-notification lifecycle accounting. Prior merge of
PR #81 does not authorize execution under the unrefined rules once this
refinement is opened; the refined artifact becomes effective only after human
review and merge of this exact head to `main`.

The authorization becomes effective only after human review and merge to
`main`. Creating, reviewing, or merging this artifact does not perform the
observation. Execution must occur in a separate proof-producing unit against
the merged authorization and must stop immediately after evidence capture.

This unit does not authorize `execute_operation`, any GHL business read or
write, raw REST, implementation work, Grant009, or infrastructure changes.

## 2. Verified prerequisites and durable evidence

Preflight was run before this refinement was authored:

```text
pwd
/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git branch --show-current
auth/nw008-at1-describe-operation-contract-observation-001

git status --short --untracked-files=all
<empty>
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #80 state | MERGED |
| PR #80 reviewed head | `f183ac14140840d5325b17c9cc6bc88378fa47aa` |
| PR #80 merge commit | `8d70390b9b962c0276a99ea0d8b63c384c1a426c` |
| PR #80 merged at | `2026-08-18T10:51:44Z` |
| PR #80 reviewed head is reachable from `origin/main` | YES |
| PR #81 state | MERGED |
| PR #81 reviewed head | `6c4256e6872fcf0f3cef0b52618cd6d1e9c959bc` |
| PR #81 merge commit | `44f3daadf4e3d2dfd10d0fe3c180a7f425f39029` |
| PR #81 merged at | `2026-08-18T11:05:15Z` |
| PR #81 reviewed head is reachable from `origin/main` | YES |
| Authorization base equals `origin/main` after PR #81 | YES |
| Observation execution under PR #81 occurred | NO |

The following merged artifacts are the only durable evidence inputs to this
authorization:

```text
PR76_SOURCE_CAPTURE=proof/nw008/nw-008-at1-mcp-response-source-capture.md
PR76_SOURCE_CAPTURE_BLOB_SHA=5c1cbb7698b24e65c92749dd7963c460aa092b1a
PR76_SOURCE_CAPTURE_SHA256=896e5a512a94d0aff6d026415c1b4f7aae7843e54a7e741ac3a26ce2ec1ff40b

PR78_PREGRANT_OBSERVATION=proof/nw008/nw-008-at1-pregrant-mcp-contract-observation-001.md
PR78_PREGRANT_OBSERVATION_BLOB_SHA=af74ebf9332e21f57a6c9b0bd9b58ac9973c2ec8
PR78_PREGRANT_OBSERVATION_SHA256=f34d722c13596a8c1e1cfd72ada631e04342573425430982c8d74d55a8b812e2

PR79_CONTRACT_GAP=proof/nw008/nw-008-at1-provider-response-contract-gap-001.md
PR79_CONTRACT_GAP_BLOB_SHA=fb295477d882bff07491431fc71aa9a131242705
PR79_CONTRACT_GAP_SHA256=7660280f71a329263147f3be0959eb065b164ea6fbe845042c61e9f99957a777

PR80_PROVIDER_AUTHORITY_ACQUISITION=proof/nw008/nw-008-at1-provider-output-authority-acquisition-001.md
PR80_PROVIDER_AUTHORITY_ACQUISITION_BLOB_SHA=becfdc8eb125b5c8f9f00d9d0dd9a4c5d5fce833
PR80_PROVIDER_AUTHORITY_ACQUISITION_SHA256=1e8bb788f6516ca2e1407a4232efcb8f081cdb67b77b0e45a1e08b7b335bdcd7
```

## 3. Inherited state and observation question

These facts are inherited from the bound evidence and are not reinterpreted by
this proposal:

```text
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25

HIGHLEVEL_DOC_DESCRIBE_OPERATION_INPUT_AUTHORITY=YES
HIGHLEVEL_DOC_DESCRIBE_OPERATION_REQUIRED_OPTIONAL_INPUTS=YES

DESCRIBE_OPERATION_RETURNS_JSON_SCHEMA=UNKNOWN
DESCRIBE_OPERATION_RESPONSE_SCHEMA_PRESENT=UNKNOWN
DESCRIBE_OPERATION_SUCCESS_BODY_METADATA_PRESENT=UNKNOWN

EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
```

PR #78 captured the provider-advertised description of `describe_operation`:
it returns compact public params, request-body fields, one sanitized payload
example, scopes, safety metadata, and idempotency constraints. PR #80 confirmed
that this is request-side evidence only on the evidence currently bound; the
tool has not yet been invoked to determine whether its exact returned metadata
also contains response-side authority.

The observation may establish only what the provider actually returns for the
five exact operation IDs below. Absence is evidence of absence in this bounded
capture, not permission to infer a contract.

## 4. Exact authorized operation set and call budget

The five distinct frozen AT-1 operation IDs are:

| Call ordinal | JSON-RPC id | Exact operation ID |
| --- | --- | --- |
| 1 | `2` | `get-contact` |
| 2 | `3` | `get-opportunity` |
| 3 | `4` | `create-note` |
| 4 | `5` | `get-note` |
| 5 | `6` | `update-opportunity` |

The duplicated AT-1 planning ordinal for `get-opportunity` reuses the same
operation and schema. A second call for that duplicate is not authorized.

```text
AT1_DISTINCT_OPERATION_COUNT=5
MCP_INITIALIZE_CALLS_MAX=1
MCP_DESCRIBE_OPERATION_CALLS_MAX=5
MCP_EXECUTE_OPERATION_CALLS_MAX=0
MCP_TOOLS_LIST_CALLS_MAX=0
MCP_SEARCH_OPERATIONS_CALLS_MAX=0
MCP_SEARCH_FETCH_CALLS_MAX=0
GHL_BUSINESS_READS_MAX=0
GHL_MUTATIONS_MAX=0
RAW_REST_CALLS_MAX=0

MCP_INITIALIZED_NOTIFICATIONS=1
MCP_SESSION_RESTARTS_MAX=0
MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_IDENTIFIER_FORWARDING=AUTHORIZED_ONLY_IF_ISSUED_BY_SUCCESSFUL_INITIALIZE
```

Exactly one protocol-required `notifications/initialized` message is permitted
after a successful version match. The proof must account for that single
lifecycle notification with HTTP status and response-body SHA-256 even when the
body is empty. No `tools/list`, discovery call, retry, polling, pagination,
session restart, or substituted operation ID is authorized.

Same-session transport rule:

```text
MCP_SESSION_IDENTIFIER_FORWARDING=
  AUTHORIZED_ONLY_IF_ISSUED_BY_SUCCESSFUL_INITIALIZE

MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_RESTARTS_MAX=0
```

A session identifier may be forwarded on subsequent requests in the same
observation only when the successful `initialize` response issued it. The
identifier must not be written into durable proof artifacts. If no session
identifier is issued, none may be synthesized. A second session, reconnect that
re-initializes, or session restart is not authorized (`MCP_SESSION_RESTARTS_MAX=0`).

## 5. Exact request plan

The observation must send the following compact JSON request bodies exactly,
with no whitespace or member-order changes. Transport-only authentication and
required protocol headers must not be included in proof except as sanitized
header names and non-secret protocol values.

Initialize request:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"mg-guide-nw008-at1-describe-operation-observation","version":"0.0.1"}}}
```

Initialized notification:

```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

The five and only five `describe_operation` requests:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"describe_operation","arguments":{"operationId":"get-contact"}}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"describe_operation","arguments":{"operationId":"get-opportunity"}}}
{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"describe_operation","arguments":{"operationId":"create-note"}}}
{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"describe_operation","arguments":{"operationId":"get-note"}}}
{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"describe_operation","arguments":{"operationId":"update-opportunity"}}}
```

The proof must compute a SHA-256 digest over the exact bytes of each request
body before transmission. It must capture each complete response body exactly
as received, including SSE framing when present, and separately retain the
exact parsed JSON-RPC payload.

## 6. Required observation procedure and fail-closed gates

The later proof-producing unit must:

1. Record a UTC start timestamp and the merged authorization commit.
2. Initialize once with offered protocol version exactly `2025-11-25`.
3. Capture the byte-exact initialize request and response, request/response id,
   transport class, sanitized response headers, server metadata, capabilities,
   and exact negotiated protocol version.
4. If the negotiated version is not exactly `2025-11-25`, stop before sending
   `notifications/initialized` or any `tools/call`.
5. Send the protocol-required initialized notification after a version match.
   Capture `INITIALIZED_NOTIFICATION_HTTP_STATUS` and
   `INITIALIZED_NOTIFICATION_RESPONSE_BODY_SHA256` over the exact response body
   bytes (use the SHA-256 of empty bytes when the body is empty). Count must be
   exactly `MCP_INITIALIZED_NOTIFICATIONS=1`.
6. Invoke `describe_operation` once for each operation in section 4, in the
   stated order, using the exact request bodies in section 5. Forward a session
   identifier only under the section 4 same-session transport rule.
7. For every call, capture start and completion timestamps, HTTP status,
   request/response id binding, byte-exact request and response bodies, parsed
   JSON-RPC payload, canonical digests, and the section 7 result-representation
   classification for the exact `CallToolResult`.
8. Inspect only returned `describe_operation` metadata. Do not follow links,
   resolve schema references through network calls, execute examples, or issue
   any business operation.
9. Complete the field-presence, result-representation, and classification
   matrices in section 7 under the parse and fail-closed rules there.
10. Record all call counts, pin the JCS implementation identity required by
    section 8, derive only the result fields in section 8 under the decision
    rules in section 9, stop, and return proof.

The unit must stop without retry or authority expansion on a protocol mismatch,
malformed response, JSON-RPC error, tool-level `isError`, request/response id
mismatch, incomplete byte capture, digest failure, conflicting simultaneous
result representations, unexpected operation identity, secret/private-identifier
exposure risk, unauthorized session-identifier use, or any condition requiring a
sixth `describe_operation` call or second session.

Partial completed calls remain evidence. Unattempted calls must be marked
`NOT_OBSERVED`; no replacement call is authorized.

## 7. Field capture and classification requirements

### 7.1 MCP result representation classification

For each of the five `describe_operation` calls, the proof must classify the
exact tool result representation before any semantic field inventory. Allowed
values are exactly:

```text
DESCRIBE_OPERATION_RESULT_REPRESENTATION=
  STRUCTURED_CONTENT |
  CONTENT_TEXT_JSON |
  CONTENT_TEXT_NON_JSON |
  MULTI_REPRESENTATION |
  NOT_OBSERVED
```

Classification rules for the exact outer MCP `CallToolResult` (after JSON-RPC
envelope parse; before semantic authority decisions):

| Observed wire condition | Required value |
| --- | --- |
| Only `structuredContent` carries the tool result object; no `content[*].text` JSON object/array payload is also present | `STRUCTURED_CONTENT` |
| No usable `structuredContent` object; one or more `content[*].text` members parse as a JSON object or array | `CONTENT_TEXT_JSON` |
| Result is only non-JSON text in `content[*].text` (and/or non-text content parts) with no structured object | `CONTENT_TEXT_NON_JSON` |
| More than one of structured object and JSON text (or multiple conflicting JSON texts) are simultaneously present | `MULTI_REPRESENTATION` |
| Call was not completed with a capturable tool result | `NOT_OBSERVED` |

The proof must also record:

```text
DESCRIBE_OPERATION_METADATA_PARSE_MODE=
  DIRECT_JSON |
  SERIALIZED_JSON_TEXT |
  NONE
```

| Condition | Required value |
| --- | --- |
| Metadata inventory is taken directly from a JSON object already present as `structuredContent` (or equivalent direct JSON member) without parsing a string body | `DIRECT_JSON` |
| Metadata inventory requires parsing JSON from a `content[*].text` string | `SERIALIZED_JSON_TEXT` |
| No JSON metadata object is available to inventory | `NONE` |

### 7.2 Serialized `content[*].text` JSON handling

When any `content[*].text` value contains JSON (object or array):

1. Preserve the exact outer `CallToolResult` JSON as received inside the
   JSON-RPC result; do not rewrite, reorder, or omit members for storage.
2. Preserve the exact `content[*].text` string bytes/characters as returned.
3. Record `CONTENT_TEXT_SHA256` over the exact text string (UTF-8 bytes of the
   exact returned text, with no trimming or newline normalization).
4. Parse that text only to build the metadata field inventory and pointers.
   Parseability alone confers no schema authority and no semantic
   classification beyond enabling inventory.
5. Record `OUTER_JSON_POINTER` to the exact `content[*].text` member inside the
   outer `CallToolResult` (for example `/content/0/text`).
6. Record `INNER_JSON_POINTER` values relative to the parsed inner JSON value
   for every inventoried field occurrence (or `NONE` when a field is absent
   from that inner value).
7. Compute `INNER_VALUE_JCS_SHA256` as the RFC 8785 JCS SHA-256 over the parsed
   inner JSON value when parse succeeds; otherwise `NOT_AVAILABLE`.
8. Do not infer response-schema authority, success/error contracts, or freeze
   readiness from the fact that text was parseable as JSON.
9. If simultaneous representations conflict—including disagreeing structured
   and text JSON payloads, disagreeing JSON texts, or a
   `MULTI_REPRESENTATION` result whose payloads are not byte-for-byte
   equivalent under the same inventory—fail closed: keep authority results
   non-positive, set `FAIL_CLOSED=YES`, and do not prefer one representation
   by inference.

When the representation is `STRUCTURED_CONTENT` with
`DESCRIBE_OPERATION_METADATA_PARSE_MODE=DIRECT_JSON`, inventory pointers are
taken directly against the structured object; `CONTENT_TEXT_SHA256` is
`NOT_AVAILABLE` unless a text member also exists and is preserved under the
rules above.

### 7.3 Required metadata field inventory

For each of the five operations, the proof must include one row for every field
name below, whether present or absent:

```text
operationId
params
required
optional
requestBodyFields
requestSchema
payloadExample
responses
response
responseSchema
outputSchema
successResponse
successSchema
errorSchema
statusCodes
responseBody
responseType
resultSchema
schemaRef
dto
scopes
safety
idempotency
```

Each per-operation row must contain:

| Required column | Required value |
| --- | --- |
| `operationId` | Exact queried operation ID |
| `fieldName` | One field name from the required list |
| `presence` | `PRESENT`, `ABSENT`, or `NOT_OBSERVED` |
| `jsonPointer` | Every exact JSON Pointer where the field occurs, or `NONE` |
| `outerJsonPointer` | Pointer into the outer `CallToolResult` when the inventory source is nested (for example through `/content/0/text`), otherwise the direct structured pointer or `NONE` |
| `innerJsonPointer` | Pointer relative to the parsed inner JSON value when `SERIALIZED_JSON_TEXT`, otherwise `NONE` |
| `exactValue` | Exact returned JSON value, or `ABSENT` / `NOT_OBSERVED` |
| `valueJcsSha256` | RFC 8785 canonical SHA-256 for a present JSON value, otherwise `NOT_AVAILABLE` |
| `classification` | One allowed classification below |
| `rationale` | Returned semantics supporting the classification, without inference |

Every present occurrence must be captured. A same-named nested field may not be
collapsed into a top-level occurrence. Additional provider-returned fields not
listed above must be added to a separate table with the same columns and
classified; they may not be ignored.

Each per-operation summary must also include:

```text
DESCRIBE_OPERATION_RESULT_REPRESENTATION=<allowed value>
DESCRIBE_OPERATION_METADATA_PARSE_MODE=<allowed value>
CONTENT_TEXT_SHA256=<sha256 or NOT_AVAILABLE>
OUTER_JSON_POINTER=<pointer or NONE>
INNER_VALUE_JCS_SHA256=<sha256 or NOT_AVAILABLE>
CALLTOOLRESULT_JCS_SHA256=<sha256 or NOT_AVAILABLE>
```

Allowed classifications are exactly:

```text
INPUT_SCHEMA_AUTHORITY
OUTPUT_SCHEMA_AUTHORITY
EXAMPLE_ONLY
SAFETY_METADATA
SCOPE_METADATA
UNKNOWN
```

Classification rules:

| Returned value semantics | Classification |
| --- | --- |
| Machine-readable parameter, required/optional, request-body, or request-schema definition | `INPUT_SCHEMA_AUTHORITY` |
| Machine-readable response/result/success/error body schema, explicit response schema reference, response DTO binding, or status-to-body contract | `OUTPUT_SCHEMA_AUTHORITY` |
| Example, sample, illustration, or payload example, even when structurally detailed | `EXAMPLE_ONLY` |
| Safety, destructive/read-only behavior, or idempotency constraint | `SAFETY_METADATA` |
| Required/available OAuth or provider scope metadata | `SCOPE_METADATA` |
| Identity, prose, ambiguous response metadata, an absent value, or any value whose semantics are not explicit in the returned metadata | `UNKNOWN` |

Field names alone do not determine classification. In particular, `response`,
`responseBody`, `schemaRef`, `dto`, or similar names are
`OUTPUT_SCHEMA_AUTHORITY` only when the returned metadata explicitly designates
their value as a machine-readable operation output contract. `payloadExample`
is always `EXAMPLE_ONLY`. `operationId` is `UNKNOWN`. `idempotency` is
`SAFETY_METADATA`. No example, prose description, current parser behavior, or
sample execution result may be promoted to schema authority.

The proof must also provide a per-operation summary containing:

```text
DESCRIBE_OPERATION_INPUT_SCHEMA_DEFINED=<YES|NO|NOT_OBSERVED>
DESCRIBE_OPERATION_RESPONSE_SCHEMA_DEFINED=<YES|NO|NOT_OBSERVED>
DESCRIBE_OPERATION_SUCCESS_METADATA_DEFINED=<YES|NO|NOT_OBSERVED>
DESCRIBE_OPERATION_ERROR_METADATA_DEFINED=<YES|NO|NOT_OBSERVED>
DESCRIBE_OPERATION_PAYLOAD_EXAMPLE_ONLY=<YES|NO|NOT_PRESENT|NOT_OBSERVED>
```

## 8. Required proof return

The proof must include the authorization ID and merge commit, exact negotiated
protocol version, exact operation IDs queried in call order, all byte-exact
request/response bodies, all timestamps, canonical digest subjects and SHA-256
digests, the complete classification tables, and the following result block:

```text
DESCRIBE_OPERATION_CALLS=<0..5>
DESCRIBE_OPERATION_EXACT_RESPONSE_CAPTURED=<YES|NO|PARTIAL>
DESCRIBE_OPERATION_INPUT_SCHEMA_DEFINED=<YES|NO|MIXED|NOT_OBSERVED>
DESCRIBE_OPERATION_RESPONSE_SCHEMA_DEFINED=<YES|NO|MIXED|NOT_OBSERVED>
DESCRIBE_OPERATION_SUCCESS_METADATA_DEFINED=<YES|NO|MIXED|NOT_OBSERVED>
DESCRIBE_OPERATION_ERROR_METADATA_DEFINED=<YES|NO|MIXED|NOT_OBSERVED>
DESCRIBE_OPERATION_PAYLOAD_EXAMPLE_ONLY=<YES|NO|MIXED|NOT_PRESENT|NOT_OBSERVED>

DESCRIBE_OPERATION_RESULT_REPRESENTATION=<STRUCTURED_CONTENT|CONTENT_TEXT_JSON|CONTENT_TEXT_NON_JSON|MULTI_REPRESENTATION|MIXED|NOT_OBSERVED>
DESCRIBE_OPERATION_METADATA_PARSE_MODE=<DIRECT_JSON|SERIALIZED_JSON_TEXT|NONE|MIXED|NOT_OBSERVED>

OPERATION_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=<YES|NO|PARTIAL|NOT_OBSERVED>
OPERATION_RESPONSE_SCHEMA_BINDABLE_TO_FROZEN_OPENAPI=<YES|NO|PARTIAL|NOT_OBSERVED>
BUSINESS_PAYLOAD_SCHEMA_SOURCE=<DESCRIBE_OPERATION|FROZEN_PROVIDER_OPENAPI_UNBOUND|COMPOSITE_DESCRIBE_AND_FROZEN_OPENAPI|NONE|NOT_OBSERVED>

EXECUTE_OPERATION_RESULT_BINDING_STILL_UNKNOWN=<YES|NO|PARTIAL|NOT_OBSERVED>
PROVIDER_OUTPUT_BINDING_FROZEN=<YES|NO>
COMPOSITE_CONTRACT_FREEZE_READY=<YES|NO>
NEXT=<terminal next step>
```

It must additionally report:

```text
NEGOTIATED_PROTOCOL_VERSION=<exact value or NOT_NEGOTIATED>
PROTOCOL_VERSION_MATCH=<YES|NO|NOT_NEGOTIATED>
EXACT_OPERATION_IDS_QUERIED=<ordered comma-separated IDs or NONE>
MCP_INITIALIZE_CALLS=<0|1>
MCP_INITIALIZED_NOTIFICATIONS=1
INITIALIZED_NOTIFICATION_HTTP_STATUS=<exact status or NOT_SENT>
INITIALIZED_NOTIFICATION_RESPONSE_BODY_SHA256=<sha256 or NOT_SENT>
MCP_DESCRIBE_OPERATION_CALLS=<0..5>
MCP_EXECUTE_OPERATION_CALLS=0
MCP_TOOLS_LIST_CALLS=0
MCP_SEARCH_OPERATIONS_CALLS=0
MCP_SEARCH_FETCH_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
RAW_REST_CALLS=0
GRANT009_EXECUTIONS=0
MCP_SESSION_IDENTIFIER_FORWARDING=<AUTHORIZED_ONLY_IF_ISSUED_BY_SUCCESSFUL_INITIALIZE|NOT_APPLICABLE>
MCP_SESSION_IDENTIFIER_ISSUED=<YES|NO|NOT_OBSERVED>
MCP_SESSION_IDENTIFIER_FORWARDED=<YES|NO>
MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_RESTARTS=0
FAIL_CLOSED=<YES|NO>
STOP_REASON=<terminal reason>
```

### 8.1 Pinned JCS canonicalization identity

For every exact JSON value, canonicalization must use RFC 8785 JCS. The proof
must pin the exact implementation identity used for every JCS digest in the
result:

```text
JCS_IMPLEMENTATION=<implementation identity>
JCS_IMPLEMENTATION_VERSION=<version identity>
JCS_IMPLEMENTATION_REVISION=<revision identity>
JCS_CONFORMANCE_VECTOR_PASS=YES
```

Allowed implementation for this observation (must match prior NW-008 AT-1
pre-grant proof practice unless a later merged authorization supersedes it):

```text
JCS_IMPLEMENTATION=local_minimal_rfc8785_subset_no_floats
```

`JCS_IMPLEMENTATION_VERSION` and `JCS_IMPLEMENTATION_REVISION` must identify the
exact code or script revision that produced the digests so a reviewer can
reproduce them. `JCS_CONFORMANCE_VECTOR_PASS` must be `YES`; if conformance
vectors do not pass, the unit must fail closed before emitting authority
conclusions.

Raw transport-body digests must hash the exact received bytes without newline
normalization. The proof must publish each digest subject or enough byte-exact
content for independent reproduction. Credentials, cookies, authorization
values, private tenant/location identifiers, private record identifiers, and
session identifiers must be omitted or replaced with an explicit redaction
marker before the proof artifact is written; no digest may require a reviewer
to possess a secret or a live session identifier.

## 9. Authority and freeze decision rules

`OPERATION_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=YES` requires explicit,
machine-readable output schema authority for all five operations. Use `PARTIAL`
when it exists for only a subset and `NO` when none is returned.

`OPERATION_RESPONSE_SCHEMA_BINDABLE_TO_FROZEN_OPENAPI=YES` requires the returned
metadata for all five operations to explicitly identify a response schema or
schema reference that can be matched without inference to the exact frozen
provider OpenAPI operation/success-schema bindings in PR #76. A matching DTO
name or `$ref` is sufficient only when the returned metadata explicitly
designates it as the operation response contract. Similar structure, examples,
or prose are insufficient.

`BUSINESS_PAYLOAD_SCHEMA_SOURCE` must be selected as follows:

| Observed condition | Required value |
| --- | --- |
| Complete response schemas are returned directly and do not rely on the frozen OpenAPI schemas | `DESCRIBE_OPERATION` |
| Returned metadata explicitly binds all five operations to the frozen OpenAPI response schemas | `COMPOSITE_DESCRIBE_AND_FROZEN_OPENAPI` |
| No bindable response authority is returned; existing frozen OpenAPI payload schemas remain unbound to MCP results | `FROZEN_PROVIDER_OPENAPI_UNBOUND` |
| No response authority exists in either source | `NONE` |
| Observation did not reach the response metadata | `NOT_OBSERVED` |

Even complete per-operation response schema metadata does not by itself define
where `execute_operation` places the business payload inside MCP
`CallToolResult`. Therefore:

- `EXECUTE_OPERATION_RESULT_BINDING_STILL_UNKNOWN=NO` only if returned
  provider metadata explicitly defines the `execute_operation` result wrapper
  or payload wire path in addition to the operation response schemas.
- `PROVIDER_OUTPUT_BINDING_FROZEN=YES` only if that explicit result binding is
  complete for all five operations and is consistent with the already-frozen
  MCP and operation schema layers.
- `COMPOSITE_CONTRACT_FREEZE_READY=YES` only if the provider output binding is
  frozen and every prerequisite frozen layer remains satisfied.

Any missing, ambiguous, example-only, partial, or conflicting result keeps
`PROVIDER_OUTPUT_BINDING_FROZEN=NO` and
`COMPOSITE_CONTRACT_FREEZE_READY=NO`. This observation cannot authorize an
implementation change; any positive freeze conclusion requires a separate
human-reviewed planning/authorization unit.

Allowed terminal `NEXT` values are:

```text
NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_HUMAN_REVIEW
NW008_AT1_PROVIDER_OUTPUT_BINDING_PLANNING
NW008_AT1_PROVIDER_OUTPUT_AUTHORITY_GAP_REMAINS
```

The proof must choose the first value when incomplete or fail-closed evidence
needs disposition, the second only when complete provider-returned authority is
identified, and the third when the complete five-operation observation returns
no sufficient output binding authority.

## 10. Hard prohibitions

This authorization does not permit:

- any `execute_operation` call;
- `search`, `fetch`, `search_operations`, `list_locations`, or `tools/list`;
- invocation of `get-contact`, `get-opportunity`, `create-note`, `get-note`,
  `update-opportunity`, or any other business operation;
- any GHL business read, write, mutation, or private-record access;
- raw REST or schema-reference retrieval over the network;
- treating an execution response, example, fixture, parser behavior, or prose
  as schema authority;
- inference beyond exact returned `describe_operation` metadata;
- parser, adapter, session, transport, workflow, or runtime implementation;
- Grant009 drafting, preparation, activation, or execution;
- IAM, credential, secret, deployment, or infrastructure changes;
- credential, private identifier, or session-identifier capture in durable
  evidence;
- synthesizing or forwarding a session identifier not issued by the successful
  `initialize` response;
- retries, additional sessions, substituted operation IDs, or budget expansion;
- preferring one of multiple conflicting result representations by inference;
- treating JSON parseability of `content[*].text` as schema authority.

```text
MCP_EXECUTE_OPERATION_AUTHORIZED=NO
GHL_BUSINESS_READ_AUTHORIZED=NO
GHL_MUTATION_AUTHORIZED=NO
RAW_REST_AUTHORIZED=NO
SAMPLE_EXECUTION_RESPONSE_AS_SCHEMA_AUTHORITY=NO
PARSER_SESSION_RUNTIME_IMPLEMENTATION_AUTHORIZED=NO
MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_RESTARTS_MAX=0
GRANT009_AUTHORIZED=NO
IAM_SECRET_DEPLOY_CHANGES_AUTHORIZED=NO
```

## 11. Authorization PR validation and stop

This authorization proposal has exactly one writable path:

```text
governance/authorizations/nw008-at1-describe-operation-contract-observation-001.md
```

Required before merge:

1. `git diff --check`;
2. exactly one changed path, equal to the path above;
3. `PYTHONPATH=src python scripts/verify_phase1_deterministic.py`;
4. exact-head `Phase 1 deterministic validation` success;
5. clean mergeability into `main`; and
6. human review and human merge authority.

The observation must not execute from an open or unmerged authorization PR.
Any push changes the exact head and requires exact-head validation and human
review again.

```text
PLANNING_ID=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001
STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=HUMAN_REVIEW_AND_MERGE_TO_MAIN
REFINEMENT=PR81_EVIDENCE_RULES_RESULT_REPRESENTATION_SESSION_JCS_LIFECYCLE

MCP_INITIALIZE_CALLS_MAX=1
MCP_INITIALIZED_NOTIFICATIONS=1
MCP_DESCRIBE_OPERATION_CALLS_MAX=5
MCP_EXECUTE_OPERATION_CALLS_MAX=0
MCP_TOOLS_LIST_CALLS_MAX=0
MCP_SEARCH_OPERATIONS_CALLS_MAX=0
GHL_BUSINESS_READS_MAX=0
GHL_MUTATIONS_MAX=0
RAW_REST_CALLS_MAX=0
MCP_SESSION_RESTARTS_MAX=0
MCP_SESSION_IDENTIFIER_DURABLE_CAPTURE=NO
MCP_SESSION_IDENTIFIER_FORWARDING=AUTHORIZED_ONLY_IF_ISSUED_BY_SUCCESSFUL_INITIALIZE

JCS_CONFORMANCE_VECTOR_PASS_REQUIRED=YES

EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO

OBSERVATION_EXECUTION_OCCURRED=NO
NEXT=HUMAN_REVIEW_AND_MERGE_AUTHORIZATION_PR
STOP_CODE=NW008_AT1_DESCRIBE_OPERATION_CONTRACT_OBSERVATION_001_EVIDENCE_RULES_REFINEMENT_READY_FOR_REVIEW
```
