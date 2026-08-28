"""Offline composition from meeting-context extraction to the bounded AT-1 runner."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

from agents.meeting_context import MeetingContextAgent
from agents.meeting_context.providers.base import ProviderRequest
from integrations.ghl import (
    At1ExecutionContext,
    BoundedAt1GhlExecutor,
    BoundedAt1Input,
    BoundedAt1Result,
    DeterministicGhlFixtureTransport,
)
from integrations.ghl.bounded_at1_executor import FixtureResponse


CANONICAL_NOTE_SCHEMA = "nw008_transcript_derived_note_v1"
_TARGET_BINDING_FIELDS = frozenset(
    {
        "location_id",
        "contact_id",
        "opportunity_id",
        "pipeline_id",
        "expected_initial_stage_id",
        "authorized_final_stage_id",
    }
)


class TranscriptRunnerCompositionError(ValueError):
    """Raised when the transcript-to-runner binding lacks an exact provenance chain."""


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def canonical_note_from_processor_output(processor_output: str) -> str:
    """Create the sole accepted note representation from captured processor bytes."""
    try:
        parsed = json.loads(processor_output)
    except json.JSONDecodeError as error:
        raise TranscriptRunnerCompositionError(
            "processor output must be canonical JSON"
        ) from error
    if not isinstance(parsed, dict) or _canonical_json(parsed) != processor_output:
        raise TranscriptRunnerCompositionError(
            "processor output must be a canonical JSON object"
        )
    return _canonical_json(
        {
            "meeting_context": parsed,
            "schema": CANONICAL_NOTE_SCHEMA,
        }
    )


@dataclass(frozen=True)
class PrewriteSealCapture:
    """The exact synthetic values received by the PR253 prewrite-seal hook."""

    transcript_content: str
    transcript_sha256: str
    canonical_note_content: str
    canonical_note_sha256: str


class _PrewriteSealCaptureTransport:
    """Offline fixture transport wrapper that records the runner's seal invocation."""

    def __init__(self, delegate: DeterministicGhlFixtureTransport) -> None:
        self._delegate = delegate
        self.prewrite_seals: list[PrewriteSealCapture] = []

    def dispatch(self, envelope: Mapping[str, Any]) -> FixtureResponse:
        return self._delegate.dispatch(envelope)

    def record_prewrite_provenance(
        self,
        *,
        transcript_content: str,
        transcript_sha256: str,
        expected_note_content: str,
        expected_note_sha256: str,
    ) -> None:
        self.prewrite_seals.append(
            PrewriteSealCapture(
                transcript_content=transcript_content,
                transcript_sha256=transcript_sha256,
                canonical_note_content=expected_note_content,
                canonical_note_sha256=expected_note_sha256,
            )
        )


@dataclass(frozen=True)
class TranscriptToRunnerComposition:
    """Immutable offline evidence chain for one synthetic transcript-runner execution."""

    source_transcript: str
    source_transcript_sha256: str
    processor_output: str
    processor_output_sha256: str
    canonical_note_content: str
    canonical_note_sha256: str
    runner_input: BoundedAt1Input

    @classmethod
    def build(
        cls,
        *,
        source_transcript: str,
        processor: MeetingContextAgent,
        processor_request: ProviderRequest,
        target_binding: Mapping[str, str],
    ) -> "TranscriptToRunnerComposition":
        """Invoke meeting-context extraction and bind its exact output to AT-1."""
        if not isinstance(source_transcript, str) or not source_transcript.strip():
            raise TranscriptRunnerCompositionError("source transcript must be non-empty")
        if processor_request.transcript_text != source_transcript:
            raise TranscriptRunnerCompositionError(
                "processor request transcript must equal the source transcript"
            )
        if set(target_binding) != _TARGET_BINDING_FIELDS:
            raise TranscriptRunnerCompositionError(
                "target binding fields must be exact and must not accept a note value"
            )
        if not all(
            isinstance(value, str) and value.strip() for value in target_binding.values()
        ):
            raise TranscriptRunnerCompositionError(
                "target binding values must be non-empty strings"
            )

        source_transcript_sha256 = sha256(source_transcript.encode("utf-8")).hexdigest()
        processor_result = processor.run(processor_request).to_dict()
        processor_output = _canonical_json(processor_result)
        processor_output_sha256 = sha256(processor_output.encode("utf-8")).hexdigest()
        canonical_note_content = canonical_note_from_processor_output(processor_output)
        canonical_note_sha256 = sha256(canonical_note_content.encode("utf-8")).hexdigest()
        runner_input = BoundedAt1Input.from_mapping(
            {
                **dict(target_binding),
                "expected_note_content_or_fingerprint": canonical_note_content,
                "transcript_content": source_transcript,
            }
        )
        composition = cls(
            source_transcript=source_transcript,
            source_transcript_sha256=source_transcript_sha256,
            processor_output=processor_output,
            processor_output_sha256=processor_output_sha256,
            canonical_note_content=canonical_note_content,
            canonical_note_sha256=canonical_note_sha256,
            runner_input=runner_input,
        )
        composition.validate()
        return composition

    def validate(self) -> None:
        """Fail closed before runner construction when any provenance value changes."""
        required_values = {
            "source transcript": self.source_transcript,
            "source transcript SHA256": self.source_transcript_sha256,
            "processor output": self.processor_output,
            "processor output SHA256": self.processor_output_sha256,
            "canonical note": self.canonical_note_content,
            "canonical note SHA256": self.canonical_note_sha256,
        }
        for name, value in required_values.items():
            if not isinstance(value, str) or not value:
                raise TranscriptRunnerCompositionError(f"{name} is required")
        if sha256(self.source_transcript.encode("utf-8")).hexdigest() != self.source_transcript_sha256:
            raise TranscriptRunnerCompositionError(
                "source transcript changed after derivation"
            )
        if sha256(self.processor_output.encode("utf-8")).hexdigest() != self.processor_output_sha256:
            raise TranscriptRunnerCompositionError("processor output hash does not match")

        try:
            processor_output = json.loads(self.processor_output)
        except json.JSONDecodeError as error:
            raise TranscriptRunnerCompositionError(
                "processor provenance is not valid JSON"
            ) from error
        if not isinstance(processor_output, dict):
            raise TranscriptRunnerCompositionError("processor provenance must be an object")
        meeting = processor_output.get("meeting")
        if not isinstance(meeting, dict) or meeting.get(
            "transcript_hash"
        ) != self.source_transcript_sha256:
            raise TranscriptRunnerCompositionError(
                "processor provenance does not bind the source transcript hash"
            )

        derived_note = canonical_note_from_processor_output(self.processor_output)
        if derived_note != self.canonical_note_content:
            raise TranscriptRunnerCompositionError(
                "canonical note differs from processor output"
            )
        if sha256(self.canonical_note_content.encode("utf-8")).hexdigest() != self.canonical_note_sha256:
            raise TranscriptRunnerCompositionError("canonical note hash does not match")
        if self.runner_input.transcript_content != self.source_transcript:
            raise TranscriptRunnerCompositionError(
                "runner transcript differs from the derived source transcript"
            )
        if (
            self.runner_input.expected_note_content_or_fingerprint
            != self.canonical_note_content
        ):
            raise TranscriptRunnerCompositionError(
                "runner expected note differs from processor-derived canonical note"
            )

    def execute(
        self,
        *,
        transport: DeterministicGhlFixtureTransport,
        context: At1ExecutionContext,
    ) -> "TranscriptToRunnerExecution":
        """Execute through PR253 only after validating the full offline composition."""
        self.validate()
        capture_transport = _PrewriteSealCaptureTransport(transport)
        result = BoundedAt1GhlExecutor(capture_transport).execute(
            self.runner_input, context
        )
        if len(capture_transport.prewrite_seals) != 1:
            raise TranscriptRunnerCompositionError(
                "PR253 prewrite seal must receive exactly one provenance record"
            )
        seal = capture_transport.prewrite_seals[0]
        if (
            seal.transcript_content != self.source_transcript
            or seal.transcript_sha256 != self.source_transcript_sha256
            or seal.canonical_note_content != self.canonical_note_content
            or seal.canonical_note_sha256 != self.canonical_note_sha256
        ):
            raise TranscriptRunnerCompositionError(
                "PR253 prewrite seal did not receive the composed provenance values"
            )
        return TranscriptToRunnerExecution(result=result, prewrite_seal=seal)

    def evidence(self) -> Mapping[str, str]:
        """Return deterministic, public-safe booleans and digests for offline proof."""
        self.validate()
        return {
            "SOURCE_TRANSCRIPT_PRESENT": "YES",
            "SOURCE_TRANSCRIPT_SHA256": self.source_transcript_sha256,
            "SOURCE_TRANSCRIPT_SHA256_CAPTURED": "YES",
            "TRANSCRIPT_PROCESSOR_INVOKED": "YES",
            "TRANSCRIPT_PROCESSOR_OUTPUT_CAPTURED": "YES",
            "PROCESSOR_OUTPUT_SHA256": self.processor_output_sha256,
            "CANONICAL_NOTE_DERIVED_FROM_PROCESSOR_OUTPUT": "YES",
            "CANONICAL_NOTE_SHA256": self.canonical_note_sha256,
            "CANONICAL_NOTE_SHA256_CAPTURED": "YES",
            "RUNNER_EXPECTED_NOTE_BYTES_EQUAL_DERIVED_NOTE_BYTES": "YES",
            "RUNNER_EXPECTED_NOTE_SHA256_EQUAL_DERIVED_NOTE_SHA256": "YES",
            "INDEPENDENT_NOTE_INJECTION_PATH_USED": "NO",
        }

@dataclass(frozen=True)
class TranscriptToRunnerExecution:
    """Runner result coupled to its observed prewrite-seal inputs."""

    result: BoundedAt1Result
    prewrite_seal: PrewriteSealCapture
