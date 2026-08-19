# MG Guide Workspace Add-on — Auth Contract v1

```text
ARTIFACT=docs/architecture/mg-guide-workspace-addon-auth-contract-v1.md
WORKFLOW=meeting_follow_up_v1
SURFACE=MG_GUIDE_WORKSPACE_ADDON
AUTH_CONTRACT_ID=MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1
STATUS=DEFINED_FOR_COMPETITION_ADAPTER
PRODUCTION_IAM_MUTATION=NO
IAP_RECONFIGURATION=NO
```

## 1. Chosen contract

```text
AUTH_MECHANISM=APPS_SCRIPT_OIDC_IDENTITY_TOKEN
TOKEN_SOURCE=ScriptApp.getIdentityToken()
TRANSPORT=HTTPS Authorization: Bearer <identity_token>
SIDE_EFFECTS_FROM_ADDON=NONE
```

The Workspace add-on authenticates to the MG Guide judge / demo view-model API
using the **Apps Script OpenID Connect identity token** for the signed-in user.

Trust chain for the dedicated competition add-on judge service:

```text
Apps Script identity token (ScriptApp.getIdentityToken)
  -> Cloud Run IAM custom-audience validation
  -> roles/run.invoker (controlled Workspace principal only)
  -> application claim validation (JUDGE_ADDON_AUTH_MODE=identity_token)
```

The add-on token is a Google-signed OIDC JWT for the signed-in Workspace user.
It is **in scope** for Cloud Run IAM when the service is configured with the
Apps Script token `aud` as a **custom audience** and the caller holds
`roles/run.invoker`. Application-level validation then enforces issuer,
audience, expiry, email, and optional hosted-domain claims.

This is **not**:

| Mechanism | Relationship to this contract |
| --- | --- |
| IAP browser authentication | Distinct. NW-007 IAP gates the human browser path to the separate browser judge service. Not used on the dedicated add-on judge path. |
| Generic service-to-service invoker tokens with audience = service URL | Related but not identical. Add-on tokens use the Apps Script OIDC audience (custom audience on Cloud Run), not the default service-URL audience. |
| API key authentication | Forbidden for the add-on path. |
| MCP authentication | Out of band; never used by CardService. |
| OAuth access / refresh tokens | Not sent by the add-on on this path. |

## 2. Required Apps Script scopes

Competition add-on manifest (`workspace_addon/appsscript.json`) requires:

```text
https://www.googleapis.com/auth/script.external_request
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
openid
https://www.googleapis.com/auth/gmail.addons.execute
https://www.googleapis.com/auth/calendar.addons.execute
```

Notes:

- `openid` is required so `ScriptApp.getIdentityToken()` can mint a usable OIDC JWT.
- No Admin Directory, Drive write, Sheets, Chat, or CRM scopes are required for
  the synthetic Meeting Follow-Up judge path.
- Gmail/Calendar execute scopes enable host entry points only; synthetic demo
  scenarios do **not** read message bodies or event payloads.

## 3. Backend validation requirements

When `JUDGE_ADDON_AUTH_MODE=identity_token`, the backend **must** validate:

| Check | Rule |
| --- | --- |
| Presence | `Authorization: Bearer <jwt>` with three base64url segments |
| Signature | Verify against Google JWKS (`https://www.googleapis.com/oauth2/v3/certs`) |
| Issuer (`iss`) | Exactly `https://accounts.google.com` or `accounts.google.com` |
| Audience (`aud`) | Exactly the configured `JUDGE_ADDON_OIDC_AUDIENCE` (Apps Script OAuth client / bound audience) |
| Expiration (`exp`) | `exp > now` (allow small skew via `JUDGE_ADDON_OIDC_CLOCK_SKEW_SECONDS`, default 60) |
| Email present | `email` claim required for judge-account audit classification |
| Email verified | `email_verified` must be true when present |
| Hosted domain (optional) | If `JUDGE_ADDON_ALLOWED_HD` is set, `hd` must match |

Rejected tokens return HTTP 401 with a non-sensitive body:

```json
{"error":"auth_error","code":"AUTH_ERROR","message":"Identity token validation failed."}
```

```text
RAW_IDENTITY_TOKEN_LOGGING=FORBIDDEN
TOKEN_VALUES_IN_LOGS=0
TOKEN_VALUES_IN_RESPONSES=0
TOKEN_VALUES_IN_PROOF=0
```

## 4. Auth modes (backend)

| Mode | Env | Behavior |
| --- | --- | --- |
| `off` | `JUDGE_ADDON_AUTH_MODE=off` (default) | No Bearer check. Preserves existing local/stub and IAP-fronted Cloud Run behavior. |
| `identity_token` | `JUDGE_ADDON_AUTH_MODE=identity_token` | Full OIDC validation per §3. |
| `local_demo` | `JUDGE_ADDON_AUTH_MODE=local_demo` | Accepts only `X-MG-Guide-Demo-Auth: local-demo` for in-process / localhost CardService simulation. The demo endpoint returns `503 LOCAL_DEMO_PUBLIC_INGRESS_FORBIDDEN` when Cloud Run sets `K_SERVICE`. |

```text
LOCAL_DEMO_MODE_PUBLIC_INGRESS=FORBIDDEN
LOCAL_DEMO_PUBLIC_INGRESS_GUARD=ENFORCED
DEFAULT_MODE_UNCHANGED=off
```

## 5. Judge-account identity behavior

```text
JUDGE_ACCOUNT_TYPE=CONTROLLED_INTERNAL_WORKSPACE
EXPECTED_BEHAVIOR=Token email identifies the controlled Workspace user; backend does not mint alternate identities.
REAL_CUSTOMER_DATA=NO
```

The add-on must not impersonate other users and must not use service-account
domain-wide delegation.

## 6. Endpoint binding

```text
METHOD=POST
PATH=/demo/meeting-follow-up
BODY={"scenario":"SUCCESS"|"AMBIGUOUS_CONTACT"|"STAGE_CHANGE_DENIED"}
```

Backend base URL is supplied via Apps Script **Script Property**
`JUDGE_BACKEND_BASE_URL` (private deploy only; never committed to the public repository).
Deployed `urlFetchWhitelist` is populated with the HTTPS service prefix in the
private Script project only; the public manifest keeps an empty whitelist.

## 7. Explicit non-goals

```text
PRODUCTION_CRM_AUTH=NO
GHL_TOKEN_HANDLING=NO
IAP_RECONFIG_IN_THIS_UNIT=NO
CLOUD_RUN_IAM_EXPANSION=NO
MCP_AUTH_REUSE=NO
```

## 8. Status

```text
AUTH_CONTRACT_DEFINED=YES
AUTH_VALIDATOR_IMPLEMENTED=YES
TEST_DEPLOYMENT_INSTALLED=YES
LEGACY_MARKETPLACE_TOUCHED=NO
DEDICATED_ADDON_JUDGE_SERVICE=YES
CLOUD_RUN_CUSTOM_AUDIENCE_BOUND=YES
APPLICATION_IDENTITY_TOKEN_MODE=YES
PRODUCTION_IAP_BROWSER_PATH_TOUCHED=NO
```

The competition repository holds the sanitized adapter source and the
validator used by tests and `identity_token` mode. Private operator records
hold the bound audience value, backend URL, and activation evidence. Public
proof never includes raw identity tokens, audience secrets, or private
endpoints.
