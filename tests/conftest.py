from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def packet_schema(repo_root: Path):
    schema = json.loads(
        (repo_root / "contracts" / "meeting_follow_up_packet.schema.json").read_text(
            encoding="utf-8"
        )
    )
    resource = Resource.from_contents(schema)
    registry = Registry().with_resource(schema["$id"], resource)
    return Draft202012Validator(schema, registry=registry)


@pytest.fixture(scope="session")
def workflow_contract(repo_root: Path):
    return yaml.safe_load(
        (repo_root / "contracts" / "workflow_states.yaml").read_text(encoding="utf-8")
    )


@pytest.fixture(scope="session")
def failure_codes(repo_root: Path):
    return yaml.safe_load(
        (repo_root / "contracts" / "failure_codes.yaml").read_text(encoding="utf-8")
    )
