# WebMCP Challenge — Submission Checklist

```text
STATUS=IN_PROGRESS
LAST_UPDATED=2026-09-01
```

## Required assets

- [x] `WEB_APP_POWERED_BY_WEBMCP` — `webmcp/static/app.js` registers 3 tools
      via `document.modelContext.registerTool`
- [ ] `WORKING_LIVE_URL` — pending Cloud Run deployment (see below)
- [x] `PUBLIC_CODE_REPO` — `https://github.com/themg-max/mg-guide-agentic-sales-workspace`
- [x] `OPEN_SOURCE_LICENSE` — Apache-2.0 (`LICENSE`, pre-existing, verified intact)
- [x] `WEBMCP_IMPLEMENTATION_VISIBLE_IN_REPO` — `src/mg_guide/webmcp/`,
      `webmcp/static/app.js`
- [ ] `DEMO_VIDEO_UNDER_3_MINUTES` — pending recording
- [ ] `DEMO_VIDEO_AUDIO` — pending recording
- [ ] `YOUTUBE_PUBLIC_VIDEO` — pending upload
- [x] `TESTING_INSTRUCTIONS` — `competition/webmcp/JUDGE_TESTING.md`

## Deployment gate status

```text
PUBLIC_REPO_OWNS_SOURCE=YES
PRIVATE_REPO_BUILD_DEPENDENCY=NO
PRIVATE_REPO_RUNTIME_DEPENDENCY=NO
SECRET_DEPENDENCY=NO
CRM_CREDENTIAL_DEPENDENCY=NO
```

Selected topology: **Option B** — dedicated competition-only Cloud Run
service (`mg-guide-webmcp-competition`) built entirely from
`deployment/webmcp/Dockerfile` in this public repository, deployed under the
existing project's default Cloud Run service identity used for other public
judge surfaces. No IAM changes are made to enable this deployment.

## Local/automated validation completed

- [x] `PYTHONPATH=src python -m pytest tests/webmcp -v` — 26/26 passed
- [x] `PYTHONPATH=src python -m pytest tests/ -q` — full existing suite green
      (no regression to judge_surface, orchestration, or agents)
- [x] End-to-end browser acceptance (Playwright-driven Chromium): SUCCESS
      flow, AMBIGUOUS_CONTACT fail-closed flow, and direct tool-`execute()`
      invocation against a mocked `document.modelContext.registerTool`, all
      updating visible page state correctly
- [x] `git diff --check` — clean (see below before commit)
- [x] Boundary curl checks — authority-field rejection, invalid-scenario
      rejection confirmed

## Remaining before feature freeze (2026-09-03T10:00:00-04:00)

1. Deploy `mg-guide-webmcp-competition` to Cloud Run from this repo.
2. Confirm public HTTPS URL responds and record it here and in README.
3. Record demo video (<3 min, with audio), upload to YouTube (public).
4. Open implementation PR; obtain CI pass and human merge.
5. Optional: add "Try MG Guide with WebMCP" link on the A.I Rolodex landing
   page (skip if not completable safely in one bounded pass).
6. Complete the Devpost submission form.
