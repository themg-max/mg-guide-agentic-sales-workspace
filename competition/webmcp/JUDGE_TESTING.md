# Judge Testing — MG Guide WebMCP Challenge Adapter

```text
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=<filled after mg-guide-webmcp deployment>
LOCAL_SETUP_TIME=~5 minutes
```

## Quick local setup (public repo only)

```bash
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace
cd mg-guide-agentic-sales-workspace
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m mg_guide.webmcp.server
# open http://localhost:8080/
```

No credentials, no environment variables, and no external services are
required. Same-origin local mode serves frontend + backend together.

## Production topology

1. Open the A.I. Rolodex product page: `/mg-guide/`
2. Frontend registers WebMCP tools and calls the bounded backend via
   `window.MG_GUIDE_WEBMCP_API_BASE`.
3. Backend is public, synthetic-only, **stateless**.

## What you should see (human path)

1. Open the page. WebMCP status line + SUCCESS / AMBIGUOUS_CONTACT buttons +
   seven sections.
2. **Run SUCCESS demo** → `COMPLETED`, draft READY with recipient/subject/preview.
3. **Run AMBIGUOUS_CONTACT demo** → `NEEDS_REVIEW`, draft
   `NOT_AVAILABLE — RELATIONSHIP_REVIEW_REQUIRED`.

## What you should see (agent path — real WebMCP browser)

Use a WebMCP-aware browser or agent client (Chrome with WebMCP testing
enabled per current official docs, or a WebMCP-capable in-app browser such
as ChatGPT). Discover:

- `process_meeting_follow_up`
- `get_current_follow_up_state`
- `get_follow_up_draft`

Invoke SUCCESS, then state, then draft; then AMBIGUOUS_CONTACT and draft
again. Expect fail-closed `NOT_AVAILABLE` after ambiguous.

**Note:** Automated CI and Playwright harnesses may mock
`document.modelContext` to verify registration/execution contracts. That is
**not** claimed as actual WebMCP browser discovery. Actual discovery proof
is collected on a real WebMCP-capable client after live deployment.

## Verifying the boundary yourself

```bash
curl -s -X POST "$BACKEND/webmcp/meeting-follow-up" \
  -H 'Content-Type: application/json' \
  -d '{"scenario":"SUCCESS","live":true}'
# -> HTTP 400 {"error":"authority_field_rejected","fields":["live"]}
```

## Running the automated test suite

```bash
PYTHONPATH=src python -m pytest tests/webmcp -v
```

## Source verification

```bash
grep -n "document.modelContext.registerTool" webmcp/static/app.js
grep -n "currentWebMCPState" webmcp/static/app.js
grep -n "MG_GUIDE_WEBMCP_API_BASE" webmcp/static/app.js
```
