"""Static-source checks for the WebMCP frontend tool registration contract.

These tests do not execute a browser; they verify the required
``document.modelContext.registerTool`` usage, tool naming, schema shape,
feature-detection guard, browser-held state, runtime API-base configuration,
and subpath-safe host assets exist in the shipped source. Full browser
acceptance is recorded separately in ``proof/webmcp/``.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_ROOT = REPO_ROOT / "webmcp" / "static"
APP_JS = STATIC_ROOT / "app.js"
INDEX_HTML = STATIC_ROOT / "index.html"
CONFIG_JS = STATIC_ROOT / "config.js"

REQUIRED_TOOL_NAMES = [
    "process_meeting_follow_up",
    "get_current_follow_up_state",
    "get_follow_up_draft",
]


def _source() -> str:
    return APP_JS.read_text(encoding="utf-8")


def test_source_uses_real_webmcp_registration_api() -> None:
    src = _source()
    assert "document.modelContext.registerTool" in src


def test_feature_detection_guard_present() -> None:
    src = _source()
    assert "document.modelContext &&" in src or "document.modelContext &&\n" in src
    assert "document.modelContext.registerTool" in src
    assert "registerWebMCPTools" in src


def test_no_registration_before_feature_check() -> None:
    src = _source()
    call_matches = list(re.finditer(r"document\.modelContext\.registerTool\(", src))
    assert call_matches, "expected at least one registerTool call"
    first_mc = src.index("document.modelContext")
    assert call_matches[0].start() > first_mc


def test_all_required_tool_names_present_and_unique() -> None:
    src = _source()
    found = re.findall(r'name:\s*"([a-z_]+)"', src)
    for name in REQUIRED_TOOL_NAMES:
        assert name in found
    assert len(found) == len(set(found)), "tool names must be unique"


def test_tool_descriptions_non_empty() -> None:
    src = _source()
    assert src.count("description:") >= len(REQUIRED_TOOL_NAMES)
    assert "No live CRM effects occur" in src or "live CRM" in src


def test_scenario_enum_bounded_to_success_and_ambiguous() -> None:
    src = _source()
    enum_match = re.search(r"enum:\s*\[([^\]]+)\]", src)
    assert enum_match is not None
    values = [v.strip().strip('"').strip("'") for v in enum_match.group(1).split(",")]
    assert set(values) == {"SUCCESS", "AMBIGUOUS_CONTACT"}


def test_input_schema_rejects_additional_properties() -> None:
    src = _source()
    assert src.count("additionalProperties: false") >= len(REQUIRED_TOOL_NAMES)


def test_no_live_or_authority_selectors_in_tool_schemas() -> None:
    src = _source()
    tools_section = src[src.index("const tools = ["): src.index("registerWebMCPTools();")]
    for banned in (
        "live",
        "crm_write",
        "send_email",
        "provider",
        "contact_id",
        "credentials",
    ):
        assert f'"{banned}"' not in tools_section and f"'{banned}'" not in tools_section


def test_browser_holds_state_not_server() -> None:
    src = _source()
    assert "currentWebMCPState" in src
    assert "getCurrentStateFromBrowser" in src
    assert "getFollowUpDraftFromBrowser" in src
    assert "/webmcp/state" not in src
    assert "/webmcp/follow-up-draft" not in src


def test_api_base_configurable() -> None:
    src = _source()
    assert "MG_GUIDE_WEBMCP_API_BASE" in src
    assert "API_BASE" in src


def test_index_assets_are_subpath_safe_and_config_loads_first() -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")
    assert 'href="./style.css"' in html
    assert 'src="./config.js"' in html
    assert 'src="./app.js"' in html
    assert html.index('src="./config.js"') < html.index('src="./app.js"')
    assert 'href="/style.css"' not in html
    assert 'src="/app.js"' not in html


def test_runtime_config_defaults_same_origin_without_overwriting_host_value() -> None:
    config = CONFIG_JS.read_text(encoding="utf-8")
    assert 'typeof window.MG_GUIDE_WEBMCP_API_BASE !== "string"' in config
    assert 'window.MG_GUIDE_WEBMCP_API_BASE = ""' in config
