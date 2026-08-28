"""Durable local execution state for offline AT-1 bounded transport evidence."""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import hmac
import json
from pathlib import Path
import sqlite3
from typing import Any

from integrations.ghl.at1_commitment_key_provider import (
    CommitmentKeyMaterial,
    _payload_bytes_from_material,
    validate_version_resource,
)


AVAILABLE = "AVAILABLE"
CLAIMED = "CLAIMED"
ATTEMPT_RECORDED = "ATTEMPT_RECORDED"
DISPATCHED = "DISPATCHED"
RESPONSE_CAPTURED = "RESPONSE_CAPTURED"
TERMINAL = "TERMINAL"


class ExecutionClaimError(RuntimeError):
    """Raised when durable grant/run claim ownership cannot be acquired."""


class DuplicateBusinessOrdinalError(RuntimeError):
    """Raised when a consumed business ordinal is attempted again."""


class AttemptStateError(RuntimeError):
    """Raised when a state transition violates the durable attempt contract."""


class RunContinuationRefusedError(RuntimeError):
    """Raised when a grant/run cannot continue due to an unresolved prior attempt."""


class ExecutionStoreSchemaError(RuntimeError):
    """Raised when the store schema or immutable metadata cannot be trusted."""


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class At1ExecutionStore:
    """SQLite-backed local execution store for AT-1 transport/evidence contracts."""

    _METADATA_TABLE = "at1_store_metadata"
    _SCHEMA_VERSION = 2
    _REQUIRED_TABLES = frozenset(
        {
            _METADATA_TABLE,
            "execution_claims",
            "attempts",
            "protocol_ledger",
            "business_ledger",
            "prewrite_provenance",
        }
    )

    def __init__(
        self,
        db_path: str | Path,
        commitment_material: CommitmentKeyMaterial,
    ) -> None:
        self._commitment_key = _payload_bytes_from_material(commitment_material)
        self._commitment_key_version_resource = validate_version_resource(
            commitment_material.version_resource
        )
        self._db_path = str(db_path)
        # sqlite3.connect() creates a missing path; capture preexistence first so a
        # preexisting empty artifact is never treated as fresh initialization.
        path_preexisted = Path(self._db_path).exists()
        self._connection = sqlite3.connect(
            self._db_path,
            isolation_level=None,
            timeout=30.0,
            check_same_thread=False,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        try:
            self._initialize_schema(path_preexisted=path_preexisted)
        except ExecutionStoreSchemaError:
            self._connection.close()
            raise

    @property
    def db_path(self) -> str:
        return self._db_path

    def _initialize_schema(self, *, path_preexisted: bool) -> None:
        table_names = self._table_names()
        if not table_names:
            if path_preexisted:
                raise ExecutionStoreSchemaError(
                    "preexisting empty store artifact cannot be initialized"
                )
            self._initialize_new_schema()
            return

        if self._METADATA_TABLE not in table_names:
            raise ExecutionStoreSchemaError(
                "legacy or partially initialized store has no authoritative metadata"
            )
        if not self._REQUIRED_TABLES.issubset(table_names):
            raise ExecutionStoreSchemaError("store schema is partially initialized")
        self._validate_existing_metadata()

    def _table_names(self) -> set[str]:
        rows = self._connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
        return {str(row["name"]) for row in rows}

    @staticmethod
    def _schema_statements() -> tuple[str, ...]:
        return (
            """
            CREATE TABLE at1_store_metadata (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                schema_version INTEGER NOT NULL,
                commitment_key_version_resource TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE execution_claims (
                grant_run_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                claimed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE attempts (
                grant_run_id TEXT NOT NULL,
                operation_ordinal INTEGER NOT NULL,
                operation_id TEXT NOT NULL,
                request_id TEXT NOT NULL,
                request_envelope_json TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                response_envelope_json TEXT,
                response_digest TEXT,
                http_status INTEGER,
                jsonrpc_error_present INTEGER,
                mcp_is_error INTEGER,
                nested_operation_success INTEGER,
                target_binding_match TEXT,
                parse_success INTEGER,
                semantic_success INTEGER,
                terminal_failure_code TEXT,
                business_effect_truth TEXT,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (grant_run_id, operation_ordinal),
                UNIQUE (grant_run_id, request_id)
            )
            """,
            """
            CREATE TABLE prewrite_provenance (
                grant_run_id TEXT PRIMARY KEY,
                transcript_json TEXT NOT NULL,
                transcript_digest TEXT NOT NULL,
                expected_note_json TEXT NOT NULL,
                expected_note_digest TEXT NOT NULL,
                captured_before_ordinal INTEGER NOT NULL CHECK (captured_before_ordinal = 1),
                captured_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE protocol_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grant_run_id TEXT NOT NULL,
                call_name TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE business_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grant_run_id TEXT NOT NULL,
                operation_ordinal INTEGER NOT NULL,
                operation_id TEXT NOT NULL,
                request_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                request_digest TEXT,
                response_digest TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
        )

    def _initialize_new_schema(self) -> None:
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            for statement in self._schema_statements():
                self._connection.execute(statement)
            self._connection.execute(
                """
                INSERT INTO at1_store_metadata (
                    singleton,
                    schema_version,
                    commitment_key_version_resource
                )
                VALUES (1, ?, ?)
                """,
                (self._SCHEMA_VERSION, self._commitment_key_version_resource),
            )
            self._connection.execute("COMMIT")
        except sqlite3.Error as exc:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise ExecutionStoreSchemaError("atomic store initialization failed") from exc

    def _validate_existing_metadata(self) -> None:
        rows = self._connection.execute(
            """
            SELECT
                singleton,
                schema_version,
                commitment_key_version_resource,
                typeof(schema_version) AS schema_version_type
            FROM at1_store_metadata
            """
        ).fetchall()
        if len(rows) != 1:
            raise ExecutionStoreSchemaError("store metadata must contain exactly one row")

        row = rows[0]
        if (
            row["singleton"] != 1
            or row["schema_version_type"] != "integer"
            or row["schema_version"] != self._SCHEMA_VERSION
        ):
            raise ExecutionStoreSchemaError("store schema version is unsupported or corrupt")

        try:
            persisted_version_resource = validate_version_resource(
                row["commitment_key_version_resource"]
            )
        except ValueError as exc:
            raise ExecutionStoreSchemaError(
                "store commitment-key version metadata is corrupt"
            ) from exc
        if persisted_version_resource != self._commitment_key_version_resource:
            raise ExecutionStoreSchemaError("store commitment-key version does not match")

    def _commitment(self, value: Any) -> str:
        payload = _canonical_json(value).encode("utf-8")
        return hmac.new(self._commitment_key, payload, hashlib.sha256).hexdigest()

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value

    def acquire_claim(self, grant_run_id: str, owner_id: str) -> None:
        grant_run_id = self._require_non_empty(grant_run_id, "grant_run_id")
        owner_id = self._require_non_empty(owner_id, "owner_id")
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO execution_claims (grant_run_id, owner_id)
                    VALUES (?, ?)
                    """,
                    (grant_run_id, owner_id),
                )
        except sqlite3.IntegrityError as exc:
            row = self._connection.execute(
                "SELECT owner_id FROM execution_claims WHERE grant_run_id = ?",
                (grant_run_id,),
            ).fetchone()
            if row is None or row["owner_id"] != owner_id:
                raise ExecutionClaimError(
                    f"grant_run_id {grant_run_id!r} is already claimed by another owner"
                ) from exc

    def assert_claim_owner(self, grant_run_id: str, owner_id: str) -> None:
        row = self._connection.execute(
            "SELECT owner_id FROM execution_claims WHERE grant_run_id = ?",
            (grant_run_id,),
        ).fetchone()
        if row is None:
            raise ExecutionClaimError(
                f"grant_run_id {grant_run_id!r} has no durable execution claim"
            )
        if row["owner_id"] != owner_id:
            raise ExecutionClaimError(
                f"grant_run_id {grant_run_id!r} is claimed by another owner"
            )

    def append_protocol_call(
        self, grant_run_id: str, call_name: str, payload: Mapping[str, Any]
    ) -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO protocol_ledger (grant_run_id, call_name, payload_json)
                VALUES (?, ?, ?)
                """,
                (grant_run_id, call_name, _canonical_json(dict(payload))),
            )

    def next_operation_ordinal(self, grant_run_id: str) -> int:
        row = self._connection.execute(
            """
            SELECT COALESCE(MAX(operation_ordinal), 0) AS max_ordinal
            FROM attempts
            WHERE grant_run_id = ?
            """,
            (grant_run_id,),
        ).fetchone()
        return int(row["max_ordinal"]) + 1

    def latest_operation_ordinal(self, grant_run_id: str) -> int | None:
        row = self._connection.execute(
            """
            SELECT MAX(operation_ordinal) AS max_ordinal
            FROM attempts
            WHERE grant_run_id = ?
            """,
            (grant_run_id,),
        ).fetchone()
        if row["max_ordinal"] is None:
            return None
        return int(row["max_ordinal"])

    def require_run_continuable(self, grant_run_id: str) -> None:
        """Fail closed if any prior attempt is unresolved or the run is terminal.

        A prior RESPONSE_CAPTURED attempt is continuable only when both parse and
        semantic processing are durably complete. Pre-dispatch, post-dispatch,
        pre-parse, pre-semantic, and TERMINAL states poison the grant/run.
        """
        rows = self._connection.execute(
            """
            SELECT state, operation_ordinal, parse_success, semantic_success
            FROM attempts
            WHERE grant_run_id = ?
            ORDER BY operation_ordinal ASC
            """,
            (grant_run_id,),
        ).fetchall()
        for row in rows:
            state = row["state"]
            if state in (ATTEMPT_RECORDED, DISPATCHED, TERMINAL):
                raise RunContinuationRefusedError(
                    f"grant_run_id {grant_run_id!r} cannot continue: "
                    f"ordinal {row['operation_ordinal']} is in state {state!r}"
                )
            if state == RESPONSE_CAPTURED and not (
                row["parse_success"] == 1 and row["semantic_success"] == 1
            ):
                raise RunContinuationRefusedError(
                    f"grant_run_id {grant_run_id!r} cannot continue: "
                    f"ordinal {row['operation_ordinal']} is in state {state!r} "
                    "without durable successful parse and semantic completion"
                )

    def record_attempt(
        self,
        *,
        grant_run_id: str,
        operation_ordinal: int,
        operation_id: str,
        request_id: str,
        request_envelope: Mapping[str, Any],
    ) -> str:
        request_json = _canonical_json(dict(request_envelope))
        request_digest = self._commitment(dict(request_envelope))
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO attempts (
                        grant_run_id,
                        operation_ordinal,
                        operation_id,
                        request_id,
                        request_envelope_json,
                        request_digest,
                        state
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        grant_run_id,
                        operation_ordinal,
                        operation_id,
                        request_id,
                        request_json,
                        request_digest,
                        ATTEMPT_RECORDED,
                    ),
                )
                self._connection.execute(
                    """
                    INSERT INTO business_ledger (
                        grant_run_id,
                        operation_ordinal,
                        operation_id,
                        request_id,
                        event_type,
                        request_digest
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        grant_run_id,
                        operation_ordinal,
                        operation_id,
                        request_id,
                        ATTEMPT_RECORDED,
                        request_digest,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateBusinessOrdinalError(
                f"operation ordinal {operation_ordinal} for {grant_run_id!r} is already consumed"
            ) from exc
        return request_digest

    def record_prewrite_provenance(
        self,
        *,
        grant_run_id: str,
        transcript_content: str,
        transcript_sha256: str,
        expected_note_content: str,
        expected_note_sha256: str,
    ) -> None:
        if self.next_operation_ordinal(grant_run_id) != 1:
            raise AttemptStateError("prewrite provenance must be captured before business ordinal 1")
        if not all(
            isinstance(value, str) and value
            for value in (
                transcript_content,
                transcript_sha256,
                expected_note_content,
                expected_note_sha256,
            )
        ):
            raise AttemptStateError("prewrite provenance values must be non-empty strings")
        if hashlib.sha256(transcript_content.encode("utf-8")).hexdigest() != transcript_sha256:
            raise AttemptStateError("transcript SHA256 does not match captured transcript")
        if hashlib.sha256(expected_note_content.encode("utf-8")).hexdigest() != expected_note_sha256:
            raise AttemptStateError("expected-note SHA256 does not match captured note")
        with self._connection:
            try:
                self._connection.execute(
                    """
                    INSERT INTO prewrite_provenance (
                        grant_run_id, transcript_json, transcript_digest,
                        expected_note_json, expected_note_digest, captured_before_ordinal
                    )
                    VALUES (?, ?, ?, ?, ?, 1)
                    """,
                    (
                        grant_run_id,
                        _canonical_json({"transcript": transcript_content}),
                        transcript_sha256,
                        _canonical_json({"note": expected_note_content}),
                        expected_note_sha256,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise AttemptStateError(
                    f"prewrite provenance is already sealed for {grant_run_id!r}"
                ) from exc

    def mark_dispatched(self, *, grant_run_id: str, operation_ordinal: int) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET state = ?, updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ?
                  AND operation_ordinal = ?
                  AND state = ?
                """,
                (DISPATCHED, grant_run_id, operation_ordinal, ATTEMPT_RECORDED),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot mark ordinal {operation_ordinal} as dispatched from current state"
                )
            row = self._connection.execute(
                """
                SELECT operation_id, request_id, request_digest
                FROM attempts
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (grant_run_id, operation_ordinal),
            ).fetchone()
            self._connection.execute(
                """
                INSERT INTO business_ledger (
                    grant_run_id,
                    operation_ordinal,
                    operation_id,
                    request_id,
                    event_type,
                    request_digest
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    grant_run_id,
                    operation_ordinal,
                    row["operation_id"],
                    row["request_id"],
                    DISPATCHED,
                    row["request_digest"],
                ),
            )

    def capture_response(
        self,
        *,
        grant_run_id: str,
        operation_ordinal: int,
        response_envelope: Mapping[str, Any],
    ) -> str:
        response_json = _canonical_json(dict(response_envelope))
        response_digest = self._commitment(dict(response_envelope))
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET response_envelope_json = ?,
                    response_digest = ?,
                    state = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ?
                  AND operation_ordinal = ?
                  AND state = ?
                """,
                (
                    response_json,
                    response_digest,
                    RESPONSE_CAPTURED,
                    grant_run_id,
                    operation_ordinal,
                    DISPATCHED,
                ),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot capture response for ordinal {operation_ordinal} from current state"
                )
            row = self._connection.execute(
                """
                SELECT operation_id, request_id, request_digest
                FROM attempts
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (grant_run_id, operation_ordinal),
            ).fetchone()
            self._connection.execute(
                """
                INSERT INTO business_ledger (
                    grant_run_id,
                    operation_ordinal,
                    operation_id,
                    request_id,
                    event_type,
                    request_digest,
                    response_digest
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    grant_run_id,
                    operation_ordinal,
                    row["operation_id"],
                    row["request_id"],
                    RESPONSE_CAPTURED,
                    row["request_digest"],
                    response_digest,
                ),
            )
        return response_digest

    def record_response_evidence(
        self,
        *,
        grant_run_id: str,
        operation_ordinal: int,
        http_status: int | None,
        jsonrpc_error_present: bool,
        mcp_is_error: bool | None,
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET http_status = ?,
                    jsonrpc_error_present = ?,
                    mcp_is_error = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ?
                  AND operation_ordinal = ?
                  AND state = ?
                """,
                (
                    http_status,
                    1 if jsonrpc_error_present else 0,
                    None if mcp_is_error is None else int(mcp_is_error),
                    grant_run_id,
                    operation_ordinal,
                    RESPONSE_CAPTURED,
                ),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot record response evidence for ordinal {operation_ordinal}"
                )

    def record_parse_outcome(
        self, *, grant_run_id: str, operation_ordinal: int, success: bool
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET parse_success = ?,
                    http_status = CASE WHEN ? = 0 THEN NULL ELSE http_status END,
                    nested_operation_success = CASE
                        WHEN ? = 0 THEN 0
                        ELSE nested_operation_success
                    END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (
                    1 if success else 0,
                    1 if success else 0,
                    1 if success else 0,
                    grant_run_id,
                    operation_ordinal,
                ),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot record parse outcome for ordinal {operation_ordinal}"
                )

    def record_semantic_outcome(
        self,
        *,
        grant_run_id: str,
        operation_ordinal: int,
        success: bool,
        target_binding_match: bool | str | None = None,
    ) -> None:
        if target_binding_match not in (True, False, "NOT_APPLICABLE", None):
            raise AttemptStateError("target binding match must be true, false, or NOT_APPLICABLE")
        public_target_binding_match = (
            "YES"
            if target_binding_match is True
            else "NO"
            if target_binding_match is False
            else target_binding_match
        )
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET semantic_success = ?,
                    target_binding_match = ?,
                    nested_operation_success = CASE
                        WHEN parse_success = 1
                         AND ? = 1
                         AND ? IN ('YES', 'NOT_APPLICABLE')
                        THEN 1
                        ELSE 0
                    END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (
                    1 if success else 0,
                    public_target_binding_match,
                    1 if success else 0,
                    public_target_binding_match,
                    grant_run_id,
                    operation_ordinal,
                ),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot record semantic outcome for ordinal {operation_ordinal}"
                )

    def mark_terminal(
        self,
        *,
        grant_run_id: str,
        operation_ordinal: int,
        failure_code: str,
        business_effect_truth: str,
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET terminal_failure_code = ?,
                    business_effect_truth = ?,
                    state = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (
                    failure_code,
                    business_effect_truth,
                    TERMINAL,
                    grant_run_id,
                    operation_ordinal,
                ),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot mark ordinal {operation_ordinal} terminal"
                )
            row = self._connection.execute(
                """
                SELECT operation_id, request_id, request_digest, response_digest
                FROM attempts
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (grant_run_id, operation_ordinal),
            ).fetchone()
            self._connection.execute(
                """
                INSERT INTO business_ledger (
                    grant_run_id,
                    operation_ordinal,
                    operation_id,
                    request_id,
                    event_type,
                    request_digest,
                    response_digest
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    grant_run_id,
                    operation_ordinal,
                    row["operation_id"],
                    row["request_id"],
                    TERMINAL,
                    row["request_digest"],
                    row["response_digest"],
                ),
            )

    def list_private_attempts(self, grant_run_id: str) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            """
            SELECT
                operation_ordinal,
                operation_id,
                request_id,
                request_envelope_json,
                request_digest,
                response_envelope_json,
                response_digest,
                http_status,
                jsonrpc_error_present,
                mcp_is_error,
                nested_operation_success,
                target_binding_match,
                parse_success,
                semantic_success,
                terminal_failure_code,
                business_effect_truth,
                state
            FROM attempts
            WHERE grant_run_id = ?
            ORDER BY operation_ordinal ASC
            """,
            (grant_run_id,),
        ).fetchall()
        attempts: list[dict[str, Any]] = []
        for row in rows:
            attempts.append(
                {
                    "operation_ordinal": int(row["operation_ordinal"]),
                    "operation_id": row["operation_id"],
                    "request_id": row["request_id"],
                    "request_envelope": json.loads(row["request_envelope_json"]),
                    "request_digest": row["request_digest"],
                    "response_envelope": (
                        json.loads(row["response_envelope_json"])
                        if row["response_envelope_json"] is not None
                        else None
                    ),
                    "response_digest": row["response_digest"],
                    "http_status": row["http_status"],
                    "jsonrpc_error_present": (
                        None
                        if row["jsonrpc_error_present"] is None
                        else bool(row["jsonrpc_error_present"])
                    ),
                    "mcp_is_error": (
                        None if row["mcp_is_error"] is None else bool(row["mcp_is_error"])
                    ),
                    "nested_operation_success": (
                        None
                        if row["nested_operation_success"] is None
                        else bool(row["nested_operation_success"])
                    ),
                    "target_binding_match": row["target_binding_match"],
                    "parse_success": (
                        None if row["parse_success"] is None else bool(row["parse_success"])
                    ),
                    "semantic_success": (
                        None
                        if row["semantic_success"] is None
                        else bool(row["semantic_success"])
                    ),
                    "terminal_failure_code": row["terminal_failure_code"],
                    "business_effect_truth": row["business_effect_truth"],
                    "state": row["state"],
                }
            )
        return attempts

    def compute_public_projection(self, grant_run_id: str) -> dict[str, Any]:
        attempts = self.list_private_attempts(grant_run_id)
        protocol_call_count = int(
            self._connection.execute(
                "SELECT COUNT(*) AS count FROM protocol_ledger WHERE grant_run_id = ?",
                (grant_run_id,),
            ).fetchone()["count"]
        )
        # Attempt truth: every durably recorded business ordinal.
        business_attempt_count = len(attempts)
        # Transport truth: durable DISPATCHED ledger events only.
        business_call_count = int(
            self._connection.execute(
                """
                SELECT COUNT(*) AS count
                FROM business_ledger
                WHERE grant_run_id = ?
                  AND event_type = ?
                """,
                (grant_run_id, DISPATCHED),
            ).fetchone()["count"]
        )
        note_write_attempts = sum(
            1 for attempt in attempts if attempt["operation_id"] == "create-note"
        )
        note_writes_succeeded = sum(
            1
            for attempt in attempts
            if attempt["operation_id"] == "create-note"
            and attempt["semantic_success"] is True
        )
        stage_write_attempts = sum(
            1 for attempt in attempts if attempt["operation_id"] == "update-opportunity"
        )
        stage_writes_succeeded = sum(
            1
            for attempt in attempts
            if attempt["operation_id"] == "update-opportunity"
            and attempt["semantic_success"] is True
        )
        request_capture_count = sum(
            1 for attempt in attempts if attempt["request_envelope"] is not None
        )
        response_capture_count = sum(
            1 for attempt in attempts if attempt["response_envelope"] is not None
        )
        expected_initial_stage_verified = any(
            attempt["operation_ordinal"] == 2 and attempt["semantic_success"] is True
            for attempt in attempts
        )
        note_readback_verified = any(
            attempt["operation_id"] == "get-note" and attempt["semantic_success"] is True
            for attempt in attempts
        )
        final_stage_readback_verified = any(
            attempt["operation_ordinal"] == 6 and attempt["semantic_success"] is True
            for attempt in attempts
        )
        terminal_failure_code = next(
            (
                attempt["terminal_failure_code"]
                for attempt in reversed(attempts)
                if attempt["terminal_failure_code"]
            ),
            None,
        )
        has_unresolved_attempt = any(
            attempt["state"] in (ATTEMPT_RECORDED, DISPATCHED)
            or (
                attempt["state"] == RESPONSE_CAPTURED
                and not (
                    attempt["parse_success"] is True
                    and attempt["semantic_success"] is True
                )
            )
            for attempt in attempts
        )
        had_successful_or_plausible_write = any(
            attempt["operation_id"] in {"create-note", "update-opportunity"}
            and attempt["parse_success"] is True
            for attempt in attempts
        )
        if has_unresolved_attempt:
            business_effect_truth = "UNKNOWN"
        elif terminal_failure_code is not None:
            business_effect_truth = (
                "UNKNOWN" if had_successful_or_plausible_write else "NO"
            )
        elif (
            business_call_count == 6
            and expected_initial_stage_verified
            and note_readback_verified
            and final_stage_readback_verified
            and note_writes_succeeded == 1
            and stage_writes_succeeded == 1
        ):
            business_effect_truth = "YES"
        else:
            business_effect_truth = "NO"
        at1_complete = business_effect_truth == "YES"
        provenance = self._connection.execute(
            """
            SELECT transcript_digest, expected_note_digest, captured_before_ordinal
            FROM prewrite_provenance WHERE grant_run_id = ?
            """,
            (grant_run_id,),
        ).fetchone()
        create_note_attempt = next(
            (attempt for attempt in attempts if attempt["operation_id"] == "create-note"),
            None,
        )
        create_note_body_digest = None
        if create_note_attempt is not None:
            try:
                create_note_body = create_note_attempt["request_envelope"]["arguments"][
                    "params"
                ]["body"]["body"]
            except (KeyError, TypeError):
                create_note_body = None
            if isinstance(create_note_body, str):
                create_note_body_digest = hashlib.sha256(
                    create_note_body.encode("utf-8")
                ).hexdigest()
        create_note_payload = self._nested_payload(create_note_attempt)
        readback_note_attempt = next(
            (attempt for attempt in attempts if attempt["operation_id"] == "get-note"),
            None,
        )
        readback_note_payload = self._nested_payload(readback_note_attempt)
        created_note_id = (
            create_note_payload.get("note_id")
            if create_note_attempt is not None
            and create_note_attempt["parse_success"] is True
            else None
        )
        if not isinstance(created_note_id, str) or not created_note_id:
            created_note_id = None
        readback_note_id = (
            readback_note_payload.get("note_id")
            if readback_note_attempt is not None
            and readback_note_attempt["parse_success"] is True
            else None
        )
        readback_contact_id = (
            readback_note_payload.get("contact_id")
            if readback_note_attempt is not None
            and readback_note_attempt["parse_success"] is True
            else None
        )
        expected_contact_id = self._request_path_value(
            readback_note_attempt, "contactId"
        )
        readback_note_content = readback_note_payload.get("content_or_fingerprint")
        readback_note_digest = (
            hashlib.sha256(readback_note_content.encode("utf-8")).hexdigest()
            if isinstance(readback_note_content, str)
            else None
        )
        readback_note_id_match = (
            created_note_id is not None and readback_note_id == created_note_id
        )
        readback_contact_match = (
            isinstance(expected_contact_id, str)
            and bool(expected_contact_id)
            and readback_contact_id == expected_contact_id
        )
        note_content_match = (
            provenance is not None
            and readback_note_digest is not None
            and readback_note_digest == provenance["expected_note_digest"]
        )
        note_visible_under_exact_contact = (
            readback_note_attempt is not None
            and readback_note_attempt["nested_operation_success"] is True
            and readback_note_id_match
            and readback_contact_match
            and note_content_match
        )
        request_response_commitments = [
            {
                "operation_ordinal": attempt["operation_ordinal"],
                "operation_id": attempt["operation_id"],
                "request_id": attempt["request_id"],
                "request_commitment": attempt["request_digest"],
                "response_commitment": attempt["response_digest"],
                "OPERATION_ID": attempt["operation_id"],
                "HTTP_STATUS": (
                    attempt["http_status"]
                    if attempt["http_status"] is not None
                    else "UNKNOWN"
                ),
                "JSONRPC_ERROR_PRESENT": self._public_flag(
                    attempt["jsonrpc_error_present"]
                ),
                "MCP_IS_ERROR": self._public_flag(attempt["mcp_is_error"]),
                "NESTED_OPERATION_SUCCESS": self._public_flag(
                    attempt["nested_operation_success"]
                ),
                "TARGET_BINDING_MATCH": attempt["target_binding_match"] or "UNKNOWN",
                "REQUEST_EVIDENCE_PERSISTED": "YES",
                "RESPONSE_EVIDENCE_PERSISTED": (
                    "YES" if attempt["response_envelope"] is not None else "NO"
                ),
                "REQUEST_RESPONSE_CORRELATION_ID": attempt["request_id"],
                "SANITIZED_REQUEST_DIGEST": attempt["request_digest"],
                "SANITIZED_RESPONSE_DIGEST": attempt["response_digest"] or "UNKNOWN",
            }
            for attempt in attempts
        ]
        return {
            "protocol_call_count": protocol_call_count,
            "business_attempt_count": business_attempt_count,
            "business_call_count": business_call_count,
            "note_write_attempts": note_write_attempts,
            "note_writes_succeeded": note_writes_succeeded,
            "stage_write_attempts": stage_write_attempts,
            "stage_writes_succeeded": stage_writes_succeeded,
            "expected_initial_stage_verified": expected_initial_stage_verified,
            "note_readback_verified": note_readback_verified,
            "final_stage_readback_verified": final_stage_readback_verified,
            "request_capture_count": request_capture_count,
            "response_capture_count": response_capture_count,
            "retry_used": False,
            "terminal_failure_code": terminal_failure_code,
            "business_effect_truth": business_effect_truth,
            "at1_complete": at1_complete,
            "request_response_commitments": request_response_commitments,
            "TRANSCRIPT_INGESTED": "YES" if provenance is not None else "NO",
            "TRANSCRIPT_HASH_CAPTURED": "YES" if provenance is not None else "NO",
            "TRANSCRIPT_DERIVED_NOTE_HASH_CAPTURED_PREWRITE": (
                "YES" if provenance is not None else "NO"
            ),
            "EXPECTED_NOTE_SHA256_CAPTURED_PREWRITE": (
                "YES" if provenance is not None else "NO"
            ),
            "TRANSCRIPT_SHA256": (
                provenance["transcript_digest"] if provenance is not None else "UNKNOWN"
            ),
            "EXPECTED_NOTE_SHA256": (
                provenance["expected_note_digest"] if provenance is not None else "UNKNOWN"
            ),
            "CREATE_NOTE_BODY_SHA256": create_note_body_digest or "UNKNOWN",
            "CREATE_NOTE_BODY_SHA256_MATCHES_EXPECTED": (
                "YES"
                if provenance is not None
                and create_note_body_digest == provenance["expected_note_digest"]
                else "NO"
            ),
            "CREATED_NOTE_ID_PRESENT": "YES" if created_note_id is not None else "NO",
            "CREATED_NOTE_ID_FINGERPRINT": (
                self._commitment({"created_note_id": created_note_id})
                if created_note_id is not None
                else "UNKNOWN"
            ),
            "READBACK_NOTE_ID_MATCH": "YES" if readback_note_id_match else "NO",
            "READBACK_CONTACT_MATCH": "YES" if readback_contact_match else "NO",
            "READBACK_NOTE_SHA256": readback_note_digest or "UNKNOWN",
            "NOTE_CONTENT_MATCH": "YES" if note_content_match else "NO",
            "NOTE_CONTENT_COMPARATOR": "SHA256",
            "CRM_NOTE_VISIBLE_UNDER_EXACT_CONTACT": (
                "YES" if note_visible_under_exact_contact else "NO"
            ),
        }

    @staticmethod
    def _public_flag(value: bool | None) -> str:
        if value is None:
            return "UNKNOWN"
        return "YES" if value else "NO"

    @staticmethod
    def _nested_payload(attempt: Mapping[str, Any] | None) -> Mapping[str, Any]:
        if attempt is None:
            return {}
        response = attempt.get("response_envelope")
        if not isinstance(response, Mapping):
            return {}
        result = response.get("result")
        if not isinstance(result, Mapping):
            return {}
        content = result.get("content")
        if not isinstance(content, list) or not content or not isinstance(content[0], Mapping):
            return {}
        payload = content[0].get("payload")
        return payload if isinstance(payload, Mapping) else {}

    @staticmethod
    def _request_path_value(
        attempt: Mapping[str, Any] | None, key: str
    ) -> str | None:
        if attempt is None:
            return None
        request = attempt.get("request_envelope")
        if not isinstance(request, Mapping):
            return None
        try:
            value = request["arguments"]["params"]["path"][key]
        except (KeyError, TypeError):
            return None
        return value if isinstance(value, str) else None
