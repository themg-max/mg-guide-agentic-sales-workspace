"""JSON Schema validation for relationship_context_v1."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from jsonschema import Draft202012Validator


def _repo_root() -> Path:
    # src/agents/relationship_context/schema.py -> repo root
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def load_relationship_context_schema() -> Dict[str, Any]:
    path = _repo_root() / "contracts" / "relationship_context.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_relationship_context(
    payload: Mapping[str, Any],
) -> Tuple[bool, Tuple[str, ...]]:
    """Validate payload against relationship_context.schema.json.

    Returns (ok, error_messages).
    """
    validator = Draft202012Validator(load_relationship_context_schema())
    errors = sorted(validator.iter_errors(dict(payload)), key=lambda e: list(e.path))
    if not errors:
        return True, tuple()
    messages = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        messages.append(f"{path}: {err.message}")
    return False, tuple(messages)
