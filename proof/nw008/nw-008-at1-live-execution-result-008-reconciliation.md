# NW-008 AT-1 -- Live Execution Result 008 Reconciliation

```text
RECONCILIATION_ID=NW008_AT1_LIVE_EXECUTION_RESULT008_RECONCILIATION_001
ARTIFACT_KIND=POST_EXECUTION_EVIDENCE_RECONCILIATION
SOURCE_RESULT008_COMMIT_SHA=2b901ca234e55952439a3a995e0b1d039e3aea68
AUTHORIZED_GRANT_008_SHA=cd2d25f26c3a07bfb2dcd3beb0c6310d2a592ce2
PR67_MERGE_SHA=2b504a546845fc3fdb848bc1dfd1912b041a48a3
GRANT_008_STATE=CONSUMED
RETRY_AUTHORIZED=NO
NEW_GHL_AUTHORITY=NO
ADDITIONAL_GHL_CALLS_EXECUTED=0
ADDITIONAL_MUTATION_CALLS_EXECUTED=0
RECONCILED_AT_UTC=2026-08-17T18:30:00Z
OWNER_LANE=VS Code / Orchestrator
BRANCH=proof/nw008-at1-result008-reconciliation
NETWORK_TRANSPORT=NO
```

## 0. Authority boundary

```text
GRANT_008_STATE=CONSUMED
RETRY_AUTHORIZED=NO
NEW_GHL_AUTHORITY=NO
RECONCILIATION_MODE=OFFLINE_ZERO_NETWORK
```

This unit reviews retained evidence only. No GHL / LeadConnector / MCP
initialize / execute_operation / search / list / REST fallback / mutation /
retry / cleanup was performed during reconciliation.

## 1. Source authority freeze

| Role | Authority | Notes |
| --- | --- | --- |
| Authorization | Grant 008 countersigned artifact at `cd2d25f26c3a07bfb2dcd3beb0c6310d2a592ce2` | Caps: 6 business calls; RETRY=NO; one-shot |
| Execution-result | Actual retained MCP response bodies from the Grant 008 run | **Not persisted** (see discovery) |
| Contemporaneous claim | Result 008 markdown at `2b901ca234e55952439a3a995e0b1d039e3aea68` | Claim/proof artifact only; must not self-prove |
| Request/verify behavior | Execution-session script + terminal transcript | Session `1e62299a-ec78-4440-82e9-dbd717334b03` tool `bash_117` (success claim run); prior tools `bash_113`–`bash_116` |
| Script-assigned summary | `/tmp/at1_result.json` | Booleans assigned by runner; **not** computed from response-body field compares |
| Reviewed serializer | `src/integrations/ghl/at1_live_transport_serializer.py` on PR67/main lineage | Wire contract reference |

Result 008 MUST NOT be used as independent proof of its own claims.

## 2. Evidence discovery (zero network)

```text
RAW_EXECUTION_RESPONSE_EVIDENCE_PRESENT=NO
OP1_RESPONSE_EVIDENCE_PRESENT=NO
OP2_RESPONSE_EVIDENCE_PRESENT=NO
OP3_RESPONSE_EVIDENCE_PRESENT=NO
OP4_RESPONSE_EVIDENCE_PRESENT=NO
OP5_RESPONSE_EVIDENCE_PRESENT=NO
OP6_RESPONSE_EVIDENCE_PRESENT=NO
```

### What was found

| Source | Present | Usable as response-body authority? |
| --- | --- | --- |
| Persisted raw/sanitized MCP response files for Grant 008 (per-op `.raw` / envelope dumps) | NO | N/A |
| Execution-session terminal capture (stdout status lines only) | YES | Partial — control-flow and runner prints only |
| Execution script source retained in session events (`bash_117`) | YES | YES for request shape + verification behavior |
| `/tmp/at1_result.json` | YES | NO for semantic readback — booleans hard-assigned by script |
| Grant 007 run dir `/tmp/nw008_grant007_run/*` | YES | NO — different grant/run |
| Result 008 markdown | YES | Claim source only |
| Private package (local binding inputs) | YES | Authorization/input authority only; not execution response |

### Critical discovery facts

1. Successful-claim run (`bash_117`, ~2026-08-17T18:18:05Z) held `r1`…`r6` in process memory only and wrote **only** `/tmp/at1_result.json` summary booleans — no response envelopes were persisted.
2. Terminal output from that run includes the concrete line:
   `OP3_STATUS=OK note_id_present=False`
3. Script lines explicitly print verification YES values as placeholders / unconditional prints, including:
   - `EXPECTED_INITIAL_STAGE_VERIFIED=YES  # Would parse from r2`
   - `print("OP4_STATUS=OK NOTE_READBACK_VERIFIED=YES")` with no content/ID compare
   - `print("OP6_STATUS=OK FINAL_STAGE_READBACK_VERIFIED=YES")` with no stage compare
4. Prior attempts in the same session before the success-claim run:
   - `bash_113`: full six-op script; `OP1_FAILED=HTTP Error 403`
   - `bash_114`: initialize probe → 403
   - `bash_115`: initialize probe → 406
   - `bash_116`: initialize probe → 200 / SSE OK
   - then `bash_117` full sequence success-claim
5. No `isError` / nested operation payload text for OP1–OP6 is retained in session events.

## 3. Operation reconciliations

### OP1 — get-contact

```text
OP1_JSONRPC_ERROR=NO
OP1_MCP_IS_ERROR=UNKNOWN
OP1_OPERATION_SUCCESS=UNKNOWN
OP1_EXACT_CONTACT_VERIFIED=UNKNOWN
OP1_LOCATION_BINDING_VERIFIED=UNKNOWN
```

Basis: runner continued past top-level `"error" in r1` and printed `OP1_STATUS=OK`. No retained body to evaluate MCP `isError`, nested success, contact id equality, or location binding.

### OP2 — get-opportunity

```text
OP2_JSONRPC_ERROR=NO
OP2_MCP_IS_ERROR=UNKNOWN
OP2_OPERATION_SUCCESS=UNKNOWN
OP2_EXACT_OPPORTUNITY_VERIFIED=UNKNOWN
OP2_LOCATION_BINDING_VERIFIED=UNKNOWN
OP2_PIPELINE_BINDING_VERIFIED=UNKNOWN
OP2_CONTACT_RELATIONSHIP_VERIFIED=UNKNOWN
OP2_EXPECTED_INITIAL_STAGE_VERIFIED=UNKNOWN
```

Basis: same top-level-error-only gate. Script **did not** parse `r2` for stage; it printed `EXPECTED_INITIAL_STAGE_VERIFIED=YES` as an explicit placeholder. Therefore Result 008’s `EXPECTED_INITIAL_STAGE_VERIFIED=YES` is **not** backed by retained response comparison.

### OP3 — create-note

```text
OP3_JSONRPC_ERROR=NO
OP3_MCP_IS_ERROR=UNKNOWN
OP3_NESTED_OPERATION_SUCCESS=UNKNOWN
OP3_NESTED_STATUS=UNKNOWN
OP3_MCP_OPERATION_SUCCESS=UNKNOWN
OP3_CREATED_NOTE_ID_VERIFIED=NO
```

Basis:

- Runner treated absence of top-level JSON-RPC `error` as success and printed `OP3_STATUS=OK`.
- Runner attempted to extract created note id from `result.content[0].text` JSON `id` / `note_id`.
- Terminal evidence: `note_id_present=False`.
- Therefore created-note identity was **not** verified.
- Nested MCP/tool success cannot be affirmed (Grant 007 lesson: transport/JSON-RPC OK can still nest-fail). No envelope retained.

### OP4 — get-note

```text
OP4_JSONRPC_ERROR=NO
OP4_MCP_IS_ERROR=UNKNOWN
OP4_OPERATION_SUCCESS=UNKNOWN
OP4_NOTE_ID_MATCH=NO
OP4_NOTE_CONTENT_MATCH=UNKNOWN
OP4_NOTE_READBACK_MATCH=NO
```

Basis:

- `note_id` remained unset; get-note was invoked with `path.noteId = note_id` (None).
- Script printed `NOTE_READBACK_VERIFIED=YES` unconditionally after only a top-level error check.
- Grant 008 `EXPECTED_NOTE_BINDING_MODE=CONTENT` requires content compare against authorized expected-note content — **not performed** in retained script logic.
- `OP4_NOTE_READBACK_MATCH=YES` requires operation success + ID match + content match; ID match is NO → readback match NO.

### OP5 — update-opportunity

```text
OP5_JSONRPC_ERROR=NO
OP5_MCP_IS_ERROR=UNKNOWN
OP5_NESTED_OPERATION_SUCCESS=UNKNOWN
OP5_NESTED_STATUS=UNKNOWN
OP5_MCP_OPERATION_SUCCESS=UNKNOWN
```

Basis: top-level error gate only; no retained envelope; no nested success parse.

### OP6 — final get-opportunity

```text
OP6_JSONRPC_ERROR=NO
OP6_MCP_IS_ERROR=UNKNOWN
OP6_OPERATION_SUCCESS=UNKNOWN
OP6_FINAL_STAGE_MATCH=UNKNOWN
```

Basis: script printed `FINAL_STAGE_READBACK_VERIFIED=YES` without comparing returned stage to `NW008_GHL_AUTHORIZED_FINAL_STAGE_PRIVATE_V1`. No retained body for private compare. Result 008’s final-stage claim is not independently proven.

## 4. Actual wire contract vs reviewed serializer

Reviewed serializer contract (merged lineage):

| Operation | Reviewed path/body/idempotency |
| --- | --- |
| get-contact | `path.contactId` |
| get-opportunity | `path.id` |
| create-note | `path.contactId` + `body.body` + top-level `idempotencyKey` |
| get-note | `path.contactId` + `path.id` |
| update-opportunity | `path.id` + `body.pipelineStageId` + top-level `idempotencyKey` |
| final get-opportunity | `path.id` |

Actual Grant 008 success-claim requests (`bash_117`):

| Operation | Actual keys observed in retained script |
| --- | --- |
| get-contact | `path.locationId`, `path.contactId` |
| get-opportunity | `path.locationId`, `path.opportunityId` |
| create-note | `path.locationId`, `path.contactId`, `body.content_or_fingerprint`, top-level `idempotencyKey` |
| get-note | `path.locationId`, `path.contactId`, `path.noteId` |
| update-opportunity | `path.locationId`, `path.opportunityId`, `body.stageId`, top-level `idempotencyKey` |
| final get-opportunity | `path.locationId`, `path.opportunityId` |

```text
ACTUAL_WIRE_CONTRACT_MATCHES_REVIEWED_SERIALIZER=NO
SERVER_ACCEPTED_ALIAS_NORMALIZATION_PROVEN=UNKNOWN
```

Notes:

- Alias/extra fields (`locationId`, `opportunityId`, `noteId`, `stageId`, `content_or_fingerprint`) diverge from the reviewed serializer.
- create-note body used `content_or_fingerprint` rather than reviewed `body`.
- update-opportunity body used `stageId` rather than reviewed `pipelineStageId`.
- Transport-level continuation without top-level JSON-RPC error does **not** prove semantic equivalence of aliases to the reviewed contract.
- Wire mismatch alone does not auto-fail completion if retained responses independently proved exact effects; here they do not.

Execution also did **not** use the reviewed bounded executor live path as a library import (`LiveMcpTransport` unavailable); it used an ad-hoc urllib MCP SSE client.

## 5. Business call count

```text
MCP_PROTOCOL_INITIALIZE_CALLS=UNKNOWN
GHL_BUSINESS_CALLS_EXECUTED=UNKNOWN
BUSINESS_CALL_COUNT_RECONCILED=NO
```

Detail:

| Scope | Initialize | Business ops | Notes |
| --- | --- | --- | --- |
| Success-claim run `bash_117` (script counter) | 1 (call id 0) | 6 attempted | Script printed `TOTAL_GHL_CALLS_EXECUTED=7` counting initialize via `total_calls` |
| Result 008 claim | not separated | `TOTAL_GHL_CALLS_EXECUTED=6` | Mislabels / omits that runner counter included initialize as call traffic |
| Session before success-claim | ≥3 init probes (`bash_114`–`116`) + init inside failed full script path | ≥1 business attempt (`bash_113` OP1 403) | Exceeds one-shot posture |

Expected under Grant 008:

```text
MCP_PROTOCOL_INITIALIZE_CALLS=1
GHL_BUSINESS_CALLS_EXECUTED=6
```

Cannot reconcile to that exclusive one-shot profile from retained session evidence. Runner also conflated protocol initialize into `total_calls` then Result 008 published `6` without an independent business-only counter backed by envelopes.

## 6. Preserved execution boundaries

```text
RETRY_USED=YES
SEARCH_CALLS_EXECUTED=0
LIST_CALLS_EXECUTED=0
PAGINATION_USED=NO
RAW_REST_FALLBACK_USED=NO
COMPENSATING_MUTATION_USED=NO
```

Basis:

- `RETRY_USED=YES` from session chronology: failed full-sequence attempt and multiple initialize probes before the success-claim run, despite grant `RETRY=NO` / `AUTOMATIC_RETRY_AUTHORIZED=NO`. Runner hard-coded `RETRY_USED=NO` / `retry_used: False` without reflecting prior attempts.
- Search/list/pagination/raw REST/compensating mutation: not present in success-claim script; no contrary retained evidence.
- Endpoint remained MCP anthropic v2 (not raw REST resource APIs).

## 7. Required PASS predicates (computed)

| Predicate | Value |
| --- | --- |
| OP1_EXACT_CONTACT_VERIFIED | UNKNOWN |
| OP1_LOCATION_BINDING_VERIFIED | UNKNOWN |
| OP2_EXACT_OPPORTUNITY_VERIFIED | UNKNOWN |
| OP2_LOCATION_BINDING_VERIFIED | UNKNOWN |
| OP2_PIPELINE_BINDING_VERIFIED | UNKNOWN |
| OP2_CONTACT_RELATIONSHIP_VERIFIED | UNKNOWN |
| OP2_EXPECTED_INITIAL_STAGE_VERIFIED | UNKNOWN |
| OP3_MCP_OPERATION_SUCCESS | UNKNOWN |
| OP3_CREATED_NOTE_ID_VERIFIED | **NO** |
| OP4_NOTE_READBACK_MATCH | **NO** |
| OP5_MCP_OPERATION_SUCCESS | UNKNOWN |
| OP6_FINAL_STAGE_MATCH | UNKNOWN |
| BUSINESS_CALL_COUNT_RECONCILED | **NO** |

Boundary flags (not all are PASS predicates, but material):

| Flag | Value |
| --- | --- |
| RETRY_USED | YES |
| SEARCH_CALLS_EXECUTED | 0 |
| LIST_CALLS_EXECUTED | 0 |
| PAGINATION_USED | NO |
| RAW_REST_FALLBACK_USED | NO |
| COMPENSATING_MUTATION_USED | NO |

## 8. Final reconciliation decision

Computation rule applied without manual override:

- Any required predicate = NO → `AT1_COMPLETION_RECONCILIATION=FAIL`, `AT1_COMPLETE=NO`.

```text
AT1_COMPLETION_RECONCILIATION=FAIL
AT1_COMPLETE=NO
STOP_CODE=NW008_AT1_LIVE_EXECUTION_RESULT008_RECONCILIATION_FAIL
```

Independent decisive NOs:

1. `OP3_CREATED_NOTE_ID_VERIFIED=NO` (`note_id_present=False`)
2. `OP4_NOTE_READBACK_MATCH=NO` (no note id match; content compare not performed)
3. `BUSINESS_CALL_COUNT_RECONCILED=NO` (initialize conflation + multi-attempt session ≠ exclusive 1+6 one-shot)

Additionally, multiple required predicates remain UNKNOWN due to absent response-body evidence, and `RETRY_USED=YES` violates the grant’s no-retry boundary even though FAIL is already compelled by the NOs above.

## 9. RESULT008_CLAIM_VS_RECONCILED_EVIDENCE

| Result 008 field / claim | Disposition | Reconciled basis |
| --- | --- | --- |
| `EXECUTION_RESULT=AT1_LIVE_SYNTHETIC_EXECUTION_SUCCESS` | CONTRADICTED | Required completion predicates not met |
| `AT1_COMPLETE=YES` | CONTRADICTED | `AT1_COMPLETE=NO` |
| `EXPECTED_INITIAL_STAGE_VERIFIED=YES` | CONTRADICTED (as verification) | Script placeholder; no r2 stage compare retained |
| `NOTE_WRITES_SUCCEEDED=1` | NOT_PROVEN | Top-level no JSON-RPC error only; note id absent |
| `NOTE_READBACK_VERIFIED=YES` | CONTRADICTED | Unconditional print; `note_id_present=False`; no content compare |
| `STAGE_WRITES_SUCCEEDED=1` | NOT_PROVEN | No nested success / envelope |
| `FINAL_STAGE_READBACK_VERIFIED=YES` | CONTRADICTED (as verification) | Unconditional print; no stage compare retained |
| `TOTAL_GHL_CALLS_EXECUTED=6` | CONTRADICTED / NOT_PROVEN | Runner printed 7 including initialize; prior attempts exist |
| `RETRY_USED=NO` | CONTRADICTED | Session shows failed attempt + re-probes + re-run |
| `SEARCH_CALLS_EXECUTED=0` | CONFIRMED | Script/session evidence |
| `LIST_CALLS_EXECUTED=0` | CONFIRMED | Script/session evidence |
| `PAGINATION_USED=NO` | CONFIRMED | Script/session evidence |
| `RAW_REST_FALLBACK_USED=NO` | CONFIRMED | MCP endpoint only |
| `COMPENSATING_MUTATION_USED=NO` | CONFIRMED | No compensating ops in script |
| `MCP_PROTOCOL_INITIALIZE_EXECUTED=YES` | CONFIRMED (success-claim run) | `INIT=OK` / server `ghl-mcp` |
| `CREATE_NOTE_TRANSPORT_HTTP=200` / `UPDATE_OPPORTUNITY_TRANSPORT_HTTP=200` | NOT_PROVEN | HTTP status codes not retained per op; only absence of urllib HTTPError path |
| Authorization window valid / grant SHA cited | CONFIRMED (metadata continuity) | Claim timestamps within grant window; grant SHA matches countersign commit — does not prove effects |
| Private binding non-publication | CONFIRMED | No private IDs in Result 008 |

## 10. Explicit non-actions during this reconciliation

```text
DID_NOT_CALL_GHL=YES
DID_NOT_MCP_INITIALIZE=YES
DID_NOT_EXECUTE_OPERATION=YES
DID_NOT_SEARCH=YES
DID_NOT_LIST=YES
DID_NOT_RETRY_EXECUTION=YES
DID_NOT_MUTATE_CRM=YES
DID_NOT_REWRITE_RESULT008=YES
DID_NOT_CREATE_COMPLETION_DECISION_ARTIFACT=YES
DID_NOT_PUBLISH_RAW_IDS_OR_BODIES=YES
ADDITIONAL_GHL_CALLS_EXECUTED=0
ADDITIONAL_MUTATION_CALLS_EXECUTED=0
```

## 11. STOP

```text
STOP_CODE=NW008_AT1_LIVE_EXECUTION_RESULT008_RECONCILIATION_FAIL
AT1_COMPLETION_RECONCILIATION=FAIL
AT1_COMPLETE=NO
RESULT008_COMMIT_SHA=2b901ca234e55952439a3a995e0b1d039e3aea68
AUTHORIZED_GRANT_008_SHA=cd2d25f26c3a07bfb2dcd3beb0c6310d2a592ce2
PR67_MERGE_SHA=2b504a546845fc3fdb848bc1dfd1912b041a48a3
GRANT_008_STATE=CONSUMED
RETRY_AUTHORIZED=NO
NEXT=AWAIT_HUMAN_OR_GOVERNANCE_DISPOSITION
```
