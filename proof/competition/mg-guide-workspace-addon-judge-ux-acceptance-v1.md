# MG Guide Workspace Add-on — Judge UX Acceptance v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-judge-ux-acceptance-v1.md
COMPETITION=Google All Things Agentic Hackathon
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
BRANCH=competition/meeting-follow-up-v1-acceptance-finalization-001
CREATED_AT_UTC=2026-08-19T12:50:00Z
MODE=workspace_addon_judge_ux_completion
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## 1. Scope delivered

Thin presentation + routing adapter only:

| Path | Role |
| --- | --- |
| `workspace_addon/*.gs` + `appsscript.json` | CardService UI: MG Guide branding, SUCCESS / AMBIGUOUS_CONTACT buttons, six-stage render, error cards |
| `src/mg_guide/workspace_addon/` | Pure CardService projection, OIDC auth validator, local in-process adapter, token-logging guards |
| `src/mg_guide/judge_surface/app.py` | Optional `JUDGE_ADDON_AUTH_MODE` gate (default **off**) |
| `docs/architecture/mg-guide-workspace-addon-auth-contract-v1.md` | Explicit auth contract |
| `docs/architecture/mg-guide-workspace-addon-judge-ux-v1.md` | UI architecture |
| `tests/workspace_addon/` | Projection, auth, security tests |

```text
APPS_SCRIPT_RENDERS_AND_ROUTES_ONLY=YES
POLICY_ENGINE_CHANGED=NO
FIXTURE_BYTES_CHANGED=NO
RUNNER_CHANGED=NO
PRODUCTION_IAM_CHANGED=NO
IAP_CHANGED=NO
CLASP_PUSH=NO
MARKETPLACE_MUTATION=NO
```

## 2. UI architecture implemented

```text
CardService (MG Guide home)
  -> runMeetingFollowUpScenario(scenario)
  -> POST {JUDGE_BACKEND_BASE_URL}/demo/meeting-follow-up
  -> existing JudgeSurfaceApp / WorkflowRunner / packet / demo_stages / ux_experience
  -> buildResultCardFromJudgePayload (display only)
```

Primary scenarios: `SUCCESS`, `AMBIGUOUS_CONTACT`  
Optional: `STAGE_CHANGE_DENIED`

Six stages displayed from backend `demo_stages` (no narrative aliases).

## 3. Auth contract status

```text
AUTH_CONTRACT_ID=MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1
AUTH_CONTRACT_DEFINED=YES
TOKEN_SOURCE=ScriptApp.getIdentityToken()
BACKEND_VALIDATOR_IMPLEMENTED=YES
DEFAULT_JUDGE_AUTH_MODE=off
PRODUCTION_CONFIG_CHANGED=NO
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
```

Distinct from IAP, Cloud Run IAM invoker tokens, API keys, and MCP auth.

**Blocker for live Workspace → Cloud Run without further grant:**

Deployed Cloud Run judge surface remains IAP-oriented for browser access.
Binding the Apps Script OIDC audience, setting `JUDGE_BACKEND_BASE_URL` +
urlFetch whitelist in a private Script project, enabling
`JUDGE_ADDON_AUTH_MODE=identity_token` on a judge revision, and clasp push /
Marketplace deploy are **out of this unit** and not performed.

## 4. Local / deterministic acceptance (executed)

```bash
export MEETING_CONTEXT_GEMINI_MODE=stub PYTHONPATH=src
.venv/bin/python -m pytest -q tests/workspace_addon tests/judge_surface tests/mg_guide/meeting_follow_up_card
.venv/bin/python scripts/verify_phase1_deterministic.py
git diff --check
```

```text
PYTEST_WORKSPACE_ADDON_JUDGE_CARD=PASS
VERIFY_PHASE1_DETERMINISTIC=PASS
GIT_DIFF_CHECK=PASS
```

### SUCCESS (local adapter over live runner fixtures)

```text
SUCCESS_SCENARIO=PASS
SUCCESS_UX_STATE=COMPLETED
SUCCESS_WORKFLOW_STATUS=completed
SUCCESS_NOTE_WRITE=allowed
SUCCESS_STAGE_WRITE=allowed
SUCCESS_EXTERNAL_EFFECTS=0
SUCCESS_LIVE_CRM_EXECUTION=NOT_PERFORMED
POLICY_RESULT_VISIBLE=YES
SALESPERSON_NEXT_STEP_VISIBLE=YES
AUDIT_STATUS_VISIBLE=YES
```

### AMBIGUOUS_CONTACT (local adapter)

```text
AMBIGUOUS_CONTACT_SCENARIO=PASS
AMBIGUOUS_UX_STATE=NEEDS_REVIEW
AMBIGUOUS_WORKFLOW_STATUS=blocked
AMBIGUOUS_NOTE_WRITE=not_attempted
AMBIGUOUS_STAGE_WRITE=not_attempted
AMBIGUOUS_REASON=AMBIGUOUS_CONTACT
AMBIGUOUS_CANDIDATE_COUNT=2
AMBIGUOUS_EXTERNAL_EFFECTS=0
AMBIGUOUS_MESSAGE_CONCEPT=No CRM changes were made. Resolve contact identity before any CRM write.
```

### Security

```text
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
EXTERNAL_EFFECTS=0
CRM_MUTATIONS_PERFORMED=NO
REAL_CUSTOMER_DATA=NO
```

## 5. Controlled judge-account live Workspace test

```text
JUDGE_ACCOUNT_TYPE=CONTROLLED_INTERNAL_WORKSPACE
JUDGE_ACCOUNT_EMAIL_REDACTED=YES
JUDGE_ACCOUNT_TESTED=NO
ADDON_OPEN_FROM_GMAIL=NOT_TESTED
ADDON_OPEN_FROM_CALENDAR=NOT_TESTED
REPEAT_OPEN_TEST=NOT_TESTED
REPEAT_SCENARIO_TEST=PASS
```

`REPEAT_SCENARIO_TEST=PASS` refers to repeated local adapter runs of both
scenarios in-process (deterministic). Live close/reopen inside Gmail/Calendar
was **not** executed in this unit (no clasp push / no judge Workspace session
in this agent environment).

## 6. Required final markers

```text
WORKSPACE_ADDON_JUDGE_UX_IMPLEMENTED=YES
MG_GUIDE_BRANDING_VISIBLE=YES
POWERED_BY_AI_ROLODEX_VISIBLE=YES

JUDGE_ACCOUNT_TYPE=CONTROLLED_INTERNAL_WORKSPACE
JUDGE_ACCOUNT_TESTED=NO

ADDON_OPEN_FROM_GMAIL=NOT_TESTED
ADDON_OPEN_FROM_CALENDAR=NOT_TESTED

SUCCESS_SCENARIO=PASS
SUCCESS_UX_STATE=COMPLETED
SUCCESS_EXTERNAL_EFFECTS=0

AMBIGUOUS_CONTACT_SCENARIO=PASS
AMBIGUOUS_UX_STATE=NEEDS_REVIEW
AMBIGUOUS_NOTE_WRITE=not_attempted
AMBIGUOUS_STAGE_WRITE=not_attempted
AMBIGUOUS_EXTERNAL_EFFECTS=0

POLICY_RESULT_VISIBLE=YES
SALESPERSON_NEXT_STEP_VISIBLE=YES
AUDIT_STATUS_VISIBLE=YES

LIVE_CRM_EXECUTION=NOT_PERFORMED
CRM_MUTATIONS_PERFORMED=NO
REAL_CUSTOMER_DATA=NO

RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0

REPEAT_OPEN_TEST=NOT_TESTED
REPEAT_SCENARIO_TEST=PASS

JUDGE_UX_ACCEPTANCE=FAIL
```

`JUDGE_UX_ACCEPTANCE=FAIL` because the mandatory controlled Workspace account
host open (Gmail/Calendar) was not executed. Local synthetic UX contract is
green.

## 7. Remaining blockers

1. **Private Script project configure + clasp push / deploy** of `workspace_addon/` (not authorized in this unit).
2. **Set `JUDGE_BACKEND_BASE_URL`** and Apps Script `urlFetchWhitelist` in the private deploy project only.
3. **Audience binding**: configure `JUDGE_ADDON_OIDC_AUDIENCE` and enable `JUDGE_ADDON_AUTH_MODE=identity_token` on a non-production judge revision when ready (no production IAM/IAP change performed here).
4. **Controlled judge Workspace account rehearsal** steps 1–16 from the unit brief (Gmail + Calendar open, both scenarios, repeat open).

## 8. Recommendation

```text
RECOMMENDATION=NOT_READY
READY_FOR=LOCAL_JUDGE_UX_REHEARSAL_AND_CODE_REVIEW
NOT_READY_FOR=LIVE_WORKSPACE_JUDGE_ISSUANCE
```

Next governed step: private deploy project push of the competition adapter +
controlled internal Workspace account dry-run, then re-run this acceptance
artifact with `JUDGE_ACCOUNT_TESTED=YES` and host open markers `PASS`.
