# NW-008 AT-8G — NOTE_PATH → At1ExecutionStore Integration Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=governance/nw008-at8g-note-path-at1-execution-store-integration-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md

BASE_REF=origin/main
BASE_SHA=b2d1d2cc1d6e01ef1760a5af6b970d08fb02561a

PREDECESSOR_PR=107
PREDECESSOR_HEAD_SHA=9ad5999ad82a7412d9a09ee86c32d51d02312c88
PREDECESSOR_MERGE_SHA=b2d1d2cc1d6e01ef1760a5af6b970d08fb02561a
PREDECESSOR_MERGE_VERIFIED=YES

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE

GRANT=NOTE_PATH_AT1_EXECUTION_STORE_OFFLINE_INTEGRATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN

AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES

IMPLEMENTATION_MODE=OFFLINE_ONLY
```

This artifact is an authorization proposal only. Creating, reviewing, or merging it does not integrate `At1ExecutionStore` into `NotePathAdapter`, load a credential, touch HighLevel, retrieve a private CRM binding, issue a contact GET, issue a note POST, activate live transport, mutate production configuration, or produce any live external effect.

The sole authorized consumer is `NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001`. No other unit may consume this grant.

### Activation semantics

```text
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
```

At authoring, this grant is proposed and not effective. Effectiveness is not a mutable field inside this file. Effectiveness is established only by repository state:

1. the exact authorization artifact path is present on `main` via human review and merge; and
2. the authorized consumer unit `NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001` independently verifies that merge (exact path on `origin/main` / merge ancestry) before writing integration code.

The artifact text does not need to mutate after merge to become effective. Rewriting any effectiveness field inside this file is forbidden and is not an activation mechanism.

This grant is one-shot, non-reusable, and non-transferable. It is not runtime execution authority, not live-read authority, not live-mutation authority, not a live-transport implementation grant, not a network-client implementation grant, not a credential grant, not a Secret Manager grant, not a deployment or IAM grant, and not a standing reusable authority.

```text
INTEGRATION_SLICE=NOTE_PATH_NOTE_CREATE_RESERVATION_TO_AT1_EXECUTION_STORE
INTEGRATION_MODE=OFFLINE_ONLY
GRANT_PERMITS_WHEN_EFFECTIVE=OFFLINE_NOTE_PATH_TO_AT1_EXECUTION_STORE_INTEGRATION_ONLY

NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
CREDENTIAL_USE_AUTHORIZED=NO
SECRET_ACCESS=NO
SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_TRANSPORT_IMPLEMENTATION_AUTHORIZED=NO
NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
BOUNDED_LIVE_NOTE_TRANSPORT_AUTHORIZATION=FROZEN
LIVE_NOTE_MUTATION_AUTHORIZATION=FROZEN
LIVE_MUTATION_AUTHORIZATION_READY=NO
EXTERNAL_EFFECTS_ALLOWED=0
```

### Non-transitivity

```text
PR107_TRUST_REPAIR_GRANTS_AT8G_IMPLEMENTATION=NO
AT10_EXECUTION_OR_COMPLETION_AUTHORITY_GRANTS_AT8G=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_NOTE_TRANSPORT=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_CRM_MUTATION=NO

AT8G_INTEGRATION_AUTHORIZATION_INFERRED_FROM_PR107=NO
AT8G_INTEGRATION_AUTHORIZATION_INFERRED_FROM_AT10=NO
```

PR107 closed the private AT8 capability-handoff trust-boundary defect. That closure removes a blocker; it does not grant AT8G implementation. AT10 completion/reconciliation is a later independent lane; it provides no authority to AT8G. This authorization, even after merge, does not grant live note transport or live CRM mutation.

## 2. Verified prerequisites and source provenance

Preflight was run before this artifact was authored.

```text
Working branch is not main
YES

PR107_MERGED
YES
PR107_HEAD_SHA=9ad5999ad82a7412d9a09ee86c32d51d02312c88
PR107_MERGE_SHA=b2d1d2cc1d6e01ef1760a5af6b970d08fb02561a
PREDECESSOR_MERGE_SHA is HEAD of origin/main
YES

AT8C_BLOCKER_3_PRIVATE_AT8_CAPABILITY_HANDOFF=CLOSED
```

| Precondition                                                    | Result |
| ---                                                             | ---    |
| Working branch is not `main`                                    | YES    |
| Predecessor PR #107 merge commit                                | `b2d1d2cc1d6e01ef1760a5af6b970d08fb02561a` |
| Predecessor merge commit is reachable from `origin/main`        | YES    |
| PR107 head SHA present in ancestry                              | `9ad5999ad82a7412d9a09ee86c32d51d02312c88` |
| AT8C blocker 3 (private AT8 capability handoff) closed by PR107 | YES    |
| AT8D fit finding present in repo                                | YES    |
| At1ExecutionStore reuse fit                                     | `YES_UNCHANGED` |
| NOTE_PATH already integrated with At1ExecutionStore             | NO     |
| This unit executed a live GET                                   | NO     |
| This unit executed a live POST                                  | NO     |
| This unit loaded credentials                                    | NO     |
| This unit accessed HighLevel                                    | NO     |
| Live mutation authorization issued                              | NO     |
| Consumer implementation performed by this unit                  | NO     |

### Predecessor authority scope

```text
PR107_AUTHORIZES_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR=YES
PR107_AUTHORIZES_NOTE_PATH_STORE_INTEGRATION=NO
PR107_AUTHORIZES_LIVE_TRANSPORT=NO
PR107_AUTHORIZES_LIVE_MUTATION=NO
PR107_TRUST_REPAIR_GRANTS_AT8G_IMPLEMENTATION=NO
```

Authorization for NOTE_PATH → At1ExecutionStore integration is not inferred from PR107. PR107 closed the private AT8 capability-handoff trust-boundary defect; that closure removes a blocker but does not grant integration authority. AT8G integration authority is issued only by this artifact after its own review and merge, and only after the consumer independently verifies that merge.

### AT8D fit finding carried forward (finding, not authority)

```text
AT1_EXECUTION_STORE_REUSE_FIT=YES_UNCHANGED
STORE_ADAPTATION_REQUIRED=NO
NOTE_PATH_STORE_INTEGRATION_REQUIRED=YES
NOTE_PATH_STORE_INTEGRATION_AUTHORIZED=NO
DURABLE_LEDGER_IMPLEMENTATION_AUTHORIZATION_REQUIRED=NO
```

AT8D established that `At1ExecutionStore` can serve unchanged as the durable NOTE_CREATE reservation primitive for a dedicated NOTE_PATH grant/run. AT8D was a planning/validation artifact only and did not authorize integration. AT8G is that separate integration authorization.

### AT10 normalization (no authority reuse)

```text
AT10_LANE=INDEPENDENT
AT10_CURRENT_STATE=COMPLETE_VIA_LATER_COMPLETION_RECONCILIATION_LANE
AT10_EXECUTION_OR_COMPLETION_AUTHORITY_GRANTS_AT8G=NO
AT10_HISTORICAL_PROOF_FILES_MODIFIED_BY_AT8G=NO
AT10_COMPLETE_NO_MUST_NOT_BE_COPIED_INTO_CURRENT_PROJECT_STATE=YES
```

Do not modify historical AT10 proof files. Do not copy historical `AT10_COMPLETE=NO` into current project state. AT10 provides no authority to AT8G.

## 3. Exact reusable At1ExecutionStore interface

The consumer must reuse the following public surface of `src/integrations/ghl/at1_execution_store.py` **unchanged**. The consumer must not add methods, modify signatures, rename fields, alter SQL schema, or change error semantics.

```text
CLASS=At1ExecutionStore
CONSTRUCTOR=At1ExecutionStore(db_path: str | Path, commitment_key: str)
```

Authorized methods (call-only; no modification):

```text
acquire_claim(grant_run_id: str, owner_id: str) -> None
assert_claim_owner(grant_run_id: str, owner_id: str) -> None
require_run_continuable(grant_run_id: str) -> None
record_attempt(*, grant_run_id, operation_ordinal, operation_id, request_id, request_envelope) -> str
mark_dispatched(*, grant_run_id, operation_ordinal) -> None
capture_response(*, grant_run_id, operation_ordinal, response_envelope) -> str
record_parse_outcome(*, grant_run_id, operation_ordinal, success: bool) -> None
record_semantic_outcome(*, grant_run_id, operation_ordinal, success: bool) -> None
mark_terminal(*, grant_run_id, operation_ordinal, failure_code, business_effect_truth) -> None
list_private_attempts(grant_run_id: str) -> list[dict]
db_path (read-only property)
```

Authorized error types (catch/raise as documented; no shadowing, no subclassing across module boundary):

```text
ExecutionClaimError
DuplicateBusinessOrdinalError
AttemptStateError
RunContinuationRefusedError
```

Explicit reservation primitives:

```text
ATOMIC_RESERVATION_PRIMITIVE=record_attempt(operation_ordinal=1, operation_id="NOTE_CREATE")
ATOMICITY_SOURCE=SQLITE_PRIMARY_KEY(attempts.grant_run_id, attempts.operation_ordinal)
DUPLICATE_RESERVATION_SIGNAL=DuplicateBusinessOrdinalError
CONTINUATION_GATE=require_run_continuable(grant_run_id)
CLAIM_GATE=acquire_claim(grant_run_id, owner_id=CLAIM_OWNER_ID)
CLAIM_OWNER_ID=consumer_authorization_identity
ADAPTER_INSTANCE_IS_OWNER=NO
SAME_AUTHORIZATION_IDENTITY_RECLAIM_ALLOWED=YES
```

Explicitly **not** authorized for use as NOTE_PATH reservation truth:

```text
next_operation_ordinal — MUST NOT be used to allocate NOTE_PATH ordinals
compute_public_projection — AT1-sequence specific (create-note/get-note/update-opportunity/six ordinals); MUST NOT be consumed as NOTE_PATH reservation truth
```

## 4. Exact NOTE_PATH producer/consumer boundary

Producer of reservation identity (unchanged inputs from `src/integrations/ghl/highlevel_rest/note_path.py`):

```text
consumer_authorization_identity : str  # already an adapter constructor argument
consumer_workflow_run_id        : str  # already an adapter constructor argument
operation                       = "NOTE_CREATE" (fixed constant _NOTE_CREATE_OPERATION)
```

Current NOTE_PATH reservation consumer (to be replaced at the exact seam only):

```text
_SharedProcessLocalTestLedger._states  # process-local, in-memory
_SharedProcessLocalTestLedger.reserve(_MutationBudgetKey)
_SharedProcessLocalTestLedger.mark_terminal(_MutationBudgetKey)
NotePathAdapter._reserve_note_create_budget()
```

That process-local ledger is not authoritative for cross-process reservation and has never been authorized as live-mutation truth. AT8G authorizes replacement of the NOTE_CREATE reservation seam only, keeping the module's public surface behavior identical from the caller's perspective.

Public surface of `NotePathAdapter` (must remain call-compatible):

```text
NotePathAdapter(location_id, contact_id, transport, *, consumer_authorization_identity, consumer_workflow_run_id)
NotePathAdapter.get_bound_contact(adapter)  # closure-bound helper
NotePathAdapter.create_meeting_note(note_contract) -> CreatedMeetingNote
NotePathAdapter.verify_meeting_note() -> VerifiedMeetingNote
NotePathAdapter.CONTACT_PREFLIGHT_VERIFIED
NotePathAdapter.POST_ATTEMPTS
```

The AT-8F/R2 verified-contact capability handoff surface (issued and validated internally) must not be relaxed by AT8G. AT8G integration must not weaken any of the trust-marker checks introduced by PR107.

### Exact pre-reservation sequence

The following two checks MUST occur, in this order, **before** any store claim or reservation call (`acquire_claim`, `require_run_continuable`, or `record_attempt`):

```text
1. PR107 verified-contact capability check
   _require_trusted_verified_capability() MUST succeed
2. NOTE contract validation and canonicalization
   _validate_note_contract(note_contract) MUST succeed and produce the canonical note
```

Reservation MUST NOT begin if either check fails. Capability failure remains a `BindingError`. Contract failure remains a `NoteContractError`. Store errors MUST NOT be raised in place of those domain errors.

## 5. Deterministic grant_run_id mapping (carried forward from AT8D)

```text
MAPPING_VERSION=1
NAMESPACE=NOTE_PATH
OPERATION=NOTE_CREATE
CANONICAL_ENCODING=UTF-8 JSON, sort_keys=True, separators=(",", ":")
CANONICAL_INPUTS={consumer_authorization_identity, consumer_workflow_run_id, mapping_version, namespace, operation}
EXCLUDED_INPUTS={contact_id, location_id, any private CRM identifier}
GRANT_RUN_ID_FORMULA=npgr1:sha256(canonical_json(canonical_inputs))
NOTE_CREATE_OPERATION_ORDINAL=1
```

Consumer must implement the mapping exactly as above. No new inputs may be added to the canonical payload. `contact_id` and `location_id` are private binding data and must not appear in the mapping key.

## 6. Claim owner normalization

```text
CLAIM_OWNER_ID=consumer_authorization_identity
ADAPTER_INSTANCE_IS_OWNER=NO
SAME_AUTHORIZATION_IDENTITY_RECLAIM_ALLOWED=YES
```

Claim ownership is the authorization identity string, not the adapter instance. Same authorization identity may reclaim the same `grant_run_id` (store same-owner reclaim). A different authorization identity cannot acquire the same claim. Adapter object identity is not an owner key.

## 7. Durable evidence privacy

AT8G must persist a **redacted NOTE_PATH reservation-evidence envelope** into `At1ExecutionStore`. The store receives digests and non-private metadata only.

```text
NOTE_PATH_STORE_ENVELOPE=REDACTED_RESERVATION_EVIDENCE
RAW_CONTACT_ID_PERSISTED=FORBIDDEN
RAW_LOCATION_ID_PERSISTED=FORBIDDEN
RAW_NOTE_BODY_PERSISTED=FORBIDDEN
RAW_MEETING_SUMMARY_PERSISTED=FORBIDDEN
RAW_NEEDS_PERSISTED=FORBIDDEN
RAW_OBJECTIONS_PERSISTED=FORBIDDEN
RAW_COMMITMENTS_PERSISTED=FORBIDDEN
RAW_PROVIDER_NOTE_ID_PERSISTED=FORBIDDEN
```

Permitted envelope fields (non-private metadata and digests only):

```text
namespace
operation
operation_ordinal
mapping_version
consumer_authorization_identity
consumer_workflow_run_id
workflow_id
request_id
note_content_digest
provider_body_digest
parse_success
semantic_success
terminal_failure_code
business_effect_truth
response_status_class   # e.g. ok | ambiguous | error — not a provider payload
```

`request_envelope` and `response_envelope` passed to `record_attempt` / `capture_response` MUST be this redacted envelope (or a strict subset). They MUST NOT contain raw `contact_id`, `location_id`, note body, meeting summary, needs, objections, commitments, or provider note ID.

`request_id` MUST be derived without embedding private CRM identifiers.

## 8. Required integration sequence

The consumer implementation must perform these steps in this exact order for the single NOTE_CREATE reservation in a NOTE_PATH grant/run:

```text
PRE-RESERVATION (mandatory, before any store write):
  1. _require_trusted_verified_capability()
  2. canonical_note = _validate_note_contract(note_contract)

RESERVATION AND DURABLE LIFECYCLE:
  3. compute grant_run_id via §5 mapping
  4. store.acquire_claim(grant_run_id, owner_id=consumer_authorization_identity)
  5. store.require_run_continuable(grant_run_id)
  6. store.record_attempt(
         grant_run_id=grant_run_id,
         operation_ordinal=1,
         operation_id="NOTE_CREATE",
         request_id=<deterministic redacted request id>,
         request_envelope=<redacted reservation-evidence envelope>,
     )
  7. store.mark_dispatched(grant_run_id, operation_ordinal=1)
  8. DeterministicFakeTransport.dispatch(...)   # existing offline fixture transport only
  9. store.capture_response(
         grant_run_id=grant_run_id,
         operation_ordinal=1,
         response_envelope=<redacted reservation-evidence envelope>,
     )
 10. store.record_parse_outcome(..., success=True|False)
 11. store.record_semantic_outcome(..., success=True|False)
 12. on terminal failure or ambiguity: store.mark_terminal(..., failure_code, business_effect_truth)
```

Required durable lifecycle order:

```text
record_attempt
-> mark_dispatched
-> DeterministicFakeTransport dispatch
-> capture_response
-> parse outcome
-> semantic outcome
-> terminalization if required
```

Do not authorize:

```text
record_attempt
-> dispatch
-> mark_dispatched
```

`mark_dispatched` MUST occur before fixture dispatch. Dispatching before `mark_dispatched` is forbidden. Steps 8–12 remain within the existing offline fixture transport; no live dispatch is authorized.

## 9. Ambiguity truth

After `mark_dispatched`, any ambiguous, uncertain, or unproven execution MUST terminalize with:

```text
business_effect_truth=UNKNOWN
```

```text
AMBIGUITY_AFTER_DISPATCH_TRUTH=UNKNOWN
UNPROVEN_ABSENCE_OF_EFFECT_MAY_NOT_ASSERT_NO=YES
BUSINESS_EFFECT_TRUTH_NO_REQUIRES_PROVEN_ABSENCE=YES
```

Never assert `business_effect_truth=NO` unless absence of business effect is actually proven. An ambiguous fixture response, a crash window after dispatch, a missing parse, or a missing semantic completion is `UNKNOWN`, not `NO`.

## 10. Error translation

Store exceptions MUST be translated at the NOTE_PATH boundary to `TransportError`, preserving the original exception as the chained cause (`raise TransportError(...) from exc`).

```text
DuplicateBusinessOrdinalError -> TransportError
RunContinuationRefusedError   -> TransportError
ExecutionClaimError           -> TransportError
AttemptStateError             -> TransportError
```

```text
ERROR_TRANSLATION_PRESERVES_CAUSE=YES
BINDINGERROR_AND_NOTECONTRACTERROR_UNCHANGED=YES
```

Capability and note-contract failures remain `BindingError` and `NoteContractError`. They MUST NOT be rewritten as `TransportError`.

## 11. Writable paths (consumer implementation)

The consumer unit is authorized to modify only:

```text
src/integrations/ghl/highlevel_rest/note_path.py
tests/integrations/ghl/highlevel_rest/**
tests/integrations/ghl/test_at8g_note_path_at1_execution_store_integration.py
proof/nw008/at-8g/**
docs/nw008/nw-008-at8g-*
governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md
```

`tests/integrations/ghl/test_at8g_note_path_at1_execution_store_integration.py` is the single explicitly named cross-boundary AT8G test file. It may be created only if a test cannot live under `tests/integrations/ghl/highlevel_rest/**`. No other cross-boundary test path is authorized.

`note_path.py` edits are restricted to the reservation seam described in §4/§8 plus the minimum wiring required to hold and query an `At1ExecutionStore` instance (constructor parameter and store attribute). The verified-capability handoff, contact preflight, note-contract validation, canonical serialization, and readback digest comparison must remain byte-identical except for the ordered pre-reservation / lifecycle calls required by this artifact.

```text
FIXTURE_MODIFICATION_DEFAULT=NO
FIXTURE_MODIFICATION_AUTHORIZED=NO
```

Fixture modification is not authorized by this artifact. If a later amendment explicitly authorizes a named fixture path, that amendment is a separate review. Until then:

```text
fixtures/**  BLOCKED
```

## 12. Blocked paths (consumer implementation)

The following files must not be modified by the consumer under this grant:

```text
src/integrations/ghl/at1_execution_store.py             # BLOCKED — reuse unchanged
src/integrations/ghl/at1_live_transport_adapter.py      # BLOCKED — not reusable per AT8D
src/integrations/ghl/at1_live_transport_serializer.py   # BLOCKED
src/integrations/ghl/bounded_at1_executor.py            # BLOCKED
src/integrations/ghl/read_adapter.py                    # BLOCKED
src/integrations/ghl/highlevel_rest/fake_transport.py   # BLOCKED (transport shape frozen)
src/integrations/ghl/__init__.py                        # BLOCKED (public export surface frozen)
src/integrations/ghl/highlevel_rest/__init__.py         # BLOCKED (public export surface frozen)
contracts/**                                            # BLOCKED
src/orchestration/**                                    # BLOCKED
src/agents/**                                           # BLOCKED
src/mg_guide/**                                         # BLOCKED
workspace_addon/**                                      # BLOCKED
governance/GOVERNANCE_PROFILE.yaml                      # BLOCKED
governance/PUBLIC_PRIVATE_BOUNDARY.md                   # BLOCKED
governance/REQUIRED_PR_CHECKS.md                        # BLOCKED
governance/required-pr-checks.md                        # BLOCKED
governance/EXECUTION_MANIFEST.schema.yaml               # BLOCKED
governance/PROOF_RETURN.schema.yaml                     # BLOCKED
governance/authorizations/*                             # BLOCKED except this exact AT8G artifact
proof/nw008/at-10/**                                    # BLOCKED (do not modify historical AT10 proof files)
fixtures/**                                             # BLOCKED (fixture modification default NO)
.github/**                                              # BLOCKED
Dockerfile                                              # BLOCKED
.env.example                                            # BLOCKED
requirements.txt                                        # BLOCKED
pyproject.toml                                          # BLOCKED
scripts/**                                              # BLOCKED
local/**                                                # BLOCKED
```

AT10 implementation artifacts must not be merged into this lane merely because they exist. AT8G authorization is scoped strictly to the NOTE_PATH ↔ At1ExecutionStore reservation seam.

## 13. Offline-only execution posture

```text
IMPLEMENTATION_MODE=OFFLINE_ONLY
TRANSPORT=DeterministicFakeTransport (existing) OR test-supplied fixture transport
LIVE_TRANSPORT_IMPLEMENTATION=FORBIDDEN
NETWORK_CLIENT_IMPLEMENTATION=FORBIDDEN
NETWORK_CALLS=0
HIGHLEVEL_ACCESS=NO
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
SQLITE_DB_PATH=TEMPORARY_TEST_PATH_ONLY
SQLITE_DB_ON_MAIN_BRANCH_RUNTIME_WIRING=NO
```

The consumer must not introduce a production-time SQLite path, environment lookup, service account, credentials loader, or `google-cloud-secret-manager` client. All store instances used under this grant are constructed with test-supplied temporary paths and test-supplied `commitment_key` values.

## 14. Deterministic fixtures and tests required

Consumer implementation must produce deterministic tests. All tests must be repeatable, offline, and free of wall-clock/random dependencies aside from what is already used in the existing NOTE_PATH tests. Tests live under `tests/integrations/ghl/highlevel_rest/**` and, if required, the single named file `tests/integrations/ghl/test_at8g_note_path_at1_execution_store_integration.py`.

Required test coverage:

```text
TEST: PRE_RESERVATION_CAPABILITY_CHECK_BEFORE_STORE
DESC: _require_trusted_verified_capability runs before acquire_claim / record_attempt.
REQUIREMENT: PASS

TEST: PRE_RESERVATION_NOTE_CONTRACT_VALIDATION_BEFORE_STORE
DESC: _validate_note_contract / canonicalization runs before acquire_claim / record_attempt.
REQUIREMENT: PASS

TEST: MARK_DISPATCHED_BEFORE_TRANSPORT_DISPATCH
DESC: store.mark_dispatched occurs before DeterministicFakeTransport.dispatch.
REQUIREMENT: PASS

TEST: DISPATCH_BEFORE_MARK_DISPATCHED_FORBIDDEN
DESC: The unauthorized order record_attempt -> dispatch -> mark_dispatched is not used.
REQUIREMENT: PASS

TEST: NOTE_CREATE_RESERVATION_USES_STORE_RECORD_ATTEMPT
DESC: A successful note POST records exactly one attempt row at ordinal 1 with operation_id "NOTE_CREATE".
REQUIREMENT: PASS

TEST: SECOND_NOTE_CREATE_IN_SAME_GRANT_RUN_BLOCKED
DESC: Second call to create_meeting_note under the same authorization identity + workflow run raises TransportError.
REQUIREMENT: PASS

TEST: DIFFERENT_WORKFLOW_RUN_MAPS_TO_DIFFERENT_GRANT_RUN
DESC: Changing consumer_workflow_run_id yields a different grant_run_id and a new NOTE_CREATE reservation succeeds.
REQUIREMENT: PASS

TEST: DIFFERENT_AUTHORIZATION_MAPS_TO_DIFFERENT_GRANT_RUN
DESC: Changing consumer_authorization_identity yields a different grant_run_id and a new NOTE_CREATE reservation succeeds.
REQUIREMENT: PASS

TEST: CONTACT_ID_AND_LOCATION_ID_NOT_IN_MAPPING
DESC: Same authorization + workflow run + different contact_id/location_id maps to the same grant_run_id.
REQUIREMENT: PASS

TEST: REDACTED_ENVELOPE_HAS_NO_PRIVATE_FIELDS
DESC: Persisted request_envelope and response_envelope contain no raw contact_id, location_id, note body, meeting summary, needs, objections, commitments, or provider note ID.
REQUIREMENT: PASS

TEST: DUPLICATE_BUSINESS_ORDINAL_TRANSLATES_TO_TRANSPORT_ERROR
DESC: Second record_attempt at ordinal 1 raises DuplicateBusinessOrdinalError chained as cause of TransportError.
REQUIREMENT: PASS

TEST: RUN_CONTINUABLE_GATE_TRANSLATES_TO_TRANSPORT_ERROR
DESC: Unresolved prior attempt refuses via RunContinuationRefusedError chained as cause of TransportError.
REQUIREMENT: PASS

TEST: CLAIM_OWNER_IS_AUTHORIZATION_IDENTITY
DESC: Claim owner_id is consumer_authorization_identity; adapter instance is not owner. Second distinct authorization identity cannot acquire the same claim; ExecutionClaimError is chained as cause of TransportError.
REQUIREMENT: PASS

TEST: SAME_AUTHORIZATION_IDENTITY_RECLAIM_ALLOWED
DESC: Same consumer_authorization_identity may reclaim the same grant_run_id claim.
REQUIREMENT: PASS

TEST: RESTART_PRESERVES_RESERVATION
DESC: Reopening At1ExecutionStore on the same SQLite path preserves NOTE_CREATE ordinal consumption; second reservation is blocked.
REQUIREMENT: PASS

TEST: AMBIGUITY_TERMINALIZES_UNKNOWN
DESC: Ambiguous/uncertain post-dispatch execution terminalizes with business_effect_truth=UNKNOWN, never NO.
REQUIREMENT: PASS

TEST: VERIFIED_CAPABILITY_STILL_REQUIRED
DESC: Reservation cannot proceed without a valid PR107 verified-contact capability; existing trust-boundary tests remain green.
REQUIREMENT: PASS

TEST: NO_NETWORK_CALLS_IN_STORE_INTEGRATION_TESTS
DESC: NETWORK_CALLS == 0, HIGHLEVEL_NETWORK_CALLS == 0, EXTERNAL_EFFECTS == 0 across all AT8G tests.
REQUIREMENT: PASS

TEST: EXISTING_NOTE_PATH_TESTS_REMAIN_GREEN
DESC: The full existing tests/integrations/ghl/highlevel_rest/ suite passes unchanged in intent.
REQUIREMENT: PASS

TEST: PROJECTION_NOT_TREATED_AS_NOTE_PATH_TRUTH
DESC: NOTE_PATH does not consume At1ExecutionStore.compute_public_projection as reservation truth.
REQUIREMENT: PASS
```

```text
FIXTURE_MODIFICATION_DEFAULT=NO
TEST_IDS=SYNTHETIC_ONLY
```

## 15. Idempotency and replay expectations

```text
NOTE_CREATE_RESERVATION_IDEMPOTENCY=SAME_AUTHORIZATION_IDENTITY_RECLAIM_ALLOWED
NOTE_CREATE_RESERVATION_EXCLUSIVITY=CROSS_PROCESS_AT_SQLITE_PK
REPLAY_AFTER_SUCCESSFUL_ATTEMPT=REFUSED via DuplicateBusinessOrdinalError -> TransportError
REPLAY_AFTER_UNRESOLVED_ATTEMPT=REFUSED via RunContinuationRefusedError -> TransportError
REPLAY_AFTER_TERMINAL=REFUSED via RunContinuationRefusedError -> TransportError

REQUEST_ID_STABILITY=DETERMINISTIC_PER_(grant_run_id, operation_ordinal=1)
REQUEST_ENVELOPE_STABILITY=DETERMINISTIC_REDACTED_ENVELOPE
```

The consumer must derive the store `request_id` and redacted `request_envelope` deterministically from already-canonicalized non-private metadata and digests, without wall-clock or random inputs, and without embedding private CRM identifiers.

## 16. Proof requirements and one-shot consumption evidence

Consumer must produce a proof-return artifact under `proof/nw008/at-8g/` containing:

```text
PROOF_UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=<sha of this artifact merged to main>
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
SOLE_CONSUMER_UNIT=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=<sha at implementation base>
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

The future implementation proof MUST bind the exact authorization merge SHA and identify the sole consumer unit. Proof must include: modified file list (path-specific), diff summary, test run summary, and explicit confirmation that no path outside §11 was touched.

## 17. Absolute denials

```text
HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
SECRET_ACCESS=NO
SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION_AUTHORIZED=NO

REAL_PRIVATE_IDS_IN_REPO=FORBIDDEN
REAL_PRIVATE_IDS_IN_TESTS=FORBIDDEN
REAL_PRIVATE_IDS_IN_FIXTURES=FORBIDDEN
PRIVATE_BINDING_LOGGING=FORBIDDEN
PRIVATE_BINDING_PUBLICATION=FORBIDDEN
RAW_CONTACT_ID_PERSISTED=FORBIDDEN
RAW_LOCATION_ID_PERSISTED=FORBIDDEN
RAW_NOTE_BODY_PERSISTED=FORBIDDEN
RAW_PROVIDER_NOTE_ID_PERSISTED=FORBIDDEN

AT1_EXECUTION_STORE_MODIFICATION_AUTHORIZED=NO
AT1_EXECUTION_STORE_SCHEMA_MODIFICATION_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_REUSE_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_IMPLEMENTATION_AUTHORIZED=NO
LIVE_TRANSPORT_IMPLEMENTATION_AUTHORIZED=NO
NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
FIXTURE_MODIFICATION_AUTHORIZED=NO

STAGE_PATH_AUTHORIZED=NO
CONTACT_GET_LIVE_AUTHORIZED=NO
NOTE_POST_LIVE_AUTHORIZED=NO
NOTE_READBACK_LIVE_AUTHORIZED=NO

LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
BOUNDED_LIVE_NOTE_TRANSPORT_AUTHORIZATION=FROZEN
LIVE_NOTE_MUTATION_AUTHORIZATION=FROZEN
LIVE_MUTATION_AUTHORIZATION_READY=NO

PR107_TRUST_REPAIR_GRANTS_AT8G_IMPLEMENTATION=NO
AT10_EXECUTION_OR_COMPLETION_AUTHORITY_GRANTS_AT8G=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_NOTE_TRANSPORT=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_CRM_MUTATION=NO

PLANNING_DOES_NOT_AUTHORIZE_IMPLEMENTATION=YES
IMPLEMENTATION_DOES_NOT_AUTHORIZE_LIVE_MUTATION=YES
LIVE_MUTATION_REQUIRES_SEPARATE_HUMAN_GRANT=YES
```

## 18. Downstream freeze

Until AT8G is reviewed, merged, its consumer implementation is reviewed, merged, and independently reinspected under a later live-execution boundary unit:

```text
BOUNDED_LIVE_NOTE_TRANSPORT_AUTHORIZATION=FROZEN
LIVE_NOTE_MUTATION_AUTHORIZATION=FROZEN
LIVE_MUTATION_AUTHORIZATION_READY=NO
STAGE_PATH_AUTHORIZED=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_NOTE_TRANSPORT=NO
AT8G_AUTHORIZATION_GRANTS_LIVE_CRM_MUTATION=NO
```

No new live-mutation, live-transport, or bounded-live-note-transport grants are issued by this artifact or its consumer.

## 19. Unresolved contract questions (deferred, not authorized here)

The following questions are explicitly deferred to later separate governed units. AT8G does not answer them and does not authorize their implementation:

```text
Q1: Production SQLite path selection (filesystem, permissions, backup, GC) — DEFERRED
Q2: Production commitment_key provenance and rotation — DEFERRED
Q3: NOTE_PATH request_id canonical form vs. AT1 sequence's request_id form — DEFERRED beyond deterministic redacted derivation for offline tests
Q4: Cross-workflow-run garbage collection of stale grant/run rows — DEFERRED
Q5: Public projection surface tailored to NOTE_PATH (if ever required) — DEFERRED; AT8G forbids reusing AT1's projection as NOTE_PATH truth
Q6: STAGE_PATH integration — DEFERRED and out of scope
Q7: Live transport client selection and rate-limiting — DEFERRED
Q8: Secret Manager / IAM / deployment wiring — DEFERRED and explicitly denied here
Q9: Fixture amendment, if later required — DEFERRED; fixture modification default is NO
```

## 20. Stop condition

```text
STOP_ON_MERGE_OF_THIS_ARTIFACT=YES
CONSUMER_NEXT_ACTION=INDEPENDENT_VERIFICATION_OF_ARTIFACT_MERGE_TO_MAIN
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES

STOP_CODE=NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_AUTHORIZATION_READY_FOR_REVIEW
```

After human review and merge to `main`, the authorized consumer unit must independently verify that this exact artifact path is present on `origin/main` and reachable in ancestry before writing any implementation code. This artifact does not self-activate. Effectiveness is repository state, not a mutable field.

## 21. Next recommended reviewer action

1. Human review of this authorization artifact on branch `governance/nw008-at8g-note-path-at1-execution-store-integration-authorization-001`.
2. If accepted, merge to `main` via governed PR.
3. Only after that merge, open a separate implementation PR from a new branch (e.g., `implementation/nw008-at8g-note-path-at1-execution-store-integration-001`) that verifies this artifact's merge ancestry, records the exact authorization merge SHA and sole consumer unit, and applies the seam replacement described in §4/§8 against the paths listed in §11.
4. Live transport, live mutation, and STAGE_PATH remain out of scope and require separate later authorizations.

---

**Authorization artifact**: `governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md`

**Predecessor**: PR #107 merge `b2d1d2cc1d6e01ef1760a5af6b970d08fb02561a`

**Authorized consumer**: `NW008_AT8G_NOTE_PATH_AT1_EXECUTION_STORE_INTEGRATION_IMPLEMENTATION_001`

**Consumption mode**: ONE_SHOT, non-reusable, non-transferable; consumption record required

**Implementation mode**: OFFLINE_ONLY

**Authorization state at authoring**: `PROPOSED_NOT_EFFECTIVE`

**Status**: Proposed, pending human review and merge to main
