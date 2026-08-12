# MG Guide Agentic Sales Workspace

**Competition:** Google All Things Agentic Hackathon
**Target track:** Fortified Enterprise Fleet
**Vertical slice:** `meeting_follow_up_v1`
**Project status:** **PHASE 1 DETERMINISTIC FOUNDATION (synthetic fixtures only)**

This repository is the standalone, competition-period home for the MG Guide
Agentic Sales Workspace. It establishes durable provenance for the
`meeting_follow_up_v1` vertical slice using **synthetic / test data only**.

> This repository is a foundation commit only. It does **not** yet run agents,
> call CRM tools, write to Firestore, or deploy services.

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

## Project goal

After a sales meeting ends, turn a meeting transcript into a **governed CRM
follow-up record** without the salesperson manually summarizing the
conversation, finding the CRM contact, deciding the pipeline state, and
documenting the next step.

**Vertical slice promise (when implemented):**

one synthetic transcript in → one verified CRM note, at most one
policy-permitted opportunity-stage change, one Firestore audit record, and one
MG Guide next-step brief out.

---

## `meeting_follow_up_v1` scope

**In scope**

- One workflow: `meeting_follow_up_v1`
- Synthetic meeting transcript fixtures only
- Isolated / test GoHighLevel (GHL) location only
- At most one contact note create and at most one opportunity-stage change per run
- Read-back verification of every mutation
- Firestore audit record per run
- MG Guide Meeting Follow-Up card (success + needs-review)

**Out of scope (blocked)**

- Production CRM writes of any kind
- Real customer / CRM data
- Email / SMS / calendar mutation
- Contact or opportunity create/delete
- Bulk CRM operations or arbitrary stage movement
- Production activation, IAM, env, or secret provisioning in this foundation

---

## Architecture intent (not yet implemented)

| Layer | Role |
| --- | --- |
| **Google ADK + Gemini 3.5+** | Specialized reasoning agents (propose; never unilaterally decide) |
| **OL3 workflow authority** | Deterministic state machine and mutation policy gate |
| **MG MCP** | Trusted organizational context — **read-only** |
| **GHL MCP** | Standardized external CRM tool boundary (test account only) |
| **Firestore** | Runtime / audit state (`workflow_runs/{run_id}`) |
| **MG Guide** | Salesperson Meeting Follow-Up experience (application surface) |
| **Planned Cloud Run** | Future deployment target for the slice (not provisioned here) |

Authority rule: agents propose facts and actions; deterministic policy and
workflow state decide whether a GHL mutation is allowed.

### GHL MCP integration boundary

```text
Agent
  ↓
OL3 authorization / policy gate
  ↓
GHL MCP client
  ↓
GHL MCP server
  ↓
GoHighLevel test CRM (isolated location only)
```

Exact GHL MCP tool/operation names remain **UNKNOWN** until live discovery
against an authorized test account. This repository must **not** invent tool
identifiers or fall back to raw GHL REST without a new architecture decision.

---

## Safety posture

- Synthetic and fixture identities only (see [`fixtures/`](fixtures/))
- No production CRM writes
- No real customer or contact information
- No secrets committed (see [`.env.example`](.env.example) and [`docs/SECURITY.md`](docs/SECURITY.md))
- Fail-closed on ambiguous contact resolution and policy denial

---

## Repository layout

```text
README.md
LICENSE
.gitignore
.env.example
pyproject.toml
requirements.txt
.python-version
docs/
  COMPETITION_BASELINE.md
  MEETING_FOLLOW_UP_FOUNDATION.md
  SECURITY.md
contracts/
  meeting_follow_up_packet.schema.json
  workflow_states.yaml
  ghl_tool_manifest.yaml
  failure_codes.yaml
fixtures/
  transcript-*.txt
  transcript-*.expected.json
src/orchestration/
tests/
  contracts/
  workflow/
  acceptance/
proof/phase1/
competition/
  NEW_WORK_LEDGER.md
  AI_COLLABORATION_LOG.md
governance/
```

---

## Reproducible setup (currently valid steps only)

These steps are valid **today** for the foundation repository. Runtime agent,
GCP, and GHL setup are intentionally omitted until later governed phases.

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
```

**Available today:**

- Contract/schema validation (including `meeting_context_v1` and `relationship_context_v1`)
- Deterministic state machine + policy tests
- Acceptance tests for three synthetic fixture packages
- Local fixture runner (sidecar test doubles only)
- Phase 2B offline GHL read adapter (synthetic fixtures; no live CRM)
- Phase 3 unit 1 Meeting Context Agent fixture harness (Gemini provider surface; default CI offline)
- Phase 3 unit 2 Google ADK runtime orchestration + Relationship Context Agent (synthetic CRM only; stop before Follow-Up Planning Agent)

**Not yet available (do not invent):**

- Follow-Up Planning Agent and full multi-agent packet assembly end-to-end
- GHL credential configuration or live CRM calls
- Firestore / Cloud Run provisioning
- Hosted demo against deployed services

Copy [`.env.example`](.env.example) only as a **placeholder catalog**. Do not
populate production values. Do not commit a real `.env`.

---

## Governance for contributors

- Do **not** implement features directly on `main` after this bootstrap commit.
- Create subsequent work on bounded topic branches.
- Stage **exact paths only** — never `git add .`.
- Keep competition-period claims honest: see [`docs/COMPETITION_BASELINE.md`](docs/COMPETITION_BASELINE.md)
  and [`competition/NEW_WORK_LEDGER.md`](competition/NEW_WORK_LEDGER.md).

---

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).

---

## Status

| Item | State |
| --- | --- |
| Foundation docs / contracts / fixtures | Present |
| Phase 1 deterministic engine + tests | Present |
| Phase 2B offline GHL read adapter | Present (synthetic only) |
| Gemini / ADK — Meeting Context Agent (unit 1) | Implemented (fixture harness green; live model optional) |
| Full Phase 3 vertical slice (remaining agents/packet) | Not complete |
| Live GHL / CRM writes | Forbidden under current grants |
| Firestore audit writer | Not implemented |
| Cloud Run deployment | Not provisioned |
| Production CRM writes | Forbidden |
| External effects (authorized units) | Always 0 |

**Stop after unit 1:** Meeting Context Agent harness is the first Phase 3
implementation unit. Do not expand blast radius without a reviewed follow-on unit.
