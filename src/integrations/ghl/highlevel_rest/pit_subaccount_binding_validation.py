"""Offline evaluator for the frozen one-read PIT/sub-account binding probe."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping

from .live_note_transport import (
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
    derive_private_provider_error_evidence,
    project_public_provider_error_evidence,
)


FROZEN_METHOD = "GET"
FROZEN_PATH_TEMPLATE = "/locations/{private_validation_location_id}"
VERSION_HEADER = "v3"
MAX_READS = 1
MAX_WRITES = 0
MAX_TOTAL_BUSINESS_CALLS = 1
NO_RETRY = True
NETWORK_ENABLED = False
LIVE_GHL_CALLS = False
SECRET_MANAGER_ACCESS = False
TARGET_SA_IMPERSONATION = False


class PitSubaccountBindingValidationError(ValueError):
    """Raised when the private evaluator input is malformed."""


class PitSubaccountBindingValidationTerminalStateError(RuntimeError):
    """Raised when an evaluator is asked to consume more than one result."""


@dataclass(frozen=True)
class PitSubaccountBindingValidationResult:
    """Public-safe result for one consumed, injected read outcome."""

    disposition: str
    public_proof: Mapping[str, Any]
    business_calls_attempted: int
    reads_attempted: int
    writes_attempted: int
    retry_performed: bool


class OfflinePitSubaccountBindingValidationExecutor:
    """Evaluate exactly one injected result without a network or credential path."""

    def __init__(self, *, private_validation_location_id: str) -> None:
        if (
            not isinstance(private_validation_location_id, str)
            or not private_validation_location_id.strip()
        ):
            raise PitSubaccountBindingValidationError(
                "private_validation_location_id must be a non-empty string"
            )
        self._private_validation_location_id = private_validation_location_id
        self._consumed = False

    def evaluate(
        self, outcome: LiveNoteHttpResult | LiveNoteHttpUncertainty
    ) -> PitSubaccountBindingValidationResult:
        """Consume one fixture result and fail closed for every non-PASS outcome."""
        if self._consumed:
            raise PitSubaccountBindingValidationTerminalStateError(
                "the one-read binding evaluation has already consumed its call budget"
            )
        if not isinstance(outcome, (LiveNoteHttpResult, LiveNoteHttpUncertainty)):
            raise PitSubaccountBindingValidationError(
                "outcome must be a LiveNoteHttpResult or LiveNoteHttpUncertainty"
            )
        self._consumed = True

        if isinstance(outcome, LiveNoteHttpUncertainty):
            return self._result(
                disposition="FAIL_AMBIGUOUS_READ",
                public_proof={
                    "READ_FAILURE_CLASS": "AMBIGUOUS",
                    "RAW_LOCATION_ID_PUBLIC": "NO",
                    "TOKEN_OR_PIT_PUBLISHED": "NO",
                },
            )

        status_code = outcome.status_code
        if type(status_code) is not int:
            return self._closed_result(http_status=None)
        if status_code == 200:
            envelope_present, returned_location_id = self._parse_success_envelope(
                outcome.body
            )
            returned_location_id_match = (
                envelope_present == "YES"
                and returned_location_id == self._private_validation_location_id
            )
            return self._result(
                disposition="PASS" if returned_location_id_match else "FAIL_CLOSED",
                public_proof={
                    "HTTP_STATUS": status_code,
                    "LOCATION_ENVELOPE_PRESENT": envelope_present,
                    "RETURNED_LOCATION_ID_MATCH": (
                        "YES" if returned_location_id_match else "NO"
                    ),
                    "PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH": (
                        "YES" if returned_location_id_match else "NO"
                    ),
                    "RAW_LOCATION_ID_PUBLIC": "NO",
                    "TOKEN_OR_PIT_PUBLISHED": "NO",
                },
            )
        if 100 <= status_code <= 599 and not 200 <= status_code <= 299:
            private_evidence = derive_private_provider_error_evidence(outcome)
            public_evidence = project_public_provider_error_evidence(
                private_evidence
            ).as_public_dict()
            public_evidence["RAW_LOCATION_ID_PUBLIC"] = "NO"
            return self._result(disposition="FAIL_CLOSED", public_proof=public_evidence)
        return self._closed_result(http_status=status_code)

    def _closed_result(
        self, *, http_status: int | None
    ) -> PitSubaccountBindingValidationResult:
        proof: dict[str, Any] = {
            "LOCATION_ENVELOPE_PRESENT": "NO",
            "RETURNED_LOCATION_ID_MATCH": "NO",
            "PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH": "NO",
            "RAW_LOCATION_ID_PUBLIC": "NO",
            "TOKEN_OR_PIT_PUBLISHED": "NO",
        }
        if http_status is not None:
            proof["HTTP_STATUS"] = http_status
        return self._result(disposition="FAIL_CLOSED", public_proof=proof)

    def _result(
        self, *, disposition: str, public_proof: Mapping[str, Any]
    ) -> PitSubaccountBindingValidationResult:
        return PitSubaccountBindingValidationResult(
            disposition=disposition,
            public_proof=dict(public_proof),
            business_calls_attempted=1,
            reads_attempted=1,
            writes_attempted=0,
            retry_performed=False,
        )

    @staticmethod
    def _parse_success_envelope(body: object) -> tuple[str, str | None]:
        """Accept only ``location.id`` or a bare top-level location ``id``."""
        if not isinstance(body, (bytes, bytearray)):
            return "NO", None
        try:
            decoded = json.loads(bytes(body).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return "NO", None
        if not isinstance(decoded, Mapping):
            return "NO", None

        if "location" in decoded:
            location = decoded["location"]
            if not isinstance(location, Mapping):
                return "NO", None
            location_id = location.get("id")
        else:
            location_id = decoded.get("id")

        if not isinstance(location_id, str) or not location_id.strip():
            return "NO", None
        return "YES", location_id
