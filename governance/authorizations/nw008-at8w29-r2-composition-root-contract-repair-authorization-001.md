# NW-008 AT8W29 R2 Composition-Root Contract Repair Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W29_R2_COMPOSITION_ROOT_CONTRACT_REPAIR_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

SOURCE_REVIEW_PR=208
SOURCE_REVIEWED_HEAD=da0eca0da8c5ddbadbadfeaa910096c50d7b7203
SOURCE_REVIEW_DISPOSITION=CHANGE_REQUEST
R1B_GATE_COMPLETE=YES

R2_AUTHORIZATION_CURRENT_STATE=PROPOSED_NOT_EFFECTIVE
R2_EXECUTION_AUTHORIZED=NO
R3_AUTHORIZED=NO
R4_AUTHORIZED=NO

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w29-r2-composition-root-contract-repair-authorization-001.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w29-r2-composition-root-contract-repair-authorization-001

GRANT_ACTIVATION=HUMAN_MERGE_TO_MAIN
ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
SELF_ACTIVATION=FORBIDDEN

AUTHORIZED_CONSUMER_UNIT=
  NW008_AT8W29_R2_COMPOSITION_ROOT_CONTRACT_REPAIR_IMPLEMENTATION_001
IMPLEMENTATION_EXECUTION_BEFORE_MERGE=FORBIDDEN
```

This artifact is authorization authoring only. It becomes effective only when a
human merges this exact artifact to `main`. Creation, review, CI, or approval of
the authorization PR does not activate the grant. After activation, only the
named consumer unit may consume it, once, for the bounded repo-local source and
offline-test repair defined below.

This authorization does not authorize R2 execution or any R3/R4 activity.

## 2. Authoring-unit zero-effect attestation

```text
EXECUTION_PERFORMED=NO
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
SECRET_PAYLOAD_READS=0
SQLITE_OPENED=NO
SQLITE_CREATED=NO
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

PRODUCTION_RUNTIME_EXECUTED=NO
ASSEMBLE_BOUND_LIVE_NOTE_RUNTIME_CALLED=NO
LIVE_SECRET_MANAGER_CLIENTS_INSTANTIATED=0
AT1_EXECUTION_STORE_CONSTRUCTIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
```

No production runtime, credential, secret, SQLite, HighLevel, HTTP, CRM, IAM,
or deployment operation was performed while authoring this artifact.

## 3. Source-only preflight basis

The preflight fetched `origin/main` without tags and inspected the exact source
objects at the following commit:

```text
SOURCE_PREFLIGHT_REF=origin/main
SOURCE_MAIN_SHA=f5ec221a667db91e43684f3acad98913b6e00bfa
SOURCE_PREFLIGHT_EFFECTS=READ_ONLY
```

Exact production files inspected:

```text
src/integrations/ghl/highlevel_rest/live_note_runtime.py
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
src/integrations/ghl/at1_commitment_key_provider.py
src/integrations/ghl/at1_execution_store.py
```

Exact existing test files located by concern:

```text
LIVE_NOTE_RUNTIME_ASSEMBLY_TEST=
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py

LIVE_NOTE_CREDENTIAL_PROVIDER_TEST=
  tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py

COMMITMENT_KEY_PROVIDER_TEST=
  tests/integrations/ghl/test_at1_commitment_key_provider.py

EXECUTION_STORE_LIFECYCLE_TEST=
  tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
```

The source inspection found:

1. production composition constructs the C4 commitment-key provider and B2
   live-note accessor independently, allowing each to create a Secret Manager
   client through implicit default credential resolution;
2. both provider classes already support injection of a client, so neither
   provider implementation requires mutation for the minimum repair;
3. `At1ExecutionStore` opens its SQLite connection during construction and
   closes it only on its own schema-initialization error;
4. after successful store construction, B2 acquisition and HTTP client,
   transport, or adapter construction can still fail before an adapter is
   returned; and
5. the composition root can implement a private ownership guard around the
   existing store connection, so no public store API redesign or
   `at1_execution_store.py` mutation is required.

```text
GAP1_CREDENTIAL_OWNERSHIP_REPAIR_DESIGNABLE=YES
GAP2_STORE_LIFECYCLE_REPAIR_DESIGNABLE=YES
AT1_EXECUTION_STORE_SOURCE_CHANGE_REQUIRED=NO
```

## 4. Bounded implementation purpose

After activation, this grant authorizes only the minimum source and test
mutations necessary to close both pre-execution production-composition contract
gaps:

1. establish explicit composition-root ownership of one short-lived target
   runtime service-account credential object and one Secret Manager client
   shared by C4 and B2; and
2. guarantee exactly one deterministic store close on every failure after
   successful store construction and before successful adapter return, while
   transferring store ownership without closing it on success.

No other behavior, cleanup, refactor, or remediation is authorized.

## 5. Gap 1: explicit runtime credential and client ownership

### 5.1 Required invariant

```text
RUNTIME_CREDENTIAL_OWNERSHIP=ROOT_OWNED
TARGET_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SHARED_TARGET_RUNTIME_CREDENTIAL_OBJECT_REQUIRED=YES
SHARED_SECRET_MANAGER_CLIENT_REQUIRED=YES
C4_AND_B2_USE_SAME_ROOT_OWNED_SECRET_MANAGER_CLIENT=YES

DIRECT_USER_ADC_SECRET_ACCESS_ALLOWED=NO
CALLER_SUPPLIED_RUNTIME_PRINCIPAL_ALLOWED=NO
CALLER_SUPPLIED_SECRET_MANAGER_CLIENT_ALLOWED=NO
USER_MANAGED_SERVICE_ACCOUNT_KEY_ALLOWED=NO
```

The production composition root must explicitly perform this dependency
construction:

```text
source ADC
  -> one short-lived impersonated credential object for the exact target runtime SA
  -> one root-owned SecretManagerServiceClient(credentials=<same credential object>)
  -> GoogleSecretManagerCommitmentKeyProvider(client=<same client object>)
  -> GoogleSecretManagerLiveNoteSecretAccessor(client=<same client object>)
```

The source ADC may be used only as the source credential for constructing the
target-SA impersonated credential. It must never be supplied to a Secret
Manager client and must never directly read C4 or B2. The public production
assembler must not accept a principal, credential, or Secret Manager client
from its caller.

The composition must retain exact-version resource sealing:

```text
EXACT_C4_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

EXACT_B2_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1
```

Alternate principals, user-managed service-account keys, secret discovery,
version discovery, `latest`, retries, caller-selected clients, caller-selected
credentials, and direct user-ADC Secret Manager reads are forbidden.

### 5.2 Resolved minimum design

```text
SHARED_RUNTIME_CREDENTIAL_OBJECT_DESIGN=
  The production composition root creates exactly one short-lived impersonated
  credential object for the sealed target runtime service account from source
  ADC and retains ownership of that object; no caller injection surface is
  added.

SHARED_SECRET_MANAGER_CLIENT_DESIGN=
  The production composition root constructs exactly one
  SecretManagerServiceClient with that exact impersonated credential object
  and passes the same client object by identity to both the C4 provider and B2
  accessor.
```

Factory/import seams used to prove object identity must remain private/internal.
They may exist only to support deterministic fakes and must not create a public
caller override.

## 6. Gap 2: execution-store lifecycle ownership

### 6.1 Required invariant

```text
IF_AT1_EXECUTION_STORE_CONSTRUCTED=YES
AND_NOTE_PATH_ADAPTER_SUCCESSFULLY_RETURNED=NO
THEN_STORE_CONNECTION_CLOSED_BY_COMPOSITION_ROOT=YES

IF_NOTE_PATH_ADAPTER_SUCCESSFULLY_RETURNED=YES
THEN_STORE_OWNERSHIP_TRANSFERRED_TO_RETURNED_OBJECT_GRAPH=YES
```

The composition root owns the store from successful construction until the
fully bound `NotePathAdapter` is successfully returned. Every exception or
other unsuccessful exit after store construction and before return must close
the store exactly once.

The repair must not reopen the store, construct a replacement database, repair
the database, delete/recreate the database, invoke a business method, or create
protocol/business writes. Successful assembly must not close the store.

### 6.2 Resolved minimum design

```text
POST_STORE_FAILURE_CLOSE_GUARANTEE_DESIGN=
  A private composition-root ownership guard holds the constructed store,
  closes its existing connection exactly once in a finally-based failure path,
  and remains responsible through B2 acquisition, HTTP client construction,
  transport construction, adapter construction, and final adapter binding.

SUCCESSFUL_STORE_OWNERSHIP_TRANSFER_DESIGN=
  Only immediately before successful adapter return does the private guard
  release root ownership to the returned object graph; release performs no
  close, and the adapter-bound store remains open for its later owner.
```

The guard must be stateful enough to prevent a duplicate close and must not
swallow or replace the original composition failure. A public
`At1ExecutionStore` API redesign is not authorized because source inspection
proved a smaller private composition-root repair viable.

## 7. Exact writable scope

### 7.1 Production source

The only authorized production source path is:

```text
PRIMARY_SOURCE_PATH=
  src/integrations/ghl/highlevel_rest/live_note_runtime.py

CONDITIONAL_SOURCE_PATHS=NONE
```

The following inspected paths are explicitly read-only under this grant:

```text
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
src/integrations/ghl/at1_commitment_key_provider.py
src/integrations/ghl/at1_execution_store.py
```

If a future implementer believes any read-only path must change, this grant
fails closed. The implementer must stop and obtain a new or amended
human-merged authorization that records the exact objective reason. This grant
does not permit the implementer to expand scope unilaterally.

### 7.2 Tests

Only these exact existing test files may be modified:

```text
tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py
tests/integrations/ghl/test_at1_commitment_key_provider.py
tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
```

No blanket `tests/**` authority is granted. A narrowly named new test file is
permitted only if the existing runtime test file cannot express a required
contract without materially unrelated coupling. Before creating it, the future
implementation proof must record the exact reason and path. New test helpers
must be synthetic and offline.

### 7.3 Future proof artifact

The future implementation unit may create only this proof artifact in addition
to the source and test paths above:

```text
PROOF_ARTIFACT=
  proof/nw008/at-8w29/nw008-at8w29-r2-composition-root-contract-repair-implementation-proof-001.md
```

## 8. Required offline deterministic test contract

All tests must use synthetic/fake dependencies. They must not obtain real
credentials, instantiate a live Secret Manager client, impersonate a service
account, mint a token, access IAM, access a network, or open/create live
SQLite.

### 8.1 Identity contract

Tests must prove object identity, not merely equivalent configuration:

```text
SHARED_TARGET_RUNTIME_CREDENTIAL_OBJECT=YES
SHARED_SECRET_MANAGER_CLIENT=YES
C4_PROVIDER_RECEIVES_SHARED_CLIENT=YES
B2_ACCESSOR_RECEIVES_SHARED_CLIENT=YES
DIRECT_USER_ADC_SECRET_ACCESS=NO
```

The fake source credential, fake impersonated credential, fake Secret Manager
client factory, fake C4 provider, and fake B2 accessor must make the selected
principal and exact object references inspectable. Tests must prove no implicit
default client path is used.

### 8.2 Lifecycle contract

```text
CASE_B2_SECRET_ACQUISITION_FAILURE:
  STORE_OPENED=YES
  ADAPTER_RETURNED=NO
  STORE_CLOSE_EVENTS=1

CASE_HTTP_CLIENT_CONSTRUCTION_FAILURE:
  STORE_OPENED=YES
  ADAPTER_RETURNED=NO
  STORE_CLOSE_EVENTS=1

CASE_TRANSPORT_CONSTRUCTION_FAILURE:
  STORE_OPENED=YES
  ADAPTER_RETURNED=NO
  STORE_CLOSE_EVENTS=1

CASE_ADAPTER_CONSTRUCTION_FAILURE:
  STORE_OPENED=YES
  ADAPTER_RETURNED=NO
  STORE_CLOSE_EVENTS=1

CASE_SUCCESS:
  ADAPTER_RETURNED=YES
  STORE_PREMATURELY_CLOSED=NO
  EXECUTION_STORE_BOUND=YES
```

Every case must additionally prove:

```text
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
EXECUTION_CLAIMS_CREATED=0
ATTEMPT_RECORDS_CREATED=0
PROTOCOL_LEDGER_EVENT_WRITES=0
BUSINESS_LEDGER_EVENT_WRITES=0
```

Failure-path assertions must count close events directly. Success assertions
must prove the exact store object is bound into the returned graph and has not
been closed.

## 9. Offline-only authority and blocked surfaces

This authorization covers repo-local implementation and offline deterministic
tests only after human merge.

```text
LIVE_CLOUD_EXECUTION_AUTHORIZED=NO
LIVE_SECRET_READ_AUTHORIZED=NO
SERVICE_ACCOUNT_IMPERSONATION_AUTHORIZED=NO
TOKEN_MINT_AUTHORIZED=NO
SQLITE_LIVE_OPEN_AUTHORIZED=NO
HIGHLEVEL_CALL_AUTHORIZED=NO
HTTP_REQUEST_DISPATCH_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
R2_EXECUTION_AUTHORIZED=NO
```

Blocked paths and surfaces include:

```text
.github/workflows/**
deploy/**
infra/**
contracts/**
unrelated documentation
unrelated proof
HighLevel business logic
stage-transition logic
note-write behavior
CRM workflows
IAM policy
secret resources
production/customer data
```

Also forbidden:

- calling `assemble_bound_live_note_runtime` against production dependencies;
- executing production runtime;
- accessing Secret Manager or IAM;
- impersonating any service account or minting any token;
- opening or creating SQLite outside synthetic offline test isolation;
- dispatching HTTP or calling HighLevel;
- mutating CRM, IAM, secret resources, or service-account keys;
- deploying or merging any PR autonomously; and
- using this grant as authority for R2, R3, or R4 execution.

## 10. Fail-closed implementation rules

The future consumer must stop without implementation or authority expansion if:

1. this exact artifact is not present on `main`;
2. the consumer unit identity does not exactly match the authorized unit;
3. the grant was already consumed;
4. a required mutation falls outside the exact writable scope;
5. either exact secret version or the target service account would change;
6. a caller-selected principal, credential, or client would be exposed;
7. a test would require real credentials, Secret Manager, IAM, network, or live
   SQLite;
8. a lifecycle failure cannot be proved to close exactly once;
9. successful assembly cannot be proved to transfer the exact open store; or
10. any blocked surface or live effect would be required.

Failure does not authorize retries, fallback credentials, alternate principals,
secret/version discovery, replacement databases, database repair, or broader
source changes.

## 11. Required future implementation proof

The implementation PR must produce the exact proof artifact named in section
7.3 and include at least:

```text
UNIT=NW008_AT8W29_R2_COMPOSITION_ROOT_CONTRACT_REPAIR_IMPLEMENTATION_001
AUTHORIZATION_CONSUMED=
  governance/authorizations/nw008-at8w29-r2-composition-root-contract-repair-authorization-001.md
AUTHORIZATION_ON_MAIN=YES

CREDENTIAL_OWNERSHIP_REPAIR=PASS
SHARED_RUNTIME_CREDENTIAL_OBJECT=YES
SHARED_SECRET_MANAGER_CLIENT=YES
C4_AND_B2_SHARED_CLIENT=YES

STORE_LIFECYCLE_REPAIR=PASS
POST_STORE_FAILURE_CLOSE_GUARANTEE=YES
SUCCESSFUL_STORE_OWNERSHIP_TRANSFER=YES

LIVE_SECRET_READS=0
TOKEN_MINTS=0
SQLITE_LIVE_OPENS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

DETERMINISTIC_TESTS=PASS
R2_EXECUTION_PERFORMED=NO
```

The proof must name every changed path, record the deterministic test command
and result, and attest that no production assembler invocation or live effect
occurred. It must not contain credentials, tokens, secret payloads, user
identity, customer data, or sensitive environment values.

## 12. CI and disposition boundary

The authorization PR must target `main` and receive exact-head canonical Phase
1 deterministic validation. A stale, superseded, or non-exact-head result does
not satisfy this requirement.

```text
REQUIRED_CANONICAL_CI=Phase 1 deterministic validation
REQUIRED_CI_HEAD_BINDING=EXACT_AUTHORIZATION_HEAD_SHA
AUTONOMOUS_MERGE_ALLOWED=NO
HUMAN_REVIEW_REQUIRED=YES
INDEPENDENT_REVIEW_REQUIRED=YES
```

After the authorization PR is opened and canonical CI is observed, work stops.
The PR must be returned for independent reviewer disposition. No repair may be
implemented in this unit.

## 13. Final authority statement

This one-shot, non-reusable, non-transferable grant authorizes only the named
future consumer, only after human merge to `main`, to make the exact bounded
repo-local production-composition repair and offline deterministic tests
defined here. It grants zero live-cloud authority and no R2/R3/R4 execution
authority.
