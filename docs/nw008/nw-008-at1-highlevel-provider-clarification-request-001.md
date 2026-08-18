# NW-008 AT-1 — HighLevel Provider Clarification Request 001

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_HIGHLEVEL_PROVIDER_CLARIFICATION_REQUEST_001
OWNER=VS Code / MG Orchestrator
PHASE=planning_only
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=f67c3ff09f48c34d6c7d07ad7e54475d3be39831
PLAN_BRANCH=planning/nw008-at1-highlevel-provider-clarification-001
CREATED_AT_UTC=2026-08-18T13:52:17Z
LOCAL_CLARIFICATION_COMMIT=671bc13
PR84_REVIEWED_HEAD=d7be0f5fbce488f4122b0434fd77de29c45f704c
PR84_MERGE_SHA=f67c3ff09f48c34d6c7d07ad7e54475d3be39831
```

This document preserves the existing clarification work from local commit `671bc13`, then moves it onto a fresh branch created from current `origin/main`. It is planning-only and does not authorize any provider interaction, network execution, or runtime validation.

```text
PROVIDER_REQUEST_DRAFTED=YES
PROVIDER_REQUEST_SUBMITTED=NO
PROVIDER_RESPONSE_CAPTURED=NO
PROVIDER_RESPONSE_RECONCILED=NO
PROVIDER_CONTACT_AUTHORIZED=HUMAN_ONLY
```

```text
CLASSIFICATION=planning_only
NETWORK_EXECUTION_AUTHORIZED=NO
MCP_RUNTIME_VALIDATION_AUTHORIZED=NO
NEW_OBSERVATION_AUTHORITY=NO
PRIOR_OBSERVATION_AUTHORITY_CONSUMED=YES
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO
```

## 2. Purpose and scope

The objective is to determine whether the original HighLevel `/mcp/` surface exposes the control-plane contract needed by NW008, or whether the authoritative contract must come from another provider-owned source. This artifact is intentionally fail-closed: the current state is that no provider request has been made, and no MCP endpoint activity is authorized.

This is a planning-only artifact. No network requests, endpoint probes, MCP validation, OAuth or PIT changes, or implementation work are authorized.

## 3. Provider questions

### Q1 — Generic endpoint control-plane tools

Does the original `https://services.leadconnectorhq.com/mcp/` endpoint expose `search_operations`, `describe_operation`, and `execute_operation` as part of the generic control-plane contract? If yes, please state whether those names are always present or conditionally present by auth mode, account, or client identity.

### Q2 — Alternative input-schema authority

If `describe_operation` is not exposed on the generic endpoint, is there another provider-owned authoritative mechanism for retrieving operation input schemas (for example: an OpenAPI document, machine-readable schema registry, developer documentation with schema payloads, or a dedicated schema endpoint)?

### Q3 — Output-contract authority and binding semantics

What provider-owned source defines the authoritative operation result/output contract for NW008? Please answer with the exact binding used by the provider, including:

- the MCP `CallToolResult` envelope
- whether `content` or `structuredContent` is the canonical business payload
- the exact business-payload location within the envelope
- any encoding or serialization behavior used for payload values
- success semantics (how success is distinguished from failure)
- error semantics (errors, codes, payload shape, retry guidance)
- stability, versioning, and provenance of that binding

If the binding is documented in more than one place, please identify the authoritative source and any version or provenance markers that distinguish the live contract from historical or sample docs.

### Q4 — PIT vs OAuth top-level toolset impact

Does the authentication mode (Private Integration Token vs OAuth) change the top-level MCP toolset returned by `tools/list`, or does it only affect the underlying operations or scopes available to those tools? Please state whether the same tool names and the same provider contract are expected across auth modes.

### Q5 — Contract acquisition without execution

For the following five operations critical to NW008:

1. `get-contact`
2. `get-opportunity`
3. `create-note`
4. `get-note`
5. `update-opportunity`

Is there a supported way to retrieve authoritative input and output contracts without executing the business operation? Please identify the provider-supported retrieval path and whether it is normative or illustrative.

### Q6 — v2 migration path and compatibility

If the control-plane capabilities above are v2-only features, what provider-supported path should a custom HTTP MCP client use until its dedicated `/mcp/{client}/v2` endpoint or equivalent migration path is available? Please state the expected compatibility and any contract or transport stability guarantees.

## 4. Result schema for provider integration

Upon provider answers, populate the result state with the current absence semantics explicitly separated from provider-confirmed absence.

```text
PROVIDER_INPUT_CONTRACT_AUTHORITY_IDENTIFIED=NO
PROVIDER_INPUT_CONTRACT_UNAVAILABLE_CONFIRMED=UNKNOWN
PROVIDER_OUTPUT_CONTRACT_AUTHORITY_IDENTIFIED=NO
PROVIDER_OUTPUT_CONTRACT_UNAVAILABLE_CONFIRMED=UNKNOWN
GENERIC_ENDPOINT_SEARCH_OPERATIONS_AVAILABLE=UNKNOWN
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE=UNKNOWN
GENERIC_ENDPOINT_EXECUTE_OPERATION_AVAILABLE=UNKNOWN
PIT_CHANGES_TOP_LEVEL_MCP_TOOLSET=UNKNOWN
OAUTH_CHANGES_TOP_LEVEL_MCP_TOOLSET=UNKNOWN
NW008_CONTRACT_ACQUISITION_PATH=UNKNOWN
FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO
```

These values intentionally distinguish between a contract not yet found (`NO` / `UNKNOWN`) and a contract that may later be confirmed unavailable by provider documentation or support guidance.

## 5. Preferred provider channel and reviewer disposition

Prefer the official **GoHighLevel/highlevel-api-docs** GitHub issue path for a human reviewer to pose the six questions above, tagged appropriately for MCP and developer tooling. This artifact remains planning-only and does not authorize a provider submission on its own.

The required disposition is a reviewer stop gate: approve or modify the questions before any human submission. No provider request is currently recorded as submitted.

## 6. Forbidden actions

The following actions are explicitly forbidden under this planning artifact:

- `initialize`, `tools/list`, `search_operations`, `describe_operation`, `execute_operation`
- endpoint probes of any kind
- User-Agent experiments
- HighLevel reads or writes
- raw REST substitution for MCP calls
- OAuth or PIT credential changes
- location binding changes
- IAM, secrets, or deployment changes
- runtime implementation changes
- any Grant009-related actions

## 7. Next steps

1. Reviewer disposition — approve or modify the questions before any human submission.
2. Human provider submission — if approved, submit through the preferred provider channel.
3. Response integration — populate the result schema and determine the NW008 contract acquisition path.
4. Future authorization gate — only after this planning step is complete may any observation or implementation authorization be designed.

---

*This document is a planning artifact only. `PROVIDER_REQUEST_SUBMITTED=NO` and zero provider, network, or MCP requests have been made.*
