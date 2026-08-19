# MG Guide Workspace Add-on — Live Judge Activation v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-live-judge-activation-v1.md
UNIT=MG_GUIDE_WORKSPACE_ADDON_PROJECT_HYDRATION_AND_TEST_INSTALL_V1
COMPETITION=Google All Things Agentic Hackathon
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
BRANCH=competition/meeting-follow-up-v1-acceptance-finalization-001
MODE=workspace_addon_project_hydration_and_test_install
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
BACKEND_CALL_TESTED=YES
OIDC_BACKEND_ACCEPTANCE_TESTED=PASS
```

## 1. Public/private evidence boundary

The operational identifiers used for the controlled test installation remain in
a private governed record. This public artifact intentionally excludes Script
IDs, deployment IDs, OAuth client IDs, account identifiers, private paths, and
all token material.

```text
PUBLIC_PRIVATE_BOUNDARY=PASS
PRIVATE_GOVERNED_IDENTIFIERS_RECORDED=YES
PUBLIC_IDENTIFIER_VALUES=0
TOKEN_VALUES_CAPTURED=0
```

## 2. Completed hydration and test install

The competition Workspace adapter source was loaded as the complete five-file
set: manifest, auth helper, card template, config, and Meeting Follow-Up
routing. No legacy Marketplace add-on source or deployment was changed.

```text
COMPETITION_SOURCE_LOADED=YES
MANIFEST_LOADED=YES
REMOTE_FILE_SET=Auth,Cards,Config,MeetingFollowUp,appsscript
LEGACY_MARKETPLACE_SOURCE_TOUCHED=NO
CLASP_PUSH_VIA_PUBLIC_REPO_CONFIG=NO
STANDARD_GCP_PROJECT_BOUND=YES
OAUTH_CONSENT_BRAND_CONFIGURED=YES
OAUTH_CONSENT_ORG_INTERNAL_ONLY=YES
TEST_DEPLOYMENT_TYPE=HEAD_TEST_LATEST_CODE
TEST_DEPLOYMENT_APPLICATIONS=Gmail,Calendar
TEST_DEPLOYMENT_INSTALLED=YES
CONTROLLED_WORKSPACE_ACCOUNT_AUTHORIZED=YES
MARKETPLACE_PRODUCTION_DEPLOYMENT_CREATED=NO
```

The verified manifest uses only `openid`, external request, profile/email, and
Gmail/Calendar execute scopes. It has no Admin Directory, Drive, or CRM scope.

```text
EXPECTED_OAUTH_SCOPES_PRESENT=YES
ADMIN_DIRECTORY_SCOPE=NO
DRIVE_SCOPE=NO
CRM_SCOPE=NO
FORBIDDEN_SCOPE_HITS=0
```

## 3. Gmail and Calendar shell visibility

The controlled internal Workspace installation showed the MG Guide CardService
homepage in both Gmail and Calendar. The visible shell included **MG Guide**,
**Powered by AI Rolodex**, **Meeting Follow-Up**, and the SUCCESS and
AMBIGUOUS_CONTACT scenario buttons.

```text
ADDON_VISIBLE_IN_GMAIL=PASS
ADDON_VISIBLE_IN_CALENDAR=PASS
MG_GUIDE_BRANDING_VISIBLE=YES
POWERED_BY_AI_ROLODEX_VISIBLE=YES
MEETING_FOLLOW_UP_VISIBLE=YES
SUCCESS_BUTTON_VISIBLE=YES
AMBIGUOUS_CONTACT_BUTTON_VISIBLE=YES
```

Existing shell screenshots are retained under
[`proof/competition/screenshots/`](screenshots/).

## 4. Explicit non-actions at this checkpoint

```text
CLOUD_RUN_OIDC_BINDING=PERFORMED
JUDGE_BACKEND_BASE_URL_CONFIGURED=YES
URLFETCH_WHITELIST_POPULATED=YES
BACKEND_CALL_TESTED=YES
OIDC_BACKEND_ACCEPTANCE_TESTED=PASS
IAP_MUTATION=NO
LEGACY_MARKETPLACE_MUTATION=NO
CRM_WRITES=NO
RAW_IDENTITY_TOKEN_LOGGING=NO
TOKEN_VALUES_CAPTURED=0
```

## 5. Checkpoint status

```text
APPS_SCRIPT_PROJECT_CREATED=YES
STANDARD_GCP_PROJECT_BOUND=YES
COMPETITION_SOURCE_LOADED=YES
MANIFEST_LOADED=YES
EXPECTED_OAUTH_SCOPES_PRESENT=YES
TEST_DEPLOYMENT_INSTALLED=YES
CONTROLLED_WORKSPACE_ACCOUNT_AUTHORIZED=YES
ADDON_VISIBLE_IN_GMAIL=PASS
ADDON_VISIBLE_IN_CALENDAR=PASS
JUDGE_UX_ACCEPTANCE=PASS
```


Final OIDC binding: [`mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md`](mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md).
