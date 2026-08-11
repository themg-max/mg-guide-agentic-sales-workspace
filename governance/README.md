# Governance profile — MG Guide Agentic Sales Workspace

This directory publishes the **public, sanitized** governance binding for the
competition repository. It does not contain private control-plane records.

## Authority split

| Surface | Role |
| --- | --- |
| Private AI Rolodex context repository | Governance / source-authority / current-phase control plane |
| **This public repository** | Implementation / test / public-proof surface |
| MG MCP | Read-only organizational context (when later authorized) |
| External systems (e.g. test CRM) | Separately gated; not authorized by docs alone |

## Operating rules

1. **Work occurs on bounded topic branches** — not directly on `main` for feature work.
2. **Exact writable scope per task** — each task names allowed paths; out-of-scope edits are refused.
3. **Agents propose; deterministic policy authorizes** — model output is never unilateral mutation authority.
4. **External mutations are separately gated** — CRM, cloud, IAM, secrets, and production data each require explicit grants.
5. **Synthetic data only** for competition-period development and proof unless a later grant says otherwise.
6. **Proof is required** — merged code without proof is incomplete.
7. **Merged PR ≠ production activation** — deployment and runtime activation need separate authority.

## Artifacts in this directory

| File | Purpose |
| --- | --- |
| [`GOVERNANCE_PROFILE.yaml`](GOVERNANCE_PROFILE.yaml) | Public machine-readable governance profile |
| [`EXECUTION_MANIFEST.schema.yaml`](EXECUTION_MANIFEST.schema.yaml) | Schema for bounded execution manifests |
| [`PROOF_RETURN.schema.yaml`](PROOF_RETURN.schema.yaml) | Schema for proof-return packets |
| [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) | What may and may not cross the public boundary |

## What this is not

- Not a copy of private `.ai` lane inventory or active-lane internals
- Not a secret store
- Not an IAM or deployment grant
- Not authorization to call production CRM or customer data
- Not Phase 1 implementation by itself

## Related public docs

- [`../README.md`](../README.md) — project foundation
- [`../docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../docs/MEETING_FOLLOW_UP_FOUNDATION.md) — sanitized foundation
- [`../competition/NEW_WORK_LEDGER.md`](../competition/NEW_WORK_LEDGER.md) — competition-period deltas
- [`../competition/AI_COLLABORATION_LOG.md`](../competition/AI_COLLABORATION_LOG.md) — AI collaboration transparency
