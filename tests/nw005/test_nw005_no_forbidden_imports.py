from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = REPO_ROOT / "src" / "mg_guide" / "firestore_audit"

FORBIDDEN_PREFIXES = (
    "orchestration",
    "agents",
    "integrations",
    "mg_guide.meeting_follow_up_card",
    "google.adk",
    "google.auth",
    "google.genai",
    "firebase",
    "requests",
    "httpx",
    "urllib.request",
    "urllib3",
    "aiohttp",
    "socket",
    "subprocess",
)

FORBIDDEN_NAMES = {
    "google.adk",
    "google.auth",
    "google.genai",
    "firebase",
    "requests",
    "httpx",
    "urllib.request",
    "urllib3",
    "aiohttp",
    "socket",
    "subprocess",
}

# Stage B introduces a single bounded Firestore adapter module. It is the only
# module permitted to import the Firestore client.
FIRESTORE_ADAPTER_FILES = {"firestore_store.py"}


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
    py_files = sorted(MODULE_DIR.glob("*.py"))
    assert py_files, "firestore_audit package missing"
    for path in py_files:
        is_firestore_adapter = path.name in FIRESTORE_ADAPTER_FILES
        for imported in _imports_from(path):
            # The Stage B adapter is allowed to import google.cloud.firestore.
            if is_firestore_adapter and imported == "google.cloud.firestore":
                continue
            assert imported not in FORBIDDEN_NAMES, f"{path.name} imports {imported}"
            assert not imported.startswith(FORBIDDEN_PREFIXES), (
                f"{path.name} imports forbidden module: {imported}"
            )


def test_google_cloud_firestore_dependency_declared():
    req = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "google-cloud-firestore" in req
    assert "google-cloud-firestore" in pyproject


def test_module_source_has_no_network_or_env_credential_reads():
    banned_snippets = (
        "os.environ",
        "os.getenv",
        "getenv(",
        "default(",
        "google.auth",
        "from_service_account",
        "requests.",
        "urlopen",
    )
    for path in MODULE_DIR.glob("*.py"):
        # The Stage B adapter legitimately constructs a firestore.Client; only
        # the ADC-backed constructor is permitted.
        if path.name in FIRESTORE_ADAPTER_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in banned_snippets:
            # allow comments mentioning forbidden items in docs
            code_lines = [
                ln
                for ln in text.splitlines()
                if not ln.strip().startswith("#") and '"""' not in ln and "'''" not in ln
            ]
            joined = "\n".join(code_lines)
            assert snippet not in joined, f"{path.name} contains banned snippet {snippet!r}"
