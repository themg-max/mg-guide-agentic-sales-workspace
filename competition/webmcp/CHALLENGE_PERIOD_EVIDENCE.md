# WebMCP Challenge — Challenge-Period Evidence Ledger

```text
SUBMISSION_PERIOD_START=2026-08-25T12:00:00-07:00
SUBMISSION_PERIOD_END=2026-09-04T01:00:00-07:00
SUBMISSION_PERIOD_END_ET=2026-09-04T04:00:00-04:00
SUBMISSION_PERIOD_END_UTC=2026-09-04T08:00:00Z
DEADLINE_SOURCE=Devpost 12-hour extension announced 2026-09-03
PROJECT_STATUS=EXISTING_PROJECT_WITH_NEW_WEBMCP_DELTA
PRE_WEBMCP_BASELINE_SHA=bc9a723f84e72ec3605da495ad16fbf78f3a99a9
PRE_WEBMCP_BASELINE_DATE=2026-08-31T19:16:51-04:00
PUBLIC_JUDGE_FRONT_DOOR_SHA=90982f31c099872179a58dd2e9d3a2c6bbf370fb
```

This ledger is the judge-facing evidence companion to
[`COMPETITION_DELTA.md`](COMPETITION_DELTA.md). Its purpose is to make one point
easy to verify: **MG Guide is an existing project, and the WebMCP submission is
a meaningful additive extension implemented during the WebMCP Challenge
submission period.**

The broader MG Guide workflow, agents, deterministic policy, Workspace work,
and cloud architecture are not claimed as newly created for this challenge.

The official challenge deadline was extended by 12 hours on September 3. This
ledger uses the final announced deadline: **September 4 at 1:00 AM PT / 4:00
AM ET**.

---

## Pre-existing baseline

The repository records
`bc9a723f84e72ec3605da495ad16fbf78f3a99a9` (August 31, 2026) as the
**pre-WebMCP implementation baseline** used to measure the public repository
delta. It is not represented as the challenge-start repository snapshot.

Pre-existing capabilities include:

- `meeting_follow_up_v1` workflow;
- Meeting Context Agent;
- Relationship Context Agent;
- Follow-Up Planning Agent;
- deterministic policy;
- existing judge-safe presentation/projection capabilities;
- Google Workspace integration;
- existing MG Guide / A.I. Rolodex product direction and hosting surface;
- broader cloud and CRM integration history.

See [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md) for the full boundary.

---

## Five-layer meaningful extension

The WebMCP challenge work is easiest to evaluate as five additive layers on top
of the existing MG Guide foundation.

| Layer | New challenge-period capability | Judge-verifiable surface |
| --- | --- | --- |
| **1. Browser-agent contract** | Exactly three native WebMCP tools: ACTION / STATE / ARTIFACT, registered with `document.modelContext.registerTool(...)` | `webmcp/static/app.js` |
| **2. New Web product surface** | Human + agent operate on the same visible MG Guide page and browser-held current state | `webmcp/static/index.html`, `webmcp/static/app.js`, presentation tests |
| **3. Bounded WebMCP adapter** | New stateless synthetic-only adapter; SUCCESS + AMBIGUOUS_CONTACT allow-list; authority-bearing fields rejected | `src/mg_guide/webmcp/`, `tests/webmcp/test_webmcp_app.py` |
| **4. Safety + experience model** | Deterministic draft, `requires_human_send=true`, fail-closed ambiguous identity, latest-run state correctness, zero external effects | `src/mg_guide/judge_surface/demo_stages.py`, `tests/judge_surface/test_demo_stages.py`, `tests/webmcp/` |
| **5. Test / deploy / proof surface** | Dedicated WebMCP tests, competition container, host integration, native discovery/invocation proof, judge docs | `tests/webmcp/`, `deployment/webmcp/`, `proof/webmcp/`, `competition/webmcp/` |

The existing workflow/agent/policy foundation remains the reused domain core.
The challenge work changes **how a browser agent can safely use that product**
and how the human and agent share state and artifacts.

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
| Sep 2, 00:22 | PR #439 merge `4b1e58046fa529c1d9a5df489c2aab8698544dc1` | Improved deterministic customer-facing SUCCESS draft quality while preserving three-tool/human-send/zero-effect contracts; this includes the targeted presentation-projection extension now called out explicitly in the Competition Delta |
| Sep 2, 01:26 | PR #441 merge `dd2d1b285c1104ca6d34dca82cca7517ee25fa44` | Added browser-local Agent Activity presentation and explicit ACTION / STATE / ARTIFACT capability framing without adding tools |
| Sep 2, 03:46 | PR #442 merge `a87b2bca4d2c3409396d7140c2a366ad8faa063d` | Fixed multi-run/latest-workflow presentation semantics to prevent stale state |
| Sep 2, 15:59 | PR #443 merge `474a1c9ab31b70a0f68ff40a69e5310e65a04e0a` | Added public-safe native functional acceptance evidence for exactly three tools, SUCCESS, AMBIGUOUS safe stop, human-send boundary, and zero external effects |
| Sep 2, 18:43 | PR #444 merge `8a9df7178e20fe8f3faf642ddf09858f6716e5da` | Elevated the MG Guide judge-facing frontend presentation while preserving the accepted runtime/tool contract |
| Sep 3, 17:10 | PR #445 merge `78f5c7976a6e1d1b4b3d6d806115648f0d5e65d3` | Finalized judge-first WebMCP submission packaging, challenge-period evidence, testing instructions, demo script, and Devpost draft around the official rubric |
| Sep 3, 20:32 | PR #446 merge `90982f31c099872179a58dd2e9d3a2c6bbf370fb` | Made WebMCP the unmistakable current judge front door while preserving Google All Things Agentic material as historical context |

All listed work occurred inside the final challenge submission window.

---

## Repository-level delta check

A direct GitHub compare from the recorded pre-WebMCP implementation baseline
`bc9a723f84e72ec3605da495ad16fbf78f3a99a9` to the public judge-front-door
state `90982f31c099872179a58dd2e9d3a2c6bbf370fb` shows the repository **60
commits ahead** of that baseline.

That compare includes substantive new WebMCP implementation and verification
surfaces, including:

- `src/mg_guide/webmcp/` — added;
- `webmcp/static/` — added;
- `tests/webmcp/` — added;
- `deployment/webmcp/Dockerfile` — added;
- `proof/webmcp/` — added;
- `competition/webmcp/` — added;
- targeted presentation integration changes under
  `src/mg_guide/judge_surface/demo_stages.py` and corresponding tests.

The targeted `judge_surface` changes are intentionally disclosed here. They
support the WebMCP follow-up draft/presentation experience and do not change the
claim that the underlying MG Guide workflow, agent sequence, and deterministic
policy are pre-existing foundation.

---

## Meaningful extension summary

```text
PRE-EXISTING MG GUIDE
meeting_follow_up_v1
+ Meeting Context Agent
+ Relationship Context Agent
+ Follow-Up Planning Agent
+ deterministic policy
+ existing MG Guide / A.I. Rolodex product surface

                    ↓ reused foundation

NEW WEBMCP CHALLENGE EXTENSION

1. BROWSER-AGENT CONTRACT
   exactly 3 native tools
   ACTION / STATE / ARTIFACT

2. NEW WEB PRODUCT SURFACE
   human + agent share visible state
   native discovery + invocation

3. BOUNDED WEBMCP ADAPTER
   stateless synthetic backend
   SUCCESS + AMBIGUOUS_CONTACT only
   authority-bearing inputs rejected

4. SAFETY + EXPERIENCE MODEL
   browser-held state
   deterministic follow-up draft
   requires_human_send=true
   fail closed on ambiguous identity
   zero CRM/email external effects

5. TEST / DEPLOY / PROOF SURFACE
   WebMCP-specific tests
   deployment packaging
   production host integration
   native functional acceptance
   competition delta + judge testing
```

This is not a thin WebMCP label placed on a pre-existing application. The
challenge work introduces a new structured browser-agent interaction model and
the supporting product, safety, test, deployment, and evidence surfaces.

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
- Browser product surface: [`../../webmcp/static/`](../../webmcp/static/)
- Bounded adapter: [`../../src/mg_guide/webmcp/`](../../src/mg_guide/webmcp/)
- Targeted presentation integration:
  [`../../src/mg_guide/judge_surface/demo_stages.py`](../../src/mg_guide/judge_surface/demo_stages.py)
- Tests: [`../../tests/webmcp/`](../../tests/webmcp/)
- Competition deployment: [`../../deployment/webmcp/Dockerfile`](../../deployment/webmcp/Dockerfile)
- Full boundary: [`COMPETITION_DELTA.md`](COMPETITION_DELTA.md)
- Native production proof: [`../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md`](../../proof/webmcp/mg-guide-webmcp-production-acceptance-001.md)
- Judge journey: [`JUDGE_TESTING.md`](JUDGE_TESTING.md)

This ledger documents competition-period implementation and packaging history
only. It does not assert that every broader MG Guide capability shown in the
repository was created during The WebMCP Challenge.
