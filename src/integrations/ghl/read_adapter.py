"""Deterministic, fixture-only mapping for the approved GHL read operations."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class OperationNotAllowedError(ValueError):
    """Raised when an operation is outside the explicit offline read allowlist."""


class RequestMappingError(ValueError):
    """Raised when request parameters do not match the discovered operation contract."""


_MUTATION_OPERATIONS = frozenset(
    {
        "create-note",
        "update-opportunity",
        "update-opportunity-status",
    }
)


@dataclass(frozen=True)
class _OperationSpec:
    path_fields: frozenset[str] = frozenset()
    query_fields: frozenset[str] = frozenset()
    body_fields: frozenset[str] = frozenset()
    required_body_fields: frozenset[str] = frozenset()


_OPERATION_SPECS = {
    "search-contacts-advanced": _OperationSpec(
        body_fields=frozenset({"pageLimit", "page", "query", "assignedTo", "projection"}),
        required_body_fields=frozenset({"pageLimit"}),
    ),
    "get-contact": _OperationSpec(path_fields=frozenset({"contactId"})),
    "search-opportunity": _OperationSpec(
        query_fields=frozenset(
            {
                "contactId",
                "pipelineId",
                "pipelineStageId",
                "q",
                "limit",
                "page",
                "status",
                "startAfter",
                "startAfterId",
            }
        )
    ),
    "search-opportunities-advanced": _OperationSpec(
        body_fields=frozenset(
            {"query", "limit", "page", "searchAfter", "additionalDetails"}
        )
    ),
    "get-pipelines": _OperationSpec(),
}


class OfflineGhlReadAdapter:
    """Maps and normalizes only approved GHL read operations without I/O."""

    allowed_operations = frozenset(_OPERATION_SPECS)

    def build_request(
        self,
        operation_id: str,
        *,
        path: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        body: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build the documented execute_operation envelope with validated params."""
        spec = self._operation_spec(operation_id)
        normalized_path = self._validate_parameters(path, spec.path_fields, "path")
        normalized_query = self._validate_parameters(query, spec.query_fields, "query")
        normalized_body = self._validate_parameters(body, spec.body_fields, "body")
        missing = spec.required_body_fields.difference(normalized_body)
        if missing:
            raise RequestMappingError(
                f"{operation_id} requires body fields: {', '.join(sorted(missing))}"
            )

        params: dict[str, dict[str, Any]] = {
            "path": normalized_path,
            "query": normalized_query,
        }
        if spec.body_fields:
            params["body"] = normalized_body

        return {
            "tool": "execute_operation",
            "arguments": {"operationId": operation_id, "params": params},
        }

    def normalize_response(
        self, operation_id: str, status_code: int, payload: Mapping[str, Any] | None
    ) -> dict[str, Any]:
        """Convert a synthetic operation payload into the stable local read result."""
        self._operation_spec(operation_id)
        payload = payload or {}
        if not isinstance(payload, Mapping):
            raise RequestMappingError("Synthetic response payload must be an object.")

        if status_code == 404:
            return self._error_result(operation_id, "NOT_FOUND", payload)
        if status_code < 200 or status_code >= 300:
            return self._error_result(
                operation_id, str(payload.get("code", f"HTTP_{status_code}")), payload
            )
        if payload.get("error"):
            return self._error_result(
                operation_id, str(payload.get("code", "GHL_TOOL_FAILURE")), payload
            )

        records = self._records_for(operation_id, payload)
        return {
            "operation_id": operation_id,
            "status": "ok",
            "records": records,
            "pagination": self._normalize_pagination(payload),
            "error": None,
        }

    def replay_fixture(self, fixture: Mapping[str, Any]) -> list[dict[str, Any]]:
        """Replay fixture cases locally; this method deliberately has no transport."""
        cases = fixture.get("cases")
        if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)):
            raise RequestMappingError("Fixture requires a cases array.")

        results: list[dict[str, Any]] = []
        for case in cases:
            if not isinstance(case, Mapping):
                raise RequestMappingError("Each fixture case must be an object.")
            operation_id = case.get("operation_id")
            response = case.get("response")
            if not isinstance(operation_id, str) or not isinstance(response, Mapping):
                raise RequestMappingError("Fixture case requires operation_id and response.")
            request = case.get("request", {})
            if not isinstance(request, Mapping):
                raise RequestMappingError("Fixture request must be an object.")
            envelope = self.build_request(
                operation_id,
                path=request.get("path"),
                query=request.get("query"),
                body=request.get("body"),
            )
            results.append(
                {
                    "case_id": case.get("case_id"),
                    "request": envelope,
                    "result": self.normalize_response(
                        operation_id,
                        int(response.get("status_code", 200)),
                        response.get("payload"),
                    ),
                }
            )
        return results

    def _operation_spec(self, operation_id: str) -> _OperationSpec:
        if operation_id in _MUTATION_OPERATIONS:
            raise OperationNotAllowedError(
                f"{operation_id} is a mutation and is explicitly denied."
            )
        try:
            return _OPERATION_SPECS[operation_id]
        except KeyError as error:
            raise OperationNotAllowedError(
                f"{operation_id} is not in the approved read-operation allowlist."
            ) from error

    @staticmethod
    def _validate_parameters(
        values: Mapping[str, Any] | None, allowed: frozenset[str], location: str
    ) -> dict[str, Any]:
        normalized = deepcopy(dict(values or {}))
        unknown = set(normalized).difference(allowed)
        if unknown:
            raise RequestMappingError(
                f"Unsupported {location} parameters: {', '.join(sorted(unknown))}"
            )
        return normalized

    def _records_for(
        self, operation_id: str, payload: Mapping[str, Any]
    ) -> list[dict[str, Any]]:
        if operation_id in {"search-contacts-advanced", "get-contact"}:
            return [self._normalize_contact(record) for record in self._as_records(payload, "contacts", "contact")]
        if operation_id in {"search-opportunity", "search-opportunities-advanced"}:
            return [
                self._normalize_opportunity(record)
                for record in self._as_records(payload, "opportunities", "opportunity")
            ]
        return [
            self._normalize_pipeline(record)
            for record in self._as_records(payload, "pipelines", "pipeline")
        ]

    @staticmethod
    def _as_records(
        payload: Mapping[str, Any], plural_key: str, singular_key: str
    ) -> list[Mapping[str, Any]]:
        value = payload.get(plural_key, payload.get(singular_key, []))
        if isinstance(value, Mapping):
            return [value]
        if not isinstance(value, list) or not all(isinstance(item, Mapping) for item in value):
            raise RequestMappingError(f"{plural_key} must be an object or array of objects.")
        return value

    @staticmethod
    def _normalize_contact(record: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "id": record.get("id", record.get("contactId")),
            "first_name": record.get("firstName", record.get("first_name")),
            "last_name": record.get("lastName", record.get("last_name")),
            "email": record.get("email"),
            "phone": record.get("phone"),
            "company_name": record.get("companyName", record.get("company_name")),
        }

    @staticmethod
    def _normalize_opportunity(record: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "id": record.get("id", record.get("opportunityId")),
            "contact_id": record.get("contactId", record.get("contact_id")),
            "pipeline_id": record.get("pipelineId", record.get("pipeline_id")),
            "pipeline_stage_id": record.get(
                "pipelineStageId", record.get("pipeline_stage_id")
            ),
            "name": record.get("name"),
            "status": record.get("status"),
            "monetary_value": record.get("monetaryValue", record.get("monetary_value")),
        }

    def _normalize_pipeline(self, record: Mapping[str, Any]) -> dict[str, Any]:
        stages = record.get("stages", [])
        if not isinstance(stages, list) or not all(isinstance(stage, Mapping) for stage in stages):
            raise RequestMappingError("Pipeline stages must be an array of objects.")
        return {
            "id": record.get("id", record.get("pipelineId")),
            "name": record.get("name"),
            "stages": [
                {
                    "id": stage.get("id", stage.get("pipelineStageId")),
                    "name": stage.get("name"),
                    "position": stage.get("position"),
                }
                for stage in stages
            ],
        }

    @staticmethod
    def _normalize_pagination(payload: Mapping[str, Any]) -> dict[str, Any]:
        source = payload.get("meta", payload.get("pagination", {}))
        if not isinstance(source, Mapping):
            raise RequestMappingError("Response pagination metadata must be an object.")
        return {
            "page": source.get("page"),
            "limit": source.get("pageLimit", source.get("limit")),
            "total": source.get("total", source.get("totalCount")),
            "next_cursor": source.get(
                "nextCursor", source.get("nextPage", source.get("startAfter"))
            ),
            "has_more": source.get("hasMore", source.get("has_more")),
        }

    @staticmethod
    def _error_result(
        operation_id: str, code: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        return {
            "operation_id": operation_id,
            "status": "not_found" if code == "NOT_FOUND" else "error",
            "records": [],
            "pagination": None,
            "error": {
                "code": code,
                "message": str(payload.get("message", "GHL read operation failed.")),
            },
        }
