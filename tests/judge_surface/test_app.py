"""Tests for the judge-safe HTTP adapter."""

from __future__ import annotations

import json
from io import BytesIO
from typing import Any, Dict, List, Tuple

import pytest

from mg_guide.judge_surface.app import JudgeSurfaceApp
from mg_guide.judge_surface.scenarios import scenario_names


class _TestClient:
    """Minimal WSGI test client."""

    def __init__(self, app) -> None:
        self.app = app

    def request(
        self,
        method: str,
        path: str,
        body: Dict[str, Any] | None = None,
    ) -> Tuple[int, Dict[str, Any]]:
        payload = b""
        if body is not None:
            payload = json.dumps(body).encode("utf-8")

        environ: Dict[str, Any] = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "CONTENT_LENGTH": str(len(payload)),
            "CONTENT_TYPE": "application/json",
            "wsgi.input": BytesIO(payload),
            "wsgi.errors": BytesIO(),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8080",
        }

        status_info: List[str] = []
        headers_info: List[Tuple[str, str]] = []

        def start_response(status, headers):
            status_info.append(status)
            headers_info.extend(headers)
            return lambda x: None

        response_body = b"".join(self.app(environ, start_response))
        code = int(status_info[0].split(" ", 1)[0])
        data = json.loads(response_body.decode("utf-8"))
        return code, data


@pytest.fixture
def client() -> _TestClient:
    return _TestClient(JudgeSurfaceApp())


def test_health_returns_ok(client: _TestClient) -> None:
    code, data = client.request("GET", "/health")
    assert code == 200
    assert data["status"] == "ok"
    assert data["service"] == "mg-guide-agentic-sales-workspace-judge"
    assert data["judge_mode"] == "stub"
    assert "SUCCESS" in data["scenario_names"]
    assert len(data["scenario_catalog_hash"]) == 64


def test_health_rejects_non_stub_mode(monkeypatch) -> None:
    monkeypatch.setenv("MEETING_CONTEXT_GEMINI_MODE", "live")
    client = _TestClient(JudgeSurfaceApp())
    code, data = client.request("GET", "/health")
    assert code == 503
    assert data["error"] == "judge_mode_rejected"
    assert data["authorized_mode"] == "stub"


def test_healthz_returns_ok(client: _TestClient) -> None:
    code, data = client.request("GET", "/healthz")
    assert code == 200
    assert data["status"] == "ok"
    assert data["service"] == "mg-guide-agentic-sales-workspace-judge"
    assert data["judge_mode"] == "stub"
    assert "SUCCESS" in data["scenario_names"]
    assert len(data["scenario_catalog_hash"]) == 64


def test_healthz_rejects_non_stub_mode(monkeypatch) -> None:
    monkeypatch.setenv("MEETING_CONTEXT_GEMINI_MODE", "live")
    client = _TestClient(JudgeSurfaceApp())
    code, data = client.request("GET", "/healthz")
    assert code == 503
    assert data["error"] == "judge_mode_rejected"
    assert data["authorized_mode"] == "stub"


def test_unknown_route_returns_404(client: _TestClient) -> None:
    code, data = client.request("GET", "/unknown")
    assert code == 404
    assert data["error"] == "not_found"


def test_demo_success_scenario(client: _TestClient) -> None:
    code, data = client.request("POST", "/demo/meeting-follow-up", {"scenario": "SUCCESS"})
    assert code == 200
    assert data["scenario"] == "SUCCESS"
    assert data["workflow_status"] == "completed"
    assert data["external_effects"] == 0
    assert data["cloud_mutation"] == "NONE"
    assert data["resolution_outcome"]["status"] == "matched"
    assert data["policy_decision"]["note_write"] == "allowed"
    assert data["policy_decision"]["stage_write"] == "allowed"
    assert data["card"]["card_state"] == "completed"
    assert data["card"]["controls"]["mutation_controls_enabled"] is False


def test_demo_stage_change_denied(client: _TestClient) -> None:
    code, data = client.request(
        "POST", "/demo/meeting-follow-up", {"scenario": "STAGE_CHANGE_DENIED"}
    )
    assert code == 200
    assert data["workflow_status"] == "completed_with_review"
    assert data["policy_decision"]["note_write"] == "allowed"
    assert data["policy_decision"]["stage_write"] == "blocked"
    assert "STAGE_TRANSITION_NOT_ALLOWED" in data["policy_decision"]["reason_codes"]
    assert data["card"]["card_state"] == "completed_with_review"
    assert data["external_effects"] == 0


def test_demo_ambiguous_contact(client: _TestClient) -> None:
    code, data = client.request(
        "POST", "/demo/meeting-follow-up", {"scenario": "AMBIGUOUS_CONTACT"}
    )
    assert code == 200
    assert data["workflow_status"] == "blocked"
    assert data["resolution_outcome"]["status"] == "ambiguous"
    assert "AMBIGUOUS_CONTACT" in data["policy_decision"]["reason_codes"]
    assert data["card"]["card_state"] == "blocked"
    assert data["external_effects"] == 0


def test_demo_invalid_scenario_returns_400(client: _TestClient) -> None:
    code, data = client.request(
        "POST", "/demo/meeting-follow-up", {"scenario": "ATTACK"}
    )
    assert code == 400
    assert data["error"] == "invalid_scenario"
    assert data["allowed"] == scenario_names()


def test_demo_missing_body_returns_400(client: _TestClient) -> None:
    code, data = client.request("POST", "/demo/meeting-follow-up")
    assert code == 400
    assert data["error"] == "missing_body"


def test_demo_html_view(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS", "view": "html"},
    )
    assert code == 200
    assert "<section class='mg-guide-card'>" in data["card_view"]


def test_demo_text_view(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS", "view": "text"},
    )
    assert code == 200
    assert "MG Guide Meeting Follow-Up Card" in data["card_view"]


def test_demo_json_view_has_no_rendered_view(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS", "view": "json"},
    )
    assert code == 200
    assert data["card_view"] is None
