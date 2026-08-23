# NW-008 AT8W14 GHLV2 Adoption Adapter Staging One-Shot Delete Authorization 001

## 1. Authorization identity and status

```text
AUTHORIZATION_ID=
  NW008_AT8W14_GHLV2_ADOPTION_ADAPTER_STAGING_ONE_SHOT_DELETE_AUTHORIZATION_001
PR_CLASS=authorization_only
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

AUTHORIZATION_BRANCH=
  nw008-at8w14-ghlv2-adoption-adapter-staging-one-shot-delete-authorization-001
AUTHORIZATION_BASE_REF=origin/main
AUTHORIZATION_BASE_SHA=
  0edf94307aa8f2d7815ec23ac419d8b35a708e09
AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w14-ghlv2-adoption-adapter-staging-one-shot-delete-authorization-001.md

GRANT_STATUS=PROPOSED_UNTIL_HUMAN_REVIEW_AND_MERGE
DELETE_EXECUTION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

This artifact proposes one narrowly bounded future Cloud Run service deletion.
Opening or reviewing the PR does not activate the grant. Only human review and
merge of the exact authorization head can activate it, and no deletion may
occur before that merge.

```text
STOP_BEFORE_DELETE=YES
HUMAN_REVIEW_REQUIRED=YES
HUMAN_MERGE_REQUIRED=YES
AGENT_SELF_AUTHORIZATION=FORBIDDEN
```

## 2. Readiness source binding

The proposal exists only because the read-only AT8W14 assessment found no
active runtime or control-plane references:

```text
READINESS_PR=181
READINESS_PR_URL=
  https://github.com/themg-max/mg-guide-agentic-sales-workspace/pull/181
READINESS_REVIEWED_HEAD=
  d302ef8b85a55e27f8ce995f9920065591b2df2b
READINESS_ARTIFACT=
  docs/nw008/nw-008-at8w14-ghlv2-adoption-adapter-staging-decommission-readiness-001.md

AT8W14_DELETE_READY=YES
ACTIVE_RUNTIME_REFERENCE_COUNT=0
ACTIVE_CONTROL_PLANE_REFERENCE_COUNT=0

READINESS_PR_STATE_AT_AUTHORIZATION_DRAFT=OPEN
READINESS_PR_MERGED_AT_AUTHORIZATION_DRAFT=NO
AUTHORIZATION_ACTIVATION_REQUIRES_READINESS_PR_MERGED=YES
AUTHORIZATION_ACTIVATION_REQUIRES_REVIEWED_HEAD_ANCESTRY=YES
```

If PR #181 is not merged with reviewed head
`d302ef8b85a55e27f8ce995f9920065591b2df2b` in its ancestry, this authorization
remains inactive even if its own PR is merged. If the readiness artifact is
amended, human governance must update this binding or create a superseding
authorization.

## 3. Exact one-shot grant

```text
DELETE_GRANT=
  TARGET=ghlv2-adoption-adapter-staging|
  PROJECT=ai-rolodex-to-crm|
  REGION=us-east4|
  DELETE_ATTEMPTS_MAX=1|
  DELETE_SERVICE_MAX=1|
  RETRY=NO|
  FALLBACK=NO

AUTHORIZED_RESOURCE_TYPE=Cloud Run service
AUTHORIZED_OPERATION=delete
AUTHORIZED_SERVICE_FULL_NAME=
  projects/ai-rolodex-to-crm/locations/us-east4/services/ghlv2-adoption-adapter-staging

DELETE_ATTEMPTS_MAX=1
DELETE_SERVICE_MAX=1
RETRY=NO
FALLBACK=NO
ALTERNATE_TARGET=NO
WILDCARD_TARGET=NO
```

The grant covers the exact service only. It does not authorize an additional
attempt after a failed or ambiguous delete request. It does not authorize
choosing another project, region, or service.

## 4. Pre-consumption fail-closed gates

Before any later execution consumes the grant, the operator must perform
read-only checks and require every gate below:

```text
PRECONSUMPTION_GATES=
  AUTHORIZATION_PR_HUMAN_MERGED=YES|
  AUTHORIZATION_EXACT_REVIEWED_HEAD_ANCESTRY=YES|
  READINESS_PR181_HUMAN_MERGED=YES|
  READINESS_HEAD_D302EF8_ANCESTRY=YES|
  EXACT_SERVICE_NAME_MATCH=YES|
  EXACT_PROJECT_MATCH=YES|
  EXACT_REGION_MATCH=YES|
  SERVICE_UID_MATCH_AT8W14=YES|
  SERVICE_GENERATION_MATCH_AT8W14=YES|
  ACTIVE_RUNTIME_REFERENCE_COUNT_RECHECK=0|
  ACTIVE_CONTROL_PLANE_REFERENCE_COUNT_RECHECK=0|
  DELETE_ATTEMPTS_ALREADY_CONSUMED=0

EXPECTED_SERVICE_UID=29be1fed-7443-4bb3-91e7-b1c3bfa86794
EXPECTED_SERVICE_GENERATION=1
```

Any mismatch, new reference, inspection error, incomplete result, or ambiguous
state fails closed:

```text
ON_PRECONSUMPTION_GATE_FAILURE=STOP_WITHOUT_DELETE
ON_IDENTITY_MISMATCH=STOP_WITHOUT_DELETE
ON_NEW_ACTIVE_REFERENCE=STOP_WITHOUT_DELETE
ON_INSPECTION_ERROR=STOP_WITHOUT_DELETE
ON_UNKNOWN=STOP_WITHOUT_DELETE
```

No failed gate consumes or broadens authority into a different operation.

## 5. Authorized effect and consumption semantics

After every gate passes, one delete request may target the exact service. The
request consumes the grant regardless of success, failure, timeout, or
ambiguous response.

```text
AUTHORIZED_DELETE_REQUESTS_MAX=1
GRANT_CONSUMED_ON_REQUEST_DISPATCH=YES
GRANT_CONSUMED_ON_SUCCESS=YES
GRANT_CONSUMED_ON_FAILURE=YES
GRANT_CONSUMED_ON_TIMEOUT=YES
GRANT_CONSUMED_ON_AMBIGUOUS_RESPONSE=YES

SECOND_DELETE_REQUEST_AUTHORIZED=NO
AUTOMATIC_RETRY_AUTHORIZED=NO
MANUAL_RETRY_UNDER_THIS_GRANT_AUTHORIZED=NO
FALLBACK_DELETE_AUTHORIZED=NO
```

A post-request read-only existence check may report the result. It may not
dispatch another deletion.

## 6. Explicitly forbidden by the grant

```text
FORBIDDEN_BY_DELETE_GRANT=
  other Cloud Run deletion|
  secret deletion|
  secret read|
  IAM mutation|
  AI Rolodex backend change|
  MG Guide runtime change|
  HighLevel call|
  CRM mutation

OTHER_CLOUD_RUN_DELETION=FORBIDDEN
SECRET_DELETION=FORBIDDEN
SECRET_PAYLOAD_READ=FORBIDDEN
IAM_MUTATION=FORBIDDEN
AI_ROLODEX_BACKEND_CHANGE=FORBIDDEN
MG_GUIDE_RUNTIME_CHANGE=FORBIDDEN
HIGHLEVEL_CALL=FORBIDDEN
CRM_MUTATION=FORBIDDEN

REVISION_DELETE_AS_SEPARATE_OPERATION=FORBIDDEN
LOG_DELETE=FORBIDDEN
HISTORICAL_EVIDENCE_DELETE=FORBIDDEN
TRAFFIC_MUTATION_BEFORE_DELETE=FORBIDDEN
DEPLOYMENT=FORBIDDEN
AT8W9_REUSE=FORBIDDEN
AT8W10_RETRY=FORBIDDEN
```

Normal platform cleanup intrinsic to deleting the exact Cloud Run service is
not authority for a separate revision-delete request or any deletion outside
the exact service operation.

## 7. Preserved resources and NW-008 boundaries

```text
PRESERVE=
  mg-guide-ghl-note-runtime service account|
  all secrets|
  all IAM policies and bindings|
  all logs|
  all historical evidence|
  AI Rolodex production backend|
  MG Guide runtime|
  existing NW008 mutation budgets|
  one POST maximum|
  same-run GET maximum|
  no retry|
  no search/list/pagination

SERVICE_ACCOUNT_DELETION_AUTHORIZED=NO
SERVICE_ACCOUNT_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
RUNTIME_SOURCE_EDIT_AUTHORIZED=NO
```

## 8. Current packet effect ledger

This authorization PR only records a proposed grant:

```text
CLOUD_RUN_DELETE_ATTEMPTS=0
CLOUD_RUN_SERVICES_DELETED=0
CLOUD_RUN_REVISIONS_DELETED_SEPARATELY=0
SECRET_READS=0
SECRET_MUTATIONS=0
IAM_MUTATIONS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
PRODUCTION_BACKEND_EDITS=0
MG_GUIDE_RUNTIME_EDITS=0
DEPLOYMENTS=0

CHANGED_FILE_COUNT=1
EXACT_INTENDED_ARTIFACT_PATH_ONLY=YES
```

## 9. Mandatory stop

```text
STOP=
  Human review/merge of delete authorization before any deletion.

STOP_NOW=YES
DELETE_NOW=NO
NEXT_ACTOR=HUMAN_GOVERNANCE
```

No deletion is performed in this authorization packet.
