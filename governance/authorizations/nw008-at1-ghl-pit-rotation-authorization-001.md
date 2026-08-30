# NW-008 AT1 GHL PIT Rotation Authorization 001

## 0. Authorization identity

```text
AUTHORIZATION_ID=
  NW008_AT1_GHL_PIT_ROTATION_AUTHORIZATION_001
ARTIFACT_PATH=
  governance/authorizations/nw008-at1-ghl-pit-rotation-authorization-001.md
CLASSIFICATION=SINGLE_PROVIDER_CONSOLE_TOKEN_ROTATION_AUTHORIZATION
PR_CLASS=authorization
OWNER=HUMAN_HIGHLEVEL_OPERATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PREPARED_AT_UTC=2026-08-30T00:00:00Z

STATE=PROPOSED_PENDING_INDEPENDENT_REVIEW
PR_READY=YES
PROOF_PR_366_MERGED=YES
PROOF_MERGE_SHA=309c99fdc8f49c83c17d7d6ec093c51b4013880d
ACTIVATION_PRESENT=NO
CONSUMED=NO
```

Drafting, reviewing, or merging this artifact rotates nothing. Rotation
requires independent review **and** a separate fresh human activation, and is
then performed by a human in the HighLevel console — never by an agent, and
never through an API.

```text
MERGING_THIS_AUTHORIZATION_ROTATES_ANYTHING=NO
SEPARATE_HUMAN_ACTIVATION_REQUIRED=YES
ROTATION_ACTOR=HUMAN_ONLY
ORCHESTRATOR_MAY_PERFORM_ROTATION=NO
ORCHESTRATOR_MAY_OBSERVE_ROTATED_VALUE=NO
```

## 1. Input gate

```text
REQUIRED_INPUT_ARTIFACT_1=
  proof/nw008/nw-008-at1-ghl-pit-operator-attestation-001.md
REQUIRED_INPUT_ARTIFACT_2=
  proof/nw008/nw-008-at1-ghl-rest-v3-provider-403-root-cause-diagnostic-001.md
CARRIED_BY=PR_366
PROOF_PR_NUMBER=366
PROOF_PR_HEAD_SHA=9a93b7f2ab917337c194a695da580672d2e3a1f8
PROOF_PR_MERGED=YES
PROOF_MERGE_SHA=309c99fdc8f49c83c17d7d6ec093c51b4013880d

REQUIRED_INPUT_PREDICATES=
  ATTESTATION_RESULT=PASS                              -> SATISFIED
  MG_GUIDE_PRIVATE_INTEGRATION_PRESENT=YES             -> SATISFIED
  MG_GUIDE_PRIVATE_INTEGRATION_ACTIVE=YES              -> SATISFIED
  BOUND_LOCATION_MATCH=YES                             -> SATISFIED
  CONTACTS_READONLY_PRESENT=YES                        -> SATISFIED
  TOKEN_CLASS=PRIVATE_INTEGRATION_TOKEN                -> SATISFIED
  TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION=YES -> SATISFIED

INPUT_GATE=OPEN
GATE_SATISFIED_BY=PROOF_PR_366_MERGED
ACTIVATABLE=NO
```

The predicate evidence is complete and durable. The gate is open for review.
Activation remains blocked because the rotated token does not yet exist; it
must be produced by a separate fresh human activation.

## 1.1 Secret version inventory — read-only, metadata only

Inspected prior to this authorization's PR:

```text
INVENTORY_METHOD=gcloud secrets versions list MG_GUIDE_PIT_GHL --project=831270426395
INVENTORY_TIMESTAMP_UTC=2026-08-30T22:31:00Z
INVENTORY_PAYLOAD_READS=0

CURRENT_SECRET_VERSION_SET={1}
CURRENT_ENABLED_VERSION_SET={1}
NEXT_EXPECTED_VERSION=2
VERSION_NUMBER_FROZEN=NO

NEXT_VERSION_DETERMINISTIC=YES
REASON=Only_version_1_exists;_GCP_Secret_Manager_will_assign_version_2
```

## 2. Justification

The attestation excluded every console-observable sub-cause. The integration
is correctly provisioned; what has never been verified is whether the bytes
sealed in `MG_GUIDE_PIT_GHL/versions/1` are this integration's live token.

```text
RESIDUAL_SUB_CAUSE=
  STALE_OR_INCORRECT_TOKEN_MATERIAL_SEALED_IN_MG_GUIDE_PIT_GHL_VERSIONS_1
RESIDUAL_SUB_CAUSE_CONFIDENCE=HIGH

WHY_ROTATION_RATHER_THAN_INSPECTION=
  THE_SEALED_PAYLOAD_MUST_NOT_BE_READ_TO_COMPARE_IT;
  ROTATION_PRODUCES_A_KNOWN_GOOD_VALUE_WITHOUT_ANY_PAYLOAD_READ
```

This is the operative point. Diagnosing the discrepancy by reading and
comparing the sealed payload would require exactly the disclosure this lane
forbids. Rotating instead yields a value known to belong to the attested
integration, with `SECRET_PAYLOAD_READS=0` throughout.

## 3. The integration is NOT to be recreated

```text
INTEGRATION=MG_Guide
INTEGRATION_IS_CORRECT=YES
INTEGRATION_ATTESTED_BY=HUMAN_HIGHLEVEL_OPERATOR
INTEGRATION_ATTESTED_AT_UTC=2026-08-30T22:22:07Z

NEW_PRIVATE_INTEGRATION_CREATE=FORBIDDEN
PRIVATE_INTEGRATION_DELETE=FORBIDDEN
PRIVATE_INTEGRATION_RENAME=FORBIDDEN
```

Creating a second integration would fork the credential boundary, leave two
plausible sources for any future 403, and invalidate the attestation this
authorization rests on. The attested integration is the correct one; only its
token is replaced.

## 4. Exact authorized mutation

```text
AUTHORIZED_SURFACE=HIGHLEVEL_OPERATOR_CONSOLE
AUTHORIZED_ACTOR=HUMAN_HIGHLEVEL_OPERATOR
AUTHORIZED_TARGET=MG_Guide private integration
AUTHORIZED_OPERATION=TOKEN_ROTATION

MAX_TOKEN_ROTATIONS=1
ROTATION_MODE=ROTATE_AND_EXPIRE_LATER
```

`ROTATE_AND_EXPIRE_LATER` is the HighLevel console rotation mode that enforces
the governance requirement: the previous token is **not** revoked at rotation
time. The mode schedules automatic expiry 7 days later, which mitigates
surprise outages when a deployed surface still holds the old token.

```text
OLD_TOKEN_REVOKED_IMMEDIATELY=NO
OLD_TOKEN_REMAINS_VALID_DURING_OVERLAP=YES
OLD_TOKEN_EXPIRY_SCHEDULED_BY_THIS_ROTATION=YES
OLD_TOKEN_EXPIRY_DELAY_DAYS=7

IMMEDIATE_TOKEN_REVOCATION=FORBIDDEN
SECOND_ROTATION_ATTEMPT_BEFORE_EXPIRY=FORBIDDEN
```

The 7-day expiry is not a separate later decision — the selected HighLevel
rotation mode itself enforces this behavior. The `IMMEDIATE_TOKEN_REVOCATION=FORBIDDEN`
guard ensures a future operator does not choose an immediate-revoke mode that
would convert a diagnosable 403 into an outage.

## 5. Forbidden effects

```text
NEW_PRIVATE_INTEGRATION_CREATE=0
PRIVATE_INTEGRATION_DELETE=0
SCOPE_EDITS=0
SCOPE_ADDITIONS=0
SCOPE_REMOVALS=0
LOCATION_EDITS=0
LOCATION_REBINDING=0

HIGHLEVEL_API_CALLS=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0

SECRET_MUTATIONS=0
SECRET_VERSIONS_ADDED=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
RUNTIME_SOURCE_EDITS=0
TEST_EDITS=0
DEPLOYMENTS=0
```

Note that `SECRET_MUTATIONS=0` is correct here. This unit rotates the provider
credential and stops. Sealing the rotated value into Secret Manager is the
separate `NW008_AT1_GHL_PIT_CREDENTIAL_REPAIR_AUTHORIZATION_001`, which carries
its own review and its own activation.

The scope flags observed during attestation — `contacts.write`,
`opportunities.readonly`, `opportunities.write`, `locations.readonly` — are
provider-state facts and confer nothing:

```text
OBSERVED_WRITE_SCOPES_AUTHORIZE_ANYTHING_HERE=NO
SCOPE_PRESENCE_IS_NOT_AUTHORITY=YES
```

## 6. Token handling — absolute

```text
TOKEN_IN_REPOSITORY=FORBIDDEN
TOKEN_IN_CHAT=FORBIDDEN
TOKEN_IN_ISSUE=FORBIDDEN
TOKEN_IN_PULL_REQUEST=FORBIDDEN
TOKEN_IN_TERMINAL_OUTPUT=FORBIDDEN
TOKEN_IN_SHELL_HISTORY=FORBIDDEN
TOKEN_IN_LOGS=FORBIDDEN
TOKEN_IN_SCREENSHOT_COMMITTED=FORBIDDEN

TOKEN_VALUE_RECORDED=NO
TOKEN_PREFIX_RECORDED=NO
TOKEN_SUFFIX_RECORDED=NO
TOKEN_LENGTH_RECORDED=NO
TOKEN_HASH_RECORDED=NO

CAPTURE_METHOD=PRIVATE_OPERATOR_CUSTODY_OUT_OF_BAND
NEW_TOKEN_IN_PRIVATE_CUSTODY=YES_REQUIRED
CUSTODY_OWNER=HUMAN_HIGHLEVEL_OPERATOR

CAPTURE_DESTINATION=
  PRIVATE_HUMAN_OPERATOR_CUSTODY_PENDING_SEPARATELY_AUTHORIZED_SECRET_REPAIR

SECRET_MANAGER_MUTATION_BY_THIS_UNIT=NO
SECRET_MANAGER_WRITE_REQUIRES_SEPARATE_ACTIVE_AUTHORIZATION=YES
```

The rotated value remains in private operator custody until the separately
authorized and activated repair unit receives it directly. This unit performs
no Secret Manager write. The token must not be pasted into this conversation,
any file, any PR, any log, or any command line — including as an argument to
`gcloud` or any tool where it would enter shell history or process listings.

## 7. Caps

| Cap | Limit | Enforced |
| --- | --- | --- |
| token rotations | 1 | YES |
| private integrations created | 0 | YES |
| private integrations deleted | 0 | YES |
| scope edits | 0 | YES |
| location edits | 0 | YES |
| HighLevel API calls | 0 | YES |
| MCP calls | 0 | YES |
| CRM reads | 0 | YES |
| CRM mutations | 0 | YES |
| secret mutations | 0 | YES |

```text
AUTHORIZATION_USE_LIMIT=1
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
CONSUMPTION_TRIGGER=FIRST_ROTATION_ACTION_IN_THE_CONSOLE
CONSUMED_ON_ATTEMPT_NOT_ON_SUCCESS=YES
```

If the rotation attempt fails or produces an unexpected console state, the
authority is spent. Recover by preparing authorization 002; do not retry under
this one.

```text
ON_ROTATION_FAILURE=
  STOP=GHL_PIT_ROTATION_FAILED
  SECOND_ROTATION_ATTEMPT=FORBIDDEN
```

## 8. Required proof on execution

```text
REQUIRED_EXECUTION_PROOF=
  proof/nw008/nw-008-at1-ghl-pit-rotation-execution-proof-001.md

REQUIRED_FIELDS=
  ROTATION_ATTEMPTS=1
  ROTATION_PERFORMED=<YES|NO>
  ROTATION_ACTOR=HUMAN_HIGHLEVEL_OPERATOR
  ROTATION_METHOD=HIGHLEVEL_OPERATOR_CONSOLE
  ROTATION_AT_UTC=<timestamp>
  ROTATION_MODE=ROTATE_AND_EXPIRE_LATER
  INTEGRATION_UNCHANGED_APART_FROM_TOKEN=YES
  INTEGRATION_STILL_ACTIVE=YES
  BOUND_LOCATION_UNCHANGED=YES
  CONTACTS_READONLY_STILL_PRESENT=YES
  SCOPES_UNCHANGED=YES
  OLD_TOKEN_REVOKED=NO
  NEW_TOKEN_IN_PRIVATE_CUSTODY=YES
  TOKEN_VALUE_PUBLISHED=NO
  TOKEN_HASH_PUBLISHED=NO
  TOKEN_LENGTH_PUBLISHED=NO
  SCREENSHOTS_COMMITTED=NO
  HIGHLEVEL_API_CALLS=0
  CRM_READS=0
  CRM_MUTATIONS=0
  SECRET_MUTATIONS=0
  AUTHORITY_CONSUMED=YES
  AUTHORITY_REUSABLE=NO
```

`BOUND_LOCATION_UNCHANGED` and `SCOPES_UNCHANGED` are required because a
console rotation flow is a plausible place to accidentally alter binding or
scope. The post-rotation proof must re-confirm both, by the same fingerprint
method used in the attestation, publishing only the boolean.

## 9. Successor units — not authorized here

```text
NEXT_1=READ_ONLY_SECRET_VERSION_INVENTORY_AND_FREEZE   (metadata only)
NEXT_2=REVIEW_AND_MERGE_CREDENTIAL_REPAIR_AUTHORIZATION_001
NEXT_3=FRESH_HUMAN_ACTIVATION_OF_REPAIR_AUTHORIZATION_001
NEXT_4=ADD_EXACTLY_ONE_MG_GUIDE_PIT_GHL_VERSION_WITH_THE_ROTATED_TOKEN
NEXT_5=RUNTIME_EXACT_VERSION_PINNING_TO_NEXT_EXPECTED_VERSION + TESTS
NEXT_6=NW008_AT1_GHL_REST_V3_BOUNDED_READ_AUTHORIZATION_004
NEXT_7=FRESH_ACTIVATION_004 + FRESH_RUN_ID
NEXT_8=EXACTLY_ONE_GET_CONTACTS_BOUNDED_READ

AUTHORIZATION_003_REUSE_ALLOWED=NO
ACTIVATION_003_REUSE_ALLOWED=NO
RUN_ID_003_REUSE_ALLOWED=NO
```

## 10. Stop

```text
STATE=PROPOSED_PENDING_INDEPENDENT_REVIEW
PR_READY=YES
PROOF_PR_366_MERGED=YES
PROOF_MERGE_SHA=309c99fdc8f49c83c17d7d6ec093c51b4013880d

INPUT_GATE=OPEN
GATE_SATISFIED_BY=PROOF_PR_366_MERGED
VERSION_INVENTORY_RECONCILED=YES
VERSION_INVENTORY_FROZEN=NO

ACTIVATABLE=NO
ACTIVATABLE_WHEN=AFTER_INDEPENDENT_REVIEW_AND_AUTHORIZATION_MERGE
BLOCKING_ON=
  INDEPENDENT_REVIEW_OF_THIS_AUTHORIZATION_PR
  AUTHORIZATION_PR_MERGE
  FRESH_HUMAN_ACTIVATION_FROM_HIGHLEVEL_CONSOLE

TOKEN_ROTATIONS_PERFORMED=0
HIGHLEVEL_API_CALLS_PERFORMED=0
SECRET_MUTATIONS_PERFORMED=0
STOP
```
