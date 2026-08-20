# NW-008 AT-2 — HighLevel REST NOTE_PATH Offline Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT2_GHL_REST_NOTE_PATH_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_BRANCH=governance/nw008-at2-note-path-implementation-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md

SOURCE_PR=93
SOURCE_PR_HEAD=554854e0d957d514600107084ed6e8dcf3e43cb8
SOURCE_MERGE_SHA=831cddb6f5ef5b3389b399948315e9b6c74e1fbc
BASE_REF=origin/main
BASE_SHA=831cddb6f5ef5b3389b399948315e9b6c74e1fbc

ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
MODE=AUTHORIZATION_PLANNING_ONLY

GRANT=NOTE_PATH_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does not implement the adapter, open a network socket, load a credential,
touch HighLevel, or produce live CRM effects.

### Conditional grant semantics

```text
GRANT=NOTE_PATH_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the
artifact defines a bounded offline `NOTE_PATH` implementation permission that
becomes usable only when both of the following are true:

1. the exact authorization artifact path is present on `main` via human review
   and merge; and
2. the authorized consumer unit
   `NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001` verifies that merge
   (exact path on `origin/main` / merge ancestry) before writing code.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is not runtime execution authority, not live-read authority, not
live-mutation authority, and not a reusable standing grant.

```text
IMPLEMENTATION_SLICE=NOTE_PATH
IMPLEMENTATION_MODE=OFFLINE_ONLY
GRANT_PERMITS_WHEN_EFFECTIVE=NOTE_PATH_OFFLINE_IMPLEMENTATION_ONLY

NOTE_PATH_ARCHITECTURE_READY=YES
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO

NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CREDENTIAL_USE_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REST_ADAPTER_LIVE_EXECUTION_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0
```

## 2. Verified prerequisites and source authority

Preflight was run before this artifact was authored:

```text
pwd
/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git fetch origin
git branch --show-current
governance/nw008-at2-note-path-implementation-authorization-001

git rev-parse HEAD
831cddb6f5ef5b3389b399948315e9b6c74e1fbc

Working branch is not main
YES

origin/main contains SOURCE_MERGE_SHA
831cddb6f5ef5b3389b399948315e9b6c74e1fbc
YES

SOURCE_PR_HEAD is ancestor of origin/main
554854e0d957d514600107084ed6e8dcf3e43cb8
YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #93 reviewed head | `554854e0d957d514600107084ed6e8dcf3e43cb8` |
| PR #93 merge commit | `831cddb6f5ef5b3389b399948315e9b6c74e1fbc` |
| PR #93 merge commit is reachable from `origin/main` | YES |
| Architecture artifact present on base | YES |
| Contract artifact present on base | YES |
| `NOTE_PATH_ARCHITECTURE_READY` on source artifacts | YES |
| `STAGE_PATH_ARCHITECTURE_READY` on source artifacts | NO |
| Source architecture `IMPLEMENTATION_AUTHORIZED` | NO |
| Source architecture live read/mutation/execution | NO |

Bound durable source inputs (read-only for the future implementation lane):

```text
ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml
SOURCE_PR=93
SOURCE_PR_HEAD=554854e0d957d514600107084ed6e8dcf3e43cb8
SOURCE_MERGE_SHA=831cddb6f5ef5b3389b399948315e9b6c74e1fbc
```

The future implementation lane must consume those artifacts as frozen authority
for route allowlisting, domain API shape, note contract, digests, fail-closed
matrix, and path readiness. It may not reinterpret stage-path readiness, expand
provider operations, or treat this authorization as live CRM authority.

## 3. What this authorization permits

### 3.1 Implementation slice

```text
IMPLEMENTATION_SLICE=NOTE_PATH
IMPLEMENTATION_MODE=OFFLINE_ONLY
TRANSPORT_REQUIREMENT=DETERMINISTIC_LOCAL_FAKE_ONLY
GRANT=NOTE_PATH_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
GRANT_PERMITS_WHEN_EFFECTIVE=NOTE_PATH_OFFLINE_IMPLEMENTATION_ONLY
AUTHORIZED_CONSUMER_UNIT=NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
```

Authorized domain API surface only:

```text
get_bound_contact
create_meeting_note
verify_meeting_note
```

Authorized provider route abstractions only (rendered against the fake
transport; never against a live origin):

```text
GET  /contacts/{contactId}
POST /contacts/{contactId}/notes
GET  /contacts/{contactId}/notes/{noteId}
```

All provider interactions in implementation and tests MUST use a deterministic
local fake transport that records fully rendered requests and returns fixture-
controlled responses. No real HTTPS client, DNS resolution to HighLevel, token
exchange, or credential provider call is authorized.

### 3.2 In-scope offline work

When the conditional grant is effective, only
`NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001` may, within the
writable paths in §5 only:

1. Implement a bounded HighLevel REST `NOTE_PATH` adapter exposing only the
   three domain methods above.
2. Implement note-contract validation and serialization consistent with the
   architecture and contract artifacts (body-only provider payload; logical
   title as first line of body; denied provider fields rejected).
3. Implement private-binding injection stubs or test doubles for note-path
   symbols only (`location_id`, `contact_id`), with synthetic fixture values
   only. Real private IDs, secrets, and production bindings must not be
   introduced into the public tree.
4. Implement exact-ID contact preflight, one-note create budget, same-run note
   ID capture, exact-ID note readback, strict readback parser, and note-content
   digest verification against the fake transport.
5. Implement a deterministic local fake transport and synthetic fixtures
   sufficient for the required tests in §7.
6. Add unit and contract tests that prove allowlist, fail-closed, budget,
   parser, digest, and zero-network / zero-external-effect properties.
7. Optionally re-export the new package symbols from package `__init__` files
   only inside the authorized path prefixes.

### 3.3 Explicit non-goals for the implementation lane

The implementation lane authorized by this artifact must not:

- call HighLevel or any external network endpoint;
- load, read, write, or reference live credentials, tokens, API keys, OAuth
  material, Secret Manager values, or `.env` secrets;
- implement or enable `STAGE_PATH`;
- implement or expose generic provider surfaces;
- modify workflow orchestration, agents, Apps Script, deploy, IAM, infra,
  competition/Devpost assets, or live transport executors outside the
  authorized prefixes;
- treat offline green tests as live-execution authority;
- reuse this authorization as a later live-read, live-mutation, or runtime
  grant.

## 4. Explicit denials

### 4.1 Live and network authority

```text
NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CREDENTIAL_USE_AUTHORIZED=NO
SECRET_ACCESS_AUTHORIZED=NO
IAM_CHANGE_AUTHORIZED=NO
DEPLOYMENT_CHANGE_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REST_ADAPTER_LIVE_EXECUTION_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0
```

Any code path that would perform real network I/O, credential use, or external
effects is out of scope and must fail closed or be absent.

### 4.2 STAGE_PATH

```text
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO
STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

Forbidden domain methods under this authorization:

```text
get_bound_opportunity
advance_authorized_stage
verify_authorized_stage
```

Forbidden provider routes under this authorization:

```text
GET /opportunities/{opportunityId}
PUT /opportunities/{opportunityId}
```

Stage-path modules, fixtures, route tables, runtime flags, and tests that would
activate stage routes are not authorized. Note-path code must not register or
enable stage routes “for later.”

### 4.3 Generic and expansive surfaces

Forbidden API / surface names and behaviors include, without limitation:

```text
request
execute
raw_http
search
list
pagination
generic provider payload
arbitrary URL
arbitrary method
batch
tools/call passthrough
MCP execute_operation expansion
caller-supplied contactId / opportunityId / headers / query / provider body
```

The adapter must not expose an HTTP client, generic execute/request API, search
API, list API, pagination API, or provider payload passthrough through its
domain interface.

### 4.4 Out-of-scope repository surfaces

The future implementation lane is forbidden from writing:

- Apps Script / `workspace_addon/**` implementation beyond any path not listed
  in §5 (all addon paths are denied);
- deploy, Dockerfile runtime promotion, Cloud Build, Cloud Run, IAM, secrets;
- credential or private-ID materialization into the public tree;
- workflow / agent / orchestration behavior changes;
- competition / Devpost assets;
- existing MCP live transport, bounded executor, or offline MCP read-adapter
  modules except by non-use (no edits authorized there);
- architecture or contract reinterpretation that expands authority.

## 5. Writable paths

### 5.1 This authorization PR (current unit)

This authorization-planning unit may write exactly one path:

```text
governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md
```

No adapter code, tests, fixtures, contracts, workflows, or deploy assets may be
created or modified in this unit.

### 5.2 Future NOTE_PATH offline implementation lane (AT3 only)

After the conditional grant is effective (exact artifact merged to `main` and
verified by the consumer), only
`NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001` may write only the
following repo-local conventional prefixes. Paths were resolved against the
existing integration layout (`src/integrations/ghl`, `tests/integrations/ghl`,
`fixtures/ghl`) and isolated under a dedicated HighLevel REST NOTE_PATH
package so MCP live/offline modules remain untouched.

```text
WRITABLE_IMPLEMENTATION_PATHS=

src/integrations/ghl/highlevel_rest/
src/integrations/ghl/highlevel_rest/**

tests/integrations/ghl/highlevel_rest/
tests/integrations/ghl/highlevel_rest/**

fixtures/ghl/highlevel_rest/
fixtures/ghl/highlevel_rest/**

IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
```

AT3 must return an exact implementation file manifest of every created or
modified path. Every manifest entry must remain under one of:

```text
src/integrations/ghl/highlevel_rest/**
tests/integrations/ghl/highlevel_rest/**
fixtures/ghl/highlevel_rest/**
```

Intended minimum contents (names may vary inside the prefixes; scope may not):

| Concern | Authorized location prefix |
| --- | --- |
| Bounded note adapter / domain API | `src/integrations/ghl/highlevel_rest/` |
| Note contract + serialization + digests + strict parser | `src/integrations/ghl/highlevel_rest/` |
| Deterministic local fake transport | `src/integrations/ghl/highlevel_rest/` |
| Synthetic private-binding test doubles (fixture IDs only) | `src/integrations/ghl/highlevel_rest/` and/or `fixtures/ghl/highlevel_rest/` |
| NOTE_PATH unit/contract tests | `tests/integrations/ghl/highlevel_rest/` |
| Deterministic request/response fixtures | `fixtures/ghl/highlevel_rest/` |

### 5.3 Explicitly non-writable for the implementation lane

```text
NON_WRITABLE_EXAMPLES=
src/integrations/ghl/read_adapter.py
src/integrations/ghl/bounded_at1_executor.py
src/integrations/ghl/at1_live_transport_adapter.py
src/integrations/ghl/at1_live_transport_serializer.py
src/integrations/ghl/at1_execution_store.py
src/integrations/ghl/__init__.py
src/agents/**
src/orchestration/**
src/mg_guide/**
workspace_addon/**
scripts/**
deploy/**
.github/**
docs/nw008/**
contracts/**
governance/**   # except that this authorization artifact is already the auth-PR scope
proof/**
competition/**
local/**
Dockerfile
requirements.txt
pyproject.toml
.env
.env.*
**/*secret*
**/*credential*
```

Contract and architecture artifacts are read-only inputs. Any contract gap that
blocks offline NOTE_PATH implementation must stop and return for a separate
planning/contract revision; it must not be “fixed” by silent scope expansion
under this authorization.

### 5.4 Path assertions

```text
WRITABLE_PATH_COUNT_PREFIXES=3
WRITABLE_PATH_PREFIX_1=src/integrations/ghl/highlevel_rest/
WRITABLE_PATH_PREFIX_2=tests/integrations/ghl/highlevel_rest/
WRITABLE_PATH_PREFIX_3=fixtures/ghl/highlevel_rest/
IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
STAGE_PATH_WRITABLE=NO
APPS_SCRIPT_WRITABLE=NO
DEPLOY_INFRA_WRITABLE=NO
SECRETS_CREDENTIALS_WRITABLE=NO
WORKFLOW_WRITABLE=NO
CONTRACT_WRITABLE=NO
ARCHITECTURE_WRITABLE=NO
```

## 6. Transport, binding, and safety rules for implementation

```text
FAKE_TRANSPORT_REQUIRED=YES
REAL_HTTP_CLIENT_AUTHORIZED=NO
PROVIDER_ORIGIN_LIVE_CALLS=NO
REDIRECT_FOLLOWING=NO
QUERY_PARAMETERS=NO
CALLER_SUPPLIED_PROVIDER_BODY=NO
CALLER_SUPPLIED_IDS=NO
PRIVATE_BINDING_PUBLICATION=NO
SYNTHETIC_FIXTURE_IDS_ONLY=YES
FULL_PROVIDER_RESPONSE_LOG_OR_PERSIST=FORBIDDEN
```

Binding rules for NOTE_PATH only:

```text
NOTE_PATH_PRIVATE_BINDING_SYMBOLS=location_id,contact_id
CONTACT_ID_SOURCE=private_binding_or_test_double_only
NOTE_ID_SOURCE=same_run_create_note_response_only
LOCATION_ID_MUST_MATCH_BINDING=YES
CONTACT_ID_MUST_MATCH_BINDING=YES
```

Provider body rules for create-note:

```text
CREATE_NOTE_PROVIDER_FIELDS_ALLOWED=body
CREATE_NOTE_PROVIDER_FIELDS_DENIED=userId,title,color,pinned
NOTE_BODY_ONLY_PAYLOAD=YES
```

Mutation budget:

```text
NOTE_POST_BUDGET_PER_RUN=1
AMBIGUOUS_POST_RETRY=NO
STAGE_PUT_BUDGET_UNDER_THIS_AUTH=0
```

## 7. Required future tests

The offline implementation lane must include deterministic tests that prove at
least the following named cases. All tests must run with fake transport only and
assert zero network calls and zero external effects.

```text
exact_contact_binding_pass
contact_binding_mismatch_block
location_binding_mismatch_block
missing_contact_binding_block
missing_location_binding_block
caller_supplied_contact_id_block
caller_supplied_location_id_block
raw_transcript_rejected
non_synthetic_source_rejected
note_body_only_payload
denied_provider_fields_rejected
same_run_note_id_required
note_contact_binding_required
strict_parser_pass
strict_parser_unknown_label_block
strict_parser_duplicate_label_block
note_content_digest_pass
note_content_digest_mismatch_block
one_note_write_budget
ambiguous_post_no_retry
search_api_absent
list_api_absent
generic_execute_absent
stage_routes_absent
real_http_client_imports_absent
socket_use_absent
dns_resolution_absent
env_credential_lookup_absent
network_calls_zero
external_effects_zero
```

Additional architecture-aligned checks are encouraged when they remain inside
the authorized paths and offline mode (for example missing capability block,
query rejection, redirect rejection, unexpected schema fail-closed). They do
not expand live authority.

Required proof posture for the implementation lane return:

```text
NETWORK_CALLS=0
EXTERNAL_EFFECTS=0
HIGHLEVEL_NETWORK_CALLS=0
CREDENTIAL_USE=0
REAL_HTTP_CLIENT_IMPORTS_ABSENT=YES
SOCKET_USE_ABSENT=YES
DNS_RESOLUTION_ABSENT=YES
ENV_CREDENTIAL_LOOKUP_ABSENT=YES
STAGE_ROUTES_PRESENT=NO
GENERIC_EXECUTE_PRESENT=NO
SEARCH_API_PRESENT=NO
LIST_API_PRESENT=NO
IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
IMPLEMENTATION_FILE_MANIFEST_WITHIN_WRITABLE_PREFIXES=YES
```

## 8. Authorization consumption rules

```text
AUTHORIZED_CONSUMER_UNIT=NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
ONE_SHOT_SCOPE=NOTE_PATH_OFFLINE_IMPLEMENTATION
REUSE_AS_LIVE_EXECUTION_AUTHORITY=NO
REUSE_AS_RUNTIME_AUTHORITY=NO
REUSE_AS_STAGE_PATH_AUTHORITY=NO
REUSE_AS_CREDENTIAL_AUTHORITY=NO
STANDING_GRANT=NO
```

### 8.1 Named consumer binding

Only unit `NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001` with
`AUTHORIZED_CONSUMER_PR_CLASS=implementation` may consume this grant. No other
unit, agent session, PR class, or follow-on lane may inherit it.

### 8.2 Activation and verification

1. Before merge: `AUTHORIZATION_EFFECTIVE=NO` and `GRANT_STATUS=CONDITIONAL`.
2. Activation condition: the exact authorization artifact is merged to `main`
   by human authority (`GRANT_ACTIVATION=MERGE_TO_MAIN`).
3. AT3 must verify that merge (exact path present on `origin/main` and
   ancestry/merge evidence) before any implementation write.
4. The artifact text is not required to mutate after merge
   (`ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO`).

### 8.3 One-shot, non-reuse, and expiry

`AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT`. The grant is not reusable and not
transferable:

```text
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

The authorization expires when any of the following occurs:

- the authorized AT3 implementation PR is merged; or
- the authorization is explicitly revoked by a later governance artifact; or
- the source architecture artifact or contract artifact is superseded before
  consumption.

After expiry, no further writes may cite this artifact as authority.

### 8.4 Remaining consumption rules

1. Only AT3 may consume this grant for offline `NOTE_PATH` code and tests
   inside §5.2 paths, and only while the grant is effective and unexpired.
2. Green offline tests do not activate live read, live mutation, or runtime
   execution.
3. Any later live synthetic read, live synthetic mutation, or production-path
   execution requires a separate human authorization artifact with its own
   budgets and writable/runtime scope.
4. This artifact must not be cited as authority for STAGE_PATH work.
5. If implementation discovers a contract or architecture blocker, it must stop
   and return; it must not expand routes, bindings, or effects under this grant.
6. AT3 must return `IMPLEMENTATION_FILE_MANIFEST` listing every created or
   modified path; every path must remain under the three writable prefixes.

## 9. Authorization PR validation gate

This PR is class `authorization`. Before merge:

1. `git diff --check` is clean;
2. exactly one changed path, equal to:

   ```text
   governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md
   ```

3. no conflict markers;
4. no secrets, tokens, private record IDs, or credential material;
5. authorization state assertions in §10 hold;
6. source SHA assertions in §2 hold;
7. writable-path assertions in §5 hold;
8. repository-required deterministic validation / exact-head checks as required
   by project governance;
9. clean mergeability into `main`;
10. human review and human merge authority.

Adapter implementation must not proceed from an open or unmerged authorization
PR. Any push changes the exact head and requires re-validation and human
review.

## 10. Authorization state assertions

```text
PR_CLASS=authorization
UNIT=NW008_AT2_GHL_REST_NOTE_PATH_IMPLEMENTATION_AUTHORIZATION_001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md

SOURCE_PR=93
SOURCE_PR_HEAD=554854e0d957d514600107084ed6e8dcf3e43cb8
SOURCE_MERGE_SHA=831cddb6f5ef5b3389b399948315e9b6c74e1fbc
ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml

NOTE_PATH_ARCHITECTURE_READY=YES
STAGE_PATH_ARCHITECTURE_READY=NO

GRANT=NOTE_PATH_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO
SELF_ACTIVATION=FORBIDDEN

AUTHORIZED_CONSUMER_UNIT=NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

IMPLEMENTATION_SLICE=NOTE_PATH
IMPLEMENTATION_MODE=OFFLINE_ONLY
GRANT_PERMITS_WHEN_EFFECTIVE=NOTE_PATH_OFFLINE_IMPLEMENTATION_ONLY
IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES

ALLOWED_DOMAIN_API=get_bound_contact,create_meeting_note,verify_meeting_note
ALLOWED_PROVIDER_ROUTES=GET /contacts/{contactId};POST /contacts/{contactId}/notes;GET /contacts/{contactId}/notes/{noteId}
FAKE_TRANSPORT_REQUIRED=YES

FORBIDDEN_DOMAIN_API=get_bound_opportunity,advance_authorized_stage,verify_authorized_stage
FORBIDDEN_GENERIC_SURFACES=request,execute,raw_http,search,list,pagination,generic_provider_payload

STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO

NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CREDENTIAL_USE_AUTHORIZED=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0

WRITABLE_IMPLEMENTATION_PATHS=src/integrations/ghl/highlevel_rest/**;tests/integrations/ghl/highlevel_rest/**;fixtures/ghl/highlevel_rest/**
AUTHORIZATION_PR_WRITABLE_PATHS=governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
IMPLEMENTATION_EXECUTED_UNDER_THIS_UNIT=NO
```

## 11. Decision and stop

```text
BRANCH=governance/nw008-at2-note-path-implementation-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at2-ghl-rest-note-path-implementation-authorization-001.md
WRITABLE_PATHS=src/integrations/ghl/highlevel_rest/**;tests/integrations/ghl/highlevel_rest/**;fixtures/ghl/highlevel_rest/**
GRANT=NOTE_PATH_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
AUTHORIZED_CONSUMER_UNIT=NW008_AT3_GHL_REST_NOTE_PATH_OFFLINE_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
IMPLEMENTATION_MODE=OFFLINE_ONLY
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
NETWORK_ACCESS_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0
NEXT=HUMAN_REVIEW_AND_MERGE_AUTHORIZATION_PR
STOP_CODE=NW008_AT2_NOTE_PATH_IMPLEMENTATION_AUTHORIZATION_READY_FOR_PR_REVIEW
```

STOP. Return this authorization artifact for ChatGPT / human review. Do not
implement adapter code under this unit.
