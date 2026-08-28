# NW-008 AT-1 — GHL REST v3 Stage Provider Contract Validation Credential Readiness Proof 001

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_CREDENTIAL_READINESS_PROOF_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-credential-readiness-proof-001.md
ARTIFACT_KIND=SANITIZED_LOCAL_CREDENTIAL_RUNTIME_READINESS_PROOF
PR_CLASS=proof_only
UNIT=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_CREDENTIAL_READINESS_001
ACTION=
  REMEDIATE_NW008_STAGE_PROVIDER_VALIDATION_CREDENTIAL_RUNTIME_AND_PROVE_READINESS
ACTION_TYPE=create
OWNER=VS_CODE_ORCHESTRATOR

PUBLIC_REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PROOF_BRANCH=
  proof/nw008-at1-ghl-rest-v3-stage-provider-contract-validation-credential-readiness-001
PROOF_BRANCH_IS_MAIN=NO
BASE_REF=origin/main
BASE_SHA=b0df125e905b4d81b170f0ae16ccbb511b8662b6

RECORDED_AT_UTC=2026-08-28T20:45:31Z
```

## 0. Authority boundary

This unit restores a host-local gitignored interpreter from already-declared
manifest dependencies and proves import/composition readiness. It does **not**
retry GRANT_001, access Secret Manager payloads, mint tokens, impersonate over
the network, call HighLevel, or mutate CRM/IAM.

```text
GRANT_001_CONSUMED=YES
GRANT_001_RETRY_AUTHORIZED=NO
GRANT_001_REUSE_AUTHORIZED=NO
SECOND_EXECUTION_UNDER_GRANT_001=FORBIDDEN

LAST_STOP_CODE=
  NW008_STAGE_PROVIDER_CONTRACT_VALIDATION_FAIL_CREDENTIAL_ACQUISITION_AFTER_CONSUMPTION_ZERO_BUSINESS_CALLS
LAST_PROVIDER_BUSINESS_CALLS=0
LAST_CRM_MUTATIONS=0

VALIDATION_EXECUTION_AUTHORIZED=NO
THREE_CALL_REST_VALIDATION_AUTHORIZED=NO
GRANT_002_CREATED_BY_THIS_UNIT=NO
SELF_ACTIVATION=FORBIDDEN
```

## 1. Preflight

```text
WORKSPACE_MATCH=YES
BRANCH_NOT_MAIN=YES
ABORT_IF_BRANCH_MAIN=YES
LOCAL_PRIVATE_LANE_GITIGNORED=YES
ORIGIN_MAIN_SHA=b0df125e905b4d81b170f0ae16ccbb511b8662b6
```

`local/` remains gitignored (`.gitignore` rule `local/`). The isolated
interpreter created by this unit is therefore not a public-tree change.

## 2. Root cause (recorded, not re-opened)

GRANT_001's one-shot attempt consumed the grant, then stopped before any
HighLevel business call because the **host-local execution interpreter** lacked
the already-declared Secret Manager client library.

```text
ROOT_CAUSE=
  HOST_LOCAL_EXECUTION_INTERPRETER_MISSING_DECLARED_DEPENDENCY
DECLARED_DEPENDENCY=
  google-cloud-secret-manager==2.27.0
PUBLIC_MANIFEST_CHANGE_REQUIRED=NO
```

The public manifest already pins the dependency. No `requirements.txt` or
`pyproject.toml` change is required or performed.

## 3. Isolated local interpreter restore

```text
VENV=local/venv-nw008-stage-provider-validation
EXECUTION_INTERPRETER_GITIGNORED=YES
CREATED_OR_REUSED_EXISTING_VENV=YES
PIP_INSTALL_SOURCE=requirements.txt
PUBLIC_MANIFEST_CHANGED=NO
NEW_DEPENDENCY_INTRODUCED=NO
```

Remediation class:

```text
REMEDIATION_CLASS=
  HOST_LOCAL_GITIGNORED_INTERPRETER_RESTORE_OF_ALREADY_DECLARED_MANIFEST_DEPENDENCIES
```

This unit did not modify `pyproject.toml`, `requirements.txt`, `src/**`,
`tests/**`, `contracts/**`, IAM, or Secret Manager.

## 4. Local-only readiness check

Performed with `PYTHONPATH=src` against the isolated interpreter. Imports only.
No Secret Manager `access_secret_version`, no ADC token mint, no impersonation
network attempt, no HighLevel HTTP.

```text
GOOGLE_CLOUD_SECRET_MANAGER_IMPORTABLE=YES
GOOGLE_AUTH_IMPORTABLE=YES
IMPERSONATED_CREDENTIALS_IMPORTABLE=YES
REPO_CREDENTIAL_PROVIDER_IMPORTABLE=YES
REPO_RUNTIME_COMPOSITION_IMPORTABLE=YES
SECRET_MANAGER_PACKAGE_VERSION=2.27.0
PIP_CHECK=PASS
```

Imported modules (names only):

- `google.cloud.secretmanager`
- `google.auth`
- `google.auth.impersonated_credentials`
- `integrations.ghl.highlevel_rest.live_note_credential_provider`
- `integrations.ghl.highlevel_rest.live_note_runtime`

`pip check` reported no broken requirements.

## 5. Normalized future execution route (not executed here)

Future GRANT_002 execution, if separately authorized and countersigned, MUST
use the repository-owned credential composition and MUST NOT reuse GRANT_001's
inline `SecretManagerServiceClient()` default-credentials path.

```text
FUTURE_CREDENTIAL_ROUTE=
  source ADC
  -> target-runtime service-account impersonated credentials
  -> SecretManagerServiceClient(credentials=target_runtime_credentials)
  -> GoogleSecretManagerLiveNoteSecretAccessor
  -> designated MG_GUIDE_PIT_GHL secret version

DO_NOT_REUSE_DIRECT_DEFAULT_SECRET_MANAGER_CLIENT=YES
REPO_OWNED_COMPOSITION_REQUIRED=YES
```

Repository composition already implements this route in
`src/integrations/ghl/highlevel_rest/live_note_runtime.py`
(`_resolve_source_application_credentials` →
`_impersonate_target_runtime_credentials` →
`_new_secret_manager_client` →
`GoogleSecretManagerLiveNoteSecretAccessor`).

This unit did not invoke that composition for live secret access.

## 6. Prohibited-surface ledger

```text
SECRET_MANAGER_ACCESS_SECRET_VERSION=0
SECRET_PAYLOAD_READS=0
ADC_TOKEN_MINTS=0
SERVICE_ACCOUNT_IMPERSONATION_NETWORK_ATTEMPTS=0

GHL_INTERACTION_PERFORMED=NO
REST_NETWORK_CALLS_TO_GHL=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MANAGER_MUTATIONS=0

DID_NOT_READ_MG_GUIDE_PIT_GHL=YES
DID_NOT_PRINT_OR_RESOLVE_GHL_PIT=YES
DID_NOT_ISSUE_GET_OPPORTUNITIES=YES
DID_NOT_ISSUE_PUT_OPPORTUNITIES=YES
DID_NOT_USE_ALTERNATE_ENVIRONMENT_TOKEN=YES
DID_NOT_USE_GCLOUD_SECRET_ACCESS_FALLBACK=YES
DID_NOT_MODIFY_IAM=YES
DID_NOT_MODIFY_SECRET_MANAGER=YES
DID_NOT_RETRY_GRANT_001=YES
```

## 7. Grant-002 preparation consequence

Local, non-network dependency-readiness gates are now proven for a **future**
grant. GRANT_002 is not created by this unit. When drafted, GRANT_002 MUST:

- bind AUTHORIZATION_001
- bind the same sealed package/digest
- bind consumed EXECUTION_PROOF_001 merge SHA
- bind CREDENTIAL_READINESS_PROOF_001 merge SHA (this artifact after merge)
- use a fresh human countersignature/window
- preserve GET → PUT → GET
- preserve `MAX_READS=2`, `MAX_WRITES=1`, `MAX_TOTAL_BUSINESS_CALLS=3`
- preserve `NO_RETRY`, `NO_ALTERNATE_BODY`, `NO_ALTERNATE_TARGET`,
  `NO_COMPENSATING_MUTATION`, `NO_AUTOMATIC_CLEANUP`
- place all local, non-network dependency-readiness gates **before** the
  irreversible grant-consumption trigger

```text
NEW_GRANT_PREPARATION_READY=YES
GRANT_002_CREATED_BY_THIS_UNIT=NO
GRANT_002_COUNTERSIGNED=NO
VALIDATION_EXECUTION_AUTHORIZED=NO
```

## 8. Required public return block

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_CREDENTIAL_READINESS_PROOF_001

PR_CLASS=proof_only
MODE=LOCAL_INTERPRETER_READINESS_ONLY

REMEDIATION_CLASS=
  HOST_LOCAL_GITIGNORED_INTERPRETER_RESTORE_OF_ALREADY_DECLARED_MANIFEST_DEPENDENCIES

PUBLIC_MANIFEST_CHANGED=NO
NEW_DEPENDENCY_INTRODUCED=NO
EXECUTION_INTERPRETER_GITIGNORED=YES

GOOGLE_CLOUD_SECRET_MANAGER_IMPORTABLE=YES
GOOGLE_AUTH_IMPORTABLE=YES
IMPERSONATED_CREDENTIALS_IMPORTABLE=YES
REPO_CREDENTIAL_PROVIDER_IMPORTABLE=YES
REPO_RUNTIME_COMPOSITION_IMPORTABLE=YES

SECRET_MANAGER_PACKAGE_VERSION=2.27.0
PIP_CHECK=PASS

SECRET_PAYLOAD_READS=0
GHL_CALLS=0
CRM_MUTATIONS=0

GRANT_001_CONSUMED=YES
GRANT_001_RETRY_AUTHORIZED=NO
SECOND_EXECUTION_UNDER_GRANT_001=FORBIDDEN

NEW_GRANT_PREPARATION_READY=YES

STOP_CODE=
  NW008_STAGE_PROVIDER_VALIDATION_CREDENTIAL_RUNTIME_READINESS_PROVEN_GRANT_002_NOT_CREATED

NEXT=
  CREATE_NW008_AT1_GHL_REST_V3_STAGE_PROVIDER_CONTRACT_VALIDATION_GRANT_002
```

## 9. Stop

```text
STOP
```
