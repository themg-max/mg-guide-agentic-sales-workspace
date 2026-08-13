"""nw005_canonical_json_v1 — packet-local canonical JSON (not RFC 8785)."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any

CANONICALIZER_ID = "nw005_canonical_json_v1"


class CanonicalizationError(ValueError):
    """Raised when a value cannot be represented under nw005_canonical_json_v1."""


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise CanonicalizationError(
            "nw005_canonical_json_v1 rejects non-integer numbers "
            f"(got float {value!r}); schema numbers are integers only"
        )
    if isinstance(value, dict):
        # Sort by Unicode code point of NFC-normalized keys.
        items = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(
                    f"object keys must be strings, got {type(key).__name__}"
                )
            items.append((unicodedata.normalize("NFC", key), _normalize(item)))
        items.sort(key=lambda kv: tuple(ord(ch) for ch in kv[0]))
        return {k: v for k, v in items}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    raise CanonicalizationError(
        f"unsupported type for nw005_canonical_json_v1: {type(value).__name__}"
    )


def nw005_canonical_json_v1(value: Any) -> bytes:
    """Serialize *value* to canonical UTF-8 JSON bytes.

    Rules (frozen PR #17 / NW-005 Decision 1c):
    1. UTF-8 encoding; strings NFC-normalized before serialization.
    2. Object keys sorted by Unicode code point, recursively.
    3. No insignificant whitespace; separators exactly ``,`` and ``:``.
    4. Strings use minimal JSON escaping (``\\"``, ``\\\\``, and ``\\uXXXX``
       for control characters only).
    5. All numbers are integers; no decimal point, no exponent.
    6. Arrays preserve field-defined order.

    This is **not** RFC 8785 (JCS). No conformance claim is made.
    """
    normalized = _normalize(value)
    text = json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return text.encode("utf-8")


def fingerprint_hex(value: Any) -> str:
    """SHA-256 lowercase hex of nw005_canonical_json_v1(value)."""
    return hashlib.sha256(nw005_canonical_json_v1(value)).hexdigest()
