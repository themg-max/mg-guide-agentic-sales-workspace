# NW-008 AT-1 Established Session and Response Contract Closure 001

## 1. Closure identity and offline boundary

```text
ARTIFACT_ID=NW008_AT1_ESTABLISHED_SESSION_AND_RESPONSE_CONTRACT_CLOSURE_001
ARTIFACT_PATH=docs/nw008/nw-008-at1-established-session-and-response-contract-closure-001.md
PR_CLASS=planning_only
OWNER=VS_CODE_ORCHESTRATOR_GOVERNANCE_AND_ARCHITECTURE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=f1d09f597dff7623fa44d70ccdf706287a384d34
PLAN_BRANCH=plan/nw008-at1-established-session-and-response-contract-closure-001
BRANCH_IS_MAIN=NO
LANE_A_EXECUTION_PROOF_PR=259

PLANNING_DESIGN_CLOSURE_ONLY=YES
IMPLEMENTATION_IN_SCOPE=NO
SESSION_ESTABLISHMENT_IN_SCOPE=NO
ENDPOINT_SELECTION_IN_SCOPE=NO
PROVIDER_CONNECTIVITY_IN_SCOPE=NO
CAPABILITY_DISCOVERY_IN_SCOPE=NO
GRANT_CREATION_IN_SCOPE=NO

LIVE_GHL_CALLS=0
MCP_NETWORK_CALLS=0
CRM_MUTATIONS=0
```

This unit closes the architecture decision needed after the stopped Grant 001
attempt. It identifies one proper future established-session seam and the
source-capture gates for its response contract. It does not implement that seam,
select an endpoint, create a client profile, initialize or probe MCP, call
HighLevel, or prepare another grant.

Merging or reviewing this closure confers no implementation, source-capture,
control-plane, grant-preparation, or live-execution authority.

## 2. Grant 001 disposition

The normalized execution proof remains the authority for the historical attempt:
the private package and schema-v2 store checks passed, but no established usable
session was available. Execution stopped before claim acquisition and before any
GHL business call.

```text
GRANT_ID=NW008_FRESH_ONE_SHOT_GHL_GRANT_001
EXECUTION_PHASE_REACHED=PRECLAIM_SESSION_GATE
E2E_EXECUTION_OCCURRED=NO

EXECUTION=STOPPED_PRE_CLAIM
FAILURE_CLASS=ESTABLISHED_SESSION_UNAVAILABLE
BUSINESS_EFFECT_TRUTH=NO

GRANT_CLAIM_ACQUIRED=NO
GRANT_CONSUMED=NO

GRANT001_TERMINAL=YES
GRANT001_REUSABLE=NO

LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
TOTAL_GHL_BUSINESS_CALLS=0
CRM_MUTATIONS=0

INDEPENDENT_POST_RUN_RECONCILIATION=NOT_APPLICABLE_ZERO_BUSINESS_CALLS

NEW_EXECUTION_ATTEMPT_AUTHORIZED=NO
RETRY_AUTHORIZED=NO
```

`GRANT001_TERMINAL=YES` is a governance closure of the stopped grant, not a
claim that its execution-store claim or business budget was consumed. The
historical `GRANT_CONSUMED=NO` fact remains unchanged. Terminal closure makes
the grant non-reusable and bars retry or reinstantiation.

## 3. Concrete future established-session seam

Exactly one future concrete component is identified:

```text
COMPONENT=At1EstablishedMcpSession
ROLE=SEALED_BUSINESS_ONLY_MCP_SESSION

ESTABLISHED_SESSION_IMPLEMENTATION_CURRENT_STATE=NOT_IMPLEMENTED
PROPER_SESSION_SEAM_IDENTIFIED=YES
SESSION_SEAM_NAME=At1EstablishedMcpSession
```

Its complete post-seal business interface is:

```text
execute_operation(request) -> provider response
```

The component must pass the adapter-supplied request to the pre-established
session without adding, removing, renaming, normalizing, or reconstructing
fields. It must return the complete provider response without interpretation or
shape conversion. Its stable identity must be non-secret and suitable for
commitment in a private package and exact binding by a later grant.

```text
WRAP_PREESTABLISHED_MCP_SESSION=YES
PRESERVE_EXACT_ADAPTER_REQUEST=YES
STABLE_NONSECRET_SESSION_IDENTITY=REQUIRED

POST_SEAL_INITIALIZE=NO
POST_SEAL_PROBE=NO
POST_SEAL_SEARCH_OPERATIONS=NO
POST_SEAL_DESCRIBE_OPERATION=NO
POST_SEAL_RECONNECT=NO
POST_SEAL_REPAIR=NO
POST_SEAL_RETRY=NO
ENDPOINT_FALLBACK=NO
RAW_REST_FALLBACK=NO
```

Sealing is a one-way transition. An unusable, expired, disconnected, mismatched,
or otherwise invalid session must fail closed before or during the later run.
It must not reopen control-plane behavior or select another endpoint.

### 3.1 Session seam response abstraction

The current adapter protocol expects a full JSON-RPC response envelope at the
session boundary. That is an adapter-side expectation only. It does not freeze
the future session seam response level, HighLevel result encoding, or parser
normalization requirement.

```text
CURRENT_ADAPTER_EXPECTED_RESPONSE_LEVEL=RAW_JSONRPC_RESPONSE_ENVELOPE

SESSION_SEAM_RESPONSE_LEVEL=
SESSION_SEAM_RESPONSE_LEVEL_FROZEN=NO

WIRE_REQUEST_ID_PRESERVATION_REQUIRED=YES
RAW_RESPONSE_CAPTURE_REQUIRED=YES
RESPONSE_RECONSTRUCTION_ALLOWED=NO

CURRENT_ADAPTER_PROVIDER_CONTENT_COMPATIBILITY=UNPROVEN

HIGHLEVEL_RESULT_ENCODING=
PARSER_NORMALIZATION_REQUIRED=UNKNOWN

RESPONSE_CONTRACT_FREEZE_BEFORE_SESSION_IMPLEMENTATION=YES
```

Blank `SESSION_SEAM_RESPONSE_LEVEL` and `HIGHLEVEL_RESULT_ENCODING` are unknown,
not defaults. This unit does not infer them from fixtures, parser behavior, or
the current adapter expectation. Future readiness may pass only after all of:

```text
SESSION_SEAM_RESPONSE_LEVEL_FROZEN=YES
PROVIDER_RESULT_ENCODING_FROZEN=YES
CURRENT_ADAPTER_COMPATIBLE_WITH_FROZEN_CONTRACT=YES
```

are proven by a later source-capture/contract freeze. Until then, session
implementation remains blocked.

## 4. Required composition and forbidden bypasses

The only allowed future composition is:

```text
sealed At1EstablishedMcpSession
  -> At1LiveTransportAdapter
  -> At1LiveTransportSerializer
  -> BoundedAt1GhlExecutor
```

This is the required component set and exclusive runtime seam. Business requests
remain constructed only by `At1LiveTransportSerializer`, validated and captured
by `At1LiveTransportAdapter`, and dispatched through the sealed
`At1EstablishedMcpSession`. The composition root may inject reviewed
dependencies and invoke `BoundedAt1GhlExecutor`; it may not construct or
dispatch an operation itself.

```text
COPILOT_TOOL_REGISTRY_AS_RUNTIME_SEAM=NO
DIRECT_EXECUTOR_TO_MCP=NO
DIRECT_COMPOSITION_ROOT_TO_EXECUTE_OPERATION=NO
SERIALIZER_BYPASS=NO
ALTERNATE_LIVE_RUNNER=NO
```

The Copilot tool registry observed by an operator is not a production runtime
dependency, session factory, capability authority, or substitute for the sealed
component.

## 5. Provider and composite response-contract closure

Current fixtures, parser behavior, tests, sample responses, and the stopped
operator attempt are implementation evidence only. They are not independent
authority for the MCP protocol shape, HighLevel provider wrapper, wrapper
location, or operation payload schemas.

The exact accepted response must eventually be one composite, versioned,
digest-bound contract covering:

1. the selected MCP protocol and authoritative schema revision;
2. the selected HighLevel endpoint profile;
3. authoritative `execute_operation` availability and input/output schema;
4. the exact HighLevel provider-wrapper encoding location and wrapper schema;
5. each bounded operation payload schema; and
6. the parser behavior that validates every layer without fallback.

The required future source-capture/contract record is:

```text
SUPPORTED_MCP_PROTOCOL_VERSION=
MCP_SCHEMA_AUTHORITY_REVISION=
MCP_SCHEMA_SHA256=

HIGHLEVEL_ENDPOINT_PROFILE=
HIGHLEVEL_EXECUTE_OPERATION_AUTHORITY=
HIGHLEVEL_EXECUTE_OPERATION_SCHEMA_VERSION=
HIGHLEVEL_EXECUTE_OPERATION_SCHEMA_SHA256=

HIGHLEVEL_PROVIDER_WRAPPER_LOCATION=
HIGHLEVEL_PROVIDER_WRAPPER_SCHEMA_FROZEN=NO

OPERATION_PAYLOAD_SCHEMAS_FROZEN=NO

COMPOSITE_RESPONSE_CONTRACT_VERSION=
COMPOSITE_RESPONSE_CONTRACT_SHA256=
```

Blank values are deliberately unknown and unfrozen, not wildcards. No runtime
or grant may choose them dynamically. Readiness remains blocked until every
blank has one exact evidence-backed value, both freeze fields are `YES`, and
the resulting composite contract has an immutable version and SHA-256 digest.

```text
CURRENT_FIXTURE_IS_PROVIDER_AUTHORITY=NO
CURRENT_PARSER_IS_PROVIDER_AUTHORITY=NO
SAMPLE_RESPONSE_IS_PROVIDER_AUTHORITY=NO

MCP_RESPONSE_CONTRACT_CURRENT_STATE=NOT_FROZEN
PREGRANT_SESSION_ESTABLISHMENT_CURRENT_STATE=NOT_FROZEN

ENDPOINT_PROFILE_READY=NO
CLIENT_PROFILE_READY=NO
PROVIDER_RESPONSE_CONTRACT_READY=NO
```

## 6. Endpoint candidates and future selection gate

The following are locator candidates only:

```text
GENERIC_MCP_ENDPOINT_CANDIDATE=https://services.leadconnectorhq.com/mcp/
PER_CLIENT_V2_CANDIDATE=https://services.leadconnectorhq.com/mcp/anthropic/v2

SELECTED_ENDPOINT_PROFILE=
ENDPOINT_SELECTED_IN_THIS_UNIT=NO
```

Neither candidate is selected, preferred, validated, or claimed compatible by
this offline unit. A separately authorized pre-grant control-plane unit may
select exactly one endpoint profile only after source and capability evidence
proves all of:

```text
CLIENT_IDENTITY_SUPPORTED=YES
AUTHENTICATION_READY=YES
NEGOTIATED_MCP_VERSION_MATCH=YES
EXECUTE_OPERATION_PRESENT=YES
REQUIRED_OPERATION_SET_AVAILABLE=YES
PROVIDER_RESPONSE_CONTRACT_MATCH=YES
```

Failure or uncertainty in any predicate leaves the endpoint and client profile
unready. The future unit may not fall back from one candidate to the other.

## 7. Pre-grant establishment, sealing, and ledger boundary

A future separately authorized control-plane unit must establish and validate
the session before any business grant becomes active. It must capture every
initialization, negotiation, capability, and schema-validation action in a
pre-grant protocol ledger, prove all endpoint-selection predicates, commit the
stable non-secret session identity, and then irreversibly seal the component.

The sealed component may carry only the exact bounded `execute_operation`
business sequence. Control-plane calls must not appear in the business-call
ledger or consume a GHL business ordinal. After sealing, capability discovery,
schema discovery, operation search/description, initialization, probing,
reconnection, repair, retry, and endpoint fallback are forbidden.

```text
PREGRANT_CONTROL_PLANE_AUTHORITY_REQUIRED=SEPARATE
PREGRANT_PROTOCOL_LEDGER_REQUIRED=YES
PREGRANT_PROTOCOL_LEDGER_FINAL_BEFORE_SEAL=YES
SESSION_SEALED_BEFORE_GRANT_ACTIVATION=YES
SESSION_IDENTITY_BINDING_REQUIRED=YES

POST_SEAL_BUSINESS_ONLY=YES
POST_SEAL_CONTROL_PLANE_CALLS=0
```

## 8. Future private-package and grant binding

The next private execution package must bind these exact values:

```text
SEALED_SESSION_IDENTITY_COMMITMENT
SELECTED_ENDPOINT_PROFILE_ID
SUPPORTED_MCP_PROTOCOL_VERSION
COMPOSITE_RESPONSE_CONTRACT_VERSION
COMPOSITE_RESPONSE_CONTRACT_SHA256
PREGRANT_PROTOCOL_LEDGER_DIGEST
```

Every value must resolve to one exact frozen value before package review. A
future grant must bind the same six values exactly. Any absence, mismatch,
expiry, replacement session, altered protocol ledger, changed endpoint profile,
or changed response contract blocks claim acquisition and requires a separate
governance decision; it does not authorize repair or retry.

```text
NEXT_PRIVATE_PACKAGE_BINDING_REQUIRED=YES
FUTURE_GRANT_EXACT_BINDING_REQUIRED=YES
RUNTIME_SUBSTITUTION_ALLOWED=NO
NEW_GRANT_PREPARATION_READY=NO
```

## 9. Next planning unit after this closure merges

The next planning unit is source-capture only:

```text
ARTIFACT_ID=NW008_AT1_HIGHLEVEL_MCP_PROVIDER_CONTRACT_SOURCE_CAPTURE_001
```

Without CRM mutation, and without implementing `At1EstablishedMcpSession`, it
must determine:

```text
SELECTED_ENDPOINT_PROFILE=
SUPPORTED_MCP_PROTOCOL_VERSION=

CLIENT_IDENTITY_SUPPORTED=
AUTHENTICATION_MODE=

EXECUTE_OPERATION_PRESENT=
EXECUTE_OPERATION_INPUT_SCHEMA_FROZEN=
EXECUTE_OPERATION_OUTPUT_SCHEMA_FROZEN=

HIGHLEVEL_RESULT_ENCODING=
PROVIDER_WRAPPER_LOCATION=
OPERATION_PAYLOAD_SCHEMAS_FROZEN=

COMPOSITE_RESPONSE_CONTRACT_VERSION=
COMPOSITE_RESPONSE_CONTRACT_SHA256=
```

Do not implement `At1EstablishedMcpSession` until that composite response
contract is frozen and the readiness predicates in §3.1 are all `YES`.

## 10. Required return and stop

```text
ARTIFACT_ID=NW008_AT1_ESTABLISHED_SESSION_AND_RESPONSE_CONTRACT_CLOSURE_001

GRANT001_STOP_PROOF_READY=YES
GRANT001_TERMINAL=YES
GRANT001_REUSABLE=NO

ESTABLISHED_SESSION_IMPLEMENTATION_CURRENT_STATE=NOT_IMPLEMENTED

PROPER_SESSION_SEAM_IDENTIFIED=YES
SESSION_SEAM_NAME=At1EstablishedMcpSession

SESSION_SEAM_RESPONSE_LEVEL_FROZEN=NO
MCP_RESPONSE_CONTRACT_CURRENT_STATE=NOT_FROZEN

PREGRANT_SESSION_ESTABLISHMENT_CURRENT_STATE=NOT_FROZEN

SESSION_IDENTITY_BINDING_REQUIRED=YES

LIVE_GHL_CALLS=0
MCP_NETWORK_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO

NEXT=NW008_AT1_HIGHLEVEL_MCP_PROVIDER_CONTRACT_SOURCE_CAPTURE_001
STOP_CODE=NW008_AT1_ESTABLISHED_SESSION_AND_RESPONSE_CONTRACT_CLOSURE_COMPLETE_OFFLINE
```
