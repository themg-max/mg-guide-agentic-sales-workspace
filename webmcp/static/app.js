// MG Guide WebMCP Challenge competition adapter frontend.
//
// This file registers real browser-native WebMCP tools via
// document.modelContext.registerTool when the API is available. It does not
// polyfill or emulate WebMCP support: if the API is absent, tools are simply
// not registered and the page falls back to the human-operable buttons only.
//
// Hosting topology (production):
//   A.I. Rolodex landing site  ->  /mg-guide/  (this page)
//   -> document.modelContext.registerTool(...)
//   -> bounded MG Guide WebMCP backend (MG_GUIDE_WEBMCP_API_BASE)
//
// STATE: the page holds currentWebMCPState in JavaScript memory. The backend
// is stateless. get_current_follow_up_state and get_follow_up_draft read only
// from browser memory — they never call the server.

(function () {
  "use strict";

  // API base: production sets window.MG_GUIDE_WEBMCP_API_BASE (no trailing slash).
  // Same-origin empty string is the local/default fallback when frontend and
  // backend are served together (python -m mg_guide.webmcp.server).
  const API_BASE = (
    typeof window.MG_GUIDE_WEBMCP_API_BASE === "string"
      ? window.MG_GUIDE_WEBMCP_API_BASE
      : ""
  ).replace(/\/$/, "");

  /** @type {object|null} Browser-held WebMCP state. Null = NOT_PROCESSED. */
  let currentWebMCPState = null;

  const els = {
    status: document.getElementById("webmcp-status"),
    processing: document.getElementById("processing-state"),
    meetingSummary: document.getElementById("meeting-summary"),
    relationshipStatus: document.getElementById("relationship-status"),
    nextStep: document.getElementById("next-step"),
    draftBody: document.getElementById("draft-body"),
    toolList: document.getElementById("tool-list"),
  };

  function setText(el, text, className) {
    el.textContent = text;
    el.className = className || "";
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str == null ? "" : String(str);
    return div.innerHTML;
  }

  function renderState(state) {
    if (!state || state.status === "NOT_PROCESSED" || !state.ux_state) {
      setText(els.processing, "NOT_PROCESSED — no meeting has been run yet.");
      setText(els.meetingSummary, "—");
      setText(els.relationshipStatus, "—");
      setText(els.nextStep, "—");
      els.draftBody.innerHTML = "<p>—</p>";
      return;
    }
    const completed = state.ux_state === "COMPLETED";
    setText(
      els.processing,
      state.ux_state + " (workflow_status=" + state.workflow_status + ")",
      completed ? "state-completed" : "state-needs-review"
    );
    setText(els.meetingSummary, state.meeting_summary || "No summary available.");
    setText(
      els.relationshipStatus,
      (state.relationship_status || "unknown") +
        " — CRM note: " +
        (state.crm_note_status || "unknown")
    );
    setText(els.nextStep, state.salesperson_next_step || "No next step recorded.");
    renderDraftFromState(state);
  }

  function renderDraftFromState(state) {
    const draft = state && state.follow_up_draft;
    if (!draft || draft.status !== "READY") {
      els.draftBody.innerHTML =
        "<p><strong>NOT_AVAILABLE</strong> — RELATIONSHIP_REVIEW_REQUIRED. " +
        "No follow-up draft can be produced until relationship identity is " +
        "confirmed.</p>";
      return;
    }
    els.draftBody.innerHTML =
      "<p><strong>To:</strong> " +
      escapeHtml(draft.recipient_name || "") +
      "</p>" +
      "<p><strong>Subject:</strong> " +
      escapeHtml(draft.subject || "") +
      "</p>" +
      "<pre>" +
      escapeHtml(draft.body_preview || "") +
      "</pre>" +
      "<p><em>requires_human_send: true — a human must review and send.</em></p>";
  }

  function apiUrl(path) {
    return API_BASE + path;
  }

  async function callAPI(path, options) {
    const resp = await fetch(apiUrl(path), options);
    const body = await resp.json();
    if (!resp.ok) {
      const err = new Error(body.error || "request_failed");
      err.body = body;
      throw err;
    }
    return body;
  }

  /**
   * Process a meeting via the bounded backend, store the full safe payload in
   * currentWebMCPState, and update the visible page.
   */
  async function processMeeting(scenario) {
    const result = await callAPI("/webmcp/meeting-follow-up", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario }),
    });
    currentWebMCPState = result;
    renderState(currentWebMCPState);
    // Agent-facing process tool returns the narrow field set (no nested draft body).
    return {
      workflow_status: result.workflow_status,
      ux_state: result.ux_state,
      meeting_summary: result.meeting_summary,
      relationship_status: result.relationship_status,
      salesperson_next_step: result.salesperson_next_step,
      crm_note_status: result.crm_note_status,
      follow_up_draft_status: result.follow_up_draft_status,
    };
  }

  /** Client-only: read currentWebMCPState. Never hits the server. */
  function getCurrentStateFromBrowser() {
    if (!currentWebMCPState) {
      return {
        status: "NOT_PROCESSED",
        message: "No meeting has been processed yet in this session.",
      };
    }
    return {
      status: "PROCESSED",
      workflow_status: currentWebMCPState.workflow_status,
      ux_state: currentWebMCPState.ux_state,
      meeting_summary: currentWebMCPState.meeting_summary,
      relationship_status: currentWebMCPState.relationship_status,
      salesperson_next_step: currentWebMCPState.salesperson_next_step,
      crm_note_status: currentWebMCPState.crm_note_status,
      follow_up_draft_status: currentWebMCPState.follow_up_draft_status,
      cloud_mutation: currentWebMCPState.cloud_mutation || "NONE",
    };
  }

  /** Client-only: read draft projection already stored in currentWebMCPState. */
  function getFollowUpDraftFromBrowser() {
    if (!currentWebMCPState) {
      return { status: "NOT_PROCESSED" };
    }
    const draft = currentWebMCPState.follow_up_draft || {};
    if (draft.status !== "READY") {
      return {
        status: "NOT_AVAILABLE",
        reason: "RELATIONSHIP_REVIEW_REQUIRED",
      };
    }
    return {
      status: "READY",
      recipient_name: draft.recipient_name,
      subject: draft.subject,
      body_preview: draft.body_preview,
      requires_human_send: true,
    };
  }

  // Human-operable buttons — the product works without an agent.
  document.getElementById("btn-success").addEventListener("click", function () {
    processMeeting("SUCCESS").catch(function (e) {
      console.error(e);
    });
  });
  document.getElementById("btn-ambiguous").addEventListener("click", function () {
    processMeeting("AMBIGUOUS_CONTACT").catch(function (e) {
      console.error(e);
    });
  });

  // Initial render: NOT_PROCESSED (browser memory starts empty).
  renderState(null);

  // WebMCP tool registration — real feature detection, no polyfill.
  function registerWebMCPTools() {
    if (
      !(
        window.document &&
        document.modelContext &&
        document.modelContext.registerTool
      )
    ) {
      setText(
        els.status,
        "WebMCP not supported in this browser/agent context. Human controls remain fully usable."
      );
      return;
    }

    const tools = [
      {
        name: "process_meeting_follow_up",
        descriptor: {
          title: "Process MG Guide Meeting Follow-Up",
          description:
            "Runs the MG Guide meeting_follow_up_v1 workflow against a fixed " +
            "synthetic scenario and returns the resulting workflow status, " +
            "relationship status, next step, and follow-up draft status. No " +
            "live CRM effects occur.",
          inputSchema: {
            type: "object",
            properties: {
              scenario: {
                type: "string",
                enum: ["SUCCESS", "AMBIGUOUS_CONTACT"],
              },
            },
            required: ["scenario"],
            additionalProperties: false,
          },
        },
        execute: async function (args) {
          const result = await processMeeting(args.scenario);
          return JSON.stringify(result);
        },
      },
      {
        name: "get_current_follow_up_state",
        descriptor: {
          title: "Get Current MG Guide Follow-Up State",
          description:
            "Returns the current human-visible MG Guide meeting follow-up " +
            "state without rerunning the workflow. Returns NOT_PROCESSED if " +
            "no meeting has been processed yet. Never triggers a provider effect.",
          inputSchema: {
            type: "object",
            properties: {},
            additionalProperties: false,
          },
        },
        execute: async function () {
          const result = getCurrentStateFromBrowser();
          renderState(currentWebMCPState);
          return JSON.stringify(result);
        },
      },
      {
        name: "get_follow_up_draft",
        descriptor: {
          title: "Get MG Guide Follow-Up Draft",
          description:
            "Returns the deterministic follow-up draft already produced by " +
            "MG Guide's existing projection for the last processed scenario. " +
            "Returns NOT_AVAILABLE with reason RELATIONSHIP_REVIEW_REQUIRED " +
            "when relationship identity was ambiguous. Never sends email or " +
            "invents new content.",
          inputSchema: {
            type: "object",
            properties: {},
            additionalProperties: false,
          },
        },
        execute: async function () {
          const result = getFollowUpDraftFromBrowser();
          if (currentWebMCPState) {
            renderDraftFromState(currentWebMCPState);
          }
          return JSON.stringify(result);
        },
      },
    ];

    const registeredNames = [];
    for (let i = 0; i < tools.length; i++) {
      const tool = tools[i];
      document.modelContext.registerTool({
        name: tool.name,
        title: tool.descriptor.title,
        description: tool.descriptor.description,
        inputSchema: tool.descriptor.inputSchema,
        execute: tool.execute,
      });
      registeredNames.push(tool.name);
    }

    setText(
      els.status,
      "WebMCP supported — " + registeredNames.length + " tools registered."
    );
    els.toolList.innerHTML = registeredNames
      .map(function (n) {
        return "<li><code>" + n + "</code></li>";
      })
      .join("");
  }

  registerWebMCPTools();

  // Expose for tests / local debugging only (not secrets).
  window.__MG_GUIDE_WEBMCP = {
    getState: function () {
      return currentWebMCPState;
    },
    getApiBase: function () {
      return API_BASE;
    },
  };
})();
