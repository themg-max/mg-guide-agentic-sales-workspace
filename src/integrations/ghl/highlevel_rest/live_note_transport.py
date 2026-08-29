"""Bounded HighLevel v3 transport for exact contact and frozen NOTE routes.

This module is injectable into NotePathAdapter through the existing
``dispatch(method, path, body=None)`` seam. It does not alter NOTE_PATH,
At1ExecutionStore, or the PR107 trust boundary.

AT8H authorizes implementation and offline deterministic tests only. It does
not authorize live transport execution, live note write, live read, live CRM
mutation, real credential use, or Secret Manager access. HTTP is performed
only through an injected client. This module does not create a network
client, discover environment secrets, or import socket/HTTP libraries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping, Protocol


BASE_URL = "https://services.leadconnectorhq.com"
API_VERSION = "v3"
VERSION_HEADER = "v3"

POST_ATTEMPTS_MAX = 1
POST_SUCCESSES_MAX = 1
READBACK_GET_ATTEMPTS_MAX = 1
TOTAL_NETWORK_CALLS_MAX = 2
TOTAL_MUTATION_CALLS_MAX = 1
CONTACT_GET_ATTEMPTS_MAX = 1
REQUEST_TIMEOUT_SECONDS = 10.0

AUTOMATIC_RETRY = False
FALLBACK = False
SECOND_POST = False
SEARCH = False
LIST = False
PAGINATION = False
DELETE = False
UPDATE_NOTE = False
ALTERNATE_TARGET = False
ALTERNATE_ROUTE = False
GENERIC_EXECUTE = False
RAW_REST_FALLBACK = False
COMPENSATING_MUTATION = False
AUTOMATIC_CLEANUP = False

LIVE_EXECUTION_AUTHORIZED = False
LIVE_NETWORK_CALLS_AUTHORIZED = False
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED = False
AMBIGUITY_TRUTH = "UNKNOWN"

_ALLOWED_METHODS = frozenset({"POST", "GET"})
_NOTE_RESPONSE_FIELDS = ("id", "body", "contactId")
_REDACTED = "<redacted>"
_REDACTED_CONTACT_GET_PATH = "/contacts/<redacted>"
_REDACTED_POST_PATH = "/contacts/<redacted>/notes"
_REDACTED_GET_PATH = "/contacts/<redacted>/notes/<redacted>"

# Response-header aliases only. Authorization and unknown headers stay ignored
# for public projection and never enter diagnostic evidence as values.
_REQUEST_ID_HEADER_ALIASES = frozenset(
    {
        "x-request-id",
        "request-id",
        "x-amzn-requestid",
        "x-amz-request-id",
        "x-amzn-trace-id",
    }
)
_CORRELATION_ID_HEADER_ALIASES = frozenset(
    {
        "x-correlation-id",
        "correlation-id",
        "x-correlationid",
        "cf-ray",
        "traceparent",
        "x-trace-id",
        "trace-id",
    }
)
_ERROR_CODE_FIELD_ALIASES = (
    "errorCode",
    "error_code",
    "code",
    "statusCode",
    "status_code",
    "type",
)
_ERROR_MESSAGE_FIELD_ALIASES = (
    "message",
    "error",
    "msg",
    "detail",
    "title",
    "description",
)
_FORBIDDEN_DIAGNOSTIC_HEADER_NAMES = frozenset(
    {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
    }
)


class LiveNoteTransportError(ValueError):
    """Raised when a dispatch is rejected before any HTTP attempt."""


class LiveNoteHttpUncertainty(Exception):
    """Raised by an injected HTTP client when dispatch effect cannot be proven."""


@dataclass(frozen=True)
class LiveNoteResponse:
    """NOTE_PATH-compatible response. Extra provider fields are not published."""

    status: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class LiveNoteHttpResult:
    """Raw HTTP result from an injected HTTP client. Not a published provider envelope.

    ``headers`` may carry definitive provider response headers privately. They
    are never projected wholesale into public proof artifacts.
    """

    status_code: int
    body: bytes
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PrivateProviderErrorEvidence:
    """Private diagnostic surface for one definitive non-2xx provider response."""

    PROVIDER_HTTP_STATUS: int
    CONTENT_TYPE: str | None
    CONTENT_TYPE_CLASS: str
    RESPONSE_BODY_LENGTH: int
    RESPONSE_BODY_SHA256: str
    PROVIDER_ERROR_ENVELOPE_PARSEABLE: bool
    PROVIDER_ERROR_CODE: str | None
    PROVIDER_ERROR_MESSAGE: str | None
    PROVIDER_REQUEST_ID: str | None
    PROVIDER_CORRELATION_ID: str | None
    PROVIDER_ERROR_CLASS: str
    PROVIDER_ERROR_CAUSE: str


@dataclass(frozen=True)
class PublicProviderErrorProjection:
    """Public-safe presence/class projection for definitive non-2xx responses."""

    PROVIDER_HTTP_STATUS: int
    PROVIDER_CONTENT_TYPE_CLASS: str
    PROVIDER_ERROR_ENVELOPE_PRESENT: str
    PROVIDER_ERROR_CODE_PRESENT: str
    PROVIDER_ERROR_MESSAGE_PRESENT: str
    PROVIDER_REQUEST_ID_PRESENT: str
    PROVIDER_CORRELATION_ID_PRESENT: str
    PROVIDER_ERROR_CLASS: str
    PROVIDER_ERROR_CAUSE: str
    RAW_PROVIDER_RESPONSE_PUBLISHED: str = "NO"
    PROVIDER_ERROR_MESSAGE_PUBLISHED: str = "NO"
    PROVIDER_REQUEST_ID_PUBLISHED: str = "NO"
    PROVIDER_CORRELATION_ID_PUBLISHED: str = "NO"
    AUTHORIZATION_HEADER_PUBLISHED: str = "NO"
    TOKEN_OR_PIT_PUBLISHED: str = "NO"

    def as_public_dict(self) -> dict[str, Any]:
        return {
            "PROVIDER_HTTP_STATUS": self.PROVIDER_HTTP_STATUS,
            "PROVIDER_CONTENT_TYPE_CLASS": self.PROVIDER_CONTENT_TYPE_CLASS,
            "PROVIDER_ERROR_ENVELOPE_PRESENT": self.PROVIDER_ERROR_ENVELOPE_PRESENT,
            "PROVIDER_ERROR_CODE_PRESENT": self.PROVIDER_ERROR_CODE_PRESENT,
            "PROVIDER_ERROR_MESSAGE_PRESENT": self.PROVIDER_ERROR_MESSAGE_PRESENT,
            "PROVIDER_REQUEST_ID_PRESENT": self.PROVIDER_REQUEST_ID_PRESENT,
            "PROVIDER_CORRELATION_ID_PRESENT": self.PROVIDER_CORRELATION_ID_PRESENT,
            "PROVIDER_ERROR_CLASS": self.PROVIDER_ERROR_CLASS,
            "PROVIDER_ERROR_CAUSE": self.PROVIDER_ERROR_CAUSE,
            "RAW_PROVIDER_RESPONSE_PUBLISHED": self.RAW_PROVIDER_RESPONSE_PUBLISHED,
            "PROVIDER_ERROR_MESSAGE_PUBLISHED": self.PROVIDER_ERROR_MESSAGE_PUBLISHED,
            "PROVIDER_REQUEST_ID_PUBLISHED": self.PROVIDER_REQUEST_ID_PUBLISHED,
            "PROVIDER_CORRELATION_ID_PUBLISHED": self.PROVIDER_CORRELATION_ID_PUBLISHED,
            "AUTHORIZATION_HEADER_PUBLISHED": self.AUTHORIZATION_HEADER_PUBLISHED,
            "TOKEN_OR_PIT_PUBLISHED": self.TOKEN_OR_PIT_PUBLISHED,
        }


def normalize_provider_response_headers(
    headers: Mapping[str, Any] | None,
) -> dict[str, str]:
    """Copy response headers while dropping credential-bearing header names."""
    if headers is None:
        return {}
    normalized: dict[str, str] = {}
    items = headers.items() if hasattr(headers, "items") else []
    for raw_key, raw_value in items:
        if raw_key is None:
            continue
        key = str(raw_key).strip()
        if not key:
            continue
        if key.lower() in _FORBIDDEN_DIAGNOSTIC_HEADER_NAMES:
            continue
        if raw_value is None:
            continue
        if isinstance(raw_value, (list, tuple)):
            value = ",".join(str(part) for part in raw_value if part is not None)
        else:
            value = str(raw_value)
        normalized[key] = value
    return normalized


# Backward-compatible internal alias used by the concrete HTTP client.
_normalize_response_headers = normalize_provider_response_headers


def _header_lookup(
    headers: Mapping[str, str], aliases: frozenset[str]
) -> str | None:
    for key, value in headers.items():
        if key.lower() in aliases:
            stripped = value.strip()
            if stripped:
                return stripped
    return None


def _content_type_value(headers: Mapping[str, str]) -> str | None:
    for key, value in headers.items():
        if key.lower() == "content-type":
            stripped = value.strip()
            return stripped or None
    return None


def classify_content_type(
    *, content_type: str | None, body: bytes
) -> str:
    """Classify provider content-type without publishing the raw header value."""
    if not body:
        return "EMPTY"
    if content_type is None:
        return "UNKNOWN"
    lowered = content_type.lower()
    media_type = lowered.split(";", 1)[0].strip()
    if media_type in {"application/json", "text/json"} or media_type.endswith("+json"):
        return "JSON"
    if media_type in {"text/html", "application/xhtml+xml"}:
        return "HTML"
    if media_type.startswith("text/"):
        return "TEXT"
    if media_type:
        return "OTHER"
    return "UNKNOWN"


def classify_provider_error_class(status_code: int) -> str:
    """Map definitive HTTP status to a bounded provider error class."""
    if status_code in {400, 422}:
        return "REQUEST_VALIDATION"
    if status_code == 401:
        return "AUTHENTICATION"
    if status_code == 403:
        return "AUTHORIZATION"
    if status_code == 404:
        return "NOT_FOUND"
    if status_code == 409:
        return "CONFLICT"
    if status_code == 429:
        return "RATE_LIMIT"
    if 500 <= status_code <= 599:
        return "PROVIDER_FAILURE"
    return "UNKNOWN"


def _extract_first_string_field(
    envelope: Mapping[str, Any], aliases: tuple[str, ...]
) -> str | None:
    lowered = {str(key).lower(): key for key in envelope.keys()}
    for alias in aliases:
        actual = lowered.get(alias.lower())
        if actual is None:
            continue
        value = envelope.get(actual)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
    nested_error = envelope.get("error")
    if isinstance(nested_error, Mapping):
        return _extract_first_string_field(nested_error, aliases)
    return None


def _parse_provider_error_envelope(
    body: bytes, content_type_class: str
) -> tuple[bool, str | None, str | None]:
    if content_type_class != "JSON" or not body:
        return False, None, None
    try:
        decoded = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False, None, None
    if not isinstance(decoded, Mapping):
        return False, None, None
    code = _extract_first_string_field(decoded, _ERROR_CODE_FIELD_ALIASES)
    message = _extract_first_string_field(decoded, _ERROR_MESSAGE_FIELD_ALIASES)
    # A bare JSON object counts as a parseable envelope even when only structure
    # is present; presence flags still remain NO when fields are absent.
    return True, code, message


def derive_private_provider_error_evidence(
    result: LiveNoteHttpResult,
) -> PrivateProviderErrorEvidence:
    """Derive private diagnostic evidence from one definitive provider response."""
    if not isinstance(result, LiveNoteHttpResult):
        raise LiveNoteTransportError("result must be a LiveNoteHttpResult")
    if 200 <= int(result.status_code) < 300:
        raise LiveNoteTransportError(
            "provider error evidence is only derived for definitive non-2xx responses"
        )
    headers = normalize_provider_response_headers(result.headers)
    body = bytes(result.body or b"")
    content_type = _content_type_value(headers)
    content_type_class = classify_content_type(content_type=content_type, body=body)
    parseable, error_code, error_message = _parse_provider_error_envelope(
        body, content_type_class
    )
    return PrivateProviderErrorEvidence(
        PROVIDER_HTTP_STATUS=int(result.status_code),
        CONTENT_TYPE=content_type,
        CONTENT_TYPE_CLASS=content_type_class,
        RESPONSE_BODY_LENGTH=len(body),
        RESPONSE_BODY_SHA256=hashlib.sha256(body).hexdigest(),
        PROVIDER_ERROR_ENVELOPE_PARSEABLE=parseable,
        PROVIDER_ERROR_CODE=error_code,
        PROVIDER_ERROR_MESSAGE=error_message,
        PROVIDER_REQUEST_ID=_header_lookup(headers, _REQUEST_ID_HEADER_ALIASES),
        PROVIDER_CORRELATION_ID=_header_lookup(
            headers, _CORRELATION_ID_HEADER_ALIASES
        ),
        PROVIDER_ERROR_CLASS=classify_provider_error_class(int(result.status_code)),
        # HTTP class alone never establishes detailed cause.
        PROVIDER_ERROR_CAUSE="UNKNOWN",
    )


def project_public_provider_error_evidence(
    evidence: PrivateProviderErrorEvidence,
) -> PublicProviderErrorProjection:
    """Project private evidence to public-safe presence and classification flags."""
    if evidence.CONTENT_TYPE_CLASS == "EMPTY" and evidence.RESPONSE_BODY_LENGTH == 0:
        envelope_present = "NO"
    elif evidence.PROVIDER_ERROR_ENVELOPE_PARSEABLE:
        envelope_present = "YES"
    elif evidence.CONTENT_TYPE_CLASS == "JSON":
        envelope_present = "NO"
    elif evidence.RESPONSE_BODY_LENGTH == 0:
        envelope_present = "NO"
    else:
        envelope_present = "UNKNOWN"

    return PublicProviderErrorProjection(
        PROVIDER_HTTP_STATUS=evidence.PROVIDER_HTTP_STATUS,
        PROVIDER_CONTENT_TYPE_CLASS=evidence.CONTENT_TYPE_CLASS,
        PROVIDER_ERROR_ENVELOPE_PRESENT=envelope_present,
        PROVIDER_ERROR_CODE_PRESENT=(
            "YES" if evidence.PROVIDER_ERROR_CODE else "NO"
        ),
        PROVIDER_ERROR_MESSAGE_PRESENT=(
            "YES" if evidence.PROVIDER_ERROR_MESSAGE else "NO"
        ),
        PROVIDER_REQUEST_ID_PRESENT=(
            "YES" if evidence.PROVIDER_REQUEST_ID else "NO"
        ),
        PROVIDER_CORRELATION_ID_PRESENT=(
            "YES" if evidence.PROVIDER_CORRELATION_ID else "NO"
        ),
        PROVIDER_ERROR_CLASS=evidence.PROVIDER_ERROR_CLASS,
        PROVIDER_ERROR_CAUSE=evidence.PROVIDER_ERROR_CAUSE,
    )


def public_provider_error_projection_from_result(
    result: LiveNoteHttpResult,
) -> dict[str, Any]:
    """Convenience: private derive + public project for one non-2xx result."""
    private = derive_private_provider_error_evidence(result)
    return project_public_provider_error_evidence(private).as_public_dict()


class LiveNoteHttpClient(Protocol):
    """Injected HTTP seam. The transport never constructs a network client."""

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


class InjectedLiveNoteCredential:
    """Injected credential placeholder. Never logged and never discovered."""

    def __init__(self, bearer_token: str) -> None:
        if not isinstance(bearer_token, str) or not bearer_token.strip():
            raise LiveNoteTransportError(
                "injected credential token must be a non-empty string"
            )
        self._bearer_token = bearer_token

    @property
    def bearer_token(self) -> str:
        return self._bearer_token

    def __repr__(self) -> str:
        return "InjectedLiveNoteCredential(bearer_token=<redacted>)"

    def __str__(self) -> str:
        return "InjectedLiveNoteCredential(bearer_token=<redacted>)"


class BoundedLiveNoteTransport:
    """Bounded contact preflight plus one POST and one same-run NOTE GET."""

    def __init__(
        self,
        *,
        bound_contact_id: str,
        credential: InjectedLiveNoteCredential,
        http_client: LiveNoteHttpClient,
        optional_author_user_id: str | None = None,
        optional_title: str | None = None,
    ) -> None:
        self._bound_contact_id = self._require_bound_contact_id(bound_contact_id)
        if not isinstance(credential, InjectedLiveNoteCredential):
            raise LiveNoteTransportError(
                "credential must be an injected InjectedLiveNoteCredential"
            )
        self._bearer_token = credential.bearer_token
        self._http_client = http_client
        self._optional_author_user_id = self._optional_metadata(
            "optional_author_user_id", optional_author_user_id
        )
        self._optional_title = self._optional_metadata("optional_title", optional_title)
        self._post_attempts = 0
        self._post_successes = 0
        self._get_attempts = 0
        self._contact_get_attempts = 0
        self._total_network_calls = 0
        self._total_mutation_calls = 0
        self._same_run_note_id: str | None = None
        self._call_history: list[tuple[str, str]] = []

    @property
    def post_attempts(self) -> int:
        return self._post_attempts

    @property
    def post_successes(self) -> int:
        return self._post_successes

    @property
    def get_attempts(self) -> int:
        return self._get_attempts

    @property
    def contact_get_attempts(self) -> int:
        return self._contact_get_attempts

    @property
    def total_network_calls(self) -> int:
        return self._total_network_calls

    @property
    def total_mutation_calls(self) -> int:
        return self._total_mutation_calls

    def __repr__(self) -> str:
        return (
            "BoundedLiveNoteTransport("
            f"bound_contact_id={_REDACTED}, "
            f"post_attempts={self._post_attempts}, "
            f"get_attempts={self._get_attempts}, "
            f"total_network_calls={self._total_network_calls})"
        )

    def dispatch(
        self, method: str, path: str, body: Mapping[str, Any] | None = None
    ) -> LiveNoteResponse:
        """Dispatch one exact bound-contact or frozen NOTE route."""
        if not isinstance(method, str) or method.upper() not in _ALLOWED_METHODS:
            raise LiveNoteTransportError("only POST and GET routes are allowed")
        normalized_method = method.upper()
        self._reject_unsafe_path(path)
        if normalized_method == "POST":
            return self._dispatch_post(path, body)
        if path == f"/contacts/{self._bound_contact_id}":
            return self._dispatch_contact_get(path, body)
        return self._dispatch_get(path, body)

    def _dispatch_post(
        self, path: str, body: Mapping[str, Any] | None
    ) -> LiveNoteResponse:
        expected_path = f"/contacts/{self._bound_contact_id}/notes"
        if path != expected_path:
            raise LiveNoteTransportError("POST path is not the bound-contact notes route")
        provider_body = self._wire_post_body(self._validate_post_body(body))
        self._require_post_budget()
        self._post_attempts += 1
        self._total_mutation_calls += 1
        self._total_network_calls += 1
        self._call_history.append(("POST", _REDACTED_POST_PATH))
        result = self._attempt_http(
            method="POST",
            path=path,
            payload=provider_body,
            mutation=True,
        )
        if result is None:
            return LiveNoteResponse("ambiguous", {})
        return self._normalize_post_http_result(result)

    def _dispatch_contact_get(
        self, path: str, body: Mapping[str, Any] | None
    ) -> LiveNoteResponse:
        if body is not None:
            raise LiveNoteTransportError("bound-contact GET does not accept a body")
        expected_path = f"/contacts/{self._bound_contact_id}"
        if path != expected_path:
            raise LiveNoteTransportError("GET path is not the bound-contact route")
        self._require_contact_get_budget()
        self._contact_get_attempts += 1
        self._call_history.append(("GET", _REDACTED_CONTACT_GET_PATH))
        result = self._attempt_http(
            method="GET",
            path=path,
            payload=None,
            mutation=False,
        )
        if result is None:
            return LiveNoteResponse("error", {})
        return self._normalize_contact_get_http_result(result)

    def _dispatch_get(
        self, path: str, body: Mapping[str, Any] | None
    ) -> LiveNoteResponse:
        if body is not None:
            raise LiveNoteTransportError("NOTE GET routes do not accept a body")
        if self._same_run_note_id is None:
            raise LiveNoteTransportError(
                "GET requires the exact note id returned by the same-run POST"
            )
        expected_path = (
            f"/contacts/{self._bound_contact_id}/notes/{self._same_run_note_id}"
        )
        if path != expected_path:
            raise LiveNoteTransportError(
                "GET path is not the bound-contact same-run note route"
            )
        self._require_get_budget()
        self._get_attempts += 1
        self._total_network_calls += 1
        self._call_history.append(("GET", _REDACTED_GET_PATH))
        result = self._attempt_http(
            method="GET",
            path=path,
            payload=None,
            mutation=False,
        )
        if result is None:
            return LiveNoteResponse("error", {})
        return self._normalize_get_http_result(result)

    def _attempt_http(
        self,
        *,
        method: str,
        path: str,
        payload: Mapping[str, Any] | None,
        mutation: bool,
    ) -> LiveNoteHttpResult | None:
        headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Version": VERSION_HEADER,
            "Accept": "application/json",
        }
        encoded_body: bytes | None = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            encoded_body = json.dumps(
                payload,
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        try:
            return self._http_client.request(
                method=method,
                url=f"{BASE_URL}{path}",
                headers=headers,
                body=encoded_body,
                timeout_seconds=REQUEST_TIMEOUT_SECONDS,
                allow_redirects=False,
            )
        except LiveNoteHttpUncertainty:
            return None
        except Exception:
            if mutation:
                return None
            raise LiveNoteTransportError(
                "GET transport failed without a proven response"
            ) from None

    def _normalize_post_http_result(self, result: LiveNoteHttpResult) -> LiveNoteResponse:
        if not 200 <= result.status_code < 300:
            if result.status_code < 200 or self._post_status_is_ambiguous(
                result.status_code
            ):
                return LiveNoteResponse("ambiguous", {})
            return LiveNoteResponse("error", {})
        note = self._extract_note_envelope(result.body)
        if note is None:
            return LiveNoteResponse("ambiguous", {})
        note_id = note.get("id")
        if not isinstance(note_id, str) or not note_id.strip():
            return LiveNoteResponse("ambiguous", {})
        normalized = self._published_note(note)
        self._same_run_note_id = note_id
        self._post_successes += 1
        return LiveNoteResponse("ok", {"note": normalized})

    def _normalize_get_http_result(self, result: LiveNoteHttpResult) -> LiveNoteResponse:
        if not 200 <= result.status_code < 300:
            return LiveNoteResponse("error", {})
        note = self._extract_note_envelope(result.body)
        if note is None:
            return LiveNoteResponse("error", {})
        return LiveNoteResponse("ok", {"note": self._published_note(note)})

    def _normalize_contact_get_http_result(
        self, result: LiveNoteHttpResult
    ) -> LiveNoteResponse:
        if not 200 <= result.status_code < 300:
            return LiveNoteResponse("error", {})
        contact = self._extract_contact_envelope(result.body)
        if contact is None:
            return LiveNoteResponse("error", {})
        contact_id = contact.get("id")
        location_id = contact.get("locationId")
        if (
            not isinstance(contact_id, str)
            or not contact_id.strip()
            or not isinstance(location_id, str)
            or not location_id.strip()
        ):
            return LiveNoteResponse("error", {})
        return LiveNoteResponse(
            "ok",
            {"contact": {"id": contact_id, "locationId": location_id}},
        )

    def _require_post_budget(self) -> None:
        if self._post_attempts >= POST_ATTEMPTS_MAX:
            raise LiveNoteTransportError("POST attempts max is 1")
        if self._post_successes >= POST_SUCCESSES_MAX:
            raise LiveNoteTransportError("POST successes max is 1")
        if self._total_mutation_calls >= TOTAL_MUTATION_CALLS_MAX:
            raise LiveNoteTransportError("total mutation calls max is 1")
        if self._total_network_calls >= TOTAL_NETWORK_CALLS_MAX:
            raise LiveNoteTransportError("total network calls max is 2")

    def _require_get_budget(self) -> None:
        if self._get_attempts >= READBACK_GET_ATTEMPTS_MAX:
            raise LiveNoteTransportError("GET attempts max is 1")
        if self._total_network_calls >= TOTAL_NETWORK_CALLS_MAX:
            raise LiveNoteTransportError("total network calls max is 2")

    def _require_contact_get_budget(self) -> None:
        if self._contact_get_attempts >= CONTACT_GET_ATTEMPTS_MAX:
            raise LiveNoteTransportError("bound-contact GET attempts max is 1")

    @staticmethod
    def _validate_post_body(body: Mapping[str, Any] | None) -> dict[str, str]:
        if not isinstance(body, Mapping) or set(body) != {"body"}:
            raise LiveNoteTransportError("NOTE POST body must contain only body")
        note_body = body["body"]
        if not isinstance(note_body, str) or not note_body:
            raise LiveNoteTransportError("NOTE POST body must be a non-empty string")
        return {"body": note_body}

    def _wire_post_body(self, provider_body: Mapping[str, str]) -> dict[str, str]:
        wire_body = dict(provider_body)
        if self._optional_author_user_id is not None:
            wire_body["userId"] = self._optional_author_user_id
        if self._optional_title is not None:
            wire_body["title"] = self._optional_title
        return wire_body

    @staticmethod
    def _post_status_is_ambiguous(status_code: int) -> bool:
        if status_code >= 500 or status_code in {302, 303, 307, 308, 408, 429}:
            return True
        return 300 <= status_code < 400

    @staticmethod
    def _extract_note_envelope(raw_body: bytes) -> Mapping[str, Any] | None:
        try:
            decoded = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            return None
        if not isinstance(decoded, Mapping):
            return None
        note = decoded.get("note")
        if not isinstance(note, Mapping):
            return None
        return note

    @staticmethod
    def _extract_contact_envelope(raw_body: bytes) -> Mapping[str, Any] | None:
        try:
            decoded = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            return None
        if not isinstance(decoded, Mapping):
            return None
        contact = decoded.get("contact")
        if not isinstance(contact, Mapping):
            return None
        return contact

    @staticmethod
    def _published_note(note: Mapping[str, Any]) -> dict[str, Any]:
        published: dict[str, Any] = {}
        for field_name in _NOTE_RESPONSE_FIELDS:
            if field_name in note:
                published[field_name] = note[field_name]
        return published

    @staticmethod
    def _require_bound_contact_id(value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise LiveNoteTransportError("bound_contact_id must be a non-empty string")
        if any(separator in value for separator in ("/", "?", "#", "\\")):
            raise LiveNoteTransportError(
                "bound_contact_id contains forbidden route characters"
            )
        return value

    @staticmethod
    def _optional_metadata(name: str, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            raise LiveNoteTransportError(
                f"{name} must be a non-empty string when supplied"
            )
        return value

    @staticmethod
    def _reject_unsafe_path(path: object) -> None:
        if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
            raise LiveNoteTransportError("path is not an allowed note route")
        if any(separator in path for separator in ("?", "#", "\\")):
            raise LiveNoteTransportError(
                "search, list, pagination, and query routes are forbidden"
            )
        if ".." in path:
            raise LiveNoteTransportError("alternate routes are forbidden")
