# NW-008 AT-1 MCP Response Source Capture

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_MCP_RESPONSE_SOURCE_CAPTURE_001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=b84b6ff50bf80261f89feac168ed0cdcbcf07a35
PLAN_BRANCH=plan/nw008-at1-mcp-response-source-capture-001
SUPERSEDES_GAP_FROM=proof/nw008/nw-008-at1-mcp-response-contract-plan.md

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

This planning-only unit executes the source-capture step required by
`proof/nw008/nw-008-at1-mcp-response-contract-plan.md` section 7.1. It freezes
every response-contract layer that can be established from immutable official
sources. It does not implement parser or session code and does not contact the
live MCP endpoint.

```text
GHL_CALLS_IN_SCOPE=0
MCP_CALLS_IN_SCOPE=0
NETWORK_TO_LIVE_GHL_MCP=FORBIDDEN
MCP_INITIALIZE=FORBIDDEN
MCP_TOOLS_LIST=FORBIDDEN
MCP_EXECUTE_OPERATION=FORBIDDEN
PRIVATE_TOKEN_ACCESS_IN_SCOPE=NO
PRIVATE_BINDING_ACCESS_IN_SCOPE=NO
SECRET_MANAGER_ACCESS_IN_SCOPE=NO
IAM_OR_DEPLOY_CHANGE_IN_SCOPE=NO
SESSION_IMPLEMENTATION_IN_SCOPE=NO
PARSER_IMPLEMENTATION_IN_SCOPE=NO
```

All network retrieval in this unit was read-only retrieval of static public
documentation and public specification source files. No GHL or MCP
business/control-plane traffic was generated.

## 2. Preflight and evidence snapshot

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | `plan/nw008-at1-mcp-response-source-capture-001` created from fetched `origin/main` |
| PR #75 reviewed head `db90a9a3554ab6036a9aede0c9fe863852913166` is ancestor of `origin/main` | YES (`git merge-base --is-ancestor` exit 0) |
| PR #75 merge SHA on `origin/main` | `b84b6ff50bf80261f89feac168ed0cdcbcf07a35` (equals `origin/main` tip) |
| `proof/nw008/nw-008-at1-mcp-response-contract-plan.md` on `origin/main` | Present (`git cat-file -e` exit 0) |

```text
PR75_REVIEWED_HEAD=db90a9a3554ab6036a9aede0c9fe863852913166
PR75_MERGE_SHA=b84b6ff50bf80261f89feac168ed0cdcbcf07a35
PR75_MAIN_REACHABLE=YES
```

## 3. Source capture: JSON-RPC 2.0

Canonical authority: the official JSON-RPC 2.0 Specification.

| Attribute | Value |
| --- | --- |
| Canonical URL | `https://www.jsonrpc.org/specification` |
| Protocol version frozen | `2.0` |
| Retrieved (UTC) | 2026-08-17T23:37Z |
| Response body size | 24512 bytes |
| Body SHA-256 | `8fe1edfdca511d309e712e47447457ea5159b728ec02071a84593aed692aefeb` |
| Versioned upstream repository | None found (`json-rpc/json-rpc.github.io`, `jsonrpcx/json-rpc.org`, `json-rpc/specification` all 404 on GitHub) |

Facts established from the captured source:

1. A successful response carries `jsonrpc` exactly `"2.0"`, an `id` member
   identical to the request `id`, and a `result` member; `result` and `error`
   are mutually exclusive and one of them is required.
2. On error, the response carries an Error Object with integer `code`, string
   `message`, and optional `data`; `error: null` on success is not a valid
   Error Object usage under the frozen profile.

Freeze treatment: the specification has no versioned upstream repository, so
this unit freezes the captured body digest above plus retrieval timestamp as
the immutable snapshot. Any future change in the digest reopens this layer.

```text
JSONRPC_AUTHORITY_CAPTURED=YES
JSONRPC_REVISION_FROZEN=YES
JSONRPC_AUTHORITY_SNAPSHOT_REVISION=jsonrpc.org/specification @ 2026-08-17T23:37Z
JSONRPC_AUTHORITY_SNAPSHOT_SHA256=8fe1edfdca511d309e712e47447457ea5159b728ec02071a84593aed692aefeb
```

## 4. Source capture: MCP

### 4.1 Protocol version

```text
MCP_PROTOCOL_VERSION_CANDIDATE=2025-11-25
SUPPORTED_MCP_PROTOCOL_VERSION=UNKNOWN
```

`2025-11-25` is confirmed to exist as an official MCP protocol version: the
specification index page and the authoritative schema repository both carry
that dated revision, and the pinned `schema.ts` declares
`LATEST_PROTOCOL_VERSION = "2025-11-25"`.

`SUPPORTED_MCP_PROTOCOL_VERSION` remains `UNKNOWN`. Compatibility with the
intended HighLevel session cannot be established without live probing (the
server's supported versions are only observable via `initialize`, which this
unit forbids), so per the unit instructions the supported version is not set.

### 4.2 Immutable schema capture

| Attribute | Value |
| --- | --- |
| Upstream repository | `github.com/modelcontextprotocol/specification` |
| Pinned revision | `c4c367f9f58296a7053f5c78a52fd02bfbb56a49` (2026-07-27T14:20:44Z; last commit touching any captured 2025-11-25 file) |
| `schema/2025-11-25/schema.ts` SHA-256 | `e74b56e73b2e37bdb595f74ba22e428ad7f07aa3519355ba661d681298ed38ac` (66671 bytes) |
| `schema/2025-11-25/schema.json` SHA-256 | `268a5f82ba70fd7e4b6dc4aa1e64f116f74b4d0edcb69dc046829c79dd4e97e7` (174323 bytes) |
| `docs/specification/2025-11-25/server/tools.mdx` SHA-256 | `39e56ad4f3d1ff1cb28ee62283e02947cd97db8aa6190782d629f4562a0f354c` |
| `docs/specification/2025-11-25/basic/lifecycle.mdx` SHA-256 | `45a6e8b7fb8c96e7b9ba1b0a3c727e8451c1e55bf56bb62f3ab63fddc365b919` |
| `schema/2025-11-25/schema.mdx` SHA-256 | `03c66be1ec2c04c7d62d4443f47f0b9ac6213656168a4316b169fc96aaf9ec15` |

All rendered documentation pages under
`https://modelcontextprotocol.io/specification/2025-11-25/...` are generated
from the pinned repository paths above.

### 4.3 Required MCP facts captured

From pinned `schema.ts` (`c4c367f`):

1. `CallToolResult.content` — required; `ContentBlock[]`, "A list of content
   objects that represent the unstructured result of the tool call."
2. `CallToolResult.structuredContent` — optional; JSON object
   (`{ [key: string]: unknown }`), "the structured result of the tool call."
3. `CallToolResult.isError` — optional boolean; "If not set, this is assumed
   to be false (the call was successful)." Tool-originated errors SHOULD be
   reported inside the result with `isError: true`, not as protocol errors.
4. `Tool.outputSchema` — optional JSON Schema object "defining the structure
   of the tool's output returned in the `structuredContent` field of a
   `CallToolResult`"; defaults to JSON Schema 2020-12; restricted to
   `type: "object"` at the root.
5. `JSONRPCResultResponse` — `{ jsonrpc: typeof JSONRPC_VERSION; id: RequestId;
   result: Result }`.
6. `JSONRPCErrorResponse` — `{ jsonrpc: typeof JSONRPC_VERSION; id?: RequestId;
   error: Error }`.
7. `JSONRPCResponse = JSONRPCResultResponse | JSONRPCErrorResponse`.

From pinned `lifecycle.mdx` (version negotiation semantics):

- The client MUST send a protocol version it supports in `initialize`; the
  server MUST respond with the same version if supported, otherwise with
  another version it supports; if the client does not support the server's
  version it SHOULD disconnect.
- Over HTTP, the client MUST send the `MCP-Protocol-Version` header on all
  subsequent requests.

From pinned `tools.mdx`:

- If an `outputSchema` is provided, servers MUST provide structured results
  conforming to it and clients SHOULD validate structured results against it.
- A tool returning structured content SHOULD also return the serialized JSON
  in a `TextContent` block for backwards compatibility.

### 4.4 Advertised-schema capability of the candidate version

The candidate version defines `Tool.outputSchema` and `structuredContent`, so
the conditional pre-grant advertised-schema authority path from the contract
plan section 3.2 is protocol-supported by this version:

```text
MCP_ADVERTISED_SCHEMA_SUPPORTED_BY_CANDIDATE_VERSION=YES
MCP_TOOL_RESULT_SCHEMA_CAPTURED=YES
MCP_SCHEMA_REVISION_FROZEN=YES
MCP_SCHEMA_UPSTREAM_REPOSITORY=github.com/modelcontextprotocol/specification
MCP_SCHEMA_UPSTREAM_REVISION=c4c367f9f58296a7053f5c78a52fd02bfbb56a49
MCP_SCHEMA_FILE_SHA256=e74b56e73b2e37bdb595f74ba22e428ad7f07aa3519355ba661d681298ed38ac
```

## 5. Source capture: HighLevel / LeadConnector MCP

Official provider documentation located:

| Attribute | Value |
| --- | --- |
| Doc URL | `https://marketplace.gohighlevel.com/docs/other/mcp` (redirects to `.../index.html`, HTTP 200) |
| Page title | "LeadConnector MCP Server \| HighLevel API" |
| Document class | Living Docusaurus page; no datestamp, no immutable permalink, no per-page version pin |
| Retrieved (UTC) | 2026-08-17T23:44Z |
| Response body size | 63883 bytes |
| Body SHA-256 | `e8bb3640d785465c32c0117a6376adc797ca5efca1cd4201c5743fad00dbc82a` |

Facts established from the captured page (verified in this unit against the
retrieved body):

1. Endpoint pattern: "the per-client endpoint
   `https://services.leadconnectorhq.com/mcp/{client}/v2` — live today for
   Claude at `/mcp/anthropic/v2`". The original `https://services.leadconnectorhq.com/mcp/`
   endpoint also remains available.
2. The per-client endpoint exposes six unified tools, including
   `execute_operation` ("Run one operation, subject to your scopes and
   built-in safety checks"), `describe_operation` ("Inspect an operation's
   inputs before running it"), `search`, `fetch`, `search_operations`, and
   `list_locations`.
3. Grant/scope behavior: OAuth (recommended) "makes the widest set of scopes
   available"; a Private Integration Token "offers a more limited set of
   scopes than OAuth"; "the integration can only do what the scopes you grant
   allow." Per-tool scope requirements are not enumerated on this page.

Facts NOT established (searched for specifically; absent from the page):

- `execute_operation` input schema (no machine-readable input schema);
- `execute_operation` output schema — no statement of `operationId`,
  `success`, `status`, `payload`, or any other wrapper field;
- whether results are returned as `CallToolResult.structuredContent`, as
  serialized JSON in a typed text content block, or in another encoding;
- any provider wrapper field names at all.

No fields are inferred. The wrapper shape assumed by the current parser
remains provisional evidence only (`SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO`).

```text
STATIC_HIGHLEVEL_MCP_DOC_FOUND=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_TOOL_CONFIRMED=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_OUTPUT_SCHEMA_FOUND=NO
```

## 6. Operation payload sources

Official machine-readable authority: the provider-owned public repository
`github.com/GoHighLevel/highlevel-api-docs` ("This repository contains the
source documentation for the GoHighLevel API V2"), per-domain OpenAPI 3.0.0
files under `apps/`. Although the repository tracks `main` without release
tags, pinning to an exact commit plus per-file digest freezes each schema
immutably.

| Attribute | Value |
| --- | --- |
| Upstream repository | `github.com/GoHighLevel/highlevel-api-docs` |
| Pinned revision | `d9cbcd5adb6df45c3efcfd09155592312e1ca4b5` (2026-05-01T11:59:09Z; last commit touching both captured files) |
| `apps/contacts.json` SHA-256 | `d251defab9b0d3ae2feb393b27c071bed7e964c63826af0131bb8e888ecfd6cb` (133996 bytes) |
| `apps/opportunities.json` SHA-256 | `bd2c63ca4ef9929fb996a04c873e7300b7d3fe5737200270e7f2270dce26e1ba` (58000 bytes) |

Both files declare `"openapi": "3.0.0"` and server
`https://services.leadconnectorhq.com`. All five operation entries below were
verified programmatically against the pinned files in this unit:

| Ordinal | Operation | Method / path | Success response | Success schema (`$ref`) | OAuth scope |
| --- | --- | --- | --- | --- | --- |
| 1 | `get-contact` | GET `/contacts/{contactId}` | 200 | `#/components/schemas/ContactsByIdSuccessfulResponseDto` | `contacts.readonly` |
| 2 | `get-opportunity` | GET `/opportunities/{id}` | 200 | `#/components/schemas/GetPostOpportunitySuccessfulResponseDto` | `opportunities.readonly` |
| 3 | `create-note` | POST `/contacts/{contactId}/notes` | 201 | `#/components/schemas/GetCreateUpdateNoteSuccessfulResponseDto` | `contacts.write` |
| 4 | `get-note` | GET `/contacts/{contactId}/notes/{id}` | 200 | `#/components/schemas/GetCreateUpdateNoteSuccessfulResponseDto` | `contacts.readonly` |
| 5 | `update-opportunity` | PUT `/opportunities/{id}` | 200 | `#/components/schemas/GetPostOpportunitySuccessfulResponseDto` | `opportunities.write` |
| 6 | `get-opportunity` (second ordinal) | same as ordinal 2 | 200 | same as ordinal 2 | `opportunities.readonly` |

The final ordinal reuses the `get-opportunity` schema, as planned.

These schemas freeze the business payload layer only. They define the REST
response bodies (`contact`, `opportunity`, `note` envelopes) that the
`payload` member of the provider wrapper must ultimately carry. They do not
define the MCP-level wrapper (`operationId`/`success`/`status`/`payload` or
its content encoding), which remains unfrozen per section 5. Generic
`execute_operation` wrapper validation stays separate from these business
payload schemas:

```text
GENERIC_PROVIDER_WRAPPER_VALIDATION_SEPARATE_FROM_OPERATION_PAYLOAD_VALIDATION=YES
OPERATION_PAYLOAD_SCHEMAS_FROZEN=YES
OPERATION_PAYLOAD_SCHEMA_UPSTREAM_REPOSITORY=github.com/GoHighLevel/highlevel-api-docs
OPERATION_PAYLOAD_SCHEMA_UPSTREAM_REVISION=d9cbcd5adb6df45c3efcfd09155592312e1ca4b5
OPERATION_PAYLOAD_CONTACTS_SHA256=d251defab9b0d3ae2feb393b27c071bed7e964c63826af0131bb8e888ecfd6cb
OPERATION_PAYLOAD_OPPORTUNITIES_SHA256=bd2c63ca4ef9929fb996a04c873e7300b7d3fe5737200270e7f2270dce26e1ba
```

## 7. Freeze decision

```text
JSONRPC_AUTHORITY_CAPTURED=YES
JSONRPC_REVISION_FROZEN=YES

MCP_PROTOCOL_VERSION_CANDIDATE=2025-11-25
SUPPORTED_MCP_PROTOCOL_VERSION=UNKNOWN

MCP_TOOL_RESULT_SCHEMA_CAPTURED=YES
MCP_SCHEMA_REVISION_FROZEN=YES

STATIC_HIGHLEVEL_MCP_DOC_FOUND=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_TOOL_CONFIRMED=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_OUTPUT_SCHEMA_FOUND=NO

MCP_ADVERTISED_SCHEMA_SUPPORTED_BY_CANDIDATE_VERSION=YES

OPERATION_PAYLOAD_SCHEMAS_FROZEN=YES

HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

Rationale:

1. JSON-RPC 2.0 and the MCP 2025-11-25 tool-result schema are frozen at
   immutable, digest-bound revisions.
2. The five AT-1 operation payload schemas are frozen at a pinned,
   digest-bound provider revision; the sixth ordinal reuses `get-opportunity`.
3. The HighLevel provider wrapper cannot be frozen statically: the official
   documentation confirms the `execute_operation` tool exists but publishes no
   output schema and no content-encoding statement. The doc page is a living
   document with no immutable version, so even its prose cannot be
   digest-pinned durably.
4. `SUPPORTED_MCP_PROTOCOL_VERSION` stays `UNKNOWN` because compatibility with
   the intended HighLevel session cannot be established without live probing,
   which this unit forbids.

Because the provider wrapper cannot be frozen statically:

```text
PREGRANT_TOOLS_LIST_REQUIRED=YES
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

The conditional fallback path from the contract plan section 3.2 remains
available in principle: the candidate MCP version defines `Tool.outputSchema`
and `structuredContent`, so a separately authorized pre-grant advertised
schema, captured, version-bound, and digest-bound before grant activation,
could satisfy provider authority. No `tools/list` was run in this unit.

## 8. Next decision

`COMPOSITE_CONTRACT_FREEZE_READY=NO` and `PREGRANT_TOOLS_LIST_REQUIRED=YES`,
therefore:

```text
NEXT=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001_AUTHORIZATION_REVIEW
```

That future authorization is NOT created by this planning unit. No
preparation, drafting, or execution of a grant-009-class authorization
occurred here.

## 9. Validation and PR

This PR is `planning_only`. Its writable scope is exactly:

```text
proof/nw008/nw-008-at1-mcp-response-source-capture.md
```

Validation performed at exact head
`b84b6ff50bf80261f89feac168ed0cdcbcf07a35` (branch created directly from
fetched `origin/main`):

1. `git diff --check` — clean;
2. exactly one changed path, equal to the path above;
3. `scripts/verify_phase1_deterministic.py` under Python 3.9 with pinned
   `requirements.txt` — all six checks PASS (YAML parse; packet schema
   validation; three fixture outcomes; replay/idempotency; mutation intent
   bounds; proof-return schema validation);
4. zero GHL/MCP business or control-plane traffic: no `initialize`, no
   `tools/list`, no `execute_operation`, no endpoint connectivity checks, no
   secret or private-binding access.

The `Phase 1 deterministic validation` GitHub check is required on the PR at
exact head.

```text
NETWORK_CALLS_TO_LIVE_GHL_MCP=0
GHL_CALLS_EXECUTED=0
MCP_CALLS_EXECUTED=0

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

NEXT=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001_AUTHORIZATION_REVIEW
STOP_CODE=NW008_AT1_MCP_RESPONSE_SOURCE_CAPTURE_READY_FOR_REVIEW
```
