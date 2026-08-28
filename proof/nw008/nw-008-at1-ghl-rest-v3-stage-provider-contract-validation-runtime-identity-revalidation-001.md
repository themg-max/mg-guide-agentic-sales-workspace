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

LOCAL_RUNTIME_ADC_WRAPPER_CLASS=
  google.auth.impersonated_credentials.Credentials

LOCAL_RUNTIME_ADC_PRECONFIGURED_IMPERSONATION_PRESENT=YES

LOCAL_ADC_EMBEDDED_IMPERSONATION_TARGET_MATCHES_MG_GUIDE_TARGET_SA=NO

GOVERNED_SOURCE_PRINCIPAL_CORRELATION=UNKNOWN

RUNTIME_IDENTITY_PARITY_WITH_AT8W24=NO

IAM_REMEDIATION_REQUIRED=UNKNOWN
CREDENTIAL_CONTROL_PLANE_READY=NO
GRANT_002_PREPARATION_READY=NO

PRIVATE_PRINCIPAL_PUBLISHED=NO

RATIONALE=
  The prior wording of this section ("RUNTIME_ADC_SOURCE_PRINCIPAL_
  CORRELATION=MISMATCH") overstated what was actually established. The
  workstation's default ADC file happened to be locally configured as an
  impersonated_service_account wrapper (source_credentials +
  service_account_impersonation_url) whose embedded impersonation target
  is a different service account than the MG Guide runtime target SA.
  That is evidence of *local ADC configuration drift on this workstation*
  — it says nothing, by itself, about whether the underlying
  privately-governed human source principal (the one previously
  correlated in NW008 AT8W24 as ADC_CREDENTIAL_TYPE=authorized_user)
  still holds the required project/SA-level roles/iam.
  serviceAccountTokenCreator grant. No evidence was gathered in this unit
  that speaks to that underlying governed-principal question either way,
  so the correlation is correctly recorded as UNKNOWN rather than
  MISMATCH, and the control plane is treated as fail-closed pending a
  revalidation performed through a clean, isolated ADC (see Section 8).
```

## 6. Effective token-creator revalidation — NOT PERFORMED

```text
STEP=EFFECTIVE_TOKEN_CREATOR_REVALIDATION
GATING_CONDITION=GOVERNED_SOURCE_PRINCIPAL_CORRELATION == MATCH
GATING_CONDITION_MET=NO (correlation = UNKNOWN)

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
  GOVERNED_SOURCE_PRINCIPAL_CORRELATION resolved to UNKNOWN rather than
  MATCH. This unit's normalization corrected an earlier overstatement
  (RUNTIME_ADC_SOURCE_PRINCIPAL_CORRELATION=MISMATCH): the observed
  impersonated_credentials wrapper with a non-matching embedded
  impersonation target is evidence of local ADC configuration drift on
  this workstation, not proof that the underlying governed human source
  principal lacks the required grant. Per instruction, effective Token
  Creator revalidation against the target service account was NOT
  performed using this ambiguous runtime identity, and no IAM
  remediation scope is being proposed in this unit because the correct
  source principal's actual standing has not yet been established via a
  clean, isolated ADC. Local pinned-venv google.auth.default() resolution
  in this workstation environment is itself only a proxy for the
  deployed production runtime's credential resolution and should not be
  treated as equivalent to it without an explicit, separately governed
  identity-parity confirmation.

NEXT=
  RETURN_RUNTIME_IDENTITY_REVALIDATION_PR_TO_CHATGPT
  (per action instructions; do not prepare GRANT_002 or any IAM
  remediation authorization scope from this unit)
```

## 8. Isolated ADC config + blocked human-operator login (this amendment)

```text
STEP=CREATE_ISOLATED_CLOUD_SDK_CONFIG
WORKTREE_ROOT=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
NW008_GCLOUD_CONFIG=
  local/runtime/nw008-stage-provider-validation/gcloud-config
NW008_GCLOUD_CONFIG_CREATED=YES
NW008_GCLOUD_CONFIG_IS_GIT_IGNORED=YES
EXISTING_WORKSTATION_ADC_COPIED_INTO_ISOLATED_CONFIG=NO
NW008_GCLOUD_CONFIG_CONTENTS_AFTER_SETUP=EMPTY

STEP=HUMAN_ADC_LOGIN
REQUIRED_COMMAND=
  CLOUDSDK_CONFIG=<isolated NW008_GCLOUD_CONFIG path> \
    gcloud auth application-default login
REQUIRED_COMMAND_MUST_NOT_INCLUDE=
  --impersonate-service-account
COMMAND_EXECUTED_BY_AGENT=NO
REASON=
  This step requires an interactive human/browser OAuth consent flow
  authenticating the exact privately governed source identity from the
  prior NW008 AT8W24 correlation. The agent cannot supply that consent
  or principal on the human operator's behalf, and no human operator was
  available in this turn to complete it interactively. Per the action's
  own framing ("Human operator:"), this step is intentionally left to a
  human to perform out-of-band.
HUMAN_ADC_LOGIN_COMPLETED=NO

STEPS_4_5_6_STATUS=BLOCKED_PENDING_HUMAN_ADC_LOGIN
STEP_4_PINNED_RUNTIME_REVALIDATION=NOT_PERFORMED
STEP_5_PRIVATE_CORRELATION=NOT_PERFORMED
STEP_6_SAME_CREDENTIAL_IAM_TEST=NOT_PERFORMED

GOVERNED_SOURCE_PRINCIPAL_CORRELATION=UNKNOWN
FAIL_CLOSED=YES

# No secret payload, token, ADC JSON, or principal was read, minted,
# printed, or persisted while probing/creating the isolated config
# directory. The isolated config directory remains empty.

NEXT_FOR_HUMAN_OPERATOR=
  1. Run, in your own terminal (not relayed through this agent):
     CLOUDSDK_CONFIG=local/runtime/nw008-stage-provider-validation/gcloud-config \
       gcloud auth application-default login
     (do NOT pass --impersonate-service-account)
  2. Authenticate as the exact privately governed NW008 source identity.
  3. Notify the orchestrator that login is complete so Steps 4-6 of this
     unit (pinned-runtime revalidation, private correlation, and the
     same-credential testIamPermissions check) can proceed.
```

## 9. Prohibited-effects attestation

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

## 10. Git

```text
GIT_DIFF_CHECK=CLEAN
STAGED_PATHS=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-runtime-identity-revalidation-001.md
GIT_ADD_DOT_USED=NO
MERGE_PERFORMED=NO
AMENDMENT_TO=PR276
```
