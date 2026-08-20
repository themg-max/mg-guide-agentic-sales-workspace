# NW-008 AT-8F-R1 — HighLevel REST Private AT8 Capability-Handoff Trust Boundary Repair Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8F_R1_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=governance/nw008-at8f-r1-private-at8-handoff-trust-boundary-repair-auth-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8f-r1-ghl-rest-private-at8-capability-handoff-trust-boundary-repair-authorization-001.md

DEFECTIVE_SOURCE_PR=105
DEFECTIVE_SOURCE_HEAD=6f7f92daa70d3969d075ccc48c973f0b9dcd574e
DEFECTIVE_SOURCE_MERGE_SHA=01741618155a509a0b3696156309cc457416173a
DEFECTIVE_SOURCE_MERGE_VERIFIED=YES

SOURCE_ORIGINAL_AUTHORIZATION_PR=104
SOURCE_ORIGINAL_AUTHORIZATION_MERGE_SHA=c10435bd8b90de39250b695a985ab6831fb2c881

BASE_REF=origin/main
BASE_SHA=01741618155a509a0b3696156309cc457416173a

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE

GRANT=PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_OFFLINE_REPAIR
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8F_R2_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

IMPLEMENTATION_MODE=OFFLINE_ONLY
```

This artifact is an authorization proposal only. Creating, reviewing, or merging it does not implement repair code, modify any live runtime behavior, load a credential, touch HighLevel, retrieve a private CRM binding, issue a contact GET, issue a note POST, integrate `At1ExecutionStore`, integrate live transport, or produce live CRM effects.

The sole authorized consumer is `NW008_AT8F_R2_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR_IMPLEMENTATION_001`. No other unit may consume this grant.

### Incident and recovery classification

```text
PR105_MERGED_WITH_KNOWN_TRUST_BOUNDARY_DEFECT=YES

DEFECT_CLASS=CALLER_CONTROLLED_INPUT_CAN_REACH_TRUSTED_CAPABILITY_MINT

LIVE_EXTERNAL_EFFECTS_FROM_DEFECT=0
HIGHLEVEL_ACCESS_FROM_DEFECT=NO
CRM_MUTATIONS_FROM_DEFECT=0

ROLLBACK_REQUIRED=NO
FORWARD_REPAIR_SELECTED=YES

SOURCE_AT8E_AUTHORIZATION_CONSUMED=YES
SOURCE_AT8E_AUTHORIZATION_REUSABLE=NO
```

The defect in PR #105 did not cause live external effects, did not access HighLevel, and did not cause CRM mutations during development or merge. Forward repair is selected. The authorization from PR #104 (AT8E) was consumed during PR #105 implementation and is not reusable.

This repair authorization does not claim to have remediated the defect. Remediation is pending AT8F-R2 implementation review and merge.

### Conditional grant semantics

```text
GRANT=PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_OFFLINE_REPAIR
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the artifact defines a bounded offline private AT8 capability-handoff trust boundary repair permission that becomes usable only when both of the following are true:

1. the exact authorization artifact path is present on `main` via human review and merge; and
2. the authorized consumer unit `NW008_AT8F_R2_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR_IMPLEMENTATION_001` verifies that merge (exact path on `origin/main` / merge ancestry) before writing repair code.

The artifact text does not need to mutate after merge to become effective. Effectiveness is established by merge presence plus consumer verification, not by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is one-shot, non-reusable, and non-transferable. It is not runtime execution authority, not live-read authority, not live-mutation authority, not a third-provider-call grant, not AT8 evidence converted into write authority, and not a reusable standing grant.

```text
REPAIR_SLICE=PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY
REPAIR_MODE=OFFLINE_ONLY
GRANT_PERMITS_WHEN_EFFECTIVE=PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_OFFLINE_REPAIR_ONLY

NOTE_PATH_ARCHITECTURE_READY=YES
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_REPAIR_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO

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
IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REST_ADAPTER_LIVE_EXECUTION_AUTHORIZED=NO
THIRD_CONTACT_GET_AUTHORIZED=NO
NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0
```

## 2. Verified prerequisites and source provenance

Preflight was run before this artifact was authored.

```text
Working branch is not main
YES

DEFECTIVE_SOURCE_MERGE_SHA is ancestor of origin/main
01741618155a509a0b3696156309cc457416173a
YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #105 merge commit | `01741618155a509a0b3696156309cc457416173a` |
| PR #105 merge commit is reachable from `origin/main` | YES |
| This repair unit executed a live GET | NO |
| This repair unit executed a live POST | NO |
| This repair unit loaded credentials | NO |
| This repair unit accessed HighLevel | NO |
| Live mutation authorization issued | NO |
| AT8F-R2 implemented by this unit | NO |

## 3. Exact defects authorized for repair

```text
DEFECT_1=RAW_PRIVATE_BINDING_CAN_BE_DIRECTLY_PROMOTED_BY_HANDOFF
DEFECT_2=GENERIC_MINT_ACCEPTS_CALLER_SELECTED_ALLOWED_TRUSTED_SOURCE
DEFECT_3=STRUCTURAL_PRIVATE_BINDING_SOURCE_HAS_NO_INTERNAL_TRUST_PROVENANCE
```

AT8F-R2 may repair only the following defects introduced in PR #105:

### Defect 1: RAW_PRIVATE_BINDING_CAN_BE_DIRECTLY_PROMOTED_BY_HANDOFF

**Symptom**: The capability handoff implementation accepts raw private binding data directly as a promotion input without internal provenance validation.

**Impact on trust boundary**: Untrusted caller input can reach the trusted capability mint without intermediate verification.

**Repair scope**: AT8F-R2 must forbid direct raw-binding input from caller path to trusted handoff. All private bindings must flow through an internal trusted-binding-source capability that validates origin.

```text
RAW_PRIVATE_BINDING_DIRECT_HANDOFF=FORBIDDEN
INTERNAL_BINDING_SOURCE_REQUIRED=YES
```

### Defect 2: GENERIC_MINT_ACCEPTS_CALLER_SELECTED_ALLOWED_TRUSTED_SOURCE

**Symptom**: The generic `_mint_trusted_capability` function permits a caller-provided argument to select which trusted source is acceptable.

**Impact on trust boundary**: Caller can forge capability acceptance by specifying trusted sources they control.

**Repair scope**: AT8F-R2 must split generic mint into narrower internal constructors. Each permitted trust origin must be hard-coded through private internal construction, not caller-selected.

```text
CALLER_SELECTED_TRUSTED_SOURCE_MINT=FORBIDDEN
HARD_CODED_TRUST_ORIGIN_CONSTRUCTION=REQUIRED
GENERIC_MINT_SPLIT_INTO_NARROWER_CONSTRUCTORS=PERMITTED
```

### Defect 3: STRUCTURAL_PRIVATE_BINDING_SOURCE_HAS_NO_INTERNAL_TRUST_PROVENANCE

**Symptom**: Private binding data sources lack internal markers or validation chains to prove their origin within the trusted system.

**Impact on trust boundary**: Structurally, bindings cannot be proven to originate from authorized internal sources.

**Repair scope**: AT8F-R2 must introduce/refine an internal trusted-binding-source capability or marker. This marker must be created only by authorized internal origins and validated on every trust-boundary crossing.

```text
UNTRUSTED_STRUCTURAL_BINDING_SOURCE_HANDOFF=FORBIDDEN
TRUST_MARKER_CREATED_ONLY_BY_INTERNAL_AUTHORIZED_ORIGIN=YES
TRUST_MARKER_VALIDATED_ON_EVERY_HANDOFF=YES
```

## 4. Required repair outcome

AT8F-R2 repair implementation must establish:

```text
RAW_PRIVATE_BINDING_DIRECT_HANDOFF=FORBIDDEN
CALLER_SELECTED_TRUSTED_SOURCE_MINT=FORBIDDEN
UNTRUSTED_STRUCTURAL_BINDING_SOURCE_HANDOFF=FORBIDDEN

PRIVATE_BINDING_IS_DATA_NOT_AUTHORITY=YES
TRUST_MARKER_CREATED_ONLY_BY_INTERNAL_AUTHORIZED_ORIGIN=YES
KNOWN_AT8_STRINGS_ALONE_MINT_CAPABILITY=NO

CAPABILITY_IMMUTABLE=YES
AT8_PROVENANCE_VALIDATION=YES
CONSUMER_AUTHORIZATION_BINDING=YES
WORKFLOW_RUN_BINDING=YES
WORKFLOW_BINDING=YES
```

These conditions must hold at merge of AT8F-R2. Repair is not complete until all conditions are verified during review.

## 5. Allowed repair design approaches

Permit AT8F-R2 to:

- Remove direct raw-binding input from trusted handoff
- Introduce or refine an internal trusted-binding-source capability or marker
- Hard-code each permitted trust origin through private internal construction (not caller selection)
- Split generic `_mint_trusted_capability` into narrower internal constructors, one per trusted origin
- Modify synthetic tests to reflect the repaired trust boundary
- Add focused negative tests (e.g., "caller cannot forge capability", "untrusted source cannot handoff")
- Create/modify trust-validation chains in fixture data only as strictly required for deterministic synthetic tests

Do not require cryptographic security. Goal: API/domain non-forgeability against ordinary callers through structural design.

```text
CRYPTOGRAPHIC_SECURITY_REQUIRED=NO
DESIGN_GOAL=API_DOMAIN_NONFORGEABILITY_AGAINST_ORDINARY_CALLERS
REPAIR_MECHANISM=STRUCTURAL_DESIGN
```

## 6. Writable paths

AT8F-R2 repair is authorized to modify only:

```text
src/integrations/ghl/highlevel_rest/**
tests/integrations/ghl/highlevel_rest/**
fixtures/ghl/highlevel_rest/**
```

Fixtures may change only if strictly required for deterministic synthetic tests. No other paths may be modified.

## 7. Absolute denials

The following are strictly forbidden:

```text
HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
SECRET_ACCESS=NO
SECRET_MANAGER_IMPLEMENTATION=NO

REAL_PRIVATE_IDS_IN_REPO=FORBIDDEN
REAL_PRIVATE_IDS_IN_TESTS=FORBIDDEN
REAL_PRIVATE_IDS_IN_FIXTURES=FORBIDDEN

AT1_EXECUTION_STORE_INTEGRATION_AUTHORIZED=NO
AT1_EXECUTION_STORE_MODIFICATION_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_MODIFICATION_AUTHORIZED=NO

LIVE_TRANSPORT_IMPLEMENTATION_AUTHORIZED=NO
NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO

CONTACT_GET_AUTHORIZED=NO
NOTE_POST_AUTHORIZED=NO
NOTE_READBACK_AUTHORIZED=NO

LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO

STAGE_PATH_AUTHORIZED=NO
```

## 8. Required repair test suite

AT8F-R2 must include comprehensive deterministic synthetic tests covering:

### Trust-boundary violation tests (must FAIL if defects not repaired)

```text
TEST: RAW_PRIVATE_BINDING_DIRECT_HANDOFF_BLOCKS
DESC: Verify that passing raw private binding directly to handoff raises authorization error
REQUIREMENT: PASS

TEST: CALLER_ALLOWED_TRUSTED_SOURCE_CANNOT_MINT
DESC: Verify that caller cannot mint capability by specifying an allowed trusted source
REQUIREMENT: PASS

TEST: UNTRUSTED_BINDING_SOURCE_CANNOT_HANDOFF
DESC: Verify that private bindings without internal trust provenance cannot cross handoff
REQUIREMENT: PASS

TEST: KNOWN_AT8_STRINGS_ALONE_CANNOT_MINT
DESC: Verify that known AT8 string values alone (without internal marker/capability) cannot mint
REQUIREMENT: PASS

TEST: PRIVATE_BINDING_IS_DATA_NOT_AUTHORITY
DESC: Verify that private binding data alone grants no authority, only internal marker does
REQUIREMENT: PASS
```

### Trust-path validation tests (must PASS)

```text
TEST: VALID_INTERNAL_TRUSTED_HANDOFF
DESC: Verify that correctly-formed internal trusted handoff succeeds
REQUIREMENT: PASS

TEST: AT8_PROVENANCE_MISMATCH_BLOCKS
DESC: Verify that mismatched AT8 provenance blocks handoff
REQUIREMENT: PASS

TEST: WRONG_CONSUMER_AUTHORIZATION_BLOCKS
DESC: Verify that wrong consumer authorization identifier blocks capability use
REQUIREMENT: PASS

TEST: WRONG_WORKFLOW_RUN_BLOCKS
DESC: Verify that wrong workflow run ID blocks capability use
REQUIREMENT: PASS

TEST: WRONG_WORKFLOW_ID_BLOCKS
DESC: Verify that wrong workflow ID blocks capability use
REQUIREMENT: PASS
```

### Security and design tests

```text
TEST: CALLER_FORGED_CAPABILITY_BLOCKS
DESC: Verify that caller cannot construct/forge a capability object
REQUIREMENT: PASS

TEST: PUBLIC_BOOLEAN_PROMOTION_BLOCKS
DESC: Verify that public boolean values cannot be promoted to trusted capability
REQUIREMENT: PASS

TEST: SYNTHETIC_TEST_FACTORY_REAL_ID_USE_BLOCKS
DESC: Verify that synthetic tests cannot accidentally use real CRM IDs
REQUIREMENT: PASS (implementation must prevent)
```

### Test execution properties

```text
NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0

All existing NOTE_PATH tests remain green
```

## 9. Downstream freeze

Until AT8F-R2 is reviewed, merged, and reinspected:

```text
NOTE_PATH_STORE_INTEGRATION_AUTHORIZATION=FROZEN
BOUNDED_LIVE_NOTE_TRANSPORT_AUTHORIZATION=FROZEN
LIVE_NOTE_MUTATION_AUTHORIZATION=FROZEN

LIVE_MUTATION_AUTHORIZATION_READY=NO
```

No new live-mutation grants are issued. No live-note-write grants are issued. No bounded live-transport grants are issued. These remain frozen until AT8F-R2 repair is verified complete and merged.

## 10. Private data boundary

```text
REAL_PRIVATE_IDS_IN_REPO=FORBIDDEN
REAL_PRIVATE_IDS_IN_FIXTURES=FORBIDDEN
REAL_PRIVATE_IDS_IN_TESTS=FORBIDDEN

PRIVATE_BINDING_PUBLICATION=NO
PRIVATE_BINDING_LOGGING=NO

TEST_IDS=SYNTHETIC_ONLY

SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
PRIVATE_PRODUCTION_SOURCE_IMPLEMENTATION_AUTHORIZED=NO
```

AT8F-R2 repair may use synthetic identifiers only in tests and fixtures. Real private CRM identifiers must not appear in repository source, fixtures, tests, logs, or this authorization artifact. No Secret Manager or private production source implementation is authorized.

## 11. Provider / mutation denials

```text
THIRD_CONTACT_GET_AUTHORIZED=NO

HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0

CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
SECRET_ACCESS=NO

IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO

LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO

NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
```

## 12. Store-integration boundary

AT8E established that `At1ExecutionStore` can be reused unchanged as the durable NOTE_CREATE reservation primitive. That finding is not this grant.

```text
AT1_EXECUTION_STORE_REUSE_FIT=YES_UNCHANGED
AT1_STORE_INTEGRATION_AUTHORIZED_BY_AT8F_R1=NO
AT1_STORE_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REQUIRED=YES

NOTE_PATH_STORE_INTEGRATION_AUTHORIZED_BY_AT8F_R1=NO
NOTE_PATH_STORE_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REQUIRED=YES
```

AT8F-R2 must not modify, integrate, or implement:

- `src/integrations/ghl/at1_execution_store.py`
- `src/integrations/ghl/at1_live_transport_adapter.py`

unless a later separate authorization explicitly allows it.

## 13. Live transport boundary

```text
AT1_LIVE_TRANSPORT_IMPLEMENTATION_AUTHORIZED=NO
LIVE_TRANSPORT_AUTHORIZATION_REQUIRED=YES

NETWORK_CLIENT_LIVE_MUTATION_AUTHORIZED=NO
NETWORK_CLIENT_AUTHORIZATION_REQUIRED=YES
```

AT8F-R2 must not implement, modify, or integrate live network transport or live CRM mutation clients, unless a later separate authorization explicitly allows it.

---

**Authorization artifact**: nw008-at8f-r1-ghl-rest-private-at8-capability-handoff-trust-boundary-repair-authorization-001.md

**Defect source**: PR #105 merge `01741618155a509a0b3696156309cc457416173a`

**Authorized consumer**: NW008_AT8F_R2_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_TRUST_BOUNDARY_REPAIR_IMPLEMENTATION_001

**Consumption mode**: ONE_SHOT, non-reusable, non-transferable

**Implementation mode**: OFFLINE_ONLY

**Status**: Proposed, pending human review and merge to main
