# NW-008 AT-8K — GHL REST Live Note Runtime Construction Path Design 001

```text
UNIT=NW008_AT8K_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_DESIGN_001
PR_CLASS=planning_only
PHASE=PLANNING_ONLY
MODE=READ_ONLY_INSPECTION_AND_PLANNING
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PLAN_BRANCH=nw008-at8k-ghl-rest-live-note-runtime-construction-path-design-001
PLAN_BASE_REF=origin/main
PLAN_BASE_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PR115_MERGE_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PR115_MERGE_VERIFIED=YES

SOURCE_EVIDENCE=docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md
SOURCE_AT8J_UNIT=NW008_AT8J_POST_AT8I_EXECUTION_BOUNDARY_REINSPECTION_001
AT8J_EVIDENCE_AVAILABLE=YES
AT8J_ON_ORIGIN_MAIN=NO
AT8J_WORKTREE_AVAILABLE=YES

PLANNING_ONLY=YES
IMPLEMENTATION_CHANGE=NO
RUNTIME_CHANGE=NO
TEST_CHANGE=NO
CONTRACT_CHANGE=NO
PACKAGE_MANIFEST_CHANGE=NO
AUTHORIZATION_ARTIFACT_CREATED=NO
LIVE_MUTATION_AUTHORIZATION_CREATED=NO
PR114_AUTHORIZATION_REUSED=NO
AT8I_AUTHORIZATION_REUSED=NO

REAL_NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
REAL_SECRET_READS=0
CRM_MUTATIONS=0
IAM_CHANGE=NO
DEPLOYMENT_CHANGE=NO
TOKEN_VALUE_EXPOSURE=NO
```

## Pre-flight

```text
PREFLIGHT_PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH_AT_START=nw008-at8j-post-at8i-execution-boundary-reinspection-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_HEAD_SHA=1ac8c4df3de9fd361d264a71fe12e21f505b2f71
PREFLIGHT_HEAD_EQUALS_PR115_MERGE=YES
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO
PREFLIGHT_AT8J_EVIDENCE_AVAILABLE=YES
PREFLIGHT_ARTIFACT_BRANCH=nw008-at8k-ghl-rest-live-note-runtime-construction-path-design-001
PREFLIGHT_ARTIFACT_BRANCH_BASE=origin/main
```

Abort conditions did not fire: the artifact branch is not `main`; the only
pre-existing worktree file was the AT8J source-evidence artifact; AT8J evidence
was readable from
`docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md`.

This unit does not consume, reuse, or extend PR114 / AT8I authority. AT8I
implementation authority remains one-shot and consumed.

## Non-actions

```text
SRC_MUTATIONS=0
TEST_MUTATIONS=0
CONTRACT_MUTATIONS=0
PACKAGE_MANIFEST_MUTATIONS=0
INIT_PY_MUTATIONS=0
LIVE_NOTE_TRANSPORT_MUTATIONS=0
HTTP_REQUESTS=0
HIGHLEVEL_INVOCATIONS=0
SECRET_MANAGER_INVOCATIONS=0
REAL_SECRET_PAYLOAD_READS=0
TOKEN_VALUES_PRINTED=NO
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENTS=0
LIVE_MUTATION_AUTHORIZATION_CREATED=NO
```

Inspected runtime targets (read-only):

- `src/integrations/ghl/highlevel_rest/live_note_http_client.py`
- `src/integrations/ghl/highlevel_rest/live_note_credential_provider.py`
- `src/integrations/ghl/highlevel_rest/live_note_transport.py`
- `src/integrations/ghl/highlevel_rest/note_path.py`
- `src/integrations/ghl/highlevel_rest/__init__.py`

Durable evidence (read-only):

- `docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md`
- `docs/nw008/nw-008-at8i-ghl-rest-live-note-runtime-assembly-implementation-001.md`
- `docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md`
- `proof/nw008/nw-008-at1-ghl-credential-location-diagnostic-result-005.md`
- `proof/nw008/nw-008-at1-write-credential-readiness.md`
- `proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md`

## Design question 1 — composition root

AT8J re-derived that the concrete HTTP client, credential-provider seam, bounded
transport, and NOTE_PATH private binding all exist, but no production assembler
connects them. This unit designs exactly one future construction path.

### Designed construction sequence

```text
verified private AT8 contact binding
  -> ConcreteLiveNoteHttpClient
  -> LiveNoteCredentialProvider
  -> InjectedLiveNoteCredential
  -> BoundedLiveNoteTransport
  -> NotePathAdapter
```

Exactly one composition root is designed. No second factory, no caller-owned
partial wiring, and no agent/orchestration constructor of these types is
designed.

```text
RUNTIME_COMPOSITION_ROOT_DESIGNED=YES
COMPOSITION_ROOT_PROPOSED_PATH=src/integrations/ghl/highlevel_rest/live_note_runtime.py
COMPOSITION_ROOT_PROPOSED_SYMBOL=assemble_bound_live_note_runtime
CALLER_SUPPLIED_CONTACT_OVERRIDE=NO
CALLER_SUPPLIED_HTTP_CLIENT_TARGET=NO
CALLER_SUPPLIED_CREDENTIAL=NO

PRIVATE_TARGET_BINDING_RUNTIME_PATH_IDENTIFIED=YES
CALLER_TARGET_OVERRIDE_IMPOSSIBLE=YES
```

### Proposed symbol contract (design only; not implemented)

```text
assemble_bound_live_note_runtime(
  *,
  verified_capability: trusted _VerifiedContactBindingCapability,
  execution_store: At1ExecutionStore | None = None,
) -> NotePathAdapter
```

Normative construction order inside the symbol:

1. Reject any argument that is not a process-issued
   `_VerifiedContactBindingCapability`. Raw `contact_id` / `location_id`
   strings, private-binding dataclasses, and AT8 provenance strings alone
   cannot assemble.
2. Copy `contact_id` and `location_id` from the capability. The caller cannot
   override either identifier.
3. Construct `ConcreteLiveNoteHttpClient()` internally. Default session is
   `StdlibLiveNoteHttpSession`. No caller URL, base-URL, host, route, or
   HighLevel target is accepted. Frozen transport `BASE_URL` remains
   `https://services.leadconnectorhq.com`.
4. Construct `LiveNoteCredentialProvider(accessor=<root-owned accessor>,
   resource_name=<root-owned sealed REST resource identity>)`. The caller
   cannot supply `resource_name`, a bearer token, or an
   `InjectedLiveNoteCredential`.
5. Call `LiveNoteCredentialProvider.get_credential()` exactly once.
6. Construct `BoundedLiveNoteTransport(bound_contact_id=capability.contact_id,
   credential=<provider credential>, http_client=<root-owned client>)`.
7. Construct `NotePathAdapter(location_id=capability.location_id,
   contact_id=capability.contact_id, transport=<bounded transport>,
   consumer_authorization_identity=capability.consumer_authorization_identity,
   consumer_workflow_run_id=capability.consumer_workflow_run_id,
   execution_store=execution_store)`.
8. Return the adapter. Do not return the credential, token, HTTP client, or
   accessor.

### Forbidden caller supplies

```text
FORBIDDEN_ASSEMBLER_ARGS=contact_id,location_id,http_client,base_url,url,host,route,headers,authorization,bearer_token,credential,resource_name,secret_payload
```

`execution_store` is allowed because it is the AT8G reservation backend, not a
target, credential, or HTTP authority.

Offline tests of the future assembler may inject only
`SyntheticLiveNoteSecretAccessor` through a test-only seam owned by the
composition root. That seam is not a caller credential supply and is not a
resource-name override.

### Binding invariants preserved from AT8J

`BoundedLiveNoteTransport` already binds one contact at construction and
rejects any other POST/GET note route. `NotePathAdapter.create_meeting_note`
POSTs only `/contacts/{self._contact_id}/notes`. The assembler copies the same
capability `contact_id` into both objects, so dispatch-time caller override
remains impossible.

`NotePathAdapter` currently types transport as `_FixtureTransport`.
`BoundedLiveNoteTransport.dispatch(method, path, body=None)` already matches
that protocol. The designed path does not require a NOTE_PATH source change to
inject the bounded transport.

### Production fail-closed rule

Until a later read-only verification binds a live-note REST credential
resource, production assembly must fail closed. The root must not fall back to
`GHL_MCP_PRIVATE_TOKEN`, environment discovery, or a caller-supplied resource
name.

## Design question 2 — authorization header

Frozen contract inspected in
`src/integrations/ghl/highlevel_rest/live_note_transport.py`:

```text
BoundedLiveNoteTransport.__init__
  stores self._bearer_token = credential.bearer_token

BoundedLiveNoteTransport._attempt_http
  headers = {
    "Authorization": "******",
    "Version": VERSION_HEADER,   # "v3"
    "Accept": "application/json",
  }
  self._http_client.request(..., headers=headers, allow_redirects=False)
```

`self._bearer_token` is assigned from `InjectedLiveNoteCredential` and is not
written onto the HTTP request. The Authorization header is the literal
redacted placeholder `******`. This unit does not change
`live_note_transport.py`.

### Designed application path

Authorization-header application has exactly one owner: the frozen transport
attempt method. The HTTP client must forward the headers it receives. The
credential provider must not speak HTTP. The composition root must not mutate
headers after transport construction. Callers of `dispatch()` cannot supply
headers.

Designed header construction, to be applied later inside `_attempt_http` only:

```text
Authorization: Bearer <InjectedLiveNoteCredential.bearer_token>
Version: v3
Accept: application/json
```

Bearer prefix is required by the HighLevel REST v3 contract already recorded in
`docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md`. The current
placeholder omits both the token and the `Bearer` scheme.

Logging prohibition remains: `InjectedLiveNoteCredential.__repr__` /
`__str__` redact the token; `ConcreteLiveNoteHttpClient` stores header names
only; transport call history stores redacted route shapes only. Future
transport-touch code must not log header values or token bytes.

```text
AUTHORIZATION_HEADER_APPLICATION_PATH_DESIGNED=YES
AUTHORIZATION_HEADER_OWNER=BoundedLiveNoteTransport._attempt_http
BEARER_TOKEN_SOURCE=InjectedLiveNoteCredential
CALLER_SUPPLIED_AUTHORIZATION_FORBIDDEN=YES
TOKEN_LOGGING_FORBIDDEN=YES
TRANSPORT_TOUCH_IMPLEMENTATION_REQUIRED=YES
```

`TRANSPORT_TOUCH_IMPLEMENTATION_REQUIRED=YES` because the stored bearer token
is not applied on the wire, and AT8H/AT8I left `live_note_transport.py` frozen.
A later one-shot offline implementation grant is required to touch
`_attempt_http`. That grant is not created in this lane.

## Design question 3 — credential identity

AT8J's historical-secret finding is normalized and not upgraded into a REST
note credential binding.

```text
HISTORICAL_GHL_MCP_SECRET_RESOURCE_IDENTIFIED=YES
HISTORICAL_GHL_MCP_SECRET_ID=GHL_MCP_PRIVATE_TOKEN
HISTORICAL_GHL_MCP_SECRET_PROJECT=ai-rolodex-to-crm
HISTORICAL_GHL_MCP_SECRET_SURFACE=GHL_ANTHROPIC_V2_MCP
HISTORICAL_GHL_MCP_SECRET_ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
```

Evidence for the historical MCP identity, not re-resolved and not payload-read:

- `proof/nw008/nw-008-at1-ghl-credential-location-diagnostic-result-005.md`
  (`DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN`)
- `proof/nw008/nw-008-at1-write-credential-readiness.md`
  (`CREDENTIAL_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN`,
  `EXECUTION_SURFACE=GHL_ANTHROPIC_V2_MCP`)

This unit does not infer that `GHL_MCP_PRIVATE_TOKEN` is the correct REST note
credential.

### Live-note REST credential class versus resource

```text
LIVE_NOTE_REST_CREDENTIAL_CLASS_IDENTIFIED=YES
LIVE_NOTE_REST_CREDENTIAL_RESOURCE_IDENTIFIED=YES
LIVE_NOTE_REST_RESOURCE_BINDING_DESIGNED=YES
HISTORICAL_MCP_PIT_REUSABLE_FOR_REST=UNKNOWN

LIVE_NOTE_REST_SECRET_RESOURCE_IDENTIFIED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_CREATED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_ID=MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_RESOURCE_PATH=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_HOST_PROJECT_LOGICAL=ai-rolodex-to-crm
LIVE_NOTE_REST_SECRET_HOST_PROJECT_NUMBER=831270426395
LIVE_NOTE_REST_SECRET_VERSION_PRESENT=YES
LIVE_NOTE_REST_SECRET_VERSION_ENABLED=YES
DEVPOST_SECRET_COPY_REQUIRED=NO
LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN
```

Class identified: a HighLevel REST v3 bearer / Private Integration Token stored
in GCP Secret Manager, with `contacts.write` for POST
`/contacts/{contactId}/notes` and `contacts.readonly` for GET
`/contacts/{contactId}/notes/{noteId}`. Supporting evidence:

- architecture Authorization / `Version: v3` rules in
  `docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md`
- frozen `InjectedLiveNoteCredential.bearer_token` and `VERSION_HEADER=v3`
- AT8 REST live-read proof used API version `v3` and
  `EXPECTED_SCOPE=contacts.readonly`
  (`proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md`)
- offline tests use synthetic resource
  `projects/synthetic-project/secrets/ghl-rest-note-token/versions/latest`,
  which is not `GHL_MCP_PRIVATE_TOKEN`
- operator authority for the dedicated MG Guide REST PIT secret resource
  `MG_GUIDE_PIT_GHL` in host project `ai-rolodex-to-crm`
  (`projects/831270426395/secrets/MG_GUIDE_PIT_GHL`)

Resource identified (resource id / path only; not payload identity): the
dedicated Secret Manager resource `MG_GUIDE_PIT_GHL` is the designed live-note
REST credential host. This is distinct from the historical MCP resource
`GHL_MCP_PRIVATE_TOKEN`. `LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED`
remains `UNKNOWN` because this unit does not access, print, diff, or otherwise
inspect the secret payload, and does not claim payload identity from screenshot
or console UI alone. Historical MCP PIT reusability for REST therefore remains
`UNKNOWN` and is no longer required once the dedicated REST resource is bound.

Known HighLevel private-integration authority normalized into this artifact
(scopes only; no token material):

```text
MG_GUIDE_PRIVATE_INTEGRATION=YES
GHL_LOCATION_ID=XpWabhp6Ez8bXZTP7w3r
CONTACTS_READONLY_SCOPE=YES
CONTACTS_WRITE_SCOPE=YES
SCOPE_EXPANSION_REQUIRED=NO
```

### Designed REST resource binding (mechanism only)

The composition root owns one sealed resource identity and injects it only as
`LiveNoteCredentialProvider.resource_name`.

```text
RESOURCE_NAME_OWNER=assemble_bound_live_note_runtime
RESOURCE_NAME_CALLER_OVERRIDE=FORBIDDEN
RESOURCE_NAME_ENV_DISCOVERY=FORBIDDEN
RESOURCE_NAME_EMBEDDED_HISTORICAL_MCP_ID=FORBIDDEN
RESOURCE_NAME_PAYLOAD_IN_REPO=FORBIDDEN
UNBOUND_PRODUCTION_ASSEMBLY=FAIL_CLOSED
```

The sealed production identity is authored as resource path only:

```text
SEALED_LIVE_NOTE_REST_RESOURCE_NAME=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SEALED_LIVE_NOTE_REST_RESOURCE_ID=MG_GUIDE_PIT_GHL
SEALED_FROM_HISTORICAL_MCP_ID=NO
```

Offline tests may continue to use the existing synthetic
`ghl-rest-note-token` resource name. Production assembly must not embed
`GHL_MCP_PRIVATE_TOKEN`.

### Evidence required to resolve `HISTORICAL_MCP_PIT_REUSABLE_FOR_REST=UNKNOWN`

Historical MCP reusability is no longer on the production binding path because
a distinct REST resource id is now recorded. The historical MCP PIT remains
identified as MCP history only. Optional later evidence (not required for the
`MG_GUIDE_PIT_GHL` binding design):

1. Durable public proof, or a redacted operator attestation, naming which
   resource the AT8 REST v3 `GET /contacts/{id}` live-read actually used.
2. An explicit compatibility statement that the historical MCP PIT is or is not
   the same credential material as `MG_GUIDE_PIT_GHL` (payload comparison is
   forbidden in this lane).

## Design question 4 — secret accessor

The injectable interface already exists:

```text
LiveNoteSecretAccessor.read_secret_payload(resource_name: str) -> str
```

File: `src/integrations/ghl/highlevel_rest/live_note_credential_provider.py`

The only concrete class in merged source is
`SyntheticLiveNoteSecretAccessor` (offline tests). No Google Secret Manager
network client exists. `google-cloud-secretmanager` is not a package
dependency.

### Future concrete accessor boundary (design only; not implemented)

```text
CONCRETE_SECRET_ACCESSOR_INTERFACE_DESIGNED=YES
SECRET_ACCESSOR_PROPOSED_PATH=src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
SECRET_ACCESSOR_PROPOSED_SYMBOL=GoogleSecretManagerLiveNoteSecretAccessor
SECRET_ACCESSOR_IMPLEMENTATION_REQUIRED=YES
SECRET_METADATA_VERIFICATION_REQUIRED_BEFORE_IMPLEMENTATION=YES
```

Proposed concrete class implements `LiveNoteSecretAccessor` only. It is
constructed exclusively by `assemble_bound_live_note_runtime`. Callers cannot
construct it with a resource override, cannot pass a payload, and cannot
receive the payload.

Required invariants:

```text
NO_ENV_TOKEN_DISCOVERY=YES
NO_GCLOUD_SUBPROCESS=YES
NO_SHELL_SECRET_READ=YES
NO_SECRET_VALUE_LOGGING=YES
NO_CALLER_SUPPLIED_RESOURCE_OVERRIDE=YES
SECRET_PAYLOAD_RETURNED_ONLY_TO_CREDENTIAL_PROVIDER=YES
```

The accessor may receive `resource_name` only from
`LiveNoteCredentialProvider.get_credential()`. It returns the payload string
only to that provider, which wraps it as `InjectedLiveNoteCredential`. No
other symbol may read the payload. `repr` / `str` must not include the
payload.

Implementation of this concrete class is forbidden until:

1. REST credential resource identity is resolved
   (`LIVE_NOTE_REST_SECRET_RESOURCE_IDENTIFIED=YES` for `MG_GUIDE_PIT_GHL`);
2. read-only Secret Manager metadata access for that resource is verified
   without reading the payload
   (see `READ_ONLY_CREDENTIAL_RUNTIME_READINESS` section below);
3. a later one-shot implementation grant names this class.

This unit does not add `google-cloud-secretmanager`, implement the concrete
accessor, apply IAM, or create that grant. Metadata-only Secret Manager reads
may be performed for readiness verification; payload access remains forbidden.

## Package export (normalized non-blocking item)

AT8J recorded that live-note types are not exported from
`src/integrations/ghl/highlevel_rest/__init__.py`, which still exports
fixture-only NOTE_PATH symbols.

```text
PACKAGE_EXPORT_CHANGE_REQUIRED=YES
PACKAGE_EXPORT_IS_LIVE_MUTATION_BLOCKER=NO
```

A later offline implementation may export the composition-root symbol. Missing
exports do not block live-mutation authorization design on their own and are
not a reason to reuse PR114 / AT8I.

## Remaining-gap classification

Every remaining gap has exactly one class.

```text
HTTP_CLIENT_LIVE_CONSTRUCTION_WIRING
  CLASS=OFFLINE_IMPLEMENTATION_REQUIRED
  NOTE=ConcreteLiveNoteHttpClient exists; assembler does not.

CREDENTIAL_PROVIDER_LIVE_CONSTRUCTION_WIRING
  CLASS=OFFLINE_IMPLEMENTATION_REQUIRED
  NOTE=LiveNoteCredentialProvider exists; assembler does not call get_credential().

AUTHORIZATION_HEADER_APPLICATION
  CLASS=OFFLINE_IMPLEMENTATION_REQUIRED
  NOTE=Requires transport-touch of BoundedLiveNoteTransport._attempt_http.

COMPOSITION_ROOT_ASSEMBLER
  CLASS=OFFLINE_IMPLEMENTATION_REQUIRED
  NOTE=Designed path src/integrations/ghl/highlevel_rest/live_note_runtime.py
       symbol assemble_bound_live_note_runtime.

LIVE_NOTE_REST_CREDENTIAL_RESOURCE_IDENTITY
  CLASS=RESOLVED
  NOTE=MG_GUIDE_PIT_GHL at projects/831270426395/secrets/MG_GUIDE_PIT_GHL;
       LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN.

SECRET_MANAGER_METADATA_ACCESS_FOR_REST_RESOURCE
  CLASS=READ_ONLY_VERIFICATION_IN_THIS_PHASE
  NOTE=Metadata-only verification for MG_GUIDE_PIT_GHL; payload forbidden.

CONCRETE_GOOGLE_SECRET_MANAGER_LIVE_NOTE_ACCESSOR
  CLASS=OFFLINE_IMPLEMENTATION_REQUIRED
  NOTE=Blocked on metadata verification + later implementation grant;
       not blocked on resource identity.

LIVE_TRANSPORT_EXECUTION
  CLASS=LIVE_AUTHORIZATION_PREREQUISITE
  NOTE=BoundedLiveNoteTransport.LIVE_EXECUTION_AUTHORIZED=False.

LIVE_NOTE_WRITE_AND_READBACK
  CLASS=LIVE_AUTHORIZATION_PREREQUISITE

LIVE_CRM_MUTATION_GRANT
  CLASS=LIVE_AUTHORIZATION_PREREQUISITE
  NOTE=LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO.

PACKAGE_EXPORT_OF_LIVE_NOTE_TYPES
  CLASS=NON_BLOCKING_CLEANUP
```

## Final fields

```text
HTTP_CLIENT_CONSTRUCTION_PATH_DESIGNED=YES
CREDENTIAL_PROVIDER_CONSTRUCTION_PATH_DESIGNED=YES
AUTHORIZATION_HEADER_APPLICATION_PATH_DESIGNED=YES
LIVE_NOTE_REST_CREDENTIAL_RESOURCE_IDENTIFIED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_IDENTIFIED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_CREATED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_ID=MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_RESOURCE_PATH=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_VERSION_PRESENT=YES
LIVE_NOTE_REST_SECRET_VERSION_ENABLED=YES
DEVPOST_SECRET_COPY_REQUIRED=NO
LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN
CONCRETE_SECRET_ACCESSOR_INTERFACE_DESIGNED=YES

NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_MUTATION_PREREQUISITES_COMPLETE=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

`NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES` applies only to a later
offline, one-shot implementation authorization for the designed assembler and
the required `_attempt_http` transport-touch. It does not make live mutation
designable. It does not authorize secret payload access. It does not bind
`GHL_MCP_PRIVATE_TOKEN` as the REST note credential. Production sealed resource
identity is `projects/831270426395/secrets/MG_GUIDE_PIT_GHL`
(`MG_GUIDE_PIT_GHL`) only.

## Next recommended unit

```text
NEXT_RECOMMENDED_UNIT=NW008_AT8L_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_IMPLEMENTATION_AUTHORIZATION_001
NEXT_PR_CLASS=authorization
NEXT_MODE=AUTHORIZATION_ARTIFACT_ONLY
```

AT8L, if later separately authorized, should be a one-shot offline
implementation authorization covering only:

1. new composition root
   `src/integrations/ghl/highlevel_rest/live_note_runtime.py`
   symbol `assemble_bound_live_note_runtime`;
2. transport-touch of `BoundedLiveNoteTransport._attempt_http` so Authorization
   is `Bearer <InjectedLiveNoteCredential.bearer_token>` with token logging
   still forbidden.

AT8L must not authorize, and this unit does not create:

- concrete Google Secret Manager network client implementation;
- production `resource_name` binding outside the sealed
  `projects/831270426395/secrets/MG_GUIDE_PIT_GHL` identity (and must not bind
  `GHL_MCP_PRIVATE_TOKEN`);
- real secret payload reads;
- IAM mutation;
- live transport execution;
- live note write or readback;
- live CRM mutation;
- reuse of PR114 / AT8I authority.

REST credential resource identity is resolved to `MG_GUIDE_PIT_GHL`. Sealing that
identity into production assembly code, implementing the concrete Secret Manager
accessor, and applying runtime secretAccessor IAM remain outside AT8L unless a
later grant explicitly names them. Payload identity verification remains
`UNKNOWN` and is not claimed from UI/screenshot evidence.

This lane's readiness phase stops after AT8K artifact normalization plus
read-only credential-runtime readiness verification. It does not create the AT8L
authorization.

## Non-authority

```text
AT8K_AUTHORIZES_IMPLEMENTATION=NO
AT8K_AUTHORIZES_TRANSPORT_TOUCH=NO
AT8K_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8K_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8K_AUTHORIZES_LIVE_NOTE_READ=NO
AT8K_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8K_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8K_AUTHORIZES_SECRET_PAYLOAD_READ=NO
AT8K_AUTHORIZES_IAM_CHANGE=NO
AT8K_AUTHORIZES_DEPLOYMENT_CHANGE=NO
AT8K_REUSES_PR114_AUTHORIZATION=NO
AT8K_REUSES_AT8I_AUTHORIZATION=NO
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

## Validation

```text
SOURCE_RUNTIME_TEST_CHANGES=NO
EXTERNAL_EFFECTS=0
ARTIFACT_ONLY_DIFF=YES
GIT_DIFF_CHECK=PASS

HIGHLEVEL_CALLS=0
REAL_SECRET_PAYLOAD_READS=0
REAL_SECRET_READS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
```

Planning-only body remains artifact-only. The readiness phase below may perform
GCP Secret Manager **metadata** API calls and local principal discovery. It must
not perform HighLevel calls, secret payload reads, IAM changes, deployments, or
CRM mutations.

## READ_ONLY_CREDENTIAL_RUNTIME_READINESS

```text
PHASE=READ_ONLY_CREDENTIAL_RUNTIME_READINESS
OWNER=VS_CODE_ORCHESTRATOR
READINESS_RECORDED_AT_LOCAL=2026-08-21T08:42:00-04:00
```

### A) Normalized REST secret resource (no payload identity claim)

```text
LIVE_NOTE_REST_SECRET_RESOURCE_IDENTIFIED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_CREATED=YES
LIVE_NOTE_REST_SECRET_RESOURCE_ID=MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_RESOURCE_PATH=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
LIVE_NOTE_REST_SECRET_HOST_PROJECT_LOGICAL=ai-rolodex-to-crm
LIVE_NOTE_REST_SECRET_HOST_PROJECT_NUMBER=831270426395
LIVE_NOTE_REST_SECRET_VERSION_PRESENT=YES
LIVE_NOTE_REST_SECRET_VERSION_ENABLED=YES
DEVPOST_SECRET_COPY_REQUIRED=NO
LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN
```

`LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN` is intentional: this
lane does not access, print, echo, diff, log, or otherwise expose the secret
payload, and does not claim payload identity from screenshot/console UI alone.

### B) Read-only metadata verification attempt (no payload)

Attempted with Application Default Credentials only after interactive
`gcloud` user auth for `themg@themiliare-group.com` failed reauthentication in
non-interactive mode. Commands used metadata endpoints only
(`secrets.get` / `versions.list` / `getIamPolicy` / project describe). No
`versions.access`, no `gcloud secrets versions access`, no payload decode.

```text
METADATA_PROBE_PRINCIPAL=buildweek-evaluator@themiliare-group.com
METADATA_PROBE_AUTH_MODE=APPLICATION_DEFAULT_CREDENTIALS
ACTIVE_GCLOUD_USER_ACCOUNT=themg@themiliare-group.com
ACTIVE_GCLOUD_USER_REAUTH_REQUIRED=YES

SECRET_METADATA_ACCESS_VERIFIED=NO
SECRET_RESOURCE_MATCH_VERIFIED=NO
SECRET_VERSION_1_ENABLED=UNKNOWN

SECRET_GET_HTTP=403
SECRET_VERSIONS_LIST_HTTP=403
SECRET_GET_IAM_POLICY_HTTP=403
PROJECT_DESCRIBE_HTTP=403

SECRET_METADATA_DENIAL_CLASS=IAM_PERMISSION_DENIED
SECRET_METADATA_DENIED_PERMISSIONS=secretmanager.secrets.get,secretmanager.versions.list,secretmanager.secrets.getIamPolicy
ENABLED_VERSION_COUNT_OBSERVED=NOT_OBSERVABLE_THIS_LANE
CURRENT_IAM_POLICY_OBSERVED=NOT_OBSERVABLE_THIS_LANE

OPERATOR_ATTESTED_SECRET_RESOURCE_PATH=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
OPERATOR_ATTESTED_SECRET_VERSION_1_EXISTS=YES
OPERATOR_ATTESTED_SECRET_VERSION_1_ENABLED=YES
OPERATOR_ATTESTATION_ACCEPTED_AS_API_VERIFICATION=NO

REAL_SECRET_PAYLOAD_READS=0
TOKEN_VALUE_EXPOSURE=NO
```

Interpretation: the dedicated REST resource identity is **normalized from
operator authority** into this artifact, but **independent API metadata
verification did not succeed** under the available non-interactive principal.
A later operator-auth metadata lane (after `gcloud auth login` for a principal
with `secretmanager.secrets.get`, `secretmanager.versions.list`, and
`secretmanager.secrets.getIamPolicy` on this single secret) is required before
claiming `SECRET_METADATA_ACCESS_VERIFIED=YES`.

### C) Runtime principal discovery for `assemble_bound_live_note_runtime`

`assemble_bound_live_note_runtime` is the designed composition root (not yet
implemented). NW-008 live-note work is owned by `VS_CODE_ORCHESTRATOR` and is
not the NW-007 Cloud Run judge surface.

```text
RUNTIME_PLATFORM=VS_CODE_ORCHESTRATOR_LOCAL
RUNTIME_PROJECT=ai-rolodex-to-crm
RUNTIME_SERVICE_ACCOUNT=UNKNOWN

RUNTIME_COMPOSITION_ROOT_SYMBOL=assemble_bound_live_note_runtime
RUNTIME_COMPOSITION_ROOT_IMPLEMENTED=NO
RUNTIME_DEDICATED_SERVICE_ACCOUNT_BOUND=NO
```

Candidate principals observed this lane (not granted; not selected as final):

```text
CANDIDATE_PRINCIPAL_1=user:themg@themiliare-group.com
CANDIDATE_PRINCIPAL_1_CLASS=OPERATOR_USER_GCLOUD
CANDIDATE_PRINCIPAL_1_STATUS=REAUTH_REQUIRED_NON_INTERACTIVE
CANDIDATE_PRINCIPAL_1_SECRET_METADATA_OBSERVED=NOT_TESTABLE_THIS_LANE

CANDIDATE_PRINCIPAL_2=user:buildweek-evaluator@themiliare-group.com
CANDIDATE_PRINCIPAL_2_CLASS=LOCAL_ADC_USER
CANDIDATE_PRINCIPAL_2_STATUS=AUTH_OK_SECRET_METADATA_PERMISSION_DENIED
CANDIDATE_PRINCIPAL_2_SECRET_METADATA_OBSERVED=403

CANDIDATE_PRINCIPAL_3=serviceAccount:mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
CANDIDATE_PRINCIPAL_3_CLASS=NW007_CLOUD_RUN_JUDGE_RUNTIME
CANDIDATE_PRINCIPAL_3_STATUS=NOT_SELECTED_FOR_LIVE_NOTE_REST
CANDIDATE_PRINCIPAL_3_REASON=Different project (mg-devpost); judge/demo surface only; DEVPOST_SECRET_COPY_REQUIRED=NO
```

Final exact identity that will eventually execute
`assemble_bound_live_note_runtime` remains `RUNTIME_SERVICE_ACCOUNT=UNKNOWN`
until a later authorization names either a dedicated runtime service account in
`ai-rolodex-to-crm` or an explicit operator-user execution principal.

### D) IAM design only (not applied)

Designed binding for the eventual runtime principal once known:

```text
SECRET_ACCESS_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
SECRET_ACCESS_ROLE=roles/secretmanager.secretAccessor
SECRET_ACCESS_MEMBER=<RUNTIME_PRINCIPAL_TBD>
IAM_SCOPE=SINGLE_SECRET_ONLY
PROJECT_WIDE_SECRET_ACCESSOR=NO
DEVPOST_SECRET_DUPLICATION=NO
IAM_CHANGE_APPLIED=NO
IAM_CHANGES=0
```

Designed (not executed) command shape for a later authorized IAM lane:

```text
gcloud secrets add-iam-policy-binding MG_GUIDE_PIT_GHL \
  --project=831270426395 \
  --member=<RUNTIME_PRINCIPAL_TBD> \
  --role=roles/secretmanager.secretAccessor \
  --condition=None
```

Do not grant `roles/secretmanager.secretAccessor` project-wide. Do not copy the
secret into `mg-devpost`. Do not grant payload access to the NW-007 judge SA
unless a later explicit grant says otherwise (current design: no).

Optional later metadata-read roles for an operator verification principal
(design only; not applied):

```text
METADATA_VERIFY_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL
METADATA_VERIFY_ROLES_OR_PERMS=secretmanager.secrets.get,secretmanager.versions.list,secretmanager.secrets.getIamPolicy
METADATA_VERIFY_IAM_APPLIED=NO
```

### E) Durability check

```text
AT8J_PATH=docs/nw008/nw-008-at8j-post-at8i-execution-boundary-reinspection-001.md
AT8K_PATH=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
AT8J_WORKTREE_PRESENT=YES
AT8K_WORKTREE_PRESENT=YES
AT8J_ON_ORIGIN_MAIN=NO
AT8K_ON_ORIGIN_MAIN=NO
AT8J_GIT_TRACKED_AT_READINESS_START=NO
AT8K_GIT_TRACKED_AT_READINESS_START=NO
```

Durability disposition is recorded after the readiness commit of these two
planning artifacts on branch
`nw008-at8k-ghl-rest-live-note-runtime-construction-path-design-001`:

```text
AT8J_DURABLY_PRESERVED=YES
AT8K_DURABLY_PRESERVED=YES
DURABILITY_MECHANISM=TOPIC_BRANCH_COMMIT_ARTIFACT_ONLY
```

### F) Authorization designability gate

```text
NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES
LIVE_MUTATION_AUTHORIZATION_DESIGNABLE=NO
```

`NEXT_IMPLEMENTATION_AUTHORIZATION_DESIGNABLE=YES` remains limited to a later
offline one-shot implementation authorization for the designed assembler and
`_attempt_http` transport-touch. It does **not** authorize:

- secret payload reads;
- IAM mutation;
- concrete GSM accessor implementation unless that later grant explicitly names it;
- live HighLevel execution;
- live CRM mutation.

Because `SECRET_METADATA_ACCESS_VERIFIED=NO` and
`RUNTIME_SERVICE_ACCOUNT=UNKNOWN`, any later grant that would implement
production secret access or apply IAM must first close those readiness gaps in a
separate authorized lane.

### G) Zero-effect assertions (this readiness phase)

```text
HIGHLEVEL_CALLS=0
REAL_SECRET_PAYLOAD_READS=0
CRM_MUTATIONS=0
IAM_CHANGES=0
DEPLOYMENT_CHANGES=0
SRC_MUTATIONS=0
TEST_MUTATIONS=0
TOKEN_VALUE_EXPOSURE=NO
GCP_SECRET_METADATA_PROBES=YES
GCP_SECRET_PAYLOAD_PROBES=NO
```

`REAL_NETWORK_CALLS` for HighLevel/CRM = 0. GCP metadata control-plane probes
were attempted and returned permission denials only; no secret payload bytes
were retrieved.

STOP before:

- secret payload access
- IAM mutation
- source implementation
- live HighLevel execution
- live CRM mutation
