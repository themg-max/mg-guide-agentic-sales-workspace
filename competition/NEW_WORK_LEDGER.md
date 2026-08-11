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
| NW-003 | TBD | GHL MCP live discovery against test account | PLANNED | Resolve all UNKNOWN tool rows or STOP |
| NW-004 | TBD | ADK/Gemini agent implementation (Gemini 3.5+) | PLANNED | Four agents max per foundation |
| NW-005 | TBD | Firestore audit writer | PLANNED | `workflow_runs/{run_id}` |
| NW-006 | TBD | MG Guide Meeting Follow-Up card experience | PLANNED | Completed + needs-review states |
| NW-007 | TBD | Cloud Run deployment (test) | PLANNED | Requires activation authority; not part of foundation |
| NW-008 | TBD | Acceptance tests AT-1…AT-10 + demo proof | PLANNED | Synthetic data only |
| NW-009 | 2026-08-11 | Phase 1 deterministic CI workflow proof | DONE | Branch `chore/phase1-deterministic-ci`; Python-only deterministic verification; no secrets or runtime dependencies |

---

## Explicit non-claims

- Creating this repository does **not** claim MG MCP or OL3 as new inventions.
- Foundation contracts do **not** authorize production CRM writes.
- UNKNOWN GHL tool identifiers are intentional; inventing them is a ledger violation.

## Phase 1 deterministic CI PASS (PR #3)

- Date (UTC): 2026-08-11
- Authorization: MG_GUIDE_PHASE1_CI_V1
- Branch: chore/phase1-deterministic-ci
- PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/3
- Green PR workflow run: https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531473115
- Head SHA at green run: 61c01a3152a072ebfaefa2ab97b0ab3124cea5ef
- Classification: competition-period new work (CI only; no product surface expansion)
