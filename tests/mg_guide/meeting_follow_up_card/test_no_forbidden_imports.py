from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_PREFIXES = (
    "orchestration.policy",
    "orchestration.runner",
    "orchestration.state_machine",
    "agents",
    "integrations",
    "google.cloud",
    "google.adk",
    "firebase",
    "firestore",
    "requests",
    "httpx",
    "urllib.request",
)

REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_DIR = REPO_ROOT / "src" / "mg_guide" / "meeting_follow_up_card"


def _imports_from(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def test_forbidden_import_guard():
    for path in MODULE_DIR.glob("*.py"):
        for imported in _imports_from(path):
            assert not imported.startswith(FORBIDDEN_PREFIXES), (
                f"{path.name} imports forbidden module: {imported}"
            )

