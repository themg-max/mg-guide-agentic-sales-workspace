# NW-008 AT8W30 R3 Private-Owner Public Ingress Repair Proof 001

```text
UNIT=
  NW008_AT8W30_R3_PRIVATE_OWNER_PUBLIC_INGRESS_REPAIR_001
AUTHORIZATION_ID=
  NW008_AT8W30_R3_PRIVATE_OWNER_PUBLIC_INGRESS_REPAIR_AUTHORIZATION_001
AUTHORIZATION_PR=230
AUTHORIZATION_MERGE_COMMIT=
  f09879ed4f07415f6f94d35b776318e91ff28bec

RESULT=PASS
STOP_CODE=NONE
```

## 1. Authorization consumption

```text
IMPLEMENTATION_AUTHORIZATION_CONSUMED=YES
IMPLEMENTATION_ATTEMPTS_USED=1
CONSUMPTION_RECORD=
  proof/nw008/at-8w30/nw008-at8w30-r3-private-owner-public-ingress-repair-consumption-001.md

CONSUMPTION_TRIGGER=
  FIRST_AUTHORIZED_REPOSITORY_MUTATION_ATTEMPT_BY_UNIT_NW008_AT8W30_R3_PRIVATE_OWNER_PUBLIC_INGRESS_REPAIR_001
CONSUMPTION_EVENT=CREATION_OF_REQUIRED_CONSUMPTION_RECORD

ONE_SHOT=YES
REUSABLE=NO
FAILURE_RESTORES_AUTHORITY=NO
```

## 2. Implemented public ingress boundary

The public runtime now accepts a process-local resolver from the designated
private owner together with that owner's opaque one-shot reference. It:

1. validates the fixed private-owner designation and resolver surface;
2. rejects raw values, mappings, forged/reconstructed references, and a wrong
   resolver before invoking the private owner;
3. verifies the exact authorization identity and workflow run before private
   consumption;
4. asks the private owner to atomically release the reference; and
5. treats the two returned binding values as data only, issuing an internal
   capability after the private verification has completed.

```text
PRIVATE_OWNER_REMAINS_AUTHORITY_SOURCE=YES
PUBLIC_RAW_ID_AUTHORITY_MINTING=NO
PUBLIC_PRODUCTION_LEASE_MATERIALIZATION=NO
SYNTHETIC_TEST_PATH_GUARD_RETAINED=YES
CROSS_PROCESS_HANDOFF=NO
REFERENCE_SERIALIZATION_OR_RECONSTRUCTION=NO
ALTERNATE_TRANSPORT=NO
```

No private owner locator, path, identifier, credential, token, secret payload,
or provider response is present in this proof.

## 3. Authorized changed paths

```text
CHANGED_PATHS=
  src/integrations/ghl/highlevel_rest/note_path.py|
  src/integrations/ghl/highlevel_rest/live_note_runtime.py|
  tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py|
  tests/integrations/ghl/highlevel_rest/test_private_owner_public_ingress_repair.py|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-owner-public-ingress-repair-consumption-001.md|
  proof/nw008/at-8w30/nw008-at8w30-r3-private-owner-public-ingress-repair-proof-001.md

AUTHORIZED_PATH_GROUPS_ONLY=YES
```

## 4. Required offline test matrix

```text
T01_LEGACY_SYNTHETIC_PATH_REMAINS_PASS=PASS
T02_RAW_LIVE_IDS_ALONE_REJECT=PASS
T03_FORGED_REFERENCE_REJECTS=PASS
T04_RECONSTRUCTED_OR_SERIALIZED_REFERENCE_REJECTS=PASS
T05_WRONG_OWNER_OR_DESIGNATION_REJECTS=PASS
T06_WRONG_AUTHORIZATION_IDENTITY_REJECTS=PASS
T07_WRONG_WORKFLOW_RUN_ID_REJECTS=PASS
T08_VALID_PRIVATE_OWNER_ONE_SHOT_REFERENCE_PASS=PASS
T09_REPLAY_OR_SECOND_CONSUME_REJECTS=PASS
T10_NON_SYNTHETIC_APPROVED_TARGET_TRAVERSES_AFTER_VERIFIED_PROVENANCE=PASS

TEST_COMMAND=
  PYTHONPATH=src python -m pytest -q tests/integrations/ghl/highlevel_rest
TEST_RESULT=247_PASSED

NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
```

## 5. R3 and PR223 preservation

```text
R3_EXECUTION_PERFORMED=NO
R3_TARGET_RUNTIME_CREDENTIAL_CONSTRUCTIONS=0
PR223_AUTHORIZATION_STATE=AVAILABLE_UNCONSUMED
PR223_AUTHORIZATION_CONSUMED=NO
R3_EXECUTION_ATTEMPTS_USED=0
R3_RETRY_AUTHORIZED=NO
R4_PERFORMED=NO
R4_AUTHORIZED=NO
```

This repair authorizes and implements no R3 execution. Under PR230's authority
rebinding rule, a future R3 operation requires an independently reviewed
authorization that binds the repaired runtime's reviewed head and merge commit.
