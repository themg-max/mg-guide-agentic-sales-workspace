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

  // ---------------------------------------------------------------------
  // Agent activity ledger (Competition Elevation Plan Slice A).
  //
  // Ephemeral, browser-local, in-memory only. Never persisted, never sent
  // to a backend. Separate from currentWebMCPState (which holds workflow
  // data, not activity history).
  //
  // Every recorded event must trace to something actually observed: a real
  // tool execute() call, a real tool result, a real human button click, or
  // a real derived workflow-state transition. This file must never
  // synthesize an event describing agent reasoning that was not directly
  // observed (e.g. "Agent decided..." or "Agent discovered tools..." are
  // never recorded here).
  // ---------------------------------------------------------------------
  let currentWebMCPActivity = [];
  let activitySequence = 0;

  /**
   * Record one activity event. actor must be one of AGENT | HUMAN | SYSTEM.
   * source documents where the fact came from (tool_call, tool_result,
   * human_action, derived_state) so every rendered line is traceable.
   */
  function recordActivity(actor, event, source, tool, status, message) {
    activitySequence += 1;
    currentWebMCPActivity.push({
      sequence: activitySequence,
      actor: actor,
      event: event,
      source: source,
      tool: tool || null,
      status: status || "OK",
      message: message,
    });
    renderActivity();
  }

  const els = {
    status: document.getElementById("webmcp-status"),
    workflowStateLabel: document.getElementById("workflow-state-label"),
    stepMeetingStatus: document.getElementById("step-meeting-status"),
    stepRelationshipStatus: document.getElementById("step-relationship-status"),
    stepPlanStatus: document.getElementById("step-plan-status"),
    stepDraftStatus: document.getElementById("step-draft-status"),
    stepHumanStatus: document.getElementById("step-human-status"),
    trustDetail: document.getElementById("trust-detail"),
    humanReviewMessage: document.getElementById("human-review-message"),
    processing: document.getElementById("processing-state"),
    meetingSummary: document.getElementById("meeting-summary"),
    relationshipStatus: document.getElementById("relationship-status"),
    nextStep: document.getElementById("next-step"),
    draftBody: document.getElementById("draft-body"),
    toolList: document.getElementById("tool-list"),
    activityList: document.getElementById("activity-list"),
    activitySummary: document.getElementById("activity-summary"),
    activityHandoff: document.getElementById("activity-handoff"),
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

  /** Map canonical workflow state into presentation-only workspace labels. */
  function renderWorkflowPresentation(state) {
    const waiting = !state || state.status === "NOT_PROCESSED" || !state.ux_state;
    const completed = !waiting && state.ux_state === "COMPLETED";

    document.body.setAttribute(
      "data-workflow-presentation",
      waiting ? "waiting" : completed ? "success" : "ambiguous"
    );

    if (waiting) {
      setText(els.workflowStateLabel, "WAITING", "workflow-state");
      setText(els.stepMeetingStatus, "WAITING");
      setText(els.stepRelationshipStatus, "WAITING");
      setText(els.stepPlanStatus, "WAITING");
      setText(els.stepDraftStatus, "NOT AVAILABLE");
      setText(els.stepHumanStatus, "REQUIRED");
      setText(
        els.trustDetail,
        "No meeting has been processed. The human review boundary is already active."
      );
      setText(
        els.humanReviewMessage,
        "Workflow has not run. Human authority remains required for every follow-up."
      );
      return;
    }

    setText(
      els.workflowStateLabel,
      completed ? "COMPLETED" : "SAFE STOP",
      "workflow-state"
    );
    setText(els.stepMeetingStatus, "READY");
    setText(els.stepRelationshipStatus, completed ? "MATCHED" : "NEEDS REVIEW");
    setText(els.stepPlanStatus, completed ? "PREPARED" : "BLOCKED");
    setText(els.stepDraftStatus, completed ? "READY" : "NOT AVAILABLE");
    setText(els.stepHumanStatus, "REQUIRED");
    setText(
      els.trustDetail,
      completed
        ? "A fluent follow-up is prepared for human review. MG Guide does not send it."
        : "Relationship identity requires review. Draft preparation stopped safely."
    );
    setText(
      els.humanReviewMessage,
      completed
        ? "Review the prepared follow-up and decide whether to send it."
        : "Confirm the relationship identity before follow-up preparation can continue."
    );
  }

  function renderState(state) {
    renderWorkflowPresentation(state);
    if (!state || state.status === "NOT_PROCESSED" || !state.ux_state) {
      setText(els.processing, "NOT_PROCESSED — no meeting has been run yet.");
      setText(els.meetingSummary, "Waiting for synthetic meeting context.");
      setText(els.relationshipStatus, "Waiting for relationship resolution.");
      setText(els.nextStep, "Waiting for a governed next step.");
      els.draftBody.innerHTML =
        '<p class="waiting-copy">No draft is available until a meeting is processed.</p>';
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

  // Icon per event: agent/system completed steps get a check, a review-
  // required step gets "!", a withheld/stopped step gets a block glyph.
  const ACTIVITY_ICON = {
    STATE_READ: "\u2713",
    WORKFLOW_PROCESS: "\u2713",
    RELATIONSHIP_MATCHED: "\u2713",
    DRAFT_READY: "\u2713",
    DRAFT_READ: "\u2713",
    RELATIONSHIP_REVIEW_REQUIRED: "!",
    SAFE_STOP: "\u25A0",
    HUMAN_HANDOFF_REQUIRED: null, // rendered separately, not as a list line
    WEBMCP_AVAILABLE: "\u2713",
  };

  const ACTOR_LABEL = {
    AGENT: "Agent",
    HUMAN: "Human",
    SYSTEM: "System",
  };

  /**
   * Derive summary and handoff presentation for only the latest workflow.
   * The activity list deliberately remains cumulative browser-session history.
   * A WORKFLOW_PROCESS event starts a fresh presentation segment so an older
   * safe stop or handoff cannot describe a later workflow.
   */
  function deriveLatestWorkflowPresentation(activity) {
    let handoffMessage = "";
    let safeStopped = false;
    let draftReady = false;
    let workflowInitiator = null;

    for (let i = 0; i < activity.length; i++) {
      const item = activity[i];
      if (item.event === "WORKFLOW_PROCESS") {
        workflowInitiator = item.actor;
        safeStopped = false;
        draftReady = false;
        handoffMessage = "";
        continue;
      }
      if (workflowInitiator === null) {
        continue;
      }
      if (item.event === "HUMAN_HANDOFF_REQUIRED") {
        handoffMessage = item.message;
      } else if (item.event === "SAFE_STOP") {
        safeStopped = true;
      } else if (item.event === "DRAFT_READY") {
        draftReady = true;
      }
    }

    if (safeStopped) {
      return {
        summary: "Stopped safely",
        summaryClass: "activity-stopped",
        handoffMessage: handoffMessage,
      };
    }
    if (draftReady && workflowInitiator === "HUMAN") {
      return {
        summary: "Human-run workflow complete",
        summaryClass: "activity-complete",
        handoffMessage: handoffMessage,
      };
    }
    if (draftReady && workflowInitiator === "AGENT") {
      return {
        summary: "Agent work complete",
        summaryClass: "activity-complete",
        handoffMessage: handoffMessage,
      };
    }
    return {
      summary: "",
      summaryClass: "",
      handoffMessage: handoffMessage,
    };
  }

  /**
   * Render the Agent Activity panel strictly from currentWebMCPActivity.
   * Only events that actually occurred are shown — the panel never
   * pre-renders an expected sequence.
   */
  function renderActivity() {
    if (!els.activityList) {
      return;
    }
    if (currentWebMCPActivity.length === 0) {
      els.activityList.innerHTML =
        '<li class="activity-empty">Waiting for activity. A person can ' +
        "run the demo, or a browser agent can use MG Guide through " +
        "WebMCP.</li>";
      setText(els.activitySummary, "");
      setText(els.activityHandoff, "");
      return;
    }

    const lines = [];

    for (let i = 0; i < currentWebMCPActivity.length; i++) {
      const item = currentWebMCPActivity[i];
      if (item.event === "HUMAN_HANDOFF_REQUIRED") {
        continue;
      }
      const icon = ACTIVITY_ICON[item.event] || "\u2022";
      const actorLabel = ACTOR_LABEL[item.actor] || item.actor;
      lines.push(
        '<li class="activity-item activity-actor-' +
          escapeHtml(item.actor.toLowerCase()) +
          '"><span class="activity-icon">' +
          icon +
          "</span> " +
          escapeHtml(actorLabel) +
          ": " +
          escapeHtml(item.message) +
          "</li>"
      );
    }

    els.activityList.innerHTML = lines.join("");
    const presentation = deriveLatestWorkflowPresentation(currentWebMCPActivity);
    setText(
      els.activitySummary,
      presentation.summary,
      presentation.summaryClass
    );

    setText(
      els.activityHandoff,
      presentation.handoffMessage
        ? "Human action required: " + presentation.handoffMessage
        : ""
    );
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
   *
   * actor documents who/what initiated this call (HUMAN for the demo
   * buttons, AGENT for the WebMCP process_meeting_follow_up tool). This is
   * recorded truthfully in the activity ledger — a human-triggered click is
   * never rendered as agent activity.
   */
  async function processMeeting(scenario, actor) {
    const callActor = actor === "AGENT" ? "AGENT" : "HUMAN";
    if (callActor === "AGENT") {
      recordActivity(
        "AGENT",
        "WORKFLOW_PROCESS",
        "tool_call",
        "process_meeting_follow_up",
        "OK",
        "processed the meeting"
      );
    } else {
      recordActivity(
        "HUMAN",
        "WORKFLOW_PROCESS",
        "human_action",
        null,
        "OK",
        "ran the " + scenario + " demo"
      );
    }
    const result = await callAPI("/webmcp/meeting-follow-up", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario }),
    });
    currentWebMCPState = result;
    renderState(currentWebMCPState);

    // Derived workflow outcomes are SYSTEM events: they describe what the
    // backend actually returned, not agent reasoning.
    if (result.ux_state === "COMPLETED") {
      recordActivity(
        "SYSTEM",
        "RELATIONSHIP_MATCHED",
        "derived_state",
        null,
        "OK",
        "relationship matched"
      );
      if (result.follow_up_draft_status === "READY") {
        recordActivity(
          "SYSTEM",
          "DRAFT_READY",
          "derived_state",
          null,
          "OK",
          "follow-up draft became ready"
        );
      }
      recordActivity(
        "SYSTEM",
        "HUMAN_HANDOFF_REQUIRED",
        "derived_state",
        null,
        "OK",
        "Review and send"
      );
    } else {
      recordActivity(
        "SYSTEM",
        "RELATIONSHIP_REVIEW_REQUIRED",
        "derived_state",
        null,
        "NEEDS_REVIEW",
        "relationship identity requires review"
      );
      recordActivity(
        "SYSTEM",
        "SAFE_STOP",
        "derived_state",
        null,
        "STOPPED",
        "follow-up draft withheld"
      );
      recordActivity(
        "SYSTEM",
        "HUMAN_HANDOFF_REQUIRED",
        "derived_state",
        null,
        "OK",
        "Confirm relationship"
      );
    }

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
    processMeeting("SUCCESS", "HUMAN").catch(function (e) {
      console.error(e);
    });
  });
  document.getElementById("btn-ambiguous").addEventListener("click", function () {
    processMeeting("AMBIGUOUS_CONTACT", "HUMAN").catch(function (e) {
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
      els.status.className = "connection-badge unavailable";
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
          const result = await processMeeting(args.scenario, "AGENT");
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
          recordActivity(
            "AGENT",
            "STATE_READ",
            "tool_call",
            "get_current_follow_up_state",
            "OK",
            "inspected current follow-up state"
          );
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
          recordActivity(
            "AGENT",
            "DRAFT_READ",
            "tool_call",
            "get_follow_up_draft",
            "OK",
            "retrieved the draft"
          );
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
      "WebMCP Connected · " + registeredNames.length + " Native Tools"
    );
    els.status.className = "connection-badge connected";
    // SYSTEM-originated: this only reports that native WebMCP is available
    // and tools were registered by this page. It does NOT claim that any
    // agent has discovered or used them — that requires separate,
    // explicit evidence from a native client (see tool_call events above).
    recordActivity(
      "SYSTEM",
      "WEBMCP_AVAILABLE",
      "system_check",
      null,
      "OK",
      registeredNames.length + " WebMCP tools registered"
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
    getActivity: function () {
      return currentWebMCPActivity.slice();
    },
  };
})();
