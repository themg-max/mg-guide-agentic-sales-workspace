# Meeting Follow-Up Synthetic Demo v1

## 0. Identity

```text
ARTIFACT=docs/demo/meeting-follow-up-demo-v1.md
PHASE=synthetic_demo_planning_and_fixture_alignment
OWNER=VS Code / MG Orchestrator
PRIMARY_PR_CLASS=planning_only
WORKFLOW=meeting_follow_up_v1
DEMO_UNIT=meeting_follow_up_synthetic_demo_v1
BRANCH=planning/meeting-follow-up-synthetic-demo-v1
BASE_REF=origin/main
BASE_SHA=b0f83653f065fe8390c7bceb6f88fd25de1a17d4
CREATED_AT_UTC=2026-08-18T14:45:00Z
COMPETITION_SAFE=YES
IMPLEMENTATION_AUTHORIZED=NO
BROADER_DEMO_IMPLEMENTATION_AUTHORIZED=NO
```

This unit is **planning + fixture alignment only**. It binds the competition
demo to **existing** repository contracts, fixtures, mapper/card surfaces, and
judge-surface scenario selectors. It does **not** authorize live CRM execution,
provider probes, OAuth/PIT changes, production data use, or new observation
authority.

```text
CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO
SUCCESS_FIXTURE_STRATEGY=REUSE_CANONICAL
AMBIGUOUS_FIXTURE_STRATEGY=REUSE_CANONICAL
NEW_FIXTURE_FILES_CREATED=NO
DUPLICATE_FIXTURE_CONCEPTS_CREATED=NO
```

**Presenter rule:** every spoken and on-screen value must match canonical
fixture / packet / card fields. No alternate emails, companies, confidences,
or dates may be introduced for “story polish.”

HighLevel support ticket `#6157765` is a **separate provider-authority lane**
and is out of scope for this demo unit’s runtime claims.

---

## 1. DEMO_TRUTH_BOUNDARY

```text
DEMO_TRUTH_BOUNDARY=synthetic_offline_only
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
FIRESTORE_WRITES_CLAIMED=NO
PROVIDER_ENDPOINT_PROBES=NO
OAUTH_PIT_CHANGES=NO
PRODUCTION_OR_CUSTOMER_DATA=NO
MCP_REQUESTS_MADE=NO
EXTERNAL_EFFECTS=0
PROPOSED_ACTIONS_LABELED_AS_EXECUTED=NO
PROPOSED_ACTIONS_LABELED_AS_VERIFIED=NO
PRIVATE_MODEL_REASONING_DISPLAYED=NO
NEW_OBSERVATION_AUTHORITY=NO
PROVIDER_TICKET_6157765_LANE=separate_not_demo_runtime
CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO
```

### Hard rules for presenters and UI copy

1. Show **statuses and evidence only** — never private chain-of-thought.
2. Mutation intents may be shown as **planned / proposed / allowed / blocked**.
3. Do **not** say note or stage “was written,” “was updated,” “was verified in
   CRM,” or “executed live.” This v1 unit keeps
   `LIVE_CRM_EXECUTION=NOT_PERFORMED`.
4. Success card framing already sets `no_crm_changes_made=true` and
   intent-only mutation fields (`note_execution_attempted=false`,
   `stage_execution_attempted=false`).
5. Ambiguity path must end with `FINAL_DISPOSITION=blocked`,
   `reason_codes=[AMBIGUOUS_CONTACT]`, `CANDIDATE_COUNT=2`, `CRM_WRITES=0`,
   `EXTERNAL_EFFECTS=0`.
6. **No narrative aliases.** Do not say Northstar, `example.test`, confidence
   `0.96`, review date `2026-08-20`, or any other non-fixture identity.

---

## 2. Existing surfaces discovered (reuse first)

### 2.1 Contracts

| Path | Role |
| --- | --- |
| `contracts/meeting_follow_up_packet.schema.json` | Packet contract |
| `contracts/mg_guide_meeting_follow_up_card.schema.json` | Card UI contract |
| `contracts/meeting_context.schema.json` | Extraction/context |
| `contracts/relationship_context.schema.json` | CRM resolution |
| `contracts/follow_up_proposal.schema.json` | Follow-up proposal |
| `contracts/workflow_states.yaml` | OL3 states + demo stage matrix |
| `contracts/failure_codes.yaml` | `AMBIGUOUS_CONTACT` fail-closed |
| `contracts/workflow_run_audit.schema.json` | Audit shape |

### 2.2 Canonical SUCCESS fixtures (reused — not duplicated)

| Path | Notes |
| --- | --- |
| `fixtures/transcript-success.txt` | Synthetic transcript; `MEETING_ID=demo_meeting_001` |
| `fixtures/transcript-success.expected.json` | Sidecar; judge catalog `SUCCESS` |
| `fixtures/nw006/packets/packet-success.completed.json` | Packet snapshot |
| `fixtures/nw006/expected/card-success.json` | Card snapshot |
| `fixtures/nw005/packets/packet-success.completed.json` | NW-005 packet twin |
| `fixtures/nw005/expected_audits/audit-success.completed.json` | Audit twin |

### 2.3 Canonical AMBIGUOUS_CONTACT fixtures (reused — not duplicated)

| Path | Notes |
| --- | --- |
| `fixtures/transcript-ambiguous-contact.txt` | Synthetic transcript; `MEETING_ID=demo_meeting_002` |
| `fixtures/transcript-ambiguous-contact.expected.json` | Sidecar; judge catalog `AMBIGUOUS_CONTACT` |
| `fixtures/nw006/packets/packet-ambiguous-contact.blocked.json` | Packet snapshot |
| `fixtures/nw006/expected/card-ambiguous-contact.json` | Card snapshot |
| `fixtures/nw005/packets/packet-ambiguous-contact.blocked.json` | NW-005 packet twin |
| `fixtures/nw005/expected_audits/audit-ambiguous-contact.blocked.json` | Audit twin |

### 2.4 UI / runner surfaces

| Surface | Path / selector |
| --- | --- |
| Judge scenario catalog | `src/mg_guide/judge_surface/scenarios.py` → `SUCCESS`, `AMBIGUOUS_CONTACT`, `STAGE_CHANGE_DENIED` |
| Judge demo route | `POST /demo/meeting-follow-up` in `src/mg_guide/judge_surface/app.py` |
| Card mapper | `src/mg_guide/meeting_follow_up_card/` |
| Deterministic runner | `src/orchestration/runner.py` (`run_fixture`) |

### 2.5 Fixture reuse decision

```text
SUCCESS_FIXTURE_STRATEGY=REUSE_CANONICAL
AMBIGUOUS_FIXTURE_STRATEGY=REUSE_CANONICAL
NEW_FIXTURE_FILES_CREATED=NO
DUPLICATE_FIXTURE_CONCEPTS_CREATED=NO
CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO
```

---

## 3. Canonical success fixture specification

Visible demo identity is **exactly** the canonical fixture/packet/card set.

### 3.1 Authoritative bindings

```text
CANONICAL_FIXTURE_ID=transcript-success
CANONICAL_TRANSCRIPT=fixtures/transcript-success.txt
CANONICAL_SIDECAR=fixtures/transcript-success.expected.json
CANONICAL_MEETING_ID=demo_meeting_001
CANONICAL_RUN_ID_SIDECAR=run_demo_success_001
CANONICAL_NW006_RUN_ID=run_nw006_success_001
CANONICAL_NW006_MEETING_ID=meeting_nw006_001
CANONICAL_PACKET=fixtures/nw006/packets/packet-success.completed.json
CANONICAL_CARD=fixtures/nw006/expected/card-success.json
JUDGE_SCENARIO_SELECTOR=SUCCESS
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

### 3.2 Visible values (presenter must use these)

| Field | Canonical visible value | Source |
| --- | --- | --- |
| Meeting title | `Taylor Morgan - Discovery Meeting` | NW-006 card `meeting.title` |
| Meeting id (card/packet) | `meeting_nw006_001` | packet/card |
| Meeting id (transcript/sidecar) | `demo_meeting_001` | transcript/sidecar |
| Occurred at (card/packet) | `2026-08-12T17:30:00Z` | packet/card |
| Source | `synthetic_demo` | packet/transcript |
| Contact name | `Taylor Morgan` | participants |
| Contact email | `taylor.morgan@example-demo.test` | participants |
| Contact phone | `+1-555-0100` | participants |
| Agent name | `Alex Rivera` | participants |
| Agent email | `alex.rivera@example-demo.test` | participants |
| Subject matter (sidecar summary) | Retirement income planning with liquidity constraints and a sixty-day timeline | sidecar `extraction_result.summary` |
| Card/packet summary | `Discovery call complete with agreed follow-up review package.` | card `learning.summary` / packet extraction |
| Needs (card) | `retirement planning`, `liquidity options` | card |
| Needs (sidecar) | `retirement income planning`, `liquidity flexibility` | sidecar |
| Objections | `liquidity lock-up concern` | card/sidecar |
| Commitment (sidecar) | Alex Rivera — `Prepare recommendation review` — due `2026-08-12` | sidecar commitments |
| Next step action | `Send recommendation review follow-up` | card/packet/sidecar |
| Next step owner | `Alex Rivera` | card/packet/sidecar |
| Next step target date (sidecar) | `2026-08-12` | sidecar |
| Next step target date (packet) | `2026-08-14` | packet |
| Extraction confidence | **`0.95`** | sidecar + packet evidence |
| Match basis | `email` (exact) | crm_resolution |
| Candidate count | `1` | crm_resolution |
| Contact id (synthetic) | `contact_demo_taylor_001` | crm_resolution |
| Opportunity id (synthetic) | `opp_demo_taylor_001` | crm_resolution |
| Current stage | `discovery_scheduled` | crm_resolution |
| Recommended / planned stage | `discovery_complete` | opportunity_signal / intents |
| Policy note_write | `allowed` | policy |
| Policy stage_write | `allowed` | policy |
| Reason codes | `[]` | policy |
| Mutations lifecycle | `intent_only` | packet |
| Note attempted / verified | `false` / `false` | packet/card |
| Stage attempted / verified | `false` / `false` | packet/card |
| Final disposition | `completed` | audit/run |
| Card state | `completed` | card |
| `no_crm_changes_made` | `true` | card framing |
| `external_effects` | `0` | packet/card integrity |

### 3.3 Presenter date/confidence rule

- Always say confidence **`0.95`** (never `0.96`).
- When showing the **card/packet path**, next-step target date is **`2026-08-14`**
  if reading packet `extraction.next_step.target_date`, and card does not invent
  another date.
- When showing the **sidecar/transcript path**, commitment due / sidecar next-step
  target is **`2026-08-12`**.
- Do not collapse these into a third date. Prefer the surface currently on screen.

### 3.4 Success story beats (canonical only)

1. **Prospect problem:** post-meeting follow-up is inconsistent (manual summary,
   CRM find, stage judgment, next-step notes).
2. **Prospect want:** automatic **governed** CRM follow-up — not unsupervised
   writes.
3. **Meeting subject:** discovery covering retirement income planning and
   liquidity constraints on a sixty-day timeline (canonical transcript/sidecar).
4. **Commitment:** Alex Rivera prepares / sends recommendation review follow-up
   (canonical commitment + next_step).
5. **Resolution:** exact synthetic contact match on email
   `taylor.morgan@example-demo.test`.
6. **Policy:** allows note proposal and stage intent
   `discovery_scheduled → discovery_complete`.
7. **Execution truth:** `LIVE_CRM_EXECUTION=NOT_PERFORMED`; card shows planned
   intents only; `external_effects=0`.

### 3.5 Explicitly forbidden success overlays

```text
FORBIDDEN_OVERLAY_COMPANY=Northstar Advisory Labs
FORBIDDEN_OVERLAY_EMAIL=taylor.morgan@example.test
FORBIDDEN_OVERLAY_CONFIDENCE=0.96
FORBIDDEN_OVERLAY_REVIEW_DATE=2026-08-20
FORBIDDEN_OVERLAY_ALIAS_ID=demo_meeting_success_001_as_visible_id
```

`demo_meeting_001` / `meeting_nw006_001` / `transcript-success` remain the only
success identities.

---

## 4. Ambiguous-contact fixture specification

### 4.1 Required failure demo outcomes

```text
SCENARIO=AMBIGUOUS_CONTACT
CANDIDATE_COUNT=2
FINAL_DISPOSITION=blocked
CRM_WRITES=0
EXTERNAL_EFFECTS=0
NOTE_EXECUTION_ATTEMPTED=false
STAGE_EXECUTION_ATTEMPTED=false
MUTATION_CONTROLS_ENABLED=false
```

### 4.2 Canonical repository bindings (authoritative)

```text
CANONICAL_FIXTURE_ID=transcript-ambiguous-contact
CANONICAL_TRANSCRIPT=fixtures/transcript-ambiguous-contact.txt
CANONICAL_SIDECAR=fixtures/transcript-ambiguous-contact.expected.json
CANONICAL_MEETING_ID=demo_meeting_002
CANONICAL_RUN_ID_SIDECAR=run_demo_ambiguous_001
CANONICAL_NW006_RUN_ID=run_nw006_ambiguous_contact_001
CANONICAL_NW006_MEETING_ID=meeting_nw006_003
CANONICAL_PACKET=fixtures/nw006/packets/packet-ambiguous-contact.blocked.json
CANONICAL_CARD=fixtures/nw006/expected/card-ambiguous-contact.json
JUDGE_SCENARIO_SELECTOR=AMBIGUOUS_CONTACT
FAILURE_CODE=AMBIGUOUS_CONTACT
```

| Field | Canonical visible value |
| --- | --- |
| Card meeting title | `Jordan Lee - Discovery Meeting` |
| Prospect | `Jordan Lee` (no email/phone in transcript) |
| Agent | `Alex Rivera` |
| Resolution status | `ambiguous` |
| Match basis | `name` |
| Candidate count | `2` |
| Contact id / opportunity id | `null` / `null` |
| Extraction confidence | `0.88` |
| Policy note_write | `blocked` |
| Policy stage_write | `blocked` |
| Reason codes | `["AMBIGUOUS_CONTACT"]` |
| Mutations lifecycle | `not_attempted` |
| Final disposition | `blocked` |
| Card state | `blocked` |
| `no_crm_changes_made` | `true` |
| `external_effects` | `0` |
| Allowed human action | `escalate_offline` |

### 4.3 Governance point for judges

When identity is not unique, MG Guide **refuses to act** rather than guessing.
That refusal is the product: governed sales work includes knowing when **not**
to write.

---

## 5. User-visible screen / flow contract

Six presenter-facing stages. Each stage shows **status + evidence fields only**.
No private model reasoning panels. Values must match §3 / §4 canonical tables.

| # | Stage | User-visible content | Backing evidence |
| --- | --- | --- | --- |
| 1 | **Meeting ready** | Meeting id, occurred_at, source=`synthetic_demo`, participants | transcript header / packet `meeting` + `participants` |
| 2 | **Meeting Context** | Summary, needs, objections, commitments, next_step, confidence **0.95** (success) | packet `extraction` + `evidence.extraction_confidence` |
| 3 | **Relationship Resolution** | resolution_status, match_basis, candidate_count, current_stage, synthetic ids when matched | packet `crm_resolution` / card `crm_display` |
| 4 | **Follow-Up Planning** | Planned note intent + planned stage intent (or empty on block) | packet `mutation_intents` / card `intents_display` |
| 5 | **Policy Evaluation** | note_write, stage_write, reason_codes | packet `policy` / card `policy_display` |
| 6 | **Meeting Follow-Up result card** | card_state, framing, brief, controls, `integrity.external_effects` | NW-006 card via mapper |

### 5.1 Success path field checklist (stage 6)

- `card_state=completed`
- `framing.tone=success`
- `framing.no_crm_changes_made=true`
- `meeting.title=Taylor Morgan - Discovery Meeting`
- `crm_display.resolution_status=matched`
- `crm_display.match_basis=email`
- `crm_display.candidate_count=1`
- `crm_display.current_stage=discovery_scheduled`
- `policy_display.note_write=allowed`
- `policy_display.stage_write=allowed`
- stage intent summary includes `discovery_scheduled -> discovery_complete`
- `intents_display.note_execution_attempted=false`
- `intents_display.stage_execution_attempted=false`
- `integrity.external_effects=0`
- Spoken/on-screen: **`LIVE_CRM_EXECUTION=NOT_PERFORMED`**
- Confidence if stated: **`0.95`**

### 5.2 Ambiguity path field checklist (stage 6)

- `card_state=blocked`
- `framing.tone=blocked`
- `framing.no_crm_changes_made=true`
- `meeting.title=Jordan Lee - Discovery Meeting`
- `crm_display.resolution_status=ambiguous`
- `crm_display.candidate_count=2`
- `policy_display.reason_codes=["AMBIGUOUS_CONTACT"]`
- `controls.allowed_human_actions` includes `escalate_offline`
- `integrity.external_effects=0`

### 5.3 Exact user-visible flow (operator)

```text
1. Meeting ready
   -> open SUCCESS (judge selector SUCCESS or NW-006 success card)
2. Meeting Context
   -> Taylor Morgan discovery; retirement/liquidity; confidence 0.95
3. Relationship Resolution
   -> matched; email; candidate_count=1; discovery_scheduled
4. Follow-Up Planning
   -> planned note; planned stage discovery_scheduled->discovery_complete
5. Policy Evaluation
   -> note_write=allowed; stage_write=allowed; reason_codes=[]
6. Meeting Follow-Up result card
   -> completed; intents planned; LIVE_CRM_EXECUTION=NOT_PERFORMED; external_effects=0
7. Switch to AMBIGUOUS_CONTACT
   -> Jordan Lee; candidate_count=2; blocked; CRM_WRITES=0
8. Close with preferred line
```

---

## 6. Timed demo script (~3:25)

Preferred total: **3 minutes 25 seconds**. Statuses/evidence only.
**Canonical fixture values only** — no narrative aliases.

| Time | Beat | Spoken / on-screen (canonical) |
| --- | --- | --- |
| **0:00–0:20** | Hook | “After a sales meeting, follow-up is inconsistent: summary, CRM lookup, stage call, next step. Prospects want that automatic — but governed.” |
| **0:20–0:40** | Stage 1 Meeting ready | Synthetic demo meeting ready: **Taylor Morgan - Discovery Meeting**; participants Taylor Morgan (`taylor.morgan@example-demo.test`) and Alex Rivera. State: **no production data**. |
| **0:40–1:05** | Stage 2 Meeting Context | Discovery covering **retirement income planning** and **liquidity** on a **sixty-day** timeline; objection **liquidity lock-up concern**; Alex next step **Send recommendation review follow-up**; confidence **0.95**. |
| **1:05–1:25** | Stage 3 Relationship Resolution | Exact **email** match; `candidate_count=1`; current stage **`discovery_scheduled`**; synthetic ids `contact_demo_taylor_001` / `opp_demo_taylor_001`. |
| **1:25–1:45** | Stage 4 Follow-Up Planning | Planned **note** intent from summary; planned **stage** intent **`discovery_scheduled → discovery_complete`**. Label both **proposed intents**, not executed writes. |
| **1:45–2:05** | Stage 5 Policy Evaluation | Policy **note_write=allowed**, **stage_write=allowed**, reason_codes empty. Deterministic gate sits between proposal and any future mutation authority. |
| **2:05–2:30** | Stage 6 Success card | Card **`completed`**; `no_crm_changes_made=true`; **`LIVE_CRM_EXECUTION=NOT_PERFORMED`**; **`external_effects=0`**. |
| **2:30–3:10** | Failure contrast | Switch to **`AMBIGUOUS_CONTACT`**: **Jordan Lee**, no unique identifiers, **`candidate_count=2`**, policy blocked, **zero CRM writes**, disposition **`blocked`**. |
| **3:10–3:25** | Close | **“MG Guide turns meetings into governed sales work—and knows when not to act.”** |

### 6.1 Optional one-line provider-lane aside (≤5s, not a runtime claim)

If asked about HighLevel MCP contract work: “Provider clarification is a
separate authority lane — support ticket `6157765` — not part of this
synthetic demo execution.”

---

## 7. Claims allowed vs claims forbidden

### 7.1 Allowed claims

- Synthetic/offline Meeting Follow-Up vertical slice exists with contracts,
  fixtures, deterministic policy, and card mapping.
- SUCCESS path prepares **governed intents** for note + approved stage
  transition `discovery_scheduled → discovery_complete` under demo policy.
- Visible success identity is Taylor Morgan /
  `taylor.morgan@example-demo.test` with confidence **0.95**.
- AMBIGUOUS_CONTACT path fail-closes with **no CRM writes** and
  `candidate_count=2`.
- Judge-safe surface can run fixed selectors `SUCCESS` and
  `AMBIGUOUS_CONTACT` without arbitrary customer input.
- `EXTERNAL_EFFECTS=0` for these fixture paths.
- `LIVE_CRM_EXECUTION=NOT_PERFORMED` in this demo unit.

### 7.2 Forbidden claims

- Live GHL/MCP calls were made during this demo unit.
- CRM note or stage was **executed**, **written**, or **verified** live.
- Firestore audit was newly written by this demo unit.
- Production or real customer data was used.
- Private model reasoning was shown.
- Narrative aliases: Northstar Advisory Labs, `example.test`, confidence
  `0.96`, review date `2026-08-20`, or any non-fixture company/email/date.
- Provider ticket `#6157765` proves MCP tool availability or authorizes
  observation/execution.
- Grant009, OAuth/PIT changes, endpoint probes, or new observation authority.
- “Fully autonomous CRM operator” without fail-closed stops.

---

## 8. Acceptance checklist

```text
[ ] Branch is not main; base is origin/main @ b0f83653f065fe8390c7bceb6f88fd25de1a17d4
[ ] docs/demo/meeting-follow-up-demo-v1.md present with required sections
[ ] DEMO_TRUTH_BOUNDARY present and fail-closed
[ ] CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
[ ] PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO
[ ] SUCCESS uses canonical fixtures only (no duplicate success concept)
[ ] AMBIGUOUS_CONTACT uses canonical fixtures (candidate_count=2, blocked, CRM_WRITES=0)
[ ] Presenter script uses confidence 0.95 and canonical dates/emails only
[ ] No Northstar / 0.96 / 2026-08-20 / example.test overlay claims
[ ] User-visible stages 1-6 specified
[ ] Timed script ~3:25 with preferred closing line
[ ] Claims allowed/forbidden explicit
[ ] LIVE_CRM_EXECUTION=NOT_PERFORMED stated for success path
[ ] EXTERNAL_EFFECTS=0 confirmed for both paths
[ ] No live GHL/CRM/Firestore/provider probe activity in this unit
[ ] git diff --check clean
[ ] PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py passes
[ ] Applicable fixture/card tests pass (expect 34)
[ ] STOP for review before broader demo implementation
```

---

## 9. Out of scope / stop gate

```text
BROADER_DEMO_UI_IMPLEMENTATION=NOT_AUTHORIZED_BY_THIS_ARTIFACT
FIXTURE_BYTE_RENORMALIZATION=NOT_PERFORMED
LIVE_EXECUTION=NOT_AUTHORIZED
PROVIDER_RUNTIME_VALIDATION=NOT_AUTHORIZED
NEXT_ACTOR=mg-pr-governance-reviewer
```

**STOP for mg-pr-governance-reviewer before broader demo implementation.**

---

*Planning-only synthetic demo artifact. `EXTERNAL_EFFECTS=0`.
`LIVE_CRM_EXECUTION=NOT_PERFORMED`.
`CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES`.
`PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO`.*
