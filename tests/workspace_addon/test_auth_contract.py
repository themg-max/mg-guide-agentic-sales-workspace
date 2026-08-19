"""Auth contract unit tests — no raw token logging, structural validation."""

from __future__ import annotations

import base64
import json
import time

import pytest

from mg_guide.judge_surface.app import JudgeSurfaceApp
from mg_guide.workspace_addon.auth_contract import (
    AUTH_CONTRACT_ID,
    AuthError,
    AuthMode,
    auth_mode_from_env,
    validate_authorization_header,
)


def _b64(data: dict) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _synthetic_jwt(claims: dict, header: dict | None = None) -> str:
    hdr = header or {"alg": "RS256", "typ": "JWT", "kid": "test-kid"}
    return f"{_b64(hdr)}.{_b64(claims)}.sig"


def test_auth_contract_id_stable():
    assert AUTH_CONTRACT_ID == "MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1"


def test_default_mode_off():
    assert auth_mode_from_env({}) is AuthMode.OFF
    ctx = validate_authorization_header({}, env={})
    assert ctx.mode is AuthMode.OFF


def test_local_demo_mode():
    env = {"JUDGE_ADDON_AUTH_MODE": "local_demo"}
    with pytest.raises(AuthError):
        validate_authorization_header({}, env=env)
    ctx = validate_authorization_header(
        {"X-MG-Guide-Demo-Auth": "local-demo"}, env=env
    )
    assert ctx.mode is AuthMode.LOCAL_DEMO
    assert ctx.email.endswith("@example-demo.test")


def test_identity_token_valid_unverified_for_tests():
    now = time.time()
    token = _synthetic_jwt(
        {
            "iss": "https://accounts.google.com",
            "aud": "test-audience",
            "exp": now + 3600,
            "email": "judge@example-demo.test",
            "email_verified": True,
            "sub": "subject-1",
            "hd": "example-demo.test",
        }
    )
    env = {
        "JUDGE_ADDON_AUTH_MODE": "identity_token",
        "JUDGE_ADDON_OIDC_AUDIENCE": "test-audience",
        "JUDGE_ADDON_ALLOWED_HD": "example-demo.test",
    }
    ctx = validate_authorization_header(
        {"Authorization": f"Bearer {token}"},
        env=env,
        now=now,
        allow_unverified_for_tests=True,
    )
    assert ctx.email == "judge@example-demo.test"
    assert ctx.hosted_domain == "example-demo.test"


def test_identity_token_rejects_bad_issuer():
    now = time.time()
    token = _synthetic_jwt(
        {
            "iss": "https://evil.example",
            "aud": "test-audience",
            "exp": now + 3600,
            "email": "judge@example-demo.test",
            "email_verified": True,
        }
    )
    env = {
        "JUDGE_ADDON_AUTH_MODE": "identity_token",
        "JUDGE_ADDON_OIDC_AUDIENCE": "test-audience",
    }
    with pytest.raises(AuthError) as exc:
        validate_authorization_header(
            {"Authorization": f"Bearer {token}"},
            env=env,
            now=now,
            allow_unverified_for_tests=True,
        )
    assert "token" not in exc.value.message.lower() or "Identity token" in exc.value.message
    # Body must not include the raw token
    body = exc.value.as_body()
    assert token not in json.dumps(body)


def test_identity_token_rejects_expired():
    now = time.time()
    token = _synthetic_jwt(
        {
            "iss": "https://accounts.google.com",
            "aud": "test-audience",
            "exp": now - 3600,
            "email": "judge@example-demo.test",
            "email_verified": True,
        }
    )
    env = {
        "JUDGE_ADDON_AUTH_MODE": "identity_token",
        "JUDGE_ADDON_OIDC_AUDIENCE": "test-audience",
    }
    with pytest.raises(AuthError):
        validate_authorization_header(
            {"Authorization": f"Bearer {token}"},
            env=env,
            now=now,
            allow_unverified_for_tests=True,
        )


def test_judge_surface_default_auth_off_still_works():
    from io import BytesIO

    app = JudgeSurfaceApp()
    payload = b'{"scenario":"SUCCESS"}'
    environ = {
        "REQUEST_METHOD": "POST",
        "PATH_INFO": "/demo/meeting-follow-up",
        "CONTENT_LENGTH": str(len(payload)),
        "CONTENT_TYPE": "application/json",
        "wsgi.input": BytesIO(payload),
        "wsgi.errors": BytesIO(),
        "wsgi.url_scheme": "http",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "8080",
    }
    status_box = []

    def start_response(status, headers):
        status_box.append(status)

    body = b"".join(app(environ, start_response))
    assert status_box[0].startswith("200")
    data = json.loads(body.decode("utf-8"))
    assert data["workflow_status"] == "completed"


def test_judge_surface_local_demo_mode(monkeypatch):
    from io import BytesIO

    monkeypatch.setenv("JUDGE_ADDON_AUTH_MODE", "local_demo")
    app = JudgeSurfaceApp()
    payload = b'{"scenario":"SUCCESS"}'

    def _call(extra_headers=None):
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/demo/meeting-follow-up",
            "CONTENT_LENGTH": str(len(payload)),
            "CONTENT_TYPE": "application/json",
            "wsgi.input": BytesIO(payload),
            "wsgi.errors": BytesIO(),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8080",
        }
        if extra_headers:
            environ.update(extra_headers)
        status_box = []

        def start_response(status, headers):
            status_box.append(status)

        body = b"".join(app(environ, start_response))
        return int(status_box[0].split()[0]), json.loads(body.decode("utf-8"))

    code, data = _call()
    assert code == 401
    assert data["code"] == "AUTH_ERROR"
    assert "Bearer" not in json.dumps(data)

    code, data = _call({"HTTP_X_MG_GUIDE_DEMO_AUTH": "local-demo"})
    assert code == 200
    assert data["scenario"] == "SUCCESS"
