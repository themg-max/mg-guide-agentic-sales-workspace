# Judge documentation index

```text
SURFACE=docs/judges/README.md
AUDIENCE=HACKATHON_JUDGES
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
```

Use this folder as the judge path. Deep engineering documents remain in place
and are linked only when you want more proof.

## 1. Start here

- [JUDGE_START_HERE.md](../../JUDGE_START_HERE.md) — one-page product and demo path
- [README.md](../../README.md) — repository front door

## 2. Testing MG Guide

- [JUDGE_ACCESS.md](JUDGE_ACCESS.md) — competition Workspace account and access rules
- [Demo script (~4 min)](../demo/meeting-follow-up-v1-4min-demo-script.md)
- [Demo truth boundary](../demo/meeting-follow-up-demo-v1.md)

Required demonstrations:

| Selector | Expected salesperson state |
| --- | --- |
| `SUCCESS` | Completed follow-up |
| `AMBIGUOUS_CONTACT` | Needs review / fail-closed |

## 3. Architecture

- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) — judge-facing summary only
- [Competition architecture](../architecture/meeting-follow-up-v1-competition-architecture.md)
- [Workspace add-on UX](../architecture/mg-guide-workspace-addon-judge-ux-v1.md)
- [Workspace add-on auth contract](../architecture/mg-guide-workspace-addon-auth-contract-v1.md)

## 4. Google technologies

Lead with the hosted three-agent runtime, then the judge surface:

| Technology | Role |
| --- | --- |
| Google Cloud Agent Runtime | Hosts `mg-guide-orchestrator` |
| Google ADK `SequentialAgent` | Sequences the three specialized agents |
| Gemini 3.5 Flash | Meeting-context extraction |
| Cloud Run | Competition judge / Workspace adapter surface |
| Firestore | Audit proof |
| Google Workspace add-on | Thin presentation and routing adapter |
| HighLevel REST v3 bounded adapter | Current CRM boundary |

## 5. Competition-period work

- [Devpost write-up](../competition/DEVPOST_WRITEUP.md)
- [Competition directory](../../competition/README.md)
- [New Work Ledger / Competition Delta](../../competition/NEW_WORK_LEDGER.md)

The ledger and AI collaboration log are evidence, not required first reading.

## 6. Evidence

- [PROOF_INDEX.md](PROOF_INDEX.md) — short claim-to-proof map
- [Proof directory](../../proof/README.md) — judge-recommended vs deep technical

## 7. Security / synthetic-data boundary

- Demonstration uses synthetic / test data.
- Judge account credentials are delivered privately, never committed.
- Agents propose; policy decides; live CRM effects remain separately governed.
- Current REST note create/readback is pending.
- Same-run transcript-to-live-CRM write is not claimed.

See [docs/SECURITY.md](../SECURITY.md) and
[governance/PUBLIC_PRIVATE_BOUNDARY.md](../../governance/PUBLIC_PRIVATE_BOUNDARY.md).

## 8. Deep technical documentation

These remain the engineering reference. They are not the judge path.

| Path | What it is |
| --- | --- |
| [`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../MEETING_FOLLOW_UP_FOUNDATION.md) | Original foundation |
| [`docs/COMPETITION_BASELINE.md`](../COMPETITION_BASELINE.md) | What was pre-existing vs competition-period |
| [`docs/nw008/`](../nw008/) | CRM transport planning and reconciliation |
| [`src/`](../../src/) | Runtime source (do not treat README claims as code changes) |
| [`proof/`](../../proof/README.md) | Durable proof history |

```text
JUDGE_PATH=README.md -> JUDGE_START_HERE.md -> docs/judges/
DEEP_ENGINEERING_REFERENCE=docs/ + proof/ + competition/ + src/
```
