// MG Guide WebMCP Challenge competition adapter frontend.
//
// This file registers real browser-native WebMCP tools via
// document.modelContext.registerTool when the API is available. It does not
// polyfill or emulate WebMCP support: if the API is absent, tools are simply
// not registered and the page falls back to the human-operable buttons only.
//
// Tools call the same-origin /webmcp/* JSON API, which is a bounded adapter
// over the existing MG Guide meeting_follow_up_v1 workflow. No live CRM
// effects, no raw identifiers, no arbitrary input.

(function () {
  "use strict";

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
      `${state.ux_state} (workflow_status=${state.workflow_status})`,
      completed ? "state-completed" : "state-needs-review"
    );
    setText(els.meetingSummary, state.meeting_summary || "No summary available.");
    setText(
      els.relationshipStatus,
      `${state.relationship_status || "unknown"} — CRM note: ${
        state.crm_note_status || "unknown"
      }`
    );
    setText(els.nextStep, state.salesperson_next_step || "No next step recorded.");
    renderDraftStatus(state.follow_up_draft_status);
  }

  function renderDraftStatus(status) {
    if (status === "READY") {
      els.draftBody.innerHTML =
        "<p>Draft is ready. Use the agent's get_follow_up_draft tool, " +
        "or refresh, to view the recipient/subject/body preview.</p>";
    } else {
      els.draftBody.innerHTML =
        "<p><strong>NOT_AVAILABLE</strong> — RELATIONSHIP_REVIEW_REQUIRED. " +
        "No follow-up draft can be produced until relationship identity is " +
        "confirmed.</p>";
    }
  }

  function renderDraft(draft) {
    if (!draft || draft.status !== "READY") {
      renderDraftStatus(draft && draft.status);
      return;
    }
    els.draftBody.innerHTML = `
      <p><strong>To:</strong> ${escapeHtml(draft.recipient_name || "")}</p>
      <p><strong>Subject:</strong> ${escapeHtml(draft.subject || "")}</p>
      <pre>${escapeHtml(draft.body_preview || "")}</pre>
      <p><em>requires_human_send: true — a human must review and send.</em></p>
    `;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  async function callAPI(path, options) {
    const resp = await fetch(path, options);
    const body = await resp.json();
    if (!resp.ok) {
      const err = new Error(body.error || "request_failed");
      err.body = body;
      throw err;
    }
    return body;
  }

  async function processMeeting(scenario) {
    const result = await callAPI("/webmcp/meeting-follow-up", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario }),
    });
    renderState(result);
    return result;
  }

  async function getCurrentState() {
    const result = await callAPI("/webmcp/state", { method: "GET" });
    renderState(result);
    return result;
  }

  async function getFollowUpDraft() {
    const result = await callAPI("/webmcp/follow-up-draft", { method: "GET" });
    renderDraft(result);
    return result;
  }

  // Human-operable buttons — the product works without an agent.
  document.getElementById("btn-success").addEventListener("click", () => {
    processMeeting("SUCCESS").catch((e) => console.error(e));
  });
  document.getElementById("btn-ambiguous").addEventListener("click", () => {
    processMeeting("AMBIGUOUS_CONTACT").catch((e) => console.error(e));
  });

  // Initial state on load.
  getCurrentState().catch(() => {
    /* NOT_PROCESSED is expected on a fresh process */
  });

  // WebMCP tool registration — real feature detection, no polyfill.
  function registerWebMCPTools() {
    if (!(window.document && document.modelContext && document.modelContext.registerTool)) {
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
        execute: async ({ scenario }) => {
          const result = await processMeeting(scenario);
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
          inputSchema: { type: "object", properties: {}, additionalProperties: false },
        },
        execute: async () => {
          const result = await getCurrentState();
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
          inputSchema: { type: "object", properties: {}, additionalProperties: false },
        },
        execute: async () => {
          const result = await getFollowUpDraft();
          return JSON.stringify(result);
        },
      },
    ];

    const registeredNames = [];
    for (const tool of tools) {
      document.modelContext.registerTool({
        name: tool.name,
        ...tool.descriptor,
        execute: tool.execute,
      });
      registeredNames.push(tool.name);
    }

    setText(
      els.status,
      `WebMCP supported — ${registeredNames.length} tools registered.`
    );
    els.toolList.innerHTML = registeredNames
      .map((n) => `<li><code>${n}</code></li>`)
      .join("");
  }

  registerWebMCPTools();
})();
