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
| NW-004 | 2026-08-12 | Gemini/ADK vertical-slice unit 1 — Meeting Context Agent harness | IN_PROGRESS_UNIT1_COMPLETE | Grant `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1`; `GEMINI_ADK_AUTHORIZED=YES`; `GEMINI_ADK_STARTED=YES`; Meeting Context Agent + fixture harness green; structured context schema-valid; policy bypass=NO; EXTERNAL_EFFECTS=0; full vertical slice still open |
| NW-005 | TBD | Firestore audit writer | PLANNED | `workflow_runs/{run_id}` |
| NW-006 | TBD | MG Guide Meeting Follow-Up card experience | PLANNED | Completed + needs-review states |
| NW-007 | TBD | Cloud Run deployment (test) | PLANNED | Requires activation authority; not part of foundation |
| NW-008 | TBD | Acceptance tests AT-1…AT-10 + demo proof | PLANNED | Synthetic data only |
| NW-011 | 2026-08-11 | Phase 1 deterministic CI workflow proof | DONE | Branch `chore/phase1-deterministic-ci`; Python-only deterministic verification; no secrets or runtime dependencies |
| NW-012 | 2026-08-11 | Isolated GHL test-account record-read compatibility probe | NOT_PURSUIED_ENVIRONMENT_UNAVAILABLE | No isolated GHL hackathon/test location can be provided; path retired. Proposed `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1` never activated; zero record reads; zero writes |
| NW-013 | 2026-08-12 | Canonical GHL location synthetic-record read proof | AUTHORIZED_NOT_EXECUTED | Grant `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1`; human binding complete; `HUMAN_SIGNATURE=APPROVED`; `CURRENT_GRANT_STATE=AUTHORIZED_FOR_EXECUTION`; private allowlist complete (IDs not public); PIT canonical location verified; IAM change not required; branch `gov/mg-guide-ghl-canonical-synthetic-read-binding-v1`; **GHL_LIVE_CALLS=0**, **GHL_WRITES=0**; live reads still unexecuted |
| NW-014 | 2026-08-12 | Phase 2B offline GHL read adapter | DONE | Auth `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1` **CLOSED_SUCCESS**; PR #6 merged; head `075a3ea47dda02fdaffdc4390d4573f947959103`; merge `2b88240e1e023150449183b03c118b91d663cabc`; network_calls=0; crm_reads=0; crm_writes=0 |

---

## Explicit non-claims

- Creating this repository does **not** claim MG MCP or OL3 as new inventions.
- Foundation contracts do **not** authorize production CRM writes.
- UNKNOWN GHL tool identifiers are intentional; inventing them is a ledger violation.
- NW-003 meta-discovery does **not** claim record-level read probes occurred (`GHL_RECORD_READS=0`).
- NW-012 is retired (no isolated GHL hackathon/test location exists); the proposed `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1` was never activated and no record probes occurred.
- NW-013 is **human-authorized but not live-executed** (`AUTHORIZED_FOR_EXECUTION` / `AUTHORIZED_NOT_EXECUTED`). The canonical GHL location is **not** a test environment. Live reads remain deferred to a separate bounded unit under the private exact-ID allowlist (`GHL_LIVE_CALLS=0` on the binding unit).
- Phase 2B live GHL access has **not** started. NW-014 closed the offline adapter only (`network=NONE`); no live GHL claim is made by this closeout.
- Gemini/ADK implementation is **authorized and unit-1 started** under NW-004 (`NW004_STATUS=AUTHORIZED_FOR_IMPLEMENTATION`, `GEMINI_ADK_AUTHORIZED=YES`, `GEMINI_ADK_STARTED=YES` for Meeting Context Agent harness only; full vertical slice not complete).
- NW-004 does **not** authorize live GHL, GHL writes, real customer data, L3A promotion, Firestore writes, or deployment (`GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`).


## NW-004 Gemini/ADK vertical-slice authorization (AUTHORIZED_FOR_IMPLEMENTATION)

- Date (UTC): 2026-08-12
- Authorization: `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1`
- Status: **AUTHORIZED_FOR_IMPLEMENTATION** / **unit 1 Meeting Context Agent complete**
- Human decision: `AUTHORIZED_FOR_IMPLEMENTATION` / `HUMAN_SIGNATURE=APPROVED`
- Private source authority: PR https://github.com/themg-max/A.I-Rolodex---Context/pull/2964
- Private merge SHA: `7c3f605504956aa26faf62ce6db0552ba9abe494`
- Public artifacts: `governance/authorizations/MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1.yaml`
- Intended public implementation branch (after this sync merges): `feat/meeting-follow-up-v1-gemini-adk-vertical-slice`
- First unit: Meeting Context Agent fixture harness (synthetic transcript → schema-valid structured meeting context)
- Architecture (max four): Meeting Context Agent · Relationship Context Agent · Follow-Up Planning Agent · DETERMINISTIC POLICY GATE
- Allowed: Gemini/ADK (bounded test/dev), synthetic transcripts/CRM fixtures, Phase1 contracts, Phase2B offline adapter read/use, deterministic policy, tests, sanitized proof
- Denied: live GHL reads/writes, broad CRM search, real customer data, L3A promotion, Firestore writes, deployment, IAM/secret mutation, raw REST, authority expansion, policy bypass
- Assertions: `GEMINI_ADK_AUTHORIZED=YES`, `GEMINI_ADK_STARTED=YES`, `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_DATA=0`, `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
- Unit 1 delivered: Meeting Context Agent fixture harness (`src/agents/meeting_context/**`, `contracts/meeting_context.schema.json`, `tests/agents/**`, `proof/phase3/**`); structured context VALID; policy bypass NO; EXTERNAL_EFFECTS=0
- Completion bar (full vertical slice still open): valid packet output; deterministic policy authority preserved; SUCCESS / AMBIGUOUS / STAGE_DENIED fixtures pass; `EXTERNAL_EFFECTS=0`
- Next: STOP after unit 1 green; subsequent agents only in later reviewed units under the same grant


## NW-013 canonical synthetic-read binding (AUTHORIZED_NOT_EXECUTED)

- Date (UTC): 2026-08-12
- Authorization: `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1`
- Status: **AUTHORIZED_FOR_EXECUTION** / **AUTHORIZED_NOT_EXECUTED**
- Human approver: Aaron Chandler (repository maintainer / CRM operator)
- Human signature: `APPROVED` at `2026-08-12T02:02:01Z`
- Branch: `gov/mg-guide-ghl-canonical-synthetic-read-binding-v1`
- Public artifacts: `governance/authorizations/MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1.yaml`, `proof/canonical-synthetic-read-binding-v1/**`
- Assertions (public): `SYNTHETIC_CONTACT_BOUND=YES`, `SYNTHETIC_OPPORTUNITY_BOUND=YES`, `RELATIONSHIP_VERIFIED=YES`, `PRIVATE_ALLOWLIST_COMPLETE=YES`, `PIT_CANONICAL_LOCATION_VERIFIED=YES`, `IAM_CHANGE_REQUIRED=NO`
- Authorized ops (deferred live): `get-contact` MAX=1, `get-opportunity` MAX=1, `get-pipelines` metadata only
- Denied: broad searches, non-allowlisted IDs, all writes, email/SMS, raw REST, real customer reads
- Effects this unit: `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_RECORD_READS=0`
- Boundary: exact IDs and PIT/token values are **not** published in this repository
- Next: separate bounded live-read execution unit only after reviewer disposition on exact PR head; no authority expansion

## Phase 2B offline GHL read adapter (CLOSED_SUCCESS)

- Date (UTC): 2026-08-12
- Authorization: `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1`
- Status: **CLOSED_SUCCESS**
- Source PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/6 (MERGED)
- Head SHA: `075a3ea47dda02fdaffdc4390d4573f947959103`
- Merge SHA (verified on `main`): `2b88240e1e023150449183b03c118b91d663cabc`
- Classification: competition-period deterministic adapter work; synthetic fixtures only
- Scope delivered: request envelopes, contact/opportunity/pipeline-stage/pagination/error normalization, explicit read allowlist, explicit mutation denial, fixture replay, acceptance tests, and proof return
- Effects: `network_calls=0`, `crm_reads=0`, `crm_writes=0`
- Preserved posture: no live GHL/CRM access, no Gemini/ADK, no Firestore/Cloud Run/IAM/Secret Manager mutation
- Live-proof gate is now human-authorized but still unexecuted: `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1` / NW-013 = `AUTHORIZED_NOT_EXECUTED` after synthetic contact + opportunity binding, private exact-ID allowlisting, authorized secret path, PIT canonical-location verification, and explicit human activation (`HUMAN_SIGNATURE=APPROVED`). Binding unit performed zero live calls.

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

## Phase 2A closure + strategy adoption (2026-08-11)

- Date (UTC): 2026-08-11
- Authorization: human review (APPROVED, verdict READY_FOR_MERGE) + human merge of PR #4 by `Achandler21` at 2026-08-11T22:41:02Z
- Final PR head: `4587270c85d792fb9d503bac20d29351b6f0164d`
- Required check: Phase 1 Deterministic CI — SUCCESS (run 31541673310)
- **Merge SHA captured (verified on `main`):** `c00dd75c53ba91a17607d7c9f3b4f6e042173cd3`
- **Closed authorization:** `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1` (meta-discovery only; `GHL_RECORD_READS=0`, `GHL_WRITES=0` preserved)
- Strategy decision:
  - NW-012 → **NOT_PURSUIED_ENVIRONMENT_UNAVAILABLE** — no isolated GHL hackathon/test location can be provided; the isolated-test-account execution path is retired.
  - NW-013 → **PLANNED** — Canonical GHL location synthetic-record read proof. The canonical location is **not** classified as a test environment.
- New proposals (not activated):
  - `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1` — offline deterministic read adapter against Phase 2A discovered operation contracts; network NONE; synthetic fixtures only.
  - `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1` — `GATED_PENDING_SYNTHETIC_RECORD_BINDING`; exact-ID synthetic reads only; blocked on synthetic record binding + private allowlist + authorized secret path.
- Historical Phase 2A claims unchanged; this section adds no claim of live CRM access.
