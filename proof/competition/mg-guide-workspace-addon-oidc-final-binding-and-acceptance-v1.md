# MG Guide Workspace Add-on — OIDC Final Binding and Acceptance v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md
UNIT=MG_GUIDE_WORKSPACE_ADDON_OIDC_FINAL_BINDING_AND_ACCEPTANCE_V1
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
BRANCH=competition/meeting-follow-up-v1-acceptance-finalization-001
CREATED_AT_UTC=2026-08-19T17:12:47Z
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## 1. Audience resolution (private operator)

Controlled Workspace operator resolved the Apps Script identity-token audience
using Google's documented `getIdentityToken` payload inspection pattern.

Only `payload.aud` was retained in the private governed activation record.

```text
APPS_SCRIPT_OIDC_AUDIENCE_RESOLVED=YES
TEMP_AUDIENCE_HELPER_REMOVED=YES
TOKEN_VALUES_CAPTURED=0
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
PUBLIC_AUDIENCE_VALUE=REDACTED
```

No new long-lived Apps Script API automation credentials were introduced beyond
the existing controlled operator user OAuth used for project management.

## 2. Cloud Run dedicated add-on judge binding

The existing dedicated add-on judge service was updated. No second service was
created. The IAP browser judge service was not modified.

```text
CLOUD_RUN_ADDON_SERVICE_READY=YES
CUSTOM_AUDIENCE_BOUND=YES
APPLICATION_AUDIENCE_MATCH=YES
JUDGE_ADDON_AUTH_MODE=identity_token
JUDGE_ADDON_OIDC_AUDIENCE=REDACTED_PRIVATE
JUDGE_ADDON_ALLOWED_HD=themiliare-group.com
RUN_INVOKER_LEAST_PRIVILEGE=YES
PUBLIC_INVOKER_BINDINGS=0
EXISTING_IAP_BROWSER_SERVICE_TOUCHED=NO
LEGACY_MARKETPLACE_TOUCHED=NO
```

Trust chain:

```text
Apps Script identity token
  -> Cloud Run IAM custom-audience validation
  -> roles/run.invoker
  -> application claim validation
```

## 3. Private Apps Script binding

```text
JUDGE_BACKEND_BASE_URL_CONFIGURED=YES
URLFETCH_WHITELIST_CONFIGURED=YES
PUBLIC_ENDPOINT_COMMITTED=NO
PUBLIC_AUDIENCE_COMMITTED=NO
TEST_DEPLOYMENT_INSTALLED=YES
```

## 4. Live OIDC backend acceptance

Controlled internal Workspace identity exercised the add-on auth path against
the dedicated judge service for both primary scenarios.

```text
OIDC_BACKEND_ACCEPTANCE_TESTED=PASS

SUCCESS_HTTP=200
SUCCESS_WORKFLOW_STATUS=completed
SUCCESS_UX_STATE=COMPLETED
SUCCESS_NOTE_WRITE=allowed
SUCCESS_STAGE_WRITE=allowed
SUCCESS_EXTERNAL_EFFECTS=0

AMBIGUOUS_HTTP=200
AMBIGUOUS_WORKFLOW_STATUS=blocked
AMBIGUOUS_UX_STATE=NEEDS_REVIEW
AMBIGUOUS_NOTE_WRITE=not_attempted
AMBIGUOUS_STAGE_WRITE=not_attempted
AMBIGUOUS_REASON=AMBIGUOUS_CONTACT
AMBIGUOUS_EXTERNAL_EFFECTS=0

POLICY_RESULT_VISIBLE=YES
SALESPERSON_NEXT_STEP_VISIBLE=YES
AUDIT_STATUS_VISIBLE=YES

RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
LIVE_CRM_EXECUTION=NOT_PERFORMED
CRM_MUTATIONS_PERFORMED=NO
```

UX state mapping follows `docs` / `demo_stages` projection:

- `workflow_status=completed` + note/stage `allowed` => `SUCCESS_UX_STATE=COMPLETED`
- `workflow_status=blocked` + reason `AMBIGUOUS_CONTACT` + writes `not_attempted` => `AMBIGUOUS_UX_STATE=NEEDS_REVIEW`

## 5. Public/private boundary

```text
PUBLIC_AI_CONTROL_PLANE_PATHS=0
PRIVATE_OPERATOR_PATHS_IN_PUBLIC_PROOF=0
PUBLIC_PRIVATE_BOUNDARY=PASS
REMOVED_PUBLIC_PATH_PREFIX=.ai/proof/addon-deployed-source-authority-readonly-live-20260818/
```

Private governed originals remain outside the public competition branch.

## 6. Final markers

```text
JUDGE_UX_ACCEPTANCE=PASS
PUBLIC_PRIVATE_BOUNDARY=PASS
LEGACY_MARKETPLACE_TOUCHED=NO
IAP_BROWSER_PATH_TOUCHED=NO
RUNTIME_ADDON_SCOPES_EXPANDED=NO
SCRIPT_PROJECTS_SCOPE_IN_RUNTIME_MANIFEST=NO
```
