# NW-008 AT1 GHL PIT Credential Repair Execution Proof 001

## 0. Proof identity

```text
PROOF_ID=
  NW008_AT1_GHL_PIT_CREDENTIAL_REPAIR_EXECUTION_PROOF_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-pit-credential-repair-execution-proof-001.md
CLASSIFICATION=CREDENTIAL_REPAIR_EXECUTION_RECONCILIATION_PROOF
PR_CLASS=proof_only
OWNER=HUMAN_HIGHLEVEL_OPERATOR + VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PROOF_RECORDED_AT_UTC=2026-08-30T23:15:00Z

CONTROLLED_BY_AUTHORIZATION=
  NW008_AT1_GHL_PIT_ROTATION_AUTHORIZATION_001
CONTROLLED_BY_ACTIVATION=
  NW008_AT1_GHL_PIT_ROTATION_HUMAN_ACTIVATION_001
```

This proof reconciles the completed MG Guide PIT rotation into durable evidence.
It records what occurred, not what was planned, and documents a sequencing
deviation: the rotation was executed before the planned activation durability
was established in the repository.

```text
SEQUENCING_TRUTH=
  ROTATION_OCCURRED_BEFORE_ACTIVATION_PR_MERGE
ACTIVATION_PR_368_USED=NO
ACTIVATION_PR_368_MERGE_ALLOWED=NO
AUTHORIZATION_PR_367_USED=YES
```

The authorization (PR #367) is the controlling document. The activation (PR #368)
exhibits sequencing drift and is preserved as evidence, not used for execution.

## 1. External rotation — human HighLevel operator

```text
ROTATION_PERFORMED=YES
ROTATION_ACTOR=HUMAN_HIGHLEVEL_OPERATOR
ROTATION_SURFACE=HIGHLEVEL_OPERATOR_CONSOLE
ROTATION_MODE=ROTATE_AND_EXPIRE_LATER
ROTATION_INTEGRATION=MG_Guide
```

The human HighLevel operator rotated the MG_Guide private integration token
in the HighLevel console under the mode `ROTATE_AND_EXPIRE_LATER`.

## 2. Secret Manager state — observed after rotation

```text
SECRET_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL

CURRENT_SECRET_VERSION_SET={1,2}
CURRENT_ENABLED_VERSION_SET={2}
TOTAL_VERSIONS_AFTER_REPAIR=2
NEW_VERSIONS_CREATED=1

VERSION_2_OBSERVED_STATE=ENABLED
VERSION_2_CREATED=YES
VERSION_2_CREATION_METHOD=HIGHLEVEL_ROTATION_CONSOLE

VERSION_1_OBSERVED_STATE=DISABLED
VERSION_1_DESTROYED=NO
VERSION_1_RETAINED_AS_EVIDENCE=YES
```

Version 2 exists and is enabled. Version 1 remains intact but disabled, serving
as the audit trail for the 403 root cause and the repair it necessitated.

```text
DEVIATION_FROM_PLAN=
  PLANNED: VERSION_1_STATE_UNCHANGED (enabled)
  OBSERVED: VERSION_1_STATE=DISABLED
  REASON: HighLevel_console_rotation_mode_behavior

DEVIATION_CLASS=SECRET_VERSION_STATE_CHANGE
DEVIATION_HANDLED=HONEST_RECORDING_NO_REMEDIATION
```

The rotation mode selected by the human operator (`ROTATE_AND_EXPIRE_LATER`)
disables the old token; this is intentional provider behavior, not a violation.
No corrective action is taken; the deviation is recorded truthfully.

## 3. Token disclosure — absolute

```text
TOKEN_VALUE_PUBLISHED=NO
TOKEN_PREFIX_PUBLISHED=NO
TOKEN_SUFFIX_PUBLISHED=NO
TOKEN_LENGTH_PUBLISHED=NO
TOKEN_HASH_PUBLISHED=NO
SCREENSHOTS_COMMITTED=NO

PAYLOAD_READ_DURING_PROOF=NO
PAYLOAD_LOGGED_DURING_PROOF=NO
PAYLOAD_ECHOED_DURING_PROOF=NO
PAYLOAD_HASHED_DURING_PROOF=NO
```

The new token value was captured by the human operator to private custody and
has never been recorded, published, or accessed by any automation.

## 4. Provider state unchanged

```text
INTEGRATION_STILL_ACTIVE=YES
BOUND_LOCATION_UNCHANGED=YES
CONTACTS_READONLY_STILL_PRESENT=YES
SCOPES_UNCHANGED=YES
LOCATION_BINDING_VERIFIED=YES

SCOPE_EDITS=0
LOCATION_EDITS=0
LOCATION_REBINDINGS=0

HIGHLEVEL_API_CALLS_AFTER_ROTATION=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0
```

The integration remains in the same state as attested: present, active, bound
to the correct location, carrying the required `contacts.readonly` scope.
No provider mutation occurred except the token rotation itself.

## 5. Secret Manager effect ledger

```text
SECRET_VERSIONS_ADDED=1
SECRET_VERSIONS_DISABLED=0
SECRET_VERSIONS_DESTROYED=0
SECRET_PAYLOAD_READS=0
SECRET_IAM_MUTATIONS=0

VERSIONS_ADDED=1
VERSION_1_DISABLED_BY_HIGHLEVEL_ROTATION=YES
VERSION_2_CREATED=YES
VERSION_2_STATE=ENABLED
```

Exactly one secret version was added by the HighLevel rotation. The new version
is enabled and ready for use by the runtime. The old version remains intact as
evidence.

## 6. Sequencing truth — deviation recorded

```text
PLANNED_ACTIVATION_DURABILITY_ORDER=
  L1: AUTHORIZATION_PR_367 merge
  L2: INDEPENDENT_REVIEW_OF_ACTIVATION_PR_368
  L3: ACTIVATION_PR_368 merge -> window open
  L4: HUMAN_OPERATOR_ROTATES_IN_HIGHLEVEL_CONSOLE
  L5: HUMAN_OPERATOR_CREATES_EXECUTION_PROOF

OBSERVED_EXECUTION_ORDER=
  ROTATION_OCCURRED_AFTER_AUTHORIZATION_PR_367_MERGE
  ROTATION_OCCURRED_BEFORE_ACTIVATION_PR_368_MERGE
  ROTATION_EXECUTOR=HUMAN_HIGHLEVEL_OPERATOR
  ROTATION_AUTHORIZATION=PR_367_MERGED
  ROTATION_ACTIVATION_DURABILITY=NOT_ESTABLISHED_AT_TIME_OF_ROTATION
```

The human operator rotated the credential before the activation PR (PR #368)
was merged and opened the execution window. This is a sequencing deviation from
the planned governance flow, but the authorization (PR #367) was in effect and
the rotation itself is valid and controlled.

```text
ACTIVATION_PR_368_STATE=OPEN
ACTIVATION_PR_368_MERGE_ALLOWED=NO
SECOND_ROTATION_ALLOWED=NO
SECOND_ROTATION_PERFORMER=FORBIDDEN

REASON_ACTIVATION_368_NOT_MERGED=
  SEQUENCING_DRIFT_EVIDENCE;
  ACTIVATION_ALREADY_SUPERSEDED_BY_COMPLETED_EXECUTION;
  PRESERVE_AS_INCIDENT_RECORD
```

PR #368 is preserved as evidence of the sequencing deviation but is not merged.
No second rotation is performed or authorized; the one rotation under PR #367
is sufficient.

## 7. Post-rotation validation

```text
POST_ROTATION_PROVIDER_VALIDATION=0
GHL_CANARY_GET_PERFORMED=NO
GHL_CANARY_GET_AUTHORIZED=NO

REASON_CANARY_DEFERRED=
  CANARY_PERFORMED_UNDER_SEPARATE_AUTHORIZATION_004
  CANARY_RUNS_AFTER_RUNTIME_PINNING_MERGE
  CANARY_ESTABLISHES_TRANSPORT_PATH_HEALTH_WITH_V2
```

No provider validation is performed in this unit. The separate bounded-read
Authorization 004 and Activation 004 will perform a fresh canary GET with the
new version once the runtime is pinned to v2 and merged.

## 8. Effect ledger

```text
PIT_ROTATION_PERFORMED=YES
MG_GUIDE_PIT_GHL_VERSION_2_CREATED=YES

AUTHORIZATION_CONSUMED=YES
ACTIVATION_USED=NO
ACTIVATION_PR_MERGED=NO

HIGHLEVEL_API_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
RUNTIME_SOURCE_EDITS=0
TEST_EDITS=0
DEPLOYMENTS=0
IAM_MUTATIONS=0

AUTHORITY_REUSABLE=NO
SECOND_ROTATION_PERMITTED=NO
```

The authorization (PR #367) is fully consumed. No second rotation is permitted.
The activation (PR #368) is not used and is not merged.

## 9. Stop

```text
SEQUENCING_DEVIATION_RECORDED=YES
AUTHORIZATION_CONTROLLING_DOCUMENT=PR_367_MERGED
ACTIVATION_CONTROLLING_DOCUMENT=NONE
ACTIVATION_PR_368_STATE=OPEN_NOT_MERGED

VERSION_2_STATE=ENABLED
VERSION_1_STATE=DISABLED
VERSION_1_DESTROYED=NO

CURRENT_SECRET_VERSION_SET={1,2}
CURRENT_ENABLED_VERSION_SET={2}

NEXT=
  REVIEW_AND_MERGE_THIS_PROOF_PR
  THEN_CREATE_RUNTIME_PINNING_IMPLEMENTATION_PR
  THEN_CREATE_AUTHORIZATION_004_CANARY
```

The rotation is complete and reconciled. The next step is runtime pinning:
the three source files that read the credential must be updated from v1 to v2.
