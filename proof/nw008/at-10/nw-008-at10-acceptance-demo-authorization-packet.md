# NW-008 AT-10 — Acceptance-Demo Authorization Packet

**This is a planning / authorization-request artifact only.** No AT-10
runtime code, Firestore client usage, document network call, API enablement,
IAM mutation, secret materialization, deployment, workflow execution, agent
rerun, policy reevaluation, or test mutation is created or authorized by this
document.

Execution, implementation, and any AT-10 completion claim each require
**separate explicit human authorization** after this packet is reviewed and
approved.

```text
AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1
PACKET_KIND=AT10_ACCEPTANCE_DEMO_AUTHORIZATION_REQUEST
STATUS=PROPOSED_NOT_AUTHORIZED
SELF_ACTIVATION=FORBIDDEN
REQUESTED_MODE=acceptance_demo
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
HUMAN_SIGNATURE=PENDING_EXPLICIT_APPROVAL

AT10_IMPLEMENTATION_AUTHORIZED=NO
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
ACCEPTANCE_DEMO_AUTHORIZED=NO
```

## Decision boundary (do not reopen Stage B smoke)

This lane is **not** NW-005 Stage B smoke reauthorization.

Existing Stage B authority is already proven and is reused by reference only:

```text
NW005_STAGE_B_ENVIRONMENT_BINDING=COMPLETE
NW005_STAGE_B_AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
NW005_STAGE_B_HUMAN_AUTHORIZATION=APPROVED
NW005_STAGE_B_AUTHORIZATION_MERGE_SHA=1d9ff931dd431ce04f47ad907b08252b433d23c9
NW005_STAGE_B_SMOKE_RESULT=PASS
NW005_STAGE_B_PROOF=proof/nw005/stage-b/nw005-persistence-proof-v1.md

INHERITED_STAGE_B_AUTHORIZATION=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
INHERITED_STAGE_B_PROOF=PASS
STAGE_B_PROOF_REUSED=YES
ENVIRONMENT_REUSED=YES
```

The Stage B grant explicitly retained:

```text
ACCEPTANCE_DEMO_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
```

Therefore the next governed lane is:

```text
NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
```

Not:

```text
NW005_STAGE_B_SMOKE_REAUTHORIZATION
```

## Objective (future execution only — not authorized by this packet)

Prove AT-10 audit completeness under temporary `acceptance_demo` retention on
the already-bound dedicated non-production Firestore environment, using only
four exact synthetic allowlisted run IDs, then mandatorily clean up.

Historical AT-10 criterion (foundation §17 — preserve verbatim; do not weaken
or reinterpret):

> Every run (success, blocked, failed) produces a `workflow_runs/{run_id}`
> record with agents, tool counts, reason codes, disposition.

## Upstream merge truth (preflight)

```text
PR50_CONFIRMED_MERGED=YES
PR50_TITLE=NW-008: D2/AT-8 governance closeout (durable D2) — closeout commit 91111ed7337700cfcddb93ebcdf2901ceeed15bd
PR50_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/50
PR50_MERGE_SHA=8f7fdd482c03dfee5e75159054d9ddf11dd793fe
PR50_MERGED_AT=2026-08-15T12:28:44Z
PR50_CLOSEOUT_SUBJECT_SHA=91111ed7337700cfcddb93ebcdf2901ceeed15bd
PR50_SUBJECT_IS_ANCESTOR_OF_ORIGIN_MAIN=YES
CURRENT_MAIN=8f7fdd482c03dfee5e75159054d9ddf11dd793fe
LOCAL_BRANCH=plan/nw008-at10-acceptance-demo-authorization
LOCAL_BASE=8f7fdd482c03dfee5e75159054d9ddf11dd793fe

NW005_STAGE_A=MERGED_COMPLETE
NW005_STAGE_B_SMOKE=PASS
NW008_D2_AT8_GOVERNANCE_CLOSEOUT=MERGED_COMPLETE
```

Post-D2 reconciliation note (factual, non-mutating here):

```text
POST_D2_RECON_PR=51
POST_D2_RECON_PR_STATE=OPEN
POST_D2_RECON_COMMIT=538d76d3c11e93b0833fc280dd839ce2996fb604
POST_D2_RECON_PATH=proof/nw008/nw-008-post-tranche-d-gap-reconciliation.md
POST_D2_RECON_AT10_STATUS_RECORDED=DEFERRED
POST_D2_RECON_RECOMMENDED_LANE_RECORDED=NW005_STAGE_B_AUTHORIZATION_READINESS
POST_D2_RECON_RECOMMENDED_LANE_SUPERSEDED_BY=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION
```

The open post-D2 reconciliation artifact still records Stage B as the primary
blocker. That recommendation is **factually superseded** by the already-proven
Stage B PASS and by this AT-10 acceptance-demo authorization request. This
packet does not mutate the open reconciliation PR; any residual status sync of
that artifact is a separate documentation lane.

## Bound environment (reused; no new provisioning)

| Field | Value | Resolution |
| --- | --- | --- |
| `PROJECT` | `mg-devpost` | **REUSED** — dedicated competition/test project |
| `PROJECT_CLASSIFICATION` | `DEDICATED_TEST_NON_PRODUCTION` | **REUSED** — not production / not customer CRM |
| `DATABASE` | `devpost-google-contest` | **REUSED** — Stage B bound Firestore Native DB |
| `LOCATION` | `us-east4` | **REUSED** — Stage B bound location |
| `COLLECTION` | `workflow_runs` | **REUSED** — exact collection only |
| `DATA` | `synthetic_only` | **REQUIRED** — fixtures only |
| `NEW_API_ENABLEMENT_REQUIRED` | `NO` | Firestore API already enabled under Stage B binding |
| `IAM_MUTATION_AUTHORIZED` | `NO` | No IAM change in this lane |
| `SECRET_MUTATION_AUTHORIZED` | `NO` | No secret change in this lane |
| `CLOUD_RUN_AUTHORIZED` | `NO` | No Cloud Run in this lane |
| `GHL_CRM_AUTHORIZED` | `NO` | No GHL/CRM in this lane |

### Binding block (machine-readable)

```text
PROJECT=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
DATABASE=devpost-google-contest
LOCATION=us-east4
COLLECTION=workflow_runs
DATA=synthetic_only

NEW_API_ENABLEMENT_REQUIRED=NO
IAM_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
CLOUD_RUN_AUTHORIZED=NO
GHL_CRM_AUTHORIZED=NO

ENVIRONMENT_REUSED=YES
ENVIRONMENT_BINDING_COMPLETE=YES
REQUIRED_FIELDS_WITH_UNKNOWN=NONE
```

## Exact run allowlist

Execution may address **only** these exact pre-bound synthetic `run_id` values.
No prefix match. No suffix match. No glob/wildcard. No dynamic ID minting.

| # | Exact `run_id` | Target disposition | Source fixture (terminal only) |
| --- | --- | --- | --- |
| 1 | `run_nw006_success_001` | `completed` | `fixtures/nw005/packets/packet-success.completed.json` |
| 2 | `run_nw006_stage_denied_001` | `completed_with_review` | `fixtures/nw005/packets/packet-stage-change-denied.completed_with_review.json` |
| 3 | `run_nw006_ambiguous_contact_001` | `blocked` | `fixtures/nw005/packets/packet-ambiguous-contact.blocked.json` |
| 4 | `run_nw006_failed_001` | `failed` | `fixtures/nw005/packets/packet-tool-failure.failed.json` |

```text
ALLOWLIST_COUNT=4
ALLOWLIST_MATCH_MODE=EXACT_STRING_EQUALITY_ONLY
ALLOWLIST_PREFIX_WILDCARD=FORBIDDEN
ALLOWLIST_COLLECTION=workflow_runs
REQUESTED_RUN_COUNT=4
MAX_DISTINCT_RUN_IDS=4
NON_TERMINAL_RUN_ID_EXAMPLE=run_nw006_non_terminal_001
NON_TERMINAL_DURABLE_WRITE=FORBIDDEN
SYNTHETIC_ONLY=YES
```

Target dispositions cover the AT-10 surface of success, blocked, and failed
(plus the existing Stage A terminal `completed_with_review` fixture already on
the NW-005 allowlist). Non-terminal packets remain forbidden for durable write.

## AT-10 historical criterion (verbatim)

Authoritative foundation source:
[`docs/MEETING_FOLLOW_UP_FOUNDATION.md`](../../../docs/MEETING_FOLLOW_UP_FOUNDATION.md) §17.

```text
AT10_ID=AT-10
AT10_TITLE=Audit completeness
AT10_CRITERION_VERBATIM=Every run (success, blocked, failed) produces a workflow_runs/{run_id} record with agents, tool counts, reason codes, disposition
AT10_CRITERION_WEAKENING=FORBIDDEN
AT10_CRITERION_REINTERPRETATION=FORBIDDEN
```

Readiness matrix mirror (current historical status on main baseline):

```text
AT10_READINESS_STATUS=DEFERRED
AT10_READINESS_SOURCE=proof/nw008/nw-008-readiness-matrix.md
```

This packet requests authorization to pursue AT-10 under `acceptance_demo`.
It does **not** itself change readiness status or claim AT-10 complete.

## Per-document required proof (each allowlisted run)

For every exact allowlisted `run_id`, future authorized execution must collect:

```text
RUN_ID_MATCH=YES
SCHEMA_VALID_AFTER_READBACK=YES
AGENTS_PRESENT=YES
TOOL_COUNTS_PRESENT=YES
REASON_CODES_PRESENT=YES
DISPOSITION_PRESENT=YES

EXPECTED_PROJECTED_CONTENT_FINGERPRINT=<hex>
STORED_CONTENT_FINGERPRINT=<hex>
RECOMPUTED_READBACK_CONTENT_FINGERPRINT=<hex>
CONTENT_FINGERPRINT_MATCH=YES
```

### Fingerprint triple equality (frozen from Stage A / Stage B)

Recompute from the **read-back document** using merged Stage A rules:

- Canonicalizer: `nw005_canonical_json_v1` (packet-local; **not** RFC 8785)
- Content body: immutable audit body **before** integrity fields are attached
- Exclusions from content body (Stage A `_content_fingerprint_body`):
  - `recorded_at`
  - entire `integrity` object
  - all persistence-proof fields (never on the Firestore doc)

Require:

```text
RECOMPUTED_READBACK_CONTENT_FINGERPRINT
  == STORED_CONTENT_FINGERPRINT
  == EXPECTED_PROJECTED_CONTENT_FINGERPRINT
```

Any inequality → `CONTENT_FINGERPRINT_MATCH=NO` → fail closed; still attempt
`acceptance_demo` cleanup for any documents created in the run.

### Field-presence semantics (do not weaken AT-10)

| Required presence | Source expectation |
| --- | --- |
| `AGENTS_PRESENT` | Durable audit document carries agent identity data projected from packet audit (`agents` / `agent_steps.agents_used` per Stage A schema) |
| `TOOL_COUNTS_PRESENT` | Durable audit document carries tool-count fields projected by Stage A (`tool_call_counts` / equivalent projected counts). Presence is required; do not silently drop the AT-10 tool-count clause |
| `REASON_CODES_PRESENT` | Durable audit document carries reason codes (`reason_codes` / `policy.reason_codes`) |
| `DISPOSITION_PRESENT` | Durable audit document carries disposition (`final_disposition` / terminal disposition aligned to target table) |

Empty lists are permitted only when the source packet legitimately has empty
agents/tools/reason_codes; the **fields themselves** must still be present on
the durable record.

## Authorized call graph request (future execution only)

For each exact allowlisted run ID, in sequence or as an explicitly bounded
four-run batch that never exceeds caps:

```text
create workflow_runs/{run_id}
  → exact get same document
  → validate schema
  → validate run_id
  → validate agents / tool_counts / reason_codes / disposition
  → recompute fingerprint
  → require triple equality
```

After all four documents are individually verified:

```text
validate aggregate AT-10 completeness across the four durable records
  → emit durable local proof artifact(s) under proof/nw008/at-10/
  → exact delete each document
  → exact get each expecting NOT_FOUND
  → STOP
```

```text
CREATE_SEMANTICS=create_only_fail_if_exists
GET_SEMANTICS=exact_document_get_only
DELETE_SEMANTICS=exact_document_delete_only
SET_OVERWRITE=FORBIDDEN
UPDATE=FORBIDDEN
LIST=FORBIDDEN
QUERY=FORBIDDEN
BATCH=FORBIDDEN
TRANSACTION=FORBIDDEN
WILDCARD=FORBIDDEN
```

## Retention

```text
REQUESTED_RETENTION_MODE=acceptance_demo
REQUESTED_RETENTION_CLASS=TEMPORARY_BOUNDED
CLEANUP_REQUIRED=YES
DELETE_VERIFICATION_REQUIRED=YES
```

All four documents may coexist only long enough to:

1. verify individual records;
2. verify aggregate AT-10 completeness;
3. capture durable local proof.

Then exact cleanup is **mandatory**. Residual documents after a failed cleanup
require human follow-up only — no collection sweep, list, or query.

| Mode | Status in this packet | Behavior if later authorized |
| --- | --- | --- |
| `stage_b_smoke` | Already proven PASS under separate grant; **not** reopened here | Single-run create/get/verify/delete (historical) |
| `acceptance_demo` | `PROPOSED_NOT_AUTHORIZED` | Four-run create/get/verify → aggregate proof → delete/get NOT_FOUND |

## Operation caps (exact planned four-run lifecycle only)

Planned network lifecycle (no unrelated margin):

| Phase | Creates | Reads | Deletes | Network calls |
| --- | --- | --- | --- | --- |
| Per-run write + readback × 4 | 4 | 4 | 0 | 8 |
| Aggregate local validation + local proof emit | 0 | 0 | 0 | 0 |
| Cleanup delete + NOT_FOUND get × 4 | 0 | 4 | 4 | 8 |
| **Total planned** | **4** | **8** | **4** | **16** |

```text
MAX_DISTINCT_RUN_IDS=4
MAX_DOCUMENT_CREATES=4
MAX_DOCUMENT_READS=8
MAX_DOCUMENT_DELETES=4
MAX_NETWORK_CALLS=16
MAX_EXECUTION_MINUTES=10
COLLECTION_FANOUT=1
COLLECTION_NAME=workflow_runs
DATA=synthetic_only
```

If any ceiling would be exceeded: **STOP**, do not continue writes, attempt
bounded cleanup only within remaining delete/read budget, then human follow-up.

No arbitrary margin for retries, unrelated operations, non-allowlisted IDs, or
exploratory reads.

## Aggregate AT-10 completeness gate (future execution)

Before cleanup, local validation must affirm:

```text
ALLOWLISTED_RUNS_PRESENT_COUNT=4
DISPOSITION_SET_COVERS_SUCCESS=YES
DISPOSITION_SET_COVERS_BLOCKED=YES
DISPOSITION_SET_COVERS_FAILED=YES
ALL_FOUR_SCHEMA_VALID=YES
ALL_FOUR_FINGERPRINT_TRIPLE_EQUAL=YES
ALL_FOUR_AGENTS_PRESENT=YES
ALL_FOUR_TOOL_COUNTS_PRESENT=YES
ALL_FOUR_REASON_CODES_PRESENT=YES
ALL_FOUR_DISPOSITION_PRESENT=YES
AT10_AGGREGATE_RECORD_PRESENCE=YES
```

Only after the above and durable local proof capture may cleanup proceed.

**Important:** AT-10 completion must **not** be claimed from Stage B smoke, and
must **not** be claimed from this planning packet. A future completion claim
requires separate `AT10_COMPLETION_CLAIM_AUTHORIZED=YES` after successful
authorized execution evidence is reviewed.

## Explicitly prohibited

This packet and any future execution under a grant derived from it forbid:

- `set` / overwrite semantics
- `update` (partial or full)
- `list`
- `query`
- `wildcard` / prefix / suffix allowlist matching
- `batch` writes
- `transaction` multi-doc commits outside the exact single-doc graph
- non-allowlisted run IDs
- non-terminal durable writes
- real customer data
- GHL / CRM calls
- agent rerun
- policy reevaluation
- IAM mutation
- secret mutation
- Cloud Run
- production deployment
- new API enablement
- self-activation by an agent/orchestrator
- AT-10 completion claim from this packet alone
- reopening or re-executing Stage B smoke as a substitute for AT-10

## Authority boundary

```text
THIS_PACKET_AUTHORIZES_EXECUTION=NO
THIS_PACKET_AUTHORIZES_IMPLEMENTATION=NO
THIS_PACKET_AUTHORIZES_COMPLETION_CLAIM=NO
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
HUMAN_SIGNATURE=PENDING_EXPLICIT_APPROVAL
SELF_ACTIVATION=FORBIDDEN

AT10_IMPLEMENTATION_AUTHORIZED=NO
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
ACCEPTANCE_DEMO_AUTHORIZED=NO
```

Human approval, if granted later, must be recorded in a **separate** execution-
authorization decision artifact (mirroring the Stage B pattern of
`nw-005-stage-b-execution-authorization.md`). Approval text in chat is not a
repository grant until that decision artifact exists and is merged under
governance.

## Human authorization request (not granted by this packet)

A human maintainer may later grant execution under:

```text
AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1
REQUESTED_DECISION=AUTHORIZED_FOR_EXECUTION
REQUESTED_MODE=acceptance_demo
REQUESTED_PROJECT=mg-devpost
REQUESTED_DATABASE=devpost-google-contest
REQUESTED_LOCATION=us-east4
REQUESTED_COLLECTION=workflow_runs
REQUESTED_ALLOWLIST_COUNT=4
REQUESTED_RUN_COUNT=4
REQUESTED_RETENTION_MODE=acceptance_demo
REQUESTED_MAX_DOCUMENT_CREATES=4
REQUESTED_MAX_DOCUMENT_READS=8
REQUESTED_MAX_DOCUMENT_DELETES=4
REQUESTED_MAX_NETWORK_CALLS=16
REQUESTED_MAX_EXECUTION_MINUTES=10
REQUESTED_MAX_DISTINCT_RUN_IDS=4
```

**Do not self-activate AT-10.** Agent/orchestrator STOP is mandatory until a
human records an explicit approval signature in a follow-on activation
decision artifact.

### Current authorization posture

```text
HUMAN_SIGNATURE=PENDING_EXPLICIT_APPROVAL
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
BLOCKERS=HUMAN_EXECUTION_APPROVAL_REQUIRED
ENVIRONMENT_BINDING_COMPLETE=YES
ENVIRONMENT_REUSED=YES
STAGE_B_PROOF_REUSED=YES
```

## Required future proof fields (blank until authorized execution)

```text
FIRESTORE_CREATE_ATTEMPTED=
FIRESTORE_CREATE_VERIFIED=
FIRESTORE_READBACK_VERIFIED=
RUN_ID_MATCH=
SCHEMA_VALID_AFTER_READBACK=
AGENTS_PRESENT=
TOOL_COUNTS_PRESENT=
REASON_CODES_PRESENT=
DISPOSITION_PRESENT=
CONTENT_FINGERPRINT_MATCH=
RECOMPUTED_READBACK_CONTENT_FINGERPRINT=
STORED_CONTENT_FINGERPRINT=
EXPECTED_PROJECTED_CONTENT_FINGERPRINT=
AT10_AGGREGATE_RECORD_PRESENCE=
DELETE_ATTEMPTED=
DELETE_VERIFIED=
DELETE_GET_NOT_FOUND=
AT10_DOCUMENT_CREATES=
AT10_DOCUMENT_READS=
AT10_DOCUMENT_DELETES=
AT10_NETWORK_CALLS=
REAL_CUSTOMER_DATA=
GHL_LIVE_CALLS=
TEST_PROJECT_ID=
DATABASE_ID=
LOCATION_ID=
PRINCIPAL=
STARTED_AT=
COMPLETED_AT=
CLEANUP_STATUS=
RETENTION_MODE=acceptance_demo
AT10_COMPLETE=
```

All fields are blank at planning time; they may only be filled by actual
authorized AT-10 acceptance-demo execution evidence.

## Scope of this planning mutation

```text
ALLOWED_PATH=proof/nw008/at-10/nw-008-at10-acceptance-demo-authorization-packet.md
RUNTIME_MUTATION=NO
TEST_MUTATION=NO
CONTRACT_MUTATION=NO
WORKFLOW_MUTATION=NO
INFRA_MUTATION=NO
FIRESTORE_DATA_MUTATION=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
DEPLOYMENT_MUTATION=NO
```

## Current truth (this planning packet)

```text
PR50_CONFIRMED_MERGED=YES
CURRENT_MAIN=8f7fdd482c03dfee5e75159054d9ddf11dd793fe

AUTHORIZATION_ID=MG_GUIDE_NW008_AT10_FIRESTORE_AUDIT_ACCEPTANCE_DEMO_V1
STATUS=PROPOSED_NOT_AUTHORIZED
REQUESTED_MODE=acceptance_demo

ENVIRONMENT_REUSED=YES
STAGE_B_PROOF_REUSED=YES
INHERITED_STAGE_B_AUTHORIZATION=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
INHERITED_STAGE_B_PROOF=PASS

REQUESTED_RUN_COUNT=4
SYNTHETIC_ONLY=YES
MAX_DISTINCT_RUN_IDS=4
MAX_DOCUMENT_CREATES=4
MAX_DOCUMENT_READS=8
MAX_DOCUMENT_DELETES=4
MAX_NETWORK_CALLS=16
MAX_EXECUTION_MINUTES=10

NEW_IAM_REQUIRED=NO
NEW_SECRET_REQUIRED=NO
NEW_API_ENABLEMENT_REQUIRED=NO

FIRESTORE_NETWORK_OPERATIONS=0
FIRESTORE_DOCUMENT_CREATES=0
FIRESTORE_DOCUMENT_READS=0
FIRESTORE_DOCUMENT_DELETES=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
CLOUD_RUN_DEPLOYMENTS=0
GHL_LIVE_CALLS=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS=0

AT10_IMPLEMENTATION_AUTHORIZED=NO
AT10_EXECUTION_AUTHORIZED=NO
AT10_COMPLETION_CLAIM_AUTHORIZED=NO
ACCEPTANCE_DEMO_AUTHORIZED=NO
HUMAN_SIGNATURE=PENDING_EXPLICIT_APPROVAL
```

```text
STOP_CODE=NW008_AT10_ACCEPTANCE_DEMO_AUTHORIZATION_PACKET_READY_FOR_HUMAN_REVIEW
```
