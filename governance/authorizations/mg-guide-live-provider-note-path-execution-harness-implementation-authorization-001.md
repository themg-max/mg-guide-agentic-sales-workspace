# MG Guide Live Provider NOTE_PATH Execution Harness Implementation Authorization 001

## 0. Authorization identity and boundary

```text
AUTHORIZATION_ID=MG_GUIDE_LIVE_PROVIDER_NOTE_PATH_EXECUTION_HARNESS_IMPLEMENTATION_AUTHORIZATION_001
ARTIFACT_PATH=governance/authorizations/mg-guide-live-provider-note-path-execution-harness-implementation-authorization-001.md
PR_CLASS=authorization
MODE=IMPLEMENTATION_AUTHORIZATION_ONLY
OWNER=VS_CODE_ORCHESTRATOR+HUMAN_GOVERNANCE
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T19:11:00Z
BASE_MAIN_SHA=d9ec4d855afa51a3977c6469b0e8c684c2e1f67f
STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW
```

This unit authorizes writing code. It is not an execution authority. It makes
no HighLevel call, reads no Secret Manager payload, mutates no CRM record,
changes no IAM, performs no deployment, and dispatches no workflow.

```text
GHL_CALLS=0
SECRET_PAYLOAD_READS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
WORKFLOW_DISPATCHES=0
IMPLEMENTATION_PERFORMED_IN_THIS_UNIT=NO
```

## 1. Bound prior records

```text
LIVE_PROVIDER_E2E_PLAN_PR=417
LIVE_PROVIDER_E2E_PLAN_MERGE_SHA=5dcc308d66e27a93119d6f8f4eb44be3f5242e9b

SCOPE_AUTHORIZATION_ID=MG_GUIDE_LIVE_PROVIDER_NOTE_PATH_AUTHORIZATION_001
SCOPE_AUTHORIZATION_PR=418
SCOPE_AUTHORIZATION_MERGE_SHA=bfec783b2fd25e09c09540664866c2c5c7bd4c2d
AUTHORIZATION_001_CONSUMED=NO
AUTHORIZATION_001_REUSABLE_AS_DEFINITION=YES

EXPIRY_RECONCILIATION_001_PR=421
EXPIRY_RECONCILIATION_001_MERGE_SHA=883d5678a648757fcdee2f1851b3d65a4b7a8cc9

ACTIVATION_002_PR=422
ACTIVATION_002_MERGE_SHA=6429b78539154b0f249507e2d567cf2e02ce9d5c
ACTIVATION_002_DISPOSITION=EXPIRED_UNUSED

CONSUMPTION_RECORD_002_PR=423
CONSUMPTION_RECORD_002_MERGE_SHA=a118d29b67b74830ac3d811494c0d3d8ee247bd2
CONSUMPTION_RECORD_002_DISPOSITION=VOID_EXPIRED_PRE_DISPATCH

HARNESS_DESIGN_PR=424
HARNESS_DESIGN_MERGE_SHA=04d7d5363c12bed05a78a1bd7edd60283ec32dc6

EXPIRY_RECONCILIATION_002_PR=425
EXPIRY_RECONCILIATION_002_HEAD=103f99f7e2e2b8191b8ea3cd34fd27e1bdb6ee99
EXPIRY_RECONCILIATION_002_MERGE_SHA=d9ec4d855afa51a3977c6469b0e8c684c2e1f67f

ACTIVATION_003_CREATED=NO
ALL_BOUND_MERGE_SHAS_IN_CURRENT_MAIN_ANCESTRY=YES
EXPIRY_RECONCILIATION_002_MERGED_AT_EXACT_REVIEWED_HEAD=YES
```

No live-provider RUN_ID is bound by this authorization. RUN_ID
`mg-guide-live-provider-note-path-002-20260831T175220Z-c780` is terminal and
must not be revived.

## 2. Authorized implementation paths

```text
IMPLEMENTATION_AUTHORIZED=YES

AUTHORIZED_IMPLEMENTATION_PATHS=
  src/integrations/ghl/highlevel_rest/live_note_execution.py
  tests/integrations/ghl/highlevel_rest/test_live_note_execution.py
  .github/workflows/mg-guide-live-provider-note-path.yml
  docs/runbooks/mg-guide-live-provider-note-path-operator-runbook.md

AUTHORIZED_EVIDENCE_PATH=
  proof/mg-guide/agent-runtime/mg-guide-live-provider-note-path-execution-harness-implementation-proof-001.md

PATH_SET_EXHAUSTIVE=YES
ANY_OTHER_PATH_MODIFICATION_AUTHORIZED=NO
EXISTING_MERGED_MODULE_MODIFICATION_AUTHORIZED=NO
```

The evidence path is authorized separately from the four implementation paths
and carries no execution authority of its own. Modification of any already
merged module — including the five mandatory-reuse modules — is outside this
authorization; if the implementation appears to require such a change, the
implementer must stop and request a separate authorization rather than widen
scope.

## 3. Effects explicitly NOT authorized

```text
LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
WORKFLOW_DISPATCH_LIVE_EXECUTION_AUTHORIZED=NO
SECRET_PAYLOAD_ACCESS_AUTHORIZED=NO
HIGHLEVEL_CALLS_AUTHORIZED=NO
CRM_MUTATION_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO
REASONING_ENGINE_ALTERATION_AUTHORIZED=NO
TERRAFORM_APPLY_AUTHORIZED=NO
WRITE_SCOPE_PROBE_AUTHORIZED=NO

MERGE_OF_HARNESS_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION=FORBIDDEN
```

Merging the harness produces a mechanism, not a permission. Execution requires
a fresh live-provider authorization, Human Activation 003, Consumption Record
003, and a separate explicit human execution act.

## 4. Required implementation contract

### 4.1 Mandatory reuse

```text
MANDATORY_REUSE=
  live_note_runtime
  live_note_credential_provider
  live_note_http_client
  live_note_transport
  note_path

NO_SECOND_REST_TRANSPORT=YES
NO_NEW_HTTP_CLIENT=YES
NO_NEW_CREDENTIAL_ACCESSOR=YES
NO_NEW_NOTE_SERIALIZER=YES
NO_NEW_DIGEST_FUNCTION=YES
NO_REDECLARATION_OF_PINNED_IDENTITIES_OR_RESOURCES=YES
```

The source principal, target note-runtime principal, WIF audience, and exact
secret version are already pinned as merged module constants. The harness
consumes them and must not re-declare, parameterize, or override them.

### 4.2 Required components

```text
C1 process entrypoint (python -m integrations.ghl.highlevel_rest.live_note_execution)
C2 governance / activation-window / RUN_ID preflight, fail closed
C3 hosted three-agent attribution check
     meeting_context_agent -> relationship_context_agent -> follow_up_planning_agent
C4 pure hosted-output -> note_contract mapper
C5 frozen digest verification against the Section 6 values
C6 ordered drive of the existing adapter (Section 5 sequence)
C7 sanitized terminal report emission
C8 fail-closed exit behaviour on every gate
```

### 4.3 Gate ordering (normative)

```text
ORDER=C2 -> C3 -> C4 -> C5 -> [private-origin materialization check]
      -> [secret access] -> C6 -> C7
SECRET_ACCESS_OCCURS_AFTER_ALL_NON_PROVIDER_GATES=YES
ANY_GATE_FAILURE_BEFORE_SECRET_ACCESS=ZERO_SECRET_READS_AND_ZERO_DISPATCHES
```

Every gate that can fail without touching the provider must fail before the
secret is read. This ordering is what keeps a defect from consuming one-shot
authority.

### 4.4 Preserved structural precondition

`build_bound_contact_get` compares returned `id` and `locationId` against the
bound values, raises on mismatch, and only then issues the capability the note
POST requires. The harness must not weaken, bypass, or pre-seed this. The test
seams `_assemble_bound_live_note_runtime_for_tests` and
`issue_synthetic_test_capability` must remain unreachable from the production
entrypoint.

## 5. Frozen provider sequence (unchanged)

```text
1  GET  /contacts/{bound_contact_id}
2  POST /contacts/{bound_contact_id}/notes          body field only
3  GET  /contacts/{bound_contact_id}/notes/{same_run_note_id}

MAX_PROVIDER_CALLS=3
MAX_CONTACT_GET_ATTEMPTS=1
MAX_NOTE_CREATE_ATTEMPTS=1
MAX_NOTE_READBACK_ATTEMPTS=1
MAX_TOTAL_GHL_MUTATIONS=1
MAX_OPPORTUNITY_STAGE_TRANSITIONS=0

NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_FALLBACK=YES
NO_ALTERNATE_OPERATION=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES
NO_GENERIC_EXECUTE=YES
NO_STAGE_MUTATION=YES

STAGE_PATH_AUTHORIZED=NO
STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
```

## 6. R1 — write scope never exercised over the network

```text
R1_RESOLUTION_STRATEGY=FRESH_HUMAN_OWNER_CONSOLE_REATTESTATION_BEFORE_LIVE_ACTIVATION
REQUIRE_CURRENT_CONTACTS_WRITE_SCOPE_REATTESTATION=YES
SEPARATE_WRITE_SCOPE_PROVIDER_PROBE=NO
WRITE_SCOPE_PROBE_AUTHORIZED=NO
REATTESTATION_EXECUTED_BY_THIS_AUTHORIZATION=NO
```

`contacts.write` is attested present by human owner console review only
(`SCOPE_VERIFICATION_METHOD=HUMAN_OWNER_CONSOLE_REVIEW_RECORDED_BY_ORCHESTRATOR`);
the one proven live call used `contacts.readonly`. The authorized note POST
would be the first live write with this PIT.

Any future live authorization must state:

```text
401_OR_403_ON_FIRST_PROVIDER_ATTEMPT_IS_TERMINAL=YES
AUTHORITY_RESTORED_ON_SCOPE_FAILURE=NO
AUTHORITY_RESTORED_ON_FAILURE=NO
NO_RETRY=YES
```

The re-attestation is a human owner act performed immediately before live
activation. It is not performed here, and no provider probe substitutes for it.

## 7. R2 — offline mapper digest closure

```text
OFFLINE_MAPPER_DIGEST_CLOSURE_REQUIRED=YES
CLOSURE_IS_PRECONDITION_FOR_LIVE_AUTHORIZATION_REQUEST=YES

TRANSCRIPT_SHA256=1a1a002eb79701d436d199a63ddba0f8e532dd96d1591cc437157e90481a24aa
NOTE_CONTENT_LOGICAL_SHA256=4d581696b2b60a6fbdccef2ea8532ecdfe98f967496fac3f6942103b94626ac2
NOTE_BODY_SHA256=a404ad7343269ea8832618c6be70320ddc5403bf146c04a9e606e148746e0db5
PROVIDER_BODY_SHA256=fbf03c4e76911679980c8956ad93c26510f77cef51c2b0b48c5d46c11f774286

COMPARISON=EXACT_STRING_EQUALITY
TOLERANT_OR_PARTIAL_MATCH_ALLOWED=NO

REAL_SECRET_READS=0
REAL_GHL_CALLS=0
REAL_CRM_MUTATIONS=0
NETWORK_CALLS=0

ON_ANY_DIGEST_DIFFERENCE:
  FAIL_CLOSED=YES
  LIVE_AUTHORIZATION_REQUEST_ALLOWED=NO
```

The mapper must be pure and deterministic, must not invent content, default
missing required fields, reorder list content, truncate, or summarize.
Serialization, canonical JSON, NFC normalization, and all digests remain
`note_path`'s responsibility; the mapper returns a `Mapping` only. The exact
ten-field contract is specified in merged design PR 424 section 5.2.

## 8. R5 — private-origin same-process materialization

```text
PRIVATE_ORIGIN_INGRESS_CONTRACT_PRESENT=YES
PRIVATE_ORIGIN_GITHUB_ACTIONS_SAME_PROCESS_MATERIALIZATION=UNRESOLVED_UNTIL_PROVEN

CROSS_PROCESS_HANDOFF_ALLOWED=NO
CROSS_PROCESS_REFERENCE_TRANSFER_ALLOWED=NO
SERIALIZED_REFERENCE_ALLOWED=NO
REFERENCE_SERIALIZATION_ALLOWED=NO
RAW_PROVIDER_IDS_ALLOWED=NO
RAW_IDS_AS_WORKFLOW_INPUTS_ALLOWED=NO
CALLER_RECONSTRUCTION_ALLOWED=NO
CALLER_RECONSTRUCTED_CAPABILITY_ALLOWED=NO
RAW_ID_FALLBACK_ALLOWED=NO

LIVE_EXECUTION_BLOCKED_WHILE_R5_UNRESOLVED=YES
```

The merged root composer honours only an **already-imported** module and never
imports one on a caller's behalf. Whether a legitimate private origin can be
provisioned into the same process inside a GitHub Actions runner is unproven,
and it is the item most likely to block live execution even after the harness
exists.

Permitted in this implementation:

```text
FAIL_CLOSED_HOOK_OR_INTERFACE_FOR_ROOT_OWNED_PRIVATE_ORIGIN=ALLOWED
```

Required behaviour:

```text
ABSENT_LEGITIMATE_SAME_PROCESS_ORIGIN=REFUSE_BEFORE_SECRET_MANAGER_ACCESS
REFUSAL_IS_TERMINAL=YES
DEGRADE_TO_CALLER_SUPPLIED_IDENTIFIER=FORBIDDEN
INVENTING_A_RAW_ID_FALLBACK=FORBIDDEN
```

A hook that merely appears to satisfy the interface while accepting
caller-reconstructed material does not resolve R5 and must not be presented as
resolving it.

## 9. Required deterministic tests

All must run with zero real network and zero real Secret Manager access, using
the existing fake transport and synthetic accessor seams.

```text
T01 three-agent order success
T02 agent-order mismatch fails closed
T03 missing agent fails closed
T04 mapper exact-contract success
T05 mapper missing-field fails closed
T06 all frozen digests match
T07 digest mismatch fails before secret access
T08 missing activation fails closed
T09 expired activation fails closed
T10 missing private origin fails closed before secret access
T11 wrong authorization / run binding fails closed
T12 get_contact mismatch prevents POST
T13 create_note uncertainty prevents readback and prevents retry
T14 readback uses same-run note ID only
T15 sanitized output only (no token, raw contact/location/note ID, or full response)
T16 exact three-call success simulation
T17 at most one mutation
T18 no search / list / pagination / retry / fallback / stage operation
T19 zero real network and zero real Secret Manager access

TEST_MATRIX_EXHAUSTIVE_FOR_MERGE=YES
```

## 10. Required validation before merge

```text
CANONICAL_DETERMINISTIC_VALIDATION=REQUIRED
FULL_PYTEST=REQUIRED
GIT_DIFF_CHECK=REQUIRED
SECRET_PATTERN_SCAN=REQUIRED
PATH_SPECIFIC_STAGING=REQUIRED
GIT_ADD_ALL=FORBIDDEN
BRANCH_MAIN=FORBIDDEN
```

## 11. Successor activation gate

```text
ACTIVATION_003_AUTHORIZED_TO_CREATE_NOW=NO

REQUIRED_BEFORE_ACTIVATION_003=
  HARNESS_IMPLEMENTATION_MERGED=YES
  OFFLINE_MAPPER_DIGEST_PROOF=PASS
  R5_SAME_PROCESS_MATERIALIZATION_PROVEN=YES
  RUNBOOK_REVIEWED=YES
  CURRENT_WRITE_SCOPE_REATTESTED=YES
  FRESH_LIVE_EXECUTION_AUTHORIZATION_MERGED=YES

THEN_ORDER=
  fresh live-provider authorization binding the exact merged harness SHA
  -> Human Activation 003
  -> Consumption Record 003
  -> separate explicit human execution act
```

Consistent with merged Expiry Reconciliation 002, no activation window may be
opened before a reviewed harness exists. Activations 001 and 002 both expired
unused because a bounded window was opened while no execution mechanism
existed; this gate exists to prevent a third occurrence.

## 12. Stop

```text
IMPLEMENTATION_AUTHORIZED=YES
LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
ACTIVATION_003_AUTHORIZED_TO_CREATE_NOW=NO
STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_HARNESS_IMPLEMENTATION
```
