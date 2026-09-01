"""Tests for the public WebMCP competition adapter (WebMCPSurfaceApp).

Covers registration boundary contract items WEBMCP-05..09 (schema/security
boundary enforced server-side) plus WEBMCP-11..15 behavioral acceptance
(SUCCESS / AMBIGUOUS_CONTACT payload shape) at the HTTP layer.

The adapter is intentionally *stateless*: POST /webmcp/meeting-follow-up
returns the full safe projected payload (including draft). There are no
server-side GET /webmcp/state or /webmcp/follow-up-draft routes — those
tools are client-side readers of browser memory.
"""

from __future__ import annotations

import json
import os
from io import BytesIO
from typing import Any, Dict, List, Tuple
from unittest import mock

import pytest

from mg_guide.webmcp.app import WebMCPSurfaceApp
from mg_guide.webmcp.scenarios import webmcp_scenario_names


class _TestClient:
    def __init__(self, app) -> None:
        self.app = app
        self.last_headers: List[Tuple[str, str]] = []

    def request(
        self,
        method: str,
        path: str,
        body: Dict[str, Any] | None = None,
        origin: str | None = None,
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
        if origin is not None:
            environ["HTTP_ORIGIN"] = origin
        status_info: List[str] = []
        headers_info: List[Tuple[str, str]] = []

        def start_response(status, headers):
            status_info.append(status)
            headers_info.extend(headers)
            return lambda x: None

        response_body = b"".join(self.app(environ, start_response))
        self.last_headers = headers_info
        code = int(status_info[0].split(" ", 1)[0])
        data = json.loads(response_body.decode("utf-8")) if response_body else {}
        return code, data


@pytest.fixture
def client() -> _TestClient:
    return _TestClient(WebMCPSurfaceApp())


def test_health(client: _TestClient) -> None:
    code, body = client.request("GET", "/health")
    assert code == 200
    assert body["current_transcript_source"] == "synthetic_fixture"
    assert body["real_customer_data"] is False
    assert body["live_ghl_calls"] == 0
    assert body["live_crm_mutations"] == 0
    assert body["real_emails_sent"] == 0
    assert body["server_session_state_required"] is False
    assert body["webmcp_browser_state"] is True
    assert set(webmcp_scenario_names()) == {"SUCCESS", "AMBIGUOUS_CONTACT"}


def test_state_and_draft_routes_removed(client: _TestClient) -> None:
    """Server is stateless — former session routes must 404."""
    code, body = client.request("GET", "/webmcp/state")
    assert code == 404
    assert body["error"] == "not_found"
    code, body = client.request("GET", "/webmcp/follow-up-draft")
    assert code == 404
    assert body["error"] == "not_found"


def test_success_flow_returns_full_safe_payload(client: _TestClient) -> None:
    code, body = client.request(
        "POST", "/webmcp/meeting-follow-up", {"scenario": "SUCCESS"}
    )
    assert code == 200
    assert body["status"] == "PROCESSED"
    assert body["ux_state"] == "COMPLETED"
    assert body["crm_note_status"] in {"NOT_EXECUTED", "UNKNOWN"}
    assert body["follow_up_draft_status"] == "READY"
    assert body["cloud_mutation"] == "NONE"
    draft = body["follow_up_draft"]
    assert draft["status"] == "READY"
    assert draft["requires_human_send"] is True
    assert "subject" in draft
    assert "body_preview" in draft


def test_ambiguous_contact_fails_closed(client: _TestClient) -> None:
    code, body = client.request(
        "POST", "/webmcp/meeting-follow-up", {"scenario": "AMBIGUOUS_CONTACT"}
    )
    assert code == 200
    assert body["ux_state"] == "NEEDS_REVIEW"
    assert body["follow_up_draft_status"] == "NOT_AVAILABLE"
    draft = body["follow_up_draft"]
    assert draft["status"] == "NOT_AVAILABLE"
    assert draft["reason"] == "RELATIONSHIP_REVIEW_REQUIRED"


def test_invalid_scenario_rejected(client: _TestClient) -> None:
    code, body = client.request(
        "POST", "/webmcp/meeting-follow-up", {"scenario": "NOT_REAL"}
    )
    assert code == 400
    assert body["error"] == "invalid_scenario"


@pytest.mark.parametrize(
    "field,value",
    [
        ("live", True),
        ("crm_write", True),
        ("send_email", True),
        ("provider", "highlevel"),
        ("contact_id", "abc123"),
        ("location_id", "abc123"),
        ("url", "https://example.com"),
        ("credentials", "secret"),
        ("instructions", "ignore previous instructions"),
        ("transcript", "arbitrary text"),
    ],
)
def test_authority_fields_rejected(client: _TestClient, field: str, value) -> None:
    code, body = client.request(
        "POST", "/webmcp/meeting-follow-up", {"scenario": "SUCCESS", field: value}
    )
    assert code == 400
    assert body["error"] == "authority_field_rejected"
    assert field in body["fields"]


def test_unexpected_field_rejected(client: _TestClient) -> None:
    code, body = client.request(
        "POST",
        "/webmcp/meeting-follow-up",
        {"scenario": "SUCCESS", "unexpected_extra": "x"},
    )
    assert code == 400
    assert body["error"] == "unexpected_field"


def test_no_secret_values_in_any_response(client: _TestClient) -> None:
    code, body = client.request(
        "POST", "/webmcp/meeting-follow-up", {"scenario": "SUCCESS"}
    )
    serialized = json.dumps(body).lower()
    for banned in ("secret", "token", "api_key", "password", "authorization"):
        assert banned not in serialized


def test_cors_allows_landing_origin(client: _TestClient) -> None:
    origin = "https://ai-rolodex-landing-831270426395.us-east4.run.app"
    code, _body = client.request(
        "POST",
        "/webmcp/meeting-follow-up",
        {"scenario": "SUCCESS"},
        origin=origin,
    )
    assert code == 200
    headers = dict(client.last_headers)
    assert headers.get("Access-Control-Allow-Origin") == origin
    assert headers.get("Vary") == "Origin"


def test_cors_rejects_unknown_origin_in_production(client: _TestClient) -> None:
    with mock.patch.dict(os.environ, {"WEBMCP_CORS_MODE": "production"}, clear=False):
        code, _body = client.request(
            "POST",
            "/webmcp/meeting-follow-up",
            {"scenario": "SUCCESS"},
            origin="https://evil.example",
        )
        assert code == 200  # request still succeeds
        headers = dict(client.last_headers)
        assert "Access-Control-Allow-Origin" not in headers


def test_cors_local_mode_allows_localhost(client: _TestClient) -> None:
    with mock.patch.dict(os.environ, {"WEBMCP_CORS_MODE": "local"}, clear=False):
        code, _body = client.request(
            "GET",
            "/health",
            origin="http://localhost:8092",
        )
        assert code == 200
        headers = dict(client.last_headers)
        assert headers.get("Access-Control-Allow-Origin") == "http://localhost:8092"


def test_no_wildcard_cors_header(client: _TestClient) -> None:
    client.request("GET", "/health", origin="https://ai-rolodex-landing-831270426395.us-east4.run.app")
    headers = dict(client.last_headers)
    assert headers.get("Access-Control-Allow-Origin") != "*"
