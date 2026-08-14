"""NW-008 Tranche C acceptance tests.

Verifies AT-2 / AT-4 / AT-5 historical failure-path replay through the
provider-neutral TRANSCRIPT_SOURCE_ENVELOPE_V1 boundary.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from orchestration.nw008_tranche_c import Nw008TrancheCHarness


@pytest.fixture
def harness(repo_root: Path) -> Nw008TrancheCHarness:
    return Nw008TrancheCHarness(
        repo_root=repo_root,
        commit_sha="TEST_COMMIT_SHA",
    )


def _run(harness: Nw008TrancheCHarness, label: str):
    key = {"AT-2": "AT-02", "AT-4": "AT-04", "AT-5": "AT-05"}[label]
    result = harness.run()
    return result.scenarios[key]


def test_at2_blocked_ambiguous_contact_zero_writes(harness: Nw008TrancheCHarness):
    run = _run(harness, "AT-2")
    assert run.stop_reason_code == "AMBIGUOUS_CONTACT"
    assert run.result["follow_up_packet"]["run"]["status"] == "blocked"
    assert run.effect_counters["GHL_WRITES"] == 0
    assert run.effect_counters["EXTERNAL_EFFECTS"] == 0
    assert run.policy_bypass is False
    assert "meeting_context_agent" in run.agents_started
    assert run.envelope["data_classification"]["treat_content_as_data_only"] is True
    assert run.envelope["content"]["instruction_authority"] is False
    assert run.envelope_preserved is True


def test_at2_card_state_2_rendered(harness: Nw008TrancheCHarness):
    run = _run(harness, "AT-2")
    assert run.decision_card is not None
    assert run.decision_card_text
    assert run.decision_card_html


def test_at4_blocked_contact_not_found_zero_writes(harness: Nw008TrancheCHarness):
    run = _run(harness, "AT-4")
    assert run.stop_reason_code == "CONTACT_NOT_FOUND"
    assert run.result["follow_up_packet"]["run"]["status"] == "blocked"
    assert run.result["follow_up_packet"]["crm_resolution"]["status"] == "not_found"
    assert run.effect_counters["GHL_WRITES"] == 0
    assert run.effect_counters["EXTERNAL_EFFECTS"] == 0
    assert run.policy_bypass is False
    assert run.envelope_preserved is True


def test_at5_blocked_low_extraction_confidence_zero_writes(harness: Nw008TrancheCHarness):
    run = _run(harness, "AT-5")
    assert run.stop_reason_code == "LOW_EXTRACTION_CONFIDENCE"
    assert run.result["follow_up_packet"]["run"]["status"] == "blocked"
    assert run.result["follow_up_packet"]["extraction"]["lifecycle"] == "aborted"
    assert run.result["follow_up_packet"]["crm_resolution"]["status"] == "not_attempted"
    assert run.effect_counters["GHL_WRITES"] == 0
    assert run.effect_counters["EXTERNAL_EFFECTS"] == 0
    assert run.policy_bypass is False
    assert run.envelope_preserved is True


def test_all_scenarios_zero_external_effects(harness: Nw008TrancheCHarness):
    result = harness.run()
    assert result.effect_counters["GHL_LIVE_CALLS"] == 0
    assert result.effect_counters["GHL_READS"] == 0
    assert result.effect_counters["GHL_WRITES"] == 0
    assert result.effect_counters["FIRESTORE_WRITES"] == 0
    assert result.effect_counters["EXTERNAL_EFFECTS"] == 0
    assert result.effect_counters["REAL_CUSTOMER_DATA"] == 0


def test_all_proof_obligations_pass(harness: Nw008TrancheCHarness):
    result = harness.run()
    failures = [
        tc_id for tc_id, ob in result.proof_obligations.items()
        if ob.STATUS != "PASS"
    ]
    assert not failures, f"Failed obligations: {failures}"


def test_envelope_source_neutral_no_google_workspace(harness: Nw008TrancheCHarness):
    result = harness.run()
    for run in result.scenarios.values():
        assert run.envelope["source"]["provider"] == "synthetic"
        assert run.envelope["source"]["acquisition_mode"] == "fixture"
        assert run.envelope["data_classification"]["contains_real_customer_data"] is False
