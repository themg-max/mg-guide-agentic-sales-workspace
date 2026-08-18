# NW-008 AT-1 Provider Response-Contract Gap 001

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_PROVIDER_RESPONSE_CONTRACT_GAP_001
OWNER=VS Code / MG Orchestrator
PHASE=planning_only
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=781f8ce90c7b63fc8e23eec62dda7544bda8d143
PLAN_BRANCH=plan/nw008-at1-provider-response-contract-gap-001

SUPERSEDES_GAP_FROM=
  proof/nw008/nw-008-at1-mcp-response-contract-plan.md
  proof/nw008/nw-008-at1-mcp-response-source-capture.md
  proof/nw008/nw-008-at1-pregrant-mcp-contract-observation-001.md

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
GRANT009_DRAFTING_IN_SCOPE=NO
```

This planning-only unit evaluates whether an authoritative, stable
response-contract strategy can be established for the future AT-1 adapter
boundary without inferring undocumented HighLevel `execute_operation` wrapper
fields. It binds only already-merged PR #76 / #77 / #78 evidence. It does not
contact the live MCP endpoint, does not call any advertised tool, does not
perform GHL business reads or mutations, and does not implement parser,
session, or runtime code.

```text
GHL_CALLS_IN_SCOPE=0
MCP_CALLS_IN_SCOPE=0
NETWORK_TO_LIVE_GHL_MCP=FORBIDDEN
MCP_INITIALIZE=FORBIDDEN
MCP_TOOLS_LIST=FORBIDDEN
MCP_EXECUTE_OPERATION=FORBIDDEN
TOOLS_CALL=FORBIDDEN
GHL_BUSINESS_READ=FORBIDDEN
GHL_MUTATION=FORBIDDEN
RAW_REST_WORKAROUND=FORBIDDEN
SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO
PRIVATE_TOKEN_ACCESS_IN_SCOPE=NO
PRIVATE_BINDING_ACCESS_IN_SCOPE=NO
SECRET_MANAGER_ACCESS_IN_SCOPE=NO
IAM_OR_DEPLOY_CHANGE_IN_SCOPE=NO
SESSION_IMPLEMENTATION_IN_SCOPE=NO
PARSER_IMPLEMENTATION_IN_SCOPE=NO
GRANT009_DRAFTING_IN_SCOPE=NO
```

## 2. Preflight and evidence binding

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES (`plan/nw008-at1-provider-response-contract-gap-001`) |
| `git fetch origin` | YES |
| Reviewed observation head `b16f49ca3813746614e228dd4433d88cf6b0cfc5` is ancestor of `origin/main` | YES (`git merge-base --is-ancestor` exit 0) |
| Observation proof path present on `origin/main` | YES (`git cat-file -e`) |
| Plan base equals current `origin/main` tip | YES (`781f8ce90c7b63fc8e23eec62dda7544bda8d143`, PR #78 merge) |

```text
PR76_SOURCE_CAPTURE=proof/nw008/nw-008-at1-mcp-response-source-capture.md
PR76_SOURCE_CAPTURE_BLOB_SHA=5c1cbb7698b24e65c92749dd7963c460aa092b1a
PR76_REVIEWED_HEAD=fb0da6d41484ae44aae06b86a4e78788ca4b211b
PR76_MERGE_SHA=262fc1670a910e147de4e634117002fd38172e87
PR76_MAIN_REACHABLE=YES

PR77_AUTHORIZATION=governance/authorizations/nw008-at1-pregrant-mcp-contract-observation-001.md
PR77_AUTHORIZATION_BLOB_SHA=44aa3b97f304a9dad97d0a43f783104085422da5
PR77_REVIEWED_HEAD=ec61a43131db1cde21581d651f2d04e970144573
PR77_MERGE_SHA=c55bf90bd652b94dc3cbea8085357205f64676f1
PR77_MAIN_REACHABLE=YES

PR78_OBSERVATION_PROOF=proof/nw008/nw-008-at1-pregrant-mcp-contract-observation-001.md
PR78_OBSERVATION_PROOF_BLOB_SHA=af74ebf9332e21f57a6c9b0bd9b58ac9973c2ec8
PR78_REVIEWED_HEAD=b16f49ca3813746614e228dd4433d88cf6b0cfc5
PR78_MERGE_SHA=781f8ce90c7b63fc8e23eec62dda7544bda8d143
PR78_MAIN_REACHABLE=YES
```

## 3. Observed state inherited from PR #78 (not re-observed)

The following fields are accepted as durable observation results from the
merged pre-grant proof. This unit does not re-run `initialize`, `tools/list`,
or any tool call.

```text
SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
PROTOCOL_VERSION_MATCH=YES

EXECUTE_OPERATION_TOOL_PRESENT=YES
EXECUTE_OPERATION_INPUT_SCHEMA_CAPTURED=YES
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE

HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

Supporting freeze state already established by PR #76 and not reopened here:

```text
JSONRPC_REVISION_FROZEN=YES
MCP_SCHEMA_REVISION_FROZEN=YES
OPERATION_PAYLOAD_SCHEMAS_FROZEN=YES
MCP_ADVERTISED_SCHEMA_SUPPORTED_BY_SELECTED_VERSION=YES
PREGRANT_ADVERTISED_SCHEMA_PATH_ELIGIBLE=YES
STATIC_HIGHLEVEL_MCP_DOC_FOUND=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_TOOL_CONFIRMED=YES
STATIC_HIGHLEVEL_EXECUTE_OPERATION_OUTPUT_SCHEMA_FOUND=NO
SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO
```

## 4. Evaluation procedure

The response-contract strategy is evaluated in the required order. Each step
may close the gap only with provider-owned or standards-owned authority. No
step may invent wrapper fields, promote sample responses, or treat the current
parser mapping as schema authority.

### 4.1 Rank-1 — official provider-owned machine-readable source for `execute_operation` output semantics

| Question | Finding | Authority basis |
| --- | --- | --- |
| Does a provider-owned machine-readable artifact define `execute_operation` output? | NO | PR #76 section 5–7; PR #78 section 7 and 10 |
| Was `Tool.outputSchema` advertised for `execute_operation`? | NO (`EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO`) | PR #78 exact catalog capture |
| Can `EXECUTE_OPERATION_SCHEMA_SHA256` be computed over advertised `inputSchema`+`outputSchema`? | NO (`NOT_AVAILABLE`) | PR #77 digest subject rule; PR #78 freeze decision |
| Do frozen OpenAPI operation payloads substitute for the MCP tool output schema? | NO | PR #76 section 6: payload schemas freeze REST business bodies only; they do not define the MCP wrapper or content encoding |

```text
RANK1_MACHINE_READABLE_OUTPUT_AUTHORITY=NO
RANK1_ADVERTISED_OUTPUT_SCHEMA=ABSENT
RANK1_CLOSES_GAP=NO
```

### 4.2 Rank-2 — official provider documentation / SDK / server-source authority

| Question | Finding | Authority basis |
| --- | --- | --- |
| Official HighLevel/LeadConnector MCP doc confirms `execute_operation` exists? | YES | PR #76 section 5 (`STATIC_HIGHLEVEL_EXECUTE_OPERATION_TOOL_CONFIRMED=YES`) |
| Same doc publishes output schema or wrapper field names (`operationId`, `success`, `status`, `payload`, encoding location)? | NO | PR #76 section 5 (`STATIC_HIGHLEVEL_EXECUTE_OPERATION_OUTPUT_SCHEMA_FOUND=NO`) |
| Doc page is immutably versioned / digest-pinnable as durable schema authority? | NO | PR #76: living Docusaurus page; no datestamp, no immutable permalink, no per-page version pin |
| Provider-owned public API docs repo freezes AT-1 operation REST payloads? | YES | PR #76 section 6 (`OPERATION_PAYLOAD_SCHEMAS_FROZEN=YES` at `d9cbcd5…`) |
| Provider-owned public API docs repo defines MCP `execute_operation` result wrapper or encoding? | NO | PR #76 section 6 explicit non-coverage |
| Public SDK or published server source defining the MCP wrapper was identified in bound evidence? | NO | PR #76 / PR #78 evidence set |

```text
RANK2_PROVIDER_DOC_TOOL_CONFIRMED=YES
RANK2_PROVIDER_DOC_OUTPUT_SCHEMA=NO
RANK2_PROVIDER_SDK_OR_SERVER_SOURCE_OUTPUT_AUTHORITY=NO
RANK2_CLOSES_GAP=NO
```

No new network retrieval is performed by this unit. Re-fetching the living
marketplace doc cannot create immutable provider-output authority that PR #76
already recorded as absent. Expanding into unpublished or unofficial sources
is outside planning scope and would not satisfy `SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO`.

### 4.3 Rank-3 — adapter boundary on frozen MCP `CallToolResult` + frozen per-operation business-payload schemas only

This is the critical strategy question: can the adapter eliminate undocumented
HighLevel wrapper assumptions by validating only:

1. frozen JSON-RPC 2.0 response framing;
2. frozen MCP 2025-11-25 `CallToolResult` (`content`, optional
   `structuredContent`, optional `isError`); and
3. frozen per-operation OpenAPI success bodies for the five AT-1 operations
   (with reused `get-opportunity` ordinal)?

| Sub-question | Finding | Rationale |
| --- | --- | --- |
| Does frozen `CallToolResult` define *where* HighLevel places business success data? | NO | MCP permits both required `content` and optional `structuredContent`; tools.mdx says structured results SHOULD also appear as serialized JSON text for compatibility, but does not designate HighLevel's chosen encoding or precedence |
| Does frozen `CallToolResult` define HighLevel success/failure fields beyond `isError`? | NO | Business HTTP status, operation identity echo, and payload envelope are not MCP fields |
| Do frozen operation payload schemas bind to a wire path without a provider encoding contract? | NO | Schemas describe REST bodies (`ContactsByIdSuccessfulResponseDto`, note/opportunity DTOs). Binding them requires a stable path `CallToolResult → business object`. That path is exactly the missing provider contract |
| Can the adapter treat "any JSON object that validates an operation schema" as success? | NO | Ambiguous encoding, multiple content blocks, simultaneous structured+text forms, tool-level soft failures, and non-2xx business bodies cannot be adjudicated without provider-owned success semantics |
| Can current parser assumptions (`content[0]` object with `operationId`/`success`/`status`/`payload`) close the gap? | NO | Explicitly provisional/nonconforming evidence only; `SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO` (PR #75/#76 contract plan) |
| Does eliminating the wrapper layer preserve fail-closed composite validation? | NO | PR #75 requires generic provider-wrapper validation separate from operation-payload validation; dropping the wrapper collapses that separation into inference |

```text
MCP_CALL_TOOL_RESULT_SUFFICIENT=NO
PROVIDER_WRAPPER_REQUIRED=YES
OPERATION_PAYLOAD_SCHEMA_BINDING_STRATEGY=DEFERRED_UNTIL_PROVIDER_OUTPUT_OR_WRAPPER_AUTHORITY
RANK3_CLOSES_GAP=NO
```

Interpretation of `PROVIDER_WRAPPER_REQUIRED=YES`: the composite response
contract still requires a provider-owned output/wrapper layer (advertised
`outputSchema`, immutable provider schema, or equivalent provider-owned
encoding+field authority). It does **not** authorize assuming the undocumented
provisional wrapper fields.

Interpretation of
`OPERATION_PAYLOAD_SCHEMA_BINDING_STRATEGY=DEFERRED_UNTIL_PROVIDER_OUTPUT_OR_WRAPPER_AUTHORITY`:
the five AT-1 operation payload schemas remain frozen and reusable, but they
must not be wire-bound, parser-encoded, or treated as implementation-ready
until a provider-owned path from `CallToolResult` to each business body is
authoritatively established.

### 4.4 Rank-4 — retain unfrozen state

Because ranks 1–3 do not yield authoritative provider-output semantics:

```text
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
RANK4_RETAIN_UNFROZEN=YES
```

## 5. Strategy decision

```text
RESPONSE_CONTRACT_STRATEGY=NO_AUTHORITATIVE_STABLE_STRATEGY_AVAILABLE_RETAIN_COMPOSITE_UNFROZEN
AUTHORITATIVE_SOURCE_IDENTIFIED=NO
PROVIDER_WRAPPER_REQUIRED=YES
MCP_CALL_TOOL_RESULT_SUFFICIENT=NO
OPERATION_PAYLOAD_SCHEMA_BINDING_STRATEGY=DEFERRED_UNTIL_PROVIDER_OUTPUT_OR_WRAPPER_AUTHORITY
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
```

### 5.1 What is already frozen and remains usable

| Layer | Status | Notes |
| --- | --- | --- |
| JSON-RPC 2.0 response/error framing | FROZEN | PR #76 digest-bound snapshot |
| MCP protocol version | FROZEN `2025-11-25` | Pre-grant match observed YES |
| MCP `CallToolResult` schema | FROZEN | PR #76 pinned specification revision |
| `execute_operation` tool presence | OBSERVED | PR #78 catalog |
| `execute_operation` `inputSchema` | CAPTURED (not output authority) | PR #78 descriptor digest |
| AT-1 operation REST payload schemas | FROZEN | PR #76 OpenAPI pin; binding deferred |

### 5.2 What remains blocking

| Gap | Status | Forbidden compensations |
| --- | --- | --- |
| HighLevel `execute_operation` output schema / wrapper fields | ABSENT | Sample responses; fixtures; parser behavior; one-off live `execute_operation` observation used as schema authority |
| Content-encoding location (`structuredContent` vs typed text vs other) | UNKNOWN | Preferring one MCP encoding without provider designation |
| Composite contract freeze | NOT READY | Implementation of parser/session/runtime against provisional shapes |
| Grant009-class live business execution | NOT AUTHORIZABLE from this unit | Drafting or executing Grant009 |

### 5.3 Implementation authorization consequence

```text
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
PARSER_IMPLEMENTATION_IN_SCOPE=NO
SESSION_IMPLEMENTATION_IN_SCOPE=NO
RUNTIME_CONTRACT_FREEZE_IN_SCOPE=NO
```

A future implementation unit may not encode provisional wrapper fields, may not
bind operation payload schemas to an inferred wire path, and may not claim
composite freeze readiness from this gap unit. Any later path that obtains
provider-owned output authority must be a new authorized planning and/or
observation unit; it is not opened here.

## 6. Explicit non-actions

This unit performed none of the following:

```text
MCP_INITIALIZE_CALLS=0
MCP_TOOLS_LIST_CALLS=0
MCP_EXECUTE_OPERATION_CALLS=0
TOOLS_CALL_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
GRANT009_DRAFTS=0
GRANT009_EXECUTIONS=0
RAW_REST_CALLS=0
IAM_SECRET_DEPLOY_CHANGES=0
PARSER_OR_SESSION_CODE_CHANGES=0
NETWORK_CALLS_TO_LIVE_GHL_MCP=0
```

## 7. Required result field block

```text
RESPONSE_CONTRACT_STRATEGY=NO_AUTHORITATIVE_STABLE_STRATEGY_AVAILABLE_RETAIN_COMPOSITE_UNFROZEN
AUTHORITATIVE_SOURCE_IDENTIFIED=NO
PROVIDER_WRAPPER_REQUIRED=YES
MCP_CALL_TOOL_RESULT_SUFFICIENT=NO
OPERATION_PAYLOAD_SCHEMA_BINDING_STRATEGY=DEFERRED_UNTIL_PROVIDER_OUTPUT_OR_WRAPPER_AUTHORITY
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
NEXT=NW008_AT1_PROVIDER_RESPONSE_CONTRACT_GAP_HUMAN_DISPOSITION
```

## 8. Next decision

```text
NEXT=NW008_AT1_PROVIDER_RESPONSE_CONTRACT_GAP_HUMAN_DISPOSITION
```

Human review of this planning-only gap unit is the only authorized next step
from this artifact. This unit does **not**:

1. draft or execute Grant009;
2. authorize another live MCP observation or any `execute_operation` call;
3. authorize parser/session/runtime implementation;
4. reopen frozen JSON-RPC, MCP, or operation-payload layers;
5. invent provider wrapper fields or promote samples to authority.

A later unit may be warranted only after human disposition, and only if a new
provider-owned authority path becomes available (for example provider-published
output schema, immutable server/SDK source, or a separately authorized
observation that captures an actual advertised `outputSchema` without using
sample business responses as schema authority). No such unit is created here.

## 9. Validation and PR

This PR is `planning_only`. Its writable scope is exactly:

```text
proof/nw008/nw-008-at1-provider-response-contract-gap-001.md
```

Provenance:

```text
PLAN_BASE_SHA=781f8ce90c7b63fc8e23eec62dda7544bda8d143
PLAN_BASE_REF=origin/main
PLAN_BRANCH=plan/nw008-at1-provider-response-contract-gap-001
```

Local validation expected on the working tree before push:

1. `git diff --check` — clean;
2. exactly one changed path, equal to the path above;
3. `PYTHONPATH=src python scripts/verify_phase1_deterministic.py` — all checks PASS;
4. zero GHL/MCP business or control-plane traffic.

```text
LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
PROTOCOL_VERSION_MATCH=YES
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=NO
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO

RESPONSE_CONTRACT_STRATEGY=NO_AUTHORITATIVE_STABLE_STRATEGY_AVAILABLE_RETAIN_COMPOSITE_UNFROZEN
AUTHORITATIVE_SOURCE_IDENTIFIED=NO
PROVIDER_WRAPPER_REQUIRED=YES
MCP_CALL_TOOL_RESULT_SUFFICIENT=NO
OPERATION_PAYLOAD_SCHEMA_BINDING_STRATEGY=DEFERRED_UNTIL_PROVIDER_OUTPUT_OR_WRAPPER_AUTHORITY
NEXT=NW008_AT1_PROVIDER_RESPONSE_CONTRACT_GAP_HUMAN_DISPOSITION
STOP_CODE=NW008_AT1_PROVIDER_RESPONSE_CONTRACT_GAP_READY_FOR_REVIEW
```
