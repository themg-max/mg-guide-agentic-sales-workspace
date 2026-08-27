"""Offline-only implementation of the HighLevel REST NOTE_PATH."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
import importlib
import json
import sys
import threading
from types import ModuleType
from typing import Any, Mapping, Protocol
from unicodedata import normalize
import weakref

from integrations.ghl.at1_execution_store import (
    At1ExecutionStore,
    AttemptStateError,
    DuplicateBusinessOrdinalError,
    ExecutionClaimError,
    RunContinuationRefusedError,
)


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
NOTE_CREATE_OPERATION_ORDINAL = 1
_MAPPING_VERSION = 1
_GRANT_RUN_ID_NAMESPACE = "NOTE_PATH"
_GRANT_RUN_ID_PREFIX = "npgr1:"
_STORE_BOUNDARY_ERRORS = (
    ExecutionClaimError,
    RunContinuationRefusedError,
    DuplicateBusinessOrdinalError,
    AttemptStateError,
)
_REDACTED_RESPONSE_STATUS_CLASSES = frozenset({"ok", "ambiguous", "error"})
_TRUSTED_SOURCE_BOUND_CONTACT = "fake_transport_bound_contact_verification"
_TRUSTED_SOURCE_AT8_SHAPED_TEST = "at8_shaped_test_capability"
_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF = "private_at8_verified_binding_handoff"
_TRUSTED_SOURCE_DESIGNATED_PRIVATE_OWNER_INGRESS = (
    "designated_private_owner_verified_binding_ingress"
)
_DESIGNATED_PRIVATE_OWNER_ID = (
    "NW008_AT8W30_R3_PRIVATE_OWNER_LEASE_INGRESS_DESIGNATION_001"
)
# Root-owned process configuration naming the private control-plane module
# that originates designated-owner anchors. Only the process root sets this;
# a public caller cannot designate an authority origin.
_ROOT_OWNED_PRIVATE_ORIGIN_MODULE_KEY = (
    "MG_GUIDE_NW008_PRIVATE_OWNER_ORIGIN_MODULE"
)
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


def _require_boolean(name: str, value: object) -> bool:
    if not isinstance(value, bool):
        raise BindingError(f"{name} must be a boolean")
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
    synthetic_contact_bound: bool = True
    private_allowlist_complete: bool = True
    relationship_verified: bool = True


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
    synthetic_contact_bound: bool
    private_allowlist_complete: bool
    relationship_verified: bool
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


@dataclass(frozen=True)
class _BoundContactGetVerificationSnapshot:
    location_id: str
    contact_id: str
    consumer_authorization_identity: str
    consumer_workflow_run_id: str


class _OpaqueSafePrivateBindingReference:
    """Opaque, process-local, one-shot handle to a private binding lease.

    The reference carries no binding data, no provenance strings, and no
    capability. It is only recognizable by identity inside the issuing process,
    so it cannot be serialized, copied, or reconstructed by a public caller.
    """

    __slots__ = ("__weakref__",)

    def __repr__(self) -> str:
        return "<opaque-safe-private-binding-reference>"

    def __reduce__(self) -> Any:
        raise BindingError("private binding lease reference is not serializable")

    def __reduce_ex__(self, protocol: int) -> Any:
        raise BindingError("private binding lease reference is not serializable")

    def __getstate__(self) -> Any:
        raise BindingError("private binding lease reference is not serializable")

    def __copy__(self) -> Any:
        raise BindingError("private binding lease reference is not copyable")

    def __deepcopy__(self, memo: Any) -> Any:
        raise BindingError("private binding lease reference is not copyable")


@dataclass(frozen=True)
class _PrivateOwnerAnchorSnapshot:
    """Verified reading of a private-origin anchor.

    This is a *verification result*, not a provisioning record. It is derived
    by reading an anchor artifact that the private control plane created; this
    module never creates the anchor it reads.
    """

    resolver_ref: object
    consumer_authorization_identity: str
    consumer_workflow_run_id: str


@dataclass(frozen=True)
class _PrivateBindingLeaseRecord:
    """Private-side lease content that never crosses the boundary."""

    trusted_binding_source: _TrustedPrivateBindingSource
    consumer_authorization_identity: str
    consumer_workflow_run_id: str
    test_only_fail_capability_issuance: bool
    trust_marker: object


class _OneShotPrivateBindingLeaseRegistry:
    """Process-local leases consumed atomically before any capability issuance."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: dict[
            int, tuple[weakref.ref[object], _PrivateBindingLeaseRecord, str]
        ] = {}

    def register(
        self,
        reference: _OpaqueSafePrivateBindingReference,
        record: _PrivateBindingLeaseRecord,
    ) -> None:
        reference_id = id(reference)

        def _cleanup(ref: weakref.ref[object], *, key: int = reference_id) -> None:
            with self._lock:
                entry = self._records.get(key)
                if entry is not None and entry[0] is ref:
                    self._records.pop(key, None)

        with self._lock:
            self._records[reference_id] = (
                weakref.ref(reference, _cleanup),
                record,
                "AVAILABLE",
            )

    def consume(
        self, reference: _OpaqueSafePrivateBindingReference
    ) -> _PrivateBindingLeaseRecord:
        """Atomically spend the lease, or fail without spending valid authority."""
        with self._lock:
            entry = self._records.get(id(reference))
            if entry is None or entry[0]() is not reference:
                raise BindingError("private binding lease reference is not recognized")
            weak_reference, record, state = entry
            if state != "AVAILABLE":
                raise BindingError("private binding lease is already consumed")
            self._records[id(reference)] = (weak_reference, record, "CONSUMED")
            return record

    def state(self, reference: object) -> str:
        with self._lock:
            entry = self._records.get(id(reference))
            if entry is None or entry[0]() is not reference:
                return "UNRECOGNIZED"
            return entry[2]


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


def _build_internal_trust_issuer() -> tuple[Any, ...]:
    """Create origin-isolated issuers that own non-exported trust markers."""

    source_markers = {
        _TRUSTED_SOURCE_BOUND_CONTACT: object(),
        _TRUSTED_SOURCE_AT8_SHAPED_TEST: object(),
        _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF: object(),
        _TRUSTED_SOURCE_DESIGNATED_PRIVATE_OWNER_INGRESS: object(),
    }
    capability_markers = {
        _TRUSTED_SOURCE_BOUND_CONTACT: object(),
        _TRUSTED_SOURCE_AT8_SHAPED_TEST: object(),
        _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF: object(),
        _TRUSTED_SOURCE_DESIGNATED_PRIVATE_OWNER_INGRESS: object(),
    }
    issued_sources = _IdentityRegistry()
    issued_capabilities = _IdentityRegistry()
    verified_bound_contact_gets = _IdentityRegistry()
    private_binding_leases = _OneShotPrivateBindingLeaseRegistry()
    lease_marker = object()

    def _issue_source(
        *,
        trusted_origin: str,
        location_id: str,
        contact_id: str,
        synthetic_contact_bound: bool,
        private_allowlist_complete: bool,
        relationship_verified: bool,
    ) -> _TrustedPrivateBindingSource:
        source = _TrustedPrivateBindingSource(
            workflow_id=_WORKFLOW_ID,
            source_execution_unit=_AT8_SOURCE_EXECUTION_UNIT,
            source_proof_merge_sha=_AT8_SOURCE_PROOF_MERGE_SHA,
            location_id=_require_identifier("location_id", location_id),
            contact_id=_require_identifier("contact_id", contact_id),
            synthetic_contact_bound=_require_boolean(
                "synthetic_contact_bound", synthetic_contact_bound
            ),
            private_allowlist_complete=_require_boolean(
                "private_allowlist_complete", private_allowlist_complete
            ),
            relationship_verified=_require_boolean(
                "relationship_verified", relationship_verified
            ),
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
                synthetic_contact_bound=source.synthetic_contact_bound,
                private_allowlist_complete=source.private_allowlist_complete,
                relationship_verified=source.relationship_verified,
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
        if not isinstance(adapter, NotePathAdapter):
            raise BindingError("successful bound contact preflight is required")
        verification_snapshot = verified_bound_contact_gets.get(adapter)
        if not isinstance(verification_snapshot, _BoundContactGetVerificationSnapshot):
            raise BindingError("successful bound contact preflight is required")
        if (
            adapter._location_id != verification_snapshot.location_id
            or adapter._contact_id != verification_snapshot.contact_id
            or (
                adapter._consumer_authorization_identity
                != verification_snapshot.consumer_authorization_identity
            )
            or adapter._consumer_workflow_run_id
            != verification_snapshot.consumer_workflow_run_id
        ):
            raise BindingError("successful bound contact preflight is required")
        source = _issue_source(
            trusted_origin=_TRUSTED_SOURCE_BOUND_CONTACT,
            location_id=verification_snapshot.location_id,
            contact_id=verification_snapshot.contact_id,
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
        )
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_BOUND_CONTACT,
            location_id=verification_snapshot.location_id,
            contact_id=verification_snapshot.contact_id,
            consumer_authorization_identity=verification_snapshot.consumer_authorization_identity,
            consumer_workflow_run_id=verification_snapshot.consumer_workflow_run_id,
            trusted_binding_source=source,
        )

    def build_bound_contact_get() -> Any:
        def get_bound_contact(adapter: NotePathAdapter) -> Mapping[str, str]:
            """Fetch and verify the exact private binding before recording issuer evidence."""
            response = adapter._transport.dispatch(
                "GET", f"/contacts/{adapter._contact_id}"
            )
            contact = adapter._required_envelope(response, "contact")
            contact_id = contact.get("id")
            location_id = contact.get("locationId")
            if contact_id != adapter._contact_id:
                raise BindingError("contact id does not match the private binding")
            if location_id != adapter._location_id:
                raise BindingError("location id does not match the private binding")
            verified_bound_contact_gets.add(
                adapter,
                _BoundContactGetVerificationSnapshot(
                    location_id=adapter._location_id,
                    contact_id=adapter._contact_id,
                    consumer_authorization_identity=adapter._consumer_authorization_identity,
                    consumer_workflow_run_id=adapter._consumer_workflow_run_id,
                ),
            )
            adapter.CONTACT_PREFLIGHT_VERIFIED = "YES"
            adapter._verified_contact_binding_capability = issue_bound_contact_capability(
                adapter=adapter,
            )
            return {"id": contact_id, "locationId": location_id}

        return get_bound_contact

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
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
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
            synthetic_contact_bound=True,
            private_allowlist_complete=True,
            relationship_verified=True,
        )

    def _require_private_at8_handoff_source(
        trusted_binding_source: object,
    ) -> _TrustedPrivateBindingSource:
        if (
            not isinstance(trusted_binding_source, _TrustedPrivateBindingSource)
            or not isinstance(
                issued_sources.get(trusted_binding_source), _SourceIssuanceSnapshot
            )
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        source_snapshot = issued_sources.get(trusted_binding_source)
        assert isinstance(source_snapshot, _SourceIssuanceSnapshot)
        if (
            source_snapshot.trusted_origin != _TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF
            or trusted_binding_source
            != _TrustedPrivateBindingSource(
                workflow_id=source_snapshot.workflow_id,
                source_execution_unit=source_snapshot.source_execution_unit,
                source_proof_merge_sha=source_snapshot.source_proof_merge_sha,
                location_id=source_snapshot.location_id,
                contact_id=source_snapshot.contact_id,
                synthetic_contact_bound=source_snapshot.synthetic_contact_bound,
                private_allowlist_complete=source_snapshot.private_allowlist_complete,
                relationship_verified=source_snapshot.relationship_verified,
                trusted_origin=source_snapshot.trusted_origin,
                _trust_marker=source_snapshot.trust_marker,
            )
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        if (
            trusted_binding_source._trust_marker
            is not source_markers[_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF]
        ):
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
            not trusted_binding_source.synthetic_contact_bound
            or not trusted_binding_source.private_allowlist_complete
            or not trusted_binding_source.relationship_verified
        ):
            raise BindingError("verified-contact capability trusted binding source is invalid")
        return trusted_binding_source

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
        trusted_binding_source = _require_private_at8_handoff_source(
            trusted_binding_source
        )
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

    def materialize_private_at8_binding_lease(
        *,
        trusted_binding_source: object,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
        test_only_fail_capability_issuance: bool = False,
    ) -> _OpaqueSafePrivateBindingReference:
        """Materialize the private one-shot lease before any public consumption.

        The lease is bound at materialization time to the exact consumer
        authorization identity and workflow run. A public string presented later
        can only match or fail; it can never create or retarget authority.
        """
        test_only_fail_capability_issuance = _require_boolean(
            "test_only_fail_capability_issuance", test_only_fail_capability_issuance
        )
        _require_at8_provenance(
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
        )
        registered_source = _require_private_at8_handoff_source(trusted_binding_source)
        record = _PrivateBindingLeaseRecord(
            trusted_binding_source=registered_source,
            consumer_authorization_identity=_require_identifier(
                "consumer_authorization_identity", consumer_authorization_identity
            ),
            consumer_workflow_run_id=_require_identifier(
                "consumer_workflow_run_id", consumer_workflow_run_id
            ),
            test_only_fail_capability_issuance=test_only_fail_capability_issuance,
            trust_marker=lease_marker,
        )
        reference = _OpaqueSafePrivateBindingReference()
        private_binding_leases.register(reference, record)
        return reference

    def issue_private_at8_binding_reference_for_synthetic_tests(
        *,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
        test_only_fail_capability_issuance: bool = False,
    ) -> _OpaqueSafePrivateBindingReference:
        """Issue synthetic test references through the private owner only."""
        trusted_binding_source = issue_private_at8_handoff_source_for_synthetic_tests(
            location_id=location_id,
            contact_id=contact_id,
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
        )
        return materialize_private_at8_binding_lease(
            trusted_binding_source=trusted_binding_source,
            consumer_authorization_identity=consumer_authorization_identity,
            consumer_workflow_run_id=consumer_workflow_run_id,
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
            test_only_fail_capability_issuance=test_only_fail_capability_issuance,
        )

    def consume_private_at8_binding_lease(
        private_binding_reference: object,
        *,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
    ) -> _VerifiedContactBindingCapability:
        """Consume the lease atomically, then issue the capability it authorizes.

        Unrecognized, forged, serialized, or copied references fail closed
        without spending valid authority. A recognized reference is spent before
        any binding comparison, so identity or workflow-run mismatch fails closed
        and leaves the authority consumed.
        """
        if not isinstance(private_binding_reference, _OpaqueSafePrivateBindingReference):
            raise BindingError("private binding lease reference is not recognized")
        record = private_binding_leases.consume(private_binding_reference)
        if (
            not isinstance(record, _PrivateBindingLeaseRecord)
            or record.trust_marker is not lease_marker
        ):
            raise BindingError("private binding lease reference is not recognized")
        expected_authorization_identity = _require_identifier(
            "consumer_authorization_identity", consumer_authorization_identity
        )
        expected_workflow_run_id = _require_identifier(
            "consumer_workflow_run_id", consumer_workflow_run_id
        )
        if record.consumer_authorization_identity != expected_authorization_identity:
            raise BindingError("private binding lease authorization binding is invalid")
        if record.consumer_workflow_run_id != expected_workflow_run_id:
            raise BindingError("private binding lease workflow run binding is invalid")
        registered_source = _require_private_at8_handoff_source(
            record.trusted_binding_source
        )
        if record.test_only_fail_capability_issuance:
            raise BindingError(
                "synthetic private binding capability issuance failed"
            )
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_PRIVATE_AT8_HANDOFF,
            location_id=registered_source.location_id,
            contact_id=registered_source.contact_id,
            consumer_authorization_identity=expected_authorization_identity,
            consumer_workflow_run_id=expected_workflow_run_id,
            trusted_binding_source=registered_source,
        )

    # This module performs NO authority origin. It contains no owner-
    # provisioning authority type, no anchor registry, and no bootstrap. The
    # designated-owner anchor is an artifact created by the private control
    # plane, which is the sole authority source. Public code below only
    # *reads and verifies* such an artifact; it never creates, registers, or
    # vouches for one, at import time or at any later time.
    #
    # Authenticity rests on an unforgeable artifact from a module that the
    # PROCESS ROOT designated, not on the artifact's own claims. Duck-typing
    # and self-declared contracts are deliberately NOT accepted: a caller can
    # always author a module that asserts it is the private control plane, so
    # any self-certifying check would be worthless. The trust root is
    # root-owned process configuration, exactly like every other root-owned
    # dependency this runtime consumes.
    def _root_designated_private_origin_module() -> object | None:
        """Return the private-origin module the process root designated.

        The module name comes from root-owned process configuration. A public
        caller cannot designate it, and this module never falls back to a
        caller-supplied or self-declared origin.
        """
        # Deferred, indirect lookup: this module never imports ``os`` at
        # module scope, preserving the offline-purity guarantee that no
        # environment/network-capable module is imported by note_path.
        module_name = importlib.import_module("os").environ.get(
            _ROOT_OWNED_PRIVATE_ORIGIN_MODULE_KEY
        )
        if not isinstance(module_name, str) or not module_name.strip():
            return None
        # Only an already-imported module is honoured. This runtime never
        # imports a module on a caller's behalf.
        return sys.modules.get(module_name.strip())

    def _read_private_origin_anchor(
        private_owner_anchor: object,
    ) -> _PrivateOwnerAnchorSnapshot | None:
        """Read a private-origin anchor artifact, or return None.

        The anchor must be an instance of the provisioned-resolver type
        exported by the root-designated private-origin module, and that type
        must genuinely refuse public construction. This public module holds no
        registry and confers nothing: it can only accept or refuse.
        """
        private_origin_module = _root_designated_private_origin_module()
        if private_origin_module is None:
            return None
        anchor_type = type(private_owner_anchor)
        if getattr(
            private_origin_module, "ProvisionedPrivateOwnerResolver", None
        ) is not anchor_type:
            return None
        # The artifact must genuinely refuse public construction. This is
        # checked behaviourally, so a module cannot merely *claim* it.
        try:
            anchor_type()
        except Exception:
            pass
        else:
            return None
        # Finally the private origin itself must recognise the artifact as one
        # it actually provisioned. Type identity alone would still admit an
        # instance reconstructed through ``__new__``, so recognition is
        # delegated to the origin rather than inferred here.
        recognises = getattr(private_origin_module, "is_genuinely_provisioned", None)
        if not callable(recognises):
            return None
        try:
            if recognises(private_owner_anchor) is not True:
                return None
        except Exception:
            return None
        designation_id = getattr(private_owner_anchor, "designation_id", None)
        resolver = getattr(private_owner_anchor, "provisioned_resolver", None)
        authorization_identity = getattr(
            private_owner_anchor, "consumer_authorization_identity", None
        )
        workflow_run_id = getattr(
            private_owner_anchor, "consumer_workflow_run_id", None
        )
        if (
            designation_id != _DESIGNATED_PRIVATE_OWNER_ID
            or not isinstance(resolver, ModuleType)
            or not isinstance(authorization_identity, str)
            or not isinstance(workflow_run_id, str)
            or not authorization_identity.strip()
            or not workflow_run_id.strip()
        ):
            return None
        return _PrivateOwnerAnchorSnapshot(
            resolver_ref=weakref.ref(resolver),
            consumer_authorization_identity=authorization_identity,
            consumer_workflow_run_id=workflow_run_id,
        )

    def _require_authentic_designated_private_owner(
        *,
        private_owner_resolver: object,
        private_owner_anchor: object,
    ) -> _PrivateOwnerAnchorSnapshot:
        """Verify genuine private-owner provenance before any private release.

        Module shape, designation strings, exported class types, and callable
        release functions are caller-reproducible and are never sufficient.
        Authenticity rests entirely on the anchor artifact's own private-origin
        attestation, which binds it to this exact resolver object. This module
        never provisions an anchor, so it can only accept or refuse one.
        """
        if (
            not isinstance(private_owner_resolver, ModuleType)
            or getattr(private_owner_resolver, "DESIGNATION_ID", None)
            != _DESIGNATED_PRIVATE_OWNER_ID
        ):
            raise BindingError("designated private owner resolver is invalid")
        anchor_snapshot = _read_private_origin_anchor(private_owner_anchor)
        if (
            not isinstance(anchor_snapshot, _PrivateOwnerAnchorSnapshot)
            or anchor_snapshot.resolver_ref() is not private_owner_resolver
        ):
            raise BindingError(
                "designated private owner authenticity anchor is invalid"
            )
        return anchor_snapshot

    def consume_designated_private_owner_binding_reference(
        *,
        private_owner_resolver: object,
        private_binding_reference: object,
        private_owner_anchor: object,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
    ) -> _VerifiedContactBindingCapability:
        """Consume a designated owner's sealed reference after exact run binding.

        The resolver is a process-local capability from the designated private
        owner, and the anchor is the unforgeable process-local proof that this
        exact resolver was provisioned by the private control plane. Both are
        verified before the private owner is invoked. The resolver releases
        only already-verified binding data; public code never accepts raw
        binding data or materializes a production lease.
        """
        presented_authorization_identity = _require_identifier(
            "consumer_authorization_identity", consumer_authorization_identity
        )
        presented_workflow_run_id = _require_identifier(
            "consumer_workflow_run_id", consumer_workflow_run_id
        )
        anchor_snapshot = _require_authentic_designated_private_owner(
            private_owner_resolver=private_owner_resolver,
            private_owner_anchor=private_owner_anchor,
        )
        expected_authorization_identity = (
            anchor_snapshot.consumer_authorization_identity
        )
        expected_workflow_run_id = anchor_snapshot.consumer_workflow_run_id
        if presented_authorization_identity != expected_authorization_identity:
            raise BindingError("designated private owner authorization binding is invalid")
        if presented_workflow_run_id != expected_workflow_run_id:
            raise BindingError("designated private owner workflow run binding is invalid")

        reference_type = getattr(
            private_owner_resolver, "OpaqueSafePrivateBindingReference", None
        )
        material_type = getattr(private_owner_resolver, "PrivateBindingMaterial", None)
        release = getattr(private_owner_resolver, "release_to_public_consumer", None)
        if (
            not isinstance(reference_type, type)
            or not isinstance(material_type, type)
            or not callable(release)
            or not isinstance(private_binding_reference, reference_type)
        ):
            raise BindingError("designated private owner reference is invalid")

        material = release(private_binding_reference)
        if (
            not isinstance(material, material_type)
            or getattr(material, "designation_id", None) != _DESIGNATED_PRIVATE_OWNER_ID
        ):
            raise BindingError("designated private owner binding material is invalid")
        provider_ids = getattr(material, "provider_ids", None)
        if (
            not isinstance(provider_ids, tuple)
            or len(provider_ids) != 2
            or not all(isinstance(value, str) and value.strip() for value in provider_ids)
        ):
            raise BindingError("designated private owner binding material is invalid")
        location_id, contact_id = provider_ids
        source = _issue_source(
            trusted_origin=_TRUSTED_SOURCE_DESIGNATED_PRIVATE_OWNER_INGRESS,
            location_id=location_id,
            contact_id=contact_id,
            synthetic_contact_bound=False,
            private_allowlist_complete=True,
            relationship_verified=True,
        )
        return _issue_capability(
            trusted_origin=_TRUSTED_SOURCE_DESIGNATED_PRIVATE_OWNER_INGRESS,
            location_id=location_id,
            contact_id=contact_id,
            consumer_authorization_identity=expected_authorization_identity,
            consumer_workflow_run_id=expected_workflow_run_id,
            trusted_binding_source=source,
        )

    def private_at8_binding_lease_state(private_binding_reference: object) -> str:
        """Report lease lifecycle state without granting or spending authority."""
        if not isinstance(private_binding_reference, _OpaqueSafePrivateBindingReference):
            return "UNRECOGNIZED"
        return private_binding_leases.state(private_binding_reference)

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
            synthetic_contact_bound=source_snapshot.synthetic_contact_bound,
            private_allowlist_complete=source_snapshot.private_allowlist_complete,
            relationship_verified=source_snapshot.relationship_verified,
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
        issue_private_at8_binding_reference_for_synthetic_tests,
        consume_private_at8_binding_lease,
        consume_designated_private_owner_binding_reference,
        private_at8_binding_lease_state,
        build_bound_contact_get,
        require_issued_verified_capability,
    )


(
    _issue_bound_contact_capability,
    _issue_synthetic_test_capability,
    _issue_private_at8_handoff_source_for_synthetic_tests,
    _handoff_private_at8_capability_from_registered_source,
    _issue_private_at8_binding_reference_for_synthetic_tests,
    _consume_private_at8_binding_lease,
    _consume_designated_private_owner_binding_reference,
    _private_at8_binding_lease_state,
    _build_bound_contact_get,
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
        execution_store: At1ExecutionStore | None = None,
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
        self._execution_store = execution_store
        self.CONTACT_PREFLIGHT_VERIFIED = CONTACT_PREFLIGHT_VERIFIED
        self.POST_ATTEMPTS = 0
        self._created_note: CreatedMeetingNote | None = None
        self._expected_note: Mapping[str, Any] | None = None
        self._verified_contact_binding_capability: _VerifiedContactBindingCapability | None = (
            None
        )

    get_bound_contact = _build_bound_contact_get()

    def create_meeting_note(self, note_contract: Mapping[str, Any]) -> CreatedMeetingNote:
        """Serialize one validated synthetic note and consume the one POST budget."""
        capability = self._require_trusted_verified_capability()
        canonical_note = self._validate_note_contract(note_contract)
        if canonical_note["workflow_id"] != capability.workflow_id:
            raise BindingError("verified-contact capability workflow binding is invalid")
        if self._execution_store is not None:
            return self._create_meeting_note_with_store(canonical_note)
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

    def _deterministic_grant_run_id(self) -> str:
        """Return a deterministic, privacy-preserving grant/run identifier.

        The mapping intentionally excludes all private CRM identifiers. Only the
        consumer authorization identity, the consumer workflow run id, and the
        fixed mapping coordinates are canonicalized.
        """
        canonical = self._canonical_json(
            {
                "consumer_authorization_identity": self._consumer_authorization_identity,
                "consumer_workflow_run_id": self._consumer_workflow_run_id,
                "mapping_version": _MAPPING_VERSION,
                "namespace": _GRANT_RUN_ID_NAMESPACE,
                "operation": _NOTE_CREATE_OPERATION,
            }
        )
        digest = sha256(canonical.encode("utf-8")).hexdigest()
        return f"{_GRANT_RUN_ID_PREFIX}{digest}"

    def _request_id_for_attempt(
        self, grant_run_id: str, operation_ordinal: int
    ) -> str:
        """Return a deterministic request id for a grant-run/ordinal pair."""
        payload = self._canonical_json(
            {"grant_run_id": grant_run_id, "operation_ordinal": operation_ordinal}
        )
        return sha256(payload.encode("utf-8")).hexdigest()

    def _build_redacted_request_envelope(
        self,
        *,
        request_id: str,
        note_content_digest: str,
        provider_body_digest: str,
    ) -> dict[str, Any]:
        """Return a redacted request envelope that contains no private CRM data."""
        return {
            "namespace": _GRANT_RUN_ID_NAMESPACE,
            "operation": _NOTE_CREATE_OPERATION,
            "operation_ordinal": NOTE_CREATE_OPERATION_ORDINAL,
            "mapping_version": _MAPPING_VERSION,
            "consumer_authorization_identity": self._consumer_authorization_identity,
            "consumer_workflow_run_id": self._consumer_workflow_run_id,
            "workflow_id": _WORKFLOW_ID,
            "request_id": request_id,
            "note_content_digest": note_content_digest,
            "provider_body_digest": provider_body_digest,
        }

    @staticmethod
    def _response_status_class(response: Any) -> str:
        status = getattr(response, "status", None)
        if status in _REDACTED_RESPONSE_STATUS_CLASSES:
            return str(status)
        return "error"

    def _build_redacted_response_envelope(
        self,
        *,
        request_id: str,
        note_content_digest: str,
        provider_body_digest: str,
        response: Any,
    ) -> dict[str, Any]:
        """Return a redacted response envelope from the authorization allowlist."""
        return {
            "namespace": _GRANT_RUN_ID_NAMESPACE,
            "operation": _NOTE_CREATE_OPERATION,
            "operation_ordinal": NOTE_CREATE_OPERATION_ORDINAL,
            "mapping_version": _MAPPING_VERSION,
            "consumer_authorization_identity": self._consumer_authorization_identity,
            "consumer_workflow_run_id": self._consumer_workflow_run_id,
            "workflow_id": _WORKFLOW_ID,
            "request_id": request_id,
            "note_content_digest": note_content_digest,
            "provider_body_digest": provider_body_digest,
            "response_status_class": self._response_status_class(response),
        }

    def _terminalize_unknown(
        self, grant_run_id: str, operation_ordinal: int, failure_code: str
    ) -> None:
        """Terminalize an attempt with UNKNOWN business-effect truth.

        Offline-only NOTE_PATH can never prove a live business effect, so the
        durable truth is always UNKNOWN rather than YES or NO.
        """
        if self._execution_store is None:
            return
        try:
            self._execution_store.mark_terminal(
                grant_run_id=grant_run_id,
                operation_ordinal=operation_ordinal,
                failure_code=failure_code,
                business_effect_truth="UNKNOWN",
            )
        except _STORE_BOUNDARY_ERRORS as exc:
            raise TransportError("NOTE_PATH store reservation refused") from exc

    def _create_meeting_note_with_store(
        self, canonical_note: Mapping[str, Any]
    ) -> CreatedMeetingNote:
        """Execute NOTE_CREATE through the durable offline execution store."""
        assert self._execution_store is not None
        grant_run_id = self._deterministic_grant_run_id()
        request_id = self._request_id_for_attempt(
            grant_run_id, NOTE_CREATE_OPERATION_ORDINAL
        )
        note_body = self._serialize_note(canonical_note)
        note_content_digest = self._logical_digest(canonical_note)
        provider_body = {"body": note_body}
        provider_body_digest = self._provider_body_digest(provider_body)
        redacted_request_envelope = self._build_redacted_request_envelope(
            request_id=request_id,
            note_content_digest=note_content_digest,
            provider_body_digest=provider_body_digest,
        )

        try:
            self._execution_store.acquire_claim(
                grant_run_id, self._consumer_authorization_identity
            )
            self._execution_store.require_run_continuable(grant_run_id)
            self._execution_store.record_attempt(
                grant_run_id=grant_run_id,
                operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                operation_id=_NOTE_CREATE_OPERATION,
                request_id=request_id,
                request_envelope=redacted_request_envelope,
            )
            self._execution_store.mark_dispatched(
                grant_run_id=grant_run_id,
                operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
            )
        except _STORE_BOUNDARY_ERRORS as exc:
            raise TransportError("NOTE_PATH store reservation refused") from exc

        try:
            response = self._transport.dispatch(
                "POST", f"/contacts/{self._contact_id}/notes", provider_body
            )
        except Exception:
            self._terminalize_unknown(
                grant_run_id,
                NOTE_CREATE_OPERATION_ORDINAL,
                failure_code="DISPATCH_EXCEPTION",
            )
            raise

        redacted_response_envelope = self._build_redacted_response_envelope(
            request_id=request_id,
            note_content_digest=note_content_digest,
            provider_body_digest=provider_body_digest,
            response=response,
        )
        try:
            self._execution_store.capture_response(
                grant_run_id=grant_run_id,
                operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                response_envelope=redacted_response_envelope,
            )

            if response.status == "ambiguous":
                self._execution_store.record_parse_outcome(
                    grant_run_id=grant_run_id,
                    operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                    success=False,
                )
                self._execution_store.record_semantic_outcome(
                    grant_run_id=grant_run_id,
                    operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                    success=False,
                )
                self._terminalize_unknown(
                    grant_run_id,
                    NOTE_CREATE_OPERATION_ORDINAL,
                    failure_code="AMBIGUOUS_POST",
                )
                raise TransportError(
                    "ambiguous note POST result is terminal and is not retried"
                )

            try:
                note = self._required_envelope(response, "note")
                note_id = note.get("id")
                note_response_body = note.get("body")
                note_contact_id = note.get("contactId")
                if not isinstance(note_id, str) or not note_id:
                    raise TransportError("created note id is required")
                if not isinstance(note_response_body, str) or not note_response_body:
                    raise TransportError("created note body is required")
                if note_contact_id != self._contact_id:
                    raise TransportError(
                        "created note contact id does not match private binding"
                    )
            except TransportError:
                self._execution_store.record_parse_outcome(
                    grant_run_id=grant_run_id,
                    operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                    success=False,
                )
                self._execution_store.record_semantic_outcome(
                    grant_run_id=grant_run_id,
                    operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                    success=False,
                )
                self._terminalize_unknown(
                    grant_run_id,
                    NOTE_CREATE_OPERATION_ORDINAL,
                    failure_code="PARSE_FAILURE",
                )
                raise

            self._execution_store.record_parse_outcome(
                grant_run_id=grant_run_id,
                operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                success=True,
            )
            self._execution_store.record_semantic_outcome(
                grant_run_id=grant_run_id,
                operation_ordinal=NOTE_CREATE_OPERATION_ORDINAL,
                success=True,
            )
        except _STORE_BOUNDARY_ERRORS as exc:
            raise TransportError("NOTE_PATH store reservation refused") from exc

        created = CreatedMeetingNote(
            note_id=note_id,
            note_content_digest=note_content_digest,
            provider_body_digest=provider_body_digest,
        )
        self._created_note = created
        self._expected_note = canonical_note
        self.POST_ATTEMPTS += 1
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

    @classmethod
    def _build_private_at8_binding_lease_for_tests(
        cls,
        *,
        location_id: str,
        contact_id: str,
        consumer_authorization_identity: str,
        consumer_workflow_run_id: str,
        workflow_id: str = _WORKFLOW_ID,
        source_execution_unit: str = _AT8_SOURCE_EXECUTION_UNIT,
        source_proof_merge_sha: str = _AT8_SOURCE_PROOF_MERGE_SHA,
        test_only_fail_capability_issuance: bool = False,
    ) -> _OpaqueSafePrivateBindingReference:
        """Model the owner-issued private lease using synthetic inputs only."""
        return _issue_private_at8_binding_reference_for_synthetic_tests(
            location_id=cls._require_synthetic_identifier("location_id", location_id),
            contact_id=cls._require_synthetic_identifier("contact_id", contact_id),
            consumer_authorization_identity=cls._require_identifier(
                "consumer_authorization_identity", consumer_authorization_identity
            ),
            consumer_workflow_run_id=cls._require_identifier(
                "consumer_workflow_run_id", consumer_workflow_run_id
            ),
            workflow_id=workflow_id,
            source_execution_unit=source_execution_unit,
            source_proof_merge_sha=source_proof_merge_sha,
            test_only_fail_capability_issuance=test_only_fail_capability_issuance,
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
