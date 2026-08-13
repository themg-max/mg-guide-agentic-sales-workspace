# NW-005 Stage A — Validation Summary

## Scope

Deterministic **offline** audit projection only:

```text
meeting_follow_up_packet_v1
  → validate
  → project_workflow_run_audit(packet, ProjectionContext)
  → workflow_run_audit_v1
  → validate
  → deterministic fingerprint / idempotency proof
  → STOP
```

No Firestore client SDK, no network, no CRM, no policy re-eval, no agent rerun,
no MG Guide card import, no Stage B.

## Baseline

| Field | Value |
| --- | --- |
| Branch | `feat/nw005-firestore-audit-stage-a` |
| Baseline SHA | `fa57a28a46e597807230b2e281e7dd3cd4bba477` (PR #17 merge) |
| PR17 final head | `4d3fb5b0d3333d107c8b48ac112645a6b7aa501e` |
| Implementation head (pre-proof-annotation) | `197574432c971f6b121e6f339cc236c413015f65` |
| Implementation head CI run | [run 31655056168](https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31655056168) **SUCCESS** |
| Final PR head (proof annotation head) | `e5519bf8d033ffc46c60efbcd51c56dc77ccffb8` |
| Exact-head CI (on final proof annotation head) | [run 31655138893](https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31655138893) **SUCCESS** |
| PR | https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/18 |

## Implementation surfaces

| Path | Role |
| --- | --- |
| `contracts/workflow_run_audit.schema.json` | `workflow_run_audit_v1` JSON Schema |
| `src/mg_guide/firestore_audit/models.py` | `ProjectionContext`, terminal constants |
| `src/mg_guide/firestore_audit/canonicalize.py` | `nw005_canonical_json_v1` (+ golden-byte tests) |
| `src/mg_guide/firestore_audit/project.py` | Pure projector + audit-local status mapper |
| `src/mg_guide/firestore_audit/validate.py` | Schema + invariant validation |
| `src/mg_guide/firestore_audit/memory_store.py` | Terminal-only in-memory store + idempotency |
| `fixtures/nw005/**` | Packets, contexts, golden expected audits |
| `tests/nw005/**` | Stage A offline tests |
| `proof/nw005/stage-a/**` | Proof-return + this summary |

## Validation commands

```bash
PYTHONPATH=src python3 -m pytest tests/nw005 -q
PYTHONPATH=src python3 -m pytest -q
git diff --check
```

| Check | Result |
| --- | --- |
| Targeted NW-005 pytest | **PASS** (41 tests) |
| Full pytest | **PASS** (162 tests) |
| `git diff --check` | **PASS** |

## Proof markers

```text
NW005_STAGE=A
AUDIT_SCHEMA_VALID=PASS
AUDIT_PROJECTION_DETERMINISTIC=PASS
AUDIT_CANONICALIZER=nw005_canonical_json_v1
AUDIT_PROJECTION_CONTEXT_EXPLICIT=PASS
AUDIT_TERMINAL_ONLY_PERSISTENCE=PASS
AUDIT_NON_TERMINAL_DURABLE_WRITE=NO
AUDIT_IDEMPOTENCY=PASS
AUDIT_IDEMPOTENCY_CONFLICT_FAILS_CLOSED=PASS
AUDIT_TERMINAL_STATE_CONFLICT_FAILS_CLOSED=PASS
AUDIT_POLICY_REEVAL=NO
AUDIT_AGENT_RERUN=NO
AUDIT_CRM_FETCH=NO
AUDIT_UI_RUNTIME_DEPENDENCY=NO
AUDIT_TRANSCRIPT_BODY_STORED=NO
AUDIT_TOOL_INVOCATION_COUNTS_AVAILABLE=NO
FIRESTORE_CLIENT_DEPENDENCY=NO
FIRESTORE_READS=0
FIRESTORE_WRITES=0
GHL_LIVE_CALLS=0
GHL_READS=0
GHL_WRITES=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS=0
NW005_STAGE_B_STATUS=NOT_AUTHORIZED
```

## Notes

- Canonicalization is **`nw005_canonical_json_v1`** (packet-local). **No RFC 8785 claim.**
- `ProjectionContext` supplies `recorded_at`, `fixture_id`, `source_refs`, writer identity — no internal clocks/env.
- `tools_listed_count` is `len(tools_used)` only — **not** an invocation count.
- Non-terminal packets may project locally; `MemoryAuditStore` refuses durable writes.
- Stage B / Firestore provisioning / IAM / deploy **not** started.

`STOP_CODE=NW005_STAGE_A_READY_FOR_PR_REVIEW`
