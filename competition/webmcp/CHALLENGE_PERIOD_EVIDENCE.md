# WebMCP Challenge — Challenge-Period Evidence Ledger

```text
SUBMISSION_PERIOD_START=2026-08-25T11:00:00-07:00
SUBMISSION_PERIOD_END=2026-09-03T13:00:00-07:00
PROJECT_STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
PRE_WEBMCP_BASELINE_SHA=bc9a723f84e72ec3605da495ad16fbf78f3a99a9
PRE_WEBMCP_BASELINE_DATE=2026-08-31T19:16:51-04:00
PACKAGING_BASE_SHA=8a9df7178e20fe8f3faf642ddf09858f6716e5da
```

This ledger is a concise judge-facing companion to
[`COMPETITION_DELTA.md`](COMPETITION_DELTA.md). It exists to make one point easy
to verify: **MG Guide is an existing project, and the WebMCP submission is a
meaningful additive extension implemented during the WebMCP Challenge
submission period.**

The broader MG Guide workflow/agents are not claimed as new challenge work.

---

## Pre-existing baseline

The repository records `bc9a723f84e72ec3605da495ad16fbf78f3a99a9`
(August 31, 2026) as the MG Guide baseline before the WebMCP competition delta.
Pre-existing capabilities include:

- `meeting_follow_up_v1` workflow;
- Meeting Context Agent;
- Relationship Context Agent;
- Follow-Up Planning Agent;
- deterministic policy;
- Google Workspace integration;
- existing MG Guide / A.I. Rolodex product direction and hosting surface.

See [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) for the full baseline.

---

## Challenge-period implementation evidence

| Date (ET) | Commit / PR | Challenge-period contribution |
| --- | --- | --- |
| Sep 1, 12:18 | `930bfa16ce518398e3a6de3cf5a6f1bcb3b5b087` | Initial bounded WebMCP competition adapter: browser frontend, stateless/synthetic backend package, exactly three native tool registrations, WebMCP tests, deployment packaging, competition docs |
| Sep 1, 15:02 | `7c5436abc281c8f3592f7276bcb21f1a6cf0c2d9` | Stateless backend/browser-state correction, CORS boundary, host topology, corrected native-vs-mocked proof semantics |
| Sep 1, 15:19 | `142c88561f01a12bc731d2d3584a816232c54c66` | Subpath-safe frontend assets for `/mg-guide/` host integration |
| Sep 1, 15:24 | PR #432 merge `2847f5a26dbc61716736b60eedb66e399c102a33` | Merged initial WebMCP adapter onto public `main` |
| Sep 1, 18:43 | PR #437 merge `d7c702bf4df174260266f5e359ba7035d0f6a1fa` | Reconciled production acceptance, live product state, native discovery/invocation proof, and judge testing |
| Sep 1, 19:46 | PR #438 merge `80ca3c10959d3a1f6cd55b5da836ceb6a334f5d6` | Added/finalized WebMCP submission packet, demo script, capture checklist, and Devpost draft |
| Sep 2, 00:22 | PR #439 merge `4b1e58046fa529c1d9a5df489c2aab8698544dc1` | Improved deterministic customer-facing SUCCESS draft quality while preserving three-tool/human-send/zero-effect contracts |
| Sep 2, 01:26 | PR #441 merge `dd2d1b285c1104ca6d34dca82cca7517ee25fa44` | Added browser-local Agent Activity presentation and explicit ACTION / STATE / ARTIFACT capability framing without adding tools |
| Sep 2, 03:46 | PR #442 merge `a87b2bca4d2c3409396d7140c2a366ad8faa063d` | Fixed multi-run/latest-workflow presentation semantics to prevent stale state |
| Sep 2, 15:59 | PR #443 merge `474a1c9ab31b70a0f68ff40a69e5310e65a04e0a` | Added public-safe native functional acceptance evidence for exactly three tools, SUCCESS, AMBIGUOUS safe stop, human-send boundary, and zero external effects |
| Sep 2, 18:43 | PR #444 merge `8a9df7178e20fe8f3faf642ddf09858f6716e5da` | Elevated the MG Guide judge-facing frontend presentation while preserving the accepted runtime/tool contract |

All of the above occurred after the August 25 submission-period start.

---

## Meaningful extension summary

The WebMCP work is not a label or thin wrapper placed on the pre-existing MG
Guide product. The challenge-period delta added a new browser-agent interaction
model and the supporting product/test/deployment surface:

```text
Existing MG Guide capability
        ↓
bounded WebMCP adapter
        ↓
exactly 3 native browser tools
        ↓
ACTION / STATE / ARTIFACT
        ↓
shared human-visible browser state
        ↓
native browser discovery + invocation
        ↓
SUCCESS + fail-closed AMBIGUOUS behavior
        ↓
human final authority
```

The challenge work therefore changes **how an agent can safely interact with
the web product**, not merely how the existing functionality is described.

---

## Exactly three tools added for the WebMCP experience

1. `process_meeting_follow_up`
2. `get_current_follow_up_state`
3. `get_follow_up_draft`

The current challenge surface intentionally does not add an email-send, CRM
write, credentials, live-mode, or arbitrary-input tool.

---

## Where judges can verify the delta

- Source registration: [`../../webmcp/static/app.js`](../../webmcp/static/app.js)
- Bounded adapter: [`../../src/mg_guide/webmcp/`](../../src/mg_guide/webmcp/)
- Tests: [`../../tests/webmcp/`](../../tests/webmcp/)
- Full boundary: [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md)
- Native production proof: [`../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md)
- Judge journey: [`JUDGE_TESTING.md`](JUDGE_TESTING.md)

This ledger documents competition-period implementation history only. It does
not assert that every broader MG Guide capability shown in the repository was
created during The WebMCP Challenge.
