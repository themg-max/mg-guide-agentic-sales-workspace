# NW-008 — Current GHL Synthetic Record Reconciliation 001

```text
ARTIFACT_ID=NW008_CURRENT_GHL_SYNTHETIC_RECORD_RECONCILIATION_001
ARTIFACT_PATH=proof/nw008/nw-008-current-ghl-synthetic-record-reconciliation-001.md
ARTIFACT_KIND=READ_ONLY_CURRENT_VS_GRANT008_SYNTHETIC_RECORD_RECONCILIATION
UNIT=NW008_CURRENT_GHL_SYNTHETIC_RECORD_RECONCILIATION_001
MODE=READ_ONLY_EVIDENCE_RECONCILIATION
PR_CLASS=proof_readonly

PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PUBLIC_BASE_SHA=9e7643855c5e88c1ab0bd37b3d30e8de45b67c09
PR248_MERGE_SHA=9e7643855c5e88c1ab0bd37b3d30e8de45b67c09
BRANCH=plan/nw008-current-ghl-synthetic-record-reconciliation-001

OWNER=VS_CODE_ORCHESTRATOR
GOVERNANCE_OWNER=HUMAN_GOVERNANCE
HUMAN_MERGE_REQUIRED=YES
SELF_ACTIVATION=FORBIDDEN

JUDGE_DEMO_LIVE_GHL_MUTATION=NO
GRANT008_REUSABLE=NO
GRANT008_REUSED=NO
NEW_LIVE_EXECUTION_AUTHORIZED=NO
NEW_MUTATION_AUTHORIZED=NO
DEMO_FIXTURE_IDS_PRESUMED_EQUAL_LIVE_GHL=NO

RECORDED_AT_UTC=2026-08-28T13:09:30Z
```

## 0. Purpose

Determine whether the synthetic GoHighLevel contact and opportunity currently
reachable through the Grant 008 private exact bindings are the **same** private
exact records targeted by historical Grant 008, and reconcile **current**
note/stage state against the historical Grant 008 proof claims — **read-only**.

This unit does **not**:

- reuse Grant 008 execution authority;
- authorize a new live mutation;
- “fix” CRM state;
- treat public demo fixture identifiers as live GHL record IDs;
- publish raw IDs, note bodies, tokens, PIT values, or idempotency keys.

## 1. Authoritative inputs (read-only)

| Role | Artifact |
| --- | --- |
| Historical live execution claim | `proof/nw008/nw-008-at1-live-execution-result-008.md` |
| One-shot grant (consumed) | `proof/nw008/nw-008-at1-live-execution-grant-008.md` |
| Private binding correction | `proof/nw008/nw-008-at1-grant008-private-binding-correction-001.md` |
| Private binding recon PASS | `proof/nw008/nw-008-at1-grant008-private-binding-reconciliation-pass-001.md` |
| Contest claim posture | `docs/nw008/nw-008-contest-critical-path-rebase-001.md` |
| Demo truth boundary | `docs/demo/meeting-follow-up-demo-v1.md` |

### 1.1 Private binding resolution (local; values not published)

```text
PRIVATE_PACKAGE_SOURCE=local/private/grant008_private_package.json
PRIVATE_PACKAGE_ENV_SOURCE=local/private/grant008_private_package.env
PRIVATE_BINDING_RECON_MACHINE_RESULT=local/private/grant008-private-binding-reconciliation-result.json

CURRENT_SYNTHETIC_CONTACT_BOUND=YES
CURRENT_SYNTHETIC_OPPORTUNITY_BOUND=YES

PRIVATE_CONTACT_BINDING_REF=NW008_GHL_CONTACT_PRIVATE_V1
PRIVATE_OPPORTUNITY_BINDING_REF=NW008_GHL_OPPORTUNITY_PRIVATE_V1
PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
PRIVATE_PIPELINE_BINDING_REF=NW008_GHL_PIPELINE_PRIVATE_V1
PRIVATE_EXPECTED_INITIAL_STAGE_REF=NW008_GHL_EXPECTED_INITIAL_STAGE_PRIVATE_V1
PRIVATE_AUTHORIZED_FINAL_STAGE_REF=NW008_GHL_AUTHORIZED_FINAL_STAGE_PRIVATE_V1
PRIVATE_EXPECTED_NOTE_REF=NW008_GHL_EXPECTED_NOTE_PRIVATE_V1

EXPECTED_NOTE_BINDING_MODE=CONTENT
PRIVATE_VALUES_PUBLISHED=NO
RAW_IDS_PUBLISHED=NO
NOTE_CONTENT_PUBLISHED=NO
PIT_PUBLISHED=NO
IDEMPOTENCY_KEYS_PUBLISHED=NO
```

Public demo fixture identifiers (for example `contact_demo_taylor_001` /
`opp_demo_taylor_001` in `docs/demo/meeting-follow-up-demo-v1.md`) are **not**
presumed equal to live GHL record IDs.

```text
DEMO_FIXTURE_IDS_PRESUMED_EQUAL_LIVE_GHL=NO
JUDGE_DEMO_LIVE_GHL_MUTATION=NO
```

### 1.2 Historical Grant 008 claimed end-state (from public proof)

From `proof/nw008/nw-008-at1-live-execution-result-008.md` (claim packet):

```text
GHL_LIVE_SYNTHETIC_WRITE_PROVEN_CLAIM=YES
TOTAL_GHL_CALLS_EXECUTED_CLAIM=6
MODELED_GHL_WRITES_CLAIM=2
NOTE_WRITES_SUCCEEDED_CLAIM=1
NOTE_READBACK_VERIFIED_CLAIM=YES
STAGE_WRITES_SUCCEEDED_CLAIM=1
FINAL_STAGE_READBACK_VERIFIED_CLAIM=YES
AT1_COMPLETE_CLAIM=YES
EXPECTED_NOTE_BINDING_MODE=CONTENT
GRANT008_STATE=CONSUMED
GRANT008_REUSABLE=NO
```

This reconciliation does **not** re-litigate offline Result-008 response-body
retention gaps. It answers only: **do the currently bound live records still
match Grant 008 targets, and does current note/stage state match the claimed
post-execution end-state?**

## 2. Read-only execution surface

```text
SURFACE=anthropic_v2
ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
AUTH_MODE=private_integration_token_bearer_via_gcp_secret_manager
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm

MCP_PROTOCOL_INITIALIZE_EXECUTED=YES
MCP_PROTOCOL_INITIALIZE_HTTP=200
MCP_PROTOCOL_INITIALIZE_COUNTS_AS_BUSINESS_CALL=NO

BUSINESS_OPERATIONS_EXECUTED=
  execute_operation:get-contact
  execute_operation:get-opportunity
  execute_operation:get-all-notes

BUSINESS_OPERATIONS_NOT_EXECUTED=
  create-note
  update-opportunity
  get-note
  delete-*
  search / fetch / list_locations / get-pipelines
  broad contact/opportunity search
  any write / compensating mutation / cleanup / retry mutation
```

```text
LIVE_GHL_READ_CALLS=6
  # 3 definitive business reads + 3 structure-confirmation re-reads
  # (get-contact, get-opportunity, get-all-notes) × 2 passes
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
SEARCH_CALLS_EXECUTED=0
LIST_LOCATIONS_CALLS_EXECUTED=0
BROAD_SEARCH_EXECUTED=NO
RAW_REST_FALLBACK_USED=NO
```

Exact-contact `get-all-notes` is treated as **note metadata read on the already
bound contact**, not broad search.

## 3. Binding equality results (sanitized)

Private exact IDs were compared in-process only. Public artifact records
equality flags and binding refs — never raw values.

### 3.1 Contact

```text
OPERATION=execute_operation:get-contact
HTTP_SUCCESS=YES
OPERATION_SUCCESS=YES

GRANT008_CONTACT_MATCHES_CURRENT=YES
CONTACT_LOCATION_MATCH=YES
CONTACT_SYNTHETIC_TAG_HINT_PRESENT=YES
PUBLIC_RECORD_PAYLOAD=WITHHELD
```

### 3.2 Opportunity

```text
OPERATION=execute_operation:get-opportunity
HTTP_SUCCESS=YES
OPERATION_SUCCESS=YES

GRANT008_OPPORTUNITY_MATCHES_CURRENT=YES
OPPORTUNITY_CONTACT_RELATION_MATCH=YES
OPPORTUNITY_LOCATION_MATCH=YES
OPPORTUNITY_PIPELINE_MATCH=YES
PUBLIC_RECORD_PAYLOAD=WITHHELD
```

### 3.3 Current stage vs Grant 008 authorized final

```text
CURRENT_OPPORTUNITY_STAGE=EXPECTED_INITIAL
CURRENT_OPPORTUNITY_STAGE_CLASS=EXPECTED_INITIAL
EXPECTED_GRANT008_FINAL_STAGE_MATCH=NO
STAGE_EQUALS_AUTHORIZED_FINAL=NO
STAGE_EQUALS_EXPECTED_INITIAL=YES
```

Observed live `pipelineStageId` equals the Grant 008 **expected initial** stage
binding (`NW008_GHL_EXPECTED_INITIAL_STAGE_PRIVATE_V1`), **not** the authorized
final stage binding (`NW008_GHL_AUTHORIZED_FINAL_STAGE_PRIVATE_V1`).

### 3.4 Expected note presence / fingerprint

```text
OPERATION=execute_operation:get-all-notes
HTTP_SUCCESS=YES
OPERATION_SUCCESS=YES
CONTACT_NOTES_COUNT_OBSERVED=0

GRANT008_EXPECTED_NOTE_PRESENT=NO
GRANT008_EXPECTED_NOTE_FINGERPRINT_MATCH=NO
EXPECTED_NOTE_BINDING_MODE=CONTENT
NOTE_CONTENT_PUBLISHED=NO
```

No notes were returned for the exact bound contact. Content/fingerprint compare
against `NW008_GHL_EXPECTED_NOTE_PRIVATE_V1` therefore cannot succeed.

## 4. Decision matrix application

Required questions:

```text
CURRENT_SYNTHETIC_CONTACT_BOUND=YES
CURRENT_SYNTHETIC_OPPORTUNITY_BOUND=YES

GRANT008_CONTACT_MATCHES_CURRENT=YES
GRANT008_OPPORTUNITY_MATCHES_CURRENT=YES

GRANT008_EXPECTED_NOTE_PRESENT=NO
GRANT008_EXPECTED_NOTE_FINGERPRINT_MATCH=NO

CURRENT_OPPORTUNITY_STAGE=EXPECTED_INITIAL
EXPECTED_GRANT008_FINAL_STAGE_MATCH=NO

HISTORICAL_PROOF_CONSISTENT_WITH_CURRENT_STATE=NO
```

Rule applied:

> IF BOTH MATCH=YES **AND** ANY EXPECTED STATE IS MISSING  
> → `RESULT=CONTRADICTORY_EVIDENCE`  
> → `NEW_MUTATION_AUTHORIZED=NO`  
> → `NEXT=HISTORICAL_AUDIT_AND_PROVIDER_STATE_RECONCILIATION`  
> → STOP

Both identity bindings match Grant 008 targets, but the claimed post-execution
end-state is **not** present on the live records now:

| Expected historical end-state element | Observed now |
| --- | --- |
| Exact synthetic contact binding | **MATCH** |
| Exact synthetic opportunity binding | **MATCH** |
| Grant 008 expected note present (content mode) | **MISSING** (`notes=0`) |
| Authorized final stage | **MISSING** (stage is **expected initial**) |

```text
RESULT=CONTRADICTORY_EVIDENCE
NEW_MUTATION_AUTHORIZED=NO
NEW_LIVE_EXECUTION_REQUIRED_FOR_PROOF=NO
NEW_LIVE_EXECUTION_AUTHORIZED=NO
GRANT008_REUSED=NO
DID_NOT_FIX_RECORD=YES
NEXT=HISTORICAL_AUDIT_AND_PROVIDER_STATE_RECONCILIATION
```

### 4.1 Interpretation (non-mutating)

1. The private Grant 008 contact/opportunity bindings still resolve to live
   records that **are** the historical synthetic targets (identity continuity
   holds).
2. Current CRM state does **not** preserve the Grant 008 claimed note+final-stage
   end-state. Possible non-exclusive explanations (not adjudicated here):
   manual/operator cleanup, later unrelated mutation, provider retention
   behavior, or historical Result-008 claim/evidence gaps already noted in
   `proof/nw008/nw-008-at1-live-execution-result-008-reconciliation.md`.
3. This unit **must not** “repair” stage/note state and **must not** treat Grant
   008 as reusable authority for a rewrite.
4. Judge/demo path remains non-mutating and independent of this live read.

## 5. Explicit non-actions

```text
DID_NOT_CREATE_NOTE=YES
DID_NOT_UPDATE_OPPORTUNITY=YES
DID_NOT_DELETE=YES
DID_NOT_CLEANUP_MUTATION=YES
DID_NOT_RETRY_MUTATION=YES
DID_NOT_CREATE_CONTACT_OR_OPPORTUNITY=YES
DID_NOT_BROAD_SEARCH=YES
DID_NOT_PUBLISH_RAW_IDS=YES
DID_NOT_PUBLISH_NOTE_CONTENT=YES
DID_NOT_PUBLISH_TOKENS_OR_PIT=YES
DID_NOT_PUBLISH_IDEMPOTENCY_KEYS=YES
DID_NOT_REUSE_GRANT008=YES
DID_NOT_AUTHORIZE_NEW_EXECUTION=YES
DID_NOT_CHANGE_IAM=YES
DID_NOT_CHANGE_SECRETS=YES
DID_NOT_DEPLOY=YES
DID_NOT_MUTATE_PRIVATE_REPO=YES
DID_NOT_MUTATE_PUBLIC_RUNTIME_SOURCE=YES
DID_NOT_FIX_RECORD=YES
```

## 6. Return block

```text
PUBLIC_BASE_SHA=9e7643855c5e88c1ab0bd37b3d30e8de45b67c09
BRANCH=plan/nw008-current-ghl-synthetic-record-reconciliation-001
ARTIFACT_ID=NW008_CURRENT_GHL_SYNTHETIC_RECORD_RECONCILIATION_001
ARTIFACT_PATH=proof/nw008/nw-008-current-ghl-synthetic-record-reconciliation-001.md

CURRENT_SYNTHETIC_CONTACT_BOUND=YES
CURRENT_SYNTHETIC_OPPORTUNITY_BOUND=YES

GRANT008_CONTACT_MATCHES_CURRENT=YES
GRANT008_OPPORTUNITY_MATCHES_CURRENT=YES

GRANT008_EXPECTED_NOTE_PRESENT=NO
GRANT008_EXPECTED_NOTE_FINGERPRINT_MATCH=NO
EXPECTED_GRANT008_FINAL_STAGE_MATCH=NO
CURRENT_OPPORTUNITY_STAGE=EXPECTED_INITIAL

HISTORICAL_PROOF_CONSISTENT_WITH_CURRENT_STATE=NO

LIVE_GHL_READ_CALLS=6
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
GRANT008_REUSED=NO
NEW_MUTATION_AUTHORIZED=NO
NEW_LIVE_EXECUTION_AUTHORIZED=NO
NEW_LIVE_EXECUTION_REQUIRED_FOR_PROOF=NO

JUDGE_DEMO_LIVE_GHL_MUTATION=NO
DEMO_FIXTURE_IDS_PRESUMED_EQUAL_LIVE_GHL=NO
PRIVATE_VALUES_PUBLISHED=NO
PUBLIC_RUNTIME_SOURCE_MUTATED=NO
PRIVATE_REPO_MUTATED=NO
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
DEPLOYMENTS=0

RESULT=CONTRADICTORY_EVIDENCE
NEXT=HISTORICAL_AUDIT_AND_PROVIDER_STATE_RECONCILIATION
STOP_CODE=NW008_CURRENT_GHL_SYNTHETIC_RECORD_RECONCILIATION_001_CONTRADICTORY_STOP
```

## 7. Stop

Open **one** proof-only / read-only reconciliation PR with this artifact. Do not
merge automatically. Do not mutate CRM. Do not reuse Grant 008. Return the PR to
ChatGPT for review before any historical-audit or provider-state follow-on.
