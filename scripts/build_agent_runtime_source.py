#!/usr/bin/env python3
"""Build the deterministic MG Guide Agent Runtime source archive."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SYNTHETIC_CRM_FIXTURE = "fixtures/ghl/relationship-context-crm.json"

EXACT_PATHS = (
    "deployment/agent-runtime/app/__init__.py",
    "deployment/agent-runtime/app/agent.py",
    "deployment/agent-runtime/requirements.txt",
    "src/integrations/__init__.py",
    "src/integrations/ghl/read_adapter.py",
    "src/orchestration/__init__.py",
    "src/orchestration/attempt_ledger.py",
    "src/orchestration/models.py",
    "src/orchestration/policy.py",
    "src/orchestration/runner.py",
    "src/orchestration/state_machine.py",
    "contracts/follow_up_proposal.schema.json",
    "contracts/meeting_context.schema.json",
    "contracts/meeting_follow_up_packet.schema.json",
    "contracts/nw008_longitudinal_context.schema.json",
    "contracts/relationship_context.schema.json",
    "contracts/workflow_states.yaml",
    SYNTHETIC_CRM_FIXTURE,
    "fixtures/transcript-success.expected.json",
    "fixtures/transcript-success.txt",
)
RECURSIVE_PYTHON_ROOTS = (
    "src/agents/adk_runtime",
    "src/agents/follow_up_planning",
    "src/agents/meeting_context",
    "src/agents/relationship_context",
)
FORBIDDEN_PATH_PARTS = {
    ".git",
    ".terraform",
    "__pycache__",
    ".pytest_cache",
    "artifacts",
    "traces",
}
FORBIDDEN_FILENAMES = {
    ".env",
    "terraform.tfstate",
    "credentials.json",
    "service-account.json",
}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb'"private_key"\s*:'),
    re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}\b"),
)


@dataclass(frozen=True)
class PackageFile:
    source_path: str
    archive_path: str
    content: bytes


def git_output(args: Sequence[str]) -> bytes:
    return subprocess.check_output(["git", *args])


def tracked_paths(source_commit: str, root: str) -> Iterable[str]:
    output = git_output(["ls-tree", "-r", "--name-only", source_commit, "--", root])
    for line in output.decode("utf-8").splitlines():
        if line.endswith(".py"):
            yield line


def archive_path(source_path: str) -> str:
    if source_path.startswith("deployment/agent-runtime/"):
        return source_path.removeprefix("deployment/agent-runtime/")
    return source_path


def validate_path(path: str) -> None:
    parts = set(Path(path).parts)
    if parts & FORBIDDEN_PATH_PARTS:
        raise ValueError(f"forbidden package path: {path}")
    if Path(path).name in FORBIDDEN_FILENAMES:
        raise ValueError(f"forbidden package file: {path}")
    if path.endswith((".tfstate", ".tfstate.backup", ".pem", "-key.json")):
        raise ValueError(f"forbidden package file type: {path}")


def read_package_files(source_commit: str) -> list[PackageFile]:
    source_paths = set(EXACT_PATHS)
    source_paths.add("src/agents/__init__.py")
    for root in RECURSIVE_PYTHON_ROOTS:
        source_paths.update(tracked_paths(source_commit, root))

    package_files: list[PackageFile] = []
    for source_path in sorted(source_paths):
        validate_path(source_path)
        content = git_output(["show", f"{source_commit}:{source_path}"])
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                raise ValueError(f"secret-like content in package file: {source_path}")
        package_files.append(
            PackageFile(
                source_path=source_path,
                archive_path=archive_path(source_path),
                content=content,
            )
        )

    fixture = next(
        item for item in package_files if item.source_path == SYNTHETIC_CRM_FIXTURE
    )
    if b'"source": "synthetic_only"' not in fixture.content:
        raise ValueError("CRM fixture is not explicitly marked synthetic_only")
    return package_files


def manifest_bytes(files: Sequence[PackageFile]) -> bytes:
    lines = [
        f"{hashlib.sha256(item.content).hexdigest()}  {item.archive_path}"
        for item in files
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def write_archive(output: Path, files: Sequence[PackageFile]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        entries = [(item.archive_path, item.content) for item in files]
        entries.append(("SOURCE_MANIFEST.sha256", manifest_bytes(files)))
        for path, content in sorted(entries):
            info = zipfile.ZipInfo(path, date_time=FIXED_ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source_commit = git_output(["rev-parse", f"{args.source_commit}^{{commit}}"]).decode(
        "ascii"
    ).strip()
    files = read_package_files(source_commit)
    write_archive(args.output, files)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"SOURCE_BASE_COMMIT={source_commit}")
    print(f"SOURCE_PACKAGE_SHA256={digest}")
    print(f"SOURCE_PACKAGE_SIZE_BYTES={args.output.stat().st_size}")
    print(f"SOURCE_PACKAGE_FILE_COUNT={len(files) + 1}")


if __name__ == "__main__":
    main()
