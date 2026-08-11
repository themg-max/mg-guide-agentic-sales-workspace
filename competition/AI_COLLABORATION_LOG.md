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

