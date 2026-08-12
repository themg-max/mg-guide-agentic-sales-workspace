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
| NW-004 | 2026-08-12 | Gemini/ADK vertical-slice units 1–3 — Meeting + Relationship + Follow-Up Planning | DONE | **CLOSED_SUCCESS**; grant `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1`; Unit 1 MERGED_COMPLETE (PR #10 / `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7`); Unit 2 MERGED_COMPLETE (PR #11 head `3ab0b1dfa0c2c20a711156d5cf88febb5d21dbfa` / merge `a3d5a5731d7342463fe365e597e5d974d3420d08`; final CI 31616758231 SUCCESS); Unit 3 MERGED_COMPLETE (PR #13 final reviewed head `32f13b6db0bfd9964001133d05f33d6ed294d0ba` / final exact-head CI 31623771005 SUCCESS / merge `91927e4cfeb5010cf399ae870ad0897156dff03e`; merged `2026-08-12T17:47:49Z`; impl evidence head `09c6a95dafa6e09f8244813e32a054aa27635d5c` / CI 31623557067); all six scenarios PASS, deterministic policy gate invoked, EXTERNAL_EFFECTS=0; no live GHL / no writes / no deployment |
| NW-005 | TBD | Firestore audit writer | PLANNED | `workflow_runs/{run_id}` |
| NW-006 | TBD | MG Guide Meeting Follow-Up card experience | PLANNED_NOT_STARTED | Planning packet only; completed + completed_with_review / blocked state handling; policy reason codes; proposed note/stage intents; next human action; no mutation controls; zero external effects; not started |
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
- Read-side GHL identifiers were discovered and governed in Phase 2A / NW-013; live canonical-location compatibility remains unexecuted, mutation capability remains separately governed, and inventing ungoverned identifiers remains a ledger violation. Raw REST fallback remains forbidden.
- NW-003 meta-discovery does **not** claim record-level read probes occurred (`GHL_RECORD_READS=0`).
- NW-012 is retired (no isolated GHL hackathon/test location exists); the proposed `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1` was never activated and no record probes occurred.
- NW-013 is **human-authorized but not live-executed** (`AUTHORIZED_FOR_EXECUTION` / `AUTHORIZED_NOT_EXECUTED`). The canonical GHL location is **not** a test environment. Live reads remain deferred to a separate bounded unit under the private exact-ID allowlist (`GHL_LIVE_CALLS=0` on the binding unit).
- Phase 2B live GHL access has **not** started. NW-014 closed the offline adapter only (`network=NONE`); no live GHL claim is made by this closeout.
- Gemini/ADK implementation is **authorized and closed** under NW-004 (`NW004_STATUS=DONE`, `NW004_CLOSEOUT_STATUS=CLOSED_SUCCESS`, `PHASE3_UNIT1_STATUS=MERGED_COMPLETE`, `PHASE3_UNIT2_STATUS=MERGED_COMPLETE`, `PHASE3_UNIT3_STATUS=MERGED_COMPLETE`, `GEMINI_ADK_AUTHORIZED=YES`). Unit 1 provider surface remains `COMPATIBLE_SURFACE_ONLY`. Unit 2 runtime truth: `GOOGLE_ADK_RUNTIME_STARTED=YES`, `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`. Unit 3 runtime truth: `FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED=YES`, `GOOGLE_ADK_RUNTIME_REUSED=YES`, `DETERMINISTIC_POLICY_GATE_INVOKED=YES`, `DETERMINISTIC_POLICY_BYPASS=NO`, `EXTERNAL_EFFECTS=0`. The remaining vertical-slice layers (mutation execution, Firestore audit, MG Guide card experience, and deployment) stay out of scope for this closeout and remain separately governed.
- NW-004 does **not** authorize live GHL, GHL writes, real customer data, L3A promotion, Firestore writes, or deployment (`GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`).


## NW-004 Gemini/ADK vertical-slice authorization (CLOSED_SUCCESS)

- Date (UTC): 2026-08-12
- Authorization: `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1`
- Status: **DONE / CLOSED_SUCCESS** / **Unit 1 MERGED_COMPLETE** / **Unit 2 MERGED_COMPLETE** / **Unit 3 MERGED_COMPLETE**
- Human decision: `AUTHORIZED_FOR_IMPLEMENTATION` / `HUMAN_SIGNATURE=APPROVED`
- Private source authority: PR https://github.com/themg-max/A.I-Rolodex---Context/pull/2964
- Private merge SHA: `7c3f605504956aa26faf62ce6db0552ba9abe494`
- Public artifacts: `governance/authorizations/MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1.yaml`
- Public Unit 1 implementation: PR #10 MERGED; merge SHA `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7`; branch `feat/meeting-follow-up-v1-gemini-adk-vertical-slice`
- Public Unit 2 implementation: PR #11 MERGED; head SHA `3ab0b1dfa0c2c20a711156d5cf88febb5d21dbfa`; merge SHA `a3d5a5731d7342463fe365e597e5d974d3420d08`; branch `feat/meeting-follow-up-v1-adk-relationship-context-unit2`; final CI run 31616758231 SUCCESS
- Public Unit 3 closeout: Follow-Up Planning Agent; branch `feat/meeting-follow-up-v1-follow-up-planning-agent-unit3`; PR #13 **MERGED**; final reviewed head `32f13b6db0bfd9964001133d05f33d6ed294d0ba`; final exact-head CI run **31623771005** SUCCESS; merge SHA `91927e4cfeb5010cf399ae870ad0897156dff03e`; merged `2026-08-12T17:47:49Z`; implementation evidence head `09c6a95dafa6e09f8244813e32a054aa27635d5c` / CI **31623557067** SUCCESS (preserved separately; not the final reviewed tip); proof `proof/phase3/unit3/proof-return.yaml`; closeout `proof/phase3/unit3/unit3-merge-closeout.md`; all six scenarios PASS; **NW-006 remains PLANNED / NOT_STARTED**
- Architecture (max four): Meeting Context Agent · Relationship Context Agent · Follow-Up Planning Agent · DETERMINISTIC POLICY GATE
- Allowed: Gemini/ADK (bounded test/dev), synthetic transcripts/CRM fixtures, Phase1 contracts, Phase2B offline adapter read/use, deterministic policy, tests, sanitized proof
- Denied: live GHL reads/writes, broad CRM search, real customer data, L3A promotion, Firestore writes, deployment, IAM/secret mutation, raw REST, authority expansion, policy bypass
- Unit 1 assertions (preserved): `GEMINI_PROVIDER_STARTED=YES`, provider-level `GOOGLE_ADK_RUNTIME_STARTED=NO`, `ADK_INTEGRATION_STATUS=COMPATIBLE_SURFACE_ONLY` on Meeting Context provider surface only
- Unit 2 assertions (merged): `GOOGLE_ADK_PACKAGE_BOUND=YES`, `GOOGLE_ADK_RUNTIME_STARTED=YES`, `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`, `ADK_RUNTIME_BACKEND=google_adk_package`, `ADK_RUNTIME_PRIMITIVE_USED=YES`, `LOCAL_ADK_FALLBACK_USED=NO`, `MEETING_CONTEXT_AGENT_REUSED=YES`, `RELATIONSHIP_CONTEXT_AGENT_IMPLEMENTED=YES`, `OFFLINE_GHL_ADAPTER_USED=YES`, `SYNTHETIC_CRM_CONTEXT_ONLY=YES`, `RELATIONSHIP_CONTEXT_OUTPUT=VALID`, `DETERMINISTIC_POLICY_BYPASS=NO`, `EXTERNAL_EFFECTS=0`, `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_DATA=0`, `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
- Unit 2 scenarios: `RELATIONSHIP_MATCH=PASS`, `AMBIGUOUS_CONTACT=PASS`, `NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT=PASS`, `AMBIGUOUS_OPPORTUNITY=PASS` (fail-closed: no selection, no stage target, review required)
- Unit 2 merge evidence: head `3ab0b1dfa0c2c20a711156d5cf88febb5d21dbfa`; merge `a3d5a5731d7342463fe365e597e5d974d3420d08`; final CI 31616758231 SUCCESS; pre-merge repair evidence head `5878c05a1881e4fde1c70ab1624704fdf8154ba4` / CI 31614783508 retained
- Unit 1 delivered: Meeting Context Agent fixture harness; structured context VALID; policy bypass NO; EXTERNAL_EFFECTS=0
- Unit 2 delivered: Google ADK runtime orchestration (`src/agents/adk_runtime/**`), Relationship Context Agent (`src/agents/relationship_context/**`), `contracts/relationship_context.schema.json`, synthetic CRM fixture, Unit 2 harness/tests, `proof/phase3/unit2/**`
- Explicit Unit 2 non-delivery: Follow-Up Planning Agent; full packet assembly; live GHL; L3A promotion; Firestore; deployment
- Unit 3 delivered proof (merged): `FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED=YES`, `MEETING_CONTEXT_REUSED=YES`, `RELATIONSHIP_CONTEXT_REUSED=YES`, `GOOGLE_ADK_RUNTIME_REUSED=YES`, `FOLLOW_UP_PROPOSAL_OUTPUT=VALID`, `DETERMINISTIC_POLICY_GATE_INVOKED=YES`, `DETERMINISTIC_POLICY_BYPASS=NO`, `EXTERNAL_EFFECTS=0`, `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
- Unit 3 scenarios (merged): `SUCCESS=PASS`, `AMBIGUOUS_CONTACT=PASS`, `AMBIGUOUS_OPPORTUNITY=PASS`, `NO_OPPORTUNITY=PASS`, `STAGE_CHANGE_DENIED=PASS`, `INSUFFICIENT_CONTEXT=PASS`
- Unit 3 delivered: Follow-Up Planning Agent (`src/agents/follow_up_planning/**`), `contracts/follow_up_proposal.schema.json`, synthetic fixtures for denied/insufficient paths, Unit 3 tests/harness, `proof/phase3/unit3/**`
- Explicit Unit 3 non-delivery: live GHL; CRM mutation execution; Firestore audit writer (NW-005); MG Guide card (NW-006); Cloud Run deployment (NW-007)
- Completion bar (full vertical slice still open beyond NW-004): mutation execution + audit + MG Guide card + deployment remain separately governed; agent/policy packet path for Units 1–3 is closed with `EXTERNAL_EFFECTS=0`
- Next: NW-006 MG Guide Meeting Follow-Up card remains **PLANNED / NOT_STARTED** (planning packet only at `proof/phase3/unit3/nw-006-meeting-follow-up-card-plan.md`); do **not** implement NW-006 in this closeout step


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
