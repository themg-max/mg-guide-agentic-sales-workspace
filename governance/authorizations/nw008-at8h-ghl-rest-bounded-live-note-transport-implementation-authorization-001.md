# NW-008 AT-8H — HighLevel REST Bounded Live NOTE Transport Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md

BASE_REF=origin/main
BASE_SHA=180818eede0fc57c846db3cc5b06f64e2ffb7e7e

PREDECESSOR_PR=110
PREDECESSOR_HEAD_SHA=9acb6173552d47a60c15b3ebd704ada41e75b140
PREDECESSOR_MERGE_SHA=180818eede0fc57c846db3cc5b06f64e2ffb7e7e
PREDECESSOR_MERGE_VERIFIED=YES

SOURCE_AT8G_COMPLETION_ARTIFACT=proof/nw008/at-8g/nw008-at8g-note-path-at1-execution-store-integration-completion-001.md
SOURCE_AT8G_COMPLETION_REVIEWER_DISPOSITION=proof/nw008/at-8g/nw008-at8g-completion-decision-reviewer-disposition-001.md

SOURCE_AT8C_ARTIFACT=docs/nw008/nw-008-at8c-ghl-rest-note-path-live-execution-boundary-design-001.md
SOURCE_AT8G_AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8g-note-path-at1-execution-store-integration-authorization-001.md
SOURCE_AT8G_AUTHORIZATION_MERGE_SHA=f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b
SOURCE_AT8G_IMPLEMENTATION_PR=109
SOURCE_AT8G_IMPLEMENTATION_HEAD_SHA=300e91ec6971bdca5d068676317cca6c5e4e7fd2
SOURCE_AT8G_IMPLEMENTATION_MERGE_SHA=27344d62c921c50534d8a6efdaca2ee41f568b0f
SOURCE_AT8G_IMPLEMENTATION_MERGE_VERIFIED=YES

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE

GRANT=BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES

IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
```

This artifact is an authorization proposal only. Creating, reviewing, or merging it does not itself implement transport, load credentials, access HighLevel, create or read a live note, bind a CRM contact, mutate production configuration, or grant a live CRM mutation.

The sole authorized consumer is `NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001`. No other unit may consume this grant.

### Activation semantics

```text
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=MERGE_TO_MAIN
ACTIVATION_RULE=MERGED_EXACT_ARTIFACT_ON_MAIN_PLUS_CONSUMER_VERIFICATION
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
CONSUMER_MUST_VERIFY_EXACT_AUTHORIZATION_MERGE=YES
```

At authoring, this grant is proposed and not effective. Effectiveness is not a mutable field inside this file. Effectiveness is established only by repository state:

1. the exact authorization artifact path is present on `main` via human review and merge; and
2. the authorized consumer unit `NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001` independently verifies that merge (exact path on `origin/main` / merge ancestry) before writing transport implementation code.

The artifact text does not need to mutate after merge to become effective. Rewriting any effectiveness field inside this file is forbidden and is not an activation mechanism.

This grant is one-shot, non-reusable, and non-transferable. When effective, it authorizes only bounded live-note transport implementation. It does not grant live transport execution, live note write, live read, live CRM mutation, real credential use, Secret Manager access, IAM change, deployment change, or production configuration mutation.

```text
GRANT_PERMITS_WHEN_EFFECTIVE=BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_ONLY

AT8H_AUTHORIZES_TRANSPORT_IMPLEMENTATION=YES_WHEN_EFFECTIVE
AT8H_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8H_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8H_AUTHORIZES_LIVE_READ=NO
AT8H_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8H_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8H_AUTHORIZES_SECRET_ACCESS=NO

LIVE_TRANSPORT_EXECUTION=NO
LIVE_NOTE_WRITE=NO
LIVE_NOTE_READBACK=NO
LIVE_CRM_MUTATION=NO
REAL_CREDENTIAL_USE=NO
SECRET_ACCESS=NO
IAM_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION=NO

NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
CREDENTIAL_USE_AUTHORIZED=NO
SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
SECRET_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION_AUTHORIZED=NO

LIVE_MUTATION_AUTHORIZATION=FROZEN
LIVE_NOTE_MUTATION_AUTHORIZATION=FROZEN

EXTERNAL_EFFECTS_ALLOWED=0
```

The authorized implementation may contain dormant transport/network code that models the frozen HighLevel v3 note routes. Implementation tests and validation must execute zero real HighLevel calls. Dormant network code is not live-transport execution authority.

### Non-transitivity

```text
PR110_COMPLETION_AUTHORITY_GRANTS_AT8H=NO
AT10_EXECUTION_OR_COMPLETION_AUTHORITY_GRANTS_AT8H=NO
AT8G_AUTHORIZATION_GRANTS_AT8H=NO
AT8H_AUTHORIZATION_GRANTS_LIVE_MUTATION=NO
AT8H_AUTHORIZATION_GRANTS_REAL_CREDENTIAL_USE=NO
AT8H_AUTHORIZATION_GRANTS_PRODUCTION_CHANGE=NO
AT8H_AUTHORIZATION_GRANTS_LIVE_TRANSPORT_EXECUTION=NO

AT8H_BOUNDED_IMPLEMENTATION_AUTHORIZATION_INFERRED_FROM_PR110=NO
AT8H_BOUNDED_IMPLEMENTATION_AUTHORIZATION_INFERRED_FROM_AT10=NO
AT8H_BOUNDED_IMPLEMENTATION_AUTHORIZATION_INFERRED_FROM_AT8G=NO
```

PR110 closed AT8G completion. That closure removes a predecessor blocker; it does not grant AT8H implementation. AT8G authority was one-shot, consumed, and non-reusable. AT10 completion/reconciliation is a later independent lane and provides no authority to AT8H. This authorization, even after merge, does not grant live mutation, live transport execution, real credential use, or production configuration changes.

## 2. Readiness and blocker state

Preflight was run before this artifact was authored and repaired.

```text
Working branch is not main
YES

PR110_MERGED
YES
PR110_HEAD_SHA=9acb6173552d47a60c15b3ebd704ada41e75b140
PR110_MERGE_SHA=180818eede0fc57c846db3cc5b06f64e2ffb7e7e
PREDECESSOR_MERGE_SHA is HEAD of origin/main
YES

AT8C_BLOCKER_1_DURABLE_STORE_FIT=CLOSED
AT8C_BLOCKER_2_CROSS_PROCESS_RESERVATION=CLOSED
AT8C_BLOCKER_3_PRIVATE_AT8_CAPABILITY_HANDOFF=CLOSED
AT8C_BLOCKER_4_BOUNDED_LIVE_NOTE_NETWORK_TRANSPORT=OPEN

AT8H_PURPOSE=CLOSE_AT8C_BLOCKER_4_BY_IMPLEMENTATION_AND_OFFLINE_VERIFICATION
LIVE_MUTATION_AUTHORIZATION_READY=NO
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| Predecessor PR #110 merge commit | `180818eede0fc57c846db3cc5b06f64e2ffb7e7e` |
| Predecessor merge commit is reachable from `origin/main` | YES |
| PR110 head SHA present in ancestry | `9acb6173552d47a60c15b3ebd704ada41e75b140` |
| AT8G completion proof present on main | YES |
| AT8G completion decision disposition present on main | YES |
| AT8G authorization merge SHA | `f62761079261bcb6fe5be8c5e62e5ccc6bd9ba2b` |
| AT8G implementation PR #109 merge SHA | `27344d62c921c50534d8a6efdaca2ee41f568b0f` |
| AT8C blocker 1 (durable store fit) | CLOSED |
| AT8C blocker 2 (cross-process reservation) | CLOSED |
| AT8C blocker 3 (private AT8 capability handoff) | CLOSED |
| AT8C blocker 4 (bounded live note network transport) | OPEN |
| This unit executed a live GET | NO |
| This unit executed a live POST | NO |
| This unit loaded credentials | NO |
| This unit accessed HighLevel | NO |
| Live mutation authorization issued | NO |
| Live transport implementation performed by this unit | NO |
| Consumer implementation performed by this unit | NO |

The connected HighLevel account is a live CRM environment. No ordinary existing contact is authorized as an AT8H test target. Synthetic/private target binding is not required to implement the transport seam and must not be inferred from arbitrary CRM records.

### Predecessor authority scope

```text
AT8G_AUTHORIZATION_SCOPE=NOTE_PATH_AT1_EXECUTION_STORE_OFFLINE_INTEGRATION
AT8G_IMPLEMENTATION_AUTHORIZATION_CONSUMED=YES
AT8G_AUTHORIZATION_REUSABLE=NO
AT8G_INTEGRATION_IMPLEMENTATION_COMPLETED=YES

AT8H_AUTHORIZATION_SCOPE=BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION
AT8H_IMPLEMENTATION_AUTHORIZATION_CONSUMED=NO
AT8H_LIVE_TRANSPORT_IMPLEMENTATION_COMPLETED=NO
LIVE_NOTE_TRANSPORT_IMPLEMENTED=NO
LIVE_NOTE_TRANSPORT_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
```

AT8G was confined to offline integration of NOTE_PATH with At1ExecutionStore. That scope has been consumed and completed. AT8H authorizes a separate, bounded scope: live note transport implementation. These are disjoint lanes with independent grant activation.

## 3. Provider contract frozen for implementation

Current HighLevel v3 provider contract to model:

```text
BASE_URL=https://services.leadconnectorhq.com
API_VERSION=v3

CREATE_NOTE_METHOD=POST
CREATE_NOTE_PATH=/contacts/{contact_id}/notes
CREATE_NOTE_SCOPE=contacts.write

GET_NOTE_METHOD=GET
GET_NOTE_PATH=/contacts/{contact_id}/notes/{same_run_note_id}
GET_NOTE_SCOPE=contacts.readonly

TOKEN_CLASS=SUB_ACCOUNT_TOKEN
AUTH_METHOD=BEARER_TOKEN_OR_PRIVATE_INTEGRATION_TOKEN
```

Provider note bodies must preserve the existing canonical NOTE_PATH serialized note content. The transport may map provider-specific optional author/title metadata only when explicitly supplied through private/injected configuration. It must not change the logical NOTE contract.

## 4. Exact implementation objective

Implement one dedicated transport class/module that satisfies the existing NOTE_PATH dispatch shape for exactly two routes:

```text
POST /contacts/{bound_contact_id}/notes
GET  /contacts/{bound_contact_id}/notes/{same_run_note_id}
```

The transport must be injectable into the existing NotePathAdapter without changing the AT8G durable reservation contract.

Recommended subject path:

```text
src/integrations/ghl/highlevel_rest/live_note_transport.py
```

Recommended transport contract:

```text
BoundedLiveNoteTransport.dispatch(method, path, body=None) -> response
```

The implementation must normalize provider responses to the existing NOTE_PATH response expectations without exposing raw credentials or unrelated provider payload fields.

This authorization PR does not implement that module. Implementation is reserved for the authorized consumer unit after this artifact is merged and independently verified.

## 5. Frozen runtime bounds

```text
ALLOWED_METHODS={POST,GET}
ALLOWED_POST_ROUTE=/contacts/{bound_contact_id}/notes
ALLOWED_GET_ROUTE=/contacts/{bound_contact_id}/notes/{same_run_note_id}

POST_ATTEMPTS_MAX=1
POST_SUCCESSES_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1

AUTOMATIC_RETRY=NO
FALLBACK=NO
SECOND_POST=NO
SEARCH=NO
LIST=NO
PAGINATION=NO
DELETE=NO
UPDATE_NOTE=NO
ALTERNATE_TARGET=NO
ALTERNATE_ROUTE=NO
GENERIC_EXECUTE=NO
RAW_REST_FALLBACK=NO
COMPENSATING_MUTATION=NO
AUTOMATIC_CLEANUP=NO
```

The GET route may use only the exact note ID returned by the same-run POST. Caller-supplied arbitrary note IDs are forbidden.

## 6. Private binding and credential boundary

```text
PUBLIC_CONTACT_ID=FORBIDDEN
PUBLIC_LOCATION_ID=FORBIDDEN
PUBLIC_NOTE_ID=FORBIDDEN
PUBLIC_TOKEN=FORBIDDEN
PUBLIC_AUTHORIZATION_HEADER=FORBIDDEN
PUBLIC_RAW_PROVIDER_RESPONSE=FORBIDDEN

TARGET_CONTACT_SOURCE=PRIVATE_TRUSTED_AT8_CAPABILITY_ONLY
CALLER_SUPPLIED_CONTACT_OVERRIDE=NO
CALLER_SUPPLIED_READBACK_NOTE_ID=NO

CREDENTIAL_SOURCE_IMPLEMENTATION=INJECTED_ONLY
SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
ENVIRONMENT_SECRET_DISCOVERY_AUTHORIZED=NO
HARDCODED_TOKEN_AUTHORIZED=NO
AUTHORIZATION_HEADER_LOGGING=NO
TOKEN_LOGGING=NO
```

AT8H may define an injected credential parameter/protocol for future execution, but AT8H implementation and tests must use synthetic placeholders only. No real token or live private binding may be loaded during AT8H implementation.

## 7. Ambiguity and fail-closed semantics

```text
POST_DISPATCH_TIMEOUT_OR_TRANSPORT_UNCERTAINTY=AMBIGUOUS
AUTOMATIC_RETRY_AFTER_AMBIGUITY=NO
SECOND_POST_AFTER_AMBIGUITY=NO
BUSINESS_EFFECT_TRUTH_AFTER_UNCERTAIN_DISPATCH=UNKNOWN
AMBIGUITY_TRUTH=UNKNOWN
```

The transport must preserve enough response classification for NotePathAdapter and At1ExecutionStore to retain the AT8G rule that unproven post-dispatch effects are UNKNOWN.

A network/transport exception must never silently fall back to another route, target, method, or retry.

## 8. Writable scope

Authorized implementation paths only:

```text
src/integrations/ghl/highlevel_rest/live_note_transport.py
tests/integrations/ghl/highlevel_rest/test_live_note_transport.py
proof/nw008/at-8h/**
docs/nw008/nw-008-at8h-*
governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md
```

Conditional additional test files under the same directory are permitted only when required to keep test responsibilities separated:

```text
tests/integrations/ghl/highlevel_rest/test_live_note_transport_*.py
```

No other source paths are authorized by default.

## 9. Blocked scope

```text
src/integrations/ghl/highlevel_rest/note_path.py=BLOCKED
src/integrations/ghl/at1_execution_store.py=BLOCKED
src/integrations/ghl/at1_live_transport_adapter.py=BLOCKED
src/integrations/ghl/at1_live_transport_serializer.py=BLOCKED
src/integrations/ghl/bounded_at1_executor.py=BLOCKED
src/integrations/ghl/read_adapter.py=BLOCKED
src/integrations/ghl/highlevel_rest/fake_transport.py=BLOCKED
src/integrations/ghl/__init__.py=BLOCKED
src/integrations/ghl/highlevel_rest/__init__.py=BLOCKED
contracts/**=BLOCKED
fixtures/**=BLOCKED
src/orchestration/**=BLOCKED
src/agents/**=BLOCKED
src/mg_guide/**=BLOCKED
workspace_addon/**=BLOCKED
.github/**=BLOCKED
requirements.txt=BLOCKED
pyproject.toml=BLOCKED
Dockerfile=BLOCKED
.env.example=BLOCKED
scripts/**=BLOCKED
local/**=BLOCKED
proof/nw008/at-10/**=BLOCKED
```

Dependency/package changes are not authorized. Prefer standard-library HTTP facilities or an already available injected HTTP client seam without modifying dependency manifests.

No NOTE_PATH changes. No At1ExecutionStore changes. No workflow/IAM/deploy/secrets changes.

## 10. Implementation-time execution posture

```text
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
LIVE_NETWORK_CALLS_DURING_IMPLEMENTATION=0
HIGHLEVEL_CALLS_DURING_IMPLEMENTATION=0
CRM_MUTATIONS_DURING_IMPLEMENTATION=0
CREDENTIAL_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_ACCESS_DURING_IMPLEMENTATION=NO
IAM_CHANGE=NO
DEPLOYMENT_CHANGE=NO
PRODUCTION_CONFIGURATION_MUTATION=NO
EXTERNAL_EFFECTS=0
```

The implementation may contain dormant live-network code, but tests and implementation validation must not invoke a real HighLevel endpoint.

## 11. Required deterministic tests

```text
TEST_EXACT_POST_ROUTE=REQUIRED
TEST_EXACT_GET_ROUTE=REQUIRED
TEST_BOUND_CONTACT_ONLY=REQUIRED
TEST_SAME_RUN_NOTE_ID_ONLY=REQUIRED
TEST_POST_MAX_ONE=REQUIRED
TEST_GET_MAX_ONE=REQUIRED
TEST_TOTAL_CALLS_MAX_TWO=REQUIRED
TEST_NO_RETRY=REQUIRED
TEST_NO_SEARCH_LIST_PAGINATION=REQUIRED
TEST_NO_ALTERNATE_TARGET=REQUIRED
TEST_NO_GENERIC_EXECUTE=REQUIRED
TEST_AUTH_HEADER_NOT_LOGGED=REQUIRED
TEST_TOKEN_NOT_LOGGED=REQUIRED
TEST_RAW_PROVIDER_RESPONSE_NOT_PUBLISHED=REQUIRED
TEST_POST_TIMEOUT_CLASSIFIED_AMBIGUOUS=REQUIRED
TEST_NO_SECOND_POST_AFTER_AMBIGUITY=REQUIRED
TEST_PROVIDER_RESPONSE_NORMALIZATION=REQUIRED
TEST_PROVIDER_NOTE_ID_ONLY_IN_MEMORY_FOR_SAME_RUN_READBACK=REQUIRED
TEST_AT8G_DURABLE_RESERVATION_CONTRACT_UNCHANGED=REQUIRED
TEST_PR107_TRUST_BOUNDARY_UNCHANGED=REQUIRED
TEST_ZERO_REAL_NETWORK_CALLS=REQUIRED
```

Required tests include:

- exact POST route
- exact GET route
- bound contact only
- same-run note ID only
- POST max one
- GET max one
- total calls max two
- no retry
- no search/list/pagination
- no alternate target
- no generic execute
- no token/auth-header logging
- no raw provider-response publication
- ambiguous POST timeout classification
- no second POST after ambiguity
- zero real network calls
- AT8G durable reservation unchanged
- PR107 trust boundary unchanged

## 12. Proof-return requirements

The consumer implementation must return a durable proof packet containing at minimum:

```text
PROOF_UNIT=NW008_AT8H_GHL_REST_BOUNDED_LIVE_NOTE_TRANSPORT_IMPLEMENTATION_001
AUTHORIZATION_ARTIFACT_PATH=governance/authorizations/nw008-at8h-ghl-rest-bounded-live-note-transport-implementation-authorization-001.md
AUTHORIZATION_ARTIFACT_MERGE_SHA=<exact merge sha>
AUTHORIZATION_ARTIFACT_MERGE_VERIFIED=YES
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
BASE_REF=origin/main
BASE_SHA=<authorization merge sha or later verified main base>
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY
LIVE_NETWORK_CALLS_DURING_IMPLEMENTATION=0
HIGHLEVEL_CALLS_DURING_IMPLEMENTATION=0
CRM_MUTATIONS_DURING_IMPLEMENTATION=0
CREDENTIAL_ACCESS_DURING_IMPLEMENTATION=NO
SECRET_ACCESS_DURING_IMPLEMENTATION=NO
NOTE_PATH_MODIFIED=NO
AT1_EXECUTION_STORE_MODIFIED=NO
PR107_TRUST_BOUNDARY_WEAKENED=NO
POST_ATTEMPTS_MAX=1
READBACK_GET_ATTEMPTS_MAX=1
TOTAL_NETWORK_CALLS_MAX=2
TOTAL_MUTATION_CALLS_MAX=1
AUTOMATIC_RETRY=NO
SEARCH=NO
LIST=NO
PAGINATION=NO
RAW_REST_FALLBACK=NO
AUTHORIZATION_HEADER_LOGGING=NO
TOKEN_LOGGING=NO
AMBIGUITY_TRUTH=UNKNOWN
TEST_SUITE_ALL_PASS=YES
PHASE1_DETERMINISTIC_VALIDATION=PASS
```

Consumption record path for the authorized consumer:

```text
CONSUMPTION_RECORD_PATH=proof/nw008/at-8h/
AUTHORIZATION_EXPIRATION=ONE_SHOT_ONLY
AUTHORIZATION_REUSE_PERMITTED=NO
AUTHORIZATION_TRANSFER_PERMITTED=NO
REUSE_ATTEMPT_BEHAVIOR=REJECT
TRANSFER_ATTEMPT_BEHAVIOR=REJECT
```

## 13. Activation and authority semantics

```text
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=MERGE_TO_MAIN
CONSUMER_MUST_VERIFY_EXACT_AUTHORIZATION_MERGE=YES
SELF_ACTIVATION=FORBIDDEN

AT8H_AUTHORIZES_TRANSPORT_IMPLEMENTATION=YES_WHEN_EFFECTIVE
AT8H_AUTHORIZES_LIVE_TRANSPORT_EXECUTION=NO
AT8H_AUTHORIZES_LIVE_NOTE_WRITE=NO
AT8H_AUTHORIZES_LIVE_CRM_MUTATION=NO
AT8H_AUTHORIZES_LIVE_READ=NO
AT8H_AUTHORIZES_REAL_CREDENTIAL_USE=NO
AT8H_AUTHORIZES_SECRET_ACCESS=NO
```

This authorization becomes effective only after:

1. this artifact is merged to `main` via human review and approval; and
2. the authorized consumer unit independently verifies the exact merge (path on `origin/main` / merge ancestry) before writing implementation code.

The consumer unit must include the merge SHA in its implementation PR to establish the provenance chain. No other unit may consume this grant.

## 14. Required next sequence after AT8H implementation

```text
AT8H_AUTHORIZATION_REVIEW_AND_MERGE
-> AT8H_BOUNDED_TRANSPORT_IMPLEMENTATION
-> EXACT_HEAD_REVIEW_AND_MERGE
-> READ_ONLY_LIVE_EXECUTION_BOUNDARY_REINSPECTION

ONLY_IF_REINSPECTION_PASS:
-> SEPARATE_ONE_SHOT_LIVE_NOTE_MUTATION_AUTHORIZATION
-> PRIVATE_SYNTHETIC_TARGET_BINDING_VERIFICATION
-> CREDENTIAL_SCOPE_VERIFICATION contacts.write + contacts.readonly
-> HUMAN_GHL_SPACE_OWNER_COUNTERSIGNATURE
-> ONE_POST_MAX + ONE_EXACT_READBACK_GET_MAX
-> EXECUTION_PROOF
-> RECONCILIATION/CLOSEOUT
```

The later live-mutation grant must bind a private synthetic/test contact and must not authorize arbitrary existing CRM contacts.

## 15. Authorization verdict at authoring

```text
AT8H_AUTHORIZATION_ARTIFACT_READY_FOR_REVIEW=YES
AT8H_GRANT_EFFECTIVE=NO
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
LIVE_NOTE_EXECUTION_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZATION_READY=NO
```
