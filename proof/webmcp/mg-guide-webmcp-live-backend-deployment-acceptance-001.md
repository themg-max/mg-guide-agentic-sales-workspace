# MG Guide WebMCP Live Backend Deployment Acceptance 001

```text
PROOF_ID=MG_GUIDE_WEBMCP_LIVE_BACKEND_DEPLOYMENT_ACCEPTANCE_001
RECORDED_AT_UTC=2026-09-01T20:41:00Z
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

SOURCE_AUTHORIZATION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_AUTHORIZATION_001
SOURCE_AUTHORIZATION_MERGE_SHA=a42972652a837897004eb1648c550ab4abb96203
HUMAN_ACTIVATION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_HUMAN_ACTIVATION_001
HUMAN_ACTIVATION_MERGE_SHA=6d4cb026af02f9bc3115aac7067a30efd5d3cbd2
AUTHORITY_CONSUMPTION_ID=MG_GUIDE_WEBMCP_PUBLIC_SYNTHETIC_BACKEND_DEPLOYMENT_CONSUMPTION_001
AUTHORITY_CONSUMPTION_MERGE_SHA=7f44ae66d7bd669a745af795c5239ae7e23f0af2
AUTHORITY_CONSUMED=YES
AUTHORITY_REUSABLE=NO

PUBLIC_SOURCE_SHA=2847f5a26dbc61716736b60eedb66e399c102a33
BUILD_ID=e2884da0-42f3-474b-bb0f-1a149d0fb109
IMAGE_URI=us-east4-docker.pkg.dev/ai-rolodex-to-crm/cloud-run-source-deploy/mg-guide-webmcp
IMAGE_DIGEST=sha256:435ec8cc3af6c5980d85cdb026cb9aeb70f788e9bd6b34d5af8a5fb4346e1d2d

PROJECT=ai-rolodex-to-crm
REGION=us-east4
SERVICE=mg-guide-webmcp
BACKEND_REVISION=mg-guide-webmcp-00001-222
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
CLOUD_RUN_SERVICE_URL=https://mg-guide-webmcp-ydru2khnaa-uk.a.run.app
RUNTIME_IDENTITY=mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_PROJECT_ROLE_COUNT=0
RUNTIME_USER_MANAGED_KEY_COUNT=0

INGRESS=all
INVOKER_IAM_DISABLED=true
INGRESS_MODE=DIRECT_PUBLIC_CLOUD_RUN
DIRECT_PUBLIC_INGRESS_FEASIBLE=YES
```

## Deployment configuration readback

```text
SERVICE=mg-guide-webmcp
RUNTIME_IDENTITY=mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
IMAGE=@sha256:435ec8cc3af6c5980d85cdb026cb9aeb70f788e9bd6b34d5af8a5fb4346e1d2d
SECRET_ENV_BINDINGS=0
SECRET_VOLUME_BINDINGS=0
VOLUME_MOUNTS=0
VOLUMES=0
APP_ENV_VARS=2
MEETING_CONTEXT_GEMINI_MODE=stub
WEBMCP_CORS_MODE=production
```

The runtime identity has no project-level role binding and no user-managed
key. The default compute service account was not used.

## Live API acceptance

| Check | Result |
| --- | --- |
| `GET /health` | PASS — HTTP 200 |
| Health status | PASS — `ok` |
| Statelessness | PASS — `server_session_state_required=false`, `webmcp_browser_state=true` |
| Synthetic boundary | PASS — `real_customer_data=false`, `live_ghl_calls=0`, `live_crm_mutations=0`, `real_emails_sent=0` |
| `POST SUCCESS` | PASS — HTTP 200, `ux_state=COMPLETED`, `follow_up_draft_status=READY`, `external_effects=0`, `cloud_mutation=NONE` |
| `POST AMBIGUOUS_CONTACT` | PASS — HTTP 200, `ux_state=NEEDS_REVIEW`, `follow_up_draft_status=NOT_AVAILABLE`, `reason=RELATIONSHIP_REVIEW_REQUIRED`, `external_effects=0` |
| Denied `live` | PASS — HTTP 400 |
| Denied `crm_write` | PASS — HTTP 400 |
| Denied `send_email` | PASS — HTTP 400 |
| Denied `provider` | PASS — HTTP 400 |
| Denied `contact_id` | PASS — HTTP 400 |
| Denied `location_id` | PASS — HTTP 400 |
| Denied `credentials` | PASS — HTTP 400 |
| Denied `instructions` | PASS — HTTP 400 |
| Denied `transcript` | PASS — HTTP 400 |
| Denied `url` | PASS — HTTP 400 |

## Production CORS acceptance

```text
APPROVED_ORIGIN=https://ai-rolodex-landing-831270426395.us-east4.run.app
OPTIONS_APPROVED_ORIGIN=HTTP_204
ACCESS_CONTROL_ALLOW_ORIGIN=approved origin exactly
VARY=Origin
OPTIONS_UNKNOWN_ORIGIN=HTTP_403
WILDCARD_ACAO=ABSENT
CORS_ACCEPTANCE=PASS
```

## Final synthetic-effect counters

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
SECRET_PAYLOAD_READS=0
REAL_CUSTOMER_DATA=0
```

## Handoff status

The backend is accepted and its public URL is eligible to be placed only in
the private host lane's `landing-page/public/mg-guide/config.js`. Landing
deployment and traffic promotion remain outside this backend authority. Actual
WebMCP browser discovery and agent invocation remain pending until a separate
landing candidate is authorized and deployed.
