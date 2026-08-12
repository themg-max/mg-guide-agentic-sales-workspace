# NW-008 Readiness Matrix — AT-1…AT-10 (Planning Only)

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Status | **PLANNED** (readiness classification only — no acceptance execution in this unit) |
| Source of historical criteria | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Companion packet | [`nw-008-implementation-packet.md`](./nw-008-implementation-packet.md) |
| NW-006 dependency | **MERGED_COMPLETE** (PR #15) — card surface available offline |
| Mutation / write posture | **No GHL writes authorized**; no isolated GHL test location |
| Audit posture | NW-005 Firestore audit writer remains **PLANNED** |
| Deployment posture | NW-007 Cloud Run test deployment remains **PLANNED** |
| Live read posture | NW-013 exact-ID synthetic read remains **AUTHORIZED_NOT_EXECUTED** |
| Production / customer data | **Forbidden** |
| Raw REST | **Forbidden** |
| Consequential-action authority | Deterministic policy remains the sole authorization surface |

## Classification legend

| Class | Meaning |
| --- | --- |
| **READY** | Historical AT can be executed end-to-end **today** under current grants with recorded evidence, without new authorization |
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

## Current readiness matrix

| AT | Readiness | What exists today (honest) | Historical gaps remaining | Primary blockers / dependencies |
| --- | --- | --- | --- | --- |
| **AT-1** | **PARTIAL** | Offline Unit 1–3 success path produces `completed` disposition intents; NW-006 card renders success / State-1-style completed packet from synthetic fixtures; Phase 1 policy encodes permitted stage transition | Note **verified** CRM write; stage `discovery_scheduled → discovery_complete` **verified** write; Firestore `workflow_runs/{run_id}` audit present; deployed full-run evidence | No GHL write auth; no isolated test GHL location; NW-005 PLANNED; NW-007 PLANNED; CRM mutation only under future separately authorized safe-environment lane |
| **AT-2** | **PARTIAL** | Offline Unit 2/3 `AMBIGUOUS_CONTACT` scenarios PASS; fail-closed **0 CRM writes** offline; NW-006 card renders blocked / State-2-style packet; fixture `transcript-ambiguous-contact.txt` present | Single NW-008 acceptance evidence package binding transcript → agents → policy → card → audit; optional live relationship read still unexecuted (NW-013) | NW-008 evidence harness not yet built; NW-005 audit completeness still open; NW-007 if demo requires deploy |
| **AT-3** | **PARTIAL** | Offline stage-denied / no-stage-change paths produce `completed_with_review` + `STAGE_TRANSITION_NOT_ALLOWED`; NW-006 card renders completed_with_review; fixtures present | Note **verified** CRM write while stage remains unchanged; full-run evidence with audit | Mutation write path unauthorized; NW-005; NW-007 for deployed proof |
| **AT-4** | **PARTIAL** | `CONTACT_NOT_FOUND` is a first-class fail-closed code in `contracts/failure_codes.yaml`; blocked disposition machinery and card blocked rendering exist | Dedicated full-run AT evidence path from transcript/fixture package through agents → policy → card → audit with explicit `CONTACT_NOT_FOUND` | NW-008 harness; NW-005; no live CRM required if pure synthetic, but historical AT still expects complete run evidence |
| **AT-5** | **PARTIAL** | `LOW_EXTRACTION_CONFIDENCE` code + `transcript-insufficient-context` fixture + Unit 3 insufficient-context path + NW-006 blocked card rendering | Closed NW-008 acceptance evidence package with 0-write proof and audit record | NW-008 harness; NW-005 |
| **AT-6** | **BLOCKED** | Failure code `GHL_TOOL_FAILURE` and NW-006 failed-card rendering exist; Phase 1 can represent failure dispositions in fixtures | Mutation **attempted: true, verified: false** during an actual/write-path tool failure; honest write-path failure injection | **No GHL writes authorized**; **no isolated GHL test location** (NW-012 retired); canonical location is **not** a test environment; requires future separately authorized safe-environment mutation lane |
| **AT-7** | **BLOCKED** | Failure code `GHL_WRITE_NOT_VERIFIED` exists; completion-must-not-be-declared posture is documented | Write succeeds then read-back mismatch on a real mutation path; verified-false completion denial under execution | Same as AT-6: write/read-back path unauthorized and environmentally unavailable under current lanes |
| **AT-8** | **PARTIAL** | Deterministic OL3/policy layer is implemented offline and is the sole consequential-action authorization surface; per-run caps are a policy concern (not agent choice) by architecture | Enforcement proof during an active mutation-execution run (second note/stage attempt refused while first path is live) | Mutation execution lane not authorized; offline policy proof ≠ full historical AT |
| **AT-9** | **PARTIAL** | GHL tool manifest + Phase 2B offline adapter explicitly deny mutation/contact-create class ops; blocked-tool posture is contract-real | Audit **warnings** recorded on durable `workflow_runs/{run_id}` for the refusal event | NW-005 required for durable audit warnings; mutation/runtime invocation path still governed separately |
| **AT-10** | **DEFERRED** | Run dispositions, reason codes, and agent/tool counts exist in offline packets/proofs; schema intent for audit is documented in foundation | Every run writes `workflow_runs/{run_id}` with agents, tool counts, reason codes, disposition | **NW-005 Firestore audit writer remains PLANNED**; Firestore writes are not authorized under completed lanes |

### Summary counts (planning snapshot)

| Class | ATs |
| --- | --- |
| READY | _(none)_ |
| PARTIAL | AT-1, AT-2, AT-3, AT-4, AT-5, AT-8, AT-9 |
| DEFERRED | AT-10 |
| BLOCKED | AT-6, AT-7 |

**No AT is READY** for full historical satisfaction at this snapshot. Offline
synthetic strength is real and valuable, but the foundation’s AT bar still
requires verified mutations, audit durability, and/or failure-path write
semantics that current grants intentionally withhold.

---

## Cross-cutting constraints (do not weaken)

```text
ISOLATED_GHL_TEST_LOCATION=NO
CANONICAL_GHL_LOCATION_IS_TEST_ENV=NO
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED_UNDER_COMPLETED_LANES=NO
NW005_STATUS=PLANNED
NW007_STATUS=PLANNED
PRODUCTION_CUSTOMER_DATA=FORBIDDEN
RAW_REST=FORBIDDEN
DETERMINISTIC_POLICY=SOLE_CONSEQUENTIAL_ACTION_AUTHORIZATION_SURFACE
NW006_STATUS=MERGED_COMPLETE
EXTERNAL_EFFECTS=0
```

## What NW-006 merge does and does not change

| Claim | Status after PR #15 |
| --- | --- |
| Card can render completed / completed_with_review / blocked / failed from packets | Yes (offline/synthetic) |
| Card re-evaluates policy or executes mutations | **No** |
| AT-1…AT-10 complete because card snapshots pass | **No — forbidden claim** |
| Vertical slice demo fully executable per foundation §18 | **No** |
| Competition acceptance (NW-008) ready to close | **No — planning only** |

## Recommended evidence standard when NW-008 executes later

For each AT marked for execution under a future authorized unit:

1. Preserve the historical expected outcome text unchanged.
2. Bind exact fixture / run IDs / packet hashes / proof paths.
3. Record `GHL_LIVE_CALLS`, `GHL_WRITES`, `FIRESTORE_WRITES`, `EXTERNAL_EFFECTS`.
4. Separate **offline synthetic proof** from **live/safe-environment proof**.
5. Refuse completion claims when any historical clause (verified write, audit
   record, card state, zero-write guarantee, etc.) is unmet.

## STOP

```text
STOP_CODE=NW006_CLOSED_NW008_READINESS_PACKET_READY_FOR_REVIEW
```
