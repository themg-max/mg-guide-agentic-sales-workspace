# NW-008 AT-1 Live Transport Evidence Remediation — Implementation

```text
IMPLEMENTATION_ID=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_IMPL_001
CLASSIFICATION=implementation

SOURCE_PLAN_HEAD_SHA=d580fddf103c179d0ccbdf9c374b0e20b7acfe0c
SOURCE_PLAN_MERGE_SHA=3c89056f346e23aa09e6b3a0d5b36a84cd2c6134
IMPLEMENTATION_BASE_SHA=3c89056f346e23aa09e6b3a0d5b36a84cd2c6134

B24_B38=PASS
CRASH_WINDOW_RESTART_CASES=PASS
EXISTING_B1_B23=PASS
GHL_TEST_SUITE=PASS
FULL_DETERMINISTIC_SUITE=PASS

PYTHON_39_COMPATIBILITY_VERIFIED=YES

RUN_TERMINALITY_PERSISTS_ACROSS_RESTART=YES
NEXT_ORDINAL_AFTER_UNRESOLVED_ATTEMPT_REFUSED=YES
RESPONSE_CAPTURE_PRE_PARSE_RESTART_REFUSED=YES
PARSE_PRE_SEMANTIC_RESTART_REFUSED=YES
PARSE_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
SEMANTIC_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
RESPONSE_CAPTURED_CONTINUABLE_ONLY_AFTER_DURABLE_SUCCESS=YES
UNRESOLVED_RESPONSE_CAPTURED_PROJECTS_UNKNOWN=YES
BUSINESS_CALL_COUNT_FROM_DISPATCH_LEDGER=YES

B27_BUSINESS_EFFECT_TRUTH=UNKNOWN
B29_BUSINESS_EFFECT_TRUTH=UNKNOWN
B30_BUSINESS_EFFECT_TRUTH=UNKNOWN

CI_COMPATIBILITY_DEFECT_FOUND=YES
CI_COMPATIBILITY_DEFECT_CLASS=PYTHON_39_ZIP_STRICT_UNSUPPORTED
CI_COMPATIBILITY_DEFECT_RUNTIME_IMPACT=NONE
CI_COMPATIBILITY_REPAIR_TEST_ONLY=YES

NETWORK_CALLS_EXECUTED=0
GHL_CALLS_EXECUTED=0
MCP_INITIALIZE_CALLS_EXECUTED=0

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

NEXT=IMPLEMENTATION_REVIEW
```

## Scope implemented

- Added durable offline execution store with atomic claim, ordinal consumption,
  durable request/response evidence capture, protocol/business ledgers, restart
  refusal semantics, and sanitized public projection.
- Added bounded live-transport adapter with injected established-session seam
  only, exact envelope validation, fail-closed layered MCP parsing, no retry,
  and request/response pre-parse evidence ordering.
- Strengthened bounded executor semantic gates per PR70 contract while
  preserving fixed six-operation order and one-attempt write budgets.
- Added offline remediation fixture + tests covering B24-B38 and crash-window
  restart refusal cases.

## Validation run

```text
PYTHONPATH=src /tmp/mg-guide-venv313/bin/python -m pytest -q tests/integrations/ghl/test_at1_live_transport_remediation.py
PYTHONPATH=src /tmp/mg-guide-venv313/bin/python -m pytest -q tests/integrations/ghl/test_bounded_at1_executor.py
PYTHONPATH=src /tmp/mg-guide-venv313/bin/python -m pytest -q tests/integrations/ghl
PYTHONPATH=src /tmp/mg-guide-venv313/bin/python scripts/verify_phase1_deterministic.py
git diff --check
```

Synthetic test completion does not alter historical project truth:
`GRANT_008_STATE=CONSUMED` and `AT1_COMPLETE=NO`.

## CI compatibility repair

A Python 3.9 compatibility defect was identified in
`tests/integrations/ghl/test_at1_live_transport_remediation.py` after the
initial implementation validation:

- `zip(..., strict=True)` is only available in Python 3.10+ and caused
  `test_b24_exact_serializer_contract` to fail on CI under Python 3.9 with
  `TypeError: zip() takes no keyword arguments`.
- The repair replaced the strict zip with an explicit cardinality assertion
  (`assert len(private_attempts) == len(expected)`) followed by a plain
  `zip(private_attempts, expected)`. The exact cardinality and order validation
  is preserved; no runtime code was changed.

## Validation run (Python 3.9)

```text
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl/test_at1_live_transport_remediation.py
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl/test_bounded_at1_executor.py
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl
PYTHONPATH=src python3.9 scripts/verify_phase1_deterministic.py
PYTHONPATH=src python3.9 -m pytest -q
git diff --check
```

Results:

```text
B24_B38=PASS
EXISTING_B1_B23=PASS
GHL_TEST_SUITE=PASS
FULL_DETERMINISTIC_SUITE=PASS
PYTHON_39_COMPATIBILITY_VERIFIED=YES
RUN_TERMINALITY_PERSISTS_ACROSS_RESTART=YES
NEXT_ORDINAL_AFTER_UNRESOLVED_ATTEMPT_REFUSED=YES
B27_BUSINESS_EFFECT_TRUTH=UNKNOWN
B29_BUSINESS_EFFECT_TRUTH=UNKNOWN
B30_BUSINESS_EFFECT_TRUTH=UNKNOWN
```

## Durable semantics repair

Two reviewer-identified fail-closed gaps were tightened:

1. **Run-terminal persistence across restart.** `At1ExecutionStore` now exposes
   `require_run_continuable()`, which the adapter calls before every business
   dispatch. If any prior ordinal is in `ATTEMPT_RECORDED`, `DISPATCHED`, or
   `TERMINAL` state, the run is poisoned and all further business transport is
   refused locally with `RunContinuationRefusedError`. This closes the gap where
   a crash after recording an attempt (but before dispatch) or after dispatch
   (but before response capture) previously allowed a correctly numbered next
   operation to proceed.

2. **Conservative business-effect truth.** `compute_public_projection()` no
   longer collapses every terminal failure to `NO`. If a terminal failure occurs
   after a write operation (`create-note` or `update-opportunity`) produced a
   successful MCP parse, the truth is now `UNKNOWN`, preserving the possibility
   that an external effect occurred. Failures before any write dispatch or after
   a conclusively rejected write remain `NO`. All six predicates proven remains
   `YES`.

New deterministic tests cover the gaps:

- `B36A`: next ordinal refused after pre-dispatch crash.
- `B36B`: next ordinal refused after unresolved dispatch.
- `B27`, `B29`, `B30`: business-effect truth is `UNKNOWN` after a plausible
  write without conclusive readback.

## Crash-window and dispatch-count repair

Two additional fail-closed gaps were closed after the durable-semantics repair:

1. **RESPONSE_CAPTURED without durable parse/semantic completion.**
   `require_run_continuable()` now treats a prior `RESPONSE_CAPTURED` attempt as
   continuable only when both `parse_success` and `semantic_success` are
   durably successful / True. Crash after response capture / before parse, or after parse /
   before semantic processing, poisons the grant/run and refuses the next
   ordinal before transport with `RunContinuationRefusedError`.
   `business_effect_truth` remains `UNKNOWN` for these unresolved windows.

2. **Independent attempt vs transport counts.** `compute_public_projection()`
   now derives:
   - `business_attempt_count` from durably recorded attempts (`len(attempts)`);
   - `business_call_count` from durable `DISPATCHED` events in the business
     ledger (not from attempt row count).

   Serializer shapes and the fixed six-operation contract are unchanged.
   Conservative `business_effect_truth=UNKNOWN` behavior from the prior repair
   is preserved.

New/extended deterministic tests:

- `B36A` / `B36B`: assert `business_attempt_count` and `business_call_count`
  (0 vs 1 dispatch) for pre-dispatch and post-dispatch crash windows.
- `B36C`: next ordinal refused after response-captured / pre-parse crash.
- `B36D`: next ordinal refused after parsed / pre-semantic crash.
- `B36E`: next ordinal refused after parse-failure / pre-terminal crash.
- `B36F`: next ordinal refused after semantic-failure / pre-terminal crash.

```text
RESPONSE_CAPTURE_PRE_PARSE_RESTART_REFUSED=YES
PARSE_PRE_SEMANTIC_RESTART_REFUSED=YES
PARSE_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
SEMANTIC_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
RESPONSE_CAPTURED_CONTINUABLE_ONLY_AFTER_DURABLE_SUCCESS=YES
UNRESOLVED_RESPONSE_CAPTURED_PROJECTS_UNKNOWN=YES
BUSINESS_CALL_COUNT_FROM_DISPATCH_LEDGER=YES
```

## Validation run (Python 3.9 — crash-window repair)

```text
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl/test_at1_live_transport_remediation.py
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl/test_bounded_at1_executor.py
PYTHONPATH=src python3.9 -m pytest -q tests/integrations/ghl
PYTHONPATH=src python3.9 scripts/verify_phase1_deterministic.py
PYTHONPATH=src python3.9 -m pytest -q
git diff --check
# forbidden network/credential scan on changed files: clean
```

Results:

```text
B24_B38=PASS
CRASH_WINDOW_RESTART_CASES=PASS
EXISTING_B1_B23=PASS
GHL_TEST_SUITE=PASS
FULL_DETERMINISTIC_SUITE=PASS
PYTHON_39_COMPATIBILITY_VERIFIED=YES
RUN_TERMINALITY_PERSISTS_ACROSS_RESTART=YES
NEXT_ORDINAL_AFTER_UNRESOLVED_ATTEMPT_REFUSED=YES
RESPONSE_CAPTURE_PRE_PARSE_RESTART_REFUSED=YES
PARSE_PRE_SEMANTIC_RESTART_REFUSED=YES
PARSE_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
SEMANTIC_FAILURE_PRE_TERMINAL_RESTART_REFUSED=YES
RESPONSE_CAPTURED_CONTINUABLE_ONLY_AFTER_DURABLE_SUCCESS=YES
UNRESOLVED_RESPONSE_CAPTURED_PROJECTS_UNKNOWN=YES
BUSINESS_CALL_COUNT_FROM_DISPATCH_LEDGER=YES
B27_BUSINESS_EFFECT_TRUTH=UNKNOWN
B29_BUSINESS_EFFECT_TRUTH=UNKNOWN
B30_BUSINESS_EFFECT_TRUTH=UNKNOWN
GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO
LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```
