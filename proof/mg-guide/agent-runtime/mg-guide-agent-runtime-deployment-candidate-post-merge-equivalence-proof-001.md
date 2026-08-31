# MG Guide Agent Runtime Deployment Candidate Post-Merge Equivalence Proof 001

## Scope

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_CANDIDATE_POST_MERGE_EQUIVALENCE_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-candidate-post-merge-equivalence-proof-001.md
PR_CLASS=BOUNDED_PROOF

PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
PR_380_MERGE_SHA=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
PR_380_REVIEW_ID=5062829496
POST_MERGE_SOURCE_COMMIT=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
CANDIDATE_SOURCE_BRANCH_COMMIT=
  eebd09055de2e72c7dce6ebf0f202a415a362a81

EXPECTED_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
```

PR #380 was squash-merged as `c37e7e518ac4702a7035c64b6d03c67530e380b9`.
This proof rebuilds from that merged `origin/main` commit, not from its
pre-merge branch commit.

## Deterministic post-merge rebuild

Two independent invocations built the candidate archive from the exact merge
commit using `scripts/build_agent_runtime_source.py`. The archives were created
outside the repository and were not committed.

```text
POST_MERGE_SOURCE_COMMIT=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
POST_MERGE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
POST_MERGE_PACKAGE_SIZE_BYTES=343228
POST_MERGE_PACKAGE_FILE_COUNT=54

ACTUAL_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
POST_MERGE_PACKAGE_MATCH=YES
POST_MERGE_PACKAGE_MATCHES_PREMERGE_CANDIDATE=YES
POST_MERGE_REBUILD_BYTE_IDENTICAL=YES
```

The fixed digest demonstrates that the squash merge preserved the exact
allowlisted Git blobs, archive paths, timestamps, modes, ordering, and source
manifest that formed the approved source candidate.

## Package validation

The rebuilt archive was verified against its expected SHA-256, extracted only
after pre-extraction safety checks, and exercised in an isolated temporary
directory. The package loaded `app.agent`, resolved the real Unit 3 shared root
factory, and executed one synthetic follow-up scenario through one external
ADK runner.

```text
PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS

ROOT_AGENT_MODULE=app.agent
ROOT_AGENT_FACTORY=
  agents.follow_up_planning.runtime.build_unit3_root_agent
REUSE_EXISTING_AGENT_GRAPH=YES
REUSE_EXISTING_DELEGATES=YES
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO

GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

## Extraction-safety hardening

The package verifier was hardened before calling `ZipFile.extractall`. It now
rejects every archive member with:

- an absolute POSIX or Windows path;
- a `..` traversal component; or
- a Unix symlink mode.

Focused negative tests passed for absolute POSIX paths, absolute Windows paths,
POSIX and Windows traversal forms, and symlink entries. A regular relative
entry test also passed.

```text
ZIP_EXTRACTION_ABSOLUTE_PATH_REJECTION=PASS
ZIP_EXTRACTION_PATH_TRAVERSAL_REJECTION=PASS
ZIP_EXTRACTION_SYMLINK_REJECTION=PASS
ZIP_EXTRACTION_SAFETY_TESTS=7_PASSED
ARCHIVE_BUILDER_CHANGED=NO
APPLICATION_PACKAGE_CONTENTS_CHANGED=NO
POST_MERGE_DIGEST_UNCHANGED_BY_HARDENING=YES
```

## Effect boundary and next gate

```text
DEPLOYMENT_AUTHORIZED=NO
DEPLOYMENT_EXECUTED=NO
TERRAFORM_APPLY_EXECUTED=NO
AGENTS_CLI_DEPLOY_EXECUTED=NO
AGENT_RUNTIME_DEPLOYMENTS=0

SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

Canonical repository validation is recorded with this proof PR. This proof
does not create deployment authority.

```text
NEXT=MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION_001
```

Any future authorization must bind without substitution:

```text
PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
PR_380_MERGE_SHA=
  c37e7e518ac4702a7035c64b6d03c67530e380b9
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
AUTHORITATIVE_TERRAFORM_ROOT=infra/agent-runtime
PROJECT=ai-rolodex-to-crm
REGION=us-east1
APPROVED_RUNTIME_SERVICE_ACCOUNT=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
MAX_DEPLOYMENTS=1
MAX_TERRAFORM_APPLY=1
```
