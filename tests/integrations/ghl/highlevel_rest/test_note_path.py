from __future__ import annotations

from copy import deepcopy
import ast
import json
from pathlib import Path

import pytest

from integrations.ghl.highlevel_rest import (
    BindingError,
    DeterministicFakeTransport,
    NoteContractError,
    NotePathAdapter,
    TransportError,
)


REPO_ROOT = Path(__file__).resolve().parents[4]
FIXTURE_PATH = REPO_ROOT / "fixtures" / "ghl" / "highlevel_rest" / "note-path-fixtures.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
SOURCE_ROOT = REPO_ROOT / "src" / "integrations" / "ghl" / "highlevel_rest"


def _note() -> dict[str, object]:
    return {
        "SYNTHETIC_MARKER": "implementation_reviewed_synthetic_marker",
        "meeting_id": "synthetic-meeting-001",
        "meeting_summary": "Synthetic discovery meeting.",
        "needs": ["Automated reminders"],
        "objections": [],
        "commitments": [{"owner": "Avery", "action": "Share proposal"}],
        "next_step": {"owner": "Avery", "action": "Review proposal"},
        "opportunity_signal": None,
        "workflow_id": "meeting_follow_up_v1",
        "transcript_hash": "a" * 64,
        "synthetic_excerpt": "Synthetic-only demonstration.",
    }


def _adapter(case_id: str) -> tuple[NotePathAdapter, DeterministicFakeTransport]:
    transport = DeterministicFakeTransport(deepcopy(FIXTURE), case_id)
    return (
        NotePathAdapter(
            location_id="synthetic-location-001",
            contact_id="synthetic-contact-001",
            transport=transport,
        ),
        transport,
    )


def _create(adapter: NotePathAdapter) -> None:
    adapter.create_meeting_note(_note())


def _replace_readback_body(
    transport: DeterministicFakeTransport, body: str
) -> DeterministicFakeTransport:
    transport._calls[-1]["response"]["payload"]["note"]["body"] = body
    return transport


def test_exact_contact_binding_pass() -> None:
    adapter, transport = _adapter("contact_success")

    assert adapter.get_bound_contact() == {
        "id": "synthetic-contact-001",
        "locationId": "synthetic-location-001",
    }
    transport.assert_exhausted()


@pytest.mark.parametrize(
    ("case_id", "message"),
    [
        ("contact_id_mismatch", "contact id"),
        ("location_id_mismatch", "location id"),
        ("contact_missing", "not successful"),
    ],
)
def test_contact_binding_mismatch_block(case_id: str, message: str) -> None:
    adapter, _ = _adapter(case_id)

    with pytest.raises((BindingError, TransportError), match=message):
        adapter.get_bound_contact()


def _adapter_with_missing_binding(field_name: str) -> None:
    kwargs = {
        "location_id": "synthetic-location-001",
        "contact_id": "synthetic-contact-001",
        "transport": DeterministicFakeTransport(deepcopy(FIXTURE), "contact_success"),
    }
    kwargs[field_name] = ""
    NotePathAdapter(**kwargs)


def test_missing_contact_binding_block() -> None:
    with pytest.raises(BindingError, match="private binding"):
        _adapter_with_missing_binding("contact_id")


def test_missing_location_binding_block() -> None:
    with pytest.raises(BindingError, match="private binding"):
        _adapter_with_missing_binding("location_id")


@pytest.mark.parametrize("field_name", ["contact_id", "location_id"])
def test_caller_supplied_provider_id_block(field_name: str) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    note[field_name] = "caller-override"

    with pytest.raises(NoteContractError, match="extra"):
        adapter.create_meeting_note(note)
    assert transport.calls == []


@pytest.mark.parametrize(
    "mutation",
    [
        lambda note: note.__setitem__("raw_transcript", "unbounded source"),
        lambda note: note.__setitem__("SYNTHETIC_MARKER", "live_source"),
    ],
)
def test_raw_transcript_and_non_synthetic_source_rejected(mutation) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    mutation(note)

    with pytest.raises(NoteContractError):
        adapter.create_meeting_note(note)
    assert transport.calls == []


def test_note_body_only_payload() -> None:
    adapter, transport = _adapter("note_create_success")

    adapter.create_meeting_note(_note())

    method, path, body = transport.calls[0]
    assert (method, path) == ("POST", "/contacts/synthetic-contact-001/notes")
    assert set(body or {}) == {"body"}
    assert "userId" not in (body or {})
    assert "title" not in (body or {})
    assert "color" not in (body or {})
    assert "pinned" not in (body or {})


@pytest.mark.parametrize("field_name", ["userId", "title", "color", "pinned"])
def test_denied_provider_fields_rejected(field_name: str) -> None:
    adapter, transport = _adapter("note_create_success")
    note = _note()
    note[field_name] = "denied"

    with pytest.raises(NoteContractError, match="extra"):
        adapter.create_meeting_note(note)
    assert transport.calls == []


@pytest.mark.parametrize(
    "case_id",
    [
        "note_create_definite_failure",
        "note_response_malformed",
        "note_response_contact_mismatch",
    ],
)
def test_same_run_note_id_and_contact_binding_required(case_id: str) -> None:
    adapter, _ = _adapter(case_id)

    with pytest.raises(TransportError):
        _create(adapter)


def test_same_run_note_id_required() -> None:
    adapter, transport = _adapter("note_create_success")
    transport._calls[0]["response"]["payload"]["note"].pop("id")

    with pytest.raises(TransportError, match="id is required"):
        _create(adapter)


def test_one_note_write_budget() -> None:
    adapter, transport = _adapter("note_create_success")
    _create(adapter)

    with pytest.raises(TransportError, match="exactly one"):
        _create(adapter)
    assert len(transport.calls) == 1


def test_ambiguous_post_no_retry() -> None:
    adapter, transport = _adapter("note_create_ambiguous_result")

    with pytest.raises(TransportError, match="not retried"):
        _create(adapter)
    with pytest.raises(TransportError, match="exactly one"):
        _create(adapter)
    assert len(transport.calls) == 1


def test_strict_parser_pass_and_note_content_digest_pass() -> None:
    adapter, transport = _adapter("note_readback_success")
    _create(adapter)
    body = transport.calls[0][2]["body"]
    _replace_readback_body(transport, body)

    result = adapter.verify_meeting_note()

    assert result.note_id == "synthetic-note-001"
    assert len(result.note_content_digest) == 64
    transport.assert_exhausted()


@pytest.mark.parametrize(
    ("case_id", "body"),
    [
        (
            "note_body_parser_failure",
            "MG Guide \u2014 Synthetic Meeting Follow-Up\nunknown: \"value\"\n",
        ),
        (
            "note_body_parser_failure",
            "MG Guide \u2014 Synthetic Meeting Follow-Up\n"
            "SYNTHETIC_MARKER: \"implementation_reviewed_synthetic_marker\"\n"
            "SYNTHETIC_MARKER: \"implementation_reviewed_synthetic_marker\"\n",
        ),
    ],
)
def test_strict_parser_unknown_and_duplicate_label_block(case_id: str, body: str) -> None:
    adapter, transport = _adapter(case_id)
    _create(adapter)
    _replace_readback_body(transport, body)

    with pytest.raises(TransportError):
        adapter.verify_meeting_note()


def test_note_content_digest_mismatch_block() -> None:
    adapter, transport = _adapter("digest_mismatch")
    _create(adapter)
    changed = _note()
    changed["meeting_summary"] = "Different synthetic summary."
    changed_body = adapter._serialize_note(changed)
    _replace_readback_body(transport, changed_body)

    with pytest.raises(TransportError, match="NOTE_CONTENT_DIGEST"):
        adapter.verify_meeting_note()


@pytest.mark.parametrize(
    "case_id",
    ["note_readback_id_mismatch", "note_readback_contact_mismatch"],
)
def test_readback_identity_mismatch_block(case_id: str) -> None:
    adapter, transport = _adapter(case_id)
    _create(adapter)
    body = transport.calls[0][2]["body"]
    _replace_readback_body(transport, body)

    with pytest.raises(TransportError):
        adapter.verify_meeting_note()


def test_search_list_generic_execute_and_stage_routes_absent() -> None:
    public_methods = {
        name for name in vars(NotePathAdapter) if not name.startswith("_")
    }

    assert public_methods == {
        "get_bound_contact",
        "create_meeting_note",
        "verify_meeting_note",
    }
    source = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_ROOT.glob("*.py"))
    assert "execute_operation" not in source
    assert "/opportunit" not in source.lower()
    assert "/contacts/" in source


def test_real_client_socket_dns_env_and_live_imports_absent() -> None:
    forbidden_import_roots = {
        "requests",
        "httpx",
        "urllib",
        "socket",
        "os",
        "asyncio",
    }
    forbidden_imports = {
        "integrations.ghl.at1_live_transport_adapter",
        "integrations.ghl.at1_live_transport_serializer",
        "integrations.ghl.bounded_at1_executor",
    }
    for path in SOURCE_ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {name.name.split(".", 1)[0] for name in node.names}
                assert not imported & forbidden_import_roots
            if isinstance(node, ast.ImportFrom):
                assert node.module not in forbidden_imports
                assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots


def test_network_calls_and_external_effects_zero() -> None:
    source = (SOURCE_ROOT / "note_path.py").read_text(encoding="utf-8")

    assert "NETWORK_CALLS = 0" in source
    assert "HIGHLEVEL_NETWORK_CALLS = 0" in source
    assert "EXTERNAL_EFFECTS = 0" in source
    assert FIXTURE["network_calls"] == 0
    assert FIXTURE["external_effects"] == 0
