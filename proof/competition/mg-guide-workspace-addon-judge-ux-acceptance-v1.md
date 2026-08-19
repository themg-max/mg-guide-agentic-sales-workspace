# MG Guide Workspace Add-on - Judge UX Acceptance v1

```text
ARTIFACT=proof/competition/mg-guide-workspace-addon-judge-ux-acceptance-v1.md
WORKFLOW=meeting_follow_up_v1
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
REAL_CUSTOMER_DATA=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

## Scope and invariants

The Workspace add-on is a thin CardService presentation and routing adapter.
It does not alter policy, runner semantics, fixture data, CRM behavior, or the
OIDC trust model.

```text
APPS_SCRIPT_RENDERS_AND_ROUTES_ONLY=YES
POLICY_ENGINE_CHANGED=NO
FIXTURE_BYTES_CHANGED=NO
RUNNER_SEMANTICS_CHANGED=NO
CRM_MUTATIONS_PERFORMED=NO
```

## Acceptance status

```text
OIDC_BACKEND_ACCEPTANCE=PASS
HOST_SHELL_ACCEPTANCE=PASS
BRANDED_HOST_UX_ACCEPTANCE=IN_PROGRESS
VIDEO_AUTHORIZATION=POSTPONED
```

The previous host-shell installation established the Gmail and Calendar add-on
shell. It is not evidence that the final branded card template has been
hydrated or manually accepted. Final acceptance requires a controlled
installation of the updated source, fresh Gmail and Calendar verification, and
post-fix repeat runs.

## Deterministic scenario contract

```text
SUCCESS_UX_STATE=COMPLETED
SUCCESS_EXTERNAL_EFFECTS=0
AMBIGUOUS_UX_STATE=NEEDS_REVIEW
AMBIGUOUS_NOTE_WRITE=not_attempted
AMBIGUOUS_STAGE_WRITE=not_attempted
AMBIGUOUS_EXTERNAL_EFFECTS=0
POLICY_RESULT_VISIBLE=YES
SALESPERSON_NEXT_STEP_VISIBLE=YES
AUDIT_STATUS_VISIBLE=YES
LIVE_CRM_EXECUTION=NOT_PERFORMED
```

```text
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=NO
TOKEN_VALUES_CAPTURED=0
```

See
[`mg-guide-workspace-addon-brand-observability-polish-v1.md`](mg-guide-workspace-addon-brand-observability-polish-v1.md)
for final-source and observability status.
