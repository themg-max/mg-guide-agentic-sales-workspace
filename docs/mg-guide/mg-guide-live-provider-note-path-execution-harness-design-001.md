# MG Guide Live Provider NOTE_PATH Execution Harness Design 001

## 0. Record identity and scope

```text
RECORD_ID=MG_GUIDE_LIVE_PROVIDER_NOTE_PATH_EXECUTION_HARNESS_DESIGN_001
ARTIFACT_PATH=docs/mg-guide/mg-guide-live-provider-note-path-execution-harness-design-001.md
PR_CLASS=design_only
MODE=DESIGN_PLANNING_ONLY
OWNER=VS_CODE_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-31T18:40:00Z
BASE_MAIN_SHA=a118d29b67b74830ac3d811494c0d3d8ee247bd2
STATUS_AT_AUTHORING=PROPOSED_PENDING_INDEPENDENT_REVIEW
```

This unit produces an implementation contract only. It accesses no Secret
Manager payload, invokes no HighLevel route, mutates no CRM record, changes no
IAM, and neither deploys nor alters the Reasoning Engine. No implementation
file is created by this unit.

```text
SECRET_PAYLOAD_READS=0
GHL_CALLS=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
REASONING_ENGINE_MUTATIONS=0
IMPLEMENTATION_FILES_CREATED=0
```

## 1. The discovered gap

```text
HOSTED_REASONING_ENGINE_ID=5719342828341952512
HOSTED_RUNTIME_LIVE_GHL_ENABLED=NO
HOSTED_RUNTIME_EXTERNAL_EFFECTS=0

LIVE_GHL_EXACT_GET_PREVIOUSLY_PROVEN=YES
LIVE_GHL_NOTE_POST_PREVIOUSLY_PROVEN=NO
LIVE_GHL_NOTE_READBACK_PREVIOUSLY_PROVEN=NO

DURABLE_PROVIDER_EXECUTION_ENTRYPOINT_PRESENT=NO
DURABLE_PROVIDER_OPERATOR_RUNBOOK_PRESENT=NO
PRIOR_SUCCESSFUL_GET_USED_EPHEMERAL_OPERATOR_SCRIPT=YES
```

### 1.1 Verified evidence for each gap claim

Verified against `a118d29` rather than accepted on assertion:

```text
FIVE_REUSE_MODULES_PRESENT=YES
  src/integrations/ghl/highlevel_rest/live_note_runtime.py
  src/integrations/ghl/highlevel_rest/live_note_credential_provider.py
  src/integrations/ghl/highlevel_rest/live_note_http_client.py
  src/integrations/ghl/highlevel_rest/live_note_transport.py
  src/integrations/ghl/highlevel_rest/note_path.py

PROPOSED_EXECUTOR_MODULE_ABSENT=YES (live_note_execution.py does not exist)
DOCS_MG_GUIDE_DIRECTORY_EXISTED_BEFORE_THIS_UNIT=NO (created by this artifact)
DOCS_RUNBOOKS_DIRECTORY_PRESENT=NO

EXISTING_WORKFLOWS=3
  .github/workflows/nw008-at1-ghl-identity-diagnostic.yml
  .github/workflows/nw008-at1-secret-access-diagnostic.yml
  .github/workflows/phase1-deterministic.yml
NOTE_PATH_WORKFLOW_PRESENT=NO
```

The prior live exact-contact GET is evidenced by
`proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md`:
`EXACT_CONTACT_GET_EXECUTED=YES`, `CONTACT_ID_MATCH=YES`,
`LOCATION_ID_MATCH=YES`, `LIVE_READ_VERIFIED=YES`, `NETWORK_CALL_COUNT=1`,
`MUTATION_CALL_COUNT=0`.

### 1.2 Correction to the requesting packet

```text
PACKET_LABEL=LIVE_GHL_V2_EXACT_GET_PREVIOUSLY_PROVEN
PACKET_LABEL_ACCURATE=NO
CORRECTED_LABEL=LIVE_GHL_V3_EXACT_GET_PREVIOUSLY_PROVEN
```

The requesting packet labels the proven GET as `V2`. The merged execution proof
records `API_VERSION=v3` and `EXPECTED_SCOPE=contacts.readonly`, and the
governing provider contract is `contracts/highlevel_rest_adapter_v1.yaml`
("HighLevel REST v3"). The proven route is v3. The `V2` label is not
propagated into this design. (The unrelated string "MG_Guide API v2.0" appears
in PIT scope-attestation artifacts as the *integration product* name, not the
REST API version; the two must not be conflated.)

### 1.3 Second gap not named by the requesting packet

```text
HOSTED_OUTPUT_TO_NOTE_CONTRACT_ADAPTER_PRESENT=NO
```

`note_contract` is only ever *consumed* inside `note_path.py`
(`_validate_note_contract`, `_serialize_note`, `_logical_digest`) and is
constructed ad hoc in tests. No merged code maps either the hosted
`follow_up_planning_agent` output or `fixtures/transcript-success.expected.json`
into a `note_contract`. Section 5's attribution gate is therefore not merely a
check to add — it requires a genuinely new mapping component, specified in
5.2. Any implementation authorization that omits this component cannot satisfy
the gate.

## 2. Execution surface decision

```text
TARGET_EXECUTION_SURFACE=MANUAL_GITHUB_ACTIONS_WORKFLOW_DISPATCH
REASONING_ENGINE_DIRECT_CRM_WRITE=NO
```

Rationale, each element verified in merged code or merged proof:

```text
WIF_PATH_PROVEN=YES
  provider projects/831270426395/locations/global/workloadIdentityPools/
  github-actions-pool-v2/providers/mg-guide-github-provider-v1
  (nw008-at1-secret-access-diagnostic.yml; pinned as
  _EXPECTED_WORKLOAD_IDENTITY_AUDIENCE in live_note_runtime.py)

SOURCE_WORKFLOW_SA_PROVEN=YES (_EXPECTED_SOURCE_PRINCIPAL)
NOTE_RUNTIME_SA_IMPERSONATION_PROVEN=YES
  (_impersonate_target_runtime_credentials, reused by secret_access_diagnostic)
EXACT_SECRET_MANAGER_ACCESS_PROVEN=YES
  (GoogleSecretManagerLiveNoteSecretAccessor pinned to the exact version)
CREDENTIAL_FILE_CLEANUP_PROVEN=YES
  (explicit delete + absence verification + residual scan, workspace and
  symlink guards, RUNNER_DISPOSAL_RELIED_UPON=NO)
ONE_SHOT_AND_AUDITABLE=YES (workflow_dispatch, single job, immutable run log)
```

The Reasoning Engine is deliberately **not** the CRM-writing surface. It holds
no HighLevel credential, its runtime service account
(`mg-guide-agent-runtime@`) is not the note-runtime identity, and granting it
provider write capability would broaden a hosted, always-on surface to carry a
one-shot mutation authority. The hosted fleet supplies *content*; the gated
workflow performs the *effect*.

## 3. Preserved credential chain

```text
SOURCE_WORKFLOW_IDENTITY=mg-guide-ghl-workflow@ai-rolodex-to-crm.iam.gserviceaccount.com
TARGET_NOTE_RUNTIME_IDENTITY=mg-guide-ghl-note-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com
GHL_SECRET_VERSION_RESOURCE=projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/2

SERVICE_ACCOUNT_KEYS_ALLOWED=NO
AMBIENT_ADC_FALLBACK_ALLOWED=NO
SECRET_VALUE_LOGGING_ALLOWED=NO
SECRET_VALUE_CLI_ARGUMENT_ALLOWED=NO
SECRET_VALUE_WORKFLOW_INPUT_ALLOWED=NO
SECRET_VALUE_ENV_EXPORT_ALLOWED=NO
```

All three identity/resource values are already pinned as module constants in
merged code (`_EXPECTED_SOURCE_PRINCIPAL`,
`_TARGET_RUNTIME_SERVICE_ACCOUNT`,
`DESIGNATED_LIVE_NOTE_SECRET_VERSION_RESOURCE` /
`_SEALED_LIVE_NOTE_REST_RESOURCE_NAME`). The harness must **not** re-declare,
parameterize, or override them; it consumes them. `read_secret_payload`
already rejects any non-designated `resource_name`, and
`GoogleSecretManagerLiveNoteSecretAccessor` already refuses construction
without an explicitly credentialed client, which is what forecloses ambient
ADC.

Credential transport into the process is by **file path**, never value:

```text
MG_GUIDE_NW008_GHL_WORKFLOW_CREDENTIAL_CONFIG=<credentials_file_path>
  (google-github-actions/auth@v2 with
   create_credentials_file: "true"
   cleanup_credentials: "false"     # explicit cleanup instead, verified
   export_environment_variables: "false")  # forecloses ambient ADC
```

`CHAIN_UNCHANGED_BY_THIS_DESIGN=YES` — no new principal, no new secret, no new
role, no new binding is proposed.

## 4. Implementation surface

```text
PROPOSED_MODULE=src/integrations/ghl/highlevel_rest/live_note_execution.py
PROPOSED_TESTS=tests/integrations/ghl/highlevel_rest/test_live_note_execution.py
PROPOSED_WORKFLOW=.github/workflows/mg-guide-live-provider-note-path.yml
PROPOSED_RUNBOOK=docs/runbooks/mg-guide-live-provider-note-path-operator-runbook.md

MANDATORY_REUSE=live_note_runtime, live_note_credential_provider,
                live_note_http_client, live_note_transport, note_path
SECOND_REST_TRANSPORT_ALLOWED=NO
NEW_HTTP_CLIENT_ALLOWED=NO
NEW_CREDENTIAL_ACCESSOR_ALLOWED=NO
NEW_NOTE_SERIALIZER_ALLOWED=NO
NEW_DIGEST_FUNCTION_ALLOWED=NO
```

### 4.1 What already exists (must be consumed, not reimplemented)

The production assembly path is complete from a private binding reference to a
wired adapter. `assemble_bound_live_note_runtime()` already performs, in order:
capability consumption and validation, root-owned dependency resolution
(source credential materialization → note-runtime impersonation → Secret
Manager client → exact-version secret accessor → credential injection →
commitment key → execution store), then constructs `BoundedLiveNoteTransport`
and `NotePathAdapter`, with store-ownership cleanup on failed assembly.

```text
def assemble_bound_live_note_runtime(
    *, private_binding_reference, consumer_authorization_identity,
    consumer_workflow_run_id, private_owner_resolver=None,
    private_owner_anchor=None) -> NotePathAdapter
```

Operation surface already present on the adapter and transport:

```text
STEP_1  note_path.<trust issuer>.build_bound_contact_get()(adapter)
          GET /contacts/{bound_contact_id} -> {"id", "locationId"}
STEP_2  adapter.create_meeting_note(note_contract) -> CreatedMeetingNote
          (note_id, note_content_digest, provider_body_digest)
STEP_3  adapter.verify_meeting_note() -> VerifiedMeetingNote
          (note_id, note_content_digest, provider_body_digest)

COUNTERS BoundedLiveNoteTransport.contact_get_attempts, post_attempts,
         post_successes, get_attempts, total_network_calls,
         total_mutation_calls
SANITIZER PublicProviderErrorProjection.as_public_dict()
```

### 4.2 Structural precondition already enforced in code

`build_bound_contact_get` compares the returned `id` and `locationId` against
the adapter's bound values, raises `BindingError` on either mismatch, sets
`CONTACT_PREFLIGHT_VERIFIED="YES"`, and only then issues the verified contact
binding capability that the note POST requires. The STEP_1 → STEP_2 fail-closed
ordering is therefore enforced structurally, not merely by operator discipline.
The harness must not weaken this by pre-seeding or synthesizing a capability;
`_assemble_bound_live_note_runtime_for_tests` and
`issue_synthetic_test_capability` are test seams and must remain unreachable
from the production entrypoint.

### 4.3 What the executor module must add (and only this)

```text
E1 process entrypoint (python -m integrations.ghl.highlevel_rest.live_note_execution)
E2 RUN_ID / activation-window / governance-binding preflight (fail closed)
E3 hosted-fleet attribution gate (Section 5)
E4 hosted-output -> note_contract mapping (Section 5.2)
E5 frozen-digest comparison against the merged Consumption Record values
E6 ordered 3-call drive of the existing adapter (Section 7)
E7 sanitized terminal report emission (Section 8)
E8 non-zero exit on any gate failure, before any secret access where applicable
```

`E4` is new logic, not reuse, and is the single largest correctness risk in the
implementation unit; it must be specified and tested offline before any live
authorization.

## 5. Hosted-fleet attribution gate

```text
GATE_ORDER=STRICTLY_BEFORE_PROVIDER_SECRET_ACCESS_AND_BEFORE_ANY_DISPATCH
REQUIRED_AGENT_SEQUENCE=meeting_context_agent
                        relationship_context_agent
                        follow_up_planning_agent
HOSTED_SERVING_OBJECT=AdkApp (deployment/agent-runtime/app/agent.py,
                              agent_runtime_app = agent_engines.AdkApp(...))
HOSTED_OPERATION=stream_query
INPUT=fixtures/transcript-success.txt
INPUT_CLASS=SYNTHETIC_APPROVED_FIXTURE

ON_MISMATCH:
  PROVIDER_SECRET_READ_ALLOWED=NO
  PROVIDER_DISPATCH_ALLOWED=NO
  STOP=HOSTED_FLEET_CONTRACT_MISMATCH
```

The gate must require all three agents to have executed in order and the
hosted output to resolve to the frozen note contract. A hosted response that
is merely non-empty is not sufficient; absence of per-agent evidence is a
mismatch, not a pass.

### 5.1 Frozen comparison values

```text
TRANSCRIPT_SHA256=1a1a002eb79701d436d199a63ddba0f8e532dd96d1591cc437157e90481a24aa
NOTE_CONTENT_LOGICAL_SHA256=4d581696b2b60a6fbdccef2ea8532ecdfe98f967496fac3f6942103b94626ac2
NOTE_BODY_SHA256=a404ad7343269ea8832618c6be70320ddc5403bf146c04a9e606e148746e0db5
PROVIDER_BODY_SHA256=fbf03c4e76911679980c8956ad93c26510f77cef51c2b0b48c5d46c11f774286
SOURCE=merged Consumption Record 002 (PR 423)
COMPARISON=EXACT_STRING_EQUALITY
TOLERANT_OR_PARTIAL_MATCH_ALLOWED=NO
```

### 5.2 Required hosted-output → note_contract mapping contract

The adapter must produce exactly the ten required fields, no more and no
fewer — `_validate_note_contract` rejects any field set that is neither
exactly `_REQUIRED_FIELDS` nor exactly required-plus-optional, and
`_OPTIONAL_FIELDS` is currently empty:

```text
SYNTHETIC_MARKER      == "implementation_reviewed_synthetic_marker" (exact)
workflow_id           == "meeting_follow_up_v1" (exact)
meeting_id            non-empty string
meeting_summary       string
needs                 array of strings
objections            array of strings
commitments           array of objects; each exactly {owner, action} or
                      {owner, action, due_date}; owner/action non-empty strings
next_step             object or null
opportunity_signal    object or null
transcript_hash       64-char lowercase SHA-256 hex
```

Mapping rules the implementation unit must honour:

```text
MAPPING_IS_PURE_AND_DETERMINISTIC=YES
MAPPING_INPUT=hosted follow_up_planning_agent structured output
MAPPING_MAY_INVENT_CONTENT=NO
MAPPING_MAY_DEFAULT_MISSING_REQUIRED_FIELDS=NO
MAPPING_MAY_REORDER_LIST_CONTENT=NO   # canonicalization belongs to note_path
MAPPING_MAY_TRUNCATE_OR_SUMMARIZE=NO
UNMAPPABLE_OR_MISSING_FIELD=FAIL_CLOSED_BEFORE_SECRET_ACCESS
SYNTHETIC_MARKER_AND_WORKFLOW_ID_SOURCED_FROM_note_path_CONSTANTS=YES
transcript_hash_RECOMPUTED_FROM_FIXTURE_BYTES=YES
```

Serialization, canonical JSON, NFC normalization, and all digests remain
`note_path`'s responsibility. The mapper produces a `Mapping`; it must not
build a body string or compute a digest.

### 5.3 Offline provability requirement

```text
MAPPING_MUST_BE_PROVEN_OFFLINE_BEFORE_LIVE_AUTHORIZATION=YES
OFFLINE_PROOF=derive note_contract from the approved fixture and assert the
              resulting logical/body/provider digests equal the Section 5.1
              frozen values, with zero network calls and zero secret reads
```

If the offline derivation cannot reproduce the frozen digests, the live
authorization must not be requested: a mismatch discovered at live time would
consume authority for a defect already discoverable offline.

## 6. Target-binding contract

```text
RAW_IDS_AS_CLI_PARAMETERS=FORBIDDEN
RAW_IDS_AS_WORKFLOW_DISPATCH_INPUTS=FORBIDDEN
RAW_IDS_COMMITTED_TO_PUBLIC_REPO=FORBIDDEN
RAW_IDS_IN_LOGS_OR_PROOF=FORBIDDEN
CALLER_TARGET_OVERRIDE_ALLOWED=NO
INPUT_CLASSIFICATION=OPERATOR_PROOF_INPUT
CONTEST_BUILD_DEPLOY_RUNTIME_DEPENDENCY=NO
```

### 6.1 Single ingress mechanism (reuse, do not invent)

The merged code already defines exactly one root-owned ingress, and the design
adopts it unchanged:

```text
ENV_KEY=MG_GUIDE_NW008_PRIVATE_OWNER_ORIGIN_MODULE
ROOT_COMPOSER=live_note_runtime.compose_root_owned_private_origin()
BINDER=note_path._bind_root_composed_private_origin(module)
CONSUMER=live_note_runtime._consume_root_owned_private_binding_reference(...)
VALIDATOR=note_path._require_issued_verified_capability(...)
LEASE_SEMANTICS=materialize -> consume (single use)
```

Two properties of the merged implementation are load-bearing and must not be
relaxed: the root honours only an **already-imported** module and never
imports one on a caller's behalf; and capability expectations are supplied
explicitly rather than derived from the submitted capability, so a capability
cannot vouch for its own authorization identity or workflow run.

### 6.2 Ephemeral materialization and destruction

```text
MATERIALIZATION_OWNER=ROOT_OPERATOR
MATERIALIZATION_SOURCE=existing private synthetic allowlist
MATERIALIZATION_LOCATION=ephemeral, outside the repository working tree
MATERIALIZATION_LIFETIME=single workflow run
DESTRUCTION_REQUIRED=YES
DESTRUCTION_VERIFICATION_REQUIRED=YES
DESTRUCTION_MODEL=mirror the proven credential-file cleanup step
                  (explicit delete, path guard, symlink guard,
                   post-delete absence assertion, residual scan,
                   RUNNER_DISPOSAL_RELIED_UPON=NO)
COMMITTED_TO_REPO=NO
PERSISTED_AS_WORKFLOW_ARTIFACT=NO
ECHOED_TO_LOGS=NO
```

The private material must be classified in the runbook as
`OPERATOR_PROOF_INPUT`: it gates a one-shot operator proof and must never
become a dependency of the contest build, the deployment, or the hosted
runtime. Absence of the material must fail the run closed with no dispatch, not
degrade to a caller-supplied identifier.

## 7. Frozen provider sequence

```text
1  GET  /contacts/{bound_contact_id}
2  POST /contacts/{bound_contact_id}/notes            body field only
3  GET  /contacts/{bound_contact_id}/notes/{same_run_note_id}

MAX_PROVIDER_CALLS=3
MAX_CONTACT_GET_ATTEMPTS=1
MAX_NOTE_CREATE_ATTEMPTS=1
MAX_NOTE_READBACK_ATTEMPTS=1
MAX_TOTAL_GHL_MUTATIONS=1

NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_FALLBACK=YES
NO_COMPENSATING_MUTATION=YES
NO_STAGE_MUTATION=YES
NO_GENERIC_EXECUTE=YES
QUERY_PARAMETERS=NO
REDIRECT_FOLLOWING=NO
```

The readback note ID must come from the same-run create response only. A
readback must never be attempted with an ID recovered by search, list, or
inference, and an uncertain create result must not be resolved by looking for
the note.

```text
STAGE_PATH_AUTHORIZED=NO
STAGE_PATH_BLOCKER=MINIMUM_VALID_UPDATE_OPPORTUNITY_BODY_UNRESOLVED
GET_OPPORTUNITY_ALLOWED=NO
UPDATE_OPPORTUNITY_STAGE_ALLOWED=NO
```

## 8. Safe output contract

Permitted in executor output and public proof:

```text
RUN_ID, timestamps, agent sequence status, HTTP status classes,
contact_match YES/NO, location_match YES/NO, note_id_present YES/NO,
note_contact_match YES/NO, body_digest_match YES/NO,
provider call count, mutation count, terminal result
```

Forbidden in executor output and public proof:

```text
PIT or bearer token (any form, including prefixes or lengths)
credential file contents or path contents
raw contact ID
raw location ID
raw note ID
full provider response body
private binding file contents
transcript-derived customer content
```

```text
DEFAULT=DENY   # emit only explicitly enumerated fields
RAW_RESPONSE_LOGGING=NO
AUTH_HEADER_LOGGING=NO
EXCEPTION_TRACEBACK_TO_PUBLIC_LOG=NO
SANITIZER_REUSE=PublicProviderErrorProjection.as_public_dict()
DIGESTS_EMITTED_AS=MATCH_BOOLEAN_ONLY_OR_ALREADY_PUBLIC_FROZEN_VALUE
NOTE_ID_EMITTED_AS=note_id_present YES/NO
```

Emitting a match boolean rather than a value is required even where the value
appears harmless: a raw note ID is a private-binding-adjacent identifier, and
the frozen digests are already public, so a boolean carries the full proof
value with no disclosure.

## 9. Open risks the implementation authorization must resolve

These are recorded because they materially affect whether a one-shot live run
can succeed, and one-shot authority is consumed on attempt, not on success.

```text
R1 CONTACTS_WRITE_SCOPE_NEVER_EXERCISED_OVER_NETWORK
   contacts.write is attested present, but by human console review
   (SCOPE_EVIDENCE_SOURCE=HUMAN_VERIFIED_MG_GUIDE_API_V2_PRIVATE_INTEGRATION_
   SCOPE_CONFIGURATION, SCOPE_VERIFICATION_METHOD=HUMAN_OWNER_CONSOLE_REVIEW_
   RECORDED_BY_ORCHESTRATOR). The proven live call used contacts.readonly.
   The authorized create_note POST would therefore be the first live write
   ever attempted with this PIT. A 401/403 scope failure consumes the
   authority and produces no note.
   MITIGATION_OPTIONS=(a) accept possible authority burn explicitly in the
   authorization; (b) re-attest scope at the owner console immediately before
   activation; (c) authorize an explicitly-labelled scope-probe attempt whose
   failure is a recognised non-defect outcome.
   RESOLUTION_REQUIRED_BEFORE_LIVE_AUTHORIZATION=YES

R2 HOSTED_OUTPUT_SHAPE_UNPROVEN_AGAINST_NOTE_CONTRACT
   No merged code maps hosted output to note_contract (1.3). Whether the
   hosted follow_up_planning_agent output can populate all ten required
   fields deterministically is unverified.
   RESOLUTION=offline derivation reproducing the Section 5.1 digests (5.3)
   RESOLUTION_REQUIRED_BEFORE_LIVE_AUTHORIZATION=YES

R3 ACTIVATION_002_WINDOW_EXPIRY
   Activation 002 / Consumption Record 002 bind RUN_ID
   mg-guide-live-provider-note-path-002-20260831T175220Z-c780 to a window
   ending 2026-08-31T18:47:20Z. No harness can exist and be reviewed within
   that window, so that RUN_ID cannot be the one that executes.
   CONSEQUENCE=Activation 002 and Consumption Record 002 will require the
   same expiry / non-consumption reconciliation applied to Activation 001
   (PR 421) before any successor activation is created.
   ACTIVATION_002_REUSABLE=NO
   WINDOW_EXTENDABLE=NO

R4 NO_LIVE_WRITE_HAS_EVER_RUN_ON_THIS_SURFACE
   The chosen workflow surface is proven for identity, impersonation, and
   secret access, but has never carried a provider mutation.
   MITIGATION=the workflow and executor must be exercised end to end with the
   fake transport and a synthetic accessor in CI before live authorization.
```

## 10. Implementation authority

```text
IMPLEMENTATION_AUTHORIZED_NOW=NO
LIVE_EXECUTION_AUTHORIZED_NOW=NO
DESIGN_MERGE_ALONE_AUTHORIZES_IMPLEMENTATION=NO
DESIGN_MERGE_ALONE_AUTHORIZES_EXECUTION=NO
SELF_AUTHORIZATION=FORBIDDEN

NEXT=FRESH_BOUNDED_IMPLEMENTATION_AUTHORIZATION_FOR_EXECUTION_HARNESS
```

The implementation authorization must bind this design, enumerate the exact
four file paths from Section 4, require offline proof per 5.3, and resolve R1
and R2. It must not carry live-provider execution authority: implementing the
harness and running it are separate acts requiring separate chains.

## 11. Prohibited effects (this unit)

```text
SECRET_MANAGER_PAYLOAD_ACCESS=NO
HIGHLEVEL_INVOCATION=NO
CRM_MUTATION=NO
IAM_MUTATION=NO
DEPLOYMENT=NO
REASONING_ENGINE_ALTERATION=NO
TERRAFORM_APPLY=NO
IMPLEMENTATION_CREATION=NO
AUTHORITY_GRANTED_TO_A_LATER_PHASE=NO
```

## 12. Stop

```text
IMPLEMENTATION_AUTHORIZED_NOW=NO
LIVE_EXECUTION_AUTHORIZED_NOW=NO
STOP=INDEPENDENT_REVIEW_REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION
```
