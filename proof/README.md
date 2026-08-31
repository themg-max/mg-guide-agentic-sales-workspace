# Proof directory

```text
SURFACE=proof/README.md
DO_NOT_MOVE_PROOF_FILES=YES
DO_NOT_ALTER_PROOF_CLAIMS_FOR_PRESENTATION=YES
```

This directory preserves engineering and governance history. Proof files are
not relocated for aesthetics. Claims inside historical packets stay
historically accurate.

Judges should start with the short index:
[docs/judges/PROOF_INDEX.md](../docs/judges/PROOF_INDEX.md).

## Judge recommended

| Packet | Why it matters |
| --- | --- |
| [competition/meeting-follow-up-v1-acceptance-finalization-001.md](competition/meeting-follow-up-v1-acceptance-finalization-001.md) | Competition acceptance: Gemini, success, fail-closed, Firestore, Cloud Run judge surface |
| [mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md](mg-guide/agent-runtime/mg-guide-agent-runtime-runtime-acceptance-proof-006.md) | Hosted Agent Runtime: `mg-guide-orchestrator`, sequential three-agent execution |
| [nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md](nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md) | HighLevel REST v3 exact synthetic contact live read |
| [demo/](demo/) | Demo evidence |
| [competition/](competition/) | Workspace add-on and competition UX acceptance |

Current CRM language for the REST packet:

```text
LIVE_REST_V3_EXACT_CONTACT_READ=PASS
CURRENT_REST_V3_NOTE_CREATE=PENDING
CURRENT_REST_V3_NOTE_READBACK=PENDING
INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO
```

## Deep technical

These trees preserve engineering and governance history. They are not required
first reading for judges.

| Tree | Scope |
| --- | --- |
| [nw005/](nw005/) | Firestore audit writer |
| [nw006/](nw006/) | Meeting Follow-Up card |
| [nw007/](nw007/) | Cloud Run judge surface |
| [nw008/](nw008/) | CRM boundary, REST, historical Grant 008, acceptance tests |
| [phase1/](phase1/) | Deterministic foundation |
| [phase2/](phase2/) | Historical HighLevel MCP discovery |
| [phase2b/](phase2b/) | Offline GHL read adapter |
| [phase3/](phase3/) | Meeting / relationship / follow-up agents |
| [mg-guide/](mg-guide/) | Agent Runtime and related MG Guide proof |
| [canonical-synthetic-read-binding-v1/](canonical-synthetic-read-binding-v1/) | Synthetic-read binding |

Historical Grant 008 is supporting evidence only, not the current transport
centerpiece.
