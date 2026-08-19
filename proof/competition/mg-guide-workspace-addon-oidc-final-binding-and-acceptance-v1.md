# MG Guide Workspace Add-on - OIDC Final Binding and Acceptance v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## OIDC binding

The controlled Workspace deployment uses the Apps Script identity-token trust
chain with Cloud Run IAM custom-audience validation and application claim
validation. The private audience, service endpoint, and account identifiers are
not committed to this repository.

```text
OIDC_BACKEND_ACCEPTANCE=PASS
APPS_SCRIPT_OIDC_AUDIENCE_RESOLVED=YES
CUSTOM_AUDIENCE_BOUND=YES
APPLICATION_AUDIENCE_MATCH=YES
JUDGE_BACKEND_BASE_URL_CONFIGURED=YES
URLFETCH_WHITELIST_CONFIGURED=YES
PUBLIC_PRIVATE_BOUNDARY=PASS
TOKEN_VALUES_CAPTURED=0
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
```

## Acceptance status

```text
HOST_SHELL_ACCEPTANCE=PASS
BRANDED_HOST_UX_ACCEPTANCE=IN_PROGRESS
VIDEO_AUTHORIZATION=POSTPONED
LEGACY_MARKETPLACE_TOUCHED=NO
IAP_BROWSER_PATH_TOUCHED=NO
```

OIDC binding is complete. Final branded host UX acceptance remains separate:
the updated CardService source must be hydrated into the private competition
project, then Gmail and Calendar must be manually rechecked. Video recording is
postponed pending final review.
