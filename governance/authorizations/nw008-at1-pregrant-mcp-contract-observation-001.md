# NW-008 AT-1 Pre-Grant MCP Contract Observation Authorization

## 1. Authorization identity and activation boundary

```text
CLASSIFICATION=authorization
AUTHORIZATION_ID=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001
OWNER=VS Code / MG Orchestrator
BASE_REF=origin/main
BASE_SHA=262fc1670a910e147de4e634117002fd38172e87
AUTHORIZATION_BRANCH=auth/nw008-at1-pregrant-mcp-contract-observation-001
SOURCE_PLANNING_UNIT=proof/nw008/nw-008-at1-mcp-response-source-capture.md

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=HUMAN_REVIEW_AND_MERGE_TO_MAIN
SELF_ACTIVATION=FORBIDDEN
OBSERVATION_EXECUTION_OCCURRED=NO
```

This unit authorizes only a pre-grant MCP protocol and advertised-tool contract
observation. The authorization becomes effective only after human review and
merge to `main`. Creating or reviewing this artifact does not execute the
observation.

The later observation must run as a separate proof-producing unit against the
merged authorization. It may negotiate the already selected protocol version
and capture the advertised tool catalog, but it may not invoke any advertised
tool.

## 2. Verified prerequisites and frozen state

The following preconditions were verified after `git fetch origin` and before
this artifact was created:

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #76 reviewed head `fb0da6d41484ae44aae06b86a4e78788ca4b211b` is an ancestor of `origin/main` | YES |
| PR #76 merge SHA | `262fc1670a910e147de4e634117002fd38172e87` |
| Source-capture artifact exists on `origin/main` | YES |

```text
PR76_REVIEWED_HEAD=fb0da6d41484ae44aae06b86a4e78788ca4b211b
PR76_MERGE_SHA=262fc1670a910e147de4e634117002fd38172e87
PR76_MAIN_REACHABLE=YES
SOURCE_CAPTURE_ON_MAIN=YES

SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES

HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
PREGRANT_TOOLS_LIST_REQUIRED=YES
```

These values are prerequisites, not outputs to be selected dynamically. The
observation may test compatibility with `2025-11-25`; it may not replace,
downgrade, or otherwise select a different supported version.

## 3. Authorized protocol operations

Once this authorization is effective, the observation has exactly this
protocol-operation authority:

```text
MCP_INITIALIZE_AUTHORIZED=YES
MCP_TOOLS_LIST_AUTHORIZED=YES

MCP_EXECUTE_OPERATION_AUTHORIZED=NO
EXECUTE_OPERATION_CALL_BUDGET=0

GHL_BUSINESS_READ_AUTHORIZED=NO
GHL_MUTATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

`MCP_INITIALIZE_AUTHORIZED=YES` permits one MCP initialization exchange using
`SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25`, including only protocol-required
lifecycle messages needed to establish and close that observation session.

`MCP_TOOLS_LIST_AUTHORIZED=YES` permits exactly one `tools/list` pagination
sequence. The sequence starts with one initial `tools/list` request and may
follow each provider-returned `nextCursor` exactly once, in order, only until
the provider omits `nextCursor`. A repeated initial request, repeated cursor,
catalog refresh, polling, retry after a completed response, or second listing
sequence is not authorized. Transport-level handling must fail closed rather
than increase this budget.

No `tools/call` request is authorized. In particular, discovering a tool named
`execute_operation` does not authorize calling it.

## 4. Required observation procedure

The later observation unit must perform these steps in order:

1. Initialize with client-supported protocol version exactly `2025-11-25`.
2. Capture the negotiated protocol version and initialization provenance.
3. If the negotiated version is not exactly `2025-11-25`, record the mismatch,
   fail closed, close the session without a `tools/list`, and stop.
4. If the version matches, run exactly one bounded `tools/list` pagination
   sequence as defined in section 3, sufficient to capture the advertised tool
   catalog.
5. Locate the tool whose `name` is exactly `execute_operation`.
6. If advertised, capture the tool descriptor exactly as returned, including
   its exact `inputSchema` and exact `outputSchema` when those members are
   advertised. Member absence must be recorded as absence, not inferred.
7. Capture protocol and server metadata needed to establish provenance,
   including the initialize request's offered version, the initialize result's
   `protocolVersion`, `serverInfo`, and `capabilities`, the transport class,
   request/response identifiers, observation timestamps, and ordered
   `tools/list` pagination evidence. Credentials, tokens, secret values, and
   private record identifiers must not be recorded.
8. Preserve a byte-exact evidence capture and compute SHA-256 digests for the
   initialize evidence, complete ordered catalog evidence, and exact
   provider-owned `execute_operation` schema evidence.
9. Make zero `execute_operation` calls and zero GHL business reads or writes.
10. Stop and return proof.

For `EXECUTE_OPERATION_SCHEMA_SHA256`, the digest subject is an RFC 8785
JSON-canonicalized object containing the exact advertised schema members:

```json
{
  "inputSchema": "<exact advertised value>",
  "outputSchema": "<exact advertised value>"
}
```

The strings above are placeholders describing the digest subject, not literal
values. The observation must substitute the exact JSON values. If
`execute_operation`, `inputSchema`, or `outputSchema` is absent, it must not
invent a schema or a schema digest; it must report the applicable capture field
as `NO` and `EXECUTE_OPERATION_SCHEMA_SHA256=NOT_AVAILABLE`.

The evidence must retain the complete ordered provider response separately from
the canonical digest subject so a reviewer can reproduce every digest without
consulting sample business responses.

## 5. Fail-closed conditions

The observation must stop without `tools/list` when:

```text
NEGOTIATED_PROTOCOL_VERSION!=2025-11-25
PROTOCOL_VERSION_MATCH=NO
FAIL_CLOSED=YES
```

It must also stop and return terminal proof, without retrying or expanding
authority, on malformed initialization data, a protocol error, pagination
cursor repetition, response/request binding failure, incomplete evidence
capture, evidence serialization failure, or any condition that would require a
second catalog sequence.

An absent `execute_operation`, absent `inputSchema`, or absent `outputSchema` is
an observation result, not permission to infer the provider contract. Those
results leave:

```text
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
```

Positive freeze results may be reported only when the captured provider-owned
advertisement and all prerequisite contract layers satisfy the source-capture
plan's authority rules. This authorization alone does not declare either
contract frozen.

## 6. Required proof return

The observation proof must identify this authorization and its merge commit,
record all call counts, bind the raw/redacted evidence and digests, and include
these result fields:

```text
NEGOTIATED_PROTOCOL_VERSION=<exact value or NOT_NEGOTIATED>
PROTOCOL_VERSION_MATCH=<YES|NO>
EXECUTE_OPERATION_TOOL_PRESENT=<YES|NO|NOT_OBSERVED>
EXECUTE_OPERATION_INPUT_SCHEMA_CAPTURED=<YES|NO|NOT_OBSERVED>
EXECUTE_OPERATION_OUTPUT_SCHEMA_CAPTURED=<YES|NO|NOT_OBSERVED>
EXECUTE_OPERATION_SCHEMA_SHA256=<sha256 or NOT_AVAILABLE>
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=<YES|NO>
COMPOSITE_CONTRACT_FREEZE_READY=<YES|NO>
```

It must also report:

```text
MCP_INITIALIZE_CALLS=<0|1>
MCP_TOOLS_LIST_SEQUENCES=<0|1>
MCP_TOOLS_LIST_REQUESTS=<non-negative integer>
MCP_EXECUTE_OPERATION_CALLS=0
GHL_BUSINESS_READS=0
GHL_MUTATIONS=0
GRANT009_EXECUTIONS=0
FAIL_CLOSED=<YES|NO>
STOP_REASON=<terminal reason>
```

`NOT_OBSERVED` is permitted only when initialization fails or the negotiated
version mismatches before `tools/list`. A completed catalog sequence must
resolve each catalog-derived field to `YES` or `NO`.

## 7. Explicit prohibitions

This authorization does not permit:

- parser, session, adapter, or runtime implementation;
- any `execute_operation` call;
- `get-contact`, `get-opportunity`, `create-note`, `get-note`, or
  `update-opportunity`;
- any other advertised tool invocation;
- any GHL business read, CRM mutation, or real-customer-data access;
- drafting, activating, or executing Grant 009;
- IAM, secret, deployment, workflow, or infrastructure changes;
- raw REST access;
- schema inference from sample responses, fixtures, parser behavior, prose
  examples, or undocumented observations;
- runtime protocol-version selection, downgrade, or post-grant schema
  discovery; or
- authority expansion through retries, pagination restart, or additional
  sessions.

```text
PARSER_IMPLEMENTATION_AUTHORIZED=NO
SESSION_IMPLEMENTATION_AUTHORIZED=NO
RAW_REST_AUTHORIZED=NO
IAM_CHANGE_AUTHORIZED=NO
SECRET_CHANGE_AUTHORIZED=NO
DEPLOYMENT_CHANGE_AUTHORIZED=NO
SAMPLE_RESPONSE_AS_SCHEMA_AUTHORITY=NO
```

## 8. Authorization PR validation and review gate

This PR is class `authorization`. Its writable scope is exactly:

```text
governance/authorizations/nw008-at1-pregrant-mcp-contract-observation-001.md
```

Required before merge:

1. `git diff --check`;
2. exactly one changed path, equal to the path above;
3. repository-required deterministic validation;
4. exact-head `Phase 1 deterministic validation` success;
5. clean mergeability into `main`; and
6. human review and human merge authority.

The observation must not execute from an open or unmerged authorization PR.
Any push changes the exact head and requires exact-head CI and human review to
be evaluated again.

## 9. Decision and stop

```text
AUTHORIZATION_ID=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001
STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=HUMAN_REVIEW_AND_MERGE_TO_MAIN

MCP_INITIALIZE_AUTHORIZED=YES
MCP_TOOLS_LIST_AUTHORIZED=YES
MCP_EXECUTE_OPERATION_AUTHORIZED=NO
EXECUTE_OPERATION_CALL_BUDGET=0

GHL_BUSINESS_READ_AUTHORIZED=NO
GHL_MUTATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

SUPPORTED_MCP_PROTOCOL_VERSION=2025-11-25
PRE_GRANT_NEGOTIATED_VERSION_MUST_EQUAL_SUPPORTED_VERSION=YES
HIGHLEVEL_PROVIDER_CONTRACT_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
PREGRANT_TOOLS_LIST_REQUIRED=YES

OBSERVATION_EXECUTION_OCCURRED=NO
NEXT=HUMAN_REVIEW_AND_MERGE_AUTHORIZATION_PR
STOP_CODE=NW008_AT1_PREGRANT_MCP_CONTRACT_OBSERVATION_001_AUTHORIZATION_READY_FOR_REVIEW
```
