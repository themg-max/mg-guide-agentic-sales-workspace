# NW008 AT8W30 R3 Private-Owner Lease Ingress Repair Authorization 001

## 1. Authorization identity and classification

```text
AUTHORIZATION_ID=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_AUTHORIZATION_001
UNIT=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_AUTHORIZATION_001

CLASSIFICATION=authorization
PR_CLASS=authorization
AUTHORIZATION_CLASS=implementation
MODE=IMPLEMENTATION_AUTHORIZATION_ONLY

ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
HUMAN_GOVERNANCE_RETAINS_MERGE_AUTHORITY=YES

PURPOSE=
  AUTHORIZE_ONE_BOUNDED_FUTURE_REPOSITORY_IMPLEMENTATION_THAT_REPAIRS_THE
  PRIVATE_OWNER_LEASE_INGRESS_PATH_SO_THE_PUBLIC_CONSUMER_ACCEPTS_A
  PREEXISTING_OPAQUE_PRIVATE_BINDING_REFERENCE_MATERIALIZED_BY_THE_PRIVATE
  OWNER_INSTEAD_OF_MATERIALIZING_OR_MINTING_AUTHORITY_IN_PUBLIC_CODE

THIS_ARTIFACT_IMPLEMENTATION=NO
THIS_ARTIFACT_EXECUTES_R3=NO
THIS_ARTIFACT_CALLS_HIGHLEVEL=NO
THIS_ARTIFACT_MUTATES_PR217=NO
AUTHORIZATION_ONLY=YES
```

This artifact grants narrowly bounded future implementation authority only. It
does not implement the repair, mutate PR #217, invoke the production runtime,
execute R3, mint a token, read a secret payload, open SQLite, dispatch HTTP, or
authorize any external effect.

## 2. Durable prerequisites

This grant is based on the canonical `origin/main` state containing the merged
public attestation for the private-owner lease ingress designation.

```text
BOUND_PRIVATE_DESIGNATION=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_DESIGNATION_001
BOUND_PUBLIC_ATTESTATION=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_ATTESTATION_001

BOUND_ATTESTATION_PR=221
BOUND_ATTESTATION_REVIEWED_HEAD=
  805ea831b8d7afd9935eb72957c7eeb46fbd0d47
BOUND_ATTESTATION_MERGE_COMMIT=
  98866e21befc8a6e0ad3b76a823d80a7b473f795

PR221_STATE=MERGED
PR221_REVIEWED_HEAD_IN_MAIN_LINEAGE=YES
ATTESTATION_PRESENT_ON_MAIN=YES
ATTESTATION_PATH_ON_MAIN=
  docs/nw008/nw-008-at8w30-r3-private-owner-lease-ingress-attestation-001.md

PR220_STATE=SUPERSEDED
PR220_MERGE_AUTHORIZED=NO
```

The superseded planning PR #220 must not be merged. Human governance may close
PR #220 as superseded after verifying PR #221 is merged. This authorization
grants no authority over PR #220 beyond the prohibition on merging it.

If any statement in this prerequisite block is false, this authorization is
invalid and the future implementation must stop without repository mutation:

```text
STOP_CODE=PR221_ATTESTATION_DURABLE_PREREQUISITE_FAILED
```

## 3. Frozen public target boundary

```text
TARGET_PR=217
TARGET_PRE_REPAIR_HEAD=
  16ae6df3b68a3a6dcf75e572a19a31f7db3b7285

PR217_STATE_AT_AUTHORIZATION=OPEN
PR217_FROZEN=YES
THIS_AUTHORIZATION_PR_MUTATES_PR217=NO
PR217_MUTATION_PERFORMED_BY_THIS_AUTHORIZATION_PR=NO

FUTURE_BOUNDED_PR217_MUTATION_AUTHORIZED_AFTER_HUMAN_MERGE=YES
FUTURE_PR217_MUTATION_LIMITED_TO_AUTHORIZED_PATHS=YES
```

PR #217 is frozen at the pre-repair head recorded above. This authorization
artifact does not mutate PR #217. The designated future implementation unit
must re-verify that the PR #217 head still equals
`16ae6df3b68a3a6dcf75e572a19a31f7db3b7285` before its first authorized
repository mutation. If the head has moved, it must stop:

```text
STOP_CODE=PR217_HEAD_MOVED
```

## 4. Private locator non-publication

```text
PRIVATE_LOCATORS_PUBLICATION=FORBIDDEN
PRIVATE_VALUES_PUBLICATION=FORBIDDEN
PRIVATE_OWNER_SCOPE_DISCLOSED_PUBLICLY=NO
PRIVATE_IDENTIFIER_HASH_PUBLICATION=FORBIDDEN
```

No private locator, private owner path, private module name, private scope,
private allowlist identifier, raw provider ID, raw payload, secret payload,
token material, token fragment, source principal, or private identifier hash
may appear in any authorized future artifact, test fixture, proof, log, or
commit message. Public artifacts may reference the private owner only through
its approved sanitized designation identity.

## 5. Authorization objective

Authorize a minimal implementation repair so that the private owner remains the
sole authority source for the lease and the public consumer only ingests a
pre-existing opaque reference.

```text
PRIVATE_OWNER_REMAINS_AUTHORITY_SOURCE=YES

PUBLIC_NOTE_PATH_IS_AUTHORITY_SOURCE=NO
PUBLIC_RUNTIME_IS_AUTHORITY_SOURCE=NO

PRIVATE_OWNER_MATERIALIZES_OPAQUE_REFERENCE=YES
PUBLIC_CONSUMER_ACCEPTS_PREEXISTING_REFERENCE=YES

PUBLIC_PRODUCTION_LEASE_MATERIALIZATION=FORBIDDEN
```

The public boundary is an ingress only. Public code may accept, validate, and
atomically consume an opaque reference that the private owner already
materialized. Public code must never create, mint, reconstruct, forge, copy,
serialize, or re-derive that reference or its authority in production.

## 6. Authorized future implementation paths

Only these paths may be changed by the future implementation:

```text
AUTHORIZED_FUTURE_PATHS=
  src/integrations/ghl/highlevel_rest/live_note_runtime.py|
  src/integrations/ghl/highlevel_rest/note_path.py|
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py|
  tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-owner-lease-ingress-repair-consumption-001.md

AUTHORIZED_PATH_COUNT_MAX=6
```

Any additional path requires an immediate stop and separate authorization.

```text
STOP_CODE=UNAUTHORIZED_PATH_OR_EFFECT
```

## 7. Blocked paths and blocked effects

```text
BLOCKED_PATHS=
  src/integrations/ghl/highlevel_rest/live_note_transport.py|
  src/integrations/ghl/highlevel_rest/live_note_http_client.py|
  src/integrations/ghl/highlevel_rest/live_note_credential_provider.py|
  src/integrations/ghl/at1_execution_store.py|
  src/integrations/ghl/at1_commitment_key_provider.py|
  contracts/**|
  requirements*|
  pyproject.toml|
  .github/workflows/**|
  deploy/**|
  infra/**|
  docs/**|
  governance/**|
  private allowlist identifiers|
  private owner modules or locators
```

```text
BLOCKED_EFFECTS=
  PR217_MUTATION_BEFORE_AUTHORIZATION_MERGE|
  PR217_MUTATION_OUTSIDE_AUTHORIZED_PATHS|
  UNBOUNDED_PR217_MUTATION|
  PR220_MERGE|
  R3_EXECUTION|
  R4_EXECUTION|
  HIGHLEVEL_CALL|
  HTTP_DISPATCH|
  TOKEN_MINT|
  SECRET_PAYLOAD_READ|
  SQLITE_OPEN|
  SQLITE_CREATE|
  CRM_MUTATION|
  IAM_MUTATION|
  DEPLOYMENT|
  PRODUCTION_RUNTIME_ASSEMBLY|
  PRIVATE_IDENTIFIER_PUBLICATION|
  PRIVATE_LOCATOR_PUBLICATION
```

## 8. Required implementation contract

### 8.1 Authority source

```text
PRIVATE_OWNER_REMAINS_AUTHORITY_SOURCE=YES
PUBLIC_NOTE_PATH_IS_AUTHORITY_SOURCE=NO
PUBLIC_RUNTIME_IS_AUTHORITY_SOURCE=NO
```

### 8.2 Reference materialization and ingress

```text
PRIVATE_OWNER_MATERIALIZES_OPAQUE_REFERENCE=YES
PUBLIC_CONSUMER_ACCEPTS_PREEXISTING_REFERENCE=YES
PUBLIC_PRODUCTION_LEASE_MATERIALIZATION=FORBIDDEN

BOUNDARY_OBJECT=
  OPAQUE_SAFE_PRIVATE_BINDING_REFERENCE
REFERENCE_SERIALIZABLE=NO
REFERENCE_COPYABLE=NO
```

### 8.3 Provenance and identifier trust

```text
RAW_PROVIDER_IDS_ALONE_CAN_MINT_AUTHORITY=NO
OPAQUE_PROVIDER_IDS_AFTER_VERIFIED_PRIVATE_PROVENANCE=YES
```

Opaque provider IDs are acceptable only after verified private provenance has
already been established by the private owner. Raw provider IDs alone must
never mint authority. Existing test-only synthetic-prefix guards must not be
weakened.

```text
TEST_SYNTHETIC_PREFIX_GUARD_UNCHANGED=YES
```

### 8.4 Process and selection boundaries

```text
SAME_PROCESS_ONLY=YES
CROSS_PROCESS_HANDOFF_AUTHORIZED=NO

ENVIRONMENT_SELECTED_PRIVATE_OWNER=FORBIDDEN
CALLER_SELECTED_PRIVATE_OWNER=FORBIDDEN
```

The private owner must not be selected by environment variable, configuration
value, caller argument, import string, plugin registry, or any other
late-bound indirection.

### 8.5 Capability boundary integrity

```text
FINISHED_CAPABILITY_AS_BOUNDARY_SUBSTITUTE=FORBIDDEN
```

A finished or already-issued capability must not be substituted for the
boundary object. The ingress boundary accepts only the opaque pre-existing
private binding reference.

### 8.6 Consumption ordering and fail-closed semantics

```text
ATOMIC_CONSUME_BEFORE_CAPABILITY_ISSUANCE=YES

SECOND_CONSUMPTION=FAIL_CLOSED
REPLAY=FAIL_CLOSED
FORGED_REFERENCE=FAIL_CLOSED
```

The reference must be atomically consumed before any capability is issued. A
failed issuance after consumption must not restore the reference.

## 9. Required future test matrix

```text
REQUIRED_TEST_MATRIX=
  1_PREEXISTING_OPAQUE_REFERENCE_INGRESS=PASS|
  2_PUBLIC_PRODUCTION_LEASE_MATERIALIZATION_ATTEMPT=FAIL_CLOSED|
  3_SECOND_CONSUMPTION_OF_SAME_REFERENCE=FAIL_CLOSED|
  4_REPLAYED_REFERENCE=FAIL_CLOSED|
  5_FORGED_REFERENCE=FAIL_CLOSED|
  6_RAW_PROVIDER_IDS_WITHOUT_VERIFIED_PRIVATE_PROVENANCE=FAIL_CLOSED|
  7_OPAQUE_PROVIDER_IDS_AFTER_VERIFIED_PRIVATE_PROVENANCE=PASS|
  8_CROSS_PROCESS_HANDOFF_ATTEMPT=FAIL_CLOSED|
  9_ENVIRONMENT_SELECTED_PRIVATE_OWNER_ATTEMPT=FAIL_CLOSED|
  10_CALLER_SELECTED_PRIVATE_OWNER_ATTEMPT=FAIL_CLOSED|
  11_FINISHED_CAPABILITY_AS_BOUNDARY_SUBSTITUTE=FAIL_CLOSED|
  12_CAPABILITY_ISSUANCE_FAILURE_DOES_NOT_RESTORE_REFERENCE=FAIL_CLOSED|
  13_EXISTING_TEST_ONLY_SYNTHETIC_PREFIX_GUARDS=PASS

ALL_TESTS_OFFLINE=YES
PRIVATE_CRM_IDENTIFIERS_IN_TESTS=NO
PRIVATE_CRM_IDENTIFIERS_IN_PROOF=NO
PRIVATE_LOCATORS_IN_TESTS=NO
PRIVATE_LOCATORS_IN_PROOF=NO
```

Focused deterministic offline tests are the only authorized verification
surface under this grant.

## 10. Authorization limits

```text
HIGHLEVEL_CALLS_MAX=0
HTTP_REQUEST_DISPATCHES_MAX=0

SECRET_PAYLOAD_READS_MAX=0
TOKEN_MINTS_MAX=0

SQLITE_OPENS_MAX=0
SQLITE_CREATES_MAX=0

CRM_MUTATIONS_MAX=0
IAM_MUTATIONS_MAX=0
DEPLOYMENTS_MAX=0

PRODUCTION_RUNTIME_ASSEMBLY_MAX=0

R3_EXECUTION_AUTHORIZED=NO
R4_AUTHORIZED=NO
NOTE_WRITE_AUTHORIZED=NO
STAGE_TRANSITION_AUTHORIZED=NO
```

## 11. Authorization lifecycle and consumption

```text
AUTHORIZED_CONSUMER_CLASS=implementation
ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
FAILURE_RESTORES_AUTHORITY=NO

AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_REQUIRED=YES

AUTHORIZATION_STATE_BEFORE_IMPLEMENTATION=
  AVAILABLE_IF_MERGED_AND_VERIFIED

AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_AUTHORIZED_REPOSITORY_MUTATION_ATTEMPT_BY_THE_DESIGNATED_IMPLEMENTATION_UNIT

AUTHORIZATION_STATE_ON_FIRST_AUTHORIZED_REPOSITORY_MUTATION_ATTEMPT=
  CONSUMED
AUTHORIZATION_STATE_AFTER_FIRST_AUTHORIZED_REPOSITORY_MUTATION_ATTEMPT=
  CONSUMED
```

Authority is consumed at the first authorized repository mutation attempt,
whether or not that attempt succeeds. A failed, aborted, reverted, or
abandoned implementation does not restore authority; any subsequent attempt
requires a new authorization artifact.

This authorization may be consumed only by the exact bounded implementation PR
after human merge of this authorization artifact to `main`.

```text
AUTHORIZED_FUTURE_CONSUMER_UNIT=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_IMPLEMENTATION_001
```

## 12. Proof and consumption-record requirements

The future implementation must create only:

```text
proof/nw008/at-8w30/
  nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md
proof/nw008/at-8w30/
  nw008-at8w30-r3-private-owner-lease-ingress-repair-consumption-001.md
```

Proof and consumption artifacts must record counters, booleans, identities, and
stop codes only.

Required proof assertions:

```text
PRIVATE_OWNER_REMAINS_AUTHORITY_SOURCE=YES
PUBLIC_NOTE_PATH_IS_AUTHORITY_SOURCE=NO
PUBLIC_RUNTIME_IS_AUTHORITY_SOURCE=NO
PUBLIC_PRODUCTION_LEASE_MATERIALIZATION=FORBIDDEN
PUBLIC_CONSUMER_ACCEPTS_PREEXISTING_REFERENCE=YES
ATOMIC_CONSUME_BEFORE_CAPABILITY_ISSUANCE=YES
SECOND_CONSUMPTION=FAIL_CLOSED
REPLAY=FAIL_CLOSED
FORGED_REFERENCE=FAIL_CLOSED
SAME_PROCESS_ONLY=YES
PRIVATE_LOCATORS_PUBLISHED=NO

HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
SECRET_PAYLOAD_READS=0
TOKEN_MINTS=0
SQLITE_OPENS=0
SQLITE_CREATES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

AUTHORIZED_PR217_MUTATION_PERFORMED=YES
PR217_MUTATION_OUTSIDE_AUTHORIZED_SCOPE=NO
CHANGED_PATH_COUNT_WITHIN_LIMIT=YES
R3_EXECUTION_PERFORMED=NO
R3_EXECUTION_AUTHORIZED=NO
R4_AUTHORIZED=NO
```

Required consumption-record assertions:

```text
AUTHORIZATION_ID=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_AUTHORIZATION_001
AUTHORIZATION_MERGE_COMMIT=<recorded_at_consumption>
CONSUMING_UNIT=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_IMPLEMENTATION_001
CONSUMPTION_TRIGGER_OBSERVED=
  FIRST_AUTHORIZED_REPOSITORY_MUTATION_ATTEMPT
AUTHORIZATION_STATE_AFTER=CONSUMED
REUSABLE=NO
TRANSFERABLE=NO
FAILURE_RESTORES_AUTHORITY=NO
PR217_HEAD_REVERIFIED=
  16ae6df3b68a3a6dcf75e572a19a31f7db3b7285
CHANGED_PATH_COUNT_WITHIN_LIMIT=YES
```

## 13. Explicit non-authorizations

```text
NOT_AUTHORIZED=
  PR217_MUTATION_BEFORE_AUTHORIZATION_MERGE|
  PR217_MUTATION_OUTSIDE_AUTHORIZED_FUTURE_PATHS|
  UNBOUNDED_PR217_MUTATION|
  PR220_MERGE|
  R3_EXECUTION|
  R3_RETRY|
  R4|
  NOTE_WRITE|
  STAGE_TRANSITION|
  CRM_MUTATION|
  IAM_MUTATION|
  DEPLOYMENT|
  SECRET_PAYLOAD_READ|
  TOKEN_MINT|
  SQLITE_OPEN_OR_CREATE|
  PRODUCTION_RUNTIME_ASSEMBLY|
  TRANSPORT_ROUTE_CHANGE|
  CONTRACT_CHANGE|
  PRIVATE_ALLOWLIST_IDENTIFIER_MUTATION|
  PRIVATE_LOCATOR_PUBLICATION|
  CROSS_PROCESS_HANDOFF|
  ENVIRONMENT_SELECTED_PRIVATE_OWNER|
  CALLER_SELECTED_PRIVATE_OWNER|
  PUBLIC_PRODUCTION_LEASE_MATERIALIZATION|
  FINISHED_CAPABILITY_AS_BOUNDARY_SUBSTITUTE|
  WEAKENING_OF_TEST_ONLY_SYNTHETIC_PREFIX_GUARDS|
  ACCEPTANCE_OF_RAW_PROVIDER_IDS_WITHOUT_VERIFIED_PRIVATE_PROVENANCE
```

## 14. Stop codes

```text
STOP_IF_PREREQUISITES_FAIL=
  PR221_ATTESTATION_DURABLE_PREREQUISITE_FAILED

STOP_IF_TARGET_MOVED=
  PR217_HEAD_MOVED

STOP_IF_SCOPE_EXCEEDED=
  UNAUTHORIZED_PATH_OR_EFFECT

STOP_IF_SECURITY_INVARIANT_VIOLATED=
  PUBLIC_RUNTIME_BECAME_AUTHORITY_SOURCE|
  PUBLIC_PRODUCTION_LEASE_MATERIALIZATION_INTRODUCED|
  RAW_PROVIDER_IDS_ALONE_CAN_MINT_AUTHORITY|
  CAPABILITY_ISSUED_BEFORE_ATOMIC_CONSUME|
  REPLAY_OR_SECOND_CONSUMPTION_SUCCEEDED|
  FORGED_REFERENCE_ACCEPTED|
  CROSS_PROCESS_HANDOFF_INTRODUCED|
  ENVIRONMENT_OR_CALLER_SELECTED_PRIVATE_OWNER_INTRODUCED|
  FINISHED_CAPABILITY_SUBSTITUTED_FOR_BOUNDARY_OBJECT|
  PRIVATE_LOCATOR_PUBLISHED
```

## 15. Final disposition of this authorization artifact

```text
AUTHORIZATION_ID=
  NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_REPAIR_AUTHORIZATION_001
AUTHORIZATION_CLASS=implementation
PR_CLASS=authorization

CHANGED_PATH_COUNT=1
CHANGED_PATH=
  governance/authorizations/nw008-at8w30-r3-private-owner-lease-ingress-repair-authorization-001.md

ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
FAILURE_RESTORES_AUTHORITY=NO

PRIVATE_LOCATORS_PUBLICATION=FORBIDDEN
PRIVATE_LOCATORS_PUBLISHED=NO

TARGET_PR=217
TARGET_PRE_REPAIR_HEAD=
  16ae6df3b68a3a6dcf75e572a19a31f7db3b7285
PR217_MUTATION_PERFORMED_BY_THIS_AUTHORIZATION_PR=NO

R3_EXECUTION_AUTHORIZED=NO
R3_EXECUTION_PERFORMED=NO
R4_AUTHORIZED=NO
EXTERNAL_EFFECTS=0

AUTO_MERGE=NO
HUMAN_GOVERNANCE_RETAINS_MERGE_AUTHORITY=YES
```
