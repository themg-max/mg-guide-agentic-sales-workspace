# Competition Acceptance — meeting_follow_up_v1

```text
ARTIFACT=proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md
COMPETITION=Google All Things Agentic Hackathon
TRACK=Fortified Enterprise Fleet
WORKFLOW=meeting_follow_up_v1
BRANCH=competition/meeting-follow-up-v1-acceptance-finalization-001
PROJECT=mg-devpost
CREATED_AT_UTC=2026-08-19T01:17:00Z
MODE=competition_acceptance_finalization
RECONCILIATION_MUTATION=NO
REAL_CUSTOMER_DATA=0
```

## Gate board

| Gate | Result | Evidence |
| --- | --- | --- |
| R4 source-authority closure | **CLOSED** (recovery PASS; lineage PARTIAL; demo not blocked) | `.ai/proof/addon-deployed-source-authority-readonly-live-20260818/r4-version47-pinned-source-recovery.md` |
| GEMINI_EXECUTION | **PASS** | Vertex AI `gemini-3.5-flash` @ `global`; live meeting-context extract schema_valid |
| ADK_EXECUTION | **PASS** | `python -m agents.follow_up_planning --scenario SUCCESS --scenario AMBIGUOUS_CONTACT` |
| CLOUD_RUN_DEPLOYMENT | **PASS** | service Ready; revision `mg-guide-agentic-sales-workspace-judge-00002-ndg` |
| FIRESTORE_AUDIT | **PASS** | Stage B smoke create→read→verify→delete |
| SUCCESS_SCENARIO | **PASS** | local judge `/demo/meeting-follow-up` + Unit3 harness |
| FAIL_CLOSED_SCENARIO | **PASS** | AMBIGUOUS_CONTACT → blocked; zero unauthorized effects |
| UNAUTHORIZED_EXTERNAL_EFFECTS | **0** | harness + judge + live Gemini path |

## Required technology declarations

| Requirement | Declaration |
| --- | --- |
| Gemini 3.5+ | `gemini-3.5-flash` via Vertex AI (`google-genai`, `vertexai=True`, location `global`) |
| Google ADK | `google-adk==1.18.0` — `Runner` / `SequentialAgent` / `InMemorySessionService` |
| Google Cloud | project `mg-devpost` |
| Cloud Run | `mg-guide-agentic-sales-workspace-judge` · region `us-east4` |
| Firestore | database `devpost-google-contest` · collection `workflow_runs` · mode `stage_b_smoke` |

## Scenario A — SUCCESS

```text
PATH=synthetic transcript → Meeting Context → Relationship Context
     → Follow-Up Planning → OL3 deterministic authorization
     → permitted synthetic effect/audit labels → MG Guide next-step state
```

Observed (local judge stub path, synthetic fixtures):

```text
workflow_status=completed
resolution_outcome.status=matched
policy_decision.note_write=allowed
policy_decision.stage_write=allowed
external_effects=0
cloud_mutation=NONE
```

Observed (Unit3 ADK package path):

```text
SUCCESS=PASS
runtime_backend=google_adk_package
google_adk_package_bound=true
deterministic_policy_gate_invoked=true
external_effects=0
```

## Scenario B — FAIL-CLOSED (AMBIGUOUS_CONTACT)

```text
PATH=ambiguous identity → agent proposal → deterministic BLOCK
     → zero unauthorized effects → needs-review / blocked state
```

Observed (local judge):

```text
workflow_status=blocked
resolution_outcome.status=ambiguous
policy_decision.reason_codes=["AMBIGUOUS_CONTACT"]
policy_decision.note_write=not_attempted
policy_decision.stage_write=not_attempted
external_effects=0
cloud_mutation=NONE
```

Observed (Unit3 ADK):

```text
AMBIGUOUS_CONTACT=PASS
EXTERNAL_EFFECTS=0
DETERMINISTIC_POLICY_BYPASS=NO
```

## Gemini live meeting-context proof

```text
MEETING_CONTEXT_GEMINI_MODE=live
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=mg-devpost
MEETING_CONTEXT_GEMINI_LOCATION=global
MEETING_CONTEXT_GEMINI_MODEL=gemini-3.5-flash
GEMINI_EXECUTION=PASS
MEETING_CONTEXT_LIVE=PASS
schema_valid=true
extraction_confidence=0.98
external_effects=0
deterministic_policy_bypass=false
```

Provider defaults now pin competition model `gemini-3.5-flash` with Vertex ADC
and schema normalizers for commitments / next_step / opportunity_signal /
evidence / confidence.

## Cloud Run proof (infrastructure)

```text
CLOUD_RUN_DEPLOYMENT=PASS
service=mg-guide-agentic-sales-workspace-judge
region=us-east4
url=https://mg-guide-agentic-sales-workspace-judge-nu73xamzbq-uk.a.run.app
latestReadyRevision=mg-guide-agentic-sales-workspace-judge-00002-ndg
Ready=True
ConfigurationsReady=True
RoutesReady=True
```

**Note:** Service is IAP-gated. Interactive browser demo against the hosted URL
requires human 2FA. Local WSGI judge proves identical scenario contract without
IAP. Hosted health/demo path is the same app packaged in `Dockerfile`.

## Firestore audit proof

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
PROJECT=mg-devpost
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs
RUN_ID=run_nw006_success_001
RESULT=PASS
FIRESTORE_CREATE_VERIFIED=YES
FIRESTORE_READBACK_VERIFIED=YES
CONTENT_FINGERPRINT_MATCH=YES
DELETE_VERIFIED=YES
CLEANUP_STATUS=SUCCESS
REAL_CUSTOMER_DATA=0
GHL_LIVE_CALLS=0
```

## R4 source-authority closure (competition stop)

```text
R4_VERSION47_PINNED_SOURCE_RECOVERY=PASS (content recovered read-only)
R3_VERSION47_TO_REPO_LINEAGE=PARTIAL (search-widget exact; ensemble drift)
R3_MUTATION_COUNT=0
RECONCILIATION_WRITE=NO
COMPETITION_SOURCE_AUTHORITY_INVESTIGATION=CLOSED
DEMO_BLOCKED_BY_SOURCE_AUTHORITY=NO
```

Private capture stays under operator config (not committed). Public redacted
proof: `.ai/proof/addon-deployed-source-authority-readonly-live-20260818/`.

## Reproduce

```bash
# Unit tests (meeting context provider)
PYTHONPATH=src python -m pytest tests/agents/test_meeting_context_agent.py -q

# ADK Unit3 SUCCESS + fail-closed
PYTHONPATH=src python -m agents.follow_up_planning \
  --scenario SUCCESS --scenario AMBIGUOUS_CONTACT

# Local judge scenarios
export PYTHONPATH=src MEETING_CONTEXT_GEMINI_MODE=stub JUDGE_MODE=local
python -m mg_guide.judge_surface.server   # then POST /demo/meeting-follow-up

# Live Gemini meeting-context (Vertex ADC)
export MEETING_CONTEXT_GEMINI_MODE=live
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=mg-devpost
export MEETING_CONTEXT_GEMINI_LOCATION=global
export MEETING_CONTEXT_GEMINI_MODEL=gemini-3.5-flash
# invoke GeminiAdkContextProvider.extract against fixtures/transcript-success.txt

# Firestore Stage B smoke (authorized)
PYTHONPATH=src python scripts/nw005/run_stage_b_wave1_smoke.py

# Cloud Run status
gcloud run services describe mg-guide-agentic-sales-workspace-judge \
  --region=us-east4 --project=mg-devpost
```

## Non-claims

- No production CRM / GHL live mutation in this acceptance lane
- No real customer data
- No Apps Script / Marketplace reconciliation write
- IAP interactive browser walkthrough deferred to human 2FA
- Judge Cloud Run image remains stub Gemini mode by design (deterministic demo)

## Related packet artifacts

- Architecture: `docs/architecture/meeting-follow-up-v1-competition-architecture.md`
- Demo script: `docs/demo/meeting-follow-up-v1-4min-demo-script.md`
- Devpost: `docs/competition/DEVPOST_WRITEUP.md`
- Provider: `src/agents/meeting_context/providers/gemini_adk_provider.py`
