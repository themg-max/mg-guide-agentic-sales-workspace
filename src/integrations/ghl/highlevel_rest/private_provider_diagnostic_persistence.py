"""Transport-neutral contracts for private provider diagnostic persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Protocol

from .live_note_transport import PrivateProviderErrorEvidence


SCHEMA_VERSION = "nw008_private_provider_diagnostic_v1"


class PrivateProviderDiagnosticPersistenceError(RuntimeError):
    """Raised when a private diagnostic cannot be persisted and verified safely."""


@dataclass(frozen=True)
class PrivateProviderDiagnosticReceipt:
    """Verified receipt for one create-only diagnostic artifact."""

    path: Path
    payload_sha256: str
    verified: bool


class PrivateProviderDiagnosticPersistence(Protocol):
    """Persistence boundary consumed by the HighLevel diagnostic evaluator."""

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
        """Persist and verify one private diagnostic artifact."""


@dataclass(frozen=True)
class PrivateProviderDiagnosticContext:
    """Execution identity and persistence boundary for one provider diagnostic."""

    store: PrivateProviderDiagnosticPersistence
    grant_id: str
    run_id: str
    operation_id: str
    sensitive_values: tuple[str, ...] = field(repr=False)
