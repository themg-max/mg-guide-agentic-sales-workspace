# MG Guide Agentic Sales Workspace

**Competition:** Google All Things Agentic Hackathon  
**Target track:** Fortified Enterprise Fleet  
**Vertical slice:** `meeting_follow_up_v1`  
**Competition acceptance branch:** `competition/meeting-follow-up-v1-acceptance-finalization-001`

This repository is the standalone, competition-period home for the MG Guide
Agentic Sales Workspace. It establishes durable provenance for the
`meeting_follow_up_v1` vertical slice using **synthetic / test data only**.

## Competition acceptance (current)

Governed hero workflow: synthetic transcript → Meeting Context (Gemini 3.5) →
Relationship Context → Follow-Up Planning (Google ADK) → **OL3 deterministic
policy gate** → MG Guide next-step card, with Cloud Run hosting and Firestore
audit proof on Google Cloud project `mg-devpost`.

| Marker | Result |
| --- | --- |
| `GEMINI_EXECUTION` | **PASS** (`gemini-3.5-flash`, Vertex AI `global`) |
| `ADK_EXECUTION` | **PASS** (`google-adk==1.18.0` Runner/SequentialAgent) |
| `CLOUD_RUN_DEPLOYMENT` | **PASS** (`mg-guide-agentic-sales-workspace-judge`, `us-east4`) |
| `FIRESTORE_AUDIT` | **PASS** (`devpost-google-contest` / `workflow_runs` Stage B smoke) |
| `SUCCESS_SCENARIO` | **PASS** |
| `FAIL_CLOSED_SCENARIO` | **PASS** (`AMBIGUOUS_CONTACT` → blocked) |
| `UNAUTHORIZED_EXTERNAL_EFFECTS` | **0** |

**Packet**

- Acceptance proof: [`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`](proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md)
- Architecture: [`docs/architecture/meeting-follow-up-v1-competition-architecture.md`](docs/architecture/meeting-follow-up-v1-competition-architecture.md)
- Demo script (~4 min): [`docs/demo/meeting-follow-up-v1-4min-demo-script.md`](docs/demo/meeting-follow-up-v1-4min-demo-script.md)
- Devpost copy: [`docs/competition/DEVPOST_WRITEUP.md`](docs/competition/DEVPOST_WRITEUP.md)
- Demo truth boundary: [`docs/demo/meeting-follow-up-demo-v1.md`](docs/demo/meeting-follow-up-demo-v1.md)

**Quick reproduce**

```bash
PYTHONPATH=src python -m pytest tests/agents/test_meeting_context_agent.py -q
PYTHONPATH=src python -m agents.follow_up_planning \
  --scenario SUCCESS --scenario AMBIGUOUS_CONTACT
# Local judge: POST /demo/meeting-follow-up with {"scenario":"SUCCESS"|"AMBIGUOUS_CONTACT"}
PYTHONPATH=src MEETING_CONTEXT_GEMINI_MODE=stub python -m mg_guide.judge_surface.server
```

> Live CRM/GHL mutation is **not** claimed. Demo paths use synthetic fixtures.
> Cloud Run is IAP-gated (browser demo may need human 2FA). Firestore Stage B
> smoke is create→read→verify→delete under existing authorization.

### Historical merge baseline

Phase 3 Unit 1–3 and NW-006 card work are merged on `main` (Unit 3 PR #13;
NW-006 PR #15). NW-005 Stage B smoke and NW-007 Cloud Run deployment evidence
exist under governed packets. See [`competition/NEW_WORK_LEDGER.md`](competition/NEW_WORK_LEDGER.md).

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

This repository now includes the merged competition-local NW-006 MG Guide
Meeting Follow-Up card renderer/reference component with no mutation controls
and zero external effects. NW-008 acceptance readiness is planning-only.

**Target end-state defined by the original foundation:**

one synthetic transcript in → one verified CRM note, at most one
policy-permitted opportunity-stage change, one Firestore audit record, and one
MG Guide next-step brief out.

> Verified CRM mutation and Firestore audit remain undelivered in this branch.
> The competition-local card and proof artifacts document the target end-state
> without claiming live verification or runtime write delivery.

---

## `meeting_follow_up_v1` scope

**In scope**

- One workflow: `meeting_follow_up_v1`
- Synthetic meeting transcript fixtures only
- Unit 2 is offline synthetic only
- CRM environment class: **business-active canonical CRM under synthetic-only
  bounded execution controls** — no isolated GHL test location is available or
  required (see
  [`docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](docs/nw008/nw-008-active-crm-synthetic-only-normalization-001.md))
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
renderers + stdout-only CLI), is **MERGED_COMPLETE** on `main` via PR #15, and
remains host-agnostic with no private authenticated integration.

| Layer | Role |
| --- | --- |
| **Google ADK + Gemini 3.5 Flash** | Specialized reasoning agents (propose; never unilaterally decide) |
| **OL3 workflow authority** | Deterministic state machine and mutation policy gate |
| **MG MCP** | Trusted organizational context — **read-only** |
| **CRM transport** | Current next planning direction is a governed HighLevel REST v3 adapter; historical GHL MCP evidence is preserved, but generic GHL MCP implementation is blocked |
| **Firestore** | Runtime / audit state (`workflow_runs/{run_id}`) — Stage B smoke proven on `mg-devpost` |
| **MG Guide** | Salesperson Meeting Follow-Up experience (application surface) |
| **Cloud Run** | Judge/demo service `mg-guide-agentic-sales-workspace-judge` (`us-east4`, IAP) |

Authority rule: agents propose facts and actions; deterministic policy and
workflow state decide whether a GHL mutation is allowed.

### CRM transport boundary

```text
Agent
  ↓
OL3 authorization / policy gate
  ↓
HighLevel REST v3 adapter (planning next; not implemented or authorized here)
  ↓
Canonical GoHighLevel location (business-active; exact allowlisted synthetic IDs only)
```

Read-side GHL MCP identifiers were discovered and governed in Phase 2A / NW-013.
That evidence remains historical and does not require GHL MCP as the future
implementation transport. Generic GHL MCP implementation is blocked; the next
planning lane is HighLevel REST v3 adapter architecture only. REST adapter
implementation, REST execution, live GHL reads, and live GHL writes remain
unauthorized. The canonical location is not a test environment, and any live
canonical synthetic access is separately governed. This repository must **not**
invent operation contracts or request bodies without a new architecture
decision.

---

## Safety posture

- Synthetic and fixture identities only (see [`fixtures/`](fixtures/))
- No real-customer or non-allowlisted CRM mutation; any separately
  human-authorized competition CRM mutation may target only the privately
  allowlisted preverified synthetic records in the canonical business-active
  location using the exact operation budget
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

# 7. NW-006 Meeting Follow-Up card (stdout-only; synthetic packet in → text/html out)
PYTHONPATH=src python3 -m mg_guide.meeting_follow_up_card \
  fixtures/nw006/packets/packet-success.completed.json
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
- NW-006 MG Guide Meeting Follow-Up card — **MERGED_COMPLETE** (PR #15 final reviewed head `c7d25b447db0a961c17ae26e326ada230b7e4627` / exact-head CI 31630399411 SUCCESS / merge `e22eb861442a37be0797d6d7aec8bb17001fb7a3`; host-agnostic renderer only; no mutation controls; EXTERNAL_EFFECTS=0)
- NW-008 readiness matrix + planning packet — **planning only** (`proof/nw008/**`; historical AT-1…AT-10 not complete)

**Not yet available (do not invent):**

- Mutation execution (live CRM note/stage writes) — agents + policy record intents; demo path does not claim live GHL mutation
- GHL credential configuration or live CRM calls against customer data
- Unauthenticated public hosted demo (Cloud Run judge is **IAP-gated**)
- Marketplace/source reconciliation writes (R4 closed read-only for competition)

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
| MG Guide Meeting Follow-Up card (NW-006) | **MERGED_COMPLETE** — PR #15; final reviewed head `c7d25b447db0a961c17ae26e326ada230b7e4627`; exact-head CI **31630399411** SUCCESS; merge `e22eb861442a37be0797d6d7aec8bb17001fb7a3`; merged `2026-08-12T19:12:33Z`; closeout [`proof/nw006/nw-006-merge-closeout.md`](proof/nw006/nw-006-merge-closeout.md); no mutation controls; zero external effects; no private host wiring |
| Competition acceptance (`meeting_follow_up_v1`) | **Packet complete on branch** — see [`proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md`](proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md); SUCCESS + FAIL-CLOSED proven; Gemini/ADK/Cloud Run/Firestore markers PASS |
| Acceptance tests AT-1…AT-10 historical matrix (NW-008) | Readiness docs remain under [`proof/nw008/`](proof/nw008/); do not mark every historical AT complete from card tests alone |
| Live GHL / CRM writes | Forbidden under current grants |
| Firestore audit writer (NW-005) | Stage A merged; Stage B smoke **PASS** on `mg-devpost` / `devpost-google-contest` |
| Cloud Run deployment (NW-007) | Judge service **Ready** on `mg-devpost` `us-east4` (IAP-gated) |
| Production CRM writes | Forbidden |
| Unauthorized external effects (demo/harness paths) | **0** |

**Closeout state:** Competition acceptance finalization proves the
`meeting_follow_up_v1` vertical slice with Gemini 3.5+, Google ADK, Cloud Run,
and Firestore audit markers. Agents still propose only; the deterministic
policy gate still evaluates/authorizes; live CRM mutation and private host
production activation remain separate governed units.
