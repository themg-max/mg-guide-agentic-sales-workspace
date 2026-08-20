"""Ordered synthetic fixture transport for the bounded NOTE_PATH routes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class FakeTransportError(ValueError):
    """Raised when a fixture or fixture call exceeds the offline boundary."""


@dataclass(frozen=True)
class FakeResponse:
    """A pre-authored fixture response."""

    status: str
    payload: Mapping[str, Any]


class DeterministicFakeTransport:
    """Consume one ordered synthetic fixture case without any I/O capability."""

    _POLICY = {
        "source": "synthetic_only",
        "network_calls": 0,
        "external_effects": 0,
    }
    _ROOT_FIELDS = frozenset({*_POLICY, "cases"})
    _CALL_FIELDS = frozenset({"method", "path", "response"})

    def __init__(self, fixture: Mapping[str, Any], case_id: str) -> None:
        self._validate_fixture(fixture)
        cases = fixture["cases"]
        case = cases.get(case_id)
        if not isinstance(case, Mapping) or set(case) != {"calls"}:
            raise FakeTransportError(f"fixture case {case_id!r} must contain only calls")
        calls = case["calls"]
        if not isinstance(calls, Sequence) or isinstance(calls, (str, bytes)):
            raise FakeTransportError(f"fixture case {case_id!r} calls must be an array")
        self._calls = [dict(call) for call in calls]
        if not all(isinstance(call, Mapping) for call in calls):
            raise FakeTransportError("fixture calls must be objects")
        self.calls: list[tuple[str, str, Mapping[str, Any] | None]] = []

    @classmethod
    def _validate_fixture(cls, fixture: Mapping[str, Any]) -> None:
        if not isinstance(fixture, Mapping) or set(fixture) != cls._ROOT_FIELDS:
            raise FakeTransportError("fixture root fields do not match offline policy")
        for name, expected in cls._POLICY.items():
            if fixture[name] != expected:
                raise FakeTransportError(f"fixture policy requires {name}={expected!r}")
        if not isinstance(fixture["cases"], Mapping):
            raise FakeTransportError("fixture cases must be an object")

    def dispatch(
        self, method: str, path: str, body: Mapping[str, Any] | None = None
    ) -> FakeResponse:
        """Return the next exact fixture response for an allowed route."""
        if not self._calls:
            raise FakeTransportError("fixture did not authorize another route")
        expected = self._calls.pop(0)
        if set(expected) != self._CALL_FIELDS:
            raise FakeTransportError("fixture call fields must be exact")
        if expected["method"] != method or expected["path"] != path:
            raise FakeTransportError(
                f"fixture expected {expected['method']} {expected['path']}, "
                f"got {method} {path}"
            )
        if method == "POST":
            if not isinstance(body, Mapping) or set(body) != {"body"}:
                raise FakeTransportError("NOTE_PATH POST body must contain only body")
        elif body is not None:
            raise FakeTransportError("NOTE_PATH GET routes do not accept a body")
        response = expected["response"]
        if not isinstance(response, Mapping) or set(response) != {"status", "payload"}:
            raise FakeTransportError("fixture response fields must be exact")
        if not isinstance(response["status"], str) or not isinstance(
            response["payload"], Mapping
        ):
            raise FakeTransportError("fixture response is malformed")
        self.calls.append((method, path, dict(body) if body is not None else None))
        return FakeResponse(response["status"], dict(response["payload"]))

    def assert_exhausted(self) -> None:
        """Ensure the adapter made neither fewer nor more fixture calls."""
        if self._calls:
            raise FakeTransportError(f"{len(self._calls)} fixture calls were not consumed")
