# NW-008 AT-8L - GHL REST Live Note Runtime Construction Path Implementation 001

```text
UNIT=NW008_AT8L_GHL_REST_LIVE_NOTE_RUNTIME_CONSTRUCTION_PATH_IMPLEMENTATION_001
PR_CLASS=implementation
IMPLEMENTATION_MODE=OFFLINE_AND_DETERMINISTIC_TEST_ONLY

AUTHORIZATION_PR=120
AUTHORIZATION_REVIEWED_HEAD=bb0e354d49985e5211ef97f90267b8884305e05f
AUTHORIZATION_MERGE_SHA=09dccc5cc9d341bc57f5c3770bfb74596e029974
AUTHORIZATION_EFFECTIVE_FOR_NAMED_CONSUMER=YES
AUTHORIZATION_CONSUMED=YES
AUTHORIZATION_REUSABLE=NO
```

## Composition root

`assemble_bound_live_note_runtime` accepts only `verified_capability`. It uses
the existing `note_path._require_issued_verified_capability` validator before
any adapter binding, then fails closed because AT8L does not authorize
root-owned production execution-store construction.

The non-exported `_assemble_bound_live_note_runtime_for_tests` is the sole
deterministic assembly seam. It accepts only the validated capability, an
existing `SyntheticLiveNoteSecretAccessor`, and an injected `At1ExecutionStore`.
It constructs the frozen HTTP client, credential provider, transport, and
`NotePathAdapter` from the exact validated capability identity and binds that
exact capability object to the adapter.

## Deliberate non-authority

```text
PRODUCTION_EXECUTION_STORE_CONSTRUCTION_IMPLEMENTED=NO
PRODUCTION_RUNTIME_READY=NO
CONCRETE_RUNTIME_SECRET_ACCESSOR_IMPLEMENTED=NO
REAL_SECRET_PAYLOAD_READS=0
HIGHLEVEL_CALLS=0
CRM_MUTATIONS=0
GCP_MUTATIONS=0
DEPLOYMENT_CHANGES=0
```

No transport, credential-provider, HTTP-client, note-path, or execution-store
source is modified by this implementation.
