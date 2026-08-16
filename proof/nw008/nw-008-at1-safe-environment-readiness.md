# NW-008 — AT-1 Safe Environment Readiness

## Scope and lane

```text
WORK_ITEM=NW-008
TRACK=AT-1
LANE=SAFE_ENVIRONMENT_READINESS
BRANCH=impl/nw008-at1-safe-environment-readiness
IMPLEMENTATION_SUBJECT_SHA=8c18a10faff28b658638da9e0d9752c8710e0e23
IMPLEMENTATION_HARDENING_SHA=998564cdfac6c24d5a414289798979a7f6220082
TRACK_B_FINAL_REVIEW_HEAD=835d86f64bd75b4983cf5e92f25b5fc7da439cc0
```

This lane separates two independent readiness surfaces:

1. **Deterministic executor readiness (Track B / fixture-backed)** — verified in-repo.
2. **External GHL environment readiness (live isolated test location)** — not yet verified.

Fixture isolation alone does **not** prove an actual GHL test location, live synthetic
CRM records, live credential scope, or live MCP operation availability. This lane does
not grant execution authority and does not perform AT-1 mutation or live GHL calls.

## Required evidence (truth table)

```text
# Deterministic / policy (VERIFIED in-repo)
DETERMINISTIC_EXECUTOR_READY=YES
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO

# External GHL environment (PENDING — requires separate read-only verification)
ISOLATED_GHL_TEST_LOCATION=PENDING
SYNTHETIC_CONTACT_READY=PENDING
SYNTHETIC_OPPORTUNITY_READY=PENDING
EXPECTED_INITIAL_STAGE_VERIFIED=PENDING
AUTHORIZED_FINAL_STAGE_VERIFIED=PENDING
REQUIRED_GHL_OPERATIONS_VERIFIED=PENDING
GHL_TARGET_SCOPE_VERIFIED=PENDING

# Aggregate readiness
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

## VERIFIED — Deterministic executor and Track B contract

The following are verified from Track B implementation/hardening and deterministic
synthetic fixture isolation. They do not substitute for external environment proof.

### Track B SHAs (preserved)

```text
IMPLEMENTATION_SUBJECT_SHA=8c18a10faff28b658638da9e0d9752c8710e0e23
IMPLEMENTATION_HARDENING_SHA=998564cdfac6c24d5a414289798979a7f6220082
TRACK_B_FINAL_REVIEW_HEAD=835d86f64bd75b4983cf5e92f25b5fc7da439cc0
DETERMINISTIC_EXECUTOR_READY=YES
```

### Deterministic synthetic fixture isolation (in-repo only)

Public-repo fixtures use synthetic placeholders only. This proves the **executor
fixture surface** is isolated from production CRM, Firestore, and network-backed
runtime **inside the deterministic harness**. It does **not** prove a live isolated
GHL test location exists or is bound.

```text
location_id=synthetic-location-at1
contact_id=synthetic-contact-at1
opportunity_id=synthetic-opportunity-at1
expected_initial_stage_id=synthetic-stage-initial
authorized_final_stage_id=synthetic-stage-final
```

Fixture policy (deterministic harness):

```text
source=synthetic_only
network_enabled=false
ghl_live_client=false
firestore_client=false
```

### Exact six-operation executor contract

The allowed GHL operation set remains identical to Track B:

```text
ORDER=get-contact,get-opportunity,create-note,get-note,update-opportunity,get-opportunity
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RAW_REST=YES
NO_ALTERNATE_OPERATION=YES
```

This verifies the **executor contract shape** (order, argument matching, refusal of
expansion). It does **not** verify that those operations are available on a live GHL
MCP connector under the intended credential scope.

### Read/write caps, no retry, no REST fallback, no compensating mutation

```text
NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1
AUTOMATIC_RETRY=NO
COMPENSATING_MUTATION=NO
NO_RAW_REST=YES
FURTHER_TRANSPORT_CALLS_AUTHORIZED=NO_AFTER_TERMINAL_FAILURE
REFUSE_BEFORE_TRANSPORT=YES
STOP_AND_PRESERVE_PROOF=YES_ON_WRITE_READBACK_FAILURE
```

### Fail-closed terminal semantics

The AT-1 contract rejects an initial-stage mismatch before any write and refuses a
final-stage update unless the exact authorized stage is supplied. On write/readback
failure the executor stops and preserves proof; further transport calls are not
authorized after terminal failure.

### Private binding publication ban

```text
PRIVATE_BINDING_PUBLICATION=NO
PRIVATE_BINDING_VALUES_COMMITTED=NO
```

The public repository intentionally contains no customer, production, or live GHL ID
values. Private binding fingerprint/reference values remain out of scope for public
commit and must not be published here.

### Authorization gates (unchanged)

```text
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## PENDING — External GHL environment (not verified by fixtures)

The claims below remain **PENDING** until a separately authorized **read-only**
external verification completes. Deterministic fixture success must not be read as
live environment readiness.

```text
ISOLATED_GHL_TEST_LOCATION=PENDING
SYNTHETIC_CONTACT_READY=PENDING
SYNTHETIC_OPPORTUNITY_READY=PENDING
EXPECTED_INITIAL_STAGE_VERIFIED=PENDING
AUTHORIZED_FINAL_STAGE_VERIFIED=PENDING
REQUIRED_GHL_OPERATIONS_VERIFIED=PENDING
GHL_TARGET_SCOPE_VERIFIED=PENDING
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
```

### What fixture isolation does not prove

| Claim | Fixture status | External status |
| --- | --- | --- |
| Actual isolated GHL test location | synthetic placeholder only | PENDING |
| Actual GHL synthetic contact record | synthetic placeholder only | PENDING |
| Actual GHL synthetic opportunity record | synthetic placeholder only | PENDING |
| Live current initial stage | synthetic placeholder only | PENDING |
| Live permitted final stage | synthetic placeholder only | PENDING |
| Live MCP operation names/schemas available | contract enumerated only | PENDING |
| Live connector target/scope | not exercised | PENDING |
| Private binding fingerprint/reference | deliberately unpublished | PENDING (private lane) |

## Read-only external verification checklist (authorization required)

Do **not** run this checklist until separate authorization is granted. When authorized,
verification is **read-only** only.

### In scope (read-only)

1. **Isolated GHL location** — confirm the bound test location is non-production and
   matches the private binding reference (do not commit private IDs).
2. **Exact synthetic contact** — confirm the designated synthetic contact exists and
   matches the private binding (exact ID read; no search/list/pagination).
3. **Exact synthetic opportunity** — confirm the designated synthetic opportunity
   exists, is tied to the contact/location binding, and matches the private binding.
4. **Current initial stage** — confirm the opportunity’s current stage equals the
   expected initial stage before any write authorization.
5. **Permitted final stage** — confirm the authorized final stage exists in the
   location pipeline and is the only permitted transition target for AT-1.
6. **Actual GHL MCP operation names/schemas** — confirm the live connector exposes
   exactly the six-operation surface (names + required args) compatible with:
   `get-contact`, `get-opportunity`, `create-note`, `get-note`,
   `update-opportunity`, `get-opportunity` (second readback). No alternate ops.
7. **Connector target/scope** — confirm credential/connector scope is limited to the
   isolated test location and intended read (and, only later if authorized, write)
   surface; record scope evidence privately, not in the public repo.
8. **Private binding fingerprint/reference** — confirm private binding material is
   available to the authorized operator lane and is **not** published to the public
   repository (`PRIVATE_BINDING_PUBLICATION=NO` remains mandatory).

### Blocked during external verification (and until AT-1 execution is authorized)

```text
BLOCKED=create-note;
update-opportunity;
ANY_OTHER_GHL_MUTATION;
PRODUCTION_CRM;
FIRESTORE_MUTATION;
RAW_GHL_REST_FALLBACK;
SEARCH_LIST_PAGINATION_EXPANSION;
RETRY;
COMPENSATING_MUTATION;
IAM_SECRETS_DEPLOYMENT_CHANGE;
PRIVATE_ID_PUBLICATION_TO_PUBLIC_REPO
```

## Readiness disposition

```text
READINESS_RESULT=DETERMINISTIC_EXECUTOR_READY_EXTERNAL_ENVIRONMENT_NOT_VERIFIED
DETERMINISTIC_EXECUTOR_READY=YES
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

Track A currently proves only that the **deterministic bounded executor** is ready
under synthetic fixtures and fail-closed contract constraints. It does **not** prove
the live isolated GHL environment is ready. AT-1 mutation remains unauthorized.

## Retrieval / indexing note

The repository's current repo_source_review_search surface remains unable to
surface NW-008 / PR64 / Track A / Track B records. This is recorded as a later
retrieval/indexing improvement, not a substitute for external environment
verification and not a grant of AT-1 execution authority.

## STOP

```text
STOP_CODE=NW008_AT1_SAFE_ENVIRONMENT_READINESS_CORRECTED_AWAIT_READONLY_EXTERNAL_VERIFICATION_AUTH
DETERMINISTIC_EXECUTOR_READY=YES
EXTERNAL_ENVIRONMENT_VERIFIED=NO
ENVIRONMENT_READY=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
NEXT=AWAIT_SEPARATE_AUTHORIZATION_FOR_READONLY_EXTERNAL_VERIFICATION
```
