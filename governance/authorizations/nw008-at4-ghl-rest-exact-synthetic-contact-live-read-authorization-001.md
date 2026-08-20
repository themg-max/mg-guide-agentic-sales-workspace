# NW-008 AT-4 — HighLevel REST Exact Synthetic Contact Live-Read Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT4_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=governance/nw008-at4-exact-synthetic-contact-live-read-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md

SOURCE_IMPLEMENTATION_PR=95
SOURCE_IMPLEMENTATION_HEAD=43b4c6ae36ea8eb7a829da47731f702ac2823e58
SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52
BASE_REF=origin/main
BASE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52

ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml
OFFLINE_IMPLEMENTATION_SOURCE=PR95_MERGED_NOTE_PATH

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE

GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does not load a credential, open a network socket, access HighLevel, perform
the authorized GET, perform any live read, perform any mutation, publish private
IDs, change implementation code, modify proof files, or change deployment / IAM /
secrets.

### Conditional grant semantics

```text
GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the
artifact defines a bounded one-shot live-read permission that becomes usable
only when both of the following are true:

1. the exact authorization artifact path is present on `main` via human review
   and merge; and
2. the authorized consumer unit
   `NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001`
   verifies that merge (exact path on `origin/main` / merge ancestry) before
   performing the GET.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is not standing live-read authority, not live-mutation authority,
not note-path execution authority, not stage-path authority, and not a reusable
grant.

## 2. Verified prerequisites and source authority

Preflight was run before this artifact was authored:

```text
pwd
/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git fetch origin

git branch --show-current
governance/nw008-at4-exact-synthetic-contact-live-read-authorization-001

git rev-parse HEAD
86d315379856102c7ee1a38e4c36c70c7560fe52

Working branch is not main
YES

origin/main contains SOURCE_IMPLEMENTATION_MERGE_SHA
86d315379856102c7ee1a38e4c36c70c7560fe52
YES

SOURCE_IMPLEMENTATION_HEAD is ancestor of origin/main
43b4c6ae36ea8eb7a829da47731f702ac2823e58
YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #95 reviewed head | `43b4c6ae36ea8eb7a829da47731f702ac2823e58` |
| PR #95 merge commit | `86d315379856102c7ee1a38e4c36c70c7560fe52` |
| PR #95 merge commit is reachable from `origin/main` | YES |
| PR #95 reviewed head is an ancestor of `origin/main` | YES |
| Architecture artifact present on base | YES |
| Contract artifact present on base | YES |
| Offline NOTE_PATH implementation present on base | YES |
| Source architecture live read/mutation/execution | NO |
| This unit executed a live GET | NO |

Bound durable source inputs (read-only for the future execution lane):

```text
ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml
SOURCE_IMPLEMENTATION_PR=95
SOURCE_IMPLEMENTATION_HEAD=43b4c6ae36ea8eb7a829da47731f702ac2823e58
SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52
```

PR #95 merged an offline-only NOTE_PATH adapter. That merge is a prerequisite
for this live-read grant. It does not itself authorize network access,
credential use, live read, or live mutation. AT5 may not reinterpret PR #95 as
live NOTE_PATH execution authority, note-create authority, or stage-path
authority.

## 3. Environment and private-binding rules

```text
CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM
SYNTHETIC_ONLY=YES
PRIVATE_ALLOWLIST_REQUIRED=YES
EXACT_ID_TARGETING_REQUIRED=YES
PRIVATE_BINDING_PUBLICATION=NO
PRIVATE_BINDING_SYMBOLS=location_id,contact_id
```

The target is the active canonical business CRM. Safety derives from the
private preverified synthetic-record allowlist and exact-ID-only access, not
from environment isolation.

```text
ISOLATED_HACKATHON_TEST_LOCATION=NO
REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
ALTERNATE_TARGET_RESOLUTION=NO
```

Private binding values must be loaded by private adapter / execution
infrastructure only. Actual `location_id` and `contact_id` values MUST NOT
appear in this artifact, in AT5 public proof, in logs committed to this
repository, or in the authorization PR body.

```text
PRIVATE_BINDING_VALUES_IN_THIS_ARTIFACT=FORBIDDEN
PRIVATE_BINDING_VALUES_IN_PUBLIC_PROOF=FORBIDDEN
CALLER_SUPPLIED_CONTACT_ID=FORBIDDEN
CALLER_SUPPLIED_LOCATION_ID=FORBIDDEN
AGENT_SUPPLIED_TARGET_OVERRIDE=FORBIDDEN
```

AT5 must fail closed if the private binding is missing, incomplete, or cannot
be loaded without publishing values into the public tree.

## 4. What this authorization permits

### 4.1 Named consumer and live authority

When the conditional grant is effective, only
`NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001` with
`AUTHORIZED_CONSUMER_PR_CLASS=execution_proof` may consume it, and only once.

```text
GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_PERMITS_WHEN_EFFECTIVE=EXACT_SYNTHETIC_CONTACT_GET_ONLY

NETWORK_ACCESS_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
CREDENTIAL_USE_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_READ_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY

LIVE_MUTATION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
NOTE_CREATE_AUTHORIZED=NO
STAGE_PATH_AUTHORIZED=NO
```

### 4.2 Authorized provider operation (exactly one)

```text
METHOD=GET
ROUTE=/contacts/{private_binding.contact_id}
API_VERSION=v3
SCOPE=contacts.readonly
QUERY_PARAMETERS=NO
REDIRECT_FOLLOWING=NO
PURPOSE=VERIFY_EXACT_SYNTHETIC_CONTACT_BINDING
```

The path parameter MUST be injected from `private_binding.contact_id`. No other
contact identifier, search result, list item, or caller-supplied ID may be
substituted.

### 4.3 Response fields consumed only

```text
RESPONSE_FIELDS_CONSUMED_ONLY=
contact.id
contact.locationId

REQUIRE=
contact.id == private_binding.contact_id
contact.locationId == private_binding.location_id
```

AT5 may use those two fields solely to prove that the privately bound synthetic
contact exists and that the returned location matches the private location
binding. No other provider field may be logged, persisted, copied into public
proof, or treated as authorization to continue into note or stage operations.

### 4.4 Execution budget

```text
CONTACT_GET_ATTEMPTS_MAX=1
NETWORK_CALL_COUNT_MAX=1
MUTATION_CALL_COUNT_MAX=0
AUTOMATIC_RETRY=NO
ALTERNATE_TARGET_RESOLUTION=NO
AMBIGUOUS_GET_RETRY=NO
```

Exactly one HighLevel HTTPS GET is authorized. A second attempt, automatic
retry, redirect follow, fallback URL, fallback method, or alternate target is
not authorized.

### 4.5 Data minimization

```text
FULL_PROVIDER_RESPONSE_LOG=FORBIDDEN
FULL_PROVIDER_RESPONSE_PERSIST=FORBIDDEN
PUBLIC_PROOF_MAY_CONTAIN_ONLY=BOOLEAN_AND_SANITIZED_OUTCOME_FIELDS
PRIVATE_RECORD_PAYLOAD_PUBLICATION=FORBIDDEN
```

Public proof may record only sanitized outcome flags such as:

```text
EXACT_CONTACT_GET_EXECUTED
CONTACT_ID_MATCH
LOCATION_ID_MATCH
LIVE_READ_VERIFIED
NETWORK_CALL_COUNT
MUTATION_CALL_COUNT
EXTERNAL_MUTATIONS
FAIL_CLOSED
STOP_CODE
```

It must not persist the raw provider body, headers, tokens, or private IDs.

## 5. Explicit denials

### 5.1 Mutations and adjacent NOTE_PATH / STAGE_PATH operations

```text
LIVE_MUTATION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
NOTE_CREATE_AUTHORIZED=NO
NOTE_GET_AUTHORIZED=NO
NOTE_POST_AUTHORIZED=NO
OPPORTUNITY_GET_AUTHORIZED=NO
OPPORTUNITY_PUT_AUTHORIZED=NO
STAGE_PATH_AUTHORIZED=NO
STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO
```

Forbidden provider operations under this authorization include, without
limitation:

```text
POST /contacts/{contactId}/notes
GET  /contacts/{contactId}/notes/{noteId}
GET  /opportunities/{opportunityId}
PUT  /opportunities/{opportunityId}
```

Forbidden domain methods under this authorization include, without limitation:

```text
create_meeting_note
verify_meeting_note
get_bound_opportunity
advance_authorized_stage
verify_authorized_stage
```

A successful exact-contact GET does not unlock note create, note readback, or
stage mutation. Those remain separately unauthorized.

### 5.2 Search, list, pagination, and alternate targeting

```text
BROAD_SEARCH_AUTHORIZED=NO
LIST_AUTHORIZED=NO
PAGINATION_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
ALTERNATE_TARGET_RESOLUTION=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO
QUERY_PARAMETERS_AUTHORIZED=NO
```

Denied behaviors include, without limitation:

```text
search
list
pagination
query parameters
alternate contact
alternate target resolution
generic execute
arbitrary HTTP method
arbitrary URL
```

AT5 may not search for a contact, list contacts, page through results, resolve
an “equivalent” synthetic record, or retry against a different ID if the bound
contact GET fails.

### 5.3 Credential, IAM, deployment, and implementation expansion

```text
CREDENTIAL_CREATE_AUTHORIZED=NO
CREDENTIAL_EXPAND_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
IAM_CHANGE_AUTHORIZED=NO
DEPLOYMENT_CHANGE_AUTHORIZED=NO
IMPLEMENTATION_CHANGE_AUTHORIZED=NO
CONTRACT_CHANGE_AUTHORIZED=NO
ARCHITECTURE_CHANGE_AUTHORIZED=NO
```

Credential use is authorized only as the minimum bearer / PIT required to
perform the exact contact GET. AT5 may not create, rotate, expand, or commit
credentials.

### 5.4 This authorization unit itself

This AT4 unit must not:

- load credentials;
- access HighLevel;
- perform the GET;
- perform any live read;
- perform any mutation;
- publish private IDs;
- change implementation code;
- modify proof files;
- modify deployment / IAM / secrets.

## 6. Writable paths

### 6.1 This authorization PR (current unit)

This authorization-planning unit may write exactly one path:

```text
governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md
```

No adapter code, tests, fixtures, contracts, workflows, proof files, or deploy
assets may be created or modified in this unit.

### 6.2 Future AT5 execution-proof lane only

After the conditional grant is effective (exact artifact merged to `main` and
verified by the consumer), only
`NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001` may write
only a sanitized execution-proof artifact under:

```text
WRITABLE_EXECUTION_PROOF_PATHS=
proof/nw008/nw-008-at5-ghl-rest-exact-synthetic-contact-live-read-execution-001.md

IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
PUBLIC_TREE_IMPLEMENTATION_CHANGE_AUTHORIZED=NO
```

AT5 may use a private runtime, private binding store, and existing credential
provider solely to issue the one authorized GET. Those private surfaces are not
writable paths in this public repository.

### 6.3 Explicitly non-writable for AT5

```text
NON_WRITABLE_EXAMPLES=
src/**
tests/**
fixtures/**
contracts/**
docs/nw008/**
governance/**
workspace_addon/**
scripts/**
deploy/**
.github/**
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

If AT5 discovers that a public-tree implementation change is required to
perform the GET, it must stop and return; it must not expand this grant into
an implementation PR.

## 7. Success conditions for future AT5

AT5 may claim success only when all of the following are true:

```text
EXACT_CONTACT_GET_EXECUTED=YES
CONTACT_ID_MATCH=YES
LOCATION_ID_MATCH=YES
LIVE_READ_VERIFIED=YES
NETWORK_CALL_COUNT=1
MUTATION_CALL_COUNT=0
EXTERNAL_MUTATIONS=0
```

Meaning:

1. exactly one HighLevel REST v3 `GET /contacts/{private_binding.contact_id}`
   completed;
2. `contact.id` equals `private_binding.contact_id`;
3. `contact.locationId` equals `private_binding.location_id`;
4. no other network call was issued;
5. no mutation was issued;
6. public proof remains sanitized.

A matching GET is verification only. It is not note-create authority and not
stage-path authority.

## 8. Fail-closed conditions

AT5 must fail closed, stop, and return terminal proof without retry, fallback,
or mutation if any of the following occur:

```text
missing private binding
missing credential
missing required scope
401
403
400
404
redirect
unexpected schema
contact ID mismatch
location ID mismatch
any requested alternate target
any requested search/list/pagination
```

Additional terminal conditions:

```text
AUTHORIZATION_ARTIFACT_NOT_ON_MAIN
CONSUMER_UNIT_MISMATCH
GRANT_ALREADY_CONSUMED
QUERY_PARAMETER_PRESENT
NON_GET_METHOD
NON_EXACT_CONTACT_ROUTE
FULL_PROVIDER_RESPONSE_WOULD_BE_PUBLISHED
CALLER_SUPPLIED_ID
```

On failure:

```text
STOP
NO RETRY
NO FALLBACK
NO MUTATION
NETWORK_CALL_COUNT_MUST_NOT_INCREASE_AFTER_FAILURE
MUTATION_CALL_COUNT=0
EXTERNAL_MUTATIONS=0
```

## 9. Authorization consumption rules

```text
AUTHORIZED_CONSUMER_UNIT=NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
ONE_SHOT_SCOPE=EXACT_SYNTHETIC_CONTACT_GET
REUSE_AS_NOTE_CREATE_AUTHORITY=NO
REUSE_AS_NOTE_GET_AUTHORITY=NO
REUSE_AS_STAGE_PATH_AUTHORITY=NO
REUSE_AS_GENERIC_LIVE_READ_AUTHORITY=NO
REUSE_AS_IMPLEMENTATION_AUTHORITY=NO
STANDING_GRANT=NO
```

### 9.1 Named consumer binding

Only unit `NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001`
with `AUTHORIZED_CONSUMER_PR_CLASS=execution_proof` may consume this grant. No
other unit, agent session, PR class, or follow-on lane may inherit it.

### 9.2 Activation and verification

1. Before merge: `AUTHORIZATION_EFFECTIVE=NO` and `GRANT_STATUS=CONDITIONAL`.
2. Activation condition: the exact authorization artifact is merged to `main`
   by human authority (`GRANT_ACTIVATION=MERGE_TO_MAIN`).
3. AT5 must verify that merge (exact path present on `origin/main` and
   ancestry/merge evidence) before any live GET.
4. The artifact text is not required to mutate after merge
   (`ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO`).

### 9.3 One-shot, non-reuse, and expiry

`AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT`. The grant is not reusable and not
transferable:

```text
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

The authorization expires when any of the following occurs:

- AT5 completes the one authorized GET, successfully or fail-closed; or
- the authorization is explicitly revoked by a later governance artifact; or
- the source implementation, architecture, or contract is superseded before
  consumption.

After expiry, no further live call may cite this artifact as authority. A later
live note, live stage, or additional contact GET requires a new human
authorization.

### 9.4 Remaining consumption rules

1. Only AT5 may consume this grant, and only for the exact contact GET in §4.
2. A successful GET does not activate note create, note GET, opportunity GET,
   opportunity PUT, or STAGE_PATH.
3. AT5 must not change implementation code, contracts, architecture, deploy,
   IAM, or secrets in the public tree.
4. AT5 must not publish private binding values.
5. If AT5 cannot perform the GET within this bound, it must stop and return; it
   must not search, list, paginate, retarget, or mutate.

## 10. Authorization PR validation gate

This PR is class `authorization`. Before merge:

1. `git diff --check` is clean;
2. exactly one changed path, equal to:

   ```text
   governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md
   ```

3. no conflict markers;
4. no secrets, tokens, private record IDs, or credential material;
5. `SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52`
   is reachable from `origin/main`;
6. named consumer assertion in §9 holds;
7. one-shot / non-reuse assertions hold;
8. exact-GET-only assertion holds;
9. mutation denial assertions hold;
10. search / list / pagination denial assertions hold;
11. `PRIVATE_BINDING_PUBLICATION=NO` holds;
12. repository-required deterministic validation / exact-head checks as required
    by project governance;
13. clean mergeability into `main`;
14. human review and human merge authority.

AT5 must not proceed from an open or unmerged authorization PR. Any push
changes the exact head and requires re-validation and human review.

## 11. Authorization state assertions

```text
PR_CLASS=authorization
UNIT=NW008_AT4_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_AUTHORIZATION_001
MODE=AUTHORIZATION_ARTIFACT_ONLY
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md

SOURCE_IMPLEMENTATION_PR=95
SOURCE_IMPLEMENTATION_HEAD=43b4c6ae36ea8eb7a829da47731f702ac2823e58
SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52
ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml

GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO
SELF_ACTIVATION=FORBIDDEN

AUTHORIZED_CONSUMER_UNIT=NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

CRM_ENVIRONMENT_CLASS=ACTIVE_CANONICAL_BUSINESS_CRM
SYNTHETIC_ONLY=YES
PRIVATE_ALLOWLIST_REQUIRED=YES
EXACT_ID_TARGETING_REQUIRED=YES
PRIVATE_BINDING_PUBLICATION=NO
PRIVATE_BINDING_SYMBOLS=location_id,contact_id

NETWORK_ACCESS_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
CREDENTIAL_USE_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_READ_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_MUTATION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
NOTE_CREATE_AUTHORIZED=NO
NOTE_GET_AUTHORIZED=NO
NOTE_POST_AUTHORIZED=NO
STAGE_PATH_AUTHORIZED=NO

AUTHORIZED_PROVIDER_OPERATION=GET /contacts/{private_binding.contact_id}
API_VERSION=v3
PURPOSE=VERIFY_EXACT_SYNTHETIC_CONTACT_BINDING
RESPONSE_FIELDS_CONSUMED_ONLY=contact.id,contact.locationId
CONTACT_GET_ATTEMPTS_MAX=1
AUTOMATIC_RETRY=NO
ALTERNATE_TARGET_RESOLUTION=NO

BROAD_SEARCH_AUTHORIZED=NO
LIST_AUTHORIZED=NO
PAGINATION_AUTHORIZED=NO
ALTERNATE_TARGET_SEARCH_AUTHORIZED=NO
NON_ALLOWLISTED_RECORD_ACCESS_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_READ_AUTHORIZED=NO
REAL_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO

FULL_PROVIDER_RESPONSE_LOG=FORBIDDEN
FULL_PROVIDER_RESPONSE_PERSIST=FORBIDDEN

IMPLEMENTATION_CHANGE_AUTHORIZED=NO
AUTHORIZATION_PR_WRITABLE_PATHS=governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md
AT5_PUBLIC_WRITABLE_PATHS=proof/nw008/nw-008-at5-ghl-rest-exact-synthetic-contact-live-read-execution-001.md

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
LIVE_GET_EXECUTED_UNDER_THIS_UNIT=NO
CREDENTIALS_LOADED_UNDER_THIS_UNIT=NO
HIGHLEVEL_ACCESSED_UNDER_THIS_UNIT=NO
PRIVATE_IDS_PUBLISHED_UNDER_THIS_UNIT=NO
```

## 12. Decision and stop

```text
BRANCH=governance/nw008-at4-exact-synthetic-contact-live-read-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md
CHANGED_PATHS=governance/authorizations/nw008-at4-ghl-rest-exact-synthetic-contact-live-read-authorization-001.md

GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

LIVE_READ_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_MUTATION_AUTHORIZED=NO
PRIVATE_BINDING_PUBLICATION=NO

NEXT=HUMAN_REVIEW_AND_MERGE_AUTHORIZATION_PR
STOP_CODE=NW008_AT4_EXACT_SYNTHETIC_CONTACT_LIVE_READ_AUTHORIZATION_READY_FOR_REVIEW
```

STOP. Return this authorization artifact for human review. Do not load
credentials, access HighLevel, perform the GET, or merge this PR from this
unit.
