# NW-008 AT8W30 R3 GET-Contact Execution Proof 003

```text
UNIT=NW008_AT8W30_R3_GET_CONTACT_EXECUTION_002
PR_CLASS=execution_proof
ACTION=ONE_SHOT_GOVERNED_EXECUTION

RESULT=FAIL_CLOSED
STOP_CODE=R3_MERGED_PUBLIC_LEASE_INGRESS_TARGET_SHAPE_GATE_BLOCKS_APPROVED_LIVE_TARGET

CONSUMPTION_TRIGGER_REACHED=NO
R3_AUTHORIZATION_STATE=AVAILABLE_UNCONSUMED
R3_AUTHORIZATION_CONSUMED=NO
R3_EXECUTION_ATTEMPTS_USED=0
R3_EXECUTION_PERFORMED=NO

HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
GET_CONTACT_ATTEMPTS=0
```

The designated unit stopped **strictly before** the authorization consumption
trigger. The PR223 one-shot grant was **not** consumed and remains available for
a future authorized attempt.

Private locator values, private identifiers, credentials, tokens, and secret
payloads are intentionally absent from this artifact.

---

## 1. Authorization identity

```text
AUTHORIZATION_ID=
  nw008-at8w30-r3-get-contact-execution-authorization-002
AUTHORIZATION_PR=223
AUTHORIZATION_ARTIFACT=
  governance/authorizations/nw008-at8w30-r3-get-contact-execution-authorization-002.md

DESIGNATED_UNIT=
  NW008_AT8W30_R3_GET_CONTACT_EXECUTION_002
DESIGNATED_RUN_ID=
  nw008-at8w30-r3-get-contact-execution-run-002
DESIGNATED_RUN_ID_STATE=RESERVED_UNUSED
DESIGNATED_RUN_ID_CHANGED_DURING_UNIT=NO

AUTHORIZATION_CONSUMPTION_TRIGGER=
  FIRST_TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTION_ATTEMPT_FOR_R3

RECORDED_AT_UTC=2026-08-26T23:36:33Z
RECORDED_AT_LOCAL=2026-08-26T19:36:33-0400
```

The reserved run identity was never bound to any private reference, because no
private reference was materialized for the live target.

---

## 2. Preflight

```text
EXECUTION_BRANCH=
  exec/nw008-at8w30-r3-get-contact-execution-003
EXECUTION_BASE_SHA=
  0e79dc345a2c8fab0dfd37ee6383990f50fb0d84

BRANCH_IS_MAIN=NO
WORKTREE_CLEAN_AT_START=YES
UNEXPECTED_WORKTREE_CHANGES=NO
ORIGIN_MAIN_FETCHED=YES
```

---

## 3. Governance gate reconciliation

```text
PR223_STATE=MERGED
PR227_STATE=MERGED
PR228_STATE=MERGED

PR228_MERGE_COMMIT=
  0e79dc345a2c8fab0dfd37ee6383990f50fb0d84
PR228_MERGE_COMMIT_IN_ORIGIN_MAIN_LINEAGE=YES

START_GATE_ACCEPTANCE_ARTIFACT_ON_ORIGIN_MAIN=YES
R3_EXECUTION_START_GATE_ACCEPTED=YES
DESIGNATED_UNIT_RELEASE_READY=YES

DESIGNATED_UNIT_MATCHES=YES
DESIGNATED_RUN_ID_MATCHES=YES

PRIOR_R3_CONSUMPTION_RECORD_PRESENT=NO
```

Prior proof `nw008-at8w30-r3-get-contact-execution-proof-002.md` (PR224) recorded
`AUTHORIZATION_CONSUMED=NO`. No durable consumption record for this grant exists
on `origin/main`. The grant was live and unconsumed at unit start.

---

## 4. Bound runtime integrity

```text
BOUND_PR217_MERGE_COMMIT=
  987b9b6646a3090666bd328c6c13eea89556a679
PR217_MERGE_COMMIT_IN_ORIGIN_MAIN_LINEAGE=YES

note_path.py_MATCHES_ORIGIN_MAIN=YES
live_note_runtime.py_MATCHES_ORIGIN_MAIN=YES

PUBLIC_RUNTIME_MODIFIED=NO
PUBLIC_TESTS_MODIFIED=NO
PUBLIC_DEPENDENCY_MANIFEST_MODIFIED=NO
```

All findings below were observed against the **bound, merged, unmodified** public
runtime.

---

## 5. Non-consuming readiness results

All checks were performed without constructing a target-runtime credential,
resolving ADC for R3, impersonating a service account, minting a token, reading a
secret payload, opening SQLite, assembling the production runtime, or dispatching
HTTP.

### 5.1 Resolved since prior attempt

```text
PRIVATE_OWNER_SOURCE_LOCALLY_RESOLVABLE=YES
PRIVATE_OWNER_IMPLEMENTATION_LOADABLE=YES
PRIVATE_OWNER_DESIGNATION_MATCH=YES
PRIVATE_OWNER_ENTRYPOINT_CALLABLE=YES
PRIVATE_OWNER_RUNS_IN_SAME_PROCESS_AS_PUBLIC_CONSUMER=YES
PRIVATE_OWNER_EXECUTION_SURFACE_READY=YES

PUBLIC_RUNTIME_COLOADABLE_IN_SAME_PROCESS=YES

ROOT_OWNED_EXECUTION_STORE_CONFIGURATION_PRESENT=YES
CONFIGURED_EXISTING_STORE_TARGET_EXISTS=YES
SQLITE_CREATE_REQUIRED=NO

REQUIRED_RUNTIME_DEPENDENCIES_IMPORTABLE=YES
```

Prior readiness failure A (`REQUIRED_PYTHON_DEPENDENCIES_IMPORTABLE=NO`) was
remediated pre-trigger by provisioning a host-local, gitignored interpreter
containing only the **already-declared** manifest dependency
`google-cloud-secret-manager==2.27.0`. No public dependency manifest was changed
and no public runtime source was modified.

```text
DEPENDENCY_REMEDIATION_CLASS=
  HOST_LOCAL_GITIGNORED_INTERPRETER_RESTORE_OF_ALREADY_DECLARED_MANIFEST_DEPENDENCY
PUBLIC_MANIFEST_CHANGED=NO
NEW_DEPENDENCY_INTRODUCED=NO
```

### 5.2 Operative blocker — merged public lease ingress rejects the approved live target

This is the decisive, structural, **pre-consumption** blocker. It is the same
class as prior readiness failure B (`MERGED_INGRESS_TARGET_SHAPE_GATE`), and it
is **not** resolved by the merged private provisioning stage.

```text
FAILED_CHECK=
  APPROVED_LIVE_TARGET_CAN_CROSS_MERGED_PUBLIC_PRIVATE_OWNER_LEASE_INGRESS
FAILURE_CLASS=MERGED_INGRESS_TARGET_SHAPE_GATE
FAILURE_SURFACE=BOUND_MERGED_PUBLIC_RUNTIME
```

Observed, in-memory, zero-effect evidence:

```text
PUBLIC_INGRESS_ACCEPTS_SYNTHETIC_TARGET=YES
PUBLIC_INGRESS_ACCEPTS_NON_SYNTHETIC_TARGET=NO
PUBLIC_INGRESS_REJECTION_CLASS=
  BindingError:private_AT8_handoff_source_value_must_be_synthetic

ONLY_PUBLIC_HANDOFF_SOURCE_ISSUER_IS_SYNTHETIC_ONLY=YES
PRIVATE_OWNER_REFERENCE_TYPE_IS_PUBLIC_LEASE_TYPE=NO
PUBLIC_LEASE_REGISTRY_RECOGNIZES_FOREIGN_REFERENCE=NO
```

Structural reading of the bound merged runtime:

1. `assemble_bound_live_note_runtime` accepts only an opaque reference that is
   registered in the **public** process-local lease registry.
2. Registration in that registry requires a trusted binding source whose trusted
   origin is the private-AT8-handoff origin.
3. In the bound merged runtime, the only issuer of that trusted origin is the
   **synthetic-only** issuer, which hard-rejects any location/contact identifier
   that is not `synthetic-` shaped.
4. The designated private owner materializes an opaque reference of its **own**
   private type, which the public lease registry does not and cannot recognize.

Therefore the approved **live** R3 target cannot reach
`GET /contacts/{private_binding.contact_id}` through the bound merged runtime.

### 5.3 Why no bridge was improvised

```text
PUBLIC_RUNTIME_MUTATED_TO_FORCE_READINESS=NO
PUBLIC_PRODUCTION_LEASE_MATERIALIZATION_PERFORMED=NO
PUBLIC_RAW_ID_AUTHORITY_MINTING_PERFORMED=NO
SYNTHETIC_SHAPED_SUBSTITUTE_FOR_LIVE_TARGET_USED=NO
ALTERNATE_OPERATION_OR_TRANSPORT_USED=NO
SECOND_R3_GRANT_CREATED=NO
```

PR223 explicitly marks `PUBLIC_PRODUCTION_LEASE_MATERIALIZATION` and
`PUBLIC_RAW_ID_AUTHORITY_MINTING` as **FORBIDDEN**. Every available route around
the ingress gate would have required one of those forbidden acts, a mutation of
the bound merged public runtime, or substituting a synthetic identifier for the
approved live target. None is authorized by this unit, so the unit stopped.

---

## 6. Authorization preservation

The unit halted **before** the trigger, so the irreversible transition never
occurred.

```text
STOPPED_BEFORE=
  FIRST_TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTION_ATTEMPT_FOR_R3

CONSUMPTION_TRIGGER_REACHED=NO
R3_AUTHORIZATION_STATE=AVAILABLE_UNCONSUMED
R3_AUTHORIZATION_CONSUMED=NO
R3_EXECUTION_ATTEMPTS_USED=0
R3_EXECUTION_PERFORMED=NO
DESIGNATED_RUN_ID_STATE=RESERVED_UNUSED

PRIVATE_OWNER_PROVENANCE_ESTABLISHED=NO
OPAQUE_PRIVATE_REFERENCE_MATERIALIZED=NO
PRIVATE_OWNER_LOCATOR_PUBLISHED=NO
```

Because the grant was never consumed, this outcome is **not** a spent attempt.
The one-shot authority is intact and still requires human governance to direct
its use.

---

## 7. Effect budget (actual)

```text
TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS=0
APPLICATION_DEFAULT_CREDENTIAL_RESOLUTIONS=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
SECRET_MANAGER_CLIENT_INSTANTIATIONS=0
SECRET_PAYLOAD_READS=0
TOKEN_MINTS=0
SQLITE_CREATES=0
SQLITE_EXISTING_OPENS=0
SQLITE_OPENS=0
PRODUCTION_RUNTIME_ASSEMBLIES=0

HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
GET_CONTACT_ATTEMPTS=0
GET_OPPORTUNITY_ATTEMPTS=0
SEARCH_CALLS=0
LIST_CALLS=0
PAGINATION_CALLS=0
RETRY_COUNT=0

NOTE_WRITES=0
STAGE_WRITES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

R4_PERFORMED=NO
```

Allowed result fields were never obtained, because no request was dispatched:

```text
CONTACT_ID_FIELD_RETURNED=NO
CONTACT_LOCATION_ID_FIELD_RETURNED=NO
```

---

## 8. Sanitization

```text
RAW_PRIVATE_BINDING_PUBLISHED=NO
PRIVATE_OWNER_LOCATOR_PUBLISHED=NO
PRIVATE_OWNER_IMPLEMENTATION_PATH_PUBLISHED=NO
PRIVATE_IDENTIFIER_PUBLISHED=NO
CREDENTIALS_PUBLISHED=NO
SECRET_PAYLOADS_PUBLISHED=NO
BEARER_OR_ACCESS_TOKENS_PUBLISHED=NO
FULL_PROVIDER_RESPONSE_PUBLISHED=NO
UNRELATED_CONTACT_FIELDS_PUBLISHED=NO
```

The placeholder identifiers used in the ingress shape probe were non-private
literals authored for the probe. No approved live target value appears here.

---

## 9. Disposition

```text
RESULT=FAIL_CLOSED
STOP_CODE=R3_MERGED_PUBLIC_LEASE_INGRESS_TARGET_SHAPE_GATE_BLOCKS_APPROVED_LIVE_TARGET

R3_RETRY_AUTHORIZED=NO
R3_SECOND_EXECUTION_AUTHORIZED=NO
R4_AUTHORIZED=NO
R4_PERFORMED=NO

RETRY_PERFORMED=NO
NEW_GRANT_CREATED=NO
FALLBACK_OPERATION_PERFORMED=NO

NEXT_ACTION=
  INDEPENDENT_HUMAN_GOVERNANCE_REVIEW_ONLY
```

The remaining blocker is a property of the **bound merged public runtime**, not of
the private owner surface. Resolving it requires a separate, human-authorized
change to the public private-owner lease ingress so that an approved live target
can cross it without public raw-ID authority minting. That change is **not**
authorized by PR223 and was not attempted.

This unit performed no live execution and stops here for independent review.
