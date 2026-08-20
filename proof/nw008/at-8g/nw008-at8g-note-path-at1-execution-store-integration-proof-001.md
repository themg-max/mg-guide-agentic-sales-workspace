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

## §16 proof-return fields

```text
PROOF_UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
SOLE_CONSUMER_UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b
IMPLEMENTATION_MODE=OFFLINE_ONLY
NETWORK_CALLS=0
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
CREDENTIAL_ACCESS=NO
SECRET_ACCESS=NO
IAM_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION=NO

STORE_INTERFACE_MODIFIED=NO
STORE_SCHEMA_MODIFIED=NO
TRUST_BOUNDARY_WEAKENED=NO
AT8F_R2_TRUST_MARKER_CHECKS_PRESERVED=YES
PRE_RESERVATION_CAPABILITY_CHECK=YES
PRE_RESERVATION_NOTE_CONTRACT_VALIDATION=YES
MARK_DISPATCHED_BEFORE_TRANSPORT_DISPATCH=YES
REDACTED_ENVELOPE_ONLY=YES
AMBIGUITY_TRUTH=UNKNOWN
ERROR_TRANSLATION_TO_TRANSPORT_ERROR=YES
ADAPTER_INSTANCE_IS_OWNER=NO
CLAIM_OWNER_ID=consumer_authorization_identity

GRANT_RUN_ID_MAPPING_VERIFIED=YES
NOTE_CREATE_OPERATION_ORDINAL=1
NOTE_CREATE_RESERVATION_ATOMICITY=SQLITE_PK
RUN_CONTINUABLE_GATE_ENFORCED=YES
CLAIM_GATE_ENFORCED=YES

TEST_SUITE_ALL_PASS=YES
EXISTING_NOTE_PATH_TESTS_STILL_PASS=YES
EXISTING_STORE_TESTS_STILL_PASS=YES

AT8G_AUTHORIZATION_GRANTS_LIVE_NOTE_TRANSPORT=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_CRM_MUTATION=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO
```

## Implementation base and head

```text
BASE_REF=origin/main
BASE_SHA=f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b
PREVIOUS_REVIEWED_HEAD_SHA=c5c66fbdc6aebcf9d3ff94aeab83c31395fa6d65
IMPLEMENTATION_HEAD_SHA=PENDING_REPAIR_COMMIT
```

## Exact changed paths

1. `src/integrations/ghl/highlevel_rest/note_path.py`
2. `tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py`
3. `tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py`
4. `proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md`
5. `proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-proof-001.md`

## Diff summary

```text
 src/integrations/ghl/highlevel_rest/note_path.py                 | store-seam + bounded repair
 tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py | 3 +-
 tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py  | AT8G coverage + bounded repair
 proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md | consumption record
 proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-proof-001.md | §16 proof-return
```

### What changed

- `note_path.py`:
  - Imported `At1ExecutionStore` and store contract errors.
  - Added `NOTE_CREATE_OPERATION_ORDINAL`, `_MAPPING_VERSION`, `_GRANT_RUN_ID_NAMESPACE`, and `_GRANT_RUN_ID_PREFIX`.
  - Added optional `execution_store` keyword-only constructor parameter.
  - Implemented exact grant/run mapping `GRANT_RUN_ID_FORMULA=npgr1:sha256(canonical_json(canonical_inputs))` as `npgr1:` plus 64-char lowercase sha256 hex. Canonical inputs were not altered. `contact_id`, `location_id`, and all private CRM identifiers remain excluded.
  - Persisted request/response envelopes use only the authorization allowlist (or a strict subset). Response envelopes no longer persist `status` or `provider_note_id_digest`. Response class is `response_status_class` (`ok` | `ambiguous` | `error`).
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
  - Every authorized At1ExecutionStore call at the NOTE_PATH boundary, including reservation calls plus `capture_response`, `record_parse_outcome`, `record_semantic_outcome`, and `mark_terminal`, translates `ExecutionClaimError`, `RunContinuationRefusedError`, `DuplicateBusinessOrdinalError`, and `AttemptStateError` to `TransportError` with the original exception chained as cause (`raise TransportError(...) from exc`).
  - `BindingError` and `NoteContractError` behavior is unchanged.
  - When `execution_store` is `None`, the original process-local behavior is preserved.

- `test_private_at8_capability_handoff.py`:
  - Updated `test_no_provider_get_and_zero_network_effects` to expect `At1ExecutionStore` integration in `note_path.py` while maintaining zero-network-call assertions.

- `test_note_path_at1_execution_store.py`:
  - Offline deterministic coverage for Phase 4 requirements, including capability/contract ordering, dispatch ordering, ordinal uniqueness, grant id determinism, privacy of redacted envelopes, error-boundary translation, owner/reclaim/contention semantics, restart reservation, ambiguity terminalization, PR107 capability enforcement, and projection non-use.
  - Independently asserts `grant_run_id` prefix `npgr1:`, 64-char lowercase sha256 digest suffix, identical mapping across different contact/location, and distinct mapping across authorization identity and workflow run.
  - Replaced same-object restart coverage with a true restart: store A on a temp SQLite path consumes NOTE_CREATE, A is closed/discarded, store B reopens the same path and key, and replay is blocked before a second POST.
  - Deterministic fault-injection proves raw `AttemptStateError` cannot leak from `record_parse_outcome`, `record_semantic_outcome`, `capture_response`, or `mark_terminal`.

- `nw008-at8g-note-path-at1-execution-store-integration-consumption-001.md`:
  - Authorization consumption record with merge SHA verification and mode declarations.

## Tests executed

```bash
git diff --check
.venv/bin/python -m pytest tests/ -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_note_path.py -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py -q
.venv/bin/python -m pytest tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py -q
.venv/bin/python -m pytest tests/integrations/ghl/test_at1_live_transport_remediation.py -q
.venv/bin/python -m pytest tests/integrations/ghl/test_bounded_at1_executor.py -q
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

## Test results

- `git diff --check`: clean.
- Full suite (`tests/`): 567 passed (exit code 0).
- `test_note_path.py`: 50 passed.
- `test_note_path_at1_execution_store.py`: 25 passed.
- `test_private_at8_capability_handoff.py`: 34 passed.
- `test_at1_live_transport_remediation.py`: 21 passed.
- `test_bounded_at1_executor.py`: 26 passed.
- Phase 1 deterministic validation: PASS.

No network calls, HighLevel access, CRM mutations, or external effects occurred.

AT10 proof files under `proof/nw008/at-10/**` were not modified by this repair. Any incidental local mutation from the full-suite run was restored to HEAD before staging.

## Validation

- `git diff --check`: clean (no trailing whitespace or conflict markers).
- No blocked path was modified.
- `origin/main` ancestry verified to include:
  - `f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b` (authorization merge SHA)
- Authorization artifact `governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md` exists on `origin/main` and names the sole authorized consumer unit `NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001`.
- AT8G does not grant live note transport, live CRM mutation, or live mutation authorization readiness.
