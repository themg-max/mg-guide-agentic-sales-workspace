"""Fixed synthetic scenario catalog for the judge-safe demo surface.

The catalog maps a bounded set of scenario selectors to existing fixture
sidecars.  No arbitrary transcript, run_id, or customer input is accepted.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES_DIR = REPO_ROOT / "fixtures"


def _sidecar(name: str) -> Path:
    return FIXTURES_DIR / name


# Scenario selector -> fixture sidecar path.
# SUCCESS and STAGE_CHANGE_DENIED are required; AMBIGUOUS_CONTACT is included
# because the existing deterministic runner already produces it cleanly.
SCENARIO_CATALOG: Dict[str, Path] = {
    "SUCCESS": _sidecar("transcript-success.expected.json"),
    "STAGE_CHANGE_DENIED": _sidecar("transcript-no-stage-change.expected.json"),
    "AMBIGUOUS_CONTACT": _sidecar("transcript-ambiguous-contact.expected.json"),
}

AUTHORIZED_JUDGE_MODE = "stub"


def judge_mode() -> str:
    """Return the active judge mode.

    Only the approved STUB judge mode is permitted for the repository-only B1
    implementation. Any other environment value is rejected to preserve a
    fail-closed runtime.
    """
    value = os.environ.get("MEETING_CONTEXT_GEMINI_MODE", AUTHORIZED_JUDGE_MODE)
    mode = (value or AUTHORIZED_JUDGE_MODE).strip().lower()
    if mode != AUTHORIZED_JUDGE_MODE:
        raise ValueError(
            "MEETING_CONTEXT_GEMINI_MODE must be 'stub'; got "
            f"{value!r} (normalized={mode!r})"
        )
    return mode


def scenario_names() -> List[str]:
    """Return the fixed scenario selector list in deterministic order."""
    return sorted(SCENARIO_CATALOG.keys())


def scenario_catalog_hash() -> str:
    """Deterministic hash of the scenario catalog for healthz provenance."""
    catalog = {
        name: str(path.relative_to(REPO_ROOT))
        for name, path in sorted(SCENARIO_CATALOG.items())
    }
    payload = json.dumps(catalog, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
