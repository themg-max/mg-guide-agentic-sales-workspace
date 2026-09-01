# Demo Capture Checklist

Use this checklist immediately before and during recording the WebMCP
Challenge demo video.

## Environment

- [ ] Clean browser profile (no unrelated tabs, bookmarks bar, or extensions
      visible)
- [ ] No private tabs open (no private governance tooling, terminals, or
      internal dashboards visible)
- [ ] No credentials visible anywhere on screen (browser autofill, saved
      passwords, tokens, `.env` files)
- [ ] Live URL ready: `https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/`
- [ ] WebMCP-enabled client ready (Chrome with WebMCP flags enabled, or a
      supported WebMCP agent client)

## Discovery

- [ ] Exactly 3 tools visible/discoverable via
      `document.modelContext.getTools()` (or client tool list)

## SUCCESS flow

- [ ] Page reset to a clean pre-run state before recording
- [ ] SUCCESS invocation prepared (`process_meeting_follow_up` with
      `{"scenario": "SUCCESS"}`) via the agent/client path
- [ ] `COMPLETED` state visible after invocation
- [ ] Follow-up draft `READY` visible
- [ ] `requires_human_send: true` visible and explained on camera

## AMBIGUOUS_CONTACT flow

- [ ] Page reset to a clean pre-run state before recording
- [ ] AMBIGUOUS_CONTACT invocation prepared (`process_meeting_follow_up`
      with `{"scenario": "AMBIGUOUS_CONTACT"}`) via the agent/client path
- [ ] `NEEDS_REVIEW` state visible after invocation
- [ ] `RELATIONSHIP_REVIEW_REQUIRED` / `NOT_AVAILABLE` draft notice visible

## Narration content

- [ ] Zero-effect statement said on camera (no CRM writes, no emails sent)
- [ ] Human-send boundary explained on camera

## Recording quality

- [ ] Microphone/audio tested before the real take
- [ ] Duration under 3:00 (hard limit)
- [ ] Target final cut 2:30–2:40
- [ ] No dead loading time in the final cut (trim in editing)

## Content boundary

- [ ] No private or customer data visible anywhere in the recording
- [ ] No unsupported claims made in narration (see
      [`SUBMISSION_PACKET.md`](SUBMISSION_PACKET.md) for the frozen claim set)

## After recording

- [ ] Final public YouTube upload remains a separate human action (not
      performed by this checklist or any automated step)
