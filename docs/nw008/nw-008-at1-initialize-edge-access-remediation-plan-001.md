# NW-008 AT-1 Initialize Edge Access Remediation Plan 001

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_INITIALIZE_EDGE_ACCESS_REMEDIATION_PLAN_001
OWNER=VS Code / MG Orchestrator
PHASE=planning_only
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=d93f4b418ed84a72c83a4b2ac07f06b4b4a5b922
PLAN_BRANCH=planning/nw008-at1-initialize-edge-access-remediation-001
CREATED_AT_UTC=2026-08-18T12:09:42Z

PR83_REVIEWED_HEAD=c892b28fa026edc22c9670165648cb5dce3690fb
PR83_MERGE_SHA=d93f4b418ed84a72c83a4b2ac07f06b4b4a5b922
PR83_REVIEWED_HEAD_REACHABLE=YES
```

This planning-only unit determines the provider-supported MCP endpoint, client
identity, and authentication configuration required before any future NW008
AT-1 observation authorization can be drafted. It binds PR #83 merged evidence
and performs no network, MCP, or implementation activity.

```text
PRIOR_OBSERVATION_AUTHORITY_CONSUMED=YES
NEW_OBSERVATION_AUTHORITY=NO
NETWORK_EXECUTION_AUTHORIZED=NO
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
```

### 1.1 Scope prohibitions

```text
MCP_INITIALIZE=FORBIDDEN
NOTIFICATIONS_INITIALIZED=FORBIDDEN
MCP_DESCRIBE_OPERATION=FORBIDDEN
MCP_TOOLS_LIST=FORBIDDEN
MCP_SEARCH_OPERATIONS=FORBIDDEN
MCP_EXECUTE_OPERATION=FORBIDDEN
ENDPOINT_PROBE=FORBIDDEN
USER_AGENT_PROBE=FORBIDDEN
GHL_BUSINESS_READ=FORBIDDEN
GHL_MUTATION=FORBIDDEN
RAW_REST=FORBIDDEN
NEW_OAUTH_ACTION=FORBIDDEN
NEW_PIT_ACTION=FORBIDDEN
IAM_SECRET_CHANGE=FORBIDDEN
DEPLOY_CHANGE=FORBIDDEN
GRANT009=FORBIDDEN
PARSER_IMPLEMENTATION=FORBIDDEN
RUNTIME_IMPLEMENTATION=FORBIDDEN
```

## 2. Inherited fail-closed state

From PR #83 merged proof (`proof/nw008/nw-008-at1-describe-operation-contract-observation-001.md`):

| Binding | Value |
| --- | --- |
| `CONDITION_NAME` | `INITIALIZE_EDGE_BLOCK` |
| `FAIL_CLOSED_CONDITION` | `INITIALIZE_RESPONSE_NOT_JSONRPC_HTTP_403_CLOUDFLARE_ERROR_1010` |
| `FAILURE_LAYER` | `PROVIDER_HTTP_EDGE` |
| `MCP_INITIALIZATION_COMPLETED` | NO |
| `NEGOTIATED_PROTOCOL_VERSION` | `NOT_NEGOTIATED` |
| `GCP_AUTH_FAILURE` | NO |
| `PIT_REJECTION` | NO |

The fail-closed observation established that:

1. The single `initialize` request at `2026-08-18T11:32:12Z` was answered at the
   Cloudflare edge with HTTP 403 error 1010 (`browser_signature_banned`).
2. The block was not a GCP authentication failure or a PIT credential rejection.
3. The Cloudflare response instructed **"Do not retry."**
4. No MCP JSON-RPC envelope was received; version negotiation never occurred.
5. The authorization permitted no retry, replacement call, or reconnect.

Error 1010 is preserved as a client/browser-signature edge block. The evidence
does not prove that the default Python User-Agent caused the block, and it does
not prove that use of the Anthropic-designated path caused the block.

## 3. Endpoint and client matrix (documented evidence)

### 3.1 Documented endpoints

From PR #80 provider-output-authority-acquisition (`proof/nw008/nw-008-at1-provider-output-authority-acquisition-001.md`) section 4.1:

| Pattern | Status | Source |
| --- | --- | --- |
| `https://services.leadconnectorhq.com/mcp/{client}/v2` | Documented client-specific pattern | HighLevel MCP doc |
| `https://services.leadconnectorhq.com/mcp/anthropic/v2` | Live; designated for Claude | HighLevel MCP doc |
| `https://services.leadconnectorhq.com/mcp/` | Supported original endpoint for custom HTTP MCP clients | HighLevel MCP doc |

The current official documentation also states that each MCP connection is
attached to a single subaccount/location and that dedicated OpenAI and VS Code
endpoints remain on the roadmap.

```text
HIGHLEVEL_MCP_DOC_STATUS=LIVING_SOURCE
HIGHLEVEL_MCP_DOC_VERIFIED_AT_UTC=2026-08-18T12:32:23Z
SOURCE_RECHECK_REQUIRED_BEFORE_FUTURE_AUTHORIZATION=YES
```

### 3.2 Prior observation surface

The consumed observation used:

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
TRANSPORT_CLASS=streamable_http_sse
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
TRANSPORT_CLIENT=python_urllib_stdlib (Python 3.9.6, default User-Agent)
```

The edge response classified the rejection as `browser_signature_banned`. That
classification identifies a client/browser-signature edge block, but it does
not isolate the default Python User-Agent or the selected path as causal.

### 3.3 Runtime topology boundary

The future HighLevel integration path requires an MG-owned GHL MCP client
adapter that connects to HighLevel's remote provider MCP server. MG MCP is not
in that runtime path; its role remains read-only governed context.

```text
HIGHLEVEL_MCP_ROLE=REMOTE_PROVIDER_MCP_SERVER
MG_INTEGRATION_ROLE=GHL_MCP_CLIENT_ADAPTER
MG_MCP_IN_RUNTIME_GHL_PATH=NO
MG_MCP_ROLE=READ_ONLY_GOVERNED_CONTEXT
```

This topology is an architecture distinction only. It does not authorize or
implement the adapter, activate a runtime connection, or validate any generic
endpoint contract.

### 3.4 Target-location gate

The documented single-subaccount attachment model is architecture-ready, but
no target location is selected or bound. A future target must be isolated or
competition-approved and use synthetic or explicitly approved test data.

```text
TARGET_GHL_LOCATION_SELECTED=NO
TARGET_GHL_LOCATION_CLASS=ISOLATED_OR_COMPETITION_APPROVED
TARGET_GHL_LOCATION_ID_IN_PUBLIC_ARTIFACT=NO
SYNTHETIC_OR_APPROVED_TEST_DATA_REQUIRED=YES
LOCATION_BINDING_REQUIRES_SEPARATE_AUTHORIZATION=YES
```

## 4. Planning questions and answers

### Q1. Is `/mcp/anthropic/v2` provider-supported for a custom Python/VS Code client, or only Claude-class clients?

**Answer: NO for the current client.**

- **Official designation**: The current HighLevel MCP documentation designates
  `/mcp/anthropic/v2` for Claude.
- **Current client**: The VS Code / MG Orchestrator is not Claude and therefore
  is not the provider-designated client for that client-specific endpoint.
- **Edge evidence boundary**: PR #83 still establishes error 1010 as a
  client/browser-signature edge block. It does not prove that the default
  Python User-Agent or the Anthropic path mismatch caused that response.

```text
Q1_ANSWER=NO
Q1_EVIDENCE_QUALITY=CURRENT_OFFICIAL_HIGHLEVEL_MCP_DOC
ANTHROPIC_V2_DESIGNATED_CLIENT=CLAUDE
ANTHROPIC_V2_PROVIDER_DESIGNATED_FOR_CURRENT_CLIENT=NO
```

### Q2. Is `/mcp/` the supported generic HTTP MCP endpoint for our current client?

**Answer: YES**

- **Official designation**: The current HighLevel MCP documentation identifies
  the original `/mcp/` endpoint as the supported surface for custom HTTP MCP
  clients.
- **Attachment boundary**: Each connection attaches to one HighLevel
  subaccount/location.
- **Observation boundary**: This planning update did not contact the endpoint.

```text
Q2_ANSWER=YES
Q2_EVIDENCE_QUALITY=CURRENT_OFFICIAL_HIGHLEVEL_MCP_DOC
SUPPORTED_CLIENT_ENDPOINT_IDENTIFIED=YES
SUPPORTED_CLIENT_ENDPOINT=https://services.leadconnectorhq.com/mcp/
SUPPORTED_CLIENT_CLASS=CUSTOM_HTTP_MCP_CLIENT
GHL_MCP_ATTACHMENT_LEVEL=SINGLE_SUBACCOUNT_PER_CONNECTION
```

### Q3. Does `/mcp/` expose `describe_operation` and the five frozen AT-1 operations?

**Answer: UNKNOWN**

- **Evidence**: From PR #78 pregrant observation, the `/mcp/anthropic/v2`
  endpoint's `tools/list` advertised `execute_operation`, `describe_operation`,
  `search`, `fetch`, `search_operations`, and `list_locations`. The five frozen
  AT-1 operation IDs (`get-contact`, `get-opportunity`, `create-note`,
  `get-note`, `update-opportunity`) were confirmed present via `search_operations`
  in Grant008.
- **Current documentation boundary**: The current official documentation does
  not document the unified `describe_operation` tool on the original `/mcp/`
  endpoint. The client-specific catalog cannot be transferred to that endpoint
  by assumption.

```text
Q3_ANSWER=UNKNOWN
Q3_EVIDENCE_QUALITY=CURRENT_DOC_ABSENCE_PLUS_ALTERNATE_ENDPOINT_OBSERVATION
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE=UNKNOWN
```

### Q4. Does PIT provide the required catalog/scopes, or is OAuth required?

**Answer: BOTH SUPPORTED; OAuth is not required and is preferred for widest scope.**

- **Evidence**: PR #77/PR #78 pregrant observation successfully initialized,
  completed `tools/list`, and captured the catalog using PIT + Bearer auth
  against `/mcp/anthropic/v2`.
- **Official authentication support**: The generic endpoint supports PIT and
  OAuth authentication. OAuth is preferred for widest scope but is not
  required for authentication.
- **Remaining catalog gap**: The official documentation does not establish
  whether PIT is sufficient for the required NW008 catalog on the generic
  endpoint.

```text
Q4_ANSWER=BOTH_SUPPORTED_OAUTH_PREFERRED_FOR_WIDEST_SCOPE
Q4_EVIDENCE_QUALITY=CURRENT_OFFICIAL_HIGHLEVEL_MCP_DOC
PIT_SUPPORTED_ON_GENERIC_ENDPOINT=YES
OAUTH_SUPPORTED_ON_GENERIC_ENDPOINT=YES
OAUTH_REQUIRED_FOR_AUTHENTICATION=NO
OAUTH_PREFERRED_FOR_WIDEST_SCOPE=YES
PIT_SUFFICIENT_FOR_REQUIRED_NW008_CATALOG=UNKNOWN
```

### Q5. Is a dedicated OpenAI/VS Code client endpoint now live or still roadmap-only?

**Answer: ROADMAP**

- **Current status**: The official HighLevel MCP documentation identifies
  dedicated OpenAI and VS Code endpoints as roadmap items, not live endpoints.
- **Current route**: The supported route for this custom HTTP MCP client is the
  original `/mcp/` endpoint.

```text
Q5_ANSWER=ROADMAP
Q5_EVIDENCE_QUALITY=CURRENT_OFFICIAL_HIGHLEVEL_MCP_DOC
DEDICATED_OPENAI_ENDPOINT_LIVE=NO
DEDICATED_VSCODE_ENDPOINT_LIVE=NO
DEDICATED_ENDPOINT_STATUS=ROADMAP
```

### Q6. What exact endpoint, client identity, auth mode, protocol version, and transport behavior would a future authorization need to freeze?

**Answer: ATTACHMENT ARCHITECTURE READY; RUNTIME ACTIVATION NOT AUTHORIZED**

A future observation authorization would need to freeze:

| Parameter | Prior Value | Future Value | Status |
| --- | --- | --- | --- |
| Endpoint | `https://services.leadconnectorhq.com/mcp/anthropic/v2` | `https://services.leadconnectorhq.com/mcp/` | Documented; not runtime-validated |
| Client class | Python `urllib` client | GHL MCP client adapter as custom HTTP MCP client | Documented; future client profile not frozen |
| Attachment | Prior bound location | Single subaccount/location per connection | Documented; target location not selected |
| Auth mode | PIT + Bearer | TBD | Likely unchanged if endpoint allows |
| Protocol version | Observed `2025-11-25` | TBD | Generic endpoint support unknown |
| Auth support | PIT | PIT or OAuth | Both supported; PIT sufficiency for the NW008 catalog remains unknown |
| Tool availability | Observed on Anthropic endpoint | `describe_operation` on generic endpoint | **UNKNOWN** |

```text
Q6_ANSWER=ATTACHMENT_ARCHITECTURE_READY_RUNTIME_ACTIVATION_NOT_AUTHORIZED
Q6_AUTH_MODE_FROZEN=NO
GENERIC_ENDPOINT_DOCUMENTED=YES
GENERIC_CLIENT_CLASS_DOCUMENTED=YES
ATTACHMENT_LEVEL_DOCUMENTED=YES
GENERIC_ENDPOINT_RUNTIME_VALIDATED=NO
PRIOR_OBSERVED_PROTOCOL_VERSION=2025-11-25
GENERIC_ENDPOINT_PROTOCOL_VERSION_SUPPORT=UNKNOWN
FUTURE_AUTH_ENDPOINT_FROZEN=NO
FUTURE_AUTH_CLIENT_PROFILE_FROZEN=NO
FUTURE_AUTH_PROTOCOL_VERSION_FROZEN=NO
FUTURE_AUTH_TRANSPORT_CONTRACT_FROZEN=NO
GHL_MCP_ATTACHMENT_ARCHITECTURE_READY=YES
GHL_MCP_RUNTIME_ACTIVATION_AUTHORIZED=NO
NW008_FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO
```

### Q7. Is HighLevel/provider clarification required before any new authorization?

**Answer: YES**

- The supported custom-client endpoint, attachment level, and authentication
  options are now identified from current official documentation.
- The remaining provider clarification is limited to whether the original
  generic endpoint exposes the unified `describe_operation` toolset needed by
  NW008.
- Provider clarification must precede any endpoint validation. Any later
  endpoint validation would require separate new authorization.

```text
Q7_ANSWER=YES
PROVIDER_CLARIFICATION_SCOPE=GENERIC_ENDPOINT_UNIFIED_TOOLSET_DESCRIBE_OPERATION
FUTURE_ENDPOINT_VALIDATION_REQUIRES_NEW_AUTHORIZATION=YES
PROVIDER_CLARIFICATION_PRECEDES_ANY_ENDPOINT_VALIDATION=YES
```

## 5. Source matrix

| PR | Reviewed head | Merge SHA | Claim supported |
| --- | --- | --- | --- |
| #76 | `fb0da6d41484ae44aae06b86a4e78788ca4b211b` | `262fc1670a910e147de4e634117002fd38172e87` | Prior observed protocol version was `2025-11-25`; this does not establish generic endpoint support |
| #78 | `b16f49ca3813746614e228dd4433d88cf6b0cfc5` | `781f8ce90c7b63fc8e23eec62dda7544bda8d143` | Prior successful client-specific endpoint observation and advertised tool catalog |
| #80 | `f183ac14140840d5325b17c9cc6bc88378fa47aa` | `8d70390b9b962c0276a99ea0d8b63c384c1a426c` | Living official HighLevel MCP documentation was acquired as source evidence |
| #83 | `c892b28fa026edc22c9670165648cb5dce3690fb` | `d93f4b418ed84a72c83a4b2ac07f06b4b4a5b922` | Error 1010 client/browser-signature edge block; no causal attribution to User-Agent or path |

The current living HighLevel MCP documentation supports the generic custom
HTTP client endpoint, single-subaccount attachment level, PIT/OAuth support,
Claude client designation, and dedicated endpoint roadmap claims. It does not
establish the generic endpoint runtime, protocol, transport, or unified
`describe_operation` contract.

## 6. Decision outputs

```text
SUPPORTED_CLIENT_ENDPOINT_IDENTIFIED=YES
SUPPORTED_CLIENT_ENDPOINT=https://services.leadconnectorhq.com/mcp/
SUPPORTED_CLIENT_CLASS=CUSTOM_HTTP_MCP_CLIENT
GHL_MCP_ATTACHMENT_LEVEL=SINGLE_SUBACCOUNT_PER_CONNECTION
HIGHLEVEL_MCP_ROLE=REMOTE_PROVIDER_MCP_SERVER
MG_INTEGRATION_ROLE=GHL_MCP_CLIENT_ADAPTER
MG_MCP_IN_RUNTIME_GHL_PATH=NO
MG_MCP_ROLE=READ_ONLY_GOVERNED_CONTEXT
ANTHROPIC_V2_DESIGNATED_CLIENT=CLAUDE
ANTHROPIC_V2_PROVIDER_DESIGNATED_FOR_CURRENT_CLIENT=NO
GENERIC_ENDPOINT_DOCUMENTED=YES
GENERIC_CLIENT_CLASS_DOCUMENTED=YES
ATTACHMENT_LEVEL_DOCUMENTED=YES
GENERIC_ENDPOINT_RUNTIME_VALIDATED=NO
PRIOR_OBSERVED_PROTOCOL_VERSION=2025-11-25
GENERIC_ENDPOINT_PROTOCOL_VERSION_SUPPORT=UNKNOWN
FUTURE_AUTH_ENDPOINT_FROZEN=NO
FUTURE_AUTH_CLIENT_PROFILE_FROZEN=NO
FUTURE_AUTH_PROTOCOL_VERSION_FROZEN=NO
FUTURE_AUTH_TRANSPORT_CONTRACT_FROZEN=NO
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE=UNKNOWN
PIT_SUPPORTED_ON_GENERIC_ENDPOINT=YES
OAUTH_SUPPORTED_ON_GENERIC_ENDPOINT=YES
OAUTH_REQUIRED_FOR_AUTHENTICATION=NO
OAUTH_PREFERRED_FOR_WIDEST_SCOPE=YES
PIT_SUFFICIENT_FOR_REQUIRED_NW008_CATALOG=UNKNOWN
DEDICATED_OPENAI_ENDPOINT_LIVE=NO
DEDICATED_VSCODE_ENDPOINT_LIVE=NO
DEDICATED_ENDPOINT_STATUS=ROADMAP
GHL_MCP_ATTACHMENT_ARCHITECTURE_READY=YES
GHL_MCP_RUNTIME_ACTIVATION_AUTHORIZED=NO
TARGET_GHL_LOCATION_SELECTED=NO
TARGET_GHL_LOCATION_CLASS=ISOLATED_OR_COMPETITION_APPROVED
TARGET_GHL_LOCATION_ID_IN_PUBLIC_ARTIFACT=NO
SYNTHETIC_OR_APPROVED_TEST_DATA_REQUIRED=YES
LOCATION_BINDING_REQUIRES_SEPARATE_AUTHORIZATION=YES
PROVIDER_CLARIFICATION_REQUIRED=YES
PROVIDER_CLARIFICATION_SCOPE=GENERIC_ENDPOINT_UNIFIED_TOOLSET_DESCRIBE_OPERATION
NW008_FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO
FUTURE_ENDPOINT_VALIDATION_REQUIRES_NEW_AUTHORIZATION=YES
PROVIDER_CLARIFICATION_PRECEDES_ANY_ENDPOINT_VALIDATION=YES
HIGHLEVEL_MCP_DOC_STATUS=LIVING_SOURCE
HIGHLEVEL_MCP_DOC_VERIFIED_AT_UTC=2026-08-18T12:32:23Z
SOURCE_RECHECK_REQUIRED_BEFORE_FUTURE_AUTHORIZATION=YES
```

## 7. Unknowns requiring provider clarification

| Unknown | Question for HighLevel |
| --- | --- |
| U1 | Does the original generic endpoint expose the unified `describe_operation` toolset required by NW008? |
| U2 | Is PIT sufficient for the required NW008 catalog on the generic endpoint? |

## 8. Proposed planning-only PR

```text
PR_TITLE=docs(nw008): AT-1 initialize edge access remediation plan — provider clarification required
PR_BODY=
## Summary

Planning-only artifact incorporating current official HighLevel endpoint,
client, location-attachment, authentication, and roadmap evidence while
narrowing provider clarification to the generic endpoint's unified
`describe_operation` toolset.

## Bindings

- PR83_REVIEWED_HEAD=c892b28fa026edc22c9670165648cb5dce3690fb
- PR83_MERGE_SHA=d93f4b418ed84a72c83a4b2ac07f06b4b4a5b922

## Decision outputs

- SUPPORTED_CLIENT_ENDPOINT_IDENTIFIED=YES
- GHL_MCP_ATTACHMENT_ARCHITECTURE_READY=YES
- GHL_MCP_RUNTIME_ACTIVATION_AUTHORIZED=NO
- PROVIDER_CLARIFICATION_REQUIRED=YES
- PROVIDER_CLARIFICATION_SCOPE=GENERIC_ENDPOINT_UNIFIED_TOOLSET_DESCRIBE_OPERATION
- NW008_FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO

## Scope

- No network, MCP, or implementation activity
- Planning-only; no authority consumed or created

## Artifact

- `docs/nw008/nw-008-at1-initialize-edge-access-remediation-plan-001.md`
```

## 9. Required state assertions

```text
PRIOR_OBSERVATION_AUTHORITY_CONSUMED=YES
NEW_OBSERVATION_AUTHORITY=NO
NETWORK_EXECUTION_AUTHORIZED=NO
PROVIDER_OUTPUT_BINDING_FROZEN=NO
COMPOSITE_CONTRACT_FREEZE_READY=NO
IMPLEMENTATION_CHANGE_AUTHORIZABLE=NO
```

## 10. STOP for reviewer disposition

This planning unit requires human review before any next step. Possible
dispositions:

1. **ACCEPT_AND_MERGE** — Merge planning artifact; proceed to provider
   clarification outreach.
2. **ACCEPT_WITH_NOTES** — Merge with reviewer amendments.
3. **REJECT_PLANNING_INCOMPLETE** — Identify missing analysis; revise before
   merge.
4. **REDIRECT_TO_ALTERNATE_STRATEGY** — Propose alternate remediation path
   (e.g., OAuth, different endpoint, abandon AT-1).

No further automated action until reviewer disposition is recorded.

```text
NEXT=HUMAN_REVIEW_DISPOSITION
```
