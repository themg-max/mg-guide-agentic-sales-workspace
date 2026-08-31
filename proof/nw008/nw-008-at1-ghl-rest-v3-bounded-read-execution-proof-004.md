# NW-008 AT1 GHL REST v3 Bounded-Read Execution Proof 004

## 0. Proof identity and outcome class

```text
PROOF_ID=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_EXECUTION_PROOF_004
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-execution-proof-004.md
CLASSIFICATION=PROOF
PR_CLASS=proof_only
OUTCOME_CLASS=PRE_DISPATCH_STOP
OWNER=VS_CODE_MG_ORCHESTRATOR
EXECUTION_OPERATOR=HUMAN_EXECUTION_OPERATOR

RUN_ID=nw008-at1-ghl-rest-v3-read-004-20260831T001221Z-7d368093
PREFLIGHT_EVALUATED_AT_UTC=2026-08-31T00:26:41Z
```

The authorized HighLevel GET was **not executed**. Required immediate-execution
preflight predicates could not be satisfied in this environment, so per the
activation contract this unit stopped before any credential or provider
attempt. Authority was not consumed.

## 1. Authority chain (verified)

```text
AUTHORIZATION_004_PR=371
AUTHORIZATION_004_MERGE_SHA=
  6904905e4d52d9d2e32ce6c330681897040db6a3
ACTIVATION_004_PR=372
ACTIVATION_004_MERGE_SHA=
  c61d441226810ac5090a70eea7d24bdaf6c42eef
ACTIVATION_004_MERGE_SHA_ANCESTOR_OF_MAIN=YES

WINDOW_START_UTC=2026-08-31T00:12:21Z
WINDOW_END_UTC=2026-08-31T01:12:21Z
WINDOW_EXTENDABLE=NO
```

Ancestry was confirmed directly:
`git merge-base --is-ancestor c61d441226810ac5090a70eea7d24bdaf6c42eef origin/main`
returned 0. `origin/main` HEAD is `c61d441`.

## 2. Immediate execution preflight results

```text
WINDOW_OPEN=YES
AUTHORITY_CONSUMED=NO

RUNTIME_EXACT_V2_PIN=YES
SECRET_RESOURCE_DECLARED=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/2

PRIVATE_BINDING_BLOB_SHA_MATCH=NO
PRIVATE_ALLOWLIST_COMPLETE=NOT_EVALUATED
SECRET_VERSION_2_ENABLED=NOT_EVALUATED
CONTACT_TARGET_EXACT_PRIVATE_SYNTHETIC=NOT_EVALUATED
LOCATION_TARGET_EXACT_PRIVATE_CANONICAL=NOT_EVALUATED

PREFLIGHT_RESULT=FAIL
```

`RUNTIME_EXACT_V2_PIN=YES` was verified from repository source at
`origin/main` HEAD: all three designated active pins
(`live_note_runtime.py`, `live_note_credential_provider.py`,
`secret_access_diagnostic.py`) carry
`MG_GUIDE_PIT_GHL/versions/2`, with no `versions/1` or `versions/latest`
in active runtime source.

### 2.1 Private binding plane unavailable

```text
PRIVATE_BINDING_REPOSITORY=themg-max/A.I-Rolodex---Context
PRIVATE_BINDING_ATTACH_ATTEMPTED=YES
PRIVATE_BINDING_ATTACH_RESULT=DENIED
PRIVATE_BINDING_PRESENT_ON_DISK=NO
REQUIRED_PRIVATE_BINDING_BLOB_SHA=
  d76d70fd3a66af775e2520819bf6aff68c9566ae
OBSERVED_PUBLIC_ATTESTATION_BLOB_SHA=
  4f60f79b5c52d66b056d7bf455a5121d604d22b8
BLOB_SHA_MATCH=NO
```

The only same-named file reachable from this environment is
`proof/canonical-synthetic-read-binding-v1/synthetic-record-binding.yaml`
in this public repository. It is a **different artifact class** — a public
attestation *about* the private binding, not the binding itself. Its own
fields confirm this by design:

```text
exact_ids_public=NO
public_disclosure_of_exact_ids=False
private_allowlist.public_copy_present=False
contact_binding.public_id_disclosed=False
RAW_CONTACT_ID_FIELD_PRESENT=NO
```

It therefore carries no exact synthetic contact identifier and no exact
canonical location identifier. The bound GET path
`/contacts/{PRIVATE_ALLOWLIST_EXACT_SYNTHETIC_CONTACT}` **cannot be
constructed** in this environment. This is the private-plane boundary working
as designed, not a defect in the artifact.

### 2.2 Credential plane unavailable

```text
GCLOUD_CLI_PRESENT=NO
APPLICATION_DEFAULT_CREDENTIALS_RESOLVED=NO
NOTE_RUNTIME_SERVICE_ACCOUNT_ASSUMABLE=NO
REQUIRED_AUTHORIZATION_HEADER_CONSUMER=
  mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
SECRET_VERSION_2_STATE_VERIFIED=NO
```

`SECRET_VERSION_2_ENABLED` could not be evaluated: no Secret Manager access
path exists here as the designated consumer principal. Ambient session
credentials present in this environment belong to a different principal and
were **not** used — substituting a non-designated identity would violate the
credential-consumer boundary fixed by Authorization 004 §3.2. No attempt was
made to read `MG_GUIDE_PIT_GHL` under any identity, since a first credential
attempt would itself consume authority.

## 3. Terminal counters (no dispatch occurred)

```text
GHL_SECRET_VERSION_USED=NONE
SECRET_ACCESS_ATTEMPTS=0
NOTE_RUNTIME_IMPERSONATION_ATTEMPTS=0

GHL_REQUESTS=0
HTTP_REQUEST_DISPATCHES=0
NETWORK_CALL_COUNT=0

HTTP_STATUS=NOT_EVALUATED
HTTP_2XX=NOT_EVALUATED
CONTACT_ID_MATCH=NOT_EVALUATED
LOCATION_ID_MATCH=NOT_EVALUATED

NO_RETRY=YES
SECOND_GET_EXECUTED=NO
SEARCH_ATTEMPTS=0
LIST_ATTEMPTS=0
PAGINATION_ATTEMPTS=0
FALLBACK_USED=NO
ALTERNATE_TARGET_USED=NO
CRM_MUTATIONS=0
```

No connectivity probe was issued against
`https://services.leadconnectorhq.com` — a probe would draw down the
single-network-call ceiling, so the provider host was never contacted.

## 4. Authority state

```text
AUTHORITY_CONSUMED=NO
CONSUMPTION_STATE=PREPARED_UNCONSUMED
CONSUMPTION_TRIGGER_REACHED=NO
ACTIVATION_004_STILL_VALID_WITHIN_WINDOW=YES
WINDOW_END_UTC=2026-08-31T01:12:21Z
ACTIVATION_REUSABLE_AFTER_WINDOW=NO
```

Because no credential or provider attempt occurred, Activation 004 remains
unconsumed. A correctly provisioned execution operator may still consume it
for exactly one GET **before** `2026-08-31T01:12:21Z`. After that instant the
activation expires unused and is not extendable; a fresh Activation 005 bound
to Authorization 004 would be required.

## 5. Disclosure boundary

```text
TOKEN_VALUE_PUBLISHED=NO
TOKEN_HASH_PUBLISHED=NO
TOKEN_LENGTH_PUBLISHED=NO
TOKEN_PREFIX_PUBLISHED=NO
TOKEN_SUFFIX_PUBLISHED=NO
CONTACT_ID_PUBLISHED=NO
LOCATION_ID_PUBLISHED=NO
FULL_PROVIDER_RESPONSE_PUBLISHED=NO
PRIVATE_VALUES_DISCLOSED=NO
```

## 6. Terminal result

```text
PROVIDER_403_RESOLVED=NOT_EVALUATED
GHL_RUNTIME_V2_TRANSPORT=NOT_EVALUATED
NW008_AT1_GHL_IDENTITY_TRANSPORT_PATH=UNKNOWN
STOP=PRE_DISPATCH_PRIVATE_BINDING_AND_CREDENTIAL_PLANE_UNAVAILABLE
```

The v1→v2 rotation hypothesis remains **untested**. This proof records only
that the bounded read did not occur and why; it makes no claim about whether
the provider 403 is resolved.

## 7. Unblock requirements for a future execution attempt

An execution environment satisfying this activation must hold, at minimum:

1. Read access to the private control-plane binding at
   `themg-max/A.I-Rolodex---Context`, commit
   `855361fcab100d07196bc021af89f7375ed2b04a`, blob
   `d76d70fd3a66af775e2520819bf6aff68c9566ae`, so the exact synthetic contact
   and canonical location resolve.
2. Secret Manager access to
   `projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/2` **as** the
   designated consumer
   `mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com`.
3. Network egress to `https://services.leadconnectorhq.com`.
4. An open, unconsumed activation window at the moment of dispatch.

Items 1 and 2 are the binding blockers. Neither is repairable from inside this
public repository, and neither should be worked around by substituting a
different identity or a public stand-in for the private binding.
