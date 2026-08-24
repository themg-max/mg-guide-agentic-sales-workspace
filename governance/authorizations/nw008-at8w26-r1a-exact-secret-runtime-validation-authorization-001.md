# NW-008 AT8W26 R1A Exact-Secret Runtime Validation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8W26_R1A_EXACT_SECRET_RUNTIME_VALIDATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
MODE=AUTHORIZATION_ARTIFACT_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-001.md
AUTHORIZATION_BRANCH=
  auth/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-001

BASE_REF=origin/main
BASE_SHA=
  ed2cce448a96ded0aca224e33be05f5fb949cac2

SOURCE_IMPLEMENTATION_MERGE=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
SOURCE_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w25/nw008-at8w25-b2-c4-c3-c2-offline-implementation-proof-001.md

STATUS_AT_AUTHORING=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE
AUTHORIZATION_STATE_AT_AUTHORING=PROPOSED_NOT_EFFECTIVE
GRANT_ACTIVATION=HUMAN_MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVENESS_SOURCE=REPO_STATE_NOT_MUTABLE_FIELD
SELF_ACTIVATION=FORBIDDEN
```

This artifact is planning-only. Creating, reviewing, or merging it does not
read a Secret Manager payload or execute runtime validation. The bounded grant
becomes usable only after human review and merge places this exact artifact on
`main`, followed by independent verification by the authorized execution
consumer.

```text
EXECUTION_PERFORMED_IN_THIS_UNIT=NO
SECRET_MANAGER_ACCESS_PERFORMED_IN_THIS_UNIT=NO
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
HIGHLEVEL_CALLS_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
SQLITE_CREATION_IN_THIS_UNIT=0
SQLITE_OPEN_IN_THIS_UNIT=0
IAM_MUTATIONS_IN_THIS_UNIT=0
TOKEN_MINTS_IN_THIS_UNIT=0
DEPLOYMENTS_IN_THIS_UNIT=0
AUTHORIZATION_CONSUMED_IN_THIS_UNIT=NO
```

## 2. Purpose and explicit non-authority

This artifact conditionally authorizes one later bounded validation of the two
exact Secret Manager resources already designated and implemented by the
merged AT8W25 implementation. The validation may establish only whether the
authorized execution identity can read each exact numeric version once.

```text
PURPOSE=
  ONE_BOUNDED_LIVE_RUNTIME_DEPENDENCY_VALIDATION_OF_TWO_EXACT_SECRET_VERSIONS

PRODUCTION_RUNTIME_EXECUTION_AUTHORIZED=NO
HIGHLEVEL_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
SQLITE_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
TOKEN_MINT_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

The future R1A consumer must not start the production runtime, construct the
production execution store, open or create SQLite, call HighLevel, mutate CRM,
change IAM, mint a token, create a service-account key, or deploy. A successful
R1A validates only exact-secret accessibility under the already-governed
execution identity.

## 3. Durable source prerequisite

```text
SOURCE_IMPLEMENTATION_PR=200
SOURCE_IMPLEMENTATION_PR_STATE=MERGED
SOURCE_IMPLEMENTATION_REVIEWED_HEAD=
  f8cec16b479808b676a4dbbcfb9a92bd716db379
SOURCE_IMPLEMENTATION_MERGE=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
SOURCE_IMPLEMENTATION_MERGE_ON_ORIGIN_MAIN=YES
SOURCE_IMPLEMENTATION_REVIEWED_HEAD_ANCESTRY=PASS

SOURCE_IMPLEMENTATION_PROOF=
  proof/nw008/at-8w25/nw008-at8w25-b2-c4-c3-c2-offline-implementation-proof-001.md
SOURCE_IMPLEMENTATION_PROOF_ON_ORIGIN_MAIN=YES

B2_IMPLEMENTATION_DURABLE=YES
C4_IMPLEMENTATION_DURABLE=YES
C3_IMPLEMENTATION_DURABLE=YES
C2_IMPLEMENTATION_DURABLE=YES
GOOGLE_CLOUD_SECRET_MANAGER_VERSION=2.27.0
```

The source implementation proof records offline implementation durability. It
does not itself authorize or prove live Secret Manager access. This artifact
does not broaden the implementation proof's runtime, GHL, SQLite, or mutation
boundary.

## 4. Exact permitted resources

Exactly two resource names are permitted:

```text
B2_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1

C4_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1

PERMITTED_SECRET_RESOURCE_COUNT=2
OTHER_SECRET_RESOURCES_PERMITTED=NO
CALLER_RESOURCE_OVERRIDE_ALLOWED=NO
LATEST_ALLOWED=NO
ALIAS_RESOLUTION_ALLOWED=NO
VERSION_DISCOVERY_ALLOWED=NO
SECRET_DISCOVERY_ALLOWED=NO
```

The exact strings above are normative. The execution consumer may not replace
a project identifier with a project number or vice versa, change a secret
name, change a numeric version, use `latest`, use an alias, resolve an alias,
or discover an alternative resource.

Forbidden Secret Manager operations include:

- secret listing;
- secret-version listing;
- version discovery or selection;
- metadata discovery used to locate an alternative resource;
- any payload access for a resource other than the two exact names above; and
- any retry of either exact access attempt.

## 5. Permitted effect budget

```text
B2_SECRET_READ_ATTEMPTS_MAX=1
C4_SECRET_READ_ATTEMPTS_MAX=1
TOTAL_SECRET_READ_ATTEMPTS_MAX=2

SECRET_LIST_CALLS_MAX=0
SECRET_VERSION_LIST_CALLS_MAX=0
SECRET_METADATA_DISCOVERY_CALLS_MAX=0

HIGHLEVEL_CALLS_MAX=0
CRM_MUTATIONS_MAX=0

SQLITE_CREATION_MAX=0
SQLITE_OPEN_MAX=0

IAM_MUTATIONS_MAX=0
TOKEN_MINTS_MAX=0
SERVICE_ACCOUNT_KEY_CREATE_MAX=0

DEPLOYMENTS_MAX=0
PRODUCTION_RUNTIME_STARTS_MAX=0
```

The maximum is exactly one attempt against B2 and exactly one attempt against
C4. Unused budget is not transferable, reusable, or available for retries.
Success requires one and only one attempt for each exact resource. A failed B2
attempt terminates the sequence before C4; a failed C4 attempt terminates the
sequence after the single successful B2 attempt.

```text
EXECUTION_ORDER=B2_THEN_C4
B2_RETRIES_MAX=0
C4_RETRIES_MAX=0
UNUSED_ALLOWANCE_TRANSFER=FORBIDDEN
```

## 6. Payload handling and non-disclosure

Secret payloads may exist only in process memory for the minimum validation
necessary. The execution consumer must discard each payload without deriving
or retaining evidence from its content.

```text
PAYLOAD_PROCESS_MEMORY_ONLY=YES
PAYLOAD_MINIMUM_LIFETIME_REQUIRED=YES
PAYLOAD_PUBLISHED_ALLOWED=NO
PAYLOAD_PERSISTED_ALLOWED=NO
PAYLOAD_HASHING_FOR_PROOF_ALLOWED=NO
PAYLOAD_LENGTH_FOR_PROOF_ALLOWED=NO
TOKEN_FRAGMENT_CAPTURE_ALLOWED=NO
```

The following are forbidden:

- stdout or stderr payload printing;
- file, repository, database, log, telemetry, or proof persistence;
- payload hashing or other content-derived fingerprints for proof;
- payload length as proof;
- token or credential fragments;
- screenshots containing payload material;
- shell command arguments or shell history containing payload material;
- exception messages, tracebacks, or serialization containing payload
  material; and
- returning payload material to ChatGPT or any other consumer.

Proof may record only:

```text
PERMITTED_PROOF_FIELDS=
  exact_resource_identifier|
  attempt_count|
  success_or_failure|
  safe_exception_class_or_category|
  already_governed_authorization_identity_attestation_reference
```

No payload value, fragment, length, hash, encoding, shape, or content-derived
property is a permitted proof field.

## 7. Authorized consumer and one-shot semantics

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

AUTHORIZATION_STATE_BEFORE_EXECUTION=AVAILABLE_IF_MERGED_AND_VERIFIED
AUTHORIZATION_STATE_ON_EXECUTION=CONSUMED
AUTHORIZATION_STATE_AFTER_FIRST_ATTEMPT=CONSUMED
```

The grant is consumed when the future execution consumer begins the first B2
access attempt, regardless of success or failure. Failure does not restore the
grant. No other unit may consume or inherit it.

Before the first access attempt, the execution consumer must independently
verify:

```text
PRE_EXECUTION_REQUIRED=
  EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN|
  EXACT_AUTHORIZATION_HEAD_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_IMPLEMENTATION_MERGE_ANCESTOR_OF_ORIGIN_MAIN|
  SOURCE_IMPLEMENTATION_PROOF_PRESENT_ON_ORIGIN_MAIN|
  EXACT_B2_RESOURCE_MATCH|
  EXACT_C4_RESOURCE_MATCH|
  EFFECT_BUDGET_ENFORCED|
  PAYLOAD_NON_DISCLOSURE_ENFORCED
```

The consumer must record one-shot consumption without modifying this artifact.

## 8. Success condition

R1A succeeds only if both exact accesses pass within the fixed attempt budget
and no forbidden effect or disclosure occurs.

```text
B2_EXACT_SECRET_ACCESS=PASS
C4_EXACT_SECRET_ACCESS=PASS

B2_READ_ATTEMPTS=1
C4_READ_ATTEMPTS=1

PAYLOADS_PUBLISHED=NO
PAYLOADS_PERSISTED=NO

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SQLITE_CREATED=NO
SQLITE_OPENED=NO
IAM_MUTATIONS=0
TOKEN_MINTS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

An access result is PASS only when Secret Manager returns the payload for the
exact requested numeric-version resource without resource substitution. The
payload must not be inspected beyond the minimum operation needed to establish
that exact access succeeded.

## 9. Fail-closed behavior

If either exact resource fails, the execution consumer must stop. It must
return only a safe failure category to ChatGPT.

```text
FAIL_CLOSED=YES
RETRY_ON_FAILURE=NO
DISCOVER_ANOTHER_VERSION_ON_FAILURE=NO
USE_LATEST_ON_FAILURE=NO
ALTER_IAM_ON_FAILURE=NO
CHANGE_RESOURCE_IDENTITY_ON_FAILURE=NO
INITIALIZE_SQLITE_ON_FAILURE=NO
START_PRODUCTION_RUNTIME_ON_FAILURE=NO
CALL_HIGHLEVEL_ON_FAILURE=NO
```

Safe failure categories may identify an exception class or non-sensitive
category such as authentication unavailable, permission denied, resource not
found, disabled version, dependency unavailable, or sanitized transport
failure. They must not include payload material, token material, request
headers, credentials, or other sensitive values.

## 10. Non-escalation

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
R1A_SUCCESS_AUTHORIZES_TOKEN_MINT=NO
R1A_SUCCESS_AUTHORIZES_DEPLOYMENT=NO
```

A successful R1A proves only the bounded exact-secret access result recorded
under this grant. Every later runtime-validation gate requires a separate,
explicit human-governed authorization.

## 11. Authoring pre-flight and zero-effect attestation

```text
PREFLIGHT_PWD=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
PREFLIGHT_BRANCH=
  auth/nw008-at8w26-r1a-exact-secret-runtime-validation-authorization-001
PREFLIGHT_BRANCH_IS_MAIN=NO
PREFLIGHT_BASE_SHA=
  ed2cce448a96ded0aca224e33be05f5fb949cac2
PREFLIGHT_UNRELATED_WORKTREE_CHANGES=NO

ARTIFACTS_CREATED_IN_THIS_UNIT=1
REPOSITORY_PATHS_MODIFIED_IN_THIS_UNIT=1
RUNTIME_SOURCE_CHANGES_IN_THIS_UNIT=0

EXECUTION_PERFORMED=NO
SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SQLITE_CREATED=NO
SQLITE_OPENED=NO
IAM_MUTATIONS=0
TOKEN_MINTS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
DEPLOYMENTS=0
PRODUCTION_RUNTIME_STARTS=0
```

## 12. Review disposition

```text
R1A_DESIGNABLE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AUTONOMOUS_MERGE_AUTHORIZED=NO

NEXT=
  return authorization artifact/PR to ChatGPT for independent review before
  any Secret Manager payload access
```
