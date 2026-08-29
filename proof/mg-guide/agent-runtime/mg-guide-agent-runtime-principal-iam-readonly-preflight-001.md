# MG Guide Agent Runtime Principal — Read-Only IAM Preflight 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_IAM_READONLY_PREFLIGHT_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-principal-iam-readonly-preflight-001.md
CLASSIFICATION=IAM_READ_ONLY_PREFLIGHT
PR_CLASS=PROOF
MODE=READ_ONLY_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

READ_ONLY_ONLY=YES
IAM_MUTATION_AUTHORIZED_IN_THIS_UNIT=NO
SELF_ACTIVATION=FORBIDDEN
DO_NOT_MUTATE_IAM_IN_THIS_UNIT=YES
```

This unit performs a fresh, read-only observation of the exact MG Guide Agent
Runtime principal and the exact proposed project IAM binding. It does not
create a service account, add or remove a binding, mint a key, impersonate the
principal, mutate secrets, call HighLevel, write CRM, deploy Agent Runtime, or
run ADK smoke/eval as this identity.

```text
IAM_MUTATIONS=0
SERVICE_ACCOUNT_CREATES=0
IAM_BINDINGS_ADDED=0
SERVICE_ACCOUNT_KEYS_CREATED=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SECRET_MUTATIONS=0
LIVE_GHL_CALLS=0
AGENT_RUNTIME_DEPLOYMENTS=0
```

## 1. Source authorization inspected on origin/main

```text
AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_EXECUTION_AUTHORIZATION_001
AUTHORIZATION_ARTIFACT_PATH=
  governance/authorizations/mg-guide-agent-runtime-principal-creation-execution-authorization-001.md
SOURCE_AUTHORIZATION_PRESENT_ON_MAIN=YES

ORIGIN_MAIN_SHA=
  ce4aaaa8a5bd3663248b00f42db913287d539301
AUTHORIZATION_AUTHOR_COMMIT_SHA=
  cbcbb00074e8e724acd6e71e49541560bf84d3c1
AUTHORIZATION_BLOB_SHA_AT_ORIGIN_MAIN=
  e6907469f841250df71fe4469c5d004eb7e88531
AUTHORIZATION_MERGE_PR=296
AUTHORIZATION_MERGE_SHA=
  ce4aaaa8a5bd3663248b00f42db913287d539301
AUTHORIZATION_MERGED_AT_UTC=2026-08-29T13:57:03Z

PREFLIGHT_BRANCH=
  preflight/mg-guide-agent-runtime-iam-readonly-001
PREFLIGHT_BASE_REF=origin/main
PREFLIGHT_BASE_SHA=
  ce4aaaa8a5bd3663248b00f42db913287d539301
```

Durable authority chain referenced by the execution authorization (not
re-executed here):

```text
PRINCIPAL_AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_AUTHORIZATION_001
COUNTERSIGNATURE_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_COUNTERSIGNATURE_001
```

Maximum FUTURE bounds from the authorization (ceilings only; not mutation
instructions):

```text
MAX_SERVICE_ACCOUNT_CREATES=1
MAX_IAM_BINDINGS=1
MAX_SERVICE_ACCOUNT_KEYS=0
PROPOSED_ROLE=roles/aiplatform.user
PROPOSED_BINDING_SCOPE=PROJECT_ai-rolodex-to-crm
```

## 2. Observation context

```text
OBSERVATION_TIMESTAMP_UTC=2026-08-29T14:10:23Z
OBSERVATION_TIMESTAMP_LOCAL=2026-08-29T10:10:23-0400
ACTIVE_GCLOUD_PROJECT=ai-rolodex-to-crm

PROJECT=ai-rolodex-to-crm
PROJECT_LIFECYCLE_STATE=ACTIVE

SERVICE_ACCOUNT_ID=mg-guide-agent-runtime
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROPOSED_MEMBER=
  serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
PROPOSED_ROLE=roles/aiplatform.user
PROPOSED_BINDING_SCOPE=PROJECT_ai-rolodex-to-crm
```

No access token, refresh token, credential JSON, secret payload, operator
account identity, project number, metrics environment tag, or unrelated IAM
member roster is recorded in this artifact.

## 3. Service-account existence classification

Fresh read-only commands:

```text
gcloud iam service-accounts describe \
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com \
  --project=ai-rolodex-to-crm
# RESULT=NOT_FOUND: Unknown service account.
# EXIT=1

gcloud iam service-accounts list \
  --project=ai-rolodex-to-crm \
  --filter='email:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com' \
  --format=json
# RESULT=[]
# EXIT=0
```

```text
SERVICE_ACCOUNT_EXISTS=NO
SERVICE_ACCOUNT_METADATA=NOT_APPLICABLE_PRINCIPAL_ABSENT
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=NOT_APPLICABLE

SERVICE_ACCOUNT_STATE=STATE_1
SERVICE_ACCOUNT_STATE_1=
  ABSENT_AND_EXACT_CREATION_PLAN_CONFLICT_FREE
SERVICE_ACCOUNT_STATE_1_ACTION=
  ELIGIBLE_FOR_AT_MOST_ONE_CREATE_AFTER_SEPARATE_HUMAN_ACTIVATION
CREATE_ALREADY_SATISFIED=NO
CREATE_ATTEMPTED_IN_THIS_UNIT=NO
SERVICE_ACCOUNT_CREATES=0
```

Near-name collision screening was performed only to confirm the exact target
email is free; near-name account emails are not published in this public proof
and are not alternate authorized targets.

```text
EXACT_TARGET_EMAIL_COLLISION=NO
ALTERNATE_SERVICE_ACCOUNT_ALLOWED_BY_AUTHORIZATION=NO
NEAR_NAME_ACCOUNTS_ARE_NOT_SUBSTITUTES=YES
```

No conflicting metadata can exist for an absent exact principal. Observation of
existence is unambiguous (`NOT_FOUND` plus empty filtered list).

## 4. Proposed exact binding classification

Because the exact principal is absent, the proposed project-level member/role
binding is not yet applicable. No synthetic principal was created merely to
inspect a binding.

```text
BINDING_STATE=NOT_YET_APPLICABLE_PRINCIPAL_ABSENT
PROPOSED_EXACT_BINDING_PRESENT=NOT_APPLICABLE
BINDING_ALREADY_SATISFIED=NO
BIND_ATTEMPTED_IN_THIS_UNIT=NO
IAM_BINDINGS_ADDED=0
```

Sanitized project IAM policy probe (exact-target classification only; policy
etag, aggregate binding counts, and unrelated members are not published):

```text
gcloud projects get-iam-policy ai-rolodex-to-crm --format=json
# exact-target member/role classification only; no public policy dump

EXACT_MEMBER=
  serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
EXACT_ROLE=roles/aiplatform.user

EXACT_MEMBER_ROLE_UNCONDITIONAL_BINDING_PRESENT=NO
# Exact target principal is absent, so no project binding can attach to it yet.
```

When a later separately human-authorized execution creates the exact principal
and verifies readback, that execution must re-classify binding state under the
authorization’s STATE_1 / STATE_2 / STATE_3 rules before any bind attempt.
Ceiling remains `MAX_IAM_BINDINGS=1`.

## 5. Least-privilege role review

Intended next capability (authorization-bound; not executed here): synthetic MG
Guide Agent Runtime using Vertex inference.

```text
LEAST_PRIVILEGE_ROLE_CANDIDATE=roles/aiplatform.user
ROLE_TITLE=Agent Platform User
ROLE_STAGE=GA
HAS_aiplatform.endpoints.predict=YES
```

Comparative predefined-role spot-checks (read-only `gcloud iam roles describe`;
not an exhaustive least-privilege proof over the full role catalog):

```text
roles/aiplatform.viewer
  HAS_aiplatform.endpoints.predict=NO

roles/aiplatform.user
  HAS_aiplatform.endpoints.predict=YES

roles/aiplatform.admin
  HAS_aiplatform.endpoints.predict=YES
  (broader than user; not a least-privilege substitute)

roles/serviceusage.serviceUsageConsumer
  HAS_aiplatform.endpoints.predict=NO
```

```text
LEAST_PRIVILEGE_ROLE_REVIEW=CANDIDATE_ACCEPTABLE
CURRENTLY_AUTHORIZED_SUITABLE_GA_CANDIDATE=roles/aiplatform.user
NARROWER_SUITABLE_GA_ROLE_FOR_EXACT_STANDARD_AGENT_RUNTIME_PATH_ESTABLISHED=NO
BROADER_ROLE_SUBSTITUTION_AUTHORIZED=NO
ALTERNATE_ROLE_ALLOWED_BY_AUTHORIZATION=NO
CUSTOM_ROLE_DESIGN_IN_THIS_UNIT=NO
ROLE_GRANT_PERFORMED_IN_THIS_UNIT=NO
```

Evidence summary: `roles/aiplatform.user` remains the currently authorized
suitable GA candidate for the stated synthetic Agent Runtime / Vertex inference
purpose and includes `aiplatform.endpoints.predict`. Spot-checks show
`roles/aiplatform.viewer` lacks predict and `roles/aiplatform.admin` is broader.
This unit does **not** claim that `roles/aiplatform.user` is the absolute
narrowest predefined role in the catalog merely because viewer lacks predict.
No narrower suitable GA role for this exact standard Agent Runtime path was
established here. This review does not authorize mutation, does not broaden
permissions, and does not substitute another role. A future custom or alternate
role would require an updated authorization, not silent substitution.

## 6. Ambiguity and conflict ledger

```text
AMBIGUITY_DETECTED=NO
CONFLICTING_METADATA_DETECTED=NO
EXACT_PRINCIPAL_IDENTITY_COLLISION=NO
FAIL_CLOSED_REQUIRED=NO
SERVICE_ACCOUNT_STATE_3=NO
BINDING_STATE_3=NO
```

## 7. Mutation and side-effect attestations

```text
IAM_MUTATIONS=0
SERVICE_ACCOUNT_CREATES=0
IAM_BINDINGS_ADDED=0
SERVICE_ACCOUNT_KEYS_CREATED=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SECRET_MUTATIONS=0
LIVE_GHL_CALLS=0
AGENT_RUNTIME_DEPLOYMENTS=0
CRM_WRITES=0
ADK_SMOKE_OR_EVAL_AS_TARGET_IDENTITY=0

NO_IAM_MUTATION=YES
NO_SERVICE_ACCOUNT_CREATE=YES
NO_IAM_BINDING_CHANGE=YES
NO_SERVICE_ACCOUNT_KEY=YES
NO_SERVICE_ACCOUNT_IMPERSONATION=YES
NO_SECRET_MUTATION=YES
NO_HIGHLEVEL_CALL=YES
NO_CRM_WRITE=YES
NO_AGENT_RUNTIME_DEPLOYMENT=YES
```

## 8. Classification return block

```text
IAM_PREFLIGHT_STATUS=READY_FOR_HUMAN_EXECUTION_REVIEW

SOURCE_AUTHORIZATION_PRESENT_ON_MAIN=YES
AUTHORIZATION_ID=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_CREATION_EXECUTION_AUTHORIZATION_001

PROJECT=ai-rolodex-to-crm
SERVICE_ACCOUNT_EMAIL=
  mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SERVICE_ACCOUNT_EXISTS=NO
SERVICE_ACCOUNT_STATE=STATE_1
SERVICE_ACCOUNT_METADATA_ACCEPTABLE=NOT_APPLICABLE

PROPOSED_EXACT_BINDING_PRESENT=NOT_APPLICABLE
BINDING_STATE=NOT_YET_APPLICABLE_PRINCIPAL_ABSENT

LEAST_PRIVILEGE_ROLE_CANDIDATE=roles/aiplatform.user
LEAST_PRIVILEGE_ROLE_REVIEW=CANDIDATE_ACCEPTABLE
```

## 9. Next governed action

```text
NEXT=HUMAN_REVIEW_FOR_BOUNDED_IAM_EXECUTION

THIS_UNIT_DOES_NOT_ACTIVATE_MUTATION=YES
HUMAN_EXECUTION_AUTHORITY_STILL_REQUIRED=YES
FRESH_PREFLIGHT_NOW_AVAILABLE_FOR_BINDING=YES
LEAST_PRIVILEGE_REVIEW_RECORDED=YES

IF_HUMAN_ACTIVATES_LATER=
  AT_MOST_ONE_SERVICE_ACCOUNT_CREATE_FOR_EXACT_ID
  THEN_CREATE_READBACK_REQUIRED
  THEN_RECLASSIFY_BINDING_STATE
  THEN_AT_MOST_ONE_PROJECT_BINDING_OF_EXACT_MEMBER_TO_roles/aiplatform.user
  THEN_BINDING_READBACK_REQUIRED
  MAX_SERVICE_ACCOUNT_KEYS_REMAINS_0
  NO_IMPERSONATION_GRANT_IN_THIS_CHAIN
  NO_GHL_CRM_SECRET_OR_DEPLOY_AUTHORITY
```

## 10. STOP

```text
STOP_CODE=
  MG_GUIDE_AGENT_RUNTIME_PRINCIPAL_IAM_READONLY_PREFLIGHT_001_COMPLETE
IAM_PREFLIGHT_EXECUTED=YES
IAM_STATE_INVENTED=NO
IAM_MUTATIONS=0
STOP
```
