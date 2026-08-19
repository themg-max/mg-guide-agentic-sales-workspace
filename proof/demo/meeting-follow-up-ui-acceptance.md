# Meeting Follow-Up UI Acceptance — COMPLETED / NEEDS_REVIEW

```text
UNIT=meeting_follow_up_ui_completion_v1
WORKFLOW=meeting_follow_up_v1
BRANCH=competition/meeting-follow-up-v1-acceptance-finalization-001
BASE_SHA=1ccc447e1f6d4b47311fb2333470f8cdf8abee3c
CREATED_AT_UTC=2026-08-19T01:13:00Z
```

## Acceptance markers

```text
MEETING_FOLLOW_UP_UI=PASS
SUCCESS_STATE_UI=PASS
NEEDS_REVIEW_STATE_UI=PASS
POLICY_RESULT_VISIBLE=PASS
SALESPERSON_NEXT_STEP_VISIBLE=PASS
AUDIT_STATUS_VISIBLE=PASS
EXISTING_WORKFLOW_TESTS=PASS
```

## What was delivered

Additive judge-surface projection only (no mapper/policy/fixture changes):

| Path | Role |
| --- | --- |
| `src/mg_guide/judge_surface/demo_stages.py` | Pure packet+card → six stages + `ux_experience` |
| `src/mg_guide/judge_surface/render_demo_stages.py` | `stages_html` / `stages_text` renderers |
| `src/mg_guide/judge_surface/app.py` | Attach `demo_stages`, `demo_truth`, `ux_experience`; honor new views |
| `tests/judge_surface/test_demo_stages.py` | Stage + UX field contracts |
| `tests/judge_surface/test_app.py` | HTTP envelope assertions |
| `proof/demo/*` | Packet, proof-return, excerpts |

### COMPLETED (SUCCESS)

- Meeting/contact context (Taylor Morgan, synthetic email)
- Concise meeting summary
- Relationship context (matched / email / candidate_count=1)
- Proposed follow-up intents only (`LIVE_CRM_EXECUTION=NOT_PERFORMED`)
- Policy decision (note/stage allowed)
- Permitted action/result (external_effects=0)
- Audit status display
- Salesperson next step

### NEEDS_REVIEW (AMBIGUOUS_CONTACT)

- Human-readable reason (multiple candidates)
- Zero unauthorized effects clearly communicated
- Block context (candidate_count=2, reason_codes, not_attempted writes, blocked)
- Explicit next action for salesperson

## Truth boundary

```text
LIVE_CRM_EXECUTION=NOT_PERFORMED
EXTERNAL_EFFECTS=0
PRIVATE_MODEL_REASONING_DISPLAYED=NO
FIXTURE_BYTES_CHANGED=NO
POLICY_ENGINE_CHANGED=NO
```

## Verification

```bash
export MEETING_CONTEXT_GEMINI_MODE=stub PYTHONPATH=src
.venv/bin/python -m pytest -q tests/judge_surface tests/mg_guide/meeting_follow_up_card
.venv/bin/python scripts/verify_phase1_deterministic.py
```

Both commands: **PASS**.

## Cloud-integrated follow-on

Local stub path success + fail-closed scenarios are proven through the same
judge-surface route intended for Cloud Run. Live Cloud Run redeploy, live
Gemini calls, and Firestore writes were **not** performed in this unit and
remain separately governed.

See `proof/demo/meeting-follow-up-ui-completion-proof-return.yaml`.
