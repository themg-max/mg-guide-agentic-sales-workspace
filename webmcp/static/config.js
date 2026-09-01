// Runtime configuration shim for the MG Guide WebMCP frontend.
//
// Public/local default is same-origin. The A.I. Rolodex host integration may
// replace only this host-specific file with the approved public backend URL,
// while keeping index.html, app.js, and style.css byte-for-byte aligned with
// the public MG Guide repository source.
(function () {
  "use strict";
  if (typeof window.MG_GUIDE_WEBMCP_API_BASE !== "string") {
    window.MG_GUIDE_WEBMCP_API_BASE = "";
  }
})();
