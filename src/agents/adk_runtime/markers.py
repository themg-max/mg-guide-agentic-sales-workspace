"""Unit 2 Google ADK runtime tech markers.

These markers are intentionally separate from the Unit 1 Meeting Context
provider surface markers (which remain COMPATIBLE_SURFACE_ONLY).
"""

from __future__ import annotations

# Unit 2 truth: multi-agent orchestration runtime is integrated and started.
GOOGLE_ADK_RUNTIME_STARTED = True
ADK_INTEGRATION_STATUS = "RUNTIME_INTEGRATED"
GEMINI_PROVIDER_STARTED = True  # Unit 1 provider surface remains available
# Compatibility umbrella remains true once either provider or runtime is active.
GEMINI_ADK_STARTED = True

RUNTIME_BACKEND_LOCAL = "local_adk_compatible_runtime"
RUNTIME_BACKEND_GOOGLE_ADK = "google_adk_package"


def runtime_markers() -> dict:
    return {
        "google_adk_runtime_started": GOOGLE_ADK_RUNTIME_STARTED,
        "adk_integration_status": ADK_INTEGRATION_STATUS,
        "gemini_provider_started": GEMINI_PROVIDER_STARTED,
        "gemini_adk_started": GEMINI_ADK_STARTED,
        "deterministic_policy_bypass": False,
        "external_effects": 0,
        "ghl_live_calls": 0,
        "ghl_writes": 0,
        "real_customer_data": 0,
        "l3a_runtime_promoted": False,
        "firestore_writes": 0,
        "deployment": False,
    }
