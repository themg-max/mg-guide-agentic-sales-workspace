"""Deterministic longitudinal context classification for NW-008 Tranche B."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from jsonschema import Draft202012Validator


_STRUCTURED_VALUE = re.compile(r"^(?P<key>[a-z0-9_.-]+)=(?P<value>.+)$")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def _schema() -> Dict[str, Any]:
    path = _repo_root() / "contracts" / "nw008_longitudinal_context.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate_longitudinal_context(payload: Mapping[str, Any]) -> Tuple[bool, Tuple[str, ...]]:
    validator = Draft202012Validator(_schema())
    errors = sorted(validator.iter_errors(dict(payload)), key=lambda e: list(e.path))
    if not errors:
        return True, tuple()
    messages = []
    for err in errors:
        path = ".".join(str(p) for p in err.path) or "<root>"
        messages.append(f"{path}: {err.message}")
    return False, tuple(messages)


def approved_prior_context(longitudinal_context: Mapping[str, Any]) -> Dict[str, Any]:
    """Return the minimal prior context needed for the next meeting."""

    return {
        "schema": str(longitudinal_context.get("schema") or "relationship_longitudinal_context_v1"),
        "current_confirmed_facts": deepcopy(
            list(longitudinal_context.get("current_confirmed_facts") or [])
        ),
        "commitments_open": deepcopy(
            list(longitudinal_context.get("commitments_open") or [])
        ),
    }


def build_longitudinal_context(
    meeting_context: Mapping[str, Any],
    *,
    prior_context: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    meeting = dict(meeting_context.get("meeting") or {})
    meeting_id = str(meeting.get("meeting_id") or "").strip()
    if not meeting_id:
        raise ValueError("meeting_context.meeting.meeting_id is required for longitudinal context")

    extraction = dict(meeting_context.get("extraction") or {})
    evidence_index = _evidence_index(meeting_context)
    current_facts, unresolved_questions, commitment_statuses, unsupported = (
        _parse_structured_claims(
            extraction=extraction,
            meeting_id=meeting_id,
            evidence_index=evidence_index,
        )
    )
    commitment_items = _parse_commitments(
        extraction=extraction,
        meeting_id=meeting_id,
        evidence_index=evidence_index,
    )
    proposed_next_step = _parse_next_step(
        extraction=extraction,
        meeting_id=meeting_id,
        evidence_index=evidence_index,
    )

    prior = dict(prior_context or {})
    prior_facts = deepcopy(list(prior.get("current_confirmed_facts") or []))
    prior_open_commitments = deepcopy(list(prior.get("commitments_open") or []))
    _assert_unique_fact_ids(prior_facts, source="prior_context.current_confirmed_facts")
    _assert_unique_fact_ids(current_facts, source="meeting_context current facts")

    prior_by_id = {str(item["fact_id"]): item for item in prior_facts}
    unchanged: List[Dict[str, Any]] = []
    corrected: List[Dict[str, Any]] = []
    new_facts: List[Dict[str, Any]] = []
    goals_refined: List[Dict[str, Any]] = []

    for fact in current_facts:
        fact_id = str(fact["fact_id"])
        prior_fact = prior_by_id.get(fact_id)
        if prior_fact is None:
            new_facts.append(deepcopy(fact))
            if fact_id.startswith("goal."):
                goals_refined.append(_goal_refinement_from_fact(fact, kind="new"))
            continue
        if _canonical_value(prior_fact.get("value")) == _canonical_value(fact.get("value")):
            unchanged.append(
                {
                    "fact_id": fact_id,
                    "value": deepcopy(fact.get("value")),
                    "prior_meeting_id": prior_fact.get("source_meeting_id"),
                    "prior_evidence_refs": list(prior_fact.get("evidence_refs") or []),
                    "current_meeting_id": meeting_id,
                    "current_evidence_refs": list(fact.get("evidence_refs") or []),
                }
            )
            continue
        correction = {
            "fact_id": fact_id,
            "prior_value": deepcopy(prior_fact.get("value")),
            "prior_meeting_id": prior_fact.get("source_meeting_id"),
            "prior_evidence_refs": list(prior_fact.get("evidence_refs") or []),
            "new_value": deepcopy(fact.get("value")),
            "current_meeting_id": meeting_id,
            "current_evidence_refs": list(fact.get("evidence_refs") or []),
            "superseded": True,
        }
        corrected.append(correction)
        if fact_id.startswith("goal."):
            goals_refined.append(
                {
                    "fact_id": fact_id,
                    "kind": "corrected",
                    "prior_value": deepcopy(prior_fact.get("value")),
                    "new_value": deepcopy(fact.get("value")),
                    "current_meeting_id": meeting_id,
                    "current_evidence_refs": list(fact.get("evidence_refs") or []),
                }
            )

    completed_commitments: List[Dict[str, Any]] = []
    open_commitments: List[Dict[str, Any]] = []
    prior_open_by_id = {
        str(item.get("commitment_id")): item
        for item in prior_open_commitments
        if item.get("commitment_id")
    }

    for commitment_id, prior_commitment in prior_open_by_id.items():
        status = commitment_statuses.get(commitment_id)
        current_refs = list(
            evidence_index.get(f"commitment_status.{commitment_id}") or []
        )
        if status == "completed" and current_refs:
            completed_commitments.append(
                {
                    "commitment_id": commitment_id,
                    "owner": prior_commitment.get("owner"),
                    "action": prior_commitment.get("action"),
                    "due_date": prior_commitment.get("due_date"),
                    "prior_meeting_id": prior_commitment.get("source_meeting_id"),
                    "prior_evidence_refs": list(
                        prior_commitment.get("evidence_refs") or []
                    ),
                    "current_meeting_id": meeting_id,
                    "current_evidence_refs": current_refs,
                }
            )
        elif status == "open" and current_refs:
            retained = deepcopy(prior_commitment)
            retained["current_meeting_id"] = meeting_id
            retained["current_evidence_refs"] = current_refs
            open_commitments.append(retained)

    seen_open = {str(item["commitment_id"]) for item in open_commitments}
    for commitment in commitment_items:
        commitment_id = str(commitment["commitment_id"])
        if commitment_id in seen_open:
            continue
        seen_open.add(commitment_id)
        open_commitments.append(commitment)

    evidence_references = _collect_evidence_references(
        current_facts=current_facts,
        unresolved_questions=unresolved_questions,
        commitments_completed=completed_commitments,
        commitments_open=open_commitments,
        proposed_next_step=proposed_next_step,
    )
    longitudinal_context = {
        "schema": "relationship_longitudinal_context_v1",
        "prior_confirmed_facts": prior_facts,
        "current_confirmed_facts": current_facts,
        "unchanged_facts": unchanged,
        "corrected_facts": corrected,
        "new_facts": new_facts,
        "commitments_completed": completed_commitments,
        "commitments_open": open_commitments,
        "goals_refined": goals_refined,
        "unresolved_questions": unresolved_questions,
        "proposed_next_step": proposed_next_step,
        "evidence_references": evidence_references,
        "unsupported_inferences": unsupported,
    }
    ok, errors = validate_longitudinal_context(longitudinal_context)
    if not ok:
        raise ValueError(
            "Longitudinal context failed schema validation: " + "; ".join(errors)
        )
    return longitudinal_context


def _assert_unique_fact_ids(items: Sequence[Mapping[str, Any]], *, source: str) -> None:
    seen = set()
    for item in items:
        fact_id = str(item.get("fact_id") or "").strip()
        if not fact_id:
            raise ValueError(f"{source} contains missing fact_id")
        if fact_id in seen:
            raise ValueError(f"{source} contains duplicate fact_id: {fact_id}")
        seen.add(fact_id)


def _evidence_index(meeting_context: Mapping[str, Any]) -> Dict[str, List[str]]:
    evidence = dict(meeting_context.get("evidence") or {})
    spans = list(evidence.get("transcript_spans") or [])
    indexed: Dict[str, List[str]] = {}
    for span in spans:
        field = str(span.get("field") or "").strip()
        excerpt_id = str(span.get("excerpt_id") or "").strip()
        if not field or not excerpt_id:
            continue
        indexed.setdefault(field, [])
        if excerpt_id not in indexed[field]:
            indexed[field].append(excerpt_id)
    return indexed


def _parse_structured_claims(
    *,
    extraction: Mapping[str, Any],
    meeting_id: str,
    evidence_index: Mapping[str, List[str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, str], List[Dict[str, Any]]]:
    current_facts: List[Dict[str, Any]] = []
    unresolved_questions: List[Dict[str, Any]] = []
    commitment_statuses: Dict[str, str] = {}
    unsupported: List[Dict[str, Any]] = []

    statements: List[str] = []
    statements.extend(str(item) for item in (extraction.get("needs") or []) if item is not None)
    statements.extend(str(item) for item in (extraction.get("objections") or []) if item is not None)
    for statement in statements:
        match = _STRUCTURED_VALUE.match(statement.strip())
        if not match:
            continue
        key = match.group("key").strip()
        value_text = match.group("value").strip()
        refs = list(evidence_index.get(key) or [])
        if not refs:
            unsupported.append(
                {
                    "claim_id": key,
                    "reason": "missing_evidence_reference",
                }
            )
            continue
        if key.startswith("question."):
            unresolved_questions.append(
                {
                    "question_id": key,
                    "question": value_text,
                    "source_meeting_id": meeting_id,
                    "evidence_refs": refs,
                }
            )
            continue
        if key.startswith("commitment_status."):
            commitment_id = key[len("commitment_status.") :]
            status = value_text.lower()
            if status in {"completed", "open"}:
                commitment_statuses[commitment_id] = status
            else:
                unsupported.append(
                    {
                        "claim_id": key,
                        "reason": f"unsupported_commitment_status:{value_text}",
                    }
                )
            continue
        current_facts.append(
            {
                "fact_id": key,
                "category": key.split(".", 1)[0],
                "value": _parse_value(value_text),
                "source_meeting_id": meeting_id,
                "evidence_refs": refs,
            }
        )

    opportunity_signal = dict(extraction.get("opportunity_signal") or {})
    recommended_stage = opportunity_signal.get("recommended_stage")
    if recommended_stage is not None:
        key = "opportunity.recommended_stage"
        refs = list(evidence_index.get(key) or [])
        if refs:
            current_facts.append(
                {
                    "fact_id": key,
                    "category": "opportunity",
                    "value": recommended_stage,
                    "source_meeting_id": meeting_id,
                    "evidence_refs": refs,
                }
            )
        else:
            unsupported.append(
                {
                    "claim_id": key,
                    "reason": "missing_evidence_reference",
                }
            )
    return current_facts, unresolved_questions, commitment_statuses, unsupported


def _parse_commitments(
    *,
    extraction: Mapping[str, Any],
    meeting_id: str,
    evidence_index: Mapping[str, List[str]],
) -> List[Dict[str, Any]]:
    commitments: List[Dict[str, Any]] = []
    for raw in list(extraction.get("commitments") or []):
        item = dict(raw or {})
        owner = str(item.get("owner") or "").strip()
        action = str(item.get("action") or "").strip()
        if not owner or not action:
            continue
        commitment_id = _commitment_id(owner=owner, action=action)
        refs = list(evidence_index.get(commitment_id) or [])
        if not refs:
            continue
        commitments.append(
            {
                "commitment_id": commitment_id,
                "owner": owner,
                "action": action,
                "due_date": item.get("due_date"),
                "source_meeting_id": meeting_id,
                "evidence_refs": refs,
            }
        )
    return commitments


def _parse_next_step(
    *,
    extraction: Mapping[str, Any],
    meeting_id: str,
    evidence_index: Mapping[str, List[str]],
) -> Optional[Dict[str, Any]]:
    next_step = dict(extraction.get("next_step") or {})
    if not next_step:
        return None
    refs = list(evidence_index.get("next_step.proposed") or [])
    if not refs:
        return None
    action = str(next_step.get("action") or "").strip()
    if not action:
        return None
    return {
        "action": action,
        "owner": next_step.get("owner"),
        "target_date": next_step.get("target_date"),
        "source_meeting_id": meeting_id,
        "evidence_refs": refs,
    }


def _collect_evidence_references(
    *,
    current_facts: Sequence[Mapping[str, Any]],
    unresolved_questions: Sequence[Mapping[str, Any]],
    commitments_completed: Sequence[Mapping[str, Any]],
    commitments_open: Sequence[Mapping[str, Any]],
    proposed_next_step: Optional[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []
    for fact in current_facts:
        evidence.append(
            {
                "claim_id": str(fact["fact_id"]),
                "excerpt_ids": list(fact.get("evidence_refs") or []),
            }
        )
    for question in unresolved_questions:
        evidence.append(
            {
                "claim_id": str(question["question_id"]),
                "excerpt_ids": list(question.get("evidence_refs") or []),
            }
        )
    for commitment in commitments_completed:
        evidence.append(
            {
                "claim_id": str(commitment["commitment_id"]),
                "excerpt_ids": list(commitment.get("current_evidence_refs") or []),
            }
        )
    for commitment in commitments_open:
        evidence.append(
            {
                "claim_id": str(commitment["commitment_id"]),
                "excerpt_ids": list(
                    commitment.get("current_evidence_refs")
                    or commitment.get("evidence_refs")
                    or []
                ),
            }
        )
    if proposed_next_step is not None:
        evidence.append(
            {
                "claim_id": "next_step.proposed",
                "excerpt_ids": list(proposed_next_step.get("evidence_refs") or []),
            }
        )
    return evidence


def _goal_refinement_from_fact(fact: Mapping[str, Any], *, kind: str) -> Dict[str, Any]:
    return {
        "fact_id": str(fact["fact_id"]),
        "kind": kind,
        "new_value": deepcopy(fact.get("value")),
        "current_meeting_id": fact.get("source_meeting_id"),
        "current_evidence_refs": list(fact.get("evidence_refs") or []),
    }


def _commitment_id(*, owner: str, action: str) -> str:
    owner_slug = _slug(owner)
    action_slug = _slug(action)
    return f"commitment.{owner_slug}.{action_slug}"


def _slug(value: str) -> str:
    lowered = value.strip().lower()
    compact = _NON_ALNUM.sub("_", lowered).strip("_")
    return compact or "unknown"


def _parse_value(value_text: str) -> Any:
    text = value_text.strip()
    if not text:
        return ""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _canonical_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
