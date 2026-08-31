# NW-008 AT1 GHL REST v3 Bounded-Read 004 Proof Normalization 001

## 0. Identity and hard boundary

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_004_PROOF_NORMALIZATION_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-004-proof-normalization-001.md
CLASSIFICATION=PROOF_SEMANTICS_NORMALIZATION
PR_CLASS=proof_only
MODE=READ_ONLY_NORMALIZATION_NO_PROVIDER_CALL
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T01:08:00Z

BRANCH_AT_AUTHORING=
  docs/nw008-ghl-403-close-and-agent-runtime-principal-binding-001
BRANCH_IS_MAIN=NO

CANONICAL_EXECUTION_PROOF_ID=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_EXECUTION_PROOF_004
CANONICAL_EXECUTION_PROOF_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-execution-proof-004.md
CANONICAL_EXECUTION_PROOF_PR=374
CANONICAL_EXECUTION_PROOF_MERGE_SHA=
  735468670e24a736723ef9b737ceee3f3f93eee1
CANONICAL_EXECUTION_PROOF_PRESENT_ON_ORIGIN_MAIN=YES
CANONICAL_EXECUTION_PROOF_EDITED_BY_THIS_UNIT=NO
```

This unit **does not** change the terminal success conclusion of proof 004. It
closes the GHL 403 remediation lane as a durable governance state and normalizes
two semantic fields that were easy to over-read from the public ledger:
ephemeral secret handling, and what `NETWORK_CALL_COUNT=1` counted.

```text
GHL_CALLS_IN_THIS_UNIT=0
CRM_MUTATIONS_IN_THIS_UNIT=0
SECRET_PAYLOAD_READS_IN_THIS_UNIT=0
IAM_MUTATIONS_IN_THIS_UNIT=0
NO_RETRY_OF_BOUNDED_READ_004=YES
```

## 1. Authority chain retained

```text
AUTHORIZATION_004_PR=371
AUTHORIZATION_004_MERGE_SHA=
  6904905e4d52d9d2e32ce6c330681897040db6a3
ACTIVATION_004_PR=372
ACTIVATION_004_MERGE_SHA=
  c61d441226810ac5090a70eea7d24bdaf6c42eef
RUN_ID=
  nw008-at1-ghl-rest-v3-read-004-20260831T001221Z-7d368093
AUTHORITY_004_CONSUMED_TERMINAL=YES
AUTHORITY_004_REUSABLE=NO
FRESH_AUTHORIZATION_REQUIRED_FOR_ANY_FURTHER_GHL_CALL=YES
```

## 2. GHL 403 lane — CLOSED

```text
NW008_GHL_403_BLOCKER=CLOSED
PROVIDER_403_RESOLVED=YES
GHL_SECRET_VERSION_USED=2
HTTP_STATUS=200
HTTP_2XX=YES
CONTACT_ID_MATCH=YES
LOCATION_ID_MATCH=YES
GHL_PROVIDER_REQUESTS=1
GHL_PROVIDER_NETWORK_CALL_COUNT=1
CRM_MUTATIONS=0
GHL_RUNTIME_V2_TRANSPORT=PASS
NW008_AT1_GHL_IDENTITY_TRANSPORT_PATH=HEALTHY
STOP_FROM_PROOF_004=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_004_COMPLETE
```

The proof-003 provider 403 under `MG_GUIDE_PIT_GHL/versions/1` does not
reproduce under version 2. The PIT rotation plus the runtime exact-v2 pin
restored the identity/transport path. This normalization **closes** the GHL 403
remediation lane. No further GHL call is authorized by this unit or by the
consumed Activation 004 authority.

```text
GHL_403_REMEDIATION_LANE_STATUS=CLOSED
GHL_403_FURTHER_DIAGNOSTIC_CALLS_AUTHORIZED=NO
GHL_403_FURTHER_BOUNDED_READ_REUSE_AUTHORIZED=NO
```

## 3. PR #373 disposition

```text
PR_373_TITLE=
  proof(nw008): record bounded-read 004 pre-dispatch stop
PR_373_STATE=CLOSED
PR_373_MERGED=NO
PR_373_SUPERSEDED=YES
PR_373_SUPERSEDED_BY=PR_374
PR_373_CLASS=PRE_DISPATCH_STOP_NON_CONSUMING
PR_373_SECRET_ACCESS_ATTEMPTS=0
PR_373_GHL_REQUESTS=0
PR_373_AUTHORITY_CONSUMED=NO
```

PR #373 correctly recorded a non-consuming pre-dispatch stop from an
unprovisioned environment. It is superseded by the actual-execution proof on
PR #374 and must not be treated as a competing terminal outcome for Activation
004.

## 4. Terminal success conclusion — UNCHANGED

```text
EXECUTION_RESULT=TERMINAL_SUCCESS
HTTP_STATUS=200
HTTP_2XX=YES
CONTACT_ID_MATCH=YES
LOCATION_ID_MATCH=YES
GHL_SECRET_VERSION_USED=2
PROVIDER_403_RESOLVED=YES
NW008_AT1_GHL_IDENTITY_TRANSPORT_PATH=HEALTHY
TERMINAL_SUCCESS_CONCLUSION_CHANGED_BY_THIS_UNIT=NO
```

## 5. Ephemeral secret-handling semantics (normalized)

Proof 004 correctly recorded that no token value was published, logged, hashed,
prefixed, suffixed, length-recorded, or durably persisted. The operator
execution path nevertheless held the secret payload briefly in process memory
and, for the single curl dispatch, wrote it into an ephemeral local config file
under a restrictive umask. That fact is recorded here so later reviewers do not
equate "not published" with "never touched a filesystem buffer."

```text
SECRET_VALUE_TEMPORARILY_HELD_IN_PROCESS_MEMORY=YES
SECRET_VALUE_TEMPORARILY_WRITTEN_TO_EPHEMERAL_FILE=YES
TEMP_SECRET_FILE_PURPOSE=CURL_CONFIG_AUTHORIZATION_HEADER_ONLY
TEMP_SECRET_FILE_ACCESS_BOUNDARY=UMASK_077
TEMP_SECRET_FILE_DESTROYED_AFTER_EXECUTION=YES
PRIVATE_TEMP_MATERIAL_DESTROYED=YES

SECRET_VALUE_PERSISTED_DURABLY=NO
SECRET_VALUE_COMMITTED=NO
SECRET_VALUE_LOGGED=NO
SECRET_VALUE_ECHOED=NO
TOKEN_VALUE_PUBLISHED=NO
PIT_VALUE_HASH_RECORDED=NO
PIT_VALUE_LENGTH_RECORDED=NO
PIT_VALUE_PREFIX_RECORDED=NO
PIT_VALUE_SUFFIX_RECORDED=NO
FULL_PROVIDER_RESPONSE_PUBLISHED=NO
CONTACT_ID_PUBLISHED=NO
LOCATION_ID_PUBLISHED=NO
```

Normalization rule for future proofs:

```text
RULE=
  Distinguish (a) durable publication / commit / log of secret material from
  (b) ephemeral process-local or umask-restricted temp-file use destroyed before
  proof authoring. (a) remains FORBIDDEN. (b), when unavoidable for a governed
  one-shot transport, must be stated explicitly and destroyed before return.
```

## 6. Network-accounting semantics (normalized)

Proof 004's ledger field `NETWORK_CALL_COUNT=1` is retained and is interpreted
as the **GHL provider network call count** for the authorized effect:

```text
GHL_PROVIDER_NETWORK_CALL_COUNT=1
GHL_REQUESTS=1
HTTP_REQUEST_DISPATCHES=1
GHL_REST_CALLS=1
GHL_READ_ATTEMPTS=1
REDIRECTS_FOLLOWED=0
SEARCH_ATTEMPTS=0
LIST_ATTEMPTS=0
PAGINATION_ATTEMPTS=0
RETRY_ATTEMPTS=0
FALLBACK_USED=NO
SECOND_GET_EXECUTED=NO
```

That count does **not** mean the operator workstation performed zero other
network I/O. Before consumption, the unit performed control-plane / metadata
reads that are out of scope for the provider-effect ceiling:

```text
CONTROL_PLANE_READ_NETWORK_CALLS=
  PRESENT_BEFORE_EXECUTION
CONTROL_PLANE_READ_CLASSES_OBSERVED=
  - private binding blob fetch (GitHub private repo API, read-only)
  - Secret Manager versions describe (state/metadata only; no payload)
  - IAM policy metadata reads (note-runtime SA / secret accessor)
  - IAM testIamPermissions (no access-token mint)
CONTROL_PLANE_READ_EXACT_COUNT=
  NOT_DETERMINISTICALLY_RECONSTRUCTED
CONTROL_PLANE_READ_EXACT_COUNT_FABRICATED=NO
```

An exact control-plane count is **not** fabricated. The durable claim is only
that control-plane reads were present before execution, while the single
authorized HighLevel effect remained one GET.

```text
NETWORK_ACCOUNTING_RULE=
  Prefer GHL_PROVIDER_NETWORK_CALL_COUNT (or equivalently scoped provider
  counters) for the authorized CRM/provider effect. Do not overload a bare
  NETWORK_CALL_COUNT to imply zero control-plane I/O unless the unit truly
  performed none and can prove it.
```

## 7. Lane separation after close

```text
GHL_403_LANE=CLOSED
AGENT_RUNTIME_IAM_LANE=SEPARATE
AGENT_RUNTIME_PRINCIPAL_BINDING_LANE=SEPARATE
VERTEX_IAM_MUTATION_AUTHORIZED_BY_THIS_UNIT=NO
AGENT_RUNTIME_DEPLOYMENT_AUTHORIZED_BY_THIS_UNIT=NO
LIVE_GHL_ADAPTER_ENABLED=NO
```

Closing the GHL 403 lane does not grant Vertex IAM, select an Agent Runtime
deployment identity for local ADC, rotate Gemini keys, or authorize live CRM
mutations. Those remain separate governance subjects.

## 8. Security gate (unchanged, still pending human)

```text
EXPOSED_GEMINI_API_KEY_ROTATED_OR_REVOKED=
  PENDING_HUMAN_ATTESTATION
DEPLOYMENT_ALLOWED_BEFORE_SECURITY_GATE=NO
KEY_VALUE_OR_HASH_OR_PREFIX_OR_SUFFIX_IN_THIS_ARTIFACT=NO
```

## 9. Stop

```text
NW008_GHL_403_BLOCKER=CLOSED
PROVIDER_403_RESOLVED=YES
AUTHORITY_004_CONSUMED_TERMINAL=YES
TERMINAL_SUCCESS_CONCLUSION_CHANGED=NO
GHL_CALLS_IN_THIS_UNIT=0
NEXT=
  DO_NOT_PERFORM_ANOTHER_GHL_CALL
  PROCEED_ONLY_ON_SEPARATE_AGENT_RUNTIME_PRINCIPAL_BINDING_AND_LATER_IAM_GATES
STOP=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_004_PROOF_NORMALIZATION_001_COMPLETE
```
