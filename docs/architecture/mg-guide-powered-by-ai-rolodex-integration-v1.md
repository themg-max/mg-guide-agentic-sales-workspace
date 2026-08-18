# MG Guide Powered by AI Rolodex — Integration Architecture v1

## 0. Identity

```text
ARTIFACT=docs/architecture/mg-guide-powered-by-ai-rolodex-integration-v1.md
PHASE=planning_only_integration_architecture
OWNER=VS Code / MG Orchestrator
PRIMARY_PR_CLASS=planning_only
WORKFLOW=meeting_follow_up_v1
DEVPOST_PRIMARY_CAPABILITY=Meeting Follow-Up
BRANCH=planning/mg-guide-powered-by-ai-rolodex-integration-v1
BASE_REF=origin/main
BASE_SHA=4d4f79f8d64d0981b8cb1adf300f25c132f219eb
CREATED_AT_UTC=2026-08-18T15:34:00Z
TOPOLOGY_NORMALIZED_AT_UTC=2026-08-18T15:51:00Z
COMPETITION_SAFE=YES
IMPLEMENTATION_AUTHORIZED=NO
CROSS_REPO_IMPLEMENTATION_AUTHORIZED=NO
RUNTIME_CHANGES_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
REPO_MIGRATION_AUTHORIZED=NO
```

This unit is **planning / architecture only**. It freezes product role,
presentation, truth-boundary decisions, and **current repository topology**
so MG Guide is the primary user-facing Workspace assistant and AI Rolodex is
the underlying relationship-intelligence capability — without treating git
repo layout as the product boundary.

It does **not** authorize repository renames, repository consolidation, MG
Guide file migration between repos, gateway renames, Apps Script push, add-on
deploy, OAuth scope changes, IAM/IAP changes, HighLevel integration changes,
production data access, or any cross-repo implementation.

```text
ARCHITECTURE_FREEZE=YES
PRODUCT_SURFACE_DECISION=FROZEN_FOR_REVIEW
IMPLEMENTATION_WORKSTREAMS=DEFERRED_PENDING_GOVERNANCE_REVIEW
STOP_AFTER=planning_pr_open
```

---

## 1. Required product decisions (frozen)

```text
USER_FACING_PRODUCT=MG_GUIDE
DISPLAY_NAME=MG Guide
DISPLAY_ATTRIBUTION=Powered by AI Rolodex

AI_ROLODEX_ROLE=RELATIONSHIP_INTELLIGENCE_CAPABILITY
AI_ROLODEX_PRIMARY_USER_INTERFACE=NO_FOR_MG_GUIDE_SURFACE

WORKSPACE_ADDON_ROLE=MG_GUIDE_PRESENTATION_ADAPTER
MG_GUIDE_BACKEND_ROLE=WORKFLOW_AND_POLICY_TRUTH
```

### 1.1 Decision intent

| Decision | Meaning |
| --- | --- |
| `USER_FACING_PRODUCT=MG_GUIDE` | Salesperson and judge-facing product identity is **MG Guide**. |
| `DISPLAY_NAME=MG Guide` | Top-level chrome, titles, and navigation say **MG Guide**. |
| `DISPLAY_ATTRIBUTION=Powered by AI Rolodex` | Subtitle/footer attribution only; not a second product name in the primary title. |
| `AI_ROLODEX_ROLE=RELATIONSHIP_INTELLIGENCE_CAPABILITY` | AI Rolodex supplies relationship intelligence (context, resolution signals, relationship brief material). It is not the Workspace assistant brand. |
| `AI_ROLODEX_PRIMARY_USER_INTERFACE=NO_FOR_MG_GUIDE_SURFACE` | On the MG Guide Workspace surface, AI Rolodex must **not** appear as a competing primary assistant or alternate home. |
| `WORKSPACE_ADDON_ROLE=MG_GUIDE_PRESENTATION_ADAPTER` | Google Workspace Add-on renders CardService UI and routes user actions to MG Guide APIs. It does not own workflow truth. |
| `MG_GUIDE_BACKEND_ROLE=WORKFLOW_AND_POLICY_TRUTH` | MG Guide backend owns Meeting Follow-Up workflow execution views, deterministic policy outcomes, and demo/view-model contracts. |

### 1.2 Explicit non-decisions (out of scope for this artifact)

```text
REPOSITORY_RENAMES=NOT_AUTHORIZED
GATEWAY_INFRASTRUCTURE_RENAMES=NOT_AUTHORIZED
APPS_SCRIPT_PUSH=NOT_AUTHORIZED
ADDON_DEPLOY=NOT_AUTHORIZED
OAUTH_SCOPE_CHANGES=NOT_AUTHORIZED
IAM_IAP_CHANGES=NOT_AUTHORIZED
HIGHLEVEL_INTEGRATION_CHANGES=NOT_AUTHORIZED
PRODUCTION_CUSTOMER_DATA_TOUCH=NOT_AUTHORIZED
```

### 1.3 Current repository topology (not product boundary)

Product architecture (§1–§2) is **not** the same as git repository layout.
Existing MG Guide / Workspace add-on work already lives primarily outside this
competition workspace. This PR records that topology; it does **not** migrate
files or consolidate repositories.

```text
MAJORITY_PREEXISTING_MG_GUIDE_WORK_LOCATION=
themg-max/A.I-Rolodex---Context

WORKSPACE_ADDON_SOURCE_REPOSITORY=
themg-max/A.I-Rolodex---Context

PREEXISTING_MG_GUIDE_MIGRATION_TO_SEPARATE_REPO=NO

MG_GUIDE_AGENTIC_SALES_WORKSPACE_ROLE=
COMPETITION_WORKSPACE_AND_BOUNDED_NEW_DELTA

REPO_TOPOLOGY_IS_NOT_PRODUCT_BOUNDARY=YES
REPO_MIGRATION_REQUIRED_FOR_DEVPOST=NO
REPO_MIGRATION_AUTHORIZED=NO
```

| Field | Meaning |
| --- | --- |
| `MAJORITY_PREEXISTING_MG_GUIDE_WORK_LOCATION` | Most pre-existing MG Guide product/add-on work already resides in `themg-max/A.I-Rolodex---Context`, not in this public competition workspace. |
| `WORKSPACE_ADDON_SOURCE_REPOSITORY` | Google Workspace Add-on source repository identity for planning discovery. |
| `PREEXISTING_MG_GUIDE_MIGRATION_TO_SEPARATE_REPO` | **NO** — pre-existing MG Guide work is **not** being migrated into a new separate repo by this effort. |
| `MG_GUIDE_AGENTIC_SALES_WORKSPACE_ROLE` | This repo (`mg-guide-agentic-sales-workspace`) is the **competition workspace and bounded new delta** surface — not the historical home of the full MG Guide product tree. |
| `REPO_TOPOLOGY_IS_NOT_PRODUCT_BOUNDARY` | **YES** — repository boundaries must not be confused with the user-facing product boundary (`USER_FACING_PRODUCT=MG_GUIDE`). |
| `REPO_MIGRATION_REQUIRED_FOR_DEVPOST` | **NO** — Devpost/product integration does not require physical repo consolidation. |
| `REPO_MIGRATION_AUTHORIZED` | **NO** — no cross-repo file moves or consolidation are authorized by this PR. |

**Explicit topology statements for this PR:**

- No existing MG Guide files are being migrated by this PR.
- Logical product integration (MG Guide user surface powered by AI Rolodex
  relationship intelligence) does **not** require physical repository
  consolidation.
- Forbidden by this unit: moving MG Guide files between repositories,
  cross-repo implementation, Apps Script push, add-on deployment, OAuth/IAM/IAP
  changes, HighLevel/MCP execution, and production/customer data access.

---

## 2. Primary architecture

```text
Google Workspace Add-on
        |
        | MG Guide CardService UI
        | Powered by AI Rolodex
        v
MG Guide demo/view-model API
        |
        +-- Meeting Follow-Up workflow
        +-- deterministic policy
        +-- AI Rolodex relationship intelligence
```

### 2.1 Layer responsibilities

| Layer | Role | Owns | Must not own |
| --- | --- | --- | --- |
| **Google Workspace Add-on** | Presentation adapter | CardService layout, navigation chrome, routing of user intents to MG Guide APIs, display of returned view-models | Meeting extraction, relationship resolution, policy, stage decisions, CRM business logic, direct CRM/GHL calls |
| **MG Guide demo/view-model API** | Backend contract surface for the add-on and judge/demo clients | Scenario/view-model assembly, demo selectors, status/evidence packaging safe for UI | Unilateral mutation execution; private chain-of-thought exposure |
| **Meeting Follow-Up workflow** | Primary Devpost capability | `meeting_follow_up_v1` state progression and packet construction (existing competition slice) | Presenting itself as a separate product brand from MG Guide |
| **Deterministic policy** | Authorization truth | Allow/block/not_attempted outcomes, fail-closed ambiguity, mutation caps | Being bypassed by UI or relationship-intelligence suggestions |
| **AI Rolodex relationship intelligence** | Capability under MG Guide | Relationship context, candidate resolution signals, Relationship Brief content inputs | Primary Workspace assistant UI; competing top-level navigation brand |

### 2.2 Architecture guard (Apps Script / add-on)

```text
APPS_SCRIPT_RENDERS_AND_ROUTES_ONLY=YES
APPS_SCRIPT_MEETING_EXTRACTION=NO
APPS_SCRIPT_RELATIONSHIP_RESOLUTION=NO
APPS_SCRIPT_POLICY_EVALUATION=NO
APPS_SCRIPT_STAGE_DECISIONS=NO
APPS_SCRIPT_CRM_BUSINESS_LOGIC=NO
```

**Guard statement:** Apps Script renders and routes only. It does not perform
meeting extraction, relationship resolution, policy, stage decisions, or CRM
business logic. Those remain MG Guide backend / workflow / policy /
relationship-intelligence responsibilities.

### 2.3 Data / control flow (conceptual)

```text
User opens Workspace Add-on
  → CardService home (title: MG Guide; attribution: Powered by AI Rolodex)
  → User selects nav item
      - Meeting Follow-Up
      - Relationship Brief
      - Ask MG Guide
  → Add-on routes intent to MG Guide demo/view-model API
  → MG Guide assembles response from:
      - Meeting Follow-Up workflow packet/card contracts
      - Deterministic policy outcomes
      - AI Rolodex relationship-intelligence capability (where applicable)
  → Add-on renders returned view-model only
```

No live CRM side effects are authorized by this architecture unit
(see §5 Truth boundary).

---

## 3. Devpost primary capability and UI navigation

### 3.1 Primary capability

```text
DEVPOST_PRIMARY_CAPABILITY=Meeting Follow-Up
WORKFLOW=meeting_follow_up_v1
```

Meeting Follow-Up is the competition vertical slice and the default demo path.
Relationship Brief and Ask MG Guide are supporting navigation destinations on
the same MG Guide surface — not separate products.

### 3.2 Required UI navigation

| Nav item | Product framing | Backend truth source |
| --- | --- | --- |
| **Meeting Follow-Up** | Primary capability; governed post-meeting CRM follow-up | MG Guide Meeting Follow-Up workflow + card/view-model |
| **Relationship Brief** | Relationship-intelligence summary under MG Guide | MG Guide view-model fed by AI Rolodex relationship intelligence |
| **Ask MG Guide** | In-product Q&A against MG Guide workflow/context | MG Guide API; must not rebrand as “Ask AI Rolodex” on this surface |

### 3.3 Primary demo selectors

```text
PRIMARY_DEMO_SELECTORS=
  SUCCESS
  AMBIGUOUS_CONTACT
```

These bind to existing judge/demo scenario selectors already present in this
repository (`SUCCESS`, `AMBIGUOUS_CONTACT`). Architecture does not invent new
selector identities.

| Selector | Demo purpose |
| --- | --- |
| `SUCCESS` | Completed Meeting Follow-Up path with evidence; mutation intents shown only as planned/proposed/allowed/not_attempted per live truth boundary |
| `AMBIGUOUS_CONTACT` | Fail-closed governance path; blocked before CRM write; zero external effects |

Supporting selector inventory may remain available on the judge surface
(e.g. `STAGE_CHANGE_DENIED`) but is **not** required for the primary
Workspace add-on demo narrative frozen here.

---

## 4. Branding rules

```text
TOP_LEVEL_TITLE=MG Guide
SUBTITLE_OR_FOOTER=Powered by AI Rolodex
AI_ROLODEX_SECTION_ATTRIBUTION=ALLOWED_NEXT_TO_RELATIONSHIP_INTELLIGENCE_SECTIONS
AI_ROLODEX_AS_SECOND_COMPETING_ASSISTANT=FORBIDDEN
```

### 4.1 Required presentation

1. **Top-level title** = `MG Guide` (home card header, add-on name presentation, primary chrome).
2. **Subtitle / footer** = `Powered by AI Rolodex`.
3. **Section-level** AI Rolodex branding **may** appear next to relationship-intelligence sections (e.g. Relationship Brief body attribution).
4. **Do not** present AI Rolodex as a second competing assistant, second home, or parallel top-level chat product on the MG Guide surface.

### 4.2 Copy anti-patterns (forbidden on MG Guide surface)

| Forbidden | Required alternative |
| --- | --- |
| “Open AI Rolodex” as primary CTA | “Open MG Guide” / Meeting Follow-Up entry |
| Dual home: MG Guide **and** AI Rolodex assistants | Single home: MG Guide |
| “Ask AI Rolodex” as primary nav | “Ask MG Guide” |
| Dropping attribution entirely | Keep `Powered by AI Rolodex` in subtitle/footer |

### 4.3 Public/private branding note

Per existing governance, the **private AI Rolodex context repository**
(`themg-max/A.I-Rolodex---Context`) remains governance / source-authority
control plane and the identified location of majority pre-existing MG Guide /
Workspace add-on work (§1.3). That private control-plane **and repository
topology** role is **orthogonal** to the user-facing product brand frozen here:

- Private lane: AI Rolodex context repo = governance authority + majority
  pre-existing MG Guide/add-on work location (unchanged by this PR).
- Public competition workspace: bounded new delta + judge/demo contracts
  (`mg-guide-agentic-sales-workspace`).
- Public user surface brand: MG Guide = assistant brand; AI Rolodex =
  capability + attribution.
- Repo topology is **not** the product boundary; no file migration is authorized.

---

## 5. Truth boundary

```text
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
PRODUCTION_DATA_USED=NO
GMAIL_MESSAGE_DATA_REQUIRED_FOR_SYNTHETIC_DEMO=NO
EXTERNAL_EFFECTS=0
```

### 5.1 Demo / architecture claims allowed

- Synthetic fixture-driven Meeting Follow-Up outcomes (`SUCCESS`, `AMBIGUOUS_CONTACT`).
- Deterministic policy outcomes as emitted by MG Guide contracts/runner/card surfaces.
- Relationship intelligence **presented** as capability-backed view-model content without claiming live production CRM reads/writes.
- UI navigation and branding structure described in this document.

### 5.2 Claims forbidden by this unit

| Claim | Status |
| --- | --- |
| Live GHL/MCP calls performed for this architecture PR | **NO** |
| CRM mutations performed | **NO** |
| Live CRM execution performed | **NOT_PERFORMED** |
| Production or customer data used | **NO** |
| Gmail message bodies/headers required to run synthetic demo | **NO** |
| External effects count | **0** |
| Proposed actions labeled as executed/verified in CRM | **NO** |
| Apps Script owns policy or CRM logic | **NO** |

### 5.3 Alignment with existing demo truth

**Authoritative on `main` today** (merged PR #87 synthetic demo plan
`docs/demo/meeting-follow-up-demo-v1.md`):

```text
DEMO_TRUTH_BOUNDARY=synthetic_offline_only
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
PRODUCTION_OR_CUSTOMER_DATA=NO
EXTERNAL_EFFECTS=0
PRIMARY_DEMO_SELECTORS=SUCCESS,AMBIGUOUS_CONTACT
AMBIGUOUS_PATH=fail_closed_blocked_zero_crm_writes
MUTATION_INTENTS_SHOWN_AS=planned_proposed_allowed_blocked
CANONICAL_FIXTURE_VALUES_CONTROL_VISIBLE_DEMO=YES
```

This architecture **inherits only those main-authoritative** competition-safe
keys. Synthetic/offline truth, fail-closed ambiguity with zero CRM writes, and
`LIVE_CRM_EXECUTION=NOT_PERFORMED` remain binding here.

**Meeting Follow-Up live-truth normalization — not yet authoritative on
`main`:**

A separate live-truth normalization unit (branch
`planning/meeting-follow-up-demo-live-truth-normalization-001`, not merged as of
this architecture freeze) may later refine presenter/runtime field authority,
including values such as:

```text
DEMO_RUNTIME_FIELD_AUTHORITY=LIVE_JUDGE_RUNNER_PACKET_AND_CARD
NW006_STATIC_SNAPSHOT_ROLE=REFERENCE_ONLY_WHEN_DIFFERENT_FROM_LIVE_JUDGE_PATH
AMBIGUOUS_RAW_POLICY_NOTE_WRITE=not_attempted
AMBIGUOUS_RAW_POLICY_STAGE_WRITE=not_attempted
AMBIGUOUS_GOVERNANCE_OUTCOME=blocked
```

**Reconciliation rule:** do **not** assert those normalization-only fields as
authoritative on `main` until that unit is separately reviewed and merged.
Until then, this PR’s §5 truth boundary stays aligned to the PR #87 main text
above; any tighter live-runner presenter authority is deferred and must not be
back-dated as already-main truth by this architecture artifact.

---

## 6. Component contracts (planning level)

### 6.1 Workspace Add-on → MG Guide

```text
DIRECTION=addon_to_mg_guide
TRANSPORT=HTTPS_TO_MG_GUIDE_DEMO_VIEW_MODEL_API
PAYLOAD_STYLE=view_model_json_or_card_dto
AUTH_CONTRACT=SEE_RESOLVE_SECTION_7
SIDE_EFFECTS_FROM_ADDON=NONE_AUTHORIZED
```

Conceptual operations (names not frozen as implementation identifiers):

| Intent | Expected backend behavior |
| --- | --- |
| `home` | Return MG Guide home chrome + nav + attribution |
| `meeting_follow_up` | Return Meeting Follow-Up card/view-model for selected demo scenario |
| `relationship_brief` | Return relationship brief view-model (Rolodex capability-backed) |
| `ask_mg_guide` | Return Q&A / guidance view-model under MG Guide brand |

### 6.2 MG Guide backend internal composition

```text
MG Guide demo/view-model API
  ├── Meeting Follow-Up workflow (packets, states, card mapper contracts)
  ├── Deterministic policy (allow / block / not_attempted)
  └── AI Rolodex relationship intelligence (capability invocation boundary)
```

Existing public-repo anchors to reuse (not re-implement in this PR):

| Anchor | Path / surface |
| --- | --- |
| Meeting Follow-Up foundation | `docs/MEETING_FOLLOW_UP_FOUNDATION.md` |
| Card contract | `contracts/mg_guide_meeting_follow_up_card.schema.json` |
| Packet contract | `contracts/meeting_follow_up_packet.schema.json` |
| Relationship context contract | `contracts/relationship_context.schema.json` |
| Judge scenario selectors | `src/mg_guide/judge_surface/scenarios.py` (`SUCCESS`, `AMBIGUOUS_CONTACT`, …) |
| Card module | `src/mg_guide/meeting_follow_up_card/` |
| Synthetic demo plan | `docs/demo/meeting-follow-up-demo-v1.md` |

### 6.3 AI Rolodex capability boundary

```text
CAPABILITY_NAME=relationship_intelligence
PRIMARY_UI=NO_FOR_MG_GUIDE_SURFACE
CONSUMED_BY=MG_GUIDE_BACKEND
EXPOSED_TO_USER_AS=MG_GUIDE_SECTIONS_WITH_OPTIONAL_SECTION_ATTRIBUTION
```

AI Rolodex may inform:

- contact/relationship candidate context,
- Relationship Brief content,
- evidence used by MG Guide to explain resolution quality,

…but **must not**:

- become the Workspace add-on product title,
- own deterministic policy allow/deny,
- perform CRM mutations outside MG Guide / OL3 policy gates,
- appear as a second assistant home beside MG Guide.

---

## 7. Resolve and record (discovery status)

Topology identity is recorded in §1.3. This section records add-on discovery
and remaining unknowns. Identifying the source repository is **not** authority
to migrate files, push Apps Script, deploy the add-on, or implement cross-repo
wiring.

```text
ADDON_SOURCE_REPOSITORY_IDENTIFIED=YES
ADDON_SOURCE_REPOSITORY=themg-max/A.I-Rolodex---Context
ADDON_APPS_SCRIPT_PROJECT_BINDING_IDENTIFIED=YES

ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED=NO
ADDON_RUNTIME_SOURCE_FILE_AUTHORITY=UNKNOWN

ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN
CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN
```

### 7.1 Add-on source repository and Apps Script project binding

```text
ADDON_SOURCE_REPOSITORY_IDENTIFIED=YES
ADDON_SOURCE_REPOSITORY=themg-max/A.I-Rolodex---Context
ADDON_APPS_SCRIPT_PROJECT_BINDING_IDENTIFIED=YES
```

**Finding:** The Workspace add-on source repository is identified as
`themg-max/A.I-Rolodex---Context` (same location as majority pre-existing MG
Guide work; see §1.3). Apps Script project binding to that source repository is
identified at planning level.

**Implication:** Future add-on work, **if authorized**, is expected to reference
that repository — not to invent a new host repo or to treat this competition
workspace as the historical add-on SoT. This PR still does **not** open that
repository for implementation, does **not** migrate MG Guide files, and does
**not** authorize clasp push/deploy.

### 7.2 Deployed revision and runtime source-file authority (still open)

```text
ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED=NO
ADDON_RUNTIME_SOURCE_FILE_AUTHORITY=UNKNOWN
```

**Finding:** Which exact source revision is currently deployed, and which
checked-in files are runtime-authoritative for that deployment, are **not**
established by this planning unit.

**Rule:** Repository identity ≠ deployed revision identity ≠ runtime file
authority. Do not treat “source repo known” as “safe to edit/deploy.”

### 7.3 `ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN`

**Finding:** No published contract in this repository defines how the Workspace
Add-on authenticates to the MG Guide demo/view-model API (e.g., IAP audience,
service account, OAuth user grant, identity-aware proxy user forwarding, or
signed app-to-app token).

**Related but distinct:** NW-007 documents IAP authentication for the **judge
surface** Cloud Run service. That judge-surface IAP posture is **not** accepted
here as the add-on→MG Guide auth contract until explicitly bound by a later
architecture/implementation grant.

### 7.4 `CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN`

**Finding:** No single, evidenced permission-block root cause is recorded in
this public repo specifically for Workspace Add-on → MG Guide access.

Possible future investigation classes (not diagnosed here):

- missing add-on OAuth scopes,
- IAP audience / member mismatch,
- absent service identity binding,
- unpublished private endpoint allowlisting,
- clasp/script project ownership gaps.

**Rule:** Do not guess a root cause. Record `UNKNOWN` until a bounded discovery
grant produces evidence.

### 7.5 Resolve matrix

| Field | Value | Evidence basis |
| --- | --- | --- |
| `ADDON_SOURCE_REPOSITORY_IDENTIFIED` | `YES` | Planning identity: `themg-max/A.I-Rolodex---Context` |
| `ADDON_SOURCE_REPOSITORY` | `themg-max/A.I-Rolodex---Context` | Same as majority pre-existing MG Guide / add-on work location (§1.3) |
| `ADDON_APPS_SCRIPT_PROJECT_BINDING_IDENTIFIED` | `YES` | Apps Script project binding identified at planning level to that source repo |
| `ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED` | `NO` | No evidenced pin of currently deployed revision in this unit |
| `ADDON_RUNTIME_SOURCE_FILE_AUTHORITY` | `UNKNOWN` | Runtime-authoritative file set for deployed add-on not established here |
| `ADDON_TO_MG_GUIDE_AUTH_CONTRACT` | `UNKNOWN` | No add-on→API auth contract published here; judge IAP ≠ add-on contract |
| `CURRENT_PERMISSION_BLOCK_CAUSE` | `UNKNOWN` | No evidenced add-on permission-block RCA in public artifacts |

---

## 8. Governance and stop conditions

### 8.1 What this PR may do

- Create/update this planning-only architecture artifact.
- Open a **planning-only** PR for architecture/governance review.
- Record product, branding, navigation, truth-boundary, current-state
  repository topology, and resolve fields.
- Distinguish existing repo topology from target MG Guide product architecture
  without moving code.

### 8.2 What this PR must not do

```text
DO_NOT_RENAME_REPOSITORIES=YES
DO_NOT_RENAME_GATEWAY_INFRASTRUCTURE=YES
DO_NOT_MIGRATE_MG_GUIDE_FILES_BETWEEN_REPOS=YES
DO_NOT_CONSOLIDATE_REPOSITORIES=YES
DO_NOT_PUSH_APPS_SCRIPT=YES
DO_NOT_DEPLOY_ADDON=YES
DO_NOT_CHANGE_OAUTH_SCOPES=YES
DO_NOT_CHANGE_IAM_OR_IAP=YES
DO_NOT_MODIFY_HIGHLEVEL_INTEGRATION=YES
DO_NOT_TOUCH_PRODUCTION_CUSTOMER_DATA=YES
DO_NOT_IMPLEMENT_CROSS_REPO_WIRING=YES
DO_NOT_CLAIM_LIVE_CRM_EXECUTION=YES
DO_NOT_ASSERT_UNMERGED_LIVE_TRUTH_NORMALIZATION_AS_MAIN=YES
```

### 8.3 Required stop

```text
STOP_FOR=architecture_governance_review
NEXT_ONLY_AFTER=explicit_implementation_grant
CROSS_REPO_IMPLEMENTATION=BLOCKED_UNTIL_REVIEW
```

**STOP** after the planning-only PR is open. Do not begin cross-repo
implementation, add-on source moves, or auth wiring until architecture and
governance review accepts this freeze (or issues a superseding decision).

### 8.4 Suggested review checklist (human)

1. Confirm MG Guide remains sole primary user-facing assistant brand.
2. Confirm AI Rolodex attribution + capability role (not competing UI).
3. Confirm Apps Script render/route-only guard.
4. Confirm demo selectors `SUCCESS` + `AMBIGUOUS_CONTACT` and §5 truth boundary
   as **main-authoritative** (PR #87); do not require unmerged live-truth
   normalization fields for this freeze.
5. Confirm §1.3 topology: majority pre-existing work + add-on source in
   `themg-max/A.I-Rolodex---Context`; this repo = competition workspace +
   bounded new delta; no migration required/authorized.
6. Accept or replace the §7 resolve fields (source repo/binding identified;
   deployed revision + runtime file authority + auth contract + permission
   block still open/unknown).
7. Only then authorize bounded follow-on workstreams (deployed-revision
   discovery, auth contract design, synthetic view-model adapter, etc.).

---

## 9. Deferred workstreams (not authorized by this artifact)

Ordered for later grants; **none** are in scope now:

| ID | Workstream | Depends on |
| --- | --- | --- |
| W1 | Pin add-on deployed source revision + runtime source-file authority (repo already identified: `themg-max/A.I-Rolodex---Context`) | Governance discovery grant; no migration |
| W2 | Define add-on → MG Guide auth contract | W1 + security review |
| W3 | Diagnose permission-block cause (if any) with evidence | W2 |
| W4 | CardService navigation shell (MG Guide chrome + attribution) | W1–W2 + implementation grant |
| W5 | Meeting Follow-Up view-model binding to existing card/packet contracts | W4 |
| W6 | Relationship Brief view-model via Rolodex capability boundary | W4 + capability contract |
| W7 | Ask MG Guide view-model (non-competing Q&A) | W4 |
| W8 | Synthetic demo rehearsal on add-on surface (`SUCCESS`, `AMBIGUOUS_CONTACT`) | W5 + truth boundary intact |
| W9 | Consume Meeting Follow-Up live-truth normalization once merged to `main` (presenter authority = live judge runner) | Separate demo normalization PR merge |

Each workstream requires its own exact writable scope and proof posture.
No workstream implies MG Guide file migration or repository consolidation.

---

## 10. Verification for this planning unit

```bash
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

Expected:

- Architecture markdown only in the commit scope.
- Phase-1 deterministic verification remains green (no runtime code changes).
- No secrets, private endpoints, or production identifiers introduced.

---

## 11. Related artifacts

| Artifact | Role |
| --- | --- |
| [`../MEETING_FOLLOW_UP_FOUNDATION.md`](../MEETING_FOLLOW_UP_FOUNDATION.md) | Frozen vertical-slice foundation |
| [`../demo/meeting-follow-up-demo-v1.md`](../demo/meeting-follow-up-demo-v1.md) | Synthetic demo truth + selectors |
| [`../COMPETITION_BASELINE.md`](../COMPETITION_BASELINE.md) | Pre-existing vs new-work split |
| [`../SECURITY.md`](../SECURITY.md) | Security/privacy non-negotiables |
| [`../../governance/README.md`](../../governance/README.md) | Public governance binding; AI Rolodex private control-plane role |
| [`../../governance/PUBLIC_PRIVATE_BOUNDARY.md`](../../governance/PUBLIC_PRIVATE_BOUNDARY.md) | Public/private boundary |
| [`../../README.md`](../../README.md) | Repository status and architecture summary |

---

## 12. One-page freeze summary

```text
USER_FACING_PRODUCT=MG_GUIDE
DISPLAY_NAME=MG Guide
DISPLAY_ATTRIBUTION=Powered by AI Rolodex
AI_ROLODEX_ROLE=RELATIONSHIP_INTELLIGENCE_CAPABILITY
AI_ROLODEX_PRIMARY_USER_INTERFACE=NO_FOR_MG_GUIDE_SURFACE
WORKSPACE_ADDON_ROLE=MG_GUIDE_PRESENTATION_ADAPTER
MG_GUIDE_BACKEND_ROLE=WORKFLOW_AND_POLICY_TRUTH
DEVPOST_PRIMARY_CAPABILITY=Meeting Follow-Up
UI_NAV=Meeting Follow-Up | Relationship Brief | Ask MG Guide
PRIMARY_DEMO_SELECTORS=SUCCESS,AMBIGUOUS_CONTACT
LIVE_GHL_CALLS=NO
CRM_MUTATIONS_PERFORMED=NO
LIVE_CRM_EXECUTION=NOT_PERFORMED
PRODUCTION_DATA_USED=NO
GMAIL_MESSAGE_DATA_REQUIRED_FOR_SYNTHETIC_DEMO=NO
EXTERNAL_EFFECTS=0
APPS_SCRIPT_RENDERS_AND_ROUTES_ONLY=YES

MAJORITY_PREEXISTING_MG_GUIDE_WORK_LOCATION=themg-max/A.I-Rolodex---Context
WORKSPACE_ADDON_SOURCE_REPOSITORY=themg-max/A.I-Rolodex---Context
PREEXISTING_MG_GUIDE_MIGRATION_TO_SEPARATE_REPO=NO
MG_GUIDE_AGENTIC_SALES_WORKSPACE_ROLE=COMPETITION_WORKSPACE_AND_BOUNDED_NEW_DELTA
REPO_TOPOLOGY_IS_NOT_PRODUCT_BOUNDARY=YES
REPO_MIGRATION_REQUIRED_FOR_DEVPOST=NO
REPO_MIGRATION_AUTHORIZED=NO
NO_MG_GUIDE_FILE_MIGRATION_IN_THIS_PR=YES
LOGICAL_PRODUCT_INTEGRATION_REQUIRES_PHYSICAL_REPO_CONSOLIDATION=NO

ADDON_SOURCE_REPOSITORY_IDENTIFIED=YES
ADDON_SOURCE_REPOSITORY=themg-max/A.I-Rolodex---Context
ADDON_APPS_SCRIPT_PROJECT_BINDING_IDENTIFIED=YES
ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED=NO
ADDON_RUNTIME_SOURCE_FILE_AUTHORITY=UNKNOWN
ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN
CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN

MEETING_FOLLOW_UP_DEMO_TRUTH_AUTHORITY_ON_MAIN=PR87_SYNTHETIC_DEMO_PLAN
LIVE_TRUTH_NORMALIZATION_AUTHORITATIVE_ON_MAIN=NO

IMPLEMENTATION_AUTHORIZED=NO
CROSS_REPO_IMPLEMENTATION_AUTHORIZED=NO
STOP_FOR=architecture_governance_review
```
