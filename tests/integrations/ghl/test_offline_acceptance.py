from __future__ import annotations

import json
from pathlib import Path

from integrations.ghl import OfflineGhlReadAdapter


def test_synthetic_read_adapter_acceptance_fixture_has_no_external_transport() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    fixture = json.loads(
        (repo_root / "fixtures" / "ghl" / "offline-read-replay.json").read_text()
    )

    results = OfflineGhlReadAdapter().replay_fixture(fixture)

    assert fixture["source"] == "synthetic_only"
    assert [result["result"]["status"] for result in results] == [
        "ok",
        "ok",
        "ok",
        "not_found",
        "error",
    ]
    assert all(
        result["request"]["tool"] == "execute_operation" for result in results
    )
