# NW-008 — E2E Runner Evidence Capability Reconciliation 001

```text
ARTIFACT_ID=NW008_E2E_RUNNER_EVIDENCE_CAPABILITY_RECONCILIATION_001
ARTIFACT_PATH=docs/nw008/nw-008-e2e-runner-evidence-capability-reconciliation-001.md
ARTIFACT_KIND=PLANNING_ONLY_RUNNER_EVIDENCE_CAPABILITY_RECONCILIATION
UNIT=NW008_E2E_RUNNER_EVIDENCE_CAPABILITY_RECONCILIATION_001
MODE=PLANNING_ONLY_CODE_EVIDENCE_RECONCILIATION
PR_CLASS=docs_planning

PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PUBLIC_BASE_SHA=a4574bffb62476ad279bba693f23f1fea8606507
PR250_MERGE_SHA=df438644f49535760dddbad07ef5467eaab46429
PR251_MERGE_SHA=a4574bffb62476ad279bba693f23f1fea8606507
PR250_MERGED=YES
PR251_MERGED=YES

BRANCH=plan/nw008-e2e-runner-evidence-capability-reconciliation-001
OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
HUMAN_MERGE_REQUIRED=YES
SELF_ACTIVATION=FORBIDDEN

CONTROLLING_ACCEPTANCE_CONTRACT=
  docs/nw008/nw-008-transcript-to-exact-ghl-contact-e2e-acceptance-001.md
ACCEPTANCE_CONTRACT_WEAKENED=NO

RECORDED_AT_UTC=2026-08-28T14:05:00Z
```

## 0. Purpose

Reconcile the **current** NW-008 AT-1 runner / evidence implementation against
**every** required PR #251 acceptance predicate and identify the **smallest**
remediation set required **before** any new one-shot GHL execution grant.

```text
RUNTIME_CODE_MUTATED=NO
LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
NEW_EXECUTION_AUTHORIZED=NO
NEW_GHL_MUTATION_AUTHORIZED=NO
ONE_SHOT_GRANT_CREATED=NO
GRANT008_REUSED=NO
SUBMISSION_READY=NO
```

This unit does **not** weaken PR #251 predicates, does **not** implement fixes,
and does **not** draft/countersign a grant.

## 1. Authority and surfaces

### 1.1 Controlling contract

```text
docs/nw008/nw-008-transcript-to-exact-ghl-contact-e2e-acceptance-001.md
  @ PR251_MERGE_SHA=a4574bffb62476ad279bba693f23f1fea8606507
```

Historical posture (inputs only; not re-litigated here):

```text
GRANT008_STATE=CONSUMED
AT1_COMPLETE=NO
PR250_RESULT=HISTORICAL_RESULT008_EVIDENCE_INSUFFICIENT
```

### 1.2 Targeted implementation surfaces (only)

| Path | Role |
| --- | --- |
| `src/integrations/ghl/bounded_at1_executor.py` | Six-op semantic sequence, attempt caps, identity/stage/note compares |
| `src/integrations/ghl/at1_live_transport_serializer.py` | Reviewed wire shape + write idempotency keys |
| `src/integrations/ghl/at1_live_transport_adapter.py` | Request/response capture order + layered MCP parse |
| `src/integrations/ghl/at1_execution_store.py` | Durable private envelopes/digests + sanitized public projection |

Direct tests:

| Path | Role |
| --- | --- |
| `tests/integrations/ghl/test_bounded_at1_executor.py` | Fixture executor caps / order / serializer shape |
| `tests/integrations/ghl/test_at1_live_transport_remediation.py` | Adapter+store+executor composition (b26–b38 evidence gates) |

### 1.3 Composition reality (verified)

```text
FIXTURE_EXECUTOR_ALONE=NETWORK_ENABLED=NO / GHL_LIVE_CLIENT=NO
LIVE_EVIDENCE_PATH=At1LiveTransportAdapter(dispatch) + At1ExecutionStore + BoundedAt1GhlExecutor(adapter)
COMPOSITION_TESTED_OFFLINE=YES
  # tests/integrations/ghl/test_at1_live_transport_remediation.py::_build_stack
PRODUCTION_LIVE_SESSION_CLIENT_IN_SCOPE_OF_THIS_RECON=NO
  # EstablishedSession is an injected Protocol; no live network client inspected here
```

Capability judgments below are for the **composed offline-proven stack**
(executor + serializer + adapter + store). Fixture-only executor without the
adapter **does not** satisfy PR #251 evidence persistence.

## 2. Status legend

```text
SUPPORTED   = current code enforces and (where required) evidences the predicate
PARTIAL     = related behavior exists but fails a PR251 required element
MISSING     = no implementation path for the predicate
NOT_APPLICABLE = not required by PR251 for this surface (unused in this matrix)
```

`REMEDIATION_REQUIRED=YES` when STATUS is PARTIAL or MISSING for a **required**
PR #251 predicate.

## 3. Predicate matrix (required minimum set)

### 3.1 Transcript / prewrite content lane

```text
PREDICATE=TRANSCRIPT_INGESTED
STATUS=MISSING
SOURCE_PATH=N/A (not present under targeted surfaces)
SOURCE_SYMBOL_OR_TEST=N/A
EVIDENCE=No transcript artifact intake, binding field, store table, or executor pre-step exists. BoundedAt1Input fields are location/contact/opportunity/stages/note only.
GAP=PR251 §3.1 requires a concrete synthetic transcript bound into the run package before GHL business calls.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=TRANSCRIPT_HASH_CAPTURED
STATUS=MISSING
SOURCE_PATH=N/A
SOURCE_SYMBOL_OR_TEST=N/A
EVIDENCE=No TRANSCRIPT_SHA256 computation or persistence in executor/store/adapter.
GAP=PR251 requires TRANSCRIPT_SHA256 prewrite capture and sanitized public projection of the digest.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=BoundedAt1Input.expected_note_content_or_fingerprint ; execute() create-note args
EVIDENCE=Note body/fingerprint is a required binding string used as create-note body via serializer `_body_for` (`content_or_fingerprint` → `params.body.body`). Readback compares exact equality to the same binding field. There is no SHA256, no prewrite hash seal timestamp, and no transcript→note derivation proof.
GAP=PR251 §3.1/§6 require EXPECTED_NOTE_SHA256 captured before create-note dispatch, body hash match, and transcript-derived provenance—not only a pre-supplied binding string.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED
STATUS=MISSING
SOURCE_PATH=src/integrations/ghl/at1_live_transport_serializer.py
SOURCE_SYMBOL_OR_TEST=At1LiveTransportSerializer._body_for
EVIDENCE=Body is copied from binding string; no hashlib of request body; store has no EXPECTED_NOTE_SHA256 / CREATE_NOTE_BODY_SHA256 fields.
GAP=Explicit prewrite expected hash + dispatch body hash compare required by PR251 §6.
REMEDIATION_REQUIRED=YES
```

### 3.2 Exact contact binding / prewrite read

```text
PREDICATE=EXACT_TARGET_CONTACT_BOUND
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=BoundedAt1Input.contact_id ; from_mapping exact field set
EVIDENCE=Non-empty contact_id required; no search/list/pagination in EXACT_OPERATION_ORDER; serializer get-contact path is contactId only.
GAP=None for binding presence. (Values remain synthetic/private in live packages.)
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=EXACT_TARGET_CONTACT_PREWRITE_READ_VERIFIED
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=BoundedAt1GhlExecutor.execute OP1 get-contact + _identity_from_record
EVIDENCE=First business op is get-contact; fails CONTACT_NOT_FOUND / CONTACT_ID_MISMATCH unless returned identity equals binding.contact_id. Composed stack uses adapter layered parse before FixtureResponse ok.
GAP=None for contact-id prewrite verify.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=CONTACT_LOCATION_BINDING_MATCH
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=BoundedAt1Input.location_id ; execute() OP1
EVIDENCE=location_id is a required binding field and is passed into executor dispatch args, but serializer get-contact wire path is **only** `contactId` (location not on wire). OP1 success path never compares a returned contact location field to binding.location_id.
GAP=PR251 §3.2 requires location match against authorized binding package after prewrite read.
REMEDIATION_REQUIRED=YES
```

### 3.3 Note write

```text
PREDICATE=CREATE_NOTE_ATTEMPTS
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=_consume_write_attempt("note") ; NOTE_WRITE_ATTEMPTS_MAX=1
EVIDENCE=Second note write refused pre-transport (WriteAttemptRefusedError). Store projection counts create-note attempts. Tests: fixture caps + remediation stack.
GAP=None.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=CREATE_NOTE_NESTED_OPERATION_SUCCESS
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py
SOURCE_SYMBOL_OR_TEST=At1LiveTransportAdapter._parse_response
EVIDENCE=Layered gate: request id match; JSON-RPC error absent; result.isError is False; nested.operationId match; nested.success is True; nested.status in 200..299; payload mapping. Failure codes include MCP_OPERATION_NOT_SUCCESS. Test: test_b26_is_error_true_fails_closed.
GAP=None for enforcement on composed live-transport path. (Fixture-only transport without adapter does not perform nested MCP parse.)
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=CREATED_NOTE_ID_PRESENT
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() post create-note note_id extraction
EVIDENCE=Requires non-empty str note_id from payload; else NOTE_WRITE_RESPONSE_INVALID and OP4 not constructed. Test: test_b27_missing_created_note_id_blocks_op4.
GAP=None.
REMEDIATION_REQUIRED=NO
```

### 3.4 Same-run note readback

```text
PREDICATE=NOTE_READBACK_BY_CREATED_NOTE_ID
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP4 get-note with note_id from OP3
EVIDENCE=get-note uses created note_id; serializer path requires contactId+id; missing id blocks before OP4.
GAP=None.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=READBACK_NOTE_ID_MATCH
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() note.record note_id compare
EVIDENCE=Fails NOTE_READBACK_MISMATCH if returned note_id != created note_id.
GAP=None.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=NOTE_READBACK_CONTACT_ID_MATCH
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP4
EVIDENCE=Request includes binding.contact_id. Response contact association is **not** read or compared. Content/id compares only.
GAP=PR251 §3.4 requires returned contact association equals exact bound contact (private compare).
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=NOTE_READBACK_CONTENT_OR_HASH_MATCH
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() content_or_fingerprint equality
EVIDENCE=Exact-bytes compare of returned content_or_fingerprint to binding.expected_note_content_or_fingerprint (PR251 allows SHA256 **or** EXACT_BYTES). Test: test_b29_wrong_note_content_preserves_partial_effect_without_stage_write.
GAP=Comparator mode not exported as NOTE_CONTENT_COMPARATOR public flag; SHA256 form not implemented (allowed alternative missing, exact path present).
REMEDIATION_REQUIRED=NO
  # Exact-bytes path satisfies PR251 OR. Optional hardening: export comparator flag.
```

```text
PREDICATE=CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP4 get-note
EVIDENCE=Successful get-note under request contactId+created id with content/id match is a same-run visibility signal. No get-all-notes / inventory confirmation; no response-side contact association verify (ties to NOTE_READBACK_CONTACT_ID_MATCH gap).
GAP=PR251 treats inventory as optional **if used**, but still requires contact association match. Without response contact compare, visibility under exact contact is not fully proven.
REMEDIATION_REQUIRED=YES
```

### 3.5 Stage / opportunity path

```text
PREDICATE=EXPECTED_INITIAL_STAGE_VERIFIED
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP2 stage_id == expected_initial_stage_id
EVIDENCE=INITIAL_STAGE_MISMATCH fails closed before writes. Flag projected via store semantic_success on ordinal 2 / executor field. Test: test_b28_wrong_initial_stage_blocks_writes.
GAP=None for stage-id compare.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=OPPORTUNITY_CONTACT_RELATION_MATCH
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP2
EVIDENCE=OP2 verifies opportunity identity + initial stage only. No compare of opportunity.contact_id (or equivalent) to binding.contact_id.
GAP=PR251 §3.5 requires contact relation verify on prewrite get-opportunity.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=OPPORTUNITY_PIPELINE_MATCH
STATUS=MISSING
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=BoundedAt1Input (no pipeline field)
EVIDENCE=PIPELINE_METADATA_RUNTIME_READ_REQUIRED="NO". Binding has no pipeline_id; OP2 does not compare pipeline.
GAP=PR251 §3.5 requires pipeline match for stage path.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=OPPORTUNITY_LOCATION_MATCH
STATUS=MISSING
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP2
EVIDENCE=location_id in binding/args but serializer get-opportunity path is id-only; no returned location compare.
GAP=PR251 §3.5 requires location match on opportunity prewrite read.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=STAGE_UPDATE_NESTED_OPERATION_SUCCESS
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py
SOURCE_SYMBOL_OR_TEST=_parse_response + execute() OP5 update-opportunity
EVIDENCE=Same layered nested success gate as other ops; attempt cap 1; opportunity id re-check on write response. Serializer body uses pipelineStageId.
GAP=None for nested success enforcement on composed path.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=FINAL_STAGE_READBACK_MATCH
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/bounded_at1_executor.py
SOURCE_SYMBOL_OR_TEST=execute() OP6 stage_id == authorized_final_stage_id
EVIDENCE=STAGE_READBACK_MISMATCH fail-closed; preserve_proof path. Test: test_b30_wrong_final_stage_fails_completion_and_preserves_consumed_stage_attempt.
GAP=None.
REMEDIATION_REQUIRED=NO
```

### 3.6 Per-call evidence schema

```text
PREDICATE=REQUEST_EVIDENCE_PERSISTED
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py ; at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=dispatch() record_attempt ; At1ExecutionStore.record_attempt
EVIDENCE=Request envelope JSON + digest stored before dispatch mark. Test: test_b35_private_capture_and_sanitized_projection ; test_b38_request_response_evidence_pair_and_public_binding.
GAP=None for private persistence on composed path.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=RESPONSE_EVIDENCE_PERSISTED
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py ; at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=dispatch() capture_response before _parse_response
EVIDENCE=Response envelope captured before layered parse; crash-window refusals tested (b36*).
GAP=None for private persistence on composed path.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=JSONRPC_ERROR_PRESENT
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py
SOURCE_SYMBOL_OR_TEST=_parse_response JSONRPC_ERROR_PRESENT failure_code
EVIDENCE=Enforced at parse time. Not stored as a first-class per-call public field; only private envelopes + parse_success/terminal codes.
GAP=PR251 §5 public projection schema requires explicit JSONRPC_ERROR_PRESENT per call.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=MCP_IS_ERROR
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py
SOURCE_SYMBOL_OR_TEST=_parse_response result.isError is not False → MCP_IS_ERROR_TRUE
EVIDENCE=Enforced. Not first-class public per-call field.
GAP=PR251 §5 requires MCP_IS_ERROR in sanitized per-call projection.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=NESTED_OPERATION_SUCCESS
STATUS=PARTIAL
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py ; at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=_parse_response nested.success ; parse_success column
EVIDENCE=Enforced; parse_success persisted privately. Public projection does not emit NESTED_OPERATION_SUCCESS boolean per ordinal (only commitments + aggregate flags).
GAP=PR251 §5 first-class per-call NESTED_OPERATION_SUCCESS field in sanitized projection.
REMEDIATION_REQUIRED=YES
```

```text
PREDICATE=REQUEST_RESPONSE_CORRELATION_ID
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_live_transport_adapter.py ; at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=request_id = f"{grant_run_id}:{ordinal}:{uuid4().hex}" ; response.id must match
EVIDENCE=Correlated request/response; mismatch → JSONRPC_REQUEST_ID_MISMATCH. Public commitments include request_id.
GAP=None.
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=SANITIZED_REQUEST_DIGEST
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=request_digest / public request_commitment
EVIDENCE=HMAC-SHA256 commitment over canonical request JSON; published without raw envelopes. test_b35 / test_b38.
GAP=None for digest form (named request_commitment in projection).
REMEDIATION_REQUIRED=NO
```

```text
PREDICATE=SANITIZED_RESPONSE_DIGEST
STATUS=SUPPORTED
SOURCE_PATH=src/integrations/ghl/at1_execution_store.py
SOURCE_SYMBOL_OR_TEST=response_digest / public response_commitment
EVIDENCE=Same commitment pattern for response; published per ordinal.
GAP=None for digest form.
REMEDIATION_REQUIRED=NO
```

### 3.7 Cross-cutting known observations (independently verified)

| Observation | Verified status | Notes |
| --- | --- | --- |
| CREATED_NOTE_ID_EXTRACTION | **SUPPORTED** | Executor gates non-empty note_id; b27 |
| NOTE_ID_AND_CONTENT_READBACK | **SUPPORTED** | Id + exact content compare; b29 |
| INITIAL_AND_FINAL_STAGE_COMPARE | **SUPPORTED** | OP2 + OP6 stage_id compares; b28/b30 |
| RAW_REQUEST_RESPONSE_CAPTURE | **SUPPORTED** | Private envelope JSON columns; capture-before-parse |
| NESTED_MCP_SUCCESS_PARSE | **SUPPORTED** | Adapter layered parse |
| TRANSCRIPT_TO_NOTE_HASH_PROVENANCE | **MISSING** | No transcript lane / note SHA256 seal |
| RETURNED_NOTE_CONTACT_ASSOCIATION_COMPARE | **PARTIAL** | Request contact only; no response contact compare |
| OPPORTUNITY_CONTACT_PIPELINE_LOCATION_COMPARE | **MISSING/PARTIAL** | Contact relation PARTIAL; pipeline+location MISSING |
| PER_CALL_SANITIZED_PUBLIC_PROJECTION | **PARTIAL** | Commitments+request_id present; missing HTTP_STATUS, JSONRPC_ERROR_PRESENT, MCP_IS_ERROR, NESTED_OPERATION_SUCCESS, TARGET_BINDING_MATCH fields |

## 4. Counts

Required minimum predicates adjudicated in §3.1–§3.6 (29 rows):

```text
SUPPORTED_COUNT=16
PARTIAL_COUNT=8
MISSING_COUNT=5
NOT_APPLICABLE_COUNT=0
REMEDIATION_REQUIRED_PREDICATE_COUNT=13
```

Breakdown:

| STATUS | Predicates |
| --- | --- |
| SUPPORTED | EXACT_TARGET_CONTACT_BOUND; EXACT_TARGET_CONTACT_PREWRITE_READ_VERIFIED; CREATE_NOTE_ATTEMPTS; CREATE_NOTE_NESTED_OPERATION_SUCCESS; CREATED_NOTE_ID_PRESENT; NOTE_READBACK_BY_CREATED_NOTE_ID; READBACK_NOTE_ID_MATCH; NOTE_READBACK_CONTENT_OR_HASH_MATCH; EXPECTED_INITIAL_STAGE_VERIFIED; STAGE_UPDATE_NESTED_OPERATION_SUCCESS; FINAL_STAGE_READBACK_MATCH; REQUEST_EVIDENCE_PERSISTED; RESPONSE_EVIDENCE_PERSISTED; REQUEST_RESPONSE_CORRELATION_ID; SANITIZED_REQUEST_DIGEST; SANITIZED_RESPONSE_DIGEST |
| PARTIAL | TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE; CONTACT_LOCATION_BINDING_MATCH; NOTE_READBACK_CONTACT_ID_MATCH; CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT; OPPORTUNITY_CONTACT_RELATION_MATCH; JSONRPC_ERROR_PRESENT; MCP_IS_ERROR; NESTED_OPERATION_SUCCESS |
| MISSING | TRANSCRIPT_INGESTED; TRANSCRIPT_HASH_CAPTURED; CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED; OPPORTUNITY_PIPELINE_MATCH; OPPORTUNITY_LOCATION_MATCH |

## 5. Minimum remediation set (planning only; not implemented here)

Ordered smallest-change set to make every required PR #251 predicate **SUPPORTED**.
No runtime changes in this unit.

### R1 — Transcript + prewrite note hash provenance (blocking)

```text
PATHS=
  src/integrations/ghl/bounded_at1_executor.py
  src/integrations/ghl/at1_execution_store.py
  tests/integrations/ghl/test_at1_live_transport_remediation.py (new cases)
  tests/integrations/ghl/test_bounded_at1_executor.py (as needed)

SYMBOLS=
  new prewrite intake on execute() or adjacent run package binder
  store fields/table for transcript_sha256 + expected_note_sha256 + capture_at
  create-note dispatch body sha256 compare

MINIMUM_CHANGE=
  1. Accept synthetic transcript bytes (or sealed private ref) in run package.
  2. Compute TRANSCRIPT_SHA256; persist private + project digest public.
  3. Derive or bind canonical note bytes; compute EXPECTED_NOTE_SHA256 prewrite;
     refuse write if capture_at missing or after first write ordinal.
  4. On create-note serialize body; compute CREATE_NOTE_BODY_SHA256; require match.
  5. Export NOTE_CONTENT_COMPARATOR=SHA256|EXACT_BYTES consistently with compare path.

CLOSES=
  TRANSCRIPT_INGESTED
  TRANSCRIPT_HASH_CAPTURED
  TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE
  CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED
  TRANSCRIPT_TO_NOTE_HASH_PROVENANCE
```

### R2 — Response-side binding compares (contact / opportunity)

```text
PATHS=
  src/integrations/ghl/bounded_at1_executor.py
  tests/integrations/ghl/test_at1_live_transport_remediation.py
  tests/integrations/ghl/test_bounded_at1_executor.py

SYMBOLS=
  BoundedAt1Input (+ optional pipeline_id field — exact field-set change)
  execute() OP1/OP2/OP4 semantic compares

MINIMUM_CHANGE=
  1. After OP1 ok: compare returned contact location (reviewed payload field) to
     binding.location_id → CONTACT_LOCATION_BINDING_MATCH.
  2. After OP2 ok: compare opportunity contact relation to binding.contact_id;
     compare pipeline to binding.pipeline_id (add exact binding field);
     compare opportunity location to binding.location_id.
  3. After OP4 ok: compare returned note contact association to binding.contact_id
     (closes NOTE_READBACK_CONTACT_ID_MATCH and strengthens
     CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT).
  4. Fail closed with distinct failure codes; no placeholder YES.

CLOSES=
  CONTACT_LOCATION_BINDING_MATCH
  OPPORTUNITY_CONTACT_RELATION_MATCH
  OPPORTUNITY_PIPELINE_MATCH
  OPPORTUNITY_LOCATION_MATCH
  NOTE_READBACK_CONTACT_ID_MATCH
  CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT (with R2.3)
  RETURNED_NOTE_CONTACT_ASSOCIATION_COMPARE
  OPPORTUNITY_CONTACT_PIPELINE_LOCATION_COMPARE
```

### R3 — Per-call sanitized public projection schema (PR251 §5)

```text
PATHS=
  src/integrations/ghl/at1_live_transport_adapter.py
  src/integrations/ghl/at1_execution_store.py
  tests/integrations/ghl/test_at1_live_transport_remediation.py (extend b35/b38)

SYMBOLS=
  _parse_response outcome metadata persistence
  compute_public_projection per-attempt object

MINIMUM_CHANGE=
  Persist and project per ordinal (sanitized, no raw ids/bodies/tokens):
    OPERATION_ID
    HTTP_STATUS              # from nested.status when parse reaches it; else UNKNOWN
    JSONRPC_ERROR_PRESENT
    MCP_IS_ERROR
    NESTED_OPERATION_SUCCESS
    TARGET_BINDING_MATCH     # filled after executor semantic compare hooks
    REQUEST_EVIDENCE_PERSISTED
    RESPONSE_EVIDENCE_PERSISTED
    REQUEST_RESPONSE_CORRELATION_ID  # existing request_id
    SANITIZED_REQUEST_DIGEST         # existing request_commitment
    SANITIZED_RESPONSE_DIGEST        # existing response_commitment
  Keep private full envelopes; do not publish raw payloads.

CLOSES=
  JSONRPC_ERROR_PRESENT (as public/schema field)
  MCP_IS_ERROR (as public/schema field)
  NESTED_OPERATION_SUCCESS (as public/schema field)
  PER_CALL_SANITIZED_PUBLIC_PROJECTION
```

### R4 — Explicit non-goals of the minimum set

```text
DO_NOT_REUSE_GRANT008=YES
DO_NOT_ADD_SEARCH_LIST_PAGINATION=YES
DO_NOT_ADD_AUTOMATIC_RETRY=YES
DO_NOT_ADD_COMPENSATING_CLEANUP=YES
DO_NOT_IMPLEMENT_LIVE_NETWORK_CLIENT_IN_REMEDIATION_UNLESS_SEPARATELY_AUTHORIZED=YES
DO_NOT_WEAKEN_PR251_PREDICATES=YES
```

## 6. Final classification

```text
RUNNER_E2E_EVIDENCE_CAPABILITY=READY_WITH_REMEDIATION
```

Rationale:

1. Core AT1 CRM spine is offline-proven: six-op order, write caps, nested MCP
   parse, created-note id gate, note id+content readback, initial/final stage
   compares, private request/response capture, correlation ids, sanitized
   digests (tests b26–b38).
2. PR #251 acceptance object is **transcript → exact contact → note (+ stage)**
   with explicit prewrite hashes and fuller binding compares. Those requirements
   are **not** fully met today (5 MISSING + 8 PARTIAL).
3. Gaps are bounded to R1–R3 above; not a greenfield rewrite.

```text
GRANT_PREPARATION_READY=NO
```

`GRANT_PREPARATION_READY=YES` is forbidden until every required PR #251 predicate
is SUPPORTED from current runner/evidence behavior. That bar is **not** met.

```text
SUBMISSION_READY=NO
NEW_EXECUTION_AUTHORIZED=NO
ONE_SHOT_GRANT_CREATED=NO
```

## 7. Explicit non-actions

```text
DID_NOT_MODIFY_RUNTIME_CODE=YES
DID_NOT_EXECUTE_GHL=YES
DID_NOT_CREATE_NOTE=YES
DID_NOT_UPDATE_OPPORTUNITY=YES
DID_NOT_DRAFT_ONE_SHOT_GRANT=YES
DID_NOT_COUNTERSIGN=YES
DID_NOT_REUSE_GRANT008=YES
DID_NOT_DEPLOY=YES
DID_NOT_CHANGE_IAM=YES
DID_NOT_CHANGE_SECRETS=YES
DID_NOT_WEAKEN_PR251=YES

LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
DEPLOYMENTS=0
```

## 8. Return block

```text
ARTIFACT_ID=NW008_E2E_RUNNER_EVIDENCE_CAPABILITY_RECONCILIATION_001
ARTIFACT_PATH=docs/nw008/nw-008-e2e-runner-evidence-capability-reconciliation-001.md

PR250_MERGED=YES
PR250_MERGE_SHA=df438644f49535760dddbad07ef5467eaab46429
PR251_MERGED=YES
PR251_MERGE_SHA=a4574bffb62476ad279bba693f23f1fea8606507

RUNNER_E2E_EVIDENCE_CAPABILITY=READY_WITH_REMEDIATION
SUPPORTED_COUNT=16
PARTIAL_COUNT=8
MISSING_COUNT=5
REMEDIATION_REQUIRED=YES
GRANT_PREPARATION_READY=NO

LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
SUBMISSION_READY=NO
NEW_EXECUTION_AUTHORIZED=NO
ONE_SHOT_GRANT_CREATED=NO
GRANT008_REUSED=NO

NEXT=IMPLEMENT_R1_R2_R3_RUNNER_EVIDENCE_REMEDIATION_UNDER_SEPARATE_AUTH_THEN_RE_RECONCILE
STOP_CODE=NW008_E2E_RUNNER_EVIDENCE_CAPABILITY_RECONCILIATION_001_READY_WITH_REMEDIATION_NO_GRANT
```

## 9. Stop

Open **one** planning-only PR with this artifact. Do not merge automatically.
Do not execute GHL. Do not draft or countersign a one-shot execution grant.
Return the PR to ChatGPT for governance review before any remediation
implementation authorization.
