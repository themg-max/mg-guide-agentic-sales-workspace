# Phase 3 Unit 2 Closeout — Google ADK runtime + Relationship Context Agent

| Field | Value |
| --- | --- |
| Grant | `MG_GUIDE_PHASE3_GEMINI_ADK_VERTICAL_SLICE_V1` |
| Ledger | NW-004 |
| Branch | `feat/meeting-follow-up-v1-adk-relationship-context-unit2` |
| Public PR | #11 |
| Unit 1 baseline | PR #10 **MERGED** @ `469ae3ba9962895bd77bebb9e5b2b44a8faac6e7` |
| Unit | Google ADK runtime orchestration + Relationship Context Agent |
| Status | **COMPLETE / TESTS GREEN** (stop before merge) |
| Grant execution_status | `IN_PROGRESS_UNIT2` |
| Stop before | Follow-Up Planning Agent |
| Evidence head | `b37247aba390080ee3acd7d4f971b53d47fa695e` (pre-binding) |
| CI | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31612017121 **SUCCESS** |

## Proof assertions

```text
GOOGLE_ADK_RUNTIME_STARTED=YES
ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED
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

## Architecture (Unit 2 stop gate)

```text
synthetic transcript
  -> Meeting Context Agent (reused from Unit 1)
  -> Google ADK runtime orchestration
  -> Relationship Context Agent
  -> Phase 2B offline GHL adapter
  -> synthetic contact/opportunity context
  -> relationship_context_v1
  -> STOP  (Follow-Up Planning Agent not invoked)
```

## Sponsor-tech precision

| Claim | Unit 2 truth |
| --- | --- |
| Unit 1 Meeting Context provider surface | **Unchanged** (`COMPATIBLE_SURFACE_ONLY` / provider-level ADK runtime = NO) |
| Google ADK runtime orchestration | **Started** (`GOOGLE_ADK_RUNTIME_STARTED=YES`) |
| ADK integration | **RUNTIME_INTEGRATED** (local ADK-compatible backend default; optional `google-adk` bind) |
| Relationship Context Agent | **Implemented** against synthetic CRM only |
| Offline GHL adapter | **Used** (Phase 2B; no transport / no live calls) |

## Delivered

- `src/agents/adk_runtime/**` — multi-agent sequential runtime, session/trace, markers
- `src/agents/relationship_context/**` — agent, resolver, synthetic CRM store, schema validation, harness
- `contracts/relationship_context.schema.json`
- `fixtures/ghl/relationship-context-crm.json`
- `tests/agents/test_relationship_context_unit2.py`
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

`STOP_CODE=PHASE3_UNIT2_ADK_RELATIONSHIP_CONTEXT_READY_FOR_REVIEW`
