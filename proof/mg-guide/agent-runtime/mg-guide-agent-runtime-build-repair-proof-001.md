# MG Guide Agent Runtime Build Repair Proof 001

## 1. Identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_BUILD_REPAIR_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-build-repair-proof-001.md
PR_CLASS=implementation
MODE=BOUNDED_SOURCE_PACKAGE_FORMAT_REPAIR
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

PR_388_MERGE_SHA=
  ce203a3aa5e7f6e521b8061aef082871cb9d3493
PR_388_ROLE=
  ATTEMPT_002_BUILD_FAILURE_DIAGNOSIS_BASELINE
PR_388_MERGE_SHA_ANCESTOR_OF_ORIGIN_MAIN=YES

ROOT_CAUSE_CLASS=PACKAGE_LAYOUT
FAILED_REMOTE_OBJECT=source_archive.tar.gz
FAILED_SUBMITTED_FORMAT=ZIP
OLD_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
NEW_PACKAGE_FORMAT=TAR_GZIP

ATTEMPT_002_RETRY_AUTHORIZED=NO
AUTHORIZATION_002_REUSABLE=NO
ACTIVATION_002_REUSABLE=NO
```

This unit repairs only Agent Runtime deployment package generation and
verification so the candidate is a deterministic gzip-compressed TAR. It does
not authorize deployment, retry Attempt 002, create Authorization 003, mutate
IAM, secrets, or service accounts, change `requirements.txt`, or run
`terraform apply`.

```text
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
IAM_MUTATION=NO
SECRET_MUTATION=NO
SERVICE_ACCOUNT_MUTATION=NO
REQUIREMENTS_TXT_CHANGED=NO
AGENT_GRAPH_CHANGED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
```

## 2. Bounded surfaces changed

```text
scripts/build_agent_runtime_source.py
scripts/verify_agent_runtime_source_package.py
tests/agents/test_agent_runtime_source_package.py
```

Unchanged:

```text
deployment/agent-runtime/requirements.txt
agent graph / delegates / model configuration
runtime service account
IAM / secrets / GHL / CRM
project=ai-rolodex-to-crm
region=us-east1
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
```

## 3. New source package contract

Two independent off-repository rebuilds from
`SOURCE_BUILD_COMMIT=c37e7e518ac4702a7035c64b6d03c67530e380b9` produced
byte-identical archives. Archive bytes were not committed.

```text
SOURCE_BUILD_COMMIT=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
NEW_SOURCE_PACKAGE_FORMAT=TAR_GZIP
GZIP_MAGIC=1f8b
IS_GZIP=YES
IS_TAR_GZIP=YES
IS_ZIP=NO

NEW_SOURCE_PACKAGE_SHA256=
  1441bd961910be80c4f2d27483ca78ee0302b933c51b7c546309b79aa079b752
NEW_SOURCE_PACKAGE_SIZE_BYTES=67778
NEW_SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_REBUILD_BYTE_IDENTICAL=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

The 54 archive paths match the prior ZIP candidate, including
`requirements.txt`, `app/agent.py`, and `SOURCE_MANIFEST.sha256`. File contents
are the same Git blobs; only the container format changed from ZIP_STORED to
deterministic USTAR+gzip (`mtime=1980-01-01T00:00:00Z`, gzip `mtime=0`).

## 4. Cloud-failure regression (local)

Commands against the exact candidate:

```text
gzip -t <candidate.tar.gz>
tar -tzf <candidate.tar.gz>
tar -xzf <candidate.tar.gz> -C <clean-temp-dir>
```

```text
GZIP_TEST=PASS
TAR_LIST=PASS
TAR_EXTRACT=PASS
HAS_REQUIREMENTS_TXT=YES
HAS_APP_AGENT=YES
```

Focused automated coverage now proves the candidate is gzip/TAR and rejects
ZIP magic. Existing absolute-path, traversal, and symlink rejection tests were
re-homed onto TAR members.

## 5. Package validation

```text
ARCHIVE_PATH_SAFETY=PASS
SYMLINK_POLICY=PASS
PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS
ROOT_AGENT_MODULE=app.agent
ROOT_AGENT_FACTORY=
  agents.follow_up_planning.runtime.build_unit3_root_agent
GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

## 6. Fresh non-mutating Terraform plan

The repaired tar.gz bytes were supplied only through the ephemeral Terraform
input surface. Commands:

```text
terraform fmt -check
terraform init -backend=false -input=false
terraform validate
terraform plan -refresh=false -input=false
```

```text
TF_FMT=PASS
TF_INIT_BACKEND_FALSE=PASS
TF_VALIDATE=PASS
TF_PLAN=PASS

PLAN_SUMMARY=
  1_TO_ADD_0_TO_CHANGE_0_TO_DESTROY
EXPECTED_RESOURCE_ONLY=YES
PLANNED_RESOURCE=
  google_vertex_ai_reasoning_engine.mg_guide
PLANNED_PROJECT=ai-rolodex-to-crm
PLANNED_REGION=us-east1
PLANNED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
RUNTIME_SERVICE_ACCOUNT_MATCH=YES

PLAN_CREATES_NEW_RUNTIME_SA=NO
PLAN_CREATES_SERVICE_ACCOUNT_KEY=NO
PLAN_ADDS_IAM=NO
PLAN_MUTATES_SECRET=NO
PLAN_DESTROYS_RESOURCE=NO

PLAN_FILE_SHA256=
  6d6c9207a26074d82401ed07a1766a88288c7548954abaef3f6f783b004ec73c
PLAN_FILE_COMMITTED_TO_REPOSITORY=NO
DEPLOYMENT_BYTES_COMMITTED=NO
TERRAFORM_APPLY_EXECUTED=NO
DEPLOYMENT_EXECUTED=NO
```

## 7. STOP / NEXT

```text
STOP=INDEPENDENT_REVIEW_REQUIRED
AUTHORIZATION_003_CREATED_IN_THIS_UNIT=NO
ATTEMPT_002_RETRY_AUTHORIZED=NO

NEXT=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_003
  after independent review and merge of this repair
```

Any future deployment still requires a fresh independently reviewed
authorization and human activation. This proof does not activate execution
authority.
