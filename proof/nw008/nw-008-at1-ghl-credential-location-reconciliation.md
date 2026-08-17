# NW-008 AT-1 -- GHL Credential / Location Reconciliation (Track A)

```text
CHECK_ID=NW008_AT1_GHL_CREDENTIAL_LOCATION_RECON_005
ARTIFACT_KIND=CREDENTIAL_LOCATION_RECONCILIATION
OWNER_LANE=VS Code / Orchestrator + Human GHL Space Owner
BRANCH=impl/nw008-at1-safe-environment-readiness
RECORDED_AT_UTC=2026-08-17T09:39:50Z

RESULT_002_COMMIT_SHA=897db6e74f1d022260d385a4852269a7bb1d1a49
RESULT_002_COMMIT_TIME_UTC=2026-08-17T00:51:20Z
RESULT_004_SHA=b641e1dc87b4a00c46c716b977b1918c1cf7e56c
GRANT_004_STATE=CLOSED_FAIL_CLOSED
GRANT_004_STOP_CODE=GRANT004_GET_PIPELINES_LOCATION_TOKEN_ACCESS_DENIED
```

Purpose: determine whether Grant 004 failed because the GHL PIT changed after
Result 002 or because the NW-008 private location binding does not match the
token-accessible synthetic opportunity location. This reconciliation executed
**zero GHL business calls**, printed **no token value**, changed **no
credentials**, and published **no private IDs**.

## Phase A -- Secret version metadata only

```text
SECRET_NAME=GHL_MCP_PRIVATE_TOKEN
SECRET_PROJECT=ai-rolodex-to-crm
SECRET_VALUE_PUBLICATION=NO

SECRET_VERSION_METADATA_VERIFIED=YES
SECRET_VERSION_COUNT=1
LATEST_VERSION_STATE=ENABLED
LATEST_VERSION_CREATED_AFTER_RESULT_002=NO
SECRET_CHANGED_AFTER_RESULT_002=NO
```

Method: `gcloud secrets versions list` (metadata only: version identifier,
state, createTime). The secret has exactly one enabled version whose createTime
predates the Result 002 commit (2026-08-17T00:51:20Z) by approximately five
months. Secret Manager versions are immutable; any PIT change after Result 002
would have required a new version. No version was added, destroyed, disabled,
or rotated, and no IAM modification was performed. The secret payload was never
accessed or printed.

## Phase B -- Private location reconciliation

```text
RESULT002_PRIVATE_LOCATION_RECOVERED=NO
NW008_PRIVATE_LOCATION_PRESENT=YES
LOCATION_BINDING_MATCH=UNKNOWN
```

Method and findings (private values never printed or committed):

1. `NW008_GHL_LOCATION_PRIVATE_V1` was loaded privately from the canonical
   NW-013 synthetic record binding control-plane file (the same source used by
   Grant 002 and Grant 004). Presence confirmed; value not printed.
2. Result 002's private observed opportunity `locationId` could **not** be
   recovered from any durable evidence. The Result 002 execution session log
   (and all other candidate session logs, session databases, checkpoints, and
   temporary directories) contain only a redacted placeholder (`<ID>`) where
   the live `locationId` was captured; the value was scrubbed at capture time
   per the no-private-IDs-in-logs discipline. Result 002's public artifact
   records only `LOCATION_ID_PRESENT=YES` and
   `LOCATION_ID_MATCHES_CONTACT_LOCATION=YES`, not the value itself.
3. Because the Result 002 private location cannot be recovered, the binding
   comparison cannot be performed. Per instructions, no value was guessed:
   `LOCATION_BINDING_MATCH=UNKNOWN`.

## Public checkpoint

```text
CHECK_ID=NW008_AT1_GHL_CREDENTIAL_LOCATION_RECON_005

SECRET_NAME=GHL_MCP_PRIVATE_TOKEN
SECRET_VALUE_PUBLICATION=NO

SECRET_VERSION_METADATA_VERIFIED=YES
SECRET_CHANGED_AFTER_RESULT_002=NO

RESULT002_PRIVATE_LOCATION_RECOVERED=NO
NW008_PRIVATE_LOCATION_PRESENT=YES
LOCATION_BINDING_MATCH=UNKNOWN

CURRENT_PIT_EXACT_OPPORTUNITY_ACCESS=NOT_TESTED

CREDENTIAL_CHANGE_AUTHORIZED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Decision

```text
LOCATION_BINDING_MATCH=UNKNOWN
NEXT=PREPARE_ONE_EXACT_OPPORTUNITY_DIAGNOSTIC_GRANT_005
```

Rationale: the PIT did **not** change after Result 002
(`SECRET_CHANGED_AFTER_RESULT_002=NO`), so a credential change is excluded as
the Grant 004 failure cause. The location-binding hypothesis cannot be
confirmed or refuted because Result 002's private observed location value was
redacted at capture time and is unrecoverable without a fresh read. Per the
UNKNOWN branch, the next step is to prepare (not execute) a single
exact-opportunity diagnostic grant 005 that re-reads the synthetic opportunity
to privately re-establish the token-accessible location for comparison against
`NW008_GHL_LOCATION_PRIVATE_V1`.

## Explicit non-actions

```text
DID_NOT_EXECUTE_GHL_BUSINESS_CALL=YES
DID_NOT_EXECUTE_GET_PIPELINES=YES
DID_NOT_PRINT_TOKEN=YES
DID_NOT_ACCESS_SECRET_PAYLOAD=YES
DID_NOT_ROTATE_SECRET=YES
DID_NOT_ADD_SECRET_VERSION=YES
DID_NOT_DESTROY_OR_DISABLE_SECRET_VERSION=YES
DID_NOT_MODIFY_IAM=YES
DID_NOT_CHANGE_CREDENTIALS=YES
DID_NOT_PUBLISH_PRIVATE_IDS=YES
DID_NOT_GUESS_LOCATION_BINDING=YES
DID_NOT_EXECUTE_GRANT_005=YES
DID_NOT_AUTHORIZE_AT1_EXECUTION=YES
DID_NOT_CLAIM_ENVIRONMENT_READY=YES
```

## STOP

```text
STOP_CODE=NW008_AT1_CREDENTIAL_LOCATION_RECON_BINDING_UNKNOWN
RESULT=RECONCILIATION_COMPLETE_BINDING_UNKNOWN
SECRET_CHANGED_AFTER_RESULT_002=NO
RESULT002_PRIVATE_LOCATION_RECOVERED=NO
LOCATION_BINDING_MATCH=UNKNOWN
CREDENTIAL_CHANGE_AUTHORIZED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=PREPARE_ONE_EXACT_OPPORTUNITY_DIAGNOSTIC_GRANT_005
```
