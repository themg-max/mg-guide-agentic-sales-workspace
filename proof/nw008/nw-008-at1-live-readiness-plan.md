# NW-008 AT-1 Live Readiness Plan

## 1. Planning identity and authority boundary

```text
CLASSIFICATION=planning_only
PLANNING_ID=NW008_AT1_LIVE_READINESS_001

PLAN_BASE_SHA=028fbb221deb95d6e250dc7b02f8d4eb39848cb7
SOURCE_RECONCILIATION_HEAD_SHA=7a2c4ea9b01cf0d0ca4d00fde889678099498d49
SOURCE_RECONCILIATION_MERGE_SHA=028fbb221deb95d6e250dc7b02f8d4eb39848cb7

PR71_REVIEWED_HEAD=c52261b1d5755b36bc7a3ba487edb085ddc9b9b8
PR71_MERGE_SHA=6d33fa550b709cd321874a0bf83caa4ab04909ab
IMPLEMENTATION_ID=NW008_AT1_LIVE_TRANSPORT_EVIDENCE_REMEDIATION_IMPL_001

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

This plan defines prerequisites for a possible future authorized AT-1 live
execution. It does not prepare, draft, countersign, or execute Grant009. It does
not authorize GHL calls, MCP initialization or probing, endpoint connectivity
tests, private-binding refresh, secret or token access, IAM changes, deployment,
or live transport.

```text
RUNTIME_IMPLEMENTATION_IN_SCOPE=NO
TEST_OR_FIXTURE_MUTATION_IN_SCOPE=NO
NETWORK_CALLS_IN_SCOPE=0
GHL_CALLS_IN_SCOPE=0
MCP_CALLS_IN_SCOPE=0
PRIVATE_BINDING_ACCESS_IN_SCOPE=NO
GRANT009_DRAFTING_IN_SCOPE=NO
```

## 2. Frozen readiness requirements

```text
ESTABLISHED_SESSION_IMPLEMENTATION_IDENTIFIED=REQUIRED
ESTABLISHED_SESSION_IMPLEMENTATION_REVIEWED=REQUIRED

MCP_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=REQUIRED
MCP_RESPONSE_SCHEMA_VERSION_FROZEN=REQUIRED

PRE_GRANT_SESSION_ESTABLISHMENT_REQUIRED=YES

POST_GRANT_INITIALIZE_ALLOWED=NO
POST_GRANT_PROBE_ALLOWED=NO
POST_GRANT_SESSION_REPAIR_ALLOWED=NO
POST_GRANT_FALLBACK_ALLOWED=NO

USE_BOUNDED_AT1_EXECUTOR=REQUIRED
USE_AT1_LIVE_TRANSPORT_SERIALIZER=REQUIRED
USE_AT1_LIVE_TRANSPORT_ADAPTER=REQUIRED
AD_HOC_INLINE_LIVE_RUNNER=FORBIDDEN

DURABLE_STORE_LOCATION_DEFINED=REQUIRED
DURABLE_STORE_PRIVATE=YES

COMMITMENT_KEY_SOURCE_DEFINED=REQUIRED
COMMITMENT_KEY_PRIVATE=YES
COMMITMENT_KEY_PUBLICATION_ALLOWED=NO

GRANT_RUN_ID_BINDING_REQUIRED=YES
SESSION_IDENTITY_BINDING_REQUIRED=YES

PRIVATE_REQUEST_CAPTURE_REQUIRED=YES
PRIVATE_RESPONSE_CAPTURE_REQUIRED=YES
PUBLIC_SANITIZED_PROJECTION_REQUIRED=YES

PROCESS_RESTART_NO_RETRY_REQUIRED=YES
CONCURRENT_EXECUTION_CLAIM_REJECTED=YES

GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

## 3. Static evidence inventory and current verdict

The reviewed implementation is durable on `main` and provides:

- `BoundedAt1GhlExecutor`, which creates all business envelopes through
  `At1LiveTransportSerializer`;
- `At1LiveTransportAdapter`, which validates those envelopes, captures requests
  before dispatch, captures responses before parsing, and invokes only an
  injected `EstablishedSession.execute_operation` seam;
- `At1ExecutionStore`, which accepts an injected SQLite path and HMAC commitment
  key, atomically claims `grant_run_id`, persists private request/response
  envelopes, refuses unresolved runs after restart, and derives an allowlisted
  public projection; and
- deterministic synthetic tests for post-grant initialize/probe refusal,
  restart refusal, concurrent claim rejection, private/public evidence
  separation, and commitment binding.

Static inspection also establishes that:

1. `EstablishedSession` is a `Protocol`, not a concrete session implementation.
   The only implementing class in the repository is
   `ScriptedEstablishedSession` under tests, and it is synthetic-only.
2. The adapter contains a reviewed parser for one response shape
   (`result.isError`, `result.content[0].operationId`, `success`, `status`, and
   `payload`), but the repository has no independently identified,
   versioned MCP response-schema authority.
3. No reviewed procedure or component establishes and seals a live MCP session
   before grant activation.
4. The SQLite path and commitment key are constructor inputs. No future-run
   private location, key source, or immutable authorization/session/binding
   manifest is frozen by repository evidence.

Therefore this plan fails closed:

```text
ESTABLISHED_SESSION_IMPLEMENTATION_CURRENT_STATE=NOT_IDENTIFIED
MCP_RESPONSE_SCHEMA_AUTHORITY_CURRENT_STATE=NOT_IDENTIFIED
PRE_GRANT_SESSION_ESTABLISHMENT_PROCEDURE_CURRENT_STATE=NOT_FROZEN
DURABLE_STORE_PRIVATE_LOCATION_CURRENT_STATE=NOT_FROZEN
COMMITMENT_KEY_SOURCE_CURRENT_STATE=NOT_FROZEN
GRANT_RUN_SESSION_BINDING_CURRENT_STATE=NOT_IMPLEMENTED
LIVE_READINESS=FAIL
```

The fail verdict is a readiness result only. It does not invalidate the merged
offline remediation implementation and does not change historical Grant 008
truth.

## 4. Readiness questions

### A. Concrete `EstablishedSession` component

No current production component satisfies the protocol. The repository contains
only the protocol in
`src/integrations/ghl/at1_live_transport_adapter.py` and the synthetic
`ScriptedEstablishedSession` in
`tests/integrations/ghl/test_at1_live_transport_remediation.py`.

A future bounded implementation unit must add and review exactly one concrete
business-only component, provisionally named `At1EstablishedMcpSession`. It must:

- wrap an already initialized and capability-validated MCP session;
- expose only `execute_operation(request)`;
- preserve the request ID and exact adapter-provided request;
- return the complete unmodified MCP response envelope;
- contain no initialize, probe, repair, reconnect, retry, endpoint selection,
  raw REST, or fallback path after it is sealed; and
- expose a stable, non-secret session identity for pre-grant binding.

```text
ESTABLISHED_SESSION_IMPLEMENTATION_IDENTIFIED=REQUIRED
ESTABLISHED_SESSION_IMPLEMENTATION_REVIEWED=REQUIRED
CURRENT_CONCRETE_IMPLEMENTATION=NONE
SYNTHETIC_TEST_SESSION_IS_LIVE_AUTHORITY=NO
```

### B. Binding without serializer bypass

The only permitted future composition is:

```text
pre-established At1EstablishedMcpSession
  -> At1LiveTransportAdapter(session, store, grant_run_id, owner_id)
  -> BoundedAt1GhlExecutor(
       transport=adapter,
       serializer=At1LiveTransportSerializer()
     )
  -> BoundedAt1GhlExecutor.execute(binding, context)
```

The executor alone constructs operation envelopes through the reviewed
serializer. The adapter validates the serializer's exact output before capture
and dispatch. The established session is injected only into the adapter and
must not be reachable by the executor, launcher, or any alternate runner.

The future composition root may load validated private inputs and invoke
`execute`, but it may not construct envelopes, call `execute_operation`
directly, interpret responses, issue retries, or assign result flags.

```text
ZERO_SERIALIZER_BYPASS_REQUIRED=YES
ZERO_DIRECT_SESSION_DISPATCH_REQUIRED=YES
ZERO_ALTERNATE_RUNNER_REQUIRED=YES
RAW_REST_FALLBACK_ALLOWED=NO
```

### C. MCP response envelope authority

No authoritative source/version is identified by current repository evidence.
`At1LiveTransportAdapter._parse_response` and the synthetic fixture freeze the
implemented expectation, but implementation and fixtures are not independent
schema authority.

Before readiness can pass, a future bounded contract unit must:

1. identify the authoritative provider/source for the JSON-RPC/MCP envelope and
   nested `execute_operation` result;
2. record the source version, retrieval date, and immutable digest or reviewed
   source revision;
3. add a versioned repository contract for the exact accepted envelope;
4. prove the adapter parser and synthetic fixtures conform to that contract; and
5. fail closed on any unknown content encoding or schema version.

No schema discovery, MCP call, or remote retrieval is authorized by this plan.

```text
MCP_RESPONSE_SCHEMA_AUTHORITY_IDENTIFIED=REQUIRED
MCP_RESPONSE_SCHEMA_VERSION_FROZEN=REQUIRED
CURRENT_SCHEMA_AUTHORITY=NOT_IDENTIFIED
CURRENT_SCHEMA_VERSION=NOT_FROZEN
```

### D. Pre-grant session establishment

The exact control-plane procedure is not yet identifiable because the concrete
session component and schema authority are absent. A future reviewed procedure
must enumerate every required action and complete it under separate pre-grant
authority before grant activation. At minimum it must freeze:

1. endpoint/channel selection without fallback;
2. transport authentication and session creation;
3. MCP initialization and capability negotiation, if required by the
   authoritative protocol;
4. `execute_operation` availability and exact schema/version confirmation;
5. session identity capture;
6. protocol-ledger capture for every control-plane call; and
7. sealing the session into business-only mode.

The future grant may bind only the sealed session. If any prerequisite expires
or the session becomes unusable, the future run must stop and require a new
separate readiness decision; it must not repair the session after activation.

```text
PRE_GRANT_SESSION_ESTABLISHMENT_REQUIRED=YES
PRE_GRANT_CONTROL_PLANE_AUTHORITY_REQUIRED=SEPARATE
CURRENT_EXACT_CONTROL_PLANE_SEQUENCE=NOT_FROZEN
```

### E. Proof of zero post-grant control-plane activity

Current static evidence proves that the adapter's exposed session seam has only
`execute_operation` and that `record_protocol_call` rejects synthetic
`initialize` and `probe` attempts after activation. That is necessary but not
sufficient: an unidentified concrete session could perform hidden control-plane
work internally.

Future readiness must prove all of the following:

- the reviewed concrete session has no post-seal initialize, probe, reconnect,
  repair, endpoint fallback, or raw REST code path;
- the composition root activates the grant only after session sealing and
  protocol-ledger finalization;
- the protocol ledger is immutable for the active grant while business
  ordinals execute;
- deterministic tests inject each forbidden action and prove zero underlying
  transport calls; and
- the sanitized projection reports the frozen pre-grant protocol count
  independently from the business dispatch count.

```text
POST_GRANT_INITIALIZE_ALLOWED=NO
POST_GRANT_PROBE_ALLOWED=NO
POST_GRANT_SESSION_REPAIR_ALLOWED=NO
POST_GRANT_FALLBACK_ALLOWED=NO
CURRENT_ADAPTER_LEVEL_REFUSAL_PROVEN=YES
END_TO_END_SESSION_LEVEL_REFUSAL_PROVEN=NO
```

### F. Durable SQLite evidence location

The future database must live on a persistent, owner-access-controlled private
control-plane filesystem outside every git worktree and outside temporary
directories. The exact private absolute path must be frozen in the private
readiness packet before any future Grant009 preparation decision. It must not be
published in this repository.

The private readiness check must prove the parent directory is durable,
owner-only, non-symlinked, writable, excluded from backup/publication paths, and
that the same database path is reused after process restart for the bound
`grant_run_id`.

```text
DURABLE_STORE_LOCATION_DEFINED=REQUIRED
DURABLE_STORE_LOCATION_CLASS=PRIVATE_PERSISTENT_CONTROL_PLANE_FILESYSTEM_OUTSIDE_GIT
DURABLE_STORE_PRIVATE=YES
DURABLE_STORE_TEMPORARY_ALLOWED=NO
DURABLE_STORE_EXACT_PATH_PUBLICATION_ALLOWED=NO
CURRENT_EXACT_PRIVATE_PATH=NOT_FROZEN
```

### G. HMAC/commitment key source

The future key must be a per-grant/run, minimum 256-bit random key generated by
an approved cryptographic random source before grant activation. It must be
placed in the private control-plane run package, loaded into memory before
adapter construction, and never written to the public projection, logs, proof,
git, command history, or process arguments.

The private readiness packet must bind a non-secret key identifier and key
provenance to the run manifest. It must not publish the key or any reversible
derivation input. This plan does not access Secret Manager or any private key
source.

```text
COMMITMENT_KEY_SOURCE_DEFINED=REQUIRED
COMMITMENT_KEY_SOURCE_CLASS=PRE_GRANT_PRIVATE_CSPRNG_RUN_PACKAGE
COMMITMENT_KEY_MINIMUM_BITS=256
COMMITMENT_KEY_PRIVATE=YES
COMMITMENT_KEY_PUBLICATION_ALLOWED=NO
CURRENT_KEY_SOURCE_INSTANCE=NOT_PROVISIONED
```

### H. Private/public evidence separation

Raw request and response envelopes remain only in the private SQLite database
outside git. The public path is only
`At1ExecutionStore.compute_public_projection()`, which emits counters,
predicates, failure codes, and HMAC commitments rather than raw envelopes.
Existing synthetic sentinel tests prove private IDs, note content, and
idempotency keys do not appear in that projection.

Future operation must additionally:

- prohibit raw request/response printing and exception interpolation;
- permit public proof generation only from an explicit projection allowlist;
- scan every proposed public artifact for private sentinels and forbidden
  fields;
- stage public proof by exact named path only; and
- reject any public projection whose commitments cannot be matched privately.

```text
PRIVATE_REQUEST_CAPTURE_REQUIRED=YES
PRIVATE_RESPONSE_CAPTURE_REQUIRED=YES
PUBLIC_SANITIZED_PROJECTION_REQUIRED=YES
RAW_PRIVATE_EVIDENCE_IN_GIT_ALLOWED=NO
RAW_PRIVATE_EVIDENCE_IN_PUBLIC_LOGS_ALLOWED=NO
```

### I. Grant, authorization, session, and binding identity

A future bounded implementation unit must define an immutable run manifest and
persist its digest with the atomic execution claim before activation. The
manifest must bind:

- future `authorization_id`;
- unique `grant_run_id`;
- reviewed runtime and composition head SHA;
- response-schema authority ID and version;
- stable non-secret sealed-session identity;
- private binding package ID and immutable digest;
- durable-store identity;
- non-secret commitment-key identifier;
- owner/process claim identity; and
- activation timestamp and grant expiry.

The database must bind the manifest on first claim. A later process may reopen
the same `grant_run_id` only with the identical manifest and claim owner, and
the existing durable ordinal state must still prevent retry. A concurrent
owner, mismatched manifest digest, different session identity, or different
private binding digest must be rejected before transport. Public proof may
expose only approved non-secret IDs and commitments.

```text
GRANT_RUN_ID_BINDING_REQUIRED=YES
SESSION_IDENTITY_BINDING_REQUIRED=YES
AUTHORIZATION_ID_BINDING_REQUIRED=YES
PRIVATE_BINDING_PACKAGE_DIGEST_REQUIRED=YES
IMMUTABLE_RUN_MANIFEST_REQUIRED=YES
CURRENT_MANIFEST_IMPLEMENTATION=NONE
```

### J. Conditions for a separate Grant009 preparation decision

A future decision may consider Grant009 preparation only after all readiness
gates in section 6 are proven, every required future implementation/contract
unit is merged and reconciled on `main`, exact-head deterministic CI is green,
and a private readiness record attests the frozen session, store, key, and
binding package without publishing their private values.

That evidence permits only a separate human decision on whether preparation may
begin. It does not itself authorize drafting, countersignature, or execution.

```text
GRANT009_PREPARATION_DECISION_PERMITTED_NOW=NO
GRANT009_PREPARATION_REQUIRES_SEPARATE_AUTHORITY=YES
GRANT009_EXECUTION_REQUIRES_SEPARATE_COUNTERSIGNED_AUTHORITY=YES
```

## 5. Future bounded implementation units

The following units are prerequisites, not work authorized in this planning PR:

1. **Established session and composition unit:** implement the one reviewed
   established MCP session, pre-grant establishment/sealing procedure, and one
   composition root with no alternate runner or direct session path.
2. **Response contract unit:** identify and freeze the authoritative MCP
   response source/version, add a versioned contract, and bind parser/fixture
   tests to it.
3. **Run-manifest persistence unit:** bind authorization, grant/run, session,
   private binding, store, commitment-key identifier, and reviewed runtime into
   the durable atomic claim.
4. **Private operational readiness unit:** privately provision and attest the
   exact durable database path, commitment key instance, sealed session, and
   binding package under separate authority.

Each implementation unit requires its own bounded authorization, review,
deterministic tests, merge reconciliation, and static readiness evidence.

## 6. Live readiness pass contract

`LIVE_READINESS=PASS` may be recorded only when all rows are proven without live
GHL traffic:

| Required proof | Current state |
| --- | --- |
| Reviewed runtime composition identified | FAIL - concrete established session and composition root absent |
| Response-schema authority identified | FAIL - no independent source/version |
| Session establishment procedure frozen | FAIL - exact control-plane sequence absent |
| Pre/post-grant boundary frozen | FAIL - adapter boundary exists, end-to-end session boundary absent |
| Private durable store location frozen | FAIL - location class defined, exact private path not attested |
| Commitment-key handling frozen | FAIL - policy defined, private source instance not attested |
| Grant/run/session identity binding frozen | FAIL - immutable manifest absent |
| Request/response capture path frozen | PASS - reviewed adapter/store and synthetic tests |
| No-retry persistence frozen | PASS - durable restart refusal and atomic claim tests |
| Sanitized public projection frozen | PASS - allowlisted projection and sentinel tests |
| Zero alternate runner path | FAIL - no reviewed production composition root |
| Zero raw REST fallback | PASS for reviewed bounded runtime; must remain true in future session |
| Zero post-grant probes | FAIL end-to-end - adapter refusal exists, concrete session absent |

```text
LIVE_READINESS_PASS_REQUIRES_ALL_ROWS_PASS=YES
LIVE_READINESS=FAIL

PASS_ESTABLISHES_READINESS_ONLY=YES
PASS_AUTHORIZES_GRANT009_PREPARATION=NO
PASS_AUTHORIZES_GRANT009_EXECUTION=NO

GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO
```

## 7. Planning-lane validation and stop

This lane changes only this planning/proof artifact. No runtime, test, fixture,
workflow, governance, deployment, or private surface is modified. Validation is
limited to deterministic repository verification and static inspection; it
must not make network, GHL, MCP, credential, token, or private-binding calls.

```text
CHANGED_PATHS_ALLOWED=proof/nw008/nw-008-at1-live-readiness-plan.md
PLANNING_PROOF_SURFACES_ONLY=YES
LIVE_TRAFFIC_EXECUTED=NO

GRANT_008_STATE=CONSUMED
AT1_COMPLETE=NO

LIVE_GHL_EXECUTION_AUTHORIZED=NO
GRANT009_PREPARATION_AUTHORIZED=NO
GRANT009_EXECUTION_AUTHORIZED=NO

NEXT=LIVE_READINESS_PLAN_REVIEW
STOP=YES
```
