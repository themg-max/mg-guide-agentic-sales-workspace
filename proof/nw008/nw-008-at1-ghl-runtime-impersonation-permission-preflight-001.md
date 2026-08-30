# NW-008 AT1 GHL Runtime Impersonation Permission Preflight 001

## 1. Artifact identity and boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_RUNTIME_IMPERSONATION_PERMISSION_PREFLIGHT_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-runtime-impersonation-permission-preflight-001.md
CLASSIFICATION=IAM_PERMISSION_READ_ONLY_PREFLIGHT
PR_CLASS=proof_only
MODE=READ_ONLY_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

OBSERVATION_TIMESTAMP_UTC=2026-08-30T00:42:35Z
OBSERVATION_TIMESTAMP_LOCAL=2026-08-29T20:42:35-0400
```

This unit resolves the exact source and target of the failed credential path,
then evaluates only the effective permission and relevant allow-policy state.
It does not mint a token, impersonate a service account, read a secret payload,
call HighLevel, or change IAM.

## 2. Bound terminal authority

```text
HIGHLEVEL_DIAGNOSTIC_PROOF_PR=303
HIGHLEVEL_DIAGNOSTIC_PROOF_MERGE_SHA=
  000c032dcf77efdabb33c7eb9c7285fa528280e8
HIGHLEVEL_DIAGNOSTIC_PROOF_PRESENT_ON_ORIGIN_MAIN=YES

BOUND_EXECUTION_PROOF_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_EXECUTION_PROOF_001
BOUND_EXECUTION_PROOF_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-opportunity-read-diagnostic-execution-proof-001.md
BOUND_EXECUTION_PROOF_BLOB_SHA=
  ab07b83c1213c97ba7aab982a78495afb30a3735

FAILURE_PHASE=IMPERSONATED_CREDENTIAL_ACQUISITION
REQUIRED_PERMISSION=iam.serviceAccounts.getAccessToken

GRANT_ID=
  NW008_AT1_GHL_REST_V3_OPPORTUNITY_READ_DIAGNOSTIC_GRANT_001
GRANT_CONSUMED=YES
GRANT_REUSABLE=NO
CONSUMED_GRANT_REUSED_BY_THIS_UNIT=NO
CONSUMED_GRANT_HUMAN_ACTIVATION_REUSED_BY_THIS_UNIT=NO
NEW_GHL_GRANT_CREATED=NO
```

PR #303 is terminal evidence for its consumed one-shot grant. This preflight
does not reopen that execution, reuse that grant or activation, or authorize
another provider request.

## 3. Exact principal binding

The exact source principal was resolved privately in process memory from the
existing ADC service-account impersonation metadata and compared only against
the exact target resource and required permission. Consistent with the existing
non-disclosure contract, the raw source identity is neither published nor
persisted here.

```text
SOURCE_PRINCIPAL=PRIVATE_EXACT_SOURCE_PRINCIPAL
SOURCE_PRINCIPAL_KIND=serviceAccount
SOURCE_PRINCIPAL_RESOLUTION=
  EXISTING_ADC_SERVICE_ACCOUNT_IMPERSONATION_TARGET
SOURCE_ADC_CONFIGURED_BY_THIS_UNIT=NO
SOURCE_PRINCIPAL_VALUE_PUBLISHED=NO
SOURCE_PRINCIPAL_VALUE_PERSISTED=NO
SOURCE_PRINCIPAL_BOUND=YES

FUTURE_DURABLE_SOURCE_BINDING_REQUIREMENT=
  PRIVATE_ATTESTATION_OR_REFERENCE_REQUIRED
FUTURE_DURABLE_SOURCE_BINDING_MAY_NOT_RELY_ON=
  ADC_FILE_MODIFICATION_TIME
FUTURE_PUBLIC_PROOF_MAY_PUBLISH_RAW_SOURCE_IDENTITY=NO

TARGET_PRINCIPAL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_PRINCIPAL_KIND=serviceAccount
TARGET_PROJECT=ai-rolodex-to-crm
TARGET_RUNTIME_CODE_BINDING_MATCH=YES
TARGET_SERVICE_ACCOUNT_EXISTS=YES
TARGET_SERVICE_ACCOUNT_PROJECT_MATCH=YES
TARGET_SERVICE_ACCOUNT_DISPLAY_NAME_MATCH=YES
TARGET_PRINCIPAL_BOUND=YES
```

The source is the principal whose effective access was evaluated. No alternate
operator, service account, credential file, or target was substituted.

## 4. Fresh effective-permission and binding observation

Read-only Policy Troubleshooter evaluated the exact source, target resource,
and permission. It did not call `generateAccessToken` and did not use
`--impersonate-service-account`.

```text
POLICY_TROUBLESHOOTER_RESOURCE=
  //iam.googleapis.com/projects/ai-rolodex-to-crm/serviceAccounts/mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
POLICY_TROUBLESHOOTER_PERMISSION=
  iam.serviceAccounts.getAccessToken
POLICY_TROUBLESHOOTER_EXIT=0
POLICY_TROUBLESHOOTER_OVERALL_ACCESS_STATE=CANNOT_ACCESS

EXACT_GET_ACCESS_TOKEN_PERMISSION_EFFECTIVE=NO
```

Sanitized allow-policy inspection found no exact source membership in
`roles/iam.serviceAccountTokenCreator` on either the target service account or
its project:

```text
TARGET_SERVICE_ACCOUNT_EXACT_TOKEN_CREATOR_BINDING_COUNT=0
PROJECT_EXACT_TOKEN_CREATOR_BINDING_COUNT=0
EXACT_RELEVANT_BINDING_PRESENT=NO

SOURCE_PRINCIPAL_BOUND=YES
TARGET_PRINCIPAL_BOUND=YES
EXACT_GET_ACCESS_TOKEN_PERMISSION_EFFECTIVE=NO
EXACT_RELEVANT_BINDING_PRESENT=NO
CONFLICTING_OR_AMBIGUOUS_STATE=NO
```

The effective-access result and exact relevant-binding observation agree.

## 5. Classification return

```text
GHL_IMPERSONATION_PREFLIGHT_STATUS=
  READY_FOR_BOUNDED_PERMISSION_AUTHORIZATION

IAM_MUTATIONS=0
LIVE_GHL_CALLS=0
SECRET_MANAGER_PAYLOAD_READS=0
```

This status permits only a later, separately governed authorization decision
for the exact source, exact target, and exact required permission. It does not
itself authorize or apply an IAM binding.

## 6. Recommended future authorization candidate (not executed here)

```text
FUTURE_AUTHORIZATION_CANDIDATE=
  NW008_AT1_GHL_RUNTIME_IMPERSONATION_TOKEN_MINT_PERMISSION_AUTHORIZATION_001

TARGET_RESOURCE_SCOPE=EXACT_TARGET_SERVICE_ACCOUNT
CANDIDATE_ROLE=roles/iam.serviceAccountTokenCreator
MAX_EXACT_MEMBER_ADDITIONS=1
MAX_IAM_POLICY_WRITES=1

PROJECT_LEVEL_TOKEN_CREATOR_GRANT_ALLOWED=NO
SERVICE_ACCOUNT_KEYS=0
SECRET_MANAGER_PAYLOAD_READS=0
LIVE_GHL_CALLS=0

FUTURE_SOURCE_BINDING_MUST_USE=
  DURABLE_PRIVATE_ATTESTATION_OR_REFERENCE
FUTURE_SOURCE_BINDING_MUST_NOT_RELY_ON=
  ADC_FILE_MODIFICATION_TIME
FUTURE_PUBLIC_PROOF_MUST_OMIT_RAW_SOURCE_IDENTITY=YES
```

Any later remediation unit must bind the exact source privately through a
durable private attestation or reference, keep the raw source identity out of
the public proof, and remain limited to the exact target service-account
resource scope. After future GHL IAM remediation is proven, a fresh read-only
credential readiness check is required before any new provider diagnostic
execution chain is prepared. The consumed diagnostic grant and its human
activation must not be reused.

## 7. Isolation and stop

```text
IAM_POLICY_WRITES=0
IAM_ROLE_GRANTS=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
GENERATE_ACCESS_TOKEN_CALLS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
SECRET_MANAGER_PAYLOAD_READS=0
PIT_ROTATIONS=0
GHL_SCOPE_CHANGES=0
ALTERNATE_CREDENTIALS_USED=0
LIVE_GHL_CALLS=0
CRM_READS=0
CRM_WRITES=0
NEW_GHL_GRANTS=0

FLEET_EXECUTION_AUTHORITY_JOINED=NO
GHL_PROVIDER_READ_PATH_PROVEN=NO
CONVERGENCE_AUTHORIZED=NO

NEXT=
  SEPARATE_EXACT_TOKEN_MINT_PERMISSION_AUTHORIZATION_AFTER_THIS_PROOF_MERGES

STOP_CODE=
  NW008_AT1_GHL_RUNTIME_IMPERSONATION_PERMISSION_PREFLIGHT_001_COMPLETE
STOP
```
