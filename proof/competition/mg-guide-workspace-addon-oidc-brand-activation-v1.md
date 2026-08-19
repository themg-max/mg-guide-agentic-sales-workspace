# MG Guide Workspace Add-on - OIDC Brand Activation v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-oidc-brand-activation-v1.md
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## Current activation truth

The controlled competition add-on is bound to the dedicated Cloud Run judge
service with the private Apps Script OIDC audience. The IAP browser judge
service and the legacy Marketplace project were not changed.

```text
OIDC_BACKEND_ACCEPTANCE=PASS
APPS_SCRIPT_OIDC_AUDIENCE_RESOLVED=YES
CUSTOM_AUDIENCE_BOUND=YES
APPLICATION_AUDIENCE_MATCH=YES
JUDGE_BACKEND_BASE_URL_CONFIGURED=YES
URLFETCH_WHITELIST_CONFIGURED=YES
RUN_INVOKER_LEAST_PRIVILEGE=YES
PUBLIC_INVOKER_BINDINGS=0
LEGACY_MARKETPLACE_TOUCHED=NO
```

## Status

```text
HOST_SHELL_ACCEPTANCE=PASS
BRANDED_HOST_UX_ACCEPTANCE=IN_PROGRESS
VIDEO_AUTHORIZATION=POSTPONED
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
```

The remaining work is final branded-source hydration, refreshed Gmail and
Calendar host acceptance, and the post-fix reliability soak. Video recording is
not authorized.

See also
[`mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md`](mg-guide-workspace-addon-oidc-final-binding-and-acceptance-v1.md)
and
[`mg-guide-workspace-addon-brand-observability-polish-v1.md`](mg-guide-workspace-addon-brand-observability-polish-v1.md).
