"""Synthetic CRM store backed by Phase 2B OfflineGhlReadAdapter (no network)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from integrations.ghl import OfflineGhlReadAdapter


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _norm(value: Optional[str]) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def _norm_phone(value: Optional[str]) -> str:
    if not value:
        return ""
    digits = re.sub(r"\D+", "", str(value))
    # Keep last 10 digits for US-style synthetic numbers.
    return digits[-10:] if len(digits) >= 10 else digits


@dataclass
class SyntheticCrmStore:
    """In-memory synthetic CRM universe; all reads go through OfflineGhlReadAdapter."""

    contacts: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]
    pipelines: List[Dict[str, Any]]
    adapter: OfflineGhlReadAdapter = field(default_factory=OfflineGhlReadAdapter)
    operations_used: List[str] = field(default_factory=list)
    live_calls: int = 0
    writes: int = 0

    @staticmethod
    def from_fixture_path(path: Optional[Path] = None) -> "SyntheticCrmStore":
        fixture_path = path or (
            _repo_root() / "fixtures" / "ghl" / "relationship-context-crm.json"
        )
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        return SyntheticCrmStore(
            contacts=[dict(c) for c in data.get("contacts") or []],
            opportunities=[dict(o) for o in data.get("opportunities") or []],
            pipelines=[dict(p) for p in data.get("pipelines") or []],
        )

    def _track(self, operation_id: str) -> None:
        self.operations_used.append(operation_id)
        # Offline only — never increments live_calls or writes.
        assert self.live_calls == 0
        assert self.writes == 0

    def search_contacts(
        self,
        *,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        page_limit: int = 20,
    ) -> Dict[str, Any]:
        """Search contacts using offline adapter request + synthetic match."""
        query_parts = [p for p in (email, phone, name) if p]
        query = " ".join(query_parts) if query_parts else ""
        # Exercise Phase 2B adapter request builder (no transport).
        envelope = self.adapter.build_request(
            "search-contacts-advanced",
            body={"pageLimit": page_limit, "page": 1, "query": query or " "},
        )
        assert envelope["tool"] == "execute_operation"
        self._track("search-contacts-advanced")

        matches = self._match_contacts(email=email, phone=phone, name=name)
        payload = {
            "contacts": matches,
            "meta": {
                "page": 1,
                "pageLimit": page_limit,
                "total": len(matches),
                "hasMore": False,
            },
        }
        return self.adapter.normalize_response(
            "search-contacts-advanced", 200, payload
        )

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        envelope = self.adapter.build_request(
            "get-contact", path={"contactId": contact_id}
        )
        assert envelope["arguments"]["operationId"] == "get-contact"
        self._track("get-contact")
        record = next((c for c in self.contacts if c.get("id") == contact_id), None)
        if record is None:
            return self.adapter.normalize_response(
                "get-contact",
                404,
                {"message": "Synthetic contact not found."},
            )
        return self.adapter.normalize_response(
            "get-contact", 200, {"contact": record}
        )

    def search_opportunities(self, *, contact_id: str) -> Dict[str, Any]:
        envelope = self.adapter.build_request(
            "search-opportunity",
            query={"contactId": contact_id, "limit": 20, "page": 1, "status": "open"},
        )
        assert envelope["arguments"]["operationId"] == "search-opportunity"
        self._track("search-opportunity")
        matches = [
            o for o in self.opportunities if o.get("contactId") == contact_id
        ]
        payload = {
            "opportunities": matches,
            "pagination": {
                "page": 1,
                "limit": 20,
                "totalCount": len(matches),
                "has_more": False,
            },
        }
        return self.adapter.normalize_response("search-opportunity", 200, payload)

    def get_pipelines(self) -> Dict[str, Any]:
        envelope = self.adapter.build_request("get-pipelines")
        assert envelope["arguments"]["operationId"] == "get-pipelines"
        self._track("get-pipelines")
        return self.adapter.normalize_response(
            "get-pipelines", 200, {"pipelines": self.pipelines}
        )

    def stage_name_for(self, pipeline_stage_id: Optional[str]) -> Optional[str]:
        if not pipeline_stage_id:
            return None
        for pipeline in self.pipelines:
            for stage in pipeline.get("stages") or []:
                if stage.get("id") == pipeline_stage_id:
                    return stage.get("name")
        return None

    def _match_contacts(
        self,
        *,
        email: Optional[str],
        phone: Optional[str],
        name: Optional[str],
    ) -> List[Dict[str, Any]]:
        email_n = _norm(email)
        phone_n = _norm_phone(phone)
        name_n = _norm(name)

        if email_n:
            hits = [c for c in self.contacts if _norm(c.get("email")) == email_n]
            if hits:
                return hits
        if phone_n:
            hits = [
                c for c in self.contacts if _norm_phone(c.get("phone")) == phone_n
            ]
            if hits:
                return hits
        if name_n:
            hits = []
            for c in self.contacts:
                full = _norm(
                    f"{c.get('firstName') or ''} {c.get('lastName') or ''}".strip()
                )
                if full == name_n or (
                    name_n in full and len(name_n.split()) >= 2
                ):
                    hits.append(c)
            return hits
        return []

    def telemetry(self) -> Dict[str, Any]:
        return {
            "mode": "offline_synthetic",
            "adapter": "phase2b_offline_ghl_read_adapter",
            "live_calls": self.live_calls,
            "writes": self.writes,
            "real_customer_data": 0,
            "operations_used": list(self.operations_used),
            "contact_count": len(self.contacts),
            "opportunity_count": len(self.opportunities),
        }
