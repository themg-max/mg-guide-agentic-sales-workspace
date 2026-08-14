# NW-008 Implementation Packet — Acceptance + Demo Proof (Planning Only)

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Title | Acceptance tests AT-1…AT-10 + demo proof |
| Packet status | **PLANNING_ONLY** |
| Implementation in this unit | **NONE** |
| Runtime / cloud / CRM changes in this unit | **NONE** |
| Ledger status target after this docs unit | **PLANNED** (unchanged execution state; readiness now truth-bound) |
| Readiness matrix | [`nw-008-readiness-matrix.md`](./nw-008-readiness-matrix.md) |
| Historical AT source | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17–§18, §20 |
| Data rule | Synthetic / authorized test identities only — **no production or real customer data** |

## Objective (future execution unit — not this branch)

Produce recorded evidence that `meeting_follow_up_v1` satisfies historical
acceptance tests AT-1…AT-10 and can support the foundation’s ~4-minute demo
flow **without silently rewriting the acceptance bar**.

This packet freezes the **plan, dependency order, and non-claims**. It does
**not** authorize or implement:

- CRM mutation execution
- GHL live reads or writes
- Firestore audit writer (NW-005)
- Cloud Run deployment (NW-007)
- Private MG Guide host integration
- NW-013 live synthetic read execution
- Any change to deterministic policy authority

## Upstream truth bindings required before NW-008 closeout

```text
NW006_STATUS=MERGED_COMPLETE
NW006_PR=15
NW006_FINAL_REVIEWED_HEAD=c7d25b447db0a961c17ae26e326ada230b7e4627
NW006_EXACT_HEAD_CI_RUN=31630399411
NW006_EXACT_HEAD_CI_RESULT=SUCCESS
NW006_MERGE_SHA=e22eb861442a37be0797d6d7aec8bb17001fb7a3
NW006_MERGED_AT=2026-08-12T19:12:33Z
NW007_STATUS=MERGED_COMPLETE
NW007_PR=37
NW007_FINAL_REVIEWED_HEAD=22a3b0b3c20373100ca0158cda7a74b4fbc1fb76
NW007_MERGE_SHA=f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6
NW007_MERGED_AT=2026-08-14T09:35:35Z
NW007_STAGE_B2_DEPLOYMENT_EVIDENCE=AVAILABLE
NW007_DEPLOYMENT_AUTHORIZATION=NO
EXTERNAL_EFFECTS=0

NW005_STATUS=PLANNED
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_WRITES_AUTHORIZED=NO
ISOLATED_GHL_TEST_LOCATION=NO
CANONICAL_GHL_LOCATION_IS_TEST_ENV=NO
RAW_REST=FORBIDDEN
DETERMINISTIC_POLICY=SOLE_CONSEQUENTIAL_ACTION_AUTHORIZATION_SURFACE
```

## Bounded dependency sequence (recommended)

Recorded competition sequence for remaining work. Each arrow is a **separately
governed** unit; later units must not start by inventing authority.

```text
1) NW-006 closeout                          [MERGED_COMPLETE]
        ↓
2) optional NW-013 bounded synthetic        [AUTHORIZED_NOT_EXECUTED today]
   live-read execution (exact-ID allowlist;
   canonical location ≠ test env;
   reads only; writes still forbidden)
        ↓
3) NW-005 Firestore audit                   [PLANNED]
   authorization + implementation
   (workflow_runs/{run_id}; no CRM writes)
        ↓
4) NW-007 bounded Cloud Run / test          [MERGED_COMPLETE — evidence exists,
   no new deployment authorization claim]    deployment proof remains staged
   under the governing lane; no production
   CRM writes by merge fact alone
       ↓
5) NW-008 final acceptance / demo proof     [PLANNED — this packet]
   AT-1…AT-10 evidence + §18 demo binding
   under whatever mutation posture is then
   honestly available
       ↓
6) CRM mutation only under a future         [NOT AUTHORIZED NOW]
   separately authorized safe-environment
   lane (not the canonical customer location;
   not production data; policy-gated)
```

### Sequencing notes

- **NW-006 is closed.** Card rendering is available as an offline/synthetic
  dependency for AT card-state clauses.
- **NW-013 is optional but valuable** before any live CRM narrative. It does not
  authorize writes. If left unexecuted, NW-008 must not claim live read
  compatibility.
- **NW-005 before AT-10.** Audit completeness cannot honestly pass without a
  durable `workflow_runs/{run_id}` writer (or an explicitly governed alternate
  audit sink — none is authorized today).
- **NW-007 before claiming deployed demo.** Foundation definition-of-done items
  that require a deployed environment remain open until NW-007 (or an explicit
  governed STOP substituting local-only demo proof).
- **CRM mutation is last and separate.** AT-1/AT-3 verified-write clauses and
  AT-6/AT-7 write-failure clauses remain **unsatisfiable** under current grants.
  They require a future safe-environment mutation lane — **not** silent
  reinterpretation as “intent-only verified.”

## Workstream breakdown (planning)

### A. Evidence harness (NW-008 coding unit — future)

- One acceptance driver that binds:
  - foundation fixtures (`transcript-*.txt` / expected sidecars)
  - agent/policy packet path (Units 1–3)
  - NW-006 card render outcomes
  - audit record expectations (after NW-005)
  - effect counters (`GHL_*`, `FIRESTORE_*`, `EXTERNAL_EFFECTS`)
- Emit per-AT proof stubs under `proof/nw008/at-XX/` (suggested; not created now).
- Fail closed if any historical clause is skipped.

### B. Offline-first AT subset (still not “READY” until evidence package exists)

Candidates for **synthetic offline evidence** after harness exists (still PARTIAL
until package + audit story close):

- AT-2 disposition + 0 writes + card blocked state
- AT-4 / AT-5 blocked paths (with dedicated fixtures where needed)
- AT-8 policy-cap refusal in deterministic offline evaluation
- AT-9 manifest-layer refusal (offline adapter / manifest)

These may become executable offline proofs **without** CRM writes, but they are
**not** automatically complete today and must not be pre-declared READY.

### C. Write-path AT subset (blocked until safe-environment mutation lane)

- AT-1 verified note + verified stage + audit + card State 1
- AT-3 verified note + unchanged stage + reason + completed_with_review
- AT-6 tool failure during write (`attempted: true, verified: false`)
- AT-7 read-back mismatch (`GHL_WRITE_NOT_VERIFIED`)

### D. Audit completeness (deferred to NW-005)

- AT-10 for success, blocked, and failed runs

### E. Demo proof (foundation §18)

Plan to map demo beats to honest capabilities at execution time:

| Demo beat | Dependency honesty |
| --- | --- |
| Friction / trigger / multi-agent work | Units 1–3 offline available now |
| Actual CRM before/after mutation | **Blocked** without safe-environment mutation lane |
| Firestore audit + MG Guide brief | NW-005 + NW-006 (card merged) |
| Ambiguous failure proof (0 writes) | Offline AT-2 path PARTIAL → harness |
| Deployed start-to-finish demo | NW-007 + mutation posture truth |

## Authorization gates (must remain explicit)

| Action | Gate |
| --- | --- |
| Offline synthetic AT harness | Future NW-008 implementation authorization (docs-only now) |
| Firestore `workflow_runs/*` writes | NW-005 authorization |
| Cloud Run deploy | NW-007 activation authority |
| Canonical-location synthetic live read | NW-013 execution unit (already human-authorized; still unexecuted) |
| Any GHL write / stage change / note create | **New** safe-environment mutation grant — **not present** |
| Production / real customer data | **Hard forbid** |
| Raw REST bypass of GHL MCP | **Hard forbid** |
| Policy bypass | **Hard forbid** |

## Non-goals for this planning packet

- Do not implement NW-005, NW-007, or NW-008 runtime.
- Do not execute NW-013.
- Do not open CRM mutation work on this branch.
- Do not mark AT-1…AT-10 complete.
- Do not revise foundation acceptance text to match current offline strength.
- Do not deploy.

## Exit criteria for a future NW-008 closeout (preview only)

NW-008 may move beyond PLANNED only when:

1. Each executed AT has evidence against the **unchanged** historical expected outcome.
2. Unexecuted ATs are explicitly labeled BLOCKED/DEFERRED with authority citations — not hidden.
3. Effect counters are recorded and truthful.
4. Demo proof either runs within authorized environment bounds or records a governed STOP.
5. Ledger/collab log/proof return agree on SHAs, grants, and non-claims.

## STOP (this docs unit)

```text
PACKET_MODE=PLANNING_ONLY
NW008_RUNTIME_CHANGES=0
NW005_RUNTIME_CHANGES=0
NW007_RUNTIME_CHANGES=0
CRM_MUTATION_CHANGES=0
DEPLOYMENT_CHANGES=0
STOP_CODE=NW006_CLOSED_NW008_READINESS_PACKET_READY_FOR_REVIEW
```
