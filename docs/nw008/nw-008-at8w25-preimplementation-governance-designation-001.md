# NW-008 AT8W25 Preimplementation Governance Designation 001

## 1. Unit identity and boundary

```text
UNIT=NW008_AT8W25_PREIMPLEMENTATION_GOVERNANCE_DESIGNATION_001
MODE=GOVERNANCE_DESIGNATION_RECORDING_ONLY
WORKSTREAM=NW-008
CLASSIFICATION=planning_only
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

RESOLUTION_BASE_REF=origin/main
RESOLUTION_BASE_SHA=b1e3d2b4a02584f5fa6e69dd2d499c6afe83db74
RESOLUTION_ARTIFACT=
  docs/nw008/nw-008-at8w25-preimplementation-governance-designation-001.md

PLANNING_ONLY=YES
RUNTIME_IMPLEMENTATION_AUTHORIZED_BY_THIS_ARTIFACT=NO
MUTATION_AUTHORITY_CREATED=NO
SECRET_PAYLOAD_READ_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
TOKEN_MINT_AUTHORIZED=NO
HIGHLEVEL_CALL_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
RUNTIME_START_AUTHORIZED=NO
SQLITE_CREATION_AUTHORIZED=NO
```

This artifact records the final human-governed dependency-manifest and B2 PIT
version designations needed to make a later bounded B2/C4/C3/C2 implementation
authorization designable. It does not itself authorize implementation or any
runtime or external effect.

## 2. Dependency designations

```text
DEPENDENCY_DECLARATION_AUTHORITY=pyproject.toml
CI_PIN_SURFACE=requirements.txt
DEPENDENCY_SYNCHRONIZATION_POLICY=
  New direct runtime dependencies declared in pyproject.toml must also be
  represented with the approved exact pin in requirements.txt while
  deterministic CI installs from requirements.txt.

DOCKERFILE_DEPENDENCY_SURFACE=OUT_OF_SCOPE_FOR_CURRENT_OFFLINE_IMPLEMENTATION

GOOGLE_CLOUD_SECRET_MANAGER_PACKAGE=google-cloud-secret-manager
GOOGLE_CLOUD_SECRET_MANAGER_VERSION_POLICY=EXACT_PIN
GOOGLE_CLOUD_SECRET_MANAGER_VERSION=2.27.0
GOOGLE_CLOUD_SECRET_MANAGER_DECLARATION=google-cloud-secret-manager==2.27.0
```

Human governance designates version `2.27.0` because it is an official Google
Secret Manager client release compatible with the repository's Python 3.9 CI.
The later implementation must not substitute the moving latest release while
CI remains on Python 3.9.

## 3. B2 GHL PIT version designation

```text
B2_PIT_SECRET_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL
B2_PIT_VERSION_POLICY=EXACT_NUMERIC
B2_PIT_VERSION=1
B2_PIT_EXACT_VERSION_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1
B2_PIT_LATEST_ALLOWED=NO
```

The future B2 production accessor is restricted to the exact version resource
above. It must not resolve, append, request, or accept `latest`, another alias,
another numeric version, or a caller-supplied resource override.

## 4. C4 commitment-key version designation

```text
C4_COMMITMENT_SECRET_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY
C4_COMMITMENT_VERSION_POLICY=EXACT_NUMERIC
C4_COMMITMENT_VERSION=1
C4_COMMITMENT_EXACT_VERSION_RESOURCE=
  projects/ai-rolodex-to-crm/secrets/MG_GUIDE_NW008_COMMITMENT_KEY/versions/1
C4_COMMITMENT_LATEST_ALLOWED=NO
```

## 5. Normalized implementation surface

```text
B2_WRITABLE_PATH=
  src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
C4_WRITABLE_PATH=
  src/integrations/ghl/at1_commitment_key_provider.py
C3_C2_WRITABLE_PATH=
  src/integrations/ghl/highlevel_rest/live_note_runtime.py

DEPENDENCY_WRITABLE_PATHS=
  pyproject.toml|
  requirements.txt

TEST_WRITABLE_PATHS=
  tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py|
  tests/integrations/ghl/test_at1_commitment_key_provider.py|
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py

REFERENCE_ONLY_PATHS=
  src/integrations/ghl/at1_execution_store.py

BLOCKED_PATHS_INCLUDE=
  Dockerfile|
  src/integrations/ghl/highlevel_rest/live_note_transport.py|
  src/integrations/ghl/highlevel_rest/live_note_http_client.py|
  src/integrations/ghl/highlevel_rest/note_path.py|
  /Users/achandler/Library/Application Support/mg-guide/nw008/runtime.env|
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3
```

`At1ExecutionStore` remains reference-only unless later implementation work
finds a concrete defect that cannot be resolved within the authorized
composition-root surface. Any such defect requires a new scope decision before
that file is modified.

## 6. Readiness and effect ledger

```text
DEPENDENCY_SYNCHRONIZATION_POLICY_RECORDED=YES
GOOGLE_CLOUD_SECRET_MANAGER_VERSION_RECORDED=YES
B2_PIT_POLICY_RECORDED=YES

IMPLEMENTATION_SCOPE_NORMALIZED=YES
IMPLEMENTATION_AUTHORIZATION_READY=YES
IMPLEMENTATION_AUTHORIZATION_GRANTED_BY_THIS_ARTIFACT=NO

REPOSITORY_MUTATIONS=DESIGNATION_ARTIFACT_ONLY
SECRET_PAYLOAD_READS=0
TOKEN_MINTS=0
IAM_MUTATIONS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SQLITE_CREATED=NO

NEXT=
  Return this designation artifact to ChatGPT for final bounded implementation
  authorization.
```
