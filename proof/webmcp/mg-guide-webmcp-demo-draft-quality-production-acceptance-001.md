# MG Guide WebMCP Demo Draft Quality Production Acceptance 001

PROOF_ID=mg-guide-webmcp-demo-draft-quality-production-acceptance-001
PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
TARGET_PROJECT=ai-rolodex-to-crm
TARGET_REGION=us-east4
TARGET_SERVICE=mg-guide-webmcp
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
LANDING_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
EVIDENCE_CAPTURED_UTC=2026-09-02T00:35Z

## Source Binding

SOURCE_PR=439
SOURCE_PR_STATUS=MERGED
SOURCE_REVIEWED_HEAD=3f210916d98f15a6c204aebff4a7865861f1aaee
SOURCE_MERGE_SHA=4b1e58046fa529c1d9a5df489c2aab8698544dc1
DEPLOY_SOURCE_BRANCH=main
DEPLOY_SOURCE_HEAD=4b1e58046fa529c1d9a5df489c2aab8698544dc1
SOURCE_MERGE_SHA_ON_ORIGIN_MAIN=PASS

## Before State

PREVIOUS_REVISION=mg-guide-webmcp-00001-222
PREVIOUS_IMAGE=us-east4-docker.pkg.dev/ai-rolodex-to-crm/cloud-run-source-deploy/mg-guide-webmcp@sha256:435ec8cc3af6c5980d85cdb026cb9aeb70f788e9bd6b34d5af8a5fb4346e1d2d
PREVIOUS_IMAGE_DIGEST=sha256:435ec8cc3af6c5980d85cdb026cb9aeb70f788e9bd6b34d5af8a5fb4346e1d2d
PREVIOUS_RUNTIME_SERVICE_ACCOUNT=mg-guide-webmcp-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PREVIOUS_INGRESS=all
PREVIOUS_ENV=MEETING_CONTEXT_GEMINI_MODE=stub,WEBMCP_CORS_MODE=production
PREVIOUS_SECRET_BINDINGS=[]
PREVIOUS_URLS=https://mg-guide-webmcp-831270426395.us-east4.run.app,https://mg-guide-webmcp-ydru2khnaa-uk.a.run.app

## Build And Deployment

BUILD_ID=ba8b92b8-f112-474b-beaa-3704fd22cb1b
IMAGE_URI=us-east4-docker.pkg.dev/ai-rolodex-to-crm/cloud-run-source-deploy/mg-guide-webmcp:pr439-4b1e580-20260902T003113Z
IMAGE_DIGEST=sha256:25d544d55b386d7bbcd1eb942a8c5769e248456d0bbd760501e3c49ce5f264aa
DEPLOYED_IMAGE=us-east4-docker.pkg.dev/ai-rolodex-to-crm/cloud-run-source-deploy/mg-guide-webmcp@sha256:25d544d55b386d7bbcd1eb942a8c5769e248456d0bbd760501e3c49ce5f264aa
DEPLOYED_REVISION=mg-guide-webmcp-00002-zoc
DEPLOYMENT_STRATEGY=deploy_no_traffic_with_tag_then_validate_then_route_100_percent
VALIDATION_TAG_URL=https://pr439-acceptance---mg-guide-webmcp-ydru2khnaa-uk.a.run.app

## Post-Deploy Readback

SERVICE=mg-guide-webmcp
REGION=us-east4
URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
LATEST_READY_REVISION=mg-guide-webmcp-00002-zoc
TRAFFIC=mg-guide-webmcp-00002-zoc:100
RUNTIME_SERVICE_ACCOUNT_UNCHANGED=YES
SECRET_BINDINGS_UNCHANGED=YES
CORS_CONFIG_UNCHANGED=YES
INGRESS_UNCHANGED=YES
ENVIRONMENT_CONFIGURATION_UNCHANGED=YES

## Backend Health

COMMAND=curl -sS -D /tmp/live-health.headers -o /tmp/live-health.json https://mg-guide-webmcp-831270426395.us-east4.run.app/health
HTTP=200
HEALTH=PASS
HEALTH_STATUS=ok
CURRENT_TRANSCRIPT_SOURCE=synthetic_fixture
SERVER_SESSION_STATE_REQUIRED=false
WEBMCP_BROWSER_STATE=true

## SUCCESS Acceptance

COMMAND=curl -sS -H 'Content-Type: application/json' -d '{"scenario":"SUCCESS"}' https://mg-guide-webmcp-831270426395.us-east4.run.app/webmcp/meeting-follow-up
HTTP=200
workflow_status=completed
ux_state=COMPLETED
follow_up_draft.status=READY
follow_up_draft.subject=Following up on our conversation
follow_up_draft.requires_human_send=true
external_effects=0
cloud_mutation=NONE

CUSTOMER_DRAFT_HUMAN_READABLE=PASS
DRAFT_SUBJECT=PASS
OWNER_METADATA_NOT_IN_CUSTOMER_COPY=PASS
MID_SENTENCE_TRUNCATION_REMOVED=PASS
REQUIRES_HUMAN_SEND=TRUE
SUCCESS_FLOW=PASS

Verified customer draft text contains natural equivalents of:

- retirement income planning
- maintaining liquidity
- sixty-day timeline
- recommendation review

Verified customer draft text does not contain:

- (owner:
- Next step:
- raw governance/internal wording

Verified body preview ends naturally:

`Best, Alex`

## AMBIGUOUS_CONTACT Acceptance

COMMAND=curl -sS -H 'Content-Type: application/json' -d '{"scenario":"AMBIGUOUS_CONTACT"}' https://mg-guide-webmcp-831270426395.us-east4.run.app/webmcp/meeting-follow-up
HTTP=200
workflow_status=blocked
ux_state=NEEDS_REVIEW
follow_up_draft.status=NOT_AVAILABLE
follow_up_draft.reason=RELATIONSHIP_REVIEW_REQUIRED
follow_up_draft.requires_human_send=true
external_effects=0
cloud_mutation=NONE
AMBIGUOUS_CONTACT_FAIL_CLOSED=PASS

## Stable Product Acceptance

LANDING_DEPLOYMENT=NO
LANDING_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
CHECK_METHOD=temporary Playwright browser automation using installed Chrome channel
SUCCESS_VISIBLE_COMPLETED=PASS
SUCCESS_VISIBLE_FOLLOW_UP_DRAFT=PASS
SUCCESS_VISIBLE_SUBJECT=PASS
SUCCESS_VISIBLE_DRAFT_FLUENT=PASS
AMBIGUOUS_VISIBLE_NEEDS_REVIEW=PASS
AMBIGUOUS_VISIBLE_NOT_AVAILABLE=PASS
AMBIGUOUS_VISIBLE_RELATIONSHIP_REVIEW_REQUIRED=PASS
SUCCESS_SCREENSHOT=/tmp/mg-guide-stable-success.png
AMBIGUOUS_SCREENSHOT=/tmp/mg-guide-stable-ambiguous.png

## WebMCP Contract Recheck

SOURCE_REGISTRATION_STATIC_CHECK=PASS
REGISTERED_TOOL_NAMES_IN_SOURCE=process_meeting_follow_up,get_current_follow_up_state,get_follow_up_draft
WEBMCP_TOOL_COUNT=3
NATIVE_WEBMCP_CAPABLE_CHROME_CONNECTOR=BLOCKED
NATIVE_WEBMCP_INVOCATION=BLOCKED

Native Chrome connector evidence:

- `mcp__node_repl.js` failed before returning Chrome documentation: `Transport closed`.
- `mcp__node_repl.js_reset` also failed: `Transport closed`.
- Chrome AppleScript JavaScript execution was not usable because Chrome reported JavaScript from Apple Events is turned off.
- Temporary Playwright/browser automation reported `typeof document.modelContext === "undefined"`, so it cannot substitute for the approved native WebMCP-capable Chrome path.

This proof does not claim native `document.modelContext.getTools()` or `document.modelContext.executeTool(...)` PASS.

## Effect Counters

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
SECRET_PAYLOAD_READS=0
EXTERNAL_EFFECTS=0

Evidence basis:

- `/health` reports `live_ghl_calls=0`, `live_crm_mutations=0`, `real_emails_sent=0`, `real_customer_data=false`.
- SUCCESS response reports `external_effects=0` and `cloud_mutation=NONE`.
- AMBIGUOUS_CONTACT response reports `external_effects=0` and `cloud_mutation=NONE`.
- Cloud Run service readback has no `secretKeyRef` entries.

## Final Disposition

BACKEND_DEPLOYMENT=PASS
BACKEND_HEALTH=PASS
SUCCESS_FLOW=PASS
AMBIGUOUS_CONTACT_FAIL_CLOSED=PASS
STABLE_PRODUCT_VISIBLE_ACCEPTANCE=PASS
NATIVE_WEBMCP_INVOCATION=BLOCKED
FINAL_DISPOSITION=BLOCKED_ON_NATIVE_CHROME_CONNECTOR_VERIFICATION

No landing deployment, AI Rolodex traffic change, IAM change, service account change, secret change, CORS change, CRM access, HighLevel access, CRM mutation, email send, WebMCP tool/schema change, new route, new auth, new storage, or private AI Rolodex repo mutation was performed.
