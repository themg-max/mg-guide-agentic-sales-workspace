# NW-008 AT8W24 Lane C Runtime Config Surface Designation 001

## 1. Unit identity and planning-only boundary

```text
UNIT=NW008_AT8W24_LANE_C_RUNTIME_CONFIG_SURFACE_DESIGNATION_001
PR_CLASS=planning_only
MODE=HUMAN_GOVERNED_CONFIGURATION_SURFACE_DESIGNATION
WORKSTREAM=NW-008
CLASSIFICATION=configuration_surface_designation
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

RESOLUTION_BASE_REF=origin/main
RESOLUTION_BASE_SHA=02505505ebb3b6930504660d20a4f27446f4e65b
RESOLUTION_ARTIFACT=
  docs/nw008/nw-008-at8w24-lane-c-runtime-config-surface-designation-001.md

PLANNING_ONLY=YES
READ_ONLY=YES
NO_MUTATION_AUTHORIZATION=YES
MUTATION_AUTHORITY_CREATED=NO
RUNTIME_RESOLUTION_AUTHORIZED=NO
CONFIG_MUTATION_AUTHORIZED=NO
HOST_MUTATION_AUTHORIZED=NO
STORE_WRITE_AUTHORIZED=NO

EXTERNAL_EFFECTS=0
IAM_MUTATIONS=0
CONFIG_MUTATIONS=0
STORE_WRITES=0
SECRET_PAYLOAD_READS=0
TOKEN_MINTS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
```

This unit is a human-governed, planning-only designation of the exact durable
NW-008 production runtime configuration-delivery surface. Completing this
designation does **not** authorize configuration application, parent-directory
creation, SQLite database creation, environment-variable mutation, runtime
start, IAM change, secret access, or any other external effect.

AT8W23 Lane C remains only partially unblocked by this unit: the configuration
surface is now designated. Actual Lane C host/config closure
(parent-directory provision + root-owned key install + read-only verification)
still requires a separate human-governed execution authorization.

## 2. Preconditions

```text
PR195_MERGED=YES
  merge_commit=02505505ebb3b6930504660d20a4f27446f4e65b
  reviewed_head=ef707d9c5f21370750784b9cd6e850e0ef22ade3
  REVIEWED_HEAD_ANCESTRY=PASS

LANE_B_STATUS=COMPLETE
C4_EXTERNAL_PREREQUISITES_READY=YES
  EVIDENCE=
    proof/nw008/at-8w24/nw008-at8w24-lane-b-commitment-key-accessor-closure-proof-001.md
    on origin/main via PR195

DESIGNATION_PACKET=
  docs/nw008/nw-008-at8w21-production-runtime-governed-designation-packet-001.md
DESIGNATION_PACKET_COMPLETE=YES
STORE_DESIGNATION_COMPLETE=YES

SOURCE_PLAN=
  docs/nw008/nw-008-at8w23-external-prerequisite-remediation-plan-001.md
LANE_C_FROM_PLAN=
  STORE_PARENT_AND_ROOT_OWNED_CONFIG_CLOSURE
PLAN_NOTE=
  AT8W23 designated store key/path and Lane C sequence but explicitly did not
  select or mutate the governed runtime configuration surface. This unit closes
  that surface-selection gap only.
```

## 3. Human designation — configuration-delivery surface

Human governance hereby designates the exact durable NW-008 production runtime
configuration-delivery surface as follows:

```text
CONFIG_SURFACE_DESIGNATED=YES

GOVERNED_RUNTIME_CONFIG_SURFACE=
  /Users/achandler/Library/Application Support/mg-guide/nw008/runtime.env

CONFIG_SURFACE_TYPE=
  DEDICATED_ORCHESTRATOR_ENV_FILE

CONFIG_SURFACE_OWNER=
  VS_CODE_ORCHESTRATOR

CONFIG_SURFACE_SCOPE=
  NW008_RUNTIME_ONLY

CONFIG_SOURCE_CLASS=
  ORCHESTRATOR_GOVERNED_ENVIRONMENT_CONFIGURATION

CONFIG_DELIVERY_MODEL=
  VS Code/orchestrator loads the dedicated runtime.env file and injects its
  validated values into the governed NW-008 child-process environment before
  runtime composition begins.
```

### 3.1 Surface semantics

1. The designated surface is a **dedicated** env file for NW-008 runtime only.
   It is not a shared shell profile, not a repository `.env`, not CI secrets
   injection, and not an ad-hoc process export.
2. Ownership is the VS Code orchestrator under human governance. Child runtime
   processes consume injected values; they do not own or rewrite the surface.
3. Delivery is load-then-inject: the orchestrator reads the designated file,
   validates required keys against designation contracts, and supplies the
   resulting environment to the governed NW-008 child process **before**
   runtime composition begins.
4. Absence of the file, parent directory, or required keys remains a fail-closed
   precondition failure until a separately authorized Lane C execution unit
   provisions them.

### 3.2 Non-surfaces (explicitly not designated)

```text
NOT_DESIGNATED_AS_NW008_RUNTIME_CONFIG_SURFACE=
  repository .env / .env.* files|
  process-local shell exports without the designated file|
  CI/CD workflow env blocks|
  Secret Manager secret payloads used as general config bags|
  macOS user shell profiles (~/.zshrc, ~/.zprofile, ~/.bash_profile)|
  launchd plist environment dictionaries|
  container/orchestrator secrets unrelated to this path|
  any path inside the git repository or git worktrees
```

## 4. Designated configuration binding (from AT8W21; unchanged)

This unit does not re-open store designation. It binds the already-designated
root-owned DB configuration key and exact DB path to the newly designated
configuration surface.

```text
RUNTIME_HOST=MG-NW008-RUNTIME-HOST-01
RUNTIME_HOST_BINDING=Aarons-MacBook-Pro

ROOT_OWNED_DB_CONFIG_KEY=
  MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH

EXACT_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3

STORE_SUBSTRATE=EMBEDDED_SQLITE_VIA_At1ExecutionStore
STORAGE_CLASS=OPERATOR_GOVERNED_DURABLE_LOCAL_DISK
```

### 4.1 Human-packet key typography normalization

The human designation packet for this unit contained the key token
`MG_GUIDIDE_NW008_EXECUTION_STORE_DB_PATH` (extra `I`). That token is treated
as a typographical error. The canonical key remains the AT8W21 / AT8W23
designated value:

```text
HUMAN_PACKET_KEY_TOKEN_OBSERVED=
  MG_GUIDIDE_NW008_EXECUTION_STORE_DB_PATH
CANONICAL_ROOT_OWNED_DB_CONFIG_KEY=
  MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH
KEY_NORMALIZED_TO_CANONICAL=YES
NEW_KEY_CREATED=NO
```

No alternate key is designated. Install and verification units MUST use only
`MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH`.

### 4.2 Required file content contract (designation only; not installed)

When a later authorized Lane C execution unit installs configuration, the
designated surface MUST present at least:

```text
# governed NW-008 runtime configuration — orchestrator-owned
# path: /Users/achandler/Library/Application Support/mg-guide/nw008/runtime.env
MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH=/Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3
```

Rules for later install (not performed by this unit):

```text
FILE_FORMAT=KEY=VALUE dotenv lines
REQUIRED_KEY=MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH
REQUIRED_VALUE_EXACT_MATCH=EXACT_DB_PATH
QUOTING=optional; value after unquote must equal EXACT_DB_PATH exactly
COMMENTS_ALLOWED=YES (# prefix)
EXPORT_PREFIX_ALLOWED=NO
INTERPOLATION_ALLOWED=NO
ADDITIONAL_KEYS_ALLOWED=YES only if separately designated later
SECRET_PAYLOADS_IN_FILE=FORBIDDEN
```

## 5. Lane C residual work (not authorized here)

AT8W23 Lane C sequence remains the residual external closure path after this
surface designation:

```text
STEP_C0=CONFIG_SURFACE_DESIGNATION
  STATUS=COMPLETE_BY_THIS_UNIT
  AUTHORITY=this planning_only designation merge (surface selection only)

STEP_C1=PROVISION_EXACT_PARENT_DIRECTORY
  STATUS=NOT_EXECUTED
  AUTHORITY_REQUIRED=
    fresh human-governed host/config mutation authorization
  TARGET_PARENT=
    /Users/achandler/Library/Application Support/mg-guide/nw008
  CREATE_DB_FILE=NO
  CREATE_RUNTIME_ENV_FILE=NO (C1 is directory only)

STEP_C2=INSTALL_ROOT_OWNED_DB_CONFIG_VALUE
  STATUS=NOT_EXECUTED
  AUTHORITY_REQUIRED=
    fresh human-governed config mutation authorization
  SURFACE=GOVERNED_RUNTIME_CONFIG_SURFACE (this designation)
  KEY=MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH
  VALUE=EXACT_DB_PATH
  ENV_VAR_SET_WITHOUT_AUTHORITY=FORBIDDEN
  AD_HOC_EXPORT_WITHOUT_FILE=FORBIDDEN

STEP_C3=READ_ONLY_EXTERNAL_CONFIG_VERIFICATION
  STATUS=NOT_EXECUTED
  SUCCESS_GATE=
    CURRENT_PARENT_PATH_EXISTS=YES
    AND CURRENT_CONFIG_SURFACE_EXISTS=YES
    AND CURRENT_CONFIG_KEY_PRESENT=YES
    AND CONFIG_VALUE_MATCHES_EXACT_DB_PATH=YES
    AND DB_FILE_STILL_ABSENT_OR_ONLY_CREATED_BY_AUTHORIZED_RUNTIME=YES
```

```text
LANE_C=
  STORE_PARENT_AND_ROOT_OWNED_CONFIG_CLOSURE
LANE_C_SURFACE_DESIGNATION=COMPLETE
LANE_C_EXECUTION_STATUS=NOT_STARTED
LANE_C_STATUS=SURFACE_DESIGNATED_EXECUTION_PENDING
LANE_C_MUTATIONS_IN_THIS_UNIT=0
STORE_WRITES=0
```

## 6. Explicit non-actions of this unit

```text
DID_NOT=
  create parent directory|
  create runtime.env|
  write MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH|
  export environment variables|
  create or open SQLite DB|
  mutate IAM|
  read secret payloads|
  mint tokens|
  call HighLevel/CRM|
  edit runtime code|
  start NW-008 runtime
```

Observed ambient host facts at designation time (read-only existence check only;
no creation):

```text
MG_GUIDE_APPLICATION_SUPPORT_PARENT_EXISTS=NO
NW008_PARENT_DIR_EXISTS=NO
RUNTIME_ENV_FILE_EXISTS=NO
EXACT_DB_FILE_EXISTS=NO
```

These absences are expected residual Lane C external blockers. They are not
remediated by this unit.

## 7. Forbidden effects and no-mutation guardrails

```text
FORBIDDEN=
  CONFIG_MUTATION|
  HOST_DIRECTORY_CREATE|
  SQLITE_CREATE|
  SQLITE_WRITE|
  ENV_VAR_SET_WITHOUT_SEPARATE_AUTHORITY|
  SECRET_PAYLOAD_READ|
  TOKEN_MINT|
  IAM_MUTATION|
  SECRET_MUTATION|
  RUNTIME_CODE_EDIT|
  DEPLOYMENT|
  HIGHLEVEL_CALL|
  CRM_MUTATION|
  NEW_SERVICE_ACCOUNT|
  PRINCIPAL_PUBLICATION
```

This designation creates no mutation authority. Any later step that would create
directories, write `runtime.env`, set configuration values, or create the SQLite
database requires a separate and explicitly authorized execution lane.

## 8. Return block

```text
UNIT=NW008_AT8W24_LANE_C_RUNTIME_CONFIG_SURFACE_DESIGNATION_001
PR_CLASS=planning_only

CONFIG_SURFACE_DESIGNATED=YES
GOVERNED_RUNTIME_CONFIG_SURFACE=
  /Users/achandler/Library/Application Support/mg-guide/nw008/runtime.env
CONFIG_SURFACE_TYPE=DEDICATED_ORCHESTRATOR_ENV_FILE
CONFIG_SURFACE_OWNER=VS_CODE_ORCHESTRATOR
CONFIG_SURFACE_SCOPE=NW008_RUNTIME_ONLY
CONFIG_SOURCE_CLASS=ORCHESTRATOR_GOVERNED_ENVIRONMENT_CONFIGURATION

ROOT_OWNED_DB_CONFIG_KEY=MG_GUIDE_NW008_EXECUTION_STORE_DB_PATH
EXACT_DB_PATH=
  /Users/achandler/Library/Application Support/mg-guide/nw008/at1-execution-store.sqlite3
KEY_NORMALIZED_TO_CANONICAL=YES

LANE_C_SURFACE_DESIGNATION=COMPLETE
LANE_C_EXECUTION_STATUS=NOT_STARTED
LANE_C_STATUS=SURFACE_DESIGNATED_EXECUTION_PENDING
C3_EXTERNAL_CONFIG_PREREQUISITES_READY=NO

MUTATION_AUTHORITY_CREATED=NO
CONFIG_MUTATIONS=0
STORE_WRITES=0
IAM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
EXTERNAL_EFFECTS=0

NEXT=
  LANE_C_STORE_PARENT_AND_ROOT_OWNED_CONFIG_EXECUTION
  (requires fresh human-governed host/config mutation authorization;
   not authorized by this designation)
```

## 9. Validation gates

```text
PR_CLASS=planning_only
CONFIG_SURFACE_DESIGNATED=YES
GOVERNED_RUNTIME_CONFIG_SURFACE_EXACT=YES
ROOT_OWNED_DB_CONFIG_KEY_CANONICAL=YES
EXACT_DB_PATH_BOUND_FROM_AT8W21=YES
NO_DIRECTORY_CREATED=YES
NO_RUNTIME_ENV_WRITTEN=YES
NO_DB_CREATED=YES
MUTATION_AUTHORITY_CREATED=NO
EXTERNAL_EFFECTS=0
LANE_C_EXECUTION_NOT_CLAIMED_COMPLETE=YES
```
