"""Standalone HTTP server entry point for the judge-safe demo surface.

This module is intentionally small and uses only the Python standard library
so the container image has no additional web-framework dependency.
"""

from __future__ import annotations

import os
import sys
import logging
from pathlib import Path
from typing import Optional
from wsgiref.simple_server import make_server

# Ensure src/ is on PYTHONPATH for container-local execution.
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from mg_guide.judge_surface.app import JudgeSurfaceApp  # noqa: E402


def main(argv: Optional[list[str]] = None) -> int:
    port = int(os.environ.get("PORT", "8080"))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    app = JudgeSurfaceApp()
    server = make_server("0.0.0.0", port, app)
    print(f"mg-guide-judge-surface listening on 0.0.0.0:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("shutting down", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
