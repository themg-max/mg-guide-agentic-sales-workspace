from __future__ import annotations

import copy

import pytest

from mg_guide.firestore_audit.memory_store import (
    AUDIT_IDEMPOTENCY_CONFLICT,
    AUDIT_NON_TERMINAL_DURABLE_WRITE,
    AUDIT_TERMINAL_STATE_CONFLICT,
    AuditStoreError,
    MemoryAuditStore,
)
from mg_guide.firestore_audit.project import project_workflow_run_audit


def _project(load_packet, stage_a_context_for, packet_name: str):
    packet = load_packet(packet_name)
    ctx = stage_a_context_for(packet_name)
    return project_workflow_run_audit(packet, ctx)


def test_create_then_idempotent_noop(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    audit = _project(load_packet, stage_a_context_for, "packet-success.completed.json")

    first = store.persist(audit)
    assert first.status == "created"
    assert first.durable_write is True
    assert store.creates == 1

    second = store.persist(audit)
    assert second.status == "idempotent_noop"
    assert second.durable_write is False
    assert second.duplicate_write_rejected is False
    assert store.creates == 1
    assert store.noop_hits == 1
    assert len(store) == 1


def test_idempotency_conflict_different_fingerprint(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    base = _project(load_packet, stage_a_context_for, "packet-success.completed.json")
    store.persist(base)

    # Same run_id + terminal_state, different packet-derived content → fingerprint change
    packet = copy.deepcopy(load_packet("packet-success.completed.json"))
    packet["policy"]["reason_codes"] = ["SYNTHETIC_REASON_FOR_CONFLICT"]
    # Keep disposition consistent
    ctx = stage_a_context_for("packet-success.completed.json")
    altered = project_workflow_run_audit(packet, ctx)
    assert altered["run_id"] == base["run_id"]
    assert altered["terminal_state"] == base["terminal_state"]
    assert (
        altered["integrity"]["projection_input_fingerprint"]
        != base["integrity"]["projection_input_fingerprint"]
    )

    with pytest.raises(AuditStoreError) as exc:
        store.persist(altered)
    assert exc.value.code == AUDIT_IDEMPOTENCY_CONFLICT
    # Original unchanged
    stored = store.get(base["run_id"])
    assert stored["integrity"] == base["integrity"]


def test_terminal_state_conflict(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    completed = _project(load_packet, stage_a_context_for, "packet-success.completed.json")
    store.persist(completed)

    blocked = _project(
        load_packet, stage_a_context_for, "packet-ambiguous-contact.blocked.json"
    )
    # Force same run_id with different terminal state
    blocked = copy.deepcopy(blocked)
    blocked["run_id"] = completed["run_id"]
    blocked["idempotency"]["key"] = completed["run_id"]
    # Recompute would change fingerprints; for store rules we only need different terminal_state
    # after validation — rebuild integrity by re-projecting with patched packet.
    packet = copy.deepcopy(load_packet("packet-ambiguous-contact.blocked.json"))
    packet["run"]["run_id"] = completed["run_id"]
    ctx = stage_a_context_for("packet-ambiguous-contact.blocked.json")
    blocked = project_workflow_run_audit(packet, ctx)
    assert blocked["run_id"] == completed["run_id"]
    assert blocked["terminal_state"] != completed["terminal_state"]

    with pytest.raises(AuditStoreError) as exc:
        store.persist(blocked)
    assert exc.value.code == AUDIT_TERMINAL_STATE_CONFLICT


def test_non_terminal_must_not_persist(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    audit = _project(
        load_packet, stage_a_context_for, "packet-non-terminal.evaluating.json"
    )
    assert audit["terminal_state"] == "non_terminal"
    with pytest.raises(AuditStoreError) as exc:
        store.persist(audit)
    assert exc.value.code == AUDIT_NON_TERMINAL_DURABLE_WRITE
    assert len(store) == 0


def test_non_terminal_reject_without_raise(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    audit = _project(
        load_packet, stage_a_context_for, "packet-non-terminal.evaluating.json"
    )
    result = store.persist(audit, raise_on_conflict=False)
    assert result.status == "rejected"
    assert result.code == AUDIT_NON_TERMINAL_DURABLE_WRITE
    assert result.durable_write is False


def test_all_terminal_classes_persist(load_packet, stage_a_context_for):
    store = MemoryAuditStore()
    names = [
        "packet-success.completed.json",
        "packet-stage-change-denied.completed_with_review.json",
        "packet-ambiguous-contact.blocked.json",
        "packet-tool-failure.failed.json",
    ]
    for name in names:
        audit = _project(load_packet, stage_a_context_for, name)
        result = store.persist(audit)
        assert result.status == "created"
        assert result.durable_write is True
    assert len(store) == 4
