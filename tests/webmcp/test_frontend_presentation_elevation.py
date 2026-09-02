"""Deterministic contract checks for the presentation-only WebMCP elevation."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_ROOT = REPO_ROOT / "webmcp" / "static"
INDEX_HTML = STATIC_ROOT / "index.html"
APP_JS = STATIC_ROOT / "app.js"
STYLE_CSS = STATIC_ROOT / "style.css"
LOGO_PNG = STATIC_ROOT / "mg-guide-logo.png"

TOOLS = (
    "process_meeting_follow_up",
    "get_current_follow_up_state",
    "get_follow_up_draft",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_brand_and_workspace_identity_are_explicit() -> None:
    html = _read(INDEX_HTML)
    for text in (
        "The Miliare Group",
        "MG Guide",
        "Agentic Sales Workspace",
        "From meeting context to human-reviewed follow-up.",
    ):
        assert text in html
    assert 'src="./mg-guide-logo.png"' in html
    assert 'alt="MG Guide logo"' in html
    assert LOGO_PNG.is_file()
    assert LOGO_PNG.stat().st_size == 19722


def test_product_horizon_is_noninteractive_and_bounded() -> None:
    html = _read(INDEX_HTML)
    nav = html[html.index('<nav class="product-horizon"') : html.index("</nav>")]
    assert "Meeting Follow-Up" in nav
    assert nav.count("ACTIVE") == 1
    assert nav.count("PLANNED") == 4
    assert "Relationship Intelligence" in nav
    assert "Meeting Prep" in nav
    assert "Opportunity Workspace" in nav
    assert "Follow-Up Cadence" in nav
    assert "<button" not in nav
    assert "<a " not in nav


def test_five_step_workspace_and_required_labels_are_present() -> None:
    html = _read(INDEX_HTML)
    for heading in (
        "Meeting Context",
        "Relationship Context",
        "Follow-Up Plan",
        "Follow-Up Draft",
        "Human Review",
    ):
        assert heading in html
    for element_id in (
        "step-meeting-status",
        "step-relationship-status",
        "step-plan-status",
        "step-draft-status",
        "step-human-status",
    ):
        assert f'id="{element_id}"' in html


def test_presentation_maps_canonical_success_and_ambiguous_states() -> None:
    src = _read(APP_JS)
    assert 'completed ? "MATCHED" : "NEEDS REVIEW"' in src
    assert 'completed ? "PREPARED" : "BLOCKED"' in src
    assert 'completed ? "READY" : "NOT AVAILABLE"' in src
    assert 'setText(els.stepMeetingStatus, "READY")' in src
    assert 'setText(els.stepHumanStatus, "REQUIRED")' in src
    assert 'data-workflow-presentation' in src


def test_initial_state_is_waiting_and_never_autoruns() -> None:
    html = _read(INDEX_HTML)
    src = _read(APP_JS)
    assert 'data-workflow-presentation="waiting"' in html
    assert "Waiting for synthetic meeting context." in html
    assert "No draft is available until a meeting is processed." in html
    assert "renderState(null);" in src
    assert not re.search(r'processMeeting\(\s*["\']SUCCESS["\']\s*\)\s*;', src)


def test_native_connection_claim_is_set_only_after_registration() -> None:
    html = _read(INDEX_HTML)
    src = _read(APP_JS)
    assert "Checking native WebMCP availability" in html
    assert '"WebMCP Connected · " + registeredNames.length + " Native Tools"' in src
    feature_guard = src.index("function registerWebMCPTools()")
    connected_claim = src.index('"WebMCP Connected · "')
    register_call = src.index("document.modelContext.registerTool({", feature_guard)
    assert feature_guard < register_call < connected_claim


def test_native_capability_panel_preserves_exact_tools() -> None:
    html = _read(INDEX_HTML)
    capability = html[
        html.index('id="section-capabilities"') : html.index('id="section-activity"')
    ]
    assert "Native WebMCP Capabilities" in capability
    assert "Typed capabilities available directly to browser agents." in capability
    assert ">ACTION<" in capability
    assert ">STATE<" in capability
    assert ">ARTIFACT<" in capability
    for tool in TOOLS:
        assert f'<code class="capability-tool">{tool}</code>' in capability


def test_human_authority_is_persistent_and_explicit() -> None:
    html = _read(INDEX_HTML)
    assert "Agent can prepare." in html
    assert "Only a person can review and send." in html
    assert "requires_human_send=true" in html
    assert "external_effects=0" in html


def test_canonical_mg_palette_is_used() -> None:
    css = _read(STYLE_CSS).lower()
    assert "--gold: #eccd86" in css
    assert "--black: #000000" in css
    assert "--white: #ffffff" in css
    assert "#14213d" not in css
    assert "#2a5db0" not in css


def test_raw_technical_state_is_visually_secondary() -> None:
    html = _read(INDEX_HTML)
    assert '<details class="technical-inspector">' in html
    assert "<summary>Technical state inspector</summary>" in html
    assert "<details class=\"technical-inspector\" open" not in html


def test_no_reference_runtime_contract_leaked_into_canonical_assets() -> None:
    shipped = "\n".join(_read(path) for path in (INDEX_HTML, APP_JS, STYLE_CSS))
    for banned in (
        "/demo/meeting-follow-up",
        "X-MG-Guide-Demo-Auth",
        "STAGE_CHANGE_DENIED",
        "runDualScenario",
    ):
        assert banned not in shipped
