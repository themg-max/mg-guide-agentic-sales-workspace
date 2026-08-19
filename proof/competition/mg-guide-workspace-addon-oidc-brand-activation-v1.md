# MG Guide Workspace Add-on — OIDC Brand Activation v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-oidc-brand-activation-v1.md
UNIT=MG_GUIDE_WORKSPACE_ADDON_OIDC_BRAND_ACTIVATION_V1
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
REGION=us-east4
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## 1. Dedicated Cloud Run service

A dedicated competition add-on judge service was created from the same proven
judge image as the existing browser service. The existing IAP browser judge
service was inspected only to obtain the image reference; it was not
reconfigured or otherwise changed.

```text
CLOUD_RUN_ADDON_SERVICE_READY=YES
DEDICATED_SERVICE_IDENTIFIER=REDACTED
DEDICATED_SERVICE_URL=REDACTED
PROVEN_JUDGE_IMAGE_REFERENCE=REDACTED
SAME_PROVEN_JUDGE_IMAGE=YES
EXISTING_IAP_BROWSER_SERVICE_TOUCHED=NO
MEETING_CONTEXT_GEMINI_MODE=stub
```

The dedicated service starts in application-level `identity_token` mode without
an audience value. This is fail-closed: the demo route rejects requests until
the exact audience can be supplied. `local_demo` is not configured.

```text
JUDGE_ADDON_AUTH_MODE=identity_token
JUDGE_ADDON_OIDC_AUDIENCE=NOT_CONFIGURED
JUDGE_ADDON_ALLOWED_HD=themiliare-group.com
FAIL_CLOSED_BEFORE_AUDIENCE_BINDING=YES
LOCAL_DEMO_PUBLIC_INGRESS_GUARD=ENFORCED_BY_APPLICATION
```

## 2. IAM boundary

Only the controlled internal judge identity has `roles/run.invoker` on the
dedicated service. No public principal has that role. The temporary project
Editor grant used solely for the completed Apps Script GCP binding was removed.

```text
RUN_INVOKER_LEAST_PRIVILEGE=YES
CONTROLLED_JUDGE_ACCOUNT=REDACTED
PUBLIC_INVOKER_BINDINGS=0
PROJECT_EDITOR_GRANT_REMOVED=YES
```

## 3. Audience and private Apps Script configuration status

The active automation credential can administer the Cloud Run resource but
does not include the Apps Script project scope. A temporary private audience
probe was denied before it read or modified Script source. No raw JWT,
signature, Authorization header, or token-derived length was logged or
persisted.

```text
APPS_SCRIPT_OIDC_AUDIENCE_RESOLVED=NO
AUDIENCE_PROBE_SOURCE_MUTATED=NO
TOKEN_VALUES_CAPTURED=0
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
CUSTOM_AUDIENCE_BOUND=NO
APPLICATION_AUDIENCE_MATCH=NO
JUDGE_BACKEND_BASE_URL_CONFIGURED=NO
URLFETCH_WHITELIST_CONFIGURED=NO
```

## 4. Activation status

```text
MG_GUIDE_BRAND_PALETTE_APPLIED=YES
MG_GUIDE_LOGO_URL_CONFIGURED=YES
ADDON_AUTH_ROUTE_SCOPE_TEST=PASS
LOCAL_DEMO_PUBLIC_INGRESS_GUARD=PASS
OIDC_BACKEND_ACCEPTANCE_TESTED=NO
JUDGE_UX_ACCEPTANCE=BLOCKED
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
REAL_CUSTOMER_DATA=NO
```

The only remaining activation prerequisite is a credential with the private
Apps Script project scope, used to resolve the signed-in add-on token's `aud`
claim and set the private backend URL/whitelist. No live Gmail or Calendar
scenario was run while that prerequisite is absent.
