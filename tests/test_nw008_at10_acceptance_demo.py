from __future__ import annotations

import json
from pathlib import Path

import pytest

from mg_guide.firestore_audit.acceptance_demo import (
    AT10_ACCEPTANCE_SET,
    FINGERPRINT_MISMATCH,
    LOCAL_CAP_EXCEEDED,
    MAX_LOCAL_CREATES,
    MAX_LOCAL_DELETES,
    MAX_LOCAL_READS,
    OFFLINE_CREATE_CONFLICT,
    AcceptanceDemoValidationError,
    OfflineAcceptanceDemoStore,
    simulate_acceptance_demo,
    validate_acceptance_demo_set,
    validate_exact_audit_field_paths,
    verify_fingerprint_gate,
)
from mg_guide.firestore_audit.models import default_stage_a_context
from mg_guide.firestore_audit.project import project_workflow_run_audit


def _project_packet(packet_name: str):
    repo_root = Path(__file__).resolve().parents[1]
    packet_path = repo_root / "fixtures" / "nw005" / "packets" / packet_name
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    context = default_stage_a_context(
        fixture_id=packet_name,
        source_refs=[f"fixtures/nw005/packets/{packet_name}"],
        recorded_at="2026-08-12T20:00:00Z",
        writer_component_version="0.1.0-stage-a",
    )
    return project_workflow_run_audit(packet, context)


def _proof_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "proof" / "nw008" / "at-10" / "acceptance-demo"


def test_acceptance_demo_allowlist_is_exact() -> None:
    assert list(AT10_ACCEPTANCE_SET) == [
        "run_nw006_success_001",
        "run_nw006_stage_denied_001",
        "run_nw006_ambiguous_contact_001",
        "run_nw006_failed_001",
    ]


def test_exact_field_paths_are_present_and_rejected_if_alias_used() -> None:
    audit = _project_packet("packet-success.completed.json")
    validate_exact_audit_field_paths(audit, run_id="run_nw006_success_001")

    alias = dict(audit)
    alias["agents"] = ["agent-1"]
    del alias["agent_steps"]["agents_used"]
    with pytest.raises(AcceptanceDemoValidationError):
        validate_exact_audit_field_paths(alias, run_id="run_nw006_success_001")


def test_acceptance_demo_store_rejects_out_of_allowlist_run() -> None:
    store = OfflineAcceptanceDemoStore()
    with pytest.raises(AcceptanceDemoValidationError):
        store.create_exact("run_other_001", _project_packet("packet-success.completed.json"))


def test_validate_acceptance_demo_set_allows_exact_four_run_set() -> None:
    records = [
        _project_packet(name)
        for name in (
            "packet-success.completed.json",
            "packet-stage-change-denied.completed_with_review.json",
            "packet-ambiguous-contact.blocked.json",
            "packet-tool-failure.failed.json",
        )
    ]
    summary = validate_acceptance_demo_set(records)
    assert summary["status"] == "PASS"
    assert summary["acceptance_set_complete"] is True
    assert summary["allowlist_count"] == 4
    assert set(summary["present_run_ids"]) == set(AT10_ACCEPTANCE_SET)


def test_pre_create_exact_get_requires_not_found_x4() -> None:
    store = OfflineAcceptanceDemoStore()
    for run_id in AT10_ACCEPTANCE_SET:
        store.require_not_found(run_id)
    assert store.local_reads == 4
    assert len(store) == 0


def test_create_exact_rejects_duplicate_run() -> None:
    store = OfflineAcceptanceDemoStore()
    audit = _project_packet("packet-success.completed.json")
    store.create_exact("run_nw006_success_001", audit)
    with pytest.raises(AcceptanceDemoValidationError) as excinfo:
        store.create_exact("run_nw006_success_001", audit)
    assert OFFLINE_CREATE_CONFLICT in str(excinfo.value)
    assert "already exists" in str(excinfo.value)


def test_fingerprint_gate_triple_equality() -> None:
    projected = _project_packet("packet-success.completed.json")
    store = OfflineAcceptanceDemoStore()
    store.create_exact("run_nw006_success_001", projected)
    readback = store.get("run_nw006_success_001")
    assert readback is not None

    gate = verify_fingerprint_gate(readback, projected)
    assert gate["fingerprint_gate"] == "PASS"
    assert (
        gate["recomputed_content_fingerprint"]
        == gate["stored_content_fingerprint"]
        == gate["expected_projected_content_fingerprint"]
    )


def test_fingerprint_gate_rejects_tampered_readback() -> None:
    projected = _project_packet("packet-success.completed.json")
    store = OfflineAcceptanceDemoStore()
    store.create_exact("run_nw006_success_001", projected)
    readback = store.get("run_nw006_success_001")
    assert readback is not None

    tampered = dict(readback)
    tampered["agent_steps"] = dict(readback["agent_steps"])
    tampered["agent_steps"]["agents_used"] = ["tampered-agent"]

    with pytest.raises(AcceptanceDemoValidationError) as excinfo:
        verify_fingerprint_gate(tampered, projected)
    assert FINGERPRINT_MISMATCH in str(excinfo.value)


def test_local_caps_fail_closed() -> None:
    # Read cap.
    store = OfflineAcceptanceDemoStore(max_local_reads=0)
    with pytest.raises(AcceptanceDemoValidationError) as excinfo:
        store.get("run_nw006_success_001")
    assert LOCAL_CAP_EXCEEDED in str(excinfo.value)

    # Create cap.
    store = OfflineAcceptanceDemoStore(max_local_creates=0)
    with pytest.raises(AcceptanceDemoValidationError) as excinfo:
        store.create_exact("run_nw006_success_001", _project_packet("packet-success.completed.json"))
    assert LOCAL_CAP_EXCEEDED in str(excinfo.value)

    # Delete cap.
    store = OfflineAcceptanceDemoStore(max_local_deletes=0)
    store.create_exact("run_nw006_success_001", _project_packet("packet-success.completed.json"))
    with pytest.raises(AcceptanceDemoValidationError) as excinfo:
        store.delete_exact("run_nw006_success_001")
    assert LOCAL_CAP_EXCEEDED in str(excinfo.value)


def test_delete_exact_and_post_delete_not_found_x4() -> None:
    packet_map = {
        "run_nw006_success_001": "packet-success.completed.json",
        "run_nw006_stage_denied_001": "packet-stage-change-denied.completed_with_review.json",
        "run_nw006_ambiguous_contact_001": "packet-ambiguous-contact.blocked.json",
        "run_nw006_failed_001": "packet-tool-failure.failed.json",
    }
    store = OfflineAcceptanceDemoStore()
    for run_id, packet_name in packet_map.items():
        store.create_exact(run_id, _project_packet(packet_name))
    assert store.local_creates == 4

    for run_id in AT10_ACCEPTANCE_SET:
        store.delete_exact(run_id)
    assert store.local_deletes == 4
    assert len(store) == 0

    for run_id in AT10_ACCEPTANCE_SET:
        store.require_not_found(run_id)


def test_disposition_mapping_enforced_per_run_id() -> None:
    expected = {
        "run_nw006_success_001": "completed",
        "run_nw006_stage_denied_001": "completed_with_review",
        "run_nw006_ambiguous_contact_001": "blocked",
        "run_nw006_failed_001": "failed",
    }
    packet_map = {
        "run_nw006_success_001": "packet-success.completed.json",
        "run_nw006_stage_denied_001": "packet-stage-change-denied.completed_with_review.json",
        "run_nw006_ambiguous_contact_001": "packet-ambiguous-contact.blocked.json",
        "run_nw006_failed_001": "packet-tool-failure.failed.json",
    }
    for run_id, disposition in expected.items():
        audit = _project_packet(packet_map[run_id])
        result = validate_exact_audit_field_paths(audit, run_id=run_id)
        assert result["required_paths_present"] is True
        assert audit["final_disposition"] == disposition


def test_cleanup_proof_only_emitted_after_cleanup() -> None:
    result = simulate_acceptance_demo()
    assert result["cleanup_performed"] is True
    assert result["cleanup_verified_not_found"] is True

    cleanup_evidence = json.loads((_proof_dir() / "at-10-cleanup-evidence.json").read_text())
    assert cleanup_evidence["cleanup_performed"] is True
    assert cleanup_evidence["cleanup_verified_not_found"] is True
    assert set(cleanup_evidence["documents_deleted"]) == set(AT10_ACCEPTANCE_SET)


def test_simulate_acceptance_demo_runs_zero_network_and_emits_proof_files() -> None:
    result = simulate_acceptance_demo()
    assert result["status"] == "PASS"
    assert result["acceptance_set_complete"] is True
    assert result["network_calls"] == 0
    assert result["firestore_network_operations"] == 0
    assert result["firestore_reads"] == 0
    assert result["firestore_writes"] == 0
    assert result["firestore_deletes"] == 0
    assert result["local_creates"] == MAX_LOCAL_CREATES
    assert result["local_reads"] == MAX_LOCAL_READS
    assert result["local_deletes"] == MAX_LOCAL_DELETES
    assert result["cleanup_performed"] is True

    for filename in (
        "at-10-run-manifest.json",
        "at-10-record-evidence.json",
        "at-10-cleanup-evidence.json",
        "proof-manifest.md",
        "proof-return.yaml",
    ):
        assert (_proof_dir() / filename).exists()


def test_proof_return_declares_at10_not_complete() -> None:
    simulate_acceptance_demo()
    yaml_text = (_proof_dir() / "proof-return.yaml").read_text()
    assert "PROOF_CLASS: \"OFFLINE_IMPLEMENTATION_VALIDATION\"" in yaml_text
    assert "OFFLINE_VALIDATION_RESULT: \"PASS\"" in yaml_text
    assert "AT10_EXECUTION_OCCURRED: \"NO\"" in yaml_text
    assert "FIRESTORE_ACCEPTANCE_DEMO_EXECUTED: \"NO\"" in yaml_text
    assert "AT10_COMPLETE: \"NO\"" in yaml_text
    assert "AT10_EXECUTION_AUTHORIZED: \"NO\"" in yaml_text
    assert "AT10_COMPLETION_CLAIM_AUTHORIZED: \"NO\"" in yaml_text
    assert f"LOCAL_DOCUMENT_CREATES: {MAX_LOCAL_CREATES}" in yaml_text
    assert f"LOCAL_DOCUMENT_READS: {MAX_LOCAL_READS}" in yaml_text
    assert f"LOCAL_DOCUMENT_DELETES: {MAX_LOCAL_DELETES}" in yaml_text
