"""One-shot workflow-to-note-runtime identity diagnostic.

Phase D defines this harness but does not execute it. A separately governed
Phase E workflow run may refresh the target credential exactly once. The
result surface contains status metadata only and never reads or renders a
credential or token value.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
from typing import Callable

from google.auth.exceptions import GoogleAuthError

from . import live_note_runtime


EXPECTED_SOURCE_PRINCIPAL = live_note_runtime._EXPECTED_SOURCE_PRINCIPAL
EXPECTED_TARGET_PRINCIPAL = live_note_runtime._TARGET_RUNTIME_SERVICE_ACCOUNT
MAX_TARGET_CREDENTIAL_REFRESH_ATTEMPTS = 1


@dataclass(frozen=True)
class WorkflowIdentityDiagnosticResult:
    """Public-safe status for one diagnostic execution."""

    diagnostic_result: str
    source_identity_gate: str
    source_principal_match: str
    target_principal_match: str
    target_credential_refresh_attempts: int
    target_credential_refresh_result: str
    stop: str

    def as_safe_metadata(self) -> dict[str, str | int]:
        return {
            "DIAGNOSTIC_RESULT": self.diagnostic_result,
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
            "TARGET_CREDENTIAL_REFRESH_ATTEMPTS": (
                self.target_credential_refresh_attempts
            ),
            "TARGET_CREDENTIAL_REFRESH_RESULT": (
                self.target_credential_refresh_result
            ),
            "TOKEN_OR_CREDENTIAL_VALUE_PUBLISHED": "NO",
            "NO_UNEXPECTED_RETRY": "YES",
            "SECRET_MANAGER_CALLS": 0,
            "GHL_REQUESTS": 0,
            "CRM_OPERATIONS": 0,
            "DEPLOYMENTS": 0,
            "STOP": self.stop,
        }

    def render(self) -> str:
        """Render only the fixed public-safe metadata fields."""
        return "\n".join(
            f"{key}={value}" for key, value in self.as_safe_metadata().items()
        )


class WorkflowIdentityDiagnosticError(RuntimeError):
    """Fail-closed diagnostic error carrying only public-safe status."""

    def __init__(self, result: WorkflowIdentityDiagnosticResult) -> None:
        self.result = result
        super().__init__(result.render())


def _failed_result(
    *,
    source_identity_gate: str,
    source_principal_match: str,
    target_principal_match: str,
    refresh_attempts: int,
    refresh_result: str,
    stop: str,
) -> WorkflowIdentityDiagnosticError:
    return WorkflowIdentityDiagnosticError(
        WorkflowIdentityDiagnosticResult(
            diagnostic_result="FAIL_CLOSED",
            source_identity_gate=source_identity_gate,
            source_principal_match=source_principal_match,
            target_principal_match=target_principal_match,
            target_credential_refresh_attempts=refresh_attempts,
            target_credential_refresh_result=refresh_result,
            stop=stop,
        )
    )


def _new_google_auth_request() -> object:
    request_module = importlib.import_module("google.auth.transport.requests")
    return request_module.Request()


def run_workflow_identity_diagnostic(
    *,
    source_gate: Callable[[], object] | None = None,
    target_credentials_constructor: Callable[[object], object] | None = None,
    request_factory: Callable[[], object] | None = None,
) -> WorkflowIdentityDiagnosticResult:
    """Validate the exact identity chain and make one target refresh attempt."""
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

    try:
        source = resolved_source_gate()
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
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            stop="SOURCE_IDENTITY_GATE_REJECTED",
        ) from None

    observed_source_principal = getattr(source, "principal", None)
    if observed_source_principal != EXPECTED_SOURCE_PRINCIPAL:
        raise _failed_result(
            source_identity_gate="FAIL",
            source_principal_match="NO",
            target_principal_match="NOT_EVALUATED",
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            stop="SOURCE_PRINCIPAL_MISMATCH",
        )

    try:
        target_credentials = resolved_target_constructor(source)
    except live_note_runtime.LiveNoteRuntimeAssemblyError:
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="NOT_CONFIRMED",
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
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
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            stop="TARGET_PRINCIPAL_MISMATCH",
        )

    refresh = getattr(target_credentials, "refresh", None)
    if not callable(refresh):
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
            stop="TARGET_REFRESH_UNAVAILABLE",
        )

    try:
        request = resolved_request_factory()
    except ImportError:
        raise _failed_result(
            source_identity_gate="PASS",
            source_principal_match="YES",
            target_principal_match="YES",
            refresh_attempts=0,
            refresh_result="NOT_ATTEMPTED",
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
            refresh_attempts=refresh_attempts,
            refresh_result="FAIL",
            stop="TARGET_CREDENTIAL_REFRESH_FAILED",
        ) from None

    return WorkflowIdentityDiagnosticResult(
        diagnostic_result="PASS",
        source_identity_gate="PASS",
        source_principal_match="YES",
        target_principal_match="YES",
        target_credential_refresh_attempts=refresh_attempts,
        target_credential_refresh_result="PASS",
        stop="NONE",
    )


def main() -> int:
    try:
        result = run_workflow_identity_diagnostic()
    except WorkflowIdentityDiagnosticError as exc:
        print(exc.result.render())
        return 1
    print(result.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
