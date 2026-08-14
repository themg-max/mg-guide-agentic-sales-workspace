# NW-008 Tranche B Implementation Packet

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Execution unit | TRANCHE_B |
| Purpose | LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY |
| Data class | SYNTHETIC_ONLY |
| Meeting count | 2 |
| Agent chain | Meeting Context Agent → Relationship Context Agent → Follow-Up Planning Agent |
| Policy authority | DETERMINISTIC_POLICY_ONLY |
| New agent | NO |
| New policy semantics | NO |
| GHL writes authorized | NO |
| Firestore writes authorized | NO |
| NW-013 execution in scope | NO |
| Deployment authorized | NO |
| Real customer data | FORBIDDEN |

## Freeze

```text
NW008_EXECUTION_UNIT=TRANCHE_B
PURPOSE=LONGITUDINAL_SYNTHETIC_AGENT_FLEET_REPLAY
DATA_CLASS=SYNTHETIC_ONLY
MEETING_COUNT=2

AGENT_CHAIN:
Meeting Context Agent
Relationship Context Agent
Follow-Up Planning Agent

POLICY_AUTHORITY=DETERMINISTIC_POLICY_ONLY

NEW_AGENT=NO
NEW_POLICY_SEMANTICS=NO

GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
NW013_EXECUTION_IN_SCOPE=NO
DEPLOYMENT_AUTHORIZED=NO
REAL_CUSTOMER_DATA=FORBIDDEN
```

## Synthetic story requirements

Design **two** entirely fictional meetings.

Meeting 1 must establish:
- participant identity
- relationship stage/context
- goals
- needs
- concerns/objections
- commitments
- unresolved questions
- explicit next meeting / next step

Meeting 2 must contain:
- at least one unchanged fact
- at least one corrected prior fact
- at least one new fact
- at least one completed prior commitment
- at least one still-open prior commitment
- refined goals or priorities
- unresolved question(s)
- proposed next step

Do **not** copy or lightly edit private real transcript content.

Forbidden:
- real names
- real contact information
- exact real balances/debt values
- employers
- insurance/account details
- verbatim transcript language
- uniquely identifying combinations of facts

## Context delta contract

Freeze the Tranche B output contract containing:

```text
PRIOR_CONFIRMED_FACTS
CURRENT_CONFIRMED_FACTS
UNCHANGED_FACTS
CORRECTED_FACTS
NEW_FACTS
COMMITMENTS_COMPLETED
COMMITMENTS_OPEN
GOALS_REFINED
UNRESOLVED_QUESTIONS
PROPOSED_NEXT_STEP
EVIDENCE_REFERENCES
```

Every claim must point to Meeting 1 or Meeting 2 evidence.
No unsupported inference may be promoted to confirmed fact.

## Agent responsibilities

- **Meeting Context Agent**: extract current-meeting evidence only.
- **Relationship Context Agent**: compare current meeting with prior approved context; classify unchanged / corrected / new facts; track commitments and goal evolution.
- **Follow-Up Planning Agent**: propose next-step options from confirmed context only.

Agents must **not** authorize consequential actions.
Deterministic policy remains the sole action gate.

## Proof obligations

Define Tranche B proof obligations before coding.

Minimum:

| ID | Obligation | Status |
| --- | --- | --- |
| TB-01 | two synthetic meetings accepted | TODO |
| TB-02 | real existing agent chain executed | TODO |
| TB-03 | prior context retrieved for Meeting 2 | TODO |
| TB-04 | unchanged fact correctly retained | TODO |
| TB-05 | corrected fact supersedes prior value without erasing provenance | TODO |
| TB-06 | new fact correctly added | TODO |
| TB-07 | completed commitment recognized | TODO |
| TB-08 | open commitment retained | TODO |
| TB-09 | goals/priorities refined | TODO |
| TB-10 | evidence references cover every confirmed context claim | TODO |
| TB-11 | follow-up plan uses confirmed context only | TODO |
| TB-12 | deterministic policy receives proposal/context | TODO |
| TB-13 | NW-007 card renders resulting policy state safely | TODO |
| TB-14 | GHL_WRITES=0 | TODO |
| TB-15 | FIRESTORE_WRITES=0 | TODO |
| TB-16 | EXTERNAL_EFFECTS=0 | TODO |
| TB-17 | REAL_CUSTOMER_DATA=0 | TODO |
| TB-18 | deterministic/replay-safe proof where applicable | TODO |

Do **not** pre-mark obligations PASS.

## Acceptance claim boundary

Tranche B is intended to close:

```text
FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_NOT_YET_EVIDENCED
```

Do **not** automatically mark AT-2 / AT-4 / AT-5 historical complete merely because
the agent chain executes. Re-evaluate each unchanged historical AT clause
independently after evidence.

## MG MCP note

Current MG MCP repo-source search returned zero records for:

```text
"NW008 PR40 merged Tranche A next steps longitudinal synthetic agent fleet replay"
```

Record:

```text
MG_MCP_TRANCHE_B_DISCOVERABILITY=UNKNOWN
```

Exact note:

UNKNOWN: expected MG MCP context was not surfaced for NW-008 Tranche B /
PR #40 post-merge planning - Action: run targeted search/alias/index validation
for NW008, PR40, Tranche B, longitudinal synthetic agent fleet replay, and
meeting_follow_up_v1.

Decision-history supporting context:
DEC-029 Phase 8 — Orchestration Utilization & Workflow Activation
DEC-001 Dual-AI Architecture

Treat these as supporting planning context only.
