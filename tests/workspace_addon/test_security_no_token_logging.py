"""Ensure competition Apps Script sources never log raw identity tokens."""

from __future__ import annotations

from pathlib import Path

from mg_guide.workspace_addon.security import (
    assert_no_raw_token_logging,
    competition_apps_script_paths,
    scan_text_for_token_leak,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_competition_apps_script_has_no_token_logging():
    paths = competition_apps_script_paths(REPO_ROOT)
    assert paths, "expected workspace_addon/*.gs sources"
    assert_no_raw_token_logging(paths)


def test_auth_gs_mentions_forbidden_logging_policy_without_logging_token():
    auth = (REPO_ROOT / "workspace_addon" / "Auth.gs").read_text(encoding="utf-8")
    assert "getIdentityToken" in auth
    assert "console.log" not in auth
    assert "Logger.log" not in auth
    assert "Bearer " in auth  # header construction
    findings = scan_text_for_token_leak(auth)
    assert findings == []


def test_legacy_pattern_would_be_detected():
    bad = 'console.log("Identity Token from ScriptApp: " + identityToken);'
    assert scan_text_for_token_leak(bad)


def test_manifest_branding_and_scopes():
    import json

    manifest = json.loads(
        (REPO_ROOT / "workspace_addon" / "appsscript.json").read_text(encoding="utf-8")
    )
    assert manifest["addOns"]["common"]["name"] == "MG Guide"
    scopes = set(manifest["oauthScopes"])
    assert "openid" in scopes
    assert "https://www.googleapis.com/auth/script.external_request" in scopes
    assert "https://www.googleapis.com/auth/gmail.addons.execute" in scopes
    assert "https://www.googleapis.com/auth/calendar.addons.execute" in scopes
    # No broad admin / drive write scopes on the competition adapter.
    for forbidden in scopes:
        assert "admin.directory" not in forbidden
        assert forbidden != "https://www.googleapis.com/auth/drive"
