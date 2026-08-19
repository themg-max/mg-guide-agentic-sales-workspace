# Meeting Follow-Up Six-Stage Synthetic Demo — Bounded Implementation Packet

| Field | Value |
| --- | --- |
| Artifact | `proof/demo/meeting-follow-up-six-stage-implementation-packet.md` |
| Packet status | **BOUNDED_IMPLEMENTATION_PACKET_READY** |
| Phase | `implementation_planning_then_bounded_implementation` |
| Owner | VS Code / MG Orchestrator |
| Authoritative demo plan | [`docs/demo/meeting-follow-up-demo-v1.md`](../../docs/demo/meeting-follow-up-demo-v1.md) (PR #87) |
| Prerequisites | PR #86 merged; PR #87 merged |
| Implementation started | **NO** |
| Coding authorized by this packet alone | **NO** — architecture/governance review first |
| Broader demo UI / deployment | **NOT authorized** by this packet |

---

## 0. Identity and baseline

```text
DEMO_UNIT=meeting_follow_up_six_stage_surface_v1
WORKFLOW=meeting_follow_up_v1
BRANCH=demo/meeting-follow-up-six-stage-surface-v1
BASE_REF=origin/main
BASE_SHA=4d4f79f8d64d0981b8cb1adf300f25c132f219eb
BASE_TITLE=Merge pull request #87 from themg-max/planning/meeting-follow-up-synthetic-demo-v1
CREATED_AT_UTC=2026-08-18T14:50:00Z
COMPETITION_SAFE=YES
MATERIAL_NEW_ARCHITECTURE_SURFACE=NO
EXISTING_SURFACES_SUFFICIENT=YES
```

### Git preflight (recorded)

```text
pwd=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
branch_at_packet_authoring=demo/meeting-follow-up-six-stage-surface-v1
not_main=YES
origin_main=4d4f79f8d64d0981b8cb1adf300f25c132f219eb
working_tree_at_checkout=clean
```

Do **not** implement from `main`. Do **not** reuse
`planning/meeting-follow-up-synthetic-demo-v1` as the implementation branch tip
(it is the PR #87 planning branch; `origin/main` already contains the merge).

---

## 1. DEMO_TRUTH_BOUNDARY (inherited, non-negotiable)

```text
CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
MCP_REQUESTS_MADE=NO
EXTERNAL_EFFECTS=0
PRODUCTION_OR_CUSTOMER_DATA=NO
PRIVATE_MODEL_REASONING_DISPLAYED=NO
FIRESTORE_WRITES_CLAIMED=NO
OAUTH_PIT_CHANGES=NO
PROVIDER_ENDPOINT_PROBES=NO
NEW_OBSERVATION_AUTHORITY=NO
FIXTURE_BYTE_RENORMALIZATION=NO
DUPLICATE_SUCCESS_OR_AMBIGUOUS_FIXTURES=NO
```

Forbidden narrative overlays (never introduce):

```text
Northstar Advisory Labs
taylor.morgan@example.test
confidence=0.96
review_date=2026-08-20
```

---

## 2. Sufficiency decision (inspect-only result)

### 2.1 Surfaces inspected

| Surface | Path | Verdict |
| --- | --- | --- |
| Demo plan | `docs/demo/meeting-follow-up-demo-v1.md` | Authoritative six-stage contract |
| Scenario catalog | `src/mg_guide/judge_surface/scenarios.py` | `SUCCESS`, `AMBIGUOUS_CONTACT`, `STAGE_CHANGE_DENIED` already registered |
| Judge HTTP adapter | `src/mg_guide/judge_surface/app.py` | `POST /demo/meeting-follow-up` runs fixture → packet → card |
| Card mapper/models/render | `src/mg_guide/meeting_follow_up_card/**` | Stage-6 card already deterministic |
| Canonical sidecars | `fixtures/transcript-success.expected.json`, `fixtures/transcript-ambiguous-contact.expected.json` | Reuse; do not duplicate |
| NW-006 twins | `fixtures/nw006/**` | Reference snapshots only; **judge path uses live runner packets** |
| Judge tests | `tests/judge_surface/**` | Cover selectors + html/text/json views |
| Card tests | `tests/mg_guide/meeting_follow_up_card/**` | Cover mapper/render integrity |

### 2.2 Live judge-path truth (runner via catalog sidecars)

Probed with `MEETING_CONTEXT_GEMINI_MODE=stub` and
`WorkflowRunner.run_fixture` / `POST /demo/meeting-follow-up`.

**SUCCESS (required claims — met by packet + card today):**

| Claim | Live value | Where today |
| --- | --- | --- |
| Contact name | Taylor Morgan | packet `participants`; card title |
| Email | `taylor.morgan@example-demo.test` | packet `participants` only |
| confidence | `0.95` | packet `evidence.extraction_confidence` only |
| match_basis | `email` | `resolution_outcome` + `card.crm_display` |
| candidate_count | `1` | same |
| current_stage | `discovery_scheduled` | same |
| planned_stage | `discovery_complete` | `card.intents_display.stage` |
| note_write | `allowed` | `policy_decision` + `card.policy_display` |
| stage_write | `allowed` | same |
| external_effects | `0` | top-level + `card.integrity` |
| cloud_mutation | `NONE` | top-level |
| card_state | `completed` | card |
| no_crm_changes_made | `true` | `card.framing` |
| synthetic ids | `contact_demo_taylor_001` / `opp_demo_taylor_001` | packet CRM + `card.metadata` |

**AMBIGUOUS_CONTACT (required claims — met by packet + card today):**

| Claim | Live value | Where today |
| --- | --- | --- |
| Prospect | Jordan Lee | card title / participants |
| resolution_status | `ambiguous` | resolution + card |
| candidate_count | `2` | same |
| reason_codes | `["AMBIGUOUS_CONTACT"]` | policy + card |
| FINAL_DISPOSITION | `blocked` | `audit_summary.final_disposition` / `workflow_status` |
| CRM_WRITES / EXTERNAL_EFFECTS | `0` | top-level + integrity |
| intents | empty note/stage; execution attempted false | card |
| allowed_human_actions | includes `escalate_offline` | card controls |

### 2.3 Presentation gaps (not architecture gaps)

The **data plane is sufficient**. Gaps are **projection/presentation only**:

1. No first-class six-stage object on the judge response (`demo_stages` absent).
2. Judge response omits fields needed for stages 1–2 as top-level evidence:
   - `meeting.source` (`synthetic_demo`)
   - `participants` (email/phone/roles)
   - `evidence.extraction_confidence` (`0.95` / `0.88`)
3. Existing `card_view` HTML is a **single flat section** (`mg-guide-card`), not a
   six-stage walkthrough; it also omits explicit
   `LIVE_CRM_EXECUTION=NOT_PERFORMED`, participants, confidence, and policy
   note/stage labels as dedicated stage panels.
4. NW-006 static ambiguous packet twin shows `policy.note_write/stage_write=blocked`,
   while **live runner** (judge path of truth) shows `not_attempted` with
   `reason_codes=["AMBIGUOUS_CONTACT"]` and terminal `blocked`.  
   **Decision:** judge demo must display **live runner values**
   (`not_attempted`), not NW-006 snapshot overlays. Do **not** change policy
   engine or renormalize fixtures to force `blocked` write flags.

### 2.4 Architecture rule check

```text
REUSE_JUDGE_ROUTE=YES
REUSE_SCENARIO_REGISTRY=YES
REUSE_CANONICAL_FIXTURES=YES
REUSE_PACKET_CARD_MAPPER=YES
REUSE_SCHEMAS=YES
NEW_HTTP_SERVICE=NO
NEW_FRONTEND_FRAMEWORK=NO
NEW_FIXTURE_CONCEPTS=NO
NEW_CRM_OR_MCP_PATH=NO
MATERIAL_NEW_ARCHITECTURE_SURFACE=NO
```

**Decision: EXISTING_SURFACES_SUFFICIENT=YES.**  
Proceed with a **thin stage projection + staged HTML view** on the existing
judge adapter. No new product architecture surface is required.

---

## 3. Bounded unit objective

Present the PR #87 six-stage Meeting Follow-Up demo on the **existing**
judge-safe surface for selectors `SUCCESS` and `AMBIGUOUS_CONTACT`, using
**canonical fixture-driven runner packets** and the **existing card mapper**.

```text
POST /demo/meeting-follow-up {scenario, view?}
  -> scenarios.SCENARIO_CATALOG[selector]          # unchanged
  -> WorkflowRunner.run_fixture(sidecar)          # unchanged
  -> map_packet_to_card(packet)                   # unchanged
  -> project_demo_stages(packet, card, ...)       # NEW pure projection
  -> optional stages HTML/text render             # NEW thin renderer
  -> JSON response (+ card_view when requested)
  -> STOP
```

User-visible stages (exact labels):

1. Meeting ready  
2. Meeting Context  
3. Relationship Resolution  
4. Follow-Up Planning  
5. Policy Evaluation  
6. Meeting Follow-Up result card  

---

## 4. Branch / baseline / path envelope

### 4.1 Branch

```text
BRANCH=demo/meeting-follow-up-six-stage-surface-v1
BASE_REF=origin/main
BASE_SHA=4d4f79f8d64d0981b8cb1adf300f25c132f219eb
```

Fresh branch from `origin/main` only. No commits on this packet alone beyond the
packet artifact itself (optional). Implementation commits land only after
governance approval of this packet.

### 4.2 Exact writable paths (implementation unit)

| Path | Change type |
| --- | --- |
| `src/mg_guide/judge_surface/demo_stages.py` | **NEW** pure projection: packet+card → ordered six-stage evidence dict (no I/O, no CRM, no runner calls) |
| `src/mg_guide/judge_surface/render_demo_stages.py` | **NEW** static HTML (and optional text) renderer for `demo_stages` only |
| `src/mg_guide/judge_surface/app.py` | **SURGICAL**: attach `demo_stages` to `_demo` response; honor `view=stages_html` (and optionally `stages_text`); keep existing `json`/`html`/`text` behavior |
| `src/mg_guide/judge_surface/__init__.py` | Export only if already exporting public symbols (minimal) |
| `tests/judge_surface/test_demo_stages.py` | **NEW** unit tests for projection field contracts |
| `tests/judge_surface/test_app.py` | **EXTEND** SUCCESS/AMBIGUOUS stage assertions + `view=stages_html` |
| `proof/demo/meeting-follow-up-six-stage-implementation-packet.md` | This packet |
| `proof/demo/meeting-follow-up-six-stage-proof-return.yaml` | **NEW** post-implementation proof return (after code) |

### 4.3 Exact blocked paths

```text
fixtures/**                         # no fixture byte changes / no duplicates
contracts/**                        # no schema churn in this unit
src/orchestration/**                # no policy/runner changes
src/agents/**                       # no agent changes
src/integrations/**                 # no GHL/MCP/OAuth/PIT
src/mg_guide/meeting_follow_up_card/**  # mapper/card schema freeze (consume only)
docs/demo/meeting-follow-up-demo-v1.md  # plan is authoritative; do not rewrite claims
Dockerfile* / deploy/** / cloudbuild/** / infra/**
.any production config / secrets / .env*
```

Hard prohibitions:

- normalize fixture bytes  
- create duplicate SUCCESS/AMBIGUOUS fixtures  
- introduce Northstar / 0.96 / 2026-08-20 aliases  
- live HighLevel calls / OAuth / PIT  
- display chain-of-thought / private model reasoning  
- production deployment expansion  
- `git add .` (stage explicit paths only)

---

## 5. Specific UI / presentation changes

### 5.1 Response shape (additive only)

Keep all existing `_demo` keys. Add:

```json
{
  "demo_stages": [
    {
      "stage_number": 1,
      "stage_id": "meeting_ready",
      "title": "Meeting ready",
      "status": "ready",
      "evidence": { "...canonical fields only..." }
    }
  ],
  "demo_truth": {
    "LIVE_CRM_EXECUTION": "NOT_PERFORMED",
    "EXTERNAL_EFFECTS": 0,
    "cloud_mutation": "NONE",
    "CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO": true,
    "PRESENTER_MAY_USE_NARRATIVE_ALIAS": false,
    "PRIVATE_MODEL_REASONING_DISPLAYED": false
  }
}
```

`demo_truth` is constant metadata for presenter/judge safety; values must not
claim execution.

### 5.2 Stage field mapping (source = live packet/card only)

| # | Title | Evidence fields (source path) |
| --- | --- | --- |
| 1 | Meeting ready | `packet.meeting.meeting_id`, `occurred_at`, `source`; `packet.participants` (name/email/phone/role); derived title from card `meeting.title` |
| 2 | Meeting Context | `packet.extraction.summary/needs/objections/next_step` (+ commitments if present); `packet.evidence.extraction_confidence` |
| 3 | Relationship Resolution | `packet.crm_resolution.status/match_basis/candidate_count/current_stage/contact_id/opportunity_id` (ids are synthetic demo ids already on packet; still no live CRM) |
| 4 | Follow-Up Planning | `card.intents_display` (note/stage summaries, execution attempted flags); empty lists on block |
| 5 | Policy Evaluation | `packet.policy.note_write/stage_write/reason_codes` (live values) |
| 6 | Meeting Follow-Up result card | existing `card` object reference fields: `card_state`, `framing`, `brief_display`, `controls`, `integrity.external_effects`, plus `demo_truth.LIVE_CRM_EXECUTION` |

No private reasoning fields. No tool traces. No prompt text.

### 5.3 SUCCESS visible contract (assert exactly)

```text
participants.prospect.name=Taylor Morgan
participants.prospect.email=taylor.morgan@example-demo.test
evidence.extraction_confidence=0.95
crm.match_basis=email
crm.candidate_count=1
crm.current_stage=discovery_scheduled
intents.stage includes discovery_scheduled -> discovery_complete
policy.note_write=allowed
policy.stage_write=allowed
card.card_state=completed
framing.no_crm_changes_made=true
integrity.external_effects=0
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

### 5.4 AMBIGUOUS_CONTACT visible contract (assert exactly)

```text
participants.prospect.name=Jordan Lee
crm.status=ambiguous
crm.candidate_count=2
policy.reason_codes=["AMBIGUOUS_CONTACT"]
workflow_status/final_disposition=blocked
intents.note=[]
intents.stage=[]
CRM write attempts false / external_effects=0
controls.allowed_human_actions includes escalate_offline
policy.note_write=not_attempted          # LIVE runner truth
policy.stage_write=not_attempted         # LIVE runner truth
```

Do **not** overwrite live `not_attempted` with NW-006 snapshot `blocked`.
Presenter copy may say “policy did not allow writes / fail-closed before
mutation” while on-screen enums remain `not_attempted` + reason code
`AMBIGUOUS_CONTACT` + disposition `blocked`.

### 5.5 HTML view

| `view` value | Behavior |
| --- | --- |
| `json` (default) | current behavior + new `demo_stages`/`demo_truth` keys; `card_view=null` |
| `html` | **unchanged** existing `render_card_html(card)` in `card_view` (compat) |
| `text` | **unchanged** existing text card render |
| `stages_html` | **new** six-section static HTML from `demo_stages` + truth banner; still JSON envelope with `card_view` string |
| `stages_text` | optional plain-text stage walkthrough |

Staged HTML requirements:

- six clearly labeled sections with the exact stage titles above  
- status + evidence fields only  
- top or bottom banner: `LIVE_CRM_EXECUTION=NOT_PERFORMED`, `EXTERNAL_EFFECTS=0`, `cloud_mutation=NONE`  
- no chain-of-thought panel  
- escape all dynamic values (`html.escape`)  
- CSS optional/minimal; no new frontend framework  

### 5.6 Non-goals for this unit

- Multi-page SPA / React / Streamlit host  
- Click-through mutation controls  
- Cloud Run redeploy proof (unless separately authorized)  
- Changing scenario catalog membership  
- Unifying NW-006 snapshot wording with live runner (document only)

---

## 6. Exact tests

### 6.1 New: `tests/judge_surface/test_demo_stages.py`

1. `test_success_demo_stages_field_contract`  
   - Build stages from live SUCCESS packet/card (via runner or app client).  
   - Assert stage titles 1–6 exact.  
   - Assert Taylor Morgan email, confidence `0.95`, match_basis `email`,
     candidate_count `1`, current_stage `discovery_scheduled`, planned stage
     `discovery_complete`, note/stage write `allowed`, external_effects `0`.

2. `test_ambiguous_demo_stages_field_contract`  
   - Jordan Lee; status `ambiguous`; candidate_count `2`;
     reason_codes `["AMBIGUOUS_CONTACT"]`; disposition/workflow `blocked`;
     intents empty; execution attempted false; external_effects `0`;
     policy write flags `not_attempted`.

3. `test_demo_stages_have_no_reasoning_payload`  
   - Serialized stages JSON must not contain forbidden keys/substrings:
     `chain_of_thought`, `reasoning`, `scratchpad`, `private_thoughts`.

4. `test_demo_stages_projection_is_pure`  
   - No filesystem writes; `external_effects` remains 0; projection does not
     import integrations/GHL/ADK.

### 6.2 Extend: `tests/judge_surface/test_app.py`

1. `test_demo_success_includes_demo_stages` — SUCCESS response has 6 stages + truth banner fields.  
2. `test_demo_ambiguous_includes_demo_stages` — AMBIGUOUS_CONTACT stage contract via HTTP.  
3. `test_demo_stages_html_view` — `view=stages_html` returns HTML containing all six titles and `LIVE_CRM_EXECUTION=NOT_PERFORMED`.  
4. Preserve existing tests for `html`/`text`/`json` compatibility and invalid scenario 400.

### 6.3 Do not require

- Changes under `tests/mg_guide/meeting_follow_up_card/**` unless a blocked-path
  regression appears (should not).  
- Browser/e2e automation.  
- Live network tests.

### 6.4 Commands (proof)

```bash
export MEETING_CONTEXT_GEMINI_MODE=stub
export PYTHONPATH=src

.venv/bin/python -m pytest -q \
  tests/judge_surface/test_demo_stages.py \
  tests/judge_surface/test_app.py

.venv/bin/python -m pytest -q tests/mg_guide/meeting_follow_up_card

.venv/bin/python scripts/verify_phase1_deterministic.py

git diff --check
```

Optional smoke:

```bash
# SUCCESS stages_html contains required tokens
# AMBIGUOUS_CONTACT stages_html contains Jordan Lee, AMBIGUOUS_CONTACT, blocked, external_effects 0
```

---

## 7. Proof requirements

After approved implementation (not this packet alone):

```text
PROOF_DIR=proof/demo/
PROOF_RETURN=proof/demo/meeting-follow-up-six-stage-proof-return.yaml
```

Proof return must record:

1. `BASE_SHA=4d4f79f8d64d0981b8cb1adf300f25c132f219eb`  
2. Implementation commit SHAs on `demo/meeting-follow-up-six-stage-surface-v1`  
3. pytest command + pass counts for judge_surface (+ card suite green)  
4. phase1 deterministic verifier pass  
5. Redacted SUCCESS JSON excerpt proving stage evidence values  
6. Redacted AMBIGUOUS JSON excerpt proving fail-closed values  
7. Explicit non-claims:

```text
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
MCP_REQUESTS_MADE=NO
EXTERNAL_EFFECTS=0
FIXTURE_BYTES_CHANGED=NO
PRIVATE_MODEL_REASONING_DISPLAYED=NO
```

---

## 8. Implementation sequence (post-approval only)

1. Confirm still on `demo/meeting-follow-up-six-stage-surface-v1` @ up-to-date `origin/main` base.  
2. Add `demo_stages.py` pure projection.  
3. Add `render_demo_stages.py` static HTML/text.  
4. Wire `app.py` additive response fields + `view=stages_html`.  
5. Add/extend tests in §6.  
6. Run proof commands in §6.4.  
7. Write proof-return YAML.  
8. Commit with explicit paths only (never `git add .`).  
9. Open PR limited to writable paths.  
10. **STOP** — no deploy, no provider work, no fixture edits.

---

## 9. Stop condition

```text
STOP_FOR=architecture_governance_review
NEXT_ACTOR=mg-pr-governance-reviewer
IMPLEMENTATION_CODING=NOT_STARTED
BROADER_DEMO_IMPLEMENTATION=NOT_AUTHORIZED
PACKET_STATUS=BOUNDED_IMPLEMENTATION_PACKET_READY
```

**Stop now.** Do not implement stage projection/HTML until this packet is
reviewed/approved. If review rejects sufficiency, return to planning — do not
silently expand scope into mapper/fixture/policy architecture.

---

## 10. Acceptance checklist (packet)

```text
[x] PR86/PR87 prerequisites acknowledged; base origin/main @ 4d4f79f8...
[x] Branch is not main
[x] Inspected judge scenarios/app, card package, demo plan, tests
[x] EXISTING_SURFACES_SUFFICIENT=YES (thin projection only)
[x] MATERIAL_NEW_ARCHITECTURE_SURFACE=NO
[x] Writable paths exact and minimal
[x] Blocked paths exact (fixtures/contracts/orchestration/integrations/card mapper freeze)
[x] Six user-visible stages named exactly
[x] SUCCESS and AMBIGUOUS_CONTACT selectors required
[x] Live ambiguous policy flags documented as not_attempted (no fixture rewrite)
[x] Truth boundary inherited
[x] Exact tests + proof commands listed
[x] STOP for review before broader implementation
```

---

*Bounded planning packet only. `EXTERNAL_EFFECTS=0`.
`LIVE_CRM_EXECUTION=NOT_PERFORMED`.
`CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES`.
`PRESENTER_MAY_USE_NARRATIVE_ALIAS=NO`.
`IMPLEMENTATION_STARTED=NO`.*
