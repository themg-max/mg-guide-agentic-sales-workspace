from __future__ import annotations

import json
from pathlib import Path
import pickle
import sqlite3

import pytest

from integrations.ghl.at1_commitment_key_provider import (
    CommitmentKeyMaterial,
    SyntheticCommitmentKeyProvider,
)
from integrations.ghl.at1_execution_store import (
    At1ExecutionStore,
    ExecutionStoreSchemaError,
)


VERSION_RESOURCE = "projects/synthetic-project/secrets/at1-commitment-key/versions/1"


def _material(
    *,
    payload: str = "synthetic-commitment-key",
    version_resource: str = VERSION_RESOURCE,
) -> CommitmentKeyMaterial:
    return SyntheticCommitmentKeyProvider(
        payload=payload,
        version_resource=version_resource,
    ).resolve()


def _store(
    db_path: Path,
    *,
    payload: str = "synthetic-commitment-key",
    version_resource: str = VERSION_RESOURCE,
) -> At1ExecutionStore:
    return At1ExecutionStore(
        db_path=db_path,
        commitment_material=_material(
            payload=payload,
            version_resource=version_resource,
        ),
    )


def _close(store: At1ExecutionStore) -> None:
    store._connection.close()


def _metadata(db_path: Path) -> tuple[int, str]:
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT schema_version, commitment_key_version_resource
            FROM at1_store_metadata
            """
        ).fetchone()
    assert row is not None
    return int(row[0]), str(row[1])


def test_synthetic_provider_returns_opaque_exact_version_material() -> None:
    material = _material()

    assert material.version_resource == VERSION_RESOURCE
    assert "synthetic-commitment-key" not in repr(material)
    assert "synthetic-commitment-key" not in str(material)
    assert VERSION_RESOURCE in repr(material)
    assert not hasattr(material, "payload")
    assert not hasattr(material, "__dict__")

    with pytest.raises(TypeError, match="serialization is forbidden"):
        pickle.dumps(material)
    with pytest.raises(TypeError):
        json.dumps({"material": material})
    with pytest.raises(TypeError, match="resolved by a provider"):
        CommitmentKeyMaterial(
            _payload=b"synthetic-commitment-key",
            _version_resource=VERSION_RESOURCE,
            _factory_token=object(),
        )


@pytest.mark.parametrize(
    "version_resource",
    [
        "projects/synthetic-project/secrets/at1-commitment-key/versions/latest",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/alias",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/0",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/-1",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/1?alt=json",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/1#fragment",
        " projects/synthetic-project/secrets/at1-commitment-key/versions/1",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/1 ",
        "projects/synthetic-project/secrets/at1-commitment-key/versions/1 2",
        "projects/synthetic-project/secrets/at1-commitment-key/versions",
        "projects//secrets/at1-commitment-key/versions/1",
    ],
)
def test_provider_rejects_non_exact_version_resources(version_resource: str) -> None:
    with pytest.raises(ValueError, match="exact positive numeric version resource"):
        _material(version_resource=version_resource)


def test_new_store_initializes_schema_v1_atomically(tmp_path: Path) -> None:
    db_path = tmp_path / "new-store.sqlite3"
    store = _store(db_path)

    assert _metadata(db_path) == (1, VERSION_RESOURCE)
    table_names = store._table_names()
    assert table_names == {
        "at1_store_metadata",
        "attempts",
        "business_ledger",
        "execution_claims",
        "protocol_ledger",
    }


def test_schema_v1_reopens_with_same_version_and_never_stores_payload(tmp_path: Path) -> None:
    db_path = tmp_path / "schema-v1-reopen.sqlite3"
    payload = "PAYLOAD_MUST_NOT_REACH_SQLITE"
    store = _store(db_path, payload=payload)
    _close(store)

    reopened = _store(db_path, payload=payload)
    assert _metadata(db_path) == (1, VERSION_RESOURCE)
    dump = "\n".join(reopened._connection.iterdump())
    assert payload not in dump
    _close(reopened)


def test_reopen_with_different_version_fails_closed(tmp_path: Path) -> None:
    db_path = tmp_path / "version-mismatch.sqlite3"
    store = _store(db_path)
    _close(store)

    with pytest.raises(ExecutionStoreSchemaError, match="version does not match"):
        _store(
            db_path,
            payload="another-synthetic-commitment-key",
            version_resource="projects/synthetic-project/secrets/at1-commitment-key/versions/2",
        )


def test_atomic_initialization_failure_rolls_back_all_schema(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "atomic-failure.sqlite3"
    original_statements = At1ExecutionStore._schema_statements

    with monkeypatch.context() as patch:
        patch.setattr(
            At1ExecutionStore,
            "_schema_statements",
            staticmethod(lambda: (*original_statements(), "CREATE TABLE broken (")),
        )
        with pytest.raises(ExecutionStoreSchemaError, match="atomic store initialization failed"):
            _store(db_path)

    assert db_path.exists()
    with sqlite3.connect(db_path) as connection:
        table_names = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                """
            )
        }
    assert table_names == set()

    # Failed-init artifact remains preexisting and empty: reopen must fail closed.
    with pytest.raises(
        ExecutionStoreSchemaError,
        match="preexisting empty store artifact cannot be initialized",
    ):
        _store(db_path)


def test_preexisting_empty_store_fails_closed(tmp_path: Path) -> None:
    zero_byte_path = tmp_path / "preexisting-zero-byte.sqlite3"
    zero_byte_path.write_bytes(b"")
    assert zero_byte_path.exists()
    assert zero_byte_path.stat().st_size == 0
    with pytest.raises(
        ExecutionStoreSchemaError,
        match="preexisting empty store artifact cannot be initialized",
    ):
        _store(zero_byte_path)

    empty_sqlite_path = tmp_path / "preexisting-empty-sqlite.sqlite3"
    with sqlite3.connect(empty_sqlite_path) as connection:
        connection.execute("PRAGMA user_version = 0")
    assert empty_sqlite_path.exists()
    with sqlite3.connect(empty_sqlite_path) as connection:
        table_names = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                """
            )
        }
    assert table_names == set()
    with pytest.raises(
        ExecutionStoreSchemaError,
        match="preexisting empty store artifact cannot be initialized",
    ):
        _store(empty_sqlite_path)


def test_failed_initialization_artifact_reopen_fails_closed(
    tmp_path: Path, monkeypatch
) -> None:
    db_path = tmp_path / "failed-init-artifact.sqlite3"
    original_statements = At1ExecutionStore._schema_statements

    with monkeypatch.context() as patch:
        patch.setattr(
            At1ExecutionStore,
            "_schema_statements",
            staticmethod(lambda: (*original_statements(), "CREATE TABLE broken (")),
        )
        with pytest.raises(ExecutionStoreSchemaError, match="atomic store initialization failed"):
            _store(db_path)

    assert db_path.exists()
    with pytest.raises(
        ExecutionStoreSchemaError,
        match="preexisting empty store artifact cannot be initialized",
    ):
        _store(db_path)


def test_interrupted_initialization_reopen_fails_closed(tmp_path: Path) -> None:
    db_path = tmp_path / "interrupted-initialization.sqlite3"
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE execution_claims (
                grant_run_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL
            )
            """
        )

    with pytest.raises(ExecutionStoreSchemaError, match="no authoritative metadata"):
        _store(db_path)


def test_partial_schema_store_fails_closed(tmp_path: Path) -> None:
    db_path = tmp_path / "partial-schema.sqlite3"
    with sqlite3.connect(db_path) as connection:
        connection.execute(At1ExecutionStore._schema_statements()[0])
        connection.execute(
            """
            INSERT INTO at1_store_metadata (
                singleton,
                schema_version,
                commitment_key_version_resource
            )
            VALUES (1, 1, ?)
            """,
            (VERSION_RESOURCE,),
        )
        connection.execute(At1ExecutionStore._schema_statements()[1])

    with pytest.raises(ExecutionStoreSchemaError, match="partially initialized"):
        _store(db_path)


def test_legacy_unversioned_store_fails_closed(tmp_path: Path) -> None:
    db_path = tmp_path / "legacy-unversioned.sqlite3"
    with sqlite3.connect(db_path) as connection:
        for statement in At1ExecutionStore._schema_statements()[1:]:
            connection.execute(statement)

    with pytest.raises(ExecutionStoreSchemaError, match="no authoritative metadata"):
        _store(db_path)


def test_at8m2r1_repair_has_no_secret_manager_or_external_effects(
    tmp_path: Path, monkeypatch
) -> None:
    blocked_prefixes = (
        "google.cloud",
        "google.auth",
        "requests",
        "httpx",
        "urllib.request",
        "secretmanager",
    )

    def _block_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        root = name.split(".", 1)[0]
        if name.startswith(blocked_prefixes) or root in {
            "requests",
            "httpx",
            "secretmanager",
        }:
            raise AssertionError(f"forbidden external import attempted: {name}")
        return original_import(name, globals, locals, fromlist, level)

    import builtins

    original_import = builtins.__import__
    monkeypatch.setattr(builtins, "__import__", _block_import)

    fresh_path = tmp_path / "no-external-effects.sqlite3"
    assert not fresh_path.exists()
    store = _store(fresh_path)
    assert _metadata(fresh_path) == (1, VERSION_RESOURCE)
    _close(store)

    empty_path = tmp_path / "preexisting-empty-for-effects.sqlite3"
    empty_path.write_bytes(b"")
    with pytest.raises(
        ExecutionStoreSchemaError,
        match="preexisting empty store artifact cannot be initialized",
    ):
        _store(empty_path)


def test_missing_and_corrupt_metadata_fail_closed(tmp_path: Path) -> None:
    missing_metadata_path = tmp_path / "missing-metadata.sqlite3"
    store = _store(missing_metadata_path)
    _close(store)
    with sqlite3.connect(missing_metadata_path) as connection:
        connection.execute("DELETE FROM at1_store_metadata")
    with pytest.raises(ExecutionStoreSchemaError, match="exactly one row"):
        _store(missing_metadata_path)

    corrupt_metadata_path = tmp_path / "corrupt-metadata.sqlite3"
    store = _store(corrupt_metadata_path)
    _close(store)
    with sqlite3.connect(corrupt_metadata_path) as connection:
        connection.execute(
            """
            UPDATE at1_store_metadata
            SET commitment_key_version_resource = 'not-a-version-resource'
            """
        )
    with pytest.raises(ExecutionStoreSchemaError, match="metadata is corrupt"):
        _store(corrupt_metadata_path)


def test_unknown_newer_schema_fails_and_v1_performs_no_migration(tmp_path: Path) -> None:
    db_path = tmp_path / "schema-version.sqlite3"
    store = _store(db_path)
    _close(store)
    reopened = _store(db_path)
    assert _metadata(db_path) == (1, VERSION_RESOURCE)
    _close(reopened)

    with sqlite3.connect(db_path) as connection:
        connection.execute("UPDATE at1_store_metadata SET schema_version = 2")
    with pytest.raises(ExecutionStoreSchemaError, match="unsupported or corrupt"):
        _store(db_path)


def test_store_requires_provenance_bound_material_and_rejects_provider(tmp_path: Path) -> None:
    db_path = tmp_path / "construction-boundary.sqlite3"
    provider = SyntheticCommitmentKeyProvider(
        payload="synthetic-commitment-key",
        version_resource=VERSION_RESOURCE,
    )

    accepted = At1ExecutionStore(
        db_path=db_path,
        commitment_material=provider.resolve(),
    )
    _close(accepted)

    with pytest.raises(TypeError, match="provider-resolved CommitmentKeyMaterial"):
        At1ExecutionStore(db_path=db_path, commitment_material=provider)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        At1ExecutionStore(
            db_path=db_path,
            commitment_material=_material(),
            commitment_key_version_resource=VERSION_RESOURCE,
        )  # type: ignore[call-arg]
