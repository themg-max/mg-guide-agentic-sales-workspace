# MG Guide Workspace Add-on — Follow-Up Draft Readiness v1 (UX v2)

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-follow-up-draft-readiness-v1.md
UNIT=MG_GUIDE_WORKSPACE_ADDON_UX_V2_FOLLOW_UP_DRAFT_001
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
BASE_SHA=46d2cef258f22d2de3b9a3dc874be5f20525ed5e
BRANCH=impl/mg-guide-workspace-addon-follow-up-draft-ux-v2-001
COMPETITION=Google All Things Agentic Hackathon
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
REAL_CUSTOMER_DATA=NO
```

## 1. Result markers

```text
ADDON_UX_V2=PASS
FOLLOW_UP_DRAFT_PROJECTION=PASS
GMAIL_COMPOSE_ACTION_IMPLEMENTED=YES

EMAIL_AUTO_SEND=NO
EMAIL_AUTO_SEND_API_PRESENT=NO
DRAFT_CREATION_REQUIRES_USER_ACTION=YES
FINAL_SEND_REQUIRES_HUMAN=YES

WORKSPACE_LIVE_TRANSCRIPT_READ=NO
CURRENT_TRANSCRIPT_SOURCE=synthetic_fixture
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=FUTURE_NOT_IMPLEMENTED

LIVE_REST_V3_NOTE_CREATE=PENDING
LIVE_REST_V3_NOTE_READBACK=PENDING
R5_RESOLVED=NO
R5_CAN_CLOSE_WITH_CURRENT_SURFACE=NO

REAL_CRM_MUTATIONS=0
REAL_EMAILS_SENT=0
REAL_NETWORK_CALLS_IN_TESTS=0
REAL_PROVIDER_CALLS=0
REAL_SECRET_READS=0
```

## 2. What changed

| Path | Change |
| --- | --- |
| `workspace_addon/Cards.gs` | UX v2: product-first home (`Process Meeting Follow-Up` primary CTA; judge test scenarios secondary); result-first SUCCESS card (Follow-up ready → Processing status → What we heard → Relationship → CRM → Follow-up draft → Send follow-up → Audit and integrity); NEEDS_REVIEW card with no compose action; CRM display wording from backend `crm_note_status` only. |
| `workspace_addon/DraftFollowUp.gs` | New. `createFollowUpDraft(e)` compose callback: validates scenario + COMPLETED + READY, re-fetches the deterministic server projection for the same approved synthetic scenario, validates recipient/subject/body, calls `GmailApp.createDraft`, returns `ComposeActionResponse`. No send APIs. |
| `workspace_addon/appsscript.json` | Added least-privilege scope `https://www.googleapis.com/auth/gmail.addons.current.action.compose`. No send/modify/full-mail/Drive/Admin scopes. |
| `src/mg_guide/judge_surface/demo_stages.py` | `project_ux_experience` now emits `follow_up_draft` (deterministic, approved fields only) and `crm_note_status` (narrow NOT_EXECUTED/BLOCKED/VERIFIED/UNKNOWN contract; VERIFIED requires explicit durable verified-effect evidence + live execution performed). |
| `src/mg_guide/workspace_addon/cardservice_projection.py` | v2 card models mirroring the Apps Script hierarchy; compose action widget model; presentation-layer fail-closed guard so VERIFIED wording cannot render while `LIVE_CRM_EXECUTION!=PERFORMED`. |
| `tests/judge_surface/test_demo_stages.py` | T-DRAFT-01/02/03/04/15/16/17/18 backend tests. |
| `tests/workspace_addon/test_cardservice_projection.py` | Home v2 + result-first ordering tests; T-DRAFT-05/06 compose-action presence; card-level draft model, raw-ID, and VERIFIED-wording tests incl. forged-claim fail-closed case. |
| `tests/workspace_addon/test_security_no_token_logging.py` | T-DRAFT-07..11 manifest scope contract; T-DRAFT-12 no auto-send APIs; T-DRAFT-13 no CRM implementation in Apps Script; T-DRAFT-14 no token logging anywhere in the add-on; updated v2 hierarchy markers. |
| `docs/architecture/mg-guide-workspace-addon-judge-ux-v2.md` | New architecture doc for the v2 UX, draft projection, compose contract, CRM status contract, and boundaries. |

## 3. What did not change

```text
WORKFLOW_RUNNER=UNCHANGED
POLICY_SEMANTICS=UNCHANGED
FIXTURES=UNCHANGED
PACKET_SCHEMA=UNCHANGED
JUDGE_ENDPOINT_CONTRACT=ADDITIVE_ONLY (new ux_experience keys)
AUTH_CONTRACT=MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1 (unchanged)
HIGHLEVEL_REST_MODULES=UNTOUCHED
LIVE_NOTE_EXECUTION=UNTOUCHED (remains blocked pending R5 + execution authority)
NOTE_PATH_HARNESS=UNTOUCHED (no Lane A/B files copied)
TERRAFORM/DEPLOYMENT/IAM/SECRET_MANAGER=UNTOUCHED
GMAIL_BODY_READS=NO
CALENDAR_EVENT_CONTENT_READS=NO
DRIVE_SCOPE=NO
```

`workspace_addon/README.md` and `…-judge-ux-v1.md` were intentionally not in
the allowed write paths; README button-label wording now differs from the v2
home card and should be refreshed in a follow-up documentation unit.

## 4. Screen / user journey

1. Judge opens MG Guide in Gmail (or Calendar) → **Meeting Follow-Up** home:
   product message, small competition truth marker, primary CTA
   **Process Meeting Follow-Up**; secondary **Judge test scenarios**
   (Ambiguous contact, Policy guardrail).
2. SUCCESS → **FOLLOW-UP READY** grid (Transcript/Meeting/Relationship/CRM
   note/Follow-up draft) → processing status → what we heard → relationship
   (matched, no provider IDs) → CRM note *not executed in competition mode* →
   follow-up draft preview (recipient, subject, body preview) →
   **Open Draft in Gmail** → audit/integrity.
3. Compose callback re-fetches the deterministic projection, validates
   readiness, creates a Gmail **draft**; Gmail shows the standard editable
   compose window. The human reviews and decides whether to send.
4. AMBIGUOUS_CONTACT → **NEEDS REVIEW**: Relationship `Ambiguous`, CRM `CRM
   update blocked. No change performed.`, Draft `Not created`, human-readable
   `Why:` + resolve-identity next action. No compose button.

## 5. Compose scope

```text
ADDED_SCOPE=https://www.googleapis.com/auth/gmail.addons.current.action.compose
GMAIL_SEND_SCOPE=ABSENT
GMAIL_MODIFY_SCOPE=ABSENT
MAIL_GOOGLE_COM_SCOPE=ABSENT
DRIVE_SCOPES=ABSENT
ADMIN_SCOPES=ABSENT
```

## 6. No-send proof

- `workspace_addon/*.gs` scanned: no `GmailApp.sendEmail`, `MailApp.sendEmail`,
  `.reply(`, `.replyAll(`, `.send(` (T-DRAFT-12).
- Compose callback returns `ComposeActionResponse` with a draft only; there is
  no code path from the add-on to sending (T-DRAFT-12, marker test).
- Manifest carries no send-capable scope (T-DRAFT-08/09/10).
- Draft content is the server projection only; Apps Script invents nothing
  (T-DRAFT-01/16; callback re-fetch design).

## 7. Synthetic transcript truth

```text
source.type=synthetic_fixture
source.provider=synthetic
source.acquisition_mode=fixture
contains_real_customer_data=false
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1 (preserved)
```

`google_workspace_meet_transcript` / `authorized_drive_read` remain
FUTURE / NOT IMPLEMENTED. No Drive scope, Drive OAuth, transcript discovery,
real transcript reads, folder discovery, or Meet API integration were added.

## 8. CRM truth

```text
CRM_NOTE_STATUS=NOT_EXECUTED (competition COMPLETED path)
CRM_NOTE_STATUS=BLOCKED (NEEDS_REVIEW paths)
LIVE_CRM_EXECUTION=NOT_PERFORMED
VERIFIED_REACHABLE_IN_COMPETITION_MODE=NO
POLICY_ALLOW_IS_NOT_EXECUTION_PROOF=ENFORCED
```

`VERIFIED` requires a future backend response with explicit durable
verified-effect evidence (`crm_effect.verified=true`,
`evidence=provider_readback`) AND `LIVE_CRM_EXECUTION=PERFORMED`. The card
layer independently fails closed to `UNKNOWN` if a VERIFIED claim arrives
without live execution (T-DRAFT-17/17b).

## 9. R5 state

```text
R5_RESOLVED=NO
R5_CAN_CLOSE_WITH_CURRENT_SURFACE=NO
LIVE_NOTE_PATH_EXECUTION=PENDING
ADDON_IS_PRIVATE_ORIGIN_OWNER=NO (never)
```

This unit is interface-ready for a future verified NOTE_PATH result (via the
`crm_note_status` contract) without depending on unmerged harness
implementation.

## 10. Tests

```text
FOCUSED_TESTS=83_PASS (tests/workspace_addon, tests/judge_surface)
FULL_TESTS=866_PASS
DETERMINISTIC_VALIDATION=PASS (scripts/verify_phase1_deterministic.py)
GIT_DIFF_CHECK=PASS
SECRET_SCAN=PASS
APPS_SCRIPT_SYNTAX=PASS (node --check on all five .gs sources)
MANIFEST_JSON=PASS
```

T-DRAFT coverage map:

| Test | Location | Result |
| --- | --- | --- |
| T-DRAFT-01 SUCCESS projects safe draft | tests/judge_surface/test_demo_stages.py | PASS |
| T-DRAFT-02 recipient only from participant context | same | PASS |
| T-DRAFT-03 missing recipient ⇒ NOT_AVAILABLE | same | PASS |
| T-DRAFT-04 AMBIGUOUS_CONTACT ⇒ NOT_AVAILABLE | same | PASS |
| T-DRAFT-05 needs-review has no compose action | tests/workspace_addon/test_cardservice_projection.py | PASS |
| T-DRAFT-06 SUCCESS has exactly one compose action | same | PASS |
| T-DRAFT-07 manifest has compose scope | tests/workspace_addon/test_security_no_token_logging.py | PASS |
| T-DRAFT-08 no gmail.send | same | PASS |
| T-DRAFT-09 no gmail.modify | same | PASS |
| T-DRAFT-10 no mail.google.com | same | PASS |
| T-DRAFT-11 no Drive scopes | same | PASS |
| T-DRAFT-12 no email auto-send API in Apps Script | same | PASS |
| T-DRAFT-13 no CRM implementation in Apps Script | same | PASS |
| T-DRAFT-14 no token values logged | same | PASS |
| T-DRAFT-15 no raw CRM IDs in draft/card | both test files | PASS |
| T-DRAFT-16 deterministic body from approved fields | tests/judge_surface/test_demo_stages.py | PASS |
| T-DRAFT-17 VERIFIED wording impossible when NOT_PERFORMED | both test files (+17b forged claim) | PASS |
| T-DRAFT-18 existing backend behavior unchanged | tests/judge_surface/test_demo_stages.py | PASS |

## 11. Changed paths (authorized only)

```text
workspace_addon/Cards.gs
workspace_addon/DraftFollowUp.gs (new)
workspace_addon/appsscript.json
src/mg_guide/judge_surface/demo_stages.py
src/mg_guide/workspace_addon/cardservice_projection.py
tests/judge_surface/test_demo_stages.py
tests/workspace_addon/test_cardservice_projection.py
tests/workspace_addon/test_security_no_token_logging.py
docs/architecture/mg-guide-workspace-addon-judge-ux-v2.md (new)
proof/competition/mg-guide-workspace-addon-follow-up-draft-readiness-v1.md (new)
```

`tests/workspace_addon/test_auth_contract.py` and
`workspace_addon/MeetingFollowUp.gs` were authorized but required no change;
the compose callback reuses the existing authenticated fetch path.

## 12. Security scan (changed paths)

```text
Bearer/access_token/refresh_token/client_secret/private_key=0_HITS
GHL_TOKEN_OR_PROVIDER_IDS=0_HITS
RAW_CONTACT_IDS_IN_RUNTIME_PATHS=0_HITS (only synthetic fixture IDs inside negative test assertions)
RAW_LOCATION_IDS=0_HITS
GMAIL_SEND_APIS=0_HITS
DRIVE_SCOPES=0_HITS
ADMIN_SCOPES=0_HITS
```

## 13. Deployment boundary

```text
TEST_DEPLOYMENT_MUTATION=NO
MARKETPLACE_MUTATION=NO
CLASP_PUSH_IN_THIS_UNIT=NO
TEST_DEPLOYMENT_REAUTH_REQUIRED=YES
```

The new compose scope changes the OAuth authorization surface, so the existing
test installation must re-authorize before the compose action works.

## 14. E2E status

```text
SAFE_COMPETITION_E2E=PASS
  synthetic transcript -> workflow -> three-agent context/follow-up path
  -> deterministic policy -> CRM note NOT_EXECUTED truth -> Gmail draft READY
TRUE_LIVE_E2E=BLOCKED
  requires GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=PROVEN
  + R5_SAME_PROCESS_PRIVATE_ORIGIN=PROVEN
  + LIVE_NOTE_PATH_EXECUTION_AUTHORIZED=YES
  + LIVE_NOTE_CREATE_READBACK=PASS
```
