# NW-008 Tranche A — Proof Manifest

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Purpose | DETERMINISTIC_ACCEPTANCE_EVIDENCE_SUBSTRATE |
| Execution unit | TRANCHE_A |
| Execution mode | OFFLINE_SYNTHETIC_ACCEPTANCE_EVIDENCE |
| Implementation subject SHA | `e77c2ce42bdda4fdc049990d56d43958f49af73c` |
| Generated at (fixture clock) | `2026-08-14T12:00:00Z` |
| GHL_LIVE_CALLS_AUTHORIZED | NO |
| GHL_WRITES_AUTHORIZED | NO |
| FIRESTORE_WRITES_AUTHORIZED | NO |
| NW013_EXECUTION_IN_SCOPE | NO |
| DEPLOYMENT_AUTHORIZED | NO |
| REAL_CUSTOMER_DATA | FORBIDDEN |
| RAW_REST | FORBIDDEN |
| DETERMINISTIC_SUPPORTING_PROOFS | AT-2, AT-4, AT-5 |
| PARTIAL_SUPPORTING_PROOFS | AT-8, AT-9 |
| HISTORICAL_AT_COMPLETE | NONE |
| NEXT_FUTURE_TRANCHE | LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY |

## AT map

| AT | Historical clauses | Evidence path | Clause status | Completion classification | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| AT-2 | blocked, AMBIGUOUS_CONTACT, 0_CRM_writes, MG_Guide_blocked_State_2_equivalent_decision_card | `proof/nw008/at-02/evidence.json` | blocked=PASS, AMBIGUOUS_CONTACT=PASS, 0_CRM_writes=PASS, MG_Guide_blocked_State_2_equivalent_decision_card=PASS | DETERMINISTIC_ACCEPTANCE_SUPPORTING_PROOF / HISTORICAL_AT_COMPLETE=NO | FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_NOT_YET_EVIDENCED |
| AT-4 | CONTACT_NOT_FOUND, blocked, 0_writes | `proof/nw008/at-04/evidence.json` | CONTACT_NOT_FOUND=PASS, blocked=PASS, 0_writes=PASS | DETERMINISTIC_ACCEPTANCE_SUPPORTING_PROOF / HISTORICAL_AT_COMPLETE=NO | FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_NOT_YET_EVIDENCED |
| AT-5 | extraction_below_threshold, LOW_EXTRACTION_CONFIDENCE, blocked, 0_writes | `proof/nw008/at-05/evidence.json` | extraction_below_threshold=PASS, LOW_EXTRACTION_CONFIDENCE=PASS, blocked=PASS, 0_writes=PASS | DETERMINISTIC_ACCEPTANCE_SUPPORTING_PROOF / HISTORICAL_AT_COMPLETE=NO | FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_NOT_YET_EVIDENCED |
| AT-8 | policy_cap_configuration_verified, single_intent_bound_behavior_verified, offline_second_attempt_model | `proof/nw008/at-08/evidence.json` | policy_cap_configuration_verified=PASS, single_intent_bound_behavior_verified=PASS, offline_second_attempt_model=PASS | PARTIAL_SUPPORTING_PROOF / HISTORICAL_AT_COMPLETE=NO | active authoritative mutation-execution trace showing the second attempt is refused by policy rather than agent choice or harness simulation |
| AT-9 | tool_manifest_refusal_offline | `proof/nw008/at-09/evidence.json` | tool_manifest_refusal_offline=PASS | PARTIAL_SUPPORTING_PROOF / HISTORICAL_AT_COMPLETE=NO | durable audit warning under an authorized audit sink |

## Not executed in Tranche A

| Class | ATs |
| --- | --- |
| BLOCKED_NOT_EXECUTED | AT-1, AT-3, AT-6, AT-7 |
| DEFERRED_NOT_EXECUTED | AT-10 |

## Source-authority separation

1. `AUTHORITATIVE_WORKFLOW_REASON` — WorkflowRunner / policy / contracts
2. `DECISION_CARD_PRESENTATION` — NW-007 mapper (fail-closed for unnamed reasons)
3. `HISTORICAL_AT_COMPLETION` — unchanged foundation §17 clauses only

NW-007 decision-card reason semantics were **not** expanded in this tranche.
