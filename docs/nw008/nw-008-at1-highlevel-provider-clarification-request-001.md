# NW-008-AT1 — HighLevel Provider Clarification Request 001

**Classification:** PLANNING_ONLY
**Planning ID:** NW008_AT1_HIGHLEVEL_PROVIDER_CLARIFICATION_REQUEST_001
**Created:** 2026-08-18
**Owner:** VS Code / MG Orchestrator

## Binding

| Key | Value |
|-----|-------|
| PR84_REVIEWED_HEAD | `d7be0f5fbce488f4122b0434fd77de29c45f704c` |
| PR84_MERGE_SHA | `f67c3ff09f48c34d6c7d07ad7e54475d3be39831` |

## Authorization Flags

| Flag | Value |
|------|-------|
| NETWORK_EXECUTION_AUTHORIZED | NO |
| MCP_RUNTIME_VALIDATION_AUTHORIZED | NO |
| NEW_OBSERVATION_AUTHORITY | NO |
| PRIOR_OBSERVATION_AUTHORITY_CONSUMED | YES |
| PROVIDER_OUTPUT_BINDING_FROZEN | NO |
| COMPOSITE_CONTRACT_FREEZE_READY | NO |
| IMPLEMENTATION_CHANGE_AUTHORIZABLE | NO |

## Purpose

Determine whether HighLevel's original `/mcp/` endpoint exposes the
control-plane contract needed by NW008, or whether another provider-owned
authoritative contract source exists.

This is a **planning-only** artifact. No network requests, MCP calls,
endpoint probes, or provider interactions are authorized.

## Provider Questions

### Q1 — Generic Endpoint Control-Plane Tools

Does the original `https://services.leadconnectorhq.com/mcp/` endpoint expose:

- `search_operations`
- `describe_operation`
- `execute_operation`

These are the control-plane tools that would allow a client to discover and
introspect available operations without prior knowledge of the operation catalog.

### Q2 — Alternative Input Schema Authority

If `describe_operation` is not exposed on the generic endpoint, is there another
provider-owned authoritative mechanism for retrieving operation input schemas
(e.g., OpenAPI spec, developer docs with machine-readable schemas, a dedicated
schema endpoint)?

### Q3 — Output Contract Authority

What provider-owned source defines operation result/output contracts, including:

- MCP `CallToolResult` structure (content array, isError semantics)
- Business payload location within the result
- Success semantics (how to distinguish success from failure)
- Error semantics (error codes, error shapes, retry guidance)

### Q4 — PIT vs OAuth Top-Level Toolset Impact

Does the authentication mode (Private Integration Token vs OAuth) change the
**top-level MCP toolset** (i.e., the set of tool names returned by `tools/list`),
or does it only affect the underlying operations/scopes available to those tools?

### Q5 — Contract Retrieval Without Execution

For the following five operations critical to NW008:

1. `get-contact`
2. `get-opportunity`
3. `create-note`
4. `get-note`
5. `update-opportunity`

Is there a supported way to retrieve authoritative input AND output contracts
without executing the business operation?

### Q6 — v2 Migration Path

If the control-plane capabilities (search/describe/execute) are v2-only features,
what provider-supported path should a custom/OpenAI/Codex client use until its
dedicated `/mcp/{client}/v2` endpoint ships?

## Required Result Schema

Upon receiving provider answers, populate the following:

```
GENERIC_ENDPOINT_SEARCH_OPERATIONS_AVAILABLE   = UNKNOWN
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE   = UNKNOWN
GENERIC_ENDPOINT_EXECUTE_OPERATION_AVAILABLE    = UNKNOWN
PROVIDER_INPUT_CONTRACT_AUTHORITY_IDENTIFIED    = NO
PROVIDER_OUTPUT_CONTRACT_AUTHORITY_IDENTIFIED   = NO
PIT_CHANGES_TOP_LEVEL_MCP_TOOLSET              = UNKNOWN
OAUTH_CHANGES_TOP_LEVEL_MCP_TOOLSET            = UNKNOWN
NW008_CONTRACT_ACQUISITION_PATH                = UNKNOWN
FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE    = NO
```

All values are initialized to UNKNOWN or NO pending provider response.

## Preferred Provider Channel

Open an issue on the official **GoHighLevel/highlevel-api-docs** GitHub repository
with the questions above, tagged appropriately for MCP / developer tooling.

## Escalation Path

Official HighLevel developer support or community channels, only if the GitHub
issue does not receive a response within a reasonable timeframe.

## Forbidden Actions

The following actions are **explicitly forbidden** under this planning artifact:

- `initialize`, `tools/list`, `search_operations`, `describe_operation`, `execute_operation`
- Endpoint probes of any kind
- User-Agent experiments
- GHL reads or writes
- Raw REST substitution for MCP calls
- OAuth or PIT credential changes
- Location binding changes
- IAM, secrets, or deployment changes
- Runtime implementation changes
- Any Grant009-related actions

## Next Steps

1. **Reviewer disposition** — reviewer approves or modifies questions before submission
2. **Provider submission** — upon approval, submit to preferred provider channel
3. **Response integration** — populate result schema and unblock NW008 contract acquisition

---

*This document is a planning artifact only. Zero provider requests have been made.*
