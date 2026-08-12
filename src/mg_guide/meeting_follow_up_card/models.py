"""Deterministic card view model for NW-006."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

CARD_SCHEMA = "mg_guide_meeting_follow_up_card_v1"
SOURCE_SCHEMA = "meeting_follow_up_packet_v1"
MAPPER_ID = "meeting_follow_up_card_mapper_v1"


@dataclass(frozen=True)
class IntentDisplay:
    kind: str
    status: Optional[str]
    summary: str
    from_stage: Optional[str]
    to_stage: Optional[str]


@dataclass(frozen=True)
class CardViewModel:
    schema: str
    card_state: str
    run: Dict[str, Any]
    meeting: Dict[str, Any]
    framing: Dict[str, Any]
    policy_display: Dict[str, Any]
    ui_integrity: Dict[str, Any]
    crm_display: Dict[str, Any]
    metadata: Dict[str, Any]
    learning: Dict[str, Any]
    intents_display: Dict[str, Any]
    brief_display: Dict[str, Any]
    controls: Dict[str, Any]
    integrity: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


def intent_to_dict(intent: IntentDisplay) -> Dict[str, Any]:
    return asdict(intent)

