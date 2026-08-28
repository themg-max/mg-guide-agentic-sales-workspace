# NW-008 AT1 GHL REST v3 Stage Provider Contract Validation — Runtime Identity Revalidation 001

## 1. Unit identity

```text
UNIT=CORRECT_NW008_STAGE_PROVIDER_RUNTIME_IDENTITY_REVALIDATION
MODE=READ_ONLY_RUNTIME_IDENTITY_RESOLUTION_AND_CORRELATION
WORKSTREAM=NW-008
CLASSIFICATION=execution_proof
PR_CLASS=execution_proof
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

STEP_SCOPE=
  PREFLIGHT +
  RUNTIME_ADC_RESOLUTION (google.auth.default(), pinned venv) +
  PRIVATE_SOURCE_CORRELATION +
  CONDITIONAL_EFFECTIVE_TOKEN_CREATOR_REVALIDATION

IAM_MUTATION_AUTHORIZED=NO
SECRET_MANAGER_MUTATION_AUTHORIZED=NO
TARGET_SA_IMPERSONATION_AUTHORIZED=NO
TARGET_SA_ACCESS_TOKEN_MINT_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATE_AUTHORIZED=NO

PROOF_ARTIFACT=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-runtime-identity-revalidation-001.md
PROOF_BRANCH=
  proof/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-runtime-identity-revalidation-001
BASE_REF=origin/main
BASE_SHA=cb031f9bdabe058123943dc2d5706f4d1a3316cd
PR275_MERGE_SHA_REQUIRED=cb031f9bdabe058123943dc2d5706f4d1a3316cd
PR275_MERGE_SHA_PRESENT_ON_ORIGIN_MAIN=YES

TARGET_PROJECT=ai-rolodex-to-crm
TARGET_SERVICE_ACCOUNT=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_SECRET=MG_GUIDE_PIT_GHL
REQUIRED_ROLE_IF_REMEDIATION_LATER_NEEDED=
  roles/iam.serviceAccountTokenCreator
REQUIRED_PERMISSION=
  iam.serviceAccounts.getAccessToken

PINNED_RUNTIME_PYTHON=
  local/runtime/nw008-stage-provider-validation/.venv/bin/python
SYSTEM_PYTHON_USED=NO

RECORDED_AT_UTC=2026-08-28T21:01:06Z
OPERATOR=VS_CODE_ORCHESTRATOR (Copilot CLI agent session)
```

## 2. Privacy / non-disclosure controls

```text
PRIVATE_PRINCIPAL_PUBLICATION=FORBIDDEN
PRIVATE_PRINCIPAL_PERSISTENCE=FORBIDDEN

PRIVATE_PRINCIPAL_PUBLISHED=NO
PRIVATE_PRINCIPAL_PERSISTED=NO
PRIVATE_PRINCIPAL_PRESENT_IN_PROOF=NO
PRIVATE_PRINCIPAL_PRESENT_IN_GIT=NO
PRIVATE_PRINCIPAL_PRESENT_IN_SESSION_STATE_FILES=NO

ACCESS_TOKEN_PRINTED=NO
REFRESH_TOKEN_PRINTED=NO
CLIENT_SECRET_PRINTED=NO
ADC_JSON_CONTENTS_PRINTED=NO
SECRET_PAYLOAD_PRINTED=NO

# Runtime identity resolution and correlation were computed entirely in
# process memory (a single Python process using the pinned venv). Only
# non-secret structural facts (credential class name, boolean comparison
# outcomes, HTTP status codes, YES/NO/MATCH-style predicates) are recorded
# below. No email address, token, ADC JSON body, or secret payload is
# present anywhere in this artifact or in git history for this branch.
```

## 3. Preflight

```text
PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
STARTING_BRANCH=
  proof/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-credential-readiness-001
BRANCH_WAS_MAIN=NO
ABORT_IF_BRANCH_MAIN=NOT_TRIGGERED

WORKING_TREE_UNTRACKED_ENTRY_PRESENT=YES
  PATH=
    proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-execution-proof-001.md
  NOTE=
    Pre-existing untracked artifact from a prior unit; left untouched and
    NOT staged by this unit.

ORIGIN_MAIN_FETCHED=YES
ORIGIN_MAIN_SHA=cb031f9bdabe058123943dc2d5706f4d1a3316cd
PR275_MERGE_SHA_REQUIRED=cb031f9bdabe058123943dc2d5706f4d1a3316cd
PR275_MERGE_SHA_IS_ANCESTOR_OF_ORIGIN_MAIN=YES

PROOF_WORK_BRANCH_CREATED=
  proof/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-runtime-identity-revalidation-001
PROOF_WORK_BRANCH_BASE=origin/main
PROOF_WORK_BRANCH_BASE_SHA=cb031f9bdabe058123943dc2d5706f4d1a3316cd
WORKED_DIRECTLY_ON_MAIN=NO

PINNED_PYTHON_EXISTS=YES
PINNED_PYTHON_PATH=
  local/runtime/nw008-stage-provider-validation/.venv/bin/python
SYSTEM_PYTHON_USED=NO
GOOGLE_AUTH_IMPORTABLE_IN_PINNED_VENV=YES
GOOGLE_AUTH_VERSION=2.57.0

KNOWN_READY_STATE_ACCEPTED_WITHOUT_REMODIFICATION=
  TARGET_SERVICE_ACCOUNT_EXISTS=YES
  TARGET_SERVICE_ACCOUNT_DISABLED=NO
  TARGET_SECRET_EXISTS=YES
  EXACT_SECRET_ACCESSOR_BINDING_PRESENT=YES
  SECRET_MANAGER_REMEDIATION_REQUIRED=NO
  SERVICE_ACCOUNT_REMEDIATION_REQUIRED=NO
NO_MODIFICATIONS_MADE_TO_ABOVE_RESOURCES=YES

PRECONDITION_GATE=PASSED
```

## 4. Runtime identity resolution (google.auth.default(), pinned venv only)

```text
STEP=RUNTIME_ADC_RESOLUTION
METHOD=
  google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
  executed via local/runtime/nw008-stage-provider-validation/.venv/bin/python
  (the exact pinned runtime interpreter; system python NOT used)

RUNTIME_GOOGLE_AUTH_DEFAULT_RESOLVES=YES
RUNTIME_ADC_CREDENTIAL_CLASS=
  google.auth.impersonated_credentials.Credentials
RUNTIME_CREDENTIAL_REFRESH_OK=YES

# Note: this differs materially from the credential class observed in
# earlier lane validation (NW008 AT8W24), which recorded
# ADC_CREDENTIAL_TYPE=authorized_user. A prior unit in this session had
# also inferred ADC_CREDENTIAL_TYPE=other by reading only the raw ADC
# JSON `type` field. This unit deliberately avoided both of those
# shortcuts and instead resolved the credential object through the
# pinned runtime's google.auth.default(), per the corrective instruction
# in this task. That resolution surfaced that the local ADC used by this
# workstation is configured as an *impersonated_service_account* ADC
# (source_credentials + service_account_impersonation_url), which
# google-auth wraps as `impersonated_credentials.Credentials` — not a
# plain `authorized_user` (Credentials) object and not the target
# service account's own compute/metadata identity.
```

## 5. Private source correlation

```text
STEP=PRIVATE_SOURCE_CORRELATION
CORRELATION_METHOD=
  IN_MEMORY_STRUCTURAL_COMPARISON
  (single process; no principal value printed, logged, or persisted)

STRUCTURAL_FACT_1=
  RUNTIME_ADC_CREDENTIAL_CLASS is google.auth.impersonated_credentials.Credentials,
  not google.oauth2.credentials.Credentials (authorized_user), which was the
  credential class underlying the previously governed correlation in
  NW008 AT8W24 (ADC_CREDENTIAL_TYPE=authorized_user).

STRUCTURAL_FACT_2=
  The impersonation target embedded in the ADC's
  service_account_impersonation_url was compared in-memory against the
  exact TARGET_SERVICE_ACCOUNT string. Only the boolean result is recorded:
  IMPERSONATION_TARGET_MATCHES_TARGET_SA=NO

STRUCTURAL_FACT_3=
  Read-only attempts to enumerate roles/iam.serviceAccountTokenCreator
  bindings (target-SA-level IAM policy and project-level IAM policy) using
  this runtime-resolved credential did not return a usable policy body
  (non-200 / non-enumerable response) for correlation purposes:
  TARGET_SA_TOKEN_CREATOR_POLICY_READ=NO
  PROJECT_TOKEN_CREATOR_POLICY_READ=NO

RUNTIME_ADC_SOURCE_PRINCIPAL_CORRELATION=MISMATCH
PRIVATE_PRINCIPAL_PUBLISHED=NO

RATIONALE=
  The runtime-resolved credential chain is structurally different in kind
  (impersonated_credentials wrapping an unrelated impersonation target)
  from the previously governed/correlated source principal basis
  (a plain authorized_user identity), and its embedded impersonation
  target is confirmed (boolean-only) to NOT be the exact target service
  account required for GRANT_002. This is sufficient to determine the
  runtime-selected source principal does not correlate to the governed
  designation without needing to print or persist either principal value.
```

## 6. Effective token-creator revalidation — NOT PERFORMED

```text
STEP=EFFECTIVE_TOKEN_CREATOR_REVALIDATION
GATING_CONDITION=RUNTIME_ADC_SOURCE_PRINCIPAL_CORRELATION == MATCH
GATING_CONDITION_MET=NO (correlation = MISMATCH)

PER_INSTRUCTION=
  "If correlation is not MATCH: EFFECTIVE_PERMISSION_EVALUATION_VALID=NO,
   IAM_REMEDIATION_REQUIRED=UNKNOWN, GRANT_002_PREPARATION_READY=NO, STOP."

ADC_TEST_IAM_GET_ACCESS_TOKEN_ON_TARGET_SA=NOT_EVALUATED
SAME_RUNTIME_ADC_IDENTITY_USED_FOR_PERMISSION_EVALUATION=NOT_APPLICABLE
EFFECTIVE_TOKEN_CREATOR_ACCESS_READY=NO

TARGET_SA_IMPERSONATION_ATTEMPTED=NO
TARGET_SA_ACCESS_TOKEN_MINT_ATTEMPTED=NO
SECRET_MANAGER_PAYLOAD_ACCESSED=NO
GHL_CALL_MADE=NO
CRM_MUTATION_MADE=NO
```

## 7. Decision

```text
EFFECTIVE_PERMISSION_EVALUATION_VALID=NO
IAM_REMEDIATION_REQUIRED=UNKNOWN
CREDENTIAL_CONTROL_PLANE_READY=NO
GRANT_002_PREPARATION_READY=NO

STOP_TRIGGERED=YES
STOP_REASON=
  RUNTIME_ADC_SOURCE_PRINCIPAL_CORRELATION resolved to MISMATCH rather than
  MATCH. Per instruction, effective Token Creator revalidation against the
  target service account was NOT performed using this runtime identity,
  and no IAM remediation scope is being proposed in this unit because the
  correct source principal (the one that should hold, or be evaluated for,
  roles/iam.serviceAccountTokenCreator on the target SA) has not yet been
  established for the actual production runtime path. Local pinned-venv
  google.auth.default() resolution in this workstation environment is
  itself only a proxy for the deployed production runtime's credential
  resolution and should not be treated as equivalent to it without an
  explicit, separately governed identity-parity confirmation.

NEXT=
  RETURN_RUNTIME_IDENTITY_REVALIDATION_PR_TO_CHATGPT
  (per action instructions; do not prepare GRANT_002 or any IAM
  remediation authorization scope from this unit)
```

## 8. Prohibited-effects attestation

```text
IAM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0
SECRET_PAYLOAD_READS=0
TARGET_SA_IMPERSONATION_ATTEMPTS=0
TARGET_SA_ACCESS_TOKEN_MINTS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 9. Git

```text
GIT_DIFF_CHECK=CLEAN
STAGED_PATHS=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-runtime-identity-revalidation-001.md
GIT_ADD_DOT_USED=NO
MERGE_PERFORMED=NO
```
