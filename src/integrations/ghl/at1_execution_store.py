"""Durable local execution state for offline AT-1 bounded transport evidence."""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import hmac
import json
from pathlib import Path
import sqlite3
from typing import Any


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


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class At1ExecutionStore:
    """SQLite-backed local execution store for AT-1 transport/evidence contracts."""

    def __init__(self, db_path: str | Path, commitment_key: str) -> None:
        if not isinstance(commitment_key, str) or not commitment_key.strip():
            raise ValueError("commitment_key must be a non-empty string")
        self._commitment_key = commitment_key.encode("utf-8")
        self._db_path = str(db_path)
        self._connection = sqlite3.connect(
            self._db_path,
            isolation_level=None,
            timeout=30.0,
            check_same_thread=False,
        )
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    @property
    def db_path(self) -> str:
        return self._db_path

    def _initialize_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS execution_claims (
                grant_run_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                claimed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS attempts (
                grant_run_id TEXT NOT NULL,
                operation_ordinal INTEGER NOT NULL,
                operation_id TEXT NOT NULL,
                request_id TEXT NOT NULL,
                request_envelope_json TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                response_envelope_json TEXT,
                response_digest TEXT,
                parse_success INTEGER,
                semantic_success INTEGER,
                terminal_failure_code TEXT,
                business_effect_truth TEXT,
                state TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (grant_run_id, operation_ordinal),
                UNIQUE (grant_run_id, request_id)
            );

            CREATE TABLE IF NOT EXISTS protocol_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grant_run_id TEXT NOT NULL,
                call_name TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS business_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grant_run_id TEXT NOT NULL,
                operation_ordinal INTEGER NOT NULL,
                operation_id TEXT NOT NULL,
                request_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                request_digest TEXT,
                response_digest TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

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

    def record_parse_outcome(
        self, *, grant_run_id: str, operation_ordinal: int, success: bool
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET parse_success = ?, updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (1 if success else 0, grant_run_id, operation_ordinal),
            )
            if cursor.rowcount != 1:
                raise AttemptStateError(
                    f"cannot record parse outcome for ordinal {operation_ordinal}"
                )

    def record_semantic_outcome(
        self, *, grant_run_id: str, operation_ordinal: int, success: bool
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE attempts
                SET semantic_success = ?, updated_at = CURRENT_TIMESTAMP
                WHERE grant_run_id = ? AND operation_ordinal = ?
                """,
                (1 if success else 0, grant_run_id, operation_ordinal),
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
        business_call_count = len(attempts)
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
        has_unresolved_dispatch = any(
            attempt["state"] == DISPATCHED and attempt["response_envelope"] is None
            for attempt in attempts
        )
        if has_unresolved_dispatch:
            business_effect_truth = "UNKNOWN"
        elif terminal_failure_code is not None:
            business_effect_truth = "NO"
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
        request_response_commitments = [
            {
                "operation_ordinal": attempt["operation_ordinal"],
                "operation_id": attempt["operation_id"],
                "request_id": attempt["request_id"],
                "request_commitment": attempt["request_digest"],
                "response_commitment": attempt["response_digest"],
            }
            for attempt in attempts
        ]
        return {
            "protocol_call_count": protocol_call_count,
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
        }
