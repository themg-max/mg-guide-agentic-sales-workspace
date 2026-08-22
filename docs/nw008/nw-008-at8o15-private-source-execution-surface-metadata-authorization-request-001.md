# NW-008 AT-8O15 - Private Source Execution-Surface Metadata Authorization Request 001

```text
UNIT=NW008_AT8O15_PRIVATE_SOURCE_EXECUTION_SURFACE_METADATA_AUTHORIZATION_REQUEST_001
PR_CLASS=planning_only
MODE=PRIVATE_EXECUTION_SURFACE_METADATA_AUTHORIZATION_REQUEST_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PREDECESSOR_UNIT=
NW008_AT8O14_ONE_SHOT_SANITIZED_PRIVATE_METADATA_INSPECTION_EXECUTION_PACKET_001

PREDECESSOR_REVIEWED_HEAD=
fb14636e962faf5f4979f0a10b07cd446f43a48a

PREDECESSOR_MERGE_COMMIT=
2c9a8decac646f3445ad570f70596b39ee1f1f9d

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0

AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO
PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_EXECUTED=NO

ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0

SEPARATE_AUTHORITY_FROM_AT8O12=YES
MERGING_THIS_REQUEST_GRANTS_EXECUTION_AUTHORITY=NO
SEPARATE_AUTHORIZATION_DECISION_UNIT_REQUIRED=YES
STOP_FOR_GOVERNANCE_REVIEW=YES
```

## 1. Purpose and authority boundary

AT8O15 requests human authorization for one bounded inspection of private
execution-surface metadata and schemas. The requested inspection is limited to
the connector/interface and operation contract facts needed to determine
whether the original AT8O12 one-shot metadata inspection can later be executed
safely.

This artifact is a request only. It does not grant authority, inspect the
private execution surface, invoke a private operation, retrieve an authority
record value, dispatch the original AT8O12 inspection, implement a connector,
or perform a production mutation.

```text
INSPECTION_SCOPE=PRIVATE_EXECUTION_SURFACE_METADATA_AND_SCHEMA_ONLY
AUTHORITY_RECORD_VALUE_RETRIEVAL=FORBIDDEN
EXACT_PRINCIPAL_MATERIAL=FORBIDDEN
PRODUCTION_MUTATION=FORBIDDEN

SEPARATE_AUTHORITY_FROM_AT8O12=YES
MERGING_THIS_REQUEST_GRANTS_EXECUTION_AUTHORITY=NO
SEPARATE_AUTHORIZATION_DECISION_UNIT_REQUIRED=YES
```

The requested authority is separate from AT8O12. Approval, denial, execution,
consumption, or closeout of this request must not consume, expand, replace, or
otherwise change the original AT8O12 authorization.

## 2. Requested authorization shape

```text
REQUEST_PURPOSE=RESOLVE_AT8O14_EXECUTION_SURFACE_SAFETY_GAPS_WITH_SANITIZED_METADATA_AND_SCHEMA_ONLY
REQUESTED_SOURCE_CLASS=PRIVATE_EXECUTION_SURFACE_METADATA
TARGET_SOURCE_CLASS=PRIVATE_EXECUTION_SURFACE_METADATA
INSPECTION_ACTOR_CLASS=HUMAN_AUTHORIZED_METADATA_REVIEWER
HUMAN_APPROVAL_REQUIRED=YES

REQUESTED_MAX_INSPECTION_ATTEMPTS=1
REQUESTED_AUTHORITY_REUSABLE=NO
REQUESTED_RETRY_AUTHORIZED=NO
REQUESTED_CONSUMPTION_TRIGGER=FIRST_PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_DISPATCH

AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO
PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_EXECUTED=NO
```

A later authorization decision must bind the exact reviewed head and merge
commit of this request. If granted, the requested authority permits one
metadata/schema inspection dispatch only. It does not permit invoking the
private source data operation described by the schema.

## 3. Requested metadata fields

```text
REQUESTED_METADATA_FIELDS=
connector_or_interface_safe_alias|
operation_safe_alias|
operation_schema_version|
request_projection_supported|
request_projection_field_names_supported|
response_schema_version|
response_field_names_supported|
pagination_model|
continuation_model|
implicit_followup_model|
retry_model|
single_invocation_completion_model|
safe_alias_production_model|
forbidden_field_source_exclusion_model|
sanitization_contract_present|
dispatch_receipt_model|
non_secret_operation_identifier_supported|
non_secret_correlation_identifier_supported|
runtime_read_interface_present
```

Only these field names are requested. Values must be sanitized metadata or
schema facts. Safe aliases must be non-principal and non-secret; if a connector
or operation cannot be represented by such an alias, its alias value must be
returned as `NOT_AUTHORIZED_TO_DISCLOSE`.

`request_projection_field_names_supported` and
`response_field_names_supported` may contain field names only. They may not
contain field values, examples populated with private data, defaults containing
private data, authority-record content, or principal material.

## 4. Explicitly forbidden fields

```text
EXPLICITLY_FORBIDDEN_FIELDS=
authority record content|
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

The inspection must stop before retrieval if a schema description, example,
default, diagnostic, or error would disclose a forbidden field value.
Retrieval followed by redaction is not authorized.

## 5. Explicitly forbidden actions

```text
EXPLICITLY_FORBIDDEN_ACTIONS=
IAM mutation|
Token Creator authorization|
service-account impersonation|
MG MCP mutation|
deployment|
HighLevel calls|
CRM mutations|
original AT8O12 inspection dispatch
```

Schema or metadata description must be read-only. No live data operation,
health probe that invokes the operation, test request, dry run that reaches the
private source, pagination request, continuation request, follow-up request, or
retry is authorized by this request.

## 6. Sanitization and provenance requirements

A future authorization decision may permit return of only the requested field
names with sanitized values. Each returned value must identify:

1. whether it was observed directly from execution-surface metadata/schema or
   derived;
2. the connector/interface safe alias, when safely disclosable;
3. the operation safe alias, when safely disclosable;
4. the schema version governing the observation, when present; and
5. whether any requested field could not be safely disclosed.

```text
RESULT_CONTENT=SANITIZED_EXECUTION_SURFACE_METADATA_AND_SCHEMA_FACTS_ONLY
RAW_SCHEMA_EXAMPLES_WITH_PRIVATE_VALUES=FORBIDDEN
RAW_DEFAULTS_WITH_PRIVATE_VALUES=FORBIDDEN
RAW_DIAGNOSTICS_WITH_PRIVATE_VALUES=FORBIDDEN
OBSERVED_VERSUS_DERIVED_PROVENANCE_REQUIRED=YES
NON_REQUESTED_FIELD_RETURN=FORBIDDEN
```

No response may contain an authority-record value, exact principal material,
credential, token, ADC content, IAM binding content, secret, or private
customer/contact value.

## 7. Separation from the original AT8O12 authorization

```text
AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

AT8O15_REQUEST_COUNTS_AS_AT8O12_DISPATCH=NO
AT8O15_REQUEST_MERGE_COUNTS_AS_AT8O12_DISPATCH=NO
AT8O15_FUTURE_SCHEMA_INSPECTION_COUNTS_AS_AT8O12_DISPATCH=NO
```

The original AT8O12 dispatch remains the first request sent to the authorized
private source for any AT8O12 metadata field. A separately authorized future
schema inspection governed by a decision on this request may inspect only
execution-surface metadata/schema and must not request any AT8O12 source
metadata value. The two authorities must have independent dispatch, attempt,
consumption, and proof states.

## 8. Fail-closed and approval requirements

The request must be denied or a later authorized inspection must fail closed
before dispatch if:

- metadata/schema cannot be separated from authority-record values;
- an exact principal, credential, token, secret, ADC content, IAM binding
  content, or private customer/contact value would be exposed;
- safe connector and operation aliases cannot be produced without inspecting
  forbidden material;
- describing the operation would invoke it or reach the original private data
  source;
- more than one metadata/schema request, pagination, continuation, follow-up,
  or retry would be required; or
- the exact reviewed request head and merge commit are not bound by a separate
  authorization decision.

```text
UNKNOWN_FAILS_CLOSED=YES
AUTHORIZATION_DECISION_REQUIRED_BEFORE_INSPECTION=YES
REQUEST_MERGE_IS_NOT_AUTHORIZATION=YES
```

Merging this request does not grant execution authority. A separate
authorization-decision unit is required before any private execution-surface
metadata/schema inspection can occur.

## 9. Hard blocks and preserved state

```text
PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION=BLOCKED_PENDING_SEPARATE_DECISION
AUTHORITY_RECORD_CONTENT_ACCESS=BLOCKED
EXACT_HUMAN_PRINCIPAL_LOOKUP=BLOCKED
ADC_INSPECTION=BLOCKED
IAM_INSPECTION_OR_MUTATION=BLOCKED
TOKEN_CREATOR_AUTHORIZATION=BLOCKED
SERVICE_ACCOUNT_IMPERSONATION=BLOCKED
MG_MCP_MUTATION=BLOCKED
DEPLOYMENT=BLOCKED
HIGHLEVEL_CALLS=BLOCKED
CRM_MUTATIONS=BLOCKED
ORIGINAL_AT8O12_INSPECTION_DISPATCH=BLOCKED

AUTHORIZATION_GRANTED=NO
PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_EXECUTED=NO
AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

## 10. Validation and stop state

Only this AT8O15 request artifact may be staged. Repository validation is
limited to the required no-inspection checks:

```text
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o15-private-source-execution-surface-metadata-authorization-request-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0
GOVERNANCE_AUTHORIZATION_CHANGES=0

AUTHORIZATION_REQUESTED=YES
AUTHORIZATION_GRANTED=NO
PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_EXECUTED=NO
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO
AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```

AT8O15 stops for governance review without inspecting the private execution
surface or consuming AT8O12.
