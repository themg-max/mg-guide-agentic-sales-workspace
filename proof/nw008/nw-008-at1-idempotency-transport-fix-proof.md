# NW-008 — AT-1 Bounded Idempotency Transport Fix Proof

## Scope

Repair durable AT-1 live MCP write serialization so every idempotency-required
write includes a frozen idempotency key, covering `create-note` and
`update-opportunity`. Preserve the existing six-operation state machine, attempt
budgets, and no-retry semantics.

## Authority

- `RESULT_007_SHA=4bd9e4d6ee23661e4e7b00ca49234e7ebdd0a058`
- `DIAGNOSTIC_001_SHA=161bdc19c7d0087a207a7b63d7347b138af7c796`
- `REQUEST_CONTRACT_RECON_SHA=a1ce3517ec26a1ac56aad95ef586213bf31e046c`
- `ROOT_CAUSE=MISSING_REQUIRED_IDEMPOTENCY_KEY`
- `DEFECT_BOUNDARY=MCP_TRANSPORT_SERIALIZATION`
- `GRANT_007_RETRY_AUTHORIZED=NO`
- `AT1_EXECUTION_AUTHORIZED=NO`

## Implementation

- Added `src/integrations/ghl/at1_live_transport_serializer.py`:
  - `At1ExecutionContext` — private container for `note_idempotency_key` and
    `stage_idempotency_key`; enforces strip non-empty and distinct keys.
  - `At1LiveTransportSerializer` — performs exact operation-specific live MCP
    serialization and emits a frozen outer seam:
    `{name: "execute_operation", arguments: {...}}`.
  - `IdempotencyKeyError` — raised locally before transport when a required key
    is missing, blank, or duplicated.

- Hardened `src/integrations/ghl/bounded_at1_executor.py`:
  - `BoundedAt1GhlExecutor.execute` now accepts an `At1ExecutionContext`.
  - Execution context is prevalidated before operation 1.
  - Writes validate the idempotency key, then consume the attempt budget, then
    dispatch with exact path/body serialization.
  - Reads continue to dispatch without idempotency keys.
  - Six-operation order, attempt caps, and no-retry semantics are unchanged.

- Updated `tests/integrations/ghl/test_bounded_at1_executor.py`:
  - All existing tests supply a private execution context and pass.
  - Added deterministic exact wire-contract tests for `get-contact`,
    `get-opportunity`, `create-note`, `get-note`, and `update-opportunity`.
  - Added malformed context tests proving total transport calls remain zero.

## Verification Results

```text
CREATE_NOTE_IDEMPOTENCY_SERIALIZATION=PASS
UPDATE_OPPORTUNITY_IDEMPOTENCY_SERIALIZATION=PASS
LIVE_WIRE_MAPPING_CREATE_NOTE=PASS
LIVE_WIRE_MAPPING_GET_NOTE=PASS
LIVE_WIRE_MAPPING_UPDATE_OPPORTUNITY=PASS
LIVE_WIRE_MAPPING_READS=PASS

CREATE_NOTE_MISSING_KEY_LOCAL_REFUSAL=PASS
UPDATE_OPPORTUNITY_MISSING_KEY_LOCAL_REFUSAL=PASS
EXECUTION_CONTEXT_PREVALIDATED=YES
MALFORMED_CONTEXT_TOTAL_TRANSPORT_CALLS=0

IDEMPOTENCY_KEYS_DISTINCT_TEST=PASS

GET_NOTE_MAPPING_REVIEWED=PASS

SIX_OPERATION_ORDER_UNCHANGED=YES
WRITE_ATTEMPT_CAPS_UNCHANGED=YES
RETRY_SEMANTICS_UNCHANGED=YES

NETWORK_EXECUTION_OCCURRED=NO
CRM_MUTATION_OCCURRED=NO

GRANT_008_PREPARATION_AUTHORIZED=NO
```

### Test Runs

- Focused bounded executor tests: `26 passed`
- Full GHL integration tests: `33 passed`
- Full deterministic test suite: `400 passed, 169 warnings`
- `git diff --check`: clean

## Governance

- No network execution occurred.
- No CRM mutation occurred.
- Raw idempotency key values are not printed or committed.
- Grant 008 preparation remains unauthorized until review, merge, and rebound
  authorization.
