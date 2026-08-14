"""Tests for Phase 3 Unit 3: Follow-Up Planning Agent + policy gate + packet."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agents.adk_runtime import (
    ADK_STATUS_RUNTIME_INTEGRATED,
    RUNTIME_BACKEND_GOOGLE_ADK,
    GoogleAdkPackageUnavailable,
)
from agents.follow_up_planning import (
    FollowUpPlanningAgent,
    FollowUpPlanningRequest,
    Unit3FollowUpHarness,
    Unit3FollowUpRuntime,
    run_unit3_harness,
)
from agents.follow_up_planning.harness import DEFAULT_SCENARIOS
from agents.follow_up_planning.packet import (
    FollowUpPacketAssembler,
    validate_follow_up_packet,
)
from agents.follow_up_planning.schema import validate_follow_up_proposal
from agents.meeting_context import MeetingContextAgent
from agents.relationship_context import RelationshipContextAgent, RelationshipRequest
from agents.relationship_context.crm_store import SyntheticCrmStore

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "fixtures"
CONTRACTS = REPO_ROOT / "contracts"
CRM_FIXTURE = FIXTURES / "ghl" / "relationship-context-crm.json"


def _contexts(transcript_fixture: str):
    """Produce Unit 1 + Unit 2 artifacts for a transcript fixture."""
    harness = Unit3FollowUpHarness()
    request = harness._load_meeting_request(transcript_fixture)
    mc = MeetingContextAgent.for_fixture_mode().run(request).to_dict()
    store = SyntheticCrmStore.from_fixture_path(CRM_FIXTURE)
    rel = (
        RelationshipContextAgent(store=store)
        .run(RelationshipRequest(meeting_context=mc, run_id="unit3_direct"))
        .to_dict()
    )
    return mc, rel


def test_follow_up_proposal_schema_file_exists():
    path = CONTRACTS / "follow_up_proposal.schema.json"
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["title"] == "follow_up_proposal_v1"


def test_unit3_runtime_graph_extends_unit2():
    from agents.adk_runtime.runtime import UNIT2_AGENT_GRAPH
    from agents.follow_up_planning.runtime import UNIT3_AGENT_GRAPH

    unit2_ids = [a.agent_id for a in UNIT2_AGENT_GRAPH]
    unit3_ids = [a.agent_id for a in UNIT3_AGENT_GRAPH]
    assert unit3_ids[:2] == unit2_ids
    assert unit3_ids[-1] == "follow_up_planning_agent"


def test_unit3_runtime_starts_on_google_adk_package():
    runtime = Unit3FollowUpRuntime()
    assert runtime.started is False
    runtime.start()
    assert runtime.started is True
    tel = runtime.telemetry()
    assert tel["google_adk_package_bound"] is True
    assert tel["runtime_backend"] == RUNTIME_BACKEND_GOOGLE_ADK
    assert tel["local_adk_fallback_used"] is False
    assert tel["ghl_live_calls"] == 0
    assert tel["ghl_writes"] == 0
    assert tel["external_effects"] == 0
    assert [a["agent_id"] for a in tel["agent_graph"]] == [
        "meeting_context_agent",
        "relationship_context_agent",
        "follow_up_planning_agent",
    ]


def test_unit3_runtime_fails_closed_without_google_adk_package(monkeypatch):
    """No local fallback: missing google-adk package => runtime never starts."""
    import agents.follow_up_planning.runtime as runtime_mod

    def _raise():
        raise GoogleAdkPackageUnavailable("simulated missing package")

    monkeypatch.setattr(runtime_mod, "_import_google_adk_primitives", _raise)
    runtime = Unit3FollowUpRuntime()
    with pytest.raises(GoogleAdkPackageUnavailable):
        runtime.start()
    assert runtime.started is False
    assert runtime.google_adk_package_bound is False
    tel = runtime.telemetry()
    assert tel["google_adk_runtime_started"] is False
    assert tel["adk_integration_status"] == "NOT_STARTED"
    assert tel["local_adk_fallback_used"] is False


def test_runtime_truth_markers_derived_and_consistent():
    """Proof truth must equal actual Google ADK execution truth."""
    harness = Unit3FollowUpHarness()
    result = harness.run_scenario("SUCCESS")
    assert result.ok, result.errors

    runtime = Unit3FollowUpRuntime()
    runtime.start()
    req = harness._load_meeting_request("transcript-success")
    run = runtime.run_unit3(meeting_request=req, scenario_id="SUCCESS")
    tel = runtime.telemetry()

    if tel["google_adk_runtime_started"] is True:
        assert tel["google_adk_package_bound"] is True
    if tel["adk_integration_status"] == ADK_STATUS_RUNTIME_INTEGRATED:
        assert tel["runtime_backend"] == RUNTIME_BACKEND_GOOGLE_ADK
    if run.google_adk_runtime_started:
        assert run.google_adk_package_bound is True
    if run.adk_integration_status == ADK_STATUS_RUNTIME_INTEGRATED:
        assert run.session.backend == RUNTIME_BACKEND_GOOGLE_ADK

    assert run.ok, run.errors
    assert run.google_adk_package_bound is True
    assert run.google_adk_runtime_started is True
    assert run.adk_integration_status == ADK_STATUS_RUNTIME_INTEGRATED
    assert run.session.backend == RUNTIME_BACKEND_GOOGLE_ADK
    assert run.adk_runtime_primitive_used is True
    assert run.local_adk_fallback_used is False


@pytest.mark.parametrize("scenario_id", list(DEFAULT_SCENARIOS.keys()))
def test_unit3_scenarios(scenario_id):
    meta = DEFAULT_SCENARIOS[scenario_id]
    harness = Unit3FollowUpHarness()
    result = harness.run_scenario(scenario_id)
    assert result.ok, result.errors
    assert result.actual_packet_status == meta["expected_packet_status"]
    assert result.external_effects == 0
    assert result.deterministic_policy_bypass is False
    assert result.google_adk_package_bound is True
    assert result.adk_runtime_primitive_used is True
    assert result.local_adk_fallback_used is False
    assert result.runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK

    expected_stop = meta.get("expected_governed_stop")
    if expected_stop is None or expected_stop["boundary_agent_id"] != (
        "meeting_context_agent"
    ):
        assert result.relationship_context_reused is True
    if expected_stop is not None:
        assert result.governed_stop is not None
        assert (
            result.governed_stop["boundary_agent_id"]
            == expected_stop["boundary_agent_id"]
        )
        assert result.governed_stop["reason_code"] == expected_stop["reason_code"]
        assert result.follow_up_proposal is None
        assert result.follow_up_packet is None
        assert result.policy_gate_invoked is False
        return

    proposal = result.follow_up_proposal
    packet = result.follow_up_packet
    assert proposal is not None and packet is not None
    ok, errors = validate_follow_up_proposal(proposal)
    assert ok, errors
    assert validate_follow_up_packet(packet) == []
    assert proposal["external_effects"] == 0
    assert packet["external_effects"] == 0
    assert proposal["policy_authority"]["deterministic_policy_bypass"] is False
    assert proposal["policy_evaluation"]["deterministic_policy_bypass"] is False

    intents = packet["mutation_intents"]
    assert len(intents["note"]) == meta["expected_note_intents"]
    assert len(intents["stage"]) == meta["expected_stage_intents"]
    for code in meta["expected_reason_codes"]:
        assert code in packet["policy"]["reason_codes"]
    # No mutation is ever attempted in Unit 3 (intent-only, zero effects).
    assert packet["mutations"]["note"]["attempted"] is False
    assert packet["mutations"]["opportunity_stage"]["attempted"] is False
    assert packet["mutations"]["opportunity_stage"]["verified"] is False


def test_success_scenario_full_authorization_path():
    result = Unit3FollowUpHarness().run_scenario("SUCCESS")
    assert result.ok, result.errors
    packet = result.follow_up_packet
    proposal = result.follow_up_proposal
    assert packet["run"]["status"] == "completed"
    assert packet["policy"]["note_write"] == "allowed"
    assert packet["policy"]["stage_write"] == "allowed"
    assert packet["crm_resolution"]["status"] == "matched"
    assert packet["crm_resolution"]["contact_id"] == "contact_demo_taylor_001"
    assert packet["crm_resolution"]["opportunity_id"] == "opp_demo_taylor_001"
    assert packet["mutations"]["lifecycle"] == "intent_only"
    assert packet["mutations"]["opportunity_stage"]["from_stage"] == (
        "discovery_scheduled"
    )
    assert packet["mutations"]["opportunity_stage"]["to_stage"] == (
        "discovery_complete"
    )
    stage_intents = packet["mutation_intents"]["stage"]
    assert len(stage_intents) == 1
    assert stage_intents[0]["status"] == "planned"
    assert result.policy_gate_invoked is True
    assert proposal["disposition"] == "proposed"
    assert proposal["policy_evaluation"]["invoked"] is True


def test_stage_change_denied_by_policy_gate():
    """Agent proposes stage intent; deterministic policy denies it."""
    result = Unit3FollowUpHarness().run_scenario("STAGE_CHANGE_DENIED")
    assert result.ok, result.errors
    packet = result.follow_up_packet
    proposal = result.follow_up_proposal
    assert packet["run"]["status"] == "completed_with_review"
    assert packet["policy"]["note_write"] == "allowed"
    assert packet["policy"]["stage_write"] == "blocked"
    assert "STAGE_TRANSITION_NOT_ALLOWED" in packet["policy"]["reason_codes"]
    # Proposal may exist; stage mutation is NOT authorized.
    assert proposal["stage_proposal"]["requested"] is True
    assert proposal["stage_proposal"]["to_stage"] == "discovery_complete"
    assert proposal["authorized_mutation_intents"]["stage"] == []
    assert len(proposal["authorized_mutation_intents"]["note"]) == 1
    assert proposal["disposition"] == "proposed_with_review"
    assert result.policy_gate_invoked is True


def test_ambiguous_contact_no_mutation_authorized():
    """Ambiguous contact resolution is blocked by the authoritative workflow
    contract (resolving->blocked when=contact_ambiguous) before any proposal,
    packet, or mutation intent exists."""
    result = Unit3FollowUpHarness().run_scenario("AMBIGUOUS_CONTACT")
    assert result.ok, result.errors
    assert result.actual_packet_status == "blocked"
    stop = result.governed_stop
    assert stop is not None
    assert stop["boundary_agent_id"] == "relationship_context_agent"
    assert stop["reason_code"] == "AMBIGUOUS_CONTACT"
    # Pre-policy fail-closed: no proposal, no packet, no intents at all.
    assert result.follow_up_proposal is None
    assert result.follow_up_packet is None
    assert result.policy_gate_invoked is False
    assert result.external_effects == 0
    assert result.deterministic_policy_bypass is False


def test_ambiguous_opportunity_no_mutation_authorized():
    result = Unit3FollowUpHarness().run_scenario("AMBIGUOUS_OPPORTUNITY")
    assert result.ok, result.errors
    packet = result.follow_up_packet
    proposal = result.follow_up_proposal
    assert packet["run"]["status"] == "blocked"
    assert packet["crm_resolution"]["status"] == "ambiguous"
    assert packet["crm_resolution"]["contact_id"] == "contact_demo_morgan_multi_001"
    assert packet["crm_resolution"]["opportunity_id"] is None
    assert "AMBIGUOUS_OPPORTUNITY" in packet["policy"]["reason_codes"]
    assert packet["mutation_intents"] == {"note": [], "stage": []}
    assert proposal["disposition"] == "needs_review"
    assert proposal["stage_proposal"]["requested"] is False


def test_no_opportunity_blocks_before_policy():
    result = Unit3FollowUpHarness().run_scenario("NO_OPPORTUNITY")
    assert result.ok, result.errors
    packet = result.follow_up_packet
    assert packet["run"]["status"] == "blocked"
    assert packet["crm_resolution"]["status"] == "opportunity_missing"
    assert packet["crm_resolution"]["contact_id"] == "contact_demo_casey_001"
    assert "OPPORTUNITY_NOT_FOUND" in packet["policy"]["reason_codes"]
    assert packet["mutation_intents"] == {"note": [], "stage": []}


def test_insufficient_context_no_fabricated_crm_facts():
    """Extraction confidence below the abort threshold is blocked by the
    authoritative workflow contract (extracting->blocked) at the meeting
    context boundary: no CRM resolution, proposal, or packet can fabricate
    facts downstream."""
    result = Unit3FollowUpHarness().run_scenario("INSUFFICIENT_CONTEXT")
    assert result.ok, result.errors
    assert result.actual_packet_status == "blocked"
    stop = result.governed_stop
    assert stop is not None
    assert stop["boundary_agent_id"] == "meeting_context_agent"
    assert stop["reason_code"] == "LOW_EXTRACTION_CONFIDENCE"
    # Extraction aborted: nothing propagates downstream at all.
    assert result.follow_up_proposal is None
    assert result.follow_up_packet is None
    assert result.policy_gate_invoked is False
    assert result.external_effects == 0
    assert result.deterministic_policy_bypass is False


def test_full_unit3_harness():
    report = run_unit3_harness()
    assert report.ok, report.to_dict()
    assert report.google_adk_package_bound is True
    assert report.google_adk_runtime_started is True
    assert report.adk_integration_status == "RUNTIME_INTEGRATED"
    assert report.adk_runtime_backend == RUNTIME_BACKEND_GOOGLE_ADK
    assert report.adk_runtime_primitive_used is True
    assert report.local_adk_fallback_used is False
    assert report.follow_up_planning_agent_implemented is True
    assert report.meeting_context_reused is True
    assert report.relationship_context_reused is True
    assert report.google_adk_runtime_reused is True
    assert report.follow_up_proposal_output_valid is True
    assert report.deterministic_policy_gate_invoked is True
    assert report.deterministic_policy_bypass is False
    assert report.external_effects == 0
    assert report.scenario_results == {
        "SUCCESS": "PASS",
        "AMBIGUOUS_CONTACT": "PASS",
        "AMBIGUOUS_OPPORTUNITY": "PASS",
        "NO_OPPORTUNITY": "PASS",
        "STAGE_CHANGE_DENIED": "PASS",
        "INSUFFICIENT_CONTEXT": "PASS",
    }
    assert len(report.cases) == 6
    markers = report.proof_markers()
    assert markers["FOLLOW_UP_PLANNING_AGENT_IMPLEMENTED"] == "YES"
    assert markers["MEETING_CONTEXT_REUSED"] == "YES"
    assert markers["RELATIONSHIP_CONTEXT_REUSED"] == "YES"
    assert markers["GOOGLE_ADK_RUNTIME_REUSED"] == "YES"
    assert markers["FOLLOW_UP_PROPOSAL_OUTPUT"] == "VALID"
    assert markers["DETERMINISTIC_POLICY_GATE_INVOKED"] == "YES"
    assert markers["DETERMINISTIC_POLICY_BYPASS"] == "NO"
    assert markers["EXTERNAL_EFFECTS"] == 0
    assert markers["GHL_LIVE_CALLS"] == 0
    assert markers["GHL_WRITES"] == 0
    assert markers["REAL_CUSTOMER_DATA"] == 0
    assert markers["L3A_RUNTIME_STATUS"] == "DEFERRED_RUNTIME_NOT_PROMOTED"
    assert markers["FIRESTORE_WRITES"] == 0
    assert markers["DEPLOYMENT"] == "NO"


def test_agent_direct_invocation_rejects_bypass_fields():
    """Agent output schema rejects any deterministic_policy_bypass claim."""
    mc, rel = _contexts("transcript-success")
    agent = FollowUpPlanningAgent()
    result = agent.run(
        FollowUpPlanningRequest(
            meeting_context=mc,
            relationship_context=rel,
            run_id="unit3_direct_success",
            scenario_id="SUCCESS",
        )
    )
    assert result.policy_gate_invoked is True
    assert result.external_effects == 0
    proposal = dict(result.proposal)
    proposal["policy_authority"] = {
        "deterministic_policy_bypass": True,
        "notes": "tampered",
    }
    ok, errors = validate_follow_up_proposal(proposal)
    assert not ok
    assert any("deterministic_policy_bypass" in e for e in errors)


def test_agent_requires_meeting_context_fields():
    mc, rel = _contexts("transcript-success")
    agent = FollowUpPlanningAgent()
    with pytest.raises(ValueError):
        agent.run(
            FollowUpPlanningRequest(
                meeting_context={"meeting": {}},
                relationship_context=rel,
            )
        )
    with pytest.raises(ValueError):
        agent.run(
            FollowUpPlanningRequest(
                meeting_context={"meeting": mc["meeting"], "participants": []},
                relationship_context=rel,
            )
        )


def test_packet_assembler_uses_deterministic_state_machine():
    """Illegal transitions remain rejected in the Unit 3 assembly path."""
    assembler = FollowUpPacketAssembler()
    with pytest.raises(Exception):
        assembler.sm.validate_transition("received", "completed")


def test_unit2_harness_no_regression():
    """Unit 2 harness remains green after Unit 3 additions."""
    from agents.relationship_context import run_unit2_harness

    report = run_unit2_harness()
    assert report.ok, report.to_dict()
