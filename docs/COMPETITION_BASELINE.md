# Competition Baseline vs New Work

**Competition:** Google All Things Agentic Hackathon
**Track target:** Fortified Enterprise Fleet
**Workflow:** `meeting_follow_up_v1`
**Repository:** `themg-max/mg-guide-agentic-sales-workspace`
**Status:** Foundation charter (public, sanitized)

This document is the authoritative separation between **pre-existing** MG
capabilities and **competition-period new work**. Judges and collaborators
must treat claims accordingly.

---

## PRE-EXISTING

The following capabilities and concepts predate the competition period and
must **not** be presented as invented for this hackathon:

| Capability | Notes |
| --- | --- |
| **MG MCP** | Pre-existing governed retrieval / trust handling / organizational context surface (read-oriented). |
| **Existing MG Guide** | Pre-existing authenticated application surface and sales-workspace product direction. |
| **OL3 architecture / governance concepts** | Pre-existing orchestration authority ideas: contracts, lanes, gates, proof packets, boundary checks, layered instruction architecture. |

These foundations are **inputs and constraints**, not competition inventions.
This public repository does not re-publish private MG implementation internals.

---

## NEW COMPETITION WORK

Competition-period novelty centers on the sales-workflow extension embodied by
this repository and its vertical slice:

| New work item | Description |
| --- | --- |
| **This repository** | Standalone public competition home with sanitized contracts, fixtures, and provenance. |
| **`meeting_follow_up_v1`** | Frozen vertical-slice workflow: transcript → governed CRM follow-up. |
| **ADK / Gemini implementation** | Google ADK multi-agent implementation using **Gemini 3.5+** for extraction/evaluation (not yet implemented in foundation). |
| **GHL MCP integration** | CRM boundary via GHL MCP (test account only); exact tool names remain UNKNOWN until discovery. |
| **Firestore audit** | Per-run `workflow_runs/{run_id}` operational proof records. |
| **New MG Guide Meeting Follow-Up experience** | Dedicated Meeting Follow-Up card (completed + needs-review), not generic chat dump. |
| **Test fixtures / tests / deployment / demo** | Synthetic fixtures, acceptance tests, planned Cloud Run deployment, and judge-facing demo proof. |

### New-work claim (one sentence)

> A competition-period meeting-follow-up agent workflow that integrates Google
> ADK/Gemini, OL3 workflow enforcement, GHL MCP CRM tools, Firestore audit
> state, and a new MG Guide sales-workspace experience.

---

## What this foundation commit is / is not

| Is | Is not |
| --- | --- |
| Public provenance and contracts | A running multi-agent system |
| Synthetic fixtures only | Production CRM integration |
| Explicit pre-existing vs new-work ledger | A copy of the private MG monorepo |
| Safe for judging inspection | Authorization to mutate IAM, secrets, or live CRM |

---

## Related artifacts

- [`MEETING_FOLLOW_UP_FOUNDATION.md`](MEETING_FOLLOW_UP_FOUNDATION.md) — frozen vertical-slice foundation
- [`SECURITY.md`](SECURITY.md) — data, secret, and mutation posture
- [`../competition/NEW_WORK_LEDGER.md`](../competition/NEW_WORK_LEDGER.md) — living ledger of competition-period deltas
- [`../competition/AI_COLLABORATION_LOG.md`](../competition/AI_COLLABORATION_LOG.md) — AI collaboration notes for the competition period
