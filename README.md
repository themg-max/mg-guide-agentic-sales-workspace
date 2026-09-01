# MG Guide | Agentic Sales Workspace

MG Guide turns a meeting transcript into structured relationship context and a
governed follow-up plan so salespeople can move from conversation to action
without rebuilding context manually.

**Competition:** Google All Things Agentic Hackathon
**Track:** Fortified Enterprise Fleet
**Vertical slice:** `meeting_follow_up_v1`

Judges: start at [JUDGE_START_HERE.md](JUDGE_START_HERE.md).

---

## MG Guide + WebMCP

MG Guide already helps turn meetings into relationship-aware follow-up. For
**The WebMCP Challenge** we added a new browser-native agent interface so the
same web experience can expose structured capabilities directly to a user's
agent, without weakening the existing authenticated judge/add-on surface or
introducing any new live CRM effect.

**Tools registered via `document.modelContext.registerTool`:**

| Tool | Purpose |
| --- | --- |
| `process_meeting_follow_up` | Runs `meeting_follow_up_v1` against a bounded synthetic scenario (`SUCCESS` or `AMBIGUOUS_CONTACT`) |
| `get_current_follow_up_state` | Reads the current visible state without rerunning the workflow |
| `get_follow_up_draft` | Reads the deterministic follow-up draft already produced by the existing projection |

- The human remains in control — every tool call visibly updates the same
  page a human sees, and any follow-up draft requires a human to send it.
- The agent can process and inspect — but never mutate CRM, send email, or
  call HighLevel.
- Ambiguous relationship identity always fails closed: no draft, no action.
- No live CRM effect is required for the WebMCP demo — it runs entirely on
  synthetic fixture data.

| | |
| --- | --- |
| **Live URL** | _pending deployment — see [`competition/webmcp/SUBMISSION_CHECKLIST.md`](competition/webmcp/SUBMISSION_CHECKLIST.md)_ |
| **Browser testing steps** | [`competition/webmcp/JUDGE_TESTING.md`](competition/webmcp/JUDGE_TESTING.md) |
| **WebMCP enablement** | Test in Chrome with WebMCP testing enabled, per current [WebMCP developer documentation](https://developer.chrome.com/) |
| **Local setup** | `PYTHONPATH=src python -m mg_guide.webmcp.server`, then open `http://localhost:8080/` |
| **Architecture** | [`competition/webmcp/WEBMCP_ARCHITECTURE.md`](competition/webmcp/WEBMCP_ARCHITECTURE.md) |
| **Competition delta** | [`competition/webmcp/COMPETITION_DELTA.md`](competition/webmcp/COMPETITION_DELTA.md) |

---

## Why we built it

Before COVID, much financial-services relationship work happened face to face.
Today many conversations happen online.

The meeting is digital, but the work after the meeting is still fragmented:

- reviewing what was said
- remembering personal and business context
- finding the correct CRM relationship
- documenting the conversation
- determining the next step
- preparing future follow-up

MG Guide is designed to close that gap. This competition slice is bounded and
honest: agents understand and propose, policy decides, and live CRM effects
remain separately governed. It does not claim production automation or a
same-run transcript-to-live-CRM write.

---

## How it works

```text
Google Workspace meeting
  -> transcript
  -> MG Guide Orchestrator on Google Cloud Agent Runtime
  -> Meeting Context Agent
  -> Relationship Context Agent
  -> Follow-Up Planning Agent
  -> deterministic policy
  -> MG Guide follow-up experience / audit state / bounded CRM boundary
```

A salesperson finishes a meeting. MG Guide reads the transcript, reconstructs
what happened, connects it to relationship context, and recommends the next
step. Deterministic policy then either permits the follow-up path or fail-closes
when identity or permission is not trustworthy.

---

## Three specialized agents

| Agent | Role |
| --- | --- |
| **Meeting Context Agent** | Understands what happened. |
| **Relationship Context Agent** | Connects the meeting to the correct relationship context. |
| **Follow-Up Planning Agent** | Turns that context into the recommended next steps. |

These three agents run as an internal Google ADK `SequentialAgent` sequence
inside one hosted orchestrator: `mg-guide-orchestrator`.

Hosted sequence:

```text
meeting_context_agent
relationship_context_agent
follow_up_planning_agent
```

---

## Google Cloud

| Technology | Role |
| --- | --- |
| **Google Cloud Agent Runtime** | Hosts `mg-guide-orchestrator` |
| **Google ADK** | `SequentialAgent` three-agent graph |
| **Gemini 3.5 Flash** | Meeting-context extraction |
| **Cloud Run** | Competition judge / Workspace adapter surface |
| **Firestore** | Audit proof |

Cloud Run is not the hosted three-agent runtime. Agent Runtime hosts the
three-agent graph. Cloud Run serves the competition judge / Workspace adapter
experience.

---

## Try MG Guide

Judge competition Workspace account:

`mg_guide.judge@themiliare-group.com`

The password / access secret is provided privately through the Devpost testing
credentials / authorized judge instructions and is intentionally not committed
to this public repository.

### Shortest safe judge journey

1. Sign into the provided Google Workspace account.
2. Open Gmail or Calendar.
3. Launch **MG Guide**.
4. Run the Meeting Follow-Up demonstration.
5. Review the completed and needs-review behaviors.

| Demonstration | What to look for |
| --- | --- |
| SUCCESS | Completed follow-up plan |
| AMBIGUOUS_CONTACT | Needs-review / fail-closed behavior |

Access details: [docs/judges/JUDGE_ACCESS.md](docs/judges/JUDGE_ACCESS.md).

The Workspace add-on is a thin presentation and routing adapter. It does not
own policy, CRM mutation, agent reasoning, or workflow truth.

---

## What is proven

| Capability | State |
| --- | --- |
| Gemini meeting-context extraction | Proven |
| Google ADK three-agent workflow | Proven |
| Hosted Agent Runtime deployment | Proven |
| Hosted three-agent sequential execution | Proven |
| Success scenario | Proven |
| Ambiguous-contact fail-closed scenario | Proven |
| Firestore audit proof | Proven |
| HighLevel REST v3 exact synthetic contact read | Proven |
| Current REST note create/readback | Pending |
| Same-run transcript-to-live-CRM write | Not claimed |

Exact current CRM language:

```text
LIVE_REST_V3_EXACT_CONTACT_READ=PASS
NETWORK_CALL_COUNT=1
MUTATION_CALL_COUNT=0
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
HOSTED_GHL_CALLS=0
HOSTED_CRM_MUTATIONS=0
```

Historical Grant 008 live synthetic note+stage proof is supporting evidence
only. It is not the current transport centerpiece.

---

## Repository navigation

**Judge path**

- [JUDGE_START_HERE.md](JUDGE_START_HERE.md)
- [docs/judges/README.md](docs/judges/README.md)
- [docs/architecture/meeting-follow-up-v1-competition-architecture.md](docs/architecture/meeting-follow-up-v1-competition-architecture.md)
- [docs/demo/meeting-follow-up-v1-4min-demo-script.md](docs/demo/meeting-follow-up-v1-4min-demo-script.md)
- [docs/competition/DEVPOST_WRITEUP.md](docs/competition/DEVPOST_WRITEUP.md)

**Best current proof**

- [proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md](proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md)
- [proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md](proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md)
- [competition/NEW_WORK_LEDGER.md](competition/NEW_WORK_LEDGER.md)

More evidence: [docs/judges/PROOF_INDEX.md](docs/judges/PROOF_INDEX.md) and
[proof/README.md](proof/README.md).

---

## Governance binding

Public sanitized governance lives under [`governance/`](governance/).

- Private AI Rolodex context repo = governance / source authority
- This public repo = implementation / test / public proof
- Agents propose; deterministic policy authorizes
- External mutations are separately gated
- Synthetic data only unless later granted
- Proof required; merged PR ≠ production activation

See [`governance/README.md`](governance/README.md) and
[`governance/PUBLIC_PRIVATE_BOUNDARY.md`](governance/PUBLIC_PRIVATE_BOUNDARY.md).

---

## Architecture (competition)

| Layer | Role |
| --- | --- |
| **Google Cloud Agent Runtime** | Hosted `mg-guide-orchestrator` |
| **Google ADK + Gemini 3.5 Flash** | Specialized reasoning agents (propose; never unilaterally decide) |
| **Deterministic policy** | State machine and mutation policy gate |
| **HighLevel REST v3 bounded adapter** | Current CRM boundary |
| **Firestore** | Runtime / audit state |
| **MG Guide** | Salesperson Meeting Follow-Up experience |
| **Cloud Run** | Judge / Workspace adapter surface |
| **Google Workspace add-on** | Thin presentation and routing adapter |

Authority rule: agents propose facts and actions; deterministic policy decides
whether an external effect is allowed.

### CRM transport boundary

```text
Agent
  ↓
deterministic policy gate
  ↓
HighLevel REST v3 bounded adapter
  ↓
allowlisted synthetic CRM records only
```

Current REST posture:

```text
LIVE_REST_V3_EXACT_CONTACT_READ=PASS
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
```

Historical HighLevel MCP evidence is preserved as supporting history. Generic
GHL MCP implementation is not the current transport.

---

## Safety posture

- Synthetic and fixture identities only (see [`fixtures/`](fixtures/))
- No real-customer CRM mutation
- No secrets committed (see [`.env.example`](.env.example) and [`docs/SECURITY.md`](docs/SECURITY.md))
- Fail-closed on ambiguous contact resolution and policy denial
- Judge/demo path does not perform live CRM mutation

---

## Reproducible setup (currently valid steps only)

These steps are valid **today**. Live GHL, GCP, Firestore, and deployment
setup remain separately governed.

```bash
# 1. Clone
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
cd mg-guide-agentic-sales-workspace

# 2. Python Phase 1 deterministic suite (no network at runtime)
python3 -m pip install -r requirements.txt
PYTHONPATH=src python3 -m pytest -q

# 3. Run one synthetic fixture package (intent-only; zero external effects)
PYTHONPATH=src python3 -m orchestration fixtures/transcript-success.expected.json

# 4. Phase 3 unit 1 — Meeting Context Agent fixture harness (offline by default)
PYTHONPATH=src python3 -m agents.meeting_context --provider fixture
PYTHONPATH=src python3 -m agents.meeting_context --provider gemini_adk_stub

# 5. Phase 3 unit 2 — ADK runtime + Relationship Context Agent (offline synthetic CRM)
PYTHONPATH=src python3 -m agents.relationship_context
PYTHONPATH=src python3 -m agents.adk_runtime

# 6. Phase 3 unit 3 — Follow-Up Planning Agent (proposal + policy gate + packet; intent-only)
PYTHONPATH=src python3 -m agents.follow_up_planning

# 7. NW-006 Meeting Follow-Up card (stdout-only; synthetic packet in → text/html out)
PYTHONPATH=src python3 -m mg_guide.meeting_follow_up_card \
  fixtures/nw006/packets/packet-success.completed.json

# 8. Local judge surface (stub Gemini; no live CRM mutation)
PYTHONPATH=src MEETING_CONTEXT_GEMINI_MODE=stub python -m mg_guide.judge_surface.server
# POST /demo/meeting-follow-up with {"scenario":"SUCCESS"|"AMBIGUOUS_CONTACT"}
```

Copy [`.env.example`](.env.example) only as a **placeholder catalog**. Do not
populate production values. Do not commit a real `.env`.

---

## Repository layout

```text
README.md
JUDGE_START_HERE.md
docs/judges/          Judge navigation
docs/architecture/    Architecture
docs/demo/            Demo script and truth boundary
docs/competition/     Devpost write-up
competition/          Competition Delta and AI collaboration log
proof/                Durable proof (do not relocate)
workspace_addon/      Thin Workspace presentation adapter
src/                  Runtime source
tests/                Tests
governance/           Public sanitized governance
```

---

## Governance for contributors

- Do **not** implement features directly on `main`.
- Create subsequent work on bounded topic branches.
- Stage **exact paths only** — never `git add .`.
- Keep competition-period claims honest: see [`docs/COMPETITION_BASELINE.md`](docs/COMPETITION_BASELINE.md)
  and [`competition/NEW_WORK_LEDGER.md`](competition/NEW_WORK_LEDGER.md).

---

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).
