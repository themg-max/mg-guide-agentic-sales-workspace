# NW-008 AT-8M2 — Offline Execution Store Substrate Implementation 001

```text
UNIT=NW008_AT8M2_OFFLINE_EXECUTION_STORE_SUBSTRATE_IMPLEMENTATION_001
OWNER=VS_CODE_ORCHESTRATOR
IMPLEMENTATION_MODE=OFFLINE_DETERMINISTIC_NO_EXTERNAL_EFFECTS

AUTHORIZATION_PR=124
AUTHORIZATION_REVIEWED_HEAD=44464d4fdb564e73a86d9a6af8bde054cef43546
AUTHORIZATION_MERGE_SHA=a02784ada82d1bc7b29ad2065d747f02690b456f
AUTHORIZATION_ARTIFACT_BLOB_SHA=33834900a67e84086b604a1fee006d046094b3ab

AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
EXTERNAL_EFFECTS=0
```

## Implemented offline substrate

`At1ExecutionStore` now accepts one provider-resolved
`CommitmentKeyMaterial` object. It does not accept a provider object, raw
commitment-key payload, or independently supplied version resource.

`SyntheticCommitmentKeyProvider` is an offline-only provider. Its resolved
material binds payload and an exact immutable version resource:

```text
projects/<project>/secrets/<secret>/versions/<positive-numeric-version>
```

The provider validates that form and rejects `latest`, aliases, `0`, negative
versions, query strings, fragments, whitespace, and malformed names. Material
payload has no public property, is excluded from `repr` / `str`, and rejects
serialization. The non-secret version resource remains available for metadata
and diagnostics.

Provider resolution happens outside the store. The store validates version
resource shape and equality with persisted metadata; it does not attempt to
prove an arbitrary payload originated in Secret Manager.

## Store schema v1

```text
INITIAL_STORE_SCHEMA_VERSION=1
CURRENT_STORE_SCHEMA_VERSION=1
SUPPORTED_STORE_SCHEMA_VERSIONS=1
AT8M2_FORWARD_MIGRATION_STEP_IMPLEMENTED=NO
```

New SQLite stores create operational tables and the singleton metadata row in
one explicit transaction. Metadata persists only `schema_version` and
`commitment_key_version_resource`; it never contains payload bytes.

Reopen fails closed when metadata is absent, corrupt, mismatched with supplied
material, or describes an unknown newer schema. A legacy/unversioned or
partially initialized store also fails closed. There is no AT8M2 migration
step.

## Deterministic proof mapping

`tests/integrations/ghl/test_at1_commitment_key_provider.py` covers:

```text
- new store initialization and schema-v1 initialization/reopen
- atomic initialization rollback
- interrupted initialization reopen fail-closed
- exact positive numeric version acceptance
- latest, alias, query, fragment, whitespace, non-positive, and malformed rejection
- same-version reopen success and different-version failure
- missing/corrupt metadata, legacy/unversioned, and unknown-newer-schema refusal
- no migration performed for schema v1
- payload absent from SQLite, repr, str, and serialization
- rejection of raw-key, independent key/version, and provider-object store inputs
- acceptance of provenance-bound material
```

The four AT8M1-frozen constructor-consumer tests now use the same canonical
provenance-bound material path:

```text
tests/integrations/ghl/test_at1_live_transport_remediation.py
tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
```

## Validation evidence

```text
AT8M2_FOCUSED_PROVIDER_STORE_TESTS=21_PASS
AT8M2_AUTHORIZED_INTEGRATION_TESTS=113_PASS
FULL_DETERMINISTIC_PYTEST=664_PASS
PHASE1_DETERMINISTIC_VALIDATION=PASS

REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
GCP_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
EXTERNAL_EFFECTS=0
```

The full deterministic suite was run in a session-only Python 3.13 virtual
environment using the repository's pinned requirements. Python 3.14 could not
install the pinned `rpds-py==0.20.1` because its bundled PyO3 version supports
up to Python 3.13; no dependency manifest was changed.
