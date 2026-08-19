"""Minimal judge-safe WSGI application for meeting_follow_up_v1.

Implements:
  GET /health    - Cloud Run liveness/provenance response
  GET /healthz   - local/container compatibility alias for /health
  POST /demo/meeting-follow-up - run a fixed synthetic scenario selector

All responses are JSON.  The adapter never performs cloud mutations, CRM
writes, Firestore writes, or live Gemini calls.
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple
from uuid import uuid4

from mg_guide.meeting_follow_up_card.mapper import map_packet_to_card
from mg_guide.meeting_follow_up_card.render_html import render_card_html
from mg_guide.meeting_follow_up_card.render_text import render_card_text
from orchestration.runner import WorkflowRunner

from .demo_stages import project_demo_payload
from .render_demo_stages import render_demo_stages_html, render_demo_stages_text
from .scenarios import (
    AUTHORIZED_JUDGE_MODE,
    SCENARIO_CATALOG,
    judge_mode,
    scenario_catalog_hash,
    scenario_names,
)

from mg_guide.workspace_addon.auth_contract import (
    AuthError,
    AuthMode,
    auth_mode_from_env,
    validate_authorization_header,
)


# pylint: disable=invalid-name
JSONType = Dict[str, Any]
StartResponse = Callable[[str, List[Tuple[str, str]]], None]
WSGIEnv = Dict[str, Any]
LOGGER = logging.getLogger("mg_guide.judge_surface")
LOGGER.setLevel(logging.INFO)


class _JSONError(RuntimeError):
    def __init__(self, status: str, body: JSONType) -> None:
        super().__init__(status)
        self.status = status
        self.body = body


class JudgeSurfaceApp:
    """WSGI application for the judge-safe demo surface."""

    def __init__(self, runner: Optional[WorkflowRunner] = None) -> None:
        # A supplied runner is retained only for explicit test/integration use.
        # Normal judge requests receive an isolated registry so static synthetic
        # fixture IDs can be replayed without changing runner duplicate policy.
        self._runner = runner
        self._service_name = "mg-guide-agentic-sales-workspace-judge"
        self._version = "0.1.0"
        self._commit = os.environ.get("GIT_COMMIT", "unknown")

    def __call__(
        self, environ: WSGIEnv, start_response: StartResponse
    ) -> Iterable[bytes]:
        started_at = time.monotonic()
        request_id = uuid4().hex
        try:
            response = self._handle(environ)
        except _JSONError as exc:
            self._log_judge_request(
                environ, request_id, started_at, exc.status, exc.body
            )
            return _send(start_response, exc.status, exc.body)
        self._log_judge_request(environ, request_id, started_at, "200 OK", response)
        return _send(start_response, "200 OK", response)

    def _handle(self, environ: WSGIEnv) -> JSONType:
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        if method == "GET" and path in ("/health", "/healthz"):
            return self._health()
        if method == "POST" and path == "/demo/meeting-follow-up":
            self._enforce_addon_auth(environ)
            return self._demo(environ)
        raise _JSONError("404 Not Found", {"error": "not_found", "path": path})

    @staticmethod
    def _enforce_addon_auth(environ: WSGIEnv) -> None:
        try:
            mode = auth_mode_from_env()
        except AuthError as exc:
            raise _JSONError("401 Unauthorized", exc.as_body()) from exc
        if mode is AuthMode.LOCAL_DEMO and os.environ.get("K_SERVICE"):
            raise _JSONError(
                "503 Service Unavailable",
                {
                    "error": "addon_auth_mode_rejected",
                    "code": "LOCAL_DEMO_PUBLIC_INGRESS_FORBIDDEN",
                },
            )
        headers = {
            "Authorization": str(environ.get("HTTP_AUTHORIZATION") or ""),
            "X-MG-Guide-Demo-Auth": str(
                environ.get("HTTP_X_MG_GUIDE_DEMO_AUTH") or ""
            ),
        }
        try:
            validate_authorization_header(headers)
        except AuthError as exc:
            raise _JSONError("401 Unauthorized", exc.as_body()) from exc

    def _health(self) -> JSONType:
        mode = self._require_judge_mode()
        return {
            "status": "ok",
            "service": self._service_name,
            "version": self._version,
            "commit": self._commit,
            "scenario_catalog_hash": scenario_catalog_hash(),
            "judge_mode": mode,
            "scenario_names": scenario_names(),
        }

    def _demo(self, environ: WSGIEnv) -> JSONType:
        self._require_judge_mode()
        body = _read_json_body(environ)
        selector = body.get("scenario")
        if selector not in SCENARIO_CATALOG:
            raise _JSONError(
                "400 Bad Request",
                {
                    "error": "invalid_scenario",
                    "scenario": selector,
                    "allowed": scenario_names(),
                },
            )

        sidecar_path = SCENARIO_CATALOG[selector]
        runner = self._runner or WorkflowRunner()
        result = runner.run_fixture(sidecar_path)

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
        view_format = str(body.get("view", "json")).lower()

        proposal = self._follow_up_proposal(packet)
        policy_decision = self._policy_decision(packet)
        demo_payload = project_demo_payload(
            packet, card, workflow_status=result.final_state
        )

        return {
            "scenario": selector,
            "workflow_status": result.final_state,
            "resolution_outcome": self._resolution_outcome(packet),
            "follow_up_proposal": proposal,
            "policy_decision": policy_decision,
            "card": card,
            "card_view": self._card_view(
                card,
                view_format,
                demo_stages=demo_payload["demo_stages"],
                demo_truth=demo_payload["demo_truth"],
                ux_experience=demo_payload["ux_experience"],
            ),
            "audit_summary": self._audit_summary(packet),
            "external_effects": result.external_effects,
            "cloud_mutation": "NONE",
            "demo_stages": demo_payload["demo_stages"],
            "demo_truth": demo_payload["demo_truth"],
            "ux_experience": demo_payload["ux_experience"],
        }

    @staticmethod
    def _log_judge_request(
        environ: WSGIEnv,
        request_id: str,
        started_at: float,
        status: str,
        body: JSONType,
    ) -> None:
        if not (
            environ.get("REQUEST_METHOD") == "POST"
            and environ.get("PATH_INFO") == "/demo/meeting-follow-up"
        ):
            return

        scenario = body.get("scenario")
        if scenario not in SCENARIO_CATALOG:
            scenario = "INVALID_OR_UNAVAILABLE"
        ux = body.get("ux_experience") or {}
        external_effects = body.get("external_effects")
        if not isinstance(external_effects, int):
            external_effects = 0
        try:
            auth_mode = auth_mode_from_env().value
        except AuthError:
            auth_mode = "invalid"
        gemini_mode = os.environ.get("MEETING_CONTEXT_GEMINI_MODE", "unset")
        if gemini_mode not in {"stub", "live"}:
            gemini_mode = "invalid"

        record = {
            "request_id": request_id,
            "scenario": scenario,
            "auth_mode": auth_mode,
            "workflow_status": body.get("workflow_status", "not_run"),
            "ux_state": ux.get("ux_state", "not_available"),
            "http_status": int(status.split(" ", 1)[0]),
            "latency_ms": round((time.monotonic() - started_at) * 1000, 2),
            "external_effects": external_effects,
            "revision": os.environ.get("K_REVISION", "unknown"),
            "gemini_mode": gemini_mode,
            "error_code": body.get("code") or body.get("error") or "NONE",
            "audience_configured": bool(
                os.environ.get("JUDGE_ADDON_OIDC_AUDIENCE", "").strip()
            ),
            "token_logged": False,
        }
        LOGGER.info(json.dumps(record, sort_keys=True, separators=(",", ":")))

    @staticmethod
    def _resolution_outcome(packet: JSONType) -> JSONType:
        crm = packet.get("crm_resolution") or {}
        result = {
            "status": crm.get("status"),
            "match_basis": crm.get("match_basis"),
            "candidate_count": crm.get("candidate_count"),
            "current_stage": crm.get("current_stage"),
        }
        # Keep the public judge-facing payload minimal and fail-closed.  The
        # demo surface does not need raw CRM identifiers.
        return result

    @staticmethod
    def _require_judge_mode() -> str:
        try:
            return judge_mode()
        except ValueError as exc:
            raise _JSONError(
                "503 Service Unavailable",
                {
                    "error": "judge_mode_rejected",
                    "authorized_mode": AUTHORIZED_JUDGE_MODE,
                    "detail": str(exc),
                    "meeting_context_gemini_mode": os.environ.get(
                        "MEETING_CONTEXT_GEMINI_MODE"
                    ),
                },
            ) from exc

    @staticmethod
    def _follow_up_proposal(packet: JSONType) -> JSONType:
        extraction = packet.get("extraction") or {}
        brief = packet.get("brief") or {}
        return {
            "summary": extraction.get("summary"),
            "needs": extraction.get("needs") or [],
            "objections": extraction.get("objections") or [],
            "next_step": extraction.get("next_step"),
            "headline": brief.get("headline"),
            "next_action": brief.get("next_action"),
            "salesperson_attention_required": brief.get("salesperson_attention_required"),
        }

    @staticmethod
    def _policy_decision(packet: JSONType) -> JSONType:
        policy = packet.get("policy") or {}
        return {
            "note_write": policy.get("note_write"),
            "stage_write": policy.get("stage_write"),
            "reason_codes": policy.get("reason_codes") or [],
        }

    @staticmethod
    def _audit_summary(packet: JSONType) -> JSONType:
        run = packet.get("run") or {}
        audit = packet.get("audit") or {}
        return {
            "run_id": run.get("run_id"),
            "workflow": run.get("workflow"),
            "created_at": run.get("created_at"),
            "started_at": audit.get("started_at"),
            "completed_at": audit.get("completed_at"),
            "final_disposition": audit.get("final_disposition"),
            "agents_used": audit.get("agents_used") or [],
            "tools_used": audit.get("tools_used") or [],
            "warnings": audit.get("warnings") or [],
        }

    @staticmethod
    def _card_view(
        card: JSONType,
        view_format: str,
        *,
        demo_stages: Optional[List[JSONType]] = None,
        demo_truth: Optional[JSONType] = None,
        ux_experience: Optional[JSONType] = None,
    ) -> Optional[str]:
        if view_format == "html":
            return render_card_html(card)
        if view_format == "text":
            return render_card_text(card)
        if view_format == "stages_html":
            return render_demo_stages_html(
                demo_stages or [],
                demo_truth or {},
                ux_experience=ux_experience,
            )
        if view_format == "stages_text":
            return render_demo_stages_text(
                demo_stages or [],
                demo_truth or {},
                ux_experience=ux_experience,
            )
        return None


def _read_json_body(environ: WSGIEnv) -> JSONType:
    try:
        length = int(environ.get("CONTENT_LENGTH", "0") or "0")
    except ValueError:
        length = 0
    if length <= 0:
        raise _JSONError("400 Bad Request", {"error": "missing_body"})
    raw = environ["wsgi.input"].read(length)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise _JSONError(
            "400 Bad Request", {"error": "invalid_json", "detail": str(exc)}
        )
    if not isinstance(data, dict):
        raise _JSONError("400 Bad Request", {"error": "invalid_json_object"})
    return data


def _send(
    start_response: StartResponse, status: str, body: JSONType
) -> Iterable[bytes]:
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(payload))),
    ]
    start_response(status, headers)
    return [payload]


def application(environ: WSGIEnv, start_response: StartResponse) -> Iterable[bytes]:
    """WSGI entry point used by container runtimes and test clients."""
    return JudgeSurfaceApp()(environ, start_response)
