# NW-007 Decision Card Proof Manifest — DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1

| Field | Value |
| --- | --- |
| Repository | `themg-max/mg-guide-agentic-sales-workspace` |
| Feature | NW-007 — DEMO_GRADE_FOLLOW_UP_DECISION_CARD_V1 |
| Implementation PR | #37 |
| Exact reviewed PR head | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| Pre-repair head (historical) | `33eae722aeee10c8efadac777009f3e56d8cb22f` |
| Implementation branch | `impl/nw007-demo-grade-follow-up-decision-card` |
| Plan authority | `f303d0775899ee755bb68636d7c425045d18b357` (`proof/nw007/nw007-demo-grade-workflow-narrative-policy-planning.md`) |
| Implementation scope | the eight authorized decision-card implementation/test paths only |
| Exact-head CI run | `31787424303` — Phase 1 Deterministic CI — **SUCCESS** |

This manifest binds every NW-007 decision-card obligation to durable, checkable
evidence. No obligation below claims PASS on narrative alone; each PASS cites
either exact-head CI run `31787424303`, named tests at head
`22a3b0b3c20373100ca0158cda7a74b4fbc1fb76`, or exact `git diff main...HEAD`
scope output.

## Technical proof basis

```text
EXACT_HEAD_CI_RUN=31787424303
EXACT_HEAD_CI_RESULT=SUCCESS
EXACT_HEAD_CI_JOB=Phase 1 deterministic validation
EXACT_HEAD_CI_HEAD_SHA=22a3b0b3c20373100ca0158cda7a74b4fbc1fb76
DETERMINISTIC_PYTEST=PASS (full suite: 233 passed at exact head)
CARD_SUITE=PASS (50 passed)
TARGETED_DECISION_CARD_TESTS=PASS (22 passed)
PACKET_SCHEMA_VALIDATION=PASS (CI run 31787424303)
PROOF_RETURN_SCHEMA_VALIDATION=PASS (CI run 31787424303)
FIXTURE_OUTCOMES_INTENT_BOUNDS=PASS (CI run 31787424303)
REPLAY_IDEMPOTENCY=PASS (CI run 31787424303)
GIT_DIFF_CHECK=PASS
AUTHORIZED_PATH_SECRET_SCAN=PASS (CI run 31787424303)
```

## Final correctness flags

```text
EXTERNAL_EFFECTS_CONST_ZERO_ENFORCED=YES
UNKNOWN_STATUS_REFLECTED=NO
AGENT_AUDIT_WORDING_SAFE=YES
MALFORMED_REASON_CODES_FAIL_CLOSED=YES
INCONSISTENT_STATE_REASON_FAIL_CLOSED=YES
UNKNOWN_REASON_REFLECTED=NO
UNKNOWN_AGENT_REFLECTED=NO
RAW_CRM_ID_RENDERED=NO
```

## Boundary flags

```text
POLICY_SEMANTICS_CHANGE=NO
ADK_ORCHESTRATION_CHANGE=NO
PACKET_SCHEMA_CHANGE=NO
NEW_AGENT=NO
NEW_LLM_CALL=NO
CLOUD_MUTATION=NONE
DEPLOYMENT_PERFORMED=NO
DEPLOYMENT_AUTHORIZATION=NO
```

## Obligation map

| Obligation | Requirement | Status | Evidence | Commit |
| --- | --- | --- | --- | --- |
| NW007-01 | Atomic exact-tuple scenario classification | PASS | `decision_mapper._classify_scenario` recognizes only the three exact tuples; proven by `test_decision_mapper_three_scenarios.py::test_decision_mapper_three_scenarios` (3 cases) and `test_decision_unknown_state_fail_closed.py` (all non-tuple inputs fail closed); exact-head CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-02 | Unsupported/malformed reason-code combinations fail closed; unsupported values never judge-visible | PASS | `test_completed_with_malformed_reason_codes_fails_closed`, `test_known_reason_plus_unknown_reason_fails_closed_and_does_not_reflect`, `test_unknown_reason_containing_crm_style_identifier_is_not_reflected`, `test_unknown_reason_containing_html_markup_is_sanitized`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-03 | external_effects accepts only canonical integer const 0 | PASS | `decision_mapper._valid_external_effects` enforces `type(value) is int and value == 0` (bool excluded); renderers display only `"0"` for that exact value, else `unknown`; `test_external_effects_numeric_one_fails_closed`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-04 | Missing/malformed/nonzero external_effects fails closed and renders unknown | PASS | `test_success_tuple_with_missing_external_effects_fails_closed`, `test_success_tuple_with_malformed_external_effects_fails_closed_and_does_not_leak`, `test_external_effects_numeric_one_fails_closed`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-05 | Unsupported workflow status values normalize to safe "unknown" and are not reflected | PASS | `_normalize_workflow_status` allowlists the nine schema statuses; `_safe_workflow_status` in both renderers re-normalizes; `test_unsupported_status_string_is_sanitized_to_unknown_in_both_renderers`, `test_render_decision_card_html_escapes_untrusted_content`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-06 | Known agent IDs map only to fixed human labels with "present in packet audit" | PASS | `KNOWN_AGENT_LABELS` allowlist; contributions render exactly `"<Label> — present in packet audit"`; `test_agent_contributions_use_fixed_labels_only`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-07 | Unknown agent identifiers are not rendered | PASS | `test_unknown_agent_identifiers_are_not_printed`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-08 | CRM identifiers / arbitrary reason values are not rendered | PASS | `test_render_decision_card_text_includes_required_fields_without_crm_ids`, `test_render_decision_card_html_includes_required_fields_without_crm_ids`, `test_unknown_reason_containing_crm_style_identifier_is_not_reflected`; CI 31787424303 SUCCESS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-09 | No policy-semantic, packet-schema, ADK, agent, cloud, or deployment change | PASS | `git diff main...HEAD --name-only` returns exactly the eight authorized decision-card files and nothing else; CI 31787424303 authorized-path secret-pattern scan PASS | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |
| NW007-10 | Exact-head deterministic CI is green | PASS | GitHub Actions run 31787424303 (Phase 1 Deterministic CI) concluded SUCCESS on head `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76`; `gh pr checks 37` shows "Phase 1 deterministic validation" pass | `22a3b0b3c20373100ca0158cda7a74b4fbc1fb76` |

## Review conclusion

```text
NO_FURTHER_NW007_APPLICATION_CODE_REPAIR_IDENTIFIED=YES
```

## STOP

```text
STOP_CODE=NW007_DECISION_CARD_PROOF_MANIFEST_COMPLETE
```
