from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from integrations.ghl import At1ExecutionStore
from integrations.ghl.at1_commitment_key_provider import (
    DESIGNATED_COMMITMENT_KEY_VERSION_RESOURCE,
    SyntheticCommitmentKeyProvider,
)
import integrations.ghl.highlevel_rest.live_note_runtime as runtime
import integrations.ghl.highlevel_rest.note_path as note_path_module
from integrations.ghl.highlevel_rest import NotePathAdapter, assemble_bound_live_note_runtime
from integrations.ghl.highlevel_rest.live_note_credential_provider import (
    RootOwnedLiveNoteCredentialInjection,
    SyntheticLiveNoteSecretAccessor,
)
from integrations.ghl.highlevel_rest.note_path import BindingError


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"
CONSUMER_IDENTITY = (
    "NW008_AT8L_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_IMPLEMENTATION_001"
)
_VERSION_RESOURCE = "projects/synthetic-project/secrets/at1-commitment-key/versions/1"


@pytest.fixture(autouse=True)
def _reset_shared_ledger() -> None:
    note_path_module._reset_shared_test_ledger()


@pytest.fixture
def execution_store(tmp_path: Path) -> At1ExecutionStore:
    return At1ExecutionStore(
        db_path=tmp_path / "live-note-runtime.sqlite3",
        commitment_material=SyntheticCommitmentKeyProvider(
            payload="synthetic-live-note-runtime-commitment-key",
            version_resource=_VERSION_RESOURCE,
        ).resolve(),
    )


def _issued_capability(
    *,
    location_id: str = "synthetic-location-001",
    contact_id: str = "synthetic-contact-001",
    consumer_authorization_identity: str = CONSUMER_IDENTITY,
    consumer_workflow_run_id: str = "synthetic-workflow-run-at8l-001",
):
    return NotePathAdapter._build_at8_shaped_test_capability(
        location_id=location_id,
        contact_id=contact_id,
        consumer_authorization_identity=consumer_authorization_identity,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )


def _root_owned_private_delivery_capability(
    *,
    consumer_workflow_run_id: str = "synthetic-workflow-run-root-owned-runtime-001",
):
    trusted_binding_source = NotePathAdapter._build_private_at8_verified_binding_source(
        location_id="synthetic-location-001",
        contact_id="synthetic-contact-001",
    )
    reference = note_path_module._register_root_owned_private_binding_delivery_reference(
        trusted_binding_source=trusted_binding_source
    )
    return note_path_module._issue_root_owned_private_binding_delivery_capability(
        safe_private_delivery_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=consumer_workflow_run_id,
    )


def _synthetic_accessor() -> SyntheticLiveNoteSecretAccessor:
    return SyntheticLiveNoteSecretAccessor(
        payloads={
            runtime._SEALED_LIVE_NOTE_REST_RESOURCE_NAME: (
                "synthetic-live-note-runtime-token"
            )
        }
    )


def test_public_assembler_accepts_only_verified_capability() -> None:
    signature = inspect.signature(assemble_bound_live_note_runtime)

    assert tuple(signature.parameters) == ("verified_capability",)
    assert signature.parameters["verified_capability"].kind is inspect.Parameter.KEYWORD_ONLY

    capability = _issued_capability()
    for forbidden_name in (
        "contact_id",
        "location_id",
        "resource_name",
        "bearer_token",
        "credential",
        "http_client",
        "base_url",
        "url",
        "host",
        "route",
        "headers",
        "authorization",
        "secret_payload",
        "execution_store",
    ):
        with pytest.raises(TypeError):
            assemble_bound_live_note_runtime(
                verified_capability=capability,
                **{forbidden_name: "caller-override"},
            )


def test_public_assembler_requires_process_issued_capability() -> None:
    with pytest.raises(BindingError):
        assemble_bound_live_note_runtime(verified_capability=None)

    forged_capability = _issued_capability()
    object.__setattr__(forged_capability, "contact_id", "forged-contact-001")
    with pytest.raises(BindingError):
        assemble_bound_live_note_runtime(verified_capability=forged_capability)


def test_public_assembler_uses_existing_validator_before_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capability = _issued_capability()
    validator_calls: list[tuple[object, dict[str, object]]] = []

    def _validator(submitted: object, **kwargs: object) -> object:
        validator_calls.append((submitted, kwargs))
        return submitted

    monkeypatch.setattr(note_path_module, "_require_issued_verified_capability", _validator)

    with pytest.raises(
        runtime.LiveNoteRuntimeAssemblyError, match="root-owned dependencies"
    ):
        assemble_bound_live_note_runtime(verified_capability=capability)

    assert validator_calls == [
        (
            capability,
            {
                "location_id": capability.location_id,
                "contact_id": capability.contact_id,
                "consumer_authorization_identity": (
                    capability.consumer_authorization_identity
                ),
                "consumer_workflow_run_id": capability.consumer_workflow_run_id,
            },
        )
    ]


def test_missing_root_owned_config_fails_closed_before_runtime_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    capability = _issued_capability()

    def _unexpected_construction(*args: object, **kwargs: object) -> None:
        raise AssertionError("missing root-owned configuration must stop assembly")

    monkeypatch.setattr(runtime, "ConcreteLiveNoteHttpClient", _unexpected_construction)
    monkeypatch.setattr(runtime, "LiveNoteCredentialProvider", _unexpected_construction)
    monkeypatch.setattr(runtime, "BoundedLiveNoteTransport", _unexpected_construction)
    monkeypatch.setattr(runtime, "NotePathAdapter", _unexpected_construction)

    with pytest.raises(
        runtime.LiveNoteRuntimeAssemblyError, match="root-owned dependencies"
    ):
        assemble_bound_live_note_runtime(verified_capability=capability)


def test_root_owned_resolver_uses_process_environment_and_fixed_dependencies(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    db_path = tmp_path / "root-owned.sqlite3"
    constructed: dict[str, object] = {}
    source_credentials = object()
    target_runtime_credentials = object()
    shared_secret_manager_client = object()

    class _FakeCommitmentKeyProvider:
        def __init__(self, *, client: object) -> None:
            constructed["provider"] = self
            constructed["provider_client"] = client

        def resolve(self):
            return SyntheticCommitmentKeyProvider(
                payload="root-owned-test-commitment-key",
                version_resource=DESIGNATED_COMMITMENT_KEY_VERSION_RESOURCE,
            ).resolve()

    class _FakeLiveNoteSecretAccessor:
        def __init__(self, *, client: object) -> None:
            constructed["accessor"] = self
            constructed["accessor_client"] = client

        def read_secret_payload(self, *, resource_name: str) -> str:
            raise AssertionError("credential acquisition is outside resolver assembly")

    def _impersonate(source: object) -> object:
        constructed["impersonation_source"] = source
        return target_runtime_credentials

    def _new_client(credentials: object) -> object:
        constructed["client_credentials"] = credentials
        return shared_secret_manager_client

    monkeypatch.setenv(runtime._ROOT_OWNED_DB_CONFIG_KEY, str(db_path))
    monkeypatch.setattr(
        runtime,
        "_resolve_source_application_credentials",
        lambda: source_credentials,
    )
    monkeypatch.setattr(
        runtime,
        "_impersonate_target_runtime_credentials",
        _impersonate,
    )
    monkeypatch.setattr(
        runtime,
        "_new_secret_manager_client",
        _new_client,
    )
    monkeypatch.setattr(
        runtime, "GoogleSecretManagerCommitmentKeyProvider", _FakeCommitmentKeyProvider
    )
    monkeypatch.setattr(
        runtime, "GoogleSecretManagerLiveNoteSecretAccessor", _FakeLiveNoteSecretAccessor
    )

    dependencies = runtime._resolve_root_owned_runtime_dependencies()

    assert isinstance(dependencies.execution_store, At1ExecutionStore)
    assert dependencies.execution_store.db_path == str(db_path)
    assert dependencies.credential_injection.build_provider().resource_name == (
        runtime._SEALED_LIVE_NOTE_REST_RESOURCE_NAME
    )
    assert constructed["impersonation_source"] is source_credentials
    assert constructed["client_credentials"] is target_runtime_credentials
    assert constructed["provider_client"] is shared_secret_manager_client
    assert constructed["accessor_client"] is shared_secret_manager_client
    dependencies.execution_store._connection.close()


class _CloseTrackingConnection:
    def __init__(self) -> None:
        self.close_events = 0

    def close(self) -> None:
        self.close_events += 1


class _SyntheticLifecycleStore(At1ExecutionStore):
    def __init__(self) -> None:
        self._connection = _CloseTrackingConnection()
        self.execution_claims_created = 0
        self.attempt_records_created = 0
        self.protocol_ledger_event_writes = 0
        self.business_ledger_event_writes = 0


class _LifecycleSecretAccessor:
    def __init__(self, *, fails: bool) -> None:
        self.fails = fails
        self.read_count = 0

    def read_secret_payload(self, *, resource_name: str) -> str:
        self.read_count += 1
        if self.fails:
            raise RuntimeError("synthetic B2 acquisition failure")
        return "synthetic-live-note-runtime-token"


def _lifecycle_dependencies(
    *, fails_during_b2_acquisition: bool
) -> tuple[
    runtime._RootOwnedLiveNoteRuntimeDependencies,
    _SyntheticLifecycleStore,
    _LifecycleSecretAccessor,
]:
    store = _SyntheticLifecycleStore()
    accessor = _LifecycleSecretAccessor(fails=fails_during_b2_acquisition)
    dependencies = runtime._RootOwnedLiveNoteRuntimeDependencies(
        credential_injection=RootOwnedLiveNoteCredentialInjection(
            accessor=accessor,
            resource_name=runtime._SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
        ),
        execution_store=store,
    )
    return dependencies, store, accessor


@pytest.mark.parametrize(
    "failure_stage",
    (
        "b2_secret_acquisition",
        "http_client_construction",
        "transport_construction",
        "adapter_construction",
    ),
)
def test_root_owned_store_closes_after_each_pre_return_failure(
    monkeypatch: pytest.MonkeyPatch, failure_stage: str
) -> None:
    dependencies, store, accessor = _lifecycle_dependencies(
        fails_during_b2_acquisition=failure_stage == "b2_secret_acquisition"
    )
    effects = {"http": 0, "transport": 0, "adapter": 0}

    def _http_client() -> object:
        effects["http"] += 1
        if failure_stage == "http_client_construction":
            raise RuntimeError("synthetic HTTP client construction failure")
        return object()

    def _transport(**kwargs: object) -> object:
        effects["transport"] += 1
        if failure_stage == "transport_construction":
            raise RuntimeError("synthetic transport construction failure")
        return object()

    class _Adapter:
        def __init__(self, **kwargs: object) -> None:
            effects["adapter"] += 1
            if failure_stage == "adapter_construction":
                raise RuntimeError("synthetic adapter construction failure")
            self.execution_store = kwargs["execution_store"]

    monkeypatch.setattr(
        runtime, "_resolve_root_owned_runtime_dependencies", lambda: dependencies
    )
    monkeypatch.setattr(runtime, "ConcreteLiveNoteHttpClient", _http_client)
    monkeypatch.setattr(runtime, "BoundedLiveNoteTransport", _transport)
    monkeypatch.setattr(runtime, "NotePathAdapter", _Adapter)

    with pytest.raises(RuntimeError, match="synthetic"):
        assemble_bound_live_note_runtime(
            verified_capability=_root_owned_private_delivery_capability()
        )

    assert store._connection.close_events == 1
    assert accessor.read_count == 1
    assert effects["http"] == (
        0 if failure_stage == "b2_secret_acquisition" else 1
    )
    assert effects["transport"] == (
        0
        if failure_stage in ("b2_secret_acquisition", "http_client_construction")
        else 1
    )
    assert effects["adapter"] == (1 if failure_stage == "adapter_construction" else 0)
    assert store.execution_claims_created == 0
    assert store.attempt_records_created == 0
    assert store.protocol_ledger_event_writes == 0
    assert store.business_ledger_event_writes == 0


def test_root_owned_store_transfers_only_after_successful_adapter_return(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dependencies, store, accessor = _lifecycle_dependencies(
        fails_during_b2_acquisition=False
    )
    effects = {"http": 0, "transport": 0, "adapter": 0}

    def _http_client() -> object:
        effects["http"] += 1
        return object()

    def _transport(**kwargs: object) -> object:
        effects["transport"] += 1
        return object()

    class _Adapter:
        def __init__(self, **kwargs: object) -> None:
            effects["adapter"] += 1
            self.execution_store = kwargs["execution_store"]

    monkeypatch.setattr(
        runtime, "_resolve_root_owned_runtime_dependencies", lambda: dependencies
    )
    monkeypatch.setattr(runtime, "ConcreteLiveNoteHttpClient", _http_client)
    monkeypatch.setattr(runtime, "BoundedLiveNoteTransport", _transport)
    monkeypatch.setattr(runtime, "NotePathAdapter", _Adapter)

    adapter = assemble_bound_live_note_runtime(
        verified_capability=_root_owned_private_delivery_capability()
    )

    assert adapter.execution_store is store
    assert store._connection.close_events == 0
    assert accessor.read_count == 1
    assert effects == {"http": 1, "transport": 1, "adapter": 1}
    assert store.execution_claims_created == 0
    assert store.attempt_records_created == 0
    assert store.protocol_ledger_event_writes == 0
    assert store.business_ledger_event_writes == 0


def test_public_assembler_uses_only_root_owned_dependencies(
    execution_store: At1ExecutionStore,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    accessor = _synthetic_accessor()
    dependencies = runtime._RootOwnedLiveNoteRuntimeDependencies(
        credential_injection=RootOwnedLiveNoteCredentialInjection(
            accessor=accessor,
            resource_name=runtime._SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
        ),
        execution_store=execution_store,
    )
    monkeypatch.setattr(
        runtime,
        "_resolve_root_owned_runtime_dependencies",
        lambda: dependencies,
    )

    adapter = assemble_bound_live_note_runtime(
        verified_capability=_root_owned_private_delivery_capability()
    )
    transport = adapter._transport

    assert isinstance(adapter, NotePathAdapter)
    assert adapter._verified_contact_binding_capability is not None
    assert transport.total_network_calls == 0
    assert transport.post_attempts == 0
    assert transport.get_attempts == 0
    assert transport._http_client.call_history == ()
    assert accessor.REAL_SECRET_READS == 0
    assert accessor.synthetic_read_count == 1


def test_root_owned_dependency_container_rejects_overrides(
    execution_store: At1ExecutionStore,
) -> None:
    injection = RootOwnedLiveNoteCredentialInjection(
        accessor=_synthetic_accessor(),
        resource_name=runtime._SEALED_LIVE_NOTE_REST_RESOURCE_NAME,
    )

    with pytest.raises(runtime.LiveNoteRuntimeAssemblyError, match="credential"):
        runtime._RootOwnedLiveNoteRuntimeDependencies(
            credential_injection=object(),  # type: ignore[arg-type]
            execution_store=execution_store,
        )
    with pytest.raises(runtime.LiveNoteRuntimeAssemblyError, match="execution store"):
        runtime._RootOwnedLiveNoteRuntimeDependencies(
            credential_injection=injection,
            execution_store=object(),  # type: ignore[arg-type]
        )


def test_private_test_seam_has_only_synthetic_accessor_and_store_args() -> None:
    signature = inspect.signature(runtime._assemble_bound_live_note_runtime_for_tests)

    assert tuple(signature.parameters) == (
        "verified_capability",
        "synthetic_secret_accessor",
        "execution_store",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


def test_private_test_seam_rejects_non_synthetic_accessor_and_store(
    execution_store: At1ExecutionStore,
) -> None:
    capability = _issued_capability()

    with pytest.raises(runtime.LiveNoteRuntimeAssemblyError, match="synthetic_secret_accessor"):
        runtime._assemble_bound_live_note_runtime_for_tests(
            verified_capability=capability,
            synthetic_secret_accessor=object(),
            execution_store=execution_store,
        )
    with pytest.raises(runtime.LiveNoteRuntimeAssemblyError, match="execution_store"):
        runtime._assemble_bound_live_note_runtime_for_tests(
            verified_capability=capability,
            synthetic_secret_accessor=_synthetic_accessor(),
            execution_store=object(),
        )


def test_private_test_seam_rejects_target_credential_and_http_overrides(
    execution_store: At1ExecutionStore,
) -> None:
    capability = _issued_capability()
    for forbidden_name in (
        "contact_id",
        "location_id",
        "resource_name",
        "bearer_token",
        "credential",
        "authorization",
        "http_client",
        "base_url",
        "url",
        "host",
        "route",
        "headers",
        "secret_payload",
    ):
        with pytest.raises(TypeError):
            runtime._assemble_bound_live_note_runtime_for_tests(
                verified_capability=capability,
                synthetic_secret_accessor=_synthetic_accessor(),
                execution_store=execution_store,
                **{forbidden_name: "caller-override"},
            )


def test_private_test_seam_binds_exact_validated_capability_and_identity(
    monkeypatch: pytest.MonkeyPatch,
    execution_store: At1ExecutionStore,
) -> None:
    submitted_capability = _issued_capability(
        location_id="synthetic-submitted-location-001",
        contact_id="synthetic-submitted-contact-001",
        consumer_authorization_identity="synthetic-submitted-consumer-001",
        consumer_workflow_run_id="synthetic-submitted-run-001",
    )
    validated_capability = _issued_capability(
        location_id="synthetic-validated-location-001",
        contact_id="synthetic-validated-contact-001",
        consumer_authorization_identity="synthetic-validated-consumer-001",
        consumer_workflow_run_id="synthetic-validated-run-001",
    )

    monkeypatch.setattr(
        note_path_module,
        "_require_issued_verified_capability",
        lambda capability, **kwargs: validated_capability,
    )
    adapter = runtime._assemble_bound_live_note_runtime_for_tests(
        verified_capability=submitted_capability,
        synthetic_secret_accessor=_synthetic_accessor(),
        execution_store=execution_store,
    )

    assert adapter._verified_contact_binding_capability is validated_capability
    assert adapter._location_id == validated_capability.location_id
    assert adapter._contact_id == validated_capability.contact_id
    assert (
        adapter._consumer_authorization_identity
        == validated_capability.consumer_authorization_identity
    )
    assert adapter._consumer_workflow_run_id == validated_capability.consumer_workflow_run_id


def test_private_test_seam_returns_adapter_without_network_or_real_secret_reads(
    execution_store: At1ExecutionStore,
    caplog: pytest.LogCaptureFixture,
) -> None:
    accessor = _synthetic_accessor()
    adapter = runtime._assemble_bound_live_note_runtime_for_tests(
        verified_capability=_issued_capability(),
        synthetic_secret_accessor=accessor,
        execution_store=execution_store,
    )
    transport = adapter._transport
    http_client = transport._http_client

    assert isinstance(adapter, NotePathAdapter)
    assert adapter._verified_contact_binding_capability is not None
    assert transport.total_network_calls == 0
    assert transport.get_attempts == 0
    assert transport.post_attempts == 0
    assert http_client.call_history == ()
    assert accessor.REAL_SECRET_READS == 0
    assert accessor.synthetic_read_count == 1
    assert "synthetic-live-note-runtime-token" not in repr(transport)
    assert "synthetic-live-note-runtime-token" not in caplog.text
    assert "Authorization" not in caplog.text


def test_runtime_never_remints_capabilities_or_accepts_caller_overrides() -> None:
    source = Path(runtime.__file__).read_text(encoding="utf-8")
    public_source = inspect.getsource(assemble_bound_live_note_runtime)

    assert "_issue_bound_contact_capability" not in source
    assert "_issue_synthetic_test_capability" not in source
    assert "_handoff_private_at8_verified_binding_capability" not in source
    assert "At1ExecutionStore(" not in public_source
    assert "_resolve_root_owned_runtime_dependencies" in public_source


def test_frozen_blocked_module_boundaries_remain_intact() -> None:
    transport_source = (SOURCE_ROOT / "live_note_transport.py").read_text(encoding="utf-8")
    note_path_source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")
    provider_source = (
        SOURCE_ROOT / "live_note_credential_provider.py"
    ).read_text(encoding="utf-8")
    http_client_source = (SOURCE_ROOT / "live_note_http_client.py").read_text(
        encoding="utf-8"
    )

    assert 'BASE_URL = "https://services.leadconnectorhq.com"' in transport_source
    assert "_require_issued_verified_capability" in note_path_source
    assert "GoogleSecretManagerLiveNoteSecretAccessor" in provider_source
    assert "versions/1" in provider_source
    assert "runtime.env" not in Path(runtime.__file__).read_text(encoding="utf-8")
    assert "AUTOMATIC_RETRY = False" in http_client_source
