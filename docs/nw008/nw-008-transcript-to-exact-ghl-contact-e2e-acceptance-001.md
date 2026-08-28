# NW-008 — Transcript → Exact GHL Contact E2E Acceptance 001

```text
ARTIFACT_ID=NW008_TRANSCRIPT_TO_EXACT_GHL_CONTACT_E2E_ACCEPTANCE_001
ARTIFACT_PATH=docs/nw008/nw-008-transcript-to-exact-ghl-contact-e2e-acceptance-001.md
ARTIFACT_KIND=PLANNING_ONLY_E2E_ACCEPTANCE_CONTRACT
UNIT=NW008_TRANSCRIPT_TO_EXACT_GHL_CONTACT_E2E_ACCEPTANCE_001
MODE=PLANNING_ONLY
PR_CLASS=docs_planning

PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PUBLIC_BASE_SHA=a75b8e49b65f5e2c548aa04888e393b3a26b006f
BRANCH=plan/nw008-transcript-to-exact-ghl-contact-e2e-acceptance-001

OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
HUMAN_MERGE_REQUIRED=YES
SELF_ACTIVATION=FORBIDDEN

RECORDED_AT_UTC=2026-08-28T13:50:19Z
```

## 0. Purpose

Define a **fresh governed acceptance contract** for **one** end-to-end synthetic
run that proves:

```text
synthetic transcript
  → transcript-derived note content (prewrite hash)
  → exact bound GHL contact (prewrite read)
  → single create-note write
  → same-run verified note readback
  → (required) single stage update + same-run final stage readback
```

This artifact is **planning only**. It does **not** authorize execution, does
**not** consume a grant, and does **not** perform CRM mutation.

```text
EXECUTION_AUTHORIZED=NO
NEW_EXECUTION_AUTHORIZED=NO
NEW_GHL_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO
GRANT008_REUSED=NO
```

## 1. Authority state (frozen inputs)

```text
GRANT008_STATE=CONSUMED
GRANT008_REUSABLE=NO
AT1_COMPLETE=NO

PR250_RESULT=HISTORICAL_RESULT008_EVIDENCE_INSUFFICIENT
PR250_STATE=OPEN_AT_PLANNING_TIME
PR250_HEAD_SHA=0ca28c07fa18d61dee944e8ec718c2788446eef6
  # Controlling historical audit finding: Result-008 success/readback claims
  # lack independent retained evidence; Grant 008 remains consumed and not reusable.

CURRENT_PROVIDER_STATE_AUTHORITY=PR249
PR249_MERGE_SHA=a75b8e49b65f5e2c548aa04888e393b3a26b006f
CURRENT_GRANT008_TARGET_IDENTITY_RECONFIRMED=YES
CURRENT_GRANT008_END_STATE_RECONFIRMED=NO

NEW_EXECUTION_AUTHORIZED=NO
NEW_GHL_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO
```

### 1.1 Why a new contract is required

| Prior surface | What it proved / failed to prove | Reuse posture |
| --- | --- | --- |
| Grant 008 + Result 008 claim | Claimed note+stage success; readback YES flags | **CONSUMED**; not reusable |
| PR #68 Result-008 reconciliation | Completion FAIL; missing envelopes; `note_id_present=False` | Controlling historical evidence |
| PR #69 completion decision | `AT1_COMPLETE=NO`; business effect partially unknown | Terminal for Grant 008 |
| PR #249 current record recon | Exact contact/opp identity MATCH; note absent; stage=initial | Current provider inventory only |
| PR #250 historical audit | `RESULT=HISTORICAL_RESULT008_EVIDENCE_INSUFFICIENT` | Does not authorize repair or rerun |
| Contest critical-path rebase | `INGESTION_TO_LIVE_GHL_SINGLE_RUN_PROVEN=NO` | Documents the gap this contract closes |

```text
DO_NOT_REUSE_GRANT008=YES
DO_NOT_TREAT_RESULT008_AS_E2E_PROOF=YES
DO_NOT_TREAT_PR249_INVENTORY_AS_WRITE_PROOF=YES
FUTURE_LIVE_RUN_REQUIRES_SEPARATE_ONE_SHOT_HUMAN_GRANT=YES
```

## 2. Acceptance object (what “done” means)

A future one-shot human-authorized **synthetic-only** live run **passes** this
contract only when **all** required machine-verifiable predicates below evaluate
to `YES` from **retained same-run evidence**, with **no** unconditional success
flags and **no** automatic retry.

```text
ACCEPTANCE_OBJECT=
  ONE_FRESH_SYNTHETIC_TRANSCRIPT_TO_EXACT_GHL_CONTACT_NOTE_AND_STAGE_E2E_RUN

AUTHORIZED_RECORD_CLASS=SYNTHETIC_ONLY
NON_SYNTHETIC_RECORD_MUTATION_AUTHORIZED=NO
JUDGE_DEMO_LIVE_GHL_MUTATION=NO
DEMO_FIXTURE_IDS_PRESUMED_EQUAL_LIVE_GHL=NO
```

### 2.1 Stage advancement requirement

Stage advancement **is required** for this acceptance object (AT1-parity “right
action” package: note create + opportunity stage update under one run).

```text
STAGE_ADVANCEMENT_REQUIRED=YES
RUNNER_CAN_PROVE_STAGE_READBACK=YES   # capability required by contract
```

Minimum contest gap closed by note-path alone is acknowledged, but this contract
does **not** accept note-only as full E2E acceptance.

## 3. Same-run business proof predicates (required)

All predicates are **required**. Evaluation is fail-closed.

### 3.1 Transcript / prewrite content lane

```text
TRANSCRIPT_INGESTED=YES
TRANSCRIPT_HASH_CAPTURED=YES
TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE=YES
```

Machine rules:

1. A concrete synthetic transcript artifact is bound into the run package before
   any GHL business call.
2. `TRANSCRIPT_SHA256` is computed over the canonical transcript bytes and
   persisted in the private run evidence store **and** projected sanitized to
   public proof (`TRANSCRIPT_SHA256=` only; raw transcript may remain private if
   policy requires).
3. Transcript-derived note body (or canonical note text used for write) is
   finalized **prewrite**.
4. `EXPECTED_NOTE_SHA256` is computed over the exact bytes that will be sent as
   the note body and captured **before** `create-note` dispatch.
5. Prewrite note hash capture timestamp ≤ first write dispatch timestamp.

```text
PREWRITE_NOTE_HASH_AFTER_WRITE_FORBIDDEN=YES
NOTE_BODY_MUTATION_AFTER_HASH_FORBIDDEN=YES
```

### 3.2 Exact contact binding / prewrite read

```text
EXACT_TARGET_CONTACT_BOUND=YES
EXACT_TARGET_CONTACT_PREWRITE_READ_VERIFIED=YES
```

Machine rules:

1. Private binding ref for the exact synthetic contact is present in the private
   execution package (value not published).
2. A prewrite `get-contact` (or equivalent exact-get) is executed against that
   binding only — no search, list, or pagination to “find” a contact.
3. Layered transport success (Section 5) is required for the prewrite read.
4. Returned contact identity matches the bound contact (private compare).
5. Location (and any required synthetic-class markers policy demands) match the
   authorized binding package.
6. Public proof records match flags only:

```text
EXACT_TARGET_CONTACT_BOUND=YES|NO
EXACT_TARGET_CONTACT_PREWRITE_READ_VERIFIED=YES|NO
CONTACT_LOCATION_BINDING_MATCH=YES|NO
RAW_CONTACT_ID_PUBLISHED=NO
```

### 3.3 Note write (single attempt)

```text
CREATE_NOTE_ATTEMPTS=1
CREATE_NOTE_NESTED_OPERATION_SUCCESS=YES
CREATED_NOTE_ID_PRESENT=YES
```

Machine rules:

1. Exactly one `create-note` attempt is authorized and observed.
2. Request body bytes’ SHA256 equals prewrite `EXPECTED_NOTE_SHA256`.
3. Layered success required (Section 5); top-level path progress alone is
   **insufficient**.
4. Created note id is extracted from the reviewed response schema field(s) and
   is non-empty.
5. If `CREATED_NOTE_ID_PRESENT=NO`, the run **stops** before any note readback
   construction; predicates depending on note id are `NO` (not placeholder YES).

```text
CREATE_NOTE_ATTEMPTS_MAX=1
AUTOMATIC_RETRY_ON_NOTE_WRITE=NO
RAW_REST_FALLBACK=NO
ALTERNATE_OPERATION=NO
```

### 3.4 Same-run note readback

```text
NOTE_READBACK_BY_CREATED_NOTE_ID=YES
NOTE_READBACK_CONTACT_ID_MATCH=YES
NOTE_READBACK_CONTENT_OR_HASH_MATCH=YES
CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT=YES
```

Machine rules:

1. Readback uses the **created note id from this run** (not a guessed id, not
   empty, not a prior-run id).
2. Layered success required for the readback operation.
3. Returned note id equals created note id (private compare).
4. Returned contact association equals the exact bound contact (private compare).
5. Returned note body SHA256 equals `EXPECTED_NOTE_SHA256` **or** exact content
   equality against the prewrite canonical note bytes (implementation may use
   either; public proof must show which comparator was used).
6. Optional/additional exact-contact notes inventory read (if used) must show the
   created note id present under the exact contact; inventory-only presence
   without id+content match is **not** sufficient for
   `NOTE_READBACK_CONTENT_OR_HASH_MATCH`.

```text
UNCONDITIONAL_NOTE_READBACK_YES_FORBIDDEN=YES
GET_NOTE_WITH_NULL_NOTE_ID_FORBIDDEN=YES
```

### 3.5 Stage path (required)

```text
EXPECTED_INITIAL_STAGE_VERIFIED=YES
STAGE_UPDATE_ATTEMPTS=1
STAGE_UPDATE_NESTED_OPERATION_SUCCESS=YES
FINAL_STAGE_READBACK_MATCH=YES
```

Machine rules:

1. Exact synthetic opportunity is bound privately; prewrite `get-opportunity`
   verifies opportunity identity, contact relation, pipeline, and **expected
   initial stage** before any stage write.
2. Exactly one `update-opportunity` stage-write attempt.
3. Layered nested operation success required for the stage write.
4. Final `get-opportunity` layered success + returned stage equals authorized
   final stage binding (private compare).
5. Public proof records stage class / match flags only — no raw stage ids.

```text
STAGE_UPDATE_ATTEMPTS_MAX=1
AUTOMATIC_RETRY_ON_STAGE_WRITE=NO
COMPENSATING_STAGE_MUTATION=NO
```

## 4. Required operation order (normative)

Default AT1-parity order for the CRM segment of the run:

```text
OP_ORDER=
  1. get-contact                 # exact bound contact prewrite
  2. get-opportunity             # exact bound opportunity + initial stage
  3. create-note                 # single attempt; body = prewrite note bytes
  4. get-note                    # by created note id + contact id
  5. update-opportunity          # single stage write to authorized final
  6. get-opportunity             # final stage readback
```

Transcript ingestion and note-hash prewrite occur **before OP1** (or before the
first write, with hash sealed before OP3). They are part of the same run package
and same evidence root.

```text
SEARCH=NO
LIST=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO
COMPENSATING_MUTATION=NO
AUTOMATIC_CLEANUP=NO
```

Any extra business call beyond the authorized modeled set fails the run unless a
future grant explicitly freezes a different capped surface. This planning
contract freezes the six-call CRM surface above plus non-business transcript
prep.

## 5. Per-call evidence schema (mandatory)

For **each** business call, the runner must retain private request/response
evidence and emit a sanitized public projection containing at least:

```text
OPERATION_ID=
HTTP_STATUS=
JSONRPC_ERROR_PRESENT=YES|NO|UNKNOWN
MCP_IS_ERROR=YES|NO|UNKNOWN
NESTED_OPERATION_SUCCESS=YES|NO|UNKNOWN
TARGET_BINDING_MATCH=YES|NO|NOT_APPLICABLE|UNKNOWN
RESPONSE_EVIDENCE_PERSISTED=YES|NO
REQUEST_EVIDENCE_PERSISTED=YES|NO
REQUEST_RESPONSE_CORRELATION_ID=
SANITIZED_REQUEST_DIGEST=
SANITIZED_RESPONSE_DIGEST=
```

Layered success gate (all required for `NESTED_OPERATION_SUCCESS=YES`):

```text
1. RESPONSE_EVIDENCE_PERSISTED=YES
2. valid JSON-RPC response for correlated request
3. JSONRPC_ERROR_PRESENT=NO
4. MCP_IS_ERROR=NO (explicit)
5. nested operation success/status explicitly success per reviewed schema
6. operation-specific identity/value schema satisfied
```

```text
TOP_LEVEL_PATH_PROGRESS_ALONE_INSUFFICIENT=YES
HTTP_200_ALONE_INSUFFICIENT=YES
ABSENCE_OF_URLLIB_ERROR_ALONE_INSUFFICIENT=YES
HARDCODED_SUCCESS_FLAGS_FORBIDDEN=YES
PLACEHOLDER_YES_PRINTS_FORBIDDEN=YES
RESULT_FLAGS_MUST_BE_COMPUTED_FROM_EVIDENCE=YES
```

Missing evidence ⇒ predicate `UNKNOWN` or `NO` ⇒ acceptance FAIL (Section 7).

## 6. Note evidence schema (mandatory)

```text
EXPECTED_NOTE_SHA256=
EXPECTED_NOTE_SHA256_CAPTURED_PREWRITE=YES|NO
CREATE_NOTE_BODY_SHA256=
CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED=YES|NO

CREATED_NOTE_ID_PRESENT=YES|NO
CREATED_NOTE_ID_FINGERPRINT=   # optional salted/fingerprint form for public proof; raw id private

READBACK_NOTE_ID_MATCH=YES|NO
READBACK_CONTACT_MATCH=YES|NO
READBACK_NOTE_SHA256=
NOTE_CONTENT_MATCH=YES|NO
NOTE_CONTENT_COMPARATOR=SHA256|EXACT_BYTES

CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT=YES|NO
```

```text
RAW_NOTE_BODY_PUBLISHED=NO
RAW_NOTE_ID_PUBLISHED=NO
RAW_CONTACT_ID_PUBLISHED=NO
RAW_OPPORTUNITY_ID_PUBLISHED=NO
TOKENS_PUBLISHED=NO
PIT_PUBLISHED=NO
IDEMPOTENCY_KEYS_PUBLISHED=NO
```

Private store **must** retain enough to recompute the public flags offline.
Public proof **must not** require reviewers to trust runner memory without
digests.

## 7. Failure rule (fail-closed)

```text
IF any required predicate is NO or UNKNOWN:
  E2E_ACCEPTANCE=FAIL
  SUBMISSION_READY=NO
  NEW_RETRY_AUTHORIZED=NO
  AUTOMATIC_RETRY=NO
  COMPENSATING_MUTATION=NO
  STOP
```

Additional terminal failures:

```text
CREATE_NOTE_ATTEMPTS>1
STAGE_UPDATE_ATTEMPTS>1
RESPONSE_EVIDENCE_PERSISTED=NO for any required business call
CREATED_NOTE_ID_PRESENT=NO after claimed create-note success path
GET_NOTE_DISPATCHED_WITHOUT_CREATED_NOTE_ID=YES
EXPECTED_NOTE_SHA256 missing or captured post-write only
GRANT008_REUSED=YES
NON_SYNTHETIC_TARGET_USED=YES
SEARCH_OR_LIST_USED=YES
RAW_REST_FALLBACK_USED=YES
```

```text
PARTIAL_EFFECT_PRESERVATION=YES
  # On FAIL after a possible write, do not auto-cleanup or compensate.
  # Preserve private envelopes for governance disposition.
```

## 8. Runner capability requirements (planning checklist)

These are **contract requirements** for any future runner/implementation that
claims this acceptance object. This unit does **not** implement them.

| Capability | Required | Notes |
| --- | --- | --- |
| Prove exact contact binding via prewrite exact-get | **YES** | No search discovery |
| Capture transcript hash + prewrite note hash | **YES** | Before write dispatch |
| Persist per-call request/response evidence | **YES** | Private + sanitized digests |
| Parse layered nested operation success | **YES** | Not top-level path only |
| Extract and prove created note id | **YES** | Gate before get-note |
| Prove note content/hash readback same-run | **YES** | Against prewrite hash |
| Prove note visible under exact contact | **YES** | Id+contact association |
| Prove initial + final stage readback | **YES** | Stage required by §2.1 |
| Refuse unconditional YES flags | **YES** | Computed predicates only |
| Refuse automatic retry | **YES** | One-shot under future grant |

Planning self-assessment against this contract text (not a live runner claim):

```text
RUNNER_CAN_PROVE_CREATED_NOTE_ID=YES
  # Contract requires created-note-id extraction + gate; future runner must implement.

RUNNER_CAN_PROVE_NOTE_CONTENT_READBACK=YES
  # Contract requires EXPECTED_NOTE_SHA256 prewrite + readback hash/content match.

RUNNER_CAN_PROVE_EXACT_CONTACT_BINDING=YES
  # Contract requires private exact binding + prewrite get-contact match.

RUNNER_CAN_PROVE_STAGE_READBACK=YES
  # Stage advancement required; initial + final compare mandatory.
```

Interpretation: values above mean **the acceptance contract demands and specifies
how to prove** each capability. They do **not** mean a live runner already
passed. Live proof remains unauthorized here.

## 9. Future authorization boundary (not granted here)

A future execution unit must supply, separately:

```text
ONE_SHOT_HUMAN_GRANT=REQUIRED
GRANT_STATE_BEFORE_EXECUTION=AUTHORIZED_ONE_SHOT_ONLY
GRANT008_REUSE=FORBIDDEN
SYNTHETIC_ONLY=YES
MODELED_GHL_READS=4
MODELED_GHL_WRITES=2
MODELED_TOTAL_GHL_BUSINESS_CALLS=6
NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
IDEMPOTENCY_REQUIRED_FOR_WRITES=YES
FRESH_IDEMPOTENCY_KEYS_REQUIRED=YES
PRIVATE_BINDING_RECONCILIATION=PASS_REQUIRED_BEFORE_COUNTERSIGN
EVIDENCE_CAPTURE_PACKAGE=REQUIRED (this contract §§5–6)
AUTHORIZATION_WINDOW=EXPLICIT_UTC_START_END
SELF_ACTIVATION=FORBIDDEN
```

```text
THIS_ARTIFACT_IS_NOT_A_GRANT=YES
THIS_ARTIFACT_DOES_NOT_COUNTERSIGN=YES
THIS_ARTIFACT_DOES_NOT_CONSUME_AUTHORITY=YES
OPERATOR_EXECUTION_AUTHORIZED=NO
```

## 10. Privacy / publication rules

```text
RAW_IDS_PUBLISHED=NO
NOTE_CONTENT_PUBLISHED=NO
TOKENS_PUBLISHED=NO
PIT_PUBLISHED=NO
IDEMPOTENCY_KEYS_PUBLISHED=NO
PRIVATE_BINDING_VALUES_PUBLISHED=NO

PUBLIC_PROOF_MAY_INCLUDE=
  predicate YES/NO/UNKNOWN flags
  sha256 digests / salted fingerprints
  operation order and counts
  sanitized HTTP status and layered success flags
  stop codes and grant metadata references (SHAs, not secrets)
```

## 11. Explicit non-actions of this planning unit

```text
DID_NOT_CREATE_NOTE=YES
DID_NOT_UPDATE_OPPORTUNITY=YES
DID_NOT_DELETE=YES
DID_NOT_CLEANUP_MUTATION=YES
DID_NOT_CREATE_CONTACT_OR_OPPORTUNITY=YES
DID_NOT_DEPLOY=YES
DID_NOT_CHANGE_IAM=YES
DID_NOT_CHANGE_SECRETS=YES
DID_NOT_REUSE_GRANT008=YES
DID_NOT_CONSUME_NEW_AUTHORIZATION=YES
DID_NOT_EXECUTE_LIVE_GHL=YES
DID_NOT_CLAIM_SUBMISSION_READY=YES
DID_NOT_CLAIM_E2E_PASS=YES

LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
```

## 12. Acceptance contract completeness

```text
ACCEPTANCE_CONTRACT_COMPLETE=YES

REQUIRED_PREWRITE_PREDICATES_DEFINED=YES
REQUIRED_WRITE_PREDICATES_DEFINED=YES
REQUIRED_SAME_RUN_READBACK_PREDICATES_DEFINED=YES
REQUIRED_STAGE_PREDICATES_DEFINED=YES
PER_CALL_EVIDENCE_SCHEMA_DEFINED=YES
NOTE_EVIDENCE_SCHEMA_DEFINED=YES
FAILURE_RULE_DEFINED=YES
NO_UNCONDITIONAL_SUCCESS_FLAGS=YES
EXECUTION_AUTHORIZED=NO
SUBMISSION_READY=NO
```

## 13. Return block

```text
ARTIFACT_ID=NW008_TRANSCRIPT_TO_EXACT_GHL_CONTACT_E2E_ACCEPTANCE_001
ARTIFACT_PATH=docs/nw008/nw-008-transcript-to-exact-ghl-contact-e2e-acceptance-001.md

ACCEPTANCE_CONTRACT_COMPLETE=YES
RUNNER_CAN_PROVE_CREATED_NOTE_ID=YES
RUNNER_CAN_PROVE_NOTE_CONTENT_READBACK=YES
RUNNER_CAN_PROVE_EXACT_CONTACT_BINDING=YES
RUNNER_CAN_PROVE_STAGE_READBACK=YES

STAGE_ADVANCEMENT_REQUIRED=YES
GRANT008_STATE=CONSUMED
GRANT008_REUSABLE=NO
GRANT008_REUSED=NO
AT1_COMPLETE=NO
PR250_RESULT=HISTORICAL_RESULT008_EVIDENCE_INSUFFICIENT

EXECUTION_AUTHORIZED=NO
NEW_EXECUTION_AUTHORIZED=NO
NEW_GHL_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO

LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
DEPLOYMENTS=0

NEXT=SEPARATE_RUNNER_EVIDENCE_CAPABILITY_AND_ONE_SHOT_GRANT_PREP_ONLY
STOP_CODE=NW008_TRANSCRIPT_TO_EXACT_GHL_CONTACT_E2E_ACCEPTANCE_001_PLANNING_COMPLETE_NO_EXECUTION
```

## 14. Stop

Open **one** planning-only PR with this artifact. Do not merge automatically.
Do not execute live CRM proof. Do not reuse Grant 008. Do not claim submission
ready. Return the PR to ChatGPT for governance review before any runner
implementation authorization or one-shot grant drafting.
