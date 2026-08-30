# NW-008 AT1 GHL Private Target Binding Readiness Proof 001

## 0. Proof identity

```text
PROOF_ID=
  NW008_AT1_GHL_PRIVATE_TARGET_BINDING_READINESS_PROOF_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-private-target-binding-readiness-proof-001.md
CLASSIFICATION=SANITIZED_PRIVATE_BINDING_READINESS_PROOF
PR_CLASS=proof
MODE=PRIVATE_BINDING_MATERIALIZATION_ATTESTATION_ONLY
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-30T19:54:23Z

GHL_REQUESTS=0
CRM_MUTATIONS=0
LIVE_PROVIDER_CALLS=0
SECRET_ACCESS_ATTEMPTS=0
```

This proof attests that the existing private NW-008 synthetic-target
control-plane binding now carries a materialized, non-placeholder, scalar
canonical GHL Location ID together with the existing exact private synthetic
contact and opportunity scalars. It does **not** authorize HighLevel access,
credential access, CRM mutation, or any provider call.

Raw contact, location, and opportunity identifiers remain exclusively in the
private control plane. They are not present in this artifact.

## 1. Private control-plane binding locus

```text
PRIVATE_BINDING_REPOSITORY=themg-max/A.I-Rolodex---Context
PRIVATE_BINDING_REPOSITORY_VISIBILITY=PRIVATE
PRIVATE_BINDING_PATH=
  .ai/memory/features/gov/
  mg-guide-ghl-canonical-synthetic-read-proof-v1/
  synthetic-record-binding.yaml
PRIVATE_BINDING_BRANCH=
  govern/nw008-at1-ghl-private-location-materialization-001
PRIVATE_BINDING_COMMIT=
  855361fcab100d07196bc021af89f7375ed2b04a
PRIVATE_BINDING_BLOB_SHA=
  d76d70fd3a66af775e2520819bf6aff68c9566ae
PRIVATE_BINDING_PRESENT=YES
PRIVATE_IDENTIFIER_PUBLICATION_ALLOWED=NO
```

Public companion authorities (no raw IDs):

```text
CANONICAL_BINDING_AUTHORITY=
  governance/authorizations/MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1.yaml
CANONICAL_BINDING_PUBLIC_EVIDENCE=
  proof/canonical-synthetic-read-binding-v1/synthetic-record-binding.yaml
```

## 2. Materialization gates (sanitized)

```text
PRIVATE_BINDING_PRESENT=YES

CONTACT_ID_MATERIALIZED=YES
CONTACT_ID_NON_PLACEHOLDER=YES

LOCATION_ID_MATERIALIZED=YES
LOCATION_ID_NON_PLACEHOLDER=YES
LOCATION_ID_SCALAR=YES

OPPORTUNITY_ID_MATERIALIZED=YES

SYNTHETIC_RECORD_CLASS_VERIFIED=YES
RECORD_CLASS=SYNTHETIC_ONLY

CONTACT_LOCATION_SAME_INTENDED_SYNTHETIC_TARGET=YES
OPPORTUNITY_CONTACT_RELATION_BOUND=YES
PRIVATE_PACKAGE_FINGERPRINT_ALIGNMENT=YES
```

Same-target alignment was proven offline against the standing private NW-008
fresh execution package and Grant 008 post-correction fingerprints. Contact and
opportunity scalars already present in the private binding matched that package.
The location scalar was the only previously unpublished placeholder
(`UNPUBLISHED_PRIVATE_ONLY`) and was replaced by the exact canonical private
location scalar from the secure operator private package. No HighLevel request
was issued for this proof.

## 3. Disclosure boundary

```text
RAW_CONTACT_ID_PUBLISHED=NO
RAW_LOCATION_ID_PUBLISHED=NO
RAW_OPPORTUNITY_ID_PUBLISHED=NO

SECRET_VALUE_PUBLISHED=NO
SECRET_VALUE_PERSISTED=NO
SECRET_VALUE_LOGGED=NO
SECRET_VALUE_ECHOED=NO
PIT_VALUE_PUBLISHED=NO
```

## 4. Effect ledger

```text
GHL_REQUESTS=0
GHL_REST_CALLS=0
GHL_READ_ATTEMPTS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
CREATE_NOTE_ATTEMPTS=0
UPDATE_OPPORTUNITY_ATTEMPTS=0
SEARCH_ATTEMPTS=0
LIST_ATTEMPTS=0
```

## 5. Binding readiness decision

```text
BINDING_READINESS=PASS
STOP=NO
PRIVATE_TARGET_BINDING_MISMATCH=NO
LOCATION_ID_MATERIALIZED=YES
LOCATION_ID_NON_PLACEHOLDER=YES
LOCATION_ID_SCALAR=YES
RAW_LOCATION_ID_PUBLISHED=NO
```

## 6. Downstream authority (not opened by this proof)

```text
THIS_PROOF_AUTHORIZES_GHL_READ=NO
THIS_PROOF_AUTHORIZES_SECRET_ACCESS=NO
THIS_PROOF_AUTHORIZES_CRM_MUTATION=NO
PR_362_REUSE_ALLOWED=NO
AUTHORIZATION_002_REUSE_ALLOWED=NO

NEXT_REQUIRED_AUTHORITY=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_AUTHORIZATION_003
NEXT_REQUIRED_ACTIVATION=
  NW008_AT1_GHL_REST_V3_BOUNDED_READ_HUMAN_ACTIVATION_003
NEXT_REQUIRED_RUN_ID=FRESH_ONE_SHOT_RUN_ID
BOUNDED_READ_OPERATION=
  GET /contacts/{exact private synthetic contact}
BOUNDED_READ_SUCCESS_GATES=
  HTTP_2XX=YES
  CONTACT_ID_MATCH=YES
  LOCATION_ID_MATCH=YES
  NO_RETRY=YES
  NO_SEARCH=YES
  NO_LIST=YES
  NO_FALLBACK=YES
  CRM_MUTATIONS=0
```

After independent review and merge of this proof, a **fresh** Authorization 003
and Activation 003 must be defined. PR #362 / Authorization 002 must not be
reused. The later one-shot GET may proceed only under that fresh authority and
only against the private control-plane binding attested here.

## 7. Terminal board

```text
PRIVATE_BINDING_PRESENT=YES
CONTACT_ID_MATERIALIZED=YES
CONTACT_ID_NON_PLACEHOLDER=YES
LOCATION_ID_MATERIALIZED=YES
LOCATION_ID_NON_PLACEHOLDER=YES
LOCATION_ID_SCALAR=YES
OPPORTUNITY_ID_MATERIALIZED=YES
SYNTHETIC_RECORD_CLASS_VERIFIED=YES
RAW_CONTACT_ID_PUBLISHED=NO
RAW_LOCATION_ID_PUBLISHED=NO
RAW_OPPORTUNITY_ID_PUBLISHED=NO
GHL_REQUESTS=0
CRM_MUTATIONS=0
BINDING_READINESS=PASS
```
