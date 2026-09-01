"""Standalone HTTP server for the public WebMCP competition surface.

Serves:
  - the WebMCPSurfaceApp JSON API (see app.py) under /health, /webmcp/*
  - the static WebMCP frontend (webmcp/static/) at /

Uses only the Python standard library, matching the existing judge_surface
server pattern.

Local default: WEBMCP_CORS_MODE=local (unless already set). Production Cloud
Run images should set WEBMCP_CORS_MODE=production explicitly.
"""

from __future__ import annotations

import mimetypes
import os
import sys
from pathlib import Path
from typing import Optional
from wsgiref.simple_server import make_server

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from mg_guide.webmcp.app import WebMCPSurfaceApp  # noqa: E402

STATIC_DIR = REPO_ROOT / "webmcp" / "static"


class StaticAndAPIApp:
    """Dispatches static frontend files and the WebMCP JSON API."""

    def __init__(self) -> None:
        self._api = WebMCPSurfaceApp()

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        if path == "/" or (
            not path.startswith("/webmcp/")
            and path not in ("/health", "/healthz")
            and not path.startswith("/api/")
        ):
            return self._serve_static(path, start_response)
        return self._api(environ, start_response)

    def _serve_static(self, path: str, start_response):
        if path == "/":
            path = "/index.html"
        candidate = (STATIC_DIR / path.lstrip("/")).resolve()
        if STATIC_DIR not in candidate.parents and candidate != STATIC_DIR:
            start_response("403 Forbidden", [("Content-Type", "text/plain")])
            return [b"forbidden"]
        if not candidate.is_file():
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"not found"]
        body = candidate.read_bytes()
        content_type = (
            mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
        )
        start_response(
            "200 OK",
            [
                ("Content-Type", content_type),
                ("Content-Length", str(len(body))),
                ("Cache-Control", "no-store"),
            ],
        )
        return [body]


def main(argv: Optional[list[str]] = None) -> int:
    # Local server defaults to local CORS so same-machine browser testing works.
    # Production containers set WEBMCP_CORS_MODE=production in the Dockerfile.
    os.environ.setdefault("WEBMCP_CORS_MODE", "local")
    port = int(os.environ.get("PORT", "8080"))
    app = StaticAndAPIApp()
    server = make_server("0.0.0.0", port, app)
    print(f"mg-guide-webmcp-competition listening on 0.0.0.0:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("shutting down", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
