# Judge Testing — MG Guide WebMCP Challenge Adapter

```text
LIVE_URL=<filled in after deployment — see SUBMISSION_CHECKLIST.md>
LOCAL_SETUP_TIME=~5 minutes
```

## Quick local setup

```bash
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace
cd mg-guide-agentic-sales-workspace
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m mg_guide.webmcp.server
# open http://localhost:8080/
```

No credentials, no environment variables, and no external services are
required. The server is entirely self-contained and uses only synthetic
fixture data already committed to this repository.

## What you should see (human path)

1. Open the page. You should see:
   - a WebMCP status line (supported or unsupported, based on your browser)
   - a "Run SUCCESS demo" and "Run AMBIGUOUS_CONTACT demo" button
   - seven sections: Meeting, MG Guide processing state, Meeting Context,
     Relationship Context, Follow-Up Planning, Follow-Up Draft, Trust/action
     boundary
2. Click **Run SUCCESS demo**. Processing state becomes `COMPLETED`, Meeting
   Context/Relationship Context/Follow-Up Planning populate, and Follow-Up
   Draft becomes ready.
3. Click **Run AMBIGUOUS_CONTACT demo**. Processing state becomes
   `NEEDS_REVIEW`, and Follow-Up Draft shows `NOT_AVAILABLE —
   RELATIONSHIP_REVIEW_REQUIRED`.

## What you should see (agent path)

Use a WebMCP-aware browser or agent client (Chrome with WebMCP testing
enabled per current [WebMCP developer
documentation](https://developer.chrome.com/), or a WebMCP-capable in-app
browser). On page load, the agent should discover three tools:

- `process_meeting_follow_up`
- `get_current_follow_up_state`
- `get_follow_up_draft`

Invoke, in order:

```json
process_meeting_follow_up({"scenario": "SUCCESS"})
get_current_follow_up_state({})
get_follow_up_draft({})
```

Expect the page to update visibly after the first call, and the two read
tools to return the state you already see on screen. Then invoke:

```json
process_meeting_follow_up({"scenario": "AMBIGUOUS_CONTACT"})
get_follow_up_draft({})
```

Expect the page to move to `NEEDS_REVIEW` and the draft tool to return
`{"status": "NOT_AVAILABLE", "reason": "RELATIONSHIP_REVIEW_REQUIRED"}`.

## Verifying the boundary yourself

```bash
# Rejected authority field:
curl -s -X POST http://localhost:8080/webmcp/meeting-follow-up \
  -H 'Content-Type: application/json' \
  -d '{"scenario":"SUCCESS","live":true}'
# -> HTTP 400 {"error":"authority_field_rejected","fields":["live"]}

# Rejected unknown scenario:
curl -s -X POST http://localhost:8080/webmcp/meeting-follow-up \
  -H 'Content-Type: application/json' \
  -d '{"scenario":"NOT_REAL"}'
# -> HTTP 400 {"error":"invalid_scenario", ...}
```

## Running the automated test suite

```bash
PYTHONPATH=src python -m pytest tests/webmcp -v
```

All 26 tests should pass. This covers HTTP-layer behavior (WEBMCP-05..09,
11..15, 16..19) and static-source checks on the tool registration contract
(WEBMCP-01..04, 10, 20). See
[`proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-end-to-end-acceptance-001.md)
for full test-by-test evidence, including real-browser tool-invocation
proof.

## Source verification

Confirm the actual WebMCP registration call is present in the shipped
source:

```bash
grep -n "document.modelContext.registerTool" webmcp/static/app.js
```
