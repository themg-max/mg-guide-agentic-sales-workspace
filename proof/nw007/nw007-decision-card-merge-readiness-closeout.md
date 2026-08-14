# NW-007 Decision Card Merge-Readiness Closeout — Final merged state

| Field | Value |
| --- | --- |
| Repository | `themg-max/mg-guide-agentic-sales-workspace` |
| Work item | NW-007 lane deliverable: DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1 |
| Public PR | #37 — `feat(nw007): DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1 bounded implementation` |
| Public PR state | **MERGED** |
| Merge SHA | `f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6` |
| Merged at (UTC) | `2026-08-14T09:35:35Z` |
| Exact reviewed head SHA | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| Pre-repair head (historical) | `33eae722aeee10c8efadac777009f3e56d8cb22f` |
| Exact-head CI run | **31787424303** SUCCESS |
| Governance closeout PR | #38 — `docs(nw007): decision-card governance closeout + merge-readiness evidence for PR #37` |
| Governance closeout merge SHA | `89302057a7dddf2410f8aedbfb1f6c4e0ea88238` |
| Governance closeout merged at (UTC) | `2026-08-14T09:36:28Z` |
| Implementation branch | `impl/nw007-demo-grade-follow-up-decision-card` |
| Plan authority | `f303d0775899ee755bb68636d7c425045d18b357` (frozen authorized planning contract) |
| Status | **MERGED_COMPLETE** |
| External effects | **0** |
| Deployment authorization | **NO** |

## Canonical GitHub binding (final merged truth)

```text
NW007_DECISION_CARD_STATUS=MERGED_COMPLETE
NW007_DECISION_CARD_PR=37
NW007_DECISION_CARD_FINAL_REVIEWED_HEAD=22a3b0b3c20373100ca0158cda7a74b4fbc1fb76
NW007_DECISION_CARD_MERGE_SHA=f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6
NW007_DECISION_CARD_MERGED_AT=2026-08-14T09:35:35Z
NW007_DECISION_CARD_PRE_REPAIR_HEAD=33eae722aeee10c8efadac777009f3e56d8cb22f
NW007_DECISION_CARD_EXACT_HEAD_CI_RUN=31787424303
NW007_DECISION_CARD_EXACT_HEAD_CI_RESULT=SUCCESS
NW007_GOVERNANCE_CLOSEOUT_PR=38
NW007_GOVERNANCE_CLOSEOUT_MERGE_SHA=89302057a7dddf2410f8aedbfb1f6c4e0ea88238
NW007_GOVERNANCE_CLOSEOUT_MERGED_AT=2026-08-14T09:36:28Z
EXTERNAL_EFFECTS=0
POLICY_SEMANTICS_CHANGE=NO
PACKET_SCHEMA_CHANGE=NO
ADK_ORCHESTRATION_CHANGE=NO
NEW_AGENT=NO
NEW_LLM_CALL=NO
CLOUD_MUTATION=NONE
DEPLOYMENT_AUTHORIZATION=NO
DEPLOYMENT_PERFORMED=NO
```

These values are bound to the exact GitHub merge facts for PR #37 and PR #38.
They are not silently revised. If either head moves away from the recorded
exact-sha truth, the durable record must be refreshed.

## What the merged implementation contains

The merged PR #37 contains only the eight authorized decision-card files and the
corresponding tests under the existing `meeting_follow_up_card` domain:

```text
src/mg_guide/meeting_follow_up_card/decision_models.py
src/mg_guide/meeting_follow_up_card/decision_mapper.py
src/mg_guide/meeting_follow_up_card/decision_render_text.py
src/mg_guide/meeting_follow_up_card/decision_render_html.py
tests/mg_guide/meeting_follow_up_card/test_decision_mapper_three_scenarios.py
tests/mg_guide/meeting_follow_up_card/test_decision_render_text.py
tests/mg_guide/meeting_follow_up_card/test_decision_render_html.py
tests/mg_guide/meeting_follow_up_card/test_decision_unknown_state_fail_closed.py
```

## Final correctness summary

```text
CARD_INPUT_CONTRACT=meeting_follow_up_packet_v1
CARD_MAPPER=deterministic
CARD_POLICY_REEVAL=NO
CARD_AGENT_RERUN=NO
CARD_CRM_FETCH=NO
CARD_MUTATION_CONTROLS=NONE
CARD_DEPLOYMENT=NO
EXTERNAL_EFFECTS=0
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS_CONST_ZERO_ENFORCED=PASS
UNKNOWN_STATUS_REFLECTED=NO
AGENT_AUDIT_WORDING_SAFE=PASS
MALFORMED_REASON_CODES_FAIL_CLOSED=PASS
INCONSISTENT_STATE_REASON_FAIL_CLOSED=PASS
UNKNOWN_REASON_REFLECTED=NO
UNKNOWN_AGENT_REFLECTED=NO
RAW_CRM_ID_RENDERED=NO
POLICY_SEMANTICS_CHANGE=NO
ADK_ORCHESTRATION_CHANGE=NO
PACKET_SCHEMA_CHANGE=NO
NEW_AGENT=NO
NEW_LLM_CALL=NO
CLOUD_MUTATION=NONE
DEPLOYMENT_PERFORMED=NO
```

Full obligation-level proof mapping:
[`nw007-decision-card-proof-manifest.md`](./nw007-decision-card-proof-manifest.md).

## Explicit non-claims

- This closeout does **not** authorize new deployment, CRM mutation, GHL writes,
  Firestore writes, or live external integration.
- This closeout does **not** change policy semantics, orchestration, packet
  schema, or agent registry.
- This closeout does **not** mark AT-1…AT-10 complete for NW-008; readiness is a
  separate planning gate.

## Related artifacts

| Artifact | Role |
| --- | --- |
| [`nw007-demo-grade-workflow-narrative-policy-planning.md`](./nw007-demo-grade-workflow-narrative-policy-planning.md) | Frozen authorized planning contract |
| [`nw007-decision-card-proof-manifest.md`](./nw007-decision-card-proof-manifest.md) | Obligation-level proof mapping |
| [`nw007-decision-card-proof-return.yaml`](./nw007-decision-card-proof-return.yaml) | Machine-readable proof return |
| [`nw007-decision-card-reviewer-disposition.md`](./nw007-decision-card-reviewer-disposition.md) | Durable reviewer disposition record |
| [`nw007-merge-closeout.md`](./nw007-merge-closeout.md) | Final merged-state closeout summary |

## MG MCP discoverability

```text
MG_MCP_DISCOVERABILITY=UNKNOWN
```

UNKNOWN: expected MG MCP context was not surfaced for NW-007 / PR #37.
Action: run targeted search/alias/index validation for NW007,
DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1, and PR #37.

## Validation summary

- GitHub truth: PR #37 merged at `2026-08-14T09:35:35Z` with merge SHA
  `f0fe64f1ed1ddab7adb0252ccd4aabb74fe65aa6`.
- Governance closeout PR #38 merged at `2026-08-14T09:36:28Z` with merge SHA
  `89302057a7dddf2410f8aedbfb1f6c4e0ea88238`.
- Decision-card technical proof remains bounded to the approved implementation
  paths and the exact-head CI run `31787424303`.
- No infrastructure, IAM, cloud, or deployment files changed in the merge.

## STOP

```text
STOP_CODE=NW007_MERGED_COMPLETE_NW008_READINESS_REFRESH_READY_FOR_REVIEW
```
