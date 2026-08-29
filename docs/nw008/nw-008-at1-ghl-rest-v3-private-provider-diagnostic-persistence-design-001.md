# NW-008 AT-1 — GHL REST v3 Private Provider Diagnostic Persistence Design 001

## 0. Identity and implementation boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PRIVATE_PROVIDER_DIAGNOSTIC_PERSISTENCE_DESIGN_001
ARTIFACT_PATH=
  docs/nw008/nw-008-at1-ghl-rest-v3-private-provider-diagnostic-persistence-design-001.md
ACTION=IMPLEMENT_PRIVATE_PROVIDER_DIAGNOSTIC_PERSISTENCE
OWNER=VS_CODE_ORCHESTRATOR
MODE=OFFLINE_IMPLEMENTATION_AND_TEST

PRIVATE_PROVIDER_DIAGNOSTIC_PERSISTENCE_DESIGNED=YES
PRIVATE_PROVIDER_DIAGNOSTIC_PERSISTENCE_IMPLEMENTED=YES
PRIVATE_DIAGNOSTIC_IMPLEMENTATION_READY_FOR_PR=YES
NO_PROVIDER_PARSING_REDESIGN=YES
```

This unit closes the persistence design gap without making a HighLevel call.
It reuses `PrivateProviderErrorEvidence`,
`derive_private_provider_error_evidence(...)`, and
`project_public_provider_error_evidence(...)`.

## 1. Required execution order

The definitive non-2xx path is:

```text
NON_2XX_RESPONSE
  -> DERIVE_PRIVATE_EVIDENCE
  -> ATOMIC_PRIVATE_PERSISTENCE
  -> VERIFY_PRIVATE_PERSISTENCE
  -> PUBLIC_SAFE_PROJECTION
  -> STOP
```

The binding-validation evaluator now fails closed before public provider-detail
projection when no private persistence context is supplied or persistence
cannot be verified. Projection is reached only after a verified receipt.

```text
PRIVATE_EVIDENCE_COLLECTION_CLASSIFICATION=FACT_COLLECTION_ONLY
PROVIDER_ERROR_CAUSE_RUNTIME_INFERENCE=FORBIDDEN
POST_RUN_OFFLINE_CAUSE_CLASSIFICATION=REQUIRED_WHEN_NON_2XX
```

Runtime collection preserves the evidence-derived cause value, currently
`UNKNOWN`, without interpreting the message or code. Any narrower cause
classification is a separate offline post-run activity over the persisted
private record.

## 2. Implementation surfaces

| Surface | Responsibility |
| --- | --- |
| `src/integrations/ghl/highlevel_rest/private_provider_diagnostic_persistence.py` | Transport-neutral persistence protocol, diagnostic context, receipt, and shared failure contract |
| `src/mg_guide/evidence/private_provider_diagnostic_persistence.py` | Whitelisted record construction, gitignore enforcement, create-only atomic write, mode and content verification |
| `src/integrations/ghl/highlevel_rest/pit_subaccount_binding_validation.py` | Required non-2xx ordering and fail-closed persistence markers |
| `tests/integrations/ghl/highlevel_rest/test_private_provider_diagnostic_persistence.py` | Store security, atomicity, overwrite, and whitelist tests |
| `tests/integrations/ghl/highlevel_rest/test_pit_subaccount_binding_validation.py` | Ordering, projection, and one-call failure semantics |

No HTTP client, provider-envelope parser, or public projection parser was
replaced.

## 3. Private record schema

The create-only JSON record contains exactly:

```text
SCHEMA_VERSION
RECORDED_AT_UTC
GRANT_ID
RUN_ID
OPERATION_ID

PROVIDER_HTTP_STATUS
CONTENT_TYPE_CLASS
RESPONSE_BODY_LENGTH
RESPONSE_BODY_SHA256

PROVIDER_ERROR_ENVELOPE_PARSEABLE
PROVIDER_ERROR_CODE
PROVIDER_ERROR_MESSAGE
PROVIDER_REQUEST_ID
PROVIDER_CORRELATION_ID
PROVIDER_ERROR_CLASS
PROVIDER_ERROR_CAUSE
```

`SCHEMA_VERSION=nw008_private_provider_diagnostic_v1`. The raw provider body
is represented only by byte length and SHA-256.

Diagnostic identity is the complete tuple:

```text
DIAGNOSTIC_IDENTITY=GRANT_ID+RUN_ID+OPERATION_ID
DIAGNOSTIC_IDENTITY_UNIQUE=YES
```

All three identity values are validated as safe non-empty identifiers and are
included in the create-only filename. A repeated tuple collides with the
existing destination and fails closed; a different grant, run, or operation
produces a different destination.

## 4. Storage and privacy contract

```text
GITIGNORED=YES
CREATE_ONLY=YES
OVERWRITE_ALLOWED=NO
FILE_MODE=0600
ATOMIC_WRITE=YES
PERSISTENCE_READBACK_VERIFICATION=YES
```

Before writing, the store uses `git check-ignore` against the exact destination.
It writes a same-directory mode-0600 temporary file with exclusive creation,
flushes and fsyncs it, then atomically publishes it with a create-only hard
link. An existing destination is never replaced. Verification reads the final
file back and checks regular-file type, non-symlink status, exact mode, exact
bytes, and decoded payload equality.

The persistence layer has an explicit field whitelist and never serializes:

```text
PIT
AUTHORIZATION_REQUEST_HEADER
ADC_TOKEN
COOKIES
RAW_PRIVATE_CRM_IDS
RAW_PROVIDER_BODY
```

Credential-bearing response headers are already excluded by the reused
evidence derivation. Callers must also supply bound tokens and raw private CRM
identifiers as sensitive values. If any supplied value appears in a persisted
field, the write is rejected before file creation.

## 5. Persistence-failure semantics

```text
PRIVATE_DIAGNOSTIC_PERSISTED=NO
DIAGNOSTIC_PERSISTENCE_VERIFIED=NO
DIAGNOSTIC_PERSISTENCE_FAILURE=YES
RETRY_PERFORMED=NO
SECOND_PROVIDER_CALL=NO
PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=UNKNOWN
```

Persistence failure does not retry, project private details, or create another
provider-call opportunity. The consumed one-read budget remains consumed.

## 6. Offline test proof

Targeted tests cover:

- exact persisted-field whitelist and body hash;
- gitignored destination enforcement;
- create-only overwrite denial and original-byte preservation;
- full grant/run/operation identity uniqueness;
- file mode `0600`;
- same-directory atomic publication and temporary-file cleanup;
- absence of authorization, cookie, token, raw body, and raw CRM ID values;
- required bound credential/private-identifier inventory;
- sensitive-value rejection before write;
- persistence before public-safe projection;
- no projection on persistence failure; and
- one read, zero writes, no retry, and no second provider call.

```text
OFFLINE_TEST_COMMAND=
  ./.venv-test/bin/python -m pytest
  tests/integrations/ghl/highlevel_rest/test_private_provider_diagnostic_persistence.py
  tests/integrations/ghl/highlevel_rest/test_pit_subaccount_binding_validation.py
  tests/integrations/ghl/highlevel_rest/test_provider_error_evidence.py

OFFLINE_TEST_RESULT=PASS
OFFLINE_TESTS_PASSED=35
OFFLINE_TESTS_FAILED=0

LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0
```

## 7. Implementation pull-request scope

The implementation PR is intentionally limited to:

```text
src/integrations/ghl/highlevel_rest/private_provider_diagnostic_persistence.py
src/integrations/ghl/highlevel_rest/pit_subaccount_binding_validation.py
src/integrations/ghl/highlevel_rest/__init__.py
src/mg_guide/evidence/__init__.py
src/mg_guide/evidence/private_provider_diagnostic_persistence.py
tests/integrations/ghl/highlevel_rest/test_private_provider_diagnostic_persistence.py
tests/integrations/ghl/highlevel_rest/test_pit_subaccount_binding_validation.py
docs/nw008/nw-008-at1-ghl-rest-v3-private-provider-diagnostic-persistence-design-001.md
```

```text
PROVIDER_EXECUTION_AUTHORIZED_BY_IMPLEMENTATION_PR=NO
NEW_GHL_GRANT_AUTHORIZED_BY_IMPLEMENTATION_PR=NO
```

## 8. Future diagnostic-call proposal

This implementation does not authorize a diagnostic call or grant. A future,
separately reviewed proposal may be bounded as follows:

```text
METHOD=GET
PATH=/opportunities/{private_validation_opportunity_id}

MAX_READS=1
MAX_WRITES=0
MAX_TOTAL_BUSINESS_CALLS=1

NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_ALTERNATE_TARGET=YES
NO_ALTERNATE_CREDENTIAL=YES

AUTHORITY_CLASS=DIAGNOSTIC_ONLY
IS_STAGE_GRANT_003=NO
FUTURE_DIAGNOSTIC_CALL_AUTHORIZED=NO
PRIVATE_DIAGNOSTIC_PERSISTENCE_REQUIRED=YES
MUST_PRECEDE_STAGE_GRANT_003=YES
```

## 9. Stop

```text
NO_HIGHLEVEL_CALL=YES
NO_GRANT_CREATION=YES
NO_IAM_MUTATION=YES
NO_AGENTS_CLI_DEPLOY=YES
NO_SECRET_MUTATION=YES
NO_PIT_ROTATION=YES
NO_GHL_SCOPE_EDIT=YES

PRIVATE_PROVIDER_DIAGNOSTIC_PERSISTENCE_DESIGNED=YES
PRIVATE_DIAGNOSTIC_IMPLEMENTATION_READY_FOR_PR=YES
LIVE_GHL_CALLS=0
IAM_MUTATIONS=0
AGENT_RUNTIME_DEPLOYMENTS=0

STOP
```
