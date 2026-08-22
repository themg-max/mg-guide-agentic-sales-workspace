# NW-008 AT-8M2 — Offline Execution Store Substrate Final Reconciliation 001

```text
UNIT=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_FINAL_RECONCILIATION_001

PR_CLASS=proof_only
MODE=EVIDENCE_RECONCILIATION_ONLY
OWNER=VS_CODE_ORCHESTRATOR

PR122_INCLUDED=YES
PR123_INCLUDED=YES
PR124_INCLUDED=YES
PR125_INCLUDED=YES
PR126_INCLUDED=YES
PR127_INCLUDED=YES

PR127_REVIEWED_HEAD=28939140cf1f477c9a08bb49c1ceb7f41e1f36e9
PR127_MERGE_SHA=3f6c8566fcbb26fa81236c6a45f3cfb2766fb651
PR127_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES

OFFLINE_STORE_SUBSTRATE_IMPLEMENTED=YES
FAILED_INIT_REOPEN_REPAIR_COMPLETE=YES

PR125_SUPERSEDED_BY_PR127=YES
PR125_MERGE_REQUIRED=NO

PR124_AUTHORIZATION_CONSUMED=YES
PR124_AUTHORIZATION_REUSABLE=NO

PR126_AUTHORIZATION_CONSUMED=YES
PR126_AUTHORIZATION_REUSABLE=NO

SCHEMA_VERSION=1
FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED

REAL_SECRET_MANAGER_ACCESS=NO
REAL_COMMITMENT_KEY_READS=0
IAM_CHANGES=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
LIVE_PRODUCTION_STORE_ACTIVATION=NO
EXTERNAL_EFFECTS=0

NEXT_LANE=NW008_AT8O_PRODUCTION_RUNTIME_IDENTITY_MECHANISM_DESIGN_001

MG_MCP_NOTE=UNKNOWN: expected MG MCP context was not surfaced for AT8M2 closeout / PR127 / runtime identity - Action: run targeted search/alias/index validation for AT8M2 closeout / PR127 / runtime identity.
```

## 1. Reconciliation scope

This is a proof-only reconciliation artifact. It records the final evidence
state of the AT8M2 offline execution-store substrate lane after the PR127
failed-initialization reopen repair merged.

No source, test, governance authorization, IAM, Secret Manager, HighLevel, CRM,
deployment, or production runtime change is included.

## 2. PR chain summary

| PR  | Title | Role | State |
| --- | ----- | ---- | ----- |
| 122 | AT8M production-runtime substrate and execution-store authority design | design | merged |
| 123 | AT8M1 store schema and commitment-key versioning design | design | merged |
| 124 | AT8M2 offline execution-store substrate implementation authorization | authorization | merged, consumed |
| 125 | AT8M2 offline execution-store substrate implementation | implementation | merged, superseded by PR127 |
| 126 | AT8M2R1 failed-init reopen repair authorization | authorization | merged, consumed |
| 127 | AT8M2R1 fail closed on preexisting empty store reopen | repair | merged |

PR125 was merged before the failed-initialization reopen defect was identified.
PR126 authorized a bounded repair. PR127 implemented and completed the repair.
PR125 is superseded by PR127; no additional PR125 merge or amendment is required.

## 3. Implemented store invariants (post-PR127)

```text
SCHEMA_VERSION=1
FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED
ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
EXACT_COMMITMENT_KEY_VERSION_MATCHING=YES
NO_MIGRATION=YES
```

The store substrate is fully implemented with all required initialization
boundaries. Path preexistence is captured before `sqlite3.connect()` to
distinguish fresh initialization from preexisting empty or failed-init
artifacts.

## 4. Authorization consumption record

```text
PR124_AUTHORIZATION_CONSUMED=YES
PR124_AUTHORIZATION_REUSABLE=NO
PR124_RETRY_AFTER_CONSUMPTION_REQUIRES_NEW_AUTHORIZATION=YES

PR126_AUTHORIZATION_CONSUMED=YES
PR126_AUTHORIZATION_REUSABLE=NO
PR126_RETRY_AFTER_CONSUMPTION_REQUIRES_NEW_AUTHORIZATION=YES
```

Both one-shot authorizations have been consumed. No further mutations to the
AT8M2/AT8M2R1 authorized paths are permitted under these grants.

## 5. Deterministic proof coverage (post-PR127)

`tests/integrations/ghl/test_at1_commitment_key_provider.py` covers:

```text
- fresh non-existent store initialization allowed
- preexisting empty store (zero-byte and empty SQLite) fails closed
- failed-initialization artifact reopen fails closed
- atomic initialization rollback (no user tables remain)
- partial-schema store fails closed
- legacy unversioned store fails closed
- interrupted initialization reopen fails closed
- schema-v1 reopen with same version succeeds
- reopen with different commitment-key version fails closed
- missing/corrupt metadata fails closed
- unknown newer schema fails closed, no migration
- payload absent from SQLite dump
- provider-resolved material accepted; raw/provider/independent rejected
- no Secret Manager or external effect imports
```

## 6. What is not included

```text
REAL_SECRET_MANAGER_ACCESS=NO
REAL_COMMITMENT_KEY_READS=0
IAM_CHANGES=0
SERVICE_ACCOUNT_IMPERSONATION=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
LIVE_PRODUCTION_STORE_ACTIVATION=NO
PRODUCTION_COMPOSITION_ROOT_STORE_WIRING=NO
EXTERNAL_EFFECTS=0
```

Production runtime identity, IAM binding, real Secret Manager reads, HighLevel
integration, and live store activation are deferred to AT8O and subsequent
lanes.

## 7. Next lane

```text
NEXT_LANE=NW008_AT8O_PRODUCTION_RUNTIME_IDENTITY_MECHANISM_DESIGN_001
NEXT_LANE_TYPE=PLANNING_ONLY
NEXT_LANE_IMPLEMENTS_CODE=NO
```

AT8O will design the production runtime identity mechanism. It does not
implement code and requires a separate authorization before any implementation.
