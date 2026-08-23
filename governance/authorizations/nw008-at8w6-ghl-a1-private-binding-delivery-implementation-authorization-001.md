# NW-008 AT8W6 GHL A1 Private-Binding Delivery Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W6_GHL_A1_PRIVATE_BINDING_DELIVERY_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w6-ghl-a1-private-binding-delivery-implementation-authorization-001.md
AUTHORIZATION_BRANCH=
  nw008-at8w6-ghl-a1-private-binding-delivery-implementation-authorization-001
BASE_REF=origin/main
BASE_SHA=2c64a67eaf82b1684bb77193bdb2b352a13485a5

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
```

This artifact is an authorization proposal only. Its creation, review, and
merge do not implement A1, modify runtime source, read a private binding or
secret payload, call HighLevel, mutate CRM, change IAM or secrets, deploy, or
change production configuration.

```text
RUNTIME_SOURCE_CHANGES_IN_AT8W6=0
IMPLEMENTATION_PERFORMED_IN_AT8W6=NO
EXTERNAL_EFFECTS_IN_AT8W6=0
LIVE_EXECUTION_AUTHORITY_CREATED=NO
```

## 2. AT8W5 merge verification

The required AT8W5 resolution was verified before authoring this authorization.

```text
AT8W5_PR=171
AT8W5_STATE=MERGED
AT8W5_HUMAN_MERGED=YES
AT8W5_MERGED_AT=2026-08-23T16:14:02Z
AT8W5_TITLE=docs(nw008): resolve AT8W5 private-binding source readiness
AT8W5_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/171

AT8W5_REVIEWED_HEAD=
393b139f5ecc1c7db7bc5bff04a61d8c419d708e

AT8W5_ACTUAL_MERGE_COMMIT=
2c64a67eaf82b1684bb77193bdb2b352a13485a5

AT8W5_MERGE_PARENTS=
  37a6b1d8bb870601a2070c6592a008b66aa8339d
  393b139f5ecc1c7db7bc5bff04a61d8c419d708e

AT8W5_SECOND_PARENT_IS_REVIEWED_HEAD=YES
AT8W5_ARTIFACT_PRESENT_ON_MAIN=YES
AT8W5_REVIEWED_HEAD_ANCESTRY_VERIFIED=YES
AT8W5_MERGE_COMMIT_ON_MAIN=YES

VERIFY_AT8W5_ARTIFACT_PRESENT_ON_MAIN=PASS
VERIFY_AT8W5_REVIEWED_HEAD_ANCESTRY=PASS
VERIFY_AT8W5_MERGE_COMMIT_ON_MAIN=PASS
```

The exact reviewed head is the second parent and an ancestor of the recorded
merge commit. The merge commit is on `origin/main`, and the predecessor
artifact is present at:

```text
AT8W5_ARTIFACT=
docs/nw008/nw-008-at8w5-ghl-private-binding-source-readiness-resolution-001.md
```

## 3. Grant and one-shot consumption semantics

```text
GRANT=OFFLINE_PRIVATE_BINDING_DELIVERY_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
AUTHORIZATION_EFFECTIVE_AT_AUTHORING=NO
SELF_ACTIVATION=FORBIDDEN

AUTHORIZED_CONSUMER=
NW008_AT8W7_GHL_A1_PRIVATE_BINDING_DELIVERY_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation

AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO
CONSUMPTION_RECORD_PATH=
proof/nw008/at-8w7/nw008-at8w7-ghl-a1-private-binding-delivery-implementation-consumption-001.md
IMPLEMENTATION_PROOF_PATH=
proof/nw008/at-8w7/nw008-at8w7-ghl-a1-private-binding-delivery-implementation-proof-001.md
```

This authorization becomes usable only after human review and merge places this
exact artifact on `main`. Before any authorized source write, the sole
authorized consumer must independently verify that merge and record its
one-shot consumption at the required path. The consumer must not alter this
authorization artifact or transfer its grant.

```text
BEFORE_FIRST_AUTHORIZED_EDIT_REQUIRED=
  VERIFY_AT8W6_EXACT_AUTHORIZATION_MERGED_TO_MAIN|
  VERIFY_AUTHORIZATION_PATH_PRESENT_ON_ORIGIN_MAIN|
  CREATE_ONE_SHOT_CONSUMPTION_RECORD
```

This is not standing implementation authority, not authority for any other
consumer, and not live execution authority.

## 4. Individually bound current readiness prerequisites

Every prerequisite is bound individually to the merged AT8W5 resolution. The
consumer must fail closed and make no authorized source edit if any required
field is not exactly `YES`, unavailable through the already attested
non-disclosing mechanism, or would require a prohibited action.

```text
PREDECESSOR_UNIT=
NW008_AT8W5_GHL_PRIVATE_BINDING_SOURCE_READINESS_RESOLUTION_001

CURRENT_PRIVATE_BINDING_SOURCE_EXISTS=YES
CURRENT_PRIVATE_BINDING_IS_SYNTHETIC=YES
CURRENT_PRIVATE_BINDING_IS_EXACT_ALLOWLISTED=YES
CURRENT_PRIVATE_BINDING_AUTHORIZED_FOR_RUNTIME_DELIVERY=YES
SAFE_PRIVATE_BINDING_DELIVERY_REFERENCE_AVAILABLE=YES
A0_POSITIVE_AND_SAFE=YES
A1_ELIGIBLE=YES

REQUIRED_PREREQUISITE_COUNT=7
REQUIRED_PREREQUISITES_BOUND_INDIVIDUALLY=YES
REQUIRED_PREREQUISITES_ALL_YES=YES
```

The authorization does not reproduce a private binding value, safe delivery
reference, or private delivery mechanism. The five current readiness
predicates are attested non-disclosing facts, not permission to discover,
inspect, enumerate, derive, or publish private identifiers.

```text
PREREQUISITE_FAILURE_POLICY=FAIL_CLOSED
FAIL_CLOSED_BEFORE_SOURCE_WRITE=YES
FAIL_CLOSED_IF_SAFE_REFERENCE_NOT_CONSUMABLE_THROUGH_ROOT_OWNED_MECHANISM=YES
FAIL_CLOSED_IF_DISCOVERY_OR_DISCLOSURE_WOULD_BE_REQUIRED=YES
```

## 5. Authorized bounded offline implementation

The future consumer may connect only the currently attested, preverified
synthetic private-binding delivery mechanism to the existing root-owned
verified-capability runtime path. The result must accept only an existing safe
private delivery reference through the authorized root-owned mechanism and
must issue the existing verified binding capability without exposing private
values to callers, logs, tests, proofs, or repository content.

```text
PERMIT=
CONSUME_EXISTING_SAFE_PRIVATE_DELIVERY_REFERENCE|
IMPLEMENT_ROOT_OWNED_BINDING_DELIVERY_SEAM|
ISSUE_EXISTING_VERIFIED_BINDING_CAPABILITY|
DETERMINISTIC_OFFLINE_TESTING

IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
PRIVATE_VALUE_IN_REPOSITORY=FORBIDDEN
PRIVATE_VALUE_IN_TEST_FIXTURE=FORBIDDEN
CALLER_SUPPLIED_PRIVATE_BINDING_OVERRIDE=FORBIDDEN
ROOT_OWNED_DELIVERY_MECHANISM_REQUIRED=YES
EXISTING_VERIFIED_CAPABILITY_REQUIRED=YES
```

The implementation seam must preserve the existing root-owned
verified-capability construction path. It may not introduce a second
composition root, a generic REST executor, a transport-budget relaxation, or a
fallback that discovers, searches for, or derives a private binding.

```text
IMPLEMENTATION_SUCCESS_REQUIRES=
  EXISTING_SAFE_PRIVATE_DELIVERY_REFERENCE_CONSUMED|
  ROOT_OWNED_BINDING_DELIVERY_SEAM_USED|
  EXISTING_VERIFIED_BINDING_CAPABILITY_ISSUED|
  DETERMINISTIC_OFFLINE_TESTS_PASS|
  ZERO_PROHIBITED_EFFECTS
```

## 6. Required implementation sequence

```text
SEQUENCE_STEP_1=VERIFY_EXACT_AT8W6_AUTHORIZATION_MERGED_TO_MAIN
SEQUENCE_STEP_2=VERIFY_ALL_SEVEN_BOUND_PREREQUISITES_EQUAL_YES
SEQUENCE_STEP_3=CREATE_ONE_SHOT_CONSUMPTION_RECORD_BEFORE_FIRST_AUTHORIZED_EDIT
SEQUENCE_STEP_4=CONSUME_ONLY_EXISTING_SAFE_PRIVATE_DELIVERY_REFERENCE
SEQUENCE_STEP_5=IMPLEMENT_ROOT_OWNED_BINDING_DELIVERY_SEAM_OR_FAIL_CLOSED
SEQUENCE_STEP_6=ISSUE_EXISTING_VERIFIED_BINDING_CAPABILITY_ONLY
SEQUENCE_STEP_7=RUN_DETERMINISTIC_OFFLINE_TESTS
SEQUENCE_STEP_8=RECORD_IMPLEMENTATION_PROOF_AND_TERMINATE

NO_SOURCE_WRITE_IF_REFERENCE_UNAVAILABLE=YES
NO_SOURCE_WRITE_IF_PROHIBITED_DISCOVERY_OR_DISCLOSURE_WOULD_BE_REQUIRED=YES
```

The consumption record must precede the first authorized edit. If the
mechanism cannot safely provide the existing reference through the authorized
root-owned path, the consumer must stop without discovery, fallback,
alternative-source access, or source mutation.

## 7. Implementation proof and deterministic validation requirements

```text
IMPLEMENTATION_PROOF_REQUIREMENTS=
AUTHORIZATION_MERGE_VERIFIED=YES|
ALL_SEVEN_BOUND_PREREQUISITES_RECORDED_INDIVIDUALLY=YES|
CONSUMPTION_RECORD_CREATED_BEFORE_FIRST_AUTHORIZED_EDIT=YES|
ROOT_OWNED_DELIVERY_SEAM_ONLY=YES|
EXISTING_VERIFIED_BINDING_CAPABILITY_ONLY=YES|
SAFE_REFERENCE_UNAVAILABLE_FAILS_CLOSED=YES|
DETERMINISTIC_OFFLINE_TESTS=PASS|
HIGHLEVEL_CALLS=0|
CRM_MUTATIONS=0|
SECRET_PAYLOAD_READS=0|
EXTERNAL_EFFECTS=0

PRIVATE_BINDING_VALUE_PUBLICATION=NO
PRIVATE_IDENTIFIER_HASH_OR_TRANSFORM=NO
NETWORK_CALLS=0
```

Required tests must be deterministic and offline. They must demonstrate that
the root-owned delivery seam accepts the authorized safe reference, issues only
the existing verified capability, rejects missing or invalid reference
conditions fail closed, and exposes no caller-controlled raw private-binding
override.

```text
VALIDATION_REQUIREMENTS=
DETERMINISTIC_UNIT_TEST_FOR_AUTHORIZED_DELIVERY_REFERENCE_ACCEPTANCE|
DETERMINISTIC_UNIT_TEST_FOR_MISSING_REFERENCE_FAIL_CLOSED|
DETERMINISTIC_UNIT_TEST_FOR_INVALID_REFERENCE_FAIL_CLOSED|
DETERMINISTIC_UNIT_TEST_FOR_EXISTING_VERIFIED_CAPABILITY_ISSUANCE|
DETERMINISTIC_UNIT_TEST_FOR_NO_CALLER_RAW_BINDING_OVERRIDE|
NO_NETWORK_TESTS|
NO_PRIVATE_VALUES_IN_TESTS_LOGS_OR_PROOFS|
TARGETED_EXISTING_TESTS_PASS|
EXACT_HEAD_CI_PASS
```

## 8. Explicit denials

```text
DISCOVER_PRIVATE_BINDING=NO
SEARCH_PRIVATE_SOURCE=NO
LIST_PRIVATE_SOURCE=NO
ENUMERATE_PRIVATE_SOURCE=NO
CREATE_PRIVATE_BINDING=NO
CHANGE_PRIVATE_BINDING=NO
PUBLISH_PRIVATE_BINDING=NO
HASH_OR_TRANSFORM_PRIVATE_IDENTIFIERS=NO
AT8O24_REACCESS=NO
AT8O20_DISPATCH=NO

HIGHLEVEL_CALL=NO
CRM_MUTATION=NO
CONTACT_CREATE=NO
NOTE_CREATE=NO
STAGE_MUTATION=NO
SECRET_PAYLOAD_READ=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO
CREDENTIAL_ROTATION=NO
DEPLOYMENT=NO
PRODUCTION_CONFIGURATION_MUTATION=NO

TRANSPORT_BUDGET_RELAXATION=NO
SECOND_COMPOSITION_ROOT=NO
GENERIC_REST_EXECUTOR=NO
```

These denials include all direct, indirect, fallback, test-fixture, logging,
proof, and publication paths. In particular, an unavailable safe reference
does not permit an alternate lookup, a reconstruction from partial data, a hash
or transform, an AT8O24 reaccess, or an AT8O20 dispatch.

```text
PRIVATE_BINDING_VALUES_DISCLOSED=NO
PRIVATE_CONTACT_SEARCH=NO
PRIVATE_CONTACT_LIST=NO
PRIVATE_SOURCE_ENUMERATION=NO
PRIVATE_ID_HASH_OR_TRANSFORM=NO
REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
RUNTIME_SOURCE_CHANGES_IN_AT8W6=0
```

## 9. Human governance countersign and PR boundary

```text
HUMAN_GOVERNANCE_COUNTERSIGN=YES

HUMAN_GOVERNANCE_GRANT=
I authorize one bounded offline implementation unit to connect the currently
attested, preverified NW-008 synthetic private-binding delivery mechanism to
the existing root-owned verified-capability runtime path. The grant permits
implementation and deterministic testing of the private-binding delivery seam
only. It does not authorize discovery, search, list, enumeration, disclosure,
hashing or transformation of private identifiers; AT8O24 reaccess; AT8O20
dispatch; real secret payload reads; HighLevel network calls; CRM mutation;
contact creation; note creation; stage mutation; IAM, secret, credential,
deployment, or production-configuration changes. The implementation must
consume only an existing safe private delivery reference and fail closed if it
cannot be provided through the authorized root-owned mechanism.

HUMAN_MERGE_REQUIRED=YES
HUMAN_GOVERNANCE_RETAINS_MERGE_AUTHORITY=YES
```

```text
AT8W6_AUTHORIZATION_PR_NON_ACTIONS=
NO_RUNTIME_SOURCE_EDIT|
NO_TEST_SOURCE_EDIT|
NO_PACKAGE_MANIFEST_EDIT|
NO_PRIVATE_SOURCE_ACCESS|
NO_PRIVATE_VALUE_READ_OR_PUBLICATION|
NO_HIGHLEVEL_CALL|
NO_CRM_MUTATION|
NO_SECRET_PAYLOAD_READ|
NO_IAM_SECRET_CREDENTIAL_DEPLOY_OR_PRODUCTION_CONFIGURATION_CHANGE|
NO_IMPLEMENTATION_PERFORMED

CHANGED_FILE_COUNT_EXPECTED=1
ONLY_AUTHORIZATION_ARTIFACT_CHANGED=YES
STOP_FOR_EXACT_HEAD_CI_AND_FORMAL_REVIEW=YES
HUMAN_MERGE_REQUIRED=YES
```

## 10. Final disposition

```text
AT8W5_MERGE_VERIFIED=YES
AT8W5_ALL_READINESS_PREDICATES_BOUND_INDIVIDUALLY=YES
AT8W6_AUTHORIZATION_PROPOSED=YES
AT8W6_AUTHORIZATION_EFFECTIVE_AT_AUTHORING=NO
AT8W6_IMPLEMENTATION_PERFORMED=NO
AT8W6_EXTERNAL_EFFECTS=0

NEXT_AFTER_HUMAN_MERGE=
NW008_AT8W7_GHL_A1_PRIVATE_BINDING_DELIVERY_IMPLEMENTATION_001

DO_NOT_IMPLEMENT_A1_IN_AT8W6=YES
DO_NOT_CREATE_LIVE_EXECUTION_AUTHORITY_IN_AT8W6=YES
STOP_FOR_FORMAL_REVIEW_AND_HUMAN_MERGE=YES
```
