# NW-008 AT-1 MCP Response Contract Plan

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_MCP_RESPONSE_CONTRACT_001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=f9359978954191519bcfe44e3f20e7ad7b43d035
PLAN_BRANCH=plan/nw008-at1-mcp-response-contract-001

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

This planning-only unit identifies the source layers that must govern the
response returned by the future established MCP session to
`At1LiveTransportAdapter._parse_response`. It records the current parser
mapping and the gaps that prevent the composite contract from being frozen.
It does not create, modify, or authorize a runtime contract.

```text
GHL_CALLS_IN_SCOPE=0
MCP_CALLS_IN_SCOPE=0
MCP_INITIALIZE_OR_PROBE_IN_SCOPE=NO
ENDPOINT_CONNECTIVITY_CHECKS_IN_SCOPE=NO
SECRET_MANAGER_ACCESS_IN_SCOPE=NO
PRIVATE_BINDING_ACCESS_IN_SCOPE=NO
SESSION_IMPLEMENTATION_IN_SCOPE=NO
RUNTIME_IMPLEMENTATION_IN_SCOPE=NO
IAM_OR_DEPLOY_CHANGE_IN_SCOPE=NO
GRANT009_DRAFTING_IN_SCOPE=NO
```

## 2. Preflight and evidence snapshot

The lane was created from fetched `origin/main` after the following durable
preconditions were verified:

| Precondition | Result |
| --- | --- |
| PR #73 (`plan/nw008-at1-live-readiness-001`) | `MERGED`; merge SHA `f9359978954191519bcfe44e3f20e7ad7b43d035` |
| PR #74 (`docs/pr-review-verification-gap-routing`) | `MERGED`; merge SHA `57d4ac27bf5e513aae764938b30b32a23a44eb36` |
| `proof/nw008/nw-008-at1-live-readiness-plan.md` on `origin/main` | Present |
| `governance/required-pr-checks.md` | Contains `External reviewer-tool unavailability` |

The following repository files are implementation evidence, not independent
wire-schema authority:

| Evidence | Source revision | SHA-256 at plan base |
| --- | --- | --- |
| `src/integrations/ghl/at1_live_transport_adapter.py` | `b56cc52913376601d40993240014148edab7a6ec` | `65d1fb585fbba3dcf42c3aa2abc5d75d0ad66ecf7622ad47874383b27446c53d` |
| `fixtures/ghl/at1-live-transport-remediation.json` | `9cdf49e73242c7dfb50de85db1c3fc8e592306ff` | `27add7dc0e38d372a5ecee830141a42a4d0e3b745349b3749fca735e8d416690` |
| `tests/integrations/ghl/test_at1_live_transport_remediation.py` | `c52261b1d5755b36bc7a3ba487edb085ddc9b9b8` | `2aa40eaf58b2ac64e952d94e852ebeae3272edd6abc00301bf6f2c3e27f4b65b` |
| `governance/required-pr-checks.md` | `bbeac1a515433dc068cda0d4127bdfd719959bf9` | `2ae5e859fcb21637325b1d3be1bea73336c7909daee8cf26cc4bc48e33835d7f` |

## 3. Composite authority decision

The response contract has three authority layers. All three must be frozen at
compatible versions before live readiness can pass.

| Layer | Required authority | Identified now | Version/revision frozen now | Decision |
| --- | --- | --- | --- | --- |
| JSON-RPC response | Official JSON-RPC 2.0 specification, especially Response Object and Error Object | Yes | Protocol version `2.0`; no immutable repository snapshot captured by this planning unit | Standards layer identified, snapshot still required |
| MCP tool result | Official Model Context Protocol schema and tools specification matching the established session's negotiated `protocolVersion` | Candidate authority identified | No negotiated protocol version, schema revision, or digest is available under this unit's authority | Not frozen |
| HighLevel `execute_operation` result | Official HighLevel MCP provider schema or provider-owned source revision defining the exact wrapper and content encoding | No | No | Blocking gap |

Locator citations for later authorized source capture:

- JSON-RPC 2.0: <https://www.jsonrpc.org/specification>
- MCP specification index: <https://modelcontextprotocol.io/specification/>
- MCP tools result: <https://modelcontextprotocol.io/specification/2025-06-18/server/tools>
- MCP authoritative schema repository:
  <https://github.com/modelcontextprotocol/specification/tree/main/schema>

These URLs are source locators, not evidence of remote retrieval in this unit.
The dated MCP URL is a known candidate, not the selected version. A later
contract implementation unit must select the version that exactly matches the
pre-grant established session's negotiated protocol version and must capture an
immutable upstream revision and digest.

No allowed repository evidence identifies whether HighLevel emits its wrapper
in `structuredContent`, in the JSON text of a typed `content` block, or in
another provider-versioned representation. The synthetic fixture's direct,
untyped object at `result.content[0]` cannot establish provider authority.

```text
JSONRPC_AUTHORITY_IDENTIFIED=YES
JSONRPC_PROTOCOL_VERSION_IDENTIFIED=2.0
MCP_BASE_AUTHORITY_IDENTIFIED=YES
MCP_NEGOTIATED_PROTOCOL_VERSION_IDENTIFIED=NO
HIGHLEVEL_EXECUTE_OPERATION_AUTHORITY_IDENTIFIED=NO

MCP_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=NO
MCP_RESPONSE_SCHEMA_VERSION_FROZEN=NO
```

## 4. Contract field register

The register separates standards-defined requirements from the unresolved
provider wrapper. `Provisional acceptance` describes the fail-closed contract
that a future implementation unit must encode after authoritative source
capture; it is not a live authorization.

| Field | Required / optional | Type and accepted constraints | Failure behavior | Source citation | Version / immutable revision |
| --- | --- | --- | --- | --- | --- |
| `jsonrpc` | Required | String exactly `"2.0"` | Reject before interpreting result | JSON-RPC 2.0 Response Object | Version `2.0`; immutable digest not captured |
| `id` | Required for this request/response exchange | Must equal the exact non-empty string request ID issued by the adapter; no coercion | Reject as request/response binding mismatch | JSON-RPC 2.0 Response Object plus adapter request binding | JSON-RPC `2.0`; adapter snapshot above |
| `result` | Required on success; mutually exclusive with `error` | MCP `CallToolResult` object | Reject missing/non-object result; reject coexistence with `error` | JSON-RPC 2.0 Response Object; MCP tools result | MCP version not frozen |
| `error` | Required on JSON-RPC failure; mutually exclusive with `result` | Object containing integer `code`, string `message`, and optional `data`; `null` is not a valid Error Object | Treat any valid error response as terminal failure; reject malformed error and result/error coexistence | JSON-RPC 2.0 Error Object | Version `2.0`; immutable digest not captured |
| `result.isError` | Optional in base MCP | Boolean; omitted means the MCP default/non-error case. A provider profile may require explicit `false` only if authoritative provider schema says so | `true` is terminal tool failure; wrong type is invalid; omission handling must follow the frozen provider profile | MCP `CallToolResult` | MCP version not frozen |
| `result.content` | Required in base MCP | Array of one or more MCP `ContentBlock` values; every block must carry a recognized `type` and satisfy that block schema | Reject empty, non-array, untyped, unknown, malformed, or unconsumed blocks | MCP `CallToolResult` and `ContentBlock` schema | MCP version not frozen |
| `result.structuredContent` | Optional in base MCP | JSON object when supplied; accepted as the HighLevel wrapper location only if the provider schema and tool output schema designate it | Reject if present but not permitted by the frozen provider profile; never silently prefer one encoding over another | MCP tools result | MCP version not frozen |
| HighLevel wrapper location | Required before parsing provider fields | Exactly one provider-authorized encoding: either `structuredContent` or decoded JSON from an authorized typed text content block | Reject zero, multiple, ambiguous, or unknown encodings | Official HighLevel provider schema required | Authority absent; version/digest unavailable |
| `operationId` | Provisional required | Non-empty string exactly equal to the dispatched operation ID; no aliases or coercion | Terminal `MCP_OPERATION_ID_MISMATCH` or successor contract-specific code | Official HighLevel `execute_operation` schema required; current parser is evidence only | Authority absent; version/digest unavailable |
| `success` | Provisional required | Boolean exactly `true` for accepted success | Any other value is terminal failure | Official HighLevel `execute_operation` schema required; current parser is evidence only | Authority absent; version/digest unavailable |
| `status` | Provisional required | JSON integer in `200..299`; booleans and numeric strings forbidden | Non-integer or non-2xx value is terminal failure | Official HighLevel `execute_operation` schema required; current parser is evidence only | Authority absent; version/digest unavailable |
| `payload` | Provisional required | JSON object; operation-specific output schema must also validate before semantic use | Non-object or operation-schema mismatch is terminal failure | Official HighLevel operation output schemas required; current parser is evidence only | Authority absent; version/digest unavailable |

### 4.1 Version-freeze record required before implementation

The later contract implementation PR must add a versioned repository contract
and record all of:

```text
NEGOTIATED_MCP_PROTOCOL_VERSION=<exact value>
MCP_SCHEMA_UPSTREAM_REPOSITORY=<official repository>
MCP_SCHEMA_UPSTREAM_REVISION=<immutable commit or release>
MCP_SCHEMA_FILE_SHA256=<digest>

HIGHLEVEL_SCHEMA_AUTHORITY=<official provider artifact>
HIGHLEVEL_SCHEMA_VERSION=<exact provider version>
HIGHLEVEL_SCHEMA_REVISION=<immutable revision where available>
HIGHLEVEL_SCHEMA_SHA256=<digest of captured source>

COMPOSITE_CONTRACT_VERSION=<repository contract version>
COMPOSITE_CONTRACT_SHA256=<digest>
```

If an official HighLevel artifact has no immutable version or digest, the
contract remains unfrozen. A screenshot, synthetic response, fixture, parser,
test expectation, undocumented sample, or one-time live observation is not
authority.

## 5. Unsupported variants and fail-closed policy

The frozen contract must reject, capture as terminal evidence, and authorize no
further business call for:

1. missing or non-`"2.0"` `jsonrpc`;
2. missing, wrong-type, or mismatched response `id`;
3. `result` and `error` both present, neither present, or malformed `error`;
4. any JSON-RPC error response;
5. `isError: true` or a non-boolean `isError`;
6. empty, non-array, untyped, malformed, or unknown MCP content blocks;
7. multiple content blocks when the frozen decoder cannot prove that every
   block is authorized and consumed;
8. ambiguous wrapper placement, including simultaneous structured and text
   representations when the provider contract does not define precedence;
9. JSON text content unless the content block is the authorized typed text
   representation and strict decoding succeeds with no trailing data;
10. `structuredContent` unless the frozen provider contract designates it;
11. missing, extra, aliased, coerced, or wrong-type provider wrapper fields
    unless the provider contract explicitly permits them;
12. `operationId` differing from the dispatched operation;
13. `success` other than JSON boolean `true`;
14. `status` outside integer `200..299`;
15. non-object `payload` or an operation-specific payload schema mismatch; and
16. any unknown MCP, HighLevel schema, or composite contract version.

No fallback between content encodings, raw REST, session repair, retry,
initialize, probe, or schema inference is allowed after grant activation.

## 6. Current adapter mapping

`At1LiveTransportAdapter._parse_response` at the plan base maps the implemented
shape as follows:

| Step | Current parser behavior | Current failure code | Frozen-contract assessment |
| --- | --- | --- | --- |
| JSON-RPC version | Does not inspect `jsonrpc` | None | Nonconforming; missing/wrong version can pass |
| Response binding | Requires `response.id == request_id` | `JSONRPC_REQUEST_ID_MISMATCH` | Conforming to the bounded binding rule |
| JSON-RPC error | Fails only when `error` is present and non-null | `JSONRPC_ERROR_PRESENT` | Nonconforming; does not validate Error Object or reject `error: null`/`result` coexistence |
| MCP result | Requires object-like `result` | `JSONRPC_RESULT_MISSING` | Partially conforming; mutual exclusivity is not enforced |
| MCP `isError` | Requires explicit `false` | `MCP_IS_ERROR_TRUE` | Fail-closed but stricter than base MCP, where the field is optional; provider profile unresolved |
| MCP content | Requires a non-empty list | `MCP_CONTENT_INVALID` | Partial only |
| Content representation | Treats `content[0]` itself as the HighLevel wrapper and requires it to be object-like | `MCP_CONTENT_INVALID` | Nonconforming with typed MCP `ContentBlock`; ignores `structuredContent` |
| Additional blocks | Ignores `content[1:]` | None | Nonconforming fail-closed policy; unknown trailing blocks can pass |
| `operationId` | Requires equality with dispatched operation | `MCP_OPERATION_ID_MISMATCH` | Provisional provider rule implemented, authority absent |
| `success` | Requires identity with boolean `true` | `MCP_OPERATION_NOT_SUCCESS` | Provisional provider rule implemented, authority absent |
| `status` | Requires Python integer in `200..299` | `MCP_OPERATION_STATUS_NOT_SUCCESS` | Provisional provider rule implemented, authority absent |
| `payload` | Requires object-like mapping and returns a shallow dictionary copy | `MCP_OPERATION_PAYLOAD_INVALID` | Provisional wrapper check only; operation payload schema is not validated here |

The synthetic fixture encodes each successful response as:

```json
{
  "jsonrpc": "2.0",
  "id": "__REQUEST_ID__",
  "result": {
    "isError": false,
    "content": [
      {
        "operationId": "get-contact",
        "success": true,
        "status": 200,
        "payload": {}
      }
    ]
  }
}
```

That direct object lacks an MCP content-block `type` discriminator. Other test
evidence stores examples using `result.structuredContent`, but those examples
exercise durable store state transitions rather than `_parse_response`, and
the parser does not consume that representation. Neither synthetic form proves
the HighLevel provider's authoritative wire output.

### 6.1 Exact mismatches

The planning review identifies these implementation changes as required, but
does not make them:

1. validate `jsonrpc == "2.0"`;
2. enforce JSON-RPC `result`/`error` exclusivity and validate the Error Object;
3. replace the raw `content[0]` assumption with the one provider-authorized,
   versioned MCP content representation;
4. validate or reject every content block rather than ignoring trailing blocks;
5. apply the frozen `isError` omission rule;
6. validate the provider wrapper and operation-specific payload against the
   captured, versioned schemas; and
7. bind parsing to the frozen composite contract version with no fallback.

Because standards-level mismatches are already demonstrable, adapter
conformance is `NO`, not merely `UNKNOWN`. The unresolved HighLevel authority
may add requirements; it cannot remove the need to validate the JSON-RPC and
MCP layers.

```text
CURRENT_ADAPTER_CONFORMS=NO
CONTRACT_IMPLEMENTATION_CHANGE_REQUIRED=YES
```

## 7. Follow-on implementation gate

No implementation may begin from this plan alone. A separately authorized
contract implementation unit must:

1. obtain the negotiated MCP protocol version through an authorized pre-grant
   session-establishment process, not by a post-grant initialize or probe;
2. capture the matching official MCP schema at an immutable revision;
3. obtain official, provider-owned HighLevel `execute_operation` output schema
   evidence without private binding or secret disclosure;
4. freeze the composite schema and digests in the repository;
5. update parser, fixtures, and tests in an implementation-class PR;
6. add negative tests for every unsupported variant in section 5; and
7. prove exact parser/schema conformance with deterministic offline tests.

Until all items pass:

```text
AT1_LIVE_READINESS=FAIL
LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

## 8. Planning PR validation and review gate

This PR is `planning_only`. Its writable scope is exactly:

```text
proof/nw008/nw-008-at1-mcp-response-contract-plan.md
```

Required validation:

1. `git diff --check`;
2. exactly one changed path, equal to the path above;
3. repository deterministic verification with no GHL, MCP, endpoint, secret,
   private-binding, or other runtime network call;
4. exact-head `Phase 1 deterministic validation` success; and
5. clean mergeability into `main`.

If an external reviewer connector is unavailable, apply
`governance/required-pr-checks.md` section 7.3. Connector outage alone must not
create a repair lane or reopen runtime scope.

## 9. Decision

```text
MCP_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=NO
MCP_RESPONSE_SCHEMA_VERSION_FROZEN=NO

CURRENT_ADAPTER_CONFORMS=NO
CONTRACT_IMPLEMENTATION_CHANGE_REQUIRED=YES

NETWORK_CALLS_EXECUTED=0
GHL_CALLS_EXECUTED=0
MCP_CALLS_EXECUTED=0

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

NEXT=MCP_RESPONSE_CONTRACT_REVIEW
STOP_CODE=NW008_AT1_MCP_RESPONSE_CONTRACT_PLAN_READY_FOR_REVIEW
```
