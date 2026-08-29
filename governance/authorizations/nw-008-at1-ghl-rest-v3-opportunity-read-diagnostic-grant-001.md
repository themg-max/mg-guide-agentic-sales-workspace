# NW-008 AT1 GHL REST v3 Opportunity Read Diagnostic Grant 001

## 1. Grant identity and current state

```text
GRANT_ID=NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
ARTIFACT_PATH=
  governance/authorizations/nw-008-at1-ghl-rest-v3-opportunity-read-diagnostic-grant-001.md
CLASSIFICATION=ONE_SHOT_EXECUTION_GRANT
PR_CLASS=AUTHORIZATION
MODE=PROPOSED_GRANT_DEFINITION_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STATUS=
  PROPOSED_PENDING_INDEPENDENT_REVIEW_AND_HUMAN_EXECUTION_AUTHORITY
GRANT_EFFECTIVE=NO
PROVIDER_DISPATCH_AUTHORIZED_NOW=NO
HUMAN_FINALIZED_ACTIVATION_PRESENT=NO
HUMAN_FINALIZED_EXECUTION_WINDOW_PRESENT=NO
SELF_ACTIVATION=FORBIDDEN
DO_NOT_CALL_HIGHLEVEL_IN_THIS_UNIT=YES
```

This artifact defines the maximum bounds of a possible future one-shot
diagnostic read. It does not activate the grant, bind private values, invent an
execution window, consume the grant, or dispatch HighLevel. Dispatch requires
independent review and merge of this artifact plus later human-finalized
activation and window authority.

## 2. Durable authority chain

```text
PERSISTENCE_MERGE_SHA=
  be6066d80632ea84544ee31853d5ec326664369b
PERSISTENCE_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

AUTHORIZATION_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_AUTHORIZATION_001
AUTHORIZATION_MERGE_SHA=
  921be3108e184c8ecde3441aedcaba9bd3e5063e
AUTHORIZATION_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

COUNTERSIGNATURE_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_COUNTERSIGNATURE_001
COUNTERSIGNATURE_MERGE_SHA=
  64a716d016002a93a73d5d456b30a28aec173003
COUNTERSIGNATURE_BLOB_SHA=
  65e8cecc12c13bd4c5f6c7e8a7d8fc45c7db5cea
COUNTERSIGNATURE_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES
COUNTERSIGNATURE_BLOB_SHA_MATCH=YES
```

Any mismatch in this chain invalidates the grant and requires an immediate
stop without provider dispatch.

```text
IF_DURABLE_CHAIN_MISMATCH=
  GRANT_EFFECTIVE=NO
  PROVIDER_DISPATCH_AUTHORIZED=NO
  STOP
```

## 3. Exact operation and call budget

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

REQUEST_BODY_ALLOWED=NO
QUERY_PARAMETERS_ALLOWED=NO
CRM_MUTATION_AUTHORIZED=NO
STAGE_MUTATION_AUTHORIZED=NO
```

Timeout, disconnect, or ambiguous transport completion consumes the one-call
budget and must stop:

```text
AMBIGUOUS_COMPLETION_DISPOSITION=FAIL_AMBIGUOUS_READ
AMBIGUOUS_COMPLETION_RETRY_ALLOWED=NO
AMBIGUOUS_COMPLETION_SECOND_CALL_ALLOWED=NO
```

## 4. Fresh private activation preflight

The following are mandatory activation predicates. Each must be freshly
verified after this artifact is independently reviewed and merged and before
human-finalized activation permits dispatch:

```text
PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND=YES
PRIVATE_CREDENTIAL_SOURCE_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_GITIGNORED=YES
PRIVATE_DIAGNOSTIC_DESTINATION_CREATE_ONLY=YES

SENSITIVE_VALUE_INVENTORY_COMPLETE=FRESHLY_VERIFIED
```

These predicates are requirements, not claims about state observed while this
artifact was authored:

```text
PRIVATE_ACTIVATION_PREFLIGHT_EXECUTED_IN_THIS_UNIT=NO
PRIVATE_VALUES_RECORDED_IN_THIS_ARTIFACT=NO
FRESH_PRIVATE_PREFLIGHT_REQUIRED_BEFORE_DISPATCH=YES
```

The complete sensitive-value inventory must include:

```text
SENSITIVE_VALUE_INVENTORY=
  PIT|
  OPPORTUNITY_ID|
  LOCATION_ID|
  ALL_OTHER_PRIVATE_IDENTIFIERS_IN_RUNTIME_CONTEXT
```

No omitted, blank, stale, or unverified private value is acceptable. The
diagnostic destination must be inside the repository's designated private
boundary, gitignored, create-only, and capable of preserving atomic persistence
and mode `0600`.

## 5. Unique execution identity and consumption

The activation record must bind unique, safe values for:

```text
UNIQUE_GRANT_ID_BINDING_REQUIRED=YES
UNIQUE_RUN_ID_BINDING_REQUIRED=YES
UNIQUE_OPERATION_ID_BINDING_REQUIRED=YES

GRANT_ID_VALUE=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
RUN_ID_VALUE=HUMAN_FINALIZATION_REQUIRED_BEFORE_DISPATCH
OPERATION_ID_VALUE=nw008-at1-opportunity-read-diagnostic-001
```

The non-sensitive grant and operation identities are frozen here. The
run-specific identity is not invented in this artifact. Before dispatch, the
effective activation record must bind a fresh unique run identity, prove all
three bindings, and consume the exact grant identity durably.

```text
GRANT_CONSUMED_BEFORE_PROVIDER_DISPATCH=YES
GRANT_REUSABLE=NO
GRANT_TRANSFERABLE=NO
GRANT_CONSUMED_AT_AUTHORING=NO
SECOND_DISPATCH_AUTHORIZED=NO
```

## 6. Definitive non-2xx semantics

On a definitive non-2xx response:

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

```text
PRIVATE_DIAGNOSTIC_PERSISTENCE_REQUIRED=YES
PUBLIC_PROJECTION_BEFORE_VERIFIED_PERSISTENCE=FORBIDDEN
RAW_PROVIDER_VALUE_PUBLICATION=FORBIDDEN
DEFINITIVE_NON_2XX_RETRY_ALLOWED=NO
DEFINITIVE_NON_2XX_SECOND_PROVIDER_CALL_ALLOWED=NO
PERSISTENCE_FAILURE_DISPOSITION=FAIL_CLOSED
```

Provider cause must not be inferred during request execution. After execution,
offline private classification may inspect the persisted provider error code,
message, request ID, and correlation ID. Only a sanitized classification may be
returned for governance review.

```text
RUNTIME_CAUSE_INFERENCE_AUTHORIZED=NO
OFFLINE_CAUSE_CLASSIFICATION_REQUIRED_ON_DEFINITIVE_NON_2XX=YES
RAW_PRIVATE_CLASSIFICATION_INPUTS_PUBLICATION=FORBIDDEN
```

## 7. Activation and expiry rule

No authorization window is defined or inferred here.

```text
AUTHORIZATION_WINDOW_START_UTC=NOT_FINALIZED
AUTHORIZATION_WINDOW_END_UTC=NOT_FINALIZED
AUTHORIZATION_WINDOW_INVENTED_BY_THIS_ARTIFACT=NO

INDEPENDENT_REVIEW_REQUIRED=YES
GRANT_MERGE_REQUIRED=YES
HUMAN_FINALIZED_ACTIVATION_REQUIRED=YES
HUMAN_FINALIZED_WINDOW_REQUIRED=YES
CURRENT_TIME_INSIDE_FINALIZED_WINDOW_REQUIRED=YES
```

If any activation predicate is absent, false, stale, ambiguous, or outside the
human-finalized window:

```text
GRANT_EFFECTIVE=NO
PROVIDER_DISPATCH_AUTHORIZED=NO
GRANT_REUSE_AUTHORIZED=NO
STOP
```

## 8. Unit attestations

```text
LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
SECRET_MUTATIONS=0
PIT_ROTATIONS=0
GHL_SCOPE_EDITS=0

NO_HIGHLEVEL_CALL=YES
NO_IAM_MUTATION=YES
NO_AGENT_RUNTIME_DEPLOYMENT=YES
NO_SECRET_MUTATION=YES
NO_PIT_ROTATION=YES
NO_GHL_SCOPE_EDIT=YES
```
