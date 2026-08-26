# NW008 AT8W30 R3 Private-Binding Provenance Trust Repair Authorization 001

## 1. Authorization identity and classification

```text
AUTHORIZATION_ID=
  NW008_AT8W30_R3_PRIVATE_BINDING_PROVENANCE_TRUST_REPAIR_AUTHORIZATION_001
UNIT=
  NW008_AT8W30_R3_PRIVATE_BINDING_PROVENANCE_TRUST_REPAIR_AUTHORIZATION_001

CLASSIFICATION=authorization
PR_CLASS=authorization
AUTHORIZATION_CLASS=implementation
MODE=IMPLEMENTATION_AUTHORIZATION_ONLY

PURPOSE=
  AUTHORIZE_ONE_BOUNDED_FUTURE_REPOSITORY_IMPLEMENTATION_THAT_REPAIRS_THE
  PRIVATE_AT8_VERIFIED_BINDING_TRUST_HANDOFF_SO_SYNTHETIC_RECORD_TRUST_IS
  DERIVED_FROM_GOVERNED_PRIVATE_PROVENANCE_RATHER_THAN_REQUIRING_PROVIDER
  ASSIGNED_IDS_THEMSELVES_TO_CARRY_A_SYNTHETIC_PREFIX

THIS_ARTIFACT_IMPLEMENTATION=NO
THIS_ARTIFACT_EXECUTES_R3=NO
THIS_ARTIFACT_CALLS_HIGHLEVEL=NO
AUTHORIZATION_ONLY=YES
```

This artifact grants narrowly bounded implementation authority only. It does
not implement the repair, invoke the production runtime, execute R3, mint a
token, read a secret payload, open SQLite, dispatch HTTP, or authorize any
external effect.

## 2. Durable failure and diagnosis prerequisites

The grant is based on the canonical `origin/main` state containing merged PR
#215 and the offline diagnosis that classified the fail-closed R3 preflight as
a private-binding provenance/configuration defect rather than a transport or
network defect.

```text
PR215_MERGED=YES
PR215_REVIEWED_HEAD=
  14f60ac4fe2a3a78e14381b308ba224ab17d3148
PR215_REVIEWED_HEAD_ANCESTRY=PASS
PR215_PROOF_ON_MAIN=YES
PR215_PROOF_BLOB_MATCH=YES

R3_RESULT=FAIL_CLOSED
R3_GATE_COMPLETE=NO
STOP_CODE=R3_PRIVATE_BINDING_PREFLIGHT_FAILED

R3_NETWORK_AUTHORIZATION_CONSUMED=NO
R3_RETRY_AUTHORIZED=NO
R3_SECOND_EXECUTION_AUTHORIZED=NO

DIAGNOSIS_RESULT=
  PRIVATE_BINDING_PROVENANCE_OR_CONFIGURATION_DEFECT

PRIVATE_BINDING_RECORD_RESOLVED=YES
TRUSTED_BINDING_SOURCE_CREATED=NO
ROOT_OWNED_DELIVERY_REFERENCE_CREATED=NO
ROOT_OWNED_CAPABILITY_ISSUED=NO

PRIMARY_FAIL_BRANCH_EXCEPTION_CLASS=BindingError
PRIMARY_FAIL_BRANCH_EXCEPTION_MESSAGE=
  location_id test capability value must be synthetic

PRIVATE_BINDING_LOCATION_SYNTHETIC_PREFIX=NO
PRIVATE_BINDING_CONTACT_SYNTHETIC_PREFIX=NO

SYNTHETIC_CONTROL_PATH=PASS
```

If any statement in this prerequisite block is false, this authorization is
invalid and the future implementation must stop without repository mutation:

```text
STOP_CODE=PR215_OR_DIAGNOSIS_DURABLE_PREREQUISITE_FAILED
```

## 3. Authorization objective

Authorize a minimal implementation repair so the private AT8 verified-binding
handoff derives "synthetic record" trust from governed private provenance
rather than requiring exact provider-assigned IDs themselves to have a
`synthetic-` prefix.

```text
DO_NOT_MODIFY_PROVIDER_IDS=YES
DO_NOT_WEAKEN_TEST_ONLY_SYNTHETIC_PREFIX_VALIDATION=YES

RAW_PROVIDER_IDS_ALONE_CANNOT_MINT_TRUST=YES

OPAQUE_PROVIDER_IDS_ACCEPTED_ONLY_WITH_VERIFIED_PRIVATE_PROVENANCE=YES
```

The future implementation must not rewrite, hash-publish, log, or commit raw
provider IDs. Provider IDs remain opaque private binding values.

## 4. Authorized future implementation paths

Only these paths may be changed by the future implementation:

```text
AUTHORIZED_FUTURE_PATHS=
  src/integrations/ghl/highlevel_rest/note_path.py|
  tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md
```

Any additional path requires an immediate stop and separate authorization.

```text
AUTHORIZED_PATH_COUNT_MAX=3
```

## 5. Blocked paths and blocked effects

The following paths and path classes are not authorized by default:

```text
BLOCKED_PATHS=
  src/integrations/ghl/highlevel_rest/live_note_runtime.py|
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
  governance/authorizations/**|
  private allowlist identifiers
```

Blocked effect classes under this grant:

```text
BLOCKED_EFFECTS=
  R3_EXECUTION|
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
  PRIVATE_IDENTIFIER_PUBLICATION
```

## 6. Required implementation semantics

### 6.1 Preserve existing test-only synthetic-prefix guards

```text
TEST_SYNTHETIC_PREFIX_GUARD_UNCHANGED=YES
```

Existing test-only factories and synthetic-shaped test capability paths must
continue to require `synthetic-` prefixes for location and contact identifiers.
This grant does not authorize weakening those guards.

### 6.2 Preserve existing trust boundaries

```text
UNTRUSTED_STRUCTURAL_SOURCE_BLOCKED=YES
CALLER_FORGED_CAPABILITY_BLOCKED=YES
RAW_PRIVATE_BINDING_DIRECT_HANDOFF_BLOCKED=YES
PUBLIC_BOOLEAN_PROMOTION_BLOCKED=YES
SERIALIZED_CAPABILITY_CANNOT_RESTORE_AUTHORITY=YES
PROCESS_LOCAL_TRUST_REGISTRY_REQUIRED=YES
```

### 6.3 Add private provenance-aware semantics

```text
PRIVATE_VERIFIED_BINDING_REQUIRES_TRUSTED_PROVENANCE=YES
PRIVATE_VERIFIED_BINDING_MAY_USE_OPAQUE_PROVIDER_IDS=YES
PRIVATE_VERIFIED_BINDING_SYNTHETIC_STATUS_COMES_FROM_PROVENANCE=YES
ORDINARY_CALLER_CANNOT_ASSERT_SYNTHETIC_PROVENANCE=YES
```

Required security invariant:

```text
RAW_PROVIDER_IDS_ALONE_CANNOT_MINT_TRUST=YES
```

Required production-private invariant:

```text
OPAQUE_PROVIDER_IDS_ACCEPTED_ONLY_WITH_VERIFIED_PRIVATE_PROVENANCE=YES
```

Minimum provenance gates for opaque provider IDs under the private AT8 handoff:

```text
REQUIRED_PRIVATE_PROVENANCE_ASSERTIONS=
  SYNTHETIC_CONTACT_BOUND=YES|
  PRIVATE_ALLOWLIST_COMPLETE=YES|
  RELATIONSHIP_VERIFIED=YES|
  TRUSTED_PRIVATE_AT8_ORIGIN|
  CORRECT_SOURCE_EXECUTION_UNIT|
  CORRECT_SOURCE_PROOF_MERGE_SHA|
  PROCESS_ISSUED_ROOT_OWNED_DELIVERY_REFERENCE
```

Opaque provider IDs without verified private provenance must fail closed.

## 7. Required future test matrix

All future implementation tests must remain offline and synthetic-only for
public fixtures. Do not use private CRM identifiers in committed tests or
proof.

```text
REQUIRED_TEST_MATRIX=
  1_SYNTHETIC_PREFIXED_IDS_THROUGH_EXISTING_TEST_FACTORY=PASS|
  2_OPAQUE_IDS_WITHOUT_TRUSTED_PROVENANCE=FAIL_CLOSED|
  3_OPAQUE_IDS_WITH_VALID_ROOT_OWNED_PRIVATE_PROVENANCE=PASS|
  4_OPAQUE_IDS_WITH_SYNTHETIC_FALSE=FAIL_CLOSED|
  5_OPAQUE_IDS_WITH_ALLOWLIST_COMPLETE_FALSE=FAIL_CLOSED|
  6_OPAQUE_IDS_WITH_RELATIONSHIP_VERIFIED_FALSE=FAIL_CLOSED|
  7_WRONG_SOURCE_EXECUTION_UNIT=FAIL_CLOSED|
  8_WRONG_SOURCE_PROOF_SHA=FAIL_CLOSED|
  9_WRONG_CONSUMER_AUTHORIZATION_IDENTITY=FAIL_CLOSED|
  10_WRONG_CONSUMER_WORKFLOW_RUN=FAIL_CLOSED|
  11_FORGED_STRUCTURAL_TRUSTED_SOURCE=FAIL_CLOSED|
  12_SERIALIZED_OR_RECONSTRUCTED_CAPABILITY_NO_AUTHORITY_RESTORE=FAIL_CLOSED

ALL_TESTS_OFFLINE=YES
PRIVATE_CRM_IDENTIFIERS_IN_TESTS=NO
PRIVATE_CRM_IDENTIFIERS_IN_PROOF=NO
```

Focused deterministic tests are the only authorized verification surface under
this grant.

## 8. Authorization limits

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
R3_RETRY_AUTHORIZED=NO
R3_SECOND_EXECUTION_AUTHORIZED=NO
R4_AUTHORIZED=NO
NOTE_WRITE_AUTHORIZED=NO
STAGE_TRANSITION_AUTHORIZED=NO
```

## 9. Authorization semantics and consumption

```text
AUTHORIZED_CONSUMER_CLASS=implementation
ONE_SHOT_IMPLEMENTATION_AUTHORITY=YES
ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
FAILURE_RESTORES_AUTHORITY=NO

AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO

AUTHORIZATION_STATE_BEFORE_IMPLEMENTATION=
  AVAILABLE_IF_MERGED_AND_VERIFIED

AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_AUTHORIZED_REPOSITORY_IMPLEMENTATION_MUTATION_ATTEMPT

AUTHORIZATION_STATE_ON_FIRST_AUTHORIZED_IMPLEMENTATION_MUTATION_ATTEMPT=
  CONSUMED
AUTHORIZATION_STATE_AFTER_FIRST_AUTHORIZED_IMPLEMENTATION_MUTATION_ATTEMPT=
  CONSUMED
```

This authorization may be consumed only by the exact bounded implementation
PR after human merge of this authorization artifact to `main`.

```text
AUTHORIZED_FUTURE_CONSUMER_UNIT=
  NW008_AT8W30_R3_PRIVATE_BINDING_PROVENANCE_TRUST_REPAIR_IMPLEMENTATION_001
```

## 10. Proof requirements for the future implementation

The future implementation must create only:

```text
proof/nw008/at-8w30/
  nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md
```

The proof must record counters, booleans, and stop codes only. It must not
include raw contact id, raw location id, raw HighLevel payload, secret payload,
token material, token fragment, source principal, or private identifier hashes.

Required proof assertions:

```text
TEST_SYNTHETIC_PREFIX_GUARD_UNCHANGED=YES
OPAQUE_PROVIDER_IDS_ACCEPTED_ONLY_WITH_VERIFIED_PRIVATE_PROVENANCE=YES
RAW_PROVIDER_IDS_ALONE_CANNOT_MINT_TRUST=YES

HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
SECRET_PAYLOAD_READS=0
TOKEN_MINTS=0
SQLITE_OPENS=0
CRM_MUTATIONS=0

R3_EXECUTION_PERFORMED=NO
R3_EXECUTION_AUTHORIZED=NO
```

## 11. Explicit non-authorizations

This grant does not authorize:

```text
NOT_AUTHORIZED=
  R3_EXECUTION|
  R3_RETRY|
  R3_SECOND_EXECUTION|
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
  WEAKENING_OF_TEST_ONLY_SYNTHETIC_PREFIX_GUARDS|
  ACCEPTANCE_OF_RAW_PROVIDER_IDS_WITHOUT_VERIFIED_PRIVATE_PROVENANCE
```

## 12. Stop codes

```text
STOP_IF_PREREQUISITES_FAIL=
  PR215_OR_DIAGNOSIS_DURABLE_PREREQUISITE_FAILED

STOP_IF_SCOPE_EXCEEDED=
  UNAUTHORIZED_PATH_OR_EFFECT

STOP_IF_SECURITY_INVARIANT_VIOLATED=
  RAW_PROVIDER_IDS_ALONE_CAN_MINT_TRUST|
  OPAQUE_PROVIDER_IDS_ACCEPTED_WITHOUT_VERIFIED_PRIVATE_PROVENANCE|
  TEST_SYNTHETIC_PREFIX_GUARD_WEAKENED
```

## 13. Final disposition of this authorization artifact

```text
AUTHORIZATION_CLASS=implementation
AUTHORIZED_PATHS=
  src/integrations/ghl/highlevel_rest/note_path.py|
  tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md

BLOCKED_PATHS=
  live_note_runtime.py|
  live_note_transport.py|
  live_note_http_client.py|
  credential providers|
  At1ExecutionStore|
  contracts|
  requirements|
  workflows|
  deploy|
  infra|
  IAM|
  Secret Manager resources|
  private allowlist identifiers

TEST_SYNTHETIC_PREFIX_GUARD_UNCHANGED=YES
OPAQUE_PROVIDER_IDS_ACCEPTED_ONLY_WITH_VERIFIED_PRIVATE_PROVENANCE=YES
RAW_PROVIDER_IDS_ALONE_CANNOT_MINT_TRUST=YES

R3_EXECUTION_AUTHORIZED=NO
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0

NEXT=
  After human merge of this authorization, construct a separate one-shot
  implementation packet for
  NW008_AT8W30_R3_PRIVATE_BINDING_PROVENANCE_TRUST_REPAIR_IMPLEMENTATION_001.
  Do not retry R3 under this grant.
```
