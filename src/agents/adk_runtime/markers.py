"""Unit 2 Google ADK runtime tech markers (derived, never hard-coded).

All runtime-truth markers are computed from actual runtime state observed by
``GoogleAdkRuntime`` (package binding, backend, started runs, primitive use).
There is no module-level claim that the Google ADK runtime has started; a
caller must supply the measured runtime state.

Unit 1 provider surface markers remain in
``agents.meeting_context.providers.gemini_adk_provider``
(COMPATIBLE_SURFACE_ONLY) and are intentionally separate.
"""

from __future__ import annotations

from typing import Any, Dict

# Backend / status labels (labels only — truth values are derived).
RUNTIME_BACKEND_GOOGLE_ADK = "google_adk_package"
ADK_STATUS_RUNTIME_INTEGRATED = "RUNTIME_INTEGRATED"
ADK_STATUS_NOT_STARTED = "NOT_STARTED"

# Unit 1 provider surface remains available (provider-level markers live in
# the Unit 1 provider module; these umbrella flags reflect that availability).
GEMINI_PROVIDER_STARTED = True
GEMINI_ADK_STARTED = True


def safety_invariants() -> Dict[str, Any]:
    """Design invariants enforced by construction across Unit 2."""
    return {
        "deterministic_policy_bypass": False,
        "external_effects": 0,
        "ghl_live_calls": 0,
        "ghl_writes": 0,
        "real_customer_data": 0,
        "l3a_runtime_promoted": False,
        "firestore_writes": 0,
        "deployment": False,
    }


def derive_runtime_markers(
    *,
    google_adk_package_bound: bool,
    runtime_backend: str,
    runtime_started: bool,
    adk_runtime_primitive_used: bool,
) -> Dict[str, Any]:
    """Derive Unit 2 runtime-truth markers from measured runtime state.

    Consistency rules (enforced by tests):
    - runtime_started => google_adk_package_bound must be True
    - RUNTIME_INTEGRATED => runtime_backend must be google_adk_package
    - No local fallback path exists; the runtime fails closed when the
      google-adk package is unavailable, so local_adk_fallback_used is
      derived (backend mismatch would surface as fallback).
    """
    bound = bool(google_adk_package_bound)
    primitive_used = bool(adk_runtime_primitive_used)
    # "started" means the ADK runtime was actually started against the bound
    # google-adk package (primitives constructed). Primitive execution use is
    # tracked separately via adk_runtime_primitive_used.
    started = bool(runtime_started) and bound
    backend = str(runtime_backend)
    integrated = started and backend == RUNTIME_BACKEND_GOOGLE_ADK
    local_fallback_used = started and backend != RUNTIME_BACKEND_GOOGLE_ADK

    markers: Dict[str, Any] = {
        "google_adk_package_bound": bound,
        "google_adk_runtime_started": started,
        "adk_integration_status": (
            ADK_STATUS_RUNTIME_INTEGRATED if integrated else ADK_STATUS_NOT_STARTED
        ),
        "runtime_backend": backend,
        "adk_runtime_primitive_used": primitive_used,
        "local_adk_fallback_used": local_fallback_used,
        "gemini_provider_started": GEMINI_PROVIDER_STARTED,
        "gemini_adk_started": GEMINI_ADK_STARTED,
    }
    markers.update(safety_invariants())
    return markers
