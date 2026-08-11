# AI Collaboration Log

**Repository:** `themg-max/mg-guide-agentic-sales-workspace`
**Competition:** Google All Things Agentic Hackathon
**Purpose:** Transparent record of AI-assisted work during the competition period.

---

## Entry template

```text
### YYYY-MM-DD — <short title>
- Human owner:
- AI surfaces used:
- Objective:
- Artifacts touched:
- Validation:
- Human decisions retained:
- Out of scope / refused:
```

---

## Entries

### 2026-08-11 — Public repository foundation bootstrap

- **Human owner:** VS Code / MG Orchestrator (directive owner for competition foundation)
- **AI surfaces used:** GitHub Copilot CLI / MG Orchestrator session
- **Objective:** Create standalone public repository and first durable foundation commit for `meeting_follow_up_v1` without runtime implementation
- **Artifacts touched:**
  - `README.md`
  - `LICENSE`
  - `.gitignore`
  - `.env.example`
  - `docs/COMPETITION_BASELINE.md`
  - `docs/MEETING_FOLLOW_UP_FOUNDATION.md` (sanitized from reviewed PROPOSED foundation)
  - `docs/SECURITY.md`
  - `contracts/*`
  - `fixtures/*`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `git diff --check`; conflict-marker scan; secret/PII heuristic scan; exact-path staging; push foundation commit only
- **Human decisions retained:**
  - Public repository visibility
  - Synthetic/test data only
  - No production CRM writes
  - No cloud/IAM/secret provisioning in foundation
  - Exact GHL MCP tool names remain UNKNOWN until discovery
- **Out of scope / refused:**
  - Gemini agent implementation
  - GHL credential configuration
  - CRM data writes
  - Google Cloud resource provisioning
  - Mutation of the pre-existing private MG monorepo for this bootstrap publish

---

## Collaboration rules (competition period)

1. Prefer artifact commits over chat-only decisions.
2. Keep baseline vs new-work claims honest.
3. Do not paste secrets, production data, or private infrastructure IDs into AI prompts or git.
4. Subsequent implementation happens on bounded branches — not directly on `main` after bootstrap.

### 2026-08-11 — Public sanitized governance binding sync

- **Human owner:** VS Code / MG Orchestrator (directive: adoption closeout + phase1 preparation)
- **AI surfaces used:** GitHub Copilot CLI / MG Orchestrator session
- **Objective:** Publish sanitized public governance binding after private repository adoption approval; no runtime implementation
- **Artifacts touched:**
  - `governance/README.md`
  - `governance/GOVERNANCE_PROFILE.yaml`
  - `governance/EXECUTION_MANIFEST.schema.yaml`
  - `governance/PROOF_RETURN.schema.yaml`
  - `governance/PUBLIC_PRIVATE_BOUNDARY.md`
  - `README.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `git diff --check`; secret/private-identifier scan; exact path scope only
- **Human decisions retained:** repository adoption approved in private control plane only; Phase 1 implementation still unauthorized; GHL/cloud/IAM withheld
- **Out of scope / refused:** Gemini agents, GHL config, CRM writes, Firestore/Cloud Run provisioning, IAM/env/secrets, private `.ai` records, Phase 1 code

### 2026-08-11 — Ownership semantics correction (append-only)

- **Human owner:** Human operator / repository maintainer (Aaron Chandler)
- **AI surfaces used:** n/a (log correction only)
- **Objective:** Correct prior entries that incorrectly listed an AI/orchestration surface as the human owner
- **Artifacts touched:** `competition/AI_COLLABORATION_LOG.md`
- **Validation:** append-only correction; historical entries left in place
- **Human decisions retained:** human owner must be a human/operator role; VS Code / MG Orchestrator is a tool/AI surface
- **Out of scope / refused:** silent rewrite of historical entry bodies

### 2026-08-11 — Phase 1 deterministic foundation implementation

- **Human owner:** Human operator / repository maintainer (Aaron Chandler)
- **AI surfaces used:** VS Code / MG Orchestrator; GitHub Copilot CLI coding worker
- **Objective:** Implement bounded Phase 1 deterministic foundation for `meeting_follow_up_v1` using synthetic fixture sidecars only
- **Artifacts touched:**
  - `contracts/meeting_follow_up_packet.schema.json`
  - `contracts/workflow_states.yaml`
  - `contracts/failure_codes.yaml`
  - `fixtures/*.expected.json`
  - `src/orchestration/**`
  - `tests/contracts/**`
  - `tests/workflow/**`
  - `tests/acceptance/**`
  - `proof/phase1/proof-return.yaml`
  - `pyproject.toml`, `requirements.txt`, `.python-version`
  - `README.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `python -m pytest`; schema validation; YAML parse; fixture acceptance outcomes; replay/idempotency; `git diff --check`; secret/private-identifier scan
- **Human decisions retained:**
  - Phase 1 only; no Gemini/ADK/GHL/CRM/Firestore/Cloud Run
  - Free-text transcripts remain evidence fixtures; extraction facts from sidecars
  - Zero external effects
  - No `.github/workflows/**` edits (CI workflow authorization required if CI desired)
- **Out of scope / refused:**
  - Gemini / ADK agent calls
  - Live GHL / CRM network
  - Firestore / Cloud Run / IAM / secrets
  - Production data
  - Phase 2 capability discovery

### 2026-08-11 — Phase 1 deterministic CI workflow

- **Human owner:** Human operator / repository maintainer (Aaron Chandler)
- **AI surfaces used:** VS Code / MG Orchestrator; GitHub Copilot CLI coding worker
- **Objective:** Add narrow GitHub Actions CI for merged Phase 1 deterministic foundation under authorization `MG_GUIDE_PHASE1_CI_V1`
- **Artifacts touched:**
  - `.github/workflows/phase1-deterministic.yml`
  - `proof/phase1/workflow-proof-note.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** workflow file review; local contract/pytest still green; PR workflow run (to be recorded in workflow-proof-note)
- **Human decisions retained:**
  - contents:read only
  - no secrets
  - no application external effects
  - no pull_request_target
  - no GHL/CRM/Gemini/ADK/Firestore/Cloud Run/IAM
- **Out of scope / refused:** deployment, secret access, repository writes from workflow, broadening beyond Phase 1 deterministic tests

## 2026-08-11 — Phase 1 CI green on PR #3

- Human owner / operator: repository maintainer (themg-max operator)
- Tool / AI surfaces: VS Code + MG Orchestrator (Copilot CLI runtime)
- Action: repaired secret-scan self-match false positive; PR workflow run succeeded
- Evidence: Actions run https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531473115
- Head at PASS: `61c01a3152a072ebfaefa2ab97b0ab3124cea5ef`
- Phase 1 CI workflow PASS recorded
