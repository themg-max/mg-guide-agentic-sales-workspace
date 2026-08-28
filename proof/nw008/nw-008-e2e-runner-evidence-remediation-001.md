# NW-008 — E2E Runner Evidence Remediation 001

```text
ARTIFACT_ID=NW008_E2E_RUNNER_EVIDENCE_REMEDIATION_001
ARTIFACT_PATH=proof/nw008/nw-008-e2e-runner-evidence-remediation-001.md
ARTIFACT_KIND=OFFLINE_BOUNDED_RUNNER_EVIDENCE_REMEDIATION_PROOF
UNIT=NW008_E2E_RUNNER_EVIDENCE_REMEDIATION_001
MODE=OFFLINE_DETERMINISTIC_IMPLEMENTATION_AND_PROOF

PUBLIC_BASE_SHA=9da8ae5c7bdb4d7c131dcb33aa3b88a361a329ea
PR251_ACCEPTANCE_CONTRACT=
  docs/nw008/nw-008-transcript-to-exact-ghl-contact-e2e-acceptance-001.md
PR252_CAPABILITY_RECONCILIATION=
  docs/nw008/nw-008-e2e-runner-evidence-capability-reconciliation-001.md

GRANT008_STATE=CONSUMED
GRANT008_REUSABLE=NO
GRANT008_REUSED=NO
NEW_LIVE_EXECUTION_AUTHORIZED=NO
NEW_GHL_MUTATION_AUTHORIZED=NO
SUBMISSION_READY=NO
```

## 1. Scope and non-actions

This unit implements only the R1–R3 bounded runner/evidence remediation
identified by PR #252. It does not execute GHL, construct a live client,
create a new grant, or weaken PR #251 acceptance criteria.

```text
LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
ONE_SHOT_GRANT_CREATED=NO
DEPLOYMENTS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SEARCH=NO
LIST=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO
AUTOMATIC_CLEANUP=NO
COMPENSATING_MUTATION=NO
```

## 2. R1 — Sealed transcript and note provenance

`BoundedAt1Input` now requires synthetic `transcript_content` and `pipeline_id`
in addition to the existing exact bindings. Before any business operation,
`BoundedAt1GhlExecutor._seal_prewrite_provenance` computes SHA256 digests of
the immutable transcript and canonical expected note body.

On the composed adapter/store path:

1. `At1LiveTransportAdapter.record_prewrite_provenance` records the evidence
   before ordinal 1.
2. `At1ExecutionStore.record_prewrite_provenance` verifies both supplied
   digests against their private values, then stores private canonical payloads
   and digests in a dedicated `prewrite_provenance` record.
3. `BoundedAt1GhlExecutor._dispatch_write` recomputes the actual serialized
   create-note body SHA256 and refuses before dispatch if it differs from the
   sealed expected-note digest.
4. The sanitized projection emits flags and SHA256 digests only; it does not
   emit transcript or note content.

```text
TRANSCRIPT_INGESTED=YES
TRANSCRIPT_HASH_CAPTURED=YES
TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE=YES
EXPECTED_NOTE_SHA256_CAPTURED_PREWRITE=YES
CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED=YES
```

## 3. R2 — Response-side exact binding verification

The executor now requires and compares these **response** values, rather than
inferring target correctness from request intent:

| Operation | Required response comparisons | Fail-closed code |
| --- | --- | --- |
| OP1 `get-contact` | contact id, location id | `CONTACT_ID_MISMATCH`, `CONTACT_LOCATION_MISMATCH` |
| OP2 `get-opportunity` | opportunity id, contact relation, pipeline id, location id, initial stage | `OPPORTUNITY_*_MISMATCH`, `INITIAL_STAGE_MISMATCH` |
| OP4 `get-note` | created note id, content, returned contact association | `NOTE_READBACK_MISMATCH`, `NOTE_READBACK_CONTACT_MISMATCH` |
| OP5/OP6 | exact opportunity id; authorized final stage at OP6 | existing stage failure codes |

```text
CONTACT_LOCATION_BINDING_MATCH=YES
OPPORTUNITY_CONTACT_RELATION_MATCH=YES
OPPORTUNITY_PIPELINE_MATCH=YES
OPPORTUNITY_LOCATION_MATCH=YES
NOTE_READBACK_CONTACT_ID_MATCH=YES
CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT=YES
```

The existing six-call bound is preserved. The OP4 created-note-id + returned
contact association + exact content comparison proves required same-run contact
visibility without an additional inventory operation.

## 4. R3 — First-class sanitized per-call evidence

`At1ExecutionStore` schema version 2 stores parse evidence and semantic
target-binding outcome per attempt. `At1LiveTransportAdapter._response_evidence`
derives fields from the retained response before parse reduction. Missing or
contradictory nested status is projected as `UNKNOWN`; no absence converts to
success.

Every `request_response_commitments` object now contains:

```text
OPERATION_ID
HTTP_STATUS
JSONRPC_ERROR_PRESENT
MCP_IS_ERROR
NESTED_OPERATION_SUCCESS
TARGET_BINDING_MATCH
REQUEST_EVIDENCE_PERSISTED
RESPONSE_EVIDENCE_PERSISTED
REQUEST_RESPONSE_CORRELATION_ID
SANITIZED_REQUEST_DIGEST
SANITIZED_RESPONSE_DIGEST
```

The store retains private request/response envelopes and canonical provenance
payloads. The public projection retains only flags, correlation identifier,
and HMAC-SHA256 commitments / SHA256 content digests.

## 5. Deterministic coverage

Targeted test evidence:

```text
tests/integrations/ghl/test_bounded_at1_executor.py
tests/integrations/ghl/test_at1_live_transport_remediation.py
tests/integrations/ghl/test_at1_commitment_key_provider.py

ALL_TARGETED_TESTS_PASS=YES
```

Coverage includes:

```text
SUCCESS_R1_TRANSCRIPT_AND_NOTE_PROVENANCE=YES
SUCCESS_R2_RESPONSE_BINDINGS=YES
SUCCESS_R3_PER_CALL_PUBLIC_EVIDENCE=YES

FAIL_CLOSED_TRANSCRIPT_PROVENANCE_MISSING=YES
FAIL_CLOSED_PREWRITE_PROVENANCE_AFTER_BUSINESS_BOUNDARY=YES
FAIL_CLOSED_CREATE_NOTE_BODY_HASH_MISMATCH=YES
FAIL_CLOSED_CONTACT_LOCATION_MISMATCH=YES
FAIL_CLOSED_OPPORTUNITY_CONTACT_MISMATCH=YES
FAIL_CLOSED_OPPORTUNITY_PIPELINE_MISMATCH=YES
FAIL_CLOSED_OPPORTUNITY_LOCATION_MISMATCH=YES
FAIL_CLOSED_NOTE_CONTACT_ASSOCIATION_MISMATCH=YES
FAIL_CLOSED_JSONRPC_ERROR=YES
FAIL_CLOSED_MCP_IS_ERROR_TRUE=YES
FAIL_CLOSED_NESTED_SUCCESS_FALSE=YES
FAIL_CLOSED_MISSING_NESTED_STATUS=YES
FAIL_CLOSED_TARGET_BINDING_MISMATCH=YES
FAIL_CLOSED_MISSING_RESPONSE_EVIDENCE=YES
SECOND_NOTE_OR_STAGE_WRITE_REFUSED=YES
```

`scripts/verify_phase1_deterministic.py` also passes with the repository's
existing deterministic test environment.

```text
PHASE1_DETERMINISTIC_LOCAL_PASS=YES
GIT_DIFF_CHECK=PASS
```

## 6. Predicate closure

All 29 required PR #251 runner/evidence predicates attributable to this
implementation are now deterministically proven by the composed offline
adapter/store/executor path and targeted tests.

```text
SUPPORTED_COUNT=29
PARTIAL_COUNT=0
MISSING_COUNT=0
RUNNER_E2E_EVIDENCE_CAPABILITY=READY
```

This is an implementation result only. A separate post-implementation
capability reconciliation and separate human governance remain required before
any grant discussion.

```text
GRANT_PREPARATION_READY=NO
EXECUTION_AUTHORIZED=NO
SUBMISSION_READY=NO
NEXT=POST_IMPLEMENTATION_CAPABILITY_RECONCILIATION_AND_GOVERNANCE_REVIEW
STOP_CODE=NW008_E2E_RUNNER_EVIDENCE_REMEDIATION_001_OFFLINE_READY_NO_GRANT
```
