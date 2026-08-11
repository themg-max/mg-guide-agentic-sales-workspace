# New Work Ledger — All Things Agentic

**Repository:** `themg-max/mg-guide-agentic-sales-workspace`
**Competition:** Google All Things Agentic Hackathon
**Track target:** Fortified Enterprise Fleet
**Workflow:** `meeting_follow_up_v1`

This ledger tracks **competition-period deltas only**. Pre-existing MG MCP,
MG Guide, and OL3 governance concepts are baseline — not new-work claims.
See [`../docs/COMPETITION_BASELINE.md`](../docs/COMPETITION_BASELINE.md).

---

## Ledger entries

| ID | Date (UTC) | Item | Status | Notes |
| --- | --- | --- | --- | --- |
| NW-000 | 2026-08-11 | Public competition repository created | DONE | `themg-max/mg-guide-agentic-sales-workspace`, visibility PUBLIC |
| NW-001 | 2026-08-11 | Foundation docs, contracts, synthetic fixtures, competition logs | DONE | Bootstrap commit; not functional runtime |
| NW-009 | 2026-08-11 | Public sanitized governance binding sync | DONE | Branch `gov/private-adoption-binding-sync-20260811`; governance profile + schemas + boundary; no runtime |
| NW-002 | 2026-08-11 | Phase 1 deterministic contracts/fixtures/state-machine foundation (no AI, no GHL) | DONE | Branch `feat/meeting-follow-up-v1-phase1-contracts-fixtures`; synthetic sidecars; zero external effects |
| NW-010 | 2026-08-11 | Phase 1 deterministic CI workflow (pytest-only) | DONE | Auth `MG_GUIDE_PHASE1_CI_V1`; branch `chore/phase1-deterministic-ci`; no secrets; contents:read |
| NW-003 | 2026-08-11 | Phase 2A GHL MCP meta-discovery (tools/list + search/describe ops only) | DONE | Auth `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1`; PR #4; zero record reads; zero writes; PASS_WITH_BLOCKERS |
| NW-004 | TBD | ADK/Gemini agent implementation (Gemini 3.5+) | PLANNED | Four agents max per foundation; `GEMINI_ADK_STARTED=NO` |
| NW-005 | TBD | Firestore audit writer | PLANNED | `workflow_runs/{run_id}` |
| NW-006 | TBD | MG Guide Meeting Follow-Up card experience | PLANNED | Completed + needs-review states |
| NW-007 | TBD | Cloud Run deployment (test) | PLANNED | Requires activation authority; not part of foundation |
| NW-008 | TBD | Acceptance tests AT-1…AT-10 + demo proof | PLANNED | Synthetic data only |
| NW-011 | 2026-08-11 | Phase 1 deterministic CI workflow proof | DONE | Branch `chore/phase1-deterministic-ci`; Python-only deterministic verification; no secrets or runtime dependencies |
| NW-012 | TBD | Isolated GHL test-account record-read compatibility probe | PLANNED | Gated: `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1`; requires isolated binding + OL3 bridge + secret path; no writes; not started |

---

## Explicit non-claims

- Creating this repository does **not** claim MG MCP or OL3 as new inventions.
- Foundation contracts do **not** authorize production CRM writes.
- UNKNOWN GHL tool identifiers are intentional; inventing them is a ledger violation.
- NW-003 meta-discovery does **not** claim record-level read probes occurred (`GHL_RECORD_READS=0`).
- NW-012 is planned only; starting it requires a separate gated authorization after blockers clear.
- Phase 2B has **not** started (`PHASE2B_STARTED=NO`).
- Gemini/ADK has **not** started (`GEMINI_ADK_STARTED=NO`).

## Phase 1 deterministic CI PASS (PR #3)

- Date (UTC): 2026-08-11
- Authorization: MG_GUIDE_PHASE1_CI_V1
- Branch: chore/phase1-deterministic-ci
- PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/3
- Green PR workflow run (initial): https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531473115
- Head SHA at initial green run: 61c01a3152a072ebfaefa2ab97b0ab3124cea5ef
- Final verified head SHA: 69c9068ae21cf6606a3bcd9de6d82fedd611e242
- Final green PR workflow run: https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31535966409 (SUCCESS)
- Classification: competition-period new work (CI only; no product surface expansion)
- Ledger correction: duplicate ID NW-009 (CI workflow proof) renumbered to NW-011; NW-009 remains the governance binding sync entry

## Phase 2A GHL MCP meta-discovery (PR #4 / NW-003)

- Date (UTC): 2026-08-11
- Authorization: MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1
- Branch: feat/meeting-follow-up-v1-ghl-mcp-read-discovery
- PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/4
- Classification: competition-period new work (meta-discovery/contract only; zero CRM mutations; zero record probes)
- Mode: READ_ONLY_META_DISCOVERY (`tools/list`, `search_operations`, `describe_operation`)
- Baseline after refresh: `main` @ `2f0742f8ac161081810db2e62963afe89d15fc42`
- Verified head (green CI): `8018533ac2f12f5f6299c5325bbb9e4ad4a106a2`
- Green PR workflow run: https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31540519394 (SUCCESS)
- Outcomes: manifest updated; proof/phase2 captured; hard-stop note/stage ops discovered on anthropic_v2 catalog
- Preserved posture: `GHL_RECORD_READS=0`, `GHL_WRITES=0`, `PHASE2B_STARTED=NO`, `GEMINI_ADK_STARTED=NO`
- Blocker: `ISOLATED_HACKATHON_TEST_ACCOUNT_BINDING_REQUIRED`
- Next planned ID: NW-012 (isolated test-account record-read compatibility probe) — **not started**
- Next gated capability (blocked): `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1`
