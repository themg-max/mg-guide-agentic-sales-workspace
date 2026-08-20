"""Offline-only implementation of the HighLevel REST NOTE_PATH."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
import json
from typing import Any, Mapping, Protocol
from unicodedata import normalize


NETWORK_CALLS = 0
HIGHLEVEL_NETWORK_CALLS = 0
EXTERNAL_EFFECTS = 0
NOTE_POST_BUDGET_PER_RUN = 1
CONTACT_PREFLIGHT_VERIFIED = "NO"

_TITLE = "MG Guide \u2014 Synthetic Meeting Follow-Up"
_MARKER = "implementation_reviewed_synthetic_marker"
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


class NotePathAdapter:
    """A private-binding NOTE_PATH that supports only three domain operations."""

    def __init__(
        self, location_id: str, contact_id: str, transport: _FixtureTransport
    ) -> None:
        self._location_id = self._require_identifier("location_id", location_id)
        self._contact_id = self._require_identifier("contact_id", contact_id)
        self._transport = transport
        self.CONTACT_PREFLIGHT_VERIFIED = CONTACT_PREFLIGHT_VERIFIED
        self.POST_ATTEMPTS = 0
        self._created_note: CreatedMeetingNote | None = None
        self._expected_note: Mapping[str, Any] | None = None

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
        return {"id": contact_id, "locationId": location_id}

    def create_meeting_note(self, note_contract: Mapping[str, Any]) -> CreatedMeetingNote:
        """Serialize one validated synthetic note and consume the one POST budget."""
        if self.CONTACT_PREFLIGHT_VERIFIED != "YES":
            raise BindingError("successful bound contact preflight is required before POST")
        canonical_note = self._validate_note_contract(note_contract)
        note_body = self._serialize_note(canonical_note)
        note_content_digest = self._logical_digest(canonical_note)
        provider_body = {"body": note_body}
        provider_body_digest = self._provider_body_digest(provider_body)
        self._consume_note_write_budget()
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

    def _consume_note_write_budget(self) -> None:
        if self.POST_ATTEMPTS >= NOTE_POST_BUDGET_PER_RUN:
            raise TransportError("NOTE_PATH permits exactly one note POST per run")
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
        if note["workflow_id"] != "meeting_follow_up_v1":
            raise NoteContractError("workflow_id must be meeting_follow_up_v1")
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
