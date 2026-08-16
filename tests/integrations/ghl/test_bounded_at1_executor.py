from __future__ import annotations

import json
from pathlib import Path

import pytest

from integrations.ghl import (
    BoundedAt1GhlExecutor,
    BoundedAt1Input,
    DeterministicGhlFixtureTransport,
    InputContractError,
    TerminalStateError,
    UnexpectedOperationError,
    WriteAttemptRefusedError,
)


FIXTURE_PATH = Path(__file__).resolve().parents[3] / "fixtures" / "ghl" / "at1-bounded-executor.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _binding() -> BoundedAt1Input:
    return BoundedAt1Input.from_mapping(FIXTURE["binding"])


def _executor(case_id: str) -> tuple[BoundedAt1GhlExecutor, DeterministicGhlFixtureTransport]:
    transport = DeterministicGhlFixtureTransport(FIXTURE["cases"][case_id]["calls"])
    return BoundedAt1GhlExecutor(transport), transport


def test_b1_success_uses_exact_order_and_independent_counters() -> None:
    executor, transport = _executor("success")

    result = executor.execute(_binding())

    transport.assert_exhausted()
    assert result.disposition == "completed"
    assert result.operations == (
        "get-contact",
        "get-opportunity",
        "create-note",
        "get-note",
        "update-opportunity",
        "get-opportunity",
    )
    assert result.note_write_attempts == result.note_writes_succeeded == 1
    assert result.stage_write_attempts == result.stage_writes_succeeded == 1
    assert result.note_readback_verified is True
    assert result.stage_readback_verified is True
    assert len(transport.calls) == 6


@pytest.mark.parametrize(
    ("case_id", "failure_code", "call_count", "note_attempts", "stage_attempts"),
    [
        ("contact_not_found", "CONTACT_NOT_FOUND", 1, 0, 0),
        ("opportunity_not_found", "OPPORTUNITY_NOT_FOUND", 2, 0, 0),
        ("note_write_rejected", "NOTE_WRITE_REJECTED", 3, 1, 0),
        ("note_readback_mismatch", "NOTE_READBACK_MISMATCH", 4, 1, 0),
        ("stage_write_rejected", "STAGE_WRITE_REJECTED", 5, 1, 1),
        ("stage_readback_mismatch", "STAGE_READBACK_MISMATCH", 6, 1, 1),
    ],
)
def test_b2_through_b7_fail_closed(
    case_id: str,
    failure_code: str,
    call_count: int,
    note_attempts: int,
    stage_attempts: int,
) -> None:
    executor, transport = _executor(case_id)

    result = executor.execute(_binding())

    transport.assert_exhausted()
    assert result.disposition == "failed"
    assert result.failure_code == failure_code
    assert result.note_write_attempts == note_attempts
    assert result.stage_write_attempts == stage_attempts
    assert result.further_transport_calls_authorized is False
    assert len(transport.calls) == call_count
    assert result.stop_and_preserve_proof is (
        case_id in {"note_readback_mismatch", "stage_readback_mismatch"}
    )


@pytest.mark.parametrize("case_id,write_kind", [("second_note_attempt", "note"), ("second_stage_attempt", "stage")])
def test_b8_and_b9_second_write_attempt_is_refused_before_transport(
    case_id: str, write_kind: str
) -> None:
    executor, transport = _executor(case_id)

    executor._consume_write_attempt(write_kind)
    with pytest.raises(WriteAttemptRefusedError, match="refused before transport"):
        executor._consume_write_attempt(write_kind)

    assert transport.calls == []


def test_b10_malformed_binding_is_refused_before_transport() -> None:
    malformed = {**FIXTURE["binding"], "contact_id": ""}

    with pytest.raises(InputContractError, match="non-empty"):
        BoundedAt1Input.from_mapping(malformed)


def test_b11_unexpected_operation_is_refused_by_fixture_transport() -> None:
    _, transport = _executor("unexpected_operation")

    with pytest.raises(UnexpectedOperationError, match="outside the bounded"):
        transport.dispatch("search-contacts-advanced", {})

    assert transport.calls == []


def test_b12_terminal_failure_prevents_any_further_transport_call() -> None:
    executor, transport = _executor("note_write_rejected")
    result = executor.execute(_binding())

    with pytest.raises(TerminalStateError, match="not authorized"):
        executor._dispatch("get-contact", {"location_id": "synthetic-location-at1", "contact_id": "synthetic-contact-at1"})

    assert result.further_transport_calls_authorized is False
    assert [operation for operation, _ in transport.calls] == [
        "get-contact",
        "get-opportunity",
        "create-note",
    ]
