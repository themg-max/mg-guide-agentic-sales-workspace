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
| NW-005 | 2026-08-13 | Firestore audit writer | STAGE_A_MERGED_COMPLETE / STAGE_B_SMOKE_PASS_COMPLETE | `workflow_runs/{run_id}`; required before honest AT-10. Stage A (offline `workflow_run_audit_v1` projection) **MERGED_COMPLETE**: PR #18 MERGED; final head `695bf3dcae3c9a82ef3af9be9cf264a669485939`; merge SHA `63aadc5c90569cfa119af7cc7e30fbac62f8544b`; merged_at `2026-08-13T01:15:44Z`. Stage B environment binding **COMPLETE** (PR #20); human execution authorization **APPROVED** (PR #22 merge `1d9ff931dd431ce04f47ad907b08252b433d23c9`; grant `MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1`); Wave 1 smoke **PASS** (PR #23; proof `proof/nw005/stage-b/nw005-persistence-proof-v1.md`). Current markers: `NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE`; `NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED`; `NW005_STAGE_B_SMOKE=PASS`. Stage B does **not** authorize AT-10 acceptance-demo (`ACCEPTANCE_DEMO_AUTHORIZED=NO`; `AT10_COMPLETION_CLAIM_AUTHORIZED=NO`). AT-10 is a separate NW-008 lane |
| NW-006 | 2026-08-12 | MG Guide Meeting Follow-Up card experience | MERGED_COMPLETE | PR #15 **MERGED**; final reviewed head `c7d25b447db0a961c17ae26e326ada230b7e4627`; exact-head CI **31630399411** SUCCESS; merge SHA `e22eb861442a37be0797d6d7aec8bb17001fb7a3`; merged_at `2026-08-12T19:12:33Z`; competition-local host-agnostic deterministic card renderer/reference component; no private host wiring; no mutation execution; `EXTERNAL_EFFECTS=0`; closeout `proof/nw006/nw-006-merge-closeout.md` |
| NW-007 | 2026-08-14 | Cloud Run deployment (test) + demo-grade decision card | MERGED_COMPLETE | PR #37 **MERGED** at `2026-08-14T09:35:35Z` via merge SHA `f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6`; final reviewed head `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76`. Governance closeout PR #38 **MERGED** at `2026-08-14T09:36:28Z` via merge SHA `89302057a7dddf2410f8aedbfb1f6c4e0ea88238`. Stage B2 deployment evidence exists, but `DEPLOYMENT_AUTHORIZATION=NO`. Decision-card implementation remains bounded and merged; `EXTERNAL_EFFECTS=0`; `POLICY_SEMANTICS_CHANGE=NO`; `PACKET_SCHEMA_CHANGE=NO`; `ADK_ORCHESTRATION_CHANGE=NO`; `NEW_AGENT=NO`; `NEW_LLM_CALL=NO`; application repair required `NO`; final closeout `proof/nw007/nw007-merge-closeout.md` |
| NW-008 | 2026-08-14 | Acceptance tests AT-1…AT-10 + demo proof | IN_PROGRESS (A+B+C+D1/D2 MERGED_COMPLETE; AT-10 ACCEPTANCE_DEMO_AUTHORIZATION) | Tranche A: PR #40 **MERGED** at `2026-08-14T11:30:36Z` via merge SHA `10347c709e86dfbca83cdf8c9ffd1a9a8491ce87`; final reviewed head `b61a4b02e0dae8c14701ccc8184c205d6bdcd29d`; purpose `DETERMINISTIC_ACCEPTANCE_EVIDENCE_SUBSTRATE`. Tranche B: PR #42 **MERGED** at `2026-08-14T13:06:06Z` via merge SHA `1ee6647d7e8284cb165c7ac8063582c6769d0a79`; final reviewed head `4da7e3fd25937e5cd90c241443ec1badbbf94e3b`; purpose `LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY`; `FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP=CLOSED`. Tranche C: PR #44 **MERGED_COMPLETE** at `2026-08-14T16:01:36Z` via merge SHA `36b0999dacee0dede9de355db28badbe38ed0581`; historical AT complete `AT-2,AT-4,AT-5`. Tranche D D1/AT-9: PR #48 **MERGED_COMPLETE**; D2/AT-8: PR #49 merge `d9f6a9bbca30c0c4419bd34e74588d98b072a641` + D2 governance closeout PR #50 merge `8f7fdd482c03dfee5e75159054d9ddf11dd793fe`; `AT8_STATUS=HISTORICAL_COMPLETE`; `AT9_STATUS=HISTORICAL_COMPLETE`. Current markers: `NW008_HISTORICAL_AT_COMPLETE=AT-2,AT-4,AT-5,AT-8,AT-9`; `NW008_HISTORICAL_AT_REMAINING=AT-1,AT-3,AT-6,AT-7,AT-10`; `AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION`; `AT10_EXECUTION_AUTHORIZED=NO`; `CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION`; NW-005 Stage B is **not** the active blocker (`NW005_STAGE_B_SMOKE=PASS`). AT-10 packet R1+AR-08 under `proof/nw008/at-10/`; implementation-only grant prep required before implementation; no execution grant yet |
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
- Gemini/ADK implementation is **authorized and closed** under NW-004 (`NW004_STATUS=DONE`, `NW004_CLOSEOUT_STATUS=CLOSED_SUCCESS`, `PHASE3_UNIT1_STATUS=MERGED_COMPLETE`, `PHASE3_UNIT2_STATUS=MERGED_COMPLETE`, `PHASE3_UNIT3_STATUS=MERGED_COMPLETE`, `GEMINI_ADK_AUTHORIZED=YES`). Unit 1 provider surface remains `COMPATIBLE_SURFACE_ONLY`. Unit 2 runtime truth: `GOOGLE_ADK_RUNTIME_STARTED=YES`, `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`. Unit 3 runtime truth: `FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED=YES`, `GOOGLE_ADK_RUNTIME_REUSED=YES`, `DETERMINISTIC_POLICY_GATE_INVOKED=YES`, `DETERMINISTIC_POLICY_BYPASS=NO`, `EXTERNAL_EFFECTS=0`. At NW-004 closeout the remaining vertical-slice layers (mutation execution, Firestore audit, MG Guide card experience, and deployment) stayed out of scope; **NW-006 is now MERGED_COMPLETE** (PR #15 / head `c7d25b447db0a961c17ae26e326ada230b7e4627` / CI 31630399411 SUCCESS / merge `e22eb861442a37be0797d6d7aec8bb17001fb7a3`), while mutation execution, Firestore audit (NW-005), deployment (NW-007), and acceptance/demo proof (NW-008) remain separately governed.
- NW-006 MERGED_COMPLETE does **not** complete AT-1…AT-10, authorize CRM mutation, authorize Firestore writes, execute NW-013 live reads, or deploy (NW-007). Synthetic card tests are not a substitute for historical acceptance criteria.
- NW-008 Tranche A is **MERGED_COMPLETE** (PR #40); Tranche B is **MERGED_COMPLETE** (PR #42) with `FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP=CLOSED`; Tranche C is **MERGED_COMPLETE** (PR #44); Tranche D D1/AT-9 and D2/AT-8 are **MERGED_COMPLETE** (PR #48/#49/#50). **Historical snapshot after Tranche C (preserved):** READY=none; HISTORICAL_COMPLETE=AT-2,AT-4,AT-5; PARTIAL=AT-8,AT-9; BLOCKED=AT-1,AT-3,AT-6,AT-7; DEFERRED=AT-10. **Current-state markers (post D2 + AT-10 auth packet prep):** `NW008_HISTORICAL_AT_COMPLETE=AT-2,AT-4,AT-5,AT-8,AT-9`; `NW008_HISTORICAL_AT_REMAINING=AT-1,AT-3,AT-6,AT-7,AT-10`; `NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE`; `NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED`; `NW005_STAGE_B_SMOKE=PASS`; `AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION`; `AT10_EXECUTION_AUTHORIZED=NO`; `CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION`; `NW008_OVERALL_STATUS=IN_PROGRESS`.
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
- Public Unit 3 closeout: Follow-Up Planning Agent; branch `feat/meeting-follow-up-v1-follow-up-planning-agent-unit3`; PR #13 **MERGED**; final reviewed head `32f13b6db0bfd9964001133d05f33d6ed294d0ba`; final exact-head CI run **31623771005** SUCCESS; merge SHA `91927e4cfeb5010cf399ae870ad0897156dff03e`; merged `2026-08-12T17:47:49Z`; implementation evidence head `09c6a95dafa6e09f8244813e32a054aa27635d5c` / CI **31623557067** SUCCESS (preserved separately; not the final reviewed tip); proof `proof/phase3/unit3/proof-return.yaml`; closeout `proof/phase3/unit3/unit3-merge-closeout.md`; all six scenarios PASS; **NW-006 later MERGED_COMPLETE** via PR #15 (see NW-006 section below)
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
- Explicit Unit 3 non-delivery (historical): live GHL; CRM mutation execution; Firestore audit writer (NW-005); Cloud Run deployment (NW-007). NW-006 card is later **MERGED_COMPLETE** (PR #15).
- Completion bar (full vertical slice still open beyond NW-004/NW-006): mutation execution + audit + deployment + AT-1…AT-10 demo proof remain separately governed; agent/policy packet path for Units 1–3 is closed with `EXTERNAL_EFFECTS=0`; card path closed with `EXTERNAL_EFFECTS=0`
- Next: optional NW-013 bounded synthetic live-read execution; then NW-005 → NW-007 → NW-008; CRM mutation only under a future separately human-authorized synthetic-only bounded lane against the business-active canonical CRM (see [`../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md))

## NW-006 MG Guide Meeting Follow-Up card (MERGED_COMPLETE)

- Date (UTC): 2026-08-12
- Status: **MERGED_COMPLETE**
- Public PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/15 (**MERGED**)
- Final reviewed head: `c7d25b447db0a961c17ae26e326ada230b7e4627`
- Exact-head CI run: **31630399411** SUCCESS
- Merge SHA: `e22eb861442a37be0797d6d7aec8bb17001fb7a3`
- Merged at: `2026-08-12T19:12:33Z`
- Branch (implementation): `feat/nw006-meeting-follow-up-card`
- Closeout branch (docs): `chore/nw006-closeout-competition-readiness`
- Durable markers:

```text
NW006_STATUS=MERGED_COMPLETE
NW006_PR=15
NW006_FINAL_REVIEWED_HEAD=c7d25b447db0a961c17ae26e326ada230b7e4627
NW006_EXACT_HEAD_CI_RUN=31630399411
NW006_EXACT_HEAD_CI_RESULT=SUCCESS
NW006_MERGE_SHA=e22eb861442a37be0797d6d7aec8bb17001fb7a3
NW006_MERGED_AT=2026-08-12T19:12:33Z
EXTERNAL_EFFECTS=0
```

- Scope delivered: competition-local host-agnostic deterministic card mapper/renderers/CLI; required CardViewModel schema; synthetic packet fixtures + expected snapshots; card tests; implementation packet + proof return + merge closeout
- Explicit non-delivery: private authenticated MG Guide host integration; CRM mutation; GHL live calls/writes; Firestore writer; deployment; AT-1…AT-10 completion claims
- Artifacts: `proof/nw006/nw-006-merge-closeout.md`, `proof/nw006/nw-006-implementation-packet.md`, `proof/nw006/proof-return.yaml`, `src/mg_guide/meeting_follow_up_card/**`, `contracts/mg_guide_meeting_follow_up_card.schema.json`, `fixtures/nw006/**`, `tests/mg_guide/meeting_follow_up_card/**`

## NW-008 acceptance readiness (A+B+C+D1/D2 MERGED_COMPLETE; AT-10 auth lane active; overall IN_PROGRESS)

- Date (UTC): 2026-08-15 (current-state sync); Tranche A/B/C historical closeouts dated 2026-08-14
- Overall NW-008: **IN_PROGRESS** — Tranches A, B, C, D1/AT-9, D2/AT-8 closed; full historical AT-1…AT-10 closeout not claimed
- Historical criteria source: `docs/MEETING_FOLLOW_UP_FOUNDATION.md` §17 (AT-1…AT-10 verbatim; not silently revised)
- Artifacts: `proof/nw008/nw008-tranche-a-merge-closeout.md`, `proof/nw008/nw-008-tranche-b-merge-closeout.md`, `proof/nw008/nw-008-tranche-c-merge-closeout.md`, `proof/nw008/nw-008-tranche-d-d1-governance-closeout.md`, `proof/nw008/nw-008-tranche-d-d2-governance-closeout.md`, `proof/nw008/nw-008-readiness-matrix.md`, `proof/nw008/nw-008-implementation-packet.md`, `proof/nw008/nw-008-tranche-b-implementation-packet.md`, `proof/nw008/nw-008-tranche-c-implementation-packet.md`, `proof/nw008/at-10/nw-008-at10-acceptance-demo-authorization-packet.md`, `proof/nw008/at-10/nw-008-at10-implementation-authorization.md`, `proof/nw008/tranche-a/**`, `proof/nw008/tranche-b/**`, `proof/nw008/tranche-c/**`, `proof/nw008/tranche-d/**`, `proof/nw008/at-0{2,4,5,8,9}/**`, `src/orchestration/nw008_harness.py`, `tests/acceptance/test_nw008_tranche_a.py`
- Current-state markers:

```text
NW008_TRANCHE_C_STATUS=MERGED_COMPLETE
NW008_TRANCHE_D_D1_STATUS=MERGED_COMPLETE
NW008_TRANCHE_D_D2_STATUS=CLOSED
NW008_HISTORICAL_AT_COMPLETE=AT-2,AT-4,AT-5,AT-8,AT-9
NW008_HISTORICAL_AT_REMAINING=AT-1,AT-3,AT-6,AT-7,AT-10
NW008_OVERALL_STATUS=IN_PROGRESS

NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE
NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED
NW005_STAGE_B_SMOKE=PASS

AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
```

- Historical readiness snapshot after Tranche C closeout (preserved): READY=none; HISTORICAL_COMPLETE=AT-2,AT-4,AT-5; PARTIAL=AT-8,AT-9; BLOCKED=AT-1,AT-3,AT-6,AT-7; DEFERRED=AT-10
- Current readiness snapshot (post D2 + AT-10 AR-08): READY=none; HISTORICAL_COMPLETE=AT-2,AT-4,AT-5,AT-8,AT-9; PARTIAL=none; BLOCKED=AT-1,AT-3,AT-6,AT-7; DEFERRED=AT-10 (active acceptance-demo authorization lane)
- Recommended dependency order (current): NW-005 Stage B smoke is already **PASS** (not an active blocker) → NW-008 AT-10 acceptance-demo authorization (implementation-only grant → offline implementation → execution grant) → remaining blocked ATs behind a future separately human-authorized synthetic-only mutation lane against the business-active canonical CRM; optional NW-013 bounded synthetic live-read remains separately governed
- Constraints retained: no isolated GHL test location; canonical GHL location is not a test environment; NW-013 AUTHORIZED_NOT_EXECUTED; no GHL writes authorized; no Firestore writes authorized under AT-10 until a separate execution grant; production/customer data forbidden; raw REST forbidden; deterministic policy sole consequential-action authorization surface; `AT10_EXECUTION_AUTHORIZED=NO`; `AT10_COMPLETION_CLAIM_AUTHORIZED=NO`

### Tranche A (MERGED_COMPLETE)

- Public PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/40 (**MERGED**)
- Purpose: deterministic acceptance-evidence substrate (offline/synthetic only)
- Durable markers:

```text
PR40_MERGED=YES
PR40_FINAL_REVIEWED_HEAD=b61a4b02e0dae8c14701ccc8184c205d6bdcd29d
PR40_MERGE_SHA=10347c709e86dfbca83cdf8c9ffd1a9a8491ce87
PR40_MERGED_AT=2026-08-14T11:30:36Z

NW008_TRANCHE_A_STATUS=MERGED_COMPLETE
NW008_TRANCHE_A_PURPOSE=DETERMINISTIC_ACCEPTANCE_EVIDENCE_SUBSTRATE
NW008_TRANCHE_A_HISTORICAL_AT_COMPLETE=NONE

DETERMINISTIC_SUPPORTING_PROOFS=AT-2,AT-4,AT-5
PARTIAL_SUPPORTING_PROOFS=AT-8,AT-9
# HISTORICAL_PLANNING_SNAPSHOT_SUPERSEDED_BY_PR44 — Tranche A-era marker only:
HISTORICAL_AT_COMPLETE=NONE
BLOCKED_NOT_EXECUTED=AT-1,AT-3,AT-6,AT-7
DEFERRED_NOT_EXECUTED=AT-10
```

- Explicit non-claim: no historical AT-1…AT-10 marked complete by Tranche A; AT definitions unchanged. Current overall historical completion after Tranche C is `AT-2,AT-4,AT-5` (see Tranche C section).

### Tranche B (MERGED_COMPLETE)

- Public PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/42 (**MERGED**)
- Purpose: longitudinal synthetic agent-fleet replay (offline/synthetic only)
- Merge closeout: `proof/nw008/nw-008-tranche-b-merge-closeout.md`
- Durable markers:

```text
PR42_MERGED=YES
PR42_FINAL_REVIEWED_HEAD=4da7e3fd25937e5cd90c241443ec1badbbf94e3b
PR42_MERGE_SHA=1ee6647d7e8284cb165c7ac8063582c6769d0a79
PR42_MERGED_AT=2026-08-14T13:06:06Z
PR42_IMPLEMENTATION_SUBJECT_SHA=27edac20756518257a54492487fb09bfb3b88576

NW008_TRANCHE_B_STATUS=MERGED_COMPLETE
NW008_TRANCHE_B_PURPOSE=LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY
FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP=CLOSED

TB_PROOF_OBLIGATIONS=TB-01..TB-18
TB_PROOF_RESULT=ALL_PASS

GHL_LIVE_CALLS=0
GHL_READS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0
NW013_EXECUTED=NO
DEPLOYMENT_PERFORMED=NO
```

- Explicit non-claim: Tranche B closed the fleet-replay evidence gap only; no historical AT-1…AT-10 marked complete by Tranche B (`HISTORICAL_PLANNING_SNAPSHOT_SUPERSEDED_BY_PR44`: Tranche-B-era `HISTORICAL_AT_COMPLETE=NONE`); AT definitions unchanged. Current overall historical completion after Tranche C is `AT-2,AT-4,AT-5`.

### Tranche C (MERGED_COMPLETE)

- Public PR: https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/44 (**MERGED**)
- Purpose: historical failure-path agent-fleet acceptance replay of AT-2 / AT-4 / AT-5 through the provider-neutral transcript source boundary
- Merge closeout: `proof/nw008/nw-008-tranche-c-merge-closeout.md`
- Implementation packet: `proof/nw008/nw-008-tranche-c-implementation-packet.md`
- Durable markers:

```text
NW008_TRANCHE_C_STATUS=MERGED_COMPLETE
NW008_TRANCHE_C_PR=44
NW008_TRANCHE_C_IMPLEMENTATION_SUBJECT_SHA=49b567c35cc2923e6faa6829e9967b8c089f402b
NW008_TRANCHE_C_FINAL_REVIEWED_HEAD=03b140040daff6768ac1ef0e22735c90f3b9f72f
NW008_TRANCHE_C_MERGE_SHA=36b0999dacee0dede9de355db28badbe38ed0581
NW008_TRANCHE_C_MERGED_AT=2026-08-14T16:01:36Z
NW008_TRANCHE_C_EXACT_HEAD_CI_RUN=31817065419
TRANCHE_C_PURPOSE=HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY

NW008_HISTORICAL_AT_COMPLETE=AT-2,AT-4,AT-5
NW008_HISTORICAL_AT_REMAINING=AT-1,AT-3,AT-6,AT-7,AT-8,AT-9,AT-10
NW008_OFFLINE_EXECUTABLE_CANDIDATES=AT-8,AT-9
NW008_TRANCHE_C_TARGETS=AT-2,AT-4,AT-5
NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9
AT2_STATUS=HISTORICAL_COMPLETE
AT4_STATUS=HISTORICAL_COMPLETE
AT5_STATUS=HISTORICAL_COMPLETE
NW008_OVERALL_STATUS=IN_PROGRESS

TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
AUTHORITATIVE_STOP_SOURCE=STATE_MACHINE_WORKFLOW_CONTRACT
NW007_CARD_SEMANTICS_CHANGE=NO
PER_SCENARIO_EXECUTION=SHORT_CIRCUIT_AT_FIRST_GOVERNED_FAILURE

GHL_LIVE_CALLS=0
GHL_READS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0
NW013_EXECUTED=NO
DEPLOYMENT_PERFORMED=NO
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_RUNTIME=NOT_AUTHORIZED_IN_TRANCHE_C
NEW_AGENT=NO
POLICY_SEMANTICS_CHANGE=NO
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

- Explicit claim boundary: only AT-2 / AT-4 / AT-5 historical clauses are promoted by Tranche C; remaining ATs stay incomplete under that tranche; no live CRM/Firestore mutation authorized by Tranche C

### Tranche D D1/AT-9 + D2/AT-8 (MERGED_COMPLETE; historical)

- D1/AT-9 governance closeout: PR #48; `proof/nw008/nw-008-tranche-d-d1-governance-closeout.md`
- D2/AT-8 implementation + durable proof: PR #49 merge `d9f6a9bbca30c0c4419bd34e74588d98b072a641`
- D2 governance closeout: PR #50 merge `8f7fdd482c03dfee5e75159054d9ddf11dd793fe`; `proof/nw008/nw-008-tranche-d-d2-governance-closeout.md`
- Durable markers:

```text
AT8_STATUS=HISTORICAL_COMPLETE
AT9_STATUS=HISTORICAL_COMPLETE
NW008_TRANCHE_D_D2_STATUS=CLOSED
```

- Explicit non-claim: Tranche D does not authorize or complete AT-10; does not reopen NW-005 Stage B smoke; does not authorize GHL/CRM mutation

### AT-10 acceptance-demo authorization lane (current; not authorized)

- Planning packet: `proof/nw008/at-10/nw-008-at10-acceptance-demo-authorization-packet.md` (R1 proof architecture AR-01…AR-07 accepted; AR-08 authority sequence bound)
- Implementation-only grant request (not approved): `proof/nw008/at-10/nw-008-at10-implementation-authorization.md`
- Durable current markers:

```text
AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION
AT10_IMPLEMENTATION_AUTHORIZED=NO
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
IMPLEMENTATION_AUTHORIZATION_MODE=IMPLEMENTATION_ONLY_NO_NETWORK
EXECUTION_GRANT_BEFORE_IMPLEMENTATION_SUBJECT=FORBIDDEN
NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE
NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED
NW005_STAGE_B_SMOKE=PASS
```

- Explicit non-claim: packet + implementation-grant prep do not authorize implementation, Firestore/network, execution, or AT-10 completion


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

---

## NW-008 durable-state normalization — active CRM synthetic-only (CURRENT)

- Normalization ID: `NW008_ACTIVE_CRM_SYNTHETIC_ONLY_NORMALIZATION_001`
- Artifact: [`../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md)
- Branch: `planning/nw008-active-crm-synthetic-only-normalization-001`
- Base: `origin/main` @ `dc48531a5d79d01a57de8fcfa81140a4dd59535c` (post PR #91 merge; PR #91 state=MERGED, final head `a4f81d70b49ba70f7b19901da49bb7080bf61881`, merge SHA `dc48531a5d79d01a57de8fcfa81140a4dd59535c`)
- Effect: current-authority and current-facing artifacts now classify the GoHighLevel target as `CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM` under synthetic-only bounded execution controls; historical proof is preserved, not rewritten.
- Preserved invariants: private exact-ID allowlist only; preverified synthetic contact/opportunity only; no broad search; no list/pagination expansion; no alternate-target discovery; no non-allowlisted record access; no real customer record read or mutation; `NOTE_WRITE_ATTEMPTS_MAX=1`; `STAGE_WRITE_ATTEMPTS_MAX=1`; no automatic retry; no compensating mutation; `LIVE_CRM_MUTATION_AUTHORIZED=NO`; `REST_ADAPTER_EXECUTION_AUTHORIZED=NO`; `SEPARATE_HUMAN_MUTATION_AUTHORIZATION_REQUIRED=YES`.
- Transport state recorded: `GHL_GENERIC_MCP_IMPLEMENTATION_PATH=BLOCKED`; `HIGHLEVEL_REST_ADAPTER=PLANNING_NEXT`; REST transport authorization reviewed separately — the REST adapter does not inherit MCP transport authority, execution grants, operation authority, or write execution authorization.
- Next (prepared, not self-authorized): `NW008_AT1_GHL_REST_ADAPTER_ARCHITECTURE_001`.
- External effects: `EXTERNAL_EFFECTS=0`; `GHL_CALLS=0`; `CRM_WRITES=0`; `IAM_CHANGES=0`; `SECRET_CHANGES=0`; `DEPLOYMENT_CHANGES=0`.
