# NW-008 AT-8D — HighLevel REST NOTE_PATH At1ExecutionStore Fit Validation 001

```text
UNIT=NW008_AT8D_GHL_REST_NOTE_PATH_AT1_EXECUTION_STORE_FIT_VALIDATION_001
PR_CLASS=planning_only
MODE=READ_ONLY_INSPECTION_AND_LOCAL_VALIDATION
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=planning/nw008-at8d-ghl-rest-note-path-at1-execution-store-fit-validation-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=441650d4bc8567d3865d35bdb36379556f36c4d7

SOURCE_AT8C_PR=102
SOURCE_AT8C_HEAD=58dbae627390738b3ec85712609a1e4a6c762ac8
SOURCE_AT8C_MERGE_SHA=441650d4bc8567d3865d35bdb36379556f36c4d7
SOURCE_AT8C_MERGE_VERIFIED=YES

PLANNING_ONLY=YES
SOURCE_CODE_CHANGE=NO
TEST_FILE_CHANGE=NO
AUTHORIZATION_ISSUED=NO
AUTHORIZATION_ARTIFACT_CREATED=NO
IMPLEMENTATION_CHANGE=NO

HIGHLEVEL_ACCESS=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

CREDENTIAL_ACCESS=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO

LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
STAGE_PATH_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO

PLANNING_DOES_NOT_AUTHORIZE_IMPLEMENTATION=YES
IMPLEMENTATION_DOES_NOT_AUTHORIZE_LIVE_MUTATION=YES
LIVE_MUTATION_REQUIRES_SEPARATE_HUMAN_GRANT=YES
```

## Boundary

This unit inspected merged sources and ran deterministic local SQLite
validation with synthetic values only. Temporary databases and a one-off local
harness were used. No tracked source, test, fixture, governance, proof,
contract, workflow, deploy, or infra path was modified except this planning
artifact.

No provider access occurred. No credential or secret state was read or
changed. No live client, persistence backend, authorization artifact, or
implementation was introduced.

The grant/run mapping below is a planning mapping. It is not implemented in
repository source.

```text
AT1_STORE_NOTE_PATH_REUSE_AUTHORIZED=NO
AT1_STORE_ADAPTATION_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_ADAPTER_REUSE_AUTHORIZED=NO
PRIVATE_AT8_CAPABILITY_HANDOFF=BLOCKED
BOUNDED_LIVE_NOTE_TRANSPORT=BLOCKED
```

## Inspected sources

- `src/integrations/ghl/at1_execution_store.py`
- `src/integrations/ghl/at1_live_transport_adapter.py`
- `tests/integrations/ghl/test_at1_live_transport_remediation.py`
- `src/integrations/ghl/highlevel_rest/note_path.py`
- `docs/nw008/nw-008-at8c-ghl-rest-note-path-live-execution-boundary-design-001.md`

Do not infer that `At1LiveTransportAdapter` must be reused merely because
`At1ExecutionStore` is reusable.

## Existing proof normalized from source and tests

```text
AT1_STORE_SQLITE_BACKED=YES
AT1_STORE_GRANT_RUN_PRIMARY_CLAIM=YES
AT1_STORE_ATTEMPT_PRIMARY_KEY=(grant_run_id,operation_ordinal)

LOCAL_DURABILITY_PROVEN=YES
PROCESS_RESTART_STATE_PERSISTENCE=YES

PRE_DISPATCH_CRASH_POISONS_RUN=YES
POST_DISPATCH_CRASH_POISONS_RUN=YES

DUPLICATE_BUSINESS_ORDINAL_BLOCKED=YES
```

Source facts:

- `At1ExecutionStore` opens a SQLite file with `timeout=30.0` and
  `isolation_level=None`.
- `execution_claims.grant_run_id` is the claim primary key.
- `attempts` primary key is `(grant_run_id, operation_ordinal)`.
- Duplicate attempt insert raises `DuplicateBusinessOrdinalError`.
- `require_run_continuable()` poisons continuation for `ATTEMPT_RECORDED`,
  `DISPATCHED`, `TERMINAL`, and `RESPONSE_CAPTURED` without durable parse and
  semantic success.

Existing tests already prove local durability and crash-window poisoning for
the store, including reopen on the same SQLite file:

- `test_b36_restart_persistence_and_crash_window_refusals`
- `test_b36a_next_ordinal_refused_after_pre_dispatch_crash`
- `test_b36b_next_ordinal_refused_after_unresolved_dispatch`
- `test_b36c` through `test_b36f` unresolved parse/semantic/terminal windows
- `test_b37_concurrent_atomic_claim_rejects_second_owner` (two connections in
  one process; not multiprocess NOTE_CREATE reservation)

`test_b37` is not treated as multiprocess NOTE_CREATE exclusivity. AT8D ran a
separate two-OS-process reservation test.

Current NOTE_PATH reservation remains the process-local in-memory ledger in
`note_path.py` (`_SharedProcessLocalTestLedger` keyed by
`consumer_authorization_identity`, `consumer_workflow_run_id`,
`operation=NOTE_CREATE`). That ledger is not the live reservation backend.

## Grant/run mapping

Deterministic mapping from NOTE_PATH reservation identity to one durable
`grant_run_id`. Designed only; not implemented in repository source.

Inputs:

- `consumer_authorization_identity`
- `consumer_workflow_run_id`
- `operation=NOTE_CREATE`

Excluded from the authority key:

- `contact_id`
- `location_id`
- any private CRM identifier

Canonical payload:

```text
{
  "consumer_authorization_identity": <consumer_authorization_identity>,
  "consumer_workflow_run_id": <consumer_workflow_run_id>,
  "mapping_version": 1,
  "namespace": "NOTE_PATH",
  "operation": "NOTE_CREATE"
}
```

Canonical encoding: UTF-8 JSON with sorted keys and separators `(",", ":")`.

```text
GRANT_RUN_ID_MAPPING=npgr1:sha256(canonical_json({consumer_authorization_identity,consumer_workflow_run_id,mapping_version=1,namespace=NOTE_PATH,operation=NOTE_CREATE}))
```

Local synthetic validation of this mapping:

- same authorization + workflow run + `NOTE_CREATE` => same `grant_run_id`
- different authorization => different `grant_run_id`
- different workflow run => different `grant_run_id`
- operation namespace is explicit (`namespace=NOTE_PATH` and
  `operation=NOTE_CREATE`)
- contact and location values are not mapping inputs

One dedicated NOTE_PATH live-mutation grant/run uses this mapping and a fixed
NOTE_CREATE ordinal. A different authorization or workflow run maps to a
different grant/run and therefore a different reservation namespace.

## Fixed NOTE_CREATE ordinal

```text
NOTE_CREATE_OPERATION_ORDINAL=1
FIXED_ORDINAL_RESERVATION_SUPPORTED=YES
```

For a dedicated NOTE_PATH grant/run, reservation is the durable insert:

```text
record_attempt(
  grant_run_id=<mapped grant_run_id>,
  operation_ordinal=1,
  operation_id="NOTE_CREATE",
  ...
)
```

Atomicity is the existing SQLite primary key
`(grant_run_id, operation_ordinal)`. A second insert of ordinal `1` for the
same grant/run raises `DuplicateBusinessOrdinalError`.

`next_operation_ordinal()` is not the atomic reservation primitive. AT8D does
not authorize NOTE_PATH to allocate ordinals by reading `MAX(operation_ordinal)`.

## Multiprocess exclusivity

Local validation used one temporary SQLite file per case, synthetic grant/run
IDs, no network, two separate OS processes, and a barrier immediately before
`record_attempt`.

Authoritative reservation success is durable insertion of the fixed
NOTE_CREATE attempt row. `acquire_claim()` success alone is not reservation
success.

Test A — same `grant_run_id`, different `owner_id`, `operation_ordinal=1`:

- exactly one process acquired the claim
- the other process received `ExecutionClaimError`
- exactly one durable NOTE_CREATE attempt row existed

```text
DIFFERENT_OWNER_SECOND_WORKER_BLOCKED=YES
```

Test B — same `grant_run_id`, same `owner_id`, `operation_ordinal=1`:

- both processes acquired the claim (same-owner re-claim is allowed)
- exactly one process inserted the fixed NOTE_CREATE attempt
- the other process received `DuplicateBusinessOrdinalError`
- exactly one durable NOTE_CREATE attempt row existed

```text
SAME_OWNER_CONCURRENT_SECOND_WORKER_BLOCKED=YES
MULTIPROCESS_NOTE_CREATE_EXCLUSIVITY=YES
```

Neither test permitted two successful fixed-ordinal attempt rows.

## Restart and ambiguity semantics

Synthetic temporary state, reopen of a new `At1ExecutionStore` on the same
SQLite file:

Case 1 — record NOTE_CREATE attempt, reopen before dispatch:

- `require_run_continuable()` raised `RunContinuationRefusedError`
  (`ATTEMPT_RECORDED`)
- second `record_attempt(..., operation_ordinal=1, operation_id="NOTE_CREATE")`
  raised `DuplicateBusinessOrdinalError`

Case 2 — record + `mark_dispatched`, reopen before response:

- `require_run_continuable()` raised `RunContinuationRefusedError`
  (`DISPATCHED`)
- second fixed-ordinal NOTE_CREATE insert was blocked

Case 3 — record + dispatch + response captured with no trustworthy parse or
semantic completion:

- `require_run_continuable()` raised `RunContinuationRefusedError`
  (`RESPONSE_CAPTURED` without durable successful parse and semantic
  completion)
- public projection `business_effect_truth=UNKNOWN`
- NOTE_CREATE ordinal `1` remained consumed
- second fixed-ordinal insert was blocked

```text
PROCESS_RESTART_PRESERVES_CONSUMPTION=YES
AMBIGUITY_POISONS_RUN=YES
SECOND_NOTE_CREATE_AFTER_RESTART_BLOCKED=YES
PRE_DISPATCH_CRASH_POISONS_RUN=YES
POST_DISPATCH_CRASH_POISONS_RUN=YES
```

## Store versus transport reuse

`At1ExecutionStore` can serve unchanged as the durable NOTE_CREATE reservation
primitive for a dedicated NOTE_PATH grant/run:

- grant/run claim keyed by `grant_run_id`
- fixed ordinal `1` insert as the reservation
- SQLite primary-key exclusivity across processes
- restart persistence
- fail-closed continuation after pre-dispatch, post-dispatch, and ambiguous
  completion

The store does not itself compute the NOTE_PATH grant/run mapping, and
`record_attempt()` does not internally require claim ownership. A later
NOTE_PATH integration seam must:

1. map reservation identity to `grant_run_id` using the mapping above
2. `acquire_claim(grant_run_id, owner_id)`
3. `require_run_continuable(grant_run_id)`
4. `record_attempt(..., operation_ordinal=1, operation_id="NOTE_CREATE")`

That seam is integration, not a store schema or API change.

`At1ExecutionStore.compute_public_projection()` remains AT1-sequence specific
(`create-note`, six ordinals, stage writes). NOTE_PATH must not treat that
projection as NOTE_PATH reservation truth. Using the store unchanged does not
require adapting that projection.

`At1LiveTransportAdapter` is not reusable for NOTE_PATH. It enforces the
legacy AT1 sequence and uses `next_operation_ordinal()`:

```text
get-contact
get-opportunity
create-note
get-note
update-opportunity
get-opportunity
```

Exact evidence does not support adapter reuse for a NOTE_PATH-only
POST/readback live path.

```text
AT1_EXECUTION_STORE_REUSE=YES_UNCHANGED
AT1_LIVE_TRANSPORT_ADAPTER_REUSE=NO
STORE_ADAPTATION_REQUIRED=NO
NOTE_PATH_STORE_INTEGRATION_REQUIRED=YES
DURABLE_LEDGER_IMPLEMENTATION_AUTHORIZATION_REQUIRED=NO
```

Reuse of the store is a fit finding only. It is not authorization to wire
NOTE_PATH to the store, adapt the store, reuse the live transport adapter, or
perform a live mutation.

## Final AT8D decision

```text
CAN_REUSE_AT1_EXECUTION_STORE_FOR_NOTE_PATH=YES

GRANT_RUN_ID_MAPPING=npgr1:sha256(canonical_json({consumer_authorization_identity,consumer_workflow_run_id,mapping_version=1,namespace=NOTE_PATH,operation=NOTE_CREATE}))

NOTE_CREATE_OPERATION_ORDINAL=1

LOCAL_DURABILITY_PROVEN=YES

PROCESS_RESTART_PRESERVES_CONSUMPTION=YES

PRE_DISPATCH_CRASH_POISONS_RUN=YES
POST_DISPATCH_CRASH_POISONS_RUN=YES

DIFFERENT_OWNER_SECOND_WORKER_BLOCKED=YES
SAME_OWNER_CONCURRENT_SECOND_WORKER_BLOCKED=YES
MULTIPROCESS_NOTE_CREATE_EXCLUSIVITY=YES

AMBIGUITY_POISONS_RUN=YES

AT1_EXECUTION_STORE_REUSE=YES_UNCHANGED
AT1_LIVE_TRANSPORT_ADAPTER_REUSE=NO

STORE_ADAPTATION_REQUIRED=NO
NOTE_PATH_STORE_INTEGRATION_REQUIRED=YES

DURABLE_LEDGER_IMPLEMENTATION_AUTHORIZATION_REQUIRED=NO

LIVE_MUTATION_AUTHORIZATION_READY=NO
```

## Blockers not closed by AT8D

AT8D answers AT8C Decision 1 fit questions only.

```text
BLOCKER_AT8C_1_STORE_FIT=VALIDATED_REUSE_UNCHANGED
BLOCKER_AT8C_2_CROSS_PROCESS_NOTE_CREATE=VALIDATED_YES

PRIVATE_AT8_CAPABILITY_HANDOFF=BLOCKED
BOUNDED_LIVE_NOTE_TRANSPORT=BLOCKED
LIVE_REAL_BINDING_MATERIALIZATION_EXISTS=NO
LIVE_NOTE_NETWORK_ADAPTER_VERIFIED=NO

LIVE_MUTATION_AUTHORIZATION_READY=NO
```

AT8D does not close capability-handoff or live-transport blockers. AT8D does
not issue implementation authorization, durable-ledger adaptation
authorization, live-transport authorization, or live-mutation authorization.

## Next governed sequence

```text
AT8D planning artifact
-> review/merge

NOTE_PATH store integration remains unauthorized here.
Capability-handoff remains blocked.
Bounded live-note transport remains blocked.

Then, only under later separate units:

separate private capability-handoff implementation authorization
-> bounded implementation
-> review/merge

separate bounded live-note-transport implementation authorization
-> bounded implementation
-> review/merge

separate NOTE_PATH store integration, if still required after those units,
under its own implementation authorization
-> bounded implementation
-> review/merge

Then:

read-only live execution boundary reinspection

Only if PASS:

separate one-shot live NOTE_PATH mutation authorization

Then, under that later grant only:

POST /contacts/{private_binding.contact_id}/notes
GET /contacts/{private_binding.contact_id}/notes/{same_run_note_id}

STAGE_PATH remains out of scope.
AT8E is not started by this unit.
```

## Validation boundary

```text
LOCAL_MACHINE_PATHS_PRESENT=NO
PRIVATE_BINDING_VALUES_PRESENT=NO
HIGHLEVEL_ACCESS=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
AUTHORIZATION_ISSUED=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO

STOP_CODE=NW008_AT8D_NOTE_PATH_AT1_EXECUTION_STORE_FIT_VALIDATION_READY_FOR_REVIEW
```
