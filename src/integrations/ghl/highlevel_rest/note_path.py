"""Offline-only implementation of the HighLevel REST NOTE_PATH."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
import json
import threading
from typing import Any, Mapping, Protocol
from unicodedata import normalize


NETWORK_CALLS = 0
HIGHLEVEL_NETWORK_CALLS = 0
EXTERNAL_EFFECTS = 0
NOTE_POST_BUDGET_PER_WORKFLOW_RUN = 1
NOTE_POST_BUDGET_PER_RUN = NOTE_POST_BUDGET_PER_WORKFLOW_RUN
CONTACT_PREFLIGHT_VERIFIED = "NO"

_TITLE = "MG Guide \u2014 Synthetic Meeting Follow-Up"
_MARKER = "implementation_reviewed_synthetic_marker"
_WORKFLOW_ID = "meeting_follow_up_v1"
_AT8_SOURCE_EXECUTION_UNIT = (
    "NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002"
)
_AT8_SOURCE_PROOF_MERGE_SHA = "6256f287bbd88effc2ef1cd13a801faec79a0af2"
_NOTE_CREATE_OPERATION = "NOTE_CREATE"
_TRUSTED_SOURCE_BOUND_CONTACT = "fake_transport_bound_contact_verification"
_TRUSTED_SOURCE_AT8_SHAPED_TEST = "at8_shaped_test_capability"
_ALLOWED_TRUSTED_SOURCES = frozenset(
    {_TRUSTED_SOURCE_BOUND_CONTACT, _TRUSTED_SOURCE_AT8_SHAPED_TEST}
)
_CAPABILITY_TRUST_MARKER = object()
_REQUIRED_FIELDS = (
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
)
_OPTIONAL_FIELDS: tuple[str, ...] = ()
_LABELS = _REQUIRED_FIELDS + _OPTIONAL_FIELDS


class NotePathError(ValueError):
    """Base error for fail-closed NOTE_PATH validation."""


class BindingError(NotePathError):
    """Raised when a private contact or location binding cannot be verified."""


class NoteContractError(NotePathError):
    """Raised when a logical synthetic meeting note is not exact."""


class TransportError(NotePathError):
    """Raised for a fixture response that cannot verify a note write."""


class _FixtureTransport(Protocol):
    def dispatch(
        self, method: str, path: str, body: Mapping[str, Any] | None = None
    ) -> Any:
        """Dispatch an exact fixture route."""


@dataclass(frozen=True)
class CreatedMeetingNote:
    """Validated identity from a same-run note creation response."""

    note_id: str
    note_content_digest: str
    provider_body_digest: str


@dataclass(frozen=True)
class VerifiedMeetingNote:
    """Successful exact-ID readback verification result."""

    note_id: str
    note_content_digest: str
    provider_body_digest: str


@dataclass(frozen=True)
class _VerifiedContactBindingCapability:
    workflow_id: str
    source_execution_unit: str
    source_proof_merge_sha: str
    location_id: str
    contact_id: str
    consumer_authorization_identity: str
    consumer_workflow_run_id: str
    trusted_source: str
    _trust_marker: object


@dataclass(frozen=True)
class _MutationBudgetKey:
    consumer_authorization_identity: str
    consumer_workflow_run_id: str
    operation: str


class _SharedProcessLocalTestLedger:
    """Process-local atomic reservation ledger for offline test semantics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._states: dict[_MutationBudgetKey, str] = {}

    def reserve(self, key: _MutationBudgetKey) -> bool:
        with self._lock:
            state = self._states.get(key, "AVAILABLE")
            if state != "AVAILABLE":
                return False
            self._states[key] = "RESERVED"
            return True

    def mark_terminal(self, key: _MutationBudgetKey) -> None:
        with self._lock:
            state = self._states.get(key, "AVAILABLE")
            if state == "AVAILABLE":
                raise TransportError("reservation must exist before terminal transition")
            self._states[key] = "TERMINAL"

    def _reset_for_tests(self) -> None:
        with self._lock:
            self._states.clear()


_SHARED_PROCESS_LOCAL_TEST_LEDGER = _SharedProcessLocalTestLedger()


def _reset_shared_test_ledger() -> None:
    _SHARED_PROCESS_LOCAL_TEST_LEDGER._reset_for_tests()


class NotePathAdapter:
    """A private-binding NOTE_PATH that supports only three domain operations."""

    def __init__(
        self,
        location_id: str,
        contact_id: str,
        transport: _FixtureTransport,
        *,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
    ) -> None:
        self._location_id = self._require_identifier("location_id", location_id)
        self._contact_id = self._require_identifier("contact_id", contact_id)
        self._consumer_authorization_identity = self._require_identifier(
            "consumer_authorization_identity", consumer_authorization_identity
        )
        self._consumer_workflow_run_id = self._require_identifier(
            "consumer_workflow_run_id", consumer_workflow_run_id
        )
        self._transport = transport
        self.CONTACT_PREFLIGHT_VERIFIED = CONTACT_PREFLIGHT_VERIFIED
        self.POST_ATTEMPTS = 0
        self._created_note: CreatedMeetingNote | None = None
        self._expected_note: Mapping[str, Any] | None = None
        self._verified_contact_binding_capability: _VerifiedContactBindingCapability | None = (
            None
        )

    def get_bound_contact(self) -> Mapping[str, str]:
        """Fetch and validate only the exact private contact and location binding."""
        response = self._transport.dispatch("GET", f"/contacts/{self._contact_id}")
        contact = self._required_envelope(response, "contact")
        contact_id = contact.get("id")
        location_id = contact.get("locationId")
        if contact_id != self._contact_id:
            raise BindingError("contact id does not match the private binding")
        if location_id != self._location_id:
            raise BindingError("location id does not match the private binding")
        self.CONTACT_PREFLIGHT_VERIFIED = "YES"
        self._verified_contact_binding_capability = (
            self._mint_bound_contact_verified_capability()
        )
        return {"id": contact_id, "locationId": location_id}

    def create_meeting_note(self, note_contract: Mapping[str, Any]) -> CreatedMeetingNote:
        """Serialize one validated synthetic note and consume the one POST budget."""
        capability = self._require_trusted_verified_capability()
        canonical_note = self._validate_note_contract(note_contract)
        if canonical_note["workflow_id"] != capability.workflow_id:
            raise BindingError("verified-contact capability workflow binding is invalid")
        self._reserve_note_create_budget()
        note_body = self._serialize_note(canonical_note)
        note_content_digest = self._logical_digest(canonical_note)
        provider_body = {"body": note_body}
        provider_body_digest = self._provider_body_digest(provider_body)
        response = self._transport.dispatch(
            "POST", f"/contacts/{self._contact_id}/notes", provider_body
        )
        if response.status == "ambiguous":
            raise TransportError("ambiguous note POST result is terminal and is not retried")
        note = self._required_envelope(response, "note")
        note_id = note.get("id")
        note_response_body = note.get("body")
        note_contact_id = note.get("contactId")
        if not isinstance(note_id, str) or not note_id:
            raise TransportError("created note id is required")
        if not isinstance(note_response_body, str) or not note_response_body:
            raise TransportError("created note body is required")
        if note_contact_id != self._contact_id:
            raise TransportError("created note contact id does not match private binding")
        created = CreatedMeetingNote(
            note_id=note_id,
            note_content_digest=note_content_digest,
            provider_body_digest=provider_body_digest,
        )
        self._created_note = created
        self._expected_note = canonical_note
        return created

    def verify_meeting_note(self) -> VerifiedMeetingNote:
        """Read back only the same-run note ID and compare its logical digest."""
        if self._created_note is None or self._expected_note is None:
            raise TransportError("same-run created note id and digest are required")
        response = self._transport.dispatch(
            "GET", f"/contacts/{self._contact_id}/notes/{self._created_note.note_id}"
        )
        note = self._required_envelope(response, "note")
        if note.get("id") != self._created_note.note_id:
            raise TransportError("readback note id does not match same-run created note id")
        if note.get("contactId") != self._contact_id:
            raise TransportError("readback note contact id does not match private binding")
        body = note.get("body")
        if not isinstance(body, str):
            raise TransportError("readback note body is required")
        parsed = self._parse_strict_note_body(body)
        actual_digest = self._logical_digest(parsed)
        if not compare_digest(actual_digest, self._created_note.note_content_digest):
            raise TransportError("NOTE_CONTENT_DIGEST does not match readback")
        return VerifiedMeetingNote(
            note_id=self._created_note.note_id,
            note_content_digest=actual_digest,
            provider_body_digest=self._created_note.provider_body_digest,
        )

    @staticmethod
    def _require_identifier(name: str, value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise BindingError(f"{name} private binding must be a non-empty string")
        return value

    @staticmethod
    def _require_synthetic_identifier(name: str, value: object) -> str:
        text = NotePathAdapter._require_identifier(name, value)
        if not text.startswith("synthetic-"):
            raise BindingError(f"{name} test capability value must be synthetic")
        return text

    @staticmethod
    def _required_envelope(response: Any, envelope_name: str) -> Mapping[str, Any]:
        if getattr(response, "status", None) != "ok":
            raise TransportError(f"{envelope_name} fixture response was not successful")
        payload = getattr(response, "payload", None)
        if not isinstance(payload, Mapping) or set(payload) != {envelope_name}:
            raise TransportError(f"{envelope_name} fixture response is malformed")
        envelope = payload[envelope_name]
        if not isinstance(envelope, Mapping):
            raise TransportError(f"{envelope_name} fixture envelope is malformed")
        return envelope

    def _mint_bound_contact_verified_capability(self) -> _VerifiedContactBindingCapability:
        return _VerifiedContactBindingCapability(
            workflow_id=_WORKFLOW_ID,
            source_execution_unit=_AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=_AT8_SOURCE_PROOF_MERGE_SHA,
            location_id=self._location_id,
            contact_id=self._contact_id,
            consumer_authorization_identity=self._consumer_authorization_identity,
            consumer_workflow_run_id=self._consumer_workflow_run_id,
            trusted_source=_TRUSTED_SOURCE_BOUND_CONTACT,
            _trust_marker=_CAPABILITY_TRUST_MARKER,
        )

    @classmethod
    def _build_at8_shaped_test_capability(
        cls,
        *,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
    ) -> _VerifiedContactBindingCapability:
        return _VerifiedContactBindingCapability(
            workflow_id=cls._require_identifier("workflow_id", workflow_id),
            source_execution_unit=cls._require_identifier(
                "source_execution_unit", source_execution_unit
            ),
            source_proof_merge_sha=cls._require_identifier(
                "source_proof_merge_sha", source_proof_merge_sha
            ),
            location_id=cls._require_synthetic_identifier("location_id", location_id),
            contact_id=cls._require_synthetic_identifier("contact_id", contact_id),
            consumer_authorization_identity=cls._require_identifier(
                "consumer_authorization_identity", consumer_authorization_identity
            ),
            consumer_workflow_run_id=cls._require_identifier(
                "consumer_workflow_run_id", consumer_workflow_run_id
            ),
            trusted_source=_TRUSTED_SOURCE_AT8_SHAPED_TEST,
            _trust_marker=_CAPABILITY_TRUST_MARKER,
        )

    def _require_trusted_verified_capability(self) -> _VerifiedContactBindingCapability:
        capability = self._verified_contact_binding_capability
        if capability is None:
            raise BindingError("successful bound contact preflight is required before POST")
        if (
            not isinstance(capability, _VerifiedContactBindingCapability)
            or capability._trust_marker is not _CAPABILITY_TRUST_MARKER
        ):
            raise BindingError("verified-contact binding capability is invalid")
        if capability.trusted_source not in _ALLOWED_TRUSTED_SOURCES:
            raise BindingError("verified-contact capability trusted source is invalid")
        if capability.workflow_id != _WORKFLOW_ID:
            raise BindingError("verified-contact capability workflow binding is invalid")
        if capability.source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
            raise BindingError("verified-contact capability source execution unit is invalid")
        if capability.source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
            raise BindingError("verified-contact capability source proof is invalid")
        if capability.location_id != self._location_id:
            raise BindingError("verified-contact capability location binding is invalid")
        if capability.contact_id != self._contact_id:
            raise BindingError("verified-contact capability contact binding is invalid")
        if (
            capability.consumer_authorization_identity
            != self._consumer_authorization_identity
        ):
            raise BindingError("verified-contact capability authorization binding is invalid")
        if capability.consumer_workflow_run_id != self._consumer_workflow_run_id:
            raise BindingError("verified-contact capability workflow run binding is invalid")
        return capability

    def _reserve_note_create_budget(self) -> None:
        budget_key = _MutationBudgetKey(
            consumer_authorization_identity=self._consumer_authorization_identity,
            consumer_workflow_run_id=self._consumer_workflow_run_id,
            operation=_NOTE_CREATE_OPERATION,
        )
        if not _SHARED_PROCESS_LOCAL_TEST_LEDGER.reserve(budget_key):
            raise TransportError("NOTE_PATH permits exactly one note POST per workflow run")
        _SHARED_PROCESS_LOCAL_TEST_LEDGER.mark_terminal(budget_key)
        self.POST_ATTEMPTS += 1

    @staticmethod
    def _canonical_json(value: Any) -> str:
        try:
            return json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        except (TypeError, ValueError) as error:
            raise NoteContractError("note values must be canonical JSON") from error

    def _validate_note_contract(self, note_contract: Mapping[str, Any]) -> Mapping[str, Any]:
        if not isinstance(note_contract, Mapping):
            raise NoteContractError("note contract must be an object")
        expected_fields = set(_REQUIRED_FIELDS + _OPTIONAL_FIELDS)
        actual_fields = set(note_contract)
        if actual_fields != set(_REQUIRED_FIELDS) and actual_fields != expected_fields:
            missing = sorted(set(_REQUIRED_FIELDS).difference(actual_fields))
            extra = sorted(actual_fields.difference(expected_fields))
            raise NoteContractError(
                f"note contract fields must be exact; missing={missing}, extra={extra}"
            )
        note = dict(note_contract)
        if note["SYNTHETIC_MARKER"] != _MARKER:
            raise NoteContractError("note contract is not synthetic")
        if note["workflow_id"] != _WORKFLOW_ID:
            raise NoteContractError(f"workflow_id must be {_WORKFLOW_ID}")
        if not isinstance(note["meeting_id"], str) or not note["meeting_id"]:
            raise NoteContractError("meeting_id must be a non-empty string")
        if not isinstance(note["meeting_summary"], str):
            raise NoteContractError("meeting_summary must be a string")
        for field_name in ("needs", "objections"):
            if not isinstance(note[field_name], list) or not all(
                isinstance(item, str) for item in note[field_name]
            ):
                raise NoteContractError(f"{field_name} must be an array of strings")
        if not isinstance(note["commitments"], list):
            raise NoteContractError("commitments must be an array")
        for commitment in note["commitments"]:
            if not isinstance(commitment, Mapping) or set(commitment) - {
                "owner",
                "action",
                "due_date",
            }:
                raise NoteContractError("commitments contain unsupported fields")
            if set(commitment) - {"due_date"} != {"owner", "action"}:
                raise NoteContractError("commitments require owner and action")
            if not all(
                isinstance(commitment[field], str) and commitment[field]
                for field in ("owner", "action")
            ):
                raise NoteContractError("commitment owner and action must be non-empty strings")
            if "due_date" in commitment and not isinstance(commitment["due_date"], str):
                raise NoteContractError("commitment due_date must be a string")
        for field_name in ("next_step", "opportunity_signal"):
            if note[field_name] is not None and not isinstance(note[field_name], Mapping):
                raise NoteContractError(f"{field_name} must be an object or null")
        transcript_hash = note["transcript_hash"]
        if (
            not isinstance(transcript_hash, str)
            or len(transcript_hash) != 64
            or any(character not in "0123456789abcdef" for character in transcript_hash)
        ):
            raise NoteContractError("transcript_hash must be a lowercase SHA-256 hex value")
        self._canonical_json(note)
        return note

    def _serialize_note(self, note_contract: Mapping[str, Any]) -> str:
        lines = [_TITLE]
        for label in _LABELS:
            if label in note_contract:
                lines.append(f"{label}: {self._canonical_json(note_contract[label])}")
        return normalize("NFC", "\n".join(lines) + "\n")

    def _parse_strict_note_body(self, body: str) -> Mapping[str, Any]:
        if normalize("NFC", body) != body or not body.endswith("\n") or body.endswith("\n\n"):
            raise TransportError("readback note body has non-canonical normalization or newline")
        lines = body[:-1].split("\n")
        if not lines or lines[0] != _TITLE:
            raise TransportError("readback note title is invalid")
        values: dict[str, Any] = {}
        expected_labels = iter(_LABELS)
        for line in lines[1:]:
            label, separator, encoded_value = line.partition(": ")
            if not separator or not encoded_value:
                raise TransportError("readback note contains an invalid labeled line")
            try:
                expected_label = next(expected_labels)
            except StopIteration as error:
                raise TransportError("readback note contains an unknown label") from error
            if label != expected_label:
                if label in values:
                    raise TransportError("readback note contains a duplicate label")
                raise TransportError("readback note contains an unknown or unordered label")
            try:
                value = json.loads(encoded_value)
            except json.JSONDecodeError as error:
                raise TransportError("readback note label is not canonical JSON") from error
            if self._canonical_json(value) != encoded_value:
                raise TransportError("readback note label JSON is not canonical")
            values[label] = value
        if set(values) not in (set(_REQUIRED_FIELDS), set(_REQUIRED_FIELDS + _OPTIONAL_FIELDS)):
            raise TransportError("readback note has missing required labels")
        parsed = self._validate_note_contract(values)
        if self._expected_note is None:
            raise TransportError("expected note contract is unavailable")
        for field_name in ("meeting_id", "transcript_hash", "workflow_id"):
            if parsed[field_name] != self._expected_note[field_name]:
                raise TransportError(f"readback note {field_name} does not match the created note")
        return parsed

    def _logical_digest(self, note_contract: Mapping[str, Any]) -> str:
        return sha256(self._canonical_json(note_contract).encode("utf-8")).hexdigest()

    def _provider_body_digest(self, provider_body: Mapping[str, str]) -> str:
        return sha256(self._canonical_json(provider_body).encode("utf-8")).hexdigest()
