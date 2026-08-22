# NW-008 AT-8O1 - Runtime Source-Principal Authority Design 001

```text
UNIT=NW008_AT8O1_RUNTIME_SOURCE_PRINCIPAL_AUTHORITY_DESIGN_001
PR_CLASS=planning_only
MODE=SOURCE_PRINCIPAL_AUTHORITY_DESIGN_ONLY
OWNER=VS_CODE_ORCHESTRATOR

PR129_REVIEWED_HEAD=bd91bebdcc461e4ab9020e8400d46bc499b456ad
PR129_MERGE_SHA=aa7364a2921c68b5fcf9032fb89580a43c51b6a0
PR129_REVIEWED_HEAD_ANCESTOR_OF_MAIN=YES

SELECTED_IDENTITY_MECHANISM=LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION
TARGET_RUNTIME_PRINCIPAL=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_PRINCIPAL_CLASS=HUMAN_OPERATOR_USER_ADC

SOURCE_PRINCIPAL_IDENTIFIED=NO
SOURCE_PRINCIPAL_PUBLIC_REF=spref:nw008-at8o1:runtime-human-operator:001

SOURCE_PRINCIPAL_EXACT_VALUE_IN_PUBLIC_REPO=NO
SOURCE_PRINCIPAL_EXACT_VALUE_LOCATION=PRIVATE_MG_MCP_AUTHORITY_RECORD
PUBLIC_REPO_PII_EXPOSURE=FORBIDDEN

AUTHORIZED_USER_ADC_IDENTITY_CORRELATION_METHOD=IN_MEMORY_GOOGLE_OAUTH_USERINFO_EMAIL_MATCH_TO_PRIVATE_AUTHORITY_RECORD

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
unresolved. AT8O1 designs how that principal is selected, stored outside the
public repository, correlated to authorized-user ADC, and referenced by a
future authorization without disclosing the human operator's email.

AT8O1 does not select the human, inspect ADC, use credentials, create a private
record, grant IAM, execute impersonation, or activate runtime behavior.

## 2. Source-principal selection authority

The exact human principal must be selected by the owner through a private
authority review. Repository history, local Git configuration, active gcloud
CLI account state, shell environment, and contributor identity are not
selection authority and must not be used to infer or guess the principal.

The private selection record must establish all of the following:

```text
PRIVATE_SELECTION_OWNER=VS_CODE_ORCHESTRATOR
PRIVATE_SELECTION_REQUIRES_EXPLICIT_HUMAN_APPROVAL=YES
SOURCE_PRINCIPAL_TYPE=USER_EMAIL_PRINCIPAL
SOURCE_PRINCIPAL_CLASS_REQUIRED=HUMAN_OPERATOR_USER_ADC
SOURCE_PRINCIPAL_MUST_NOT_BE_CI_PRINCIPAL=YES
SOURCE_PRINCIPAL_MUST_NOT_BE_TARGET_RUNTIME_SERVICE_ACCOUNT=YES
SOURCE_PRINCIPAL_GUESSING=FORBIDDEN
```

The owner must supply the exact user principal directly in the private
authority surface. No agent may derive it from likely usernames, repository
authors, local machine accounts, organization conventions, or nearby IAM
members.

## 3. Private representation and public opaque reference

The selected exact principal is stored only in a private MG MCP authority
record. The public repository carries only the reserved opaque reference:

```text
PRIVATE_AUTHORITY_SURFACE_SELECTED=YES
PRIVATE_AUTHORITY_RECORD_CREATED=NO
PRIVATE_AUTHORITY_RECORD_TYPE=RUNTIME_SOURCE_PRINCIPAL_AUTHORITY
SOURCE_PRINCIPAL_PUBLIC_REF=spref:nw008-at8o1:runtime-human-operator:001

PUBLIC_REF_DERIVED_FROM_PRINCIPAL_VALUE=NO
PUBLIC_REF_REASSIGNABLE=NO
PRIVATE_RECORD_REASSIGNABLE=NO
PRIVATE_RECORD_VERSIONED=YES
PRIVATE_RECORD_MUTABLE_AFTER_APPROVAL=NO
```

The opaque reference is an identifier, not an encoding, hash, prefix, domain,
or other derivative of the human email. It must never be reassigned to another
principal. A private record for the reference must bind:

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

No public artifact may contain the exact principal, a reversible transform, a
principal-derived unsalted digest, or an IAM command containing the principal.

## 4. Authorized-user ADC identity correlation

Selection authority and credential identity are separate facts. Before a
future Token Creator authorization can be designed, a separately authorized
private preflight must prove that the local authorized-user ADC belongs to the
exact principal stored in the private authority record.

The designed correlation method is:

1. Resolve the opaque reference to the exact expected principal inside the
   private authority surface.
2. Load only local ADC with credential type `authorized_user`; reject generic
   implicit ADC fallback, service account keys, external-account credentials,
   compute metadata credentials, and
   `GOOGLE_APPLICATION_CREDENTIALS` overrides.
3. Refresh an access token in memory without printing, exporting, persisting,
   or returning it.
4. Call the Google OAuth userinfo endpoint with the token only in the
   authorization header.
5. Require `email_verified=true`, then read the returned email in memory and
   compare its normalized exact value to the private authority record.
6. Persist privately only the correlation result, record version, time, and
   opaque reference. Public evidence may state `MATCH=YES|NO` and the opaque
   reference only.
7. Destroy in-memory token and identity response values when the preflight
   completes.

```text
ADC_CREDENTIAL_TYPE_REQUIRED=authorized_user
ADC_EMAIL_VERIFIED_REQUIRED=YES
ADC_EMAIL_NORMALIZATION=TRIM_AND_ASCII_LOWERCASE
ADC_IDENTITY_MATCH_REQUIRED=EXACT_NORMALIZED_EMAIL_EQUALITY
ADC_IDENTITY_MATCH_OUTPUT_PUBLIC=BOOLEAN_AND_OPAQUE_REF_ONLY
ADC_IDENTITY_MISMATCH=FAIL_CLOSED
ADC_EMAIL_CLAIM_MISSING=FAIL_CLOSED
ADC_CREDENTIAL_TYPE_MISMATCH=FAIL_CLOSED
MULTIPLE_CANDIDATE_IDENTITIES=FAIL_CLOSED
GITHUB_OR_GIT_IDENTITY_AS_ADC_PROOF=FORBIDDEN
GCLOUD_ACTIVE_ACCOUNT_AS_ADC_PROOF=FORBIDDEN
```

This method is designed, not executed. Credential refresh and Google OAuth
userinfo access require a separate, explicit read-only preflight
authorization. AT8O1 performs neither.

## 5. Safe binding to future authorization

A future Token Creator authorization may become designable only after every
gate below is satisfied:

```text
GATE_1_PRIVATE_SOURCE_PRINCIPAL_SELECTED=REQUIRED
GATE_2_PRIVATE_RECORD_APPROVED_AND_IMMUTABLE=REQUIRED
GATE_3_AUTHORIZED_USER_ADC_CORRELATION_MATCH=REQUIRED
GATE_4_OPAQUE_REF_AND_PRIVATE_RECORD_VERSION_BOUND=REQUIRED
GATE_5_TARGET_RUNTIME_PRINCIPAL_EXACT_MATCH=REQUIRED
GATE_6_FRESH_HUMAN_AUTHORIZATION_REVIEW=REQUIRED
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

Until the private selection, immutable record, and ADC correlation all exist,
the Token Creator binding remains not authorization-designable.

## 6. Fail-closed rules

```text
MISSING_PRIVATE_AUTHORITY_RECORD=FAIL_CLOSED
MISSING_PRIVATE_RECORD_VERSION=FAIL_CLOSED
MISSING_EXACT_SOURCE_PRINCIPAL=FAIL_CLOSED
OPAQUE_REF_NOT_FOUND=FAIL_CLOSED
OPAQUE_REF_REASSIGNED=FAIL_CLOSED
TARGET_RUNTIME_PRINCIPAL_MISMATCH=FAIL_CLOSED
ADC_CORRELATION_NOT_RUN=FAIL_CLOSED
ADC_CORRELATION_MISMATCH=FAIL_CLOSED
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
ACCESS_TOKEN_PRINTED_OR_EXPORTED=NO
REFRESH_TOKEN_READ_OR_EXPOSED=NO
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
