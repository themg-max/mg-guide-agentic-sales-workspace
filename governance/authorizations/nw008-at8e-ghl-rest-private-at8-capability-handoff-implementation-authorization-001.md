# NW-008 AT-8E — HighLevel REST Private AT8 Capability-Handoff Implementation Authorization 001

## 1. Authorization identity and activation boundary

```text
UNIT=NW008_AT8E_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_AUTHORIZATION_001
CLASSIFICATION=authorization
PR_CLASS=authorization
OWNER=VS Code orchestrator
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
MODE=AUTHORIZATION_ARTIFACT_ONLY

AUTHORIZATION_BRANCH=governance/nw008-at8e-ghl-rest-private-at8-capability-handoff-implementation-authorization-001
AUTHORIZATION_ARTIFACT=governance/authorizations/nw008-at8e-ghl-rest-private-at8-capability-handoff-implementation-authorization-001.md

SOURCE_AT8C_PR=102
SOURCE_AT8C_MERGE_SHA=441650d4bc8567d3865d35bdb36379556f36c4d7

SOURCE_AT8D_PR=103
SOURCE_AT8D_HEAD=5307a40c5893b50307c968da3ee616f7f492966b
SOURCE_AT8D_MERGE_SHA=b04da1cfbeaadd5827b12a372a27bcc27192acb6
SOURCE_AT8D_MERGE_VERIFIED=YES

SOURCE_LIVE_READ_PROOF_PR=99
SOURCE_LIVE_READ_PROOF_MERGE_SHA=6256f287bbd88effc2ef1cd13a801faec79a0af2

SOURCE_HARDENING_PR=101
SOURCE_HARDENING_MERGE_SHA=12a47888567c0842e4791cc78970c6760292f3ea

BASE_REF=origin/main
BASE_SHA=b04da1cfbeaadd5827b12a372a27bcc27192acb6

STATUS=PROPOSED_PENDING_HUMAN_REVIEW_AND_MERGE

GRANT=PRIVATE_AT8_VERIFIED_BINDING_CAPABILITY_HANDOFF_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
EFFECTIVE_CONDITION=EXACT_AUTHORIZATION_ARTIFACT_MERGED_TO_MAIN_AND_VERIFIED_BY_CONSUMER
SELF_ACTIVATION=FORBIDDEN
ARTIFACT_TEXT_MUTATION_AFTER_MERGE_REQUIRED=NO

AUTHORIZED_CONSUMER_UNIT=NW008_AT8F_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_001
AUTHORIZED_CONSUMER_PR_CLASS=implementation
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

IMPLEMENTATION_MODE=OFFLINE_ONLY
```

This artifact is an authorization proposal only. Creating, reviewing, or merging
it does not implement adapter code, open a network socket, load a credential,
touch HighLevel, retrieve a private CRM binding, issue a contact GET, issue a
note POST, integrate `At1ExecutionStore`, or produce live CRM effects.

The sole authorized consumer is
`NW008_AT8F_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_001`.
No other unit may consume this grant.

### Conditional grant semantics

```text
GRANT=PRIVATE_AT8_VERIFIED_BINDING_CAPABILITY_HANDOFF_OFFLINE_IMPLEMENTATION
GRANT_STATUS=CONDITIONAL
GRANT_ACTIVATION=MERGE_TO_MAIN
AUTHORIZATION_EFFECTIVE=NO
```

Before merge, this grant is not effective. `GRANT_STATUS=CONDITIONAL` means the
artifact defines a bounded offline private AT8 verified-binding capability
handoff permission that becomes usable only when both of the following are
true:

1. the exact authorization artifact path is present on `main` via human review
   and merge; and
2. the authorized consumer unit
   `NW008_AT8F_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_001`
   verifies that merge (exact path on `origin/main` / merge ancestry) before
   writing code.

The artifact text does not need to mutate after merge to become effective.
Effectiveness is established by merge presence plus consumer verification, not
by rewriting `AUTHORIZATION_EFFECTIVE` inside this file.

This grant is one-shot, non-reusable, and non-transferable. It is not runtime
execution authority, not live-read authority, not live-mutation authority, not
a third-provider-call grant, not AT8 evidence converted into write authority,
and not a reusable standing grant.

```text
IMPLEMENTATION_SLICE=NOTE_PATH_PRIVATE_AT8_CAPABILITY_HANDOFF
IMPLEMENTATION_MODE=OFFLINE_ONLY
GRANT_PERMITS_WHEN_EFFECTIVE=PRIVATE_AT8_VERIFIED_BINDING_CAPABILITY_HANDOFF_OFFLINE_IMPLEMENTATION_ONLY

NOTE_PATH_ARCHITECTURE_READY=YES
STAGE_PATH_ARCHITECTURE_READY=NO
STAGE_PATH_IMPLEMENTATION_AUTHORIZED=NO
STAGE_PATH_RUNTIME_ENABLED=NO

NETWORK_ACCESS_AUTHORIZED=NO
HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
HIGHLEVEL_NETWORK_CALLS_AUTHORIZED=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
CREDENTIAL_USE_AUTHORIZED=NO
SECRET_ACCESS=NO
IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO
LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO
LIVE_EXECUTION_AUTHORIZED=NO
LIVE_CRM_MUTATION_AUTHORIZED=NO
REST_ADAPTER_LIVE_EXECUTION_AUTHORIZED=NO
THIRD_CONTACT_GET_AUTHORIZED=NO
NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
EXTERNAL_EFFECTS_ALLOWED=0
```

## 2. Verified prerequisites and source provenance

Preflight was run before this artifact was authored.

```text
Working branch is not main
YES

SOURCE_AT8C_MERGE_SHA is ancestor of origin/main
441650d4bc8567d3865d35bdb36379556f36c4d7
YES

SOURCE_AT8D_HEAD is ancestor of origin/main
5307a40c5893b50307c968da3ee616f7f492966b
YES

SOURCE_AT8D_MERGE_SHA is ancestor of origin/main
b04da1cfbeaadd5827b12a372a27bcc27192acb6
YES

SOURCE_LIVE_READ_PROOF_MERGE_SHA is ancestor of origin/main
6256f287bbd88effc2ef1cd13a801faec79a0af2
YES

SOURCE_HARDENING_MERGE_SHA is ancestor of origin/main
12a47888567c0842e4791cc78970c6760292f3ea
YES
```

| Precondition | Result |
| --- | --- |
| Working branch is not `main` | YES |
| PR #102 merge commit | `441650d4bc8567d3865d35bdb36379556f36c4d7` |
| PR #102 merge commit is reachable from `origin/main` | YES |
| PR #103 reviewed head | `5307a40c5893b50307c968da3ee616f7f492966b` |
| PR #103 merge commit | `b04da1cfbeaadd5827b12a372a27bcc27192acb6` |
| PR #103 merge commit is reachable from `origin/main` | YES |
| PR #99 merge commit | `6256f287bbd88effc2ef1cd13a801faec79a0af2` |
| PR #99 merge commit is reachable from `origin/main` | YES |
| PR #101 merge commit | `12a47888567c0842e4791cc78970c6760292f3ea` |
| PR #101 merge commit is reachable from `origin/main` | YES |
| This unit executed a live GET | NO |
| This unit executed a live POST | NO |
| This unit loaded credentials | NO |
| This unit accessed HighLevel | NO |
| Live mutation authorization issued | NO |
| AT8F implemented by this unit | NO |

Bound durable source inputs (read-only for the future implementation lane):

```text
WORKFLOW_ID=meeting_follow_up_v1

AT8_SOURCE_EXECUTION_UNIT=NW008_AT8_GHL_REST_EXACT_SYNTHETIC_CONTACT_LIVE_READ_EXECUTION_002
AT8_SOURCE_PROOF_MERGE_SHA=6256f287bbd88effc2ef1cd13a801faec79a0af2

AT8_READ_GRANT_CONSUMED=YES
AT8_READ_GRANT_REUSABLE=NO
AT8_READ_GRANT_TRANSFERABLE=NO
AT8_EVIDENCE_IS_WRITE_AUTHORITY=NO

SOURCE_AT8C_PR=102
SOURCE_AT8C_MERGE_SHA=441650d4bc8567d3865d35bdb36379556f36c4d7
SOURCE_AT8D_PR=103
SOURCE_AT8D_HEAD=5307a40c5893b50307c968da3ee616f7f492966b
SOURCE_AT8D_MERGE_SHA=b04da1cfbeaadd5827b12a372a27bcc27192acb6
SOURCE_HARDENING_PR=101
SOURCE_HARDENING_MERGE_SHA=12a47888567c0842e4791cc78970c6760292f3ea
```

AT8 evidence remains evidence only. The AT8 read grant remains consumed,
non-reusable, and non-transferable. AT8F may validate AT8 proof provenance as
an input to an offline trusted capability. AT8F may not treat AT8 evidence as
note-write authority, live-read authority, or live-mutation authority.

## 3. What this authorization permits

AT8F may implement only a trusted handoff seam equivalent to:

```text
trusted private-binding input
+ AT8 proof provenance
+ consumer_authorization_identity
+ consumer_workflow_run_id
+ workflow_id
=> immutable trusted verified-contact capability
```

Permit only:

- internal capability factory/handoff
- injected private-binding-source interface/protocol
- immutable capability construction
- provenance validation
- workflow validation
- consumer authorization binding
- workflow-run binding
- deterministic synthetic tests

Do not implement provider operations.

```text
PROVIDER_OPERATIONS_AUTHORIZED=NO
CONTACT_GET_AUTHORIZED=NO
NOTE_POST_AUTHORIZED=NO
NOTE_READBACK_AUTHORIZED=NO
STAGE_TRANSITION_AUTHORIZED=NO
```

## 4. Private data boundary

```text
REAL_PRIVATE_IDS_IN_REPO=FORBIDDEN
REAL_PRIVATE_IDS_IN_FIXTURES=FORBIDDEN
REAL_PRIVATE_IDS_IN_TESTS=FORBIDDEN

PRIVATE_BINDING_PUBLICATION=NO
PRIVATE_BINDING_LOGGING=NO

TEST_IDS=SYNTHETIC_ONLY

SECRET_MANAGER_IMPLEMENTATION_AUTHORIZED=NO
PRIVATE_PRODUCTION_SOURCE_IMPLEMENTATION_AUTHORIZED=NO
```

AT8F tests may use synthetic identifiers only. Real private CRM identifiers
must not appear in repository source, fixtures, tests, logs, or this
authorization artifact. No Secret Manager or private production source
implementation is authorized.

## 5. Provider / mutation denials

```text
THIRD_CONTACT_GET_AUTHORIZED=NO

HIGHLEVEL_ACCESS=NO
HIGHLEVEL_NETWORK_CALLS=0
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0

CREDENTIAL_ACCESS=NO
CREDENTIAL_USE=NO
SECRET_ACCESS=NO

IAM_CHANGE=NO
SECRET_CHANGE=NO
DEPLOYMENT_CHANGE=NO

LIVE_READ_AUTHORIZED=NO
LIVE_MUTATION_AUTHORIZED=NO
LIVE_NOTE_WRITE_AUTHORIZED=NO

NETWORK_CLIENT_IMPLEMENTATION_AUTHORIZED=NO
```

## 6. Store-integration boundary

AT8D validated that `At1ExecutionStore` can be reused unchanged as the durable
NOTE_CREATE reservation primitive. That fit finding is not this grant.

```text
AT1_EXECUTION_STORE_REUSE_FIT=YES_UNCHANGED
AT1_STORE_ADAPTATION_IMPLEMENTATION_AUTHORIZATION_REQUIRED=NO

NOTE_PATH_STORE_INTEGRATION_REQUIRED=YES
NOTE_PATH_STORE_INTEGRATION_IMPLEMENTATION_AUTHORIZED_BY_AT8E=NO
NOTE_PATH_STORE_INTEGRATION_IMPLEMENTATION_AUTHORIZATION_REQUIRED=YES
```

AT8E/AT8F must not modify or integrate:

- `src/integrations/ghl/at1_execution_store.py`
- `src/integrations/ghl/at1_live_transport_adapter.py`

unless a later separate authorization explicitly allows it.

```text
AT1_EXECUTION_STORE_MODIFICATION_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_ADAPTER_REUSE_AUTHORIZED=NO
AT1_LIVE_TRANSPORT_ADAPTER_MODIFICATION_AUTHORIZED=NO
```

## 7. Test factory boundary

```text
AT8_SHAPED_TEST_FACTORY_AUTHORIZED_FOR_REAL_PRIVATE_BINDING=NO
CALLER_PUBLIC_CAPABILITY_CONSTRUCTION=FORBIDDEN
CALLER_SUPPLIED_TRUSTED_SOURCE=FORBIDDEN
PUBLIC_BOOLEAN_PROMOTION=FORBIDDEN
```

The synthetic AT8-shaped test factory must remain synthetic-test-only. Callers
must not publicly construct a trusted capability, inject a trusted source, or
promote a public boolean into trust.

## 8. AT8F writable prefixes

When this grant is effective and consumed by the named unit only:

```text
WRITABLE_IMPLEMENTATION_PATHS=src/integrations/ghl/highlevel_rest/**;tests/integrations/ghl/highlevel_rest/**;fixtures/ghl/highlevel_rest/**
WRITABLE_PATH_COUNT_PREFIXES=3
WRITABLE_PATH_PREFIX_1=src/integrations/ghl/highlevel_rest/
WRITABLE_PATH_PREFIX_2=tests/integrations/ghl/highlevel_rest/
WRITABLE_PATH_PREFIX_3=fixtures/ghl/highlevel_rest/
```

No other path is authorized for AT8F.

```text
STAGE_PATH_WRITABLE=NO
APPS_SCRIPT_WRITABLE=NO
DEPLOY_INFRA_WRITABLE=NO
SECRETS_CREDENTIALS_WRITABLE=NO
WORKFLOW_WRITABLE=NO
CONTRACT_WRITABLE=NO
ARCHITECTURE_WRITABLE=NO
PROOF_WRITABLE=NO
GOVERNANCE_WRITABLE_BY_AT8F=NO
AT1_EXECUTION_STORE_WRITABLE=NO
AT1_LIVE_TRANSPORT_ADAPTER_WRITABLE=NO
```

This authorization PR itself may change only:

```text
AUTHORIZATION_PR_WRITABLE_PATHS=governance/authorizations/nw008-at8e-ghl-rest-private-at8-capability-handoff-implementation-authorization-001.md
```

## 9. Required AT8F tests

AT8F must prove all of the following with deterministic synthetic tests and
keep all existing NOTE_PATH tests green:

```text
VALID_PRIVATE_BINDING_HANDOFF_SHAPE=PASS
AT8_PROVENANCE_MISMATCH_BLOCKS=PASS
WRONG_CONSUMER_AUTHORIZATION_BLOCKS=PASS
WRONG_WORKFLOW_RUN_BLOCKS=PASS
WRONG_WORKFLOW_ID_BLOCKS=PASS

CALLER_FORGED_CAPABILITY_BLOCKS=PASS
PUBLIC_TRUSTED_SOURCE_INJECTION_BLOCKS=PASS
SYNTHETIC_TEST_FACTORY_REAL_ID_USE_BLOCKS=PASS

PRIVATE_BINDING_PUBLICATION=NO

NO_PROVIDER_GET=PASS
NETWORK_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

## 10. Authorization does not include

This grant does not include:

- `At1ExecutionStore` integration
- `At1ExecutionStore` adaptation
- live HTTP transport
- HighLevel credential loading
- Secret Manager loading
- real private-ID retrieval
- contact GET
- note POST
- note readback
- stage transition
- deployment
- live proof

```text
IMPLEMENTATION_DOES_NOT_AUTHORIZE_LIVE_MUTATION=YES
LIVE_MUTATION_REQUIRES_SEPARATE_HUMAN_GRANT=YES
LIVE_MUTATION_AUTHORIZATION_READY=NO
AT8F_STARTED_BY_AT8E=NO
```

## 11. Stop

```text
HIGHLEVEL_ACCESS=NO
CRM_NETWORK_CALLS=0
CRM_MUTATIONS=0
LIVE_MUTATION_AUTHORIZED=NO
NOTE_PATH_STORE_INTEGRATION_IMPLEMENTATION_AUTHORIZED_BY_AT8E=NO
AUTHORIZATION_CONSUMPTION_MODE=ONE_SHOT
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO
AUTHORIZED_CONSUMER_UNIT=NW008_AT8F_GHL_REST_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_001
GRANT=PRIVATE_AT8_VERIFIED_BINDING_CAPABILITY_HANDOFF_OFFLINE_IMPLEMENTATION
IMPLEMENTATION_MODE=OFFLINE_ONLY

STOP_CODE=NW008_AT8E_PRIVATE_AT8_CAPABILITY_HANDOFF_IMPLEMENTATION_AUTHORIZATION_READY_FOR_REVIEW
```
