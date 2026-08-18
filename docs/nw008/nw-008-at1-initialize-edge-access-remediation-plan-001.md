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

## 3. Endpoint and client matrix (documented evidence)

### 3.1 Documented endpoints

From PR #80 provider-output-authority-acquisition (`proof/nw008/nw-008-at1-provider-output-authority-acquisition-001.md`) section 4.1:

| Pattern | Status | Source |
| --- | --- | --- |
| `https://services.leadconnectorhq.com/mcp/{client}/v2` | Documented | LeadConnector MCP doc |
| `https://services.leadconnectorhq.com/mcp/anthropic/v2` | Live (for Claude-class clients) | LeadConnector MCP doc |
| `https://services.leadconnectorhq.com/mcp/` | Documented as original endpoint | LeadConnector MCP doc |

### 3.2 Prior observation surface

The consumed observation used:

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
TRANSPORT_CLASS=streamable_http_sse
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
TRANSPORT_CLIENT=python_urllib_stdlib (Python 3.9.6, default User-Agent)
```

The edge block attributed the rejection to "browser's signature" (`browser_signature_banned`), which correlates to the User-Agent or client fingerprint, not to the credential itself.

## 4. Planning questions and answers

### Q1. Is `/mcp/anthropic/v2` provider-supported for a custom Python/VS Code client, or only Claude-class clients?

**Answer: UNKNOWN**

- **Evidence for Claude-only**: The endpoint path contains `/anthropic/` which
  suggests it is intended for Anthropic/Claude clients. The Cloudflare error
  1010 blocking a Python `urllib` client with default User-Agent on this
  endpoint supports the hypothesis that client fingerprinting is enforced.
- **Evidence against Claude-only**: The MCP documentation does not explicitly
  state that `/mcp/anthropic/v2` rejects non-Anthropic clients. The
  documentation describes `/mcp/{client}/v2` as a pattern.
- **Gap**: No official HighLevel documentation defines which `{client}` values
  are supported, what User-Agent patterns are allowed, or whether a generic
  Python/VS Code client can use `/mcp/anthropic/v2`.

```text
Q1_ANSWER=UNKNOWN
Q1_EVIDENCE_QUALITY=INFERENCE_FROM_EDGE_BLOCK
Q1_PROVIDER_CLARIFICATION_REQUIRED=YES
```

### Q2. Is `/mcp/` the supported generic HTTP MCP endpoint for our current client?

**Answer: UNKNOWN**

- **Evidence**: The MCP documentation mentions `/mcp/` as the "original
  endpoint" that remains available. No PR #83-scope observation used `/mcp/`.
- **Gap**: No observation or documentation confirms that `/mcp/` accepts the
  same `streamable-http+sse` transport with PIT auth for a Python/VS Code
  client. The Cloudflare WAF configuration at `/mcp/` is not observable from
  merged evidence.

```text
Q2_ANSWER=UNKNOWN
Q2_EVIDENCE_QUALITY=DOC_MENTION_ONLY
Q2_ENDPOINT_PROBE_REQUIRED=YES
Q2_PROVIDER_CLARIFICATION_REQUIRED=YES
```

### Q3. Does `/mcp/` expose `describe_operation` and the five frozen AT-1 operations?

**Answer: UNKNOWN**

- **Evidence**: From PR #78 pregrant observation, the `/mcp/anthropic/v2`
  endpoint's `tools/list` advertised `execute_operation`, `describe_operation`,
  `search`, `fetch`, `search_operations`, and `list_locations`. The five frozen
  AT-1 operation IDs (`get-contact`, `get-opportunity`, `create-note`,
  `get-note`, `update-opportunity`) were confirmed present via `search_operations`
  in Grant008.
- **Gap**: No observation confirms `/mcp/` advertises the same tool catalog.
  Endpoint-specific tool catalogs cannot be assumed identical.

```text
Q3_ANSWER=UNKNOWN
Q3_EVIDENCE_QUALITY=INFERENCE_FROM_ALTERNATE_ENDPOINT
Q3_ENDPOINT_PROBE_REQUIRED=YES
```

### Q4. Does PIT provide the required catalog/scopes, or is OAuth required?

**Answer: PARTIAL (PIT confirmed sufficient for prior observations; OAuth not required but recommended by HighLevel)**

- **Evidence**: PR #77/PR #78 pregrant observation successfully initialized,
  completed `tools/list`, and captured the catalog using PIT + Bearer auth
  against `/mcp/anthropic/v2`. The MCP documentation states OAuth is
  "recommended" and PIT is "more limited" but does not enumerate specific
  catalog/scope differences.
- **Gap**: If endpoint changes (e.g., to `/mcp/`), PIT scope compatibility is
  not guaranteed. The PR #83 fail-closed stop was at the edge before PIT could
  be validated on the repeat attempt.

```text
Q4_ANSWER=PIT_SUFFICIENT_FOR_PRIOR_OBSERVATION
Q4_EVIDENCE_QUALITY=OBSERVED_PRIOR_SUCCESS_PLUS_DOC
Q4_OAUTH_REQUIRED_FOR_CURRENT_KNOWN_CATALOG=NO
Q4_OAUTH_REQUIRED_FOR_ALTERNATE_ENDPOINT=UNKNOWN
```

### Q5. Is a dedicated OpenAI/VS Code client endpoint now live or still roadmap-only?

**Answer: UNKNOWN**

- **Evidence**: The MCP documentation mentions `/mcp/{client}/v2` pattern.
  `/mcp/anthropic/v2` is documented and confirmed live. No `/mcp/openai/v2`,
  `/mcp/vscode/v2`, `/mcp/generic/v2`, or similar endpoint is mentioned in any
  merged source.
- **Gap**: No HighLevel documentation, changelog, or public repo source
  confirms the existence of a dedicated VS Code or OpenAI endpoint.

```text
Q5_ANSWER=UNKNOWN
Q5_EVIDENCE_QUALITY=NO_DOC_OR_REPO_EVIDENCE
Q5_PROVIDER_CLARIFICATION_REQUIRED=YES
```

### Q6. What exact endpoint, client identity, auth mode, protocol version, and transport behavior would a future authorization need to freeze?

**Answer: CANNOT_FREEZE (multiple unknowns)**

A future observation authorization would need to freeze:

| Parameter | Prior Value | Future Value | Status |
| --- | --- | --- | --- |
| Endpoint | `https://services.leadconnectorhq.com/mcp/anthropic/v2` | TBD | **BLOCKED** by edge ban |
| Client identity (User-Agent) | Python `urllib` default | TBD | **UNKNOWN** (provider-supported value unknown) |
| Auth mode | PIT + Bearer | TBD | Likely unchanged if endpoint allows |
| Protocol version | `2025-11-25` | `2025-11-25` | Frozen in PR #76 |
| Transport | `streamable-http+sse` | TBD | Endpoint-dependent |

```text
Q6_ANSWER=CANNOT_FREEZE_WITHOUT_PROVIDER_CLARIFICATION
Q6_ENDPOINT_FROZEN=NO
Q6_CLIENT_IDENTITY_FROZEN=NO
Q6_AUTH_MODE_FROZEN=LIKELY_UNCHANGED
Q6_PROTOCOL_VERSION_FROZEN=YES
Q6_TRANSPORT_FROZEN=NO
```

### Q7. Is HighLevel/provider clarification required before any new authorization?

**Answer: YES**

- The edge block explicitly cites "browser's signature" as the ban reason.
- No merged evidence establishes which client identities (User-Agent patterns)
  are provider-supported for MCP access.
- No merged evidence establishes whether `/mcp/` accepts non-Claude clients.
- No merged evidence establishes whether a dedicated non-Anthropic endpoint
  exists.

Without provider clarification, any new observation authorization would risk
consuming authority on another edge-blocked attempt, which would violate the
single-shot authority model.

```text
Q7_ANSWER=YES
Q7_CLARIFICATION_SCOPE=ENDPOINT_CLIENT_IDENTITY_USER_AGENT_PATTERN
```

## 5. Source matrix

| Source | Type | PR | SHA | Finding |
| --- | --- | --- | --- | --- |
| `proof/nw008/nw-008-at1-describe-operation-contract-observation-001.md` | Merged proof | #83 | `c892b28` | Edge block HTTP 403 error 1010 at `/mcp/anthropic/v2` |
| `proof/nw008/nw-008-at1-pregrant-mcp-contract-observation-001.md` | Merged proof | #78 | `b16f49c` | Prior successful initialize at `/mcp/anthropic/v2` |
| `proof/nw008/nw-008-at1-provider-output-authority-acquisition-001.md` | Merged proof | #80 | `023ddbb` | MCP doc endpoint patterns; no output schema authority |
| `proof/nw008/nw-008-at1-mcp-response-source-capture.md` | Merged proof | #76 | `262fc16` | MCP protocol version frozen `2025-11-25` |
| LeadConnector MCP doc (living) | Official doc | N/A | N/A | Endpoint patterns; PIT/OAuth; no client identity spec |
| Cloudflare error 1010 response | Transport evidence | #83 | N/A | `browser_signature_banned`; "Do not retry" |

## 6. Decision outputs

```text
SUPPORTED_CLIENT_ENDPOINT_IDENTIFIED=NO
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE=UNKNOWN
PIT_SUFFICIENT_FOR_REQUIRED_CATALOG=YES (for prior endpoint; unknown for alternatives)
OAUTH_REQUIRED_FOR_REQUIRED_CATALOG=NO (for prior endpoint; unknown for alternatives)
DEDICATED_VSCODE_OR_OPENAI_ENDPOINT_LIVE=UNKNOWN
PROVIDER_CLARIFICATION_REQUIRED=YES
FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO
```

## 7. Unknowns requiring provider clarification

| Unknown | Question for HighLevel |
| --- | --- |
| U1 | Which MCP endpoint(s) support non-Anthropic/non-Claude clients (e.g., custom Python/VS Code integrations)? |
| U2 | What User-Agent pattern(s) are allowed for MCP access without triggering Cloudflare WAF error 1010? |
| U3 | Is `/mcp/` available for custom clients with `streamable-http+sse` transport and PIT auth? |
| U4 | Is there a dedicated endpoint path (e.g., `/mcp/generic/v2`, `/mcp/vscode/v2`) for non-LLM-provider integrations? |
| U5 | Does the tool catalog (`describe_operation`, `execute_operation`, etc.) differ by endpoint? |

## 8. Proposed planning-only PR

```text
PR_TITLE=docs(nw008): AT-1 initialize edge access remediation plan — provider clarification required
PR_BODY=
## Summary

Planning-only artifact identifying endpoint/client/auth unknowns blocking
future NW008 AT-1 observation authorization.

## Bindings

- PR83_REVIEWED_HEAD=c892b28fa026edc22c9670165648cb5dce3690fb
- PR83_MERGE_SHA=d93f4b418ed84a72c83a4b2ac07f06b4b4a5b922

## Decision outputs

- SUPPORTED_CLIENT_ENDPOINT_IDENTIFIED=NO
- PROVIDER_CLARIFICATION_REQUIRED=YES
- FUTURE_OBSERVATION_AUTHORIZATION_DESIGNABLE=NO

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
