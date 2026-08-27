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
private owner together with that owner's opaque one-shot reference and the
owner's unforgeable process-local authenticity anchor. It:

1. validates the fixed private-owner designation and resolver surface;
2. verifies the process-local authenticity anchor by identity against the
   private control plane's provisioning registry, bound to the exact resolver
   object, before invoking the private owner (shape, designation strings,
   exported classes, and callable release functions are never sufficient);
3. rejects raw values, mappings, forged/reconstructed references, a wrong
   resolver, and forged or transplanted anchors before invoking the private
   owner;
4. verifies the exact authorization identity and workflow run against the
   anchor's provisioned binding before private consumption;
5. asks the private owner to atomically release the reference; and
6. treats the two returned binding values as data only, issuing an internal
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
T11_FORGED_OWNER_WITH_CORRECT_DESIGNATION_REJECTS=PASS
T12_VALID_OWNER_REMAINS_AVAILABLE_AFTER_FORGED_OWNER_REJECTION=PASS
T13_PUBLIC_SYNTHETIC_HANDOFF_SOURCE_CANNOT_PROVISION_DESIGNATED_OWNER=PASS

TEST_COMMAND=
  PYTHONPATH=src python -m pytest -q tests/integrations/ghl/highlevel_rest
TEST_RESULT=252_PASSED

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

---

## 6. Remediation addendum (PR231 review change request)

Remediation applied in place on the PR231 branch in response to the reviewed
head `4792bae62fa2f0fe5da6ad5f2424a1f7d9c50e1f` change request:

```text
REMEDIATION_OF=AUTHORITY_AUTHENTICITY_GAP
REMEDIATION_OF=REQUIRED_EXACT_HEAD_CI_NOT_VERIFIED
REMEDIATION_OF=AUTHORITY_REBINDING_TIGHTENING
NEW_REPAIR_AUTHORIZATION_OPENED=NO
R3_EXECUTION_PERFORMED=NO
```

### 6.1 Private-owner authenticity anchor

`isinstance(resolver, ModuleType)`, `DESIGNATION_ID` string equality, exported
class types, and a callable `release_to_public_consumer` are all
caller-reproducible and are no longer treated as sufficient authenticity. The
private control plane now issues a `_PrivateOwnerAuthenticityAnchor` at owner
provisioning time. The anchor:

```text
ANCHOR_CONSTRUCTIBLE_BY_PUBLIC_CALLER=NO
ANCHOR_SERIALIZABLE=NO
ANCHOR_COPYABLE=NO
ANCHOR_RECOGNITION=PROCESS_LOCAL_IDENTITY_REGISTRY_ONLY
ANCHOR_BOUND_TO=EXACT_RESOLVER_OBJECT_WEAKREF_IDENTITY
PROVISIONING_AUTHORITY_GATE=PRIVATE_CONTROL_PLANE_OWNER_PROVISIONING_AUTHORITY
PUBLIC_SYNTHETIC_AT8_HANDOFF_SATISFIES_PROVISIONING=NO
```

The public runtime verifies the anchor by identity and resolver binding before
`release_to_public_consumer(...)` is ever called. A caller-created module that
reproduces the entire public resolver shape — exact `DESIGNATION_ID`, exported
reference/material classes, a callable release function, and plausible
non-synthetic provider IDs — fails closed, whether it presents a fabricated
anchor object or a genuine anchor transplanted from the provisioned owner.
Provisioning itself requires a distinct process-local
`_PrivateOwnerProvisioningAuthority` issued only by the private control-plane
provisioning path. A source created through
`_issue_private_at8_handoff_source_for_synthetic_tests` cannot designate an
owner. Anchor snapshots bind the resolver with `resolver_ref() is
private_owner_resolver`, not integer `id()` equality alone.

```text
PRIVATE_OWNER_AUTHENTICITY_ANCHOR=
  PROCESS_LOCAL_IDENTITY_REGISTRY_BOUND_TO_RESOLVER_IDENTITY_AND_PROVISIONED_BY_PRIVATE_CONTROL_PLANE
FORGED_CORRECT_DESIGNATION_OWNER_REJECTS=YES
VALID_OWNER_SURVIVES_FORGERY_PROBE=YES
```

### 6.2 Authorization rebinding seam

The repaired ingress no longer hard-requires the pre-repair PR223
authorization identity or workflow run. The hardcoded PR223 consumer
authorization/run constants are removed from the runtime. The exact consumer
authorization identity and workflow run are bound at owner provisioning time
into the anchor's immutable snapshot by the private control plane, so the
eventual independently reviewed post-repair R3 authorization is bound by a
governed provisioning act with no further public runtime mutation.

```text
PR223_HARDCODE_REMOVED=YES
AUTHORIZATION_MATCHING_BROADENED=NO
CALLER_SELECTED_ARBITRARY_AUTHORIZATION_IDS_ACCEPTED=NO
EXACT_AUTHORIZATION_RUN_BINDING_WAIVED=NO
POST_REPAIR_AUTHORIZATION_BINDING_READY=YES
POST_REPAIR_BINDING_REQUIRES_IMPLEMENTATION_MUTATION=NO
```

### 6.3 Remediation validation

```text
T01-T10=PASS
T11_FORGED_OWNER_WITH_CORRECT_DESIGNATION_REJECTS=PASS
T12_VALID_OWNER_REMAINS_AVAILABLE_AFTER_FORGED_OWNER_REJECTION=PASS
T13_PUBLIC_SYNTHETIC_HANDOFF_SOURCE_CANNOT_PROVISION_DESIGNATED_OWNER=PASS
TEST_RESULT=252_PASSED

NETWORK_CALLS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0

PR223_AUTHORIZATION_CONSUMED=NO
R3_EXECUTION_ATTEMPTS_USED=0
R3_EXECUTION_PERFORMED=NO
R4_PERFORMED=NO
```

### 6.4 Owner-provisioning authority origin (second change request)

```text
REMEDIATION_OF=DESIGNATED_PRIVATE_OWNER_ANCHOR_PROVISIONING_IS_REACHABLE_FROM_PUBLIC_SYNTHETIC_HANDOFF_SOURCE
OWNER_PROVISIONING_AUTHORITY_ORIGIN=
  PROCESS_LOCAL_PRIVATE_CONTROL_PLANE_PROVISIONING_AUTHORITY_TOKEN
PUBLIC_SYNTHETIC_SOURCE_CAN_PROVISION_OWNER=NO
RESOLVER_BINDING_BY_OBJECT_IDENTITY=WEAKREF_IS_CHECK
```

`provision_designated_private_owner_resolver` no longer accepts a
`_TrustedPrivateBindingSource`. It requires a distinct
`_PrivateOwnerProvisioningAuthority` issued only by
`issue_private_owner_provisioning_authority` inside the private control-plane
trust issuer. `_issue_private_at8_handoff_source_for_synthetic_tests` remains
the public synthetic lease-handoff path and cannot provision a designated
owner.
