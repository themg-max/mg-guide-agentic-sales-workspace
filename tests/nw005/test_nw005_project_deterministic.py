from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from mg_guide.firestore_audit.canonicalize import nw005_canonical_json_v1
from mg_guide.firestore_audit.models import ProjectionContext
from mg_guide.firestore_audit.project import (
    AUDIT_PROJECTION_INCONSISTENT,
    AuditProjectionError,
    map_card_state,
    map_terminal_state,
    project_workflow_run_audit,
)
from mg_guide.firestore_audit.validate import validate_workflow_run_audit

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
def test_golden_terminal_projections(
    load_packet,
    load_expected_audit,
    stage_a_context_for,
    packet_name,
    expected_name,
    terminal,
):
    packet = load_packet(packet_name)
    expected = load_expected_audit(expected_name)
    ctx = stage_a_context_for(packet_name)

    actual = project_workflow_run_audit(packet, ctx)
    validate_workflow_run_audit(actual)

    assert actual["terminal_state"] == terminal
    assert actual["mg_guide_card"]["card_state"] == terminal
    assert actual["mg_guide_card"]["projection_source"] == "audit_status_mapper_v1"
    assert nw005_canonical_json_v1(actual) == nw005_canonical_json_v1(expected)
    assert actual == expected


def test_non_terminal_local_projection(load_packet, load_expected_audit, stage_a_context_for):
    packet_name = "packet-non-terminal.evaluating.json"
    packet = load_packet(packet_name)
    expected = load_expected_audit("audit-non-terminal.evaluating.json")
    ctx = stage_a_context_for(packet_name)

    actual = project_workflow_run_audit(packet, ctx)
    validate_workflow_run_audit(actual)
    assert actual["terminal_state"] == "non_terminal"
    assert actual["mg_guide_card"]["card_state"] == "in_progress"
    assert actual == expected


def test_deterministic_repeatability(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    ctx = stage_a_context_for("packet-success.completed.json")
    a = project_workflow_run_audit(packet, ctx)
    b = project_workflow_run_audit(copy.deepcopy(packet), ctx)
    assert nw005_canonical_json_v1(a) == nw005_canonical_json_v1(b)
    assert a["integrity"] == b["integrity"]


def test_projection_context_explicit_fields(load_packet):
    packet = load_packet("packet-success.completed.json")
    ctx = ProjectionContext(
        recorded_at="2026-01-01T00:00:00Z",
        fixture_id="custom-fixture",
        source_refs=("proof/a", "fixtures/b"),
        writer_component="mg_guide.firestore_audit.project",
        writer_component_version="test-version",
        writer_mode="local_fixture",
    )
    audit = project_workflow_run_audit(packet, ctx)
    assert audit["recorded_at"] == "2026-01-01T00:00:00Z"
    assert audit["provenance"]["fixture_id"] == "custom-fixture"
    assert audit["provenance"]["source_refs"] == ["proof/a", "fixtures/b"]
    assert audit["provenance"]["writer"]["component_version"] == "test-version"
    assert audit["provenance"]["writer"]["mode"] == "local_fixture"


def test_recorded_at_excluded_from_content_fingerprint(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    ctx1 = stage_a_context_for("packet-success.completed.json")
    ctx2 = ProjectionContext(
        recorded_at="2099-01-01T00:00:00Z",
        fixture_id=ctx1.fixture_id,
        source_refs=ctx1.source_refs,
        writer_component=ctx1.writer_component,
        writer_component_version=ctx1.writer_component_version,
        writer_mode=ctx1.writer_mode,
    )
    a = project_workflow_run_audit(packet, ctx1)
    b = project_workflow_run_audit(packet, ctx2)
    assert a["integrity"]["content_fingerprint"] == b["integrity"]["content_fingerprint"]
    assert a["integrity"]["projection_input_fingerprint"] == b[
        "integrity"
    ]["projection_input_fingerprint"]
    assert a["recorded_at"] != b["recorded_at"]


def test_status_disposition_mismatch_fails_closed(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    packet = copy.deepcopy(packet)
    packet["audit"]["final_disposition"] = "blocked"
    ctx = stage_a_context_for("packet-success.completed.json")
    with pytest.raises(AuditProjectionError) as exc:
        project_workflow_run_audit(packet, ctx)
    assert exc.value.code == AUDIT_PROJECTION_INCONSISTENT


def test_invalid_workflow_fails_closed(load_packet, stage_a_context_for):
    packet = copy.deepcopy(load_packet("packet-success.completed.json"))
    packet["run"]["workflow"] = "other_workflow"
    ctx = stage_a_context_for("packet-success.completed.json")
    with pytest.raises(AuditProjectionError):
        project_workflow_run_audit(packet, ctx)


def test_map_helpers():
    assert map_terminal_state("completed", "completed") == "completed"
    assert map_terminal_state("evaluating", "pending") == "non_terminal"
    assert map_terminal_state("writing", None) == "non_terminal"
    assert map_card_state("completed") == "completed"
    assert map_card_state("evaluating") == "in_progress"


def test_no_transcript_body_in_projection(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    ctx = stage_a_context_for("packet-success.completed.json")
    audit = project_workflow_run_audit(packet, ctx)
    blob = json.dumps(audit)
    assert "transcript_body" not in blob
    assert "Discovery call complete with agreed" not in blob  # extraction summary not copied
    # Only hash retained
    assert audit["provenance"]["transcript_hash"] == packet["meeting"]["transcript_hash"]


def test_failed_errors_include_reason_codes(load_packet, stage_a_context_for):
    packet = load_packet("packet-tool-failure.failed.json")
    ctx = stage_a_context_for("packet-tool-failure.failed.json")
    audit = project_workflow_run_audit(packet, ctx)
    assert any("GHL_TOOL_FAILURE" in e for e in audit["errors"])
    assert any("final_disposition=failed" in e for e in audit["errors"])


def test_tools_listed_count_is_not_invocation_count(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    ctx = stage_a_context_for("packet-success.completed.json")
    audit = project_workflow_run_audit(packet, ctx)
    assert audit["tool_call_counts"]["tools_listed_count"] == len(
        packet["audit"]["tools_used"]
    )
    # No invocation-count field present
    assert "invocation_count" not in json.dumps(audit["tool_call_counts"])


def test_fingerprints_non_recursive(load_packet, stage_a_context_for):
    packet = load_packet("packet-success.completed.json")
    ctx = stage_a_context_for("packet-success.completed.json")
    audit = project_workflow_run_audit(packet, ctx)
    # Integrity values must not appear as inputs inside themselves via embedding
    pip = audit["integrity"]["projection_input_fingerprint"]
    cfp = audit["integrity"]["content_fingerprint"]
    body_without_integrity = {k: v for k, v in audit.items() if k != "integrity"}
    assert pip not in json.dumps(body_without_integrity)
    # content fingerprint is of body without integrity/recorded_at — recomputing is stable
    from mg_guide.firestore_audit.canonicalize import fingerprint_hex
    from mg_guide.firestore_audit.project import _content_fingerprint_body, _projection_input_body

    assert fingerprint_hex(_projection_input_body(audit)) == pip
    assert fingerprint_hex(_content_fingerprint_body(audit)) == cfp
