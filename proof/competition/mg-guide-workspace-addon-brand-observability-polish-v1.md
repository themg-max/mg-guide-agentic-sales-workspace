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

This session's controlled credential received HTTP 403 when attempting the
read-only Drive metadata lookup required to obtain the private competition
Script project for `projects.getContent`. No Script project, deployment,
Marketplace add-on, or Workspace account was modified.

```text
REMOTE_APPS_SCRIPT_ACCESS=DENIED
REMOTE_MANIFEST_REPO_PARITY=NOT_VERIFIED
REMOTE_CARDS_REPO_PARITY=NOT_VERIFIED
REMOTE_SOURCE_HYDRATION=NOT_PERFORMED
TEST_DEPLOYMENT_REINSTALL=NOT_PERFORMED
GMAIL_BRANDED_HOST_ACCEPTANCE=NOT_PERFORMED
CALENDAR_BRANDED_HOST_ACCEPTANCE=NOT_PERFORMED
POST_FIX_REPEAT_SUCCESS=NOT_PERFORMED
POST_FIX_REPEAT_AMBIGUOUS=NOT_PERFORMED
POST_FIX_5XX_COUNT=NOT_VERIFIED
```

No raw token, Authorization header, email, subject claim, audience, complete
JWT payload, Script ID, deployment ID, OAuth client ID, or endpoint value was
captured in this artifact.
