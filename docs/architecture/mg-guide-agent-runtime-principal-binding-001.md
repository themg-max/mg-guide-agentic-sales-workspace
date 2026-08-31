# MG Guide — Agent Runtime Principal Binding 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_BINDING_001
ARTIFACT_PATH=
  docs/architecture/mg-guide-agent-runtime-principal-binding-001.md
CLASSIFICATION=ARCHITECTURE_PRINCIPAL_BINDING_RESOLUTION
PR_CLASS=architecture
MODE=PLANNING_AND_BINDING_RESOLUTION_ONLY
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T01:08:00Z

BRANCH_AT_AUTHORING=
  docs/nw008-ghl-403-close-and-agent-runtime-principal-binding-001
BRANCH_IS_MAIN=NO

IAM_MUTATIONS=0
SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
API_ENABLEMENTS=0
DEPLOYMENTS=0
SECRET_MUTATIONS=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

This artifact **resolves** the durable MG Guide Agent Runtime principal against
the currently observed ADC principal. It does **not** grant IAM, create or
delete a service account, mint keys, change ADC, deploy Agent Runtime, access
HighLevel, or mutate secrets.

```text
VERTEX_IAM_GRANT_EXECUTED_IN_THIS_UNIT=NO
MERGE_ALONE_AUTHORIZES_IAM_MUTATION=NO
IAM_GRANT_TO_OBSERVED_ADC_ALLOWED=NO
```

## 1. Why this binding is required now

Local Agent Runtime readiness previously reported:

```text
OBSERVED_ADC_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_ADC_CREDENTIAL_TYPE=other
OBSERVED_ADC_CREDENTIAL_SUBTYPE=impersonated_service_account
OBSERVED_ADC_PROJECT=ai-rolodex-to-crm
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=NO
AGENT_RUNTIME_IAM_READY=NO
```

Those facts come from:

- `docs/architecture/mg-guide-agent-runtime-iam-readiness-001.md`
- `docs/architecture/mg-guide-agent-runtime-principal-decision-001.md`

They describe the **currently resolved local ADC**, not the approved durable
MG Guide Agent Runtime identity. Granting `roles/aiplatform.user` (or any
Vertex permission) to the observed ADC without first resolving the intended
principal would enlarge the wrong blast radius.

## 2. Durable principal — RESOLVED

The durable MG Guide Agent Runtime principal is already designated, created,
and retained by merged governance/proof:

```text
INTENDED_DURABLE_MG_GUIDE_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_DISPLAY_NAME=MG Guide Agent Runtime
SELECTED_OPTION=DEDICATED_MG_GUIDE_RUNTIME_SERVICE_ACCOUNT
REUSE_BABY_BUMPS_RUNTIME_B=NO
PRINCIPAL_REUSE_ALLOWED=NO
```

Authority chain for principal existence (already on origin/main):

```text
PRINCIPAL_CREATION_AUTHORIZATION=
  governance/authorizations/mg-guide-agent-runtime-principal-creation-authorization-001.md
ONE_CREATE_EXECUTION_PROOF=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-principal-one-create-execution-proof-001.md
ONE_CREATE_EXECUTION_PROOF_PR=302
ONE_CREATE_EXECUTION_PROOF_MERGE_SHA=
  6691a8d3e51b6066adebbe30a29018e44adeea23
```

Fresh read-only existence check for this unit:

```text
SERVICE_ACCOUNT_EXISTS=YES
SERVICE_ACCOUNT_EMAIL_MATCH=YES
SERVICE_ACCOUNT_PROJECT_MATCH=YES
SERVICE_ACCOUNT_DISPLAY_NAME_MATCH=YES
SERVICE_ACCOUNT_DISABLED=NO
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=YES
```

## 3. Observed ADC vs intended durable runtime

```text
OBSERVED_ADC_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
INTENDED_DURABLE_MG_GUIDE_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

OBSERVED_ADC_EQUALS_INTENDED_RUNTIME=NO
```

Consequences:

```text
IAM_GRANT_TO_OBSERVED_ADC_ALLOWED=NO
IAM_GRANT_CANDIDATE_REVIEW_ALLOWED=NO
SHARED_IDENTITY_GOVERNANCE_ACCEPTED=NO
OPTION_A_REUSE_BABY_BUMPS_REJECTED=YES
NEXT=REPAIR_ADC_OR_RUNTIME_IDENTITY_SELECTION
```

Local smoke/eval that currently resolve ADC to Baby Bumps Runtime B are using
the wrong principal for MG Guide Agent Runtime. Remediation is an **identity
selection / ADC repair** problem first, not a grant-to-observed-ADC problem.

```text
DO_NOT_GRANT_VERTEX_TO_BABY_BUMPS_FOR_MG_GUIDE=YES
DO_NOT_TREAT_LOCAL_ADC_AS_DURABLE_RUNTIME_IDENTITY=YES
```

## 4. Existing Vertex binding on the intended principal (read-only)

A separate, already-consumed Lane A unit added the exact intended member to the
existing unconditional project binding for `roles/aiplatform.user`:

```text
PRIOR_VERTEX_EXACT_MEMBER_ADDITION_PROOF=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-vertex-exact-member-addition-execution-proof-002.md
PRIOR_VERTEX_MEMBER=
  serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PRIOR_VERTEX_ROLE=roles/aiplatform.user
PRIOR_VERTEX_PROJECT=ai-rolodex-to-crm
```

Fresh read-only confirmation in this unit:

```text
INTENDED_PRINCIPAL_HAS_ROLES_AIPLATFORM_USER_ON_PROJECT=YES
OBSERVED_ADC_HAS_ROLES_AIPLATFORM_USER_ON_PROJECT=NO
```

Therefore:

```text
VERTEX_PERMISSION_GAP_ON_INTENDED_PRINCIPAL=NO
VERTEX_PERMISSION_GAP_ON_OBSERVED_ADC=YES
GAP_CLASS=
  LOCAL_ADC_POINTS_AT_NON_INTENDED_PRINCIPAL
```

Policy Troubleshooter / `aiplatform.endpoints.predict` must still be re-proven
**as the intended principal** after ADC/runtime identity selection is repaired.
The readiness artifact's `AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=NO` remains true
for the observed ADC and must not be misread as absence of the project role on
`mg-guide-agent-runtime@...`.

```text
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT_FOR_OBSERVED_ADC=NO
AIPLATFORM_ENDPOINTS_PREDICT_REPROOF_REQUIRED_AS_INTENDED_PRINCIPAL=YES
AGENT_RUNTIME_IAM_READY=NO
```

`AGENT_RUNTIME_IAM_READY` stays `NO` until identity selection is repaired and
predict permission is verified under the intended principal.

## 5. Candidate Vertex IAM authorization (NOT authored, NOT effective)

The task template names a future separate authorization artifact:

```text
FUTURE_CANDIDATE_AUTHORIZATION_PATH=
  governance/authorizations/mg-guide-agent-runtime-vertex-predict-iam-authorization-001.md
FUTURE_CANDIDATE_ROLE=roles/aiplatform.user
FUTURE_CANDIDATE_REQUIRED_PERMISSION=
  aiplatform.endpoints.predict
FUTURE_CANDIDATE_AUTHORED_IN_THIS_UNIT=NO
FUTURE_CANDIDATE_EFFECTIVE=NO
```

Bounds that any such future authorization must freeze before becoming
executable (merge alone still must not execute IAM):

```text
MAX_IAM_BINDING_ADDITIONS=1
IAM_REMOVALS=0
SERVICE_ACCOUNT_CREATES=0
SERVICE_ACCOUNT_KEY_CREATES=0
CUSTOM_ROLE_CREATES=0
API_ENABLEMENTS=0
DEPLOYMENTS=0
SECRET_MUTATIONS=0
GHL_CALLS=0
CRM_MUTATIONS=0
```

Because the intended principal **already** holds the candidate project role,
any new authorization must first complete exact resource/grant-scope review and
fresh read-only revalidation. Likely outcomes after binding merge:

1. **No new project-role addition** — only ADC/runtime identity repair + Policy
   Troubleshooter reproof as `mg-guide-agent-runtime@...`; or
2. A narrowly scoped residual grant only if fresh review proves a real missing
   binding on the exact intended member/resource (not on Baby Bumps).

```text
NEW_IAM_AUTH_REQUIRED_BEFORE_IDENTITY_REPAIR=NO
IAM_GRANT_TO_OBSERVED_ADC_ALLOWED=NO
```

## 6. Required identity-repair path (before smoke)

```text
NEXT=REPAIR_ADC_OR_RUNTIME_IDENTITY_SELECTION

REPAIR_GOAL=
  Make local and deployed Agent Runtime execution resolve to
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
  rather than baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com

ACCEPTABLE_REPAIR_CLASSES=
  - configure local ADC / impersonation to the intended principal
  - configure Agent Runtime deploy identity to the intended principal
  - document and enforce that Baby Bumps is out of MG Guide runtime scope

FORBIDDEN_REPAIR_CLASSES=
  - grant roles/aiplatform.user to baby-bumps-runtime-b for MG Guide convenience
  - treat observed ADC as the durable runtime principal by silence
  - mint user-managed keys for either principal in this lane without separate
    key authority
```

After repair, require read-only verification:

```text
REQUIRED_POST_REPAIR_CHECKS=
  - OBSERVED_OR_RUNTIME_PRINCIPAL_EQUALS_INTENDED=YES
  - Policy Troubleshooter or equivalent:
      principal=mg-guide-agent-runtime@...
      permission=aiplatform.endpoints.predict
      result allows access
  - AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=YES
  - AGENT_RUNTIME_IAM_READY=YES
```

## 7. Agent architecture freezes (unchanged)

```text
EXISTING_AGENT_GRAPH=YES
EXISTING_DELEGATES=YES
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO

INITIAL_MODE=SYNTHETIC_ONLY
LIVE_GHL_ADAPTER_ENABLED=NO
CRM_MUTATION_AUTHORIZED=NO
TARGET_AUTH_MODE=GOOGLE_CLOUD_ADC_FOR_AGENT_RUNTIME
MODEL_LOCATION=global
AGENT_RUNTIME_REGION=us-east1
DETERMINISTIC_EVALUATION_HARD_GATES=YES
```

Synthetic-only smoke remains the first runtime exercise after IAM readiness:

```text
SYNTHETIC_SMOKE_AUTHORIZED_NOW=NO
SYNTHETIC_SMOKE_REQUIRES=
  AGENT_RUNTIME_IAM_READY=YES
  EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=YES (human attestation)
```

## 8. GHL lane separation

The GHL REST v3 bounded-read 004 path is closed and healthy under PIT v2. That
outcome does not bind HighLevel credentials to Agent Runtime.

```text
NW008_GHL_403_BLOCKER=CLOSED
PROVIDER_403_RESOLVED=YES
AUTHORITY_004_CONSUMED_TERMINAL=YES
GHL_CALLS_IN_THIS_UNIT=0
PIT_OR_TOKEN_BOUND_TO_AGENT_RUNTIME=NO
LIVE_GHL_ADAPTER_ENABLED=NO
```

## 9. Security gate

```text
EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=
  PENDING_HUMAN_ATTESTATION
DEPLOYMENT_ALLOWED_BEFORE_SECURITY_GATE=NO
MG_GUIDE_RUNTIME_USES_GEMINI_API_KEY=NO
TARGET_AUTH_MODE=GOOGLE_CLOUD_ADC_FOR_AGENT_RUNTIME
KEY_VALUE_OR_HASH_OR_PREFIX_OR_SUFFIX_IN_THIS_ARTIFACT=NO
```

## 10. Decision board and stop

```text
INTENDED_DURABLE_MG_GUIDE_AGENT_RUNTIME_PRINCIPAL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_ADC_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
OBSERVED_ADC_EQUALS_INTENDED_RUNTIME=NO
IAM_GRANT_TO_OBSERVED_ADC_ALLOWED=NO
IAM_GRANT_CANDIDATE_REVIEW_ALLOWED=NO
AGENT_RUNTIME_IAM_READY=NO
AIPLATFORM_ENDPOINTS_PREDICT_PRESENT=NO
  (for observed ADC; reproof required as intended principal after repair)

NEXT=REPAIR_ADC_OR_RUNTIME_IDENTITY_SELECTION

AFTER_IDENTITY_REPAIR_AND_PREDICT_REPROOF=
  AGENT_RUNTIME_IAM_READY=YES
  THEN synthetic-only smoke/eval hard gates
  THEN separate AGENT_RUNTIME_DEPLOYMENT_AUTHORIZATION
  THEN later, under separate live CRM authority, the synthetic transcript
    → root agent → exact contact → exact opportunity → create note →
    note readback → stage update → opportunity readback path

NO_IAM_MUTATION=YES
NO_GHL_CALL=YES
NO_DEPLOY=YES
NO_SECRET_MUTATION=YES
STOP=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_BINDING_001_COMPLETE
```
