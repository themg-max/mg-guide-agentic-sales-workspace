# WebMCP Challenge — Submission Checklist

```text
STATUS=IN_PROGRESS
LAST_UPDATED=2026-09-01
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

## Required assets

- [x] `WEB_APP_POWERED_BY_WEBMCP` — `webmcp/static/app.js` registers 3 tools
- [ ] `WORKING_LIVE_URL` — pending landing `/mg-guide/` + backend deploy
- [x] `PUBLIC_CODE_REPO` — `https://github.com/themg-max/mg-guide-agentic-sales-workspace`
- [x] `OPEN_SOURCE_LICENSE` — Apache-2.0
- [x] `WEBMCP_IMPLEMENTATION_VISIBLE_IN_REPO`
- [ ] `DEMO_VIDEO_UNDER_3_MINUTES` — pending
- [ ] `DEMO_VIDEO_AUDIO` — pending
- [ ] `YOUTUBE_PUBLIC_VIDEO` — pending
- [x] `TESTING_INSTRUCTIONS` — `competition/webmcp/JUDGE_TESTING.md`

## Architecture gates

```text
SEPARATE_WEB_SURFACE_REQUIRED=NO
EXISTING_AI_ROLODEX_SURFACE_REUSED=YES
SEPARATE_WEBMCP_BACKEND_BOUNDARY=YES
SERVER_SESSION_STATE_REQUIRED=NO
WEBMCP_BROWSER_STATE=YES
PUBLIC_REPO_OWNS_SOURCE=YES
PRIVATE_REPO_BUILD_DEPENDENCY=NO
PRIVATE_REPO_RUNTIME_DEPENDENCY=NO
SECRET_DEPENDENCY=NO
CRM_CREDENTIAL_DEPENDENCY=NO
```

## Validation completed (source)

- [x] Stateless backend (no `_last_state`)
- [x] Browser `currentWebMCPState`
- [x] Configurable `MG_GUIDE_WEBMCP_API_BASE`
- [x] CORS allowlist (no `*`)
- [x] Focused WebMCP tests
- [x] Corrected acceptance claims: mocked ≠ actual WebMCP browser proof

## Remaining

1. Independent review + merge of PR 432 (after this correction commit)
2. Backend deploy preflight → dedicated runtime identity if needed
3. Landing integration branch: host `webmcp/static` at `/mg-guide/`
4. Actual WebMCP browser discovery + agent invocation on live URL
5. Demo video + Devpost form
