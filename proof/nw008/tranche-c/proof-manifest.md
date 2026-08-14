# NW-008 Tranche C — Proof Manifest

| Field | Value |
| --- | --- |
| Execution unit | TRANCHE_C |
| Purpose | HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY |
| Implementation subject SHA | `a8715dcdeaa58f8404766f39db4e4dea289f951e` |
| Transcript source contract | TRANSCRIPT_SOURCE_ENVELOPE_V1 |
| Targets | AT-2, AT-4, AT-5 |
| Excludes | AT-8, AT-9 |
| Deterministic replay | PASS |

## Entrypoints

- `MEETING_CONTEXT_ENTRYPOINT` = `agents.meeting_context.agent.MeetingContextAgent.run`
- `RELATIONSHIP_CONTEXT_ENTRYPOINT` = `agents.relationship_context.agent.RelationshipContextAgent.run`
- `FOLLOW_UP_PLANNING_ENTRYPOINT` = `agents.follow_up_planning.agent.FollowUpPlanningAgent.run`
- `ADK_RUNTIME_ENTRYPOINT` = `agents.follow_up_planning.runtime.Unit3FollowUpRuntime.run_unit3`
- `POLICY_ENTRYPOINT` = `orchestration.policy.evaluate_policy`
- `PACKET_ENTRYPOINT` = `agents.follow_up_planning.packet.FollowUpPacketAssembler.assemble`
- `DECISION_CARD_ENTRYPOINT` = `mg_guide.meeting_follow_up_card.decision_mapper.map_packet_to_decision_card`
- `TRANSCRIPT_SOURCE_ENTRYPOINT` = `orchestration.transcript_source.envelope_to_provider_request`

## Proof obligations

| ID | Status | Detail |
| --- | --- | --- |
| TC-01 | PASS | AT-2 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with TRANSCRIPT_CONTENT_HASH=918490426de1f35b2a70b117dab878ef10fed926a359fb3816d28c5b19895dc5 |
| TC-02 | PASS | AT-2 AGENTS_STARTED=['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-03 | PASS | AT-2 STOP_POINT=relationship_context_agent, STOP_REASON_CODE=AMBIGUOUS_CONTACT, DISPOSITION=blocked |
| TC-04 | PASS | AT-2 AGENT_STATUSES={'meeting_context_agent': 'ok', 'relationship_context_agent': 'BLOCK_ORIGIN', 'follow_up_planning_agent': 'SKIPPED_GOVERNED_STOP'}, AGENT_EXECUTION={'meeting_context_agent': {'wrapper_status': 'EXECUTED', 'delegate_called': True, 'block_origin': False}, 'relationship_context_agent': {'wrapper_status': 'BLOCK_ORIGIN', 'delegate_called': True, 'block_origin': True}, 'follow_up_planning_agent': {'wrapper_status': 'SKIPPED_GOVERNED_STOP', 'delegate_called': False, 'block_origin': False, 'skipped_by': 'relationship_context_agent'}} |
| TC-05 | PASS | AT-2 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, POLICY_BYPASS=False, EFFECT_COUNTERS={'GHL_LIVE_CALLS': 0, 'GHL_READS': 0, 'GHL_WRITES': 0, 'FIRESTORE_WRITES': 0, 'EXTERNAL_EFFECTS': 0, 'REAL_CUSTOMER_DATA': 0} |
| TC-06 | PASS | AT-4 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with TRANSCRIPT_CONTENT_HASH=c5b645af3f30d172928266483ea3a97ac90afb5de03f2fe0c2c8e69efcf63eae |
| TC-07 | PASS | AT-4 AGENTS_STARTED=['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-08 | PASS | AT-4 STOP_POINT=relationship_context_agent, STOP_REASON_CODE=CONTACT_NOT_FOUND, DISPOSITION=blocked |
| TC-09 | PASS | AT-4 AGENT_STATUSES={'meeting_context_agent': 'ok', 'relationship_context_agent': 'BLOCK_ORIGIN', 'follow_up_planning_agent': 'SKIPPED_GOVERNED_STOP'}, AGENT_EXECUTION={'meeting_context_agent': {'wrapper_status': 'EXECUTED', 'delegate_called': True, 'block_origin': False}, 'relationship_context_agent': {'wrapper_status': 'BLOCK_ORIGIN', 'delegate_called': True, 'block_origin': True}, 'follow_up_planning_agent': {'wrapper_status': 'SKIPPED_GOVERNED_STOP', 'delegate_called': False, 'block_origin': False, 'skipped_by': 'relationship_context_agent'}} |
| TC-10 | PASS | AT-4 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, POLICY_BYPASS=False, EFFECT_COUNTERS={'GHL_LIVE_CALLS': 0, 'GHL_READS': 0, 'GHL_WRITES': 0, 'FIRESTORE_WRITES': 0, 'EXTERNAL_EFFECTS': 0, 'REAL_CUSTOMER_DATA': 0} |
| TC-11 | PASS | AT-5 TRANSCRIPT_SOURCE_ENVELOPE_V1 accepted with TRANSCRIPT_CONTENT_HASH=775d6f0998b8421f44f094eb40570e61469c3d56135d1eb8125b8beb1275c67f |
| TC-12 | PASS | AT-5 AGENTS_STARTED=['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-13 | PASS | AT-5 STOP_POINT=meeting_context_agent, STOP_REASON_CODE=LOW_EXTRACTION_CONFIDENCE, DISPOSITION=blocked |
| TC-14 | PASS | AT-5 AGENT_STATUSES={'meeting_context_agent': 'BLOCK_ORIGIN', 'relationship_context_agent': 'SKIPPED_GOVERNED_STOP', 'follow_up_planning_agent': 'SKIPPED_GOVERNED_STOP'}, AGENT_EXECUTION={'meeting_context_agent': {'wrapper_status': 'BLOCK_ORIGIN', 'delegate_called': True, 'block_origin': True}, 'relationship_context_agent': {'wrapper_status': 'SKIPPED_GOVERNED_STOP', 'delegate_called': False, 'block_origin': False, 'skipped_by': 'meeting_context_agent'}, 'follow_up_planning_agent': {'wrapper_status': 'SKIPPED_GOVERNED_STOP', 'delegate_called': False, 'block_origin': False, 'skipped_by': 'meeting_context_agent'}} |
| TC-15 | PASS | AT-5 PRE_POLICY_FAIL_CLOSED=true, POLICY_GATE_INVOKED=false, POLICY_BYPASS=False, EFFECT_COUNTERS={'GHL_LIVE_CALLS': 0, 'GHL_READS': 0, 'GHL_WRITES': 0, 'FIRESTORE_WRITES': 0, 'EXTERNAL_EFFECTS': 0, 'REAL_CUSTOMER_DATA': 0} |
| TC-16 | PASS | Existing fleet entrypoints reused; no new runtime agent IDs observed |
| TC-17 | PASS | Deterministic replay result=PASS |
| TC-18 | PASS | Synthetic-only envelope invariants verified from fixture envelopes |
| TC-19 | PASS | canonical AT-2/AT-4/AT-5 definitions verified in contracts/workflow_states.yaml |
| TC-20 | PASS | TRANSCRIPT_CONTENT_HASH and ENVELOPE_DIGEST verified; source/ownership/access_context/provenance preserved |
| TC-21 | PASS | All envelopes enforce treat_content_as_data_only=true and instruction_authority=false |
| TC-22 | PASS | AT-2 State-2-equivalent card semantics: policy_state=BLOCKED, policy_reason_code=AMBIGUOUS_CONTACT, next_action=RESOLVE_CONTACT |

## Effect counters

- `GHL_LIVE_CALLS` = `0`
- `GHL_READS` = `0`
- `GHL_WRITES` = `0`
- `FIRESTORE_WRITES` = `0`
- `EXTERNAL_EFFECTS` = `0`
- `REAL_CUSTOMER_DATA` = `0`
- `NW013_EXECUTED` = `NO`
- `DEPLOYMENT_PERFORMED` = `NO`

## Historical AT claims

- **AT-2**: CANDIDATE — Blocked with AMBIGUOUS_CONTACT; PRE_POLICY_FAIL_CLOSED=true; State2Equivalent=true.
- **AT-4**: CANDIDATE — Blocked with CONTACT_NOT_FOUND; PRE_POLICY_FAIL_CLOSED=true; NW007 card semantics unchanged.
- **AT-5**: CANDIDATE — Blocked with LOW_EXTRACTION_CONFIDENCE; PRE_POLICY_FAIL_CLOSED=true; NW007 card semantics unchanged.

## Card evidence source

- `AT2_CARD_EVIDENCE_SOURCE` = `GOVERNED_STOP_PROOF_PROJECTION_THROUGH_EXISTING_NW007_MAPPER`
- `NW007_CARD_SEMANTICS_CHANGE` = `NO`
