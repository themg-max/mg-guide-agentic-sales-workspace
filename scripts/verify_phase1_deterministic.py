#!/usr/bin/env python3
"""Deterministic Phase 1 verification for meeting_follow_up_v1."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, List, Tuple

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from orchestration.policy import bound_intents, evaluate_policy
from orchestration.runner import WorkflowRunner
from orchestration.state_machine import StateMachine

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_yaml_parse() -> None:
    for path in [
        REPO_ROOT / "contracts" / "workflow_states.yaml",
        REPO_ROOT / "contracts" / "failure_codes.yaml",
        REPO_ROOT / "governance" / "PROOF_RETURN.schema.yaml",
        REPO_ROOT / "proof" / "phase1" / "proof-return.yaml",
    ]:
        load_yaml(path)
    print("YAML parse: PASS")


def validate_packet_schema() -> None:
    schema_path = REPO_ROOT / "contracts" / "meeting_follow_up_packet.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    resource = Resource.from_contents(schema)
    registry = Registry().with_resource(schema["$id"], resource)
    validator = Draft202012Validator(schema, registry=registry)
    runner = WorkflowRunner()
    fixtures: List[Tuple[str, str]] = [
        ("transcript-success.expected.json", "completed"),
        ("transcript-ambiguous-contact.expected.json", "blocked"),
        ("transcript-no-stage-change.expected.json", "completed_with_review"),
    ]
    for fixture_name, expected_state in fixtures:
        result = runner.run_fixture(REPO_ROOT / "fixtures" / fixture_name)
        if not result.validation_ok:
            raise AssertionError(f"fixture failed validation: {fixture_name}")
        if result.final_state != expected_state:
            raise AssertionError(
                f"fixture {fixture_name} expected state {expected_state} got {result.final_state}"
            )
        validator.validate(result.packet)
    print("Packet schema validation: PASS")


def validate_fixture_outcomes() -> None:
    fixtures: List[Tuple[str, str, List[str], Tuple[int, int]]] = [
        ("transcript-success.expected.json", "completed", [], (1, 1)),
        ("transcript-ambiguous-contact.expected.json", "blocked", ["AMBIGUOUS_CONTACT"], (0, 0)),
        ("transcript-no-stage-change.expected.json", "completed_with_review", ["STAGE_TRANSITION_NOT_ALLOWED"], (1, 0)),
    ]
    for fixture_name, expected_state, expected_codes, bounds in fixtures:
        result = WorkflowRunner().run_fixture(REPO_ROOT / "fixtures" / fixture_name)
        if result.final_state != expected_state:
            raise AssertionError(
                f"fixture outcome mismatch for {fixture_name}: expected {expected_state} got {result.final_state}"
            )
        for code in expected_codes:
            if code not in result.reason_codes:
                raise AssertionError(f"missing reason code {code} for {fixture_name}")
        note_n = len(result.mutation_intents.get("note") or [])
        stage_n = len(result.mutation_intents.get("stage") or [])
        if note_n > bounds[0] or stage_n > bounds[1]:
            raise AssertionError(
                f"mutation intent bounds exceeded for {fixture_name}: {note_n}/{stage_n} > {bounds}"
            )
        if expected_state == "blocked" and "AMBIGUOUS_CONTACT" in expected_codes:
            if note_n != 0 or stage_n != 0:
                raise AssertionError(f"blocked fixture should have zero intents: {fixture_name}")
        if expected_state == "completed_with_review":
            if stage_n != 0:
                raise AssertionError(f"review fixture should have zero stage intents: {fixture_name}")
    print("Three fixture outcomes: PASS")


def validate_replay_idempotency() -> None:
    fixture_path = REPO_ROOT / "fixtures" / "transcript-success.expected.json"
    first_runner = WorkflowRunner()
    first = first_runner.run_fixture(fixture_path, created_at="2026-08-11T15:00:00Z")
    second_runner = WorkflowRunner()
    second = second_runner.run_fixture(fixture_path, created_at="2026-08-11T15:00:00Z")
    if first.final_state != second.final_state:
        raise AssertionError("replay changed terminal state")
    if first.reason_codes != second.reason_codes:
        raise AssertionError("replay changed reason codes")
    if first.mutation_intents != second.mutation_intents:
        raise AssertionError("replay changed mutation intents")
    if first.external_effects != second.external_effects:
        raise AssertionError("replay changed external effects")
    packet_a = deepcopy(first.packet)
    packet_b = deepcopy(second.packet)
    packet_a["audit"] = {**packet_a["audit"], "completed_at": "X"}
    packet_b["audit"] = {**packet_b["audit"], "completed_at": "X"}
    if packet_a != packet_b:
        raise AssertionError("replay changed packet contents")

    duplicate_runner = WorkflowRunner()
    duplicate_first = duplicate_runner.run_fixture(fixture_path)
    duplicate_second = duplicate_runner.run_fixture(fixture_path)
    if not duplicate_first.validation_ok:
        raise AssertionError("initial duplicate probe should validate")
    if not duplicate_second.rejected_duplicate:
        raise AssertionError("duplicate run should be rejected")
    print("Replay / idempotency: PASS")


def validate_mutation_intent_bounds() -> None:
    sm = StateMachine.from_yaml(REPO_ROOT / "contracts" / "workflow_states.yaml")
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
    if len(intents["note"]) > 1 or len(intents["stage"]) > 1:
        raise AssertionError("mutation intent bounds violated")
    print("Mutation intent bounds: PASS")


def validate_proof_return_schema() -> None:
    schema = load_yaml(REPO_ROOT / "governance" / "PROOF_RETURN.schema.yaml")
    payload = load_yaml(REPO_ROOT / "proof" / "phase1" / "proof-return.yaml")
    validator = Draft202012Validator(schema)
    validator.validate(payload)
    print("Proof-return schema validation: PASS")


def main() -> int:
    validate_yaml_parse()
    validate_packet_schema()
    validate_fixture_outcomes()
    validate_replay_idempotency()
    validate_mutation_intent_bounds()
    validate_proof_return_schema()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
