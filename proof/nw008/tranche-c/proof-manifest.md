# NW-008 Tranche C — Proof Manifest

| Field | Value |
| --- | --- |
| Execution unit | TRANCHE_C |
| Purpose | HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY |
| Implementation subject SHA | `06aee0392b30bf1515bf9c59a07b1463a8ec23cd` |
| Transcript source contract | TRANSCRIPT_SOURCE_ENVELOPE_V1 |
| Targets | AT-2, AT-4, AT-5 |
| Excludes | AT-8, AT-9 |

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
| TC-01 | PASS | AT-2 envelope entered fleet via TRANSCRIPT_SOURCE_ENVELOPE_V1; envelope hash 918490426de1f35b2a70b117dab878ef10fed926a359fb3816d28c5b19895dc5 |
| TC-02 | PASS | AT-2 AGENTS_STARTED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-03 | PASS | AT-2 STOP_POINT=relationship_context_agent, STOP_REASON_CODE=AMBIGUOUS_CONTACT, disposition=blocked, CRM_WRITES=0 |
| TC-04 | PASS | AT-2 AGENTS_COMPLETED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent']; downstream agents completed but produced no actionable output after the governed boundary |
| TC-05 | PASS | AT-2 POLICY_BYPASS=False, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 |
| TC-06 | PASS | AT-4 envelope entered fleet via TRANSCRIPT_SOURCE_ENVELOPE_V1; envelope hash c5b645af3f30d172928266483ea3a97ac90afb5de03f2fe0c2c8e69efcf63eae |
| TC-07 | PASS | AT-4 AGENTS_STARTED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-08 | PASS | AT-4 STOP_POINT=relationship_context_agent, STOP_REASON_CODE=CONTACT_NOT_FOUND, disposition=blocked, CRM_WRITES=0 |
| TC-09 | PASS | AT-4 AGENTS_COMPLETED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent']; downstream agents completed but produced no actionable output after the governed boundary |
| TC-10 | PASS | AT-4 POLICY_BYPASS=False, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 |
| TC-11 | PASS | AT-5 envelope entered fleet via TRANSCRIPT_SOURCE_ENVELOPE_V1; envelope hash 775d6f0998b8421f44f094eb40570e61469c3d56135d1eb8125b8beb1275c67f |
| TC-12 | PASS | AT-5 AGENTS_STARTED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent'] |
| TC-13 | PASS | AT-5 STOP_POINT=meeting_context_agent, STOP_REASON_CODE=LOW_EXTRACTION_CONFIDENCE, disposition=blocked, CRM_WRITES=0 |
| TC-14 | PASS | AT-5 AGENTS_COMPLETED: ['meeting_context_agent', 'relationship_context_agent', 'follow_up_planning_agent']; downstream agents completed but produced no actionable output after the governed boundary |
| TC-15 | PASS | AT-5 POLICY_BYPASS=False, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 |
| TC-16 | PASS | Existing fleet entrypoints reused; no new agent or parallel orchestration engine |
| TC-17 | PASS | Deterministic fixture/provider mode; replay produces identical agent trace and reason codes |
| TC-18 | PASS | Synthetic-only envelopes: contains_real_customer_data=false, permitted_for_public_proof=true, approved example-demo.test domain |
| TC-19 | PASS | Historical AT definitions unchanged (foundation §17 verbatim) |
| TC-20 | PASS | source, ownership, access_context, and provenance preserved in proof record |
| TC-21 | PASS | All envelopes set treat_content_as_data_only=true and instruction_authority=false |
| TC-22 | PASS | Historical completion claims match unchanged AT clauses; no over-claim |

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

- **AT-2**: CANDIDATE — Blocked with AMBIGUOUS_CONTACT; 0 CRM writes; MG Guide card State 2 rendered=True. Historical completion candidacy pending review.
- **AT-4**: CANDIDATE — Blocked with CONTACT_NOT_FOUND; 0 CRM writes; NW007 card semantics unchanged. Historical completion candidacy pending review.
- **AT-5**: CANDIDATE — Blocked with LOW_EXTRACTION_CONFIDENCE; 0 CRM writes; NW007 card semantics unchanged. Historical completion candidacy pending review.
