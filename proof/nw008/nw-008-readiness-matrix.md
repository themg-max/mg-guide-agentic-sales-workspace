# NW-008 Readiness Matrix — AT-1…AT-10 (Planning Only)

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Status | **PLANNED** (readiness classification only — no acceptance execution in this unit) |
| Source of historical criteria | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Companion packet | [`nw-008-implementation-packet.md`](./nw-008-implementation-packet.md) |
| NW-006 dependency | **MERGED_COMPLETE** (PR #15) — card surface available offline |
| NW-007 dependency | **MERGED_COMPLETE** (PR #37 merged; Stage B2 deployment evidence exists; proof closeout merged via PR #38) |
| Mutation / write posture | **No GHL writes authorized**; no isolated GHL test location |
| Audit posture | NW-005 Firestore audit writer remains **PLANNED / NOT_AUTHORIZED** unless a newer human grant is recorded on current main |
| Deployment posture | NW-007 Stage B2 deployment evidence exists, but `DEPLOYMENT_AUTHORIZATION=NO` |
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

## Current readiness matrix (post NW-007 merge + NW-007 closeout)

| AT | Historical expected outcome | Current readiness | Current evidence | Remaining gap | Authorization dependency | Recommended next action |
| --- | --- | --- | --- | --- | --- | --- |
| **AT-1** | `transcript-success.txt` full run → `completed`; note `verified`; stage `discovery_scheduled → discovery_complete` verified; audit record present; MG Guide card State 1 | **BLOCKED** | NW-007 decision-card proof is merged complete; deterministic success render and policy semantics are proven offline; synthetic success path remains available for offline review | Live write-path verification still cannot be honestly executed without a safe-environment mutation grant; no isolated GHL test location; no Firestore audit writer under current main | Future safe-environment mutation + audit authorization | Keep this AT deferred behind a separately authorized write path; do not claim full success without a safe-environment lane |
| **AT-2** | `transcript-ambiguous-contact.txt` → `blocked` with `AMBIGUOUS_CONTACT`; 0 CRM writes; MG Guide card State 2 | **PARTIAL** | Offline Unit 2/3 ambiguous-contact path remains valid; deterministic policy + card render produce blocked/zero-write semantics; raw CRM IDs remain absent | No full transcript-to-agent-to-policy-to-card evidence package is yet recorded on main as an executed NW-008 proof bundle | No new mutation authority required for synthetic offline proof; live relationship read remains optional and unexecuted | Execute synthetic AT-2 evidence package without GHL writes; keep live reads unclaimed |
| **AT-3** | `transcript-no-stage-change.txt` → note `verified`; stage unchanged with `STAGE_TRANSITION_NOT_ALLOWED`; disposition `completed_with_review` | **BLOCKED** | Offline stage-denied semantics and the card’s completed-with-review rendering exist; deterministic policy prevents stage write | The historical AT requires a live verified note + stage-write refusal evidence path under a safe-environment mutation lane | Future safe-environment mutation authorization and audit writer | Do not claim completion of AT-3 until write-path evidence exists under explicit authority |
| **AT-4** | Contact not found → `blocked` with `CONTACT_NOT_FOUND`; 0 writes | **PARTIAL** | Offline fail-closed handling and blocked card rendering for contact-not-found is present and synthetic-friendly; no external effects | Historical full-run proof needs a transcript/agent/policy/card evidence package tied to approved synthetic data | No new mutation authority required for synthetic offline evidence; real CRM contact lookup remains unavailable/no live claim | Execute a synthetic AT-4 evidence package with explicit zero-write proof |
| **AT-5** | Extraction confidence below threshold → `blocked` with `LOW_EXTRACTION_CONFIDENCE`; 0 writes | **PARTIAL** | Low-confidence blocked path and card rendering are present in deterministic fixtures; no mutation produced | Full AT evidence still requires a durable transcript/decision-record package under the current audit boundary | No new mutation authority required for synthetic offline proof; no Firestore writes today | Package AT-5 as a synthetic offline decision proof and keep the live write path disclaimed |
| **AT-6** | GHL tool failure during write → `failed` with `GHL_TOOL_FAILURE`; mutation recorded `attempted: true, verified: false` | **BLOCKED** | Failure-code semantics and failed-card rendering exist; no mutation path is available under current grants | Real write-path failure injected on a live GHL tool is not authorized; isolated test service is unavailable and canonical GHL location is not a test environment | Separate safe-environment mutation lane; explicit human authority required | Do not claim AT-6 completion; keep blocked until a governed mutation environment exists |
| **AT-7** | Write succeeds but read-back mismatch → `failed` with `GHL_WRITE_NOT_VERIFIED`; no completion declared | **BLOCKED** | Failure semantics and denial-of-completion posture are documented; deterministic card fail-state exists | Real write/read-back mismatch cannot be executed without GHL mutation + verification path | Separate safe-environment mutation lane + verification authority | Keep AT-7 blocked; no completion claim without live write/read-back evidence |
| **AT-8** | Per-run mutation caps → second note or stage write attempt is refused by OL3 policy, not by agent choice | **PARTIAL** | Deterministic policy remains the sole consequential-action authorization surface; offline policy caps are the right architecture | Full historical proof requires an active policy+execution trace showing the second attempt is refused under live mutation conditions | No new mutation authority required for offline policy proof; live mutation remains unauthorized | Prefer synthetic policy-cap proof package over unverified live mutation execution |
| **AT-9** | Blocked tool invocation (e.g., contact create) → refused at tool-manifest layer; recorded in audit warnings | **PARTIAL** | Tool-manifest refusal posture is documented and offline adapter denies mutation/contact-create class ops | Audit warnings in `workflow_runs/{run_id}` still require authorized Firestore writer or an alternate explicitly allowed audit sink | NW-005 Stage B authorization required for durable audit warnings; no authorizing grant exists on current main | Preserve the offline refusal proof; do not claim audit completion without NW-005 authority |
| **AT-10** | Every run produces a `workflow_runs/{run_id}` record with agents, tool counts, reason codes, disposition | **DEFERRED** | Offline audit schema and run-disposition models exist; NW-007 is merged complete and the decision card is durable | Firestore audit writer is still not authorized under current main; Stage B remains unapproved | NW-005 Stage B authorization required | Keep AT-10 deferred until a human-approved Firestore audit lane is in place |

### Summary counts (current readiness refresh)

| Class | ATs |
| --- | --- |
| READY | _(none)_ |
| PARTIAL | AT-2, AT-4, AT-5, AT-8, AT-9 |
| BLOCKED | AT-1, AT-3, AT-6, AT-7 |
| DEFERRED | AT-10 |

**Recommended first executable tranche:** `AT-2, AT-4, AT-5, AT-8, AT-9`

This tranche is preferred because it:

- requires no new mutation authority;
- uses synthetic / approved data only;
- demonstrates transcript → agents → deterministic policy → decision card;
- can produce strong judge-visible evidence;
- avoids AT-6 / AT-7 write-path behavior;
- does not imply Firestore writes without NW-005 Stage B authorization.

```text
NW008_FIRST_EXECUTABLE_TRANCHE=AT-2,AT-4,AT-5,AT-8,AT-9
NW008_TRANCHE_REQUIRES_NEW_AUTHORIZATION=NO
NW005_STAGE_B_STATUS=PLANNED_NOT_AUTHORIZED
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
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
NW005_STATUS=PLANNED_NOT_AUTHORIZED
NW007_STATUS=MERGED_COMPLETE
NW007_STAGE_B2_DEPLOYMENT_EVIDENCE=AVAILABLE
NW007_DEPLOYMENT_AUTHORIZATION=NO
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
STOP_CODE=NW007_MERGED_COMPLETE_NW008_READINESS_REFRESH_READY_FOR_REVIEW
```
