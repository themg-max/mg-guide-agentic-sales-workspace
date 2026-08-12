"""Contact/opportunity resolution against synthetic CRM (offline only)."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from .crm_store import SyntheticCrmStore
from .models import empty_resolution


def _prospect_participants(
    participants: Sequence[Mapping[str, Any]],
) -> List[Mapping[str, Any]]:
    prospects = [p for p in participants if p.get("role") in {"prospect", "client"}]
    if prospects:
        return list(prospects)
    # Fall back to non-agent participants.
    others = [p for p in participants if p.get("role") != "agent"]
    return list(others) if others else list(participants)


def resolve_relationship(
    store: SyntheticCrmStore,
    *,
    participants: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Resolve CRM relationship context.

    Returns (resolution_dict, evidence_dict).
    """
    prospects = _prospect_participants(participants)
    participant_keys = [
        {
            "role": str(p.get("role") or "unknown"),
            "name": p.get("name"),
            "email": p.get("email"),
            "phone": p.get("phone"),
        }
        for p in prospects
    ]

    # Insufficient identifiers across all prospects.
    usable = [
        p
        for p in prospects
        if p.get("email") or p.get("phone") or (p.get("name") and str(p.get("name")).strip())
    ]
    if not usable:
        resolution = empty_resolution(status="insufficient_context", match_basis="none")
        evidence = {
            "participant_keys": participant_keys,
            "resolution_confidence": 0.0,
            "notes": "No usable participant identifiers for CRM resolution.",
        }
        return resolution, evidence

    # Prefer email, then phone, then name — first prospect with strongest key.
    ordered = sorted(
        usable,
        key=lambda p: (
            0 if p.get("email") else 1 if p.get("phone") else 2,
        ),
    )

    collected: List[Dict[str, Any]] = []
    match_basis = "none"
    seen_ids = set()

    for prospect in ordered:
        email = prospect.get("email")
        phone = prospect.get("phone")
        name = prospect.get("name")
        result = store.search_contacts(email=email, phone=phone, name=name)
        records = list(result.get("records") or [])
        if not records:
            continue
        if email and any(
            (r.get("email") or "").lower() == str(email).lower() for r in records
        ):
            local_basis = "email"
        elif phone:
            local_basis = "phone"
        else:
            local_basis = "name"
        if match_basis == "none":
            match_basis = local_basis
        elif match_basis != local_basis and local_basis == "email":
            match_basis = "email"
        for rec in records:
            rid = rec.get("id")
            if rid in seen_ids:
                continue
            seen_ids.add(rid)
            collected.append(rec)

    if not collected:
        resolution = empty_resolution(status="not_found", match_basis=match_basis)
        evidence = {
            "participant_keys": participant_keys,
            "resolution_confidence": 0.2,
            "notes": "No synthetic CRM contacts matched participant identifiers.",
        }
        return resolution, evidence

    candidates = [
        {
            "contact_id": str(c.get("id")),
            "display_name": _display_name(c),
            "email": c.get("email"),
            "phone": c.get("phone"),
            "match_basis": match_basis,
        }
        for c in collected
    ]

    if len(collected) > 1:
        resolution = {
            "lifecycle": "complete",
            "status": "ambiguous",
            "contact_id": None,
            "opportunity_id": None,
            "match_basis": match_basis,
            "candidate_count": len(collected),
            "current_stage": None,
            "candidates": candidates,
            "contact": None,
            "opportunity": None,
        }
        evidence = {
            "participant_keys": participant_keys,
            "resolution_confidence": 0.45,
            "notes": (
                f"Ambiguous contact match: {len(collected)} synthetic candidates; "
                "fail-closed with zero CRM writes."
            ),
        }
        return resolution, evidence

    # Unique contact match.
    contact_norm = collected[0]
    contact_id = str(contact_norm.get("id"))
    # Optional exact get-contact through adapter.
    got = store.get_contact(contact_id)
    contact_record = (got.get("records") or [contact_norm])[0]

    opp_result = store.search_opportunities(contact_id=contact_id)
    opportunities = list(opp_result.get("records") or [])

    contact_out = {
        "id": str(contact_record.get("id")),
        "first_name": contact_record.get("first_name"),
        "last_name": contact_record.get("last_name"),
        "email": contact_record.get("email"),
        "phone": contact_record.get("phone"),
        "company_name": contact_record.get("company_name"),
    }

    if not opportunities:
        resolution = {
            "lifecycle": "complete",
            "status": "opportunity_missing",
            "contact_id": contact_id,
            "opportunity_id": None,
            "match_basis": match_basis,
            "candidate_count": 1,
            "current_stage": None,
            "candidates": candidates,
            "contact": contact_out,
            "opportunity": None,
        }
        evidence = {
            "participant_keys": participant_keys,
            "resolution_confidence": 0.7,
            "notes": (
                "Unique synthetic contact matched but no open opportunity found."
            ),
        }
        return resolution, evidence

    # Prefer single open opportunity; if multiple, take first deterministically by id.
    opportunities_sorted = sorted(opportunities, key=lambda o: str(o.get("id") or ""))
    opp = opportunities_sorted[0]
    stage_id = opp.get("pipeline_stage_id")
    # Resolve human stage name via pipelines metadata (offline).
    store.get_pipelines()
    stage_name = store.stage_name_for(stage_id)

    opportunity_out = {
        "id": str(opp.get("id")),
        "contact_id": str(opp.get("contact_id") or contact_id),
        "pipeline_id": opp.get("pipeline_id"),
        "pipeline_stage_id": stage_id,
        "name": opp.get("name"),
        "status": opp.get("status"),
        "stage_name": stage_name,
        "monetary_value": opp.get("monetary_value"),
    }

    resolution = {
        "lifecycle": "complete",
        "status": "matched",
        "contact_id": contact_id,
        "opportunity_id": opportunity_out["id"],
        "match_basis": match_basis,
        "candidate_count": 1,
        "current_stage": stage_name,
        "candidates": candidates,
        "contact": contact_out,
        "opportunity": opportunity_out,
    }
    evidence = {
        "participant_keys": participant_keys,
        "resolution_confidence": 0.95 if match_basis == "email" else 0.85,
        "notes": (
            "Unique synthetic contact and opportunity matched via offline GHL adapter."
        ),
    }
    return resolution, evidence


def _display_name(contact: Mapping[str, Any]) -> Optional[str]:
    first = contact.get("first_name") or ""
    last = contact.get("last_name") or ""
    name = f"{first} {last}".strip()
    return name or None
