"""Security helpers for the Workspace add-on adapter."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Sequence

# Three base64url segments separated by dots — rough JWT shape.
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")

# Patterns that indicate raw token logging in Apps Script sources.
_FORBIDDEN_LOG_PATTERNS = (
    re.compile(r"console\.log\s*\(\s*[\"']Identity Token", re.I),
    re.compile(r"console\.log\s*\(\s*[\"'].*token.*[\"']\s*\+", re.I),
    re.compile(r"Logger\.log\s*\(\s*.*getIdentityToken", re.I),
    re.compile(r"console\.log\s*\(\s*.*getIdentityToken\s*\(", re.I),
    re.compile(r"console\.log\s*\(\s*[\"']Token type:", re.I),
    re.compile(r"Raw token value", re.I),
)


def scan_text_for_token_leak(text: str) -> List[str]:
    """Return human-readable findings if token-like material appears."""
    findings: List[str] = []
    if _JWT_RE.search(text):
        findings.append("jwt_shaped_token_present")
    for pattern in _FORBIDDEN_LOG_PATTERNS:
        if pattern.search(text):
            findings.append(f"forbidden_log_pattern:{pattern.pattern}")
    return findings


def assert_no_raw_token_logging(paths: Sequence[Path]) -> None:
    """Fail if competition add-on sources log raw identity tokens."""
    problems: List[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for finding in scan_text_for_token_leak(text):
            # Allow documentation of the forbidden pattern itself.
            if path.suffix == ".md":
                continue
            problems.append(f"{path}:{finding}")
    if problems:
        raise AssertionError(
            "RAW_IDENTITY_TOKEN_LOGGING_PRESENT — " + "; ".join(problems)
        )


def competition_apps_script_paths(repo_root: Path) -> List[Path]:
    root = repo_root / "workspace_addon"
    return sorted(p for p in root.glob("*.gs") if p.is_file())
