from __future__ import annotations

import ast
import logging
import os
import subprocess
from pathlib import Path

import pytest

from integrations.ghl.highlevel_rest.live_note_credential_provider import (
    LiveNoteCredentialProvider,
    LiveNoteCredentialProviderError,
    SyntheticLiveNoteSecretAccessor,
)
from integrations.ghl.highlevel_rest.live_note_transport import (
    AMBIGUITY_TRUTH,
    AUTOMATIC_RETRY,
    InjectedLiveNoteCredential,
    POST_ATTEMPTS_MAX,
    REQUEST_TIMEOUT_SECONDS,
    TOTAL_MUTATION_CALLS_MAX,
    TOTAL_NETWORK_CALLS_MAX,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"
PROVIDER_PATH = SOURCE_ROOT / "live_note_credential_provider.py"
HTTP_CLIENT_PATH = SOURCE_ROOT / "live_note_http_client.py"
TRANSPORT_PATH = SOURCE_ROOT / "live_note_transport.py"
NOTE_PATH_PATH = SOURCE_ROOT / "note_path.py"

SYNTHETIC_RESOURCE = (
    "projects/synthetic-project/secrets/ghl-rest-note-token/versions/latest"
)
SYNTHETIC_TOKEN = "synthetic-placeholder-token-at8i-credential"


def _provider(
    *,
    token: str = SYNTHETIC_TOKEN,
    resource_name: str = SYNTHETIC_RESOURCE,
) -> tuple[LiveNoteCredentialProvider, SyntheticLiveNoteSecretAccessor]:
    accessor = SyntheticLiveNoteSecretAccessor(
        payloads={resource_name: token},
    )
    provider = LiveNoteCredentialProvider(
        accessor=accessor,
        resource_name=resource_name,
    )
    return provider, accessor


def test_credential_provider_injectable() -> None:
    provider, accessor = _provider()

    credential = provider.get_credential()

    assert isinstance(credential, InjectedLiveNoteCredential)
    assert credential.bearer_token == SYNTHETIC_TOKEN
    assert accessor.synthetic_read_count == 1
    assert provider.acquire_count == 1
    assert provider.resource_name == SYNTHETIC_RESOURCE


def test_credential_provider_synthetic_only() -> None:
    provider, accessor = _provider()
    credential = provider.get_credential()

    assert isinstance(credential, InjectedLiveNoteCredential)
    assert accessor.SECRET_PAYLOAD_READS_ARE_SYNTHETIC is True
    assert accessor.REAL_SECRET_READS == 0
    assert LiveNoteCredentialProvider.REAL_SECRET_READS_AUTHORIZED is False
    assert LiveNoteCredentialProvider.REAL_CREDENTIAL_USE_AUTHORIZED is False
    assert LiveNoteCredentialProvider.ENVIRONMENT_TOKEN_DISCOVERY is False
    assert LiveNoteCredentialProvider.GCLOUD_SUBPROCESS_SECRET_ACCESS is False
    assert LiveNoteCredentialProvider.SHELL_SECRET_ACCESS is False
    assert LiveNoteCredentialProvider.CONCRETE_SECRET_MANAGER_NETWORK_CLIENT is False

    tree = ast.parse(PROVIDER_PATH.read_text(encoding="utf-8"))
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.add(node.module)
    joined = "\n".join(sorted(imported_modules)).lower()
    assert "google.cloud" not in joined
    assert "secretmanager" not in joined
    assert "subprocess" not in joined
    assert "os" not in imported_modules
    source = PROVIDER_PATH.read_text(encoding="utf-8")
    assert "os.environ" not in source
    assert "getenv(" not in source


def test_zero_real_secret_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    def _forbid_subprocess(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("gcloud/shell secret access is forbidden in AT8I")

    def _forbid_getenv(key: str, default: object = None) -> object:
        if "TOKEN" in key.upper() or "SECRET" in key.upper() or "GHL" in key.upper():
            raise AssertionError(f"environment secret discovery forbidden: {key}")
        return default

    monkeypatch.setattr(subprocess, "run", _forbid_subprocess)
    monkeypatch.setattr(subprocess, "Popen", _forbid_subprocess)
    monkeypatch.setattr(subprocess, "call", _forbid_subprocess)
    monkeypatch.setattr(subprocess, "check_output", _forbid_subprocess)
    monkeypatch.setattr(os, "getenv", _forbid_getenv)
    monkeypatch.delenv("GHL_TOKEN", raising=False)
    monkeypatch.delenv("HIGHLEVEL_TOKEN", raising=False)

    # Ensure google-cloud-secretmanager is not importable/used by provider path.
    import sys

    for name in list(sys.modules):
        if name.startswith("google.cloud.secretmanager") or name == "google.cloud":
            monkeypatch.delitem(sys.modules, name, raising=False)

    provider, accessor = _provider()
    credential = provider.get_credential()
    assert credential.bearer_token == SYNTHETIC_TOKEN
    assert accessor.REAL_SECRET_READS == 0
    assert accessor.synthetic_read_count == 1


def test_token_not_logged(caplog: pytest.LogCaptureFixture) -> None:
    provider, accessor = _provider()
    with caplog.at_level(logging.DEBUG):
        credential = provider.get_credential()

    rendered = "\n".join(
        [
            repr(provider),
            str(provider),
            repr(accessor),
            str(accessor),
            repr(credential),
            str(credential),
            caplog.text,
        ]
    )
    assert SYNTHETIC_TOKEN not in rendered
    assert "Bearer " not in rendered
    assert credential.bearer_token == SYNTHETIC_TOKEN


def test_authorization_header_not_logged(caplog: pytest.LogCaptureFixture) -> None:
    provider, _accessor = _provider()
    with caplog.at_level(logging.DEBUG):
        credential = provider.get_credential()

    haystack = "\n".join(
        [repr(provider), str(provider), repr(credential), str(credential), caplog.text]
    )
    assert "Authorization" not in haystack
    assert "authorization" not in haystack.lower()


def test_provider_rejects_empty_payload() -> None:
    accessor = SyntheticLiveNoteSecretAccessor(payloads={SYNTHETIC_RESOURCE: "   "})
    provider = LiveNoteCredentialProvider(
        accessor=accessor,
        resource_name=SYNTHETIC_RESOURCE,
    )
    with pytest.raises(LiveNoteCredentialProviderError, match="empty"):
        provider.get_credential()


def test_provider_requires_accessor_and_resource() -> None:
    accessor = SyntheticLiveNoteSecretAccessor(
        payloads={SYNTHETIC_RESOURCE: SYNTHETIC_TOKEN}
    )
    with pytest.raises(LiveNoteCredentialProviderError, match="resource_name"):
        LiveNoteCredentialProvider(accessor=accessor, resource_name="")
    with pytest.raises(LiveNoteCredentialProviderError, match="accessor"):
        LiveNoteCredentialProvider(accessor=None, resource_name=SYNTHETIC_RESOURCE)  # type: ignore[arg-type]


def test_provider_module_import_policy() -> None:
    forbidden = {
        "google",
        "google.cloud",
        "secretmanager",
        "subprocess",
        "requests",
        "httpx",
        "aiohttp",
    }
    tree = ast.parse(PROVIDER_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name for alias in node.names}
            assert not names & forbidden
            roots = {name.split(".", 1)[0] for name in names}
            assert "subprocess" not in roots
            assert "google" not in roots
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            assert not module.startswith("google")
            assert module.split(".", 1)[0] not in {"subprocess", "requests", "httpx"}


def test_private_target_boundary_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "_trust_marker" in source
    assert "private_at8_verified_binding_handoff" in source
    provider_source = PROVIDER_PATH.read_text(encoding="utf-8")
    assert "_trust_marker" not in provider_source
    assert "VerifiedContactBindingCapability" not in provider_source
    assert "contact_id" not in provider_source


def test_caller_target_override_forbidden() -> None:
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "POST path is not the bound-contact notes route" in transport_source
    provider_source = PROVIDER_PATH.read_text(encoding="utf-8")
    assert "bound_contact_id" not in provider_source
    assert "location_id" not in provider_source


def test_at8h_transport_caps_unchanged() -> None:
    assert POST_ATTEMPTS_MAX == 1
    assert TOTAL_NETWORK_CALLS_MAX == 2
    assert TOTAL_MUTATION_CALLS_MAX == 1
    assert REQUEST_TIMEOUT_SECONDS == 10.0
    assert AUTOMATIC_RETRY is False
    assert HTTP_CLIENT_PATH.is_file()
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert "REQUEST_TIMEOUT_SECONDS = 10.0" in transport_source


def test_at8g_reservation_contract_unchanged() -> None:
    source = NOTE_PATH_PATH.read_text(encoding="utf-8")
    assert "NOTE_CREATE_OPERATION_ORDINAL = 1" in source
    assert '_GRANT_RUN_ID_PREFIX = "npgr1:"' in source
    assert "mark_dispatched" in source
    assert 'business_effect_truth="UNKNOWN"' in source


def test_ambiguity_no_retry_unchanged() -> None:
    assert AMBIGUITY_TRUTH == "UNKNOWN"
    assert AUTOMATIC_RETRY is False
    transport_source = TRANSPORT_PATH.read_text(encoding="utf-8")
    assert 'AMBIGUITY_TRUTH = "UNKNOWN"' in transport_source
    assert "SECOND_POST = False" in transport_source
