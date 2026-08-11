# Workflow Proof Note — Phase 1 Deterministic CI

| Field | Value |
| --- | --- |
| Authorization ID | `MG_GUIDE_PHASE1_CI_V1` |
| Authorization status | APPROVED |
| Authority source | Human instruction in ChatGPT Project session, 2026-08-11 |
| Public repository | `themg-max/mg-guide-agentic-sales-workspace` |
| Baseline merge | PR #2 → `47deaae2820720b629eafe3ffec8c21245f4dfcb` |
| Branch | `chore/phase1-deterministic-ci` |
| Workflow path | `.github/workflows/phase1-deterministic.yml` |
| Recorded at (UTC) | 2026-08-11T20:10:00Z |

## What the workflow does

Runs **Python-test-only** deterministic validation for the merged Phase 1 foundation:

1. Install pinned dependencies from `requirements.txt`
2. Parse `contracts/workflow_states.yaml`
3. Parse `contracts/failure_codes.yaml`
4. Validate `contracts/meeting_follow_up_packet.schema.json`
5. Validate `proof/phase1/proof-return.yaml` against `governance/PROOF_RETURN.schema.yaml`
6. `PYTHONPATH=src python -m pytest -q`
7. Verify three synthetic fixture terminal outcomes
8. Verify replay/idempotency
9. Verify note/stage intent cardinality bounds
10. `git diff --check`
11. Secret-pattern scan on authorized paths

## Why it was necessary

Phase 1 implementation merged via PR #2 with local proof only. Repository had no CI workflows, and the original Phase 1 implementation grant did not authorize `.github/workflows/**`. Authorization `MG_GUIDE_PHASE1_CI_V1` now permits this narrow deterministic workflow.

## Security posture

```text
permissions.contents: read
secrets: NONE
application_external_effects: 0
pull_request_target: NOT USED
repository writes from workflow: NOT AUTHORIZED
GHL/CRM/Gemini/ADK/Firestore/Cloud Run/IAM/Secret Manager: BLOCKED
```

## Explicit non-claims

- Does not call Gemini, ADK, GHL, CRM, Firestore, or Cloud Run
- Does not deploy
- Does not mutate IAM or read Secret Manager
- Does not use production data
- Does not grant workflow write permissions

## Validation / CI result

| Item | Status |
| --- | --- |
| Local workflow file present | YES |
| PR opened | PENDING |
| Workflow run from PR | PENDING |
| Workflow conclusion | PENDING |

Update this section after the PR workflow run completes.

## STOP condition

CI workflow passes from PR execution and this note records the result.
