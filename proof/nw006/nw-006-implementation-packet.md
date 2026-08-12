# NW-006 Implementation Packet — MG Guide Meeting Follow-Up Card

| Field | Value |
| --- | --- |
| Work item | **NW-006** |
| Artifact | `proof/nw006/nw-006-implementation-packet.md` |
| Packet status | **BOUNDED_IMPLEMENTATION_PACKET_READY** |
| Implementation started | **NO** |
| Coding authorized by this packet alone | **NO** — review first |
| Baseline PR | **#14 MERGED** |
| Baseline merge SHA (GitHub `main`) | `87d962e05e118e364eb452ce3f367cdb2de08399` |
| Baseline merge title | `docs(phase3): close Unit 3 and prepare NW-006 card plan` |
| Baseline merged at (UTC) | `2026-08-12T18:25:04Z` |
| Working branch | `feat/nw006-meeting-follow-up-card` |
| Branch base | fresh from merged `main` @ `87d962e05e118e364eb452ce3f367cdb2de08399` |
| Do **not** reuse | `feat/meeting-follow-up-v1-follow-up-planning-agent-unit3` |
| Input contract | `meeting_follow_up_packet_v1` |
| External effects target | **0** |
| Mutation controls | **none** |
| CRM / GHL / Firestore / deployment / IAM / secrets | **forbidden** |
| Product surface claim | MG Guide Meeting Follow-Up card; competition-local, host-agnostic renderer/reference component only |

This packet freezes the **exact** UI / runtime / component surface for NW-006
before any card code is written. It supersedes the planning-only envelope in
[`proof/phase3/unit3/nw-006-meeting-follow-up-card-plan.md`](../phase3/unit3/nw-006-meeting-follow-up-card-plan.md)
for implementation bounding, without authorizing live systems.

---

## 1. Objective

Render an already-produced, schema-valid `meeting_follow_up_packet_v1` as a
dedicated **MG Guide Meeting Follow-Up card** through a **deterministic
CardViewModel mapper**, with zero external effects and zero mutation authority.

NW-006 delivers only a **competition-local, host-agnostic card
renderer/reference component**. Private authenticated MG Guide host integration
is explicitly **not delivered** and **not authorized** by NW-006.

```text
meeting_follow_up_packet_v1
  -> deterministic CardViewModel mapper
  -> MG Guide Meeting Follow-Up card
  -> STOP
```

Authority rules (hard):

| Rule | Requirement |
| --- | --- |
| Packet | **Authoritative input** — sole data source for the card |
| Policy | Card **renders** `policy.*` already on the packet; **must not** call `evaluate_policy` |
| Agents | Card **must not** rerun any agent (`meeting_context`, `relationship_context`, `follow_up_planning`, ADK runtime) |
| CRM context | Card **must not** fetch CRM / relationship context |
| Mutation intents | Card **displays** intents only; **must not** execute them |
| GHL | **No** GHL integration (no read adapter use, no live calls, no writes) |
| Firestore | **No** writer / reader |
| Deployment / IAM / secrets | **No** |
| External effects | **EXTERNAL_EFFECTS=0** |

---

## 2. Existing MG Guide application runtime / framework (truth)

### 2.1 What exists in this public repository today

| Surface | Present on baseline? | Notes |
| --- | --- | --- |
| Python package layout under `src/` | **YES** | `agents/`, `orchestration/`, `integrations/` |
| Deterministic OL3 state machine + policy gate | **YES** | `src/orchestration/**` — **upstream of card; not called by card** |
| `meeting_follow_up_packet_v1` assembly | **YES** | Unit 3 `src/agents/follow_up_planning/packet.py` + Phase 1 runner |
| Google ADK agent runtime | **YES** | Units 1–3 — **forbidden import for card** |
| Offline GHL read adapter | **YES** | Phase 2B — **forbidden import for card** |
| React / Vite / Next.js app | **NO** | Not in this repository |
| Streamlit / Dash host | **NO** | Not in this repository |
| Pre-wired authenticated MG Guide HTTP route | **NO** | Pre-existing private product surface is **outside** this repo (baseline claim only) |

### 2.2 Runtime decision for NW-006 (fixed)

Because this public competition repository has **no** pre-existing frontend host,
NW-006 implements the **competition-local, host-agnostic MG Guide Meeting
Follow-Up card module** as a **pure-Python, side-effect-free render path** that:

1. Accepts a completed (or explicitly non-terminal) `meeting_follow_up_packet_v1`
   document already on disk / in memory.
2. Maps it deterministically to a `CardViewModel`.
3. Renders **card chrome** as structured text + static HTML suitable for demo
   review and pytest assertions.
4. Does **not** stand up Cloud Run, does **not** bind private authenticated MG
   Guide host routes, and does **not** introduce a network server requirement
   for tests.

**Framework stack (allowed):**

| Layer | Choice | Rationale |
| --- | --- | --- |
| Language | Python 3.9+ (repo standard) | Matches `pyproject.toml` / pytest |
| Mapper | Pure functions + dataclasses / Typed structures | Deterministic, no I/O |
| Card chrome | Structured plain-text + static HTML string builder | No JS framework dependency; demo-visible card |
| Optional offline CLI | `python -m mg_guide.meeting_follow_up_card` | Fixture → stdout / file only |
| Test runner | `pytest` (existing) | No new test framework |
| Schema validation (optional at boundary) | `jsonschema` (already depended) | Validate packet **shape** only; never re-run policy |

**Framework stack (forbidden for NW-006):**

- Live HTTP servers as a required runtime for acceptance
- Browser automation as a required gate
- Any CRM/GHL/Firestore/GCP client
- Any ADK / Gemini invocation from the card path
- Any call into `orchestration.policy.evaluate_policy`
- Any call into agent harnesses / runners that produce packets

**Product surface class (unchanged from foundation §14):**

> Not another chat response. A dedicated **Meeting Follow-Up card**.

Reference: [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §14.

---

## 3. Exact repository / component paths

### 3.1 New implementation root (only card surface)

```text
src/mg_guide/
  __init__.py
  meeting_follow_up_card/
    __init__.py                 # public exports: map_packet_to_card, render_card_*
    models.py                   # CardViewModel + enums (pure data)
    mapper.py                   # meeting_follow_up_packet_v1 -> CardViewModel
    render_text.py              # CardViewModel -> plain-text card chrome
    render_html.py              # CardViewModel -> static HTML card chrome
    cli.py                      # offline fixture/file loader + print (no network)
    __main__.py                 # python -m mg_guide.meeting_follow_up_card
```

### 3.2 Synthetic fixtures (card-only packets)

```text
fixtures/nw006/
  packets/
    packet-success.completed.json
    packet-stage-change-denied.completed_with_review.json
    packet-ambiguous-contact.blocked.json
    packet-ambiguous-opportunity.blocked.json
    packet-no-opportunity.blocked.json
    packet-insufficient-context.blocked.json
    packet-tool-failure.failed.json
    packet-non-terminal.evaluating.json
  expected/
    card-success.json
    card-stage-change-denied.json
    card-ambiguous-contact.json
    card-ambiguous-opportunity.json
    card-no-opportunity.json
    card-insufficient-context.json
    card-tool-failure.json
    card-non-terminal.json
```

Packet fixtures are **static JSON** snapshots of schema-valid
`meeting_follow_up_packet_v1` documents. They are the **only** runtime input to
the card under test. They are **not** live CRM exports.

### 3.3 Tests

```text
tests/mg_guide/meeting_follow_up_card/
  test_mapper_terminal_states.py
  test_mapper_non_terminal.py
  test_render_text_and_html.py
  test_no_forbidden_imports.py
  test_external_effects_zero.py
```

### 3.4 Proof / closeout (after implementation is green — not this packet)

```text
proof/nw006/
  nw-006-implementation-packet.md   # THIS artifact (planning/envelope)
  proof-return.yaml                 # post-implementation only
  closeout.md                       # post-implementation only
```

### 3.5 Contracts reused (read-only; no mutation of CRM contracts required)

| Path | Use |
| --- | --- |
| `contracts/meeting_follow_up_packet.schema.json` | Validate input packet shape at card boundary (optional but recommended) |
| `contracts/failure_codes.yaml` | Display vocabulary for reason codes (read-only reference) |
| `contracts/workflow_states.yaml` | Terminal vs non-terminal status vocabulary (read-only reference) |

**No new CRM / GHL / Firestore schemas** are authorized in NW-006.

---

## 4. Exact allowed files (implementation unit)

### 4.1 Allowed to create / edit

| Path pattern | Purpose |
| --- | --- |
| `src/mg_guide/**` | Card module only |
| `fixtures/nw006/**` | Synthetic packet + expected CardViewModel fixtures |
| `tests/mg_guide/meeting_follow_up_card/**` | Card unit/acceptance tests |
| `contracts/mg_guide_meeting_follow_up_card.schema.json` | **Required** CardViewModel contract for NW-006 |
| `proof/nw006/**` | Packet, proof-return, closeout (sanitized) |
| `competition/NEW_WORK_LEDGER.md` | NW-006 status reconciliation **after** green tests only |
| `competition/AI_COLLABORATION_LOG.md` | Session log after green tests only |
| `README.md` | Status line only after green tests (no architecture rewrite) |

### 4.2 Explicitly forbidden paths / surfaces

| Path / surface | Why forbidden |
| --- | --- |
| `src/integrations/ghl/**` | No GHL integration on card |
| `src/agents/**` | No agent rerun / no packet production from card |
| `src/orchestration/policy.py` | No `evaluate_policy` from card |
| `src/orchestration/runner.py` | Card must not drive workflow |
| `src/agents/adk_runtime/**` | No ADK from card |
| Firestore clients / `workflow_runs/**` paths | No audit writer (NW-005) |
| Cloud Run / Dockerfile / deploy manifests | NW-007 |
| IAM / Secret Manager / `.env` secrets | Out of scope |
| Live network clients | EXTERNAL_EFFECTS must remain 0 |
| Mutation execution APIs | No approve-and-write controls |
| `contracts/**` except `contracts/mg_guide_meeting_follow_up_card.schema.json` | No other contract modifications authorized in NW-006 |

### 4.3 Import allowlist for `src/mg_guide/meeting_follow_up_card/**`

**Allowed:**

- Python stdlib (`dataclasses`, `enum`, `json`, `pathlib`, `typing`, `html`, …)
- `jsonschema` (optional packet shape check only)
- sibling modules inside `mg_guide.meeting_follow_up_card`

**Forbidden imports (enforced by test):**

```text
orchestration.policy
orchestration.runner
orchestration.state_machine
agents
agents.follow_up_planning
agents.meeting_context
agents.relationship_context
agents.adk_runtime
integrations
integrations.ghl
google.cloud
google.adk
firebase
firestore
requests
httpx
urllib.request   # (network use)
```

Card tests may load fixtures via stdlib `json` + `pathlib` only.

---

## 5. CardViewModel contract

### 5.1 Conceptual type (normative)

```text
CardViewModel
  schema: "mg_guide_meeting_follow_up_card_v1"
  card_state: CardState
  run:
    run_id: string
    workflow: "meeting_follow_up_v1"
    packet_status: PacketStatus          # echo of packet.run.status
    created_at: string | null
  meeting:
    meeting_id: string
    occurred_at: string | null
    title: string                        # e.g. "{Prospect} — Discovery Meeting"
  framing:
    tone: "success" | "review" | "blocked" | "failed" | "in_progress"
    headline: string
    body: string
    no_crm_changes_made: bool            # explicit UX banner when true
  policy_display:
    note_write: string                   # echo only
    stage_write: string                  # echo only
    reason_codes: string[]               # echo only; never recomputed
  ui_integrity:
    errors: string[]                     # card-local UI/integrity errors only
  crm_display:
    resolution_status: string | null     # echo packet.crm_resolution.status
    match_basis: string | null
    candidate_count: int | null
    current_stage: string | null
  metadata:
    contact_id: string | null            # non-renderable metadata only
    opportunity_id: string | null        # non-renderable metadata only
  learning:
    summary: string | null
    needs: string[]
    objections: string[]
    next_step_action: string | null
    next_step_owner: string | null
  intents_display:
    note: IntentDisplay[]                # from mutation_intents.note only
    stage: IntentDisplay[]               # from mutation_intents.stage only
    note_execution_attempted: bool       # from mutations.note.attempted
    stage_execution_attempted: bool
  brief_display:
    headline: string | null
    next_action: string | null
    crm_actions: string[]
    salesperson_attention_required: bool | null   # preserve packet nullability
  controls:
    mutation_controls_enabled: false     # CONSTANT
    agent_rerun_enabled: false           # CONSTANT
    policy_reeval_enabled: false         # CONSTANT
    allowed_human_actions: HumanAction[] # acknowledge | copy_note_text | escalate_offline
  integrity:
    external_effects: 0                  # CONSTANT for NW-006 renders
    source_schema: "meeting_follow_up_packet_v1"
    mapper_id: "meeting_follow_up_card_mapper_v1"
```

```text
CardState =
  | "completed"
  | "completed_with_review"
  | "blocked"
  | "failed"
  | "in_progress"

PacketStatus =
  | "received" | "extracting" | "resolving" | "evaluating" | "writing"
  | "completed" | "completed_with_review" | "blocked" | "failed"

HumanAction =
  | "acknowledge"
  | "copy_note_text_offline"
  | "escalate_offline"
  | "wait"                    # non-terminal only

IntentDisplay =
  kind: "note" | "stage"
  status: string | null
  summary: string             # human-readable; no executable payload
  from_stage: string | null
  to_stage: string | null
```

### 5.2 Mapper purity rules

1. **Total function over packet JSON** — same packet bytes ⇒ same CardViewModel
   fields (ignore only explicit render clocks if any; prefer zero clocks).
2. **No hidden defaults that invent CRM facts** — missing contact/opportunity
   stay null; never fabricate IDs.
3. **Reason codes pass through** from `packet.policy.reason_codes` (and are not
   sorted into a different semantic meaning). Display order may be stable-sorted
   for determinism **without dropping/adding codes**.
4. **Intents are display projections** of `packet.mutation_intents` only.
5. **`controls.mutation_controls_enabled` is always `false`.**
6. **`integrity.external_effects` is always `0` on the view model** for NW-006
   (card does not perform effects; it may also assert `packet.external_effects == 0`
   and fail closed to a `failed` chrome if a packet claims nonzero effects —
   still without executing anything).

### 5.3 Required CardViewModel schema contract

NW-006 **must** define and validate against:

```text
contracts/mg_guide_meeting_follow_up_card.schema.json
```

This contract is **required** and must not redefine policy authority.

### 5.4 Input-integrity invariant (required fail-closed behavior)

Before mapping a packet to a normal card state, enforce:

```text
packet.external_effects == 0
packet.mutations.lifecycle in {"not_attempted", "intent_only"}
packet.mutations.note.attempted == false
packet.mutations.note.verified == false
packet.mutations.opportunity_stage.attempted == false
packet.mutations.opportunity_stage.verified == false
```

Any violation is NW-006 out-of-scope input and must:

1. be rejected as out-of-scope input, or
2. render failed chrome with `CARD_INPUT_OUT_OF_SCOPE`

In both paths, the card must never claim verified CRM effects.

Out-of-scope failed framing body (normative):

```text
Input is outside the NW-006 zero-effect display envelope.
This card did not perform CRM changes.
```

`no_crm_changes_made` / equivalent copy must describe this card path only, not
unverified upstream CRM effects.

### 5.5 Error provenance separation

`policy_display.reason_codes` is only for deterministic policy reason codes
echoed from the packet.

`ui_integrity.errors` is only for card/UI integrity errors.

`CARD_INPUT_INVALID` and `CARD_INPUT_OUT_OF_SCOPE` are UI/card errors and must
not be inserted into `policy_display.reason_codes`.

---

## 6. Terminal-state mapping (UI acceptance)

Packet `run.status` is the primary driver. Scenario labels below are acceptance
names from the vertical slice; the card maps **packet fields**, not scenario IDs.

| Acceptance scenario | Packet condition (authoritative) | `CardState` | Framing tone | `no_crm_changes_made` | Notes |
| --- | --- | --- | --- | --- | --- |
| **SUCCESS** | `run.status == "completed"` | `completed` | `success` | `true` if both mutation `attempted` flags are false (Phase 3 intent-only baseline); never claim live CRM write success unless packet `mutations.*.verified == true` **and** future grant exists — **NW-006 must not fake verified writes** | Show resolved contact summary, permitted planned intents, brief next step |
| **STAGE_CHANGE_DENIED** | `run.status == "completed_with_review"` **and** reason codes include `STAGE_TRANSITION_NOT_ALLOWED` (typical) | `completed_with_review` | `review` | same honesty rule as above | Preserve stage denial codes; note intent may display; stage intent absent/flagged |
| **AMBIGUOUS_CONTACT** | `run.status == "blocked"` **and** `AMBIGUOUS_CONTACT` ∈ reason codes | `blocked` | `blocked` | **`true` (required copy)** | Zero mutation intents expected |
| **AMBIGUOUS_OPPORTUNITY** | `run.status == "blocked"` **and** `AMBIGUOUS_OPPORTUNITY` ∈ reason codes | `blocked` | `blocked` | **`true`** | Zero mutation intents expected |
| **NO_OPPORTUNITY** | `run.status == "blocked"` **and** (`OPPORTUNITY_NOT_FOUND` ∈ reason codes **or** `crm_resolution.status == "opportunity_missing"`) | `blocked` | `blocked` | **`true`** | Do not offer stage intent |
| **INSUFFICIENT_CONTEXT** | `run.status == "blocked"` **and** (`LOW_EXTRACTION_CONFIDENCE` ∈ reason codes **or** equivalent insufficient path already on packet) | `blocked` | `blocked` | **`true`** | No fabricated CRM facts |
| **FAILED packet** | `run.status == "failed"` | `failed` | `failed` | **`true`** | Show failure codes (e.g. `GHL_TOOL_FAILURE`, `GHL_WRITE_NOT_VERIFIED`); no retry-from-card |
| **NON_TERMINAL packet** | `run.status ∈ {received, extracting, resolving, evaluating, writing}` | `in_progress` | `in_progress` | **`true`** | **Never** map to completed/blocked/failed chrome |

### 6.1 Additional mapping rules

1. If `run.status` is terminal (`completed` | `completed_with_review` | `blocked` | `failed`),
   `card_state` **equals** that status string (1:1).
2. If `run.status` is non-terminal, `card_state` is **always** `in_progress`
   (preferred NW-006 behavior: distinct in-progress chrome; never a terminal claim).
3. Unknown / missing `run.status` → treat as render error → `failed` chrome with
   a **card-local** UI error `CARD_INPUT_INVALID` (display only; do not write
   into packet; do not call policy; do not place in policy reason codes).
4. Card **does not** reinterpret `completed` into `completed_with_review` based on
   reason codes; packet status wins. Reason codes are still displayed.
5. Foundation demo copy (“Meeting note created”, “Opportunity moved”) is **only**
   allowed when the packet records verified mutation success. Under the current
   baseline (`mutations.lifecycle == "intent_only"`, `attempted: false`), the card
   must say **planned / authorized intent** language, not “created/moved in CRM”.

### 6.2 Required UX copy anchors

| State | Required user-visible anchor |
| --- | --- |
| `blocked` | **“No CRM changes were made by this card.”** |
| `failed` | Failure framing + reason codes; no mutation controls |
| `completed_with_review` | Explicit review needed; show stage denial when present |
| `completed` | Success framing for a clean terminal packet; intents shown as planned when not verified |
| `in_progress` | “Follow-up not ready” / in-progress shell; **no** completed/blocked/failed wording |

### 6.3 Human actions by state

| `CardState` | Allowed human actions (display only) |
| --- | --- |
| `completed` | `acknowledge`, `copy_note_text_offline` |
| `completed_with_review` | `acknowledge`, `copy_note_text_offline`, `escalate_offline` |
| `blocked` | `escalate_offline` |
| `failed` | `escalate_offline` |
| `in_progress` | `wait` |

No action executes CRM mutations. “Copy note text” is clipboard/offline text only
inside the local demo renderer (tests assert string availability, not OS clipboard).

---

## 7. Non-terminal behavior

```text
NON_TERMINAL statuses:
  received | extracting | resolving | evaluating | writing
```

| Behavior | Rule |
| --- | --- |
| Preferred chrome | Dedicated **in_progress / not ready** card shell |
| Terminal claim | **Forbidden** |
| Invented reason codes | **Forbidden** |
| Mutation controls | **Forbidden** (already globally false) |
| Agent poll / resume | **Forbidden** in NW-006 |
| Alternate allowed | Reject non-terminal input with a clear “packet not terminal” message **without** mapping to `completed`/`blocked`/`failed` success semantics — still surfaces as `in_progress` or invalid input, never a false terminal |

---

## 8. Synthetic fixture strategy

### 8.1 Principles

1. **Synthetic identities only** (Taylor Morgan, Casey, Morgan Case, Sam Unlisted, …).
2. Card fixtures are **pre-baked packets**, not live generator output during tests.
3. Fixture production **may** use Unit 3 / Phase 1 harnesses **offline once** on the
   implementation branch to mint JSON, then check in the snapshots. Runtime card
   tests **must not** call those harnesses.
4. Every acceptance scenario in §6 has exactly one packet fixture and one expected
   CardViewModel fixture.
5. `external_effects` on every packet fixture is `0`.
6. No real customer data, no production IDs, no secrets.
7. Card fixtures may contain synthetic CRM IDs in packet metadata, but text/HTML
   rendering tests must assert no raw `contact_id` / `opportunity_id` leakage.

### 8.2 Scenario → fixture map

| Scenario | Packet fixture | Expected card fixture |
| --- | --- | --- |
| SUCCESS | `fixtures/nw006/packets/packet-success.completed.json` | `.../expected/card-success.json` |
| STAGE_CHANGE_DENIED | `.../packet-stage-change-denied.completed_with_review.json` | `.../card-stage-change-denied.json` |
| AMBIGUOUS_CONTACT | `.../packet-ambiguous-contact.blocked.json` | `.../card-ambiguous-contact.json` |
| AMBIGUOUS_OPPORTUNITY | `.../packet-ambiguous-opportunity.blocked.json` | `.../card-ambiguous-opportunity.json` |
| NO_OPPORTUNITY | `.../packet-no-opportunity.blocked.json` | `.../card-no-opportunity.json` |
| INSUFFICIENT_CONTEXT | `.../packet-insufficient-context.blocked.json` | `.../card-insufficient-context.json` |
| FAILED | `.../packet-tool-failure.failed.json` | `.../card-tool-failure.json` |
| NON_TERMINAL | `.../packet-non-terminal.evaluating.json` | `.../card-non-terminal.json` |

### 8.3 Provenance sources (for minting snapshots only)

| Scenario | Upstream synthetic source (minting aid; not a card runtime dep) |
| --- | --- |
| SUCCESS | `fixtures/transcript-success.expected.json` → Phase 1 runner or Unit 3 harness |
| STAGE_CHANGE_DENIED | `fixtures/transcript-stage-change-denied.expected.json` / `transcript-no-stage-change.expected.json` |
| AMBIGUOUS_CONTACT | `fixtures/transcript-ambiguous-contact.expected.json` |
| AMBIGUOUS_OPPORTUNITY | `fixtures/transcript-ambiguous-opportunity.expected.json` |
| NO_OPPORTUNITY | Synthetic packet with `crm_resolution.status=opportunity_missing` / `OPPORTUNITY_NOT_FOUND` |
| INSUFFICIENT_CONTEXT | `fixtures/transcript-insufficient-context.expected.json` |
| FAILED | Hand-authored synthetic packet: `run.status=failed`, reason `GHL_TOOL_FAILURE`, empty intents |
| NON_TERMINAL | Hand-authored synthetic packet: `run.status=evaluating`, policy lifecycle `not_attempted` or mid-run fields |

---

## 9. Test commands

Primary (implementation gate):

```bash
pytest tests/mg_guide/meeting_follow_up_card -q
```

Broader regression (must remain green; card must not break upstream):

```bash
pytest -q
```

Optional offline demo (non-CI authority; stdout only):

```bash
python -m mg_guide.meeting_follow_up_card \
  --packet fixtures/nw006/packets/packet-success.completed.json \
  --format text
```

CLI must write to stdout only. No module-owned file writes are allowed. Demo
files may be produced only by shell redirection outside the module.

**CI:** reuse existing `.github/workflows/phase1-deterministic.yml` pytest path;
do not add secret-bearing workflows. No deploy jobs.

---

## 10. Proof obligations (post-implementation)

Required markers in `proof/nw006/proof-return.yaml`:

```text
NW006_STATUS=IMPLEMENTED_PENDING_MERGE   # or MERGED_COMPLETE on closeout
NW006_CARD_IMPLEMENTED=YES
CARD_INPUT_CONTRACT=meeting_follow_up_packet_v1
CARD_VIEWMODEL_MAPPER=deterministic
CARD_POLICY_REEVAL=NO
CARD_AGENT_RERUN=NO
CARD_CRM_FETCH=NO
CARD_MUTATION_CONTROLS=NONE
CARD_GHL_INTEGRATION=NO
CARD_FIRESTORE_WRITER=NO
CARD_DEPLOYMENT=NO
EXTERNAL_EFFECTS=0
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
REAL_CUSTOMER_DATA=0
```

Scenario proof matrix (all must PASS):

| Scenario | Required |
| --- | --- |
| SUCCESS → `completed` | PASS |
| STAGE_CHANGE_DENIED → `completed_with_review` | PASS |
| AMBIGUOUS_CONTACT → `blocked` | PASS |
| AMBIGUOUS_OPPORTUNITY → `blocked` | PASS |
| NO_OPPORTUNITY → `blocked` | PASS |
| INSUFFICIENT_CONTEXT → `blocked` | PASS |
| FAILED packet → `failed` | PASS |
| NON_TERMINAL → `in_progress` (never terminal) | PASS |
| Forbidden import guard | PASS |
| `external_effects == 0` on all card fixtures | PASS |
| `CARD_INPUT_SCHEMA_VALIDATION` | PASS |
| `CARD_OUT_OF_SCOPE_MUTATION_PACKET_FAILS_CLOSED` | PASS |
| `CARD_POLICY_REASON_CODES_PASSTHROUGH` | PASS |
| `CARD_UI_ERRORS_SEPARATE_FROM_POLICY` | PASS |
| `CARD_RAW_CRM_IDS_NOT_RENDERED` | PASS |
| `CARD_HTML_ESCAPING` | PASS |
| `CARD_DETERMINISTIC_REPEATABILITY` | PASS |
| `CARD_FORBIDDEN_IMPORT_GUARD` | PASS |

---

## 11. Implementation sequence (when coding is later authorized)

1. Land this packet on `feat/nw006-meeting-follow-up-card` for review.
2. After review: create pure `CardViewModel` + mapper (no render yet) + packet fixtures.
3. Add terminal + non-terminal mapper tests until green.
4. Add text + HTML renderers + render tests (chrome only).
5. Add forbidden-import and EXTERNAL_EFFECTS guards.
6. Optional CLI demo entrypoint.
7. Write `proof/nw006/proof-return.yaml` + closeout; reconcile ledger/README.
8. **STOP** — do not continue into NW-005 / NW-007 / mutation execution.

Exact-path staging only; no `git add .`.

---

## 12. Explicit non-goals (this unit)

- Live GHL reads or writes
- Mutation approve-and-execute controls
- Firestore audit writer (NW-005)
- Cloud Run / hosting deployment (NW-007)
- Private production MG Guide route wiring / auth gateway changes
- IAM, secrets, env provisioning
- Re-running Units 1–3 agents from the card
- Replacing deterministic policy with LLM judgment on the card
- Broad design-system / multi-page app build-out beyond the single card surface

### HTML safety requirement (mandatory tests)

Render HTML must escape packet/user content before insertion. Add mandatory
escaping tests using synthetic content containing:

- `<script>`
- `<img onerror>`
- ampersands
- angle brackets
- quotes

No scripts or executable markup from packet content may appear in output.

---

## 13. Entry / exit criteria

### Entry (coding may start only when all true)

1. PR #14 is **MERGED** on GitHub. **SATISFIED** (`87d962e05e118e364eb452ce3f367cdb2de08399`).
2. This implementation packet exists and is reviewed.
3. Working branch is **not** `main` and is **not** the Unit 3 branch.
4. Fresh branch from merged main: `feat/nw006-meeting-follow-up-card`. **SATISFIED** for this envelope step.
5. No CRM/Firestore/deployment work is mixed into the same unit.

### Exit (implementation complete)

1. All §10 proof markers true.
2. All §10 scenarios PASS under the test commands in §9.
3. `EXTERNAL_EFFECTS=0`.
4. Public CI green on the NW-006 PR head.
5. Stop before mutation execution, Firestore writer, or deployment.

---

## 14. Baseline binding (machine-checkable)

```text
PR14_STATE=MERGED
PR14_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/14
PR14_MERGE_SHA=87d962e05e118e364eb452ce3f367cdb2de08399
ORIGIN_MAIN_SHA=87d962e05e118e364eb452ce3f367cdb2de08399
BRANCH=feat/nw006-meeting-follow-up-card
IMPLEMENTATION_STARTED=NO
PACKET_STATUS=BOUNDED_IMPLEMENTATION_PACKET_READY
UI_SURFACE=src/mg_guide/meeting_follow_up_card/**
MAPPER=src/mg_guide/meeting_follow_up_card/mapper.py
VIEWMODEL=src/mg_guide/meeting_follow_up_card/models.py
RENDER_TEXT=src/mg_guide/meeting_follow_up_card/render_text.py
RENDER_HTML=src/mg_guide/meeting_follow_up_card/render_html.py
FIXTURES=fixtures/nw006/**
TESTS=tests/mg_guide/meeting_follow_up_card/**
EXTERNAL_EFFECTS=0
CARD_INPUT_SCHEMA_VALIDATION=PASS
CARD_OUT_OF_SCOPE_MUTATION_PACKET_FAILS_CLOSED=PASS
CARD_POLICY_REASON_CODES_PASSTHROUGH=PASS
CARD_UI_ERRORS_SEPARATE_FROM_POLICY=PASS
CARD_RAW_CRM_IDS_NOT_RENDERED=PASS
CARD_HTML_ESCAPING=PASS
CARD_DETERMINISTIC_REPEATABILITY=PASS
CARD_FORBIDDEN_IMPORT_GUARD=PASS
```

---

## 15. STOP

This step defines the bounded implementation surface only.
**No Meeting Follow-Up card code is implemented by this packet.**

```text
STOP_CODE=NW006_IMPLEMENTATION_PACKET_READY_FOR_REVIEW
```
