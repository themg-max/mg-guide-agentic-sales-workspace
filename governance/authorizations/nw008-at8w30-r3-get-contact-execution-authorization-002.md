# R3 GET-Contact Execution Authorization

**Authorization ID:** `nw008-at8w30-r3-get-contact-execution-authorization-002`

**Date Issued (original draft, local time):** 2026-08-26T13:29:59-04:00 (UTC equivalent: 2026-08-26T17:29:59Z)

**Authorization Reissued At (UTC):** 2026-08-26T17:50:12Z

**Authority Status:** REISSUED — `PROPOSED_NOT_EFFECTIVE` (activation pending human merge to main; see Section 1.1 and Section 5)

---

## 1. Reconciliation Binding

### PR217 Merge Verification

| Field | Value |
|-------|-------|
| PR Number | 217 |
| PR State | MERGED |
| Reviewed Head OID | `67fda247c3319058bffb0d74112ca6961802962a` |
| Merge Commit OID | `987b9b6646a3090666bd328c6c13eea89556a679` |
| Merged At | 2026-08-26T17:27:19Z |
| Head in Main Lineage | YES |
| Merge Commit in Main Lineage | YES |

### Implementation Lane Status

| Status | Value |
|--------|-------|
| `PR217_TERMINALLY_RECONCILED` | YES |
| `PR217_REPAIR_LANE_REOPEN_REQUIRED` | NO |
| `R3_EXECUTION_AUTHORIZED` | NO |
| `R3_EXECUTION_PERFORMED` | NO |
| `R4_AUTHORIZED` | NO |

### Merged Artifacts Verification

The following artifacts from PR217 are present on `origin/main`:

- ✓ `src/integrations/ghl/highlevel_rest/note_path.py`
- ✓ `src/integrations/ghl/highlevel_rest/live_note_runtime.py`
- ✓ `tests/integrations/ghl/highlevel_rest/test_private_at8_capability_handoff.py`
- ✓ `tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py`
- ✓ `proof/nw008/at-8w30/nw008-at8w30-r3-private-binding-provenance-trust-repair-proof-001.md`
- ✓ `proof/nw008/at-8w30/nw008-at8w30-r3-private-owner-lease-ingress-repair-consumption-001.md`

---

## 1.1 Temporal Provenance & Reissue Record

The original top-level `Date Issued` line used a local wall-clock time with a
misleading `Z` (UTC) suffix. This section corrects that treatment and
reconciles it against the true PR217 merge time and the true reissue time,
without deleting the original historical timing evidence.

| Field | Value |
|-------|-------|
| `ORIGINAL_DRAFT_LOCAL_TIME` | `2026-08-26T13:29:59-04:00` |
| `ORIGINAL_DRAFT_UTC_EQUIVALENT` | `2026-08-26T17:29:59Z` |
| `EXECUTION_BUDGET_ADDENDUM_LOCAL_TIME` | `2026-08-26T13:39:08-04:00` |
| `EXECUTION_BUDGET_ADDENDUM_UTC_EQUIVALENT` | `2026-08-26T17:39:08Z` |
| `PR217_MERGED_AT` | `2026-08-26T17:27:19Z` |
| `AUTHORIZATION_REISSUED_AT` | `2026-08-26T17:50:12Z` |
| `AUTHORIZATION_REISSUED_AFTER_PR217_MERGE` | `YES` |

---

## 2. Authorization Scope

### Operation Definition

| Parameter | Value |
|-----------|-------|
| **OPERATION_ID** | `get-contact` |
| **METHOD** | GET |
| **PATH** | `/contacts/{private_binding.contact_id}` |

### Data Consumption

This authorization permits consumption of **ONLY** the following response fields:

- `contact.id`
- `contact.locationId`

**CONSTRAINT:** Full response logging or persistence is **FORBIDDEN**.

---

## 3. Private Binding Authority

### Authorization Bindings

| Binding | Status | Value |
|---------|--------|-------|
| `BOUND_PR217_REVIEWED_HEAD` | REQUIRED | `67fda247c3319058bffb0d74112ca6961802962a` |
| `BOUND_PR217_MERGE_COMMIT` | REQUIRED | `987b9b6646a3090666bd328c6c13eea89556a679` |
| `PRIVATE_OWNER_LEASE_INGRESS_REPAIR_MERGED` | YES | From PR217 |

### Authority Constraints

| Constraint | Status | Justification |
|-----------|--------|---------------|
| `APPROVED_PRIVATE_REFERENCE_REQUIRED` | YES | Binding requires private reference validation |
| `PUBLIC_RAW_ID_AUTHORITY_MINTING` | FORBIDDEN | Raw ID materialization prohibited |
| `PUBLIC_PRODUCTION_LEASE_MATERIALIZATION` | FORBIDDEN | Lease materialization prohibited |

---

## 4. Network Budget

**Single-Shot Execution Limits:**

| Resource | Budget | Constraint |
|----------|--------|-----------|
| **HIGHLEVEL_TOTAL_CALLS_MAX** | 1 | Hard limit: one API call only |
| **HTTP_REQUEST_DISPATCHES_MAX** | 1 | Single dispatch only |
| **GET_CONTACT_ATTEMPTS_MAX** | 1 | One attempt only; no retries |
| **GET_OPPORTUNITY_ATTEMPTS_MAX** | 0 | Forbidden |
| **SEARCH_CALLS_MAX** | 0 | Forbidden |
| **LIST_CALLS_MAX** | 0 | Forbidden |
| **PAGINATION_CALLS_MAX** | 0 | Forbidden |
| **RETRY_MAX** | 0 | No retries permitted |
| **NOTE_WRITE_ATTEMPTS_MAX** | 0 | Forbidden |
| **STAGE_WRITE_ATTEMPTS_MAX** | 0 | Forbidden |
| **CRM_MUTATIONS_MAX** | 0 | Forbidden |

---

## 5. Authority Lifecycle

### Activation Contract

| Field | Value |
|-------|-------|
| `AUTHORIZATION_STATE_AT_AUTHORING` | `PROPOSED_NOT_EFFECTIVE` |
| `GRANT_ACTIVATION` | `HUMAN_MERGE_TO_MAIN_PLUS_DURABLE_MAIN_RECONCILIATION` |
| `R3_EXECUTION_AUTHORIZED_BEFORE_HUMAN_MERGE` | `NO` |
| `R3_EXECUTION_AUTHORIZED_AFTER_HUMAN_MERGE_AND_MAIN_RECONCILIATION` | `YES` |
| `R3_EXECUTION_ATTEMPTS_MAX` | `1` |
| `R3_SECOND_EXECUTION_AUTHORIZED` | `NO` |
| `R3_RETRY_AUTHORIZED` | `NO` |

### One-Shot Constraints

| Attribute | Value | Implication |
|-----------|-------|-------------|
| `ONE_SHOT` | YES | Single execution only |
| `REUSABLE` | NO | Cannot be reused |
| `TRANSFERABLE` | NO | Cannot be transferred |
| `FAILURE_RESTORES_AUTHORITY` | NO | Failed execution does not restore authorization |
| `R4_AUTHORIZED` | NO | No escalation to R4 permitted |

### Consumption Boundary

| Field | Value |
|-------|-------|
| `AUTHORIZATION_CONSUMPTION_TRIGGER` | `FIRST_TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTION_ATTEMPT_FOR_R3` |
| `AUTHORIZATION_STATE_BEFORE_EXECUTION` | `AVAILABLE` |
| `AUTHORIZATION_STATE_ON_TRIGGER` | `CONSUMED` |
| `AUTHORIZATION_STATE_AFTER_EXECUTION` | `CONSUMED` |
| `ONE_SHOT` | `YES` |
| `REUSABLE` | `NO` |
| `TRANSFERABLE` | `NO` |
| `FAILURE_RESTORES_AUTHORITY` | `NO` |
| `FAILURE_BEFORE_HTTP_DISPATCH_RESTORES_AUTHORITY` | `NO` |
| `FAILURE_AFTER_HTTP_DISPATCH_RESTORES_AUTHORITY` | `NO` |

### Runtime Prohibitions

**The following are FORBIDDEN until this authorization is independently reviewed, human-merged, and reconciled to main:**

- ❌ Secret Manager payload read
- ❌ Token mint operations
- ❌ SQLite database open
- ❌ Production runtime assembly
- ❌ HighLevel HTTP calls

---

## 6. Execution Preconditions

**This authorization PR must:**

1. ✓ Pass authorization-only scope validation
2. ✓ Be independently reviewed by a human (not automated merge)
3. ✓ Be human-approved and merged to main
4. ✓ Be reconciled to main before R3 execution
5. ✓ Remain under version control for audit trail

**After human approval and main reconciliation:**

The R3 GET-contact operation may be executed with these constraints and budgets.

---

## 7. Audit Trail

| Event | Status | Details |
|-------|--------|---------|
| Authorization Created | 2026-08-26T13:29:59Z | Fresh one-shot authorization |
| PR217 Merge Verification | COMPLETE | Reconciled and verified |
| Artifacts Verification | COMPLETE | All required files on main |
| Authorization Scope | SEALED | Ready for independent review |
| Execution Status | PENDING HUMAN REVIEW | Awaiting approval |
| Authorization Reissued | 2026-08-26T17:50:12Z | Temporal provenance corrected; activation contract and consumption boundary added; PR217 merge state reconfirmed |

---

## 8. Next Steps

1. **Commit this authorization** to the authorization branch
2. **Push to remote** for review
3. **Open a PR to main** (do not auto-merge)
4. **Await independent human review** before execution
5. **Do not execute R3** until this PR is merged to main

---

## 9. Addendum: R3 Execution Effect Budget (received pre-merge)

**Added (local time):** 2026-08-26T13:39:08-04:00 (UTC equivalent: 2026-08-26T17:39:08Z)
**Status of PR at time of receipt:** OPEN, `mergedAt=null`, no review decision.

This addendum records a proposed fine-grained execution-effect budget submitted
while this authorization PR was still open and unreviewed. It is recorded here
**for reviewer visibility only**. Receipt of this budget did **not** trigger
execution — the merge gate in Section 6 was not satisfied, so no credential
construction, secret read, token mint, or HighLevel HTTP call was performed.

### Execution attempt ceiling

| Field | Value |
|---|---|
| R3_EXECUTION_ATTEMPTS_MAX | 1 |
| R3_SECOND_EXECUTION_AUTHORIZED | NO |
| R3_RETRY_AUTHORIZED | NO |

### Credential / identity budget

| Field | Value |
|---|---|
| TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS_MAX | 1 |
| SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX | 1 |
| SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX | 1 |
| SERVICE_ACCOUNT_KEY_CREATE_MAX | 0 |
| STANDING_TOKEN_AUTHORITY | NO |

### Secret access budget

| Field | Value |
|---|---|
| SECRET_MANAGER_CLIENT_INSTANTIATIONS_MAX | 1 |
| C4_SECRET_READ_ATTEMPTS_MAX | 1 |
| B2_SECRET_READ_ATTEMPTS_MAX | 1 |
| OTHER_SECRET_READ_ATTEMPTS_MAX | 0 |
| SECRET_PAYLOAD_READS_MAX | 2 |
| SECRET_LIST_CALLS_MAX | 0 |
| SECRET_VERSION_LIST_CALLS_MAX | 0 |
| SECRET_METADATA_DISCOVERY_CALLS_MAX | 0 |

### Storage / runtime assembly budget

| Field | Value |
|---|---|
| DESIGNATED_SQLITE_CREATE_MAX | 0 |
| AT1_EXECUTION_STORE_CONSTRUCTIONS_MAX | 1 |
| AT1_EXECUTION_STORE_EXISTING_OPEN_MAX | 1 |
| PRODUCTION_RUNTIME_ASSEMBLY_MAX | 1 |
| PRODUCTION_RUNTIME_STARTS_MAX | 0 |

### HighLevel transport / call budget

| Field | Value |
|---|---|
| HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS_MAX | 1 |
| HIGHLEVEL_TRANSPORT_INSTANTIATIONS_MAX | 1 |
| NOTE_PATH_ADAPTER_ASSEMBLIES_MAX | 1 |
| HIGHLEVEL_TOTAL_CALLS_MAX | 1 |
| HTTP_REQUEST_DISPATCHES_MAX | 1 |
| GET_CONTACT_ATTEMPTS_MAX | 1 |
| GET_OPPORTUNITY_ATTEMPTS_MAX | 0 |
| SEARCH_CALLS_MAX | 0 |
| LIST_CALLS_MAX | 0 |
| PAGINATION_CALLS_MAX | 0 |
| RETRY_MAX | 0 |

### Mutation / ledger budget (unchanged — all zero)

| Field | Value |
|---|---|
| NOTE_WRITE_ATTEMPTS_MAX | 0 |
| STAGE_WRITE_ATTEMPTS_MAX | 0 |
| CRM_MUTATIONS_MAX | 0 |
| EXECUTION_CLAIMS_MAX | 0 |
| ATTEMPT_RECORDS_MAX | 0 |
| PROTOCOL_LEDGER_EVENT_WRITES_MAX | 0 |
| BUSINESS_LEDGER_EVENT_WRITES_MAX | 0 |
| IAM_MUTATIONS_MAX | 0 |
| DEPLOYMENTS_MAX | 0 |

### Disposition

This budget does not itself authorize execution. It supplements Sections 4 and 5
with tighter, per-resource ceilings for the reviewer to evaluate alongside the
existing binding. `R4_AUTHORIZED=NO` is reaffirmed. Execution against this
budget may only begin after a human reviewer approves and merges this PR to
main — consistent with Section 6.

---

**AUTHORIZATION STATUS: PREPARED FOR INDEPENDENT REVIEW**

**NO EXECUTION PERMITTED UNTIL HUMAN-MERGED TO MAIN**

---

*Generated as part of PR217 reconciliation and R3 execution authorization workflow.*
