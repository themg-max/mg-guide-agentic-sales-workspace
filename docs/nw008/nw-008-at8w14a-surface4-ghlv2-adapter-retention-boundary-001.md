# NW-008 AT8W14A Surface 4 GHLV2 Adapter Retention Boundary 001

## 1. Unit identity and planning-only boundary

```text
UNIT=NW008_AT8W14A_SURFACE4_GHLV2_ADAPTER_RETENTION_BOUNDARY_001
PR_CLASS=planning_only
MODE=READ_ONLY_CROSS_SYSTEM_RESOURCE_ROLE_RECONCILIATION
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BOUNDARY_BRANCH=
  nw008-at8w14a-surface4-ghlv2-adapter-retention-boundary-001
BOUNDARY_BASE_REF=origin/main
BOUNDARY_BASE_SHA=
  ad4e3d989a4ddcfd3041c7057d7d162e9e475065
BOUNDARY_ARTIFACT=
  docs/nw008/nw-008-at8w14a-surface4-ghlv2-adapter-retention-boundary-001.md

PLANNING_ONLY=YES
READ_ONLY=YES
CLOUD_RUN_MODIFIED=NO
SERVICE_DELETED=NO
EXTERNAL_EFFECTS=0
```

This unit records why `ghlv2-adoption-adapter-staging` is retained even though
merged AT8W13 found it unsuitable for NW-008 runtime reuse. The service belongs
to an independent AI Rolodex Surface 4 Consumer A boundary. That role is not an
NW-008 role.

```text
MERGING_THIS_BOUNDARY_CONFERS_IMPLEMENTATION_AUTHORITY=NO
MERGING_THIS_BOUNDARY_CONFERS_DELETE_AUTHORITY=NO
MERGING_THIS_BOUNDARY_CONFERS_LIVE_EXECUTION_AUTHORITY=NO
```

## 2. Pre-flight and merged-state verification

```text
PRE_FLIGHT=
  pwd|
  git branch --show-current|
  git status --short --untracked-files=all|
  git fetch origin

WORKING_DIRECTORY=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH_AT_PRE_FLIGHT=
  nw008-at8w15-ai-rolodex-backend-ghl-capability-reference-assessment-001
BRANCH_IS_MAIN=NO
UNEXPECTED_DIRTY_WORKTREE=NO
DIRTY_PATH_COUNT=0
ORIGIN_FETCHED=YES
ABORT_TRIGGERED=NO
```

The controlling merged predecessors were verified on `origin/main`:

```text
PR180_STATE=MERGED
PR180_REVIEWED_HEAD=
  a1fe146773a8ae468047464374e6c003b029f4bb
PR180_ACTUAL_MERGE_COMMIT=
  6e9a12eb7d9071db8c88e51b9f01ae155f877b11
PR180_REVIEWED_HEAD_IS_MERGE_SECOND_PARENT=YES
PR180_MERGE_COMMIT_ON_ORIGIN_MAIN=YES

PR183_STATE=MERGED
PR183_REVIEWED_HEAD=
  9c5571df267482e925b1a9fbe6b6e28bff57ab7d
PR183_ACTUAL_MERGE_COMMIT=
  ad4e3d989a4ddcfd3041c7057d7d162e9e475065
PR183_REVIEWED_HEAD_IS_MERGE_SECOND_PARENT=YES
PR183_MERGE_COMMIT_ON_ORIGIN_MAIN=YES
PR183_MERGE_COMMIT_EQUALS_BOUNDARY_BASE_SHA=YES
```

The two decommission-track PRs did not merge:

```text
PR181_STATE=CLOSED_UNMERGED
PR181_CLOSED_UNMERGED=YES
PR181_CONTENT_ON_MAIN=NO

PR182_STATE=CLOSED_UNMERGED
PR182_CLOSED_UNMERGED=YES
PR182_CONTENT_ON_MAIN=NO

MERGED_DELETE_READINESS_ARTIFACT_PRESENT=NO
MERGED_DELETE_AUTHORIZATION_PRESENT=NO
DELETE_AUTHORITY=NONE
```

PR181's unmerged assessment and PR182's unmerged proposed grant cannot confer
authority. Closing them leaves no service-delete authority.

## 3. Surface 4 evidence class

Read-only source search in `themg-max/A.I-Rolodex---Context` at default-branch
head `f3ad12377405b3c8228a3b46dbc299c2a13573db` found the retained mapping in:

```text
SOURCE_SYSTEM=A.I_ROLODEX_SURFACE4
SOURCE_EVIDENCE_CLASS=MERGED_EXTERNAL_CONTROL_PLANE_EVIDENCE_INDEX
SOURCE_EVIDENCE_PATH=
  .ai/memory/features/plan-orchestration-l3-surface4-consumer-adoption-endpoint-provisioning-v1/consumer-adoption-staging-evidence-index.md

SURFACE4_CONSUMER_ID=consumer-a
SURFACE4_CONSUMER_ROLE=GHLV2_ADOPTION_QUEUE
SURFACE4_STAGING_SERVICE=ghlv2-adoption-adapter-staging
SOURCE_EVIDENCE_DISPOSITION=ACCEPTED
SOURCE_EVIDENCE_VALIDATION_CLASS=CONTROL_PLANE_METADATA_ONLY
```

The source evidence binds Consumer A to the exact Cloud Run staging service.
Its validation method was control-plane metadata inspection. It expressly did
not establish endpoint invocation. No secret value or private business
identifier is reproduced here.

## 4. Retained service boundary

```text
SERVICE=ghlv2-adoption-adapter-staging
SERVICE_PROJECT=ai-rolodex-to-crm
SERVICE_REGION=us-east4
SERVICE_DISPOSITION=RETAIN

SOURCE_SYSTEM=A.I_ROLODEX_SURFACE4
SURFACE4_CONSUMER_ID=consumer-a
SURFACE4_CONSUMER_ROLE=GHLV2_ADOPTION_QUEUE
RESOURCE_ROLE=STAGING_CONTROL_PLANE_REFERENCE
```

`RETAIN` means:

1. do not delete the service under NW-008 authority;
2. do not repurpose it as the NW-008 note runtime;
3. do not infer that its name proves a live GHL adapter;
4. leave any Surface 4 modification to its own owner and governance lane.

```text
RETENTION_REASON=
  independent Surface 4 Consumer A staging control-plane reference
RETENTION_IS_NW008_RUNTIME_ADOPTION=NO
RETENTION_IS_LIVE_WIRING_PROOF=NO
RETENTION_IS_GHL_HANDOFF_PROOF=NO
```

## 5. Proven and unproven facts

The cross-system evidence proves a resource-role association, not live
application behavior:

```text
SURFACE4_CONTROL_PLANE_RESOURCE_ASSOCIATION_PROVEN=YES
SURFACE4_CONSUMER_A_ROLE_ASSOCIATION_PROVEN=YES

LIVE_SURFACE4_RUNTIME_WIRING_PROVEN=NO
LIVE_GHL_HANDOFF_PROVEN=NO
SERVICE_ROUTE_CONTRACT_PROVEN=NO
SERVICE_TO_HIGHLEVEL_REQUEST_PROVEN=NO
DEPLOYED_IMAGE_IS_GHL_ADAPTER_PROVEN=NO
```

Merged AT8W13 separately established that the deployed revision was the generic
Cloud Run hello image, not a GHLV2 adapter implementation. Retaining the
resource therefore preserves the external control-plane boundary without
overstating runtime capability.

```text
AT8W13_SUITABILITY_FINDING_PRESERVED=YES
AT8W13_DEPLOYED_IMAGE_FINDING_REOPENED=NO
SERVICE_NAME_USED_AS_RUNTIME_PROOF=NO
```

## 6. NW-008 separation

```text
NW008_RUNTIME_ROLE=NONE
NW008_DEPENDENCY_ON_SERVICE=NO
NW008_REQUESTS_ROUTE_THROUGH_SERVICE=NO
NW008_CREDENTIALS_BOUND_TO_SERVICE=NO
NW008_EXECUTION_STORE_BOUND_TO_SERVICE=NO
NW008_SERVICE_ACCOUNT_BOUND_TO_SERVICE=NO
```

The retained service does not replace or participate in:

- `BoundedLiveNoteTransport`;
- `ConcreteLiveNoteHttpClient`;
- `RootOwnedLiveNoteCredentialInjection`;
- the capability-bound contact target;
- the one-POST/same-run-GET note verification path.

```text
NW008_DIRECT_REST_ARCHITECTURE_REMAINS_CONTROLLING=YES
NW008_RUNTIME_REUSE_OF_SURFACE4_SERVICE=NO
NW008_DEPLOYMENT_TO_SURFACE4_SERVICE=NO
```

## 7. Authority disposition

```text
SERVICE_DISPOSITION=RETAIN
DELETE_AUTHORITY=NONE
MODIFICATION_AUTHORITY_CREATED=NO
DEPLOYMENT_AUTHORITY_CREATED=NO
RUNTIME_WIRING_AUTHORITY_CREATED=NO

PR181_CLOSED_UNMERGED=YES
PR182_CLOSED_UNMERGED=YES
```

Any future deletion or modification proposal must originate in the Surface 4
owner lane, re-evaluate the then-current resource role, and obtain fresh human
governance. No prior NW-008 delete proposal may be reused.

## 8. Preservation and forbidden effects

```text
PRESERVE=
  ghlv2-adoption-adapter-staging service|
  Surface 4 Consumer A ownership boundary|
  mg-guide-ghl-note-runtime service account|
  BoundedLiveNoteTransport|
  ConcreteLiveNoteHttpClient|
  RootOwnedLiveNoteCredentialInjection|
  one POST maximum|
  same-run GET maximum|
  no retry|
  no search|
  no list|
  no pagination

FORBIDDEN=
  HIGHLEVEL_CALL|
  CRM_MUTATION|
  SECRET_PAYLOAD_READ|
  IAM_MUTATION|
  SECRET_MUTATION|
  BACKEND_SOURCE_EDIT|
  NW008_RUNTIME_SOURCE_EDIT|
  DEPLOYMENT|
  CLOUD_RUN_CONFIGURATION_CHANGE|
  SURFACE4_SERVICE_MODIFICATION|
  CLOUD_RUN_DELETION|
  NEW_SERVICE_ACCOUNT

HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
BACKEND_SOURCE_EDITS=0
NW008_RUNTIME_SOURCE_EDITS=0
DEPLOYMENTS=0
CLOUD_RUN_CONFIGURATION_CHANGES=0
SURFACE4_SERVICE_MODIFICATIONS=0
CLOUD_RUN_DELETIONS=0
NEW_SERVICE_ACCOUNTS=0
```

## 9. Final disposition and stop

```text
SERVICE=ghlv2-adoption-adapter-staging
SERVICE_DISPOSITION=RETAIN
RESOURCE_ROLE=STAGING_CONTROL_PLANE_REFERENCE
NW008_RUNTIME_ROLE=NONE
NW008_DEPENDENCY_ON_SERVICE=NO
DELETE_AUTHORITY=NONE

CHANGED_FILE_COUNT=1
EXACT_INTENDED_PLANNING_ARTIFACT_ONLY=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
```

AT8W14A stops after recording the retained cross-system boundary. No Cloud Run
resource is modified.
