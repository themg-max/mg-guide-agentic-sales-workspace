# NW-008 AT-8O19 - Private Execution-Surface Locator Metadata Authorization Request 001

```text
UNIT=NW008_AT8O19_PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_AUTHORIZATION_REQUEST_001
PR_CLASS=planning_only

MODE=
PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_AUTHORIZATION_REQUEST_ONLY

ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PREDECESSOR_UNIT=
NW008_AT8O18_PRIVATE_EXECUTION_SURFACE_LOCATOR_EVIDENCE_PACKET_001

PREDECESSOR_REVIEWED_HEAD=
e937eaf4f64d0adbcc3154bf269edaa12de62086

PREDECESSOR_MERGE_COMMIT=
299c98bfe69c8343946d0328b946e4b0b23e07dd

AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO

SEPARATE_AUTHORITY_FROM_AT8O16=YES
SEPARATE_AUTHORITY_FROM_AT8O12=YES

MERGING_THIS_REQUEST_GRANTS_EXECUTION_AUTHORITY=NO
SEPARATE_AUTHORIZATION_DECISION_UNIT_REQUIRED=YES

REQUESTED_MAX_INSPECTION_ATTEMPTS=1
REQUESTED_AUTHORITY_REUSABLE=NO
REQUESTED_RETRY_AUTHORIZED=NO

SOURCE_CLASS=
PRIVATE_EXECUTION_SURFACE_METADATA

SOURCE_CLASS_ALREADY_PROVEN_BY_AT8O18=YES
SOURCE_CLASS_REINSPECTION_REQUESTED=NO

SAFE_LOCATOR_MUST_BE_NON_SECRET=YES
SAFE_LOCATOR_MUST_BE_NON_PRINCIPAL=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_INTERNAL_ONLY_RAW_ENDPOINT=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_RAW_PRIVATE_CONTROL_PLANE_PATH=YES

SAFE_LOCATOR_RESULT=NOT_AUTHORIZED_TO_DISCLOSE

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```

## 1. Purpose and authority boundary

AT8O19 requests human authorization for one bounded inspection of private
locator metadata only. The requested inspection is intended to resolve the
AT8O18 locator evidence gap without spending, expanding, or modifying AT8O16 or
AT8O12.

This artifact is a request only. It does not grant authority, inspect private
locator metadata, inspect AT8O16 metadata/schema, dispatch AT8O12, invoke a
private data operation, retrieve an authority-record value, or perform any
implementation or external effect.

```text
REQUEST_SCOPE=PRIVATE_EXECUTION_SURFACE_LOCATOR_METADATA_ONLY
AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO
MERGING_THIS_REQUEST_GRANTS_EXECUTION_AUTHORITY=NO
SEPARATE_AUTHORIZATION_DECISION_UNIT_REQUIRED=YES
```

A separate authorization-decision unit must bind the exact reviewed head and
merge commit of this request before any locator-metadata inspection may occur.

## 2. Requested one-shot authorization

```text
REQUESTED_MAX_INSPECTION_ATTEMPTS=1
REQUESTED_AUTHORITY_REUSABLE=NO
REQUESTED_RETRY_AUTHORIZED=NO
REQUESTED_CONSUMPTION_TRIGGER=FIRST_PRIVATE_LOCATOR_METADATA_INSPECTION_DISPATCH

PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO
```

If separately granted, the requested authority permits at most one
locator-metadata inspection dispatch. It does not permit a second request,
pagination, continuation, follow-up, retry, or inspection under AT8O16 or
AT8O12.

## 3. Requested locator metadata fields

```text
REQUESTED_LOCATOR_METADATA_FIELDS=
connector_or_interface_safe_alias|
operation_safe_alias|
schema_or_descriptor_safe_locator|
metadata_plane_vs_data_plane_boundary_class|
locator_source_authority_class
```

Only these five locator-metadata fields are requested. No source-class
reinspection is requested:

```text
SOURCE_CLASS=
PRIVATE_EXECUTION_SURFACE_METADATA

SOURCE_CLASS_ALREADY_PROVEN_BY_AT8O18=YES
SOURCE_CLASS_REINSPECTION_REQUESTED=NO
```

The source class is preserved as context from merged AT8O18 evidence and must
not be included as a sixth requested field.

## 4. Safe locator disclosure rules

```text
SAFE_LOCATOR_MUST_BE_NON_SECRET=YES
SAFE_LOCATOR_MUST_BE_NON_PRINCIPAL=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_INTERNAL_ONLY_RAW_ENDPOINT=YES
SAFE_LOCATOR_MUST_NOT_DISCLOSE_RAW_PRIVATE_CONTROL_PLANE_PATH=YES

SAFE_LOCATOR_RESULT=NOT_AUTHORIZED_TO_DISCLOSE
```

The requested `schema_or_descriptor_safe_locator` may be returned only as a
connector-safe, non-secret, non-principal locator that does not reveal:

- an exact endpoint URL;
- an internal-only raw endpoint;
- a raw private control-plane filesystem or repository path;
- a principal, account, tenant, credential, token, or secret; or
- authority-record or private customer/contact content.

If any requested alias or locator cannot be disclosed under all safe-locator
rules, the only permitted value is `NOT_AUTHORIZED_TO_DISCLOSE`. Hashing,
truncating, encoding, or otherwise transforming a forbidden raw value does not
make it an authorized safe locator.

## 5. Explicitly forbidden fields and values

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

The future locator-metadata inspection must fail closed before retrieval if any
requested field requires a forbidden value to be read, returned, logged,
persisted, or transformed. Retrieval followed by redaction is not authorized.

## 6. Explicitly forbidden actions

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

The request does not authorize a live test, dry run reaching a private data
source, operation-invoking health probe, descriptor access that invokes a data
operation, or mutation of any connector or control-plane surface.

## 7. Separation from AT8O16

```text
SEPARATE_AUTHORITY_FROM_AT8O16=YES

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O19_REQUEST_COUNTS_AS_AT8O16_DISPATCH=NO
AT8O19_REQUEST_MERGE_COUNTS_AS_AT8O16_DISPATCH=NO
FUTURE_AT8O19_LOCATOR_INSPECTION_COUNTS_AS_AT8O16_DISPATCH=NO
```

A future locator-metadata inspection governed by this request must not request
any AT8O16 metadata/schema field. AT8O16 maintains independent dispatch,
attempt, consumption, and proof state.

## 8. Separation from AT8O12

```text
SEPARATE_AUTHORITY_FROM_AT8O12=YES

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

AT8O19_REQUEST_COUNTS_AS_AT8O12_DISPATCH=NO
AT8O19_REQUEST_MERGE_COUNTS_AS_AT8O12_DISPATCH=NO
FUTURE_AT8O19_LOCATOR_INSPECTION_COUNTS_AS_AT8O12_DISPATCH=NO
```

A future locator-metadata inspection governed by this request must not request
any original AT8O12 metadata field or invoke the private data operation.
AT8O12 maintains independent dispatch, attempt, consumption, and proof state.

## 9. Fail-closed and decision requirements

A separate decision must deny the request, or a later authorized inspection
must fail closed before dispatch, if:

- the five requested fields cannot be isolated from non-requested metadata;
- a safe alias or safe locator cannot be produced without reading or exposing a
  forbidden raw value;
- metadata-plane access cannot be separated from private-data-plane invocation;
- a private data operation, AT8O16 inspection, or AT8O12 inspection would be
  dispatched;
- more than one request, pagination, continuation, follow-up, or retry would be
  required; or
- the exact reviewed request head and merge commit are not bound.

```text
UNKNOWN_FAILS_CLOSED=YES
REQUEST_MERGE_IS_NOT_AUTHORIZATION=YES
AUTHORIZATION_DECISION_REQUIRED_BEFORE_INSPECTION=YES
```

Merging AT8O19 does not authorize inspection.

## 10. Hard blocks and preserved state

```text
PRIVATE_LOCATOR_METADATA_INSPECTION=BLOCKED_PENDING_SEPARATE_DECISION
AT8O16_INSPECTION_DISPATCH=BLOCKED
AT8O12_INSPECTION_DISPATCH=BLOCKED
PRIVATE_DATA_OPERATION_INVOCATION=BLOCKED
AUTHORITY_RECORD_CONTENT_ACCESS=BLOCKED
EXACT_HUMAN_PRINCIPAL_LOOKUP=BLOCKED
ADC_INSPECTION=BLOCKED
IAM_INSPECTION_OR_MUTATION=BLOCKED
TOKEN_CREATOR_AUTHORIZATION=BLOCKED
SERVICE_ACCOUNT_IMPERSONATION=BLOCKED
MG_MCP_MUTATION=BLOCKED
DEPLOYMENT=BLOCKED
HIGHLEVEL_CALLS=BLOCKED
CRM_MUTATION=BLOCKED

AUTHORIZATION_GRANTED=NO
PRIVATE_LOCATOR_METADATA_INSPECTION_EXECUTED=NO

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

## 11. Validation and stop state

Only this AT8O19 artifact may be staged:

```text
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o19-private-execution-surface-locator-metadata-authorization-request-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0
GOVERNANCE_AUTHORIZATION_CHANGES=0

AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO
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

AT8O19 stops for formal governance review without inspection, dispatch,
mutation, or authorization consumption.
