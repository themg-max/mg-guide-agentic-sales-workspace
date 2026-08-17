from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping

import pytest

from integrations.ghl import (
    At1ExecutionContext,
    At1ExecutionStore,
    At1LiveTransportAdapter,
    At1LiveTransportSerializer,
    BoundedAt1GhlExecutor,
    BoundedAt1Input,
    DuplicateBusinessOrdinalError,
    ExecutionClaimError,
    PostGrantControlPlaneCallRefusedError,
    RunContinuationRefusedError,
)
from integrations.ghl.bounded_at1_executor import EXACT_OPERATION_ORDER


FIXTURE_PATH = (
    Path(__file__).resolve().parents[3]
    / "fixtures"
    / "ghl"
    / "at1-live-transport-remediation.json"
)
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


class ScriptedEstablishedSession:
    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self._responses = [deepcopy(response) for response in responses]
        self.dispatch_log: list[dict[str, Any]] = []

    def execute_operation(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        self.dispatch_log.append(deepcopy(dict(request)))
        if not self._responses:
            raise AssertionError("missing scripted response")
        response = deepcopy(self._responses.pop(0))
        if response.get("id") == "__REQUEST_ID__":
            response["id"] = request["id"]
        return response


def _binding() -> BoundedAt1Input:
    return BoundedAt1Input.from_mapping(FIXTURE["binding"])


def _context() -> At1ExecutionContext:
    return At1ExecutionContext(
        note_idempotency_key="synthetic-idempotency-SENTINEL_NOTE_KEY",
        stage_idempotency_key="synthetic-idempotency-SENTINEL_STAGE_KEY",
    )


def _adapter_and_executor(
    tmp_path: Path,
    case_id: str,
    *,
    grant_run_id: str = "grant-run-at1-remediation",
    owner_id: str = "owner-1",
    grant_active: bool = True,
) -> tuple[At1LiveTransportAdapter, BoundedAt1GhlExecutor, ScriptedEstablishedSession]:
    store = At1ExecutionStore(
        db_path=tmp_path / "at1-remediation.sqlite3",
        commitment_key="synthetic-commitment-key",
    )
    session = ScriptedEstablishedSession(
        responses=list(FIXTURE["cases"][case_id]["responses"])
    )
    adapter = At1LiveTransportAdapter(
        session=session,
        store=store,
        grant_run_id=grant_run_id,
        owner_id=owner_id,
        grant_active=grant_active,
    )
    return adapter, BoundedAt1GhlExecutor(adapter), session


def test_b24_exact_serializer_contract(tmp_path: Path) -> None:
    adapter, executor, _ = _adapter_and_executor(tmp_path, "success")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "completed"
    private_attempts = adapter.store.list_private_attempts(adapter.grant_run_id)
    assert len(private_attempts) == 6

    serializer = At1LiveTransportSerializer()
    binding = _binding()
    context = _context()
    expected = [
        serializer.build_execute_operation_call(
            "get-contact",
            {"location_id": binding.location_id, "contact_id": binding.contact_id},
        ),
        serializer.build_execute_operation_call(
            "get-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
            },
        ),
        serializer.build_execute_operation_call(
            "create-note",
            {
                "location_id": binding.location_id,
                "contact_id": binding.contact_id,
                "content_or_fingerprint": binding.expected_note_content_or_fingerprint,
            },
            context,
        ),
        serializer.build_execute_operation_call(
            "get-note",
            {
                "location_id": binding.location_id,
                "contact_id": binding.contact_id,
                "note_id": "synthetic-note-SENTINEL_NOTE_ID",
            },
        ),
        serializer.build_execute_operation_call(
            "update-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
                "stage_id": binding.authorized_final_stage_id,
            },
            context,
        ),
        serializer.build_execute_operation_call(
            "get-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
            },
        ),
    ]

    assert len(private_attempts) == len(expected)
    for attempt, expected_envelope in zip(private_attempts, expected):
        assert attempt["request_envelope"] == expected_envelope
        serialized = json.dumps(attempt["request_envelope"], sort_keys=True)
        for forbidden_alias in (
            "locationId",
            "opportunityId",
            "noteId",
            "stageId",
            "content_or_fingerprint",
        ):
            assert forbidden_alias not in serialized


def test_b25_nested_mcp_failure_under_transport_success_is_terminal(
    tmp_path: Path,
) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "nested_failure_op3")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.note_writes_succeeded == 0
    assert result.further_transport_calls_authorized is False
    assert [call["arguments"]["operationId"] for call in session.dispatch_log] == [
        "get-contact",
        "get-opportunity",
        "create-note",
    ]


def test_b26_is_error_true_fails_closed(tmp_path: Path) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "is_error_op3")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.further_transport_calls_authorized is False
    assert [call["arguments"]["operationId"] for call in session.dispatch_log] == [
        "get-contact",
        "get-opportunity",
        "create-note",
    ]


def test_b27_missing_created_note_id_blocks_op4(tmp_path: Path) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "missing_note_id")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.failure_code == "NOTE_WRITE_RESPONSE_INVALID"
    assert result.note_write_attempts == 1
    assert result.business_effect_truth == "UNKNOWN"
    assert "get-note" not in [call["arguments"]["operationId"] for call in session.dispatch_log]


def test_b28_wrong_initial_stage_blocks_writes(tmp_path: Path) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "wrong_initial_stage")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.failure_code == "INITIAL_STAGE_MISMATCH"
    assert result.note_write_attempts == 0
    assert result.stage_write_attempts == 0
    assert [call["arguments"]["operationId"] for call in session.dispatch_log] == [
        "get-contact",
        "get-opportunity",
    ]


def test_b29_wrong_note_content_preserves_partial_effect_without_stage_write(
    tmp_path: Path,
) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "wrong_note_content")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.failure_code == "NOTE_READBACK_MISMATCH"
    assert result.note_readback_verified is False
    assert result.stage_write_attempts == 0
    assert result.business_effect_truth == "UNKNOWN"
    assert result.stop_and_preserve_proof is True
    assert "update-opportunity" not in [
        call["arguments"]["operationId"] for call in session.dispatch_log
    ]


def test_b30_wrong_final_stage_fails_completion_and_preserves_consumed_stage_attempt(
    tmp_path: Path,
) -> None:
    _, executor, _ = _adapter_and_executor(tmp_path, "wrong_final_stage")

    result = executor.execute(_binding(), _context())

    assert result.disposition == "failed"
    assert result.failure_code == "STAGE_READBACK_MISMATCH"
    assert result.stage_write_attempts == 1
    assert result.stage_writes_succeeded == 1
    assert result.final_stage_readback_verified is False
    assert result.business_effect_truth == "UNKNOWN"
    assert result.at1_complete is False


def test_b31_protocol_and_business_ledgers_are_separate(tmp_path: Path) -> None:
    adapter, executor, _ = _adapter_and_executor(tmp_path, "success", grant_active=False)
    adapter.record_protocol_call("initialize", {"synthetic": True})
    adapter.record_protocol_call("probe", {"synthetic": True})
    adapter.activate_grant()

    result = executor.execute(_binding(), _context())
    projection = adapter.public_projection()

    assert result.disposition == "completed"
    assert projection["protocol_call_count"] == 2
    assert projection["business_attempt_count"] == 6
    assert projection["business_call_count"] == 6


def test_b32_second_same_process_attempt_is_refused_before_transport(
    tmp_path: Path,
) -> None:
    _, executor, session = _adapter_and_executor(tmp_path, "nested_failure_op3")
    executor.execute(_binding(), _context())
    first_attempt_call_count = len(session.dispatch_log)

    _, second_executor, second_session = _adapter_and_executor(
        tmp_path,
        "success",
    )
    with pytest.raises(RunContinuationRefusedError):
        second_executor.execute(_binding(), _context())

    assert len(session.dispatch_log) == first_attempt_call_count
    assert second_session.dispatch_log == []


def test_b33_post_grant_initialize_probe_refused_locally(tmp_path: Path) -> None:
    adapter, _, session = _adapter_and_executor(tmp_path, "success")

    with pytest.raises(PostGrantControlPlaneCallRefusedError):
        adapter.record_protocol_call("initialize", {"synthetic": True})
    with pytest.raises(PostGrantControlPlaneCallRefusedError):
        adapter.record_protocol_call("probe", {"synthetic": True})

    assert session.dispatch_log == []
    assert adapter.public_projection()["protocol_call_count"] == 0


def test_b34_caller_cannot_inject_success_flags(tmp_path: Path) -> None:
    _, executor, _ = _adapter_and_executor(tmp_path, "wrong_note_content")

    with pytest.raises(TypeError):
        executor.execute(  # type: ignore[call-arg]
            _binding(),
            _context(),
            expected_initial_stage_verified=True,
        )

    result = executor.execute(_binding(), _context())
    assert result.note_readback_verified is False
    assert result.at1_complete is False


def test_b35_private_capture_and_sanitized_projection(tmp_path: Path) -> None:
    adapter, executor, _ = _adapter_and_executor(tmp_path, "success")
    executor.execute(_binding(), _context())

    private_attempts = adapter.store.list_private_attempts(adapter.grant_run_id)
    projection = adapter.public_projection()
    private_blob = json.dumps(private_attempts, sort_keys=True)
    public_blob = json.dumps(projection, sort_keys=True)

    assert "SENTINEL_CONTACT_ID" in private_blob
    assert "SENTINEL_NOTE_ID" in private_blob
    assert "SENTINEL_NOTE_CONTENT" in private_blob
    assert "SENTINEL_NOTE_KEY" in private_blob
    assert "SENTINEL_STAGE_KEY" in private_blob
    for private_sentinel in (
        "SENTINEL_CONTACT_ID",
        "SENTINEL_NOTE_ID",
        "SENTINEL_NOTE_CONTENT",
        "SENTINEL_NOTE_KEY",
        "SENTINEL_STAGE_KEY",
    ):
        assert private_sentinel not in public_blob
    assert projection["request_capture_count"] == 6
    assert projection["response_capture_count"] == 6


def test_b36_restart_persistence_and_crash_window_refusals(tmp_path: Path) -> None:
    db_path = tmp_path / "at1-remediation-restart.sqlite3"
    serializer = At1LiveTransportSerializer()
    binding = _binding()
    envelope = serializer.build_execute_operation_call(
        "get-contact",
        {"location_id": binding.location_id, "contact_id": binding.contact_id},
    )

    store_a = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session_a = ScriptedEstablishedSession(responses=list(FIXTURE["cases"]["success"]["responses"]))
    adapter_a = At1LiveTransportAdapter(
        session=session_a,
        store=store_a,
        grant_run_id="grant-run-restart",
        owner_id="owner-1",
    )
    adapter_a.dispatch(envelope)
    # Simulate executor semantic completion so the ordinal is fully resolved.
    adapter_a.record_semantic_outcome(True)
    assert len(session_a.dispatch_log) == 1

    store_b = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session_b = ScriptedEstablishedSession(responses=list(FIXTURE["cases"]["success"]["responses"]))
    adapter_b = At1LiveTransportAdapter(
        session=session_b,
        store=store_b,
        grant_run_id="grant-run-restart",
        owner_id="owner-1",
    )
    with pytest.raises(DuplicateBusinessOrdinalError):
        adapter_b.dispatch(envelope)
    assert session_b.dispatch_log == []

    store_c = At1ExecutionStore(
        db_path=tmp_path / "at1-remediation-crash-before-dispatch.sqlite3",
        commitment_key="synthetic-commitment-key",
    )
    store_c.acquire_claim("grant-run-crash-before-dispatch", "owner-1")
    store_c.record_attempt(
        grant_run_id="grant-run-crash-before-dispatch",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-1",
        request_envelope=envelope,
    )
    store_c_restarted = At1ExecutionStore(
        db_path=tmp_path / "at1-remediation-crash-before-dispatch.sqlite3",
        commitment_key="synthetic-commitment-key",
    )
    adapter_c = At1LiveTransportAdapter(
        session=ScriptedEstablishedSession(responses=[]),
        store=store_c_restarted,
        grant_run_id="grant-run-crash-before-dispatch",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter_c.dispatch(envelope)

    store_d = At1ExecutionStore(
        db_path=tmp_path / "at1-remediation-crash-after-dispatch.sqlite3",
        commitment_key="synthetic-commitment-key",
    )
    store_d.acquire_claim("grant-run-crash-after-dispatch", "owner-1")
    store_d.record_attempt(
        grant_run_id="grant-run-crash-after-dispatch",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-2",
        request_envelope=envelope,
    )
    store_d.mark_dispatched(
        grant_run_id="grant-run-crash-after-dispatch",
        operation_ordinal=1,
    )
    store_d_restarted = At1ExecutionStore(
        db_path=tmp_path / "at1-remediation-crash-after-dispatch.sqlite3",
        commitment_key="synthetic-commitment-key",
    )
    adapter_d = At1LiveTransportAdapter(
        session=ScriptedEstablishedSession(responses=[]),
        store=store_d_restarted,
        grant_run_id="grant-run-crash-after-dispatch",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter_d.dispatch(envelope)
    assert (
        adapter_d.public_projection()["business_effect_truth"] == "UNKNOWN"
    )


def test_b36a_next_ordinal_refused_after_pre_dispatch_crash(tmp_path: Path) -> None:
    """Crash after attempt record / before dispatch: OP2 must be refused before transport."""
    db_path = tmp_path / "at1-remediation-crash-before-dispatch-next.sqlite3"
    serializer = At1LiveTransportSerializer()
    binding = _binding()
    op1_envelope = serializer.build_execute_operation_call(
        "get-contact",
        {"location_id": binding.location_id, "contact_id": binding.contact_id},
    )
    op2_envelope = serializer.build_execute_operation_call(
        "get-opportunity",
        {
            "location_id": binding.location_id,
            "opportunity_id": binding.opportunity_id,
        },
    )

    store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    store.acquire_claim("grant-run-crash-before-dispatch-next", "owner-1")
    store.record_attempt(
        grant_run_id="grant-run-crash-before-dispatch-next",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-next-1",
        request_envelope=op1_envelope,
    )

    restarted_store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session = ScriptedEstablishedSession(responses=[])
    adapter = At1LiveTransportAdapter(
        session=session,
        store=restarted_store,
        grant_run_id="grant-run-crash-before-dispatch-next",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter.dispatch(op2_envelope)
    assert session.dispatch_log == []
    projection = adapter.public_projection()
    assert projection["business_effect_truth"] == "UNKNOWN"
    assert projection["business_attempt_count"] == 1
    assert projection["business_call_count"] == 0


def test_b36b_next_ordinal_refused_after_unresolved_dispatch(tmp_path: Path) -> None:
    """Crash after dispatch / before response capture: OP2 must be refused before transport."""
    db_path = tmp_path / "at1-remediation-crash-after-dispatch-next.sqlite3"
    serializer = At1LiveTransportSerializer()
    binding = _binding()
    op1_envelope = serializer.build_execute_operation_call(
        "get-contact",
        {"location_id": binding.location_id, "contact_id": binding.contact_id},
    )
    op2_envelope = serializer.build_execute_operation_call(
        "get-opportunity",
        {
            "location_id": binding.location_id,
            "opportunity_id": binding.opportunity_id,
        },
    )

    store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    store.acquire_claim("grant-run-crash-after-dispatch-next", "owner-1")
    store.record_attempt(
        grant_run_id="grant-run-crash-after-dispatch-next",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-next-2",
        request_envelope=op1_envelope,
    )
    store.mark_dispatched(
        grant_run_id="grant-run-crash-after-dispatch-next",
        operation_ordinal=1,
    )

    restarted_store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session = ScriptedEstablishedSession(responses=[])
    adapter = At1LiveTransportAdapter(
        session=session,
        store=restarted_store,
        grant_run_id="grant-run-crash-after-dispatch-next",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter.dispatch(op2_envelope)
    assert session.dispatch_log == []
    projection = adapter.public_projection()
    assert projection["business_effect_truth"] == "UNKNOWN"
    assert projection["business_attempt_count"] == 1
    assert projection["business_call_count"] == 1


def test_b36c_next_ordinal_refused_after_response_captured_pre_parse(
    tmp_path: Path,
) -> None:
    """Crash after response capture / before parse: OP2 must be refused before transport."""
    db_path = tmp_path / "at1-remediation-crash-response-pre-parse.sqlite3"
    serializer = At1LiveTransportSerializer()
    binding = _binding()
    op1_envelope = serializer.build_execute_operation_call(
        "get-contact",
        {"location_id": binding.location_id, "contact_id": binding.contact_id},
    )
    op2_envelope = serializer.build_execute_operation_call(
        "get-opportunity",
        {
            "location_id": binding.location_id,
            "opportunity_id": binding.opportunity_id,
        },
    )
    response_envelope = {
        "jsonrpc": "2.0",
        "id": "synthetic-crash-request-next-3",
        "result": {
            "isError": False,
            "structuredContent": {
                "success": True,
                "data": {"id": "SENTINEL_CONTACT_ID"},
            },
        },
    }

    store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    store.acquire_claim("grant-run-crash-response-pre-parse", "owner-1")
    store.record_attempt(
        grant_run_id="grant-run-crash-response-pre-parse",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-next-3",
        request_envelope=op1_envelope,
    )
    store.mark_dispatched(
        grant_run_id="grant-run-crash-response-pre-parse",
        operation_ordinal=1,
    )
    store.capture_response(
        grant_run_id="grant-run-crash-response-pre-parse",
        operation_ordinal=1,
        response_envelope=response_envelope,
    )

    restarted_store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session = ScriptedEstablishedSession(responses=[])
    adapter = At1LiveTransportAdapter(
        session=session,
        store=restarted_store,
        grant_run_id="grant-run-crash-response-pre-parse",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter.dispatch(op2_envelope)
    assert session.dispatch_log == []
    projection = adapter.public_projection()
    assert projection["business_effect_truth"] == "UNKNOWN"
    assert projection["business_attempt_count"] == 1
    assert projection["business_call_count"] == 1
    private = restarted_store.list_private_attempts("grant-run-crash-response-pre-parse")
    assert private[0]["state"] == "RESPONSE_CAPTURED"
    assert private[0]["parse_success"] is None
    assert private[0]["semantic_success"] is None


def test_b36d_next_ordinal_refused_after_parsed_pre_semantic(
    tmp_path: Path,
) -> None:
    """Crash after parse / before semantic: OP2 must be refused before transport."""
    db_path = tmp_path / "at1-remediation-crash-parsed-pre-semantic.sqlite3"
    serializer = At1LiveTransportSerializer()
    binding = _binding()
    op1_envelope = serializer.build_execute_operation_call(
        "get-contact",
        {"location_id": binding.location_id, "contact_id": binding.contact_id},
    )
    op2_envelope = serializer.build_execute_operation_call(
        "get-opportunity",
        {
            "location_id": binding.location_id,
            "opportunity_id": binding.opportunity_id,
        },
    )
    response_envelope = {
        "jsonrpc": "2.0",
        "id": "synthetic-crash-request-next-4",
        "result": {
            "isError": False,
            "structuredContent": {
                "success": True,
                "data": {"id": "SENTINEL_CONTACT_ID"},
            },
        },
    }

    store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    store.acquire_claim("grant-run-crash-parsed-pre-semantic", "owner-1")
    store.record_attempt(
        grant_run_id="grant-run-crash-parsed-pre-semantic",
        operation_ordinal=1,
        operation_id="get-contact",
        request_id="synthetic-crash-request-next-4",
        request_envelope=op1_envelope,
    )
    store.mark_dispatched(
        grant_run_id="grant-run-crash-parsed-pre-semantic",
        operation_ordinal=1,
    )
    store.capture_response(
        grant_run_id="grant-run-crash-parsed-pre-semantic",
        operation_ordinal=1,
        response_envelope=response_envelope,
    )
    store.record_parse_outcome(
        grant_run_id="grant-run-crash-parsed-pre-semantic",
        operation_ordinal=1,
        success=True,
    )

    restarted_store = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    session = ScriptedEstablishedSession(responses=[])
    adapter = At1LiveTransportAdapter(
        session=session,
        store=restarted_store,
        grant_run_id="grant-run-crash-parsed-pre-semantic",
        owner_id="owner-1",
    )
    with pytest.raises(RunContinuationRefusedError):
        adapter.dispatch(op2_envelope)
    assert session.dispatch_log == []
    projection = adapter.public_projection()
    assert projection["business_effect_truth"] == "UNKNOWN"
    assert projection["business_attempt_count"] == 1
    assert projection["business_call_count"] == 1
    private = restarted_store.list_private_attempts("grant-run-crash-parsed-pre-semantic")
    assert private[0]["state"] == "RESPONSE_CAPTURED"
    assert private[0]["parse_success"] is True
    assert private[0]["semantic_success"] is None


def test_b37_concurrent_atomic_claim_rejects_second_owner(tmp_path: Path) -> None:
    db_path = tmp_path / "at1-remediation-concurrent-claim.sqlite3"
    store_1 = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")
    store_2 = At1ExecutionStore(db_path=db_path, commitment_key="synthetic-commitment-key")

    store_1.acquire_claim("grant-run-concurrency", "owner-1")
    with pytest.raises(ExecutionClaimError):
        store_2.acquire_claim("grant-run-concurrency", "owner-2")
    assert store_1.compute_public_projection("grant-run-concurrency")[
        "business_call_count"
    ] == 0


def test_b38_request_response_evidence_pair_and_public_binding(tmp_path: Path) -> None:
    adapter, executor, _ = _adapter_and_executor(tmp_path, "success")
    executor.execute(_binding(), _context())

    private_attempts = adapter.store.list_private_attempts(adapter.grant_run_id)
    projection = adapter.public_projection()
    first = private_attempts[0]
    commitment = projection["request_response_commitments"][0]

    assert first["operation_ordinal"] == 1
    assert first["request_envelope"]["arguments"]["operationId"] == "get-contact"
    assert first["response_envelope"]["result"]["content"][0]["operationId"] == "get-contact"
    assert first["request_id"]
    assert commitment["operation_ordinal"] == 1
    assert commitment["request_id"] == first["request_id"]
    assert commitment["request_commitment"] == first["request_digest"]
    assert commitment["response_commitment"] == first["response_digest"]
    assert commitment["operation_id"] == EXACT_OPERATION_ORDER[0]
    public_blob = json.dumps(projection, sort_keys=True)
    assert "SENTINEL_CONTACT_ID" not in public_blob
    assert "SENTINEL_NOTE_CONTENT" not in public_blob
