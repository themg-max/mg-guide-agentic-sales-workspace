"""Tests for safe extraction of the Agent Runtime source candidate."""

from __future__ import annotations

import gzip
import io
import tarfile
import zipfile
from pathlib import Path

import pytest

from scripts.build_agent_runtime_source import PackageFile, write_archive
from scripts.verify_agent_runtime_source_package import (
    require_tar_gzip_bytes,
    validate_archive_members,
)


def _member(path: str, *, typeflag: bytes = tarfile.REGTYPE) -> tarfile.TarInfo:
    member = tarfile.TarInfo(name=path)
    member.type = typeflag
    member.mode = 0o644
    member.size = 0
    return member


@pytest.mark.parametrize(
    "path",
    (
        "/absolute/path.py",
        r"\absolute\path.py",
        r"C:\absolute\path.py",
        "src/../../escape.py",
        r"src\..\..\escape.py",
    ),
)
def test_source_archive_rejects_absolute_and_traversal_paths(path: str) -> None:
    with pytest.raises(ValueError):
        validate_archive_members(
            [_member(path), _member("SOURCE_MANIFEST.sha256")]
        )


def test_source_archive_rejects_symlink_entry() -> None:
    with pytest.raises(ValueError, match="symlink"):
        validate_archive_members(
            [
                _member("link.py", typeflag=tarfile.SYMTYPE),
                _member("SOURCE_MANIFEST.sha256"),
            ]
        )


def test_source_archive_accepts_regular_relative_entries() -> None:
    names = validate_archive_members(
        [_member("app/agent.py"), _member("SOURCE_MANIFEST.sha256")]
    )

    assert names == ["app/agent.py", "SOURCE_MANIFEST.sha256"]


def test_require_tar_gzip_rejects_zip_magic() -> None:
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("SOURCE_MANIFEST.sha256", "x\n")
    with pytest.raises(ValueError, match="ZIP"):
        require_tar_gzip_bytes(payload.getvalue())


def test_require_tar_gzip_rejects_non_gzip() -> None:
    with pytest.raises(ValueError, match="gzip-compressed TAR"):
        require_tar_gzip_bytes(b"not-an-archive")


def test_write_archive_is_deterministic_gzip_tar(tmp_path: Path) -> None:
    files = (
        PackageFile(
            source_path="deployment/agent-runtime/app/agent.py",
            archive_path="app/agent.py",
            content=b"root = None\n",
        ),
        PackageFile(
            source_path="deployment/agent-runtime/requirements.txt",
            archive_path="requirements.txt",
            content=b"google-adk==1.18.0\n",
        ),
    )
    first = tmp_path / "a.tar.gz"
    second = tmp_path / "b.tar.gz"
    write_archive(first, files)
    write_archive(second, files)

    first_bytes = first.read_bytes()
    second_bytes = second.read_bytes()
    assert first_bytes == second_bytes
    assert first_bytes.startswith(b"\x1f\x8b")
    assert not first_bytes.startswith(b"PK")
    require_tar_gzip_bytes(first_bytes)
    gzip.decompress(first_bytes)

    with tarfile.open(first, mode="r:gz") as archive:
        names = validate_archive_members(archive.getmembers())
    assert "app/agent.py" in names
    assert "requirements.txt" in names
    assert "SOURCE_MANIFEST.sha256" in names

