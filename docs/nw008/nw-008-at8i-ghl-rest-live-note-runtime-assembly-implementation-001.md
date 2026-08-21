# NW-008 AT-8I — GHL REST Live Note Runtime Assembly Implementation 001

```text
UNIT=NW008_AT8I_GHL_REST_LIVE_NOTE_RUNTIME_ASSEMBLY_IMPLEMENTATION_001
PR_CLASS=implementation
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8i-ghl-rest-live-note-runtime-assembly-implementation-authorization-001.md
AUTHORIZATION_PR=114
AUTHORIZATION_REVIEWED_HEAD=58322a50f8339c8de00c64fdfb51942a8e460e85
AUTHORIZATION_MERGE_SHA=673a06a9a069a357d6acc5263c54e802b3b75539
AUTHORIZATION_BLOB_SHA=86ca56f3f9bb35e9f3a9292628e653a0b0241d61
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT

LIVE_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
REAL_SECRET_READS=0
SECRET_PAYLOAD_READS=0
REAL_CREDENTIAL_USE=NO
TOKEN_VALUE_EXPOSURE=NO
```

## Scope

This unit implements the two missing offline runtime assembly components
authorized by merged PR #114:

1. concrete `LiveNoteHttpClient` adapter
2. injectable credential provider / Secret Manager accessor seam

Frozen protocol and value contracts remain in
`src/integrations/ghl/highlevel_rest/live_note_transport.py` and are not
modified.

## HTTP client

Path:

```text
src/integrations/ghl/highlevel_rest/live_note_http_client.py
```

Contract:

```text
ConcreteLiveNoteHttpClient.request(
  method, url, headers, body, timeout_seconds, allow_redirects
) -> LiveNoteHttpResult
```

Behavior:

- Implements the existing `LiveNoteHttpClient` protocol.
- Default timeout equals frozen `REQUEST_TIMEOUT_SECONDS` (`10.0`).
- Timeout is always explicit on each request.
- Session/client is injectable for deterministic tests.
- Dormant concrete path uses Python stdlib HTTP only (`urllib`).
- Exactly one request attempt; no hidden retry.
- `allow_redirects` must be `False`; redirects are not followed.
- No alternate route, generic REST fallback, or target authority.
- Authorization header values and tokens are never logged.
- Diagnostic history stores header names only.

## Credential provider

Path:

```text
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
```

Contract:

```text
LiveNoteCredentialProvider.get_credential() -> InjectedLiveNoteCredential
```

Behavior:

- Injectable `LiveNoteSecretAccessor` interface.
- Synthetic accessor for offline tests.
- Returns frozen `InjectedLiveNoteCredential`.
- No concrete Google Secret Manager network client.
- No `google-cloud-secretmanager` dependency.
- No gcloud subprocess or shell secret access.
- No environment token discovery.
- Token values are redacted from `repr` / `str`.

## Non-authority

```text
AT8I_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8I_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8I_AUTHORIZES_LIVE_NOTE_READ=NO
AT8I_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8I_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8I_AUTHORIZES_SECRET_PAYLOAD_READ=NO
AT8I_AUTHORIZES_IAM_CHANGE=NO
AT8I_AUTHORIZES_DEPLOYMENT_CHANGE=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO
```

## Frozen invariants preserved

```text
PR107_PRIVATE_AT8_CAPABILITY_BOUNDARY=UNCHANGED
AT8G_DURABLE_RESERVATION_SEMANTICS=UNCHANGED
AT8H_POST_GET_CAPS=UNCHANGED
AMBIGUITY_TRUTH=UNKNOWN
AMBIGUOUS_POST_RETRY=FORBIDDEN
CALLER_TARGET_OVERRIDE=FORBIDDEN
```

Next governed step after this implementation PR is independent review and
merge, then a new execution-boundary reinspection. Live mutation requires a
later separate one-shot grant.
