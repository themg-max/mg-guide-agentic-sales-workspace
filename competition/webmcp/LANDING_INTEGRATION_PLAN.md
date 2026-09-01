# A.I. Rolodex Landing Integration Plan (HOST_INTEGRATION_ONLY)

```text
STATUS=EXECUTED_AND_PROVEN
PUBLIC_CANONICAL_REPO=themg-max/mg-guide-agentic-sales-workspace
PRIVATE_HOST_REPO=themg-max/A.I-Rolodex---Context
PRODUCT_PATH=/mg-guide/
BACKEND_SERVICE=mg-guide-webmcp
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
NATIVE_WEBMCP_DISCOVERY=PASS
NATIVE_WEBMCP_INVOCATION=PASS
PRODUCTION_HOST_INTEGRATION=PASS
PRODUCTION_ACCEPTANCE_PROOF=proof/webmcp/mg-guide-webmcp-production-acceptance-001.md
```

## 1. Current status / final observed outcome

Production host integration is **complete**. The public WebMCP static assets
(`index.html`, `style.css`, `app.js`, `config.js`) are live at
`https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`, served
alongside the dedicated bounded backend `mg-guide-webmcp`. Native WebMCP tool
discovery (exactly 3 tools) and agent invocation of the SUCCESS and
AMBIGUOUS_CONTACT fail-closed flows have both been verified against the live
production URL using a real WebMCP-capable client — see
[`proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md).

## 2. Preserved constraints

These constraints governed the integration and remain the permanent boundary
for any future change to this host surface:

- Private landing repo is **host integration only**
- Do not copy MG domain logic, CRM code, credentials, R5, private governance
- Public repo remains WebMCP canonical source
- Exact public SHA + file hashes of hosted canonical static files were
  recorded at integration time
- `config.js` is the one host-specific deployment configuration surface; it
  may set only the public backend base URL and must contain no credentials

## 3. Historical pre-execution observations (recorded before integration)

These facts described the landing surface before the WebMCP host integration
was executed. They are preserved for engineering history only and do not
describe the current state:

- Service: `ai-rolodex-landing` (us-east4)
- Image: nginx serving Vite SPA from `/usr/share/nginx/html`
- nginx: SPA `try_files $uri $uri/ /index.html` — static files under a real
  path work if present on disk before SPA fallback
- At the time of planning, no `landing-page/public/` directory existed
  (subsequently created as part of execution)
- Runtime SA at the time: default compute SA (over-privileged for secrets);
  landing itself mounted no secrets (env empty)
- SPA injects `process.env.GEMINI_API_KEY` at build time via vite.config for
  unrelated features — this pattern was deliberately **not** extended to
  WebMCP; the WebMCP API base is a public URL only
- Public WebMCP `index.html` uses relative `./style.css`, `./config.js`, and
  `./app.js`, which made it safe to host below `/mg-guide/`

## 4. Historical execution plan (completed)

The following steps were the original integration plan and have since been
executed in the private host repository under its own separate governance
and proof trail:

1. Branch from `origin/main` in `A.I-Rolodex---Context` (never `main`)
2. Create `landing-page/public/mg-guide/` with exact copies of public
   `webmcp/static/{index.html,style.css,app.js}` at the merged public SHA
3. Create host-specific `landing-page/public/mg-guide/config.js` from the
   public `webmcp/static/config.js` template, changing only
   `window.MG_GUIDE_WEBMCP_API_BASE` to the approved public backend URL
4. Record hashes for exact-copy files and record the host-specific config
   value separately in the landing proof
5. Build and verify a candidate revision of `ai-rolodex-landing`
6. Verify `/`, `/mg-guide/`, terms/privacy, static assets, and backend CORS
7. Collect actual WebMCP browser discovery + agent invocation proof on the
   live candidate URL
8. Promote traffic to the accepted candidate

All steps above are complete. This public repository does not own or track
the private host repository's Cloud Run, IAM, or traffic operations — those
remain governed separately in `themg-max/A.I-Rolodex---Context`.

## 5. Final verified outcome

```text
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
NATIVE_WEBMCP_DISCOVERY=PASS (exactly 3 tools)
NATIVE_WEBMCP_INVOCATION=PASS
SUCCESS_FLOW=PASS
AMBIGUOUS_CONTACT_FAIL_CLOSED=PASS
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

Full evidence: [`proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md).

## 6. Remaining scope

```text
REMAINING_HOST_INTEGRATION_SCOPE=NONE
```

Host integration is complete. Remaining work across the competition submission
is limited to submission operations (demo video, YouTube upload, Devpost form)
tracked in [`competition/webmcp/SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md).

### HISTORICAL_PRE_EXECUTION_GATE (resolved)

```text
GATE_ID=DEDICATED_WEBMCP_RUNTIME_IDENTITY_AUTHORIZATION
STATUS=HISTORICAL_PRE_EXECUTION_GATE
RESOLUTION=RESOLVED_BEFORE_BACKEND_DEPLOYMENT
```

Before backend deployment, this gate required that `mg-guide-webmcp` not run
under the default compute service account (which held
`roles/secretmanager.secretAccessor` project-wide and broad data/admin roles).
A dedicated minimal runtime identity was authorized and used for deployment
with:

- HIGHLEVEL_ACCESS=NO
- SECRET_ACCESS=NO
- CRM_MUTATION_ACCESS=NO
- IAM_MUTATION_ACCESS=NO
- no secret/env bindings

This gate is resolved and is not a current blocker.
