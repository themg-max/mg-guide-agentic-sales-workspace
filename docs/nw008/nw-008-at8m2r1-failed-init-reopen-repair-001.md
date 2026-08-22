# NW-008 AT-8M2R1 — Failed-Initialization Reopen Repair 001

```text
UNIT=NW008_AT8M2R1_OFFLINE_EXECUTION_STORE_FAILED_INIT_REOPEN_REPAIR_001
OWNER=VS_CODE_ORCHESTRATOR
IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS

AUTHORIZATION_PR=126
AUTHORIZATION_REVIEWED_HEAD=56798c5e0a9face80b088f1f76f4432988676398
AUTHORIZATION_MERGE_SHA=978ed921be23e45b16eb3b6b021666603326535a
AUTHORIZATION_ARTIFACT_BLOB_SHA=78c882352d2aea8c84f3b544b0aa7d9201f8b1c3

PR125_REVIEWED_HEAD=6d2fd608f134f0d1a29131e4303978f568a4fd3d
AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
EXTERNAL_EFFECTS=0
```

## Defect repaired

PR125's `At1ExecutionStore` opened SQLite with `sqlite3.connect()`, which
creates a missing path. `_initialize_schema()` then treated any store with
`TABLE_COUNT=0` as a fresh initialization target. That collapsed three distinct
states into one:

```text
1. fresh non-existent path            -> should initialize
2. preexisting empty SQLite artifact  -> must fail closed
3. artifact left after failed init    -> must fail closed
```

States 2 and 3 were incorrectly re-initialized.

## Repair

Before `sqlite3.connect()`, the constructor records `PATH_PREEXISTED` from
`Path(db_path).exists()`.

```text
PATH_PREEXISTED=NO  AND TABLE_COUNT=0  -> schema-v1 initialization proceeds
PATH_PREEXISTED=YES AND TABLE_COUNT=0  -> ExecutionStoreSchemaError (fail closed)
```

No deletion, recreation, or migration of a failed artifact is performed. An
existing empty file remains unacceptable on every subsequent open.

## Preserved contracts

```text
FAILED_INITIALIZATION_ARTIFACT_REOPEN=FAIL_CLOSED
PREEXISTING_EMPTY_STORE_OPEN=FAIL_CLOSED
FRESH_NONEXISTENT_STORE_INITIALIZATION=ALLOWED
ATOMIC_SCHEMA_AND_METADATA_INITIALIZATION=YES
PARTIAL_SCHEMA_INITIALIZATION=FAIL_CLOSED
LEGACY_UNVERSIONED_STORE_OPEN=FAIL_CLOSED
```

Unchanged:

- schema-v1 metadata semantics (`schema_version`, `commitment_key_version_resource`)
- exact commitment-key version matching on reopen
- partial-schema refusal
- legacy-unversioned refusal
- no migration step
- zero external effects / no Secret Manager access
- blocked provider path `src/integrations/ghl/at1_commitment_key_provider.py`

## Writable scope consumed

```text
AUTHORIZED_SOURCE_PATHS=
  src/integrations/ghl/at1_execution_store.py

AUTHORIZED_TEST_PATHS=
  tests/integrations/ghl/test_at1_commitment_key_provider.py

AUTHORIZED_PROOF_PATHS=
  proof/nw008/at-8m2r1/**

AUTHORIZED_DOC_PATH_EXACT=
  docs/nw008/nw-008-at8m2r1-failed-init-reopen-repair-001.md
```

## Deterministic proof mapping

`tests/integrations/ghl/test_at1_commitment_key_provider.py` covers:

```text
1. fresh non-existent path initializes successfully
2. pre-created zero-byte/empty SQLite path fails closed
3. injected initialization failure rolls back (no user tables)
4. artifact left by failed initialization fails closed on subsequent reopen
5. partial-schema store fails closed
6. legacy unversioned store fails closed
7. no Secret Manager access
8. EXTERNAL_EFFECTS=0
```
