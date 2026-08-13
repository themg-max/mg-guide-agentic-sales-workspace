from __future__ import annotations

import copy

import pytest

from mg_guide.firestore_audit.project import project_workflow_run_audit
from mg_guide.firestore_audit.validate import (
    AuditValidationError,
    is_valid_workflow_run_audit,
    validate_workflow_run_audit,
)

TERMINAL_CASES = [
    (
        "packet-success.completed.json",
        "audit-success.completed.json",
        "completed",
    ),
    (
        "packet-stage-change-denied.completed_with_review.json",
        "audit-stage-change-denied.completed_with_review.json",
        "completed_with_review",
    ),
    (
        "packet-ambiguous-contact.blocked.json",
        "audit-ambiguous-contact.blocked.json",
        "blocked",
    ),
    (
        "packet-tool-failure.failed.json",
        "audit-tool-failure.failed.json",
        "failed",
    ),
]


@pytest.mark.parametrize("packet_name,expected_name,terminal", TERMINAL_CASES)
def test_expected_audits_schema_valid(
    load_packet, load_expected_audit, stage_a_context_for, packet_name, expected_name, terminal
):
    expected = load_expected_audit(expected_name)
    validate_workflow_run_audit(expected)
    ok, errs = is_valid_workflow_run_audit(expected)
    assert ok and not errs

    # Fresh projection also validates
    audit = project_workflow_run_audit(
        load_packet(packet_name), stage_a_context_for(packet_name)
    )
    validate_workflow_run_audit(audit)
    assert audit["terminal_state"] == terminal


def test_schema_rejects_missing_integrity(load_expected_audit):
    audit = copy.deepcopy(load_expected_audit("audit-success.completed.json"))
    del audit["integrity"]
    with pytest.raises(AuditValidationError):
        validate_workflow_run_audit(audit)


def test_schema_rejects_wrong_schema_const(load_expected_audit):
    audit = copy.deepcopy(load_expected_audit("audit-success.completed.json"))
    audit["schema"] = "not_audit"
    with pytest.raises(AuditValidationError):
        validate_workflow_run_audit(audit)


def test_idempotency_key_must_match_run_id(load_expected_audit):
    audit = copy.deepcopy(load_expected_audit("audit-success.completed.json"))
    audit["idempotency"]["key"] = "other-run"
    with pytest.raises(AuditValidationError):
        validate_workflow_run_audit(audit)
