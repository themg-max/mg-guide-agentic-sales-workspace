# NW-008 AT-8M2R1 — Failed-Init Reopen Repair Proof 001

```text
UNIT=NW008_AT8M2R1_OFFLINE_EXECUTION_STORE_FAILED_INIT_REOPEN_REPAIR_001
PROOF_CLASS=offline_deterministic
EXTERNAL_EFFECTS=0
SECRET_MANAGER_ACCESS=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
```

## Required repair proofs

```text
1. FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED
   test_new_store_initializes_schema_v1_atomically
   test_at8m2r1_repair_has_no_secret_manager_or_external_effects (fresh path)

2. PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
   test_preexisting_empty_store_fails_closed
     - zero-byte preexisting path
     - preexisting empty SQLite file (TABLE_COUNT=0)

3. ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
   test_atomic_initialization_failure_rolls_back_all_schema
     - injected broken DDL raises ExecutionStoreSchemaError
     - no user tables remain after rollback

4. FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
   test_atomic_initialization_failure_rolls_back_all_schema (reopen clause)
   test_failed_initialization_artifact_reopen_fails_closed
     - does not delete or recreate the failed artifact
     - subsequent open refuses preexisting empty artifact

5. PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
   test_partial_schema_store_fails_closed
   test_interrupted_initialization_reopen_fails_closed

6. LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
   test_legacy_unversioned_store_fails_closed

7. NO_SECRET_MANAGER_ACCESS=YES
   test_at8m2r1_repair_has_no_secret_manager_or_external_effects
     - blocked google.cloud / secretmanager / HTTP client imports during open

8. EXTERNAL_EFFECTS=0
   test_at8m2r1_repair_has_no_secret_manager_or_external_effects
   implementation confined to local SQLite path operations
```

## Non-repair (preserved)

```text
SCHEMA_V1_METADATA_SEMANTICS=PRESERVED
EXACT_COMMITMENT_KEY_VERSION_MATCHING=PRESERVED
NO_MIGRATION=PRESERVED
PROVIDER_PATH_UNMODIFIED=YES
src/integrations/ghl/at1_commitment_key_provider.py=UNTOUCHED
```
