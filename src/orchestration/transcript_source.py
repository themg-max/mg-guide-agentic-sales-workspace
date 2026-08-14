"""TRANSCRIPT_SOURCE_ENVELOPE_V1 — provider-neutral transcript intake boundary.

This module implements the minimal deterministic competition-local envelope
contract used by NW-008 Tranche C. It does not perform Google Workspace
acquisition, OAuth, Drive API calls, or real grant evaluation.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from jsonschema import Draft202012Validator

from agents.meeting_context.providers.base import ProviderRequest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENVELOPE_SCHEMA_PATH = REPO_ROOT / "contracts" / "transcript_source_envelope.schema.json"


class TranscriptSourceEnvelopeError(ValueError):
    """Raised when an envelope violates the TRANSCRIPT_SOURCE_ENVELOPE_V1 contract."""


@dataclass(frozen=True)
class TranscriptSourceEnvelope:
    """Typed carrier for the provider-neutral transcript source envelope."""

    source: Dict[str, Any]
    ownership: Dict[str, Any]
    access_context: Dict[str, Any]
    meeting: Dict[str, Any]
    artifact: Dict[str, Any]
    data_classification: Dict[str, Any]
    provenance: Dict[str, Any]
    content: Dict[str, Any]
    security: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": "transcript_source_envelope_v1",
            "source": deepcopy(dict(self.source)),
            "ownership": deepcopy(dict(self.ownership)),
            "access_context": deepcopy(dict(self.access_context)),
            "meeting": deepcopy(dict(self.meeting)),
            "artifact": deepcopy(dict(self.artifact)),
            "data_classification": deepcopy(dict(self.data_classification)),
            "provenance": deepcopy(dict(self.provenance)),
            "content": deepcopy(dict(self.content)),
            "security": deepcopy(dict(self.security)),
        }

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content["text"].encode("utf-8")).hexdigest()


def _load_envelope_schema() -> Dict[str, Any]:
    return json.loads(ENVELOPE_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_envelope(data: Mapping[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a raw envelope dict against TRANSCRIPT_SOURCE_ENVELOPE_V1 schema."""
    validator = Draft202012Validator(_load_envelope_schema())
    errors = sorted(validator.iter_errors(dict(data)), key=lambda e: list(e.path))
    messages = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        messages.append(f"{path}: {err.message}")
    if not messages:
        if data.get("data_classification", {}).get("treat_content_as_data_only") is not True:
            messages.append("data_classification.treat_content_as_data_only must be true")
        if data.get("content", {}).get("instruction_authority") is not False:
            messages.append("content.instruction_authority must be false")
        artifact_hash = (data.get("artifact") or {}).get("content_hash")
        if artifact_hash:
            content_text = (data.get("content") or {}).get("text", "")
            expected = hashlib.sha256(content_text.encode("utf-8")).hexdigest()
            if artifact_hash != expected:
                messages.append(
                    f"artifact.content_hash mismatch: expected {expected}, got {artifact_hash}"
                )
    return (not messages, messages)


def envelope_from_dict(data: Mapping[str, Any]) -> TranscriptSourceEnvelope:
    """Parse and validate a raw envelope dict into a typed envelope."""
    ok, errors = validate_envelope(data)
    if not ok:
        raise TranscriptSourceEnvelopeError(
            "Envelope validation failed: " + "; ".join(errors)
        )
    return TranscriptSourceEnvelope(
        source=dict(data["source"]),
        ownership=dict(data["ownership"]),
        access_context=dict(data["access_context"]),
        meeting=dict(data["meeting"]),
        artifact=dict(data["artifact"]),
        data_classification=dict(data["data_classification"]),
        provenance=dict(data["provenance"]),
        content=dict(data["content"]),
        security=dict(data["security"]),
    )


def envelope_to_provider_request(
    envelope: TranscriptSourceEnvelope,
    *,
    extraction_result: Mapping[str, Any],
    extraction_confidence: float,
    evidence_references: Optional[List[Dict[str, str]]] = None,
    participants: Optional[List[Dict[str, Any]]] = None,
) -> ProviderRequest:
    """Convert a validated transcript source envelope into a Meeting Context ProviderRequest.

    The envelope is the authoritative transcript source; this adapter only
    reshapes data for the existing fixture-capable fleet entrypoint.
    """
    meeting = {
        "meeting_id": envelope.meeting["meeting_id"],
        "occurred_at": envelope.meeting.get("started_at") or "",
        # The existing meeting_context_v1 / packet schemas require
        # source=synthetic_demo for synthetic competition fixtures. The envelope
        # still records the acquisition source as synthetic_fixture.
        "source": "synthetic_demo",
        "transcript_hash": envelope.content_hash,
    }
    return ProviderRequest(
        fixture_id=envelope.artifact["artifact_id"],
        transcript_text=envelope.content["text"],
        transcript_path=None,
        meeting=meeting,
        participants=list(participants or []),
        extraction_result=dict(extraction_result),
        extraction_confidence=float(extraction_confidence),
        evidence_references=list(evidence_references or []),
    )
