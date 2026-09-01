"""Bounded scenario allow-list for the public WebMCP competition surface.

Reuses the identical fixture sidecars already approved for the judge_surface
add-on. Only SUCCESS and AMBIGUOUS_CONTACT are exposed to the public WebMCP
route -- STAGE_CHANGE_DENIED remains judge_surface-only and is intentionally
not part of the public WebMCP contract to keep the public schema minimal.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES_DIR = REPO_ROOT / "fixtures"

WEBMCP_SCENARIOS: Dict[str, Path] = {
    "SUCCESS": FIXTURES_DIR / "transcript-success.expected.json",
    "AMBIGUOUS_CONTACT": FIXTURES_DIR / "transcript-ambiguous-contact.expected.json",
}


def webmcp_scenario_names() -> List[str]:
    return sorted(WEBMCP_SCENARIOS.keys())
