"""Static-source checks for the WebMCP frontend tool registration contract.

These tests do not execute a browser; they verify the required
document.modelContext.registerTool usage, tool naming, schema shape, and
feature-detection guard exist in the shipped source, satisfying
WEBMCP-01..04, WEBMCP-10, and WEBMCP-20 without requiring a live browser in
CI. Full browser acceptance (WEBMCP-11..15) is recorded separately in
proof/webmcp/ from manual Chrome/agent testing.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_JS = REPO_ROOT / "webmcp" / "static" / "app.js"

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
    # No tool registration must occur if modelContext is unavailable.
    assert "document.modelContext && document.modelContext.registerTool" in src
    assert "registerWebMCPTools" in src


def test_no_registration_before_feature_check() -> None:
    src = _source()
    guard_idx = src.index("if (!(window.document")
    first_register_idx = src.index("document.modelContext.registerTool(")
    assert first_register_idx > guard_idx


def test_all_required_tool_names_present_and_unique() -> None:
    src = _source()
    found = re.findall(r'name:\s*"([a-z_]+)"', src)
    for name in REQUIRED_TOOL_NAMES:
        assert name in found
    assert len(found) == len(set(found)), "tool names must be unique"


def test_tool_descriptions_non_empty() -> None:
    src = _source()
    descriptions = re.findall(r'description:\s*\n?\s*"([^"]+)"', src)
    assert len(descriptions) >= len(REQUIRED_TOOL_NAMES)
    for desc in descriptions:
        assert desc.strip()


def test_scenario_enum_bounded_to_success_and_ambiguous() -> None:
    src = _source()
    enum_match = re.search(r'enum:\s*\[([^\]]+)\]', src)
    assert enum_match is not None
    values = [v.strip().strip('"') for v in enum_match.group(1).split(",")]
    assert set(values) == {"SUCCESS", "AMBIGUOUS_CONTACT"}


def test_input_schema_rejects_additional_properties() -> None:
    src = _source()
    assert src.count("additionalProperties: false") >= len(REQUIRED_TOOL_NAMES)


def test_no_live_or_authority_selectors_in_tool_schemas() -> None:
    src = _source()
    tools_section = src[src.index("const tools = ["):src.index("registerWebMCPTools();")]
    for banned in ("live", "crm_write", "send_email", "provider", "contact_id", "credentials"):
        assert f'"{banned}"' not in tools_section and f"'{banned}'" not in tools_section
