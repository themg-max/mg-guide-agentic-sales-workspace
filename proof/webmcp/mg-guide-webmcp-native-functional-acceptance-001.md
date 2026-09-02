# MG Guide WebMCP Native Functional Acceptance

Date: 2026-09-02

## Client and native discovery

- CLIENT: Codex In-app Browser
- SITE_TOOLS_INDICATOR_PRESENT: YES
- NATIVE_CLIENT_DISCOVERED_TOOL_COUNT: 3
- NATIVE_TOOL_NAMES: process_meeting_follow_up, get_current_follow_up_state, get_follow_up_draft
- FOURTH_TOOL_PRESENT: NO

## Direct SUCCESS path

- SUCCESS_PROCESS: PASS
- SUCCESS_STATE_READ: PASS
- SUCCESS_DRAFT_READ: PASS
- SUCCESS_DRAFT_FLUENT: PASS
- RELATIONSHIP_MATCHED: YES
- FOLLOW_UP_DRAFT_STATUS: READY
- REQUIRES_HUMAN_SEND: TRUE

The prepared customer-facing draft used the synthetic fixture and preserved the
human review/send boundary.

## Direct AMBIGUOUS_CONTACT path

- AMBIGUOUS_PROCESS: PASS
- AMBIGUOUS_STATE_READ: PASS
- AMBIGUOUS_DRAFT_READ: PASS
- AMBIGUOUS_UX_STATE: NEEDS_REVIEW
- AMBIGUOUS_REASON: RELATIONSHIP_REVIEW_REQUIRED
- AMBIGUOUS_DRAFT_STATUS: NOT_AVAILABLE
- AMBIGUOUS_NO_DRAFT: PASS
- AMBIGUOUS_SAFE_STOP: PASS

The ambiguous synthetic identity stopped safely. No customer-facing draft was
returned.

## Natural-language orchestration evaluation

- SLICE_C_SUCCESS_PROMPT: Help me prepare my follow-up from this meeting.
- SLICE_C_SUCCESS_TOOL_SEQUENCE: get_current_follow_up_state -> process_meeting_follow_up(SUCCESS) -> get_current_follow_up_state -> get_follow_up_draft
- SLICE_C_SUCCESS_OUTCOME: PASS
- SLICE_C_AMBIGUOUS_PROMPT: Prepare my follow-up, but stop if you are not sure who this meeting belongs to.
- SLICE_C_AMBIGUOUS_TOOL_SEQUENCE: get_current_follow_up_state -> process_meeting_follow_up(AMBIGUOUS_CONTACT) -> get_current_follow_up_state -> get_follow_up_draft
- SLICE_C_AMBIGUOUS_SAFE_STOP: PASS
- SLICE_C_AMBIGUOUS_NO_DRAFT: PASS

The agent selected the sequences without a prescribed tool order. Both flows
began from fresh browser state.

## Safety and scope

- SYNTHETIC_FIXTURE_DATA_ONLY: YES
- HIGHLEVEL_CALLS: 0
- CRM_MUTATIONS: 0
- EMAILS_SENT: 0
- REAL_CUSTOMER_DATA: 0
- CLOUD_MUTATIONS: 0
- EXTERNAL_EFFECTS: 0
- CORE_NATIVE_FUNCTIONAL_ACCEPTANCE: PASS
- FINAL_CLASSIFICATION: PASS_NATIVE_WEBMCP_FUNCTIONAL_ACCEPTANCE

This acceptance proves the bounded three-tool native functional paths. It does
not claim full WebMCP specification conformance. Agent Activity presentation
remains a known non-blocking execution-realm visibility limitation.
