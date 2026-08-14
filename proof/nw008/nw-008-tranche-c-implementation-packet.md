# NW-008 Tranche C Implementation Packet

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Execution unit | TRANCHE_C |
| Purpose | HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY |
| Reusability objective | PROVE_FAILURE_PATHS_THROUGH_PROVIDER_NEUTRAL_TRANSCRIPT_SOURCE_BOUNDARY |
| Transcript source contract | **TRANSCRIPT_SOURCE_ENVELOPE_V1** |
| Data class | SYNTHETIC_ONLY |
| Historical ATs in scope | AT-2, AT-4, AT-5 (failure paths only) |
| Agent chain | Meeting Context Agent → Relationship Context Agent → Follow-Up Planning Agent (existing fleet only) |
| Policy authority | DETERMINISTIC_POLICY_ONLY |
| Packet status | **PLANNED** — `TRANCHE_C_EXECUTION_STARTED=NO` |
| New agent | NO |
| New policy semantics | NO |
| GHL writes authorized | NO |
| Firestore writes authorized | NO |
| NW-013 execution in scope | NO |
| Deployment authorized | NO |
| Real customer data | FORBIDDEN |
| Google Workspace runtime | **FUTURE_NOT_IMPLEMENTED / NOT_AUTHORIZED_IN_TRANCHE_C** |
| Prior tranche | Tranche B **MERGED_COMPLETE** (PR #42) — see [`nw-008-tranche-b-merge-closeout.md`](./nw-008-tranche-b-merge-closeout.md) |

## Freeze

```text
NW008_EXECUTION_UNIT=TRANCHE_C
PURPOSE=HISTORICAL_FAILURE_PATH_AGENT_FLEET_ACCEPTANCE_REPLAY
REUSABILITY_OBJECTIVE=PROVE_FAILURE_PATHS_THROUGH_PROVIDER_NEUTRAL_TRANSCRIPT_SOURCE_BOUNDARY
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
DATA_CLASS=SYNTHETIC_ONLY

TRANCHE_C_STATUS=PLANNED
TRANCHE_C_EXECUTION_STARTED=NO

NW008_OFFLINE_EXECUTABLE_CANDIDATES=AT-2,AT-4,AT-5,AT-8,AT-9
NW008_TRANCHE_C_TARGETS=AT-2,AT-4,AT-5
NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9

AVAILABLE_FLEET_PATH=
Meeting Context Agent
→ Relationship Context Agent
→ Follow-Up Planning Agent

PER_SCENARIO_EXECUTION=SHORT_CIRCUIT_AT_FIRST_GOVERNED_FAILURE

AUTHORITATIVE_REASON_SOURCE=WORKFLOW_POLICY
NW007_CARD_SEMANTICS_CHANGE=NO

POLICY_AUTHORITY=DETERMINISTIC_POLICY_ONLY

NEW_AGENT=NO
NEW_POLICY_SEMANTICS=NO
PACKET_SCHEMA_CHANGE=NO

GHL_WRITES_AUTHORIZED=NO
FIRESTORE_WRITES_AUTHORIZED=NO
NW013_EXECUTION_IN_SCOPE=NO
DEPLOYMENT_AUTHORIZED=NO
REAL_CUSTOMER_DATA=FORBIDDEN

GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_RUNTIME=NOT_AUTHORIZED_IN_TRANCHE_C
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
```

## Why this packet is revised

Tranche B (PR #42, **MERGED_COMPLETE**) closed
`FULL_AGENT_FLEET_TRANSCRIPT_REPLAY_GAP` for the success-path longitudinal
replay, but it fed transcripts directly into fleet processing. Tranche C
regenerates the failure-path replay plan so that historical AT-2 / AT-4 / AT-5
acceptance replay enters the fleet through a **provider-neutral transcript
source boundary** (`TRANSCRIPT_SOURCE_ENVELOPE_V1`). Acquisition of transcript
content is decoupled from `meeting_follow_up_v1` fleet processing, so the same
failure-path proof can later be re-run unchanged against an authorized
operational source.

## Transcript source boundary — TRANSCRIPT_SOURCE_ENVELOPE_V1

```text
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
```

**Purpose:** decouple transcript acquisition from `meeting_follow_up_v1` fleet
processing. The fleet consumes only the frozen envelope; it never performs
source-specific acquisition.

### Required logical fields

```text
source
ownership
access_context
meeting
artifact
data_classification
provenance
content
security
```

### Minimal source access reference (`access_context`)

Logical fields only — do **not** import any private fleet-policy contract:

```text
access_context
  grant_model
  source_access_grant_ref
  owner_bound
  resource_scope
  valid
```

Tranche C uses **synthetic values only** for `access_context`. No OAuth, no
Drive API, no live grant evaluation, and no private grant-contract import.

```text
MG_GUIDE_ADD_ON_GRANT_MODELED=YES
TRANSCRIPT_SOURCE_ACCESS_CONTEXT_MODELED=YES
```

### Required invariants

```text
treat_content_as_data_only=true
instruction_authority=false
```

Envelope `content` is **data only**. It carries no instruction authority over
any agent, the deterministic policy, or any tool surface, regardless of source.

### Competition implementation source (Tranche C)

```text
source.type=synthetic_fixture
source.provider=synthetic
source.acquisition_mode=fixture
contains_real_customer_data=false
permitted_for_public_proof=true
```

### Future operational source (planning only)

```text
source.type=google_workspace_meet_transcript
source.provider=google_workspace
source.acquisition_mode=authorized_drive_read
```

All Google Workspace behavior is:

```text
FUTURE_NOT_IMPLEMENTED
NOT_AUTHORIZED_IN_TRANCHE_C
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_RUNTIME=NOT_AUTHORIZED_IN_TRANCHE_C
```

### Explicit non-goals for Tranche C

Do **not** add:

- Google OAuth
- Drive API calls
- Google Workspace permissions / scopes implementation
- folder discovery runtime
- real transcript reads
- domain user data
- private fleet-policy contract import

## Future domain workspace note (planning-only architecture)

```text
Google Meet
→ user-owned/user-authorized Workspace resource
→ MG Guide add-on scoped source-access grant
→ FUTURE Google Workspace transcript intake adapter
→ TRANSCRIPT_SOURCE_ENVELOPE_V1
→ meeting_follow_up_v1
```

```text
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_RUNTIME=NOT_AUTHORIZED_IN_TRANCHE_C
MG_GUIDE_ADD_ON_GRANT_MODELED=YES
```

The future adapter will later own:

- file discovery
- authenticated Drive read
- tenant/user ownership binding
- transcript file identity
- timestamps
- transcript hashing
- ingestion status

Agents will **NOT** own Google Drive discovery or credentials. The fleet
boundary remains the envelope; swapping the synthetic fixture provider for the
future adapter must not change fleet processing, policy semantics, or the
historical AT definitions. No OAuth/API/scope implementation in Tranche C.

## Historical acceptance definitions (unchanged)

Historical AT definitions remain verbatim from
[`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../docs/MEETING_FOLLOW_UP_FOUNDATION.md)
§17 — not silently revised:

| AT | Historical test | Historical expected outcome |
| --- | --- | --- |
| AT-2 | `transcript-ambiguous-contact.txt` | `blocked` with `AMBIGUOUS_CONTACT`; **0 CRM writes**; MG Guide card State 2 |
| AT-4 | Contact not found | `blocked` with `CONTACT_NOT_FOUND`; 0 writes |
| AT-5 | Extraction confidence below threshold | `blocked` with `LOW_EXTRACTION_CONFIDENCE`; 0 writes |

Tranche C replay targets these **unchanged** definitions only:

```text
NW008_TRANCHE_C_TARGETS=AT-2,AT-4,AT-5
NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9

AT-2: blocked / AMBIGUOUS_CONTACT / CRM_WRITES=0 / MG Guide card State 2
AT-4: blocked / CONTACT_NOT_FOUND / CRM_WRITES=0
AT-5: blocked / LOW_EXTRACTION_CONFIDENCE / CRM_WRITES=0
```

### Card claim boundary (AT-4 / AT-5)

```text
AUTHORITATIVE_REASON_SOURCE=WORKFLOW_POLICY
NW007_CARD_SEMANTICS_CHANGE=NO
```

- Authoritative reason codes for AT-2 / AT-4 / AT-5 come from workflow /
  deterministic policy — **not** invented NW-007 card presentation semantics.
- Only **AT-2** historically requires MG Guide card State 2.
- AT-4 and AT-5 do **not** claim named NW-007 card scenario semantics beyond
  what the existing card surface already exposes.
- Unsupported reason tuples may fail closed under existing NW-007 semantics.
- Do **not** alter historical AT definitions and do **not** change the NW-007
  decision-card mapper to invent presentation semantics.

### Fleet execution language

```text
AVAILABLE_FLEET_PATH=
Meeting Context Agent
→ Relationship Context Agent
→ Follow-Up Planning Agent

PER_SCENARIO_EXECUTION=SHORT_CIRCUIT_AT_FIRST_GOVERNED_FAILURE
```

### Architectural rule

Do **not** force downstream agents to execute after the correct governed
failure boundary merely to claim fleet execution. When the governed failure
boundary is reached, the run short-circuits there; the proof records which
agents started and completed up to that boundary.

### Required proof fields (per replayed AT run)

```text
AGENTS_STARTED
AGENTS_COMPLETED
STOP_POINT
STOP_REASON_CODE
POLICY_BYPASS=false
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
```

Any non-zero write/effect counter or `POLICY_BYPASS=true` → **FAIL CLOSED and
STOP**.

## Proof obligations

Baseline set **TC-01…TC-19** is carried forward for the Tranche C failure-path
replay; **TC-20…TC-22** are added in this revision for the transcript source
boundary. Do **not** pre-mark obligations PASS.

| ID | Obligation | Status |
| --- | --- | --- |
| TC-01 | AT-2 transcript enters fleet only via TRANSCRIPT_SOURCE_ENVELOPE_V1 | TODO |
| TC-02 | AT-2 AGENTS_STARTED recorded for fleet entry | TODO |
| TC-03 | AT-2 stops at governed failure boundary: STOP_POINT + STOP_REASON_CODE=`AMBIGUOUS_CONTACT`; disposition `blocked`; CRM_WRITES=0 | TODO |
| TC-04 | AT-2 AGENTS_COMPLETED exact — no downstream agent forced past the failure boundary | TODO |
| TC-05 | AT-2 counters: POLICY_BYPASS=false, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 | TODO |
| TC-06 | AT-4 transcript enters fleet only via TRANSCRIPT_SOURCE_ENVELOPE_V1 | TODO |
| TC-07 | AT-4 AGENTS_STARTED recorded for fleet entry | TODO |
| TC-08 | AT-4 stops at governed failure boundary: STOP_POINT + STOP_REASON_CODE=`CONTACT_NOT_FOUND`; disposition `blocked`; CRM_WRITES=0 | TODO |
| TC-09 | AT-4 AGENTS_COMPLETED exact — no downstream agent forced past the failure boundary | TODO |
| TC-10 | AT-4 counters: POLICY_BYPASS=false, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 | TODO |
| TC-11 | AT-5 transcript enters fleet only via TRANSCRIPT_SOURCE_ENVELOPE_V1 | TODO |
| TC-12 | AT-5 AGENTS_STARTED recorded for fleet entry | TODO |
| TC-13 | AT-5 stops at governed failure boundary: STOP_POINT + STOP_REASON_CODE=`LOW_EXTRACTION_CONFIDENCE`; disposition `blocked`; CRM_WRITES=0 | TODO |
| TC-14 | AT-5 AGENTS_COMPLETED exact — no downstream agent forced past the failure boundary | TODO |
| TC-15 | AT-5 counters: POLICY_BYPASS=false, GHL_WRITES=0, FIRESTORE_WRITES=0, EXTERNAL_EFFECTS=0 | TODO |
| TC-16 | Existing fleet entrypoints reused; no new agent, no parallel orchestration engine | TODO |
| TC-17 | Deterministic / replay-safe proof: normalized semantic snapshots compared across bounded runs | TODO |
| TC-18 | REAL_CUSTOMER_DATA=0; synthetic fixture safety validation passes (`contains_real_customer_data=false`, `permitted_for_public_proof=true`) | TODO |
| TC-19 | Historical AT definitions unchanged (foundation §17 verbatim; no silent revision) | TODO |
| TC-20 | TRANSCRIPT_SOURCE_PROVENANCE_PRESERVED — source, ownership, access reference (`access_context`), and provenance survive intake into fleet processing unaltered | TODO |
| TC-21 | TRANSCRIPT_CONTENT_HAS_NO_INSTRUCTION_AUTHORITY — envelope content treated as data only (`treat_content_as_data_only=true`, `instruction_authority=false`) | TODO |
| TC-22 | HISTORICAL_COMPLETION_CLAIMS_EXACT — completion claims match the unchanged historical AT clauses exactly; no over-claim | TODO |

## Acceptance claim boundary

Tranche C is intended to evidence the historical **failure paths** through the
provider-neutral transcript source boundary:

```text
AT-2: blocked / AMBIGUOUS_CONTACT / CRM_WRITES=0 / MG Guide card State 2
AT-4: blocked / CONTACT_NOT_FOUND / CRM_WRITES=0
AT-5: blocked / LOW_EXTRACTION_CONFIDENCE / CRM_WRITES=0

AUTHORITATIVE_REASON_SOURCE=WORKFLOW_POLICY
NW007_CARD_SEMANTICS_CHANGE=NO
```

Do **not** mark any historical AT complete unless every clause of its
unchanged historical definition is evidenced. Only AT-2 historically requires
the MG Guide card State 2 clause; AT-4 / AT-5 completion claims rest on
workflow/policy reason codes and zero-write guarantees, not invented NW-007
named card semantics. AT-1 / AT-3 / AT-6 / AT-7 remain write-path blocked;
AT-8 / AT-9 remain partial and are **excluded** from Tranche C
(`NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9`); AT-10 remains deferred behind NW-005
Stage B authority. None of those postures change in Tranche C.

## Non-goals (enforced)

- Do not implement the Google Workspace transcript adapter.
- Do not add Google OAuth, Drive API calls, Google Workspace permissions,
  folder discovery runtime, real transcript reads, or domain user data.
- Do not change deterministic policy semantics to force PASS.
- Do not force downstream agents to execute past the governed failure
  boundary.
- Do not execute NW-013 live reads.
- Do not deploy.
- Do not authorize CRM mutation.
- Do not revise foundation acceptance text.

## Boundaries

```text
APPLICATION_CODE_CHANGED=NO
GOOGLE_WORKSPACE_RUNTIME_CHANGED=NO
CRM_MUTATION_AUTHORITY_CHANGED=NO
POLICY_SEMANTICS_CHANGE=NO
NEW_AGENT=NO
DEPLOYMENT=NO
MG_MCP_WRITES=NO
```

## STOP

```text
NW008_TRANCHE_C_TARGETS=AT-2,AT-4,AT-5
NW008_TRANCHE_C_EXCLUDES=AT-8,AT-9
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
TRANSCRIPT_SOURCE_ACCESS_CONTEXT_MODELED=YES
MG_GUIDE_ADD_ON_GRANT_MODELED=YES
GOOGLE_WORKSPACE_ADAPTER_STATUS=FUTURE_NOT_IMPLEMENTED
GOOGLE_WORKSPACE_RUNTIME=NOT_AUTHORIZED_IN_TRANCHE_C
AUTHORITATIVE_REASON_SOURCE=WORKFLOW_POLICY
NW007_CARD_SEMANTICS_CHANGE=NO
PER_SCENARIO_EXECUTION=SHORT_CIRCUIT_AT_FIRST_GOVERNED_FAILURE
TRANCHE_C_STATUS=PLANNED
TRANCHE_C_EXECUTION_STARTED=NO
APPLICATION_CODE_CHANGED=NO
READY_FOR_TRANCHE_C_IMPLEMENTATION=YES
STOP_CODE=NW008_TRANCHE_C_PLAN_FROZEN_READY_FOR_IMPLEMENTATION
```
