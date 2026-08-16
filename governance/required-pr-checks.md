# MG Guide — Repo-Local PR Review and Required Check Policy

```text
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
POLICY_SCOPE=PR_REVIEW_AND_REQUIRED_CHECKS
POLICY_AUTHORITY=REPOSITORY_LOCAL
POLICY_ID=mg-guide-pr-review-required-checks-v1
RECORDED_AT_UTC=2026-08-16T15:21:00Z
STATUS=AUTHORITATIVE_FOR_MG_GUIDE_REVIEWERS
```

## 1. Purpose and authority

This file is the **repository-local** PR review and required-check policy for
**themg-max/mg-guide-agentic-sales-workspace** (MG Guide) only.

Reviewers must resolve required checks, PR classes, proof obligations, and
merge readiness from **this document and live MG Guide repository
configuration** — not by importing policy from any other repository
(including `themg-max/A.I-Rolodex---Context` or other private control-plane
repos).

| Field | Value |
| --- | --- |
| Repository | `themg-max/mg-guide-agentic-sales-workspace` |
| Policy scope | PR review classification + required checks + merge verdict |
| Policy authority | Repository-local (this file) |
| CI mutation by this policy | None — documentation only |

Related public governance (not substitutes for this policy):

- [`GOVERNANCE_PROFILE.yaml`](GOVERNANCE_PROFILE.yaml)
- [`REQUIRED_PR_CHECKS.md`](REQUIRED_PR_CHECKS.md) — earlier convention record;
  where conflict exists, **this file controls** for PR review disposition
- [`README.md`](README.md) — governance directory overview

---

## 2. Live required-check configuration (derived, not copied)

### 2.1 Inspection basis

Recorded from live repository inspection on **2026-08-16** (no CI workflow
changed by this policy unit):

| Probe | Result |
| --- | --- |
| Default branch | `main` |
| Branch protection on `main` | **Not configured** (`GET .../branches/main/protection` → HTTP 404) |
| Repository rulesets | **None** (`[]`) |
| Active workflows | One: **Phase 1 Deterministic CI** (`.github/workflows/phase1-deterministic.yml`, state=`active`) |
| Workflow job / check-run name | **`Phase 1 deterministic validation`** |
| Recent merged protected-path PRs | PRs #50–#60 each show exactly one successful check: `Phase 1 deterministic validation` under workflow `Phase 1 Deterministic CI` |

### 2.2 Canonical required check names

GitHub does not currently enforce branch-protection required status checks on
`main`. For **repo-local reviewer policy**, the following check names are
**canonical** and must be evaluated at the **exact PR head SHA** under review:

| # | Canonical check name (exact) | Workflow name | Source of truth |
| --- | --- | --- | --- |
| 1 | `Phase 1 deterministic validation` | `Phase 1 Deterministic CI` | Live workflow job `name:` in `.github/workflows/phase1-deterministic.yml`; observed on merged PRs #50–#60 and open PR heads |

**Do not** treat any of the following as MG Guide required checks unless this
file is later amended after a live configuration change:

- Checks defined only in `themg-max/A.I-Rolodex---Context` (or any non-MG-Guide repo)
- Renamed, aliased, or “equivalent” check labels that do not match the exact
  string `Phase 1 deterministic validation`
- Optional third-party apps not present on recent successful MG Guide PR heads

### 2.3 Human merge authority (non-check)

In addition to the automated check above, merge into `main` requires **human
reviewer / merge authority** at the exact reviewed head. This is not a GitHub
Actions check name; it is a governance obligation recorded in reviewer
disposition or the merge act itself.

### 2.4 Re-derivation rule

If live configuration changes (new workflow jobs, branch protection, or
rulesets), update **this file** with freshly inspected exact names before
treating new checks as required. Until then, section 2.2 remains authoritative
for reviewers.

---

## 3. PR classes

Every PR under review must be classified as **exactly one** primary class
(secondary notes allowed). Classification drives artifact obligations.

| PR class | Intent |
| --- | --- |
| `planning_only` | Plans, scopes, authorization *requests*, or design docs with no runtime execution and no production-path implementation |
| `proof_only` | Proof packets, closeouts, reconciliations, or evidence under `proof/**` without implementation or infra change |
| `authorization` | Explicit lane / grant / authorization artifacts under governance (or designated auth paths) that unlock later work |
| `execution_proof` | Proof that a previously authorized bounded execution ran (or failed closed) with evidence |
| `completion_decision` | Acceptance, completion claim, or go/no-go decision records for a work item |
| `implementation` | Product, contract, test, or script code changes that alter runtime or verified behavior |
| `workflow_or_infra` | CI workflows, deploy, infra, or repository automation surfaces |

---

## 4. Artifact requirements by PR class

Legend:

- `REQUIRED` — must be present and coherent for `READY_FOR_MERGE`
- `NOT_APPLICABLE` — must not be demanded for this class
- `CONDITIONAL` — required when the PR touches the named surface or claims the named effect
- `REQUIRED_IF_CLAIMED` — required when the PR body/title claims execution, completion, or external effect

### 4.1 Matrix

| PR class | `PLANNING_ARTIFACT` | `RUNTIME_HARNESS` | `EXECUTION_PROOF` | `REVIEWER_DISPOSITION_FILE` | Notes |
| --- | --- | --- | --- | --- | --- |
| `planning_only` | REQUIRED | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | No runtime mutation; plan must be path-bounded |
| `proof_only` | CONDITIONAL | NOT_APPLICABLE | REQUIRED | CONDITIONAL | Proof under `proof/**`; disposition when closing a reviewed unit |
| `authorization` | CONDITIONAL | NOT_APPLICABLE | NOT_APPLICABLE | CONDITIONAL | Explicit grant/auth artifact; does not itself execute |
| `execution_proof` | CONDITIONAL | CONDITIONAL | REQUIRED | CONDITIONAL | Must cite prior authorization; no silent scope expansion |
| `completion_decision` | CONDITIONAL | NOT_APPLICABLE | REQUIRED_IF_CLAIMED | REQUIRED | Decision must reference evidence / prior PRs |
| `implementation` | CONDITIONAL | CONDITIONAL | REQUIRED_IF_CLAIMED | CONDITIONAL | Tests/contracts as applicable; CI must pass |
| `workflow_or_infra` | CONDITIONAL | CONDITIONAL | NOT_APPLICABLE | CONDITIONAL | Treat as higher-risk; justify blast radius |

### 4.2 `planning_only` (normative detail)

```text
PLANNING_ARTIFACT=REQUIRED
RUNTIME_HARNESS=NOT_APPLICABLE
EXECUTION_PROOF=NOT_APPLICABLE
REVIEWER_DISPOSITION_FILE=NOT_APPLICABLE
```

A `planning_only` PR must not introduce executable external mutation paths or
claim live execution. Required check policy in §5 still applies (CI green at
head) so the tree remains merge-safe.

### 4.3 Artifact location conventions (MG Guide)

| Artifact kind | Expected surface |
| --- | --- |
| Planning | `docs/**`, `competition/**`, task/plan paths named in the PR, or bounded markdown under an agreed work-item prefix |
| Proof | `proof/**` (**MG Guide planning/proof surface**) |
| Authorization | `governance/authorizations/**` (and related governance grant files when explicitly in scope) |
| Reviewer disposition | Typically under `proof/**` for the work item (e.g. `*-reviewer-disposition.md`) when the class requires it |
| Runtime harness | `src/**`, `scripts/**`, tests that invoke live/safe-env runners — only when authorized |

---

## 5. Surfaces and lane authorization

### 5.1 MG Guide planning / proof surface

```text
proof/**
```

Proof-only and execution-proof PRs should concentrate durable evidence here
unless a task explicitly names another proof path.

### 5.2 Higher-risk surfaces

Changes under any of the following are **higher-risk** and require heightened
review. When the change enables or performs gated behavior, **explicit lane
authorization** is required before execution (authorization may land in a
prior `authorization` PR):

```text
src/**
tests/**
contracts/**
.github/workflows/**
deploy/**
infra/**
governance/authorizations/**
```

### 5.3 Explicit lane authorization rule

Require an explicit, merged (or same-PR) authorization artifact when the PR:

1. Touches higher-risk surfaces **and** claims or enables external mutation,
   deployment, IAM/secret change, or live CRM/cloud side effects; or
2. Is class `execution_proof` or `implementation` with runtime side effects; or
3. Expands scope beyond a previously granted allowlist / budget.

Authorization docs alone do not execute. Execution still needs a separate
authorized run and proof when claimed.

Absence of GitHub branch protection does **not** waive lane authorization.

---

## 6. Required-check evaluation procedure (reviewers)

For the PR head SHA `H` under review:

1. **Classify** the PR (§3).
2. **Scope check** — diff paths must match the claimed class and any
   task-writable path list; higher-risk surfaces trigger §5.
3. **Artifact check** — apply §4 matrix for the class.
4. **Required automated checks** — confirm canonical check(s) in §2.2 are
   `SUCCESS` on **exact head `H`** (not an ancestor, not a stale push).
5. **Mergeability** — no unresolved merge conflicts with the PR base (`main`
   unless otherwise stated); no blocking review state if human process requires
   approval.
6. **Proof / auth obligations** — class-specific; fail closed if claimed
   execution lacks proof or authorization.
7. **Verdict** — apply §7.

Stale checks after new pushes invalidate a prior green verdict until re-run on
the new head.

---

## 7. Formal reviewer verdict

### 7.1 `READY_FOR_MERGE`

```text
REVIEWER_FORMAL_VERDICT=READY_FOR_MERGE
```

Emit **only** when **all** of the following hold:

1. **All repo-local required checks** listed in §2.2 are `SUCCESS` on the
   **exact PR head** under review.
2. **Scope is valid** for the declared PR class and task writable paths
   (including higher-risk surface rules in §5).
3. **Proof obligations pass** for the class (§4), including authorization
   linkage when required.
4. **Mergeability is clean** (mergeable into base; no conflict; human merge
   authority satisfied per process).

### 7.2 Non-ready outcomes (informative)

Reviewers should refuse `READY_FOR_MERGE` when any §7.1 condition fails.
Common non-ready labels (non-exhaustive):

| Condition | Suggested disposition |
| --- | --- |
| Required check missing, pending, or failed on head | `CHECKS_NOT_GREEN` |
| Diff out of class / writable scope | `SCOPE_INVALID` |
| Missing proof or authorization for claimed effect | `PROOF_OR_AUTH_INCOMPLETE` |
| Conflicts or unclean mergeability | `NOT_MERGEABLE` |
| Policy/docs-only disagreement without check failure | Address in review comments; do not invent extra required check names |

---

## 8. What this policy does not do

- Does **not** change `.github/workflows/**` or any CI definition
- Does **not** enable runtime mutation, deployment, CRM writes, or IAM/secret changes
- Does **not** configure GitHub branch protection or rulesets
- Does **not** import or depend on A.I-Rolodex required-check lists
- Does **not** self-merge any PR
- Does **not** retroactively alter historical merge legitimacy; it standardizes
  **forward** reviewer disposition for MG Guide

---

## 9. Evidence appendix (inspection snapshot)

```text
REPO=themg-max/mg-guide-agentic-sales-workspace
DEFAULT_BRANCH=main
BRANCH_PROTECTION_MAIN=NOT_CONFIGURED
RULESETS=NONE
WORKFLOW_FILE=.github/workflows/phase1-deterministic.yml
WORKFLOW_NAME=Phase 1 Deterministic CI
CHECK_RUN_NAME=Phase 1 deterministic validation
EXAMPLE_MERGED_PR_HEADS_WITH_CHECK=PR#60,PR#59,PR#58,PR#57,PR#56
FOREIGN_REPO_CHECKS_IMPORTED=NO
```

---

## 10. STOP

```text
REPO_LOCAL_REVIEW_POLICY=YES
REQUIRED_CHECK_POLICY_RESOLVED=YES
STOP_CODE=MG_GUIDE_PR_REVIEW_POLICY_READY_FOR_REVIEW
```
