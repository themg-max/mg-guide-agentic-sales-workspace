"""Tests for the judge-safe HTTP adapter."""

from __future__ import annotations

import json
import logging
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
        headers: Dict[str, str] | None = None,
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
        if headers:
            environ.update(headers)

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


def test_addon_auth_only_gates_demo_route(monkeypatch) -> None:
    monkeypatch.setenv("JUDGE_ADDON_AUTH_MODE", "identity_token")
    monkeypatch.setenv("JUDGE_ADDON_OIDC_AUDIENCE", "test-audience")
    client = _TestClient(JudgeSurfaceApp())

    health_code, health_data = client.request("GET", "/health")
    healthz_code, healthz_data = client.request("GET", "/healthz")
    demo_code, demo_data = client.request(
        "POST", "/demo/meeting-follow-up", {"scenario": "SUCCESS"}
    )

    assert health_code == 200
    assert health_data["status"] == "ok"
    assert healthz_code == 200
    assert healthz_data["status"] == "ok"
    assert demo_code == 401
    assert demo_data["code"] == "AUTH_ERROR"


def test_local_demo_mode_fails_closed_on_cloud_run(monkeypatch) -> None:
    monkeypatch.setenv("JUDGE_ADDON_AUTH_MODE", "local_demo")
    monkeypatch.setenv("K_SERVICE", "mg-guide-agentic-sales-workspace-addon-judge")
    client = _TestClient(JudgeSurfaceApp())

    health_code, health_data = client.request("GET", "/health")
    demo_code, demo_data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS"},
        {"HTTP_X_MG_GUIDE_DEMO_AUTH": "local-demo"},
    )

    assert health_code == 200
    assert health_data["status"] == "ok"
    assert demo_code == 503
    assert demo_data == {
        "error": "addon_auth_mode_rejected",
        "code": "LOCAL_DEMO_PUBLIC_INGRESS_FORBIDDEN",
    }


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


def test_demo_replay_isolated_per_request() -> None:
    client = _TestClient(JudgeSurfaceApp())
    for scenario in ("SUCCESS", "SUCCESS", "AMBIGUOUS_CONTACT", "AMBIGUOUS_CONTACT"):
        code, data = client.request("POST", "/demo/meeting-follow-up", {"scenario": scenario})
        assert code == 200
        assert data["scenario"] == scenario


def test_judge_request_log_is_structured_and_token_safe(caplog) -> None:
    client = _TestClient(JudgeSurfaceApp())
    with caplog.at_level(logging.INFO, logger="mg_guide.judge_surface"):
        code, _ = client.request(
            "POST",
            "/demo/meeting-follow-up",
            {"scenario": "SUCCESS"},
            {"HTTP_AUTHORIZATION": "Bearer synthetic-token-must-not-appear"},
        )
    assert code == 200
    record = json.loads(caplog.records[-1].message)
    assert set(record) == {
        "request_id",
        "scenario",
        "auth_mode",
        "workflow_status",
        "ux_state",
        "http_status",
        "latency_ms",
        "external_effects",
        "revision",
        "gemini_mode",
        "error_code",
        "audience_configured",
        "token_logged",
    }
    assert record["scenario"] == "SUCCESS"
    assert record["http_status"] == 200
    assert record["external_effects"] == 0
    assert record["token_logged"] is False
    assert "synthetic-token-must-not-appear" not in caplog.text


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


def test_demo_success_includes_demo_stages(client: _TestClient) -> None:
    code, data = client.request("POST", "/demo/meeting-follow-up", {"scenario": "SUCCESS"})
    assert code == 200
    stages = data["demo_stages"]
    assert len(stages) == 6
    assert [s["title"] for s in stages] == [
        "Meeting ready",
        "Meeting Context",
        "Relationship Resolution",
        "Follow-Up Planning",
        "Policy Evaluation",
        "Meeting Follow-Up result card",
    ]
    truth = data["demo_truth"]
    assert truth["LIVE_CRM_EXECUTION"] == "NOT_PERFORMED"
    assert truth["EXTERNAL_EFFECTS"] == 0
    assert truth["cloud_mutation"] == "NONE"
    ux = data["ux_experience"]
    assert ux["ux_state"] == "COMPLETED"
    assert ux["policy_decision"]["note_write"] == "allowed"
    assert ux["salesperson_next_step"]
    assert ux["audit_status"]["recorded"] is True
    assert ux["permitted_action_result"]["external_effects"] == 0


def test_demo_ambiguous_includes_demo_stages(client: _TestClient) -> None:
    code, data = client.request(
        "POST", "/demo/meeting-follow-up", {"scenario": "AMBIGUOUS_CONTACT"}
    )
    assert code == 200
    assert len(data["demo_stages"]) == 6
    policy_stage = data["demo_stages"][4]["evidence"]
    assert policy_stage["reason_codes"] == ["AMBIGUOUS_CONTACT"]
    assert policy_stage["note_write"] == "not_attempted"
    assert policy_stage["stage_write"] == "not_attempted"
    ux = data["ux_experience"]
    assert ux["ux_state"] == "NEEDS_REVIEW"
    assert ux["needs_review"]["zero_unauthorized_effects"] is True
    assert "No CRM changes were made" in ux["needs_review"]["zero_unauthorized_effects_message"]
    assert ux["needs_review"]["explicit_next_action"]
    assert data["demo_truth"]["EXTERNAL_EFFECTS"] == 0


def test_demo_stages_html_view(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS", "view": "stages_html"},
    )
    assert code == 200
    html = data["card_view"]
    assert html is not None
    assert "mg-guide-demo-stages" in html
    assert "Meeting ready" in html
    assert "Meeting Context" in html
    assert "Relationship Resolution" in html
    assert "Follow-Up Planning" in html
    assert "Policy Evaluation" in html
    assert "Meeting Follow-Up result card" in html
    assert "LIVE_CRM_EXECUTION" in html
    assert "NOT_PERFORMED" in html
    assert "COMPLETED" in html
    assert "Salesperson next step" in html
    assert "Policy decision" in html
    assert "Audit status" in html


def test_demo_stages_html_needs_review(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "AMBIGUOUS_CONTACT", "view": "stages_html"},
    )
    assert code == 200
    html = data["card_view"]
    assert "NEEDS_REVIEW" in html
    assert "Jordan Lee" in html
    assert "AMBIGUOUS_CONTACT" in html
    assert "No CRM changes were made" in html


def test_demo_stages_text_view(client: _TestClient) -> None:
    code, data = client.request(
        "POST",
        "/demo/meeting-follow-up",
        {"scenario": "SUCCESS", "view": "stages_text"},
    )
    assert code == 200
    text = data["card_view"]
    assert "MG Guide Meeting Follow-Up" in text
    assert "UX state: COMPLETED" in text
    assert "EXTERNAL_EFFECTS=0" in text
