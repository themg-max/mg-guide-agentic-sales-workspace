# NW-008 AT8W15 AI Rolodex Backend GHL Capability-Reference Assessment 001

## 1. Unit identity and read-only boundary

```text
UNIT=NW008_AT8W15_AI_ROLODEX_BACKEND_GHL_CAPABILITY_REFERENCE_ASSESSMENT_001
PR_CLASS=planning_only
MODE=READ_ONLY_SOURCE_CAPABILITY_REFERENCE_ASSESSMENT
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

ASSESSMENT_BRANCH=
  nw008-at8w15-ai-rolodex-backend-ghl-capability-reference-assessment-001
ASSESSMENT_BASE_REF=origin/main
ASSESSMENT_BASE_SHA=
  0edf94307aa8f2d7815ec23ac419d8b35a708e09
ASSESSMENT_ARTIFACT=
  docs/nw008/nw-008-at8w15-ai-rolodex-backend-ghl-capability-reference-assessment-001.md

READ_ONLY=YES
SOURCE_REPOSITORY_EDITED=NO
AI_ROLODEX_BACKEND_EDITED=NO
NW008_RUNTIME_EDITED=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
```

This unit inspects one public source file as a capability reference. It does
not import, copy, deploy, invoke, or modify the AI Rolodex backend. It does not
authorize NW-008 implementation or live execution.

```text
MERGING_THIS_ASSESSMENT_CONFERS_IMPLEMENTATION_AUTHORITY=NO
MERGING_THIS_ASSESSMENT_CONFERS_DEPLOYMENT_AUTHORITY=NO
MERGING_THIS_ASSESSMENT_CONFERS_LIVE_EXECUTION_AUTHORITY=NO
```

## 2. Pre-flight and source pin

```text
PRE_FLIGHT=
  pwd|
  git branch --show-current|
  git status --short --untracked-files=all|
  git fetch origin

WORKING_DIRECTORY=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH_AT_PRE_FLIGHT=
  nw008-at8w13-ghlv2-adoption-adapter-staging-suitability-assessment-001
BRANCH_IS_MAIN=NO
UNEXPECTED_DIRTY_WORKTREE=NO
DIRTY_PATH_COUNT=0
ORIGIN_FETCHED=YES
ABORT_TRIGGERED=NO
```

The assessed source is pinned independently from its moving default branch:

```text
SOURCE_REPOSITORY=themg-max/A.I-Rolodex---Context
SOURCE_DEFAULT_BRANCH=main
SOURCE_DEFAULT_BRANCH_HEAD_AT_INSPECTION=
  f3ad12377405b3c8228a3b46dbc299c2a13573db
SOURCE_PATH=services/ghlService.js
SOURCE_BLOB_SHA=
  b26ce2222c54c6f2df7ea7bb6b2b107fd3366902
SOURCE_PATH_LAST_COMMIT=
  8029ba2a4e34cdf58717f21c66ec6bf318194f2e
SOURCE_PATH_LAST_COMMITTED_AT=2026-05-13T15:17:06Z
```

All findings below apply to that exact blob. Later changes to the external
repository require a fresh assessment.

## 3. GHL REST base URL

The source defines:

```text
GHL_REST_BASE_URL=https://services.leadconnectorhq.com
GHL_REST_BASE_URL_MATCHES_NW008=YES
BASE_URL_CALLER_OVERRIDE_PRESENT=NO
```

Every implemented provider request concatenates a fixed path to this authority.
The source does not implement a generic arbitrary-host request function.

This is a useful static reference but not proof that any deployed backend can
currently reach HighLevel.

## 4. PIT authentication construction

The source reads the PIT from the process environment identifier
`CRM_API_KEY` at module load. `getGHLHeaders()` constructs an Authorization
Bearer header from that value and adds version and JSON content headers.

```text
PIT_BEARER_AUTH_CONSTRUCTION_PRESENT=YES
PIT_SOURCE=PROCESS_ENVIRONMENT
PIT_READ_AT_MODULE_LOAD=YES
AUTHORIZATION_HEADER_SCHEME=Bearer
AUTHORIZATION_HEADER_VALUE_LOGGED_BY_CONFIG_LOG=NO
PIT_PRESENCE_BOOLEAN_LOGGED=YES

INJECTED_CREDENTIAL_OBJECT=NO
ROOT_OWNED_CREDENTIAL_INJECTION=NO
SECRET_RESOURCE_IDENTITY_BINDING=NO
SECRET_ACCESSOR_INTERFACE=NO
```

The bearer construction is conceptually consistent with HighLevel PIT use, but
the acquisition seam is incompatible with NW-008. NW-008 forbids environment
token discovery and requires a root-owned accessor to produce an injected,
redaction-safe credential object.

Static source inspection does not establish whether the environment value
exists, is valid, or belongs to the required private location.

## 5. API-Version handling

The assessed source defines a date-valued API version and sends it in the
`Version` header on every request produced by `getGHLHeaders()`:

```text
SOURCE_VERSION_HEADER_NAME=Version
SOURCE_VERSION_HEADER_VALUE=2021-07-28
SOURCE_VERSION_HEADER_CENTRALIZED=YES

NW008_VERSION_HEADER_NAME=Version
NW008_VERSION_HEADER_VALUE=v3
VERSION_HEADER_NAME_MATCH=YES
VERSION_HEADER_VALUE_MATCH=NO
```

The AI Rolodex value must not silently replace NW-008's frozen value. Resolving
which provider contract is authoritative would require a separate governed
design or implementation unit; this assessment does not change either source.

## 6. Location binding

The source reads `LOCATION_ID` from the process environment at module load and
inserts it into every GHL request:

```text
LOCATION_SOURCE=PROCESS_ENVIRONMENT
LOCATION_READ_AT_MODULE_LOAD=YES
OPPORTUNITY_SEARCH_LOCATION_PARAMETER=location_id
PIPELINE_LOCATION_PARAMETER=locationId
MISSING_LOCATION_PRECHECK_PRESENT=YES

VERIFIED_PRIVATE_BINDING_CAPABILITY_REQUIRED=NO
CONTACT_BOUND_TARGET_AUTHORITY=NO
RESPONSE_LOCATION_REBOUND_TO_VERIFIED_CAPABILITY=NO
CALLER_LOCATION_OVERRIDE_ARGUMENT=NO
```

Location scoping is present, but it is configuration scoping rather than
NW-008 capability binding. NW-008 validates a private issued capability before
constructing the note runtime and binds both location and contact identities in
`NotePathAdapter`. The lower HTTP client is intentionally denied target
authority.

## 7. Provider request and error handling

### 7.1 Request behavior

The source uses the runtime-global `fetch` function directly in each networked
method:

```text
HTTP_ABSTRACTION=GLOBAL_FETCH
INJECTABLE_HTTP_SESSION=NO
EXPLICIT_REQUEST_TIMEOUT=NO
EXPLICIT_REDIRECT_REJECTION=NO
AUTOMATIC_RETRY_LOOP_OBSERVED=NO
NO_RETRY_CONTRACT_ENFORCED=NO
REQUEST_BUDGET_LEDGER=NO
```

No retry loop or retry library is present. However, there is no frozen
single-attempt contract, timeout, redirect prohibition, or shared budget.
`fetchAllMetrics()` deliberately invokes three independent GET methods
concurrently against the same opportunity-search route. Those are not retries,
but they demonstrate why this client cannot inherit NW-008's two-call budget.

### 7.2 HTTP and transport errors

The main GET methods:

1. check `response.ok`;
2. read the provider error body as text;
3. log status plus that error text;
4. throw a new error;
5. catch, log the exception message, and rethrow.

Exceptions exist:

- `healthCheck()` catches every request failure and returns `false`;
- three metric methods return numeric zero when credentials are missing;
- `fetchAllMetrics()` uses `Promise.allSettled`, converts individual rejected
  metric calls to zero, and throws only if all three active metric calls fail.

```text
NON_2XX_CHECK_PRESENT=YES
PROVIDER_ERROR_BODY_READ=YES
PROVIDER_ERROR_BODY_LOGGED=YES
TRANSPORT_ERROR_CLASSIFICATION=NO
MUTATION_AMBIGUITY_CLASSIFICATION=NOT_APPLICABLE_NO_MUTATION_METHOD
PARTIAL_FAILURE_SUCCESS_SHAPED_DEFAULTS=YES
HEALTHCHECK_ERROR_DETAIL_PRESERVED=NO
```

These fallbacks are designed for a metrics dashboard, not the fail-closed
NW-008 mutation boundary. They must not be reused for note creation.

## 8. Telemetry

Telemetry is extensive:

```text
CONFIG_TELEMETRY=YES
REQUEST_STATUS_TELEMETRY=YES
REQUEST_LATENCY_TELEMETRY=YES_FOR_OPPORTUNITY_SEARCH_METHODS
METRIC_SUCCESS_FAILURE_TELEMETRY=YES
CONTRACT_COMPLETENESS_TELEMETRY=YES
EXTRACTION_PROVENANCE_TELEMETRY=YES
```

The source also logs provider-derived opportunity samples, identifiers, names,
pipeline/stage values, monetary values, dates, raw metric structures, and the
configured location identifier in several records. Request debug messages
include URLs containing the location query parameter.

```text
RAW_PROVIDER_DERIVED_SAMPLE_LOGGING=YES
PRIVATE_LOCATION_VALUE_CAN_APPEAR_IN_LOGS=YES
CRM_RECORD_IDENTIFIERS_CAN_APPEAR_IN_LOGS=YES
NW008_REDACTED_TELEMETRY_COMPATIBLE=NO
```

NW-008's `ConcreteLiveNoteHttpClient` records only method, URL, header names,
body length, timeout, and redirect posture; it never stores header values. The
bounded transport publishes only `id`, `body`, and `contactId` from the note
envelope. AI Rolodex telemetry is therefore informative as a metrics
operability reference but is not safe to transplant into the NW-008 note path.

## 9. Response normalization

The source performs domain-specific normalization:

- missing opportunities become an empty array;
- pipeline opportunity records become totals, counts, stage summaries,
  forecast values, roster diagnostics, and leadership metrics;
- metric fields are wrapped in a versioned contract with null/zero semantics;
- pipeline metadata is reduced to pipeline and stage identifiers/names;
- dashboard parity output retains a selected opportunity projection.

```text
METRIC_RESPONSE_NORMALIZATION=YES
PIPELINE_METADATA_NORMALIZATION=YES
VERSIONED_METRICS_CONTRACT=YES
RAW_PROVIDER_RESPONSE_RETURNED_DIRECTLY=NO
SELECTED_PROVIDER_RECORD_PROJECTION_RETURNED=YES

NOTE_RESPONSE_NORMALIZATION=NO
NOTE_FIELDS_ID_BODY_CONTACT_ID_NORMALIZATION=NO
SAME_RUN_NOTE_ID_CAPTURE=NO
NOTE_CONTENT_DIGEST_VERIFICATION=NO
```

This is useful evidence of response-shaping experience, but none of the
normalizers implements the NW-008 note envelope or readback proof.

## 10. Implemented GHL methods

| Exported method | Provider effect | Route | Result behavior |
| --- | --- | --- | --- |
| `fetchPipelineTotal` | one GET | `/opportunities/search` with location and limit 100 | returns opportunity-derived pipeline/leadership summary |
| `fetchAppointmentsBooked` | none | none | placeholder numeric zero |
| `fetchShowRate` | none | none | placeholder numeric zero |
| `fetchApplicationsSubmitted` | one GET | `/opportunities/search` with location and limit 100 | returns filtered count |
| `fetchOpportunitiesThisWeek` | one GET | `/opportunities/search` with location and limit 100 | returns filtered count |
| `fetchAllMetrics` | up to three concurrent GETs through methods above | opportunity search | returns normalized metrics; partial failures default to zero |
| `healthCheck` | one GET | `/opportunities/pipelines` with location | returns boolean |
| `fetchPipelineMetadata` | one GET | `/opportunities/pipelines` with location | returns simplified pipelines/stages |
| `getDashboardParityData` | one GET | `/opportunities/search` with location and limit 100 | returns filter metadata and selected opportunities |
| `getCurrentQuarterRange` | none | none | local date calculation |

```text
IMPLEMENTED_GHL_GET_METHOD_FAMILIES=opportunity_search|pipeline_read
IMPLEMENTED_GHL_POST_METHOD_COUNT=0
IMPLEMENTED_CONTACT_METHOD_COUNT=0
IMPLEMENTED_NOTE_METHOD_COUNT=0
NOTE_CREATE_METHOD_PRESENT=NO
NOTE_READBACK_METHOD_PRESENT=NO
SEARCH_OR_LIST_STYLE_PROVIDER_ACCESS_PRESENT=YES
LIMIT_PARAMETER_PRESENT=YES
PAGINATION_IMPLEMENTED=NO
```

The source's `limit=100` access is a search/list-style metrics read. It is
outside NW-008's preserved no-search/list/pagination boundary.

## 11. Comparison to existing NW-008 implementation

### 11.1 BoundedLiveNoteTransport

NW-008's transport already enforces:

```text
NW008_ALLOWED_POST_ROUTE=/contacts/{bound_contact_id}/notes
NW008_ALLOWED_GET_ROUTE=
  /contacts/{bound_contact_id}/notes/{same_run_note_id}
NW008_POST_ATTEMPTS_MAX=1
NW008_POST_SUCCESSES_MAX=1
NW008_READBACK_GET_ATTEMPTS_MAX=1
NW008_TOTAL_NETWORK_CALLS_MAX=2
NW008_TOTAL_MUTATION_CALLS_MAX=1
NW008_AUTOMATIC_RETRY=NO
NW008_SEARCH=NO
NW008_LIST=NO
NW008_PAGINATION=NO
```

The AI Rolodex source has no comparable note route allowlist, same-run state,
mutation ambiguity state, or budget counters.

```text
CAN_REPLACE_BOUNDED_LIVE_NOTE_TRANSPORT=NO
CAN_BE_WRAPPED_WITHOUT_NEW_NW008_LOGIC=NO
```

### 11.2 ConcreteLiveNoteHttpClient

NW-008's concrete client accepts an injected session, performs exactly one
attempt, requires the frozen 10-second timeout, rejects redirects, exposes no
target authority, and retains a redacted call history.

The AI Rolodex source uses direct global fetch calls with no injected session,
explicit timeout, or redirect control.

```text
CAN_REPLACE_CONCRETE_LIVE_NOTE_HTTP_CLIENT=NO
INJECTABLE_SESSION_COMPATIBLE=NO
TIMEOUT_CONTRACT_COMPATIBLE=NO
REDIRECT_CONTRACT_COMPATIBLE=NO
REDACTED_CALL_HISTORY_COMPATIBLE=NO
```

### 11.3 Credential seam

NW-008 uses `RootOwnedLiveNoteCredentialInjection`,
`LiveNoteCredentialProvider`, an injected `LiveNoteSecretAccessor`, and
`InjectedLiveNoteCredential`. Environment token discovery is explicitly
disabled.

```text
AI_ROLODEX_PROCESS_ENV_PIT_PRESENT_IN_SOURCE=YES
NW008_ROOT_OWNED_CREDENTIAL_SEAM_PRESENT=YES
CREDENTIAL_SEAM_COMPATIBLE=NO
PRESERVE_NW008_CREDENTIAL_SEAM=YES
```

### 11.4 Note create/readback path

NW-008's `NotePathAdapter.create_meeting_note()` performs one bound-contact
POST, captures the exact created note ID, and treats ambiguous mutation results
as terminal. `verify_meeting_note()` permits only the same-run note-ID GET and
verifies identity, contact binding, strict body contract, and logical digest.

```text
AI_ROLODEX_NOTE_CREATE_PATH=ABSENT
AI_ROLODEX_NOTE_READBACK_PATH=ABSENT
AI_ROLODEX_SAME_RUN_PROOF=ABSENT
AI_ROLODEX_EXECUTION_STORE_RESERVATION=ABSENT
CAN_REPLACE_NW008_NOTE_CREATE_READBACK_PATH=NO
```

## 12. Capability-reference disposition

The source is a **partial, non-authoritative reference** for:

- the shared provider authority;
- PIT Bearer-header construction;
- centralized `Version` header construction;
- location-scoped GHL GET construction;
- latency/status telemetry concepts;
- domain-specific response normalization.

It is not a reusable NW-008 runtime component.

```text
STATIC_GHL_CAPABILITY_REFERENCE_VALUE=PARTIAL
PROVES_AI_ROLODEX_SOURCE_HAS_GHL_GET_LOGIC=YES
PROVES_DEPLOYED_GHL_CONNECTIVITY=NO
PROVES_VALID_PIT_OR_LOCATION_BINDING=NO
PROVES_NOTE_CAPABILITY=NO

NW008_RUNTIME_REUSE_READY=NO
NW008_NOTE_PATH_REUSE_READY=NO
NW008_CREDENTIAL_REUSE_READY=NO
NW008_HTTP_CLIENT_REUSE_READY=NO
NW008_TRANSPORT_REUSE_READY=NO

RECOMMENDED_USE=REFERENCE_ONLY
SOURCE_IMPORT_RECOMMENDED=NO
SOURCE_COPY_RECOMMENDED=NO
PRODUCTION_BACKEND_EDIT_RECOMMENDED=NO
```

Any future implementation should preserve the existing NW-008 transport,
client, credential, capability-binding, execution-store, and note-verification
boundaries rather than adapting this metrics service into the mutation path.

## 13. Preservation and forbidden effects

```text
PRESERVE=
  mg-guide-ghl-note-runtime service account|
  existing NW008 mutation budgets|
  one POST maximum|
  same-run GET maximum|
  no retry|
  no search/list/pagination

FORBIDDEN=
  HIGHLEVEL_CALL|
  CRM_MUTATION|
  SECRET_PAYLOAD_READ|
  IAM_MUTATION|
  SECRET_MUTATION|
  PRODUCTION_BACKEND_EDIT|
  DEPLOYMENT|
  CLOUD_RUN_DELETION|
  AT8W9_REUSE|
  AT8W10_RETRY

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
PRODUCTION_BACKEND_EDITS=0
DEPLOYMENTS=0
CLOUD_RUN_DELETIONS=0
```

## 14. Final stop

```text
CHANGED_FILE_COUNT=1
EXACT_INTENDED_ARTIFACT_PATH_ONLY=YES
READ_ONLY_SOURCE_ASSESSMENT_COMPLETE=YES
IMPLEMENTATION_AUTHORIZATION_CREATED=NO
IMPLEMENTATION_STARTED=NO
LIVE_EXECUTION_PERFORMED=NO

STOP_FOR_HUMAN_REVIEW=YES
HUMAN_MERGE_REQUIRED=YES
```

AT8W15 stops after recording the capability-reference assessment.
