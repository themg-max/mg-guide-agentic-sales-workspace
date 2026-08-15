"""NW-005 Stage B: bounded Firestore persistence adapter for Wave 1 smoke.

The smallest surface needed for the authorized call graph:

- create_exact(run_id, audit)
- get_exact(run_id)
- delete_exact(run_id)
- verify_readback(readback, run_id, expected_content_fingerprint)

All operations fail closed before any network call unless the target is the
exact authorized project, database, collection, run_id, retention_mode, and a
terminal workflow_run_audit_v1 document. No set/overwrite, update, query, list,
batch, transaction, or wildcard access is exposed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

from google.cloud import firestore

from .canonicalize import fingerprint_hex
from .models import TERMINAL_STATES
from .project import content_fingerprint_body
from .validate import validate_workflow_run_audit

AUTHORIZED_PROJECT = "mg-devpost"
AUTHORIZED_DATABASE = "devpost-google-contest"
AUTHORIZED_COLLECTION = "workflow_runs"
AUTHORIZED_LOCATION = "us-east4"
AUTHORIZED_MODE = "stage_b_smoke"

WAVE1_RUN_ID = "run_nw006_success_001"

# Outer allowlist from authorization artifact. Wave 1 is only permitted to
# execute WAVE1_RUN_ID; the remaining IDs are retained for traceability.
OUTER_ALLOWLIST = frozenset(
    {
        "run_nw006_success_001",
        "run_nw006_stage_denied_001",
        "run_nw006_ambiguous_contact_001",
        "run_nw006_failed_001",
    }
)

FIRESTORE_GUARD_REJECTED = "FIRESTORE_GUARD_REJECTED"
FIRESTORE_CAP_EXCEEDED = "FIRESTORE_CAP_EXCEEDED"
FIRESTORE_CREATE_CONFLICT = "FIRESTORE_CREATE_CONFLICT"
FIRESTORE_READBACK_INVALID = "FIRESTORE_READBACK_INVALID"
FIRESTORE_RUN_ID_MISMATCH = "FIRESTORE_RUN_ID_MISMATCH"
FIRESTORE_FINGERPRINT_MISMATCH = "FIRESTORE_FINGERPRINT_MISMATCH"
FIRESTORE_NOT_FOUND_AFTER_DELETE = "FIRESTORE_NOT_FOUND_AFTER_DELETE"


class FirestoreAuditStoreError(ValueError):
    """Fail-closed Firestore store error with a stable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass
class FirestoreAuditStore:
    """Bounded, create-only Firestore adapter for Stage B smoke proof.

    Uses Application Default Credentials. No service-account JSON keys, no IAM
    mutation, no set/overwrite/update/list/query/batch/transaction support.
    """

    project: str = AUTHORIZED_PROJECT
    database: str = AUTHORIZED_DATABASE
    collection: str = AUTHORIZED_COLLECTION
    retention_mode: str = AUTHORIZED_MODE
    max_creates: int = 10
    max_reads: int = 20
    max_deletes: int = 10

    creates: int = field(default=0, init=False)
    reads: int = field(default=0, init=False)
    deletes: int = field(default=0, init=False)

    _client: Optional[firestore.Client] = field(default=None, init=False, repr=False)

    def _guard(self, run_id: Optional[str] = None) -> None:
        """Fail-closed pre-network authorization and configuration guard."""
        if self.project != AUTHORIZED_PROJECT:
            raise FirestoreAuditStoreError(
                FIRESTORE_GUARD_REJECTED,
                f"project={self.project!r} is not authorized",
            )
        if self.database != AUTHORIZED_DATABASE:
            raise FirestoreAuditStoreError(
                FIRESTORE_GUARD_REJECTED,
                f"database={self.database!r} is not authorized",
            )
        if self.collection != AUTHORIZED_COLLECTION:
            raise FirestoreAuditStoreError(
                FIRESTORE_GUARD_REJECTED,
                f"collection={self.collection!r} is not authorized",
            )
        if self.retention_mode != AUTHORIZED_MODE:
            raise FirestoreAuditStoreError(
                FIRESTORE_GUARD_REJECTED,
                f"retention_mode={self.retention_mode!r} is not authorized",
            )
        if run_id is not None:
            if run_id != WAVE1_RUN_ID:
                raise FirestoreAuditStoreError(
                    FIRESTORE_GUARD_REJECTED,
                    f"run_id={run_id!r} is not authorized for Wave 1",
                )

    def _client_instance(self) -> firestore.Client:
        if self._client is None:
            self._client = firestore.Client(project=self.project, database=self.database)
        return self._client

    def _collection_ref(self):
        return self._client_instance().collection(self.collection)

    def _document_ref(self, run_id: str):
        return self._collection_ref().document(run_id)

    @staticmethod
    def _is_terminal(audit: Mapping[str, Any]) -> bool:
        validate_workflow_run_audit(audit)
        return audit.get("terminal_state") in TERMINAL_STATES

    def create_exact(
        self,
        run_id: str,
        audit: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Create-only write of a terminal audit document by exact run_id."""
        self._guard(run_id=run_id)
        if not self._is_terminal(audit):
            raise FirestoreAuditStoreError(
                FIRESTORE_GUARD_REJECTED,
                "non-terminal audit documents must not be durably written",
            )
        if self.creates >= self.max_creates:
            raise FirestoreAuditStoreError(
                FIRESTORE_CAP_EXCEEDED,
                f"create cap {self.max_creates} would be exceeded",
            )

        self.creates += 1
        try:
            self._document_ref(run_id).create(dict(audit))
        except Exception as exc:
            # Translate AlreadyExists and similar conflicts into a stable code.
            message = str(exc)
            if "already exists" in message.lower() or "ALREADY_EXISTS" in message:
                raise FirestoreAuditStoreError(
                    FIRESTORE_CREATE_CONFLICT,
                    f"document workflow_runs/{run_id} already exists",
                ) from exc
            raise

        return {"run_id": run_id, "created": True}

    def get_exact(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Exact document read by run_id; returns None when NOT_FOUND."""
        self._guard(run_id=run_id)
        if self.reads >= self.max_reads:
            raise FirestoreAuditStoreError(
                FIRESTORE_CAP_EXCEEDED,
                f"read cap {self.max_reads} would be exceeded",
            )

        self.reads += 1
        snapshot = self._document_ref(run_id).get()
        if not snapshot.exists:
            return None
        return snapshot.to_dict()

    def delete_exact(self, run_id: str) -> Dict[str, Any]:
        """Exact document delete by run_id; idempotent, no error if missing."""
        self._guard(run_id=run_id)
        if self.deletes >= self.max_deletes:
            raise FirestoreAuditStoreError(
                FIRESTORE_CAP_EXCEEDED,
                f"delete cap {self.max_deletes} would be exceeded",
            )

        self.deletes += 1
        self._document_ref(run_id).delete()
        return {"run_id": run_id, "deleted": True}

    def verify_readback(
        self,
        readback: Mapping[str, Any],
        run_id: str,
        expected_content_fingerprint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validate schema, run_id, and content fingerprint of a readback doc."""
        if not isinstance(readback, Mapping):
            raise FirestoreAuditStoreError(
                FIRESTORE_READBACK_INVALID,
                "readback document must be a mapping",
            )
        try:
            validate_workflow_run_audit(readback)
        except Exception as exc:
            raise FirestoreAuditStoreError(
                FIRESTORE_READBACK_INVALID,
                f"readback schema validation failed: {exc}",
            ) from exc

        if readback.get("run_id") != run_id:
            raise FirestoreAuditStoreError(
                FIRESTORE_RUN_ID_MISMATCH,
                f"readback run_id={readback.get('run_id')!r} != {run_id!r}",
            )

        stored = readback.get("integrity", {}).get("content_fingerprint")
        recomputed = fingerprint_hex(content_fingerprint_body(readback))
        if stored != recomputed:
            raise FirestoreAuditStoreError(
                FIRESTORE_FINGERPRINT_MISMATCH,
                "stored content_fingerprint does not match recomputed readback fingerprint",
            )

        if expected_content_fingerprint is not None and stored != expected_content_fingerprint:
            raise FirestoreAuditStoreError(
                FIRESTORE_FINGERPRINT_MISMATCH,
                "stored content_fingerprint does not match expected projected fingerprint",
            )

        return {
            "run_id": run_id,
            "schema_valid": True,
            "run_id_match": True,
            "stored_content_fingerprint": stored,
            "recomputed_content_fingerprint": recomputed,
            "expected_content_fingerprint": expected_content_fingerprint,
        }

    def require_not_found_after_delete(self, run_id: str) -> None:
        """Post-delete guard: exact get must return NOT_FOUND."""
        after = self.get_exact(run_id)
        if after is not None:
            raise FirestoreAuditStoreError(
                FIRESTORE_NOT_FOUND_AFTER_DELETE,
                f"document workflow_runs/{run_id} still exists after delete",
            )
