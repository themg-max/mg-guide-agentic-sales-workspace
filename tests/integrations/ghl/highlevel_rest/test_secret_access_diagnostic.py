from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace

from google.api_core.exceptions import PermissionDenied
from google.auth.exceptions import RefreshError
import pytest
import yaml

import integrations.ghl.highlevel_rest.live_note_runtime as live_note_runtime
import integrations.ghl.highlevel_rest.secret_access_diagnostic as diagnostic


REPO_ROOT = Path(__file__).resolve().parents[4]
WORKFLOW_PATH = (
    REPO_ROOT
    / ".github"
    / "workflows"
    / "nw008-at1-secret-access-diagnostic.yml"
)
IDENTITY_WORKFLOW_PATH = (
    REPO_ROOT / ".github" / "workflows" / "nw008-at1-ghl-identity-diagnostic.yml"
)
HARNESS_PATH = (
    REPO_ROOT
    / "src"
    / "integrations"
    / "ghl"
    / "highlevel_rest"
    / "secret_access_diagnostic.py"
)
TOKEN_SENTINEL = "synthetic-target-token-must-never-render"
SOURCE_CREDENTIAL_SENTINEL = "synthetic-source-credential-must-never-render"
GHL_PAYLOAD_SENTINEL = "synthetic-ghl-payload-must-never-render"
COMMITMENT_PAYLOAD_SENTINEL = "synthetic-commitment-payload-must-never-render"
FAILURE_SENTINEL = "synthetic-access-failure-must-never-render"


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


class _FakeSecretManagerClient:
    def __init__(
        self,
        *,
        payloads: tuple[bytes, bytes] | None = None,
        fail_call: int | None = None,
    ) -> None:
        self.payloads = payloads or (
            GHL_PAYLOAD_SENTINEL.encode(),
            COMMITMENT_PAYLOAD_SENTINEL.encode(),
        )
        self.fail_call = fail_call
        self.calls: list[tuple[dict[str, str], object]] = []

    def access_secret_version(
        self,
        *,
        request: dict[str, str],
        retry: object,
    ) -> object:
        self.calls.append((request, retry))
        call_number = len(self.calls)
        if call_number == self.fail_call:
            raise PermissionDenied(FAILURE_SENTINEL)
        return SimpleNamespace(
            payload=SimpleNamespace(data=self.payloads[call_number - 1])
        )


def _source(principal: str) -> object:
    credentials = type("FakeSourceCredentials", (), {})()
    credentials.token = SOURCE_CREDENTIAL_SENTINEL
    return live_note_runtime._MaterializedWorkflowSource(
        credentials=credentials,
        principal=principal,
    )


def _rendered_result(result: diagnostic.SecretAccessDiagnosticResult) -> str:
    return "\n".join(
        (
            result.render(),
            repr(result),
            json.dumps(result.as_safe_metadata(), sort_keys=True),
        )
    )


def _expected_secret_calls(
    count: int,
) -> list[tuple[dict[str, str], object]]:
    return [
        (
            {"name": diagnostic.GHL_SECRET_VERSION_RESOURCE},
            None,
        ),
        (
            {"name": diagnostic.COMMITMENT_KEY_VERSION_RESOURCE},
            None,
        ),
    ][:count]


def test_exact_access_order_uses_runtime_identity_chain_and_one_refresh(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL)
    target = _FakeTargetCredentials(diagnostic.EXPECTED_TARGET_PRINCIPAL)
    request = object()
    client = _FakeSecretManagerClient()
    effects: dict[str, object] = {
        "source_gate_calls": 0,
        "target_constructor_calls": 0,
        "client_factory_calls": 0,
    }

    def fake_source_gate() -> object:
        effects["source_gate_calls"] = int(effects["source_gate_calls"]) + 1
        return source

    def fake_target_constructor(observed_source: object) -> object:
        effects["target_constructor_calls"] = (
            int(effects["target_constructor_calls"]) + 1
        )
        effects["target_constructor_source"] = observed_source
        return target

    def fake_client_factory(observed_target: object) -> object:
        effects["client_factory_calls"] = int(effects["client_factory_calls"]) + 1
        effects["client_factory_target"] = observed_target
        return client

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

    result = diagnostic.run_secret_access_diagnostic(
        request_factory=lambda: request,
        client_factory=fake_client_factory,
    )

    assert effects == {
        "source_gate_calls": 1,
        "target_constructor_calls": 1,
        "client_factory_calls": 1,
        "target_constructor_source": source,
        "client_factory_target": target,
    }
    assert target.refresh_requests == [request]
    assert client.calls == _expected_secret_calls(2)
    assert result.source_principal_match == "YES"
    assert result.target_principal_match == "YES"
    assert result.target_credential_refresh_attempts == 1
    assert result.ghl_secret_access_attempts == 1
    assert result.commitment_key_access_attempts == 1
    assert result.access_secret_version_calls == 2
    assert diagnostic.EXPECTED_SOURCE_PRINCIPAL == (
        "mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )
    assert diagnostic.EXPECTED_TARGET_PRINCIPAL == (
        "mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )
    assert diagnostic.GHL_SECRET_VERSION_RESOURCE == (
        "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1"
    )
    assert diagnostic.COMMITMENT_KEY_VERSION_RESOURCE == (
        "projects/ai-rolodex-to-crm/secrets/"
        "MG_GUIDE_NW008_COMMITMENT_KEY/versions/1"
    )

    metadata = result.as_safe_metadata()
    assert metadata["GITHUB_OIDC_TO_WORKFLOW"] == "PASS"
    assert metadata["SOURCE_PRINCIPAL_MATCH"] == "YES"
    assert metadata["TARGET_PRINCIPAL_MATCH"] == "YES"
    assert metadata["TARGET_IMPERSONATION_SUCCEEDED"] == "YES"
    assert metadata["GHL_SECRET_ACCESS_ATTEMPTS"] == 1
    assert metadata["GHL_SECRET_PAYLOAD_PRESENT"] == "YES"
    assert metadata["COMMITMENT_KEY_ACCESS_ATTEMPTS"] == 1
    assert metadata["COMMITMENT_KEY_PAYLOAD_PRESENT"] == "YES"
    assert metadata["ACCESS_SECRET_VERSION_CALLS"] == 2
    assert metadata["NO_UNEXPECTED_RETRY"] == "YES"
    assert metadata["GHL_REQUESTS"] == 0
    assert metadata["GHL_REST_CALLS"] == 0
    assert metadata["CRM_CALLS"] == 0
    assert metadata["CRM_OPERATIONS"] == 0
    assert metadata["CRM_MUTATIONS"] == 0
    assert metadata["MUTATIONS"] == 0
    assert metadata["IAM_MUTATIONS"] == 0
    assert metadata["SECRET_MUTATIONS"] == 0
    for safety_field in (
        "SECRET_VALUE_PUBLISHED",
        "SECRET_VALUE_PERSISTED",
        "SECRET_VALUE_LOGGED",
        "SECRET_VALUE_ECHOED",
        "SECRET_VALUE_HASHED_FOR_PROOF",
        "SECRET_VALUE_LENGTH_RECORDED",
        "SECRET_PAYLOAD_RETURNED",
        "TOKEN_OR_CREDENTIAL_VALUE_PUBLISHED",
    ):
        assert metadata[safety_field] == "NO"

    rendered = _rendered_result(result)
    for sentinel in (
        TOKEN_SENTINEL,
        SOURCE_CREDENTIAL_SENTINEL,
        GHL_PAYLOAD_SENTINEL,
        COMMITMENT_PAYLOAD_SENTINEL,
    ):
        assert sentinel not in rendered


def test_source_mismatch_stops_before_target_refresh_or_secret_client() -> None:
    effects = {"target_constructions": 0, "client_constructions": 0}

    def unexpected_target_constructor(source: object) -> object:
        effects["target_constructions"] += 1
        raise AssertionError("source mismatch must stop target construction")

    def unexpected_client_factory(target: object) -> object:
        effects["client_constructions"] += 1
        raise AssertionError("source mismatch must stop client construction")

    with pytest.raises(diagnostic.SecretAccessDiagnosticError) as failure:
        diagnostic.run_secret_access_diagnostic(
            source_gate=lambda: _source("unrelated@example.invalid"),
            target_credentials_constructor=unexpected_target_constructor,
            request_factory=lambda: object(),
            client_factory=unexpected_client_factory,
        )

    result = failure.value.result
    assert result.source_principal_match == "NO"
    assert result.target_credential_refresh_attempts == 0
    assert result.access_secret_version_calls == 0
    assert result.stop == "SOURCE_PRINCIPAL_MISMATCH"
    assert effects == {"target_constructions": 0, "client_constructions": 0}


def test_target_mismatch_stops_before_refresh_or_secret_client() -> None:
    target = _FakeTargetCredentials("unrelated@example.invalid")
    client_constructions = 0

    def unexpected_client_factory(observed_target: object) -> object:
        nonlocal client_constructions
        client_constructions += 1
        raise AssertionError("target mismatch must stop client construction")

    with pytest.raises(diagnostic.SecretAccessDiagnosticError) as failure:
        diagnostic.run_secret_access_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=lambda: object(),
            client_factory=unexpected_client_factory,
        )

    result = failure.value.result
    assert result.target_principal_match == "NO"
    assert result.target_credential_refresh_attempts == 0
    assert result.access_secret_version_calls == 0
    assert result.stop == "TARGET_PRINCIPAL_MISMATCH"
    assert target.refresh_requests == []
    assert client_constructions == 0


def test_target_refresh_failure_is_one_shot_and_stops_secret_access() -> None:
    target = _FakeTargetCredentials(
        diagnostic.EXPECTED_TARGET_PRINCIPAL,
        fail_refresh=True,
    )
    request = object()
    client_constructions = 0

    def unexpected_client_factory(observed_target: object) -> object:
        nonlocal client_constructions
        client_constructions += 1
        raise AssertionError("refresh failure must stop client construction")

    with pytest.raises(diagnostic.SecretAccessDiagnosticError) as failure:
        diagnostic.run_secret_access_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=lambda: request,
            client_factory=unexpected_client_factory,
        )

    result = failure.value.result
    assert target.refresh_requests == [request]
    assert client_constructions == 0
    assert result.target_credential_refresh_attempts == 1
    assert result.target_credential_refresh_result == "FAIL"
    assert result.access_secret_version_calls == 0
    assert result.stop == "TARGET_CREDENTIAL_REFRESH_FAILED"
    assert TOKEN_SENTINEL not in f"{failure.value}\n{_rendered_result(result)}"


@pytest.mark.parametrize(
    ("fail_call", "expected_stop"),
    (
        (1, "GHL_SECRET_ACCESS_FAILED"),
        (2, "COMMITMENT_KEY_ACCESS_FAILED"),
    ),
)
def test_access_failure_stops_at_failed_call_without_retry(
    fail_call: int,
    expected_stop: str,
) -> None:
    target = _FakeTargetCredentials(diagnostic.EXPECTED_TARGET_PRINCIPAL)
    request = object()
    client = _FakeSecretManagerClient(fail_call=fail_call)

    with pytest.raises(diagnostic.SecretAccessDiagnosticError) as failure:
        diagnostic.run_secret_access_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=lambda: request,
            client_factory=lambda credentials: client,
        )

    result = failure.value.result
    assert target.refresh_requests == [request]
    assert client.calls == _expected_secret_calls(fail_call)
    assert result.ghl_secret_access_attempts == 1
    assert result.commitment_key_access_attempts == fail_call - 1
    assert result.access_secret_version_calls == fail_call
    assert result.stop == expected_stop
    assert result.as_safe_metadata()["NO_UNEXPECTED_RETRY"] == "YES"
    rendered = f"{failure.value}\n{_rendered_result(result)}"
    for sentinel in (
        TOKEN_SENTINEL,
        SOURCE_CREDENTIAL_SENTINEL,
        GHL_PAYLOAD_SENTINEL,
        COMMITMENT_PAYLOAD_SENTINEL,
        FAILURE_SENTINEL,
    ):
        assert sentinel not in rendered


@pytest.mark.parametrize(
    ("payloads", "expected_calls", "expected_stop"),
    (
        (
            (b"", COMMITMENT_PAYLOAD_SENTINEL.encode()),
            1,
            "GHL_SECRET_PAYLOAD_MISSING",
        ),
        (
            (GHL_PAYLOAD_SENTINEL.encode(), b""),
            2,
            "COMMITMENT_KEY_PAYLOAD_MISSING",
        ),
    ),
)
def test_empty_payload_fails_closed_without_another_attempt(
    payloads: tuple[bytes, bytes],
    expected_calls: int,
    expected_stop: str,
) -> None:
    target = _FakeTargetCredentials(diagnostic.EXPECTED_TARGET_PRINCIPAL)
    client = _FakeSecretManagerClient(payloads=payloads)

    with pytest.raises(diagnostic.SecretAccessDiagnosticError) as failure:
        diagnostic.run_secret_access_diagnostic(
            source_gate=lambda: _source(diagnostic.EXPECTED_SOURCE_PRINCIPAL),
            target_credentials_constructor=lambda source: target,
            request_factory=lambda: object(),
            client_factory=lambda credentials: client,
        )

    result = failure.value.result
    assert client.calls == _expected_secret_calls(expected_calls)
    assert result.access_secret_version_calls == expected_calls
    assert result.stop == expected_stop


def test_static_workflow_contract_matches_identity_auth_bridge_and_cleanup() -> None:
    raw_workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.load(raw_workflow, Loader=yaml.BaseLoader)
    identity_workflow = yaml.load(
        IDENTITY_WORKFLOW_PATH.read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )

    assert workflow["on"] == {"workflow_dispatch": {}}
    assert workflow["permissions"] == {
        "contents": "read",
        "id-token": "write",
    }
    assert list(workflow["jobs"]) == ["secret-access-diagnostic"]
    steps = workflow["jobs"]["secret-access-diagnostic"]["steps"]
    identity_steps = identity_workflow["jobs"]["workflow-identity-diagnostic"][
        "steps"
    ]

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

    harness_index, harness_step = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("run")
        == "python -m integrations.ghl.highlevel_rest.secret_access_diagnostic"
    )
    assert harness_step["env"] == {
        "MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG": (
            "${{ steps.auth.outputs.credentials_file_path }}"
        ),
        "PYTHONPATH": "src",
    }

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
    assert auth_index < harness_index < delete_index < verify_index

    for cleanup_name, cleanup_step in (
        ("Delete auth credential file", delete_step),
        ("Verify auth credential file is absent", verify_step),
    ):
        identity_cleanup_step = next(
            step for step in identity_steps if step.get("name") == cleanup_name
        )
        assert cleanup_step == identity_cleanup_step

    assert "secrets." not in raw_workflow
    assert "GOOGLE_GHA_CREDS_PATH" not in raw_workflow
    assert "GOOGLE_APPLICATION_CREDENTIALS" not in raw_workflow


def test_harness_static_contract_has_no_payload_transform_or_ghl_path() -> None:
    source = HARNESS_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)

    assert 'importlib.import_module("google.cloud.secretmanager")' in source
    assert "secretmanager_module.SecretManagerServiceClient(" in source
    assert "credentials=target_runtime_credentials" in source
    assert "retry=None" in source
    assert ".decode(" not in source
    assert "hashlib" not in source
    assert "base64" not in source
    assert "google.auth.default" not in source

    forbidden_call_names = {"len", "hash", "open"}
    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        if isinstance(call.func, ast.Name):
            assert call.func.id not in forbidden_call_names

    for forbidden_path in (
        "ConcreteLiveNoteHttpClient",
        "live_note_http_client",
        "assemble_bound_live_note_runtime",
        "services.leadconnectorhq.com",
        "subprocess",
        "urllib",
        "http.client",
    ):
        assert forbidden_path not in source

    for handler in (
        node for node in ast.walk(tree) if isinstance(node, ast.ExceptHandler)
    ):
        assert handler.type is not None
        caught_names = {
            node.id for node in ast.walk(handler.type) if isinstance(node, ast.Name)
        }
        assert "Exception" not in caught_names
        assert "BaseException" not in caught_names
