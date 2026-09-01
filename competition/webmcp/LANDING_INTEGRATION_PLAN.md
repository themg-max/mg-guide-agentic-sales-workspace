# A.I. Rolodex Landing Integration Plan (HOST_INTEGRATION_ONLY)

```text
STATUS=EXECUTED_AND_PROVEN
PUBLIC_CANONICAL_REPO=themg-max/mg-guide-agentic-sales-workspace
PRIVATE_HOST_REPO=themg-max/A.I-Rolodex---Context
PRODUCT_PATH=/mg-guide/
BACKEND_SERVICE=mg-guide-webmcp
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
PRODUCTION_ACCEPTANCE_PROOF=proof/webmcp/mg-guide-webmcp-production-acceptance-001.md
```

## Constraints

- Private landing repo is **host integration only**
- Do not copy MG domain logic, CRM code, credentials, R5, private governance
- Public repo remains WebMCP canonical source
- Record exact public SHA + file hashes of hosted canonical static files
- `config.js` is the one host-specific deployment configuration surface; it
  may set only the public backend base URL and must contain no credentials

## Landing surface facts (current)

- Service: `ai-rolodex-landing` (us-east4)
- Image: nginx serving Vite SPA from `/usr/share/nginx/html`
- nginx: SPA `try_files $uri $uri/ /index.html` — static files under a real
  path (e.g. `/mg-guide/index.html`) work if present on disk before SPA fallback
- No `landing-page/public/` directory today — create
  `landing-page/public/mg-guide/` so Vite copies assets into `dist/mg-guide/`
- Runtime SA today: default compute SA (over-privileged for secrets); landing
  itself mounts **no** secrets (env empty) — good for static host
- SPA currently injects `process.env.GEMINI_API_KEY` at build time via
  vite.config — **do not** extend that pattern for WebMCP; API base is a
  public URL only
- Public WebMCP `index.html` uses relative `./style.css`, `./config.js`, and
  `./app.js`, so it is safe to host below `/mg-guide/`

## Integration steps (separate private-repo branch, after public PR merge)

1. Branch from origin/main in A.I-Rolodex---Context (never main)
2. Create `landing-page/public/mg-guide/` with exact copies of public
   `webmcp/static/{index.html,style.css,app.js}` at the merged public SHA
3. Create host-specific `landing-page/public/mg-guide/config.js` from the
   public `webmcp/static/config.js` template, changing only
   `window.MG_GUIDE_WEBMCP_API_BASE` to the approved public backend URL
4. Record hashes for exact-copy files and record the host-specific config
   value separately in the landing proof
5. Optionally add one nav CTA on the React landing: "Try MG Guide with WebMCP"
   linking to `/mg-guide/`
6. Adjust nginx only if required after candidate validation; prefer an explicit
   `location /mg-guide/` only if current SPA fallback does not serve the real
   static directory correctly
7. Build candidate revision of `ai-rolodex-landing` with **no traffic**
8. Verify `/`, `/mg-guide/`, terms/privacy, static assets, and backend CORS
9. Collect actual WebMCP browser discovery + agent invocation proof on the
   live candidate URL
10. Promote traffic only after acceptance

## Backend deploy gate (separate)

```text
STOP=DEDICATED_WEBMCP_RUNTIME_IDENTITY_AUTHORIZATION_REQUIRED
```

Default compute SA has `roles/secretmanager.secretAccessor` project-wide and
broad data/admin roles. Public ingress on that identity is **not** acceptable
for `mg-guide-webmcp` without a dedicated minimal runtime identity with:

- HIGHLEVEL_ACCESS=NO
- SECRET_ACCESS=NO
- CRM_MUTATION_ACCESS=NO
- IAM_MUTATION_ACCESS=NO
- no secret/env bindings
