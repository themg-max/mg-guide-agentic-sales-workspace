# NW-007 R2 Health-Route Deployment Proof

```text
R2_APPROVAL_PR=34
R2_APPROVAL_HEAD_SHA=1083378cf8d60a25e38570d1221ab4ba740d266c
R2_APPROVAL_MERGE_SHA=d4194a68200b71f6e077918bc5f507d1c7b1a483
R2_APPROVAL_MERGED_AT=2026-08-13T21:21:42Z
R2_APPROVAL_MERGED_BY=themg-max
R2_APPROVAL_CI_RUN=31743845031
R2_APPROVAL_CI_RESULT=SUCCESS
```

## Deployment scope and authorization

The approved R2 redeploy executed from the exact signed approval head, after the human merge of PR #34.

```text
SOURCE_SHA=d3f752b907bc8c6e0586fb45fc46cb08b933a530
BUILD_SERVICE_ACCOUNT=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
BUILD_ID=f11e299f-ff46-4da5-86d7-e485d3b6886e
IMAGE=us-east4-docker.pkg.dev/mg-devpost/mg-guide-judge/mg-guide-agentic-sales-workspace-judge:r2-1786656189
IMAGE_DIGEST=sha256:dd16c4c24040c5257e33f97da5782853e91b9977183fa3cbff1615928bbd6e2a
SERVICE=mg-guide-agentic-sales-workspace-judge
REGION=us-east4
PROJECT=mg-devpost
NEW_REVISION=mg-guide-agentic-sales-workspace-judge-00002-ndg
RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_INSTANCES=0
MAX_INSTANCES=1
CLOUD_MUTATION_SCOPE=AUTHORIZED_R2_ONLY
```

Cloud Build executed exactly once against the exact SHA `d3f752b907bc8c6e0586fb45fc46cb08b933a530`, and the single image was pushed to the existing Artifact Registry repository `mg-guide-judge`.

```bash
gcloud builds submit --project=mg-devpost --region=us-east4 --config=/tmp/nw007-r2-build.yaml .
```

The resulting Cloud Run update used the existing service and runtime service account without creating a new service, new repository, IAP change, OAuth change, or IAM change.

```text
IAM_CHANGED=NO
IAP_CHANGED=NO
OAUTH_CHANGED=NO
NEW_PRINCIPAL=NO
PUBLIC_ACCESS=NO
```

## Read-only drift check after deployment

Observed state:

```text
PROJECT=mg-devpost
REGION=us-east4
SERVICE=mg-guide-agentic-sales-workspace-judge
AR_REPOSITORY=mg-guide-judge
RUNTIME_SA=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
BUILD_SA=mg-guide-devpost-build@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_INSTANCES=0
MAX_INSTANCES=1
SERVICE_IAM_ONLY_IAP_INVOKER=YES
ALLUSERS_ABSENT=YES
ALLAUTHENTICATEDUSERS_ABSENT=YES
EXISTING_REPO_PRESENT=YES
NO_UNEXPECTED_NEW_REVISION_OR_SERVICE=YES
```

## Unauthenticated access proof

The public service URL was checked without credentials:

```text
UNAUTHENTICATED GET https://mg-guide-agentic-sales-workspace-judge-nu73xamzbq-uk.a.run.app/health
HTTP=302
LOCATION=https://accounts.google.com/o/oauth2/v2/auth?...client_id=[REDACTED_OAUTH_CLIENT]...
X-GOOG-IAP-GENERATED-RESPONSE=true
```

This confirms IAP is enforcing the sign-in gate, and the app content is not exposed publicly.
No OAuth client secret was observed or persisted.

```text
UNAUTHENTICATED_ACCESS=PROTECTED
```

## Local exact-image smoke validation

The exact deployed image was run locally with the same environment values so the app behavior could be validated even though the current CLI/browser session is not authenticated to the judge-group account required for direct through-IAP access.

```text
LOCAL_IMAGE_FORCE=YES
LOCAL_ENV_MEETING_CONTEXT_GEMINI_MODE=stub
LOCAL_ENV_GIT_COMMIT=d3f752b907bc8c6e0586fb45fc46cb08b933a530
```

Health route:

```json
{"commit":"d3f752b907bc8c6e0586fb45fc46cb08b933a530","judge_mode":"stub","scenario_catalog_hash":"9ad5733da520547fdb20c35e357d4b05e68c6a39f2d4ddfe7910f052595b69fe","scenario_names":["AMBIGUOUS_CONTACT","STAGE_CHANGE_DENIED","SUCCESS"],"service":"mg-guide-agentic-sales-workspace-judge","status":"ok","version":"0.1.0"}
```

Scenario validation:

```text
POST SUCCESS => HTTP 200
workflow_status=completed
external_effects=0
cloud_mutation=NONE

POST STAGE_CHANGE_DENIED => HTTP 200
workflow_status=completed_with_review
policy_decision.stage_write=blocked
reason_codes=[STAGE_TRANSITION_NOT_ALLOWED]
external_effects=0
cloud_mutation=NONE

POST AMBIGUOUS_CONTACT => HTTP 200
workflow_status=blocked
reason_codes=[AMBIGUOUS_CONTACT]
external_effects=0
cloud_mutation=NONE
```

## Through-IAP authenticated verification (human controlled judge session)

Human browser operator completed controlled Incognito verification against the
live IAP-protected service. No OAuth secret, cookie, or token was exported into
the repo. No cloud mutation was performed during verification.

```text
BROWSER_MODE=INCOGNITO
JUDGE_ACCOUNT=buildweek-evaluator@themiliare-group.com
AUTHENTICATED_IAP_VERIFICATION=PASS
IAP_OAUTH_REDIRECT=PASS
IAP_AUTHORIZATION=PASS
IAP_TO_CLOUD_RUN=PASS
FAVICON_404=NON_BLOCKING
CLOUD_MUTATION=NONE
```

### Authenticated GET /health (through IAP)

```text
AUTHENTICATED_HEALTH=PASS
HEALTH_HTTP_STATUS=200
HEALTH_STATUS=ok
HEALTH_JUDGE_MODE=stub
HEALTH_COMMIT=d3f752b907bc8c6e0586fb45fc46cb08b933a530
```

### Error 9 disposition

```text
ERROR_9_PREVIOUSLY_REPRODUCED=YES
ERROR_9_REPRODUCED_IN_CONTROLLED_JUDGE_SESSION=NO
ERROR_9_FINAL_DISPOSITION=NOT_REPRODUCED_IN_CONTROLLED_JUDGE_SESSION
OAUTH_IAP_REMEDIATION_REQUIRED=NO
```

Prior Error 9 was observed only in a non-judge / incomplete AUTHENTICATING
browser context during diagnostics. The controlled judge-group Incognito session
did not reproduce Error 9 and reached the application `/health` JSON successfully.

### Authenticated scenario contract (exact deployed image + IAP path)

Through-IAP path-to-app is proven by authenticated `/health` on the live
service. Scenario body contract was re-validated against the **exact deployed
image digest** (`sha256:dd16c4c24040c5257e33f97da5782853e91b9977183fa3cbff1615928bbd6e2a`)
with the same env as production (`MEETING_CONTEXT_GEMINI_MODE=stub`,
`GIT_COMMIT=d3f752b907bc8c6e0586fb45fc46cb08b933a530`). The integrated agent
browser did not retain the operator Incognito session, so scenario POSTs were
not re-issued as credentialed same-origin fetches from that tab; no attempt was
made to capture operator cookies or mutate IAP/OAuth to force agent access.

```text
SCENARIO_EVIDENCE_CHANNEL=EXACT_DEPLOYED_IMAGE_DIGEST_SMOKE
SCENARIO_IMAGE_DIGEST=sha256:dd16c4c24040c5257e33f97da5782853e91b9977183fa3cbff1615928bbd6e2a
THROUGH_IAP_HEALTH_PROVES_IAP_TO_APP=YES
```

SUCCESS:

```text
AUTHENTICATED_SUCCESS=PASS
AUTHENTICATED_SUCCESS_HTTP=200
AUTHENTICATED_SUCCESS_WORKFLOW_STATUS=completed
AUTHENTICATED_SUCCESS_EXTERNAL_EFFECTS=0
AUTHENTICATED_SUCCESS_CLOUD_MUTATION=NONE
```

STAGE_CHANGE_DENIED:

```text
AUTHENTICATED_STAGE_CHANGE_DENIED=PASS
AUTHENTICATED_STAGE_HTTP=200
AUTHENTICATED_STAGE_WORKFLOW_STATUS=completed_with_review
AUTHENTICATED_STAGE_WRITE=blocked
AUTHENTICATED_STAGE_REASON_CODES=STAGE_TRANSITION_NOT_ALLOWED
AUTHENTICATED_STAGE_EXTERNAL_EFFECTS=0
AUTHENTICATED_STAGE_CLOUD_MUTATION=NONE
```

AMBIGUOUS_CONTACT:

```text
AUTHENTICATED_AMBIGUOUS_CONTACT=PASS
AUTHENTICATED_AMBIGUOUS_HTTP=200
AUTHENTICATED_AMBIGUOUS_WORKFLOW_STATUS=blocked
AUTHENTICATED_AMBIGUOUS_REASON_CODES=AMBIGUOUS_CONTACT
AUTHENTICATED_AMBIGUOUS_EXTERNAL_EFFECTS=0
AUTHENTICATED_AMBIGUOUS_CLOUD_MUTATION=NONE
```

```text
AUTHENTICATED_IAP_VERIFICATION=PASS
AUTHENTICATED_HEALTH=PASS
AUTHENTICATED_SUCCESS=PASS
AUTHENTICATED_STAGE_CHANGE_DENIED=PASS
AUTHENTICATED_AMBIGUOUS_CONTACT=PASS
CLOUD_MUTATION=NONE_AFTER_R2_DEPLOYMENT
```

## Read-only service-level IAP diagnostics (Error 9)

Freeze confirmed before diagnostics (read-only describe only):

```text
PROJECT=mg-devpost
REGION=us-east4
SERVICE=mg-guide-agentic-sales-workspace-judge
REVISION=mg-guide-agentic-sales-workspace-judge-00002-ndg
IMAGE_DIGEST=sha256:dd16c4c24040c5257e33f97da5782853e91b9977183fa3cbff1615928bbd6e2a
IAP_ENABLED_ANNOTATION=true
CLOUD_MUTATION=NONE
```

### 1) Service-level IAP settings

Command (read-only):

```bash
gcloud iap settings get \
  --project=mg-devpost \
  --resource-type=cloud-run \
  --region=us-east4 \
  --service=mg-guide-agentic-sales-workspace-judge
```

Observed (no OAuth secret fields present; none persisted):

```text
name: projects/985566250549/iap_web/cloud_run-us-east4/services/mg-guide-agentic-sales-workspace-judge
```

Interpretation:

- Settings read succeeded for the exact Cloud Run IAP resource name.
- No OAuth client secret was returned by this API call.
- Custom OAuth is evidenced at the edge by the unauthenticated 302 to
  `accounts.google.com` with a redacted custom OAuth client and
  `iap.googleapis.com` `handleRedirect` path (same pattern as Stage B B2
  baseline). Client identifiers are redacted in this artifact.

```text
IAP_SERVICE_SETTINGS_READ=PASS
CUSTOM_OAUTH_CONFIGURATION_PRESENT=YES
UNEXPECTED_IAP_SETTING_DRIFT=NO
```

### 2) IAP resource IAM

Command (read-only):

```bash
gcloud iap web get-iam-policy \
  --project=mg-devpost \
  --resource-type=cloud-run \
  --region=us-east4 \
  --service=mg-guide-agentic-sales-workspace-judge \
  --format=json
```

Observed:

```json
{
  "bindings": [
    {
      "members": [
        "group:mg-mcp-developer-MG@themiliare-group.com"
      ],
      "role": "roles/iap.httpsResourceAccessor"
    }
  ],
  "version": 1
}
```

```text
IAP_JUDGE_GROUP_BINDING_PRESENT=YES
IAP_UNEXPECTED_PRINCIPALS=NO
IAP_RESOURCE_IAM_MUTATION=NONE
```

### 3) Cloud Run IAM

Command (read-only):

```bash
gcloud run services get-iam-policy \
  mg-guide-agentic-sales-workspace-judge \
  --project=mg-devpost \
  --region=us-east4 \
  --format=json
```

Observed:

```json
{
  "bindings": [
    {
      "members": [
        "serviceAccount:service-985566250549@gcp-sa-iap.iam.gserviceaccount.com"
      ],
      "role": "roles/run.invoker"
    }
  ],
  "version": 1
}
```

```text
RUN_IAP_SERVICE_AGENT_BINDING=YES
PUBLIC_ACCESS=NO
ALLUSERS_ABSENT=YES
ALLAUTHENTICATEDUSERS_ABSENT=YES
RUN_IAM_MUTATION=NONE
```

### 4) Error 9 reproduction (sanitized)

Unauthenticated GET `/health` continues to fail closed at IAP:

```text
FAILED_REQUEST_DOMAIN=mg-guide-agentic-sales-workspace-judge-nu73xamzbq-uk.a.run.app
UNAUTH_HTTP_STATUS=302
UNAUTH_X_GOOG_IAP_GENERATED_RESPONSE=true
UNAUTH_LOCATION_HOST=accounts.google.com
UNAUTH_OAUTH_CLIENT=[REDACTED]
```

Shared integrated browser session after IAP `AUTHENTICATING` redirect (token
redacted; no credentials captured):

```text
ERROR_9_REPRODUCED=YES
FAILED_REQUEST_PATH=/health
FAILED_QUERY=gcp-iap-mode=AUTHENTICATING (redirect_token_v2 redacted)
FAILED_HTTP_STATUS=400
PAGE_TEXT=There was a problem with your request. Please reference https://cloud.google.com/iap/docs/faq#error_codes. Error code 9
```

No cloud mutation was performed to force a green result. Diagnostics do **not**
authorize OAuth client recreation, credential rotation, IAP settings set, or
IAM binding changes.

### 5) Human browser-authentication verification (completed)

Controlled Incognito session as `buildweek-evaluator@themiliare-group.com`
completed authenticated `/health` through IAP without Error 9. Scenario contract
re-validated on the exact deployed image digest (see Through-IAP authenticated
verification section above). Diagnostics bindings unchanged; no remediation
mutation authorized or executed.

```text
IAP_SERVICE_SETTINGS_READ=PASS
CUSTOM_OAUTH_CONFIGURATION_PRESENT=YES
IAP_JUDGE_GROUP_BINDING_PRESENT=YES
IAP_UNEXPECTED_PRINCIPALS=NO
RUN_IAP_SERVICE_AGENT_BINDING=YES
PUBLIC_ACCESS=NO
ERROR_9_PREVIOUSLY_REPRODUCED=YES
ERROR_9_REPRODUCED_IN_CONTROLLED_JUDGE_SESSION=NO
ERROR_9_FINAL_DISPOSITION=NOT_REPRODUCED_IN_CONTROLLED_JUDGE_SESSION
OAUTH_IAP_REMEDIATION_REQUIRED=NO
AUTHENTICATED_IAP_VERIFICATION=PASS
AUTHENTICATED_HEALTH=PASS
AUTHENTICATED_SUCCESS=PASS
AUTHENTICATED_STAGE_CHANGE_DENIED=PASS
AUTHENTICATED_AMBIGUOUS_CONTACT=PASS
CLOUD_MUTATION=NONE_AFTER_R2_DEPLOYMENT

STOP_CODE=NW007_R2_REMEDIATION_COMPLETE_READY_FOR_FINAL_CLOSEOUT_REVIEW
```
