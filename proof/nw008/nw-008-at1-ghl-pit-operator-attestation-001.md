# NW-008 AT1 GHL PIT Operator Attestation 001

## 0. Artifact identity

```text
ARTIFACT_ID=
  NW008_AT1_GHL_PIT_OPERATOR_ATTESTATION_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-pit-operator-attestation-001.md
CLASSIFICATION=ZERO_CALL_HUMAN_OPERATOR_ATTESTATION_INSTRUMENT
PR_CLASS=proof_only
MODE=OPERATOR_SURFACE_ONLY_NO_PROVIDER_CONTACT
OWNER=HUMAN_HIGHLEVEL_OPERATOR + VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
PREPARED_AT_UTC=2026-08-30T00:00:00Z

GHL_API_CALLS=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_PAYLOAD_READS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
```

This unit is the **instrument** for a human HighLevel operator attestation. The
orchestrator prepared and bounded it. The orchestrator did **not** and could
not complete it: every predicate in section 4.2 is observable only on the
HighLevel operator surface, to which the orchestrator has no access. The values
recorded there were supplied by the human operator from console review.

```text
ORCHESTRATOR_COMPLETED_ATTESTATION=NO
ORCHESTRATOR_CAN_COMPLETE_ATTESTATION=NO
ATTESTATION_AUTHORITY=HUMAN_HIGHLEVEL_OPERATOR_ONLY
PREDICATE_VALUES_SUPPLIED_BY=HUMAN_HIGHLEVEL_OPERATOR
INFERRED_OR_ASSUMED_PREDICATE_VALUES=NONE

SCREENSHOTS_COMMITTED=NO
SCREENSHOT_EVIDENCE_RETAINED=PRIVATELY_BY_OPERATOR_OUT_OF_BAND
SCREENSHOT_EXCLUSION_REASON=
  CONSOLE_CAPTURES_CONTAIN_PRIVATE_IDENTIFIERS_AND_TOKEN_FRAGMENTS
TOKEN_MATERIAL_PUBLISHED=NO
RAW_LOCATION_ID_PUBLISHED=NO
```

## 1. Preflight — archive finding, RESOLVED via canonical clone

The artifact was originally authored in an unpacked archive with no Git. That
finding is retained below because it explains why authoring and publication are
separate events in this lane, and it is resolved in section 1.1.

```text
PWD=/Users/achandler/Downloads/mg-guide-agentic-sales-workspace-main
GIT_BRANCH_SHOW_CURRENT=
  fatal: not a git repository (or any of the parent directories): .git
GIT_STATUS_SHORT=
  fatal: not a git repository (or any of the parent directories): .git

IS_GIT_REPOSITORY=NO
GIT_DIR_PRESENT=NO
BRANCH_RESOLVABLE=NO
BRANCH_IS_MAIN=UNKNOWN_UNRESOLVABLE
WORKING_TREE_PROVENANCE=MAIN_BRANCH_ARCHIVE_EXPORT
  # directory basename "...-workspace-main" indicates a main-branch snapshot
GIT_ADD_DOT_USED=NO
```

The abort-if-main gate **cannot be evaluated**, because there is no branch to
evaluate. The tree is an unpacked main-branch archive: no `.git`, no index, no
branch, no remote, no upstream.

```text
COMMIT_POSSIBLE_HERE=NO
BRANCH_CREATION_POSSIBLE_HERE=NO
PR_CREATION_POSSIBLE_HERE=NO
REPOSITORY_MUTATION_PERFORMED=NO
```

Consequence, stated plainly: this artifact was authored into the local snapshot
only. It carries **no** durable repository evidence until it is placed in a real
clone, on a non-`main` branch, and opened as a PR. Nothing here has been staged,
committed, or pushed, and no `git add .` was used or could have been used.

```text
PREFLIGHT_RESULT=BLOCKED_FOR_REPOSITORY_MUTATION
PREFLIGHT_RESULT_FOR_AUTHORING=PROCEED_LOCAL_ONLY
```

### 1.1 Canonical clone located (read-only reconnaissance)

```text
CANONICAL_CLONE=
  /Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
CANONICAL_CLONE_IS_GIT_REPOSITORY=YES
ORIGIN_URL=
  https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
ORIGIN_MATCHES_EXPECTED_REPOSITORY=YES
FETCH_PRUNE_EXECUTED=YES
ORIGIN_MAIN_SHA=a9bf506bb93f9dcfdffa872a2abfa121ee6149dd
ORIGIN_MAIN_TIP_SUBJECT=
  proof(nw008): record bounded-read 003 terminal provider 403 (#365)
ORIGIN_MAIN_MATCHES_CURRENT_SOURCE_OF_TRUTH_PR_365=YES

GIT_INIT_INSIDE_ARCHIVE=NO
ARCHIVE_TREATED_AS_REPOSITORY=NO
WORKTREE_CREATED=NO
WORKTREE_CREATION_GATE=ATTESTATION_MUST_PASS_FIRST
```

The canonical clone's primary checkout is on a diagnostic branch with a dirty
working tree. It is left untouched, consistent with the standing mission-ledger
posture `SOURCE_WORKTREE_ACTION=LEAVE_UNTOUCHED`.

```text
PRIMARY_CHECKOUT_BRANCH=diagnostic/nw008-at1-ghl-runtime-source-principal-resolution-001
PRIMARY_CHECKOUT_BRANCH_IS_MAIN=NO
PRIMARY_CHECKOUT_DIRTY_PATH_COUNT=46
PRIMARY_CHECKOUT_MODIFIED_BY_THIS_UNIT=NO
PRIMARY_CHECKOUT_STAGED_BY_THIS_UNIT=NO
RECOVERY_METHOD=DEDICATED_WORKTREE_OFF_ORIGIN_MAIN
```

Target branch and path are free:

```text
TARGET_BRANCH=proof/nw008-at1-ghl-pit-403-diagnostic-and-attestation-001
TARGET_BRANCH_ALREADY_EXISTS=NO
TARGET_ARTIFACT_ON_ORIGIN_MAIN=NO
VERIFY_SCRIPT_PRESENT_ON_ORIGIN_MAIN=YES
  # scripts/verify_phase1_deterministic.py
```

### 1.2 Lane-order dependency — BLOCKING FINDING

Neither predecessor artifact authored in this lane has ever reached the
repository. Both exist only in the local archive:

```text
ROOT_CAUSE_DIAGNOSTIC_ON_ORIGIN_MAIN=NO
  proof/nw008/nw-008-at1-ghl-rest-v3-provider-403-root-cause-diagnostic-001.md
REPAIR_AUTHORIZATION_ON_ORIGIN_MAIN=NO
  governance/authorizations/nw008-at1-ghl-pit-credential-repair-authorization-001.md
```

Section 2 of this attestation cites the root-cause diagnostic by path. If this
attestation merges first, it cites a path that does not exist in the
repository, and a reviewer cannot verify its controlling diagnosis.

Mission `NW008_AT1_GHL_PIT_CREDENTIAL_REPAIR_AND_TRANSPORT_RECOVERY_001`
resolves this by carrying **both** proof artifacts in a single `proof_only`
PR, so the citation and its target land together.

```text
REQUIRED_LANE_ORDER=
  L1=PR_DIAGNOSTIC_001_AND_ATTESTATION_001  (one proof_only PR) -> merge
  L2=READ_ONLY_SECRET_VERSION_INVENTORY                (metadata only)
  L3=CREATE_AND_PR_REPAIR_AUTHORIZATION_001            -> review -> merge
  L4=FRESH_HUMAN_ACTIVATION                            (separate unit)
  L5=EXECUTE_ONE_SECRET_VERSION_ADD                    (separate unit)
  L6=RUNTIME_EXACT_VERSION_PINNING + TESTS             (separate unit)
  L7=AUTHORIZATION_004 + ACTIVATION_004 + FRESH_RUN_ID (separate unit)
  L8=EXACTLY_ONE_GET_CONTACTS_BOUNDED_READ             (separate unit)

DIAGNOSTIC_AND_ATTESTATION_SHARE_ONE_PR=YES
L3_BEFORE_L1_MERGE=FORBIDDEN
L5_BEFORE_L2_RESOLUTION=FORBIDDEN
```

### 1.3 Recovery command sequence (prepared, NOT executed)

To be run only after section 4.2 is completed and passes:

```text
R=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
W=$R.worktrees/nw008-at1-ghl-pit-403-diagnostic-and-attestation-001
B=proof/nw008-at1-ghl-pit-403-diagnostic-and-attestation-001

git -C "$R" fetch --prune origin
git -C "$R" worktree add -b "$B" "$W" origin/main

# in $W: pwd; git branch --show-current;
#        git status --short --untracked-files=all; git rev-parse HEAD;
#        git rev-parse origin/main
# require BRANCH_IS_MAIN=NO, WORKTREE_CLEAN_BEFORE_COPY=YES,
#         HEAD_EQUALS_ORIGIN_MAIN=YES

# copy ONLY the two finalized proof artifacts, then stage exact paths:
git -C "$W" add \
  proof/nw008/nw-008-at1-ghl-rest-v3-provider-403-root-cause-diagnostic-001.md \
  proof/nw008/nw-008-at1-ghl-pit-operator-attestation-001.md

git -C "$W" diff --check
PYTHONPATH=src python scripts/verify_phase1_deterministic.py
pytest
# require: no unexpected generated or modified paths after validation

GIT_ADD_DOT=FORBIDDEN
AUTHORIZATION_ARTIFACT_INCLUDED_IN_THIS_PR=NO
PR_CLASS=proof_only
```

The authorization draft is deliberately excluded from this PR. It is created
on its own branch at L3, after this proof merges.

The worktree sibling path follows the existing repository convention
(`<clone>.worktrees/<unit>`), so it never nests inside the dirty checkout.

## 2. Controlling diagnosis carried in

From `proof/nw008/nw-008-at1-ghl-rest-v3-provider-403-root-cause-diagnostic-001.md`:

```text
IDENTITY_CHAIN_HEALTHY=YES
SECRET_MANAGER_ACCESS_HEALTHY=YES
PRIVATE_TARGET_BINDING_HEALTHY=YES

FAILED_CREDENTIAL_RESOURCE=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1
CURRENT_FAILURE=HTTP_403
ROOT_CAUSE_CLASS=CREDENTIAL_AUTHORIZATION_REJECTION
ROOT_CAUSE=
  MG_GUIDE_PIT_GHL_VERSION_1_CREDENTIAL_NOT_ACCEPTED_FOR_THE_BOUND_GHL_CONTACT_READ
ROOT_CAUSE_CONFIDENCE=HIGH
SUB_CAUSE=UNKNOWN
```

This attestation resolves the sub-cause on the operator surface, with zero
provider requests.

```text
NEW_GHL_REQUEST_ISSUED_BY_THIS_UNIT=NO
EXECUTION_003_RETRIED=NO
AUTHORITY_CONSUMED_BY_THIS_UNIT=NONE
```

## 3. Credential boundary — canonical, and not to be repointed

```text
CANONICAL_MG_GUIDE_CREDENTIAL_BOUNDARY=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL

REPOINT_RUNTIME_TO_GHL_MCP_PRIVATE_TOKEN=FORBIDDEN
GHL_MCP_PRIVATE_TOKEN_ROLE=EVIDENCE_AND_LEGACY_CONTEXT_ONLY
GHL_MCP_PRIVATE_TOKEN_READ_BY_THIS_UNIT=NO
GHL_MCP_PRIVATE_TOKEN_MUTATED_BY_THIS_UNIT=NO
GHL_MCP_PRIVATE_TOKEN_ROTATED=NO
```

The prior diagnostic used `GHL_MCP_PRIVATE_TOKEN` only as historical evidence of
what a working credential looks like. It is not, and does not become, the MG
Guide runtime credential. The repair restores `MG_GUIDE_PIT_GHL` to a working
state rather than migrating away from it.

## 4. Operator attestation — TO BE COMPLETED BY THE HUMAN OPERATOR

### 4.1 Method constraints

```text
ALLOWED_SURFACE=HIGHLEVEL_UI_OPERATOR_CONSOLE_ONLY
ALLOWED_ACTIONS=VISUAL_INSPECTION_AND_COPY_TOKEN_TO_SECURE_CLIPBOARD
FORBIDDEN=HIGHLEVEL_API_CALL
FORBIDDEN=MCP_CALL
FORBIDDEN=CRM_RECORD_READ
FORBIDDEN=CRM_MUTATION
FORBIDDEN=TOKEN_PASTED_INTO_CHAT_TERMINAL_LOG_ISSUE_OR_PR
FORBIDDEN=TOKEN_WRITTEN_TO_ANY_REPOSITORY_FILE
```

### 4.2 Predicates — ESTABLISHED

Supplied by the human HighLevel operator from console visual review. The
orchestrator transcribed these values and inferred none of them.

```text
MG_GUIDE_PRIVATE_INTEGRATION_PRESENT=YES
MG_GUIDE_PRIVATE_INTEGRATION_ACTIVE=YES

BOUND_LOCATION_MATCH=YES
CONTACTS_READONLY_PRESENT=YES

TOKEN_CLASS=PRIVATE_INTEGRATION_TOKEN
  # required value: PRIVATE_INTEGRATION_TOKEN -> SATISFIED

TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION=YES

ATTESTED_BY=HUMAN_HIGHLEVEL_OPERATOR
ATTESTED_AT_UTC=2026-08-30T22:22:07Z
ATTESTATION_METHOD=HIGHLEVEL_OPERATOR_CONSOLE_VISUAL_REVIEW
```

`BOUND_LOCATION_MATCH=YES` was established by private fingerprint comparison
against the already-public canonical fingerprint in section 4.3 P3. The
identifier itself was not transmitted, recorded, or published.

### 4.2.1 Additional observed scope readiness — NOT an authorization

The operator additionally observed the following scopes on the same
integration. They are recorded as provider-state facts only.

```text
CONTACTS_WRITE_PRESENT=YES
OPPORTUNITIES_READONLY_PRESENT=YES
OPPORTUNITIES_WRITE_PRESENT=YES
LOCATIONS_READONLY_PRESENT=YES
```

These flags describe what the provider *would permit*. They confer no authority
whatsoever within this governance model, in which every CRM effect requires its
own reviewed authorization plus a separate fresh human activation.

```text
SCOPE_FLAGS_AUTHORIZE_CRM_MUTATION=NO
SCOPE_FLAGS_AUTHORIZE_CRM_READ=NO
SCOPE_FLAGS_AUTHORIZE_NOTE_CREATE=NO
SCOPE_FLAGS_AUTHORIZE_OPPORTUNITY_UPDATE=NO
SCOPE_PRESENCE_IS_NOT_AUTHORITY=YES

WRITE_SCOPE_FIRST_LEGITIMATE_USE=
  SEPARATELY_AUTHORIZED_AGENT_FLEET_ACCEPTANCE_UNIT
WRITE_SCOPE_USE_BEFORE_THAT=FORBIDDEN
```

Recording write-scope presence in a proof artifact is deliberate: a later
reviewer must be able to see that write capability existed and was *not* used,
rather than discovering it for the first time at the moment something writes.

### 4.3 How the operator establishes each predicate

```text
P1 MG_GUIDE_PRIVATE_INTEGRATION_PRESENT
   Open the HighLevel private-integrations list for the MG Guide sub-account.
   Confirm the MG_Guide API v2.0 private integration exists.

P2 MG_GUIDE_PRIVATE_INTEGRATION_ACTIVE
   Confirm it is enabled/active — not revoked, disabled, expired, or deleted.
   A present-but-revoked integration is the leading SUB_CAUSE candidate.

P3 BOUND_LOCATION_MATCH
   Confirm the integration is bound to the SAME sub-account/location that the
   NW-008 private binding targets. Verify by fingerprint, never by publishing
   the value: SHA-256 of the location identifier must equal
   5e14ac52bf73156914fc2a017415561e619f76f911c9e509316825f39c5fd614
   This fingerprint is already public in merged NW-008 artifacts.
   Record only YES or NO. Do not record the identifier.

P4 CONTACTS_READONLY_PRESENT
   Confirm the contacts.readonly scope is present on that integration.
   This is the exact scope the bounded read requires.

P5 TOKEN_CLASS
   Confirm the credential is a HighLevel Private Integration Token, not an
   OAuth access token, agency/company-level token, API key, or location key.

P6 TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION
   Confirm the operator can obtain the token value for this integration —
   either it is retrievable, or the operator can issue a fresh one on this
   same integration. Do not paste it anywhere at this stage.
```

### 4.4 Prohibited recordings — absolute

```text
TOKEN_VALUE_RECORDED=NO
TOKEN_PREFIX_RECORDED=NO
TOKEN_SUFFIX_RECORDED=NO
TOKEN_LENGTH_RECORDED=NO
TOKEN_HASH_RECORDED=NO
RAW_LOCATION_ID_RECORDED=NO
RAW_CONTACT_ID_RECORDED=NO
RAW_OPPORTUNITY_ID_RECORDED=NO

TOKEN_VALUE_PUBLISHED=NO
TOKEN_HASH_PUBLISHED=NO
```

Token length and token hash are prohibited even though they feel harmless: both
are distinguishers that narrow a credential, and a hash is directly checkable
against a guess.

## 5. Attestation gate

```text
REQUIRED_FOR_PASS=
  MG_GUIDE_PRIVATE_INTEGRATION_PRESENT=YES        -> YES  SATISFIED
  MG_GUIDE_PRIVATE_INTEGRATION_ACTIVE=YES         -> YES  SATISFIED
  BOUND_LOCATION_MATCH=YES                        -> YES  SATISFIED
  CONTACTS_READONLY_PRESENT=YES                   -> YES  SATISFIED
  TOKEN_CLASS=PRIVATE_INTEGRATION_TOKEN           -> MATCH SATISFIED
  TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION=YES -> YES SATISFIED

CURRENT_STATE=ALL_SIX_PREDICATES_ESTABLISHED
UNATTESTED_PREDICATES_REMAINING=0
ATTESTATION_RESULT=PASS

STOP=NONE
```

All six required predicates are established from human console evidence. The
attestation gate is **CLOSED AS PASS**.

### 5.0.1 What this PASS resolves, and what it does not

```text
SUB_CAUSE_REVOKED_OR_DISABLED_INTEGRATION=EXCLUDED   # P2=YES
SUB_CAUSE_WRONG_LOCATION_BINDING=EXCLUDED            # P3=YES
SUB_CAUSE_MISSING_CONTACTS_READONLY_SCOPE=EXCLUDED   # P4=YES
SUB_CAUSE_WRONG_TOKEN_CLASS_CONFIGURED=EXCLUDED      # P5=YES
SUB_CAUSE_NO_INTEGRATION_PROVISIONED=EXCLUDED        # P1=YES

RESIDUAL_SUB_CAUSE=
  STALE_OR_INCORRECT_TOKEN_MATERIAL_SEALED_IN
  MG_GUIDE_PIT_GHL/versions/1
RESIDUAL_SUB_CAUSE_CONFIDENCE=HIGH
```

This is the decisive narrowing. The integration is present, active, correctly
bound, correctly scoped, and of the correct token class — so the provider-side
configuration is sound, and the 403 is not explained by anything the operator
can see in the console. What remains is the one thing the console cannot show:
whether the bytes sealed into `MG_GUIDE_PIT_GHL/versions/1` are the bytes of
*this* integration's live token. The root-cause diagnostic already recorded
`LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN`; the attestation
converts that from one hypothesis among several into the only surviving one.

The repair therefore follows directly: rotate this integration's token and
seal the fresh value as a new secret version. Creating a new integration would
be the wrong repair — the attested one is correct.

```text
CORRECT_REPAIR=ROTATE_EXISTING_MG_GUIDE_INTEGRATION_TOKEN_AND_RESEAL
NEW_PRIVATE_INTEGRATION_REQUIRED=NO
PRIVATE_BINDING_EDIT_REQUIRED=NO
SCOPE_EDIT_REQUIRED=NO
REQUEST_CONTRACT_EDIT_REQUIRED=NO
```

### 5.0.2 Authority NOT conferred by this PASS

```text
SECRET_MUTATION_AUTHORIZED_BY_THIS_PASS=NO
TOKEN_ROTATION_AUTHORIZED_BY_THIS_PASS=NO
GHL_REQUEST_AUTHORIZED_BY_THIS_PASS=NO
RUNTIME_EDIT_AUTHORIZED_BY_THIS_PASS=NO
CRM_READ_OR_MUTATION_AUTHORIZED_BY_THIS_PASS=NO

THIS_ARTIFACT_IS=EVIDENCE_ONLY
NEXT_REQUIRED=SEPARATE_REVIEWED_AUTHORIZATION_PLUS_FRESH_HUMAN_ACTIVATION
```

### 5.1 Failure branches — retained, NONE TAKEN

All six predicates returned the required value, so no branch below was taken.
They are retained because they document what each failure would have meant, and
because a reviewer re-examining this attestation needs to see the alternatives
that were live at the time it was written.

```text
BRANCH_TAKEN=NONE
ALL_BRANCHES_BELOW_ARE_COUNTERFACTUAL=YES
```

```text
IF MG_GUIDE_PRIVATE_INTEGRATION_PRESENT=NO
  => the designated integration does not exist. The repair is not a new secret
     version; a private integration must first be created on the bound
     location. Escalate to a separate provisioning unit.

IF MG_GUIDE_PRIVATE_INTEGRATION_ACTIVE=NO
  => SUB_CAUSE resolved as REVOKED_OR_DISABLED_INTEGRATION. Reactivate or
     reissue on the same integration, then proceed to the secret repair.

IF BOUND_LOCATION_MATCH=NO
  => SUB_CAUSE resolved as WRONG_LOCATION_BINDING. Do NOT edit the NW-008
     private binding to chase the token — that binding is proven healthy.
     Escalate: the integration must be bound to the correct location, or a
     location-authority decision is required. This is a human governance call.

IF CONTACTS_READONLY_PRESENT=NO
  => contradicts the prior human scope review recorded in
     proof/nw008/nw-008-at1-write-credential-readiness.md. Treat the
     contradiction as the finding; reconcile before any secret mutation.

IF TOKEN_CLASS != PRIVATE_INTEGRATION_TOKEN
  => the runtime contract expects a PIT bearer. A different class requires a
     transport-contract decision, not a secret swap.

IF TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION=NO
  => issue a fresh PIT on the same integration. Do not substitute any other
     credential, and specifically not GHL_MCP_PRIVATE_TOKEN.
```

## 6. Verification block

```text
ATTESTATION_RESULT=PASS                  # required: PASS -> SATISFIED
BOUND_LOCATION_MATCH=YES                 # required: YES  -> SATISFIED
CONTACTS_READONLY_PRESENT=YES            # required: YES  -> SATISFIED
TOKEN_MATERIAL_AVAILABLE_FOR_ATTESTED_INTEGRATION=YES  # required: YES -> SATISFIED
GHL_API_CALLS=0                          # required: 0    -> SATISFIED
SECRET_MUTATIONS=0                       # required: 0    -> SATISFIED
SCREENSHOTS_COMMITTED=NO                 # required: NO   -> SATISFIED
TOKEN_MATERIAL_PUBLISHED=NO              # required: NO   -> SATISFIED
RAW_LOCATION_ID_PUBLISHED=NO             # required: NO   -> SATISFIED

VERIFY_RESULT=PASS
VERIFY_PENDING_HUMAN=NONE
```

The zero-effect and disclosure predicates are provable from this unit's own
ledger. The attestation predicates are provable only from human console review,
were supplied by the human operator, and were transcribed without inference.

## 7. Downstream — prepared, gated, not activated

```text
PREPARED_REPAIR_AUTHORIZATION=
  governance/authorizations/nw008-at1-ghl-pit-credential-repair-authorization-001.md
PREPARED_REPAIR_AUTHORIZATION_ID=
  NW008_AT1_GHL_PIT_CREDENTIAL_REPAIR_AUTHORIZATION_001
PREPARED_REPAIR_AUTHORIZATION_STATE=DRAFT_NOT_REVIEWED_NOT_ACTIVATED
PREPARED_REPAIR_AUTHORIZATION_INPUT_GATE=SATISFIED_BY_THIS_PASS
PREPARED_REPAIR_AUTHORIZATION_IN_THIS_PR=NO
```

Sequence, each step gated on the previous:

```text
S1=HUMAN_COMPLETES_THIS_ATTESTATION                   -> DONE (PASS)
S2=INDEPENDENT_REVIEW_AND_MERGE_OF_THIS_PROOF_PR      -> currently BLOCKING
S3=PREPARE_AND_REVIEW_PIT_ROTATION_AUTHORIZATION_001   (separate unit)
S4=FRESH_ACTIVATION + ONE_HUMAN_CONSOLE_TOKEN_ROTATION (separate unit)
S5=READ_ONLY_SECRET_VERSION_INVENTORY, THEN FREEZE      (metadata only)
S6=INDEPENDENT_REVIEW_OF_REPAIR_AUTHORIZATION_001      (separate unit)
S7=FRESH_HUMAN_ACTIVATION_OF_REPAIR_AUTHORIZATION_001  (separate unit)
S8=ADD_EXACTLY_ONE_MG_GUIDE_PIT_GHL_VERSION            (separate unit)
S9=RUNTIME_EXACT_VERSION_PINNING_TO_NEXT_EXPECTED_VERSION + TESTS (separate unit)
S10=FRESH_AUTHORIZATION_004 + ACTIVATION_004 + RUN_ID  (separate unit)
S11=EXACTLY_ONE_GET_CONTACTS_BOUNDED_READ              (separate unit)
```

No step beyond S2 is authorized by this artifact. Note that token rotation (S4)
now precedes the secret version add (S8): the value sealed into the new secret
version is the freshly rotated token, so the rotation must happen first.

## 8. Disclosure remediation — explicitly not mixed in

```text
RAW_LOCATION_ID_DISCLOSURE_FILE=
  docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
RAW_LOCATION_ID_DISCLOSURE_LINE=344
HANDLED_IN_THIS_UNIT=NO
MIXED_INTO_PIT_REPAIR=NO
DISPOSITION=SEPARATE_BOUNDED_REMEDIATION_UNIT_REQUIRED
GIT_HISTORY_REWRITE_PERFORMED=NO
GIT_HISTORY_REWRITE_PROPOSED_AUTOMATICALLY=NO
```

Deliberately untouched. The current-tree redaction and the public-proof-posture
correction belong to their own unit, and any historical removal is a human
governance decision that this lane must not pre-empt.

## 9. Effect ledger

```text
GHL_API_CALLS=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_READS=0
CRM_MUTATIONS=0
SECRET_MUTATIONS=0
SECRET_VERSIONS_ADDED=0
SECRET_VERSIONS_DISABLED=0
SECRET_VERSIONS_DESTROYED=0
SECRET_PAYLOAD_READS=0
SECRET_IAM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
RUNTIME_SOURCE_EDITS=0
TEST_EDITS=0
PROVIDER_STATE_MUTATIONS=0
TOKEN_ROTATIONS=0
AUTHORITY_CONSUMED=NONE
```

The ledger covers provider, secret, IAM, and runtime effects. This artifact is
itself committed as proof; that commit adds no such effect.

## 10. Disclosure boundary

```text
TOKEN_VALUE_PUBLISHED=NO
TOKEN_HASH_PUBLISHED=NO
TOKEN_PREFIX_OR_SUFFIX_PUBLISHED=NO
TOKEN_LENGTH_PUBLISHED=NO
RAW_LOCATION_ID_PUBLISHED=NO
RAW_CONTACT_ID_PUBLISHED=NO
RAW_OPPORTUNITY_ID_PUBLISHED=NO
SECRET_PAYLOAD_PUBLISHED=NO
AUTHORIZATION_HEADER_PUBLISHED=NO
```

The only correlation value restated is the location SHA-256 fingerprint, which
is already published in merged NW-008 artifacts.

## 11. Stop

```text
ATTESTATION_RESULT=PASS
STOP=NONE
ATTESTATION_GATE=CLOSED_AS_PASS

BLOCKING_ON=INDEPENDENT_REVIEWER_DISPOSITION_OF_THIS_PROOF_PR

NO_GHL_REQUEST_MADE
NO_SECRET_MUTATED
NO_TOKEN_ROTATED
NO_RUNTIME_REPOINTED
NO_SCREENSHOT_COMMITTED
NO_PROVEN_HEALTHY_BOUNDARY_MODIFIED

NEXT=REVIEW_AND_MERGE_THIS_PROOF_PR
THEN=PREPARE_NW008_AT1_GHL_PIT_ROTATION_AUTHORIZATION_001
```
