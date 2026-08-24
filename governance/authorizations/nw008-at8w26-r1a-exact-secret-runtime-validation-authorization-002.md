# NW-008 AT8W26 R1A Exact-Secret Runtime Validation Authorization 002

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W26_R1A_EXACT_SECRET_RUNTIME_VALIDATION_AUTHORIZATION_002
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-002.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-002

BASE_REF=origin/main
BASE_SHA=
  cd40d699601803c1a8dac169e5b52a72900b3745

SUPERSEDES_AUTHORIZATION=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-001.md
SUPERSESSION_REASON=
  ALIGN_R1A_WITH_DURABLE_RUNTIME_IDENTITY_MECHANISM

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=HUMAN_MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
```

This artifact is planning-only. Creating, reviewing, or merging it does not
impersonate a service account, mint a token, read a Secret Manager payload,
open SQLite, call HighLevel, mutate CRM or IAM, or start production runtime.

The bounded grant becomes usable only after human review and merge places this
exact artifact on `main`, followed by independent verification by the sole
authorized execution consumer.

```text
EXECUTION_PERFORMED_IN_THIS_UNIT=NO
SERVICE_ACCOUNT_IMPERSONATION_IN_THIS_UNIT=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_IN_THIS_UNIT=0
SECRET_MANAGER_ACCESS_PERFORMED_IN_THIS_UNIT=NO
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
HIGHLEVEL_CALLS_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
SQLITE_CREATION_IN_THIS_UNIT=0
SQLITE_OPEN_IN_THIS_UNIT=0
IAM_MUTATIONS_IN_THIS_UNIT=0
DEPLOYMENTS_IN_THIS_UNIT=0
AUTHORIZATION_CONSUMED_IN_THIS_UNIT=NO
```

## 2. Supersession of authorization 001

```text
SUPERSEDES_AUTHORIZATION=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-001.md

SUPERSESSION_REASON=
  ALIGN_R1A_WITH_DURABLE_RUNTIME_IDENTITY_MECHANISM

PR201_STATE=MERGED
PR201_MERGE_COMMIT=
  cd40d699601803c1a8dac169e5b52a72900b3745
PR201_REVIEWED_HEAD=
  7d05c98facbc699b2d723f8fccc8a47ab562700c
PR201_AUTHORIZATION_PRESENT_ON_ORIGIN_MAIN=YES

PR201_AUTHORIZATION_CONSUMED_BEFORE_SUPERSESSION=NO
AUTHORIZATION_001_EXECUTION_PERFORMED=NO
AUTHORIZATION_001_SECRET_PAYLOAD_READS=0
AUTHORIZATION_001_IMPERSONATION_ATTEMPTS=0
AUTHORIZATION_001_TOKEN_MINTS=0

AUTHORIZATION_001_EXECUTION_ALLOWED_AFTER_002_MERGE=NO
AUTHORIZATION_001_STATUS_AFTER_002_MERGE=SUPERSEDED_NOT_EXECUTABLE
```

Authorization 001 remains historically durable on `main` as the first R1A
grant proposal and merge record. It was never consumed by an execution unit.
After human merge of this exact authorization 002 artifact, authorization 001
must not be used as execution authority. The sole executable R1A grant is this
authorization 002.

## 3. Purpose and explicit non-authority

This artifact conditionally authorizes one later bounded validation that:

1. obtains at most one short-lived access token for the already-governed
   production runtime service account via local operator ADC impersonation; and
2. uses that token only to attempt the exact two Secret Manager version reads
   already designated and implemented by AT8W25.

```text
PURPOSE=
  ONE_BOUNDED_LIVE_RUNTIME_DEPENDENCY_VALIDATION_OF_TWO_EXACT_SECRET_VERSIONS
  UNDER_DURABLE_RUNTIME_SERVICE_ACCOUNT_IMPERSONATION

PRODUCTION_RUNTIME_EXECUTION_AUTHORIZED=NO
HIGHLEVEL_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
SQLITE_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATE_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
STANDING_TOKEN_AUTHORITY=NO
```

A successful R1A proves only exact-secret accessibility under the bound
runtime principal and identity mechanism. It does not authorize production
runtime start, HighLevel, CRM, SQLite, IAM mutation, key creation, deployment,
or any later gate (R1B/R2/R3/R4).

## 4. Durable source prerequisites

```text
SOURCE_IMPLEMENTATION_PR=200
SOURCE_IMPLEMENTATION_MERGE=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
SOURCE_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w25/nw008-at8w25-b2-c4-c3-c2-offline-implementation-proof-001.md
SOURCE_IMPLEMENTATION_PROOF_ON_ORIGIN_MAIN=YES

SOURCE_AUTHORIZATION_001_PR=201
SOURCE_AUTHORIZATION_001_MERGE=
  cd40d699601803c1a8dac169e5b52a72900b3745
SOURCE_AUTHORIZATION_001_ON_ORIGIN_MAIN=YES
SOURCE_AUTHORIZATION_001_CONSUMED=NO

B2_IMPLEMENTATION_DURABLE=YES
C4_IMPLEMENTATION_DURABLE=YES
C3_IMPLEMENTATION_DURABLE=YES
C2_IMPLEMENTATION_DURABLE=YES
GOOGLE_CLOUD_SECRET_MANAGER_VERSION=2.27.0
```

The offline implementation and authorization 001 remain source context. They
do not authorize execution after this superseding grant merges.

## 5. Identity binding

```text
TARGET_RUNTIME_PRINCIPAL=
  serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

TARGET_RUNTIME_SERVICE_ACCOUNT_EMAIL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SOURCE_PRINCIPAL_CLASS=
  HUMAN_OPERATOR_USER_ADC

SOURCE_PRINCIPAL_PRIVATE_ATTESTATION_REF=
  NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af

DO_NOT_PUBLISH_SOURCE_PRINCIPAL=YES
SOURCE_PRINCIPAL_PUBLICATION_ALLOWED=NO
SOURCE_PRINCIPAL_PERSISTENCE_ALLOWED=NO

IDENTITY_MECHANISM=
  LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION

CALLER_SUPPLIED_RUNTIME_IDENTITY_OVERRIDE=FORBIDDEN
USER_MANAGED_SERVICE_ACCOUNT_KEY=FORBIDDEN
DIRECT_USER_ADC_AS_SECRET_ACCESS_PRINCIPAL=FORBIDDEN
```

The execution consumer must authenticate Secret Manager only as the exact
target runtime service account, obtained solely through short-lived
impersonation from the operator's local user ADC. The consumer must not:

- publish or persist the operator principal identity;
- use a user-managed service-account key;
- use direct user ADC as the Secret Manager access principal;
- accept a caller-supplied runtime identity override; or
- impersonate any principal other than the exact target runtime SA above.

Proof may reference only the opaque attestation ref
`NW008-ID-ATT-18bfa765-fdbe-4cf7-8b35-9f8518a4d0af` for the source principal
class, not the human operator email or other identifying material.

## 6. Identity effect budget

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS_MAX=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS_MAX=1

IAM_MUTATIONS_MAX=0
IAM_POLICY_WRITES_MAX=0
SERVICE_ACCOUNT_KEY_CREATE_MAX=0

TOKEN_LOGGING_ALLOWED=NO
TOKEN_PERSISTENCE_ALLOWED=NO
TOKEN_HASHING_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
TOKEN_STDOUT_STDERR_ALLOWED=NO

TOKEN_USE_SCOPE=
  R1A_EXACT_TWO_SECRET_READS_ONLY

TOKEN_REUSE_AFTER_R1A=FORBIDDEN
SECOND_TOKEN_MINT_OR_REFRESH=FORBIDDEN
TOKEN_LIFETIME=SHORT_LIVED_MINIMUM_NECESSARY
```

Exactly one impersonation attempt and exactly one short-lived access-token mint
are permitted for the exact target runtime SA. The token may be used only for
the B2 then C4 exact secret reads in this unit. After R1A ends (success or
fail-closed stop), the token must not be reused, refreshed, logged, persisted,
hashed for proof, or captured in fragments.

## 7. Exact secret resources and secret effect budget

Exactly two Secret Manager resources are permitted:

```text
B2_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1

C4_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

PERMITTED_SECRET_RESOURCE_COUNT=2
OTHER_SECRET_RESOURCES_PERMITTED=NO
```

```text
B2_SECRET_READ_ATTEMPTS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
TOTAL_SECRET_READ_ATTEMPTS_MAX=2

EXECUTION_ORDER=B2_THEN_C4
B2_RETRIES_MAX=0
C4_RETRIES_MAX=0

SECRET_LIST_CALLS_MAX=0
SECRET_VERSION_LIST_CALLS_MAX=0
SECRET_METADATA_DISCOVERY_CALLS_MAX=0

LATEST_ALLOWED=NO
ALIAS_RESOLUTION_ALLOWED=NO
VERSION_DISCOVERY_ALLOWED=NO
SECRET_DISCOVERY_ALLOWED=NO
CALLER_RESOURCE_OVERRIDE_ALLOWED=NO
```

The exact resource strings above are normative. The consumer may not substitute
project number/id forms, change secret names, change numeric versions, use
`latest`, resolve aliases, list secrets/versions, discover alternatives, accept
caller overrides, or retry either read.

## 8. Other forbidden effects

```text
HIGHLEVEL_CALLS_MAX=0
CRM_MUTATIONS_MAX=0

SQLITE_OPEN_MAX=0
SQLITE_CREATION_MAX=0

DEPLOYMENTS_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0
```

## 9. Payload and identity privacy

```text
PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_MINIMUM_LIFETIME_REQUIRED=YES
PAYLOAD_PUBLISHED_ALLOWED=NO
PAYLOAD_PERSISTED_ALLOWED=NO
PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
```

Forbidden disclosures include:

- stdout/stderr payload or token printing;
- file, repository, database, log, telemetry, or proof persistence of payload
  or token material;
- payload or token hashing for proof;
- payload length as proof;
- token or credential fragments;
- screenshots containing payload or token material;
- shell history or command arguments containing payload or token material;
- exception messages/tracebacks containing payload or token material;
- publication of the operator source principal identity.

Proof may record only:

```text
PERMITTED_PROOF_FIELDS=
  authorization_artifact_identity|
  opaque_source_principal_attestation_reference|
  target_runtime_service_account_resource|
  impersonation_attempt_count|
  token_mint_count|
  exact_secret_resource_identifiers|
  read_attempt_counts|
  success_or_failure|
  safe_sanitized_error_category|
  forbidden_effect_zero_ledger
```

## 10. Authorized consumer and one-shot semantics

```text
AUTHORIZED_CONSUMER_UNIT=
  NW008_AT8W26_R1A_EXACT_SECRET_RUNTIME_VALIDATION_EXECUTION_001
AUTHORIZED_CONSUMER_CLASS=execution_proof

ONE_SHOT=YES
REUSABLE=NO
TRANSFERABLE=NO
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_CONSUMPTION_RECORD_REQUIRED=YES
AUTHORIZATION_ARTIFACT_MUTABLE_BY_CONSUMER=NO

AUTHORIZATION_STATE_BEFORE_EXECUTION=
  AVAILABLE_IF_MERGED_AND_VERIFIED
AUTHORIZATION_STATE_ON_FIRST_IMPERSONATION_ATTEMPT=
  CONSUMED
AUTHORIZATION_STATE_AFTER_FIRST_IMPERSONATION_ATTEMPT=
  CONSUMED
FAILURE_RESTORES_AUTHORITY=NO
```

The grant is consumed when the future execution consumer begins the first
service-account impersonation attempt, regardless of success or failure.
Failure does not restore the grant. No other unit may consume or inherit it.
Authorization 001 must not be consumed after this grant merges.

Before the first impersonation attempt, the execution consumer must
independently verify:

```text
PRE_EXECUTION_REQUIRED=
  EXACT_AUTHORIZATION_002_ARTIFACT_MERGED_TO_MAIN|
  EXACT_AUTHORIZATION_002_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  AUTHORIZATION_001_SUPERSEDED_AND_NOT_EXECUTABLE|
  SOURCE_IMPLEMENTATION_MERGE_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_IMPLEMENTATION_PROOF_PRESENT_ON_ORIGIN_MAIN|
  EXACT_TARGET_RUNTIME_PRINCIPAL_MATCH|
  EXACT_IDENTITY_MECHANISM_MATCH|
  EXACT_B2_RESOURCE_MATCH|
  EXACT_C4_RESOURCE_MATCH|
  IDENTITY_AND_SECRET_EFFECT_BUDGETS_ENFORCED|
  PAYLOAD_AND_TOKEN_NON_DISCLOSURE_ENFORCED
```

## 11. Success condition

R1A succeeds only if all of the following hold within the fixed budgets and
with zero forbidden effects or disclosures:

```text
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=1
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=1

B2_EXACT_SECRET_ACCESS=PASS
C4_EXACT_SECRET_ACCESS=PASS

B2_READ_ATTEMPTS=1
C4_READ_ATTEMPTS=1

PAYLOADS_PUBLISHED=NO
PAYLOADS_PERSISTED=NO
TOKENS_PUBLISHED=NO
TOKENS_PERSISTED=NO

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SQLITE_CREATED=NO
SQLITE_OPENED=NO
IAM_MUTATIONS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

An access result is PASS only when Secret Manager returns the payload for the
exact requested numeric-version resource under the impersonated runtime
principal, without resource or principal substitution. Payload and token
material must not be inspected beyond the minimum needed to establish success.

## 12. Fail-closed behavior

If impersonation, token mint, or either exact secret access fails, the
execution consumer must stop and return only a safe failure category.

```text
FAIL_CLOSED=YES
RETRY_ON_FAILURE=NO
SECOND_TOKEN_MINT_OR_REFRESH_ON_FAILURE=NO
DISCOVER_ANOTHER_VERSION_ON_FAILURE=NO
USE_LATEST_ON_FAILURE=NO
ALTER_IAM_ON_FAILURE=NO
CHANGE_RESOURCE_IDENTITY_ON_FAILURE=NO
CHANGE_RUNTIME_PRINCIPAL_ON_FAILURE=NO
INITIALIZE_SQLITE_ON_FAILURE=NO
START_PRODUCTION_RUNTIME_ON_FAILURE=NO
CALL_HIGHLEVEL_ON_FAILURE=NO
FALL_BACK_TO_AUTHORIZATION_001_ON_FAILURE=NO
FALL_BACK_TO_DIRECT_USER_ADC_SECRET_ACCESS_ON_FAILURE=NO
```

Safe failure categories may identify non-sensitive classes such as
authentication unavailable, impersonation denied, permission denied, resource
not found, disabled version, dependency unavailable, or sanitized transport
failure. They must not include payload, token, credential, header, or operator
principal material.

## 13. Non-escalation

```text
R1A_SUCCESS_AUTHORIZES_R1B=NO
R1A_SUCCESS_AUTHORIZES_R2=NO
R1A_SUCCESS_AUTHORIZES_R3=NO
R1A_SUCCESS_AUTHORIZES_R4=NO

R1A_SUCCESS_AUTHORIZES_PRODUCTION_RUNTIME=NO
R1A_SUCCESS_AUTHORIZES_HIGHLEVEL=NO
R1A_SUCCESS_AUTHORIZES_CRM_MUTATION=NO
R1A_SUCCESS_AUTHORIZES_SQLITE=NO
R1A_SUCCESS_AUTHORIZES_IAM_MUTATION=NO
R1A_SUCCESS_AUTHORIZES_STANDING_TOKEN=NO
R1A_SUCCESS_AUTHORIZES_DEPLOYMENT=NO
```

Every later runtime-validation gate requires a separate, explicit
human-governed authorization.

## 14. Authoring pre-flight and zero-effect attestation

```text
PREFLIGHT_PWD=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=
  auth/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-002
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_SHA=
  cd40d699601803c1a8dac169e5b52a72900b3745
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO

PR201_MERGED=YES
AUTHORIZATION_001_ON_ORIGIN_MAIN=YES
PR201_AUTHORIZATION_CONSUMED_BEFORE_SUPERSESSION=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=1
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
SERVICE_ACCOUNT_IMPERSONATION=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
SQLITE_OPENED=NO
SQLITE_CREATED=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

## 15. Review disposition

```text
R1A_DESIGNABLE=YES
R1A_EXECUTION_READY_AFTER_MERGE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

NEXT=
  return authorization 002 PR to ChatGPT for independent reviewer disposition
```
