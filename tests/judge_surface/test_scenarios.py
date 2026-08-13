"""Tests for the fixed synthetic scenario catalog."""

from __future__ import annotations

from pathlib import Path

import pytest

from mg_guide.judge_surface.scenarios import (
    FIXTURES_DIR,
    REPO_ROOT,
    SCENARIO_CATALOG,
    judge_mode,
    scenario_catalog_hash,
    scenario_names,
)


@pytest.mark.parametrize("name", ["SUCCESS", "STAGE_CHANGE_DENIED", "AMBIGUOUS_CONTACT"])
def test_catalog_scenario_exists_and_points_to_file(name: str) -> None:
    path = SCENARIO_CATALOG[name]
    assert path.is_file(), f"missing fixture for {name}: {path}"
    assert path.suffix == ".json"


def test_catalog_hash_is_stable() -> None:
    h1 = scenario_catalog_hash()
    h2 = scenario_catalog_hash()
    assert h1 == h2
    assert len(h1) == 64


def test_scenario_names_are_fixed() -> None:
    names = scenario_names()
    assert names == ["AMBIGUOUS_CONTACT", "STAGE_CHANGE_DENIED", "SUCCESS"]


def test_judge_mode_defaults_to_stub(monkeypatch) -> None:
    monkeypatch.delenv("MEETING_CONTEXT_GEMINI_MODE", raising=False)
    assert judge_mode() == "stub"


def test_judge_mode_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("MEETING_CONTEXT_GEMINI_MODE", "STUB")
    assert judge_mode() == "stub"
