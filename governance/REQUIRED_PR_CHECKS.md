> **HISTORICAL / SUPERSEDED FOR CURRENT PR REVIEW**
>
> Current repository-local PR review authority:
> [`governance/required-pr-checks.md`](required-pr-checks.md)
>
> This file remains as the earlier convention record. Do not treat it as
> current merge-readiness authority when the two documents conflict.

# Required PR Check Policy — Convention Record

```text
STATUS=PROPOSED_NOT_YET_AUTHORITATIVE
ARTIFACT_KIND=REQUIRED_CHECK_POLICY_CONVENTION_RECORD
RECORDED_AT=2026-08-14
SCOPE=themg-max/mg-guide-agentic-sales-workspace
```

## Why this declaration is needed

Reviewers currently cannot point to a repo-authoritative declaration of which
checks are required for implementation-PR merge readiness. GitHub branch
protection for `main` is not configured (`gh api
repos/themg-max/mg-guide-agentic-sales-workspace/branches/main/protection`
returns 404), and no file in this repository declares a required-check set.
This file records the **observed convention** so reviewers have a durable,
honest reference. It does **not** create new policy.

## Current Phase 1 deterministic CI

The repository's single CI workflow is **Phase 1 Deterministic CI**
(`.github/workflows/phase1-deterministic.yml`), job **"Phase 1 deterministic
validation"**. It runs deterministic verification, contract/proof schema
validation, the full pytest suite, replay/idempotency checks,
`git diff --check`, and an authorized-path secret-pattern scan.

## Proposed required checks for this repo

| Proposed required check | Source / evidence |
| --- | --- |
| Phase 1 Deterministic CI — SUCCESS at the exact reviewed PR head | Recorded merge convention in `competition/NEW_WORK_LEDGER.md` ("Required check: Phase 1 Deterministic CI — SUCCESS (run 31541673310)") and `proof/phase2/closeout-note.md`; applied to every merged implementation PR (e.g. PR #4, PR #13, PR #15, PR #30) |
| Human review verdict at the exact reviewed head (merge performed by human merge authority) | Same recorded convention; e.g. PR #30 reviewer disposition recorded in `proof/nw007/nw007-stage-b-cloud-deployment-proof.md` |

## Human authority required to approve

Ratifying this convention into an authoritative policy (and/or configuring
GitHub branch protection to enforce it) requires explicit human governance
approval from the repository owner. No agent may self-authorize that change.

## Non-retroactivity

This record **cannot retroactively self-authorize PR #37** or any other open
PR. It documents the convention reviewers have already applied; it does not
weaken or strengthen governance, and it does not merge anything.

## STOP

```text
STOP_CODE=REQUIRED_CHECK_CONVENTION_RECORDED_PROPOSED_NOT_YET_AUTHORITATIVE
```
