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

### 2026-08-11 — Phase 1 deterministic CI workflow authorization

- **Human owner:** Human operator / repository maintainer (Aaron Chandler)
- **AI surfaces used:** VS Code / MG Orchestrator; GitHub Copilot CLI coding worker
- **Objective:** Create a bounded CI-only branch and add Python-only deterministic verification for `meeting_follow_up_v1` under authorization `MG_GUIDE_PHASE1_CI_V1`
- **Artifacts touched:**
  - `.github/workflows/phase1-deterministic.yml`
  - `scripts/verify_phase1_deterministic.py`
  - `proof/phase1/workflow-proof-note.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `python scripts/verify_phase1_deterministic.py`; `PYTHONPATH=src python3 -m pytest -q`; `git diff --check`; repository-local secret scan
- **Human decisions retained:**
  - CI workflow is read-only and uses no repository/application secrets
  - Workflow remains bounded to local Python execution and synthetic fixtures only
  - No GHL/CRM/Gemini/ADK/GCP deployment runtime invoked
- **Out of scope / refused:**
  - Live GHL tool discovery
  - Production CRM writes
  - Cloud runtime deployment

### 2026-08-11 — Phase 1 CI green on PR #3

- **Human owner / operator:** repository maintainer (themg-max operator)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Action:** repaired secret-scan self-match false positive; PR workflow run succeeded
- **Evidence:** Actions run https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531473115
- **Head at PASS:** `61c01a3152a072ebfaefa2ab97b0ab3124cea5ef`
- **Phase 1 CI workflow PASS recorded**

### 2026-08-11 — PR #3 documentary closeout normalization

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Objective:** Documentary-only normalization of PR #3 before human review and merge; bind CI proof to current tested evidence
- **Artifacts touched:**
  - `proof/phase1/proof-return.yaml`
  - `proof/phase1/workflow-proof-note.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `python scripts/verify_phase1_deterministic.py`; `PYTHONPATH=src python -m pytest -q`; `git diff --check`; repository-local secret scan; GitHub Actions run https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31535966409 (SUCCESS) on head `69c9068ae21cf6606a3bcd9de6d82fedd611e242`
- **Human decisions retained:**
  - Documentary changes only; no workflow/runtime/test semantics altered
  - Duplicate ledger ID NW-009 (CI proof) renumbered to NW-011; NW-009 not reused
  - `proof/phase1/proof-return.yaml` now included in its own changed-files accounting
- **Out of scope / refused:**
  - Any workflow, runtime, test, or contract semantic change
  - Phase 2B or any GHL write capability

## 2026-08-11 — Phase 2A GHL MCP read discovery

- Human owner / operator: repository maintainer (themg-max operator)
- Tool / AI surfaces: VS Code + MG Orchestrator (Copilot CLI runtime)
- Authorization: `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1`
- Mode: READ ONLY meta discovery (tools/list, search_operations, describe_operation)
- Mutations executed: 0
- CRM record reads executed: 0
- Key finding: `create-note` present on anthropic_v2 catalog; absent as first-class tool on original `/mcp/` discrete surface for this PIT
- Blocker: isolated hackathon test account binding required before record probes

### 2026-08-11 — PR #4 Phase 2A meta-discovery closeout normalization

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Objective:** Documentary-only normalization of refreshed PR #4 after Phase 1 CI baseline merge; bind proof/ledger to verified green CI evidence; mark NW-003 DONE (meta-discovery only); plan NW-012 without implying record probes
- **Artifacts touched (authorized paths only):**
  - `proof/phase2/proof-return.yaml`
  - `proof/phase2/discovery-report.md`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `PYTHONPATH=src python3 scripts/verify_phase1_deterministic.py` PASS; `PYTHONPATH=src python3 -m pytest -q` PASS; `git diff --check` PASS; GitHub Actions run https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31540519394 (SUCCESS) on head `8018533ac2f12f5f6299c5325bbb9e4ad4a106a2`
- **Human decisions retained:**
  - NW-003 = Phase 2A GHL MCP meta-discovery / DONE
  - NW-012 = isolated GHL test-account record-read compatibility probe / PLANNED (not started)
  - Preserve `GHL_RECORD_READS=0`, `GHL_WRITES=0`, `PHASE2B_STARTED=NO`, `GEMINI_ADK_STARTED=NO`
  - Blocker remains `ISOLATED_HACKATHON_TEST_ACCOUNT_BINDING_REQUIRED`
  - Next gated capability `MG_GUIDE_PHASE2A_GHL_TEST_ACCOUNT_READ_PROBE_V1` must not start until PR #4 reviewed, private OL3 bridge merged, isolated binding proven, and secret path authorized
- **Out of scope / refused:**
  - Any GHL record-level read probe
  - Any GHL write / CRM mutation
  - Phase 2B
  - Gemini / ADK
  - Secret/PIT/location binding changes in the public repo

### 2026-08-11 — Phase 2A closure + no-sandbox GHL strategy adoption

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Objective:** Close `MG_GUIDE_PHASE2A_GHL_MCP_READ_DISCOVERY_V1` against durable main after human merge of PR #4; retire the isolated-test-account path; adopt governed canonical-location synthetic-record strategy
- **Artifacts touched (authorized paths only):**
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `git diff --check` PASS; secret/private-identifier scan PASS; merge SHA `c00dd75c53ba91a17607d7c9f3b4f6e042173cd3` verified on `main` after `git fetch`/`pull`
- **Human decisions retained:**
  - NW-003 = Phase 2A GHL MCP meta-discovery / DONE (preserved, unchanged)
  - NW-012 = NOT_PURSUIED_ENVIRONMENT_UNAVAILABLE (no isolated GHL hackathon/test location can be provided)
  - NW-013 = Canonical GHL location synthetic-record read proof / PLANNED
  - Canonical location is NOT classified as a test environment
  - `GHL_RECORD_READS=0`, `GHL_WRITES=0`, `PHASE2B_STARTED=NO`, `GEMINI_ADK_STARTED=NO` preserved
- **New proposals (NOT activated):**
  - `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1` — offline deterministic read adapter vs Phase 2A discovered contracts; network NONE; synthetic fixtures only; live CRM reads/writes, Gemini/ADK, deployment, IAM, Secret Manager all blocked
  - `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1` — GATED_PENDING_SYNTHETIC_RECORD_BINDING; exact synthetic contact/opportunity IDs via private allowlist; redacted proof only; `GHL_WRITES=0`, `REAL_PRODUCTION_RECORD_READS=0`
- **Out of scope / refused:**
  - Any live GHL access until human authorizes the canonical-location synthetic-read grant
  - Any GHL write / CRM mutation
  - Unrestricted production reads
  - Phase 2B mutation capability

### 2026-08-11 — Phase 2B offline GHL read adapter

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Private execution authority:** `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1`
- **Objective:** Implement a deterministic, fixture-only GHL MCP read adapter after PR #5 merged, without live GHL access.
- **Artifacts touched (authorized paths only):**
  - `src/integrations/ghl/**`
  - `tests/integrations/ghl/**`
  - `fixtures/ghl/**`
  - `proof/phase2b/**`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `PYTHONPATH=src python3 scripts/verify_phase1_deterministic.py`; `PYTHONPATH=src python3 -m pytest -q`; `git diff --check`
- **Human decisions retained:**
  - Private authorization binds public PR #5 merge SHA `ea44f366f82039d3fa19168af1996a73253e6924`
  - Read allowlist is limited to discovered contact, opportunity, and pipeline operations
  - Synthetic fixtures are the sole response source; no adapter transport exists
  - Canonical-location synthetic read proof remains separately gated
- **Out of scope / refused:**
  - Any live GHL/CRM call or credential/Secret Manager path
  - `create-note`, `update-opportunity`, or any CRM mutation
  - Gemini, ADK, Firestore, Cloud Run, IAM, and non-synthetic data

### 2026-08-12 — Canonical synthetic-read human binding + activation decision

- **Human owner / operator:** repository maintainer / CRM operator (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1`
- **Objective:** Record public-sanitized human synthetic-record binding, PIT/canonical-location verification (no token values), and explicit activation decision; do **not** execute any live GHL call
- **Artifacts touched (authorized paths only):**
  - `governance/authorizations/MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1.yaml`
  - `governance/GOVERNANCE_PROFILE.yaml`
  - `proof/canonical-synthetic-read-binding-v1/**`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** YAML parse of binding + execution-manifest; `git diff --check`; secret/private-identifier heuristic scan; no network/CRM calls
- **Human decisions retained:**
  - `DECISION=AUTHORIZED_FOR_EXECUTION`
  - `HUMAN_SIGNATURE=APPROVED`
  - `SYNTHETIC_CONTACT_BOUND=YES`, `SYNTHETIC_OPPORTUNITY_BOUND=YES`, `RELATIONSHIP_VERIFIED=YES`
  - `PRIVATE_ALLOWLIST_COMPLETE=YES` (IDs private-control-plane only)
  - `PIT_CANONICAL_LOCATION_VERIFIED=YES`, `IAM_CHANGE_REQUIRED=NO`
  - Authorized ops only: exact-ID `get-contact` MAX=1, exact-ID `get-opportunity` MAX=1, `get-pipelines` metadata
  - All searches/writes/email/SMS/raw REST/non-allowlisted IDs denied
  - `GHL_LIVE_CALLS=0`, `GHL_WRITES=0` for this binding unit
  - `DEPLOYMENT_AUTHORIZED=NO`, `GEMINI_ADK_AUTHORIZED=NO`, `AUTHORITY_EXPANSION=NO`
- **Out of scope / refused:**
  - Any live GHL/CRM call in this unit
  - Public disclosure of exact record IDs or PIT/token values
  - CRM writes, deployment, Gemini/ADK, IAM/secret mutation
  - Mapping private monorepo PR #2954 path literally (not present in this public repo); public PR created on topic branch instead

### 2026-08-12 — Phase 2B offline adapter closeout (PR #6 merged)

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Objective:** Close `MG_GUIDE_PHASE2B_GHL_READ_ADAPTER_OFFLINE_V1` against durable public `main` after human merge of PR #6; mark NW-014 DONE; preserve NW-013 unexecuted with no live GHL claim
- **Artifacts touched (authorized paths only):**
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
  - `proof/phase2b/**`
- **Validation:** `PYTHONPATH=src python3 scripts/verify_phase1_deterministic.py`; `PYTHONPATH=src python3 -m pytest -q`; `git diff --check`
- **Human decisions retained:**
  - Source PR #6 MERGED
  - Head SHA `075a3ea47dda02fdaffdc4390d4573f947959103`
  - Merge SHA `2b88240e1e023150449183b03c118b91d663cabc`
  - `network_calls=0`, `crm_reads=0`, `crm_writes=0`
  - NW-014 = DONE / offline grant `CLOSED_SUCCESS`
  - NW-013 remains PLANNED / unexecuted (`GATED_PENDING_SYNTHETIC_RECORD_BINDING`)
  - No live GHL claim; canonical-location synthetic read proof remains separately gated in private OL3
- **Out of scope / refused:**
  - Any live GHL/CRM call
  - Any CRM write / mutation
  - Binding real or synthetic record IDs into the public repo
  - Gemini / ADK / deployment / IAM / Secret Manager mutation

### 2026-08-12 — NW-004 Phase 3 Gemini/ADK authorization sync (private PR #2964 merged)

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1`
- **Objective:** Sync sanitized public grant/ledger after private source-authority merge; do **not** start Gemini/ADK implementation in this unit
- **Artifacts touched (authorized paths only):**
  - `governance/authorizations/MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1.yaml`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Private provenance (sanitized):**
  - `PRIVATE_PHASE3_AUTHORIZATION_PR=https://github.com/themg-max/A.I-Rolodex---Context/pull/2964`
  - `PRIVATE_PHASE3_AUTHORIZATION_MERGE_SHA=7c3f605504956aa26faf62ce6db0552ba9abe494`
- **Human decisions retained:**
  - `DECISION=AUTHORIZED_FOR_IMPLEMENTATION`
  - `HUMAN_SIGNATURE=APPROVED`
  - `NW004_STATUS=AUTHORIZED_FOR_IMPLEMENTATION`
  - `GEMINI_ADK_AUTHORIZED=YES`
  - `GEMINI_ADK_STARTED=NO`
  - Deterministic policy remains authoritative (bypass forbidden)
  - First unit after sync merge: Meeting Context Agent fixture harness only
  - `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_DATA=0`
  - `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
- **Out of scope / refused:**
  - Implementation code in this authorization-sync unit
  - Live GHL/CRM calls or writes
  - L3A promotion, Firestore writes, deployment, IAM/secret mutation
  - Private IDs, secrets, or control-plane paths in public artifacts
  - Authority expansion beyond the grant envelope

### 2026-08-12 — Phase 3 unit 1: Meeting Context Agent fixture harness

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` (NW-004)
- **Objective:** First implementation unit only — synthetic transcript → schema-valid structured meeting context; stop when tests green
- **Branch:** `feat/meeting-follow-up-v1-gemini-adk-vertical-slice`
- **Artifacts touched (authorized paths only):**
  - `contracts/meeting_context.schema.json`
  - `src/agents/meeting_context/**`
  - `tests/agents/test_meeting_context_agent.py`
  - `proof/phase3/**`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Validation:** `PYTHONPATH=src python3 -m pytest -q` PASS; fixture harness fixture + gemini_adk_stub PASS; `git diff --check`
- **Proof:**
  - `GEMINI_PROVIDER_STARTED=YES`
  - `GOOGLE_ADK_RUNTIME_STARTED=NO`
  - `ADK_INTEGRATION_STATUS=COMPATIBLE_SURFACE_ONLY`
  - `GEMINI_ADK_STARTED=YES` (compatibility umbrella only; not ADK runtime)
  - `MEETING_CONTEXT_AGENT_IMPLEMENTED=YES`
  - `SYNTHETIC_TRANSCRIPT_INPUT=YES`
  - `STRUCTURED_CONTEXT_OUTPUT=VALID`
  - `DETERMINISTIC_POLICY_BYPASS=NO`
  - `EXTERNAL_EFFECTS=0`
  - `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
  - `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`
- **Out of scope / refused this unit:**
  - Google ADK runtime execution
  - Relationship / Follow-Up agents and full packet assembly
  - Live GHL/CRM calls or writes
  - L3A promotion, Firestore, deployment, IAM/secret mutation
  - Deterministic policy bypass

### 2026-08-12 — PR #10 proof/governance consistency repair (stop for disposition)

- **Human owner / operator:** repository maintainer (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` (NW-004) — repair only; no Unit 1 scope expansion
- **Objective:** Reconcile public grant execution state; separate Gemini provider vs Google ADK runtime claims; fix proof SHA semantics; optional network-free mocked live provider test
- **Branch / PR:** `feat/meeting-follow-up-v1-gemini-adk-vertical-slice` / #10
- **Artifacts touched (authorized paths only):**
  - `governance/authorizations/MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1.yaml` (`execution_status=IN_PROGRESS_UNIT1_COMPLETE`)
  - `proof/phase3/proof-return.yaml` (`reviewed_head_sha` / `ci_run_id`; no self-ref head)
  - `proof/phase3/unit1-closeout.md`
  - `src/agents/meeting_context/**` (precise tech markers + harness telemetry)
  - `tests/agents/test_meeting_context_agent.py` (markers + mocked live path)
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
- **Evidence binding:**
  - `reviewed_head_sha=b5d44b703f4ca3c2245c8e0d8b27752171c6fc29`
  - `reviewed_head_role=pre-repair_exact_evidence_head`
  - `ci_run_id=31608390000`
- **Assertions retained:**
  - `PUBLIC_GRANT_STATE_MATCH=YES`
  - `GEMINI_PROVIDER_STARTED=YES`
  - `GOOGLE_ADK_RUNTIME_STARTED=NO`
  - `ADK_INTEGRATION_STATUS=COMPATIBLE_SURFACE_ONLY`
  - `PROOF_HEAD_SEMANTICS_VALID=YES`
  - `EXTERNAL_EFFECTS=0`, `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
  - `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`
- **Out of scope / refused:** Unit 1 feature expansion; live network Gemini; CRM; merge without reviewer disposition
- **STOP:** `STOP_CODE=PHASE3_UNIT1_PROOF_GOVERNANCE_REPAIR_READY_FOR_REVIEW`

### 2026-08-12 — Phase 3 Unit 1 merge closeout + Unit 2 ADK runtime / Relationship Context

- **Human owner / operator:** VS Code / MG Orchestrator (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` (NW-004) — no new grant
- **Objective:** Close PR #10 as merged Unit 1 baseline; implement Unit 2 Google ADK runtime orchestration + Relationship Context Agent using synthetic/offline CRM only; stop before Follow-Up Planning Agent
- **Branch:** `feat/meeting-follow-up-v1-adk-relationship-context-unit2` (fresh; does not reuse Unit 1 branch)
- **Unit 1 baseline:** PR #10 **MERGED**; `PUBLIC_PR10_MERGE_SHA=469ae3ba9962895bd77bebb9e5b2b44a8faac6e7`; `PHASE3_UNIT1_STATUS=MERGED_COMPLETE`
- **Artifacts touched (authorized paths only):**
  - `contracts/relationship_context.schema.json`
  - `fixtures/ghl/relationship-context-crm.json`
  - `src/agents/adk_runtime/**`
  - `src/agents/relationship_context/**`
  - `tests/agents/test_relationship_context_unit2.py`
  - `proof/phase3/unit2/**` (new; does not overwrite Unit 1 proof)
  - `governance/authorizations/MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1.yaml`
  - `competition/NEW_WORK_LEDGER.md`
  - `competition/AI_COLLABORATION_LOG.md`
  - `README.md`, `pyproject.toml`, `.env.example` (bounded Unit 2 docs)
- **Validation:** `PYTHONPATH=src python3 -m pytest -q` PASS; Unit 1 harness fixture + gemini_adk_stub PASS; Unit 2 relationship/ADK harness PASS; `git diff --check` PASS
- **Proof:**
  - `GOOGLE_ADK_RUNTIME_STARTED=YES`
  - `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`
  - `MEETING_CONTEXT_AGENT_REUSED=YES`
  - `RELATIONSHIP_CONTEXT_AGENT_IMPLEMENTED=YES`
  - `OFFLINE_GHL_ADAPTER_USED=YES`
  - `SYNTHETIC_CRM_CONTEXT_ONLY=YES`
  - `RELATIONSHIP_CONTEXT_OUTPUT=VALID`
  - `RELATIONSHIP_MATCH=PASS`
  - `AMBIGUOUS_CONTACT=PASS`
  - `NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT=PASS`
  - `DETERMINISTIC_POLICY_BYPASS=NO`
  - `EXTERNAL_EFFECTS=0`
  - `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_DATA=0`
  - `L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED`, `FIRESTORE_WRITES=0`, `DEPLOYMENT=NO`
- **Human decisions retained:**
  - `NW004_STATUS=IN_PROGRESS`
  - `NEXT_PHASE3_UNIT=GOOGLE_ADK_RUNTIME_PLUS_RELATIONSHIP_CONTEXT` (this unit)
  - Unit 1 provider markers remain surface-only; Unit 2 runtime markers are separate and true
  - Stop before Follow-Up Planning Agent and full packet assembly
- **Out of scope / refused this unit:**
  - Follow-Up Planning Agent
  - Full packet assembly end-to-end
  - Live GHL/CRM calls or writes; broad CRM search; production/customer data
  - L3A promotion, Firestore writes, deployment, IAM/secret mutation
  - Deterministic policy bypass; authority expansion
- **STOP:** `STOP_CODE=PHASE3_UNIT2_ADK_RELATIONSHIP_CONTEXT_READY_FOR_REVIEW`

### 2026-08-12 — Phase 3 Unit 2 sponsor-tech truth repair (PR #11)

- **Human owner / operator:** VS Code / MG Orchestrator (Aaron Chandler)
- **Tool / AI surfaces:** VS Code + MG Orchestrator (Copilot CLI runtime)
- **Authorization:** `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` (NW-004) — no new grant; Unit 2 scope preserved (no Follow-Up Planning Agent)
- **Objective:** Repair PR #11 so actual Google ADK execution truth equals recorded proof truth, and reconcile public docs
- **Root cause repaired:** prior Unit 2 evidence recorded ADK runtime claims backed by custom local orchestration plus an import-only `google.adk` binding
- **Repair 1 (runtime):** Unit 2 now orchestrates through actual `google.adk` primitives — `Runner` + `SequentialAgent` + custom `BaseAgent` wrappers + `InMemorySessionService`; package pinned `google-adk==1.18.0`; fail-closed with no local fallback when the package is unavailable; all runtime markers derived from measured runtime state
- **Repair 2 (test/proof):** added runtime-truth consistency test (fails if `GOOGLE_ADK_RUNTIME_STARTED=YES` without package bound, or `RUNTIME_INTEGRATED` without backend `google_adk_package`); added fail-closed `AMBIGUOUS_OPPORTUNITY` scenario (unique contact + multiple eligible open opportunities → select none, no stage target, require review, external effects 0); all prior scenarios preserved
- **Repair 3 (docs):** README no longer claims "Phase 1 foundation / does not run agents"; records Unit 1 merged + Unit 2 current, full slice not complete, no live CRM/Firestore/deployment. `.env.example` no longer "FOUNDATION ONLY"; states canonical GHL location is not a test environment and live GHL remains unused/unauthorized by Phase 3 Unit 2; placeholders only, no real IDs/tokens
- **Evidence head:** `5878c05a1881e4fde1c70ab1624704fdf8154ba4` (pre-binding); CI run 31614783508 SUCCESS
- **Validation:** `PYTHONPATH=src python3 -m pytest -q` (71 passed); Unit 1 fixture + gemini_adk_stub harnesses PASS; `agents.relationship_context` / `agents.adk_runtime` PASS; `git diff --check` PASS
- **Proof:**
  - `GOOGLE_ADK_PACKAGE_BOUND=YES`, `GOOGLE_ADK_RUNTIME_STARTED=YES`
  - `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`, `ADK_RUNTIME_BACKEND=google_adk_package`
  - `ADK_RUNTIME_PRIMITIVE_USED=YES`, `LOCAL_ADK_FALLBACK_USED=NO`
  - `RELATIONSHIP_MATCH=PASS`, `AMBIGUOUS_CONTACT=PASS`, `NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT=PASS`, `AMBIGUOUS_OPPORTUNITY=PASS`
  - `DETERMINISTIC_POLICY_BYPASS=NO`, `EXTERNAL_EFFECTS=0`, `GHL_LIVE_CALLS=0`, `GHL_WRITES=0`, `REAL_CUSTOMER_DATA=0`
- **Out of scope / refused:** Follow-Up Planning Agent; live GHL reads/writes; Firestore; deployment; L3A promotion; merge without reviewer disposition
- **STOP:** `STOP_CODE=PHASE3_UNIT2_REPAIR_READY_FOR_REVIEW`
