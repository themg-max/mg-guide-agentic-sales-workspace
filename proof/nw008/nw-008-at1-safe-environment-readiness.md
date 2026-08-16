# NW-008 — AT-1 Safe Environment Readiness

## Scope and lane

```text
WORK_ITEM=NW-008
TRACK=AT-1
LANE=SAFE_ENVIRONMENT_READINESS
BRANCH=impl/nw008-at1-safe-environment-readiness
IMPLEMENTATION_SUBJECT_SHA=8c18a10faff28b658638da9e0d9752c8710e0e23
IMPLEMENTATION_HARDENING_SHA=998564cdfac6c24d5a414289798979a7f6220082
TRACK_B_FINAL_REVIEW_HEAD=835d86f64bd75b4983cf5e92f25b5fc7da439cc0
```

This lane proves the AT-1 environment is safe for the bounded operation contract
and that all public-repo evidence remains synthetic and non-authoritative. It does
not grant execution authority and does not perform AT-1 mutation or live GHL
calls.

## Required evidence

```text
ISOLATED_GHL_TEST_LOCATION=YES
SYNTHETIC_CONTACT_READY=YES
SYNTHETIC_OPPORTUNITY_READY=YES
EXPECTED_INITIAL_STAGE_VERIFIED=YES
AUTHORIZED_FINAL_STAGE_VERIFIED=YES
REQUIRED_GHL_OPERATIONS_VERIFIED=YES
PRIVATE_BINDING_PUBLICATION=NO
ENVIRONMENT_READY=YES
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Deterministic readiness basis

### 1. Isolated / test GHL location

The bounded executor contract is deliberately limited to a synthetic location
identifier, never a production GHL location or live credentialed target:

```text
location_id=synthetic-location-at1
contact_id=synthetic-contact-at1
opportunity_id=synthetic-opportunity-at1
```

The fixture policy requires:

```text
source=synthetic_only
network_enabled=false
ghl_live_client=false
firestore_client=false
```

This proves the AT-1 lane is operationally isolated from any production GHL,
Firestore, or network-backed runtime. No live GHL call is performed in this
Track A readiness lane.

### 2. Synthetic contact and opportunity

The synthetic engagement objects are the only public identifiers used in the
proof chain. They are explicit fixtures, not live CRM records:

```text
contact_id=synthetic-contact-at1
opportunity_id=synthetic-opportunity-at1
```

The required contact/opportunity reads are bounded to those exact IDs and must
match the deterministic fixture bindings. No search, list, or pagination method is
part of the readiness contract.

### 3. Initial stage and final stage evidence

The expected stage transition is fixed and synthetic:

```text
expected_initial_stage_id=synthetic-stage-initial
authorized_final_stage_id=synthetic-stage-final
```

The AT-1 contract rejects an initial-stage mismatch before any write and refuses a
final-stage update unless the exact authorized stage is supplied. This keeps the
state transition within the same bounded proof surface as Track B.

### 4. Exact GHL MCP operation availability

The exact allowed GHL operation set remains identical to Track B and is limited to
what the deterministic fixture transport authorizes:

```text
ORDER=get-contact,get-opportunity,create-note,get-note,update-opportunity,get-opportunity
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RAW_REST=YES
NO_ALTERNATE_OPERATION=YES
```

The operation surface is not expanded for Track A readiness. The exact operation
order and argument matching are verified via the fixture-only transport contract
and the deterministic executor proof.

### 5. Credential scope and target isolation

The readiness proof explicitly excludes all external runtime authority:

```text
CREDENTIAL_SCOPE=READ_WRITE_BOUND_TO_SYNTHETIC_AT1_FIXTURE_ONLY
TARGET_ISOLATION=YES
PRIVATE_BINDING_VALUES_COMMITTED=NO
```

This lane does not change IAM, deployment, secrets, or repository policy. It does
not publish private IDs or credential scopes to the public repo. All fixture
values remain public-safe synthetic placeholders.

### 6. Private IDs excluded from the public repo

The repository proof intentionally contains no customer, production, or live GHL
ID values. The public evidence uses only deterministic synthetic values, and the
AT-1 contract is exact about expected fields:

```text
location_id
contact_id
opportunity_id
expected_initial_stage_id
authorized_final_stage_id
expected_note_content_or_fingerprint
```

Any private binding values remain out of scope for this public repository lane.

### 7. Read/write caps remain identical to Track B

The AT-1 read/write caps are preserved without widening the execution surface:

```text
NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
FURTHER_TRANSPORT_CALLS_AUTHORIZED=NO_AFTER_TERMINAL_FAILURE
REFUSE_BEFORE_TRANSPORT=YES
STOP_AND_PRESERVE_PROOF=YES_ON_WRITE_READBACK_FAILURE
```

The safety posture remains fail-closed. No additional runtime capability is added
or exercised in this readiness lane.

## Readiness disposition

This Track A lane proves that the environment is safe for a bounded AT-1
readiness assessment, but not that AT-1 is authorized to run.

```text
READINESS_RESULT=SAFE_ENVIRONMENT_READY_FOR_REVIEW_ONLY
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
EXECUTION_BLOCKED=LIVE_MUTATION;
PRODUCTION_GHL;
FIRESTORE_MUTATION;
RAW_GHL_REST_FALLBACK;
ADDITIONAL_SEARCH_LIST_PAGINATION;
RETRY_LOGIC;
COMPENSATING_MUTATION;
IAM_SECRETS_DEPLOYMENT_CHANGE;
PRIVATE_ID_PUBLICATION
```

## Retrieval / indexing note

The repository's current repo_source_review_search surface remains unable to
surface NW-008 / PR64 / Track A / Track B records. This is recorded as a later
retrieval/indexing improvement, not a blocker for this safe-environment
readiness proof.

## STOP

```text
STOP_CODE=NW008_AT1_SAFE_ENVIRONMENT_READINESS_PROVED_STOP
```
