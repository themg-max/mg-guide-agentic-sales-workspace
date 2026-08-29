# NW-008 AT1 GHL REST v3 Opportunity Read Diagnostic Activation Private Preflight 001

## 1. Artifact identity and source authority

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_ACTIVATION_PRIVATE_PREFLIGHT_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-opportunity-read-diagnostic-activation-private-preflight-001.md
ARTIFACT_KIND=SANITIZED_NON_CONSUMING_PRIVATE_ACTIVATION_PREFLIGHT
PR_CLASS=proof_only
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BRANCH=
  proof/nw008-at1-ghl-rest-v3-opportunity-read-diagnostic-activation-private-preflight-001
BRANCH_IS_MAIN=NO
LOCAL_WORKTREE_PATH_PUBLISHED=NO
OPERATOR_USERNAME_PUBLISHED=NO
WORKSTATION_PATH_PUBLISHED=NO

RECORDED_AT_LOCAL=2026-08-29T10:09:24.572-04:00
RECORDED_AT_UTC=2026-08-29T14:09:24.572Z

SOURCE_MAIN_COMMIT=
  ce4aaaa8a5bd3663248b00f42db913287d539301
SOURCE_GRANT_MERGE_SHA=
  5f70f764d23c21019a84c55048ba18ce2bf038a1
SOURCE_GRANT_BLOB_SHA=
  a2132196c91bea79ea08c390712e171f4167a691
SOURCE_GRANT_PRESENT_ON_MAIN=YES
SOURCE_GRANT_MERGE_SHA_PRESENT_ON_MAIN=YES

SOURCE_GRANT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
```

This preflight inspected the merged grant, repository-owned credential and
diagnostic-persistence boundaries, and existing gitignored private metadata
without reading or publishing raw values. It did not resolve ADC, impersonate a
service account, access Secret Manager, consume the grant, or dispatch a
provider request.

## 2. Frozen non-sensitive operation identity

```text
GRANT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
GRANT_ID_MATCH=YES

OPERATION_ID=nw008-at1-opportunity-read-diagnostic-001
OPERATION_ID_MATCH=YES

RUN_ID=HUMAN_FINALIZATION_REQUIRED
RUN_ID_FINALIZED=NO
RUN_ID_INVENTED=NO

AUTHORIZATION_WINDOW_START_UTC=HUMAN_FINALIZATION_REQUIRED
AUTHORIZATION_WINDOW_END_UTC=HUMAN_FINALIZATION_REQUIRED
EXECUTION_WINDOW_FINALIZED=NO
EXECUTION_WINDOW_INVENTED=NO
```

## 3. Fresh private metadata inspection

The existing designated gitignored private metadata boundary was scanned using
key names and fixed grant/operation identifiers only. Values, fragments,
digests of values, and private file paths discovered during that metadata scan
were not emitted into this public proof.

```text
PRIVATE_METADATA_SCAN=PASS
PRIVATE_METADATA_FILES_SCANNED=9148
RAW_PRIVATE_VALUES_EMITTED=NO
PRIVATE_FILE_PATHS_RECORDED=NO
PRIVATE_FILE_PATHS_RECORDED_SCOPE=
  PATHS_DISCOVERED_DURING_PRIVATE_METADATA_SCAN
PRIVATE_FILE_PATHS_RECORDED_DOES_NOT_NEGATE=
  INTENTIONAL_NON_SECRET_REPOSITORY_DESTINATION_CONVENTION

CURRENT_GRANT_REFERENCE_FILES=0
CURRENT_OPERATION_REFERENCE_FILES=0
CURRENT_GRANT_COMPLETE_BINDING_FILES=0
```

`PRIVATE_FILE_PATHS_RECORDED=NO` means no private filesystem paths found by the
metadata scan were published here. It does **not** mean the intentional
non-secret repository destination convention in section 6 is unpublished; that
relative destination remains a repository-owned, gitignored public convention.

Historical private packages containing opportunity, location, or credential
metadata were not accepted as current bindings because none was bound to this
grant ID or operation ID. Reuse or inference from a prior execution lane is
forbidden.

## 4. Mandatory predicate classification

| Mandatory predicate | Result | Non-secret basis |
| --- | --- | --- |
| `PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND` | FAIL | No existing private package references the current grant or operation; no current opportunity binding can be verified. |
| `PRIVATE_CREDENTIAL_SOURCE_BOUND` | PASS | Repository-owned composition seals one exact Secret Manager version resource through the exact target-runtime credential injection; equality and no-environment/no-shell discovery checks passed without access. |
| `PRIVATE_DIAGNOSTIC_DESTINATION_BOUND` | PASS | The exact repository-local private provider-diagnostic destination was selected and committed below. |
| `PRIVATE_DIAGNOSTIC_DESTINATION_GITIGNORED` | PASS | `git check-ignore` accepted the exact relative destination under the repository-wide `local/` rule. |
| `PRIVATE_DIAGNOSTIC_DESTINATION_CREATE_ONLY` | PASS | Destination probe was absent and the persistence implementation's exclusive-create/never-overwrite tests passed. |
| `SENSITIVE_VALUE_INVENTORY_COMPLETE` | FAIL | No current-grant private package exists, so PIT, opportunity ID, location ID, and all remaining runtime-private identifiers cannot be proven complete as one fresh inventory. |

Normalized required return values:

```text
PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND=NO
PRIVATE_CREDENTIAL_SOURCE_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_BOUND=YES
PRIVATE_DIAGNOSTIC_DESTINATION_GITIGNORED=YES
PRIVATE_DIAGNOSTIC_DESTINATION_CREATE_ONLY=YES
SENSITIVE_VALUE_INVENTORY_COMPLETE=NO
```

## 5. Sensitive-value inventory coverage

Only category coverage was inspected. No actual value was read into this
artifact.

| Required category | Result | Reason |
| --- | --- | --- |
| PIT | FAIL | Exact credential source is sealed, but no fresh current-grant private inventory entry was available for comparison at preflight. |
| Opportunity ID | FAIL | No current-grant/current-operation private binding exists. |
| Location ID | FAIL | Historical location metadata is not a fresh binding to this grant. |
| All other private identifiers in runtime context | UNKNOWN | No current-grant runtime-context inventory exists from which completeness can be established. |

```text
PIT_INVENTORY_COVERAGE=FAIL
OPPORTUNITY_ID_INVENTORY_COVERAGE=FAIL
LOCATION_ID_INVENTORY_COVERAGE=FAIL
ALL_OTHER_PRIVATE_IDENTIFIERS_IN_RUNTIME_CONTEXT_COVERAGE=UNKNOWN

RAW_PIT_RECORDED=NO
RAW_OPPORTUNITY_ID_RECORDED=NO
RAW_LOCATION_ID_RECORDED=NO
RAW_OTHER_PRIVATE_IDENTIFIER_RECORDED=NO
```

Any failed or unknown inventory category makes
`SENSITIVE_VALUE_INVENTORY_COMPLETE=NO`.

## 6. Private diagnostic destination safety

The destination is a non-secret repository convention already present in the
merged persistence design and tests:

```text
PRIVATE_DIAGNOSTIC_DESTINATION_CLASS=
  REPOSITORY_LOCAL_PRIVATE_PROVIDER_DIAGNOSTICS
PRIVATE_DIAGNOSTIC_DESTINATION_RELATIVE=
  local/private/provider-diagnostics
PRIVATE_DIAGNOSTIC_DESTINATION_COMMITMENT_SHA256=
  26781aa5f2619f9bb4ffa3f43d6f660fe131e4cac61c617525958b06e88f6b57

PRIVATE_DIAGNOSTIC_DESTINATION_WITHIN_REPOSITORY=PASS
PRIVATE_DIAGNOSTIC_DESTINATION_GITIGNORED=PASS
PRIVATE_DIAGNOSTIC_DESTINATION_CREATE_ONLY=PASS
PRIVATE_DIAGNOSTIC_ATOMIC_PERSISTENCE_READY=PASS
PRIVATE_DIAGNOSTIC_MODE_0600_READY=PASS
PRIVATE_DIAGNOSTIC_TEMPORARY_FILE_CLEANUP_READY=PASS
PRIVATE_DIAGNOSTIC_DIRECTORY_FSYNC_READY=PASS
```

The merged concrete implementation uses exclusive creation, no-follow where
available, mode `0600`, file and directory `fsync`, same-directory hard-link
publication, create-only destination semantics, content verification, and
temporary cleanup.

Projection ordering was validated:

```text
PRIVATE_EVIDENCE_DERIVATION_BEFORE_PERSISTENCE=PASS
ATOMIC_PRIVATE_PERSISTENCE_BEFORE_VERIFICATION=PASS
VERIFIED_PRIVATE_PERSISTENCE_BEFORE_PUBLIC_SAFE_PROJECTION=PASS
PUBLIC_SAFE_PROJECTION_BEFORE_VERIFIED_PRIVATE_PERSISTENCE=FORBIDDEN
PERSISTENCE_FAILURE_DISPOSITION=FAIL_CLOSED
```

## 7. Deterministic validation evidence

```text
PERSISTENCE_AND_PROJECTION_TEST_COMMAND=
  ./.venv-test/bin/python -m pytest -q
  tests/integrations/ghl/highlevel_rest/test_private_provider_diagnostic_persistence.py
  tests/integrations/ghl/highlevel_rest/test_pit_subaccount_binding_validation.py
  tests/integrations/ghl/highlevel_rest/test_provider_error_evidence.py
PERSISTENCE_AND_PROJECTION_TEST_RESULT=PASS
PERSISTENCE_AND_PROJECTION_TESTS_PASSED=35

CREDENTIAL_PROVIDER_TEST_COMMAND=
  ./.venv-test/bin/python -m pytest -q
  tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py
CREDENTIAL_PROVIDER_TEST_RESULT=PASS
CREDENTIAL_PROVIDER_TESTS_PASSED=20

HIGHLEVEL_REST_TRUST_BOUNDARY_TEST_RESULT=PASS
SEALED_CREDENTIAL_RESOURCE_MATCH=YES
CREDENTIAL_PROVIDER_ENV_DISCOVERY_DISABLED=YES
CREDENTIAL_PROVIDER_SHELL_ACCESS_DISABLED=YES

PHASE1_DETERMINISTIC_VERIFICATION_SCRIPT=PASS
FULL_PYTEST=PASS
```

## 8. Zero-effect and consumption ledger

```text
GRANT_CONSUMED=NO
GRANT_CONSUMPTION_ATTEMPTS=0
PROVIDER_DISPATCH_AUTHORIZED=NO

LIVE_GHL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_READS=0
CRM_WRITES=0
IAM_MUTATIONS=0
SECRET_MANAGER_PAYLOAD_READS=0
SECRET_MUTATIONS=0
PIT_ROTATIONS=0
GHL_SCOPE_EDITS=0

NO_ALTERNATE_TARGET=YES
NO_ALTERNATE_CREDENTIAL=YES
NO_ALTERNATE_OPERATION=YES
```

## 9. Final disposition and blockers

```text
HIGHLEVEL_PREFLIGHT_STATUS=PREFLIGHT_BLOCKED
PREFLIGHT_READY_FOR_HUMAN_ACTIVATION=NO
```

Blocking predicates:

```text
BLOCKER_1=
  PRIVATE_VALIDATION_OPPORTUNITY_ID_BOUND=FAIL
BLOCKER_2=
  SENSITIVE_VALUE_INVENTORY_COMPLETE=FAIL
BLOCKER_2_DETAIL=
  PIT=FAIL|
  OPPORTUNITY_ID=FAIL|
  LOCATION_ID=FAIL|
  ALL_OTHER_PRIVATE_IDENTIFIERS_IN_RUNTIME_CONTEXT=UNKNOWN
```

Smallest safe remediation:

1. The private control plane must create one fresh gitignored activation package
   bound to the exact grant ID and operation ID in this artifact.
2. That package must privately bind the validation opportunity ID and location
   ID, bind the sealed credential source, and enumerate PIT plus every other
   private identifier present in the final runtime context.
3. The verifier must rerun this non-consuming preflight and obtain PASS for all
   six mandatory predicates without publishing values.
4. `RUN_ID` and the authorization window must remain
   `HUMAN_FINALIZATION_REQUIRED` until a later explicit human activation act.

```text
BLOCKERS=
  PRIVATE_VALIDATION_OPPORTUNITY_ID_NOT_BOUND_TO_CURRENT_GRANT_OR_OPERATION|
  CURRENT_GRANT_SENSITIVE_VALUE_INVENTORY_INCOMPLETE

NEXT=REMEDIATE_PREFLIGHT_ONLY
```
