"""Public, bounded, *stateless* WSGI adapter for the WebMCP Challenge slice.

Contract (see competition/webmcp/WEBMCP_ARCHITECTURE.md):

  GET  /health                      -- liveness / provenance
  POST /webmcp/meeting-follow-up    -- {"scenario": "SUCCESS"|"AMBIGUOUS_CONTACT"}

This route is intentionally UNAUTHENTICATED and public: it is a synthetic,
fixture-only, read-mostly demo surface with a fixed two-value scenario
enum. It never calls HighLevel, never mutates CRM, never sends email, and
never accepts raw CRM identifiers, transcripts, or live-mode selectors. It
reuses the existing meeting_follow_up_v1 WorkflowRunner and the existing
judge_surface projection helpers (map_packet_to_card, project_demo_payload)
without modifying either.

STATELESSNESS
-------------
This adapter holds **no server-side session state**. Every POST returns the
full safe projected payload (including the bounded draft projection when
READY). The browser page holds ``currentWebMCPState`` in JavaScript memory;
``get_current_follow_up_state`` and ``get_follow_up_draft`` are pure
client-side WebMCP tools that read that browser state. No Firestore, no
cookies, no session database, no sticky routing, no min-instances
requirement.

CORS
----
Production allowlist is explicit (see ``WEBMCP_CORS_ORIGINS``). Local/dev
mode (``WEBMCP_CORS_MODE=local``) additionally permits localhost origins.
"""

from __future__ import annotations

import json
import logging
import os
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

# Production allowlist for the A.I. Rolodex host surface. Additional origins
# may be supplied via WEBMCP_CORS_ORIGINS (comma-separated) without code change.
DEFAULT_PRODUCTION_ORIGINS = (
    "https://ai-rolodex-landing-831270426395.us-east4.run.app",
)

LOCAL_ORIGIN_PREFIXES = (
    "http://localhost:",
    "http://127.0.0.1:",
)


class _JSONError(RuntimeError):
    def __init__(self, status: str, body: JSONType) -> None:
        super().__init__(status)
        self.status = status
        self.body = body


class WebMCPSurfaceApp:
    """WSGI application for the public WebMCP competition adapter.

    Stateless: no ``_last_state``, no locks, no server session.
    """

    def __init__(self, runner: Optional[WorkflowRunner] = None) -> None:
        # A fresh isolated registry per request (via factory) avoids
        # duplicate-run-id rejection across repeated demo invocations of the
        # same fixture, without retaining any cross-request state.
        self._runner_factory = (lambda: runner) if runner is not None else WorkflowRunner
        self._service_name = "mg-guide-webmcp-competition"
        self._version = "0.2.0"
        self._commit = os.environ.get("GIT_COMMIT", "unknown")

    def __call__(
        self, environ: WSGIEnv, start_response: StartResponse
    ) -> Iterable[bytes]:
        started_at = time.monotonic()
        request_id = uuid4().hex
        origin = str(environ.get("HTTP_ORIGIN") or "")
        try:
            if environ.get("REQUEST_METHOD") == "OPTIONS":
                return _send_preflight(start_response, origin)
            response = self._handle(environ)
        except _JSONError as exc:
            self._log(environ, request_id, started_at, exc.status, exc.body)
            return _send(start_response, exc.status, exc.body, origin=origin)
        self._log(environ, request_id, started_at, "200 OK", response)
        return _send(start_response, "200 OK", response, origin=origin)

    def _handle(self, environ: WSGIEnv) -> JSONType:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        if method == "GET" and path in ("/health", "/healthz"):
            return self._health()
        if method == "POST" and path == "/webmcp/meeting-follow-up":
            return self._process(environ)
        raise _JSONError("404 Not Found", {"error": "not_found", "path": path})

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
            "server_session_state_required": False,
            "webmcp_browser_state": True,
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
        draft = ux.get("follow_up_draft") or {}

        return {
            "status": "PROCESSED",
            "scenario": selector,
            "workflow_status": result.final_state,
            "ux_state": ux.get("ux_state"),
            "meeting_summary": ux.get("summary"),
            "relationship_status": (ux.get("relationship_context") or {}).get(
                "resolution_status"
            ),
            "salesperson_next_step": ux.get("salesperson_next_step"),
            "crm_note_status": (ux.get("crm_note_status") or {}).get("state"),
            "follow_up_draft_status": draft.get("status"),
            "follow_up_draft": _safe_draft_projection(draft),
            "external_effects": result.external_effects,
            "cloud_mutation": "NONE",
        }

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


def _safe_draft_projection(draft: JSONType) -> JSONType:
    status = draft.get("status")
    if status != "READY":
        return {
            "status": "NOT_AVAILABLE",
            "reason": "RELATIONSHIP_REVIEW_REQUIRED",
            "requires_human_send": True,
        }
    body_text = draft.get("body_text")
    return {
        "status": "READY",
        "recipient_name": draft.get("recipient_name"),
        "subject": draft.get("subject"),
        "body_preview": _preview(body_text),
        "requires_human_send": True,
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


def _allowed_origins() -> List[str]:
    extra = os.environ.get("WEBMCP_CORS_ORIGINS", "").strip()
    origins = list(DEFAULT_PRODUCTION_ORIGINS)
    if extra:
        origins.extend(o.strip() for o in extra.split(",") if o.strip())
    return origins


def _cors_mode() -> str:
    return (os.environ.get("WEBMCP_CORS_MODE") or "production").strip().lower()


def _origin_allowed(origin: str) -> bool:
    if not origin:
        return False
    if origin in _allowed_origins():
        return True
    if _cors_mode() == "local":
        return any(origin.startswith(p) for p in LOCAL_ORIGIN_PREFIXES)
    return False


def _cors_headers(origin: str) -> List[Tuple[str, str]]:
    if not _origin_allowed(origin):
        return []
    return [
        ("Access-Control-Allow-Origin", origin),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type"),
        ("Vary", "Origin"),
    ]


def _send_preflight(start_response: StartResponse, origin: str) -> Iterable[bytes]:
    headers = _cors_headers(origin)
    headers.append(("Content-Length", "0"))
    if _origin_allowed(origin):
        start_response("204 No Content", headers)
    else:
        start_response("403 Forbidden", [("Content-Length", "0")])
    return [b""]


def _send(
    start_response: StartResponse,
    status: str,
    body: JSONType,
    *,
    origin: str = "",
) -> Iterable[bytes]:
    payload = json.dumps(body, sort_keys=True).encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(payload))),
    ]
    headers.extend(_cors_headers(origin))
    start_response(status, headers)
    return [payload]
