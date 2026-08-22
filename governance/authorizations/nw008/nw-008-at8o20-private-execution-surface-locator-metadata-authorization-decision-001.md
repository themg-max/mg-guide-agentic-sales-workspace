# NW-008 AT-8O20 - Private Execution-Surface Locator Metadata Authorization Decision 001

```text
UNIT=
NW008_AT8O20_PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_AUTHORIZATION_DECISION_001

PR_CLASS=authorization

MODE=
PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_AUTHORIZATION_DECISION_ONLY

ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

AUTHORIZATION_SUBJECT_UNIT=
NW008_AT8O19_PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_AUTHORIZATION_REQUEST_001

AUTHORIZATION_SUBJECT_REVIEWED_HEAD=
429c415cba8ec1c20776b0c977ee877dcc5dad2f

AUTHORIZATION_SUBJECT_MERGE_COMMIT=
cd001ebe34a3e9d7c9b797b765476a64b2618322

AUTHORIZATION_DECISION=GRANTED

AUTHORIZED_SOURCE_CLASS=
PRIVATE_EXECUTION_SURFACE_METADATA

AUTHORIZED_LOCATOR_METADATA_FIELDS=
connector_or_interface_safe_alias|
operation_safe_alias|
schema_or_descriptor_safe_locator|
metadata_plane_vs_data_plane_boundary_class|
locator_source_authority_class

MAX_INSPECTION_ATTEMPTS=1
INSPECTION_ATTEMPTS_USED=0

AUTHORITY_REUSABLE=NO
RETRY_AUTHORIZED=NO

AUTHORIZATION_CONSUMPTION_MODEL=
CONSUMED_ON_FIRST_PRIVATE_LOCATOR_METADATA_INSPECTION_DISPATCH

PRE_DISPATCH_FAILURE_CONSUMES_ATTEMPT=NO
POST_DISPATCH_FAILURE_CONSUMES_ATTEMPT=YES
INDETERMINATE_DISPATCH_CONSUMES_ATTEMPT=YES

INSPECTION_DISPATCH_DEFINITION=
FIRST_REQUEST_SENT_TO_THE_AUTHORIZED_PRIVATE_LOCATOR_METADATA_SOURCE_FOR_ANY_AUTHORIZED_AT8O20_FIELD

DISTRIBUTED_ATOMICITY_CLAIMED=NO

AUTHORIZATION_ACTIVATION_CONDITION=
PR_MERGED_TO_MAIN_AND_REVIEWED_HEAD_ANCESTRY_VERIFIED

AUTHORIZATION_EFFECTIVE=NO
AUTHORIZATION_STATE=PENDING_MERGE

SAFE_LOCATOR_FALLBACK_RESULT=
NOT_AUTHORIZED_TO_DISCLOSE

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

AT8O20_LOCATOR_METADATA_INSPECTION_DISPATCHED=NO
PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```

## 1. Authorization decision

AT8O20 grants the exact merged AT8O19 request for one bounded private
locator-metadata inspection attempt. The grant is limited to the five
authorized locator metadata fields and does not authorize AT8O16 inspection,
AT8O12 inspection, or a private data operation.

Before this decision PR is merged, the authorization is not effective:

```text
AUTHORIZATION_EFFECTIVE=NO
AUTHORIZATION_STATE=PENDING_MERGE
AUTHORIZATION_ACTIVATION_CONDITION=PR_MERGED_TO_MAIN_AND_REVIEWED_HEAD_ANCESTRY_VERIFIED
```

Merge and reviewed-head ancestry verification are necessary for activation.
They do not dispatch or execute inspection.

## 2. Authorized source and locator metadata fields

```text
AUTHORIZED_SOURCE_CLASS=
PRIVATE_EXECUTION_SURFACE_METADATA

AUTHORIZED_LOCATOR_METADATA_FIELDS=
connector_or_interface_safe_alias|
operation_safe_alias|
schema_or_descriptor_safe_locator|
metadata_plane_vs_data_plane_boundary_class|
locator_source_authority_class
```

The source class is binding context and is not an additional inspection field.
Only the five listed fields may be requested or returned.

## 3. Safe-locator constraints preserved exactly from AT8O19

```text
SAFE_LOCATOR_MUST_BE_NON_SECRET=YES
SAFE_LOCATOR_MUST_BE_NON_PRINCIPAL=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_INTERNAL_ONLY_RAW_ENDPOINT=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_RAW_PRIVATE_CONTROL_PLANE_PATH=YES
```

If any authorized alias or locator cannot be safely disclosed under every
constraint, the permitted fallback is:

```text
SAFE_LOCATOR_FALLBACK_RESULT=
NOT_AUTHORIZED_TO_DISCLOSE
```

The fallback is not a pre-inspection result state and does not imply that a
locator has been inspected or found.

## 4. Forbidden fields and values preserved exactly from AT8O19

```text
EXPLICITLY_FORBIDDEN_FIELDS=
exact endpoint URL|
raw private control-plane path|
authority-record content|
exact human principal|
principal email|
principal user ID|
credentials|
tokens|
ADC contents|
IAM policy binding contents|
secrets|
private customer/contact data
```

No forbidden raw value may be read merely to redact, hash, truncate, encode, or
transform it. If producing an authorized field requires access to a forbidden
value, future execution must fail closed before retrieval.

## 5. Forbidden actions preserved exactly from AT8O19

```text
EXPLICITLY_FORBIDDEN_ACTIONS=
AT8O16 inspection dispatch|
AT8O12 inspection dispatch|
private data operation invocation|
ADC inspection|
IAM inspection or mutation|
Token Creator authorization|
service-account impersonation|
MG MCP mutation|
deployment|
HighLevel calls|
CRM mutation
```

The grant does not permit live operation tests, a dry run reaching a private
data source, an operation-invoking health probe, or a descriptor request that
invokes the private data plane.

## 6. One-shot dispatch and consumption model

```text
MAX_INSPECTION_ATTEMPTS=1
INSPECTION_ATTEMPTS_USED=0
AUTHORITY_REUSABLE=NO
RETRY_AUTHORIZED=NO

AUTHORIZATION_CONSUMPTION_MODEL=
CONSUMED_ON_FIRST_PRIVATE_LOCATOR_METADATA_INSPECTION_DISPATCH

PRE_DISPATCH_FAILURE_CONSUMES_ATTEMPT=NO
POST_DISPATCH_FAILURE_CONSUMES_ATTEMPT=YES
INDETERMINATE_DISPATCH_CONSUMES_ATTEMPT=YES

INSPECTION_DISPATCH_DEFINITION=
FIRST_REQUEST_SENT_TO_THE_AUTHORIZED_PRIVATE_LOCATOR_METADATA_SOURCE_FOR_ANY_AUTHORIZED_AT8O20_FIELD

DISTRIBUTED_ATOMICITY_CLAIMED=NO
```

An indeterminate source-facing handoff must be treated as dispatched and
consumed. No retry, continuation, follow-up, pagination request, or compensating
dispatch is authorized.

AT8O20 is decision-only and does not cross the dispatch boundary:

```text
AT8O20_LOCATOR_METADATA_INSPECTION_DISPATCHED=NO
PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO
```

## 7. Separation from AT8O16 and AT8O12

AT8O20 is a distinct authority. It does not consume, expand, replace, or modify
either existing authorization.

```text
AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO
```

Future AT8O20 locator-metadata inspection must not request any AT8O16 or AT8O12
field and must retain independent dispatch, attempt, consumption, and proof
state.

## 8. Hard blocks during AT8O20

```text
LOCATOR_METADATA_INSPECTION_EXECUTION=BLOCKED
AT8O16_INSPECTION_DISPATCH=BLOCKED
AT8O12_INSPECTION_DISPATCH=BLOCKED
PRIVATE_DATA_OPERATION=BLOCKED
AUTHORITY_RECORD_VALUES=BLOCKED
EXACT_PRINCIPAL=BLOCKED
ADC_INSPECTION=BLOCKED
IAM_INSPECTION_OR_MUTATION=BLOCKED
TOKEN_CREATOR_AUTHORIZATION=BLOCKED
SERVICE_ACCOUNT_IMPERSONATION=BLOCKED
MG_MCP_MUTATION=BLOCKED
DEPLOYMENT=BLOCKED
HIGHLEVEL_CALL=BLOCKED
CRM_MUTATION=BLOCKED
```

No private locator metadata is inspected, requested, or returned in this
decision unit.

## 9. Validation and non-actions

Only this AT8O20 artifact may be staged:

```text
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=governance/authorizations/nw008/nw-008-at8o20-private-execution-surface-locator-metadata-authorization-decision-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0

AUTHORIZATION_DECISION=GRANTED
AUTHORIZATION_EFFECTIVE=NO
AUTHORIZATION_STATE=PENDING_MERGE

AT8O20_LOCATOR_METADATA_INSPECTION_DISPATCHED=NO
PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```

AT8O20 stops for governance review without inspection, dispatch, mutation, or
consumption of AT8O20, AT8O16, or AT8O12.
