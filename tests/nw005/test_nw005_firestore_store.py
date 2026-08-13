from __future__ import annotations

import copy
from typing import Any, Dict, Mapping, Optional

import pytest
from google.api_core.exceptions import AlreadyExists

from mg_guide.firestore_audit.firestore_store import (
    AUTHORIZED_COLLECTION,
    AUTHORIZED_DATABASE,
    AUTHORIZED_MODE,
    AUTHORIZED_PROJECT,
    FIRESTORE_CAP_EXCEEDED,
    FIRESTORE_CREATE_CONFLICT,
    FIRESTORE_FINGERPRINT_MISMATCH,
    FIRESTORE_GUARD_REJECTED,
    FIRESTORE_NOT_FOUND_AFTER_DELETE,
    FIRESTORE_READBACK_INVALID,
    FIRESTORE_RUN_ID_MISMATCH,
    WAVE1_RUN_ID,
    FirestoreAuditStore,
    FirestoreAuditStoreError,
)
from mg_guide.firestore_audit.project import project_workflow_run_audit


class _FakeSnapshot:
    def __init__(self, data: Optional[Dict[str, Any]]) -> None:
        self.exists = data is not None
        self._data = data

    def to_dict(self) -> Optional[Dict[str, Any]]:
        return copy.deepcopy(self._data)


class _FakeDocument:
    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self._data: Optional[Dict[str, Any]] = None

    def create(self, data: Mapping[str, Any]) -> None:
        if self._data is not None:
            raise AlreadyExists(
                f"Document workflow_runs/{self.run_id} already exists."
            )
        self._data = dict(data)

    def get(self) -> _FakeSnapshot:
        return _FakeSnapshot(self._data)

    def delete(self) -> None:
        self._data = None


class _FakeCollection:
    def __init__(self) -> None:
        self._docs: Dict[str, _FakeDocument] = {}

    def document(self, run_id: str) -> _FakeDocument:
        return self._docs.setdefault(run_id, _FakeDocument(run_id))


class _FakeClient:
    def __init__(self, project: str, database: str) -> None:
        self.project = project
        self.database = database
        self._collection = _FakeCollection()

    def collection(self, name: str) -> _FakeCollection:
        assert name == AUTHORIZED_COLLECTION
        return self._collection


@pytest.fixture
def fake_store(monkeypatch):
    store = FirestoreAuditStore()
    monkeypatch.setattr(
        "mg_guide.firestore_audit.firestore_store.firestore.Client",
        lambda project, database: _FakeClient(project, database),
    )
    return store


def _project_success(load_packet, stage_a_context_for):
    return project_workflow_run_audit(
        load_packet("packet-success.completed.json"),
        stage_a_context_for("packet-success.completed.json"),
    )


def test_correct_project_database_collection_accepted(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    result = fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert result["created"] is True
    assert fake_store.creates == 1


def test_wrong_project_rejected_before_network(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.project = "other-project"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


def test_wrong_database_rejected_before_network(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.database = "other-database"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


def test_wrong_collection_rejected_before_network(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.collection = "other_collection"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


def test_non_wave1_run_id_rejected_before_network(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact("run_nw006_stage_denied_001", audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


@pytest.mark.parametrize(
    "bad_run_id",
    [
        "run_nw006_success_001/extra",
        "run_nw006_success_001*",
        "*",
        "",
        "RUN_NW006_SUCCESS_001",
    ],
)
def test_dynamic_or_wildcard_run_id_rejected(fake_store, load_packet, stage_a_context_for, bad_run_id):
    audit = _project_success(load_packet, stage_a_context_for)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(bad_run_id, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


def test_non_terminal_audit_rejected(fake_store, load_packet, stage_a_context_for):
    audit = project_workflow_run_audit(
        load_packet("packet-non-terminal.evaluating.json"),
        stage_a_context_for("packet-non-terminal.evaluating.json"),
    )
    assert audit["terminal_state"] == "non_terminal"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
    assert fake_store.creates == 0


def test_create_uses_create_only_semantics(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_CREATE_CONFLICT


def test_already_existing_doc_fails_closed(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    # Same content again must fail closed, not overwrite.
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_CREATE_CONFLICT


def test_exact_get_only(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    assert readback is not None
    assert readback["run_id"] == WAVE1_RUN_ID
    assert fake_store.reads == 1


def test_readback_run_id_mismatch_fails(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    # Keep the document schema-valid by updating both run_id and idempotency key
    # together; the mismatch with the requested run_id is then detected.
    readback["run_id"] = "tampered"
    readback["idempotency"]["key"] = "tampered"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.verify_readback(readback, WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_RUN_ID_MISMATCH


def test_schema_mismatch_fails(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    del readback["integrity"]
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.verify_readback(readback, WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_READBACK_INVALID


def test_fingerprint_mismatch_fails(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    readback["integrity"]["content_fingerprint"] = "0" * 64
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.verify_readback(readback, WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_FINGERPRINT_MISMATCH


def test_exact_delete_only(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    fake_store.delete_exact(WAVE1_RUN_ID)
    assert fake_store.deletes == 1
    assert fake_store.get_exact(WAVE1_RUN_ID) is None


def test_post_delete_not_found_required(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    fake_store.delete_exact(WAVE1_RUN_ID)
    fake_store.require_not_found_after_delete(WAVE1_RUN_ID)
    assert fake_store.get_exact(WAVE1_RUN_ID) is None


def test_cleanup_attempted_after_post_create_verification_failure(
    fake_store, load_packet, stage_a_context_for
):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    # Tamper the readback so verification fails after the create succeeded.
    readback["integrity"]["content_fingerprint"] = "0" * 64
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.verify_readback(readback, WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_FINGERPRINT_MISMATCH

    # Cleanup must still be attempted and must leave the document NOT_FOUND.
    fake_store.delete_exact(WAVE1_RUN_ID)
    fake_store.require_not_found_after_delete(WAVE1_RUN_ID)


def test_operation_counters_remain_within_caps(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.max_creates = 1
    fake_store.max_reads = 1
    fake_store.max_deletes = 1

    fake_store.create_exact(WAVE1_RUN_ID, audit)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_CAP_EXCEEDED

    fake_store.get_exact(WAVE1_RUN_ID)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.get_exact(WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_CAP_EXCEEDED

    fake_store.delete_exact(WAVE1_RUN_ID)
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.delete_exact(WAVE1_RUN_ID)
    assert exc.value.code == FIRESTORE_CAP_EXCEEDED


def test_verify_readback_matches_expected_projected_fingerprint(
    fake_store, load_packet, stage_a_context_for
):
    audit = _project_success(load_packet, stage_a_context_for)
    expected_fp = audit["integrity"]["content_fingerprint"]
    fake_store.create_exact(WAVE1_RUN_ID, audit)
    readback = fake_store.get_exact(WAVE1_RUN_ID)
    result = fake_store.verify_readback(readback, WAVE1_RUN_ID, expected_fp)
    assert result["schema_valid"] is True
    assert result["run_id_match"] is True
    assert result["stored_content_fingerprint"] == expected_fp
    assert result["recomputed_content_fingerprint"] == expected_fp


def test_retention_mode_guard_rejects_non_stage_b_smoke(fake_store, load_packet, stage_a_context_for):
    audit = _project_success(load_packet, stage_a_context_for)
    fake_store.retention_mode = "acceptance_demo"
    with pytest.raises(FirestoreAuditStoreError) as exc:
        fake_store.create_exact(WAVE1_RUN_ID, audit)
    assert exc.value.code == FIRESTORE_GUARD_REJECTED
