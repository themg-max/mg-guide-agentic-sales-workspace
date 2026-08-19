"""Ensure competition Apps Script sources never log raw identity tokens."""

from __future__ import annotations

from pathlib import Path

from mg_guide.workspace_addon.security import (
    assert_no_raw_token_logging,
    competition_apps_script_paths,
    scan_text_for_token_leak,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
STABLE_LOGO_URL = (
    "https://storage.googleapis.com/"
    "mg-devpost-assets/mg-guide/mg-guide-128x128.png"
)


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
    common = manifest["addOns"]["common"]
    assert common["layoutProperties"] == {
        "primaryColor": "#BDA161",
        "secondaryColor": "#000000",
    }
    assert common["logoUrl"] == STABLE_LOGO_URL
    assert common["logoUrl"].startswith("https://")
    assert "raw.githubusercontent.com" not in common["logoUrl"]
    assert common["logoUrl"].endswith("mg-guide/mg-guide-128x128.png")
    config = (REPO_ROOT / "workspace_addon" / "Config.gs").read_text(encoding="utf-8")
    assert STABLE_LOGO_URL in config
    assert "raw.githubusercontent.com" not in config
    scopes = set(manifest["oauthScopes"])
    assert "openid" in scopes
    assert "https://www.googleapis.com/auth/script.external_request" in scopes
    assert "https://www.googleapis.com/auth/gmail.addons.execute" in scopes
    assert "https://www.googleapis.com/auth/calendar.addons.execute" in scopes
    # No broad admin / drive write scopes on the competition adapter.
    for forbidden in scopes:
        assert "admin.directory" not in forbidden
        assert forbidden != "https://www.googleapis.com/auth/drive"


def test_cardservice_template_keeps_judge_hierarchy_visible():
    cards = (REPO_ROOT / "workspace_addon" / "Cards.gs").read_text(encoding="utf-8")
    required = (
        "MG_GUIDE_PRODUCT_NAME",
        "MG_GUIDE_ATTRIBUTION",
        "MG_GUIDE_PRIMARY_CAPABILITY",
        "MG_GUIDE_LOGO_URL",
        "setImageStyle(CardService.ImageStyle.SQUARE)",
        "setImageAltText('MG Guide logo')",
        "Turn a meeting into a governed follow-up plan.",
        "Synthetic data · No CRM writes",
        "'Outcome'",
        "'Meeting summary'",
        "'Relationship'",
        "'Policy'",
        "'Six-stage workflow summary'",
        "'Salesperson next step'",
        "'Audit'",
        "stages.length !== 6",
        "'Integrity'",
        "external_effects=",
        "LIVE_CRM_EXECUTION=",
    )
    for marker in required:
        assert marker in cards
    assert "brandFooter_" not in cards
    assert "'Run SUCCESS'" not in cards
    assert "'Run AMBIGUOUS_CONTACT'" not in cards
