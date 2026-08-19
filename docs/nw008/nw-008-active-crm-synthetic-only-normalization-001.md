# NW-008 Active CRM Synthetic-Only Durable-State Normalization 001

```text
ARTIFACT_KIND=DURABLE_STATE_NORMALIZATION
NORMALIZATION_ID=NW008_ACTIVE_CRM_SYNTHETIC_ONLY_NORMALIZATION_001
WORKFLOW=meeting_follow_up_v1
BRANCH=planning/nw008-active-crm-synthetic-only-normalization-001
BASE_SHA=dc48531a5d79d01a57de8fcfa81140a4dd59535c
RECORDED_AT_UTC=2026-08-19
AUTHORITY_SCOPE=DOCUMENTATION_AND_DURABLE_STATE_ONLY
```

This artifact is the **current superseding interpretation** of the GoHighLevel
environment classification for `meeting_follow_up_v1`. It reconciles merged
durable state; it does not authorize GHL MCP execution, HighLevel REST
execution, live CRM mutation, IAM changes, credential changes, deployment, or
customer-data access.

## Sequencing gate record

```text
PR91_STATE=MERGED
PR91_FINAL_HEAD=a4f81d70b49ba70f7b19901da49bb7080bf61881
PR91_MERGE_SHA=dc48531a5d79d01a57de8fcfa81140a4dd59535c
NORMALIZATION_BASE_SHA=dc48531a5d79d01a57de8fcfa81140a4dd59535c
```

PR #91 (`feat(competition): meeting_follow_up_v1 acceptance finalization`) was
preserved as its own acceptance-finalization unit. This normalization lane was
branched from verified `origin/main` **after** the PR #91 merge; it was not
branched from an obsolete pre-#91 main, and PR #91 was not contaminated with
REST adapter architecture or CRM execution work.

---

## 1. Prior-state summary

Current-facing durable state on pre-normalization `main` mixed two
environment classifications:

- **Stale (superseded by this artifact):** foundation-era language requiring an
  *isolated/test GHL location or account* as the precondition for any live
  CRM work — e.g. `environment: hackathon_test_required`,
  `location_id: UNKNOWN_TEST_LOCATION`, "GHL test-account write policy",
  "GoHighLevel Test CRM", "Isolated / test location only", and "future
  safe-environment mutation lane". That language was written when it was
  believed an isolated hackathon test location might be provisioned.
- **Merged truth (binding):** no isolated hackathon test location exists or
  was ever made available; the canonical MG Guide GoHighLevel location is the
  target, and it is **business-active and non-isolated**. A human-approved
  synthetic-only live-location exception governs any live proof.

The stale phrasing misclassified the controlling environment and implied that
safety derives from environmental isolation. It does not: safety derives from
the deterministic controls and the private exact-ID allowlist.

## 2. Controlling merged evidence

### PR #5 — no-sandbox strategy

```text
PR=5
MERGE_SHA=ea44f366f82039d3fa19168af1996a73253e6924
ISOLATED_HACKATHON_TEST_LOCATION_AVAILABLE=NO
CANONICAL_GHL_LOCATION_USED=YES
CANONICAL_LOCATION_CLASSIFIED_AS_TEST_ENVIRONMENT=NO
```

### PR #8 — canonical synthetic read binding

```text
PR=8
MERGE_SHA=93a118ff0cf85e5b9ba0b7fde3ed99be0b1c8a69
SYNTHETIC_CONTACT_BOUND=YES
SYNTHETIC_OPPORTUNITY_BOUND=YES
PRIVATE_ALLOWLIST_COMPLETE=YES
PIT_CANONICAL_LOCATION_VERIFIED=YES
PRIVATE_EXACT_IDS_PUBLICATION=NO
```

The historical read authorization permitted exact allowlisted record access
and denied: `BROAD_SEARCH`, `NON_ALLOWLISTED_IDS`, `CRM_WRITES`, `EMAIL_SMS`,
`REAL_CUSTOMER_READS`, `AUTHORITY_EXPANSION`.

### Live-location exception

```text
DECISION_ID=NW008_AT1_LIVE_LOCATION_EXCEPTION_001
PROOF=proof/nw008/nw-008-at1-live-location-synthetic-only-exception.md

ISOLATED_GHL_TEST_LOCATION=NO
DEDICATED_TEST_LOCATION_AVAILABLE=NO
LIVE_GHL_LOCATION_REQUIRED=YES
LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION_APPROVED=YES

NEW_PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2

SYNTHETIC_CONTACT_ONLY=YES
SYNTHETIC_OPPORTUNITY_ONLY=YES

PRODUCTION_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO
SEARCH_FOR_ALTERNATE_TARGET=NO

AT1_EXECUTION_AUTHORIZED=NO
```

The CRM is business-active and non-isolated. It must not be described as a
test environment, and its underlying business data must not be treated as
disposable.

### Track A readiness (external environment)

```text
ISOLATED_GHL_TEST_LOCATION=NO
LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION=YES
LIVE_LOCATION_BINDING_VERIFIED=YES
PIPELINE_METADATA_VERIFIED=YES

SYNTHETIC_CONTACT_READY=YES
SYNTHETIC_OPPORTUNITY_READY=YES

EXPECTED_INITIAL_STAGE_BOUND=YES
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ

AUTHORIZED_FINAL_STAGE_VERIFIED=YES

AT1_WRITE_OPERATION_SCHEMA_READY=YES
AT1_WRITE_CREDENTIAL_SCOPE_VERIFIED=YES
AT1_WRITE_CREDENTIAL_READY=YES
REQUIRED_GHL_OPERATIONS_VERIFIED=YES

EXTERNAL_ENVIRONMENT_VERIFIED=YES
ENVIRONMENT_READY=YES

AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

**Environment readiness is not mutation authorization.**

## 3. Explicit supersession matrix

| # | OLD (superseded) | CURRENT (controlling) |
| --- | --- | --- |
| S1 | isolated/test GHL required | active canonical business CRM under synthetic-only bounded controls |
| S2 | safe environment provides safety | deterministic controls + exact private allowlist provide safety |
| S3 | environment readiness may be interpreted as write readiness | `ENVIRONMENT_READY != EXECUTION_AUTHORIZED` |
| S4 | generic contact/opportunity search may be part of resolution | current live proof: exact preverified synthetic IDs only; broad/alternate search forbidden |
| S5 | MCP transport selected | generic GHL MCP implementation blocked; REST adapter architecture planning is next; no REST execution authority yet |

This matrix supersedes conflicting environment semantics in current-facing
surfaces. It does **not** rewrite historical proof (§8).

## 4. Canonical normalized environment contract

```text
CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM

ISOLATED_GHL_TEST_LOCATION=NO
DEDICATED_TEST_LOCATION_AVAILABLE=NO

LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION=YES
LIVE_LOCATION_BINDING_VERIFIED=YES

SYNTHETIC_CONTACT_READY=YES
SYNTHETIC_OPPORTUNITY_READY=YES

PRIVATE_ALLOWLIST_REQUIRED=YES
EXACT_ID_TARGETING_REQUIRED=YES
PRIVATE_BINDING_PUBLICATION=NO

BROAD_SEARCH_AUTHORIZED=NO
LIST_PAGINATION_EXPANSION_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO

REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO

NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1

AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO

EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ

LIVE_CRM_MUTATION_AUTHORIZED=NO
REST_ADAPTER_EXECUTION_AUTHORIZED=NO

SEPARATE_HUMAN_MUTATION_AUTHORIZATION_REQUIRED=YES
```

Preferred human-readable phrase:

> business-active canonical CRM under synthetic-only bounded execution controls

"Safe CRM environment" and "test CRM" are **not** the controlling environment
classification. Safety derives from the controls, not from environmental
isolation.

## 5. Private-ID / allowlist rules

- The live location binding (`NW008_GHL_LIVE_LOCATION_PRIVATE_V2`), the
  synthetic contact ID, the synthetic opportunity ID, and the pipeline/stage
  IDs are **private** and must never be published in this public repository.
- Competition live proof is restricted to the privately allowlisted
  preverified synthetic contact and synthetic opportunity only.
- The allowlist is closed: no record outside it may be accessed for any
  competition purpose.

## 6. Exact-ID / no-search rules

```text
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_ALTERNATE_TARGET=YES
EXACT_PRIVATE_IDS_ONLY=YES
```

The bounded AT-1 call-shape concept is preserved:

```text
get-contact
get-opportunity
create-note
get-note
update-opportunity
get-opportunity
```

Invariants:

```text
NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
STOP_ON_TERMINAL_FAILURE=YES
```

This normalization does **not** authorize those write operations.

## 7. Separate human mutation authorization rule

The target CRM is the business-active canonical GoHighLevel environment.
Competition live proof is restricted to privately allowlisted synthetic
records and exact-ID operations. No real customer record may be searched,
read, or mutated. Environment readiness does not authorize mutation. Any note
creation or opportunity-stage update requires a separate human-reviewed
execution authorization bound to the exact transport, credential, location,
synthetic IDs, allowed stage transition, operation budget, and proof
requirements.

No real-customer or non-allowlisted CRM mutation. Competition CRM mutations,
if separately human-authorized, may target only the privately allowlisted
preverified synthetic records in the canonical business-active location using
the exact operation budget.

Preserved mutation envelope:

```text
0-1 NOTE CREATE
0-1 STAGE UPDATE

ONLY:
authorized initial stage
→
authorized final stage

READBACK_REQUIRED=YES
```

Before any future stage write:

```text
FRESH_PREEXECUTION_INITIAL_STAGE_READ_REQUIRED=YES
```

Fail closed on mismatch.

## 8. Historical-artifact preservation policy

Terminology was **not** globally replaced. Historical execution, proof, grant,
result, and reconciliation artifacts preserve what was believed or required at
the time. This artifact — not edited history — is the current superseding
interpretation.

Classification classes used in the audit:

```text
CURRENT_AUTHORITY_STALE     → normalized
CURRENT_FACING_STALE        → normalized
HISTORICAL_VALID            → preserved unchanged
FIXTURE_OR_TEST_HARNESS_VALID → preserved unchanged
UNRELATED_TEST_USAGE        → preserved unchanged
```

Examples of historical evidence intentionally left unchanged:

- `proof/phase2/**` (Phase 2A discovery record, incl. `proof/phase2/closeout-note.md`)
- PR #5 proof and PR #8 proof (`proof/canonical-synthetic-read-binding-v1/**`)
- Older NW-008 grants/results, including Grant/Result 005 and Grant/Result 006
- PR #61 planning evidence
- Provider-contract investigation artifacts (`proof/nw008/nw-008-at1-*provider*`, `docs/nw008/nw-008-at1-highlevel-provider-clarification-*`)
- All other `proof/nw008/**` historical grants/results/plans not listed in §9
- `docs/COMPETITION_BASELINE.md`, `governance/README.md` (historical/baseline phrasing)
- `fixtures/**` (test-harness seed comments) and `tests/**` (harness usage)

## 9. Active files reconciled

| File | Changes |
| --- | --- |
| `README.md` | `meeting_follow_up_v1` scope now states the normalized environment class and links this artifact; current-facing CRM transport language points to HighLevel REST v3 planning and blocks generic GHL MCP implementation; security posture uses the exact non-allowlisted/real-customer mutation wording |
| `docs/MEETING_FOLLOW_UP_FOUNDATION.md` | Header normalization note; §4/§5 scope environment statement; §6 architecture diagram CRM node and transport boundary; §10 bounded synthetic-only mutation authorization; §11 CRM transport contract shifted to HighLevel REST v3 architecture planning with exact-ID operations only; §12 mutation-policy environment clause rewritten to the canonical contract; §15 fixture intent; §16 phase-2 gate; §18 demo beat; §19 data guard; §20 DoD items 1–2; Appendix A row |
| `docs/SECURITY.md` | Non-negotiable mutation wording normalized; allowed-environments GHL row replaced with the canonical-location synthetic-only exact-ID posture; environment-semantics paragraph added before blast-radius section; historical GHL MCP evidence preserved while current transport planning points to HighLevel REST v3 with no implementation/execution authorization |
| `contracts/ghl_tool_manifest.yaml` | Header block now records the current environment class, REST-adapter boundary, and a historical note; `environment_binding_status`, `location_id`, and `location_binding_notes` annotated as HISTORICAL/superseded (Phase 2A discovery record preserved, not rewritten) |
| `proof/nw008/nw-008-readiness-matrix.md` | Front-matter environment-semantics row added; historical "safe-environment"/"isolated" rows below preserved as the historical record |
| `proof/nw008/nw-008-implementation-packet.md` | Environment-semantics supersession note added; historical dependency-sequence phrasing preserved |
| `competition/NEW_WORK_LEDGER.md` | Two current-facing "safe-environment lane" forward references normalized; new normalization entry appended; historical NW-012/Phase-2A closure records preserved |
| `docs/competition/DEVPOST_WRITEUP.md` | "What's next" future-lane bullet normalized to the canonical synthetic-only bounded mutation lane |

## 10. Files intentionally left historical

| File / area | Class | Reason |
| --- | --- | --- |
| `proof/phase2/**` | HISTORICAL_VALID | Phase 2A discovery-time record |
| `proof/nw008/**` (all grants/results/plans other than the two reconciled in §9) | HISTORICAL_VALID | Execution-time beliefs preserved |
| `proof/canonical-synthetic-read-binding-v1/**` | HISTORICAL_VALID | PR #8 binding proof |
| `docs/COMPETITION_BASELINE.md` | HISTORICAL_VALID | Baseline document; "test account only" reflects discovery-time posture |
| `governance/README.md` | HISTORICAL_VALID | Generic governance example phrasing |
| `fixtures/transcript-no-stage-change.txt`, `fixtures/transcript-ambiguous-contact.txt` | FIXTURE_OR_TEST_HARNESS_VALID | Fixture seed comments |
| `tests/**` | FIXTURE_OR_TEST_HARNESS_VALID | Test-harness usage |
| `.env.example` | CURRENT_FACING (already correct) | Already states canonical location is not a test environment; no change needed |
| `docs/architecture/meeting-follow-up-v1-competition-architecture.md` | UNRELATED_TEST_USAGE / already correct | No stale environment claims (only "synthetic CRM fixtures, no live GHL mutation in demo") |
| `docs/demo/meeting-follow-up-v1-4min-demo-script.md` | UNRELATED_TEST_USAGE / already correct | No stale environment claims |
| `proof/competition/meeting-follow-up-v1-acceptance-finalization-001.md` | Already correct | Post-PR-#91 acceptance record; no stale environment semantics |
| `proof/nw007/nw007-decision-card-reviewer-disposition.md`, `proof/nw005/**` | HISTORICAL_VALID | Unrelated historical proof |

## 11. Remaining unknowns

```text
EXPECTED_INITIAL_STAGE_VERIFIED=NO_PENDING_FRESH_PREEXECUTION_READ
```

- The expected initial stage is **bound** but must be re-verified by a fresh
  pre-execution read immediately before any future authorized stage write
  (fail closed on mismatch). No such read is pending or authorized by this
  artifact.
- Exact private IDs (location, contact, opportunity, pipeline, stages) remain
  unpublished by design (`PRIVATE_BINDING_PUBLICATION=NO`).
- REST adapter transport, credential scoping for REST, and REST operation
  contracts are **not** designed here; they are the next architecture gate.

## 12. Next architecture gate

```text
GHL_GENERIC_MCP_IMPLEMENTATION_PATH=BLOCKED
HIGHLEVEL_REST_ADAPTER=PLANNING_NEXT
CRM_TRANSPORT_FUTURE=HIGHLEVEL_REST_V3
REST_ADAPTER_IMPLEMENTATION_AUTHORIZED=NO
REST_ADAPTER_EXECUTION_AUTHORIZED=NO
```

Prepared (not self-authorized, not executed):

```text
NW008_AT1_GHL_REST_ADAPTER_ARCHITECTURE_001
```

The future REST adapter may reuse the verified facts that the live location
binding exists, the synthetic contact binding exists, the synthetic
opportunity binding exists, the private allowlist exists, and the target
pipeline/stage bindings exist. It must **not** automatically inherit MCP
transport authority, MCP execution grants, MCP operation authority, or write
execution authorization. Transport authorization must be reviewed separately.

That next unit must begin from this normalized durable state and preserve:

```text
ACTIVE_CANONICAL_BUSINESS_CRM
SYNTHETIC_ONLY
PRIVATE_ALLOWLIST
EXACT_ID_ONLY
NO_BROAD_SEARCH
NO_REAL_CUSTOMER_ACCESS
SEPARATE_HUMAN_MUTATION_AUTHORIZATION
```

---

## Scan report (targeted semantic scan of current-facing files)

Current-authority/current-facing surfaces were scanned for assertions, as
present truth, of: isolated GHL test location exists; GHL target is a test
account; hackathon test CRM is the live target; broad search permitted during
live proof; non-allowlisted CRM records may be accessed; environment readiness
equals mutation authority.

```text
SCAN_RESULT=PASS
CURRENT_AUTHORITY_STALE_REMAINING=0
CURRENT_FACING_STALE_REMAINING=0
HISTORICAL_VALID_PRESERVED=YES
FIXTURE_OR_TEST_HARNESS_VALID_PRESERVED=YES
```

Remaining matches for legacy phrases after normalization exist only in
classified-historical or fixture/harness files (§10) or as explicitly labeled
HISTORICAL Phase 2A fields inside `contracts/ghl_tool_manifest.yaml`.

## Explicit non-actions

```text
DID_NOT_PERFORM_GHL_READ=YES
DID_NOT_PERFORM_GHL_WRITE=YES
DID_NOT_CREATE_OR_ROTATE_CREDENTIALS=YES
DID_NOT_CHANGE_IAM=YES
DID_NOT_DEPLOY=YES
DID_NOT_IMPLEMENT_REST_ADAPTER=YES
DID_NOT_REWRITE_HISTORICAL_PROOF=YES
DID_NOT_SELF_AUTHORIZE_NEXT_UNIT=YES
```

## STOP

```text
EXTERNAL_EFFECTS=0
GHL_CALLS=0
CRM_WRITES=0
IAM_CHANGES=0
SECRET_CHANGES=0
DEPLOYMENT_CHANGES=0

STOP_CODE=NW008_ACTIVE_CRM_SYNTHETIC_ONLY_NORMALIZATION_001_READY_FOR_HUMAN_REVIEW
```
