"""Offline-only implementation of the HighLevel REST NOTE_PATH."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
import json
import threading
from typing import Any, Mapping, Protocol
from unicodedata import normalize
import weakref


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
_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF = "private_at8_verified_binding_handoff"
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


def _require_identifier(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BindingError(f"{name} private binding must be a non-empty string")
    return value


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
class _PrivateContactBinding:
    """Private target data only. Not authorization and not a trusted capability."""

    location_id: str
    contact_id: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "location_id", _require_identifier("location_id", self.location_id)
        )
        object.__setattr__(
            self, "contact_id", _require_identifier("contact_id", self.contact_id)
        )


@dataclass(frozen=True)
class _TrustedPrivateBindingSource:
    """Internal provenance marker for a validated private binding."""

    workflow_id: str
    source_execution_unit: str
    source_proof_merge_sha: str
    location_id: str
    contact_id: str
    trusted_origin: str
    _trust_marker: object


@dataclass(frozen=True)
class _VerifiedContactBindingCapability:
    workflow_id: str
    source_execution_unit: str
    source_proof_merge_sha: str
    location_id: str
    contact_id: str
    consumer_authorization_identity: str
    consumer_workflow_run_id: str
    trusted_binding_source: _TrustedPrivateBindingSource
    _trust_marker: object


@dataclass(frozen=True)
class _SourceIssuanceSnapshot:
    workflow_id: str
    source_execution_unit: str
    source_proof_merge_sha: str
    location_id: str
    contact_id: str
    trusted_origin: str
    trust_marker: object


@dataclass(frozen=True)
class _CapabilityIssuanceSnapshot:
    workflow_id: str
    source_execution_unit: str
    source_proof_merge_sha: str
    location_id: str
    contact_id: str
    consumer_authorization_identity: str
    consumer_workflow_run_id: str
    trusted_origin: str
    trusted_source_object_identity: int
    trust_marker: object


class _IdentityRegistry:
    """Process-local object identities paired with immutable issuance records."""

    def __init__(self) -> None:
        self._records: dict[int, tuple[weakref.ref[object], object]] = {}

    def add(self, obj: object, snapshot: object) -> None:
        obj_id = id(obj)

        def _cleanup(ref: weakref.ref[object], *, key: int = obj_id) -> None:
            record = self._records.get(key)
            if record is not None and record[0] is ref:
                self._records.pop(key, None)

        self._records[obj_id] = (weakref.ref(obj, _cleanup), snapshot)

    def get(self, obj: object) -> object | None:
        record = self._records.get(id(obj))
        if record is None or record[0]() is not obj:
            return None
        return record[1]


def _require_at8_provenance(
    *,
    workflow_id: str,
    source_execution_unit: str,
    source_proof_merge_sha: str,
) -> None:
    if workflow_id != _WORKFLOW_ID:
        raise BindingError("verified-contact capability workflow binding is invalid")
    if source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
        raise BindingError("verified-contact capability source execution unit is invalid")
    if source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
        raise BindingError("verified-contact capability source proof is invalid")


def _build_internal_trust_issuer() -> tuple[Any, Any, Any, Any, Any]:
    """Create origin-isolated issuers that own non-exported trust markers."""

    source_markers = {
        _TRUSTED_SOURCE_BOUND_CONTACT: object(),
        _TRUSTED_SOURCE_AT8_SHAPED_TEST: object(),
        _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF: object(),
    }
    capability_markers = {
        _TRUSTED_SOURCE_BOUND_CONTACT: object(),
        _TRUSTED_SOURCE_AT8_SHAPED_TEST: object(),
        _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF: object(),
    }
    issued_sources = _IdentityRegistry()
    issued_capabilities = _IdentityRegistry()

    def _issue_source(
        *,
        trusted_origin: str,
        location_id: str,
        contact_id: str,
    ) -> _TrustedPrivateBindingSource:
        source = _TrustedPrivateBindingSource(
            workflow_id=_WORKFLOW_ID,
            source_execution_unit=_AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=_AT8_SOURCE_PROOF_MERGE_SHA,
            location_id=_require_identifier("location_id", location_id),
            contact_id=_require_identifier("contact_id", contact_id),
            trusted_origin=trusted_origin,
            _trust_marker=source_markers[trusted_origin],
        )
        issued_sources.add(
            source,
            _SourceIssuanceSnapshot(
                workflow_id=source.workflow_id,
                source_execution_unit=source.source_execution_unit,
                source_proof_merge_sha=source.source_proof_merge_sha,
                location_id=source.location_id,
                contact_id=source.contact_id,
                trusted_origin=source.trusted_origin,
                trust_marker=source._trust_marker,
            ),
        )
        return source

    def _issue_capability(
        *,
        trusted_origin: str,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        trusted_binding_source: _TrustedPrivateBindingSource,
    ) -> _VerifiedContactBindingCapability:
        capability = _VerifiedContactBindingCapability(
            workflow_id=_WORKFLOW_ID,
            source_execution_unit=_AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=_AT8_SOURCE_PROOF_MERGE_SHA,
            location_id=location_id,
            contact_id=contact_id,
            consumer_authorization_identity=_require_identifier(
                "consumer_authorization_identity", consumer_authorization_identity
            ),
            consumer_workflow_run_id=_require_identifier(
                "consumer_workflow_run_id", consumer_workflow_run_id
            ),
            trusted_binding_source=trusted_binding_source,
            _trust_marker=capability_markers[trusted_origin],
        )
        issued_capabilities.add(
            capability,
            _CapabilityIssuanceSnapshot(
                workflow_id=capability.workflow_id,
                source_execution_unit=capability.source_execution_unit,
                source_proof_merge_sha=capability.source_proof_merge_sha,
                location_id=capability.location_id,
                contact_id=capability.contact_id,
                consumer_authorization_identity=capability.consumer_authorization_identity,
                consumer_workflow_run_id=capability.consumer_workflow_run_id,
                trusted_origin=trusted_origin,
                trusted_source_object_identity=id(trusted_binding_source),
                trust_marker=capability._trust_marker,
            ),
        )
        return capability

    def issue_bound_contact_capability(
        *,
        adapter: object,
    ) -> _VerifiedContactBindingCapability:
        if (
            not isinstance(adapter, NotePathAdapter)
            or adapter._verified_bound_contact_preflight
            is not adapter._bound_contact_preflight_marker
        ):
            raise BindingError("successful bound contact preflight is required")
        source = _issue_source(
            trusted_origin=_TRUSTED_SOURCE_BOUND_CONTACT,
            location_id=adapter._location_id,
            contact_id=adapter._contact_id,
        )
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_BOUND_CONTACT,
            location_id=adapter._location_id,
            contact_id=adapter._contact_id,
            consumer_authorization_identity=adapter._consumer_authorization_identity,
            consumer_workflow_run_id=adapter._consumer_workflow_run_id,
            trusted_binding_source=source,
        )

    def issue_synthetic_test_capability(
        *,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
    ) -> _VerifiedContactBindingCapability:
        _require_at8_provenance(
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
        )
        if not location_id.startswith("synthetic-"):
            raise BindingError("location_id test capability value must be synthetic")
        if not contact_id.startswith("synthetic-"):
            raise BindingError("contact_id test capability value must be synthetic")
        location_id = _require_identifier("location_id", location_id)
        contact_id = _require_identifier("contact_id", contact_id)
        source = _issue_source(
            trusted_origin=_TRUSTED_SOURCE_AT8_SHAPED_TEST,
            location_id=location_id,
            contact_id=contact_id,
        )
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_AT8_SHAPED_TEST,
            location_id=location_id,
            contact_id=contact_id,
            consumer_authorization_identity=consumer_authorization_identity,
            consumer_workflow_run_id=consumer_workflow_run_id,
            trusted_binding_source=source,
        )

    def issue_private_at8_handoff_source_for_synthetic_tests(
        *,
        location_id: str,
        contact_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
    ) -> _TrustedPrivateBindingSource:
        _require_at8_provenance(
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
        )
        location_id = _require_identifier("location_id", location_id)
        contact_id = _require_identifier("contact_id", contact_id)
        if not location_id.startswith("synthetic-"):
            raise BindingError("location_id private AT8 handoff source value must be synthetic")
        if not contact_id.startswith("synthetic-"):
            raise BindingError("contact_id private AT8 handoff source value must be synthetic")
        return _issue_source(
            trusted_origin=_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF,
            location_id=location_id,
            contact_id=contact_id,
        )

    def handoff_private_at8_capability_from_registered_source(
        *,
        trusted_binding_source: object,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
    ) -> _VerifiedContactBindingCapability:
        _require_at8_provenance(
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
        )
        if (
            not isinstance(trusted_binding_source, _TrustedPrivateBindingSource)
            or not isinstance(issued_sources.get(trusted_binding_source), _SourceIssuanceSnapshot)
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        source_snapshot = issued_sources.get(trusted_binding_source)
        assert isinstance(source_snapshot, _SourceIssuanceSnapshot)
        if (
            source_snapshot.trusted_origin != _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF
            or trusted_binding_source != _TrustedPrivateBindingSource(
                workflow_id=source_snapshot.workflow_id,
                source_execution_unit=source_snapshot.source_execution_unit,
                source_proof_merge_sha=source_snapshot.source_proof_merge_sha,
                location_id=source_snapshot.location_id,
                contact_id=source_snapshot.contact_id,
                trusted_origin=source_snapshot.trusted_origin,
                _trust_marker=source_snapshot.trust_marker,
            )
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if trusted_binding_source._trust_marker is not source_markers[_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF]:
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if trusted_binding_source.workflow_id != _WORKFLOW_ID:
            raise BindingError(
                "verified-contact capability trusted binding source workflow is invalid"
            )
        if trusted_binding_source.source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
            raise BindingError(
                "verified-contact capability trusted binding source execution unit is invalid"
            )
        if trusted_binding_source.source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
            raise BindingError("verified-contact capability trusted binding source proof is invalid")
        if (
            not trusted_binding_source.location_id.startswith("synthetic-")
            or not trusted_binding_source.contact_id.startswith("synthetic-")
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF,
            location_id=trusted_binding_source.location_id,
            contact_id=trusted_binding_source.contact_id,
            consumer_authorization_identity=_require_identifier(
                "consumer_authorization_identity", consumer_authorization_identity
            ),
            consumer_workflow_run_id=_require_identifier(
                "consumer_workflow_run_id", consumer_workflow_run_id
            ),
            trusted_binding_source=trusted_binding_source,
        )

    def require_issued_verified_capability(
        capability: _VerifiedContactBindingCapability | None,
        *,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
    ) -> _VerifiedContactBindingCapability:
        if capability is None:
            raise BindingError("successful bound contact preflight is required before POST")
        if (
            not isinstance(capability, _VerifiedContactBindingCapability)
            or not isinstance(issued_capabilities.get(capability), _CapabilityIssuanceSnapshot)
        ):
            raise BindingError("verified-contact binding capability is invalid")
        capability_snapshot = issued_capabilities.get(capability)
        assert isinstance(capability_snapshot, _CapabilityIssuanceSnapshot)
        trusted_binding_source = capability.trusted_binding_source
        if (
            not isinstance(trusted_binding_source, _TrustedPrivateBindingSource)
            or not isinstance(issued_sources.get(trusted_binding_source), _SourceIssuanceSnapshot)
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        source_snapshot = issued_sources.get(trusted_binding_source)
        assert isinstance(source_snapshot, _SourceIssuanceSnapshot)
        if trusted_binding_source != _TrustedPrivateBindingSource(
            workflow_id=source_snapshot.workflow_id,
            source_execution_unit=source_snapshot.source_execution_unit,
            source_proof_merge_sha=source_snapshot.source_proof_merge_sha,
            location_id=source_snapshot.location_id,
            contact_id=source_snapshot.contact_id,
            trusted_origin=source_snapshot.trusted_origin,
            _trust_marker=source_snapshot.trust_marker,
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if (
            capability != _VerifiedContactBindingCapability(
                workflow_id=capability_snapshot.workflow_id,
                source_execution_unit=capability_snapshot.source_execution_unit,
                source_proof_merge_sha=capability_snapshot.source_proof_merge_sha,
                location_id=capability_snapshot.location_id,
                contact_id=capability_snapshot.contact_id,
                consumer_authorization_identity=capability_snapshot.consumer_authorization_identity,
                consumer_workflow_run_id=capability_snapshot.consumer_workflow_run_id,
                trusted_binding_source=trusted_binding_source,
                _trust_marker=capability_snapshot.trust_marker,
            )
            or source_snapshot.trusted_origin != capability_snapshot.trusted_origin
            or id(trusted_binding_source) != capability_snapshot.trusted_source_object_identity
        ):
            if capability.workflow_id != _WORKFLOW_ID:
                raise BindingError("verified-contact capability workflow binding is invalid")
            if capability.source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
                raise BindingError("verified-contact capability source execution unit is invalid")
            if capability.source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
                raise BindingError("verified-contact capability source proof is invalid")
            if capability.consumer_authorization_identity != consumer_authorization_identity:
                raise BindingError("verified-contact capability authorization binding is invalid")
            if capability.consumer_workflow_run_id != consumer_workflow_run_id:
                raise BindingError("verified-contact capability workflow run binding is invalid")
            raise BindingError("verified-contact binding capability is invalid")
        trusted_origin = source_snapshot.trusted_origin
        if trusted_origin not in source_markers:
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if trusted_binding_source._trust_marker is not source_markers[trusted_origin]:
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if capability._trust_marker is not capability_markers[trusted_origin]:
            raise BindingError("verified-contact binding capability is invalid")
        if trusted_binding_source.workflow_id != _WORKFLOW_ID:
            raise BindingError(
                "verified-contact capability trusted binding source workflow is invalid"
            )
        if trusted_binding_source.source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
            raise BindingError(
                "verified-contact capability trusted binding source execution unit is invalid"
            )
        if trusted_binding_source.source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
            raise BindingError("verified-contact capability trusted binding source proof is invalid")
        if capability.workflow_id != _WORKFLOW_ID:
            raise BindingError("verified-contact capability workflow binding is invalid")
        if capability.source_execution_unit != _AT8_SOURCE_EXECUTION_UNIT:
            raise BindingError("verified-contact capability source execution unit is invalid")
        if capability.source_proof_merge_sha != _AT8_SOURCE_PROOF_MERGE_SHA:
            raise BindingError("verified-contact capability source proof is invalid")
        if capability.location_id != location_id:
            raise BindingError("verified-contact capability location binding is invalid")
        if capability.contact_id != contact_id:
            raise BindingError("verified-contact capability contact binding is invalid")
        if capability.consumer_authorization_identity != consumer_authorization_identity:
            raise BindingError("verified-contact capability authorization binding is invalid")
        if capability.consumer_workflow_run_id != consumer_workflow_run_id:
            raise BindingError("verified-contact capability workflow run binding is invalid")
        if (
            trusted_binding_source.location_id != capability.location_id
            or trusted_binding_source.contact_id != capability.contact_id
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        return capability

    return (
        issue_bound_contact_capability,
        issue_synthetic_test_capability,
        issue_private_at8_handoff_source_for_synthetic_tests,
        handoff_private_at8_capability_from_registered_source,
        require_issued_verified_capability,
    )


(
    _issue_bound_contact_capability,
    _issue_synthetic_test_capability,
    _issue_private_at8_handoff_source_for_synthetic_tests,
    _handoff_private_at8_capability_from_registered_source,
    _require_issued_verified_capability,
) = _build_internal_trust_issuer()


def _handoff_private_at8_verified_binding_capability(
    *,
    source_execution_unit: str,
    source_proof_merge_sha: str,
    consumer_authorization_identity: str,
    consumer_workflow_run_id: str,
    workflow_id: str,
    trusted_binding_source: object,
) -> _VerifiedContactBindingCapability:
    """Private AT8 handoff is not a generic capability issuer.

    Bound-contact and synthetic origins have their own issuers. Caller-supplied
    trusted sources, raw private bindings, and AT8 strings alone cannot mint.
    """
    return _handoff_private_at8_capability_from_registered_source(
        trusted_binding_source=trusted_binding_source,
        source_execution_unit=source_execution_unit,
        source_proof_merge_sha=source_proof_merge_sha,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
        workflow_id=workflow_id,
    )


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
        self._bound_contact_preflight_marker = object()
        self._verified_bound_contact_preflight: object | None = None
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
        self._verified_bound_contact_preflight = self._bound_contact_preflight_marker
        verified_contact = {"id": contact_id, "locationId": location_id}
        self._verified_contact_binding_capability = _issue_bound_contact_capability(
            adapter=self,
        )
        return verified_contact

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
        return _require_identifier(name, value)

    @staticmethod
    def _require_synthetic_identifier(name: str, value: object) -> str:
        text = _require_identifier(name, value)
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
        return _issue_synthetic_test_capability(
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
        )

    @classmethod
    def _build_private_at8_verified_binding_source(
        cls,
        *,
        location_id: str,
        contact_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
    ) -> _TrustedPrivateBindingSource:
        return _issue_private_at8_handoff_source_for_synthetic_tests(
            workflow_id=cls._require_identifier("workflow_id", workflow_id),
            source_execution_unit=cls._require_identifier(
                "source_execution_unit", source_execution_unit
            ),
            source_proof_merge_sha=cls._require_identifier(
                "source_proof_merge_sha", source_proof_merge_sha
            ),
            location_id=cls._require_synthetic_identifier("location_id", location_id),
            contact_id=cls._require_synthetic_identifier("contact_id", contact_id),
        )

    def _require_trusted_verified_capability(self) -> _VerifiedContactBindingCapability:
        return _require_issued_verified_capability(
            self._verified_contact_binding_capability,
            location_id=self._location_id,
            contact_id=self._contact_id,
            consumer_authorization_identity=self._consumer_authorization_identity,
            consumer_workflow_run_id=self._consumer_workflow_run_id,
        )

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
