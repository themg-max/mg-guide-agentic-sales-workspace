# NW-008 Tranche D — AT-8 / AT-9 Feasibility Packet

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Lane | Tranche D feasibility (planning only) |
| Branch | `chore/nw008-at8-at9-feasibility` |
| Base SHA | `5cd9e32d5fa781dfbb879ff93037e5d0b9eb0772` (PR #45 merge = `origin/main` at planning start) |
| PR #45 head | `9d556b25a7c2f69be3276baa14b80f6c1e33ad25` |
| PR #45 merge SHA | `5cd9e32d5fa781dfbb879ff93037e5d0b9eb0772` |
| PR #45 merged at | `2026-08-14T16:26:19Z` |
| PR45_MERGE_IS_ANCESTOR_OF_ORIGIN_MAIN | `YES` |
| Historical criteria source | [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17 |
| Companion readiness matrix | [`nw-008-readiness-matrix.md`](./nw-008-readiness-matrix.md) |
| Planning posture | **PLANNING_ONLY=YES** — no application/runtime/policy/manifest/audit-schema mutation in this pass |

```text
PLANNING_ONLY=YES
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
TOOL_MANIFEST_CHANGED=NO
AUDIT_SCHEMA_CHANGED=NO
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0
NW013_EXECUTED=NO
NW005_STAGE_B_ACTIVATED=NO
GOOGLE_WORKSPACE_RUNTIME=NO
DEPLOYMENT=NO
AT2_STATUS=HISTORICAL_COMPLETE
AT4_STATUS=HISTORICAL_COMPLETE
AT5_STATUS=HISTORICAL_COMPLETE
NW008_OVERALL_STATUS=IN_PROGRESS
```

---

## 1. Purpose

Determine whether historical **AT-8** and/or **AT-9** can be completed using
**existing** offline execution / policy / audit surfaces **without new
authorization**, after PR #45 closeout.

This packet does **not**:

- reinterpret or weaken §17 clauses;
- authorize GHL writes, Firestore Stage B, NW-013, deployment, or Workspace runtime;
- claim AT-8 / AT-9 historically complete;
- change readiness classifications in the matrix (feasibility only).

Each AT ends in exactly one feasibility state:

```text
OFFLINE_EXECUTABLE
REQUIRES_NEW_AUTHORIZATION
BLOCKED_BY_MISSING_CAPABILITY
```

---

## 2. Authoritative historical criteria (verbatim §17)

Source: `docs/MEETING_FOLLOW_UP_FOUNDATION.md` §17 — preserved without revision.

| # | Test | Expected outcome |
| --- | --- | --- |
| **AT-8** | Per-run mutation caps | Second note or stage write attempt in one run is refused by OL3 policy, not by agent choice |
| **AT-9** | Blocked tool invocation (e.g., contact create) | Refused at tool-manifest layer; recorded in audit warnings |

Supporting foundation invariants (not substitutes for §17, cited only for
boundary fidelity):

- §9 OL3: *“Max one note write and one stage write per run, enforced by OL3
  policy, not by agent self-restraint.”*
- §12 GHL mutation policy: allowlist per run max one `note_create` and one
  `opportunity_stage_update`; mutation authorization is a **separate** grant
  and is **not** implied by this packet.
- Packet audit model (§8): `audit.warnings: [string]`.
- §13 Firestore `workflow_runs/{run_id}` is the **online** audit document shape;
  it is **not** named in the AT-9 expected-outcome clause.

---

## 3. Posture entering feasibility

| Item | State |
| --- | --- |
| Tranche A / B / C | Merged (PR #40 / #42 / #44); PR #45 closeout + acceptance reconciliation on `main` |
| Historical complete | **AT-2, AT-4, AT-5** |
| Remaining | AT-1, AT-3, AT-6, AT-7, **AT-8**, **AT-9**, AT-10 |
| Matrix class for AT-8 / AT-9 | **PARTIAL** + listed as offline-executable candidates |
| Mutation / write posture | No GHL writes authorized; no isolated GHL test location |
| Audit posture | NW-005 **Stage A** offline projection **MERGED_COMPLETE**; Stage B Firestore write **PLANNED_NOT_AUTHORIZED** |
| Partial AT-8 evidence | [`proof/nw008/at-08/`](./at-08/) — `PARTIAL_SUPPORTING_PROOF`; `historical_policy_refusal_trace=NOT_PROVEN` |
| Partial AT-9 evidence | [`proof/nw008/at-09/`](./at-09/) — `PARTIAL_SUPPORTING_PROOF`; `durable_audit_warning_recorded=false` |

---

## 4. AT-8 feasibility inspection

### 4.1 Surfaces inspected (existing only)

| Surface | Path / symbol | Role today |
| --- | --- | --- |
| Deterministic per-run mutation cap policy | [`contracts/workflow_states.yaml`](../../contracts/workflow_states.yaml) invariants `max_note_writes_per_run: 1`, `max_stage_writes_per_run: 1`, `max_note_intents_per_run: 1`, `max_stage_intents_per_run: 1` | Contractual OL3 caps |
| State machine constants | [`src/orchestration/state_machine.py`](../../src/orchestration/state_machine.py) `max_note_intents=1`, `max_stage_intents=1` | Runtime cap constants |
| Intent binding / cardinality guard | [`src/orchestration/policy.py`](../../src/orchestration/policy.py) `bound_intents()` | Raises `ValueError("… intent cardinality exceeded")` if a **single** bound bag exceeds max |
| Policy decision (no I/O) | `evaluate_policy()` / `PolicyDecision` | Permits/denies note/stage **intent** without external effects |
| Mutation execution boundary | [`src/orchestration/runner.py`](../../src/orchestration/runner.py) writing branch | **Intent-only**: sets `mutations.*.attempted=False`, `lifecycle=intent_only`, `external_effects=0`; comment: *“Phase 1: no external mutation execution.”* |
| Mutation attempt fields | [`src/orchestration/models.py`](../../src/orchestration/models.py) `empty_mutations()` | Already models `attempted` / `verified` / `record_id` without requiring live GHL |
| Synthetic / offline adapters | [`src/integrations/ghl/read_adapter.py`](../../src/integrations/ghl/read_adapter.py) `OfflineGhlReadAdapter` | Read-only; mutations denied; no write transport |
| Partial AT-8 harness | [`src/orchestration/nw008_harness.py`](../../src/orchestration/nw008_harness.py) `_run_policy_cap` | Binds first intents via `bound_intents`, then **locally simulates** a second bag with harness-side `if len(...) > max` — not a sequential run-scoped execution ledger |
| Audit / proof representation | Packet `mutations` + `mutation_intents` + NW-008 evidence JSON under `proof/nw008/at-08/` | Can record offline counters; does not yet prove authoritative second-attempt refusal |

### 4.2 Feasibility questions

#### Q1 — Can attempt #1 be represented as policy-permitted / execution-attempted without a live external write?

**YES (with implementation delta; no new authorization).**

- Policy can already emit `note_write=allowed` / `stage_write=allowed` and bind a single planned intent (`bound_intents`).
- Packet mutation records already distinguish `attempted` vs `verified` vs external effects.
- Honest offline model: mark attempt #1 as **policy-permitted intent** and **execution-attempted** under a **synthetic offline executor** that performs **no** GHL transport, keeps `EXTERNAL_EFFECTS=0`, `GHL_WRITES=0`, and does **not** claim live verification.
- This does **not** satisfy AT-1/AT-3 (verified live write). It only needs to show that a first write **attempt** was admitted by policy inside one run.

#### Q2 — Can attempt #2 reach the actual execution/policy boundary and be refused specifically because the per-run cap is exhausted?

**NOT with the current wiring; YES after a bounded offline delta.**

Today:

- `bound_intents()` only ever appends at most one note and one stage from a single `PolicyDecision`, so the cardinality `raise` is unreachable on the normal single-decision path.
- The runner never issues a second sequential write attempt in one run; it stops at intent-only.
- The Tranche A harness proves the **concept** of a second bag by constructing lists in harness code (`historical_policy_refusal_trace=NOT_PROVEN`). That is supporting proof, not historical completion.

Required offline boundary (still using existing cap constants / OL3 ownership):

1. Maintain a **per-run mutation attempt ledger** (note count, stage count) owned by orchestration/policy — not by agent self-restraint.
2. Route sequential attempt #2 through that ledger **before** any external effect.
3. Refuse with a deterministic policy error when `count >= max_*_per_run`, independent of agent choice.

No live GHL grant is required for that refusal path.

#### Q3 — Can proof distinguish the required layers?

| Layer | Feasible offline? | Notes |
| --- | --- | --- |
| `AGENT_PROPOSAL` | YES | Synthetic second proposal / oversized intent bag input |
| `POLICY_PERMITTED_INTENT` | YES | Existing `PolicyDecision` + `mutation_intents` |
| `EXECUTION_ATTEMPT` | YES (delta) | Set `mutations.*.attempted=true` via offline executor; must remain `GHL_WRITES=0` |
| `POLICY_CAP_REFUSAL` | YES (delta) | Ledger/cap enforcer must be the refusing authority (not harness-local `if`) |
| `EXTERNAL_EFFECT` | YES | Counter stays `0`; fail closed if non-zero |

Current partial evidence does **not** yet emit this full layer separation.

#### Q4 — Can the run prove the required counters / authority markers?

Target proof markers (offline):

```text
SECOND_ATTEMPT_REFUSED_BY=DETERMINISTIC_POLICY
SECOND_ATTEMPT_REFUSED_BY_AGENT=NO
GHL_LIVE_CALLS=0
GHL_WRITES=0
EXTERNAL_EFFECTS=0
```

**Feasible** once Q2’s ledger/enforcer is the actual refusal site and the proof
artifact records first-attempt admission vs second-attempt policy refusal.
Not proven today (`NOT_PROVEN` in at-08 details).

#### Q5 — Does any historical wording truly require a live GHL mutation?

**NO.**

§17 AT-8 requires that a **second note or stage write attempt** in one run is
**refused by OL3 policy, not by agent choice**. It does **not** require:

- a successful live GHL write on attempt #1;
- read-back verification;
- production or isolated test-location mutation authority.

Those belong to AT-1 / AT-3 / AT-6 / AT-7 write-path ATs, which remain
**BLOCKED** pending separate mutation grants. Treating AT-8 as live-write-
dependent would **strengthen** the clause beyond §17 and incorrectly collapse
it into the blocked write lane.

### 4.3 AT-8 decision

```text
AT8_FEASIBILITY=OFFLINE_EXECUTABLE
AT8_NEW_AUTHORIZATION_REQUIRED=NO
```

**AT8_REASON=**

Historical AT-8 is a **policy-cap enforcement** clause, not a live CRM success
clause. Contractual caps, state-machine maxima, intent-binding helpers, and
mutation attempt fields already exist offline. What is missing is an
**authoritative per-run attempt ledger + sequential attempt path** that refuses
attempt #2 at the deterministic policy/execution boundary (replacing harness
simulation). That is an implementation gap on existing surfaces, not a missing
external system and not a new authorization domain.

**AT8_REQUIRED_IMPLEMENTATION_DELTA=**

1. Add a run-scoped mutation attempt ledger (note/stage counts) consulted at the
   orchestration execution/policy boundary.
2. Provide an **offline / synthetic** mutation attempt path that can admit
   attempt #1 as `POLICY_PERMITTED_INTENT` + `EXECUTION_ATTEMPT` with
   `attempted=true` and **zero** external effects (no GHL transport).
3. Route attempt #2 through the same boundary so refusal raises/records
   **deterministic policy cap exhaustion** (`POLICY_CAP_REFUSAL`), not agent
   omission and not harness-only simulation.
4. Ensure `bound_intents` / cap enforcer behavior is the authority cited in
   proof (align harness with production boundary; do not keep dual semantics).
5. Emit structured proof distinguishing the five layers in §4.2 Q3.
6. Acceptance tests + `proof/nw008/` artifacts with the Q4 markers.
7. **Do not** change policy numeric caps, allow live GHL, or claim verified
   external writes.

**AT8_REQUIRED_PROOF=**

- Single offline run artifact showing:
  - attempt #1: policy-permitted + execution-attempted (synthetic);
  - attempt #2: refused at deterministic policy cap boundary;
  - `SECOND_ATTEMPT_REFUSED_BY=DETERMINISTIC_POLICY`;
  - `SECOND_ATTEMPT_REFUSED_BY_AGENT=NO`;
  - `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `EXTERNAL_EFFECTS=0`;
  - layer map: `AGENT_PROPOSAL` / `POLICY_PERMITTED_INTENT` /
    `EXECUTION_ATTEMPT` / `POLICY_CAP_REFUSAL` / `EXTERNAL_EFFECT=0`.
- Tests proving refusal still occurs if the agent **proposes** the second write
  (agent choice cannot bypass the ledger).
- Update AT-8 evidence class only when the above is green (out of scope for
  this planning pass).

---

## 5. AT-9 feasibility inspection

### 5.1 Surfaces inspected (existing only)

| Surface | Path / symbol | Role today |
| --- | --- | --- |
| Tool manifest blocked ops | [`contracts/ghl_tool_manifest.yaml`](../../contracts/ghl_tool_manifest.yaml) `ghl_mcp.blocked_capability_classes` includes `contact_create` | Declarative tool-manifest denial list |
| Offline adapter denial | [`OfflineGhlReadAdapter._operation_spec`](../../src/integrations/ghl/read_adapter.py) | Refuses mutations and non-allowlisted ops (e.g. `create-contact`) with `OperationNotAllowedError`; zero I/O |
| Contact-create denial behavior | Harness `_run_tool_manifest_refusal` + adapter | Proves offline refusal strings; does **not** emit audit warnings |
| Packet audit warnings | [`src/orchestration/models.py`](../../src/orchestration/models.py) `audit.warnings: []` | Field exists; runner does not populate on tool refusal |
| `workflow_run_audit_v1.warnings` | [`contracts/workflow_run_audit.schema.json`](../../contracts/workflow_run_audit.schema.json) | Required `string[]`; schema-ready |
| NW-005 Stage A projection | [`src/mg_guide/firestore_audit/project.py`](../../src/mg_guide/firestore_audit/project.py) `project_workflow_run_audit` | Copies `packet.audit.warnings` → audit `warnings` deterministically |
| Offline durable sink | [`src/mg_guide/firestore_audit/memory_store.py`](../../src/mg_guide/firestore_audit/memory_store.py) `MemoryAuditStore` | Terminal-only in-memory persist; zero external effects |
| Proof artifact persistence | NW-008 / NW-005 Stage A proof dirs | Disk JSON/MD proof is the established judge-visible offline pattern |
| Stage B Firestore boundary | [`src/mg_guide/firestore_audit/firestore_store.py`](../../src/mg_guide/firestore_audit/firestore_store.py) + Stage B auth packets | **Not authorized** on current main; not required by §17 AT-9 wording |
| Partial AT-9 harness | `nw008_harness._run_tool_manifest_refusal` | `durable_audit_warning_recorded: false`; remaining gap text still says “authorized audit sink” |

### 5.2 Feasibility questions

#### Q1 — Can an actual blocked tool invocation reach the manifest layer and be refused there without any external effect?

**YES.**

- Manifest already lists `contact_create` under `blocked_capability_classes`.
- `OfflineGhlReadAdapter.build_request("create-contact")` refuses with zero
  network/CRM effect.
- Implementation delta should make a **first-class tool-manifest gate** the
  cited `REFUSAL_LAYER=TOOL_MANIFEST` (load blocked classes from the contract,
  refuse before transport), with the offline adapter remaining a fail-closed
  secondary boundary — not a live MCP call.

#### Q2 — Does that refusal currently emit/produce an audit warning?

**NO.**

- Packet `audit.warnings` stays `[]` through the Phase 1 runner.
- AT-9 partial evidence explicitly sets `durable_audit_warning_recorded: false`.
- No production path appends a warning string on tool-manifest refusal today.

#### Q3 — Can NW-005 Stage A preserve that warning in a durable proof artifact sufficient for the historical clause?

**YES.**

If the run writes a concrete warning into `packet.audit.warnings` (e.g.
`TOOL_MANIFEST_REFUSED:contact_create`):

1. `project_workflow_run_audit` already preserves `warnings` in
   `workflow_run_audit_v1`;
2. `validate_workflow_run_audit` accepts non-empty warning arrays;
3. `MemoryAuditStore.persist` can hold a terminal audit in-process;
4. NW-008 proof can write the projected audit JSON under `proof/nw008/` as the
   durable judge-visible artifact (same pattern as Tranche A/B/C evidence).

No Firestore client, network, or Stage B activation is required for that chain.

#### Q4 — Does the historical clause require Firestore persistence specifically, or merely an audit warning record?

**Merely an audit warning record.**

§17 AT-9 expected outcome (verbatim):  
*“Refused at tool-manifest layer; recorded in audit warnings.”*

It does **not** say:

- `workflow_runs/{run_id}` Firestore document;
- Stage B;
- online durability.

Those appear in **AT-10** (“Every run … produces a `workflow_runs/{run_id}`
record …”) and in the §13 Firestore contract — separate remaining work.

Equating AT-9’s “audit warnings” with authorized Firestore Stage B **over-
interprets** §17 and incorrectly couples AT-9 to AT-10’s deferred lane. This
packet restores clause fidelity: **warning recorded in the audit model +
offline projected proof** satisfies AT-9; Firestore remains optional sink /
AT-10 concern.

#### Q5 — Is Stage B genuinely required, or merely one possible persistence sink?

**Merely one possible persistence sink.**

| Sink | Authorized now? | Sufficient for AT-9 historical clause? |
| --- | --- | --- |
| Packet `audit.warnings` + Stage A `workflow_run_audit_v1` proof artifact | YES (Stage A merged) | **YES** |
| `MemoryAuditStore` (in-process terminal) | YES (Stage A) | YES (supporting) |
| Firestore Stage B `workflow_runs/{run_id}` | **NO** | Not required for AT-9 |

Matrix text that still frames AT-9 as needing Stage B should be treated as a
**readiness over-constraint** relative to §17; correcting that classification
is a follow-on docs/readiness action after implementation proof, not a reason
to demand new authorization here.

### 5.3 Required proof shape (if executed offline)

```text
TOOL_INVOCATION_ATTEMPTED=true
TOOL_MANIFEST_REFUSED=true
REFUSAL_LAYER=TOOL_MANIFEST
AUDIT_WARNING_RECORDED=true
AUDIT_WARNING_ARTIFACT=<path under proof/nw008/…>
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
```

### 5.4 AT-9 decision

```text
AT9_FEASIBILITY=OFFLINE_EXECUTABLE
AT9_STAGE_A_AUDIT_SUFFICIENT=YES
AT9_STAGE_B_FIRESTORE_REQUIRED=NO
AT9_NEW_AUTHORIZATION_REQUIRED=NO
```

**AT9_REASON=**

Historical AT-9 requires (1) a blocked tool invocation refused at the
**tool-manifest** layer and (2) that refusal **recorded in audit warnings**.
Both building blocks exist offline: declarative blocked classes, offline
refusal behavior, packet + `workflow_run_audit_v1` warning fields, Stage A
projector, and proof-dir durability. The gap is **wiring** (invoke → manifest
refuse → append warning → project/persist proof), not missing capability and
not Stage B authorization.

**AT9_REQUIRED_IMPLEMENTATION_DELTA=**

1. Introduce/use a tool-manifest gate that evaluates
   `blocked_capability_classes` (and related allowlisting) **before** any
   external effect; refuse `contact_create` / `create-contact` with
   `REFUSAL_LAYER=TOOL_MANIFEST`.
2. On refusal, append a stable warning string to `packet.audit.warnings` (and
   record tools/agents metadata as appropriate without live calls).
3. Project via NW-005 Stage A to `workflow_run_audit_v1`; validate schema.
4. Persist durable offline proof artifact path under `proof/nw008/` (optional
   `MemoryAuditStore` assertion in tests).
5. Acceptance tests asserting the §5.3 marker set; keep
   `FIRESTORE_WRITES=0`, `NW005_STAGE_B_ACTIVATED=NO`.
6. **Do not** activate Stage B, change manifest blocked semantics beyond
   exercising existing classes, or claim AT-10 complete.

**AT9_REQUIRED_PROOF=**

- Offline run evidence with §5.3 markers all true/zero as specified.
- Artifact file containing projected audit `warnings` including the
  tool-manifest refusal.
- Explicit `REFUSAL_LAYER=TOOL_MANIFEST` (not merely “adapter denied” without
  manifest authority citation).
- Effect counters all zero; no Firestore / GHL live calls.

---

## 6. Cross-cutting boundaries (this planning pass and any future offline execution)

```text
PLANNING_ONLY=YES          # this PR/pass
FUTURE_OFFLINE_IMPL_OK=YES # recommended next lane; still zero external effects

APPLICATION_CODE_CHANGED=NO   # this pass
RUNTIME_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO    # caps and blocked classes stay as contracted
TOOL_MANIFEST_CHANGED=NO
AUDIT_SCHEMA_CHANGED=NO

GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
REAL_CUSTOMER_DATA=0

NW013_EXECUTED=NO
NW005_STAGE_B_ACTIVATED=NO
GOOGLE_WORKSPACE_RUNTIME=NO
DEPLOYMENT=NO
```

Non-goals for AT-8/AT-9 offline completion:

- AT-1 / AT-3 verified write paths;
- AT-6 / AT-7 live failure injection;
- AT-10 Firestore `workflow_runs/{run_id}` completeness;
- NW-013 live synthetic read execution;
- Google Workspace transcript runtime;
- any consequential-action authority beyond deterministic offline policy/tool gates.

---

## 7. Decision summary

```text
AT8_FEASIBILITY=OFFLINE_EXECUTABLE
AT8_NEW_AUTHORIZATION_REQUIRED=NO

AT9_FEASIBILITY=OFFLINE_EXECUTABLE
AT9_STAGE_A_AUDIT_SUFFICIENT=YES
AT9_STAGE_B_FIRESTORE_REQUIRED=NO
AT9_NEW_AUTHORIZATION_REQUIRED=NO

RECOMMENDED_NEXT_IMPLEMENTATION_TARGET=AT-8+AT-9
```

### 7.1 Why `AT-8+AT-9` (not NONE, not single-AT only)

| Lens | Assessment |
| --- | --- |
| **Historical-clause fidelity** | Both clauses are satisfiable **without** live GHL mutation and **without** Firestore Stage B when read verbatim from §17. Neither requires weakening. |
| **Authority** | No new authorization grant is required. Caps and blocked classes are already contracted. Stage A audit projection is already merged. |
| **Implementation scope** | Both deltas are bounded offline orchestration/proof work: per-run attempt ledger + synthetic attempt path (AT-8); manifest gate → warning → Stage A proof (AT-9). Shared zero-effect harness, counters, and proof layout. |
| **Judge-visible value** | Closes the only two remaining **PARTIAL / offline-executable** ATs after Tranche C, demonstrating (a) OL3 policy—not agent choice—enforces per-run caps and (b) tool-manifest refusals leave durable audit warnings — without entering the blocked write lane (AT-1/3/6/7) or deferred AT-10 Firestore lane. |
| **Sequencing note** | If a single-AT slice is forced, prefer **AT-9 first** (smaller wiring surface, Stage A already copies warnings). Prefer **combined tranche** when capacity allows: one offline governance package, one proof return, maximal closure of PARTIAL rows. |

### 7.2 Explicit non-recommendations

- **Do not** wait for NW-005 Stage B to start AT-9 — that couples AT-9 to AT-10 incorrectly.
- **Do not** wait for safe-environment GHL mutation grants to start AT-8 — that couples AT-8 to AT-1/3 incorrectly.
- **Do not** mark either AT historically complete from Tranche A partial proofs alone.

---

## 8. Return block (machine-readable)

```text
BRANCH=chore/nw008-at8-at9-feasibility
BASE_SHA=5cd9e32d5fa781dfbb879ff93037e5d0b9eb0772

AT8_FEASIBILITY=OFFLINE_EXECUTABLE
AT8_NEW_AUTHORIZATION_REQUIRED=NO
AT8_REQUIRED_IMPLEMENTATION_DELTA=per-run mutation attempt ledger + offline synthetic first-attempt execution boundary + second-attempt POLICY_CAP_REFUSAL at deterministic OL3 boundary + layered proof (no live GHL)

AT9_FEASIBILITY=OFFLINE_EXECUTABLE
AT9_STAGE_A_AUDIT_SUFFICIENT=YES
AT9_STAGE_B_FIRESTORE_REQUIRED=NO
AT9_NEW_AUTHORIZATION_REQUIRED=NO
AT9_REQUIRED_IMPLEMENTATION_DELTA=tool-manifest gate refusal for contact_create + emit packet.audit.warnings + NW-005 Stage A project/validate + offline proof artifact (no Firestore Stage B)

RECOMMENDED_NEXT_IMPLEMENTATION_TARGET=AT-8+AT-9

PLANNING_ONLY=YES
APPLICATION_CODE_CHANGED=NO
RUNTIME_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
EXTERNAL_EFFECTS=0

READY_FOR_FEASIBILITY_REVIEW=YES
STOP_CODE=NW008_AT8_AT9_FEASIBILITY_READY_FOR_REVIEW
```

---

## 9. Validation checklist (this pass)

- [x] PR #45 merge SHA is ancestor of `origin/main`
- [x] Fresh branch `chore/nw008-at8-at9-feasibility` from that base
- [x] Single docs artifact created under `proof/nw008/`
- [x] Each AT ends in exactly one feasibility enum
- [x] No application / runtime / test / policy / manifest / schema edits
- [x] No external effects

```text
STOP_CODE=NW008_AT8_AT9_FEASIBILITY_READY_FOR_REVIEW
```
