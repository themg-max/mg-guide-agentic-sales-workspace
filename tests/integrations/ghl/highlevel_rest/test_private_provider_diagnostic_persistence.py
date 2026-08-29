from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

import pytest

from integrations.ghl.highlevel_rest.live_note_transport import (
    LiveNoteHttpResult,
    PrivateProviderErrorEvidence,
    derive_private_provider_error_evidence,
)
from integrations.ghl.highlevel_rest.private_provider_diagnostic_persistence import (
    SCHEMA_VERSION,
    PrivateProviderDiagnosticPersistenceError,
    PrivateProviderDiagnosticStore,
)


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".gitignore").write_text("local/\n", encoding="utf-8")
    return repo


def _store(tmp_path: Path) -> PrivateProviderDiagnosticStore:
    repo = _repo(tmp_path)
    return PrivateProviderDiagnosticStore(
        repo_root=repo,
        private_root=repo / "local" / "private" / "provider-diagnostics",
    )


def _evidence(
    *,
    message: str = "private synthetic forbidden detail",
    body_extra: dict[str, str] | None = None,
) -> tuple[bytes, PrivateProviderErrorEvidence]:
    body = {
        "errorCode": "forbidden_scope",
        "message": message,
        **(body_extra or {}),
    }
    raw_body = json.dumps(body, separators=(",", ":"), sort_keys=True).encode()
    evidence = derive_private_provider_error_evidence(
        LiveNoteHttpResult(
            status_code=403,
            body=raw_body,
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": "request-test-001",
                "X-Correlation-Id": "correlation-test-001",
                "Authorization": "synthetic-authorization-never-persist",
                "Cookie": "synthetic-cookie-never-persist",
            },
        )
    )
    return raw_body, evidence


def test_persists_exact_whitelist_create_only_mode_0600(tmp_path: Path) -> None:
    raw_body, evidence = _evidence(
        body_extra={"locationId": "synthetic-private-location-never-persist"}
    )
    store = _store(tmp_path)

    receipt = store.persist(
        evidence,
        grant_id="grant-001",
        run_id="run-001",
        operation_id="operation-001",
        sensitive_values=(
            "synthetic-token-never-persist",
            "synthetic-private-location-never-persist",
        ),
        recorded_at_utc="2026-08-29T12:00:00Z",
    )

    payload = json.loads(receipt.path.read_text(encoding="utf-8"))
    assert receipt.verified is True
    assert stat.S_IMODE(receipt.path.stat().st_mode) == 0o600
    assert receipt.payload_sha256 == hashlib.sha256(
        receipt.path.read_bytes()
    ).hexdigest()
    assert payload == {
        "SCHEMA_VERSION": SCHEMA_VERSION,
        "RECORDED_AT_UTC": "2026-08-29T12:00:00Z",
        "GRANT_ID": "grant-001",
        "RUN_ID": "run-001",
        "OPERATION_ID": "operation-001",
        "PROVIDER_HTTP_STATUS": 403,
        "CONTENT_TYPE_CLASS": "JSON",
        "RESPONSE_BODY_LENGTH": len(raw_body),
        "RESPONSE_BODY_SHA256": hashlib.sha256(raw_body).hexdigest(),
        "PROVIDER_ERROR_ENVELOPE_PARSEABLE": True,
        "PROVIDER_ERROR_CODE": "forbidden_scope",
        "PROVIDER_ERROR_MESSAGE": "private synthetic forbidden detail",
        "PROVIDER_REQUEST_ID": "request-test-001",
        "PROVIDER_CORRELATION_ID": "correlation-test-001",
        "PROVIDER_ERROR_CLASS": "AUTHORIZATION",
        "PROVIDER_ERROR_CAUSE": "UNKNOWN",
    }
    rendered = receipt.path.read_text(encoding="utf-8")
    assert raw_body.decode() not in rendered
    assert "synthetic-authorization-never-persist" not in rendered
    assert "synthetic-cookie-never-persist" not in rendered
    assert "synthetic-token-never-persist" not in rendered
    assert "synthetic-private-location-never-persist" not in rendered
    assert not any(receipt.path.parent.glob(".*.tmp"))


def test_existing_destination_is_never_overwritten(tmp_path: Path) -> None:
    _, evidence = _evidence()
    store = _store(tmp_path)
    receipt = store.persist(
        evidence,
        grant_id="grant-001",
        run_id="run-001",
        operation_id="operation-001",
        sensitive_values=("synthetic-token-never-persist",),
        recorded_at_utc="2026-08-29T12:00:00Z",
    )
    original = receipt.path.read_bytes()

    with pytest.raises(
        PrivateProviderDiagnosticPersistenceError, match="already exists"
    ):
        store.persist(
            evidence,
            grant_id="grant-001",
            run_id="run-001",
            operation_id="operation-001",
            sensitive_values=("synthetic-token-never-persist",),
            recorded_at_utc="2026-08-29T12:01:00Z",
        )

    assert receipt.path.read_bytes() == original

    next_grant = store.persist(
        evidence,
        grant_id="grant-002",
        run_id="run-001",
        operation_id="operation-001",
        sensitive_values=("synthetic-token-never-persist",),
        recorded_at_utc="2026-08-29T12:02:00Z",
    )
    assert next_grant.path != receipt.path
    assert next_grant.path.exists()


def test_unignored_destination_is_rejected_before_write(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    store = PrivateProviderDiagnosticStore(
        repo_root=repo,
        private_root=repo / "private-provider-diagnostics",
    )
    _, evidence = _evidence()

    with pytest.raises(
        PrivateProviderDiagnosticPersistenceError, match="not gitignored"
    ):
        store.persist(
            evidence,
            grant_id="grant-001",
            run_id="run-001",
            operation_id="operation-001",
            sensitive_values=("synthetic-token-never-persist",),
        )

    assert not (repo / "private-provider-diagnostics").exists()


def test_sensitive_value_in_persisted_fields_is_rejected(tmp_path: Path) -> None:
    private_id = "synthetic-private-opportunity-never-persist"
    _, evidence = _evidence(message=f"access denied for {private_id}")
    store = _store(tmp_path)

    with pytest.raises(
        PrivateProviderDiagnosticPersistenceError,
        match="forbidden sensitive value",
    ):
        store.persist(
            evidence,
            grant_id="grant-001",
            run_id="run-001",
            operation_id="operation-001",
            sensitive_values=(private_id,),
        )

    private_root = tmp_path / "repo" / "local" / "private"
    if private_root.exists():
        assert not list(private_root.rglob("*.json"))


def test_bound_sensitive_value_inventory_is_required(tmp_path: Path) -> None:
    _, evidence = _evidence()
    store = _store(tmp_path)

    with pytest.raises(
        PrivateProviderDiagnosticPersistenceError,
        match="all bound credential and private CRM values",
    ):
        store.persist(
            evidence,
            grant_id="grant-001",
            run_id="run-001",
            operation_id="operation-001",
            sensitive_values=(),
        )
