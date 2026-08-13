"""Schema validation for workflow_run_audit_v1 projections."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from jsonschema import Draft202012Validator, FormatChecker


class AuditValidationError(ValueError):
    """Raised when a projected audit fails schema or invariant checks."""

    def __init__(self, messages: List[str]) -> None:
        super().__init__("; ".join(messages))
        self.messages = messages


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def _audit_validator() -> Draft202012Validator:
    schema_path = _repo_root() / "contracts" / "workflow_run_audit.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    # Create a FormatChecker with a date-time checker that accepts RFC3339-like
    # strings. The stdlib datetime.fromisoformat accepts offsets but not trailing
    # Z; normalize Z to +00:00 and try parsing. Register this checker under
    # 'date-time' so schema format: date-time is enforced.
    fc = FormatChecker()

    @fc.checks("date-time")
    def _is_datetime(instance: str) -> bool:  # type: ignore
        from datetime import datetime

        if not isinstance(instance, str):
            # Non-strings are type-errors elsewhere; format checks only for strs.
            return True
        try:
            sval = instance
            if sval.endswith("Z"):
                sval = sval[:-1] + "+00:00"
            # datetime.fromisoformat handles the offset form produced above
            datetime.fromisoformat(sval)
            return True
        except Exception:
            return False

    return Draft202012Validator(schema, format_checker=fc)


def schema_errors(audit: Mapping[str, Any]) -> List[str]:
    messages: List[str] = []
    for error in sorted(_audit_validator().iter_errors(audit), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "<root>"
        messages.append(f"{path}: {error.message}")
    return messages


def invariant_errors(audit: Mapping[str, Any]) -> List[str]:
    """Extra fail-closed invariants beyond JSON Schema."""
    messages: List[str] = []
    # Transcript body must never appear.
    blob = json.dumps(audit, ensure_ascii=False)
    banned_keys = ("transcript_body", "transcript_text", "raw_transcript")
    for key in banned_keys:
        if key in blob:
            messages.append(f"forbidden transcript field present: {key}")

    integrity = audit.get("integrity") if isinstance(audit.get("integrity"), Mapping) else {}
    for field in ("projection_input_fingerprint", "content_fingerprint"):
        value = integrity.get(field)
        if not isinstance(value, str) or len(value) != 64:
            messages.append(f"integrity.{field} must be 64-char hex")

    # Fingerprints must not be embedded elsewhere (non-recursive definition).
    if "integrity" in json.dumps(
        {k: v for k, v in audit.items() if k != "integrity"}, ensure_ascii=False
    ):
        # only flag if nested integrity key exists outside top-level
        def _walk(obj: Any, path: str = "") -> None:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    p = f"{path}.{k}" if path else k
                    if k == "integrity" and path != "":
                        messages.append(f"nested integrity object at {p}")
                    _walk(v, p)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    _walk(item, f"{path}[{i}]")

        _walk({k: v for k, v in audit.items() if k != "integrity"})

    idem = audit.get("idempotency") if isinstance(audit.get("idempotency"), Mapping) else {}
    if idem.get("key") != audit.get("run_id"):
        messages.append("idempotency.key must equal run_id")

    return messages


def validate_workflow_run_audit(audit: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate audit document; return a shallow copy on success."""
    if not isinstance(audit, Mapping):
        raise AuditValidationError(["audit must be an object"])
    messages = schema_errors(audit) + invariant_errors(audit)
    if messages:
        raise AuditValidationError(messages)
    return dict(audit)


def is_valid_workflow_run_audit(audit: Mapping[str, Any]) -> Tuple[bool, List[str]]:
    try:
        validate_workflow_run_audit(audit)
        return True, []
    except AuditValidationError as exc:
        return False, list(exc.messages)
