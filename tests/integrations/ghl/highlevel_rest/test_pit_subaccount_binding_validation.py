from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any

import pytest

from integrations.ghl.highlevel_rest.pit_subaccount_binding_validation import (
    LIVE_GHL_CALLS,
    MAX_READS,
    MAX_TOTAL_BUSINESS_CALLS,
    MAX_WRITES,
    NETWORK_ENABLED,
    NO_RETRY,
    SECRET_MANAGER_ACCESS,
    TARGET_SA_IMPERSONATION,
    OfflinePitSubaccountBindingValidationExecutor,
    PitSubaccountBindingValidationTerminalStateError,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    LiveNoteHttpResult,
    LiveNoteHttpUncertainty,
)
from integrations.ghl.highlevel_rest.private_provider_diagnostic_persistence import (
    PrivateProviderDiagnosticContext,
    PrivateProviderDiagnosticStore,
)


FIXTURE_PATH = (
    Path(__file__).resolve().parents[4]
    / "fixtures"
    / "ghl"
    / "pit-subaccount-binding-validation.json"
)
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
PRIVATE_TARGET = FIXTURE["binding"]["private_validation_location_id"]


def _executor(
    *,
    private_diagnostic_context: PrivateProviderDiagnosticContext | None = None,
) -> OfflinePitSubaccountBindingValidationExecutor:
    return OfflinePitSubaccountBindingValidationExecutor(
        private_validation_location_id=PRIVATE_TARGET,
        private_diagnostic_context=private_diagnostic_context,
    )


def _result(case_id: str) -> LiveNoteHttpResult:
    case = FIXTURE["cases"][case_id]
    body = (
        case["raw_body"].encode("utf-8")
        if "raw_body" in case
        else json.dumps(case["body"], separators=(",", ":")).encode("utf-8")
    )
    return LiveNoteHttpResult(
        status_code=case["status_code"], body=body, headers=case["headers"]
    )


def _assert_one_read_budget(result: Any) -> None:
    assert result.business_calls_attempted == 1
    assert result.reads_attempted == 1
    assert result.writes_attempted == 0
    assert result.retry_performed is False


def _private_diagnostic_context(tmp_path: Path) -> PrivateProviderDiagnosticContext:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".gitignore").write_text("local/\n", encoding="utf-8")
    return PrivateProviderDiagnosticContext(
        store=PrivateProviderDiagnosticStore(
            repo_root=repo,
            private_root=repo / "local" / "private" / "provider-diagnostics",
        ),
        grant_id="grant-test-001",
        run_id="run-test-001",
        operation_id="location-get-001",
        sensitive_values=("synthetic-pit-never-persist",),
    )


def test_exact_location_match_passes_without_publishing_private_values() -> None:
    result = _executor().evaluate(_result("exact_location_match"))

    assert result.disposition == "PASS"
    assert result.public_proof == {
        "HTTP_STATUS": 200,
        "LOCATION_ENVELOPE_PRESENT": "YES",
        "RETURNED_LOCATION_ID_MATCH": "YES",
        "PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH": "YES",
        "RAW_LOCATION_ID_PUBLIC": "NO",
        "TOKEN_OR_PIT_PUBLISHED": "NO",
    }
    assert PRIVATE_TARGET not in json.dumps(result.public_proof)
    _assert_one_read_budget(result)


def test_bare_location_response_shape_passes() -> None:
    result = _executor().evaluate(
        LiveNoteHttpResult(
            status_code=200,
            body=json.dumps({"id": PRIVATE_TARGET}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
    )

    assert result.disposition == "PASS"
    assert result.public_proof["LOCATION_ENVELOPE_PRESENT"] == "YES"
    assert result.public_proof["RETURNED_LOCATION_ID_MATCH"] == "YES"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "YES"
    _assert_one_read_budget(result)


def test_explicit_wrong_location_id_is_definitive_mismatch() -> None:
    result = _executor().evaluate(_result("wrong_location_id"))

    assert result.disposition == "FAIL_CLOSED"
    assert result.public_proof["HTTP_STATUS"] == 200
    assert result.public_proof["LOCATION_ENVELOPE_PRESENT"] == "YES"
    assert result.public_proof["RETURNED_LOCATION_ID_MATCH"] == "NO"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "NO"
    assert result.public_proof["RAW_LOCATION_ID_PUBLIC"] == "NO"
    _assert_one_read_budget(result)


@pytest.mark.parametrize(
    ("case_id", "envelope_present"),
    [
        ("missing_location_envelope", "NO"),
        ("malformed_payload", "NO"),
    ],
)
def test_200_missing_or_malformed_binding_is_unknown(
    case_id: str, envelope_present: str
) -> None:
    result = _executor().evaluate(_result(case_id))

    assert result.disposition == "FAIL_CLOSED"
    assert result.public_proof["HTTP_STATUS"] == 200
    assert result.public_proof["LOCATION_ENVELOPE_PRESENT"] == envelope_present
    assert result.public_proof["RETURNED_LOCATION_ID_MATCH"] == "UNKNOWN"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "UNKNOWN"
    assert result.public_proof["RAW_LOCATION_ID_PUBLIC"] == "NO"
    _assert_one_read_budget(result)


def test_invalid_status_shape_is_binding_unresolved() -> None:
    result = _executor().evaluate(
        LiveNoteHttpResult(status_code="200", body=b"{}", headers={})  # type: ignore[arg-type]
    )

    assert result.disposition == "FAIL_CLOSED"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "UNKNOWN"
    assert result.public_proof["RETURNED_LOCATION_ID_MATCH"] == "UNKNOWN"
    assert "HTTP_STATUS" not in result.public_proof
    _assert_one_read_budget(result)


@pytest.mark.parametrize(
    ("case_id", "error_class"),
    [
        ("unauthenticated", "AUTHENTICATION"),
        ("unauthorized", "AUTHORIZATION"),
        ("not_found", "NOT_FOUND"),
        ("request_validation", "REQUEST_VALIDATION"),
        ("rate_limit", "RATE_LIMIT"),
        ("provider_failure", "PROVIDER_FAILURE"),
    ],
)
def test_definitive_non_2xx_is_binding_unresolved_with_safe_provider_evidence(
    case_id: str, error_class: str, tmp_path: Path
) -> None:
    result = _executor(
        private_diagnostic_context=_private_diagnostic_context(tmp_path)
    ).evaluate(_result(case_id))
    rendered_public = json.dumps(result.public_proof)

    assert result.disposition == "FAIL_CLOSED"
    assert result.public_proof["PROVIDER_ERROR_CLASS"] == error_class
    assert result.public_proof["PROVIDER_ERROR_CAUSE"] == "UNKNOWN"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "UNKNOWN"
    assert result.public_proof["RAW_PROVIDER_RESPONSE_PUBLISHED"] == "NO"
    assert result.public_proof["TOKEN_OR_PIT_PUBLISHED"] == "NO"
    assert result.public_proof["RAW_LOCATION_ID_PUBLIC"] == "NO"
    assert result.public_proof["PRIVATE_DIAGNOSTIC_PERSISTED"] == "YES"
    assert result.public_proof["DIAGNOSTIC_PERSISTENCE_VERIFIED"] == "YES"
    assert result.public_proof["DIAGNOSTIC_PERSISTENCE_FAILURE"] == "NO"
    assert result.public_proof["RETRY_PERFORMED"] == "NO"
    assert result.public_proof["SECOND_PROVIDER_CALL"] == "NO"
    assert set(result.public_proof) == {
        "PROVIDER_HTTP_STATUS",
        "PROVIDER_CONTENT_TYPE_CLASS",
        "PROVIDER_ERROR_ENVELOPE_PRESENT",
        "PROVIDER_ERROR_CODE_PRESENT",
        "PROVIDER_ERROR_MESSAGE_PRESENT",
        "PROVIDER_REQUEST_ID_PRESENT",
        "PROVIDER_CORRELATION_ID_PRESENT",
        "PROVIDER_ERROR_CLASS",
        "PROVIDER_ERROR_CAUSE",
        "RAW_PROVIDER_RESPONSE_PUBLISHED",
        "PROVIDER_ERROR_MESSAGE_PUBLISHED",
        "PROVIDER_REQUEST_ID_PUBLISHED",
        "PROVIDER_CORRELATION_ID_PUBLISHED",
        "AUTHORIZATION_HEADER_PUBLISHED",
        "TOKEN_OR_PIT_PUBLISHED",
        "PRIVATE_DIAGNOSTIC_PERSISTED",
        "DIAGNOSTIC_PERSISTENCE_VERIFIED",
        "DIAGNOSTIC_PERSISTENCE_FAILURE",
        "RETRY_PERFORMED",
        "SECOND_PROVIDER_CALL",
        "PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH",
        "RAW_LOCATION_ID_PUBLIC",
    }
    assert FIXTURE["cases"][case_id]["body"]["message"] not in rendered_public
    assert PRIVATE_TARGET not in rendered_public
    _assert_one_read_budget(result)


def test_non_2xx_without_private_persistence_fails_before_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_projection(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("public projection ran before persistence verification")

    monkeypatch.setattr(
        "integrations.ghl.highlevel_rest.pit_subaccount_binding_validation."
        "project_public_provider_error_evidence",
        unexpected_projection,
    )
    result = _executor().evaluate(_result("unauthorized"))

    assert result.disposition == "FAIL_CLOSED"
    assert result.public_proof == {
        "PROVIDER_HTTP_STATUS": 403,
        "PRIVATE_DIAGNOSTIC_PERSISTED": "NO",
        "DIAGNOSTIC_PERSISTENCE_VERIFIED": "NO",
        "DIAGNOSTIC_PERSISTENCE_FAILURE": "YES",
        "PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH": "UNKNOWN",
        "RAW_PROVIDER_RESPONSE_PUBLISHED": "NO",
        "RAW_LOCATION_ID_PUBLIC": "NO",
        "TOKEN_OR_PIT_PUBLISHED": "NO",
        "RETRY_PERFORMED": "NO",
        "SECOND_PROVIDER_CALL": "NO",
    }
    _assert_one_read_budget(result)


@pytest.mark.parametrize("uncertainty", ["timeout", "disconnect"])
def test_timeout_or_disconnect_is_binding_unresolved_ambiguous_read(
    uncertainty: str,
) -> None:
    result = _executor().evaluate(LiveNoteHttpUncertainty(uncertainty))

    assert result.disposition == "FAIL_AMBIGUOUS_READ"
    assert result.public_proof["READ_FAILURE_CLASS"] == "AMBIGUOUS"
    assert result.public_proof["PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH"] == "UNKNOWN"
    assert result.public_proof["RAW_LOCATION_ID_PUBLIC"] == "NO"
    _assert_one_read_budget(result)


def test_budgets_are_terminal_and_offline_only() -> None:
    executor = _executor()
    executor.evaluate(_result("exact_location_match"))

    with pytest.raises(PitSubaccountBindingValidationTerminalStateError):
        executor.evaluate(_result("exact_location_match"))

    assert MAX_READS == MAX_TOTAL_BUSINESS_CALLS == 1
    assert MAX_WRITES == 0
    assert NO_RETRY is True
    assert NETWORK_ENABLED is False
    assert LIVE_GHL_CALLS is False
    assert SECRET_MANAGER_ACCESS is False
    assert TARGET_SA_IMPERSONATION is False
