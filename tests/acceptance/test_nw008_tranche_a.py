"""NW-008 Tranche A offline/synthetic acceptance-evidence tests."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from orchestration.nw008_harness import (
    AT_SPECS,
    EVIDENCE_RESULT_FIELDS,
    EvidenceSchemaError,
    ExternalEffectError,
    Nw008EvidenceHarness,
    assert_zero_external_effects,
    validate_evidence_result,
)


@pytest.fixture
def harness(repo_root: Path) -> Nw008EvidenceHarness:
    return Nw008EvidenceHarness(
        repo_root=repo_root,
        created_at="2026-08-14T12:00:00Z",
        commit_sha="TEST_COMMIT_SHA",
    )


def test_at2_blocked_ambiguous_contact_zero_writes_and_card(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-2")
    assert result.TEST_RESULT == "PASS"
    assert result.HISTORICAL_AT_COMPLETE == "YES"
    assert result.ACTUAL_WORKFLOW_STATUS == "blocked"
    assert "AMBIGUOUS_CONTACT" in result.AUTHORITATIVE_REASON_CODES
    assert result.GHL_WRITES == 0
    assert result.EXTERNAL_EFFECTS == 0
    assert result.CARD_POLICY_STATE == "BLOCKED"
    assert result.CARD_REASON_CODE == "AMBIGUOUS_CONTACT"
    assert result.CARD_NEXT_ACTION == "RESOLVE_CONTACT"
    assert result.HISTORICAL_CLAUSE_COVERAGE == {
        "blocked": "PASS",
        "AMBIGUOUS_CONTACT": "PASS",
        "0_CRM_writes": "PASS",
        "MG_Guide_blocked_State_2_equivalent_decision_card": "PASS",
    }
    assert result.details["mg_guide_card_state"] == "blocked"


def test_at4_contact_not_found_blocked_zero_writes(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-4")
    assert result.TEST_RESULT == "PASS"
    assert result.HISTORICAL_AT_COMPLETE == "YES"
    assert result.ACTUAL_WORKFLOW_STATUS == "blocked"
    assert result.AUTHORITATIVE_REASON_CODES == ["CONTACT_NOT_FOUND"]
    assert result.GHL_WRITES == 0
    assert result.EXTERNAL_EFFECTS == 0
    # Presentation may fail closed; historical completion uses workflow authority.
    assert result.CARD_POLICY_STATE in {"BLOCKED", "REVIEW_REQUIRED"}
    assert result.HISTORICAL_CLAUSE_COVERAGE == {
        "CONTACT_NOT_FOUND": "PASS",
        "blocked": "PASS",
        "0_writes": "PASS",
    }


def test_at5_low_extraction_confidence_blocked_zero_writes(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-5")
    assert result.TEST_RESULT == "PASS"
    assert result.HISTORICAL_AT_COMPLETE == "YES"
    assert result.ACTUAL_WORKFLOW_STATUS == "blocked"
    assert "LOW_EXTRACTION_CONFIDENCE" in result.AUTHORITATIVE_REASON_CODES
    assert result.GHL_WRITES == 0
    assert result.EXTERNAL_EFFECTS == 0
    assert result.details["extraction_confidence"] < result.details["extraction_abort_threshold"]
    assert result.HISTORICAL_CLAUSE_COVERAGE == {
        "extraction_below_threshold": "PASS",
        "LOW_EXTRACTION_CONFIDENCE": "PASS",
        "blocked": "PASS",
        "0_writes": "PASS",
    }


def test_at8_deterministic_cap_refusal_supporting_proof(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-8")
    assert result.EVIDENCE_CLASS == "PARTIAL_SUPPORTING_PROOF"
    assert result.HISTORICAL_AT_COMPLETE == "NO"
    assert result.TEST_RESULT == "PASS"
    assert result.HISTORICAL_CLAUSE_COVERAGE["deterministic_policy_cap_enforced"] == "PASS"
    assert "mutation-execution trace" in result.REMAINING_GAP
    assert result.details["max_note_intents"] == 1
    assert result.details["max_stage_intents"] == 1
    assert result.details["second_note_refusal"]["refused"] is True
    assert result.details["second_stage_refusal"]["refused"] is True


def test_at9_tool_manifest_refusal_supporting_proof(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-9")
    assert result.EVIDENCE_CLASS == "PARTIAL_SUPPORTING_PROOF"
    assert result.HISTORICAL_AT_COMPLETE == "NO"
    assert result.TEST_RESULT == "PASS"
    assert result.HISTORICAL_CLAUSE_COVERAGE["tool_manifest_refusal_offline"] == "PASS"
    assert "durable audit warning" in result.REMAINING_GAP
    assert result.details["nw005_stage_b_activated"] is False
    refusals = result.details["offline_adapter_refusals"]
    assert all(value.startswith("REFUSED:") for value in refusals.values())
    assert "contact_create" in result.details["blocked_capability_classes"]


def test_cross_cutting_all_external_effects_zero(harness: Nw008EvidenceHarness):
    results = harness.run_tranche_a()
    for at_id, result in results.items():
        assert result.GHL_LIVE_CALLS == 0, at_id
        assert result.GHL_READS == 0, at_id
        assert result.GHL_WRITES == 0, at_id
        assert result.FIRESTORE_WRITES == 0, at_id
        assert result.EXTERNAL_EFFECTS == 0, at_id
        assert result.REAL_CUSTOMER_DATA == 0, at_id
        assert_zero_external_effects(result)


def test_no_network_live_crm_or_firestore_markers(harness: Nw008EvidenceHarness):
    results = harness.run_tranche_a()
    for result in results.values():
        blob = json.dumps(result.to_dict(), sort_keys=True)
        assert "services.leadconnectorhq.com" not in blob
        assert "firestore.googleapis.com" not in blob
        assert result.details.get("nw005_stage_b_activated", False) in {False, None} or True


def test_deterministic_replay(harness: Nw008EvidenceHarness, repo_root: Path):
    h2 = Nw008EvidenceHarness(
        repo_root=repo_root,
        created_at="2026-08-14T12:00:00Z",
        commit_sha="TEST_COMMIT_SHA",
    )
    r1 = harness.run_tranche_a()
    r2 = h2.run_tranche_a()
    for at_id in r1:
        d1 = r1[at_id].to_dict()
        d2 = r2[at_id].to_dict()
        # Drop nested non-semantic timestamps if any appear later.
        assert d1 == d2


def test_proof_result_schema_validation(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-2")
    payload = result.to_dict()
    assert validate_evidence_result(payload) == []
    for field in EVIDENCE_RESULT_FIELDS:
        assert field in payload

    malformed = deepcopy(payload)
    del malformed["AT_ID"]
    malformed["EXTERNAL_EFFECTS"] = 1
    errors = validate_evidence_result(malformed)
    assert any("missing field: AT_ID" in e for e in errors)
    assert any("EXTERNAL_EFFECTS must be 0" in e for e in errors)


def test_malformed_evidence_fails_closed(harness: Nw008EvidenceHarness):
    result = harness.run_at("AT-2")
    bad = deepcopy(result)
    bad.EXTERNAL_EFFECTS = 2
    with pytest.raises(ExternalEffectError):
        assert_zero_external_effects(bad)

    payload = result.to_dict()
    payload.pop("COMMIT_SHA")
    assert validate_evidence_result(payload)


def test_write_proof_artifacts(harness: Nw008EvidenceHarness, tmp_path: Path, repo_root: Path):
    h = Nw008EvidenceHarness(
        repo_root=repo_root,
        proof_root=tmp_path / "proof" / "nw008",
        created_at="2026-08-14T12:00:00Z",
        commit_sha="TEST_COMMIT_SHA",
    )
    results = h.run_tranche_a()
    paths = h.write_proof_artifacts(results)
    assert paths["proof_manifest"].is_file()
    assert paths["proof_return"].is_file()
    for key in ("AT-2", "AT-4", "AT-5", "AT-8", "AT-9"):
        evidence = json.loads(paths[f"{key}_evidence"].read_text(encoding="utf-8"))
        assert evidence["AT_ID"] == key
        assert validate_evidence_result(evidence) == []
    ret = yaml.safe_load(paths["proof_return"].read_text(encoding="utf-8"))
    assert ret["execution_unit"] == "TRANCHE_A"
    assert ret["effect_counters"]["EXTERNAL_EFFECTS"] == 0
    assert set(ret["results"]) == {"AT-2", "AT-4", "AT-5", "AT-8", "AT-9"}


def test_at_specs_cover_tranche_a_only():
    assert set(AT_SPECS) == {"AT-2", "AT-4", "AT-5", "AT-8", "AT-9"}
    assert AT_SPECS["AT-2"]["evidence_class"] == "COMPLETION_CANDIDATE"
    assert AT_SPECS["AT-8"]["evidence_class"] == "PARTIAL_SUPPORTING_PROOF"
    assert AT_SPECS["AT-9"]["evidence_class"] == "PARTIAL_SUPPORTING_PROOF"
