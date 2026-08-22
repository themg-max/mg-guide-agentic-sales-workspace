# NW-008 AT-8O2 - Private Source-Principal Authority System Design 001

```text
UNIT=NW008_AT8O2_PRIVATE_SOURCE_PRINCIPAL_AUTHORITY_SYSTEM_DESIGN_001
PR_CLASS=planning_only
MODE=PRIVATE_AUTHORITY_SYSTEM_DESIGN_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PR130_REVIEWED_HEAD=c8fa48f8be206ba2a0df497b59ab87e31e783bbc
PR130_MERGE_SHA=fdf0b0454f2afea8702b7e92e5fb93fccb894350
PR130_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES

PRIVATE_AUTHORITY_SYSTEM_OF_RECORD_IDENTIFIED=YES
PRIVATE_AUTHORITY_SYSTEM_OF_RECORD=GOVERNED_PRIVATE_APPEND_ONLY_GIT_AUTHORITY_REGISTRY

PRIVATE_AUTHORITY_WRITE_PATH_IDENTIFIED=YES
PRIVATE_AUTHORITY_WRITE_PATH=HUMAN_APPROVED_PULL_REQUEST_TO_PROTECTED_APPEND_ONLY_PRIVATE_REGISTRY
PRIVATE_AUTHORITY_RECORD_CREATION_AUTHORITY_IDENTIFIED=YES
PRIVATE_AUTHORITY_RECORD_CREATION_AUTHORITY=PRIVATE_AUTHORITY_HUMAN_REVIEWER_QUORUM
PRIVATE_AUTHORITY_RECORDING_ACTOR=GOVERNED_PRIVATE_REGISTRY_MERGE_WORKFLOW

PRIVATE_AUTHORITY_RECORD_SCHEMA_REQUIRED=YES
PRIVATE_AUTHORITY_RECORD_VERSIONING_REQUIRED=YES
PRIVATE_AUTHORITY_RECORD_IMMUTABLE_AFTER_APPROVAL=YES

SOURCE_PRINCIPAL_PUBLIC_REF_NON_REASSIGNABLE=YES
SOURCE_PRINCIPAL_REPLACEMENT_REQUIRES_NEW_PUBLIC_REF=YES
PRIVATE_RECORD_SUPERSESSION_REQUIRED=YES
REVOKED_RECORD_USE=FORBIDDEN

PRIVATE_RUNTIME_RETRIEVAL_PATH_IDENTIFIED=YES
PRIVATE_RUNTIME_RETRIEVAL_PATH=OPAQUE_REF_LOOKUP_VIA_PRIVATE_MG_MCP_AUTHORITY_INDEX

MG_MCP_ROLE=READ_ONLY_RETRIEVAL_AFTER_GOVERNED_INGESTION
MG_MCP_INGESTION_PATH_IDENTIFIED=YES
MG_MCP_INGESTION_PATH=GOVERNED_PRIVATE_REGISTRY_TO_PRIVATE_AUTHORITY_INDEX
MG_MCP_WRITE_AUTHORITY_ASSUMED=NO

SOURCE_PRINCIPAL_IDENTIFIED=NO
SOURCE_PRINCIPAL_SELECTION_EXECUTED=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO

TOKEN_CREATOR_BINDING_AUTHORIZATION_DESIGNABLE=NO

IMPLEMENTATION_PERFORMED=NO
IAM_CHANGES=0
ADC_MUTATIONS=0
CREDENTIAL_USE=0
SECRET_READS=0
SERVICE_ACCOUNT_IMPERSONATION_EXECUTED=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
EXTERNAL_EFFECTS=0
```

## 1. Decision and boundary

AT8O2 selects a governed private append-only Git authority registry as the
system of record for exact human source-principal authority. The registry is
private infrastructure outside this public repository. Its concrete repository
identifier, host details, branch name, access groups, and endpoints are not
published here.

MG MCP is not the system of record and receives no runtime writes. It remains a
read-only governed context surface. A separately governed ingestion workflow
may project approved private registry records into a private MG MCP authority
index for read-only lookup.

This design does not provision the registry or index, configure ingestion,
select a human principal, create a record, use credentials, inspect ADC, or
authorize IAM.

```text
PRIVATE_AUTHORITY_SYSTEM_DESIGN_DECIDED=YES
PRIVATE_AUTHORITY_SYSTEM_PROVISIONED=NO
PRIVATE_AUTHORITY_REGISTRY_IDENTIFIER_PUBLIC=NO
PRIVATE_INFRASTRUCTURE_IDENTIFIERS_PUBLIC=NO
MG_MCP_RUNTIME_WRITES=FORBIDDEN
MG_MCP_SYSTEM_OF_RECORD=NO
```

## 2. Write authority and creation path

All record creation and lifecycle events use a pull request against the private
registry. Direct pushes and force pushes are forbidden. The protected
append-only branch requires:

```text
PRIVATE_REGISTRY_DIRECT_PUSH=FORBIDDEN
PRIVATE_REGISTRY_FORCE_PUSH=FORBIDDEN
PRIVATE_REGISTRY_HISTORY_REWRITE=FORBIDDEN
PRIVATE_REGISTRY_REQUIRED_HUMAN_APPROVALS=2
PRIVATE_REGISTRY_SIGNED_COMMITS_REQUIRED=YES
PRIVATE_REGISTRY_SCHEMA_VALIDATION_REQUIRED=YES
PRIVATE_REGISTRY_APPEND_ONLY_VALIDATION_REQUIRED=YES
```

The human reviewer quorum is the record-creation authority. It approves the
exact private principal and the complete record event. The merge workflow is
the recording actor: it may validate and merge approved content, but it may not
select, infer, substitute, or rewrite the principal.

```text
SOURCE_PRINCIPAL_SELECTION_AUTHORITY=HUMAN_ONLY
SOURCE_PRINCIPAL_SELECTION_BY_MERGE_WORKFLOW=FORBIDDEN
RECORDING_ACTOR_MAY_SELECT_PRINCIPAL=NO
RECORDING_ACTOR_MAY_MODIFY_APPROVED_PAYLOAD=NO
RECORDING_ACTOR_MAY_BYPASS_REVIEW=NO
```

The exact identities authorized to review or operate the private workflow are
private registry configuration. AT8O2 identifies their authority classes, not
their member values, and grants no access.

## 3. Append-only authority record model

The registry stores an append-only event stream per opaque public reference.
Every approved event is a new immutable file revision and signed Git commit.
No approved event is edited in place.

### 3.1 Required envelope

Each event must validate against a versioned private JSON schema with these
logical fields:

```text
schema_version                 positive integer
event_id                       unique opaque identifier
event_version                  positive monotonic integer per public_ref
event_type                     APPROVE | SUPERSEDE | REVOKE
public_ref                     opaque non-PII reference
record_state                   ACTIVE | SUPERSEDED | REVOKED
exact_source_principal         private exact user principal
source_principal_class         HUMAN_OPERATOR_USER_ADC
selected_identity_mechanism    LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION
target_runtime_principal       exact target service account
predecessor_public_ref         null or prior opaque reference
successor_public_ref           null or replacement opaque reference
reason_code                    governed non-secret reason
approved_at                    UTC timestamp
effective_at                   UTC timestamp
approvals                      private reviewer attestations
correlation_contract_version   AT8O1 contract version
google_subject_id              optional private stable subject identifier
```

The schema must reject access tokens, refresh tokens, credential payloads,
service account keys, arbitrary secrets, and public-repository paths.

```text
EXACT_SOURCE_PRINCIPAL_DATA_CLASS=PRIVATE_PII
ACCESS_TOKEN_FIELD_ALLOWED=NO
REFRESH_TOKEN_FIELD_ALLOWED=NO
CREDENTIAL_MATERIAL_FIELD_ALLOWED=NO
SECRET_VALUE_FIELD_ALLOWED=NO
PUBLIC_REPOSITORY_STORAGE_ALLOWED=NO
```

### 3.2 Versioning and immutability

`schema_version` versions the record grammar. `event_version` versions the
authority lifecycle for one `public_ref`. Both are explicit and independently
validated.

Approval makes an event immutable. Any post-approval correction requires a
`SUPERSEDE` event and a newly approved lineage under a new public reference; it
never amends an approved payload or rewrites Git history. The registry retains
every approved event for audit.

```text
APPROVED_EVENT_MUTATION=FORBIDDEN
APPROVED_EVENT_DELETION=FORBIDDEN
CORRECTION_REQUIRES_SUPERSESSION_AND_NEW_PUBLIC_REF=YES
EVENT_VERSION_MONOTONICITY_REQUIRED=YES
SCHEMA_VERSION_EXPLICIT=YES
APPROVED_HISTORY_RETENTION_REQUIRED=YES
```

Git history supplies the durable version chain, while schema validation
supplies domain-level monotonicity and state-transition checks. Git alone is
not treated as sufficient authority validation.

The only valid lifecycle is:

```text
ABSENT -> APPROVE(ACTIVE)
ACTIVE -> SUPERSEDE(SUPERSEDED)
ACTIVE -> REVOKE(REVOKED)
SUPERSEDED -> TERMINAL
REVOKED -> TERMINAL
```

## 4. Public-reference lifecycle

The opaque public reference identifies one exact human principal authority
lineage and is never reassigned.

```text
SOURCE_PRINCIPAL_PUBLIC_REF_NON_REASSIGNABLE=YES
PUBLIC_REF_DERIVED_FROM_EXACT_PRINCIPAL=NO
PUBLIC_REF_REUSE_AFTER_REVOCATION=FORBIDDEN
PUBLIC_REF_REUSE_AFTER_SUPERSESSION=FORBIDDEN
```

A replacement human principal always receives a new opaque public reference.
The old lineage receives an immutable `SUPERSEDE` event that names only the new
opaque reference as its successor. The new lineage may name the old opaque
reference as its predecessor.

```text
SOURCE_PRINCIPAL_REPLACEMENT_REQUIRES_NEW_PUBLIC_REF=YES
PRIVATE_RECORD_SUPERSESSION_REQUIRED=YES
SUPERSESSION_IS_BIDIRECTIONALLY_LINKED=YES
SUPERSEDED_RECORD_USE=FORBIDDEN
```

Revocation appends an immutable `REVOKE` event to the existing lineage. It does
not delete history, free the public reference for reuse, or silently select a
replacement.

```text
REVOKED_RECORD_USE=FORBIDDEN
REVOCATION_RETAINS_AUDIT_HISTORY=YES
REVOCATION_AUTO_SELECTS_REPLACEMENT=NO
REVOCATION_REQUIRES_NEW_EVENT=YES
```

The resolver fails closed if a lineage has malformed ordering, conflicting
active states, missing predecessor/successor links, or a terminal
`SUPERSEDED`/`REVOKED` state.

## 5. Governed MG MCP ingestion

The ingestion path is an offline governed projection:

```text
PRIVATE_SYSTEM_OF_RECORD
  -> approved protected-branch commit
  -> append-only and schema validation
  -> human-approved ingestion release
  -> private MG MCP authority index
  -> read-only opaque-ref retrieval
```

The ingestion workflow reads only approved commits and validates the entire
lineage before publishing a projection. It must preserve:

```text
- public_ref
- exact private source principal
- resolved lifecycle state
- latest valid event_version
- schema_version
- target runtime principal
- selected identity mechanism
- approval and effective timestamps
- optional private Google subject binding
- source Git commit identity
```

The private index must not expose the exact principal to public search,
cross-tenant retrieval, logs, telemetry, or public proof. Failed ingestion
leaves the previous projection intact but marks the new registry version
unavailable; it must not create a success-shaped partial projection.

```text
MG_MCP_INGESTION_REQUIRES_HUMAN_APPROVED_RELEASE=YES
MG_MCP_INGESTION_SOURCE=APPROVED_PRIVATE_REGISTRY_COMMITS_ONLY
MG_MCP_PARTIAL_PROJECTION=FORBIDDEN
MG_MCP_PUBLIC_INDEXING=FORBIDDEN
MG_MCP_CROSS_TENANT_RETRIEVAL=FORBIDDEN
MG_MCP_EXACT_PRINCIPAL_LOGGING=FORBIDDEN
MG_MCP_INGESTION_EXECUTED=NO
MG_MCP_WRITE_AUTHORITY_ASSUMED=NO
```

This is not an MG MCP write by the application or runtime. It is a separately
governed platform ingestion from the private system of record. The current
read-only MG MCP surface does not authorize, expose, or execute that ingestion.
Concrete private endpoint, index, and job identifiers remain unpublished.

## 6. Private runtime retrieval contract

The future private preflight retrieves by exact opaque public reference from
the private MG MCP authority index. It requests one lineage and receives one
resolved private authority result.

```text
PRIVATE_RUNTIME_RETRIEVAL_PATH_IDENTIFIED=YES
PRIVATE_RUNTIME_RETRIEVAL_INPUT=EXACT_OPAQUE_PUBLIC_REF
PRIVATE_RUNTIME_RETRIEVAL_CARDINALITY=EXACTLY_ONE_ACTIVE_RESULT
PRIVATE_RUNTIME_RETRIEVAL_RESULT_VISIBILITY=PRIVATE_ONLY
PRIVATE_RUNTIME_RETRIEVAL_WRITE_CAPABILITY=NONE
```

A valid retrieval result must be:

```text
- sourced from an approved ingested commit
- schema-valid
- lifecycle-valid
- ACTIVE
- not superseded
- not revoked
- bound to the requested opaque reference
- bound to the selected identity mechanism
- bound to the exact target runtime principal
```

Retrieval returns the exact principal only in private memory for the AT8O1 OIDC
correlation. Public evidence is limited to the opaque reference, record/event
versions, source commit identifier, and boolean correlation outcome.

```text
PRIVATE_RETRIEVAL_NOT_FOUND=FAIL_CLOSED
PRIVATE_RETRIEVAL_MULTIPLE_RESULTS=FAIL_CLOSED
PRIVATE_RETRIEVAL_STALE_PROJECTION=FAIL_CLOSED
PRIVATE_RETRIEVAL_SCHEMA_MISMATCH=FAIL_CLOSED
PRIVATE_RETRIEVAL_SUPERSEDED=FAIL_CLOSED
PRIVATE_RETRIEVAL_REVOKED=FAIL_CLOSED
PRIVATE_RETRIEVAL_TARGET_MISMATCH=FAIL_CLOSED
PRIVATE_RETRIEVAL_MECHANISM_MISMATCH=FAIL_CLOSED
PRIVATE_RETRIEVAL_PUBLIC_PII_OUTPUT=FORBIDDEN
```

No runtime retrieval is executed or authorized by AT8O2. Authentication and
authorization for future private retrieval require a separate design and
authorization.

## 7. Authorization gates

The following facts remain unresolved or unperformed:

```text
SOURCE_PRINCIPAL_IDENTIFIED=NO
SOURCE_PRINCIPAL_SELECTION_EXECUTED=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO
PRIVATE_AUTHORITY_SYSTEM_PROVISIONED=NO
MG_MCP_PRIVATE_INDEX_PROVISIONED=NO
MG_MCP_INGESTION_EXECUTED=NO
PRIVATE_RUNTIME_RETRIEVAL_EXECUTED=NO
```

Token Creator authorization remains blocked until the private registry and
ingestion path are implemented under separate authority, a human-approved
source-principal record exists, the active record is retrievable privately, and
AT8O1 ADC correlation succeeds.

```text
TOKEN_CREATOR_BINDING_AUTHORIZATION_DESIGNABLE=NO
TOKEN_CREATOR_ROLE_GRANTED=NO
```

## 8. Explicit non-actions

```text
EXACT_HUMAN_PRINCIPAL_SELECTED=NO
EXACT_HUMAN_PRINCIPAL_IN_PUBLIC_REPO=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO
PRIVATE_REGISTRY_PROVISIONED=NO
MG_MCP_INGESTION_CONFIGURED=NO
MG_MCP_INGESTION_EXECUTED=NO
ADC_INSPECTED=NO
ADC_LOGIN_EXECUTED=NO
CREDENTIAL_REFRESH_EXECUTED=NO
CREDENTIAL_USE=0
SECRET_READS=0
IAM_CHANGES=0
TOKEN_CREATOR_ROLE_GRANTED=NO
SERVICE_ACCOUNT_IMPERSONATION_EXECUTED=NO
SRC_MODIFIED=NO
TESTS_MODIFIED=NO
DEPLOYMENT_CHANGES=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

## 9. Validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o2-private-source-principal-authority-system-design-001.md
SRC_CHANGES=0
TEST_CHANGES=0
IMPLEMENTATION_PERFORMED=NO
IAM_CHANGES=0
ADC_MUTATIONS=0
CREDENTIAL_USE=0
SECRET_READS=0
SERVICE_ACCOUNT_IMPERSONATION_EXECUTED=NO
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
DEPLOYMENT_CHANGES=0
EXTERNAL_EFFECTS=0
```
