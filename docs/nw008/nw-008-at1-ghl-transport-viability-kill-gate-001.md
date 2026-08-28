# NW-008 AT-1 — GHL Transport Viability Kill Gate 001

## 1. Identity and authority boundary

```text
ARTIFACT_ID=NW008_AT1_GHL_TRANSPORT_VIABILITY_KILL_GATE_001
ARTIFACT_PATH=docs/nw008/nw-008-at1-ghl-transport-viability-kill-gate-001.md
PR_CLASS=planning_only
OWNER=VS_CODE_ORCHESTRATOR_PLANNING_GOVERNANCE_LANE

PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=c903adfbf41e5ccb489f616dd59665ef965890e6
PLAN_BRANCH=plan/nw008-at1-ghl-transport-viability-kill-gate-001
BRANCH_IS_MAIN=NO

PLANNING_DESIGN_CLOSURE_ONLY=YES
IMPLEMENTATION_IN_SCOPE=NO
MCP_NETWORK_CALLS=0
REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NEW_MCP_CONNECTIVITY_PROBE_AUTHORIZED=NO
NEW_GRANT_PREPARATION_READY=NO
LIVE_EXECUTION_AUTHORIZED=NO
SUBMISSION_READY=NO
```

This unit closes the competition transport decision for HighLevel (GHL)
connectivity. It evaluates whether the HighLevel MCP path remains viable for
the current competition runtime under fail-closed predicates, using only
already-merged authoritative planning and proof artifacts. It does not
implement adapters, probe MCP, call REST, mutate CRM, freeze a new provider
contract, or prepare a grant.

Merging or reviewing this kill gate confers no implementation, network,
control-plane, grant-preparation, or live-execution authority.

## 2. Controlling history

```text
PR259_MERGED=YES
PR259_MERGE_SHA=f1d09f597dff7623fa44d70ccdf706287a384d34
PR259_TITLE=proof(nw008): close Grant 001 pre-claim session stop

PR260_MERGED=YES
PR260_MERGE_SHA=c903adfbf41e5ccb489f616dd59665ef965890e6
PR260_TITLE=docs(nw008): freeze established-session response seam contract

GRANT_ID=NW008_FRESH_ONE_SHOT_GHL_GRANT_001
GRANT001_TERMINAL=YES
GRANT001_REUSABLE=NO
GRANT001_CONSUMED=NO

EXECUTION_PHASE_REACHED=PRECLAIM_SESSION_GATE
E2E_EXECUTION_OCCURRED=NO
FAILURE_CLASS=ESTABLISHED_SESSION_UNAVAILABLE
BUSINESS_EFFECT_TRUTH=NO
```

Authority for Grant 001 disposition remains the merged PR #259 execution-proof
and the PR #260 established-session response-seam closure. Terminal closure
makes the grant non-reusable and bars retry or reinstantiation. Historical
`GRANT_CONSUMED=NO` is unchanged: the attempt stopped before claim acquisition
and before any GHL business call.

## 3. Source-authority disposition (current clients and endpoints)

Recorded from already-merged offline authority only. No new MCP network call
was made to overturn or refresh these dispositions.

```text
HIGHLEVEL_FULL_V2_EXECUTE_OPERATION_ENDPOINT_CURRENT_CLIENT=CLAUDE
OPENAI_CODEX_V2_ENDPOINT_CURRENT_STATE=PLANNED
VS_CODE_V2_ENDPOINT_CURRENT_STATE=PLANNED

GENERIC_MCP_ENDPOINT=
  https://services.leadconnectorhq.com/mcp/
GENERIC_MCP_ENDPOINT_SUPPORTS_HTTP_CLIENTS=YES
GENERIC_MCP_ENDPOINT_COVERAGE=NARROWER
GENERIC_MCP_EXECUTE_OPERATION_CONTRACT_STATICALLY_PROVEN=NO

PER_CLIENT_V2_PATTERN=
  https://services.leadconnectorhq.com/mcp/{client}/v2
ANTHROPIC_V2_ENDPOINT=
  https://services.leadconnectorhq.com/mcp/anthropic/v2
ANTHROPIC_V2_DESIGNATED_CLIENT=CLAUDE
ANTHROPIC_V2_PROVIDER_DESIGNATED_FOR_CURRENT_CLIENT=NO

DEDICATED_OPENAI_ENDPOINT_LIVE=NO
DEDICATED_VSCODE_ENDPOINT_LIVE=NO
DEDICATED_ENDPOINT_STATUS=ROADMAP
```

Primary offline sources:

| Source | Binding used here |
| --- | --- |
| `docs/nw008/nw-008-at1-initialize-edge-access-remediation-plan-001.md` | Claude-only Anthropic v2 designation; generic `/mcp/` for custom HTTP clients; OpenAI/VS Code v2 roadmap; generic `describe_operation` / unified toolset UNKNOWN; generic execute contract not statically proven |
| `docs/nw008/nw-008-at1-established-session-and-response-contract-closure-001.md` (PR #260) | Endpoint candidates unselected; response contract unfrozen; session seam not implemented; PR260 seam requires exact request preservation and no response reconstruction |
| `docs/nw008/nw-008-at1-highlevel-provider-clarification-request-001.md` | Provider Qs on generic control-plane tools still unresolved at answer level |
| `docs/nw008/nw-008-at1-highlevel-provider-clarification-submission-001.md` | Ticket submitted; provider answer not captured or reconciled |
| `docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md` + `contracts/highlevel_rest_adapter_v1.yaml` (PR #93 lineage) | Existing bounded HighLevel REST v3 architecture and contract |

```text
PROVIDER_RESPONSE_CAPTURED=NO
PROVIDER_RESPONSE_RECONCILED=NO
PROVIDER_INPUT_CONTRACT_AUTHORITY_IDENTIFIED=NO
PROVIDER_OUTPUT_CONTRACT_AUTHORITY_IDENTIFIED=NO
GENERIC_ENDPOINT_EXECUTE_OPERATION_AVAILABLE=UNKNOWN
GENERIC_ENDPOINT_DESCRIBE_OPERATION_AVAILABLE=UNKNOWN
MCP_RESPONSE_CONTRACT_CURRENT_STATE=NOT_FROZEN
SESSION_SEAM_RESPONSE_LEVEL_FROZEN=NO
ENDPOINT_PROFILE_READY=NO
CLIENT_PROFILE_READY=NO
PROVIDER_RESPONSE_CONTRACT_READY=NO
```

## 4. Competition MCP kill criteria

MCP may remain the current competition transport only if **all** predicates
below are `YES`. Evaluation is offline and fail-closed: any `NO` or `UNKNOWN`
kills the current competition MCP path.

### 4.1 Predicate matrix

| Predicate | Value | Basis (offline) |
| --- | --- | --- |
| `CURRENT_RUNTIME_OFFICIALLY_SUPPORTED_BY_SELECTED_HIGHLEVEL_MCP_ENDPOINT` | **NO** | Full v2 `execute_operation` surface is designated for Claude (`/mcp/anthropic/v2`). Current competition runtime is VS Code / custom HTTP MCP client, not Claude. OpenAI Codex and VS Code dedicated v2 endpoints remain `PLANNED` / roadmap. Generic `/mcp/` is documented for custom HTTP clients but is not a selected, proven PR260-compatible full-v2 business seam. |
| `SELECTED_ENDPOINT_EXPOSES_REQUIRED_BUSINESS_EXECUTION_SEAM` | **UNKNOWN** | No endpoint profile is selected post-PR260. Generic endpoint `execute_operation` availability and contract are not statically proven. Anthropic v2 catalog observations are not transferable by assumption. |
| `EXACT_CONTACT_READ_CAPABILITY_VERIFIED` | **UNKNOWN** | Required exact contact read not verified on a current-runtime-supported, selected MCP endpoint under PR260 seam rules. |
| `EXACT_OPPORTUNITY_READ_CAPABILITY_VERIFIED` | **UNKNOWN** | Same gap for exact opportunity read. |
| `CREATE_NOTE_CAPABILITY_VERIFIED` | **UNKNOWN** | Same gap for create-note. |
| `EXACT_CREATED_NOTE_READBACK_CAPABILITY_VERIFIED` | **UNKNOWN** | Same gap for exact created-note readback. |
| `UPDATE_OPPORTUNITY_STAGE_CAPABILITY_VERIFIED` | **UNKNOWN** | Same gap for stage update. |
| `SESSION_RESPONSE_LEVEL_COMPATIBLE_WITH_PR260_SEAM` | **UNKNOWN** | PR260 left `SESSION_SEAM_RESPONSE_LEVEL` blank/unfrozen; adapter JSON-RPC envelope expectation is not provider authority. |
| `REQUEST_ID_PRESERVATION_COMPATIBLE` | **UNKNOWN** | Wire request-id preservation required by PR260; not proven for any selected current-runtime endpoint. |
| `RESPONSE_RECONSTRUCTION_REQUIRED` | **UNKNOWN** | PR260 forbids reconstruction (`RESPONSE_RECONSTRUCTION_ALLOWED=NO`) but does not prove reconstruction is unnecessary on a viable current endpoint. Fail-closed: cannot assert `NO`. |
| `CLIENT_SPECIFIC_RUNTIME_SUBSTITUTION_REQUIRED` | **YES** | Using Anthropic v2 for a non-Claude current runtime would require client-specific runtime substitution the provider does not designate. Dedicated OpenAI/VS Code v2 endpoints are not live. |
| `ARCHITECTURE_REDESIGN_REQUIRED` | **YES** | PR260 MCP composition (`At1EstablishedMcpSession` → live transport adapter/serializer → bounded executor) is not implemented; response contract unfrozen; current runtime lacks an officially supported full-v2 execute seam. Remaining on MCP for competition would require redesign or unproven generic-endpoint assumptions. |
| `PROVIDER_CONTRACT_SUFFICIENT_FOR_IMPLEMENTATION` | **NO** | Composite MCP response contract unfrozen; provider clarification unanswered; generic execute/describe contracts not statically proven. |

Normalized kill-gate predicate block:

```text
CURRENT_RUNTIME_OFFICIALLY_SUPPORTED_BY_SELECTED_HIGHLEVEL_MCP_ENDPOINT=NO

SELECTED_ENDPOINT_EXPOSES_REQUIRED_BUSINESS_EXECUTION_SEAM=UNKNOWN

EXACT_CONTACT_READ_CAPABILITY_VERIFIED=UNKNOWN
EXACT_OPPORTUNITY_READ_CAPABILITY_VERIFIED=UNKNOWN
CREATE_NOTE_CAPABILITY_VERIFIED=UNKNOWN
EXACT_CREATED_NOTE_READBACK_CAPABILITY_VERIFIED=UNKNOWN
UPDATE_OPPORTUNITY_STAGE_CAPABILITY_VERIFIED=UNKNOWN

SESSION_RESPONSE_LEVEL_COMPATIBLE_WITH_PR260_SEAM=UNKNOWN

REQUEST_ID_PRESERVATION_COMPATIBLE=UNKNOWN

RESPONSE_RECONSTRUCTION_REQUIRED=UNKNOWN

CLIENT_SPECIFIC_RUNTIME_SUBSTITUTION_REQUIRED=YES

ARCHITECTURE_REDESIGN_REQUIRED=YES

PROVIDER_CONTRACT_SUFFICIENT_FOR_IMPLEMENTATION=NO
```

### 4.2 Kill-gate result

Because one or more predicates are `NO` or `UNKNOWN`, the competition MCP path
fails the current-runtime viability gate.

```text
MCP_KILL_GATE_RESULT=FAIL_CURRENT_COMPETITION_RUNTIME
MCP_COMPETITION_PATH=STOP
MCP_TECHNOLOGY_REJECTED_PERMANENTLY=NO
MCP_POST_COMPETITION_RESEARCH=RETAIN
NEW_MCP_CONNECTIVITY_PROBE_AUTHORIZED=NO
```

Interpretation:

- **STOP** applies only to the **current competition** MCP transport path.
- MCP is **not** permanently rejected as a technology or post-competition
  architecture candidate.
- No new MCP connectivity probe is authorized by this artifact to try to
  overturn the planning result.

## 5. REST fallback decision

With the competition MCP path stopped, the existing bounded HighLevel REST v3
architecture becomes the competition transport.

```text
REST_FALLBACK_ACTIVATED=YES
COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3

EXISTING_REST_ARCHITECTURE_PRESENT=YES
EXISTING_REST_ARCHITECTURE_ARTIFACT=
  docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
EXISTING_REST_CONTRACT_PRESENT=YES
EXISTING_REST_CONTRACT_ARTIFACT=
  contracts/highlevel_rest_adapter_v1.yaml

REST_GENERIC_REQUEST_API_ALLOWED=NO
REST_GENERIC_EXECUTE_ALLOWED=NO
REST_SEARCH_ALLOWED=NO
REST_LIST_ALLOWED=NO

REST_SYNTHETIC_ONLY=YES
REST_EXACT_ID_ONLY=YES
REST_PRIVATE_BINDING_REQUIRED=YES

CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM
BROAD_SEARCH_AUTHORIZED=NO
LIST_PAGINATION_EXPANSION_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO
```

This decision **selects** the already-defined REST architecture as the
competition transport target. It does **not** authorize implementation work
beyond what separate governance already allowed historically, does not
authorize live reads or mutations, and does not authorize any business call.

## 6. REST current operation surface

The intended bounded routes remain exactly the five exact-ID method/path pairs
from the REST architecture and contract. Confirmed:

```text
GET /contacts/{contactId}
GET /opportunities/{opportunityId}
POST /contacts/{contactId}/notes
GET /contacts/{contactId}/notes/{noteId}
PUT /opportunities/{opportunityId}
GET /opportunities/{opportunityId}
```

Notes on surface confirmation:

- Domain allowlist in the architecture table is five rows; opportunity GET is
  reused for preflight and post-update readback (listed twice above for
  clarity of both uses).
- `contactId` / `opportunityId` inject from private allowlist only.
- `noteId` comes only from the same-run successful note POST.
- No query strings, redirects, search, list, batch, generic execute, or
  arbitrary URL APIs.
- Adapter domain API must not expose HTTP client, `execute`, `request`,
  `search`, `list`, or pass-through operations.

```text
NO_BUSINESS_CALL_AUTHORIZED_BY_THIS_ARTIFACT=YES
REST_ADAPTER_EXECUTION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
```

## 7. Path readiness and historical stage blocker

Do not silently remove the historical stage-path blocker. Preserve and restate
it, then require explicit revalidation under the REST competition path.

```text
NOTE_PATH_ARCHITECTURE_READY=YES
REST_NOTE_PATH_CURRENT_STATE=ARCHITECTURE_READY_IMPLEMENTATION_NOT_REAUTHORIZED_HERE

STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_BLOCKER=
MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
REST_STAGE_PATH_CURRENT_STATE=BLOCKED_MINIMUM_VALID_UPDATE_BODY_UNRESOLVED

REST_STAGE_PATH_REVALIDATION_REQUIRED=YES
```

Contract mirror (`contracts/highlevel_rest_adapter_v1.yaml`):

```text
path_readiness.NOTE_PATH_ARCHITECTURE_READY=true
path_readiness.STAGE_PATH_ARCHITECTURE_READY=false
path_readiness.STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
provider_operations.get_opportunity.runtime_enabled=false
provider_operations.update_opportunity_stage.runtime_enabled=false
```

Next artifact after this kill gate:

```text
ARTIFACT_ID=
NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001
```

That unit's job is to compare **current authoritative HighLevel REST v3**
`Get Opportunity` and `Update Opportunity` contracts against the historical
stage blocker `MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED`. It remains
planning/contract reconciliation only unless separately authorized otherwise.

## 8. MCP re-entry criteria (post-competition / future architecture)

Preserve MCP as a future architecture candidate. Competition re-entry remains
closed until an explicit re-entry predicate is satisfied.

```text
MCP_REENTRY_IF_OPENAI_CODEX_V2_OFFICIALLY_AVAILABLE=YES
MCP_REENTRY_IF_VSCODE_V2_OFFICIALLY_AVAILABLE=YES
MCP_REENTRY_IF_GENERIC_ENDPOINT_PROVES_PR260_COMPATIBLE_WITHOUT_REDESIGN=YES

MCP_COMPETITION_REENTRY_UNTIL_THEN=NO
MCP_TECHNOLOGY_REJECTED_PERMANENTLY=NO
MCP_POST_COMPETITION_RESEARCH=RETAIN
```

Re-entry still requires separate governance: frozen composite response
contract, selected endpoint profile, sealed session seam compatible with
PR260, and any required grants. This kill gate does not pre-authorize those
steps.

## 9. Boundaries and forbidden actions

```text
IMPLEMENTATION_IN_SCOPE=NO
MCP_NETWORK_CALLS=0
REST_NETWORK_CALLS=0
LIVE_GHL_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO
LIVE_EXECUTION_AUTHORIZED=NO
SUBMISSION_READY=NO
NEW_MCP_CONNECTIVITY_PROBE_AUTHORIZED=NO
ENDPOINT_PROBE=FORBIDDEN
MCP_INITIALIZE=FORBIDDEN
MCP_TOOLS_LIST=FORBIDDEN
MCP_SEARCH_OPERATIONS=FORBIDDEN
MCP_DESCRIBE_OPERATION=FORBIDDEN
MCP_EXECUTE_OPERATION=FORBIDDEN
RAW_REST_BUSINESS_CALL=FORBIDDEN
OAUTH_OR_PIT_CHANGE=FORBIDDEN
IAM_SECRET_CHANGE=FORBIDDEN
DEPLOY_CHANGE=FORBIDDEN
```

This artifact must not be read as:

- authorization to implement `At1EstablishedMcpSession` or REST runtime code;
- authorization to probe generic or client-specific MCP endpoints;
- authorization to issue HighLevel REST calls;
- consumption or reissue of Grant 001;
- clearance of `STAGE_PATH_BLOCKER` without the reconciliation unit.

## 10. Decision summary

```text
COMPETITION_TRANSPORT_DECISION=BOUNDED_HIGHLEVEL_REST_V3
MCP_KILL_GATE_RESULT=FAIL_CURRENT_COMPETITION_RUNTIME
MCP_COMPETITION_PATH=STOP
MCP_POST_COMPETITION_RESEARCH=RETAIN
REST_FALLBACK_ACTIVATED=YES

REST_NOTE_PATH_CURRENT_STATE=ARCHITECTURE_READY_IMPLEMENTATION_NOT_REAUTHORIZED_HERE
REST_STAGE_PATH_CURRENT_STATE=BLOCKED_MINIMUM_VALID_UPDATE_BODY_UNRESOLVED
REST_STAGE_PATH_REVALIDATION_REQUIRED=YES

NEXT=NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001
STOP_CODE=NW008_AT1_GHL_TRANSPORT_VIABILITY_KILL_GATE_001_COMPLETE_OFFLINE
```

## 11. Required return block

```text
ARTIFACT_ID=NW008_AT1_GHL_TRANSPORT_VIABILITY_KILL_GATE_001

BASE_SHA=c903adfbf41e5ccb489f616dd59665ef965890e6
PR_NUMBER=
HEAD_SHA=

MCP_KILL_GATE_RESULT=FAIL_CURRENT_COMPETITION_RUNTIME
MCP_COMPETITION_PATH=STOP
MCP_POST_COMPETITION_RESEARCH=RETAIN

REST_FALLBACK_ACTIVATED=YES
COMPETITION_GHL_TRANSPORT=BOUNDED_HIGHLEVEL_REST_V3

EXISTING_REST_ARCHITECTURE_PRESENT=YES
EXISTING_REST_CONTRACT_PRESENT=YES

REST_NOTE_PATH_CURRENT_STATE=ARCHITECTURE_READY_IMPLEMENTATION_NOT_REAUTHORIZED_HERE
REST_STAGE_PATH_CURRENT_STATE=BLOCKED_MINIMUM_VALID_UPDATE_BODY_UNRESOLVED
REST_STAGE_PATH_REVALIDATION_REQUIRED=YES

LIVE_GHL_CALLS=0
MCP_NETWORK_CALLS=0
CRM_MUTATIONS=0

NEW_GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO

NEXT=NW008_AT1_GHL_REST_V3_STAGE_CONTRACT_RECONCILIATION_001
STOP_CODE=NW008_AT1_GHL_TRANSPORT_VIABILITY_KILL_GATE_001_COMPLETE_OFFLINE
```

`PR_NUMBER` and `HEAD_SHA` are filled by the planning PR submission that
carries this artifact. Return that PR to ChatGPT for review before any
implementation, MCP probe, REST call, or new grant preparation.
