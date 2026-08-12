# NW-006 planning-only packet — MG Guide Meeting Follow-Up card

## Status

| Field | Value |
| --- | --- |
| Work item | NW-006 |
| Status | **PLANNED_NOT_STARTED** |
| Execution | **planning only** (no implementation in this closeout) |
| Input contract | `meeting_follow_up_packet_v1` |
| Mutation controls | **none** |
| External effects | **0** |
| Agent rerun | **forbidden** |
| Policy re-evaluation on card | **forbidden** (render only) |

## Intended UI / application implementation surface

**Before any NW-006 coding begins, the implementation surface is fixed as:**

1. **Primary surface:** authenticated **MG Guide application** Meeting Follow-Up
   experience — a dedicated **Meeting Follow-Up card** (not a generic chat dump).
   Foundation reference: [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §14.
2. **Not the surface:** VS Code custom agents, GitHub PR comments, CLI stdout alone,
   raw JSON blob dumps without card chrome, or ad-hoc chat responses.
3. **Data path (planning intent only):** already-produced
   `meeting_follow_up_packet_v1` → MG Guide card renderer → human review actions.
4. **Authority path:** card **displays** deterministic policy outcomes already present
   on the packet; card **must not** call the policy gate, agents, GHL, Firestore, or
   deployment APIs.

Exact host route / component path inside the pre-existing MG Guide app remains
implementation-detail for a later governed coding unit and is **not** invented here.
What is fixed now is the product surface class: **MG Guide Meeting Follow-Up card**.

## Input contract

```text
meeting_follow_up_packet_v1
  -> MG Guide Meeting Follow-Up card
```

The card consumes a schema-valid terminal (or explicitly non-terminal) packet and
renders human-readable state. It does not synthesize CRM facts.

## Terminal packet states (render contracts)

### `completed`

- Policy permitted the intended note and/or stage outcome path without open blockers.
- Card shows success framing (contact resolved summary, proposed/authorized intents
  as already recorded on the packet, next-step brief).
- No live CRM write is performed by the card.
- Human action: acknowledge / archive; optional copy of note text for offline use only.

### `completed_with_review`

- Packet is usable but requires human confirmation (e.g. stage transition denied or
  approval-required while note intent may remain).
- Preserve and display policy reason codes (e.g. `STAGE_TRANSITION_NOT_ALLOWED`).
- Proposed note intent may remain visible; stage intent withheld or flagged.
- Human action: accept note language, decline stage change, or escalate.

### `blocked`

- Ambiguity, missing relationship context, or fail-closed policy path prevents a
  clean completion claim.
- Preserve reason codes such as `AMBIGUOUS_CONTACT`, `AMBIGUOUS_OPPORTUNITY`,
  `OPPORTUNITY_NOT_FOUND`, `LOW_EXTRACTION_CONFIDENCE`, `CONTACT_NOT_FOUND`.
- Explicit UX copy: **No CRM changes were made** (and none are offered by the card).
- Human action: resolve ambiguity offline / in CRM, then start a new governed run
  (no in-card agent rerun).

### `failed`

- Workflow/tool failure disposition already recorded on the packet
  (e.g. `GHL_TOOL_FAILURE`, `GHL_WRITE_NOT_VERIFIED` when those phases exist later).
- Card shows failure framing with reason codes; zero mutation controls.
- Human action: investigate failure using audit/proof outside this card; do not
  retry from the card UI in NW-006 scope.

## Non-terminal packets

Packets whose status is still in-flight
(`received` | `extracting` | `resolving` | `evaluating` | `writing`, or any other
non-terminal status) are **not** claimed as completed outcomes.

**Planning rule for NW-006:**

- **Preferred:** **reject** non-terminal packets for the terminal card view
  (show a lightweight **in-progress / not ready** shell, or an error that the packet
  is not terminal).
- **Allowed alternate:** render a distinct **in-progress** card chrome that never
  uses completed/blocked/failed copy.
- **Forbidden:** treat non-terminal packets as `completed`, invent terminal reason
  codes, or enable mutation controls while in-progress.

## Policy reason codes (display only)

Reason codes are packet metadata for human triage. The card renders them; it does
not recompute them.

```text
AMBIGUOUS_CONTACT
AMBIGUOUS_OPPORTUNITY
OPPORTUNITY_NOT_FOUND
CONTACT_NOT_FOUND
LOW_EXTRACTION_CONFIDENCE
STAGE_TRANSITION_NOT_ALLOWED
GHL_TOOL_FAILURE
GHL_WRITE_NOT_VERIFIED
```

## Proposed note / stage intents (display only)

- Proposed note intent: note text / summary / next step already present on packet.
- Proposed stage intent: optional pipeline transition suggestion already present.
- No hidden mutation command, no direct write call, no CRM action token.
- Card never promotes an intent into an external effect.

## Card authority rules (hard)

| Rule | Requirement |
| --- | --- |
| Policy | **Render only** — do not re-evaluate policy |
| Agents | **No agent rerun** from the card |
| Mutation controls | **None** in this planning unit |
| GHL | **No** live reads/writes |
| Firestore | **No** writes |
| Deployment | **No** |
| External effects | **EXTERNAL_EFFECTS=0** |

## Next human action (generic)

1. Open the card for a terminal packet state.
2. Read reason codes and proposed intents.
3. Confirm, rewrite offline, or escalate — outside any automated CRM write path.
4. Do not expect the card to execute CRM mutations under NW-006.

## Explicit non-goals for this planning packet

- Implementing the MG Guide card UI/code
- Wiring mutation execution or approve-and-write controls
- Live GHL, Firestore audit writer (NW-005), Cloud Run (NW-007)
- Replacing deterministic policy with LLM judgment on the card

## STOP

`STOP_CODE=NW006_PLANNED_NOT_STARTED`
