"""Fixture-only, exact-ID executor for the NW-008 AT-1 operation sequence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence

from integrations.ghl.at1_live_transport_serializer import (
    At1ExecutionContext,
    At1LiveTransportSerializer,
    IdempotencyKeyError,
)


PIPELINE_METADATA_RUNTIME_READ_REQUIRED = "NO"
NETWORK_ENABLED = "NO"
GHL_LIVE_CLIENT = "NO"
FIRESTORE_CLIENT = "NO"
NOTE_WRITE_ATTEMPTS_MAX = 1
NOTE_WRITES_SUCCEEDED_MAX = 1
STAGE_WRITE_ATTEMPTS_MAX = 1
STAGE_WRITES_SUCCEEDED_MAX = 1

EXACT_OPERATION_ORDER = (
    "get-contact",
    "get-opportunity",
    "create-note",
    "get-note",
    "update-opportunity",
    "get-opportunity",
)
_ALLOWED_OPERATIONS = frozenset(EXACT_OPERATION_ORDER)
_FIXTURE_POLICY = {
    "source": "synthetic_only",
    "network_enabled": False,
    "ghl_live_client": False,
    "firestore_client": False,
}
_FIXTURE_ROOT_FIELDS = frozenset({*_FIXTURE_POLICY, "binding", "cases"})


class InputContractError(ValueError):
    """Raised when an AT-1 binding is missing, malformed, or broadened."""


class UnexpectedOperationError(ValueError):
    """Raised when a fixture transport receives an operation outside AT-1."""


class TerminalStateError(RuntimeError):
    """Raised if any caller tries to dispatch after a terminal failure."""


class WriteAttemptRefusedError(RuntimeError):
    """Raised before transport when a write attempt budget is exhausted."""


class FixturePolicyError(ValueError):
    """Raised when a fixture could permit data or effects outside the offline policy."""


@dataclass(frozen=True)
class BoundedAt1Input:
    """The complete public AT-1 binding contract; values must be synthetic in tests."""

    location_id: str
    contact_id: str
    opportunity_id: str
    expected_initial_stage_id: str
    authorized_final_stage_id: str
    expected_note_content_or_fingerprint: str

    def __post_init__(self) -> None:
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.strip():
                raise InputContractError(f"{field_name} must be a non-empty string")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "BoundedAt1Input":
        expected_fields = {
            "location_id",
            "contact_id",
            "opportunity_id",
            "expected_initial_stage_id",
            "authorized_final_stage_id",
            "expected_note_content_or_fingerprint",
        }
        actual_fields = set(value)
        if actual_fields != expected_fields:
            missing = sorted(expected_fields.difference(actual_fields))
            extra = sorted(actual_fields.difference(expected_fields))
            raise InputContractError(
                f"AT-1 binding fields must be exact; missing={missing}, extra={extra}"
            )
        return cls(**dict(value))


@dataclass(frozen=True)
class FixtureResponse:
    """A deterministic response that never represents a network request."""

    status: str
    record: Mapping[str, Any] = field(default_factory=dict)
    error_code: str | None = None


class GhlFixtureTransport(Protocol):
    """Transport seam deliberately limited to pre-authored fixture responses."""

    def dispatch(self, envelope: Mapping[str, Any]) -> FixtureResponse:
        """Return one deterministic response for an allowed exact-ID envelope."""


class DeterministicGhlFixtureTransport:
    """Consumes an ordered synthetic fixture case with no client or network support."""

    def __init__(self, fixture: Mapping[str, Any], case_id: str) -> None:
        self._validate_fixture_policy(fixture)
        cases = fixture["cases"]
        case = cases.get(case_id)
        if not isinstance(case, Mapping):
            raise FixturePolicyError(f"fixture case {case_id!r} must be an object")
        calls = case.get("calls")
        if not isinstance(calls, Sequence) or isinstance(calls, (str, bytes)):
            raise FixturePolicyError(f"fixture case {case_id!r} requires a calls array")
        if not all(isinstance(call, Mapping) for call in calls):
            raise FixturePolicyError(f"fixture case {case_id!r} calls must be objects")
        self._calls = [dict(call) for call in calls]
        self.calls: list[tuple[str, dict[str, str]]] = []
        self.envelopes: list[dict[str, Any]] = []

    @staticmethod
    def _validate_fixture_policy(fixture: Mapping[str, Any]) -> None:
        if not isinstance(fixture, Mapping):
            raise FixturePolicyError("fixture root must be an object")
        actual_fields = set(fixture)
        if actual_fields != _FIXTURE_ROOT_FIELDS:
            missing = sorted(_FIXTURE_ROOT_FIELDS.difference(actual_fields))
            extra = sorted(actual_fields.difference(_FIXTURE_ROOT_FIELDS))
            raise FixturePolicyError(
                f"fixture root fields must be exact; missing={missing}, extra={extra}"
            )
        for field_name, expected_value in _FIXTURE_POLICY.items():
            actual_value = fixture[field_name]
            if isinstance(expected_value, bool):
                valid = type(actual_value) is bool and actual_value is expected_value
            else:
                valid = type(actual_value) is str and actual_value == expected_value
            if not valid:
                raise FixturePolicyError(
                    f"fixture policy requires {field_name}={expected_value!r}"
                )
        if not isinstance(fixture["binding"], Mapping):
            raise FixturePolicyError("fixture binding must be an object")
        if not isinstance(fixture["cases"], Mapping):
            raise FixturePolicyError("fixture cases must be an object")

    def dispatch(self, envelope: Mapping[str, Any]) -> FixtureResponse:
        if not isinstance(envelope, Mapping):
            raise UnexpectedOperationError("transport envelope must be an object")
        if envelope.get("name") != "execute_operation":
            raise UnexpectedOperationError(
                "transport envelope must call execute_operation"
            )
        arguments_map = dict(envelope.get("arguments", {}))
        operation_id = arguments_map.get("operationId")
        params = dict(arguments_map.get("params", {}))
        path = params.get("path", {})
        body = params.get("body", None)
        if not isinstance(path, Mapping):
            raise UnexpectedOperationError("params.path must be an object")
        if body is not None and not isinstance(body, Mapping):
            raise UnexpectedOperationError("params.body must be an object when present")

        if operation_id not in _ALLOWED_OPERATIONS:
            raise UnexpectedOperationError(
                f"{operation_id} is outside the bounded AT-1 operation surface"
            )
        if not self._calls:
            raise UnexpectedOperationError(
                f"fixture did not authorize another {operation_id} call"
            )

        expected = self._calls.pop(0)
        if expected.get("operation_id") != operation_id:
            raise UnexpectedOperationError(
                f"fixture expected {expected.get('operation_id')!r}, got {operation_id!r}"
            )
        expected_arguments = expected.get("arguments", {})
        if not isinstance(expected_arguments, Mapping):
            raise UnexpectedOperationError("fixture expected arguments must be an object")

        if not self._matches_expected_wire_arguments(
            operation_id, dict(expected_arguments), dict(path), body
        ):
            raise UnexpectedOperationError(
                f"fixture arguments differ for {operation_id}: "
                f"expected {expected_arguments!r}, got path={dict(path)!r}, body={body!r}"
            )

        self.calls.append((operation_id, dict(expected_arguments)))
        self.envelopes.append(dict(envelope))
        return FixtureResponse(
            status=str(expected.get("response", {}).get("status", "error")),
            record=dict(expected.get("response", {}).get("record", {})),
            error_code=expected.get("response", {}).get("error_code"),
        )

    @staticmethod
    def _matches_expected_wire_arguments(
        operation_id: str,
        expected_arguments: Mapping[str, Any],
        path: Mapping[str, Any],
        body: Mapping[str, Any] | None,
    ) -> bool:
        if operation_id == "get-contact":
            return path == {"contactId": expected_arguments.get("contact_id")} and body is None
        if operation_id == "get-opportunity":
            return path == {"id": expected_arguments.get("opportunity_id")} and body is None
        if operation_id == "create-note":
            return (
                path == {"contactId": expected_arguments.get("contact_id")}
                and body
                == {"body": expected_arguments.get("content_or_fingerprint")}
            )
        if operation_id == "get-note":
            return (
                path
                == {
                    "contactId": expected_arguments.get("contact_id"),
                    "id": expected_arguments.get("note_id"),
                }
                and body is None
            )
        if operation_id == "update-opportunity":
            return (
                path == {"id": expected_arguments.get("opportunity_id")}
                and body
                == {"pipelineStageId": expected_arguments.get("stage_id")}
            )
        return False

    def assert_exhausted(self) -> None:
        if self._calls:
            raise AssertionError(f"fixture calls were not consumed: {self._calls!r}")


@dataclass(frozen=True)
class BoundedAt1Result:
    """Immutable proof of the bounded execution and its independent counters."""

    disposition: str
    failure_code: str | None
    operations: tuple[str, ...]
    note_write_attempts: int
    note_writes_succeeded: int
    stage_write_attempts: int
    stage_writes_succeeded: int
    note_readback_verified: bool
    stage_readback_verified: bool
    further_transport_calls_authorized: bool
    stop_and_preserve_proof: bool


class BoundedAt1GhlExecutor:
    """Runs only the prescribed AT-1 sequence against a deterministic fixture seam."""

    def __init__(
        self,
        transport: GhlFixtureTransport,
        serializer: At1LiveTransportSerializer | None = None,
    ) -> None:
        self._transport = transport
        self._serializer = serializer or At1LiveTransportSerializer()
        self._operations: list[str] = []
        self._write_attempts = {"note": 0, "stage": 0}
        self._writes_succeeded = {"note": 0, "stage": 0}
        self._terminal = False
        self._note_readback_verified = False
        self._stage_readback_verified = False

    def execute(
        self, binding: BoundedAt1Input, context: At1ExecutionContext
    ) -> BoundedAt1Result:
        """Execute once in model order; every failure is terminal and non-retrying."""
        self._prevalidate_execution_context(context)
        contact = self._dispatch_read(
            "get-contact", {"location_id": binding.location_id, "contact_id": binding.contact_id}
        )
        if contact.status != "ok":
            return self._fail("CONTACT_NOT_FOUND")

        opportunity = self._dispatch_read(
            "get-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
            },
        )
        if opportunity.status != "ok":
            return self._fail("OPPORTUNITY_NOT_FOUND")
        if opportunity.record.get("stage_id") != binding.expected_initial_stage_id:
            return self._fail("INITIAL_STAGE_MISMATCH")

        created_note = self._dispatch_write(
            "create-note",
            {
                "location_id": binding.location_id,
                "contact_id": binding.contact_id,
                "content_or_fingerprint": binding.expected_note_content_or_fingerprint,
            },
            context,
        )
        if created_note.status != "ok":
            return self._fail("NOTE_WRITE_REJECTED")
        self._record_write_success("note")
        note_id = created_note.record.get("note_id")
        if not isinstance(note_id, str) or not note_id:
            return self._fail("NOTE_WRITE_RESPONSE_INVALID")

        note = self._dispatch_read(
            "get-note",
            {
                "location_id": binding.location_id,
                "contact_id": binding.contact_id,
                "note_id": note_id,
            },
        )
        if note.status != "ok" or (
            note.record.get("content_or_fingerprint")
            != binding.expected_note_content_or_fingerprint
        ):
            return self._fail("NOTE_READBACK_MISMATCH", preserve_proof=True)
        self._note_readback_verified = True

        updated_opportunity = self._dispatch_write(
            "update-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
                "stage_id": binding.authorized_final_stage_id,
            },
            context,
        )
        if updated_opportunity.status != "ok":
            return self._fail("STAGE_WRITE_REJECTED")
        self._record_write_success("stage")

        readback_opportunity = self._dispatch_read(
            "get-opportunity",
            {
                "location_id": binding.location_id,
                "opportunity_id": binding.opportunity_id,
            },
        )
        if (
            readback_opportunity.status != "ok"
            or readback_opportunity.record.get("stage_id")
            != binding.authorized_final_stage_id
        ):
            return self._fail("STAGE_READBACK_MISMATCH", preserve_proof=True)
        self._stage_readback_verified = True
        return self._result(disposition="completed")

    def _dispatch_read(
        self, operation_id: str, arguments: Mapping[str, str]
    ) -> FixtureResponse:
        if self._terminal:
            raise TerminalStateError("further transport calls are not authorized")
        self._operations.append(operation_id)
        envelope = self._serializer.build_execute_operation_call(
            operation_id, arguments
        )
        return self._transport.dispatch(envelope)

    def _dispatch_write(
        self,
        operation_id: str,
        arguments: Mapping[str, str],
        context: At1ExecutionContext,
    ) -> FixtureResponse:
        if self._terminal:
            raise TerminalStateError("further transport calls are not authorized")
        # Pre-transport hardening: validate the idempotency key before consuming
        # any write attempt budget. A missing key refuses locally with zero
        # transport calls and fail-closed semantics.
        envelope = self._serializer.build_execute_operation_call(
            operation_id, arguments, context
        )
        write_kind = "note" if operation_id == "create-note" else "stage"
        self._consume_write_attempt(write_kind)
        self._operations.append(operation_id)
        return self._transport.dispatch(envelope)

    @staticmethod
    def _prevalidate_execution_context(context: At1ExecutionContext) -> None:
        if not isinstance(context.note_idempotency_key, str) or not context.note_idempotency_key.strip():
            raise IdempotencyKeyError("note_idempotency_key must be a private non-empty string")
        if not isinstance(context.stage_idempotency_key, str) or not context.stage_idempotency_key.strip():
            raise IdempotencyKeyError("stage_idempotency_key must be a private non-empty string")
        if context.note_idempotency_key == context.stage_idempotency_key:
            raise IdempotencyKeyError("note and stage idempotency keys must be distinct")

    def _consume_write_attempt(self, write_kind: str) -> None:
        maximum = NOTE_WRITE_ATTEMPTS_MAX if write_kind == "note" else STAGE_WRITE_ATTEMPTS_MAX
        if self._write_attempts[write_kind] >= maximum:
            self._terminal = True
            raise WriteAttemptRefusedError(
                f"second {write_kind} write attempt refused before transport"
            )
        self._write_attempts[write_kind] += 1

    def _record_write_success(self, write_kind: str) -> None:
        maximum = (
            NOTE_WRITES_SUCCEEDED_MAX
            if write_kind == "note"
            else STAGE_WRITES_SUCCEEDED_MAX
        )
        if self._writes_succeeded[write_kind] >= maximum:
            self._terminal = True
            raise WriteAttemptRefusedError(
                f"second {write_kind} write success refused before transport"
            )
        self._writes_succeeded[write_kind] += 1

    def _fail(self, failure_code: str, *, preserve_proof: bool = False) -> BoundedAt1Result:
        self._terminal = True
        return self._result(
            disposition="failed",
            failure_code=failure_code,
            stop_and_preserve_proof=preserve_proof,
        )

    def _result(
        self,
        *,
        disposition: str,
        failure_code: str | None = None,
        stop_and_preserve_proof: bool = False,
    ) -> BoundedAt1Result:
        return BoundedAt1Result(
            disposition=disposition,
            failure_code=failure_code,
            operations=tuple(self._operations),
            note_write_attempts=self._write_attempts["note"],
            note_writes_succeeded=self._writes_succeeded["note"],
            stage_write_attempts=self._write_attempts["stage"],
            stage_writes_succeeded=self._writes_succeeded["stage"],
            note_readback_verified=self._note_readback_verified,
            stage_readback_verified=self._stage_readback_verified,
            further_transport_calls_authorized=not self._terminal,
            stop_and_preserve_proof=stop_and_preserve_proof,
        )
