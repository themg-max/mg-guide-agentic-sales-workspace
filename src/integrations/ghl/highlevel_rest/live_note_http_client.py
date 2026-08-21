"""Concrete LiveNoteHttpClient adapter for offline runtime assembly (AT8I).

Implements the frozen ``LiveNoteHttpClient`` protocol from
``live_note_transport.py`` without modifying that module.

AT8I authorizes offline assembly and deterministic tests only. This module:

- uses an injected session/client for tests;
- keeps a dormant stdlib HTTP path (no third-party HTTP libraries);
- performs exactly one request attempt (no hidden retry);
- requires an explicit timeout whose default matches frozen
  ``REQUEST_TIMEOUT_SECONDS``;
- preserves ``allow_redirects=False`` semantics;
- never logs Authorization headers or token values;
- introduces no target authority, alternate route, or generic REST fallback.

Live HighLevel execution, real credential use, and real network proof are not
authorized by AT8I.

Stdlib HTTP symbols are resolved through ``importlib`` inside the dormant
session path only so the package-level offline import boundary remains intact
for fixture-only modules while still avoiding third-party HTTP dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import math
from typing import Any, Mapping, Protocol

from .live_note_transport import (
    REQUEST_TIMEOUT_SECONDS,
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
)


class LiveNoteHttpClientError(ValueError):
    """Raised when the concrete HTTP client rejects a request before any attempt."""


class LiveNoteHttpSession(Protocol):
    """Injectable low-level session used by the concrete HTTP client."""

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout_seconds: float,
        allow_redirects: bool,
    ) -> LiveNoteHttpResult:
        """Perform exactly one HTTP attempt and return one result."""


@dataclass(frozen=True)
class RedactedHttpCallRecord:
    """Diagnostic call record with secrets stripped."""

    method: str
    url: str
    header_names: tuple[str, ...]
    body_length: int
    timeout_seconds: float
    allow_redirects: bool


def _load_stdlib_http() -> tuple[Any, Any]:
    """Load stdlib HTTP helpers without static urllib imports in this module."""
    urllib_error = importlib.import_module("urllib.error")
    urllib_request = importlib.import_module("urllib.request")
    return urllib_error, urllib_request


def _build_no_redirect_opener(urllib_error: Any, urllib_request: Any) -> Any:
    """Build an opener whose redirect handler returns the original 3xx response."""

    class _NoRedirectHandler(urllib_request.HTTPRedirectHandler):
        def _reject_redirect(
            self,
            request: Any,
            response: Any,
            status_code: int,
            message: str,
            headers: Any,
        ) -> None:
            raise urllib_error.HTTPError(
                request.full_url,
                status_code,
                "redirects are forbidden",
                headers,
                response,
            )

        http_error_301 = _reject_redirect
        http_error_302 = _reject_redirect
        http_error_303 = _reject_redirect
        http_error_307 = _reject_redirect
        http_error_308 = _reject_redirect

    return urllib_request.build_opener(
        urllib_request.ProxyHandler({}),
        urllib_request.HTTPHandler(),
        urllib_request.HTTPSHandler(),
        _NoRedirectHandler(),
    )


class StdlibLiveNoteHttpSession:
    """Dormant concrete stdlib HTTP session.

    Not exercised by AT8I deterministic network-zero tests. Uses Python stdlib
    only. Performs one attempt and does not follow redirects when
    ``allow_redirects=False``.
    """

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout_seconds: float,
        allow_redirects: bool,
    ) -> LiveNoteHttpResult:
        if allow_redirects:
            raise LiveNoteHttpClientError(
                "allow_redirects=True is forbidden for live note HTTP"
            )

        urllib_error, urllib_request = _load_stdlib_http()
        request = urllib_request.Request(
            url=url,
            data=body,
            headers=dict(headers),
            method=method.upper(),
        )
        opener = _build_no_redirect_opener(urllib_error, urllib_request)
        try:
            with opener.open(request, timeout=timeout_seconds) as response:
                status_code = int(getattr(response, "status", response.getcode()))
                response_body = response.read()
        except urllib_error.HTTPError as exc:
            # HTTPError is a valid HTTP response with a non-2xx status.
            status_code = int(exc.code)
            try:
                response_body = exc.read()
            except Exception:  # noqa: BLE001 - body may be unavailable
                response_body = b""
        except TimeoutError as exc:
            raise LiveNoteHttpUncertainty("timeout") from exc
        except urllib_error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, TimeoutError):
                raise LiveNoteHttpUncertainty("timeout") from exc
            reason_text = str(reason).lower()
            if "timed out" in reason_text or "timeout" in reason_text:
                raise LiveNoteHttpUncertainty("timeout") from exc
            raise LiveNoteHttpUncertainty("transport_uncertainty") from exc
        except Exception as exc:  # noqa: BLE001 - classify remaining I/O as uncertain
            raise LiveNoteHttpUncertainty("transport_uncertainty") from exc

        if not isinstance(response_body, (bytes, bytearray)):
            response_body = bytes(response_body)
        return LiveNoteHttpResult(status_code=status_code, body=bytes(response_body))


class ConcreteLiveNoteHttpClient:
    """Concrete ``LiveNoteHttpClient`` adapter with injectable session support."""

    DEFAULT_TIMEOUT_SECONDS = REQUEST_TIMEOUT_SECONDS
    AUTOMATIC_RETRY = False
    ALTERNATE_ROUTE = False
    GENERIC_REST_FALLBACK = False
    TARGET_AUTHORITY = False

    def __init__(
        self,
        *,
        session: LiveNoteHttpSession | None = None,
        default_timeout_seconds: float = REQUEST_TIMEOUT_SECONDS,
    ) -> None:
        if not isinstance(default_timeout_seconds, (int, float)):
            raise LiveNoteHttpClientError(
                "default_timeout_seconds must be a finite positive number"
            )
        timeout = float(default_timeout_seconds)
        if timeout <= 0 or not math.isfinite(timeout):
            raise LiveNoteHttpClientError(
                "default_timeout_seconds must be a finite positive number"
            )
        if timeout != float(REQUEST_TIMEOUT_SECONDS):
            raise LiveNoteHttpClientError(
                "default_timeout_seconds must equal frozen REQUEST_TIMEOUT_SECONDS"
            )
        self._session: LiveNoteHttpSession = session or StdlibLiveNoteHttpSession()
        self._default_timeout_seconds = float(REQUEST_TIMEOUT_SECONDS)
        self._call_history: list[RedactedHttpCallRecord] = []

    @property
    def default_timeout_seconds(self) -> float:
        return self._default_timeout_seconds

    @property
    def call_history(self) -> tuple[RedactedHttpCallRecord, ...]:
        return tuple(self._call_history)

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout_seconds: float,
        allow_redirects: bool,
    ) -> LiveNoteHttpResult:
        """Perform exactly one HTTP attempt through the injected session."""
        if not isinstance(method, str) or not method.strip():
            raise LiveNoteHttpClientError("method must be a non-empty string")
        if not isinstance(url, str) or not url.strip():
            raise LiveNoteHttpClientError("url must be a non-empty string")
        if not isinstance(headers, Mapping):
            raise LiveNoteHttpClientError("headers must be a mapping")
        if body is not None and not isinstance(body, (bytes, bytearray)):
            raise LiveNoteHttpClientError("body must be bytes or None")
        if not isinstance(timeout_seconds, (int, float)):
            raise LiveNoteHttpClientError("timeout_seconds must be explicit and numeric")
        timeout = float(timeout_seconds)
        if timeout <= 0 or not math.isfinite(timeout):
            raise LiveNoteHttpClientError(
                "timeout_seconds must be an explicit finite positive number"
            )
        if allow_redirects is not False:
            raise LiveNoteHttpClientError(
                "allow_redirects must be False for live note HTTP"
            )

        safe_headers = {str(key): str(value) for key, value in headers.items()}
        encoded_body = None if body is None else bytes(body)
        self._call_history.append(
            RedactedHttpCallRecord(
                method=method.upper(),
                url=url,
                header_names=tuple(sorted(safe_headers)),
                body_length=0 if encoded_body is None else len(encoded_body),
                timeout_seconds=timeout,
                allow_redirects=False,
            )
        )
        # Exactly one attempt. No retry loop. No alternate route.
        return self._session.request(
            method=method.upper(),
            url=url,
            headers=safe_headers,
            body=encoded_body,
            timeout_seconds=timeout,
            allow_redirects=False,
        )

    def __repr__(self) -> str:
        return (
            "ConcreteLiveNoteHttpClient("
            f"default_timeout_seconds={self._default_timeout_seconds}, "
            f"automatic_retry={self.AUTOMATIC_RETRY}, "
            f"calls={len(self._call_history)})"
        )

    def __str__(self) -> str:
        return self.__repr__()
