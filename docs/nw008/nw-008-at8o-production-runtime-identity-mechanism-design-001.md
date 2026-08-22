# NW-008 AT-8O — Production Runtime Identity Mechanism Design 001

```text
UNIT=NW008_AT8O_PRODUCTION_RUNTIME_IDENTITY_MECHANISM_DESIGN_001
PR_CLASS=planning_only
MODE=RUNTIME_IDENTITY_DESIGN_ONLY
OWNER=VS_CODE_ORCHESTRATOR

IMPLEMENTATION_PERFORMED=NO
IAM_CHANGES=0
SECRET_READS=0
SERVICE_ACCOUNT_IMPERSONATION_EXECUTED=NO
DEPLOYMENT_CHANGES=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

This artifact is a planning-only design document. It does not modify source,
tests, IAM, secrets, deployment, or any external system. It evaluates identity
mechanism options for the governed production runtime and records a design
decision.

## 1. Production runtime host class

```text
PRODUCTION_RUNTIME_HOST_CLASS=GOVERNED_SINGLE_INSTANCE_LONG_LIVED_LOCAL_PROCESS
```

The AT-1 bounded transport runtime executes as a single-instance, long-lived
local process on an operator-controlled host. It is not a Cloud Run service,
Cloud Function, GKE workload, or Compute Engine VM with attached metadata
server. The runtime must acquire GCP credentials from the local environment to
access Secret Manager and HighLevel via REST.

## 2. Target runtime principal

```text
TARGET_RUNTIME_PRINCIPAL=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_RUNTIME_PRINCIPAL_IDENTIFIED=YES
```

This service account was established in prior AT8K design as the
least-privilege principal for the GHL note-path runtime. It holds only the
IAM bindings required for Secret Manager accessor on the specific secrets
consumed by the runtime.

```text
USER_MANAGED_SERVICE_ACCOUNT_KEYS=0
AI_ROLODEX_CI_PRINCIPAL_REUSE=FORBIDDEN
DEC_027_PRESERVED=YES
```

DEC-027 prohibits reuse of the `ai-rolodex-to-crm` CI/deployment principal
for runtime workloads. The runtime principal is distinct.

## 3. AT8N parallel planning status

```text
AT8N_STATUS=PENDING_PARALLEL_PLANNING
AT8N_SUPERSEDED=NO
AT8N_SCOPE=GHL_PIT_SECRET_MANAGER_ACCESSOR_ONLY
```

AT8N plans the GHL PIT Secret Manager accessor binding for the runtime
principal. It is a parallel, non-overlapping lane. AT8O designs the identity
mechanism (how the runtime acquires credentials); AT8N designs the IAM grant
(what the credential authorizes). Neither implements anything.

## 4. Identity mechanism evaluation

### 4.1 Option A: Local operator ADC + short-lived service account impersonation

```text
OPTION=A
MECHANISM=LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION
```

The operator authenticates locally via `gcloud auth application-default login`.
The runtime discovers the operator's ADC, then uses
`google.auth.impersonated_credentials` to obtain short-lived access tokens for
the target runtime service account.

| Criterion | Assessment |
| --- | --- |
| Trust boundary | Operator identity is the trust root; runtime identity is derived |
| Credential lifetime | Short-lived (default 1 hour, configurable ≤12 hours); auto-refreshed |
| Keyless | YES — no exported service account key |
| Operator dependency | YES — operator must have active ADC and `roles/iam.serviceAccountTokenCreator` on target SA |
| Auditability | HIGH — Cloud Audit Logs record both operator identity and impersonated SA; impersonation events are logged |
| Revocation | Immediate — revoke operator ADC or remove Token Creator binding |
| Local-host compatibility | YES — works on any host with gcloud CLI and network access |
| Required IAM | `roles/iam.serviceAccountTokenCreator` on target SA for operator principal |
| Fail-closed behavior | YES — missing ADC, expired credentials, or removed Token Creator binding all fail before any Secret Manager or HighLevel call |
| Portability to governed host | HIGH — same SA works with Workload Identity Federation or attached SA on Cloud Run/GKE |

**Strengths**: Keyless, auditable, revocable, fail-closed, portable. Operator
identity is traceable. No long-lived credentials stored on disk beyond the
operator's own ADC refresh token (managed by gcloud).

**Weaknesses**: Requires operator to maintain active ADC. Token Creator binding
is an additional IAM grant. Adds impersonation latency (~1 RPC per token
refresh).

### 4.2 Option B: Direct user ADC as production runtime identity

```text
OPTION=B
MECHANISM=DIRECT_USER_ADC_AS_PRODUCTION_RUNTIME_IDENTITY
```

The operator's own user identity (via ADC) is used directly as the runtime
principal. Secret Manager IAM bindings are granted to the user, not a service
account.

| Criterion | Assessment |
| --- | --- |
| Trust boundary | Operator identity IS the runtime identity; no separation |
| Credential lifetime | ADC refresh token is long-lived; access tokens are short-lived |
| Keyless | YES |
| Operator dependency | YES |
| Auditability | MEDIUM — logs show user identity, but cannot distinguish runtime calls from other user activity |
| Revocation | Removes runtime access AND all other user access |
| Local-host compatibility | YES |
| Required IAM | Direct Secret Manager accessor and other bindings on user principal |
| Fail-closed behavior | YES — missing ADC fails |
| Portability to governed host | LOW — user ADC is not portable to Cloud Run/GKE; requires re-architecture |

**Strengths**: Simplest to set up. No impersonation IAM.

**Weaknesses**: Violates principal separation. Cannot distinguish runtime calls
from user activity. Not portable. Over-privileges user principal. DEC-027
intent is undermined if user principal accumulates runtime-specific IAM.

### 4.3 Option C: User-managed service account key

```text
OPTION=C
MECHANISM=USER_MANAGED_SERVICE_ACCOUNT_KEY
```

Export a JSON key file for the target service account. The runtime loads it
via `GOOGLE_APPLICATION_CREDENTIALS`.

| Criterion | Assessment |
| --- | --- |
| Trust boundary | Key file is the trust root; any holder can act as the SA |
| Credential lifetime | INDEFINITE — key does not expire unless manually rotated or deleted |
| Keyless | NO — exported key on disk |
| Operator dependency | NO — key file is self-contained |
| Auditability | LOW — logs show SA identity but cannot attribute to specific operator or host |
| Revocation | Requires key deletion in IAM console; rotation is manual |
| Local-host compatibility | YES |
| Required IAM | None beyond SA's own bindings |
| Fail-closed behavior | PARTIAL — missing key file fails, but a compromised key grants indefinite access |
| Portability to governed host | LOW — bad practice on Cloud Run/GKE; Workload Identity Federation is preferred |

**Strengths**: Simple, no operator dependency.

**Weaknesses**: Long-lived credential on disk. Highest exfiltration risk.
Violates Google Cloud security best practices. Not auditable to specific
operator. Manual rotation burden.

### 4.4 Option D: Attached cloud workload identity

```text
OPTION=D
MECHANISM=ATTACHED_CLOUD_WORKLOAD_IDENTITY
```

The runtime runs on a GCP-managed compute surface (Cloud Run, GKE, Compute
Engine) with the target SA attached via metadata server or Workload Identity.

| Criterion | Assessment |
| --- | --- |
| Trust boundary | Platform-managed; credentials never touch disk |
| Credential lifetime | Short-lived; auto-rotated by platform |
| Keyless | YES |
| Operator dependency | NO — platform-managed |
| Auditability | HIGH — SA identity in logs, attributed to specific workload |
| Revocation | Detach SA or delete workload |
| Local-host compatibility | NO — requires GCP-managed compute surface |
| Required IAM | SA bindings only; no Token Creator needed |
| Fail-closed behavior | YES — missing attachment fails |
| Portability to governed host | NATIVE — this IS the governed host pattern |

**Strengths**: Most secure. No credentials on disk. Auto-rotated.

**Weaknesses**: Not compatible with current local-process host class. Requires
migration to Cloud Run/GKE. Not applicable for current development phase.

## 5. Design decision

```text
PRODUCTION_RUNTIME_IDENTITY_MECHANISM_DECIDED=YES
SELECTED_IDENTITY_MECHANISM=LOCAL_OPERATOR_ADC_PLUS_SHORT_LIVED_SERVICE_ACCOUNT_IMPERSONATION
```

### 5.1 Selection rationale

Option A is selected because:

1. **Keyless**: No exported service account keys (Option C rejected).
2. **Principal separation**: Runtime acts as dedicated SA, not operator user
   identity (Option B rejected).
3. **Local-host compatible**: Works on current governed single-instance host
   (Option D deferred — not rejected for future migration).
4. **Auditable**: Both operator identity and impersonated SA are logged.
5. **Fail-closed**: Missing ADC, expired token, or removed Token Creator
   binding all prevent any downstream call.
6. **Portable**: Same target SA transitions to Workload Identity when the
   runtime migrates to a governed cloud host.

### 5.2 Rejected and deferred options

```text
DIRECT_USER_ADC_AS_RUNTIME_IDENTITY=REJECT
USER_MANAGED_SA_KEY=REJECT
CLOUD_WORKLOAD_ATTACHMENT=DEFER
```

Option B is rejected: violates principal separation, not portable, undermines
DEC-027 intent.

Option C is rejected: long-lived key on disk, highest exfiltration risk,
violates Google Cloud security best practices.

Option D is deferred: correct long-term target, but not compatible with current
local-process host class. The selected SA and IAM design are portable to
Option D when the host migrates.

## 6. Resolved identity parameters

```text
SOURCE_PRINCIPAL_IDENTIFIED=YES
SOURCE_PRINCIPAL=OPERATOR_ADC_IDENTITY

TARGET_RUNTIME_PRINCIPAL_IDENTIFIED=YES
TARGET_RUNTIME_PRINCIPAL=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com

SERVICE_ACCOUNT_TOKEN_CREATOR_BINDING_REQUIRED=YES
TOKEN_CREATOR_TARGET_RESOURCE=serviceAccount:mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
IMPERSONATION_TOKEN_LIFETIME_POLICY=DEFAULT_1_HOUR

MISSING_RUNTIME_IDENTITY=FAIL_CLOSED
IDENTITY_DISCOVERY_FROM_ENVIRONMENT=FORBIDDEN_UNLESS_EXPLICITLY_DESIGNED
CALLER_SUPPLIED_RUNTIME_IDENTITY_OVERRIDE=FORBIDDEN
```

The operator's ADC identity is the source principal. The runtime impersonates
the target SA with short-lived tokens (default 1-hour lifetime). The Token
Creator binding is on the target SA resource, granted to the operator's
identity.

Identity discovery from environment variables or implicit ADC chain is
forbidden unless explicitly designed in a future implementation authorization.
The runtime must fail closed if the impersonation chain cannot be established.
Caller-supplied identity overrides are forbidden.

## 7. AT8N advancement

```text
AT8N_CAN_ADVANCE_AFTER_AT8O=PARALLEL
COMMITMENT_KEY_SECRET_IAM_DESIGN_INCLUDED=NO
LIVE_PRODUCTION_STORE_ACTIVATION_AUTHORIZATION_DESIGNABLE=NO
```

AT8N can proceed in parallel. It designs the Secret Manager accessor IAM
binding for the target SA, independent of the identity mechanism decision.
AT8O does not include commitment-key secret IAM design (AT8N scope) or live
production store activation authorization.

## 8. Implementation boundary

```text
AT8O_IMPLEMENTS_CODE=NO
AT8O_IMPLEMENTS_IAM=NO
AT8O_IMPLEMENTS_IMPERSONATION=NO
AT8O_READS_SECRETS=NO

NEXT_IMPLEMENTATION_REQUIRES_SEPARATE_AUTHORIZATION=YES
NEXT_IMPLEMENTATION_MUST_FREEZE_IDENTITY_MECHANISM=YES
NEXT_IMPLEMENTATION_MUST_INCLUDE_FAIL_CLOSED_IDENTITY_VALIDATION=YES
```

This design document freezes the identity mechanism decision. Any future
implementation that wires impersonation, grants Token Creator, reads secrets,
or activates the production runtime requires a separate, explicitly scoped
authorization PR.

## 9. Validation

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o-production-runtime-identity-mechanism-design-001.md
SRC_CHANGES=0
TEST_CHANGES=0
IAM_CHANGES=0
SECRET_CHANGES=0
DEPLOYMENT_CHANGES=0
IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```
