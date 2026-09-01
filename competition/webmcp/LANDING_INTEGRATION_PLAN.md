# A.I. Rolodex Landing Integration Plan (HOST_INTEGRATION_ONLY)

```text
STATUS=PLAN_READY_NOT_EXECUTED
PUBLIC_CANONICAL_REPO=themg-max/mg-guide-agentic-sales-workspace
PRIVATE_HOST_REPO=themg-max/A.I-Rolodex---Context
PRODUCT_PATH=/mg-guide/
BACKEND_SERVICE=mg-guide-webmcp
```

## Constraints

- Private landing repo is **host integration only**
- Do not copy MG domain logic, CRM code, credentials, R5, private governance
- Public repo remains WebMCP canonical source
- Record exact public SHA + file hashes of hosted static copy

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

## Integration steps (separate private-repo branch, after public PR merge)

1. Branch from origin/main in A.I-Rolodex---Context (never main)
2. Create `landing-page/public/mg-guide/` with exact copies of public
   `webmcp/static/{index.html,style.css,app.js}` at known public SHA
3. Add `landing-page/public/mg-guide/config.js` (or inline script in index.html)
   setting `window.MG_GUIDE_WEBMCP_API_BASE` to the approved backend URL
4. Optionally add one nav CTA on the React landing: "Try MG Guide with WebMCP"
   linking to `/mg-guide/`
5. Adjust nginx if needed so `/mg-guide/` is not swallowed incorrectly
   (prefer explicit `location /mg-guide/` with `try_files`)
6. Build candidate revision of `ai-rolodex-landing` with **no traffic**
7. Verify `/`, `/mg-guide/`, terms/privacy, static assets
8. Actual WebMCP browser proof on live candidate URL
9. Promote traffic only after acceptance

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
