"""Relationship Context Agent entrypoint."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .crm_store import SyntheticCrmStore
from .longitudinal import build_longitudinal_context
from .models import RelationshipContextResult, RelationshipRequest
from .resolver import resolve_relationship
from .schema import validate_relationship_context


class RelationshipContextAgent:
    """Resolves synthetic CRM relationship context from meeting context.

    Uses Phase 2B OfflineGhlReadAdapter against synthetic fixtures only.
    Does not call live GHL, does not write CRM, does not bypass deterministic policy.
    """

    agent_id = "relationship_context_agent"

    def __init__(self, store: Optional[SyntheticCrmStore] = None) -> None:
        self.store = store or SyntheticCrmStore.from_fixture_path()

    def run(self, request: RelationshipRequest) -> RelationshipContextResult:
        meeting_context = dict(request.meeting_context)
        meeting = dict(meeting_context.get("meeting") or {})
        participants = list(meeting_context.get("participants") or [])
        if not meeting.get("meeting_id"):
            raise ValueError("meeting_context.meeting.meeting_id is required")
        if not participants:
            raise ValueError("meeting_context.participants must be non-empty")

        resolution, evidence = resolve_relationship(
            self.store, participants=participants
        )

        result = RelationshipContextResult(
            schema="relationship_context_v1",
            agent=self.agent_id,
            provider="offline_ghl_fixture",
            meeting_ref={
                "meeting_id": meeting["meeting_id"],
                "transcript_hash": meeting.get("transcript_hash") or "unknown",
                "run_id": request.run_id,
            },
            resolution=resolution,
            crm_source={
                "mode": "offline_synthetic",
                "adapter": "phase2b_offline_ghl_read_adapter",
                "live_calls": 0,
                "writes": 0,
                "real_customer_data": 0,
                "operations_used": list(dict.fromkeys(self.store.operations_used)),
            },
            evidence=evidence,
            external_effects=0,
            policy_authority={
                "deterministic_policy_bypass": False,
                "notes": (
                    "Relationship Context Agent proposes CRM resolution only; "
                    "deterministic policy remains authoritative for any CRM mutation. "
                    "Offline synthetic reads only (Phase 2B adapter)."
                ),
            },
            longitudinal_context=build_longitudinal_context(
                meeting_context,
                prior_context=request.prior_context,
            ),
        )

        payload = result.to_dict()
        ok, errors = validate_relationship_context(payload)
        if not ok:
            raise ValueError(
                "Relationship context failed schema validation: " + "; ".join(errors)
            )
        if payload["external_effects"] != 0:
            raise ValueError("Relationship Context Agent must set external_effects=0")
        if payload["policy_authority"]["deterministic_policy_bypass"] is not False:
            raise ValueError("Deterministic policy bypass is forbidden")
        if payload["crm_source"]["live_calls"] != 0:
            raise ValueError("GHL live calls are forbidden in Unit 2")
        if payload["crm_source"]["writes"] != 0:
            raise ValueError("GHL writes are forbidden")
        return result

    def telemetry(self) -> Dict[str, Any]:
        store_tel = self.store.telemetry()
        return {
            "agent_id": self.agent_id,
            "provider": "offline_ghl_fixture",
            "offline_ghl_adapter_used": True,
            "synthetic_crm_context_only": True,
            "external_effects": 0,
            "deterministic_policy_bypass": False,
            "ghl_live_calls": store_tel["live_calls"],
            "ghl_writes": store_tel["writes"],
            "real_customer_data": 0,
            "crm_store": store_tel,
        }
