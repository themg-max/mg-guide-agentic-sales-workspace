# NW-007 — Cloud Run Health-Route Remediation Authorization

ARTIFACT_ID=MG_GUIDE_NW007_HEALTH_ROUTE_REMEDIATION_AUTHORIZATION_V1
ARTIFACT_KIND=BOUNDED_REMEDIATION_AUTHORIZATION_PLANNING
OWNER_LANE=VS Code / Orchestrator planning lane
CREATED_AT=2026-08-13T19:56:00Z
STATUS=NW007_HEALTH_ROUTE_REMEDIATION_AUTHORIZATION_READY_FOR_REVIEW

This artifact is **PLANNING ONLY**. Creating or merging it does **not**
implement application changes, rebuild images, push to Artifact Registry,
deploy Cloud Run, alter IAP/IAM/OAuth, or mutate any cloud resource.

Human approval of an approved-and-merged R1 implementation PR is required
before any R2 cloud mutation. Self-activation is forbidden.

---

## Durable B2 proof baseline (freeze record)

Verified at authorization authoring time against GitHub and local `origin/main`.

```
NW007_B2_PROOF_PR=31
NW007_B2_PROOF_HEAD=2f381221e4bc382d0c0073e8fbfe18267fb3bcee
NW007_B2_PROOF_MERGE_SHA=7d10a13e3ab2198b7c42820b39f718c6d62d6dc8
NW007_B2_PROOF_MERGED_AT=2026-08-13T19:55:17Z
NW007_B2_PROOF_CI_RUN=31737446009
NW007_B2_PROOF_CI_RESULT=SUCCESS
NW007_B2_PROOF_PATH=proof/nw007/nw007-stage-b-cloud-deployment-proof.md
NW007_B2_PROOF_BRANCH=deploy/nw007-stage-b-cloud-deployment-proof
```

Pre-merge / merge verification (exact):

```
REVIEWED_HEAD_SHA=2f381221e4bc382d0c0073e8fbfe18267fb3bcee
PR31_HEAD_SHA_OBSERVED=2f381221e4bc382d0c0073e8fbfe18267fb3bcee
PR31_STATE=MERGED
EXACT_HEAD_CI_RUN=31737446009
EXACT_HEAD_CI_HEAD_SHA=2f381221e4bc382d0c0073e8fbfe18267fb3bcee
EXACT_HEAD_CI_RESULT=SUCCESS
HEAD_IS_ANCESTOR_OF_MAIN=YES
MAIN_TIP_AT_AUTHORING=7d10a13e3ab2198b7c42820b39f718c6d62d6dc8
```

PR #31 is accepted as the truthful Stage B B2 baseline. No reinterpretation of
B2 IAP/IAM/OAuth outcomes is authorized by this packet.

---

## Parent authority chain (exact, inherited)

```
SIGNED_GRANT_PR=26
SIGNED_GRANT_MERGE_SHA=e5822b3a24ad7bcb71add846e60a578255c663e5
SIGNED_GRANT_PATH=proof/nw007/nw007-cloud-run-human-execution-grant.md

STAGE_B_ACTIVATION_PR=29
STAGE_B_ACTIVATION_MERGE_SHA=17d1b2798a1511e8c938c8b6a371f4b77a1737ed
STAGE_B_ACTIVATION_PATH=proof/nw007/nw007-stage-b-deployment-activation.md

STAGE_B_IMPLEMENTATION_PR=30
STAGE_B_IMPLEMENTATION_MERGE_SHA=14b97c5517e61733783d6b14facd8d33757c897d

STAGE_B_B2_PROOF_PR=31
STAGE_B_B2_PROOF_MERGE_SHA=7d10a13e3ab2198b7c42820b39f718c6d62d6dc8
```

This remediation authorization is a **bounded follow-on** to the frozen B2
proof. It does not reopen Stage A bootstrap, does not expand the signed grant,
and does not authorize greenfield service creation.

---

## Repo preflight (before artifact edits)

```bash
pwd
# /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git branch --show-current
# plan/nw007-health-route-remediation-authorization

git status --short --untracked-files=all
# (empty before this artifact)

git rev-parse HEAD
# 7d10a13e3ab2198b7c42820b39f718c6d62d6dc8
```

Preflight result:

```
BRANCH_IS_MAIN=NO
WORKING_TREE_CLEAN_BEFORE_ARTIFACT=YES
UNRELATED_CHANGES=NO
BASE_IS_B2_PROOF_MERGE=YES
```

Abort conditions were not met. Artifact edits proceed only on the planning
branch above. `git add .` is not used.

---

## Source-authority finding (why remediation is required)

### Observed B2 execution finding (PR #31 proof)

From `proof/nw007/nw007-stage-b-cloud-deployment-proof.md` (merged via PR #31):

```
SMOKE_THROUGH_IAP_HEALTHZ=BLOCKED_GFE_RESERVED_PATH_NEVER_REACHES_SERVICE
```

Exact-path `GET /healthz` returns the Google Front End's own HTTP 404 robot
page and **never reaches IAP or Cloud Run**, for both unauthenticated and
authenticated requests, on both service URL forms. Adjacent paths
(`/healthzz`, `/healthz/`, `/HEALTHZ`, app JSON 404s) do reach the service and
carry normal GFE/trace headers. This is platform edge behavior, not an IAP
denial and not an IAM/OAuth misconfiguration.

Compensating B2 evidence (unchanged by this authorization):

- Exact deployed image digest locally serves `GET /healthz` → HTTP 200,
  `status=ok`, `judge_mode=stub`, expected catalog hash/names.
- Through-IAP authenticated judge POSTs for SUCCESS and STAGE_CHANGE_DENIED
  passed with zero external effects.
- Working IAP/IAM/OAuth configuration must not be modified by this remediation.

### Official Cloud Run Known Issues alignment

Official Cloud Run Known Issues document reserved URL paths:

- some paths ending with `"z"` cannot be used
- Google recommends avoiding **all** paths ending in `"z"`

Therefore:

```
PATH_/healthz=INCOMPATIBLE_WITH_CLOUD_RUN_JUDGE_ENDPOINT_IN_OBSERVED_EXECUTION
CANONICAL_REPLACEMENT=/health
PATH_/health_ENDS_WITH_Z=NO
```

`/health` is the recommended replacement for the externally reachable liveness
route on the existing Cloud Run judge service.

---

## Current repository contract (as of B2 baseline)

Application (`src/mg_guide/judge_surface/app.py`):

- Implements `GET /healthz` only as the liveness/provenance route.
- Payload fields: `status`, `service`, `version`, `commit`,
  `scenario_catalog_hash`, `judge_mode`, `scenario_names`.
- Demo route remains `POST /demo/meeting-follow-up`.

Tests (`tests/judge_surface/test_app.py`):

- Assert `GET /healthz` → 200 / `status=ok` / `judge_mode=stub`.
- Assert non-stub mode rejection on `/healthz`.

Judge docs / prior authorizations reference `/healthz` as the smoke liveness
path. Those references become stale for **through-Cloud-Run** checks and must
be updated in R1 to prefer `/health` without changing IAP/IAM/OAuth doctrine.

---

## Authorized remediation sequence

```
REMEDIATION_SEQUENCE=
R1_REPO_REMEDIATION;
R2_BOUNDED_REDEPLOY

SELF_ACTIVATION=FORBIDDEN
R2_REQUIRES_HUMAN_APPROVAL_AFTER_MERGED_R1=YES
```

### R1 — repository remediation (no cloud mutation)

```
R1_REPO_REMEDIATION=
ADD_CANONICAL_GET_/health;
OPTIONALLY_RETAIN_/healthz_LOCAL_COMPATIBILITY;
UPDATE_TESTS;
UPDATE_JUDGE_DOCS

R1_CLOUD_MUTATION=NO
```

R1 implementation requirements (deferred to a separate implementation PR after
this authorization merges):

1. **Canonical route:** add `GET /health` returning the **existing** health
   payload (same fields and fail-closed judge-mode behavior as today's
   `_healthz()` contract).
2. **Optional compatibility:** retain `GET /healthz` for local/container
   compatibility only. It remains useful for image-digest smoke outside GFE,
   but must not be treated as the through-Cloud-Run canonical liveness path.
3. **Tests:**
   - `GET /health` → HTTP 200
   - `status=ok`
   - `judge_mode=stub`
   - scenario catalog unchanged (names + catalog hash contract preserved)
   - non-stub mode rejection continues to fail closed on the health handler(s)
4. **Docs:** update judge-surface / NW-007 smoke references so canonical
   external liveness is `/health`. Note `/healthz` GFE reservation and optional
   local retention explicitly.
5. **Branch name for implementation (post-auth merge):**
   `fix/nw007-cloud-run-health-route`
6. **Out of R1:** any `gcloud` write, Cloud Build submit, image push, Cloud Run
   update, IAM bind, IAP toggle, OAuth change, secret change, Firestore write,
   CRM mutation, or live Gemini enablement.

```
R1_DELIVERABLE=IMPLEMENTATION_PR_FOR_REVIEW
R1_STOP_BEFORE=ANY_CLOUD_MUTATION
```

### R2 — bounded cloud redeploy (human-gated; not authorized to execute yet)

```
R2_PREREQUISITE=
APPROVED_AND_MERGED_R1_IMPLEMENTATION_PR

R2_SCOPE=
ONE_CLOUD_BUILD;
ONE_IMAGE_PUSH_TO_EXISTING_MG_GUIDE_JUDGE_REPO;
ONE_UPDATE_TO_EXISTING_CLOUD_RUN_SERVICE;
ONE_NEW_REVISION;
AUTHENTICATED_SMOKE

R2_CLOUD_MUTATION=DEFERRED_PENDING_HUMAN_APPROVAL
```

R2 invariants (hard; must match the frozen B2 service, not a new surface):

```
R2_INVARIANTS=
PROJECT=mg-devpost
REGION=us-east4
SERVICE=mg-guide-agentic-sales-workspace-judge
RUNTIME_SA=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
MEETING_CONTEXT_GEMINI_MODE=stub
MIN_INSTANCES=0
MAX_INSTANCES=1
```

R2 expected smoke (after human approval and execution authorization):

- Authenticated `GET /health` through the existing IAP-protected service URL
  returns HTTP 200 with `status=ok`, `judge_mode=stub`, catalog unchanged.
- Existing authenticated demo scenarios remain green (SUCCESS,
  STAGE_CHANGE_DENIED at minimum; AMBIGUOUS_CONTACT if included in prior B2
  smoke set).
- Unauthenticated access remains denied (no public binding).
- No requirement to “fix” exact-path `/healthz` through GFE; platform
  reservation may persist. Optional local `/healthz` is not the external gate.

---

## Forbidden actions (R1 and R2)

```
FORBIDDEN=
NEW_SERVICE;
NEW_AR_REPO;
NEW_SERVICE_ACCOUNT;
NEW_IAM_BINDING;
IAP_CHANGE;
OAUTH_CHANGE;
NEW_PRINCIPAL;
PUBLIC_ACCESS;
LIVE_GEMINI;
FIRESTORE_WRITE;
CRM_MUTATION;
SECRET_MANAGER_MUTATION
```

Explicit non-goals:

- Do **not** modify working IAP/IAM/OAuth configuration established in B2.
- Do **not** add `allUsers` / `allAuthenticatedUsers`.
- Do **not** create a second judge service or alternate region.
- Do **not** widen instance caps, attach new secrets, or enable live Gemini.
- Do **not** treat ChatGPT/reviewer disposition as human cloud-execution
  approval for R2.

---

## Human approval gates

```
GATE_0_THIS_AUTHORIZATION_PR=
REQUIRED_BEFORE_R1_IMPLEMENTATION_MERGE_ACCEPTANCE
# Planning merge records authority to implement R1 in-repo only.

GATE_1_R1_IMPLEMENTATION_PR=
REQUIRED_HUMAN_REVIEW_AND_MERGE
# Code + tests + docs only. CI must be SUCCESS on exact head.

GATE_2_R2_CLOUD_EXECUTION=
REQUIRED_SEPARATE_HUMAN_APPROVAL_AFTER_MERGED_R1
# No R2 build/deploy may start without explicit human approval referencing
# the merged R1 SHA and this authorization artifact.
```

```
HUMAN_APPROVAL_REQUIRED_BEFORE_R2=YES
IAP_IAM_OAUTH_MUTATION_AUTHORIZED=NO
PUBLIC_ACCESS_AUTHORIZED=NO
```

---

## Post-authorization implementation handoff (not executed in this PR)

After **this** remediation authorization is approved and merged:

1. Create fresh branch `fix/nw007-cloud-run-health-route` from updated `main`.
2. Implement R1 only (`GET /health`, optional local `/healthz`, tests, docs).
3. Open implementation PR for human review.
4. STOP for review. Do not begin R2.

```
IMPLEMENTATION_BRANCH_NAME=fix/nw007-cloud-run-health-route
IMPLEMENTATION_CLOUD_MUTATION=NO
RETURN_IMPLEMENTATION_PR_FOR_REVIEW_BEFORE_R2=YES
```

---

## STOP

```
STOP_CODE=NW007_HEALTH_ROUTE_REMEDIATION_AUTHORIZATION_READY_FOR_REVIEW
CLOUD_MUTATION_PERFORMED_BY_THIS_ARTIFACT=NO
IAP_IAM_OAUTH_TOUCHED=NO
R1_IMPLEMENTED_IN_THIS_PR=NO
R2_EXECUTED=NO
NEXT_HUMAN_ACTION=REVIEW_AND_MERGE_THIS_AUTHORIZATION_THEN_ALLOW_R1_IMPLEMENTATION_PR
```
