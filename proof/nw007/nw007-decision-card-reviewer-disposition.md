# NW-007 Decision Card Reviewer Disposition — DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1

| Field | Value |
| --- | --- |
| verdict | **BLOCKED_AWAITING_HUMAN_MERGE_REVIEW** |
| confidence | HIGH (technical evidence complete; merge authority reserved to human reviewer) |
| commit_sha | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| checked_at | 2026-08-14 |
| ci_state | SUCCESS (exact-head run `31787424303`) |
| artifacts_present | implementation packet (plan) / proof-return / proof-manifest / reviewer-disposition (this file) / required-check convention record |
| scope_result | PASS — PR #37 contains only the eight authorized decision-card paths |
| proof_mapping | `proof/nw007/nw007-decision-card-proof-manifest.md` (NW007-01 … NW007-10 all PASS) |
| static_scan_summary | PASS — authorized-path secret-pattern scan in CI run `31787424303`; no raw CRM IDs rendered (test-asserted) |
| required_human_actions | Human reviewer must issue the merge verdict on PR #37 and perform any merge; required-check policy remains convention-level (human governance may optionally ratify) |
| evidence_links | PR #37; Actions run `31787424303`; plan `proof/nw007/nw007-demo-grade-workflow-narrative-policy-planning.md`; proof manifest `proof/nw007/nw007-decision-card-proof-manifest.md`; proof return `proof/nw007/nw007-decision-card-proof-return.yaml` |
| ci_status_source | GitHub Actions API + `gh pr checks 37` (Phase 1 deterministic validation: pass) |
| harness_output | targeted 22 passed; card suite 50 passed; full suite 233 passed (exact head) |
| static_scan_output | PASS (authorized-path secret-pattern scan; HTML escaping tests; no CRM ID leakage tests) |
| conflict_scan | NONE — no conflicting authoritative artifact found for NW-007 decision card |
| evidence_manifest | `proof/nw007/nw007-decision-card-proof-manifest.md` |
| blocking_reason | Awaiting human merge-review verdict on PR #37; repo-wide required-check policy exists only as convention (no formal policy artifact), which does not block merge but is recorded |
| human_summary | Technical repair complete and fully evidenced; independent reviewer can legitimately determine READY_FOR_MERGE |
| machine_result | ALL_AUTOMATED_EVIDENCE_PASS |
| orchestrator_note | This disposition intentionally does NOT set READY_FOR_MERGE; that verdict belongs to the independent human reviewer |

## Verification basis

All claims in this disposition are bound to exact head
`22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` and exact GitHub Actions run
`31787424303`. The pre-repair head `33eae722aeee10c8efadac777009f3e56d8cb22f`
is retained as historical `PRE_REPAIR_HEAD` only.

## MG MCP discoverability

```text
MG_MCP_DISCOVERABILITY=UNKNOWN
```

UNKNOWN: expected MG MCP context was not surfaced for NW-007 / PR #37.
Action: run targeted search/alias/index validation for NW007,
DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1, and PR #37.

## STOP

```text
STOP_CODE=NW007_DECISION_CARD_DISPOSITION_RECORDED_AWAITING_HUMAN_MERGE_REVIEW
```
