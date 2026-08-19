# MG Guide Workspace Add-on - Brand and Observability Polish v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-brand-observability-polish-v1.md
UNIT=MG_GUIDE_WORKSPACE_ADDON_BRANDED_HOST_UX_AND_OBSERVABILITY_POLISH_V1
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
VIDEO_AUTHORIZATION=POSTPONED
LIVE_CRM_EXECUTION=NOT_PERFORMED
CRM_MUTATIONS_PERFORMED=NO
REAL_CUSTOMER_DATA=NO
```

## Evidence reconciliation

```text
OIDC_BACKEND_ACCEPTANCE=PASS
HOST_SHELL_ACCEPTANCE=PASS
BRANDED_HOST_UX_ACCEPTANCE=IN_PROGRESS
VIDEO_AUTHORIZATION=POSTPONED
EVIDENCE_CONTRADICTIONS=0
```

## Continuation authority and public branding asset

The separately committed continuation authority is remotely durable on PR #91.
The verified, public competition asset is hosted independently of the feature
branch and is used identically by `Config.gs` and `appsscript.json`.

```text
DEDICATED_ADDON_SERVICE_AUTHORITY=APPROVED
AUTHORIZATION_REMOTE_DURABILITY=PASS
RESCUE_ASSET_INTEGRITY=PASS
MG_GUIDE_PUBLIC_HTTPS=PASS
MG_GUIDE_PRIMARY_ASSET=https://storage.googleapis.com/mg-devpost-assets/mg-guide/mg-guide-128x128.png
CONFIG_MANIFEST_LOGO_PARITY=PASS
RAW_GITHUB_LOGO_URL_PRESENT=NO
```

## Repository card template

The competition template now uses the MG Guide square header image, retains
attribution in the header subtitle, removes the attribution-only fixed footer,
and presents human-friendly scenario labels while preserving backend selectors.
The primary result hierarchy is Outcome, Meeting summary, Relationship, Policy,
Six-stage workflow summary, Salesperson next step, Audit, and Integrity.

```text
MG_GUIDE_CARD_TEMPLATE=PASS
MG_GUIDE_HEADER_LOGO_CONFIGURED=YES
ATTRIBUTION_BUTTON_REMOVED=YES
TECHNICAL_ENUM_LABELS_HIDDEN_FROM_PRIMARY_UX=YES
SIX_STAGE_SUMMARY_VISIBLE=YES
```

## Cloud Run 500 RCA

Bounded revision logs for the specified interval showed one successful request
followed by five endpoint-generated 500 responses. The service process creates
one `JudgeSurfaceApp`; its long-lived `WorkflowRunner` retained terminal
synthetic fixture run IDs. Replay of either static scenario therefore hit the
runner's intentional duplicate-run rejection and the judge adapter returned
`run_failed` as HTTP 500. This was neither an IAM/OIDC rejection nor a Cloud
Run routing failure.

The repair keeps runner duplicate behavior unchanged and gives the normal judge
endpoint a fresh runner registry per HTTP request. A regression test verifies
repeated SUCCESS and AMBIGUOUS_CONTACT requests return 200.

```text
CLOUD_RUN_500_RCA=CLOSED
RCA_CLASSIFICATION=CONTAINER_SCOPED_SYNTHETIC_FIXTURE_RUN_ID_REPLAY
RUNNER_SEMANTICS_CHANGED=NO
```

## Structured safe observability

The judge endpoint now emits one JSON record per request with only:
`request_id`, `scenario`, `auth_mode`, `workflow_status`, `ux_state`,
`http_status`, `latency_ms`, `external_effects`, `revision`, `gemini_mode`,
`error_code`, `audience_configured`, and `token_logged`.

```text
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
STRUCTURED_JUDGE_LOGGING=PASS
```

## Controlled remote operation status

The existing controlled human identity was reauthorized with the required
Drive and Apps Script project scopes. The controlled competition Script project
was identified by its MG Guide manifest (without recording its identifier),
then hydrated with the five authorized adapter files. A post-write content
comparison confirmed repository parity and the stable Devpost logo URL. The
legacy Marketplace project was not read or modified.

```text
REMOTE_APPS_SCRIPT_ACCESS=PASS
REMOTE_MANIFEST_REPO_PARITY=PASS
REMOTE_CARDS_REPO_PARITY=PASS
REMOTE_CONFIG_REPO_PARITY=PASS
REMOTE_SOURCE_HYDRATION=PASS
REMOTE_LOGO_URL_VERIFIED=PASS
TEST_DEPLOYMENT_REINSTALL=NOT_PERFORMED
GMAIL_BRANDED_HOST_ACCEPTANCE=NOT_PERFORMED
CALENDAR_BRANDED_HOST_ACCEPTANCE=NOT_PERFORMED
POST_FIX_REPEAT_SUCCESS=PASS
POST_FIX_REPEAT_AMBIGUOUS=PASS
POST_FIX_5XX_COUNT=0
```

No raw token, Authorization header, email, subject claim, audience, complete
JWT payload, Script ID, deployment ID, OAuth client ID, or endpoint value was
captured in this artifact.

## Evaluator invocation recovery and Apps Script OIDC acceptance

`run.services.get PERMISSION_DENIED` for the controlled evaluator is not an
invocation failure. The evaluator remains the existing Workspace user principal
with only `roles/run.invoker`. No Cloud Run Viewer grant, invoker expansion,
public invoker binding, service-account key, custom-audience change, or auth
validation weakening was performed.

Local `gcloud auth print-identity-token ... --audiences=<client-id>` fails for
this user account because gcloud restricts `--audiences` to service accounts.
That is a local token-minting limitation, not a contract requirement to replace
the Workspace identity-token path with a service account.

Cloud Run IAM crossing for the existing evaluator principal was verified with a
user identity token against the private service: unauthenticated health checks
return 403, while the evaluator-authenticated health check returns application
200. Application OIDC acceptance uses the existing competition Apps Script
project contract (`ScriptApp.getIdentityToken()` via `Auth.gs`, then
`MeetingFollowUp.gs` POST to the judge demo endpoint). A temporary operator
helper invoked that same auth and fetch path and was removed afterward; remote
source was restored to the five authorized adapter files only.

```text
EVALUATOR_PRINCIPAL=user:buildweek-evaluator@themiliare-group.com
EVALUATOR_ROLE=roles/run.invoker
EVALUATOR_GCLOUD_AUTH=PASS
EVALUATOR_CLOUD_RUN_IAM_CROSSING=PASS
EVALUATOR_IAM_EXPANSION=NO
NEW_SERVICE_ACCOUNT_CREATED=NO
SERVICE_ACCOUNT_KEYS_CREATED=NO
CUSTOM_AUDIENCE_MODIFIED=NO
APPLICATION_AUTH_VALIDATION_MODIFIED=NO
HOSTED_DOMAIN_VALIDATION_WEAKENED=NO
PUBLIC_INVOKER_BINDINGS=0
APPS_SCRIPT_IDENTITY_TOKEN_ACQUISITION=PASS
APPS_SCRIPT_TO_CLOUD_RUN_AUTH=PASS
APPLICATION_OIDC_VALIDATION=PASS
WORKSPACE_HOSTED_DOMAIN_VALIDATION=PASS
AUTH_ERROR_COUNT=0
```

Governed SUCCESS / AMBIGUOUS_CONTACT reliability soak through the Apps Script
identity-token path:

```text
RELIABILITY_SOAK_HARNESS=apps_script_identity_token_reliability_soak_v1
RELIABILITY_SOAK_TOTAL_REQUESTS=20
RELIABILITY_SOAK_HTTP_200=20
RELIABILITY_SOAK_HTTP_401=0
RELIABILITY_SOAK_HTTP_403=0
RELIABILITY_SOAK_HTTP_5XX=0
SUCCESS_REQUESTS=10
SUCCESS_HTTP_200=10
SUCCESS_WORKFLOW_STATUS=completed
SUCCESS_EXTERNAL_EFFECTS=0
AMBIGUOUS_CONTACT_REQUESTS=10
AMBIGUOUS_CONTACT_HTTP_200=10
AMBIGUOUS_CONTACT_WORKFLOW_STATUS=blocked
AMBIGUOUS_CONTACT_EXTERNAL_EFFECTS=0
TEMP_OPERATOR_HELPER_REMOVED=YES
REMOTE_SOURCE_RESTORED_TO_FIVE_ADAPTER_FILES=YES
TOKEN_VALUES_CAPTURED=0
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
```

## Runtime publication

The exact PR source was built by the governed dedicated build identity with
Cloud Logging-only output. Its staged source bucket grants only the conditional
bucket-scoped `roles/storage.objectViewer` B3 binding to that identity; the
default Compute service account was not expanded. The resulting immutable image
was deployed to the existing dedicated add-on judge service, which now uses the
dedicated runtime identity with a maximum of one instance. Its existing custom
audience and non-public invoker boundary were preserved.

```text
CLOUD_BUILD_IDENTITY_RECONCILED=PASS
DEFAULT_COMPUTE_SA_PERMISSION_EXPANSION=NO
B3_SOURCE_BUCKET_REQUIRED=YES
B3_BUCKET_SCOPED=YES
BROAD_STORAGE_ROLE_GRANTED=NO
CLOUD_BUILD_IMAGE_PUBLICATION=PASS
CLOUD_RUN_FINAL_REVISION_DEPLOYED=YES
CLOUD_RUN_FINAL_RUNTIME_IDENTITY=DEDICATED
CLOUD_RUN_FINAL_MAX_INSTANCES=1
CUSTOM_AUDIENCE_PRESERVED=YES
PUBLIC_INVOKER_BINDINGS=0
```
