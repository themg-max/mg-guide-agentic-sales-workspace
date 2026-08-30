from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from google.auth.exceptions import RefreshError

import integrations.ghl.highlevel_rest.live_note_runtime as live_note_runtime
import integrations.ghl.highlevel_rest.workflow_identity_diagnostic as diagnostic


REPO_ROOT = Path(__file__).resolve().parents[4]
WORKFLOW_PATH = (
    REPO_ROOT / ".github" / "workflows" / "nw008-at1-ghl-identity-diagnostic.yml"
)
TOKEN_SENTINEL = "synthetic-token-value-must-never-render"
CREDENTIAL_SENTINEL = "synthetic-credential-value-must-never-render"


class _FakeTargetCredentials:
    def __init__(self, principal: str, *, fail_refresh: bool = False) -> None:
        self.service_account_email = principal
        self.token = TOKEN_SENTINEL
        self.fail_refresh = fail_refresh
        self.refresh_requests: list[object] = []

    def refresh(self, request: object) -> None:
        self.refresh_requests.append(request)
        if self.fail_refresh:
            raise RefreshError(TOKEN_SENTINEL)


def _source(principal: str) -> object:
    credentials = type("FakeSourceCredentials", (), {})()
    credentials.token = CREDENTIAL_SENTINEL
    return live_note_runtime._MaterializedWorkflowSource(
        credentials=credentials,
        principal=principal,
    )


def _rendered_result(result: diagnostic.WorkflowIdentityDiagnosticResult) -> str:
    return "\n".join(
        (
            result.render(),
            repr(result),
            json.dumps(result.as_safe_metadata(), sort_keys=True),
        )
    )


def test_one_refresh_uses_existing_source_gate_target_constructor_and_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL)
    target = _FakeTargetCredentials(diagnostic.EXPECTED_TARGET_PRINCIPAL)
    request = object()
    calls: dict[str, object] = {"source_gate": 0, "target_constructor": 0}

    def fake_source_gate() -> object:
        calls["source_gate"] = int(calls["source_gate"]) + 1
        return source

    def fake_target_constructor(observed_source: object) -> object:
        calls["target_constructor"] = int(calls["target_constructor"]) + 1
        calls["constructor_source"] = observed_source
        return target

    monkeypatch.setattr(
        live_note_runtime,
        "_resolve_source_application_credentials",
        fake_source_gate,
    )
    monkeypatch.setattr(
        live_note_runtime,
        "_impersonate_target_runtime_credentials",
        fake_target_constructor,
    )

    result = diagnostic.run_workflow_identity_diagnostic(
        request_factory=lambda: request
    )

    assert calls == {
        "source_gate": 1,
        "target_constructor": 1,
        "constructor_source": source,
    }
    assert target.refresh_requests == [request]
    assert result.source_principal_match == "YES"
    assert result.target_principal_match == "YES"
    assert result.target_credential_refresh_attempts == 1
    assert result.target_credential_refresh_result == "PASS"
    assert result.as_safe_metadata()["OBSERVED_WORKFLOW_SOURCE_PRINCIPAL"] == (
        diagnostic.EXPECTED_SOURCE_PRINCIPAL
    )
    assert result.as_safe_metadata()["TARGET_PRINCIPAL"] == (
        diagnostic.EXPECTED_TARGET_PRINCIPAL
    )
    assert result.as_safe_metadata()["NO_UNEXPECTED_RETRY"] == "YES"
    assert result.as_safe_metadata()["GITHUB_OIDC_EXCHANGE_ATTEMPTS"] == 1
    assert result.as_safe_metadata()["NOTE_RUNTIME_IMPERSONATION_ATTEMPTS"] == 1
    assert result.as_safe_metadata()["GITHUB_OIDC_TO_WORKFLOW"] == "PASS"
    assert result.as_safe_metadata()["TARGET_IMPERSONATION_SUCCEEDED"] == "YES"
    assert diagnostic.EXPECTED_SOURCE_PRINCIPAL == (
        "mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )
    assert diagnostic.EXPECTED_TARGET_PRINCIPAL == (
        "mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )

    rendered = _rendered_result(result)
    assert TOKEN_SENTINEL not in rendered
    assert CREDENTIAL_SENTINEL not in rendered
    assert result.as_safe_metadata()["TOKEN_OR_CREDENTIAL_VALUE_PUBLISHED"] == "NO"


def test_source_mismatch_fails_before_target_construction_or_refresh() -> None:
    effects = {"target_constructions": 0, "request_constructions": 0}

    def unexpected_target_constructor(source: object) -> object:
        effects["target_constructions"] += 1
        raise AssertionError("source mismatch must stop target construction")

    def unexpected_request_factory() -> object:
        effects["request_constructions"] += 1
        raise AssertionError("source mismatch must stop request construction")

    with pytest.raises(diagnostic.WorkflowIdentityDiagnosticError) as failure:
        diagnostic.run_workflow_identity_diagnostic(
            source_gate=lambda: _source("unrelated@example.invalid"),
            target_credentials_constructor=unexpected_target_constructor,
            request_factory=unexpected_request_factory,
        )

    assert failure.value.result.source_principal_match == "NO"
    assert failure.value.result.target_credential_refresh_attempts == 0
    assert failure.value.result.stop == "SOURCE_PRINCIPAL_MISMATCH"
    assert effects == {"target_constructions": 0, "request_constructions": 0}


def test_source_gate_preserves_precise_safe_stop_code() -> None:
    def rejected_source_gate() -> object:
        raise live_note_runtime.SourceIdentityGateError(
            stop="SOURCE_PROVIDER_MISMATCH",
            detail="synthetic safe failure",
        )

    with pytest.raises(diagnostic.WorkflowIdentityDiagnosticError) as failure:
        diagnostic.run_workflow_identity_diagnostic(
            source_gate=rejected_source_gate,
        )

    assert failure.value.result.stop == "SOURCE_PROVIDER_MISMATCH"
    assert failure.value.result.source_principal_match == "NOT_CONFIRMED"
    assert failure.value.result.target_credential_refresh_attempts == 0


def test_target_mismatch_fails_before_request_creation_or_refresh() -> None:
    target = _FakeTargetCredentials("unrelated@example.invalid")
    request_constructions = 0

    def unexpected_request_factory() -> object:
        nonlocal request_constructions
        request_constructions += 1
        raise AssertionError("target mismatch must stop request construction")

    with pytest.raises(diagnostic.WorkflowIdentityDiagnosticError) as failure:
        diagnostic.run_workflow_identity_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=unexpected_request_factory,
        )

    result = failure.value.result
    assert result.target_principal_match == "NO"
    assert result.target_credential_refresh_attempts == 0
    assert result.target_credential_refresh_result == "NOT_ATTEMPTED"
    assert result.stop == "TARGET_PRINCIPAL_MISMATCH"
    assert target.refresh_requests == []
    assert request_constructions == 0


def test_refresh_failure_is_one_shot_and_sanitized() -> None:
    target = _FakeTargetCredentials(
        diagnostic.EXPECTED_TARGET_PRINCIPAL,
        fail_refresh=True,
    )
    request = object()

    with pytest.raises(diagnostic.WorkflowIdentityDiagnosticError) as failure:
        diagnostic.run_workflow_identity_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=lambda: request,
        )

    result = failure.value.result
    assert target.refresh_requests == [request]
    assert result.target_credential_refresh_attempts == 1
    assert result.target_credential_refresh_result == "FAIL"
    assert result.stop == "TARGET_CREDENTIAL_REFRESH_FAILED"
    rendered = f"{failure.value}\n{_rendered_result(result)}"
    assert TOKEN_SENTINEL not in rendered
    assert CREDENTIAL_SENTINEL not in rendered


def test_static_workflow_contract_is_manual_and_identity_only() -> None:
    raw_workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.load(raw_workflow, Loader=yaml.BaseLoader)

    assert workflow["on"] == {"workflow_dispatch": {}}
    assert workflow["permissions"] == {
        "contents": "read",
        "id-token": "write",
    }

    jobs = workflow["jobs"]
    assert list(jobs) == ["workflow-identity-diagnostic"]
    steps = jobs["workflow-identity-diagnostic"]["steps"]
    auth_index, auth = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("id") == "auth"
    )
    assert auth["uses"] == "google-github-actions/auth@v2"
    assert auth["with"] == {
        "workload_identity_provider": (
            "projects/831270426395/locations/global/"
            "workloadIdentityPools/github-actions-pool-v2/"
            "providers/mg-guide-github-provider-v1"
        ),
        "service_account": (
            "mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com"
        ),
        "create_credentials_file": "true",
        "cleanup_credentials": "false",
        "export_environment_variables": "false",
    }

    diagnostic_index, diagnostic_step = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("run")
        == "python -m integrations.ghl.highlevel_rest.workflow_identity_diagnostic"
    )
    assert diagnostic_index > auth_index
    assert diagnostic_step["env"][
        "MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG"
    ] == "${{ steps.auth.outputs.credentials_file_path }}"
    assert diagnostic_step["env"]["PYTHONPATH"] == "src"

    delete_index, delete_step = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("name") == "Delete auth credential file"
    )
    verify_index, verify_step = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("name") == "Verify auth credential file is absent"
    )

    assert auth_index < diagnostic_index < delete_index < verify_index
    for cleanup_step in (delete_step, verify_step):
        assert cleanup_step["if"] == "always()"
        assert cleanup_step["shell"] == "bash"
        assert cleanup_step["env"]["CREDENTIAL_FILE_PATH"] == (
            "${{ steps.auth.outputs.credentials_file_path }}"
        )

    delete_script = delete_step["run"]
    assert 'rm -- "$CREDENTIAL_FILE_PATH"' in delete_script
    assert "rm -rf" not in delete_script
    assert '[[ -L "$CREDENTIAL_FILE_PATH" ]]' in delete_script
    assert '[[ ! -f "$CREDENTIAL_FILE_PATH" ]]' in delete_script
    assert '"$GITHUB_WORKSPACE"/gha-creds-*.json' in delete_script
    assert "CREDENTIAL_FILE_DELETE_ATTEMPTS=1" in delete_script
    assert "EXPLICIT_CREDENTIAL_CLEANUP_PERFORMED=YES" in delete_script

    verify_script = verify_step["run"]
    assert '[[ -e "$CREDENTIAL_FILE_PATH" || -L "$CREDENTIAL_FILE_PATH" ]]' in (
        verify_script
    )
    assert 'residual_files=("$GITHUB_WORKSPACE"/gha-creds-*.json)' in verify_script
    assert "CREDENTIAL_FILE_ABSENT_AFTER_DELETE=YES" in verify_script
    assert "RESIDUAL_GHA_CREDENTIAL_FILES=0" in verify_script
    assert "RUNNER_DISPOSAL_RELIED_UPON=NO" in verify_script
    assert "CREDENTIAL_CLEANUP_RESULT=PASS" in verify_script

    assert "secrets." not in raw_workflow
    assert "GOOGLE_GHA_CREDS_PATH" not in raw_workflow
    assert "GOOGLE_APPLICATION_CREDENTIALS" not in raw_workflow


def test_harness_has_no_ambient_adc_or_downstream_operation_path() -> None:
    source = (
        REPO_ROOT
        / "src"
        / "integrations"
        / "ghl"
        / "highlevel_rest"
        / "workflow_identity_diagnostic.py"
    ).read_text(encoding="utf-8")

    assert "google.auth.default" not in source
    for forbidden_call in (
        "_new_secret_manager_client(",
        "access_secret_version(",
        "ConcreteLiveNoteHttpClient(",
        "assemble_bound_live_note_runtime(",
        "subprocess.",
    ):
        assert forbidden_call not in source
