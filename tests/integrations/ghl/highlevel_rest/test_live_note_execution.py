from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Mapping

import pytest
from google.adk.events import Event, EventActions

import integrations.ghl.at1_execution_store as at1_execution_store
import integrations.ghl.highlevel_rest.live_note_execution as execution
import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest import BindingError, NotePathAdapter, TransportError
from integrations.ghl.highlevel_rest.live_note_execution import (
    ExecutionMode,
    FROZEN_NOTE_BODY_SHA256,
    FROZEN_NOTE_CONTENT_LOGICAL_SHA256,
    FROZEN_PROVIDER_BODY_SHA256,
    FROZEN_TRANSCRIPT_SHA256,
    IMPLEMENTATION_AUTHORIZATION_ID,
    OFFLINE_SIMULATION_AUTHORITY_ID,
    OfflineSimulationWindow,
    REFUSE_BEFORE_SECRET_MANAGER_ACCESS,
    LiveNoteExecutionContractError,
    accumulate_local_adk_events,
    build_sanitized_terminal_report,
    derive_note_contract_and_frozen_digests,
    main,
    map_hosted_result_to_note_contract,
    require_frozen_digest_match,
    require_governance_preflight,
    run_offline_harness,
)
from integrations.ghl.highlevel_rest.live_note_credential_provider import (
    GoogleSecretManagerLiveNoteSecretAccessor,
)
from integrations.ghl.highlevel_rest.live_note_http_client import (
    ConcreteLiveNoteHttpClient,
    StdlibLiveNoteHttpSession,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    BoundedLiveNoteTransport,
    InjectedLiveNoteCredential,
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
MODULE_SOURCE = (
    REPO_ROOT
    / "src"
    / "integrations"
    / "ghl"
    / "highlevel_rest"
    / "live_note_execution.py"
).read_text(encoding="utf-8")
EXPECTED_FIXTURE = json.loads(
    (REPO_ROOT / "fixtures" / "transcript-success.expected.json").read_text(
        encoding="utf-8"
    )
)
TRANSCRIPT_BYTES = (REPO_ROOT / "fixtures" / "transcript-success.txt").read_bytes()
NOW = datetime(2026, 8, 31, 20, 0, tzinfo=timezone.utc)
RUN_ID = "synthetic-pass2-run-001"
SYNTHETIC_CONTACT_ID = "synthetic-contact-001"
SYNTHETIC_LOCATION_ID = "synthetic-location-001"
SYNTHETIC_NOTE_ID = "synthetic-note-001"
EXPECTED_NOTE_FIELDS = {
    "SYNTHETIC_MARKER",
    "meeting_id",
    "meeting_summary",
    "needs",
    "objections",
    "commitments",
    "next_step",
    "opportunity_signal",
    "workflow_id",
    "transcript_hash",
}
EFFECT_COUNTER_NAMES = (
    "NETWORK_CALLS",
    "REAL_SECRET_READS",
    "REAL_GHL_CALLS",
    "REAL_CRM_MUTATIONS",
    "PROVIDER_DISPATCH_ATTEMPTS",
    "CREDENTIAL_MATERIALIZATION_ATTEMPTS",
    "SECRET_ACCESS_ATTEMPTS",
    "LIVE_GHL_ATTEMPTS",
)


@pytest.fixture(autouse=True)
def _reset_test_state() -> None:
    execution._reset_attempt_counters_for_tests()
    note_path_module._reset_shared_test_ledger()


def _window(
    *,
    authorization_identity: str = OFFLINE_SIMULATION_AUTHORITY_ID,
    run_id: str = RUN_ID,
    not_before: datetime = NOW - timedelta(minutes=1),
    expires_at: datetime = NOW + timedelta(minutes=1),
) -> OfflineSimulationWindow:
    return OfflineSimulationWindow(
        authorization_identity=authorization_identity,
        run_id=run_id,
        not_before=not_before,
        expires_at=expires_at,
    )


def _hosted_success_result() -> dict[str, object]:
    extraction = deepcopy(EXPECTED_FIXTURE["extraction_result"])
    meeting = deepcopy(EXPECTED_FIXTURE["meeting"])
    participants = deepcopy(EXPECTED_FIXTURE["participants"])
    evidence_references = deepcopy(EXPECTED_FIXTURE["evidence_references"])
    return {
        "session": {
            "workflow": "meeting_follow_up_v1",
            "agent_trace": [
                {
                    "agent_id": "meeting_context_agent",
                    "status": "ok",
                    "output_schema": "meeting_context_v1",
                    "error": None,
                    "external_effects": 0,
                },
                {
                    "agent_id": "relationship_context_agent",
                    "status": "ok",
                    "output_schema": "relationship_context_v1",
                    "error": None,
                    "external_effects": 0,
                },
                {
                    "agent_id": "follow_up_planning_agent",
                    "status": "ok",
                    "output_schema": "follow_up_proposal_v1",
                    "error": None,
                    "external_effects": 0,
                },
            ],
        },
        "meeting_context": {
            "schema": "meeting_context_v1",
            "agent": "meeting_context_agent",
            "provider": "fixture",
            "meeting": meeting,
            "participants": participants,
            "extraction": {
                "lifecycle": "complete",
                "summary": extraction["summary"],
                "needs": extraction["needs"],
                "objections": extraction["objections"],
                "commitments": extraction["commitments"],
                "next_step": extraction["next_step"],
                "opportunity_signal": extraction["opportunity_signal"],
            },
            "evidence": {
                "transcript_spans": evidence_references,
                "extraction_confidence": EXPECTED_FIXTURE["extraction_confidence"],
            },
            "external_effects": 0,
            "policy_authority": {"deterministic_policy_bypass": False},
        },
        "relationship_context": {
            "schema": "relationship_context_v1",
            "agent": "relationship_context_agent",
            "provider": "offline_ghl_fixture",
            "meeting_ref": {
                "meeting_id": meeting["meeting_id"],
                "transcript_hash": meeting["transcript_hash"],
                "run_id": EXPECTED_FIXTURE["run_id"],
            },
            "resolution": {"status": "matched"},
            "crm_source": {"mode": "offline_synthetic", "live_calls": 0, "writes": 0},
            "evidence": {},
            "external_effects": 0,
            "policy_authority": {"deterministic_policy_bypass": False},
            "longitudinal_context": {},
        },
        "follow_up_proposal": {
            "schema": "follow_up_proposal_v1",
            "agent": "follow_up_planning_agent",
            "external_effects": 0,
        },
        "follow_up_packet": {
            "schema": "meeting_follow_up_packet_v1",
            "run": {"workflow": "meeting_follow_up_v1"},
            "meeting": {
                "meeting_id": meeting["meeting_id"],
                "transcript_hash": meeting["transcript_hash"],
            },
            "extraction": {
                "summary": extraction["summary"],
                "needs": extraction["needs"],
                "objections": extraction["objections"],
                "commitments": extraction["commitments"],
                "next_step": extraction["next_step"],
                "opportunity_signal": extraction["opportunity_signal"],
            },
            "external_effects": 0,
        },
    }


def _typed_local_events(hosted_result: Mapping[str, object]) -> list[Event]:
    return [
        Event(
            author="meeting_context_agent",
            actions=EventActions(
                state_delta={"meeting_context": hosted_result["meeting_context"]}
            ),
        ),
        Event(
            author="relationship_context_agent",
            actions=EventActions(
                state_delta={"relationship_context": hosted_result["relationship_context"]}
            ),
        ),
        Event(
            author="follow_up_planning_agent",
            actions=EventActions(
                state_delta={
                    "follow_up_proposal": hosted_result["follow_up_proposal"],
                    "follow_up_packet": hosted_result["follow_up_packet"],
                }
            ),
        ),
    ]

def _offline_stack(
    session: execution._OfflineThreeCallSession | None = None,
) -> tuple[
    NotePathAdapter,
    BoundedLiveNoteTransport,
    ConcreteLiveNoteHttpClient,
    execution._OfflineThreeCallSession,
]:
    """Build the production stack through the module, never through test code."""

    return execution._build_offline_note_path_stack(session)


def _drive(
    *,
    adapter: NotePathAdapter,
    transport: BoundedLiveNoteTransport,
    client: ConcreteLiveNoteHttpClient,
    note_contract: Mapping[str, object],
) -> execution._OfflineProviderSimulation:
    """Call the module's C6 driver. The drive itself lives in production code."""

    return execution._drive_offline_note_path(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=note_contract,
        digest=require_frozen_digest_match(
            note_contract, transcript_text=TRANSCRIPT_BYTES
        ),
    )


def _typed_note_contract_from_events(
    hosted_result: Mapping[str, object],
) -> dict[str, object]:
    hosted_result = accumulate_local_adk_events(
        events=_typed_local_events(hosted_result)
    )
    return map_hosted_result_to_note_contract(
        hosted_result=hosted_result,
        transcript_text=TRANSCRIPT_BYTES,
    )


def _typed_note_contract() -> dict[str, object]:
    return _typed_note_contract_from_events(_hosted_success_result())


def _assert_zero_real_effects() -> None:
    for name in EFFECT_COUNTER_NAMES:
        assert getattr(execution, name) == 0, name


def _offline_run(**overrides: object) -> execution.HarnessExecutionResult:
    kwargs: dict[str, object] = {
        "mode": ExecutionMode.OFFLINE_SIMULATION,
        "authorization_identity": OFFLINE_SIMULATION_AUTHORITY_ID,
        "run_id": RUN_ID,
        "window": _window(),
        "events": _typed_local_events(_hosted_success_result()),
        "transcript_text": TRANSCRIPT_BYTES,
        "now": NOW,
    }
    kwargs.update(overrides)
    return run_offline_harness(**kwargs)  # type: ignore[arg-type]


def test_t01_three_agent_order_success() -> None:
    result = accumulate_local_adk_events(events=_typed_local_events(_hosted_success_result()))
    payload = result.payload

    assert [entry["agent_id"] for entry in payload["session"]["agent_trace"]] == list(
        execution.REQUIRED_AGENT_SEQUENCE
    )
    _assert_zero_real_effects()


def test_t02_agent_order_mismatch_fails_closed() -> None:
    events = _typed_local_events(_hosted_success_result())
    swapped = [events[1], events[0], events[2]]

    with pytest.raises(LiveNoteExecutionContractError, match="author mismatch"):
        accumulate_local_adk_events(events=swapped)
    with pytest.raises(LiveNoteExecutionContractError, match="author mismatch"):
        map_hosted_result_to_note_contract(
            hosted_result=accumulate_local_adk_events(events=swapped),
            transcript_text=TRANSCRIPT_BYTES,
        )
    _assert_zero_real_effects()


def test_t03_missing_or_unknown_agent_fails_closed() -> None:
    events = _typed_local_events(_hosted_success_result())

    with pytest.raises(
        LiveNoteExecutionContractError, match="exactly three events are required"
    ):
        accumulate_local_adk_events(events=events[:2])

    unknown = [
        Event(
            author="unknown_agent",
            actions=EventActions(state_delta={"meeting_context": {}}),
        ),
        events[1],
        events[2],
    ]
    with pytest.raises(LiveNoteExecutionContractError, match="author mismatch"):
        map_hosted_result_to_note_contract(
            hosted_result=accumulate_local_adk_events(events=unknown),
            transcript_text=TRANSCRIPT_BYTES,
        )
    _assert_zero_real_effects()


def test_t04_ten_field_contract_from_typed_events() -> None:
    note_contract = _typed_note_contract()

    assert set(note_contract) == EXPECTED_NOTE_FIELDS
    assert note_contract["SYNTHETIC_MARKER"] == note_path_module._MARKER
    assert note_contract["workflow_id"] == note_path_module._WORKFLOW_ID
    assert note_contract["meeting_id"] == EXPECTED_FIXTURE["meeting"]["meeting_id"]
    assert note_contract["meeting_summary"] == EXPECTED_FIXTURE["extraction_result"]["summary"]
    assert note_contract["needs"] == EXPECTED_FIXTURE["extraction_result"]["needs"]
    assert note_contract["objections"] == EXPECTED_FIXTURE["extraction_result"]["objections"]
    assert note_contract["commitments"] == EXPECTED_FIXTURE["extraction_result"]["commitments"]
    assert note_contract["next_step"] == EXPECTED_FIXTURE["extraction_result"]["next_step"]
    assert note_contract["opportunity_signal"] == EXPECTED_FIXTURE["extraction_result"][
        "opportunity_signal"
    ]
    assert note_contract["transcript_hash"] == FROZEN_TRANSCRIPT_SHA256
    _assert_zero_real_effects()


def test_t05_missing_structured_field_fails_closed_before_secret() -> None:
    hosted_result = _hosted_success_result()
    del hosted_result["follow_up_packet"]["extraction"]["summary"]  # type: ignore[index]

    with pytest.raises(LiveNoteExecutionContractError, match="extraction.summary"):
        _typed_note_contract_from_events(hosted_result)
    _assert_zero_real_effects()


def test_t06_all_frozen_digests_match() -> None:
    note_contract, digest = derive_note_contract_and_frozen_digests(
        hosted_result=accumulate_local_adk_events(
            events=_typed_local_events(_hosted_success_result())
        ),
        transcript_text=TRANSCRIPT_BYTES,
    )

    assert set(note_contract) == EXPECTED_NOTE_FIELDS
    assert digest.transcript_sha256 == FROZEN_TRANSCRIPT_SHA256
    assert digest.note_content_logical_sha256 == FROZEN_NOTE_CONTENT_LOGICAL_SHA256
    assert digest.note_body_sha256 == FROZEN_NOTE_BODY_SHA256
    assert digest.provider_body_sha256 == FROZEN_PROVIDER_BODY_SHA256
    assert digest.transcript_sha256_match is True
    assert digest.note_body_sha256_match is True
    _assert_zero_real_effects()


def test_t07_digest_mismatch_fails_before_secret_access() -> None:
    note_contract = _typed_note_contract()
    note_contract["meeting_summary"] = "tampered"

    with pytest.raises(
        LiveNoteExecutionContractError,
        match="R2 offline digest closure failed: NOTE_CONTENT_LOGICAL_SHA256",
    ):
        require_frozen_digest_match(note_contract, transcript_text=TRANSCRIPT_BYTES)
    _assert_zero_real_effects()


def test_t08_missing_window_fails_closed() -> None:
    result = _offline_run(window=None, events=())

    assert result.exit_code == 2
    assert result.report["GOVERNANCE_PREFLIGHT_STATE"] == "REFUSED"
    assert result.report["TERMINAL_RESULT"] == "REFUSE_GOVERNANCE_PREFLIGHT"
    _assert_zero_real_effects()


def test_t09_expired_window_fails_closed() -> None:
    result = _offline_run(
        window=_window(
            not_before=NOW - timedelta(minutes=2),
            expires_at=NOW - timedelta(minutes=1),
        ),
        events=(),
    )

    assert result.exit_code == 2
    assert result.report["GOVERNANCE_PREFLIGHT_STATE"] == "REFUSED"
    _assert_zero_real_effects()


def test_t10_absent_private_origin_refuses_before_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _missing_private_origin() -> None:
        raise execution.live_note_runtime.LiveNoteRuntimeAssemblyError("unavailable")

    def _unexpected_runtime_assembly(**_: object) -> None:
        execution._fail_if_credential_materialization_touched()

    monkeypatch.setattr(
        execution.live_note_runtime,
        "compose_root_owned_private_origin",
        _missing_private_origin,
    )
    monkeypatch.setattr(
        execution.live_note_runtime,
        "assemble_bound_live_note_runtime",
        _unexpected_runtime_assembly,
    )

    # The offline R5 gate refuses the live continuation before any secret.
    offline = _offline_run()
    assert offline.exit_code == 2
    assert offline.report["TERMINAL_RESULT"] == REFUSE_BEFORE_SECRET_MANAGER_ACCESS
    assert offline.report["FAILURE_CLASS"] == "PRIVATE_ORIGIN_UNAVAILABLE"
    assert offline.report["R5_RESOLVED"] == "NO"
    assert offline.report["LIVE_EXECUTION_BLOCKED"] == "YES"

    # Live mode refuses even earlier, before the gate is reached at all.
    live = _offline_run(mode=ExecutionMode.LIVE)
    assert live.exit_code == 2
    assert live.report["TERMINAL_RESULT"] == REFUSE_BEFORE_SECRET_MANAGER_ACCESS
    assert live.report["R5_RESOLVED"] == "NO"
    assert live.report["LIVE_EXECUTION_BLOCKED"] == "YES"
    _assert_zero_real_effects()


def test_t11_wrong_authorization_or_run_binding_fails_closed() -> None:
    with pytest.raises(LiveNoteExecutionContractError, match="authorization identity"):
        require_governance_preflight(
            mode=ExecutionMode.OFFLINE_SIMULATION,
            authorization_identity="wrong-authorization",
            run_id=RUN_ID,
            window=_window(authorization_identity="wrong-authorization"),
            now=NOW,
        )
    with pytest.raises(LiveNoteExecutionContractError, match="must match"):
        require_governance_preflight(
            mode=ExecutionMode.OFFLINE_SIMULATION,
            authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
            run_id=RUN_ID,
            window=_window(run_id="synthetic-other-run-001"),
            now=NOW,
        )
    _assert_zero_real_effects()


def test_t12_contact_mismatch_prevents_post() -> None:
    session = execution._OfflineThreeCallSession(
        contact_id="synthetic-other-contact-001"
    )
    adapter, transport, client, session = _offline_stack(session)

    with pytest.raises(BindingError, match="contact id does not match"):
        _drive(
            adapter=adapter,
            transport=transport,
            client=client,
            note_contract=_typed_note_contract(),
        )

    assert [method for method, _path in session.calls] == ["GET"]
    assert transport.post_attempts == 0
    _assert_zero_real_effects()


def test_t13_uncertain_create_prevents_retry_and_readback() -> None:
    session = execution._OfflineThreeCallSession(uncertain_post=True)
    adapter, transport, client, session = _offline_stack(session)

    with pytest.raises(TransportError, match="ambiguous note POST result"):
        _drive(
            adapter=adapter,
            transport=transport,
            client=client,
            note_contract=_typed_note_contract(),
        )

    assert [method for method, _path in session.calls] == ["GET", "POST"]
    assert transport.post_attempts == 1
    assert transport.get_attempts == 0
    _assert_zero_real_effects()


def test_t14_readback_uses_same_run_note_id_only() -> None:
    session = execution._OfflineThreeCallSession(note_id="synthetic-same-run-note-001")
    adapter, transport, client, session = _offline_stack(session)

    _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )

    assert session.calls[-1][1] == (
        "/contacts/synthetic-contact-001/notes/synthetic-same-run-note-001"
    )
    assert len(session.calls) == 3
    _assert_zero_real_effects()


def test_t15_sanitized_report_is_default_deny() -> None:
    adapter, transport, client, _session = _offline_stack()
    note_contract = _typed_note_contract()
    digest = require_frozen_digest_match(
        note_contract, transcript_text=TRANSCRIPT_BYTES
    )
    simulation = _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=note_contract,
    )
    report = build_sanitized_terminal_report(
        run_id=RUN_ID,
        timestamp=NOW,
        governance_preflight_state="PASS",
        hosted_attribution_gate_state="PASS",
        hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
        terminal_result="OFFLINE_SIMULATION_PASS",
        failure_class="NONE",
        digest=digest,
        simulation=simulation,
    )
    serialized = json.dumps(report, sort_keys=True)

    assert set(report) == execution._SANITIZED_REPORT_KEYS
    assert "synthetic-contact-001" not in serialized
    assert "synthetic-location-001" not in serialized
    assert "synthetic-note-001" not in serialized
    assert execution._OFFLINE_CREDENTIAL_PAYLOAD not in serialized
    assert report["NOTE_ID_PRESENT"] == "YES"
    assert report["CONTACT_MATCH"] == "YES"
    assert report["LOCATION_MATCH"] == "YES"
    assert report["SIMULATED_PROVIDER_CALLS"] == 3
    assert report["SIMULATED_MUTATIONS"] == 1
    assert report["TRANSCRIPT_SHA256_MATCH"] is True


def test_t16_exact_three_call_success_simulation() -> None:
    adapter, transport, client, session = _offline_stack()

    simulation = _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )

    assert simulation.provider_calls == 3
    assert simulation.mutations == 1
    assert [method for method, _path in session.calls] == ["GET", "POST", "GET"]
    _assert_zero_real_effects()


def test_t17_at_most_one_mutation() -> None:
    adapter, transport, client, _session = _offline_stack()

    simulation = _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )

    assert simulation.mutations == 1
    assert transport.total_mutation_calls == 1
    with pytest.raises(TransportError, match="exactly one note POST"):
        adapter.create_meeting_note(_typed_note_contract())
    assert transport.total_mutation_calls == 1
    _assert_zero_real_effects()


def test_t18_no_forbidden_provider_operations() -> None:
    adapter, transport, client, session = _offline_stack()

    _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )

    assert [path for _method, path in session.calls] == [
        "/contacts/synthetic-contact-001",
        "/contacts/synthetic-contact-001/notes",
        "/contacts/synthetic-contact-001/notes/synthetic-note-001",
    ]
    assert all("?" not in path for _method, path in session.calls)
    assert transport.contact_get_attempts == 1
    assert transport.post_attempts == 1
    assert transport.get_attempts == 1
    assert len(client.call_history) == 3
    for forbidden in (
        "retry",
        "search",
        "list",
        "pagination",
        "fallback",
        "stage",
        "delete",
        "update_note",
    ):
        assert f"def {forbidden}" not in MODULE_SOURCE
    _assert_zero_real_effects()


def test_t19_no_real_network_or_secret_manager_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fail_network_if_touched(**_: object) -> None:
        execution._fail_if_live_ghl_touched()

    def _fail_secret_if_touched(**_: object) -> None:
        execution._fail_if_secret_access_touched()

    monkeypatch.setattr(
        StdlibLiveNoteHttpSession,
        "request",
        _fail_network_if_touched,
    )
    monkeypatch.setattr(
        GoogleSecretManagerLiveNoteSecretAccessor,
        "read_secret_payload",
        _fail_secret_if_touched,
    )
    adapter, transport, client, _session = _offline_stack()

    _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )

    result = execution.run_offline_simulation_cli("transcript-success")
    assert result.exit_code == 0
    _assert_zero_real_effects()


def test_cross_agent_provenance_mismatches_fail_closed() -> None:
    hosted_result = _hosted_success_result()
    hosted_result["relationship_context"]["meeting_ref"]["meeting_id"] = "other-meeting"  # type: ignore[index]
    with pytest.raises(
        LiveNoteExecutionContractError,
        match="cross-agent provenance mismatch: meeting_id",
    ):
        _typed_note_contract_from_events(hosted_result)

    hosted_result = _hosted_success_result()
    hosted_result["follow_up_packet"]["meeting"]["transcript_hash"] = "different-hash"  # type: ignore[index]
    with pytest.raises(
        LiveNoteExecutionContractError,
        match="cross-agent provenance mismatch: transcript_hash",
    ):
        _typed_note_contract_from_events(hosted_result)


def test_serialized_or_mapping_events_are_rejected_before_mapping() -> None:
    with pytest.raises(
        LiveNoteExecutionContractError,
        match=execution.HOSTED_STREAM_QUERY_NORMALIZATION_REFUSED,
    ):
        accumulate_local_adk_events(events=[_hosted_success_result()])
    with pytest.raises(
        LiveNoteExecutionContractError,
        match="must originate from typed local ADK events",
    ):
        map_hosted_result_to_note_contract(
            hosted_result=_hosted_success_result(),
            transcript_text=TRANSCRIPT_BYTES,
        )
    with pytest.raises(
        LiveNoteExecutionContractError,
        match="must originate from typed local ADK events",
    ):
        derive_note_contract_and_frozen_digests(
            hosted_result=_hosted_success_result(),
            transcript_text=TRANSCRIPT_BYTES,
        )
    _assert_zero_real_effects()


# --- Repair coverage required by the approved Lane A repair plan (S8) ---


def test_no_direct_digest_implementation_in_module() -> None:
    """Lane A must contain no digest implementation of its own."""

    for forbidden in ("hashlib", "hexdigest", ".digest(", "sha1", "blake2", "md5"):
        assert forbidden not in MODULE_SOURCE, forbidden
    assert "import sha256" not in MODULE_SOURCE
    assert "sha256(" not in MODULE_SOURCE


def test_frozen_body_and_transcript_closure_uses_execution_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Both byte-level frozen values close through the existing store helper."""

    recorded: list[dict[str, object]] = []
    original = at1_execution_store.At1ExecutionStore.record_prewrite_provenance

    def _spy(self: object, **kwargs: object) -> None:
        recorded.append(dict(kwargs))
        return original(self, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(
        at1_execution_store.At1ExecutionStore, "record_prewrite_provenance", _spy
    )

    digest = require_frozen_digest_match(
        _typed_note_contract(), transcript_text=TRANSCRIPT_BYTES
    )

    assert digest.note_body_sha256 == FROZEN_NOTE_BODY_SHA256
    assert len(recorded) == 1
    assert recorded[0]["transcript_sha256"] == FROZEN_TRANSCRIPT_SHA256
    assert recorded[0]["expected_note_sha256"] == FROZEN_NOTE_BODY_SHA256

    # Tampered transcript bytes fail closed with no digest code in Lane A.
    tampered_transcript = TRANSCRIPT_BYTES + b"tamper"
    with pytest.raises(
        LiveNoteExecutionContractError, match="R2 offline digest closure failed"
    ):
        require_frozen_digest_match(
            _typed_note_contract(), transcript_text=tampered_transcript
        )

    # Tampered note body fails closed through the same helper.
    tampered_contract = _typed_note_contract()
    tampered_contract["meeting_summary"] = "tampered body"
    evaluated = execution.evaluate_frozen_digests(
        tampered_contract, transcript_text=TRANSCRIPT_BYTES
    )
    assert evaluated.note_body_sha256_match is False
    assert evaluated.note_body_sha256 == execution._UNVERIFIED_BY_EXECUTION_STORE
    _assert_zero_real_effects()


def test_c6_reached_through_harness_not_tests() -> None:
    """Deleting the tests would not remove C6: the harness drives it itself."""

    result = execution.run_offline_simulation_cli("transcript-success")

    assert result.exit_code == 0
    assert result.report["TERMINAL_RESULT"] == "OFFLINE_SIMULATION_PASS"
    assert result.report["SIMULATED_PROVIDER_CALLS"] == 3
    assert result.report["SIMULATED_MUTATIONS"] == 1
    assert result.report["NOTE_ID_PRESENT"] == "YES"
    assert result.report["CONTACT_MATCH"] == "YES"
    assert result.report["LOCATION_MATCH"] == "YES"
    assert result.report["PROVIDER_PATH_EXECUTION_CLASS"] == (
        "SIMULATED_OFFLINE_NO_LIVE_WRITE"
    )
    # C6 lives in the production module, not in this test module.
    assert "_drive_offline_note_path" in MODULE_SOURCE
    assert "_build_offline_note_path_stack" in MODULE_SOURCE
    assert "_OfflineThreeCallSession" in MODULE_SOURCE
    _assert_zero_real_effects()


def test_gate_order_c2_c3_c4_c5_then_r5(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each earlier gate failure prevents every later gate from running."""

    order: list[str] = []
    original_accumulate = execution.accumulate_local_adk_events
    original_derive = execution.derive_note_contract_and_frozen_digests
    original_origin = execution.require_private_origin_materialization
    original_simulation = execution.run_offline_provider_simulation

    def _accumulate(**kwargs: object) -> object:
        order.append("C3")
        return original_accumulate(**kwargs)  # type: ignore[arg-type]

    def _derive(**kwargs: object) -> object:
        order.append("C4_C5")
        return original_derive(**kwargs)  # type: ignore[arg-type]

    def _origin() -> None:
        order.append("R5")
        return original_origin()

    def _simulation(**kwargs: object) -> object:
        order.append("C6")
        return original_simulation(**kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(execution, "accumulate_local_adk_events", _accumulate)
    monkeypatch.setattr(execution, "derive_note_contract_and_frozen_digests", _derive)
    monkeypatch.setattr(execution, "require_private_origin_materialization", _origin)
    monkeypatch.setattr(execution, "run_offline_provider_simulation", _simulation)

    # Full offline order.
    order.clear()
    assert execution.run_offline_simulation_cli("transcript-success").exit_code == 0
    assert order == ["C3", "C4_C5", "R5", "C6"]

    # C2 failure prevents C3, C4/C5, R5, and C6.
    order.clear()
    assert _offline_run(window=None).exit_code == 2
    assert order == []

    # C3 failure prevents C4/C5, R5, and C6.
    order.clear()
    assert _offline_run(events=()).exit_code == 2
    assert order == ["C3"]

    # C4/C5 failure prevents R5 and C6.
    order.clear()
    broken = _hosted_success_result()
    del broken["follow_up_packet"]["extraction"]["summary"]  # type: ignore[index]
    assert _offline_run(events=_typed_local_events(broken)).exit_code == 2
    assert order == ["C3", "C4_C5"]
    _assert_zero_real_effects()


def test_offline_preflight_rejects_implementation_authorization() -> None:
    """Implementation authorization is design authority, never execution authority."""

    with pytest.raises(
        LiveNoteExecutionContractError,
        match="implementation authorization is not execution authority",
    ):
        require_governance_preflight(
            mode=ExecutionMode.OFFLINE_SIMULATION,
            authorization_identity=IMPLEMENTATION_AUTHORIZATION_ID,
            run_id=RUN_ID,
            window=_window(authorization_identity=IMPLEMENTATION_AUTHORIZATION_ID),
            now=NOW,
        )

    result = _offline_run(
        authorization_identity=IMPLEMENTATION_AUTHORIZATION_ID,
        window=_window(authorization_identity=IMPLEMENTATION_AUTHORIZATION_ID),
    )
    assert result.exit_code == 2
    assert result.report["GOVERNANCE_PREFLIGHT_STATE"] == "REFUSED"
    assert result.report["ACTIVATION_003"] == "ABSENT"

    preflight = require_governance_preflight(
        mode=ExecutionMode.OFFLINE_SIMULATION,
        authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
        run_id=RUN_ID,
        window=_window(),
        now=NOW,
    )
    assert preflight.live_authority is False
    assert preflight.simulation is True
    assert preflight.activation_003 == "ABSENT"
    _assert_zero_real_effects()


def test_live_mode_refuses_before_any_secret_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Live mode never reaches a credential, secret, origin, or provider surface."""

    def _unexpected(*_args: object, **_kwargs: object) -> None:
        execution._fail_if_secret_access_touched()

    def _unexpected_origin() -> None:
        execution._fail_if_credential_materialization_touched()

    def _unexpected_stack(*_args: object, **_kwargs: object) -> None:
        execution._fail_if_provider_dispatch_touched()

    monkeypatch.setattr(
        GoogleSecretManagerLiveNoteSecretAccessor, "read_secret_payload", _unexpected
    )
    monkeypatch.setattr(
        execution.live_note_runtime,
        "compose_root_owned_private_origin",
        _unexpected_origin,
    )
    monkeypatch.setattr(
        execution, "_build_offline_note_path_stack", _unexpected_stack
    )

    with pytest.raises(
        LiveNoteExecutionContractError, match="live mode is unavailable"
    ):
        require_governance_preflight(
            mode=ExecutionMode.LIVE,
            authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
            run_id=RUN_ID,
            window=_window(),
            now=NOW,
        )

    assert main(["--mode", "live"]) == 2
    result = _offline_run(mode=ExecutionMode.LIVE)
    assert result.exit_code == 2
    assert result.report["EXECUTION_MODE"] == "live"
    assert result.report["LIVE_MODE_AVAILABLE"] == "NO"
    assert result.report["TERMINAL_RESULT"] == REFUSE_BEFORE_SECRET_MANAGER_ACCESS
    assert result.report["FAILURE_CLASS"] == "LIVE_EXECUTION_NOT_AUTHORIZED"
    assert result.report["FAIL_CLOSED_BEFORE_SECRET"] == "YES"
    assert result.report["SIMULATED_PROVIDER_CALLS"] == 0
    _assert_zero_real_effects()


def test_cli_offline_success_emits_sanitized_report(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Offline CLI exits 0 and emits exactly one allowlisted, deterministic line."""

    assert main(["--mode", "offline-simulation"]) == 0
    first = capsys.readouterr()
    assert first.err == ""
    lines = first.out.strip().splitlines()
    assert len(lines) == 1
    report = json.loads(lines[0])

    assert set(report) == execution._SANITIZED_REPORT_KEYS
    assert report["TERMINAL_RESULT"] == "OFFLINE_SIMULATION_PASS"
    assert report["EXECUTION_MODE"] == "offline-simulation"
    assert report["R5_RESOLVED"] == "NO"
    assert report["LIVE_EXECUTION_BLOCKED"] == "YES"
    assert report["TRANSCRIPT_SHA256_MATCH"] is True
    assert report["NOTE_CONTENT_LOGICAL_SHA256_MATCH"] is True
    assert report["NOTE_BODY_SHA256_MATCH"] is True
    assert report["PROVIDER_BODY_SHA256_MATCH"] is True

    assert main(["--mode", "offline-simulation", "--fixture", "transcript-success"]) == 0
    second = capsys.readouterr()
    assert second.out == first.out
    _assert_zero_real_effects()


def test_cli_rejects_raw_identifier_arguments(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Raw identifiers, secrets, tokens, and live bindings are refused as input."""

    refused_argv = (
        ["--mode", "offline-simulation", "--fixture", "contact_demo_taylor_001"],
        ["--mode", "offline-simulation", "--contact-id", "contact_demo_taylor_001"],
        ["--mode", "offline-simulation", "--token=abc123"],
        ["--mode", "offline-simulation", "--credential", "x"],
        ["--mode", "offline-simulation", "--location_id", "x"],
        ["--mode", "offline-simulation", "https://services.leadconnectorhq.com"],
        ["--mode", "offline-simulation", "projects/p/secrets/s/versions/1"],
        ["--mode", "offline-simulation", "--fixture", "a" * 40],
        ["--mode", "offline-simulation", "--fixture", "transcript-not-approved"],
        [],
    )
    for argv in refused_argv:
        assert main(list(argv)) == 2, argv
        captured = capsys.readouterr()
        report = json.loads(captured.out.strip())
        assert set(report) == execution._SANITIZED_REPORT_KEYS
        assert report["FAILURE_CLASS"] == "INVOCATION_ARGUMENTS_REJECTED"
        assert "contact_demo_taylor_001" not in captured.out
        assert "leadconnectorhq" not in captured.out
        assert captured.err == ""
    _assert_zero_real_effects()


def test_no_traceback_or_raw_content_in_any_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No forced failure leaks a traceback, exception text, or raw content."""

    forbidden_fragments = (
        "Traceback",
        "most recent call call",
        "AttemptStateError",
        "LiveNoteExecutionContractError",
        "sqlite3",
        "Taylor Morgan",
        "taylor.morgan@example-demo.test",
        "contact_demo_taylor_001",
        "opp_demo_taylor_001",
        "synthetic-contact-001",
        "synthetic-note-001",
        execution._OFFLINE_CREDENTIAL_PAYLOAD,
        execution._OFFLINE_COMMITMENT_KEY_PAYLOAD,
        execution._OFFLINE_COMMITMENT_KEY_VERSION_RESOURCE,
    )

    broken_events = _hosted_success_result()
    del broken_events["follow_up_packet"]["extraction"]["summary"]  # type: ignore[index]

    results = [
        _offline_run(window=None),
        _offline_run(events=()),
        _offline_run(events=_typed_local_events(broken_events)),
        _offline_run(),
        _offline_run(mode=ExecutionMode.LIVE),
        _offline_run(mode="not-a-mode"),
        _offline_run(now="not-a-datetime"),
        execution.run_offline_simulation_cli("transcript-success"),
    ]
    for result in results:
        serialized = json.dumps(result.report, sort_keys=True)
        for fragment in forbidden_fragments:
            assert fragment not in serialized, fragment
        assert set(result.report) == execution._SANITIZED_REPORT_KEYS

    for argv in (["--mode", "offline-simulation"], ["--mode", "live"], ["--bad"]):
        main(list(argv))
        captured = capsys.readouterr()
        assert captured.err == ""
        for fragment in forbidden_fragments:
            assert fragment not in captured.out, fragment
    _assert_zero_real_effects()


def test_pre_post_effect_counters_are_zero() -> None:
    """Real-effect counters are unchanged pre to post on every path."""

    broken_events = _hosted_success_result()
    del broken_events["follow_up_packet"]["extraction"]["summary"]  # type: ignore[index]

    paths = (
        lambda: _offline_run(window=None),
        lambda: _offline_run(events=()),
        lambda: _offline_run(events=_typed_local_events(broken_events)),
        lambda: _offline_run(),
        lambda: _offline_run(mode=ExecutionMode.LIVE),
        lambda: _offline_run(mode="not-a-mode"),
        lambda: execution.run_offline_simulation_cli("transcript-success"),
    )
    for path in paths:
        before = tuple(getattr(execution, name) for name in EFFECT_COUNTER_NAMES)
        result = path()
        after = tuple(getattr(execution, name) for name in EFFECT_COUNTER_NAMES)
        assert before == after == (0,) * len(EFFECT_COUNTER_NAMES)
        assert result.report["PRE_RUN_EFFECT_COUNTERS_ZERO"] == "YES"
        assert result.report["POST_RUN_EFFECT_COUNTERS_ZERO"] == "YES"
        assert result.report["REAL_NETWORK_CALLS"] == 0
        assert result.report["REAL_SECRET_READS"] == 0
        assert result.report["REAL_GHL_CALLS"] == 0
        assert result.report["REAL_CRM_MUTATIONS"] == 0


def test_production_entrypoint_cannot_reach_test_seams() -> None:
    """The two named test seams are unreferenced by the production module."""

    assert "_assemble_bound_live_note_runtime_for_tests" not in MODULE_SOURCE
    assert "issue_synthetic_test_capability" not in MODULE_SOURCE
    assert "_reset_shared_test_ledger" not in MODULE_SOURCE
    assert "issue_private_at8_binding_reference_for_synthetic_tests" not in MODULE_SOURCE
    assert "issue_private_at8_handoff_source_for_synthetic_tests" not in MODULE_SOURCE
    assert "_build_at8_shaped_test_capability" not in MODULE_SOURCE
    # The real structural preconditions run instead.
    assert "adapter.get_bound_contact()" in MODULE_SOURCE


def test_five_module_reuse_status_is_declared() -> None:
    """Reuse is declared truthfully: four full, one bounded at the R5 gate."""

    for module_name in (
        "note_path",
        "live_note_transport",
        "live_note_http_client",
        "live_note_credential_provider",
        "live_note_runtime",
    ):
        assert module_name in MODULE_SOURCE, module_name

    result = execution.run_offline_simulation_cli("transcript-success")
    assert result.report["FIVE_MODULE_PRODUCTION_ASSEMBLY_REUSE"] == "BLOCKED_BY_R5"
    assert result.report["R5_RESOLVED"] == "NO"
    assert result.report["R5_SAME_PROCESS_MATERIALIZATION_STATE"] == (
        "UNRESOLVED_FAIL_CLOSED"
    )
    # live_note_runtime is consumed only at the R5 gate and never assembled.
    assert "assemble_bound_live_note_runtime(" not in MODULE_SOURCE
    assert "compose_root_owned_private_origin()" in MODULE_SOURCE
    _assert_zero_real_effects()


def test_offline_stack_uses_production_classes() -> None:
    """The offline stack is production code above an offline HTTP session only."""

    adapter, transport, client, session = _offline_stack()

    assert isinstance(adapter, NotePathAdapter)
    assert isinstance(transport, BoundedLiveNoteTransport)
    assert isinstance(client, ConcreteLiveNoteHttpClient)
    assert isinstance(session, execution._OfflineThreeCallSession)
    assert adapter._execution_store is None
    assert isinstance(
        InjectedLiveNoteCredential(execution._OFFLINE_CREDENTIAL_PAYLOAD),
        InjectedLiveNoteCredential,
    )
    _assert_zero_real_effects()


def test_offline_session_refuses_a_fourth_call_or_unknown_route() -> None:
    """No retry, search, list, pagination, fallback, or stage route is servable."""

    session = execution._OfflineThreeCallSession()
    headers = {"Authorization": "Bearer offline"}

    with pytest.raises(
        LiveNoteExecutionContractError, match="refuses an unknown provider route"
    ):
        session.request(
            method="GET",
            url="https://example.invalid/contacts/synthetic-contact-001/notes?limit=10",
            headers=headers,
            body=None,
            timeout_seconds=10.0,
            allow_redirects=False,
        )

    adapter, transport, client, session = _offline_stack()
    _drive(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=_typed_note_contract(),
    )
    with pytest.raises(
        LiveNoteExecutionContractError, match="exactly three provider calls"
    ):
        session.request(
            method="GET",
            url="https://example.invalid/contacts/synthetic-contact-001",
            headers=headers,
            body=None,
            timeout_seconds=10.0,
            allow_redirects=False,
        )
    _assert_zero_real_effects()
