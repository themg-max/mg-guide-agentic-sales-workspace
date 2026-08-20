# NW-008 AT-8G — NOTE_PATH → At1ExecutionStore Integration Proof 001

## Authorization and mode declarations

```text
AUTHORIZATION_ARTIFACT_PATH=
governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md

AUTHORIZATION_ARTIFACT_MERGE_SHA=
f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b

AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
IMPLEMENTATION_MODE=OFFLINE_ONLY

SOLE_CONSUMER_UNIT=
NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
```

```text
NETWORK_CALLS=0
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

CREDENTIAL_ACCESS=NO
SECRET_ACCESS=NO
IAM_CHANGE=NO
DEPLOYMENT_CHANGE=NO

STORE_INTERFACE_MODIFIED=NO
STORE_SCHEMA_MODIFIED=NO
TRUST_BOUNDARY_WEAKENED=NO
AT8F_R2_TRUST_MARKER_CHECKS_PRESERVED=YES
REDACTED_ENVELOPE_ONLY=YES
AMBIGUITY_TRUTH=UNKNOWN
NOTE_CREATE_OPERATION_ORDINAL=1
```

## Implementation base and head

```text
BASE_REF=origin/main
BASE_SHA=f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b
IMPLEMENTATION_HEAD_SHA=58c6aa19a2a184694e63642ee436ec5232537a1e
```

## Exact changed paths

1. `src/integrations/ghl/highlevel_rest/note_path.py`
2. `tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py`
3. `tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py`
4. `proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md`
5. `proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-proof-001.md`

## Diff summary

```text
 src/integrations/ghl/highlevel_rest/note_path.py                 | 236 ++++++++++++++++++
 tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py |   3 +-
 tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py  | 470 ++++++++++++++++++++++++++
 proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md  |  39 +++
 proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-proof-001.md        | 145 +++++++++
```

### What changed

- `note_path.py`:
  - Imported `At1ExecutionStore` and store contract errors.
  - Added `NOTE_CREATE_OPERATION_ORDINAL`, `_MAPPING_VERSION`, and `_GRANT_RUN_ID_NAMESPACE` constants.
  - Added optional `execution_store` keyword-only constructor parameter.
  - Added deterministic, privacy-preserving `grant_run_id` mapping that excludes `contact_id`, `location_id`, and all private CRM data.
  - Added redacted request/response envelope builders.
  - Added `_create_meeting_note_with_store` implementing the exact pre-reservation ordering:
    1. `_require_trusted_verified_capability()`
    2. `_validate_note_contract(note_contract)`
    3. deterministic `grant_run_id` mapping
    4. `store.acquire_claim(...)`
    5. `store.require_run_continuable(...)`
    6. `store.record_attempt(ordinal=1, operation_id="NOTE_CREATE")`
    7. `store.mark_dispatched(...)`
    8. `DeterministicFakeTransport.dispatch(...)`
    9. `store.capture_response(...)`
    10. `store.record_parse_outcome(...)`
    11. `store.record_semantic_outcome(...)`
    12. terminalize with `business_effect_truth=UNKNOWN` when required
  - `DuplicateBusinessOrdinalError`, `RunContinuationRefusedError`, `ExecutionClaimError`, and `AttemptStateError` are translated to `TransportError` with chained cause.
  - `BindingError` and `NoteContractError` behavior is unchanged.
  - When `execution_store` is `None`, the original process-local behavior is preserved.

- `test_private_at8_capability_handoff.py`:
  - Updated `test_no_provider_get_and_zero_network_effects` to expect `At1ExecutionStore` integration in `note_path.py` while maintaining zero-network-call assertions.

- `test_note_path_at1_execution_store.py` (new):
  - Offline deterministic coverage for all Phase 4 requirements, including capability/contract ordering, dispatch ordering, ordinal uniqueness, grant id determinism, privacy of redacted envelopes, error-boundary translation, owner/reclaim/contention semantics, restart reservation, ambiguity terminalization, PR107 capability enforcement, and projection non-use.

- `nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md` (new):
  - Authorization consumption record with merge SHA verification and mode declarations.

## Tests executed

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_note_path.py -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py -q
.venv/bin/python -m pytest tests/integrations/ghl/test_at1_live_transport_remediation.py -q
.venv/bin/python -m pytest tests/integrations/ghl/test_bounded_at1_executor.py -q
```

## Test results

- Full suite: passed (exit code 0).
- `test_note_path.py`: 50 passed.
- `test_note_path_at1_execution_store.py`: 20 passed.
- `test_private_at8_capability_handoff.py`: 35 passed.
- `test_at1_live_transport_remediation.py`: 19 passed.
- `test_bounded_at1_executor.py`: 28 passed.

No network calls, HighLevel access, CRM mutations, or external effects occurred.

## Validation

- `git diff --check`: clean (no trailing whitespace or conflict markers).
- No blocked path was modified.
- `origin/main` ancestry verified to include both:
  - `f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b` (authorization merge SHA)
  - `6886f2cd9838055fef96a27612738efa2bd16f9b` (reviewed authorization head)
- Authorization artifact `governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md` exists on `origin/main` and names the sole authorized consumer unit `NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001`.
