# NW-008 AT8W16 AI Rolodex Deployed GHL Connectivity Reference Reconciliation 001

## 1. Unit identity and read-only boundary

```text
UNIT=NW008_AT8W16_AI_ROLODEX_DEPLOYED_GHL_CONNECTIVITY_REFERENCE_RECONCILIATION_001
PR_CLASS=planning_only
MODE=READ_ONLY_DEPLOYED_CONNECTIVITY_REFERENCE
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

RECONCILIATION_BRANCH=
  nw008-at8w16-ai-rolodex-deployed-ghl-connectivity-reference-reconciliation-001
RECONCILIATION_BASE_REF=origin/main
RECONCILIATION_BASE_SHA=
  ad4e3d989a4ddcfd3041c7057d7d162e9e475065
RECONCILIATION_ARTIFACT=
  docs/nw008/nw-008-at8w16-ai-rolodex-deployed-ghl-connectivity-reference-reconciliation-001.md
OBSERVED_AT=2026-08-23T20:00:05Z

TARGET_SERVICE=ai-rolodex-crm-backend
TARGET_PROJECT=ai-rolodex-to-crm
TARGET_PROJECT_NUMBER=831270426395
TARGET_REGION=us-east4

READ_ONLY=YES
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
CLOUD_RUN_CONFIGURATION_CHANGES=0
DEPLOYMENTS=0
```

This unit reconciles static source findings from merged AT8W15 with current
deployed Cloud Run metadata and bounded recent logs. It does not invoke the
backend or HighLevel.

```text
MERGING_THIS_RECONCILIATION_CONFERS_IMPLEMENTATION_AUTHORITY=NO
MERGING_THIS_RECONCILIATION_CONFERS_DEPLOYMENT_AUTHORITY=NO
MERGING_THIS_RECONCILIATION_CONFERS_LIVE_EXECUTION_AUTHORITY=NO
```

## 2. Pre-flight and merged predecessor binding

```text
PRE_FLIGHT=
  pwd|
  git branch --show-current|
  git status --short --untracked-files=all|
  git fetch origin

WORKING_DIRECTORY=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH_AT_PRE_FLIGHT=
  nw008-at8w15-ai-rolodex-backend-ghl-capability-reference-assessment-001
BRANCH_IS_MAIN=NO
UNEXPECTED_DIRTY_WORKTREE=NO
DIRTY_PATH_COUNT=0
ORIGIN_FETCHED=YES
ABORT_TRIGGERED=NO

PR180_STATE=MERGED
PR180_REVIEWED_HEAD=
  a1fe146773a8ae468047464374e6c003b029f4bb
PR180_ACTUAL_MERGE_COMMIT=
  6e9a12eb7d9071db8c88e51b9f01ae155f877b11

PR183_STATE=MERGED
PR183_REVIEWED_HEAD=
  9c5571df267482e925b1a9fbe6b6e28bff57ab7d
PR183_ACTUAL_MERGE_COMMIT=
  ad4e3d989a4ddcfd3041c7057d7d162e9e475065
PR183_MERGE_COMMIT_EQUALS_RECONCILIATION_BASE_SHA=YES
```

Merged AT8W15 remains the static capability-reference baseline. AT8W16 adds
deployed evidence; it does not reverse AT8W15's finding that the AI Rolodex
metrics client cannot replace the NW-008 note path.

## 3. Public-safety and inspection method

Only these read-only surfaces were inspected:

1. Cloud Run service metadata.
2. Current revision metadata.
3. Container image digest and in-toto/SLSA provenance.
4. Environment key names and value-source classes.
5. Secret Manager reference metadata, never payloads.
6. Bounded Cloud Logging entries reduced to timestamps, severity, revision,
   event class, status class, latency availability, and route family.
7. The exact deployed source commit for event-to-route interpretation.

```text
DO_NOT_PUBLISH=
  PIT|
  secret value|
  location ID|
  contact ID|
  opportunity ID|
  raw provider payload|
  customer data

PIT_PUBLISHED=NO
SECRET_VALUE_PUBLISHED=NO
LOCATION_ID_VALUE_PUBLISHED=NO
CONTACT_ID_PUBLISHED=NO
OPPORTUNITY_ID_PUBLISHED=NO
RAW_PROVIDER_PAYLOAD_PUBLISHED=NO
CUSTOMER_DATA_PUBLISHED=NO
```

No service URL was requested and no backend route was invoked.

## 4. Current Cloud Run service and revision

```text
SERVICE_NAME=ai-rolodex-crm-backend
SERVICE_PROJECT=ai-rolodex-to-crm
SERVICE_PROJECT_NUMBER=831270426395
SERVICE_REGION=us-east4
SERVICE_UID=1d11f60c-23ef-4080-ad87-3e97544a8f01
SERVICE_GENERATION=6928
SERVICE_READY=True

LATEST_CREATED_REVISION=ai-rolodex-crm-backend-04111-dhw
LATEST_READY_REVISION=ai-rolodex-crm-backend-04111-dhw
CURRENT_TRAFFIC_REVISION=ai-rolodex-crm-backend-04111-dhw
CURRENT_TRAFFIC_PERCENT=100

REVISION_NAME=ai-rolodex-crm-backend-04111-dhw
REVISION_UID=52b80c48-536f-4ad1-957a-6f68f4ff23e3
REVISION_CREATED_AT=2026-07-14T04:09:48.065448Z
REVISION_READY=True
REVISION_ACTIVE=True

DEPLOYED_BACKEND_REVISION_IDENTIFIED=YES
```

The current service and log evidence resolve to the same revision.

## 5. Container image and source provenance

The service template names a commit-shaped image tag. The active revision
resolves it to one immutable digest:

```text
DEPLOYED_SOURCE_COMMIT=
  0321b906e71cdb8f91606572574b78992ec7e86b
DEPLOYED_IMAGE_DIGEST=
  sha256:5d6e0d02ac2e351fb5cf5325c44e5069a3f49a104db339f37a46487090cd12ff
DEPLOYED_IMAGE_REPOSITORY=
  us-docker.pkg.dev/ai-rolodex-to-crm/gcr.io/ai-rolodex-backend
SLSA_BUILD_LEVEL=3
```

Read-only Artifact Analysis provenance establishes:

- the exact digest as the provenance subject;
- the subject tag ending in the exact source commit above;
- a successful Google Cloud Build;
- an in-toto SLSA v1 statement;
- build completion immediately before revision creation.

The exact commit exists in `themg-max/A.I-Rolodex---Context`, and its deploy
check completed successfully.

```text
IMAGE_DIGEST_IDENTIFIED=YES
IMAGE_TO_SOURCE_COMMIT_PROVENANCE_IDENTIFIED=YES
SOURCE_COMMIT_EXISTS_IN_CANONICAL_REPOSITORY=YES
DEPLOY_CHECK_SUCCESS_AT_SOURCE_COMMIT=YES

DEPLOYED_SOURCE_IMAGE_PROVENANCE_IDENTIFIED=YES
```

No source archive or build payload is reproduced.

## 6. Runtime service account

```text
DEPLOYED_RUNTIME_SERVICE_ACCOUNT=
  github-ci-deployer@ai-rolodex-to-crm.iam.gserviceaccount.com
DEPLOYED_RUNTIME_SERVICE_ACCOUNT_IDENTIFIED=YES

NW008_PRESERVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCHES_NW008=NO
```

The deployed AI Rolodex identity is evidence about that backend only. It is not
a candidate replacement for the dedicated NW-008 runtime identity.

## 7. GHL credential and location configuration

The current revision's environment metadata contains the source-consumed
credential key name `CRM_API_KEY`. Its value source is a Cloud Run Secret
Manager reference. Only the key name and source class were inspected.

```text
GHL_CREDENTIAL_CONFIGURATION_PRESENT=YES
GHL_CREDENTIAL_CONFIGURATION_CLASS=SECRET_REFERENCE
GHL_CREDENTIAL_SECRET_REFERENCE_PRESENT=YES
GHL_CREDENTIAL_SECRET_VERSION_SELECTOR_CLASS=ALIAS
GHL_CREDENTIAL_SECRET_PAYLOAD_READ=NO
GHL_CREDENTIAL_VALUE_PUBLISHED=NO
```

The source-consumed `LOCATION_ID` key name is also present. It is configured as
a plain environment value rather than a Secret Manager reference. The value
was neither displayed nor recorded.

```text
GHL_LOCATION_CONFIGURATION_PRESENT=YES
GHL_LOCATION_CONFIGURATION_CLASS=PLAIN_ENV
GHL_LOCATION_VALUE_READ_FOR_PUBLICATION=NO
GHL_LOCATION_VALUE_PUBLISHED=NO
```

This establishes configuration presence, not correctness of the private
location binding or authorization scope.

## 8. Bounded recent GHL log reconciliation

### 8.1 Window and sanitization

```text
LOG_WINDOW_START=2026-08-16T19:55:00Z
LOG_WINDOW_END=2026-08-23T20:00:05Z
LOG_WINDOW_CLASS=BOUNDED_RECENT_SEVEN_DAY
TARGET_LOG_RESOURCE=cloud_run_revision
TARGET_LOG_SERVICE=ai-rolodex-crm-backend

SUCCESS_EVENT_QUERY_LIMIT=100
ERROR_EVENT_QUERY_LIMIT=100
RAW_LOG_MESSAGE_PUBLISHED=NO
RAW_STRUCTURED_METADATA_PUBLISHED=NO
```

The success query reached its limit; it proves presence but is not presented as
an exhaustive count.

### 8.2 Success-path evidence

The exact deployed source emits `GHL_RAW_OPPORTUNITIES_RESPONSE` only after:

1. GET `/opportunities/search` returns `response.ok`;
2. the response JSON is parsed;
3. request latency is calculated.

The bounded log query found 100 such events, all from the current revision,
between `2026-08-23T03:30:09Z` and `2026-08-23T19:30:10Z`.

```text
RECENT_GHL_SUCCESS_EVENT_CLASS=GHL_RAW_OPPORTUNITIES_RESPONSE
RECENT_GHL_SUCCESS_EVENT_SAMPLE_COUNT=100
RECENT_GHL_SUCCESS_EVENT_QUERY_LIMIT_REACHED=YES
RECENT_GHL_SUCCESS_EVENT_REVISION_MATCH=YES
RECENT_GHL_SUCCESS_EVENT_SEVERITY=INFO

RECENT_GHL_REQUEST_SUCCESS_TELEMETRY_PRESENT=YES
RECENT_GHL_ROUTE_FAMILY=OPPORTUNITY_SEARCH
RECENT_GHL_STATUS_CLASS=SUCCESS_2XX_INFERRED_FROM_RESPONSE_OK_GATE
```

No customer record, location, provider payload, or URL query value is
published.

### 8.3 Error evidence

A separate seven-day query for severity `ERROR` entries containing the GHL
classification returned zero entries.

```text
RECENT_GHL_ERROR_EVENT_SAMPLE_COUNT=0
RECENT_GHL_ERROR_EVENT_QUERY_LIMIT_REACHED=NO
RECENT_GHL_REQUEST_ERROR_TELEMETRY_PRESENT=NO
```

`NO` means no matching recent error telemetry was present in the bounded
window. It does not guarantee that no historical or unlogged failure has ever
occurred.

### 8.4 Status and latency retention

The deployed source intends to attach numeric response status and latency to
the success event. The current logging sink retains only the event label for
the inspected entries; the numeric fields are not present in retained log
metadata.

```text
RECENT_GHL_EXACT_STATUS_VALUE_PRESENT=NO
RECENT_GHL_EXACT_STATUS_VALUE=UNKNOWN
RECENT_GHL_STATUS_CLASS=SUCCESS_2XX_INFERRED_FROM_RESPONSE_OK_GATE

RECENT_GHL_LATENCY_VALUE_PRESENT=NO
RECENT_GHL_LATENCY_MS=UNKNOWN
```

The success-path event plus the pinned source is sufficient to classify a
successful 2xx opportunity-search exchange, but not its exact status code or
latency.

## 9. Deployed connectivity disposition

Evidence joins across:

1. current revision identity;
2. immutable image digest;
3. SLSA provenance to exact source commit;
4. source-consumed credential and location configuration presence;
5. current-revision success-path events emitted after an `ok` GHL response and
   JSON parse.

```text
DEPLOYED_BACKEND_REVISION_IDENTIFIED=YES
DEPLOYED_SOURCE_IMAGE_PROVENANCE_IDENTIFIED=YES
DEPLOYED_RUNTIME_SERVICE_ACCOUNT_IDENTIFIED=YES

GHL_CREDENTIAL_CONFIGURATION_PRESENT=YES
GHL_CREDENTIAL_CONFIGURATION_CLASS=SECRET_REFERENCE
GHL_LOCATION_CONFIGURATION_PRESENT=YES

RECENT_GHL_REQUEST_SUCCESS_TELEMETRY_PRESENT=YES
RECENT_GHL_REQUEST_ERROR_TELEMETRY_PRESENT=NO

DEPLOYED_GHL_CONNECTIVITY_EVIDENCE=YES
DEPLOYED_GHL_CONNECTIVITY_SCOPE=
  read-only opportunity-search response path on the current AI Rolodex revision
```

This does **not** prove:

- note-create permission;
- contact-note readback permission;
- the NW-008 private contact binding;
- the NW-008 mutation budget;
- safe mutation ambiguity behavior;
- the dedicated NW-008 runtime identity chain.

```text
DEPLOYED_NOTE_CREATE_CAPABILITY_PROVEN=NO
DEPLOYED_NOTE_READBACK_CAPABILITY_PROVEN=NO
NW008_LIVE_NOTE_READINESS_PROVEN=NO
```

## 10. AI Rolodex pattern map

| AI_ROLODEX_PATTERN | NW008_COMPATIBILITY | PRESERVE / ADAPT / REJECT | EVIDENCE | RATIONALE |
| --- | --- | --- | --- | --- |
| Fixed `services.leadconnectorhq.com` authority | Compatible authority | **PRESERVE** | Pinned deployed source | Same provider authority; NW-008 route allowlist remains controlling |
| Bearer PIT construction | Conceptually compatible | **ADAPT** | Pinned deployed source + secret-backed key presence | Keep PIT semantics but acquire only through the NW-008 root-owned credential seam |
| Secret-backed environment credential | Incompatible acquisition seam | **REJECT** for direct reuse | Cloud Run key/source metadata | NW-008 forbids environment token discovery and requires injected credentials |
| Secret version alias | Incompatible with exact pinning | **REJECT** | Cloud Run secret-reference metadata | NW-008 production design requires governed exact resource/version binding |
| Plain-environment location configuration | Incompatible target authority | **REJECT** | Cloud Run key/source metadata | NW-008 location/contact authority comes from a verified private capability |
| Direct global `fetch` calls | Incompatible HTTP boundary | **REJECT** | Pinned deployed source | No injected session, frozen timeout, or redirect rejection |
| No retry loop observed | Compatible principle | **PRESERVE** | Pinned deployed source | Preserve the stronger explicit NW-008 no-retry enforcement |
| Opportunity search with limit | Forbidden route family | **REJECT** | Pinned source + deployed event mapping | NW-008 forbids search, list, and pagination |
| Success-path event after `response.ok` and JSON parse | Useful evidence pattern | **ADAPT** | Current-revision logs + pinned source | Retain redacted outcome evidence but persist safe status/latency fields |
| Provider-derived diagnostic logging | Incompatible disclosure boundary | **REJECT** | Merged AT8W15 source assessment | NW-008 must not publish raw provider/customer data |
| Metrics response normalization | Different domain contract | **REJECT** for note path | Pinned source | It does not normalize or verify the note envelope |
| AI Rolodex runtime service account | Incompatible runtime identity | **REJECT** | Current revision metadata | Preserve the dedicated `mg-guide-ghl-note-runtime` principal |
| SLSA digest-to-source provenance | Compatible evidence method | **PRESERVE** | Artifact Analysis provenance | Exact deployed-source binding is useful without changing runtime authority |

## 11. Preserved NW-008 boundaries

```text
PRESERVE_NW008=
  mg-guide-ghl-note-runtime service account|
  BoundedLiveNoteTransport|
  ConcreteLiveNoteHttpClient|
  RootOwnedLiveNoteCredentialInjection|
  one POST maximum|
  same-run GET maximum|
  no retry|
  no search|
  no list|
  no pagination

AI_ROLODEX_BACKEND_USED_AS_NW008_RUNTIME=NO
AI_ROLODEX_RUNTIME_SERVICE_ACCOUNT_REUSED=NO
AI_ROLODEX_CREDENTIAL_SEAM_REUSED=NO
AI_ROLODEX_SEARCH_ROUTE_REUSED=NO
```

Deployed connectivity evidence is a reference, not an implementation shortcut.

## 12. Remaining external inputs and authorization stop

Merged AT8W12A normalized unresolved external facts to `UNKNOWN`. AT8W16 does
not resolve the NW-008 external identity chain, commitment-key inputs, or
production execution-store inputs.

```text
NW008_EXTERNAL_IDENTITY_INPUTS_AFFIRMATIVELY_RESOLVED=NO
NW008_COMMITMENT_KEY_INPUTS_AFFIRMATIVELY_RESOLVED=NO
NW008_PRODUCTION_STORE_INPUTS_AFFIRMATIVELY_RESOLVED=NO

B2_IMPLEMENTATION_AUTHORIZATION_CREATED=NO
C2_IMPLEMENTATION_AUTHORIZATION_CREATED=NO
C3_IMPLEMENTATION_AUTHORIZATION_CREATED=NO
C4_IMPLEMENTATION_AUTHORIZATION_CREATED=NO

DO_NOT_CREATE_B2_C2_C3_C4_IMPLEMENTATION_AUTHORIZATION_UNTIL=
  AT8W16 reviewed and external identity commitment-key and store inputs
  affirmatively resolved
```

## 13. Forbidden effects and effect ledger

```text
FORBIDDEN=
  HIGHLEVEL_CALL|
  CRM_MUTATION|
  SECRET_PAYLOAD_READ|
  IAM_MUTATION|
  SECRET_MUTATION|
  BACKEND_SOURCE_EDIT|
  NW008_RUNTIME_SOURCE_EDIT|
  DEPLOYMENT|
  CLOUD_RUN_CONFIGURATION_CHANGE|
  SURFACE4_SERVICE_MODIFICATION|
  NEW_SERVICE_ACCOUNT

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
BACKEND_SOURCE_EDITS=0
NW008_RUNTIME_SOURCE_EDITS=0
DEPLOYMENTS=0
CLOUD_RUN_CONFIGURATION_CHANGES=0
SURFACE4_SERVICE_MODIFICATIONS=0
NEW_SERVICE_ACCOUNTS=0
```

## 14. Final disposition and stop

```text
DEPLOYED_GHL_CONNECTIVITY_EVIDENCE=YES
CONNECTIVITY_EVIDENCE_IS_REFERENCE_ONLY=YES
NW008_LIVE_NOTE_READINESS_PROVEN=NO

CHANGED_FILE_COUNT=1
EXACT_INTENDED_PLANNING_ARTIFACT_ONLY=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
```

AT8W16 stops after read-only deployed connectivity reconciliation.
