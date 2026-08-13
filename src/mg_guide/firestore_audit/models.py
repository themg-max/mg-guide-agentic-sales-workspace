"""Models and constants for workflow_run_audit_v1 projection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

AUDIT_SCHEMA = "workflow_run_audit_v1"
PACKET_SCHEMA = "meeting_follow_up_packet_v1"
WORKFLOW_ID = "meeting_follow_up_v1"
PROJECTION_VERSION = "workflow_run_audit_v1"
AUDIT_STATUS_MAPPER_ID = "audit_status_mapper_v1"
IDEMPOTENCY_STRATEGY = "create_only_if_absent"

TERMINAL_STATES = frozenset(
    {
        "completed",
        "completed_with_review",
        "blocked",
        "failed",
    }
)

NON_TERMINAL_STATES = frozenset(
    {
        "received",
        "extracting",
        "resolving",
        "evaluating",
        "writing",
    }
)

CARD_STATES = frozenset(
    {
        "completed",
        "completed_with_review",
        "blocked",
        "failed",
        "in_progress",
    }
)

WRITER_MODES = frozenset(
    {
        "local_fixture",
        "emulator",
        "firestore_test_project",
    }
)


@dataclass(frozen=True)
class ProjectionContext:
    """Explicit pure-projection inputs (no internal clocks/env/I/O)."""

    recorded_at: str
    fixture_id: Optional[str]
    source_refs: Tuple[str, ...]
    writer_component: str
    writer_component_version: str
    writer_mode: str

    def __post_init__(self) -> None:
        if not isinstance(self.recorded_at, str) or not self.recorded_at.strip():
            raise ValueError("projection_context.recorded_at must be a non-empty string")
        if self.fixture_id is not None and (
            not isinstance(self.fixture_id, str) or not self.fixture_id.strip()
        ):
            raise ValueError("projection_context.fixture_id must be None or non-empty string")
        if not isinstance(self.source_refs, (tuple, list)):
            raise ValueError("projection_context.source_refs must be a sequence of strings")
        refs = tuple(self.source_refs)
        if any(not isinstance(r, str) or not r.strip() for r in refs):
            raise ValueError("projection_context.source_refs entries must be non-empty strings")
        object.__setattr__(self, "source_refs", refs)
        if not isinstance(self.writer_component, str) or not self.writer_component.strip():
            raise ValueError("projection_context.writer_component must be a non-empty string")
        if (
            not isinstance(self.writer_component_version, str)
            or not self.writer_component_version.strip()
        ):
            raise ValueError(
                "projection_context.writer_component_version must be a non-empty string"
            )
        if self.writer_mode not in WRITER_MODES:
            raise ValueError(
                f"projection_context.writer_mode must be one of {sorted(WRITER_MODES)}"
            )

    @classmethod
    def from_mapping(cls, data: dict) -> "ProjectionContext":
        refs = data.get("source_refs") or []
        if isinstance(refs, list):
            refs_t: Sequence[str] = tuple(refs)
        else:
            refs_t = tuple(refs)
        return cls(
            recorded_at=data["recorded_at"],
            fixture_id=data.get("fixture_id"),
            source_refs=tuple(refs_t),
            writer_component=data["writer_component"],
            writer_component_version=data["writer_component_version"],
            writer_mode=data["writer_mode"],
        )

    def to_dict(self) -> dict:
        return {
            "recorded_at": self.recorded_at,
            "fixture_id": self.fixture_id,
            "source_refs": list(self.source_refs),
            "writer_component": self.writer_component,
            "writer_component_version": self.writer_component_version,
            "writer_mode": self.writer_mode,
        }


def default_stage_a_context(
    *,
    fixture_id: str,
    source_refs: Optional[List[str]] = None,
    recorded_at: str = "2026-08-12T20:00:00Z",
    writer_component_version: str = "0.1.0-stage-a",
) -> ProjectionContext:
    """Stable synthetic context for Stage A golden fixtures."""
    refs = source_refs or [f"fixtures/nw005/packets/{fixture_id}"]
    return ProjectionContext(
        recorded_at=recorded_at,
        fixture_id=fixture_id,
        source_refs=tuple(refs),
        writer_component="mg_guide.firestore_audit.project",
        writer_component_version=writer_component_version,
        writer_mode="local_fixture",
    )
