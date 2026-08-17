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
```
