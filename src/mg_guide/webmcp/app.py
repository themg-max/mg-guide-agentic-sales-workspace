"""Public, bounded WSGI adapter for the WebMCP Challenge competition slice.

Contract (see competition/webmcp/WEBMCP_ARCHITECTURE.md):

  GET  /health                      -- liveness / provenance
  POST /webmcp/meeting-follow-up    -- {"scenario": "SUCCESS"|"AMBIGUOUS_CONTACT"}
  GET  /webmcp/state                -- last processed state for this process
  GET  /webmcp/follow-up-draft      -- deterministic draft for last processed run

This route is intentionally UNAUTHENTICATED and public: it is a synthetic,
fixture-only, read-mostly demo surface with a fixed two-value scenario
enum. It never calls HighLevel, never mutates CRM, never sends email, and
never accepts raw CRM identifiers, transcripts, or live-mode selectors. It
reuses the existing meeting_follow_up_v1 WorkflowRunner and the existing
judge_surface projection helpers (map_packet_to_card, project_demo_payload)
without modifying either.

State is held in-process only (no Firestore, no external persistence) and is
reset on every new process. This mirrors the judge_surface stub posture and
keeps the WebMCP demo bounded to a single Cloud Run instance / min-instances=1
deployment for demo determinism.
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from uuid import uuid4

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card
from orchestration.runner import WorkflowRunner

from mg_guide.judge_surface.demo_stages import project_demo_payload

from .scenarios import WEBMCP_SCENARIOS, webmcp_scenario_names

JSONType = Dict[str, Any]
StartResponse = Callable[[str, List[Tuple[str, str]]], None]
WSGIEnv = Dict[str, Any]
LOGGER = logging.getLogger("mg_guide.webmcp")
LOGGER.setLevel(logging.INFO)

NOT_PROCESSED = "NOT_PROCESSED"


class _JSONError(RuntimeError):
    def __init__(self, status: str, body: JSONType) -> None:
        super().__init__(status)
        self.status = status
        self.body = body


class WebMCPSurfaceApp:
    """WSGI application for the public WebMCP competition adapter."""

    def __init__(self, runner: Optional[WorkflowRunner] = None) -> None:
        # A fresh isolated registry per process avoids duplicate-run-id
        # rejection across repeated demo invocations of the same fixture.
        self._runner_factory = (lambda: runner) if runner is not None else WorkflowRunner
        self._service_name = "mg-guide-webmcp-competition"
        self._version = "0.1.0"
        self._commit = os.environ.get("GIT_COMMIT", "unknown")
        self._lock = threading.Lock()
        self._last_state: Optional[JSONType] = None

    def __call__(
        self, environ: WSGIEnv, start_response: StartResponse
    ) -> Iterable[bytes]:
        started_at = time.monotonic()
        request_id = uuid4().hex
        try:
            response = self._handle(environ)
        except _JSONError as exc:
            self._log(environ, request_id, started_at, exc.status, exc.body)
            return _send(start_response, exc.status, exc.body, cors=True)
        self._log(environ, request_id, started_at, "200 OK", response)
        return _send(start_response, "200 OK", response, cors=True)

    def _handle(self, environ: WSGIEnv) -> JSONType:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        if method == "OPTIONS":
            return {}
        if method == "GET" and path in ("/health", "/healthz"):
            return self._health()
        if method == "POST" and path == "/webmcp/meeting-follow-up":
            return self._process(environ)
        if method == "GET" and path == "/webmcp/state":
            return self._state()
        if method == "GET" and path == "/webmcp/follow-up-draft":
            return self._draft()
        raise _JSONError("404 Not Found", {"error": "not_found", "path": path})

    # -- routes ---------------------------------------------------------

    def _health(self) -> JSONType:
        return {
            "status": "ok",
            "service": self._service_name,
            "version": self._version,
            "commit": self._commit,
            "scenario_names": webmcp_scenario_names(),
            "current_transcript_source": "synthetic_fixture",
            "real_customer_data": False,
            "live_ghl_calls": 0,
            "live_crm_mutations": 0,
            "real_emails_sent": 0,
        }

    def _process(self, environ: WSGIEnv) -> JSONType:
        body = _read_json_body(environ)
        _reject_unexpected_fields(body)
        selector = body.get("scenario")
        if selector not in WEBMCP_SCENARIOS:
            raise _JSONError(
                "400 Bad Request",
                {
                    "error": "invalid_scenario",
                    "scenario": selector,
                    "allowed": webmcp_scenario_names(),
                },
            )

        sidecar_path = WEBMCP_SCENARIOS[selector]
        # A fresh run_id per invocation lets the same fixture replay across
        # repeated demo/judge/agent invocations without duplicate rejection.
        run_id_override = f"webmcp-{selector.lower()}-{uuid4().hex[:12]}"
        runner = self._runner_factory()
        result = runner.run_fixture(sidecar_path, run_id_override=run_id_override)

        if result.rejected_duplicate or not result.validation_ok:
            raise _JSONError(
                "500 Internal Server Error",
                {
                    "error": "run_failed",
                    "scenario": selector,
                    "detail": result.error,
                    "final_state": result.final_state,
                },
            )

        packet = result.packet
        card = map_packet_to_card(packet)
        demo_payload = project_demo_payload(
            packet, card, workflow_status=result.final_state
        )
        ux = demo_payload["ux_experience"]

        state_snapshot = {
            "scenario": selector,
            "workflow_status": result.final_state,
            "ux_state": ux.get("ux_state"),
            "meeting_summary": ux.get("summary"),
            "relationship_status": (ux.get("relationship_context") or {}).get(
                "resolution_status"
            ),
            "salesperson_next_step": ux.get("salesperson_next_step"),
            "crm_note_status": (ux.get("crm_note_status") or {}).get("state"),
            "follow_up_draft_status": (ux.get("follow_up_draft") or {}).get("status"),
            "follow_up_draft": ux.get("follow_up_draft"),
            "external_effects": result.external_effects,
            "cloud_mutation": "NONE",
        }
        with self._lock:
            self._last_state = state_snapshot

        # Public tool-facing response: narrow field set only, per boundary.
        return {
            "workflow_status": state_snapshot["workflow_status"],
            "ux_state": state_snapshot["ux_state"],
            "meeting_summary": state_snapshot["meeting_summary"],
            "relationship_status": state_snapshot["relationship_status"],
            "salesperson_next_step": state_snapshot["salesperson_next_step"],
            "crm_note_status": state_snapshot["crm_note_status"],
            "follow_up_draft_status": state_snapshot["follow_up_draft_status"],
        }

    def _state(self) -> JSONType:
        with self._lock:
            snapshot = self._last_state
        if snapshot is None:
            return {
                "status": NOT_PROCESSED,
                "message": "No meeting has been processed yet in this session.",
            }
        return {
            "status": "PROCESSED",
            "workflow_status": snapshot["workflow_status"],
            "ux_state": snapshot["ux_state"],
            "meeting_summary": snapshot["meeting_summary"],
            "relationship_status": snapshot["relationship_status"],
            "salesperson_next_step": snapshot["salesperson_next_step"],
            "crm_note_status": snapshot["crm_note_status"],
            "follow_up_draft_status": snapshot["follow_up_draft_status"],
            "cloud_mutation": "NONE",
        }

    def _draft(self) -> JSONType:
        with self._lock:
            snapshot = self._last_state
        if snapshot is None:
            return {"status": NOT_PROCESSED}
        draft = snapshot.get("follow_up_draft") or {}
        if draft.get("status") != "READY":
            return {
                "status": "NOT_AVAILABLE",
                "reason": "RELATIONSHIP_REVIEW_REQUIRED",
            }
        return {
            "status": "READY",
            "recipient_name": draft.get("recipient_name"),
            "subject": draft.get("subject"),
            "body_preview": _preview(draft.get("body_text")),
            "requires_human_send": True,
        }

    # -- helpers ----------------------------------------------------------

    @staticmethod
    def _log(
        environ: WSGIEnv,
        request_id: str,
        started_at: float,
        status: str,
        body: JSONType,
    ) -> None:
        record = {
            "request_id": request_id,
            "path": environ.get("PATH_INFO"),
            "method": environ.get("REQUEST_METHOD"),
            "http_status": status.split(" ", 1)[0],
            "latency_ms": round((time.monotonic() - started_at) * 1000, 2),
            "external_effects": 0,
        }
        LOGGER.info(json.dumps(record, sort_keys=True, separators=(",", ":")))


_ALLOWED_FIELDS = {"scenario"}
_DENYLIST_FIELDS = {
    "live",
    "crm_write",
    "send_email",
    "provider",
    "contact_id",
    "location_id",
    "url",
    "credentials",
    "instructions",
    "transcript",
}


def _reject_unexpected_fields(body: JSONType) -> None:
    keys = set(body.keys())
    denied = keys & _DENYLIST_FIELDS
    if denied:
        raise _JSONError(
            "400 Bad Request",
            {"error": "authority_field_rejected", "fields": sorted(denied)},
        )
    unexpected = keys - _ALLOWED_FIELDS
    if unexpected:
        raise _JSONError(
            "400 Bad Request",
            {"error": "unexpected_field", "fields": sorted(unexpected)},
        )


def _preview(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    flat = " ".join(str(text).split())
    return flat[:280]


def _read_json_body(environ: WSGIEnv) -> JSONType:
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except (TypeError, ValueError):
        length = 0
    if length <= 0:
        return {}
    raw = environ["wsgi.input"].read(length)
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise _JSONError(
            "400 Bad Request", {"error": "invalid_json", "detail": str(exc)}
        ) from exc
    if not isinstance(parsed, dict):
        raise _JSONError("400 Bad Request", {"error": "invalid_body"})
    return parsed


def _send(
    start_response: StartResponse,
    status: str,
    body: JSONType,
    *,
    cors: bool = False,
) -> Iterable[bytes]:
    payload = json.dumps(body, sort_keys=True).encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(payload))),
    ]
    if cors:
        headers.append(("Access-Control-Allow-Origin", "*"))
        headers.append(("Access-Control-Allow-Methods", "GET, POST, OPTIONS"))
        headers.append(("Access-Control-Allow-Headers", "Content-Type"))
    start_response(status, headers)
    return [payload]
