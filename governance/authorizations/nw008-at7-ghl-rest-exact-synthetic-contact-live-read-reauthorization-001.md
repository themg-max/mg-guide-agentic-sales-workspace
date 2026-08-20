# NW-008 AT-7 — HighLevel REST Exact Synthetic Contact Live-Read Reauthorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT7_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_REAUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=governance/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md

PRIOR_AUTHORIZATION_PR=96
PRIOR_AUTHORIZATION_HEAD=bf0610ccdb9cd23fa3dcec36edec0ef9a6f3adb4
PRIOR_AUTHORIZATION_MERGE_SHA=0f4db30f470daa67b60a34a4c7ddf4878dbe5a26
PRIOR_AUTHORIZATION_CONSUMED=YES
PRIOR_AUTHORIZATION_REUSABLE=NO
PRIOR_AUTHORIZATION_TRANSFERABLE=NO
PRIOR_AUTHORIZATION_UNIT=NW008_AT4_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_AUTHORIZATION_001
PRIOR_AUTHORIZED_CONSUMER_UNIT=NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001

PRIOR_EXECUTION_PROOF_PR=97
PRIOR_EXECUTION_PROOF_HEAD=c89942d1aaf42100a345bb15da4cdb4749ae27fb
PRIOR_EXECUTION_PROOF_MERGE_SHA=5ceaee129e25887918ba57c38a217a062874ecbc
PRIOR_EXECUTION_RESULT=FAILED_CLOSED_PRE_NETWORK
PRIOR_EXECUTION_NETWORK_CALL_COUNT=0
PRIOR_EXECUTION_MUTATION_CALL_COUNT=0

CREDENTIAL_READINESS_UNIT=NW008_AT6_GHL_CREDENTIAL_PROVIDER_READINESS_001
SECRET_PROVIDER_READY=YES

SOURCE_IMPLEMENTATION_PR=95
SOURCE_IMPLEMENTATION_HEAD=43b4c6ae36ea8eb7a829da47731f702ac2823e58
SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52
BASE_REF=origin/main
BASE_SHA=5ceaee129e25887918ba57c38a217a062874ecbc

ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml
OFFLINE_IMPLEMENTATION_SOURCE=PR95_MERGED_NOTE_PATH
PRIOR_LIVE_READ_AUTHORIZATION_SOURCE=PR96_MERGED_AND_CONSUMED
PRIOR_LIVE_READ_EXECUTION_SOURCE=PR97_MERGED_FAILED_CLOSED_PRE_NETWORK

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE

GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

This artifact is a one-shot replacement authorization proposal only. Creating,
reviewing, or merging it does not load a credential, open a network socket,
access HighLevel, perform the authorized GET, perform any live read, perform any
mutation, publish private IDs, change implementation code, modify proof files, or
change deployment / IAM / secrets.

AT7 itself performs no credential access, HighLevel call, CRM read, or mutation.

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
   `NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002`
   verifies that merge (exact path on `origin/main` / merge ancestry) before
   performing the GET.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is not standing live-read authority, not live-mutation authority,
not note-path execution authority, not stage-path authority, and not a reusable
grant. It does not revive, transfer, or extend PR #96 authority.

## 2. Verified prerequisites and source authority

Preflight was run before this artifact was authored:

```text
pwd
/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace

git fetch origin

git branch --show-current
governance/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001

git rev-parse HEAD
5ceaee129e25887918ba57c38a217a062874ecbc

Working branch is not main
YES

origin/main contains PRIOR_EXECUTION_PROOF_MERGE_SHA (PR #97)
5ceaee129e25887918ba57c38a217a062874ecbc
YES

origin/main contains PRIOR_AUTHORIZATION_MERGE_SHA (PR #96)
0f4db30f470daa67b60a34a4c7ddf4878dbe5a26
YES

origin/main contains SOURCE_IMPLEMENTATION_MERGE_SHA (PR #95)
86d315379856102c7ee1a38e4c36c70c7560fe52
YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #97 merge commit | `5ceaee129e25887918ba57c38a217a062874ecbc` |
| PR #97 merge commit is reachable from `origin/main` | YES |
| PR #97 reviewed head | `c89942d1aaf42100a345bb15da4cdb4749ae27fb` |
| PR #97 reviewed head is an ancestor of `origin/main` | YES |
| PR #96 merge commit | `0f4db30f470daa67b60a34a4c7ddf4878dbe5a26` |
| PR #96 merge commit is reachable from `origin/main` | YES |
| PR #96 reviewed head | `bf0610ccdb9cd23fa3dcec36edec0ef9a6f3adb4` |
| PR #96 authorization consumed by AT5 | YES |
| PR #96 reusable / transferable | NO / NO |
| PR #95 merge commit is reachable from `origin/main` | YES |
| Architecture artifact present on base | YES |
| Contract artifact present on base | YES |
| Offline NOTE_PATH implementation present on base | YES |
| AT6 credential-provider readiness independently proven | YES |
| This unit executed a live GET | NO |
| This unit loaded credentials | NO |
| This unit accessed HighLevel | NO |

Bound durable source inputs (read-only for the future execution lane):

```text
ARCHITECTURE_ARTIFACT=docs/nw008/nw-008-at1-ghl-rest-adapter-architecture-001.md
CONTRACT_ARTIFACT=contracts/highlevel_rest_adapter_v1.yaml
SOURCE_IMPLEMENTATION_PR=95
SOURCE_IMPLEMENTATION_HEAD=43b4c6ae36ea8eb7a829da47731f702ac2823e58
SOURCE_IMPLEMENTATION_MERGE_SHA=86d315379856102c7ee1a38e4c36c70c7560fe52
PRIOR_AUTHORIZATION_PR=96
PRIOR_AUTHORIZATION_MERGE_SHA=0f4db30f470daa67b60a34a4c7ddf4878dbe5a26
PRIOR_EXECUTION_PROOF_PR=97
PRIOR_EXECUTION_PROOF_MERGE_SHA=5ceaee129e25887918ba57c38a217a062874ecbc
CREDENTIAL_READINESS_UNIT=NW008_AT6_GHL_CREDENTIAL_PROVIDER_READINESS_001
```

### 2.1 Prior authorization is consumed and non-reusable

```text
PRIOR_AUTHORIZATION_PR=96
PRIOR_AUTHORIZATION_CONSUMED=YES
PRIOR_AUTHORIZATION_REUSABLE=NO
PRIOR_AUTHORIZATION_TRANSFERABLE=NO
```

PR #96 authorized only
`NW008_AT5_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_001` once. AT5
consumed that authority and recorded durable fail-closed proof on `main` via
PR #97. PR #96 may not be reused, transferred, or cited by AT8 as live-read
authority. This AT7 artifact is a fresh one-shot replacement authorization, not
an amendment, extension, or transfer of PR #96.

### 2.2 Prior execution proof (PR #97)

```text
PRIOR_EXECUTION_PROOF_PR=97
PRIOR_EXECUTION_RESULT=FAILED_CLOSED_PRE_NETWORK
PRIOR_EXECUTION_NETWORK_CALL_COUNT=0
PRIOR_EXECUTION_MUTATION_CALL_COUNT=0
FAILURE_CLASS=CREDENTIAL_PROVIDER_AUTHENTICATION_UNAVAILABLE
EXACT_CONTACT_GET_EXECUTED=NO
FAIL_CLOSED=YES
```

AT5 loaded the private binding without publication, then failed closed before any
HighLevel request because the credential provider could not authenticate
non-interactively. Zero network calls and zero mutations were performed. That
outcome exhausts PR #96 authority and does not authorize a second attempt under
the same grant.

### 2.3 Credential-provider readiness (AT6) — independent of this unit

```text
CREDENTIAL_READINESS_UNIT=NW008_AT6_GHL_CREDENTIAL_PROVIDER_READINESS_001
GCLOUD_ACCOUNT_CLASS=MG_CONTROLLED_ACCOUNT
GCLOUD_PROJECT=ai-rolodex-to-crm

GCLOUD_ACCESS_TOKEN_MINT=PASS
SECRET_METADATA_ACCESS=PASS
SECRET_PAYLOAD_ACCESS=PASS
SECRET_PROVIDER_READY=YES

HIGHLEVEL_ACCESS_DURING_AT6=NO
CRM_NETWORK_CALLS_DURING_AT6=0
IAM_CHANGE_EXECUTED=NO
SECRET_MUTATION_EXECUTED=NO
CREDENTIAL_ROTATION_EXECUTED=NO
```

AT6 independently proved that the controlled credential provider can mint a
gcloud access token and read secret metadata and payload for the GHL secret in
project `ai-rolodex-to-crm`. AT6 did not access HighLevel, did not perform CRM
network calls, and did not change IAM, secrets, or credentials.

AT7 does not re-run AT6, does not load the GHL secret, and does not treat AT6 as
HighLevel live-read authority. AT6 readiness is a precondition for issuing this
replacement grant to AT8; it is not itself contact-GET authority.

PR #95 merged an offline-only NOTE_PATH adapter. That merge remains a
prerequisite for this live-read grant. It does not itself authorize network
access, credential use, live read, or live mutation. AT8 may not reinterpret
PR #95, PR #96, PR #97, or AT6 as live NOTE_PATH execution authority, note-create
authority, or stage-path authority.

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
appear in this artifact, in AT8 public proof, in logs committed to this
repository, or in the authorization PR body.

```text
PRIVATE_BINDING_VALUES_IN_THIS_ARTIFACT=FORBIDDEN
PRIVATE_BINDING_VALUES_IN_PUBLIC_PROOF=FORBIDDEN
CALLER_SUPPLIED_CONTACT_ID=FORBIDDEN
CALLER_SUPPLIED_LOCATION_ID=FORBIDDEN
AGENT_SUPPLIED_TARGET_OVERRIDE=FORBIDDEN
```

AT8 must fail closed if the private binding is missing, incomplete, or cannot
be loaded without publishing values into the public tree.

## 4. What this authorization permits

### 4.1 Named consumer and live authority

When the conditional grant is effective, only
`NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002` with
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

No other unit — including AT5, AT6, AT7, or any unnamed follow-on lane — may
consume this grant.

### 4.2 Authorized provider operation (exactly one)

```text
METHOD=GET
ROUTE=/contacts/{private_binding.contact_id}
API_VERSION=v3
EXPECTED_SCOPE=contacts.readonly
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

AT8 may use those two fields solely to prove that the privately bound synthetic
contact exists and that the returned location matches the private location
binding. No other provider field may be logged, persisted, copied into public
proof, or treated as authorization to continue into note or stage operations.

### 4.4 Execution budget

```text
CONTACT_GET_ATTEMPTS_MAX=1
NETWORK_CALL_COUNT_MAX=1
MUTATION_CALL_COUNT_MAX=0
AUTOMATIC_RETRY=NO
FALLBACK=NO
SECOND_GET=NO
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
NOTE_READBACK_AUTHORIZED=NO
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

AT8 may not search for a contact, list contacts, page through results, resolve
an “equivalent” synthetic record, or retry against a different ID if the bound
contact GET fails.

### 5.3 Credential, IAM, deployment, and implementation expansion

```text
CREDENTIAL_CREATE_AUTHORIZED=NO
CREDENTIAL_EXPAND_AUTHORIZED=NO
CREDENTIAL_ROTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
IAM_CHANGE_AUTHORIZED=NO
DEPLOYMENT_CHANGE_AUTHORIZED=NO
IMPLEMENTATION_CHANGE_AUTHORIZED=NO
CONTRACT_CHANGE_AUTHORIZED=NO
ARCHITECTURE_CHANGE_AUTHORIZED=NO
```

Credential use is authorized only as the minimum bearer / PIT required to
perform the exact contact GET. AT8 may not create, rotate, expand, or commit
credentials. AT7 may not load the GHL secret at all.

### 5.4 This authorization unit itself (AT7)

This AT7 unit must not:

- load the GHL secret;
- load credentials;
- call HighLevel;
- perform live reads;
- perform mutations;
- publish private IDs;
- change implementation code;
- modify proof files;
- change IAM;
- change secrets;
- rotate credentials;
- execute AT8.

## 6. Writable paths

### 6.1 This authorization PR (current unit)

This authorization-planning unit may write exactly one path:

```text
governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md
```

No adapter code, tests, fixtures, contracts, workflows, proof files, or deploy
assets may be created or modified in this unit.

### 6.2 Future AT8 execution-proof lane only

After the conditional grant is effective (exact artifact merged to `main` and
verified by the consumer), only
`NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002` may write
only a sanitized execution-proof artifact under:

```text
WRITABLE_EXECUTION_PROOF_PATHS=
proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md

IMPLEMENTATION_FILE_MANIFEST_REQUIRED=YES
PUBLIC_TREE_IMPLEMENTATION_CHANGE_AUTHORIZED=NO
```

AT8 may use a private runtime, private binding store, and existing credential
provider solely to issue the one authorized GET. Those private surfaces are not
writable paths in this public repository.

### 6.3 Explicitly non-writable for AT8

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

If AT8 discovers that a public-tree implementation change is required to
perform the GET, it must stop and return; it must not expand this grant into
an implementation PR.

## 7. Success conditions for future AT8

AT8 may claim success only when all of the following are true:

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

AT8 must fail closed, stop, and return terminal proof without retry, fallback,
second GET, or mutation if any of the following occur:

```text
credential retrieval failure
401
403
404
unexpected status
redirect
unexpected response schema
contact.id mismatch
contact.locationId mismatch
search/list/pagination attempt
alternate target attempt
query parameter attempt
missing private binding
missing credential
missing required scope
400
```

Additional terminal conditions:

```text
AUTHORIZATION_ARTIFACT_NOT_ON_MAIN
CONSUMER_UNIT_MISMATCH
GRANT_ALREADY_CONSUMED
PRIOR_AUTHORIZATION_PR96_CITED_AS_AUTHORITY
QUERY_PARAMETER_PRESENT
NON_GET_METHOD
NON_EXACT_CONTACT_ROUTE
FULL_PROVIDER_RESPONSE_WOULD_BE_PUBLISHED
CALLER_SUPPLIED_ID
```

On any terminal failure:

```text
AUTHORIZATION_CONSUMED=YES
STOP
NO RETRY
NO FALLBACK
NO SECOND GET
NO MUTATION
NETWORK_CALL_COUNT_MUST_NOT_INCREASE_AFTER_FAILURE
MUTATION_CALL_COUNT=0
EXTERNAL_MUTATIONS=0
```

## 9. Authorization consumption rules

```text
AUTHORIZED_CONSUMER_UNIT=NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002
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
PRIOR_AUTHORIZATION_PR96_REUSE=NO
```

### 9.1 Named consumer binding

Only unit `NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002`
with `AUTHORIZED_CONSUMER_PR_CLASS=execution_proof` may consume this grant. No
other unit, agent session, PR class, or follow-on lane may inherit it. AT5 may
not re-consume under this artifact. AT7 may not execute the GET.

### 9.2 Activation and verification

1. Before merge: `AUTHORIZATION_EFFECTIVE=NO` and `GRANT_STATUS=CONDITIONAL`.
2. Activation condition: the exact authorization artifact is merged to `main`
   by human authority (`GRANT_ACTIVATION=MERGE_TO_MAIN`).
3. AT8 must verify that merge (exact path present on `origin/main` and
   ancestry/merge evidence) before any live GET.
4. AT8 must verify that PR #96 remains consumed and is not cited as authority.
5. The artifact text is not required to mutate after merge
   (`ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO`).

### 9.3 One-shot, non-reuse, and expiry

`AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT`. The grant is not reusable and not
transferable:

```text
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
```

The authorization expires when any of the following occurs:

- AT8 completes the one authorized GET, successfully or fail-closed; or
- AT8 hits any terminal failure condition in §8 (including pre-network
  credential retrieval failure), which consumes the grant; or
- the authorization is explicitly revoked by a later governance artifact; or
- the source implementation, architecture, or contract is superseded before
  consumption.

After expiry, no further live call may cite this artifact as authority. A later
live note, live stage, or additional contact GET requires a new human
authorization.

### 9.4 Remaining consumption rules

1. Only AT8 may consume this grant, and only for the exact contact GET in §4.
2. A successful GET does not activate note create, note GET, opportunity GET,
   opportunity PUT, or STAGE_PATH.
3. AT8 must not change implementation code, contracts, architecture, deploy,
   IAM, or secrets in the public tree.
4. AT8 must not publish private binding values.
5. If AT8 cannot perform the GET within this bound, it must stop and return; it
   must not search, list, paginate, retarget, or mutate.
6. PR #96 remains consumed and may not be reused by AT8.

## 10. Authorization PR validation gate

This PR is class `authorization`. Before merge:

1. `git diff --check` is clean;
2. exactly one changed path, equal to:

   ```text
   governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md
   ```

3. no conflict markers;
4. no secrets, tokens, private record IDs, or credential material;
5. `PRIOR_EXECUTION_PROOF_MERGE_SHA=5ceaee129e25887918ba57c38a217a062874ecbc`
   (PR #97) is reachable from `origin/main`;
6. `PRIOR_AUTHORIZATION_MERGE_SHA=0f4db30f470daa67b60a34a4c7ddf4878dbe5a26`
   (PR #96) is reachable from `origin/main` and asserted consumed;
7. AT6 credential-provider readiness assertion holds
   (`SECRET_PROVIDER_READY=YES`; no HighLevel access during AT6);
8. named consumer assertion names AT8 only
   (`NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002`);
9. one-shot / non-reuse assertions hold;
10. exact-GET-only assertion holds;
11. mutation denial assertions hold;
12. search / list / pagination denial assertions hold;
13. `PRIVATE_BINDING_PUBLICATION=NO` holds;
14. AT7 itself performs no credential access, HighLevel call, CRM read, or
    mutation;
15. repository-required deterministic validation / exact-head checks as required
    by project governance;
16. clean mergeability into `main`;
17. human review and human merge authority.

AT8 must not proceed from an open or unmerged authorization PR. Any push
changes the exact head and requires re-validation and human review.

## 11. Authorization state assertions

```text
PR_CLASS=authorization
UNIT=NW008_AT7_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_REAUTHORIZATION_001
MODE=AUTHORIZATION_ARTIFACT_ONLY
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md

PRIOR_AUTHORIZATION_PR=96
PRIOR_AUTHORIZATION_CONSUMED=YES
PRIOR_AUTHORIZATION_REUSABLE=NO
PRIOR_AUTHORIZATION_TRANSFERABLE=NO

PRIOR_EXECUTION_PROOF_PR=97
PRIOR_EXECUTION_RESULT=FAILED_CLOSED_PRE_NETWORK
PRIOR_EXECUTION_NETWORK_CALL_COUNT=0
PRIOR_EXECUTION_MUTATION_CALL_COUNT=0

CREDENTIAL_READINESS_UNIT=NW008_AT6_GHL_CREDENTIAL_PROVIDER_READINESS_001
SECRET_PROVIDER_READY=YES
CREDENTIAL_PROVIDER_READY=YES
HIGHLEVEL_ACCESS_DURING_AT6=NO

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

AUTHORIZED_CONSUMER_UNIT=NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002
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
CALLER_SUPPLIED_CONTACT_ID=FORBIDDEN
CALLER_SUPPLIED_LOCATION_ID=FORBIDDEN
AGENT_SUPPLIED_TARGET_OVERRIDE=FORBIDDEN

NETWORK_ACCESS_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
CREDENTIAL_USE_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_READ_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_MUTATION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
NOTE_CREATE_AUTHORIZED=NO
NOTE_GET_AUTHORIZED=NO
NOTE_POST_AUTHORIZED=NO
NOTE_READBACK_AUTHORIZED=NO
OPPORTUNITY_GET_AUTHORIZED=NO
OPPORTUNITY_PUT_AUTHORIZED=NO
STAGE_PATH_AUTHORIZED=NO

AUTHORIZED_PROVIDER_OPERATION=GET /contacts/{private_binding.contact_id}
API_VERSION=v3
EXPECTED_SCOPE=contacts.readonly
QUERY_PARAMETERS=NO
REDIRECT_FOLLOWING=NO
PURPOSE=VERIFY_EXACT_SYNTHETIC_CONTACT_BINDING
RESPONSE_FIELDS_CONSUMED_ONLY=contact.id,contact.locationId
CONTACT_GET_ATTEMPTS_MAX=1
NETWORK_CALL_COUNT_MAX=1
MUTATION_CALL_COUNT_MAX=0
AUTOMATIC_RETRY=NO
FALLBACK=NO
SECOND_GET=NO
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

IAM_CHANGE_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
CREDENTIAL_ROTATION_AUTHORIZED=NO
IMPLEMENTATION_CHANGE_AUTHORIZED=NO

AUTHORIZATION_PR_WRITABLE_PATHS=governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md
AT8_PUBLIC_WRITABLE_PATHS=proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
LIVE_GET_EXECUTED_UNDER_THIS_UNIT=NO
CREDENTIALS_LOADED_UNDER_THIS_UNIT=NO
HIGHLEVEL_ACCESSED_UNDER_THIS_UNIT=NO
CRM_READ_EXECUTED_UNDER_THIS_UNIT=NO
MUTATION_EXECUTED_UNDER_THIS_UNIT=NO
PRIVATE_IDS_PUBLISHED_UNDER_THIS_UNIT=NO
```

## 12. Decision and stop

```text
BRANCH=governance/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md
CHANGED_PATHS=governance/authorizations/nw008-at7-ghl-rest-exact-synthetic-contact-live-read-reauthorization-001.md

PRIOR_AUTHORIZATION_CONSUMED=YES
CREDENTIAL_PROVIDER_READY=YES

GRANT=GHL_EXACT_SYNTHETIC_CONTACT_LIVE_READ
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002
AUTHORIZED_CONSUMER_PR_CLASS=execution_proof
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

LIVE_READ_AUTHORIZED=YES_FOR_EXACT_CONTACT_GET_ONLY
LIVE_MUTATION_AUTHORIZED=NO
PRIVATE_BINDING_PUBLICATION=NO

NEXT=HUMAN_REVIEW_AND_MERGE_AUTHORIZATION_PR
STOP_CODE=NW008_AT7_EXACT_SYNTHETIC_CONTACT_LIVE_READ_REAUTHORIZATION_READY_FOR_REVIEW
```

STOP. Return this authorization artifact for human review. Do not load
credentials, access HighLevel, perform the GET, execute AT8, or merge this PR
from this unit.
