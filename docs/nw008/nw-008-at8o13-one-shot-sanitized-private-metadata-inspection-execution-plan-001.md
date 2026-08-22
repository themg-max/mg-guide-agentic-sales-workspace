# NW-008 AT-8O13 - One-Shot Sanitized Private Metadata Inspection Execution Plan 001

```text
UNIT=NW008_AT8O13_ONE_SHOT_SANITIZED_PRIVATE_METADATA_INSPECTION_EXECUTION_PLAN_001
PR_CLASS=planning_only
MODE=ONE_SHOT_PRIVATE_METADATA_INSPECTION_EXECUTION_PLAN_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

AUTHORIZATION_SUBJECT_UNIT=
NW008_AT8O12_PRIVATE_SOURCE_METADATA_INSPECTION_AUTHORIZATION_DECISION_001

AUTHORIZATION_SUBJECT_REVIEWED_HEAD=
6fa958e93de6de974e45e824b673077fbc124ed9

AUTHORIZATION_SUBJECT_MERGE_COMMIT=
c7bf51d45c293cd1249356c39b9f5d8adc9e8af8

AUTHORIZATION_EFFECTIVE=YES
AUTHORIZATION_STATE=AVAILABLE

MAX_INSPECTION_ATTEMPTS=1
INSPECTION_ATTEMPTS_USED=0
RETRY_AUTHORIZED=NO
AUTHORITY_REUSABLE=NO

INSPECTION_DISPATCHED=NO
PRIVATE_METADATA_INSPECTION_EXECUTED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0

INSPECTION_DISPATCH_DEFINITION=
FIRST_REQUEST_SENT_TO_AUTHORIZED_PRIVATE_SOURCE_FOR_ANY_AUTHORIZED_METADATA_FIELD

AUTHORITY_CONSUMPTION_TRIGGER=INSPECTION_DISPATCH
CURRENT_RESULT_STATE=NOT_EXECUTED
STOP_FOR_GOVERNANCE_REVIEW=YES
```

## 1. Purpose and execution boundary

AT8O13 defines the bounded execution plan for one future sanitized,
metadata-only inspection of the authorized private source. This artifact does
not dispatch or execute that inspection. It does not retrieve a private record,
create execution proof, implement an integration, or consume the available
authorization.

The plan is bound to the exact reviewed AT8O12 authorization head and merge
commit recorded above. A future executor must verify both bindings before any
dispatch. A mismatch must fail closed without dispatch and without consuming
the available attempt.

## 2. Authorized metadata allowlist

The authorized metadata allowlist is copied exactly from AT8O12:

```text
AUTHORIZED_METADATA_FIELDS=
source_class|
source_identifier_or_safe_alias|
operating_owner_role|
authority_status|
approval_status|
record_schema_version|
lifecycle_model_present|
provenance_model_present|
version_binding_model_present|
trust_model_present|
admissibility_model_present|
private_pii_processing_authority_status|
runtime_read_interface_present|
authentication_model_class|
authorization_model_class|
iam_dependency_class|
selected_system_of_record_status
```

No field outside this allowlist may be requested, observed, derived, returned,
logged, or included in future execution proof.

```text
SAFE_SOURCE_ALIAS_RULE=ONLY_CONNECTOR_SAFE_NON_PRINCIPAL_NON_SECRET_ALIAS_MAY_BE_RETURNED; OTHERWISE NOT_AUTHORIZED_TO_DISCLOSE
```

If a source identifier cannot be represented by the permitted safe alias, the
future execution must return `NOT_AUTHORIZED_TO_DISCLOSE` for that field. It
must not substitute, infer, hash, truncate, or otherwise transform a principal,
secret, or private identifier into an alias.

## 3. Forbidden fields and actions

The forbidden fields and actions are copied exactly from AT8O12:

```text
EXACT_HUMAN_PRINCIPAL=FORBIDDEN
PRINCIPAL_EMAIL=FORBIDDEN
PRINCIPAL_USER_ID=FORBIDDEN
AUTHORITY_RECORD_CONTENT=FORBIDDEN
CREDENTIALS=FORBIDDEN
TOKENS=FORBIDDEN
ADC_CONTENTS=FORBIDDEN
IAM_POLICY_BINDING_CONTENTS=FORBIDDEN
SECRETS=FORBIDDEN
PRIVATE_CUSTOMER_CONTACT_DATA=FORBIDDEN
IAM_MUTATION=FORBIDDEN
TOKEN_CREATOR_AUTHORIZATION=FORBIDDEN
SERVICE_ACCOUNT_IMPERSONATION=FORBIDDEN
MG_MCP_MUTATION=FORBIDDEN
DEPLOYMENT=FORBIDDEN
HIGHLEVEL_CALLS=FORBIDDEN
CRM_MUTATIONS=FORBIDDEN
```

Discovery of a request or response surface that would require or disclose a
forbidden field or action must fail closed. A forbidden value must never be
retrieved merely to redact it afterward.

## 4. One-shot dispatch and consumption model

```text
INSPECTION_DISPATCH_DEFINITION=
FIRST_REQUEST_SENT_TO_AUTHORIZED_PRIVATE_SOURCE_FOR_ANY_AUTHORIZED_METADATA_FIELD

AUTHORITY_CONSUMPTION_TRIGGER=INSPECTION_DISPATCH

IF INSPECTION_DISPATCHED=YES THEN
INSPECTION_ATTEMPTS_USED=1
AUTHORIZATION_STATE=CONSUMED
RETRY_AUTHORIZED=NO
```

Pre-dispatch validation does not consume the attempt when no request has been
sent to the authorized private source. Once dispatch occurs, the attempt and
authorization are consumed regardless of success, partial output, forbidden
field detection, source unavailability, or execution error. No retry,
continuation request, follow-up query, pagination request, or second source
request is authorized.

The future executor must construct one bounded request containing only the
authorized field names. It must validate that request locally before dispatch.
If the source cannot satisfy the request in one dispatch, execution must fail
closed rather than issue another request.

## 5. Required result vocabulary

The future execution result must use exactly one of these states:

```text
NOT_EXECUTED
SUCCESS_SANITIZED
PARTIAL_SANITIZED
FAIL_CLOSED_FORBIDDEN_FIELD
FAIL_CLOSED_SOURCE_UNAVAILABLE
FAIL_CLOSED_AUTHORIZATION_MISMATCH
FAIL_CLOSED_NO_SAFE_ALIAS
ERROR_CONSUMED
```

`NOT_EXECUTED` is the state of this planning-only unit. It is valid only before
dispatch. `SUCCESS_SANITIZED` means every returned value is within the
allowlist and sanitized. `PARTIAL_SANITIZED` means dispatch occurred but only a
sanitized subset of authorized fields was returned. Each `FAIL_CLOSED_*` state
identifies the corresponding bounded stop. `ERROR_CONSUMED` applies to any
post-dispatch error not represented by another result state.

Any result after dispatch must also satisfy the post-dispatch invariant in
Section 4.

## 6. Future execution procedure

Before dispatch, the future execution unit must:

1. Verify that the exact authorization reviewed head is
   `6fa958e93de6de974e45e824b673077fbc124ed9`.
2. Verify that the exact authorization merge commit is
   `c7bf51d45c293cd1249356c39b9f5d8adc9e8af8`.
3. Verify that the reviewed authorization head is an ancestor of the governing
   main branch and that the authorization state is `AVAILABLE`.
4. Verify that inspection attempts used is `0`, maximum inspection attempts is
   `1`, retry is not authorized, and authority is not reusable.
5. Build and locally validate one request containing only the exact authorized
   metadata field names.
6. Confirm that no request requires a forbidden field, forbidden action, exact
   principal, secret, credential, token, private record content, ADC content,
   or IAM policy binding content.
7. Confirm that the response path can retain only sanitized outputs and
   observed-versus-derived provenance.

Only a separately reviewed future execution unit may perform the first request.
At the instant that request is sent, it must atomically record dispatch,
consume the sole attempt, and transition authorization state to `CONSUMED`.
Response handling must reject non-allowlisted material without retaining or
reproducing it. No raw exact principal or private record content may enter the
execution proof.

## 7. Proof requirements for future execution

A separate future execution-proof artifact must record:

- exact authorization reviewed head;
- exact authorization merge commit;
- dispatch timestamp;
- result state;
- authorized field names requested;
- sanitized outputs only;
- observed versus derived provenance;
- no raw exact principal or private record content;
- authority-consumption state; and
- attempts used = 1 after dispatch.

These are requirements for future execution proof, not proof supplied by this
planning artifact. AT8O13 creates no execution proof.

## 8. Hard blocks during AT8O13

```text
INSPECTION_DISPATCH=BLOCKED
PRIVATE_RECORD_RETRIEVAL=BLOCKED
EXACT_HUMAN_PRINCIPAL_LOOKUP=BLOCKED
ADC_INSPECTION=BLOCKED
IAM_INSPECTION_OR_MUTATION=BLOCKED
TOKEN_CREATOR_AUTHORIZATION=BLOCKED
SERVICE_ACCOUNT_IMPERSONATION=BLOCKED
MG_MCP_MUTATION=BLOCKED
DEPLOYMENT=BLOCKED
HIGHLEVEL_CALL=BLOCKED
CRM_MUTATION=BLOCKED
```

AT8O13 is planning-only. No action in this unit may change
`INSPECTION_DISPATCHED=NO`, `INSPECTION_ATTEMPTS_USED=0`,
`AUTHORIZATION_STATE=AVAILABLE`, `PRIVATE_METADATA_INSPECTION_EXECUTED=NO`, or
`EXTERNAL_EFFECTS=0`.

## 9. Validation and stop state

Only this AT8O13 artifact may be staged. Repository validation is limited to
the required non-inspection checks:

```text
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

After validation and pull-request creation, this unit stops for governance
review. It does not execute inspection, create execution proof, or consume the
authorization.

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o13-one-shot-sanitized-private-metadata-inspection-execution-plan-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0
INSPECTION_DISPATCHED=NO
PRIVATE_METADATA_INSPECTION_EXECUTED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
AUTHORIZATION_STATE=AVAILABLE
INSPECTION_ATTEMPTS_USED=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```
