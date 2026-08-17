"""Durable, bounded live MCP transport serializer for the AT-1 write surface.

This module is intentionally not a general GHL SDK. It only serializes the six
operations used by NW-008 AT-1 bounded execution, and it hardens every write
dispatch with a frozen, private idempotency key before the request reaches any
transport seam.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


AT1_WRITE_OPERATIONS = frozenset({"create-note", "update-opportunity"})
AT1_READ_OPERATIONS = frozenset({"get-contact", "get-opportunity", "get-note"})
AT1_ALLOWED_OPERATIONS = AT1_WRITE_OPERATIONS | AT1_READ_OPERATIONS


class IdempotencyKeyError(ValueError):
    """Raised before transport when a required idempotency key is missing or invalid."""


@dataclass(frozen=True)
class At1ExecutionContext:
    """Private execution context supplying distinct idempotency keys for each write."""

    note_idempotency_key: str
    stage_idempotency_key: str

    def __post_init__(self) -> None:
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.strip():
                raise IdempotencyKeyError(
                    f"{field_name} must be a private non-empty string"
                )
        if self.note_idempotency_key == self.stage_idempotency_key:
            raise IdempotencyKeyError(
                "note and stage idempotency keys must be distinct"
            )


class At1LiveTransportSerializer:
    """Builds execute_operation envelopes for the bounded AT-1 operation surface.

    Reads are serialized without idempotency keys. Writes are refused locally
    unless a non-empty idempotency key is supplied, and the key is frozen into
    the top level of the envelope arguments so it travels with the MCP request.
    """

    allowed_operations = AT1_ALLOWED_OPERATIONS

    def build_execute_operation_arguments(
        self,
        operation_id: str,
        arguments: Mapping[str, Any],
        context: At1ExecutionContext | None = None,
    ) -> dict[str, Any]:
        """Return exact execute_operation arguments for the bounded AT-1 surface.

        Raises:
            IdempotencyKeyError: if a write operation lacks a valid idempotency key.
            ValueError: if ``operation_id`` is outside the bounded AT-1 surface.
        """
        if operation_id not in self.allowed_operations:
            raise ValueError(
                f"{operation_id} is outside the bounded AT-1 operation surface"
            )

        execute_operation_arguments: dict[str, Any] = {
            "operationId": operation_id,
            "params": {"path": self._path_for(operation_id, arguments)},
        }
        body = self._body_for(operation_id, arguments)
        if body is not None:
            execute_operation_arguments["params"]["body"] = body

        if operation_id in AT1_WRITE_OPERATIONS:
            if context is None:
                raise IdempotencyKeyError(
                    f"{operation_id} requires an execution context with an idempotency key"
                )
            key = (
                context.note_idempotency_key
                if operation_id == "create-note"
                else context.stage_idempotency_key
            )
            if not isinstance(key, str) or not key.strip():
                raise IdempotencyKeyError(
                    f"{operation_id} requires a private non-empty idempotencyKey"
                )
            execute_operation_arguments["idempotencyKey"] = key

        return execute_operation_arguments

    def build_execute_operation_call(
        self,
        operation_id: str,
        arguments: Mapping[str, Any],
        context: At1ExecutionContext | None = None,
    ) -> dict[str, Any]:
        """Return the frozen MCP call seam for execute_operation."""
        return {
            "name": "execute_operation",
            "arguments": self.build_execute_operation_arguments(
                operation_id, arguments, context
            ),
        }

    def build_execute_operation_envelope(
        self,
        operation_id: str,
        arguments: Mapping[str, Any],
        context: At1ExecutionContext | None = None,
    ) -> dict[str, Any]:
        """Backwards-compatible alias for call construction."""
        return self.build_execute_operation_call(operation_id, arguments, context)

    @staticmethod
    def _require_non_empty_string(
        arguments: Mapping[str, Any], field_name: str, operation_id: str
    ) -> str:
        value = arguments.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{operation_id} requires {field_name} as a non-empty string"
            )
        return value

    def _path_for(
        self, operation_id: str, arguments: Mapping[str, Any]
    ) -> dict[str, str]:
        if operation_id == "get-contact":
            return {
                "contactId": self._require_non_empty_string(
                    arguments, "contact_id", operation_id
                )
            }
        if operation_id == "get-opportunity":
            return {"id": self._require_non_empty_string(arguments, "opportunity_id", operation_id)}
        if operation_id == "create-note":
            return {
                "contactId": self._require_non_empty_string(
                    arguments, "contact_id", operation_id
                )
            }
        if operation_id == "get-note":
            return {
                "contactId": self._require_non_empty_string(
                    arguments, "contact_id", operation_id
                ),
                "id": self._require_non_empty_string(arguments, "note_id", operation_id),
            }
        if operation_id == "update-opportunity":
            return {"id": self._require_non_empty_string(arguments, "opportunity_id", operation_id)}
        raise ValueError(f"{operation_id} is outside the bounded AT-1 operation surface")

    def _body_for(
        self, operation_id: str, arguments: Mapping[str, Any]
    ) -> dict[str, str] | None:
        if operation_id == "create-note":
            return {
                "body": self._require_non_empty_string(
                    arguments, "content_or_fingerprint", operation_id
                )
            }
        if operation_id == "update-opportunity":
            return {
                "pipelineStageId": self._require_non_empty_string(
                    arguments, "stage_id", operation_id
                )
            }
        return None
