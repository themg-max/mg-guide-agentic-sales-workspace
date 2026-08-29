# NW-008 AT1 GHL REST v3 Opportunity Read Diagnostic Authorization 001

## 1. Authorization identity and activation boundary

```text
AUTHORIZATION_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_AUTHORIZATION_001
CLASSIFICATION=AUTHORIZATION
PR_CLASS=AUTHORIZATION
MODE=AUTHORIZATION_DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw-008-at1-ghl-rest-v3-opportunity-read-diagnostic-authorization-001.md

PR290_MERGE_SHA=
  be6066d80632ea84544ee31853d5ec326664369b
PR290_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW
AUTHORIZATION_EFFECTIVE=NO
PROVIDER_CALL_AUTHORIZED_NOW=NO
SELF_ACTIVATION=FORBIDDEN

HIGHLEVEL_DIAGNOSTIC_AUTHORIZATION_READY_FOR_REVIEW=YES
```

This artifact defines a possible future one-read diagnostic lane. Creating,
reviewing, or merging it does not call HighLevel and does not itself authorize
a provider call. Future execution requires human review, merge, a human
countersignature, and a separate one-shot execution grant.

```text
HUMAN_REVIEW_REQUIRED=YES
MERGE_REQUIRED=YES
HUMAN_COUNTERSIGNATURE_REQUIRED=YES
SEPARATE_ONE_SHOT_EXECUTION_GRANT_REQUIRED=YES
MERGE_ALONE_AUTHORIZES_PROVIDER_CALL=NO
```

## 2. Exact future operation

```text
METHOD=GET
PATH=/opportunities/{private_validation_opportunity_id}

MAX_READS=1
MAX_WRITES=0
MAX_TOTAL_BUSINESS_CALLS=1

NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_ALTERNATE_TARGET=YES
NO_ALTERNATE_CREDENTIAL=YES
NO_ALTERNATE_OPERATION=YES

PRIVATE_VALIDATION_OPPORTUNITY_ID_SOURCE=
  SEPARATELY_BOUND_PRIVATE_EXECUTION_INPUT
CALLER_SELECTED_TARGET_ALLOWED=NO
CALLER_SELECTED_PATH_ALLOWED=NO
QUERY_PARAMETERS_ALLOWED=NO
REQUEST_BODY_ALLOWED=NO
```

The future grant may bind exactly one private synthetic validation opportunity
identifier. It may not expose a generic REST surface, substitute an identifier,
credential, route, operation, or account, or expand the one-call budget.

```text
IS_STAGE_GRANT_003=NO
STAGE_GRANT_AUTHORIZED=NO
STAGE_MUTATION_AUTHORIZED=NO
OPPORTUNITY_MUTATION_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
```

## 3. Private diagnostic persistence gate

The future execution must provide the complete bound sensitive-value inventory
before dispatch. A definitive non-2xx response may be projected publicly only
after private evidence has been persisted atomically and the persisted artifact
has been verified.

```text
PRIVATE_DIAGNOSTIC_PERSISTENCE_REQUIRED=YES
SENSITIVE_VALUE_INVENTORY_COMPLETE=YES
SENSITIVE_VALUE_INVENTORY_REQUIRED_BEFORE_DISPATCH=YES
PUBLIC_PROJECTION_BEFORE_VERIFIED_PERSISTENCE=FORBIDDEN
RAW_PROVIDER_RESPONSE_PUBLICATION=FORBIDDEN
PRIVATE_IDENTIFIER_PUBLICATION=FORBIDDEN
CREDENTIAL_PUBLICATION=FORBIDDEN
```

Normative definitive non-2xx sequence:

```text
DERIVE_PRIVATE_EVIDENCE
->
ATOMIC_PRIVATE_PERSISTENCE
->
VERIFY_PRIVATE_PERSISTENCE
->
PUBLIC_SAFE_PROJECTION
->
STOP
```

If atomic persistence or verification fails, execution must fail closed, publish
no private provider details, perform no retry, and stop without a second
provider call.

```text
PERSISTENCE_FAILURE_DISPOSITION=FAIL_CLOSED
PERSISTENCE_FAILURE_RETRY_ALLOWED=NO
PERSISTENCE_FAILURE_SECOND_PROVIDER_CALL_ALLOWED=NO
```

## 4. Runtime and offline cause-classification separation

Request execution is fact collection only. It may preserve the evidence-derived
cause value but must not interpret a provider message, code, or body to infer a
narrower cause while the request is executing.

```text
RUNTIME_CAUSE_INFERENCE_AUTHORIZED=NO
PROVIDER_ERROR_CAUSE_RUNTIME_VALUE=UNKNOWN
OFFLINE_PRIVATE_CAUSE_CLASSIFICATION_REQUIRED_AFTER_EXECUTION=YES
OFFLINE_CLASSIFICATION_MAY_TRIGGER_PROVIDER_CALL=NO
OFFLINE_CLASSIFICATION_MAY_PUBLISH_PRIVATE_VALUES=NO
```

Offline cause classification must occur only after the bounded execution has
stopped and only over the verified private diagnostic artifact. It does not
extend or reopen the one-read grant.

## 5. Explicit non-authority and unit attestations

```text
LIVE_GHL_CALLS=0
HIGHLEVEL_CALLS_IN_THIS_UNIT=0
HTTP_REQUEST_DISPATCHES_IN_THIS_UNIT=0
CRM_READS_IN_THIS_UNIT=0
CRM_WRITES_IN_THIS_UNIT=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
SECRET_MUTATIONS=0
PIT_ROTATIONS=0
GHL_SCOPE_EDITS=0

NO_HIGHLEVEL_CALL=YES
NO_IAM_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOY=YES
NO_SECRET_MUTATION=YES
NO_PIT_ROTATION=YES
NO_GHL_SCOPE_EDIT=YES
```

This artifact grants no service-account impersonation, token minting, Secret
Manager payload read, IAM mutation, runtime deployment, PIT rotation, OAuth
scope edit, opportunity mutation, stage mutation, note mutation, or other CRM
authority.

## 6. Future one-shot execution prerequisites

A future execution unit must stop unless it verifies all of the following:

```text
THIS_EXACT_ARTIFACT_HUMAN_REVIEWED=YES
THIS_EXACT_ARTIFACT_MERGED_TO_MAIN=YES
HUMAN_COUNTERSIGNATURE_DURABLE=YES
SEPARATE_ONE_SHOT_EXECUTION_GRANT_DURABLE=YES
PR290_REPAIR_DURABLE_ON_MAIN=YES
PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND=YES
PRIVATE_CREDENTIAL_BOUND=YES
SENSITIVE_VALUE_INVENTORY_COMPLETE=YES
PRIVATE_DIAGNOSTIC_DESTINATION_BOUND_AND_GITIGNORED=YES
```

The separate execution grant must freeze the exact reviewed artifact and
countersignature commits, private input sources, execution identity, credential
source, diagnostic destination, one-call budget, stop conditions, and
consumption record. No authority is reusable or transferable.

```text
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
EXECUTION_GRANT_REUSABLE=NO
EXECUTION_GRANT_CONSUMPTION_REQUIRED=YES

HIGHLEVEL_DIAGNOSTIC_AUTHORIZATION_READY_FOR_REVIEW=YES
```
