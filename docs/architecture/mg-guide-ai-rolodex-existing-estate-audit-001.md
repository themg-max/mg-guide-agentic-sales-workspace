# MG Guide / AI Rolodex — Existing-Estate Audit 001 (Public Architecture Decision Summary)

## 0. Identity

```text
ARTIFACT=docs/architecture/mg-guide-ai-rolodex-existing-estate-audit-001.md
UNIT=MG_GUIDE_AI_ROLODEX_EXISTING_ESTATE_AUDIT_001
ARTIFACT_CLASS=public_safe_architecture_decision_summary
OWNER=VS Code / MG Orchestrator
BRANCH=planning/mg-guide-ai-rolodex-existing-estate-audit-001
BASE_REF=origin/main
BASE_SHA=aff6e3a3c047cfd57e82f997097704cd3aefe886
BASE_AUTHORITY=PR88 merge commit (mg-guide-powered-by-ai-rolodex-integration-v1)
CREATED_AT_LOCAL=2026-08-18T12:35:00-04:00
```

This artifact is the **public-safe decision summary** of a read-only audit of
the existing MG Guide + Workspace Add-on estate, performed to identify the
smallest reuse seam for the Devpost **Meeting Follow-Up** experience. The
full detailed audit (with deployment evidence, file/line citations, and
internal configuration) is preserved **privately** inside the governed OL3
lane process of the private source-authority repository, per the cross-repo
orchestration bridge. This public summary records **decisions and their
rationale only**.

```text
RUNTIME_MUTATION=0
DEPLOYMENT=0
CLASP_PUSH=0
APPS_SCRIPT_DEPLOY=0
OAUTH_SCOPE_CHANGES=0
IAM_IAP_CHANGES=0
PERMISSION_GRANTS=0
GHL_MCP_CALLS=0
PRODUCTION_CUSTOMER_DATA_TOUCH=0
REPO_MIGRATION=0
```

### 0.1 Public/private boundary

```text
PRIVATE_ENDPOINTS_IN_PUBLIC_ARTIFACT=NO
PRIVATE_IDS_IN_PUBLIC_ARTIFACT=NO
PRIVATE_RUNTIME_CONFIG_IN_PUBLIC_ARTIFACT=NO
PRIVATE_AI_ARTIFACT_CONTENT_COPIED=NO
```

This summary intentionally omits: private service URLs/endpoints, Apps Script
project identifiers, cloud project identifiers, service-account identities,
secret names, workload-identity pool/provider configuration, deployment
revisions, exact private `.ai` artifact contents, and any other internal IDs
or configuration. Where a finding depends on such a value, the value is
described by role (e.g. "the deployed MG Guide production service") and the
evidence remains in the private governed record.

### 0.2 Product freeze (carried from PR88, unchanged)

```text
USER_FACING_PRODUCT=MG_GUIDE
DISPLAY_NAME=MG Guide
DISPLAY_ATTRIBUTION=Powered by AI Rolodex
AI_ROLODEX_ROLE=RELATIONSHIP_INTELLIGENCE_CAPABILITY
REPO_TOPOLOGY_IS_NOT_PRODUCT_BOUNDARY=YES
REPO_MIGRATION_REQUIRED_FOR_DEVPOST=NO
REPO_MIGRATION_AUTHORIZED=NO
```

---

## 1. Audit scope (summary)

The audit read only the previously authorized surfaces in the private source
repository: the MG Guide integration plan, deployment status, SQL fix status,
and runtime-identity-hardening documents; the consumer-side MG Guide HTTP
client module; the Workspace Add-on manifest, clasp binding, and both
checked-in runtime source files; the directly referenced MG Guide service
tree (existence only); and the targeted `mg-guide` entries in the private
lane/review/feature-memory control plane. No unrelated areas were scanned;
no runtime, deployment, or auth-path testing was performed.

---

## 2. Component reuse classification (public level)

| Component | Reusability | Public-safe rationale |
| --- | --- | --- |
| **Existing Google Workspace Add-on** (Apps Script, CardService) | `WITH_CHANGES` | Only existing Workspace presentation surface; its render-and-route shape already matches the PR88 add-on guard. Needs branding conformance (currently presented under the capability brand, not `MG Guide`), a Meeting Follow-Up card/route, and resolution of a source-level ambiguity about which checked-in file is runtime-authoritative before any edit could be safe. |
| **Existing public judge/demo backend** (`src/mg_guide/judge_surface/`, incl. `POST /demo/meeting-follow-up`) | `YES` | Already serves fixed synthetic scenario selectors (`SUCCESS`, `AMBIGUOUS_CONTACT`) from the existing WorkflowRunner + packet/card truth; already competition-safe (`synthetic_offline_only`, `EXTERNAL_EFFECTS=0`). |
| **Legacy MG Guide production service** (private deployment) | `WITH_CHANGES` — but `NO_BY_DEFAULT` as demo host | Architecturally mature (locked delivery-executor separation, WIF-only CI/CD, observability posture), but it is a production leadership-pulse service; coupling the public synthetic demo to it would add unnecessary production entanglement. Retained as the future live-path host candidate, not the demo host. |
| **AI Rolodex relationship-intelligence capability** (private resolver/intelligence services) | `WITH_CHANGES` (as designed capability seam) | Exists and is operationally documented, but the demo truth boundary forbids live relationship/CRM reads. Reuse is as **capability-framed synthetic view-model content**, designed but not invoked at runtime in the synthetic demo. |
| **Private MCP decision engine / CRM intelligence backend / snapshot store** | Out of demo path | Precedents for decision/execution separation; not part of the synthetic demo seam. |
| **Public Meeting Follow-Up contracts** (`contracts/meeting_follow_up_packet.schema.json`, `contracts/mg_guide_meeting_follow_up_card.schema.json`, `contracts/relationship_context.schema.json`, judge scenarios, card module) | `AS_IS` | Smallest existing truth surface; no new contracts needed. |

---

## 3. Required decisions

```text
EXISTING_WORKSPACE_ADDON_REUSABLE=WITH_CHANGES
EXISTING_PUBLIC_JUDGE_BACKEND_REUSABLE=YES
PREFERRED_SYNTHETIC_DEMO_BACKEND=PUBLIC_JUDGE_SURFACE
NEW_BACKEND_REQUIRED_FOR_SYNTHETIC_DEMO=NO
NEW_FRONTEND_REQUIRED=NO
MEETING_FOLLOW_UP_INTEGRATION_SEAM_IDENTIFIED=YES

LEGACY_MG_GUIDE_PRODUCTION_SERVICE_AS_DEMO_HOST=NO_BY_DEFAULT

AI_ROLODEX_CAPABILITY_SEAM_DESIGNED=YES
AI_ROLODEX_RUNTIME_INVOCATION_IN_SYNTHETIC_DEMO=NO
LIVE_AI_ROLODEX_RELATIONSHIP_READS=NO

ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED=NO
ADDON_RUNTIME_SOURCE_FILE_AUTHORITY=UNKNOWN
ADDON_TO_MG_GUIDE_AUTH_CONTRACT=UNKNOWN
```

### 3.1 Decision rationale

- **`PREFERRED_SYNTHETIC_DEMO_BACKEND=PUBLIC_JUDGE_SURFACE`**: the public judge
  surface already exposes the demo route, already runs the WorkflowRunner over
  canonical fixtures, and already carries the merged PR #87/#88 truth boundary.
  Reusing it keeps the demo self-contained, competition-safe, and free of any
  private production coupling.
- **`LEGACY_MG_GUIDE_PRODUCTION_SERVICE_AS_DEMO_HOST=NO_BY_DEFAULT`**: the
  private production service remains the candidate host for any *future live*
  Meeting Follow-Up capability, but the synthetic demo must not depend on it.
- **`NEW_FRONTEND_REQUIRED=NO`**: the existing add-on is the frontend; only an
  in-place, presentation-layer adapter delta is implied, after the deployed
  source-revision and runtime-file-authority unknowns are resolved read-only.
- **AI Rolodex seam**: designed at the capability boundary (relationship
  brief content, candidate-resolution context, evidence framing) and frozen to
  `AI_ROLODEX_RUNTIME_INVOCATION_IN_SYNTHETIC_DEMO=NO` /
  `LIVE_AI_ROLODEX_RELATIONSHIP_READS=NO` per the standing truth boundary.
- **Auth**: four *distinct* pre-existing auth contracts were observed in the
  estate (add-on→gateway user identity token; backend→MCP API key;
  backend→resolver OIDC service-to-service; consumer→MG-Guide MCP API-key
  header). **None** of them is a published add-on→demo-backend contract, and
  the judge-surface IAP posture (NW-007) is explicitly not accepted as one
  (PR88 §7.3). No new auth path was invented or tested.

---

## 4. Deployed add-on discovery (public-safe summary)

```text
ADDON_DEPLOYED_SOURCE_REVISION_IDENTIFIED=NO
ADDON_RUNTIME_SOURCE_FILE_AUTHORITY=UNKNOWN
DEPLOYED_API_BASE_URL=UNKNOWN
DEPLOYED_MANIFEST_REVISION=UNKNOWN
```

Source-only findings (no clasp/deployment reads performed; full evidence in
the private governed record):

1. Two checked-in runtime source files define the same add-on entry points and
   **disagree on the backend base URL**; the manifest's fetch whitelist matches
   only one of the two candidate values.
2. The push tooling configuration does not establish file ordering or which
   file wins at runtime.
3. Therefore: repository identity ≠ deployed revision ≠ runtime file authority
   (PR88 §7.2 rule upheld). All four deployed-source fields stay
   `NO`/`UNKNOWN` pending a bounded read-only deployment-inspection grant.

### 4.1 Security observation (record only — no remediation here)

```text
RAW_IDENTITY_TOKEN_LOGGING_PRESENT=YES
```

The checked-in add-on source logs the raw user identity token (including on an
error path) to the script execution log. Recorded for architecture review;
**not** remediated in this unit. Removal is queued as a separately governed
private change (see §7).

---

## 5. Public seam (smallest proposed integration seam)

```text
Existing Workspace Add-on (render-and-route only)
  -> auth contract TBD
  -> existing POST /demo/meeting-follow-up
  -> additive demo_stages JSON projection
  -> existing WorkflowRunner + packet/card truth
```

| Seam element | Status |
| --- | --- |
| Existing Workspace Add-on | Exists (private source repo); reuse `WITH_CHANGES` |
| Auth contract | `UNKNOWN` — to be designed (Unit C item 4); nothing invented here |
| `POST /demo/meeting-follow-up` | **Exists** in `src/mg_guide/judge_surface/app.py` |
| `demo_stages` JSON projection | **Additive/planned** — a stage-by-stage JSON projection of the existing packet/card truth, shaped for CardService rendering; does not exist yet |
| WorkflowRunner + packet/card truth | **Exists** (`src/orchestration/runner.py`, `contracts/`, `src/mg_guide/meeting_follow_up_card/`) |

Why this is the smallest seam: no new frontend, no new backend, no new
contracts, no repo migration, no live CRM/GHL path, no auth invention. The
only new artifact implied is the additive `demo_stages` projection inside the
existing public judge surface.

---

## 6. Remaining unknowns

| # | Unknown | Blocking? | Resolution path |
| --- | --- | --- | --- |
| Q1 | Deployed add-on source revision + runtime file authority (which checked-in file is authoritative) | Yes, before any add-on edit | Bounded read-only deployment-inspection grant (private) |
| Q2 | Deployed manifest revision | Yes, before branding conformance work | Same grant as Q1 |
| Q3 | Add-on → public judge/demo surface auth contract | Yes, before any live add-on→API call | Auth contract design (Unit C item 4) under explicit grant |
| Q4 | Permission-block root cause for add-on→MG Guide access (carried from PR88 §7.4) | Yes | Bounded discovery grant; do not guess |
| Q5 | Unmerged live-truth normalization effect on demo field authority | Demo copy accuracy only | Human merge/review of that unit; not asserted here |

---

## 7. Sequencing (Unit C — gated on this audit's merge)

After this public audit merges:

1. Finish Meeting Follow-Up live-truth normalization (unmerged unit; do not
   assert its fields as main truth until merged).
2. Resolve deployed Apps Script revision/file authority **read-only** (Q1/Q2).
3. Remove the raw identity-token logging in a **separately governed private
   change** (recorded in §4.1; not part of this audit).
4. Design the add-on → public judge auth contract (Q3).
5. Return two implementation packets:
   - **A.** public `demo_stages` projection (additive to the existing judge
     surface), and
   - **B.** private CardService MG Guide adapter (add-on presentation delta).

```text
STOP_BEFORE=code_implementation_or_deployment
```

---

## 8. Compliance confirmations

```text
RUNTIME_MUTATION=0
DEPLOYMENT=0
CLASP_PUSH=0
APPS_SCRIPT_DEPLOY=0
OAUTH_SCOPE_CHANGES=0
IAM_IAP_CHANGES=0
PERMISSION_GRANTS=0
GHL_MCP_CALLS=0
PRODUCTION_CUSTOMER_DATA_TOUCH=0
REPO_MIGRATION=0
NEW_AUTH_PATH_INVENTED_OR_TESTED=0
SECRET_OR_TOKEN_DISCLOSURE=0
PRIVATE_ENDPOINTS_IN_PUBLIC_ARTIFACT=NO
PRIVATE_IDS_IN_PUBLIC_ARTIFACT=NO
PRIVATE_RUNTIME_CONFIG_IN_PUBLIC_ARTIFACT=NO
PRIVATE_AI_ARTIFACT_CONTENT_COPIED=NO
FILES_CHANGED_BY_THIS_UNIT=1 (this artifact only)
```

## 9. Stop

```text
STOP=governance_review_before_implementation
```

This artifact is a planning-only decision summary. No implementation,
cross-repo wiring, add-on edit, deployment, or auth work is authorized.
