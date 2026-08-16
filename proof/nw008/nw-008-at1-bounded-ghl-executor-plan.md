# NW-008 — AT-1 Bounded GHL Executor Plan

## Pre-closeout

| Check | Result |
| --- | --- |
| Branch | `plan/nw008-at1-bounded-ghl-executor` |
| Base | `origin/main` @ `44dd00e6373af2e78d5913bdfaf006a25fc8c052` |
| PR #61 merged to `origin/main` | **YES** |
| PR #61 merge SHA (exact 40-char) | `44dd00e6373af2e78d5913bdfaf006a25fc8c052` |
| PR #61 artifact on `origin/main` | `proof/nw008/nw-008-safe-env-ghl-mutation-authorization-plan.md` |
| Live GHL execution in this artifact | **NONE** |
| Live Firestore execution in this artifact | **NONE** |

```text
PR61_STATE=MERGED
PR61_MERGE_SHA=44dd00e6373af2e78d5913bdfaf006a25fc8c052
```

## Implementation lane

```text
WORK_ITEM=NW-008
ACCEPTANCE_TEST=AT-1
LANE_TYPE=REPO_OWNED_GHL_EXECUTOR_PLAN
BRANCH=plan/nw008-at1-bounded-ghl-executor
EXECUTION_MODE=DETERMINISTIC_MOCKS_AND_FIXTURES_ONLY
GHL_EXECUTION_OCCURRED=NO
FIRESTORE_EXECUTION_OCCURRED=NO
```

## Required operation surface (exact-ID only)

The AT-1 repo-owned GHL executor exposes exactly these operations. Every call
must use a synthetic ID supplied by the future private binding layer; no
broad query, search, or discovery is permitted.

| Operation | Direction | ID(s) required | Purpose |
| --- | --- | --- | --- |
| `get-contact` | read | `contactId` (exact) | Read contact record for AT-1 context. |
| `get-opportunity` | read | `opportunityId` (exact) | Read opportunity before mutation. |
| `create-note` | write | `contactId` (exact) | Create exactly one note on the contact. |
| `get-note` | read | `noteId` (exact) | Read-back verification of created note. |
| `update-opportunity` | write | `opportunityId` (exact), `stageId` (exact) | Transition opportunity stage exactly once. |
| `get-opportunity` | read | `opportunityId` (exact) | Post-update read-back verification. |

> The duplicated `get-opportunity` entry represents two distinct call sites:
> pre-mutation read and post-mutation read-back verification.

## Pipeline metadata runtime read

```text
PIPELINE_METADATA_RUNTIME_READ_REQUIRED=NO
```

Reason: all operation inputs are exact synthetic IDs and strings supplied by
the future private binding layer. The executor does **not** discover pipelines,
stages, contacts, opportunities, or notes at runtime. It receives bound values
as explicit invocation arguments and validates shape/format only.

## Private binding contract (future)

Required future binding fields only. Do **not** commit actual private IDs in
this public repository.

```text
location_id
contact_id
opportunity_id
expected_initial_stage_id
authorized_final_stage_id

PRIVATE_BINDING_VALUES_COMMITTED_PUBLICLY=NO
```

## Implementation requirements

### Identity and discovery

- Exact synthetic IDs only, supplied by future private binding.
- No broad search, list, or lookup operations.
- No pagination.
- No raw REST fallback.
- No automatic retry.
- No compensating mutations.

### Mutation safety (fail-closed counters)

```text
NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1

SECOND_NOTE_WRITE_ATTEMPT_AUTHORIZED=NO
SECOND_STAGE_WRITE_ATTEMPT_AUTHORIZED=NO

AUTOMATIC_RETRY_AUTHORIZED=NO
COMPENSATING_MUTATION_AUTHORIZED=NO
```

Legacy alias labels (equivalent intent; prefer the write-attempt/succeeded pair):

```text
NOTE_CREATE_MAX=1
STAGE_TRANSITION_MAX=1
```

Counter rules:

- Per-invocation `NOTE_WRITE_ATTEMPTS` starts at 0; increments before each
  `create-note` attempt. Exceeding `NOTE_WRITE_ATTEMPTS_MAX` fails closed
  before any call is issued.
- Per-invocation `NOTE_WRITES_SUCCEEDED` starts at 0; increments only after a
  successful `create-note` response. Exceeding `NOTE_WRITES_SUCCEEDED_MAX`
  fails closed.
- Per-invocation `STAGE_WRITE_ATTEMPTS` starts at 0; increments before each
  `update-opportunity` attempt. Exceeding `STAGE_WRITE_ATTEMPTS_MAX` fails
  closed before any call is issued.
- Per-invocation `STAGE_WRITES_SUCCEEDED` starts at 0; increments only after a
  successful `update-opportunity` response. Exceeding
  `STAGE_WRITES_SUCCEEDED_MAX` fails closed.
- Second note write attempt is never authorized.
- Second stage write attempt is never authorized.
- Automatic retry is never authorized.
- Compensating mutation is never authorized.

### Failure semantics

```text
ON_NOTE_WRITE_SUCCESS_AND_READBACK_FAILURE=STOP_AND_PRESERVE_PROOF
ON_STAGE_WRITE_SUCCESS_AND_READBACK_FAILURE=STOP_AND_PRESERVE_PROOF
```

- If a note write succeeds and read-back fails: stop immediately; preserve
  proof of the partial effect; do not retry; do not compensate.
- If a stage write succeeds and read-back fails: stop immediately; preserve
  proof of the partial effect; do not retry; do not compensate.
- Any other partial-effect failure stops execution immediately and preserves
  proof of the partial effect for inspection.

### Verification

- `create-note` is followed by `get-note` read-back verification.
- `update-opportunity` is followed by `get-opportunity` read-back verification.
- If read-back does not match expected state, apply the failure semantics above.

### Test substrate

- Deterministic mocks/fixtures cover success and every required failure path.
- Fixtures are repo-owned and committed.
- No live GHL calls in unit, integration, or acceptance tests.
- No Firestore calls in unit, integration, or acceptance tests.

### Failure paths to fixture

| Path | Fixture behavior |
| --- | --- |
| Contact not found | `get-contact` returns deterministic 404-shaped error. |
| Opportunity not found | `get-opportunity` returns deterministic 404-shaped error. |
| Note create rejected | `create-note` returns deterministic write-denied error; attempts may increment, succeeded stays 0. |
| Note write success + read-back failure | `get-note` mismatch; `ON_NOTE_WRITE_SUCCESS_AND_READBACK_FAILURE=STOP_AND_PRESERVE_PROOF`. |
| Stage transition rejected | `update-opportunity` returns deterministic write-denied error; attempts may increment, succeeded stays 0. |
| Stage write success + read-back failure | `get-opportunity` unexpected stage; `ON_STAGE_WRITE_SUCCESS_AND_READBACK_FAILURE=STOP_AND_PRESERVE_PROOF`. |
| Second note write attempt | `SECOND_NOTE_WRITE_ATTEMPT_AUTHORIZED=NO`; fail closed before issuing call. |
| Second stage write attempt | `SECOND_STAGE_WRITE_ATTEMPT_AUTHORIZED=NO`; fail closed before issuing call. |

## Verification checklist

- [x] PR #61 merged to `origin/main`.
- [x] `proof/nw008/nw-008-safe-env-ghl-mutation-authorization-plan.md` exists on `origin/main`.
- [x] No live GHL calls in this plan.
- [x] No Firestore calls in this plan.
- [x] Operation surface is exact-ID only.
- [x] Deterministic mocks/fixtures required for success and failure paths.
- [x] Fail-closed write attempt/success counters normalized.
- [x] Read-back verification required after each mutation.
- [x] Partial-effect failure stops and preserves proof.
- [x] Private binding field names recorded; values not committed publicly.
- [x] `PIPELINE_METADATA_RUNTIME_READ_REQUIRED=NO`.

## Return

```text
PR61_MERGE_SHA=44dd00e6373af2e78d5913bdfaf006a25fc8c052
AT1_EXECUTOR_PLAN_READY=YES
PIPELINE_METADATA_RUNTIME_READ_REQUIRED=NO
NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
GHL_EXECUTION_OCCURRED=NO
FIRESTORE_EXECUTION_OCCURRED=NO
PRIVATE_BINDING_VALUES_COMMITTED_PUBLICLY=NO
STOP_CODE=NW008_AT1_BOUNDED_EXECUTOR_PLAN_READY_FOR_REVIEW
```
