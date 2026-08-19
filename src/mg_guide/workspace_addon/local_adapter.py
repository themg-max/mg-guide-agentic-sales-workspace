"""In-process Workspace add-on adapter over JudgeSurfaceApp.

Used for deterministic judge UX proof without clasp deploy or live CRM.
"""

from __future__ import annotations

import json
from io import BytesIO
from typing import Any, Dict, List, Mapping, Optional, Tuple

from mg_guide.judge_surface.app import JudgeSurfaceApp

from .cardservice_projection import (
    ERROR_AUTH,
    ERROR_BACKEND,
    ERROR_INVALID,
    ERROR_SCENARIO_BLOCKED,
    project_cardservice_home,
    project_cardservice_result,
    project_error_card,
)


class WorkspaceAddonLocalAdapter:
    """Thin routing adapter: scenario button → judge endpoint → card model."""

    def __init__(self, app: Optional[JudgeSurfaceApp] = None) -> None:
        self.app = app or JudgeSurfaceApp()

    def home(self) -> Dict[str, Any]:
        return project_cardservice_home()

    def run_scenario(self, scenario: str) -> Dict[str, Any]:
        code, body = self._post_demo(scenario)
        if code == 400 and body.get("error") == "invalid_scenario":
            return project_error_card(
                ERROR_SCENARIO_BLOCKED,
                "Scenario is not authorized for the judge path.",
            )
        if code == 401 or body.get("code") == "AUTH_ERROR":
            return project_error_card(ERROR_AUTH, "Authentication failed.")
        if code == 503 or body.get("error") == "judge_mode_rejected":
            return project_error_card(
                ERROR_BACKEND, "Judge backend rejected the request mode."
            )
        if code >= 500:
            return project_error_card(ERROR_BACKEND, "Backend unavailable.")
        if code != 200:
            return project_error_card(
                ERROR_INVALID, f"Unexpected status {code}."
            )
        return project_cardservice_result(body)

    def _post_demo(self, scenario: str) -> Tuple[int, Dict[str, Any]]:
        payload = json.dumps({"scenario": scenario}).encode("utf-8")
        environ: Dict[str, Any] = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/demo/meeting-follow-up",
            "CONTENT_LENGTH": str(len(payload)),
            "CONTENT_TYPE": "application/json",
            "wsgi.input": BytesIO(payload),
            "wsgi.errors": BytesIO(),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8080",
            # Local adapter does not inject Bearer tokens; auth mode stays off
            # unless the process env enables identity_token (which would 401).
            "HTTP_X_MG_GUIDE_DEMO_AUTH": "local-demo",
        }
        status_info: List[str] = []

        def start_response(status: str, _headers: List[Tuple[str, str]]):
            status_info.append(status)
            return lambda _x: None

        raw = b"".join(self.app(environ, start_response))
        code = int(status_info[0].split(" ", 1)[0])
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return code, {"error": "invalid_json"}
        if not isinstance(data, dict):
            return code, {"error": "invalid_json_object"}
        return code, data


def flatten_visible_text(card: Mapping[str, Any]) -> str:
    """Concatenate judge-visible widget text for acceptance assertions."""
    parts: List[str] = []
    header = card.get("header") if isinstance(card.get("header"), Mapping) else {}
    parts.append(str(header.get("title") or ""))
    parts.append(str(header.get("subtitle") or ""))
    for section in card.get("sections") or []:
        if not isinstance(section, Mapping):
            continue
        parts.append(str(section.get("header") or ""))
        for widget in section.get("widgets") or []:
            if not isinstance(widget, Mapping):
                continue
            for key in ("text", "content", "top_label"):
                if widget.get(key) is not None:
                    parts.append(str(widget.get(key)))
    err = card.get("error")
    if isinstance(err, Mapping):
        parts.append(str(err.get("code") or ""))
        parts.append(str(err.get("message") or ""))
    return "\n".join(parts)
