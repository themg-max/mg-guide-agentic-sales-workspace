# Phase 2A — GHL MCP Read Discovery Report

| Field | Value |
| --- | --- |
| Authorization ID | `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1` |
| Status | APPROVED (human, 2026-08-11) — meta-discovery complete; closeout pending human PR review |
| Mode | READ ONLY — meta discovery |
| Workflow | `meeting_follow_up_v1` |
| Branch | `feat/meeting-follow-up-v1-ghl-mcp-read-discovery` |
| PR | https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/4 |
| Baseline | `main` @ `2f0742f8ac161081810db2e62963afe89d15fc42` |
| Verified head (green CI) | `8018533ac2f12f5f6299c5325bbb9e4ad4a106a2` |
| Discovery content SHA | `6fa1c7d301dbbf94f27474b56e525bfa39d1f99a` |
| Recorded at (UTC) | 2026-08-11T20:20:00Z (discovery); 2026-08-11T22:15:00Z (closeout normalize) |

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

- Mode used: Private Integration Token via `Authorization: ******
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

**Blocker:** `ISOLATED_HACKATHON_TEST_ACCOUNT_BINDING_REQUIRED` — bind an explicit isolated test location + PIT before any record-level probes or later mutation phases.

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

**No record-level probes occurred in this phase.** Because production CRM data reads are forbidden without a proven isolated test account:

- not-found response shapes
- ambiguous multi-match shapes
- live pagination cursors against real data
- rate-limit headers under load
- authorization denials for missing scopes against real ops
- concrete output JSON examples from live records

## Preserved posture (closeout)

| Flag | Value |
| --- | --- |
| `GHL_RECORD_READS` | `0` |
| `GHL_WRITES` | `0` |
| `PHASE2B_STARTED` | `NO` |
| `GEMINI_ADK_STARTED` | `NO` |

## Artifacts

- [`contracts/ghl_tool_manifest.yaml`](../../contracts/ghl_tool_manifest.yaml)
- [`proof/phase2/tools/`](./tools/)
- [`proof/phase2/operations/`](./operations/)
- [`proof/phase2/search-operations-by-intent.json`](./search-operations-by-intent.json)
- [`proof/phase2/proof-return.yaml`](./proof-return.yaml)

## Closeout validation (PR #4 refresh)

| Check | Result |
| --- | --- |
| `PYTHONPATH=src python3 scripts/verify_phase1_deterministic.py` | PASS |
| `PYTHONPATH=src python3 -m pytest -q` | PASS |
| `git diff --check` | PASS |
| GitHub Actions `Phase 1 deterministic validation` on `8018533` | SUCCESS ([run 31540519394](https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31540519394)) |

## Verdict

`PASS_WITH_BLOCKERS`

Next gated capability (do **not** start until gates clear): `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1`

Gates required before that probe:

1. PR #4 meta-discovery closeout reviewed
2. Private OL3 bridge merged
3. Isolated GHL test account/location binding proven
4. Secret delivery path verified as already authorized, or a separate micro-grant approved

No GHL writes. No Phase 2B. No Gemini/ADK.
