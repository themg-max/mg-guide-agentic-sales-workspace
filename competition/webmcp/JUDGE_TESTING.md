# Judge Testing — MG Guide WebMCP Challenge Adapter

```text
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
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

1. Open the A.I. Rolodex product page: `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`
2. Frontend registers WebMCP tools via `document.modelContext.registerTool` and calls the bounded backend via `window.MG_GUIDE_WEBMCP_API_BASE`.
3. Backend is public, synthetic-only, **stateless** at `https://mg-guide-webmcp-831270426395.us-east4.run.app`.

## Judge testing journey (live product URL)

### 1. Open the live page
Navigate to: `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`

### 2. Verify native WebMCP tool discovery (3 tools)
In a WebMCP-capable browser (Google Chrome with `--enable-features=WebMCP,ModelContextProtocol` or a supported WebMCP agent client), inspect `document.modelContext.getTools()`. You will see exactly three registered tools:
1. `process_meeting_follow_up` — runs `meeting_follow_up_v1` on synthetic scenario
2. `get_current_follow_up_state` — client-only reader for visible workflow state
3. `get_follow_up_draft` — client-only reader for generated follow-up draft

### 3. Run SUCCESS demo
- **Human button**: Click **Run SUCCESS demo**
- **Agent invocation**: Execute `process_meeting_follow_up` with `{"scenario": "SUCCESS"}`
- **Expected result**:
  - `ux_state = COMPLETED`
  - `workflow_status = completed`
  - `follow_up_draft_status = READY`
  - Visible sections populate with meeting summary, matched relationship context, salesperson next step, and follow-up draft preview.

### 4. Run AMBIGUOUS_CONTACT demo
- **Human button**: Click **Run AMBIGUOUS_CONTACT demo**
- **Agent invocation**: Execute `process_meeting_follow_up` with `{"scenario": "AMBIGUOUS_CONTACT"}`
- **Expected result**:
  - `ux_state = NEEDS_REVIEW`
  - `workflow_status = blocked`
  - `follow_up_draft_status = NOT_AVAILABLE`
  - Draft notice: `NOT_AVAILABLE — RELATIONSHIP_REVIEW_REQUIRED`
  - Fail-closed: no draft is produced and no CRM action is allowed.

### 5. Verify the human-send boundary
- Every follow-up draft is tagged `requires_human_send: true`.
- The agent can process meeting context and inspect the draft, but the system strictly prohibits autonomous sending. A human must review and send any customer-facing email.

### 6. Verify zero live CRM / email effects
- The demo runs exclusively on fixed synthetic fixtures.
- `HIGHLEVEL_CALLS = 0`
- `CRM_MUTATIONS = 0`
- `EMAILS_SENT = 0`
- `REAL_CUSTOMER_DATA = 0`
- Any attempt to pass authority fields (`live`, `crm_write`, `send_email`, `credentials`) is immediately rejected with HTTP 400.

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
