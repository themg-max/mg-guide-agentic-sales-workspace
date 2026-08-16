# NW-008 AT-1 — Read-Only External Verification Grant

```text
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_001
GRANT_TYPE=READ_ONLY_EXTERNAL_VERIFICATION
ARTIFACT_KIND=BOUNDED_READ_ONLY_EXTERNAL_VERIFICATION_GRANT
OWNER_LANE=VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
BOUND_TRACK_A_BASELINE_PATH=proof/nw008/nw-008-at1-safe-environment-readiness.md
```

This artifact is **AUTHORIZATION ONLY** for a bounded **read-only** external GHL
environment verification lane. It does **not** authorize AT-1 mutation execution,
write operations, credential creation/expansion, IAM/secrets/deployment changes,
Firestore mutation, raw REST fallback, search/list/pagination, retry, or
compensating mutation.

Self-activation is **FORBIDDEN**. No external CRM read may run until human
countersignature fields below are non-pending and `GRANT_STATE` is flipped by an
explicit human approving authority.

## Bound Track A baseline (frozen)

```text
TRACK_A_READINESS_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
DETERMINISTIC_EXECUTOR_READY=YES
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
PRIVATE_BINDING_PUBLICATION=NO
```

Baseline disposition at grant authoring: deterministic executor ready under
synthetic fixtures; external GHL environment not verified; environment not ready;
AT-1 execution unauthorized.

## Authority and countersignature

```text
REQUEST_INITIATOR=VS_CODE_ORCHESTRATOR_OPERATOR_LANE
APPROVING_AUTHORITY=PENDING_EXPLICIT_HUMAN_AUTHORITY
GRANT_STATE=READY_FOR_HUMAN_COUNTERSIGNATURE
HUMAN_COUNTERSIGNATURE=PENDING
HUMAN_APPROVER=PENDING
APPROVED_AT=PENDING
SELF_ACTIVATION=FORBIDDEN
EXPIRY=60_MINUTES_AFTER_APPROVAL
```

### Human countersignature block (fill only by approving human)

```text
# Human approver completes all fields below to activate this grant.
# Leave PENDING until signed. Do not self-activate.

HUMAN_COUNTERSIGNATURE=PENDING
HUMAN_APPROVER=
APPROVED_AT=
APPROVAL_STATEMENT=
# Required approval statement when signing:
# "I authorize NW008_AT1_RO_EXTERNAL_VERIFY_001 read-only external verification
#  only, bound to TRACK_A_READINESS_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a,
#  with MUTATION_CALLS_MAX=0, CRM_RECORD_READS_MAX=4, expiry 60 minutes after approval.
#  AT-1 execution remains unauthorized."

GRANT_STATE_AFTER_SIGNATURE=AUTHORIZED_READ_ONLY_EXTERNAL_VERIFICATION
```

Until countersigned:

```text
EXTERNAL_READS_AUTHORIZED=NO
MCP_DISCOVERY_AUTHORIZED=NO
OPERATOR_EXECUTION_AUTHORIZED=NO
```

After valid countersignature (and only until expiry):

```text
EXTERNAL_READS_AUTHORIZED=YES
MCP_DISCOVERY_AUTHORIZED=YES
OPERATOR_EXECUTION_AUTHORIZED=YES_READ_ONLY_WITHIN_GRANT
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Hard caps

```text
CRM_RECORD_READS_MAX=4
MUTATION_CALLS_MAX=0
MCP_TOOLS_LIST_MAX=1
MCP_SCHEMA_DISCOVERY_MAX=UNBOUNDED_WITHIN_ALLOWED_OPERATION_SET_ONLY
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
RAW_REST_FALLBACK=NO
SEARCH_LIST_PAGINATION=NO
FIRESTORE_MUTATION=NO
IAM_SECRETS_DEPLOYMENT_CHANGE=NO
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
EXPIRY=60_MINUTES_AFTER_APPROVAL
```

## ALLOWED (after countersignature only)

```text
ALLOWED_EXACT_LOCATION_READ=YES
ALLOWED_EXACT_CONTACT_READ=YES
ALLOWED_EXACT_OPPORTUNITY_READ=YES
ALLOWED_EXACT_PIPELINE_BY_ID_READ=YES
ALLOWED_MCP_TOOLS_LIST=YES
ALLOWED_MCP_OPERATION_DISCOVERY=YES
ALLOWED_MCP_OPERATION_SCHEMA_DESCRIPTION=YES
```

Exact CRM reads (count toward `CRM_RECORD_READS_MAX=4`):

1. location (exact id from private binding)
2. contact (exact id from private binding)
3. opportunity (exact id from private binding)
4. pipeline by exact pipelineId (from opportunity read; stop if unavailable)

MCP control-plane (not CRM record reads; discovery only):

- tools/list / equivalent connector tool enumeration
- operation name discovery for the required AT-1 surface
- operation schema description for required ops

## BLOCKED (always in this grant)

```text
BLOCKED_RECORD_SEARCH=YES
BLOCKED_RECORD_LIST_PAGINATION=YES
BLOCKED_CREATE_NOTE_EXECUTION=YES
BLOCKED_UPDATE_OPPORTUNITY_EXECUTION=YES
BLOCKED_ANY_OTHER_MUTATION=YES
BLOCKED_RAW_REST_FALLBACK=YES
BLOCKED_FIRESTORE_MUTATION=YES
BLOCKED_IAM_SECRETS_DEPLOYMENT_CHANGES=YES
BLOCKED_RETRY=YES
BLOCKED_COMPENSATING_MUTATION=YES
BLOCKED_PRODUCTION_CRM=YES
BLOCKED_PRIVATE_ID_PUBLICATION_TO_PUBLIC_REPO=YES
BLOCKED_AT1_MUTATION_EXECUTION=YES
BLOCKED_CREDENTIAL_CREATE_OR_EXPAND=YES
```

## Expected credential scopes (read-only)

Before any operator use, verify integration scopes in the GHL UI against:

```text
EXPECTED_READONLY_SCOPES=locations.readonly;contacts.readonly;opportunities.readonly
```

PIT / token handling:

```text
PIT_IN_CHAT=FORBIDDEN
PIT_IN_COMMIT=FORBIDDEN
PIT_IN_TERMINAL_LOGS=FORBIDDEN
PIT_IN_PROOF=FORBIDDEN
PIT_STORAGE=EXISTING_SECRET_STORAGE_OR_LOCAL_MCP_CONFIG_ONLY
```

If write scopes or unrelated broad scopes make the credential unsuitable for a
read-only verification lane:

```text
STOP_CODE=CREDENTIAL_SCOPE_TOO_BROAD
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

Do **not** create or expand credentials in this lane.

## Private binding (operator lane only)

Use existing private evidence only. Do **not** copy private IDs into this public
proof artifact.

```text
PRIVATE_LOCATION_ID_SOURCE=BUSINESS_PROFILE_SCREENSHOT
PRIVATE_CONTACT_ID_SOURCE=SYNTHETIC_CONTACT_AUDIT_LOG
PRIVATE_OPPORTUNITY_ID_SOURCE=SYNTHETIC_OPPORTUNITY_AUDIT_LOG
PRIVATE_BINDING_PUBLICATION=NO
```

### Reuse provenance (required before NW-008 binding)

```text
CONTACT_REUSE_NOTE=EXISTING_SYNTHETIC_CONTACT_AUDIT_INCLUDES_NW013_TAG
CONTACT_REUSE_PROVENANCE_REQUIRED=YES
CONTACT_REUSE_PROVENANCE_STATUS=PENDING_OPERATOR_RECORD_IN_PRIVATE_LANE
NW008_BINDING_OF_REUSED_SYNTHETIC_CONTACT=ALLOWED_ONLY_AFTER_PROVENANCE_RECORDED_PRIVATELY
```

Record reuse provenance in the **private** operator evidence pack before binding
the contact to NW-008 reads. Public repo remains free of private IDs.

## Post-countersignature operator procedure (do not run before approval)

### A. Credential scope gate

1. Open GHL UI integration scopes for the existing connector credential.
2. Confirm expected read-only scopes (or a clearly read-bounded subset suitable
   for this lane).
3. If write or unrelated broad scopes render the credential unsuitable →
   `STOP_CODE=CREDENTIAL_SCOPE_TOO_BROAD` (no credential mutation).

### B. MCP discovery (verify presence; do not execute mutations)

Enumerate MCP tools/control-plane metadata. Required runtime operation mappings
to **VERIFY (presence + schema), not execute**:

```text
REQUIRED_OP_MAPPINGS=get-contact;get-opportunity;create-note;get-note;update-opportunity
```

Notes:

- `create-note` and `update-opportunity` must be **present and schema-described**
  for future AT-1 readiness accounting, but **must not be executed** under this
  grant (`MUTATION_CALLS_MAX=0`).
- If `create-note` or `get-note` is absent from the MCP tool surface:

```text
STOP_CODE=REQUIRED_GHL_OPERATIONS_MISSING
REQUIRED_GHL_OPERATIONS_VERIFIED=NO
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

### C. Exact CRM reads (max 4; exact IDs only)

1. **Location** — exact private location id.
2. **Contact** — exact private contact id (after reuse provenance recorded).
3. **Opportunity** — exact private opportunity id.
4. **Pipeline** — exact `pipelineId` from opportunity read only.

From opportunity read, verify and record **privately**:

```text
opportunity.location_binding
opportunity.contact_binding
opportunity.pipelineId
opportunity.current_pipelineStageId
```

From exact pipeline read, verify and record **privately**:

```text
current_stage_exists
human_selected_final_stage_exists
authorized_final_stage_id
```

If exact pipeline read is unavailable:

```text
STOP_CODE=EXACT_PIPELINE_READ_UNAVAILABLE
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

### D. Success / failure disposition (after operator run)

On full success of discovery + four exact reads + stage existence checks, a
**separate** Track A readiness update (not this grant file) may record:

```text
SUCCESS:
EXTERNAL_ENVIRONMENT_VERIFIED=YES
ENVIRONMENT_READY=YES
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Any stop condition or cap breach:

```text
FAILURE:
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
<specific STOP_CODE>
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

This grant never flips `AT1_EXECUTION_AUTHORIZED` to YES.

## Relationship to Track A readiness

| Surface | State at grant authoring |
| --- | --- |
| Deterministic executor (fixtures) | VERIFIED (`DETERMINISTIC_EXECUTOR_READY=YES`) |
| External GHL environment | NOT VERIFIED |
| This grant | `READY_FOR_HUMAN_COUNTERSIGNATURE` |
| AT-1 mutation execution | UNAUTHORIZED |

Updating Track A external flags requires a post-verification proof amendment after
a countersigned operator run completes within caps and expiry.

## STOP

```text
STOP_CODE=NW008_AT1_RO_EXTERNAL_VERIFY_GRANT_READY_FOR_HUMAN_COUNTERSIGNATURE
GRANT_ID=NW008_AT1_RO_EXTERNAL_VERIFY_001
GRANT_STATE=READY_FOR_HUMAN_COUNTERSIGNATURE
BOUND_TRACK_A_BASELINE_SHA=7e5982e2ffe3cd873550f18e8a2f37a97d497e8a
MUTATION_CALLS_MAX=0
CRM_RECORD_READS_MAX=4
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=HUMAN_COUNTERSIGNATURE_REQUIRED_BEFORE_ANY_EXTERNAL_READ
```
