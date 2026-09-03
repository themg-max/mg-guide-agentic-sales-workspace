# Judge Testing — MG Guide | Agent-Native Follow-Up

```text
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
BACKEND_URL=https://mg-guide-webmcp-831270426395.us-east4.run.app
EXPECTED_WEBMCP_TOOL_COUNT=3
LOGIN_REQUIRED=NO
DATA_CLASS=SYNTHETIC_ONLY
```

The fastest way to evaluate the project is through the live product in a
WebMCP-capable browser. No production credentials or customer data are needed.

## Supported judge browsers

Use either:

1. **ChatGPT's in-app browser**, which supports WebMCP; or
2. **Google Chrome 149+** with
   `chrome://flags/#enable-webmcp-testing` enabled, then restart Chrome.

These instructions match the current WebMCP Challenge rules and submission
guidance.

---

## 1. Open the live product

Navigate to:

```text
https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

You should see the MG Guide follow-up workspace, the human-control trust
boundary, and the ACTION / STATE / ARTIFACT capability presentation.

---

## 2. Verify exactly three WebMCP tools

The page registers exactly three browser-native tools through
`document.modelContext.registerTool`:

1. `process_meeting_follow_up` — **ACTION**
2. `get_current_follow_up_state` — **STATE**
3. `get_follow_up_draft` — **ARTIFACT**

No fourth tool is part of the competition surface.

A technical judge can inspect the browser's native WebMCP tool list. A simpler
judge path is to ask the browser agent to use the site's tools directly.

Suggested prompt:

> Use the WebMCP tools exposed by this page. First process the SUCCESS meeting,
> then read the current follow-up state and the follow-up draft.

---

## 3. SUCCESS — process, inspect state, inspect draft

The agent should invoke:

```text
process_meeting_follow_up({"scenario":"SUCCESS"})
```

Expected visible result:

```text
ux_state=COMPLETED
workflow_status=completed
relationship_status=matched
follow_up_draft_status=READY
requires_human_send=true
```

Then the agent should use:

```text
get_current_follow_up_state
get_follow_up_draft
```

Expected behavior:

- the state tool reads the same current workflow state shown on the page;
- the draft tool returns the deterministic follow-up draft already visible on
  the page;
- neither read tool reruns the workflow or makes a server mutation;
- the draft remains marked `requires_human_send=true`.

The important collaboration boundary is: **the agent can prepare the work; a
person must still review and send anything customer-facing.**

---

## 4. AMBIGUOUS_CONTACT — verify fail-closed behavior

Suggested prompt:

> Now use the site's WebMCP tools to process AMBIGUOUS_CONTACT. Tell me the
> current follow-up state and whether a follow-up draft is available.

Expected result:

```text
ux_state=NEEDS_REVIEW
workflow_status=blocked
relationship_status=ambiguous
follow_up_draft_status=NOT_AVAILABLE
reason=RELATIONSHIP_REVIEW_REQUIRED
```

`get_follow_up_draft` should return `NOT_AVAILABLE` rather than inventing or
preparing a customer-facing message.

This is the intended safe stop: when relationship identity is uncertain, MG
Guide does not guess.

---

## 5. Verify zero external effects

The WebMCP competition path is synthetic-only.

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

The bounded backend accepts only:

```json
{"scenario":"SUCCESS"}
```

or:

```json
{"scenario":"AMBIGUOUS_CONTACT"}
```

Unexpected or authority-bearing fields such as `live`, `crm_write`,
`send_email`, credentials, raw transcript, contact IDs, or location IDs are
rejected.

Optional boundary check:

```bash
BACKEND=https://mg-guide-webmcp-831270426395.us-east4.run.app
curl -i -X POST "$BACKEND/webmcp/meeting-follow-up" \
  -H 'Content-Type: application/json' \
  -d '{"scenario":"SUCCESS","live":true}'
```

Expected: HTTP 400 with an authority-field rejection.

---

## 6. Source inspection

The public implementation is intentionally easy to find:

```bash
grep -n "document.modelContext.registerTool" webmcp/static/app.js
grep -n "currentWebMCPState" webmcp/static/app.js
grep -n "MG_GUIDE_WEBMCP_API_BASE" webmcp/static/app.js
```

Key paths:

- `webmcp/static/app.js` — all three WebMCP registrations and browser state
- `src/mg_guide/webmcp/` — bounded stateless backend adapter
- `tests/webmcp/` — WebMCP-specific tests
- `competition/webmcp/COMPETITION_DELTA.md` — pre-existing vs. challenge work

---

## 7. Local setup (optional)

```bash
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
cd mg-guide-agentic-sales-workspace
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m mg_guide.webmcp.server
# Open http://localhost:8080/
```

No credentials, environment variables, CRM service, or customer data are
required for local same-origin testing.

Run the focused test suite with:

```bash
PYTHONPATH=src python -m pytest tests/webmcp -q
```

---

## What the demo is proving

MG Guide is not demonstrating an autonomous outbound-sales bot. It is proving
a narrower and more useful WebMCP pattern:

```text
ACTION → STATE → ARTIFACT → HUMAN CONTROL
```

The browser agent can invoke structured capabilities and inspect the result on
the same page as the human. The person retains final judgment and send
authority.
