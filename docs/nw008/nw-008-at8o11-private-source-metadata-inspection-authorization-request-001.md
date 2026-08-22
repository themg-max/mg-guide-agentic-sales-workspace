# NW-008 AT-8O11 - Private Source Metadata Inspection Authorization Request 001

```text
UNIT=NW008_AT8O11_PRIVATE_SOURCE_METADATA_INSPECTION_AUTHORIZATION_REQUEST_001
PR_CLASS=planning_only
MODE=PRIVATE_METADATA_INSPECTION_AUTHORIZATION_REQUEST_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PREDECESSOR_UNIT=NW008_AT8O10_EXACT_RETRIEVAL_AND_PRIVATE_AUTHORITY_SOURCE_ACQUISITION_001
PREDECESSOR_REVIEWED_HEAD=95e341fc0eb546d959dd1444def0f8428e749714
PREDECESSOR_MERGE_COMMIT=9548d5d3149e72e2a224b240ac0cd88747e044dc
PREDECESSOR_REVIEWED_HEAD_ANCESTOR_OF_ORIGIN_MAIN=YES
PREDECESSOR_MERGE_COMMIT_ANCESTOR_OF_ORIGIN_MAIN=YES

REQUEST_PURPOSE=DEFINE_MINIMUM_SANITIZED_PRIVATE_SOURCE_METADATA_INSPECTION_REQUEST_TO_RESOLVE_AT8O10_UNKNOWNS
REQUESTED_SOURCE_CLASS=PRIVATE_SOURCE_METADATA
TARGET_SOURCE_CLASS=PRIVATE_SOURCE_METADATA
EVIDENCE_SOURCE_CLASS=DECISION_HISTORY

PREFERRED_OPTION=UNRESOLVED
FINAL_MECHANISM_SELECTION_DESIGNABLE=NO
OPTION_B_ADAPTER_PLACEMENT=UNKNOWN
OPTION_B_NEW_INFRASTRUCTURE_REQUIRED=UNKNOWN
OPTION_B_NEW_IAM_SURFACE_REQUIRED=UNKNOWN
OPTION_B_COMPLETE_AUTHORITY_RETRIEVAL_CONTRACT_FIT=UNKNOWN

PRIVATE_METADATA_INSPECTION_EXECUTED=NO
PRIVATE_METADATA_INSPECTION_AUTHORIZATION_GRANTED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_ARCHITECTURE_REVIEW=YES
```

## 1. Purpose and boundary

AT8O11 defines the smallest sanitized metadata-only inspection request needed to
resolve the remaining AT8O10 unknowns. It requests future human authorization
only. It does not grant inspection, does not execute inspection, and does not
select a human principal.

The request is limited to private-source metadata needed for governance and
authority-status evaluation. It explicitly excludes exact human-principal
values, authority-record content, credentials, tokens, ADC contents, IAM policy
binding contents, secrets, and private customer/contact values.

## 2. Requested authorization shape

```text
REQUEST_PURPOSE=RESOLVE_AT8O10_UNKNOWNS_WITH_SANITIZED_METADATA_ONLY
REQUESTED_SOURCE_CLASS=PRIVATE_SOURCE_METADATA
TARGET_SOURCE_CLASS=PRIVATE_SOURCE_METADATA
EVIDENCE_SOURCE_CLASS=DECISION_HISTORY
INSPECTION_ACTOR_CLASS=HUMAN_AUTHORIZED_METADATA_REVIEWER
HUMAN_APPROVAL_REQUIRED=YES
PRIVATE_METADATA_INSPECTION_EXECUTED=NO
PRIVATE_METADATA_INSPECTION_AUTHORIZATION_GRANTED=NO
```

The approval request is intentionally split from any public or approved-source
inspection posture. Public and approved-source inspection may be separately
authorized in the surrounding architecture, but that does not grant access to
the private remainder.

```text
AUTHORIZED_PUBLIC_AND_APPROVED_SOURCE_INSPECTION=YES
PRIVATE_REMAINDER_INSPECTION_AUTHORIZATION=NOT_AUTHORIZED_TO_INSPECT
```

## 3. Minimum sanitized metadata fields

```text
REQUESTED_METADATA_FIELDS=
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

These fields are sufficient to determine whether the private source can answer
the remaining AT8O10 questions without disclosing any exact human principal or
private record content.

## 4. Explicit exclusions

```text
EXPLICITLY_FORBIDDEN_FIELDS=
exact human principal|
principal email|
principal user id|
authority-record content|
credentials|
tokens|
ADC contents|
IAM policy binding contents|
secrets|
private customer values|
private contact values
```

No field in the request may be used as a backdoor for principal retrieval or
private authority-record reconstruction.

## 5. Sanitization and provenance rules

```text
RESULT_SANITIZATION_RULE=RETURN_SANITIZED_METADATA_ONLY; REDACT EXACT HUMAN PRINCIPAL, AUTHORITY-RECORD CONTENT, CREDENTIALS, TOKENS, ADC CONTENTS, IAM POLICY BINDINGS, SECRETS, AND PRIVATE CUSTOMER/CONTACT VALUES
RESULT_PROVENANCE_REQUIREMENTS=EACH RESULT MUST STATE SOURCE_CLASS, SOURCE_IDENTIFIER_OR_SAFE_ALIAS, AND WHETHER THE FIELD WAS OBSERVED DIRECTLY OR DERIVED
RESULT_AUTHORITY_STATUS_REQUIREMENTS=EACH RESULT MUST SEPARATELY STATE PUBLIC_OR_APPROVED_SOURCE_AUTHORIZATION AND PRIVATE_REMAINDER_AUTHORIZATION
```

The result must preserve the distinction between:

1. the source class being inspected;
2. the evidence source class used to justify the request; and
3. the authority status of the inspection itself.

## 6. Stop conditions and one-shot rule

```text
STOP_CONDITIONS=STOP_IF_ANY_FORBIDDEN_FIELD_WOULD_BE_EXPOSED|STOP_IF_EXACT_HUMAN_PRINCIPAL_IS_REQUIRED|STOP_BEFORE_PRIVATE_RETRIEVAL|STOP_BEFORE_AUTHORITY_RECORD_CONTENT
EXPIRATION_OR_ONE_SHOT_RULE=SINGLE_USE_REQUEST; EXPIRES_AFTER_ONE_APPROVED_METADATA_ONLY_INSPECTION_ATTEMPT_OR_REVIEW_CLOSEOUT
```

The request must fail closed if the target cannot be identified without exact
human-principal disclosure or if any non-sanitized private content would be
required.

## 7. Preserved AT8O10 states

```text
PREFERRED_OPTION=UNRESOLVED
FINAL_MECHANISM_SELECTION_DESIGNABLE=NO
OPTION_B_ADAPTER_PLACEMENT=UNKNOWN
OPTION_B_NEW_INFRASTRUCTURE_REQUIRED=UNKNOWN
OPTION_B_NEW_IAM_SURFACE_REQUIRED=UNKNOWN
OPTION_B_COMPLETE_AUTHORITY_RETRIEVAL_CONTRACT_FIT=UNKNOWN

PRIVATE_METADATA_INSPECTION_EXECUTED=NO
PRIVATE_METADATA_INSPECTION_AUTHORIZATION_GRANTED=NO
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

This artifact requests authority to inspect only sanitized metadata. It does
not change the architecture conclusion that the final Option B mechanism
selection is still not designable.

## 8. Validation and non-actions

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o11-private-source-metadata-inspection-authorization-request-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0
GOVERNANCE_AUTHORIZATION_CHANGES=0

GIT_DIFF_CHECK=PASS
PRIVATE_HUMAN_PRINCIPAL_MATERIAL_PRESENT=NO
PRIVATE_METADATA_INSPECTION_EXECUTED=NO
HUMAN_APPROVAL_REQUIRED=YES
```

No private metadata is inspected here. This file only defines the request that
would need separate human approval before any sanitized inspection can occur.
