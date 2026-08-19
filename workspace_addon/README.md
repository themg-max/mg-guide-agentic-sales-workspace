# MG Guide — Workspace Add-on (competition adapter)

```text
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
ROLE=THIN_PRESENTATION_AND_ROUTING_ADAPTER
WORKFLOW=meeting_follow_up_v1
```

## Architecture

```text
CardService UI
  -> POST {JUDGE_BACKEND_BASE_URL}/demo/meeting-follow-up
  -> existing WorkflowRunner + packet + policy + demo_stages / ux_experience
  -> CardService render of returned fields only
```

Apps Script **must not** implement meeting extraction, relationship resolution,
follow-up planning, policy evaluation, audit semantics, workflow state machines,
or CRM mutation logic.

## Branding

- Title: **MG Guide**
- Attribution: **Powered by AI Rolodex**

## Judge scenarios

| Button | Selector | Expected UX_STATE |
| --- | --- | --- |
| Run SUCCESS | `SUCCESS` | `COMPLETED` |
| Run AMBIGUOUS_CONTACT | `AMBIGUOUS_CONTACT` | `NEEDS_REVIEW` |
| Run STAGE_CHANGE_DENIED (optional) | `STAGE_CHANGE_DENIED` | `NEEDS_REVIEW` |

## Configuration (Script Properties)

| Property | Purpose |
| --- | --- |
| `JUDGE_BACKEND_BASE_URL` | Base URL of the judge surface (no trailing slash). **Required** before live calls. |
| `JUDGE_ADDON_AUTH_MODE` | Optional mirror of backend mode (`off` / `identity_token`). Default: send identity token when available. |

Do **not** commit private Script IDs, deployment IDs, OAuth client secrets, or
production customer endpoints into this public repository.

`urlFetchWhitelist` in `appsscript.json` is intentionally empty in the public
tree. Operators set the bound backend URL and whitelist in the private deploy
project only.

## Auth

See [`docs/architecture/mg-guide-workspace-addon-auth-contract-v1.md`](../docs/architecture/mg-guide-workspace-addon-auth-contract-v1.md).

```text
TOKEN_SOURCE=ScriptApp.getIdentityToken()
RAW_IDENTITY_TOKEN_LOGGING=FORBIDDEN
```

## Local truth verification (no clasp)

```bash
export MEETING_CONTEXT_GEMINI_MODE=stub PYTHONPATH=src
.venv/bin/python -m pytest -q tests/workspace_addon tests/judge_surface
```

The Python local adapter exercises the same projection contract the Apps Script
cards render.

## Deploy boundary

```text
CLASP_PUSH_IN_THIS_REPO_UNIT=NOT_AUTHORIZED_BY_DEFAULT
MARKETPLACE_MUTATION=NO
OAUTH_SCOPE_EXPANSION_BEYOND_MANIFEST=NO
```
