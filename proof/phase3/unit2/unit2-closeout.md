# Phase 3 Unit 2 Closeout — Google ADK runtime + Relationship Context Agent

| Field | Value |
| --- | --- |
| Grant | `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` |
| Ledger | NW-004 |
| Branch | `feat/meeting-follow-up-v1-adk-relationship-context-unit2` |
| Public PR | #11 |
| Unit 1 baseline | PR #10 **MERGED** @ `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7` |
| Unit | Google ADK runtime orchestration + Relationship Context Agent |
| Status | **REPAIRED / TESTS GREEN** (stop before merge) |
| Grant execution_status | `IN_PROGRESS_UNIT2` |
| Stop before | Follow-Up Planning Agent |
| Evidence head | `5878c05a1881e4fde1c70ab1624704fdf8154ba4` (pre-binding; repairs `b37247aba390080ee3acd7d4f971b53d47fa695e`) |
| CI | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31614783508 **SUCCESS** |

## Repair note (sponsor-tech truth)

The first Unit 2 evidence head backed `GOOGLE_ADK_RUNTIME_STARTED=YES` with a
custom local orchestration class plus an import-only `google.adk` binding.
That did not equal actual Google ADK runtime execution. This repair:

- Orchestrates Unit 2 through **actual `google.adk` primitives**:
  `Runner` + `SequentialAgent` + custom `BaseAgent` wrappers +
  `InMemorySessionService` (package pinned `google-adk==1.18.0`).
- **Derives** all runtime markers from measured runtime state (package
  binding, backend, consumed ADK events, session state). No hard-coded truth.
- **Fails closed** when the google-adk package is unavailable — there is no
  local fallback runtime (`LOCAL_ADK_FALLBACK_USED=NO`).
- Adds a truth-consistency test: fails if `GOOGLE_ADK_RUNTIME_STARTED=YES`
  without the package bound, or if `ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED`
  without `ADK_RUNTIME_BACKEND=google_adk_package`.
- Adds fail-closed `AMBIGUOUS_OPPORTUNITY` scenario: a uniquely matched
  contact with multiple eligible open opportunities selects **none**, sets no
  stage target, requires review, external effects = 0.
- Reconciles README/.env.example to the Unit 2 state.

## Proof assertions

```text
GOOGLE_ADK_PACKAGE_BOUND=YES
GOOGLE_ADK_RUNTIME_STARTED=YES
ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED
ADK_RUNTIME_BACKEND=google_adk_package
ADK_RUNTIME_PRIMITIVE_USED=YES
LOCAL_ADK_FALLBACK_USED=NO
MEETING_CONTEXT_AGENT_REUSED=YES
RELATIONSHIP_CONTEXT_AGENT_IMPLEMENTED=YES
OFFLINE_GHL_ADAPTER_USED=YES
SYNTHETIC_CRM_CONTEXT_ONLY=YES
RELATIONSHIP_CONTEXT_OUTPUT=VALID
DETERMINISTIC_POLICY_BYPASS=NO
EXTERNAL_EFFECTS=0
GHL_LIVE_CALLS=0
GHL_WRITES=0
REAL_CUSTOMER_DATA=0
L3A_RUNTIME_STATUS=DEFERRED_RUNTIME_NOT_PROMOTED
FIRESTORE_WRITES=0
DEPLOYMENT=NO
```

## Scenario results

| Scenario | Transcript fixture | Expected status | Result |
| --- | --- | --- | --- |
| `RELATIONSHIP_MATCH` | `transcript-success` | `matched` | **PASS** |
| `AMBIGUOUS_CONTACT` | `transcript-ambiguous-contact` | `ambiguous` | **PASS** |
| `NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT` | `transcript-no-stage-change` | `opportunity_missing` | **PASS** |
| `AMBIGUOUS_OPPORTUNITY` | `transcript-ambiguous-opportunity` | `opportunity_ambiguous` | **PASS** |

## Architecture (Unit 2 stop gate)

```text
synthetic transcript
  -> Meeting Context Agent (reused from Unit 1; ADK BaseAgent wrapper)
  -> Google ADK SequentialAgent + Runner + InMemorySessionService
  -> Relationship Context Agent (ADK BaseAgent wrapper)
  -> Phase 2B offline GHL adapter
  -> synthetic contact/opportunity context
  -> relationship_context_v1
  -> STOP  (Follow-Up Planning Agent not invoked)
```

## Sponsor-tech precision

| Claim | Unit 2 truth |
| --- | --- |
| Unit 1 Meeting Context provider surface | **Unchanged** (`COMPATIBLE_SURFACE_ONLY` / provider-level ADK runtime = NO) |
| Google ADK runtime orchestration | **Started** via actual `google.adk` package primitives (`GOOGLE_ADK_PACKAGE_BOUND=YES`, `GOOGLE_ADK_RUNTIME_STARTED=YES`) |
| ADK integration | **RUNTIME_INTEGRATED** with `ADK_RUNTIME_BACKEND=google_adk_package`; no local fallback (`LOCAL_ADK_FALLBACK_USED=NO`) |
| Relationship Context Agent | **Implemented** against synthetic CRM only |
| Offline GHL adapter | **Used** (Phase 2B; no transport / no live calls) |

## Delivered

- `src/agents/adk_runtime/**` — google.adk Runner/SequentialAgent/BaseAgent orchestration, session/trace, derived markers
- `src/agents/relationship_context/**` — agent, fail-closed resolver (incl. ambiguous-opportunity), synthetic CRM store, schema validation, harness
- `contracts/relationship_context.schema.json` (+ `opportunity_ambiguous` status)
- `contracts/failure_codes.yaml` (+ `AMBIGUOUS_OPPORTUNITY`)
- `fixtures/ghl/relationship-context-crm.json` (+ multi-opportunity synthetic contact)
- `fixtures/transcript-ambiguous-opportunity.{txt,expected.json}`
- `tests/agents/test_relationship_context_unit2.py` (+ runtime-truth consistency and fail-closed tests)
- Unit 1 harness regression retained green
- Ledger + grant reconciliation for PR #10 merge + Unit 2 start

## Explicit non-delivery (by design / stop gate)

- Follow-Up Planning Agent
- Full `meeting_follow_up_packet_v1` end-to-end assembly under Gemini/ADK
- Live GHL reads/writes
- Broad CRM search beyond fixture-bound offline resolution
- L3A promotion, Firestore writes, deployment, IAM/secret mutation
- Deterministic policy bypass

## Validation commands

```bash
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 -m agents.meeting_context --provider fixture
PYTHONPATH=src python3 -m agents.meeting_context --provider gemini_adk_stub
PYTHONPATH=src python3 -m agents.relationship_context
PYTHONPATH=src python3 -m agents.adk_runtime
git diff --check
```

## STOP

`STOP_CODE=PHASE3_UNIT2_REPAIR_READY_FOR_REVIEW`
