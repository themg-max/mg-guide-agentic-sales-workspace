# MG Guide | Agentic Sales Workspace

MG Guide turns a meeting transcript into structured relationship context and a
governed follow-up plan so salespeople can move from conversation to action
without rebuilding context manually.

This repository supports two competition submissions from one codebase. The
competition-specific work is documented separately so judges can evaluate the
right delta without confusing it with pre-existing MG Guide capabilities.

## Competition judge routes

| Competition | Start here |
| --- | --- |
| **The WebMCP Challenge — MG Guide \| Agent-Native Follow-Up** | [`competition/webmcp/README.md`](competition/webmcp/README.md) |
| **Google All Things Agentic Hackathon — MG Guide \| Agentic Sales Workspace** | [`JUDGE_START_HERE.md`](JUDGE_START_HERE.md) |

---

# WebMCP Challenge — MG Guide | Agent-Native Follow-Up

**Live demo:** https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/

**Judge guide:** [`competition/webmcp/README.md`](competition/webmcp/README.md)

**Testing steps:** [`competition/webmcp/JUDGE_TESTING.md`](competition/webmcp/JUDGE_TESTING.md)

**Competition delta:** [`competition/webmcp/COMPETITION_DELTA.md`](competition/webmcp/COMPETITION_DELTA.md)

**Core trust boundary:** **Agent can prepare. Only a person can review and send.**

MG Guide existed before the WebMCP Challenge. During the challenge submission
period, we added a browser-native WebMCP layer so the same page a person uses
can expose structured capabilities directly to an AI agent.

The competition surface registers exactly three tools through
`document.modelContext.registerTool`:

| WebMCP tool | Role | Purpose |
| --- | --- | --- |
| `process_meeting_follow_up` | **ACTION** | Runs the bounded synthetic `meeting_follow_up_v1` scenario (`SUCCESS` or `AMBIGUOUS_CONTACT`) |
| `get_current_follow_up_state` | **STATE** | Reads the current browser-held follow-up state without rerunning the workflow |
| `get_follow_up_draft` | **ARTIFACT** | Reads the deterministic draft already prepared on the page |

There is no fourth tool, no autonomous send tool, and no CRM-write tool.

## What judges should see

A WebMCP-capable browser agent can discover the tools and run the complete
human-agent workflow on the live page:

```text
SUCCESS
→ meeting context
→ matched relationship
→ follow-up plan
→ draft READY
→ requires_human_send=true
```

Then the same surface demonstrates the safety boundary:

```text
AMBIGUOUS_CONTACT
→ relationship ambiguous
→ NEEDS_REVIEW
→ draft NOT_AVAILABLE
→ RELATIONSHIP_REVIEW_REQUIRED
→ no external effect
```

The agent can prepare and inspect the work. The person keeps customer-facing
authority.

## Why WebMCP fits this use case

Post-meeting follow-up is a natural human-agent collaboration problem. A
salesperson still needs judgment and relationship awareness, but repetitive
navigation, context reconstruction, and draft preparation can be delegated.

Without WebMCP, an agent would need a separate integration or would have to
infer meaning from DOM structure and UI navigation. WebMCP lets the website
publish a narrow, typed, discoverable tool contract instead. The human and the
agent act on the same visible page state rather than maintaining separate
human and agent interfaces.

That gives MG Guide a stronger interaction model:

- **Discoverable:** the browser agent sees named tools instead of guessing.
- **Bounded:** only approved synthetic scenarios are accepted.
- **Shared:** the same page visibly reflects agent-invoked state.
- **Fail-closed:** ambiguous identity produces review, not action.
- **Human-controlled:** every usable draft requires human review/send.

## WebMCP implementation

The WebMCP layer is additive; it does not replace the core MG Guide architecture.

```text
Human + browser agent
        ↓
A.I. Rolodex / MG Guide web page
        ↓
document.modelContext.registerTool(...)
        ↓
3 WebMCP tools: ACTION / STATE / ARTIFACT
        ↓
bounded stateless mg-guide-webmcp adapter
        ↓
existing meeting_follow_up_v1 workflow
        ↓
Meeting Context → Relationship Context → Follow-Up Planning
        ↓
deterministic safe result shown on the same page
```

Key public surfaces:

| Surface | Path |
| --- | --- |
| Tool registration + browser state | [`webmcp/static/app.js`](webmcp/static/app.js) |
| Human-facing WebMCP page | [`webmcp/static/index.html`](webmcp/static/index.html) |
| Bounded backend adapter | [`src/mg_guide/webmcp/`](src/mg_guide/webmcp/) |
| WebMCP tests | [`tests/webmcp/`](tests/webmcp/) |
| Architecture | [`competition/webmcp/WEBMCP_ARCHITECTURE.md`](competition/webmcp/WEBMCP_ARCHITECTURE.md) |
| New-vs-existing work | [`competition/webmcp/COMPETITION_DELTA.md`](competition/webmcp/COMPETITION_DELTA.md) |
| Judge journey | [`competition/webmcp/JUDGE_TESTING.md`](competition/webmcp/JUDGE_TESTING.md) |
| Demo script | [`competition/webmcp/DEMO_SCRIPT_UNDER_3_MIN.md`](competition/webmcp/DEMO_SCRIPT_UNDER_3_MIN.md) |

## WebMCP safety posture

The WebMCP competition demo runs on synthetic fixture data only.

```text
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EMAILS_SENT=0
REAL_CUSTOMER_DATA=0
```

The competition tool surface does not accept credentials, arbitrary customer
identifiers, a live-mode selector, or an autonomous email/CRM authority field.
Ambiguous relationship identity fails closed.

## What was pre-existing vs. new

**Pre-existing MG Guide:** the core meeting-follow-up workflow, specialized
Meeting Context / Relationship Context / Follow-Up Planning agents,
deterministic policy, Google Workspace integration, and broader Google
Cloud-hosted MG Guide architecture.

**New for The WebMCP Challenge:** the browser-native WebMCP frontend, bounded
stateless adapter, exactly-three-tool registration, WebMCP-specific tests,
challenge deployment packaging, native browser acceptance, presentation work,
and challenge-specific judge/submission documentation.

See [`competition/webmcp/COMPETITION_DELTA.md`](competition/webmcp/COMPETITION_DELTA.md)
for the dated implementation history and exact boundary.

---

# Broader MG Guide product context

The meeting is digital, but much of the work after the meeting remains
fragmented:

- reviewing what was said;
- remembering personal and business context;
- connecting the meeting to the correct relationship;
- deciding the next step;
- preparing future follow-up.

The broader MG Guide architecture addresses that workflow with three
specialized agents and deterministic policy:

```text
Google Workspace meeting
  → transcript
  → MG Guide Orchestrator
  → Meeting Context Agent
  → Relationship Context Agent
  → Follow-Up Planning Agent
  → deterministic policy
  → MG Guide follow-up experience / bounded external-effect boundary
```

| Agent | Role |
| --- | --- |
| **Meeting Context Agent** | Understands what happened. |
| **Relationship Context Agent** | Connects the meeting to the correct relationship context. |
| **Follow-Up Planning Agent** | Turns that context into recommended next steps. |

For the Google All Things Agentic competition-specific judge path and proof,
start at [`JUDGE_START_HERE.md`](JUDGE_START_HERE.md).

---

## Reproducible local setup

The core deterministic suite and WebMCP competition adapter can be inspected
without production credentials.

```bash
# Clone
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
cd mg-guide-agentic-sales-workspace

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Run repository tests
PYTHONPATH=src python3 -m pytest -q

# Run the local WebMCP adapter
PYTHONPATH=src python3 -m mg_guide.webmcp.server
# Then open http://localhost:8080/
```

No production `.env`, CRM credential, or customer data is required for the
WebMCP competition demo.

---

## Repository navigation

```text
README.md
JUDGE_START_HERE.md                 Google competition judge route
competition/webmcp/README.md        WebMCP Challenge judge route
competition/webmcp/                 WebMCP brief, delta, testing, demo, submission docs
webmcp/static/                       Browser-native WebMCP frontend
src/mg_guide/webmcp/                Bounded synthetic WebMCP backend adapter
tests/webmcp/                        WebMCP tests
proof/webmcp/                        Public WebMCP evidence
src/                                 Broader MG Guide runtime source
tests/                               Repository tests
governance/                          Public sanitized governance
```

## Governance and truth boundary

- Private AI Rolodex context repo = governance / source authority for private
  host operations.
- This public repo = MG Guide implementation, tests, public proof, and
  competition documentation.
- Competition requirements constrain the submission; they do not authorize
  production mutation.
- Agents can propose and prepare; deterministic policy and humans retain
  downstream authority.
- Synthetic data is used for the public WebMCP demo.
- Merged code is not automatically treated as production activation.

See [`governance/README.md`](governance/README.md) and
[`governance/PUBLIC_PRIVATE_BOUNDARY.md`](governance/PUBLIC_PRIVATE_BOUNDARY.md).

---

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).
