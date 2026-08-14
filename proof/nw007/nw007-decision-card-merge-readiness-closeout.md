# NW-007 Decision Card Merge-Readiness Closeout — PR #37

| Field | Value |
| --- | --- |
| Repository | `themg-max/mg-guide-agentic-sales-workspace` |
| Work item | NW-007 lane deliverable: DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1 |
| Public PR | #37 — `feat(nw007): DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1 bounded implementation` |
| Public PR state | **OPEN** (not merged) |
| Exact reviewed head SHA | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| Pre-repair head (historical) | `33eae722aeee10c8efadac777009f3e56d8cb22f` |
| Final exact-head CI run | **31787424303** SUCCESS |
| Implementation branch | `impl/nw007-demo-grade-follow-up-decision-card` |
| Plan authority | `f303d0775899ee755bb68636d7c425045d18b357` (frozen authorized planning contract) |
| Status | **TECHNICAL_REPAIR_COMPLETE — READY_FOR_FINAL_MERGE_REVIEW** |
| External effects | **0** |
| Deployment authorization | **NO** |

## Canonical GitHub binding (exact reviewed tip)

```text
NW007_DECISION_CARD_STATUS=TECHNICAL_REPAIR_COMPLETE
NW007_DECISION_CARD_PR=37
NW007_DECISION_CARD_FINAL_REVIEWED_HEAD=22a3b0b3c20373100ca0158cda7a74b4fbc1fb76
NW007_DECISION_CARD_EXACT_HEAD_CI_RUN=31787424303
NW007_DECISION_CARD_EXACT_HEAD_CI_RESULT=SUCCESS
NW007_DECISION_CARD_PRE_REPAIR_HEAD=33eae722aeee10c8efadac777009f3e56d8cb22f
EXTERNAL_EFFECTS=0
PR37_STATE=OPEN
PR37_MERGEABLE=MERGEABLE
PR37_MERGE_STATE=CLEAN
```

These values are truth-bound to verified GitHub facts for PR #37 at record time
and must not be silently rewritten. If the PR head moves off
`22a3b0b3c20373100ca0158cda7a74b4fbc1fb76`, this closeout is stale and the
reviewer evidence must be regenerated.

## What the implementation contains (scope preserved)

PR #37 contains exactly the eight authorized decision-card files and nothing
else (verified via `git diff main...HEAD --name-only`):

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

## Proof assertions retained

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

Full obligation-level mapping with per-obligation evidence:
[`nw007-decision-card-proof-manifest.md`](./nw007-decision-card-proof-manifest.md).

## Scope boundaries preserved

- The decision card **renders** deterministic policy outcomes already present
  on the packet; it does not re-evaluate policy, rerun agents, fetch CRM,
  write Firestore, deploy, or offer mutation controls.
- `external_effects` accepts only the canonical packet value (integer const
  `0`); every other value fails closed and renders as `unknown`.
- Unsupported workflow status values normalize to safe `unknown` and are never
  reflected into text or HTML.
- Agent audit wording is restricted to allowlisted fixed labels stating
  "present in packet audit"; no execution status is inferred.
- Unsupported reason codes and unknown agent identifiers are never rendered.

## Explicit non-claims

- This closeout does **not** merge PR #37.
- This closeout does **not** authorize deployment, CRM mutation, Firestore
  writes, live GHL, or private host integration.
- This closeout does **not** establish a repo-wide required-check policy;
  it records the existing convention (see below).
- NW-007 demo-grade decision-card completion does **not** mark AT-1…AT-10
  complete (see `proof/nw008/nw-008-readiness-matrix.md`).

## Required-check policy record (convention, not new policy)

```text
REQUIRED_CHECK_POLICY_PATH=NONE_FOUND_IN_REPO
REQUIRED_CHECK_POLICY_STATUS=CONVENTION_ONLY
CONVENTION_REQUIRED_CHECK=Phase 1 Deterministic CI — SUCCESS at exact reviewed head
```

Repository search found no authoritative repo-wide required-check policy
artifact. GitHub branch protection for `main` is **not configured**
(`gh api .../branches/main/protection` → 404). The durable repo convention,
recorded in `competition/NEW_WORK_LEDGER.md` and `proof/phase2/closeout-note.md`
and applied to every merged implementation PR to date, is: **Phase 1
Deterministic CI SUCCESS at the exact reviewed head + human review verdict**.

For PR #37 this convention is satisfied on evidence: run `31787424303` is
SUCCESS at exact head `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76`; the human
review verdict remains the outstanding reviewer action. No new policy is
created by this artifact, and this artifact cannot self-authorize a merge.

## Related artifacts

| Artifact | Role |
| --- | --- |
| [`nw007-demo-grade-workflow-narrative-policy-planning.md`](./nw007-demo-grade-workflow-narrative-policy-planning.md) | Frozen authorized planning contract (plan authority) |
| [`nw007-decision-card-proof-manifest.md`](./nw007-decision-card-proof-manifest.md) | Obligation-level proof mapping NW007-01…NW007-10 |
| [`nw007-decision-card-proof-return.yaml`](./nw007-decision-card-proof-return.yaml) | Machine-readable proof return (governance schema) |
| [`nw007-decision-card-reviewer-disposition.md`](./nw007-decision-card-reviewer-disposition.md) | Durable reviewer disposition (BLOCKED_AWAITING_HUMAN_MERGE_REVIEW) |

## MG MCP discoverability

```text
MG_MCP_DISCOVERABILITY=UNKNOWN
```

UNKNOWN: expected MG MCP context was not surfaced for NW-007 / PR #37.
Action: run targeted search/alias/index validation for NW007,
DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1, and PR #37.

## Validation summary (closeout documentation unit)

- No application source or test code changed in this closeout unit.
- PR #37 content unchanged; this closeout adds governance/proof artifacts only.
- Every artifact references exact PR head
  `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` and exact CI run `31787424303`.
- No infrastructure, IAM, cloud, or deployment files changed.

## STOP

```text
STOP_CODE=NW007_GOVERNANCE_CLOSEOUT_READY_FOR_FINAL_MERGE_REVIEW
```
