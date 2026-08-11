from __future__ import annotations

import json
from pathlib import Path

import pytest

from orchestration.runner import WorkflowRunner


FIXTURES = [
    (
        "transcript-success.expected.json",
        "completed",
        [],
        (1, 1),
    ),
    (
        "transcript-ambiguous-contact.expected.json",
        "blocked",
        ["AMBIGUOUS_CONTACT"],
        (0, 0),
    ),
    (
        "transcript-no-stage-change.expected.json",
        "completed_with_review",
        ["STAGE_TRANSITION_NOT_ALLOWED"],
        (1, 0),
    ),
]


@pytest.mark.parametrize("name,state,codes,intent_bounds", FIXTURES)
def test_fixture_outcomes(repo_root, packet_schema, name, state, codes, intent_bounds):
    runner = WorkflowRunner()
    path = repo_root / "fixtures" / name
    result = runner.run_fixture(path)
    assert result.validation_ok
    assert result.external_effects == 0
    assert result.final_state == state
    for code in codes:
        assert code in result.reason_codes
    if state == "completed":
        assert result.reason_codes == []
    note_n = len(result.mutation_intents.get("note") or [])
    stage_n = len(result.mutation_intents.get("stage") or [])
    note_max, stage_max = intent_bounds
    assert note_n <= note_max
    assert stage_n <= stage_max
    if state == "blocked" and "AMBIGUOUS_CONTACT" in codes:
        assert note_n == 0 and stage_n == 0
    if state == "completed_with_review":
        assert stage_n == 0
        assert note_n <= 1
    packet_schema.validate(result.packet)
    assert result.packet["external_effects"] == 0


def test_duplicate_run_id_cannot_advance(repo_root):
    runner = WorkflowRunner()
    path = repo_root / "fixtures" / "transcript-success.expected.json"
    first = runner.run_fixture(path)
    assert first.final_state == "completed"
    second = runner.run_fixture(path)
    assert second.rejected_duplicate is True
    assert second.validation_ok is False
    assert "duplicate run_id" in (second.error or "")


def test_equivalent_deterministic_replay_result(repo_root):
    path = repo_root / "fixtures" / "transcript-success.expected.json"
    r1 = WorkflowRunner().run_fixture(path, created_at="2026-08-11T15:00:00Z")
    r2 = WorkflowRunner().run_fixture(path, created_at="2026-08-11T15:00:00Z")
    assert r1.final_state == r2.final_state
    assert r1.reason_codes == r2.reason_codes
    assert r1.mutation_intents == r2.mutation_intents
    assert r1.external_effects == r2.external_effects == 0
    # Semantic packet fields (ignore completed_at clock if any drift)
    p1 = dict(r1.packet)
    p2 = dict(r2.packet)
    p1["audit"] = {**p1["audit"], "completed_at": "X"}
    p2["audit"] = {**p2["audit"], "completed_at": "X"}
    assert p1 == p2


def test_zero_external_effects_all_fixtures(repo_root):
    runner = WorkflowRunner()
    for name, *_ in FIXTURES:
        # fresh runner registry per fixture via same runner is fine; unique run ids
        result = runner.run_fixture(repo_root / "fixtures" / name)
        assert result.external_effects == 0
