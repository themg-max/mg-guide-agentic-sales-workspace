# MG Guide Agentic Sales Workspace

**Competition:** Google All Things Agentic Hackathon
**Target track:** Fortified Enterprise Fleet
**Vertical slice:** `meeting_follow_up_v1`
**Project status:** **PHASE 3 CLOSED FOR UNIT 3 — Unit 1 MERGED; Unit 2 MERGED; Unit 3 MERGED (PR #13 / merge `91927e4cfeb5010cf399ae870ad0897156dff03e`); NW-004 CLOSED_SUCCESS; NW-006 IMPLEMENTED_PENDING_REVIEW (branch `feat/nw006-meeting-follow-up-card`)**

This repository is the standalone, competition-period home for the MG Guide
Agentic Sales Workspace. It establishes durable provenance for the
`meeting_follow_up_v1` vertical slice using **synthetic / test data only**.

> Phase 3 is now closed for Unit 3: Phase 1 deterministic foundation and the
> Phase 2B offline GHL read adapter are merged; Phase 3 Unit 1 (Meeting
> Context Agent) is merged; Phase 3 Unit 2 (Google ADK package runtime
> orchestration + Relationship Context Agent) is merged (PR #11); Phase 3
> Unit 3 (Follow-Up Planning Agent) is merged (PR #13). The competition-local
> NW-006 Meeting Follow-Up card module is implemented pending review. Remaining
> governed work is mutation execution, Firestore audit, deployment, and private
> host integration. There are still **no** live CRM calls, no Firestore writes,
> and no deployment.

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

This repository now includes the competition-local NW-006 MG Guide Meeting
Follow-Up card renderer/reference component with no mutation controls and zero
external effects.

**Vertical slice promise (when implemented):**

one synthetic transcript in → one verified CRM note, at most one
policy-permitted opportunity-stage change, one Firestore audit record, and one
MG Guide next-step brief out.

---

## `meeting_follow_up_v1` scope

**In scope**

- One workflow: `meeting_follow_up_v1`
- Synthetic meeting transcript fixtures only
- Unit 2 is offline synthetic only
- No isolated GHL test location is available
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

## Architecture (Phase 3 closeout state)

Unit 1, Unit 2, and Unit 3 are implemented offline against synthetic fixtures
and merged. NW-006 adds a bounded deterministic card module (mapper + text/html
renderers + stdout-only CLI) and remains host-agnostic with no private
authenticated integration.

| Layer | Role |
| --- | --- |
| **Google ADK + Gemini 3.5+** | Specialized reasoning agents (propose; never unilaterally decide) |
| **OL3 workflow authority** | Deterministic state machine and mutation policy gate |
| **MG MCP** | Trusted organizational context — **read-only** |
| **GHL MCP** | Standardized external CRM tool boundary (Unit 2 offline synthetic only) |
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
Canonical GoHighLevel location (not a test environment)
```

Read-side GHL MCP identifiers were discovered and governed in Phase 2A / NW-013.
Live canonical-location compatibility remains **unexecuted**, mutation
capability remains separately governed, and raw REST fallback remains
forbidden. The canonical location is not a test environment, and any live
canonical synthetic read is separately governed. Unit 2 does not authorize
live GHL or any writes. This repository must **not** invent tool identifiers
or fall back to raw GHL REST without a new architecture decision.

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
  follow_up_proposal.schema.json
  workflow_states.yaml
  ghl_tool_manifest.yaml
  failure_codes.yaml
fixtures/
  transcript-*.txt
  transcript-*.expected.json
src/orchestration/
src/agents/
src/integrations/
tests/
  contracts/
  workflow/
  acceptance/
  agents/
  integrations/
proof/phase1/
competition/
  NEW_WORK_LEDGER.md
  AI_COLLABORATION_LOG.md
governance/
```

---

## Reproducible setup (currently valid steps only)

These steps are valid **today**. Live GHL, GCP, Firestore, and deployment
setup remain intentionally omitted until later governed phases.

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
```

**Available today:**

- Contract/schema validation (including `meeting_context_v1`, `relationship_context_v1`, and `follow_up_proposal_v1`)
- Deterministic state machine + policy tests
- Acceptance tests for three synthetic fixture packages
- Local fixture runner (sidecar test doubles only)
- Phase 2B offline GHL read adapter (synthetic fixtures; no live CRM)
- Phase 3 unit 1 Meeting Context Agent fixture harness — **merged** (PR #10; Gemini provider surface; default CI offline)
- Phase 3 unit 2 Google ADK package runtime orchestration (actual `google-adk` Runner/SequentialAgent/session primitives; fail-closed, no local fallback) + Relationship Context Agent — **merged** (PR #11; synthetic CRM only)
- Phase 3 unit 3 Follow-Up Planning Agent — **merged** (PR #13 final reviewed head `32f13b6db0bfd9964001133d05f33d6ed294d0ba` / final exact-head CI 31623771005 / merge `91927e4cfeb5010cf399ae870ad0897156dff03e`; synthetic only; deterministic policy gate invoked; intent-only packet assembly; EXTERNAL_EFFECTS=0)

**Not yet available (do not invent):**

- Mutation execution (CRM note/stage writes) — Unit 3 records policy-bounded intents only
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
| Gemini / ADK — Meeting Context Agent (unit 1) | **Merged** (PR #10; fixture harness green; live model optional) |
| Google ADK runtime + Relationship Context Agent (unit 2) | **Merged** (PR #11 / `a3d5a5731d7342463fe365e597e5d974d3420d08`) |
| Follow-Up Planning Agent (unit 3) | **Merged** (PR #13 final reviewed head `32f13b6db0bfd9964001133d05f33d6ed294d0ba` / CI 31623771005 / merge `91927e4cfeb5010cf399ae870ad0897156dff03e`; merged `2026-08-12T17:47:49Z`) |
| MG Guide Meeting Follow-Up card (NW-006) | **IMPLEMENTED_PENDING_REVIEW** — bounded implementation packet at [`proof/nw006/nw-006-implementation-packet.md`](proof/nw006/nw-006-implementation-packet.md), implementation proof at [`proof/nw006/proof-return.yaml`](proof/nw006/proof-return.yaml); no mutation controls; zero external effects; no private host wiring |
| Full end-to-end competition vertical slice (remaining surfaces) | Not complete; remaining governed work is mutation execution, Firestore audit, deployment, and private host integration |
| Live GHL / CRM writes | Forbidden under current grants |
| Firestore audit writer | Not implemented |
| Cloud Run deployment | Not provisioned |
| Production CRM writes | Forbidden |
| External effects (authorized units) | Always 0 |

**Closeout state:** Unit 3 (Follow-Up Planning Agent) has merged under PR #13 and
NW-006 is implemented on a dedicated branch as a deterministic card renderer.
The Follow-Up Planning Agent still proposes only; the deterministic policy gate
still evaluates/authorizes; mutation execution, Firestore audit, deployment,
and private host integration remain separate governed units.
