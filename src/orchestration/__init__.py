"""Phase 1 deterministic orchestration for meeting_follow_up_v1."""

from .runner import RunResult, WorkflowRunner

__all__ = ["RunResult", "WorkflowRunner"]
# NW-008 harness is imported explicitly via orchestration.nw008_harness to avoid
# pulling card/adapter dependencies into baseline Phase 1 import paths.
