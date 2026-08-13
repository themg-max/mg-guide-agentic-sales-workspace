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

## 0.1 Review reconciliation (PR #17 draft feedback, applied)

Six review repairs were applied to this packet without changing the core
architecture (`packet → deterministic audit projection → workflow_runs/{run_id}
→ STOP`; audit records, never authorizes):

1. **Audit truth vs persistence proof split** — `write_attempted`,
   `write_verified`, writer-side Firestore op counts, read-back compare, and
   cleanup results moved out of `workflow_run_audit_v1` into the separate
   `nw005_persistence_proof_v1` envelope (Decision 1b) emitted to
   proof-return. The Firestore document never gets a second update merely to
   say its first write succeeded.
2. **Fingerprint semantics normalized** — exact pinned canonicalization
   (algorithm name `nw005_canonical_json_v1`; see §0.2 repair 7) replaces
   "JCS-like";
   `projection_input_fingerprint` hashes the normalized mapped-input subset;
   `content_fingerprint` hashes the immutable audit body **before** the
   fingerprint fields are attached, explicitly excluding `recorded_at`,
   persistence-proof fields, and both fingerprint fields — non-recursive
   (Decision 1c).
3. **`policy.outcome_summary` removed** — the ambiguous display label
   (previously `display_summary_label`) is removed from
   `workflow_run_audit_v1` entirely, along with its projection mapping.
   Authoritative audit truth remains exactly: `policy.lifecycle`,
   `policy.note_write`, `policy.stage_write`, `policy.reason_codes`, and
   `final_disposition` (Decision 2).
4. **MG Guide coupling removed** — the audit writer must not import or render
   `mg_guide.meeting_follow_up_card`; canonical audit field is
   `packet.run.status`; `card_state` comes from a frozen audit-local mapping
   (`audit_status_mapper_v1`) or an upstream-provided value (Decision 2).
5. **Stage B IAM language corrected** — no claim of IAM collection-path
   restriction; server SDK access is IAM/ADC-controlled and bypasses Security
   Rules; least-permission custom role scoped to the actual proof call graph
   in a dedicated test project/database, plus an application-level hard
   allowlist on collection + `run_id` (Decision 9).
6. **Smoke vs acceptance retention separated** — `stage_b_smoke`
   (create → read-back → verify → immediate delete) proves write/read
   correctness only; a separately authorized `acceptance_demo` retention
   window is required before any AT-10 record-presence claim (Decision 10).

## 0.2 Final normalization repairs (PR #17 draft, second review round, applied)

Four further repairs were applied without changing the core architecture:

7. **Canonicalization naming fixed** — the NFC / code-point-sort serializer
   pinned in Decision 1c is **no longer claimed to be RFC 8785 (JCS)**. It is
   now named **`nw005_canonical_json_v1`**: an explicit, packet-local
   canonicalization with fully specified serialization rules and
   golden-byte tests. RFC 8785 differs (e.g. JCS mandates ES2015
   `Number.prototype.toString` formatting for all numbers, not an
   integer-only restriction), so calling this algorithm "RFC 8785 subset"
   was a standards mismatch and has been removed. The alternative of
   implementing literal RFC 8785 semantics was considered and rejected for
   v1 because all numbers in this schema are integers and the pinned rules
   below are simpler to implement and golden-byte-test; any future claim of
   RFC 8785 conformance must ship a true ES2015-number JCS serializer and
   pass the RFC 8785 test vectors.
8. **Pure projection context made explicit** — the conceptual signature is
   now `project_workflow_run_audit(packet, projection_context)` where
   `projection_context` explicitly carries `recorded_at`, `fixture_id`,
   `source_refs`, `writer_component`, `writer_component_version`, and
   `writer_mode`. Same packet + same context must produce byte-identical
   output (Decision 2).
9. **Idempotency observation split** — `workflow_run_audit_v1` retains only
   the *static* idempotency declaration (`idempotency.key`,
   `idempotency.strategy`). The *dynamic* observations
   (`prior_terminal_state`, `duplicate_write_rejected`) moved into the
   `nw005_persistence_proof_v1` envelope, because an immutable
   create-once Firestore document cannot truthfully encode later
   retry/duplicate events (Decision 5).
10. **Tool-count honesty** — `packet.audit.tools_used` is only an array of
    strings; `tool_call_counts.total_tools_listed` renamed to
    **`tools_listed_count`** with an explicit statement that this is **not**
    an invocation count. True tool invocation counts require an explicit
    upstream count/event contract on the packet before the relevant AT-10
    clause can be satisfied (Decision 2 / AT-10 binding).

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
| Card | May project card state **only** via a frozen audit-local pure mapping from `packet.run.status`; must **not** import or render the NW-006 card module (`mg_guide.meeting_follow_up_card`) — no audit→UI runtime dependency |
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
recorded_at: string            # from projection_context.recorded_at (explicit
                             # context input; Stage A fixture uses fixed
                             # synthetic timestamp — see Decision 2)

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
# NOTE: write_attempted / write_verified and writer-side Firestore op counts
# are PERSISTENCE PROOF, not audit truth. They live in the
# nw005_persistence_proof_v1 envelope (Decision 1b) and are never written
# into this document — the doc never gets a second update merely to record
# that its first write succeeded.

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
  # NOTE: no display/summary label field. Authoritative audit truth is
  # exactly policy.lifecycle, policy.note_write, policy.stage_write,
  # policy.reason_codes, and final_disposition.

# Reason codes (top-level convenience mirror for AT-10)
reason_codes: [string]         # == policy.reason_codes (deterministic copy)

# Tool counts (derived; never invented live CRM traffic)
# NOTE: packet.audit.tools_used is ONLY an array of strings. tools_listed_count
# is len(tools_used) — a count of LISTED tool names, NOT an invocation count.
# True tool invocation counts require an explicit upstream count/event contract
# on the packet before the AT-10 tool-count clause can be satisfied.
tool_call_counts:
  tools_listed_count: integer  # len(tools_used); NOT an invocation count
  ghl_mcp:
    reads: integer             # from external_effects breakdown when present; else 0
    writes: integer            # must be 0 under current grants
  # NOTE: the writer's OWN Firestore read/write counts for persisting this
  # audit are persistence proof (Decision 1b envelope), not audit truth, and
  # are excluded from this document.
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

# MG Guide card state (frozen audit-local mapping from packet.run.status;
# the audit writer must NOT import the NW-006 card module — see Decision 2)
mg_guide_card:
  card_state: string           # completed | completed_with_review | blocked |
                               # failed | in_progress
  projection_source: string    # const: audit_status_mapper_v1 (frozen in the
                               # audit module; NOT mg_guide.meeting_follow_up_card)

# External effect counters
external_effects:
  packet_external_effects: integer|object  # as on packet (int today)
  counters:
    GHL_READS: integer
    GHL_WRITES: integer
    EXTERNAL_EFFECTS: integer  # sum of consequential external ops claimed
# FIRESTORE_READS / FIRESTORE_WRITES for the writer's own persistence ops are
# persistence proof (Decision 1b), not packet truth — excluded from this doc.

# Warnings / errors
warnings: [string]             # packet.audit.warnings
errors: [string]               # empty unless terminal_state=failed or
                               # explicit error codes present on packet

# Final disposition mirrors
final_disposition: string|null # packet.audit.final_disposition
brief_headline: string|null    # optional short UX crumb from packet.brief.headline
                               # (not full brief body required)

# Idempotency / integrity
# NOTE: only the STATIC idempotency declaration lives here. Dynamic retry
# observations (prior_terminal_state, duplicate_write_rejected) belong to the
# nw005_persistence_proof_v1 envelope (Decision 1b) — an immutable create-once
# document must not pretend to know later retry events.
idempotency:
  key: string                  # == run_id
  strategy: string             # create_only_if_absent | reject_if_terminal_conflict

integrity:
  projection_input_fingerprint: string  # sha256-hex of canonical JSON of the
                                        # normalized mapped-input subset (Decision 1c)
  content_fingerprint: string           # sha256-hex of canonical JSON of the
                                        # immutable audit body computed BEFORE the
                                        # integrity fields are attached; excludes
                                        # recorded_at, all persistence-proof fields,
                                        # and both fingerprint fields themselves
                                        # (non-recursive — Decision 1c)
```

**Decision 1b — Persistence proof envelope (separate from audit truth)**

`workflow_run_audit_v1` is **immutable packet-derived audit truth**: it is
projected entirely from the packet plus fixed writer identity metadata,
written once (create-only), and never updated merely to record that its own
write succeeded. Evidence that persistence happened is a **separate artifact**
emitted by the proof harness, not a field on the Firestore document:

```yaml
schema: nw005_persistence_proof_v1  # lives in proof/nw005/.../proof-return.yaml; NOT in Firestore
run_id: string
mode: string                        # stage_b_smoke | acceptance_demo (Decision 10)
write_attempted: boolean
write_verified: boolean             # true only after successful read-back compare
idempotency_observation:            # DYNAMIC retry observations — proof artifact
  prior_terminal_state: string|null # only; never fields on the immutable doc
  duplicate_write_rejected: boolean
firestore_ops:
  creates: integer                  # 0|1 per run_id under idempotency rules
  reads: integer                    # bounded read-back count
  deletes: integer                  # cleanup count
read_back_compare:
  content_fingerprint_match: boolean
  mismatched_fields: [string]
cleanup:
  attempted: boolean
  status: string                    # OK | FAILED | NOT_REQUIRED
recorded_at: string                 # proof harness clock
```

Rules:

- The Firestore document **never** receives a second update whose only purpose
  is to say the first write was verified.
- `recorded_at` on the audit document is set once at projection/write time and
  is excluded from `content_fingerprint` (Decision 1c).
- The persistence envelope is the **only** place writer-side op counts,
  read-back comparison results, cleanup results, and dynamic idempotency
  observations (`prior_terminal_state`, `duplicate_write_rejected`) are
  recorded. The immutable Firestore document retains only the static
  declaration (`idempotency.key`, `idempotency.strategy`); it must not
  pretend to know later retry events.

**Decision 1c — Canonicalization and fingerprint semantics (exact, non-recursive)**

Canonical JSON algorithm — name: **`nw005_canonical_json_v1`** (pinned and
golden-byte-tested in Stage A; **not** "JCS-like", and **not** claimed to be
RFC 8785 — see §0.2 repair 7):

1. UTF-8 encoding; strings NFC-normalized before serialization.
2. Object keys sorted by Unicode code point, recursively for nested objects.
3. No insignificant whitespace; separators are exactly `,` and `:`.
4. Strings use minimal JSON escaping (`\"`, `\\`, and `\uXXXX` for control
   characters only).
5. All numbers in this schema are integers; serialized with no decimal point
   and no exponent. Booleans and null use JSON literals.
6. Arrays preserve field-defined order.

This is **`nw005_canonical_json_v1`**, a packet-local canonicalization
inspired by — but **not** claiming conformance to — RFC 8785 (JCS). JCS
mandates ES2015 `Number.prototype.toString` formatting for all numbers;
this schema restricts all numbers to integers (rule 5) and therefore does
not implement the full JCS number serialization. Any future RFC 8785
conformance claim must implement true JCS number semantics and pass the
RFC 8785 test vectors. The implementation pins this exact serializer in the
projection module and unit-tests it against golden byte strings.

- `projection_input_fingerprint` = SHA-256 (lowercase hex) of the canonical
  JSON of the **normalized mapped-input subset**: exactly the packet-derived
  fields enumerated in the Decision 2 projection table, assembled into the
  audit field structure, computed before writer clock fields and integrity
  fields are added.
- `content_fingerprint` = SHA-256 (lowercase hex) of the canonical JSON of the
  **immutable audit body** computed **before** the `integrity` fields are
  attached. The hash input explicitly excludes:
  - `recorded_at` (context-supplied clock input),
  - every persistence-proof field (`write_attempted`, `write_verified`,
    Firestore op counts, read-back compare, cleanup result — all of which live
    in `nw005_persistence_proof_v1`, never in this document), and
  - both `integrity.*` fingerprint fields themselves.

  The definition is therefore **non-recursive**: no hash input ever contains a
  fingerprint field.

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

Projection is a **pure function** with an explicit context parameter:

```text
project_workflow_run_audit(
  packet: meeting_follow_up_packet_v1,
  projection_context: {
    recorded_at: string,              # explicit clock input (fixtures pin a
                                      # fixed synthetic timestamp; Stage B
                                      # harness supplies its own clock value)
    fixture_id: string|null,
    source_refs: [string],
    writer_component: string,         # e.g. mg_guide.firestore_audit.writer
    writer_component_version: string, # semver or git SHA short
    writer_mode: string,              # emulator | local_fixture | firestore_test_project
  }
) -> workflow_run_audit_v1
```

Purity contract: **same packet + same projection_context must produce
byte-identical output** (including both fingerprints). The projector reads no
clocks, env vars, randomness, or I/O on its own — every volatile input
arrives via `projection_context`.

| Output field | Source / rule |
| --- | --- |
| `run_id` | `packet.run.run_id` (required, non-empty) |
| `workflow_id` | `packet.run.workflow` must equal `meeting_follow_up_v1` else fail closed (no write) |
| `started_at` | `packet.audit.started_at` |
| `completed_at` | `packet.audit.completed_at` |
| `terminal_state` | Decision 4 mapping from `run.status` + `audit.final_disposition` |
| `recorded_at` | `projection_context.recorded_at` (never an internally read clock) |
| `provenance.*` | `meeting.*`, `run.status`, `fixture_id`/`source_refs`/writer metadata from `projection_context` |
| `agent_steps.agents_used` | `packet.audit.agents_used` (stable order copy) |
| `agent_steps.tools_used` | `packet.audit.tools_used` |
| `policy.*` | direct copy of `packet.policy.*` (`lifecycle`, `note_write`, `stage_write`, `reason_codes`) |
| `reason_codes` | copy of `packet.policy.reason_codes` |
| `mutation_intents` | deep copy of `packet.mutation_intents` |
| `mutations` | deep copy of `packet.mutations` note/stage flags |
| `crm_resolution` | subset copy from `packet.crm_resolution` (no enrichment) |
| `mg_guide_card.card_state` | Frozen audit-local pure map (`audit_status_mapper_v1`) over `packet.run.status`: terminal statuses → themselves; non-terminal → `in_progress`; status/disposition mismatch → projection fails closed per Decision 4 (no card state emitted). Alternatively the caller may pass an already-produced card-state value into the projection. Must **not** import `mg_guide.meeting_follow_up_card` |
| `external_effects.packet_external_effects` | `packet.external_effects` |
| `external_effects.counters.GHL_*` | **0** unless packet/tools explicitly encode counts; current competition packets use integer `external_effects` and empty `tools_used` → zeros |
| `tool_call_counts.tools_listed_count` | `len(packet.audit.tools_used)` — count of **listed** tool-name strings only; **not** an invocation count. True invocation counts are unavailable until the packet gains an explicit upstream count/event contract; until then the AT-10 tool-count clause cannot be satisfied from this field alone |
| `tool_call_counts.ghl_mcp.writes` | **must be 0** under current grants; if projection ever sees a positive write count it still **only records** it — never performs CRM writes |
| `warnings` | `packet.audit.warnings` |
| `errors` | `[]` unless `terminal_state=failed`, then include final_disposition + reason_codes as error crumbs (no stack traces required) |
| `final_disposition` | `packet.audit.final_disposition` |
| fingerprints | SHA-256 over exact canonical JSON (`nw005_canonical_json_v1`) per Decision 1c (no "JCS-like" ambiguity, no RFC 8785 conformance claim; non-recursive) |

**Forbidden in projection module**

- Imports that perform I/O (except the separate writer adapter boundary).
- Reading system clocks, environment variables, or randomness — all volatile
  inputs arrive exclusively via `projection_context` (purity contract above).
- Imports of `mg_guide.meeting_follow_up_card` or any UI/card renderer — the
  audit layer must not depend on the UI layer at runtime or import time.
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
| `mg_guide_card.card_state` | YES | Frozen audit-local mapping from `packet.run.status`; no UI import |
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
| non-terminal (`received`…`writing`, `evaluating`, etc.) | `pending` / null | `non_terminal` | `in_progress` | **NW-005 v1: never write** a durable Firestore doc; Stage A/debug may emit local projection JSON only. There is no `allow_non_terminal` flag and no non-terminal → terminal durable upgrade path |
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
store + read-back for synthetic records only. Note on tool counts: the audit
record carries `tools_listed_count` (count of listed tool-name strings), which
is **not** an invocation count; true tool invocation counts — and therefore
full satisfaction of the AT-10 tool-count clause — additionally require an
explicit upstream count/event contract on the packet (§0.2 repair 10). A Stage B **smoke** run
(create → read-back → verify → immediate delete) demonstrates write/read
correctness only; it does **not** by itself close AT-10 record presence. AT-10
presence evidence requires either the separately authorized `acceptance_demo`
retention mode (Decision 10) or NW-008's own governed evidence. Full AT-10
closeout remains an NW-008 concern after NW-005 implementation is authorized
and merged.

---

### Decision 5 — Idempotency behavior for duplicate `run_id`

Aligned with `contracts/workflow_states.yaml` replay rule:

> Once a `run_id` reaches a terminal state, any subsequent attempt with the same
> `run_id` must be rejected and must not advance workflow or emit additional
> mutation intents.

NW-005 audit store rules:

NW-005 v1 persists **terminal states only** (`completed`,
`completed_with_review`, `blocked`, `failed`). Non-terminal packets may be
projected locally for Stage A/debug but **MUST NOT** be written to Firestore.
There is no `allow_non_terminal` flag and no non-terminal → terminal durable
upgrade path; the audit writer never consults any "policy allows upgrade"
rule.

Dynamic observations from this table (`prior_terminal_state`,
`duplicate_write_rejected`) are recorded **only** in the
`nw005_persistence_proof_v1` envelope (Decision 1b), never on the immutable
Firestore document, which retains only the static `idempotency.key` /
`idempotency.strategy` declaration (§0.2 repair 9).

| Existing doc | New projection | Behavior |
| --- | --- | --- |
| Absent | any terminal | **Create** (Stage B: create-only); envelope records `duplicate_write_rejected=false` |
| Absent | non-terminal | **Never write** to Firestore (terminal-only persistence); local projection JSON only for Stage A/debug |
| Present, same `projection_input_fingerprint`, same `terminal_state` | same | **No-op success** (idempotent retry); do not increment logical write counters beyond first verified write; leave doc unchanged |
| Present, terminal T1 | projection terminal T1 with different `projection_input_fingerprint` | **Reject** with `AUDIT_IDEMPOTENCY_CONFLICT`; do not overwrite; envelope records `duplicate_write_rejected=true`, `prior_terminal_state=T1` |
| Present, terminal T1 | projection terminal T2 ≠ T1 | **Reject** with `AUDIT_TERMINAL_STATE_CONFLICT`; do not overwrite; envelope records `duplicate_write_rejected=true`, `prior_terminal_state=T1` |
| Present | any | **Never delete** as part of normal write path |

Fingerprint roles: `projection_input_fingerprint` represents the logical
packet/audit truth and drives the idempotency equivalence above;
`content_fingerprint` represents stored-document integrity and remains the
read-back/integrity comparison field (`read_back_compare` in the
`nw005_persistence_proof_v1` envelope).

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
2) project audit doc (+ fingerprints per Decision 1c)
3) create workflow_runs/{run_id} (create-only precondition)
4) get read-back
5) compare fingerprints / critical fields
6) emit nw005_persistence_proof_v1 envelope (write_attempted/verified,
   op counters, read-back compare, cleanup result) into proof-return —
   never as a second update to the Firestore document
7) cleanup per Decision 10 mode:
   - stage_b_smoke: immediate delete
   - acceptance_demo: retain within the separately authorized window, then delete
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
| Access model | Server-side Firestore SDK uses **IAM/ADC** and **bypasses Firestore Security Rules** — Security Rules are not the control for Stage B and must not be cited as one |
| Environment | Dedicated **test project and test database**, isolated from any production or customer-adjacent resource |
| Role scope | Custom role containing **only the permissions the proof call graph actually requires** (verified: e.g. `datastore.entities.create/get/delete`, plus index/list only if the call graph needs them); database-scoped IAM condition where applicable and verified; avoid Editor/Owner. **IAM cannot restrict access to a collection path — this packet makes no such claim** |
| App allowlist | Application-level hard allowlist enforced in writer code: collection must equal `workflow_runs` **and** `run_id` must be in the bounded synthetic proof allowlist (Decision 11) |
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
| Stage B `stage_b_smoke` mode (default) | Zero retention beyond the proof call | create → read-back → verify → **immediate delete** in proof script `finally`; smoke proves write/read correctness only |
| Stage B `acceptance_demo` mode (separately authorized) | Bounded retention window defined in the authorizing grant (long enough for judge/test evidence capture) | Synthetic records remain present for the authorized window so AT-10 record presence can be demonstrated, then deleted; window + run_id allowlist recorded in the sanitized grant mirror |
| AT-10 claim rule | — | Do **not** claim durable AT-10 evidence from a smoke record already deleted in the same proof run |
| Orphan safety | If delete fails | Record `CLEANUP_FAILED` in proof-return; human follows up; no second unrestricted sweep |
| TTL | Optional Firestore TTL policy on `recorded_at` / `expire_at` field **if** separately authorized; not required for Stage A |
| Production retention | N/A | No production writes |

Proof scripts must log:

```text
DOCS_CREATED=<n>
DOCS_DELETED=<n>
CLEANUP_STATUS=OK|FAILED
RETENTION_MODE=stage_b_smoke|acceptance_demo
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
STOP_CODE=NW005_PLANNING_PACKET_FROZEN_READY_FOR_HUMAN_REVIEW
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
NW005_STAGE_B_MODE=stage_b_smoke|acceptance_demo
FIRESTORE_WRITES=<bounded>
FIRESTORE_READS=<bounded>
CLEANUP_STATUS=OK
PERSISTENCE_PROOF_ENVELOPE=nw005_persistence_proof_v1  # in proof-return, not in the Firestore doc
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
STOP_CODE=NW005_PLANNING_PACKET_FROZEN_READY_FOR_HUMAN_REVIEW
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
- Create + read-back verify + cleanup; persistence evidence emitted as the
  `nw005_persistence_proof_v1` envelope (Decision 1b), never as a document update.
- Retention follows Decision 10: `stage_b_smoke` deletes immediately;
  `acceptance_demo` retains within a separately authorized window.
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
| NW-006 card | Card state derived via frozen audit-local mapping from `packet.run.status` (or an upstream-provided value); the audit writer never imports the card module |
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
- [ ] Fingerprint definition is non-recursive with exact canonicalization (Decision 1c)
- [ ] Canonicalization named `nw005_canonical_json_v1`; no RFC 8785 conformance claim (§0.2 repair 7)
- [ ] Projection signature is pure with explicit `projection_context`; same packet + context → identical output (§0.2 repair 8)
- [ ] Dynamic idempotency observations live only in `nw005_persistence_proof_v1` (§0.2 repair 9)
- [ ] `tools_listed_count` is not claimed as an invocation count (§0.2 repair 10)
- [ ] Persistence proof is separated from audit content (Decision 1b)
- [ ] IAM language makes no collection-path restriction claim (Decision 9)
- [ ] Audit writer has no UI dependency ambiguity (Decision 2)
- [ ] Smoke vs acceptance retention semantics are explicit (Decision 10)
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
STOP_CODE=NW005_PLANNING_PACKET_FROZEN_READY_FOR_HUMAN_REVIEW
```
