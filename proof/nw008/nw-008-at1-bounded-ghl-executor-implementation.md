# NW-008 — AT-1 Bounded GHL Executor Implementation

## Baseline and implementation subject

```text
PR63_MERGE_SHA=04ec0cc1a46589c242e6c20fbb1ce6356d4b8245
IMPLEMENTATION_SUBJECT_SHA=8c18a10faff28b658638da9e0d9752c8710e0e23
```

The implementation subject is the initial implementation commit; this
follow-up closeout commit records it without a self-referential commit hash.

## Frozen changed paths

- `src/integrations/ghl/bounded_at1_executor.py`
- `src/integrations/ghl/__init__.py`
- `fixtures/ghl/at1-bounded-executor.json`
- `tests/integrations/ghl/test_bounded_at1_executor.py`
- `proof/nw008/nw-008-at1-bounded-ghl-executor-implementation.md`

## Bounded operation surface

```text
PIPELINE_METADATA_RUNTIME_READ_REQUIRED=NO
ORDER=get-contact,get-opportunity,create-note,get-note,update-opportunity,get-opportunity
MODELED_GHL_READS=4
MODELED_GHL_WRITES=2
MODELED_TOTAL_GHL_CALLS=6
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_RAW_REST=YES
NO_ALTERNATE_OPERATION=YES
NO_AUTOMATIC_CLEANUP=YES
NO_COMPENSATING_MUTATION=YES
```

The input contract is limited to `location_id`, `contact_id`, `opportunity_id`,
`expected_initial_stage_id`, `authorized_final_stage_id`, and
`expected_note_content_or_fingerprint`. All committed fixture values are
synthetic.

## Counter and terminal behavior

```text
NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1
REFUSE_BEFORE_TRANSPORT=YES
FURTHER_TRANSPORT_CALLS_AUTHORIZED=NO_AFTER_TERMINAL_FAILURE
STOP_AND_PRESERVE_PROOF=YES_ON_WRITE_READBACK_FAILURE
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
```

A write attempt is incremented immediately before its one permitted dispatch,
so a rejected write consumes its attempt budget. The deterministic transport
rejects operations outside the exact AT-1 surface and validates fixture order
and arguments.

## Deterministic verification

| Command | Result |
| --- | --- |
| `PYTHONPATH=src .venv/bin/python -m pytest tests/integrations/ghl/test_bounded_at1_executor.py` | PASS — 12 tests |
| `PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py` | PASS — 6 validation sections |
| `git diff --check` | PASS |
| `.venv/bin/python -m json.tool fixtures/ghl/at1-bounded-executor.json` | PASS |

The focused test surface covers B1 through B12: success; contact and
opportunity absence; write rejections; note and stage read-back mismatches;
second note and stage attempts refused before transport; malformed binding;
unexpected operation; and no calls after terminal failure.

```text
PHASE1_DETERMINISTIC_VALIDATION=PASS
PHASE1_CI_RESULT=PENDING_PULL_REQUEST
NETWORK_EXECUTION_OCCURRED=NO
GHL_EXECUTION_OCCURRED=NO
FIRESTORE_EXECUTION_OCCURRED=NO
PRIVATE_BINDING_VALUES_COMMITTED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

```text
STOP_CODE=NW008_AT1_BOUNDED_EXECUTOR_IMPLEMENTATION_READY_FOR_REVIEW
```
