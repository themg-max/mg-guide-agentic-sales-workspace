# MG Guide Agent Runtime Vertex Binding State Reclassification 001

## 1. Artifact identity and boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_VERTEX_BINDING_STATE_RECLASSIFICATION_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-vertex-binding-state-reclassification-001.md
CLASSIFICATION=IAM_BINDING_STATE_READ_ONLY_RECLASSIFICATION
PR_CLASS=proof_only
MODE=READ_ONLY_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

OBSERVATION_TIMESTAMP_UTC=2026-08-30T00:42:35Z
OBSERVATION_TIMESTAMP_LOCAL=2026-08-29T20:42:35-0400
```

This unit preserves the canonical create history and reclassifies only the
fresh service-account metadata and exact candidate project binding state. It
does not edit or replace the canonical execution proof, and it does not write
IAM policy.

## 2. Canonical create proof binding

```text
CANONICAL_CREATE_PROOF_PR=302
CANONICAL_CREATE_PROOF_MERGE_SHA=
  6691a8d3e51b6066adebbe30a29018e44adeea23
CANONICAL_CREATE_PROOF_PRESENT_ON_ORIGIN_MAIN=YES
CANONICAL_CREATE_PROOF_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_ONE_CREATE_EXECUTION_PROOF_001
CANONICAL_CREATE_PROOF_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-principal-one-create-execution-proof-001.md
CANONICAL_CREATE_PROOF_BLOB_SHA=
  c82164d2f100b9463f23b23ee6497ab548d126af
CANONICAL_CREATE_PROOF_EDITED_BY_THIS_UNIT=NO

CANONICAL_CREATE_AUTHORITY_CONSUMED=YES
CANONICAL_SERVICE_ACCOUNT_CREATE_ATTEMPTS=1
CANONICAL_SERVICE_ACCOUNT_CREATE_RESULT=PASS
CANONICAL_CREATE_HISTORY_RECLASSIFIED=NO
```

## 3. PR #304 disposition and non-competition

```text
PR304_REVIEW_DISPOSITION=CONTRADICTORY_EVIDENCE
PR304_MERGE_AUTHORIZED=NO
PR304_STATE_AT_OBSERVATION=OPEN

PR304_CANONICAL_ARTIFACT_ID_REUSED_BY_THIS_UNIT=NO
PR304_CANONICAL_ARTIFACT_PATH_REUSED_BY_THIS_UNIT=NO
PR304_TERMINAL_HISTORY_ADOPTED_BY_THIS_UNIT=NO
PR304_USEFUL_LATER_OBSERVATION_REFRAMED=YES
THIS_ARTIFACT_COMPETES_WITH_PR302=NO
```

PR #304's later existence observation is useful, but its alternate create
history is not. This distinct artifact binds the merged PR #302 result and
advances only the requested binding-state reclassification.

## 4. Exact target and fresh metadata observation

```text
PROJECT=ai-rolodex-to-crm
MEMBER=
  serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
CANDIDATE_ROLE=roles/aiplatform.user

SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SERVICE_ACCOUNT_EXACT_MATCH_COUNT=1
SERVICE_ACCOUNT_EXISTS=YES
SERVICE_ACCOUNT_EMAIL_MATCH=YES
SERVICE_ACCOUNT_PROJECT_MATCH=YES
SERVICE_ACCOUNT_DISPLAY_NAME_MATCH=YES
SERVICE_ACCOUNT_DISABLED=NO
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=YES
```

The exact filtered service-account list returned one enabled account with the
canonical email, project, display name, and description.

## 5. Fresh candidate-binding observation

The project IAM policy was read and reduced locally to the exact candidate role
and exact member. No policy roster, etag, or unrelated member identity is
recorded in this artifact.

```text
PROJECT_IAM_POLICY_READ=YES
PROJECT_IAM_POLICY_WRITE=NO

EXACT_CANDIDATE_ROLE_BINDING_PRESENT=YES
EXACT_MEMBER_PRESENT_IN_BINDING=NO
EXACT_MEMBER_ROLE_BINDING_COUNT=0
CONFLICTING_OR_AMBIGUOUS_STATE=NO
```

The candidate role already has a project binding, but the exact MG Guide Agent
Runtime member is absent. The existence and IAM-policy observations agree.

## 6. Classification return and explicit next IAM operation

```text
SERVICE_ACCOUNT_EXISTS=YES
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=YES
EXACT_CANDIDATE_ROLE_BINDING_PRESENT=YES
EXACT_MEMBER_PRESENT_IN_BINDING=NO
EXACT_MEMBER_ROLE_BINDING_COUNT=0
CONFLICTING_OR_AMBIGUOUS_STATE=NO

FLEET_BINDING_RECLASSIFICATION_STATUS=
  READY_FOR_ONE_EXACT_MEMBER_ADDITION_AUTHORIZATION

BINDING_ACTION=
  ADD_EXACT_MEMBER_TO_EXISTING_ROLE_BINDING

IAM_MUTATIONS=0
```

This status permits only a later, separately governed authorization decision
for one exact-member addition to the already-present candidate role binding.
It does not authorize or apply that addition.

## 7. Recommended future authorization ceilings (not executed here)

```text
FUTURE_AUTHORIZATION_RECOMMENDED=
  MG_GUIDE_AGENT_RUNTIME_VERTEX_EXACT_MEMBER_ADDITION_AUTHORIZATION_001

MAX_PROJECT_IAM_POLICY_WRITES=1
MAX_EXACT_MEMBER_ADDITIONS=1
MAX_ROLE_BINDINGS_CREATED=0
MAX_MEMBER_REMOVALS=0
MAX_CONDITION_CHANGES=0
MAX_SERVICE_ACCOUNT_KEYS=0

IMMEDIATE_PRE_WRITE_REVALIDATION_REQUIRED=YES
EXACT_POST_WRITE_POLICY_DELTA_VERIFICATION_REQUIRED=YES
```

Any later execution unit must revalidate the exact project, member, and role
immediately before the single allowed write, then verify the post-write policy
delta shows only the exact member addition and no other change.

## 8. Isolation and convergence stop

```text
SERVICE_ACCOUNT_CREATES=0
IAM_MUTATIONS=0
IAM_BINDINGS_ADDED=0
SERVICE_ACCOUNT_KEYS_CREATED=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
ADC_CONFIGURATION_CHANGES=0
AGENT_RUNTIME_DEPLOYMENTS=0
ADK_SMOKE_OR_EVAL_RUNS=0
LIVE_GHL_CALLS=0
SECRET_MANAGER_PAYLOAD_READS=0

FLEET_RUNTIME_IDENTITY_PROVEN=NO
GHL_PROVIDER_READ_PATH_PROVEN=NO
FLEET_AND_GHL_EXECUTION_AUTHORITY_JOINED=NO
CONVERGENCE_AUTHORIZED=NO

FUTURE_VERTICAL_SLICE=
  MG_GUIDE_ADD_ON_TO_AGENTIC_FLEET_TO_TRANSCRIPT_WORKFLOW_INTERPRETATION_TO_BOUNDED_GHL_REST_V3_EXECUTOR_TO_PERMITTED_CRM_WRITE_TO_DETERMINISTIC_READBACK_TO_AUDIT_PROOF
FUTURE_VERTICAL_SLICE_PLANNED_BY_THIS_UNIT=NO

NEXT=
  SEPARATE_EXACT_MEMBER_ADDITION_AUTHORIZATION_AFTER_THIS_PROOF_MERGES

STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_VERTEX_BINDING_STATE_RECLASSIFICATION_001_COMPLETE
STOP
```
