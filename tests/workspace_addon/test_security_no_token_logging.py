"""Ensure competition Apps Script sources never log raw identity tokens.

Also covers the UX v2 compose surface: least-privilege scopes, no email
auto-send APIs, and no CRM implementation inside the thin adapter.
"""

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

# Any of these in an Apps Script source would mean the add-on can send mail
# without the human pressing send. The compose action may only create drafts.
FORBIDDEN_EMAIL_SEND_PATTERNS = (
    "GmailApp.sendEmail",
    "MailApp.sendEmail",
    ".reply(",
    ".replyAll(",
    ".send(",
)

# The adapter must not implement CRM access; it renders backend truth only.
FORBIDDEN_CRM_PATTERNS = (
    "highlevel",
    "leadconnector",
    "ghl",
    "/contacts/",
    "/opportunities/",
    "createContact",
    "updateContact",
    "createNote",
    "note_write_request",
    "stage_write_request",
)


def _addon_sources():
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in competition_apps_script_paths(REPO_ROOT)
    }


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


def test_t_draft_14_no_token_values_logged_anywhere_in_addon():
    sources = _addon_sources()
    assert "DraftFollowUp.gs" in sources
    for name, text in sources.items():
        assert scan_text_for_token_leak(text) == [], name
        assert "console.log" not in text, name
        assert "Logger.log" not in text, name


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


def _manifest_scopes():
    import json

    manifest = json.loads(
        (REPO_ROOT / "workspace_addon" / "appsscript.json").read_text(encoding="utf-8")
    )
    return set(manifest["oauthScopes"])


def test_t_draft_07_manifest_contains_compose_action_scope():
    scopes = _manifest_scopes()
    assert (
        "https://www.googleapis.com/auth/gmail.addons.current.action.compose"
        in scopes
    )


def test_t_draft_08_manifest_has_no_gmail_send_scope():
    assert "https://www.googleapis.com/auth/gmail.send" not in _manifest_scopes()


def test_t_draft_09_manifest_has_no_gmail_modify_scope():
    assert "https://www.googleapis.com/auth/gmail.modify" not in _manifest_scopes()


def test_t_draft_10_manifest_has_no_full_mail_scope():
    assert "https://mail.google.com/" not in _manifest_scopes()


def test_t_draft_11_manifest_introduces_no_drive_scopes():
    for scope in _manifest_scopes():
        assert "/auth/drive" not in scope
    # Gmail scope surface stays least-privilege: addons execute + compose only.
    gmail_scopes = {
        s
        for s in _manifest_scopes()
        if "/auth/gmail" in s or "mail.google.com" in s
    }
    assert gmail_scopes == {
        "https://www.googleapis.com/auth/gmail.addons.execute",
        "https://www.googleapis.com/auth/gmail.addons.current.action.compose",
    }


def test_t_draft_12_apps_script_contains_no_email_auto_send_api():
    sources = _addon_sources()
    assert sources, "expected workspace_addon/*.gs sources"
    for name, text in sources.items():
        for pattern in FORBIDDEN_EMAIL_SEND_PATTERNS:
            assert pattern not in text, f"{name}: {pattern}"
    # The compose callback only ever creates a draft.
    draft_gs = sources["DraftFollowUp.gs"]
    assert "GmailApp.createDraft" in draft_gs
    assert "newComposeActionResponseBuilder" in draft_gs


def test_t_draft_13_apps_script_contains_no_crm_implementation():
    sources = _addon_sources()
    assert sources, "expected workspace_addon/*.gs sources"
    for name, text in sources.items():
        lowered = text.lower()
        for pattern in FORBIDDEN_CRM_PATTERNS:
            assert pattern.lower() not in lowered, f"{name}: {pattern}"


def test_cardservice_template_keeps_judge_hierarchy_visible():
    cards = (REPO_ROOT / "workspace_addon" / "Cards.gs").read_text(encoding="utf-8")
    required = (
        "MG_GUIDE_PRODUCT_NAME",
        "MG_GUIDE_ATTRIBUTION",
        "MG_GUIDE_PRIMARY_CAPABILITY",
        "MG_GUIDE_LOGO_URL",
        "setImageStyle(CardService.ImageStyle.SQUARE)",
        "setImageAltText('MG Guide logo')",
        "Turn a completed meeting into",
        "relationship context, CRM-ready documentation, and a follow-up draft.",
        "Approved synthetic transcript",
        "governed CRM boundary",
        "Process Meeting Follow-Up",
        "Judge test scenarios",
        "Ambiguous contact",
        "Policy guardrail",
        "Follow-up ready",
        "FOLLOW-UP READY",
        "Processing status",
        "What we heard",
        "'Relationship'",
        "'CRM'",
        "Follow-up draft",
        "Send follow-up",
        "Open Draft in Gmail",
        "Needs review",
        "NEEDS REVIEW",
        "Not created",
        "Audit and integrity",
        "setComposeAction",
        "createFollowUpDraft",
        "CardService.ComposedEmailType.STANDALONE_DRAFT",
        "stages.length !== 6",
        "external_effects=",
        "LIVE_CRM_EXECUTION=",
        "CRM_MUTATIONS_PERFORMED=NO",
        "EMAIL_AUTO_SEND=FORBIDDEN",
    )
    for marker in required:
        assert marker in cards
    assert "brandFooter_" not in cards
    assert "'Run SUCCESS'" not in cards
    assert "'Run AMBIGUOUS_CONTACT'" not in cards
    assert "'Run Successful Follow-Up'" not in cards


def test_draft_follow_up_gs_marks_no_send_contract():
    draft = (REPO_ROOT / "workspace_addon" / "DraftFollowUp.gs").read_text(
        encoding="utf-8"
    )
    assert "EMAIL_AUTO_SEND=FORBIDDEN" in draft
    assert "DRAFT_CREATION_REQUIRES_USER_ACTION=YES" in draft
    assert "FINAL_SEND_REQUIRES_HUMAN=YES" in draft
    assert "function createFollowUpDraft(e)" in draft
    # Compose callback re-fetches the deterministic server projection instead
    # of inventing content client-side.
    assert "fetchMeetingFollowUp_" in draft
    assert "follow_up_draft" in draft
