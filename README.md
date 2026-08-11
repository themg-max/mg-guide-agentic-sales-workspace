# MG Guide Agentic Sales Workspace

**Competition:** Google All Things Agentic Hackathon
**Target track:** Fortified Enterprise Fleet
**Vertical slice:** `meeting_follow_up_v1`
**Project status:** **FOUNDATION / NOT YET FUNCTIONAL**

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
  transcript-success.txt
  transcript-ambiguous-contact.txt
  transcript-no-stage-change.txt
competition/
  NEW_WORK_LEDGER.md
  AI_COLLABORATION_LOG.md
```

---

## Reproducible setup (currently valid steps only)

These steps are valid **today** for the foundation repository. Runtime agent,
GCP, and GHL setup are intentionally omitted until later governed phases.

```bash
# 1. Clone
git clone https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
cd mg-guide-agentic-sales-workspace

# 2. Inspect foundation artifacts
ls docs contracts fixtures competition

# 3. Review baseline vs new-work separation
less docs/COMPETITION_BASELINE.md

# 4. Review the frozen vertical-slice foundation
less docs/MEETING_FOLLOW_UP_FOUNDATION.md

# 5. Review contracts and synthetic fixtures
less contracts/meeting_follow_up_packet.schema.json
less fixtures/transcript-success.txt
```

**Not yet available (do not invent):**

- Dependency install / package manager lockfiles
- Local agent runtime commands
- GHL credential configuration
- Firestore / Cloud Run provisioning
- Live demo script against deployed services

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
| Gemini / ADK agents | Not implemented |
| GHL MCP client | Not implemented |
| Firestore audit writer | Not implemented |
| Cloud Run deployment | Not provisioned |
| Production CRM writes | Forbidden |

**Next recommended implementation branch (after human authorization):**
`feat/meeting-follow-up-v1-phase1-contracts-fixtures` — schema tests and
deterministic state-machine scaffolding only (no AI, no GHL, no cloud).
