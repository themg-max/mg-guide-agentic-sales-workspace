"""Tests for Meeting Context Agent fixture harness (Phase 3 unit 1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents.meeting_context import MeetingContextAgent, MeetingContextFixtureHarness
from agents.meeting_context.harness import run_fixture_harness
from agents.meeting_context.providers.base import ProviderRequest
from agents.meeting_context.providers.gemini_adk_provider import (
    ADK_INTEGRATION_STATUS,
    GEMINI_ADK_STARTED,
    GEMINI_PROVIDER_STARTED,
    GOOGLE_ADK_RUNTIME_STARTED,
    GeminiAdkConfig,
    GeminiAdkContextProvider,
    adk_agent_declaration,
    _call_gemini_generate,
)
from agents.meeting_context.schema import validate_meeting_context
from orchestration.policy import evaluate_policy
from orchestration.state_machine import StateMachine


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "fixtures"
CONTRACTS = REPO_ROOT / "contracts"


def test_meeting_context_schema_file_exists():
    path = CONTRACTS / "meeting_context.schema.json"
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["title"] == "meeting_context_v1"


def test_gemini_provider_and_adk_runtime_markers():
    assert GEMINI_PROVIDER_STARTED is True
    assert GOOGLE_ADK_RUNTIME_STARTED is False
    assert ADK_INTEGRATION_STATUS == "COMPATIBLE_SURFACE_ONLY"
    # Compatibility umbrella only — not ADK runtime execution.
    assert GEMINI_ADK_STARTED is True
    decl = adk_agent_declaration()
    assert decl["gemini_provider_started"] is True
    assert decl["google_adk_runtime_started"] is False
    assert decl["adk_integration_status"] == "COMPATIBLE_SURFACE_ONLY"
    assert decl["gemini_adk_started"] is True
    assert decl["deterministic_policy_bypass"] is False
    assert decl["crm_access"] == "none"
    assert decl["tools"] == []


@pytest.mark.parametrize(
    "fixture_id",
    [
        "transcript-success",
        "transcript-ambiguous-contact",
        "transcript-no-stage-change",
    ],
)
def test_fixture_provider_produces_valid_context(fixture_id):
    harness = MeetingContextFixtureHarness(provider_mode="fixture")
    result = harness.run_case(fixture_id)
    assert result.ok, result.errors
    assert result.external_effects == 0
    assert result.deterministic_policy_bypass is False
    assert result.context is not None
    ok, errors = validate_meeting_context(result.context)
    assert ok, errors
    assert result.context["schema"] == "meeting_context_v1"
    assert result.context["agent"] == "meeting_context_agent"
    assert result.context["provider"] == "fixture"
    assert result.context["extraction"]["lifecycle"] == "complete"
    assert result.context["meeting"]["meeting_id"]


def test_gemini_adk_stub_provider_harness():
    report = run_fixture_harness(provider_mode="gemini_adk_stub")
    assert report.ok, report.to_dict()
    assert report.gemini_provider_started is True
    assert report.google_adk_runtime_started is False
    assert report.adk_integration_status == "COMPATIBLE_SURFACE_ONLY"
    assert report.gemini_adk_started is True
    assert report.meeting_context_agent_implemented is True
    assert report.synthetic_transcript_input is True
    assert report.structured_context_output_valid is True
    assert report.deterministic_policy_bypass is False
    assert report.external_effects == 0
    providers = {c.provider for c in report.cases}
    assert providers == {"gemini_adk_stub"}


def test_full_fixture_harness_fixture_mode():
    report = run_fixture_harness(provider_mode="fixture")
    assert report.ok
    assert len(report.cases) == 3
    assert all(c.ok for c in report.cases)


def test_agent_rejects_empty_transcript():
    agent = MeetingContextAgent.for_fixture_mode()
    sidecar = json.loads(
        (FIXTURES / "transcript-success.expected.json").read_text(encoding="utf-8")
    )
    request = ProviderRequest(
        fixture_id="transcript-success",
        transcript_text="   ",
        transcript_path=None,
        meeting=sidecar["meeting"],
        participants=sidecar["participants"],
        extraction_result=sidecar["extraction_result"],
        extraction_confidence=sidecar["extraction_confidence"],
        evidence_references=sidecar["evidence_references"],
    )
    with pytest.raises(ValueError, match="transcript_text"):
        agent.run(request)


def test_context_does_not_bypass_deterministic_policy():
    """Meeting context is proposal-only; policy still decides stage/note writes."""
    harness = MeetingContextFixtureHarness(provider_mode="fixture")
    case = harness.run_case("transcript-no-stage-change")
    assert case.ok
    ctx = case.context
    assert ctx is not None
    assert ctx["policy_authority"]["deterministic_policy_bypass"] is False

    sidecar = json.loads(
        (FIXTURES / "transcript-no-stage-change.expected.json").read_text(
            encoding="utf-8"
        )
    )
    sm = StateMachine.from_yaml(CONTRACTS / "workflow_states.yaml")
    decision = evaluate_policy(
        sm,
        extraction_confidence=float(ctx["evidence"]["extraction_confidence"]),
        crm=sidecar["crm_resolution_stub"],
        policy_inputs=sidecar["policy_inputs"],
        extraction_result=ctx["extraction"],
    )
    # Fixture expects stage denial path to remain enforceable.
    assert "STAGE_TRANSITION_NOT_ALLOWED" in decision.reason_codes or decision.stage_write in {
        "blocked",
        "approval_required",
    }


def test_context_overlay_compatible_with_packet_extraction_shape():
    harness = MeetingContextFixtureHarness(provider_mode="fixture")
    result = harness.run_case("transcript-success")
    extraction = result.context["extraction"]
    required = {
        "lifecycle",
        "summary",
        "needs",
        "objections",
        "commitments",
        "next_step",
        "opportunity_signal",
    }
    assert required.issubset(extraction.keys())
    assert extraction["lifecycle"] == "complete"


def test_agent_telemetry_surface():
    agent = MeetingContextAgent.for_gemini_adk(mode="stub")
    tel = agent.telemetry()
    assert tel["gemini_provider_started"] is True
    assert tel["google_adk_runtime_started"] is False
    assert tel["adk_integration_status"] == "COMPATIBLE_SURFACE_ONLY"
    assert tel["gemini_adk_started"] is True
    assert tel["external_effects"] == 0
    assert tel["deterministic_policy_bypass"] is False


def test_live_gemini_provider_path_mocked_no_network(monkeypatch):
    """Network-free mocked live path: no credentials, no CRM, no real egress."""
    sidecar = json.loads(
        (FIXTURES / "transcript-success.expected.json").read_text(encoding="utf-8")
    )
    transcript = (FIXTURES / "transcript-success.txt").read_text(encoding="utf-8")

    mocked_payload = {
        "summary": sidecar["extraction_result"]["summary"],
        "needs": sidecar["extraction_result"]["needs"],
        "objections": sidecar["extraction_result"]["objections"],
        "commitments": sidecar["extraction_result"]["commitments"],
        "next_step": sidecar["extraction_result"]["next_step"],
        "opportunity_signal": sidecar["extraction_result"]["opportunity_signal"],
        "extraction_confidence": sidecar["extraction_confidence"],
        "evidence_references": sidecar["evidence_references"],
        "meeting": sidecar["meeting"],
        "participants": sidecar["participants"],
    }

    def _fake_generate(*, model, credential, prompt, **_kwargs):
        assert model
        assert credential == "test-not-a-real-secret"
        assert "TRANSCRIPT" in prompt
        # Return JSON text only — no network.
        return json.dumps(mocked_payload)

    monkeypatch.setenv("GEMINI_API_KEY", "test-not-a-real-secret")
    monkeypatch.setattr(
        "agents.meeting_context.providers.gemini_adk_provider._call_gemini_generate",
        _fake_generate,
    )

    provider = GeminiAdkContextProvider(GeminiAdkConfig(mode="live"))
    request = ProviderRequest(
        fixture_id="transcript-success",
        transcript_text=transcript,
        transcript_path=str(FIXTURES / "transcript-success.txt"),
        meeting=sidecar["meeting"],
        participants=sidecar["participants"],
    )
    result = provider.extract(request)
    payload = result.to_dict()
    ok, errors = validate_meeting_context(payload)
    assert ok, errors
    assert payload["provider"] == "gemini_adk"
    assert payload["external_effects"] == 0
    assert payload["policy_authority"]["deterministic_policy_bypass"] is False
    assert GOOGLE_ADK_RUNTIME_STARTED is False
    # Ensure helper remains importable for patch target stability.
    assert callable(_call_gemini_generate)
