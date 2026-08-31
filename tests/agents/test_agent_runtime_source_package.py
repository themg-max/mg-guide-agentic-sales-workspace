"""Tests for safe extraction of the Agent Runtime source candidate."""

from __future__ import annotations

import stat
import zipfile

import pytest

from scripts.verify_agent_runtime_source_package import validate_archive_members


def _member(path: str, *, mode: int = 0o100644) -> zipfile.ZipInfo:
    member = zipfile.ZipInfo(path)
    member.create_system = 3
    member.external_attr = mode << 16
    return member


def _archive_members(
    tmp_path, members: list[zipfile.ZipInfo]
) -> list[zipfile.ZipInfo]:
    archive_path = tmp_path / "candidate.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for member in members:
            archive.writestr(member, "")
    with zipfile.ZipFile(archive_path) as archive:
        return archive.infolist()


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
def test_source_archive_rejects_absolute_and_traversal_paths(
    tmp_path, path: str
) -> None:
    with pytest.raises(ValueError):
        validate_archive_members(
            _archive_members(
                tmp_path, [_member(path), _member("SOURCE_MANIFEST.sha256")]
            )
        )


def test_source_archive_rejects_symlink_entry(tmp_path) -> None:
    with pytest.raises(ValueError, match="symlink"):
        validate_archive_members(
            _archive_members(
                tmp_path,
                [
                    _member("link.py", mode=stat.S_IFLNK | 0o777),
                    _member("SOURCE_MANIFEST.sha256"),
                ],
            )
        )


def test_source_archive_accepts_regular_relative_entries(tmp_path) -> None:
    names = validate_archive_members(
        _archive_members(
            tmp_path, [_member("app/agent.py"), _member("SOURCE_MANIFEST.sha256")]
        )
    )

    assert names == ["app/agent.py", "SOURCE_MANIFEST.sha256"]
