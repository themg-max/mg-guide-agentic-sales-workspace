"""Bounded, fixture-only HighLevel REST NOTE_PATH implementation."""

from .fake_transport import DeterministicFakeTransport, FakeResponse
from .note_path import (
    BindingError,
    CONTACT_PREFLIGHT_VERIFIED,
    CreatedMeetingNote,
    NoteContractError,
    NotePathAdapter,
    NotePathError,
    TransportError,
    VerifiedMeetingNote,
)

__all__ = [
    "BindingError",
    "CONTACT_PREFLIGHT_VERIFIED",
    "CreatedMeetingNote",
    "DeterministicFakeTransport",
    "FakeResponse",
    "NoteContractError",
    "NotePathAdapter",
    "NotePathError",
    "TransportError",
    "VerifiedMeetingNote",
]
