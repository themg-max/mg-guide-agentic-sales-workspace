# NW-008 AT1 GHL REST v3 Opportunity Read Diagnostic Activation Private Preflight Rerun 001

## 1. Artifact identity and source authority

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_ACTIVATION_PRIVATE_PREFLIGHT_RERUN_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-opportunity-read-diagnostic-activation-private-preflight-rerun-001.md
ARTIFACT_KIND=SANITIZED_NON_CONSUMING_PRIVATE_ACTIVATION_PREFLIGHT_RERUN
PR_CLASS=proof_only
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BRANCH=
  proof/nw008-at1-ghl-rest-v3-opportunity-read-diagnostic-activation-private-preflight-rerun-001
BRANCH_IS_MAIN=NO
LOCAL_WORKTREE_PATH_PUBLISHED=NO
PRIVATE_PACKAGE_PATH_PUBLISHED=NO
PRIVATE_SOURCE_PATHS_PUBLISHED=NO

SOURCE_PR=298
SOURCE_PR298_MERGE_SHA=
  d7777f0e4c14006dcdeb5c665eda5d1fffcfc6b0
SOURCE_PR298_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES
SOURCE_PR298_PROOF_BLOB_SHA=
  9cbc905dadc6e78788bb310b218b89b4948701a9

SOURCE_GRANT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
OPERATION_ID=nw008-at1-opportunity-read-diagnostic-001
```

This proof records one exact-path rerun after materialization of one fresh
gitignored private activation-binding package. It contains no private values,
value fragments, private source paths, or package content.

## 2. Private package materialization

```text
PRIVATE_PACKAGE_CREATED=YES
PRIVATE_PACKAGE_COUNT_CREATED_BY_THIS_UNIT=1
PRIVATE_PACKAGE_LOCATION_CLASS=
  DETERMINISTIC_EXPECTED_REPOSITORY_LOCAL_GITIGNORED_PATH
PRIVATE_PACKAGE_EXPECTED_LOCATION_MATCH=YES
PRIVATE_PACKAGE_DISCOVERED_BY_BROAD_SCAN=NO

PRIVATE_PACKAGE_SCHEMA_VERSION_PRESENT=YES
PRIVATE_PACKAGE_SCHEMA_VERSION_MATCH=YES
PRIVATE_PACKAGE_CREATED_AT_PRESENT=YES
PRIVATE_PACKAGE_FRESH_AT_VERIFICATION=YES

PRIVATE_PACKAGE_GITIGNORED=YES
PRIVATE_PACKAGE_CREATE_ONLY=YES
PRIVATE_PACKAGE_OVERWRITE_ALLOWED=NO
PRIVATE_PACKAGE_MODE_0600=YES
PRIVATE_PACKAGE_REGULAR_FILE=YES
PRIVATE_PACKAGE_SYMLINK=NO

EXACT_GRANT_MATCH=YES
EXACT_OPERATION_MATCH=YES
```

Create-only behavior was verified by an exclusive-create probe against the
already-created exact package. The probe received the expected exists
condition, performed no overwrite, and did not alter package content.

## 3. Category-level binding and provenance classification

The fresh package binds the exact current grant and operation. Sensitive values
remain exclusively inside the gitignored private package.

| Required private category | Result | Sanitized basis |
| --- | --- | --- |
| `PRIVATE_VALIDATION_OPPORTUNITY_ID` | PASS | Nonblank authoritative sources agreed exactly; the fresh package binds the value to this grant and operation. |
| `LOCATION_ID` | PASS | Nonblank authoritative sources agreed exactly; the fresh package binds the value to this grant and operation. |
| `EXACT_SEALED_CREDENTIAL_SOURCE` | PASS | The package binds the repository-owned exact sealed credential source; no payload was accessed. |
| `PIT_INVENTORY_CATEGORY` | PASS | Inventory uses the exact sealed credential source, copies no historical PIT, and performs no payload read. |
| `ALL_OTHER_PRIVATE_IDENTIFIERS_REQUIRED_BY_FINAL_GET_RUNTIME_CONTEXT` | PASS | The exact GET context inventory was evaluated and marked complete; no additional private identifier category was required. |
| `BINDING_PROVENANCE` | PASS | Current-source observation, current grant/operation binding, nonblank state, no alternate value, exact cross-source agreement, and freshness were recorded privately. |

```text
PRIVATE_VALUES_PUBLISHED=NO
PRIVATE_VALUE_FRAGMENTS_PUBLISHED=NO
PRIVATE_VALUE_DIGESTS_PUBLISHED=NO
HISTORICAL_PACKAGE_ACCEPTED_AS_CURRENT_BINDING=NO
HISTORICAL_PIT_COPIED=NO
SECRET_MANAGER_PAYLOAD_READS=0

OPPORTUNITY_SOURCE_NONBLANK=YES
OPPORTUNITY_AUTHORITATIVE_SOURCES_EXACT_MATCH=YES
LOCATION_SOURCE_NONBLANK=YES
LOCATION_AUTHORITATIVE_SOURCES_EXACT_MATCH=YES
ALTERNATE_PRIVATE_VALUE_DETECTED=NO
BINDING_PROVENANCE_COMPLETE=YES
```

Historical packages were not accepted as the active package. This unit created
a new package with a new schema, fresh creation time, exact current grant and
operation bindings, and separately recorded source provenance.

## 4. Six mandatory predicate results

```text
PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND=YES
PRIVATE_CREDENTIAL_SOURCE_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_GITIGNORED=YES
PRIVATE_DIAGNOSTIC_DESTINATION_CREATE_ONLY=YES
SENSITIVE_VALUE_INVENTORY_COMPLETE=YES
```

Supporting diagnostic safety gates remain satisfied:

```text
PRIVATE_DIAGNOSTIC_ATOMIC_PERSISTENCE_READY=YES
PRIVATE_DIAGNOSTIC_MODE_0600_READY=YES
VERIFIED_PRIVATE_PERSISTENCE_BEFORE_PUBLIC_SAFE_PROJECTION=YES
PUBLIC_SAFE_PROJECTION_BEFORE_VERIFIED_PRIVATE_PERSISTENCE=FORBIDDEN
```

## 5. Non-consuming activation state

```text
RUN_ID=HUMAN_FINALIZATION_REQUIRED
RUN_ID_FINALIZED=NO
RUN_ID_INVENTED=NO

AUTHORIZATION_WINDOW_START_UTC=HUMAN_FINALIZATION_REQUIRED
AUTHORIZATION_WINDOW_END_UTC=HUMAN_FINALIZATION_REQUIRED
EXECUTION_WINDOW_FINALIZED=NO
EXECUTION_WINDOW_INVENTED=NO

GRANT_CONSUMED=NO
GRANT_CONSUMPTION_ATTEMPTS=0
PROVIDER_DISPATCH_AUTHORIZED_BY_THIS_UNIT=NO
```

## 6. Zero-effect ledger

```text
LIVE_GHL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_READS=0
CRM_WRITES=0
STAGE_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MANAGER_PAYLOAD_READS=0
SECRET_MUTATIONS=0
PIT_ROTATIONS=0
GHL_SCOPE_EDITS=0

ALTERNATE_TARGETS_USED=0
ALTERNATE_CREDENTIALS_USED=0
ALTERNATE_OPERATIONS_USED=0
```

No HighLevel request, CRM read or write, stage change, credential payload read,
grant consumption, PIT rotation, GHL scope change, or IAM mutation occurred.

## 7. Deterministic verification

The rerun read only the deterministic expected package location. It did not
repeat broad private-tree discovery.

```text
EXACT_PACKAGE_PATH_VERIFIER=PASS
PACKAGE_SCHEMA_AND_IDENTITY=PASS
PACKAGE_PROVENANCE_AND_FRESHNESS=PASS
PACKAGE_MODE_AND_CREATE_ONLY_SAFETY=PASS
PACKAGE_ABSENT_FROM_GIT_STATUS=PASS

PREFLIGHT_SAFETY_TEST_COMMAND=
  ./.venv-test/bin/python -m pytest -q
  tests/integrations/ghl/highlevel_rest/test_private_provider_diagnostic_persistence.py
  tests/integrations/ghl/highlevel_rest/test_pit_subaccount_binding_validation.py
  tests/integrations/ghl/highlevel_rest/test_provider_error_evidence.py
  tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py
PREFLIGHT_SAFETY_TEST_RESULT=PASS
PREFLIGHT_SAFETY_TESTS_PASSED=55

PHASE1_DETERMINISTIC_VERIFICATION_SCRIPT=PASS
FULL_PYTEST=PASS
```

## 8. Final disposition

```text
HIGHLEVEL_PREFLIGHT_STATUS=PREFLIGHT_READY_FOR_HUMAN_ACTIVATION
PREFLIGHT_READY_FOR_HUMAN_ACTIVATION=YES
BLOCKERS=NONE

NEXT=RETURN_FOR_HUMAN_FINALIZED_ONE_SHOT_ACTIVATION
```

This readiness result does not activate the grant. A later explicit human act
must finalize the unique `RUN_ID` and execution window. The GET remains
forbidden until that later act is complete and all durable gates are rechecked.
