# Proof index — judges

```text
SURFACE=docs/judges/PROOF_INDEX.md
PURPOSE=SHORT_EVIDENCE_INDEX
DO_NOT_COPY_FULL_PROOF=YES
```

This is a map from public claims to the best current evidence. It does not
replace the proof packets.

| Claim | Status | Best evidence | What it proves |
| --- | --- | --- | --- |
| Gemini meeting-context extraction | Proven | [Competition acceptance](../../proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md) | Live Gemini 3.5 extraction on the competition slice |
| Three-agent Google ADK sequence | Proven | [Agent Runtime acceptance 006](../../proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md) | `meeting_context_agent` → `relationship_context_agent` → `follow_up_planning_agent` |
| Hosted Agent Runtime | Proven | [Agent Runtime acceptance 006](../../proof/mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md) | Hosted `mg-guide-orchestrator` (`google-adk`, `SequentialAgent`) |
| Success / fail-closed behavior | Proven | [Competition acceptance](../../proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md) | SUCCESS completed; `AMBIGUOUS_CONTACT` fail-closed |
| Firestore audit | Proven | [Competition acceptance](../../proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md) | Authorized `workflow_runs` audit smoke |
| HighLevel REST v3 exact live read | Proven | [REST exact synthetic contact read 002](../../proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md) | `LIVE_REST_V3_EXACT_CONTACT_READ=PASS`; `NETWORK_CALL_COUNT=1`; `MUTATION_CALL_COUNT=0` |
| Current REST note path | Pending | This index + REST packet above | `CURRENT_REST_V3_NOTE_CREATE=PENDING`; `CURRENT_REST_V3_NOTE_READBACK=PENDING`; `NOTE_CREATE_EXECUTED=NO`; `NOTE_READBACK_EXECUTED=NO` |
| Same-run transcript-to-live-CRM write | Not claimed | Competition acceptance + this index | `INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO` |
| Competition Delta | Recorded | [NEW_WORK_LEDGER.md](../../competition/NEW_WORK_LEDGER.md) | Competition-period provenance |

## Current CRM language (exact)

```text
LIVE_REST_V3_EXACT_CONTACT_READ=PASS
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
```

Do not convert the exact-contact live read into a note-write claim.

## Historical supporting evidence

Grant 008 live synthetic note+stage is **supporting evidence only**, not the
current transport centerpiece:

- [Historical Grant 008 result](../../proof/nw008/nw-008-at1-live-execution-result-008.md)

Historical HighLevel MCP discovery remains under [`proof/phase2/`](../../proof/phase2/).

For the full tree, see [proof/README.md](../../proof/README.md).
