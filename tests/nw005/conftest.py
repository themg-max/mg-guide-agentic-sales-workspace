from __future__ import annotations

import json
from pathlib import Path

import pytest

from mg_guide.firestore_audit.models import ProjectionContext, default_stage_a_context

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "fixtures" / "nw005"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def nw005_fixtures() -> Path:
    return FIXTURES


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def load_packet(nw005_fixtures: Path):
    def _load(name: str):
        return _load_json(nw005_fixtures / "packets" / name)

    return _load


@pytest.fixture
def load_expected_audit(nw005_fixtures: Path):
    def _load(name: str):
        return _load_json(nw005_fixtures / "expected_audits" / name)

    return _load


@pytest.fixture
def stage_a_context_for():
    def _make(packet_filename: str) -> ProjectionContext:
        return default_stage_a_context(
            fixture_id=packet_filename,
            source_refs=[f"fixtures/nw005/packets/{packet_filename}"],
            recorded_at="2026-08-12T20:00:00Z",
            writer_component_version="0.1.0-stage-a",
        )

    return _make


TERMINAL_CASES = [
    (
        "packet-success.completed.json",
        "audit-success.completed.json",
        "completed",
    ),
    (
        "packet-stage-change-denied.completed_with_review.json",
        "audit-stage-change-denied.completed_with_review.json",
        "completed_with_review",
    ),
    (
        "packet-ambiguous-contact.blocked.json",
        "audit-ambiguous-contact.blocked.json",
        "blocked",
    ),
    (
        "packet-tool-failure.failed.json",
        "audit-tool-failure.failed.json",
        "failed",
    ),
]
