# Phase 3 Unit 2 Closeout — Google ADK runtime + Relationship Context Agent

| Field | Value |
| --- | --- |
| Grant | `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` |
| Ledger | NW-004 |
| Branch | `feat/meeting-follow-up-v1-adk-relationship-context-unit2` |
| Public PR | #11 **MERGED** |
| Unit 1 baseline | PR #10 **MERGED** @ `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7` |
| Unit | Google ADK runtime orchestration + Relationship Context Agent |
| Status | **MERGED_COMPLETE** |
| Grant execution_status | `IN_PROGRESS_UNIT2_COMPLETE` |
| Public head SHA | `3ab0b1dfa0c2c20a711156d5cf88febb5d21dbfa` |
| Public merge SHA | `a3d5a5731d7342463fe365e597e5d974d3420d08` |
| Final CI | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31616758231 **SUCCESS** |
| Stop before (Unit 2) | Follow-Up Planning Agent |
| Next Phase 3 unit | Follow-Up Planning Agent (implementation not started) |

## Merge closeout

PR #11 merged to public `main` after sponsor-tech truth repair and final README
GHL environment reconciliation. Unit 2 delivered Google ADK package runtime
orchestration and the Relationship Context Agent against offline synthetic CRM
only. External effects remained 0. Follow-Up Planning Agent was **not** part of
Unit 2.

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
PHASE3_UNIT2_STATUS=MERGED_COMPLETE
PUBLIC_PR11_MERGE_SHA=a3d5a5731d7342463fe365e597e5d974d3420d08
```

## Scenario results

| Scenario | Transcript fixture | Expected status | Result |
| --- | --- | --- | --- |
| `RELATIONSHIP_MATCH` | `transcript-success` | `matched` | **PASS** |
| `AMBIGUOUS_CONTACT` | `transcript-ambiguous-contact` | `ambiguous` | **PASS** |
| `NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT` | `transcript-no-stage-change` | `opportunity_missing` | **PASS** |
| `AMBIGUOUS_OPPORTUNITY` | `transcript-ambiguous-opportunity` | `opportunity_ambiguous` | **PASS** |

## Architecture (Unit 2 delivered)

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
| Google ADK runtime orchestration | **Started** via actual `google.adk` package primitives and **merged** |
| ADK integration | **RUNTIME_INTEGRATED** with `ADK_RUNTIME_BACKEND=google_adk_package`; no local fallback |
| Relationship Context Agent | **Implemented** against synthetic CRM only |
| Offline GHL adapter | **Used** (Phase 2B; no transport / no live calls) |
| Follow-Up Planning Agent | **Not delivered** in Unit 2 |

## Delivered

- `src/agents/adk_runtime/**` — google.adk Runner/SequentialAgent/BaseAgent orchestration, session/trace, derived markers
- `src/agents/relationship_context/**` — agent, fail-closed resolver (incl. ambiguous-opportunity), synthetic CRM store, schema validation, harness
- `contracts/relationship_context.schema.json` (+ `opportunity_ambiguous` status)
- `contracts/failure_codes.yaml` (+ `AMBIGUOUS_OPPORTUNITY`)
- `fixtures/ghl/relationship-context-crm.json` (+ multi-opportunity synthetic contact)
- `fixtures/transcript-ambiguous-opportunity.{txt,expected.json}`
- `tests/agents/test_relationship_context_unit2.py` (+ runtime-truth consistency and fail-closed tests)
- Unit 1 harness regression retained green
- Ledger + grant reconciliation for PR #11 merge

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

## Next

Unit 3 candidate: Follow-Up Planning Agent. Bounded implementation packet:
[`../unit3/unit3-implementation-packet.md`](../unit3/unit3-implementation-packet.md).
Implementation not started in this closeout.

## STOP

`STOP_CODE=PHASE3_UNIT2_CLOSED_UNIT3_PLAN_READY_FOR_REVIEW`
