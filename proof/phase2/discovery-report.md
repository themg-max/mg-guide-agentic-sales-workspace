# Phase 2A — GHL MCP Read Discovery Report

| Field | Value |
| --- | --- |
| Authorization ID | `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1` |
| Status | APPROVED (human, 2026-08-11) |
| Mode | READ ONLY — meta discovery |
| Workflow | `meeting_follow_up_v1` |
| Branch | `feat/meeting-follow-up-v1-ghl-mcp-read-discovery` |
| Baseline | Phase 1 merge `47deaae2820720b629eafe3ffec8c21245f4dfcb` |
| Recorded at (UTC) | 2026-08-11T20:20:00Z |

## Scope exercised

| Action | Status |
| --- | --- |
| MCP initialize | PASS (both endpoints) |
| tools/list | PASS |
| search_operations | PASS (anthropic_v2) |
| describe_operation | PASS (key ops) |
| execute_operation | NOT EXERCISED |
| search / fetch record tools | NOT EXERCISED |
| note_create execution | FORBIDDEN / not run |
| opportunity stage update execution | FORBIDDEN / not run |
| raw GHL REST | FORBIDDEN / not run |
| Gemini / ADK | FORBIDDEN / not run |

## Endpoints observed

### Original MCP
- URL: `https://services.leadconnectorhq.com/mcp/`
- serverInfo: `{name: ghl-mcp, version: 1.0.0}`
- tools/list count: **36** discrete tools
- **No** first-class note create/get tools under this PIT grant

### Anthropic v2 (recommended)
- URL: `https://services.leadconnectorhq.com/mcp/anthropic/v2`
- serverInfo: `{name: ghl-mcp, version: 1.0.0}`
- tools/list count: **6** unified tools:
  - `search`
  - `fetch`
  - `search_operations`
  - `describe_operation`
  - `execute_operation`
  - `list_locations`

## Auth observations

- Mode used: Private Integration Token via `Authorization: Bearer <PIT>`
- Raw token without `Bearer` → `401 invalid_token`
- Python `urllib` default UA → Cloudflare **403 Error 1010** (browser signature banned)
- `curl` + normal browser User-Agent → PASS
- Optional `locationId` header accepted
- OAuth not exercised

## Environment / isolation

| Item | Result |
| --- | --- |
| Required environment | isolated / hackathon test GHL account only |
| Available secret | `GHL_MCP_PRIVATE_TOKEN` in GCP project `ai-rolodex-to-crm` |
| Location binding | canonical MG Guide location exists in private config |
| Proven hackathon isolation | **NO** |
| Production CRM record reads | **NOT PERFORMED** |

**Blocker:** bind an explicit isolated test location + PIT before any record-level probes or later mutation phases.

## Capability mapping (LIVE meta)

| Logical capability | Exact operation | Scopes | Surface |
| --- | --- | --- | --- |
| Contact search | `search-contacts-advanced` (+ `get-duplicate-contact`) | `contacts.readonly` | anthropic_v2 `execute_operation` |
| Contact fetch | `get-contact` | `contacts.readonly` | anthropic_v2 / original `contacts_get-contact` |
| Opportunity search | `search-opportunity` (+ advanced) | `opportunities.readonly` | anthropic_v2 / original |
| Pipeline/stage metadata | `get-pipelines` | `opportunities.readonly` | anthropic_v2 / original |
| Mutation readback (note) | `get-note` / `get-all-notes` | `contacts.readonly` | anthropic_v2 catalog |
| Mutation readback (opp) | `get-opportunity` | `opportunities.readonly` | both |
| Note create (future) | `create-note` | `contacts.write` | **anthropic_v2 only** |
| Stage update (future) | `update-opportunity` (`pipelineStageId`) | `opportunities.write` | both |

## Hard-stop evaluation

| Rule | Result |
| --- | --- |
| note_create discoverable | **PASS** on anthropic_v2 (`create-note`) |
| opportunity_stage_update discoverable | **PASS** (`update-opportunity.pipelineStageId`) |
| original-only note path | **FAIL** (no first-class note tool) |
| Hard stop triggered for Phase 2A | **NO** (catalog discovery succeeded on recommended surface) |

## Intentionally unknown (record behavior)

Because production CRM data reads are forbidden without a proven test account:

- not-found response shapes
- ambiguous multi-match shapes
- live pagination cursors against real data
- rate-limit headers under load
- authorization denials for missing scopes against real ops
- concrete output JSON examples from live records

## Artifacts

- [`contracts/ghl_tool_manifest.yaml`](../../contracts/ghl_tool_manifest.yaml)
- [`proof/phase2/tools/`](./tools/)
- [`proof/phase2/operations/`](./operations/)
- [`proof/phase2/search-operations-by-intent.json`](./search-operations-by-intent.json)
- [`proof/phase2/proof-return.yaml`](./proof-return.yaml)

## Verdict

`PASS_WITH_BLOCKERS`

Next authorized step (separate grant): bind isolated hackathon test GHL location/PIT, complete record-level read behavior probes, then consider Phase 2B read-only vertical slice authorization.
