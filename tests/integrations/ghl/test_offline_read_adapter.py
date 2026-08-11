from __future__ import annotations

import json
from pathlib import Path

import pytest

from integrations.ghl import (
    OfflineGhlReadAdapter,
    OperationNotAllowedError,
    RequestMappingError,
)


FIXTURES = Path(__file__).resolve().parents[3] / "fixtures" / "ghl"


def test_builds_discovered_mcp_request_envelope() -> None:
    envelope = OfflineGhlReadAdapter().build_request(
        "search-contacts-advanced",
        body={"pageLimit": 20, "query": "Avery Demo"},
    )

    assert envelope == {
        "tool": "execute_operation",
        "arguments": {
            "operationId": "search-contacts-advanced",
            "params": {
                "path": {},
                "query": {},
                "body": {"pageLimit": 20, "query": "Avery Demo"},
            },
        },
    }


@pytest.mark.parametrize("operation_id", ["create-note", "update-opportunity"])
def test_explicitly_denies_mutation_operations(operation_id: str) -> None:
    with pytest.raises(OperationNotAllowedError, match="explicitly denied"):
        OfflineGhlReadAdapter().build_request(operation_id)


def test_rejects_unapproved_operations_and_parameters() -> None:
    adapter = OfflineGhlReadAdapter()

    with pytest.raises(OperationNotAllowedError, match="allowlist"):
        adapter.build_request("get-all-notes")
    with pytest.raises(RequestMappingError, match="requires body fields"):
        adapter.build_request("search-contacts-advanced", body={})
    with pytest.raises(RequestMappingError, match="Unsupported query"):
        adapter.build_request("get-contact", query={"contactId": "demo-contact-001"})


def test_fixture_replay_is_deterministic_and_normalized() -> None:
    fixture = json.loads((FIXTURES / "offline-read-replay.json").read_text())
    expected = json.loads((FIXTURES / "offline-read-replay.expected.json").read_text())

    first = OfflineGhlReadAdapter().replay_fixture(fixture)
    second = OfflineGhlReadAdapter().replay_fixture(fixture)

    assert first == second
    summary = []
    for result in first:
        normalized = result["result"]
        entry = {"case_id": result["case_id"], "status": normalized["status"]}
        if normalized["records"]:
            entry["record_id"] = normalized["records"][0]["id"]
            entry["next_cursor"] = normalized["pagination"]["next_cursor"]
        if normalized["error"]:
            entry["error_code"] = normalized["error"]["code"]
        summary.append(entry)
    assert summary == expected


def test_contact_opportunity_and_pipeline_shapes_are_canonical() -> None:
    fixture = json.loads((FIXTURES / "offline-read-replay.json").read_text())
    results = OfflineGhlReadAdapter().replay_fixture(fixture)

    contact, opportunity, pipeline = [result["result"] for result in results[:3]]
    assert contact["records"][0] == {
        "id": "demo-contact-001",
        "first_name": "Avery",
        "last_name": "Demo",
        "email": "avery@example-demo.test",
        "phone": "+15550000001",
        "company_name": "Demo Co",
    }
    assert opportunity["records"][0]["pipeline_stage_id"] == "demo-stage-discovery"
    assert pipeline["records"][0]["stages"] == [
        {"id": "demo-stage-discovery", "name": "Discovery", "position": 1}
    ]
