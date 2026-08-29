"""Create-only filesystem persistence for private provider diagnostics."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from typing import Iterable
from uuid import uuid4

from integrations.ghl.highlevel_rest.live_note_transport import (
    PrivateProviderErrorEvidence,
)
from integrations.ghl.highlevel_rest.private_provider_diagnostic_persistence import (
    SCHEMA_VERSION,
    PrivateProviderDiagnosticPersistenceError,
    PrivateProviderDiagnosticReceipt,
)


_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class PrivateProviderDiagnosticStore:
    """Persist a whitelisted diagnostic record under a gitignored private root."""

    def __init__(self, *, repo_root: Path, private_root: Path) -> None:
        self._repo_root = repo_root.resolve()
        self._private_root = private_root.resolve()
        try:
            self._private_root.relative_to(self._repo_root)
        except ValueError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic root must be inside the repository"
            ) from exc

    def persist(
        self,
        evidence: PrivateProviderErrorEvidence,
        *,
        grant_id: str,
        run_id: str,
        operation_id: str,
        sensitive_values: Iterable[str],
        recorded_at_utc: str | None = None,
    ) -> PrivateProviderDiagnosticReceipt:
        """Atomically create and verify one mode-0600 private diagnostic file."""
        if not isinstance(evidence, PrivateProviderErrorEvidence):
            raise PrivateProviderDiagnosticPersistenceError(
                "evidence must be PrivateProviderErrorEvidence"
            )
        identifiers = {
            "GRANT_ID": grant_id,
            "RUN_ID": run_id,
            "OPERATION_ID": operation_id,
        }
        for name, value in identifiers.items():
            if not isinstance(value, str) or not _SAFE_IDENTIFIER.fullmatch(value):
                raise PrivateProviderDiagnosticPersistenceError(
                    f"{name} must be a safe non-empty identifier"
                )

        timestamp = recorded_at_utc or self._recorded_at_utc()
        if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
            raise PrivateProviderDiagnosticPersistenceError(
                "RECORDED_AT_UTC must be an RFC3339 UTC value ending in Z"
            )
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp[:-1] + "+00:00")
        except ValueError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "RECORDED_AT_UTC must be a valid RFC3339 UTC value"
            ) from exc
        if parsed_timestamp.utcoffset() != timezone.utc.utcoffset(parsed_timestamp):
            raise PrivateProviderDiagnosticPersistenceError(
                "RECORDED_AT_UTC must resolve to UTC"
            )

        filename = (
            f"{grant_id}--{run_id}--{operation_id}.provider-diagnostic.json"
        )
        destination = self._private_root / filename
        self._require_gitignored(destination)

        payload = {
            "SCHEMA_VERSION": SCHEMA_VERSION,
            "RECORDED_AT_UTC": timestamp,
            **identifiers,
            "PROVIDER_HTTP_STATUS": evidence.PROVIDER_HTTP_STATUS,
            "CONTENT_TYPE_CLASS": evidence.CONTENT_TYPE_CLASS,
            "RESPONSE_BODY_LENGTH": evidence.RESPONSE_BODY_LENGTH,
            "RESPONSE_BODY_SHA256": evidence.RESPONSE_BODY_SHA256,
            "PROVIDER_ERROR_ENVELOPE_PARSEABLE": (
                evidence.PROVIDER_ERROR_ENVELOPE_PARSEABLE
            ),
            "PROVIDER_ERROR_CODE": evidence.PROVIDER_ERROR_CODE,
            "PROVIDER_ERROR_MESSAGE": evidence.PROVIDER_ERROR_MESSAGE,
            "PROVIDER_REQUEST_ID": evidence.PROVIDER_REQUEST_ID,
            "PROVIDER_CORRELATION_ID": evidence.PROVIDER_CORRELATION_ID,
            "PROVIDER_ERROR_CLASS": evidence.PROVIDER_ERROR_CLASS,
            "PROVIDER_ERROR_CAUSE": evidence.PROVIDER_ERROR_CAUSE,
        }
        required_sensitive_values = tuple(sensitive_values)
        if not required_sensitive_values or any(
            not isinstance(value, str) or not value
            for value in required_sensitive_values
        ):
            raise PrivateProviderDiagnosticPersistenceError(
                "all bound credential and private CRM values must be supplied"
            )

        serialized = (
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
        ).encode("utf-8")
        self._reject_sensitive_values(serialized, required_sensitive_values)
        self._atomic_create(destination, serialized)
        self._verify(destination, serialized, payload)
        return PrivateProviderDiagnosticReceipt(
            path=destination,
            payload_sha256=hashlib.sha256(serialized).hexdigest(),
            verified=True,
        )

    @staticmethod
    def _recorded_at_utc() -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    def _require_gitignored(self, destination: Path) -> None:
        relative = destination.relative_to(self._repo_root)
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self._repo_root),
                    "check-ignore",
                    "-q",
                    "--",
                    str(relative),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "unable to verify the private diagnostic gitignore boundary"
            ) from exc
        if result.returncode != 0:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic destination is not gitignored"
            )

    @staticmethod
    def _reject_sensitive_values(
        serialized: bytes, sensitive_values: Iterable[str]
    ) -> None:
        text = serialized.decode("utf-8")
        for value in sensitive_values:
            if isinstance(value, str) and value and value in text:
                raise PrivateProviderDiagnosticPersistenceError(
                    "private diagnostic contains a forbidden sensitive value"
                )

    def _atomic_create(self, destination: Path, serialized: bytes) -> None:
        try:
            self._private_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        except OSError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "unable to create the private diagnostic directory"
            ) from exc

        temporary = self._private_root / f".{destination.name}.{uuid4().hex}.tmp"
        fd: int | None = None
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(temporary, flags, 0o600)
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as handle:
                fd = None
                handle.write(serialized)
                handle.flush()
                os.fsync(handle.fileno())
            os.link(temporary, destination, follow_symlinks=False)
            temporary.unlink()
            self._fsync_directory()
        except FileExistsError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic destination already exists"
            ) from exc
        except OSError as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "atomic private diagnostic creation failed"
            ) from exc
        finally:
            if fd is not None:
                os.close(fd)
            temporary.unlink(missing_ok=True)

    def _fsync_directory(self) -> None:
        flags = os.O_RDONLY
        if hasattr(os, "O_DIRECTORY"):
            flags |= os.O_DIRECTORY
        directory_fd = os.open(self._private_root, flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)

    @staticmethod
    def _verify(
        destination: Path, serialized: bytes, expected_payload: dict[str, object]
    ) -> None:
        try:
            metadata = destination.lstat()
            persisted = destination.read_bytes()
            decoded = json.loads(persisted)
        except (OSError, json.JSONDecodeError) as exc:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic persistence verification failed"
            ) from exc
        if not stat.S_ISREG(metadata.st_mode) or destination.is_symlink():
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic is not a regular file"
            )
        if stat.S_IMODE(metadata.st_mode) != 0o600:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic file mode is not 0600"
            )
        if persisted != serialized or decoded != expected_payload:
            raise PrivateProviderDiagnosticPersistenceError(
                "private diagnostic content verification failed"
            )
