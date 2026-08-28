from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
from typing import Callable

import pytest

from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from integrations.ghl import At1ExecutionContext, BoundedAt1Input, DeterministicGhlFixtureTransport
from orchestration.transcript_to_runner_composition import (
    TranscriptRunnerCompositionError,
    TranscriptToRunnerComposition,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
AT1_FIXTURE = json.loads(
    (REPO_ROOT / "fixtures" / "ghl" / "at1-bounded-executor.json").read_text(
        encoding="utf-8"
    )
)
SOURCE_SIDECAR = json.loads(
    (REPO_ROOT / "fixtures" / "transcript-success.expected.json").read_text(
        encoding="utf-8"
    )
)
SOURCE_TRANSCRIPT = (
    REPO_ROOT / "fixtures" / "transcript-success.txt"
).read_text(encoding="utf-8")


def _request() -> ProviderRequest:
    return ProviderRequest(
        fixture_id=SOURCE_SIDECAR["fixture_id"],
        transcript_text=SOURCE_TRANSCRIPT,
        transcript_path=None,
        meeting=dict(SOURCE_SIDECAR["meeting"]),
        participants=list(SOURCE_SIDECAR["participants"]),
        extraction_result=dict(SOURCE_SIDECAR["extraction_result"]),
        extraction_confidence=SOURCE_SIDECAR["extraction_confidence"],
        evidence_references=list(SOURCE_SIDECAR["evidence_references"]),
    )


def _target_binding() -> dict[str, str]:
    return {
        name: value
        for name, value in AT1_FIXTURE["binding"].items()
        if name
        not in {"expected_note_content_or_fingerprint", "transcript_content"}
    }


def _composition() -> TranscriptToRunnerComposition:
    return TranscriptToRunnerComposition.build(
        source_transcript=SOURCE_TRANSCRIPT,
        processor=MeetingContextAgent.for_fixture_mode(),
        processor_request=_request(),
        target_binding=_target_binding(),
    )


def _transport(composition: TranscriptToRunnerComposition) -> DeterministicGhlFixtureTransport:
    fixture = deepcopy(AT1_FIXTURE)
    fixture["binding"]["expected_note_content_or_fingerprint"] = (
        composition.canonical_note_content
    )
    fixture["binding"]["transcript_content"] = composition.source_transcript
    for call in fixture["cases"]["success"]["calls"]:
        operation_id = call["operation_id"]
        record = call["response"].get("record")
        if operation_id == "create-note":
            call["arguments"]["content_or_fingerprint"] = composition.canonical_note_content
        elif operation_id == "get-note":
            record["content_or_fingerprint"] = composition.canonical_note_content
        if isinstance(record, dict):
            if operation_id == "get-contact":
                record["location_id"] = fixture["binding"]["location_id"]
            elif operation_id == "get-opportunity":
                record["contact_id"] = fixture["binding"]["contact_id"]
                record["pipeline_id"] = fixture["binding"]["pipeline_id"]
                record["location_id"] = fixture["binding"]["location_id"]
            elif operation_id == "get-note":
                record["contact_id"] = fixture["binding"]["contact_id"]
    return DeterministicGhlFixtureTransport(fixture, "success")


def _context() -> At1ExecutionContext:
    return At1ExecutionContext(
        note_idempotency_key="synthetic-composed-note-key",
        stage_idempotency_key="synthetic-composed-stage-key",
    )


def test_composes_actual_meeting_context_output_into_pr253_runner_and_seal() -> None:
    composition = _composition()
    transport = _transport(composition)

    execution = composition.execute(transport=transport, context=_context())

    transport.assert_exhausted()
    assert execution.result.disposition == "completed"
    assert execution.result.operations == (
        "get-contact",
        "get-opportunity",
        "create-note",
        "get-note",
        "update-opportunity",
        "get-opportunity",
    )
    assert execution.prewrite_seal.transcript_content == SOURCE_TRANSCRIPT
    assert execution.prewrite_seal.transcript_sha256 == composition.source_transcript_sha256
    assert execution.prewrite_seal.canonical_note_content == composition.canonical_note_content
    assert execution.prewrite_seal.canonical_note_sha256 == composition.canonical_note_sha256
    assert (
        composition.runner_input.expected_note_content_or_fingerprint
        == composition.canonical_note_content
    )
    processor_output = json.loads(composition.processor_output)
    assert processor_output["agent"] == "meeting_context_agent"
    assert processor_output["provider"] == "fixture"
    assert processor_output["meeting"]["transcript_hash"] == composition.source_transcript_sha256
    assert composition.evidence()["INDEPENDENT_NOTE_INJECTION_PATH_USED"] == "NO"


@pytest.mark.parametrize(
    "tamper, message",
    [
        (
            lambda value: replace(value, source_transcript="tampered after derivation"),
            "source transcript changed after derivation",
        ),
        (
            lambda value: replace(value, canonical_note_content="tampered canonical note"),
            "canonical note differs from processor output",
        ),
        (
            lambda value: replace(
                value,
                runner_input=BoundedAt1Input(
                    **{
                        **value.runner_input.__dict__,
                        "expected_note_content_or_fingerprint": "independent note injection",
                    }
                ),
            ),
            "runner expected note differs from processor-derived canonical note",
        ),
        (
            lambda value: replace(value, processor_output=""),
            "processor output is required",
        ),
        (
            lambda value: replace(value, source_transcript_sha256=""),
            "source transcript SHA256 is required",
        ),
        (
            lambda value: replace(value, canonical_note_sha256=""),
            "canonical note SHA256 is required",
        ),
    ],
)
def test_composition_tampering_fails_before_any_transport_call(
    tamper: Callable[
        [TranscriptToRunnerComposition], TranscriptToRunnerComposition
    ],
    message: str,
) -> None:
    composition = _composition()
    transport = _transport(composition)

    with pytest.raises(TranscriptRunnerCompositionError, match=message):
        tamper(composition).execute(transport=transport, context=_context())

    assert transport.calls == []
    assert transport.envelopes == []
