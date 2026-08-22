# NW-008 AT-8O1 - Runtime Source-Principal Authority Design 001

```text
UNIT=NW008_AT8O1_RUNTIME_SOURCE_PRINCIPAL_AUTHORITY_DESIGN_001
PR_CLASS=planning_only
MODE=SOURCE_PRINCIPAL_AUTHORITY_DESIGN_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PR129_REVIEWED_HEAD=bd91bebdcc461e4ab9020e8400d46bc499b456ad
PR129_MERGE_SHA=aa7364a2921c68b5fcf9032fb89580a43c51b6a0
PR129_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES

SELECTED_IDENTITY_MECHANISM=LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION
TARGET_RUNTIME_PRINCIPAL=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_PRINCIPAL_CLASS=HUMAN_OPERATOR_USER_ADC

SOURCE_PRINCIPAL_IDENTIFIED=NO
SOURCE_PRINCIPAL_PUBLIC_REF=spref:nw008-at8o1:runtime-human-operator:001
SOURCE_PRINCIPAL_PUBLIC_REF_RESERVED=YES

SOURCE_PRINCIPAL_EXACT_VALUE_IN_PUBLIC_REPO=NO
SOURCE_PRINCIPAL_EXACT_VALUE_LOCATION=UNRESOLVED_PRIVATE_AUTHORITY_SYSTEM
PUBLIC_REPO_PII_EXPOSURE=FORBIDDEN

AUTHORIZED_USER_ADC_IDENTITY_CORRELATION_METHOD=IN_MEMORY_GOOGLE_OAUTH_USERINFO_EMAIL_MATCH_TO_PRIVATE_AUTHORITY_RECORD

SOURCE_PRINCIPAL_SELECTION_AUTHORITY=HUMAN_ONLY
SOURCE_PRINCIPAL_SELECTION_REQUIRES_EXPLICIT_HUMAN_APPROVAL=YES
SOURCE_PRINCIPAL_SELECTION_BY_AGENT=FORBIDDEN
SOURCE_PRINCIPAL_RECORDING_AGENT=UNRESOLVED

PRIVATE_AUTHORITY_SYSTEM_OF_RECORD_IDENTIFIED=NO
PRIVATE_AUTHORITY_SYSTEM_OF_RECORD=UNRESOLVED
PRIVATE_AUTHORITY_WRITE_PATH_IDENTIFIED=NO
PRIVATE_AUTHORITY_RECORD_CREATION_AUTHORITY_IDENTIFIED=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO
PRIVATE_AUTHORITY_SURFACE_SELECTED=NO

MG_MCP_ROLE=READ_ONLY_RETRIEVAL_AFTER_GOVERNED_INGESTION
MG_MCP_PRIVATE_AUTHORITY_RECORD_CREATION=NOT_AVAILABLE_VIA_CURRENT_SURFACE
MG_MCP_INGESTION_PATH_IDENTIFIED=NO

PUBLIC_REF_DERIVED_FROM_PRINCIPAL_VALUE=NO
PUBLIC_REF_REASSIGNABLE=NO

TOKEN_OR_REFRESH_TOKEN_PRINTING=FORBIDDEN
ADC_SECRET_MATERIAL_READOUT=FORBIDDEN
CREDENTIAL_EXPORT=FORBIDDEN

TOKEN_CREATOR_BINDING_AUTHORIZATION_DESIGNABLE=NO

AT8N_STATUS=PENDING_PARALLEL_PLANNING
AT8N_NEW_GHL_PIT_IAM_GRANT_REQUIRED=NO

COMMITMENT_KEY_SECRET_IAM_INCLUDED=NO
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO

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

## 1. Purpose and boundary

AT8O selected local authorized-user ADC plus short-lived service account
impersonation, but deliberately left the exact human source principal
unresolved. AT8O1 designs the human-only selection rule, reserves an opaque
public reference, specifies authorized-user ADC correlation, and defines gates
for a future authorization without disclosing the human operator's email. The
private system of record and its governed write path remain unresolved.

AT8O1 does not select the human, inspect ADC, use credentials, create a private
record, grant IAM, execute impersonation, or activate runtime behavior.

## 2. Source-principal selection authority

The artifact owner is the VS Code orchestrator, but artifact ownership does not
confer source-principal selection authority. The exact human principal must be
selected by a human through explicit private approval. Repository history,
local Git configuration, active gcloud CLI account state, shell environment,
and contributor identity are not selection authority and must not be used to
infer or guess the principal.

The private selection record must establish all of the following:

```text
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR
SOURCE_PRINCIPAL_SELECTION_AUTHORITY=HUMAN_ONLY
SOURCE_PRINCIPAL_SELECTION_REQUIRES_EXPLICIT_HUMAN_APPROVAL=YES
SOURCE_PRINCIPAL_SELECTION_BY_AGENT=FORBIDDEN
SOURCE_PRINCIPAL_RECORDING_AGENT=UNRESOLVED
SOURCE_PRINCIPAL_TYPE=USER_EMAIL_PRINCIPAL
SOURCE_PRINCIPAL_CLASS_REQUIRED=HUMAN_OPERATOR_USER_ADC
SOURCE_PRINCIPAL_MUST_NOT_BE_CI_PRINCIPAL=YES
SOURCE_PRINCIPAL_MUST_NOT_BE_TARGET_RUNTIME_SERVICE_ACCOUNT=YES
SOURCE_PRINCIPAL_GUESSING=FORBIDDEN
```

A human authority must eventually supply the exact user principal through a
governed private write path. That path and the recording agent are not yet
identified. No agent may select or derive the principal from likely usernames,
repository authors, local machine accounts, organization conventions, or
nearby IAM members.

## 3. Private representation and public opaque reference

No private authority system of record is selected. The current MG MCP surface
is read-only retrieval after governed ingestion; it does not expose private
authority record creation, and no ingestion path is identified. The public
repository therefore reserves only the opaque reference:

```text
PRIVATE_AUTHORITY_SYSTEM_OF_RECORD_IDENTIFIED=NO
PRIVATE_AUTHORITY_SYSTEM_OF_RECORD=UNRESOLVED
PRIVATE_AUTHORITY_WRITE_PATH_IDENTIFIED=NO
PRIVATE_AUTHORITY_RECORD_CREATION_AUTHORITY_IDENTIFIED=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO
PRIVATE_AUTHORITY_SURFACE_SELECTED=NO

SOURCE_PRINCIPAL_EXACT_VALUE_LOCATION=UNRESOLVED_PRIVATE_AUTHORITY_SYSTEM

MG_MCP_ROLE=READ_ONLY_RETRIEVAL_AFTER_GOVERNED_INGESTION
MG_MCP_PRIVATE_AUTHORITY_RECORD_CREATION=NOT_AVAILABLE_VIA_CURRENT_SURFACE
MG_MCP_INGESTION_PATH_IDENTIFIED=NO

SOURCE_PRINCIPAL_PUBLIC_REF=spref:nw008-at8o1:runtime-human-operator:001
SOURCE_PRINCIPAL_PUBLIC_REF_RESERVED=YES
PUBLIC_REF_DERIVED_FROM_PRINCIPAL_VALUE=NO
PUBLIC_REF_REASSIGNABLE=NO
```

The opaque reference is an identifier, not an encoding, hash, prefix, domain,
or other derivative of the human email. It must never be reassigned to another
principal. Reservation does not claim that a private record exists. Once a
governed private system, write path, and creation authority are separately
selected, its record for the reference must bind:

```text
- exact human user principal
- source-principal class
- opaque public reference
- selected identity mechanism
- target runtime service account
- authorized-user ADC requirement
- approval identity and timestamp
- immutable private record version
```

Immutability, versioning, non-reassignment, and approval are requirements for a
future system selection, not capabilities claimed for MG MCP or any currently
available surface.

No public artifact may contain the exact principal, a reversible transform, a
principal-derived unsalted digest, or an IAM command containing the principal.

## 4. Authorized-user ADC identity correlation

Selection authority and credential identity are separate facts. After a
private system and principal record exist, a separately authorized private
preflight must prove that local authorized-user ADC belongs to the exact
principal in that system before a future Token Creator authorization can be
designed.

The designed correlation method is:

1. Resolve the opaque reference to the exact expected principal inside the
   selected private system of record.
2. Load only local ADC with credential type `authorized_user`; reject generic
   implicit ADC fallback, service account keys, external-account credentials,
   compute metadata credentials, and
   `GOOGLE_APPLICATION_CREDENTIALS` overrides.
3. Validate that the effective granted identity scopes include both `openid`
   and `https://www.googleapis.com/auth/userinfo.email`; fail closed if scope
   metadata is unavailable or either scope is absent.
4. Refresh an access token in memory without printing, exporting, persisting,
   logging, or returning it.
5. Send `GET https://openidconnect.googleapis.com/v1/userinfo` with the bearer
   access token only in the `Authorization` header.
6. Require HTTP 200 and valid JSON containing an email with
   `email_verified=true`.
7. Compare the normalized email exactly to the private authority record.
   Private binding of the stable Google subject identifier is recommended.
8. Persist privately only the correlation result, record version, time, and
   opaque reference. Public evidence may state `MATCH=YES|NO` and the opaque
   reference only.
9. Retain no token or identity-response references after preflight completion
   and perform best-effort reference release. Do not claim deterministic
   memory zeroization.

```text
ADC_CREDENTIAL_TYPE_REQUIRED=authorized_user
ADC_IDENTITY_ENDPOINT=https://openidconnect.googleapis.com/v1/userinfo
ADC_IDENTITY_ENDPOINT_METHOD=GET
ADC_IDENTITY_AUTHORIZATION=BEARER_ACCESS_TOKEN_IN_HEADER_ONLY

ADC_REQUIRED_SCOPE_VALIDATION=YES
ADC_REQUIRED_IDENTITY_SCOPES=openid,https://www.googleapis.com/auth/userinfo.email

ADC_REQUIRED_SCOPE_MISSING=FAIL_CLOSED
ADC_USERINFO_NON_200=FAIL_CLOSED
ADC_USERINFO_INVALID_JSON=FAIL_CLOSED
ADC_EMAIL_CLAIM_MISSING=FAIL_CLOSED
ADC_EMAIL_VERIFIED_FALSE=FAIL_CLOSED
ADC_IDENTITY_MISMATCH=FAIL_CLOSED

ADC_EMAIL_VERIFIED_REQUIRED=YES
ADC_EMAIL_NORMALIZATION=TRIM_AND_ASCII_LOWERCASE
ADC_IDENTITY_MATCH_REQUIRED=EXACT_NORMALIZED_EMAIL_EQUALITY
ADC_IDENTITY_MATCH_OUTPUT_PUBLIC=BOOLEAN_AND_OPAQUE_REF_ONLY
ADC_CREDENTIAL_TYPE_MISMATCH=FAIL_CLOSED
MULTIPLE_CANDIDATE_IDENTITIES=FAIL_CLOSED
GITHUB_OR_GIT_IDENTITY_AS_ADC_PROOF=FORBIDDEN
GCLOUD_ACTIVE_ACCOUNT_AS_ADC_PROOF=FORBIDDEN

GOOGLE_SUBJECT_ID_PRIVATE_BINDING=RECOMMENDED
GOOGLE_SUBJECT_ID_PUBLIC_DISCLOSURE=NO

ACCESS_TOKEN_PERSISTENCE=FORBIDDEN
IDENTITY_RESPONSE_PERSISTENCE=FORBIDDEN
SECRET_VALUE_LOGGING=FORBIDDEN
IN_MEMORY_REFERENCE_RETENTION_AFTER_PREFLIGHT=FORBIDDEN
BEST_EFFORT_REFERENCE_RELEASE_REQUIRED=YES
DETERMINISTIC_MEMORY_ZEROIZATION_CLAIMED=NO
```

This method is designed, not executed. Credential refresh and Google OAuth
userinfo access require a separate, explicit read-only preflight
authorization. AT8O1 performs neither.

## 5. Safe binding to future authorization

A future Token Creator authorization may become designable only after every
gate below is satisfied:

```text
GATE_1_PRIVATE_SYSTEM_OF_RECORD_SELECTED=REQUIRED
GATE_2_PRIVATE_WRITE_PATH_AND_CREATION_AUTHORITY_IDENTIFIED=REQUIRED
GATE_3_PRIVATE_SOURCE_PRINCIPAL_SELECTED_BY_HUMAN=REQUIRED
GATE_4_PRIVATE_RECORD_APPROVED_AND_IMMUTABLE=REQUIRED
GATE_5_AUTHORIZED_USER_ADC_CORRELATION_MATCH=REQUIRED
GATE_6_OPAQUE_REF_AND_PRIVATE_RECORD_VERSION_BOUND=REQUIRED
GATE_7_TARGET_RUNTIME_PRINCIPAL_EXACT_MATCH=REQUIRED
GATE_8_FRESH_HUMAN_AUTHORIZATION_REVIEW=REQUIRED
```

The future public authorization must identify only the opaque source reference,
private record version, target service account, requested role, resource scope,
and fail-closed preconditions. The exact source member value must be resolved
from the private authority record only inside the separately authorized IAM
execution context.

```text
FUTURE_ROLE=roles/iam.serviceAccountTokenCreator
FUTURE_ROLE_TARGET=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
FUTURE_SOURCE_MEMBER_PUBLIC_VALUE=FORBIDDEN
FUTURE_SOURCE_MEMBER_PRIVATE_RESOLUTION=REQUIRED
FUTURE_AUTHORIZATION_MUST_BIND_OPAQUE_REF=YES
FUTURE_AUTHORIZATION_MUST_BIND_PRIVATE_RECORD_VERSION=YES
FUTURE_AUTHORIZATION_REUSABLE=NO
```

Until the private system, write path, creation authority, human selection,
immutable record, and ADC correlation all exist, the Token Creator binding
remains not authorization-designable.

## 6. Fail-closed rules

```text
MISSING_PRIVATE_AUTHORITY_SYSTEM_OF_RECORD=FAIL_CLOSED
MISSING_PRIVATE_AUTHORITY_WRITE_PATH=FAIL_CLOSED
MISSING_PRIVATE_RECORD_CREATION_AUTHORITY=FAIL_CLOSED
MISSING_PRIVATE_AUTHORITY_RECORD=FAIL_CLOSED
MISSING_PRIVATE_RECORD_VERSION=FAIL_CLOSED
MISSING_EXACT_SOURCE_PRINCIPAL=FAIL_CLOSED
OPAQUE_REF_NOT_FOUND=FAIL_CLOSED
OPAQUE_REF_REASSIGNED=FAIL_CLOSED
TARGET_RUNTIME_PRINCIPAL_MISMATCH=FAIL_CLOSED
ADC_CORRELATION_NOT_RUN=FAIL_CLOSED
ADC_CORRELATION_MISMATCH=FAIL_CLOSED
ADC_REQUIRED_SCOPE_MISSING=FAIL_CLOSED
ADC_USERINFO_NON_200=FAIL_CLOSED
ADC_USERINFO_INVALID_JSON=FAIL_CLOSED
ADC_EMAIL_VERIFIED_FALSE=FAIL_CLOSED
PRIVATE_APPROVAL_MISSING=FAIL_CLOSED
PUBLIC_PII_DISCLOSURE_DETECTED=FAIL_CLOSED
```

Failure does not fall back to direct user ADC, a service account key, a
different operator, a CI principal, or an implicit ADC chain.

## 7. Parallel and excluded lanes

```text
AT8N_STATUS=PENDING_PARALLEL_PLANNING
AT8N_NEW_GHL_PIT_IAM_GRANT_REQUIRED=NO
AT8N_DEPENDS_ON_SOURCE_PRINCIPAL_SELECTION=NO

COMMITMENT_KEY_SECRET_IAM_INCLUDED=NO
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO
```

AT8N may continue its planning-only reconciliation of the already-configured
GHL PIT accessor binding. AT8O1 does not include commitment-key secret IAM,
runtime activation, or any new GHL PIT grant.

## 8. Explicit non-actions

```text
EXACT_HUMAN_OPERATOR_EMAIL_WRITTEN_TO_PUBLIC_REPO=NO
OPERATOR_PRINCIPAL_GUESSED=NO
TOKEN_CREATOR_ROLE_GRANTED=NO
GCLOUD_ADC_LOGIN_EXECUTED=NO
ADC_CREDENTIAL_REFRESH_EXECUTED=NO
ADC_USERINFO_CALLED=NO
ACCESS_TOKEN_PRINTED_OR_EXPORTED=NO
REFRESH_TOKEN_READ_OR_EXPOSED=NO
PRIVATE_AUTHORITY_RECORD_CREATED=NO
IAM_MUTATED=NO
SECRET_MANAGER_READ=NO
SRC_MODIFIED=NO
TESTS_MODIFIED=NO
DEPLOYMENT_EXECUTED=NO
HIGHLEVEL_CALLED=NO
CRM_MUTATED=NO
EXTERNAL_EFFECTS=0
```

## 9. Validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o1-runtime-source-principal-authority-design-001.md
SRC_CHANGES=0
TEST_CHANGES=0
IAM_CHANGES=0
ADC_MUTATIONS=0
CREDENTIAL_USE=0
SECRET_READS=0
DEPLOYMENT_CHANGES=0
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```
