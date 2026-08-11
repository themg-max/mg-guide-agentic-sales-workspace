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
| Recorded at (UTC) | 2026-08-11T20:12:00Z |

## What the workflow does

Runs **Python-test-only** deterministic validation for the merged Phase 1 foundation, including the repository-local verifier script for packet/schema/fixture/replay checks:

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
| PR opened | YES — https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/3 |
| Workflow run from PR | YES — https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531473115 |
| PR head SHA at green run | `61c01a3152a072ebfaefa2ab97b0ab3124cea5ef` |
| Workflow conclusion | **success / PASS** |
| Secret-scan false-positive fix | commit `61c01a3152a072ebfaefa2ab97b0ab3124cea5ef` (PEM marker constructed; scanner self-skip) |
| Push-event corroborating run | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531468581 (success) |

## Repair note

Initial PR runs failed because the secret-pattern scanner matched the literal PEM begin token embedded in the workflow pattern list. Fixed by constructing the marker at runtime and skipping the scanner definition file. No secrets were present.

## STOP condition

CI workflow passes from PR execution and this note records the result.

**STOP CONDITION MET** for green PR workflow run `31531473115` on head `61c01a3152a072ebfaefa2ab97b0ab3124cea5ef`.
This note update is documentary evidence of that pass; a subsequent tip commit may re-run CI and should also pass without changing workflow semantics.

## Final tip binding (post-documentary commit)

| Item | Value |
| --- | --- |
| Final PR tip SHA | `28a85e1539e4eb1356a01e632f875d74f2eec9f4` |
| Final PR workflow run | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31531651114 |
| Final workflow conclusion | **success / PASS** |

STOP condition remains MET on final tip after proof-note recording commit.

## Closeout binding (documentary normalization, PR #3)

| Item | Value |
| --- | --- |
| Closeout head SHA | `69c9068ae21cf6606a3bcd9de6d82fedd611e242` |
| Closeout PR workflow run | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31535966409 |
| Closeout workflow conclusion | **success / PASS** (all 14 verification steps green) |
| Corroborating push-event run | https://github.com/themg-max/mg-guide-agentic-sales-workspace/actions/runs/31535963747 (success) |

This closeout commit is documentary-only: it binds `proof/phase1/proof-return.yaml`
to tested head `69c9068ae21cf6606a3bcd9de6d82fedd611e242` and PR #3, includes
`proof-return.yaml` in its own changed-files accounting, fixes a duplicate
ledger ID, and completes the PR #3 CI/proof checklist. No workflow, runtime,
or test semantics were altered.

