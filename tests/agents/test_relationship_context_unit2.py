"""Tests for Phase 3 Unit 2: ADK runtime + Relationship Context Agent."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents.adk_runtime import (
    ADK_STATUS_RUNTIME_INTEGRATED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    GoogleAdkPackageUnavailable,
    GoogleAdkRuntime,
    adk_runtime_declaration,
)
from agents.meeting_context import MeetingContextAgent, MeetingContextFixtureHarness
from agents.meeting_context.providers.gemini_adk_provider import (
    ADK_INTEGRATION_STATUS as UNIT1_ADK_STATUS,
)
from agents.meeting_context.providers.gemini_adk_provider import (
    GOOGLE_ADK_RUNTIME_STARTED as UNIT1_ADK_RUNTIME,
)
from agents.relationship_context import (
    RelationshipContextAgent,
    RelationshipRequest,
    run_unit2_harness,
)
from agents.relationship_context.crm_store import SyntheticCrmStore
from agents.relationship_context.harness import (
    DEFAULT_SCENARIOS,
    Unit2RelationshipHarness,
)
from agents.relationship_context.schema import validate_relationship_context
from integrations.ghl import OperationNotAllowedError


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "fixtures"
CONTRACTS = REPO_ROOT / "contracts"
CRM_FIXTURE = FIXTURES / "ghl" / "relationship-context-crm.json"


def test_relationship_context_schema_file_exists():
    path = CONTRACTS / "relationship_context.schema.json"
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["title"] == "relationship_context_v1"


def test_unit2_adk_runtime_markers_distinct_from_unit1_provider_surface():
    """Unit 1 provider remains surface-only; Unit 2 runtime is integrated."""
    assert UNIT1_ADK_RUNTIME is False
    assert UNIT1_ADK_STATUS == "COMPATIBLE_SURFACE_ONLY"
    runtime = GoogleAdkRuntime()
    runtime.start()
    markers = runtime.telemetry()
    assert markers["google_adk_runtime_started"] is True
    assert markers["adk_integration_status"] == "RUNTIME_INTEGRATED"
    assert markers["external_effects"] == 0
    assert markers["ghl_live_calls"] == 0
    assert markers["ghl_writes"] == 0
    decl = adk_runtime_declaration(runtime)
    assert decl["google_adk_runtime_started"] is True
    assert decl["integration_status"] == "RUNTIME_INTEGRATED"
    assert decl["stop_before"] == "follow_up_planning_agent"
    assert "follow_up_planning_agent" not in decl["agents"]
    assert "relationship_context_agent" in decl["agents"]
    assert "meeting_context_agent" in decl["agents"]


def test_adk_runtime_starts_and_reports_backend():
    runtime = GoogleAdkRuntime()
    assert runtime.started is False
    runtime.start()
    assert runtime.started is True
    tel = runtime.telemetry()
    assert tel["runtime_started"] is True
    assert tel["google_adk_package_bound"] is True
    assert tel["runtime_backend"] == RUNTIME_BACKEND_GOOGLE_ADK
    assert tel["local_adk_fallback_used"] is False
    assert tel["stop_before"] == "follow_up_planning_agent"
    assert tel["ghl_live_calls"] == 0
    assert tel["deployment"] is False


def test_runtime_truth_markers_derived_and_consistent():
    """Proof truth must equal actual Google ADK execution truth.

    Fails if GOOGLE_ADK_RUNTIME_STARTED=YES while the google-adk package is
    not bound, or if ADK_INTEGRATION_STATUS=RUNTIME_INTEGRATED while the
    runtime backend is not the google_adk_package.
    """
    harness = Unit2RelationshipHarness()
    result = harness.run_scenario("RELATIONSHIP_MATCH")
    assert result.ok, result.errors

    runtime = GoogleAdkRuntime()
    runtime.start()
    req = harness._load_meeting_request("transcript-success")
    run = runtime.run_unit2(meeting_request=req, scenario_id="RELATIONSHIP_MATCH")
    tel = runtime.telemetry()

    if tel["google_adk_runtime_started"] is True:
        assert tel["google_adk_package_bound"] is True
    if tel["adk_integration_status"] == ADK_STATUS_RUNTIME_INTEGRATED:
        assert tel["runtime_backend"] == RUNTIME_BACKEND_GOOGLE_ADK
    if run.google_adk_runtime_started:
        assert run.google_adk_package_bound is True
    if run.adk_integration_status == ADK_STATUS_RUNTIME_INTEGRATED:
        assert run.session.backend == RUNTIME_BACKEND_GOOGLE_ADK

    # Expected positive truth for this PR: package-bound ADK execution.
    assert run.ok, run.errors
    assert run.google_adk_package_bound is True
    assert run.google_adk_runtime_started is True
    assert run.adk_integration_status == ADK_STATUS_RUNTIME_INTEGRATED
    assert run.session.backend == RUNTIME_BACKEND_GOOGLE_ADK
    assert run.adk_runtime_primitive_used is True
    assert run.local_adk_fallback_used is False


def test_runtime_fails_closed_without_google_adk_package(monkeypatch):
    """No local fallback: missing google-adk package => runtime never starts."""
    import agents.adk_runtime.runtime as runtime_mod

    def _raise():
        raise GoogleAdkPackageUnavailable("simulated missing package")

    monkeypatch.setattr(runtime_mod, "_import_google_adk_primitives", _raise)
    runtime = GoogleAdkRuntime()
    with pytest.raises(GoogleAdkPackageUnavailable):
        runtime.start()
    assert runtime.started is False
    assert runtime.google_adk_package_bound is False
    assert runtime.backend != RUNTIME_BACKEND_GOOGLE_ADK
    tel = runtime.telemetry()
    assert tel["google_adk_runtime_started"] is False
    assert tel["adk_integration_status"] == "NOT_STARTED"
    assert tel["local_adk_fallback_used"] is False


@pytest.mark.parametrize(
    "scenario_id,expected_status",
    [
        ("RELATIONSHIP_MATCH", "matched"),
        ("AMBIGUOUS_CONTACT", "ambiguous"),
        ("NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT", "opportunity_missing"),
        ("AMBIGUOUS_OPPORTUNITY", "opportunity_ambiguous"),
    ],
)
def test_unit2_scenarios(scenario_id, expected_status):
    harness = Unit2RelationshipHarness()
    result = harness.run_scenario(scenario_id)
    assert result.ok, result.errors
    assert result.actual_status == expected_status
    assert result.external_effects == 0
    assert result.deterministic_policy_bypass is False
    assert result.offline_ghl_adapter_used is True
    assert result.google_adk_package_bound is True
    assert result.adk_runtime_primitive_used is True
    assert result.local_adk_fallback_used is False
    assert result.runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK
    assert result.relationship_context is not None
    ok, errors = validate_relationship_context(result.relationship_context)
    assert ok, errors
    crm = result.relationship_context["crm_source"]
    assert crm["mode"] == "offline_synthetic"
    assert crm["adapter"] == "phase2b_offline_ghl_read_adapter"
    assert crm["live_calls"] == 0
    assert crm["writes"] == 0
    assert crm["real_customer_data"] == 0
    assert crm["operations_used"]
    assert result.relationship_context["policy_authority"][
        "deterministic_policy_bypass"
    ] is False


def test_full_unit2_harness():
    report = run_unit2_harness()
    assert report.ok, report.to_dict()
    assert report.google_adk_package_bound is True
    assert report.google_adk_runtime_started is True
    assert report.adk_integration_status == "RUNTIME_INTEGRATED"
    assert report.adk_runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK
    assert report.adk_runtime_primitive_used is True
    assert report.local_adk_fallback_used is False
    assert report.meeting_context_agent_reused is True
    assert report.relationship_context_agent_implemented is True
    assert report.offline_ghl_adapter_used is True
    assert report.synthetic_crm_context_only is True
    assert report.relationship_context_output_valid is True
    assert report.deterministic_policy_bypass is False
    assert report.external_effects == 0
    assert report.scenario_results == {
        "RELATIONSHIP_MATCH": "PASS",
        "AMBIGUOUS_CONTACT": "PASS",
        "NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT": "PASS",
        "AMBIGUOUS_OPPORTUNITY": "PASS",
    }
    assert len(report.cases) == 4
    markers = report.proof_markers()
    assert markers["GOOGLE_ADK_PACKAGE_BOUND"] == "YES"
    assert markers["GOOGLE_ADK_RUNTIME_STARTED"] == "YES"
    assert markers["ADK_INTEGRATION_STATUS"] == "RUNTIME_INTEGRATED"
    assert markers["ADK_RUNTIME_BACKEND"] == "google_adk_package"
    assert markers["ADK_RUNTIME_PRIMITIVE_USED"] == "YES"
    assert markers["LOCAL_ADK_FALLBACK_USED"] == "NO"
    assert markers["DETERMINISTIC_POLICY_BYPASS"] == "NO"
    assert markers["EXTERNAL_EFFECTS"] == 0
    assert markers["GHL_LIVE_CALLS"] == 0
    assert markers["GHL_WRITES"] == 0


def test_relationship_match_has_contact_and_opportunity():
    result = Unit2RelationshipHarness().run_scenario("RELATIONSHIP_MATCH")
    assert result.ok, result.errors
    res = result.relationship_context["resolution"]
    assert res["contact_id"] == "contact_demo_taylor_001"
    assert res["opportunity_id"] == "opp_demo_taylor_001"
    assert res["match_basis"] == "email"
    assert res["contact"]["email"] == "taylor.morgan@example-demo.test"
    assert res["opportunity"]["id"] == "opp_demo_taylor_001"
    assert res["current_stage"] == "discovery_scheduled"


def test_ambiguous_contact_fail_closed():
    result = Unit2RelationshipHarness().run_scenario("AMBIGUOUS_CONTACT")
    assert result.ok, result.errors
    res = result.relationship_context["resolution"]
    assert res["status"] == "ambiguous"
    assert res["contact_id"] is None
    assert res["opportunity_id"] is None
    assert res["candidate_count"] == 2
    assert len(res["candidates"]) == 2


def test_no_opportunity_unique_contact():
    result = Unit2RelationshipHarness().run_scenario(
        "NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT"
    )
    assert result.ok, result.errors
    res = result.relationship_context["resolution"]
    assert res["status"] == "opportunity_missing"
    assert res["contact_id"] == "contact_demo_casey_001"
    assert res["opportunity_id"] is None
    assert res["contact"] is not None
    assert res["opportunity"] is None


def test_ambiguous_opportunity_fail_closed():
    """Unique contact + multiple eligible open opportunities => select none."""
    result = Unit2RelationshipHarness().run_scenario("AMBIGUOUS_OPPORTUNITY")
    assert result.ok, result.errors
    res = result.relationship_context["resolution"]
    assert res["status"] == "opportunity_ambiguous"
    assert res["contact_id"] == "contact_demo_morgan_multi_001"
    assert res["opportunity_id"] is None
    assert res["current_stage"] is None
    assert res["candidate_count"] == 1
    assert res["contact"] is not None
    assert res["opportunity"] is None
    assert "review" in result.relationship_context["evidence"]["notes"].lower()
    assert result.external_effects == 0
    crm = result.relationship_context["crm_source"]
    assert crm["live_calls"] == 0
    assert crm["writes"] == 0


def test_ambiguous_opportunity_overlay_maps_to_ambiguous():
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    harness = Unit2RelationshipHarness()
    mc_result = harness._meeting_agent().run(
        harness._load_meeting_request("transcript-ambiguous-opportunity")
    )
    agent = RelationshipContextAgent(store=store)
    rel = agent.run(
        RelationshipRequest(
            meeting_context=mc_result.to_dict(), run_id="overlay_ambopp"
        )
    )
    overlay = rel.to_crm_resolution_overlay()
    assert overlay["status"] == "ambiguous"
    assert overlay["contact_id"] == "contact_demo_morgan_multi_001"
    assert overlay["opportunity_id"] is None
    assert overlay["current_stage"] is None


def test_crm_resolution_overlay_packet_compatible():
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    # Build meeting context via unit1 agent.
    mc = MeetingContextFixtureHarness(provider_mode="fixture").run_case(
        "transcript-success"
    )
    assert mc.ok
    agent = RelationshipContextAgent(store=store)
    rel = agent.run(
        RelationshipRequest(meeting_context=mc.context, run_id="overlay_test")
    )
    overlay = rel.to_crm_resolution_overlay()
    assert overlay["lifecycle"] == "complete"
    assert overlay["status"] == "matched"
    assert overlay["contact_id"] == "contact_demo_taylor_001"
    assert overlay["opportunity_id"] == "opp_demo_taylor_001"
    assert overlay["match_basis"] == "email"
    assert overlay["candidate_count"] == 1


def test_offline_store_denies_mutations():
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    with pytest.raises(OperationNotAllowedError):
        store.adapter.build_request("create-note")
    with pytest.raises(OperationNotAllowedError):
        store.adapter.build_request("update-opportunity")


def test_unit1_meeting_context_harness_no_regression():
    """Unit 1 harness remains green after Unit 2 additions."""
    report = MeetingContextFixtureHarness(provider_mode="fixture").run()
    assert report.ok
    assert report.google_adk_runtime_started is False
    assert report.adk_integration_status == "COMPATIBLE_SURFACE_ONLY"
    stub = MeetingContextFixtureHarness(provider_mode="gemini_adk_stub").run()
    assert stub.ok


def test_runtime_does_not_invoke_follow_up_planning_agent():
    harness = Unit2RelationshipHarness()
    result = harness.run_scenario("RELATIONSHIP_MATCH")
    assert result.ok
    # Reconstruct a run to inspect session stop gate.
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    runtime = GoogleAdkRuntime(
        meeting_agent=MeetingContextAgent.for_fixture_mode(),
        relationship_agent=RelationshipContextAgent(store=store),
    )
    # Use harness internals for request.
    req = harness._load_meeting_request("transcript-success")
    run = runtime.run_unit2(meeting_request=req, scenario_id="RELATIONSHIP_MATCH")
    assert run.session.get("follow_up_planning_agent_invoked") is False
    assert run.session.get("stop_before") == "follow_up_planning_agent"
    agent_ids = [t.agent_id for t in run.session.agent_trace]
    assert agent_ids == ["meeting_context_agent", "relationship_context_agent"]


def test_insufficient_context_path():
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    agent = RelationshipContextAgent(store=store)
    meeting_context = {
        "schema": "meeting_context_v1",
        "agent": "meeting_context_agent",
        "provider": "fixture",
        "meeting": {
            "meeting_id": "demo_insufficient",
            "occurred_at": "2026-08-10T15:00:00Z",
            "source": "synthetic_demo",
            "transcript_hash": "a" * 64,
        },
        "participants": [
            {"name": None, "email": None, "phone": None, "role": "prospect"},
            {
                "name": "Alex Rivera",
                "email": "alex.rivera@example-demo.test",
                "phone": "+1-555-0199",
                "role": "agent",
            },
        ],
        "extraction": {
            "lifecycle": "complete",
            "summary": "n/a",
            "needs": [],
            "objections": [],
            "commitments": [],
            "next_step": None,
            "opportunity_signal": None,
        },
        "evidence": {"transcript_spans": [], "extraction_confidence": 0.5},
        "external_effects": 0,
        "policy_authority": {
            "deterministic_policy_bypass": False,
            "notes": "test",
        },
    }
    rel = agent.run(RelationshipRequest(meeting_context=meeting_context))
    assert rel.resolution["status"] == "insufficient_context"
    ok, errors = validate_relationship_context(rel.to_dict())
    assert ok, errors


def test_default_scenarios_cover_required_proof_keys():
    assert set(DEFAULT_SCENARIOS) == {
        "RELATIONSHIP_MATCH",
        "AMBIGUOUS_CONTACT",
        "NO_OPPORTUNITY_OR_INSUFFICIENT_CONTEXT",
        "AMBIGUOUS_OPPORTUNITY",
    }
