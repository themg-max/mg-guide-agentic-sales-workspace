# NW-008 AT-1 -- Live Transport and Evidence Remediation Plan

```text
REMEDIATION_ID=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_001
REMEDIATION_PHASE=PLANNING

SOURCE_PR69_MERGE_SHA=17a78dbd3bcc7b73904df3eb99996962deaaa3e7
SOURCE_RECONCILIATION_SHA=04dca73fcc9862c3e7fa5a88b2fd8aabd0c7312d

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_AUTHORIZED=NO
```

## 1. Planning boundary

This artifact defines a bounded future remediation for the AT-1 live transport
and evidence-capture failures established by Result 008 reconciliation. It is a
plan only. It does not implement, activate, exercise, or authorize the future
runtime.

```text
CLASSIFICATION=planning_only
RUNTIME_IMPLEMENTATION_IN_SCOPE=NO
RUNTIME_MUTATION_IN_THIS_PR=NO
LIVE_GHL_CALLS_IN_THIS_PR=0
MCP_INITIALIZE_OR_PROBE_CALLS_IN_THIS_PR=0
NETWORK_TESTS_IN_SCOPE=NO
GRANT009_PREPARATION_IN_SCOPE=NO
NEW_GHL_AUTHORITY=NO
GRANT_008_RETRY_AUTHORIZED=NO
```

The consumed Grant 008 attempt remains historical and non-repeatable. Nothing
in this plan repairs its missing evidence, changes its reconciliation, or
converts it into authority for another attempt. Any future implementation,
review, private binding, readiness check, grant preparation, or live execution
must occur in separately authorized units.

## 2. Main-reachable source state

| Required source | Main-reachable state |
| --- | --- |
| PR #69 head `a67f32da287ef53e6995f9db9a510c179b0947b9` | YES |
| PR #69 merge `17a78dbd3bcc7b73904df3eb99996962deaaa3e7` | YES |
| `proof/nw008/nw-008-at1-completion-decision.md` | PRESENT |
| `proof/nw008/nw-008-at1-completion-decision-reviewer-disposition.md` | PRESENT |
| Completion decision | `AT1_COMPLETE=NO` |
| Grant state | `GRANT_008_STATE=CONSUMED` |

The controlling source remains reconciliation commit
`04dca73fcc9862c3e7fa5a88b2fd8aabd0c7312d`. Its material remediation inputs
are:

1. the live attempt bypassed the reviewed bounded executor and serializer with
   an ad-hoc inline runner;
2. actual request aliases diverged from the reviewed serializer wire shape;
3. HTTP/JSON-RPC continuation was treated as business success without parsing
   MCP `isError` or nested operation success;
4. the created note ID was absent, but the runner still issued get-note;
5. initial stage, note identity/content, and final stage were not compared;
6. outbound request and inbound response envelopes were not retained;
7. result flags were assigned rather than computed from response evidence; and
8. protocol calls and business calls were conflated while retries and
   post-failure probes occurred in the same process scope, with no durable
   grant/run claim that would survive process restart.

## 3. Immutable remediation contracts

### Runtime composition

```text
USE_BOUNDED_AT1_EXECUTOR=REQUIRED
USE_AT1_LIVE_TRANSPORT_SERIALIZER=REQUIRED
AD_HOC_INLINE_LIVE_RUNNER=FORBIDDEN
```

The future live path must enter through `BoundedAt1GhlExecutor`. It must inject
a bounded live transport adapter at the existing transport seam and must use
`At1LiveTransportSerializer` for every business request. A script may perform
input loading and invoke the bounded entry point, but it must not construct
operation envelopes, interpret operation success, issue retries, or assign
result flags.

### Exact wire shape

```text
EXACT_SERIALIZER_WIRE_SHAPE_REQUIRED=YES
ALIAS_FIELD_SUBSTITUTION_ALLOWED=NO
```

The future adapter must dispatch the serializer output without adding,
renaming, or normalizing operation fields. The exact business wire contract is:

| Ordinal | Operation | Exact serialized fields |
| --- | --- | --- |
| 1 | `get-contact` | `operationId=get-contact`; `params.path.contactId` |
| 2 | `get-opportunity` | `operationId=get-opportunity`; `params.path.id` |
| 3 | `create-note` | `operationId=create-note`; `params.path.contactId`; `params.body.body`; top-level `idempotencyKey` |
| 4 | `get-note` | `operationId=get-note`; `params.path.contactId`; `params.path.id` |
| 5 | `update-opportunity` | `operationId=update-opportunity`; `params.path.id`; `params.body.pipelineStageId`; top-level `idempotencyKey` |
| 6 | `get-opportunity` | `operationId=get-opportunity`; `params.path.id` |

All six calls retain the frozen outer call seam:

```text
name=execute_operation
arguments=<exact At1LiveTransportSerializer output>
```

Fields used by Result 008 but absent from this table are forbidden, including
`path.locationId`, `path.opportunityId`, `path.noteId`, `body.stageId`, and
`body.content_or_fingerprint`. No adapter-side alias fallback is allowed.

### Layered MCP success

```text
JSONRPC_ERROR_PARSE_REQUIRED=YES
MCP_IS_ERROR_PARSE_REQUIRED=YES
NESTED_OPERATION_SUCCESS_PARSE_REQUIRED=YES
```

HTTP success is transport evidence only. A future response may reach the
executor as an operation success only after all of these checks pass in order:

1. the response envelope is captured privately before semantic reduction;
2. the response is a valid JSON-RPC response for the matching request;
3. no top-level JSON-RPC `error` is present;
4. the MCP result is structurally valid and `isError` is explicitly false;
5. MCP content is decoded using the reviewed response schema;
6. nested operation success/status explicitly represents success; and
7. the operation-specific payload satisfies its required identity and value
   schema.

A missing, malformed, contradictory, or unknown value at any layer fails
closed. HTTP 200, the absence of a top-level error, or a truthy envelope cannot
individually establish business success. Parser failure is terminal and cannot
trigger a retry or alternate interpretation.

## 4. Semantic verification state machine

```text
EXPECTED_INITIAL_STAGE_COMPARE_REQUIRED=YES
CREATED_NOTE_ID_REQUIRED_BEFORE_GET_NOTE=YES
NOTE_ID_COMPARE_REQUIRED=YES
NOTE_CONTENT_COMPARE_REQUIRED=YES
FINAL_STAGE_COMPARE_REQUIRED=YES
```

The existing six-operation order remains unchanged. Future implementation must
apply the following gates:

1. **Initial opportunity gate:** normalize OP2 only after layered MCP success,
   then compare the returned opportunity identity and stage to the authorized
   binding. A stage mismatch or unverifiable stage stops before either write.
2. **Created note gate:** normalize OP3 only after layered MCP success. Extract
   a non-empty created note ID from the reviewed response field. Missing or
   malformed identity stops immediately; OP4 is not constructed or dispatched.
3. **Note readback gate:** construct OP4 only with the OP3-created note ID.
   Require layered MCP success, exact returned note-ID equality, and exact
   authorized note-content equality. Any mismatch stops and preserves the
   private evidence of the possible partial effect.
4. **Final stage gate:** after the one permitted stage-write attempt, require
   layered MCP success for OP6 and exact equality between the returned final
   stage and the authorized final stage. Any mismatch stops and preserves
   private evidence.

No comparison may be represented by a placeholder print, unconditional flag,
or inference from control-flow continuation.

## 5. Evidence architecture

```text
PRIVATE_REQUEST_ENVELOPE_CAPTURE_REQUIRED=YES
PRIVATE_RESPONSE_ENVELOPE_CAPTURE_REQUIRED=YES
REQUEST_CAPTURE_BEFORE_DISPATCH_REQUIRED=YES
RESPONSE_CAPTURE_BEFORE_PARSE_REQUIRED=YES
REQUEST_RESPONSE_CORRELATION_REQUIRED=YES
REQUEST_RESPONSE_DIGEST_BINDING_REQUIRED=YES
SANITIZED_PUBLIC_PROJECTION_REQUIRED=YES
RESULT_FLAGS_MUST_BE_COMPUTED=YES
HARDCODED_SUCCESS_FLAGS_FORBIDDEN=YES
```

### Capture ordering

Every future business call must follow this exact order:

```text
serializer output
-> exact schema validation
-> private request capture
-> durable business-attempt record
-> dispatch
-> private response capture
-> layered parse
-> semantic comparison
-> sanitized projection/result
```

Hard fail-closed rules:

- if private request capture fails, do not dispatch;
- if private response capture fails, stop before any later operation;
- no request capture means no dispatch;
- no response capture means no parse, no semantic comparison, and no later
  business ordinal.

### Private request and response capture

The future adapter must durably capture the exact outbound serialized MCP
request envelope in a private, access-controlled execution package after
serializer schema validation and before dispatch. After transport returns, it
must durably capture the complete inbound MCP response envelope before the
envelope is parsed or discarded.

Each paired private record must bind:

- remediation implementation version and future grant/run identity;
- process identity and monotonically increasing ledger ordinal;
- JSON-RPC request ID and AT-1 operation ordinal;
- exact outbound serialized request envelope;
- transport outcome and complete inbound MCP response envelope;
- capture timestamps for request and response;
- request digest and response digest; and
- correlation identifiers that bind the request/response pair and allow the
  sanitized projection to bind to both private digests.

The private package may contain private IDs, note content, nested response
bodies, idempotency keys, and error details. It must not be committed to the
public repository or printed to public logs. Request-capture failure forbids
dispatch of that ordinal. Response-capture failure is terminal for the run:
later business calls are not authorized when the current call's response
evidence cannot be retained.

### Sanitized public projection

The public projection must be derived from captured request/response pairs
through an explicit allowlist. It may include operation ordinals, parser
outcomes, computed predicates, counters, failure codes, and non-reversible
private request/response digests. It must exclude authorization headers,
tokens, idempotency keys, raw private IDs, note content, full request bodies,
and unreviewed response text. Sanitization must be tested against synthetic
sentinel values.

### Computed result model

Result flags must be derived from immutable parser and comparison records.
Callers must not be able to pass values such as
`EXPECTED_INITIAL_STAGE_VERIFIED`, `NOTE_READBACK_VERIFIED`,
`FINAL_STAGE_READBACK_VERIFIED`, write-success counters, or `AT1_COMPLETE`.
The result constructor must compute them from:

- successful layered parsing for the corresponding operation;
- exact identity/value comparisons;
- process-scoped and grant/run-scoped protocol and business ledgers;
- durable consumed attempt state;
- consumed write-attempt budgets; and
- terminal-state evidence.

`AT1_COMPLETE=YES` is possible only when every required predicate is computed
YES and the ledgers prove the exact authorized call profile. Any NO or UNKNOWN
required predicate computes `AT1_COMPLETE=NO`.

## 6. Protocol, business, and no-retry ledgers

```text
MCP_PROTOCOL_CALL_LEDGER_REQUIRED=YES
GHL_BUSINESS_CALL_LEDGER_REQUIRED=YES
GRANT_SCOPE_NO_RETRY_REQUIRED=YES
PROCESS_SCOPE_NO_RETRY_REQUIRED=YES
DURABLE_EXECUTION_CLAIM_REQUIRED=YES
DURABLE_EXECUTION_CLAIM_ATOMIC=YES
PROCESS_RESTART_MUST_NOT_RESET_ATTEMPT_HISTORY=YES
CONCURRENT_EXECUTION_CLAIM_REJECTED=YES
PRE_GRANT_CONTROL_PLANE_PROBING_REQUIRED_IF_NEEDED=YES
PRE_GRANT_CONTROL_PLANE_READINESS_REQUIRES_SEPARATE_AUTHORITY=YES
SESSION_IDENTITY_BOUND_TO_FUTURE_GRANT=YES
POST_GRANT_PROBING_ALLOWED=NO
```

Two append-only ledgers are required:

| Ledger | Included calls | Excluded calls |
| --- | --- | --- |
| MCP protocol | initialize, capability negotiation, health/control-plane probes | `execute_operation` business calls |
| GHL business | each attempted `execute_operation`, recorded after private request capture and immediately before dispatch | initialize, negotiation, health/probe traffic |

### Process-scope and grant/run-scope no-retry

The ledgers share one process-scoped execution guard. Creating another adapter,
executor, or wrapper in the same process must not reset attempt history. Each
authorized business ordinal has one dispatch opportunity. A transport,
protocol, parser, capture, or semantic failure consumes that ordinal and
terminates the run; the same business operation cannot be attempted again.

In addition, no-retry protection must be durable and grant/run-scoped:

- a durable execution claim is keyed to the future grant/run identity;
- claim acquisition is atomic and permits exactly one owner;
- concurrent duplicate claim attempts for the same grant/run are rejected
  before transport;
- consumed ordinals and attempt history are persisted with the claim;
- a fresh process or reconstructed executor using the same grant/run must load
  the consumed attempt state and refuse duplicate transport locally;
- process restart must not reset attempt history.

### Control-plane readiness and session binding

Any control-plane initialization or probing needed to establish readiness must
finish before a future live grant becomes active, must be recorded in the
protocol ledger, and requires separate readiness authority. Once the future
grant is active, the already-established session identity is bound to that
grant. Initialize, reprobe, capability rediscovery, endpoint fallback, and
session repair are forbidden after grant activation. The bound session may
carry only the exact bounded business sequence. If it is unusable, execution
stops without a business retry.

The sanitized result must report protocol and business counts independently.
Protocol traffic must never increment or satisfy the six-call GHL business
budget.

## 7. Offline deterministic test plan

All remediation tests use committed synthetic fixtures and an in-memory
transport. Socket creation, HTTP clients, MCP servers, GHL credentials, and
external endpoints are prohibited in this test lane.

```text
OFFLINE_DETERMINISTIC_FIXTURES_REQUIRED=YES
NETWORK_TESTS=0
LIVE_GHL_TEST_CALLS=0
PRIVATE_VALUES_IN_FIXTURES=NO
```

| ID | Deterministic fixture | Required assertion |
| --- | --- | --- |
| B24 | Exact serializer contract | All six business calls equal the serializer's reviewed outer seam and exact path/body/idempotency shape; extra and alias fields are absent. |
| B25 | Nested MCP failure under HTTP 200 | HTTP 200 with JSON-RPC success but nested operation failure computes operation failure, stops the executor, and does not increment write-success state. |
| B26 | `isError=true` fail closed | MCP `isError=true` is terminal even when HTTP and JSON-RPC layers succeed; no later call is dispatched. |
| B27 | Missing note ID blocks get-note | Successful-looking OP3 without a valid created note ID computes failure; OP4 is absent from the business ledger and transport log. |
| B28 | Wrong initial stage blocks write | OP2 returns a stage different from the authorized expected initial stage; both write-attempt counters and all write transport calls remain zero. |
| B29 | Wrong note content fails readback | OP4 returns the created note ID with mismatched content; note readback is false, stage write is not dispatched, and partial-effect evidence is preserved. |
| B30 | Wrong final stage fails readback | OP6 returns a stage different from the authorized final stage; final-stage verification and AT-1 completion compute false while the consumed stage attempt is preserved. |
| B31 | Protocol vs business call ledger separation | Synthetic initialize/probe records appear only in the protocol ledger; the six modeled operations appear only in the business ledger; totals cannot be conflated. |
| B32 | Second business attempt rejected | After the first dispatch attempt for an ordinal fails, a second attempt in the same process is refused before transport, including when a new adapter/executor wrapper is constructed. |
| B33 | Post-grant initialize/probe rejected | After synthetic grant activation, initialize and probe requests are locally refused and absent from the transport log; no fallback session is created. |
| B34 | Hard-coded result flag impossible by construction | Public result creation accepts evidence records, not success booleans; attempts to inject/override success flags are rejected, and contradictory fixture evidence computes failure. |
| B35 | Private response capture to sanitized projection | A synthetic envelope with sentinel token, IDs, idempotency key, and note content is retained in the private sink; the public projection binds by digest and contains none of the sentinels. |
| B36 | Grant/run retry survives process restart | After a synthetic ordinal is consumed under grant/run identity G, a new process that loads the same durable claim cannot redispatch that ordinal; refusal occurs before transport and the business ledger remains unchanged. |
| B37 | Concurrent execution claim rejected | Atomic durable claim acquisition permits exactly one owner for grant/run identity G; a concurrent second owner is rejected before transport and creates zero business dispatch records. |
| B38 | Outbound-request/inbound-response evidence pair | Exact serializer request is captured before dispatch; exact synthetic response is captured before parse; request id + operation ordinal + request/response digests correlate the pair; public projection binds both digests and contains no private sentinels. |

Each fixture must also assert terminal call count, both ledgers, write-attempt and
write-success counters, private request/response capture counts, durable claim
state, sanitized projection, and computed completion state. There are no
network-marked variants of B24-B38.

## 8. Candidate future implementation paths

The following paths are candidates for a separately authorized implementation
unit. They are identified here but are not edited by this planning PR:

```text
src/integrations/ghl/bounded_at1_executor.py
src/integrations/ghl/at1_live_transport_serializer.py
src/integrations/ghl/<new bounded live transport adapter>

tests/integrations/ghl/<AT1 remediation tests>
fixtures/ghl/<AT1 remediation fixtures>
```

Expected responsibilities:

- `bounded_at1_executor.py`: preserve the six-operation state machine and own
  semantic gates, terminal behavior, and computed result assembly;
- `at1_live_transport_serializer.py`: remain the only business wire-shape
  authority;
- new bounded adapter: own established-session dispatch, layered MCP parsing,
  process-scoped and grant/run-scoped durable no-retry claims, private
  request/response envelope capture, and sanitized projection;
- remediation tests/fixtures: prove B24-B38 offline with synthetic values.

The implementation unit must decide exact adapter and fixture filenames through
normal repository review. It must not broaden the operation surface, add raw
REST fallback, add search/list/pagination, add automatic retry, or implement
compensating mutation.

## 9. Future implementation acceptance gates

A future remediation implementation is reviewable only when all of the
following are demonstrated without live traffic:

1. B24-B38 pass deterministically and offline.
2. Existing bounded executor and GHL integration tests remain green.
3. Phase 1 deterministic validation passes at the exact implementation head.
4. The reviewed serializer is the only source of business wire envelopes.
5. All MCP success layers fail closed on missing or negative evidence.
6. Semantic comparison gates prevent later calls exactly as specified.
7. Exact outbound wire requests are privately recoverable before dispatch.
8. Exact inbound responses are privately recoverable before parse.
9. Sanitized proof binds to both request and response digests and is
   allowlist-only.
10. No request capture means no dispatch; no response capture stops the run
    before any later operation.
11. Result flags cannot be supplied or overridden by an execution script.
12. Protocol and business ledgers reconcile independently.
13. Process-scoped no-retry state survives wrapper reconstruction.
14. Durable no-retry authority is grant/run-scoped and survives process restart.
15. Concurrent duplicate grant/run claims fail closed before transport.
16. No network test, GHL call, private binding, Grant 009 preparation, or live
    authority is included.

Passing these gates would establish implementation readiness only. It would not
authorize private binding, Grant 009 preparation, or live execution.

## 10. Planning-unit non-actions

```text
DID_NOT_EDIT_RUNTIME=YES
DID_NOT_EDIT_TESTS=YES
DID_NOT_EDIT_FIXTURES=YES
DID_NOT_CALL_GHL=YES
DID_NOT_MCP_INITIALIZE=YES
DID_NOT_EXECUTE_OPERATION=YES
DID_NOT_PROBE_CONTROL_PLANE=YES
DID_NOT_RETRY=YES
DID_NOT_COMPENSATE=YES
DID_NOT_PREPARE_GRANT009=YES
DID_NOT_AUTHORIZE_GRANT009=YES
ADDITIONAL_GHL_CALLS_EXECUTED=0
ADDITIONAL_MUTATION_CALLS_EXECUTED=0
```

## 11. STOP

```text
STOP_CODE=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_PLAN_HARDENED_FOR_REVIEW
REMEDIATION_ID=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_001
REMEDIATION_PHASE=PLANNING
CLASSIFICATION=planning_only
GRANT_SCOPE_NO_RETRY_REQUIRED=YES
PROCESS_RESTART_MUST_NOT_RESET_ATTEMPT_HISTORY=YES
PRIVATE_REQUEST_ENVELOPE_CAPTURE_REQUIRED=YES
REQUEST_CAPTURE_BEFORE_DISPATCH_REQUIRED=YES
GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO
LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_AUTHORIZED=NO
NEXT=FINAL_PR70_REVIEWER_DISPOSITION
```
