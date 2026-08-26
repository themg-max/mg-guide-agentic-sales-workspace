from __future__ import annotations

import copy
import inspect
import pickle
import types
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
CONSUMER_IDENTITY = "NW008_AT8W30_R3_SYNTHETIC_LEASE_CONSUMER_IDENTITY_001"
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


def _private_binding_lease(
    *,
    location_id: str = "synthetic-location-001",
    contact_id: str = "synthetic-contact-001",
    consumer_authorization_identity: str = CONSUMER_IDENTITY,
    consumer_workflow_run_id: str = "synthetic-workflow-run-root-owned-runtime-001",
):
    return NotePathAdapter._build_private_at8_binding_lease_for_tests(
        location_id=location_id,
        contact_id=contact_id,
        consumer_authorization_identity=consumer_authorization_identity,
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


def test_public_assembler_accepts_only_preexisting_opaque_reference() -> None:
    signature = inspect.signature(assemble_bound_live_note_runtime)

    assert tuple(signature.parameters) == (
        "private_binding_reference",
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
    )
    for parameter in signature.parameters.values():
        assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
        assert parameter.default is inspect.Parameter.empty

    for forbidden_name in (
        "verified_capability",
        "capability",
        "trusted_binding_source",
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
                private_binding_reference=_private_binding_lease(),
                consumer_authorization_identity=CONSUMER_IDENTITY,
                consumer_workflow_run_id="synthetic-workflow-run-public-signature-001",
                **{forbidden_name: "caller-override"},
            )


def test_environment_selected_authority_provider_is_absent() -> None:
    source = (SOURCE_ROOT / "live_note_runtime.py").read_text(encoding="utf-8")

    assert not hasattr(runtime, "_resolve_root_owned_private_authority_consumer")
    assert not hasattr(runtime, "_resolve_root_owned_verified_capability")
    assert not hasattr(runtime, "_ROOT_OWNED_PRIVATE_AUTHORITY_CONSUMER_MODULE_KEY")
    assert not hasattr(runtime, "_ROOT_OWNED_PRIVATE_AUTHORITY_CONSUMER_CALLABLE_KEY")
    assert not hasattr(runtime, "_ROOT_OWNED_PRIVATE_AUTHORITY_CONSUMER_IDENTITY")

    assert "MG_GUIDE_NW008_PRIVATE_AUTHORITY_CONSUMER_MODULE" not in source
    assert "MG_GUIDE_NW008_PRIVATE_AUTHORITY_CONSUMER_CALLABLE" not in source
    assert "PRIVATE_AUTHORITY_CONSUMER_AND_PR217_CORRECTION_IMPLEMENTATION" not in source


def test_first_authentic_lease_consumption_transitions_available_to_consumed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workflow_run_id = "synthetic-workflow-run-first-consumption-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    assert note_path_module._private_at8_binding_lease_state(reference) == "AVAILABLE"

    capability = runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )

    assert capability.location_id == "synthetic-location-001"
    assert capability.contact_id == "synthetic-contact-001"
    assert capability.consumer_authorization_identity == CONSUMER_IDENTITY
    assert capability.consumer_workflow_run_id == workflow_run_id
    assert note_path_module._private_at8_binding_lease_state(reference) == "CONSUMED"


def test_second_consumption_and_replay_fail_closed() -> None:
    workflow_run_id = "synthetic-workflow-run-replay-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )

    for _ in range(2):
        with pytest.raises(BindingError, match="already consumed"):
            runtime._consume_root_owned_private_binding_reference(
                private_binding_reference=reference,
                consumer_authorization_identity=CONSUMER_IDENTITY,
                consumer_workflow_run_id=workflow_run_id,
            )

    assert note_path_module._private_at8_binding_lease_state(reference) == "CONSUMED"


def test_forged_reference_fails_closed_without_consuming_valid_authority() -> None:
    workflow_run_id = "synthetic-workflow-run-forged-001"
    valid_reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)
    forged_reference = note_path_module._OpaqueSafePrivateBindingReference()

    with pytest.raises(BindingError, match="not recognized"):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=forged_reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )

    assert note_path_module._private_at8_binding_lease_state(valid_reference) == "AVAILABLE"
    assert runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=valid_reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    ).contact_id == "synthetic-contact-001"


def test_serialized_or_copied_reference_fails_closed() -> None:
    workflow_run_id = "synthetic-workflow-run-serialized-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    with pytest.raises(BindingError, match="not serializable"):
        pickle.dumps(reference)
    with pytest.raises(BindingError, match="not copyable"):
        copy.copy(reference)
    with pytest.raises(BindingError, match="not copyable"):
        copy.deepcopy(reference)

    assert note_path_module._private_at8_binding_lease_state(reference) == "AVAILABLE"

    for structural_copy in (
        types.SimpleNamespace(),
        object(),
        repr(reference),
    ):
        with pytest.raises(BindingError, match="not recognized"):
            runtime._consume_root_owned_private_binding_reference(
                private_binding_reference=structural_copy,
                consumer_authorization_identity=CONSUMER_IDENTITY,
                consumer_workflow_run_id=workflow_run_id,
            )

    assert note_path_module._private_at8_binding_lease_state(reference) == "AVAILABLE"


def test_authorization_identity_mismatch_fails_closed_and_consumes() -> None:
    workflow_run_id = "synthetic-workflow-run-identity-mismatch-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    with pytest.raises(BindingError, match="authorization binding is invalid"):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=reference,
            consumer_authorization_identity="NW008_UNRELATED_CONSUMER_IDENTITY_001",
            consumer_workflow_run_id=workflow_run_id,
        )

    assert note_path_module._private_at8_binding_lease_state(reference) == "CONSUMED"

    with pytest.raises(BindingError, match="already consumed"):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )


def test_workflow_run_mismatch_fails_closed_and_consumes() -> None:
    workflow_run_id = "synthetic-workflow-run-run-mismatch-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    with pytest.raises(BindingError, match="workflow run binding is invalid"):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-other-001",
        )

    assert note_path_module._private_at8_binding_lease_state(reference) == "CONSUMED"

    with pytest.raises(BindingError, match="already consumed"):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )


def test_preissued_capability_as_public_boundary_input_is_rejected() -> None:
    capability = _issued_capability(
        consumer_workflow_run_id="synthetic-workflow-run-preissued-001"
    )

    with pytest.raises(
        runtime.LiveNoteRuntimeAssemblyError, match="opaque private binding reference"
    ):
        runtime._consume_root_owned_private_binding_reference(
            private_binding_reference=capability,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-preissued-001",
        )

    with pytest.raises(
        runtime.LiveNoteRuntimeAssemblyError, match="opaque private binding reference"
    ):
        assemble_bound_live_note_runtime(
            private_binding_reference=capability,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-preissued-001",
        )


def test_raw_ids_cannot_mint_lease_or_capability() -> None:
    for raw_location_id, raw_contact_id in (
        ("real-location-001", "synthetic-contact-001"),
        ("synthetic-location-001", "real-contact-001"),
    ):
        with pytest.raises(BindingError, match="must be synthetic"):
            _private_binding_lease(
                location_id=raw_location_id,
                contact_id=raw_contact_id,
            )

    for raw_reference in ("real-location-001", ("real-location-001", "real-contact-001")):
        with pytest.raises(BindingError, match="not recognized"):
            runtime._consume_root_owned_private_binding_reference(
                private_binding_reference=raw_reference,
                consumer_authorization_identity=CONSUMER_IDENTITY,
                consumer_workflow_run_id="synthetic-workflow-run-raw-ids-001",
            )


def test_capability_issued_only_after_successful_lease_consumption(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workflow_run_id = "synthetic-workflow-run-order-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)
    observed: list[str] = []
    real_consume = note_path_module._consume_private_at8_binding_lease

    def _tracking_consume(submitted: object, **kwargs: object) -> object:
        observed.append("consume")
        return real_consume(submitted, **kwargs)

    real_validate = runtime._validate_issued_capability

    def _tracking_validate(submitted: object, **kwargs: object) -> object:
        observed.append("validate")
        return real_validate(submitted, **kwargs)

    monkeypatch.setattr(
        note_path_module, "_consume_private_at8_binding_lease", _tracking_consume
    )
    monkeypatch.setattr(runtime, "_validate_issued_capability", _tracking_validate)

    runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )

    assert observed == ["consume", "validate"]


def test_validator_expectations_are_explicitly_bound_not_self_derived(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    signature = inspect.signature(runtime._validate_issued_capability)

    for required_name in (
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
    ):
        assert signature.parameters[required_name].default is inspect.Parameter.empty

    workflow_run_id = "synthetic-workflow-run-validator-binding-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)
    validator_calls: list[tuple[object, dict[str, object]]] = []

    def _validator(submitted: object, **kwargs: object) -> object:
        validator_calls.append((submitted, kwargs))
        return submitted

    monkeypatch.setattr(note_path_module, "_require_issued_verified_capability", _validator)

    capability = runtime._consume_root_owned_private_binding_reference(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id=workflow_run_id,
    )

    assert validator_calls == [
        (
            capability,
            {
                "location_id": capability.location_id,
                "contact_id": capability.contact_id,
                "consumer_authorization_identity": CONSUMER_IDENTITY,
                "consumer_workflow_run_id": workflow_run_id,
            },
        )
    ]


def test_missing_root_owned_config_fails_closed_before_runtime_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workflow_run_id = "synthetic-workflow-run-missing-config-001"
    reference = _private_binding_lease(consumer_workflow_run_id=workflow_run_id)

    def _unexpected_construction(*args: object, **kwargs: object) -> None:
        raise AssertionError("missing root-owned configuration must stop assembly")

    monkeypatch.setattr(runtime, "ConcreteLiveNoteHttpClient", _unexpected_construction)
    monkeypatch.setattr(runtime, "LiveNoteCredentialProvider", _unexpected_construction)
    monkeypatch.setattr(runtime, "BoundedLiveNoteTransport", _unexpected_construction)
    monkeypatch.setattr(runtime, "NotePathAdapter", _unexpected_construction)
    monkeypatch.delenv(runtime._ROOT_OWNED_DB_CONFIG_KEY, raising=False)

    with pytest.raises(
        runtime.LiveNoteRuntimeAssemblyError, match="root-owned dependencies"
    ):
        assemble_bound_live_note_runtime(
            private_binding_reference=reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id=workflow_run_id,
        )

    assert note_path_module._private_at8_binding_lease_state(reference) == "CONSUMED"


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
        constructed["impersonation_factory_calls"] = (
            int(constructed.get("impersonation_factory_calls", 0)) + 1
        )
        constructed["impersonation_source"] = source
        return target_runtime_credentials

    def _new_client(credentials: object) -> object:
        constructed["secret_manager_client_factory_calls"] = (
            int(constructed.get("secret_manager_client_factory_calls", 0)) + 1
        )
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
    assert constructed["impersonation_factory_calls"] == 1
    assert constructed["secret_manager_client_factory_calls"] == 1
    dependencies.execution_store._connection.close()


def test_impersonate_target_runtime_credentials_selects_sealed_principal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_credentials = object()
    captured: dict[str, object] = {
        "constructor_calls": 0,
        "network_calls": 0,
        "token_mints": 0,
        "real_impersonation_attempts": 0,
    }

    class _FakeImpersonatedCredentials:
        def __init__(
            self,
            *,
            source_credentials: object,
            target_principal: str,
            target_scopes: list[str],
            lifetime: int,
        ) -> None:
            captured["constructor_calls"] = int(captured["constructor_calls"]) + 1
            captured["source_credentials"] = source_credentials
            captured["target_principal"] = target_principal
            captured["target_scopes"] = list(target_scopes)
            captured["lifetime"] = lifetime

    fake_module = types.SimpleNamespace(Credentials=_FakeImpersonatedCredentials)
    real_import_module = runtime.importlib.import_module

    def _import_module(name: str, package: str | None = None) -> object:
        if name == "google.auth.impersonated_credentials":
            return fake_module
        if name in {
            "google.auth",
            "google.cloud.secretmanager",
            "google.cloud",
        }:
            raise AssertionError(f"unexpected live dependency import: {name}")
        return real_import_module(name, package)

    monkeypatch.setattr(runtime.importlib, "import_module", _import_module)

    result = runtime._impersonate_target_runtime_credentials(source_credentials)

    assert isinstance(result, _FakeImpersonatedCredentials)
    assert captured["constructor_calls"] == 1
    assert captured["source_credentials"] is source_credentials
    assert captured["target_principal"] == (
        "mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
    )
    assert captured["target_scopes"] == [
        "https://www.googleapis.com/auth/cloud-platform"
    ]
    assert captured["lifetime"] == 3600
    assert captured["real_impersonation_attempts"] == 0
    assert captured["token_mints"] == 0
    assert captured["network_calls"] == 0


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
    reference = _private_binding_lease(
        consumer_workflow_run_id="synthetic-workflow-run-store-close-001"
    )

    with pytest.raises(RuntimeError, match="synthetic"):
        assemble_bound_live_note_runtime(
            private_binding_reference=reference,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-store-close-001",
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
    reference = _private_binding_lease(
        consumer_workflow_run_id="synthetic-workflow-run-store-success-001"
    )

    adapter = assemble_bound_live_note_runtime(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-store-success-001",
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
    reference = _private_binding_lease(
        consumer_workflow_run_id="synthetic-workflow-run-root-owned-deps-001"
    )

    adapter = assemble_bound_live_note_runtime(
        private_binding_reference=reference,
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-root-owned-deps-001",
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
        "consumer_authorization_identity",
        "consumer_workflow_run_id",
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
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-at8l-001",
            synthetic_secret_accessor=object(),
            execution_store=execution_store,
        )
    with pytest.raises(runtime.LiveNoteRuntimeAssemblyError, match="execution_store"):
        runtime._assemble_bound_live_note_runtime_for_tests(
            verified_capability=capability,
            consumer_authorization_identity=CONSUMER_IDENTITY,
            consumer_workflow_run_id="synthetic-workflow-run-at8l-001",
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
                consumer_authorization_identity=CONSUMER_IDENTITY,
                consumer_workflow_run_id="synthetic-workflow-run-at8l-001",
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
        consumer_authorization_identity="synthetic-submitted-consumer-001",
        consumer_workflow_run_id="synthetic-submitted-run-001",
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
        consumer_authorization_identity=CONSUMER_IDENTITY,
        consumer_workflow_run_id="synthetic-workflow-run-at8l-001",
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
    assert "_materialize_private_at8_binding_lease" not in source
    assert "_resolve_root_owned_private_authority_consumer" not in source
    assert "At1ExecutionStore(" not in public_source
    assert "_resolve_root_owned_runtime_dependencies" in public_source
    assert "_consume_root_owned_private_binding_reference" in public_source
    assert "verified_capability:" not in public_source


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
