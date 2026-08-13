"""NW-005 Stage A: deterministic offline Firestore audit projection.

Pure packet → workflow_run_audit_v1 projection with terminal-only in-memory
persistence. No Firestore client, no CRM, no policy re-eval, no agent rerun.
"""

from __future__ import annotations

from .canonicalize import (
    CANONICALIZER_ID,
    fingerprint_hex,
    nw005_canonical_json_v1,
)
from .firestore_store import (
    AUTHORIZED_COLLECTION,
    AUTHORIZED_DATABASE,
    AUTHORIZED_LOCATION,
    AUTHORIZED_MODE,
    AUTHORIZED_PROJECT,
    FIRESTORE_CAP_EXCEEDED,
    FIRESTORE_CREATE_CONFLICT,
    FIRESTORE_FINGERPRINT_MISMATCH,
    FIRESTORE_GUARD_REJECTED,
    FIRESTORE_NOT_FOUND_AFTER_DELETE,
    FIRESTORE_READBACK_INVALID,
    FIRESTORE_RUN_ID_MISMATCH,
    OUTER_ALLOWLIST,
    WAVE1_RUN_ID,
    FirestoreAuditStore,
    FirestoreAuditStoreError,
)
from .memory_store import (
    AUDIT_IDEMPOTENCY_CONFLICT,
    AUDIT_NON_TERMINAL_DURABLE_WRITE,
    AUDIT_TERMINAL_STATE_CONFLICT,
    MemoryAuditStore,
    PersistResult,
)
from .models import (
    AUDIT_SCHEMA,
    AUDIT_STATUS_MAPPER_ID,
    PACKET_SCHEMA,
    PROJECTION_VERSION,
    TERMINAL_STATES,
    WORKFLOW_ID,
    ProjectionContext,
)
from .project import (
    AUDIT_PROJECTION_INCONSISTENT,
    AuditProjectionError,
    map_card_state,
    map_terminal_state,
    project_workflow_run_audit,
)
from .validate import validate_workflow_run_audit

__all__ = [
    "AUDIT_IDEMPOTENCY_CONFLICT",
    "AUDIT_NON_TERMINAL_DURABLE_WRITE",
    "AUDIT_PROJECTION_INCONSISTENT",
    "AUDIT_SCHEMA",
    "AUDIT_STATUS_MAPPER_ID",
    "AUDIT_TERMINAL_STATE_CONFLICT",
    "AUTHORIZED_COLLECTION",
    "AUTHORIZED_DATABASE",
    "AUTHORIZED_LOCATION",
    "AUTHORIZED_MODE",
    "AUTHORIZED_PROJECT",
    "AuditProjectionError",
    "CANONICALIZER_ID",
    "FIRESTORE_CAP_EXCEEDED",
    "FIRESTORE_CREATE_CONFLICT",
    "FIRESTORE_FINGERPRINT_MISMATCH",
    "FIRESTORE_GUARD_REJECTED",
    "FIRESTORE_NOT_FOUND_AFTER_DELETE",
    "FIRESTORE_READBACK_INVALID",
    "FIRESTORE_RUN_ID_MISMATCH",
    "FirestoreAuditStore",
    "FirestoreAuditStoreError",
    "MemoryAuditStore",
    "OUTER_ALLOWLIST",
    "PACKET_SCHEMA",
    "PROJECTION_VERSION",
    "PersistResult",
    "ProjectionContext",
    "TERMINAL_STATES",
    "WAVE1_RUN_ID",
    "WORKFLOW_ID",
    "fingerprint_hex",
    "map_card_state",
    "map_terminal_state",
    "nw005_canonical_json_v1",
    "project_workflow_run_audit",
    "validate_workflow_run_audit",
]
