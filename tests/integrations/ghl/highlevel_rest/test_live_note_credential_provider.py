from __future__ import annotations

import ast
import logging
from types import SimpleNamespace
from pathlib import Path

import pytest

from integrations.ghl.highlevel_rest.live_note_credential_provider import (
    DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE,
    GoogleSecretManagerLiveNoteSecretAccessor,
    LiveNoteCredentialProvider,
    LiveNoteCredentialProviderError,
    RootOwnedLiveNoteCredentialInjection,
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


class _FakeSecretManagerClient:
    def __init__(self, payload: bytes = b"fake-production-token") -> None:
        self.payload = payload
        self.request_names: list[str] = []

    def access_secret_version(self, *, request: dict[str, str]) -> SimpleNamespace:
        self.request_names.append(request["name"])
        return SimpleNamespace(payload=SimpleNamespace(data=self.payload))


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


def test_credential_provider_synthetic_accessor_remains_offline() -> None:
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
    assert "subprocess" not in joined
    assert "os" not in imported_modules
    source = PROVIDER_PATH.read_text(encoding="utf-8")
    assert "os.environ" not in source
    assert "getenv(" not in source


def test_root_owned_injection_builds_provider_from_synthetic_accessor() -> None:
    accessor = SyntheticLiveNoteSecretAccessor(
        payloads={SYNTHETIC_RESOURCE: SYNTHETIC_TOKEN}
    )
    injection = RootOwnedLiveNoteCredentialInjection(
        accessor=accessor,
        resource_name=SYNTHETIC_RESOURCE,
    )

    provider = injection.build_provider()

    assert accessor.synthetic_read_count == 0
    assert provider.get_credential().bearer_token == SYNTHETIC_TOKEN
    assert accessor.synthetic_read_count == 1
    assert SYNTHETIC_RESOURCE not in repr(injection)
    assert SYNTHETIC_TOKEN not in repr(injection)


def test_root_owned_injection_rejects_missing_accessor_or_resource() -> None:
    accessor = SyntheticLiveNoteSecretAccessor(
        payloads={SYNTHETIC_RESOURCE: SYNTHETIC_TOKEN}
    )

    with pytest.raises(LiveNoteCredentialProviderError, match="accessor"):
        RootOwnedLiveNoteCredentialInjection(
            accessor=None,  # type: ignore[arg-type]
            resource_name=SYNTHETIC_RESOURCE,
        )
    with pytest.raises(LiveNoteCredentialProviderError, match="resource_name"):
        RootOwnedLiveNoteCredentialInjection(accessor=accessor, resource_name="")


def test_production_accessor_is_fixed_to_designated_version_and_uses_fake_client() -> None:
    client = _FakeSecretManagerClient()
    accessor = GoogleSecretManagerLiveNoteSecretAccessor(client=client)

    assert accessor.resource_name == DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE
    assert accessor.version_resource == DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE
    assert accessor.read_secret_payload(
        resource_name=DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE
    ) == "fake-production-token"
    assert client.request_names == [DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE]
    assert accessor.REAL_SECRET_READS == 1


@pytest.mark.parametrize(
    "resource_name",
    [
        "projects/831270426395/secrets/MG_GUIDE_PIT_GHL",
        "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/latest",
        "projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/2",
        "projects/831270426395/secrets/OTHER/versions/1",
    ],
)
def test_production_accessor_rejects_non_designated_resource(
    resource_name: str,
) -> None:
    accessor = GoogleSecretManagerLiveNoteSecretAccessor(
        client=_FakeSecretManagerClient()
    )

    with pytest.raises(LiveNoteCredentialProviderError, match="root-owned"):
        accessor.read_secret_payload(resource_name=resource_name)


def test_production_accessor_has_no_resource_or_version_override() -> None:
    with pytest.raises(TypeError):
        GoogleSecretManagerLiveNoteSecretAccessor(
            resource_name=DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE
        )
    with pytest.raises(TypeError):
        GoogleSecretManagerLiveNoteSecretAccessor(
            version_resource=DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE
        )


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
    source = PROVIDER_PATH.read_text(encoding="utf-8")
    assert "importlib.import_module" in source
    assert "import google" not in source


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
