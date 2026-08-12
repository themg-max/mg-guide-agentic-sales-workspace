# NW-005 Implementation Packet — Firestore Audit Writer (Planning Only)

| Field | Value |
| --- | --- |
| Work item | **NW-005** |
| Title | Bounded Firestore audit writer for `meeting_follow_up_v1` |
| Artifact | `proof/nw005/nw-005-firestore-audit-implementation-packet.md` |
| Packet status | **PLANNING_ONLY** |
| Implementation started | **NO** (`NW005_IMPLEMENTATION_STARTED=NO`) |
| Coding authorized by this packet alone | **NO** — human review first |
| Runtime / cloud / CRM / Firestore writes in this unit | **NONE** |
| Working branch | `feat/nw005-firestore-audit` |
| Branch base | fresh from merged `main` after PR #16 |
| Do **not** reuse | `chore/nw006-closeout-competition-readiness`, `feat/nw006-meeting-follow-up-card` |
| Input contract | `meeting_follow_up_packet_v1` |
| Output contract | `workflow_runs/{run_id}` audit document (projection only) |
| External effects in this docs unit | **0** |
| Data rule | Synthetic / authorized test identities only — **no production or real customer data** |

This packet freezes the **plan, document contract, projection rules, proof
stages, and non-claims** for NW-005. It does **not** authorize or implement
Firestore writes, IAM changes, secret materialization, deployment, CRM access,
policy evaluation, or agent reruns.

---

## 0. Canonical PR #16 binding (preflight)

NW-005 planning starts only after human merge of the NW-006 closeout /
NW-008 readiness docs PR.

```text
PR16_STATE=MERGED
PR16_TITLE=docs(nw006): close NW-006 and publish NW-008 readiness packet
PR16_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/16
PR16_FINAL_REVIEWED_HEAD=3abeee30535f365867de5916fc38f8354245e1a1
PR16_EXACT_HEAD_CI_RUN=31633248471
PR16_EXACT_HEAD_CI_RESULT=SUCCESS
PR16_EXACT_HEAD_CI_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31633248471
PR16_MERGE_SHA=95ffefbbe7f96f2069ad96a3c6814c806563b531
PR16_MERGED_AT=2026-08-12T19:39:23Z
PR16_REVIEW_VERDICT=READY_WITH_NOTES
PR16_BLOCKING_REASON=NONE
LOCAL_MAIN_AT_BRANCH_CREATE=95ffefbbe7f96f2069ad96a3c6814c806563b531
NW005_BRANCH=feat/nw005-firestore-audit
NW005_IMPLEMENTATION_STARTED=NO
FIRESTORE_WRITES=0
GHL_WRITES=0
EXTERNAL_EFFECTS=0
```

Upstream truth at packet authoring:

```text
NW006_STATUS=MERGED_COMPLETE
NW006_PR=15
NW008_STATUS=PLANNED
NW008_PACKET=proof/nw008/nw-008-implementation-packet.md
NW005_STATUS=PLANNED
NW007_STATUS=PLANNED
NW013_STATUS=AUTHORIZED_NOT_EXECUTED
DETERMINISTIC_POLICY=SOLE_CONSEQUENTIAL_ACTION_AUTHORIZATION_SURFACE
RAW_REST=FORBIDDEN
PRODUCTION_ACTIVATION=FORBIDDEN
```

---

## 1. Objective (future implementation units — not this branch docs unit)

Persist a **deterministic operational proof record** for each
`meeting_follow_up_v1` run so AT-10 (audit completeness) can be honestly
satisfied later.

Architecture (hard bound):

```text
meeting_follow_up_packet_v1
  → deterministic audit projection
  → workflow_runs/{run_id}
  → STOP
```

### Authority rule (hard)

| Rule | Requirement |
| --- | --- |
| Audit role | Firestore audit **records outcomes** already present on the packet |
| Authorization role | Firestore **does not** authorize actions |
| Policy | Audit writer **must not** call `evaluate_policy` / deterministic policy gate |
| Agents | Audit writer **must not** rerun any agent (`meeting_context`, `relationship_context`, `follow_up_planning`, ADK runtime) |
| CRM | Audit writer **must not** fetch CRM / relationship context or call GHL |
| Packet | Authoritative input — sole data source for projection |
| Card | May project **already-computable** MG Guide card state via pure deterministic mapper import **or** inline equivalent pure function; must not render for side effects |
| Mutations | Records mutation **intents** and **attempted/verified flags** only; never executes mutations |
| Transcripts | Store **hash + fixture/source refs** only — never full transcript body |

---

## 2. Required packet decisions (frozen for review)

### Decision 1 — Exact `workflow_runs/{run_id}` document contract

**Collection / document path**

```text
workflow_runs/{run_id}
```

- Collection ID: `workflow_runs` (fixed; matches `.env.example` catalog name
  `FIRESTORE_COLLECTION_WORKFLOW_RUNS`).
- Document ID: exact `packet.run.run_id` string (1:1).
- No subcollections in NW-005.
- No alternate sinks authorized (no BigQuery, GCS, local SQLite-as-prod-claim).

**Document schema (public contract v1)** — field names are normative for Stage A
JSON Schema + Stage B Firestore documents:

```yaml
schema: workflow_run_audit_v1
run_id: string                 # == document id == packet.run.run_id
workflow_id: string            # const: meeting_follow_up_v1
started_at: string             # RFC3339 from packet.audit.started_at
completed_at: string|null      # packet.audit.completed_at
terminal_state: string         # see Decision 4
recorded_at: string            # writer clock when projection persisted (Stage B)
                             # Stage A fixture may use fixed synthetic timestamp

# Provenance (Decision 3)
provenance:
  packet_schema: string        # const: meeting_follow_up_packet_v1
  meeting_id: string
  meeting_source: string       # e.g. synthetic_demo
  transcript_hash: string      # 64-char hex; NOT transcript body
  fixture_id: string|null      # synthetic fixture id when known
  packet_run_status: string    # raw packet.run.status
  source_refs: [string]        # proof/fixture/path refs; no secrets
  writer:
    component: string          # e.g. mg_guide.firestore_audit.writer
    component_version: string  # semver or git SHA short when available
    projection_version: string # const: workflow_run_audit_v1
    mode: string               # emulator | local_fixture | firestore_test_project
    write_attempted: boolean
    write_verified: boolean    # true only after successful read-back (Stage B)

# Agent steps / provenance
agent_steps:
  agents_used: [string]        # packet.audit.agents_used (order preserved)
  tools_used: [string]         # packet.audit.tools_used

# Policy outcome (recorded, not re-evaluated)
policy:
  lifecycle: string
  note_write: string
  stage_write: string
  reason_codes: [string]       # packet.policy.reason_codes
  outcome_summary: string      # derived label only; see projection rules

# Reason codes (top-level convenience mirror for AT-10)
reason_codes: [string]         # == policy.reason_codes (deterministic copy)

# Tool call counts (derived; never invented live CRM traffic)
tool_call_counts:
  total_tools_listed: integer  # len(tools_used)
  ghl_mcp:
    reads: integer             # from external_effects breakdown when present; else 0
    writes: integer            # must be 0 under current grants
  firestore:
    reads: integer             # writer read-back count for THIS audit op only
    writes: integer            # 0|1 for THIS audit op (never CRM)
  other: integer               # residual listed tools not classified above

# Mutation intents (from packet.mutation_intents; status only)
mutation_intents:
  note: [{kind, status, body_ref?}]
  stage: [{kind, status, from_stage?, to_stage?}]

# Mutation attempted/verified flags (from packet.mutations)
mutations:
  lifecycle: string
  note:
    attempted: boolean
    verified: boolean
    record_id: string|null     # synthetic/test ids only in public fixtures
  opportunity_stage:
    attempted: boolean
    verified: boolean
    from_stage: string|null
    to_stage: string|null

# CRM resolution summary (no live fetch; packet projection only)
crm_resolution:
  lifecycle: string
  status: string|null
  match_basis: string|null
  candidate_count: integer|null
  # contact_id / opportunity_id: OPTIONAL and REDACTED in public proof
  # exports unless already synthetic demo ids. Stage A fixtures may include
  # synthetic ids; Stage B public artifacts must not introduce real IDs.

# MG Guide card state (deterministic projection)
mg_guide_card:
  card_state: string           # completed | completed_with_review | blocked |
                               # failed | in_progress
  projection_source: string    # packet_status_mapper_v1

# External effect counters
external_effects:
  packet_external_effects: integer|object  # as on packet (int today)
  counters:
    GHL_READS: integer
    GHL_WRITES: integer
    FIRESTORE_READS: integer
    FIRESTORE_WRITES: integer
    EXTERNAL_EFFECTS: integer  # sum of consequential external ops claimed

# Warnings / errors
warnings: [string]             # packet.audit.warnings
errors: [string]               # empty unless terminal_state=failed or
                               # explicit error codes present on packet

# Final disposition mirrors
final_disposition: string|null # packet.audit.final_disposition
brief_headline: string|null    # optional short UX crumb from packet.brief.headline
                               # (not full brief body required)

# Idempotency / integrity
idempotency:
  key: string                  # == run_id
  strategy: string             # create_only_if_absent | reject_if_terminal_conflict
  prior_terminal_state: string|null
  duplicate_write_rejected: boolean

integrity:
  projection_input_fingerprint: string  # sha256 of canonical JSON of mapped fields
  content_fingerprint: string           # sha256 of canonical JSON of stored doc
                                        # excluding recorded_at + write flags that
                                        # legitimately differ on retry metadata
```

**Storage rules (from foundation §13, restated as NW-005 gates)**

- Do **not** store entire transcript text.
- Do **not** store chat memory / multi-turn conversation blobs.
- Do **not** store secrets, tokens, private project numbers, or private SA emails
  in the document body.
- Store: transcript hash, synthetic fixture ID, structured action evidence,
  policy reason codes, tool counts, disposition.
- Firestore holds **operational proof**, not authorization state machines.

Foundation §13 example remains the narrative parent; this packet is the
**implementation-normative** expansion for coding units.

---

### Decision 2 — Deterministic field projection

Projection is a **pure function**:

```text
project_workflow_run_audit(packet: meeting_follow_up_packet_v1) -> workflow_run_audit_v1
```

| Output field | Source / rule |
| --- | --- |
| `run_id` | `packet.run.run_id` (required, non-empty) |
| `workflow_id` | `packet.run.workflow` must equal `meeting_follow_up_v1` else fail closed (no write) |
| `started_at` | `packet.audit.started_at` |
| `completed_at` | `packet.audit.completed_at` |
| `terminal_state` | Decision 4 mapping from `run.status` + `audit.final_disposition` |
| `provenance.*` | `meeting.*`, `run.status`, optional fixture ref arg, writer metadata |
| `agent_steps.agents_used` | `packet.audit.agents_used` (stable order copy) |
| `agent_steps.tools_used` | `packet.audit.tools_used` |
| `policy.*` | direct copy of `packet.policy.*` |
| `policy.outcome_summary` | derived: `PASS` if note or stage allowed and no blocking reason dominating; `BLOCKED` if note_write=blocked or status blocked; `DENIED_PARTIAL` if stage blocked/approval_required with note allowed; `NOT_ATTEMPTED` if policy.lifecycle=not_attempted; never calls policy engine |
| `reason_codes` | copy of `packet.policy.reason_codes` |
| `mutation_intents` | deep copy of `packet.mutation_intents` |
| `mutations` | deep copy of `packet.mutations` note/stage flags |
| `crm_resolution` | subset copy from `packet.crm_resolution` (no enrichment) |
| `mg_guide_card.card_state` | pure map: terminal statuses → themselves; non-terminal → `in_progress`; invalid/missing disposition mismatch → prefer fail-closed `failed` only when packet already indicates failed |
| `external_effects.packet_external_effects` | `packet.external_effects` |
| `external_effects.counters.GHL_*` | **0** unless packet/tools explicitly encode counts; current competition packets use integer `external_effects` and empty `tools_used` → zeros |
| `tool_call_counts.ghl_mcp.writes` | **must be 0** under current grants; if projection ever sees a positive write count it still **only records** it — never performs CRM writes |
| `warnings` | `packet.audit.warnings` |
| `errors` | `[]` unless `terminal_state=failed`, then include final_disposition + reason_codes as error crumbs (no stack traces required) |
| `final_disposition` | `packet.audit.final_disposition` |
| fingerprints | SHA-256 over canonical JCS-like sorted-key JSON of projection body |

**Forbidden in projection module**

- Imports that perform I/O (except the separate writer adapter boundary).
- Calls into `orchestration.policy.evaluate_policy`.
- Calls into agent runtimes / ADK / Gemini.
- Calls into GHL adapters (online or offline) for “refresh.”
- Network clients inside the pure projector.

**Suggested future code layout (not created in this unit)**

```text
src/mg_guide/firestore_audit/
  __init__.py
  models.py              # WorkflowRunAuditV1 dataclasses / TypedDicts
  project.py             # pure projector
  validate.py            # schema validate projection
  writer.py              # Stage B only; gated adapter interface
  emulator_store.py      # Stage A in-memory / emulator facade
  cli.py                 # offline fixture → projection JSON (no cloud)
  __main__.py

contracts/
  workflow_run_audit.schema.json   # new schema file in implementation unit

fixtures/nw005/
  packets/               # may reuse / symlink semantics from fixtures/nw006
  expected_audits/       # golden projections per terminal class

tests/nw005/
  test_project_deterministic.py
  test_idempotency.py
  test_no_policy_import.py
  test_emulator_roundtrip.py   # Stage A
  # test_firestore_test_project_roundtrip.py  # Stage B; default skip
```

---

### Decision 3 — Required provenance fields

Minimum provenance that must appear on every stored/emitted audit record:

| Field | Required | Notes |
| --- | --- | --- |
| `run_id` | YES | Document identity |
| `workflow_id` | YES | `meeting_follow_up_v1` |
| `provenance.packet_schema` | YES | `meeting_follow_up_packet_v1` |
| `provenance.meeting_id` | YES | From packet |
| `provenance.transcript_hash` | YES | 64-hex; no body |
| `provenance.meeting_source` | YES | Prefer `synthetic_demo` |
| `provenance.fixture_id` | CONDITIONAL | Required for fixture-driven proofs |
| `provenance.packet_run_status` | YES | Raw status |
| `provenance.source_refs` | YES | At least one proof/fixture/path ref in proof runs |
| `provenance.writer.component` | YES | Stable module id |
| `provenance.writer.projection_version` | YES | `workflow_run_audit_v1` |
| `provenance.writer.mode` | YES | `local_fixture` / `emulator` / `firestore_test_project` |
| `agent_steps.agents_used` | YES | May be empty list if packet says so |
| `policy.reason_codes` + top-level `reason_codes` | YES | May be empty list |
| `mutations.*.attempted/verified` | YES | Booleans |
| `mg_guide_card.card_state` | YES | Deterministic |
| `external_effects.counters` | YES | Explicit zeros preferred over omission |
| `integrity.projection_input_fingerprint` | YES | |

---

### Decision 4 — Success / blocked / failed record semantics

| Packet `run.status` | `audit.final_disposition` | `terminal_state` | `mg_guide_card.card_state` | Writer behavior |
| --- | --- | --- | --- | --- |
| `completed` | `completed` | `completed` | `completed` | Persist success audit |
| `completed_with_review` | `completed_with_review` | `completed_with_review` | `completed_with_review` | Persist partial-success audit |
| `blocked` | `blocked` | `blocked` | `blocked` | Persist blocked audit (still required for AT-10) |
| `failed` | `failed` | `failed` | `failed` | Persist failed audit (still required) |
| non-terminal (`received`…`writing`, `evaluating`, etc.) | `pending` / null | `non_terminal` | `in_progress` | **Default NW-005: do not write** durable Firestore doc unless explicitly invoked with `allow_non_terminal=true` for debug; Stage A may emit local projection JSON only |
| status vs disposition mismatch | any | fail closed → no cloud write; local validate error | n/a | Surface `AUDIT_PROJECTION_INCONSISTENT` |

**Semantics notes**

- **Success** means the *workflow run* completed under packet truth — not that CRM
  writes occurred. Current NW-006 fixtures are often `mutations.lifecycle=
  intent_only` with `attempted=false`; audit must record that honestly.
- **Blocked** is a first-class durable record (AT-10), not an omission.
- **Failed** records tool/verification failure paths; must keep
  `mutations.*.attempted/verified` truthful (e.g., attempted true, verified false).
- Audit persistence failure is **not** allowed to flip packet policy or invent
  CRM success. Writer errors surface as writer-level failure codes only.

**AT-10 binding (foundation §17)**

> Every run (success, blocked, failed) produces a `workflow_runs/{run_id}`
> record with agents, tool counts, reason codes, disposition.

NW-005 Stage A proves projection completeness offline. Stage B proves durable
store + read-back for synthetic records only. Full AT-10 closeout remains an
NW-008 concern after NW-005 implementation is authorized and merged.

---

### Decision 5 — Idempotency behavior for duplicate `run_id`

Aligned with `contracts/workflow_states.yaml` replay rule:

> Once a `run_id` reaches a terminal state, any subsequent attempt with the same
> `run_id` must be rejected and must not advance workflow or emit additional
> mutation intents.

NW-005 audit store rules:

| Existing doc | New projection | Behavior |
| --- | --- | --- |
| Absent | any terminal | **Create** (Stage B: create-only); set `duplicate_write_rejected=false` |
| Absent | non-terminal | Default **skip cloud write** |
| Present, same `content_fingerprint` (ignoring writer timestamps) | same | **No-op success** (idempotent retry); do not increment logical write counters beyond first verified write; may refresh `recorded_at` only if explicitly allowed — **preferred: leave doc unchanged** |
| Present, terminal T1 | projection terminal T1 with different non-meta fields | **Reject** with `AUDIT_IDEMPOTENCY_CONFLICT`; do not overwrite |
| Present, terminal T1 | projection terminal T2 ≠ T1 | **Reject** with `AUDIT_TERMINAL_STATE_CONFLICT`; do not overwrite |
| Present, non_terminal | terminal | **Allow single upgrade write** only if prior doc was explicitly non-terminal and policy allows upgrade path; NW-005 v1 **prefers never writing non-terminal**, so this path should be rare/disabled by default |
| Present | any | **Never delete** as part of normal write path |

Implementation mechanism (Stage B):

- Prefer Firestore **create** (`create()` / equivalent precondition “doc must not
  exist”) over blind `set()`.
- On already-exists: read-back, compare fingerprints, classify no-op vs conflict.
- In-memory Stage A store mirrors the same truth table.

Audit idempotency **must not** be used as a side channel to authorize CRM
retries.

---

### Decision 6 — Emulator / local fixture strategy (Stage A)

**Goal:** prove schema + projection + idempotency with **zero cloud effects**.

| Element | Plan |
| --- | --- |
| Inputs | Reuse `fixtures/nw006/packets/*.json` terminal classes + any NW-005-specific synthetic packets |
| Golden outputs | `fixtures/nw005/expected_audits/*.json` |
| Store | In-process dict store **and/or** Firestore emulator facade behind the same writer interface |
| Network | Disabled; tests fail if Google cloud client attempts real transport without emulator flag |
| Dependencies | Prefer optional `google-cloud-firestore` only under extra; pure projection tests need no GCP libs |
| CLI | `python -m mg_guide.firestore_audit project --packet PATH --out PATH` (fixture → JSON only) |
| CI | Extend Phase 1 deterministic pytest job **only** with offline tests; no secrets |
| Effect counters | `FIRESTORE_WRITES=0`, `EXTERNAL_EFFECTS=0` for Stage A proof-return |

Stage A acceptance (future coding unit):

1. Golden projection match for completed / completed_with_review / blocked / failed.
2. Idempotency table unit tests (in-memory).
3. Import guard tests: projector module does not import policy/agents/ghl.
4. Schema validation against `workflow_run_audit.schema.json`.
5. No transcript body appears in projection JSON.

---

### Decision 7 — Bounded real Firestore proof strategy (Stage B; separately activated)

Stage B is **not** authorized by this planning packet. It requires a future
human grant (suggested id below) and a separate implementation/proof unit.

| Constraint | Requirement |
| --- | --- |
| Project | Explicitly authorized **test/sandbox** GCP project only |
| Data | Synthetic records only |
| Collection | `workflow_runs` only |
| Ops | Bounded creates + get read-back + delete cleanup |
| Max docs | Small ceiling (see Decision 11) |
| CRM | None |
| Production | Forbidden |
| Public proof | Show redacted evidence (project number redacted if sensitive); SHAs; counters |
| Activation | Separate grant file under `governance/authorizations/` when human approves |

Suggested future grant id (not created now):

```text
MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
```

Stage B sequence (when authorized):

```text
1) load synthetic packet
2) project audit doc
3) create workflow_runs/{run_id}
4) get read-back
5) compare fingerprints / critical fields
6) record counters FIRESTORE_WRITES / FIRESTORE_READS
7) cleanup delete (or TTL) per Decision 10
8) STOP
```

Default test posture: Stage B tests **skipped** unless
`NW005_FIRESTORE_STAGE_B=1` **and** grant marker present **and** project id
matches allowlisted test project env.

---

### Decision 8 — Project / environment classification

| Class | Allowed for NW-005? | Notes |
| --- | --- | --- |
| Local / CI offline | YES (Stage A) | Default |
| Firestore emulator | YES (Stage A optional) | Still zero external prod effects |
| GCP test/sandbox project | CONDITIONAL (Stage B only) | Requires separate human grant; ID UNKNOWN in public docs until provisioned |
| GCP production project | **NO** | Hard forbid |
| Canonical customer GHL location as “test” | **NO** | Unrelated; still not a test env |
| Unclassified / unknown project | **NO** | Fail closed |

Public docs must continue to treat concrete project IDs as **UNKNOWN** until a
sanitized grant mirror records classification without leaking private control
plane paths beyond what SECURITY.md already allows.

Env catalog (names only; already sketched in `.env.example`):

```text
FIRESTORE_PROJECT_ID=          # test/sandbox only when Stage B authorized
FIRESTORE_COLLECTION_WORKFLOW_RUNS=workflow_runs
FIRESTORE_EMULATOR_HOST=       # Stage A optional
GOOGLE_CLOUD_PROJECT=          # must not silently double as prod
NW005_FIRESTORE_STAGE_B=0      # default off
```

---

### Decision 9 — Minimal service identity boundary

| Topic | Decision |
| --- | --- |
| Identity type | Least-privilege GCP principal for **test project only** (user ADC for dev **or** dedicated test SA) |
| Role scope | Prefer custom role or narrow predefined roles limited to datastore create/get/delete on `workflow_runs` path pattern if available; avoid Editor/Owner |
| Secrets | No SA JSON keys in git; no secret value commits; use ADC / secret manager outside repo |
| Public repo | Grant mirrors sanitized; no private SA emails required in public packet |
| IAM changes | **Not authorized** by this planning packet; require separate authority if any project IAM is modified |
| Runtime deploy identity | Out of scope (NW-007) |
| Human operator | Aaron Chandler / repository maintainer for activation decisions |

NW-005 writer identity **must not** hold GHL credentials and **must not** be
reused to expand CRM blast radius.

---

### Decision 10 — Retention / cleanup plan

| Mode | Retention | Cleanup |
| --- | --- | --- |
| Stage A in-memory | Process lifetime | Dropped on process exit |
| Stage A emulator | Local emulator data | `emulator flush` / container recycle in proof scripts |
| Stage B test project | **Short-lived synthetic docs only** | Mandatory cleanup in proof script `finally`: delete `workflow_runs/{run_id}` created by the proof |
| Orphan safety | If delete fails | Record `CLEANUP_FAILED` in proof-return; human follows up; no second unrestricted sweep |
| TTL | Optional Firestore TTL policy on `recorded_at` / `expire_at` field **if** separately authorized; not required for Stage A |
| Production retention | N/A | No production writes |

Proof scripts must log:

```text
DOCS_CREATED=<n>
DOCS_DELETED=<n>
CLEANUP_STATUS=OK|FAILED
```

---

### Decision 11 — Cost ceiling

| Ceiling | Value | Enforcement idea |
| --- | --- | --- |
| Stage A cloud spend | **$0.00** | No cloud calls |
| Stage B max documents created per proof run | **≤ 10** | Hard counter in writer wrapper |
| Stage B max read-backs per proof run | **≤ 20** | Counter |
| Stage B max distinct run_ids | **≤ 10** | Allowlist in proof harness |
| Stage B wall clock | **≤ 10 minutes** | Script timeout |
| Collection fan-out | **1 collection** (`workflow_runs`) | Code allowlist |
| Query fan-out | **No collection group queries**; get-by-id only for proof | Code allowlist |
| Monthly exploratory spend (if any) | Prefer **$0** beyond free-tier emulator; any paid project use needs human note in grant | Process |

If any ceiling would be exceeded: **STOP**, do not continue writes.

---

### Decision 12 — Proof markers

Future proof-return / collab-log markers (names frozen now):

```text
NW005_PACKET_STATUS=PLANNING_ONLY
NW005_IMPLEMENTATION_STARTED=NO
NW005_STAGE_A_STATUS=NOT_STARTED
NW005_STAGE_B_STATUS=NOT_AUTHORIZED
FIRESTORE_WRITES=0
FIRESTORE_READS=0
GHL_WRITES=0
GHL_READS=0
EXTERNAL_EFFECTS=0
POLICY_INVOKED_BY_AUDIT_WRITER=NO
AGENT_RERUN_BY_AUDIT_WRITER=NO
CRM_FETCH_BY_AUDIT_WRITER=NO
RAW_REST=FORBIDDEN
PRODUCTION_ACTIVATION=NO
STOP_CODE=NW005_FIRESTORE_AUDIT_PACKET_READY_FOR_REVIEW
```

After a future Stage A coding unit (preview only):

```text
NW005_STAGE_A_STATUS=PASSED
NW005_IMPLEMENTATION_STARTED=YES
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
```

After a future Stage B proof (preview only):

```text
NW005_STAGE_B_STATUS=PASSED
FIRESTORE_WRITES=<bounded>
FIRESTORE_READS=<bounded>
CLEANUP_STATUS=OK
EXTERNAL_EFFECTS=<firestore only>
```

---

### Decision 13 — STOP condition

**This docs unit STOP**

```text
PACKET_MODE=PLANNING_ONLY
NW005_IMPLEMENTATION_STARTED=NO
NW005_RUNTIME_CHANGES=0
FIRESTORE_WRITES=0
GHL_WRITES=0
CRM_MUTATION_CHANGES=0
DEPLOYMENT_CHANGES=0
IAM_CHANGES=0
SECRET_CHANGES=0
NW007_RUNTIME_CHANGES=0
NW008_RUNTIME_CHANGES=0
NW013_EXECUTED=NO
STOP_CODE=NW005_FIRESTORE_AUDIT_PACKET_READY_FOR_REVIEW
```

**Future implementation unit STOP (preview)** — coding may stop when:

1. Stage A offline tests pass on exact head CI.
2. Import/authority guards pass.
3. No GHL/CRM/deploy/IAM/secret scope creep.
4. Stage B either skipped with explicit `NOT_AUTHORIZED` **or** completed under
   grant with cleanup OK.
5. Ledger + collab log + proof-return agree on SHAs and counters.
6. No claim that AT-10 / NW-008 is complete solely because the writer exists.

---

## 3. Two-stage validation plan (preferred)

### Stage A — deterministic schema/projection + emulator/local tests

- Zero cloud effects.
- Pure projector + schema + in-memory/emulator idempotency.
- CI-safe default.

### Stage B — separately authorized bounded Firestore test-project proof

- Synthetic records only.
- `workflow_runs/{run_id}` only.
- Create + read-back verify + cleanup.
- Not started by this packet.

```text
Stage A (default)          Stage B (separate grant)
─────────────────          ────────────────────────
packet fixtures            same synthetic packets
   │                          │
   ▼                          ▼
project()                  project()
   │                          │
   ▼                          ▼
validate schema            validate schema
   │                          │
   ▼                          ▼
memory/emulator store      test-project create()
   │                          │
   ▼                          ▼
idempotency tests          get read-back + compare
   │                          │
   ▼                          ▼
STOP (offline)             cleanup delete → STOP
```

---

## 4. Hard blocked (this packet and default NW-005 scope)

| Blocked item | Status |
| --- | --- |
| All GHL writes | **BLOCKED** |
| Live CRM mutation | **BLOCKED** |
| Broad CRM read/search | **BLOCKED** |
| Real customer data | **BLOCKED** |
| Policy bypass | **BLOCKED** |
| Agent rerun from audit writer | **BLOCKED** |
| Cloud Run deployment | **BLOCKED** (NW-007) |
| NW-007 implementation | **BLOCKED** |
| NW-008 acceptance execution | **BLOCKED** |
| NW-013 execution | **BLOCKED** |
| Raw REST | **BLOCKED** |
| Unapproved IAM | **BLOCKED** |
| Secret changes without separate authority | **BLOCKED** |
| Production activation | **BLOCKED** |
| Firestore writes during **this** planning unit | **BLOCKED** |

---

## 5. Authorization gates

| Action | Gate now | Notes |
| --- | --- | --- |
| Publish this planning packet | Human PR review | This branch |
| Implement Stage A projector + offline tests | Future coding authorization after packet review | Still `FIRESTORE_WRITES=0` |
| Add `google-cloud-firestore` dependency | Future coding unit | Optional extra preferred |
| Stage B test-project writes | **New** grant required | Suggested `MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1` |
| IAM / secret materialization | Separate authority | Not this packet |
| NW-007 deploy | NW-007 activation | Not this packet |
| GHL writes | Safe-env mutation grant (absent) | Never via audit writer |
| NW-008 AT-10 closeout | NW-008 after NW-005 evidence | Packet alone insufficient |

---

## 6. Relationship to other work items

| Item | Relationship |
| --- | --- |
| NW-004 agents | Produce packets consumed as audit **inputs**; writer must not rerun them |
| NW-006 card | Card state projected into audit; card remains offline renderer |
| NW-008 AT-10 | Depends on durable (or governed alternate) audit sink — NW-005 is the authorized sink plan |
| NW-007 | May host writer later; deploy not required for Stage A |
| NW-013 | Independent optional live CRM read proof; not a dependency to start Stage A |

Dependency arrow (from NW-008 readiness packet, unchanged):

```text
… → NW-005 Firestore audit → NW-007 deploy → NW-008 acceptance/demo
```

---

## 7. Non-goals for this planning packet unit

- Do not implement projector, writer, schema file, fixtures, or tests yet.
- Do not call Firestore emulator or cloud APIs.
- Do not modify IAM, secrets, or `.env` real values.
- Do not execute NW-013, NW-007, or NW-008.
- Do not mark ledger NW-005 as DONE.
- Do not claim AT-10 complete.
- Do not broaden collection design beyond `workflow_runs/{run_id}`.

---

## 8. Exit criteria for future NW-005 closeout (preview only)

NW-005 may move beyond PLANNED only when:

1. `workflow_run_audit.schema.json` exists and matches this contract (or a
   reviewed delta is recorded).
2. Deterministic projector has golden tests for success / blocked / failed /
   completed_with_review.
3. Idempotency conflicts fail closed without overwrite of terminal truth.
4. Authority guards prove no policy/agent/CRM calls from writer path.
5. Stage A proof-return shows `FIRESTORE_WRITES=0` offline success **or** Stage B
   shows bounded writes + cleanup under grant.
6. Public artifacts remain synthetic-data clean.
7. Ledger, collab log, and proof-return agree.

---

## 9. Review checklist (human)

- [ ] PR #16 binding SHAs above match GitHub
- [ ] Architecture remains packet → projection → `workflow_runs/{run_id}` → STOP
- [ ] Authority rule: audit records, does not authorize
- [ ] All 13 decisions are acceptable or explicitly amended in review notes
- [ ] Stage B remains separately gated
- [ ] No implementation files slipped into this docs unit
- [ ] `NW005_IMPLEMENTATION_STARTED=NO`

---

## 10. STOP (this docs unit)

```text
PACKET_MODE=PLANNING_ONLY
NW005_IMPLEMENTATION_STARTED=NO
NW005_RUNTIME_CHANGES=0
FIRESTORE_WRITES=0
FIRESTORE_READS=0
GHL_WRITES=0
GHL_READS=0
EXTERNAL_EFFECTS=0
POLICY_INVOKED_BY_AUDIT_WRITER=NO
AGENT_RERUN_BY_AUDIT_WRITER=NO
CRM_FETCH_BY_AUDIT_WRITER=NO
DEPLOYMENT_CHANGES=0
IAM_CHANGES=0
SECRET_CHANGES=0
NW007_RUNTIME_CHANGES=0
NW008_RUNTIME_CHANGES=0
NW013_EXECUTED=NO
CHANGED_PATH_CLASS=NW005_PLANNING_GOVERNANCE_ONLY
STOP_CODE=NW005_FIRESTORE_AUDIT_PACKET_READY_FOR_REVIEW
```
