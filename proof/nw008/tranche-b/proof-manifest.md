# NW-008 Tranche B — Proof Manifest

| Field | Value |
| --- | --- |
| Execution unit | TRANCHE_B |
| Purpose | LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY |
| Implementation subject SHA | `27edac20756518257a54492487fb09bfb3b88576` |
| Meeting 1 fixture | `fixtures/nw008/tranche_b/meeting-1.expected.json` |
| Meeting 2 fixture | `fixtures/nw008/tranche_b/meeting-2.expected.json` |
| Meeting 1 hash | `7694ec62ddeb06a82811b334c9891f69917bac379d52f676585c576ad1f82d90` |
| Meeting 2 hash | `f7272b32e6298c767a962caf9a443ebc1e4a28070adfb781d45709a963324496` |
| Actual agent chain executed | `True` |
| Prior context retrieved | `True` |
| Deterministic replay | `PASS` |

## Entrypoints

- `MEETING_CONTEXT_ENTRYPOINT` = `agents.meeting_context.agent.MeetingContextAgent.run`
- `RELATIONSHIP_CONTEXT_ENTRYPOINT` = `agents.relationship_context.agent.RelationshipContextAgent.run`
- `FOLLOW_UP_PLANNING_ENTRYPOINT` = `agents.follow_up_planning.agent.FollowUpPlanningAgent.run`
- `ADK_RUNTIME_ENTRYPOINT` = `agents.follow_up_planning.runtime.Unit3FollowUpRuntime.run_unit3`
- `POLICY_ENTRYPOINT` = `orchestration.policy.evaluate_policy`
- `PACKET_ENTRYPOINT` = `agents.follow_up_planning.packet.FollowUpPacketAssembler.assemble`
- `DECISION_CARD_ENTRYPOINT` = `mg_guide.meeting_follow_up_card.decision_mapper.map_packet_to_decision_card`

## Proof obligations

| ID | Status | Evidence path | Detail | Remaining gap |
| --- | --- | --- | --- | --- |
| TB-01 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | Both synthetic meetings were accepted through the real Unit 3 runtime path. | none |
| TB-02 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | Each run recorded Meeting Context Agent -> Relationship Context Agent -> Follow-Up Planning Agent under the Google ADK backend. | none |
| TB-03 | PASS | `proof/nw008/tranche-b/meeting-2-run.json` | Meeting 2 session state included approved_prior_context and the resulting context delta retained prior_confirmed_facts. | none |
| TB-04 | PASS | `proof/nw008/tranche-b/context-delta.json` | The primary goal stayed unchanged across both meetings. | none |
| TB-05 | PASS | `proof/nw008/tranche-b/context-delta.json` | Flexible monthly savings capacity was corrected from 450 to 325 with prior/current evidence retained and superseded=true. | none |
| TB-06 | PASS | `proof/nw008/tranche-b/context-delta.json` | Meeting 2 added a new confirmed fact for the synthetic grant end month. | none |
| TB-07 | PASS | `proof/nw008/tranche-b/context-delta.json` | The prospect budget worksheet commitment moved to completed. | none |
| TB-08 | PASS | `proof/nw008/tranche-b/context-delta.json` | The advisor draft scenario commitment remained open with current-meeting evidence. | none |
| TB-09 | PASS | `proof/nw008/tranche-b/context-delta.json` | Meeting 2 refined priorities by explicitly elevating emergency liquidity ahead of studio funding. | none |
| TB-10 | PASS | `proof/nw008/tranche-b/context-delta.json` | Every confirmed current fact, unresolved question, and proposed next step retained evidence references. | none |
| TB-11 | PASS | `proof/nw008/tranche-b/meeting-2-run.json` | Follow-Up Planning recorded confirmed_context_used from relationship_context.longitudinal_context and excluded unsupported inferences. | none |
| TB-12 | PASS | `proof/nw008/tranche-b/meeting-2-run.json` | The deterministic policy gate was invoked and received proposal context sourced from relationship_context.longitudinal_context. | none |
| TB-13 | PASS | `proof/nw008/tranche-b/decision-card.json` | NW-007 decision card mapping and both text/html renderers completed without requiring new reason semantics. | none |
| TB-14 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | GHL writes remained zero throughout the bounded replay. | none |
| TB-15 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | Firestore writes remained zero throughout the bounded replay. | none |
| TB-16 | PASS | `proof/nw008/tranche-b/meeting-2-run.json` | External effects stayed at zero for the complete replay. | none |
| TB-17 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | Only synthetic identities, synthetic contact points, and synthetic amounts were used. | none |
| TB-18 | PASS | `proof/nw008/tranche-b/meeting-1-run.json + proof/nw008/tranche-b/meeting-2-run.json` | Normalized semantic replay snapshots were compared across two bounded runs. | none |
