# NW-008 AT8W30 R3 Post-Reconciliation GET-Contact Execution Proof 002

```text
UNIT=NW008_AT8W30_R3_POST_RECONCILIATION_GET_CONTACT_EXECUTION_002
OPERATION_ID=get-contact
METHOD=GET
PATH=/contacts/{private_binding.contact_id}

EXPECTED_PUBLIC_MAIN=2d3d9fcb927e48e048878f098e173cfb78558eb0
PUBLIC_ORIGIN_MAIN=2d3d9fcb927e48e048878f098e173cfb78558eb0
PUBLIC_BASE_MATCH=YES
EXECUTION_BRANCH=exec/nw008-at8w30-r3-post-reconciliation-get-contact-execution-002
EXECUTION_BRANCH_IS_MAIN=NO
NO_UNRELATED_PUBLIC_WORKTREE_CHANGES=YES

CONTINUATION_MODE=POST_RECONCILIATION_FRESH_EXECUTION_PROCESS
IS_R3_RETRY_AFTER_CONSUMPTION=NO

R3_EXECUTION_AUTHORITY_SOURCE=PR233_ONLY
AUTHORIZATION_PR=233
PR233_AUTHORIZATION_MERGE=ba64aa661019d26902ca8122dfa107cc57d73366

PRIVATE_DEPENDENCY_PR=3137
PRIVATE_DEPENDENCY_EXPECTED_HEAD_DECLARED=YES
PRIVATE_BINDING_INPUT_IS_AUTHORITY=NO
PRIVATE_BINDING_INPUT_IS_DATA=YES

PRIVATE_DESIGNATED_ROOT_POINTER_USED=DESIGNATED_PROVISIONED_SURFACE_ONLY
PRIVATE_ROOT_REDISCOVERY_PERFORMED=NO
PRIVATE_ROOT_BROAD_FILESYSTEM_SEARCH=NO
PRIVATE_ROOT_TRANSCRIPT_DERIVED=NO
PRIVATE_ROOT_NEAREST_GIT_ROOT_FALLBACK=NO
PRIVATE_ROOT_ALTERNATE_CHECKOUT_FALLBACK=NO

PRIVATE_DESIGNATED_ROOT_PRESENT=YES
PRIVATE_RESOLVED_REPO_IS_EXPECTED_REPOSITORY=YES
PRIVATE_EXPECTED_HEAD_MATCH=NO
PRIVATE_RESOLVED_HEAD_IS_DESCENDANT_OF_EXPECTED_HEAD=NO
PRIVATE_RESOLVED_CHECKOUT_ON_UNRELATED_DIVERGENT_BRANCH=YES
PRIVATE_WORKTREE_CLEAN_OR_EXPECTED=CLEAN_BUT_NOT_EXPECTED_HEAD
PRIVATE_OWNER_MODULE_ORIGIN_WITHIN_DESIGNATED_ROOT=NOT_EVALUATED_STOPPED_AT_ROOT_GATE

GENUINE_PRIVATE_ANCHOR_PRESENT=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
GENUINE_RESOLVER_PRESENT=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
GENUINE_PROVISION_RECOGNITION=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
CONSUMER_AUTH_IDENTITY_MATCH=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
WORKFLOW_RUN_IDENTITY_MATCH=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
PRIVATE_BINDING_CONTINUITY=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
PROCESS_LOCAL_MEMBERSHIP_READY=NOT_EVALUATED_STOPPED_AT_ROOT_GATE
PRIVATE_PROVENANCE_READY=NOT_EVALUATED_STOPPED_AT_ROOT_GATE

TARGET_PROVENANCE_VERIFIED=NO
OPAQUE_PRIVATE_BINDING_REFERENCE_MATERIALIZED=NO

R3_RESULT=BLOCKED_PRE_TRIGGER
CREDENTIAL_CONSTRUCTION_TRIGGER_CROSSED=NO

PR233_AUTHORIZATION_STATE=AVAILABLE_UNCONSUMED
PR233_AUTHORIZATION_CONSUMED=NO
R3_EXECUTION_ATTEMPTS_USED=0

TARGET_RUNTIME_CREDENTIAL_OBJECT_CONSTRUCTIONS=0
SERVICE_ACCOUNT_IMPERSONATION_ATTEMPTS=0
SERVICE_ACCOUNT_ACCESS_TOKEN_MINTS=0
SECRET_MANAGER_CLIENT_INSTANTIATIONS=0
SECRET_PAYLOAD_READS=0
AT1_EXECUTION_STORE_CONSTRUCTIONS=0
AT1_EXECUTION_STORE_EXISTING_OPENS=0
PRODUCTION_RUNTIME_ASSEMBLY=0

HIGHLEVEL_HTTP_CLIENT_INSTANTIATIONS=0
HIGHLEVEL_TRANSPORT_INSTANTIATIONS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
GET_CONTACT_ATTEMPTS=0

GET_OPPORTUNITY_ATTEMPTS=0
SEARCH_CALLS=0
LIST_CALLS=0
PAGINATION_CALLS=0

CONTACT_ID_MATCH=NO
LOCATION_ID_MATCH=NO

RETRY_COUNT=0
WRITES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
SECRET_MUTATIONS=0
DEPLOYMENTS=0

NOTE_WRITE_ATTEMPTS=0
STAGE_WRITE_ATTEMPTS=0

R4_AUTHORIZED=NO
R4_PERFORMED=NO

SECOND_EXECUTION_AUTHORIZED=NO
RETRY_AUTHORIZED=NO

PRIVATE_VALUES_DISCLOSED=NO
RAW_PROVIDER_RESPONSE_DISCLOSED=NO
RAW_PROVIDER_RESPONSE_LOGGED=NO
RAW_PROVIDER_RESPONSE_PERSISTED=NO

PUBLIC_PROOF_PATH=proof/nw008/at-8w30/nw008-at8w30-r3-post-reconciliation-get-contact-execution-proof-002.md
VALIDATION=PASS_SANITIZED_TERMINAL_LEDGER_RECONCILIATION
STOP_CODE=VALIDATED_PRIVATE_EXECUTION_ROOT_UNAVAILABLE_OR_CHANGED
```

## Terminal disposition

The public pre-flight gate passed against the exact required public baseline: the
fetched public origin main equalled the declared expected main, the execution
lane was a fresh non-main branch cut from that baseline, and the public worktree
carried no unrelated changes.

The execution process then resolved the private dependency root exclusively from
the designated provisioned private-owner execution surface. No broad filesystem
search, transcript-derived locator, nearest-git-root heuristic, stale worktree
selection, or caller-selected private implementation was used.

The designated root was present and resolved to the expected private repository,
but its checked-out head did not equal the declared expected private head for
private PR 3137. The resolved head was not a descendant of the expected head
either; the designated checkout was sitting on an unrelated divergent branch.
The worktree itself was free of modified or untracked entries, so this is a head
divergence of the designated root rather than local dirt.

Because the required private execution root no longer matched the state that the
reconciliation validated, the process stopped at the private-root gate. It did
not silently fall back to any other checkout, did not move, fetch, reset, or
check out anything in the private root, and did not continue into same-process
anchor, resolver, provenance, identity, or binding-continuity re-establishment.

No opaque private binding reference was materialized. The irreversible PR233
consumption trigger — the first target-runtime credential object construction
attempt for R3 — was never begun. There was no impersonation, no token mint, no
Secret Manager client instantiation, no secret payload read, no execution-store
construction or open, no production runtime assembly, no HighLevel client or
transport instantiation, and no provider dispatch.

PR233 therefore remains available and unconsumed with zero R3 execution attempts
used. This unit was not retried and no second execution process was started. R4
was neither authorized nor performed. No runtime source was modified in response
to this blocked execution.

No private binding value, private contact or location identifier, private
locator or worktree path, credential material, token value, secret payload,
opaque-reference internal, or raw provider response appears in this proof.

## Required remediation before any further R3 attempt

The designated private execution root must be restored to, and independently
re-validated at, the declared expected private head for private PR 3137 under
private-owner control. A fresh governed start-gate acceptance should then confirm
the root gate before another R3 execution process is opened. PR233 remains the
sole execution authority and is still unconsumed, so no new authorization is
required — only a corrected private dependency root.
