# NW-008 AT1 GHL PIT Rotation Human Activation 001

## 0. Activation identity

```text
ACTIVATION_ID=
  NW008_AT1_GHL_PIT_ROTATION_HUMAN_ACTIVATION_001
ARTIFACT_PATH=
  governance/authorizations/nw008-at1-ghl-pit-rotation-human-activation-001.md
CLASSIFICATION=HUMAN_FINALIZED_ONE_SHOT_HIGHLEVEL_PIT_ROTATION_ACTIVATION
PR_CLASS=authorization
OWNER=HUMAN_HIGHLEVEL_OPERATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PREPARED_AT_UTC=2026-08-30T23:02:24Z
ACTIVATION_FINALIZED_AT_UTC=2026-08-30T23:02:24Z

STATE=FINALIZED_READY_FOR_EXECUTION
ACTIVATED_BY_HUMAN_REVIEW_MERGE=YES
ACTIVATION_PRESENT=YES
CONSUMED=NO
EXECUTION_WINDOW_OPEN=YES
```

This activation grants authority to a human HighLevel operator to perform
exactly one token rotation of the MG_Guide private integration, under the
merged authorization `NW008_AT1_GHL_PIT_ROTATION_AUTHORIZATION_001`.

```text
MERGING_THIS_ACTIVATION_ROTATES_ANYTHING=NO
HUMAN_CONSOLE_ROTATION_AUTHORIZED_BY_THIS_ACTIVATION=YES
HUMAN_OPERATOR_PERFORMS_ROTATION_NOT_ORCHESTRATOR=YES
ORCHESTRATOR_PERFORMS_ROTATION=NO
ORCHESTRATOR_OBSERVES_ROTATED_VALUE=NO
```

Merge of this activation opens the bounded execution window. The human
operator then initiates the rotation in the HighLevel console at their
discretion. The orchestrator has zero role in the actual rotation action.

## 1. Controlling authorization

```text
AUTHORIZATION_ID=
  NW008_AT1_GHL_PIT_ROTATION_AUTHORIZATION_001
AUTHORIZATION_PR=367
AUTHORIZATION_PR_MERGED=YES
AUTHORIZATION_MERGE_SHA=
  a181193bc33851b3667510d8d44b85acddfe0bb3
AUTHORIZATION_STATE=MERGED
AUTHORIZATION_FORMAL_VERDICT=READY_FOR_MERGE
AUTHORIZATION_REVIEW_ID=5062121113
```

The authorization is merged and carries all required predicates from proof
PR #366 (`ATTESTATION_RESULT=PASS`, integration present/active/correctly-bound,
correct scopes, correct token class).

## 2. Bounded execution — one-shot fresh window

```text
RUN_ID=
  nw008-at1-ghl-pit-rotation-20260830T230224Z-c2302c9bf722
WINDOW_START_UTC=2026-08-30T23:02:24Z
WINDOW_DURATION_MINUTES=60
WINDOW_EXTENDABLE=NO
ACTIVATION_REUSABLE=NO
ACTIVATION_TRANSFERABLE=NO

EXECUTION_GATE=OPEN_AFTER_ACTIVATION_MERGE
EXECUTION_WINDOW_STATE=ACTIVE
```

The window is 60 minutes from merge. The human operator must complete the
rotation within this window. The window is **not** extendable: if the window
closes without execution, do not reopen it under this activation. Prepare
a fresh activation instead.

## 3. Authorized actor and surface

```text
AUTHORIZED_ACTOR=
  HUMAN_HIGHLEVEL_OPERATOR

AUTHORIZED_SURFACE=
  HIGHLEVEL_OPERATOR_CONSOLE

AUTHORIZED_TARGET=
  MG_Guide private integration

AUTHORIZED_OPERATION=
  TOKEN_ROTATION
```

The human HighLevel operator navigates to the console, locates the MG_Guide
private integration, and initiates the rotation from the console UI. This is
the only authorized actor and surface.

```text
ORCHESTRATOR_CONSOLE_ACCESS=NO
ORCHESTRATOR_REST_API_ACCESS=NO
ORCHESTRATOR_MCP_ACCESS_FOR_ROTATION=NO
ORCHESTRATOR_MUTATION_AUTHORITY=NO
```

## 4. Rotation specification — exact

```text
ROTATION_MODE=ROTATE_AND_EXPIRE_LATER
OLD_TOKEN_REVOKED_IMMEDIATELY=NO
OLD_TOKEN_EXPIRY_DELAY_DAYS=7

MAX_TOKEN_ROTATIONS=1
ROTATION_ATTEMPTS_RESERVED=1

ROTATE_AND_EXPIRE_NOW=FORBIDDEN
SECOND_ROTATION=FORBIDDEN
SECOND_ROTATION_ATTEMPT=FORBIDDEN
```

Select `ROTATE_AND_EXPIRE_LATER` from the console UI. Do not select
`Revoke Immediately` or `Rotate & Revoke`. The selected mode schedules
automatic expiry of the old token 7 days after rotation.

## 5. Forbidden provider mutations

```text
NEW_PRIVATE_INTEGRATION_CREATE=0
PRIVATE_INTEGRATION_DELETE=0
PRIVATE_INTEGRATION_RENAME=0

SCOPE_EDITS=0
LOCATION_EDITS=0
LOCATION_REBINDING=0

HIGHLEVEL_API_CALLS=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0

SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
RUNTIME_SOURCE_EDITS=0
TEST_EDITS=0
DEPLOYMENTS=0
```

No changes to the integration itself — only the token. Integration state,
scopes, and location binding must remain unchanged.

## 6. Token disclosure — absolute

```text
TOKEN_IN_REPOSITORY=FORBIDDEN
TOKEN_IN_CHAT=FORBIDDEN
TOKEN_IN_PULL_REQUEST=FORBIDDEN
TOKEN_IN_ISSUE=FORBIDDEN
TOKEN_IN_LOG=FORBIDDEN
TOKEN_IN_TERMINAL_OUTPUT=FORBIDDEN
TOKEN_IN_SHELL_HISTORY=FORBIDDEN
TOKEN_IN_SCREENSHOT=FORBIDDEN

TOKEN_VALUE_RECORDED=NO
TOKEN_PREFIX_RECORDED=NO
TOKEN_SUFFIX_RECORDED=NO
TOKEN_LENGTH_RECORDED=NO
TOKEN_HASH_RECORDED=NO

NEW_TOKEN_DESTINATION_AFTER_ROTATION=
  PRIVATE_HUMAN_OPERATOR_CUSTODY

SECRET_MANAGER_WRITE_BY_THIS_ACTIVATION=NO
```

After the rotation, the HighLevel console displays the new token once. The
human operator is responsible for capturing it to private custody pending
the separately authorized repair unit. The token must not be pasted into any
file, terminal, chat, log, or screenshot. This activation performs no Secret
Manager write.

## 7. Consumption record

```text
CONSUMPTION_RECORD_ID=
  NW008_AT1_GHL_PIT_ROTATION_CONSUMPTION_001

INITIAL_STATE=PREPARED_UNCONSUMED

STATE_AT_ACTIVATION_MERGE=PREPARED_UNCONSUMED
STATE_IMMEDIATELY_BEFORE_ROTATION_CLICK=AUTHORITY_CONSUMED

CONSUMPTION_TRIGGER=
  FIRST_ROTATION_ATTEMPT_IN_HIGHLEVEL_CONSOLE

CONSUMED_ON_ATTEMPT_NOT_ON_SUCCESS=YES
```

Authority is consumed the moment the human clicks the rotation control in
the console. If HighLevel returns an unexpected state (e.g., "rotation failed",
"integration not found", "token invalid"), the authority is still spent.

```text
ON_ROTATION_FAILURE=
  ROTATION_AUTHORITY_REUSABLE=NO
  SECOND_ROTATION_ATTEMPT=FORBIDDEN
  STOP=GHL_PIT_ROTATION_FAILED
```

Do not attempt to rotate again under this activation. Prepare a fresh
activation instead.

## 8. Expected execution proof — mandatory after rotation

After the human completes the console rotation action, this unit requires
the operator to create:

```text
REQUIRED_EXECUTION_PROOF=
  proof/nw008/nw-008-at1-ghl-pit-rotation-execution-proof-001.md
```

The proof documents that exactly one rotation was performed, the new token
was captured to private custody, the integration state remained unchanged,
and no provider API calls were made.

```text
REQUIRED_PROOF_FIELDS=
  ROTATION_ATTEMPTS=1
  ROTATION_PERFORMED=<YES|NO>
  ROTATION_ACTOR=HUMAN_HIGHLEVEL_OPERATOR
  ROTATION_METHOD=HIGHLEVEL_OPERATOR_CONSOLE
  ROTATION_MODE=ROTATE_AND_EXPIRE_LATER
  ROTATION_AT_UTC=<timestamp>

  INTEGRATION_STILL_ACTIVE=<YES|NO>
  BOUND_LOCATION_UNCHANGED=<YES|NO>
  CONTACTS_READONLY_STILL_PRESENT=<YES|NO>
  SCOPES_UNCHANGED=<YES|NO>

  NEW_TOKEN_IN_PRIVATE_CUSTODY=<YES|NO>
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

If `ROTATION_PERFORMED=NO`, this activation's authority was not used.
If `ROTATION_PERFORMED=YES`, a separate Activation 002 would be required for
any future rotation.

## 9. Stop

```text
STATE=FINALIZED_READY_FOR_EXECUTION
ACTIVATED_BY_HUMAN_REVIEW_MERGE=YES
ACTIVATION_PRESENT=YES
EXECUTION_WINDOW_STATE=ACTIVE
EXECUTION_WINDOW_EXPIRES_UTC=2026-08-30T23:02:24Z_PLUS_60_MINUTES

WINDOW_EXTENDABLE=NO
ACTIVATION_REUSABLE=NO

DO_NOT_EXECUTE_DURING_REPO_UNIT=YES
DO_NOT_CLICK_ROTATION_WHILE_PULL_REQUEST_OPEN=YES

TOKEN_ROTATIONS_PERFORMED_IN_THIS_REPO_UNIT=0
HIGHLEVEL_API_CALLS_IN_THIS_REPO_UNIT=0
SECRET_MUTATIONS_IN_THIS_REPO_UNIT=0

AUTHORITY_CONSUMED_IN_THIS_REPO_UNIT=NO
READY_FOR_HUMAN_OPERATOR=YES

NEXT=HUMAN_OPERATOR_INITIATES_ROTATION_IN_HIGHLEVEL_CONSOLE_AFTER_MERGE
THEN=HUMAN_OPERATOR_CREATES_EXECUTION_PROOF
THEN=EXECUTE_NW008_AT1_GHL_PIT_CREDENTIAL_REPAIR_AUTHORIZATION_001
```

This is the instrument; its merge is the authorization. The human operator
reads it, understands the bounded execution window and token custody
requirements, then navigates to the HighLevel console at their discretion
within the 60-minute window and performs the rotation under the selected
`ROTATE_AND_EXPIRE_LATER` mode.
