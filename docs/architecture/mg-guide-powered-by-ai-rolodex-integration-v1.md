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
COMPETITION_SAFE=YES
IMPLEMENTATION_AUTHORIZED=NO
CROSS_REPO_IMPLEMENTATION_AUTHORIZED=NO
RUNTIME_CHANGES_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

This unit is **planning / architecture only**. It freezes product role,
presentation, and truth-boundary decisions so MG Guide is the primary
user-facing Workspace assistant and AI Rolodex is the underlying
relationship-intelligence capability.

It does **not** authorize repository renames, gateway renames, Apps Script
push, add-on deploy, OAuth scope changes, IAM/IAP changes, HighLevel
integration changes, production data access, or any cross-repo implementation.

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

Per existing governance, the **private AI Rolodex context repository** remains
governance / source-authority control plane. That private control-plane role is
**orthogonal** to the user-facing product brand frozen here:

- Private lane: AI Rolodex context repo = governance authority (unchanged).
- Public user surface: MG Guide = assistant brand; AI Rolodex = capability + attribution.

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

This architecture inherits the competition-safe posture already documented for
the synthetic Meeting Follow-Up demo unit (`docs/demo/meeting-follow-up-demo-v1.md`
on `main`): synthetic/offline truth, presenter values bound to live judge
runner packet/card when demonstrated, and fail-closed ambiguity with zero CRM
writes.

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

These fields are deliberately resolved against **this public repository and
published artifacts only**. Private control-plane details are not invented.

```text
ADDON_SOURCE_OF_TRUTH_IDENTIFIED=NO
ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN
CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN
```

### 7.1 `ADDON_SOURCE_OF_TRUTH_IDENTIFIED=NO`

**Finding:** This public repository does **not** contain Google Workspace
Add-on / Apps Script project source, clasp config, or a documented path to the
add-on source-of-truth tree.

**Implication:** Add-on implementation work cannot begin from this repo alone.
A later governed discovery must identify the authoritative add-on source
location (likely private/control-plane or a separate host repo) without
violating the public/private boundary.

### 7.2 `ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN`

**Finding:** No published contract in this repository defines how the Workspace
Add-on authenticates to the MG Guide demo/view-model API (e.g., IAP audience,
service account, OAuth user grant, identity-aware proxy user forwarding, or
signed app-to-app token).

**Related but distinct:** NW-007 documents IAP authentication for the **judge
surface** Cloud Run service. That judge-surface IAP posture is **not** accepted
here as the add-on→MG Guide auth contract until explicitly bound by a later
architecture/implementation grant.

### 7.3 `CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN`

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

### 7.4 Resolve matrix

| Field | Value | Evidence basis |
| --- | --- | --- |
| `ADDON_SOURCE_OF_TRUTH_IDENTIFIED` | `NO` | No add-on/Apps Script source tree in this public repo |
| `ADDON_TO_MG_GUIDE_AUTH_CONTRACT` | `UNKNOWN` | No add-on→API auth contract published here; judge IAP ≠ add-on contract |
| `CURRENT_PERMISSION_BLOCK_CAUSE` | `UNKNOWN` | No evidenced add-on permission-block RCA in public artifacts |

---

## 8. Governance and stop conditions

### 8.1 What this PR may do

- Create this planning-only architecture artifact.
- Open a **planning-only** PR for architecture/governance review.
- Record product, branding, navigation, truth-boundary, and resolve fields.

### 8.2 What this PR must not do

```text
DO_NOT_RENAME_REPOSITORIES=YES
DO_NOT_RENAME_GATEWAY_INFRASTRUCTURE=YES
DO_NOT_PUSH_APPS_SCRIPT=YES
DO_NOT_DEPLOY_ADDON=YES
DO_NOT_CHANGE_OAUTH_SCOPES=YES
DO_NOT_CHANGE_IAM_OR_IAP=YES
DO_NOT_MODIFY_HIGHLEVEL_INTEGRATION=YES
DO_NOT_TOUCH_PRODUCTION_CUSTOMER_DATA=YES
DO_NOT_IMPLEMENT_CROSS_REPO_WIRING=YES
DO_NOT_CLAIM_LIVE_CRM_EXECUTION=YES
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
4. Confirm demo selectors `SUCCESS` + `AMBIGUOUS_CONTACT` and truth boundary.
5. Accept or replace the three resolve fields in §7.
6. Only then authorize bounded follow-on workstreams (discovery of add-on SoT,
   auth contract design, synthetic view-model adapter, etc.).

---

## 9. Deferred workstreams (not authorized by this artifact)

Ordered for later grants; **none** are in scope now:

| ID | Workstream | Depends on |
| --- | --- | --- |
| W1 | Identify add-on source-of-truth repository/path | Governance discovery grant |
| W2 | Define add-on → MG Guide auth contract | W1 + security review |
| W3 | Diagnose permission-block cause (if any) with evidence | W2 |
| W4 | CardService navigation shell (MG Guide chrome + attribution) | W1–W2 + implementation grant |
| W5 | Meeting Follow-Up view-model binding to existing card/packet contracts | W4 |
| W6 | Relationship Brief view-model via Rolodex capability boundary | W4 + capability contract |
| W7 | Ask MG Guide view-model (non-competing Q&A) | W4 |
| W8 | Synthetic demo rehearsal on add-on surface (`SUCCESS`, `AMBIGUOUS_CONTACT`) | W5 + truth boundary intact |

Each workstream requires its own exact writable scope and proof posture.

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
ADDON_SOURCE_OF_TRUTH_IDENTIFIED=NO
ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN
CURRENT_PERMISSION_BLOCK_CAUSE=UNKNOWN
IMPLEMENTATION_AUTHORIZED=NO
STOP_FOR=architecture_governance_review
```
