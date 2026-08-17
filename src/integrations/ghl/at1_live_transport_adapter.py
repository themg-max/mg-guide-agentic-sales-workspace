"""Bounded offline live-transport adapter with durable evidence capture."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any, Protocol
from uuid import uuid4

from .at1_execution_store import (
    At1ExecutionStore,
    DuplicateBusinessOrdinalError,
)
from .bounded_at1_executor import FixtureResponse


_ALLOWED_OPERATIONS = (
    "get-contact",
    "get-opportunity",
    "create-note",
    "get-note",
    "update-opportunity",
)
_EXACT_OPERATION_ORDER = (
    "get-contact",
    "get-opportunity",
    "create-note",
    "get-note",
    "update-opportunity",
    "get-opportunity",
)
_CONTROL_PLANE_CALLS = frozenset({"initialize", "probe"})


class PostGrantControlPlaneCallRefusedError(RuntimeError):
    """Raised when initialize/probe is attempted after grant activation."""


class TransportEnvelopeError(ValueError):
    """Raised when the call differs from the serializer's bounded wire contract."""


class EstablishedSession(Protocol):
    """Injected established-session seam. No network client is created here."""

    def execute_operation(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        """Dispatch one bounded operation and return one synthetic response envelope."""


@dataclass(frozen=True)
class _ParsedOperation:
    success: bool
    payload: dict[str, Any]
    failure_code: str | None = None


class At1LiveTransportAdapter:
    """Durable adapter that captures exact request/response evidence before parsing."""

    def __init__(
        self,
        *,
        session: EstablishedSession,
        store: At1ExecutionStore,
        grant_run_id: str,
        owner_id: str,
        grant_active: bool = True,
    ) -> None:
        self._session = session
        self.store = store
        self.grant_run_id = grant_run_id
        self.owner_id = owner_id
        self._grant_active = grant_active
        self.store.acquire_claim(grant_run_id, owner_id)
        self.store.assert_claim_owner(grant_run_id, owner_id)

    def activate_grant(self) -> None:
        self._grant_active = True

    def record_protocol_call(self, call_name: str, payload: Mapping[str, Any]) -> None:
        if call_name not in _CONTROL_PLANE_CALLS:
            raise PostGrantControlPlaneCallRefusedError(
                f"{call_name!r} is not an allowed protocol call"
            )
        if self._grant_active:
            raise PostGrantControlPlaneCallRefusedError(
                f"{call_name!r} is refused after grant activation"
            )
        self.store.append_protocol_call(self.grant_run_id, call_name, payload)

    def dispatch(self, envelope: Mapping[str, Any]) -> FixtureResponse:
        operation_id = self._validate_and_extract_operation(envelope)
        ordinal = self.store.next_operation_ordinal(self.grant_run_id)
        if ordinal > len(_EXACT_OPERATION_ORDER):
            raise DuplicateBusinessOrdinalError("all six business ordinals are consumed")
        expected_operation = _EXACT_OPERATION_ORDER[ordinal - 1]
        if operation_id != expected_operation:
            raise DuplicateBusinessOrdinalError(
                f"ordinal {ordinal} expected {expected_operation!r}, got {operation_id!r}"
            )
        request_id = f"{self.grant_run_id}:{ordinal}:{uuid4().hex}"
        self.store.record_attempt(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
            operation_id=operation_id,
            request_id=request_id,
            request_envelope=envelope,
        )
        self.store.mark_dispatched(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
        )
        request = {
            "id": request_id,
            "name": envelope["name"],
            "arguments": envelope["arguments"],
        }
        response = self._session.execute_operation(request)
        self.store.capture_response(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
            response_envelope=response,
        )
        parsed = self._parse_response(
            request_id=request_id,
            operation_id=operation_id,
            response=response,
        )
        if not parsed.success:
            self.store.record_parse_outcome(
                grant_run_id=self.grant_run_id,
                operation_ordinal=ordinal,
                success=False,
            )
            self.store.record_semantic_outcome(
                grant_run_id=self.grant_run_id,
                operation_ordinal=ordinal,
                success=False,
            )
            self.store.mark_terminal(
                grant_run_id=self.grant_run_id,
                operation_ordinal=ordinal,
                failure_code=str(parsed.failure_code),
                business_effect_truth="NO",
            )
            return FixtureResponse(status="error", error_code=parsed.failure_code)
        self.store.record_parse_outcome(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
            success=True,
        )
        return FixtureResponse(status="ok", record=parsed.payload)

    def record_semantic_outcome(self, success: bool) -> None:
        ordinal = self.store.latest_operation_ordinal(self.grant_run_id)
        if ordinal is None:
            return
        self.store.record_semantic_outcome(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
            success=success,
        )

    def record_terminal_failure(
        self, failure_code: str, *, business_effect_truth: str = "NO"
    ) -> None:
        ordinal = self.store.latest_operation_ordinal(self.grant_run_id)
        if ordinal is None:
            return
        self.store.mark_terminal(
            grant_run_id=self.grant_run_id,
            operation_ordinal=ordinal,
            failure_code=failure_code,
            business_effect_truth=business_effect_truth,
        )

    def public_projection(self) -> dict[str, Any]:
        return self.store.compute_public_projection(self.grant_run_id)

    @staticmethod
    def _require_string(mapping: Mapping[str, Any], field_name: str) -> str:
        value = mapping.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise TransportEnvelopeError(f"{field_name} must be a non-empty string")
        return value

    def _validate_and_extract_operation(self, envelope: Mapping[str, Any]) -> str:
        if set(envelope.keys()) != {"name", "arguments"}:
            raise TransportEnvelopeError("envelope must contain exact keys: name, arguments")
        if envelope["name"] != "execute_operation":
            raise TransportEnvelopeError("only execute_operation is allowed")
        arguments = envelope["arguments"]
        if not isinstance(arguments, Mapping):
            raise TransportEnvelopeError("arguments must be an object")
        operation_id = self._require_string(arguments, "operationId")
        if operation_id not in _ALLOWED_OPERATIONS:
            raise TransportEnvelopeError(f"{operation_id!r} is outside the bounded surface")
        params = arguments.get("params")
        if not isinstance(params, Mapping):
            raise TransportEnvelopeError("params must be an object")
        path = params.get("path")
        if not isinstance(path, Mapping):
            raise TransportEnvelopeError("params.path must be an object")
        is_write = operation_id in {"create-note", "update-opportunity"}

        if is_write and set(arguments.keys()) != {"operationId", "params", "idempotencyKey"}:
            raise TransportEnvelopeError("write arguments must be exact and include idempotencyKey")
        if not is_write and set(arguments.keys()) != {"operationId", "params"}:
            raise TransportEnvelopeError("read arguments must be exact")
        if is_write and not isinstance(arguments.get("idempotencyKey"), str):
            raise TransportEnvelopeError("idempotencyKey must be a non-empty string")
        if is_write and not arguments.get("idempotencyKey", "").strip():
            raise TransportEnvelopeError("idempotencyKey must be a non-empty string")

        if operation_id == "get-contact":
            if set(params.keys()) != {"path"} or set(path.keys()) != {"contactId"}:
                raise TransportEnvelopeError("get-contact wire shape mismatch")
            self._require_string(path, "contactId")
        elif operation_id == "get-opportunity":
            if set(params.keys()) != {"path"} or set(path.keys()) != {"id"}:
                raise TransportEnvelopeError("get-opportunity wire shape mismatch")
            self._require_string(path, "id")
        elif operation_id == "create-note":
            body = params.get("body")
            if (
                set(params.keys()) != {"path", "body"}
                or set(path.keys()) != {"contactId"}
                or not isinstance(body, Mapping)
                or set(body.keys()) != {"body"}
            ):
                raise TransportEnvelopeError("create-note wire shape mismatch")
            self._require_string(path, "contactId")
            self._require_string(body, "body")
        elif operation_id == "get-note":
            if set(params.keys()) != {"path"} or set(path.keys()) != {"contactId", "id"}:
                raise TransportEnvelopeError("get-note wire shape mismatch")
            self._require_string(path, "contactId")
            self._require_string(path, "id")
        elif operation_id == "update-opportunity":
            body = params.get("body")
            if (
                set(params.keys()) != {"path", "body"}
                or set(path.keys()) != {"id"}
                or not isinstance(body, Mapping)
                or set(body.keys()) != {"pipelineStageId"}
            ):
                raise TransportEnvelopeError("update-opportunity wire shape mismatch")
            self._require_string(path, "id")
            self._require_string(body, "pipelineStageId")
        return operation_id

    def _parse_response(
        self,
        *,
        request_id: str,
        operation_id: str,
        response: Mapping[str, Any],
    ) -> _ParsedOperation:
        if response.get("id") != request_id:
            return _ParsedOperation(False, {}, "JSONRPC_REQUEST_ID_MISMATCH")
        if "error" in response and response.get("error") is not None:
            return _ParsedOperation(False, {}, "JSONRPC_ERROR_PRESENT")
        result = response.get("result")
        if not isinstance(result, Mapping):
            return _ParsedOperation(False, {}, "JSONRPC_RESULT_MISSING")
        if result.get("isError") is not False:
            return _ParsedOperation(False, {}, "MCP_IS_ERROR_TRUE")
        content = result.get("content")
        if not isinstance(content, list) or not content:
            return _ParsedOperation(False, {}, "MCP_CONTENT_INVALID")
        nested = content[0]
        if not isinstance(nested, Mapping):
            return _ParsedOperation(False, {}, "MCP_CONTENT_INVALID")
        if nested.get("operationId") != operation_id:
            return _ParsedOperation(False, {}, "MCP_OPERATION_ID_MISMATCH")
        if nested.get("success") is not True:
            return _ParsedOperation(False, {}, "MCP_OPERATION_NOT_SUCCESS")
        status = nested.get("status")
        if not isinstance(status, int) or not (200 <= status < 300):
            return _ParsedOperation(False, {}, "MCP_OPERATION_STATUS_NOT_SUCCESS")
        payload = nested.get("payload")
        if not isinstance(payload, Mapping):
            return _ParsedOperation(False, {}, "MCP_OPERATION_PAYLOAD_INVALID")
        return _ParsedOperation(True, dict(payload), None)
