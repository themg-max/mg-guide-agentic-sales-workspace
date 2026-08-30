# NW-008 AT1 GHL Runtime Identity and Retry-Control Repair Plan 001

## 0. Plan identity and boundary

```text
PLAN_ID=
  NW008_AT1_GHL_RUNTIME_IDENTITY_AND_RETRY_CONTROL_REPAIR_PLAN_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-runtime-identity-and-retry-control-repair-plan-001.md
CLASSIFICATION=BOUNDED_RUNTIME_AND_TEST_REPAIR_PLAN
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace

BASE=origin/main@ab7ce6bd723d78cfb2883b1230958492ed84a074
BRANCH=repair/nw008-at1-runtime-identity-retry-control-001
BRANCH_IS_MAIN=NO

LIVE_TOKEN_MINT_AUTHORIZED=NO
SECRET_MANAGER_ACCESS_AUTHORIZED=NO
HIGHLEVEL_CALL_AUTHORIZED=NO
CRM_CALL_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
```

This plan approves only the deterministic runtime and test repair surfaces listed
in section 5. It does not authorize a live execution, credential refresh, token
mint, secret read, HighLevel call, CRM call, deployment, service-account key, or
IAM policy change.

## 1. Reviewed and merged inputs

```text
PR_340_FORMAL_VERDICT=READY_FOR_MERGE
PR_340_REVIEW_ID=5060232118
PR_340_REVIEWED_HEAD=3b451fae89331489d8085a1634165440ed4e8324
PR_340_MERGE_SHA=2c72d5fc429052fa91de94edcb6dbf3c9b03ab8d

PR_341_FORMAL_VERDICT=READY_FOR_MERGE
PR_341_REVIEW_ID=5060232951
PR_341_REVIEWED_HEAD=b44bef2dca3231cd42ad4690df75ad47483dcbc5
PR_341_MERGE_SHA=ab7ce6bd723d78cfb2883b1230958492ed84a074
```

The merged evidence establishes:

```text
ROOT_CAUSE=
  EXECUTION_RUNTIME_DID_NOT_MATERIALIZE_DEDICATED_GHL_WORKFLOW_IDENTITY
OBSERVED_SOURCE_PRINCIPAL=
  baby-bumps-runtime-b@ai-rolodex-to-crm.iam.gserviceaccount.com
EXPECTED_SOURCE_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_PRINCIPAL_MATCH=NO

IAM_GRANT_REPAIR_REQUIRED=NO
RUNTIME_IDENTITY_MATERIALIZATION_REPAIR_REQUIRED=YES
RETRY_CONTROL_REPAIR_REQUIRED=YES
```

The existing IAM relationship remains authoritative and unchanged:

```text
mg-guide-ghl-workflow
  -> roles/iam.serviceAccountTokenCreator
  -> exact mg-guide-ghl-note-runtime
```

## 2. Deterministic source-principal contract

The runtime composition root will define one immutable expected source:

```text
EXPECTED_SOURCE_PRINCIPAL=
  mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_RUNTIME_PRINCIPAL=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SOURCE_PRINCIPAL_COMPARISON=EXACT
SOURCE_IDENTITY_GATE_POSITION=BEFORE_TARGET_IMPERSONATION
```

The production path will no longer call `google.auth.default()`. It will require
an explicit root-owned credential configuration path from:

```text
MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG
```

The composition root will load that exact file with
`google.auth.load_credentials_from_file()`. The accepted credential object must
be `google.auth.impersonated_credentials.Credentials`, which materializes a
short-lived service-account identity without a service-account key. Its
`service_account_email` must exactly equal `EXPECTED_SOURCE_PRINCIPAL`.
Authorized-user credentials, compute credentials, external ambient ADC,
service-account key credentials, and unrelated impersonated credentials are not
accepted at this boundary.

The validated credential object and exact principal will be wrapped in a private
materialized-source value. Target impersonation will accept only that value, so
the source gate cannot be bypassed by passing an arbitrary credential object.

On an exact-principal mismatch, the raised fail-closed result will expose only
non-secret control fields:

```text
SOURCE_IDENTITY_GATE=FAIL
TOKEN_MINT_ATTEMPTS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
STOP=SOURCE_PRINCIPAL_MISMATCH
```

No credential refresh occurs while loading or inspecting the source credential.

## 3. Credential and Secret Manager retry-control repair

The application credential provider and both production Secret Manager adapters
will be one-shot:

```text
MAX_PROVIDER_CREDENTIAL_ATTEMPTS=1
MAX_SECRET_MANAGER_ATTEMPTS_PER_ADAPTER=1
AUTOMATIC_RETRY_DISABLED=YES
```

The provider attempt counter advances before secret access. A failed first
attempt is terminal for that provider instance, and a second call is rejected
without invoking the accessor.

Each Secret Manager adapter will:

1. advance its attempt counter before the client invocation;
2. reject any second invocation before client access; and
3. call `access_secret_version(..., retry=None)` explicitly.

Passing `retry=None` removes the `google-api-core` default retry object that
caused the merged execution's hidden credential-metadata retry loop. The target
impersonated credential remains lazy during assembly; construction alone does
not refresh or mint.

## 4. Ordering and fail-closed execution

The repaired production composition order is:

1. require the root-owned execution-store path;
2. require the explicit workflow credential-config path;
3. load the explicit credential object without refresh;
4. require the allowed impersonated credential class;
5. resolve and exactly compare `service_account_email`;
6. create the private materialized-source value;
7. construct target credentials for the unchanged note-runtime principal;
8. construct the Secret Manager client with those target credentials;
9. perform later one-shot secret operations only when a separately authorized
   future live execution reaches them.

A source mismatch stops at step 5. It cannot construct target credentials,
construct a Secret Manager client, read a secret payload, or dispatch HighLevel.

## 5. Approved implementation and test surfaces

Only these paths are approved for this repair:

```text
docs/nw008/nw-008-at1-ghl-runtime-identity-and-retry-control-repair-plan-001.md
src/integrations/ghl/highlevel_rest/live_note_runtime.py
src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
src/integrations/ghl/at1_commitment_key_provider.py
tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py
tests/integrations/ghl/test_at1_commitment_key_provider.py
```

No IAM, Terraform, deployment, workflow, secret, provider-integration, or
authorization artifact is in scope.

## 6. Deterministic verification matrix

All verification uses injected fake modules, credential objects, and Secret
Manager clients. No test may refresh a credential or reach a live client.

```text
EXPECTED_SOURCE_MATCH_PASS=
  explicit config loads once; expected source is wrapped; target constructor
  receives exactly the wrapped workflow credential

WRONG_SOURCE_FAIL_CLOSED=
  mismatch raises SOURCE_PRINCIPAL_MISMATCH; target constructor calls=0;
  Secret Manager client constructions=0; token mints=0; secret reads=0;
  GHL calls=0

MAX_PROVIDER_CREDENTIAL_ATTEMPTS=1=
  first failed provider attempt consumes the only attempt; second provider call
  performs no accessor call

AUTOMATIC_RETRY_DISABLED=YES=
  both Secret Manager adapters invoke their fake client once with retry=None;
  second adapter call is rejected before client access

SECRET_NON_DISCLOSURE=PASS=
  credential payload is absent from exceptions, repr, str, and logs

IAM_SCOPE_UNCHANGED=YES=
  target principal remains exact; runtime sources contain no IAM policy mutation
  API, project-level Token Creator grant, service-account key creation, or
  subprocess workaround
```

Targeted verification:

```text
pytest -q \
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py \
  tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py \
  tests/integrations/ghl/test_at1_commitment_key_provider.py
```

The repository's existing compile and hygiene checks will also run before
delivery.

## 7. IAM and identity invariants

```text
IAM_BINDINGS_ADDED=0
IAM_BINDINGS_REMOVED=0
IAM_BINDINGS_BROADENED=0
PROJECT_LEVEL_TOKEN_CREATOR_GRANTS=0
BABY_BUMPS_RUNTIME_B_TOKEN_CREATOR_GRANTS=0
FLEET_TOKEN_CREATOR_GRANTS=0
HUMAN_OPERATOR_TOKEN_CREATOR_GRANTS=0
SERVICE_ACCOUNT_KEYS_CREATED=0
TARGET_RUNTIME_PRINCIPAL_CHANGED=NO
```

## 8. Zero-effect ledger for this repair unit

```text
GENERATE_ACCESS_TOKEN_CALLS=0
TOKEN_MINT_ATTEMPTS=0
TOKEN_MINTS=0
ACCESS_SECRET_VERSION_CALLS=0
SECRET_PAYLOAD_READS=0
GHL_REST_CALLS=0
GHL_READ_ATTEMPTS=0
HTTP_REQUEST_DISPATCHES_TO_GHL=0
CRM_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
SERVICE_ACCOUNT_KEY_CREATES=0
DEPLOYMENTS=0
```

Repository fetch, local source edits, local fake-only tests, commit creation, and
pull-request creation are the only external/repository control-plane operations
permitted by this plan.

## 9. Implementation verification

```text
IMPLEMENTATION_STATUS=COMPLETE
EXPECTED_SOURCE_MATCH_PASS=YES
WRONG_SOURCE_FAIL_CLOSED=YES
MAX_PROVIDER_CREDENTIAL_ATTEMPTS=1
AUTOMATIC_RETRY_DISABLED=YES
SECRET_NON_DISCLOSURE=PASS
IAM_SCOPE_UNCHANGED=YES

EXPANDED_DETERMINISTIC_TESTS=326
EXPANDED_DETERMINISTIC_TESTS_RESULT=PASS
PYTHON_COMPILEALL=PASS
GIT_DIFF_CHECK=PASS

LIVE_CREDENTIAL_OBJECTS_LOADED=0
LIVE_CREDENTIAL_REFRESHES=0
LIVE_PROVIDER_OPERATIONS=0
EXTERNAL_MUTATIONS=0
```

The 326-test expanded suite covered the complete
`tests/integrations/ghl/highlevel_rest` directory and the commitment-key provider
tests. All credential, Secret Manager, and HTTP collaborators were synthetic or
injected fakes.

## 10. Readiness and stop

The bounded repair is implemented and locally verified. A future live execution
remains blocked pending independent review and merge of the repair, fresh
authorization, fresh activation, and provision of the explicit root-owned
workflow credential configuration.

```text
REPAIR_PLAN_READY=YES
REPAIR_IMPLEMENTATION_READY_FOR_REVIEW=YES
LIVE_EXECUTION_READY=NO
FRESH_LIVE_AUTHORIZATION_REQUIRED=YES
FRESH_LIVE_ACTIVATION_REQUIRED=YES
STOP=FOR_INDEPENDENT_IMPLEMENTATION_REVIEW
```
