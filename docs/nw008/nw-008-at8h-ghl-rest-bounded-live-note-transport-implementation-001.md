# NW-008 AT-8H — Bounded Live NOTE Transport Implementation 001

```text
UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001
PR_CLASS=implementation
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=47fc7166557e79c867c6e428d1ca464c9a7fc385
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT

LIVE_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
REAL_CREDENTIAL_USE=NO
SECRET_ACCESS=NO
```

## Scope

This unit implements the bounded HighLevel v3 note transport seam authorized
by merged PR #111. The transport is injectable into existing `NotePathAdapter`
via `dispatch(method, path, body=None)` and does not modify NOTE_PATH,
At1ExecutionStore, or the PR107 trust boundary.

Frozen routes:

```text
POST /contacts/{bound_contact_id}/notes
GET  /contacts/{bound_contact_id}/notes/{same_run_note_id}
```

## Runtime bounds

```text
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
AUTOMATIC_RETRY=NO
SECOND_POST=NO
SEARCH=NO
LIST=NO
PAGINATION=NO
FALLBACK=NO
ALTERNATE_TARGET=NO
GENERIC_EXECUTE=NO
RAW_REST_FALLBACK=NO
```

POST timeout or transport uncertainty classifies `status=ambiguous`. Business
effect truth remains `UNKNOWN`. No retry and no second POST are performed.

## HTTP seam

HTTP is performed only through an injected client. The module does not import
socket or HTTP libraries, does not construct a network client, and does not
discover environment secrets. AT8H tests inject a scripted client and execute
zero real HighLevel calls.

Credentials are injected synthetic placeholders only. Authorization headers
and tokens are not logged and are not published on the NOTE_PATH response.
Transport call history is private and records only redacted route shapes, so
bound contact IDs and same-run note IDs are not exposed through diagnostics.

Provider responses are normalized to `{note: {id, body, contactId}}`. Extra
provider fields are stripped. A 2xx POST without a provider note envelope and
a nonempty string `note.id` is classified ambiguous, consumes the single POST
attempt, and does not unlock same-run GET.

## Non-authority

```text
AT8H_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8H_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8H_AUTHORIZES_LIVE_READ=NO
AT8H_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8H_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8H_AUTHORIZES_SECRET_ACCESS=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO
```

Next governed step after this implementation PR is exact-head review and
merge, then read-only live execution boundary reinspection. Live mutation
requires a later separate one-shot grant.
