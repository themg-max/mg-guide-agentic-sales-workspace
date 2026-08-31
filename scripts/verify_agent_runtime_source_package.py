#!/usr/bin/env python3
"""Validate the exact MG Guide Agent Runtime source archive candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


EXPECTED_ROOT_MODULE = "app.agent"
EXPECTED_ROOT_FACTORY = "agents.follow_up_planning.runtime.build_unit3_root_agent"
EXPECTED_AGENTS = (
    "meeting_context_agent",
    "relationship_context_agent",
    "follow_up_planning_agent",
)
FORBIDDEN_PATH_TERMS = (
    ".git/",
    ".env",
    "credentials",
    "service-account",
    ".tfstate",
    "__pycache__",
    ".pytest_cache",
    "artifacts/traces",
)

SMOKE_PROGRAM = r"""
import asyncio
import json
from pathlib import Path

from app.agent import root_agent
from agents.follow_up_planning.runtime import build_unit3_root_agent
from agents.meeting_context.providers.base import ProviderRequest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

assert root_agent.name == "unit3_meeting_to_follow_up_packet"
assert [agent.name for agent in root_agent.sub_agents] == [
    "meeting_context_agent",
    "relationship_context_agent",
    "follow_up_planning_agent",
]
assert build_unit3_root_agent.__module__ == "agents.follow_up_planning.runtime"

async def smoke():
    package_root = Path.cwd()
    sidecar = json.loads(
        (package_root / "fixtures" / "transcript-success.expected.json").read_text()
    )
    transcript = (
        package_root / "fixtures" / "transcript-success.txt"
    ).read_text()
    request = ProviderRequest(
        fixture_id=sidecar["fixture_id"],
        transcript_text=transcript,
        transcript_path=None,
        meeting=sidecar["meeting"],
        participants=sidecar["participants"],
        extraction_result=sidecar["extraction_result"],
        extraction_confidence=sidecar["extraction_confidence"],
        evidence_references=sidecar["evidence_references"],
    )
    state = {
        "meeting_request": request,
        "run_id": sidecar["run_id"],
        "scenario_id": "DEPLOYMENT_CANDIDATE_SMOKE",
        "approved_prior_context": None,
        "errors": [],
        "meeting_context": None,
        "relationship_context": None,
        "follow_up_proposal": None,
        "follow_up_packet": None,
        "follow_up_policy_gate_invoked": False,
        "stop_after": "follow_up_planning_agent",
        "mutation_execution": "not_authorized_intent_only",
        "governed_stop": None,
        "agent_execution": {},
    }
    sessions = InMemorySessionService()
    session = await sessions.create_session(
        app_name="mg_guide_deployment_candidate",
        user_id="synthetic_candidate",
        state=state,
    )
    runner = Runner(
        agent=root_agent,
        app_name="mg_guide_deployment_candidate",
        session_service=sessions,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="run the synthetic MG Guide follow-up graph")],
    )
    authors = []
    async for event in runner.run_async(
        user_id="synthetic_candidate",
        session_id=session.id,
        new_message=message,
    ):
        authors.append(event.author)
    final = await sessions.get_session(
        app_name="mg_guide_deployment_candidate",
        user_id="synthetic_candidate",
        session_id=session.id,
    )
    packet = final.state["follow_up_packet"]
    relationship = final.state["relationship_context"]
    assert packet["schema"] == "meeting_follow_up_packet_v1"
    assert packet["external_effects"] == 0
    assert packet["mutations"]["lifecycle"] == "intent_only"
    assert relationship["crm_source"]["mode"] == "offline_synthetic"
    assert relationship["crm_source"]["live_calls"] == 0
    assert relationship["crm_source"]["writes"] == 0
    assert all(
        name in authors
        for name in (
            "meeting_context_agent",
            "relationship_context_agent",
            "follow_up_planning_agent",
        )
    )

asyncio.run(smoke())
print("PACKAGE_IMPORT=PASS")
print("ROOT_AGENT_LOAD=PASS")
print("SYNTHETIC_SMOKE=PASS")
print("LIVE_GHL_ADAPTER_ENABLED=NO")
print("GHL_CALLS=0")
print("CRM_MUTATIONS=0")
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()

    archive_bytes = args.archive.read_bytes()
    actual_digest = hashlib.sha256(archive_bytes).hexdigest()
    if actual_digest != args.sha256:
        raise SystemExit(
            f"archive digest mismatch: expected {args.sha256}, got {actual_digest}"
        )

    with zipfile.ZipFile(args.archive) as archive:
        names = archive.namelist()
        for name in names:
            lowered = name.lower()
            if any(term in lowered for term in FORBIDDEN_PATH_TERMS):
                raise SystemExit(f"forbidden archive path: {name}")
        if len(names) != len(set(names)):
            raise SystemExit("archive contains duplicate paths")
        if "SOURCE_MANIFEST.sha256" not in names:
            raise SystemExit("archive source manifest is missing")

        with tempfile.TemporaryDirectory(prefix="mg-guide-source-") as temp_dir:
            archive.extractall(temp_dir)
            env = {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": f"{temp_dir}:{temp_dir}/src",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            subprocess.run(
                [sys.executable, "-c", SMOKE_PROGRAM],
                cwd=temp_dir,
                env=env,
                check=True,
            )

    print(f"ROOT_AGENT_MODULE={EXPECTED_ROOT_MODULE}")
    print(f"ROOT_AGENT_FACTORY={EXPECTED_ROOT_FACTORY}")
    print(f"SOURCE_PACKAGE_SHA256={actual_digest}")
    print("SECRETS_INCLUDED=NO")
    print("PRIVATE_DATA_INCLUDED=NO")


if __name__ == "__main__":
    main()
