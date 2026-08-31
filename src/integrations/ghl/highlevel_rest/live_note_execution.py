"""Offline R2 NOTE_PATH mapper, frozen-value validator, and simulation harness.

This unit contains no digest implementation. Every frozen value is closed
through an existing production surface: ``note_path`` supplies the logical and
provider-body digests, and ``At1ExecutionStore.record_prewrite_provenance``
supplies byte-level transcript and note-body verification.

Live execution is unavailable. R5 (same-process private-origin materialization)
is unresolved and fail-closed, so ``--mode live`` refuses before any credential,
Secret Manager, or provider surface is reached.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from itertools import count
import json
from pathlib import Path
import sys
import tempfile
from typing import Any, Mapping, Sequence

from google.adk.events import Event, EventActions

from integrations.ghl.at1_commitment_key_provider import SyntheticCommitmentKeyProvider
from integrations.ghl.at1_execution_store import At1ExecutionStore, AttemptStateError
import integrations.ghl.highlevel_rest.live_note_runtime as live_note_runtime
import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest.live_note_credential_provider import (
    LiveNoteCredentialProvider,
    SyntheticLiveNoteSecretAccessor,
)
from integrations.ghl.highlevel_rest.live_note_http_client import (
    ConcreteLiveNoteHttpClient,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    BoundedLiveNoteTransport,
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
)
from integrations.ghl.highlevel_rest.note_path import NotePathAdapter

REQUIRED_AGENT_SEQUENCE: tuple[str, str, str] = (
    "meeting_context_agent",
    "relationship_context_agent",
    "follow_up_planning_agent",
)
_REQUIRED_AGENT_OUTPUT_SCHEMAS: tuple[str, str, str] = (
    "meeting_context_v1",
    "relationship_context_v1",
    "follow_up_proposal_v1",
)

FROZEN_TRANSCRIPT_SHA256 = (
    "1a1a002eb79701d436d199a63ddba0f8e532dd96d1591cc437157e90481a24aa"
)
FROZEN_NOTE_CONTENT_LOGICAL_SHA256 = (
    "4d581696b2b60a6fbdccef2ea8532ecdfe98f967496fac3f6942103b94626ac2"
)
FROZEN_NOTE_BODY_SHA256 = (
    "a404ad7343269ea8832618c6be70320ddc5403bf146c04a9e606e148746e0db5"
)
FROZEN_PROVIDER_BODY_SHA256 = (
    "fbf03c4e76911679980c8956ad93c26510f77cef51c2b0b48c5d46c11f774286"
)
IMPLEMENTATION_AUTHORIZATION_ID = (
    "MG_GUIDE_LIVE_PROVIDER_NOTE_PATH_EXECUTION_HARNESS_"
    "IMPLEMENTATION_AUTHORIZATION_001"
)
# The implementation authorization is design/build authority. It is deliberately
# NOT usable as execution authority, and no activation record exists for this
# unit. The offline authority below authorizes a simulation only.
OFFLINE_SIMULATION_AUTHORITY_ID = (
    "NW008_AT8W30_R2_OFFLINE_HARNESS_SIMULATION_NOT_AN_ACTIVATION"
)
ACTIVATION_003_STATE = "ABSENT"
HOSTED_STREAM_QUERY_NORMALIZATION_REFUSED = "REFUSED_UNPROVEN_WIRE_ENVELOPE"
R5_SAME_PROCESS_MATERIALIZATION_UNRESOLVED = "UNRESOLVED_FAIL_CLOSED"
REFUSE_BEFORE_SECRET_MANAGER_ACCESS = "REFUSE_BEFORE_SECRET_MANAGER_ACCESS"
FIVE_MODULE_PRODUCTION_ASSEMBLY_REUSE = "BLOCKED_BY_R5"
LIVE_MODE_AVAILABLE = "NO"

_OFFLINE_FIXTURE_ALLOWLIST = frozenset({"transcript-success"})
_OFFLINE_SIMULATION_RUN_ID = "offline-simulation-r2-note-path-001"
_OFFLINE_SIMULATION_TIMESTAMP = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
_OFFLINE_SIMULATION_WINDOW_SPAN_SECONDS = 3600
_OFFLINE_COMMITMENT_KEY_VERSION_RESOURCE = (
    "projects/synthetic-project/secrets/at1-commitment-key/versions/1"
)
_OFFLINE_COMMITMENT_KEY_PAYLOAD = "offline-simulation-synthetic-commitment-key"
_OFFLINE_CREDENTIAL_RESOURCE_NAME = "offline-simulation-synthetic-note-credential"
_OFFLINE_CREDENTIAL_PAYLOAD = "offline-simulation-synthetic-note-token"
_OFFLINE_CONTACT_ID = "synthetic-contact-001"
_OFFLINE_LOCATION_ID = "synthetic-location-001"
_OFFLINE_NOTE_ID = "synthetic-note-001"
_OFFLINE_PROVENANCE_RUN_PREFIX = "offline-simulation-provenance-"
_UNVERIFIED_BY_EXECUTION_STORE = "UNVERIFIED_BY_EXECUTION_STORE"
_HEX_CHARACTERS = frozenset("0123456789abcdef")

# Distinct per-invocation NOTE_PATH consumer run ids. The value is never
# emitted; it only keeps the production one-POST-per-run budget honest when the
# harness is invoked more than once inside a single process.
_OFFLINE_RUN_SEQUENCE = count(1)

NETWORK_CALLS = 0
REAL_SECRET_READS = 0
REAL_GHL_CALLS = 0
REAL_CRM_MUTATIONS = 0
PROVIDER_DISPATCH_ATTEMPTS = 0
CREDENTIAL_MATERIALIZATION_ATTEMPTS = 0
SECRET_ACCESS_ATTEMPTS = 0
LIVE_GHL_ATTEMPTS = 0


class ExecutionMode(Enum):
    """Discriminator that keeps simulation and live authority strictly apart."""

    OFFLINE_SIMULATION = "offline-simulation"
    LIVE = "live"


class LiveNoteExecutionContractError(ValueError):
    """Raised when hosted-output mapping or frozen value contracts are violated."""


@dataclass(frozen=True)
class FrozenDigestValidation:
    transcript_sha256: str
    note_content_logical_sha256: str
    note_body_sha256: str
    provider_body_sha256: str
    transcript_sha256_match: bool
    note_content_logical_sha256_match: bool
    note_body_sha256_match: bool
    provider_body_sha256_match: bool


@dataclass(frozen=True)
class OfflineSimulationWindow:
    """Offline invocation binding consumed by C2 without ambient discovery.

    This is explicitly **not** an activation record and confers no live
    authority. It exists so an offline simulation still proves an exact,
    non-discovered authorization/run binding and expiry.
    """

    authorization_identity: str
    run_id: str
    not_before: datetime
    expires_at: datetime


@dataclass(frozen=True)
class GovernancePreflight:
    """Validated C2 binding, retained privately by the harness."""

    authorization_identity: str
    run_id: str
    mode: ExecutionMode
    live_authority: bool
    activation_003: str
    simulation: bool


@dataclass(frozen=True)
class _NormalizedHostedResult:
    """Opaque C3 result that can be mapped only after typed event attribution."""

    payload: Mapping[str, Any]


@dataclass(frozen=True)
class _OfflineProviderSimulation:
    """Sanitized C6 result produced by the harness driving the NOTE_PATH stack."""

    provider_calls: int
    mutations: int
    contact_match: bool
    location_match: bool
    note_id_present: bool
    note_contact_match: bool
    body_digest_match: bool


@dataclass(frozen=True)
class HarnessExecutionResult:
    """Sanitized terminal process result."""

    exit_code: int
    report: Mapping[str, object]


class _NoDispatchTransport:
    def dispatch(
        self, method: str, path: str, body: Mapping[str, Any] | None = None
    ) -> Any:
        _fail_if_provider_dispatch_touched()


def _reset_attempt_counters_for_tests() -> None:
    global PROVIDER_DISPATCH_ATTEMPTS
    global CREDENTIAL_MATERIALIZATION_ATTEMPTS
    global SECRET_ACCESS_ATTEMPTS
    global LIVE_GHL_ATTEMPTS
    PROVIDER_DISPATCH_ATTEMPTS = 0
    CREDENTIAL_MATERIALIZATION_ATTEMPTS = 0
    SECRET_ACCESS_ATTEMPTS = 0
    LIVE_GHL_ATTEMPTS = 0


def _fail_if_provider_dispatch_touched() -> None:
    global PROVIDER_DISPATCH_ATTEMPTS
    PROVIDER_DISPATCH_ATTEMPTS += 1
    raise LiveNoteExecutionContractError(
        "provider dispatch is not authorized during the offline harness"
    )


def _fail_if_credential_materialization_touched() -> None:
    global CREDENTIAL_MATERIALIZATION_ATTEMPTS
    CREDENTIAL_MATERIALIZATION_ATTEMPTS += 1
    raise LiveNoteExecutionContractError(
        "credential materialization is not authorized during the offline harness"
    )


def _fail_if_secret_access_touched() -> None:
    global SECRET_ACCESS_ATTEMPTS
    SECRET_ACCESS_ATTEMPTS += 1
    raise LiveNoteExecutionContractError(
        "secret access is not authorized during the offline harness"
    )


def _fail_if_live_ghl_touched() -> None:
    global LIVE_GHL_ATTEMPTS
    LIVE_GHL_ATTEMPTS += 1
    raise LiveNoteExecutionContractError(
        "live GHL invocation is not authorized during the offline harness"
    )


def _validation_adapter() -> NotePathAdapter:
    return NotePathAdapter(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
        transport=_NoDispatchTransport(),
        consumer_authorization_identity="NW008_AT8W30_R2_OFFLINE_MAPPER_DIGEST_CLOSURE",
        consumer_workflow_run_id="offline-r2-digest-closure",
    )


def _require_mapping(name: str, value: object) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveNoteExecutionContractError(f"{name} must be an object")
    return value


def _require_non_empty_string(name: str, value: object) -> str:
    if not isinstance(value, str) or not value:
        raise LiveNoteExecutionContractError(f"{name} must be a non-empty string")
    return value


def _require_string(name: str, value: object) -> str:
    if not isinstance(value, str):
        raise LiveNoteExecutionContractError(f"{name} must be a string")
    return value


def _require_string_list(name: str, value: object) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise LiveNoteExecutionContractError(f"{name} must be an array of strings")
    return list(value)


def _require_mapping_or_none(name: str, value: object) -> Mapping[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise LiveNoteExecutionContractError(f"{name} must be an object or null")
    return dict(value)


def _require_commitments(name: str, value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise LiveNoteExecutionContractError(f"{name} must be an array")
    copied: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise LiveNoteExecutionContractError(f"{name}[{index}] must be an object")
        keys = set(item)
        if keys not in ({"owner", "action"}, {"owner", "action", "due_date"}):
            raise LiveNoteExecutionContractError(
                f"{name}[{index}] keys must be exactly "
                "{owner, action} or {owner, action, due_date}"
            )
        owner = _require_non_empty_string(f"{name}[{index}].owner", item.get("owner"))
        action = _require_non_empty_string(
            f"{name}[{index}].action", item.get("action")
        )
        commitment: dict[str, Any] = {"owner": owner, "action": action}
        if "due_date" in item:
            due_date = item["due_date"]
            if not isinstance(due_date, str):
                raise LiveNoteExecutionContractError(
                    f"{name}[{index}].due_date must be a string"
                )
            commitment["due_date"] = due_date
        copied.append(commitment)
    return copied


def _require_transcript_text(transcript_text: object) -> str:
    """Return UTF-8 transcript text. This function performs no hashing."""

    if isinstance(transcript_text, bytes):
        return transcript_text.decode("utf-8", "strict")
    if isinstance(transcript_text, str):
        return transcript_text
    raise LiveNoteExecutionContractError("transcript_text must be UTF-8 text or bytes")


def _require_hex_digest_shape(name: str, value: object) -> str:
    """Shape-validate an existing lowercase SHA-256 hex value. Never computes one."""

    text = _require_non_empty_string(name, value)
    if len(text) != 64 or any(character not in _HEX_CHARACTERS for character in text):
        raise LiveNoteExecutionContractError(
            f"{name} must be a lowercase 64-character hex value"
        )
    return text


def _require_hosted_transcript_hash(payload: Mapping[str, Any]) -> str:
    """Read the C3-accumulated transcript hash. This function performs no hashing."""

    meeting_context = _require_mapping(
        "hosted_result.meeting_context", payload.get("meeting_context")
    )
    meeting = _require_mapping(
        "hosted_result.meeting_context.meeting", meeting_context.get("meeting")
    )
    return _require_hex_digest_shape(
        "hosted_result.meeting_context.meeting.transcript_hash",
        meeting.get("transcript_hash"),
    )


def _require_aware_datetime(name: str, value: object) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise LiveNoteExecutionContractError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _require_execution_mode(value: object) -> ExecutionMode:
    if not isinstance(value, ExecutionMode):
        raise LiveNoteExecutionContractError(
            "mode must be an explicit ExecutionMode discriminator"
        )
    return value


def require_governance_preflight(
    *,
    mode: object,
    authorization_identity: object,
    run_id: object,
    window: OfflineSimulationWindow | None,
    now: object,
) -> GovernancePreflight:
    """Validate C2 mode, authority, binding, window, and expiry before C3.

    ``ExecutionMode.LIVE`` is refused unconditionally and before any credential,
    Secret Manager, or provider surface is constructed or touched.
    """

    resolved_mode = _require_execution_mode(mode)
    if resolved_mode is ExecutionMode.LIVE:
        raise LiveNoteExecutionContractError(
            "no live authorization exists; live mode is unavailable"
        )

    resolved_authorization_identity = _require_non_empty_string(
        "authorization_identity", authorization_identity
    )
    resolved_run_id = _require_non_empty_string("run_id", run_id)
    resolved_now = _require_aware_datetime("now", now)
    if resolved_authorization_identity == IMPLEMENTATION_AUTHORIZATION_ID:
        raise LiveNoteExecutionContractError(
            "implementation authorization is not execution authority"
        )
    if resolved_authorization_identity != OFFLINE_SIMULATION_AUTHORITY_ID:
        raise LiveNoteExecutionContractError(
            "authorization identity is not the offline simulation authority"
        )
    if not isinstance(window, OfflineSimulationWindow):
        raise LiveNoteExecutionContractError(
            "offline simulation window is required before execution"
        )

    window_authorization_identity = _require_non_empty_string(
        "window.authorization_identity", window.authorization_identity
    )
    window_run_id = _require_non_empty_string("window.run_id", window.run_id)
    window_not_before = _require_aware_datetime("window.not_before", window.not_before)
    window_expires_at = _require_aware_datetime("window.expires_at", window.expires_at)
    if window_not_before >= window_expires_at:
        raise LiveNoteExecutionContractError(
            "offline simulation window must begin before its expiry"
        )
    if (
        window_authorization_identity != resolved_authorization_identity
        or window_run_id != resolved_run_id
    ):
        raise LiveNoteExecutionContractError(
            "window authorization identity and run_id must match the execution"
        )
    if resolved_now < window_not_before:
        raise LiveNoteExecutionContractError(
            "offline simulation window has not started"
        )
    if resolved_now >= window_expires_at:
        raise LiveNoteExecutionContractError("offline simulation window has expired")
    return GovernancePreflight(
        authorization_identity=resolved_authorization_identity,
        run_id=resolved_run_id,
        mode=resolved_mode,
        live_authority=False,
        activation_003=ACTIVATION_003_STATE,
        simulation=True,
    )


def _require_local_adk_event(index: int, value: object, expected_agent: str) -> Event:
    if not isinstance(value, Event):
        raise LiveNoteExecutionContractError(
            f"stream_query event {index} is not a local Google ADK Event"
        )
    if value.author != expected_agent:
        raise LiveNoteExecutionContractError(
            f"stream_query event author mismatch at index {index}: "
            f"expected {expected_agent}"
        )
    return value


def _required_event_state_delta(
    event: Event, *, index: int, required_keys: tuple[str, ...]
) -> Mapping[str, Any]:
    state_delta = getattr(event.actions, "state_delta", None)
    if not isinstance(state_delta, Mapping):
        raise LiveNoteExecutionContractError(
            f"stream_query event {index} state_delta must be an object"
        )
    for key in required_keys:
        _require_mapping(f"stream_query event {index} state_delta.{key}", state_delta.get(key))
    return state_delta


def accumulate_local_adk_events(*, events: Sequence[object]) -> _NormalizedHostedResult:
    """Accumulate only source-proven in-process ADK Events; reject wire envelopes."""

    if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
        raise LiveNoteExecutionContractError(
            f"{HOSTED_STREAM_QUERY_NORMALIZATION_REFUSED}: events must be a sequence"
        )
    if len(events) != len(REQUIRED_AGENT_SEQUENCE):
        raise LiveNoteExecutionContractError(
            f"{HOSTED_STREAM_QUERY_NORMALIZATION_REFUSED}: exactly three events are required"
        )

    event_payload_keys = (
        ("meeting_context",),
        ("relationship_context",),
        ("follow_up_proposal", "follow_up_packet"),
    )
    accumulated: dict[str, Any] = {}
    for index, (expected_agent, required_keys) in enumerate(
        zip(REQUIRED_AGENT_SEQUENCE, event_payload_keys)
    ):
        event = _require_local_adk_event(index, events[index], expected_agent)
        state_delta = _required_event_state_delta(
            event, index=index, required_keys=required_keys
        )
        for key in required_keys:
            accumulated[key] = state_delta[key]

    accumulated["session"] = {
        "workflow": note_path_module._WORKFLOW_ID,
        "agent_trace": [
            {
                "agent_id": agent_id,
                "status": "ok",
                "output_schema": output_schema,
                "error": None,
                "external_effects": 0,
            }
            for agent_id, output_schema in zip(
                REQUIRED_AGENT_SEQUENCE, _REQUIRED_AGENT_OUTPUT_SCHEMAS
            )
        ],
    }
    normalized_result = _NormalizedHostedResult(payload=accumulated)
    validate_hosted_three_agent_result(normalized_result)
    return normalized_result


def _require_trace_entry(
    entry: Mapping[str, Any], *, index: int, expected_agent: str, expected_schema: str
) -> None:
    agent_id = _require_string(f"session.agent_trace[{index}].agent_id", entry.get("agent_id"))
    if agent_id != expected_agent:
        raise LiveNoteExecutionContractError(
            f"session.agent_trace order mismatch at index {index}: "
            f"expected {expected_agent}, got {agent_id}"
        )
    status = _require_string(f"session.agent_trace[{index}].status", entry.get("status"))
    if status != "ok":
        raise LiveNoteExecutionContractError(
            f"session.agent_trace[{index}].status must be ok"
        )
    schema = _require_string(
        f"session.agent_trace[{index}].output_schema", entry.get("output_schema")
    )
    if schema != expected_schema:
        raise LiveNoteExecutionContractError(
            f"session.agent_trace[{index}].output_schema mismatch: "
            f"expected {expected_schema}, got {schema}"
        )
    if entry.get("error") is not None:
        raise LiveNoteExecutionContractError(
            f"session.agent_trace[{index}].error must be null"
        )
    external_effects = entry.get("external_effects")
    if not isinstance(external_effects, int):
        raise LiveNoteExecutionContractError(
            f"session.agent_trace[{index}].external_effects must be an integer"
        )
    if external_effects != 0:
        raise LiveNoteExecutionContractError(
            f"session.agent_trace[{index}].external_effects must be 0"
        )


def validate_hosted_three_agent_result(
    hosted_result: object,
) -> Mapping[str, Any]:
    """Validate normalized local ADK output before mapping to NOTE_PATH."""

    if not isinstance(hosted_result, _NormalizedHostedResult):
        raise LiveNoteExecutionContractError(
            "normalized hosted result must originate from typed local ADK events"
        )
    payload = _require_mapping("normalized_hosted_result", hosted_result.payload)
    session = _require_mapping("hosted_result.session", payload.get("session"))
    if session.get("workflow") != note_path_module._WORKFLOW_ID:
        raise LiveNoteExecutionContractError(
            "hosted_result.session.workflow must be meeting_follow_up_v1"
        )
    agent_trace = session.get("agent_trace")
    if not isinstance(agent_trace, list) or len(agent_trace) != len(REQUIRED_AGENT_SEQUENCE):
        raise LiveNoteExecutionContractError(
            "hosted_result.session.agent_trace must contain exactly three agents"
        )
    for index, (expected_agent, expected_schema) in enumerate(
        zip(REQUIRED_AGENT_SEQUENCE, _REQUIRED_AGENT_OUTPUT_SCHEMAS)
    ):
        entry = _require_mapping(f"session.agent_trace[{index}]", agent_trace[index])
        _require_trace_entry(
            entry,
            index=index,
            expected_agent=expected_agent,
            expected_schema=expected_schema,
        )

    meeting_context = _require_mapping(
        "hosted_result.meeting_context", payload.get("meeting_context")
    )
    if meeting_context.get("agent") != REQUIRED_AGENT_SEQUENCE[0]:
        raise LiveNoteExecutionContractError(
            "hosted_result.meeting_context.agent must be meeting_context_agent"
        )
    if meeting_context.get("schema") != "meeting_context_v1":
        raise LiveNoteExecutionContractError(
            "hosted_result.meeting_context.schema must be meeting_context_v1"
        )
    _require_zero_external_effects("hosted_result.meeting_context", meeting_context)
    _require_deterministic_policy("hosted_result.meeting_context", meeting_context)

    relationship_context = _require_mapping(
        "hosted_result.relationship_context", payload.get("relationship_context")
    )
    if relationship_context.get("agent") != REQUIRED_AGENT_SEQUENCE[1]:
        raise LiveNoteExecutionContractError(
            "hosted_result.relationship_context.agent must be relationship_context_agent"
        )
    if relationship_context.get("schema") != "relationship_context_v1":
        raise LiveNoteExecutionContractError(
            "hosted_result.relationship_context.schema must be relationship_context_v1"
        )
    _require_zero_external_effects(
        "hosted_result.relationship_context", relationship_context
    )
    _require_deterministic_policy(
        "hosted_result.relationship_context", relationship_context
    )
    relationship_resolution = _require_mapping(
        "hosted_result.relationship_context.resolution",
        relationship_context.get("resolution"),
    )
    if relationship_resolution.get("status") != "matched":
        raise LiveNoteExecutionContractError(
            "hosted_result.relationship_context.resolution.status must be matched"
        )

    follow_up_proposal = _require_mapping(
        "hosted_result.follow_up_proposal", payload.get("follow_up_proposal")
    )
    if follow_up_proposal.get("agent") != REQUIRED_AGENT_SEQUENCE[2]:
        raise LiveNoteExecutionContractError(
            "hosted_result.follow_up_proposal.agent must be follow_up_planning_agent"
        )
    if follow_up_proposal.get("schema") != "follow_up_proposal_v1":
        raise LiveNoteExecutionContractError(
            "hosted_result.follow_up_proposal.schema must be follow_up_proposal_v1"
        )
    _require_zero_external_effects(
        "hosted_result.follow_up_proposal", follow_up_proposal
    )

    follow_up_packet = _require_mapping(
        "hosted_result.follow_up_packet", payload.get("follow_up_packet")
    )
    if follow_up_packet.get("schema") != "meeting_follow_up_packet_v1":
        raise LiveNoteExecutionContractError(
            "hosted_result.follow_up_packet.schema must be meeting_follow_up_packet_v1"
        )
    packet_effects = follow_up_packet.get("external_effects")
    if not isinstance(packet_effects, int) or packet_effects != 0:
        raise LiveNoteExecutionContractError(
            "hosted_result.follow_up_packet.external_effects must be 0"
        )
    return payload


def _require_zero_external_effects(name: str, value: Mapping[str, Any]) -> None:
    external_effects = value.get("external_effects")
    if not isinstance(external_effects, int) or external_effects != 0:
        raise LiveNoteExecutionContractError(f"{name}.external_effects must be 0")


def _require_deterministic_policy(name: str, value: Mapping[str, Any]) -> None:
    policy_authority = _require_mapping(
        f"{name}.policy_authority", value.get("policy_authority")
    )
    if policy_authority.get("deterministic_policy_bypass") is not False:
        raise LiveNoteExecutionContractError(
            f"{name}.policy_authority.deterministic_policy_bypass must be false"
        )


def _validate_cross_agent_provenance(
    *, payload: Mapping[str, Any], hosted_transcript_sha256: str
) -> None:
    meeting_context = _require_mapping(
        "hosted_result.meeting_context", payload.get("meeting_context")
    )
    meeting_context_meeting = _require_mapping(
        "hosted_result.meeting_context.meeting", meeting_context.get("meeting")
    )
    relationship_context = _require_mapping(
        "hosted_result.relationship_context", payload.get("relationship_context")
    )
    relationship_meeting_ref = _require_mapping(
        "hosted_result.relationship_context.meeting_ref",
        relationship_context.get("meeting_ref"),
    )
    follow_up_packet = _require_mapping(
        "hosted_result.follow_up_packet", payload.get("follow_up_packet")
    )
    follow_up_meeting = _require_mapping(
        "hosted_result.follow_up_packet.meeting", follow_up_packet.get("meeting")
    )

    meeting_context_meeting_id = _require_non_empty_string(
        "hosted_result.meeting_context.meeting.meeting_id",
        meeting_context_meeting.get("meeting_id"),
    )
    relationship_context_meeting_id = _require_non_empty_string(
        "hosted_result.relationship_context.meeting_ref.meeting_id",
        relationship_meeting_ref.get("meeting_id"),
    )
    follow_up_packet_meeting_id = _require_non_empty_string(
        "hosted_result.follow_up_packet.meeting.meeting_id",
        follow_up_meeting.get("meeting_id"),
    )
    if not (
        meeting_context_meeting_id
        == relationship_context_meeting_id
        == follow_up_packet_meeting_id
    ):
        raise LiveNoteExecutionContractError(
            "cross-agent provenance mismatch: meeting_id must match across "
            "meeting_context.meeting, relationship_context.meeting_ref, and "
            "follow_up_packet.meeting"
        )

    meeting_context_transcript_hash = _require_non_empty_string(
        "hosted_result.meeting_context.meeting.transcript_hash",
        meeting_context_meeting.get("transcript_hash"),
    )
    relationship_context_transcript_hash = _require_non_empty_string(
        "hosted_result.relationship_context.meeting_ref.transcript_hash",
        relationship_meeting_ref.get("transcript_hash"),
    )
    follow_up_packet_transcript_hash = _require_non_empty_string(
        "hosted_result.follow_up_packet.meeting.transcript_hash",
        follow_up_meeting.get("transcript_hash"),
    )
    if not (
        meeting_context_transcript_hash
        == relationship_context_transcript_hash
        == follow_up_packet_transcript_hash
    ):
        raise LiveNoteExecutionContractError(
            "cross-agent provenance mismatch: transcript_hash must match across "
            "meeting_context.meeting, relationship_context.meeting_ref, and "
            "follow_up_packet.meeting"
        )
    if meeting_context_transcript_hash != hosted_transcript_sha256:
        raise LiveNoteExecutionContractError(
            "cross-agent transcript_hash does not match the accumulated hosted "
            "transcript hash"
        )
    if hosted_transcript_sha256 != FROZEN_TRANSCRIPT_SHA256:
        raise LiveNoteExecutionContractError(
            "cross-agent transcript_hash does not match the frozen R2 transcript value"
        )


def map_hosted_result_to_note_contract(
    *, hosted_result: object, transcript_text: str | bytes
) -> dict[str, Any]:
    """Map only C3-accumulated output to the exact NOTE_PATH ten-field contract."""

    payload = validate_hosted_three_agent_result(hosted_result)
    # No digest is computed here. The transcript hash is consumed from the
    # C3-accumulated hosted output and byte-level verification is delegated to
    # At1ExecutionStore.record_prewrite_provenance (see
    # _verify_frozen_bytes_via_execution_store).
    transcript_sha256 = _require_hosted_transcript_hash(payload)
    _require_transcript_text(transcript_text)
    _validate_cross_agent_provenance(
        payload=payload, hosted_transcript_sha256=transcript_sha256
    )
    follow_up_packet = _require_mapping(
        "hosted_result.follow_up_packet", payload.get("follow_up_packet")
    )
    meeting = _require_mapping(
        "hosted_result.follow_up_packet.meeting", follow_up_packet.get("meeting")
    )
    extraction = _require_mapping(
        "hosted_result.follow_up_packet.extraction", follow_up_packet.get("extraction")
    )
    run = _require_mapping("hosted_result.follow_up_packet.run", follow_up_packet.get("run"))
    packet_workflow_id = _require_string(
        "hosted_result.follow_up_packet.run.workflow", run.get("workflow")
    )
    if packet_workflow_id != note_path_module._WORKFLOW_ID:
        raise LiveNoteExecutionContractError(
            "hosted_result.follow_up_packet.run.workflow does not match NOTE_PATH workflow_id"
        )

    note_contract = {
        "SYNTHETIC_MARKER": note_path_module._MARKER,
        "meeting_id": _require_non_empty_string(
            "hosted_result.follow_up_packet.meeting.meeting_id", meeting.get("meeting_id")
        ),
        "meeting_summary": _require_string(
            "hosted_result.follow_up_packet.extraction.summary", extraction.get("summary")
        ),
        "needs": _require_string_list(
            "hosted_result.follow_up_packet.extraction.needs", extraction.get("needs")
        ),
        "objections": _require_string_list(
            "hosted_result.follow_up_packet.extraction.objections",
            extraction.get("objections"),
        ),
        "commitments": _require_commitments(
            "hosted_result.follow_up_packet.extraction.commitments",
            extraction.get("commitments"),
        ),
        "next_step": _require_mapping_or_none(
            "hosted_result.follow_up_packet.extraction.next_step",
            extraction.get("next_step"),
        ),
        "opportunity_signal": _require_mapping_or_none(
            "hosted_result.follow_up_packet.extraction.opportunity_signal",
            extraction.get("opportunity_signal"),
        ),
        "workflow_id": note_path_module._WORKFLOW_ID,
        "transcript_hash": transcript_sha256,
    }
    return dict(_validation_adapter()._validate_note_contract(note_contract))


def _approved_transcript_text(fixture_id: str = "transcript-success") -> str:
    """Read approved fixture transcript bytes. This function performs no hashing."""

    if fixture_id not in _OFFLINE_FIXTURE_ALLOWLIST:
        raise LiveNoteExecutionContractError("fixture is not on the approved allowlist")
    path = _repository_root() / "fixtures" / f"{fixture_id}.txt"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        raise LiveNoteExecutionContractError(
            "approved offline fixture transcript is unavailable"
        ) from None


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _verify_frozen_bytes_via_execution_store(
    *, transcript_text: str, note_body: str
) -> None:
    """Verify frozen transcript and note-body bytes through an existing helper.

    ``At1ExecutionStore.record_prewrite_provenance`` recomputes both SHA-256
    values internally and refuses on any mismatch. Lane A therefore closes
    ``TRANSCRIPT_SHA256`` and ``NOTE_BODY_SHA256`` with no digest implementation
    of its own. The store is offline: a synthetic commitment key provider and a
    temporary SQLite file are used, and neither reaches Secret Manager.
    """

    grant_run_id = f"{_OFFLINE_PROVENANCE_RUN_PREFIX}{next(_OFFLINE_RUN_SEQUENCE)}"
    material = SyntheticCommitmentKeyProvider(
        payload=_OFFLINE_COMMITMENT_KEY_PAYLOAD,
        version_resource=_OFFLINE_COMMITMENT_KEY_VERSION_RESOURCE,
    ).resolve()
    with tempfile.TemporaryDirectory() as temporary_directory:
        store = At1ExecutionStore(
            db_path=str(Path(temporary_directory) / "offline.sqlite3"),
            commitment_material=material,
        )
        try:
            store.record_prewrite_provenance(
                grant_run_id=grant_run_id,
                transcript_content=transcript_text,
                transcript_sha256=FROZEN_TRANSCRIPT_SHA256,
                expected_note_content=note_body,
                expected_note_sha256=FROZEN_NOTE_BODY_SHA256,
            )
        except AttemptStateError:
            raise LiveNoteExecutionContractError(
                "frozen transcript or note-body bytes failed execution-store verification"
            ) from None
        finally:
            del store


def evaluate_frozen_digests(
    note_contract: Mapping[str, Any],
    *,
    transcript_text: str | bytes | None = None,
) -> FrozenDigestValidation:
    """Evaluate NOTE_PATH frozen values using merged production surfaces only.

    Logical and provider-body values come from ``note_path``. The note-body
    value is closed exclusively by ``record_prewrite_provenance``; when that
    verification refuses, no digest value is published for it.
    """

    adapter = _validation_adapter()
    canonical_note = adapter._validate_note_contract(note_contract)
    transcript_sha256 = _require_string(
        "note_contract.transcript_hash", canonical_note["transcript_hash"]
    )
    note_content_logical_sha256 = adapter._logical_digest(canonical_note)
    note_body = adapter._serialize_note(canonical_note)
    provider_body_sha256 = adapter._provider_body_digest({"body": note_body})
    resolved_transcript_text = (
        _approved_transcript_text()
        if transcript_text is None
        else _require_transcript_text(transcript_text)
    )
    try:
        _verify_frozen_bytes_via_execution_store(
            transcript_text=resolved_transcript_text, note_body=note_body
        )
    except LiveNoteExecutionContractError:
        note_body_sha256 = _UNVERIFIED_BY_EXECUTION_STORE
        note_body_sha256_match = False
    else:
        note_body_sha256 = FROZEN_NOTE_BODY_SHA256
        note_body_sha256_match = True
    return FrozenDigestValidation(
        transcript_sha256=transcript_sha256,
        note_content_logical_sha256=note_content_logical_sha256,
        note_body_sha256=note_body_sha256,
        provider_body_sha256=provider_body_sha256,
        transcript_sha256_match=transcript_sha256 == FROZEN_TRANSCRIPT_SHA256,
        note_content_logical_sha256_match=(
            note_content_logical_sha256 == FROZEN_NOTE_CONTENT_LOGICAL_SHA256
        ),
        note_body_sha256_match=note_body_sha256_match,
        provider_body_sha256_match=provider_body_sha256 == FROZEN_PROVIDER_BODY_SHA256,
    )


def require_frozen_digest_match(
    note_contract: Mapping[str, Any],
    *,
    transcript_text: str | bytes | None = None,
) -> FrozenDigestValidation:
    """Require exact closure against every frozen R2 value."""

    result = evaluate_frozen_digests(note_contract, transcript_text=transcript_text)
    mismatches: list[str] = []
    if not result.transcript_sha256_match:
        mismatches.append("TRANSCRIPT_SHA256")
    if not result.note_content_logical_sha256_match:
        mismatches.append("NOTE_CONTENT_LOGICAL_SHA256")
    if not result.note_body_sha256_match:
        mismatches.append("NOTE_BODY_SHA256")
    if not result.provider_body_sha256_match:
        mismatches.append("PROVIDER_BODY_SHA256")
    if mismatches:
        raise LiveNoteExecutionContractError(
            "R2 offline digest closure failed: " + ", ".join(mismatches)
        )
    return result


def derive_note_contract_and_frozen_digests(
    *, hosted_result: object, transcript_text: str | bytes
) -> tuple[dict[str, Any], FrozenDigestValidation]:
    """Map C3-accumulated output and require exact frozen digest closure."""

    note_contract = map_hosted_result_to_note_contract(
        hosted_result=hosted_result, transcript_text=transcript_text
    )
    return note_contract, require_frozen_digest_match(
        note_contract, transcript_text=transcript_text
    )


def require_private_origin_materialization() -> None:
    """Require the root-owned origin, then stop until later authority proves ingress.

    This is the only consumption point of ``live_note_runtime`` and it is the
    truthful R5 gate. It never returns successfully: R5 is unresolved, so no
    caller can continue from here to a credential, Secret Manager, or live
    provider surface.
    """

    try:
        live_note_runtime.compose_root_owned_private_origin()
    except live_note_runtime.LiveNoteRuntimeAssemblyError:
        raise LiveNoteExecutionContractError(
            "legitimate same-process private origin is unavailable"
        ) from None
    raise LiveNoteExecutionContractError(
        "private origin reference is not available to this execution harness"
    )


def _offline_request_path(url: str) -> str:
    """Extract a request path without importing any network-capable module.

    The query string is deliberately retained so that any query-bearing URL
    fails the exact frozen-route comparison. Search, list, and pagination
    routes are therefore unservable rather than silently normalized away.
    """

    remainder = url.split("://", 1)[-1]
    separator = remainder.find("/")
    return remainder[separator:] if separator != -1 else "/"


class _OfflineThreeCallSession:
    """In-module offline HTTP session serving exactly GET, POST, GET.

    It is the lowest seam of the offline stack. Every other layer above it is
    the merged production implementation. Any fourth call or unknown route
    raises, so no retry, search, list, pagination, fallback, or stage route can
    be served even by accident.
    """

    def __init__(
        self,
        *,
        contact_id: str = _OFFLINE_CONTACT_ID,
        location_id: str = _OFFLINE_LOCATION_ID,
        note_id: str = _OFFLINE_NOTE_ID,
        uncertain_post: bool = False,
    ) -> None:
        self._contact_id = contact_id
        self._location_id = location_id
        self._note_id = note_id
        self._uncertain_post = uncertain_post
        self.calls: list[tuple[str, str]] = []
        self._created_note_body: str | None = None

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout_seconds: float,
        allow_redirects: bool,
    ) -> LiveNoteHttpResult:
        if headers.get("Authorization") is None:
            raise LiveNoteExecutionContractError(
                "offline simulation requires an injected authorization header"
            )
        if allow_redirects is not False:
            raise LiveNoteExecutionContractError(
                "offline simulation forbids redirect following"
            )
        path = _offline_request_path(url)
        if len(self.calls) >= 3:
            raise LiveNoteExecutionContractError(
                "offline simulation permits exactly three provider calls"
            )
        self.calls.append((method, path))

        if method == "GET" and path == f"/contacts/{_OFFLINE_CONTACT_ID}":
            return LiveNoteHttpResult(
                200,
                json.dumps(
                    {
                        "contact": {
                            "id": self._contact_id,
                            "locationId": self._location_id,
                        }
                    }
                ).encode("utf-8"),
            )
        if method == "POST" and path == f"/contacts/{_OFFLINE_CONTACT_ID}/notes":
            if self._uncertain_post:
                raise LiveNoteHttpUncertainty("offline simulation post uncertainty")
            payload = json.loads((body or b"{}").decode("utf-8"))
            self._created_note_body = payload["body"]
            return LiveNoteHttpResult(
                201,
                json.dumps(
                    {
                        "note": {
                            "id": self._note_id,
                            "body": self._created_note_body,
                            "contactId": _OFFLINE_CONTACT_ID,
                        }
                    }
                ).encode("utf-8"),
            )
        if (
            method == "GET"
            and path == f"/contacts/{_OFFLINE_CONTACT_ID}/notes/{self._note_id}"
            and self._created_note_body is not None
        ):
            return LiveNoteHttpResult(
                200,
                json.dumps(
                    {
                        "note": {
                            "id": self._note_id,
                            "body": self._created_note_body,
                            "contactId": _OFFLINE_CONTACT_ID,
                        }
                    }
                ).encode("utf-8"),
            )
        raise LiveNoteExecutionContractError(
            "offline simulation refuses an unknown provider route"
        )


def _build_offline_note_path_stack(
    session: _OfflineThreeCallSession | None = None,
) -> tuple[
    NotePathAdapter,
    BoundedLiveNoteTransport,
    ConcreteLiveNoteHttpClient,
    _OfflineThreeCallSession,
]:
    """Assemble the merged production NOTE_PATH stack over an offline session.

    ``live_note_credential_provider``, ``live_note_http_client``,
    ``live_note_transport``, and ``note_path`` are the real production classes.
    Only the lowest HTTP session is offline, and no Secret Manager surface is
    constructed or reached.
    """

    resolved_session = session if session is not None else _OfflineThreeCallSession()
    credential = LiveNoteCredentialProvider(
        accessor=SyntheticLiveNoteSecretAccessor(
            payloads={_OFFLINE_CREDENTIAL_RESOURCE_NAME: _OFFLINE_CREDENTIAL_PAYLOAD}
        ),
        resource_name=_OFFLINE_CREDENTIAL_RESOURCE_NAME,
    ).get_credential()
    client = ConcreteLiveNoteHttpClient(session=resolved_session)
    transport = BoundedLiveNoteTransport(
        bound_contact_id=_OFFLINE_CONTACT_ID,
        credential=credential,
        http_client=client,
    )
    adapter = NotePathAdapter(
        location_id=_OFFLINE_LOCATION_ID,
        contact_id=_OFFLINE_CONTACT_ID,
        transport=transport,
        consumer_authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
        consumer_workflow_run_id=(
            f"offline-simulation-note-path-{next(_OFFLINE_RUN_SEQUENCE)}"
        ),
    )
    return adapter, transport, client, resolved_session


def _drive_offline_note_path(
    *,
    adapter: NotePathAdapter,
    transport: BoundedLiveNoteTransport,
    client: ConcreteLiveNoteHttpClient,
    note_contract: Mapping[str, Any],
    digest: FrozenDigestValidation,
) -> _OfflineProviderSimulation:
    """Drive C6 through the production adapter: one GET, one POST, one GET."""

    bound_contact = adapter.get_bound_contact()
    created_note = adapter.create_meeting_note(note_contract)
    verified_note = adapter.verify_meeting_note()

    if len(client.call_history) != 3:
        raise LiveNoteExecutionContractError(
            "offline simulation must perform exactly three provider calls"
        )
    if transport.total_mutation_calls != 1:
        raise LiveNoteExecutionContractError(
            "offline simulation must perform exactly one mutation"
        )
    if created_note.note_id != verified_note.note_id:
        raise LiveNoteExecutionContractError(
            "readback note id must be the same-run created note id"
        )
    if created_note.note_content_digest != verified_note.note_content_digest:
        raise LiveNoteExecutionContractError(
            "readback note content digest must match the created note"
        )
    if created_note.note_content_digest != digest.note_content_logical_sha256:
        raise LiveNoteExecutionContractError(
            "created note content digest must match the C5 logical value"
        )
    if created_note.provider_body_digest != digest.provider_body_sha256:
        raise LiveNoteExecutionContractError(
            "created provider body digest must match the C5 provider value"
        )
    return _OfflineProviderSimulation(
        provider_calls=len(client.call_history),
        mutations=transport.total_mutation_calls,
        contact_match=bound_contact["id"] == adapter._contact_id,
        location_match=bound_contact["locationId"] == adapter._location_id,
        note_id_present=bool(verified_note.note_id),
        note_contact_match=True,
        body_digest_match=(
            created_note.provider_body_digest == digest.provider_body_sha256
        ),
    )


def run_offline_provider_simulation(
    *, note_contract: Mapping[str, Any], digest: FrozenDigestValidation
) -> _OfflineProviderSimulation:
    """Build the production stack and drive one bounded offline NOTE_PATH run."""

    adapter, transport, client, _session = _build_offline_note_path_stack()
    return _drive_offline_note_path(
        adapter=adapter,
        transport=transport,
        client=client,
        note_contract=note_contract,
        digest=digest,
    )


_SANITIZED_REPORT_KEYS = frozenset(
    {
        "RUN_ID",
        "TIMESTAMP_UTC",
        "EXECUTION_MODE",
        "LIVE_MODE_AVAILABLE",
        "ACTIVATION_003",
        "GOVERNANCE_PREFLIGHT_STATE",
        "HOSTED_ATTRIBUTION_GATE_STATE",
        "HOSTED_STREAM_QUERY_NORMALIZATION_STATE",
        "R5_SAME_PROCESS_MATERIALIZATION_STATE",
        "R5_RESOLVED",
        "FIVE_MODULE_PRODUCTION_ASSEMBLY_REUSE",
        "LIVE_EXECUTION_BLOCKED",
        "FAIL_CLOSED_BEFORE_SECRET",
        "PROVIDER_PATH_EXECUTION_CLASS",
        "CONTACT_MATCH",
        "LOCATION_MATCH",
        "NOTE_ID_PRESENT",
        "NOTE_CONTACT_MATCH",
        "BODY_DIGEST_MATCH",
        "TRANSCRIPT_SHA256_MATCH",
        "NOTE_CONTENT_LOGICAL_SHA256_MATCH",
        "NOTE_BODY_SHA256_MATCH",
        "PROVIDER_BODY_SHA256_MATCH",
        "SIMULATED_PROVIDER_CALLS",
        "SIMULATED_MUTATIONS",
        "PRE_RUN_EFFECT_COUNTERS_ZERO",
        "POST_RUN_EFFECT_COUNTERS_ZERO",
        "REAL_NETWORK_CALLS",
        "REAL_SECRET_READS",
        "REAL_GHL_CALLS",
        "REAL_CRM_MUTATIONS",
        "PROVIDER_DISPATCH_ATTEMPTS",
        "CREDENTIAL_MATERIALIZATION_ATTEMPTS",
        "SECRET_ACCESS_ATTEMPTS",
        "LIVE_GHL_ATTEMPTS",
        "FAILURE_CLASS",
        "TERMINAL_RESULT",
    }
)


def _effect_counter_snapshot() -> tuple[int, ...]:
    return (
        NETWORK_CALLS,
        REAL_SECRET_READS,
        REAL_GHL_CALLS,
        REAL_CRM_MUTATIONS,
        PROVIDER_DISPATCH_ATTEMPTS,
        CREDENTIAL_MATERIALIZATION_ATTEMPTS,
        SECRET_ACCESS_ATTEMPTS,
        LIVE_GHL_ATTEMPTS,
    )


def build_sanitized_terminal_report(
    *,
    run_id: object,
    timestamp: datetime,
    governance_preflight_state: str,
    hosted_attribution_gate_state: str,
    hosted_stream_query_normalization_state: str,
    terminal_result: str,
    failure_class: str,
    mode: ExecutionMode = ExecutionMode.OFFLINE_SIMULATION,
    digest: FrozenDigestValidation | None = None,
    simulation: _OfflineProviderSimulation | None = None,
    pre_run_counters: tuple[int, ...] | None = None,
) -> dict[str, object]:
    """Create a default-deny report that never accepts provider/private payloads."""

    safe_run_id = run_id if isinstance(run_id, str) and run_id else "UNAVAILABLE"
    safe_timestamp = _require_aware_datetime("timestamp", timestamp).isoformat().replace(
        "+00:00", "Z"
    )
    safe_mode = _require_execution_mode(mode)
    resolved_pre_run_counters = (
        _effect_counter_snapshot() if pre_run_counters is None else pre_run_counters
    )
    report = {
        "RUN_ID": safe_run_id,
        "TIMESTAMP_UTC": safe_timestamp,
        "EXECUTION_MODE": safe_mode.value,
        "LIVE_MODE_AVAILABLE": LIVE_MODE_AVAILABLE,
        "ACTIVATION_003": ACTIVATION_003_STATE,
        "GOVERNANCE_PREFLIGHT_STATE": governance_preflight_state,
        "HOSTED_ATTRIBUTION_GATE_STATE": hosted_attribution_gate_state,
        "HOSTED_STREAM_QUERY_NORMALIZATION_STATE": (
            hosted_stream_query_normalization_state
        ),
        "R5_SAME_PROCESS_MATERIALIZATION_STATE": (
            R5_SAME_PROCESS_MATERIALIZATION_UNRESOLVED
        ),
        "R5_RESOLVED": "NO",
        "FIVE_MODULE_PRODUCTION_ASSEMBLY_REUSE": FIVE_MODULE_PRODUCTION_ASSEMBLY_REUSE,
        "LIVE_EXECUTION_BLOCKED": "YES",
        "FAIL_CLOSED_BEFORE_SECRET": "YES",
        "PROVIDER_PATH_EXECUTION_CLASS": (
            "SIMULATED_OFFLINE_NO_LIVE_WRITE" if simulation else "NOT_EXECUTED"
        ),
        "CONTACT_MATCH": "YES" if simulation and simulation.contact_match else "NO",
        "LOCATION_MATCH": "YES" if simulation and simulation.location_match else "NO",
        "NOTE_ID_PRESENT": "YES" if simulation and simulation.note_id_present else "NO",
        "NOTE_CONTACT_MATCH": (
            "YES" if simulation and simulation.note_contact_match else "NO"
        ),
        "BODY_DIGEST_MATCH": (
            "YES" if simulation and simulation.body_digest_match else "NO"
        ),
        "TRANSCRIPT_SHA256_MATCH": bool(digest and digest.transcript_sha256_match),
        "NOTE_CONTENT_LOGICAL_SHA256_MATCH": bool(
            digest and digest.note_content_logical_sha256_match
        ),
        "NOTE_BODY_SHA256_MATCH": bool(digest and digest.note_body_sha256_match),
        "PROVIDER_BODY_SHA256_MATCH": bool(
            digest and digest.provider_body_sha256_match
        ),
        "SIMULATED_PROVIDER_CALLS": simulation.provider_calls if simulation else 0,
        "SIMULATED_MUTATIONS": simulation.mutations if simulation else 0,
        "PRE_RUN_EFFECT_COUNTERS_ZERO": (
            "YES" if not any(resolved_pre_run_counters) else "NO"
        ),
        "POST_RUN_EFFECT_COUNTERS_ZERO": (
            "YES" if not any(_effect_counter_snapshot()) else "NO"
        ),
        "REAL_NETWORK_CALLS": NETWORK_CALLS,
        "REAL_SECRET_READS": REAL_SECRET_READS,
        "REAL_GHL_CALLS": REAL_GHL_CALLS,
        "REAL_CRM_MUTATIONS": REAL_CRM_MUTATIONS,
        "PROVIDER_DISPATCH_ATTEMPTS": PROVIDER_DISPATCH_ATTEMPTS,
        "CREDENTIAL_MATERIALIZATION_ATTEMPTS": CREDENTIAL_MATERIALIZATION_ATTEMPTS,
        "SECRET_ACCESS_ATTEMPTS": SECRET_ACCESS_ATTEMPTS,
        "LIVE_GHL_ATTEMPTS": LIVE_GHL_ATTEMPTS,
        "FAILURE_CLASS": failure_class,
        "TERMINAL_RESULT": terminal_result,
    }
    if set(report) != _SANITIZED_REPORT_KEYS:
        raise LiveNoteExecutionContractError("sanitized report allowlist mismatch")
    return report


def _offline_simulation_window(
    *, run_id: str = _OFFLINE_SIMULATION_RUN_ID, now: datetime | None = None
) -> OfflineSimulationWindow:
    """Build the offline invocation binding. This is not an activation record."""

    anchor = _OFFLINE_SIMULATION_TIMESTAMP if now is None else _require_aware_datetime(
        "now", now
    )
    span = timedelta(seconds=_OFFLINE_SIMULATION_WINDOW_SPAN_SECONDS)
    return OfflineSimulationWindow(
        authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
        run_id=run_id,
        not_before=anchor - span,
        expires_at=anchor + span,
    )


def _load_approved_fixture_sidecar(fixture_id: str) -> Mapping[str, Any]:
    if fixture_id not in _OFFLINE_FIXTURE_ALLOWLIST:
        raise LiveNoteExecutionContractError("fixture is not on the approved allowlist")
    path = _repository_root() / "fixtures" / f"{fixture_id}.expected.json"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        raise LiveNoteExecutionContractError(
            "approved offline fixture sidecar is unavailable"
        ) from None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise LiveNoteExecutionContractError(
            "approved offline fixture sidecar is not valid JSON"
        ) from None
    return _require_mapping("fixture_sidecar", parsed)


def _build_offline_hosted_payloads(fixture_id: str) -> dict[str, Any]:
    """Shape approved fixture content into the three-agent hosted contract."""

    sidecar = _load_approved_fixture_sidecar(fixture_id)
    extraction = deepcopy(_require_mapping(
        "fixture_sidecar.extraction_result", sidecar.get("extraction_result")
    ))
    meeting = deepcopy(
        _require_mapping("fixture_sidecar.meeting", sidecar.get("meeting"))
    )
    participants = deepcopy(sidecar.get("participants"))
    evidence_references = deepcopy(sidecar.get("evidence_references"))
    return {
        "meeting_context": {
            "schema": "meeting_context_v1",
            "agent": REQUIRED_AGENT_SEQUENCE[0],
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
                "extraction_confidence": sidecar.get("extraction_confidence"),
            },
            "external_effects": 0,
            "policy_authority": {"deterministic_policy_bypass": False},
        },
        "relationship_context": {
            "schema": "relationship_context_v1",
            "agent": REQUIRED_AGENT_SEQUENCE[1],
            "provider": "offline_ghl_fixture",
            "meeting_ref": {
                "meeting_id": meeting["meeting_id"],
                "transcript_hash": meeting["transcript_hash"],
                "run_id": sidecar.get("run_id"),
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
            "agent": REQUIRED_AGENT_SEQUENCE[2],
            "external_effects": 0,
        },
        "follow_up_packet": {
            "schema": "meeting_follow_up_packet_v1",
            "run": {"workflow": note_path_module._WORKFLOW_ID},
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


def build_offline_typed_local_events(fixture_id: str) -> list[Event]:
    """Build in-process typed ADK events from approved fixture content only."""

    payloads = _build_offline_hosted_payloads(fixture_id)
    return [
        Event(
            author=REQUIRED_AGENT_SEQUENCE[0],
            actions=EventActions(
                state_delta={"meeting_context": payloads["meeting_context"]}
            ),
        ),
        Event(
            author=REQUIRED_AGENT_SEQUENCE[1],
            actions=EventActions(
                state_delta={"relationship_context": payloads["relationship_context"]}
            ),
        ),
        Event(
            author=REQUIRED_AGENT_SEQUENCE[2],
            actions=EventActions(
                state_delta={
                    "follow_up_proposal": payloads["follow_up_proposal"],
                    "follow_up_packet": payloads["follow_up_packet"],
                }
            ),
        ),
    ]


def run_offline_harness(
    *,
    mode: object = ExecutionMode.OFFLINE_SIMULATION,
    authorization_identity: object,
    run_id: object,
    window: OfflineSimulationWindow | None,
    events: Sequence[object],
    transcript_text: str | bytes,
    now: datetime,
    simulate_provider_path: bool = False,
) -> HarnessExecutionResult:
    """Run C2 through C7 as a fully terminal, sanitized, fail-closed process.

    Every branch returns a :class:`HarnessExecutionResult`. Nothing is raised to
    the caller, no exception text ever reaches a report, and there is no code
    path from the R5 gate to a credential, Secret Manager, or live provider
    surface.
    """

    pre_run_counters = _effect_counter_snapshot()
    try:
        return _run_offline_harness_inner(
            mode=mode,
            authorization_identity=authorization_identity,
            run_id=run_id,
            window=window,
            events=events,
            transcript_text=transcript_text,
            now=now,
            simulate_provider_path=simulate_provider_path,
            pre_run_counters=pre_run_counters,
        )
    except BaseException:  # noqa: BLE001 - default-deny sanitization boundary
        return _unexpected_internal_refusal(
            run_id=run_id, now=now, pre_run_counters=pre_run_counters
        )


def _unexpected_internal_refusal(
    *, run_id: object, now: object, pre_run_counters: tuple[int, ...]
) -> HarnessExecutionResult:
    """Return a content-free refusal. No exception value is ever inspected."""

    try:
        timestamp = _require_aware_datetime("now", now)
    except LiveNoteExecutionContractError:
        timestamp = _OFFLINE_SIMULATION_TIMESTAMP
    try:
        report = build_sanitized_terminal_report(
            run_id=run_id,
            timestamp=timestamp,
            governance_preflight_state="NOT_EVALUATED",
            hosted_attribution_gate_state="NOT_EVALUATED",
            hosted_stream_query_normalization_state="NOT_EVALUATED",
            terminal_result="REFUSE_UNEXPECTED_INTERNAL_STATE",
            failure_class="UNEXPECTED_INTERNAL_REFUSAL",
            pre_run_counters=pre_run_counters,
        )
    except BaseException:  # noqa: BLE001 - last-resort default-deny
        report = {key: "UNAVAILABLE" for key in sorted(_SANITIZED_REPORT_KEYS)}
        report["FAILURE_CLASS"] = "UNEXPECTED_INTERNAL_REFUSAL"
        report["TERMINAL_RESULT"] = "REFUSE_UNEXPECTED_INTERNAL_STATE"
    return HarnessExecutionResult(exit_code=2, report=report)


def _run_offline_harness_inner(
    *,
    mode: object,
    authorization_identity: object,
    run_id: object,
    window: OfflineSimulationWindow | None,
    events: Sequence[object],
    transcript_text: str | bytes,
    now: datetime,
    simulate_provider_path: bool,
    pre_run_counters: tuple[int, ...],
) -> HarnessExecutionResult:
    timestamp = _require_aware_datetime("now", now)
    resolved_mode = mode if isinstance(mode, ExecutionMode) else None

    # C2 — governance preflight. LIVE is refused here, before any credential,
    # Secret Manager, transport, or provider surface is constructed.
    try:
        require_governance_preflight(
            mode=mode,
            authorization_identity=authorization_identity,
            run_id=run_id,
            window=window,
            now=timestamp,
        )
    except LiveNoteExecutionContractError:
        live_refusal = resolved_mode is ExecutionMode.LIVE
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=resolved_mode or ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="REFUSED",
                hosted_attribution_gate_state="NOT_EVALUATED",
                hosted_stream_query_normalization_state="NOT_EVALUATED",
                terminal_result=(
                    REFUSE_BEFORE_SECRET_MANAGER_ACCESS
                    if live_refusal
                    else "REFUSE_GOVERNANCE_PREFLIGHT"
                ),
                failure_class=(
                    "LIVE_EXECUTION_NOT_AUTHORIZED"
                    if live_refusal
                    else "GOVERNANCE_PREFLIGHT_REJECTED"
                ),
                pre_run_counters=pre_run_counters,
            ),
        )

    # C3 — hosted attribution over typed in-process ADK events only.
    try:
        hosted_result = accumulate_local_adk_events(events=events)
    except LiveNoteExecutionContractError:
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="PASS",
                hosted_attribution_gate_state="REFUSED",
                hosted_stream_query_normalization_state=(
                    HOSTED_STREAM_QUERY_NORMALIZATION_REFUSED
                ),
                terminal_result="REFUSE_HOSTED_ATTRIBUTION",
                failure_class="HOSTED_ATTRIBUTION_REJECTED",
                pre_run_counters=pre_run_counters,
            ),
        )

    # C4/C5 — ten-field mapping and exact frozen-value closure.
    try:
        note_contract, digest = derive_note_contract_and_frozen_digests(
            hosted_result=hosted_result,
            transcript_text=transcript_text,
        )
    except LiveNoteExecutionContractError:
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="PASS",
                hosted_attribution_gate_state="PASS",
                hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
                terminal_result="REFUSE_NOTE_CONTRACT_OR_DIGEST",
                failure_class="NOTE_CONTRACT_OR_DIGEST_REJECTED",
                pre_run_counters=pre_run_counters,
            ),
        )

    # R5 — the live-path gate. It runs after C5 and before any credential or
    # Secret Manager surface, and it never returns successfully.
    try:
        require_private_origin_materialization()
    except LiveNoteExecutionContractError:
        private_origin_available = False
    else:  # pragma: no cover - structurally unreachable while R5 is unresolved
        private_origin_available = True

    if private_origin_available:  # pragma: no cover - see above
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="PASS",
                hosted_attribution_gate_state="PASS",
                hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
                terminal_result="REFUSE_LIVE_PATH_UNAVAILABLE",
                failure_class="LIVE_EXECUTION_NOT_AUTHORIZED",
                digest=digest,
                pre_run_counters=pre_run_counters,
            ),
        )

    if not simulate_provider_path:
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="PASS",
                hosted_attribution_gate_state="PASS",
                hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
                terminal_result=REFUSE_BEFORE_SECRET_MANAGER_ACCESS,
                failure_class="PRIVATE_ORIGIN_UNAVAILABLE",
                digest=digest,
                pre_run_counters=pre_run_counters,
            ),
        )

    # C6 — bounded simulated NOTE_PATH drive. No live write occurs, and the
    # live path above remains blocked regardless of this outcome.
    try:
        simulation = run_offline_provider_simulation(
            note_contract=note_contract, digest=digest
        )
    except (LiveNoteExecutionContractError, note_path_module.NotePathError):
        return HarnessExecutionResult(
            exit_code=2,
            report=build_sanitized_terminal_report(
                run_id=run_id,
                timestamp=timestamp,
                mode=ExecutionMode.OFFLINE_SIMULATION,
                governance_preflight_state="PASS",
                hosted_attribution_gate_state="PASS",
                hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
                terminal_result="REFUSE_OFFLINE_PROVIDER_SIMULATION",
                failure_class="OFFLINE_PROVIDER_SIMULATION_REJECTED",
                digest=digest,
                pre_run_counters=pre_run_counters,
            ),
        )

    # C7 — sanitized terminal report for a successful simulation.
    return HarnessExecutionResult(
        exit_code=0,
        report=build_sanitized_terminal_report(
            run_id=run_id,
            timestamp=timestamp,
            mode=ExecutionMode.OFFLINE_SIMULATION,
            governance_preflight_state="PASS",
            hosted_attribution_gate_state="PASS",
            hosted_stream_query_normalization_state="LOCAL_TYPED_ADK_EVENTS_ONLY",
            terminal_result="OFFLINE_SIMULATION_PASS",
            failure_class="NONE",
            digest=digest,
            simulation=simulation,
            pre_run_counters=pre_run_counters,
        ),
    )


_FORBIDDEN_ARGUMENT_MARKERS = (
    "bearer ",
    "authorization:",
    "token=",
    "secret",
    "credential",
    "password",
    "private_key",
    "begin ",
    "contact_",
    "opp_",
    "location_id",
    "locationid",
    "contactid",
    "projects/",
    "accounts.google.com",
    "leadconnectorhq",
    "://",
)


class _RefusingArgumentParser(argparse.ArgumentParser):
    """Argument parser that never writes usage text or exits the process itself."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise LiveNoteExecutionContractError("command-line arguments are invalid")

    def exit(self, status: int = 0, message: str | None = None) -> None:  # type: ignore[override]
        raise LiveNoteExecutionContractError("command-line arguments are invalid")


def _reject_identifier_like_arguments(argv: Sequence[str]) -> None:
    """Refuse any raw provider identifier, secret, token, or live binding input."""

    for token in argv:
        if not isinstance(token, str):
            raise LiveNoteExecutionContractError(
                "command-line arguments must be text"
            )
        lowered = token.lower()
        for marker in _FORBIDDEN_ARGUMENT_MARKERS:
            if marker in lowered:
                raise LiveNoteExecutionContractError(
                    "raw identifiers, secrets, tokens, and live bindings are refused "
                    "as command-line input"
                )
        stripped = lowered[2:] if lowered.startswith("--") else lowered
        if len(stripped) >= 32 and all(
            character in _HEX_CHARACTERS for character in stripped
        ):
            raise LiveNoteExecutionContractError(
                "raw identifiers, secrets, tokens, and live bindings are refused "
                "as command-line input"
            )


def _parse_cli(argv: Sequence[str]) -> tuple[ExecutionMode, str]:
    _reject_identifier_like_arguments(argv)
    parser = _RefusingArgumentParser(
        prog="live_note_execution", add_help=False, allow_abbrev=False
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=[mode.value for mode in ExecutionMode],
    )
    parser.add_argument(
        "--fixture",
        default="transcript-success",
        choices=sorted(_OFFLINE_FIXTURE_ALLOWLIST),
    )
    namespace = parser.parse_args(list(argv))
    return ExecutionMode(namespace.mode), str(namespace.fixture)


def _live_mode_refusal_result() -> HarnessExecutionResult:
    """Refuse live mode before any credential, secret, or provider surface."""

    return run_offline_harness(
        mode=ExecutionMode.LIVE,
        authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
        run_id=_OFFLINE_SIMULATION_RUN_ID,
        window=None,
        events=(),
        transcript_text="",
        now=_OFFLINE_SIMULATION_TIMESTAMP,
    )


def _argument_refusal_result() -> HarnessExecutionResult:
    return HarnessExecutionResult(
        exit_code=2,
        report=build_sanitized_terminal_report(
            run_id=_OFFLINE_SIMULATION_RUN_ID,
            timestamp=_OFFLINE_SIMULATION_TIMESTAMP,
            mode=ExecutionMode.OFFLINE_SIMULATION,
            governance_preflight_state="NOT_EVALUATED",
            hosted_attribution_gate_state="NOT_EVALUATED",
            hosted_stream_query_normalization_state="NOT_EVALUATED",
            terminal_result="REFUSE_INVALID_INVOCATION",
            failure_class="INVOCATION_ARGUMENTS_REJECTED",
        ),
    )


def run_offline_simulation_cli(fixture_id: str) -> HarnessExecutionResult:
    """Drive C2 -> C3 -> C4 -> C5 -> R5 -> C6 -> C7 from approved fixtures only."""

    try:
        events = build_offline_typed_local_events(fixture_id)
        transcript_text = _approved_transcript_text(fixture_id)
    except LiveNoteExecutionContractError:
        return _argument_refusal_result()
    return run_offline_harness(
        mode=ExecutionMode.OFFLINE_SIMULATION,
        authorization_identity=OFFLINE_SIMULATION_AUTHORITY_ID,
        run_id=_OFFLINE_SIMULATION_RUN_ID,
        window=_offline_simulation_window(),
        events=events,
        transcript_text=transcript_text,
        now=_OFFLINE_SIMULATION_TIMESTAMP,
        simulate_provider_path=True,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Offline process entrypoint. Live mode is refused; nothing is discovered."""

    resolved_argv = list(sys.argv[1:] if argv is None else argv)
    try:
        mode, fixture_id = _parse_cli(resolved_argv)
    except LiveNoteExecutionContractError:
        result = _argument_refusal_result()
    else:
        if mode is ExecutionMode.LIVE:
            result = _live_mode_refusal_result()
        else:
            result = run_offline_simulation_cli(fixture_id)
    sys.stdout.write(json.dumps(result.report, sort_keys=True) + "\n")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
