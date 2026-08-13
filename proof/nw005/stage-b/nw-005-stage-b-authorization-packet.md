# NW-005 Stage B — Environment Binding & Authorization Packet

**This is a planning / environment-binding artifact only.** No Stage B runtime
code, Firestore client usage, document network call, API enablement, IAM
mutation, secret materialization, or deployment is created or authorized by
this document. Execution requires a **separate explicit human authorization**
after all required environment fields are resolved.

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
PACKET_KIND=STAGE_B_ENVIRONMENT_BINDING_AND_ACTIVATION_REQUEST
STATUS=PROPOSED_NOT_AUTHORIZED
SELF_ACTIVATION=FORBIDDEN
```

## Objective (bounded smoke proof — future execution only)

```text
workflow_run_audit_v1
  → Firestore create-only write
  → exact get
  → content_fingerprint verification (read-back triple equality)
  → exact delete
  → exact get expect NOT_FOUND
  → STOP
```

Stage B's sole purpose is to prove that a Stage A-projected
`workflow_run_audit_v1` document can be durably written to a dedicated
Firestore test project/database, read back exactly, verified against its
`content_fingerprint` under Stage A `nw005_canonical_json_v1` content-body
rules, and cleaned up — nothing more.

## Upstream merge truth (preflight)

```text
PR19_STATE=MERGED
PR19_TITLE=NW-005 Stage B Firestore smoke-proof authorization packet (planning only)
PR19_URL=https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/19
PR19_MERGE_SHA=b1847821adad8fa8231110e2fac3e90ee24fdf68
PR19_MERGED_AT=2026-08-13T01:28:11Z
PR19_HEAD_BRANCH=plan/nw005-stage-b-firestore-proof
LOCAL_BRANCH=plan/nw005-stage-b-environment-binding
LOCAL_BASE=b1847821adad8fa8231110e2fac3e90ee24fdf68
DO_NOT_REUSE_BRANCH=plan/nw005-stage-b-firestore-proof

NW005_STAGE_A=MERGED_COMPLETE
NW005_STAGE_A_PR18_MERGE_SHA=63aadc5c90569cfa119af7cc7e30fbac62f8544b
NW005_STAGE_A_PR18_FINAL_HEAD=695bf3dcae3c9a82ef3af9be9cf264a669485939
NW005_STAGE_A_PR18_MERGED_AT=2026-08-13T01:15:44Z
```

## Required environment bindings (Stage B gate)

| Field | Value | Resolution |
| --- | --- | --- |
| `GCP_TEST_PROJECT_ID` | `mg-devpost` | **BOUND** — dedicated competition/test project `MG DevPost` (`projectNumber=985566250549`, `lifecycleState=ACTIVE`) |
| `PROJECT_CLASSIFICATION` | `DEDICATED_TEST_NON_PRODUCTION` | **BOUND** — not a production CRM/customer project; selected over multi-workload project `ai-rolodex-to-crm` |
| `FIRESTORE_DATABASE_ID` | `devpost-google-contest` | **BOUND** — dedicated Firestore Native database created for the NW-005 test project and ready for explicit human authorization review |
| `FIRESTORE_LOCATION_ID` | `us-east4` | **BOUND** — dedicated Firestore location aligned to the new database |
| `FIRESTORE_API_STATUS` | `ENABLED` | **BOUND** — `firestore.googleapis.com` is enabled on `mg-devpost` and must not be mutated in this packet |
| `FIRESTORE_EDITION` | `STANDARD` | **BOUND** — database edition is standard |
| `FIRESTORE_MODE` | `NATIVE` | **BOUND** — database mode is Firestore Native |
| `ENCRYPTION_MODE` | `GOOGLE_MANAGED` | **BOUND** — encryption is Google-managed |
| `EXECUTION_PRINCIPAL` | `user:themg@themiliare-group.com` | **BOUND** — active gcloud account observed at binding time; Owner on `mg-devpost` |
| `CREDENTIAL_SOURCE` | `USER_APPLICATION_DEFAULT_CREDENTIALS` | **BOUND** — local user ADC (`type=authorized_user`); no SA JSON key; no secret commit |
| `IAM_CHANGE_REQUIRED` | `NO` | **BOUND** — principal already holds `roles/owner` on `mg-devpost`; no IAM mutation required for smoke once API+DB exist. Least-privilege custom role remains **recommended** and still requires separate authority if pursued |
| `SYNTHETIC_RUN_ID_ALLOWLIST_BOUND` | `YES` | **BOUND** — exact IDs only (see Allowlist) |
| `ALLOWLIST_COUNT` | `4` | **BOUND** — terminal Stage A fixture run IDs only |

### Binding block (machine-readable)

```text
GCP_TEST_PROJECT_ID=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION
FIRESTORE_DATABASE_ID=devpost-google-contest
FIRESTORE_LOCATION_ID=us-east4
FIRESTORE_API_STATUS=ENABLED
FIRESTORE_EDITION=STANDARD
FIRESTORE_MODE=NATIVE
ENCRYPTION_MODE=GOOGLE_MANAGED
EXECUTION_PRINCIPAL=user:themg@themiliare-group.com
CREDENTIAL_SOURCE=USER_APPLICATION_DEFAULT_CREDENTIALS
IAM_CHANGE_REQUIRED=NO
SYNTHETIC_RUN_ID_ALLOWLIST_BOUND=YES
ALLOWLIST_COUNT=4
REQUIRED_FIELDS_WITH_UNKNOWN=NONE
ENVIRONMENT_BINDING_COMPLETE=YES
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
```

### Hard gate

```text
REQUIRED_FIELDS_WITH_UNKNOWN=NONE
ENVIRONMENT_BINDING_COMPLETE=YES
STATUS=PROPOSED_NOT_AUTHORIZED
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
```

**Gate result:** `REQUIRED_FIELDS_WITH_UNKNOWN=NONE` and
`ENVIRONMENT_BINDING_COMPLETE=YES`, so the environment is fully bound for
explicit human authorization review. This packet still forbids any Stage B
implementation or execution; `CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED` and
must remain so until a human authorizes execution in a follow-on approval.

### Explicit non-bindings / rejected alternates

| Candidate | Decision | Reason |
| --- | --- | --- |
| `ai-rolodex-to-crm` | **REJECTED** as Stage B target | Multi-workload project; existing Firestore DBs (`ingestion-controller`@`us-east4`, `sm-scheduler`@`nam7`) are not a dedicated NW-005 smoke database; classification ≠ `DEDICATED_TEST_NON_PRODUCTION` for this grant |
| Any production / customer project | **FORBIDDEN** | Hard forbid (implementation packet Decision 8) |
| Unclassified project | **FORBIDDEN** | Fail closed |

### Environment provisioning completed

The following Stage B environment prerequisites are complete and are recorded
as binding evidence for execution-authorization review:

1. `firestore.googleapis.com` is enabled on `mg-devpost`
2. Firestore Native database `devpost-google-contest` has been created
3. Database location is bound to `us-east4`
4. Database edition is `STANDARD`
5. Database mode is `NATIVE`
6. Encryption is `GOOGLE_MANAGED`
7. User Application Default Credentials availability has been verified without
   exposing token material

### Remaining prerequisite

1. Separate explicit human authorization to execute Stage B smoke under
   `MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1`

Optional future hardening:

- A least-privilege execution identity/role may be introduced under separate
  IAM authority. It is not required for this environment-binding PR and must
  not be created here.

## Synthetic run ID allowlist (exact match only)

Execution may address **only** these exact pre-bound synthetic `run_id` values.
No prefix match. No suffix match. No glob/wildcard. No dynamic ID minting.

| # | Exact `run_id` | Source fixture (terminal only) |
| --- | --- | --- |
| 1 | `run_nw006_success_001` | `fixtures/nw005/packets/packet-success.completed.json` |
| 2 | `run_nw006_stage_denied_001` | `fixtures/nw005/packets/packet-stage-change-denied.completed_with_review.json` |
| 3 | `run_nw006_ambiguous_contact_001` | `fixtures/nw005/packets/packet-ambiguous-contact.blocked.json` |
| 4 | `run_nw006_failed_001` | `fixtures/nw005/packets/packet-tool-failure.failed.json` |

```text
ALLOWLIST_MATCH_MODE=EXACT_STRING_EQUALITY_ONLY
ALLOWLIST_PREFIX_WILDCARD=FORBIDDEN
ALLOWLIST_COLLECTION=workflow_runs
NON_TERMINAL_RUN_ID_EXAMPLE=run_nw006_non_terminal_001
NON_TERMINAL_DURABLE_WRITE=FORBIDDEN
```

Application hard allowlist (future writer, not in this PR):

- collection path must equal exactly `workflow_runs`
- document id / `run_id` must be a member of the exact allowlist above
- any other collection or run id → fail closed before network call

## Permitted Firestore call graph (complete and exhaustive — future execution)

1. `create workflow_runs/{allowlisted_synthetic_run_id}` (create-only; fails if document exists)
2. `get workflow_runs/{same_run_id}` (exact document get, no query)
3. Local verification after read-back (schema / `run_id` / fingerprint triple — see below)
4. `delete workflow_runs/{same_run_id}` for `stage_b_smoke` cleanup
5. `get workflow_runs/{same_run_id}` expecting `NOT_FOUND` (delete verification)
6. STOP

## Verification semantics (frozen for future Stage B execution)

### 1. Read-back fingerprint (triple equality)

Recompute from the **read-back document** using the merged Stage A rules:

- Canonicalizer: `nw005_canonical_json_v1` (packet-local; **not** RFC 8785)
- Content body: immutable audit body **before** integrity fields are attached
- Exclusions from content body (Stage A `_content_fingerprint_body` /
  Decision 1c):
  - `recorded_at`
  - entire `integrity` object (includes both fingerprint fields)
  - all persistence-proof fields (those never belong on the Firestore doc)

Require:

```text
RECOMPUTED_READBACK_CONTENT_FINGERPRINT
  == STORED_CONTENT_FINGERPRINT
  == EXPECTED_PROJECTED_CONTENT_FINGERPRINT
```

Where:

| Symbol | Meaning |
| --- | --- |
| `EXPECTED_PROJECTED_CONTENT_FINGERPRINT` | `integrity.content_fingerprint` from the local Stage A projection **before** write |
| `STORED_CONTENT_FINGERPRINT` | `integrity.content_fingerprint` field value on the read-back document |
| `RECOMPUTED_READBACK_CONTENT_FINGERPRINT` | `fingerprint_hex(_content_fingerprint_body(readback_doc))` using Stage A rules |

Any inequality → `CONTENT_FINGERPRINT_MATCH=NO` → fail closed; still attempt
`stage_b_smoke` cleanup.

### 2. Delete verification (preferred flow)

```text
delete exact document workflow_runs/{run_id}
  → exact get same document
  → expected NOT_FOUND
  → DELETE_VERIFIED=YES
```

If delete fails: `CLEANUP_STATUS=FAILED` / `DELETE_VERIFIED=NO`; do **not**
perform unrestricted collection sweeps; human follow-up only.

### 3. Allowlist enforcement

```text
addressable_targets = exact pre-bound synthetic run IDs only
prefix_only_wildcard_behavior = FORBIDDEN
collection_wildcard / list / query = FORBIDDEN
```

### 4. Stage B external-effect counters (execution-time; not planning-time zeros)

Once authorized execution starts, do **not** require `EXTERNAL_EFFECTS=0`.
Record actual counters:

```text
STAGE_B_DOCUMENT_CREATES=<n>
STAGE_B_DOCUMENT_READS=<n>
STAGE_B_DOCUMENT_DELETES=<n>
STAGE_B_NETWORK_CALLS=<n>
STAGE_B_AUTHORIZED_MUTATING_EXTERNAL_EFFECTS=<n>  # creates + deletes under grant
```

Planning-time / this-packet counters remain zero (see Current truth).

Persistence evidence is emitted only as `nw005_persistence_proof_v1` in
proof-return — **never** as a second update to the Firestore document
(Decision 1b).

## Operation caps (preserved)

```text
MAX_DOCUMENT_CREATES=10
MAX_DOCUMENT_READS=20
MAX_DOCUMENT_DELETES=10
MAX_EXECUTION_MINUTES=10
DATA=synthetic_only
MAX_DISTINCT_RUN_IDS=4
COLLECTION_FANOUT=1
COLLECTION_NAME=workflow_runs
```

If any ceiling would be exceeded: **STOP**, do not continue writes.

## Retention modes

| Mode | Status | Behavior |
| --- | --- | --- |
| `stage_b_smoke` | In scope **only after** separate human execution authorization | `create → get → verify → delete → get NOT_FOUND`; no residual documents |
| `acceptance_demo` | `NOT_AUTHORIZED` | Deferred to NW-008; requires a temporary retention window before cleanup |

## Required Stage B proof fields (to be collected at execution, not now)

```text
FIRESTORE_CREATE_ATTEMPTED=
FIRESTORE_CREATE_VERIFIED=
FIRESTORE_READBACK_VERIFIED=
RUN_ID_MATCH=
CONTENT_FINGERPRINT_MATCH=
RECOMPUTED_READBACK_CONTENT_FINGERPRINT=
STORED_CONTENT_FINGERPRINT=
EXPECTED_PROJECTED_CONTENT_FINGERPRINT=
SCHEMA_VALID_AFTER_READBACK=
DELETE_ATTEMPTED=
DELETE_VERIFIED=
DELETE_GET_NOT_FOUND=
STAGE_B_DOCUMENT_CREATES=
STAGE_B_DOCUMENT_READS=
STAGE_B_DOCUMENT_DELETES=
STAGE_B_NETWORK_CALLS=
STAGE_B_AUTHORIZED_MUTATING_EXTERNAL_EFFECTS=
REAL_CUSTOMER_DATA=
GHL_LIVE_CALLS=
TEST_PROJECT_ID=
DATABASE_ID=
LOCATION_ID=
PRINCIPAL=
STARTED_AT=
COMPLETED_AT=
CLEANUP_STATUS=
RETENTION_MODE=stage_b_smoke
```

All fields are blank at binding time; they may only be filled by actual
authorized Stage B execution evidence.

## Acceptance-test boundary

**AT-10 must NOT be claimed complete from `stage_b_smoke`.** The smoke proof
demonstrates write/readback/cleanup mechanics only. Honest AT-10 completion
is deferred to NW-008 with the `acceptance_demo` retention mode, which is
separately NOT_AUTHORIZED here.

## Explicitly prohibited (this packet and default Stage B scope)

- Runtime code in this binding PR
- Firestore document network calls (create/get/list/query/delete) in this PR
- API enablement mutation in this PR
- IAM mutation in this PR
- Secret creation or key commits
- Cloud Run deployment
- GHL / CRM calls
- Policy reevaluation
- Agent rerun
- Production / customer data
- `acceptance_demo` retention
- AT-10 completion claim
- `set` / overwrite semantics
- `update` (any partial or full update)
- collection `list` / any `query`
- wildcard document access / prefix allowlist behavior
- Self-activation of Stage B by an agent

## Credential verification (planning-only; no tokens disclosed)

```bash
gcloud config get-value project
gcloud auth list --filter=status:ACTIVE
gcloud auth application-default print-access-token >/dev/null
```

The credential check confirms the active project and active user account are
available for ADC-based authorization review without printing any token value,
without creating service-account JSON keys, and without writing Firestore data.

## Human authorization request (not granted by this packet)

The environment is now fully bound and ready for explicit human execution
authorization review. A human maintainer may grant execution under:

```text
AUTHORIZATION_ID=MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
REQUESTED_DECISION=AUTHORIZED_FOR_EXECUTION
REQUESTED_MODE=stage_b_smoke
REQUESTED_PROJECT=mg-devpost
REQUESTED_DATABASE=devpost-google-contest
REQUESTED_LOCATION=us-east4
REQUESTED_COLLECTION=workflow_runs
REQUESTED_ALLOWLIST_COUNT=4
```

**Do not self-activate Stage B.** Agent/orchestrator STOP is mandatory until a
human records an explicit approval signature in a follow-on activation
decision artifact.

### Current authorization posture

```text
HUMAN_SIGNATURE=PENDING_EXPLICIT_APPROVAL
CURRENT_GRANT_STATE=PROPOSED_NOT_AUTHORIZED
BLOCKERS=HUMAN_EXECUTION_APPROVAL_REQUIRED
ENVIRONMENT_BINDING_COMPLETE=YES
```

## Current truth (this binding packet)

```text
NW005_STAGE_A=MERGED_COMPLETE
NW005_STAGE_A_PR18_MERGE_SHA=63aadc5c90569cfa119af7cc7e30fbac62f8544b
NW005_STAGE_B=ENVIRONMENT_BINDING_PROPOSED_NOT_AUTHORIZED
NW005_STAGE_B_RUNTIME_CODE=0
FIRESTORE_NETWORK_OPERATIONS=0
FIRESTORE_DOCUMENT_CREATES=0
FIRESTORE_DOCUMENT_READS=0
FIRESTORE_DOCUMENT_DELETES=0
FIRESTORE_API_ENABLEMENT_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
CLOUD_RUN_DEPLOYMENTS=0
GHL_LIVE_CALLS=0
REAL_CUSTOMER_DATA=0
EXTERNAL_EFFECTS=0
AT10_CLAIMED=NO
ACCEPTANCE_DEMO=NOT_AUTHORIZED
```

```text
STOP_CODE=NW005_STAGE_B_ENVIRONMENT_BOUND_READY_FOR_AUTHORIZATION_REVIEW
```
