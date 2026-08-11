from __future__ import annotations

import pytest

from orchestration.models import RunRegistry
from orchestration.policy import bound_intents, evaluate_policy
from orchestration.state_machine import StateMachine, TransitionError


def test_all_legal_transitions(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    edges = sm.all_legal_edges()
    assert edges
    for src, dst, when in edges:
        tr = sm.validate_transition(src, dst, when=when)
        assert tr.source == src and tr.target == dst


def test_illegal_transition_rejected(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    with pytest.raises(TransitionError):
        sm.validate_transition("received", "completed")


@pytest.mark.parametrize("term", ["completed", "completed_with_review", "blocked", "failed"])
def test_terminal_immutable(repo_root, term):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    with pytest.raises(TransitionError):
        sm.validate_transition(term, "received")


def test_thresholds_distinct(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    assert sm.extraction_abort_threshold == 0.70
    assert sm.stage_transition_confidence_min == 0.90
    assert sm.extraction_abort_threshold < sm.stage_transition_confidence_min


def test_policy_note_denial(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    decision = evaluate_policy(
        sm,
        extraction_confidence=0.95,
        crm={
            "status": "matched",
            "match_basis": "email",
            "current_stage": "discovery_scheduled",
        },
        policy_inputs={
            "note_write_request": True,
            "stage_write_request": False,
            "force_note_denied": True,
        },
        extraction_result=None,
    )
    assert decision.note_write == "blocked"
    assert "NOTE_WRITE_BLOCKED" in decision.reason_codes
    assert decision.any_permitted is False


def test_note_only_path(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    decision = evaluate_policy(
        sm,
        extraction_confidence=0.82,
        crm={
            "status": "matched",
            "match_basis": "email",
            "current_stage": "discovery_scheduled",
        },
        policy_inputs={
            "note_write_request": True,
            "stage_write_request": True,
            "recommended_stage": "discovery_complete",
        },
        extraction_result={
            "opportunity_signal": {
                "recommended_stage": "discovery_complete",
                "rationale": "x",
            }
        },
    )
    assert decision.note_write == "allowed"
    assert decision.stage_write == "blocked"
    assert "STAGE_TRANSITION_NOT_ALLOWED" in decision.reason_codes
    intents = bound_intents(decision)
    assert len(intents["note"]) == 1
    assert len(intents["stage"]) == 0


def test_stage_allowed_path(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    decision = evaluate_policy(
        sm,
        extraction_confidence=0.95,
        crm={
            "status": "matched",
            "match_basis": "email",
            "current_stage": "discovery_scheduled",
        },
        policy_inputs={
            "note_write_request": True,
            "stage_write_request": True,
            "recommended_stage": "discovery_complete",
        },
        extraction_result=None,
    )
    assert decision.stage_write == "allowed"
    intents = bound_intents(decision)
    assert len(intents["stage"]) == 1


def test_mutation_intent_bounds(repo_root):
    sm = StateMachine.from_yaml(repo_root / "contracts" / "workflow_states.yaml")
    decision = evaluate_policy(
        sm,
        extraction_confidence=0.95,
        crm={
            "status": "matched",
            "match_basis": "email",
            "current_stage": "discovery_scheduled",
        },
        policy_inputs={
            "note_write_request": True,
            "stage_write_request": True,
            "recommended_stage": "discovery_complete",
        },
        extraction_result=None,
    )
    intents = bound_intents(decision, max_note=1, max_stage=1)
    assert len(intents["note"]) <= 1
    assert len(intents["stage"]) <= 1


def test_replay_registry():
    reg = RunRegistry()
    assert not reg.is_terminal("r1")
    reg.mark_terminal("r1", "completed")
    assert reg.is_terminal("r1")
