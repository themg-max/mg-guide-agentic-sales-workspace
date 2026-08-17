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
compatible versions before live readiness can pass. Protocol and schema
selection are planning-time only. Runtime must bind to one pre-frozen composite
contract; it must not discover, negotiate, or switch schemas.

| Layer | Required authority | Identified now | Version/revision frozen now | Decision |
| --- | --- | --- | --- | --- |
| JSON-RPC response | Official JSON-RPC 2.0 specification, especially Response Object and Error Object | Yes | Protocol version `2.0`; no immutable repository snapshot captured by this planning unit | Locator identified; snapshot still required |
| MCP tool result | Official Model Context Protocol tools/result schema for one planning-selected supported protocol version | Locator yes | Supported protocol version not selected; schema revision/digest not captured | Locator identified; tool-result schema not frozen |
| HighLevel `execute_operation` result | Official HighLevel MCP provider schema or provider-owned source revision defining the exact wrapper and content encoding | No | No | Blocking gap |

### 3.1 Supported MCP protocol version selection (no dynamic runtime selection)

The repository must freeze exactly one supported MCP protocol version before any
parser or live-session implementation binds to MCP result shapes. Pre-grant
session establishment may only accept a negotiated protocol version that equals
that frozen supported version. A negotiated mismatch is terminal fail-closed.
Runtime schema selection, multi-version decode tables, and post-grant schema
discovery are forbidden.

```text
SUPPORTED_MCP_PROTOCOL_VERSION_SELECTION_REQUIRED=YES
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES
RUNTIME_SCHEMA_SELECTION_ALLOWED=NO
POST_GRANT_SCHEMA_DISCOVERY_ALLOWED=NO
SUPPORTED_MCP_PROTOCOL_VERSION=NOT_SELECTED
```

Locator citations for later authorized source capture (locators only; not
retrieval evidence and not a selected version):

- JSON-RPC 2.0: <https://www.jsonrpc.org/specification>
- MCP specification index: <https://modelcontextprotocol.io/specification/>
- MCP tools result candidate page:
  <https://modelcontextprotocol.io/specification/2025-06-18/server/tools>
- MCP authoritative schema repository:
  <https://github.com/modelcontextprotocol/specification/tree/main/schema>

The dated MCP URL is a known candidate locator only. It is not the supported
protocol version and must not be treated as selected until a later source-capture
unit freezes an exact version, upstream revision, and digest.

### 3.2 Provider-authority hierarchy

Provider authority is ranked and exclusive. Lower ranks may be used only when
higher ranks are unavailable and only under the stated conditions.

| Rank | Path | Status in this plan | Rule |
| --- | --- | --- | --- |
| 1 | Official static HighLevel documentation or provider-owned schema artifact for `execute_operation` | Preferred; availability unknown | `HIGHLEVEL_PROVIDER_AUTHORITY_PATH_STATIC_DOC=ALLOWED` |
| 2 | Separately authorized pre-grant advertised tool/output schema, only if the frozen supported MCP version defines such advertisement and the exact schema is captured, version-bound, and digest-bound before grant activation | Conditional fallback | `HIGHLEVEL_PROVIDER_AUTHORITY_PATH_PREGRANT_ADVERTISED_SCHEMA=CONDITIONALLY_ALLOWED_IF_MCP_SPEC_SUPPORTS_AND_SCHEMA_IS_CAPTURED_BOUND` |
| Forbidden | Sample responses, synthetic fixtures, parser behavior, tests, one-time live observations, screenshots, or undocumented dumps | Forbidden as authority | `SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO` |

No allowed repository evidence identifies whether HighLevel emits its wrapper
in `structuredContent`, in the JSON text of a typed `content` block, or in
another provider-versioned representation. The synthetic fixture's direct,
untyped object at `result.content[0]` cannot establish provider authority.

### 3.3 Validation separation

Generic HighLevel provider-wrapper validation is separate from
operation-specific payload validation. The composite contract must freeze both:

1. the provider wrapper (`operationId`, `success`, `status`, `payload` container,
   and the exact encoding location); and
2. the six AT-1 operation payload schemas (`get-contact`, `get-opportunity`,
   `create-note`, `get-note`, `update-opportunity`, and the second
   `get-opportunity` ordinal under the same operation payload schema).

A response may not be treated as business-success unless both layers pass.
Wrapper success does not authorize skipping operation payload schema checks.

```text
GENERIC_PROVIDER_WRAPPER_VALIDATION_SEPARATE_FROM_OPERATION_PAYLOAD_VALIDATION=YES
```

### 3.4 Authority freeze status

```text
JSONRPC_AUTHORITY_LOCATOR_IDENTIFIED=YES
JSONRPC_AUTHORITY_SNAPSHOT_FROZEN=NO

MCP_AUTHORITY_LOCATOR_IDENTIFIED=YES
MCP_TOOL_RESULT_SCHEMA_FROZEN=NO

HIGHLEVEL_AUTHORITY_LOCATOR_IDENTIFIED=NO
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO

HIGHLEVEL_PROVIDER_AUTHORITY_PATH_STATIC_DOC=ALLOWED
HIGHLEVEL_PROVIDER_AUTHORITY_PATH_PREGRANT_ADVERTISED_SCHEMA=CONDITIONALLY_ALLOWED_IF_MCP_SPEC_SUPPORTS_AND_SCHEMA_IS_CAPTURED_BOUND
SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO

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

A later source-capture planning unit, then a separately authorized contract
implementation unit, must freeze and record all of:

```text
SUPPORTED_MCP_PROTOCOL_VERSION=<exact value selected at planning time>
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES
RUNTIME_SCHEMA_SELECTION_ALLOWED=NO
POST_GRANT_SCHEMA_DISCOVERY_ALLOWED=NO

JSONRPC_AUTHORITY_SNAPSHOT_REVISION=<immutable source/revision>
JSONRPC_AUTHORITY_SNAPSHOT_SHA256=<digest>

MCP_SCHEMA_UPSTREAM_REPOSITORY=<official repository>
MCP_SCHEMA_UPSTREAM_REVISION=<immutable commit or release matching supported version>
MCP_SCHEMA_FILE_SHA256=<digest>
MCP_TOOL_RESULT_SCHEMA_FROZEN=YES

HIGHLEVEL_PROVIDER_AUTHORITY_PATH=<STATIC_DOC|PREGRANT_ADVERTISED>
HIGHLEVEL_SCHEMA_AUTHORITY=<official provider artifact or captured advertisement>
HIGHLEVEL_SCHEMA_VERSION=<exact provider version>
HIGHLEVEL_SCHEMA_REVISION=<immutable revision where available>
HIGHLEVEL_SCHEMA_SHA256=<digest of captured source>
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=YES

GENERIC_PROVIDER_WRAPPER_VALIDATION_SEPARATE_FROM_OPERATION_PAYLOAD_VALIDATION=YES
OPERATION_PAYLOAD_SCHEMAS_FROZEN=YES

COMPOSITE_CONTRACT_VERSION=<repository contract version>
COMPOSITE_CONTRACT_SHA256=<digest>
```

If an official HighLevel artifact has no immutable version or digest, and the
conditional pre-grant advertisement path is not both MCP-supported and
captured/bound, the contract remains unfrozen. A screenshot, synthetic
response, fixture, parser, test expectation, undocumented sample, or one-time
live observation is not authority (`SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO`).

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

## 7. Follow-on gates

No implementation may begin from this plan alone.

### 7.1 Source-capture planning unit (next, after this plan merges)

After this plan is reviewed and merged, a separate planning-only unit
`NW008_AT1_MCP_RESPONSE_SOURCE_CAPTURE_001` must answer, without runtime
mutation:

1. what immutable JSON-RPC 2.0 source/revision is captured;
2. what single supported MCP protocol version the reviewed runtime will accept;
3. what immutable MCP tools/schema revision corresponds to that version;
4. whether that version defines an advertised tool/output schema usable under
   the conditional HighLevel authority path;
5. whether an official static HighLevel `execute_operation` schema is available;
6. if not, whether a future separately authorized pre-grant tools/schema
   advertisement can satisfy provider authority under section 3.2;
7. what exact wrapper fields are provider-defined;
8. what exact operation payload schemas apply to each of the six AT-1 ops; and
9. what composite contract version/digest will bind these layers.

That unit still executes zero GHL/MCP/network calls unless a later explicit
authority grants a different scope. This plan does not authorize that capture.

### 7.2 Contract implementation unit (only after freeze)

A separately authorized contract implementation unit may begin only after
source capture freezes the composite contract. It must:

1. bind exclusively to the frozen supported MCP protocol version and captured
   schema digests;
2. refuse any pre-grant negotiated protocol version that does not equal the
   supported version;
3. implement no runtime schema selection and no post-grant schema discovery;
4. validate the generic provider wrapper separately from each operation payload
   schema;
5. update parser, fixtures, and tests in an implementation-class PR;
6. add negative tests for every unsupported variant in section 5; and
7. prove exact parser/schema conformance with deterministic offline tests.

Until all freeze and implementation gates pass:

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
SUPPORTED_MCP_PROTOCOL_VERSION_SELECTION_REQUIRED=YES
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES
RUNTIME_SCHEMA_SELECTION_ALLOWED=NO
POST_GRANT_SCHEMA_DISCOVERY_ALLOWED=NO

JSONRPC_AUTHORITY_LOCATOR_IDENTIFIED=YES
JSONRPC_AUTHORITY_SNAPSHOT_FROZEN=NO

MCP_AUTHORITY_LOCATOR_IDENTIFIED=YES
MCP_TOOL_RESULT_SCHEMA_FROZEN=NO

HIGHLEVEL_AUTHORITY_LOCATOR_IDENTIFIED=NO
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO

HIGHLEVEL_PROVIDER_AUTHORITY_PATH_STATIC_DOC=ALLOWED
HIGHLEVEL_PROVIDER_AUTHORITY_PATH_PREGRANT_ADVERTISED_SCHEMA=CONDITIONALLY_ALLOWED_IF_MCP_SPEC_SUPPORTS_AND_SCHEMA_IS_CAPTURED_BOUND
SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO

GENERIC_PROVIDER_WRAPPER_VALIDATION_SEPARATE_FROM_OPERATION_PAYLOAD_VALIDATION=YES

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
