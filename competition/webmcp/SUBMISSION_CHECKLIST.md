# WebMCP Challenge — Final Submission Checklist

```text
STATUS=SUBMISSION_PACKAGING_IN_PROGRESS
LAST_UPDATED=2026-09-03
DEADLINE_PT=2026-09-03T13:00:00-07:00
DEADLINE_ET=2026-09-03T16:00:00-04:00
LIVE_PRODUCT_URL=https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
PUBLIC_REPO=https://github.com/themg-max/mg-guide-agentic-sales-workspace
```

This checklist separates already-proven WebMCP implementation from the final
runtime-freeze and submission operations that must still be completed before
the deadline.

## 1. Competition implementation

- [x] `WEB_APP_POWERED_BY_WEBMCP`
- [x] `DOCUMENT_MODELCONTEXT_REGISTERTOOL_PRESENT`
- [x] `EXACTLY_THREE_TOOLS`
  - [x] `process_meeting_follow_up`
  - [x] `get_current_follow_up_state`
  - [x] `get_follow_up_draft`
- [x] `ACTION_STATE_ARTIFACT_PATTERN`
- [x] `SUCCESS_FLOW_IMPLEMENTED`
- [x] `AMBIGUOUS_CONTACT_FAIL_CLOSED_IMPLEMENTED`
- [x] `REQUIRES_HUMAN_SEND_TRUE`
- [x] `SYNTHETIC_ONLY_DEMO_BOUNDARY`
- [x] `ZERO_LIVE_CRM_EMAIL_EFFECT_DESIGN`
- [x] `WEBMCP_SPECIFIC_TESTS_PRESENT`
- [x] `PUBLIC_IMPLEMENTATION_VISIBLE`

## 2. Existing-project competition delta

- [x] `APP_STATUS=Existing`
- [x] Pre-existing MG Guide capabilities explicitly separated from new WebMCP work
- [x] WebMCP work added after the Aug 25 submission-period start
- [x] Dated public commit/PR history preserved
- [x] `competition/webmcp/COMPETITION_DELTA.md` documents the boundary
- [x] Judge-facing repo copy does not claim the broader MG Guide system was built during this challenge

## 3. Public repository

- [x] Repository is public
- [x] Apache-2.0 license is detected by GitHub
- [x] WebMCP source registration is easy to find
- [x] Root README routes WebMCP judges to a dedicated competition start page **on the packaging branch**
- [x] `competition/webmcp/README.md` judge-first start page created **on the packaging branch**
- [x] Judge testing uses current official browser instructions **on the packaging branch**
- [x] Demo script exercises ACTION + STATE + ARTIFACT **on the packaging branch**
- [ ] Packaging PR merged to `main`
- [ ] Public repo verified logged out/incognito after packaging merge
- [ ] GitHub About description aligned with WebMCP submission
- [ ] GitHub homepage set to the live MG Guide URL
- [ ] License visibly detected in GitHub About panel after final repo check

Recommended manual GitHub About values:

```text
Description:
MG Guide — agent-native meeting follow-up with WebMCP ACTION / STATE / ARTIFACT tools and human send control.

Website:
https://ai-rolodex-landing-831270426395.us-east4.run.app/mg-guide/
```

## 4. Live runtime and final freeze

Historical production/native acceptance exists, but the final judge-facing
runtime must be revalidated and frozen after the current judge-render repair
before submission.

- [x] Dedicated bounded WebMCP backend deployed historically
- [x] Native WebMCP discovery/invocation proven historically
- [x] SUCCESS and AMBIGUOUS paths proven historically
- [x] Exactly three native tools proven historically
- [ ] Current repaired frontend candidate acceptance `PASS`
- [ ] Current repaired frontend promoted to normal production traffic
- [ ] Final live URL opened in a fresh/incognito WebMCP-capable browser
- [ ] Returning/stale-cache browser render check `PASS`
- [ ] Narrow in-app/browser render check `PASS`
- [ ] Native WebMCP tool count still exactly `3`
- [ ] SUCCESS → STATE → ARTIFACT final smoke `PASS`
- [ ] AMBIGUOUS_CONTACT fail-closed final smoke `PASS`
- [ ] `requires_human_send=true` final readback `PASS`
- [ ] Backend revision/digest unchanged unless separately authorized
- [ ] `HIGHLEVEL_CALLS=0`
- [ ] `CRM_MUTATIONS=0`
- [ ] `EMAILS_SENT=0`
- [ ] `REAL_CUSTOMER_DATA=0`
- [ ] Final frontend revision/image digest recorded
- [ ] `FINAL_RUNTIME_FREEZE=BOUND`

**Stop product mutation once this section passes.**

## 5. Demo video

Official requirement: public YouTube video, under 3 minutes, with audio showing
the project functioning and how WebMCP is used.

- [x] Demo script exists
- [x] Script shows working product immediately
- [x] Script shows exactly three tools
- [x] Script exercises all three tools
- [x] Script shows fail-closed ambiguous behavior
- [x] Script explains why WebMCP is better than DOM guessing / separate agent UI
- [ ] Final runtime freeze complete before recording
- [ ] Video recorded
- [ ] Runtime `< 3:00`
- [ ] Audio clear
- [ ] Project shown working in first 10–15 seconds
- [ ] Native agent actually uses WebMCP tools
- [ ] No credentials/private URLs/private governance in frame
- [ ] No copyrighted music/material without permission
- [ ] Uploaded to YouTube
- [ ] YouTube visibility `Public`
- [ ] Public video link tested logged out

Use:
[`DEMO_SCRIPT_UNDER_3_MIN.md`](DEMO_SCRIPT_UNDER_3_MIN.md)

## 6. Devpost project copy

- [x] Existing Devpost project created: `MG Guide | Agent-Native Follow-Up`
- [x] Project name remains human-selected and unchanged
- [x] Draft description exists
- [x] Revised rubric-aligned draft prepared **on the packaging branch**
- [ ] Devpost project tagline/description updated from final approved draft
- [ ] Live URL field exact
- [ ] Public repo URL exact
- [ ] Existing-project update field explains WebMCP challenge delta
- [ ] Testing instructions pasted
- [ ] Agents/clients tested answer reflects only actual validation
- [ ] AI tools used answer complete and accurate
- [ ] Submitter type provided by human
- [ ] Country/countries provided by human
- [ ] Organization name provided if applicable
- [ ] Learning level provided by human
- [ ] AI career-value answer provided by human
- [ ] Video URL attached

See:
[`DEVPOST_SUBMISSION_DRAFT.md`](DEVPOST_SUBMISSION_DRAFT.md)

## 7. Final submission gate

Before clicking Submit, require:

```text
FINAL_LIVE_RUNTIME_ACCEPTANCE=PASS
FINAL_RUNTIME_FREEZE=BOUND
PUBLIC_REPO_PACKAGING_MERGED=YES
PUBLIC_REPO_LOGGED_OUT_CHECK=PASS
OPEN_SOURCE_LICENSE_VISIBLE=PASS
LIVE_URL_LOGGED_OUT_CHECK=PASS
WEBMCP_NATIVE_TOOL_COUNT=3
SUCCESS_FINAL_SMOKE=PASS
AMBIGUOUS_FINAL_SMOKE=PASS
VIDEO_PUBLIC_YOUTUBE=YES
VIDEO_RUNTIME_LT_3_MIN=YES
VIDEO_AUDIO=PASS
DEVPOST_REQUIRED_FIELDS_COMPLETE=YES
```

Then verify the project is marked **Submitted**, not Draft.

## 8. Post-deadline freeze

Once the submission period closes at 1:00 PM PT / 4:00 PM ET:

- do not edit the submitted Devpost submission;
- do not modify the submitted public repository;
- do not change the submitted live site;
- do not replace or edit the submitted video;
- keep the project free, accessible, and functioning for judges through the
  judging period.

If continued development is necessary after the deadline, do it on a separate
copy/fork that does not alter the submitted repo/live project.
