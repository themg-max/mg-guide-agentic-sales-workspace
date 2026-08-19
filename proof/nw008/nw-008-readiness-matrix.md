# NW-008 Acceptance Readiness Matrix — AT-1…AT-10

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Status | **IN_PROGRESS** (Tranche A **MERGED_COMPLETE** PR #40; Tranche B **MERGED_COMPLETE** PR #42; Tranche C **MERGED_COMPLETE** PR #44; Tranche D D1/AT-9 + D2/AT-8 **MERGED_COMPLETE** via PR #48/#49/#50) |
| Source of historical criteria | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Companion packets | [`nw-008-implementation-packet.md`](./nw-008-implementation-packet.md) (Tranche A), [`nw-008-tranche-b-implementation-packet.md`](./nw-008-tranche-b-implementation-packet.md) (Tranche B), [`nw-008-tranche-c-implementation-packet.md`](./nw-008-tranche-c-implementation-packet.md) (Tranche C), [`at-10/nw-008-at10-acceptance-demo-authorization-packet.md`](./at-10/nw-008-at10-acceptance-demo-authorization-packet.md) (AT-10 planning) |
| Tranche B closeout | [`nw-008-tranche-b-merge-closeout.md`](./nw-008-tranche-b-merge-closeout.md) — `FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP=CLOSED` |
| Tranche C transcript source contract | **TRANSCRIPT_SOURCE_ENVELOPE_V1** (provider-neutral; Google Workspace adapter `FUTURE_NOT_IMPLEMENTED`) |
| NW-006 dependency | **MERGED_COMPLETE** (PR #15) — card surface available offline |
| NW-007 dependency | **MERGED_COMPLETE** (PR #37 merged; Stage B2 deployment evidence exists; proof closeout merged via PR #38) |
| Mutation / write posture | **No GHL writes authorized**; no isolated GHL test location |
| Audit posture | NW-005 Stage A offline audit projection is **MERGED_COMPLETE**; Stage B environment binding **COMPLETE**, human authorization **APPROVED**, smoke **PASS** (PR #22/#23); AT-10 acceptance-demo remains a **separate** authorization lane (`AT10_EXECUTION_AUTHORIZED=NO`) |
| Deployment posture | NW-007 Stage B2 deployment evidence exists, but `DEPLOYMENT_AUTHORIZATION=NO` |
| Live read posture | NW-013 exact-ID synthetic read remains **AUTHORIZED_NOT_EXECUTED** |
| Current next lane | `CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION` (`AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION`) |
| Production / customer data | **Forbidden** |
| Raw REST | **Forbidden** |
| Consequential-action authority | Deterministic policy remains the sole authorization surface |
| Environment semantics | **Normalized:** CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM (synthetic-only bounded controls) per [`../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](../../docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md). Historical "safe-environment"/"isolated test location" phrasing below is preserved as the historical record; the normalized contract is the controlling current interpretation. `ENVIRONMENT_READY != EXECUTION_AUTHORIZED`; separate human mutation authorization required |

## Classification legend

| Class | Meaning |
| --- | --- |
| **READY** | Historical AT can be executed end-to-end **today** under current grants with recorded evidence, without new authorization |
| **HISTORICAL_COMPLETE** | Historical AT has been satisfied by a merged proof bundle without changing the original §17 definition |
| **PARTIAL** | Material offline/synthetic prerequisites exist, but one or more historical expected outcomes remain unsatisfied |
| **DEFERRED** | Intentionally sequenced behind a planned dependency (authorization, implementation, or deployment lane) |
| **BLOCKED** | Hard environmental or authorization stop prevents honest execution of the historical criterion |

> **Integrity rule:** Historical AT-1…AT-10 definitions are preserved verbatim below.
> They are **not** silently revised. Passing synthetic card tests, Unit 3 scenario
> harnesses, or offline policy fixtures alone does **not** mark an AT complete.

---

## Historical acceptance criteria (verbatim from foundation §17)

| # | Test | Expected outcome |
| --- | --- | --- |
| AT-1 | `transcript-success.txt` full run | `completed`; note `verified`; stage `discovery_scheduled → discovery_complete` `verified`; audit record present; MG Guide card State 1 |
| AT-2 | `transcript-ambiguous-contact.txt` | `blocked` with `AMBIGUOUS_CONTACT`; **0 CRM writes**; MG Guide card State 2 |
| AT-3 | `transcript-no-stage-change.txt` | Note `verified`; stage unchanged with `STAGE_TRANSITION_NOT_ALLOWED` reason; disposition `completed_with_review` |
| AT-4 | Contact not found | `blocked` with `CONTACT_NOT_FOUND`; 0 writes |
| AT-5 | Extraction confidence below threshold | `blocked` with `LOW_EXTRACTION_CONFIDENCE`; 0 writes |
| AT-6 | GHL tool failure during write | `failed` with `GHL_TOOL_FAILURE`; mutation recorded `attempted: true, verified: false` |
| AT-7 | Write succeeds but read-back mismatch | `failed` with `GHL_WRITE_NOT_VERIFIED`; no completion declared |
| AT-8 | Per-run mutation caps | Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice |
| AT-9 | Blocked tool invocation (e.g., contact create) | Refused at tool-manifest layer; recorded in audit warnings |
| AT-10 | Audit completeness | Every run (success, blocked, failed) produces a `workflow_runs/{run_id}` record with agents, tool counts, reason codes, disposition |

---

## Current readiness matrix (post Tranche C merge / PR #44)

> **Historical-record note (NW008_ACTIVE_CRM_SYNTHETIC_ONLY_NORMALIZATION_001):**
> the AT rows below are preserved as their historical snapshot. Their
> "safe-environment mutation lane" and "no isolated GHL test location"
> phrasing reflects what was believed/required at the time and is superseded
> for current environment semantics by the normalized contract (see
> front-matter *Environment semantics* row): the target is the business-active
> canonical CRM under synthetic-only bounded execution controls, and any
> future mutation lane is a separately human-authorized synthetic-only bounded
> execution grant — not a "safe environment" lane.

| AT | Historical expected outcome | Current readiness | Current evidence | Remaining gap | Authorization dependency | Recommended next action |
| --- | --- | --- | --- | --- | --- | --- |
| **AT-1** | `transcript-success.txt` full run → `completed`; note `verified`; stage `discovery_scheduled → discovery_complete` verified; audit record present; MG Guide card State 1 | **BLOCKED** | NW-007 decision-card proof is merged complete; deterministic success render and policy semantics are proven offline; synthetic success path remains available for offline review | Live write-path verification still cannot be honestly executed without a safe-environment mutation grant; no isolated GHL test location; no Firestore audit writer under current main | Future safe-environment mutation + audit authorization | Keep this AT deferred behind a separately authorized write path; do not claim full success without a safe-environment lane |
| **AT-2** | `transcript-ambiguous-contact.txt` → `blocked` with `AMBIGUOUS_CONTACT`; 0 CRM writes; MG Guide card State 2 | **HISTORICAL_COMPLETE** | Tranche C replay proved `AMBIGUOUS_CONTACT` + zero-write fail-closed handling in `proof/nw008/tranche-c/at-02-run.json`; deterministic replay and `TC-03`/`TC-04`/`TC-05`/`TC-22` pass | No remaining gap in the historical criterion; the broader live CRM path remains outside this lane | No new mutation authority required for this historical clause; live relationship read remains optional and unexecuted | Maintain the historical completion flag; do not claim a wider live mutation lane or reinterpret the historical clause |
| **AT-3** | `transcript-no-stage-change.txt` → note `verified`; stage unchanged with `STAGE_TRANSITION_NOT_ALLOWED`; disposition `completed_with_review` | **BLOCKED** | Offline stage-denied semantics and the card’s completed-with-review rendering exist; deterministic policy prevents stage write | The historical AT requires a live verified note + stage-write refusal evidence path under a safe-environment mutation lane | Future safe-environment mutation authorization and audit writer | Do not claim completion of AT-3 until write-path evidence exists under explicit authority |
| **AT-4** | Contact not found → `blocked` with `CONTACT_NOT_FOUND`; 0 writes | **HISTORICAL_COMPLETE** | Tranche C replay proved `CONTACT_NOT_FOUND` + zero-write fail-closed handling in `proof/nw008/tranche-c/at-04-run.json`; deterministic replay and `TC-08`/`TC-09`/`TC-10` pass | No remaining gap in the historical criterion; no live write path is implied | No new mutation authority required for this historical clause; live CRM lookup remains outside this lane | Maintain the historical completion flag; do not expand this to a live mutation or broader runtime lane |
| **AT-5** | Extraction confidence below threshold → `blocked` with `LOW_EXTRACTION_CONFIDENCE`; 0 writes | **HISTORICAL_COMPLETE** | Tranche C replay proved `LOW_EXTRACTION_CONFIDENCE` + zero-write fail-closed handling in `proof/nw008/tranche-c/at-05-run.json`; deterministic replay and `TC-13`/`TC-14`/`TC-15` pass | No remaining gap in the historical criterion; no live write path is implied | No new mutation authority required for this historical clause; no Firestore writes today | Maintain the historical completion flag; do not imply a future write-capable runtime without separate authority |
| **AT-6** | GHL tool failure during write → `failed` with `GHL_TOOL_FAILURE`; mutation recorded `attempted: true, verified: false` | **BLOCKED** | Failure-code semantics and failed-card rendering exist; no mutation path is available under current grants | Real write-path failure injected on a live GHL tool is not authorized; isolated test service is unavailable and canonical GHL location is not a test environment | Separate safe-environment mutation lane; explicit human authority required | Do not claim AT-6 completion; keep blocked until a governed mutation environment exists |
| **AT-7** | Write succeeds but read-back mismatch → `failed` with `GHL_WRITE_NOT_VERIFIED`; no completion declared | **BLOCKED** | Failure semantics and denial-of-completion posture are documented; deterministic card fail-state exists | Real write/read-back mismatch cannot be executed without GHL mutation + verification path | Separate safe-environment mutation lane + verification authority | Keep AT-7 blocked; no completion claim without live write/read-back evidence |
| **AT-8** | Per-run mutation caps → second note or stage write attempt is refused by OL3 policy, not by agent choice | **HISTORICAL_COMPLETE** | Tranche D D2/AT-8 durable proof + governance closeout (PR #49 merge `d9f6a9bbca30c0c4419bd34e74588d98b072a641`; D2 closeout PR #50 / `8f7fdd482c03dfee5e75159054d9ddf11dd793fe`); `AT8_STATUS=HISTORICAL_COMPLETE` | No remaining gap in the historical criterion; live CRM mutation remains outside this lane | No new mutation authority required for this historical clause | Maintain the historical completion flag; do not expand into AT-10 Firestore acceptance-demo without separate AT-10 grants |
| **AT-9** | Blocked tool invocation (e.g., contact create) → refused at tool-manifest layer; recorded in audit warnings | **HISTORICAL_COMPLETE** | Tranche D D1/AT-9 governance closeout (PR #48) + durable offline refusal proof; historical criterion satisfied without Stage B Firestore activation | No remaining gap in the historical criterion; durable Firestore `workflow_runs/{run_id}` completeness is AT-10, not AT-9 | No NW-005 Stage B dependency for this historical clause | Maintain the historical completion flag; do not couple AT-9 completion to AT-10 execution |
| **AT-10** | Every run produces a `workflow_runs/{run_id}` record with agents, tool counts, reason codes, disposition | **DEFERRED** (active planning lane) | NW-005 Stage A merged; Stage B binding **COMPLETE**, human auth **APPROVED**, smoke **PASS**; AT-10 acceptance-demo authorization packet R1+AR-08 proposed under `proof/nw008/at-10/` | AT-10 acceptance-demo is **not** authorized; Stage B smoke is **not** the active blocker. Next governed step is implementation-only grant review (AR-08), then offline implementation, then separate execution grant | `CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION`; `AT10_EXECUTION_AUTHORIZED=NO`; implementation-only grant required before implementation; execution grant forbidden before implementation subject SHA | Do **not** reopen Stage B smoke; do **not** implement or execute AT-10 until the AR-08 sequence grants are merged |

### Summary counts (current readiness refresh)

| Class | ATs |
| --- | --- |
| READY | _(none)_ |
| HISTORICAL_COMPLETE | AT-2, AT-4, AT-5, AT-8, AT-9 |
| PARTIAL | _(none)_ |
| BLOCKED | AT-1, AT-3, AT-6, AT-7 |
| DEFERRED | AT-10 |

**Historical note (preserved):** After Tranche C merge, offline executable candidates were `AT-8, AT-9`. Those candidates were subsequently closed as **HISTORICAL_COMPLETE** under Tranche D (D1/AT-9, D2/AT-8). They are no longer the active next lane.

**Tranche C** is a merged historical replay of **exactly** `AT-2, AT-4, AT-5` entering through the
provider-neutral `TRANSCRIPT_SOURCE_ENVELOPE_V1` boundary
([`nw-008-tranche-c-implementation-packet.md`](./nw-008-tranche-c-implementation-packet.md)).
`AT-8` / `AT-9` were **excluded** from Tranche C and later closed under Tranche D.
Future Google Workspace transcript adapter remains
`FUTURE_NOT_IMPLEMENTED` / `NOT_AUTHORIZED_IN_TRANCHE_C`.

```text
NW008_HISTORICAL_AT_COMPLETE=AT-2,AT-4,AT-5,AT-8,AT-9
NW008_HISTORICAL_AT_REMAINING=AT-1,AT-3,AT-6,AT-7,AT-10
NW008_OFFLINE_EXECUTABLE_CANDIDATES=
NW008_TRANCHE_C_STATUS=MERGED_COMPLETE
NW008_TRANCHE_C_PR=44
NW008_TRANCHE_C_TARGETS=AT-2,AT-4,AT-5
NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9
NW008_TRANCHE_C_REQUIRED_NEW_AUTHORIZATION=NO
NW008_TRANCHE_B_STATUS=MERGED_COMPLETE
NW008_TRANCHE_D_D1_STATUS=MERGED_COMPLETE
NW008_TRANCHE_D_D2_STATUS=CLOSED
FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP=CLOSED
NW008_OVERALL_STATUS=IN_PROGRESS
TRANCHE_C_STATUS=MERGED_COMPLETE
TRANCHE_C_EXECUTION_STARTED=YES
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
TRANSCRIPT_SOURCE_ACCESS_CONTEXT_MODELED=YES
MG_GUIDE_ADD_ON_GRANT_MODELED=YES
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=FUTURE_NOT_IMPLEMENTED
AUTHORITATIVE_STOP_SOURCE=STATE_MACHINE_WORKFLOW_CONTRACT
NW007_CARD_SEMANTICS_CHANGE=NO
PER_SCENARIO_EXECUTION=SHORT_CIRCUIT_AT_FIRST_GOVERNED_FAILURE
NW005_STAGE_A_STATUS=MERGED_COMPLETE
NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE
NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED
NW005_STAGE_B_SMOKE=PASS
NW005_STAGE_B_STATUS=SMOKE_PASS_COMPLETE
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
MG_MCP_NW008_DISCOVERABILITY=UNKNOWN
```

## Cross-cutting guardrails (unchanged)

```text
NW007_DECISION_CARD_STATUS=MERGED_COMPLETE
NW007_APPLICATION_REPAIR_REQUIRED=NO
NW007_STAGE_B2_DEPLOYMENT_EVIDENCE=AVAILABLE
NW007_PROOF_CLOSEOUT_STATUS=MERGED
EXTERNAL_EFFECTS=0
POLICY_SEMANTICS_CHANGE=NO
PACKET_SCHEMA_CHANGE=NO
ADK_ORCHESTRATION_CHANGE=NO
NEW_AGENT=NO
NEW_LLM_CALL=NO
CLOUD_MUTATION=NONE
DEPLOYMENT_PERFORMED=NO
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
PRODUCTION_CUSTOMER_DATA=FORBIDDEN
RAW_REST=FORBIDDEN
CANONICAL_GHL_LOCATION_IS_TEST_ENV=NO
```

---

## Cross-cutting constraints (do not weaken)

```text
ISOLATED_GHL_TEST_LOCATION=NO
CANONICAL_GHL_LOCATION_IS_TEST_ENV=NO
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED_UNDER_COMPLETED_LANES=NO
NW005_STAGE_A_STATUS=MERGED_COMPLETE
NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE
NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED
NW005_STAGE_B_SMOKE=PASS
NW005_STAGE_B_STATUS=SMOKE_PASS_COMPLETE
NW007_STATUS=MERGED_COMPLETE
NW007_STAGE_B2_DEPLOYMENT_EVIDENCE=AVAILABLE
NW007_DEPLOYMENT_AUTHORIZATION=NO
PRODUCTION_CUSTOMER_DATA=FORBIDDEN
RAW_REST=FORBIDDEN
DETERMINISTIC_POLICY=SOLE_CONSEQUENTIAL_ACTION_AUTHORIZATION_SURFACE
NW006_STATUS=MERGED_COMPLETE
EXTERNAL_EFFECTS=0
AT10_CURRENT_PHASE=ACCEPTANCE_DEMO_AUTHORIZATION
AT10_EXECUTION_AUTHORIZED=NO
CURRENT_NEXT_LANE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
```

## What NW-006 merge does and does not change

| Claim | Status after PR #15 |
| --- | --- |
| Card can render completed / completed_with_review / blocked / failed from packets | Yes (offline/synthetic) |
| Card re-evaluates policy or executes mutations | **No** |
| AT-1…AT-10 complete because card snapshots pass | **No — forbidden claim** |
| Vertical slice demo fully executable per foundation §18 | **No** |
| Competition acceptance (NW-008) ready to close | **No** — **IN_PROGRESS**; AT-2/AT-4/AT-5/AT-8/AT-9 are **HISTORICAL_COMPLETE**; AT-1/AT-3/AT-6/AT-7 remain blocked on safe-env mutation; AT-10 is the active acceptance-demo authorization lane (`AT10_EXECUTION_AUTHORIZED=NO`) |

## Recommended evidence standard for remaining NW-008 AT execution

For each AT marked for execution under a future authorized unit:

1. Preserve the historical expected outcome text unchanged.
2. Bind exact fixture / run IDs / packet hashes / proof paths.
3. Record `GHL_LIVE_CALLS`, `GHL_WRITES`, `FIRESTORE_WRITES`, `EXTERNAL_EFFECTS`.
4. Separate **offline synthetic proof** from **live/safe-environment proof**.
5. Refuse completion claims when any historical clause (verified write, audit
   record, card state, zero-write guarantee, etc.) is unmet.

## STOP

```text
STOP_CODE=NW008_TRANCHE_C_CLOSEOUT_ACCEPTANCE_RECONCILIATION_READY_FOR_REVIEW
```
