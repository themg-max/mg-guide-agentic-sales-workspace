"""One-shot exact Secret Manager access diagnostic.

Importing and testing this module is offline-only. A separately activated
manual workflow may resolve the sealed workflow identity, impersonate the
note-runtime identity, and check only that both authorized payloads are
present. Payload data is never decoded, measured, rendered, or returned.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
from typing import Callable

from google.api_core.exceptions import GoogleAPICallError
from google.auth.exceptions import GoogleAuthError

from . import live_note_runtime


EXPECTED_SOURCE_PRINCIPAL = live_note_runtime._EXPECTED_SOURCE_PRINCIPAL
EXPECTED_TARGET_PRINCIPAL = live_note_runtime._TARGET_RUNTIME_SERVICE_ACCOUNT
GHL_SECRET_VERSION_RESOURCE = (
    "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/2"
)
COMMITMENT_KEY_VERSION_RESOURCE = (
    "projects/ai-rolodex-to-crm/secrets/"
    "MG_GUIDE_NW008_COMMITMENT_KEY/versions/1"
)
MAX_TARGET_CREDENTIAL_REFRESH_ATTEMPTS = 1
MAX_GHL_SECRET_ACCESS_ATTEMPTS = 1
MAX_COMMITMENT_KEY_ACCESS_ATTEMPTS = 1
MAX_ACCESS_SECRET_VERSION_CALLS = 2

_SAFE_SOURCE_GATE_STOPS = frozenset(
    {
        "SOURCE_CREDENTIAL_CONFIG_REQUIRED",
        "SOURCE_CREDENTIAL_CONFIG_INVALID",
        "SOURCE_CREDENTIAL_TYPE_REJECTED",
        "SOURCE_PROVIDER_MISMATCH",
        "SOURCE_PRINCIPAL_MISMATCH",
    }
)


@dataclass(frozen=True)
class SecretAccessDiagnosticResult:
    """Public-safe status for one bounded diagnostic execution."""

    diagnostic_result: str
    source_identity_gate: str
    source_principal_match: str
    target_principal_match: str
    target_impersonation_attempts: int
    target_credential_refresh_attempts: int
    target_credential_refresh_result: str
    ghl_secret_access_attempts: int
    ghl_secret_payload_present: str
    commitment_key_access_attempts: int
    commitment_key_payload_present: str
    access_secret_version_calls: int
    stop: str

    def as_safe_metadata(self) -> dict[str, str | int]:
        """Return fixed status and effect metadata without sensitive values."""
        identity_chain_passed = (
            self.source_principal_match == "YES"
            and self.target_principal_match == "YES"
            and self.target_credential_refresh_result == "PASS"
        )
        return {
            "DIAGNOSTIC_RESULT": self.diagnostic_result,
            "SECRET_ACCESS_RESULT": self.diagnostic_result,
            "OBSERVED_WORKFLOW_SOURCE_PRINCIPAL": (
                EXPECTED_SOURCE_PRINCIPAL
                if self.source_principal_match == "YES"
                else "MISMATCH_REDACTED"
            ),
            "TARGET_PRINCIPAL": (
                EXPECTED_TARGET_PRINCIPAL
                if self.target_principal_match == "YES"
                else "MISMATCH_REDACTED"
            ),
            "SOURCE_IDENTITY_GATE": self.source_identity_gate,
            "SOURCE_PRINCIPAL_MATCH": self.source_principal_match,
            "TARGET_PRINCIPAL_MATCH": self.target_principal_match,
            "TARGET_IMPERSONATION_ATTEMPTS": self.target_impersonation_attempts,
            "TARGET_CREDENTIAL_REFRESH_ATTEMPTS": (
                self.target_credential_refresh_attempts
            ),
            "TARGET_CREDENTIAL_REFRESH_RESULT": (
                self.target_credential_refresh_result
            ),
            "GITHUB_OIDC_EXCHANGE_ATTEMPTS": (
                self.target_credential_refresh_attempts
            ),
            "NOTE_RUNTIME_IMPERSONATION_ATTEMPTS": (
                self.target_impersonation_attempts
            ),
            "GITHUB_OIDC_TO_WORKFLOW": (
                "PASS" if identity_chain_passed else "NOT_PROVEN"
            ),
            "TARGET_IMPERSONATION_SUCCEEDED": (
                "YES" if identity_chain_passed else "NO"
            ),
            "GHL_SECRET_ACCESS_ATTEMPTS": self.ghl_secret_access_attempts,
            "GHL_SECRET_PAYLOAD_PRESENT": self.ghl_secret_payload_present,
            "COMMITMENT_KEY_ACCESS_ATTEMPTS": (
                self.commitment_key_access_attempts
            ),
            "COMMITMENT_KEY_PAYLOAD_PRESENT": (
                self.commitment_key_payload_present
            ),
            "ACCESS_SECRET_VERSION_CALLS": self.access_secret_version_calls,
            "SECRET_VALUE_PUBLISHED": "NO",
            "SECRET_VALUE_PERSISTED": "NO",
            "SECRET_VALUE_LOGGED": "NO",
            "SECRET_VALUE_ECHOED": "NO",
            "SECRET_VALUE_HASHED_FOR_PROOF": "NO",
            "SECRET_VALUE_LENGTH_RECORDED": "NO",
            "SECRET_PAYLOAD_RETURNED": "NO",
            "TOKEN_OR_CREDENTIAL_VALUE_PUBLISHED": "NO",
            "NO_UNEXPECTED_RETRY": "YES",
            "GHL_REQUESTS": 0,
            "GHL_REST_CALLS": 0,
            "CRM_CALLS": 0,
            "CRM_OPERATIONS": 0,
            "CRM_READS": 0,
            "CRM_MUTATIONS": 0,
            "MUTATIONS": 0,
            "IAM_MUTATIONS": 0,
            "SECRET_MUTATIONS": 0,
            "PROVIDER_MUTATIONS": 0,
            "SERVICE_ACCOUNT_KEYS_CREATED": 0,
            "DEPLOYMENTS": 0,
            "STOP": self.stop,
        }

    def render(self) -> str:
        """Render only fixed public-safe metadata fields."""
        return "\n".join(
            f"{key}={value}" for key, value in self.as_safe_metadata().items()
        )


class SecretAccessDiagnosticError(RuntimeError):
    """Fail-closed diagnostic error carrying only public-safe status."""

    def __init__(self, result: SecretAccessDiagnosticResult) -> None:
        self.result = result
        super().__init__(result.render())


def _failed_result(
    *,
    source_identity_gate: str,
    source_principal_match: str,
    target_principal_match: str,
    target_impersonation_attempts: int,
    refresh_attempts: int,
    refresh_result: str,
    ghl_attempts: int,
    ghl_payload_present: str,
    commitment_attempts: int,
    commitment_payload_present: str,
    access_calls: int,
    stop: str,
) -> SecretAccessDiagnosticError:
    return SecretAccessDiagnosticError(
        SecretAccessDiagnosticResult(
            diagnostic_result="FAIL_CLOSED",
            source_identity_gate=source_identity_gate,
            source_principal_match=source_principal_match,
            target_principal_match=target_principal_match,
            target_impersonation_attempts=target_impersonation_attempts,
            target_credential_refresh_attempts=refresh_attempts,
            target_credential_refresh_result=refresh_result,
            ghl_secret_access_attempts=ghl_attempts,
            ghl_secret_payload_present=ghl_payload_present,
            commitment_key_access_attempts=commitment_attempts,
            commitment_key_payload_present=commitment_payload_present,
            access_secret_version_calls=access_calls,
            stop=stop,
        )
    )


def _new_google_auth_request() -> object:
    request_module = importlib.import_module("google.auth.transport.requests")
    return request_module.Request()


def _new_secret_manager_client(target_runtime_credentials: object) -> object:
    secretmanager_module = importlib.import_module("google.cloud.secretmanager")
    return secretmanager_module.SecretManagerServiceClient(
        credentials=target_runtime_credentials
    )


def _payload_data_is_present(response: object) -> bool:
    payload = getattr(response, "payload", None)
    if payload is None:
        return False
    return bool(getattr(payload, "data", None))


def _safe_source_gate_stop(stop: object) -> str:
    if isinstance(stop, str) and stop in _SAFE_SOURCE_GATE_STOPS:
        return stop
    return "SOURCE_IDENTITY_GATE_FAILED"


def run_secret_access_diagnostic(
    *,
    source_gate: Callable[[], object] | None = None,
    target_credentials_constructor: Callable[[object], object] | None = None,
    request_factory: Callable[[], object] | None = None,
    client_factory: Callable[[object], object] | None = None,
) -> SecretAccessDiagnosticResult:
    """Validate both identities and check each exact payload once, in order."""
    resolved_source_gate = (
        source_gate
        if source_gate is not None
        else live_note_runtime._resolve_source_application_credentials
    )
    resolved_target_constructor = (
        target_credentials_constructor
        if target_credentials_constructor is not None
        else live_note_runtime._impersonate_target_runtime_credentials
    )
    resolved_request_factory = (
        request_factory if request_factory is not None else _new_google_auth_request
    )
    resolved_client_factory = (
        client_factory if client_factory is not None else _new_secret_manager_client
    )

    try:
        source = resolved_source_gate()
    except live_note_runtime.SourceIdentityGateError as exc:
        raise _failed_result(
            source_identity_gate="FAIL",
            source_principal_match=(
                "NO" if exc.STOP == "SOURCE_PRINCIPAL_MISMATCH" else "NOT_CONFIRMED"
            ),
            target_principal_match="NOT_EVALUATED",
            target_impersonation_attempts=0,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop=_safe_source_gate_stop(exc.STOP),
        ) from None
    except (
        GoogleAuthError,
        OSError,
        ValueError,
        live_note_runtime.LiveNoteRuntimeAssemblyError,
    ):
        raise _failed_result(
            source_identity_gate="FAIL",
            source_principal_match="NOT_CONFIRMED",
            target_principal_match="NOT_EVALUATED",
            target_impersonation_attempts=0,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="SOURCE_CREDENTIAL_MATERIALIZATION_FAILED",
        ) from None

    observed_source_principal = getattr(source, "principal", None)
    if observed_source_principal != EXPECTED_SOURCE_PRINCIPAL:
        raise _failed_result(
            source_identity_gate="FAIL",
            source_principal_match="NO",
            target_principal_match="NOT_EVALUATED",
            target_impersonation_attempts=0,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="SOURCE_PRINCIPAL_MISMATCH",
        )

    target_impersonation_attempts = 1
    try:
        target_credentials = resolved_target_constructor(source)
    except (
        GoogleAuthError,
        ValueError,
        live_note_runtime.LiveNoteRuntimeAssemblyError,
    ):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="NOT_CONFIRMED",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="TARGET_CREDENTIAL_CONSTRUCTION_FAILED",
        ) from None

    observed_target_principal = getattr(
        target_credentials, "service_account_email", None
    )
    if observed_target_principal != EXPECTED_TARGET_PRINCIPAL:
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="NO",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="TARGET_PRINCIPAL_MISMATCH",
        )

    refresh = getattr(target_credentials, "refresh", None)
    if not callable(refresh):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="TARGET_REFRESH_UNAVAILABLE",
        )

    try:
        request = resolved_request_factory()
    except (ImportError, OSError):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="REQUEST_CONSTRUCTION_FAILED",
        ) from None

    refresh_attempts = MAX_TARGET_CREDENTIAL_REFRESH_ATTEMPTS
    try:
        refresh(request)
    except GoogleAuthError:
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="FAIL",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="TARGET_CREDENTIAL_REFRESH_FAILED",
        ) from None

    try:
        client = resolved_client_factory(target_credentials)
    except (GoogleAuthError, ImportError, ValueError):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="SECRET_MANAGER_CLIENT_CONSTRUCTION_FAILED",
        ) from None

    if not callable(getattr(client, "access_secret_version", None)):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=0,
            ghl_payload_present="NOT_EVALUATED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=0,
            stop="SECRET_MANAGER_CLIENT_INVALID",
        )

    ghl_attempts = MAX_GHL_SECRET_ACCESS_ATTEMPTS
    access_calls = 1
    try:
        ghl_response = client.access_secret_version(
            request={"name": GHL_SECRET_VERSION_RESOURCE},
            retry=None,
        )
    except (GoogleAPICallError, GoogleAuthError):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=ghl_attempts,
            ghl_payload_present="NOT_CONFIRMED",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=access_calls,
            stop="GHL_SECRET_ACCESS_FAILED",
        ) from None
    if not _payload_data_is_present(ghl_response):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=ghl_attempts,
            ghl_payload_present="NO",
            commitment_attempts=0,
            commitment_payload_present="NOT_EVALUATED",
            access_calls=access_calls,
            stop="GHL_SECRET_PAYLOAD_MISSING",
        )
    del ghl_response

    commitment_attempts = MAX_COMMITMENT_KEY_ACCESS_ATTEMPTS
    access_calls = MAX_ACCESS_SECRET_VERSION_CALLS
    try:
        commitment_response = client.access_secret_version(
            request={"name": COMMITMENT_KEY_VERSION_RESOURCE},
            retry=None,
        )
    except (GoogleAPICallError, GoogleAuthError):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=ghl_attempts,
            ghl_payload_present="YES",
            commitment_attempts=commitment_attempts,
            commitment_payload_present="NOT_CONFIRMED",
            access_calls=access_calls,
            stop="COMMITMENT_KEY_ACCESS_FAILED",
        ) from None
    if not _payload_data_is_present(commitment_response):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            target_impersonation_attempts=target_impersonation_attempts,
            refresh_attempts=refresh_attempts,
            refresh_result="PASS",
            ghl_attempts=ghl_attempts,
            ghl_payload_present="YES",
            commitment_attempts=commitment_attempts,
            commitment_payload_present="NO",
            access_calls=access_calls,
            stop="COMMITMENT_KEY_PAYLOAD_MISSING",
        )
    del commitment_response

    return SecretAccessDiagnosticResult(
        diagnostic_result="PASS",
        source_identity_gate="PASS",
        source_principal_match="YES",
        target_principal_match="YES",
        target_impersonation_attempts=target_impersonation_attempts,
        target_credential_refresh_attempts=refresh_attempts,
        target_credential_refresh_result="PASS",
        ghl_secret_access_attempts=ghl_attempts,
        ghl_secret_payload_present="YES",
        commitment_key_access_attempts=commitment_attempts,
        commitment_key_payload_present="YES",
        access_secret_version_calls=access_calls,
        stop="NONE",
    )


def main() -> int:
    try:
        result = run_secret_access_diagnostic()
    except SecretAccessDiagnosticError as exc:
        print(exc.result.render())
        return 1
    print(result.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
